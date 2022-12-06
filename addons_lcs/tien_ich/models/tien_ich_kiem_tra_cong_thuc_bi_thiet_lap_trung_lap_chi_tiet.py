# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_KIEM_TRA_CONG_THUC_BI_THIET_LAP_TRUNG_LAP_CHI_TIET(models.Model):
    _name = 'tien.ich.kiem.tra.cong.thuc.bi.thiet.lap.trung.lap.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    TAI_KHOAN = fields.Char(string='Tài khoản', help='Tài khoản')
    MA_CHI_TIEU = fields.Char(string='Mã chỉ tiêu', help='Mã chỉ tiêu')
    TEN_CHI_TIEU = fields.Char(string='Tên chỉ tiêu', help='Tên chỉ tiêu')
    CONG_THUC = fields.Char(string='Công thức', help='Công thức')
    CHI_TIET_ID = fields.Many2one('tien.ich.kiem.tra.cong.thuc.thiet.lap.trung.lap', string='Chi tiết', help='Chi tiết')
    name = fields.Char(string='Name', help='Name', oldname='NAME')