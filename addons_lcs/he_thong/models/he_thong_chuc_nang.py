# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class HE_THONG_SUB_SYSTEM(models.Model):
    _name = 'he.thong.chuc.nang'
    _description = 'Cây chức năng'

    menu_id = fields.Many2one('ir.ui.menu', string='Menu')
    parent_menu_id = fields.Many2one('ir.ui.menu', string='Parent Menu')
    permission_id = fields.Many2one('he.thong.permission', string='Quyền hạn')
    name = fields.Char('Chức năng')