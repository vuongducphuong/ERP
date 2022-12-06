# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round

class PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA(models.Model):
    _name = 'purchase.ex.tra.lai.hang.mua.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng', required=True)
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
    KHO_ID = fields.Many2one('danh.muc.kho',string='Kho', help='Kho')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan',string='TK công nợ', help='Tài khoản công nợ')
    TK_KHO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK kho ', help='Tài khoản kho ' )
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đơn vị tính')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits= decimal_precision.get_precision('DON_GIA'))
    THANH_TIEN = fields.Monetary(string='Thành tiền', help='Thành tiền', currency_field='currency_id')
    DIEN_GIAI_THUE = fields.Char(string='Diễn giải thuế', help='Diễn giải thuế')
    PHAN_TRAM_THUE_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang',string='% thuế GTGT', help='Phần trăm thuế giá trị gia tăng')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế giá trị gia tăng', currency_field='currency_id')
    TK_THUE_GTGT_ID = fields.Many2one('danh.muc.he.thong.tai.khoan',string='TK thuế GTGT', help='Tiền thuế giá trị gia tăng')
    NHOM_HHDV_MUA_VAO_ID = fields.Many2one('danh.muc.nhom.hhdv',string='Nhóm HHDV mua vào', help='Nhóm hàng hóa dịch vụ mua vào', default=lambda self: self.lay_nhom_hhdv_mac_dinh())
    SO_LO = fields.Char(string='Số lô', help='Số lô')
    HAN_SU_DUNG = fields.Date(string='Hạn sử dụng', help='Hạn sử dụng')
    SO_CHUNG_TU = fields.Many2one('purchase.document',string='Số CT mua hàng', help='Số chứng từ mua hàng')
    SO_HD_MUA_HANG = fields.Char(string='Số HĐ mua hàng', help='Số hóa đơn mua hàng')
    NGAY_HD_MUA_HANG = fields.Date(string='Ngày HĐ mua hàng', help='Ngày hóa đơn mua hàng')
    HOP_DONG_MUA_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang', string='Hợp đồng mua', help='Hợp đồng mua')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke',string='Mã thống kê', help='Mã thống kê')
    
    # LENH_SAN_XUAT_ID = fields.Many2one('stock.ex.lenh.san.xuat',string='Lệnh sản xuất', help='Lệnh sản xuất')
    # THANH_PHAM_ID = fields.Many2one('stock.ex.lenh.san.xuat.chi.tiet.thanh.pham',string='Thành phẩm', help='Thành phẩm')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục CP', help='Khoản mục chi phí')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc',string='Đơn vị', help='Đơn vị')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng tập hợp chi phí')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang',string='Đơn đặt hàng', help='Đơn đặt hàng')
    
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban',string='Hợp đồng bán', help='Hợp đồng bán')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan',string='TK chi phí', help='Tài khoản chi phí')
    TK_TIEN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan',string='TK tiền', help='Tài khoản tiền')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CHUNG_TU_TRA_LAI_HANG_MUA_ID = fields.Many2one('purchase.ex.tra.lai.hang.mua', string='Chứng từ trả lại hàng mua ids', help='Mã hàng ', ondelete='cascade')
    THANH_TIEN_QUY_DOI = fields.Monetary(string='Thành tiền quy đổi', help='Thành tiền quy đổi', currency_field='base_currency_id')
    TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='Tiền thuế GTGT quy đổi', help='Tiền thuế GTGT quy đổi', currency_field='base_currency_id')
    CHUNG_TU_MUA_HANG = fields.Many2one('purchase.document',string='Chứng từ mua hàng', help='Chứng từ mua hàng')

    # currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền' ,related='CHUNG_TU_TRA_LAI_HANG_MUA_ID.currency_id')

    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='CHUNG_TU_TRA_LAI_HANG_MUA_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)

    SO_LUONG_DVT_CHINH = fields.Float(string='Số lượng ĐVT chính', help='Số lượng đơn vị tính chính')
    DON_GIA_DVT_CHINH = fields.Float(string='Đơn giá ĐVT chính', help='Đơn giá theo đơn vị tính chính')
    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết',help='Thứ tự sắp xếp các dòng chi tiết')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá',related='CHUNG_TU_TRA_LAI_HANG_MUA_ID.TY_GIA')
    MUA_HANG_CHI_TIET_ID = fields.Many2one('purchase.document.line', string='Chứng từ mua hàng chi tiết', help='Tạo từ chứng từ mua hàng', store=False)
    CHI_TIET_DON_MUA_HANG_ID = fields.Many2one('purchase.ex.don.mua.hang.chi.tiet',string='Đơn mua hàng chi tiết', help='Đơn mua hàng chi tiết')
    
    @api.onchange('THANH_TIEN','TIEN_THUE_GTGT','TY_GIA')
    def update_so_tien_quy_doi_details(self):
        self.tinh_tien_quy_doi()

    def tinh_tien_quy_doi(self):
        self.THANH_TIEN_QUY_DOI = float_round(self.THANH_TIEN * self.TY_GIA,0)
        self.TIEN_THUE_GTGT_QUY_DOI = float_round(self.TIEN_THUE_GTGT * self.TY_GIA,0)
    @api.onchange('MA_HANG_ID')
    def laythongtinsanpham(self):
        if self.MA_HANG_ID:
            self.TEN_HANG = self.MA_HANG_ID.TEN
            dienGiaiThue = "Thuế GTGT - " + str(self.MA_HANG_ID.TEN) if self.MA_HANG_ID.TEN else ""
            self.DIEN_GIAI_THUE = dienGiaiThue
            self.DVT_ID = self.MA_HANG_ID.DVT_CHINH_ID
            self.SO_LUONG = 1
            self.DON_GIA = self.MA_HANG_ID.DON_GIA_BAN
            self.PHAN_TRAM_THUE_GTGT_ID  =self.MA_HANG_ID.THUE_SUAT_GTGT_ID
            self.KHO_ID = self.MA_HANG_ID.KHO_NGAM_DINH_ID
            # self.DIEN_GIAI_THUE  =self.MA_HANG_ID.description

    @api.onchange('SO_LUONG')
    def update_THANH_TIEN(self):
        self.THANH_TIEN = self.DON_GIA * self.SO_LUONG
    
    @api.onchange('DON_GIA')
    def update_DON_GIA(self):
        self.THANH_TIEN = self.DON_GIA * self.SO_LUONG

    @api.onchange('MA_HANG_ID','DVT_ID')
    def onchange_dvt_id(self):
        if (self.MA_HANG_ID and self.DVT_ID):
            self.DON_GIA = self.MA_HANG_ID.compute_DON_GIA_BAN(self.DVT_ID.id)

    @api.onchange('PHAN_TRAM_THUE_GTGT_ID','THANH_TIEN')
    def update_THUE_GTGT(self):
        self.TIEN_THUE_GTGT = self.THANH_TIEN * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100
    @api.model
    def default_get(self, fields):
        rec = super(PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA, self).default_get(fields)
        # rec['TK_CO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '1561')],limit=1).id
        # rec['TK_THUE_GTGT_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '1331')],limit=1).id
        # rec['TK_KHO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '152')],limit=1).id
        # rec['KHO_ID'] = self.env['danh.muc.kho'].search([('MA_KHO', '=', 'KHH')],limit=1).id
        # rec['TK_TIEN_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '1111')],limit=1).id
        return rec

    # @api.onchange('LENH_SAN_XUAT_ID')
    # def onchange_THANH_PHAM(self):
    #     for record in self:
    #         record.THANH_PHAM_ID = record.LENH_SAN_XUAT_ID.STOCK_EX_LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_IDS.MA_HANG_ID