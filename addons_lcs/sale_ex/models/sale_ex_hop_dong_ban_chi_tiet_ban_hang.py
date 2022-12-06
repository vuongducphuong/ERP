# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SALE_EX_HOP_DONG_BAN_CHI_TIET_BAN_HANG(models.Model):
    _name = 'sale.ex.hop.dong.ban.chi.tiet.ban.hang'
    _description = ''
    _inherit = ['mail.thread']
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Float(string='Số chứng từ', help='Số chứng từ')
    SO_HOA_DON = fields.Float(string='Số hóa đơn', help='Số hóa đơn')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TONG_TIEN_THANH_TOAN = fields.Float(string='Tổng tiền thanh toán', help='Tổng tiền thanh toán')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')