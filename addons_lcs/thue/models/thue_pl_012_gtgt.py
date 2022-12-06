# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class THUE_PL_012_GTGT(models.Model):
    _name = 'thue.pl.012.gtgt'
    _description = ''
    _inherit = ['mail.thread']
    STT = fields.Char(string='STT', help='STT')
    SO_HOA_DON = fields.Char(string='Số hóa đơn ', help='Số hóa đơn ')
    NGAY_THANG_NAM_LAP_HOA_DON = fields.Char(string='Ngày, tháng, năm lập hóa đơn', help='Ngày tháng năm lập hóa đơn')
    TEN_NGUOI_BAN = fields.Char(string='Tên người bán', help='Tên người bán')
    MA_SO_THUE_NGUOI_BAN = fields.Char(string='Mã số thuế người bán', help='Mã số thuế người bán')
    GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE = fields.Float(string='Giá trị HHDV mua vào chưa có thuế', help='Giá trị HHDV mua vào chưa có thuế', digits=decimal_precision.get_precision('VND'))
    GHI_CHU = fields.Char(string='Ghi chú', help='Ghi chú')
    THUE_GTGT = fields.Float(string='Thuế GTGT', help='Thuế giá trị gia tăng', digits=decimal_precision.get_precision('VND'))
    NHOM_HHDV = fields.Selection([('1', '1. Hàng hóa, dịch vụ dùng riêng cho SXKD chịu thuế GTGT và sử dụng cho các hoạt động cung cấp hàng hóa, dịch vụ không kê khai, nộp thuế GTGT đủ điều kiện khấu trừ thuế'), ('2', '2. Hàng hóa,dịch vụ dùng chung cho SXKD chịu thuế và không chịu thuế đủ điều kiện khấu trừ thuế'), ('3', '3. Hàng hóa,dịch vụ dùng cho dự án đầu tư đủ điều kiện được khấu trừ thuế'), ], string='Nhóm HHDV', help='Nhóm hàng hóa dịch vụ')
    CHI_TIET_ID = fields.Many2one('thue.thue', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')