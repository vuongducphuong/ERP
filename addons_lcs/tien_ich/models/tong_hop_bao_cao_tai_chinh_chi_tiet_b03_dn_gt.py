# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_BAO_CAO_TAI_CHINH_CHI_TIET_B03_DN_GT(models.Model):
    _name = 'tong.hop.bao.cao.tai.chinh.chi.tiet.b03.dn.gt'
    _description = ''
    _inherit = ['mail.thread']
    CHI_TIEU = fields.Char(string='Chỉ tiêu', help='Chỉ tiêu')
    MA_SO = fields.Char(string='Mã số', help='Mã số')
    THUYET_MINH = fields.Char(string='Thuyết minh', help='Thuyết minh')
    QUY_NAY = fields.Float(string='Quý này', help='Quý này')
    QUY_TRUOC = fields.Float(string='Quý trước', help='Quý trước')
    BAO_CAO_TAI_CHINH_ID = fields.Many2one('tong.hop.bao.cao.tai.chinh', string='Báo cáo tài chính', help='Báo cáo tài chính', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')