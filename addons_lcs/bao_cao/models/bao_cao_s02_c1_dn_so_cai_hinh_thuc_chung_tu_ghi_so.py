# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_S02_C1_DN_SO_CAI_HINH_THUC_CHUNG_TU_GHI_SO(models.Model):
    _name = 'bao.cao.s02.c1.dn.so.cai.hinh.thuc.chung.tu.ghi.so'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('res.company', string='Chi nhánh', help='Chi nhánh')
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI', required='True')
    TU = fields.Date(string='Từ', help='Từ', default=fields.Datetime.now, required='True')
    DEN = fields.Date(string='Đến', help='Đến', default=fields.Datetime.now, required='True')
    NGAY_THANG_GHI_SO = fields.Date(string='Ngày tháng ghi sổ', help='Ngày tháng ghi sổ')
    SO_HIEU = fields.Float(string='Số hiệu', help='Số hiệu')
    NGAY_THANG = fields.Date(string='Ngày tháng', help='Ngày tháng')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    SO_HIEU_TK_DOI_UNG = fields.Float(string='Số hiệu tk đối ứng', help='Số hiệu tk đối ứng')
    NO = fields.Char(string='Nợ', help='Nợ')
    CO = fields.Char(string='Có', help='Có')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = fields.Boolean(string='Cộng gộp các bút toán giống nhau', help='Chi nhánh', default='True')

    
    TAI_KHOAN_IDS = fields.One2many('danh.muc.he.thong.tai.khoan')


    #FIELD_IDS = fields.One2many('model.name')

    ### START IMPLEMENTING CODE ###
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_S02_C1_DN_SO_CAI_HINH_THUC_CHUNG_TU_GHI_SO, self).default_get(fields_list)
        result['TAI_KHOAN_IDS'] = self.env['danh.muc.he.thong.tai.khoan'].search([]).ids
        result['CHI_NHANH_ID'] = self.env['res.company'].search([],limit=1).id
        return result
    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')

    def _validate(self):
        params = self._context
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        TU = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

        if(TU=='False'):
            raise ValidationError('<Từ> không được bỏ trống.')
        elif(DEN=='False'):
            raise ValidationError('<Đến> không được bỏ trống.')
        elif(TU > DEN):
            raise ValidationError('<Đến> phải lớn hơn hoặc bằng <Từ>.')
            
    def _validate(self):
        params = self._context
        TAI_KHOAN_IDS = params['TAI_KHOAN_IDS'] if 'TAI_KHOAN_IDS' in params.keys() else 'False'
        if TAI_KHOAN_IDS=='False':
            raise ValidationError('Bạn chưa chọn <tài khoản>. Xin vui lòng chọn lại.')


    # @api.onchange('field_name')
    # def _cap_nhat(self):
    #     for item in self:
    #         item.FIELDS_IDS = self.env['model_name'].search([])

    # def _validate(self):
    #     params = self._context
    #     FIELDS_IDS = params['FIELDS_IDS'] if 'FIELDS_IDS' in params.keys() else 'False'
    #     if(not len(FIELDS_IDS)):
    #         raise ValidationError('Noi dung thong bao!')

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() else 'False'
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() else 'False'
        KY_BAO_CAO = params['KY_BAO_CAO'] if 'KY_BAO_CAO' in params.keys() else 'False'
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = params['CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU'] if 'CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU' in params.keys() else 'False'
        # Execute SQL query here
        cr = self.env.cr
        query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
        cr.execute(query)
        # Get and show result
        for line in cr.dictfetchall():
            record.append({
                'NGAY_THANG_GHI_SO': '',
                'SO_HIEU': '',
                'NGAY_THANG': '',
                'DIEN_GIAI': '',
                'SO_HIEU_TK_DOI_UNG': '',
                'NO': '',
                'CO': '',
                'name': '',
                })
        return record

    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        TU = self.get_vntime('TU')
        DEN = self.get_vntime('DEN')
        TAI_KHOAN_ID = self.get_context('TAI_KHOAN_ID')
        param = 'Từ ngày: %s đến ngày %s' % (TU, DEN)
        action = self.env.ref('bao_cao.open_report__s02_c1_dn_so_cai_hinh_thuc_chung_tu_ghi_so').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action