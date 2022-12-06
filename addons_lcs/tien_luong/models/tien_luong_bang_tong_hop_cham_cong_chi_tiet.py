# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class TIEN_LUONG_BANG_TONG_HOP_SO_CONG_CHI_TIET(models.Model):
    _name = 'tien.luong.bang.tong.hop.cham.cong.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    _order = "STT,id"
    
    STT = fields.Integer(string='STT', help='Số thứ tự')
    MA_NHAN_VIEN = fields.Many2one('res.partner', string='Mã nhân viên', help='Mã nhân viên')
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='Tên nhân viên', related='MA_NHAN_VIEN.HO_VA_TEN', )
    CON_OM = fields.Float(string='Con ốm', help='Con ốm',digits= decimal_precision.get_precision('SO_CONG'))
    HOI_NGHI_HOC_TAP = fields.Float(string='Hội nghị, học tập', help='Hội nghị học tập',digits= decimal_precision.get_precision('SO_CONG'))
    LAO_DONG_NGHIA_VU = fields.Float(string='Lao động nghĩa vụ', help='Lao động nghĩa vụ',digits= decimal_precision.get_precision('SO_CONG'))
    LUONG_SAN_PHAM = fields.Float(string='Lương sản phẩm', help='Lương sản phẩm',digits= decimal_precision.get_precision('SO_CONG'))
    LUONG_THOI_GIAN_CA_NGAY = fields.Float(string='Lương thời gian(cả ngày)', help='Lương thời gian(cả ngày)',digits= decimal_precision.get_precision('SO_CONG'))
    LUONG_THOI_GIAN_NUA_NGAY = fields.Float(string='Lương thời gian(nửa ngày)', help='Lương thời gian(nửa ngày)',digits= decimal_precision.get_precision('SO_CONG'))
    NGHI_BU = fields.Float(string='Nghỉ bù', help='Nghỉ bù',digits= decimal_precision.get_precision('SO_CONG'))
    NGHI_KHONG_LUONG = fields.Float(string='Nghỉ không lương', help='Nghỉ không lương',digits= decimal_precision.get_precision('SO_CONG'))
    NGHI_PHEP = fields.Float(string='Nghỉ phép', help='Nghỉ phép',digits= decimal_precision.get_precision('SO_CONG'))
    NGUNG_VIEC = fields.Float(string='Ngừng việc', help='Ngừng việc',digits= decimal_precision.get_precision('SO_CONG'))
    OM_DIEU_DUONG = fields.Float(string='Ốm điều dưỡng', help='Ốm điều dưỡng',digits= decimal_precision.get_precision('SO_CONG'))
    TAI_NAN = fields.Float(string='Tai nạn', help='Tai nạn',digits= decimal_precision.get_precision('SO_CONG'))
    THAI_SAN = fields.Float(string='Thai sản', help='Thai sản',digits= decimal_precision.get_precision('SO_CONG'))
    SO_CONG_HUONG = fields.Float(string='Số công hưởng 100% lương', help='Số công hưởng 100% lương',digits= decimal_precision.get_precision('SO_CONG'))
    SO_CONG_KHONG_HUONG = fields.Float(string='Số công không hưởng 100% lương', help='Số công không hưởng 100% lương',digits= decimal_precision.get_precision('SO_CONG'))
    NGAY_THUONG_BAN_NGAY = fields.Float(string='Ngày thường', help='Ngày thường',digits= decimal_precision.get_precision('SO_CONG'))
    THU_BAY_CHU_NHAT_BAN_NGAY = fields.Float(string='Ngày thứ 7, chủ nhật', help='Ngày thứ 7, chủ nhật',digits= decimal_precision.get_precision('SO_CONG'))
    LE_TET_BAN_NGAY = fields.Float(string='Ngày lễ, tết', help='Lễ tết ban ngày',digits= decimal_precision.get_precision('SO_CONG'))
    NGAY_THUONG_BAN_DEM = fields.Float(string='Ngày thường', help='Ngày thường',digits= decimal_precision.get_precision('SO_CONG'))
    THU_BAY_CHU_NHAT_BAN_DEM = fields.Float(string='Ngày thứ 7, chủ nhật', help='Ngày thứ 7, chủ nhật',digits= decimal_precision.get_precision('SO_CONG'))
    LE_TET_BAN_DEM = fields.Float(string='Ngày lễ, tết', help='Ngày lễ, tết',digits= decimal_precision.get_precision('SO_CONG'))
    TONG = fields.Float(string='Tổng', help='Tổng',digits= decimal_precision.get_precision('SO_CONG'))
    CHI_TIET_ID = fields.Many2one('tien.luong.bang.tong.hop.cham.cong', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    PHONG_BAN = fields.Char(string='Phòng ban', help='Phòng ban')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', related='MA_NHAN_VIEN.DON_VI_ID', store=True, )
    
    @api.onchange('HOI_NGHI_HOC_TAP','LAO_DONG_NGHIA_VU','LUONG_THOI_GIAN_CA_NGAY','LUONG_THOI_GIAN_NUA_NGAY','NGHI_BU','NGHI_PHEP','THAI_SAN')
    def update_SO_CONG_HUONG(self):
        self.SO_CONG_HUONG = self.HOI_NGHI_HOC_TAP + self.LAO_DONG_NGHIA_VU + self.LUONG_THOI_GIAN_CA_NGAY + self.LUONG_THOI_GIAN_NUA_NGAY + self.NGHI_BU + self.NGHI_PHEP + self.THAI_SAN

    @api.onchange('CON_OM','LUONG_SAN_PHAM','NGHI_KHONG_LUONG','NGUNG_VIEC','OM_DIEU_DUONG','TAI_NAN')
    def update_SO_CONG_KHONG_HUONG(self):
        self.SO_CONG_KHONG_HUONG = self.CON_OM + self.LUONG_SAN_PHAM + self.NGHI_KHONG_LUONG + self.NGUNG_VIEC + self.OM_DIEU_DUONG + self.TAI_NAN 

    @api.onchange('NGAY_THUONG_BAN_NGAY','THU_BAY_CHU_NHAT_BAN_NGAY','LE_TET_BAN_NGAY','NGAY_THUONG_BAN_DEM','THU_BAY_CHU_NHAT_BAN_DEM','LE_TET_BAN_DEM')
    def update_TONG(self):
        self.TONG = self.NGAY_THUONG_BAN_NGAY + self.THU_BAY_CHU_NHAT_BAN_NGAY + self.LE_TET_BAN_NGAY + self.NGAY_THUONG_BAN_DEM + self.THU_BAY_CHU_NHAT_BAN_DEM + self.LE_TET_BAN_DEM

    