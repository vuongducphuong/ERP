# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_DANH_LAI_SO_CHUNG_TU_CHI_TIET(models.Model):
    _name = 'tien.ich.danh.lai.so.chung.tu.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    SO_CHUNG_TU_MOI = fields.Char(string='Số chứng từ mới', help='Số chứng từ mới')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    DANH_LAI_SO_CHUNG_TU_ID = fields.Many2one('tien.ich.danh.lai.so.chung.tu', string='Đánh lại số chứng từ', help='Đánh lại số chứng từ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    ID_GOC = fields.Char(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')
    ID_AND_MODEL = fields.Char(string='ghép id và model gốc', help='ghép id và model gốc')
    REF_TYPE = fields.Integer(string='ref type', help='ref type')