# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class HE_THONG_VAI_TRO_QUYEN_HAN(models.Model):
    _name = 'he.thong.role.permission.mapping'
    _description = 'Vai trò gắn với quyền hạn'

    VAI_TRO_ID = fields.Many2one('he.thong.vai.tro.va.quyen.han', string='Vai trò')
    menu_id = fields.Many2one('ir.ui.menu', string='Menu', ondelete='set null')
    model_id = fields.Many2one('ir.model', string='Model', compute='_compute_model', store=True, )
    permission_id = fields.Many2one('he.thong.permission', string='Quyền hạn', required=True)
    report_id = fields.Many2one('tien.ich.bao.cao', string='Báo cáo')
    ref = fields.Char(string='ref_id của Menu/Báo cáo trong ir.model.data')

    @api.multi
    @api.depends('menu_id')
    def _compute_model(self):
        for record in self:
            record.model_id = record.menu_id.model_id.id

    # _sql_constraints = [
    #     ('name_uniq', 'unique ("VAI_TRO_ID",menu_id,permission_id)', 'Quyền và menu gắn với một vai trò là duy nhất!')
    # ]