# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ASSET_TINH_KHAU_HAO_CHI_TIET(models.Model):
    _name = 'asset.tinh.khau.hao.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MA_TAI_SAN_ID = fields.Many2one('asset.ghi.tang', string='Mã tài sản', help='Mã tài sản')
    
    TEN_TAI_SAN = fields.Char(string='Tên tài sản', help='Tên tài sản',related='MA_TAI_SAN_ID.TEN_TAI_SAN',store=True)
    LOAI_TAI_SAN = fields.Char(string='Loại tài sản', help='Loại tài sản')
    LOAI_TAI_SAN_ID = fields.Many2one('danh.muc.loai.tai.san.co.dinh', string='Loại tài sản', help='Loại tài sản',compute='set_tai_san',store=True)
    DON_VI_SU_DUNG_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị sử dụng', help='Đơn vị sử dụng')
    GIA_TRI_KH_THANG = fields.Float(string='Giá trị kh tháng', help='Giá trị kh tháng',digits=decimal_precision.get_precision('VND'))
    GIA_TRI_TINH_VAO_CP_HOP_LY = fields.Float(string='Giá trị tính vào cp hợp lý', help='Giá trị tính vào cp hợp lý',digits=decimal_precision.get_precision('VND'))
    GIA_TRI_TINH_VAO_CP_KHONG_HOP_LY = fields.Float(string='Giá trị tính vào cp không hợp lý', help='Giá trị tính vào cp không hợp lý',digits=decimal_precision.get_precision('VND'))
    TINH_KHAU_HAO_ID = fields.Many2one('asset.tinh.khau.hao', string='Tính khấu hao', help='Tính khấu hao', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    sequence = fields.Integer()

    @api.depends('MA_TAI_SAN_ID')
    def set_tai_san(self):
        for record in self:
            record.LOAI_TAI_SAN_ID = record.MA_TAI_SAN_ID.LOAI_TAI_SAN_ID 


