# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class HE_THONG_THIET_LAP_VAI_TRO(models.Model):
    _name = 'he.thong.thiet.lap.vai.tro'
    _description = 'Thiết lập vai trò'
    _auto = False

    VAI_TRO_ID = fields.Many2one('he.thong.vai.tro.va.quyen.han', string='Vai trò', readonly=True)
    CHI_TIET_IDS = fields.One2many('he.thong.thiet.lap.vai.tro.chi.tiet', 'THIET_LAP_ID', string='Tất cả chức năng')

    def action_save(self, args):
        # Reset lại quyền của vai trò
        for role in self.env['he.thong.role.permission.mapping'].search([('VAI_TRO_ID','=',self.VAI_TRO_ID.id)]):
            if role.permission_id.active:
                role.unlink()
        # Dùng can_view_report như VAI_TRO_ID
        can_view_report = False
        for line in args.get('selected'):
            if line.get('report_id'):
                can_view_report = line.get('VAI_TRO_ID')
            self.env['he.thong.role.permission.mapping'].create(line)
        # Bổ sung menu báo cáo
        if can_view_report:
            self.env['he.thong.role.permission.mapping'].create({
                'VAI_TRO_ID': can_view_report,
                'permission_id': self.env.ref('base_import_ex_he_thong_permission.Use').id,
                'menu_id': self.env.ref('menu.menu_bao_cao').id,
            })
