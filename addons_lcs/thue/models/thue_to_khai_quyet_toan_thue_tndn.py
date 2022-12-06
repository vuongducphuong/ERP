# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class THUE_TO_KHAI_QUYET_TOAN_THUE_TNDN(models.Model):
    _name = 'thue.to.khai.quyet.toan.thue.tndn'
    _description = ''
    _inherit = ['mail.thread']

    STT = fields.Char(string='STT', help='STT')
    CHI_TIEU = fields.Char(string='Chỉ tiêu', help='Chỉ tiêu')
    MA_CHI_TIEU = fields.Char(string='Mã chỉ tiêu', help='Mã chỉ tiêu')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    CHI_TIET_ID_2 = fields.Many2one('thue.thue', string='Chi tiết', help='Thuế tndn phải nộp khác ', ondelete='cascade')
    name = fields.Char(string='Name', help='Thuế tndn của hoạt động sản xuất kinh doanh', oldname='NAME')