# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError , UserError
from odoo.addons import decimal_precision

class SALE_DOCUMENT_EXCEL(models.Model):
	_name = 'sale.document.excel'
	_description = 'Chứng từ bán hàng'
	_auto = False


	HINH_THUC_BAN_HANG = fields.Selection([('0', 'Bán hàng hóa dịch vụ trong nước'), ('1', 'Bán hàng xuất khẩu'), ('2', 'Báng hàng đại lý bán đúng giá'),('3', 'Bán hàng ủy thác xuất khẩu')],string='Hình thức bán hàng',default = '0')
	PHUONG_THUC_THANH_TOAN = fields.Selection([('0', 'Chưa thu tiền'), ('1', 'Thu tiền ngay - Tiền mặt'), ('2', 'Thu tiền ngay - chuyển khoản')],string='Phương thức thanh toán', default = '0')
	KIEM_PHIEU_XUAT_KHO = fields.Selection([('0', 'Không kiêm phiếu xuất kho'), ('1', 'Kiêm phiếu xuất kho')],string='Kiêm phiếu xuất kho', default = '1')
	LAP_KEM_HOA_DON = fields.Selection([('0', 'Không lập kèm hóa đơn'), ('1', 'Lập kèm hóa đơn')],string='Lập kèm hóa đơn',default = '1')
	DA_LAP_HOA_DON = fields.Selection([('0', 'Chưa lập hóa đơn'), ('1', 'Đã lập hóa đơn')],string='Đã lập hóa đơn' ,default = '0')

	NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán (*)', help='Ngày hạch toán (*)')
	NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ (*)', help='Ngày chứng từ (*)')
	SO_CHUNG_TU = fields.Char(string='Số chứng từ (*)', help='Số chứng từ (*)')
	SO_PHIEU_XUAT = fields.Char(string='Số phiếu xuất', help='Số phiếu xuất')
	LY_DO_XUAT = fields.Char(string='Lý do xuất', help='Lý do xuất')
	MAU_SO_HD = fields.Char(string='Mẫu số HĐ', help='Mẫu số HĐ')
	KY_HIEU_HD = fields.Char(string='Ký hiệu HĐ', help='Ký hiệu HĐ')
	SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
	NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')

	MA_KHACH_HANG = fields.Char(string='Mã khách hàng', help='Mã khách hàng')
	TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
	DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
	MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
	DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
	NOP_VAO_TAI_KHOAN = fields.Char(string='Nộp vào TK', help='Nộp vào TK')
	NV_BAN_HANG = fields.Char(string='NV bán hàng', help='NV bán hàng')
	LOAI_TIEN = fields.Char(string='Loại tiền', help='Loại tiền')
	TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá' ,default = 1)

	MA_HANG = fields.Char(string='Mã hàng (*)', help='Mã hàng (*)')
	TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng')
	HANG_KHUYEN_MAI = fields.Selection([('0', 'Không là hàng khuyến mãi'), ('1', 'là hàng khuyến mãi')],string='Hàng khuyến mại', default = '0')
	TK_NO = fields.Char(string='TK Tiền/Chi phí/Nợ (*)', help='TK Tiền/Chi phí/Nợ (*)')
	TK_CO = fields.Char(string='TK Doanh thu/Có (*)', help='TK Doanh thu/Có (*)')
	DVT = fields.Char(string='ĐVT', help='ĐVT')
	SO_LUONG = fields.Float(string='Số lượng', help='Số lượng')
	DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá')
	THANH_TIEN = fields.Float(string='Thành tiền', help='Thành tiền')
	THANH_TIEN_QUY_DOI = fields.Float(string='Thành tiền quy đổi', help='Thành tiền quy đổi')
	TY_LE_CK = fields.Float(string='Tỷ lệ CK (%)', help='Tỷ lệ CK (%)')
	TIEN_CHIET_KHAU = fields.Float(string='Tiền chiết khấu', help='Tiền chiết khấu')
	TIEN_CHIET_KHAU_QUY_DOI = fields.Float(string='Tiền chiết khấu quy đổi', help='Tiền chiết khấu quy đổi')
	TK_CHIET_KHAU = fields.Char(string='TK chiết khấu', help='TK chiết khấu')
	GIA_TINH_THUE_XUAT_KHAU = fields.Float(string='Giá tính thuế XK', help='Giá tính thuế XK')
	PHAN_TRAM_THUE_XK = fields.Float(string='% thuế XK', help='% thuế XK')
	TIEN_THUE_XUAT_KHAU = fields.Float(string='Tiền thuế XK', help='Tiền thuế XK')
	TK_THUE_XK = fields.Char(string='TK thuế XK', help='TK thuế XK')
	PHAN_TRAM_THUE_GTGT = fields.Char(string='% thuế GTGT', help='% thuế GTGT')
	TIEN_THUE_GTGT = fields.Float(string='Tiền thuế GTGT', help='Tiền thuế GTGT')
	TIEN_THUE_GTGT_QUY_DOI = fields.Float(string='Tiền thuế GTGT quy đổi', help='Tiền thuế GTGT quy đổi')
	TK_THUE_GTGT = fields.Char(string='TK thuế GTGT', help='TK thuế GTGT')
	KHO = fields.Char(string='Kho', help='Kho')
	TK_GIA_VON = fields.Char(string='TK giá vốn', help='TK giá vốn')
	TK_KHO = fields.Char(string='TK Kho', help='TK Kho')
	DON_GIA_VON = fields.Float(string='Đơn giá vốn', help='Đơn giá vốn')
	TIEN_VON = fields.Float(string='Tiền vốn', help='Tiền vốn')


	def import_from_excel(self, import_fields, data):
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
			elif not d.get('TK_NO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK Tiền/Chi phí/Nợ>  bắt buộc nhập' % (line_number,)})
			elif not d.get('TK_CO'):
				error.append({'type':'error', 'message' : 'Dòng thứ %s: Cột <TK Doanh thu/Có>  bắt buộc nhập' % (line_number,)})

			mau_so_hd_id = None
			khach_hang_id = None
			nv_ban_hang_id = None
			loai_tien_id = None
			ma_hang_id = None
			tk_no_id = None
			tk_co_id = None
			don_vi_tinh_id = None
			tk_chiet_khau_id = None
			tk_thue_xk_id = None
			phan_tram_thue_gtgt_id = None
			tk_thue_gtgt_id = None
			tk_kho_id = None
			kho_id = None
			tk_gia_von_id = None
			tk_ngan_hang_id = None

			if d.get('MAU_SO_HD'):
				mau_so_hd_id = self.env['danh.muc.mau.so.hd'].search([('MAU_SO_HD', '=', d.get('MAU_SO_HD'))], limit=1)
				if not mau_so_hd_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mẫu số HĐ <%s> trong danh mục mẫu số hóa đơn' % (line_number,d.get('MAU_SO_HD'))})
			
			if d.get('MA_KHACH_HANG'):
				khach_hang_id = self.env['res.partner'].search([('MA', '=', d.get('MA_KHACH_HANG'))], limit=1)
				if not khach_hang_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Mã khách hàng <%s> trong danh mục khách hàng' % (line_number,d.get('MA_KHACH_HANG'))})

			if d.get('NV_BAN_HANG'):
				nv_ban_hang_id = self.env['res.partner'].search([('MA', '=', d.get('NV_BAN_HANG'))], limit=1)
				if not nv_ban_hang_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy NV bán hàng <%s> trong danh mục nhân viên' % (line_number,d.get('NV_BAN_HANG'))})

			if d.get('LOAI_TIEN'):
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', d.get('LOAI_TIEN'))], limit=1)
				if not loai_tien_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Loại tiền <%s> trong danh mục loại tiền' % (line_number,d.get('LOAI_TIEN'))})

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
			if d.get('TK_CHIET_KHAU'):
				tk_chiet_khau_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_CHIET_KHAU'))], limit=1)
				if not tk_chiet_khau_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK chiết khấu <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_CHIET_KHAU'))})

			if d.get('TK_THUE_XK'):
				tk_thue_xk_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_THUE_XK'))], limit=1)
				if not tk_thue_xk_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK thuế XK <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_THUE_XK'))})
			
			if d.get('PHAN_TRAM_THUE_GTGT'):
				phan_tram_thue_gtgt_id = self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', d.get('PHAN_TRAM_THUE_GTGT'))], limit=1)
				if not phan_tram_thue_gtgt_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy phần trăm thuế GTGT <%s> trong danh mục thuế suất giá trị gia tăng' % (line_number,d.get('PHAN_TRAM_THUE_GTGT'))})
			
			if d.get('TK_THUE_GTGT'):
				tk_thue_gtgt_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_THUE_GTGT'))], limit=1)
				if not tk_thue_gtgt_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK thuế GTGT <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_THUE_GTGT'))})
			
			if d.get('KHO'):
				kho_id = self.env['danh.muc.kho'].search([('MA_KHO', '=', d.get('KHO'))], limit=1)
				if not kho_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy Kho <%s> trong danh mục kho' % (line_number,d.get('KHO'))})
    					
			
			if d.get('TK_GIA_VON'):
				tk_gia_von_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_GIA_VON'))], limit=1)
				if not tk_gia_von_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK giá vốn <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_GIA_VON'))})

			if d.get('TK_KHO'):
				tk_kho_id = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', d.get('TK_KHO'))], limit=1)
				if not tk_kho_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy TK Kho <%s> trong danh mục hệ thống tài khoản' % (line_number,d.get('TK_KHO'))})


			if d.get('NOP_VAO_TAI_KHOAN'):
				tk_ngan_hang_id = self.env['danh.muc.tai.khoan.ngan.hang'].search([('SO_TAI_KHOAN', '=', d.get('NOP_VAO_TAI_KHOAN'))], limit=1)
				if not tk_ngan_hang_id:
					error.append({'type':'error', 'message' : 'Dòng thứ %s: Không tìm thấy số tài khoản <%s> trong danh mục tài khoản ngân hàng' % (line_number,d.get('NOP_VAO_TAI_KHOAN'))}) 
			
			#########################
			hinh_thuc_ban_hang = ''
			thu_tien_ngay = False
			loai_thanh_toan = ''
			kiem_phieu_xuat_kho = False
			lap_kem_hoa_don = False
			da_lap_hoa_don = False

			# Gán giá trị cho Cột Loại nghiệp vụ 
			if d.get('HINH_THUC_BAN_HANG') == '0' or d.get('HINH_THUC_BAN_HANG') == '':
				hinh_thuc_ban_hang = 'TRONG_NUOC'
			elif d.get('HINH_THUC_BAN_HANG') == '1':
				hinh_thuc_ban_hang = 'XUAT_KHAU'
			elif d.get('HINH_THUC_BAN_HANG') == '2':
				hinh_thuc_ban_hang = 'DAI_LY'
			elif d.get('HINH_THUC_BAN_HANG') == '3':
				hinh_thuc_ban_hang = 'UY_THAC'
			
			# Gán giá trị cho Cột Thu tiền ngay và Loại thanh toán
			if d.get('PHUONG_THUC_THANH_TOAN') == '0' or d.get('PHUONG_THUC_THANH_TOAN') == '':
				thu_tien_ngay = False
			elif d.get('PHUONG_THUC_THANH_TOAN') == '1':
				thu_tien_ngay = True
				loai_thanh_toan = 'TIEN_MAT'
			elif d.get('PHUONG_THUC_THANH_TOAN') == '2':
				thu_tien_ngay = True
				loai_thanh_toan = 'CHUYEN_KHOAN'

			# Gán giá trị cho trường KIEM_PHIEU_NHAP_XUAT_KHO
			if d.get('KIEM_PHIEU_XUAT_KHO') == '1' or d.get('KIEM_PHIEU_XUAT_KHO') == '':
				kiem_phieu_xuat_kho = True
			elif d.get('KIEM_PHIEU_XUAT_KHO') == '0':
				kiem_phieu_xuat_kho = False
			
			# Gán giá trị cho trường LAP_KEM_HOA_DON
			if d.get('LAP_KEM_HOA_DON') == '1' or d.get('LAP_KEM_HOA_DON') == '':
				lap_kem_hoa_don = True
			elif d.get('LAP_KEM_HOA_DON') == '0':
				lap_kem_hoa_don = False

			# Gán giá trị cho trường DA_LAP_HOA_DON
			if d.get('DA_LAP_HOA_DON') == '0' or d.get('DA_LAP_HOA_DON') == '':
				da_lap_hoa_don = False
			elif d.get('DA_LAP_HOA_DON') == '1':
				da_lap_hoa_don = True
			
			# Gán giá trị cho trường LA_HANG_KHUYEN_MAI ở detail
			la_hang_khuyen_mai = False
			if d.get('HANG_KHUYEN_MAI') == '0' or d.get('HANG_KHUYEN_MAI') == '':
				la_hang_khuyen_mai = False
			elif d.get('HANG_KHUYEN_MAI') == '1':
				la_hang_khuyen_mai = True

			key = '_'.join([hinh_thuc_ban_hang + str(d.get('SO_CHUNG_TU'))]) # d[0]: Loại nghiệp vụ - d[1]: Số chứng từ
			so_chung_tu_col = 'SO_CHUNG_TU_GHI_NO'
			if thu_tien_ngay:
				if loai_thanh_toan == 'CHUYEN_KHOAN':
					so_chung_tu_col = 'SO_CHUNG_TU_PHIEU_THU_CHUYEN_KHOAN'
				else:
					so_chung_tu_col = 'SO_CHUNG_TU_PHIEU_THU_TIEN_MAT'
			if key not in dict:
				dict[key] = {
					'LOAI_NGHIEP_VU': hinh_thuc_ban_hang,
					'THU_TIEN_NGAY': thu_tien_ngay,
					'LOAI_THANH_TOAN': loai_thanh_toan,
					'KIEM_PHIEU_NHAP_XUAT_KHO': kiem_phieu_xuat_kho,
					'LAP_KEM_HOA_DON': lap_kem_hoa_don,
					'DA_LAP_HOA_DON': da_lap_hoa_don,

					'NGAY_HACH_TOAN': d.get('NGAY_HACH_TOAN'),
					'NGAY_CHUNG_TU': d.get('NGAY_CHUNG_TU'),
					so_chung_tu_col: d.get('SO_CHUNG_TU'),
					'SO_CHUNG_TU_PHIEU_XUAT': d.get('SO_PHIEU_XUAT'),
					'LY_DO_NHAP_XUAT': d.get('LY_DO_XUAT'),
					'MAU_SO_HD_ID': mau_so_hd_id.id if mau_so_hd_id else None,
					'KY_HIEU_HD': d.get('KY_HIEU_HD'),
					'SO_HOA_DON': d.get('SO_HOA_DON'),
					'NGAY_HOA_DON': d.get('NGAY_HOA_DON'),

					'DOI_TUONG_ID': khach_hang_id.id if khach_hang_id else None,
					'TEN_KHACH_HANG': d.get('TEN_KHACH_HANG'),
					'DIA_CHI': d.get('DIA_CHI'),
					'MA_SO_THUE': d.get('MA_SO_THUE'),
					'DIEN_GIAI': d.get('DIEN_GIAI'),
					'NOP_VAO_TK_ID': tk_ngan_hang_id.id if tk_ngan_hang_id else None, 
					'NHAN_VIEN_ID': nv_ban_hang_id.id if nv_ban_hang_id else None,
					'currency_id': loai_tien_id.id if loai_tien_id else None,
					'TY_GIA': d.get('TY_GIA'),
					'SALE_DOCUMENT_LINE_IDS': []
				}
			dict[key]['SALE_DOCUMENT_LINE_IDS'] += [[0,0,{
				'MA_HANG_ID': ma_hang_id.id if ma_hang_id else None,
				'TEN_HANG': d.get('TEN_HANG'),
				'LA_HANG_KHUYEN_MAI': la_hang_khuyen_mai,
				'TK_NO_ID': tk_no_id.id if tk_no_id else None,
				'TK_CO_ID': tk_co_id.id if tk_co_id else None,
				'DVT_ID': don_vi_tinh_id.id if don_vi_tinh_id else None,
				'SO_LUONG': d.get('SO_LUONG') ,
				'DON_GIA': d.get('DON_GIA'),
				'THANH_TIEN': d.get('THANH_TIEN'),
				'THANH_TIEN_QUY_DOI': d.get('THANH_TIEN_QUY_DOI'),
				'TY_LE_CK': d.get('TY_LE_CK'),
				'TIEN_CHIET_KHAU': d.get('TIEN_CHIET_KHAU'),
				'TIEN_CK_QUY_DOI': d.get('TIEN_CHIET_KHAU_QUY_DOI'),
				'TK_CHIET_KHAU_ID': tk_chiet_khau_id.id if tk_chiet_khau_id else None,
				'GIA_TINH_THUE_XK': d.get('GIA_TINH_THUE_XUAT_KHAU'),
				'THUE_XUAT_KHAU': d.get('PHAN_TRAM_THUE_XK'),
				'TIEN_THUE_XUAT_KHAU': d.get('TIEN_THUE_XUAT_KHAU'),
				'TK_THUE_XK_ID': tk_thue_xk_id.id if tk_thue_xk_id else None,
				'THUE_GTGT_ID': phan_tram_thue_gtgt_id.id if phan_tram_thue_gtgt_id else None,
				'TIEN_THUE_GTGT': d.get('TIEN_THUE_GTGT'),
				'TIEN_THUE_GTGT_QUY_DOI': d.get('TIEN_THUE_GTGT_QUY_DOI'),
				'TK_THUE_GTGT_ID': tk_thue_gtgt_id.id if tk_thue_gtgt_id else None,
				'DON_GIA_VON': d.get('DON_GIA_VON'),
				'TIEN_VON': d.get('TIEN_VON'),
			}]]
			line_number += 1
		if not error:
			for key in dict:
				self.env['sale.document'].create(dict.get(key))
			return {}

		return {'messages' : error}