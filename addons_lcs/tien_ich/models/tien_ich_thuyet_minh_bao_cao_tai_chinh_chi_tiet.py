# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_THUYET_MINH_BAO_CAO_TAI_CHINH_CHI_TIET(models.Model):
	_name = 'tien.ich.thuyet.minh.bao.cao.tai.chinh.chi.tiet'
	_description = ''
	_inherit = ['mail.thread']
	
	MA_CHI_TIEU = fields.Char(string='Mã chỉ tiêu', help='Mã chỉ tiêu')
	TEN_CHI_TIEU = fields.Char(string='Tên chỉ tiêu', help='Tên chỉ tiêu')
	TEN_TIENG_ANH = fields.Char(string='Tên tiếng anh', help='Tên tiếng anh')
	NOI_DUNG = fields.Char(string='Nội dung', help='Nội dung')
	THUOC_PHAN = fields.Char(string='Thuộc phần', help='Thuộc phần')
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
	KHONG_IN = fields.Boolean(string='Không in', help='Không in')
	IN_DAM = fields.Boolean(string='In đậm', help='In đậm')
	IN_NGHIENG = fields.Boolean(string='In nghiêng', help='In nghiêng')
	SO_THU_TU = fields.Integer(string='Số thứ tự các dòng chi tiết', help='Số thứ tự các dòng chi tiết')
	CHI_TIET_ID_1 = fields.Many2one('tien.ich.thiet.lap.bao.cao.tai.chinh', string='Chi tiết', help='Chi tiết', ondelete='cascade')
	THONG_TU  = fields.Char(string='Thông tư' , help = 'Thông tư')
	name = fields.Char(string='Name', help='Name', oldname='NAME')
	tab = fields.Selection([
		('1', '1.Thông tin chung'),
		('2', '2.Thông tin bổ sung'),
		('3', '3.Đầu tư tài chính'),
		('4', '4.Phải thu khác'),
		('5', '5.Nợ xấu'),
		('6', '6.Hàng tồn kho'),
		('7', '7.TS dở dang dài hạn'),
		('8', '8.TSCĐ hữu hình'),
		('9', '9.TSCĐ vô hình'),
		('10', '10.TSCĐ thuê tài chính'),
		('11', '11.Tăng giảm BĐS đầu tư'),
		('12', '12.Các khoản vay'),
		('13', '13.Nợ thuê tài chính'),
		('14', '14.Thuế và các khoản phải nộp'),
		('15', '15.Trái phiếu phát hành'),
		('16', '16.Biến động vốn CSH'),
		('17', '17.Tài sản thiếu chờ xử lý'),
		('18', '18. Phải trả người bán'),
		])

	TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_TONG_HOP_IDS = fields.One2many('tien.ich.xdct.tmbctc.loai.chi.tieu.tong.hop', 'CHI_TIET_ID_1', string='Xây dựng công thức loại chỉ tiêu tổng hợp')
	TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_CHI_TIET_IDS = fields.One2many('tien.ich.xdct.tmbctc.loai.chi.tieu.chi.tiet', 'CHI_TIET_ID_1', string='Xây dựng công thức loại chỉ tiêu chi tiết')

	@api.model
	def thuc_hien_xoa_cong_thuc_tmbctc(self, args):
		new_line = [[5]]
		if self.LOAI_CHI_TIEU == '1':
			return {'TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_TONG_HOP_IDS': new_line,
					 'CUOI_NAM': '' ,
					}
		elif self.LOAI_CHI_TIEU == '0' or self.LOAI_CHI_TIEU == '2': 
			return {'TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_CHI_TIET_IDS': new_line,
					'CUOI_NAM': '' ,
					}


	@api.model
	def thuc_hien_lay_gia_tri_mac_dinh_tmbctc(self, args):		
		if args['ten_bao_cao'] =='THUYET_MINH_BAO_CAO_TAI_CHINH':
			cong_thuc_tmbctc_tong_hop =[[5]]
			cong_thuc_tmbctc_tien_ich=[[5]]
			chitietmacdinh = self.env['tien.ich.thuyet.minh.bao.cao.tai.chinh.chi.tiet.mac.dinh'].search([('MA_CHI_TIEU', '=', args['ma_chi_tieu'])],limit=1)
			for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_IDS:
					cong_thuc_tmbctc_tong_hop += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'MA_CHI_TIEU' : chitiet_baocaotcchitiet.MA_CHI_TIEU,
					'TEN_CHI_TIEU' : chitiet_baocaotcchitiet.TEN_CHI_TIEU,
				})]

			for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LCT_CHI_TIET_IDS:
				cong_thuc_tmbctc_tien_ich += [(0,0,{
				'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
				'KY_HIEU' : chitiet_baocaotcchitiet.KY_HIEU,
				'DIEN_GIAI' : chitiet_baocaotcchitiet.DIEN_GIAI,
				'TAI_KHOAN_ID' : chitiet_baocaotcchitiet.TAI_KHOAN_ID.id,
				'TK_DOI_UNG_ID' : chitiet_baocaotcchitiet.TK_DOI_UNG_ID.id,
			})]

			return {'TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_TONG_HOP_IDS': cong_thuc_tmbctc_tong_hop , 'TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_CHI_TIET_IDS': cong_thuc_tmbctc_tien_ich}