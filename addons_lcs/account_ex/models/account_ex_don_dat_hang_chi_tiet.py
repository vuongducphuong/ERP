# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.tools.float_utils import float_round
from odoo.addons import decimal_precision

class ACCOUNT_EX_DON_DAT_HANG_CHI_TIET(models.Model):
    _name = 'account.ex.don.dat.hang.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng', required=True)
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đvt')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_DA_GIAO = fields.Float(string='Số lượng đã giao', help='Số lượng đã giao', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá', digits=decimal_precision.get_precision('DON_GIA'))
    THANH_TIEN = fields.Monetary(string='Thành tiền', help='Thành tiền', currency_field='currency_id')
    THANH_TIEN_QUY_DOI = fields.Monetary(string='Thành tiền quy đổi', help='Thành tiền quy đổi', currency_field='base_currency_id')
    PHAN_TRAM_THUE_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang', string='Phần trăm thuế GTGT', help='Phần trăm thuế gtgt')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế gtgt', currency_field='currency_id')
    TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='Tiền thuế GTGT quy đổi', help='Tiền thuế gtgt quy đổi', currency_field='base_currency_id')
    DON_DAT_HANG_CHI_TIET_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng chi tiết', help='Đơn đặt hàng chi tiết', ondelete='cascade')
    name = fields.Char(string='name', help='name')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá',related='DON_DAT_HANG_CHI_TIET_ID.TY_GIA', store=True)
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị',related='DON_DAT_HANG_CHI_TIET_ID.NV_BAN_HANG_ID.DON_VI_ID', store=True)


    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='DON_DAT_HANG_CHI_TIET_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)

    TOAN_TU_QUY_DOI = fields.Selection([('0', 'nhân'), ('1', 'chia')], string='ExchangeRateOperator', compute='_compute_ty_le_chuyen_doi', store=True) # trường này bên dữ liệu tham khảo đều bằng nhân nên tính theo bên mình dữ liệu có thể không khớp với dữ liệu tham khảo (đã check với a quân)
    TY_LE_CHUYEN_DOI_THEO_DVT_CHINH = fields.Float(string='Tỷ lệ chuyển đổi theo đvt chính', help='Tỷ lệ chuyển đổi theo đvt chính', compute='_compute_ty_le_chuyen_doi', store=True) # trường này bên dữ liệu tham khảo đều bằng 1 nên tính theo bên mình có thể không khớp với bên misa (đã check với a quân)

    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê') # trường này bên dữ liệu tham khảo đều bằng null nên tạo thời chưa tính (đã check với a quân)
    MA_KHO_ID = fields.Many2one('danh.muc.kho', string='Mã kho', help='Mã kho',related='MA_HANG_ID.KHO_NGAM_DINH_ID', store=True)

    SO_LUONG_DA_GIAO_NAM_TRUOC_BAN_HANG = fields.Float(string='Số lượng đã giao năm trước bán hàng', help='QuantityDeliveredSALastYear', digits=decimal_precision.get_precision('SO_LUONG')) #trường này chưa biết cập nhật thế nào
    SO_LUONG_DA_GIAO_NAM_TRUOC_BAN_HANG_THEO_DVT_CHINH = fields.Float(string='Số lượng đã giao năm trước bán hàng', help='MainQuantityDeliveredSALastYear', digits=decimal_precision.get_precision('SO_LUONG'))  # trường này chưa biết cập nhật thế nào
    SO_LUONG_DA_GIAO_NAM_TRUOC_PX = fields.Float(string='Số lượng đã giao năm trước phiếu xuất', help='QuantityDeliveredINLastYear', digits=decimal_precision.get_precision('SO_LUONG')) # trường này chưa biết cập nhật thế nào
    SO_LUONG_DA_GIAO_BAN_HANG = fields.Float(string='Số lượng đã giao bán hàng', help='QuantityDeliveredSA', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_DA_GIAO_BAN_HANG_THEO_DVT_CHINH = fields.Float(string='Số lượng đã giao bán hàng', help='MainQuantityDeliveredSA', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_DA_GIAO_PX = fields.Float(string='Số lượng đã giao phiếu xuất', help='QuantityDeliveredIN', digits=decimal_precision.get_precision('SO_LUONG'))

    TIEN_CHIET_KHAU_QUY_DOI = fields.Float(string='Số tiền chiết khấu quy đổi', help='DiscountAmount')
    SO_TIEN_QUY_DOI_DA_GIAO_NAM_TRUOC = fields.Float(string='Số tiền quy đổi đã giao năm trước', help='LastYearDeliveredAmount')
    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết',help='Thứ tự sắp xếp các dòng chi tiết')
    LA_HANG_KHUYEN_MAI = fields.Boolean(string='Là hàng khuyến mại', help='IsPromotion')
    PHAN_TRAM_CHIET_KHAU = fields.Float(string='Chiết khấu', help='DiscountRate')
    TIEN_CHIET_KHAU = fields.Float(string='Số tiền chiết khấu', help='DiscountAmountOC')
    sequence = fields.Integer()
    
    @api.depends('MA_HANG_ID','DVT_ID')
    def _compute_ty_le_chuyen_doi(self):
        for record in self:
            if record.MA_HANG_ID:
                if record.MA_HANG_ID.DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI_IDS:
                    for dv_chuyen_doi in record.MA_HANG_ID.DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI_IDS:
                        if dv_chuyen_doi.DVT_ID.id == record.DVT_ID.id: 
                            record.TY_LE_CHUYEN_DOI_THEO_DVT_CHINH = dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                            if dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_CHIA':
                                record.TOAN_TU_QUY_DOI = '1'
                            else:
                                record.TOAN_TU_QUY_DOI = '0'
                        else:
                            record.TY_LE_CHUYEN_DOI_THEO_DVT_CHINH = 1


    @api.onchange('SO_LUONG')
    def update_THANH_TIEN(self):
        self.THANH_TIEN = self.DON_GIA * self.SO_LUONG
    
    @api.onchange('DON_GIA')
    def update_DON_GIA(self):
        self.THANH_TIEN = self.DON_GIA * self.SO_LUONG

    @api.onchange('THANH_TIEN','TIEN_THUE_GTGT')
    def update_so_tien_quy_doi_details(self):
        for record in self:
            record.tinh_tien_quy_doi()

    def tinh_tien_quy_doi(self):        
        self.THANH_TIEN_QUY_DOI = float_round(self.THANH_TIEN * self.TY_GIA , 0)
        self.TIEN_THUE_GTGT_QUY_DOI = float_round(self.TIEN_THUE_GTGT * self.TY_GIA,0)

    @api.onchange('PHAN_TRAM_THUE_GTGT_ID','THANH_TIEN')
    def update_THUE_GTGT(self):
        self.TIEN_THUE_GTGT = self.THANH_TIEN * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100

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
            