# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
class DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI(models.Model):
    _name = 'danh.muc.vat.tu.hang.hoa.don.vi.chuyen.doi'
    _description = ''
    _inherit = ['mail.thread']
    STT = fields.Integer(string='Stt', help='Stt')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Đơn vị chuyển đổi', help='Đơn vị chuyển đổi')
    TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH = fields.Float(string='Tỷ lệ chuyển đổi và đơn vị chính', help='Tỷ lệ chuyển đổi và đơn vị chính')
    PHEP_TINH_CHUYEN_DOI = fields.Selection([('PHEP_NHAN', 'Phép nhân'), ('PHEP_CHIA', 'Phép chia'), ], string='Phép tính chuyển đổi', help='Phép tính chuyển đổi',default="PHEP_NHAN")
    MO_TA = fields.Char(string='Mô tả', help='Mô tả')
    VAT_TU_HANG_HOA_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Vật tư hàng hóa', help='Vật tư hàng hóa', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    DON_GIA_BAN_1 = fields.Float(string='Đơn giá bán 1', help='Giá bán 1',digits=decimal_precision.get_precision('DON_GIA'))
    DON_GIA_BAN_2 = fields.Float(string='Đơn giá bán 2', help='Giá bán 2',digits=decimal_precision.get_precision('DON_GIA'))
    DON_GIA_BAN_3 = fields.Float(string='Đơn giá bán 3', help='Giá bán 3',digits=decimal_precision.get_precision('DON_GIA'))
    DON_GIA_CO_DINH = fields.Float(string='Đơn giá cố định', help='Đơn giá cố định',digits=decimal_precision.get_precision('DON_GIA'))

