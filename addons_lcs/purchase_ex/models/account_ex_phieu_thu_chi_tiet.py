# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class PHIEU_THU_CHI_TIET_INHERIT(models.Model):
    _inherit = 'account.ex.phieu.thu.chi.tiet'

    HOP_DONG_MUA_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang', string='Hợp đồng mua', help='Hợp đồng mua')