# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_DIEU_CHUYEN_CCDC_CHI_TIET(models.Model):
    _name = 'bao.cao.dieu.chuyen.ccdc.chi.tiet'
    _auto = False

    MA_CCDC = fields.Char(string='MA_CCDC', help='SupplyCode')
    TEN_CCDC = fields.Char(string='TEN_CCDC', help='SupplyName')
    TU_DON_VI = fields.Char(string='TU_DON_VI', help='FromDepartmentName')
    DEN_DON_VI = fields.Char(string='DEN_DON_VI', help='ToDeparmentName')
    SO_LUONG_DANG_DUNG = fields.Float(string='SO_LUONG_DANG_DUNG', help='UseQuantity',digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_DIEU_CHUYEN = fields.Float(string='SO_LUONG_DIEU_CHUYEN', help='TransferQuantity',digits=decimal_precision.get_precision('SO_LUONG'))
    THU_TU_SAP_XEP = fields.Integer(string='THU_TU_SAP_XEP', help='SortOrder')

    PHIEU_THU_CHI_ID = fields.Many2one('bao.cao.dieu.chuyen.ccdc', string='Phiếu thu chi', help='Phiếu thu chi')
    
  

   
    
    