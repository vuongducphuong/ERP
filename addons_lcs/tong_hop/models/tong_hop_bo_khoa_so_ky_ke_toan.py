# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_BO_KHOA_SO_KY_KE_TOAN(models.Model):
    _name = 'tong.hop.bo.khoa.so.ky.ke.toan'
    _description = ''
    _auto = False

    NGAY_KHOA_SO_HIEN_THOI = fields.Date(string='Ngày khóa sổ hiện thời', help='Ngày khóa sổ hiện thời')
    DAT_NGAY_KHOA_SO_VE_NGAY = fields.Date(string='Đặt ngày khóa sổ về ngày', help='Đặt ngày khóa sổ về ngày')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(TONG_HOP_BO_KHOA_SO_KY_KE_TOAN, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result