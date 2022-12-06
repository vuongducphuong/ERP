# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ASSET_TAI_SAN_CO_DINH_DUNG_CU_PHU_TUNG(models.Model):
    _name = 'asset.ghi.tang.dung.cu.phu.tung'
    _description = ''
    _inherit = ['mail.thread']
    TEN_QUY_CACH_DUNG_CU_PHU_TUNG = fields.Char(string='Tên quy cách dụng cụ, phụ tùng', help='Tên quy cách dụng cụ, phụ tùng')
    DON_VI_TINH = fields.Char(string='Đơn vị tính', help='Đơn vị tính')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    GIA_TRI = fields.Char(string='Giá trị', help='Giá trị')
    TAI_SAN_CO_DINH_GHI_TANG_ID = fields.Many2one('asset.ghi.tang', string='Tài sản cố định ghi tăng', help='Tài sản cố định ghi tăng', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết',help='Thứ tự sắp xếp các dòng chi tiết')
    @api.model
    def default_get(self, fields):
        rec = super(ASSET_TAI_SAN_CO_DINH_DUNG_CU_PHU_TUNG, self).default_get(fields)
        rec['SO_LUONG'] = 1
        return rec