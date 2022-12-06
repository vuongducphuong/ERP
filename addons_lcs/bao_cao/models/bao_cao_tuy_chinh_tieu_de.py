# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class BAO_CAO_TUY_CHINH_TIEU_DE(models.Model):
    _name = 'bao.cao.tuy.chinh.tieu.de'
    _description = 'Tiêu đề của báo cáo'

    header = fields.Text('Tiêu đề', help='Html của header')

    @api.model
    def default_get(self, fields):
        rec = super(BAO_CAO_TUY_CHINH_TIEU_DE, self).default_get(fields)
        html = self.env.ref('bao_cao.external_layout_customized_header')
        if html:
            rec['header'] = html.arch_db
        return rec

    def _action_view_report(self):
        self.ensure_one()
        html = self.env.ref('bao_cao.external_layout_customized_header')
        if html:
            html.write({'arch_db': self.header})
        return True