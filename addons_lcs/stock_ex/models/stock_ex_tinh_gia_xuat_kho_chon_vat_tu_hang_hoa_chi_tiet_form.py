# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class STOCK_EX_TINH_GIA_XUAT_KHO_CHON_VAT_TU_HANG_HOA_CHI_TIET_FORM(models.Model):
    _name = 'stock.ex.tinh.gia.xuat.kho.chon.vat.tu.hang.hoa.chi.tiet.form'
    _description = ''
    _inherit = ['mail.thread']

    AUTO_SELECT = fields.Boolean()
    MA_VAT_TU_HANG_HOA_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã vật tư hàng hóa', help='Mã vật tư hàng hóa')
    TEN_VAT_TU_HANG_HOA = fields.Char(string='Tên vật tư hàng hóa', help='Tên vật tư hàng hóa')
    NHOM_VAT_TU_HANG_HOA_ID = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm vật tư hàng hóa', help='Nhóm vật tư hàng hóa')
    TINH_GIA_XUAT_KHO_CHON_VAT_TU_HANG_HOA_ID = fields.Many2one('stock.ex.tinh.gia.xuat.kho.chon.vat.tu.hang.hoa.form', string='Tính giá xuất kho chọn vật tư hàng hóa tính giá xuất', help='Tính giá xuất kho chọn vật tư hàng hóa tính giá xuất')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    