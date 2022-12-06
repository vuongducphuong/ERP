# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_PHIEU_XUAT_KHO_BAN_HANG_CHI_TIET(models.Model):
	_name = 'bao.cao.phieu.xuat.kho.ban.hang.chi.tiet'
	_auto = False

	DIEN_GIAI_DETAIL = fields.Char(string='Diễn giải', help='Diễn giải') #Description

	MA_HANG = fields.Char(string='Mã hàng') #InventoryItemCode
	
	DVT = fields.Char(string='Đơn vị tính') #UnitName
	SO_LUONG = fields.Float(string='Số lượng',digits= decimal_precision.get_precision('SO_LUONG')) #Quantity
	DON_GIA = fields.Monetary(string='Đơn giá',currency_field='currency_id') #UnitPrice
	THANH_TIEN = fields.Monetary(string='Thành tiền',currency_field='currency_id') #AmountOC
	THANH_TIEN_QUY_DOI = fields.Float(string='Thành tiền quy đổi', digits=decimal_precision.get_precision('VND'))#Amount

	TY_LE_CHIET_KHAU = fields.Float(string='Tỷ lệ chiết khấu') #DiscountRate
	TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu',currency_field='currency_id') #DiscountAmountOC_1
	TIEN_CHIET_KHAU_QUY_DOI = fields.Float(string='Tiền chiết khấu quy đổi', digits=decimal_precision.get_precision('VND'))#DiscountAmount
	TK_CHIET_KHAU = fields.Char(string='TK chiết khấu') #DiscountAccount

	THUE_SUAT = fields.Float(string='Thuế suất') #VATRate_1
	TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế gtgt',currency_field='currency_id') #VATAmountOC
	TIEN_THUE_GTGT_QUY_DOI = fields.Float(string='Tiền thuế gtgt quy đổi', digits=decimal_precision.get_precision('VND'))#VATAmount
	TK_THUE_GTGT = fields.Char(string='TK thuế gtgt') #VATAccount
	LA_HANG_KHUYEN_MAI = fields.Integer(string='Là hàng khuyến mãi') #IsPromotion

	PHIEU_THU_CHI_ID = fields.Many2one('bao.cao.phieu.xuat.kho.ban.hang', string='Phiếu thu chi', help='Phiếu thu chi')
	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền')
	