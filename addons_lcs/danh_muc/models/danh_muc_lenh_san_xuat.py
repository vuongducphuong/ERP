# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_LENH_SAN_XUAT(models.Model):
    _name = 'danh.muc.lenh.san.xuat'
    _description = ''
    _inherit = ['mail.thread']
    NGAY = fields.Date(string='Ngày', help='Ngày')
    SO_LENH_SAN_XUAT = fields.Char(string='Số lệnh sản xuất', help='Số lệnh sản xuất', auto_num='danh_muc_lenh_san_xuat_SO_LENH_SAN_XUAT')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    @api.model
    def create(self, vals): 
        # if not vals.get('move_lines'):
           # raise ValidationError("Bạn phải nhập chứng từ chi tiết!")
        if (vals.get('SO_LENH_SAN_XUAT')):
            vals['name'] = vals.get('SO_LENH_SAN_XUAT')
        result = super(DANH_MUC_LENH_SAN_XUAT, self).create(vals)
        return result