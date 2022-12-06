# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class DANH_MUC_VAT_TU_HANG_HOA_CHIET_KHAU(models.Model):
    _name = 'danh.muc.vat.tu.hang.hoa.chiet.khau'
    _description = ''
    _inherit = ['mail.thread']
    SO_LUONG_TU = fields.Float(string='Số lượng từ', help='Số lượng từ', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_DEN = fields.Float(string='Số lượng đến', help='Số lượng đến', digits=decimal_precision.get_precision('SO_LUONG'))
    CHIET_KHAU = fields.Float(string='Chiết khấu', help='Chiết khấu')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    VAT_TU_HANG_HOA_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Vật tư hàng hóa', help='Vật tư hàng hóa', ondelete='cascade')