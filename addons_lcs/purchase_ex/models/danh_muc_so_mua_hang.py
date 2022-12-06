# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SO_MUA_HANG(models.Model):
    _inherit = 'so.mua.hang.chi.tiet'

    CHUNG_TU_MUA_HANG_ID = fields.Many2one('purchase.document', string='ID chứng từ mua hàng', help='ID chứng từ mua hàng')
    CHUNG_TU_MUA_HANG_CHI_TIET_ID = fields.Many2one('purchase.document.line', string='ID chứng từ mua hàng chi tiết', help='ID chứng từ mua hàng chi tiết')