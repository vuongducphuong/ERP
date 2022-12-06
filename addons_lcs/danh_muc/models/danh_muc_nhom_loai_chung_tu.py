# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_NHOM_LOAI_CHUNG_TU(models.Model):
    _name = 'danh.muc.nhom.loai.chung.tu'
    _description = ''
    _inherit = ['mail.thread']
    MA_NHOM_CHUNG_TU = fields.Integer(string='Mã nhóm chứng từ', help='Mã nhóm chứng từ')
    TEN_NHOM_CHUNG_TU = fields.Char(string='Tên nhóm chứng từ', help='Tên nhóm chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    name = fields.Char(string='Name', help='Name',related='TEN_NHOM_CHUNG_TU',store=True, oldname='NAME')
    REF_TYPE = fields.Many2many('danh.muc.reftype', string='Ref type', help='Ref type')