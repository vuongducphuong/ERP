# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_UNC_TECHCOMBANK_CHI_TIET(models.Model):
    _name = 'bao.cao.uy.nhiem.chi.techcombank.chi.tiet'
    _auto = False

    THANH_TIEN_QUY_DOI = fields.Monetary(string='Thành tiền quy đổi', currency_field='currency_id')#Amount
    THANH_TIEN = fields.Monetary(string='Thành tiền', currency_field='currency_id')#AmountOC
    TK_NO = fields.Char(string='TK nợ')#DebitAccount
    TK_CO = fields.Char(string='TK có')#CreditAccount
    DIEN_GIAI_DEATAIL = fields.Char(string='Diễn giải')#Description
    PHIEU_THU_CHI_ID = fields.Many2one('bao.cao.uy.nhiem.chi.techcombank', string='Phiếu thu chi', help='Phiếu thu chi')
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh())