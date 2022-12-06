# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round

class SALE_EX_CHI_TIET_HOA_DON_BAN_HANG(models.Model):
    _name = 'sale.ex.chi.tiet.hoa.don.ban.hang'
    _description = ''
    _inherit = ['mail.thread']
    
    MA_HANG_ID  = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng')
    TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đơn vị tính')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits= decimal_precision.get_precision('DON_GIA'))
    THANH_TIEN = fields.Monetary(string='Thành tiền', help='Thành tiền', currency_field='currency_id')
    THANH_TIEN_QUY_DOI = fields.Monetary(string='Thành tiền quy đổi', help='Thành tiền quy đổi', currency_field='base_currency_id')
    TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='Tiền thuế GTGT quy đổi', help='Tiền thuế GTGT quy đổi', currency_field='base_currency_id')
    TIEN_CHIET_KHAU_QUY_DOI = fields.Monetary(string='Tiền chiết khấu quy đổi', help='Tiền chiết khấu quy đổi', currency_field='base_currency_id')
    TY_LE_CK = fields.Float(string='Tỉ lệ CK (%)', help='Tỉ lệ chiết khấu')
    TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu', currency_field='currency_id')
    THUE_GTGT = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang',string='% thuế GTGT', help='Thuế giá trị gia tăng')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế giá trị gia tăng', currency_field='currency_id')
    HOA_DON_ID_ID = fields.Many2one('sale.ex.hoa.don.ban.hang', string='Hóa đơn id', help='Hóa đơn id', ondelete='cascade')
    # trường này chỉ có tác dụng trên form không cần import
    CHUNG_TU_BAN_HANG_ID = fields.Many2one('sale.document', string='Chứng từ bán hàng', help='Chứng từ bán hàng')

    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='HOA_DON_ID_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá',related='HOA_DON_ID_ID.TY_GIA', store=True)
    LA_HANG_KHUYEN_MAI = fields.Boolean(string='Là hàng khuyến mại', help='IsPromotion')
    TK_THUE_GTGT_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK thuế GTGT', help='Tài khoản thuế GTGT')

    @api.onchange('THANH_TIEN','TIEN_THUE_GTGT','TIEN_CHIET_KHAU','TY_GIA')
    def on_change_tinh_tien_quy_doi(self):
        for record in self:
            record.tinh_tien_quy_doi()

    def tinh_tien_quy_doi(self):        
        self.THANH_TIEN_QUY_DOI = float_round(self.THANH_TIEN * self.TY_GIA,0)
        self.TIEN_THUE_GTGT_QUY_DOI = float_round(self.TIEN_THUE_GTGT * self.TY_GIA,0)
        self.TIEN_CHIET_KHAU_QUY_DOI = float_round(self.TIEN_CHIET_KHAU * self.TY_GIA,0)
        



    # @api.onchange('THANH_TIEN','TIEN_THUE_GTGT','TIEN_CHIET_KHAU')
    # def update_quy_doi_gia_tri_details(self):
    #     self.THANH_TIEN_QUY_DOI = self.THANH_TIEN * self.currency_id.TY_GIA_QUY_DOI
    #     self.TIEN_THUE_GTGT_QUY_DOI = self.TIEN_THUE_GTGT * self.currency_id.TY_GIA_QUY_DOI
    #     self.TIEN_CHIET_KHAU_QUY_DOI = self.TIEN_CHIET_KHAU * self.currency_id.TY_GIA_QUY_DOI

    @api.onchange('MA_HANG_ID')
    def laythongtinsanpham(self):
        self.TEN_HANG = self.MA_HANG_ID.TEN
        self.DVT_ID = self.MA_HANG_ID.DVT_CHINH_ID
        self.SO_LUONG = 1
        self.DON_GIA = self.MA_HANG_ID.DON_GIA_BAN
        self.TY_LE_CK = self.MA_HANG_ID.TY_LE_CKMH
        self.THUE_GTGT  =self.MA_HANG_ID.THUE_SUAT_GTGT_ID

    @api.onchange('MA_HANG_ID','DVT_ID')
    def onchange_dvt_id(self):
        if (self.MA_HANG_ID and self.DVT_ID):
            self.DON_GIA = self.MA_HANG_ID.compute_DON_GIA_BAN(self.DVT_ID.id)
    

    @api.onchange('SO_LUONG','DON_GIA')
    def update_THANH_TIEN(self):
        self.THANH_TIEN = self.DON_GIA * self.SO_LUONG
        # self.TIEN_CHIET_KHAU = (self.TY_LE_CK * self.THANH_TIEN) / 100
    
    # @api.onchange('DON_GIA')
    # def update_DON_GIA(self):
    #     self.THANH_TIEN = self.DON_GIA * self.SO_LUONG
    #     self.TIEN_CHIET_KHAU = (self.TY_LE_CK * self.THANH_TIEN) / 100

    @api.onchange('TY_LE_CK','THANH_TIEN')
    def update_TIEN_CHIET_KHAU(self):
        self.TIEN_CHIET_KHAU = (self.TY_LE_CK * self.THANH_TIEN) / 100
        # self.TIEN_THUE_GTGT = (self.THANH_TIEN - self.TIEN_CHIET_KHAU) * self.THUE_GTGT.PHAN_TRAM_THUE_GTGT / 100

    @api.onchange('THUE_GTGT','THANH_TIEN','TIEN_CHIET_KHAU')
    def update_THUE_GTGT(self):
        self.TIEN_THUE_GTGT = (self.THANH_TIEN - self.TIEN_CHIET_KHAU) * self.THUE_GTGT.PHAN_TRAM_THUE_GTGT / 100
         

    
        


