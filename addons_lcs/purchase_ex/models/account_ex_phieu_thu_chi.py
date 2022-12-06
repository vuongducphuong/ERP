# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED
from odoo import api, models, fields

class ACCOUNT_EX_PHIEU_THU_CHI(models.Model):
    _inherit = 'account.ex.phieu.thu.chi'

    SOURCE_ID = fields.Reference(selection_add=[
        ('purchase.document', 'Chứng từ mua hàng'),
        ('purchase.ex.tra.lai.hang.mua', 'Chứng từ trả lại hàng mua'),
        ('purchase.ex.giam.gia.hang.mua', 'Chứng từ giảm giá hàng mua'),
        ], string='Lập từ')
    PURCHASE_DOCUMENT_LINE_IDS = fields.One2many('purchase.document.line', 'PHIEU_CHI_ID', string='Chi tiết chứng từ', copy=True)