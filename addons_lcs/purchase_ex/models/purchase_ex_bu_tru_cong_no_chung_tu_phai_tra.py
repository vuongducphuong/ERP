﻿# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class PURCHASE_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA(models.Model):
    _name = 'purchase.bu.tru.cong.no.chung.tu.phai.tra'
    _description = ''
    _auto = False

    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chừng từ', help='Số chừng từ')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    HAN_THANH_TOAN = fields.Date(string='Hạn thanh toán', help='Hạn thanh toán')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('Product Price'))
    SO_CON_NO = fields.Float(string='Số còn nợ', help='Số còn nợ',digits=decimal_precision.get_precision('Product Price'))
    SO_TIEN_BU_TRU = fields.Float(string='Số tiền bù trừ', help='Số tiền bù trừ',digits=decimal_precision.get_precision('Product Price'))
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    BU_TRU_CONG_NO_ID = fields.Many2one('purchase.ex.bu.tru.cong.no', string='Bù trừ công nợ', help='Bù trừ công nợ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CHON = fields.Boolean(string='Chọn', help='Chọn')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(PURCHASE_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result

    @api.onchange('CHON')
    def update_CHON(self):
        if self.SO_TIEN_BU_TRU == 0:
            if self.CHON == True:
                self.SO_TIEN_BU_TRU = self.SO_CON_NO
        if self.SO_TIEN_BU_TRU != 0:
            if self.CHON == False:
                self.SO_TIEN_BU_TRU = 0
    @api.onchange('SO_TIEN_BU_TRU')
    def update_SO_TIEN_BU_TRU(self):
        if self.SO_TIEN_BU_TRU != 0:
            self.CHON = True
        elif self.SO_TIEN_BU_TRU == 0:
            self.CHON = False


