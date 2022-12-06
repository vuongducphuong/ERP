# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class PURCHASE_EX_NHAN_HOA_DON_CHI_TIET(models.Model):
    _name = 'purchase.ex.nhan.hoa.don.chi.tiet'
    _description = ''
    _auto = False

    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    ID_ct_muahang  =  fields.Integer(string='ID', help='ID')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    LOAI_TIEN = fields.Char(string='Loại tiền', help='Loại tiền')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá',digits= decimal_precision.get_precision('Product Price'))
    SO_TIEN = fields.Float(string='Số tiền ', help='Số tiền ',digits= decimal_precision.get_precision('Product Price'))
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CHON = fields.Boolean(string='Chọn', help='Chọn')
    NHAN_HOA_DON_CHI_TIET_ID = fields.Many2one('purchase.ex.nhan.hoa.don', string='Nhận hóa đơn chi tiết ', help='Nhận hóa đơn chi tiết')
    AUTO_SELECT = fields.Boolean()
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(PURCHASE_EX_NHAN_HOA_DON_CHI_TIET, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result

    def action_view_result(self):
        action = self.env.ref('purchase_ex.action_open_purchase_ex_nhan_hoa_don_chi_tiet_form').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        return action
