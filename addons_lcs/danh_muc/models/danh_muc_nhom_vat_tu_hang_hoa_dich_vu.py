# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_NHOM_VAT_TU_HANG_HOA_DICH_VU(models.Model):
    _name = 'danh.muc.nhom.vat.tu.hang.hoa.dich.vu'
    _description = 'Vật tư, hàng hóa, dịch vụ'
    _parent_store = True

    _inherit = ['mail.thread']
    MA = fields.Char(string='Mã (*)', help='Mã',required=True)
    parent_id = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Thuộc', help='Thuộc')
    TEN = fields.Char(string='Tên (*)', help='Tên', required=True)
    name = fields.Char(string='name', help='name',related='MA',store=True)
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    MA_PHAN_CAP = fields.Char(string='Mã phân cấp', help='Mã phân cấp')

    _sql_constraints = [
        ('MA_uniq', 'unique ("MA")', 'Mã nhóm vật tư, hàng hóa, dịch vụ <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]
