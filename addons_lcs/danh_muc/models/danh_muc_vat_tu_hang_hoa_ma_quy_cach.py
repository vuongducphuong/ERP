# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class DANH_MUC_VAT_TU_HANG_HOA_MA_QUY_CACH(models.Model):
    _name = 'danh.muc.vat.tu.hang.hoa.ma.quy.cach'
    _description = ''
    _inherit = ['mail.thread']
    CHON = fields.Boolean(string='Chọn', help='Chọn')
    MA_QUY_CACH = fields.Char(string='Mã quy cách', help='Mã quy cách', auto_num='danh_muc_vat_tu_hang_hoa_ma_quy_cach_MA_QUY_CACH')
    TEN_HIEN_THI = fields.Char(string='Tên hiển thị', help='Tên hiển thị')
    CHO_PHEP_TRUNG = fields.Boolean(string='Cho phép trùng', help='Cho phép trùng')
    VAT_TU_HANG_HOA_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Vật tư hàng hóa', help='Vật tư hàng hóa', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    SO_LUONG_NHAP = fields.Float(string='Số lượng nhập', help='Số lượng nhập', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_XUAT = fields.Float(string='Số lượng xuất', help='Số lượng xuất', digits=decimal_precision.get_precision('SO_LUONG'))