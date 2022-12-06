# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_PHIEU_THU_MAU_DAY_DU_CHI_TIET(models.Model):
    _name = 'bao.cao.phieu.thu.mau.day.du.chi.tiet'
    _auto = False
    

    TK_NO = fields.Char(string='TK Nợ', help='Tài khoản nợ')#DebitAccount
    TK_CO = fields.Char(string='TK Có', help='Tài khoản có')#CreditAccount
    SO_TIEN_QUY_DOI = fields.Float(string='Số tiền', help='Số tiền', digits=decimal_precision.get_precision('VND')) #Amount
    SO_TIEN = fields.Monetary(string='Số tiền nguyên tệ', help='Số tiền nguyên tệ', currency_field='currency_id')#AmountOC
    DIEN_GIAI_DETAIL = fields.Char(string='Diễn giải', help='Diễn giải') #Description
    PHIEU_THU_CHI_ID = fields.Many2one('bao.cao.phieu.thu.mau.day.du', string='Phiếu thu chi', help='Phiếu thu chi')

    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)