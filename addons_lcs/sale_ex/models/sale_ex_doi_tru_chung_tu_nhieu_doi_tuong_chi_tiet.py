# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SALE_EX_DOI_TRU_CHUNG_TU_NHIEU_DOI_TUONG_CHI_TIET(models.Model):
    _name = 'sale.ex.doi.tru.chung.tu.nhieu.doi.tuong.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MA_KHACH_HANG_ID = fields.Many2one('res.partner', string='Mã khách hàng', help='Mã khách hàng')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    NHOM_KHACH_HANG_ID = fields.Many2one('danh.muc.nhom.khach.hang.nha.cung.cap', string='Nhóm khách hàng', help='Nhóm khách hàng')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    CHON = fields.Char(string='Chọn', help='Chọn')
    AUTO_SELECT = fields.Boolean()

    SO_THANH_TOAN_CHUA_DOI_TRU = fields.Float(string='Số thanh toán chưa đối trừ', help='Số thanh toán chưa đối trừ')
    SO_CONG_NO_CHUA_DOI_TRU = fields.Float(string='Số công nợ chưa đối trừ', help='Số công nợ chưa đối trừ')
    DOI_TRU_CHUNG_TU_NHIEU_DOI_TUONG_CHI_TIET_ID = fields.Many2one('sale.ex.doi.tru.chung.tu.nhieu.doi.tuong', string='Đối trừ chứng từ nhiều đối tượng chi tiết', help='Đối trừ chứng từ nhiều đối tượng chi tiết')
    SO_CHUA_DOI_TRU_THANH_TOAN = fields.Float(string='Số chưa đối trừ', help='Số chưa đối trừ thanh toán')
    SO_CHUA_DOI_TRU_QUY_DOI_THANH_TOAN = fields.Float(string='Số chưa đối trừ quy đổi', help='Số chưa đối trừ quy đổi thanh toán')
    SO_DOI_TRU_THANH_TOAN = fields.Float(string='Số đối trừ', help='Số đối trừ thanh toán')
    SO_DOI_TRU_QUY_DOI_THANH_TOAN = fields.Float(string='Số đối trừ quy đổi', help='Số đối trừ quy đổi thanh toán')
    SO_CHUA_DOI_TRU_CONG_NO = fields.Float(string='Số chưa đối trừ', help='Số chưa đối trừ công nợ')
    SO_CHUA_DOI_TRU_QUY_DOI_CONG_NO = fields.Float(string='Số chưa đối trừ quy đổi', help='Số chưa đối trừ quy đổi công nợ')
    SO_DOI_TRU_CONG_NO = fields.Float(string='Số đối trừ', help='Số đối trừ công nợ')
    SO_DOI_TRU_QUY_DOI_CONG_NO = fields.Float(string='Số đối trừ quy đổi', help='Số đối trừ quy đổi công nợ')
    CHENH_LECH_TY_GIA = fields.Float(string='Chênh lệch tỷ giá', help='Chênh lệch tỷ giá')
    TK_XU_LY_CHENH_LECH_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK xử lý chênh lệch', help='Tk xử lý chênh lệch')