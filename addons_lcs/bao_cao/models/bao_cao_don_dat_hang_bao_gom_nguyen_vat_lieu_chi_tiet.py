# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_DON_DAT_HANG_BAO_GOM_NGUYEN_VAT_LIEU_CHI_TIET(models.Model):
    _name = 'bao.cao.don.dat.hang.bao.gom.nvl.chi.tiet'
    _auto = False

    TEN_THANH_PHAM = fields.Char(string='TK Nợ', help='Tài khoản nợ') #InventoryItemCode
    TEN_NGUYEN_VAT_LIEU = fields.Char(string='TK Có', help='Tài khoản có') #Description
    DVT_NGUYEN_VAT_LIEU = fields.Char(string='TK Có', help='Tài khoản có') #UnitName
    
    SO_LUONG_DAT = fields.Float(string='Thành tiền quy đổi', digits=decimal_precision.get_precision('SO_LUONG'))#Quantity
    DINH_MUC_NVL_1_MON = fields.Float(string='Thành tiền quy đổi')#DiscountRate
    TONG_KHOI_LUONG_NVL = fields.Float(string='Thành tiền quy đổi')#DiscountRate
    
    PHIEU_THU_CHI_ID = fields.Many2one('bao.cao.don.dat.hang.bao.gom.nvl', string='Phiếu thu chi', help='Phiếu thu chi')
    
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền')
    ROWSPAN = fields.Integer(string='rowspan')


   
    
    