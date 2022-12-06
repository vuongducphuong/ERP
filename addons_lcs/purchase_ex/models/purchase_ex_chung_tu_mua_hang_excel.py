# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError , UserError
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round


class PURCHASE_DOCUMENT_EXCEL(models.Model):
	_name = 'purchase.document.excel'
	_description = 'Chứng từ mua hàng'
	_auto = False


	HINH_THUC_MUA_HANG = fields.Selection([('1', 'Mua hàng trong nước nhập kho'), ('2', 'Mua hàng trong nước không qua kho'), ('3', 'Mua nhập khẩu nhập kho'),('4', 'Mua nhập khẩu không qua kho')],string='Hình thức mua hàng', default= '1')
	PHUONG_THUC_THANH_TOAN = fields.Selection([('0', 'Chưa thanh toán'), ('1', 'Tiền mặt'), ('2', 'Ủy nhiệm chi'),('3', 'Séc chuyển khoản'),('4', 'Séc tiền mặt')],string='Phương thức thanh toán',default= '0')
	NHAN_KEM_HOA_DON = fields.Selection([('0', 'Nhận hàng không kèm hóa đơn'), ('1', 'Nhận hàng kèm hóa đơn'), ('2', 'Không có hóa đơn')],string='Nhận kèm hóa đơn',default= '1')

	NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán (*)', help='Ngày hạch toán (*)')
	NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ (*)', help='Ngày chứng từ (*)')
	SO_CHUNG_TU = fields.Char(string='Số chứng từ (*)', help='Số chứng từ (*)')
	SO_PHIEU_NHAP = fields.Char(string='Số phiếu nhập', help='Số phiếu nhập')
	LY_DO_XUAT = fields.Char(string='Lý do xuất', help='Lý do xuất')
	MAU_SO_HD = fields.Char(string='Mẫu số HĐ', help='Mẫu số HĐ')
	KY_HIEU_HD = fields.Char(string='Ký hiệu HĐ', help='Ký hiệu HĐ')
	SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
	NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')

	MA_NHA_CUNG_CAP = fields.Char(string='Mã nhà cung cấp', help='Mã nhà cung cấp')
	TEN_NHA_CUNG_CAP = fields.Char(string='Tên nhà cung cấp', help='Tên nhà cung cấp')
	NGUOI_GIAO_HANG = fields.Char(string='Người giao hàng', help='Người giao hàng')
	
	DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
	NV_MUA_HANG = fields.Char(string='NV mua hàng', help='NV mua hàng')
	LOAI_TIEN = fields.Char(string='Loại tiền', help='Loại tiền')
	TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá', default=1)

	MA_HANG = fields.Char(string='Mã hàng (*)', help='Mã hàng (*)')
	TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng')
	KHO = fields.Char(string='Kho', help='Kho')
	TK_KHO = fields.Char(string='TK kho', help='TK kho')
	TK_CHI_PHI = fields.Char(string='TK chi phí', help='TK chi phí')

	DVT = fields.Char(string='ĐVT', help='ĐVT')
	SO_LUONG = fields.Float(string='Số lượng', help='Số lượng')
	DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá')
	THANH_TIEN = fields.Float(string='Thành tiền', help='Thành tiền')
	THANH_TIEN_QUY_DOI = fields.Float(string='Thành tiền quy đổi', help='Thành tiền quy đổi')
	TY_LE_CK = fields.Float(string='Tỷ lệ CK', help='Tỷ lệ CK')
	TIEN_CHIET_KHAU = fields.Float(string='Tiền chiết khấu', help='Tiền chiết khấu')
	TIEN_CHIET_KHAU_QUY_DOI = fields.Float(string='Tiền chiết khấu quy đổi', help='Tiền chiết khấu quy đổi')
	PHI_HANG_VE_KHO = fields.Float(string='Phí hàng về kho/Chi phí mua hàng', help='Phí hàng về kho/Chi phí mua hàng')
	PHAN_TRAM_THUE_GTGT = fields.Char(string='% thuế GTGT', help='% thuế GTGT')
	TIEN_THUE_GTGT = fields.Float(string='Tiền thuế GTGT', help='Tiền thuế GTGT')
	TIEN_THUE_GTGT_QUY_DOI = fields.Float(string='Tiền thuế GTGT quy đổi', help='Tiền thuế GTGT quy đổi')
	TKDU_THUE_GTGT = fields.Char(string='TKĐƯ thuế GTGT', help='TKĐƯ thuế GTGT')
	TK_THUE_GTGT = fields.Char(string='TK thuế GTGT', help='TK thuế GTGT')
	NHOM_HHDV_MUA_VAO = fields.Char(string='Nhóm HHDV mua vào', help='Nhóm HHDV mua vào')
	PHI_TRUOC_HAI_QUAN = fields.Float(string='Phí trước hải quan', help='Phí trước hải quan')
	GIA_TINH_THUE_NHAP_KHAU = fields.Float(string='Giá tính thuế NK', help='Giá tính thuế NK')
	PHAN_TRAM_THUE_NK = fields.Float(string='% thuế NK', help='% thuế NK')
	TIEN_THUE_NHAP_KHAU = fields.Float(string='Tiền thuế NK', help='Tiền thuế NK')
	TK_THUE_NK = fields.Char(string='TK thuế NK', help='TK thuế NK')

	PHAN_TRAM_THUE_TTDB = fields.Float(string='% thuế TTĐB', help='% thuế TTĐB')
	TIEN_THUE_TTDB = fields.Float(string='Tiền thuế TTĐB', help='Tiền thuế TTĐB')
	TK_THUE_TTDB = fields.Char(string='TK thuế TTĐB', help='TK thuế TTĐB')


	# các trường Mua dịch vụ
	LA_CP_MUA_HANG = fields.Selection([('0', 'Không là chi phí mua hàng'), ('1', 'Là chi phí mua hàng'),], string='Là CP mua hàng', default = '0')
	DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
	DIEN_GIAI_LY_DO_CHI_NDTT = fields.Char(string='Diễn giải/Lý do chi/Nội dung thanh toán', help='Diễn giải/Lý do chi/Nội dung thanh toán')
	MA_DICH_VU = fields.Char(string='Mã dịch vụ (*)', help='Mã dịch vụ (*)')
	TEN_DICH_VU = fields.Char(string='Tên dịch vụ', help='Tên dịch vụ')
	TK_CHI_PHI_KHO = fields.Char(string='TK chi phí/TK kho (*)', help='TK chi phí/TK kho (*)')
	TK_CONG_NO_TIEN = fields.Char(string='TK công nợ/TK tiền (*)', help='TK công nợ/TK tiền (*)')
	DOI_TUONG = fields.Char(string='Đối tượng', help='Đối tượng')
	MA_NCC = fields.Char(string='Mã NCC', help='Mã NCC')
	TEN_NCC = fields.Char(string='Tên NCC', help='Tên NCC')
	MA_SO_THUE_NCC = fields.Char(string='Mã số thuế NCC', help='Mã số thuế NCC')
	DIA_CHI_NCC = fields.Char(string='Địa chỉ NCC', help='Địa chỉ NCC')

	def import_from_excel(self, import_fields, data):
		default_type = self._context.get('default_type')
		result = None
		if default_type == 'hang_hoa':
			result = self.import_from_excel_mua_hang_hoa(import_fields, data)
		elif default_type == 'dich_vu':
			result = self.import_from_excel_mua_dich_vu(import_fields, data)
		
		return result
	# hàm import excel cho chứng từ mua hàng
	def import_from_excel_mua_hang_hoa(self, import_fields, data):
		dict = {}
		error = []
		line_number = 1
		for item in data:
			d = self.get_formatted_data(import_fields, item, error, line_number)
			####### Validate ########
			hi = d.get('HINH_THUC_MUA_HANG')
			
			if not d.get('NGAY_HACH_TOAN'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Ngày hạch toán>  bắt buộc nhập' % (line_number,)})
			elif not d.get('NGAY_CHUNG_TU'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Ngày chứng từ>  bắt buộc nhập' % (line_number,)})
			elif not d.get('SO_CHUNG_TU'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Số chứng từ>  bắt buộc nhập' % (line_number,)})
			elif not d.get('MA_HANG'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Mã hàng>  bắt buộc nhập' % (line_number,)})
			elif not d.get('TK_CONG_NO_TIEN'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK công nợ/TK tiền>  bắt buộc nhập' % (line_number,)})

			mau_so_hd_id = None
			nha_cung_cap_id = None
			nv_mua_hang_id = None
			loai_tien_id = None
			ma_hang_id = None
			kho_id = None
			tk_kho_id = None
			tk_chi_phi_id = None
			tk_co_id = None

			tk_no_id = None #Tạo tham số này để gán giá trị của tk_chi_phi_id và tk_co_id

			don_vi_tinh_id = None
			phan_tram_thue_gtgt_id = None
			tkdu_thue_gtgt_id = None
			tk_thue_gtgt_id = None
			nhom_hhdv_mua_vao_id = None

			tk_thue_nk_id = None
			tk_thue_ttdb_id = None
			
			if d.get('MAU_SO_HD'):
				mau_so_hd_id = self.env['danh.muc.mau.so.hd'].search([('MAU_SO_HD', '=', d.get('MAU_SO_HD'))], limit=1)
				if not mau_so_hd_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mẫu số HĐ <%s> trong danh mục mẫu số hóa đơn' % (line_number,d.get('MAU_SO_HD'))})
			
			if d.get('MA_NHA_CUNG_CAP'):
				nha_cung_cap_id = self.env['res.partner'].search([('MA', '=', d.get('MA_NHA_CUNG_CAP'))], limit=1)
				if not nha_cung_cap_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã nhà cung cấp <%s> trong danh mục nhà cung cấp' % (line_number,d.get('MA_NHA_CUNG_CAP'))})

			if d.get('NV_MUA_HANG'):
				nv_mua_hang_id = self.env['res.partner'].search([('MA', '=', d.get('NV_MUA_HANG'))], limit=1)
				if not nv_mua_hang_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy NV mua hàng <%s> trong danh mục nhân viên' % (line_number,d.get('NV_MUA_HANG'))})

			if d.get('LOAI_TIEN'):
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', d.get('LOAI_TIEN'))], limit=1)
				if not loai_tien_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Loại tiền <%s> trong danh mục loại tiền' % (line_number,d.get('LOAI_TIEN'))})

			if d.get('MA_HANG'):
				ma_hang_id = self.env['danh.muc.vat.tu.hang.hoa'].search([('MA', '=', d.get('MA_HANG'))], limit=1)
				if not ma_hang_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã hàng <%s> trong danh mục vật tư hàng hóa' % (line_number,d.get('MA_HANG'))})
			
			if d.get('KHO'):
				kho_id = self.env['danh.muc.kho'].search([('MA_KHO', '=', d.get('KHO'))], limit=1)
				if not kho_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Kho <%s> trong danh mục kho' % (line_number,d.get('KHO'))})

			if d.get('TK_KHO'):
				tk_kho_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_KHO'))], limit=1)
				if not tk_kho_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK Kho <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_KHO'))})
			
			if d.get('TK_CHI_PHI'):
				tk_chi_phi_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_CHI_PHI'))], limit=1)
				if not tk_chi_phi_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK chi phí <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_CHI_PHI'))})
			
			if d.get('TK_CONG_NO_TIEN'):
				tk_co_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_CONG_NO_TIEN'))], limit=1)
				if not tk_co_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK công nợ/TK tiền <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_CONG_NO_TIEN'))})

			if d.get('DVT'):
				don_vi_tinh_id = self.env['danh.muc.don.vi.tinh'].search([('DON_VI_TINH', '=', d.get('DVT'))], limit=1)
				if not don_vi_tinh_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy ĐVT <%s> trong danh mục đơn vị tính' % (line_number,d.get('DVT'))})

			if d.get('PHAN_TRAM_THUE_GTGT'):
				phan_tram_thue_gtgt_id = self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', d.get('PHAN_TRAM_THUE_GTGT'))], limit=1)
				if not phan_tram_thue_gtgt_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy phần trăm thuế GTGT <%s> trong danh mục thuế suất giá trị gia tăng' % (line_number,d.get('PHAN_TRAM_THUE_GTGT'))})
			
			if d.get('TKDU_THUE_GTGT'):
				tkdu_thue_gtgt_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TKDU_THUE_GTGT'))], limit=1)
				if not tkdu_thue_gtgt_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TKĐƯ thuế GTGT <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TKDU_THUE_GTGT'))})
			
			if d.get('TK_THUE_GTGT'):
				tk_thue_gtgt_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_THUE_GTGT'))], limit=1)
				if not tk_thue_gtgt_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK thuế GTGT <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_THUE_GTGT'))})
			
			if d.get('NHOM_HHDV_MUA_VAO'):
				nhom_hhdv_mua_vao_id = self.env['danh.muc.nhom.hhdv'].search([('MA_NHOM_HHDV', '=', d.get('NHOM_HHDV_MUA_VAO'))], limit=1)
				if not nhom_hhdv_mua_vao_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Nhóm HHDV mua vào <%s> trong danh mục nhóm hàng hóa dịch vụ mua vào' % (line_number,d.get('NHOM_HHDV_MUA_VAO'))})
			
			if d.get('TK_THUE_TTDB'):
				tk_thue_ttdb_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_THUE_TTDB'))], limit=1)
				if not tk_thue_ttdb_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK thuế TTĐB <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_THUE_TTDB'))})
			
			if d.get('TK_THUE_NK'):
				tk_thue_nk_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_THUE_NK'))], limit=1)
				if not tk_thue_nk_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK thuế NK <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_THUE_NK'))})
			
			# if d.get('HINH_THUC_MUA_HANG') :
			#########################
			hinh_thuc_mua_hang = ''
			da_thanh_toan = False
			loai_thanh_toan = ''
			loai_hoa_don = ''
			tien_thue_gtgt_quy_doi = 0
		
			# Gán giá trị cho Cột LOAI_CHUNG_TU_MH
			if d.get('HINH_THUC_MUA_HANG') == '1' or d.get('HINH_THUC_MUA_HANG') == '':
				hinh_thuc_mua_hang = 'trong_nuoc_nhap_kho'
				tk_no_id = tk_kho_id
				tien_thue_gtgt_quy_doi = float_round(d.get('TIEN_THUE_GTGT') * d.get('TY_GIA'), 0)
			elif d.get('HINH_THUC_MUA_HANG')  == '2':
				hinh_thuc_mua_hang = 'trong_nuoc_khong_qua_kho'
				tk_no_id = tk_chi_phi_id
				tien_thue_gtgt_quy_doi = float_round(d.get('TIEN_THUE_GTGT') * d.get('TY_GIA'), 0)
			elif d.get('HINH_THUC_MUA_HANG') == '3':
				hinh_thuc_mua_hang = 'nhap_khau_nhap_kho'
				tk_no_id = tk_kho_id
				tien_thue_gtgt_quy_doi = float_round(d.get('TIEN_THUE_GTGT'), 0)
			elif d.get('HINH_THUC_MUA_HANG') == '4':
				hinh_thuc_mua_hang = 'nhap_khau_khong_qua_kho'
				tk_no_id = tk_chi_phi_id
				tien_thue_gtgt_quy_doi = float_round(d.get('TIEN_THUE_GTGT'), 0)

			so_chung_tu_temp = 'SO_CHUNG_TU_MUA_HANG' #Khai báo cột số chứng từ tạm để gán số chứng từ ở tất cả các trường hợp do cột số chứng từ compute
			
			# Gán giá trị cho Cột DA_THANH_TOAN và Loại thanh toán
			if d.get('PHUONG_THUC_THANH_TOAN') == '0' or d.get('PHUONG_THUC_THANH_TOAN') == '':
				da_thanh_toan = False
			elif d.get('PHUONG_THUC_THANH_TOAN') == '1':
				da_thanh_toan = True
				loai_thanh_toan = 'tien_mat'
				so_chung_tu_temp = 'SO_PHIEU_CHI'
			elif d.get('PHUONG_THUC_THANH_TOAN') == '2':
				da_thanh_toan = True
				loai_thanh_toan = 'uy_nhiem_chi'
				so_chung_tu_temp = 'SO_UY_NHIEM_CHI'
			elif d.get('PHUONG_THUC_THANH_TOAN') == '3':
				da_thanh_toan = True
				loai_thanh_toan = 'sec_chuyen_khoan'
				so_chung_tu_temp = 'SO_SEC_CHUYEN_KHOAN'
			elif d.get('PHUONG_THUC_THANH_TOAN') == '4':
				da_thanh_toan = True
				loai_thanh_toan = 'sec_tien_mat'
				so_chung_tu_temp = 'SO_SEC_TIEN_MAT'

			# Gán giá trị cho trường LOAI_HOA_DON
			if d.get('NHAN_KEM_HOA_DON') == '0' or d.get('NHAN_KEM_HOA_DON') == '':
				loai_hoa_don = '0'
			elif d.get('NHAN_KEM_HOA_DON') == '1':
				loai_hoa_don = '1'
			elif d.get('NHAN_KEM_HOA_DON') == '2':
				loai_hoa_don = '2'

			key = '_'.join([hinh_thuc_mua_hang + str(d.get('SO_CHUNG_TU'))]) # d[0]: Loại nghiệp vụ - d[1]: Số chứng từ
			if key not in dict:
				dict[key] = {
					'LOAI_CHUNG_TU_MH': hinh_thuc_mua_hang,
					'DA_THANH_TOAN': da_thanh_toan,
					'LOAI_THANH_TOAN': loai_thanh_toan,
					'LOAI_HOA_DON': loai_hoa_don,
				
					'NGAY_HACH_TOAN': d.get('NGAY_HACH_TOAN'),
					'NGAY_CHUNG_TU': d.get('NGAY_CHUNG_TU'),
					'SO_PHIEU_NHAP': d.get('SO_PHIEU_NHAP'),
					
					so_chung_tu_temp: d.get('SO_CHUNG_TU'),

					'MAU_SO_HD_ID': mau_so_hd_id.id if mau_so_hd_id else None,
					'KY_HIEU_HD': d.get('KY_HIEU_HD'),
					'SO_HOA_DON': d.get('SO_HOA_DON'),
					'NGAY_HOA_DON': d.get('NGAY_HOA_DON'),

					'DOI_TUONG_ID': nha_cung_cap_id.id if nha_cung_cap_id else None,
					'TEN_DOI_TUONG': d.get('TEN_NHA_CUNG_CAP'),
					'NGUOI_GIAO_HANG': d.get('NGUOI_GIAO_HANG'),
					'DIEN_GIAI': d.get('DIEN_GIAI'),
					'NHAN_VIEN_ID': nv_mua_hang_id.id if nv_mua_hang_id else None,
					'currency_id': loai_tien_id.id if loai_tien_id else None,
					'TY_GIA': d.get('TY_GIA'),
					'CHI_TIET_IDS': []
				}
			dict[key]['CHI_TIET_IDS'] += [[0,0,{
				'MA_HANG_ID': ma_hang_id.id if ma_hang_id else None,
				'name': d.get('TEN_HANG'),
				'KHO_ID': kho_id.id if kho_id else None,
				# Tài khoản chi phí và tài khoản kho
				'TK_NO_ID': tk_no_id.id if tk_no_id else None,
				# Tài khoản tiền / tài khoản công nợ
				'TK_CO_ID': tk_co_id.id if tk_co_id else None,
				'DVT_ID': don_vi_tinh_id.id if don_vi_tinh_id else None,
				'SO_LUONG': d.get('SO_LUONG') ,
				'DON_GIA': d.get('DON_GIA'),
				'THANH_TIEN': d.get('THANH_TIEN'),
				'THANH_TIEN_QUY_DOI': float_round(d.get('THANH_TIEN') * d.get('TY_GIA'), 0),
				'TY_LE_CK': d.get('TY_LE_CK'),
				'TIEN_CHIET_KHAU': d.get('TIEN_CHIET_KHAU'),
				'TIEN_CHIET_KHAU_QUY_DOI': float_round(d.get('TIEN_CHIET_KHAU') * d.get('TY_GIA'), 0),
				'CHI_PHI_MUA_HANG': d.get('PHI_HANG_VE_KHO'),
				
				'THUE_GTGT_ID': phan_tram_thue_gtgt_id.id if phan_tram_thue_gtgt_id else None,
				'TIEN_THUE_GTGT': d.get('TIEN_THUE_GTGT'),
				'TIEN_THUE_GTGT_QUY_DOI': tien_thue_gtgt_quy_doi,
				'TK_DU_THUE_GTGT_ID': tkdu_thue_gtgt_id.id if tkdu_thue_gtgt_id else None,
				'TK_THUE_GTGT_ID': tk_thue_gtgt_id.id if tk_thue_gtgt_id else None,
				'NHOM_HHDV_ID': nhom_hhdv_mua_vao_id.id if nhom_hhdv_mua_vao_id else None,
				'PHI_TRUOC_HAI_QUAN': d.get('PHI_TRUOC_HAI_QUAN'),
				'GIA_TINH_THUE_NK': d.get('GIA_TINH_THUE_NHAP_KHAU'),
				'THUE_NK': d.get('PHAN_TRAM_THUE_NK'),
				'TIEN_THUE_NK': d.get('TIEN_THUE_NHAP_KHAU'),
				'TK_THUE_NK_ID': tk_thue_nk_id.id if tk_thue_nk_id else None,
				'THUE_TTDB': d.get('PHAN_TRAM_THUE_TTDB'),
				'TIEN_THUE_TTDB': d.get('TIEN_THUE_TTDB'),
				'TK_THUE_TTDB_ID': tk_thue_ttdb_id.id if tk_thue_ttdb_id else None,
			}]]
			line_number += 1
		if not error:
			for key in dict:
				self.env['purchase.document'].create(dict.get(key))
			return {}

		return {'messages' : error}

	# hàm import excel cho chứng từ mua dịch vụ 
	def import_from_excel_mua_dich_vu(self, import_fields, data):
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
			elif not d.get('MA_DICH_VU'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Mã dịch vụ (*)>  bắt buộc nhập' % (line_number,)})
			elif not d.get('TK_CHI_PHI_KHO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK chi phí/TK kho (*)>  bắt buộc nhập' % (line_number,)})
			elif not d.get('TK_CONG_NO_TIEN'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK công nợ/TK tiền (*)>  bắt buộc nhập' % (line_number,)})
			
			nha_cung_cap_id = None
			nv_mua_hang_id = None
			loai_tien_id = None
			ma_dich_vu_id = None
			tk_chi_phi_kho_id = None
			tk_cong_no_tien_id = None

			doi_tuong_id = None

			don_vi_tinh_id = None
			phan_tram_thue_gtgt_id = None
			tk_thue_gtgt_id = None
			mau_so_hd_id = None
			nhom_hhdv_mua_vao_id = None
			nha_cung_cap_chi_tiet_id = None

			
			if d.get('MA_NHA_CUNG_CAP'):
				nha_cung_cap_id = self.env['res.partner'].search([('MA', '=', d.get('MA_NHA_CUNG_CAP'))], limit=1)
				if not nha_cung_cap_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã nhà cung cấp <%s> trong danh mục nhà cung cấp' % (line_number,d.get('MA_NHA_CUNG_CAP'))})

			if d.get('NV_MUA_HANG'):
				nv_mua_hang_id = self.env['res.partner'].search([('MA', '=', d.get('NV_MUA_HANG'))], limit=1)
				if not nv_mua_hang_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy NV mua hàng <%s> trong danh mục nhân viên' % (line_number,d.get('NV_MUA_HANG'))})

			if d.get('LOAI_TIEN'):
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', d.get('LOAI_TIEN'))], limit=1)
				if not loai_tien_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Loại tiền <%s> trong danh mục loại tiền' % (line_number,d.get('LOAI_TIEN'))})

			if d.get('MA_DICH_VU'):
				ma_dich_vu_id = self.env['danh.muc.vat.tu.hang.hoa'].search([('MA', '=', d.get('MA_DICH_VU'))], limit=1)
				if not ma_dich_vu_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã dịch vụ <%s> trong danh mục vật tư hàng hóa' % (line_number,d.get('MA_DICH_VU'))})
			
			if d.get('MAU_SO_HD'):
				mau_so_hd_id = self.env['danh.muc.mau.so.hd'].search([('MAU_SO_HD', '=', d.get('MAU_SO_HD'))], limit=1)
				if not mau_so_hd_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mẫu số HĐ <%s> trong danh mục mẫu số hóa đơn' % (line_number,d.get('MAU_SO_HD'))})
			
			
			if d.get('TK_CHI_PHI_KHO'):
				tk_chi_phi_kho_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_CHI_PHI_KHO'))], limit=1)
				if not tk_chi_phi_kho_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK chi phí/TK kho (*) <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_CHI_PHI_KHO'))})
			
			if d.get('TK_CONG_NO_TIEN'):
				tk_cong_no_tien_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_CONG_NO_TIEN'))], limit=1)
				if not tk_cong_no_tien_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK công nợ/TK tiền (*) <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_CONG_NO_TIEN'))})

			if d.get('DVT'):
				don_vi_tinh_id = self.env['danh.muc.don.vi.tinh'].search([('DON_VI_TINH', '=', d.get('DVT'))], limit=1)
				if not don_vi_tinh_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy ĐVT <%s> trong danh mục đơn vị tính' % (line_number,d.get('DVT'))})

			if d.get('PHAN_TRAM_THUE_GTGT'):
				phan_tram_thue_gtgt_id = self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', d.get('PHAN_TRAM_THUE_GTGT'))], limit=1)
				if not phan_tram_thue_gtgt_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy phần trăm thuế GTGT <%s> trong danh mục thuế suất giá trị gia tăng' % (line_number,d.get('PHAN_TRAM_THUE_GTGT'))})
			
			
			if d.get('TK_THUE_GTGT'):
				tk_thue_gtgt_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_THUE_GTGT'))], limit=1)
				if not tk_thue_gtgt_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK thuế GTGT <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_THUE_GTGT'))})
			
			if d.get('NHOM_HHDV_MUA_VAO'):
				nhom_hhdv_mua_vao_id = self.env['danh.muc.nhom.hhdv'].search([('MA_NHOM_HHDV', '=', d.get('NHOM_HHDV_MUA_VAO'))], limit=1)
				if not nhom_hhdv_mua_vao_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Nhóm HHDV mua vào <%s> trong danh mục nhóm hàng hóa dịch vụ mua vào' % (line_number,d.get('NHOM_HHDV_MUA_VAO'))})
			
			if d.get('DOI_TUONG'):
				doi_tuong_id = self.env['res.partner'].search([('MA', '=', d.get('DOI_TUONG'))], limit=1)
				if not doi_tuong_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Đối tượng <%s> trong danh mục đối tượng' % (line_number,d.get('DOI_TUONG'))})

			if d.get('MA_NCC'):
				nha_cung_cap_chi_tiet_id = self.env['res.partner'].search([('MA', '=', d.get('MA_NCC'))], limit=1)
				if not nha_cung_cap_chi_tiet_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã NCC <%s> trong danh mục nhà cung cấp' % (line_number,d.get('MA_NCC'))})

			
			#########################
		
			da_thanh_toan = False
			la_cp_mua_hang = False
			loai_thanh_toan = ''
			loai_hoa_don = ''

			so_chung_tu_ghi_no = False
			so_chung_tu_unc = False
			so_chung_tu_phieu_chi = False
			so_chung_tu_sck = False
			so_chung_tu_stm = False

			dien_giai_ghi_no = ''
			noi_dung_thanh_toan = ''
			dien_giai_phieu_chi = ''
			
			if d.get('LA_CP_MUA_HANG') == '0' or d.get('LA_CP_MUA_HANG') == '':
				la_cp_mua_hang = False
			else:
				la_cp_mua_hang = True
		
			# Gán giá trị cho Cột DA_THANH_TOAN và Loại thanh toán
			if d.get('PHUONG_THUC_THANH_TOAN') == '0' or d.get('PHUONG_THUC_THANH_TOAN') == '':
				da_thanh_toan = False
				so_chung_tu_ghi_no = d.get('SO_CHUNG_TU')
				dien_giai_ghi_no = d.get('DIEN_GIAI_LY_DO_CHI_NDTT')

			elif d.get('PHUONG_THUC_THANH_TOAN') == '1':
				da_thanh_toan = True
				loai_thanh_toan = 'tien_mat'
				so_chung_tu_phieu_chi = d.get('SO_CHUNG_TU')
				dien_giai_phieu_chi = d.get('DIEN_GIAI_LY_DO_CHI_NDTT')

			elif d.get('PHUONG_THUC_THANH_TOAN') == '2':
				da_thanh_toan = True
				loai_thanh_toan = 'uy_nhiem_chi'
				so_chung_tu_unc = d.get('SO_CHUNG_TU')
				noi_dung_thanh_toan = d.get('DIEN_GIAI_LY_DO_CHI_NDTT')

			elif d.get('PHUONG_THUC_THANH_TOAN') == '3':
				da_thanh_toan = True
				loai_thanh_toan = 'sec_chuyen_khoan'
				so_chung_tu_sck = d.get('SO_CHUNG_TU')
				noi_dung_thanh_toan = d.get('DIEN_GIAI_LY_DO_CHI_NDTT')
			else:
				da_thanh_toan = True
				loai_thanh_toan = 'sec_tien_mat'
				so_chung_tu_stm = d.get('SO_CHUNG_TU')
				noi_dung_thanh_toan = d.get('DIEN_GIAI_LY_DO_CHI_NDTT')

			# Gán giá trị cho trường LOAI_HOA_DON
			if d.get('NHAN_KEM_HOA_DON') == '0' or d.get('NHAN_KEM_HOA_DON') == '':
				loai_hoa_don = '0'
			elif d.get('NHAN_KEM_HOA_DON') == '1':
				loai_hoa_don = '1'
			else:
				loai_hoa_don = '2'

			key = '_'.join([loai_thanh_toan + str(d.get('SO_CHUNG_TU'))]) # d[0]: Loại nghiệp vụ - d[1]: Số chứng từ
			if key not in dict:
				dict[key] = {
					'DA_THANH_TOAN': da_thanh_toan,
					'LOAI_THANH_TOAN': loai_thanh_toan,
					'LOAI_HOA_DON': loai_hoa_don,
					'LA_CHI_PHI_MUA_HANG': la_cp_mua_hang,
				
					'NGAY_HACH_TOAN': d.get('NGAY_HACH_TOAN'),
					'NGAY_CHUNG_TU': d.get('NGAY_CHUNG_TU'),

					'SO_CHUNG_TU_MUA_HANG':so_chung_tu_ghi_no,
					'SO_UY_NHIEM_CHI': so_chung_tu_unc,
					'SO_PHIEU_CHI': so_chung_tu_phieu_chi,
					'SO_SEC_CHUYEN_KHOAN': so_chung_tu_sck,
					'SO_SEC_TIEN_MAT': so_chung_tu_stm,

					'DOI_TUONG_ID': nha_cung_cap_id.id if nha_cung_cap_id else None,
					'TEN_DOI_TUONG': d.get('TEN_NHA_CUNG_CAP'),
					'DIA_CHI': d.get('DIA_CHI'),

					'DIEN_GIAI':dien_giai_ghi_no,
					'NOI_DUNG_THANH_TOAN': noi_dung_thanh_toan,
					'LY_DO_CHI': dien_giai_phieu_chi,
					'NHAN_VIEN_ID': nv_mua_hang_id.id if nv_mua_hang_id else None,
					'currency_id': loai_tien_id.id if loai_tien_id else None,
					'TY_GIA': d.get('TY_GIA'),
					'CHI_TIET_IDS': []
				}
			dict[key]['CHI_TIET_IDS'] += [[0,0,{
				'MA_HANG_ID': ma_dich_vu_id.id if ma_dich_vu_id else None,
				'name': d.get('TEN_DICH_VU'),
				'TK_NO_ID': tk_chi_phi_kho_id.id if tk_chi_phi_kho_id else None,
				'TK_CO_ID': tk_cong_no_tien_id.id if tk_cong_no_tien_id else None,
				'DOI_TUONG_ID': doi_tuong_id.id if doi_tuong_id else None,
				'DVT_ID': don_vi_tinh_id.id if don_vi_tinh_id else None,
				'SO_LUONG': d.get('SO_LUONG'), 
				'DON_GIA':  d.get('DON_GIA'),
				'THANH_TIEN':  d.get('THANH_TIEN'),
				'THANH_TIEN_QUY_DOI': d.get('THANH_TIEN_QUY_DOI'),
				
				
				'THUE_GTGT_ID': phan_tram_thue_gtgt_id.id if phan_tram_thue_gtgt_id else None,
				'TIEN_THUE_GTGT':  d.get('TIEN_THUE_GTGT'),
				'TIEN_THUE_GTGT_QUY_DOI':  d.get('TIEN_THUE_GTGT_QUY_DOI'),
				'TK_THUE_GTGT_ID': tk_thue_gtgt_id.id if tk_thue_gtgt_id else None,

				'MAU_SO_HD_ID': mau_so_hd_id.id if mau_so_hd_id else None,
				'KY_HIEU_HOA_DON':  d.get('KY_HIEU_HD'),
				'SO_HOA_DON_DETAIL': d.get('SO_HOA_DON'),
				'NGAY_HOA_DON':  d.get('NGAY_HOA_DON'),
				'NHOM_HHDV_ID': nhom_hhdv_mua_vao_id.id if nhom_hhdv_mua_vao_id else None,
				'MA_NCC_ID': nha_cung_cap_chi_tiet_id.id if nha_cung_cap_chi_tiet_id else None,
				'TEN_NCC': d.get('TEN_NCC'),
				'MA_SO_THUE_NCC': d.get('MA_SO_THUE_NCC'),
				'DIA_CHI_NCC': d.get('DIA_CHI_NCC'),
			}]]
			line_number += 1
		if not error:
			for key in dict:
				self.env['purchase.document'].create(dict.get(key))
			return {}

		return {'messages' : error}