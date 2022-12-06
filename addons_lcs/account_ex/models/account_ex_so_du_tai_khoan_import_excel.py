# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime

class ACCOUNT_EX_SO_DU_TAI_KHOAN(models.Model):
	_name = 'so.du.tai.khoan'
	_description = ''
	_auto = False

	SO_TAI_KHOAN = fields.Char(string='Số tài khoản (*)', help='Số tài khoản (*)')
	currency_id = fields.Many2one('res.currency', string='Loại tiền')
	DON_VI = fields.Char(string='Đơn vị', help='Đơn vị')
	KHOAN_MUC_CP = fields.Char(string='Khoản mục CP', help='Khoản mục CP')
	DOI_TUONG_THCP = fields.Char(string='Đối tượng THCP', help='Đối tượng THCP')
	CONG_TRINH = fields.Char(string='Công trình', help='Công trình')
	DON_DAT_HANG = fields.Char(string='Đơn đặt hàng', help='Đơn đặt hàng')
	DON_MUA_HANG = fields.Char(string='Đơn mua hàng', help='Đơn mua hàng')
	HOP_DONG_BAN = fields.Char(string='Hợp đồng bán', help='Hợp đồng bán')
	HOP_DONG_MUA = fields.Char(string='Hợp đồng mua', help='Hợp đồng mua')
	MA_THONG_KE = fields.Char(string='Mã thống kê', help='Mã thống kê')
	DU_NO = fields.Float(string='Dư Nợ quy đổi', help='Dư Nợ quy đổi')
	DU_CO = fields.Float(string='Dư Có quy đổi', help='Dư Có quy đổi')
	DU_NO_NGUYEN_TE = fields.Float(string='Dư Nợ', help='Dư Nợ')
	DU_CO_NGUYEN_TE = fields.Float(string='Dư Có', help='Dư Có')


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
				if tai_khoan.DOI_TUONG == True:
					thong_bao = u'Cột Số tài khoản dòng thứ ' + str(t) + u' là tài khoản chi tiết theo đối tượng'
					error.append({'type':'error', 'message' : thong_bao})
				if tai_khoan.TAI_KHOAN_NGAN_HANG == True:
					thong_bao = u'Cột Số tài khoản dòng thứ ' + str(t) + u' là tài khoản chi tiết theo tài khoản ngân hàng'
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
				thong_bao = u'Cột Số tài khoản dòng thứ ' + str(i) + u' là trường bắt buộc nhập vui lòng nhập để import'
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
			
			# Đơn vị
			don_vi = False
			if data.get('DON_VI') != '':
				tc = self.env['danh.muc.to.chuc'].search([('MA_DON_VI', '=', data.get('DON_VI'))])
				if tc:
					don_vi = tc.id
				else:
					thong_bao = u'Cột Đơn vị dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/đươn vị'
					error.append({'type':'error', 'message' : thong_bao})

			# khoản mục cp
			khoan_muc_cp = False
			if data.get('KHOAN_MUC_CP') != '':
				kmcp = self.env['danh.muc.khoan.muc.cp'].search([('MA_KHOAN_MUC_CP', '=', data.get('KHOAN_MUC_CP'))])
				if kmcp:
					khoan_muc_cp = kmcp.id
				else:
					thong_bao = u'Cột khoản mục chi phí dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/khoản mục CP'
					error.append({'type':'error', 'message' : thong_bao})

			# đối tượng thcp
			doi_tuong_thcp = False
			if data.get('DOI_TUONG_THCP') != '':
				dtthcp = self.env['danh.muc.doi.tuong.tap.hop.chi.phi'].search([('MA_DOI_TUONG_THCP', '=', data.get('DOI_TUONG_THCP'))])
				if dtthcp:
					doi_tuong_thcp = dtthcp.id
				else:
					thong_bao = u'Cột đối tượng thcp dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/đối tượng thcp'
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

			# đơn đặt hàng
			don_dat_hang = False
			if data.get('DON_DAT_HANG') != '':
				ddh = self.env['account.ex.don.dat.hang'].search([('SO_DON_HANG', '=', data.get('DON_DAT_HANG'))])
				if ddh:
					don_dat_hang = ddh.id
				else:
					thong_bao = u'Cột đơn đặt hàng dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/đơn đặt hàng'
					error.append({'type':'error', 'message' : thong_bao})

			# Đơn mua hàng
			don_mua_hang = False
			if data.get('DON_MUA_HANG') != '':
				dmh = self.env['purchase.ex.don.mua.hang'].search([('SO_DON_HANG', '=', data.get('DON_MUA_HANG'))])
				if dmh:
					don_mua_hang = dmh.id
				else:
					thong_bao = u'Cột Hợp đồng bán dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/Hợp đồng bán'
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

			# Hợp đồng mua
			hop_dong_mua = False
			if data.get('HOP_DONG_MUA') != '':
				hdm = self.env['purchase.ex.hop.dong.mua.hang'].search([('SO_HOP_DONG', '=', data.get('HOP_DONG_MUA'))])
				if hdm:
					hop_dong_mua = hdm.id
				else:
					thong_bao = u'Cột Hợp đồng mua dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/Hợp đồng mua'
					error.append({'type':'error', 'message' : thong_bao})

			# mã thống kê
			ma_thong_ke = False
			if data.get('MA_THONG_KE') != '':
				mtk = self.env['danh.muc.ma.thong.ke'].search([('MA_THONG_KE', '=', data.get('MA_THONG_KE'))])
				if mtk:
					ma_thong_ke = mtk.id
				else:
					thong_bao = u'Cột mã thống kê dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/mã thống kê'
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

			key_excel = str(loai_tien) + ',' + str(tai_khoan)
			arr_excel.append(key_excel)

			if key_level1 not in dict_create:
				dict_create[key_level1] = {}

			key_tai_khoan = tai_khoan
			if key_tai_khoan not in dict_create[key_level1]:
				dict_create[key_level1][key_tai_khoan] = []

			line_ids = dict_create[key_level1][key_tai_khoan]
			du_lieu_1_dong = {
				'SO_TAI_KHOAN' : data.get('SO_TAI_KHOAN') if data.get('SO_TAI_KHOAN') != '' else False, # Số tài khoản
				'currency_id'	 : loai_tien, # Loại tiền
				'DON_VI_ID' : don_vi,
				'KHOAN_MUC_CP_ID' : khoan_muc_cp,
				'DOI_TUONG_THCP_ID' : doi_tuong_thcp,
				'CONG_TRINH_ID'  : cong_trinh,
				'DON_DAT_HANG_ID': don_dat_hang,
				'DON_MUA_HANG_ID' : don_mua_hang,
				'HOP_DONG_BAN_ID' : hop_dong_ban,
				'HOP_DONG_MUA_ID' : hop_dong_mua,
				'MA_THONG_KE_ID' : ma_thong_ke,

				'DU_NO_NGUYEN_TE' : du_no_nguyen_te, # Dư nợ
				'DU_NO' : du_no, # Dư nợ quy đổi
				'DU_CO_NGUYEN_TE' : du_co_nguyen_te, # Dư có
				'DU_CO' : du_co, # Dư có quy đổi
				'TK_ID' : tai_khoan,
				
				'LOAI_CHUNG_TU' : '610',
				'KHAI_BAO_DAU_KY' : True,
				'NGAY_HACH_TOAN' : ngay_hach_toan_str,
				'NHAP_SO_DU_CHI_TIET' : 'Nhập chi tiết công nợ',
				'TY_GIA' : ty_gia,
			}                 
			line_ids += [(0,0,du_lieu_1_dong)]


		# check trong db
		if du_lieu_trong_dtb:
			for du_lieu in du_lieu_trong_dtb:
				if du_lieu.TK_ID.DOI_TUONG == False and du_lieu.TK_ID.TAI_KHOAN_NGAN_HANG == False:
					key_data_base = str(du_lieu.currency_id.id) +','+ str(du_lieu.TK_ID.id)
					key_create = str(du_lieu.currency_id.id)
					if key_data_base not in arr_excel:
						if key_create not in dict_create:
							dict_create[key_create] = {}

						key_tai_khoan = du_lieu.TK_ID.id
						if key_tai_khoan not in dict_create[key_create]:
							dict_create[key_create][key_tai_khoan] = []

						line_ids = dict_create[key_create][key_tai_khoan]

						if du_lieu.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS:
							for ct_theo_doi_tuong in du_lieu.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS:
								du_lieu_1_dong = {
									'SO_TAI_KHOAN' : du_lieu.SO_TAI_KHOAN, # Số tài khoản
									'currency_id' : du_lieu.currency_id.id, # Loain tiền

									'DON_VI_ID' : ct_theo_doi_tuong.DON_VI_ID.id,
									'KHOAN_MUC_CP_ID' : ct_theo_doi_tuong.KHOAN_MUC_CP_ID.id,
									'DOI_TUONG_THCP_ID' : ct_theo_doi_tuong.DOI_TUONG_THCP_ID.id,
									'CONG_TRINH_ID' : ct_theo_doi_tuong.CONG_TRINH_ID.id,
									'DON_DAT_HANG_ID' : ct_theo_doi_tuong.DON_DAT_HANG_ID.id,
									'DON_MUA_HANG_ID' : ct_theo_doi_tuong.DON_MUA_HANG_ID.id,
									'HOP_DONG_BAN_ID' : ct_theo_doi_tuong.HOP_DONG_BAN_ID.id,
									'HOP_DONG_MUA_ID' : ct_theo_doi_tuong.HOP_DONG_MUA_ID.id,
									'MA_THONG_KE_ID' : ct_theo_doi_tuong.MA_THONG_KE_ID.id,

									'DU_NO_NGUYEN_TE' : ct_theo_doi_tuong.DU_NO_NGUYEN_TE, # Dư nợ
									'DU_NO' : ct_theo_doi_tuong.DU_NO, # Dư nợ quy đổi
									'DU_CO_NGUYEN_TE' : ct_theo_doi_tuong.DU_CO_NGUYEN_TE, # Dư có
									'DU_CO' : ct_theo_doi_tuong.DU_CO, # Dư có quy đổi

									'TK_ID' : du_lieu.TK_ID.id,
									'LOAI_CHUNG_TU' : du_lieu.LOAI_CHUNG_TU,
									'KHAI_BAO_DAU_KY' : du_lieu.KHAI_BAO_DAU_KY,
									'NGAY_HACH_TOAN' : du_lieu.NGAY_HACH_TOAN,
									'NHAP_SO_DU_CHI_TIET' : du_lieu.NHAP_SO_DU_CHI_TIET,
									'TY_GIA' : du_lieu.TY_GIA,
								}
						else:
							du_lieu_1_dong = {
								'SO_TAI_KHOAN' : du_lieu.SO_TAI_KHOAN, # Số tài khoản
								'currency_id' : du_lieu.currency_id.id, # Loain tiền
								'TK_ID' : du_lieu.TK_ID.id,

								'DON_VI_ID' : False,
								'KHOAN_MUC_CP_ID' : False,
								'DOI_TUONG_THCP_ID' : False,
								'CONG_TRINH_ID' : False,
								'DON_DAT_HANG_ID' : False,
								'DON_MUA_HANG_ID' : False,
								'HOP_DONG_BAN_ID' : False,
								'HOP_DONG_MUA_ID' : False,
								'MA_THONG_KE_ID' : False,

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
						dicChiTietTheoDoiTuong.update(dong_chi_tiet[2])
						if dong_chi_tiet[2].get('DU_NO') != False or dong_chi_tiet[2].get('DU_NO_NGUYEN_TE') or dong_chi_tiet[2].get('DU_CO') or dong_chi_tiet[2].get('DU_CO_NGUYEN_TE'):
							du_no += dong_chi_tiet[2].get('DU_NO')
							du_no_nguyen_te += dong_chi_tiet[2].get('DU_NO_NGUYEN_TE')
							du_co += dong_chi_tiet[2].get('DU_CO')
							du_co_nguyen_te += dong_chi_tiet[2].get('DU_CO_NGUYEN_TE')
						

						if dong_chi_tiet[2].get('DON_VI_ID') != False or dong_chi_tiet[2].get('KHOAN_MUC_CP_ID') != False \
								or dong_chi_tiet[2].get('DOI_TUONG_THCP_ID') != False or dong_chi_tiet[2].get('CONG_TRINH_ID') != False \
								or dong_chi_tiet[2].get('DON_DAT_HANG_ID') != False or dong_chi_tiet[2].get('DON_MUA_HANG_ID') != False \
								or dong_chi_tiet[2].get('HOP_DONG_BAN_ID') != False or dong_chi_tiet[2].get('HOP_DONG_MUA_ID') != False \
								or dong_chi_tiet[2].get('MA_THONG_KE_ID') != False:	

							dict_chi_tiet_theo_doi_tuong = {}
							dict_chi_tiet_theo_doi_tuong.update(dong_chi_tiet[2])
							dicChiTietTheoDoiTuong['ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS'] += [(0,0,dict_chi_tiet_theo_doi_tuong)]

						
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

					chi_tiet += [(0,0,dicChiTietTheoDoiTuong)]

				for loai_bo_chi_tiet in chi_tiet:
					if loai_bo_chi_tiet[2]['ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS'] == []:
						loai_bo_chi_tiet[2].pop('ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS', None)
					
				self.env['account.ex.so.du.tai.khoan'].create({
					'currency_id': int(gia_tri) if gia_tri != 'False' else False,
					'CHI_TIET_THEO_DOI_TUONG' : 0,
					# 'LOAI_DOI_TUONG' : '2',
					'LOAI_CHUNG_TU' : '610',
					'ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_IDS': chi_tiet,
				})
		if error == []:
			return {}
		else:
			return {'messages' : error}

			