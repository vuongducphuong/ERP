# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_HOP_DONG_MUA(models.Model):
    _name = 'purchase.ex.hop.dong.mua.hang'
    _description = 'Hợp đồng mua hàng'
    _inherit = ['mail.thread']