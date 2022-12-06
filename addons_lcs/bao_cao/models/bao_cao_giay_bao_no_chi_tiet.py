# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_GIAY_BAO_NO_CHI_TIET(models.Model):
    _name = 'bao.cao.giay.bao.no.chi.tiet'
    _auto = False

    TK_NO = fields.Char(string='TK Nợ', help='Tài khoản nợ') #DebitAccount
    TK_CO = fields.Char(string='TK Có', help='Tài khoản có') #CreditAccount
    THANH_TIEN = fields.Monetary(string='Thành tiền',currency_field='currency_id') #AmountOC
    THANH_TIEN_QUY_DOI = fields.Float(string='Thành tiền quy đổi', digits=decimal_precision.get_precision('VND'))#Amount
    PHIEU_THU_CHI_ID = fields.Many2one('bao.cao.giay.bao.no', string='Phiếu thu chi', help='Phiếu thu chi')
    DIEN_GIAI_DETAIL = fields.Char(string='Diễn giải', help='Diễn giải') #Description
    STT = fields.Integer(string='Số thứ tự') #SortOrder
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền')
    