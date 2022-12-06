# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_LOAI_TAI_SAN_CO_DINH(models.Model):
    _name = 'danh.muc.loai.tai.san.co.dinh'
    _description = 'Loại tài sản cố định'
    _parent_store = True
    _inherit = ['mail.thread']
    MA = fields.Char(string='Mã(*)', help='Mã')
    TEN = fields.Char(string='Tên(*)', help='Tên')
    parent_id = fields.Many2one('danh.muc.loai.tai.san.co.dinh', string='Thuộc loại', help='Thuộc loại')
    TK_NGUYEN_GIA_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK nguyên giá', help='Tài khoản nguyên giá')
    TK_KHAU_HAO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK khấu hao', help='Tài khoản khấu hao')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    name = fields.Char(string='Name', help='Name', related='TEN', store=True)
    MA_PHAN_CAP = fields.Char(string='Mã phân cấp', help='Mã phân cấp')

    _sql_constraints = [
        ('MA_uniq', 'unique ("MA")', 'Mã loại tài sản cố định <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]


    # @api.model
    # def create(self, vals): 
    #     # if not vals.get('move_lines'):
    #        # raise ValidationError("Bạn phải nhập chứng từ chi tiết!")
    #     if (vals.get('TEN')):
    #         vals['name'] = vals.get('TEN')
    #     result = super(DANH_MUC_LOAI_TAI_SAN_CO_DINH, self).create(vals)
    #     return result

