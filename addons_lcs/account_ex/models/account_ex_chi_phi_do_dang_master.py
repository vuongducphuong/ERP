# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class ACCOUNT_EX_CHI_PHI_DO_DANG_MASTER(models.Model):
	_name = 'account.ex.chi.phi.do.dang.master'
	_description = ''
	_inherit = ['mail.thread']
	NHAP_CHI_TIET_LOAI_CPDD_DTTHCP = fields.Boolean(string='Nhập chi tiết theo các yếu tố chi phí', help='Nhập chi tiết theo các yếu tố chi phí')
	NHAP_CHI_TIET_LOAI_CPDD_CONG_TRINH = fields.Boolean(string='Nhập chi tiết theo các yếu tố chi phí', help='Nhập chi tiết theo các yếu tố chi phí')
	NHAP_CHI_TIET_LOAI_CPDD_DON_HANG = fields.Boolean(string='Nhập chi tiết theo các yếu tố chi phí', help='Nhập chi tiết theo các yếu tố chi phí')
	NHAP_CHI_TIET_LOAI_CPDD_HOP_DONG = fields.Boolean(string='Nhập chi tiết theo các yếu tố chi phí', help='Nhập chi tiết theo các yếu tố chi phí')
	name = fields.Char(string='Name', help='Name', oldname='NAME')

	ACCOUNT_EX_CHI_PHI_DO_DANG_IDS = fields.One2many('account.ex.chi.phi.do.dang', 'CHI_PHI_DO_DANG_MASTER_ID', string='Chi phí dở dang')
	ACCOUNT_EX_KHAI_BAO_CHI_PHI_CHUNG_CAN_PHAN_BO_IDS = fields.One2many('account.ex.khai.bao.chi.phi.chung.can.phan.bo', 'CHI_PHI_DO_DANG_MASTER_ID', string='Khai báo chi phí chung cần phân bổ')


	
	@api.model
	def default_get(self,default_fields):
		res = super(ACCOUNT_EX_CHI_PHI_DO_DANG_MASTER, self).default_get(default_fields)
		config = self.env['gia.thanh.cau.hinh.so.du.dau.ky'].search([],limit=1)
		if config:
			res['NHAP_CHI_TIET_LOAI_CPDD_DTTHCP'] = config.CHI_TIET_THEO_DTTHCP
			res['NHAP_CHI_TIET_LOAI_CPDD_CONG_TRINH'] = config.CHI_TIET_THEO_CONG_TRINH
			res['NHAP_CHI_TIET_LOAI_CPDD_DON_HANG'] = config.CHI_TIET_THEO_DON_HANG
			res['NHAP_CHI_TIET_LOAI_CPDD_HOP_DONG'] = config.CHI_TIET_THEO_HOP_DONG
		return res

	@api.model
	def create(self, values):
		if values.get('ACCOUNT_EX_CHI_PHI_DO_DANG_IDS'):
			for line in values.get('ACCOUNT_EX_CHI_PHI_DO_DANG_IDS'):
				if line[2].get('LOAI_CHI_PHI_DO_DANG') == '1':
					chi_tiet_server = self.env['account.ex.chi.phi.do.dang'].search([('LOAI_CHI_PHI_DO_DANG', '=', line[2].get('LOAI_CHI_PHI_DO_DANG')),('MA_DOI_TUONG_THCP_ID', '=', line[2].get('MA_DOI_TUONG_THCP_ID'))])
				elif line[2].get('LOAI_CHI_PHI_DO_DANG') == '2':
					chi_tiet_server = self.env['account.ex.chi.phi.do.dang'].search([('LOAI_CHI_PHI_DO_DANG', '=', line[2].get('LOAI_CHI_PHI_DO_DANG')),('MA_CONG_TRINH_ID', '=', line[2].get('MA_CONG_TRINH_ID'))])
				elif line[2].get('LOAI_CHI_PHI_DO_DANG') == '3':
					chi_tiet_server = self.env['account.ex.chi.phi.do.dang'].search([('LOAI_CHI_PHI_DO_DANG', '=', line[2].get('LOAI_CHI_PHI_DO_DANG')),('DON_HANG_ID', '=', line[2].get('DON_HANG_ID'))])
				elif line[2].get('LOAI_CHI_PHI_DO_DANG') == '4':
					chi_tiet_server = self.env['account.ex.chi.phi.do.dang'].search([('LOAI_CHI_PHI_DO_DANG', '=', line[2].get('LOAI_CHI_PHI_DO_DANG')),('HOP_DONG_ID', '=', line[2].get('HOP_DONG_ID'))])
				for chi_tiet in chi_tiet_server:
					chi_tiet.unlink()

		chi_phi_chung_can_phan_bo_ids = self.env['account.ex.khai.bao.chi.phi.chung.can.phan.bo'].search([])
		if chi_phi_chung_can_phan_bo_ids:
			for line in chi_phi_chung_can_phan_bo_ids:
				line.unlink()
			
		master = self.env['account.ex.chi.phi.do.dang.master'].search([])
		if master:
			for mt in master:
				mt.unlink()

		# cập nhật lại bảng gia.thanh.cau.hinh.so.du.dau.ky
		# Đối tượng thcp
		if 'NHAP_CHI_TIET_LOAI_CPDD_DTTHCP' in values:
			cau_hinh_gia_thanh = self.env['gia.thanh.cau.hinh.so.du.dau.ky'].search([])
			if cau_hinh_gia_thanh:
				for line_cau_hinh in cau_hinh_gia_thanh:
					line_cau_hinh.write({'CHI_TIET_THEO_DTTHCP' : values.get('NHAP_CHI_TIET_LOAI_CPDD_DTTHCP')})
			else:
				self.env['gia.thanh.cau.hinh.so.du.dau.ky'].create({'CHI_TIET_THEO_DTTHCP' : values.get('NHAP_CHI_TIET_LOAI_CPDD_DTTHCP')})

		# công trình
		if 'NHAP_CHI_TIET_LOAI_CPDD_CONG_TRINH' in values:
			cau_hinh_gia_thanh = self.env['gia.thanh.cau.hinh.so.du.dau.ky'].search([])
			if cau_hinh_gia_thanh:
				for line_cau_hinh in cau_hinh_gia_thanh:
					line_cau_hinh.write({'CHI_TIET_THEO_CONG_TRINH' : values.get('NHAP_CHI_TIET_LOAI_CPDD_CONG_TRINH')})
			else:
				self.env['gia.thanh.cau.hinh.so.du.dau.ky'].create({'CHI_TIET_THEO_CONG_TRINH' : values.get('NHAP_CHI_TIET_LOAI_CPDD_CONG_TRINH')})
		
		# đơn hàng
		if 'NHAP_CHI_TIET_LOAI_CPDD_DON_HANG' in values:
			cau_hinh_gia_thanh = self.env['gia.thanh.cau.hinh.so.du.dau.ky'].search([])
			if cau_hinh_gia_thanh:
				for line_cau_hinh in cau_hinh_gia_thanh:
					line_cau_hinh.write({'CHI_TIET_THEO_DON_HANG' : values.get('NHAP_CHI_TIET_LOAI_CPDD_DON_HANG')})
			else:
				self.env['gia.thanh.cau.hinh.so.du.dau.ky'].create({'CHI_TIET_THEO_DON_HANG' : values.get('NHAP_CHI_TIET_LOAI_CPDD_DON_HANG')})

		# Hợp đồng
		if 'NHAP_CHI_TIET_LOAI_CPDD_HOP_DONG' in values:
			cau_hinh_gia_thanh = self.env['gia.thanh.cau.hinh.so.du.dau.ky'].search([])
			if cau_hinh_gia_thanh:
				for line_cau_hinh in cau_hinh_gia_thanh:
					line_cau_hinh.write({'CHI_TIET_THEO_HOP_DONG' : values.get('NHAP_CHI_TIET_LOAI_CPDD_HOP_DONG')})
			else:
				self.env['gia.thanh.cau.hinh.so.du.dau.ky'].create({'CHI_TIET_THEO_HOP_DONG' : values.get('NHAP_CHI_TIET_LOAI_CPDD_HOP_DONG')})

		# Tạo bản ghi không qua hàm supper
		if values.get('ACCOUNT_EX_CHI_PHI_DO_DANG_IDS'):
			for line in values.get('ACCOUNT_EX_CHI_PHI_DO_DANG_IDS'):
				if line[2].get('TONG') > 0:
					self.env['account.ex.chi.phi.do.dang'].create(line[2])

		if values.get('ACCOUNT_EX_KHAI_BAO_CHI_PHI_CHUNG_CAN_PHAN_BO_IDS'):
			for line in values.get('ACCOUNT_EX_KHAI_BAO_CHI_PHI_CHUNG_CAN_PHAN_BO_IDS'):
				if line[2].get('SO_TIEN') > 0:
					self.env['account.ex.khai.bao.chi.phi.chung.can.phan.bo'].create(line[2])

		values['ACCOUNT_EX_CHI_PHI_DO_DANG_IDS'] = {}
		values['ACCOUNT_EX_KHAI_BAO_CHI_PHI_CHUNG_CAN_PHAN_BO_IDS'] = {}
		result = super(ACCOUNT_EX_CHI_PHI_DO_DANG_MASTER, self).create(values)
	
		return result
	

	@api.onchange('NHAP_CHI_TIET_LOAI_CPDD_DTTHCP')
	def _onchange_NHAP_CHI_TIET_LOAI_CPDD_DTTHCP(self):
		if self.NHAP_CHI_TIET_LOAI_CPDD_DTTHCP == False:
			for line in self.ACCOUNT_EX_CHI_PHI_DO_DANG_IDS:
				line.CHI_PHI_KHAC_CHUNG = line.CHI_PHI_KHAC_CHUNG + line.CHI_PHI_NVL_GIAN_TIEP + line.CHI_PHI_NHAN_CONG_GIAN_TIEP + line.CHI_PHI_KHAU_HAO + line.CHI_PHI_MUA_NGOAI
				line.CHI_PHI_NVL_GIAN_TIEP = line.CHI_PHI_NHAN_CONG_GIAN_TIEP = line.CHI_PHI_KHAU_HAO = line.CHI_PHI_MUA_NGOAI = 0

	@api.onchange('NHAP_CHI_TIET_LOAI_CPDD_DON_HANG')
	def _onchange_NHAP_CHI_TIET_LOAI_CPDD_DON_HANG(self):
		if self.NHAP_CHI_TIET_LOAI_CPDD_DON_HANG == False:
			for line in self.ACCOUNT_EX_CHI_PHI_DO_DANG_IDS:
				line.CHI_PHI_KHAC_CHUNG = line.CHI_PHI_KHAC_CHUNG + line.CHI_PHI_NVL_GIAN_TIEP + line.CHI_PHI_NHAN_CONG_GIAN_TIEP + line.CHI_PHI_KHAU_HAO + line.CHI_PHI_MUA_NGOAI
				line.CHI_PHI_NVL_GIAN_TIEP = line.CHI_PHI_NHAN_CONG_GIAN_TIEP = line.CHI_PHI_KHAU_HAO = line.CHI_PHI_MUA_NGOAI = 0

	@api.onchange('NHAP_CHI_TIET_LOAI_CPDD_HOP_DONG')
	def _onchange_NHAP_CHI_TIET_LOAI_CPDD_HOP_DONG(self):
		if self.NHAP_CHI_TIET_LOAI_CPDD_HOP_DONG == False:
			for line in self.ACCOUNT_EX_CHI_PHI_DO_DANG_IDS:
				line.CHI_PHI_KHAC_CHUNG = line.CHI_PHI_KHAC_CHUNG + line.CHI_PHI_NVL_GIAN_TIEP + line.CHI_PHI_NHAN_CONG_GIAN_TIEP + line.CHI_PHI_KHAU_HAO + line.CHI_PHI_MUA_NGOAI
				line.CHI_PHI_NVL_GIAN_TIEP = line.CHI_PHI_NHAN_CONG_GIAN_TIEP = line.CHI_PHI_KHAU_HAO = line.CHI_PHI_MUA_NGOAI = 0

	# @api.onchange('NHAP_CHI_TIET_LOAI_CPDD_CONG_TRINH')
	# def _onchange_NHAP_CHI_TIET_LOAI_CPDD_CONG_TRINH(self):
	# 	if self.NHAP_CHI_TIET_LOAI_CPDD_CONG_TRINH == True:
	# 		for line in self.ACCOUNT_EX_CHI_PHI_DO_DANG_IDS:
	# 			line.MTC_CHI_PHI_KHAC_CHUNG = line.MTC_CHI_PHI_NVL_GIAN_TIEP + line.MTC_CHI_PHI_NHAN_CONG + line.MTC_CHI_PHI_KHAU_HAO_DAU_KY + line.MTC_CHI_PHI_MUA_NGOAI_DAU_KY
	# 			line.CHI_PHI_KHAC_CHUNG = line.MTC_CHI_PHI_NHAN_CONG + line.CHI_PHI_NHAN_CONG_GIAN_TIEP + line.CHI_PHI_KHAU_HAO + line.MTC_CHI_PHI_MUA_NGOAI_DAU_KY
	# 			line.MTC_CHI_PHI_NVL_GIAN_TIEP = line.MTC_CHI_PHI_NHAN_CONG = line.MTC_CHI_PHI_KHAU_HAO_DAU_KY = line.MTC_CHI_PHI_MUA_NGOAI_DAU_KY = 0
	# 			line.MTC_CHI_PHI_NHAN_CONG = line.CHI_PHI_NHAN_CONG_GIAN_TIEP = line.CHI_PHI_KHAU_HAO = line.MTC_CHI_PHI_MUA_NGOAI_DAU_KY = 0


	@api.model
	def lay_du_lieu_dtthcp(self, args):
		new_line = [[5]]
		chi_nhanh_id = self.get_chi_nhanh()
		du_lieu_dtthcp = self.lay_du_lieu_chi_phi_do_dang(1,chi_nhanh_id)
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
		return {'ACCOUNT_EX_CHI_PHI_DO_DANG_IDS': new_line}

	def compute_for_parent(self, fields, record, du_lieu_cong_trinh, cache):
		# Giả sử lấy CONG_TRINH_ID làm key cho cache
		if record.get('CONG_TRINH_ID') in cache:
			return cache.get(record.get('CONG_TRINH_ID'))
		if not record.get('isparent'):
			return record
		result = record
		for ct in du_lieu_cong_trinh:
			# Kiểm tra lại SQL với điều kiện này
			if ct.get('parent_id') == record.get('CONG_TRINH_ID'):
				if ct.get('isparent'):
					ct = self.compute_for_parent(fields, ct, du_lieu_cong_trinh, cache)
				for field in fields:
					result[field] = result.get(field, 0) + ct.get(field, 0)
		record.update(result)
		cache[record.get('CONG_TRINH_ID')] = record
		return record

	@api.model
	def lay_du_lieu_cong_trinh(self, args):
		new_line = [[5]]
		du_lieu_cong_trinh = self.lay_du_lieu_chi_phi_do_dang(2,self.get_chi_nhanh())
		# Bổ sung dữ liệu chi phi dở dang cho các công trình cha
		fields = ['CHI_PHI_NVL_TRUC_TIEP','CHI_PHI_NHAN_CONG_TRUC_TIEP','CHI_PHI_NVL_GIAN_TIEP','CHI_PHI_NHAN_CONG_GIAN_TIEP','CHI_PHI_KHAU_HAO','CHI_PHI_MUA_NGOAI','CHI_PHI_KHAC_CHUNG','TONG_CHI_PHI',\
				'MTC_CHI_PHI_NVL_GIAN_TIEP','MTC_CHI_PHI_NHAN_CONG','MTC_CHI_PHI_KHAU_HAO_DAU_KY','MTC_CHI_PHI_KHAC_CHUNG','MTC_CHI_PHI_MUA_NGOAI_DAU_KY','MTC_TONG','TONG','SO_DA_NGHIEM_THU','SO_CHUA_NGHIEM_THU']
		cache = {}
		for line in du_lieu_cong_trinh:
			line = self.compute_for_parent(fields, line, du_lieu_cong_trinh, cache)
		if du_lieu_cong_trinh:
			for ct in du_lieu_cong_trinh:
				record = self.env['danh.muc.cong.trinh'].browse(ct.get('CONG_TRINH_ID'))
				new_line += [(0,0,{
					'parent_id': [record.parent_id.id, record.parent_id.TEN_CONG_TRINH],
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
		return {'ACCOUNT_EX_CHI_PHI_DO_DANG_IDS': new_line}

	
	@api.model
	def lay_du_lieu_don_hang(self, args):
		new_line = [[5]]
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
		return {'ACCOUNT_EX_CHI_PHI_DO_DANG_IDS': new_line}

	@api.model
	def lay_du_lieu_hop_dong(self, args):
		new_line = [[5]]
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
		return {'ACCOUNT_EX_CHI_PHI_DO_DANG_IDS': new_line}



	@api.model
	def lay_du_lieu_chi_phi_chung(self, args):
		new_line = [[5]]
		chi_nhanh_id = self.get_chi_nhanh()
		chi_phi_chung_can_phan_bo_ids = self.lay_du_lieu_chi_phi_do_dang(6,chi_nhanh_id)
		# chi_phi_chung_can_phan_bo_ids = self.env['account.ex.khai.bao.chi.phi.chung.can.phan.bo'].search([])
		if chi_phi_chung_can_phan_bo_ids:
			for cpc in chi_phi_chung_can_phan_bo_ids:
				new_line += [(0,0,{
					# 'KHOAN_MUC_CP_ID' : [cpc.get('KHOAN_MUC_CP_ID'),cpc.get('MA_KHOAN_MUC_CP')],
					'KHOAN_MUC_CP_ID' : [cpc.get('KHOAN_MUC_CP_ID'), '\xa0\xa0\xa0\xa0' * cpc.get('BAC', 0) + cpc.get('MA_KHOAN_MUC_CP', '')],
					'TEN_KHOAN_MUC_CP' : cpc.get('TEN_KHOAN_MUC_CP'),
					'SO_TIEN' : cpc.get('SO_TIEN'),
					'LA_TONG_HOP' : cpc.get('LA_TONG_HOP'),
					})]
		return {'ACCOUNT_EX_KHAI_BAO_CHI_PHI_CHUNG_CAN_PHAN_BO_IDS': new_line}


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
						,concat((CASE WHEN "BAC" = 1 THEN '  ' WHEN "BAC" = 2 THEN '    ' WHEN "BAC" = 3 THEN '      ' WHEN "BAC" = 4 THEN '        ' ELSE '' END), "MA_KHOAN_MUC_CP") AS "MA_KHOAN_MUC_CP"
						, EI."TEN_KHOAN_MUC_CP"
						, parent_id
						, "BAC"
						, EI."LA_TONG_HOP"
                    	,"MA_PHAN_CAP"
						, --                 SortMISACodeID ,
						coalesce(J."SO_TIEN", 0) AS "SO_TIEN"
						, tham_so_chi_nhanh        AS "CHI_NHANH_ID"
					FROM danh_muc_khoan_muc_cp AS EI
						LEFT JOIN account_ex_khai_bao_chi_phi_chung_can_phan_bo AS J ON J."KHOAN_MUC_CP_ID" = EI.id
																						AND
																						"CHI_NHANH_ID" = tham_so_chi_nhanh
					WHERE EI."MA_PHAN_CAP" LIKE concat(ma_phan_cap, '%%')
			;

			--                 ORDER BY SortMISACodeID

		END IF
		;

		IF tham_so_loai_cpdd  IN (1,2)
		THEN
			UPDATE	TMP_KET_QUA R
			SET		"DA_THEM" = 1
			WHERE	EXISTS(SELECT * FROM TMP_KET_QUA T WHERE T."MA_PHAN_CAP" LIKE concat(R."MA_PHAN_CAP",'%%') AND T."DA_THEM" = 1)
			;
		END IF;


		END $$;

		SELECT *FROM TMP_KET_QUA;


		"""  
		record = self.execute(query, params)
		
		return record