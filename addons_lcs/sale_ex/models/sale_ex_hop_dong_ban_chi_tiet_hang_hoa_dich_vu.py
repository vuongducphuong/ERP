# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round
class SALE_EX_HOP_DONG_BAN_CHI_TIET_HANG_HOA_DICH_VU(models.Model):
    _name = 'sale.ex.hop.dong.ban.chi.tiet.hang.hoa.dich.vu'
    _description = ''
    _inherit = ['mail.thread']
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng')
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Đơn vị tính', help='Đơn vị tính')
    SO_LUONG_YEU_CAU = fields.Float(string='Số lượng yêu cầu', help='Số lượng yêu cầu', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_DA_GIAO = fields.Float(string='Số lượng đã giao', help='Số lượng đã giao', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits= decimal_precision.get_precision('DON_GIA'))
   
    
    TY_LE_CK = fields.Float(string='Tỷ lệ CK', help='Tỷ lệ ck')
   
    PHAN_TRAM_THUE_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang', string='Phần trăm thuế GTGT', help='Phần trăm thuế gtgt',digits= decimal_precision.get_precision('Product Price'))
    
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán', ondelete='cascade')

    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='HOP_DONG_BAN_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)
    # SO_TIEN = fields.Monetary(string='Số tiền', help='Số tiền', currency_field='currency_id')
    # QUY_DOI = fields.Monetary(string='Quy đổi', help='Quy đổi', currency_field='base_currency_id')

    THANH_TIEN = fields.Monetary(string='Thành tiền', help='Thành tiền', currency_field='currency_id')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế GTGT', currency_field='currency_id')
    TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu', currency_field='currency_id')
    THANH_TIEN_QUY_DOI = fields.Monetary(string='Thành tiền quy đổi', help='Thành tiền quy đổi', currency_field='base_currency_id')
    TIEN_CHIET_KHAU_QUY_DOI = fields.Monetary(string='Tiền chiết khấu quy đổi', help='Tiền chiết khấu quy đổi', currency_field='base_currency_id')
    TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='Tiền thuế GTGT quy đổi', help='Tiền thuế gtgt quy đổi', currency_field='base_currency_id')
    DON_GIA_QUY_DOI = fields.Monetary(string='Đơn giá quy đổi', help='Đơn giá quy đổi')

    TONG_TIEN = fields.Monetary(string='Tổng tiền', help='Tổng tiền', currency_field='currency_id')
    TONG_TIEN_QUY_DOI = fields.Monetary(string='Tổng tiền quy đổi', help='Tổng tiền  quy đổi', currency_field='base_currency_id')
    STT = fields.Integer(string='STT', help='STT')
    SO_LUONG_DA_GIAO_NAM_TRUOC = fields.Float(string='Số lượng đã giao năm trước', help='Số lượng đã giao năm trước')

    @api.onchange('MA_HANG_ID')
    def onchange_product_id(self):
        for record in self:
            record.DON_GIA = record.MA_HANG_ID.DON_GIA_BAN
            record.SO_LUONG_YEU_CAU = 1
            # record.PHAN_TRAM_THUE_GTGT_ID = record.MA_HANG_ID.THUE_SUAT_GTGT_ID
            record.TEN_HANG = record.MA_HANG_ID.TEN
            record.DVT_ID = record.MA_HANG_ID.DVT_CHINH_ID

    @api.onchange('SO_LUONG_YEU_CAU','DON_GIA')
    def update_thanh_tien(self):
        self.THANH_TIEN = self.SO_LUONG_YEU_CAU * self.DON_GIA

    @api.onchange('THANH_TIEN','PHAN_TRAM_THUE_GTGT_ID','TY_LE_CK','TIEN_CHIET_KHAU')
    def update_don_gia(self):
        self.DON_GIA = self.THANH_TIEN / self.SO_LUONG_YEU_CAU
        self.TIEN_CHIET_KHAU = self.THANH_TIEN * self.TY_LE_CK/100
        self.TIEN_THUE_GTGT = (self.THANH_TIEN - self.TIEN_CHIET_KHAU)  * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100

    @api.onchange('THANH_TIEN','TIEN_THUE_GTGT','TIEN_CHIET_KHAU','DON_GIA')
    def update_so_tien_quy_doi_details(self):
        self.THANH_TIEN_QUY_DOI = float_round(self.THANH_TIEN * self.currency_id.TY_GIA_QUY_DOI , 0)
        self.TIEN_THUE_GTGT_QUY_DOI = float_round(self.TIEN_THUE_GTGT * self.currency_id.TY_GIA_QUY_DOI, 0)
        self.TIEN_CHIET_KHAU_QUY_DOI = float_round(self.TIEN_CHIET_KHAU * self.currency_id.TY_GIA_QUY_DOI, 0)
        self.DON_GIA_QUY_DOI = float_round(self.DON_GIA * self.currency_id.TY_GIA_QUY_DOI, 0)
        
