# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class bao_cao_bang_tinh_khau_hao_tscd_chi_tiet(models.Model):
    _name = 'bao.cao.bang.tinh.khau.hao.tscd.chi.tiet'
    _auto = False
    
    NHAP_XUAT_ID = fields.Many2one('bao.cao.bang.tinh.khau.hao.tscd')
    MA_TAI_SAN = fields.Char(string='MA_TAI_SAN', help='FixedAssetCode')
    TEN_TAI_SAN = fields.Char(string='TEN_TAI_SAN', help='FixedAssetName')
    TEN_DON_VI = fields.Char(string='TEN_DON_VI', help='OrganizationUnitName')
    GIA_TRI_TINH_KHAU_HAO = fields.Monetary(string='GIA_TRI_TINH_KHAU_HAO', help='TotalDepreciationAmount',currency_field='base_currency_id')
    GIA_TRI_KH_THANG = fields.Monetary(string='GIA_TRI_KH_THANG', help='MonthlyDepreciationAmount',currency_field='base_currency_id')
    HAO_MON_LUY_KE = fields.Monetary(string='HAO_MON_LUY_KE', help='AccumDepreciationAmount',currency_field='base_currency_id')
    GIA_TRI_CON_LAI = fields.Monetary(string='GIA_TRI_CON_LAI', help='RemainAmount',currency_field='base_currency_id')
    SortOrder = fields.Integer(string='SortOrder', help='SortOrder')

    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh())

