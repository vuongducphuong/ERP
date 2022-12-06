# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from datetime import timedelta, datetime

class BAO_CAO_UNC_VIETTINBANK(models.Model):
	_name = 'bao.cao.uy.nhiem.chi.viettinbank'
	_auto = False

	ref = fields.Char(string='Reffence ID')
	ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
	MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')
	LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ')#RefType
	NGAY_CHUNG_TU = fields.Char(string='Ngày chứng từ')#RefDate
	STK_NGAN_HANG = fields.Char(string='STK ngân hàng')#BankAccountNumber
	TEN_NGAN_HANG = fields.Char(string='Tên ngân hàng')#BankName
	CHI_NHANH_CUA_NGAN_HANG = fields.Char(string='Chi nhánh ngân hàng')#BranchOfBank
	TEN_NGAN_HANG_DI = fields.Char(string='Tên ngân hàng DI')#DIBankName
	CHU_TK_NGAN_HANG = fields.Char(string='Chủ TK ngân hàng')#BankOwner
	STK_NGAN_HANG_DOI_TUONG = fields.Char(string='Số tài khoản ngân hàng đối tượng')#AccountObjectBankAccount
	TEN_DOI_TUONG = fields.Char(string='Tên đối tượng')#AccountObjectName
	DIA_CHI_DOI_TUONG = fields.Char(string='Địa chỉ đối tượng')#AccountObjectAddress
	DIA_CHI_DOI_TUONG_DI = fields.Char(string='Địa chỉ đối tượng DI')#AccountObjectAddressDI
	TEN_NGAN_HANG_DOI_TUONG = fields.Char(string='Tên ngân hàng đối tượng')#AccountObjectBankName
	CHI_NHANH_NGAN_HANG_DOI_TUONG = fields.Char(string='Chi nhánh ngân hàng đối tượng')#BranchOfAccountObjectBank
	SO_CMND = fields.Char(string='Số CMND')#IdentificationNumber
	NGAY_CMND = fields.Date(string='Ngày CMND')#IssueDate
	NOI_CAP_CMND = fields.Char(string='Nơi cấp CMND')#IssueBy
	SO_DIEN_THOAI = fields.Char(string='Số điện thoại')#Tel
	DIEN_GIAI = fields.Char(string='Diễn giải')#JournalMemo
	LOAI_TIEN = fields.Char(string='Loại tiền')#CurrencyID
	TONG_TIEN = fields.Monetary(string='Tổng tiền',currency_field='currency_id')#TotalAmountOC
	SO_CHUNG_TU = fields.Char(string='Số chứng từ')#RefNo
	NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán')#PostedDate
	MA_CHI_NHANH = fields.Char(string='Mã chi nhánh')#BranchCode
	TAI_KHOAN_NGAN_HANG = fields.Char(string='Tài khoản ngân hàng')#BankAccount
	THONG_TIN_TEN_NGAN_HANG = fields.Char(string='Thông tin tên ngân hàng')#InfoBankName
	THONG_TIN_DIA_CHI_NGAN_HANG = fields.Char(string='Thông tin địa chỉ ngân hàng')#InfoBankAddress
	DIA_CHI_NGAN_HANG = fields.Char(string='Địa chỉ ngân hàng')#Address
	TEN_CHI_NHANH_NGAN_HANG = fields.Char(string='Tên chi nhánh ngân hàng')#BankBranchName
	TAI_KHOAN_DOI_TUONG = fields.Char(string='Tài khoản đối tượng')#AccountingObjectCode
	TY_GIA = fields.Float(string='Tỷ giá')#ExchangeRate
	TONG_TIEN_QUY_DOI = fields.Float(string='Tổng tiền quy đổi')#TotalAmount
	

	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())

	ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.uy.nhiem.chi.viettinbank.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')


class BAO_CAO_UNC_VIETTINBANK_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_vietinbankunc'

	@api.model
	def get_report_values(self, docids, data=None):
		refTypeList, records = self.get_reftype_list(data)
		
		env = self.env['report.bao_cao.template_agribankunc']

		sql_result = env.ham_lay_du_lieu_tra_ve(refTypeList)

		for line in sql_result:
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
			
			master_data = self.env['bao.cao.uy.nhiem.chi.viettinbank'].convert_for_update(line)
			detail_data = self.env['bao.cao.uy.nhiem.chi.viettinbank.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
				records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.uy.nhiem.chi.viettinbank.chi.tiet'].new(detail_data)
		
		docs = [records.get(k) for k in records]
		for record in docs:
			
			if not record.LOAI_TIEN:
				record.currency_id = self.lay_loai_tien_mac_dinh()
			else:
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', record.LOAI_TIEN)],limit=1)
				if loai_tien_id:
					record.currency_id = loai_tien_id.id
			
			for line in record.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
				line.currency_id = record.currency_id

			str_tai_ngan_hang_doi_tuong = ""
			if not record.CHI_NHANH_NGAN_HANG_DOI_TUONG:
				str_tai_ngan_hang_doi_tuong = record.TEN_NGAN_HANG_DOI_TUONG
			else:
				str_tai_ngan_hang_doi_tuong = record.TEN_NGAN_HANG_DOI_TUONG + ' - ' + record.CHI_NHANH_NGAN_HANG_DOI_TUONG
			record.TEN_NGAN_HANG_DOI_TUONG = str_tai_ngan_hang_doi_tuong
			
			str_ngay_chung_tu = ""

			if not record.NGAY_CHUNG_TU:
				record.NGAY_CHUNG_TU = str_ngay_chung_tu
			else:
				record.NGAY_CHUNG_TU = datetime.strptime(record.NGAY_CHUNG_TU,'%Y-%m-%d %H:%M:%S').date().strftime('%d/%m/%Y')
				
		# Tạo object để in
		return {
			'docs':docs,
		}