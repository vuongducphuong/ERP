# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class ASSET_KIEM_KE_TAI_SAN_CO_DINH_THANH_VIEN_THAM_GIA(models.Model):
    _name = 'asset.kiem.ke.thanh.vien.tham.gia'
    _description = ''
    _inherit = ['mail.thread']
    HO_TEN = fields.Char(string='Họ tên', help='Họ tên')
    CHUC_DANH = fields.Char(string='Chức danh', help='Chức danh')
    DAI_DIEN = fields.Char(string='Đại diện', help='Đại diện')
    KIEM_KE_TAI_SAN_CO_DINH_ID = fields.Many2one('asset.kiem.ke', string='Kiểm kê tài sản cố định', help='Kiểm kê tài sản cố định', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')