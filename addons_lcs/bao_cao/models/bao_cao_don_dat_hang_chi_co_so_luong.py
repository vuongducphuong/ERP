# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round
from datetime import timedelta, datetime

class BAO_CAO_DON_DAT_HANG_CHI_CO_SO_LUONG(models.Model):
	_name = 'bao.cao.don.dat.hang.chi.co.so.luong'
	_auto = False

	ref = fields.Char(string='Reffence ID')

	ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
	MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')

	TEN_KHACH_HANG = fields.Char(string='Tên khách hàng') #AccountObjectName
	MA_KHACH_HANG = fields.Char(string='Tên ngân hàng')#AccountObjectCode
	DIA_CHI = fields.Char(string='Địa chỉ') #AccountObjectAddress
	MA_SO_THUE = fields.Char(string='Địa chỉ') #AccountObjectTaxCode
	MA_NHAN_VIEN = fields.Char(string='Địa chỉ') #EmployeeCode
	TEN_NHAN_VIEN_BAN_HANG = fields.Char(string='Địa chỉ') #EmployeeName
	NGAY_DON_HANG = fields.Char(string='Địa chỉ') #RefDate
	DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải') #JournalMemo
	SO_DON_HANG = fields.Char(string='Diễn giải', help='Diễn giải') #RefNo
	LOAI_TIEN = fields.Char(string='Loại tiền') #CurrencyID
	TY_GIA = fields.Monetary(string='Tỷ giá', currency_field='currency_id') #ExchangeRate
	TONG_TIEN_QUY_DOI = fields.Float(string='Tổng tiền quy đổi',digits=decimal_precision.get_precision('VND')) #TotalAmount
	NGAY_GIAO_HANG = fields.Date(string='Ngày chứng từ') #DeliveryDate
	DIA_DIEM_GIAO_HANG = fields.Char(string='Loại tiền') #ShippingAddress
	DIEU_KHOAN_KHAC = fields.Char(string='Loại tiền') #OtherTerm
	TEN_DIEU_KHOAN = fields.Char(string='Loại tiền') #PaymentTermName
	SO_DIEN_THOAI = fields.Char(string='Loại tiền') #Tel
	FAX = fields.Char(string='Loại tiền') #Fax

	SO_TIEN_CHIET_KHAU = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalDiscount
	TONG_THANH_TIEN = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalAmount
	THUE_SUAT_GTGT = fields.Float(string='Số tiền chiết khấu',digits=decimal_precision.get_precision('VND')) #dVATRate
	TIEN_THUE_GTGT = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalVAT
	CONG_TIEN_HANG = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalAmount - dTotalDiscount

	TY_LE_CHIET_KHAU = fields.Float(string='Tỷ lệ chiết khấu') #dTotalDiscount / dTotalAmount

	TONG_TIEN_THANH_TOAN = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalAmount+dTotalVAT-dTotalDiscount
	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())


	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())

	ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.don.dat.hang.chi.co.so.luong.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')



class BAO_CAO_DON_DAT_HANG_CHI_CO_SO_LUONG_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_saordervoucher3520quanity'

	@api.model
	def get_report_values(self, docids, data=None):
		############### START SQL lấy dữ liệu ###############
		refTypeList, records = self.get_reftype_list(data)
		env = self.env['report.bao_cao.template_saordervoucher3520']
		sql_result = env.ham_lay_du_lieu_sql_tra_ve(refTypeList)

		for line in sql_result:
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
			master_data = self.env['bao.cao.don.dat.hang.chi.co.so.luong'].convert_for_update(line)
			detail_data = self.env['bao.cao.don.dat.hang.chi.co.so.luong.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
				records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.don.dat.hang.chi.co.so.luong.chi.tiet'].new(detail_data)
		
		docs = [records.get(k) for k in records]

		for record in docs:
			if not record.LOAI_TIEN:
				record.currency_id = self.lay_loai_tien_mac_dinh()
			else:
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', record.LOAI_TIEN)],limit=1)
				if loai_tien_id:
					record.currency_id = loai_tien_id.id

			if record.NGAY_DON_HANG:
				record.NGAY_DON_HANG = 	datetime.strptime(record.NGAY_DON_HANG,'%Y-%m-%d').date().strftime('%d/%m/%Y')

		return {
			'docs': docs,
        }

	
