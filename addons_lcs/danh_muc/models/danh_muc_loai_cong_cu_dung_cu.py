# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_LOAI_CONG_CU_DUNG_CU(models.Model):
    _name = 'danh.muc.loai.cong.cu.dung.cu'
    _description = 'Danh mục loại công cụ dụng cụ'
    _parent_store = True
    _inherit = ['mail.thread']
    MA = fields.Char(string='Mã(*)', help='Mã')
    TEN = fields.Char(string='Tên(*)', help='Tên')
    parent_id = fields.Many2one('danh.muc.loai.cong.cu.dung.cu', string='Thuộc', help='Thuộc')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    name = fields.Char(string='Name', help='Name', related='TEN', store=True)
    MA_PHAN_CAP = fields.Char(string='Mã phân cấp', help='Mã phân cấp')

    _sql_constraints = [
        ('MA_uniq', 'unique ("MA")', 'Mã loại công cụ dụng cụ <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]
