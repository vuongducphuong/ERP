# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class THUE_NOP_THUE_CHI_TIET(models.Model):
    _name = 'thue.nop.thue.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    KHOAN_PHAI_NOP = fields.Char(string='Khoản phải nộp', help='Khoản phải nộp')
    SO_PHAI_NOP = fields.Float(string='Số phải nộp', help='Số phải nộp', digits=decimal_precision.get_precision('VND'))
    SO_NOP_LAN_NAY = fields.Float(string='Số nộp lần này', help='Số nộp lần này', digits=decimal_precision.get_precision('VND'))
    CHI_TIET_ID = fields.Many2one('thue.nop.thue.form', string='Chi tiết', help='Chi tiết')
    AUTO_SELECT = fields.Boolean()
    name = fields.Char(string='Name', help='Name', oldname='NAME')