# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class PURCHASE_EX_DON_MUA_HANG_CHI_TIET(models.Model):
    _inherit = 'purchase.ex.don.mua.hang.chi.tiet'

    # LENH_SAN_XUAT_ID = fields.Many2one('stock.ex.lenh.san.xuat', string='Lệnh sản xuất', help='Lệnh sản xuất')
    # LENH_SAN_XUAT_CHI_TIET_ID = fields.Many2one('stock.ex.lenh.san.xuat.chi.tiet.thanh.pham', string='Lệnh sản xuất chi tiết', help='Lệnh sản xuất chi tiết')