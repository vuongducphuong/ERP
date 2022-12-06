# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision

class DANH_MUC_VAT_TU_HANG_HOA(models.Model):
	_name = 'danh.muc.vat.tu.hang.hoa'
	_description = 'Danh mục vật tư hàng hóa'
	_inherit = ['mail.thread']
	_order = "TEN"
	
	MA = fields.Char(string='Mã (*)', help='Mã', required=True, auto_num='sequence_danh_muc_vat_tu_hang_hoa_MA_VTHH')
	TEN = fields.Char(string='Tên (*)', help='Tên', required=True)
	TINH_CHAT = fields.Selection([('0', 'Vật tư hàng hóa'), ('1', 'Thành phẩm'), ('2', 'Dịch vụ'), ('3', 'Chỉ là diễn giải'), ], string='Tính chất', help='Tính chất',default="0",required=True)
	NHOM_VTHH = fields.Many2many('danh.muc.nhom.vat.tu.hang.hoa.dich.vu','vat_tu_hang_hoa_nhom_vthh_dich_vu_rel', string='Nhóm VTHH', help='Nhóm vật tư hàng hóa')
	MO_TA = fields.Text(string='Mô tả', help='Mô tả')
	DVT_CHINH_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT chính', help='Đơn vị tính chính')
	THOI_HAN_BH = fields.Selection([('1_THANG', '1 tháng'), ('2_THANG', '2 tháng'), ('3_THANG', '3 tháng'), ('6_THANG', '6 tháng'), ('9_THANG', '9 tháng'), ('1_NAM', '1 năm'), ('2_NAM', '2 năm'), ('3_NAM', '3 năm'), ('6_NAM', '6 năm'), ], string='Thời hạn BH', help='Thời hạn bh')
	SO_LUONG_TON_TOI_THIEU = fields.Float(string='SL tồn tối thiểu', help='Số lượng tồn tối thiểu', digits=decimal_precision.get_precision('SO_LUONG'))
	CHO_PHEP_XUAT_QUA_SL_TON = fields.Boolean(string='Cho phép xuất quá số lượng tồn', help='Cho phép xuất quá số lượng tồn', default=True)
	NGUON_GOC = fields.Char(string='Nguồn gốc', help='Nguồn gốc')
	DIEN_GIAI_KHI_MUA = fields.Char(string='Diễn giải khi mua', help='Diễn giải khi mua')
	DIEN_GIAI_KHI_BAN = fields.Char(string='Diễn giải khi bán', help='Diễn giải khi bán')
	CHIET_KHAU = fields.Boolean(string='Chiết khấu', help='Chiết khấu')
	LOAI_CHIET_KHAU = fields.Selection([('THEO_PT', 'Theo %'), ('THEO_SO_TIEN', 'Theo số tiền'), ('THEO_DON_GIA', 'Theo đơn giá (số tiền CK/ 1 đơn vị SL)'), ], string='Loại chiết khấu', help='Loại chiết khấu',default="THEO_PT", required="1")
	KHO_NGAM_DINH_ID = fields.Many2one('danh.muc.kho', string='Kho ngầm định', help='Kho ngầm định')
	TAI_KHOAN_KHO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản kho', help='Tài khoản kho')
	TK_DOANH_THU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK doanh thu', help='Tài khoản doanh thu')
	TK_CHIET_KHAU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chiết khấu', help='Tài khoản chiết khấu')
	TK_GIAM_GIA_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK giảm giá', help='Tài khoản giảm giá')
	TK_TRA_LAI_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK trả lại', help='Tài khoản trả lại')
	TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chi phí', help='Tài khoản chi phí')
	TY_LE_CKMH = fields.Float(string='Tỷ lệ CKMH (%)', help='Tỷ lệ chiết khấu mua hàng')
	DON_GIA_MUA_CO_DINH = fields.Float(string='Đơn giá mua cố định', help='Đơn giá mua cố định',digits=decimal_precision.get_precision('DON_GIA'))
	DON_GIA_MUA_GAN_NHAT = fields.Float(string='Đơn giá mua gần nhất', help='Đơn giá mua gần nhất',digits=decimal_precision.get_precision('DON_GIA'))
	DON_GIA_BAN = fields.Float(string='Đơn giá bán', help='Đơn giá bán',digits=decimal_precision.get_precision('DON_GIA'))
	THUE_SUAT_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang', string='Thuế suất GTGT (%)', help='Thuế suất giá trị gia tăng')
	THUE_SUAT_THUE_NK = fields.Float(string='Thuế suất thuế NK (%)', help='Thuế suất thuế nhập khẩu')
	THUE_SUAT_THUE_XK = fields.Float(string='Thuế suất thuế XK (%)', help='Thuế suất thuế xuất khẩu')
	NHOM_HHDV_CHIU_THUE_TTDB_ID = fields.Many2one('danh.muc.bieu.thue.tieu.thu.dac.biet', string='Nhóm hhdv chịu thuế TTĐB', help='Nhóm hhdv chịu thuế tiêu thụ đặc biệt')
	active = fields.Boolean( string='Theo dõi', help='Theo dõi', default=True)
	SO_LUONG_TON = fields.Float(string='Số lượng tồn', help='Số lượng tồn', digits=decimal_precision.get_precision('SO_LUONG'))
	GIA_TRI_TON = fields.Float(string='Giá trị tồn', help='Số lượng tồn', digits=decimal_precision.get_precision('VND'))
	GIA_BAN_1 = fields.Float(string='Đơn giá bán 1', help='Đơn giá bán 1',digits=decimal_precision.get_precision('VND'))
	GIA_BAN_2 = fields.Float(string='Đơn giá bán 2', help='Đơn giá bán 2',digits=decimal_precision.get_precision('VND'))
	GIA_BAN_3 = fields.Float(string='Đơn giá bán 3', help='Đơn giá bán 3',digits=decimal_precision.get_precision('VND'))
	GIA_CO_DINH = fields.Float(string='Đơn giá cố định', help='Đơn giá cố định',digits=decimal_precision.get_precision('VND'))
	name = fields.Char(string='Name', help='Name', related='MA', store=True)
	BAR_CODE = fields.Char(string='Mã vạch', help='Mã vạch')
	MA_PHAN_CAP = fields.Char(string='Mã phân cấp', help='Mã phân cấp')
	MA_NHOM_VTHH = fields.Char(string='Mã nhóm vật tư hàng hóa', help='Mã nhóm vật tư hàng hóa')
	LA_DON_GIA_SAU_THUE = fields.Boolean(string='Là đơn giá sau thuế', help='Là đơn giá sau thuế')
	LA_HE_THONG = fields.Boolean(string='Là hệ thống', help='Là hệ thống')
	THEO_DOI_THEO_MA_QUY_CACH = fields.Boolean(string='Theo dõi theo mã quy cách', help='Theo dõi theo mã quy cách')
	PHUONG_PHAP_TINH_GIA = fields.Integer(string='Phương pháp tính giá', help='Phương pháp tính giá')
	LIST_NHOM_VTHH = fields.Char(string='List các nhóm vthh', help='List các nhóm vthh', compute='_compute_list', store=True)
	LIST_TEN_NHOM_VTHH = fields.Char(string='List tên các nhóm vthh', help='List tên các nhóm vthh', compute='_compute_list', store=True)
	LIST_MPC_NHOM_VTHH = fields.Char(string='List mã phân cấp nhóm vật tư hàng hóa', help='List mã phân cấp nhóm vật tư hàng hóa', compute='_compute_list', store=True)
	
	@api.depends('NHOM_VTHH')
	def _compute_list(self):
		for record in self:
			record.LIST_TEN_NHOM_VTHH = record.lay_ten_nhom_vthh_dv()
			record.LIST_MPC_NHOM_VTHH = record.lay_ma_pc_nhom_vthh_dv()
			record.LIST_NHOM_VTHH = record.luu_nhom_vthh()

	#Mạnh thêm mới trường Đặc tính và Ảnh
	DAC_TINH = fields.Text(string='Đặc tính', help='Đặc tính')
	image = fields.Binary("Image", attachment=True,
	   help="Chọn logo",)

	# Mạnh thêm hai trường để làm task 3513
	DUA_TREN_CACH_TINH = fields.Selection([('CHU_VI_HCN', 'Chu vi hình chữ nhật'), ('DIEN_TICH_HCN', 'Diện tích hình chữ nhật'), ('THE_TICH_HHCN', 'Thể tích hình hộp chữ nhật'), ('CHU_VI_HT', 'Chu vi hình tròn'), ('DIEN_TICH_HT', 'Diện tích hình tròn'), ('THE_TICH_HINH_TRU', 'Thể tích hình trụ') ], string='Dựa trên cách tính', help='Dựa trên cách tính')
	THIET_LAP_CONG_THUC = fields.Char(string='Thiết lập công thức', help='Thiết lập công thức', compute='_compute_thiet_lap_cong_thuc' ,store=True)

	@api.depends('DUA_TREN_CACH_TINH')
	def _compute_thiet_lap_cong_thuc(self):
		for record in self:
			thietLapCongThuc = ''
			if record.DUA_TREN_CACH_TINH =='CHU_VI_HCN':
				thietLapCongThuc = '([Chiều dài]+[Chiều rộng])*2*[Lượng]'
			elif record.DUA_TREN_CACH_TINH =='DIEN_TICH_HCN':
				thietLapCongThuc = '[Chiều dài]*[Chiều rộng]*[Lượng]'
			elif record.DUA_TREN_CACH_TINH =='THE_TICH_HHCN':
				thietLapCongThuc = '[Chiều dài]*[Chiều rộng]*[Chiều cao]*[Lượng]'
			elif record.DUA_TREN_CACH_TINH =='CHU_VI_HT':
				thietLapCongThuc = '2*3.14*[Bán kính]*[Lượng]'
			elif record.DUA_TREN_CACH_TINH =='DIEN_TICH_HT':
				thietLapCongThuc = '3.14*[Bán kính]*[Bán kính]*[Lượng]'
			elif record.DUA_TREN_CACH_TINH =='THE_TICH_HINH_TRU':
				thietLapCongThuc = '3.14*[Bán kính]*[Bán kính]*[Chiều cao]*[Lượng]'
			record.THIET_LAP_CONG_THUC = thietLapCongThuc


	DANH_MUC_VAT_TU_HANG_HOA_MA_QUY_CACH_IDS = fields.One2many('danh.muc.vat.tu.hang.hoa.ma.quy.cach', 'VAT_TU_HANG_HOA_ID', string='Vật tư hàng hóa mã quy cách', copy=True)
	DANH_MUC_VAT_TU_HANG_HOA_CHIET_KHAU_IDS = fields.One2many('danh.muc.vat.tu.hang.hoa.chiet.khau', 'VAT_TU_HANG_HOA_ID', string='Vật tư hàng hóa chiết khấu', copy=True)
	DANH_MUC_VAT_TU_HANG_HOA_DAC_TINH_HINH_ANH_IDS = fields.One2many('danh.muc.vat.tu.hang.hoa.dac.tinh.hinh.anh', 'VAT_TU_HANG_HOA_ID', string='Vật tư hàng hóa đặc tính hình ảnh', copy=True)
	DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI_IDS = fields.One2many('danh.muc.vat.tu.hang.hoa.don.vi.chuyen.doi', 'VAT_TU_HANG_HOA_ID', string='Vật tư hàng hóa đơn vị chuyển đổi', copy=True)
	DANH_MUC_VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_IDS = fields.One2many('danh.muc.vat.tu.hang.hoa.chi.tiet.dinh.muc.nvl', 'VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_ID', string='Vật tư hàng hóa chi tiết định mức nguyên vật liệu', copy=True)

	DANH_MUC_VTHH_DON_GIA_MUA_CO_DINH_IDS = fields.One2many('danh.muc.vthh.don.gia.mua.co.dinh', 'VAT_TU_HANG_HOA_ID', string='VTHH Đơn giá mua cố định', copy=True)
	DANH_MUC_VTHH_DON_GIA_MUA_GAN_NHAT_IDS = fields.One2many('danh.muc.vthh.don.gia.mua.gan.nhat', 'VAT_TU_HANG_HOA_ID', string='VTHH Đơn giá mua gần nhất', copy=True)

	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

	GIA_VON = fields.Float(string='Giá vốn', help='tổng thành tiền của phần định mức nguyên vật liêu', compute='_compute_gia_von', store=False ,digits=decimal_precision.get_precision('VND')) 


	_sql_constraints = [
		('MA_uniq', 'unique ("MA")', 'Mã vật tư hàng hóa <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
	]

	@api.depends('DANH_MUC_VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_IDS')
	def _compute_gia_von(self):
		gia_von = 0
		for record in self:
			for line in record.DANH_MUC_VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_IDS:
				gia_von += line.THANH_TIEN
			record.GIA_VON = gia_von

	@api.model
	def create(self, values):
		# values['LIST_NHOM_VTHH'] = self.luu_nhom_vthh(values)
		result = super(DANH_MUC_VAT_TU_HANG_HOA, self).create(values)
		return result

	def luu_nhom_vthh(self):
		ten_nhom_vthh = ''
		if self.NHOM_VTHH:
			arr_list_ten_nhom_vthh = []
			for line in self.NHOM_VTHH:
				arr_list_ten_nhom_vthh.append(line.MA)
			ten_nhom_vthh = ",".join(arr_list_ten_nhom_vthh)
		return ten_nhom_vthh

		# nhom_vthh = ''
		# if self.NHOM_VTHH:
		# 	for line in self.NHOM_VTHH:
		# 		if nhom_vthh == '':
		# 			nhom_vthh = self.env['danh.muc.nhom.vat.tu.hang.hoa.dich.vu'].search([('id', '=', line.id)],limit=1).MA
		# 		else:
		# 			nhom_vthh += "," + self.env['danh.muc.nhom.vat.tu.hang.hoa.dich.vu'].search([('id', '=', line.id)],limit=1).MA
		# return nhom_vthh

	
	@api.multi
	def write(self, values):
		# values['LIST_NHOM_VTHH'] = self.luu_nhom_vthh(values)
		result = super(DANH_MUC_VAT_TU_HANG_HOA, self).write(values)
		return result
	
	@api.onchange('NHOM_VTHH')
	def _onchange_NHOM_VTHH(self):
		self.LIST_MPC_NHOM_VTHH = self.lay_ma_pc_nhom_vthh_dv()

	# @api.onchange('NHOM_VTHH')
	# def _onchange_NHOM_VTHH(self):
	# 	self.LIST_TEN_NHOM_VTHH = self.lay_ten_nhom_vthh_dv()

	def lay_ma_pc_nhom_vthh_dv(self):
		ma_pc_nhom_vthh = ''
		if self.NHOM_VTHH:
			for line in self.NHOM_VTHH:
				ma_pc_nhom_vthh += ";" + line.MA_PHAN_CAP
			ma_pc_nhom_vthh += ";"
		return ma_pc_nhom_vthh

	def lay_ten_nhom_vthh_dv(self):
		ten_nhom_vthh = ''
		if self.NHOM_VTHH:
			arr_list_ten_nhom_vthh = []
			for line in self.NHOM_VTHH:
				arr_list_ten_nhom_vthh.append(line.TEN)
			ten_nhom_vthh = ";".join(arr_list_ten_nhom_vthh)
		return ten_nhom_vthh
	

	@api.model
	def default_get(self, fields):
		rec = super(DANH_MUC_VAT_TU_HANG_HOA, self).default_get(fields)
		rec['TK_DOANH_THU_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like', '5111')], limit=1).id
		rec['TK_CHIET_KHAU_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like', '5211')], limit=1).id
		rec['TK_GIAM_GIA_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like', '5213')], limit=1).id
		rec['TK_TRA_LAI_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like', '5212')], limit=1).id
		rec['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like', '632')], limit=1).id
		arr_quy_cach = [(0, 0, {'MA_QUY_CACH' : 'Mã quy cách' + str(stt)}) for stt in range(1,5)]

		rec['DANH_MUC_VAT_TU_HANG_HOA_MA_QUY_CACH_IDS'] = arr_quy_cach
		
		# action['context'] = helper.Obj.merge(context, action.get('context'))
		return rec

	def compute_toan_tu_quy_doi(self, dvt):
		
		if len(self)==1 and dvt != self.DVT_CHINH_ID.id:
			for dv_chuyen_doi in self.DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI_IDS:
				if dv_chuyen_doi.DVT_ID.id == dvt: 
					if dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_NHAN':
						return '0'
					elif dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_CHIA':
						return '1'
		return '0'

	# Nếu không truyền đơn giá thì được hiểu là lấy đơn giá bán
	# Hiện tại, hàm này cũng chỉ tính được DON_GIA theo DON_GIA_BAN
	# Chưa áp dụng để tính DON_GIA khi DVT thay đổi. Nó chỉ đúng khi DVT trước khi thay đổi là DVT chính
	def compute_ty_le_chuyen_doi(self, dvt):
		
		if len(self)==1 and dvt != self.DVT_CHINH_ID.id:
			for dv_chuyen_doi in self.DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI_IDS:
				if dv_chuyen_doi.DVT_ID.id == dvt: 
					if dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_NHAN':
						return dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH 
					elif dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_CHIA':
						if dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH == 0:
							raise ValidationError("Tỷ lệ chuyển đổi đơn vị tính của <<%s - %s>> hiện tại đang bằng không. Vui lòng thay đổi tỷ lệ chuyển đổi đơn vị tính của sản phẩm này trong danh mục vật tư hàng hóa!" % (self.MA, self.TEN))
						return 1 / dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
			# Remove this code: Khi thay đổi mã hàng khác DVT chính thì hay bị lỗi này
			# if not self._context.get('fromMS'):
				# raise ValidationError('Đơn vị tính không phù hợp với vật tư hàng hóa <<%s - %s>>. Vui lòng chọn lại!!' % (self.MA, self.TEN))
		return 1

	# Nếu không truyền đơn giá thì được hiểu là lấy đơn giá bán
	# Hiện tại, hàm này cũng chỉ tính được DON_GIA theo DON_GIA_BAN
	# Chưa áp dụng để tính DON_GIA khi DVT thay đổi. Nó chỉ đúng khi DVT trước khi thay đổi là DVT chính
	def compute_DON_GIA_BAN(self, dvt, don_gia=None):
		if don_gia is None:
			don_gia = self.DON_GIA_BAN
		if len(self)==1 and dvt != self.DVT_CHINH_ID.id:
			for dv_chuyen_doi in self.DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI_IDS:
				if dv_chuyen_doi.DVT_ID.id == dvt: 
					if dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_NHAN':
						return dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH * don_gia
					elif dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_CHIA':
						if dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH == 0:
							raise ValidationError("Tỷ lệ chuyển đổi đơn vị tính của <<%s - %s>> hiện tại đang bằng không. Vui lòng thay đổi tỷ lệ chuyển đổi đơn vị tính của sản phẩm này trong danh mục vật tư hàng hóa!" % (self.MA, self.TEN))
						return don_gia / dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
			# Remove this code: Khi thay đổi mã hàng khác DVT chính thì hay bị lỗi này
			# if not self._context.get('fromMS'):
				# raise ValidationError('Đơn vị tính không phù hợp với vật tư hàng hóa <<%s - %s>>. Vui lòng chọn lại!!' % (self.MA, self.TEN))
		return don_gia

	def compute_DON_GIA_MUA_GAN_NHAT(self, dvt, don_gia=None):
		if don_gia is None:
			don_gia = self.DON_GIA_MUA_GAN_NHAT
		if len(self)==1 and dvt != self.DVT_CHINH_ID.id:
			for dv_chuyen_doi in self.DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI_IDS:
				if dv_chuyen_doi.DVT_ID.id == dvt: 
					if dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_NHAN':
						return dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH * don_gia
					elif dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_CHIA':
						if dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH == 0:
							raise ValidationError("Tỷ lệ chuyển đổi đơn vị tính của <<%s - %s>> hiện tại đang bằng không. Vui lòng thay đổi tỷ lệ chuyển đổi đơn vị tính của sản phẩm này trong danh mục vật tư hàng hóa!" % (self.MA, self.TEN))
						return don_gia / dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
			# Remove this code: Khi thay đổi mã hàng khác DVT chính thì hay bị lỗi này
			# if not self._context.get('fromMS'):
				# raise ValidationError('Đơn vị tính không phù hợp với vật tư hàng hóa <<%s - %s>>. Vui lòng chọn lại!!' % (self.MA, self.TEN))
		return don_gia
	
	def compute_SO_LUONG(self,soluong,dvt):
		if(dvt==self.DVT_CHINH_ID.id):
			return soluong
		else: 
			for dv_chuyen_doi in self.DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI_IDS:
				if dv_chuyen_doi.DVT_ID.id == dvt:
					if dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_NHAN':
						return dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH * soluong
					elif dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_CHIA':
						if dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH == 0:
							raise ValidationError("Tỷ lệ chuyển đổi đơn vị tính của <<%s - %s>> hiện tại đang bằng không. Vui lòng thay đổi tỷ lệ chuyển đổi đơn vị tính của sản phẩm này trong danh mục vật tư hàng hóa!" % (self.MA, self.TEN))
						return soluong / dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
			if not self._context.get('fromMS'):
				raise ValidationError('Đơn vị tính không phù hợp với vật tư hàng hóa <<%s - %s>>. Vui lòng chọn lại!!' % (self.MA, self.TEN))

	def compute_SO_LUONG_THEO_DVT_CHINH(self,soluong,dvt):
		ty_le_chuyen_doi = 1
		so_luong_theo_dvt_chinh = soluong
		if(dvt==self.DVT_CHINH_ID.id):
			return so_luong_theo_dvt_chinh
		else: 
			for dv_chuyen_doi in self.DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI_IDS:
				if dv_chuyen_doi.DVT_ID.id == dvt:
					ty_le_chuyen_doi = dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
					if ty_le_chuyen_doi != 0:
						if dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_NHAN':
							so_luong_theo_dvt_chinh = soluong/ty_le_chuyen_doi
						elif dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_CHIA':
							so_luong_theo_dvt_chinh = soluong*ty_le_chuyen_doi
		return so_luong_theo_dvt_chinh

	def compute_DON_GIA_THEO_DVT_CHINH(self,don_gia,dvt):
		ty_le_chuyen_doi = 1
		don_gia_theo_dvt_chinh = don_gia
		if(dvt!=self.DVT_CHINH_ID.id):
			for dv_chuyen_doi in self.DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI_IDS:
				if dv_chuyen_doi.DVT_ID.id == dvt:
					ty_le_chuyen_doi = dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
					if ty_le_chuyen_doi != 0:
						if dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_NHAN':
							don_gia_theo_dvt_chinh = don_gia/ty_le_chuyen_doi
						elif dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_CHIA':
							don_gia_theo_dvt_chinh = don_gia*ty_le_chuyen_doi
		return don_gia_theo_dvt_chinh

	@api.onchange('KHO_NGAM_DINH_ID')
	def _onchange_KHO_NGAM_DINH_ID(self):
		self.TAI_KHOAN_KHO_ID = self.KHO_NGAM_DINH_ID.TK_KHO_ID

	def lay_tai_khoan_kho(self):
		tk_kho = False
		if self.TAI_KHOAN_KHO_ID:
			tk_kho = self.TAI_KHOAN_KHO_ID.id
		elif self.KHO_NGAM_DINH_ID and self.KHO_NGAM_DINH_ID.TK_KHO_ID:
			tk_kho = self.KHO_NGAM_DINH_ID.TK_KHO_ID.id
		return tk_kho

	def lay_doi_tuong_thcp(self):
		doi_tuong_thcp_id = False
		doi_tuong_thcp_chi_tiet = self.env['danh.muc.chi.tiet.doi.tuong.tinh.gia.thanh'].search([('MA_HANG_ID', '=', self.id)])
		doi_tuong_tap_hop_chi_phi = self.env['danh.muc.doi.tuong.tap.hop.chi.phi'].search([('CHON_THANH_PHAM', '=', self.id)])
		if doi_tuong_thcp_chi_tiet:
			if len(doi_tuong_thcp_chi_tiet) == 1 and not doi_tuong_tap_hop_chi_phi:
				doi_tuong_thcp_id = doi_tuong_thcp_chi_tiet[0].DOI_TUONG_TONG_HOP_CHI_PHI_ID.id
		return doi_tuong_thcp_id

	def tinh_so_luong_theo_cong_thuc(self, CHIEU_DAI, CHIEU_RONG, CHIEU_CAO, BAN_KINH, LUONG):
		self.ensure_one()
		so_luong = None
		if self.TINH_CHAT in ('0','1'):
			if self.DUA_TREN_CACH_TINH =='CHU_VI_HCN':
				so_luong = (CHIEU_DAI + CHIEU_RONG) * 2 * LUONG
			elif self.DUA_TREN_CACH_TINH =='DIEN_TICH_HCN':
				so_luong = CHIEU_DAI * CHIEU_RONG * LUONG
			elif self.DUA_TREN_CACH_TINH =='THE_TICH_HHCN':
				so_luong = CHIEU_DAI * CHIEU_RONG * CHIEU_CAO * LUONG
			elif self.DUA_TREN_CACH_TINH =='CHU_VI_HT':
				so_luong = 2 * 3.14 * BAN_KINH * LUONG
			elif self.DUA_TREN_CACH_TINH =='DIEN_TICH_HT':
				so_luong = 3.14 * BAN_KINH * BAN_KINH * LUONG
			elif self.DUA_TREN_CACH_TINH =='THE_TICH_HINH_TRU':
				so_luong = 3.14 * BAN_KINH * BAN_KINH * CHIEU_CAO * LUONG

		return so_luong

	# Hàm lấy số lượng tồn ở tất cả kho
	def lay_so_luong_ton_tat_ca_kho(self, balance_date, IN_ref_order,branch_id):
		self.ensure_one()
		qty = 0
		params = {
			'vthh_id': self.id,
			'BalanceDate': balance_date,
			'INRefOrder': IN_ref_order,
			'BranchID': branch_id,
		}
		query = """
			DO LANGUAGE plpgsql $$
			DECLARE
			
				ngay_can_doi      TIMESTAMP :=%(BalanceDate)s; --@BalanceDate

				stt_loai_chung_tu TIMESTAMP :=%(INRefOrder)s; --@INRefOrder

				chi_nhanh_id      INT := %(BranchID)s;  -- id chi nhánh--@BranchID

				PHUONG_PHAP_TINH_GIA_XUAT_KHO   VARCHAR;

			BEGIN


				SELECT value INTO PHUONG_PHAP_TINH_GIA_XUAT_KHO FROM ir_config_parameter
				WHERE key='he_thong.PHUONG_PHAP_TINH_GIA_XUAT_KHO'FETCH FIRST 1 ROW ONLY;

				if PHUONG_PHAP_TINH_GIA_XUAT_KHO IS NULL
					THEN
					PHUONG_PHAP_TINH_GIA_XUAT_KHO = 'BINH_QUAN_TUC_THOI';
				END IF;

				DROP TABLE IF EXISTS TMP_KET_QUA
				;

				CREATE TEMP TABLE TMP_KET_QUA
					AS

						SELECT
							II.id
							, II."MA" as "MA_HANG"
							, II."TEN" AS "TEN_HANG"
							, COALESCE(II."SO_LUONG_TON_TOI_THIEU", 0)                                                       AS "SL_TON_TOI_THIEU"
							,
							--trường hợp là chứng từ k cập nhật đơn giá mà trừ số lượng thì mới lấy số lượng vào để trừ đi lúc tính giá
							SUM(COALESCE("SO_LUONG_NHAP_THEO_DVT_CHINH", 0) - COALESCE("SO_LUONG_XUAT_THEO_DVT_CHINH",
																						0))                                 AS "SO_LUONG_TON_THEO_DVT_CHINH"
							, SUM(COALESCE("SO_LUONG_NHAP_THEO_DVT_CHINH", 0) - COALESCE("SO_LUONG_XUAT_THEO_DVT_CHINH",
																						0))                                 AS "SO_LUONG_TON_THEO_DVT_CHINH_CHUNG_TU"
							,
							--Phải đẻ thêm món này để thông báo Xuất quá số lượng tồn theo từng chứng từ (ko phải theo từng dòng chi tiết)
							ngay_can_doi                                                                                   AS "NGAY_HACH_TOAN"
							,
							stt_loai_chung_tu                                                                              AS "STT_LOAI_CHUNG_TU"

						FROM  danh_muc_vat_tu_hang_hoa AS II
							--Chú ý: Phải LEFT JOIN để các Vật tư, kho nào chưa phát sinh thì vẫn phải lấy lên dòng có Số tồn = 0
							LEFT JOIN so_kho_chi_tiet IL ON IL."MA_HANG_ID" = II.id
															AND (PHUONG_PHAP_TINH_GIA_XUAT_KHO = 'GIA_DICH_DANH'
							OR (PHUONG_PHAP_TINH_GIA_XUAT_KHO <> 'GIA_DICH_DANH' AND (IL."NGAY_HACH_TOAN" < ngay_can_doi OR ("NGAY_HACH_TOAN" = ngay_can_doi AND "STT_LOAI_CHUNG_TU" <= stt_loai_chung_tu))))
															--bndinh 8/10/2015: sửa lỗi 73261, khi check số tồn thì lấy cả các chứng từ trùng giờ

															AND IL."CHI_NHANH_ID" = chi_nhanh_id

						WHERE II.id = %(vthh_id)s
						GROUP BY II.id,
							II."MA",
							II."TEN",
							COALESCE(II."SO_LUONG_TON_TOI_THIEU", 0)
				;
			END $$
			;

			SELECT  * from TMP_KET_QUA
		"""
		result = self.execute(query, params)
		if result:
			qty = result[0].get('SO_LUONG_TON_THEO_DVT_CHINH', 0)
		return qty

	# Hàm lấy số lượng tồn trong 1 kho tại một thời điểm
	# stock_id: ID của kho
	# balance_date: Ngày hạch toán, định dạng YYYY-MM-DD 00:00:00
	# IN_ref_order: Ngày giờ xuất kho, định dạng YYYY-MM-DD hh:mm:ss
	def lay_so_luong_ton(self, stock_id, balance_date, IN_ref_order,branch_id):
		self.ensure_one()
		qty = 0
		params = {
			'InventoryItemStockIDs': (','+ str(self.id) + ';' + str(stock_id) +','),
			'BalanceDate': balance_date,
			'INRefOrder': IN_ref_order,
			'BranchID': branch_id,
		}
		query = """
		DO LANGUAGE plpgsql $$
		DECLARE

			ds_vthh_kho_ids       VARCHAR := %(InventoryItemStockIDs)s;--(gồm id của mã vật tư hàng hóa và mã kho)  @InventoryItemStockIDs

			ngay_can_doi      TIMESTAMP :=%(BalanceDate)s; --@BalanceDate

			stt_loai_chung_tu TIMESTAMP :=%(INRefOrder)s; --@INRefOrder

			chi_nhanh_id      INT := %(BranchID)s;  -- id chi nhánh--@BranchID

			PHUONG_PHAP_TINH_GIA_XUAT_KHO   VARCHAR;

		BEGIN


			SELECT value INTO PHUONG_PHAP_TINH_GIA_XUAT_KHO FROM ir_config_parameter
			WHERE key='he_thong.PHUONG_PHAP_TINH_GIA_XUAT_KHO'FETCH FIRST 1 ROW ONLY;

			if PHUONG_PHAP_TINH_GIA_XUAT_KHO IS NULL
				THEN
				PHUONG_PHAP_TINH_GIA_XUAT_KHO = 'BINH_QUAN_TUC_THOI';
			END IF;



			DROP TABLE IF EXISTS TMP_VTHH_KHO
			;

			CREATE TEMP TABLE TMP_VTHH_KHO
			(
				"MA_HANG_ID" INT,
				"MA_KHO_ID"  INT

			)
			;


			INSERT INTO TMP_VTHH_KHO
			("MA_HANG_ID",
			"MA_KHO_ID")
				SELECT
					T.Value1
					, T.Value2
				FROM chuyen_chuoi_dinh_danh_guid_int_thanh_bang(ds_vthh_kho_ids, ',', ';') T
			;

			DROP TABLE IF EXISTS TMP_KET_QUA
			;

			CREATE TEMP TABLE TMP_KET_QUA
				AS

					SELECT
						TIIS."MA_HANG_ID"
						, II."MA" as "MA_HANG"
						, II."TEN" AS "TEN_HANG"
						, COALESCE(II."SO_LUONG_TON_TOI_THIEU", 0)                                                       AS "SL_TON_TOI_THIEU"
						, S."id" AS "MA_KHO_ID"
						, S."MA_KHO"
						, S."TEN_KHO"
						,
						--trường hợp là chứng từ k cập nhật đơn giá mà trừ số lượng thì mới lấy số lượng vào để trừ đi lúc tính giá
						SUM(COALESCE("SO_LUONG_NHAP_THEO_DVT_CHINH", 0) - COALESCE("SO_LUONG_XUAT_THEO_DVT_CHINH",
																					0))                                 AS "SO_LUONG_TON_THEO_DVT_CHINH"
						, SUM(COALESCE("SO_LUONG_NHAP_THEO_DVT_CHINH", 0) - COALESCE("SO_LUONG_XUAT_THEO_DVT_CHINH",
																					0))                                 AS "SO_LUONG_TON_THEO_DVT_CHINH_CHUNG_TU"
						,
						--Phải đẻ thêm món này để thông báo Xuất quá số lượng tồn theo từng chứng từ (ko phải theo từng dòng chi tiết)
						ngay_can_doi                                                                                   AS "NGAY_HACH_TOAN"
						,
						stt_loai_chung_tu                                                                              AS "STT_LOAI_CHUNG_TU"

					FROM TMP_VTHH_KHO AS TIIS
						INNER JOIN danh_muc_vat_tu_hang_hoa AS II ON TIIS."MA_HANG_ID" = II."id"
						INNER JOIN danh_muc_kho AS S ON TIIS."MA_KHO_ID" = S."id"
						--Chú ý: Phải LEFT JOIN để các Vật tư, kho nào chưa phát sinh thì vẫn phải lấy lên dòng có Số tồn = 0
						LEFT JOIN so_kho_chi_tiet IL ON IL."MA_HANG_ID" = TIIS."MA_HANG_ID" AND IL."KHO_ID" = TIIS."MA_KHO_ID"
														AND (PHUONG_PHAP_TINH_GIA_XUAT_KHO = 'GIA_DICH_DANH'
						OR (PHUONG_PHAP_TINH_GIA_XUAT_KHO <> 'GIA_DICH_DANH' AND (IL."NGAY_HACH_TOAN" < ngay_can_doi OR ("NGAY_HACH_TOAN" = ngay_can_doi AND "STT_LOAI_CHUNG_TU" <= stt_loai_chung_tu))))
														--bndinh 8/10/2015: sửa lỗi 73261, khi check số tồn thì lấy cả các chứng từ trùng giờ

														AND IL."CHI_NHANH_ID" = chi_nhanh_id


					GROUP BY TIIS."MA_HANG_ID",
						II."MA",
						II."TEN",
						COALESCE(II."SO_LUONG_TON_TOI_THIEU", 0),
						S."id",
						S."MA_KHO",
						S."TEN_KHO"
			;


		END $$

		;

		SELECT  * from TMP_KET_QUA
		"""
		result = self.execute(query, params)
		if len(result):
			qty = result[0].get('SO_LUONG_TON_THEO_DVT_CHINH', 0)
		return qty

	def lay_so_luong_ton_kho_hien_tai(self, items):
		result = {}
		params = {
			'LIST_VTHH' : items,
			'NGAY_HACH_TOAN' : str(self.lay_ngay_hach_toan()),
			}
		query = """   
			SELECT
				I."MA_HANG_ID"                                                           AS "MA_HANG_ID",
				SUM(I."SO_LUONG_NHAP_THEO_DVT_CHINH" - I."SO_LUONG_XUAT_THEO_DVT_CHINH") AS "SO_LUONG_TON",
				SUM(I."SO_TIEN_NHAP" - I."SO_TIEN_XUAT")                                 AS "GIA_TRI_TON"
			FROM so_kho_chi_tiet I
			INNER JOIN danh_muc_vat_tu_hang_hoa II ON I."MA_HANG_ID" = II.id
			INNER JOIN danh_muc_to_chuc BR ON I."CHI_NHANH_ID" = BR.id
			WHERE II."TINH_CHAT" <> '2' AND II."TINH_CHAT" <> '3'
				AND (I."MA_HANG_ID" = any( %(LIST_VTHH)s))
				AND I."NGAY_HACH_TOAN" <= %(NGAY_HACH_TOAN)s
			GROUP BY I."MA_HANG_ID"
		"""  
		self._cr.execute(query,params)
		for line in self._cr.dictfetchall():
			result[line.get('MA_HANG_ID')] = line
		return result

	# Tạm remove hàm này do chưa sử dụng
	# def lay_don_gia_mua_gan_nhat_theo_DVT_chinh(self):
	# 	if len(self) == 1:
	# 		result = self.execute("""SELECT "DON_GIA","DVT_ID" FROM purchase_document_line WHERE "MA_HANG_ID" = %s ORDER BY id DESC LIMIT 1""" % self.id)
	# 		if result:
	# 			return self.compute_DON_GIA_THEO_DVT_CHINH(result[0].get('DON_GIA'),result[0].get('DVT_ID'))
	# 	return 0

	@api.model
	def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
		result = super(DANH_MUC_VAT_TU_HANG_HOA, self).search_read(domain, fields, offset, limit, order)
		if not fields or 'SO_LUONG_TON' in fields:
			result = self.update_ton_kho(result)
		return result

	def update_ton_kho(self, result):
		if len(result):
			result_ids = [res.get('id') for res in result]
			ton_kho = self.lay_so_luong_ton_kho_hien_tai(result_ids)
			for res in result:
				if res.get('id') in ton_kho:
					res.update(ton_kho.get(res.get('id')))
		return result

	@api.multi
	def name_get_extend(self, fields=[]):
		result = super(DANH_MUC_VAT_TU_HANG_HOA, self).name_get_extend(fields)
		if 'SO_LUONG_TON' in fields:
			result = self.update_ton_kho(result)
		return result

	# @api.model
	# def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
	# 	return self.env['danh.muc.vat.tu.hang.hoa.view'].search_read(domain=None, fields=None, offset=0, limit=None, order=None)

