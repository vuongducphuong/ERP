# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_BCTC_KIEM_TRA_KE_TOAN_KO_CAN_CHI_TIET_CHI_TIEU_FORM(models.Model):
    _name = 'tong.hop.bctc.kiem.tra.ke.toan.ko.can.chi.tiet.chi.tieu.form'
    _description = ''
    _inherit = ['mail.thread']
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản')
    MA_CHI_TIEU = fields.Char(string='Mã chỉ tiêu', help='Mã chỉ tiêu')
    TEN_CHI_TIEU = fields.Char(string='Tên chỉ tiêu', help='Tên chỉ tiêu')
    CONG_THUC = fields.Char(string='Công thức', help='Công thức')
    BCTC_KIEM_TRA_CAN_DOI_KE_TOAN_KO_CAN_ID = fields.Many2one('tong.hop.bctc.kiem.tra.bang.ke.toan.khong.can.form', string='Bctc kiểm tra cân đối kế toán ko cân', help='Bctc kiểm tra cân đối kế toán ko cân')
    name = fields.Char(string='Name', help='Name', oldname='NAME')