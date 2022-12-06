# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SALE_EX_DON_DAT_HANG_XEM_SL_TON_CHUA_DAT_HANG_FORM(models.Model):
    _name = 'sale.ex.don.dat.hang.xem.sl.ton.chua.dat.hang.form'
    _description = ''
    _inherit = ['mail.thread']
    MH = fields.Char(string='Mh', help='Mh')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    SALE_EX_DON_DAT_HANG_XEM_SL_TON_CHUA_DAT_HANG_CHI_TIET_FORM_IDS = fields.One2many('sale.ex.don.dat.hang.xem.sl.ton.chua.dat.hang.chi.tiet.form', 'DON_DAT_HANG_XEM_SL_TON_CHUA_DAT_HANG_CHI_TIET_ID', string='Đơn đặt hàng xem SL tồn chưa đặt hàng chi tiết form')