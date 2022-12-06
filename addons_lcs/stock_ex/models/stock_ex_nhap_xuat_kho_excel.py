# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError , UserError
from odoo.addons import decimal_precision

class STOCK_EX_NHAP_XUAT_KHO_EXCEL(models.Model):
	_name = 'stock.ex.nhap.xuat.kho.excel'
	_description = 'Nhập xuất kho'
	_auto = False


	LOAI_NHAP_KHO =  fields.Selection([('0', 'Nhập kho thành phẩm sản xuất'), ('1', 'Nhập kho hàng bán trả lại'),('2','Nhập kho khác')],string='Loại nhập kho',default = '2')
	NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán (*)', help='Ngày hạch toán (*)')
	NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ (*)', help='Ngày chứng từ (*)')
	SO_CHUNG_TU = fields.Char(string='Số chứng từ (*)', help='Số chứng từ (*)')

	MA_DOI_TUONG = fields.Char(string='Mã đối tượng', help='Mã đối tượng')
	TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng')
	NGUOI_GIAO_HANG = fields.Char(string='Người giao hàng', help='Người giao hàng')

	DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
	NV_BAN_HANG = fields.Char(string='Nhân viên bán hàng', help='Nhân viên bán hàng')
	KEM_THEO = fields.Char(string='Kèm theo', help='Kèm theo')
	
	MA_HANG = fields.Char(string='Mã hàng (*)', help='Mã hàng (*)')
	TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng')
	KHO = fields.Char(string='Kho (*)', help='Kho (*)')
	TK_NO = fields.Char(string='TK Nợ (*)', help='TK Nợ (*)')
	TK_CO = fields.Char(string='TK Có (*)', help='TK Có (*)')
	DVT = fields.Char(string='ĐVT', help='ĐVT')
	SO_LUONG = fields.Float(string='Số lượng', help='Số lượng')
	DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá')
	THANH_TIEN = fields.Float(string='Thành tiền', help='Thành tiền')
	SO_LO = fields.Char(string='Số lô', help='Số lô')
	HAN_SU_DUNG = fields.Date(string='Hạn sử dụng', help='Hạn sử dụng')
	KHOAN_MUC_CHI_PHI = fields.Char(string='Khoản mục CP', help='Khoản mục CP')
	DON_VI = fields.Char(string='Đơn vị', help='Đơn vị')
	DOI_TUONG_THCP = fields.Char(string='Đối tượng THCP', help='Đối tượng THCP')
	CONG_TRINH = fields.Char(string='Công trình', help='Công trình')
	DON_DAT_HANG = fields.Char(string='Đơn đặt hàng', help='Đơn đặt hàng')
	HOP_DONG_BAN = fields.Char(string='Hợp đồng bán', help='Hợp đồng bán')
	MA_THONG_KE = fields.Char(string='Mã thống kê', help='Mã thống kê')

	LOAI_XUAT_KHO = fields.Selection([('0', 'Xuất kho bán hàng'), ('1', 'Xuất kho sản xuất'),('2','Xuất hàng cho chi nhánh khác'),('3','Xuất khác')],string='Loại xuất kho', default = '0')
	MAU_SO_HD = fields.Char(string='Mẫu số HĐ', help='Mẫu số HĐ')
	KY_HIEU_HD = fields.Char(string='Ký hiệu HĐ', help='Ký hiệu HĐ')
	DIA_CHI_BO_PHAN = fields.Char(string='Địa chỉ/Bộ phận', help='Địa chỉ/Bộ phận')
	TEN_NGUOI_NHAN = fields.Char(string='Tên người nhận/Của', help='Tên người nhận/Của')
	LY_DO_XUAT = fields.Char(string='Lý do xuất/Về việc', help='Lý do xuất/Về việc')
	SO_LENH_DIEU_DONG = fields.Char(string='Số lệnh điều động', help='Số lệnh điều động')
	NGAY_LENH_DIEU_DONG = fields.Date(string='Ngày lệnh điều động', help='Ngày lệnh điều động')
	NGUOI_VAN_CHUYEN = fields.Char(string='Người vận chuyển', help='Người vận chuyển')
	TEN_NGUOI_VAN_CHUYEN = fields.Char(string='Tên người vận chuyển', help='Tên người vận chuyển')
	HOP_DONG_SO = fields.Char(string='Hợp đồng số', help='Hợp đồng số')
	PHUONG_TIEN_VAN_CHUYEN = fields.Selection([('1', 'Ô tô'), ('2', 'Máy bay'),('3','Tàu hỏa'),('4','Giao tay')],string='Phương tiện vận chuyển', default = '1')
	XUAT_TAI_KHO = fields.Char(string='Xuất tại kho', help='Xuất tại kho')
	NHAP_TAI_KHO = fields.Char(string='Nhập tại kho', help='Nhập tại kho')
	DON_GIA_BAN = fields.Float(string='Đơn giá bán', help='Đơn giá bán')
	DON_GIA_VON = fields.Float(string='Đơn giá vốn', help='Đơn giá vốn')
	TIEN_VON = fields.Float(string='Tiền vốn', help='Tiền vốn')
	DOI_TUONG = fields.Char(string='Đối tượng', help='Đối tượng')
	CP_KHONG_HOP_LY = fields.Float(string='CP không hợp lý', help='CP không hợp lý')

	def import_from_excel(self, import_fields, data):
		default_type = self._context.get('default_type')
		result = None
		if default_type == 'NHAP_KHO':
			result = self.import_from_excel_nhap_kho(import_fields, data)
		elif default_type == 'XUAT_KHO':
			result = self.import_from_excel_xuat_kho(import_fields, data)
		elif default_type == 'CHUYEN_KHO':
			result = self.import_from_excel_chuyen_kho(import_fields, data)
		return result
	# Hàm import excel nhập kho
	def import_from_excel_nhap_kho(self, import_fields, data):
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
			elif not d.get('MA_HANG'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Mã hàng>  bắt buộc nhập' % (line_number,)})
			elif not d.get('KHO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Kho (*)>  bắt buộc nhập' % (line_number,)})
			elif not d.get('TK_NO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK Nợ (*)>  bắt buộc nhập' % (line_number,)})
			elif not d.get('TK_CO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK Có (*)>  bắt buộc nhập' % (line_number,)})

			doi_tuong_id = None
			nv_ban_hang_id = None
			
			ma_hang_id = None
			kho_id = None
			tk_no_id = None
			tk_co_id = None
			don_vi_tinh_id = None

			khoan_muc_cp_id = None
			don_vi_id = None
			doi_tuong_thcp_id = None
			cong_trinh_id = None
			don_dat_hang_id = None
			hop_dong_ban_id = None
			ma_thong_ke_id = None

			
			if d.get('MA_DOI_TUONG'):
				doi_tuong_id = self.env['res.partner'].search([('MA', '=', d.get('MA_DOI_TUONG'))], limit=1)
				if not doi_tuong_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã đối tượng <%s> trong danh mục đối tượng' % (line_number,d.get('MA_DOI_TUONG'))})

			if d.get('NV_BAN_HANG'):
				nv_ban_hang_id = self.env['res.partner'].search([('MA', '=', d.get('NV_BAN_HANG'))], limit=1)
				if not nv_ban_hang_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy NV bán hàng <%s> trong danh mục nhân viên' % (line_number,d.get('NV_BAN_HANG'))})

			
			if d.get('MA_HANG'):
				ma_hang_id = self.env['danh.muc.vat.tu.hang.hoa'].search([('MA', '=', d.get('MA_HANG'))], limit=1)
				if not ma_hang_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã hàng <%s> trong danh mục vật tư hàng hóa' % (line_number,d.get('MA_HANG'))})
			
			if d.get('TK_NO'):
				tk_no_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_NO'))], limit=1)
				if not tk_no_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK Tiền/Chi phí/Nợ <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_NO'))})
			
			if d.get('TK_CO'):
				tk_co_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_CO'))], limit=1)
				if not tk_co_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK Doanh thu/Có <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_CO'))})

			if d.get('DVT'):
				don_vi_tinh_id = self.env['danh.muc.don.vi.tinh'].search([('DON_VI_TINH', '=', d.get('DVT'))], limit=1)
				if not don_vi_tinh_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy ĐVT <%s> trong danh mục đơn vị tính' % (line_number,d.get('DVT'))})
			
			if d.get('KHO'):
				kho_id = self.env['danh.muc.kho'].search([('MA_KHO', '=', d.get('KHO'))], limit=1)
				if not kho_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Kho <%s> trong danh mục kho' % (line_number,d.get('KHO'))})
						
			if d.get('DON_VI'):
				don_vi_id = self.env['danh.muc.to.chuc'].search([('MA_DON_VI', '=', d.get('DON_VI'))], limit=1)
				if not don_vi_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Đơn vị <%s> trong danh mục cơ cấu tổ chức' % (line_number,d.get('DON_VI'))})
			
			if d.get('DOI_TUONG_THCP'):
				doi_tuong_thcp_id = self.env['danh.muc.doi.tuong.tap.hop.chi.phi'].search([('MA_DOI_TUONG_THCP', '=', d.get('DOI_TUONG_THCP'))], limit=1)
				if not doi_tuong_thcp_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Đối tượng THCP <%s> trong danh mục đối tượng tập hợp chi phí' % (line_number,d.get('DOI_TUONG_THCP'))})
			
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

			
			if d.get('MA_THONG_KE'):
				ma_thong_ke_id = self.env['danh.muc.ma.thong.ke'].search([('MA_THONG_KE', '=', d.get('MA_THONG_KE'))], limit=1)
				if not ma_thong_ke_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã thống kê <%s> trong danh mục mã thống kê' % (line_number,d.get('MA_THONG_KE'))})
			
			if d.get('KHOAN_MUC_CHI_PHI'):
				khoan_muc_cp_id = self.env['danh.muc.khoan.muc.cp'].search([('MA_KHOAN_MUC_CP', '=', d.get('KHOAN_MUC_CHI_PHI'))], limit=1)
				if not khoan_muc_cp_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy khoản mục chi phí <%s> trong danh mục khoản mục chi phí' % (line_number,d.get('KHOAN_MUC_CHI_PHI'))})
			
			#########################
			loai_nhap_kho = ''
			
			# Gán giá trị cho Cột LOAI_NHAP_KHO
			if d.get('LOAI_NHAP_KHO') == '2' or d.get('LOAI_NHAP_KHO') == '':
				loai_nhap_kho = 'KHAC'
			elif d.get('LOAI_NHAP_KHO') == '0':
				loai_nhap_kho = 'THANH_PHAM'
			elif d.get('LOAI_NHAP_KHO') == '1':
				loai_nhap_kho = 'TRA_LAI'
		
			key = '_'.join([loai_nhap_kho + str(d.get('SO_CHUNG_TU'))]) # d[0]: Loại nghiệp vụ - d[1]: Số chứng từ
			if key not in dict:
				dict[key] = {
					'LOAI_NHAP_KHO': loai_nhap_kho,
					
					'NGAY_HACH_TOAN': d.get('NGAY_HACH_TOAN'),
					'NGAY_CHUNG_TU': d.get('NGAY_CHUNG_TU'),
					'SO_CHUNG_TU': d.get('SO_CHUNG_TU'),
					'DOI_TUONG_ID': doi_tuong_id.id if doi_tuong_id else None,
					'TEN_DOI_TUONG': d.get('TEN_DOI_TUONG'),
					'NGUOI_GIAO_HANG_TEXT': d.get('NGUOI_GIAO_HANG'),
					'DIEN_GIAI': d.get('DIEN_GIAI'),
					'NHAN_VIEN_ID': nv_ban_hang_id.id if nv_ban_hang_id else None,
					'KEM_THEO_CHUNG_TU_GOC': d.get('KEM_THEO'),
					'type': 'NHAP_KHO',
					'CHI_TIET_IDS': []
				}
			dict[key]['CHI_TIET_IDS'] += [[0,0,{
				'MA_HANG_ID': ma_hang_id.id if ma_hang_id else None,
				'TEN_HANG': d.get('TEN_HANG'),
				'KHO_ID': kho_id.id if kho_id else None,
				'TK_NO_ID': tk_no_id.id if tk_no_id else None,
				'TK_CO_ID': tk_co_id.id if tk_co_id else None,
				'DVT_ID': don_vi_tinh_id.id if don_vi_tinh_id else None,
				'SO_LUONG': d.get('SO_LUONG') ,
				'DON_GIA_VON': d.get('DON_GIA'),
				'TIEN_VON': d.get('THANH_TIEN'),
				'SO_LO': d.get('SO_LO'),
				'HAN_SU_DUNG': d.get('HAN_SU_DUNG'),
				'KHOAN_MUC_CP_ID': khoan_muc_cp_id.id if khoan_muc_cp_id else None,
				'DON_VI_ID': don_vi_id.id if don_vi_id else None,
				'DOI_TUONG_THCP_ID': doi_tuong_thcp_id.id if doi_tuong_thcp_id else None,
				'CONG_TRINH_ID': cong_trinh_id.id if cong_trinh_id else None,
				'DON_DAT_HANG_ID': don_dat_hang_id.id if don_dat_hang_id else None,
				'HOP_DONG_BAN_ID': hop_dong_ban_id.id if hop_dong_ban_id else None,
				'MA_THONG_KE_ID': ma_thong_ke_id.id if ma_thong_ke_id else None
				
			}]]
			line_number += 1
		if not error:
			for key in dict:
				self.env['stock.ex.nhap.xuat.kho'].create(dict.get(key))
			return {}

		return {'messages' : error}

	# Hàm import excel xuất kho
	def import_from_excel_xuat_kho(self, import_fields, data):
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
			elif not d.get('MA_HANG'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Mã hàng>  bắt buộc nhập' % (line_number,)})
			elif not d.get('KHO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <Kho (*)>  bắt buộc nhập' % (line_number,)})
			elif not d.get('TK_NO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK Nợ (*)>  bắt buộc nhập' % (line_number,)})
			elif not d.get('TK_CO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK Có (*)>  bắt buộc nhập' % (line_number,)})

			
			doi_tuong_id = None
			nv_ban_hang_id = None
			nguoi_van_chuyen_id = None
			kho_xuat_id = None
			kho_nhap_id = None
			
			ma_hang_id = None
			kho_id = None
			tk_no_id = None
			tk_co_id = None
			don_vi_tinh_id = None

			doi_tuong_chi_tiet_id = None

			khoan_muc_cp_id = None
			don_vi_id = None
			doi_tuong_thcp_id = None
			cong_trinh_id = None
			don_dat_hang_id = None
			hop_dong_ban_id = None
			ma_thong_ke_id = None

			
			if d.get('MA_DOI_TUONG'):
				doi_tuong_id = self.env['res.partner'].search([('MA', '=', d.get('MA_DOI_TUONG'))], limit=1)
				if not doi_tuong_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã đối tượng <%s> trong danh mục đối tượng' % (line_number,d.get('MA_DOI_TUONG'))})

			if d.get('NV_BAN_HANG'):
				nv_ban_hang_id = self.env['res.partner'].search([('MA', '=', d.get('NV_BAN_HANG'))], limit=1)
				if not nv_ban_hang_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy NV bán hàng <%s> trong danh mục nhân viên' % (line_number,d.get('NV_BAN_HANG'))})

			if d.get('NGUOI_VAN_CHUYEN'):
				nguoi_van_chuyen_id = self.env['res.partner'].search([('MA', '=', d.get('NGUOI_VAN_CHUYEN'))], limit=1)
				if not nguoi_van_chuyen_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Người vận chuyển <%s> trong danh mục đối tượng' % (line_number,d.get('NGUOI_VAN_CHUYEN'))})
			
			if d.get('XUAT_TAI_KHO'):
				kho_xuat_id = self.env['danh.muc.kho'].search([('MA_KHO', '=', d.get('XUAT_TAI_KHO'))], limit=1)
				if not kho_xuat_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Kho <%s> trong danh mục kho' % (line_number,d.get('XUAT_TAI_KHO'))})
			
			if d.get('NHAP_TAI_KHO'):
				kho_nhap_id = self.env['danh.muc.kho'].search([('MA_KHO', '=', d.get('NHAP_TAI_KHO'))], limit=1)
				if not kho_nhap_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Kho <%s> trong danh mục kho' % (line_number,d.get('NHAP_TAI_KHO'))})
				
			if d.get('MA_HANG'):
				ma_hang_id = self.env['danh.muc.vat.tu.hang.hoa'].search([('MA', '=', d.get('MA_HANG'))], limit=1)
				if not ma_hang_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã hàng <%s> trong danh mục vật tư hàng hóa' % (line_number,d.get('MA_HANG'))})
			
			if d.get('TK_NO'):
				tk_no_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_NO'))], limit=1)
				if not tk_no_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK Tiền/Chi phí/Nợ <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_NO'))})
			
			if d.get('TK_CO'):
				tk_co_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_CO'))], limit=1)
				if not tk_co_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK Doanh thu/Có <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_CO'))})

			if d.get('DVT'):
				don_vi_tinh_id = self.env['danh.muc.don.vi.tinh'].search([('DON_VI_TINH', '=', d.get('DVT'))], limit=1)
				if not don_vi_tinh_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy ĐVT <%s> trong danh mục đơn vị tính' % (line_number,d.get('DVT'))})
			
			if d.get('KHO'):
				kho_id = self.env['danh.muc.kho'].search([('MA_KHO', '=', d.get('KHO'))], limit=1)
				if not kho_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Kho <%s> trong danh mục kho' % (line_number,d.get('KHO'))})
						
			if d.get('DON_VI'):
				don_vi_id = self.env['danh.muc.to.chuc'].search([('MA_DON_VI', '=', d.get('DON_VI'))], limit=1)
				if not don_vi_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Đơn vị <%s> trong danh mục cơ cấu tổ chức' % (line_number,d.get('DON_VI'))})
			
			if d.get('DOI_TUONG_THCP'):
				doi_tuong_thcp_id = self.env['danh.muc.doi.tuong.tap.hop.chi.phi'].search([('MA_DOI_TUONG_THCP', '=', d.get('DOI_TUONG_THCP'))], limit=1)
				if not doi_tuong_thcp_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Đối tượng THCP <%s> trong danh mục đối tượng tập hợp chi phí' % (line_number,d.get('DOI_TUONG_THCP'))})
			
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

			if d.get('MA_THONG_KE'):
				ma_thong_ke_id = self.env['danh.muc.ma.thong.ke'].search([('MA_THONG_KE', '=', d.get('MA_THONG_KE'))], limit=1)
				if not ma_thong_ke_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã thống kê <%s> trong danh mục mã thống kê' % (line_number,d.get('MA_THONG_KE'))})
			
			if d.get('KHOAN_MUC_CHI_PHI'):
				khoan_muc_cp_id = self.env['danh.muc.khoan.muc.cp'].search([('MA_KHOAN_MUC_CP', '=', d.get('KHOAN_MUC_CHI_PHI'))], limit=1)
				if not khoan_muc_cp_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy khoản mục chi phí <%s> trong danh mục khoản mục chi phí' % (line_number,d.get('KHOAN_MUC_CHI_PHI'))})
			
			if d.get('DOI_TUONG'):
				doi_tuong_chi_tiet_id = self.env['res.partner'].search([('MA', '=', d.get('DOI_TUONG'))], limit=1)
				if not doi_tuong_chi_tiet_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Đối tượng <%s> trong danh mục đối tượng' % (line_number,d.get('DOI_TUONG'))})

			#########################
			loai_xuat_kho = ''
			
			# Gán giá trị cho Cột LOAI_NHAP_KHO
			if d.get('LOAI_XUAT_KHO') == '0' or d.get('LOAI_XUAT_KHO') == '':
				loai_xuat_kho = 'BAN_HANG'
			elif d.get('LOAI_XUAT_KHO') == '1':
				loai_xuat_kho = 'SAN_XUAT'
			elif d.get('LOAI_XUAT_KHO') == '2':
				loai_xuat_kho = 'XUAT_HANG'
			elif d.get('LOAI_XUAT_KHO') == '3':
				loai_xuat_kho = 'KHAC'
			
			phuong_tien_van_chuyen = ''
			if d.get('PHUONG_TIEN_VAN_CHUYEN') == '1' or d.get('PHUONG_TIEN_VAN_CHUYEN') == '':
				phuong_tien_van_chuyen = 'O_TO'
			elif d.get('PHUONG_TIEN_VAN_CHUYEN') == '2':
				phuong_tien_van_chuyen = 'MAY_BAY'
			elif d.get('PHUONG_TIEN_VAN_CHUYEN') == '3':
				phuong_tien_van_chuyen = 'TAU_HOA'
			elif d.get('PHUONG_TIEN_VAN_CHUYEN') == '4':
				phuong_tien_van_chuyen = 'GIAO_TAY'
			

			key = '_'.join([loai_xuat_kho + str(d.get('SO_CHUNG_TU'))]) # d[0]: Loại nghiệp vụ - d[1]: Số chứng từ
			if key not in dict:
				dict[key] = {
					'LOAI_XUAT_KHO': loai_xuat_kho,
					'NGAY_HACH_TOAN': d.get('NGAY_HACH_TOAN'),
					'NGAY_CHUNG_TU': d.get('NGAY_CHUNG_TU'),
					'SO_CHUNG_TU': d.get('SO_CHUNG_TU'),
					'MAU_SO': d.get('MAU_SO_HD'),
					'KY_HIEU': d.get('KY_HIEU_HD'),
					'DOI_TUONG_ID': doi_tuong_id.id if doi_tuong_id else None,
					'TEN_DOI_TUONG': d.get('TEN_DOI_TUONG'),
					'DIA_CHI': d.get('DIA_CHI_BO_PHAN'),
					'NGUOI_NHAN_TEXT': d.get('TEN_NGUOI_NHAN'),
					'LY_DO_XUAT': d.get('LY_DO_XUAT'),
					'NHAN_VIEN_ID': nv_ban_hang_id.id if nv_ban_hang_id else None,
					'KEM_THEO_CHUNG_TU_GOC': d.get('KEM_THEO'),
					'LENH_DIEU_DONG_SO': d.get('SO_LENH_DIEU_DONG'),
					'NGAY': d.get('NGAY_LENH_DIEU_DONG'),
					'NGUOI_VAN_CHUYEN_ID':  nguoi_van_chuyen_id.id if nguoi_van_chuyen_id else None,
					'TEN_NGUOI_VAN_CHUYEN': d.get('TEN_NGUOI_VAN_CHUYEN'),
					'HOP_DONG_SO': d.get('HOP_DONG_SO'),
					'PHUONG_TIEN': phuong_tien_van_chuyen,
					'XUAT_TAI_KHO_ID': kho_xuat_id.id if kho_xuat_id else None,
					'NHAP_TAI_KHO_ID': kho_nhap_id.id if kho_nhap_id else None,
					'type': 'XUAT_KHO',

					'CHI_TIET_IDS': []
				}
			dict[key]['CHI_TIET_IDS'] += [[0,0,{
				'MA_HANG_ID': ma_hang_id.id if ma_hang_id else None,
				'TEN_HANG': d.get('TEN_HANG'),
				'KHO_ID': kho_id.id if kho_id else None,
				'TK_NO_ID': tk_no_id.id if tk_no_id else None,
				'TK_CO_ID': tk_co_id.id if tk_co_id else None,
				'DVT_ID': don_vi_tinh_id.id if don_vi_tinh_id else None,
				'SO_LUONG': d.get('SO_LUONG') ,
				'DON_GIA': d.get('DON_GIA_BAN'),
				'THANH_TIEN': d.get('THANH_TIEN'),
				'DON_GIA_VON': d.get('DON_GIA_VON'),
				'TIEN_VON': d.get('TIEN_VON'),
				'SO_LO': d.get('SO_LO'),
				'HAN_SU_DUNG': d.get('HAN_SU_DUNG'),
				'KHOAN_MUC_CP_ID': khoan_muc_cp_id.id if khoan_muc_cp_id else None,
				'DOI_TUONG_ID': doi_tuong_chi_tiet_id.id if doi_tuong_chi_tiet_id else None,
				'DON_VI_ID': don_vi_id.id if don_vi_id else None,
				'DOI_TUONG_THCP_ID': doi_tuong_thcp_id.id if doi_tuong_thcp_id else None,
				'CONG_TRINH_ID': cong_trinh_id.id if cong_trinh_id else None,
				'DON_DAT_HANG_ID': don_dat_hang_id.id if don_dat_hang_id else None,
				'HOP_DONG_BAN_ID': hop_dong_ban_id.id if hop_dong_ban_id else None,
				'MA_THONG_KE_ID': ma_thong_ke_id.id if ma_thong_ke_id else None
				
			}]]
			line_number += 1
		if not error:
			for key in dict:
				self.env['stock.ex.nhap.xuat.kho'].create(dict.get(key))
			return {}

		return {'messages' : error}

	# Hàm import excel chuyển kho
	def import_from_excel_chuyen_kho(self, import_fields, data):
		return {}