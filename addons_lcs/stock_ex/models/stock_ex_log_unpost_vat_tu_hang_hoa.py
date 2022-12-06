# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class STOCK_EX_LOG_UNPOST_VAT_TU_HANG_HOA(models.Model):
    _name = 'stock.ex.log.unpost.vat.tu.hang.hoa'
    _description = ''
    _inherit = ['mail.thread']
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    THOI_GIAN_THUC_HIEN = fields.Datetime(string='Thời gian thực hiện', help='Thời gian thực hiện')
    LOAI_HANH_DONG = fields.Char(string='Loại hành động ', help='Loại hành động ')
    ID_CHUNG_TU = fields.Integer(string='Id chứng từ', help='Id chứng từ')
    MODEL_CHUNG_TU = fields.Char(string='Model chứng từ', help='Model chứng từ')
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_THU_TU_CHUNG_TU = fields.Integer(string='Số thứ tự chứng từ', help='Số thứ tự chứng từ')
    CHI_NHANH_ID = fields.Many2one('danh.muc.co.cau.to.chuc', string='Chi nhánh', help='Chi nhánh')
    ID_CHUNG_TU_CHI_TIET = fields.Integer(string='Id chứng từ chi tiết', help='Id chứng từ chi tiết')
    MODEL_CHUNG_TU_CHI_TIET = fields.Char(string='Model chứng từ chi tiết', help='Model chứng từ chi tiết')
    VAT_TU_HANG_HOA_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Vật tư hàng hóa', help='Vật tư hàng hóa')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')