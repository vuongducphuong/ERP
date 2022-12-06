# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime

class ACCOUNT_EX_CONG_NO_KHACH_HANG_EXCEL(models.Model):
	_name = 'cong.no.khach.hang'
	_description = ''
	_auto = False

	SO_TAI_KHOAN = fields.Char(string='Số tài khoản (*)', help='Số tài khoản (*)')
	MA_KHACH_HANG = fields.Char(string='Mã khách hàng (*)', help='Mã khách hàng (*)')
	currency_id = fields.Many2one('res.currency', string='Loại tiền')
	NHAN_VIEN = fields.Char(string='Nhân viên', help='Nhân viên')
	DON_VI = fields.Char(string='Đơn vị', help='Đơn vị')
	CONG_TRINH = fields.Char(string='Công trình', help='Công trình')
	DON_DAT_HANG = fields.Char(string='Đơn đặt hàng', help='Đơn đặt hàng')
	HOP_DONG_BAN = fields.Char(string='Hợp đồng bán', help='Hợp đồng bán')
	DU_NO = fields.Float(string='Dư Nợ quy đổi', help='Dư Nợ quy đổi')
	DU_CO = fields.Float(string='Dư Có quy đổi', help='Dư Có quy đổi')
	DU_NO_NGUYEN_TE = fields.Float(string='Dư Nợ', help='Dư Nợ')
	DU_CO_NGUYEN_TE = fields.Float(string='Dư Có', help='Dư Có')
	
	NGAY_HOA_DON_CHUNG_TU = fields.Date(string='Ngày hóa đơn/chứng từ', help='Ngày hóa đơn/chứng từ')
	SO_HOA_DON_CHUNG_TU = fields.Char(string='Số hóa đơn/chứng từ', help='Số hóa đơn/chứng từ')
	HAN_THANH_TOAN = fields.Date(string='Hạn thanh toán', help='Hạn thanh toán')
	TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
	GIA_TRI_HOA_DON = fields.Float(string='Giá trị hóa đơn', help='Giá trị hóa đơn')
	GIA_TRI_HOA_DON_QUY_DOI = fields.Float(string='GT hóa đơn quy đổi', help='GT hóa đơn quy đổi')
	SO_CON_PHAI_TRA = fields.Float(string='Số còn phải thu', help='Số còn phải thu')
	SO_CON_PHAI_TRA_QUY_DOI = fields.Float(string='Số còn phải thu quy đổi', help='Số còn phải thu quy đổi')
	SO_TRA_TRUOC = fields.Float(string='Số thu trước', help='Số thu trước')
	SO_TRA_TRUOC_QUY_DOI = fields.Float(string='Số thu trước quy đổi', help='Số thu trước quy đổi')
	NHAN_VIEN_HOA_DON = fields.Char(string='Nhân viên (Hóa đơn)', help='Nhân viên (Hóa đơn)')
	
	# TEN_NHA_CUNG_CAP = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
	# HOP_DONG_BAN = fields.Char(string='Hợp đồng bán', help='Hợp đồng bán')


	def import_from_excel(self, import_fields, data):

		data_field = []
		for row in data:
			j = 0
			row_field = {}
			for field in import_fields:
				row_field[field] = row[j]
				j += 1
			data_field.append(row_field)

		dict_create = {}
		error = []
		arr_excel = []
		du_lieu_trong_dtb = self.env['account.ex.so.du.tai.khoan.chi.tiet'].search([])
		i = 0
		# Tính ngày hạch toán
		ngay_hach_toan_str = False
		ngay_bat_dau_nam_tai_chinh = self.env['ir.config_parameter'].get_param('he_thong.TU_NGAY_BAT_DAU_TAI_CHINH')
		if ngay_bat_dau_nam_tai_chinh:
			ngay_bat_dau_nam_tai_chinh_date = datetime.strptime(ngay_bat_dau_nam_tai_chinh, '%Y-%m-%d').date()
			ngay_hach_toan = ngay_bat_dau_nam_tai_chinh_date + timedelta(days=-1)
			ngay_hach_toan_str = ngay_hach_toan.strftime('%Y-%m-%d')

        # 1. trường hợp import thông thuwongf, gọi vào hàm load()
		for data in data_field:
			

			i += 1

			# Số tài khoản
			tai_khoan = False
			if data.get('SO_TAI_KHOAN') != '':
				tk = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', data.get('SO_TAI_KHOAN'))])
				if tk:
					tai_khoan = tk.id
				else:
					thong_bao = u'Cột Số tài khoản dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/Hệ thống tài khoản'
					error.append({'type':'error', 'message' : thong_bao})
			else:
				thong_bao = u'Cột Số tài khoản dòng thứ ' + str(i) + u' là trường bắt buộc nhập vui long nhập để import'
				error.append({'type':'error', 'message' : thong_bao})

			# Mã khách hàng
			doi_tuong = False
			ten_doi_tuong = False
			if data.get('MA_KHACH_HANG') != '':
				dt = self.env['res.partner'].search([('MA', '=', data.get('MA_KHACH_HANG'))])
				if dt:
					doi_tuong = dt.id
					ten_doi_tuong = dt.HO_VA_TEN
					if dt.LA_KHACH_HANG == False:
						thong_bao = u'Cột Mã khách hàng (*) dòng thứ ' + str(i) + u' không tìm thấy ' + str(data.get('MA_NHA_CUNG_CAP')) + ' trong danh mục/khách hàng. Vui lòng kiểm tra lại'
						error.append({'type':'error', 'message' : thong_bao})
				else:
					thong_bao = u'Cột Mã khách hàng (*) dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/khách hàng'
					error.append({'type':'error', 'message' : thong_bao})
			else:
				thong_bao = u'Cột Mã khách hàng (*) thứ ' + str(i) + u' là trường bắt buộc nhập vui long nhập để import'
				error.append({'type':'error', 'message' : thong_bao})
			# Loại tiền
			loai_tien = False
			tien_vnd = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'VND')],limit=1)
			loai_tien = tien_vnd.id
			ma_loai_tien = tien_vnd.MA_LOAI_TIEN
			ty_gia = 1
			if data.get('currency_id') != '':
				tien = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', data.get('currency_id'))])
				if tien:
					loai_tien = tien.id
					ty_gia = tien.TY_GIA_QUY_DOI
					ma_loai_tien = tien.MA_LOAI_TIEN
				else:
					thong_bao = u'cột loại tiền dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/loại tiền'
					error.append({'type':'error', 'message' : thong_bao})
			
			# Nhân viên
			nhan_vien = False
			if data.get('NHAN_VIEN') != '':
				dt = self.env['res.partner'].search([('MA', '=', data.get('NHAN_VIEN'))])
				if dt:
					nhan_vien = dt.id
				else:
					thong_bao = u'Cột Mã nhân viên dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/nhân viên'
					error.append({'type':'error', 'message' : thong_bao})

			# Đơn vị
			don_vi = False
			if data.get('DON_VI') != '':
				tc = self.env['danh.muc.to.chuc'].search([('MA_DON_VI', '=', data.get('DON_VI'))])
				if tc:
					don_vi = tc.id
				else:
					thong_bao = u'Cột Công trình dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/công trình'
					error.append({'type':'error', 'message' : thong_bao})
			
			# Công trình
			cong_trinh = False
			if data.get('CONG_TRINH') != '':
				ct = self.env['danh.muc.cong.trinh'].search([('MA_CONG_TRINH', '=', data.get('CONG_TRINH'))])
				if ct:
					cong_trinh = ct.id
				else:
					thong_bao = u'Cột Công trình dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/công trình'
					error.append({'type':'error', 'message' : thong_bao})

			# Đơn đặt hàng
			don_dat_hang = False
			if data.get('DON_DAT_HANG') != '':
				ddh = self.env['account.ex.don.dat.hang'].search([('SO_DON_HANG', '=', data.get('DON_DAT_HANG'))])
				if ddh:
					don_dat_hang = ddh.id
				else:
					thong_bao = u'Cột đơn đặt hàng dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/đơn đặt hàng'
					error.append({'type':'error', 'message' : thong_bao})

			# Hợp đồng bán
			hop_dong_ban = False
			if data.get('HOP_DONG_BAN') != '':
				hdb = self.env['sale.ex.hop.dong.ban'].search([('SO_HOP_DONG', '=', data.get('HOP_DONG_BAN'))])
				if hdb:
					hop_dong_ban = hdb.id
				else:
					thong_bao = u'Cột Hợp đồng bán dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/Hợp đồng bán'
					error.append({'type':'error', 'message' : thong_bao})

			# Nhân viên hóa đơn
			nhan_vien_hoa_don = False
			if data.get('NHAN_VIEN_HOA_DON') != '':
				dt_hd = self.env['res.partner'].search([('MA', '=', data.get('NHAN_VIEN_HOA_DON'))])
				if dt_hd:
					nhan_vien_hoa_don = dt_hd.id
				else:
					thong_bao = u'Cột Mã nhân viên hóa đơn dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/nhân viên'
					error.append({'type':'error', 'message' : thong_bao})

			# validate
			ty_gia_chi_tiet = 0
			if data.get('SO_TRA_TRUOC') != '' and data.get('SO_TRA_TRUOC_QUY_DOI') != '':
				if float(data.get('SO_TRA_TRUOC')) != 0 and float(data.get('SO_TRA_TRUOC_QUY_DOI')) != 0:
					ty_gia_chi_tiet = float(data.get('SO_TRA_TRUOC_QUY_DOI'))/float(data.get('SO_TRA_TRUOC'))
			
			if data.get('SO_CON_PHAI_TRA_QUY_DOI') != '' and data.get('SO_CON_PHAI_TRA') != '':
				if (float(data.get('SO_CON_PHAI_TRA_QUY_DOI')) != 0 and float(data.get('SO_CON_PHAI_TRA')) != 0) and ty_gia_chi_tiet == 0:
					ty_gia_chi_tiet = float(data.get('SO_CON_PHAI_TRA_QUY_DOI'))/float(data.get('SO_CON_PHAI_TRA'))

				if data.get('GIA_TRI_HOA_DON_QUY_DOI') != '' and data.get('GIA_TRI_HOA_DON') != '':
					if float(data.get('GIA_TRI_HOA_DON_QUY_DOI')) != 0 and float(data.get('GIA_TRI_HOA_DON')) != 0:
						if float(data.get('GIA_TRI_HOA_DON_QUY_DOI'))/float(data.get('GIA_TRI_HOA_DON')) != ty_gia_chi_tiet:
							thong_bao = u'Tỷ giá chuyển đổi của cột giá trị hóa đơn và số còn phải trả dòng ' + str(i) + ' khác nhau vui lòng kiểm tra lại'
							error.append({'type':'error', 'message' : thong_bao})

			if data.get('SO_TRA_TRUOC') != '' and data.get('SO_TRA_TRUOC_QUY_DOI') != ''\
					and data.get('SO_CON_PHAI_TRA_QUY_DOI') != '' and data.get('SO_CON_PHAI_TRA') != ''\
					and data.get('GIA_TRI_HOA_DON_QUY_DOI') != '' and data.get('GIA_TRI_HOA_DON') != '':
				if (float(data.get('SO_TRA_TRUOC')) != 0 or float(data.get('SO_TRA_TRUOC_QUY_DOI')) != 0)\
						and ((float(data.get('SO_CON_PHAI_TRA_QUY_DOI')) != 0 and float(data.get('SO_CON_PHAI_TRA')) != 0)\
						or float(data.get('GIA_TRI_HOA_DON_QUY_DOI')) != 0 and float(data.get('GIA_TRI_HOA_DON')) != 0):
					thong_bao = u'Dòng thứ ' + str(i) + ' , Một dòng không được nhập dồng thời cả giá trị hóa đơn/Số còn phải thu và Số thu trước. Bạn vui lòng kiểm tra lại'
					error.append({'type':'error', 'message' : thong_bao})

			# kiểm tra theo loại tiền
			du_no = False
			du_co = False
			du_no_nguyen_te = False
			du_co_nguyen_te = False

			gia_tri_hoa_don = False
			gia_tri_hoa_don_quy_doi = False
			so_con_phai_thu = False
			so_con_phai_thu_quy_doi = False
			so_thu_truoc = False
			so_thu_truoc_quy_doi = False

			if data.get('GIA_TRI_HOA_DON') != '':
				if float(data.get('GIA_TRI_HOA_DON')) != 0:
					gia_tri_hoa_don = float(data.get('GIA_TRI_HOA_DON'))
			if data.get('GIA_TRI_HOA_DON_QUY_DOI') != '':
				if float(data.get('GIA_TRI_HOA_DON_QUY_DOI')) != 0:
					gia_tri_hoa_don_quy_doi = float(data.get('GIA_TRI_HOA_DON_QUY_DOI'))
			if data.get('SO_CON_PHAI_TRA') != '':
				if float(data.get('SO_CON_PHAI_TRA')) != 0:
					so_con_phai_thu = float(data.get('SO_CON_PHAI_TRA'))
			if data.get('SO_CON_PHAI_TRA_QUY_DOI') != '':
				if float(data.get('SO_CON_PHAI_TRA_QUY_DOI')) != 0:
					so_con_phai_thu_quy_doi = float(data.get('SO_CON_PHAI_TRA_QUY_DOI'))
			if data.get('SO_TRA_TRUOC') != '':
				if float(data.get('SO_TRA_TRUOC')) != 0:
					so_thu_truoc = float(data.get('SO_TRA_TRUOC'))
			if data.get('SO_TRA_TRUOC_QUY_DOI') != '':
				if float(data.get('SO_TRA_TRUOC_QUY_DOI')) != 0:
					so_thu_truoc_quy_doi = float(data.get('SO_TRA_TRUOC_QUY_DOI'))

			if data.get('DU_NO') != '':
				if float(data.get('DU_NO')) != 0:
					du_no = float(data.get('DU_NO'))
			if data.get('DU_CO') != '':
				if float(data.get('DU_CO')) != 0:
					du_co = float(data.get('DU_CO'))
			if data.get('DU_NO_NGUYEN_TE') != '':
				if float(data.get('DU_NO_NGUYEN_TE')) != 0:
					du_no_nguyen_te = float(data.get('DU_NO_NGUYEN_TE'))
			if data.get('DU_CO_NGUYEN_TE') != '':
				if float(data.get('DU_CO_NGUYEN_TE')) != 0:
					du_co_nguyen_te = float(data.get('DU_CO_NGUYEN_TE'))
			
			if gia_tri_hoa_don == False and gia_tri_hoa_don_quy_doi == False and so_con_phai_thu == False \
				and so_con_phai_thu_quy_doi == False and so_thu_truoc == False and so_thu_truoc_quy_doi == False:
				if du_co == False and du_no == False:
					thong_bao = u'Dòng thứ ' + str(i) + ' , Bạn phải nhập Dư nợ quy đổi hoặc Dư có quy đổi'
					error.append({'type':'error', 'message' : thong_bao})
				else:
					if ma_loai_tien != 'VND':
						if not ((du_no != False and du_no_nguyen_te != False) or (du_co != False and du_co_nguyen_te != False)):
							thong_bao = u'Dòng thứ ' + str(i) + ' , Với loại tiền khác VND thì bạn phải nhập cả dư nợ và dư nợ quy đổi hoặc dư có và dư có quy đổi'
							error.append({'type':'error', 'message' : thong_bao})
					else:
						if du_no_nguyen_te == False and du_no != False:
							du_no_nguyen_te = du_no
						if du_co_nguyen_te == False and du_co != False:
							du_co_nguyen_te = du_co
					# validate không được nhập cả dư nợ và dư có
					if (du_no != False or du_no_nguyen_te != False) and (du_co != False or du_co_nguyen_te != False):
						thong_bao = u'Dòng thứ ' + str(i) + ' , đang nhập cả Dư nợ và Dư có. Bạn không được phép nhập cả Dư nợ và Dư có cho một tài khoản'
						error.append({'type':'error', 'message' : thong_bao})
			elif du_no == False and du_no_nguyen_te == False and du_co == False and du_co_nguyen_te == False:
				if ma_loai_tien == 'VND':
					if gia_tri_hoa_don == False and gia_tri_hoa_don_quy_doi != False:
						gia_tri_hoa_don = gia_tri_hoa_don_quy_doi
					if so_con_phai_thu == False and so_con_phai_thu_quy_doi != False:
						so_con_phai_thu = so_con_phai_thu_quy_doi
					if so_thu_truoc == False and so_thu_truoc_quy_doi != False:
						so_thu_truoc = so_thu_truoc_quy_doi



			key_level1 = str(loai_tien) + ',' + str(tai_khoan) 

			key_excel = str(loai_tien) + ',' + str(tai_khoan) + ',' + str(doi_tuong)
			arr_excel.append(key_excel)

			if key_level1 not in dict_create:
				dict_create[key_level1] = {}

			key_doi_tuong = doi_tuong
			if key_doi_tuong not in dict_create[key_level1]:
				dict_create[key_level1][key_doi_tuong] = []

			line_ids = dict_create[key_level1][key_doi_tuong]
			du_lieu_1_dong = {
				'SO_TAI_KHOAN' : data.get('SO_TAI_KHOAN') if data.get('SO_TAI_KHOAN') != '' else False, # Số tài khoản
				'MA_KHACH_HANG' : data.get('MA_KHACH_HANG') if data.get('MA_KHACH_HANG') != '' else False, # Mã khách hàng

				'DU_NO_NGUYEN_TE' : du_no_nguyen_te, # Dư nợ
				'DU_NO' : du_no, # Dư nợ quy đổi
				'DU_CO_NGUYEN_TE' : du_co_nguyen_te, # Dư có
				'DU_CO' : du_co, # Dư có quy đổi
				'TK_ID' : tai_khoan,
				'DOI_TUONG_ID' : doi_tuong,
				'currency_id'	 : loai_tien, # Loại tiền
				'NHAN_VIEN_ID' : nhan_vien,
				'DON_VI_ID' : don_vi,
				'CONG_TRINH_ID'  : cong_trinh,
				'HOP_DONG_BAN_ID': hop_dong_ban,
				'DON_DAT_HANG_ID' : don_dat_hang,
				'NGAY_HOA_DON' : data.get('NGAY_HOA_DON_CHUNG_TU'),
				'SO_HOA_DON' : data.get('SO_HOA_DON_CHUNG_TU'),
				'HAN_THANH_TOAN' : data.get('HAN_THANH_TOAN'),
				'TY_GIA' : float(data.get('TY_GIA')) if data.get('TY_GIA') != '' else False,
				'GIA_TRI_HOA_DON_NGUYEN_TE' : gia_tri_hoa_don,
				'GIA_TRI_HOA_DON' : gia_tri_hoa_don_quy_doi,
				'SO_CON_PHAI_THU_NGUYEN_TE' : so_con_phai_thu,
				'SO_CON_PHAI_THU' : so_con_phai_thu_quy_doi,
				'SO_THU_TRUOC_NGUYEN_TE' : so_thu_truoc,
				'SO_THU_TRUOC' : so_thu_truoc_quy_doi,
				'NHAN_VIEN_HOA_DON' : nhan_vien_hoa_don,
				
				'LOAI_CHUNG_TU' : '613',
				'KHAI_BAO_DAU_KY' : True,
				'NGAY_HACH_TOAN' : ngay_hach_toan_str,
				'NHAP_SO_DU_CHI_TIET' : 'Nhập chi tiết công nợ',
				'TEN_DOI_TUONG' : ten_doi_tuong,
				'TY_GIA' : ty_gia,
				'TY_GIA_CHI_TIET' : ty_gia_chi_tiet,
			}                 
			line_ids += [(0,0,du_lieu_1_dong)]


		# check trong db
		if du_lieu_trong_dtb:
			for du_lieu in du_lieu_trong_dtb:
				if du_lieu.TK_ID.DOI_TUONG == True and du_lieu.TK_ID.DOI_TUONG_SELECTION == '1':
					key_data_base = str(du_lieu.currency_id.id) +','+ str(du_lieu.TK_ID.id)  + ',' + str(du_lieu.DOI_TUONG_ID.id)
					key_create = str(du_lieu.currency_id.id) +','+ str(du_lieu.TK_ID.id) 
					if key_data_base not in arr_excel:
						if key_create not in dict_create:
							dict_create[key_create] = {}

						key_doi_tuong = du_lieu.DOI_TUONG_ID.id
						if key_doi_tuong not in dict_create[key_create]:
							dict_create[key_create][key_doi_tuong] = []

						line_ids = dict_create[key_create][key_doi_tuong]

						if du_lieu.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS:
							for ct_theo_doi_tuong in du_lieu.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS:
								du_lieu_1_dong = {
									'SO_TAI_KHOAN' : du_lieu.SO_TAI_KHOAN, # Số tài khoản
									'MA_KHACH_HANG' : du_lieu.DOI_TUONG_ID.MA, # Mã nhân viên
									'currency_id' : du_lieu.currency_id.id, # Loain tiền

									'NHAN_VIEN_ID' : ct_theo_doi_tuong.NHAN_VIEN_ID.id,
									'DON_VI_ID' : ct_theo_doi_tuong.DON_VI_ID.id,
									'CONG_TRINH_ID' : ct_theo_doi_tuong.CONG_TRINH_ID.id,
									'DON_DAT_HANG_ID' : ct_theo_doi_tuong.DON_DAT_HANG_ID.id,
									'HOP_DONG_BAN_ID' : ct_theo_doi_tuong.HOP_DONG_BAN_ID.id,

									'DU_NO_NGUYEN_TE' : du_lieu.DU_NO_NGUYEN_TE, # Dư nợ
									'DU_NO' : du_lieu.DU_NO,  # Dư nợ quy đổi
									'DU_CO_NGUYEN_TE' : du_lieu.DU_CO_NGUYEN_TE,  # Dư có
									'DU_CO' : du_lieu.DU_CO,  # Dư có quy đổi

									'NGAY_HOA_DON' : False,
									'SO_HOA_DON' : False,
									'HAN_THANH_TOAN' : False,
									'TY_GIA' : False,
									'GIA_TRI_HOA_DON_NGUYEN_TE' : False,
									'GIA_TRI_HOA_DON' : False,
									'SO_CON_PHAI_THU_NGUYEN_TE' : False,
									'SO_CON_PHAI_THU' : False,
									'SO_THU_TRUOC_NGUYEN_TE' : False,
									'SO_THU_TRUOC' : False,
									'NHAN_VIEN_HOA_DON' : False,

									'TK_ID' : du_lieu.TK_ID.id,
									'DOI_TUONG_ID' : du_lieu.DOI_TUONG_ID.id,
									'LOAI_CHUNG_TU' : du_lieu.LOAI_CHUNG_TU,
									'KHAI_BAO_DAU_KY' : du_lieu.KHAI_BAO_DAU_KY,
									'NGAY_HACH_TOAN' : du_lieu.NGAY_HACH_TOAN,
									'NHAP_SO_DU_CHI_TIET' : du_lieu.NHAP_SO_DU_CHI_TIET,
									'TY_GIA' : du_lieu.TY_GIA,
								}
						elif du_lieu.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS:
							for ct_theo_hoa_don in du_lieu.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS:
								du_lieu_1_dong = {
									'SO_TAI_KHOAN' : du_lieu.SO_TAI_KHOAN, # Số tài khoản
									'MA_KHACH_HANG' : du_lieu.DOI_TUONG_ID.MA, # Mã nhân viên
									'currency_id' : du_lieu.currency_id.id, # Loain tiền

									'NHAN_VIEN_ID' : False,
									'DON_VI_ID' : False,
									'CONG_TRINH_ID' : False,
									'DON_DAT_HANG_ID' : False,
									'HOP_DONG_BAN_ID' : False,


									'DU_NO_NGUYEN_TE' : False, # Dư nợ
									'DU_NO' : False,  # Dư nợ quy đổi
									'DU_CO_NGUYEN_TE' : False,  # Dư có
									'DU_CO' : False,  # Dư có quy đổi

									'NGAY_HOA_DON' : ct_theo_hoa_don.NGAY_HOA_DON,
									'SO_HOA_DON' : ct_theo_hoa_don.SO_HOA_DON,
									'HAN_THANH_TOAN' : ct_theo_hoa_don.HAN_THANH_TOAN,
									'TY_GIA' : ct_theo_hoa_don.TY_GIA,
									'GIA_TRI_HOA_DON_NGUYEN_TE' : ct_theo_hoa_don.GIA_TRI_HOA_DON_NGUYEN_TE,
									'GIA_TRI_HOA_DON' : ct_theo_hoa_don.GIA_TRI_HOA_DON,
									'SO_CON_PHAI_THU_NGUYEN_TE' : ct_theo_hoa_don.SO_CON_PHAI_THU_NGUYEN_TE,
									'SO_CON_PHAI_THU' : ct_theo_hoa_don.SO_CON_PHAI_THU,
									'SO_THU_TRUOC_NGUYEN_TE' : ct_theo_hoa_don.SO_THU_TRUOC_NGUYEN_TE,
									'SO_THU_TRUOC' : ct_theo_hoa_don.SO_THU_TRUOC,
									'NHAN_VIEN_HOA_DON' : ct_theo_hoa_don.NHAN_VIEN_ID.id,

									'TK_ID' : du_lieu.TK_ID.id,
									'DOI_TUONG_ID' : du_lieu.DOI_TUONG_ID.id,
									'LOAI_CHUNG_TU' : du_lieu.LOAI_CHUNG_TU,
									'KHAI_BAO_DAU_KY' : du_lieu.KHAI_BAO_DAU_KY,
									'NGAY_HACH_TOAN' : du_lieu.NGAY_HACH_TOAN,
									'NHAP_SO_DU_CHI_TIET' : du_lieu.NHAP_SO_DU_CHI_TIET,
									'TY_GIA' : du_lieu.TY_GIA,
									'TY_GIA_CHI_TIET' : ct_theo_hoa_don.TY_GIA,
								}
						else:
							du_lieu_1_dong = {
								'SO_TAI_KHOAN' : du_lieu.SO_TAI_KHOAN, # Số tài khoản
								'MA_KHACH_HANG' : du_lieu.DOI_TUONG_ID.MA, # Mã nhân viên
								'currency_id' : du_lieu.currency_id.id, # Loain tiền

								'NHAN_VIEN_ID' : False,
								'DON_VI_ID' : False,
								'CONG_TRINH_ID' : False,
								'DON_DAT_HANG_ID' : False,
								'HOP_DONG_BAN_ID' : False,

								'NGAY_HOA_DON' : False,
								'SO_HOA_DON' : False,
								'HAN_THANH_TOAN' : False,
								'TY_GIA' : False,
								'GIA_TRI_HOA_DON_NGUYEN_TE' : False,
								'GIA_TRI_HOA_DON' : False,
								'SO_CON_PHAI_THU_NGUYEN_TE' : False,
								'SO_CON_PHAI_THU' : False,
								'SO_THU_TRUOC_NGUYEN_TE' : False,
								'SO_THU_TRUOC' : False,
								'NHAN_VIEN_HOA_DON' : False,

								'DU_NO_NGUYEN_TE' : du_lieu.DU_NO_NGUYEN_TE, # Dư nợ
								'DU_NO' : du_lieu.DU_NO,  # Dư nợ quy đổi
								'DU_CO_NGUYEN_TE' : du_lieu.DU_CO_NGUYEN_TE,  # Dư có
								'DU_CO' : du_lieu.DU_CO,  # Dư có quy đổi
								'TK_ID' : du_lieu.TK_ID.id,
								'DOI_TUONG_ID' : du_lieu.DOI_TUONG_ID.id,
								'LOAI_CHUNG_TU' : du_lieu.LOAI_CHUNG_TU,
								'KHAI_BAO_DAU_KY' : du_lieu.KHAI_BAO_DAU_KY,
								'NGAY_HACH_TOAN' : du_lieu.NGAY_HACH_TOAN,
								'NHAP_SO_DU_CHI_TIET' : du_lieu.NHAP_SO_DU_CHI_TIET,
								'TY_GIA' : du_lieu.TY_GIA,
							}                 
						line_ids += [(0,0,du_lieu_1_dong)]
            
		#voi moi tai khoan va loai tien
		if error == []:
			for gia_tri in dict_create:
				chi_tiet = []
				#voi moi nhan vien
				for gia_ben_trong in dict_create[gia_tri]:
					dicChiTietTheoDoiTuong = {}
					du_no = 0
					du_no_nguyen_te = 0
					du_co = 0
					du_co_nguyen_te = 0
					
					dict_chi_tiet = dict_create[gia_tri][gia_ben_trong]

					dicChiTietTheoDoiTuong['ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS']=[]
					dicChiTietTheoDoiTuong['ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS']=[]
					# neu co chi tiet
					for dong_chi_tiet in dict_chi_tiet:
						dicChiTietTheoDoiTuong.update(dong_chi_tiet[2])
						if dong_chi_tiet[2].get('DU_NO') != False or dong_chi_tiet[2].get('DU_NO_NGUYEN_TE') or dong_chi_tiet[2].get('DU_CO') or dong_chi_tiet[2].get('DU_CO_NGUYEN_TE'):
							du_no += dong_chi_tiet[2].get('DU_NO')
							du_no_nguyen_te += dong_chi_tiet[2].get('DU_NO_NGUYEN_TE')
							du_co += dong_chi_tiet[2].get('DU_CO')
							du_co_nguyen_te += dong_chi_tiet[2].get('DU_CO_NGUYEN_TE')
						elif dong_chi_tiet[2].get('GIA_TRI_HOA_DON_NGUYEN_TE') != False or dong_chi_tiet[2].get('GIA_TRI_HOA_DON') or dong_chi_tiet[2].get('SO_CON_PHAI_THU_NGUYEN_TE') or dong_chi_tiet[2].get('SO_CON_PHAI_THU') or dong_chi_tiet[2].get('SO_THU_TRUOC_NGUYEN_TE') or dong_chi_tiet[2].get('SO_THU_TRUOC'):
							du_co += dong_chi_tiet[2].get('SO_THU_TRUOC')
							du_co_nguyen_te += dong_chi_tiet[2].get('SO_THU_TRUOC_NGUYEN_TE')
							du_no += dong_chi_tiet[2].get('SO_CON_PHAI_THU')
							du_no_nguyen_te += dong_chi_tiet[2].get('SO_CON_PHAI_THU_NGUYEN_TE')

						if dong_chi_tiet[2].get('CONG_TRINH_ID') != False or dong_chi_tiet[2].get('HOP_DONG_BAN_ID') != False \
								or dong_chi_tiet[2].get('DON_DAT_HANG_ID') != False or dong_chi_tiet[2].get('NHAN_VIEN_ID') != False:	

							dict_chi_tiet_theo_doi_tuong = {}
							dict_chi_tiet_theo_doi_tuong.update(dong_chi_tiet[2])
							dicChiTietTheoDoiTuong['ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS'] += [(0,0,dict_chi_tiet_theo_doi_tuong)]

						if dong_chi_tiet[2].get('NGAY_HOA_DON') != '' or dong_chi_tiet[2].get('SO_HOA_DON') != '' \
								or dong_chi_tiet[2].get('HAN_THANH_TOAN') != '' \
								or dong_chi_tiet[2].get('GIA_TRI_HOA_DON_NGUYEN_TE') != False or dong_chi_tiet[2].get('GIA_TRI_HOA_DON') != False \
								or dong_chi_tiet[2].get('SO_CON_PHAI_THU_NGUYEN_TE') != False or dong_chi_tiet[2].get('SO_CON_PHAI_THU') != False \
								or dong_chi_tiet[2].get('SO_THU_TRUOC_NGUYEN_TE') != False or dong_chi_tiet[2].get('SO_THU_TRUOC') != False \
								or dong_chi_tiet[2].get('NHAN_VIEN_HOA_DON') != False:
							dict_chi_tiet_theo_hoa_don = {}
							dict_chi_tiet_theo_hoa_don.update(dong_chi_tiet[2])
							dict_chi_tiet_theo_hoa_don['NHAN_VIEN_ID'] = dong_chi_tiet[2].get('NHAN_VIEN_HOA_DON')
							dict_chi_tiet_theo_hoa_don['TY_GIA'] = dong_chi_tiet[2].get('TY_GIA_CHI_TIET')
							dicChiTietTheoDoiTuong['ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS'] += [(0,0,dict_chi_tiet_theo_hoa_don)]
						
					# cập nhật lại dư nợ, dư có quy đổi
					if du_no > 0 and du_co > 0:
						du_no_tru_du_co = du_no - du_co
						if du_no_tru_du_co > 0:
							du_no = du_no_tru_du_co
							du_co = 0
						elif du_no_tru_du_co < 0:
							du_co = -1*du_no_tru_du_co
							du_no = 0
						else:
							du_no = 0
							du_co = 0
					# cập nhật lại dư nợ, dư có nguyên tệ
					if du_no_nguyen_te > 0 and du_co_nguyen_te > 0:
						du_no_tru_du_co_nguyen_te = du_no_nguyen_te - du_co_nguyen_te
						if du_no_tru_du_co_nguyen_te > 0:
							du_no_nguyen_te = du_no_tru_du_co_nguyen_te
							du_co_nguyen_te = 0
						elif du_no_tru_du_co_nguyen_te < 0:
							du_co_nguyen_te = -1*du_no_tru_du_co_nguyen_te
							du_no_nguyen_te = 0
						else:
							du_no_nguyen_te = 0
							du_co_nguyen_te = 0

					dicChiTietTheoDoiTuong['DU_NO'] = du_no
					dicChiTietTheoDoiTuong['DU_NO_NGUYEN_TE'] = du_no_nguyen_te
					dicChiTietTheoDoiTuong['DU_CO'] = du_co
					dicChiTietTheoDoiTuong['DU_CO_NGUYEN_TE'] = du_co_nguyen_te

					dicChiTietTheoDoiTuong['DOI_TUONG_ID']= gia_ben_trong
					chi_tiet += [(0,0,dicChiTietTheoDoiTuong)]

				for loai_bo_chi_tiet in chi_tiet:
					if loai_bo_chi_tiet[2]['ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS'] == []:
						loai_bo_chi_tiet[2].pop('ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS', None)
					if loai_bo_chi_tiet[2]['ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS'] == []:
						loai_bo_chi_tiet[2].pop('ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS', None)
				
				self.env['account.ex.so.du.tai.khoan'].create({
					'currency_id': int(gia_tri.split(',')[0]) if gia_tri.split(',')[0] != 'False' else False,
					'SO_TAI_KHOAN_ID' : int(gia_tri.split(',')[1]) if gia_tri.split(',')[1] != 'False' else False,
					'CHI_TIET_THEO_DOI_TUONG' : 1,
					'LOAI_DOI_TUONG' : '1',
					'LOAI_CHUNG_TU' : '613',
					'ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_IDS': chi_tiet,
				})
		if error == []:
			return {}
		else:
			return {'messages' : error}