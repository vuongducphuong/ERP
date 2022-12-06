# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class PURCHASE_EX_PHAN_BO_CHI_PHI_MUA_HANG(models.Model):
    _name = 'purchase.ex.phan.bo.chi.phi.mua.hang'
    _description = ''
    _inherit = ['mail.thread']
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng')
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    THANH_TIEN = fields.Float(string='Thành tiền', help='Thành tiền')
    TY_LE_PHAN_BO = fields.Float(string='Tỷ lệ phân bổ', help='Tỷ lệ phân bổ')
    CHI_PHI_MUA_HANG = fields.Float(string='Chi phí mua hàng', help='Chi phí mua hàng')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CHUNG_TU_MUA_HANG_ID = fields.Many2one('purchase.document', string='Chứng từ mua hàng chi tiết', help='Chứng từ mua hàng chi tiết', ondelete='cascade')