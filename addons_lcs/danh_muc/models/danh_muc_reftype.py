# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_REFTYPE(models.Model):
    _name = 'danh.muc.reftype'
    _description = ''
    _inherit = ['mail.thread']
    REFTYPE = fields.Integer(string='Reftype', help='Reftype')
    REFTYPENAME = fields.Char(string='Reftypename', help='Reftypename')
    name = fields.Char(string='Name', help='Name', oldname='NAME')