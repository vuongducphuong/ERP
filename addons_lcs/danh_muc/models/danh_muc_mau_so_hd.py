# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_MAU_SO_HD(models.Model):
    _name = 'danh.muc.mau.so.hd'
    _description = ''
    _inherit = ['mail.thread']
    MAU_SO_HD = fields.Char(string='Mẫu số HĐ', help='Mẫu số hđ')
    TEN_MAU_SO_HD = fields.Char(string='Tên mẫu số HĐ', help='Tên mẫu số hđ')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi')
    name = fields.Char(string='Name', help='Name',related="MAU_SO_HD",store=True, oldname='NAME')