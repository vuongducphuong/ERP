# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO(models.Model):
    _name = 'sale.ex.doi.tru.chung.tu.chi.tiet.cong.no'
    _description = ''
    _inherit = ['mail.thread']
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    HAN_THANH_TOAN = fields.Date(string='Hạn thanh toán', help='Hạn thanh toán')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    MA_NHAN_VIEN_ID = fields.Many2one('res.partner', string='Mã nhân viên', help='Mã nhân viên')
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='Tên nhân viên')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('Product Price'))
    SO_TIEN_QUY_DOI = fields.Float(string='Số tiền quy đổi', help='Số tiền quy đổi')
    TY_GIA_DANH_GIA_LAI = fields.Float(string='Tỷ giá đánh giá lại', help='Tỷ giá đánh giá lại')
    SO_CON_NO = fields.Float(string='Số còn nợ', help='Số còn nợ',digits=decimal_precision.get_precision('Product Price'))
    SO_CON_NO_QUY_DOI = fields.Float(string='Số còn nợ quy đổi', help='Số còn nợ quy đổi')
    SO_TIEN_DOI_TRU = fields.Float(string='Số tiền đối trừ', help='Số tiền đối trừ',digits=decimal_precision.get_precision('Product Price'))
    SO_TIEN_DOI_TRU_QUY_DOI = fields.Float(string='Số tiền đối trừ quy đổi', help='Số tiền đối trừ quy đổi')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')
    TEN_LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    CHON = fields.Boolean(string='Chọn', help='Chọn')
    DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_ID = fields.Many2one('sale.ex.doi.tru.chung.tu', string='Đối trừ chứng từ chi tiết công nợ', help='Đối trừ chứng từ chi tiết công nợ')
    AUTO_SELECT = fields.Boolean()
    ID_CHUNG_TU_CONG_NO = fields.Char(string='Chứng từ công nợ', help='Id chứng từ công nợ')
    MODEL_CHUNG_TU_CONG_NO = fields.Char(string='Model chứng từ công nợ', help='Model chứng từ công nợ')