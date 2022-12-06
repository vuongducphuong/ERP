# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime

class ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET(models.Model):
	_name = 'account.ex.so.du.tai.khoan.chi.tiet'
	_description = ''

	name = fields.Char(string='Name', help='Name', oldname='NAME')
	ID_TAI_KHOAN = fields.Integer(string='ID tài khoản', help='ID tài khoản')
	SO_TAI_KHOAN = fields.Char(string='Số tài khoản', help='Số tài khoản', compute='_compute_tai_khoan', store=True)
	TEN_TAI_KHOAN = fields.Char(string='Tên tài khoản', help='Tên tài khoản')
	TK_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản')
	state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái')
	# Không để related vì trường này dùng SQL để tính
	# Đã thử related nhưng client không lấy được dữ liệu: https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/1505
	TINH_CHAT_TAI_KHOAN = fields.Selection([
		('0', 'Dư Nợ'), 
		('1', 'Dư Có'), 
		('2', 'Lưỡng tính'), 
		('3', 'Không có số dư'),
	], )#related='TK_ID.TINH_CHAT')
	DU_NO = fields.Float(string='Dư Nợ', help='Dư Nợ', default=0,)# compute='_compute_DU_NO', store=True, )
	DU_CO = fields.Float(string='Dư Có', help='Dư Có', default=0,)# compute='_compute_DU_CO', store=True, )
	DU_NO_NGUYEN_TE = fields.Float(string='Dư nợ nguyên tệ', help='Dư nợ nguyên tệ')
	DU_CO_NGUYEN_TE = fields.Float(string='Dư có nguyên tệ', help='Dư có nguyên tệ')
	currency_id = fields.Many2one('res.currency', string='Loại tiền')
	SO_DU_TAI_KHOAN_ID = fields.Many2one('account.ex.so.du.tai.khoan', string='Số dư tài khoản', help='Số dư tài khoản', ondelete='cascade')
	NHAP_SO_DU_CHI_TIET = fields.Char(string='', default='Nhập số dư chi tiết')
	LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
	NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', default=fields.Datetime.now)
	NGAY_GHI_SO = fields.Date(string='Ngày ghi sổ', default=fields.Datetime.now)
	TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá', compute='_compute_ty_gia', store=True)
	DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng')
	TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng')
	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
	SO_CAI_ID = fields.Many2one('so.cai', ondelete='set null')
	SO_CONG_NO_ID = fields.Many2one('so.cong.no', ondelete='set null')
	CO_HACH_TOAN_NGOAI_TE = fields.Boolean(string='Có hạch toán ngoại tệ', help='Có hạch toán ngoại tệ')

	TK_NGAN_HANG_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='Số TK ngân hàng', help='Số TK ngân hàng')
	TEN_NGAN_HANG = fields.Char(string='Tên ngân hàng', help='Tên ngân hàng')
	KHAI_BAO_DAU_KY = fields.Boolean(string='Khai báo đầu kỳ', help='Khai báo đầu kỳ', default=True)
	
	# Chi tiết số dư
	ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS = fields.One2many('account.ex.sdtkct.theo.doi.tuong', 'SO_DU_TAI_KHOAN_CHI_TIET_ID', string='Nhập Số dư tài khoản')
	ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS = fields.One2many('account.ex.sdtkct.theo.hoa.don', 'SO_DU_TAI_KHOAN_CHI_TIET_ID', string='Nhập Số dư tài khoản')

	@api.depends('DU_NO','DU_CO','DU_NO_NGUYEN_TE','DU_CO_NGUYEN_TE')
	def _compute_ty_gia(self):
		for record in self:
			ty_gia = 1
			if record.DU_NO > 0 or record.DU_NO_NGUYEN_TE > 0:
				if record.DU_NO_NGUYEN_TE > 0:
					ty_gia = record.DU_NO/record.DU_NO_NGUYEN_TE
			elif record.DU_CO > 0 or record.DU_CO_NGUYEN_TE > 0:
				if record.DU_CO_NGUYEN_TE > 0:
					ty_gia = record.DU_CO/record.DU_CO_NGUYEN_TE
			record.TY_GIA = ty_gia

	@api.depends('TK_ID')
	def _compute_tai_khoan(self):
		for record in self:
			record.SO_TAI_KHOAN = record.TK_ID.SO_TAI_KHOAN
			record.TINH_CHAT_TAI_KHOAN = record.TK_ID.TINH_CHAT

	@api.onchange('currency_id')
	def _onchange_LOAI_TIEN_ID(self):
		if self.currency_id.MA_LOAI_TIEN == 'VND':
			self.CO_HACH_TOAN_NGOAI_TE = False
		else:
			self.CO_HACH_TOAN_NGOAI_TE = True

	@api.onchange('DU_NO','DU_CO')
	def _onchange_DU_NO(self):
		if self.SO_DU_TAI_KHOAN_ID.currency_id.MA_LOAI_TIEN == 'VND':
			self.DU_NO_NGUYEN_TE = self.DU_NO
			self.DU_CO_NGUYEN_TE = self.DU_CO

	def action_ghi_so(self):
		self.ghi_so_cai()
		if self.LOAI_CHUNG_TU in ('613','612','614'):
			self.ghi_cong_cong_no()
		self.write({'state':'da_ghi_so'})

	def ghi_so_cai(self):
		line_ids = []
		ngay_hach_toan_str = ''
		ngay_bat_dau_nam_tai_chinh = self.env['ir.config_parameter'].get_param('he_thong.TU_NGAY_BAT_DAU_TAI_CHINH')
		if ngay_bat_dau_nam_tai_chinh:
			ngay_bat_dau_nam_tai_chinh_date = datetime.strptime(ngay_bat_dau_nam_tai_chinh, '%Y-%m-%d').date()
			ngay_hach_toan = ngay_bat_dau_nam_tai_chinh_date + timedelta(days=-1)
			ngay_hach_toan_str = ngay_hach_toan.strftime('%Y-%m-%d')
		data_ghi_no = {}
		if self.LOAI_CHUNG_TU in ('613','612','614','610'):
			if self.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS:
				for line in self.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS:
					data_ghi_no = helper.Obj.inject(line, self)
					ty_gia = 1
					if (line.DU_NO > 0 and line.DU_NO_NGUYEN_TE) and line.DU_NO_NGUYEN_TE > 0:
						ty_gia = line.DU_NO/line.DU_NO_NGUYEN_TE
					else:
						if line.DU_CO_NGUYEN_TE > 0:
							ty_gia = line.DU_CO/line.DU_CO_NGUYEN_TE
					# if self.LOAI_CHUNG_TU == '610' and self.currency_id.MA_LOAI_TIEN != 'VND':
					# 	ty_gia = 0
					# else:
					# 	ty_gia = self.currency_id.TY_GIA_QUY_DOI
					data_ghi_no.update({
						'ID_CHUNG_TU': self.id,
						'MODEL_CHUNG_TU' : self._name,
						'CHI_TIET_ID' : line.id,
						'CHI_TIET_MODEL' : line._name,
						'LOAI_CHUNG_TU' : self.LOAI_CHUNG_TU,
						'SO_CHUNG_TU' : 'OPN',
						'NGAY_HACH_TOAN': ngay_hach_toan_str,
						'NGAY_CHUNG_TU': ngay_hach_toan_str,
						'TAI_KHOAN_ID': self.TK_ID.id,
						'currency_id' : self.currency_id.id,
						'TY_GIA' : ty_gia,
						'GHI_NO' : line.DU_NO,
						'GHI_CO': line.DU_CO,
						'GHI_NO_NGUYEN_TE': line.DU_NO_NGUYEN_TE,
						'GHI_CO_NGUYEN_TE': line.DU_CO_NGUYEN_TE,
						'NHAN_VIEN_ID' : line.NHAN_VIEN_ID.id if self.LOAI_CHUNG_TU != '614' else self.DOI_TUONG_ID.id,
						'DOI_TUONG_ID' : self.DOI_TUONG_ID.id if self.DOI_TUONG_ID else False,
						'CHI_NHANH_ID' : self.CHI_NHANH_ID.id,
						'LOAI_HACH_TOAN' : '1',
					})
					line_ids += [(0,0,data_ghi_no)]
			elif self.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS:
				for line2 in self.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS:
					data_ghi_no = helper.Obj.inject(line2, self)
					ty_gia = 1
					if (line2.DU_NO > 0 and line2.DU_NO_NGUYEN_TE) and line2.DU_NO_NGUYEN_TE > 0:
						ty_gia = line2.DU_NO/line2.DU_NO_NGUYEN_TE
					else:
						if line2.DU_CO_NGUYEN_TE > 0:
							ty_gia = line2.DU_CO/line2.DU_CO_NGUYEN_TE
					# if self.LOAI_CHUNG_TU == '610' and self.currency_id.MA_LOAI_TIEN != 'VND':
					# 	ty_gia = 0
					# else:
					# 	ty_gia = self.currency_id.TY_GIA_QUY_DOI
					data_ghi_no.update({
						'ID_CHUNG_TU': self.id,
						'MODEL_CHUNG_TU' : self._name,
						'CHI_TIET_ID' : line2.id,
						'CHI_TIET_MODEL' : line2._name,
						'LOAI_CHUNG_TU' : self.LOAI_CHUNG_TU,
						'SO_CHUNG_TU' : 'OPN',
						'NGAY_HACH_TOAN': ngay_hach_toan_str,
						'NGAY_CHUNG_TU': ngay_hach_toan_str,
						'TAI_KHOAN_ID': self.TK_ID.id,
						'currency_id' : self.currency_id.id,
						'TY_GIA' : ty_gia,
						'GHI_NO' : self.DU_NO,
						'GHI_CO': self.DU_CO,
						'GHI_NO_NGUYEN_TE': self.DU_NO_NGUYEN_TE,
						'GHI_CO_NGUYEN_TE': self.DU_CO_NGUYEN_TE,
						'NHAN_VIEN_ID' : line2.NHAN_VIEN_ID.id,
						'DOI_TUONG_ID' : self.DOI_TUONG_ID.id if self.DOI_TUONG_ID else False,
						'CHI_NHANH_ID' : self.CHI_NHANH_ID.id,
						'NHAN_VIEN_ID' : line2.NHAN_VIEN_ID.id if self.LOAI_CHUNG_TU != '614' else self.DOI_TUONG_ID.id,
						'SO_HOA_DON' : None,
						'NGAY_HOA_DON' : None,
						'LOAI_HACH_TOAN' : '1',
					})
					line_ids += [(0,0,data_ghi_no)]
			else:
				ty_gia = 1
				if (self.DU_NO > 0 and self.DU_NO_NGUYEN_TE) and self.DU_NO_NGUYEN_TE > 0:
					ty_gia = self.DU_NO/self.DU_NO_NGUYEN_TE
				else:
					if self.DU_CO_NGUYEN_TE > 0:
						ty_gia = self.DU_CO/self.DU_CO_NGUYEN_TE
				# if self.LOAI_CHUNG_TU == '610' and self.currency_id.MA_LOAI_TIEN != 'VND':
				# 		ty_gia = 0
				# else:
				# 	ty_gia = self.currency_id.TY_GIA_QUY_DOI
				data_ghi_no.update({
					'ID_CHUNG_TU': self.id,
					'MODEL_CHUNG_TU' : self._name,
					'LOAI_CHUNG_TU' : self.LOAI_CHUNG_TU,
					'SO_CHUNG_TU' : 'OPN',
					'NGAY_HACH_TOAN': ngay_hach_toan_str,
					'NGAY_CHUNG_TU': ngay_hach_toan_str,
					'TAI_KHOAN_ID': self.TK_ID.id,
					'currency_id' : self.currency_id.id,
					'TY_GIA' : ty_gia,
					'GHI_NO' : self.DU_NO,
					'GHI_CO': self.DU_CO,
					'GHI_NO_NGUYEN_TE': self.DU_NO_NGUYEN_TE,
					'GHI_CO_NGUYEN_TE': self.DU_CO_NGUYEN_TE,
					'DOI_TUONG_ID' : self.DOI_TUONG_ID.id if self.DOI_TUONG_ID else False,
					'CHI_NHANH_ID' : self.CHI_NHANH_ID.id,
					'NHAN_VIEN_ID' : self.DOI_TUONG_ID.id if self.LOAI_CHUNG_TU == '614' else False,
					'LOAI_HACH_TOAN' : '1',
				})
				line_ids += [(0,0,data_ghi_no)]
		else:
			ty_gia = 1
			if (self.DU_NO > 0 and self.DU_NO_NGUYEN_TE) and self.DU_NO_NGUYEN_TE > 0:
				ty_gia = self.DU_NO/self.DU_NO_NGUYEN_TE
			else:
				if self.DU_CO_NGUYEN_TE > 0:
					ty_gia = self.DU_CO/self.DU_CO_NGUYEN_TE
			data_ghi_no.update({
				'ID_CHUNG_TU': self.id,
				'MODEL_CHUNG_TU' : self._name,
				'LOAI_CHUNG_TU' : self.LOAI_CHUNG_TU,
				'SO_CHUNG_TU' : 'OPN',
				'NGAY_HACH_TOAN': ngay_hach_toan_str,
				'NGAY_CHUNG_TU': ngay_hach_toan_str,
				'TAI_KHOAN_ID': self.TK_ID.id,
				'currency_id' : self.currency_id.id,
				'TY_GIA' : 1 if self.currency_id.MA_LOAI_TIEN == 'VND' else 0,
				'GHI_NO' : self.DU_NO,
				'GHI_CO': self.DU_CO,
				'GHI_NO_NGUYEN_TE': self.DU_NO_NGUYEN_TE,
				'GHI_CO_NGUYEN_TE': self.DU_CO_NGUYEN_TE,
				'DOI_TUONG_ID' : self.DOI_TUONG_ID.id if self.DOI_TUONG_ID else False,
				'CHI_NHANH_ID' : self.CHI_NHANH_ID.id,
				'TAI_KHOAN_NGAN_HANG_ID' : self.TK_NGAN_HANG_ID.id,
				'LOAI_HACH_TOAN' : '1',
			})
			line_ids += [(0,0,data_ghi_no)]
			# thu_tu += 1
		# Tạo master
		sc = self.env['so.cai'].create({
			'name': 'OPN',
			'line_ids': line_ids,
			})
		self.write({'SO_CAI_ID':sc.id})
		return True


	def ghi_cong_cong_no(self):
		line_ids = []
		ngay_hach_toan_str = ''
		ngay_bat_dau_nam_tai_chinh = self.env['ir.config_parameter'].get_param('he_thong.TU_NGAY_BAT_DAU_TAI_CHINH')
		if ngay_bat_dau_nam_tai_chinh:
			ngay_bat_dau_nam_tai_chinh_date = datetime.strptime(ngay_bat_dau_nam_tai_chinh, '%Y-%m-%d').date()
			ngay_hach_toan = ngay_bat_dau_nam_tai_chinh_date + timedelta(days=-1)
			ngay_hach_toan_str = ngay_hach_toan.strftime('%Y-%m-%d')
		data_ghi_no = {}
		if self.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS:
			for line in self.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS:
				data_ghi_no = helper.Obj.inject(line, self)
				# ty_gia = 1
				# if (line.DU_NO > 0 and line.DU_NO_NGUYEN_TE) and line.DU_NO_NGUYEN_TE > 0:
				# 	ty_gia = line.DU_NO/line.DU_NO_NGUYEN_TE
				# else:
				# 	if line.DU_CO_NGUYEN_TE > 0:
				# 		ty_gia = line.DU_CO/line.DU_CO_NGUYEN_TE
				data_ghi_no.update({
					'ID_CHUNG_TU': self.id,
					'MODEL_CHUNG_TU' : self._name,
					'CHI_TIET_ID' : line.id,
					'CHI_TIET_MODEL' : line._name,
					'LOAI_CHUNG_TU' : self.LOAI_CHUNG_TU,
					'SO_CHUNG_TU' : 'OPN',
					'NGAY_HACH_TOAN': ngay_hach_toan_str,
					'NGAY_CHUNG_TU': ngay_hach_toan_str,
					'TK_ID': self.TK_ID.id,
					'currency_id' : self.currency_id.id,
					'TY_GIA' : self.currency_id.TY_GIA_QUY_DOI,
					'GHI_NO' : line.DU_NO,
					'GHI_CO': line.DU_CO,
					'GHI_NO_NGUYEN_TE': line.DU_NO_NGUYEN_TE if self.currency_id.MA_LOAI_TIEN != 'VND' else line.DU_NO,
					'GHI_CO_NGUYEN_TE': line.DU_CO_NGUYEN_TE if self.currency_id.MA_LOAI_TIEN != 'VND' else line.DU_CO,
					'NHAN_VIEN_ID' : line.NHAN_VIEN_ID.id if self.LOAI_CHUNG_TU != '614' else self.DOI_TUONG_ID.id,
					'DOI_TUONG_ID' : self.DOI_TUONG_ID.id if self.DOI_TUONG_ID else False,
					'CHI_NHANH_ID' : self.CHI_NHANH_ID.id,
					'LOAI_HACH_TOAN' : '1',
					'SO_HOP_DONG' : line.HOP_DONG_BAN_ID.SO_HOP_DONG,
					'TEN_DOI_TUONG' : self.TEN_DOI_TUONG,
				})
				line_ids += [(0,0,data_ghi_no)]
		elif self.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS and self.LOAI_CHUNG_TU != '614':
			for line2 in self.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS:
				data_ghi_no = helper.Obj.inject(line2, self)
				# ty_gia = 1
				# if (line2.DU_NO > 0 and line2.DU_NO_NGUYEN_TE) and line2.DU_NO_NGUYEN_TE > 0:
				# 	ty_gia = line2.DU_NO/line2.DU_NO_NGUYEN_TE
				# else:
				# 	if line2.DU_CO_NGUYEN_TE > 0:
				# 		ty_gia = line2.DU_CO/line2.DU_CO_NGUYEN_TE
				data_ghi_no.update({
					'ID_CHUNG_TU': self.id,
					'MODEL_CHUNG_TU' : self._name,
					'CHI_TIET_ID' : line2.id,
					'CHI_TIET_MODEL' : line2._name,
					'LOAI_CHUNG_TU' : self.LOAI_CHUNG_TU,
					'SO_CHUNG_TU' : 'OPN',
					'NGAY_HACH_TOAN': ngay_hach_toan_str,
					'NGAY_CHUNG_TU': ngay_hach_toan_str,
					'TK_ID': self.TK_ID.id,
					'currency_id' : self.currency_id.id,
					'TY_GIA' : self.currency_id.TY_GIA_QUY_DOI,
					'GHI_NO' : line2.SO_THU_TRUOC if self.LOAI_CHUNG_TU == '613' else line2.SO_CON_PHAI_THU,
					'GHI_CO': line2.SO_CON_PHAI_THU  if self.LOAI_CHUNG_TU == '613' else line2.SO_THU_TRUOC,
					'GHI_NO_NGUYEN_TE': line2.SO_THU_TRUOC_NGUYEN_TE  if self.LOAI_CHUNG_TU == '613' else line2.SO_CON_PHAI_THU_NGUYEN_TE,
					'GHI_CO_NGUYEN_TE': line2.SO_CON_PHAI_THU_NGUYEN_TE  if self.LOAI_CHUNG_TU == '613' else line2.SO_THU_TRUOC_NGUYEN_TE,
					# 'GHI_NO' : line2.SO_THU_TRUOC,
					# 'GHI_CO': line2.SO_CON_PHAI_THU,
					# 'GHI_NO_NGUYEN_TE': line2.SO_THU_TRUOC_NGUYEN_TE,
					# 'GHI_CO_NGUYEN_TE': line2.SO_CON_PHAI_THU_NGUYEN_TE,
					'NHAN_VIEN_ID' : line2.NHAN_VIEN_ID.id,
					'DOI_TUONG_ID' : self.DOI_TUONG_ID.id if self.DOI_TUONG_ID else False,
					'CHI_NHANH_ID' : self.CHI_NHANH_ID.id,
					'NHAN_VIEN_ID' : line2.NHAN_VIEN_ID.id if self.LOAI_CHUNG_TU != '614' else self.DOI_TUONG_ID.id,
					'LOAI_HACH_TOAN' : '1',
					'SO_HOA_DON' : None,
					'NGAY_HOA_DON' : None,
					'TEN_DOI_TUONG' : self.TEN_DOI_TUONG,
				})
				line_ids += [(0,0,data_ghi_no)]
		else:
			# ty_gia = 1
			# if (self.DU_NO > 0 and self.DU_NO_NGUYEN_TE) and self.DU_NO_NGUYEN_TE > 0:
			# 	ty_gia = self.DU_NO/self.DU_NO_NGUYEN_TE
			# else:
			# 	if self.DU_CO_NGUYEN_TE > 0:
			# 		ty_gia = self.DU_CO/self.DU_CO_NGUYEN_TE
			data_ghi_no.update({
				'ID_CHUNG_TU': self.id,
				'MODEL_CHUNG_TU' : self._name,
				'LOAI_CHUNG_TU' : self.LOAI_CHUNG_TU,
				'SO_CHUNG_TU' : 'OPN',
				'NGAY_HACH_TOAN': ngay_hach_toan_str,
				'NGAY_CHUNG_TU': ngay_hach_toan_str,
				'TK_ID': self.TK_ID.id,
				'currency_id' : self.currency_id.id,
				'TY_GIA' : self.currency_id.TY_GIA_QUY_DOI,
				'GHI_NO' : self.DU_NO,
				'GHI_CO': self.DU_CO,
				'GHI_NO_NGUYEN_TE': self.DU_NO_NGUYEN_TE,
				'GHI_CO_NGUYEN_TE': self.DU_CO_NGUYEN_TE,
				'DOI_TUONG_ID' : self.DOI_TUONG_ID.id if self.DOI_TUONG_ID else False,
				'CHI_NHANH_ID' : self.CHI_NHANH_ID.id,
				'NHAN_VIEN_ID' : self.DOI_TUONG_ID.id if self.LOAI_CHUNG_TU == '614' else False,
				'LOAI_HACH_TOAN' : '1',
				'TEN_DOI_TUONG' : self.TEN_DOI_TUONG,
			})
			line_ids += [(0,0,data_ghi_no)]
		# Tạo master
		sc = self.env['so.cong.no'].create({
			'name': 'OPN',
			'line_ids': line_ids,
			})
		self.write({'SO_CONG_NO_ID':sc.id})
		return True
	# @api.multi
	# def action_bo_ghi_so(self):
		# self.bo_ghi_so()





	
	@api.model_cr
	def init(self):
		self.env.cr.execute(""" 
				DROP  VIEW so_du_tai_khoan_chi_tiet_view;
				CREATE or REPLACE VIEW so_du_tai_khoan_chi_tiet_view
				AS
				SELECT    OPN.id AS "ID_CHUNG_TU" ,
									OPN."LOAI_CHUNG_TU" ,
									OPN."NGAY_HACH_TOAN" ,
									OPN."SO_TAI_KHOAN" ,
									OPN."TK_ID" AS "TAI_KHOAN_ID",
									OPN."DOI_TUONG_ID" ,
									OPN."currency_id" ,
									OPN."TY_GIA" ,
									OPN."DU_NO_NGUYEN_TE" ,
									OPN."DU_NO" ,
									OPN."DU_CO_NGUYEN_TE" ,
									OPN."DU_CO" ,
									OPN."TK_NGAN_HANG_ID" ,
									OPN."CHI_NHANH_ID" ,
				-- 					OPN.CashBook"NGAY_HACH_TOAN" ,
									OPN.create_date ,
									AC."SO_TAI_KHOAN" AS Expr1 ,
									AC.name AS "TEN_TAI_KHOAN" ,
									AO."MA_DOI_TUONG" ,
									AO.name AS "TEN_DOI_TUONG" ,
									BA."SO_TAI_KHOAN" AS "SO_TAI_KHOAN_NGAN_HANG" ,
									NH."TEN_DAY_DU" AS "TEN_NGAN_HANG",
									BA."NGAN_HANG_ID"
				FROM      account_ex_so_du_tai_khoan_chi_tiet OPN
									INNER JOIN danh_muc_he_thong_tai_khoan AC ON OPN."TK_ID" = AC.id
									LEFT JOIN res_partner AO ON OPN."DOI_TUONG_ID" = AO.id
									LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON OPN."TK_NGAN_HANG_ID" = BA.id
									LEFT JOIN danh_muc_ngan_hang NH ON NH.id = BA."NGAN_HANG_ID"
		""")
		
