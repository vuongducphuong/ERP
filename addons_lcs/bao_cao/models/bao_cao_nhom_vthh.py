# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class BAO_CAO_NHOM_VTHH(models.Model):
    _name = 'bao.cao.nhom.vthh'
    
    
    MA_NHOM = fields.Char(string='Mã nhóm', help='Mã nhóm', required=True)#, auto_num='bao_cao_nhom_vthh_MA_NHOM')
    TEN_NHOM = fields.Char(string='Tên nhóm', help='Tên nhóm')
    name = fields.Char(string='Name', help='Name', oldname='NAME')