# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
class SO_KHO_CHI_TIET(models.Model):
    _inherit = 'so.kho.chi.tiet'

    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng', help='ContractID')
    