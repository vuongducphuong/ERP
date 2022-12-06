# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class ACCOUNT_EX_DOI_CHIEU_NGAN_HANG_CHUNG_TU_THU_TIEN(models.Model):
    _name = 'account.ex.doi.chieu.ngan.hang.chung.tu.thu.tien'
    _description = ''
    _auto = False

    NGAY = fields.Date(string='Ngày', help='Ngày')
    SO = fields.Char(string='Số ', help='Số ')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    DOI_TUONG = fields.Char(string='Đối tượng', help='Đối tượng')
    CHUNG_TU_THU_TIEN_CHI_TIET_ID = fields.Many2one('account.ex.doi.chieu.ngan.hang', string='Chứng từ thu tiền chi tiết', help='Chứng từ thu tiền chi tiết')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(ACCOUNT_EX_DOI_CHIEU_NGAN_HANG_CHUNG_TU_THU_TIEN, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result