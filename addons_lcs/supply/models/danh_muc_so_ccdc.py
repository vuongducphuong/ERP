# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
class SO_CCDC_CHI_TIET(models.Model):
    _inherit = 'so.ccdc.chi.tiet'

    CCDC_ID = fields.Many2one('supply.ghi.tang', string='Ccdc', help='SupplyID')
    MA_CCDC = fields.Char(string='Mã ccdc', help='Mã ccdc', compute='_compute_CCDC_ID', store=True)
    TEN_CCDC = fields.Char(string='Tên ccdc', help='Tên ccdc', compute='_compute_CCDC_ID', store=True)
	
    @api.depends('CCDC_ID')
    def _compute_CCDC_ID(self):
        for record in self:
            record.MA_CCDC = record.CCDC_ID.MA_CCDC
            record.TEN_CCDC = record.CCDC_ID.TEN_CCDC