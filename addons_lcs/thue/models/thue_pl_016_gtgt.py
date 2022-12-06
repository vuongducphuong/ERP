# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class THUE_PL_016_GTGT(models.Model):
    _name = 'thue.pl.016.gtgt'
    _description = ''
    _inherit = ['mail.thread']
    STT = fields.Char(string='STT', help='STT')
    TEN_CO_SO_SX_TRUC_THUOC = fields.Char(string='Tên cơ sở sản xuất trực thuộc', help='Tên cơ sở sản xuất trực thuộc')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    
    CO_QUAN_THUE_CAP_CUC = fields.Char(string='Cơ quan thuế cấp Cục', help='Cơ quan thuế cấp Cục')
    CO_QUAN_THUE_TRUC_TIEP_QUAN_LY = fields.Char(string='Cơ quan thuế trực tiếp quản lý', help='Cơ quan thuế trực tiếp quản lý')
    HANG_HOA_CHIU_THUE_5_PT = fields.Float(string='Hàng hóa chịu thuế suất 5%', help='Hàng hóa chịu thuế suất 5%', digits=decimal_precision.get_precision('VND'))
    HANG_HOA_CHIU_THUE_10_PT = fields.Float(string='Hàng hóa chịu thuế suất 10%', help='Hàng hóa chịu thuế suất 10%' , digits=decimal_precision.get_precision('VND'))
    TONG = fields.Float(string='Tổng', help='Tổng' , digits=decimal_precision.get_precision('VND'))

    SO_THUE_PHAI_NOP_CHO_DIA_PHUONG = fields.Float(string='Số thuế phải nộp cho từng địa phương nơi có cơ sở sản xuất trực thuộc', help='Số thuế phải nộp cho từng địa phương nơi có cơ sở sản xuất trực thuộc', digits=decimal_precision.get_precision('VND'))
    SO_THUE_PHAI_NOP_CHO_DIA_PHUONG_TH_O616 = fields.Float(string='Số thuế phải nộp cho từng địa phương nơi có cơ sở sản xuất trực thuộc trong trường hợp [06] < [16]', help='Số thuế phải nộp cho từng địa phương nơi có cơ sở sản xuất trực thuộc trong trường hợp [06] < [16]', digits=decimal_precision.get_precision('VND'))

    CHI_TIET_ID = fields.Many2one('thue.thue', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')