# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED
from odoo import api, models, fields

class STOCK_EX_NHAP_XUAT_KHO(models.Model):
    _inherit = 'stock.ex.nhap.xuat.kho'

    SOURCE_ID = fields.Reference(selection_add=[
        ('sale.document', 'Chứng từ bán hàng'),
        ('sale.ex.tra.lai.hang.ban', 'Chứng từ trả lại hàng bán'),        
        ], string='Lập từ')
    SALE_DOCUMENT_IDS = fields.Many2many('sale.document', 'sale_ex_document_outward_rel')
    
class STOCK_EX_NHAP_XUAT_KHO_CHI_TIET(models.Model):
    _inherit = 'stock.ex.nhap.xuat.kho.chi.tiet'
    
    SALE_DOCUMENT_LINE_IDS = fields.Many2many('sale.document.line', 'sale_ex_document_outward_detail_ref',string='Chi tiết chứng từ')
    TRA_LAI_HANG_BAN_CHI_TIET_IDS = fields.Many2many('sale.ex.tra.lai.hang.ban.chi.tiet', 'sale_ex_return_inward_detail_ref',string='Chi tiết chứng từ')