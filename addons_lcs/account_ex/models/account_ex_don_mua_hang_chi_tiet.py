# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round

class PURCHASE_EX_DON_MUA_HANG_CHI_TIET(models.Model):
    _name = 'purchase.ex.don.mua.hang.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng', compute='_compute_ma_hang', store=True)
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đvt')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_THEO_DVT_CHINH = fields.Float(string='Số lượng theo đvt chính', help='Số lượng theo đvt chính', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_NHAN = fields.Float(string='Số lượng nhận', help='Số lượng nhận', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits=decimal_precision.get_precision('DON_GIA'))
    DON_GIA_THEO_DVT_CHINH = fields.Float(string='Đơn giá theo đvt chính', help='Đơn giá theo đvt chính',digits=decimal_precision.get_precision('DON_GIA'))
    DON_GIA_SAU_THUE = fields.Float(string='Đơn giá sau thuế', help='Đơn giá sau thuế', digits=decimal_precision.get_precision('DON_GIA'))

    THANH_TIEN = fields.Monetary(string='Thành tiền', help='Thành tiền',currency_field='currency_id',digits=decimal_precision.get_precision('VND'))
    THANH_TIEN_QUY_DOI = fields.Monetary(string='Thành tiền quy đổi', help='Thành tiền quy đổi',currency_field='base_currency_id',digits=decimal_precision.get_precision('VND'))

    PHAN_TRAM_THUE_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang', string='Phần trăm thuế gtgt', help='Phần trăm thuế gtgt')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế gtgt',currency_field='currency_id',digits=decimal_precision.get_precision('VND'))
    TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='Tiền thuế GTGT quy đổi', help='Tiền thuế gtgt quy đổi',currency_field='base_currency_id')
    LENH_SAN_XUAT = fields.Char(string='Lệnh sản xuất', help='Lệnh sản xuất')
    THANH_PHAM = fields.Char(string='Thành phẩm', help='Thành phẩm')
    DON_MUA_HANG_CHI_TIET_ID = fields.Many2one('purchase.ex.don.mua.hang', string='Đơn mua hàng chi tiết', help='Đơn mua hàng chi tiết', ondelete='cascade')
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng', required=True)
    name = fields.Char(string='name', help='name')
    TY_LE_CHIET_KHAU = fields.Float(string='Tỷ lệ chiết khấu', help='Tỷ lệ chiết khấu')
    TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu',currency_field='currency_id')
    TIEN_CHIET_KHAU_QUY_DOI = fields.Monetary(string='Tiền chiết khấu quy đổi', help='Tiền chiết khấu quy đổi',currency_field='base_currency_id')


    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TY_LE_CHUYEN_DOI_RA_DVT_CHINH = fields.Float(string='Tỷ lệ chuyển đổi ra đvt chính', help='Tỷ lệ chuyển đổi ra đvt chính')
    TOAN_TU_QUY_DOI = fields.Selection([('NHAN', 'Nhân'), ('CHIA', 'Chia')], string='Toán tử quy đổi')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục CP', help='Khoản mục CP')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng THCP')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Hợp đồng bán')
    HOP_DONG_MUA_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang', string='Hợp đồng mua', help='Hợp đồng mua')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn vị')
    KHO_ID = fields.Many2one('danh.muc.kho', string='Kho')
    THU_TU_CAC_DONG_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết', help='Thứ tự sắp xếp các dòng chi tiết')
    
    # HOP_DONG_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang', string='Hợp đồng', help='Hợp đồng')
    
    
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='DON_MUA_HANG_CHI_TIET_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)

    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')

    SO_LUONG_NHAN_NAM_TRUOC = fields.Float(string='Số lượng nhận năm trước', help='Số lượng nhận năm trước', digits=decimal_precision.get_precision('SO_LUONG'))
    

    @api.onchange('SO_LUONG','DON_GIA')
    def update_THANH_TIEN(self):
        self.THANH_TIEN = self.DON_GIA * self.SO_LUONG
    

    @api.onchange('THANH_TIEN')
    def update_so_tien_quy_doi_details(self):
        self.THANH_TIEN_QUY_DOI = float_round(self.THANH_TIEN * self.currency_id.TY_GIA_QUY_DOI , 0)
        self.TIEN_THUE_GTGT = self.THANH_TIEN * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100
        if self.SO_LUONG > 0:
            self.DON_GIA = self.THANH_TIEN/self.SO_LUONG
        

    @api.onchange('TIEN_THUE_GTGT')
    def _onchange_TIEN_THUE_GTGT(self):
        self.TIEN_THUE_GTGT_QUY_DOI = float_round(self.TIEN_THUE_GTGT * self.currency_id.TY_GIA_QUY_DOI,0)

    @api.onchange('PHAN_TRAM_THUE_GTGT_ID')
    def update_THUE_GTGT(self):
        self.TIEN_THUE_GTGT = self.THANH_TIEN * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100

    # @api.onchange('MA_HANG_ID')
    # def laythongtinsanpham(self):
    #     self.TEN_HANG = self.MA_HANG_ID.TEN
    #     self.DVT_ID = self.MA_HANG_ID.DVT_CHINH_ID
    #     self.SO_LUONG = 1
    #     self.DON_GIA = self.MA_HANG_ID.DON_GIA_BAN
    #     self.PHAN_TRAM_THUE_GTGT_ID  =self.MA_HANG_ID.THUE_SUAT_GTGT_ID


    @api.onchange('MA_HANG_ID')
    def onchange_product_id(self):
        for record in self:
            record.DON_GIA = record.MA_HANG_ID.DON_GIA_BAN
            record.SO_LUONG = 1
            record.PHAN_TRAM_THUE_GTGT_ID = record.MA_HANG_ID.THUE_SUAT_GTGT_ID
            record.TEN_HANG = record.MA_HANG_ID.TEN
            record.DVT_ID = record.MA_HANG_ID.DVT_CHINH_ID

    @api.onchange('MA_HANG_ID','DVT_ID')
    def onchange_dvt_id(self):
        if (self.MA_HANG_ID and self.DVT_ID):
            self.DON_GIA = self.MA_HANG_ID.compute_DON_GIA_BAN(self.DVT_ID.id)

    @api.depends('MA_HANG_ID')
    def _compute_ma_hang(self):
        for record in self:
            record.TEN_HANG = record.MA_HANG_ID.TEN
            


    