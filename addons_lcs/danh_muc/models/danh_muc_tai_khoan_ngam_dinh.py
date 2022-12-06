# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_TAI_KHOAN_NGAM_DINH(models.Model):
    _name = 'danh.muc.tai.khoan.ngam.dinh'
    _description = ''
    _inherit = ['mail.thread']
    LOAI_CHUNG_TU_ID = fields.Many2one('danh.muc.loai.chung.tu', string='Loại chứng từ', help='Loại chứng từ')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')
    name = fields.Char(string='Tên loại chứng từ', help='Tên loại chứng từ')
    DANH_MUC_TAI_KHOAN_NGAM_DINH_CHI_TIET_IDS = fields.One2many('danh.muc.tai.khoan.ngam.dinh.chi.tiet', 'DANH_MUC_TAI_KHOAN_NGAM_DINH_ID', string='Tài khoản ngầm định chi tiết', copy=True)