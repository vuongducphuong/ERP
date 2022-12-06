# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class HE_THONG_THIET_LAP_VAI_TRO_CHI_TIET(models.Model):
    _name = 'he.thong.thiet.lap.vai.tro.chi.tiet'
    _description = 'Thiết lập vai trò'
    _auto = False

    THIET_LAP_ID = fields.Many2one('he.thong.thiet.lap.vai.tro')
    menu = fields.Integer(string='Menu')
    parent = fields.Integer(string='Menu Parent')    
    menu_id = fields.Many2one('ir.ui.menu', string='Menu')
    parent_menu_id = fields.Many2one('ir.ui.menu', string='Menu')
    report_id = fields.Many2one('tien.ich.bao.cao', string='Report')
    parent_report_id = fields.Many2one('tien.ich.bao.cao', string='Report')
    permission_id = fields.Many2one('he.thong.permission', string='Quyền hạn')
    AUTO_SELECT = fields.Boolean('Chọn')
    name = fields.Char('Chức năng')

