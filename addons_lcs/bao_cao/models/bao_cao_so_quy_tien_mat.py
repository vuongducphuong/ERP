# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_SO_QUY_TIEN_MAT(models.Model):
    _name = 'bao.cao.so.quy.tien.mat'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh', required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TU_NGAY = fields.Date(string='Từ', help='Từ ngày',required=True,default=fields.Datetime.now)
    DEN_NGAY = fields.Date(string='Đến', help='Đến ngày',required=True,default=fields.Datetime.now)
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',required=True)
    NGAY_GHI_SO = fields.Date(string='Ngày ghi sổ ', help='Ngày ghi sổ ')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    THU_SO_HIEU_CHUNG_TU = fields.Float(string='Thu', help='Thu số hiệu chứng từ',digits=decimal_precision.get_precision('VND'))
    CHI_SO_HIEU_CHUNG_TU = fields.Float(string='Chi', help='Chi số hiệu chứng từ',digits=decimal_precision.get_precision('VND'))
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    THU_SO_TIEN = fields.Float(string='Thu', help='Thu số tiền',digits=decimal_precision.get_precision('VND'))
    CHI_SO_TIEN = fields.Float(string='Chi', help='Chi số tiền',digits=decimal_precision.get_precision('VND'))
    TON_SO_TIEN = fields.Float(string='Tồn', help='Tồn số tiền',digits=decimal_precision.get_precision('VND'))
    NGUOI_NHAN_NGUOI_NOP = fields.Char(string='Người nhận/ Người nộp', help='Người nhận hoặc người nộp')
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    GHICHU = fields.Char(string='Ghi chú', help='Ghi chú')

    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_SO_QUY_TIEN_MAT, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        loai_tien = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')],limit=1)
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        if loai_tien:
            result['currency_id'] = loai_tien.id
        return result

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU_NGAY', 'DEN_NGAY')

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        # Execute SQL query here
        cr = self.env.cr
        query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
        cr.execute(query)
        # Get and show result
        for line in cr.dictfetchall():
            record.append({
                'NGAY_GHI_SO': '',
                'NGAY_CHUNG_TU': '',
                'THU_SO_HIEU_CHUNG_TU': '',
                'CHI_SO_HIEU_CHUNG_TU': '',
                'DIEN_GIAI': '',
                'THU_SO_TIEN': '',
                'CHI_SO_TIEN': '',
                'TON_SO_TIEN': '',
                'NGUOI_NHAN_NGUOI_NOP': '',
                'LOAI_CHUNG_TU': '',
                })
        return record

    ### END IMPLEMENTING CODE ###
    def _validate(self):
        params = self._context
       
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
       

        if(TU_NGAY=='False'):
            raise ValidationError('<Từ> không được bỏ trống.')
        elif(DEN_NGAY=='False'):
            raise ValidationError('<Đến> không được bỏ trống.')
        elif(TU_NGAY_F > DEN_NGAY_F):
            raise ValidationError('<Đến> phải lớn hơn hoặc bằng <Từ>.')

    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU_NGAY')
        DEN_NGAY_F = self.get_vntime('DEN_NGAY')
        currency_id = self.get_context('currency_id')
        loai_tien = ''
        if currency_id:
            loai_tien = self.env['res.currency'].browse(currency_id).MA_LOAI_TIEN
        param = 'Loại tiền: %s; Từ ngày: %s đến ngày %s' % (loai_tien, TU_NGAY_F, DEN_NGAY_F)
        action = self.env.ref('bao_cao.open_report_so_quy_tien_mat').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action