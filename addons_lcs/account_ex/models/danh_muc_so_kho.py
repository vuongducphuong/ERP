# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
class SO_KHO_CHI_TIET(models.Model):
    _inherit = 'so.kho.chi.tiet'

    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='OrderID')
    