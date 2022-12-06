# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class STOCK_EX_LENH_SAN_XUAT_CHI_TIET_THANH_PHAM(models.Model):
    _name = 'stock.ex.lenh.san.xuat.chi.tiet.thanh.pham'
    _description = ''
    _inherit = ['mail.thread']
    # Updated 2019-08-03 by anhtuan: Trong phần lớn các TH, display_name của model là LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID, không phải name
    _rec_name = 'LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID'

    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã thành phẩm', help='Mã thành phẩm')
    TEN_THANH_PHAM = fields.Char(string='Tên thành phẩm', help='Tên thành phẩm')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đơn vị tính')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng thcp')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID = fields.Many2one('stock.ex.lenh.san.xuat', string='Lệnh sản xuất chi tiết thành phẩm', help='Lệnh sản xuất chi tiết thành phẩm', ondelete='cascade')
    
    name = fields.Char(string='name', help='name', related='MA_HANG_ID.MA',store=True, oldname='NAME')
    SO = fields.Char(string='Số', help='Số', related='LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID.SO_LENH', store=True)
    NGAY  = fields.Date(string='Ngày', help='Ngày', related='LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID.NGAY', store=True)
    DIEN_GIAI  = fields.Text(string='Diễn giải', help='Diễn giải', related='LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID.DIEN_GIAI', store=True)
    DA_LAP_DU_PX = fields.Boolean(string='Đã lập đủ PX', help='Đã lập đủ phiếu xuất' , related='LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID.DA_LAP_DU_PX' ,store=True )
    sequence = fields.Integer()

    STOCK_EX_THANH_PHAM_CHI_TIET_DINH_MUC_XUAT_NVL_IDS = fields.One2many('stock.ex.thanh.pham.chi.tiet.dinh.muc.xuat.nvl', 'THANH_PHAM_CHI_TIET_DINH_MUC_XUAT_NVL_ID', string='Thành phẩm chi tiết định mức xuất  NVL', copy=True)

    @api.onchange('MA_HANG_ID')
    def onchange_product_id(self):
        for record in self:
            env = self.env['stock.ex.thanh.pham.chi.tiet.dinh.muc.xuat.nvl']
            self.STOCK_EX_THANH_PHAM_CHI_TIET_DINH_MUC_XUAT_NVL_IDS = []
            if not record.SO_LUONG:
                record.SO_LUONG = 1
            record.TEN_THANH_PHAM = record.MA_HANG_ID.TEN
            record.DVT_ID = record.MA_HANG_ID.DVT_CHINH_ID
            record.DOI_TUONG_THCP_ID = record.MA_HANG_ID.lay_doi_tuong_thcp()

            if record.MA_HANG_ID.DANH_MUC_VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_IDS:
                for line in record.MA_HANG_ID.DANH_MUC_VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_IDS:
                    new_line_dong1 = env.new({
                        'MA_HANG_ID': line.MA_NGUYEN_VAT_LIEU_ID.id,
                        'TEN_NGUYEN_VAT_LIEU': line.TEN_NGUYEN_VAT_LIEU,
                        'DVT_ID': line.DVT_ID.id,
                        'SO_LUONG_NVL_TREN_SP': line.SO_LUONG,   
                        'SO_LUONG_NVL': line.SO_LUONG*self.SO_LUONG,
                    })

                    self.STOCK_EX_THANH_PHAM_CHI_TIET_DINH_MUC_XUAT_NVL_IDS += new_line_dong1

    @api.onchange('SO_LUONG')
    def _onchange_SO_LUONG(self):
        if self.STOCK_EX_THANH_PHAM_CHI_TIET_DINH_MUC_XUAT_NVL_IDS and self.MA_HANG_ID:
            for line in self.STOCK_EX_THANH_PHAM_CHI_TIET_DINH_MUC_XUAT_NVL_IDS:
                line.SO_LUONG_NVL = line.SO_LUONG_NVL_TREN_SP*self.SO_LUONG
