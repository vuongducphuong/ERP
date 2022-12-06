# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class THUE_PL_017_GTGT(models.Model):
    _name = 'thue.pl.017.gtgt'
    _description = ''
    _inherit = ['mail.thread']
    STT = fields.Char(string='STT', help='STT')
    TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình')
    DOANH_THU = fields.Float(string='Doanh thu', help='Doanh thu', digits=decimal_precision.get_precision('VND'))
    
    CO_QUAN_THUE_CAP_CUC = fields.Char(string='Cơ quan thuế cấp Cục', help='Cơ quan thuế cấp Cục')
    CO_QUAN_THUE_QUAN_LY = fields.Char(string='Cơ quan thuế quản lý', help='Cơ quan thuế quản lý')
    TY_LE_PHAN_BO = fields.Float(string='Tỷ lệ phân bổ(%)', help='Tỷ lệ phân bổ(%)')
    SO_THUE_GIA_TRI_GIA_TANG_PHAI_NOP = fields.Float(string='Số thuế giá trị gia tăng phải nộp', help='Số thuế giá trị gia tăng phải nộp' , digits=decimal_precision.get_precision('VND'))
    
    CHI_TIET_ID = fields.Many2one('thue.thue', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')