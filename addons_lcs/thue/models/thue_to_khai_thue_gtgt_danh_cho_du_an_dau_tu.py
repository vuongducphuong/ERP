# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class THUE_TO_KHAI_THUE_GTGT_DANH_CHO_DU_AN_DAU_TU(models.Model):
    _name = 'thue.to.khai.thue.gtgt.danh.cho.du.an.dau.tu'
    _description = ''
    _inherit = ['mail.thread']
    THUE_GTGT_CHUA_DUOC_HOAN_KY_TRUOC_CHUYEN_SANG = fields.Float(string='Thuế gtgt chưa được hoàn kỳ trước chuyển sang', help='Thuế gtgt chưa được hoàn kỳ trước chuyển sang')
    THUE_GTGT_DAU_VAO_CUA_DADT_NHAN_BAN_GIAO_TU_CHU_DADT = fields.Float(string='Thuế gtgt đầu vào của dự án đầu tư nhận bàn giao từ chủ dự án đầu tư', help='Thuế gtgt đầu vào của dự án đầu tư nhận bàn giao từ chủ dự án đầu tư')
    KE_KHAI_THUE_GTGT_DAU_VAO_CUA_DU_AN_DAU_TU = fields.Float(string='Kê khai thuế gtgt đầu vào của dự án đầu tư', help='Kê khai thuế gtgt đầu vào của dự án đầu tư')
    HANG_HOA_DICH_VU_MUA_VAO_TRONG_KY = fields.Float(string='Hàng hóa dịch vụ mua vào trong kỳ', help='Hàng hóa dịch vụ mua vào trong kỳ')
    DIEU_CHINH_TANG = fields.Float(string='Điều chỉnh tăng', help='Điều chỉnh tăng')
    DIEU_CHINH_GIAM = fields.Float(string='Điều chỉnh giảm', help='Điều chỉnh giảm')
    TONG_SO_THUE_GTGT_DAU_VAO_CUA_HHDV_MUA_VAO = fields.Float(string='Tổng số thuế gtgt đầu vào của hhdv mua vào', help='Tổng số thuế gtgt đầu vào của hhdv mua vào')
    THUE_GTGT_MUA_VAO_DU_AN_DAU_TU = fields.Float(string='Thuế gtgt mua vào dự án đầu tư', help='Thuế gtgt mua vào dự án đầu tư')
    THUE_GTGT_DAU_VAO_CHUA_DUOC_HOAN_DEN_KY_TINH_THUE_CUA_DADT = fields.Float(string='Thuế gtgt đầu vào chưa được hoàn đến kỳ tinh thuế của dự án đầu tư', help='Thuế gtgt đầu vào chưa được hoàn đến kỳ tinh thuế của dự án đầu tư')
    THUE_GTGT_DE_NGHI_HOAN = fields.Float(string='Thuế gtgt đề nghị hoàn', help='Thuế gtgt đề nghị hoàn')
    # THUE_GTGT_DAU_VAO_CUA_HANG_HOA_NHAP_KHAU_THUOC_LOAI_TRONG_NUOC_CHUA_SAN_XUAT_DUOC_DE_TAO_TAI_SAN_CO_DINH_DA_DE_NGHI_HOAN = fields.Float(string='Thuế gtgt đầu vào của hàng hóa nhập khẩu thuộc loại trong nước chưa sản xuất được để tạo tài sản cố định đã đề nghị hoàn', help='Thuế gtgt đầu vào của hàng hóa nhập khẩu thuộc loại trong nước chưa sản xuất được để tạo tài sản cố định đã đề nghị hoàn')
    THUE_GTGT_DAU_VAO_CON_LAI_CUA_DU_AN_DAU_TU_DE_NGHI_HOAN = fields.Float(string='Thuế gtgt đầu vào còn lại của dự án đầu tư đề nghị hoàn', help='Thuế gtgt đầu vào còn lại của dự án đầu tư đề nghị hoàn')
    # THUE_GTGT_DAU_VAO_CUA_DU_AN_DAU_TU_CHUA_DUOC_HOAN_BAN_GIAO_CHO_DOANH_NGHIEP_MOI_THANH_LAP_TRONG_KY = fields.Float(string='Thuế gtgt đầu vào của dự án đầu tư chưa được hoàn bàn giao cho doanh nghiệp mới thành lập trong kỳ', help='Thuế gtgt đầu vào của dự án đầu tư chưa được hoàn bàn giao cho doanh nghiệp mới thành lập trong kỳ')
    THUE_GTGT_DAU_VAO_CUA_DU_AN_DAU_TU_CHUA_DUOC_HOAN_CHUYEN_KY_SAU = fields.Float(string='Thuế gtgt đầu vào của dự án đầu tư chưa được hoàn chuyển kỳ sau', help='Thuế gtgt đầu vào của dự án đầu tư chưa được hoàn chuyển kỳ sau')
    CHI_TIET_ID_3 = fields.Many2one('thue.thue', string='Chi tiết', help='Chi tiết')
    name = fields.Char(string='Name', help='Name', oldname='NAME')