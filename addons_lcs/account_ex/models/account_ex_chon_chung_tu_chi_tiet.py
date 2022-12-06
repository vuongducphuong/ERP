# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class ASSET_CHON_CHUNG_TU_TSCD_CHI_TIET(models.Model):
    _name = 'account.ex.chon.chung.tu.chi.tiet'
    _auto = False
    _description = ''
    
    NGAY_HACH_TOAN = fields.Char(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Char(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK nợ', help='Tài khoản nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK có', help='Tài khoản có')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits= decimal_precision.get_precision('Product Price'))
    CHON_CHUNG_TU_ID = fields.Many2one('account.ex.chon.chung.tu.form', string='Chọn chứng từ', help='Chọn chứng từ')
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    ID_GOC = fields.Integer()
    MODEL_GOC = fields.Char ()
    CHON = fields.Boolean(string='Chọn', help='Chọn')

    AUTO_SELECT = fields.Boolean()