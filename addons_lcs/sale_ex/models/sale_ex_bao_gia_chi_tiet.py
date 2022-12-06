# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.tools.float_utils import float_round
from odoo.addons import decimal_precision

class SALE_EX_BAO_GIA_CHI_TIET(models.Model):
    _name = 'sale.ex.bao.gia.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng', required=True)
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đvt')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá', digits=decimal_precision.get_precision('DON_GIA'))
    THANH_TIEN = fields.Monetary(string='Thành tiền', help='Thành tiền', currency_field='currency_id')
    THANH_TIEN_QUY_DOI = fields.Monetary(string='Thành tiền quy đổi', help='Thành tiền quy đổi', currency_field='base_currency_id')
    TY_LE_CK = fields.Float(string='Tỷ lệ CK', help='Tỷ lệ ck')
    TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu', currency_field='currency_id')
    TIEN_CHIET_KHAU_QUY_DOI = fields.Monetary(string='Tiền chiết khấu QĐ', help='Tiền chiết khấu quy đổi', currency_field='base_currency_id')
    PHAN_TRAM_THUE_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang', string='Phần trăm thuế GTGT', help='Phần trăm thuế gtgt')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế gtgt', currency_field='currency_id')
    TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='Tiền thuế GTGT quy đổi', help='Tiền thuế gtgt quy đổi', currency_field='base_currency_id')
    BAO_GIA_CHI_TIET_ID = fields.Many2one('sale.ex.bao.gia', string='Báo giá chi tiết', help='Báo giá chi tiết', ondelete='cascade')
    name = fields.Char(string='name', help='name')

    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='BAO_GIA_CHI_TIET_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)
    # currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền' ,related='BAO_GIA_CHI_TIET_ID.currency_id')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá',related='BAO_GIA_CHI_TIET_ID.TY_GIA', store=True)
    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết',help='Thứ tự sắp xếp các dòng chi tiết')
    LA_HANG_KHUYEN_MAI = fields.Boolean(string='Là hàng khuyến mại', help='IsPromotion')
    @api.onchange('SO_LUONG')
    def update_THANH_TIEN(self):
        self.THANH_TIEN = self.DON_GIA * self.SO_LUONG
    
    @api.onchange('DON_GIA')
    def update_DON_GIA(self):
        self.THANH_TIEN = self.DON_GIA * self.SO_LUONG

    @api.onchange('THANH_TIEN')
    def update_TIEN_CK(self):
        self.TIEN_CHIET_KHAU = self.THANH_TIEN * self.TY_LE_CK/100
        self.TIEN_THUE_GTGT = (self.THANH_TIEN - self.TIEN_CHIET_KHAU) * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100

    @api.onchange('PHAN_TRAM_THUE_GTGT_ID','TIEN_CHIET_KHAU')
    def update_THUE_GTGT(self):
        self.TIEN_THUE_GTGT = (self.THANH_TIEN - self.TIEN_CHIET_KHAU) * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100

    @api.onchange('TY_LE_CK')
    def update_TIEN_CHIET_KHAU(self):
        self.TIEN_CHIET_KHAU = self.THANH_TIEN * self.TY_LE_CK/100

    
        

    @api.onchange('THANH_TIEN','TIEN_THUE_GTGT','TIEN_CHIET_KHAU')
    def update_so_tien_quy_doi_details(self):
        for record in self:
            record.tinh_tien_quy_doi()
        
    def tinh_tien_quy_doi(self):
        self.THANH_TIEN_QUY_DOI = float_round(self.THANH_TIEN * self.TY_GIA, 0)
        self.TIEN_THUE_GTGT_QUY_DOI = float_round(self.TIEN_THUE_GTGT * self.TY_GIA, 0)
        self.TIEN_CHIET_KHAU_QUY_DOI = float_round(self.TIEN_CHIET_KHAU * self.TY_GIA, 0)        
        


    @api.onchange('MA_HANG_ID')
    def onchange_product_id(self):
        for record in self:
            record.TEN_HANG = record.MA_HANG_ID.TEN
            record.DON_GIA = record.MA_HANG_ID.DON_GIA_BAN
            record.SO_LUONG = 1
            record.PHAN_TRAM_THUE_GTGT_ID = record.MA_HANG_ID.THUE_SUAT_GTGT_ID
            record.name = record.MA_HANG_ID.TEN
            record.DVT_ID = record.MA_HANG_ID.DVT_CHINH_ID

    @api.onchange('MA_HANG_ID','DVT_ID')
    def onchange_dvt_id(self):
        if (self.MA_HANG_ID and self.DVT_ID):
            self.DON_GIA = self.MA_HANG_ID.compute_DON_GIA_BAN(self.DVT_ID.id)