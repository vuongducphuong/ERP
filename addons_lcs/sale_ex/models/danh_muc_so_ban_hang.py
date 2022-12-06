# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SO_BAN_HANG(models.Model):
    _inherit = 'so.ban.hang.chi.tiet'

    CHUNG_TU_BAN_HANG_ID = fields.Many2one('sale.document', string='chứng từ bán hàng', help='chứng từ bán hàng')
    CHUNG_TU_BAN_HANG_CHI_TIET_ID = fields.Many2one('sale.document.line', string='chứng từ bán hàng chi tiết', help='chứng từ bán hàng chi tiết')