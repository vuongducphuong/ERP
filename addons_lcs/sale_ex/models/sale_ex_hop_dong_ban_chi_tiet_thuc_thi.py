﻿# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SALE_EX_HOP_DONG_BAN_CHI_TIET_THUC_THI(models.Model):
    _name = 'sale.ex.hop.dong.ban.chi.tiet.thuc.thi'
    _description = ''
    _inherit = ['mail.thread']
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Float(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục cp', help='Khoản mục cp')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán ', help='Hợp đồng bán ', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')