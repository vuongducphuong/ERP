# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class PURCHASE_EX_PHAN_BO_CHIET_KHAU_THEO_HOA_DON(models.Model):
    _name = 'purchase.ex.phan.bo.chiet.khau.theo.hoa.don'
    _auto = False
    _description = ''
    
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền', digits=decimal_precision.get_precision('Product Price'))
    PHUONG_PHAP_PHAN_BO = fields.Selection([('THEO_SO_LUONG', 'Theo số lượng'), ('THEO_GIA_TRI', 'Theo giá trị'),], string='Phương pháp phân bổ', help='Phương pháp phân bổ',default='THEO_SO_LUONG',required=True)
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    
    