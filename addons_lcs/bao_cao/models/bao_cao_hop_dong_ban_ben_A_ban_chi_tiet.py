# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_HOP_DONG_BAN_CHI_TIET(models.Model):
    _name = 'bao.cao.hop.dong.ban.chi.tiet'
    _auto = False

    ID_CHUNG_TU = fields.Integer() #SortOrder
    MA = fields.Char(string='TK Nợ', help='Tài khoản nợ') #InventoryItemCode
    TEN_HANG = fields.Char(string='TK Có', help='Tài khoản có') #InventoryItemName
    SO_LUONG_YEU_CAU = fields.Float(string='Thành tiền quy đổi', digits=decimal_precision.get_precision('SO_LUONG'))#Quantity
    SO_LUONG_DA_GIAO = fields.Float(string='Thành tiền quy đổi', digits=decimal_precision.get_precision('SO_LUONG'))#QuantityDelivered
    SO_LUONG_DA_GIAO_NAM_TRUOC = fields.Float(string='Thành tiền quy đổi', digits=decimal_precision.get_precision('SO_LUONG'))#QuantityDeliveredLastYear
    DON_GIA = fields.Float(string='Thành tiền',digits=decimal_precision.get_precision('VND')) #UnitPriceOC
    DON_GIA_QUY_DOI = fields.Float(string='Thành tiền',digits=decimal_precision.get_precision('VND')) #UnitPrice
    THANH_TIEN = fields.Float(string='Thành tiền',digits=decimal_precision.get_precision('VND')) #AmountOC
    THANH_TIEN_QUY_DOI = fields.Float(string='Thành tiền',digits=decimal_precision.get_precision('VND')) #Amount
    TY_LE_CK = fields.Float(string='Thành tiền quy đổi', digits=decimal_precision.get_precision('VND'))#DiscountRate
    TIEN_CHIET_KHAU = fields.Float(string='Thành tiền quy đổi', digits=decimal_precision.get_precision('VND'))#DiscountAmountOC
    TIEN_CHIET_KHAU_QUY_DOI = fields.Float(string='Thành tiền quy đổi', digits=decimal_precision.get_precision('VND'))#DiscountAmount
    PHAN_TRAM_THUE_GTGT = fields.Float(string='Thành tiền quy đổi',digits=decimal_precision.get_precision('VND'))#VATRate
    TIEN_THUE_GTGT = fields.Float(string='Thành tiền',digits=decimal_precision.get_precision('VND')) #VATAmountOC
    TIEN_THUE_GTGT_QUY_DOI = fields.Float(string='Thành tiền',digits=decimal_precision.get_precision('VND')) #VATAmount
    DVT = fields.Char(string='TK Có', help='Tài khoản có') #Unit
    DVT_CHINH_DVC = fields.Char(string='TK Có', help='Tài khoản có') #MainUnit
    STT = fields.Integer(string='Số thứ tự') #SortOrder
    
    
    PHIEU_THU_CHI_ID = fields.Many2one('bao.cao.hop.dong.ban', string='Phiếu thu chi', help='Phiếu thu chi')
    
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền')
    