# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision

class DANH_MUC_VAT_TU_HANG_HOA(models.Model):
	_inherit = 'danh.muc.vat.tu.hang.hoa'
	
	DUA_TREN_CACH_TINH = fields.Selection(selection_add=[('DIEN_TICH_HCN_TU_MM', 'Diện tích hình chữ nhật từ Mi-li-mét') ])
	THIET_LAP_CONG_THUC = fields.Char(string='Thiết lập công thức', help='Thiết lập công thức', compute='_compute_thiet_lap_cong_thuc' ,store=True)

	@api.depends('DUA_TREN_CACH_TINH')
	def _compute_thiet_lap_cong_thuc(self):
		for record in self:
			if record.DUA_TREN_CACH_TINH =='DIEN_TICH_HCN_TU_MM':
				record.THIET_LAP_CONG_THUC = '[Chiều dài]*[Chiều rộng]*[Lượng]*0.000001'
			else:
				super(DANH_MUC_VAT_TU_HANG_HOA, record)._compute_thiet_lap_cong_thuc()

	def tinh_so_luong_theo_cong_thuc(self, CHIEU_DAI, CHIEU_RONG, CHIEU_CAO, BAN_KINH, LUONG):
		self.ensure_one()
		so_luong = 0
		if self.TINH_CHAT in ('0','1'):
			if self.DUA_TREN_CACH_TINH =='DIEN_TICH_HCN_TU_MM':
				so_luong = CHIEU_DAI * CHIEU_RONG * LUONG * 0.000001
			else:
				so_luong = super(DANH_MUC_VAT_TU_HANG_HOA, self).tinh_so_luong_theo_cong_thuc(CHIEU_DAI, CHIEU_RONG, CHIEU_CAO, BAN_KINH, LUONG)

		return so_luong

	def lay_so_luong_ton_tat_ca_kho(self, balance_date, IN_ref_order,branch_id):
		so_luong_ton = super(DANH_MUC_VAT_TU_HANG_HOA, self).lay_so_luong_ton_tat_ca_kho(balance_date, IN_ref_order,branch_id)
		query = """
			SELECT ddhct."MA_HANG_ID", SUM(ddhct."SO_LUONG") as so_da_dat_hang
			FROM account_ex_don_dat_hang ddh
			INNER JOIN account_ex_don_dat_hang_chi_tiet ddhct
				ON ddh.id = ddhct."DON_DAT_HANG_CHI_TIET_ID"
			WHERE ddhct."MA_HANG_ID" = %s
				AND ddh."NGAY_DON_HANG" <= '%s'
				-- TINH_TRANG" == '3': Đã hủy
				AND ddh."TINH_TRANG" != '3'
				AND (ddh."CHUNG_TU_BAN_HANG_ID" ISNULL
					OR NOT EXISTS(
					SELECT id FROM sale_document as sale
					WHERE sale.id =  ddh."CHUNG_TU_BAN_HANG_ID"
					AND sale.state = 'da_ghi_so'
					LIMIT 1
					)) 
			GROUP BY ddhct."MA_HANG_ID"
		""" % (self.id, balance_date)
		result = self.execute(query)
		if result:
			so_luong_ton -= result[0].get('so_da_dat_hang',0)
		return so_luong_ton