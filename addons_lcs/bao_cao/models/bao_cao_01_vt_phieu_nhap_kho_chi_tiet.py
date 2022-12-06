# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_01VT_NHAP_KHO_CHI_TIET(models.Model):
    _name = 'bao.cao.01vt.nhap.kho.chi.tiet'
    _auto = False
    
    NHAP_XUAT_ID = fields.Many2one('bao.cao.01vt.nhap.kho')
    MA_HANG = fields.Char(string='Mã hàng') #InventoryItemCode
    TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng')  #InventoryItemName
    
    DVT = fields.Char(string='ĐVT', help='Đơn vị tính') #UnitName
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng',digits=decimal_precision.get_precision('SO_LUONG'))#Quantity
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits=decimal_precision.get_precision('VND')) #UnitPrice
    SO_TIEN = fields.Float(string='Thành tiền', help='Thành tiền',digits=decimal_precision.get_precision('VND')) #Amount
