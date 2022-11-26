# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class HE_THONG_THIET_LAP_VAI_TRO(models.Model):
    _name = 'he.thong.vai.tro.nguoi.dung'
    _description = 'Thêm người dùng'
    _auto = False

    VAI_TRO_ID = fields.Many2one('he.thong.vai.tro.va.quyen.han', string='Vai trò', readonly=True)
    CHI_TIET_IDS = fields.One2many('he.thong.vai.tro.nguoi.dung.chi.tiet', 'THIET_LAP_ID', string='Tất cả chức năng')

    def action_save(self, args):
        # Reset lại quyền của vai trò
        self.env['he.thong.role.permission.mapping'].search([('VAI_TRO_ID','=',self.VAI_TRO_ID.id)]).unlink()
        for line in args.get('selected'):
            self.env['he.thong.role.permission.mapping'].create(line)
