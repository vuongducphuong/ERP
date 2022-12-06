# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class HE_THONG_SUB_SYSTEM(models.Model):
    _name = 'he.thong.user.join.role'
    _description = 'Quan hệ giữa User-Role trên từng Branch'

    user_id = fields.Many2one(string='Người dùng', required=True)
    VAI_TRO_ID = fields.Many2one(string='Vai trò', required=True)
    CHI_NHANH_ID = fields.Char(string='Làm việc với chi nhánh nào')