# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_LUONG_TRA_LUONG_FORM_THAM_SO_CHI_TIET(models.Model):
    _name = 'tien.luong.tra.luong.form.tham.so.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']

    MA_NHAN_VIEN_ID = fields.Many2one('res.partner',string='Mã nhân viên', help='Mã nhân viên')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc' , string='Đơn vị', help='Đơn vị')
    MA_NHAN_VIEN = fields.Char(string='Mã nhân viên', help='Mã nhân viên')
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='Tên nhân viên')
    DON_VI = fields.Char(string='Đơn vị', help='Đơn vị')
    SO_TAI_KHOAN = fields.Char(string='Số tài khoản', help='Số tài khoản')
    TEN_NGAN_HANG = fields.Char(string='Tên ngân hàng', help='Tên ngân hàng')
    SO_CON_PHAI_TRA = fields.Float(string='Số còn phải trả', help='Số còn phải trả')
    SO_TRA = fields.Float(string='Số trả', help='Số trả')
    LICH_SU_TRA_LUONG = fields.Char(string='Lịch sử trả lương', help='Lịch sử trả lương')
    CHI_TIET_ID = fields.Many2one('tien.luong.tra.luong.form.tham.so', string='Chi tiết', help='Chi tiết')
    NGAN_HANG_ID = fields.Many2one('danh.muc.doi.tuong.chi.tiet',string='Số tài khoản', help='Số tài khoản')
    name = fields.Char(string='Name', oldname='NAME')
    AUTO_SELECT = fields.Boolean()
