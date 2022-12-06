# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class SALE_EX_BO_DOI_TRU_CHI_TIET(models.Model):
    _name = 'sale.ex.bo.doi.tru.chi.tiet'
    _description = ''
    _auto = False

    CHON = fields.Boolean(string='Chọn', help='Chọn')
    LOAI_CHUNG_TU_THANH_TOAN = fields.Char(string='Loại chứng từ')
    NGAY_CHUNG_TU_THANH_TOAN = fields.Date(string='Ngày chứng từ')
    SO_CHUNG_TU_THANH_TOAN = fields.Char(string='Số chứng từ')
    SO_DOI_TRU_THANH_TOAN = fields.Float(string='Số đối trừ',digits= decimal_precision.get_precision('Product Price'))
    SO_DOI_TRU_QUY_DOI_THANH_TOAN = fields.Float(string='Số đối trừ quy đổi')
    LOAI_CHUNG_TU_CONG_NO = fields.Char(string='Loại chứng từ')
    NGAY_CHUNG_TU_CONG_NO = fields.Date(string='Ngày chứng từ')
    SO_CHUNG_TU_CONG_NO = fields.Char(string='Số chứng từ')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    SO_DOI_TRU_CONG_NO = fields.Float(string='Số đối trừ',digits=decimal_precision.get_precision('Product Price'))
    SO_DOI_TRU_QUY_DOI_CONG_NO = fields.Float(string='Số đối trừ quy đổi')
    CHENH_LECH_TY_GIA = fields.Float(string='Chênh lệch tỷ giá', help='Chênh lệch tỷ giá',digits= decimal_precision.get_precision('Product Price'))
    SO_CT_XU_LY_CHENH_LECH_TY_GIA = fields.Char(string='Số CT xử lý chênh lệch tỷ giá', help='Số ct xử lý chênh lệch tỷ giá')
    BO_DOI_TRU_CHI_TIET_ID = fields.Many2one('sale.ex.bo.doi.tru', string='Bỏ đối trừ chi tiết', help='Bỏ đối trừ chi tiết')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    AUTO_SELECT = fields.Boolean()
    ID_DOI_TRU = fields.Integer()
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())