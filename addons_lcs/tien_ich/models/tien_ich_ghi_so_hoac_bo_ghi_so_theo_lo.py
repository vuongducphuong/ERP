# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_GHI_SO_HOAC_BO_GHI_SO_THEO_LO(models.Model):
	_name = 'tien.ich.ghi.so.hoac.bo.ghi.so.theo.lo'
	_description = 'Ghi sổ/Bỏ ghi sổ theo lô'
	_auto = False
	
	KY = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ', help='Kỳ ghi sổ', default='DAU_THANG_DEN_HIEN_TAI',required=True)
	TU_NGAY = fields.Date(string='Từ', help='Từ ngày',required=True,default=fields.Datetime.now)
	DEN_NGAY = fields.Date(string='Đến', help='Đến ngày',required=True,default=fields.Datetime.now)
	TINH_LAI_TY_GIA_XUAT_KHO = fields.Boolean(string='Tính lại tỷ giá xuất kho', help='Tính lại tỷ giá xuất kho')
	TINH_LAI_TY_GIA_XUAT_QUY = fields.Boolean(string='Tính lại tỷ giá xuất quỹ', help='Tính lại tỷ giá xuất quỹ')
	name = fields.Char(string='Name', help='Name', oldname='NAME')

	TIEN_ICH_GHI_SO_HOAC_BO_GHI_SO_THEO_LO_PHAN_HE_IDS = fields.One2many('tien.ich.ghi.so.hoac.bo.ghi.so.theo.lo.phan.he', 'GHI_SO_HOAC_BO_GHI_SO_THEO_LO_PHAN_HE_ID', string='Ghi sổ hoặc bỏ ghi sổ theo lô phân hệ')

	@api.onchange('KY')
	def _cap_nhat_ngay(self):
		self.onchange_time(self.KY, 'TU_NGAY', 'DEN_NGAY')

	
	@api.model
	def load_phan_he(self, args):
		new_line = [[5]]
		dict_phan_he = [
			{'PHAN_HE' : 'QUY','TEN_PHAN_HE' : 'Quỹ'},
			{'PHAN_HE' : 'NGAN_HANG', 'TEN_PHAN_HE' : 'Ngân hàng'},
			{'PHAN_HE' : 'MUA_HANG', 'TEN_PHAN_HE' : 'Mua hàng'},
			{'PHAN_HE' : 'BAN_HANG', 'TEN_PHAN_HE' : 'Bán hàng'},
			{'PHAN_HE' : 'KHO', 'TEN_PHAN_HE' : 'Kho'},
			{'PHAN_HE' : 'TAI_SAN_CO_DINH', 'TEN_PHAN_HE' : 'Tài sản cố định'},
			{'PHAN_HE' : 'CONG_CU_DUNG_CU', 'TEN_PHAN_HE' : 'Công cụ dụng cụ'},
			{'PHAN_HE' : 'GIA_THANH', 'TEN_PHAN_HE' : 'Giá thành'},
			{'PHAN_HE' : 'TONG_HOP', 'TEN_PHAN_HE' : 'Tổng hợp'},
			{'PHAN_HE' : 'TIEN_LUONG', 'TEN_PHAN_HE' : 'Tiền lương'},
		]
		for line in dict_phan_he:
			new_line += [(0,0,{
				'PHAN_HE' : line.get('TEN_PHAN_HE'),
				})]
		return {'TIEN_ICH_GHI_SO_HOAC_BO_GHI_SO_THEO_LO_PHAN_HE_IDS': new_line}