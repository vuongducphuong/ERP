# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class THUE_TAI_LIEU_KEM_THEO(models.Model):
    _name = 'thue.tai.lieu.kem.theo'
    _description = ''
    _inherit = ['mail.thread']
    STT = fields.Char(string='STT', help='STT')
    TEN_TAI_LIEU = fields.Char(string='Tên tài liệu', help='Tên tài liệu')
    
    CHI_TIET_ID = fields.Many2one('thue.thue', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')