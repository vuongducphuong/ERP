# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_UNC_PVCOMBANK_CHI_TIET(models.Model):
    _name = 'bao.cao.uy.nhiem.chi.pvc.chi.tiet'
    _auto = False

    SO_TIEN = fields.Monetary(string='Số tiền', help='Số tiền', currency_field='currency_id')
    PHIEU_THU_CHI_ID = fields.Many2one('bao.cao.uy.nhiem.chi.pvc', string='Phiếu thu chi', help='Phiếu thu chi')
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='PHIEU_THU_CHI_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)