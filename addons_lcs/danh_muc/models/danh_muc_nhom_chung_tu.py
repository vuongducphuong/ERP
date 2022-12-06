# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_NHOM_CHUNG_TU(models.Model):
    _name = 'danh.muc.nhom.chung.tu'
    _description = ''
    _inherit = ['mail.thread']
    NHOM_LOAI_CHUNG_TU = fields.Integer(string='Nhóm loại chứng từ', help='Nhóm loại chứng từ')
    TEN_NHOM_LOAI_CHUNG_TU = fields.Char(string='Tên nhóm loại chứng từ', help='Tên nhóm loại chứng từ')
    TAI_KHOAN_NO_MAC_DINH_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản nợ mặc định', help='Tài khoản nợ mặc định')
    TAI_KHOAN_CO_MAC_DINH_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản có mặc định', help='Tài khoản có mặc định')
    SU_DUNG_SO_CHUNG_TU = fields.Integer(string='Sử dụng số chứng từ', help='Sử dụng số chứng từ')
    THU_TU = fields.Integer(string='Thứ tự', help='Thứ tự')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    REF_TYPE = fields.Many2many('danh.muc.reftype', string='Ref type', help='Ref type')