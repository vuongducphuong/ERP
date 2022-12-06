# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_HOP_DONG_BAN(models.Model):
    _name = 'sale.ex.hop.dong.ban'
    _description = 'Hợp đồng bán'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', help='Name')
    DOI_TUONG_ID = fields.Many2one('res.partner', domain=[('LA_KHACH_HANG', '=', True)], string='Khách hàng', help='Khách hàng')