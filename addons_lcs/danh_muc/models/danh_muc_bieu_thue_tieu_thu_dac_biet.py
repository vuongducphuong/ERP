# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision


class DANH_MUC_BIEU_THUE_TIEU_THU_DAC_BIET(models.Model):
    _name = 'danh.muc.bieu.thue.tieu.thu.dac.biet'
    _description = 'Biểu thuế tiêu thụ đặc biệt'
    _inherit = ['mail.thread'] 
    MA = fields.Char(string='Mã (*)', help='Mã')
    TEN = fields.Char(string='Tên (*)', help='Tên',required=True)
    THUOC = fields.Many2one('danh.muc.bieu.thue.tieu.thu.dac.biet',string='Thuộc (*)', help='Thuộc')
    DVT = fields.Char(string='ĐVT', help='Đơn vị tính')
    THUE_SUAT = fields.Float(string='Thuế suất (%)', help='Thuế suất')
    DIEN_GIAI = fields.Text(string='Diễn giải', help='Diễn giải')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    name = fields.Char(string='Name', help='Name',related='TEN', store=True)

    _sql_constraints = [
        ('MA_uniq', 'unique ("MA")', 'Mã biểu thuế <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]

    
    @api.model
    def create(self, values):
        if(values.get('TEN')):
            values['name']=values.get('TEN')
        if not values.get('MA'):
            raise ValidationError("<Mã> không được bỏ trống.")
        elif not values.get('TEN'):
            raise ValidationError("<Tên> không được bỏ trống.")
        # elif not values.get('THUOC'):
        #     raise ValidationError("<Thuộc> không được phép bỏ trống.") 
        result = super(DANH_MUC_BIEU_THUE_TIEU_THU_DAC_BIET, self).create(values)
    
        return result
    