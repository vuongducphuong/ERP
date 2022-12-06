# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_KHOA_SO_KY_KE_TOAN_CHI_TIET(models.Model):
    _name = 'tong.hop.khoa.so.ky.ke.toan.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh')
    NGAY_KHOA_SO = fields.Date(string='Ngày khóa sổ', help='Ngày khóa sổ')
    KHOA_SO_KY_KE_TOAN = fields.Float(string='Khóa sổ kỳ kế toán', help='Khóa sổ kỳ kế toán')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    KHOA_SO_KY_KE_TOAN_ID = fields.Many2one('tong.hop.khoa.so.ky.ke.toan', string='Khóa sổ kỳ kế toán', help='Khóa sổ kỳ kế toán')