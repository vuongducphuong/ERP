# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_DSCT_PHAT_SINH_MA_QUY_CACH_CHI_TIET(models.Model):
    _name = 'danh.muc.dsct.phat.sinh.ma.quy.cach.chi.tiet'
    _description = ''
    _auto = False

    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU_SO_TC = fields.Char(string='Số chứng từ sổ tc', help='Số chứng từ sổ tc')
    SO_CHUNG_TU_SO_QT = fields.Char(string='Số chứng từ sổ qt', help='Số chứng từ sổ qt')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')
    CHI_NHANH = fields.Char(string='Chi nhánh', help='Chi nhánh')
    CHI_TIET_ID = fields.Many2one('danh.muc.dsct.phat.sinh.ma.quy.cach.form', string='Chi tiết', help='Chi tiết')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name', copy=True)
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(DANH_MUC_DSCT_PHAT_SINH_MA_QUY_CACH_CHI_TIET, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result