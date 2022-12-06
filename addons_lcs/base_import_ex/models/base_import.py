# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime
import io
import itertools
import logging
import psycopg2
import operator
import os
import re

from odoo import api, fields, models, helper
from odoo.tools.translate import _
from odoo.tools.mimetypes import guess_mimetype
from odoo.tools.misc import ustr
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, pycompat
from xml.etree import ElementTree
from odoo.modules.module import get_module_resource

FIELDS_RECURSION_LIMIT = 2
ERROR_PREVIEW_BYTES = 200
_logger = logging.getLogger(__name__)

try:
    import xlrd
    try:
        from xlrd import xlsx
    except ImportError:
        xlsx = None
except ImportError:
    xlrd = xlsx = None

try:
    from . import odf_ods_reader
except ImportError:
    odf_ods_reader = None

FILE_TYPE_DICT = {
    'text/csv': ('csv', True, None),
    'application/vnd.ms-excel': ('xls', xlrd, 'xlrd'),
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ('xlsx', xlsx, 'xlrd >= 1.0.0'),
    'application/vnd.oasis.opendocument.spreadsheet': ('ods', odf_ods_reader, 'odfpy')
}
EXTENSIONS = {
    '.' + ext: handler
    for mime, (ext, handler, req) in FILE_TYPE_DICT.items()
}

MODULE = 'base_import_ex'
DICT_ACCOUNT = {"CreditAccount":"TK_CO_ID", 
            "DebitAccount":"TK_NO_ID", 
            "DeductionDebitAccount":"TK_DU_THUE_GTGT_ID", 
            "DiscountAccount":"TK_CHIET_KHAU_ID", 
            "EnvironmentalTaxAccount":"TK_THUE_BVMT_ID", 
            "ExportTaxAccount":"TK_THUE_XK_ID", 
            "ImportTaxAccount":"TK_THUE_NK_ID", 
            "SpecialConsumeTaxAccount":"TK_THUE_TTDB_ID", 
            "VATAccount":"TK_THUE_GTGT_ID"}

