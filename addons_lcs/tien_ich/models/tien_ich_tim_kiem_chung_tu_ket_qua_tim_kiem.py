# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class TIEN_ICH_TIM_KIEM_CHUNG_TU_KET_QUA_TIM_KIEM(models.Model):
    _name = 'tien.ich.tim.kiem.chung.tu.ket.qua.tim.kiem'
    _description = ''
    _inherit = ['mail.thread']
    STT = fields.Integer(string='STT', help='Số thứ tự')
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
    TK_NO_ID = fields.Char(string='TK nợ', help='Tài khoản nợ')
    TK_CO_ID = fields.Char(string='TK có', help='Tài khoản có')
    LOAI_TIEN = fields.Char(string='Loại tiền', help='Loại tiền')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    QUY_DOI = fields.Float(string='Quy đổi', help='Quy đổi',digits=decimal_precision.get_precision('Product Price'))
    MA_VTHH = fields.Char(string='Mã VTHH', help='Mã vật tư hàng hóa')
    TEN_VTHH = fields.Char(string='Tên VTHH', help='Tên vật tư hàng hóa')
    KHO_NHAP = fields.Char(string='Kho nhập', help='Kho nhập')
    KHO_XUAT = fields.Char(string='Kho xuất', help='Kho xuất')
    DVT = fields.Char(string='ĐVT', help='Đơn vị tính')
    SO_LUONG = fields.Float(string='Số lượng ', help='Số lượng ', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits= decimal_precision.get_precision('DON_GIA'))
    TY_LE_CK = fields.Float(string='Tỷ lệ CK', help='Tỷ lệ chiết khấu',digits= decimal_precision.get_precision('Product Price'))
    TIEN_CK = fields.Float(string='Tiền CK', help='Tiền chiết khấu',digits= decimal_precision.get_precision('Product Price'))
    LOAI_TSCD = fields.Char(string='Loại TSCĐ', help='Loại tài sản cố định')
    MA_TSCD = fields.Char(string='Mã TSCĐ', help='Mã tài sản cố định')
    MA_CCDC = fields.Char(string='Mã CCDC', help='Mã công cụ dụng cụ')
    DOI_TUONG_NO = fields.Char(string='Đối tượng nợ', help='Đối tượng nợ')
    DOI_TUONG_CO = fields.Char(string='Đối tượng có', help='Đối tượng có')
    DON_VI = fields.Char(string='Đơn vị', help='Đơn vị')
    NHAN_VIEN = fields.Char(string='Nhân viên', help='Nhân viên')
    TAI_KHOAN_NGAN_HANG = fields.Char(string='Tài khoản ngân hàng', help='Tài khoản ngân hàng')
    KHOAN_MUC_CHI_PHI = fields.Char(string='Khoản mục chi phí', help='Khoản mục chi phí')
    CONG_TRINH = fields.Char(string='Công trình', help='Công trình')
    DT_TAP_HOP_CHI_PHI = fields.Char(string='ĐT tập hợp chi phí', help='Đối tượng tập hợp chi phí')
    DON_MUA_HANG = fields.Char(string='Đơn mua hàng', help='Đơn mua hàng')
    DON_DAT_HANG = fields.Char(string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOP_DONG_MUA = fields.Char(string='Hợp đồng mua', help='Hợp đồng mua')
    HOP_DONG_BAN = fields.Char(string='Hợp đồng bán', help='Hợp đồng bán')
    MA_THONG_KE = fields.Char(string='Mã thống kê', help='Mã thống kê')
    DIEN_GIAI_CHUNG = fields.Char(string='Diễn giải chung', help='Diễn giải chung')
    DIEN_GIAI_CHI_TIET = fields.Char(string='Diễn giải chi tiết', help='Tìm kiếm chứng từ')
    TINH_TRANG_GHI_SO = fields.Char(string='Tình trạng ghi sổ', help='Diễn giải chi tiết')
    name = fields.Char(string='Name', oldname='NAME')
    TIM_KIEM_CHUNG_TU_KET_QUA_TIM_KIEM_ID = fields.Many2one('tien.ich.tim.kiem.chung.tu', string='Tìm kiếm chứng từ kết quả tìm kiếm', help='Tìm kiếm chứng từ kết quả tìm kiếm')