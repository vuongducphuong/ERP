# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_CHUNG_TU_GHI_TANG_TSCD_DCPTKT(models.Model):
    _name = 'bao.cao.chung.tu.ghi.tang.tscd.dcptkt'
    _auto = False


    TEN_QUY_CACH_DUNG_CU_PHU_TUNG = fields.Char(string='Tên quy cách dụng cụ phụ tùng') #Description

    DON_VI_TINH = fields.Char(string='Đơn vị tính')#Unit

    SO_LUONG = fields.Float(string='Số lượng') #Quantity
    GIA_TRI = fields.Float(string='Giá trị') #Amount

    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp') #SortOrder

    PHIEU_THU_CHI_ID = fields.Many2one('bao.cao.chung.tu.ghi.tang.tscd', string='Phiếu thu chi', help='Phiếu thu chi')
   
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền')
    