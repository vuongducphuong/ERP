# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class THUE_PL_015_GTGT(models.Model):
    _name = 'thue.pl.015.gtgt'
    _description = ''
    _inherit = ['mail.thread']
    STT = fields.Char(string='STT', help='STT')
    SO_CHUNG_TU_NOP_THUE = fields.Char(string='Số chứng từ nộp thuế', help='Số chứng từ nộp thuế')
    NGAY_NOP_THUE = fields.Date(string='Ngày nộp thuế', help='Ngày nộp thuế')
    NOI_NOP_THUE = fields.Char(string='Nơi nộp thuế (Kho bạc Nhà nước)', help='Nơi nộp thuế')
    CO_QUAN_THUE_CAP_CUC = fields.Char(string='Cơ quan thuế cấp cục', help='Cơ quan thuế cấp cục')
    CO_QUAN_THUE_QUAN_LY = fields.Char(string='Cơ quan thuế quản lý', help='Cơ quan thuế quản lý')
    SO_TIEN_THUE_DA_NOP = fields.Float(string='Số tiền thuế đã nộp', help='Số tiền thuế đã nộp',digits=decimal_precision.get_precision('VND'))

    CHI_TIET_ID = fields.Many2one('thue.thue', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')