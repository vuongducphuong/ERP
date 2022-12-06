# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_DANH_SACH_KET_CHUYEN_CHI_PHI(models.Model):
    _name = 'gia.thanh.danh.sach.ket.chuyen.chi.phi'
    _description = ''
    _auto = False

    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(GIA_THANH_DANH_SACH_KET_CHUYEN_CHI_PHI, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result
    GIA_THANH_DANH_SACH_KET_CHUYEN_CHI_PHI_CHI_TIET_IDS = fields.One2many('gia.thanh.danh.sach.ket.chuyen.chi.phi.chi.tiet', 'CHI_TIET_ID', string='Danh sách kết chuyển chi phí chi tiết')