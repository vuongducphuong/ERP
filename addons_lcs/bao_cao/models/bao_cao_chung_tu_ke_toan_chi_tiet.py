# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class BAO_CAO_CHUNG_TU_KE_TOAN_CHI_TIET(models.Model):
    _name = 'bao.cao.chung.tu.ke.toan.chi.tiet'
    _auto = False
    
    CHUNG_TU_ID = fields.Many2one('bao.cao.chung.tu.ke.toan')

    TK_NO = fields.Char(string='TK Nợ', help='Tài khoản nợ')#DebitAccount
    TK_CO = fields.Char(string='TK Có', help='Tài khoản có')#CreditAccount
    THANH_TIEN_QUY_DOI = fields.Monetary(string='Số tiền', help='Số tiền', currency_field='currency_id') #Amount
    THANH_TIEN = fields.Monetary(string='Số tiền nguyên tệ', help='Số tiền nguyên tệ', currency_field='currency_id')#AmountOC
    DIEN_GIAI_DETAIL = fields.Char(string='Diễn giải', help='Diễn giải') #DESCRIPTION
    rownumber  = fields.Integer(string='Thứ tự sắp xếp')#rownumber
    RowOrder  = fields.Integer(string='Thứ tự sắp xếp')#RowOrder
    
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền')


