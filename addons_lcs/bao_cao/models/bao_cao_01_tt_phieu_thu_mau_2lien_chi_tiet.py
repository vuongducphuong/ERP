# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_01TT_PHIEU_THU_MAU_2LIEN_CHI_TIET(models.Model):
    _name = 'bao.cao.01tt.phieu.thu.mau.2lien.chi.tiet'
    _auto = False

    SO_TIEN = fields.Monetary(string='Số tiền', help='Số tiền', currency_field='currency_id') #Amount
    THANH_TIEN = fields.Monetary(string='Số tiền nguyên tệ', help='Số tiền nguyên tệ', currency_field='currency_id')#AmountOC
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)

    PHIEU_THU_CHI_ID = fields.Many2one('bao.cao.01tt.phieu.thu.mau.2lien', string='Phiếu thu chi', help='Phiếu thu chi')

