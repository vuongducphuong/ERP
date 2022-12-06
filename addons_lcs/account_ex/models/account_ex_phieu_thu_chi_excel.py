# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError , UserError
from odoo.addons import decimal_precision

class ACCOUNT_EX_PHIEU_THU_CHI_EXCEL(models.Model):
	_name = 'account.ex.phieu.thu.chi.excel'
	_description = 'Quỹ phiếu thu chi'
	_auto = False


	# Các trường dùng chung
	NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán (*)')
	NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ (*)')
	SO_CHUNG_TU = fields.Char(string='Số chứng từ (*)')
	MA_DOI_TUONG = fields.Char(string='Mã đối tượng')
	TEN_DOI_TUONG = fields.Char(string='Tên đối tượng')
	DIA_CHI = fields.Char(string='Địa chỉ')
	KEM_THEO = fields.Char(string='Kèm theo')
	LOAI_TIEN = fields.Char(string='Loại tiền')
	TY_GIA = fields.Float(string='Tỷ giá', default=1)

	# Các trường từ file import exel Quỹ phiếu thu
	LY_DO_NOP = fields.Selection([('10', 'Rút tiền gửi về nộp quỹ'), ('11', ' Thu hoàn thuế GTGT'), ('12', ' Thu hoàn ứng'), ('13', 'Thu khác'), ], string='Lý do nộp', default = '13')
	DIEN_GIAI_LY_DO_NOP = fields.Char(string='Diễn giải lý do nộp')
	NGUOI_NOP = fields.Char(string='Người nộp')
	NHAN_VIEN_THU = fields.Char(string='Nhân viên thu')

	# Các trường từ file import exel Ngân hàng phiếu thu
	NOP_VAO_TAI_KHOAN = fields.Char(string='Nộp vào TK', help='Nộp vào TK')
	MO_TAI_NGAN_HANG = fields.Char(string='Mở tại NH', help='Mở tại NH')
	LY_DO_THU = fields.Selection([('30', 'Vay nợ'), ('31', ' Thu lãi đầu tư tài chính'), ('32', ' Thu hoàn ứng'), ('33', 'Thu hoàn thuế GTGT'), ('34', 'Thu khác'), ],string='Lý do thu', default = '34')
	DIEN_GIAI_LY_DO_THU = fields.Char(string='Diễn giải lý do thu', help='Diễn giải lý do thu')

	# Ngân hàng phiếu chi
	PHUONG_THUC_THANH_TOAN = fields.Selection([('0', 'Ủy nhiệm chi'), ('1', 'Séc chuyển khoản'), ('2', 'Séc tiền mặt'),],string='Phương thức thanh toán', default = '0')
	TAI_KHOAN_CHI = fields.Char(string='Tài khoản chi', help='Tài khoản chi')
	NOI_DUNG_THANH_TOAN = fields.Selection([('40', 'Trả các khoản vay'), ('42', 'Tạm ứng cho nhân viên'), ('43', 'Chi khác'),],string='Nội dung thanh toán', default = '43')
	DIEN_GIAI_NOI_DUNG_THANH_TOAN = fields.Char(string='Diễn giải nội dung thanh toán', help='Diễn giải nội dung thanh toán')
	TAI_KHOAN_NHAN = fields.Char(string='Tài khoản nhận', help='Tài khoản nhận')
	TAI_NGAN_HANG_NHAN = fields.Char(string='Tên NH nhận', help='Tên NH nhận')
	NGUOI_LINH_TIEN = fields.Char(string='Người lĩnh tiền', help='Người lĩnh tiền')

	# Các trường bổ sung cho Ngân hàng Chuyển tiền nội bộ
	TAI_KHOAN_DI = fields.Char(string='Tài khoản đi (*)', help='Tài khoản đi (*)')
	TEN_TAI_KHOAN_DI = fields.Char(string='Tên tài khoản đi', help='Tên tài khoản đi')
	TAI_KHOAN_DEN = fields.Char(string='Tài khoản đến (*)', help='Tài khoản đến (*)')
	TEN_TAI_KHOAN_DEN = fields.Char(string='Tên tài khoản đến', help='Tên tài khoản đến')
	LY_DO_CHUYEN = fields.Char(string='Lý do chuyển', help='Lý do chuyển')


	# Các trường phần chi tiết Hạch toán dùng chung
	DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
	TK_NO = fields.Char(string='TK Nợ (*)', help='TK Nợ (*)')
	TK_CO = fields.Char(string='TK Có (*)', help='TK Có (*)')
	SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
	SO_TIEN_QUY_DOI = fields.Float(string='Số tiền quy đổi', help='Số tiền quy đổi')
	QUY_DOI = fields.Float(string='Quy đổi', help='Quy đổi')
	DOI_TUONG = fields.Char(string='Đối tượng', help='Đối tượng')

	DON_VI = fields.Char(string='Đơn vị', help='Đơn vị')
	CONG_TRINH = fields.Char(string='Công trình', help='Công trình')
	DON_DAT_HANG = fields.Char(string='Đơn đặt hàng', help='Đơn đặt hàng')
	HOP_DONG_MUA = fields.Char(string='Hợp đồng mua', help='Hợp đồng mua')
	HOP_DONG_BAN = fields.Char(string='Hợp đồng bán', help='Hợp đồng bán')
	MA_THONG_KE = fields.Char(string='Mã thống kê', help='Mã thống kê')
	TK_NGAN_HANG = fields.Char(string='TK ngân hàng', help='TK ngân hàng')

	KHOAN_MUC_CHI_PHI = fields.Char(string='Khoản mục chi phí', help='Khoản mục chi phí')
	DOI_TUONG_TAP_HOP_CHI_PHI = fields.Char(string='ĐT tập hợp chi phí', help='ĐT tập hợp chi phí')

	# Các trường từ file import exel Quỹ phiếu chi
	NHAN_VIEN = fields.Char(string='Nhân viên', help='Nhân viên')
	LY_DO_CHI = fields.Selection([('21', 'Tạm ứng nhân viên'), ('22', ' Gửi tiền vào ngân hàng'), ('23', 'Chi khác'),],string='Lý do chi', default = '23')
	DIEN_GIAI_LY_DO_CHI = fields.Char(string='Diễn giải lý do chi', help='Diễn giải lý do chi')
	NGUOI_NHAN = fields.Char(string='Người nhận', help='Người nhận')

	# Các trường phần chi tiết thuế
	DIEN_GIAI_THUE = fields.Char(string='Diễn giải (Thuế)', help='Diễn giải (Thuế)')
	TK_THUE_GTGT = fields.Char(string='TK thuế GTGT', help='TK thuế GTGT')
	TIEN_THUE_GTGT = fields.Float(string='Tiền thuế GTGT', help='Tiền thuế GTGT')
	PHAN_TRAM_THUE_GTGT = fields.Char(string='% thuế GTGT', help='% thuế GTGT')
	HHDV_CHUA_THUE = fields.Float(string='Giá trị HHDV chưa thuế', help='Giá trị HHDV chưa thuế')
	MAU_SO_HOA_DON = fields.Char(string='Mẫu số hóa đơn', help='Mẫu số hóa đơn')
	KY_HIEU_HOA_DON = fields.Char(string='Ký hiệu hóa đơn', help='Ký hiệu hóa đơn')
	NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
	SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
	
	NHOM_HHDV_MUA_VAO = fields.Char(string='Nhóm HHDV mua vào', help='Nhóm HHDV mua vào')
	MA_NHA_CUNG_CAP = fields.Char(string='Mã nhà cung cấp', help='Mã nhà cung cấp')
	TEN_NHA_CUNG_CAP = fields.Char(string='Tên nhà cung cấp', help='Tên nhà cung cấp')
	MA_SO_THUE_NHA_CUNG_CAP = fields.Char(string='Mã số thuế nhà cung cấp', help='Mã số thuế nhà cung cấp')


	def import_from_excel(self, import_fields, data):
		default_LOAI_PHIEU = self._context.get('default_LOAI_PHIEU')
		default_TYPE_NH_Q = self._context.get('default_TYPE_NH_Q')
		result = None
		if default_TYPE_NH_Q == 'NGAN_HANG':
			if default_LOAI_PHIEU == 'PHIEU_THU':
				result = self.import_from_excel_ngan_hang_phieu_thu(import_fields, data)
			elif default_LOAI_PHIEU == 'PHIEU_CHI':
				result = self.import_from_excel_ngan_hang_phieu_chi(import_fields, data)
			elif default_LOAI_PHIEU == 'PHIEU_CHUYEN_TIEN':
				result = self.import_from_excel_ngan_hang_phieu_chuyen_tien(import_fields, data)
		elif default_TYPE_NH_Q == 'QUY':
			if default_LOAI_PHIEU == 'PHIEU_THU':
				result = self.import_from_excel_quy_phieu_thu(import_fields, data)
			elif default_LOAI_PHIEU == 'PHIEU_CHI':
				result = self.import_from_excel_quy_phieu_chi(import_fields, data)
		return result

	# Hàm import cho Quỹ phiếu thu
	def import_from_excel_quy_phieu_thu(self, import_fields, data):
		dict = {}
		error = []
		line_number = 1
		for item in data:
			d = self.get_formatted_data(import_fields, item, error, line_number)
			####### Validate ########
						
			if not d.get('NGAY_HACH_TOAN'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Ngày hạch toán>  bắt buộc nhập' % (line_number,)})
			elif not d.get('NGAY_CHUNG_TU'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Ngày chứng từ>  bắt buộc nhập' % (line_number,)})
			elif not d.get('SO_CHUNG_TU'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Số chứng từ>  bắt buộc nhập' % (line_number,)})
			elif not d.get('TK_NO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK Nợ>  bắt buộc nhập' % (line_number,)})
			elif not d.get('TK_CO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK Có>  bắt buộc nhập' % (line_number,)})
			
			doi_tuong_id = None
			nv_thu_id = None
			loai_tien_id = None
			tk_co_id = None
			tk_no_id = None
			doi_tuong_chi_tiet_id = None
			tk_ngan_hang_id = None
			
			if d.get('MA_DOI_TUONG'):
				doi_tuong_id = self.env['res.partner'].search([('MA', '=', d.get('MA_DOI_TUONG'))], limit=1)
				if not doi_tuong_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã đối tượng <%s> trong danh mục nhà cung cấp' % (line_number,d.get('MA_DOI_TUONG'))})

			if d.get('NHAN_VIEN_THU'):
				nv_thu_id = self.env['res.partner'].search([('MA', '=', d.get('NHAN_VIEN_THU'))], limit=1)
				if not nv_thu_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy NV thu <%s> trong danh mục nhân viên' % (line_number,d.get('NHAN_VIEN_THU'))})

			if d.get('LOAI_TIEN'):
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', d.get('LOAI_TIEN'))], limit=1)
				if not loai_tien_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Loại tiền <%s> trong danh mục loại tiền' % (line_number,d.get('LOAI_TIEN'))})
			
			if d.get('TK_CO'):
				tk_co_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_CO'))], limit=1)
				if not tk_co_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK có <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_CO'))})
			
			if d.get('TK_NO'):
				tk_no_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_NO'))], limit=1)
				if not tk_no_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK nợ <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_NO'))})
			
			if d.get('DOI_TUONG'):
				doi_tuong_chi_tiet_id = self.env['res.partner'].search([('MA', '=', d.get('DOI_TUONG'))], limit=1)
				if not doi_tuong_chi_tiet_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã đối tượng <%s> trong danh mục đối tượng' % (line_number,d.get('DOI_TUONG'))})


			if d.get('TK_NGAN_HANG'):
				tk_ngan_hang_id = self.env['danh.muc.tai.khoan.ngan.hang'].search([('SO_TAI_KHOAN', '=', d.get('TK_NGAN_HANG'))], limit=1)
				if not tk_ngan_hang_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy số tài khoản <%s> trong danh mục tài khoản ngân hàng' % (line_number,d.get('TK_NGAN_HANG'))}) 
			
			ly_do_nop =''
			if d.get('LY_DO_NOP') == '10':
				ly_do_nop = '10'
			elif d.get('LY_DO_NOP') == '11':
				ly_do_nop = '11'
			elif d.get('LY_DO_NOP') == '12':
				ly_do_nop = '12'
			else:
				ly_do_nop = '13'

			

			key = '_'.join([str(d.get('NGAY_HACH_TOAN')) + str(d.get('SO_CHUNG_TU'))]) # d[0]: Loại nghiệp vụ - d[1]: Số chứng từ
			if key not in dict:
				dict[key] = {
					
					'NGAY_HACH_TOAN': d.get('NGAY_HACH_TOAN'),
					'NGAY_CHUNG_TU': d.get('NGAY_CHUNG_TU'),
					'SO_CHUNG_TU': d.get('SO_CHUNG_TU'),
					
					'DOI_TUONG_ID': doi_tuong_id.id if doi_tuong_id else None,
					'TEN_DOI_TUONG': d.get('TEN_DOI_TUONG'),
					'DIA_CHI': d.get('DIA_CHI'),
					'NGUOI_NOP': d.get('NGUOI_NOP'),
					'LY_DO_NOP': ly_do_nop,
					'DIEN_GIAI': d.get('DIEN_GIAI_LY_DO_NOP'),
					'NHAN_VIEN_ID': nv_thu_id.id if nv_thu_id else None,
					'KEM_THEO_CHUNG_TU_GOC':  d.get('KEM_THEO'),

					'currency_id': loai_tien_id.id if loai_tien_id else None,
					'TY_GIA': d.get('TY_GIA'),
					'ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS': []
				}
			dict[key]['ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS'] += [[0,0,{
				
				'DIEN_GIAI_DETAIL': d.get('DIEN_GIAI'),
				'TK_NO_ID': tk_no_id.id if tk_no_id else None,
				'TK_CO_ID': tk_co_id.id if tk_co_id else None,
				'SO_TIEN': d.get('SO_TIEN'),
				'SO_TIEN_QUY_DOI': d.get('SO_TIEN') * d.get('TY_GIA'),
				'DOI_TUONG_ID': doi_tuong_chi_tiet_id.id if doi_tuong_chi_tiet_id else None,
				'TK_NGAN_HANG_ID': tk_ngan_hang_id.id if tk_ngan_hang_id else None,
				
			}]]
			line_number += 1
		if not error:
			for key in dict:
				new_dict = dict.get(key)
				new_dict['LOAI_CHUNG_TU'] = 1010
				new_dict['NHOM_CHUNG_TU'] = int(new_dict.get('LY_DO_NOP',0))
				self.env['account.ex.phieu.thu.chi'].create(new_dict)
			return {}

		return {'messages' : error}

	# Hàm import cho Quỹ phiếu chi
	def import_from_excel_quy_phieu_chi(self, import_fields, data):
		dict = {}
		error = []
		line_number = 1
		for item in data:
			d = self.get_formatted_data(import_fields, item, error, line_number)
			####### Validate ########
						
			if not d.get('NGAY_HACH_TOAN'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Ngày hạch toán>  bắt buộc nhập' % (line_number,)})
			elif not d.get('NGAY_CHUNG_TU'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Ngày chứng từ>  bắt buộc nhập' % (line_number,)})
			elif not d.get('SO_CHUNG_TU'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Số chứng từ>  bắt buộc nhập' % (line_number,)})
			elif not d.get('TK_NO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK Nợ>  bắt buộc nhập' % (line_number,)})
			elif not d.get('TK_CO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK Có>  bắt buộc nhập' % (line_number,)})
			

			doi_tuong_id = None
			nv_chi_id = None
			loai_tien_id = None
			
			tk_co_id = None
			tk_no_id = None
			doi_tuong_chi_tiet_id = None

			tk_ngan_hang_id = None
			tk_thue_gtgt_id = None
			phan_tram_thue_gtgt_id = None
			nhom_hhdv_mua_vao_id = None
			nha_cung_cap_id = None

			
			if d.get('MA_DOI_TUONG'):
				doi_tuong_id = self.env['res.partner'].search([('MA', '=', d.get('MA_DOI_TUONG'))], limit=1)
				if not doi_tuong_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã đối tượng <%s> trong danh mục nhà cung cấp' % (line_number,d.get('MA_DOI_TUONG'))})

			if d.get('NHAN_VIEN'):
				nv_chi_id = self.env['res.partner'].search([('MA', '=', d.get('NHAN_VIEN'))], limit=1)
				if not nv_chi_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy nhân viên <%s> trong danh mục nhân viên' % (line_number,d.get('NHAN_VIEN'))})

			if d.get('LOAI_TIEN'):
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', d.get('LOAI_TIEN'))], limit=1)
				if not loai_tien_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Loại tiền <%s> trong danh mục loại tiền' % (line_number,d.get('LOAI_TIEN'))})
			
			if d.get('TK_CO'):
				tk_co_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_CO'))], limit=1)
				if not tk_co_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK có <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_CO'))})
			
			if d.get('TK_NO'):
				tk_no_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_NO'))], limit=1)
				if not tk_no_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK nợ <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_NO'))})
			
			if d.get('DOI_TUONG'):
				doi_tuong_chi_tiet_id = self.env['res.partner'].search([('MA', '=', d.get('DOI_TUONG'))], limit=1)
				if not doi_tuong_chi_tiet_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã đối tượng <%s> trong danh mục đối tượng' % (line_number,d.get('DOI_TUONG'))})

			if d.get('TK_NGAN_HANG'):
				tk_ngan_hang_id = self.env['danh.muc.tai.khoan.ngan.hang'].search([('SO_TAI_KHOAN', '=', d.get('TK_NGAN_HANG'))], limit=1)
				if not tk_ngan_hang_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy số tài khoản <%s> trong danh mục tài khoản ngân hàng' % (line_number,d.get('TK_NGAN_HANG'))}) 
			
			if d.get('TK_THUE_GTGT'):
				tk_thue_gtgt_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_THUE_GTGT'))], limit=1)
				if not tk_thue_gtgt_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK thuế GTGT <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_THUE_GTGT'))})
			
			if d.get('PHAN_TRAM_THUE_GTGT'):
				phan_tram_thue_gtgt_id = self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', d.get('PHAN_TRAM_THUE_GTGT'))], limit=1)
				if not phan_tram_thue_gtgt_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy phần trăm thuế GTGT <%s> trong danh mục thuế suất giá trị gia tăng' % (line_number,d.get('PHAN_TRAM_THUE_GTGT'))})
			
			if d.get('NHOM_HHDV_MUA_VAO'):
				nhom_hhdv_mua_vao_id = self.env['danh.muc.nhom.hhdv'].search([('MA_NHOM_HHDV', '=', d.get('NHOM_HHDV_MUA_VAO'))], limit=1)
				if not nhom_hhdv_mua_vao_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Nhóm HHDV mua vào <%s> trong danh mục nhóm hàng hóa dịch vụ mua vào' % (line_number,d.get('NHOM_HHDV_MUA_VAO'))})
			
			if d.get('MA_NHA_CUNG_CAP'):
				nha_cung_cap_id = self.env['res.partner'].search([('MA', '=', d.get('MA_NHA_CUNG_CAP'))], limit=1)
				if not nha_cung_cap_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã nhà cung cấp <%s> trong danh mục nhà cung cấp' % (line_number,d.get('MA_NHA_CUNG_CAP'))})

			ly_do_chi =''
			if d.get('LY_DO_CHI') == '21':
				ly_do_chi = 'TAM_UNG_CHO_NHAN_VIEN'
			elif d.get('LY_DO_CHI') == '22':
				ly_do_chi = 'GUI_TIEN_VAO_NGAN_HANG'
			else:
				ly_do_chi = 'CHI_KHAC'

			
			
			key = '_'.join([str(d.get('NGAY_HACH_TOAN')) + str(d.get('SO_CHUNG_TU'))]) # d[0]: Loại nghiệp vụ - d[1]: Số chứng từ
			if key not in dict:
				dict[key] = {
					
					'NGAY_HACH_TOAN': d.get('NGAY_HACH_TOAN'),
					'NGAY_CHUNG_TU': d.get('NGAY_CHUNG_TU'),
					'SO_CHUNG_TU': d.get('SO_CHUNG_TU'),
					
					'DOI_TUONG_ID': doi_tuong_id.id if doi_tuong_id else None,
					'TEN_DOI_TUONG': d.get('TEN_DOI_TUONG'),
					'DIA_CHI': d.get('DIA_CHI'),
					'NGUOI_NOP': d.get('NGUOI_NHAN'),
					'LY_DO_CHI': ly_do_chi,
					'DIEN_GIAI_PC': d.get('DIEN_GIAI_LY_DO_CHI'),
					'LY_DO_CHI_PC_NOP_TIEN': d.get('DIEN_GIAI_LY_DO_CHI'),
					'NHAN_VIEN_ID': nv_chi_id.id if nv_chi_id else None,
					'KEM_THEO_CHUNG_TU_GOC':  d.get('KEM_THEO'),


					'currency_id': loai_tien_id.id if loai_tien_id else None,
					'TY_GIA': d.get('TY_GIA'),
					'ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS': [],
					'ACCOUNT_EX_PHIEU_THU_CHI_THUE_IDS': []
				}

			dict[key]['ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS'] += [[0,0,{
				
				'DIEN_GIAI_DETAIL': d.get('DIEN_GIAI'),
				'TK_NO_ID': tk_no_id.id if tk_no_id else None,
				'TK_CO_ID': tk_co_id.id if tk_co_id else None,
				'SO_TIEN': d.get('SO_TIEN'),
				'SO_TIEN_QUY_DOI': d.get('SO_TIEN') * d.get('TY_GIA'),
				'DOI_TUONG_ID': doi_tuong_chi_tiet_id.id if doi_tuong_chi_tiet_id else None,
				'TK_NGAN_HANG_ID': tk_ngan_hang_id.id if tk_ngan_hang_id else None,
				
			}]]

			dict[key]['ACCOUNT_EX_PHIEU_THU_CHI_THUE_IDS'] += [[0,0,{
				
				'DIEN_GIAI_THUE': d.get('DIEN_GIAI_THUE'),
				'TK_THUE_GTGT_ID': tk_thue_gtgt_id.id if tk_thue_gtgt_id else None,
				'TIEN_THUE_GTGT': d.get('TIEN_THUE_GTGT'),
				'PHAN_TRAM_THUE_GTGT_ID': phan_tram_thue_gtgt_id.id if phan_tram_thue_gtgt_id else None,
				'GIA_TRI_HHDV_CHUA_THUE': d.get('HHDV_CHUA_THUE'),
				'NGAY_HOA_DON':  d.get('NGAY_HOA_DON'),
				'SO_HOA_DON': d.get('SO_HOA_DON'),
				'NHOM_HHDV_MUA_VAO': nhom_hhdv_mua_vao_id.id if nhom_hhdv_mua_vao_id else None,
				'DOI_TUONG_ID': nha_cung_cap_id.id if nha_cung_cap_id else None,
				'TEN_NCC': d.get('TEN_NHA_CUNG_CAP'),
				'MA_SO_THUE_NCC': d.get('MA_SO_THUE_NHA_CUNG_CAP'),
				
			}]]
			line_number += 1
		if not error:
			for key in dict:
				new_dict = dict.get(key)
				new_dict['LOAI_CHUNG_TU'] = 1020
				if new_dict.get('LY_DO_CHI') == 'TAM_UNG_CHO_NHAN_VIEN':
					new_dict['NHOM_CHUNG_TU'] = 21
				elif new_dict.get('LY_DO_CHI') =='GUI_TIEN_VAO_NGAN_HANG':
					new_dict['NHOM_CHUNG_TU'] = 22
				elif new_dict.get('LY_DO_CHI') =='CHI_KHAC':
					new_dict['NHOM_CHUNG_TU'] = 23
				self.env['account.ex.phieu.thu.chi'].create(new_dict)
			return {}

		return {'messages' : error}

	# Hàm import cho ngân hàng phiếu thu
	def import_from_excel_ngan_hang_phieu_thu(self, import_fields, data):
		dict = {}
		error = []
		line_number = 1
		for item in data:
			d = self.get_formatted_data(import_fields, item, error, line_number)
			####### Validate ########
						
			if not d.get('NGAY_HACH_TOAN'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Ngày hạch toán>  bắt buộc nhập' % (line_number,)})
			elif not d.get('NGAY_CHUNG_TU'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Ngày chứng từ>  bắt buộc nhập' % (line_number,)})
			elif not d.get('SO_CHUNG_TU'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Số chứng từ>  bắt buộc nhập' % (line_number,)})
			elif not d.get('TK_NO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK Nợ>  bắt buộc nhập' % (line_number,)})
			elif not d.get('TK_CO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK Có>  bắt buộc nhập' % (line_number,)})
			
			doi_tuong_id = None
			tk_ngan_hang_id = None
			loai_tien_id = None
			tk_co_id = None
			tk_no_id = None
			doi_tuong_chi_tiet_id = None
			don_vi_id = None
			cong_trinh_id = None
			don_dat_hang_id = None
			hop_dong_ban_id = None
			ma_thong_ke_id = None

			if d.get('MA_DOI_TUONG'):
				doi_tuong_id = self.env['res.partner'].search([('MA', '=', d.get('MA_DOI_TUONG'))], limit=1)
				if not doi_tuong_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã đối tượng <%s> trong danh mục nhà cung cấp' % (line_number,d.get('MA_DOI_TUONG'))})

			if d.get('NOP_VAO_TAI_KHOAN'):
				tk_ngan_hang_id = self.env['danh.muc.tai.khoan.ngan.hang'].search([('SO_TAI_KHOAN', '=', d.get('NOP_VAO_TAI_KHOAN'))], limit=1)
				if not tk_ngan_hang_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy số tài khoản <%s> trong danh mục tài khoản ngân hàng' % (line_number,d.get('NOP_VAO_TAI_KHOAN'))}) 
			
			
			if d.get('LOAI_TIEN'):
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', d.get('LOAI_TIEN'))], limit=1)
				if not loai_tien_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Loại tiền <%s> trong danh mục loại tiền' % (line_number,d.get('LOAI_TIEN'))})
			
			if d.get('TK_CO'):
				tk_co_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_CO'))], limit=1)
				if not tk_co_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK có <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_CO'))})
			
			if d.get('TK_NO'):
				tk_no_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_NO'))], limit=1)
				if not tk_no_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK nợ <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_NO'))})
			
			if d.get('DOI_TUONG'):
				doi_tuong_chi_tiet_id = self.env['res.partner'].search([('MA', '=', d.get('DOI_TUONG'))], limit=1)
				if not doi_tuong_chi_tiet_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã đối tượng <%s> trong danh mục đối tượng' % (line_number,d.get('DOI_TUONG'))})

			if d.get('CONG_TRINH'):
				cong_trinh_id = self.env['danh.muc.cong.trinh'].search([('MA_CONG_TRINH', '=', d.get('CONG_TRINH'))], limit=1)
				if not cong_trinh_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Công trình <%s> trong danh mục công trình' % (line_number,d.get('CONG_TRINH'))})
			
			if d.get('DON_VI'):
				don_vi_id = self.env['danh.muc.to.chuc'].search([('MA_DON_VI', '=', d.get('DON_VI'))], limit=1)
				if not don_vi_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Đơn vị <%s> trong danh mục cơ cấu tổ chức' % (line_number,d.get('DON_VI'))})
			
			if d.get('DON_DAT_HANG'):
				don_dat_hang_id = self.env['account.ex.don.dat.hang'].search([('SO_DON_HANG', '=', d.get('DON_DAT_HANG'))], limit=1)
				if not don_dat_hang_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Đơn đặt hàng <%s> trong Đơn đặt hàng' % (line_number,d.get('DON_DAT_HANG'))})

			if d.get('HOP_DONG_BAN'):
				hop_dong_ban_id = self.env['sale.ex.hop.dong.ban'].search([('SO_HOP_DONG', '=', d.get('HOP_DONG_BAN'))], limit=1)
				if not hop_dong_ban_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Hợp đồng bán <%s> trong Hợp đồng bán' % (line_number,d.get('HOP_DONG_BAN'))})

			if d.get('MA_THONG_KE'):
				ma_thong_ke_id = self.env['danh.muc.ma.thong.ke'].search([('MA_THONG_KE', '=', d.get('MA_THONG_KE'))], limit=1)
				if not ma_thong_ke_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã thống kê <%s> trong danh mục mã thống kê' % (line_number,d.get('MA_THONG_KE'))})

			ly_do_thu =''
			if d.get('LY_DO_THU') == '30':
				ly_do_thu = '30'
			elif d.get('LY_DO_THU') == '31':
				ly_do_thu = '31'
			elif d.get('LY_DO_THU') == '32':
				ly_do_thu = '32'
			elif d.get('LY_DO_THU') == '33':
				ly_do_thu = '33'
			else:
				ly_do_thu = '34'

			
			key = '_'.join([str(d.get('NGAY_HACH_TOAN')) + str(d.get('SO_CHUNG_TU'))]) # d[0]: Loại nghiệp vụ - d[1]: Số chứng từ
			if key not in dict:
				dict[key] = {
					'NGAY_HACH_TOAN': d.get('NGAY_HACH_TOAN'),
					'NGAY_CHUNG_TU': d.get('NGAY_CHUNG_TU'),
					'SO_CHUNG_TU': d.get('SO_CHUNG_TU'),
					
					'DOI_TUONG_ID': doi_tuong_id.id if doi_tuong_id else None,
					'TEN_DOI_TUONG': d.get('TEN_DOI_TUONG'),
					'DIA_CHI': d.get('DIA_CHI'),

					'TAI_KHOAN_NOP_ID': tk_ngan_hang_id.id if tk_ngan_hang_id else None,
					'TEN_TK_THU': d.get('MO_TAI_NGAN_HANG'),
					'ly_do_thu': ly_do_thu,
					'TEN_LY_DO_THU': d.get('DIEN_GIAI_LY_DO_THU'),
					# 'NHAN_VIEN_ID': nv_thu_id.id if nv_thu_id else None,
					
					'currency_id': loai_tien_id.id if loai_tien_id else None,
					'TY_GIA': d.get('TY_GIA'),
					'ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS': []
				}
			dict[key]['ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS'] += [[0,0,{
				
				'DIEN_GIAI_DETAIL': d.get('DIEN_GIAI'),
				'TK_NO_ID': tk_no_id.id if tk_no_id else None,
				'TK_CO_ID': tk_co_id.id if tk_co_id else None,
				'SO_TIEN': d.get('SO_TIEN'),
				'SO_TIEN_QUY_DOI': d.get('SO_TIEN') * d.get('TY_GIA'),
				'DOI_TUONG_ID': doi_tuong_chi_tiet_id.id if doi_tuong_chi_tiet_id else None,
				'DON_VI_ID': don_vi_id.id if don_vi_id else None,
				'CONG_TRINH_ID': cong_trinh_id.id if cong_trinh_id else None,
				'DON_DAT_HANG_ID': don_dat_hang_id.id if don_dat_hang_id else None,
				'HOP_DONG_BAN_ID': hop_dong_ban_id.id if hop_dong_ban_id else None,
				'MA_THONG_KE_ID': ma_thong_ke_id.id if ma_thong_ke_id else None,				
			}]]
			line_number += 1
		if not error:
			for key in dict:
				new_dict = dict.get(key)

				new_dict['LOAI_CHUNG_TU'] = 1500
				new_dict['NHOM_CHUNG_TU'] = int(new_dict.get('ly_do_thu',0))
				
				self.env['account.ex.phieu.thu.chi'].create(new_dict)
			return {}

		return {'messages' : error}

	# Hàm import exel cho Ngân hàng phiếu Chi
	def import_from_excel_ngan_hang_phieu_chi(self, import_fields, data):
		dict = {}
		error = []
		line_number = 1
		for item in data:
			d = self.get_formatted_data(import_fields, item, error, line_number)
			####### Validate ########
						
			if not d.get('NGAY_HACH_TOAN'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Ngày hạch toán>  bắt buộc nhập' % (line_number,)})
			elif not d.get('NGAY_CHUNG_TU'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Ngày chứng từ>  bắt buộc nhập' % (line_number,)})
			elif not d.get('SO_CHUNG_TU'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Số chứng từ>  bắt buộc nhập' % (line_number,)})
			elif not d.get('TK_NO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK Nợ>  bắt buộc nhập' % (line_number,)})
			elif not d.get('TK_CO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK Có>  bắt buộc nhập' % (line_number,)})
			

			doi_tuong_id = None
			nv_chi_id = None
			loai_tien_id = None
	
			tk_co_id = None
			tk_no_id = None
			doi_tuong_chi_tiet_id = None

			tk_ngan_hang_chi_id = None
			tk_ngan_hang_nhan_id = None
			tk_thue_gtgt_id = None
			phan_tram_thue_gtgt_id = None
			nhom_hhdv_mua_vao_id = None
			nha_cung_cap_id = None
			khoan_muc_cp_id = None
			don_vi_id = None
			cong_trinh_id = None
			don_dat_hang_id = None
			hop_dong_ban_id = None
			hop_dong_mua_id = None
			ma_thong_ke_id = None
			doi_tuong_thcp_id = None
			mau_so_hoa_don_id = None

			if d.get('TAI_KHOAN_CHI'):
				tk_ngan_hang_chi_id = self.env['danh.muc.tai.khoan.ngan.hang'].search([('SO_TAI_KHOAN', '=', d.get('TAI_KHOAN_CHI'))], limit=1)
				if not tk_ngan_hang_chi_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy số tài khoản <%s> trong danh mục tài khoản ngân hàng' % (line_number,d.get('TAI_KHOAN_CHI'))}) 
			

			if d.get('MA_DOI_TUONG'):
				doi_tuong_id = self.env['res.partner'].search([('MA', '=', d.get('MA_DOI_TUONG'))], limit=1)
				if not doi_tuong_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã đối tượng <%s> trong danh mục nhà cung cấp' % (line_number,d.get('MA_DOI_TUONG'))})

			if d.get('TAI_KHOAN_NHAN'):
				tk_ngan_hang_nhan_id = self.env['danh.muc.doi.tuong.chi.tiet'].search([('SO_TAI_KHOAN', '=', d.get('TAI_KHOAN_NHAN'))], limit=1)
				if not tk_ngan_hang_nhan_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy số tài khoản <%s> trong danh mục đối tượng chi tiết' % (line_number,d.get('TAI_KHOAN_NHAN'))}) 
			

			if d.get('NHAN_VIEN'):
				nv_chi_id = self.env['res.partner'].search([('MA', '=', d.get('NHAN_VIEN'))], limit=1)
				if not nv_chi_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy nhân viên <%s> trong danh mục nhân viên' % (line_number,d.get('NHAN_VIEN'))})

			if d.get('LOAI_TIEN'):
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', d.get('LOAI_TIEN'))], limit=1)
				if not loai_tien_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Loại tiền <%s> trong danh mục loại tiền' % (line_number,d.get('LOAI_TIEN'))})
			
			if d.get('TK_CO'):
				tk_co_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_CO'))], limit=1)
				if not tk_co_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK có <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_CO'))})
			
			if d.get('TK_NO'):
				tk_no_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_NO'))], limit=1)
				if not tk_no_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK nợ <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_NO'))})
			
			if d.get('DOI_TUONG'):
				doi_tuong_chi_tiet_id = self.env['res.partner'].search([('MA', '=', d.get('DOI_TUONG'))], limit=1)
				if not doi_tuong_chi_tiet_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Đối tượng <%s> trong danh mục đối tượng' % (line_number,d.get('DOI_TUONG'))})
			
			if d.get('KHOAN_MUC_CHI_PHI'):
				khoan_muc_cp_id = self.env['danh.muc.khoan.muc.cp'].search([('MA_KHOAN_MUC_CP', '=', d.get('KHOAN_MUC_CHI_PHI'))], limit=1)
				if not khoan_muc_cp_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy khoản mục chi phí <%s> trong danh mục khoản mục chi phí' % (line_number,d.get('KHOAN_MUC_CHI_PHI'))})

			if d.get('DON_VI'):
				don_vi_id = self.env['danh.muc.to.chuc'].search([('MA_DON_VI', '=', d.get('DON_VI'))], limit=1)
				if not don_vi_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Đơn vị <%s> trong danh mục cơ cấu tổ chức' % (line_number,d.get('DON_VI'))})
			
			if d.get('DOI_TUONG_TAP_HOP_CHI_PHI'):
				doi_tuong_thcp_id = self.env['danh.muc.doi.tuong.tap.hop.chi.phi'].search([('MA_DOI_TUONG_THCP', '=', d.get('DOI_TUONG_TAP_HOP_CHI_PHI'))], limit=1)
				if not doi_tuong_thcp_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Đối tượng THCP <%s> trong danh mục đối tượng tập hợp chi phí' % (line_number,d.get('DOI_TUONG_TAP_HOP_CHI_PHI'))})
			
			if d.get('CONG_TRINH'):
				cong_trinh_id = self.env['danh.muc.cong.trinh'].search([('MA_CONG_TRINH', '=', d.get('CONG_TRINH'))], limit=1)
				if not cong_trinh_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Công trình <%s> trong danh mục công trình' % (line_number,d.get('CONG_TRINH'))})
			
			if d.get('DON_DAT_HANG'):
				don_dat_hang_id = self.env['account.ex.don.dat.hang'].search([('SO_DON_HANG', '=', d.get('DON_DAT_HANG'))], limit=1)
				if not don_dat_hang_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Đơn đặt hàng <%s> trong Đơn đặt hàng' % (line_number,d.get('DON_DAT_HANG'))})

			if d.get('HOP_DONG_BAN'):
				hop_dong_ban_id = self.env['sale.ex.hop.dong.ban'].search([('SO_HOP_DONG', '=', d.get('HOP_DONG_BAN'))], limit=1)
				if not hop_dong_ban_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Hợp đồng bán <%s> trong Hợp đồng bán' % (line_number,d.get('HOP_DONG_BAN'))})

			if d.get('HOP_DONG_MUA'):
				hop_dong_mua_id = self.env['purchase.ex.hop.dong.mua.hang'].search([('SO_HOP_DONG', '=', d.get('HOP_DONG_MUA'))], limit=1)
				if not hop_dong_mua_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Hợp đồng mua <%s> trong Hợp đồng mua' % (line_number,d.get('HOP_DONG_MUA'))})

			if d.get('MA_THONG_KE'):
				ma_thong_ke_id = self.env['danh.muc.ma.thong.ke'].search([('MA_THONG_KE', '=', d.get('MA_THONG_KE'))], limit=1)
				if not ma_thong_ke_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã thống kê <%s> trong danh mục mã thống kê' % (line_number,d.get('MA_THONG_KE'))})

			if d.get('TK_THUE_GTGT'):
				tk_thue_gtgt_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_THUE_GTGT'))], limit=1)
				if not tk_thue_gtgt_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK thuế GTGT <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_THUE_GTGT'))})
			
			if d.get('PHAN_TRAM_THUE_GTGT'):
				phan_tram_thue_gtgt_id = self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', d.get('PHAN_TRAM_THUE_GTGT'))], limit=1)
				if not phan_tram_thue_gtgt_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy phần trăm thuế GTGT <%s> trong danh mục thuế suất giá trị gia tăng' % (line_number,d.get('PHAN_TRAM_THUE_GTGT'))})
			
			if d.get('MAU_SO_HOA_DON'):
				mau_so_hoa_don_id = self.env['danh.muc.mau.so.hd'].search([('MAU_SO_HD', '=', d.get('MAU_SO_HOA_DON'))], limit=1)
				if not mau_so_hoa_don_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mẫu số HĐ <%s> trong danh mục mẫu số hóa đơn' % (line_number,d.get('MAU_SO_HOA_DON'))})
			
			if d.get('NHOM_HHDV_MUA_VAO'):
				nhom_hhdv_mua_vao_id = self.env['danh.muc.nhom.hhdv'].search([('MA_NHOM_HHDV', '=', d.get('NHOM_HHDV_MUA_VAO'))], limit=1)
				if not nhom_hhdv_mua_vao_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Nhóm HHDV mua vào <%s> trong danh mục nhóm hàng hóa dịch vụ mua vào' % (line_number,d.get('NHOM_HHDV_MUA_VAO'))})
			
			if d.get('MA_NHA_CUNG_CAP'):
				nha_cung_cap_id = self.env['res.partner'].search([('MA', '=', d.get('MA_NHA_CUNG_CAP'))], limit=1)
				if not nha_cung_cap_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã nhà cung cấp <%s> trong danh mục nhà cung cấp' % (line_number,d.get('MA_NHA_CUNG_CAP'))})

			phuong_thuc_thanh_toan =''
			if d.get('PHUONG_THUC_THANH_TOAN') == '1':
				phuong_thuc_thanh_toan = 'SEC_CHUYEN_KHOAN'
			elif d.get('PHUONG_THUC_THANH_TOAN') == '2':
				phuong_thuc_thanh_toan = 'SEC_TIEN_MAT'
			else:
				phuong_thuc_thanh_toan = 'UY_NHIEM_CHI'

			noi_dung_thanh_toan = ''
			if d.get('NOI_DUNG_THANH_TOAN') == '40':
				noi_dung_thanh_toan = '40'
			elif d.get('NOI_DUNG_THANH_TOAN') == '42':
				noi_dung_thanh_toan = '42'
			else:
				noi_dung_thanh_toan = '43'

			
			key = '_'.join([phuong_thuc_thanh_toan + str(d.get('SO_CHUNG_TU'))]) # d[0]: Loại nghiệp vụ - d[1]: Số chứng từ
			if key not in dict:
				dict[key] = {
					
					'PHUONG_THUC_TT': phuong_thuc_thanh_toan,
					'NGAY_HACH_TOAN': d.get('NGAY_HACH_TOAN'),
					'NGAY_CHUNG_TU': d.get('NGAY_CHUNG_TU'),
					'SO_CHUNG_TU': d.get('SO_CHUNG_TU'),
					
					'TAI_KHOAN_CHI_GUI_ID': tk_ngan_hang_chi_id.id if tk_ngan_hang_chi_id else None,
					'TEN_TK_CHI': d.get('MO_TAI_NGAN_HANG'),
					'NOI_DUNG_TT': noi_dung_thanh_toan,
					'TEN_NOI_DUNG_TT': d.get('DIEN_GIAI_NOI_DUNG_THANH_TOAN'),
					'DOI_TUONG_ID': doi_tuong_id.id if doi_tuong_id else None,
					'TEN_DOI_TUONG': d.get('TEN_DOI_TUONG'),

					'DIA_CHI': d.get('DIA_CHI'),
					'TAI_KHOAN_THU_NHAN_ID': tk_ngan_hang_nhan_id.id if tk_ngan_hang_nhan_id else None,
					'TEN_TK_NHAN': d.get('TAI_NGAN_HANG_NHAN'),
					'NGUOI_LINH_TIEN': d.get('NGUOI_LINH_TIEN'),
					'TAI_KHOAN_CHI_GUI_ID': tk_ngan_hang_chi_id.id if tk_ngan_hang_chi_id else None,
					'NHAN_VIEN_ID': nv_chi_id.id if nv_chi_id else None,
					'currency_id': loai_tien_id.id if loai_tien_id else None,
					'TY_GIA': d.get('TY_GIA'),
					'ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS': [],
					'ACCOUNT_EX_PHIEU_THU_CHI_THUE_IDS': []
				}

			dict[key]['ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS'] += [[0,0,{
				
				'DIEN_GIAI_DETAIL': d.get('DIEN_GIAI'),
				'TK_NO_ID': tk_no_id.id if tk_no_id else None,
				'TK_CO_ID': tk_co_id.id if tk_co_id else None,
				'SO_TIEN': d.get('SO_TIEN'),
				'SO_TIEN_QUY_DOI': d.get('SO_TIEN') * d.get('TY_GIA'),
				'DOI_TUONG_ID': doi_tuong_chi_tiet_id.id if doi_tuong_chi_tiet_id else None,
				'KHOAN_MUC_CP_ID': khoan_muc_cp_id.id if khoan_muc_cp_id else None,
				'DON_VI_ID': don_vi_id.id if don_vi_id else None,
				'DOI_TUONG_THCP_ID': doi_tuong_thcp_id.id if doi_tuong_thcp_id else None,
				'CONG_TRINH_ID': cong_trinh_id.id if cong_trinh_id else None,
				'DON_DAT_HANG_ID': don_dat_hang_id.id if don_dat_hang_id else None,
				'HOP_DONG_MUA_ID': hop_dong_mua_id.id if hop_dong_mua_id else None,
				'HOP_DONG_BAN_ID': hop_dong_ban_id.id if hop_dong_ban_id else None,
				'MA_THONG_KE_ID': ma_thong_ke_id.id if ma_thong_ke_id else None,
				
			}]]

			dict[key]['ACCOUNT_EX_PHIEU_THU_CHI_THUE_IDS'] += [[0,0,{
				
				'DIEN_GIAI_THUE': d.get('DIEN_GIAI_THUE'),
				'TK_THUE_GTGT_ID': tk_thue_gtgt_id.id if tk_thue_gtgt_id else None,
				'TIEN_THUE_GTGT': d.get('TIEN_THUE_GTGT'),
				'PHAN_TRAM_THUE_GTGT_ID': phan_tram_thue_gtgt_id.id if phan_tram_thue_gtgt_id else None,
				'GIA_TRI_HHDV_CHUA_THUE': d.get('HHDV_CHUA_THUE'),
				'MAU_SO_HD_ID': mau_so_hoa_don_id.id if mau_so_hoa_don_id else None,

				'KY_HIEU_HOA_DON':  d.get('KY_HIEU_HOA_DON'),
				'NGAY_HOA_DON':  d.get('NGAY_HOA_DON'),
				'SO_HOA_DON': d.get('SO_HOA_DON'),

				'NHOM_HHDV_MUA_VAO': nhom_hhdv_mua_vao_id.id if nhom_hhdv_mua_vao_id else None,
				'DOI_TUONG_ID': nha_cung_cap_id.id if nha_cung_cap_id else None,
				'TEN_NCC': d.get('TEN_NHA_CUNG_CAP'),
				'MA_SO_THUE_NCC': d.get('MA_SO_THUE_NHA_CUNG_CAP'),
				
			}]]
			line_number += 1
		if not error:
			for key in dict:
				new_dict = dict.get(key)

				if new_dict.get('PHUONG_THUC_TT') =='UY_NHIEM_CHI':
					new_dict['LOAI_CHUNG_TU'] = 1510
	
				elif new_dict.get('PHUONG_THUC_TT') =='SEC_TIEN_MAT':
					new_dict['LOAI_CHUNG_TU'] = 1520
					
				elif new_dict.get('PHUONG_THUC_TT') =='SEC_CHUYEN_KHOAN':
					new_dict['LOAI_CHUNG_TU'] = 1530
				
				new_dict['NHOM_CHUNG_TU'] = int(new_dict.get('NOI_DUNG_TT',0))
				
				self.env['account.ex.phieu.thu.chi'].create(new_dict)
			return {}

		return {'messages' : error}
	
	# Hàm import cho Ngân hàng chuyển tiền nội bộ
	def import_from_excel_ngan_hang_phieu_chuyen_tien(self, import_fields, data):
		dict = {}
		error = []
		line_number = 1
		for item in data:
			d = self.get_formatted_data(import_fields, item, error, line_number)
			####### Validate ########
						
			if not d.get('NGAY_HACH_TOAN'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Ngày hạch toán>  bắt buộc nhập' % (line_number,)})
			elif not d.get('NGAY_CHUNG_TU'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Ngày chứng từ>  bắt buộc nhập' % (line_number,)})
			elif not d.get('SO_CHUNG_TU'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Số chứng từ>  bắt buộc nhập' % (line_number,)})
			
			elif not d.get('TAI_KHOAN_DI'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Tài khoản đi (*)>  bắt buộc nhập' % (line_number,)})
			
			elif not d.get('TAI_KHOAN_DEN'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Tài khoản đến (*)>  bắt buộc nhập' % (line_number,)})
			
			elif not d.get('TK_NO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK Nợ>  bắt buộc nhập' % (line_number,)})
			elif not d.get('TK_CO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK Có>  bắt buộc nhập' % (line_number,)})
			

			tai_khoan_di_id = None
			tai_khoan_den_id = None
			loai_tien_id = None
			tk_co_id = None
			tk_no_id = None
			ma_thong_ke_id = None

			if d.get('LOAI_TIEN'):
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', d.get('LOAI_TIEN'))], limit=1)
				if not loai_tien_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Loại tiền <%s> trong danh mục loại tiền' % (line_number,d.get('LOAI_TIEN'))})
			
			if d.get('TK_CO'):
				tk_co_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_CO'))], limit=1)
				if not tk_co_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK có <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_CO'))})
			
			if d.get('TK_NO'):
				tk_no_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_NO'))], limit=1)
				if not tk_no_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK nợ <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_NO'))})
			
			if d.get('TAI_KHOAN_DI'):
				tai_khoan_di_id = self.env['danh.muc.tai.khoan.ngan.hang'].search([('SO_TAI_KHOAN', '=', d.get('TAI_KHOAN_DI'))], limit=1)
				if not tai_khoan_di_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Tài khoản đi (*) <%s> trong danh mục tài khoản ngân hàng' % (line_number,d.get('TAI_KHOAN_DI'))}) 
			
			if d.get('TAI_KHOAN_DEN'):
				tai_khoan_den_id = self.env['danh.muc.tai.khoan.ngan.hang'].search([('SO_TAI_KHOAN', '=', d.get('TAI_KHOAN_DEN'))], limit=1)
				if not tai_khoan_den_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Tài khoản đến (*) <%s> trong danh mục tài khoản ngân hàng' % (line_number,d.get('TAI_KHOAN_DEN'))}) 
			
			if d.get('MA_THONG_KE'):
				ma_thong_ke_id = self.env['danh.muc.ma.thong.ke'].search([('MA_THONG_KE', '=', d.get('MA_THONG_KE'))], limit=1)
				if not ma_thong_ke_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã thống kê <%s> trong danh mục mã thống kê' % (line_number,d.get('MA_THONG_KE'))})

			# Trường số lượng details
			
			key = '_'.join([str(d.get('NGAY_HACH_TOAN')) + str(d.get('SO_CHUNG_TU'))]) # d[0]: Loại nghiệp vụ - d[1]: Số chứng từ
			if key not in dict:
				dict[key] = {
					
					'NGAY_HACH_TOAN': d.get('NGAY_HACH_TOAN'),
					'NGAY_CHUNG_TU': d.get('NGAY_CHUNG_TU'),
					'SO_CHUNG_TU': d.get('SO_CHUNG_TU'),
					
					'TAI_KHOAN_CHI_GUI_ID': tai_khoan_di_id.id if tai_khoan_di_id else None,
					'TAI_KHOAN_DEN_ID': tai_khoan_den_id.id if tai_khoan_den_id else None,

					'TEN_TK_CHI': d.get('TEN_TAI_KHOAN_DI'),
					'TEN_TK_NHAN_CTNB': d.get('TEN_TAI_KHOAN_DEN'),
					'DIEN_GIAI': d.get('LY_DO_CHUYEN'),
					
					'currency_id': loai_tien_id.id if loai_tien_id else None,
					'TY_GIA': d.get('TY_GIA'),
					'ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS': []
				}
			dict[key]['ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS'] += [[0,0,{
				
				'DIEN_GIAI_DETAIL': d.get('DIEN_GIAI'),
				'TK_NO_ID': tk_no_id.id if tk_no_id else None,
				'TK_CO_ID': tk_co_id.id if tk_co_id else None,
				'SO_TIEN': d.get('SO_TIEN'),
				'SO_TIEN_QUY_DOI': d.get('SO_TIEN') * d.get('TY_GIA'),
				'MA_THONG_KE_ID': ma_thong_ke_id.id if ma_thong_ke_id else None,
				
			}]]
			line_number += 1
		if not error:
			for key in dict:
				new_dict = dict.get(key)
				new_dict['LOAI_CHUNG_TU'] = 1560
				self.env['account.ex.phieu.thu.chi'].create(new_dict)
			return {}

		return {'messages' : error}