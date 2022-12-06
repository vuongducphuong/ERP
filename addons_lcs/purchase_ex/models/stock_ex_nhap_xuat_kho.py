# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED
from odoo import api, models, fields

class STOCK_EX_NHAP_XUAT_KHO(models.Model):
    _inherit = 'stock.ex.nhap.xuat.kho'

    SOURCE_ID = fields.Reference(selection_add=[
        ('purchase.document', 'Chứng từ mua hàng'),
        ('purchase.ex.tra.lai.hang.mua', 'Chứng từ trả lại hàng mua'),        
        ], string='Lập từ')
    PURCHASE_DOCUMENT_LINE_IDS = fields.One2many('purchase.document.line', 'PHIEU_XUAT_ID', string='Chi tiết chứng từ', copy=True)

    