# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class STOCK_NHAP_XUAT_KHO_CHI_TIET_HOP_DONG_MUA(models.Model):
    _inherit = 'stock.ex.nhap.xuat.kho.chi.tiet'

    HOP_DONG_MUA_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang', string='Hợp đồng mua', help='Hợp đồng mua')