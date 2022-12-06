# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class THUE_032A_TNDN(models.Model):
    _name = 'thue.032a.tndn'
    _description = ''
    _inherit = ['mail.thread']
    STT = fields.Char(string='STT', help='STT')
    NAM_PHAT_SINH_LO = fields.Char(string='Năm phát sinh lỗ', help='Năm phát sinh lỗ')
    SO_LO_PHAT_SINH = fields.Float(string='Số lỗ phát sinh', help='Số lỗ phát sinh' , digits=decimal_precision.get_precision('VND'))
    SO_LO_DA_CHUYEN_TRONG_CAC_KY_TINH_THUE_TRUOC = fields.Float(string='Số lỗ đã chuyển trong các kỳ tính thuế trước', help='Số lỗ đã chuyển trong các kỳ tính thuế trước', digits=decimal_precision.get_precision('VND'))
    SO_LO_DUOC_CHUYEN_TRONG_KY_TINH_THUE_NAY = fields.Float(string='Số lỗ được chuyển trong kỳ tính thuế này', help='Số lỗ được chuyển trong kỳ tính thuế này', digits=decimal_precision.get_precision('VND'))
    SO_LO_CON_DUOC_CHUYEN_CHUYEN_SANG_KY_TINH_THUE_SAU = fields.Float(string='Số lỗ còn được chuyển sang các kỳ tính thuế sau', help='Số lỗ còn được chuyển sang các kỳ tính thuế sau', digits=decimal_precision.get_precision('VND'))
    

    CHI_TIET_ID = fields.Many2one('thue.thue', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')