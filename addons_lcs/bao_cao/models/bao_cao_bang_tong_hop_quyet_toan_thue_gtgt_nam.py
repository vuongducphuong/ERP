# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_BANG_TONG_HOP_QUYET_TOAN_THUE_GTGT_NAM(models.Model):
    _name = 'bao.cao.bang.tong.hop.quyet.toan.thue.gtgt.nam'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh', required=True)
    NAM = fields.Integer(string='Năm', help='Năm')
    KY_TINH_THUE = fields.Char(string='Kỳ tính thuế', help='Kỳ tính thuế')
    SO_CON_DUOC_KHAU_TRU_KY_TRUOC_CHUYEN_SANG = fields.Float(string='Số còn được khấu trừ kỳ trước chuyển sang', help='Số còn được khấu trừ kỳ trước chuyển sang',digits=decimal_precision.get_precision('VND'))
    SO_THUE_DAU_RA = fields.Float(string='Số thuế đầu ra', help='Số thuế đầu ra',digits=decimal_precision.get_precision('VND'))
    SO_THUE_DAU_VAO = fields.Float(string='Số thuế đầu vào', help='Số thuế đầu vào',digits=decimal_precision.get_precision('VND'))
    SO_DUOC_KHAU_TRU_TRONG_KY = fields.Float(string='Số được khấu trừ trong kỳ', help='Số được khấu trừ trong kỳ',digits=decimal_precision.get_precision('VND'))
    SO_PHAI_NOP = fields.Float(string='Số phải nộp', help='Số phải nộp',digits=decimal_precision.get_precision('VND'))
    SO_THUE_DE_NGHI_HOAN = fields.Float(string='Số thuế đề nghị hoàn', help='Số thuế đề nghị hoàn',digits=decimal_precision.get_precision('VND'))
    SO_CON_DUOC_KHAU_TRU_CHUYEN_KY_SAU = fields.Float(string='Số còn được khấu trừ chuyển kỳ sau', help='Số còn được khấu trừ chuyển kỳ sau',digits=decimal_precision.get_precision('VND'))
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_BANG_TONG_HOP_QUYET_TOAN_THUE_GTGT_NAM, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        if chi_nhanh :
            result['CHI_NHANH_ID'] = chi_nhanh.id
        result['NAM'] = datetime.now().year
        return result


    selection_ky_tinh_thue = fields.Selection([
        ('thang', 'Tháng'),
        ('quy','Qúy'),
        ], default='thang',string=" ")

    def _validate(self):
        params = self._context
        NAM = params['NAM'] if 'NAM' in params.keys() else 'False'
        if( NAM < 1700 or NAM > 9999):
            raise ValidationError('<Năm> phải nằm trong khoảng 1700 - 9999.')

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() else 'False'
        NAM = params['NAM'] if 'NAM' in params.keys() else 'False'
        KY_TINH_THUE = params['KY_TINH_THUE'] if 'KY_TINH_THUE' in params.keys() else 'False'
        # Execute SQL query here
        cr = self.env.cr
        query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
        cr.execute(query)
        # Get and show result
        for line in cr.dictfetchall():
            record.append({
                'SO_CON_DUOC_KHAU_TRU_KY_TRUOC_CHUYEN_SANG': '',
                'SO_THUE_DAU_RA': '',
                'SO_THUE_DAU_VAO': '',
                'SO_DUOC_KHAU_TRU_TRONG_KY': '',
                'SO_PHAI_NOP': '',
                'SO_THUE_DE_NGHI_HOAN': '',
                'SO_CON_DUOC_KHAU_TRU_CHUYEN_KY_SAU': '',
                'name': '',
                })
        return record

    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        ky_tinh_thues = self._context.get('selection_ky_tinh_thue')
        nam = self._context.get('NAM')
        ky_tinh_thue = ''
        if ky_tinh_thues =='thang':
            ky_tinh_thue = 'Tháng'
        else:
            ky_tinh_thue = 'Quý'
        param = 'Năm: %s; Kỳ tính thuế: %s' % (nam, ky_tinh_thue)
        action = self.env.ref('bao_cao.open_report_bang_tong_hop_quyet_toan_thue_gtgt_nam').read()[0]
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action