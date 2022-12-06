# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round

class PURCHASE_EX_GIAM_GIA_HANG_MUA_CHI_TIET(models.Model):
    _name = 'purchase.ex.giam.gia.hang.mua.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa',string='Mã hàng', help='Mã hàng', required=True)
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK nợ', help='TK nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK có', help='TK có')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh',string='ĐVT', help='Đơn vị tính')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits= decimal_precision.get_precision('DON_GIA'))
    DIEN_GIAI_THUE = fields.Char(string='Diễn giải thuế', help='Diễn giải thuế')
    PHAN_TRAM_THUE_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang',string='% thuế GTGT', help='Phần trăm thuế giá trị gia tăng')
    TK_THUE_GTGT_ID = fields.Many2one('danh.muc.he.thong.tai.khoan',string='TK thuế GTGT', help='Tài khoản thuế GTGT')
    NHOM_HHDV_MUA_VAO_ID = fields.Many2one('danh.muc.nhom.hhdv',string='Nhóm HHDV mua vào', help='Nhóm hàng hóa dịch vụ mua vào', default=lambda self: self.lay_nhom_hhdv_mac_dinh())
    SO_LO = fields.Char(string='Số lô', help='Số lô')
    HAN_SU_DUNG = fields.Date(string='Hạn sử dụng', help='Hạn sử dụng')
    SO_CHUNG_TU = fields.Many2one('purchase.document',string='Số CT mua hàng', help='Số chứng từ mua hàng')
    SO_HD_MUA_HANG = fields.Char(string='Số HĐ mua hàng', help='Số hóa đơn mua hàng')
    NGAY_HD_MUA_HANG = fields.Date(string='Ngày HĐ mua hàng', help='Ngày hóa đơn mua hàng')
    KHO_ID = fields.Many2one('danh.muc.kho', string='Kho', help='Kho')
    TK_KHO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan',string='TK kho', help='Tài khoản kho',related='TK_CO_ID', )
    HOP_DONG_MUA_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang', string='Hợp đồng mua', help='Hợp đồng mua')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke',string='Mã thống kê', help='Mã thống kê')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục CP', help='Khoản mục chi phí')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng tổng hợp chi phí')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang',string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban',string='Hợp đồng bán', help='Hợp đồng bán')
    GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID = fields.Many2one('purchase.ex.giam.gia.hang.mua', string='Giảm giá hàng mua chi tiết id', help='Giảm giá hàng mua chi tiết id', ondelete='cascade')
    THANH_TIEN_QUY_DOI = fields.Monetary(string='Thành tiền quy đổi', help='Thành tiền quy đổi', currency_field='base_currency_id')
    TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='Tiền thuế GTGT quy đổi', help='Tiền thuế GTGT quy đổi', currency_field='base_currency_id')
    CHUNG_TU_MUA_HANG = fields.Many2one('purchase.document',string='Chứng từ mua hàng', help='Chứng từ mua hàng')
    THANH_TIEN_QUY_DOI = fields.Monetary(string='Thành tiền quy đổi', help='Thành tiền quy đổi', currency_field='base_currency_id')
    TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='Tiền thuế GTGT quy đổi', help='Tiền thuế GTGT quy đổi', currency_field='base_currency_id')
    THANH_TIEN = fields.Monetary(string='Thành tiền', help='Thành tiền', currency_field='currency_id')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế giá trị gia tăng', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)
    HOA_DON_ID = fields.Many2one('purchase.ex.hoa.don.mua.hang', string='Hóa đơn', )
    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết',help='Thứ tự sắp xếp các dòng chi tiết')
    @api.onchange('THANH_TIEN','TIEN_THUE_GTGT')
    def update_so_tien_quy_doi_details(self):
        self.THANH_TIEN_QUY_DOI = float_round(self.THANH_TIEN * self.currency_id.TY_GIA_QUY_DOI, 0)
        self.TIEN_THUE_GTGT_QUY_DOI = float_round(self.TIEN_THUE_GTGT * self.currency_id.TY_GIA_QUY_DOI, 0)

    @api.onchange('MA_HANG_ID')
    def laythongtinsanpham(self):
        if self.MA_HANG_ID:
            self.TEN_HANG = self.MA_HANG_ID.TEN
            self.DVT_ID = self.MA_HANG_ID.DVT_CHINH_ID
            self.SO_LUONG = 1
            self.PHAN_TRAM_THUE_GTGT_ID  =self.MA_HANG_ID.THUE_SUAT_GTGT_ID
            thuegtgt = 'Thuế GTGT - '+ str(self.MA_HANG_ID.TEN) if self.MA_HANG_ID.TEN else ""
            self.DIEN_GIAI_THUE  = thuegtgt
            self.KHO_ID = self.MA_HANG_ID.KHO_NGAM_DINH_ID

    @api.onchange('MA_HANG_ID','DVT_ID')
    def onchange_dvt_id(self):
        if (self.MA_HANG_ID and self.DVT_ID):
            self.DON_GIA = self.MA_HANG_ID.compute_DON_GIA_BAN(self.DVT_ID.id)

    @api.onchange('SO_LUONG','DON_GIA')
    def update_THANH_TIEN(self):
        self.THANH_TIEN = self.DON_GIA * self.SO_LUONG

    @api.onchange('THANH_TIEN')
    def _onchange_THANH_TIEN(self):
        if self.SO_LUONG:
            self.DON_GIA = self.THANH_TIEN/self.SO_LUONG
        self.TIEN_THUE_GTGT = self.THANH_TIEN * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100

    @api.onchange('PHAN_TRAM_THUE_GTGT_ID')
    def update_THUE_GTGT(self):
        self.TIEN_THUE_GTGT = self.THANH_TIEN * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100