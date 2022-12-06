# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round

class sale_ex_tra_lai_hang_ban_chi_tiet(models.Model):
    _name = 'sale.ex.tra.lai.hang.ban.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']

    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng ', help='Mã hàng ', required=True)
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
    TK_TRA_LAI_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK trả lại', help='Tài khoản trả lại',related='TK_NO_ID', )
    TK_CONG_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK công nợ', help='Tài khoản công nợ',related='TK_CO_ID', )
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK nợ', help='Tài khoản nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK có', help='Tài khoản có')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đơn vị tính')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Monetary(string='Đơn giá', help='Đơn giá', currency_field='base_currency_id')
    THANH_TIEN = fields.Monetary(string='Thành tiền', help='Thành tiền', currency_field='currency_id')
    TY_LE_CK_PHAN_TRAM = fields.Float(string='Tỷ lệ CK (%)', help='Tỷ lệ chiết khấu phần trăm')
    TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu', currency_field='currency_id')
    TK_CHIET_KHAU = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chiết khấu', help='Tài khoản chiết khấu')
    SO_CHUNG_TU_ID = fields.Many2one('sale.document',string='Số CT bán hàng', help='Số chứng từ bán hàng')
    DIEN_GIAI_THUE = fields.Char(string='Diễn giải thuế', help='Diễn giải thuế')
    PHAN_TRAM_THUE_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang',string='% thuế GTGT', help='Phần trăm thuế giá trị gia tăng')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế giá trị gia tăng',  currency_field='currency_id')
    TK_THUE_GTGT_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK thuế GTGT', help='Tài khoản thuế GTGT')
    NHOM_HHDV_MUA_VAO_ID = fields.Many2one('danh.muc.nhom.hhdv', string='Nhóm HHDV mua vào', help='Nhóm hàng hóa mua vào', default=lambda self: self.lay_nhom_hhdv_mac_dinh())
    KHO_ID = fields.Many2one('danh.muc.kho', string='Kho', help='Kho')
    TK_KHO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK kho', help='Tài khoản kho')
    TK_GIA_VON_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK giá vốn', help='Tài khoản giá vốn')
    TIEN_VON = fields.Float(string='Tiền vốn', help='Tiền vốn', digits= decimal_precision.get_precision('Product Price'))
    SO_LO = fields.Float(string='Số lô', help='Số lô')
    HAN_SU_DUNG = fields.Date(string='Hạn sử dụng', help='Hạn sử dụng')
    LENH_SAN_XUAT = fields.Char(string='Lệnh sản xuất', help='Lệnh sản xuất')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng tổng hợp chi phí')
    MA_THONG_KE = fields.Many2one('danh.muc.ma.thong.ke',string='Mã thống kê', help='Mã thống kê')
    TK_TIEN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK tiền', help='Tài khoản tiền',related='TK_CO_ID', )
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    TRA_LAI_HANG_BAN_ID = fields.Many2one('sale.ex.tra.lai.hang.ban', string='Trả lại hàng hóa id', help='Trả lại hàng hóa id', ondelete='cascade')
    DON_GIA_VON = fields.Float(string='Đơn giá vốn', help='Đơn giá vốn',digits= decimal_precision.get_precision('DON_GIA'))
    THANH_TIEN_QUY_DOI = fields.Monetary(string='Thành tiền quy đổi', help='Thành tiền quy đổi', currency_field='base_currency_id')
    TIEN_CHIET_KHAU_QUY_DOI = fields.Monetary(string='Tiền chiết khấu quy đổi', help='Tiền chiết khấu quy đổi', currency_field='base_currency_id')
    TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='Tiền thuế GTGT quy đổi', help='Tiền thuế giá trị gia tăng quy đổi', currency_field='base_currency_id')
    BAN_HANG_CHI_TIET_ID = fields.Many2one('sale.document.line', string='Chứng từ bán hàng chi tiết', help='Tạo từ chứng từ bán hàng', store=False)

    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='TRA_LAI_HANG_BAN_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)

    TY_GIA_XUAT_QUY = fields.Float(string='Tỷ giá xuất quỹ', help='Tỷ giá xuất quỹ')
    THANH_TIEN_THEO_TY_GIA_XUAT_QUY = fields.Monetary(string='Tiền thanh toán theo TGXQ', help='Tiền thanh toán theo TGXQ', currency_field='base_currency_id')
    CHENH_LECH = fields.Float(string='Chênh lệch', help='Chênh lệch')
    TK_XU_LY_CHENH_LECH = fields.Many2one('danh.muc.he.thong.tai.khoan',string='TK xử lý chênh lệch', help='Tài khoản xử lý chênh lệch')
    HOA_DON_ID = fields.Many2one('purchase.ex.hoa.don.mua.hang', string='Hóa đơn', help='Hóa đơn mua hàng', ondelete='set null')
    PHIEU_NHAP_ID = fields.Many2one('stock.ex.nhap.xuat.kho', string='Phiếu nhập', ondelete='set null')
    LA_HANG_KHUYEN_MAI = fields.Boolean(string='Là hàng khuyến mại', help='IsPromotion')
    DON_DAT_HANG_CHI_TIET_ID = fields.Many2one('account.ex.don.dat.hang.chi.tiet', string='Đơn đặt hàng chi tiết', help='SAOrderRefDetailID')

    SO_LUONG_THEO_DVT_CHINH = fields.Float(string='Số lượng theo đvt chính', help='Số lượng theo đvt chính', digits=decimal_precision.get_precision('SO_LUONG'))
    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết',help='Thứ tự sắp xếp các dòng chi tiết')
    TIEN_THUE_GTGT_QUY_DOI_THEO_TGXQ = fields.Monetary(string='Tiền thuế GTGT quy đổi theo TGXQ', help='Tiền thuế giá trị gia tăng quy đổi theo tỷ giá xuất quỹ', currency_field='base_currency_id')

    CHENH_LECH_TIEN_THUE_GTGT = fields.Float(string='Chênh lệch tiền thuế giá trị gia tăng', help='Chênh lệch tiền thuế giá trị gia tăng')
    @api.onchange('MA_HANG_ID')
    def laythongtinsanpham(self):
        self.TEN_HANG = self.MA_HANG_ID.TEN
        self.DVT_ID = self.MA_HANG_ID.DVT_CHINH_ID
        self.SO_LUONG = 1
        self.DON_GIA = self.MA_HANG_ID.DON_GIA_BAN
        self.KHO_ID = self.MA_HANG_ID.KHO_NGAM_DINH_ID
        self.TK_KHO_ID = self.MA_HANG_ID.TAI_KHOAN_KHO_ID
        # self.TY_LE_CK_PHAN_TRAM = self.MA_HANG_ID.TY_LE_CHIET_KHAU_MUA_HANG
        self.PHAN_TRAM_THUE_GTGT_ID  =self.MA_HANG_ID.THUE_SUAT_GTGT_ID
        thuegtgt = 'Thue GTGT '
        self.DIEN_GIAI_THUE  = thuegtgt 

    @api.onchange('MA_HANG_ID','DVT_ID')
    def onchange_dvt_id(self):
        if (self.MA_HANG_ID and self.DVT_ID):
            self.DON_GIA = self.MA_HANG_ID.compute_DON_GIA_BAN(self.DVT_ID.id)
        
        

    # @api.model
    # def default_get(self, fields):
    #     rec = super(sale_ex_tra_lai_hang_ban_chi_tiet, self).default_get(fields)
        # rec['TK_TRA_LAI_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','5212')], limit=1).id
        # rec['TK_CO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','131')], limit=1).id
        # rec['TK_CHIET_KHAU'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','5211')], limit=1).id
        # rec['TK_THUE_GTGT_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','33311')], limit=1).id
        # tk_gia_von  = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','632')], limit=1)
        # if tk_gia_von:
        #     rec['TK_GIA_VON_ID'] = tk_gia_von.id

        # return rec

    @api.onchange('SO_LUONG')
    def update_THANH_TIEN(self):
        self.THANH_TIEN = self.DON_GIA * self.SO_LUONG
        self.TIEN_CHIET_KHAU = float_round(((self.TY_LE_CK_PHAN_TRAM * self.THANH_TIEN) / 100),0)
    
    @api.onchange('DON_GIA')
    def update_DON_GIA(self):
        self.THANH_TIEN = self.DON_GIA * self.SO_LUONG
        self.TIEN_CHIET_KHAU = (self.TY_LE_CK_PHAN_TRAM * self.THANH_TIEN) / 100
    
    @api.onchange('TY_LE_CK_PHAN_TRAM')
    def update_TIEN_CHIET_KHAU(self):
        self.TIEN_CHIET_KHAU = (self.TY_LE_CK_PHAN_TRAM * self.THANH_TIEN) / 100
        self.TIEN_THUE_GTGT = (self.THANH_TIEN - self.TIEN_CHIET_KHAU) * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100

    @api.onchange('PHAN_TRAM_THUE_GTGT_ID','THANH_TIEN','TIEN_CHIET_KHAU')
    def update_THUE_GTGT(self):
        self.TIEN_THUE_GTGT = (self.THANH_TIEN - self.TIEN_CHIET_KHAU) * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100

    @api.onchange('THANH_TIEN','TIEN_THUE_GTGT','TIEN_CHIET_KHAU')
    def update_so_tien_quy_doi_details(self):
        self.THANH_TIEN_QUY_DOI = float_round(self.THANH_TIEN * self.currency_id.TY_GIA_QUY_DOI, 0)
        self.TIEN_THUE_GTGT_QUY_DOI = float_round(self.TIEN_THUE_GTGT * self.currency_id.TY_GIA_QUY_DOI, 0)
        self.TIEN_CHIET_KHAU_QUY_DOI = float_round(self.TIEN_CHIET_KHAU * self.currency_id.TY_GIA_QUY_DOI, 0)