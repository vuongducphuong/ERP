# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision


class bao_cao_bien_ban_kiem_ke_vthh_can_dieu_chinh(models.Model):
    _name = 'bao.cao.bien.ban.kiem.ke.vthh.can.dieu.chinh'
    _auto = False

    ID_CHUNG_TU = fields.Integer(string='ID_CHUNG_TU')
    TEN_HANG = fields.Char(string='TEN_HANG', help='InventoryItemName')
    MA_HANG = fields.Char(string='MA_HANG', help='InventoryItemCode')
    MA_KHO_ID = fields.Integer(string='MA_KHO_ID')
    MA_KHO = fields.Char(string='MA_KHO', help='StockCode')
    TEN_KHO = fields.Char(string='TEN_KHO', help='StockName')
    DVT = fields.Char(string='DVT', help='Unit')
    SO_LUONG_SO_KE_TOAN = fields.Float(string='SO_LUONG_SO_KE_TOAN', help='QuantityOnBook',digits=decimal_precision.get_precision('SO_LUONG'))
    GIA_TRI_SO_KE_TOAN = fields.Monetary(string='GIA_TRI_SO_KE_TOAN', help='AmountOnBook', currency_field='base_currency_id')
    SO_LUONG_KIEM_KE = fields.Float(string='SO_LUONG_KIEM_KE', help='QuantityInventory', digits=decimal_precision.get_precision('SO_LUONG'))
    GIA_TRI_KIEM_KE = fields.Monetary(string='GIA_TRI_KIEM_KE', help='AmountInventory', currency_field='base_currency_id')
    SO_LUONG_CHENH_LECH = fields.Float(string='SO_LUONG_CHENH_LECH', help='DefferenceQuantity', digits=decimal_precision.get_precision('SO_LUONG'))
    GIA_TRI_CHENH_LECH = fields.Monetary(string='GIA_TRI_CHENH_LECH', help='DefferenceAmount', currency_field='base_currency_id')
    PHAM_CHAT_CON_TOT = fields.Float(string='PHAM_CHAT_CON_TOT', help='GoodQuantity')
    KEM_PHAM_CHAT = fields.Float(string='KEM_PHAM_CHAT', help='PoorQuantity')
    MAT_PHAM_CHAT = fields.Float(string='MAT_PHAM_CHAT', help='DateriorateQuantity')
    SortOrderMaster = fields.Integer(string='SortOrderMaster', help='SortOrderMaster')
    SortOrder = fields.Integer(string='SortOrder', help='SortOrder')
    TONG_SL_SO_KE_TOAN = fields.Float(string='TONG_SL_SO_KE_TOAN', help='TotalQuantityOnBookByStock')
    TONG_GIA_TRI_SO_KE_TOAN = fields.Float(string='TONG_GIA_TRI_SO_KE_TOAN', help='TotalAmountOnBookByStock')
    TONG_SL_KIEM_KE = fields.Float(string='TONG_SL_KIEM_KE', help='TotalQuantityAuditByStock')
    TONG_GIA_TRI_KIEM_KE = fields.Float(string='TONG_GIA_TRI_KIEM_KE', help='TotalAmountAuditByStock')
    TONG_SL_CHENH_LECH = fields.Float(string='TONG_SL_CHENH_LECH', help='TotalDiffQuantityByStock')
    TONG_GIA_TRI_CHENH_LECH = fields.Float(string='TONG_GIA_TRI_CHENH_LECH', help='TotalDiffAmountByStock')

    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)

    BIEN_BAN_KIEM_KE_ID = fields.Many2one('bao.cao.bien.ban.kiem.ke')
    BIEN_BAN_KIEM_KE_GROUP_ID = fields.Many2one('bao.cao.bien.ban.kiem.ke.group')