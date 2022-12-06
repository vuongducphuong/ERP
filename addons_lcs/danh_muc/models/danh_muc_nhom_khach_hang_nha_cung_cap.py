# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_NHOM_KHACH_HANG_NHA_CUNG_CAP(models.Model):
    _name = 'danh.muc.nhom.khach.hang.nha.cung.cap'
    _description = 'Nhóm khách hàng nhà cung cấp'
    _parent_store = True
    _inherit = ['mail.thread']

    MA = fields.Char(string='Mã', help='Mã')
    TEN = fields.Char(string='Tên', help='Tên')
    name = fields.Char(string='name', help='name',related='MA',store=True)
    parent_id = fields.Many2one('danh.muc.nhom.khach.hang.nha.cung.cap', string='Thuộc', help='Thuộc')
    DIEN_GIAI = fields.Text(string='Diễn giải', help='Diễn giải')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    BAC = fields.Integer(string='Bậc',help='Bậc')
    MA_PHAN_CAP = fields.Char(help='Mã phân cấp')

    _sql_constraints = [
        ('MA_uniq', 'unique ("MA")', 'Mã <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]
