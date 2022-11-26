# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_TAP_HOP_CHI_PHI_TRUC_TIEP_CHI_TIET(models.Model):
    _name = 'gia.thanh.tap.hop.chi.phi.truc.tiep.chi.tiet'
    _description = ''
    
    MA_DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Mã đối tượng THCP', help='Mã đối tượng tập hợp chi phí')
    MA_CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Mã công trình', help='Mã công trình')
    SO_DON_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Số đơn hàng', help='Số đơn hàng')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Số đơn hàng', help='Số đơn hàng')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_CHI_PHI_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chi phí', help='Tài khoản chi phí')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    TEN_DOI_TUONG_THCP = fields.Char(string='Tên đối tượng THCP', help='Tên đối tượng tập hợp chi phí')
    CHI_TIET_ID = fields.Many2one('gia.thanh.tap.hop.chi.phi.truc.tiep', string='Chi tiết', help='Chi tiết')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    MA_KHOAN_MUC_CP = fields.Char(string='Mã khoản mục CP', help='Mã khoản mục CP')
    TEN_KHOAN_MUC_CP = fields.Char(string='Tên khoản mục CP', help='Tên khoản mục CP')
    TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình')