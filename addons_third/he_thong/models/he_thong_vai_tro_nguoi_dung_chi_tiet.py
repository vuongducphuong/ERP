# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class HE_THONG_THIET_LAP_VAI_TRO_CHI_TIET(models.Model):
    _name = 'he.thong.vai.tro.nguoi.dung.chi.tiet'
    _description = 'Thêm người dùng'
    _auto = False

    THIET_LAP_ID = fields.Many2one('he.thong.vai.tro.nguoi.dung')
    user_id = fields.Many2one('res.users', string='Người dùng')
    TEN_DANG_NHAP = fields.Char('Tên đăng nhập', related='user_id.login')
    HO_VA_TEN = fields.Char('Họ và tên', related='user_id.name')
    CHUC_DANH = fields.Char('Chức danh', related='user_id.CHUC_DANH')
    CHI_NHANH_IDS = fields.Many2many('danh.muc.to.chuc', string='Làm việc với chi nhánh')
    AUTO_SELECT = fields.Boolean('Chọn')

