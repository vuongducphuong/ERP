# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class PHIEU_THU_CHI_TIET_INHERIT(models.Model):
    _inherit = 'account.ex.phieu.thu.chi.thue'

    CHUNG_TU_MUA_HANG_ID = fields.Many2one('purchase.document', string='Chứng từ mua hàng', help='Chứng từ mua hàng')
    CHUNG_TU_MUA_HANG_CHI_TIET_ID = fields.Many2one('purchase.document.line', string='Chứng từ mua hàng chi tiết', help='Chứng từ mua hàng chi tiết')