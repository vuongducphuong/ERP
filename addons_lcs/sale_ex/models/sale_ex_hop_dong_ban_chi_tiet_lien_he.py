# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SALE_EX_HOP_DONG_BAN_CHI_TIET_LIEN_HE(models.Model):
    _name = 'sale.ex.hop.dong.ban.chi.tiet.lien.he'
    _description = ''
    _inherit = ['mail.thread']
    HO_VA_TEN = fields.Char(string='Họ và tên', help='Họ và tên')
    CHUC_VU = fields.Char(string='Chức vụ', help='Chức vụ')
    DT_DI_DONG = fields.Char(string='Đt di động', help='Đt di động')
    DT_DI_DONG_KHAC = fields.Char(string='Đt di động khác', help='Đt di động khác')
    DT_CO_DINH = fields.Char(string='Đt cố định', help='Đt cố định')
    EMAIL = fields.Char(string='Email', help='Email')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đông bán', help='Hợp đông bán', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')