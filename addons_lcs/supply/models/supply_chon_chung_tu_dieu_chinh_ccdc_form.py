# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SUPPLY_CHON_CHUNG_TU_DIEU_CHINH_CCDC_FORM(models.Model):
    _name = 'supply.chon.chung.tu.dieu.chinh.ccdc.form'
    _auto = False
    _description = ''
 
    LOAI_CHUNG_TU = fields.Selection([('NHAP_KHO', 'Nhập kho'), ('XUAT_KHO', ' Xuất kho'), ('MUA_HANG', ' Mua hàng'), ('CHUNG_TU_NGHIEP_VU_KHAC', ' Chứng từ nghiệp vụ khác'), ('PHIEU_THU', ' Phiếu thu'), ('PHIEU_CHI', ' Phiếu chi'), ('SEC_TIEN_MAT', 'Séc tiền mặt'), ('SEC_CHUYEN_KHOAN', ' Séc chuyển khoản'), ('UY_NHIEM_CHI', ' Ủy nhiệm chi'), ('THU_TIEN_GUI', 'Thu tiền gửi'), ('TAT_CA', ' Tất cả  '), ], string='Loại chứng từ', help='Loại chứng từ',required=True,default='TAT_CA')
    KHOANG_THOI_GIAN = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Khoảng thời gian', help='Khoảng thời gian', default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TU_NGAY = fields.Date(string='Từ ', help='Từ ngày',default=fields.Datetime.now)
    DEN_NGAY = fields.Date(string='Đến ', help='Đến ngày',default=fields.Datetime.now)
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    SUPPLY_CHON_CHUNG_TU_DIEU_CHINH_CONG_CU_DUNG_CU_CHI_TIET_IDS = fields.One2many('supply.chon.chung.tu.dieu.chinh.cong.cu.dung.cu.chi.tiet', 'CHON_CHUNG_TU_ID', string='chọn chứng từ điều chỉnh công cụ dụng cụ chi tiết ')

    @api.onchange('KHOANG_THOI_GIAN')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KHOANG_THOI_GIAN, 'TU_NGAY', 'DEN_NGAY')