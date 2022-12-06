# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round

class SALE_EX_CHI_TIET_GIAM_GIA_HANG_BAN(models.Model):
    _name = 'sale.ex.chi.tiet.giam.gia.hang.ban'
    _description = ''
    _inherit = ['mail.thread']
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng', required=True)
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
    TK_GIAM_GIA_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK giảm giá', help='Tài khoản giảm giá')
    TK_TIEN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK tiền', help='Tài khoản tiền' )
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK nợ', help='Tài khoản nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK có', help='Tài khoản có')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đơn vị tính')
    SO_LUONG = fields.Float(string='Số lượng ', help='Số lượng ', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits=decimal_precision.get_precision('DON_GIA'))
    THANH_TIEN = fields.Monetary(string='Thành tiền', help='Thành tiền', currency_field='currency_id',digits=decimal_precision.get_precision('VND'))
    TY_LE_CHIET_KHAU_PHAN_TRAM = fields.Float(string='Tỷ lệ chiết khấu (%)', help='Tỷ lệ chiết khấu phần trăm')
    TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu', currency_field='currency_id',digits=decimal_precision.get_precision('VND'))
    TK_CHIET_KHAU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chiết khấu', help='Tài khoản chiết khấu')
    DIEN_GIAI_THUE = fields.Char(string='Diễn giải thuế', help='Diễn giải thuế')
    PHAN_TRAM_THUE_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang', string='% thuế GTGT', help='Phần trăm thuế giá trị gia tăng')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế giá trị gia tăng', currency_field='currency_id',digits=decimal_precision.get_precision('VND'))
    TK_THUE_GTGT_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK thuế GTGT', help='Tài khoản thuế giá trị gia tăng')
    SO_CHUNG_TU_BAN_HANG = fields.Many2one('sale.document',string='Số CT bán hàng', help='Số chứng từ bán hàng')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng tổng hợp chi phí')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    GIAM_GIA_HANG_BAN_ID = fields.Many2one('sale.ex.giam.gia.hang.ban', string='Chi tiết giảm giá hàng bán ids', help='Chi tiết giảm giá hàng bán ids', ondelete='cascade')
    GHI_CHU = fields.Char(string='Ghi chú', help='Ghi chú')
    THANH_TIEN_QUY_DOI = fields.Monetary(string='Thành tiền quy đổi', help='Thành tiền quy đổi', currency_field='base_currency_id')
    TIEN_CHIET_KHAU_QUY_DOI = fields.Monetary(string='Tiền chiết khấu quy đổi', help='Tiền chiết khấu quy đổi', currency_field='base_currency_id')
    TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='Tiền thuế GTGT quy đổi', help='Tiền thuế GTGT quy đổi', currency_field='base_currency_id')
    CHUNG_TU_BAN_HANG_ID = fields.Many2one('sale.document', string='Chứng từ bán hàng', help='Chứng từ bán hàng')

    TY_GIA_XUAT_QUY = fields.Float(string='Tỷ giá xuất quỹ', help='Tỷ giá xuất quỹ')
    THANH_TIEN_THEO_TY_GIA_XUAT_QUY = fields.Float(string='Thành tiền theo TGXQ', help='Thành tiền sau chiết khấu theo tỷ giá xuất quỹ')
    CHENH_LECH = fields.Float(string='Chênh lệch', help='Chênh lệch')
    TK_XU_LY_CHENH_LECH = fields.Many2one('danh.muc.he.thong.tai.khoan',string='TK xử lý chênh lệch', help='Tài khoản xử lý chênh lệch')

    TIEN_THUE_GTGT_THEO_TGXQ = fields.Monetary(string='Tiền thuế GTGT theo TGXQ', help='Tiền thuế giá trị gia tăng theo tỷ giá xuất quỹ', currency_field='base_currency_id')
    CHENH_LECH_TIEN_THUE_GTGT = fields.Monetary(string='Chênh lệch tiền thuế GTGT', help='Chênh lệch tiền thuế giá trị gia tăng', currency_field='base_currency_id')


    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='GIAM_GIA_HANG_BAN_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)
    
    HOA_DON_BAN_HANG_ID = fields.Many2one('sale.ex.hoa.don.ban.hang', string='Hóa đơn bán hàng', help='SAInvoiceRefID')
    DON_DAT_HANG_CHI_TIET_ID = fields.Many2one('account.ex.don.dat.hang.chi.tiet', string='Đơn đặt hàng chi tiết', help='SAOrderRefDetailID')
    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết',help='Thứ tự sắp xếp các dòng chi tiết')
    @api.onchange('THANH_TIEN','TIEN_THUE_GTGT','TIEN_CHIET_KHAU')
    def update_quy_doi_gia_tri_details(self):
        self.THANH_TIEN_QUY_DOI = float_round(self.THANH_TIEN * self.currency_id.TY_GIA_QUY_DOI,0)
        self.TIEN_THUE_GTGT_QUY_DOI = float_round(self.TIEN_THUE_GTGT * self.currency_id.TY_GIA_QUY_DOI,0)
        self.TIEN_CHIET_KHAU_QUY_DOI = float_round(self.TIEN_CHIET_KHAU * self.currency_id.TY_GIA_QUY_DOI,0)

    @api.onchange('MA_HANG_ID')
    def laythongtinsanpham(self):
        self.TEN_HANG = self.MA_HANG_ID.TEN
        self.DVT_ID = self.MA_HANG_ID.DVT_CHINH_ID
        self.SO_LUONG = 1
        self.DON_GIA = self.MA_HANG_ID.DON_GIA_BAN
        # self.TY_LE_CHIET_KHAU_PHAN_TRAM = self.MA_HANG_ID.TY_LE_CHIET_KHAU_MUA_HANG
        self.PHAN_TRAM_THUE_GTGT_ID  =self.MA_HANG_ID.THUE_SUAT_GTGT_ID
        if self.PHAN_TRAM_THUE_GTGT_ID:
            self.TIEN_THUE_GTGT = self.THANH_TIEN * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100
        thuegtgt = 'Thuế GTGT - '
        self.DIEN_GIAI_THUE  = thuegtgt + str(self.MA_HANG_ID.TEN)

    @api.model
    def default_get(self, fields):
        rec = super(SALE_EX_CHI_TIET_GIAM_GIA_HANG_BAN, self).default_get(fields)
        # rec['TK_TRA_LAI_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('code','=','5212')], limit=1).id
        # rec['TAI_KHOAN_CONG_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','131')], limit=1).id
        rec['TK_CHIET_KHAU_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','5211')], limit=1).id
        rec['TK_THUE_GTGT_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','33311')], limit=1).id
        rec['TK_GIAM_GIA_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','331')], limit=1).id

        return rec

    @api.onchange('MA_HANG_ID','DVT_ID')
    def onchange_dvt_id(self):
        if (self.MA_HANG_ID and self.DVT_ID):
            self.DON_GIA = self.MA_HANG_ID.compute_DON_GIA_BAN(self.DVT_ID.id)

    @api.onchange('SO_LUONG')
    def update_THANH_TIEN(self):
        self.THANH_TIEN = self.DON_GIA * self.SO_LUONG
        self.TIEN_CHIET_KHAU = (self.TY_LE_CHIET_KHAU_PHAN_TRAM * self.THANH_TIEN) / 100
    
    @api.onchange('DON_GIA')
    def update_DON_GIA(self):
        self.THANH_TIEN = self.DON_GIA * self.SO_LUONG
        self.TIEN_CHIET_KHAU = (self.TY_LE_CHIET_KHAU_PHAN_TRAM * self.THANH_TIEN) / 100

    @api.onchange('THANH_TIEN')
    def _onchange_THANH_TIEN(self):
        if self.SO_LUONG:
            self.DON_GIA = self.THANH_TIEN/self.SO_LUONG
        if self.PHAN_TRAM_THUE_GTGT_ID:
            self.TIEN_THUE_GTGT = self.THANH_TIEN * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100
    
    @api.onchange('TY_LE_CHIET_KHAU_PHAN_TRAM','THANH_TIEN','PHAN_TRAM_THUE_GTGT_ID','TIEN_CHIET_KHAU')
    def update_TIEN_CHIET_KHAU(self):
        self.TIEN_CHIET_KHAU = (self.TY_LE_CHIET_KHAU_PHAN_TRAM * self.THANH_TIEN) / 100
        self.TIEN_THUE_GTGT = (self.THANH_TIEN - self.TIEN_CHIET_KHAU) * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100

    @api.onchange('PHAN_TRAM_THUE_GTGT_ID')
    def update_THUE_GTGT(self):
        self.TIEN_THUE_GTGT = self.THANH_TIEN * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100

    