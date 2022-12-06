# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class DANH_MUC_MA_THONG_KE(models.Model):
    _name = 'danh.muc.ma.thong.ke'
    _description = 'Danh mục mã thống kê'
    _parent_store = True
    _inherit = ['mail.thread']
    _order = "MA_THONG_KE"


    MA_THONG_KE = fields.Char(string='Mã (*)', help='Mã')
    TEN_THONG_KE = fields.Char(string='Tên (*)', help='Tên')
    parent_id = fields.Many2one('danh.muc.ma.thong.ke',string='Thuộc', help='Thuộc')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    name = fields.Char(string='Name', help='Name',related='MA_THONG_KE', store=True)
    MA_PHAN_CAP = fields.Char(string='Mã phân cấp', help='Mã phân cấp')

    _sql_constraints = [
        ('MA_THONG_KE_uniq', 'unique ("MA_THONG_KE")', 'Mã thống kê <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]
