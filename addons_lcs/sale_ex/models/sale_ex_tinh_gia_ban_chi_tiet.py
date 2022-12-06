# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SALE_EX_TINH_GIA_BAN_CHI_TIET(models.Model):
    _name = 'sale.ex.tinh.gia.ban.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng')
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
    NHOM_VTHH_ID = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm vthh', help='Nhóm vthh')
    LIST_NHOM_VTHH = fields.Char(string='Nhóm VTHH', help='Nhóm VTHH')
    DON_VI_TINH_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Đơn vị tính', help='Đơn vị tính')
    GIA_NHAP_GAN_NHAT = fields.Float(string='Giá nhập gần nhất', help='Giá nhập gần nhất')
    GIA_MUA_CO_DINH = fields.Float(string='Giá mua cố định', help='Giá mua cố định')
    GIA_BAN_CO_DINH = fields.Float(string='Giá bán cố định', help='Giá bán cố định')
    GIA_BAN_1 = fields.Float(string='Giá bán 1', help='Giá bán 1')
    GIA_BAN_2 = fields.Float(string='Giá bán 2', help='Giá bán 2')
    GIA_BAN_3 = fields.Float(string='Giá bán 3', help='Giá bán 3')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    TINH_GIA_BAN_CHI_TIET_ID = fields.Many2one('sale.ex.tinh.gia.ban', string='Tính giá bán chi tiết', help='Tính giá bán chi tiết')
    AUTO_SELECT = fields.Boolean()