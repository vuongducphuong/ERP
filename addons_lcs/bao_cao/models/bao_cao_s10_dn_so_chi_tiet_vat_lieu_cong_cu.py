# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_S10_DN_SO_CHI_TIET_VAT_LIEU_CONG_CU(models.Model):
	_name = 'bao.cao.s10.dn.so.chi.tiet.vat.lieu.cong.cu'
	_auto = False

	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
	BAO_GOM_SO_LIEU_CHI_NHANH_PHUC_VU = fields.Boolean(string='Bao gồm số liệu chi nhánh phục thuộc', help='Bao gồm số liệu chi nhánh phục vụ',default='True')
	KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default='THANG_4')
	TU = fields.Date(string='Từ', help='Từ',default=fields.Datetime.now)
	DEN = fields.Date(string='Đến', help='Đến',default=fields.Datetime.now)
	NHOM_VTHH_ID = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm VTHH', help='Nhóm vthh')
	DON_VI_TINH = fields.Selection([('DON_VI_TINH_CHINH', 'Đơn vị tính chính'), ('DON_VI_CHUYEN_DOI_1', 'Đơn vị chuyển đổi 1'), ('DON_VI_CHUYEN_DOI_2', 'Đơn vị chuyển đổi 2'), ], string='Đơn vị tính', help='Đơn vị tính',default='DON_VI_CHUYEN_DOI_2')
	KHO_ID = fields.Many2one('danh.muc.kho', string='Kho', help='Kho')
	CHUNG_TU_SO_HIEU = fields.Char(string='Số hiệu', help='Số hiệu')
	CHUNG_TU_NGAY_THANG = fields.Char(string='Ngày,tháng', help='Ngày,tháng')
	DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
	TAI_KHOAN_DOI_UNG = fields.Char(string='Tài khoản đối ứng', help='Tài khoản đối ứng')
	DVT = fields.Char(string='ĐVT', help='Đơn vị tính')
	DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá', digits=decimal_precision.get_precision('DON_GIA'))
	SO_LUONG_NHAP = fields.Float(string='Số lượng', help='Nhập số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
	SO_TIEN_NHAP = fields.Float(string='Thành tiền', help='Nhập thành tiền')
	SO_LUONG_XUAT = fields.Float(string='Số lượng', help='Xuất số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
	SO_TIEN_XUAT = fields.Float(string='Thành tiền', help='Xuất thành tiền')
	SO_LUONG_TON = fields.Float(string='Số lượng ', help='Tồn số lượng ', digits=decimal_precision.get_precision('SO_LUONG'))
	SO_TIEN_TON = fields.Float(string='Thành tiền', help='Tồn thành tiền')
	MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa')
	MA_HANG = fields.Char(string='Mã hàng', help='Mã hàng')
	TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng')
	MA_KHO = fields.Char(string='Mã kho', help='Mã kho')
	TEN_KHO = fields.Char(string='Tên kho', help='Tên kho')


	HANG_ID = fields.One2many('danh.muc.vat.tu.hang.hoa')
	CHON_TAT_CA_SAN_PHAM = fields.Boolean('Tất cả sản phẩm', default=True)
	SAN_PHAM_MANY_IDS = fields.Many2many('danh.muc.vat.tu.hang.hoa','s10dn_danh_muc_vthh', string='Chọn sản phẩm')
	MA_PC_NHOM_VTHH = fields.Char()

	ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
	MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')
	MA_HANG_TEN_HANG = fields.Char(string='Mã hàng - Tên hàng', help='Mã hàng - Tên hàng')
	MA_KHO_TEN_KHO = fields.Char(string='Mã kho - Tên kho', help='Mã kho - Tên kho')

	GROUP_VTHH = fields.Many2one('bao.cao.s10.dn.so.chi.tiet.vat.lieu.cong.cu.group.vthh')

	@api.onchange('HANG_ID')
	def update_SAN_PHAM_IDS(self):
		self.SAN_PHAM_MANY_IDS = self.HANG_ID.ids
	   
	@api.onchange('NHOM_VTHH_ID')
	def update_NHOM_VTHH_ID(self):
		self.SAN_PHAM_MANY_IDS = []
		self.MA_PC_NHOM_VTHH =self.NHOM_VTHH_ID.MA_PHAN_CAP

	@api.onchange('SAN_PHAM_MANY_IDS')
	def _onchange_SAN_PHAM_MANY_IDS(self):
		self.HANG_ID = self.SAN_PHAM_MANY_IDS.ids

	### START IMPLEMENTING CODE ###

	
	@api.model
	def default_get(self, fields_list):
		result = super(BAO_CAO_S10_DN_SO_CHI_TIET_VAT_LIEU_CONG_CU, self).default_get(fields_list)
		chi_nhanh =  self.env['danh.muc.to.chuc'].search([],limit=1)
		kho = self.env['danh.muc.kho'].search([],limit=1)
		if chi_nhanh:
			result['CHI_NHANH_ID'] = chi_nhanh.id
		if kho : 
			result['KHO_ID'] = kho.id
		return result


	def _validate(self):
		params = self._context

		TU = params.get('TU')
		TU_NGAY_F = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		DEN = params.get('DEN')
		DEN_NGAY_F = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		
		CHON_TAT_CA_SAN_PHAM = params['CHON_TAT_CA_SAN_PHAM'] if 'CHON_TAT_CA_SAN_PHAM' in params.keys() else 'False'
		SAN_PHAM_MANY_IDS = params['SAN_PHAM_MANY_IDS'] if 'SAN_PHAM_MANY_IDS' in params.keys() else 'False'

		if(TU=='False'):
			raise ValidationError('<Từ ngày> không được bỏ trống.')
		elif(DEN=='False'):
			raise ValidationError('<Đến ngày> không được bỏ trống.')
		elif(TU_NGAY_F > DEN_NGAY_F):
			raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')
		 # validate của các trường hợp thống kê không chọn
		if CHON_TAT_CA_SAN_PHAM == 'False':
			if SAN_PHAM_MANY_IDS == []:
				raise ValidationError('Bạn chưa chọn <Mặt hàng>. Xin vui lòng chọn lại.')
		


	@api.model
	def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
		record = []
		# Get paramerters here
		params = self._context
		if not params.get('active_model'):
			return
		cr = self.env.cr
		chi_nhanh_id = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else -1 
		bao_gom_du_lieu_chi_nhanh_phu_thuoc =  1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHUC_VU' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHUC_VU'] else 0
		tu_ngay = self.get_dbtime('TU')
		den_ngay = self.get_dbtime('DEN')

		# loai_dvt = 0 if 'DON_VI_TINH' in params.keys() and params['DON_VI_TINH_CHINH'] else 0
		loai_dvt_param = params.get('DON_VI_TINH')
		if loai_dvt_param == 'DON_VI_CHUYEN_DOI_1':
			loai_dvt = 1
		elif loai_dvt_param == 'DON_VI_CHUYEN_DOI_2':
			loai_dvt = 2
		else:
			loai_dvt = 0


		ma_kho_id = params['KHO_ID'] if 'KHO_ID' in params.keys() and params['KHO_ID'] != 'False' else -1 
		if ma_kho_id == 'False':
			ma_kho_id = 0
		# ma_hang_ids = tuple([tk['id'] for tk in self.get_context('HANG_ID')])
		MA_PC_NHOM_VTHH = params.get('MA_PC_NHOM_VTHH')
		if params.get('CHON_TAT_CA_SAN_PHAM'):
			domain = []
			if MA_PC_NHOM_VTHH:
				domain += [('LIST_MPC_NHOM_VTHH','ilike', '%'+ MA_PC_NHOM_VTHH +'%')]
			SAN_PHAM_IDS = self.env['danh.muc.vat.tu.hang.hoa'].search(domain).ids
		else:
			SAN_PHAM_IDS = params.get('SAN_PHAM_MANY_IDS')

		loai_tien_chinh = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')],limit=1).id
		dien_giai_dau_ky = 'Số dư đầu kỳ'
		kho_empty_id = 0
		nhom_vthh_id = params['NHOM_VTHH_ID'] if 'NHOM_VTHH_ID' in params.keys() and params['NHOM_VTHH_ID'] != 'False' else -1 
		params = {
			'chi_nhanh_id':chi_nhanh_id, 
			'tu_ngay':tu_ngay, 
			'den_ngay':den_ngay, 
			'loai_dvt':loai_dvt, 
			'ma_kho_id': ma_kho_id, 
			'ma_hang_ids':SAN_PHAM_IDS or None,
			'bao_gom_du_lieu_chi_nhanh_phu_thuoc':bao_gom_du_lieu_chi_nhanh_phu_thuoc,
			'loai_tien_chinh': loai_tien_chinh,
			'dien_giai_dau_ky': dien_giai_dau_ky,
			'kho_empty_id': kho_empty_id,
			'nhom_vthh_id': nhom_vthh_id,
			'limit': limit,
			'offset': offset,
			}      
		
		# Execute SQL query here
		# Step 1: Tính dữ liệu thô 
		query = """
			DO LANGUAGE plpgsql $$
			DECLARE
			
			chi_nhanh_id                        INTEGER :=%(chi_nhanh_id)s;
			
			tu_ngay                             DATE := %(tu_ngay)s;
			
			den_ngay                            DATE := %(den_ngay)s;
			
			loai_dvt                            INTEGER := %(loai_dvt)s;
			
			ma_kho_id                           INTEGER := %(ma_kho_id)s;
			
			bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(bao_gom_du_lieu_chi_nhanh_phu_thuoc)s;
			
			nhom_vthh_id                        INTEGER := %(nhom_vthh_id)s;
			
			
			DIEN_GIAI_DAU_KY                    VARCHAR(100) :=  %(dien_giai_dau_ky)s;
			
			LOAI_TIEN_CHINH                      INTEGER := %(loai_tien_chinh)s;
			
			KHO_TAT_CA                          INTEGER := -1;
			
			SO_TIEN_TON                         FLOAT := 0;
			
			SO_LUONG_TON                        FLOAT := 0;
			
			KHO_TON_ID                          INTEGER := -1;
			
			HANG_TON_ID                         INTEGER := -1;

			RowNum_max                         INTEGER := 0;
						
			
			rec                                 RECORD;
			
			BEGIN


			DROP TABLE IF EXISTS VAT_TU_HANG_HOA
			;

			CREATE TEMP TABLE VAT_TU_HANG_HOA
				AS
					SELECT
						I.id
						, I."MA"
						, I."TEN"
						, I."LIST_NHOM_VTHH"
						, U.id AS "DON_VI_ID"
						, U."DON_VI_TINH"
						, CASE WHEN loai_dvt = 0
									OR loai_dvt IS NULL
						THEN 1
						WHEN IU."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
							THEN 1
						WHEN IU."PHEP_TINH_CHUYEN_DOI" = '*'
							THEN 1 / COALESCE(IU."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
						ELSE COALESCE(IU."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
						END  AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"


					FROM danh_muc_vat_tu_hang_hoa AS I
						LEFT JOIN danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi AS IU ON I."id" = IU."VAT_TU_HANG_HOA_ID"
																					AND IU."STT" = loai_dvt
						LEFT JOIN danh_muc_don_vi_tinh AS U ON ((loai_dvt IS NULL
																OR loai_dvt = 0
																)
																AND I."DVT_CHINH_ID" = U.id
															)
															OR (loai_dvt IS NOT NULL
																AND loai_dvt <> 0
																AND IU."DVT_ID" = U.id
															)
					WHERE (loai_dvt IS NULL
						OR loai_dvt = 0
						OR IU."STT" IS NOT NULL)
											AND ( I.id = any(%(ma_hang_ids)s))
			;


			DROP TABLE IF EXISTS TMP_KET_QUA
			;

			CREATE TEMP TABLE TMP_KET_QUA
				AS

					SELECT
						(row_number()
						OVER (
							ORDER BY S."MA_KHO",
								I."MA",
								CASE
								WHEN IL."NGAY_HACH_TOAN" < tu_ngay
									THEN
										NULL
								ELSE
									IL."NGAY_CHUNG_TU"
								END NULLS FIRST
								, CASE
									WHEN IL."NGAY_HACH_TOAN" < tu_ngay
										THEN
											NULL
									ELSE
										IL."SO_CHUNG_TU"
									END NULLS FIRST,
								CASE
								WHEN IL."NGAY_HACH_TOAN" < tu_ngay
									THEN
										NULL
								ELSE
									IL."ID_CHUNG_TU"
								END NULLS FIRST ) - 1) * 2 + 1 AS "rownum"
						, CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								NULL
						ELSE
							IL."ID_CHUNG_TU"
						END                                     AS "ID_CHUNG_TU"
						, CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								''
						ELSE
							IL."LOAI_CHUNG_TU"
						END
						, S."id"                                  AS "ID_KHO"
						, S."MA_KHO"
						, S."TEN_KHO"
						, I."id"                                  AS "MA_HANG_ID"
						, I."MA"
						, I."TEN"
						, CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								NULL
						ELSE
							IL."NGAY_HACH_TOAN"
						END                                     AS "NGAY_HACH_TOAN"
						, CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								NULL
						ELSE
							IL."NGAY_CHUNG_TU"
						END                                     AS "NGAY_CHUNG_TU"
						, CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								NULL
						ELSE
							IL."SO_CHUNG_TU"
						END                                     AS "SO_CHUNG_TU"
						, CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								DIEN_GIAI_DAU_KY
						ELSE
							IL."DIEN_GIAI_CHUNG"
						END
						, CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								NULL
						ELSE
							IL."MA_TK_CO"
						END
						, I."DON_VI_TINH"
						, CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								LOAI_TIEN_CHINH
						ELSE
							COALESCE("currency_id", LOAI_TIEN_CHINH)
						END                                     AS "currency_id"
						, CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN 0
						WHEN I."DON_VI_ID" = IL."DVT_ID"
							THEN
								IL."DON_GIA"
						ELSE
							IL."DON_GIA_THEO_DVT_CHINH" / I."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
						END                                     AS "DON_GIA"
						, SUM(CASE
							WHEN IL."NGAY_HACH_TOAN" < tu_ngay
								THEN
									0
							WHEN I."DON_VI_ID" = IL."DVT_ID"
								THEN
									IL."SO_LUONG_NHAP"
							ELSE
								IL."SO_LUONG_NHAP_THEO_DVT_CHINH" * I."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
							END
						)                                       AS "SO_LUONG_NHAP"
						, SUM(CASE
							WHEN IL."NGAY_HACH_TOAN" < tu_ngay
								THEN
									0
							ELSE
								IL."SO_TIEN_NHAP"
							END
						)                                       AS "SO_TIEN_NHAP"
						, SUM(CASE
							WHEN IL."NGAY_HACH_TOAN" < tu_ngay
								THEN
									0
							WHEN IL."DVT_ID" = I."DON_VI_ID"
								THEN
									IL."SO_LUONG_XUAT"
							ELSE
								IL."SO_LUONG_XUAT_THEO_DVT_CHINH" * I."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
							END
						)                                       AS "SO_LUONG_XUAT"
						, SUM(CASE
							WHEN IL."NGAY_HACH_TOAN" < tu_ngay
								THEN
									0
							ELSE
								IL."SO_TIEN_XUAT"
							END
						)                                       AS "SO_TIEN_XUAT"
						, SUM(CASE
							WHEN IL."NGAY_HACH_TOAN" >= tu_ngay
								THEN
									0
							WHEN IL."DVT_ID" = I."DON_VI_ID"
								THEN
									IL."SO_LUONG_NHAP" - IL."SO_LUONG_XUAT"
							ELSE
								(IL."SO_LUONG_NHAP_THEO_DVT_CHINH" - IL."SO_LUONG_XUAT_THEO_DVT_CHINH") *
								I."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
							END
						)                                       AS "SO_LUONG_TON_KQ"
						, SUM(CASE
							WHEN IL."NGAY_HACH_TOAN" >= tu_ngay
								THEN
									0
							ELSE
								IL."SO_TIEN_NHAP" - IL."SO_TIEN_XUAT"
							END
						)                                       AS "SO_TIEN_TON_KQ"
						, CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								1
						ELSE
							0
						END
						, MAX(IL."THU_TU_TRONG_CHUNG_TU")         AS "THU_TU_TRONG_CHUNG_TU"
						, 0                                       AS "RownumTemp" --Dùng để sắp xếp các dòng số dư đầu kỳ =0
						, CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								NULL
						ELSE
							IL."MODEL_CHUNG_TU"
						END                                     AS "MODEL_CHUNG_TU"
					FROM so_kho_chi_tiet IL
						INNER JOIN danh_muc_kho S ON IL."KHO_ID" = S.id
						INNER JOIN VAT_TU_HANG_HOA I ON IL."MA_HANG_ID" = I.id
						INNER JOIN danh_muc_to_chuc OU ON OU.id = IL."CHI_NHANH_ID"
					WHERE "NGAY_HACH_TOAN" <= den_ngay
						AND
						(IL."KHO_ID" = ma_kho_id OR ma_kho_id = ma_kho_id
						OR ma_kho_id = KHO_TAT_CA)
						AND (OU."id" = chi_nhanh_id
							OR (OU."HACH_TOAN_SELECTION" = 'PHU_THUOC'
								AND bao_gom_du_lieu_chi_nhanh_phu_thuoc = 1))


					GROUP BY
						CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								NULL
						ELSE
							IL."ID_CHUNG_TU"
						END,
						CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								NULL
						ELSE
							IL."MODEL_CHUNG_TU"
						END,
						CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								''
						ELSE
							IL."LOAI_CHUNG_TU"
						END
						, S."id"
						, S."MA_KHO"
						, S."TEN_KHO"
						, I."id"
						, I."MA"
						, I."TEN"

						, I."DON_VI_ID"
						--                 , IL."NGAY_HACH_TOAN"
						--                 , IL."DVT_ID"
						--                 , IL."DON_GIA"
						--                 , IL."DON_GIA_THEO_DVT_CHINH"
						--                         , IL."MODEL_CHUNG_TU"
						--                 , I."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
						--         , IL."NGAY_CHUNG_TU"

						, CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								NULL
						ELSE
							IL."NGAY_HACH_TOAN"
						END,
						CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								NULL
						ELSE
							IL."NGAY_CHUNG_TU"
						END,
						CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								NULL
						ELSE
							IL."SO_CHUNG_TU"
						END,
						CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								DIEN_GIAI_DAU_KY
						ELSE
							IL."DIEN_GIAI_CHUNG"
						END,
						CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								NULL
						ELSE
							IL."MA_TK_CO"
						END,
						I."DON_VI_TINH",
						CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								LOAI_TIEN_CHINH
						ELSE
							COALESCE("currency_id", LOAI_TIEN_CHINH)
						END, CASE
							WHEN IL."NGAY_HACH_TOAN" < tu_ngay
								THEN 0
							WHEN I."DON_VI_ID" = IL."DVT_ID"
								THEN
									IL."DON_GIA"
							ELSE
								IL."DON_GIA_THEO_DVT_CHINH" / I."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
							END,
						CASE
						WHEN IL."NGAY_HACH_TOAN" < tu_ngay
							THEN
								1
						ELSE
							0
						END

					ORDER BY S."MA_KHO",
						I."MA",
						"NGAY_CHUNG_TU",
						--INRefOrder,
						"SO_CHUNG_TU",
						"THU_TU_TRONG_CHUNG_TU"
			;

			FOR rec IN
			SELECT *
			FROM TMP_KET_QUA
			ORDER BY "MA_KHO", "MA_HANG_ID" NULLS FIRST, "NGAY_CHUNG_TU" NULLS FIRST, "SO_CHUNG_TU" NULLS FIRST,
				"THU_TU_TRONG_CHUNG_TU", "ID_CHUNG_TU" NULLS FIRST
			LOOP

				SELECT CASE WHEN rec."ID_CHUNG_TU" IS NULL
					THEN rec."SO_TIEN_TON_KQ"
					WHEN KHO_TON_ID <> rec."ID_KHO"
							OR HANG_TON_ID <> rec."MA_HANG_ID"
							THEN rec."SO_TIEN_NHAP" - rec."SO_TIEN_XUAT"
						ELSE SO_TIEN_TON + rec."SO_TIEN_NHAP" - rec."SO_TIEN_XUAT"
						END
				INTO SO_TIEN_TON
			;

				SELECT CASE WHEN rec."ID_CHUNG_TU" IS NULL
					THEN rec."SO_LUONG_TON_KQ"
					WHEN KHO_TON_ID <> rec."ID_KHO"
							OR HANG_TON_ID <> rec."MA_HANG_ID"
						THEN rec."SO_LUONG_NHAP" - rec."SO_LUONG_XUAT"
					ELSE SO_LUONG_TON + rec."SO_LUONG_NHAP" - rec."SO_LUONG_XUAT"
					END
				INTO SO_LUONG_TON
			;

				UPDATE TMP_KET_QUA
				SET "SO_TIEN_TON_KQ" = SO_TIEN_TON
				WHERE "rownum" = rec."rownum"
			;

				UPDATE TMP_KET_QUA
				SET "SO_LUONG_TON_KQ" = SO_LUONG_TON
				WHERE "rownum" = rec."rownum"
			;


				KHO_TON_ID := rec."ID_KHO"
			;

				HANG_TON_ID := rec."MA_HANG_ID"
			;

			END LOOP
			;


			DROP TABLE IF EXISTS TMP_KET_QUA_HANG_TON_KHO
			;

			CREATE TEMP TABLE TMP_KET_QUA_HANG_TON_KHO
				AS
					SELECT
						R."ID_KHO"
						, "MA_KHO"
						, "TEN_KHO"
						, R."MA_HANG_ID"
						, "MA"
						, "TEN"
						, MIN(RowNum) - 1 AS "RowNum"

					FROM TMP_KET_QUA R
					GROUP BY
						R."ID_KHO",
						"MA_KHO",
						"TEN_KHO",
						R."MA_HANG_ID",

						"MA",
						"TEN"
			;

			UPDATE TMP_KET_QUA
			SET "RownumTemp" = "rownum"
			;

			SELECT MAX("rownum")
			INTO rownum_max
			FROM TMP_KET_QUA
			;

			INSERT INTO TMP_KET_QUA
				(
					SELECT
						rownum_max + (row_number()
										OVER () * 2) AS "rownum"
						, NULL                       AS "ID_CHUNG_TU"
						, 0                          AS "LOAI_CHUNG_TU"
						, "ID_KHO"
						, "MA_KHO"
						, "TEN_KHO"
						, "MA_HANG_ID"
						, "MA"
						, "TEN"
						, NULL                       AS "NGAY_HACH_TOAN"
						, NULL                       AS "NGAY_CHUNG_TU"
						, NULL                       AS "SO_CHUNG_TU"
						, DIEN_GIAI_DAU_KY           AS "DIEN_GIAI_CHUNG"
						, NULL                       AS "MA_TK_CO"
						, NULL                       AS "DON_VI_TINH"
						, NULL                       AS "currency_id"
						, 0                          AS "DON_GIA"
						, 0                          AS "SO_LUONG_NHAP"
						, 0                          AS "SO_TIEN_NHAP"
						, 0                          AS "SO_LUONG_XUAT"
						, 0                          AS "SO_TIEN_XUAT"
						, 0                          AS "SO_LUONG_TON_KQ"
						, 0                          AS "SO_TIEN_TON_KQ"
						, 0
						, 0
						, COALESCE(I."RowNum", 0)    AS "RowNumTemp"
					FROM TMP_KET_QUA_HANG_TON_KHO I
					WHERE NOT EXISTS(SELECT 1
									FROM TMP_KET_QUA R
									WHERE R."ID_KHO" = I."ID_KHO"
										AND R."MA_HANG_ID" = I."MA_HANG_ID"
										AND R."ID_CHUNG_TU" IS NULL))
			;

			DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
			;

			CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
				AS
					SELECT
						"ID_CHUNG_TU"
						, "LOAI_CHUNG_TU"
						, "ID_KHO"
						, "MA_KHO"
						, "TEN_KHO"
						, "MA_HANG_ID"
						, "MA"
						, "TEN"
						, "NGAY_HACH_TOAN"
						, "NGAY_CHUNG_TU"
						, "SO_CHUNG_TU"
						, "DIEN_GIAI_CHUNG"
						, "MA_TK_CO"
						, "DON_VI_TINH"
						, CASE WHEN "ID_CHUNG_TU" IS NULL
									AND "SO_LUONG_TON_KQ" <> 0
						THEN "SO_TIEN_TON_KQ" / "SO_LUONG_TON_KQ"
						WHEN "ID_CHUNG_TU" IS NOT NULL
							THEN CASE WHEN "LOAI_CHUNG_TU" IN ('3030', '3031')
											AND "currency_id" <> LOAI_TIEN_CHINH
								THEN CASE WHEN "SO_LUONG_NHAP" > 0
									THEN "SO_TIEN_NHAP" / "SO_LUONG_NHAP"
									WHEN "SO_LUONG_XUAT" > 0
										THEN "SO_TIEN_XUAT" / "SO_LUONG_XUAT"
									ELSE 0
									END
								ELSE "DON_GIA"
								END
						END                             AS "DON_GIA"

						, "SO_LUONG_NHAP"
						, "SO_TIEN_NHAP"
						, "SO_LUONG_XUAT"
						, "SO_TIEN_XUAT"
						, "SO_LUONG_TON_KQ"
						, "SO_TIEN_TON_KQ"
						, ROW_NUMBER()
						OVER (
							ORDER BY "RownumTemp" ASC ) AS "RowNum"
						, "THU_TU_TRONG_CHUNG_TU"
						, "MODEL_CHUNG_TU"


					FROM TMP_KET_QUA R

					WHERE ("ID_CHUNG_TU" IS NULL
						AND (
							--Lấy lên số dư đầu kỳ <> 0
							("SO_TIEN_TON_KQ" <> 0
								OR "SO_LUONG_TON_KQ" <> 0
							)
							--Chỉ lấy những dòng số dư đầu kỳ =0 khi có phát sinh trong kỳ
							OR EXISTS(SELECT 1
										FROM TMP_KET_QUA r1
										WHERE R1."ID_KHO" = R."ID_KHO"
											AND R1."MA_HANG_ID" = R."MA_HANG_ID"
											AND r1."ID_CHUNG_TU" IS NOT NULL)
						)
						-- Nếu không phát sinh một vật tư nào đó trong trong kỳ thì không được xuất khẩu Excel Extend cái dòng đầu kỳ

						OR ("ID_CHUNG_TU" IS NOT NULL
							AND ("SO_LUONG_NHAP" <> 0
									OR "SO_TIEN_NHAP" <> 0
									OR "SO_LUONG_XUAT" <> 0
									OR "SO_TIEN_XUAT" <> 0
									OR "SO_LUONG_TON_KQ" <> 0
									OR "SO_TIEN_TON_KQ" <> 0
							)
						))
			;

		END $$
		;



			SELECT *
			FROM TMP_KET_QUA_CUOI_CUNG
			OFFSET %(offset)s
			LIMIT %(limit)s;

		"""
		cr.execute(query,params)
		for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
			record.append({
				'CHUNG_TU_SO_HIEU': line.get('SO_CHUNG_TU', ''),
				'MA_HANG_TEN_HANG': line.get('MA', '') + ' - ' +line.get('TEN', ''),
				'MA_HANG': line.get('MA', '') ,
				'TEN_HANG': line.get('TEN', ''),
				'CHUNG_TU_NGAY_THANG': line.get('NGAY_CHUNG_TU', ''),
				'DIEN_GIAI': line.get('DIEN_GIAI_CHUNG', ''),
				'TAI_KHOAN_DOI_UNG': line.get('MA_TK_CO', ''),
				'DVT': line.get('DON_VI_TINH', ''),
				'DON_GIA': line.get('DON_GIA', 0),
				'SO_LUONG_NHAP': line.get('SO_LUONG_NHAP', 0),
				'SO_TIEN_NHAP': line.get('SO_TIEN_NHAP', 0),
				'SO_LUONG_XUAT': line.get('SO_LUONG_XUAT', 0),
				'SO_TIEN_XUAT': line.get('SO_TIEN_XUAT', 0),
				'SO_LUONG_TON': line.get('SO_LUONG_TON_KQ', 0),
				'SO_TIEN_TON': line.get('SO_TIEN_TON_KQ', 0),
				'KHO_ID': line.get('ID_KHO'),
				'MA_HANG_ID': line.get('MA_HANG_ID'),
				'ID_GOC': line.get('ID_CHUNG_TU', ''),
				'MODEL_GOC': line.get('MODEL_CHUNG_TU', ''),
				'MA_KHO_TEN_KHO':  line.get('MA_KHO', '') + ' - ' +line.get('TEN_KHO', ''),
				'MA_KHO':  line.get('MA_KHO', ''),
				'MA_KHO_TEN_KHO': line.get('TEN_KHO', ''),
				})
		
		
		return record

	### END IMPLEMENTING CODE ###

	def _action_view_report(self):
		self._validate()
		action = self.env.ref('bao_cao.open_report__s10_dn_so_chi_tiet_vat_lieu_cong_cu').read()[0]
		# action['options'] = {'clear_breadcrumbs': True}
		return action

	@api.onchange('KY_BAO_CAO')
	def _cap_nhat_ngay(self):
		self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')

class BAO_CAO_S10_DN_SO_CHI_TIET_VAT_LIEU_CONG_CU_GROUP_KHO_REPORT(models.Model):
	_name = 'bao.cao.s10.dn.so.chi.tiet.vat.lieu.cong.cu.group.kho'
	_auto = False
	_description = 'Nhóm sổ chi tiết theo kho'

	MA_KHO = fields.Char()
	TEN_KHO = fields.Char()
	sum_SO_TIEN_NHAP = fields.Monetary()
	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh())
	data = fields.One2many('bao.cao.s10.dn.so.chi.tiet.vat.lieu.cong.cu.group.vthh', 'GROUP_KHO')

