# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class STOCK_EX_LENH_SAN_XUAT_CHI_TIET_DINH_MUC_XUAT_THANH_PHAM(models.Model):
    _name = 'stock.ex.lenh.san.xuat.chi.tiet.dinh.muc.xuat.thanh.pham'
    _description = ''
    _inherit = ['mail.thread']
    MA_NGUYEN_VAT_LIEU_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã nguyên vật liệu', help='Mã nguyên vật liệu')
    TEN_NGUYEN_VAT_LIEU = fields.Char(string='Tên nguyên vật liệu', help='Tên nguyên vật liệu')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='ĐVT')
    SO_LUONG_NVL_TREN_SP = fields.Float(string='Số lượng NVL/1 đơn vị SP', help='Số lượng nguyên vật liệu trên 1 đơn vị sản phẩm', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_NVL = fields.Float(string='Số lượng NVL', help='Số lượng nvl', digits=decimal_precision.get_precision('SO_LUONG'))
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng thcp')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục CP', help='Khoản mục chi phí')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    LENH_SAN_XUAT_CHI_TIET_DINH_MUC_XUAT_THANH_PHAM_ID = fields.Many2one('stock.ex.lenh.san.xuat', string='Lệnh sản xuất chi tiết định mức xuất  thành phẩm', help='Lệnh sản xuất chi tiết định mức xuất  thành phẩm')

    @api.onchange('MA_NGUYEN_VAT_LIEU_ID')
    def _onchange_field(self):
        if self.MA_NGUYEN_VAT_LIEU_ID:
            self.TEN_NGUYEN_VAT_LIEU = self.MA_NGUYEN_VAT_LIEU_ID.TEN
            self.DVT_ID = self.MA_NGUYEN_VAT_LIEU_ID.DVT_CHINH_ID