# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ACCOUNT_EX_CHI_PHI_DO_DANG(models.Model):
	_name = 'account.ex.chi.phi.do.dang'
	_description = ''
	_inherit = ['mail.thread']
	TEN = fields.Char(string='Tên', help='Tên')
	SO_DU_BAN_DAU_ID = fields.Many2one('account.ex.nhap.so.du.ban.dau', string='Số dư ban đầu', help='Số dư ban đầu', ondelete='cascade')

	MA_DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Mã đối tượng THCP', help='Mã đối tượng tập hợp chi phí')
	TEN_DOI_TUONG_THCP = fields.Char(string='Tên đối tượng THCP', help='Tên đối tượng tập hợp chi phí')
	LOAI_DOI_TUONG_THCP = fields.Char(string='Loại đối tượng THCP', help='Loại đối tượng tập hợp chi phí')

	MA_CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Mã công trình', help='Mã công trình')
	parent_id = fields.Many2one('danh.muc.cong.trinh', related='MA_CONG_TRINH_ID.parent_id',store=True)
	TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình')
	LOAI_CONG_TRINH = fields.Many2one('danh.muc.loai.cong.trinh', string='Loại công trình', help='Loại công trình')

	DON_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn hàng', help='Đơn hàng')
	SO_DON_HANG = fields.Char(string='Số đơn hàng', help='Số đơn hàng', auto_num='account_ex_don_hang_SO_DON_HANG')
	NGAY_DON_HANG = fields.Date(string='Ngày đơn hàng', help='Ngày đơn hàng')
	DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
	KHACH_HANG_ID = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng')

	HOP_DONG_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
	SO_HOP_DONG = fields.Char(string='Số hợp đồng', help='Số hợp đồng', auto_num='account_ex_hop_dong_SO_HOP_DONG')
	NGAY_KY = fields.Date(string='Ngày ký', help='Ngày ký')
	TRICH_YEU = fields.Char(string='Trích yếu', help='Trích yếu')
	# trường chuẩn
	CHI_PHI_NVL_TRUC_TIEP = fields.Float(string='NVL trực tiếp', help='Chi phí nguyên vật liệu trực tiếp đầu kỳ')#DirectMatetialAmount
	CHI_PHI_NHAN_CONG_TRUC_TIEP = fields.Float(string='Nhân công trực tiếp', help='Nhân công trực tiếp',digits=decimal_precision.get_precision('Product Price'))#DirectLaborAmount
	

	CHI_PHI_NVL_GIAN_TIEP = fields.Float(string='NVL gián tiếp', help='Chi phí nguyên vật liệu gián tiếp đầu kỳ')#IndirectMatetialAmount 
	CHI_PHI_NHAN_CONG_GIAN_TIEP = fields.Float(string='Nhân công gián tiếp', help='Chi phí nhân công gián tiếp') #IndirectLaborAmount
	CHI_PHI_KHAU_HAO = fields.Float(string='Khấu hao', help='Chi phí khấu hao đầu kỳ') #DepreciationAmount
	CHI_PHI_MUA_NGOAI = fields.Float(string='Chi phí mua ngoài', help='Chi phí mua ngoài',digits=decimal_precision.get_precision('Product Price'))#PurchaseAmount
	CHI_PHI_KHAC_CHUNG = fields.Float(string='Chi phí khác', help='Chi phí khác/ chi phí chung')#OtherAmount
	TONG_CHI_PHI = fields.Float(string='Tổng chi phí', help='Tổng chi phí')
	CHI_PHI_CHUNG = fields.Float(string='Chi phí chung', help='Chi phí chung',related='CHI_PHI_KHAC_CHUNG')

	MTC_CHI_PHI_NVL_GIAN_TIEP = fields.Float(string='NVL gián tiếp', help='Chi phí nguyên vật liệu gián tiếp đầu kỳ (máy thi công)')#MachineIndirectMatetialAmount
	MTC_CHI_PHI_NHAN_CONG = fields.Float(string='Nhân công', help='Máy thi công - nhân công')#MachineIndirectLaborAmount
	MTC_CHI_PHI_KHAU_HAO_DAU_KY = fields.Float(string='Khấu hao', help='Chi phí khấu hao đầu kỳ (máy thi công)')#MachineDepreciationAmount
	MTC_CHI_PHI_KHAC_CHUNG = fields.Float(string='chi phí khác', help='chi phí khác/ chi phí chung (máy thi công)')#MachineOtherAmount
	MTC_CHI_PHI_MUA_NGOAI_DAU_KY = fields.Float(string='Chi phí mua ngoài', help='Chi phí mua ngoài đầu kỳ (máy thi công)')#MachinePurchaseAmount
	MTC_TONG = fields.Float(string='Tổng', help='Tổng (máy thi công)')
	MAY_THI_CONG = fields.Float(string='Máy thi công', help='Máy thi công',related='MTC_TONG')

	# Do related đang có lỗi (chỉ related 1 chiều) nên phải tự onchange
	@api.onchange('CHI_PHI_CHUNG')
	def _onchange_CHI_PHI_CHUNG(self):
		self.CHI_PHI_KHAC_CHUNG = self.CHI_PHI_CHUNG

	@api.onchange('MAY_THI_CONG')
	def _onchange_MAY_THI_CONG(self):
		self.MTC_TONG = self.MAY_THI_CONG

	TONG = fields.Float(string='Tổng', help='Tổng',digits=decimal_precision.get_precision('Product Price'), compute='tinh_tong_tien', store=True)#TotalAmount

	TAI_KHOAN_CPSXKD_DO_DANG_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản cpsxkd dở dang', help='Tài khoản cpsxkd dở dang')
	name = fields.Char(string='Name', help='Name', oldname='NAME')
	NHAP_SO_DU_BAN_DAU_ID = fields.Many2one('account.ex.nhap.so.du.ban.dau', string='Nhập số dư ban đầu', help='Nhập số dư ban đầu')
	MA_PHAN_CAP = fields.Char(string='Mã phân cấp', help='Mã phân cấp')
	THU_TU_THEO_MA_PHAN_CAP = fields.Integer(string='Thứ tự theo mã phân cấp', help='Thứ tự theo mã phân cấp')
	# CHI_PHI_NVL_GIAN_TIEP = fields.Float(string='Chi phí nguyên vật liệu gián tiếp đầu kỳ', help='Chi phí nguyên vật liệu gián tiếp đầu kỳ')
	SO_DA_NGHIEM_THU = fields.Float(string='Số đã nghiệm thu', help='Số đã nghiệm thu')#AcceptedAmount
	SO_CHUA_NGHIEM_THU = fields.Float(string='Số chưa nghiệm thu', help='Số chưa nghiệm thu', compute='tinh_tong_tien', store=True)
	STT = fields.Integer(string='Số thứ tự dòng', help='Số thứ tự dòng')
	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
	CHI_PHI_DO_DANG_MASTER_ID = fields.Many2one('account.ex.chi.phi.do.dang.master', string='Chi phí dở dang master', help='Chi phí dở dang master', ondelete='cascade')
	LOAI_CHI_PHI_DO_DANG = fields.Selection([('1', 'Đối tượng tập hợp chi phí'), ('2', 'Công trình'), ('3', 'Đơn hàng'), ('4', 'Hợp đồng')], string='Loại chứng từ')

	BAC = fields.Integer(string='Bậc', help='Bậc') 
	isparent = fields.Boolean(string='là đối tượng tổng hợp', help='Tên nhãn')
	#-----------------------------------------------------------------------------

	@api.depends('TONG_CHI_PHI','CHI_PHI_NVL_TRUC_TIEP','CHI_PHI_NHAN_CONG_TRUC_TIEP','MTC_TONG','SO_DA_NGHIEM_THU','MTC_TONG','CHI_PHI_KHAC_CHUNG')
	def tinh_tong_tien(self):
		for record in self: 
			if record.LOAI_CHI_PHI_DO_DANG in ('1','3','4'):
				record.TONG = record.TONG_CHI_PHI + record.CHI_PHI_NVL_TRUC_TIEP + record.CHI_PHI_NHAN_CONG_TRUC_TIEP
			elif record.LOAI_CHI_PHI_DO_DANG == '2':
				record.TONG = record.TONG_CHI_PHI + record.CHI_PHI_NVL_TRUC_TIEP + record.CHI_PHI_NHAN_CONG_TRUC_TIEP + record.MTC_TONG
			record.SO_CHUA_NGHIEM_THU = record.TONG - record.SO_DA_NGHIEM_THU
                

	# NVL_TRUC_TIEP = fields.Float(string='NVL trực tiếp', help='Nguyên vật liệu trực tiếp',digits=decimal_precision.get_precision('Product Price'))
	# NVL_GIAN_TIEP = fields.Float(string='NVL gián tiếp', help='Nguyên vật liệu gián tiếp',digits=decimal_precision.get_precision('Product Price'))
	# CHI_PHI_NHAN_CONG_TRUC_TIEP_DAU_KY = fields.Float(string='Nhân công trực tiếp', help='Nhân công trực tiếp',digits=decimal_precision.get_precision('Product Price'))
	# NHAN_CONG_TRUC_TIEP = fields.Float(string='Nhân công trực tiếp', help='Nhân công trực tiếp',digits=decimal_precision.get_precision('Product Price'))
	# CHI_PHI_NHAN_CONG_GIAN_TIEP = fields.Float(string='Nhân công trực tiếp', help='Nhân công trực tiếp',digits=decimal_precision.get_precision('Product Price'))
	# KHAU_HAO = fields.Float(string='Khấu hao', help='Khấu hao',digits=decimal_precision.get_precision('Product Price'))
	# CHI_PHI_MUA_NGOAI = fields.Float(string='Chi phí mua ngoài', help='Chi phí mua ngoài',digits=decimal_precision.get_precision('Product Price'))
	
	

	# CHI_PHI_CHUNG = fields.Float(string='Chi phí chung', help='Chi phí chung',digits=decimal_precision.get_precision('Product Price'))
	# TONG_HOP_CHI_PHI = fields.Float(string='Tổng hợp chi phí', help='Tổng hợp chi phí',digits=decimal_precision.get_precision('Product Price'))
	
	
	
	
	
	# CHI_PHI_NHAN_CONG_GIAN_TIEP = fields.Float(string='Chi phí nhân công gián tiếp', help='Chi phí nhân công gián tiếp')
	
	# CHI_PHI_MUA_NGOAI = fields.Float(string='Chi phí mua ngoài đầu kỳ', help='Chi phí mua ngoài đầu kỳ')
	# CHI_PHI_KHAC = fields.Float(string='chi phí khác', help='chi phí khác')


	# MTC_TONG = fields.Float(string='Máy thi công', help='Máy thi công')

	# Các trường của group Máy thi công 
	
	# MTC_CHI_PHI_NVL_TRUC_TIEP = fields.Float(string='Chi phí nguyên vật liệu trực tiếp đầu kỳ (máy thi công)', help='Chi phí nguyên vật liệu trực tiếp đầu kỳ (máy thi công)')
	# MTC_CHI_PHI_NHAN_CONG = fields.Float(string='Máy thi công - nhân công', help='Máy thi công - nhân công')
	# MTC_CHI_PHI_NHAN_CONG_GIAN_TIEP = fields.Float(string='Chi phí nhân công gián tiếp (máy thi công)', help='Chi phí nhân công gián tiếp (máy thi công)')
	# MTC_CHI_PHI_KHAU_HAO_DAU_KY = fields.Float(string='Chi phí khấu hao đầu kỳ (máy thi công)', help='Chi phí khấu hao đầu kỳ (máy thi công)')
	
	
	

	# Các trường của group Chi phí chung
	

	# CHI_PHI_NVL_TRUC_TIEP = fields.Float(string='Chi phí nguyên vật liệu gián tiếp đầu kỳ (Chi phí chung)', help='Chi phí nguyên vật liệu gián tiếp đầu kỳ (Chi phí chung)')
	# CHI_PHI_NHAN_CONG_GIAN_TIEP = fields.Float(string='Chi phí nhân công gián tiếp (Chi phí chung)', help='Chi phí nhân công gián tiếp (Chi phí chung)')
	# CHI_PHI_KHAU_HAO = fields.Float(string='Chi phí khấu hao đầu kỳ (Chi phí chung)', help='Chi phí khấu hao đầu kỳ (Chi phí chung)')
	# MTC_CHI_PHI_MUA_NGOAI_DAU_KY = fields.Float(string='Chi phí mua ngoài đầu kỳ (Chi phí chung)', help='Chi phí mua ngoài đầu kỳ (Chi phí chung)')
	# CHI_PHI_KHAC_CHUNG = fields.Float(string='chi phí khác (chi phí chung )', help='chi phí khác (chi phí chung )')
	# TONG_CHI_PHI = fields.Float(string='Tổng (chi phí chung)', help='Tổng (chi phí chung)')


	
	# TONG_CHI_PHI = fields.Float(string='Tổng chi phí', help='Tổng chi phí')
	

	@api.onchange('CHI_PHI_NVL_GIAN_TIEP','CHI_PHI_NHAN_CONG_GIAN_TIEP','CHI_PHI_KHAU_HAO','CHI_PHI_MUA_NGOAI','CHI_PHI_KHAC_CHUNG')
	def _onchange_NVL_GIAN_TIEP(self):
		
		self.TONG_CHI_PHI = self.CHI_PHI_NVL_GIAN_TIEP + self.CHI_PHI_NHAN_CONG_GIAN_TIEP + self.CHI_PHI_KHAU_HAO + self.CHI_PHI_MUA_NGOAI + self.CHI_PHI_KHAC_CHUNG
		# self.TONG_CHI_PHI = self.CHI_PHI_KHAC_CHUNG + self.CHI_PHI_NVL_TRUC_TIEP + self.CHI_PHI_NHAN_CONG_TRUC_TIEP

	@api.onchange('MTC_CHI_PHI_NVL_GIAN_TIEP','MTC_CHI_PHI_NHAN_CONG','MTC_CHI_PHI_KHAU_HAO_DAU_KY','MTC_CHI_PHI_KHAC_CHUNG','MTC_CHI_PHI_MUA_NGOAI_DAU_KY')
	def _onchange_MTC_CHI_PHI_NVL_GIAN_TIEP(self):
		self.MTC_TONG = self.MTC_CHI_PHI_NVL_GIAN_TIEP + self.MTC_CHI_PHI_NHAN_CONG + self.MTC_CHI_PHI_KHAU_HAO_DAU_KY + self.MTC_CHI_PHI_KHAC_CHUNG + self.MTC_CHI_PHI_MUA_NGOAI_DAU_KY
		# self.MTC_TONG = self.MTC_CHI_PHI_NVL_GIAN_TIEP + self.MTC_CHI_PHI_NHAN_CONG + self.MTC_CHI_PHI_KHAU_HAO_DAU_KY + self.MTC_CHI_PHI_MUA_NGOAI_DAU_KY + self.MTC_CHI_PHI_KHAC_CHUNG


	# @api.onchange('CHI_PHI_NVL_TRUC_TIEP','CHI_PHI_NHAN_CONG_TRUC_TIEP','TONG_CHI_PHI','MTC_TONG')
	# def _onchange_CHI_PHI_CHUNG_CHI_PHI_NVL_GIAN_TIEP(self):
	# 	self.TONG_CHI_PHI = self.CHI_PHI_NVL_TRUC_TIEP + self.CHI_PHI_NHAN_CONG_GIAN_TIEP + self.CHI_PHI_KHAU_HAO + self.MTC_CHI_PHI_MUA_NGOAI_DAU_KY + self.CHI_PHI_KHAC_CHUNG
		# self.CHI_PHI_KHAC_CHUNG = self.CHI_PHI_NVL_TRUC_TIEP + self.CHI_PHI_NHAN_CONG_GIAN_TIEP + self.CHI_PHI_KHAU_HAO + self.MTC_CHI_PHI_MUA_NGOAI_DAU_KY + self.CHI_PHI_KHAC_CHUNG

	# @api.onchange('MTC_TONG','TONG_CHI_PHI','NVL_TRUC_TIEP','CHI_PHI_NHAN_CONG_TRUC_TIEP')
	# def _onchange_MTC_TONG(self):
	# 	self.TONG_CHI_PHI = self.MTC_TONG + self.TONG_CHI_PHI + self.NVL_TRUC_TIEP + self.CHI_PHI_NHAN_CONG_TRUC_TIEP




	