# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class BAO_CAO_PHIEU_XUAT_KHO_02VT_MAU_A5_CHI_TIET(models.Model):
    _name = 'bao.cao.phieu.xuat.kho.02vt.mau.a5.chi.tiet'
    _auto = False
    
    CHUNG_TU_TRA_LAI_HANG_MUA_ID = fields.Many2one('bao.cao.phieu.xuat.kho.02vt.mau.a5')
    MA_HANG =  fields.Char(string='Mã hàng')
    TEN_HANG =  fields.Char(string='Tên hàng')
    DVT =  fields.Char(string='Đơn vị tính')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng',digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá', digits=decimal_precision.get_precision('VND'))
    SO_TIEN =  fields.Float(string='Số tiền', digits=decimal_precision.get_precision('VND'))
