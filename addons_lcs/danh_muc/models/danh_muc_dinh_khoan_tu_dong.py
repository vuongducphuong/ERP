# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_DINH_KHOAN_TU_DONG(models.Model):
    _name = 'danh.muc.dinh.khoan.tu.dong'
    _description = ''
    _inherit = ['mail.thread']
    _order = "TEN_DINH_KHOAN"
    
    LOAI_CHUNG_TU = fields.Selection([('0', 'Thu tiền mặt'), ('1', 'Chi tiền mặt'), ('2', 'Thu tiền gửi'), ('3', 'Chi tiền gửi'), ('4', 'Nghiệp vụ khác'), ('5', 'Quyết toán tạm ứng'), ], string='Loại chứng từ (*)', help='Loại chứng từ',required=True)
    TEN_DINH_KHOAN = fields.Char(string='Tên định khoản (*)', help='Tên định khoản',required=True)
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK nợ', help='Tài khoản nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK có', help='Tài khoản có')
    name = fields.Char(string='Name', help='Name',related='TEN_DINH_KHOAN',store=True)

    _sql_constraints = [
	    ('TEN_DINH_KHOAN_uniq', 'unique ("TEN_DINH_KHOAN","LOAI_CHUNG_TU")', 'Tên định khoản đã tồn tại!'),
	]