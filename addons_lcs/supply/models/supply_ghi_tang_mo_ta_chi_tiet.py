# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SUPPLY_GHI_TANG_MO_TA_CHI_TIET(models.Model):
    _name = 'supply.ghi.tang.mo.ta.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MO_TA = fields.Char(string='Mô tả', help='Mô tả')
    SO_HIEU = fields.Char(string='Số hiệu', help='Số hiệu')
    GHI_TANG_MO_TA_CHI_TIET_ID = fields.Many2one('supply.ghi.tang', string='Ghi tăng mô tả chi tiết', help='Ghi tăng mô tả chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')