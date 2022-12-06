# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
class SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN(models.Model):
    _name = 'sale.ex.doi.tru.chung.tu.chi.tiet.thanh.toan'
    _description = ''
    _inherit = ['mail.thread']
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    MA_NHAN_VIEN_ID = fields.Many2one('res.partner', string='Mã nhân viên', help='Mã nhân viên')
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='Tên nhân viên')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('Product Price'))
    SO_TIEN_QUY_DOI = fields.Float(string='Số tiền quy đổi', help='Số tiền quy đổi')
    TY_GIA_DANH_GIA_LAI = fields.Float(string='Tỷ giá đánh giá lại', help='Tỷ giá đánh giá lại')
    SO_CHUA_DOI_TRU = fields.Float(string='Số chưa đối trừ', help='Số chưa đối trừ',digits=decimal_precision.get_precision('Product Price'))
    SO_CHUA_DOI_TRU_QUY_DOI = fields.Float(string='Số chưa đối trừ quy đổi', help='Số chưa đối trừ quy đổi')
    SO_TIEN_DOI_TRU = fields.Float(string='Số tiền đối trừ', help='Số tiền đối trừ',digits=decimal_precision.get_precision('Product Price'))
    SO_TIEN_DOI_TRU_QUY_DOI = fields.Float(string='Số tiền đối trừ quy đổi', help='Số tiền đối trừ quy đổi')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')
    TEN_LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    CHON = fields.Boolean(string='Chọn', help='Chọn')
    DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_ID = fields.Many2one('sale.ex.doi.tru.chung.tu', string='Đối trừ chứng từ chi tiết thanh toán', help='Đối trừ chứng từ chi tiết thanh toán')
    AUTO_SELECT = fields.Boolean()
    ID_CHUNG_TU_THANH_TOAN = fields.Char(string='Id chứng từ thanh toán', help='Id chứng từ thanh toán')
    MODEL_CHUNG_TU_THANH_TOAN = fields.Char(string='Model chứng từ thanh toán', help='Model chứng từ thanh toán')