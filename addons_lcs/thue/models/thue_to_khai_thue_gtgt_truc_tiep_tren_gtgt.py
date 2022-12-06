# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class THUE_TO_KHAI_THUE_GTGT_TRUC_TIEP_TREN_GTGT(models.Model):
    _name = 'thue.to.khai.thue.gtgt.truc.tiep.tren.gtgt'
    _description = ''
    _inherit = ['mail.thread']
    STT = fields.Char(string='STT', help='STT')
    CHI_TIEU = fields.Char(string='Chỉ tiêu', help='Chỉ tiêu')
    MA_CHI_TIEU = fields.Char(string='Mã chỉ tiêu', help='Mã chỉ tiêu')
    GIA_TRI = fields.Float(string='Giá trị', help='Giá trị', digits=decimal_precision.get_precision('VND'))
    
    CHI_TIET_ID_1 = fields.Many2one('thue.thue', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')