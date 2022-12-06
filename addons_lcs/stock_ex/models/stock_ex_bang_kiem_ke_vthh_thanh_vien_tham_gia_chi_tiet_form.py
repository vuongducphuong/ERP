# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class STOCK_EX_BANG_KIEM_KE_VTHH_THANH_VIEN_THAM_GIA_CHI_TIET_FORM(models.Model):
    _name = 'stock.ex.bang.kiem.ke.vthh.tv.tham.gia.chi.tiet.form'
    _description = ''
    _inherit = ['mail.thread']
    HO_VA_TEN = fields.Char(string='Họ và tên', help='Họ và tên')
    CHUC_DANH = fields.Char(string='Chức danh', help='Chức danh')
    DAI_DIEN = fields.Char(string='Đại diện', help='Đại diện')
    BANG_KIEM_KE_VTHH_ID = fields.Many2one('stock.ex.kiem.ke.bang.kiem.ke.vat.tu.hang.hoa.form', string='Bảng kiểm kê vthh ', help='Bảng kiểm kê vthh ', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    sequence = fields.Integer()