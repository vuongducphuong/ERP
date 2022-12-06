# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SALE_EX_HOP_DONG_BAN_CHON_CHUNG_TU_THU_CHI_TIET_FORM(models.Model):
    _name = 'sale.ex.hop.dong.ban.chon.chung.tu.thu.chi.tiet.form'
    _description = ''
    _inherit = ['mail.thread']

    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    AUTO_SELECT = fields.Boolean()
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Float(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    MA_DOI_TUONG_ID = fields.Many2one('res.partner', string='Mã đối tượng', help='Mã đối tượng')
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng')
    HOP_DONG_BAN_CHON_CHUNG_TUU_THU_ID = fields.Many2one('sale.ex.hop.dong.ban.chon.chung.tu.thu.form', string='Hợp đồng bán chọn chứng từu thu', help='Hợp đồng bán chọn chứng từu thu')
    name = fields.Char(string='Name', help='Name', oldname='NAME')