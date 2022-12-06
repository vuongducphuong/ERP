# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_GHI_SO_HOAC_BO_GHI_SO_THEO_LO_PHAN_HE(models.Model):
    _name = 'tien.ich.ghi.so.hoac.bo.ghi.so.theo.lo.phan.he'
    _description = ''
    _inherit = ['mail.thread']
    PHAN_HE = fields.Char(string='Phân hệ', help='Phân hệ')
    AUTO_SELECT = fields.Boolean()
    GHI_SO_HOAC_BO_GHI_SO_THEO_LO_PHAN_HE_ID = fields.Many2one('tien.ich.ghi.so.hoac.bo.ghi.so.theo.lo', string='Ghi sổ hoặc bỏ ghi sổ theo lô phân hệ', help='Ghi sổ hoặc bỏ ghi sổ theo lô phân hệ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')