class BAO_CAO_S10_DN_SO_CHI_TIET_VAT_LIEU_CONG_CU_GROUP_VTHH_REPORT(models.Model):
	_name = 'bao.cao.s10.dn.so.chi.tiet.vat.lieu.cong.cu.group.vthh'
	_auto = False
	_description = 'Nhóm sổ chi tiết theo vật tư hàng hóa'

	MA_HANG = fields.Char()
	TEN_HANG = fields.Char()
	sum_SO_TIEN_NHAP = fields.Monetary()
	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh())
	GROUP_KHO = fields.Many2one('bao.cao.s10.dn.so.chi.tiet.vat.lieu.cong.cu.group.kho')
	data = fields.One2many('bao.cao.s10.dn.so.chi.tiet.vat.lieu.cong.cu', 'GROUP_VTHH')

class BAO_CAO_S10_DN_SO_CHI_TIET_VAT_LIEU_CONG_CU_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_s10_dn_so_chi_tiet_vat_lieu_cong_cu'
	
	@api.model
	def get_report_values(self, docids, data=None):
		env = self.env[data.get('model')]
		docs = [d for d in env.with_context(data.get('context')).search_read()]
		
		grouped_data = {}
		result = []
		# grouped_data_key = {}
		for record in docs:
			kho_key = record.get('MA_KHO_TEN_KHO')
			if kho_key not in grouped_data:
				grouped_data[kho_key] = {
					'data': {},
					'MA_KHO': record.get('MA_KHO'),
					'TEN_KHO': record.get('TEN_KHO'),
					'sum_SO_TIEN_NHAP': 0,
				}
			hang_key = record.get('MA_HANG_TEN_HANG')
			if hang_key not in grouped_data[kho_key]['data']:
				grouped_data[kho_key]['data'][hang_key] = {
					'data': [],
					'MA_HANG': record.get('MA_HANG'),
					'TEN_HANG': record.get('TEN_HANG'),
					'sum_SO_TIEN_NHAP': 0,					
				}
			
			
			grouped_data[kho_key]['sum_SO_TIEN_NHAP'] += record.get('SO_TIEN_NHAP')
			grouped_data[kho_key]['data'][hang_key]['sum_SO_TIEN_NHAP'] += record.get('SO_TIEN_NHAP')
			grouped_data[kho_key]['data'][hang_key]['data'] += [record]

		for k in grouped_data:
			kho = grouped_data.get(k)
			data_line_kho = []
			for h in kho.get('data'):
				hang = kho.get('data').get(h)
				data_line_hang = []
				for h in hang.get('data'):
					data_line_hang += [[0,0,h]]
				data_line_kho += [[0,0,{
					'MA_HANG': hang.get('MA_HANG'),
					'TEN_HANG': hang.get('TEN_HANG'),
					'sum_SO_TIEN_NHAP': hang.get('sum_SO_TIEN_NHAP'),
					'data': data_line_hang
				}]]

			result += self.env['bao.cao.s10.dn.so.chi.tiet.vat.lieu.cong.cu.group.kho'].new({
				'MA_KHO': kho.get('MA_KHO'),
				'TEN_KHO': kho.get('TEN_KHO'),
				'sum_SO_TIEN_NHAP': kho.get('sum_SO_TIEN_NHAP'),
				'data': data_line_kho
			})

		added_data = {
			'tieu_de_nguoi_ky': self.get_danh_sach_tieu_de_nguoi_ky(data.get('model')),
			'ten_nguoi_ky': self.get_danh_sach_ten_nguoi_ky(data.get('model')),
			'sub_title': data.get('breadcrumb'),
		}
			
		return {
			'docs': docs,
			'grouped_data': result,
			'added_data': added_data,
			'o': self,
		}