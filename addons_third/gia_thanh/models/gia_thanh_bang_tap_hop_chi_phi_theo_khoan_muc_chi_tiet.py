# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_BANG_TAP_HOP_CHI_PHI_THEO_KHOAN_MUC_CHI_TIET(models.Model):
    _name = 'gia.thanh.bang.tap.hop.chi.phi.theo.khoan.muc.chi.tiet'
    _description = ''
    
    MA_DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Mã đối tượng THCP', help='Mã đối tượng tập hợp chi phí')
    TEN_DOI_TUONG_THCP = fields.Char(string='Tên đối tượng THCP', help='Tên đối tượng tập hợp chi phí')
    LOAI_DOI_TUONG_THCP = fields.Char(string='Loại đối tượng THCP', help='Loại đối tượng tập hợp chi phí')
    
    MA_CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Mã công trình', help='Mã công trình')
    TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình')
    LOAI_CONG_TRINH = fields.Char(string='Loại công trình', help='Loại công trình')
    
    SO_DON_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Số đơn hàng', help='Số đơn hàng')
    NGAY_DON_HANG = fields.Date(string='Ngày đơn hàng', help='Ngày đơn hàng')
    KHACH_HANG = fields.Char(string='Khách hàng', help='Khách hàng')

    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Số hợp đồng', help='Số hợp đồng')    
    NGAY_KY = fields.Date(string='Ngày ký', help='Ngày ký')
    TRICH_YEU = fields.Char(string='Trích yếu', help='Trích yếu')

    TONG_GIA_THANH = fields.Float(string='Tổng giá thành', help='Tổng giá thành')
    NGUYEN_VAT_LIEU_DAU_KY = fields.Float(string='Nguyên vật liệu', help='Nguyên vật liệu dở dang đầu kỳ')
    NHAN_CONG_DAU_KY = fields.Float(string='Nhân công ', help='Nhân công dở dang đầu kỳ')
    KHAU_HAO_DAU_KY = fields.Float(string='Khấu hao', help='Khấu hao dở dang đầu kỳ')
    CHI_PHI_MUA_NGOAI_DAU_KY = fields.Float(string='Chi phí mua ngoài', help='Chi phí mua ngoài đầu kỳ')
    CHI_PHI_KHAC_DAU_KY = fields.Float(string='Chi phí khác', help='Chi phí khác đầu kỳ')
    TONG_DO_DANG_DAU_KY = fields.Float(string='Tổng', help='Tổng dở dang đầu kỳ')
    NGUYEN_VAT_LIEU_TRONG_KY = fields.Float(string='Nguyên vật liệu', help='Nguyên vật liệu trong kỳ')
    NHAN_CONG_TRONG_KY = fields.Float(string='Nhân công', help='Nhân công trong kỳ')
    KHAU_HAO_TRONG_KY = fields.Float(string='Khấu hao', help='Khấu hao trong kỳ')
    CHI_PHI_MUA_NGOAI_TRONG_KY = fields.Float(string='Chi phí mua ngoài', help='Chi phí mua ngoài trong kỳ')
    CHI_PHI_KHAC_TRONG_KY = fields.Float(string='Chi phí khác ', help='Chi phí khác trong kỳ ')
    TONG_PHAT_SINH_TRONG_KY = fields.Float(string='Tổng', help='Tổng phát sinh trong kỳ')
    KHOAN_GIAM_GIA_THANH = fields.Float(string='Khoản giảm giá thành', help='Khoản giảm giá thành')
    NGUYEN_VAT_LIEU_CUOI_KY = fields.Float(string='Nguyên vật liệu', help='Nguyên vật liệu cuối kỳ')
    NHAN_CONG_CUOI_KY = fields.Float(string='Nhân công', help='Nhân công cuối kỳ')
    KHAU_HAO_CUOI_KY = fields.Float(string='Khấu hao', help='Khấu hao cuối kỳ')
    CHI_PHI_MUA_NGOAI_CUOI_KY = fields.Float(string='Chi phí mua ngoài', help='Chi phí mua ngoài cuối kỳ')
    CHI_PHI_KHAC_CUOI_KY = fields.Float(string='Chi phí khác', help='Chi phí khác cuối kỳ ')
    TONG_DO_DANG_CUOI_KY = fields.Float(string='Tổng', help='Tổng ')
    CHI_TIET_ID = fields.Many2one('gia.thanh.bang.tap.hop.chi.phi.theo.khoan.muc',string='Chi tiết', help='Chi tiết')

    LUY_KE_CHI_PHI = fields.Float(string='Lũy kế chi phí', help='Lũy kế chi phí')
    LUY_KE_DA_NGHIEM_THU = fields.Float(string='Lũy kế đã nghiệm thu', help='Lũy kế đã nghiệm thu')
    SO_CHUA_NGHIEM_THU_DAU_KY = fields.Float(string='Số chưa nghiệm thu đầu kỳ', help='Số chưa nghiệm thu đầu kỳ')
    SO_CHUA_NGHIEM_THU_CUOI_KY = fields.Float(string='Số chưa nghiệm thu cuối kỳ', help='Số chưa nghiệm thu cuối kỳ')

    LUY_KE_NVL_TRUC_TIEP = fields.Float(string='NVL trực tiếp', help='NVL trực tiếp')
    LUY_KE_NHAN_CONG_TRUC_TIEP = fields.Float(string='Nhân công trực tiếp', help='Nhân công trực tiếp')
    LUY_KE_MAY_THI_CONG = fields.Float(string='Máy thi công', help='Máy thi công')
    LUY_KE_CHI_PHI_CHUNG = fields.Float(string='Chi phí chung', help='Chi phí chung')
    LUY_KE_TONG = fields.Float(string='Tổng', help='Tổng')
    MAY_THI_CONG_DAU_KY = fields.Float(string='Máy thi công', help='Máy thi công')
    MAY_THI_CONG_TRONG_KY = fields.Float(string='Máy thi công', help='Máy thi công') 