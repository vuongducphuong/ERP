# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_DON_MUA_HANG_CHI_TIET(models.Model):
    _name = 'bao.cao.don.mua.hang.chi.tiet'
    _auto = False

    MA_HANG = fields.Char(string='TK Nợ', help='Tài khoản nợ') #InventoryItemCode
    DIEN_GIAI_DETAIL = fields.Char(string='TK Có', help='Tài khoản có') #Description
    DON_VI_TINH = fields.Char(string='TK Có', help='Tài khoản có') #UnitName
    THANH_TIEN = fields.Monetary(string='Thành tiền',currency_field='currency_id') #AmountOC
    TIEN_THUE_GTGT = fields.Monetary(string='Thành tiền',currency_field='currency_id') #VATAmountOC
    DON_GIA = fields.Monetary(string='Thành tiền',currency_field='currency_id') #UnitPrice
    PHAN_TRAM_THUE = fields.Float(string='Thành tiền quy đổi')#VATRate
    THANH_TIEN_QUY_DOI = fields.Float(string='Thành tiền quy đổi')#Amount
    SO_LUONG = fields.Float(string='Thành tiền quy đổi', digits=decimal_precision.get_precision('SO_LUONG'))#Quantity
    TY_LE_CHIET_KHAU = fields.Float(string='Thành tiền quy đổi', digits=decimal_precision.get_precision('VND'))#DiscountRate
    

    LA_HANG_KHUYEN_MAI = fields.Boolean(string='Là hàng khuyến mãi') #IsPromotion

    
    PHIEU_THU_CHI_ID = fields.Many2one('bao.cao.don.mua.hang', string='Phiếu thu chi', help='Phiếu thu chi')
    
    STT = fields.Integer(string='Số thứ tự') #RefIDSortOrder
    # THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Số thứ tự') #SortOrder
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền')
    