# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class BAO_CAO_LOAI_CCDC(models.Model):
    _name = 'bao.cao.loai.ccdc'
    
    
    MA_CCDC = fields.Char(string='Mã ccdc', help='Mã ccdc', required=True)#, auto_num='bao_cao_loai_ccdc_MA_CCDC')
    TEN_CCDC = fields.Char(string='Tên ccdc', help='Tên ccdc')
    name = fields.Char(string='Name', help='Name', oldname='NAME')