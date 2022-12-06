# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class DANH_MUC_LOAI_CHUNG_TU(models.Model):
    _name = 'danh.muc.loai.chung.tu'
    _description = ''
    _inherit = ['mail.thread']
    _order = "MA_LOAI, TEN_LOAI"
    
    MA_LOAI = fields.Char(string='Mã loại (*)', help='Mã loại', required=True)
    TEN_LOAI = fields.Char(string='Tên loại (*)', help='Tên loại', required=True)
    # NHOM_CHUNG_TU = fields.Char(string='Nhóm chứng từ', help='Nhóm chứng từ',readonly=True)
    NHOM_LOAI_CHUNG_TU_ID = fields.Many2many('danh.muc.nhom.loai.chung.tu', string='Nhóm loại chứng từ', help='Nhóm loại chứng từ')
    NHOM_CHUNG_TU_ID = fields.Many2many('danh.muc.nhom.chung.tu', string='Nhóm chứng từ', help='Nhóm chứng từ')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK Nợ', help='Tài khoản nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK Có', help='Tài khoản có')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    active = fields.Boolean(string='Ngừng theo dõi ', help='Ngừng theo dõi ')
    name = fields.Char(string='Name', help='Name',related='TEN_LOAI', store=True)
    PHAT_SINH_SELECTION = fields.Selection([('PHAT_SINH_THEO_TAI_KHOAN', 'Phát sinh theo tài khoản'),('PHAT_SINH_THEO_NHOM_CHUNG_TU', 'Phát sinh theo nhóm chứng từ'),],  default='PHAT_SINH_THEO_TAI_KHOAN')
    MA = fields.Integer()

    _sql_constraints = [
        ('MA_LOAI_uniq', 'unique ("MA_LOAI")', 'Mã loại chứng từ <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]

    @api.model
    def create(self, values):
        if not values.get('MA_LOAI'):
            raise ValidationError("<Mã loại> không được bỏ trống.")
        elif not values.get('TEN_LOAI'):
            raise ValidationError("<Tên loại> không được bỏ trống.")
        # elif (not values.get('TK_NO_ID') and not values.get('TK_CO_ID')):
        #     raise ValidationError("Bạn phải nhập ít nhất TK nợ hoặc TK có.") 
        result = super(DANH_MUC_LOAI_CHUNG_TU, self).create(values)

        return result