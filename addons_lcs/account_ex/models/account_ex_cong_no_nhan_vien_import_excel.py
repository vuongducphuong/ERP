# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime

class ACCOUNT_EX_CONG_NO_NHAN_VIEN_EXCEL(models.Model):
	_name = 'cong.no.nhan.vien'
	_description = ''
	_auto = False

	SO_TAI_KHOAN = fields.Char(string='Số tài khoản (*)', help='Số tài khoản (*)')
	DU_NO = fields.Float(string='Dư Nợ quy đổi', help='Dư Nợ quy đổi')
	DU_CO = fields.Float(string='Dư Có quy đổi', help='Dư Có quy đổi')
	DU_NO_NGUYEN_TE = fields.Float(string='Dư Nợ', help='Dư Nợ')
	DU_CO_NGUYEN_TE = fields.Float(string='Dư Có', help='Dư Có')
	currency_id = fields.Many2one('res.currency', string='Loại tiền')
	MA_NHAN_VIEN = fields.Char(string='Nhân viên (*)', help='Nhân viên (*)')
	TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='Tên nhân viên')
	CONG_TRINH = fields.Char(string='Công trình', help='Công trình')
	HOP_DONG_MUA = fields.Char(string='Hợp đồng mua', help='Hợp đồng mua')
	HOP_DONG_BAN = fields.Char(string='Hợp đồng bán', help='Hợp đồng bán')
	DON_VI = fields.Char(string='Đơn vị', help='Đơn vị')


	def import_from_excel(self, import_fields, data):
        # 1. trường hợp import thông thuwongf, gọi vào hàm load()
		if data and import_fields:
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
					if tai_khoan.DOI_TUONG == False:
						thong_bao = u'Cột Số tài khoản dòng thứ ' + str(t) + u' là không phải là tài khoản chi tiết theo đối tượng vui lòng kiểm tra lại'
						error.append({'type':'error', 'message' : thong_bao})
				t += 1

			for data in data_field:
				i += 1
				doi_tuong = False
				ten_doi_tuong = False
				tai_khoan = False
				cong_trinh = False
				hop_dong_mua = False
				hop_dong_ban = False
				don_vi = False

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
					else:
						thong_bao = u'cột loại tiền dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/loại tiền'
						error.append({'type':'error', 'message' : thong_bao})
				
				if data.get('MA_NHAN_VIEN') != '':
					dt = self.env['res.partner'].search([('MA', '=', data.get('MA_NHAN_VIEN'))])
					if dt:
						doi_tuong = dt.id
						ten_doi_tuong = dt.HO_VA_TEN
						if dt.LA_NHAN_VIEN == False:
							thong_bao = u'Cột Nhân viên (*) dòng thứ ' + str(i) + u' không tìm thấy ' + str(data.get('MA_NHA_CUNG_CAP')) + ' trong danh mục/nhân viên. Vui lòng kiểm tra lại'
							error.append({'type':'error', 'message' : thong_bao})
					else:
						thong_bao = u'Cột Nhân viên (*) dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/nhân viên'
						error.append({'type':'error', 'message' : thong_bao})
				else:
					thong_bao = u'Cột Nhân viên (*) dòng thứ ' + str(i) + u' là trường bắt buộc nhập vui long nhập để import'
					error.append({'type':'error', 'message' : thong_bao})

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
				if data.get('CONG_TRINH') != '':
					ct = self.env['danh.muc.cong.trinh'].search([('MA_CONG_TRINH', '=', data.get('CONG_TRINH'))])
					if ct:
						cong_trinh = ct.id
					else:
						thong_bao = u'Cột Công trình dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/công trình'
						error.append({'type':'error', 'message' : thong_bao})
				if data.get('HOP_DONG_MUA') != '':
					hdm = self.env['purchase.ex.hop.dong.mua.hang'].search([('SO_HOP_DONG', '=', data.get('HOP_DONG_MUA'))])
					if hdm:
						hop_dong_mua = hdm.id
					else:
						thong_bao = u'Cột Hợp đồng mua dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/Hợp đồng mua'
						error.append({'type':'error', 'message' : thong_bao})
				if data.get('HOP_DONG_BAN') != '':
					hdb = self.env['sale.ex.hop.dong.ban'].search([('SO_HOP_DONG', '=', data.get('HOP_DONG_BAN'))])
					if hdb:
						hop_dong_ban = hdb.id
					else:
						thong_bao = u'Cột Hợp đồng bán dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/Hợp đồng bán'
						error.append({'type':'error', 'message' : thong_bao})

				# đơn vị
				if data.get('DON_VI') != '':
					dv = self.env['danh.muc.to.chuc'].search([('MA_DON_VI', '=', data.get('DON_VI'))])
					if dv:
						don_vi = dv.id
					else:
						thong_bao = u'Cột Đơn vị dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/đơn vị'
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
					'MA_NHAN_VIEN' : data.get('MA_NHAN_VIEN') if data.get('MA_NHAN_VIEN') != '' else False, # Mã nhân viên
					'currency_id' : loai_tien, # Loại tiền
					'DU_NO_NGUYEN_TE' : du_no_nguyen_te, # Dư nợ
					'DU_NO' : du_no, # Dư nợ quy đổi
					'DU_CO_NGUYEN_TE' : du_co_nguyen_te, # Dư có
					'DU_CO' : du_co, # Dư có quy đổi
					'CONG_TRINH_ID'  : cong_trinh,
					'HOP_DONG_MUA_ID': hop_dong_mua,
					'HOP_DONG_BAN_ID' : hop_dong_ban,
					'TK_ID' : tai_khoan,
					'DOI_TUONG_ID' : doi_tuong,
					'LOAI_CHUNG_TU' : '614',
					'KHAI_BAO_DAU_KY' : True,
					'NGAY_HACH_TOAN' : ngay_hach_toan_str,
					'NHAP_SO_DU_CHI_TIET' : 'Nhập chi tiết công nợ',
					'TEN_DOI_TUONG' : ten_doi_tuong,
					'TY_GIA' : ty_gia,
					'DON_VI_ID' : don_vi,
				}                 
				line_ids += [(0,0,du_lieu_1_dong)]

			if du_lieu_trong_dtb:
				for du_lieu in du_lieu_trong_dtb:
					if du_lieu.TK_ID.DOI_TUONG == True and du_lieu.TK_ID.DOI_TUONG_SELECTION == '2':
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
										'MA_NHAN_VIEN' : du_lieu.DOI_TUONG_ID.MA, # Mã nhân viên
										'currency_id' : du_lieu.currency_id.id, # Loain tiền
										
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
										'CONG_TRINH_ID' : ct_theo_doi_tuong.CONG_TRINH_ID.id,
										'HOP_DONG_MUA_ID' : ct_theo_doi_tuong.HOP_DONG_MUA_ID.id,
										'HOP_DONG_BAN_ID' : ct_theo_doi_tuong.HOP_DONG_BAN_ID.id,
										'DON_VI_ID' : ct_theo_doi_tuong.DON_VI_ID.id,
									}
							else:
								du_lieu_1_dong = {
									'SO_TAI_KHOAN' : du_lieu.SO_TAI_KHOAN, # Số tài khoản
									'MA_NHAN_VIEN' : du_lieu.DOI_TUONG_ID.MA, # Mã nhân viên
									'currency_id' : du_lieu.currency_id.id, # Loain tiền
									# import_fields[3] : du_lieu.DOI_TUONG_ID.HO_VA_TEN, # Tên nhân viên
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
									'CONG_TRINH_ID' : False,
									'HOP_DONG_MUA_ID' : False,
									'HOP_DONG_BAN_ID' : False,  
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
						# neu co chi tiet
						for dong_chi_tiet in dict_chi_tiet:
							# inject dong_chi_tiet vao dicChiTietTheoDoiTuong
							dicChiTietTheoDoiTuong.update(dong_chi_tiet[2])
							du_no += dong_chi_tiet[2].get('DU_NO')
							du_no_nguyen_te += dong_chi_tiet[2].get('DU_NO_NGUYEN_TE')
							du_co += dong_chi_tiet[2].get('DU_CO')
							du_co_nguyen_te += dong_chi_tiet[2].get('DU_CO_NGUYEN_TE')

							if dong_chi_tiet[2].get('CONG_TRINH_ID') != False or dong_chi_tiet[2].get('HOP_DONG_MUA_ID') != False or dong_chi_tiet[2].get('HOP_DONG_BAN_ID') != False:
								dicChiTietTheoDoiTuong['ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS'] += [dong_chi_tiet]
								# chi_tiet += [(0,0,dicChiTietTheoDoiTuong)]
								
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


						
					self.env['account.ex.so.du.tai.khoan'].create({
						'currency_id': int(gia_tri.split(',')[0]) if gia_tri.split(',')[0] != 'False' else False,
						'SO_TAI_KHOAN_ID' : int(gia_tri.split(',')[1]) if gia_tri.split(',')[1] != 'False' else False,
						'CHI_TIET_THEO_DOI_TUONG' : 1,
						'LOAI_DOI_TUONG' : '2',
						'LOAI_CHUNG_TU' : '614',
						'ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_IDS': chi_tiet,
					})
		if error == []:
			return {}
		else:
			return {'messages' : error}