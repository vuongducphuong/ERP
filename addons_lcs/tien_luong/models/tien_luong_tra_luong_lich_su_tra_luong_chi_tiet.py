# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_LUONG_LICH_SU_TRA_LUONG_FORM_CHI_TIET(models.Model):
    _name = 'tien.luong.lich.su.tra.luong.form.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']

    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ')
    SO_CHUNG_TU = fields.Date(string='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải')
   
    SO_PHAI_TRA = fields.Float(string='Số phải trả')
    SO_DA_TRA = fields.Float(string='Số đã trả')
    SO_CON_PHAI_TRA = fields.Float(string='Số còn phải trả')
    
    CHI_TIET_ID = fields.Many2one('tien.luong.lich.su.tra.luong.form', string='Chi tiết', help='Chi tiết')
    name = fields.Char(string='Name', oldname='NAME')
    ID_GOC = fields.Integer()
    MODEL_GOC = fields.Char ()
