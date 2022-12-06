# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class DANH_MUC_DIEU_KHOAN_THANH_TOAN(models.Model):
    _name = 'danh.muc.dieu.khoan.thanh.toan'
    _description = 'Danh mục điều khoản thanh toán'
    _inherit = ['mail.thread']
    _order = "MA_DIEU_KHOAN"
    
    MA_DIEU_KHOAN = fields.Char(string='Mã(*)', help='Mã điều khoản', required=True)#auto_num='danh_muc_dieu_khoan_thanh_toan_MA_DIEU_KHOAN')
    TEN_DIEU_KHOAN = fields.Char(string='Tên(*)', help='Tên điều khoản', required=True)#auto_num='danh_muc_dieu_khoan_thanh_toan_TEN_DIEU_KHOAN')
    SO_NGAY_DUOC_NO = fields.Integer(string='Số ngày được nợ', help='Số ngày được nợ')
    THOI_HAN_HUONG_CHIET_KHAU = fields.Integer(string='Thời hạn hưởng chiết khấu', help='Thời hạn hưởng chiết khấu')
    TY_LE_CHIET_KHAU = fields.Float(string='Tỷ lệ chiết khấu (%)', help='Tỷ lệ chiết khấu')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    name = fields.Char(string='Name', help='Name',related='MA_DIEU_KHOAN', store=True)

    _sql_constraints = [
        ('MA_DIEU_KHOAN_uniq', 'unique ("MA_DIEU_KHOAN")', 'Mã điều khoản <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]

    @api.model
    def create(self, values):
        if(values.get('TEN_DIEU_KHOAN')):
            values['name']=values.get('TEN_DIEU_KHOAN')
        if not values.get('MA_DIEU_KHOAN'):
            raise ValidationError("<Mã> không được bỏ trống.")
        elif not values.get('TEN_DIEU_KHOAN'):
            raise ValidationError("<Tên> không được bỏ trống.")
        result = super(DANH_MUC_DIEU_KHOAN_THANH_TOAN, self).create(values)

        return result
    