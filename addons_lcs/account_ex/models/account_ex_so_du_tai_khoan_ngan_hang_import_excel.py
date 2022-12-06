# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime

class ACCOUNT_EX_SO_DU_TK_NGAN_HANG_EXCEL(models.Model):
	_name = 'so.du.tk.ngan.hang'
	_description = ''
	_auto = False

	SO_TK_NGAN_HANG = fields.Char(string='TK ngân hàng (*)', help='TK ngân hàng (*)')
	DU_NO = fields.Float(string='Dư Nợ quy đổi', help='Dư Nợ quy đổi')
	DU_CO = fields.Float(string='Dư Có quy đổi', help='Dư Có quy đổi')
	DU_NO_NGUYEN_TE = fields.Float(string='Dư Nợ', help='Dư Nợ')
	DU_CO_NGUYEN_TE = fields.Float(string='Dư Có', help='Dư Có')
	currency_id = fields.Many2one('res.currency', string='Loại tiền')
	SO_TAI_KHOAN = fields.Char(string='Số tài khoản (*)', help='Số tài khoản (*)')

	def import_from_excel(self, import_fields, data):

		data_field = []
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

		t = 0
		for row in data:
			j = 0
			row_field = {}
			for field in import_fields:
				row_field[field] = row[j]
				j += 1
			data_field.append(row_field)

			if len(data) >= t:
				tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', data[t][0])],limit=1)
				if tai_khoan.TAI_KHOAN_NGAN_HANG == False:
					thong_bao = u'Cột Số tài khoản dòng thứ ' + str(t) + u' không phải là tài khoản chi tiết theo tài khoản ngân hàng vui lòng kiểm tra lại'
					error.append({'type':'error', 'message' : thong_bao})
			t += 1

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
					thong_bao = u'Cột Số tài khoản dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/hệ thống tài khoản'
					error.append({'type':'error', 'message' : thong_bao})
			else:
				thong_bao = u'Cột Số tài khoản dòng thứ ' + str(i) + u' là trường bắt buộc nhập vui long nhập để import'
				error.append({'type':'error', 'message' : thong_bao})

			# Tài khoản ngân hàng
			tk_ngan_hang = False
			if data.get('SO_TK_NGAN_HANG') != '':
				tknh = self.env['danh.muc.tai.khoan.ngan.hang'].search([('SO_TAI_KHOAN', '=', data.get('SO_TK_NGAN_HANG'))])
				if tknh:
					tk_ngan_hang = tknh.id
				else:
					thong_bao = u'Cột Số tài khoản ngân hàng dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/tài khoản ngân hàng'
					error.append({'type':'error', 'message' : thong_bao})
			else:
				thong_bao = u'Cột Số tài khoản ngân hàng dòng thứ ' + str(i) + u' là trường bắt buộc nhập vui long nhập để import'
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
			else:
				thong_bao = u'cột loại tiền dòng thứ ' + str(i) + u' là trường bắt buộc nhập vui long nhập để import'
				error.append({'type':'error', 'message' : thong_bao})


			# kiểm tra theo loại tiền
			du_no = False
			du_co = False
			du_no_nguyen_te = False
			du_co_nguyen_te = False
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
			# validate bắt buộc phải nhập trường quy đổi
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
			
			key_level1 = str(loai_tien)

			key_excel = str(loai_tien) + ',' + str(tk_ngan_hang)
			arr_excel.append(key_excel)

			if key_level1 not in dict_create:
				dict_create[key_level1] = {}

			key_tk_ngan_hang = tk_ngan_hang
			if key_tk_ngan_hang not in dict_create[key_level1]:
				dict_create[key_level1][key_tk_ngan_hang] = []

			line_ids = dict_create[key_level1][key_tk_ngan_hang]
			du_lieu_1_dong = {
				'SO_TAI_KHOAN' : data.get('SO_TAI_KHOAN') if data.get('SO_TAI_KHOAN') != '' else False, # Số tài khoản
				'currency_id'	 : loai_tien, # Loại tiền
				'TK_NGAN_HANG_ID' : tk_ngan_hang,

				'DU_NO_NGUYEN_TE' : du_no_nguyen_te, # Dư nợ
				'DU_NO' : du_no, # Dư nợ quy đổi
				'DU_CO_NGUYEN_TE' : du_co_nguyen_te, # Dư có
				'DU_CO' : du_co, # Dư có quy đổi
				'TK_ID' : tai_khoan,
				
				'LOAI_CHUNG_TU' : '620',
				'KHAI_BAO_DAU_KY' : True,
				'NGAY_HACH_TOAN' : ngay_hach_toan_str,
				'NHAP_SO_DU_CHI_TIET' : 'Nhập chi tiết công nợ',
				'TY_GIA' : ty_gia,
			}                 
			line_ids += [(0,0,du_lieu_1_dong)]


		# check trong db
		if du_lieu_trong_dtb:
			for du_lieu in du_lieu_trong_dtb:
				if du_lieu.TK_ID.TAI_KHOAN_NGAN_HANG == True:
					key_data_base = str(du_lieu.currency_id.id) +','+ str(du_lieu.TK_NGAN_HANG_ID.id)
					key_create = str(du_lieu.currency_id.id)
					if key_data_base not in arr_excel:
						if key_create not in dict_create:
							dict_create[key_create] = {}

						key_tk_ngan_hang = du_lieu.TK_NGAN_HANG_ID.id
						if key_tk_ngan_hang not in dict_create[key_create]:
							dict_create[key_create][key_tk_ngan_hang] = []

						line_ids = dict_create[key_create][key_tk_ngan_hang]
						
						du_lieu_1_dong = {
							'SO_TAI_KHOAN' : du_lieu.SO_TAI_KHOAN, # Số tài khoản
							'currency_id' : du_lieu.currency_id.id, # Loain tiền
							'TK_NGAN_HANG_ID' : du_lieu.TK_NGAN_HANG_ID.id,

							'DU_NO_NGUYEN_TE' : du_lieu.DU_NO_NGUYEN_TE, # Dư nợ
							'DU_NO' : du_lieu.DU_NO, # Dư nợ quy đổi
							'DU_CO_NGUYEN_TE' : du_lieu.DU_CO_NGUYEN_TE, # Dư có
							'DU_CO' : du_lieu.DU_CO, # Dư có quy đổi

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
				for gia_ben_trong in dict_create[gia_tri]:
					dicChiTietTheoDoiTuong = {}
					dict_chi_tiet = dict_create[gia_tri][gia_ben_trong]
					for dong_chi_tiet in dict_chi_tiet:
						dicChiTietTheoDoiTuong.update(dong_chi_tiet[2])
					chi_tiet += [(0,0,dicChiTietTheoDoiTuong)]
					
				self.env['account.ex.so.du.tai.khoan'].create({
					'currency_id': int(gia_tri) if gia_tri != 'False' else False,
					'CHI_TIET_THEO_DOI_TUONG' : 0,
					'CHI_TIET_THEO_TK_NGAN_HANG' : 1,
					'LOAI_CHUNG_TU' : '620',
					'ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_IDS': chi_tiet,
				})
		if error == []:
			return {}
		else:
			return {'messages' : error}

			