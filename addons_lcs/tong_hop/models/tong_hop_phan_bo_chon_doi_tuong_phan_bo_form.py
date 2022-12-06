# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_PHAN_BO_CHON_DOI_TUONG_PHAN_BO_FORM(models.Model):
    _name = 'tong.hop.phan.bo.chon.doi.tuong.phan.bo.form'
    _description = ''
    _auto = False

    PHAN_BO = fields.Char(string='Phân bổ', help='Phân bổ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(TONG_HOP_PHAN_BO_CHON_DOI_TUONG_PHAN_BO_FORM, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result
    TONG_HOP_PHAN_BO_CHON_DOI_TUONG_PHAN_BO_CHI_TIET_FORM_IDS = fields.One2many('tong.hop.phan.bo.chon.doi.tuong.phan.bo.chi.tiet.form', 'PHAN_BO_CHON_DOI_TUONG_PHAN_BO_ID', string='Phân bổ chọn đối tượng phân bổ chi tiết form')
    
    
    