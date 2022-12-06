# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET(models.Model):
	_name = 'gia.thanh.ket.qua.phan.bo.chi.tiet'
	_description = ''
	
	MA_DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Mã đối tượng THCP', help='Mã đối tượng tập hợp chi phí')
	TEN_DOI_TUONG_THCP = fields.Char(string='Tên đối tượng THCP', help='Tên đối tượng tập hợp chi phí')
	LOAI_DOI_TUONG_THCP = fields.Selection([('0', 'Phân xưởng'), ('1', 'Sản phẩm'), ('2', 'Quy trình sản xuất'), ('3', 'Công đoạn'), ],string='Loại đối tượng THCP', help='Loại đối tượng tập hợp chi phí')

	MA_CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Mã công trình', help='Mã công trình')
	TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình')
	LOAI_CONG_TRINH = fields.Many2one('danh.muc.loai.cong.trinh', string='Loại công trình', help='Loại công trình') 

	SO_DON_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Số đơn hàng', help='Số đơn hàng')
	NGAY_DON_HANG = fields.Date(string='Ngày đơn hàng', help='Ngày đơn hàng')
	KHACH_HANG = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng')

	HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng', help='Hợp đồng bán')    
	NGAY_KY = fields.Date(string='Ngày ký', help='Ngày ký')
	TRICH_YEU = fields.Char(string='Trích yếu', help='Trích yếu')



	TY_LE_PHAN_TRAM_621 = fields.Float(string='Tỷ lệ (%)', help='Tỷ lệ phần trăm')
	SO_TIEN_621 = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('VND'))
	TY_LE_PHAN_TRAM_622 = fields.Float(string='Tỷ lệ (%)', help='Tỷ lệ phần trăm',digits=decimal_precision.get_precision('TY_LE_PHAN_BO'))
	SO_TIEN_622 = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('VND'))
	TY_LE_PHAN_TRAM_6271 = fields.Float(string='Tỷ lệ (%)', help='Tỷ lệ phần trăm',digits=decimal_precision.get_precision('TY_LE_PHAN_BO'))
	SO_TIEN_6271 = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('VND'))

	TY_LE_PHAN_TRAM_6272 = fields.Float(string='Tỷ lệ (%)', help='Tỷ lệ phần trăm',digits=decimal_precision.get_precision('TY_LE_PHAN_BO'))
	SO_TIEN_6272 = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('VND'))
	TY_LE_PHAN_TRAM_6273 = fields.Float(string='Tỷ lệ (%)', help='Tỷ lệ phần trăm',digits=decimal_precision.get_precision('TY_LE_PHAN_BO'))
	SO_TIEN_6273 = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('VND'))
	TY_LE_PHAN_TRAM_6274 = fields.Float(string='Tỷ lệ (%)', help='Tỷ lệ phần trăm',digits=decimal_precision.get_precision('TY_LE_PHAN_BO'))
	SO_TIEN_6274 = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('VND'))
 
	TY_LE_PHAN_TRAM_6277 = fields.Float(string='Tỷ lệ (%)', help='Tỷ lệ phần trăm',digits=decimal_precision.get_precision('TY_LE_PHAN_BO'))
	SO_TIEN_6277 = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('VND'))
	TY_LE_PHAN_TRAM_6278 = fields.Float(string='Tỷ lệ (%)', help='Tỷ lệ phần trăm',digits=decimal_precision.get_precision('TY_LE_PHAN_BO'))
	SO_TIEN_6278 = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('VND'))
	TONG_CHI_PHI = fields.Float(string='Tổng chi phí', help='Tổng chi phí',compute='tinh_tong_chi_phi',store=True,digits=decimal_precision.get_precision('VND'))
	CHI_TIET_ID = fields.Many2one('gia.thanh.tinh.gia.thanh', string='Chi tiết', help='Chi tiết', ondelete='cascade')
	PHAN_BO_CHI_PHI_CHUNG_CHI_TIET_ID = fields.Many2one('gia.thanh.phan.bo.chi.phi.chung', string='Phân bổ chi phí chung chi tiết', help='Phân bổ chi phí chung chi tiết')
	KY_TINH_GIA_THANH_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh', string='Chi tiết', help='Chi tiết', ondelete='cascade')
	name = fields.Char(string='Name', help='Name', oldname='NAME')

	

	@api.onuichange('TY_LE_PHAN_TRAM_6271')
	def update_so_tien_6271(self):
		for record in self:
			if (record.CHI_TIET_ID.TONG_SO_DA_PHAN_BO_TK6271>0):
				so_tien = (record.TY_LE_PHAN_TRAM_6271 * record.CHI_TIET_ID.TONG_SO_DA_PHAN_BO_TK6271) / 100
				record.SO_TIEN_6271 = so_tien

	@api.onuichange('SO_TIEN_6271')
	def update_ty_le_phan_tram_6271(self):
		for record in self:
			if (record.CHI_TIET_ID.TONG_SO_DA_PHAN_BO_TK6271>0):
				ty_le_phan_tram = (record.SO_TIEN_6271 / record.CHI_TIET_ID.TONG_SO_DA_PHAN_BO_TK6271) * 100
				record.TY_LE_PHAN_TRAM_6271 = ty_le_phan_tram

	@api.onuichange('TY_LE_PHAN_TRAM_621')
	def update_so_tien_621(self):
		for record in self:
			if (record.CHI_TIET_ID.TONG_SO_DA_PHAN_BO_TK621>0):
				so_tien = (record.TY_LE_PHAN_TRAM_621 * record.CHI_TIET_ID.TONG_SO_DA_PHAN_BO_TK621) / 100
				record.SO_TIEN_621 = so_tien

	@api.onuichange('SO_TIEN_621')
	def update_ty_le_phan_tram_621(self):
		for record in self:
			if (record.CHI_TIET_ID.TONG_SO_DA_PHAN_BO_TK621>0):
				ty_le_phan_tram = (record.SO_TIEN_621 / record.CHI_TIET_ID.TONG_SO_DA_PHAN_BO_TK621) * 100
				record.TY_LE_PHAN_TRAM_621 = ty_le_phan_tram

	@api.onuichange('TY_LE_PHAN_TRAM_6277')
	def update_so_tien_6277(self):
		for record in self:
			if (record.CHI_TIET_ID.TONG_SO_DA_PHAN_BO_TK6277>0):
				so_tien = (record.TY_LE_PHAN_TRAM_6277 * record.CHI_TIET_ID.TONG_SO_DA_PHAN_BO_TK6277) / 100
				record.SO_TIEN_6277 = so_tien

	@api.onuichange('SO_TIEN_6277')
	def update_ty_le_phan_tram_6277(self):
		for record in self:
			if (record.CHI_TIET_ID.TONG_SO_DA_PHAN_BO_TK6277>0):
				ty_le_phan_tram = (record.SO_TIEN_6277 / record.CHI_TIET_ID.TONG_SO_DA_PHAN_BO_TK6277) * 100
				record.TY_LE_PHAN_TRAM_6277 = ty_le_phan_tram

	@api.depends('SO_TIEN_6271','SO_TIEN_621','SO_TIEN_6277')
	def tinh_tong_chi_phi(self):
		for line in self:
			line.TONG_CHI_PHI = line.SO_TIEN_621 + line.SO_TIEN_622 + line.SO_TIEN_6271 + line.SO_TIEN_6272 + line.SO_TIEN_6273 + line.SO_TIEN_6274 + line.SO_TIEN_6277 + line.SO_TIEN_6278
			
