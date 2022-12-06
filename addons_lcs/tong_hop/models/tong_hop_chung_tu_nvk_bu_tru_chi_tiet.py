# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_CHUNG_TU_NVK_BU_TRU_CHI_TIET(models.Model):
    _name = 'tong.hop.chung.tu.nvk.bu.tru.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    ID_CHUNG_TU = fields.Integer(string='Id chứng từ', help='Id chứng từ')
    ID_CHUNG_TU_THANH_TOAN = fields.Integer(string='Id chứng từ thanh toán', help='Id chứng từ thanh toán')
    LOAI_CHUNG_TU_THANH_TOAN_ID = fields.Many2one('danh.muc.loai.chung.tu', string='Loại chứng từ thanh toán', help='Loại chứng từ thanh toán')
    NGAY_CHUNG_TU_THANH_TOAN = fields.Date(string='Ngày chứng từ thanh toán', help='Ngày chứng từ thanh toán')
    NGAY_HACH_TOAN_THANH_TOAN = fields.Date(string='Ngày hạch toán thanh toán', help='Ngày hạch toán thanh toán')
    SO_CHUNG_TU_THANH_TOAN = fields.Char(string='Số chứng từ thanh toán', help='Số chứng từ thanh toán')
    SO_TIEN_THANH_TOAN = fields.Float(string='Số tiền thanh toán', help='Số tiền thanh toán')
    SO_TIEN_THANH_TOAN_QUY_DOI = fields.Float(string='Số tiền thanh toán quy đổi', help='Số tiền thanh toán quy đổi')
    TY_GIA_THANH_TOAN = fields.Float(string='Tỷ giá thanh toán', help='Tỷ giá thanh toán')
    LOAI_CHUNG_TU_THANH_TOAN = fields.Integer(string='Loại chứng từ thanh toán', help='Loại chứng từ thanh toán')
    TEN_LOAI_CHUNG_TU_THANH_TOAN = fields.Char(string='Tên loại chứng từ thanh toán', help='Tên Loại chứng từ thanh toán')
    HAN_THANH_TOAN = fields.Date(string='Hạn thanh toán', help='Hạn thanh toán')
    SO_HOA_DON_THANH_TOAN = fields.Char(string='Số hóa đơn thanh toán', help='Số hóa đơn thanh toán')
    SO_CHUA_THANH_TOAN = fields.Float(string='Số chưa thanh toán', help='Số chưa thanh toán')
    SO_CHUA_THANH_TOAN_QUY_DOI = fields.Float(string='Số chưa thanh toán quy đổi', help='Số chưa thanh toán quy đổi')
    SO_THANH_TOAN_LAN_NAY = fields.Float(string='Số thanh toán lần này', help='Số thanh toán lần này')
    SO_THANH_TOAN_LAN_NAY_QUY_DOI = fields.Float(string='Số thanh toán lần này quy đổi', help='Số thanh toán lần này quy đổi')
    MODEL_CHUNG_TU_THANH_TOAN = fields.Char(string='Model chứng từ thanh toán', help='Model chứng từ thanh toán')

    
    ID_CHUNG_TU_CONG_NO = fields.Integer(string='Chứng từ công nợ', help='Id chứng từ công nợ')
    LOAI_CHUNG_TU_CONG_NO_ID = fields.Many2one('danh.muc.loai.chung.tu', string='Loại chứng từ công nợ', help='Loại chứng từ công nợ')
    NGAY_CHUNG_TU_CONG_NO = fields.Date(string='Ngày chứng từ công nợ', help='Ngày chứng từ công nợ')
    NGAY_HACH_TOAN_CONG_NO = fields.Date(string='Ngày hạch toán công nợ', help='Ngày hạch toán công nợ')
    SO_CHUNG_TU_CONG_NO = fields.Char(string='Số chứng từ công nợ', help='Số chứng từ công nợ')
    SO_HOA_DON_CONG_NO = fields.Char(string='Số hóa đơn công nợ', help='Số hóa đơn công nợ')
    SO_TIEN_CONG_NO = fields.Float(string='Số tiền công nợ', help='Số tiền công nợ')
    SO_TIEN_CONG_NO_QUY_DOI = fields.Float(string='Số tiền công nợ quy đổi', help='Số tiền công nợ quy đổi')
    CHENH_LECH_TY_GIA_SO_TIEN_QUY_DOI = fields.Float(string='Chênh lệch tỷ giá số tiền quy đổi', help='Chênh lệch tỷ giá số tiền quy đổi')
    LOAI_CHUNG_TU_CONG_NO = fields.Integer(string='Loại chứng từ công nợ', help='Loại chứng từ công nợ')
    TEN_LOAI_CHUNG_TU_CONG_NO = fields.Char(string='Tên loại chứng từ công nợ', help='Tên loại chứng từ công nợ')
    HAN_THANH_TOAN_CONG_NO = fields.Date(string='Hạn thanh toán công nợ', help='Hạn thanh toán công nợ')
    SO_TIEN_CON_NO = fields.Float(string='Số tiền còn nợ', help='Số tiền còn nợ')
    SO_TIEN_CON_NO_QUY_DOI = fields.Float(string='Số còn nợ quy đổi', help='Số còn nợ quy đổi')
    MODEL_CHUNG_TU_CONG_NO = fields.Char(string='Model chứng từ công nợ', help='Model chứng từ công nợ')
    SO_CONG_NO_THANH_TOAN_LAN_NAY = fields.Float(string='Số thanh toán lần này', help='Số thanh toán lần này')
    SO_CONG_NO_THANH_TOAN_LAN_NAY_QUY_DOI = fields.Float(string='Số thanh toán lần này quy đổi', help='Số thanh toán lần này quy đổi')


    TY_GIA_CONG_NO = fields.Float(string='Tỷ giá công nợ', help='Tỷ giá công nợ')
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản')
    TAI_KHOAN_GIAM_GIA_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản giảm giá', help='Tài khoản giảm giá')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng')
    CTTT_DA_GHI_SO = fields.Boolean(string='Chứng từ thanh toán đã ghi sổ', help='Chứng từ thanh toán đã ghi sổ')
    CTCN_DA_GHI_SO = fields.Boolean(string='Chứng từ công nợ đã ghi sổ', help='Chứng từ công nợ đã ghi sổ')
    LOAI_DOI_TRU = fields.Selection([('0', 'Loại 1'), ('1', 'Loại 2'), ('2', 'Loại 3'), ], string='Loại chứng từ', help='Loại chứng từ')
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    HIEN_TREN_BU_TRU = fields.Boolean(string='Hiện trên bù trừ', help='Dòng này có hiện trên chứng từ nghiệp vụ khác không',default=False)
    CHUNG_TU_NGHIEP_VU_KHAC_ID = fields.Many2one('account.ex.chung.tu.nghiep.vu.khac', string='Chứng từ nghiệp vụ khác', help='Chứng từ nghiệp vụ khác', ondelete='cascade')
    CHENH_LECH_TY_GIA = fields.Float(string='Chênh lệch tỷ giá', help='Chênh lệch tỷ giá')
    