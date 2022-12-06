# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_KY_TINH_GIA_THANH(models.Model):
    _name = 'danh.muc.ky.tinh.gia.thanh'
    _description = ''
    _inherit = ['mail.thread']
    name = fields.Char(string='Tên kỳ tính giá thành', help='Tên kỳ tính giá thành', oldname='NAME')
    LOAI = fields.Char(string='Loại', help='Loại')