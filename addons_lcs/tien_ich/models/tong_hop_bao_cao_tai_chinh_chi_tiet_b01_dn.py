# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class TONG_HOP_BAO_CAO_TAI_CHINH_CHI_TIET_B01_DN(models.Model):
    _name = 'tong.hop.bao.cao.tai.chinh.chi.tiet.b01.dn'
    _description = ''
    _inherit = ['mail.thread']
    CHI_TIEU = fields.Char(string='Chỉ tiêu', help='Chỉ tiêu')
    MA_SO = fields.Char(string='Mã số', help='Mã số')
    THUYET_MINH = fields.Char(string='Thuyết minh', help='Thuyết minh')
    SO_CUOI_QUY = fields.Float(string='Số cuối quý', help='Số cuối quý',digits= decimal_precision.get_precision('VND'))
    SO_DAU_QUY = fields.Float(string='Số đầu quý', help='Số đầu quý',digits= decimal_precision.get_precision('VND'))
    BAO_CAO_TAI_CHINH_ID = fields.Many2one('tong.hop.bao.cao.tai.chinh', string='Báo cáo tài chính', help='Báo cáo tài chính', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')