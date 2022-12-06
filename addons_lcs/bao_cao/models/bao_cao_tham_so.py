# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class BAO_CAO_THAM_SO(models.Model):
    _name = 'bao.cao.tham.so'
    _description = 'Tham số của báo cáo'

    user_id = fields.Many2one('res.users', string='Người dùng', required=True)
    report = fields.Char(string='Model của báo cáo', required=True)
    params = fields.Text('Tham số báo cáo', help='Lưu dưới dạng json')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh')