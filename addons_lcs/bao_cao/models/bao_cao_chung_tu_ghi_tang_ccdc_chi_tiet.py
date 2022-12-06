# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_CHUNG_TU_GHI_TANG_CCDC_CHI_TIET(models.Model):
    _name = 'bao.cao.chung.tu.ghi.tang.ccdc.chi.tiet'
    _auto = False

    NHAP_XUAT_ID = fields.Many2one('bao.cao.chung.tu.ghi.tang.ccdc')
    SO_CHUNG_TU = fields.Char(string='SO_CHUNG_TU', help='RefNo')
    NGAY_CHUNG_TU = fields.Date(string='NGAY_CHUNG_TU', help='RefDate')
    MA_CCDC = fields.Char(string='MA_CCDC', help='SupplyCode')
    TEN_CCDC = fields.Char(string='TEN_CCDC', help='SupplyName')
    LY_DO_GHI_TANG = fields.Char(string='LY_DO_GHI_TANG', help='ReasonIncrement')
    TEN_DON_VI = fields.Char(string='TEN_DON_VI', help='OrganizationUnitName')
    SO_LUONG = fields.Float(string='SO_LUONG', help='Quantity',digits= decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='DON_GIA', help='UnitPrice',digits= decimal_precision.get_precision('DON_GIA'))
    
    THANH_TIEN = fields.Monetary(string='THANH_TIEN', help='Amount',currency_field='base_currency_id')

    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh())