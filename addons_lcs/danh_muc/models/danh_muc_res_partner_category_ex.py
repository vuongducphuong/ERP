# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_NHOM_KHACH_HANG(models.Model):
    _inherit = 'res.partner.category'
    
    MA_NHOM = fields.Char(string='Mã nhóm KH, NCC', help='Mã nhóm KH, NCC')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')