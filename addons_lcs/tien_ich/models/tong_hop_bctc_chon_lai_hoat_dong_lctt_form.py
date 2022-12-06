# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_BCTC_CHON_LAI_HOAT_DONG_LCTT_FORM(models.Model):
    _name = 'tong.hop.bctc.chon.lai.hoat.dong.lctt.form'
    _description = ''
    _auto = False

    CHON_HOAT_DONG_LCTT_AP_CHO_TAT_CA_CAC_CHUNG_TU = fields.Selection([('HOAT_DONG_KINH_DOANH', 'Hoạt động kinh doanh'), ('HOAT_DONG_DAU_TU', ' Hoạt động đầu tư'), ('HOAT_DONG_TAI_CHINH', ' Hoạt động tài chính'), ], string='Chọn hoạt động LCTT áp cho tất cả các chứng từ', help='Chọn hoạt động LCTT áp cho tất cả các chứng từ',default='HOAT_DONG_KINH_DOANH',required=True)
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(TONG_HOP_BCTC_CHON_LAI_HOAT_DONG_LCTT_FORM, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result
    TONG_HOP_BCTC_CHON_LAI_HOAT_DONG_LCTT_CHI_TIET_FORM_IDS = fields.One2many('tong.hop.bctc.chon.lai.hoat.dong.lctt.chi.tiet.form', 'BCTC_CHON_LAI_HOAT_DONG_LCTT_ID', string='BCTT chọn lại hoạt động LCTT chi tiết form')