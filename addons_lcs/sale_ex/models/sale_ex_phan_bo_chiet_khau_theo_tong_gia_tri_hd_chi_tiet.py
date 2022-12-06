# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET(models.Model):
    _name = 'sale.ex.phan.bo.chiet.khau.theo.tong.gia.tri.hd.chi.tiet'
    _auto = False
    _description = ''

    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng')
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
    HANG_KHUYEN_MAI = fields.Boolean(string='Hàng khuyến mãi', help='Hàng khuyến mãi')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    THANH_TIEN = fields.Monetary(string='Thành tiền', help='Thành tiền', currency_field='currency_id')
    TY_LE_PHAN_BO = fields.Float(string='Tỷ lệ phân bổ', help='Tỷ lệ phân bổ')
    TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu', currency_field='currency_id') 
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_ID = fields.Many2one('sale.ex.phan.bo.chiet.khau.theo.tong.gia.tri.hd.form', string='Phân bổ chiết khấu theo tổng giá trị hóa đơn', help='Phân bổ chiết khấu theo tổng giá trị hóa đơn')
    ID_CHI_TIET = fields.Integer()
    sequence = fields.Integer()
    INDEX = fields.Integer(store=False, )
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',store=False)