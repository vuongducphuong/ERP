# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_THUC_HIEN_NGHIA_VU_DOI_VOI_NHA_NUOC_CHI_TIET(models.Model):
	_name = 'tien.ich.thuc.hien.nghia.vu.doi.voi.nha.nuoc.chi.tiet'
	_description = ''
	_inherit = ['mail.thread']
	MA_CHI_TIEU = fields.Char(string='Mã chỉ tiêu', help='Mã chỉ tiêu')
	TEN_CHI_TIEU = fields.Char(string='Tên chỉ tiêu', help='Tên chỉ tiêu')
	TEN_TIENG_ANH = fields.Char(string='Tên tiếng anh', help='Tên tiếng anh')
	LOAI_CHI_TIEU = fields.Selection([('0', 'Chi tiết'), ('1', 'Tổng hợp'), ('2', 'Tiêu đề'),('3', 'Chú thích'), ], string='Loại chỉ tiêu', help='Loại chỉ tiêu', default='0' , required=True)
	SO_CON_PHAI_NOP_KY_TRUOC_CHUYEN_SANG = fields.Char(string='Số còn phải nộp kỳ trước chuyển sang', help='Số còn phải nộp kỳ trước chuyển sang')
	SO_PHAI_NOP_TRONG_KY = fields.Char(string='Số phải nộp trong kỳ', help='Số phải nộp trong kỳ')
	SO_DA_NOP_TRONG_KY = fields.Char(string='Số đã nộp trong kỳ', help='Số đã nộp trong kỳ')
	KHONG_IN = fields.Boolean(string='Không in', help='Không in')
	IN_DAM = fields.Boolean(string='In đậm', help='In đậm')
	IN_NGHIENG = fields.Boolean(string='In nghiêng', help='In nghiêng')
	CHI_TIET_ID_2 = fields.Many2one('tien.ich.thiet.lap.bao.cao.tai.chinh', string='Chi tiết', help='Chi tiết', ondelete='cascade')

	THONG_TU  = fields.Char(string='Thông tư' , help = 'Thông tư')
	name = fields.Char(string='Name', help='Name', oldname='NAME')

	SO_THU_TU = fields.Integer(string='Số thứ tự các dòng chi tiết', help='Số thứ tự các dòng chi tiết')

	TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_CHI_TIET_IDS = fields.One2many('tien.ich.ththnvdvnnpntk.loai.chi.tieu.chi.tiet', 'CHI_TIET_ID', string='Tình hình THNVDVNN PNTK loại chỉ tiêu chi tiết')
	TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_TONG_HOP_IDS = fields.One2many('tien.ich.ththnvdvnnpntk.loai.chi.tieu.tong.hop', 'CHI_TIET_ID', string='Tình hình THNVDVNN PNTK loại chỉ tiêu tổng hợp')
	TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_CHI_TIET_IDS = fields.One2many('tien.ich.ththnvdvnndntk.loai.chi.tieu.chi.tiet', 'CHI_TIET_ID', string='Tình hình THNVDVNN DNTK loại chỉ tiêu chi tiết')
	TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_TONG_HOP_IDS = fields.One2many('tien.ich.ththnvdvnnpnkt.loai.chi.tieu.tong.hop', 'CHI_TIET_ID', string='Tình hình THNVDVNN PNKT loại chỉ tiêu tổng hợp')
	TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_CHI_TIET_IDS = fields.One2many('tien.ich.ththnvdvnnpnkt.loai.chi.tieu.chi.tiet', 'CHI_TIET_ID', string='Tình hình THNVDVNN PNKT loại chỉ tiêu chi tiết ')
	TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_TONG_HOP_IDS = fields.One2many('tien.ich.ththnvdvnndntk.loai.chi.tieu.tong.hop', 'CHI_TIET_ID', string='Tình hình THNVDVNN DNTK loại chỉ tiêu tổng hợp')


	@api.model
	def thuc_hien_xoa_cong_thuc(self, args):
		new_line = [[5]]
		if self.LOAI_CHI_TIEU == '1':
			return {'TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_TONG_HOP_IDS': new_line,
					 'SO_CON_PHAI_NOP_KY_TRUOC_CHUYEN_SANG': '' ,
					}
		else: 
			return {'TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_CHI_TIET_IDS': new_line,
					'SO_CON_PHAI_NOP_KY_TRUOC_CHUYEN_SANG': '' ,
					}

	@api.model
	def thuc_hien_xoa_cong_thuc_1(self, args):
		new_line = [[5]]
		if self.LOAI_CHI_TIEU == '1':
			return {'TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_TONG_HOP_IDS': new_line,
					 'SO_PHAI_NOP_TRONG_KY': '' ,
					}
		else: 
			return {'TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_CHI_TIET_IDS': new_line,
					'SO_PHAI_NOP_TRONG_KY': '' ,
					}
	@api.model
	def thuc_hien_xoa_cong_thuc_2(self, args):
		new_line = [[5]]
		if self.LOAI_CHI_TIEU == '1':
			return {'TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_TONG_HOP_IDS': new_line,
					 'SO_DA_NOP_TRONG_KY': '' ,
					}
		else: 
			return {'TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_CHI_TIET_IDS': new_line,
					'SO_DA_NOP_TRONG_KY': '' ,
					}
	
	@api.model
	def thuc_hien_lay_gia_tri_mac_dinh_phai_nop_ky_truoc(self, args):		

		listchitietmacdinh = self.env['tien.ich.thuc.hien.nghia.vu.doi.voi.nha.nuoc.mac.dinh'].search([('MA_CHI_TIEU', '=', args['ma_chi_tieu'])])
		phai_nop_ky_truoc_cong_thuc_tong_hop =[[5]]
		phai_nop_ky_truoc_cong_thuc_chi_tiet=[[5]]
		
		for chitiet_baocaotcchitiet in listchitietmacdinh.TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_TONG_HOP_MD_IDS:
			phai_nop_ky_truoc_cong_thuc_tong_hop += [(0,0,{
			'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
			'MA_CHI_TIEU' : chitiet_baocaotcchitiet.MA_CHI_TIEU,
			'TEN_CHI_TIEU' : chitiet_baocaotcchitiet.TEN_CHI_TIEU,
		})]

		for chitiet_baocaotcchitiet in listchitietmacdinh.TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_CHI_TIET_MD_IDS:
			phai_nop_ky_truoc_cong_thuc_chi_tiet += [(0,0,{
			'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
			'KY_HIEU' : chitiet_baocaotcchitiet.KY_HIEU,
			'DIEN_GIAI' : chitiet_baocaotcchitiet.DIEN_GIAI,
			'TAI_KHOAN_ID' : chitiet_baocaotcchitiet.TAI_KHOAN_ID,
			'TK_DOI_UNG_ID' : chitiet_baocaotcchitiet.TK_DOI_UNG_ID,
		})]

		return {'TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_TONG_HOP_IDS' : phai_nop_ky_truoc_cong_thuc_tong_hop,
				'TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_CHI_TIET_IDS' : phai_nop_ky_truoc_cong_thuc_chi_tiet,}
	@api.model
	def thuc_hien_lay_gia_tri_mac_dinh_phai_nop_trong_ky(self, args):		
		
		listchitietmacdinh = self.env['tien.ich.thuc.hien.nghia.vu.doi.voi.nha.nuoc.mac.dinh'].search([('MA_CHI_TIEU', '=', args['ma_chi_tieu'])])
		
		phai_nop_trong_ky_cong_thuc_tong_hop =[[5]]
		phai_nop_trong_ky_cong_thuc_chi_tiet=[[5]]
		
		
		for chitiet_baocaotcchitiet in listchitietmacdinh.TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_TONG_HOP_MD_IDS:
			phai_nop_trong_ky_cong_thuc_tong_hop += [(0,0,{
			'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
			'MA_CHI_TIEU' : chitiet_baocaotcchitiet.MA_CHI_TIEU,
			'TEN_CHI_TIEU' : chitiet_baocaotcchitiet.TEN_CHI_TIEU,
		})]

		for chitiet_baocaotcchitiet in listchitietmacdinh.TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_CHI_TIET_MD_IDS:
			phai_nop_trong_ky_cong_thuc_chi_tiet += [(0,0,{
			'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
			'KY_HIEU' : chitiet_baocaotcchitiet.KY_HIEU,
			'DIEN_GIAI' : chitiet_baocaotcchitiet.DIEN_GIAI,
			'TAI_KHOAN_ID' : chitiet_baocaotcchitiet.TAI_KHOAN_ID,
			'TK_DOI_UNG_ID' : chitiet_baocaotcchitiet.TK_DOI_UNG_ID,
		})]
			
		
		return {'TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_CHI_TIET_IDS' : phai_nop_trong_ky_cong_thuc_chi_tiet,
				'TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_TONG_HOP_IDS' : phai_nop_trong_ky_cong_thuc_tong_hop,}
	
	@api.model
	def thuc_hien_lay_gia_tri_mac_dinh_da_nop_trong_ky(self, args):		
		
		listchitietmacdinh = self.env['tien.ich.thuc.hien.nghia.vu.doi.voi.nha.nuoc.mac.dinh'].search([('MA_CHI_TIEU', '=', args['ma_chi_tieu'])])

		da_nop_trong_ky_cong_thuc_tong_hop =[[5]]
		da_nop_trong_ky_cong_thuc_chi_tiet=[[5]]

		for chitiet_baocaotcchitiet in listchitietmacdinh.TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_TONG_HOP_MD_IDS:
			da_nop_trong_ky_cong_thuc_tong_hop += [(0,0,{
			'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
			'MA_CHI_TIEU' : chitiet_baocaotcchitiet.MA_CHI_TIEU,
			'TEN_CHI_TIEU' : chitiet_baocaotcchitiet.TEN_CHI_TIEU,
		})]
			
		for chitiet_baocaotcchitiet in listchitietmacdinh.TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_CHI_TIET_MD_IDS:
			da_nop_trong_ky_cong_thuc_chi_tiet += [(0,0,{
			'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
			'KY_HIEU' : chitiet_baocaotcchitiet.KY_HIEU,
			'DIEN_GIAI' : chitiet_baocaotcchitiet.DIEN_GIAI,
			'TAI_KHOAN_ID' : chitiet_baocaotcchitiet.TAI_KHOAN_ID,
			'TK_DOI_UNG_ID' : chitiet_baocaotcchitiet.TK_DOI_UNG_ID,
		})]
		
		return {'TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_CHI_TIET_IDS' : da_nop_trong_ky_cong_thuc_chi_tiet,
				'TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_TONG_HOP_IDS' : da_nop_trong_ky_cong_thuc_tong_hop}