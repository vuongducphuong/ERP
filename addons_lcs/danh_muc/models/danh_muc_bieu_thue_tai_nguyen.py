# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class DANH_MUC_BIEU_THUE_TAI_NGUYEN(models.Model):
    _name = 'danh.muc.bieu.thue.tai.nguyen'
    _description = 'Danh mục biểu thuế tài nguyên'
    _parent_store = True

    _inherit = ['mail.thread']
    MA = fields.Char(string='Mã (*)', help='Mã')
    TEN = fields.Char(string='Tên (*)', help='Tên',required=True)
    DON_VI = fields.Char(string='Đơn vị', help='Đơn vị')
    parent_id = fields.Many2one('danh.muc.bieu.thue.tai.nguyen',string='Thuộc nhóm', help='Thuộc nhóm')
    THUE_SUAT_PHAN_TRAM = fields.Float(string='Thuế suất (%)', help='Thuế suất phần trăm')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    name = fields.Char(string='Name', help='Name',related='TEN', store=True)
    MA_PHAN_CAP = fields.Char(string='Mã phân cấp', help='Mã phân cấp')


    @api.model
    def create(self, values):
        if(values.get('TEN')):
            values['name']=values.get('TEN')
        if not values.get('MA'):
            raise ValidationError("<Mã> không được bỏ trống.")
        elif not values.get('TEN'):
            raise ValidationError("<Tên> không được bỏ trống.")
        # elif not values.get('parent_id'):
        #     raise ValidationError("<Thuộc nhóm> không được phép bỏ trống.")
        result = super(DANH_MUC_BIEU_THUE_TAI_NGUYEN, self).create(values)
    
        return result