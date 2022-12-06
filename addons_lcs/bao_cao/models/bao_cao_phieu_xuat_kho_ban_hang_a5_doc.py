# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round

class BAO_CAO_PHIEU_XUAT_KHO_BAN_HANG_A5_DOC(models.Model):
	_name = 'bao.cao.phieu.xuat.kho.ban.hang.a5.doc'
	_auto = False

	ref = fields.Char(string='Reffence ID')

	ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
	MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')
	LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ') #Reftype
	TEN_KHACH_HANG = fields.Char(string='Tên khách hàng') #AccountObjectName
	DIA_CHI = fields.Char(string='Địa chỉ') #AccountObjectAddress
	MA_SO_THUE = fields.Char(string='Mã số thuế') #AccountObjectTaxCode
	NGUOI_MUA = fields.Char(string='Người mua') #Buyer
	SO_CT_GOC_KEM_THEO = fields.Integer(string='Số CT gốc kèm theo') #DocumentIncluded
	SO_DIEN_THOAI = fields.Char(string='Số điện thoại') #Tel
	TEN_NHAN_VIEN_BAN_HANG = fields.Char(string='Tên nhân viên bán hàng') #EmployeeName
	DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải') #JournalMemo
	NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán') #PostedDate
	NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ') #RefDate
	SO_CHUNG_TU = fields.Char(string='Số chứng từ') #RefNo
	LOAI_TIEN = fields.Char(string='Loại tiền') #CurrencyID
	TY_GIA = fields.Monetary(string='Tỷ giá', currency_field='currency_id') #ExchangeRate

	TONG_TIEN = fields.Monetary(string='Tổng tiền', currency_field='currency_id') #TotalAmountOC
	TONG_TIEN_QUY_DOI = fields.Float(string='Tổng tiền quy đổi',digits=decimal_precision.get_precision('VND')) #TotalAmount
	TONG_TIEN_CHIET_KHAU = fields.Monetary(string='Tổng tiền chiết khấu', currency_field='currency_id') #TotalDiscountAmountOC
	TONG_TIEN_CHIET_KHAU_QD = fields.Float(string='Tổng tiền chiết khấu quy đổi',digits=decimal_precision.get_precision('VND')) #TotalDiscountAmount
	TONG_TIEN_THUE = fields.Monetary(string='Tổng tiền thuế', currency_field='currency_id') #TotalVATAmountOC
	TONG_TIEN_THUE_QD = fields.Float(string='Tổng tiền thuế quy đổi',digits=decimal_precision.get_precision('VND')) #TotalVATAmount
	
	TINH_CHAT = fields.Char(string='Tính chất') #InventoryItemType
	TEN_DIEU_KHOAN_THANH_TOAN = fields.Char(string='Tên điều khoản thanh toán') #PaymentTermName

	TK_NO = fields.Char(string='TK Nợ', help='Tài khoản nợ') #DebitAccount
	TK_CO = fields.Char(string='TK Có', help='Tài khoản có') #CreditAccount

	TONG_THANH_TIEN = fields.Monetary(string='Tổng tiền', currency_field='currency_id')

	TONG_THANH_TIEN_LA_KHUYEN_MAI =fields.Monetary(string='Tổng tiền', currency_field='currency_id')
	TONG_TIEN_CHIET_KHAU_LA_KHUYEN_MAI = fields.Monetary(string='Tổng tiền', currency_field='currency_id')
	TONG_TIEN_THUE_GTGT_LA_KHUYEN_MAI = fields.Monetary(string='Tổng tiền', currency_field='currency_id')
	MAX_THUE_SUAT = fields.Float(string='Thành tiền quy đổi',digits=decimal_precision.get_precision('VND')) #dVATRate
	TONG_TIEN_THANH_TOAN = fields.Monetary(string='Tổng tiền', currency_field='currency_id')
	TY_LE_CHIET_KHAU = fields.Monetary(string='Thành tiền quy đổi', help='Thành tiền quy đổi', currency_field='base_currency_id')
	CONG_TIEN_HANG_DA_TRU_CHIET_KHAU = fields.Monetary(string='Tổng tiền', currency_field='currency_id')
	
	
	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
	

	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
	base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh())

	ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.phieu.xuat.kho.ban.hang.a5.doc.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')



