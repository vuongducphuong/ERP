# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_LENH_THAO_DO_CHI_TIET(models.Model):
	_name = 'bao.cao.lenh.thao.do.chi.tiet'
	_auto = False

	
	MA_HANG_DETAIL = fields.Char(string='MA_HANG_DETAIL', help='InventoryItemCodeDetail')
	TEN_HANG_DETAL = fields.Char(string='TEN_HANG_DETAL', help='InventoryItemNameDetail')
	DVT_DETAIL = fields.Char(string='DVT_DETAIL', help='UnitNameDetail')
	SO_LUONG_DEATAIL = fields.Float(string='SO_LUONG_DEATAIL', help='QuantityDetail',digits=decimal_precision.get_precision('SO_LUONG'))
	
	
	PHIEU_THU_CHI_ID = fields.Many2one('bao.cao.lenh.thao.do', string='Phiếu thu chi', help='Phiếu thu chi')
	
	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền')
	