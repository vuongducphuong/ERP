# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_NHOM_HHDV(models.Model):
    _name = 'danh.muc.nhom.hhdv'
    _description = 'Danh mục nhóm HHDV mua vào/PurchasePurpose'
    _inherit = ['mail.thread']
	
    MA_NHOM_HHDV = fields.Char(string='Mã nhóm hhdv', help='Mã nhóm hhdv', required=True)#auto_num='danh_muc_nhom_hhdv_MA_NHOM_HHDV')
    TEN_NHOM_HHDV = fields.Char(string='Tên nhóm hhdv', help='Tên nhóm hhdv')
    name = fields.Char(string='Name',related="MA_NHOM_HHDV",store=True, oldname='NAME')