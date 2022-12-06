# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_CHUNG_TU_GHI_GIAM_CCDC_CHI_TIET(models.Model):
    _name = 'bao.cao.chung.tu.ghi.giam.ccdc.chi.tiet'
    _auto = False

    MA_CCDC = fields.Char(string='MA_CCDC') #SupplyCode

    TEN_CCDC = fields.Char(string='TEN_CCDC')#SupplyName

    TEN_DON_VI = fields.Char(string='TEN_DON_VI')#OrganizationUnitName

    SO_LUONG_GHI_GIAM = fields.Float(string='Số lượng',digits=decimal_precision.get_precision('SO_LUONG')) #DecrementQuantity
    GIA_TRI_CCDC = fields.Float(string='GIA_TRI_CCDC',digits=decimal_precision.get_precision('VND')) #Amount

    GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM = fields.Float(string='GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM',digits=decimal_precision.get_precision('VND')) #RemainingDecrementAmount

    PHIEU_THU_CHI_ID = fields.Many2one('bao.cao.chung.tu.ghi.giam.ccdc', string='Phiếu thu chi', help='Phiếu thu chi')
    
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền')
    