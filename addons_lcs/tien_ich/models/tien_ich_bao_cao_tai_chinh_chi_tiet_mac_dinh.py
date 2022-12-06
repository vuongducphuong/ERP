# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_BAO_CAO_TAI_CHINH_CHI_TIET_MAC_DINH(models.Model):
	_name = 'tien.ich.bao.cao.tai.chinh.chi.tiet.mac.dinh'

	MA_CHI_TIEU = fields.Char(string='Mã chỉ tiêu', help='Mã chỉ tiêu')
	TEN_CHI_TIEU = fields.Char(string='Tên chỉ tiêu', help='Tên chỉ tiêu')
	TEN_TIENG_ANH = fields.Char(string='Tên tiếng anh', help='Tên tiếng anh')
	THUYET_MINH = fields.Char(string='Thuyết minh', help='Thuyết minh')
	LOAI_CHI_TIEU = fields.Selection([('0', 'Chi tiết'), ('1', 'Tổng hợp'), ('2', 'Chi tiết (chỉ lấy giá trị lớn hơn 0)'), ], string='Loại chỉ tiêu', help='Loại chỉ tiêu', default='0' , required=True)
	CONG_THUC = fields.Char(string='Công thức', help='Công thức')
	KHONG_IN = fields.Boolean(string='Không in', help='Không in')
	IN_DAM = fields.Boolean(string='In đậm', help='In đậm')
	IN_NGHIENG = fields.Boolean(string='In nghiêng', help='In nghiêng')
	DA_SUA_CT_MAC_DINH = fields.Boolean(string='Đã sửa CT mặc định', help='Đã sửa công thức mặc định')
	ReportID  = fields.Integer(string='Loại báo cáo' , help = 'Loại báo cáo')
	THONG_TU  = fields.Char(string='Thông tư' , help = 'Thông tư')
	XAY_DUNG_CONG_THUC  = fields.Char(string='Thông tư' , help = 'Thông tư')

	SO_THU_TU = fields.Integer(string='Số thứ tự các dòng chi tiết', help='Số thứ tự các dòng chi tiết')
	ID_CHI_TIEU = fields.Char(string='GUID', help='Trường lưu id của master chỉ tiêu')

	TIEN_ICH_XAY_DUNG_CONG_THUC_IDS = fields.One2many('tien.ich.xay.dung.cong.thuc.mac.dinh', 'MAC_DINH_ID', string='Xây dựng công thức')
	TIEN_ICH_XAY_DUNG_CONG_THUC_LCT_CHI_TIET_IDS = fields.One2many('tien.ich.xdct.loai.chi.tieu.chi.tiet.mac.dinh', 'CHI_TIET_ID', string='Xây dựng công thức')

	name = fields.Char(string='Name', help='Name', oldname='NAME')
