# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
class SO_TSCD_CHI_TIET(models.Model):
    _inherit = 'so.tscd.chi.tiet'

    TSCD_ID = fields.Many2one('asset.ghi.tang', string='TSCĐ', help='TSCĐ')
    MA_TSCD = fields.Char(string='Mã tscd', help='Mã tscd', compute='_compute_TSCD_ID', store=True)
    TEN_TSCD = fields.Char(string='Tên tscd', help='Tên tscd', compute='_compute_TSCD_ID', store=True)

    @api.depends('TSCD_ID')
    def _compute_TSCD_ID(self):
        for record in self:
            record.MA_TSCD = record.TSCD_ID.MA_TAI_SAN
            record.TEN_TSCD = record.TSCD_ID.TEN_TAI_SAN