# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SUPPLY_KIEM_KE_CCDC_TV_THAM_GIA(models.Model):
    _name = 'supply.kiem.ke.thanh.vien.tham.gia'
    _description = ''
    _inherit = ['mail.thread']
    HO_TEN = fields.Char(string='Họ tên', help='Họ tên')
    CHUC_DANH = fields.Char(string='Chức danh', help='Chức danh')
    DAI_DIEN = fields.Char(string='Đại diện', help='Đại diện')
    KIEM_KE_CCDC_ID = fields.Many2one('supply.kiem.ke', string='Kiểm kê công cụ dụng cụ', help='Kiểm kê công cụ dụng cụ', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')