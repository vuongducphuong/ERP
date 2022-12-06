# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class TONG_HOP_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE_CONG_NO_THANH_TOAN(models.Model):
    _name = 'tong.hop.danh.gia.lai.tai.khoan.ngoai.te.cong.no.thanh.toan'
    _description = ''
    _inherit = ['mail.thread']
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_CONG_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK công nợ', help='Tk công nợ')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng')
    TY_GIA_TREN_CT = fields.Float(string='Tỷ giá trên CT', help='Tỷ giá trên ct')
    TY_GIA_DANH_GIA_LAI_GAN_NHAT = fields.Float(string='Tỷ giá đánh giá lại gần nhất', help='Tỷ giá đánh giá lại gần nhất')
    SO_CHUA_DOI_TRU = fields.Float(string='Số chưa đối trừ', help='Số chưa đối trừ',digits=decimal_precision.get_precision('VND'))
    SO_CHUA_DOI_TRU_QUY_DOI = fields.Float(string='Số chưa đối trừ quy đổi', help='Số chưa đối trừ quy đổi',digits=decimal_precision.get_precision('VND'))
    DANH_GIA_LAI = fields.Float(string='Đánh giá lại', help='Đánh giá lại',digits=decimal_precision.get_precision('VND'))
    CHENH_LECH = fields.Float(string='Chênh lệch', help='Chênh lệch',digits=decimal_precision.get_precision('VND'))
    DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE_ID = fields.Many2one('tong.hop.danh.gia.lai.tai.khoan.ngoai.te', string='Đánh giá lại tài khoản ngoại tệ', help='Đánh giá lại tài khoản ngoại tệ')
    ID_CHUNG_TU_GOC = fields.Integer(string='ID chứng từ gốc', help='ID chứng từ gốc')
    MODEL_CHUNG_TU_GOC = fields.Char(string='Model chứng từ gốc', help='Model chứng từ gốc')
    ID_TK_VA_ID_DOI_TUONG = fields.Char(string='ID của tài khoản và id của đối tượng để filter', help='ID của tài khoản và id của đối tượng để filter')

    @api.onchange('DANH_GIA_LAI')
    def _onchange_DANH_GIA_LAI(self):
        if self.DANH_GIA_LAI:
            self.CHENH_LECH = self.DANH_GIA_LAI - self.SO_CHUA_DOI_TRU_QUY_DOI