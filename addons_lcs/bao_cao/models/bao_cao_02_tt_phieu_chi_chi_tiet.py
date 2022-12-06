# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_02TT_PHIEU_CHI_CHI_TIET(models.Model):
    _name = 'bao.cao.02tt.phieu.chi.chi.tiet'
    _auto = False

    THANH_TIEN_QUY_DOI = fields.Monetary(string='Thành tiền quy đổi', help='Thành tiền quy đổi', currency_field='currency_id') #Amount
    THANH_TIEN = fields.Monetary(string='Thành tiền', help='Thành tiền', currency_field='currency_id')#AmountOC
    DIEN_GIAI_DETAIL = fields.Char(string='Diễn giải', help='Diễn giải')#Description
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)
    PHIEU_THU_CHI_ID = fields.Many2one('bao.cao.02tt.phieu.chi', string='Phiếu thu chi', help='Phiếu thu chi')