# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_BAO_GIA_CHI_TIET(models.Model):
	_name = 'bao.cao.bao.gia.chi.tiet'
	_auto = False

	MA_HANG = fields.Char(string='MA_HANG', help='InventoryItemCode')
	DIEN_GIAI_DETAIL = fields.Char(string='DIEN_GIAI_DETAIL', help='Description')
	SO_LUONG = fields.Float(string='SO_LUONG', help='Quantity',digits=decimal_precision.get_precision('SO_LUONG'))
	DON_GIA = fields.Monetary(string='DON_GIA', help='UnitPrice',currency_field='currency_id')
	THANH_TIEN = fields.Monetary(string='Thành tiền',currency_field='currency_id') #AmountOC
	THANH_TIEN_QUY_DOI = fields.Float(string='THANH_TIEN_QUY_DOI', help='Amount')
	TY_LE_CHIET_KHAU = fields.Float(string='TY_LE_CHIET_KHAU', help='DiscountRate')
	TIEN_CHIET_KHAU =  fields.Monetary(string='Thành tiền',currency_field='currency_id') #DiscountAmountOC
	TIEN_CHIET_KHAU_QUY_DOI = fields.Float(string='TIEN_CHIET_KHAU_QUY_DOI', help='DiscountAmount')
	THUE_SUAT = fields.Float(string='THUE_SUAT', help='VATRate')
	TIEN_THUE_GTGT = fields.Monetary(string='Thành tiền',currency_field='currency_id') #VATAmountOC
	TIEN_THUE_GTGT_QUY_DOI = fields.Float(string='TIEN_THUE_GTGT_QUY_DOI', help='VATAmount')
	DON_VI_TINH = fields.Char(string='DON_VI_TINH', help='UnitName')
	THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='THU_TU_SAP_XEP_CHI_TIET', help='SortOrder')
	STT = fields.Integer(string='STT', help='RefIDSortOrder')

	LA_HANG_KHUYEN_MAI = fields.Boolean(string='Là hàng khuyến mãi') #IsPromotion
	
	
	PHIEU_THU_CHI_ID = fields.Many2one('bao.cao.bao.gia', string='Phiếu thu chi', help='Phiếu thu chi')
	
	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền')
	