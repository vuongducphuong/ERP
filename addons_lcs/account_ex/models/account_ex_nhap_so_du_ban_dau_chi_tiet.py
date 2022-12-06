# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class ACCOUNT_EX_NHAP_SO_DU_BAN_DAU_CHI_TIET(models.Model):
    _name = 'account.ex.nhap.so.du.ban.dau.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    SO_TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Số tài khoản', help='Số tài khoản')
    SO_TAI_KHOAN = fields.Char(string='Số tài khoản', help='Số tài khoản')
    TEN_TAI_KHOAN = fields.Char(string='Tên tài khoản', help='Tên tài khoản')
#     DU_NO & DU_CO là hai biến đề lưu trữ dư nợ sau khi quy đổi sang 1 loại tiền khác VND
    DU_NO = fields.Float(string='Dư nợ', help='Dư nợ')
    DU_CO = fields.Float(string='Dư có', help='Dư có')
#  Dư nợ nguyên tệ và dư có nguyên tệ là hai biến  lưu trữ dư nợ và dư có khi loại tiền là VNĐ
    DU_NO_NGUYEN_TE = fields.Float(string='Dư nợ nguyên tệ', help='Dư nợ nguyên tệ')
    DU_CO_NGUYEN_TE = fields.Float(string='Dư có nguyên tệ', help='Dư có nguyên tệ')
    NHAP_SO_DU_BAN_DAU_ID = fields.Many2one('account.ex.nhap.so.du.ban.dau', string='Nhập số dư ban đầu', help='Nhập số dư ban đầu', ondelete='cascade')
    CHI_TIET_THEO_DOI_TUONG = fields.Integer(string='Chi tiết theo đối tượng', help='Chi tiết theo đối tượng')
    CHI_TIET_THEO_TK_NGAN_HANG = fields.Integer(string='Chi tiết theo đối tượng', help='Chi tiết theo đối tượng')
    LA_TK_TONG_HOP = fields.Boolean(string='Là tài khoản tổng hợp', help='Là tài khoản tổng hợp')
    LOAI_DOI_TUONG = fields.Integer(string='Loại đối tượng', help='Loại đối tượng')
    currency_id = fields.Many2one('res.currency', string='Loại tiền')
    child_id = fields.Integer(string='id của TK')
    parent_id = fields.Integer(string='id của TK Tổng hợp')
    TINH_CHAT_TAI_KHOAN = fields.Selection([
        ('0', 'Dư Nợ'), 
		('1', 'Dư Có'), 
		('2', 'Lưỡng tính'), 
		('3', 'Không có số dư'),
    ], related='SO_TAI_KHOAN_ID.TINH_CHAT')
    name = fields.Char(string='Name', help='Name', oldname='NAME')