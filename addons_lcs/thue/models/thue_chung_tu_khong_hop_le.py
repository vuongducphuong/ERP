# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class THUE_CHUNG_TU_KHONG_HOP_LE(models.Model):
    _name = 'thue.chung.tu.khong.hop.le'
    _description = ''
    _auto = False

    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(THUE_CHUNG_TU_KHONG_HOP_LE, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result
    THUE_CHUNG_TU_KHONG_HOP_LE_CHI_TIET_IDS = fields.One2many('thue.chung.tu.khong.hop.le.chi.tiet', 'CHI_TIET_ID', string='Chứng từ không hợp lệ chi tiết')