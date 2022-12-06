# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class PURCHASE_EX_LAP_TU_CHUNG_TU_BAN_HANG_FORM_CHI_TIET(models.Model):
    _name = 'purchase.ex.lap.tu.chung.tu.ban.hang.form.chi.tiet'
    _description = ''
    _auto = False

    AUTO_SELECT = fields.Boolean()
    ID_CHUNG_TU_BAN_HANG = fields.Integer(string='id chứng từ bán hàng')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Số đơn hàng')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Mã hàng')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Tên hàng')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Số lượng chưa nhận')
    SO_HOA_DON = fields.Date(string='Số hóa đơn', help='Đơn giá')
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Thành tiền')
    TY_GIA = fields.Float(string='Tỷ giá', help='Số lượng nhận')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    TEN_DOI_TUONG = fields.Char( string='Tên đối tượng', help='Tên đối tượng')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    TEN_CHI_NHANH = fields.Char(string='Chi nhánh', help='Chi nhánh')
    CHI_TIET_ID = fields.Many2one('purchase.ex.lap.tu.chung.tu.ban.hang.form', string='Chi tiết', help='Chi tiết')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(PURCHASE_EX_LAP_TU_CHUNG_TU_BAN_HANG_FORM_CHI_TIET, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result