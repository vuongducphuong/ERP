# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper

class PURCHASE_EX_NHAN_HOA_DON_MUA_HANG_HOA(models.Model):
    _inherit = 'purchase.ex.hoa.don.mua.hang'

    SOURCE_ID = fields.Reference(selection_add=[
        ('sale.ex.tra.lai.hang.ban', 'Chứng từ trả lại hàng bán'),
        ], string='Lập từ')