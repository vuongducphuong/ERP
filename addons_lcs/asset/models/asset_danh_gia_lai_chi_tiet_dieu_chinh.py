# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_DIEU_CHINH(models.Model):
    _name = 'asset.danh.gia.lai.chi.tiet.dieu.chinh'
    _description = ''
    _inherit = ['mail.thread']
    MA_TAI_SAN_ID = fields.Many2one('asset.ghi.tang', string='Mã tài sản', help='Mã tài sản')
    TEN_TAI_SAN = fields.Char(string='Tên tài sản', help='Tên tài sản',related='MA_TAI_SAN_ID.TEN_TAI_SAN',store=True)
    DON_VI_SU_DUNG = fields.Many2one('danh.muc.to.chuc', string='Đơn vị sử dụng', help='Đơn vị sử dụng')
    GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH = fields.Float(string='Trước điều chỉnh', help='Giá trị còn lại trước điều chỉnh',digits= decimal_precision.get_precision('VND'))
    GIA_TRI_CON_LAI_SAU_DIEU_CHINH = fields.Float(string='Sau điều chỉnh', help='Giá trị còn lại sau điều chỉnh',digits= decimal_precision.get_precision('VND'))
    CHENH_LECH_GIA_TRI = fields.Float(string='Chênh lệch', help='Chênh lệch giá trị',digits= decimal_precision.get_precision('VND'))
    THOI_GIAN_CON_LAI_TRUOC_DIEU_CHINH = fields.Float(string='Trước điều chỉnh', help='Thời gian còn lại trước điều chỉnh')
    THOI_GIAN_CON_LAI_SAU_DIEU_CHINH = fields.Float(string='Sau điều chỉnh', help='Thời gian còn lại sau điều chỉnh')
    CHENH_LECH_THOI_GIAN = fields.Float(string='Chênh lệch', help='Chênh lệch thời gian')
    HAO_MON_LUY_KE_TRUOC_DIEU_CHINH = fields.Float(string='Trước điều chỉnh', help='Hao mòn lũy kế trước điều chỉnh',digits= decimal_precision.get_precision('VND'))
    HAO_MON_LUY_KE_SAU_DIEU_CHINH = fields.Float(string='Sau điều chỉnh', help='Hao mòn lũy kế sau điều chỉnh',digits= decimal_precision.get_precision('VND'))
    CHENH_LECH_HAO_MON_LUY_KE = fields.Float(string='Chênh lệch ', help='Chênh lệch hao mòn lũy kế',digits= decimal_precision.get_precision('VND'))
    TK_CHI_PHI_HAO_MON_LUY_KE =fields.Many2one('danh.muc.he.thong.tai.khoan',string='TK chi phí ', help='Tài khoản chi phí hao mòn lũy kế')
    GIA_TRI_KHAU_HAO_TRUOC_DIEU_CHINH = fields.Float(string='Trước điều chỉnh', help='Giá trị khấu hao trước điều chỉnh',digits= decimal_precision.get_precision('VND'))
    GIA_TRI_KHAU_HAO_SAU_DIEU_CHINH = fields.Float(string='Sau điều chỉnh', help='Giá trị khấu hao sau điều chỉnh',digits= decimal_precision.get_precision('VND'))
    CHENH_LECH_GTKH = fields.Float(string='Chênh lệch ', help='Chênh lệch giá trị khấu hao',digits= decimal_precision.get_precision('VND'))
    TK_DANH_GIA_LAI_GTKH = fields.Many2one('danh.muc.he.thong.tai.khoan',string='TK đánh giá lại', help='Tài khoản đánh giá lại giá trị khấu hao')
    GTKH_THANG_SAU_DIEU_CHINH = fields.Float(string='GTKH tháng sau điều chỉnh', help='Giá trị khấu hao tháng sau điều chỉnh',digits= decimal_precision.get_precision('VND'))
    GTKH_THANG_THEO_LUAT_SAU_DIEU_CHINH = fields.Float(string='GTKH tháng theo luật sau điều chỉnh', help='Giá trị khấu hao tháng theo luật sau điều chỉnh',digits= decimal_precision.get_precision('VND'))
    name = fields.Char(string='Name', oldname='NAME')
    DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_ID = fields.Many2one('asset.danh.gia.lai', string='Đánh giá lại tài sản cố định chi tiết ', help='Đánh giá lại tài sản cố định chi tiết ', ondelete='cascade')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán',related='DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_ID.NGAY_HACH_TOAN')

    @api.model
    def default_get(self, fields):
        rec = super(ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_DIEU_CHINH, self).default_get(fields)
        rec['TK_DANH_GIA_LAI_GTKH'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','412')],limit=1).id
        return rec

    @api.onchange('MA_TAI_SAN_ID')
    def update_thongtintscd(self):
        if self.MA_TAI_SAN_ID:
            tscd = self.MA_TAI_SAN_ID.lay_du_lieu_phan_bo(self.NGAY_HACH_TOAN)
            gia_tri = self.MA_TAI_SAN_ID.tinh_gia_tri_con_lai(self.NGAY_HACH_TOAN)
            hao_mon_luy_ke = 0
            gia_tri_con_kai = 0
            if gia_tri:
                hao_mon_luy_ke = gia_tri[0].get('GIA_TRI_KHAU_HAO_LUY_KE')
                gia_tri_con_kai = gia_tri[0].get('GIA_TRI_CON_LAI')
            if tscd:
                self.TEN_TAI_SAN = tscd[0].get('TEN_TSCD')
                self.DON_VI_SU_DUNG = tscd[0].get('DON_VI_SU_DUNG_ID')
                self.GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH = gia_tri_con_kai
                self.GIA_TRI_CON_LAI_SAU_DIEU_CHINH = gia_tri_con_kai
                self.THOI_GIAN_CON_LAI_TRUOC_DIEU_CHINH = tscd[0].get('THOI_GIAN_SU_DUNG_CON_LAI')
                self.THOI_GIAN_CON_LAI_SAU_DIEU_CHINH = tscd[0].get('THOI_GIAN_SU_DUNG_CON_LAI')
                self.HAO_MON_LUY_KE_TRUOC_DIEU_CHINH = hao_mon_luy_ke
                self.HAO_MON_LUY_KE_SAU_DIEU_CHINH = hao_mon_luy_ke
                self.GIA_TRI_KHAU_HAO_TRUOC_DIEU_CHINH = tscd[0].get('GIA_TRI_TINH_KHAU_HAO')
                self.GIA_TRI_KHAU_HAO_SAU_DIEU_CHINH = tscd[0].get('GIA_TRI_TINH_KHAU_HAO')
                self.TK_DANH_GIA_LAI_GTKH = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like', '412')])
                if self.THOI_GIAN_CON_LAI_SAU_DIEU_CHINH != 0:
                    self.GTKH_THANG_SAU_DIEU_CHINH = self.GIA_TRI_CON_LAI_SAU_DIEU_CHINH/self.THOI_GIAN_CON_LAI_SAU_DIEU_CHINH
                    if self.CHENH_LECH_THOI_GIAN > 0:
                        self.GTKH_THANG_THEO_LUAT_SAU_DIEU_CHINH = self.GIA_TRI_CON_LAI_SAU_DIEU_CHINH/self.THOI_GIAN_CON_LAI_SAU_DIEU_CHINH
                    else:
                        self.GTKH_THANG_THEO_LUAT_SAU_DIEU_CHINH = 0
                else:
                    self.GTKH_THANG_SAU_DIEU_CHINH = 0
                    self.GTKH_THANG_THEO_LUAT_SAU_DIEU_CHINH = 0

    @api.onchange('GIA_TRI_CON_LAI_SAU_DIEU_CHINH','THOI_GIAN_CON_LAI_SAU_DIEU_CHINH')
    def _onchange_GIA_TRI_CON_LAI_SAU_DIEU_CHINH(self):
        if self.THOI_GIAN_CON_LAI_SAU_DIEU_CHINH != 0:
            self.GTKH_THANG_SAU_DIEU_CHINH = self.GIA_TRI_CON_LAI_SAU_DIEU_CHINH/self.THOI_GIAN_CON_LAI_SAU_DIEU_CHINH
            if self.CHENH_LECH_THOI_GIAN > 0:
                self.GTKH_THANG_THEO_LUAT_SAU_DIEU_CHINH = self.GIA_TRI_CON_LAI_SAU_DIEU_CHINH/self.THOI_GIAN_CON_LAI_SAU_DIEU_CHINH
            else:
                self.GTKH_THANG_THEO_LUAT_SAU_DIEU_CHINH = 0
        else:
            self.GTKH_THANG_SAU_DIEU_CHINH = 0
            self.GTKH_THANG_THEO_LUAT_SAU_DIEU_CHINH = 0
        self.CHENH_LECH_GIA_TRI = self.GIA_TRI_CON_LAI_SAU_DIEU_CHINH - self.GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH
        self.CHENH_LECH_THOI_GIAN = self.THOI_GIAN_CON_LAI_SAU_DIEU_CHINH - self.THOI_GIAN_CON_LAI_TRUOC_DIEU_CHINH
        

    @api.onchange('CHENH_LECH_GIA_TRI','CHENH_LECH_HAO_MON_LUY_KE')
    def _onchange_CHENH_LECH_GIA_TRI(self):
        self.GIA_TRI_KHAU_HAO_SAU_DIEU_CHINH = self.GIA_TRI_KHAU_HAO_TRUOC_DIEU_CHINH + self.CHENH_LECH_GIA_TRI + self.CHENH_LECH_HAO_MON_LUY_KE
        
    @api.onchange('HAO_MON_LUY_KE_SAU_DIEU_CHINH')
    def _onchange_HAO_MON_LUY_KE_SAU_DIEU_CHINH(self):
        self.CHENH_LECH_HAO_MON_LUY_KE = self.HAO_MON_LUY_KE_SAU_DIEU_CHINH - self.HAO_MON_LUY_KE_TRUOC_DIEU_CHINH

    @api.onchange('GIA_TRI_KHAU_HAO_SAU_DIEU_CHINH')
    def _onchange_GIA_TRI_KHAU_HAO_SAU_DIEU_CHINH(self):
        self.CHENH_LECH_GTKH = self.GIA_TRI_KHAU_HAO_SAU_DIEU_CHINH - self.GIA_TRI_KHAU_HAO_TRUOC_DIEU_CHINH


