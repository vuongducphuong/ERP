# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_THANH_PHAM(models.Model):
    _name = 'danh.muc.thanh.pham'
    _description = ''
    _inherit = ['mail.thread']
    name = fields.Char(string='Tên thành phẩm', help='Tên thành phẩm', oldname='NAME')
    MA_DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Mã đối tượng thcp', help='Mã đối tượng thcp')
    TEN_DOI_TUONG_THCP = fields.Char(string='Tên đối tượng thcp', help='Tên đối tượng thcp')