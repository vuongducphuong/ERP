# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH_THANH_VIEN_THAM_GIA(models.Model):
    _name = 'asset.danh.gia.lai.thanh.vien.tham.gia'
    _description = ''
    _inherit = ['mail.thread']
    HO_VA_TEN = fields.Char(string='Họ và tên', help='Họ và tên')
    CHUC_DANH = fields.Char(string='Chức danh', help='Chức danh')
    DAI_DIEN = fields.Char(string='Đại diện', help='Đại diện')
    DANH_GIA_LAI_TAI_SAN_CO_DINH_ID = fields.Many2one('asset.danh.gia.lai', string='Đánh giá lại tài sản cố định', help='Đánh giá lại tài sản cố định', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')