class DANH_MUC_VAT_TU_HANG_HOA_VIEW(models.Model):
	_name = 'danh.muc.vat.tu.hang.hoa.view'
	_auto = False

	MA = fields.Char(string='Mã (*)', help='Mã')
	TEN = fields.Char(string='Tên (*)', help='Tên')
	TINH_CHAT = fields.Selection([('0', 'Vật tư hàng hóa'), ('1', 'Thành phẩm'), ('2', 'Dịch vụ'), ('3', 'Chỉ là diễn giải'), ], string='Tính chất', help='Tính chất',default="0",required=True)
	MO_TA = fields.Text(string='Mô tả', help='Mô tả')
	DVT_CHINH_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT chính', help='Đơn vị tính chính')
	THOI_HAN_BH = fields.Selection([('1_THANG', '1 tháng'), ('2_THANG', '2 tháng'), ('3_THANG', '3 tháng'), ('6_THANG', '6 tháng'), ('9_THANG', '9 tháng'), ('1_NAM', '1 năm'), ('2_NAM', '2 năm'), ('3_NAM', '3 năm'), ('6_NAM', '6 năm'), ], string='Thời hạn BH', help='Thời hạn bh')
	SO_LUONG_TON_TOI_THIEU = fields.Float(string='Số lượng tồn tối thiểu', help='Số lượng tồn tối thiểu', digits=decimal_precision.get_precision('SO_LUONG'))
	NGUON_GOC = fields.Char(string='Nguồn gốc', help='Nguồn gốc')
	DIEN_GIAI_KHI_MUA = fields.Char(string='Diễn giải khi mua', help='Diễn giải khi mua')
	DIEN_GIAI_KHI_BAN = fields.Char(string='Diễn giải khi bán', help='Diễn giải khi bán')
	CHIET_KHAU = fields.Boolean(string='Chiết khấu', help='Chiết khấu')
	LOAI_CHIET_KHAU = fields.Selection([('THEO_PT', 'Theo %'), ('THEO_SO_TIEN', 'Theo số tiền'), ('THEO_DON_GIA', 'Theo đơn giá (số tiền CK/ 1 đơn vị SL)'), ], string='Loại chiết khấu', help='Loại chiết khấu',default="THEO_PT", required="1")
	KHO_NGAM_DINH_ID = fields.Many2one('danh.muc.kho', string='Kho ngầm định', help='Kho ngầm định')
	TAI_KHOAN_KHO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản kho', help='Tài khoản kho')
	TK_DOANH_THU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK doanh thu', help='Tài khoản doanh thu')
	TK_CHIET_KHAU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chiết khấu', help='Tài khoản chiết khấu')
	TK_GIAM_GIA_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK giảm giá', help='Tài khoản giảm giá')
	TK_TRA_LAI_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK trả lại', help='Tài khoản trả lại')
	TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chi phí', help='Tài khoản chi phí')
	TY_LE_CKMH = fields.Float(string='Tỷ lệ CKMH (%)', help='Tỷ lệ chiết khấu mua hàng')
	DON_GIA_MUA_CO_DINH = fields.Float(string='Đơn giá mua cố định', help='Đơn giá mua cố định',digits=decimal_precision.get_precision('DON_GIA'))
	DON_GIA_MUA_GAN_NHAT = fields.Float(string='Đơn giá mua gần nhất', help='Đơn giá mua gần nhất',digits=decimal_precision.get_precision('DON_GIA'))
	DON_GIA_BAN = fields.Float(string='Đơn giá bán', help='Đơn giá bán',digits=decimal_precision.get_precision('DON_GIA'))
	THUE_SUAT_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang', string='Thuế suất GTGT (%)', help='Thuế suất giá trị gia tăng')
	THUE_SUAT_THUE_NK = fields.Float(string='Thuế suất thuế NK (%)', help='Thuế suất thuế nhập khẩu')
	THUE_SUAT_THUE_XK = fields.Float(string='Thuế suất thuế XK (%)', help='Thuế suất thuế xuất khẩu')
	NHOM_HHDV_CHIU_THUE_TTDB_ID = fields.Many2one('danh.muc.bieu.thue.tieu.thu.dac.biet', string='Nhóm hhdv chịu thuế TTĐB', help='Nhóm hhdv chịu thuế tiêu thụ đặc biệt')
	active = fields.Boolean( string='Theo dõi', help='Theo dõi', default=True)
	SO_LUONG_TON = fields.Float(string='Số lượng tồn', help='Số lượng tồn', digits=decimal_precision.get_precision('SO_LUONG'))
	GIA_BAN_1 = fields.Float(string='Đơn giá bán 1', help='Đơn giá bán 1',digits=decimal_precision.get_precision('VND'))
	GIA_BAN_2 = fields.Float(string='Đơn giá bán 2', help='Đơn giá bán 2',digits=decimal_precision.get_precision('VND'))
	GIA_BAN_3 = fields.Float(string='Đơn giá bán 3', help='Đơn giá bán 3',digits=decimal_precision.get_precision('VND'))
	GIA_CO_DINH = fields.Float(string='Đơn giá cố định', help='Đơn giá cố định',digits=decimal_precision.get_precision('VND'))
	name = fields.Char(string='Name', help='Name', related='MA', store=True)
	BAR_CODE = fields.Char(string='Mã vạch', help='Mã vạch')
	MA_PHAN_CAP = fields.Char(string='Mã phân cấp', help='Mã phân cấp')
	MA_NHOM_VTHH = fields.Char(string='Mã nhóm vật tư hàng hóa', help='Mã nhóm vật tư hàng hóa')
	LA_DON_GIA_SAU_THUE = fields.Boolean(string='Là đơn giá sau thuế', help='Là đơn giá sau thuế')
	LA_HE_THONG = fields.Boolean(string='Là hệ thống', help='Là hệ thống')
	THEO_DOI_THEO_MA_QUY_CACH = fields.Boolean(string='Theo dõi theo mã quy cách', help='Theo dõi theo mã quy cách')
	PHUONG_PHAP_TINH_GIA = fields.Integer(string='Phương pháp tính giá', help='Phương pháp tính giá')
	LIST_NHOM_VTHH = fields.Char(string='List các nhóm vthh', help='List các nhóm vthh')
	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

	@api.model_cr
	def init(self):
		self.env.cr.execute(""" 
			CREATE OR REPLACE VIEW public.tim_vat_tu_hang_hoa_theo_chi_nhanh AS
				SELECT ii.id AS "MA_HANG_ID",
					ii."CHI_NHANH_ID",
					ii."BAR_CODE",
					ii."MA" AS "MA_HANG",
					ii."TEN" AS "TEN_HANG",
					ii."TINH_CHAT",
					ii."LIST_NHOM_VTHH",
					ii."DIEN_GIAI_KHI_MUA",
					ii."DIEN_GIAI_KHI_BAN",
					ii."DVT_CHINH_ID",
					ii."THOI_HAN_BH",
					ii."SO_LUONG_TON_TOI_THIEU",
					ii."NGUON_GOC",
					ii."KHO_NGAM_DINH_ID",
					s."MA_KHO",
					s."TEN_KHO",
					ii."TAI_KHOAN_KHO_ID",
					ii."TK_NO_ID" AS "TK_CHI_PHI_ID",
					ii."TY_LE_CKMH",
					ii."DON_GIA_MUA_CO_DINH",
					ii."GIA_BAN_1",
					ii."GIA_BAN_2",
					ii."GIA_BAN_3",
					ii."GIA_CO_DINH",
					ii."LA_DON_GIA_SAU_THUE",
					ii."THUE_SUAT_GTGT_ID",
					ii."THUE_SUAT_THUE_NK",
					ii."THUE_SUAT_THUE_XK",
					ii."NHOM_HHDV_CHIU_THUE_TTDB_ID",
					ii."LA_HE_THONG",
					ii.active,
					ii."CHIET_KHAU",
					ii."LOAI_CHIET_KHAU",
					ii."THEO_DOI_THEO_MA_QUY_CACH",
					ii."PHUONG_PHAP_TINH_GIA",
					u.name AS "TEN_DVT",
					t.id AS "SO_CHI_NHANH_ID",
					ou."TEN_DON_VI" AS "TEN_CHI_NHANH",
					ii."TK_GIAM_GIA_ID",
					ii."TK_DOANH_THU_ID",
					ii."TK_TRA_LAI_ID",
					ii."TK_CHIET_KHAU_ID"
				FROM danh_muc_vat_tu_hang_hoa ii
					LEFT JOIN danh_muc_don_vi_tinh u ON ii."DVT_CHINH_ID" = u.id
					LEFT JOIN danh_muc_kho s ON ii."KHO_NGAM_DINH_ID" = s.id
					CROSS JOIN ( SELECT ou_1.id,
							ou_1.name,
							ou_1."MA_DON_VI",
							ou_1."TEN_DON_VI",
							ou_1."parent_id",
							ou_1."CAP_TO_CHUC",
							ou_1."TK_CHI_PHI_LUONG_ID",
							ou_1."TEN_TK_CHI_PHI_LUONG",
							ou_1."DIA_CHI",
							ou_1."MA_SO_THUE",
							ou_1."active",
							ou_1."MA_PHAN_CAP",
							ou_1."DIEN_THOAI",
							ou_1."FAX",
							ou_1."NGUOI_KY_CHUC_DANH_GIAM_DOC",
							ou_1."NGUOI_KY_TEN_GIAM_DOC",
							ou_1."NGUOI_KY_CHUC_DANH_KE_TOAN_TRUONG",
							ou_1."NGUOI_KY_TEN_KE_TOAN_TRUONG",
							ou_1."NGUOI_KY_CHUC_DANH_THU_KHO",
							ou_1."NGUOI_KY_TEN_THU_KHO",
							ou_1."NGUOI_KY_CHUC_DANH_THU_QUY",
							ou_1."NGUOI_KY_TEN_THU_QUY",
							ou_1."NGUOI_KY_CHUC_DANH_NGUOI_LAP_BIEU",
							ou_1."NGUOI_KY_TEN_NGUOI_LAP_BIEU",
							ou_1.message_last_post,
							ou_1.create_uid,
							ou_1.create_date,
							ou_1.write_uid,
							ou_1.write_date,
							ou_1."HACH_TOAN_DOC_LAP",
							ou_1."KE_KHAI_THUE_GTGT_TTDB_RIENG",
							ou_1."BAC",
							ou_1."ISPARENT",
							ou_1.parent_id,
							ou_1."NGUOI_KY_TIEU_DE_GIAM_DOC",
							ou_1."NGUOI_KY_TIEU_DE_TOAN_TRUONG",
							ou_1."NGUOI_KY_TIEU_DE_KHO",
							ou_1."NGUOI_KY_TIEU_DE_QUY",
							ou_1."NGUOI_KY_TIEU_DE_LAP_BIEU",
							ou_1."SO_DANG_KY",
							ou_1."NGAY_CAP",
							ou_1."NOI_CAP",
							ou_1."QUAN_HUYEN",
							ou_1."TINH_TP",
							ou_1."EMAIL",
							ou_1."WEBSITE",
							ou_1."DV_CHU_QUAN",
							ou_1."MST_DV_CHU_QUAN",
							ou_1."TK_NGAN_HANG_ID",
							ou_1."IN_TEN_NGUOI_KY",
							ou_1."LAY_TEN_NGUOI_LAP",
							ou_1."HACH_TOAN_SELECTION",
							ou_1.active
						FROM danh_muc_to_chuc ou_1
						WHERE ou_1."BAC" = ANY (ARRAY[1, 2])) t
					LEFT JOIN danh_muc_to_chuc ou ON ii."CHI_NHANH_ID" = ou.id;
		""")
		self.env.cr.execute(""" 
			DO LANGUAGE plpgsql $$
			--DECLARE
				--chi_nhanh_id INTEGER:= 81; Không sử dụng được biến ở đây
			BEGIN
			
			CREATE or REPLACE VIEW danh_muc_vat_tu_hang_hoa_view
			AS
			SELECT temp."MA_HANG_ID" as id,
				'' as "MA", --Cần update các cột này để hiển thị trên list
				'' as "TEN",
				ROW_NUMBER() OVER(ORDER BY "MA_HANG") as RowNum, *
			FROM	(SELECT  V.* ,
						coalesce(R."SO_LUONG_TON",0) AS "SO_LUONG_TON",
						coalesce(R."GIA_TRI_TON",0) AS "GIA_TRI_TON"
					FROM    (SELECT "MA_HANG_ID","SO_CHI_NHANH_ID",RowNum
							FROM 	(SELECT ROW_NUMBER() OVER(ORDER BY V."MA_HANG") as RowNum,
										V."SO_CHI_NHANH_ID",
										V."MA_HANG_ID"
									FROM tim_vat_tu_hang_hoa_theo_chi_nhanh AS V
									LEFT  JOIN 	(SELECT
													I."MA_HANG_ID" AS "MA_HANG_ID",
													SUM(I."SO_LUONG_NHAP_THEO_DVT_CHINH" - I."SO_LUONG_XUAT_THEO_DVT_CHINH") AS "SO_LUONG_TON"  ,
													SUM(I."SO_TIEN_NHAP" - I."SO_TIEN_XUAT") AS "GIA_TRI_TON"
												FROM so_kho_chi_tiet I
												INNER JOIN danh_muc_vat_tu_hang_hoa II ON I."MA_HANG_ID" = II.id
												INNER JOIN danh_muc_to_chuc BR ON I."CHI_NHANH_ID" = BR.id
												WHERE II."TINH_CHAT" <>  '2' AND II."TINH_CHAT" <> '3'
												GROUP BY I.id
												)  AS  R ON R."MA_HANG_ID" = v."MA_HANG_ID" 
							) AS tmp
					) AS T
					LEFT JOIN tim_vat_tu_hang_hoa_theo_chi_nhanh V ON T."MA_HANG_ID" = V."MA_HANG_ID"
					LEFT  JOIN 	(SELECT I."MA_HANG_ID",
									SUM(I."SO_LUONG_NHAP_THEO_DVT_CHINH" - I."SO_LUONG_XUAT_THEO_DVT_CHINH") AS "SO_LUONG_TON"  ,
									SUM(I."SO_TIEN_NHAP" - I."SO_TIEN_XUAT") AS "GIA_TRI_TON"
								FROM so_kho_chi_tiet I
								INNER JOIN danh_muc_vat_tu_hang_hoa II ON I."MA_HANG_ID" = II.id
								INNER JOIN danh_muc_to_chuc BR ON I."CHI_NHANH_ID" = BR.id
								WHERE II."TINH_CHAT" <>  '2' AND II."TINH_CHAT" <> '3'
								GROUP BY I."MA_HANG_ID"
					) AS  R 
					ON R."MA_HANG_ID" = v."MA_HANG_ID"
					WHERE ( T."SO_CHI_NHANH_ID"=V."SO_CHI_NHANH_ID")
			) as temp
			--WHERE   "SO_CHI_NHANH_ID"= chi_nhanh_id --Không sử dụng được biến ở đây
			ORDER BY RowNum ;
			END $$;
		""")