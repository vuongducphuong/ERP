# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_KIEM_TRA_CONG_THUC_THIET_LAP_TRUNG_LAP(models.Model):
    _name = 'tien.ich.kiem.tra.cong.thuc.thiet.lap.trung.lap'
    _description = ''
    _auto = False

    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(TIEN_ICH_KIEM_TRA_CONG_THUC_THIET_LAP_TRUNG_LAP, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result
    TIEN_ICH_KIEM_TRA_CONG_THUC_BI_THIET_LAP_TRUNG_LAP_CHI_TIET_IDS = fields.One2many('tien.ich.kiem.tra.cong.thuc.bi.thiet.lap.trung.lap.chi.tiet', 'CHI_TIET_ID', string='Kiểm tra công thức bị thiết lập trùng lặp chi tiết')