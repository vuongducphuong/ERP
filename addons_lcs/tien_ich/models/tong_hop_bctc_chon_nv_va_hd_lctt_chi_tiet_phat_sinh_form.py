# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
class TONG_HOP_BCTC_CHON_NV_VA_HD_LCTT_CHI_TIET_PHAT_SINH_FORM(models.Model):
    _name = 'tong.hop.bctc.chon.nv.va.hd.lctt.chi.tiet.phat.sinh.form'
    _description = ''
    _inherit = ['mail.thread']

    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Float(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK Nợ', help='Tk nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK Có', help='Tk có')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits= decimal_precision.get_precision('VND'))
    HOAT_DONG = fields.Boolean(string='Hoạt động', help='Hoạt động')
    BCTC_CHON_NGHIEP_VU_VA_HOAT_DONG_LCTT_ID = fields.Many2one('tong.hop.bctc.chon.nghiep.vu.va.hoat.dong.lctt.form', string='Bctc chọn nghiệp vụ và hoạt động lctt', help='Bctc chọn nghiệp vụ và hoạt động lctt')
    name = fields.Char(string='Name', help='Name', oldname='NAME')