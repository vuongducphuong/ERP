# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class THUE_PHU_LUC_KE_KHAI(models.Model):
    _name = 'thue.phu.luc.ke.khai'
    _description = ''
    _inherit = ['mail.thread']
    MA_PHU_LUC = fields.Char(string='Mã phụ lục', help='Mã phụ lục')
    TEN_PHU_LUC = fields.Char(string='Tên phụ lục', help='Tên phụ lục')
    CHI_TIET_ID = fields.Many2one('thue.chon.ky.tinh.thue', string='Chi tiết', help='Chi tiết')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    AUTO_SELECT = fields.Boolean()