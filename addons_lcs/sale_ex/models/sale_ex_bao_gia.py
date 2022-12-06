# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
class SALE_EX_BAO_GIA(models.Model):
    _name = 'sale.ex.bao.gia'
    _description = 'Báo giá'
    _inherit = ['mail.thread']
    _order = "NGAY_BAO_GIA desc, SO_BAO_GIA desc"


    KHACH_HANG_ID = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng', related='KHACH_HANG_ID', )
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    NGUOI_LIEN_HE = fields.Char(string='Người liên hệ', help='Người liên hệ')
    NV_MUA_HANG_ID = fields.Many2one('res.partner', string='NV bán hàng', help='Nhân viên bán hàng')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    SO_BAO_GIA = fields.Char(string='Số báo giá', help='Số báo giá', auto_num='sale_ex_bao_gia_SO_BAO_GIA')
    NGAY_BAO_GIA = fields.Date(string='Ngày báo giá', help='Ngày báo giá',default=fields.Datetime.now)
    HIEU_LUC_DEN = fields.Date(string='Hiệu lực đến', help='Hiệu lực đến')
    
    TIEN_HANG = fields.Monetary(string='Tiền hàng', help='Tiền hàng',compute='tinhtongtien',store=True, currency_field='currency_id')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế gtgt',compute='tinhtongtien',store=True, currency_field='currency_id')
    TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu',compute='tinhtongtien',store=True, currency_field='currency_id')
    TONG_TIEN = fields.Monetary(string='Tổng tiền', help='Tổng tiền',compute='tinhtongtien',store=True, currency_field='currency_id')
    GHI_CHU = fields.Char(string='Ghi chú', help='Ghi chú')
    name = fields.Char(string='name', help='name', related='SO_BAO_GIA',store=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    SALE_EX_BAO_GIA_CHI_TIET_IDS = fields.One2many('sale.ex.bao.gia.chi.tiet', 'BAO_GIA_CHI_TIET_ID', string='báo giá chi tiết', copy=True)
    

    THANH_TIEN_QUY_DOI = fields.Monetary(string='',help='Tiền hàng quy đổi',compute='tinhtongtien',store=True, currency_field='base_currency_id')
    TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='', help='Tiền thuế gtgt',compute='tinhtongtien',store=True, currency_field='base_currency_id')
    TIEN_CHIET_KHAU_QUY_DOI = fields.Monetary(string='',help='Tiền chiết khấu',compute='tinhtongtien',store=True, currency_field='base_currency_id')
    TONG_TIEN_QUY_DOI = fields.Monetary(string='',help='Tổng tiền',compute='tinhtongtien',store=True, currency_field='base_currency_id')
    PHAN_TRAM_THUE = fields.Float(string='phần trăm thuế GTGT', help='phần trăm thuế GTGT',compute='tinhtongtien',strore=True,digits=decimal_precision.get_precision('Product Price'))

    CONG_TIEN_TRU_CK = fields.Float(string='Cộng tiền hàng(đã trừ CK)', help='Cộng tiền hàng(đã trừ CK)',compute='tinhtongtien',store=True)
    TY_LE_CK_MT = fields.Float(string='Tỷ lệ CK', help='Tỷ lệ CK',compute='tinhtongtien',store=True)


    # currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    # LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền',default=True)
    
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, )
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')
    

    _sql_constraints = [
	('SO_BAO_GIA_uniq', 'unique ("SO_BAO_GIA")', 'Số chứng từ <<>> đã tồn tại, vui lòng nhập số chứng từ khác!'),
	]

    @api.model
    def default_get(self, fields): 
        rec = super(SALE_EX_BAO_GIA, self).default_get(fields)
      
        rec['KHACH_HANG_ID'] = self._context.get('default_KHACH_HANG_ID')
        rec['TEN_KHACH_HANG'] = self._context.get('default_TEN_KHACH_HANG')
        rec['DIA_CHI'] = self._context.get('default_DIA_CHI')
        rec['NGUOI_LIEN_HE'] = self._context.get('default_NGUOI_LIEN_HE')
        rec['NV_MUA_HANG_ID'] = self._context.get('default_NV_MUA_HANG_ID')
        
     
        return rec
    
    @api.model
    def create(self, values):
        result = super(SALE_EX_BAO_GIA, self).create(values)
        result['LOAI_CHUNG_TU'] = 3510
        return result
    

    @api.onchange('currency_id')
    def update_tygia(self):
        self.TY_GIA = self.currency_id.TY_GIA_QUY_DOI
    
    @api.onchange('TY_GIA')
    def update_thaydoiIsTy_gia(self):
        if self.TY_GIA == 1.0 :
            self.LA_TIEN_CO_SO = True
        else:
            self.LA_TIEN_CO_SO =False
        for line in self.SALE_EX_BAO_GIA_CHI_TIET_IDS:
            line.tinh_tien_quy_doi()
    
    @api.onchange('KHACH_HANG_ID')
    def update_kh(self):
        if self.KHACH_HANG_ID:
            self.TEN_KHACH_HANG = self.KHACH_HANG_ID.HO_VA_TEN
            self.DIA_CHI = self.KHACH_HANG_ID.DIA_CHI
            self.MA_SO_THUE = self.KHACH_HANG_ID.MA_SO_THUE
            self.NGUOI_LIEN_HE = self.KHACH_HANG_ID.HO_VA_TEN_LIEN_HE
            self.NV_MUA_HANG_ID = self.KHACH_HANG_ID.NHAN_VIEN_ID.id
    
    # @api.model
    # def default_get(self, fields):
    #     rec = super(SALE_EX_BAO_GIA, self).default_get(fields)
    #     rec['currency_id'] = self.env['res.currency'].search([('name','=','VND')]).id
    #     return rec

    @api.depends('SALE_EX_BAO_GIA_CHI_TIET_IDS')
    def tinhtongtien(self):
        for order in self:
            tong_tien_hang = tong_tien_thue_gtgt = tong_tien = tong_tien_chiet_khau =tong_tien_hang_quy_doi = tong_tien_thue_gtgt_quy_doi  = tong_tien_chiet_khau_quy_doi = tong_tien_quy_doi  = 0.0
            phan_tram_thue=0
            cong_tien_hang_ck=0
            ty_le_ck=0
            for line in order.SALE_EX_BAO_GIA_CHI_TIET_IDS:
                if line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT > phan_tram_thue:
                    phan_tram_thue= line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT
                tong_tien_hang += line.THANH_TIEN
                tong_tien_thue_gtgt += line.TIEN_THUE_GTGT
                tong_tien_chiet_khau += line.TIEN_CHIET_KHAU
                tong_tien = tong_tien_hang + tong_tien_thue_gtgt - tong_tien_chiet_khau

                tong_tien_hang_quy_doi += line.THANH_TIEN_QUY_DOI
                tong_tien_thue_gtgt_quy_doi += line.TIEN_THUE_GTGT_QUY_DOI
                tong_tien_chiet_khau_quy_doi += line.TIEN_CHIET_KHAU_QUY_DOI
                tong_tien_quy_doi = tong_tien_hang_quy_doi + tong_tien_thue_gtgt_quy_doi - tong_tien_chiet_khau_quy_doi
                cong_tien_hang_ck = tong_tien_hang - tong_tien_chiet_khau
            
            #ck master =tongtienchietkhau/tong_tien_hang *100                    
            if tong_tien_hang > 0:
                ty_le_ck = tong_tien_chiet_khau / tong_tien_hang* 100
            order.update({
                'TIEN_HANG': tong_tien_hang,
                'TIEN_THUE_GTGT': tong_tien_thue_gtgt,
                'TIEN_CHIET_KHAU': tong_tien_chiet_khau,
                'TONG_TIEN': tong_tien,

                'THANH_TIEN_QUY_DOI': tong_tien_hang_quy_doi,
                'TIEN_THUE_GTGT_QUY_DOI': tong_tien_thue_gtgt_quy_doi,
                'TIEN_CHIET_KHAU_QUY_DOI': tong_tien_chiet_khau_quy_doi,
                'TONG_TIEN_QUY_DOI': tong_tien_quy_doi,
                'CONG_TIEN_TRU_CK': cong_tien_hang_ck,
                'TY_LE_CK_MT': ty_le_ck,
                'PHAN_TRAM_THUE': phan_tram_thue,

            })