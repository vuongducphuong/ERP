# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.addons import decimal_precision
from datetime import timedelta, datetime
from odoo.tools.float_utils import float_round


class ASSET_TAI_SAN_CO_DINH_GHI_GIAM_TAI_SAN(models.Model):
    _name = 'asset.ghi.giam.tai.san'
    _description = ''
    _inherit = ['mail.thread']
    MA_TAI_SAN = fields.Many2one('asset.ghi.tang', string='Mã tài sản', help='Mã tài sản')
    TEN_TAI_SAN = fields.Char(string='Tên tài sản', help='Tên tài sản',related='MA_TAI_SAN.TEN_TAI_SAN',store=True )
    DON_VI_SU_DUNG_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị sử dụng', help='Đơn vị sử dụng')
    NGUYEN_GIA = fields.Float(string='Nguyên giá', help='Nguyên giá',digits=decimal_precision.get_precision('VND'))
    GIA_TRI_TINH_KHAU_HAO = fields.Float(string='Giá trị tính khấu hao', help='Giá trị tính khấu hao' ,digits=decimal_precision.get_precision('VND'))
    HAO_MON_LUY_KE = fields.Float(string='Hao mòn lũy kế', help='Hao mòn lũy kế' ,digits=decimal_precision.get_precision('VND'))
    GIA_TRI_CON_LAI = fields.Float(string='Giá trị còn lại', help='Giá trị còn lại' ,digits=decimal_precision.get_precision('VND'))
    TK_NGUYEN_GIA_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk nguyên giá', help='Tk nguyên giá')
    TK_HAO_MON_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk hao mòn', help='Tk hao mòn')
    TK_XU_LY_GIA_TRI_CON_LAI_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk xử lý giá trị còn lại', help='Tk xử lý giá trị còn lại')
    TAI_SAN_CO_DINH_GHI_GIAM_ID = fields.Many2one('asset.ghi.giam', string='Tài sản cố định ghi giảm', help='Tài sản cố định ghi giảm', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán',related='TAI_SAN_CO_DINH_GHI_GIAM_ID.NGAY_HACH_TOAN')

    @api.onchange('MA_TAI_SAN')
    def _onchange_MA_TAI_SAN(self):
        self.update_gia_tri_tscd()
    
    def update_gia_tri_tscd(self):
        # số khấu hao = ((ngày ghi giảm - 1) / số ngày trong tháng ghi giảm) * giá trị khấu hao tháng ở trong sổ
        # hao mòn lũy kế = hao mòn lũy kế trong sổ + số khâu hao
        # giá trị còn lại = giá trị còn lại trong sổ - số khấu hao
        if self.MA_TAI_SAN:
            tscd = self.MA_TAI_SAN.lay_du_lieu_phan_bo(self.NGAY_HACH_TOAN)
            gia_tri_tren_so = self.MA_TAI_SAN.lay_du_lieu_tren_so(self.NGAY_HACH_TOAN)
            du_lieu_tinh_gtcl = self.MA_TAI_SAN.lay_du_lieu_tren_so_de_tinh_gtcl(self.NGAY_HACH_TOAN)
            if gia_tri_tren_so:
                so_khau_hao = 0
                if du_lieu_tinh_gtcl:
                    ngay_cuoi_cung_tren_so = datetime.strptime(du_lieu_tinh_gtcl.NGAY_HACH_TOAN, '%Y-%m-%d').date()
                    ngay_hien_tai = datetime.strptime(self.NGAY_HACH_TOAN, '%Y-%m-%d').date()
                    so_ngay_trong_thang = helper.Datetime.lay_so_ngay_trong_thang(ngay_hien_tai.year, ngay_hien_tai.month)
                    if ngay_cuoi_cung_tren_so.month == ngay_hien_tai.month and ngay_cuoi_cung_tren_so.year == ngay_hien_tai.year and so_ngay_trong_thang != 0:
                        so_khau_hao = ((ngay_hien_tai.day - ngay_cuoi_cung_tren_so.day + 1)/so_ngay_trong_thang)*du_lieu_tinh_gtcl.GIA_TRI_KHAU_HAO_THANG
                    else:
                        so_khau_hao = ((ngay_hien_tai.day - 1)/so_ngay_trong_thang)*du_lieu_tinh_gtcl.GIA_TRI_KHAU_HAO_THANG
                if tscd:
                    self.TEN_TAI_SAN = tscd[0].get('TEN_TSCD')
                    self.DON_VI_SU_DUNG_ID = tscd[0].get('DON_VI_SU_DUNG_ID')
                    self.NGUYEN_GIA = tscd[0].get('NGUYEN_GIA')
                    self.GIA_TRI_TINH_KHAU_HAO = tscd[0].get('GIA_TRI_TINH_KHAU_HAO')
                    self.HAO_MON_LUY_KE = float_round(gia_tri_tren_so.GIA_TRI_HAO_MON_LUY_KE + so_khau_hao,0)
                    self.GIA_TRI_CON_LAI = float_round(gia_tri_tren_so.GIA_TRI_CON_LAI - so_khau_hao,0)
                    self.TK_NGUYEN_GIA_ID = tscd[0].get('TK_NGUYEN_GIA_ID')
                    self.TK_HAO_MON_ID = tscd[0].get('TK_HAO_MON_ID')
                    self.TK_XU_LY_GIA_TRI_CON_LAI_ID = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like', '811')])
