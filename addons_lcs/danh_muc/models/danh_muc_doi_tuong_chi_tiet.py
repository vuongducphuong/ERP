# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_DOI_TUONG_CHI_TIET(models.Model):
    _name = 'danh.muc.doi.tuong.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    DIA_DIEM = fields.Char(string='Địa điểm', help='Địa điểm')
    SO_TAI_KHOAN = fields.Char(string='Số tài khoản', help='Số tài khoản')
    TEN_NGAN_HANG = fields.Char(string='Tên ngân hàng', help='Tên ngân hàng')
    CHI_NHANH = fields.Char(string='Chi nhánh', help='Chi nhánh')
    TINH_TP_CUA_NGAN_HANG = fields.Char(string='Tỉnh/TP của ngân hàng', help='Tỉnh tp của ngân hàng')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng', ondelete='cascade')
    name = fields.Char(string='Name', help='Name',related='SO_TAI_KHOAN', oldname='NAME')
    STT = fields.Integer(string='STT', help='STT')