# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class TIEN_ICH_TIM_KIEM_CHUNG_TU_CAC_DIEU_KIEN_DA_CHON(models.Model):
    _name = 'tien.ich.tim.kiem.chung.tu.cac.dieu.kien.da.chon'
    _description = ''
    _inherit = ['mail.thread']
    VA_HOAC = fields.Char( string='Tìm theo', help='Tìm theo')
    TIM_THEO = fields.Char(string='Tìm theo', help='Tìm theo')
    TU_NGAY = fields.Char(string='Từ ngày', help='Từ ngày')
    DEN_NGAY = fields.Char(string='Đến ngày', help='Đến ngày')
    GIA_TRI  = fields.Char(string='Giá trị', help='Giá trị')

    DIEU_KIEN = fields.Char(string='Điều kiện', help='Điều kiện')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    TIM_KIEM_CHUNG_TU_ID = fields.Many2one('tien.ich.tim.kiem.chung.tu', string='Tìm kiếm chứng từ', help='Tìm kiếm chứng từ')