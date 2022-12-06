# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ACCOUNT_EX_SO_CONG_NO_EX(models.Model):
    _inherit = 'so.cong.no.chi.tiet'
    _description = ''

    DON_DAT_HANG = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    DON_MUA_HANG_ID = fields.Many2one('purchase.ex.don.mua.hang', string='Đơn mua hàng')
	
    
    