# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_LENH_SAN_XUAT_CHI_TIET(models.Model):
	_name = 'bao.cao.lenh.san.xuat.chi.tiet'
	_auto = False

	
	MA = fields.Char(string='MA', help='InventoryItemCode')
	TEN_HANG = fields.Char(string='TEN_HANG', help='InventoryItemName')
	DON_VI_TINH = fields.Char(string='DON_VI_TINH', help='UnitName')
	SO_LUONG = fields.Float(string='SO_LUONG', help='Quantity',digits=decimal_precision.get_precision('SO_LUONG'))
	MA_DOI_TUONG_THCP = fields.Char(string='MA_DOI_TUONG_THCP', help='JobCode')
	TEN_DOI_TUONG_THCP = fields.Char(string='TEN_DOI_TUONG_THCP', help='JobName')
	
	
	PHIEU_THU_CHI_ID = fields.Many2one('bao.cao.lenh.san.xuat', string='Phiếu thu chi', help='Phiếu thu chi')
	
	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền')
	