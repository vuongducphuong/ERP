# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class DANH_MUC_BIEU_TINH_THUE_THU_NHAP_TIEN_LUONG(models.Model):
    _name = 'danh.muc.bieu.tinh.thue.thu.nhap.tien.luong'
    _description = 'Danh mục biểu tính thuế thu nhập tiền lương'
    _inherit = ['mail.thread']
    BAC = fields.Integer(string='Bậc', help='Bậc')
    PHAN_THU_NHAP_TU = fields.Float(string='Phần thu nhập từ', help='Phần thu nhập từ',digits= decimal_precision.get_precision('Product Price'))
    PHAN_THU_NHAP_DEN = fields.Float(string='Phần thu nhập đến', help='Phần thu nhập đến',digits= decimal_precision.get_precision('Product Price'))
    THUE_SUAT = fields.Float(string='Thuế suất', help='Thuế suất')
    name = fields.Integer(string='Name', help='Name', related='BAC' ,store=True)
    THUE_THEO_NAM_TU = fields.Float(string='Từ biểu tính thuế theo năm ', help='Từ biểu tính thuế theo năm',digits= decimal_precision.get_precision('Product Price'))
    THUE_THEO_NAM_DEN = fields.Float(string='Đến biểu tính thuế theo năm ', help='Đến biểu tính thuế theo năm',digits= decimal_precision.get_precision('Product Price'))


    @api.onchange('PHAN_THU_NHAP_TU','PHAN_THU_NHAP_DEN')
    def update_THUE_THEO_NAM(self):
        self.THUE_THEO_NAM_TU = self.PHAN_THU_NHAP_TU * 12
        self.THUE_THEO_NAM_DEN = self. PHAN_THU_NHAP_DEN * 12