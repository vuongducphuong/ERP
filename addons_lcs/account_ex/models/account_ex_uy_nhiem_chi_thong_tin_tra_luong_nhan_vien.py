# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_LUONG_UY_NHIEM_CHI_THONG_TIN_TRA_LUONG_NHAN_VIEN(models.Model):
    _name = 'tien.luong.uy.nhiem.chi.thong.tin.tra.luong.nhan.vien'
    _description = ''
    _inherit = ['mail.thread']
    MA_NHAN_VIEN = fields.Many2one('res.partner',string='Mã nhân viên', help='Mã nhân viên')
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='Tên nhân viên')
    SO_TAI_KHOAN = fields.Many2one('danh.muc.doi.tuong.chi.tiet',string='Số tài khoản', help='Số tài khoản')
    TEN_NGAN_HANG = fields.Char(string='Tên ngân hàng', help='Tên ngân hàng')
    DON_VI = fields.Many2one('danh.muc.to.chuc' , string='Đơn vị', help='Đơn vị')
    SO_CON_PHAI_TRA = fields.Float(string='Số còn phải trả', help='Số còn phải trả')
    SO_TRA = fields.Float(string='Số trả', help='Số trả')
    THONG_TIN_TRA_LUONG_CHI_TIET_ID = fields.Many2one('account.ex.phieu.thu.chi', string='Thông tin trả lương chi tiết', help='Thông tin trả lương chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')