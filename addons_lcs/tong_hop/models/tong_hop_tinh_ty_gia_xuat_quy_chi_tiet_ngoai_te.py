# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_TINH_TY_GIA_XUAT_QUY_CHI_TIET_NGOAI_TE(models.Model):
    _name = 'tong.hop.tinh.ty.gia.xuat.quy.chi.tiet.ngoai.te'
    _description = ''
    _inherit = ['mail.thread']
    AUTO_SELECT = fields.Boolean()
    MA_LOAI_TIEN_ID = fields.Many2one('res.currency', string='Mã loại tiền', help='Mã loại tiền')
    TEN_LOAI_TIEN = fields.Char(string='Tên loại tiền', help='Tên loại tiền')
    TY_GIA_XUAT_QUY_ID = fields.Many2one('tong.hop.tinh.ty.gia.xuat.quy', string='Tỷ giá xuất quỹ', help='Tỷ giá xuất quỹ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')