# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class HE_THONG_VAI_TRO_VA_QUYEN_HAN_CHI_TIET(models.Model):
    _name = 'he.thong.vai.tro.va.quyen.han.chi.tiet'
    _description = 'Vai trò và quyền hạn chi tiết'

    VAI_TRO_ID = fields.Many2one('he.thong.vai.tro.va.quyen.han', string='Vai trò', ondelete='cascade')
    menu_id = fields.Many2one('ir.ui.menu', string='Menu', ondelete='set null')
    permission_id = fields.Many2one('he.thong.permission', string='Quyền hạn', required=True)
    permission_name = fields.Char(string='Tên quyền hạn')
    selected = fields.Boolean(string='Chọn', help='Nếu tích chọn, vai trò sẽ có quyền hạn này')