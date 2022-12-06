# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class RES_USER(models.Model):
    _inherit = 'res.users'

    @api.model
    def _get_chi_nhanh(self):
        if self.env.user.CHI_NHANH_ID:
            return self.env.user.CHI_NHANH_ID
        else:
            chi_nhanh = self.env['danh.muc.to.chuc'].search([('CAP_TO_CHUC','in',['1','2'])],limit=1)
            self.env.user.write({'CHI_NHANH_ID': chi_nhanh.id})
            return chi_nhanh

    CHI_NHANH_IDS = fields.Many2many('danh.muc.to.chuc', string='Làm việc với chi nhánh', help='Các chi nhánh được làm việc', domain=[('CAP_TO_CHUC','in',['1','2'])], default=_get_chi_nhanh, required=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh đang làm việc', help='Chi nhánh đang làm việc', domain=[('CAP_TO_CHUC','in',['1','2'])],default=_get_chi_nhanh, required=True)
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    BAO_GOM_CHUNG_TU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm chứng từ chi nhánh phụ thuộc')

    @api.onchange('CHI_NHANH_IDS')
    def _onchange_CHI_NHANH_IDS(self):
        if len(self.CHI_NHANH_IDS) > 0:
            self.CHI_NHANH_ID = self.CHI_NHANH_IDS[0].id
	
