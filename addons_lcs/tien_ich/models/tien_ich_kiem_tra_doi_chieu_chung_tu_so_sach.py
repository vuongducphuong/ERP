# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_KIEM_TRA_DOI_CHIEU_CHUNG_TU_SO_SACH(models.Model):
    _name = 'tien.ich.kiem.tra.doi.chieu.chung.tu.so.sach'
    _description = ''
    _auto = False

    CHON_BO_TAT_CA = fields.Boolean(string='Chọn/bỏ tất cả', help='Chọn/bỏ tất cả')
    TRANG_THAI_GHI_SO_CHUNG_TU = fields.Boolean(string='Trạng thái ghi sổ chứng từ', help='Trạng thái ghi sổ chứng từ')
    TIEN_MAT_TIEN_GUI = fields.Boolean(string='Tiền mặt, tiền gửi', help='Tiền mặt, tiền gửi')
    KHO_MUA_HANG = fields.Boolean(string='Kho, mua hàng', help='Kho, mua hàng')
    CONG_NO = fields.Boolean(string='Công nợ', help='Công nợ')
    TAI_SAN_CO_DINH = fields.Boolean(string='Tài sản cố định', help='Tài sản cố định')
    CONG_CU_DUNG_CU = fields.Boolean(string='Công cụ dụng cụ, chi phí trả trước', help='Công cụ dụng cụ, chi phí trả trước')
    THUE = fields.Boolean(string='Thuế', help='Thuế')
    KHO_BAN_HANG = fields.Boolean(string='Kho, bán hàng', help='Kho, bán hàng')
    GIA_THANH = fields.Boolean(string='Giá thành', help='Giá thành')
    KET_CHUYEN_LAI_LO_THEO_KY = fields.Boolean(string='Kết chuyển lãi lỗ theo kỳ', help='Kết chuyển lãi lỗ theo kỳ')
    BAO_CAO_TAI_CHINH = fields.Boolean(string='Báo cáo tài chính', help='Báo cáo tài chính')
    THU_QUY = fields.Boolean(string='Thủ quỹ', help='Thủ quỹ')
    THU_KHO = fields.Boolean(string='Thủ kho', help='Thủ kho')
    KHOANG_THOI_GIAN = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Khoảng thời gian', help='Khoảng thời gian', default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày',default=fields.Datetime.now)
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày',default=fields.Datetime.now)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh')
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default=True)
    name = fields.Char(string='Name', help='Name', oldname='NAME')
   

    @api.model
    def default_get(self, fields_list):
      result = super(TIEN_ICH_KIEM_TRA_DOI_CHIEU_CHUNG_TU_SO_SACH, self).default_get(fields_list)
      result['CHI_NHANH_ID'] = self.env['danh.muc.to.chuc'].search([],limit=1).id
      return result

    @api.onchange('KHOANG_THOI_GIAN')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KHOANG_THOI_GIAN, 'TU_NGAY', 'DEN_NGAY')