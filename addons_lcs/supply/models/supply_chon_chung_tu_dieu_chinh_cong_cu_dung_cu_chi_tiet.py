# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class SUPPLY_CHON_CHUNG_TU_DIEU_CHINH_CONG_CU_DUNG_CU_CHI_TIET(models.Model):
    _name = 'supply.chon.chung.tu.dieu.chinh.cong.cu.dung.cu.chi.tiet'
    _auto = False
    _description = ''
    
    NGAY_HACH_TOAN = fields.Char(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Char(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền' ,digits= decimal_precision.get_precision('Product Price'))
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    CHON_CHUNG_TU_ID = fields.Many2one('supply.chon.chung.tu.dieu.chinh.ccdc.form', string='Chọn chứng từ', help='Chọn chứng từ')