# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ACCOUNT_EX_SO_DU_TK_NGAN_HANG(models.Model):
    _name = 'account.ex.so.du.tk.ngan.hang'
    _description = ''
    _inherit = ['mail.thread']
    SO_TK_NGAN_HANG_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='Số tk ngân hàng', help='Số tk ngân hàng')
    TEN_NGAN_HANG = fields.Char(string='Tên ngân hàng', help='Tên ngân hàng')
    SO_TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Số tài khoản', help='Số tài khoản')
    DU_NO = fields.Float(string='Dư nợ', help='Dư nợ',digits=decimal_precision.get_precision('Product Price'))
    DU_CO = fields.Float(string='Dư có', help='Dư có',digits=decimal_precision.get_precision('Product Price'))
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    DU_NO_NGUYEN_TE = fields.Float(string='Dư nợ nguyên tệ', help='Dư nợ nguyên tệ',digits=decimal_precision.get_precision('Product Price'))
    DU_CO_NGUYEN_TE = fields.Float(string='Dư có nguyên tệ', help='Dư có nguyên tệ',digits=decimal_precision.get_precision('Product Price'))
    SO_DU_BAN_DAU_ID = fields.Many2one('account.ex.nhap.so.du.ban.dau', string='Số dư ban đâu', help='Số dư ban đâu', ondelete='cascade')
    CHI_TIET_SO_DU = fields.Char()
    CHI_TIET_THEO_TK_NGAN_HANG = fields.Integer(string='Chi tiết theo đối tượng', help='Chi tiết theo đối tượng')