# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ACCOUNT_EX_DON_DAT_HANG_XEM_SL_TON_CHUA_DAT_HANG_CHI_TIET_FORM(models.Model):
    _name = 'account.ex.don.dat.hang.xem.sl.ton.chua.dat.hang.chi.tiet.form'
    _description = ''
    _inherit = ['mail.thread']
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng')
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
    DVT_CHINH_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Đvt chính', help='Đvt chính')
    SO_LUONG_TON = fields.Float(string='Số lượng tồn', help='Số lượng tồn', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_TON_CHUA_DAT_HANG = fields.Float(string='Số lượng tồn chưa đặt hàng', help='Số lượng tồn chưa đặt hàng', digits=decimal_precision.get_precision('SO_LUONG'))
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    DON_DAT_HANG_XEM_SL_TON_CHUA_DAT_HANG_CHI_TIET_ID = fields.Many2one('account.ex.don.dat.hang.xem.sl.ton.chua.dat.hang.form', string='Đơn đặt hàng xem sl tồn chưa đặt hàng chi tiết', help='Đơn đặt hàng xem sl tồn chưa đặt hàng chi tiết', ondelete='cascade')