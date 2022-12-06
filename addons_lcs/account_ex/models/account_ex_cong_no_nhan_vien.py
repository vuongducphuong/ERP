# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ACCOUNT_EX_CONG_NO_NHAN_VIEN(models.Model):
    _name = 'account.ex.cong.no.nhan.vien'
    _description = ''

    SO_TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Số tài khoản', help='Số tài khoản')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Mã nhân viên', help='Mã nhân viên')
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='Tên nhân viên')
    DU_NO = fields.Float(string='Dư nợ', help='Dư nợ',digits=decimal_precision.get_precision('Product Price'))
    DU_CO = fields.Float(string='Dư có', help='Dư có',digits=decimal_precision.get_precision('Product Price'))
    SO_DU_TAI_KHOAN_ID = fields.Many2one('account.ex.nhap.so.du.ban.dau', string='Số dư tài khoản', help='Số dư tài khoản', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    DU_NO_NGUYEN_TE = fields.Float(string='Dư nợ nguyên tệ', help='Dư nợ nguyên tệ')
    DU_CO_NGUYEN_TE = fields.Float(string='Dư có nguyên tệ', help='Dư có nguyên tệ')
    CHI_TIET_SO_DU = fields.Char()
    CHI_TIET_THEO_DOI_TUONG = fields.Integer(string='Chi tiết theo đối tượng', help='Chi tiết theo đối tượng')
    LOAI_DOI_TUONG = fields.Integer(string='Loại đối tượng', help='Loại đối tượng')

    ACCOUNT_EX_NHAP_CHI_TIET_CONG_NO_NHAN_VIEN_IDS = fields.One2many('account.ex.nhap.chi.tiet.cong.no.nhan.vien', 'CONG_NO_NHAN_VIEN_ID', string='Nhập chi tiết công nợ nhân viên')