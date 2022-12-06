# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DON_MUA_HANG_CHI_TIET(models.Model):
    _inherit = 'purchase.ex.don.mua.hang.chi.tiet'

    HOP_DONG_MUA_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang', string='Hợp đồng mua', help='Hợp đồng mua')