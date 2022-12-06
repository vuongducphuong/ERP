# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_product_category_ex(models.Model):
    _inherit = 'product.category'
    MA_NHOM = fields.Char(string='Mã nhóm vật tư, hàng hóa, dịch vụ', help='Mã nhóm vật tư, hàng hóa, dịch vụ')