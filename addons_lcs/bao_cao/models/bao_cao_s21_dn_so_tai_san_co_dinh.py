# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_S21_DN_SO_TAI_SAN_CO_DINH(models.Model):
		_name = 'bao.cao.s21.dn.so.tai.san.co.dinh'
		
		
		_auto = False

		CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
		BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
		KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default='DAU_THANG_DEN_HIEN_TAI',required='True')
		TU = fields.Date(string='Từ', help='Từ',default=fields.Datetime.now)
		DEN = fields.Date(string='Đến', help='Đến',default=fields.Datetime.now)
		LOAI_TSCD_ID = fields.Many2one('danh.muc.loai.tai.san.co.dinh', string='Loại TSCĐ', help='Loại tài sản cố định')
		DON_VI_SU_DUNG_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị sử dụng', help='Đơn vị sử dụng')
		STT = fields.Integer(string='STT', help='Số thứ tự')
		SO_HIEU_CHUNG_TU = fields.Char(string='Số hiệu', help='Số hiệu chứng từ')
		NGAY_THANG_CHUNG_TU = fields.Date(string='Ngày tháng', help='Ngày tháng chứng từ')
		NUOC_SAN_XUAT = fields.Char(string='Nước sản xuất', help='Nước sản xuất')
		THANG_NAM_DUA_VAO_SU_DUNG = fields.Char(string='Tháng năm đưa vào sử dụng', help='Tháng năm đưa vào sử dụng')
		SO_HIEU_TSCD = fields.Char(string='Số hiệu TSCĐ', help='Số hiệu tài sản cố định')
		NGUYEN_GIA = fields.Float(string='Nguyên giá', help='Nguyên giá',digits=decimal_precision.get_precision('VND'))
		GIA_TRI_TINH_KH = fields.Float(string='Giá trị tính KH', help='Giá trị tính kh', digits=decimal_precision.get_precision('VND'))
		TY_LE_PHAN_TRAM_KHAU_HAO = fields.Float(string='Tỷ lệ phần trăm khấu hao', help='Tỷ lệ phần trăm khấu hao')
		KHAU_HAO_LUY_KE = fields.Float(string='Khấu hao lũy kế', help='Khấu hao lũy kế', digits=decimal_precision.get_precision('VND'))
		KHAU_HAO = fields.Float(string='Khấu hao', help='Khấu hao', digits=decimal_precision.get_precision('VND'))
		SO_HIEU_CHUNG_TU_GHI_GIAM = fields.Char(string='Số hiệu ', help='Số hiệu chứng từ ghi giảm')
		NGAY_THANG_CHUNG_TU_GHI_GIAM = fields.Date(string='Ngày tháng ', help='Ngày tháng chứng từ ghi giảm')
		LY_DO_GIAM_TSCD = fields.Char(string='Lý do giảm TSCĐ', help='Lý do giảm tài sản cố định')
		MA_TSCD = fields.Char(string='Mã TSCĐ', help='Mã tài sản cố định')

		ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
		MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')



		#FIELD_IDS = fields.One2many('model.name')

		### START IMPLEMENTING CODE ###
		@api.model
		def default_get(self, fields_list):
			result = super(BAO_CAO_S21_DN_SO_TAI_SAN_CO_DINH, self).default_get(fields_list)
			chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
			if chi_nhanh:
				result['CHI_NHANH_ID'] = chi_nhanh.id
			return result

		# @api.onchange('field_name')
		# def _cap_nhat(self):
		#     for item in self:
		#         item.FIELDS_IDS = self.env['model_name'].search([])

		def _validate(self):
				TU = self.get_dbtime('TU')
				DEN = self.get_dbtime('DEN')
				if(not TU):
						raise ValidationError('<Từ ngày> không được bỏ trống.')
				if(not DEN):
						raise ValidationError('<Đến ngày> không được bỏ trống.')
				if (TU > DEN):
						raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')
		@api.model
		def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
				record = []
				# Get paramerters here
				params = self._context
				if not params.get('active_model'):
						return

				# TAI_KHOAN_ID = params['TAI_KHOAN_ID'] if 'TAI_KHOAN_ID' in params.keys() and params['TAI_KHOAN_ID'] != 'False' else -1 
				CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else -1 
				BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] else 0
				KY_BAO_CAO = params['KY_BAO_CAO'] if 'KY_BAO_CAO' in params.keys() else 'False'
				TU = params['TU'] if 'TU' in params.keys() else 'False'
				DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
				LOAI_TSCD_ID = params['LOAI_TSCD_ID'] if 'LOAI_TSCD_ID' in params.keys() and params['LOAI_TSCD_ID'] != 'False' else -1 
				DON_VI_SU_DUNG_ID = params['DON_VI_SU_DUNG_ID'] if 'DON_VI_SU_DUNG_ID' in params.keys() and params['DON_VI_SU_DUNG_ID'] != 'False' else -1 
				TU_NGAY = self.get_dbtime('TU')
				DEN_NGAY = self.get_dbtime('DEN')
				MA_PHAN_CAP = ''
				dv_sd = ''
				if DON_VI_SU_DUNG_ID != 'False':
					MA_PHAN_CAP = self.env['danh.muc.to.chuc'].search([('id', '=', DON_VI_SU_DUNG_ID)], limit=1).MA_PHAN_CAP
					dv_sd = 'True'
				else:
					dv_sd = 'False'
				loai_tscd = ''
				chi_nhanh = ''


				if LOAI_TSCD_ID != 'False':
					loai_tscd = 'True'
				else:
					loai_tscd = 'False'
	
				params = {
						'CHI_NHANH_ID':CHI_NHANH_ID,
						'TU_NGAY':TU_NGAY, 
						'DEN_NGAY':DEN_NGAY, 
						'LOAI_TSCD_ID':LOAI_TSCD_ID, 
						'DON_VI_SU_DUNG_ID': DON_VI_SU_DUNG_ID, 
						'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC, 
						'MA_PHAN_CAP' : MA_PHAN_CAP,
						}      
				# Execute SQL query here
				cr = self.env.cr
				query = """
				DO LANGUAGE plpgsql $$
				DECLARE

					chi_nhanh                           INTEGER :=%(CHI_NHANH_ID)s;
					TU_NGAY                             DATE := %(TU_NGAY)s;
					DEN_NGAY                            DATE := %(DEN_NGAY)s;
					loai_tscd                           INTEGER := %(LOAI_TSCD_ID)s;
					dv_sd                               INTEGER := %(DON_VI_SU_DUNG_ID)s;
					BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC INTEGER :=%(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

					rec                                 RECORD;
					MA_PHAN_CAP_DON_VI                  VARCHAR(100);
					MA_PHAN_CAP_LOAI_TAI_SAN            VARCHAR(100);


			 BEGIN
						
								IF dv_sd <> -1
								THEN
										SELECT concat("MA_PHAN_CAP", '%%')
										INTO MA_PHAN_CAP_DON_VI
										FROM danh_muc_to_chuc
						
										WHERE id = dv_sd
										;
						
								END IF
								;
						
								IF loai_tscd <> -1
								THEN
										SELECT concat("MA_PHAN_CAP", '%%')
										INTO MA_PHAN_CAP_LOAI_TAI_SAN
										FROM danh_muc_loai_tai_san_co_dinh
						
										WHERE id = loai_tscd
										;
						
								END IF
								;
						
						
								DROP TABLE IF EXISTS TMP_KET_QUA
								;
						
								CREATE TEMP TABLE TMP_KET_QUA (
						
										"ID_CHUNG_TU"               INTEGER,
										"LOAI_CHUNG_TU"             INTEGER,
										"LOAI_TSCD_ID"              INTEGER,
										"MA_LOAI_TSCD"              VARCHAR(127),
										"NGAY_GHI_TANG"             DATE,
										"TY_LE_TINH_KHAU_HAO_THANG" FLOAT,
										"NGUYEN_GIA"                FLOAT,
										"KHAU_HAO_LUY_KE"           FLOAT, -- DepreciationAmount
										"TSCD_ID"                   INTEGER,
										"NGAY_CHUNG_TU"             DATE,
										"TEN_LOAI_TSCD"             VARCHAR(500),
										"NUOC_SAN_XUAT"             VARCHAR(200),
										"SO_HIEU"                   VARCHAR(200),
										"MA_TAI_SAN"                VARCHAR(500),
										"TEN_TSCD"                  VARCHAR(500),
						
										"GIA_TRI_TINH_KHAU_HAO"     FLOAT,
										"HAO_MON_LUY_KE"            FLOAT ,--AccumDepreciationAmount
						
						
						
										"NGAY_THANG_DUA_VAO_SD"              VARCHAR(500)
						
								)
								;
						
								INSERT INTO TMP_KET_QUA (
										SELECT
													FA.id                        AS "ID_CHUNG_TU"
												, FA."LOAI_CHUNG_TU"
												, FA."LOAI_TAI_SAN_ID"         AS "LOAI_TSCD_ID"
												, FAC."MA"                     AS "MA_LOAI_TSCD"
												, FA."NGAY_GHI_TANG"
												, FA."TY_LE_TINH_KHAU_HAO_THANG"
												, FA."NGUYEN_GIA"
												, CASE WHEN FA."NGAY_GHI_TANG" >= TU_NGAY
												THEN FA."HAO_MON_LUY_KE"
													ELSE 0
													END                          AS "KHAU_HAO_LUY_KE"
												, FA.id                        AS "TSCD_ID"
												, CASE WHEN FA."NGAY_GHI_TANG" < TU_NGAY
												THEN NULL
													ELSE FA."NGAY_GHI_TANG" END  AS "NGAY_CHUNG_TU"
												, FAC."TEN"                    AS "TEN_LOAI_TSCD"
												, FA."NUOC_SAN_XUAT"
												, CASE WHEN FA."NGAY_GHI_TANG" < TU_NGAY
												THEN NULL
													ELSE FA."SO_CT_GHI_TANG" END AS "SO_HIEU"
												, FA."MA_TAI_SAN"
												, FA."TEN_TAI_SAN"             AS "TEN_TSCD"
												, CASE WHEN FA."NGAY_GHI_TANG" >= TU_NGAY
												THEN FA."GIA_TRI_TINH_KHAU_HAO"
													ELSE 0 -- FLL."GIA_TRI_TINH_KHAU_HAO"
													END                          AS "GIA_TRI_TINH_KHAU_HAO"
												, FA."HAO_MON_LUY_KE"
						
												, concat(CASE WHEN EXTRACT(MONTH  FROM FA."NGAY_BAT_DAU_TINH_KH") < 10 THEN '0'
																				 ELSE ''
																		END ,CAST(EXTRACT(MONTH  FROM FA."NGAY_BAT_DAU_TINH_KH" ) AS VARCHAR)
																		, '/' ,  CAST(EXTRACT(YEAR  FROM FA."NGAY_BAT_DAU_TINH_KH" )  AS VARCHAR)) AS "NGAY_THANG_DUA_VAO_SD"
						
						
										FROM asset_ghi_tang FA
												LEFT JOIN danh_muc_loai_tai_san_co_dinh FAC ON FAC.id = FA."LOAI_TAI_SAN_ID"
												INNER JOIN LATERAL (
																	 SELECT
																			 OU."MA_PHAN_CAP"
																			 , FL."DON_VI_SU_DUNG_ID" -- Lấy lên đơn vị sử dụng cuối cùng của tài sản
																	 FROM so_tscd_chi_tiet FL
																			 INNER JOIN danh_muc_to_chuc OU ON OU.id = FL."DON_VI_SU_DUNG_ID"
																			 INNER JOIN (SELECT *
																									 FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh,
																																								BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)) AS TLB
																					 ON FL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
																	 WHERE FL."TSCD_ID" = FA.id
																				 AND FL."NGAY_HACH_TOAN" <= DEN_NGAY
																	 ORDER BY FL."NGAY_HACH_TOAN" DESC
																	 FETCH FIRST 1 ROW ONLY
																	 ) FL ON TRUE
										WHERE
												(loai_tscd = -1
												 OR (FAC."MA_PHAN_CAP" LIKE MA_PHAN_CAP_LOAI_TAI_SAN)
												)
												AND ((dv_sd = -1
															AND FL."DON_VI_SU_DUNG_ID" IS NOT NULL
														 )
														 OR (FL."MA_PHAN_CAP" LIKE MA_PHAN_CAP_DON_VI)
												)
						
												AND
												FA.id NOT IN (
														SELECT "MA_TAI_SAN"
														FROM asset_ghi_giam_tai_san AS FAD
																INNER JOIN asset_ghi_giam AS FD
																		ON FAD."TAI_SAN_CO_DINH_GHI_GIAM_ID" = FD.id
														WHERE
						
																((FD."state" = 'da_ghi_so')
																)
																AND FD."CHI_NHANH_ID" = chi_nhanh
																AND FD."NGAY_HACH_TOAN" < TU_NGAY
						
												)
						
								)
								;
						
								--   UPDATE Nguyên giá, Hao mòn lũy kế và giá trị tính khấu hao cho tài sản có ngày ghi tăng trước ngày FromDate
								UPDATE TMP_KET_QUA
								SET "NGUYEN_GIA"                = (SELECT FL."NGUYEN_GIA"
						
																									 FROM so_tscd_chi_tiet FL
																									 WHERE FL."TSCD_ID" = TMP_KET_QUA."TSCD_ID"
																												 AND FL."NGAY_HACH_TOAN" < TU_NGAY
						
																									 ORDER BY FL."NGAY_HACH_TOAN" DESC
						
																									 LIMIT 1
								),
										"HAO_MON_LUY_KE"            = (SELECT FL."GIA_TRI_HAO_MON_LUY_KE"
						
																									 FROM so_tscd_chi_tiet FL
																									 WHERE FL."TSCD_ID" = TMP_KET_QUA."TSCD_ID"
																												 AND FL."NGAY_HACH_TOAN" < TU_NGAY
						
																									 ORDER BY FL."NGAY_HACH_TOAN" DESC
						
																									 LIMIT 1
										),
						
										"GIA_TRI_TINH_KHAU_HAO"     = (SELECT FL."GIA_TRI_TINH_KHAU_HAO"
						
																									 FROM so_tscd_chi_tiet FL
																									 WHERE FL."TSCD_ID" = TMP_KET_QUA."TSCD_ID"
																												 AND FL."NGAY_HACH_TOAN" < TU_NGAY
						
																									 ORDER BY FL."NGAY_HACH_TOAN" DESC
						
																									 LIMIT 1
										),
										"TY_LE_TINH_KHAU_HAO_THANG" = (SELECT FL."TY_LE_KHAU_HAO_THANG"
						
																									 FROM so_tscd_chi_tiet FL
																									 WHERE FL."TSCD_ID" = TMP_KET_QUA."TSCD_ID"
																												 AND FL."NGAY_HACH_TOAN" < TU_NGAY
						
																									 ORDER BY FL."NGAY_HACH_TOAN" DESC
																									 --                   FL.RefOrder DESC
																									 LIMIT 1
										)
								--   FROM TMP_KET_QUA FA
								--     INNER JOIN LATERAL ( SELECT
								--                            FL."NGUYEN_GIA",
								--                            FL."GIA_TRI_HAO_MON_LUY_KE"
								--                            + FL."CHENH_LECH_GIA_TRI_HAO_MON_LUY_KE" AS GIA_TRI_HAO_MON_LUY_KE,
								--                            FL."GIA_TRI_TINH_KHAU_HAO",
								--                            FL."TY_LE_KHAU_HAO_THANG"
								--                          FROM so_tscd_chi_tiet FL
								--                          WHERE FL.id = FA.id
								--                                AND FL."NGAY_HACH_TOAN" < TU_NGAY
								--
								--                          ORDER BY FL."NGAY_HACH_TOAN" DESC
								--                          --                   FL.RefOrder DESC
								--                          FETCH FIRST 1 ROW ONLY
								--                ) FL ON TRUE
								WHERE "NGAY_GHI_TANG" < TU_NGAY
								;
						
								--
								--     --SELECT * FROM #tblFixedAsset FA
								DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
								;
						
								CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
										AS
												SELECT
														"ID_CHUNG_TU"
														, "LOAI_CHUNG_TU"
														, "LOAI_TSCD_ID"
														, "MA_LOAI_TSCD"
														, "TY_LE_TINH_KHAU_HAO_THANG"
														, "NGUYEN_GIA"
														, 0            AS "KHAU_HAO"
														, "TSCD_ID"
														, "NGAY_CHUNG_TU"
														, "TEN_LOAI_TSCD"
														, "NUOC_SAN_XUAT"
														, "SO_HIEU"
														, "MA_TAI_SAN"
														, "TEN_TSCD"
														, "GIA_TRI_TINH_KHAU_HAO"
														, "KHAU_HAO_LUY_KE"
														, ''           AS "SO_HIEU_GHI_GIAM"
														, NULL :: DATE AS "NGAY_THANG_CHUNG_TU_GHI_GIAM"
														, ''           AS "LY_DO_GIAM_TSCD"
														, 1            AS "THU_TU_TRONG_CHUNG_TU"
														, NULL :: INT  AS "ID_GOC"
														, ''           AS "MODEL_GOC"
													 ,  "NGAY_THANG_DUA_VAO_SD"
						
												FROM TMP_KET_QUA
												UNION ALL
						
												SELECT
														FAL."ID_CHUNG_TU"
														, FAL."LOAI_CHUNG_TU"
														, FAA."LOAI_TSCD_ID"
														, FAA."MA_LOAI_TSCD"
														, CASE WHEN FAL."LOAI_CHUNG_TU" = 251
																				OR FAL."THOI_GIAN_SU_DUNG" + FAL."CHENH_LECH_THOI_GIAN_SU_DUNG" = 0
														--                          - FAL.SumMonthly = 0 -- OR THOI_GIAN_SU_DUNG_CON_LAI
														THEN 0
															ELSE FAL."TY_LE_KHAU_HAO_THANG"
															END                         AS "TY_LE_TINH_KHAU_HAO_THANG"
														, FAL."CHENH_LECH_NGUYEN_GIA" AS "NGUYEN_GIA"
														, CASE WHEN FAL."LOAI_CHUNG_TU" = 254
														THEN FAL."GIA_TRI_KHAU_HAO_THANG_KHI_KH"
															WHEN FAL."LOAI_CHUNG_TU" IN (252, 256)
																	THEN COALESCE(FAL."CHENH_LECH_GIA_TRI_HAO_MON_LUY_KE", 0)
															ELSE 0
															END                         AS "KHAU_HAO"
														, -- Hao mòn tháng,
						
						
														FAL."TSCD_ID"
														, CASE WHEN FAL."LOAI_CHUNG_TU" = 251
														THEN NULL
															ELSE COALESCE(FAL."NGAY_HACH_TOAN", FAL."NGAY_CHUNG_TU")
						
															END                         AS "NGAY_CHUNG_TU"
														, FAA."TEN_LOAI_TSCD"
														, ''                          AS "NUOC_SAN_XUAT"
														, CASE WHEN FAL."LOAI_CHUNG_TU" = 251
														THEN ''
															ELSE FAL."SO_CHUNG_TU"
						
															END                         AS "SO_HIEU"
														, FAA."MA_TAI_SAN"
														, FAA."TEN_TSCD"
														, -- Tỷ lệ khấu hao tháng
														-- Khấu hao	-- Đánh giá lại và chuyển TS thuê TC thì lấy Cột chênh lệch
						
														 COALESCE(FAL."CHENH_LENH_GIA_TRI_TINH_KHAU_HAO",0) AS "GIA_TRI_KHAU_HAO_THANG" -- Hao mòn tháng,
						
														--   -- Khấu hao lũy kế
														, CASE WHEN FAL."LOAI_CHUNG_TU" = 251
														THEN FAL."GIA_TRI_TINH_KHAU_HAO" - FAL."GIA_TRI_CON_LAI"
															ELSE COALESCE(FAL."GIA_TRI_HAO_MON_LUY_KE", 0)
																	 + COALESCE(FAL."CHENH_LECH_GIA_TRI_HAO_MON_LUY_KE", 0)
															END                         AS "KHAU_HAO_LUY_KE"
														, CASE WHEN FAl."LOAI_CHUNG_TU" = 251
														THEN FAL."SO_CHUNG_TU"
															ELSE ''
															END                         AS "SO_HIEU_GHI_GIAM"
														, CASE WHEN FAl."LOAI_CHUNG_TU" = 251
														THEN FAL."NGAY_CHUNG_TU"
															ELSE NULL
															END                         AS "NGAY_THANG_CHUNG_TU_GHI_GIAM"
														, CASE WHEN FAL."LOAI_CHUNG_TU" = 251
														THEN FAL."DIEN_GIAI_CHUNG"
															ELSE ''
															END                         AS "LY_DO_GIAM_TSCD"
														, CASE WHEN FAL."LOAI_CHUNG_TU" = 251
														THEN 3
															ELSE 2
															END                         AS "THU_TU_TRONG_CHUNG_TU"
														, FAL."ID_CHUNG_TU"           AS "ID_GOC"
														, FAL."MODEL_CHUNG_TU"        AS "MODEL_GOC"
														, ''             AS "NGAY_THANG_DUA_VAO_SD"
						
						
												FROM so_tscd_chi_tiet FAL INNER JOIN TMP_KET_QUA FAA ON FAA."TSCD_ID" = FAL."TSCD_ID"
														INNER JOIN (SELECT *
																				FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh, BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)) AS TLB
																ON FAL."CHI_NHANH_ID" = TLB."CHI_NHANH_ID"
						
						
												WHERE
														FAL."NGAY_HACH_TOAN" BETWEEN TU_NGAY AND DEN_NGAY
														AND
														FAL."LOAI_CHUNG_TU" NOT IN (253, 255, 250, 615)
						
												ORDER BY
														"MA_LOAI_TSCD",
														"THU_TU_TRONG_CHUNG_TU"
								;
						
						
						END $$
						;
						
						SELECT *
						FROM TMP_KET_QUA_CUOI_CUNG
						
						
						;
				"""
				cr.execute(query,params)
				# Get and show result
				stt = 0
				for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
						stt += 1
						record.append({
								'STT': stt,
								'SO_HIEU_CHUNG_TU': line.get('SO_HIEU', ''),
								'NGAY_THANG_CHUNG_TU': line.get('NGAY_CHUNG_TU', ''),
								'NUOC_SAN_XUAT': line.get('NUOC_SAN_XUAT', ''),
								'THANG_NAM_DUA_VAO_SU_DUNG': line.get('NGAY_THANG_DUA_VAO_SD', ''),
								'SO_HIEU_TSCD': '',
								'NGUYEN_GIA': line.get('NGUYEN_GIA', ''),
								'GIA_TRI_TINH_KH': line.get('GIA_TRI_TINH_KHAU_HAO', ''),
								'TY_LE_PHAN_TRAM_KHAU_HAO': line.get('TY_LE_TINH_KHAU_HAO_THANG', ''),
								'KHAU_HAO_LUY_KE': line.get('KHAU_HAO_LUY_KE', ''),
								'KHAU_HAO': line.get('KHAU_HAO', ''),
								'SO_HIEU_CHUNG_TU_GHI_GIAM': line.get('SO_HIEU_GHI_GIAM', ''),
								'NGAY_THANG_CHUNG_TU_GHI_GIAM': line.get('NGAY_THANG_CHUNG_TU_GHI_GIAM', ''),
								'LY_DO_GIAM_TSCD': line.get('LY_DO_GIAM_TSCD', ''),
								'MA_TSCD': line.get('MA_TAI_SAN', ''),
								'ID_GOC': line.get('ID_GOC', ''),
								'MODEL_GOC': line.get('MODEL_GOC', ''),
								})
				return record

		### END IMPLEMENTING CODE ###

		def _action_view_report(self):
				self._validate()
				action = self.env.ref('bao_cao.open_report_s21_dn_so_tai_san_co_dinh').read()[0]
				# action['options'] = {'clear_breadcrumbs': True}
				return action
		
		@api.onchange('KY_BAO_CAO')
		def _cap_nhat_ngay(self):
				self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')
	
class BAO_CAO_S21_DN_SO_TAI_SAN_CO_DINH_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_s21_dn_so_tai_san_co_dinh'

	@api.model
	def get_report_values(self, docids, data=None):
		env = self.env[data.get('model')]
		docs = [env.new(d) for d in env.with_context(data.get('context')).search_read()]
		
		grouped_data = {}

		added_data = {
			'tieu_de_nguoi_ky': self.get_danh_sach_tieu_de_nguoi_ky(data.get('model')),
			'ten_nguoi_ky': self.get_danh_sach_ten_nguoi_ky(data.get('model')),
			'sub_title': data.get('breadcrumb'),

		}

		return {
			'docs': docs,
			'grouped_data': grouped_data,
			'added_data': added_data,
			'o': self,
		}