class Import(models.TransientModel):

    _name = 'base_import_ex.import'

    # allow imports to survive for 12h in case user is slow
    _transient_max_hours = 12.0

    res_model = fields.Char('Model')
    file = fields.Binary('File', help="File to check and/or import, raw binary (not base64)")
    file_name = fields.Char('File Name')
    file_type = fields.Char('File Type')
    parent_id = fields.Many2one('base_import_ex.import')

    @api.model
    def get_fields(self, model, depth=FIELDS_RECURSION_LIMIT):
        """ Recursively get fields for the provided model (through
        fields_get) and filter them according to importability

        The output format is a list of ``Field``, with ``Field``
        defined as:

        .. class:: Field

            .. attribute:: id (str)

                A non-unique identifier for the field, used to compute
                the span of the ``required`` attribute: if multiple
                ``required`` fields have the same id, only one of them
                is necessary.

            .. attribute:: name (str)

                The field's logical (Odoo) name within the scope of
                its parent.

            .. attribute:: string (str)

                The field's human-readable name (``@string``)

            .. attribute:: required (bool)

                Whether the field is marked as required in the
                model. Clients must provide non-empty import values
                for all required fields or the import will error out.

            .. attribute:: fields (list(Field))

                The current field's subfields. The database and
                external identifiers for m2o and m2m fields; a
                filtered and transformed fields_get for o2m fields (to
                a variable depth defined by ``depth``).

                Fields with no sub-fields will have an empty list of
                sub-fields.

        :param str model: name of the model to get fields form
        :param int landing: depth of recursion into o2m fields
        """
        Model = self.env[model]
        importable_fields = [{
            'id': 'id',
            'name': 'id',
            'string': _("External ID"),
            'required': False,
            'fields': [],
            'type': 'id',
        }]
        model_fields = Model.fields_get()
        blacklist = models.MAGIC_COLUMNS + [Model.CONCURRENCY_CHECK_FIELD]
        for name, field in model_fields.items():
            if name in blacklist:
                continue
            # an empty string means the field is deprecated, @deprecated must
            # be absent or False to mean not-deprecated
            if field.get('deprecated', False) is not False:
                continue
            if field.get('readonly'):
                states = field.get('states')
                if not states:
                    continue
                # states = {state: [(attr, value), (attr2, value2)], state2:...}
                if not any(attr == 'readonly' and value is False
                           for attr, value in itertools.chain.from_iterable(states.values())):
                    continue
            field_value = {
                'id': name,
                'name': name,
                'string': field['string'],
                # Y U NO ALWAYS HAS REQUIRED
                'required': bool(field.get('required')),
                'fields': [],
                'type': field['type'],
            }

            if field['type'] in ('many2many', 'many2one'):
                field_value['fields'] = [
                    dict(field_value, name='id', string=_("External ID"), type='id'),
                    dict(field_value, name='.id', string=_("Database ID"), type='id'),
                ]
            elif field['type'] == 'one2many' and depth:
                field_value['fields'] = self.get_fields(field['relation'], depth=depth-1)
                if self.user_has_groups('base.group_no_one'):
                    field_value['fields'].append({'id': '.id', 'name': '.id', 'string': _("Database ID"), 'required': False, 'fields': [], 'type': 'id'})

            importable_fields.append(field_value)

        # TODO: cache on model?
        return importable_fields

    @api.multi
    def _read_file(self, options):
        """ Dispatch to specific method to read file content, according to its mimetype or file type
            :param options : dict of reading options (quoting, separator, ...)
        """
        self.ensure_one()
        # guess mimetype from file content
        mimetype = guess_mimetype(self.file)
        (file_extension, handler, req) = FILE_TYPE_DICT.get(mimetype, (None, None, None))
        if handler:
            try:
                return getattr(self, '_read_' + file_extension)(options)
            except Exception:
                _logger.warn("Failed to read file '%s' (transient id %d) using guessed mimetype %s", self.file_name or '<unknown>', self.id, mimetype)

        # try reading with user-provided mimetype
        (file_extension, handler, req) = FILE_TYPE_DICT.get(self.file_type, (None, None, None))
        if handler:
            try:
                return getattr(self, '_read_' + file_extension)(options)
            except Exception:
                _logger.warn("Failed to read file '%s' (transient id %d) using user-provided mimetype %s", self.file_name or '<unknown>', self.id, self.file_type)

        # fallback on file extensions as mime types can be unreliable (e.g.
        # software setting incorrect mime types, or non-installed software
        # leading to browser not sending mime types)
        if self.file_name:
            p, ext = os.path.splitext(self.file_name)
            if ext in EXTENSIONS:
                try:
                    return getattr(self, '_read_' + ext[1:])(options)
                except Exception:
                    _logger.warn("Failed to read file '%s' (transient id %s) using file extension", self.file_name, self.id)

        if req:
            raise ImportError(_("Unable to load \"{extension}\" file: requires Python module \"{modname}\"").format(extension=file_extension, modname=req))
        raise ValueError(_("Unsupported file format \"{}\", import only supports CSV, ODS, XLS and XLSX").format(self.file_type))

    @api.multi
    def _read_xls(self, options):
        """ Read file content, using xlrd lib """
        book = xlrd.open_workbook(file_contents=self.file)
        return self._read_xls_book(book)

    def _read_xls_book(self, book):
        sheet = book.sheet_by_index(0)
        # emulate Sheet.get_rows for pre-0.9.4
        for row in pycompat.imap(sheet.row, range(sheet.nrows)):
            values = []
            for cell in row:
                if cell.ctype is xlrd.XL_CELL_NUMBER:
                    is_float = cell.value % 1 != 0.0
                    values.append(
                        pycompat.text_type(cell.value)
                        if is_float
                        else pycompat.text_type(int(cell.value))
                    )
                elif cell.ctype is xlrd.XL_CELL_DATE:
                    is_datetime = cell.value % 1 != 0.0
                    # emulate xldate_as_datetime for pre-0.9.3
                    dt = datetime.datetime(*xlrd.xldate.xldate_as_tuple(cell.value, book.datemode))
                    values.append(
                        dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                        if is_datetime
                        else dt.strftime(DEFAULT_SERVER_DATE_FORMAT)
                    )
                elif cell.ctype is xlrd.XL_CELL_BOOLEAN:
                    values.append(u'True' if cell.value else u'False')
                elif cell.ctype is xlrd.XL_CELL_ERROR:
                    raise ValueError(
                        _("Error cell found while reading XLS/XLSX file: %s") %
                        xlrd.error_text_from_code.get(
                            cell.value, "unknown error code %s" % cell.value)
                    )
                else:
                    values.append(cell.value)
            if any(x for x in values if x.strip()):
                yield values

    # use the same method for xlsx and xls files
    _read_xlsx = _read_xls

    @api.multi
    def _read_ods(self, options):
        """ Read file content using ODSReader custom lib """
        doc = odf_ods_reader.ODSReader(file=io.BytesIO(self.file))

        return (
            row
            for row in doc.getFirstSheet()
            if any(x for x in row if x.strip())
        )

    @api.multi
    def _read_csv(self, options):
        """ Returns a CSV-parsed iterator of all empty lines in the file
            :throws csv.Error: if an error is detected during CSV parsing
            :throws UnicodeDecodeError: if ``options.encoding`` is incorrect
        """
        csv_data = self.file

        # TODO: guess encoding with chardet? Or https://github.com/aadsm/jschardet
        encoding = options.get('encoding', 'utf-8')
        if encoding != 'utf-8':
            # csv module expect utf-8, see http://docs.python.org/2/library/csv.html
            csv_data = csv_data.decode(encoding).encode('utf-8')

        csv_iterator = pycompat.csv_reader(
            io.BytesIO(csv_data),
            quotechar=str(options['quoting']),
            delimiter=str(options['separator']))

        return (
            row for row in csv_iterator
            if any(x for x in row if x.strip())
        )

    @api.model
    def _try_match_column(self, preview_values, options):
        """ Returns the potential field types, based on the preview values, using heuristics
            :param preview_values : list of value for the column to determine
            :param options : parsing options
        """
        # If all values are empty in preview than can be any field
        if all([v == '' for v in preview_values]):
            return ['all']
        # If all values starts with __export__ this is probably an id
        if all(v.startswith('__export__') for v in preview_values):
            return ['id', 'many2many', 'many2one', 'one2many']
        # If all values can be cast to int type is either id, float or monetary
        # Exception: if we only have 1 and 0, it can also be a boolean
        try:
            field_type = ['id', 'integer', 'char', 'float', 'monetary', 'many2one', 'many2many', 'one2many']
            res = set(int(v) for v in preview_values if v)
            if {0, 1}.issuperset(res):
                field_type.append('boolean')
            return field_type
        except ValueError:
            pass
        # If all values are either True or False, type is boolean
        if all(val.lower() in ('true', 'false', 't', 'f', '') for val in preview_values):
            return ['boolean']
        # If all values can be cast to float, type is either float or monetary
        # Or a date/datetime if it matches the pattern
        results = []
        try:
            thousand_separator = decimal_separator = False
            for val in preview_values:
                val = val.strip()
                if not val:
                    continue
                # value might have the currency symbol left or right from the value
                val = self._remove_currency_symbol(val)
                if val:
                    if options.get('float_thousand_separator') and options.get('float_decimal_separator'):
                        val = val.replace(options['float_thousand_separator'], '').replace(options['float_decimal_separator'], '.')
                    # We are now sure that this is a float, but we still need to find the
                    # thousand and decimal separator
                    else:
                        if val.count('.') > 1:
                            options['float_thousand_separator'] = '.'
                            options['float_decimal_separator'] = ','
                        elif val.count(',') > 1:
                            options['float_thousand_separator'] = ','
                            options['float_decimal_separator'] = '.'
                        elif val.find('.') > val.find(','):
                            thousand_separator = ','
                            decimal_separator = '.'
                        elif val.find(',') > val.find('.'):
                            thousand_separator = '.'
                            decimal_separator = ','
                else:
                    # This is not a float so exit this try
                    float('a')
            if thousand_separator and not options.get('float_decimal_separator'):
                options['float_thousand_separator'] = thousand_separator
                options['float_decimal_separator'] = decimal_separator
            results  = ['float', 'monetary']
        except ValueError:
            pass
        # Try to see if all values are a date or datetime
        dt = datetime.datetime
        separator = [' ', '/', '-']
        date_format = ['%mr%dr%Y', '%dr%mr%Y', '%Yr%mr%d', '%Yr%dr%m']
        date_patterns = [options['date_format']] if options.get('date_format') else []
        if not date_patterns:
            date_patterns = [pattern.replace('r', sep) for sep in separator for pattern in date_format]
            date_patterns.extend([p.replace('Y', 'y') for p in date_patterns])
        datetime_patterns = [options['datetime_format']] if options.get('datetime_format') else []
        if not datetime_patterns:
            datetime_patterns = [pattern + ' %H:%M:%S' for pattern in date_patterns]

        current_date_pattern = False
        current_datetime_pattern = False

        def check_patterns(patterns, preview_values):
            for pattern in patterns:
                match = True
                for val in preview_values:
                    if not val:
                        continue
                    try:
                        dt.strptime(val, pattern)
                    except ValueError:
                        match = False
                        break
                if match:
                    return pattern
            return False

        current_date_pattern = check_patterns(date_patterns, preview_values)
        if current_date_pattern:
            options['date_format'] = current_date_pattern
            results += ['date']

        current_datetime_pattern = check_patterns(datetime_patterns, preview_values)
        if current_datetime_pattern:
            options['datetime_format'] = current_datetime_pattern
            results += ['datetime']

        if results:
            return results
        return ['id', 'text', 'char', 'datetime', 'selection', 'many2one', 'one2many', 'many2many', 'html']

    @api.model
    def _find_type_from_preview(self, options, preview):
        type_fields = []
        if preview:
            for column in range(0, len(preview[0])):
                preview_values = [value[column].strip() for value in preview]
                type_field = self._try_match_column(preview_values, options)
                type_fields.append(type_field)
        return type_fields

    def _match_header(self, header, fields, options):
        """ Attempts to match a given header to a field of the
            imported model.

            :param str header: header name from the CSV file
            :param fields:
            :param dict options:
            :returns: an empty list if the header couldn't be matched, or
                      all the fields to traverse
            :rtype: list(Field)
        """
        string_match = None
        for field in fields:
            # FIXME: should match all translations & original
            # TODO: use string distance (levenshtein? hamming?)
            if header.lower() == field['name'].lower():
                return [field]
            if header.lower() == field['string'].lower():
                # matching string are not reliable way because
                # strings have no unique constraint
                string_match = field
        if string_match:
            # this behavior is only applied if there is no matching field['name']
            return [string_match]

        if '/' not in header:
            return []

        # relational field path
        traversal = []
        subfields = fields
        # Iteratively dive into fields tree
        for section in header.split('/'):
            # Strip section in case spaces are added around '/' for
            # readability of paths
            match = self._match_header(section.strip(), subfields, options)
            # Any match failure, exit
            if not match:
                return []
            # prep subfields for next iteration within match[0]
            field = match[0]
            subfields = field['fields']
            traversal.append(field)
        return traversal

    def _match_headers(self, rows, fields, options):
        """ Attempts to match the imported model's fields to the
            titles of the parsed CSV file, if the file is supposed to have
            headers.

            Will consume the first line of the ``rows`` iterator.

            Returns a pair of (None, None) if headers were not requested
            or the list of headers and a dict mapping cell indices
            to key paths in the ``fields`` tree

            :param Iterator rows:
            :param dict fields:
            :param dict options:
            :rtype: (None, None) | (list(str), dict(int: list(str)))
        """
        if not options.get('headers'):
            return [], {}

        headers = next(rows)
        return headers, {
            index: [field['name'] for field in self._match_header(header, fields, options)] or None
            for index, header in enumerate(headers)
        }
    ##########################################################################
    #############################START IMPORTIMG##############################
    ##########################################################################
    # Chi nhánh/Đơn vị
    def _import_OrganizationUnit(self, tag):
        rec_model = 'danh.muc.to.chuc'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'OrganizationUnitID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'OrganizationUnitCode':
                res['MA_DON_VI'] = child.text
            elif child.tag == 'OrganizationUnitName':
                res['TEN_DON_VI'] = child.text
            elif child.tag == 'MISACodeID':
                res['MA_PHAN_CAP'] = child.text
            elif child.tag == 'ParentID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['parent_id'] = rid.id
            elif child.tag == 'Address':
                res['DIA_CHI'] = child.text
            elif child.tag == 'OrganizationUnitTypeID':
                res['CAP_TO_CHUC'] = child.text
            
            #vũ sửa hạch toán
            elif child.tag == 'IsDependent':
                if child.text =='true':
                    res['HACH_TOAN_SELECTION'] = 'PHU_THUOC'
                else:
                    res['HACH_TOAN_SELECTION'] = 'DOC_LAP'

            elif child.tag == 'IsPrivateVATDeclaration':
                res['KE_KHAI_THUE_GTGT_TTDB_RIENG'] = bool(child.text)
            elif child.tag == 'CompanyTaxCode':
                res['MA_SO_THUE'] = child.text
            elif child.tag == 'CompanyTel':
                res['DIEN_THOAI'] = child.text
            elif child.tag == 'CompanyFax':
                res['FAX'] = child.text
            elif child.tag == 'IsPrivateVATDeclaration':
                res['KE_KHAI_THUE_GTGT_TTDB_RIENG'] = bool(child.text)
            elif child.tag == 'DirectorTitle':
                res['NGUOI_KY_CHUC_DANH_GIAM_DOC'] = child.text
            elif child.tag == 'DirectorName':
                res['NGUOI_KY_TEN_GIAM_DOC'] = child.text
            elif child.tag == 'ChiefOfAccountingTitle':
                res['NGUOI_KY_CHUC_DANH_KE_TOAN_TRUONG'] = child.text
            elif child.tag == 'ChiefOfAccountingName':
                res['NGUOI_KY_TEN_KE_TOAN_TRUONG'] = child.text
            elif child.tag == 'StoreKeeperTitle':
                res['NGUOI_KY_CHUC_DANH_THU_KHO'] = child.text
            elif child.tag == 'StoreKeeperName':
                res['NGUOI_KY_TEN_THU_KHO'] = child.text
            elif child.tag == 'CashierTitle':
                res['NGUOI_KY_CHUC_DANH_THU_QUY'] = child.text
            elif child.tag == 'CashierName':
                res['NGUOI_KY_TEN_THU_QUY'] = child.text
            elif child.tag == 'ReporterTitle':
                res['NGUOI_KY_CHUC_DANH_NGUOI_LAP_BIEU'] = child.text
            elif child.tag == 'ReporterName':
                res['NGUOI_KY_TEN_NGUOI_LAP_BIEU'] = child.text

            elif child.tag == 'CostAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CHI_PHI_LUONG_ID'] = rid.id


            
            elif child.tag == 'BusinessRegistrationNumber':
                res['SO_DANG_KY'] = child.text
            elif child.tag == 'BusinessRegistrationNumberIssuedDate':
                res['NGAY_CAP'] = child.text
            elif child.tag == 'BusinessRegistrationNumberIssuedPlace':
                res['NOI_CAP'] = child.text
            elif child.tag == 'CompanyDistrict':
                res['QUAN_HUYEN'] = child.text
            elif child.tag == 'CompanyCity':
                res['TINH_TP'] = child.text
            
            elif child.tag == 'CompanyEmail':
                res['EMAIL'] = child.text
            elif child.tag == 'CompanyWebsite':
                res['WEBSITE'] = child.text
            
            elif child.tag == 'CompanyBankAccountNumber':
                rid = self.env['danh.muc.tai.khoan.ngan.hang'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NGAN_HANG_ID'] = rid.id
            elif child.tag == 'IsParent':           
                res['ISPARENT'] = True if child.text == 'true' else False
 
            
                
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Đối tượng/Nhà cung cấp/Khách hàng
    def _import_AccountObject(self, tag):
        rec_model = 'res.partner'
        res = {}
        rec_id = False
        id_quoc_gia = False
        id_tinh = False
        id_quan_huyen = False
        for child in tag.getchildren():
            if child.tag == 'AccountObjectID':
                rec_id = child.text
            elif child.tag == 'AccountObjectCode':
                res['MA'] = child.text
            elif child.tag == 'AccountObjectName':
                res['HO_VA_TEN'] = child.text
            elif child.tag == 'Address':
                res['DIA_CHI'] = child.text
            elif child.tag == 'CompanyTaxCode':
                res['MA_SO_THUE'] = child.text
            elif child.tag == 'AccountObjectGroupListCode':
                res['NHOM_KH_NCC_ID'] = [(6,0,self.env['danh.muc.nhom.khach.hang.nha.cung.cap'].search([('MA', 'in', child.text.split('; '))]).ids)]

            elif child.tag == 'Tel':
                res['DIEN_THOAI'] =  child.text

            elif child.tag == 'IssueDate':
                res['NGAY_CAP'] =  child.text

            elif child.tag == 'Mobile':
                res['DT_DI_DONG'] =  child.text
            elif child.tag == 'Fax':
                res['FAX'] = child.text
            elif child.tag == 'EmailAddress':
                res['EMAIL'] = child.text
            elif child.tag == 'Website':
                res['WEBSITE'] = child.text
            elif child.tag == 'DueTime':
                res['SO_NGAY_DUOC_NO'] = int(child.text)
            elif child.tag == 'MaximizeDebtAmount':
                res['SO_NO_TOI_DA'] = float(child.text)
            elif child.tag == 'EmployeeID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHAN_VIEN_ID'] = rid.id
            elif child.tag == 'PaymentTermID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DIEU_KHOAN_TT_ID'] = rid.id
            elif child.tag == 'Country':
                text = ''
                if child.text == 'Việt Nam':
                    text = 'Vietnam'
                else:
                    text = child.text
                rid = self.env['res.country'].search([('name', '=', text)], limit=1)
                if rid:
                    res['QUOC_GIA_ID'] = rid.id
                    id_quoc_gia = rid.id
            elif child.tag == 'Prefix':
                res['XUNG_HO'] = helper.Obj.convert_to_key(child.text)
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text


            elif child.tag == 'EInvoiceContactName':
                res['TEN_NGUOI_NHAN'] = child.text
            elif child.tag == 'EInvoiceContactMobile':
                res['DT_NGUOI_NHAN'] = child.text
           
            elif child.tag == 'EInvoiceContactEmail':
                res['EMAIL_NGUOI_NHAN'] = child.text
            elif child.tag == 'EInvoiceContactAddress':
                res['DIA_CHI_NGUOI_NHAN'] = child.text
            elif child.tag == 'LegalRepresentative':
                res['DAI_DIEN_THEO_PL'] = child.text
           

            elif child.tag == 'ContactName':
                res['HO_VA_TEN_LIEN_HE'] = child.text
            elif child.tag == 'ContactTitle':
                res['CHUC_DANH'] = child.text
            elif child.tag == 'ContactMobile':
                res['DT_DI_DONG_LIEN_HE'] = child.text
            elif child.tag == 'ContactFixedTel':
                res['DT_CO_DINH_LIEN_HE'] = child.text
            elif child.tag == 'ContactEmail':
                res['EMAIL_LIEN_HE'] = child.text
            elif child.tag == 'ContactAddress':
                res['DIA_CHI_LIEN_HE'] = child.text
            elif child.tag == 'OtherContactMobile':
                res['DTDD_KHAC_LIEN_HE'] = child.text
            
            elif child.tag == 'IdentificationNumber':
                res['SO_CMND'] = child.text
            elif child.tag == 'IssueBy':
                res['NOI_CAP'] = child.text

            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id

            elif child.tag == 'IsVendor':
                res['LA_NHA_CUNG_CAP'] = True if child.text == 'true' else False
            elif child.tag == 'IsCustomer':
                res['LA_KHACH_HANG'] = True if child.text == 'true' else False
            elif child.tag == 'IsEmployee':
                res['LA_NHAN_VIEN'] = True if child.text == 'true' else False
            elif child.tag == 'AccountObjectType':
                res['LOAI_KHACH_HANG'] = child.text
            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id

        for child in tag.getchildren():
            if child.tag == 'ProvinceOrCity':
                rid = self.env['res.country.state'].search([('name', '=', child.text),('country_id', '=', id_quoc_gia)], limit=1)
                if rid:
                    res['TINH_TP_ID'] = rid.id
                    id_tinh = rid.id

        for child in tag.getchildren():
            if child.tag == 'District':
                rid = self.env['res.country.state.district'].search([('TEN_DAY_DU', '=', child.text),('state_id', '=', id_tinh)], limit=1)
                if rid:
                    res['QUAN_HUYEN_ID'] = rid.id
                    id_quan_huyen =  rid.id
        
        for child in tag.getchildren():
            if child.tag == 'WardOrCommune':
                rid = self.env['res.country.state.district.ward'].search([('TEN_DAY_DU', '=', child.text),('district_id', '=', id_quan_huyen)], limit=1)
                if rid:
                    res['XA_PHUONG_ID'] = rid.id
        

        #vu: trùng code với hàm _compute_MA bên danh mục đối tượng
        if (res['LA_NHAN_VIEN']):
            res['MA_NHAN_VIEN']= res['MA']
            res['KIEU_DOI_TUONG']= 'NHAN_VIEN'

        if (res['LA_NHA_CUNG_CAP']):
            res['MA_NHA_CUNG_CAP']= res['MA']
            res['KIEU_DOI_TUONG']= 'NHA_CC'
            
        if (res['LA_KHACH_HANG']):
            res['MA_KHACH_HANG']= res['MA']
            res['KIEU_DOI_TUONG']= 'KHACH_HANG'
        
        
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # KH/ncc/đối tượng chi tiết (địa điểm giao hàng)
    def _import_AccountObjectShippingAddress(self, tag):
        rec_model = 'danh.muc.doi.tuong.dia.diem.giao.hang'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ShippingAddressID':
                rec_id = child.text
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'ShippingAddress':
                res['DIA_DIEM'] =child.text
            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)




    # Nhân viên
    def _import_Employee(self, tag):
        rec_model = 'res.partner'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'AccountObjectID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountObjectCode':
                res['MA_NHAN_VIEN'] = child.text
            elif child.tag == 'AccountObjectName':
                res['HO_VA_TEN'] = child.text
            
            elif child.tag == 'CompanyTaxCode':
                res['MA_SO_THUE'] = child.text
            elif child.tag == 'AgreementSalary':
                res['LUONG_THOA_THUAN'] =float(child.text)
            elif child.tag == 'ContactTitle':
                res['CHUC_DANH'] = child.text
            elif child.tag == 'InsuranceSalary':
                res['LUONG_DONG_GOP_BH'] = float(child.text)
            # elif child.tag == 'OrganizationUnitID':
            #     res['DON_VI_ID'] = self.env.ref('{}.{}'.format(MODULE,child.text), False).id
            elif child.tag == 'NumberOfDependent':
                res['SO_NGUOI_PHU_THUOC'] = int(child.text)
           

            elif child.tag == 'Gender':
                res['GIOI_TINH'] = child.text

            elif child.tag == 'BirthDate':
                res['NGAY_SINH'] = child.text
            elif child.tag == 'ModifiedDate':
                res['NGAY_CAP'] = child.text
            elif child.tag == 'SalaryCoefficient':
                res['HE_SO_LUONG'] = float(child.text)
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_ID'] = rid.id

            elif child.tag == 'Address':
                res['DIA_CHI_LIEN_HE'] = child.text
            elif child.tag == 'Tel':
                res['DT_CO_DINH_LIEN_HE'] = child.text
            elif child.tag == 'Mobile':
                res['DT_DI_DONG_LIEN_HE'] = child.text
            elif child.tag == 'EmailAddress':
                res['EMAIL_LIEN_HE'] = child.text
            elif child.tag == 'IsVendor':
                res['LA_NHA_CUNG_CAP'] = True if child.text == 'true' else False
            elif child.tag == 'IsCustomer':
                res['LA_KHACH_HANG'] = True if child.text == 'true' else False
            elif child.tag == 'IsEmployee':
                res['LA_NHAN_VIEN'] = True if child.text == 'true' else False
            elif child.tag == 'AccountObjectType':
                res['LOAI_KHACH_HANG'] = child.text
            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
            
            elif child.tag == 'BankAccount':
                res['SO_TAI_KHOAN'] = child.text
            elif child.tag == 'BankName':
                res['TEN_NGAN_HANG'] = child.text
            elif child.tag == 'BankBranchName':
                res['TEN_CHI_NHANH_NGAN_HANG'] = child.text
            elif child.tag == 'ProvinceOrCity':
                res['TINH_TP_CUA_NGAN_HANG'] = child.text
            elif child.tag == 'AccountObjectGroupListCode':
                res['NHOM_KH_NCC_ID'] = [(6,0,self.env['danh.muc.nhom.khach.hang.nha.cung.cap'].search([('MA', 'in', child.text.split('; '))]).ids)]
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

