# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_DIEU_KHOAN_THAN_TOAN(models.Model):
    _inherit = 'account.payment.term'
    
    MA_DIEU_KHOAN = fields.Char(string='Mã điều khoản', help='Mã điều khoản')
    SO_NGAY_DUOC_NO = fields.Float(string ='Số ngày được nợ',help='Số ngày được nợ')
    THOI_HAN_HUONG_CK = fields.Float(string ='Thời hạn hưởng CK (ngày)',help='Thời hạn hưởng CK (ngày)')
    TY_LE_CK = fields.Float(string ='Tỷ lệ CK(%)',help='Tỷ lệ CK(%)')
    HAN_THANH_TOAN = fields.Date(string='Hạn thanh toán', help='Hạn thanh toán')