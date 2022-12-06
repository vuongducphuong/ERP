# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class THUE_CHUNG_TU_KHONG_HOP_LE_CHI_TIET(models.Model):
    _name = 'thue.chung.tu.khong.hop.le.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    NGAY_CHUNG_TU = fields.Char(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    KY_HIEU_HOA_DON = fields.Char(string='Ký hiệu hóa đơn', help='Ký hiệu hóa đơn')
    MAU_SO_HOA_DON = fields.Char(string='Mẫu số hóa đơn', help='Mẫu số hóa đơn')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    TEN_HANG_HOA_DICH_VU = fields.Char(string='Tên hàng hóa, dịch vụ', help='Tên hàng hóa, dịch vụ')
    TEN_NGUOI_MUA = fields.Char(string='Tên người mua', help='Tên người mua')
    TEN_NGUOI_BAN = fields.Char(string='Tên người bán', help='Tên người bán')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    NHOM_HHDV_MUA_VAO = fields.Char(string='Nhóm HHDV mua vào', help='Nhóm HHDV mua vào')
    PHAN_TRAM_THUE_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang', string='% thuế GTGT', help='Phần trăm thuế giá trị gia tăng')
    CHI_TIET_ID = fields.Many2one('thue.chung.tu.khong.hop.le', string='Chi tiết', help='Chi tiết')
    name = fields.Char(string='Name', help='Name', oldname='NAME')