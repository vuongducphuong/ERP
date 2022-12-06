# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class STOCK_EX_THANH_PHAM_CHI_TIET_DINH_MUC_XUAT_NVL(models.Model):
    _name = 'stock.ex.thanh.pham.chi.tiet.dinh.muc.xuat.nvl'
    _description = ''
    _inherit = ['mail.thread']
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã nguyên vật liệu', help='Mã nguyên vật liệu')
    TEN_NGUYEN_VAT_LIEU = fields.Char(string='Tên nguyên vật liệu', help='Tên nguyên vật liệu')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đơn vị tính')
    SO_LUONG_NVL_TREN_SP = fields.Float(string='Số lượng NVL/1 đơn vị SP', help='Số lượng nguyên vật liệu trên 1 sản phẩm', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_NVL = fields.Float(string='Số lượng NVL', help='Số lượng nguyên vật liệu', digits=decimal_precision.get_precision('SO_LUONG'))
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng tập hợp chi phí')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục CP', help='Khoản mục chi phí')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    THANH_PHAM_CHI_TIET_DINH_MUC_XUAT_NVL_ID = fields.Many2one('stock.ex.lenh.san.xuat.chi.tiet.thanh.pham', string='Thành phẩm chi tiết định mức xuất  nvl', help='Thành phẩm chi tiết định mức xuất  nvl', ondelete='cascade')

    @api.onchange('MA_HANG_ID')
    def _onchange_TEN_NGUYEN_VAT_LIEU(self):
        for record in self:
            record.TEN_NGUYEN_VAT_LIEU = record.MA_HANG_ID.TEN
            record.DVT_ID = record.MA_HANG_ID.DVT_CHINH_ID
            record.DOI_TUONG_THCP_ID = record.MA_HANG_ID.lay_doi_tuong_thcp()