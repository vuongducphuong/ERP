# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class TIEN_LUONG_NOP_BAO_HIEM_FORM_THAM_SO_CHI_TIET(models.Model):
    _name = 'tien.luong.nop.bao.hiem.form.tham.so.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    KHOAN_PHAI_NOP = fields.Char(string='Khoản phải nộp', help='Khoản phải nộp')
    SO_PHAI_NOP = fields.Float(string='Số phải nộp', help='Số phải nộp',digits=decimal_precision.get_precision('VND'))
    SO_NOP_LAN_NAY = fields.Float(string='Số nộp lần này', help='Số nộp lần này',digits= decimal_precision.get_precision('VND'))
    CHI_TIET_ID = fields.Many2one('tien.luong.nop.bao.hiem.form.tham.so', string='Chi tiết', help='Chi tiết')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    SO_TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan')

    AUTO_SELECT = fields.Boolean()