# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_CAU_HINH_LAI_LO_CHO_CT_HD_DH_CONG_THUC(models.Model):
    _name = 'tien.ich.cau.hinh.lai.lo.cho.ct.hd.dh.cong.thuc'
    _description = ''
    _inherit = ['mail.thread']
    MA_BAO_CAO = fields.Char(string='Mã báo cáo', help='Mã báo cáo')
    HE_THONG_KE_TOAN = fields.Char(string='Hệ thống kế toán', help='Hệ thống kế toán')
    CAU_HINH_LAI_LO_CHO_CT_HD_DH_ID = fields.Many2one('tien.ich.cau.hinh.lai.lo.cho.ct.hd.dh', string='Cấu hình lãi lỗ cho ct hd dh', help='Cấu hình lãi lỗ cho công trình hợp đồng đơn hàng')
    TEN_COT = fields.Char(string='Tên cột', help='Tên cột')
    AM_DUONG = fields.Integer(string='Âm dương', help='Âm dương')
    MA_HAM = fields.Char(string='Mã hàm', help='Mã hàm')
    MA_TAI_KHOAN = fields.Char(string='Mã tài khoản', help='Mã tài khoản')
    TAI_KHOAN_DOI_UNG = fields.Char(string='Tài khoản đối ứng', help='Tài khoản đối ứng')
    KY = fields.Integer(string='Kỳ', help='Kỳ')
    sequence = fields.Integer()
    name = fields.Char(string='Name', help='Name')