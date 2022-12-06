# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from datetime import datetime

class ACCOUNT_EX_NHAP_SO_DU_BAN_DAU(models.Model):
	_name = 'account.ex.nhap.so.du.ban.dau'
	_description = 'Nhập số dư ban đầu'
	
	MA = fields.Char(string='Ma', help='Ma')
	name = fields.Char(string='Name', help='Name', default='Nhập số dư ban đầu', oldname='NAME')
	SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
	SO_CONG_NO_ID = fields.Many2one('so.cong.no', ondelete='set null')
	KHO_ID = fields.Many2one('danh.muc.kho', string='Kho', help='Kho')
	ACCOUNT_EX_CONG_NO_KHACH_HANG_IDS = fields.One2many('account.ex.cong.no.khach.hang', 'SO_DU_BAN_DAU_ID', string='Công nợ khách hàng')
	ACCOUNT_EX_CHI_PHI_DO_DANG_IDS = fields.One2many('account.ex.chi.phi.do.dang', 'SO_DU_BAN_DAU_ID', string='Chi phí dở dang')
	ACCOUNT_EX_SO_DU_TAI_KHOAN_IDS = fields.One2many('account.ex.so.du.tai.khoan', 'SO_DU_BAN_DAU_ID', string='Số dư tài khoản')
	ACCOUNT_EX_CONG_NO_NHAN_VIEN_IDS = fields.One2many('account.ex.cong.no.nhan.vien', 'SO_DU_TAI_KHOAN_ID', string='công nợ nhân viên')
	ACCOUNT_EX_SO_DU_TK_NGAN_HANG_IDS = fields.One2many('account.ex.so.du.tk.ngan.hang', 'SO_DU_BAN_DAU_ID', string='Số dư TK ngân hàng')
	ACCOUNT_EX_CONG_NO_NHA_CUNG_CAP_IDS = fields.One2many('account.ex.cong.no.nha.cung.cap', 'SO_DU_BAN_DAU_ID', string='Công nợ nhà cung cấp')
	ACCOUNT_EX_TON_KHO_VAT_TU_HANG_HOA_IDS = fields.One2many('account.ex.ton.kho.vat.tu.hang.hoa', 'SO_DU_BAN_DAU_ID', string='Tồn kho vật tư hàng hóa')
	ACCOUNT_EX_KHAI_BAO_CHI_PHI_CHUNG_CAN_PHAN_BO_IDS = fields.One2many('account.ex.khai.bao.chi.phi.chung.can.phan.bo', 'SO_DU_BAN_DAU_ID', string='Khai báo chi phí chung cần phân bổ')
	# Khai báo các trường loại tiền tương ứng với các tab ở view
	# loại tiền của tab số dư ngân hàng
	LOAI_TIEN_ID_SO_DU_TAI_KHOAN = fields.Many2one('res.currency', string='Loại tiền')
	# tab số dư tk ngân hàng
	LOAI_TIEN_ID_SO_DU_TK_NGAN_HANG = fields.Many2one('res.currency', string='Loại tiền')
	# tab công nợ khách hàng
	LOAI_TIEN_ID_SO_CONG_NO_KHACH_HANG = fields.Many2one('res.currency', string='Loại tiền')
	# tab công nợ nhà cung cấp
	LOAI_TIEN_ID_SO_CONG_NO_NHA_CUNG_CAP = fields.Many2one('res.currency', string='Loại tiền')
	# tab công nợ nhân viên
	LOAI_TIEN_ID_SO_CONG_NO_NHAN_VIEN = fields.Many2one('res.currency', string='Loại tiền')
	

	#  khai báo các trường dùng để ẩn hiện các cột theo trường loại tiền ở các tab thay đổi
	CO_HACH_TOAN_NGOAI_TE_SO_DU_TAI_KHOAN = fields.Boolean(default=True)
	CO_HACH_TOAN_NGOAI_TE_SO_DU_TK_NGAN_HANG = fields.Boolean(default=True)
	CO_HACH_TOAN_NGOAI_TE_SO_CONG_NO_KHACH_HANG = fields.Boolean(default=True)
	CO_HACH_TOAN_NGOAI_TE_SO_CONG_NO_NHA_CUNG_CAP= fields.Boolean(default=True)
	CO_HACH_TOAN_NGOAI_TE_SO_CONG_NO_NHAN_VIEN = fields.Boolean(default=True)
	ACCOUNT_EX_NHAP_SO_DU_BAN_DAU_CHI_TIET_IDS = fields.One2many('account.ex.nhap.so.du.ban.dau.chi.tiet', 'NHAP_SO_DU_BAN_DAU_ID', string='Nhập số dư ban đầu chi tiết')

	chi_phi_do_dang = fields.Selection([
		('DT_THCP', 'Đối tượng tập hợp chi phí'),
		('CONG_TRINH', 'Công trình'),
		('DON_HANG', 'Đơn hàng'),
		('HOP_DONG', 'Hợp đồng'),   
		('CHI_PHI_PB', 'Chi phí chung cần phân bổ'),
		], default='HOP_DONG', string='NO_SAVE')
	
	IS_DT_THCP = fields.Boolean(default='False')
	IS_CONG_TRINH = fields.Boolean(default='False')
	IS_DON_HANG = fields.Boolean(default='False')
	IS_HOP_DONG = fields.Boolean(default='True')
	IS_CHI_TIET = fields.Boolean()

	@api.onchange('chi_phi_do_dang')
	def _onchange_chi_phi_do_dang(self):
		if self.chi_phi_do_dang:
			config = self.env['gia.thanh.cau.hinh.so.du.dau.ky'].search([],limit=1)
			if self.chi_phi_do_dang == 'DT_THCP':
				self.IS_CHI_TIET = config.CHI_TIET_THEO_DTTHCP
			elif self.chi_phi_do_dang == 'CONG_TRINH':
				self.IS_CHI_TIET = config.CHI_TIET_THEO_CONG_TRINH
			elif self.chi_phi_do_dang == 'DON_HANG':
				self.IS_CHI_TIET = config.CHI_TIET_THEO_DON_HANG
			elif self.chi_phi_do_dang == 'HOP_DONG':
				self.IS_CHI_TIET = config.CHI_TIET_THEO_HOP_DONG

			

	@api.onchange('LOAI_TIEN_ID_SO_DU_TAI_KHOAN')
	def _onchange_LOAI_TIEN_ID_SO_DU_TAI_KHOAN(self):
		ten_loai_tien = ''
		if self.LOAI_TIEN_ID_SO_DU_TAI_KHOAN.id != -1:
			ten_loai_tien = self.LOAI_TIEN_ID_SO_DU_TAI_KHOAN.MA_LOAI_TIEN
		if ten_loai_tien == 'VND' or self.LOAI_TIEN_ID_SO_DU_TAI_KHOAN.id == -1:
			self.CO_HACH_TOAN_NGOAI_TE_SO_DU_TAI_KHOAN = False
		else:
			self.CO_HACH_TOAN_NGOAI_TE_SO_DU_TAI_KHOAN = True

	@api.onchange('LOAI_TIEN_ID_SO_DU_TK_NGAN_HANG')
	def _onchange_LOAI_TIEN_ID_SO_DU_TK_NGAN_HANG(self):
		ten_loai_tien = ''
		if self.LOAI_TIEN_ID_SO_DU_TK_NGAN_HANG.id != -1:
			ten_loai_tien = self.LOAI_TIEN_ID_SO_DU_TK_NGAN_HANG.MA_LOAI_TIEN
		if ten_loai_tien == 'VND' or self.LOAI_TIEN_ID_SO_DU_TK_NGAN_HANG.id == -1:
			self.CO_HACH_TOAN_NGOAI_TE_SO_DU_TK_NGAN_HANG = False
		else:
			self.CO_HACH_TOAN_NGOAI_TE_SO_DU_TK_NGAN_HANG = True

	@api.onchange('LOAI_TIEN_ID_SO_CONG_NO_KHACH_HANG')
	def _onchange_LOAI_TIEN_ID_SO_CONG_NO_KHACH_HANG(self):
		ten_loai_tien = ''
		if self.LOAI_TIEN_ID_SO_CONG_NO_KHACH_HANG.id != -1:
			ten_loai_tien = self.LOAI_TIEN_ID_SO_CONG_NO_KHACH_HANG.MA_LOAI_TIEN
		if ten_loai_tien == 'VND' or self.LOAI_TIEN_ID_SO_CONG_NO_KHACH_HANG.id == -1:
			self.CO_HACH_TOAN_NGOAI_TE_SO_CONG_NO_KHACH_HANG = False
		else:
			self.CO_HACH_TOAN_NGOAI_TE_SO_CONG_NO_KHACH_HANG = True

	@api.onchange('LOAI_TIEN_ID_SO_CONG_NO_NHA_CUNG_CAP')
	def _onchange_LOAI_TIEN_ID_SO_CONG_NO_NHA_CUNG_CAP(self):
		ten_loai_tien = ''
		if self.LOAI_TIEN_ID_SO_CONG_NO_NHA_CUNG_CAP.id != -1:
			ten_loai_tien = self.LOAI_TIEN_ID_SO_CONG_NO_NHA_CUNG_CAP.MA_LOAI_TIEN
		if ten_loai_tien == 'VND' or self.LOAI_TIEN_ID_SO_CONG_NO_NHA_CUNG_CAP.id == -1:
			self.CO_HACH_TOAN_NGOAI_TE_SO_CONG_NO_NHA_CUNG_CAP = False
		else:
			self.CO_HACH_TOAN_NGOAI_TE_SO_CONG_NO_NHA_CUNG_CAP = True


	@api.onchange('LOAI_TIEN_ID_SO_CONG_NO_NHAN_VIEN')
	def _onchange_LOAI_TIEN_ID_SO_CONG_NO_NHAN_VIEN(self):
		ten_loai_tien = ''
		if self.LOAI_TIEN_ID_SO_CONG_NO_NHAN_VIEN.id != -1:
			ten_loai_tien = self.LOAI_TIEN_ID_SO_CONG_NO_NHAN_VIEN.MA_LOAI_TIEN
		if ten_loai_tien == 'VND' or self.LOAI_TIEN_ID_SO_CONG_NO_NHAN_VIEN.id == -1:
			self.CO_HACH_TOAN_NGOAI_TE_SO_CONG_NO_NHAN_VIEN = False
		else:
			self.CO_HACH_TOAN_NGOAI_TE_SO_CONG_NO_NHAN_VIEN = True

	# @api.onchange('currency_id')
	# def thay_doi_loai_tien(self):
	# 	self.load_form()
	# 	ten_loai_tien = self.env['res.currency'].search([('id', '=', self.currency_id.id)],limit=1).name
	# 	if ten_loai_tien=='VND':
	# 		self.IS_LOAI_TIEN = False
	# 	else:
	# 		self.IS_LOAI_TIEN = True
		

	@api.model
	def default_get(self,default_fields):
		res = super(ACCOUNT_EX_NHAP_SO_DU_BAN_DAU, self).default_get(default_fields)
		
		res['LOAI_TIEN_ID_SO_DU_TAI_KHOAN'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'VND')], limit=1).id
		res['LOAI_TIEN_ID_SO_DU_TK_NGAN_HANG'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'VND')], limit=1).id
		res['LOAI_TIEN_ID_SO_CONG_NO_KHACH_HANG'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'VND')], limit=1).id
		res['LOAI_TIEN_ID_SO_CONG_NO_NHA_CUNG_CAP'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'VND')], limit=1).id
		res['LOAI_TIEN_ID_SO_CONG_NO_NHAN_VIEN'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'VND')], limit=1).id
		res['KHO_ID'] = -1

		return res


	@api.model
	def load_form(self,args):
		new_line_ton_kho_vthh = [[5]]
		new_line_ton_cpdd = [[5]]
		lay_du_lieu_vthh = self.lay_du_lieu_vthh(-1,self.get_chi_nhanh())
		lay_du_lieu_chi_phi_do_dang = self.lay_du_lieu_chi_phi_do_dang(4,self.get_chi_nhanh())
			
		if lay_du_lieu_vthh:
			for vthh in lay_du_lieu_vthh:
				# if vthh.get('SO_LUONG',0) > 0:
				new_line_ton_kho_vthh += [(0, 0, {
					'MA_HANG_ID': [vthh.get('MA_HANG_ID'),vthh.get('MA_HANG')],
					'TEN_HANG': vthh.get('TEN_HANG'),
					'LIST_NHOM_VTHH': vthh.get('LIST_NHOM_VTHH'),
					'DVT_ID': [vthh.get('DVT_ID'),vthh.get('TEN_DVT')],
					'KHO_ID': [vthh.get('KHO_ID'),vthh.get('MA_KHO')],
					'SO_LUONG': vthh.get('SO_LUONG'),
					'GIA_TRI_TON': vthh.get('GIA_TRI_TON'),
					'SO_LO': vthh.get('SO_LO'),
					'HAN_SU_DUNG': vthh.get('HAN_SU_DUNG'),
					'SO_LUONG_THEO_DVT_CHINH': vthh.get('SO_LUONG_THEO_DVT_CHINH'),
					'CHI_TIET_VTHH' : 1,
					'TY_LE_CHUYEN_DOI_THEO_DVT_CHINH': vthh.get('TY_LE_CHUYEN_DOI_THEO_DVT_CHINH'),
					})]

		if lay_du_lieu_chi_phi_do_dang:
			for cpdd in lay_du_lieu_chi_phi_do_dang:
				new_line_ton_cpdd += [(0, 0, {
					'HOP_DONG_ID' : [cpdd.get('HOP_DONG_ID'),cpdd.get('SO_HOP_DONG')],
					'NGAY_KY' : cpdd.get('NGAY_KY'),
					'TRICH_YEU' : cpdd.get('TRICH_YEU'),
					'KHACH_HANG_ID' : [cpdd.get('DOI_TUONG_ID'),cpdd.get('TEN_DOI_TUONG')],
					'CHI_PHI_NVL_TRUC_TIEP' : cpdd.get('CHI_PHI_NVL_TRUC_TIEP_DAU_KY'),
					'CHI_PHI_NHAN_CONG_TRUC_TIEP' : cpdd.get('CHI_PHI_NHAN_CONG_TRUC_TIEP',0),
					'CHI_PHI_KHAC_CHUNG' : cpdd.get('CHI_PHI_KHAC_CHUNG',0),
					'TONG_CHI_PHI' : cpdd.get('TONG_CHI_PHI',0),
					'SO_DA_NGHIEM_THU' : cpdd.get('SO_DA_NGHIEM_THU',0),
					'SO_CHUA_NGHIEM_THU' : cpdd.get('SO_CHUA_NGHIEM_THU',0),
					'TAI_KHOAN_CPSXKD_DO_DANG_ID' : [cpdd.get('TAI_KHOAN_CPSXKD_DO_DANG_ID',0),cpdd.get('MA_TAI_KHOAN_CPDD',0)],
					'LOAI_CHI_PHI_DO_DANG' : '4',
					'BAC' : 2,
					'isparent' : False,
					})]
		return {'ACCOUNT_EX_NHAP_SO_DU_BAN_DAU_CHI_TIET_IDS': self.lay_du_tai_khoan(self.LOAI_TIEN_ID_SO_DU_TAI_KHOAN.id),
				'ACCOUNT_EX_SO_DU_TK_NGAN_HANG_IDS': self.lay_du_lieu_so_du_tai_khoan(self.LOAI_TIEN_ID_SO_DU_TK_NGAN_HANG.id,self.get_chi_nhanh(),3),
				'ACCOUNT_EX_CONG_NO_KHACH_HANG_IDS' :self.lay_du_lieu_so_du_tai_khoan(self.LOAI_TIEN_ID_SO_CONG_NO_KHACH_HANG.id,self.get_chi_nhanh(),1),
				'ACCOUNT_EX_CONG_NO_NHA_CUNG_CAP_IDS' : self.lay_du_lieu_so_du_tai_khoan(self.LOAI_TIEN_ID_SO_CONG_NO_NHA_CUNG_CAP.id,self.get_chi_nhanh(),0),
				'ACCOUNT_EX_CONG_NO_NHAN_VIEN_IDS': self.lay_du_lieu_so_du_tai_khoan(self.LOAI_TIEN_ID_SO_CONG_NO_NHAN_VIEN.id,self.get_chi_nhanh(),2),
				'ACCOUNT_EX_TON_KHO_VAT_TU_HANG_HOA_IDS' : new_line_ton_kho_vthh,
				'ACCOUNT_EX_CHI_PHI_DO_DANG_IDS' : new_line_ton_cpdd,
				}

	def lay_du_lieu_cpdd(self, args):
		new_line = [[5]]
		if args.get('loai_cpdd') == 'CONG_TRINH':
			du_lieu_cong_trinh = self.lay_du_lieu_chi_phi_do_dang(2,self.get_chi_nhanh())
			if du_lieu_cong_trinh:
				for ct in du_lieu_cong_trinh:
					new_line += [(0,0,{
						# 'parent_id': [record.parent_id.id, record.parent_id.TEN_CONG_TRINH],
						'MA_CONG_TRINH_ID' : [ct.get('CONG_TRINH_ID'), '\xa0\xa0\xa0\xa0' * ct.get('BAC', 0) + ct.get('MA_CONG_TRINH')],
						'TEN_CONG_TRINH' : ct.get('TEN_CONG_TRINH'),
						'LOAI_CONG_TRINH' : [ct.get('LOAI'),ct.get('TEN_LOAI_CONG_TRINH')],
						'CHI_PHI_NVL_TRUC_TIEP' : ct.get('CHI_PHI_NVL_TRUC_TIEP'),
						'CHI_PHI_NVL_GIAN_TIEP' : ct.get('CHI_PHI_NVL_GIAN_TIEP'),
						'CHI_PHI_MUA_NGOAI' : ct.get('CHI_PHI_MUA_NGOAI'),
						'CHI_PHI_NHAN_CONG_TRUC_TIEP' : ct.get('CHI_PHI_NHAN_CONG_TRUC_TIEP'),
						'MTC_TONG' : ct.get('MTC_TONG'),
						'CHI_PHI_KHAC_CHUNG' : ct.get('CHI_PHI_KHAC_CHUNG'),
						'MTC_CHI_PHI_NVL_GIAN_TIEP' : ct.get('MTC_CHI_PHI_NVL_GIAN_TIEP'),
						'MTC_CHI_PHI_NHAN_CONG' : ct.get('MTC_CHI_PHI_NHAN_CONG'),
						'MTC_CHI_PHI_KHAU_HAO_DAU_KY' : ct.get('MTC_CHI_PHI_KHAU_HAO_DAU_KY'),
						'MTC_CHI_PHI_MUA_NGOAI_DAU_KY' : ct.get('MTC_CHI_PHI_MUA_NGOAI_DAU_KY'),
						'MTC_CHI_PHI_KHAC_CHUNG' : ct.get('MTC_CHI_PHI_KHAC_CHUNG'),
						'MTC_TONG' : ct.get('MTC_TONG'),
						'MTC_CHI_PHI_NHAN_CONG' : ct.get('MTC_CHI_PHI_NHAN_CONG'),
						'CHI_PHI_NHAN_CONG_GIAN_TIEP' : ct.get('CHI_PHI_NHAN_CONG_GIAN_TIEP'),
						'CHI_PHI_KHAU_HAO' : ct.get('CHI_PHI_KHAU_HAO'),
						'MTC_CHI_PHI_MUA_NGOAI_DAU_KY' : ct.get('MTC_CHI_PHI_MUA_NGOAI_DAU_KY'),
						'CHI_PHI_KHAC_CHUNG' : ct.get('CHI_PHI_KHAC_CHUNG'),
						'TONG_CHI_PHI' : ct.get('TONG_CHI_PHI'),
						'TONG' : ct.get('TONG'),
						'LOAI_CHI_PHI_DO_DANG' : '2',
						'BAC' : ct.get('BAC'),
						'isparent' : ct.get('isparent'),

						# 'CHI_PHI_NHAN_CONG_TRUC_TIEP' : ct.get('CHI_PHI_NHAN_CONG_TRUC_TIEP',0),
						# 'MTC_CHI_PHI_KHAC_CHUNG' : ct.get('MTC_CHI_PHI_KHAC_CHUNG',0),
						# 'TONG_CHI_PHI' : 2,#ct.get('TONG_CHI_PHI',0),
						'SO_DA_NGHIEM_THU' : ct.get('SO_DA_NGHIEM_THU',0),
						'SO_CHUA_NGHIEM_THU' : ct.get('SO_CHUA_NGHIEM_THU',0),
						'TAI_KHOAN_CPSXKD_DO_DANG_ID' : [ct.get('TAI_KHOAN_CPSXKD_DO_DANG_ID',0),ct.get('MA_TAI_KHOAN_CPDD',0)],
						})]
		elif args.get('loai_cpdd') == 'DT_THCP':
			du_lieu_dtthcp = self.lay_du_lieu_chi_phi_do_dang(1,self.get_chi_nhanh())
			if du_lieu_dtthcp:
				ten_loai_dtthcp = ''
				for thcp in du_lieu_dtthcp:
					if thcp.get('LOAI_DTTHCP') == '0':
						ten_loai_dtthcp = 'Phân xưởng'
					elif thcp.get('LOAI_DTTHCP') == '1':
						ten_loai_dtthcp = 'Sản phẩm'
					elif thcp.get('LOAI_DTTHCP') == '2':
						ten_loai_dtthcp = 'Quy trình sản xuất'
					elif thcp.get('LOAI_DTTHCP') == '3':
						ten_loai_dtthcp = 'Công đoạn'
					new_line += [(0,0,{
						'MA_DOI_TUONG_THCP_ID' : [thcp.get('DTTHCP_ID'), '\xa0\xa0\xa0\xa0' * thcp.get('BAC', 0) + thcp.get('MA_DOI_TUONG_THCP')],
						'TEN_DOI_TUONG_THCP' : thcp.get('TEN_DOI_TUONG_THCP'),
						'LOAI_DOI_TUONG_THCP' : ten_loai_dtthcp,
						'CHI_PHI_NVL_TRUC_TIEP' : thcp.get('CHI_PHI_NVL_TRUC_TIEP'),
						'CHI_PHI_NHAN_CONG_TRUC_TIEP' : thcp.get('CHI_PHI_NHAN_CONG_TRUC_TIEP',0),
						'CHI_PHI_NVL_GIAN_TIEP' : thcp.get('CHI_PHI_NVL_GIAN_TIEP',0),
						'CHI_PHI_NHAN_CONG_GIAN_TIEP' : thcp.get('CHI_PHI_NHAN_CONG_GIAN_TIEP',0),
						'CHI_PHI_KHAU_HAO' : thcp.get('CHI_PHI_KHAU_HAO',0),
						'CHI_PHI_MUA_NGOAI' : thcp.get('CHI_PHI_MUA_NGOAI',0),
						'CHI_PHI_KHAC_CHUNG' : thcp.get('CHI_PHI_KHAC_CHUNG',0),
						'TONG_CHI_PHI' : thcp.get('TONG_CHI_PHI',0),
						'TONG' : thcp.get('TONG',0),
						'SO_DA_NGHIEM_THU' : thcp.get('SO_DA_NGHIEM_THU',0),
						'SO_CHUA_NGHIEM_THU' : thcp.get('SO_CHUA_NGHIEM_THU',0),
						'TAI_KHOAN_CPSXKD_DO_DANG_ID' : [thcp.get('TAI_KHOAN_CPSXKD_DO_DANG_ID',0),thcp.get('MA_TAI_KHOAN_CPDD',0)],
						'LOAI_CHI_PHI_DO_DANG' : '1',
						'BAC' : thcp.get('BAC'),
						'isparent' : thcp.get('isparent'),
						})]
		
		elif args.get('loai_cpdd') == 'DON_HANG':
			du_lieu_don_hang = self.lay_du_lieu_chi_phi_do_dang(3,self.get_chi_nhanh())
			if du_lieu_don_hang:
				for dh in du_lieu_don_hang:
					new_line += [(0,0,{
						'DON_HANG_ID' : [dh.get('DON_HANG_ID'),dh.get('SO_DON_HANG')],
						'NGAY_DON_HANG' : dh.get('NGAY_DON_HANG'),
						'DIEN_GIAI' : dh.get('DIEN_GIAI'),
						'KHACH_HANG_ID' : [dh.get('DOI_TUONG_ID'),dh.get('TEN_DOI_TUONG')],

						'CHI_PHI_NVL_TRUC_TIEP' : dh.get('CHI_PHI_NVL_TRUC_TIEP'),
						'CHI_PHI_NHAN_CONG_TRUC_TIEP' : dh.get('CHI_PHI_NHAN_CONG_TRUC_TIEP',0),
						'CHI_PHI_NVL_GIAN_TIEP' : dh.get('CHI_PHI_NVL_GIAN_TIEP',0),
						'CHI_PHI_NHAN_CONG_GIAN_TIEP' : dh.get('CHI_PHI_NHAN_CONG_GIAN_TIEP',0),
						'CHI_PHI_KHAU_HAO' : dh.get('CHI_PHI_KHAU_HAO',0),
						'CHI_PHI_MUA_NGOAI' : dh.get('CHI_PHI_MUA_NGOAI',0),
						'CHI_PHI_KHAC_CHUNG' : dh.get('CHI_PHI_KHAC_CHUNG',0),
						'TONG_CHI_PHI' : dh.get('TONG_CHI_PHI',0),
						'TONG' : dh.get('TONG',0),
						'SO_DA_NGHIEM_THU' : dh.get('SO_DA_NGHIEM_THU',0),
						'SO_CHUA_NGHIEM_THU' : dh.get('SO_CHUA_NGHIEM_THU',0),
						'TAI_KHOAN_CPSXKD_DO_DANG_ID' : [dh.get('TAI_KHOAN_CPSXKD_DO_DANG_ID',0),dh.get('MA_TAI_KHOAN_CPDD',0)],
						'LOAI_CHI_PHI_DO_DANG' : '3',
						'BAC' : 2,
						'isparent' : False,
						})]

		elif args.get('loai_cpdd') == 'HOP_DONG':
			du_lieu_hop_dong = self.lay_du_lieu_chi_phi_do_dang(4,self.get_chi_nhanh())
			if du_lieu_hop_dong:
				for hd in du_lieu_hop_dong:
					new_line += [(0,0,{
						'HOP_DONG_ID' : [hd.get('HOP_DONG_ID'),hd.get('SO_HOP_DONG')],
						'NGAY_KY' : hd.get('NGAY_KY'),
						'TRICH_YEU' : hd.get('TRICH_YEU'),
						'KHACH_HANG_ID' : [hd.get('DOI_TUONG_ID'),hd.get('TEN_DOI_TUONG')],
						'CHI_PHI_NVL_TRUC_TIEP' : hd.get('CHI_PHI_NVL_TRUC_TIEP'),
						'CHI_PHI_NHAN_CONG_TRUC_TIEP' : hd.get('CHI_PHI_NHAN_CONG_TRUC_TIEP'),
						'CHI_PHI_NVL_GIAN_TIEP' : hd.get('CHI_PHI_NVL_GIAN_TIEP'),
						'CHI_PHI_NHAN_CONG_GIAN_TIEP' : hd.get('CHI_PHI_NHAN_CONG_GIAN_TIEP'),
						'CHI_PHI_KHAU_HAO' : hd.get('CHI_PHI_KHAU_HAO'),
						'CHI_PHI_MUA_NGOAI' : hd.get('CHI_PHI_MUA_NGOAI',0),
						'CHI_PHI_KHAC_CHUNG' : hd.get('CHI_PHI_KHAC_CHUNG',0),
						'TONG_CHI_PHI' : hd.get('TONG_CHI_PHI',0),
						'TONG' : hd.get('TONG',0),
						'SO_DA_NGHIEM_THU' : hd.get('SO_DA_NGHIEM_THU',0),
						'SO_CHUA_NGHIEM_THU' : hd.get('SO_CHUA_NGHIEM_THU',0),
						'TAI_KHOAN_CPSXKD_DO_DANG_ID' : [hd.get('TAI_KHOAN_CPSXKD_DO_DANG_ID',0),hd.get('MA_TAI_KHOAN_CPDD',0)],
						'LOAI_CHI_PHI_DO_DANG' : '4',
						'BAC' : 2,
						'isparent' : False,
						})]

		elif args.get('loai_cpdd') == 'CHI_PHI_PB':
			du_lieu_hop_dong = self.lay_du_lieu_chi_phi_do_dang(6,self.get_chi_nhanh())
			if du_lieu_hop_dong:
				for cpc in du_lieu_hop_dong:
					new_line += [(0,0,{
						'KHOAN_MUC_CP_ID' : [cpc.get('KHOAN_MUC_CP_ID'),cpc.get('MA_KHOAN_MUC_CP')],
						'TEN_KHOAN_MUC_CP' : cpc.get('TEN_KHOAN_MUC_CP'),
						'SO_TIEN' : cpc.get('SO_TIEN'),
						'LA_TONG_HOP' : cpc.get('LA_TONG_HOP'),
						})]

		if args.get('loai_cpdd') == 'CHI_PHI_PB':
			return {'ACCOUNT_EX_KHAI_BAO_CHI_PHI_CHUNG_CAN_PHAN_BO_IDS': new_line}
		else:
			return {'ACCOUNT_EX_CHI_PHI_DO_DANG_IDS': new_line}

	def lay_du_tai_khoan_ui(self,args):
		return {'ACCOUNT_EX_NHAP_SO_DU_BAN_DAU_CHI_TIET_IDS': self.lay_du_tai_khoan(args['id_loai_tien'])}
		
	def lay_du_tai_khoan(self,loai_tien_id):
		new_line_so_du_tk = [[5]]
		record =[]
		chi_nhanh = self.get_chi_nhanh()
		ngay_bat_dau = datetime.today().strftime('%Y-%m-%d')
		if self.env['ir.config_parameter'].get_param('he_thong.TU_NGAY_BAT_DAU_TAI_CHINH'):
			ngay_bat_dau = self.env['ir.config_parameter'].get_param('he_thong.TU_NGAY_BAT_DAU_TAI_CHINH')
		
		if self.env['res.currency'].search([('id', '=', loai_tien_id)], limit=1).MA_LOAI_TIEN == 'VND' or loai_tien_id == -1:
			co_hach_toan_ngoai_te = False
		else:
			co_hach_toan_ngoai_te = True
		params = {
			'currency_id': loai_tien_id,
			'CO_HACH_TOAN_NGOAI_TE' : co_hach_toan_ngoai_te,
			'CHI_NHANH_ID' : chi_nhanh,
			'NGAY_BAT_DAU' : ngay_bat_dau
			}

		query = """   

		DO LANGUAGE plpgsql $$ DECLARE
  tham_so_loai_tien_id          INTEGER := %(currency_id)s;
  tham_so_co_hach_toan_ngoai_te BOOLEAN := %(CO_HACH_TOAN_NGOAI_TE)s;
  tham_so_hien_thi_tren_so      INTEGER :=0;
  tham_so_chi_nhanh_id          INTEGER := %(CHI_NHANH_ID)s;
  tham_so_ngay_bat_dau          DATE := %(NGAY_BAT_DAU)s;
  tham_so_goi_form_chi_tiet     INTEGER :=0;

  msc_loai_tai_khoan            VARCHAR(50) :='3';
  msc_tong_hop_loai_tien        INTEGER :=-1;
  int_grade                     INTEGER :=0;

BEGIN

  IF tham_so_loai_tien_id = msc_tong_hop_loai_tien
  THEN
	DROP TABLE IF EXISTS TMP_OPN_DATA_2;
	CREATE TEMP TABLE TMP_OPN_DATA_2
	  AS
		SELECT
			"TK_ID"            AS "TAI_KHOAN_ID"
		  , NULL               AS "ID_CHUNG_TU"
		  , "DOI_TUONG_ID"
		  , OPN."SO_TAI_KHOAN" AS "MA_TAI_KHOAN"
		  , "TINH_CHAT"
		  , "currency_id"
		  , SUM(CASE WHEN "TINH_CHAT" = '2'
						  AND ("DU_NO_NGUYEN_TE" - "DU_CO_NGUYEN_TE") > 0
		  THEN ("DU_NO_NGUYEN_TE" - "DU_CO_NGUYEN_TE")
				WHEN "TINH_CHAT" = '2'
					 AND ("DU_NO_NGUYEN_TE" - "DU_CO_NGUYEN_TE") <= 0
				  THEN 0
				ELSE "DU_NO_NGUYEN_TE"
				END)              "DU_NO_NGUYEN_TE"
		  , SUM(CASE WHEN "TINH_CHAT" = '2'
						  AND ("DU_NO" - "DU_CO") > 0
		  THEN ("DU_NO" - "DU_CO")
				WHEN "TINH_CHAT" = '2'
					 AND ("DU_NO" - "DU_CO") <= 0
				  THEN 0
				ELSE "DU_NO"
				END)              "DU_NO"
		  , SUM(CASE WHEN "TINH_CHAT" = '2'
						  AND ("DU_CO_NGUYEN_TE" - "DU_NO_NGUYEN_TE") > 0
		  THEN ("DU_CO_NGUYEN_TE" - "DU_NO_NGUYEN_TE")
				WHEN "TINH_CHAT" = '2'
					 AND ("DU_CO_NGUYEN_TE" - "DU_NO_NGUYEN_TE") <= 0
				  THEN 0
				ELSE "DU_CO_NGUYEN_TE"
				END)              "DU_CO_NGUYEN_TE"
		  , SUM(CASE WHEN "TINH_CHAT" = '2'
						  AND ("DU_CO" - "DU_NO") > 0
		  THEN ("DU_CO" - "DU_NO")
				WHEN "TINH_CHAT" = '2'
					 AND ("DU_CO" - "DU_NO") <= 0
				  THEN 0
				ELSE "DU_CO"
				END)              "DU_CO"
		  , "CHI_NHANH_ID"
		FROM danh_muc_he_thong_tai_khoan A
		  INNER JOIN account_ex_so_du_tai_khoan_chi_tiet OPN ON OPN."TK_ID" = A.id
		WHERE (tham_so_goi_form_chi_tiet = 0
			   OR (OPN."LOAI_CHUNG_TU" = '610'
				   AND tham_so_goi_form_chi_tiet = 1
			   )
			  ) -- Số dư tài khoản
			  AND A."TINH_CHAT" <> msc_loai_tai_khoan
			  AND (OPN."currency_id" = tham_so_loai_tien_id
				   OR tham_so_loai_tien_id = msc_tong_hop_loai_tien
			  )
			  AND A."LA_TK_TONG_HOP" = FALSE
			  AND OPN."CHI_NHANH_ID" = tham_so_chi_nhanh_id
		GROUP BY "TK_ID",
		  OPN."DOI_TUONG_ID",
		  "currency_id",
		  OPN."SO_TAI_KHOAN",
		  "TINH_CHAT",
		  "CHI_NHANH_ID"
		ORDER BY OPN."SO_TAI_KHOAN";


	DROP TABLE IF EXISTS TMP_OPN_DATA;
	CREATE TEMP TABLE TMP_OPN_DATA
	  AS
		SELECT
		  "TAI_KHOAN_ID"
		  , NULL                 AS "ID_CHUNG_TU"
		  , "MA_TAI_KHOAN"
		  , "TINH_CHAT"
		  , tham_so_loai_tien_id AS "currency_id"
		  , SUM("DU_NO_NGUYEN_TE")  "DU_NO_NGUYEN_TE"
		  , SUM("DU_NO")            "DU_NO"
		  , SUM("DU_CO_NGUYEN_TE")  "DU_CO_NGUYEN_TE"
		  , SUM("DU_CO")            "DU_CO"
		  , "CHI_NHANH_ID"
		FROM TMP_OPN_DATA_2 A
		GROUP BY "TAI_KHOAN_ID",
		  "TINH_CHAT",
		  "MA_TAI_KHOAN",
		  "CHI_NHANH_ID"
		ORDER BY "MA_TAI_KHOAN";

	DROP TABLE IF EXISTS TMP_TAI_KHOAN;
	CREATE TEMP TABLE TMP_TAI_KHOAN
	(
	  "TAI_KHOAN_ID" INTEGER
	);
  END IF;

  IF tham_so_loai_tien_id <> msc_tong_hop_loai_tien
  THEN
	DROP TABLE IF EXISTS TMP_OPN_DATA;
	CREATE TEMP TABLE TMP_OPN_DATA
	  AS
		SELECT
			A.id                 AS    "TAI_KHOAN_ID"
		  , NULL                 AS    "ID_CHUNG_TU"
		  , OPN."SO_TAI_KHOAN"   AS    "MA_TAI_KHOAN"
		  , A."TINH_CHAT"
		  , tham_so_loai_tien_id AS    "currency_id"
		  , SUM(OPN."DU_NO_NGUYEN_TE") "DU_NO_NGUYEN_TE"
		  , SUM(OPN."DU_NO")           "DU_NO"
		  , SUM(OPN."DU_CO_NGUYEN_TE") "DU_CO_NGUYEN_TE"
		  , SUM(OPN."DU_CO")           "DU_CO"
		  , OPN."CHI_NHANH_ID"
		FROM danh_muc_he_thong_tai_khoan A
		  INNER JOIN account_ex_so_du_tai_khoan_chi_tiet OPN ON OPN."TK_ID" = A.id
		WHERE (tham_so_goi_form_chi_tiet = 0
			   OR (OPN."LOAI_CHUNG_TU" = '610'
				   AND tham_so_goi_form_chi_tiet = 1
			   )
			  )
			  AND A."TINH_CHAT" <> msc_loai_tai_khoan
			  AND (OPN."currency_id" = tham_so_loai_tien_id
				   OR tham_so_loai_tien_id = msc_tong_hop_loai_tien
			  )
			  AND A."LA_TK_TONG_HOP" = '0'    --
			  --             AND OPN.DisplayOnBook = @DisplayOnBook -- Biến truyên vào khi validate
			  AND OPN."CHI_NHANH_ID" = tham_so_chi_nhanh_id
		GROUP BY A.id,
		  A."TINH_CHAT",
		  OPN."SO_TAI_KHOAN",
		  OPN."CHI_NHANH_ID"
		ORDER BY A."SO_TAI_KHOAN";
  END IF;

  DROP TABLE IF EXISTS TMP_TAI_KHOAN;
  CREATE TEMP TABLE TMP_TAI_KHOAN
  (
	"TAI_KHOAN_ID" INTEGER
  );

  IF tham_so_co_hach_toan_ngoai_te = TRUE
  THEN
	INSERT INTO TMP_TAI_KHOAN (
	  SELECT A.id AS "TAI_KHOAN_ID"
	  FROM danh_muc_he_thong_tai_khoan A
		LEFT JOIN (SELECT "SO_TAI_KHOAN" AS "MA_TAI_KHOAN"
				   FROM danh_muc_he_thong_tai_khoan
				   WHERE "LA_TK_TONG_HOP" = '0'
						 AND "CO_HACH_TOAN_NGOAI_TE" = TRUE
				  ) OPN1 ON OPN1."MA_TAI_KHOAN" LIKE concat(A."SO_TAI_KHOAN", '%%')
	  WHERE A."TINH_CHAT" <> msc_loai_tai_khoan
			AND ((a."CO_HACH_TOAN_NGOAI_TE" = FALSE
	  ))
			AND A."LA_TK_TONG_HOP" = '1'
			AND (CASE WHEN OPN1."MA_TAI_KHOAN" IS NULL
						   AND A."LA_TK_TONG_HOP" = '1'
		THEN 1
				 ELSE 0
				 END) = 0
	  GROUP BY A."SO_TAI_KHOAN", A.id);
  END IF;

  DROP TABLE IF EXISTS TMP_OPN_TAI_KHOAN;
  CREATE TEMP TABLE TMP_OPN_TAI_KHOAN
	AS
	  SELECT
		  coalesce(OPN."ID_CHUNG_TU", '')                    AS "ID_CHUNG_TU"
		, CASE WHEN OPN."CHI_NHANH_ID" IS NULL
		THEN 1
		  ELSE 0
		  END                                                   IsAddedNew
		, A.id                                               AS "TAI_KHOAN_ID"
		, A."SO_TAI_KHOAN"                                   AS "MA_TAI_KHOAN"
		, A."TEN_TAI_KHOAN"                                             AS "TEN_TAI_KHOAN"
		, A."TEN_TIENG_ANH"
		, A.parent_id                                        AS "TK_TONG_HOP"
		, A."MA_PHAN_CAP"
		, A."BAC"
		, A."LA_TK_TONG_HOP"
		, A."TINH_CHAT"
		, CASE WHEN A."CHI_TIET_THEO_DOI_TUONG" = TRUE
		THEN 1
		  ELSE 0 END                                         AS "CHI_TIET_THEO_DOI_TUONG"
		, A."DOI_TUONG_SELECTION"                            AS "LOAI_DOI_TUONG"
		, CASE WHEN A."TAI_KHOAN_NGAN_HANG" = TRUE
		THEN 1
		  ELSE 0 END                                         AS "CHI_TIET_THEO_TK_NGAN_HANG"
		, A."CO_HACH_TOAN_NGOAI_TE"
		, coalesce(OPN."currency_id", tham_so_loai_tien_id) AS "LOAI_TIEN"
		, coalesce(OPN."DU_NO_NGUYEN_TE", 0)                 AS "DU_NO_NGUYEN_TE"
		, coalesce(OPN."DU_NO", 0)                           AS "DU_NO"
		, coalesce(OPN."DU_CO_NGUYEN_TE", 0)                 AS "DU_CO_NGUYEN_TE"
		, coalesce(OPN."DU_CO", 0)                           AS "DU_CO"
		, tham_so_chi_nhanh_id                               AS "CHI_NHANH_ID"
		, --           coalesce(OPN.DisplayOnBook, @DisplayOnBook) AS DisplayOnBook ,
		--           coalesce(OPN.IsPostedCashBook, 0) AS IsPostedCashBook ,
		  A."LA_TK_TONG_HOP"                                 AS "LA_TONG_HOP"
	  FROM danh_muc_he_thong_tai_khoan A
		LEFT JOIN TMP_OPN_DATA OPN ON OPN."TAI_KHOAN_ID" = A.id
		LEFT JOIN TMP_TAI_KHOAN T ON T."TAI_KHOAN_ID" = A.id
	  WHERE A."TINH_CHAT" <> msc_loai_tai_khoan
			AND ((a."CO_HACH_TOAN_NGOAI_TE" = tham_so_co_hach_toan_ngoai_te
				  AND tham_so_co_hach_toan_ngoai_te = TRUE
				 )
				 OR (tham_so_co_hach_toan_ngoai_te = FALSE)
				 OR (A."LA_TK_TONG_HOP" = TRUE
					 AND tham_so_co_hach_toan_ngoai_te = TRUE
					 /*hoant 20.06.2018 sửa lỗi 234151*/
					 AND T."TAI_KHOAN_ID" IS NOT NULL
				 )
			);


  SELECT MAX("BAC")
  INTO int_grade
  FROM TMP_OPN_TAI_KHOAN;

  IF tham_so_loai_tien_id = msc_tong_hop_loai_tien
  THEN

	WHILE (int_grade > 0)
	LOOP

	  UPDATE TMP_OPN_TAI_KHOAN B
	  SET "DU_NO"         = G."DU_NO_1",
		"DU_NO_NGUYEN_TE" = G."DU_NO_NGUYEN_TE_1",
		"DU_CO"           = G."DU_CO_1",
		"DU_CO_NGUYEN_TE" = G."DU_CO_NGUYEN_TE_1",
		"LA_TONG_HOP"     = CASE WHEN G."TK_TONG_HOP" ISNULL
		  THEN FALSE
							ELSE TRUE END
	  FROM (
			 SELECT
			   "TK_TONG_HOP"
			   , SUM("DU_NO")           AS "DU_NO_1"
			   , SUM("DU_NO_NGUYEN_TE") AS "DU_NO_NGUYEN_TE_1"
			   , SUM("DU_CO")           AS "DU_CO_1"
			   , SUM("DU_CO_NGUYEN_TE") AS "DU_CO_NGUYEN_TE_1"
			 FROM TMP_OPN_TAI_KHOAN
			 WHERE "BAC" = int_grade
			 GROUP BY "TK_TONG_HOP"

		   ) G
	  WHERE B."TAI_KHOAN_ID" = G."TK_TONG_HOP";
	  int_grade := int_grade - 1;

	END LOOP;

  ELSE

	WHILE (int_grade > 0)
	LOOP

	  UPDATE TMP_OPN_TAI_KHOAN B
	  SET "DU_NO"         = G."DU_NO_1",
		"DU_NO_NGUYEN_TE" = G."DU_NO_NGUYEN_TE_1",
		"DU_CO"           = G."DU_CO_1",
		"DU_CO_NGUYEN_TE" = G."DU_CO_NGUYEN_TE_1",
		"LA_TONG_HOP"     = FALSE
	  FROM (
			 SELECT
			   "TK_TONG_HOP"
			   , SUM("DU_NO")           AS "DU_NO_1"
			   , SUM("DU_NO_NGUYEN_TE") AS "DU_NO_NGUYEN_TE_1"
			   , SUM("DU_CO")           AS "DU_CO_1"
			   , SUM("DU_CO_NGUYEN_TE") AS "DU_CO_NGUYEN_TE_1"
			 FROM TMP_OPN_TAI_KHOAN
			 WHERE "BAC" = int_grade
			 GROUP BY "TK_TONG_HOP"

		   ) G
	  WHERE B."TAI_KHOAN_ID" = G."TK_TONG_HOP";
	  int_grade := int_grade - 1;

	END LOOP;

  END IF;


END $$;

SELECT *
FROM TMP_OPN_TAI_KHOAN
ORDER BY "MA_TAI_KHOAN"

		"""  
	
		record = self.execute(query, params)
		for account in record:
			new_line_so_du_tk += [(0, 0, {
				'SO_TAI_KHOAN_ID': [account.get('TAI_KHOAN_ID'),account.get('MA_TAI_KHOAN')],
				'SO_TAI_KHOAN': account.get('MA_TAI_KHOAN'),
				'TEN_TAI_KHOAN': account.get('TEN_TAI_KHOAN'),
				'DU_NO': account.get('DU_NO'),
				'DU_CO': account.get('DU_CO'),
				'DU_NO_NGUYEN_TE' : account.get('DU_NO_NGUYEN_TE'),
				'DU_CO_NGUYEN_TE' : account.get('DU_CO_NGUYEN_TE'),
				'child_id': account.get('TAI_KHOAN_ID'),
				'parent_id': account.get('TK_TONG_HOP'),
				'CHI_TIET_THEO_DOI_TUONG': account.get('CHI_TIET_THEO_DOI_TUONG'),
				'CHI_TIET_THEO_TK_NGAN_HANG': account.get('CHI_TIET_THEO_TK_NGAN_HANG'),
				'LOAI_DOI_TUONG': account.get('LOAI_DOI_TUONG'),
				'LA_TK_TONG_HOP' : account.get('LA_TK_TONG_HOP'),
				})]
		return new_line_so_du_tk

	def lay_cong_no_nhan_vien_ui(self,args):
		return {'ACCOUNT_EX_CONG_NO_NHAN_VIEN_IDS': self.lay_du_lieu_so_du_tai_khoan(args['id_loai_tien'],self.get_chi_nhanh(),2)}


	def lay_cong_no_khach_hang_ui(self,args):
		return {'ACCOUNT_EX_CONG_NO_KHACH_HANG_IDS': self.lay_du_lieu_so_du_tai_khoan(args['id_loai_tien'],self.get_chi_nhanh(),1)}

	def lay_du_lieu_so_du_tai_khoan(self,loai_tien_id,chi_nhanh,loai_chi_tiet):
		new_line_chi_tiet = [[5]]
		record =[]
		ref_type = 0
		loai_doi_tuong = ''
		chi_tiet_theo_doi_tuong = 0
		chi_tiet_theo_tk_ngan_hang = 0
		# chi tiết theo nhà cung cấp
		if loai_chi_tiet == 0:
			ref_type = '613'
			chi_tiet_theo_doi_tuong = 1
			loai_doi_tuong = '0'
		# chi tiết theo khách hàng
		elif loai_chi_tiet == 1:
			ref_type = '612'
			chi_tiet_theo_doi_tuong = 1
			loai_doi_tuong = '1'
		# chi tiết theo nhân viên
		elif loai_chi_tiet == 2:
			ref_type = '614'
			chi_tiet_theo_doi_tuong = 1
			loai_doi_tuong = '2'
		# chi tiết theo tài khoản ngân hàng
		elif loai_chi_tiet == 3:
			ref_type = '620'
			loai_chi_tiet = '2'
			chi_tiet_theo_doi_tuong = 0
			chi_tiet_theo_tk_ngan_hang = 1

		params = {
			'currency_id': loai_tien_id,
			'CHI_NHANH_ID' : chi_nhanh,
			'REF_TYPE' : ref_type,
			}

		query = """   

		DO LANGUAGE plpgsql $$ DECLARE

			tham_so_loai_tien INTEGER := %(currency_id)s ;
			tham_so_chi_nhanh INTEGER := %(CHI_NHANH_ID)s ;
			tham_so_reftype   VARCHAR(50) := %(REF_TYPE)s;


			BEGIN
			IF tham_so_loai_tien = -1
			THEN
			DROP TABLE IF EXISTS TMP_KET_QUA;
			CREATE TEMP TABLE TMP_KET_QUA
			AS
			SELECT
			ROW_NUMBER()
			OVER (
				ORDER BY "SO_TAI_KHOAN", "MA" ) AS RowNum
			, *
			FROM

			(
				SELECT
					row_number()
					OVER (
					PARTITION BY TRUE :: BOOLEAN ) AS "ID_CHUNG_TU"
				, OPN."LOAI_CHUNG_TU"
				, now()                            AS "NGAY_HACH_TOAN"
				, OPN."TK_ID"                      AS "TAI_KHOAN_ID"
				, AC."SO_TAI_KHOAN"
				, OPN."DOI_TUONG_ID"
				, -- 					OPN."currency_id" AS "currency_id" ,
				-- 					OPN."TY_GIA" AS "TY_GIA" ,
					SUM("DU_NO_NGUYEN_TE")           AS "DU_NO_NGUYEN_TE"
				, SUM("DU_NO")                     AS "DU_NO"
				, SUM("DU_CO_NGUYEN_TE")           AS "DU_CO_NGUYEN_TE"
				, SUM("DU_CO")                     AS "DU_CO"
				, OPN."TK_NGAN_HANG_ID"
				, BA."SO_TAI_KHOAN"                AS "SO_TAI_KHOAN_NGAN_HANG"
				, OPN."CHI_NHANH_ID"
				, AC."TEN_TAI_KHOAN"                          AS "TEN_TAI_KHOAN"
				, AO."MA"
				, AO."HO_VA_TEN"                          AS "TEN_DOI_TUONG"
				, NH."TEN_DAY_DU"                  AS "TEN_NGAN_HANG"
				FROM account_ex_so_du_tai_khoan_chi_tiet OPN
				INNER JOIN danh_muc_he_thong_tai_khoan AC ON OPN."TK_ID" = AC.id
				LEFT JOIN res_partner AO ON OPN."DOI_TUONG_ID" = AO.id
				LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON OPN."TK_NGAN_HANG_ID" = BA.id
				LEFT JOIN danh_muc_ngan_hang NH ON NH.id = BA."NGAN_HANG_ID"
				GROUP BY OPN."LOAI_CHUNG_TU",
				OPN."CHI_NHANH_ID",
				OPN."TK_ID",
				OPN."DOI_TUONG_ID",
				OPN."TK_NGAN_HANG_ID",
				-- 					OPN."currency_id",
				-- 					OPN."TY_GIA",
				AC."SO_TAI_KHOAN",
				AC."TEN_TAI_KHOAN",
				AO."MA",
				AO."HO_VA_TEN",
				BA."SO_TAI_KHOAN",
				NH."TEN_DAY_DU"
			) view_sum

			WHERE "LOAI_CHUNG_TU" = tham_so_reftype AND "CHI_NHANH_ID" = tham_so_chi_nhanh;
			ELSE
			DROP TABLE IF EXISTS TMP_KET_QUA;
			CREATE TEMP TABLE TMP_KET_QUA
			AS
			SELECT
			ROW_NUMBER()
			OVER (
				ORDER BY "SO_TAI_KHOAN", "MA" ) AS RowNum
			, *
			FROM

			(
				SELECT
					row_number()
					OVER (
					PARTITION BY TRUE :: BOOLEAN ) AS "ID_CHUNG_TU"
				, OPN."LOAI_CHUNG_TU"
				, now()                            AS "NGAY_HACH_TOAN"
				, OPN."TK_ID"                      AS "TAI_KHOAN_ID"
				, AC."SO_TAI_KHOAN"
				, OPN."DOI_TUONG_ID"
				,OPN."currency_id" AS "currency_id"
				,OPN."TY_GIA" AS "TY_GIA"
				,SUM("DU_NO_NGUYEN_TE")           AS "DU_NO_NGUYEN_TE"
				, SUM("DU_NO")                     AS "DU_NO"
				, SUM("DU_CO_NGUYEN_TE")           AS "DU_CO_NGUYEN_TE"
				, SUM("DU_CO")                     AS "DU_CO"
				, OPN."TK_NGAN_HANG_ID"
				, BA."SO_TAI_KHOAN"                AS "SO_TAI_KHOAN_NGAN_HANG"
				, OPN."CHI_NHANH_ID"
				, AC."TEN_TAI_KHOAN"                          AS "TEN_TAI_KHOAN"
				, AO."MA"
				, AO."HO_VA_TEN"                          AS "TEN_DOI_TUONG"
				, NH."TEN_DAY_DU"                  AS "TEN_NGAN_HANG"
				FROM account_ex_so_du_tai_khoan_chi_tiet OPN
				INNER JOIN danh_muc_he_thong_tai_khoan AC ON OPN."TK_ID" = AC.id
				LEFT JOIN res_partner AO ON OPN."DOI_TUONG_ID" = AO.id
				LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON OPN."TK_NGAN_HANG_ID" = BA.id
				LEFT JOIN danh_muc_ngan_hang NH ON NH.id = BA."NGAN_HANG_ID"
				GROUP BY OPN."LOAI_CHUNG_TU",
				OPN."CHI_NHANH_ID",
				OPN."TK_ID",
				OPN."DOI_TUONG_ID",
				OPN."TK_NGAN_HANG_ID",
				OPN."currency_id",
				OPN."TY_GIA",
				AC."SO_TAI_KHOAN",
				AC."TEN_TAI_KHOAN",
				AO."MA",
				AO."HO_VA_TEN",
				BA."SO_TAI_KHOAN",
				NH."TEN_DAY_DU"
			) view_sum

			WHERE "LOAI_CHUNG_TU" = tham_so_reftype AND "CHI_NHANH_ID" = tham_so_chi_nhanh AND "currency_id" = tham_so_loai_tien;
			END IF;

			END $$;

			SELECT *FROM TMP_KET_QUA;

		"""  
		record= self.execute(query, params)
		for chi_tiet in record:
			if chi_tiet.get('DU_NO_NGUYEN_TE') > 0 or chi_tiet.get('DU_CO_NGUYEN_TE') > 0:
				new_line_chi_tiet += [(0, 0, {
					'SO_TAI_KHOAN_ID': [chi_tiet.get('TAI_KHOAN_ID'),chi_tiet.get('SO_TAI_KHOAN')],
					'DOI_TUONG_ID': [chi_tiet.get('DOI_TUONG_ID'),chi_tiet.get('MA')],
					'SO_TK_NGAN_HANG_ID': [chi_tiet.get('TK_NGAN_HANG_ID'),chi_tiet.get('SO_TAI_KHOAN_NGAN_HANG')],
					'TEN_NGAN_HANG': chi_tiet.get('TEN_NGAN_HANG'),
					'TEN_KHACH_HANG': chi_tiet.get('TEN_DOI_TUONG'),
					'TEN_NHA_CUNG_CAP': chi_tiet.get('TEN_DOI_TUONG'),
					'TEN_NHAN_VIEN': chi_tiet.get('TEN_DOI_TUONG'),
					'DU_NO': chi_tiet.get('DU_NO'),
					'DU_CO': chi_tiet.get('DU_CO'),
					'DU_NO_NGUYEN_TE': chi_tiet.get('DU_NO_NGUYEN_TE'),
					'DU_CO_NGUYEN_TE': chi_tiet.get('DU_CO_NGUYEN_TE'),
					'CHI_TIET_THEO_DOI_TUONG': chi_tiet_theo_doi_tuong,
					'LOAI_DOI_TUONG': loai_doi_tuong,
					'CHI_TIET_THEO_TK_NGAN_HANG' : chi_tiet_theo_tk_ngan_hang
					})]
		return new_line_chi_tiet
	
	def lay_cong_no_nha_cung_cap_ui(self,args):
		return {'ACCOUNT_EX_CONG_NO_NHA_CUNG_CAP_IDS': self.lay_du_lieu_so_du_tai_khoan(args['id_loai_tien'],self.get_chi_nhanh(),0)}

	
	
	def lay_so_du_tai_khoan_ngan_hang_ui(self,args):
		return {'ACCOUNT_EX_SO_DU_TK_NGAN_HANG_IDS': self.lay_du_lieu_so_du_tai_khoan(args['id_loai_tien'],self.get_chi_nhanh(),3)}



	def lay_du_lieu_vthh(self,kho_id,chi_nhanh):
		record = []
		phuong_phap_tinh_gia = self.env['ir.config_parameter'].get_param('he_thong.PHUONG_PHAP_TINH_GIA_XUAT_KHO')
		tham_so_phuong_thuc_tinh_gia = 0
		if phuong_phap_tinh_gia == 'GIA_DICH_DANH':
			tham_so_phuong_thuc_tinh_gia = 1
		elif phuong_phap_tinh_gia == 'BINH_QUAN_TUC_THOI':
			tham_so_phuong_thuc_tinh_gia = 2
		elif phuong_phap_tinh_gia == 'NHAP_TRUOC_XUAT_TRUOC':
			tham_so_phuong_thuc_tinh_gia = 3
		params = {
			'KHO_ID': kho_id,
			'CHI_NHANH_ID': chi_nhanh,
			'PHUONG_THUC_TINH_GIA' : tham_so_phuong_thuc_tinh_gia
			}
		query = """   

			DO LANGUAGE plpgsql $$ DECLARE

			tham_so_kho_id  INTEGER := %(KHO_ID)s;
			tham_so_chi_nhanh INTEGER := %(CHI_NHANH_ID)s ;
			tham_so_la_chi_tiet INTEGER := 0 ;
			tham_so_phuong_thuc_tinh_gia INTEGER := %(PHUONG_THUC_TINH_GIA)s ;



			BEGIN

			IF tham_so_phuong_thuc_tinh_gia = 0 OR tham_so_phuong_thuc_tinh_gia = 1
			THEN
			DROP TABLE IF EXISTS TMP_KET_QUA;
			CREATE TEMP TABLE TMP_KET_QUA
			AS
			SELECT
					O.id AS "ID_CHUNG_TU" ,
					O."LOAI_CHUNG_TU" ,
					O."NGAY_HACH_TOAN" ,
					O."SO_CHUNG_TU" ,
					o. state AS "TRANG_THAI_GHI_SO" ,
					O."MA_HANG_ID" ,
					I."MA" AS "MA_HANG" ,
					I."TEN" AS "TEN_HANG" ,
					O."KHO_ID" ,
					O."DVT_ID" ,
					U."DON_VI_TINH" AS "TEN_DVT",
					coalesce(O."SO_LUONG",0) AS "SO_LUONG",
					O."DON_GIA" ,
					O."GIA_TRI_TON" ,
					O."HAN_SU_DUNG" ,
					O."SO_LO" ,
					O."DVT_CHINH_ID" ,
					O."DON_GIA_THEO_DVT_CHINH" ,
					O."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH" ,
					O."SO_LUONG_THEO_DVT_CHINH" ,
					O."TOAN_TU_QUY_DOI" ,
					O."CHI_NHANH_ID" ,
					O."STT" ,
					O."THU_TU_CHUNG_TU" ,
			--         O.InventoryResaleTypeID,
					S."MA_KHO",
			--         I.InventoryItemCategoryName,
					I."LIST_NHOM_VTHH"
			FROM    account_ex_ton_kho_vat_tu_hang_hoa O
					INNER JOIN danh_muc_vat_tu_hang_hoa I ON O."MA_HANG_ID" = I.id
					LEFT JOIN danh_muc_to_chuc AS OU ON O."CHI_NHANH_ID" = OU.id
					LEFT JOIN danh_muc_don_vi_tinh AS U ON O."DVT_ID" = U.id
					LEFT JOIN danh_muc_kho AS S ON O."KHO_ID" = S.id
			WHERE(O."KHO_ID" = tham_so_kho_id OR tham_so_kho_id = -1)
					AND ( ( tham_so_chi_nhanh IS NULL
							AND "HACH_TOAN_SELECTION" = 'PHU_THUOC'
						)
						OR ( tham_so_chi_nhanh IS NOT NULL
							AND O."CHI_NHANH_ID" = tham_so_chi_nhanh
							)
						)
			ORDER BY
			CASE tham_so_la_chi_tiet WHEN 0 THEN I.id	ELSE NULL END ,
					CASE tham_so_la_chi_tiet WHEN 0 THEN U.id			ELSE NULL END,
					O."THU_TU_CHUNG_TU", -- KDCHIEN 27.07.2018:243107: Bỏ sort trên giao diện thì phải Sort dưới store
					O."STT"; --bndinh 23/12/2015: sửa lỗi 83466, sắp xếp trên danh sách số dư theo RefOrder trước
			ELSE

					DROP TABLE IF EXISTS TMP_KET_QUA;
			CREATE TEMP TABLE TMP_KET_QUA
			AS
			SELECT
			O.id AS "ID_CHUNG_TU" ,
			O."LOAI_CHUNG_TU" ,
					O."NGAY_HACH_TOAN" ,
					O."SO_CHUNG_TU" ,
					o.state AS "TRANG_THAI_GHI_SO" ,
					O."MA_HANG_ID" ,
					I."MA" AS "MA_HANG" ,
					I."TEN" AS "TEN_HANG" ,
					O."KHO_ID" ,
					O."DVT_ID" ,
					U."DON_VI_TINH" AS "TEN_DVT",
					coalesce(O."SO_LUONG",0) AS "SO_LUONG",
					O."DON_GIA" ,
					O."GIA_TRI_TON" ,
					O."HAN_SU_DUNG" ,
					O."SO_LO" ,
					O."DVT_CHINH_ID" ,
					O."DON_GIA_THEO_DVT_CHINH" ,
					O."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH" ,
					O."SO_LUONG_THEO_DVT_CHINH" ,
					O."TOAN_TU_QUY_DOI" ,
					O."CHI_NHANH_ID" ,
					O."STT" ,
					O."THU_TU_CHUNG_TU" ,
			--         O.InventoryResaleTypeID,
					S."MA_KHO",
			--         I.InventoryItemCategoryName,
					I."LIST_NHOM_VTHH"
			FROM    account_ex_ton_kho_vat_tu_hang_hoa O
					INNER JOIN danh_muc_vat_tu_hang_hoa I ON O."MA_HANG_ID" = I.id
					LEFT JOIN danh_muc_to_chuc AS OU ON o."CHI_NHANH_ID" = OU.id
					LEFT JOIN danh_muc_don_vi_tinh AS U ON O."DVT_ID" = U.id
					LEFT JOIN danh_muc_kho AS S ON O."KHO_ID" = S.id
			WHERE   (O."KHO_ID" = tham_so_kho_id OR tham_so_kho_id = -1)
					AND ( ( tham_so_chi_nhanh IS NULL
							AND "HACH_TOAN_SELECTION" = 'PHU_THUOC'
						)
						OR ( tham_so_chi_nhanh IS NOT NULL
							AND O."CHI_NHANH_ID" = tham_so_chi_nhanh
							)
						)
			ORDER BY
			CASE tham_so_la_chi_tiet WHEN 0 THEN "NGAY_HACH_TOAN"			ELSE NULL END ,
					CASE tham_so_la_chi_tiet WHEN 0 THEN "SO_CHUNG_TU"			ELSE NULL END , --kdchien 26/12/2015:83699:Sắp xếp theo số chứng từ nữa
					CASE tham_so_la_chi_tiet WHEN 0 THEN I."MA"	ELSE NULL END ,
					CASE tham_so_la_chi_tiet WHEN 0 THEN U."DON_VI_TINH"			ELSE NULL END ,
					"THU_TU_CHUNG_TU",-- KDCHIEN 27.07.2018:243107: Bỏ sort trên giao diện thì phải Sort dưới store
					"STT"; --bndinh 23/12/2015: sửa lỗi 83466, sắp xếp trên danh sách số dư theo RefOrder trước
			END IF;

			END $$;

			SELECT *FROM TMP_KET_QUA ORDER BY "MA_HANG"


		"""  
		record = self.execute(query, params)
		
		return record

	


	def lay_du_lieu_chi_phi_do_dang(self,loai_cpdd,chi_nhanh):
		record = []
		params = {
			'LOAI_CPDD': loai_cpdd,
			'CHI_NHANH_ID': chi_nhanh,
			}
		query = """   

		DO LANGUAGE plpgsql $$ DECLARE

		tham_so_loai_cpdd  INTEGER := %(LOAI_CPDD)s;
		tham_so_gop_theo_chi_nhanh INTEGER := 0 ;
		tham_so_chi_nhanh INTEGER := %(CHI_NHANH_ID)s ;
		ts_154 INTEGER := 0 ;
		ten_tk VARCHAR(50):='';
		ma_phan_cap                VARCHAR(200) := '';


		BEGIN

		SELECT id,"SO_TAI_KHOAN" INTO ts_154,ten_tk
		FROM danh_muc_he_thong_tai_khoan a
		WHERE "SO_TAI_KHOAN" LIKE '154%%'
		ORDER BY a."MA_PHAN_CAP"
		FETCH FIRST 1 ROW ONLY;

		IF tham_so_loai_cpdd = 1
		THEN
		DROP TABLE IF EXISTS TMP_KET_QUA;
		CREATE TEMP TABLE TMP_KET_QUA
		AS
		SELECT
			CASE WHEN J.isparent = TRUE THEN row_number() OVER (PARTITION BY true::boolean)
					ELSE coalesce(OPN.id, row_number() OVER (PARTITION BY true::boolean))
			END AS "ID_CHUNG_TU" , -- OPNID - uniqueidentifier
			tham_so_chi_nhanh AS "CHI_NHANH_ID" , -- BranchID - uniqueidentifier
			J.id AS "DTTHCP_ID" , -- JobID - uniqueidentifier
			J."MA_DOI_TUONG_THCP" , -- JobCode - nvarchar(20)
			J."TEN_DOI_TUONG_THCP" , -- JobName - nvarchar(255)
			J."LOAI" AS "LOAI_DTTHCP" , -- JobType - int
			J.parent_id ,
			J."BAC" ,
			J.isparent ,
			J."MA_PHAN_CAP" ,
			CASE WHEN J.isparent = TRUE THEN NULL
					ELSE coalesce(OPN."TAI_KHOAN_CPSXKD_DO_DANG_ID", ts_154)
			END AS "TAI_KHOAN_CPSXKD_DO_DANG_ID" ,  --Ngầm định là 154 với con, cha để trống
			CASE WHEN J.isparent = TRUE THEN NULL
					ELSE coalesce(A."SO_TAI_KHOAN", ten_tk)
			END AS "MA_TAI_KHOAN_CPDD" ,
			coalesce(OPN."TONG", 0) AS "TONG" ,
			coalesce(OPN."CHI_PHI_NVL_TRUC_TIEP", 0) AS "CHI_PHI_NVL_TRUC_TIEP" , -- DirectMatetialAmount - decimal
			coalesce(OPN."CHI_PHI_NVL_GIAN_TIEP", 0) AS "CHI_PHI_NVL_GIAN_TIEP" , -- IndirectMatetialAmount - decimal
			coalesce(OPN."CHI_PHI_NHAN_CONG_TRUC_TIEP", 0) AS "CHI_PHI_NHAN_CONG_TRUC_TIEP" , -- DirectLaborAmount - decimal
			coalesce(OPN."CHI_PHI_NHAN_CONG_GIAN_TIEP", 0) AS "CHI_PHI_NHAN_CONG_GIAN_TIEP" , -- IndirectLaborAmount - decimal
			coalesce(OPN."CHI_PHI_KHAU_HAO", 0) AS "CHI_PHI_KHAU_HAO" , -- DepreciationAmount - decimal
			coalesce(OPN."CHI_PHI_MUA_NGOAI", 0) AS "CHI_PHI_MUA_NGOAI" , -- PurchaseAmount - decimal
			coalesce(OPN."CHI_PHI_KHAC_CHUNG", 0) AS "CHI_PHI_KHAC_CHUNG" , -- OtherAmount - decimal
			coalesce(OPN."MTC_CHI_PHI_NVL_GIAN_TIEP", 0) AS "MTC_CHI_PHI_NVL_GIAN_TIEP" ,
			coalesce(OPN."MTC_CHI_PHI_NHAN_CONG", 0) AS "MTC_CHI_PHI_NHAN_CONG" ,
			coalesce(OPN."MTC_CHI_PHI_KHAU_HAO_DAU_KY", 0) AS "MTC_CHI_PHI_KHAU_HAO_DAU_KY" ,
			coalesce(OPN."MTC_CHI_PHI_MUA_NGOAI_DAU_KY", 0) AS "MTC_CHI_PHI_MUA_NGOAI_DAU_KY" ,
			coalesce(OPN."MTC_CHI_PHI_KHAC_CHUNG", 0) AS "MTC_CHI_PHI_KHAC_CHUNG" ,
			coalesce(OPN."SO_DA_NGHIEM_THU", 0) AS "SO_DA_NGHIEM_THU" , -- AcceptedAmount - decimal
			coalesce(OPN."SO_CHUA_NGHIEM_THU", 0) AS "SO_CHUA_NGHIEM_THU" , -- NotAcceptedAmount - decimal
			coalesce(OPN."TONG_CHI_PHI", 0) AS "TONG_CHI_PHI" ,  -- TotalAmount - decimal
			coalesce(OPN."STT", 0) AS "STT" ,
			CASE WHEN OPN.id IS NULL THEN 0
					ELSE 1
			END AS "DA_THEM"
		FROM    danh_muc_doi_tuong_tap_hop_chi_phi AS J
			LEFT JOIN ( SELECT  J.* ,
								J2."MA_PHAN_CAP" AS "MPC"
						FROM    account_ex_chi_phi_do_dang AS J
								INNER JOIN danh_muc_doi_tuong_tap_hop_chi_phi AS J2 ON J."MA_DOI_TUONG_THCP_ID" = J2.id
											AND J."CHI_NHANH_ID" = tham_so_chi_nhanh
						) AS OPN ON j."MA_PHAN_CAP"  LIKE concat(OPN."MPC",'%%')
			LEFT JOIN danh_muc_he_thong_tai_khoan A ON OPN."TAI_KHOAN_CPSXKD_DO_DANG_ID" = A.id
		WHERE   ( tham_so_gop_theo_chi_nhanh = 1
				AND ( J."CHI_NHANH_ID" = tham_so_chi_nhanh )
				OR OPN.id IS NOT NULL
			)
			OR tham_so_gop_theo_chi_nhanh = 0
		ORDER BY J."THU_TU_THEO_MA_PHAN_CAP",Opn."THU_TU_THEO_MA_PHAN_CAP";

		END IF;

		IF tham_so_loai_cpdd = 2
		THEN
		DROP TABLE IF EXISTS TMP_KET_QUA;
		CREATE TEMP TABLE TMP_KET_QUA
		AS
		SELECT
			CASE WHEN P.isparent = TRUE THEN row_number() OVER (PARTITION BY true::boolean)
					ELSE coalesce(OPN.id, row_number() OVER (PARTITION BY true::boolean))
			END AS "ID_CHUNG_TU" , -- OPNID - uniqueidentifier
			tham_so_chi_nhanh AS "CHI_NHANH_ID" , -- "CHI_NHANH_ID" - uniqueidentifier
			P.id AS "CONG_TRINH_ID" , -- uniqueidentifier
			P."MA_CONG_TRINH" , -- nvarchar(20)
			P."TEN_CONG_TRINH" , -- nvarchar(255)
			P."LOAI_CONG_TRINH" AS "LOAI" , -- int
			LCT.name AS "TEN_LOAI_CONG_TRINH" ,
			P.parent_id ,
			P."BAC" ,
			P.isparent ,
			P."MA_PHAN_CAP" ,
			CASE WHEN P.isparent = TRUE THEN NULL
					ELSE coalesce(OPN."TAI_KHOAN_CPSXKD_DO_DANG_ID", ts_154)
			END AS "TAI_KHOAN_CPSXKD_DO_DANG_ID" ,  --Ngầm định là 154 với con, cha để trống
			CASE WHEN P.isparent = TRUE THEN NULL
					ELSE coalesce(A."SO_TAI_KHOAN", ten_tk)
			END AS "MA_TAI_KHOAN_CPDD" ,
			coalesce(OPN."CHI_PHI_NVL_TRUC_TIEP", 0) AS "CHI_PHI_NVL_TRUC_TIEP" ,
			coalesce(OPN."CHI_PHI_NHAN_CONG_TRUC_TIEP", 0) AS "CHI_PHI_NHAN_CONG_TRUC_TIEP" ,
			coalesce(OPN."CHI_PHI_NVL_GIAN_TIEP", 0) AS "CHI_PHI_NVL_GIAN_TIEP" ,
			coalesce(OPN."CHI_PHI_MUA_NGOAI", 0) AS "CHI_PHI_MUA_NGOAI" ,

			coalesce(OPN."MTC_CHI_PHI_NVL_GIAN_TIEP", 0) AS "MTC_CHI_PHI_NVL_GIAN_TIEP" ,
			coalesce(OPN."MTC_CHI_PHI_NHAN_CONG", 0) AS "MTC_CHI_PHI_NHAN_CONG" ,
			coalesce(OPN."MTC_CHI_PHI_KHAU_HAO_DAU_KY", 0) AS "MTC_CHI_PHI_KHAU_HAO_DAU_KY" ,
			coalesce(OPN."MTC_CHI_PHI_MUA_NGOAI_DAU_KY", 0) AS "MTC_CHI_PHI_MUA_NGOAI_DAU_KY" ,
			coalesce(OPN."MTC_CHI_PHI_KHAC_CHUNG", 0) AS "MTC_CHI_PHI_KHAC_CHUNG" ,
			coalesce(OPN."MTC_TONG", 0) AS "MTC_TONG" ,
			coalesce(OPN."TONG", 0) AS "TONG" ,
			coalesce(OPN."CHI_PHI_NHAN_CONG_GIAN_TIEP", 0) AS "CHI_PHI_NHAN_CONG_GIAN_TIEP" ,
			coalesce(OPN."CHI_PHI_KHAU_HAO", 0) AS "CHI_PHI_KHAU_HAO" ,
--			coalesce(OPN."MTC_CHI_PHI_MUA_NGOAI_DAU_KY", 0) AS "MTC_CHI_PHI_MUA_NGOAI_DAU_KY" ,
			coalesce(OPN."CHI_PHI_KHAC_CHUNG", 0) AS "CHI_PHI_KHAC_CHUNG" ,
--			coalesce(OPN."TONG_CHI_PHI", 0) AS "TONG_CHI_PHI" ,
-- 			coalesce(OPN."TONG_CHI_PHI", 0) AS "TONG_CHI_PHI" ,

-- 			coalesce(OPN."CHI_PHI_NVL_TRUC_TIEP", 0) AS "CHI_PHI_NVL_TRUC_TIEP_DAU_KY" , -- DirectMatetialAmount - decimal
-- 			coalesce(OPN."CHI_PHI_NVL_GIAN_TIEP", 0) AS "CHI_PHI_NVL_GIAN_TIEP_DAU_KY" , -- IndirectMatetialAmount - decimal
-- 			coalesce(OPN."CHI_PHI_NHAN_CONG_TRUC_TIEP", 0) AS "CHI_PHI_NHAN_CONG_TRUC_TIEP" , -- DirectLaborAmount - decimal
-- 			coalesce(OPN."CHI_PHI_NHAN_CONG_GIAN_TIEP", 0) AS "CHI_PHI_NHAN_CONG_GIAN_TIEP_DAU_KY" , -- IndirectLaborAmount - decimal
-- 			coalesce(OPN."CHI_PHI_KHAU_HAO_DAU_KY", 0) AS "CHI_PHI_KHAU_HAO_DAU_KY" , -- DepreciationAmount - decimal
-- 			coalesce(OPN."CHI_PHI_MUA_NGOAI", 0) AS "CHI_PHI_MUA_NGOAI" , -- PurchaseAmount - decimal
-- 			coalesce(OPN."CHI_PHI_KHAC_CHUNG", 0) AS "CHI_PHI_KHAC_CHUNG" , -- OtherAmount - decimal
-- 			coalesce(OPN."MTC_CHI_PHI_NVL_GIAN_TIEP", 0) AS "MTC_CHI_PHI_NVL_GIAN_TIEP" ,
-- 			coalesce(OPN."MTC_CHI_PHI_NHAN_CONG", 0) AS "MTC_CHI_PHI_NHAN_CONG" ,
-- 			coalesce(OPN."MTC_CHI_PHI_KHAU_HAO_DAU_KY", 0) AS "MTC_CHI_PHI_KHAU_HAO_DAU_KY" ,
-- 			coalesce(OPN."MTC_CHI_PHI_MUA_NGOAI_DAU_KY", 0) AS "MTC_CHI_PHI_MUA_NGOAI_DAU_KY" ,
-- 			coalesce(OPN."MTC_CHI_PHI_KHAC_CHUNG", 0) AS "MTC_CHI_PHI_KHAC_CHUNG" ,
			coalesce(OPN."SO_DA_NGHIEM_THU", 0) AS "SO_DA_NGHIEM_THU" , -- AcceptedAmount - decimal
			coalesce(OPN."SO_CHUA_NGHIEM_THU", 0) AS "SO_CHUA_NGHIEM_THU" , -- NotAcceptedAmount - decimal
			coalesce(OPN."TONG_CHI_PHI", 0) AS "TONG_CHI_PHI" ,  -- TotalAmount - decimal
			coalesce(OPN."STT", 0) AS "STT" ,
			CASE WHEN OPN.id IS NULL THEN 0
					ELSE 1
			END AS "DA_THEM"
		FROM    danh_muc_cong_trinh AS P
			LEFT JOIN ( SELECT  J.* ,
								J2."MA_PHAN_CAP" AS "MPC"
						FROM    account_ex_chi_phi_do_dang AS J
								INNER JOIN danh_muc_cong_trinh
								AS J2 ON J."MA_CONG_TRINH_ID" = J2.id
											AND J."CHI_NHANH_ID" = tham_so_chi_nhanh
						) AS OPN ON OPN."MPC" = P."MA_PHAN_CAP"
			LEFT JOIN danh_muc_he_thong_tai_khoan A ON OPN."TAI_KHOAN_CPSXKD_DO_DANG_ID" = A.id
			LEFT JOIN danh_muc_loai_cong_trinh LCT ON P."LOAI_CONG_TRINH" = LCT.id
		WHERE   ( tham_so_gop_theo_chi_nhanh = 1
				AND ( P."CHI_NHANH_ID" = tham_so_chi_nhanh )
				OR OPN.id IS NOT NULL
			)
			OR tham_so_gop_theo_chi_nhanh = 0
		--WHERE P.active = 0
		ORDER BY P."THU_TU_THEO_MA_PHAN_CAP",OPN."THU_TU_THEO_MA_PHAN_CAP";
		END IF;

		IF tham_so_loai_cpdd = 3
		THEN
		DROP TABLE IF EXISTS TMP_KET_QUA;
		CREATE TEMP TABLE TMP_KET_QUA
		AS
		SELECT
			coalesce(OPN.id, row_number() OVER (PARTITION BY true::boolean)) AS "ID_CHUNG_TU" , -- OPNID - uniqueidentifier
			tham_so_chi_nhanh AS "CHI_NHANH_ID" , -- BranchID - uniqueidentifier
			S.id AS "DON_HANG_ID" ,  -- uniqueidentifier
			S."SO_DON_HANG" , -- nvarchar(25)
			S."NGAY_DON_HANG" AS "NGAY_DON_HANG" , -- datetime
			S."DIEN_GIAI" , -- nvarchar(255)
			S."KHACH_HANG_ID" AS "DOI_TUONG_ID" , -- nvarchar(255)
			A."HO_VA_TEN" AS "TEN_DOI_TUONG",
			ts_154 AS "TAI_KHOAN_CPSXKD_DO_DANG_ID",
			ten_tk AS "MA_TAI_KHOAN_CPDD",
			coalesce(OPN."CHI_PHI_NVL_TRUC_TIEP", 0) AS "CHI_PHI_NVL_TRUC_TIEP" , -- DirectMatetialAmount - decimal
			coalesce(OPN."CHI_PHI_NVL_GIAN_TIEP", 0) AS "CHI_PHI_NVL_GIAN_TIEP" , -- IndirectMatetialAmount - decimal
			coalesce(OPN."CHI_PHI_NHAN_CONG_TRUC_TIEP", 0) AS "CHI_PHI_NHAN_CONG_TRUC_TIEP" , -- DirectLaborAmount - decimal
			coalesce(OPN."CHI_PHI_NHAN_CONG_GIAN_TIEP", 0) AS "CHI_PHI_NHAN_CONG_GIAN_TIEP" , -- IndirectLaborAmount - decimal
			coalesce(OPN."CHI_PHI_KHAU_HAO", 0) AS "CHI_PHI_KHAU_HAO" , -- DepreciationAmount - decimal
			coalesce(OPN."CHI_PHI_MUA_NGOAI", 0) AS "CHI_PHI_MUA_NGOAI" , -- PurchaseAmount - decimal
			coalesce(OPN."CHI_PHI_KHAC_CHUNG", 0) AS "CHI_PHI_KHAC_CHUNG" , -- OtherAmount - decimal
			coalesce(OPN."TONG", 0) AS "TONG" ,
			coalesce(OPN."MTC_CHI_PHI_NHAN_CONG", 0) AS "MTC_CHI_PHI_NHAN_CONG" ,
			coalesce(OPN."MTC_CHI_PHI_KHAU_HAO_DAU_KY", 0) AS "MTC_CHI_PHI_KHAU_HAO_DAU_KY" ,
			coalesce(OPN."MTC_CHI_PHI_MUA_NGOAI_DAU_KY", 0) AS "MTC_CHI_PHI_MUA_NGOAI_DAU_KY" ,
			coalesce(OPN."MTC_CHI_PHI_KHAC_CHUNG", 0) AS "MTC_CHI_PHI_KHAC_CHUNG" ,
			coalesce(OPN."SO_DA_NGHIEM_THU", 0) AS "SO_DA_NGHIEM_THU" , -- AcceptedAmount - decimal
			coalesce(OPN."SO_CHUA_NGHIEM_THU", 0) AS "SO_CHUA_NGHIEM_THU" , -- NotAcceptedAmount - decimal
			coalesce(OPN."TONG_CHI_PHI", 0) AS "TONG_CHI_PHI" ,  -- TotalAmount - decimal
			coalesce(OPN."STT", 0) AS "STT" ,
			CASE WHEN OPN.id IS NULL THEN 0
					ELSE 1
			END AS "DA_THEM"
		FROM    account_ex_don_dat_hang S
			LEFT JOIN account_ex_chi_phi_do_dang OPN ON S.id = OPN."DON_HANG_ID"
										AND OPN."CHI_NHANH_ID" = tham_so_chi_nhanh
			LEFT JOIN res_partner A ON A.id = S."KHACH_HANG_ID"
		WHERE   S."TINH_GIA_THANH" = TRUE
		--         AND S."CHI_NHANH_ID" = tham_so_chi_nhanh --Có tích chọn tính giá thành & tình trạng khác Hủy bỏ, đã hoàn thành.
		ORDER BY S.date_order ,
			S."SO_DON_HANG";
		END IF;

		IF tham_so_loai_cpdd = 4
		THEN
		DROP TABLE IF EXISTS TMP_KET_QUA;
		CREATE TEMP TABLE TMP_KET_QUA
		AS
		SELECT
			coalesce(OPN.id, row_number() OVER (PARTITION BY true::boolean)) AS "ID_CHUNG_TU" , -- OPNID - uniqueidentifier
			tham_so_chi_nhanh AS "CHI_NHANH_ID" , -- BranchID - uniqueidentifier
			C.id AS "HOP_DONG_ID" ,-- uniqueidentifier
			C."SO_HOP_DONG" ,-- nvarchar(25)
			C."NGAY_KY" ,-- datetime
			C."TRICH_YEU" ,-- nvarchar(255)
			Ao.id AS "DOI_TUONG_ID" ,-- nvarchar(255)
			AO."HO_VA_TEN" AS "TEN_DOI_TUONG",
			ts_154 AS "TAI_KHOAN_CPSXKD_DO_DANG_ID",
			ten_tk AS "MA_TAI_KHOAN_CPDD",
			coalesce(OPN."CHI_PHI_NVL_TRUC_TIEP", 0) AS "CHI_PHI_NVL_TRUC_TIEP" , -- DirectMatetialAmount - decimal
			coalesce(OPN."CHI_PHI_NVL_GIAN_TIEP", 0) AS "CHI_PHI_NVL_GIAN_TIEP" , -- IndirectMatetialAmount - decimal
			coalesce(OPN."CHI_PHI_NHAN_CONG_TRUC_TIEP", 0) AS "CHI_PHI_NHAN_CONG_TRUC_TIEP" , -- DirectLaborAmount - decimal
			coalesce(OPN."CHI_PHI_NHAN_CONG_GIAN_TIEP", 0) AS "CHI_PHI_NHAN_CONG_GIAN_TIEP" , -- IndirectLaborAmount - decimal
			coalesce(OPN."CHI_PHI_KHAU_HAO", 0) AS "CHI_PHI_KHAU_HAO" , -- DepreciationAmount - decimal
			coalesce(OPN."CHI_PHI_MUA_NGOAI", 0) AS "CHI_PHI_MUA_NGOAI" , -- PurchaseAmount - decimal
			coalesce(OPN."CHI_PHI_KHAC_CHUNG", 0) AS "CHI_PHI_KHAC_CHUNG" , -- OtherAmount - decimal
			coalesce(OPN."TONG", 0) AS "TONG" ,
			coalesce(OPN."MTC_CHI_PHI_NHAN_CONG", 0) AS "MTC_CHI_PHI_NHAN_CONG" ,
			coalesce(OPN."MTC_CHI_PHI_KHAU_HAO_DAU_KY", 0) AS "MTC_CHI_PHI_KHAU_HAO_DAU_KY" ,
			coalesce(OPN."MTC_CHI_PHI_MUA_NGOAI_DAU_KY", 0) AS "MTC_CHI_PHI_MUA_NGOAI_DAU_KY" ,
			coalesce(OPN."MTC_CHI_PHI_KHAC_CHUNG", 0) AS "MTC_CHI_PHI_KHAC_CHUNG" ,
			coalesce(OPN."SO_DA_NGHIEM_THU", 0) AS "SO_DA_NGHIEM_THU" , -- AcceptedAmount - decimal
			coalesce(OPN."SO_CHUA_NGHIEM_THU", 0) AS "SO_CHUA_NGHIEM_THU" , -- NotAcceptedAmount - decimal
			coalesce(OPN."TONG_CHI_PHI", 0) AS "TONG_CHI_PHI" ,  -- TotalAmount - decimal
			coalesce(OPN."STT", 0) AS "STT" ,
			CASE WHEN OPN.id IS NULL THEN 0
					ELSE 1
			END AS "DA_THEM"
		FROM    sale_ex_hop_dong_ban C
			LEFT JOIN account_ex_chi_phi_do_dang OPN ON C.id = OPN."HOP_DONG_ID"
										AND OPN."CHI_NHANH_ID" = tham_so_chi_nhanh
			LEFT JOIN res_partner AS AO ON C."KHACH_HANG_ID" = AO.id
		WHERE   C."TINH_GIA_THANH" = TRUE
			AND C."CHI_NHANH_ID" = tham_so_chi_nhanh --Có tích chọn tính giá thành & tình trạng khác Hủy bỏ, đã hoàn thành.
		ORDER BY c."NGAY_KY" ,
			C."SO_HOP_DONG";
		END IF;

		IF tham_so_loai_cpdd  IN (1,2)
		THEN
			UPDATE	TMP_KET_QUA R
			SET		"DA_THEM" = 1
			WHERE	EXISTS(SELECT * FROM TMP_KET_QUA T WHERE T."MA_PHAN_CAP" LIKE concat(R."MA_PHAN_CAP",'%%') AND T."DA_THEM" = 1)
			;
		END IF;

		IF tham_so_loai_cpdd = 6
		THEN
			SELECT "MA_PHAN_CAP"
			INTO ma_phan_cap
			FROM danh_muc_khoan_muc_cp AS EI
			WHERE "MA_KHOAN_MUC_CP" = 'CPSX'
			;

			DROP TABLE IF EXISTS TMP_KET_QUA
			;

			CREATE TEMP TABLE TMP_KET_QUA
				AS


					SELECT
						--                 CASE WHEN J.RefID IS NOT NULL THEN J.RefID ELSE NEWID() END AS RefID ,
						EI.id                    AS "KHOAN_MUC_CP_ID"
	--                     , "MA_KHOAN_MUC_CP"
						,concat((CASE WHEN "BAC" = 1 THEN '  ' WHEN "BAC" = 2 THEN '    ' WHEN "BAC" = 3 THEN '      ' WHEN "BAC" = 4 THEN '        ' ELSE '' END), "MA_KHOAN_MUC_CP") AS "MA_KHOAN_MUC_CP"
						, EI."TEN_KHOAN_MUC_CP"
						, parent_id
						, "BAC"
						, EI."LA_TONG_HOP"
						,"MA_PHAN_CAP"
						, --                 SortMISACodeID ,
						coalesce(J."SO_TIEN", 0) AS "SO_TIEN"
						, tham_so_chi_nhanh        AS "CHI_NHANH_ID"
						, CASE WHEN J.id IS NULL
						THEN 0
						ELSE 1
						END                                             AS "DA_THEM"
					FROM danh_muc_khoan_muc_cp AS EI
						LEFT JOIN account_ex_khai_bao_chi_phi_chung_can_phan_bo AS J ON J."KHOAN_MUC_CP_ID" = EI.id
																						AND
																						"CHI_NHANH_ID" = tham_so_chi_nhanh
					WHERE EI."MA_PHAN_CAP" LIKE concat(ma_phan_cap, '%%')
			;
		END IF
		;


		END $$;

		SELECT *FROM TMP_KET_QUA WHERE "DA_THEM" = 1;


		"""  
		record = self.execute(query, params)
		
		return record

	
	def action_nhap_khau_tu_excel(self):
		return self.env.ref('base_import_ex.action_nhap_khau_du_lieu_ban_dau_tu_excel').read()[0]