# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_CTGS_CHON_CHUNG_TU_CHI_TIET_FORM(models.Model):
    _name = 'tong.hop.ctgs.chon.chung.tu.chi.tiet.form'
    _description = ''
    _inherit = ['mail.thread']
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk nợ', help='Tk nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk có', help='Tk có')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CHON_CHUNG_TU_ID = fields.Many2one('tong.hop.ctgs.chon.chung.tu.form', string='Chọn chứng từ', help='Chọn chứng từ')
    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')
    AUTO_SELECT = fields.Boolean()