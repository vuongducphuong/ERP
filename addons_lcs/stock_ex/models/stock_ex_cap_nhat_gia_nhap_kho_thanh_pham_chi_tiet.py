# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class STOCK_EX_CAP_NHAT_GIA_NHAP_KHO_THANH_PHAM_CHI_TIET(models.Model):
    _name = 'stock.ex.cap.nhat.gia.nhap.kho.thanh.pham.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']


    AUTO_SELECT = fields.Boolean()
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng')
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits= decimal_precision.get_precision('DON_GIA'))
    CAP_NHAT_GIA_NHAP_KHO_THANH_PHAM_ID = fields.Many2one('stock.ex.cap.nhat.gia.nhap.kho.thanh.pham', string='Cập nhật giá nhập kho thành phẩm', help='Cập nhật giá nhập kho thành phẩm')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    