# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round
class PURCHASE_EX_HOP_DONG_MUA_CHI_TIET(models.Model):
    _name = 'purchase.ex.hop.dong.mua.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng', required=True)
    TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng', related='MA_HANG_ID.TEN')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đơn vị tính')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá', digits=decimal_precision.get_precision('DON_GIA'))
    THANH_TIEN = fields.Monetary(string='Thành tiền', help='Thành tiền', currency_field='currency_id')
    THANH_TIEN_QUY_DOI = fields.Monetary(string='Thành tiền quy đổi', help='Thành tiền quy đổi', currency_field='base_currency_id')
    TY_LE_CK = fields.Float(string='Tỷ lệ CK', help='Tỷ lệ ck')
    TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu', currency_field='currency_id')
    TIEN_CHIET_KHAU_QUY_DOI = fields.Monetary(string='Tiền chiết khấu quy đổi', help='Tiền chiết khấu quy đổi', currency_field='base_currency_id')
    PHAN_TRAM_THUE_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang', string='Phần trăm thuế GTGT', help='Phần trăm thuế gtgt')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế gtgt', currency_field='currency_id')
    TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='Tiền thuế GTGT quy đổi', help='Tiền thuế gtgt quy đổi', currency_field='base_currency_id')
    TONG_TIEN_THANH_TOAN = fields.Monetary(string='Tổng tiền thanh toán', help='Tổng tiền thanh toán', currency_field='currency_id')
    TONG_TIEN_THANH_TOAN_QUY_DOI = fields.Monetary(string='Tổng tiền thanh toán quy đổi', help='Tổng tiền thanh toán quy đổi', currency_field='base_currency_id')
    HOP_DONG_MUA_CHI_TIET_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang', string='Hợp đồng mua chi tiết', help='Hợp đồng mua chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name')

 
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='HOP_DONG_MUA_CHI_TIET_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)


    @api.onchange('SO_LUONG')
    def update_THANH_TIEN(self):
        self.THANH_TIEN = self.DON_GIA * self.SO_LUONG
    
    @api.onchange('DON_GIA')
    def update_DON_GIA(self):
        self.THANH_TIEN = self.DON_GIA * self.SO_LUONG

    @api.onchange('THANH_TIEN')
    def update_TIEN_CK(self):
        self.TIEN_CHIET_KHAU = self.THANH_TIEN * self.TY_LE_CK/100
        self.TONG_TIEN_THANH_TOAN = self.THANH_TIEN + self.TIEN_THUE_GTGT - self.TIEN_CHIET_KHAU
        self.TIEN_THUE_GTGT = (self.THANH_TIEN - self.TIEN_CHIET_KHAU)  * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100

    @api.onchange('PHAN_TRAM_THUE_GTGT_ID','TIEN_CHIET_KHAU')
    def update_THUE_GTGT(self):
        self.TIEN_THUE_GTGT = (self.THANH_TIEN - self.TIEN_CHIET_KHAU)  * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100

    @api.onchange('TY_LE_CK')
    def update_TIEN_CHIET_KHAU(self):
        self.TIEN_CHIET_KHAU = self.THANH_TIEN * self.TY_LE_CK/100

    @api.onchange('THANH_TIEN','TIEN_THUE_GTGT','TIEN_CHIET_KHAU')
    def update_TONG_TIEN_THANH_TOAN(self):
        self.TONG_TIEN_THANH_TOAN = self.THANH_TIEN + self.TIEN_THUE_GTGT - self.TIEN_CHIET_KHAU
        

    @api.onchange('THANH_TIEN','TIEN_THUE_GTGT','TIEN_CHIET_KHAU','TONG_TIEN_THANH_TOAN')
    def update_so_tien_quy_doi_details(self):
        self.THANH_TIEN_QUY_DOI = float_round(self.THANH_TIEN * self.currency_id.TY_GIA_QUY_DOI, 0)
        self.TIEN_THUE_GTGT_QUY_DOI = float_round(self.TIEN_THUE_GTGT * self.currency_id.TY_GIA_QUY_DOI, 0)
        self.TIEN_CHIET_KHAU_QUY_DOI = float_round(self.TIEN_CHIET_KHAU * self.currency_id.TY_GIA_QUY_DOI, 0)
        self.TONG_TIEN_THANH_TOAN_QUY_DOI = float_round(self.TONG_TIEN_THANH_TOAN * self.currency_id.TY_GIA_QUY_DOI, 0)


    @api.onchange('MA_HANG_ID')
    def onchange_product_id(self):
        for record in self:
            record.DON_GIA = record.MA_HANG_ID.DON_GIA_BAN
            record.SO_LUONG = 1
            record.PHAN_TRAM_THUE_GTGT_ID = record.MA_HANG_ID.THUE_SUAT_GTGT_ID
            record.name = record.MA_HANG_ID.TEN
            record.DVT_ID = record.MA_HANG_ID.DVT_CHINH_ID

    @api.onchange('MA_HANG_ID','DVT_ID')
    def onchange_dvt_id(self):
        if (self.MA_HANG_ID and self.DVT_ID):
            self.DON_GIA = self.MA_HANG_ID.compute_DON_GIA_BAN(self.DVT_ID.id)