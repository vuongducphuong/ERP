# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SUPPLY_TAP_HOP_CHUNG_TU_CCDC(models.Model):
    _name = 'supply.dieu.chinh.tap.hop.chung.tu'
    _description = ''
    _inherit = ['mail.thread']
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    TAP_HOP_CHUNG_TU_CCDC_ID_ID = fields.Many2one('supply.dieu.chinh', string='Tập hợp chứng từ ccdc id', help='Tập hợp chứng từ ccdc id', ondelete='cascade')
    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')