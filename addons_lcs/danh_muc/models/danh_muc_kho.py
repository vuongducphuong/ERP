# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_KHO(models.Model):
    _name = 'danh.muc.kho'
    _description = 'Kho'
    _inherit = ['mail.thread']
    _order = "MA_KHO"

    MA_KHO = fields.Char(string='Mã (*)', help='Mã kho', required=True)
    TEN_KHO = fields.Char(string='Tên (*)', help='Tên kho', required=True)
    TK_KHO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK kho', help='Tài khoản kho')
    DIA_CHI = fields.Text(string='Địa chỉ', help='Địa chỉ')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    name = fields.Char(string='Name', help='Name', related='MA_KHO', store=True, )
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

    _sql_constraints = [
        ('MA_KHO_uniq', 'unique ("MA_KHO")', 'Mã <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]

