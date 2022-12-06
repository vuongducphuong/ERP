# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_DOI_TUONG_DIA_DIEM_GIAO_HANG(models.Model):
    _name = 'danh.muc.doi.tuong.dia.diem.giao.hang'
    _description = ''
    _inherit = ['mail.thread']
    DIA_DIEM = fields.Char(string='Địa điểm', help='Địa điểm')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')