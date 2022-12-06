# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper

class TIEN_ICH_BAO_CAO_TAI_CHINH_CHI_TIET(models.Model):
	_name = 'tien.ich.bao.cao.tai.chinh.chi.tiet'
	_description = ''
	
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
	CHI_TIET_ID = fields.Many2one('tien.ich.thiet.lap.bao.cao.tai.chinh', string='Chi tiết ', help='Chi tiết', ondelete='cascade')
	name = fields.Char(string='Name', help='Name', oldname='NAME', related='MA_CHI_TIEU')
	SO_THU_TU = fields.Integer(string='Số thứ tự các dòng chi tiết', help='Số thứ tự các dòng chi tiết')
	THONG_TU  = fields.Char(string='Thông tư' , help = 'Thông tư')
	ID_CHI_TIEU = fields.Char(string='GUID', help='Trường lưu id của master chỉ tiêu', default=helper.Obj.create_guid())

	ReportID  = fields.Integer(string='Loại báo cáo' , help = 'Loại báo cáo')

	TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_TONG_HOP_IDS = fields.One2many('tien.ich.xay.dung.cong.thuc.loai.chi.tieu.tong.hop', 'CHI_TIET_ID', string='Xây dựng công thức loại chỉ tiêu tổng hợp')
	TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_CHI_TIET_IDS = fields.One2many('tien.ich.xay.dung.cong.thuc.loai.chi.tieu.chi.tiet', 'CHI_TIET_ID', string='Xây dựng công thức loại chỉ tiêu chi tiết')

	@api.model
	def thuc_hien_xoa_cong_thuc(self, args):
		new_line = [[5]]
		if self.LOAI_CHI_TIEU == '1':
			return {'TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_TONG_HOP_IDS': new_line,
					 'CONG_THUC': '' ,
					}
		else: 
			return {'TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_CHI_TIET_IDS': new_line,
					'CONG_THUC': '' ,
					}

	@api.model
	def thuc_hien_lay_gia_tri_mac_dinh(self, args):		
		if args['ten_bao_cao'] =='BANG_CAN_DOI_KE_TOAN':
			cong_thuc_tong_hop =[[5]]
			cong_thuc_tien_ich=[[5]]
			chitietmacdinh = self.env['tien.ich.bao.cao.tai.chinh.chi.tiet.mac.dinh'].search([('ReportID', '=', '1'),('MA_CHI_TIEU', '=', args['ma_chi_tieu'])])
			for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_XAY_DUNG_CONG_THUC_IDS:
					cong_thuc_tong_hop += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'MA_CHI_TIEU' : chitiet_baocaotcchitiet.MA_CHI_TIEU,
					'TEN_CHI_TIEU' : chitiet_baocaotcchitiet.TEN_CHI_TIEU,
				})]

			for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_XAY_DUNG_CONG_THUC_LCT_CHI_TIET_IDS:
				cong_thuc_tien_ich += [(0,0,{
				'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
				'KY_HIEU' : chitiet_baocaotcchitiet.KY_HIEU,
				'DIEN_GIAI' : chitiet_baocaotcchitiet.DIEN_GIAI,
				'TAI_KHOAN_ID' : chitiet_baocaotcchitiet.TAI_KHOAN_ID.id,
				'TK_DOI_UNG_ID' : chitiet_baocaotcchitiet.TK_DOI_UNG_ID.id,
			})]

			return {'TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_TONG_HOP_IDS': cong_thuc_tong_hop , 'TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_CHI_TIET_IDS': cong_thuc_tien_ich}
 