#detail khách hàng/ncc.đối tượng
    def _import_AccountObjectBankAccount(self, tag):
        rec_model = 'danh.muc.doi.tuong.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'AccountObjectBankAccountID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'BankAccount':
                res['SO_TAI_KHOAN'] = child.text
            elif child.tag == 'BankName':
                res['TEN_NGAN_HANG'] = child.text
            elif child.tag == 'BankBranchName':
                res['CHI_NHANH'] = child.text
            elif child.tag == 'ProvinceOrCity':
                res['TINH_TP_CUA_NGAN_HANG'] = child.text
           
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    # # Phiếu chi
    # def _import_CAPayment(self, tag):
    #     rec_model = 'account.ex.phieu.thu.chi'
    #     res = {'phieu_thu_chi':'phieu_chi'}
    #     rec_id = False
    #     for child in tag.getchildren():
    #         if child.tag == 'RefID':
    #             rec_id = child.text
    #         elif child.tag == 'JournalMemo':
    #             res['DIEN_GIAI_CHUNG'] = child.text
    #         elif child.tag == 'RefNoFinance':
    #             res['SO_CHUNG_TU'] = child.text
    #         elif child.tag == 'RefType':
    #             res['LOAI_CHUNG_TU'] = child.text
    #         elif child.tag == 'RefDate':
    #             res['NGAY_CHUNG_TU'] = child.text
    #         elif child.tag == 'PostedDate':
    #             res['NGAY_GHI_SO'] = child.text
    #         elif child.tag == 'AccountObjectID':
    #             res['DOI_TUONG_ID'] = self.env.ref('{}.{}'.format(MODULE,child.text), False).id
    #         elif child.tag == 'BranchID':
    #             res['CHI_NHANH_ID'] = self.env.ref('{}.{}'.format(MODULE,child.text), False).id
    #     return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # # Phiếu chi chi tiết
    # def _import_CAPaymentDetail(self, tag):
    #     rec_model = 'account.ex.phieu.thu.chi.tiet'
    #     res = {}
    #     rec_id = False
    #     for child in tag.getchildren():
    #         if child.tag == 'RefDetailID':
    #             rec_id = child.text
    #         elif child.tag == 'RefID':
    #             res['PHIEU_THU_CHI_ID'] = self.env.ref('{}.{}'.format(MODULE,child.text), False).id
    #         elif child.tag == 'Description':
    #             res['DIEN_GIAI'] = child.text
    #         elif child.tag == 'DebitAccount':
    #             res['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id 
    #         elif child.tag == 'CreditAccount':
    #             res['TK_CO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id 
    #         elif child.tag == 'Amount':
    #             res['SO_TIEN'] = float(child.text)
    #     return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # danh mục loại công cụ dụng cụ
    def _import_SupplyCategory(self, tag):
        rec_model = 'danh.muc.loai.cong.cu.dung.cu'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'SupplyCategoryID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'SupplyCategoryCode':
                res['MA'] = child.text
            elif child.tag == 'SupplyCategoryName':
                res['TEN'] = child.text
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'ParentID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['parent_id'] = rid.id
            elif child.tag == 'MISACodeID':
                res['MA_PHAN_CAP'] = child.text
            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # danh mục loại tài sản cố định
    def _import_FixedAssetCategory(self, tag):
        rec_model = 'danh.muc.loai.tai.san.co.dinh'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'FixedAssetCategoryID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'FixedAssetCategoryCode':
                res['MA'] = child.text
            elif child.tag == 'FixedAssetCategoryName':
                res['TEN'] = child.text
            # elif child.tag == 'Description':
            #     res['DIEN_GIAI'] = child.text
            elif child.tag == 'ParentID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['parent_id'] = rid.id
            elif child.tag == 'MISACodeID':
                res['MA_PHAN_CAP'] = child.text
            elif child.tag == 'OrgPriceAccount':
                res['TK_NGUYEN_GIA_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag == 'DepreciationAccount':
                res['TK_KHAU_HAO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag =='Inactive':
                res['active'] = False if child.text == 'true' else True
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    
    # danh mục vật tư hàng hóa
    # - vật tư hàng hóa 
    def _import_InventoryItem(self, tag):
        rec_model = 'danh.muc.vat.tu.hang.hoa'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'InventoryItemID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'InventoryItemCode':
                res['MA'] = child.text
            elif child.tag == 'InventoryItemName':
                res['TEN'] = child.text
            elif child.tag == 'InventoryItemType':
                res['TINH_CHAT'] = child.text
            elif child.tag == 'InventoryItemCategoryCode':
                res['NHOM_VTHH'] = [(6,0,self.env['danh.muc.nhom.vat.tu.hang.hoa.dich.vu'].search([('MA', 'in', child.text.split('; '))]).ids)] 
            elif child.tag == 'Description':
                res['MO_TA'] = child.text

            elif child.tag == 'UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_CHINH_ID'] = rid.id
            elif child.tag == 'MinimumStock':
                res['SO_LUONG_TON_TOI_THIEU'] = float(child.text)
            elif child.tag == 'InventoryItemSource':
                res['NGUON_GOC'] = child.text
            elif child.tag =='PurchaseDescription':
                res['DIEN_GIAI_KHI_MUA'] = child.text
            elif child.tag =='SaleDescription':
                res['DIEN_GIAI_KHI_BAN'] = child.text
            elif child.tag =='GuarantyPeriod':
                res['THOI_HAN_BH'] = helper.Obj.convert_to_key(child.text)
            elif child.tag =='DefaultStockID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHO_NGAM_DINH_ID'] = rid.id
                
            elif child.tag =='InventoryAccount':
                res['TAI_KHOAN_KHO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag =='SaleAccount':
                res['TK_DOANH_THU_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag =='DiscountAccount':
                res['TK_CHIET_KHAU_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag =='SaleOffAccount':
                res['TK_GIAM_GIA_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag =='ReturnAccount':
                res['TK_TRA_LAI_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag =='COGSAccount':
                res['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag =='PurchaseDiscountRate':
                res['TY_LE_CKMH'] = float(child.text)
            elif child.tag =='FixedUnitPrice':
                res['DON_GIA_MUA_CO_DINH'] = float(child.text)
            elif child.tag =='UnitPrice':
                res['DON_GIA_MUA_GAN_NHAT'] = float(child.text)
            elif child.tag =='SalePrice1':
                res['GIA_BAN_1'] = float(child.text)
            elif child.tag =='SalePrice2':
                res['GIA_BAN_2'] = float(child.text)
            elif child.tag =='SalePrice3':
                res['GIA_BAN_3'] = float(child.text)
            elif child.tag =='FixedSalePrice':
                res['GIA_CO_DINH'] = float(child.text)
            elif child.tag =='ImportTaxRate':
                res['THUE_SUAT_THUE_NK'] = float(child.text)
            elif child.tag =='ExportTaxRate':
                res['THUE_SUAT_THUE_XK'] = float(child.text)


            elif child.tag =='TaxRate':
                rid = self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:

                    res['THUE_SUAT_GTGT_ID'] = rid.id
            elif child.tag == 'InventoryCategorySpecialTaxID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHOM_HHDV_CHIU_THUE_TTDB_ID'] = rid.id
            elif child.tag =='IsSaleDiscount':
                res['CHIET_KHAU'] = False if child.text == 'false' else True
            elif child.tag =='IsFollowSerialNumber':
                res['THEO_DOI_THEO_MA_QUY_CACH'] = False if child.text == 'false' else True
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    # danh sách đơn giá mua cố định
    def _import_InventoryItemPurchaseFixedUnitPrice(self, tag):
        rec_model = 'danh.muc.vthh.don.gia.mua.co.dinh'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'InventoryItemDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['VAT_TU_HANG_HOA_ID'] = rid.id
            elif child.tag == 'UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_TINH_ID'] = rid.id
            elif child.tag == 'UnitPrice':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'CurrencyID':
                res['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1).id

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # danh sách đơn giá mua gần nhất
    def _import_InventoryItemPurchaseUnitPrice(self, tag):
        rec_model = 'danh.muc.vthh.don.gia.mua.gan.nhat'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'InventoryItemDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['VAT_TU_HANG_HOA_ID'] = rid.id
            elif child.tag == 'UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_TINH_ID'] = rid.id
            elif child.tag == 'UnitPrice':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'CurrencyID':
                res['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1).id

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # danh mục vật tư hàng hóa chi tiết (định mức nvl)
    def _import_InventoryItemDetailNorm(self, tag):
        rec_model = 'danh.muc.vat.tu.hang.hoa.chi.tiet.dinh.muc.nvl'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'InventoryItemDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_ID'] = rid.id
            elif child.tag =='MaterialID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_NGUYEN_VAT_LIEU_ID'] = rid.id
            elif child.tag =='UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'MaterialName':
                res['TEN_NGUYEN_VAT_LIEU'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # danh mục vật tư hàng hóa chi tiết(chiết khấu)
    def _import_InventoryItemDetailDiscount(self, tag):
        rec_model = 'danh.muc.vat.tu.hang.hoa.chiet.khau'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'InventoryItemDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['VAT_TU_HANG_HOA_ID'] = rid.id
           
            elif child.tag == 'FromQuantity':
                res['SO_LUONG_TU'] = float(child.text)
            elif child.tag == 'ToQuantity':
                res['SO_LUONG_DEN'] = float(child.text)
            elif child.tag == 'DiscountRate':
                res['CHIET_KHAU'] = float(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # danh mục vật tư hàng hóa chi tiết(đơn vị chuyển đổi)
    def _import_InventoryItemUnitConvert(self, tag):
        rec_model = 'danh.muc.vat.tu.hang.hoa.don.vi.chuyen.doi'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'InventoryItemUnitConvertID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['VAT_TU_HANG_HOA_ID'] = rid.id
            elif child.tag == 'UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id
            elif child.tag == 'SortOrder':
                res['STT'] = int(child.text)
            elif child.tag == 'Description':
                res['MO_TA'] = child.text

            # elif child.tag == 'ExchangeRateOperator':
            #     res['PHEP_TINH_CHUYEN_DOI'] = helper.Obj.convert_to_key(child.text)
            elif child.tag == 'ConvertRate':
                res['TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH'] = float(child.text)
            elif child.tag == 'SalePrice1':
                res['DON_GIA_BAN_1'] = float(child.text)
            elif child.tag == 'SalePrice2':
                res['DON_GIA_BAN_2'] = float(child.text)
            elif child.tag == 'SalePrice3':
                res['DON_GIA_BAN_3'] = float(child.text)
            elif child.tag == 'FixedSalePrice':
                res['DON_GIA_CO_DINH'] = float(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)  

     # danh mục vật tư hàng hóa chi tiết(mã quy cách)
    def _import_InventoryItemDetailSerialType(self, tag):
        rec_model = 'danh.muc.vat.tu.hang.hoa.ma.quy.cach'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'InventoryItemDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['VAT_TU_HANG_HOA_ID'] = rid.id
           
            elif child.tag == 'SerialTypeName':
                res['MA_QUY_CACH'] = child.text
            elif child.tag == 'DisplayName':
                res['TEN_HIEN_THI'] = child.text
            elif child.tag =='Selected':
                res['CHON'] = False if child.text == 'false' else True
            elif child.tag =='AllowDuplicate':
                res['CHO_PHEP_TRUNG'] = False if child.text == 'false' else True
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # - Kho
    def _import_Stock(self, tag):
        rec_model = 'danh.muc.kho'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'StockID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'StockCode':
                res['MA_KHO'] = child.text
            elif child.tag == 'StockName':
                res['TEN_KHO'] = child.text
            elif child.tag == 'InventoryAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_KHO_ID'] =  rid.id
                
            elif child.tag == 'Description':
                res['DIA_CHI'] = child.text
            elif child.tag =='Inactive':
                res['active'] = False if child.text == 'true' else True
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # - Nhóm vật tư, hàng hóa, dịch vụ
    def _import_InventoryItemCategory(self, tag):
        rec_model = 'danh.muc.nhom.vat.tu.hang.hoa.dich.vu'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'InventoryCategoryID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'InventoryCategoryCode':
                res['MA'] = child.text
            elif child.tag == 'InventoryCategoryName':
                res['TEN'] = child.text
            elif child.tag == 'ParentID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['parent_id'] =  rid.id
            elif child.tag == 'MISACodeID':
                res['MA_PHAN_CAP'] = child.text
            elif child.tag =='Inactive':
                res['active'] = False if child.text == 'true' else True
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # - Đơn vị tính
    def _import_Unit(self, tag):
        rec_model = 'danh.muc.don.vi.tinh'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'UnitID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'UnitName':
                res['DON_VI_TINH'] = child.text
            elif child.tag == 'Description':
                res['MO_TA'] = child.text
            elif child.tag =='Inactive':
                res['active'] = False if child.text == 'true' else True
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    



     #Danh mục-Đối tượng tổng hợp chi 
    def _import_Job(self, tag):
        rec_model = 'danh.muc.doi.tuong.tap.hop.chi.phi'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'JobID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'JobCode':
                res['MA_DOI_TUONG_THCP'] = child.text
            elif child.tag == 'JobName':
                res['TEN_DOI_TUONG_THCP'] = child.text
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'JobType':
                res['LOAI'] = child.text
            elif child.tag == 'Stage':
                res['CONG_DOAN_THU'] = int(child.text)
            elif child.tag == 'ParentID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['parent_id'] = rid.id
            elif child.tag == 'MISACodeID':
                res['MA_PHAN_CAP'] = child.text
            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHON_THANH_PHAM'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #Danh mục-Đối tượng tổng hợp chi phí(chi tiết giá thành)
    def _import_JobProduct(self, tag):
        rec_model = 'danh.muc.chi.tiet.doi.tuong.tinh.gia.thanh'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'JobProductID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_TONG_HOP_CHI_PHI_ID'] = rid.id
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id
            elif child.tag == 'Note':
                res['TEN_THANH_PHAM'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)



    #Danh mục-Khoản mục chi phi
    def _import_ExpenseItem(self, tag):
        rec_model = 'danh.muc.khoan.muc.cp'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ExpenseItemID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'ExpenseItemCode':
                res['MA_KHOAN_MUC_CP'] = child.text
            elif child.tag == 'ExpenseItemName':
                res['TEN_KHOAN_MUC_CP'] = child.text
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            
            elif child.tag == 'ParentID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['parent_id'] = rid.id
            elif child.tag == 'MISACodeID':
                res['MA_PHAN_CAP'] = child.text

            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #Danh mục-Loại công trình
    def _import_ProjectWorkCategory(self, tag):
        rec_model = 'danh.muc.loai.cong.trinh'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ProjectWorkCategoryID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'ProjectWorkCategoryCode':
                res['MA_LOAI_CONG_TRINH'] = child.text
            elif child.tag == 'ProjectWorkCategoryName':
                res['name'] = child.text
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #Danh mục-công trình
    def _import_ProjectWork(self, tag):
        rec_model = 'danh.muc.cong.trinh'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ProjectWorkID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'ProjectWorkType':
                res['CONG_TRINH_SELECTION'] = child.text
            elif child.tag == 'ProjectWorkCode':
                res['MA_CONG_TRINH'] = child.text
            elif child.tag == 'ProjectWorkName':
                res['TEN_CONG_TRINH'] = child.text
            elif child.tag == 'ProjectWorkCategoryName':
                res['LOAI_CONG_TRINH'] = self.env['danh.muc.loai.cong.trinh'].search([('name', '=', child.text)], limit=1).id
            # elif child.tag == 'ProjectWorkStatusName':
            #     res['TINH_TRANG'] = child.text
            elif child.tag == 'StartDate':
                res['NGAY_BAT_DAU'] = child.text
            elif child.tag == 'FinishDate':
                res['NGAY_KET_THUC'] = child.text

            elif child.tag == 'EstimateAmount':
                res['DU_TOAN'] = float(child.text)
            elif child.tag == 'Stakeholder':
                res['CHU_DAU_TU'] = child.text
            elif child.tag == 'StakeholderAddress':
                res['DIA_CHI'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
                
            
            elif child.tag == 'ParentID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['parent_id'] = rid.id
            elif child.tag == 'MISACodeID':
                res['MA_PHAN_CAP'] = child.text
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text

            elif child.tag == 'Inactive':
            
                res['active'] = False if child.text == 'true' else True
            elif child.tag == 'ProjectWorkStatus':
                if child.text=='0':
                    res['TINH_TRANG'] = 'DANG_THUC_HIEN'
                elif child.text=='1':
                    res['TINH_TRANG'] = 'DA_HOAN_THANH'
            elif child.tag == 'IsParent':
            
                res['isparent'] = True if child.text == 'true' else False
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    


    #Danh mục-Ngân hàng
    def _import_Bank(self, tag):
        rec_model = 'danh.muc.ngan.hang'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'BankID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'BankCode':
                res['TEN_VIET_TAT'] = child.text
            elif child.tag == 'BankName':
                res['TEN_DAY_DU'] = child.text
            elif child.tag == 'BankNameEnglish':
                res['TEN_TIENG_ANH'] = child.text
            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
            elif child.tag == 'Address':
                res['DIA_CHI_HOI_SO_CHINH'] = child.text
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'Icon':
                res['image'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    
    # # #Danh mục- Tài khoản Ngân hàng
    def _import_BankAccount(self, tag):
        rec_model = 'danh.muc.tai.khoan.ngan.hang'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'BankAccountID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'BankAccountNumber':
                res['SO_TAI_KHOAN'] = child.text
            elif child.tag == 'BankID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NGAN_HANG_ID'] = rid.id
                
            elif child.tag == 'BankName':
                res['CHI_NHANH'] = child.text
            elif child.tag == 'Address':
                res['DIA_CHI_CN'] = child.text
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'ProvinceOrCity':
                res['TINH_TP'] = child.text
            elif child.tag == 'AccountHolder':
                res['CHU_TAI_KHOAN'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_2'] = rid.id
            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #Danh mục-Điều khoản thanh toán
    def _import_PaymentTerm(self, tag):
        rec_model = 'danh.muc.dieu.khoan.thanh.toan'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'PaymentTermID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'PaymentTermCode':
                res['MA_DIEU_KHOAN'] = child.text
            elif child.tag == 'PaymentTermName':
                res['TEN_DIEU_KHOAN'] = child.text
            elif child.tag == 'DueTime':
                res['SO_NGAY_DUOC_NO'] = int(child.text)
            elif child.tag == 'DiscountTime':
                res['THOI_HAN_HUONG_CHIET_KHAU'] = int(child.text)
            elif child.tag == 'DiscountPercent':
                res['TY_LE_CHIET_KHAU'] = float(child.text)
            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #Danh mục-Mã thống kê
    def _import_ListItem(self, tag):
        rec_model = 'danh.muc.ma.thong.ke'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ListItemID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'ListItemCode':
                res['MA_THONG_KE'] = child.text
            elif child.tag == 'ListItemName':
                res['TEN_THONG_KE'] = child.text
            elif child.tag == 'ParentID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['parent_id'] = rid.id
            elif child.tag == 'MISACodeID':
                res['MA_PHAN_CAP'] = child.text
            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    #Danh mục-Biểu thuế tiêu thụ đặc biệt
    def _import_InventoryItemCategorySpecialTax(self, tag):
        rec_model = 'danh.muc.bieu.thue.tieu.thu.dac.biet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'InventoryCategorySpecialTaxID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'InventoryCategorySpecialTaxCode':
                res['MA'] = child.text
            elif child.tag == 'InventoryCategorySpecialTaxName':
                res['TEN'] = child.text
            elif child.tag == 'TaxRate':
                res['THUE_SUAT'] = float(child.text)
            elif child.tag == 'Unit':
                res['DVT'] = child.text
            elif child.tag == 'ParentID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['THUOC'] = rid.id
            
            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    
    #Danh mục-Biểu thuế tài nguyên
    def _import_ResourcesTaxTable(self, tag):
        rec_model = 'danh.muc.bieu.thue.tai.nguyen'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ResourcesTaxTableID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'ResourcesTaxTableCode':
                res['MA'] = child.text
            elif child.tag == 'ResourcesTaxTableName':
                res['TEN'] = child.text
            elif child.tag == 'TaxRate':
                res['THUE_SUAT_PHAN_TRAM'] = float(child.text)
            elif child.tag == 'Unit':
                res['DON_VI'] = child.text
            elif child.tag == 'ParentID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['parent_id'] = rid.id
            elif child.tag == 'MISACodeID':
                res['MA_PHAN_CAP'] = child.text

            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #Danh mục-Loại chứng từ
    def _import_VoucherType(self, tag):
        rec_model = 'danh.muc.loai.chung.tu'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'VoucherTypeID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'


            elif child.tag == 'MovementBy':
                if child.text=='0':
                    res['PHAT_SINH_SELECTION'] = 'PHAT_SINH_THEO_TAI_KHOAN'
                elif child.text=='1':
                    res['PHAT_SINH_SELECTION'] = 'PHAT_SINH_THEO_NHOM_CHUNG_TU'


            elif child.tag == 'VoucherTypeCode':
                res['MA_LOAI'] = child.text
            elif child.tag == 'VoucherTypeName':
                res['TEN_LOAI'] = child.text
            elif child.tag == 'DebitAccount': 
                res['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag == 'CreditAccount':
                res['TK_CO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            
            elif child.tag == 'VoucherTypeCategory':
                res['NHOM_LOAI_CHUNG_TU_ID'] = [(6,0,self.env['danh.muc.nhom.loai.chung.tu'].search([('MA_NHOM_CHUNG_TU', 'in', child.text.split('; '))]).ids)] 
            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)



    # Danh mục tài khoản
    # Hệ thống tài khoản
    def _import_Account(self, tag):
        rec_model = 'danh.muc.he.thong.tai.khoan'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'AccountID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountNumber':
                res['SO_TAI_KHOAN'] = child.text
            elif child.tag == 'AccountName':
                res['TEN_TAI_KHOAN'] = child.text
            elif child.tag == 'AccountNameEnglish':
                res['TEN_TIENG_ANH'] = child.text
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'ParentID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['parent_id'] = rid.id
            elif child.tag == 'MISACodeID':
                res['MA_PHAN_CAP'] = child.text
            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
            elif child.tag == 'IsPostableInForeignCurrency':
                res['CO_HACH_TOAN_NGOAI_TE'] = True if child.text == 'true' else False
            elif child.tag == 'AccountCategoryKind':
                res['TINH_CHAT'] = child.text
            elif child.tag == 'DetailByBankAccount':
                res['TAI_KHOAN_NGAN_HANG'] = True if child.text == 'true' else False
            elif child.tag == 'DetailByJob':
                res['DOI_TUONG_THCP'] = True if child.text == 'true' else False
            elif child.tag == 'DetailByProjectWork':
                res['CONG_TRINH'] = True if child.text == 'true' else False
            elif child.tag == 'DetailByOrder':
                res['DON_DAT_HANG'] = True if child.text == 'true' else False
            elif child.tag == 'DetailByContract':
                res['HOP_DONG_BAN'] = True if child.text == 'true' else False
            elif child.tag == 'DetailByPUContract':
                res['HOP_DONG_MUA'] = True if child.text == 'true' else False
            elif child.tag == 'DetailByExpenseItem':
                res['KHOAN_MUC_CP'] = True if child.text == 'true' else False
            elif child.tag == 'DetailByDepartment':
                res['DON_VI'] = True if child.text == 'true' else False
            elif child.tag == 'DetailByListItem':
                res['MA_THONG_KE'] = True if child.text == 'true' else False
            elif child.tag == 'AccountObjectType':
                res['DOI_TUONG_SELECTION'] = child.text
            elif child.tag == 'DetailByJobKind':
                res['DOI_TUONG_THCP_SELECTION'] = child.text
            elif child.tag == 'DetailByProjectWorkKind':
                res['CONG_TRINH_SELECTION'] = child.text
            elif child.tag == 'DetailByOrderKind':
                res['DON_DAT_HANG_SELECTION'] = child.text
            elif child.tag == 'DetailByContractKind':
                res['HOP_DONG_BAN_SELECTION'] = child.text
            elif child.tag == 'DetailByPUContractKind':
                res['HOP_DONG_MUA_SELECTION'] = child.text
            elif child.tag == 'DetailByExpenseItemKind':
                res['KHOAN_MUC_CP_SELECTION'] = child.text
            elif child.tag == 'DetailByDepartmentKind':
                res['DON_VI_SELECTION'] = child.text
            elif child.tag == 'DetailByListItemKind':
                res['MA_THONG_KE_SELECTION'] = child.text
            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
            elif child.tag == 'Grade':
                res['BAC'] = child.text
            elif child.tag == 'DetailByAccountObject':
                res['DOI_TUONG'] = True if child.text == 'true' else False
        if res['DOI_TUONG'] == False:
            res['DOI_TUONG_SELECTION'] = None
        elif res['DOI_TUONG_THCP'] == False:
            res['DOI_TUONG_THCP_SELECTION'] = None
        elif res['CONG_TRINH'] == False:
            res['CONG_TRINH_SELECTION'] = None
        elif res['DON_DAT_HANG'] == False:
            res['DON_DAT_HANG_SELECTION'] = None
        elif res['HOP_DONG_BAN'] == False:
            res['HOP_DONG_BAN_SELECTION'] = None
        elif res['HOP_DONG_MUA'] == False:
            res['HOP_DONG_MUA_SELECTION'] = None
        elif res['KHOAN_MUC_CP'] == False:
            res['KHOAN_MUC_CP_SELECTION'] = None
        elif res['DON_VI'] == False:
            res['DON_VI_SELECTION'] = None
        elif res['MA_THONG_KE'] == False:
            res['MA_THONG_KE_SELECTION'] = None
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)   

    #Danh mục-tài khoản ngầm định detail
    def _import_AccountDefault(self, tag):
        rec_model = 'danh.muc.tai.khoan.ngam.dinh.chi.tiet' 
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'AccountDefaultID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'ColumnCaption':
                res['TEN_COT'] = child.text
            elif child.tag == 'ColumnName':
                res['TEN_COT_CHUYEN_DOI'] = DICT_ACCOUNT.get(child.text)
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
            elif child.tag == 'VoucherType':
                res['NHOM_CHUNG_TU'] = int(child.text)
            elif child.tag == 'FilterCondition': 
                if child.text:
                    res['LOC_TAI_KHOAN'] = [(6,0,self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', 'in', tuple(child.text.split('; ')))]).ids)] 
            elif child.tag == 'DefaultValue': 
                res['TK_NGAM_DINH_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text.strip())], limit=1).id
            elif child.tag == 'RefTypeName': 
                res['name'] = child.text
        # Tìm kiếm bản ghi master
        tk_nd = self.env['danh.muc.tai.khoan.ngam.dinh'].search([('LOAI_CHUNG_TU', '=', res['LOAI_CHUNG_TU'])], limit=1)
        if not tk_nd:
            tk_nd = self.env['danh.muc.tai.khoan.ngam.dinh'].create({
                'LOAI_CHUNG_TU':  res.get('LOAI_CHUNG_TU'),
                'name': res.get('name')
            })
        res['DANH_MUC_TAI_KHOAN_NGAM_DINH_ID'] = tk_nd.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #Danh mục-dinh khoản tự động
    def _import_AutoBusiness(self, tag):
        rec_model = 'danh.muc.dinh.khoan.tu.dong'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'AutoBusinessID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'VoucherType':
                res['LOAI_CHUNG_TU'] = child.text
            elif child.tag == 'AutoBusinessName':
                res['TEN_DINH_KHOAN'] = child.text
            elif child.tag == 'DebitAccount': 
                res['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag == 'CreditAccount': 
                res['TK_CO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            
        
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)



    #Danh mục-tài khoản kết chuyển
    def _import_AccountTransfer(self, tag):
        rec_model = 'danh.muc.tai.khoan.ket.chuyen'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'AccountTransferID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountTransferCode':
                res['MA_KET_CHUYEN'] = child.text
            elif child.tag == 'TransferOrder':
                res['THU_TU_KET_CHUYEN'] = int(child.text)
            elif child.tag == 'FromAccount': 
                res['KET_CHUYEN_TU_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag == 'ToAccount': 
                res['KET_CHUYEN_DEN_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag == 'TransferSideName':
                res['BEN_KET_CHUYEN'] = helper.Obj.convert_to_key(child.text)
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'SetupTypeName':
                res['LOAI_KET_CHUYEN'] = helper.Obj.convert_to_key(child.text)
            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
            
        
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    #Danh mục-Nhóm khách hàng,nhà cung cấp
    def _import_AccountObjectGroup(self, tag):
        rec_model = 'danh.muc.nhom.khach.hang.nha.cung.cap'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'AccountObjectGroupID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountObjectGroupCode':
                res['MA'] = child.text
            elif child.tag == 'AccountObjectGroupName':
                res['TEN'] = child.text
            elif child.tag == 'ParentID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['parent_id'] = rid.id
            elif child.tag == 'MISACodeID':
                res['MA_PHAN_CAP'] = child.text
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #Danh mục-Loại tiền
    def _import_CCY(self, tag):
        rec_model = 'res.currency'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'AfterDecimalENG':
                res['DOC_SO_TIEN_SAU_THAP_PHAN_TIENG_ANH'] = child.text
            elif child.tag == 'CurrencyID':
                res['MA_LOAI_TIEN'] = child.text
                res['name'] = child.text
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'CurrencyName':
                res['TEN_LOAI_TIEN'] = child.text
            elif child.tag == 'ExchangeRate': 
                res['TY_GIA_QUY_DOI'] = float(child.text)
            elif child.tag == 'CAAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_TIEN_MAT_ID'] = rid.id
            elif child.tag == 'BAAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_TIEN_GUI_ID'] = rid.id     
            elif child.tag == 'CCYName':
                res['DOC_TEN_LOAI_TIEN'] = child.text
            elif child.tag == 'DecimalSeperate':
                res['DOC_PHAN_CACH_THAP_PHAN'] = child.text
            elif child.tag == 'ConvertRate':
                res['TY_LE_CHUYEN_DOI'] = float(child.text)
            elif child.tag == 'CCYNameENG': 
                res['DOC_TEN_LOAI_TIEN_TIENG_ANH'] = child.text
            elif child.tag == 'DecimalSeperateENG':
                res['DOC_PHAN_CACH_THAP_PHAN_TIENG_ANH'] = child.text 
            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
            elif child.tag == 'Prefix': 
                res['KY_HIEU_BAT_DAU'] = child.text
            elif child.tag == 'PrefixENG':
                res['KY_HIEU_BAT_DAU_TIENG_ANH'] = child.text
            elif child.tag == 'AfterDecimal': 
                res['DOC_SO_TIEN_SAU_THAP_PHAN'] = child.text
            elif child.tag == 'Subfix':
                res['KY_HIEU_KET_THUC'] = child.text
            elif child.tag == 'SubfixENG': 
                res['KY_HIEU_KET_THUC_TIENG_ANH'] = child.text
            elif child.tag == 'ConvertRateENG':
                res['TY_LE_CHUYEN_DOI_TIENG_ANH'] = float(child.text)
            # import giá trị mặc định
            elif child.tag == 'PrefixDefault':
                res['KY_HIEU_BAT_DAU_MAC_DINH'] = child.text
            elif child.tag == 'CCYNameDefault':
                res['DOC_TEN_LOAI_TIEN_MAC_DINH'] = child.text
            elif child.tag == 'DecimalSeperateDefault':
                res['DOC_PHAN_CACH_THAP_PHAN_MAC_DINH'] = child.text
            elif child.tag == 'AfterDecimalDefault':
                res['DOC_SO_TIEN_SAU_THAP_PHAN_MAC_DINH'] = child.text
            elif child.tag == 'ConvertRateDefault':
                res['TY_LE_CHUYEN_DOI_MAC_DINH'] = float(child.text)
            elif child.tag == 'SubfixDefault':
                res['KY_HIEU_KET_THUC_MAC_DINH'] = child.text

            elif child.tag == 'PrefixDefaultENG':
                res['KY_HIEU_BAT_DAU_TIENG_ANH_MAC_DINH'] = child.text
            elif child.tag == 'CCYNameDefaultENG':
                res['DOC_TEN_LOAI_TIEN_TIENG_ANH_MAC_DINH'] = child.text
            elif child.tag == 'DecimalSeperateDefaultENG':
                res['DOC_PHAN_CACH_THAP_PHAN_TIENG_ANH_MAC_DINH'] = child.text
            elif child.tag == 'AfterDecimalDefaultENG':
                res['DOC_SO_TIEN_SAU_THAP_PHAN_TIENG_ANH_MAC_DINH'] = child.text
            elif child.tag == 'ConvertRateDefaultENG':
                res['TY_LE_CHUYEN_DOI_TIENG_ANH_MAC_DINH'] = float(child.text)
            elif child.tag == 'SubfixDefaultENG':
                res['KY_HIEU_KET_THUC_TIENG_ANH_MAC_DINH'] = child.text
            
            # elif child.tag == 'UnitAmount': 
            #     res['KY_HIEU_KET_THUC_TIENG_ANH'] = child.text
            elif child.tag == 'ExampleAmount':
                res['NHAP_SO_TIEN'] = float(child.text)

        return self.env['ir.model.data']._update(rec_model, 'base', res, rec_id, noupdate=0, mode='update', return_id=False)

    #  danh mục ký hiệu chấm công lương nhân viên
    def _import_TimeSheetSign(self, tag):
        rec_model = 'danh.muc.ky.hieu.cham.cong.tien.luong'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'TimeSheetSignID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'TimeSheetSignCode':
                res['KY_HIEU'] = child.text
            elif child.tag == 'TimeSheetSignName':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'SalaryRate':
                res['TY_LE_HUONG_LUONG'] = float(child.text)
            elif child.tag == 'Inactive':
                res['active'] = False if child.text == 'true' else True
            elif child.tag == 'IsDefault':
                res['LA_KY_HIEU_MAC_DINH'] = True if child.text == 'true' else False
            elif child.tag == 'IsHalfDay':
                res['LA_KY_HIEU_NUA_NGAY'] = True if child.text == 'true' else False
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #  danh mục biểu tính thuế thu nhập
    def _import_PersonalIncomeTaxRate(self, tag):
        rec_model = 'danh.muc.bieu.tinh.thue.thu.nhap.tien.luong'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'PersonalIncomeTaxRateID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'TaxGrade':
                res['BAC'] = int(child.text)
            elif child.tag == 'FromIncomeByMonth':
                res['PHAN_THU_NHAP_TU'] = float(child.text)
            elif child.tag == 'ToIncomeByMonth':
                res['PHAN_THU_NHAP_DEN'] = float(child.text)
            elif child.tag == 'FromIncomeByYear':
                res['THUE_THEO_NAM_TU'] = float(child.text)
            elif child.tag == 'ToIncomeByYear':
                res['THUE_THEO_NAM_DEN'] = float(child.text)
            elif child.tag == 'TaxRate':
                res['THUE_SUAT'] = float(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #Danh mục-Mẫu số HĐ
    def _import_InvoiceTypeAutoID(self, tag):
        rec_model = 'danh.muc.mau.so.hd'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'InvTemplateNo':
                rec_id = child.text
                res['MAU_SO_HD'] = child.text
                res['TEN_MAU_SO_HD'] = child.text
            if child.tag == 'InvTemplateName':
                res['TEN_MAU_SO_HD'] = child.text
            res['active'] = True
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #Danh mục Tỉnh/TP
    def _import_ResCountryState(self, tag):
        rec_model = 'res.country.state'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'id':
                rec_id = child.text
            elif child.tag == 'name':
                res['name'] = child.text
            elif child.tag == 'cap_to_chuc':
                res['CAP'] = child.text
            elif child.tag == 'code':
                res['code'] = child.text
            elif child.tag == 'country_id':
                res['country_id'] = self.env['res.country'].search([('code','=',child.text)],limit=1).id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    
    def _import_ResCountryStateDistrict(self, tag):
        rec_model = 'res.country.state.district'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'id':
                rec_id = child.text
            elif child.tag == 'name':
                res['name'] = child.text
            elif child.tag == 'cap_to_chuc':
                res['CAP'] = child.text
            elif child.tag == 'code':
                res['code'] = child.text
            elif child.tag == 'state_id':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['state_id'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    
    def _import_ResCountryStateDistrictWard(self, tag):
        rec_model = 'res.country.state.district.ward'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'id':
                rec_id = child.text
            elif child.tag == 'name':
                res['name'] = child.text
            elif child.tag == 'cap_to_chuc':
                res['CAP'] = child.text
            elif child.tag == 'code':
                res['code'] = child.text
            elif child.tag == 'district_id':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['district_id'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    ##########################################################################
    #############################END IMPORTIMG################################
    ##########################################################################
    def importFromMS(self, tag):
        method = getattr(self, '_import_' + str(tag.tag), lambda tag: None)
        return method(tag)

    @api.multi
    def parse_preview(self, options, count=10):
        self.ensure_one()
        # import_ids = self.env['base_import_ex.import'].search([('parent_id','=',self.id)])
        result = []
        result.append({
                    'matches': False,
                    'headers': False,
                    'headers_type': False,
                })
        # for import_id in import_ids:
        #     for tag in ElementTree.fromstring(import_id.file.replace(b'xmlns="http://tempuri.org/DataSetImportExport.xsd"',b'')):
        #         self.importFromMS(tag)
        return result

    @api.multi
    def parse_preview1(self, options, count=10):
        """ Generates a preview of the uploaded files, and performs
            fields-matching between the import's file data and the model's
            columns.

            If the headers are not requested (not options.headers),
            ``matches`` and ``headers`` are both ``False``.

            :param int count: number of preview lines to generate
            :param options: format-specific options.
                            CSV: {encoding, quoting, separator, headers}
            :type options: {str, str, str, bool}
            :returns: {fields, matches, headers, preview} | {error, preview}
            :rtype: {dict(str: dict(...)), dict(int, list(str)), list(str), list(list(str))} | {str, str}
        """
        self.ensure_one()
        import_ids = self.env['base_import_ex.import'].search([('parent_id','=',self.id)])
        result = []
        for import_id in import_ids:
            fields = import_id.get_fields(import_id.res_model)
            try:
                rows = import_id._read_file(options)
                headers, matches = import_id._match_headers(rows, fields, options)
                # Match should have consumed the first row (iif headers), get
                # the ``count`` next rows for preview
                preview = list(itertools.islice(rows, count))
                assert preview, "CSV file seems to have no content"
                header_types = import_id._find_type_from_preview(options, preview)
                if options.get('keep_matches', False) and len(options.get('fields', [])):
                    matches = {}
                    for index, match in enumerate(options.get('fields')):
                        if match:
                            matches[index] = match.split('/')

                result.append({
                    'fields': fields,
                    'matches': matches or False,
                    'headers': headers or False,
                    'headers_type': header_types or False,
                    'preview': preview,
                    'options': options,
                    'advanced_mode': any([len(models.fix_import_export_id_paths(col)) > 1 for col in headers or []]),
                    'debug': self.user_has_groups('base.group_no_one'),
                    'res_model': import_id.res_model,
                })
            except Exception as error:
                # Due to lazy generators, UnicodeDecodeError (for
                # instance) may only be raised when serializing the
                # preview to a list in the return.
                _logger.debug("Error during parsing preview", exc_info=True)
                preview = None
                if self.file_type == 'text/csv':
                    preview = self.file[:ERROR_PREVIEW_BYTES].decode('iso-8859-1')
                return {
                    'error': str(error),
                    # iso-8859-1 ensures decoding will always succeed,
                    # even if it yields non-printable characters. This is
                    # in case of UnicodeDecodeError (or csv.Error
                    # compounded with UnicodeDecodeError)
                    'preview': preview,
                }
        return result

    @api.model
    def _convert_import_data(self, fields, options):
        """ Extracts the input BaseModel and fields list (with
            ``False``-y placeholders for fields to *not* import) into a
            format Model.import_data can use: a fields list without holes
            and the precisely matching data matrix

            :param list(str|bool): fields
            :returns: (data, fields)
            :rtype: (list(list(str)), list(str))
            :raises ValueError: in case the import data could not be converted
        """
        # Get indices for non-empty fields
        indices = [index for index, field in enumerate(fields) if field]
        if not indices:
            raise ValueError(_("You must configure at least one field to import"))
        # If only one index, itemgetter will return an atom rather
        # than a 1-tuple
        if len(indices) == 1:
            mapper = lambda row: [row[indices[0]]]
        else:
            mapper = operator.itemgetter(*indices)
        # Get only list of actually imported fields
        import_fields = [f for f in fields if f]

        rows_to_import = self._read_file(options)
        if options.get('headers'):
            rows_to_import = itertools.islice(rows_to_import, 1, None)
        data = [
            list(row) for row in pycompat.imap(mapper, rows_to_import)
            # don't try inserting completely empty rows (e.g. from
            # filtering out o2m fields)
            if any(row)
        ]

        return data, import_fields

    @api.model
    def _remove_currency_symbol(self, value):
        value = value.strip()
        negative = False
        # Careful that some countries use () for negative so replace it by - sign
        if value.startswith('(') and value.endswith(')'):
            value = value[1:-1]
            negative = True
        float_regex = re.compile(r'([-]?[0-9.,]+)')
        split_value = [g for g in float_regex.split(value) if g]
        if len(split_value) > 2:
            # This is probably not a float
            return False
        if len(split_value) == 1:
            if float_regex.search(split_value[0]) is not None:
                return split_value[0] if not negative else '-' + split_value[0]
            return False
        else:
            # String has been split in 2, locate which index contains the float and which does not
            currency_index = 0
            if float_regex.search(split_value[0]) is not None:
                currency_index = 1
            # Check that currency exists
            currency = self.env['res.currency'].search([('symbol', '=', split_value[currency_index].strip())])
            if len(currency):
                return split_value[(currency_index + 1) % 2] if not negative else '-' + split_value[(currency_index + 1) % 2]
            # Otherwise it is not a float with a currency symbol
            return False

    @api.model
    def _parse_float_from_data(self, data, index, name, options):
        thousand_separator = options.get('float_thousand_separator', ' ')
        decimal_separator = options.get('float_decimal_separator', '.')
        for line in data:
            line[index] = line[index].strip()
            if not line[index]:
                continue
            line[index] = line[index].replace(thousand_separator, '').replace(decimal_separator, '.')
            old_value = line[index]
            line[index] = self._remove_currency_symbol(line[index])
            if line[index] is False:
                raise ValueError(_("Column %s contains incorrect values (value: %s)" % (name, old_value)))

    @api.multi
    def _parse_import_data(self, data, import_fields, options):
        """ Lauch first call to _parse_import_data_recursive with an
        empty prefix. _parse_import_data_recursive will be run
        recursively for each relational field.
        """
        return self._parse_import_data_recursive(self.res_model, '', data, import_fields, options)

    @api.multi
    def _parse_import_data_recursive(self, model, prefix, data, import_fields, options):
        # Get fields of type date/datetime
        all_fields = self.env[model].fields_get()
        for name, field in all_fields.items():
            name = prefix + name
            if field['type'] in ('date', 'datetime') and name in import_fields:
                # Parse date
                index = import_fields.index(name)
                dt = datetime.datetime
                server_format = DEFAULT_SERVER_DATE_FORMAT if field['type'] == 'date' else DEFAULT_SERVER_DATETIME_FORMAT

                if options.get('%s_format' % field['type'], server_format) != server_format:
                    # datetime.str[fp]time takes *native strings* in both
                    # versions, for both data and pattern
                    user_format = pycompat.to_native(options.get('%s_format' % field['type']))
                    for num, line in enumerate(data):
                        if line[index]:
                            line[index] = line[index].strip()
                        if line[index]:
                            try:
                                line[index] = dt.strftime(dt.strptime(pycompat.to_native(line[index]), user_format), server_format)
                            except ValueError as e:
                                raise ValueError(_("Column %s contains incorrect values. Error in line %d: %s") % (name, num + 1, e))
                            except Exception as e:
                                raise ValueError(_("Error Parsing Date [%s:L%d]: %s") % (name, num + 1, e))
            # Check if the field is in import_field and is a relational (followed by /)
            # Also verify that the field name exactly match the import_field at the correct level.
            elif any(name + '/' in import_field and name == import_field.split('/')[prefix.count('/')] for import_field in import_fields):
                # Recursive call with the relational as new model and add the field name to the prefix
                self._parse_import_data_recursive(field['relation'], name + '/', data, import_fields, options)
            elif field['type'] in ('float', 'monetary') and name in import_fields:
                # Parse float, sometimes float values from file have currency symbol or () to denote a negative value
                # We should be able to manage both case
                index = import_fields.index(name)
                self._parse_float_from_data(data, index, name, options)
        return data

    # Thực hiện 1 hàm do duy nhất để import, không thể revert
    @api.multi
    def do(self, fields, options, dryrun=False):
        self.ensure_one()
        self._cr.execute('SAVEPOINT import')
        import_ids = self.env['base_import_ex.import'].search([('parent_id','=',self.id)])
        record_ids = []
        for import_id in import_ids:
            for tag in ElementTree.fromstring(import_id.file.replace(b'xmlns="http://tempuri.org/DataSetImportExport.xsd"',b'')):
                record = self.with_context(import_file=True, fromMS=True).importFromMS(tag)
                if record:# and record != 'nothing':
                    record_ids += [record]
        
        # Post-processing
        for rec in record_ids:
            # Ghi sổ
            if hasattr(rec, 'state'):
                if rec.state == 'da_ghi_so':
                    rec.bo_ghi_so()
                    rec.action_ghi_so()                    
                elif rec.state == 'chua_ghi_so':
                    rec.bo_ghi_so()
        # Update MA_CHI_TIEU_ID cho công thức trong báo cáo tài chính
        if self.env.get('tien.ich.xay.dung.cong.thuc.mac.dinh'):
            cong_thuc_BCTC = self.env['tien.ich.xay.dung.cong.thuc.mac.dinh'].search([('MA_CHI_TIEU', '!=', None),('MA_CHI_TIEU_ID', '=', None)])
            for ct in cong_thuc_BCTC:
                ma_chi_tieu = self.env['tien.ich.bao.cao.tai.chinh.chi.tiet.mac.dinh'].search([('MA_CHI_TIEU', '=', ct.MA_CHI_TIEU)], limit=1)
                if ma_chi_tieu:
                    ct.write({'MA_CHI_TIEU_ID': ma_chi_tieu.id})
        try:
            if dryrun:
                self._cr.execute('ROLLBACK TO SAVEPOINT import')
            else:
                self._cr.execute('RELEASE SAVEPOINT import')
        except psycopg2.InternalError:
            pass
        return 'Success!!!'

    @api.multi
    def do1(self, fields, options, dryrun=False):
        """ Actual execution of the import

        :param fields: import mapping: maps each column to a field,
                       ``False`` for the columns to ignore
        :type fields: list(str|bool)
        :param dict options:
        :param bool dryrun: performs all import operations (and
                            validations) but rollbacks writes, allows
                            getting as much errors as possible without
                            the risk of clobbering the database.
        :returns: A list of errors. If the list is empty the import
                  executed fully and correctly. If the list is
                  non-empty it contains dicts with 3 keys ``type`` the
                  type of error (``error|warning``); ``message`` the
                  error message associated with the error (a string)
                  and ``record`` the data which failed to import (or
                  ``false`` if that data isn't available or provided)
        :rtype: list({type, message, record})
        """
        self.ensure_one()
        self._cr.execute('SAVEPOINT import')
        import_ids = self.env['base_import_ex.import'].search([('parent_id','=',self.id)])
        for import_id in import_ids:
            field_names = [x['val'] for x in fields if x['res_model'] == import_id.res_model]
            try:
                data, import_fields = import_id._convert_import_data(field_names, options)
                # Parse date and float field
                data = import_id._parse_import_data(data, import_fields, options)
            except ValueError as error:
                return [{
                    'type': 'error',
                    'message': pycompat.text_type(error),
                    'record': False,
                }]

            _logger.info('importing %d rows...', len(data))

            model = self.env[import_id.res_model].with_context(import_file=True)
            defer_parent_store = import_id.env.context.get('defer_parent_store_computation', True)
            if defer_parent_store and model._parent_store:
                model = model.with_context(defer_parent_store_computation=True)
            
            import_result = model.load(import_fields, data)
            _logger.info('done')

        # If transaction aborted, RELEASE SAVEPOINT is going to raise
        # an InternalError (ROLLBACK should work, maybe). Ignore that.
        # TODO: to handle multiple errors, create savepoint around
        #       write and release it in case of write error (after
        #       adding error to errors array) => can keep on trying to
        #       import stuff, and rollback at the end if there is any
        #       error in the results.
        try:
            if dryrun:
                self._cr.execute('ROLLBACK TO SAVEPOINT import')
            else:
                self._cr.execute('RELEASE SAVEPOINT import')
        except psycopg2.InternalError:
            pass

        return import_result['messages']

    def auto_import(self, filename):
        try:
            xlsx_file_path = get_module_resource('base_import_ex', 'static\\csv', filename)
            file_content = open(xlsx_file_path, 'rb').read()
            import_wizard = self.env['base_import_ex.import'].create({
                'file': file_content,
            })
            for tag in ElementTree.fromstring(import_wizard.file.replace(b'xmlns="http://tempuri.org/DataSetImportExport.xsd"',b'')):
                self.with_context(import_file=True, fromMS=True).importFromMS(tag)
            _logger.info('[Cloudify] - Auto import %s successful!!!', filename)
        except ValueError as error:
            _logger.info('[Cloudify] - Auto import %s fail!!!', filename)
            pass
            