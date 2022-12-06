# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class PURCHASE_EX_NHAN_HOA_DON_MUA_HANG_HOA_CHI_TIET(models.Model):
    _name = 'purchase.ex.hoa.don.mua.hang.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', required=True)
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
    TK_THUE_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK thuế', help='Tài khoản thuế')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK công nợ', help='Tài khoản công nợ')
    GIA_TRI_HHDV_CHUA_THUE = fields.Monetary(string='Giá trị HHDV chưa thuế', help='Giá trị hàng hóa dịch vụ chưa thuế', currency_field='currency_id')
    DIEN_GIAI_THUE = fields.Char(string='Diễn giải thuế', help='Diễn giải thuế')
    PHAN_TRAM_THUE_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang', string='% thuế GTGT', help='Phần trăm thuế giá trị gia tăng')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế giá trị gia tăng',compute='laytienthuegtgt', currency_field='currency_id', store=True)
    NHOM_HHDV_MUA_VAO_ID = fields.Many2one('danh.muc.nhom.hhdv', string='Nhóm HHDV mua vào', help='Nhóm hàng hóa dịch vụ mua vào', default=lambda self: self.lay_nhom_hhdv_mac_dinh())
    DON_MUA_HANG_ID = fields.Many2one('purchase.ex.don.mua.hang', string='Đơn mua hàng', help='Đơn mua hàng')
    SO_CHUNG_TU_ID = fields.Many2one('purchase.document',string='Số CT mua hàng', help='Số chứng từ mua hàng')
    SO_CHUNG_TU_MUA_HANG = fields.Char(string='Số CT mua hàng', help='Số CT mua hàng')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    HOP_DONG_MUA_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang', string='Hợp đồng mua', help='Hợp đồng mua')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    HOA_DON_MUA_HANG_ID = fields.Many2one('purchase.ex.hoa.don.mua.hang', string='Nhận hóa đơn hàng hóa', help='Nhận hóa đơn hàng hóa', ondelete='cascade')
    GIA_TRI_HHDV_CHUA_THUE_QUY_DOI = fields.Monetary(string='Giá trị HHDV chưa thuế quy đổi', help='Giá trị HHDV chưa thuế quy đổi', currency_field='base_currency_id',compute='tinh_tien_quy_doi', store=True)
    TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế giá trị gia tăng', currency_field='base_currency_id',compute='tinh_tien_quy_doi', store=True)
    ID_CHUNG_TU_GOC = fields.Many2one('purchase.document', string='ID chứng từ gốc', help='ID chứng từ gốc')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')


    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='HOA_DON_MUA_HANG_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)

    CHUNG_TU_MUA_HANG_CHI_TIET_ID = fields.Many2one('purchase.document.line', string='Chứng từ mua hàng chi tiết', help='PUVoucherRefDetailID')
    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết',help='Thứ tự sắp xếp các dòng chi tiết')
    @api.depends('GIA_TRI_HHDV_CHUA_THUE','PHAN_TRAM_THUE_GTGT_ID')
    def laytienthuegtgt(self):
        for record in self:
            record.TIEN_THUE_GTGT =  (record.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT * record.GIA_TRI_HHDV_CHUA_THUE) / 100
    
    @api.onchange('MA_HANG_ID')
    def _onchange_MA_HANG_ID(self):
        self.TEN_HANG = self.MA_HANG_ID.TEN

    @api.depends('TIEN_THUE_GTGT','GIA_TRI_HHDV_CHUA_THUE')
    def tinh_tien_quy_doi(self):
        for record in self:
            record.TIEN_THUE_GTGT_QUY_DOI =  record.TIEN_THUE_GTGT*record.HOA_DON_MUA_HANG_ID.TY_GIA
            record.GIA_TRI_HHDV_CHUA_THUE_QUY_DOI =  record.GIA_TRI_HHDV_CHUA_THUE*record.HOA_DON_MUA_HANG_ID.TY_GIA
