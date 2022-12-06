# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_CHUNG_TU_NGHIEP_VU_KHAC_CONG_NO_THANH_TOAN(models.Model):
    _name = 'tong.hop.chung.tu.nghiep.vu.khac.cong.no.thanh.toan'
    _description = ''
    _inherit = ['mail.thread']


    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')

    LOAI_CHUNG_TU_ID = fields.Many2one('danh.muc.reftype',string='Loại chứng từ', help='Loại chứng từ')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_CONG_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK công nợ', help='Tk công nợ')

    MA_TAI_KHOAN = fields.Char(string='Mã tài khoản', help='Mã tài khoản' ,related='TK_CONG_NO_ID.SO_TAI_KHOAN', store=True)
    
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng')
    TY_GIA_TREN_CT = fields.Float(string='Tỷ giá trên CT', help='Tỷ giá trên ct')
    TY_GIA_DANH_GIA_LAI_GAN_NHAT = fields.Float(string='Tỷ giá đánh giá lại gần nhất', help='Tỷ giá đánh giá lại gần nhất')
    
    SO_CHUA_DOI_TRU = fields.Monetary(string='Số chưa đối trừ', help='Số chưa đối trừ', currency_field='currency_id')
    SO_CHUA_DOI_TRU_QUY_DOI = fields.Monetary(string='Số chưa đối trừ quy đổi', help='Số chưa đối trừ quy đổi', currency_field='base_currency_id')
    TY_GIA_DANH_GIA_LAI = fields.Float(string='Tỷ giá đánh giá lại', help='Tỷ giá đánh giá lại')
    DANH_GIA_LAI = fields.Monetary(string='Đánh giá lại', help='Đánh giá lại', currency_field='base_currency_id')
    CHENH_LECH = fields.Monetary(string='Chênh lệch', help='Chênh lệch', currency_field='base_currency_id')
    CHUNG_TU_NGHIEP_VU_KHAC_ID = fields.Many2one('account.ex.chung.tu.nghiep.vu.khac', string='Chứng từ nghiệp vụ khác', help='Chứng từ nghiệp vụ khác', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    ID_CHUNG_TU_GOC = fields.Integer(string='ID của chứng từ gốc', help='ID của chứng từ gốc')
    MODEL_CHUNG_TU_GOC = fields.Char(string='Model chứng từ gốc', help='Model chứng từ gốc')

    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='CHUNG_TU_NGHIEP_VU_KHAC_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)


    