# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_S03A1_DN_SO_NHAT_KY_THU_TIEN(models.Model):
    _name = 'bao.cao.s03a1.dn.so.nhat.ky.thu.tien'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo ', help='Kỳ báo cáo ', default='DAU_THANG_DEN_HIEN_TAI', required='True')
    TU = fields.Date(string='Từ', help='Từ ngày', default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến ngày', default=fields.Datetime.now)
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản', required='True')
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', required='True')
    TK_NGAN_HANG_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='TK ngân hàng', help='Tài khoản ngân hàng')
    CONG_GOP_THEO_CHUNG_TU = fields.Boolean(string='Cộng gộp theo chứng từ', help='Cộng gộp theo chứng từ')
    NGAY_THANG_GHI_SO = fields.Date(string='Ngày,tháng ghi sổ', help='Ngày tháng ghi sổ')
    SO_HIEU = fields.Char(string='Số hiệu', help='Số hiệu')
    NGAY_THANG = fields.Date(string='Ngày,tháng', help='Ngày tháng')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    GHI_NO_TK = fields.Char(string='Ghi Nợ TK', help='Ghi nợ tài khoản')
    TK_TRONG_1 = fields.Char(string=' ', help='Tài khoản trống 1')
    TK_TRONG_2 = fields.Char(string=' ', help='Tài khoản trống 2')
    TK_TRONG_3 = fields.Char(string=' ', help='Tài khoản trống 3')
    TK_TRONG_4 = fields.Char(string=' ', help='Tài khoản trống 4')
    SO_TIEN = fields.Char(string='Số tiền', help='Số tiền')
    SO_HIEU_TK_KHAC = fields.Char(string='Số hiệu', help='Số hiệu tài khoản khác')
 
    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')
    
    ### START IMPLEMENTING CODE ###
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
        TAI_KHOAN_ID = params['TAI_KHOAN_ID'] if 'TAI_KHOAN_ID' in params.keys() else 'False'
        currency_id = params['currency_id'] if 'currency_id' in params.keys() else 'False'
        TK_NGAN_HANG_ID = params['TK_NGAN_HANG_ID'] if 'TK_NGAN_HANG_ID' in params.keys() else 'False'
        CONG_GOP_THEO_CHUNG_TU = params['CONG_GOP_THEO_CHUNG_TU'] if 'CONG_GOP_THEO_CHUNG_TU' in params.keys() else 'False'
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
                'GHI_NO_TK': '',
                'TK_TRONG_1': '',
                'TK_TRONG_2': '',
                'TK_TRONG_3': '',
                'TK_TRONG_4': '',
                'SO_TIEN': '',
                'SO_HIEU_TK_KHAC': '',
                })
        return record

   
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

    @api.model
    def default_get(self,default_fields):
        res = super(BAO_CAO_S03A1_DN_SO_NHAT_KY_THU_TIEN, self).default_get(default_fields)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        tai_khoan =  self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','111')],limit=1)
        loai_tien = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')],limit=1)
        tai_khoan_ngan_hang = self.env['danh.muc.tai.khoan.ngan.hang'].search([],limit=1)
        if chi_nhanh:
            res['CHI_NHANH_ID'] = chi_nhanh.id
        if tai_khoan : 
            res['TAI_KHOAN_ID'] = tai_khoan.id
        if loai_tien :
            res['currency_id'] = loai_tien.id
        if tai_khoan_ngan_hang :
            res['TK_NGAN_HANG_ID'] = tai_khoan_ngan_hang.id
        return res
        
    def _action_view_report(self):
        self._validate()
        TU = self.get_vntime('TU')
        DEN = self.get_vntime('DEN')
        param = 'Từ ngày: %s đến ngày %s' % (TU, DEN)
        action = self.env.ref('bao_cao.open_report__s03a1_dn_so_nhat_ky_thu_tien').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action
