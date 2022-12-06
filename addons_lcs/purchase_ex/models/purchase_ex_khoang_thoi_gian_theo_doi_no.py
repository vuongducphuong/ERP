# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class PURCHASE_EX_KHOANG_THOI_GIAN_THEO_DOI_NO(models.Model):
    _name = 'purchase.ex.khoang.thoi.gian.theo.doi.no'
    _description = ''
    _inherit = ['mail.thread']
    TEN_KHOANG_THOI_GIAN_NO = fields.Char(string='Tên khoảng thời gian nợ', help='Tên khoảng thời gian nợ')
    LOAI_KHOANG_THOI_GIAN_NO = fields.Integer(string='Loại khoảng thời gian nợ', help='Loại khoảng thời gian nợ')
    TU_NGAY = fields.Integer(string='Từ ngày', help='Từ ngày')
    DEN_NGAY = fields.Integer(string='Đến ngày', help='Đến ngày')
    SAP_XEP = fields.Integer(string='Sắp xếp', help='Sắp xếp')
    MA_BAO_CAO = fields.Char(string='Mã báo cáo', help='Mã báo cáo')
    name = fields.Char(string='Name', help='Name')