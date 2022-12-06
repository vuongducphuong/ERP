# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class HE_THONG_QUYEN(models.Model):
    _name = 'he.thong.permission'
    _description = 'Quyền hạn'

    PermissionID = fields.Char(string='Mã quyền (*)')
    PermissionName = fields.Char(string='Tên quyền (*)')
    Description = fields.Char(string='Mô tả')
    name =  fields.Char(related='PermissionID', )
    active = fields.Boolean('Theo dõi', default=True)

    _sql_constraints = [
        ('name_uniq', 'unique ("PermissionID")', 'Mã quyền hạn là duy nhất!')
    ]