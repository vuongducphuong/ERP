# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_THUYET_MINH_BAO_CAO_TAI_CHINH_CHI_TIET_MAC_DINH(models.Model):
	_name = 'tien.ich.thuyet.minh.bao.cao.tai.chinh.chi.tiet.mac.dinh'
	_description = ''
	_inherit = ['mail.thread']
	MA_CHI_TIEU = fields.Char(string='Mã chỉ tiêu', help='Mã chỉ tiêu')
	TEN_CHI_TIEU = fields.Char(string='Tên chỉ tiêu', help='Tên chỉ tiêu')
	TEN_TIENG_ANH = fields.Char(string='Tên tiếng anh', help='Tên tiếng anh')
	NOI_DUNG = fields.Char(string='Nội dung', help='Nội dung')
	THUOC_PHAN = fields.Char(string='Thuộc phần', help='Thuộc phần')
	KHONG_IN = fields.Boolean(string='Không in', help='Không in')
	IN_DAM = fields.Boolean(string='In đậm', help='In đậm')
	IN_NGHIENG = fields.Boolean(string='In nghiêng', help='In nghiêng')
	THONG_TU  = fields.Char(string='Thông tư' , help = 'Thông tư')
	SO_THU_TU = fields.Integer(string='Số thứ tự các dòng chi tiết', help='Số thứ tự các dòng chi tiết')
	name = fields.Char(string='Name', help='Name', oldname='NAME')
	LOAI_CHI_TIEU = fields.Selection([('0', 'Chi tiết'), ('1', 'Tổng hợp'), ('2', 'Tiêu đề'),('3', 'Chú thích'), ], string='Loại chỉ tiêu', help='Loại chỉ tiêu', default='0' , required=True)
	PART_IN_TAB = fields.Integer(string='part in tab', help='part in tab')
	CUOI_NAM = fields.Char(string='Cuối năm', help='Cuối năm')
	DAU_NAM = fields.Char(string='Đầu năm', help='Đầu năm')
	GIA_TRI_HOP_LY_GHI_SO_CUOI_NAM = fields.Char(string='Giá trị hợp lý/ghi sổ cuối năm', help='Giá trị hợp lý/ghi sổ cuối năm')
	DU_PHONG_CUOI_NAM = fields.Char(string='Dự phòng cuối năm', help='Dự phòng cuối năm')
	DU_PHONG_DAU_NAM = fields.Char(string='Dự phòng đầu năm', help='Dự phòng đầu năm')
	NHA_CUA_VAT_CHAT_KIEN_TRUC = fields.Char(string='Nhà cửa vật chất kiến trúc', help='Nhà cửa vật chất kiến trúc')
	PHUONG_TIEN_VAN_TAI_TRUYEN_DAN = fields.Char(string='Phương tiện vận tải truyền dẫn', help='Phương tiện vận tải truyền dẫn')
	CAY_LAU_NAM_SUC_VAT_LAM_VIEC_CHO_SAN_PHAM = fields.Char(string='Cây lâu năm, súc vật làm việc cho sản phẩm', help='Cây lâu năm, súc vật làm việc cho sản phẩm')
	KET_CAU_HA_TANG_DNNDTXD = fields.Char(string='Kết cấu hạ tầng do NN ĐTXD...', help='Kết cấu hạ tầng, có giá trị lớn do Nhà nước đầu tư xây dựng có nguồn ngân sách Nhà nước')
	TAI_SAN_CO_DINH_HUU_HINH_KHAC = fields.Char(string='Tài sản cố định hữu hình khác', help='Tài sản cố định hữu hình khác')
	TONG_CONG = fields.Char(string='Tổng cộng', help='Tổng cộng')
	SO_DAU_NAM = fields.Char(string='Số đầu năm', help='Số đầu năm')
	SO_CUOI_NAM = fields.Char(string='Số cuối năm', help='Số cuối năm')
	GIA_TRI_DAU_NAM_12 = fields.Char(string='Giá trị đầu năm', help='Giá trị đầu năm', related = 'DAU_NAM' ,store=False, )
	GIAM_TRONG_NAM_12 = fields.Char(string='Giảm trong năm', help='Giảm trong năm', related = 'DU_PHONG_DAU_NAM' ,store=False, )
	TANG_TRONG_NAM_12 = fields.Char(string='Tăng trong năm', help='Tăng trong năm', related = 'DU_PHONG_CUOI_NAM' ,store=False, )
	GIA_TRI_CUOI_NAM_12 = fields.Char(string='Giá trị cuối năm', help='Giá trị cuối năm', related = 'CUOI_NAM' ,store=False, )
	CUOI_NAM_14 = fields.Char(string='Cuối năm', help='Cuối năm' , related='CUOI_NAM', store=False,  )
	DAU_NAM_14 = fields.Char(string='Đầu năm', help='Đầu năm' , related='DAU_NAM', store=False, )
	GIA_TRI_DAU_NAM_15 = fields.Char(string='Giá trị đầu năm', help='Giá trị đầu năm', related = 'DAU_NAM' ,store=False, )
	GIA_TRI_CUOI_NAM_15 = fields.Char(string='Giá trị cuối năm', help='Giá trị cuối năm', related = 'CUOI_NAM' ,store=False, )
	GIA_TRI_DAU_NAM_17 = fields.Char(string='Giá trị đầu năm', help='Giá trị đầu năm', related = 'DAU_NAM' ,store=False, )
	GIA_TRI_CUOI_NAM_17 = fields.Char(string='Giá trị cuối năm', help='Giá trị cuối năm', related = 'CUOI_NAM' ,store=False, )
	GIA_TRI_DAU_NAM_18 = fields.Char(string='Giá trị đầu năm', help='Giá trị đầu năm', related = 'DAU_NAM' ,store=False, )
	GIA_TRI_CUOI_NAM_18 = fields.Char(string='Giá trị cuối năm', help='Giá trị cuối năm', related = 'CUOI_NAM' ,store=False, )

	TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_IDS = fields.One2many('tien.ich.xdct.tmbctc.tong.hop.mac.dinh', 'MAC_DINH_ID_1', string='Xây dựng công thức')
	TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LCT_CHI_TIET_IDS = fields.One2many('tien.ich.xdct.tmbctc.lct.chi.tiet.mac.dinh', 'CHI_TIET_ID_1', string='Xây dựng công thức')
