# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class SUPPLY_KHAI_BAO_CCDC_DAU_KY_DON_VI_SD(models.Model):
    _name = 'supply.khai.bao.dau.ky.don.vi.sd'
    _description = ''
    _inherit = ['mail.thread']
    MA_DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Mã đơn vị', help='Mã đơn vị')
    TEN_DON_VI = fields.Char(string='Tên đơn vị', help='Tên đơn vị')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CCDC_DAU_KY_CHI_TIET_ID = fields.Many2one('supply.khai.bao.dau.ky.chi.tiet', string='Ccdc đầu kỳ chi tiết', help='Ccdc đầu kỳ chi tiết', ondelete='cascade')

    @api.model
    def default_get(self, fields):
        rec = super(SUPPLY_KHAI_BAO_CCDC_DAU_KY_DON_VI_SD, self).default_get(fields)
        rec['SO_LUONG'] = 1
        return rec

    @api.onchange('MA_DON_VI_ID')
    def _onchange_MA_DON_VI_ID(self):
        self.TEN_DON_VI = self.MA_DON_VI_ID.TEN_DON_VI