class BAO_CAO_PHIEU_XUAT_KHO_BAN_HANG_A5_DOC_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_outwardstockbysalevouchera5doc'

	@api.model
	def get_report_values(self, docids, data=None):
		############### START SQL lấy dữ liệu ###############
		refTypeList, records = self.get_reftype_list(data)
		env = self.env['report.bao_cao.template_outwardstockbysalevoucher']
		sql_result = env.ham_lay_du_lieu_sql_tra_ve(refTypeList)
		dic_tk_no  = {}
		dic_tk_co  = {}

		for line in sql_result:
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))

			if key not in dic_tk_no:
				dic_tk_no[key] = []
			if key not in dic_tk_co:
				dic_tk_co[key] = []

			if line.get('TK_NO') and line.get('TK_NO') not in dic_tk_no[key]:
				dic_tk_no[key] += [line.get('TK_NO')]

			if line.get('TK_CO') and line.get('TK_CO') not in dic_tk_co[key]:
				dic_tk_co[key] += [line.get('TK_CO')]
				
			master_data = self.env['bao.cao.phieu.xuat.kho.ban.hang.a5.doc'].convert_for_update(line)
			detail_data = self.env['bao.cao.phieu.xuat.kho.ban.hang.a5.doc.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
				records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.phieu.xuat.kho.ban.hang.a5.doc.chi.tiet'].new(detail_data)
		
		for key in records:
			if key in dic_tk_no:
				records[key].TK_NO = ', '.join(dic_tk_no[key])
			if key in dic_tk_co:
				records[key].TK_CO = ', '.join(dic_tk_co[key])

		docs = [records.get(k) for k in records]

		for record in docs:
			if not record.LOAI_TIEN:
				record.currency_id = self.lay_loai_tien_mac_dinh()
				record.base_currency_id = self.lay_loai_tien_mac_dinh()
			else:
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', record.LOAI_TIEN)],limit=1)
				if loai_tien_id:
					record.currency_id = loai_tien_id.id
					record.base_currency_id = loai_tien_id.id

			tong_thanh_tien = 0 
			tong_thanh_tien_la_khuyen_mai = 0
			tong_tien_chiet_khau_la_khuyen_mai = 0
			tong_tien_thue_gtgt_la_khuyen_mai = 0
			thue_suat_max = 0 
			for line in record.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
				tong_thanh_tien += line.THANH_TIEN 
				line.currency_id = record.currency_id
				if line.LA_HANG_KHUYEN_MAI == 0:
					tong_thanh_tien_la_khuyen_mai += line.THANH_TIEN
					tong_tien_chiet_khau_la_khuyen_mai += line.TIEN_CHIET_KHAU
					tong_tien_thue_gtgt_la_khuyen_mai += line.TIEN_THUE_GTGT
				if line.THUE_SUAT > thue_suat_max:
					thue_suat_max = line.THUE_SUAT

			record.TONG_THANH_TIEN = tong_thanh_tien

			record.TONG_THANH_TIEN_LA_KHUYEN_MAI = tong_thanh_tien_la_khuyen_mai
			record.TONG_TIEN_CHIET_KHAU_LA_KHUYEN_MAI = tong_tien_chiet_khau_la_khuyen_mai
			record.MAX_THUE_SUAT = thue_suat_max * 100
			record.TONG_TIEN_THUE_GTGT_LA_KHUYEN_MAI = tong_tien_thue_gtgt_la_khuyen_mai

			record.TONG_TIEN_THANH_TOAN = record.TONG_THANH_TIEN_LA_KHUYEN_MAI + record.TONG_TIEN_THUE_GTGT_LA_KHUYEN_MAI - record.TONG_TIEN_CHIET_KHAU_LA_KHUYEN_MAI
			if record.TONG_THANH_TIEN_LA_KHUYEN_MAI != 0:
				record.TY_LE_CHIET_KHAU = float_round( (record.TONG_TIEN_CHIET_KHAU_LA_KHUYEN_MAI / record.TONG_THANH_TIEN_LA_KHUYEN_MAI ) * 100 , 2)
			
			record.CONG_TIEN_HANG_DA_TRU_CHIET_KHAU = record.TONG_THANH_TIEN_LA_KHUYEN_MAI - record.TONG_TIEN_CHIET_KHAU_LA_KHUYEN_MAI
			

		return {
			'docs': docs,
		}
