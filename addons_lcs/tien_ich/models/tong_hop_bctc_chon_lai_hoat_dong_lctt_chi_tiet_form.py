# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
class TONG_HOP_BCTT_CHON_LAI_HOAT_DONG_LCTT_CHI_TIET_FORM(models.Model):
    _name = 'tong.hop.bctc.chon.lai.hoat.dong.lctt.chi.tiet.form'
    _description = ''
    _inherit = ['mail.thread']

    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Float(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK Nợ', help='Tk nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK Có', help='Tk có')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits= decimal_precision.get_precision('VND'))
    HOAT_DONG = fields.Selection([('0', 'Hoạt động kinh doanh'), ('1', ' Hoạt động đầu tư'), ('3', ' Hoạt động tài chính'), ], string='Hoạt động', help='Hoạt động')
    BCTC_CHON_LAI_HOAT_DONG_LCTT_ID = fields.Many2one('tong.hop.bctc.chon.lai.hoat.dong.lctt.form', string='Bctc chọn lại hoạt động lctt', help='Bctc chọn lại hoạt động lctt')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CHI_TIET_ID = fields.Integer(string='chi tiết id', help='id của các chứng từ chi tiết')
    CHI_TIET_MODEL = fields.Char(string='model chi tiết', help='model chi tiết')