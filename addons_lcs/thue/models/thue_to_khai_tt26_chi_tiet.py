# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class THUE_TO_KHAI_TT26_CHI_TIET(models.Model):
    _name = 'thue.to.khai.tt26.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    KHONG_PHAT_SINH_HOAT_DONG_MUA_BAN_TRONG_KY = fields.Boolean(string='Không phát sinh hoạt động mua bán trong kỳ', help='Không phát sinh hoạt động mua bán trong kỳ')
    THUE_GTGT_CON_DUOC_KHAU_TRU_KY_TRUOC_CHUYEN_SANG = fields.Float(string='Thuế gtgt còn được khấu trừ kỳ trước chuyển sang', help='Thuế gtgt còn được khấu trừ kỳ trước chuyển sang')
    KE_KHAI_THUE_GTGT_PHAI_NOP_NGAN_SACH_NHA_NUOC = fields.Float(string='Kê khai thuế gtgt phải nộp ngân sách nhà nước', help='Kê khai thuế gtgt phải nộp ngân sách nhà nước')
    HANG_HOA_DICH_VU_MUA_VAO_TRONG_KY = fields.Float(string='Hàng hóa dịch vụ mua vào trong kỳ', help='Hàng hóa dịch vụ mua vào trong kỳ')
    GIA_TRI_VA_THUE_GTGT_CUA_HANG_HOA_DICH_VU_MUA_VAO = fields.Float(string='Giá trị và thuế gtgt của hàng hóa dịch vụ mua vào', help='Giá trị và thuế gtgt của hàng hóa dịch vụ mua vào')
    TONG_SO_THUE_GTGT_DUOC_KHAU_TRU_KY_NAY = fields.Float(string='Tổng số thuế gtgt được khấu trừ kỳ này', help='Tổng số thuế gtgt được khấu trừ kỳ này')
    HANG_HOA_DICH_VU_BAN_RA_TRONG_KY = fields.Float(string='Hàng hóa dịch vụ bán ra trong kỳ', help='Hàng hóa dịch vụ bán ra trong kỳ')
    HANG_HOA_DICH_VU_KHONG_CHIU_THUE_GTGT = fields.Float(string='Hàng hóa dịch vụ không chịu thuế gtgt', help='Hàng hóa dịch vụ không chịu thuế gtgt')
    HANG_HOA_DICH_VU_BAN_RA_KHONG_CHIU_THUE_GTGT = fields.Float(string='Hàng hóa dịch vụ bán ra không chịu thuế gtgt', help='Hàng hóa dịch vụ bán ra không chịu thuế gtgt')
    HANG_HOA_DICH_VU_BAN_RA_CHIU_THUE_SUAT_0_PHAN_TRAM = fields.Float(string='Hàng hóa dịch vụ bán ra chịu thuế suất 0 phần trăm', help='Hàng hóa dịch vụ bán ra chịu thuế suất 0 phần trăm')
    HANG_HOA_DICH_VU_BAN_RA_CHIU_THUE_SUAT_5_PHAN_TRAM = fields.Float(string='Hàng hóa dịch vụ bán ra chịu thuế suất 5 phần trăm', help='Hàng hóa dịch vụ bán ra chịu thuế suất 5 phần trăm')
    HANG_HOA_DICH_VU_BAN_RA_CHIU_THUE_SUAT_10_PHAN_TRAM = fields.Float(string='Hàng hóa dịch vụ bán ra chịu thuế suất 10 phần trăm', help='Hàng hóa dịch vụ bán ra chịu thuế suất 10 phần trăm')
    HANG_HOA_DICH_VU_BAN_RA_KHONG_TINH_THUE = fields.Float(string='Hàng hóa dịch vụ bán ra không tính thuế', help='Hàng hóa dịch vụ bán ra không tính thuế')
    TONG_DOANH_THU_VA_THUE_GTGT_CUA_HHDV_BAN_RA = fields.Float(string='Tổng doanh thu và thuế gtgt của hhdv bán ra', help='Tổng doanh thu và thuế gtgt của hhdv bán ra')
    THUE_GTGT_PHAT_SINH_TRONG_KY = fields.Float(string='Thuế gtgt phát sinh trong kỳ', help='Thuế gtgt phát sinh trong kỳ')
    # Điều chính tăng giảm thuế gtgt còn được khấu trừ của các kỳ trước
    DIEU_CHINH_TANG_GIAM_THUE_GTGT_CON_DUOC_KT_CUA_CAC_KY_TRUOC = fields.Float(string='Điều chính tăng giảm thuế gtgt còn được khấu trừ của các kỳ trước', help='Điều chính tăng giảm thuế gtgt còn được khấu trừ của các kỳ trước')
    DIEU_CHINH_GIAM = fields.Float(string='Điều chỉnh giảm', help='Điều chỉnh giảm')
    DIEU_CHINH_TANG = fields.Float(string='Điều chỉnh tăng', help='Điều chỉnh tăng')
    # Thuế gtgt đã nộp ở địa phương khác của hoạt động kinh doanh xây dựng lắp đặt bán hàng bất động sản ngoại tỉnh
    THUE_GTGT_DA_NOP_O_DIA_PHUONG_KHAC_CUA_HDKDXDLDBHBDS_NGOAI_TINH = fields.Float(string='Thuế gtgt đã nộp ở địa phương khác của hoạt động kinh doanh xây dựng lắp đặt bán hàng bất động sản ngoại tỉnh', help='Thuế gtgt đã nộp ở địa phương khác của hoạt động kinh doanh xây dựng lắp đặt bán hàng bất động sản ngoại tỉnh')
    XAC_DINH_NGHIA_VU_THUE_GTGT_PHAI_NOP_TRONG_KY = fields.Float(string='Xác định nghĩa vụ thuế gtgt phải nộp trong kỳ', help='Xác định nghĩa vụ thuế gtgt phải nộp trong kỳ')
    THUE_GTGT_PHAI_NOP_CUA_HOAT_DONG_SAN_XUAT_KINH_DOANH_TRONG_KY = fields.Float(string='Thuế gtgt phải nộp của hoạt động sản xuất kinh doanh trong kỳ', help='Thuế gtgt phải nộp của hoạt động sản xuất kinh doanh trong kỳ')
    THUE_GTGT_MUA_VAO_CUA_DU_AN_DAU_TU = fields.Float(string='Thuế gtgt mua vào của dự án đầu tư', help='Thuế gtgt mua vào của dự án đầu tư')
    THUE_GTGT_CON_PHAI_NOP_TRONG_KY = fields.Float(string='Thuế gtgt còn phải nộp trong kỳ', help='Thuế gtgt còn phải nộp trong kỳ')
    THUE_GTGT_CHUA_KHAU_TRU_HET_KY_NAY = fields.Float(string='Thuế gtgt chưa khấu trừ  hết kỳ này', help='Thuế gtgt chưa khấu trừ  hết kỳ này')
    TONG_SO_THUE_GTGT_DE_NGHI_HOAN = fields.Float(string='Tổng số thuế gtgt đề nghị hoàn', help='Tổng số thuế gtgt đề nghị hoàn')
    THUE_GTGT_DE_NGHI_HOAN_TAI_KHOAN_1331 = fields.Float(string='Thuế gtgt đề nghị hoàn tài khoản 1331', help='Thuế gtgt đề nghị hoàn tài khoản 1331')
    THUE_GTGT_DE_NGHI_HOAN_TAI_KHOAN_1332 = fields.Float(string='Thuế gtgt đề nghị hoàn tài khoản 1332', help='Thuế gtgt đề nghị hoàn tài khoản 1332')
    THUE_GTGT_CON_CHUA_DUOC_KHAU_TRU_CHUYEN_KY_SAU = fields.Float(string='Thuế gtgt còn chưa được khấu trừ chuyển kỳ sau', help='Thuế gtgt còn chưa được khấu trừ chuyển kỳ sau')
    CHI_TIET_ID = fields.Many2one('thue.thue', string='Chi tiết', help='Chi tiết')
    name = fields.Char(string='Name', oldname='NAME')