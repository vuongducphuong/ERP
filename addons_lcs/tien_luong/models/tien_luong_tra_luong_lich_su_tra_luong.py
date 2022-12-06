# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from odoo.exceptions import ValidationError

class TIEN_LUONG_LICH_SU_TRA_LUONG_FORM(models.Model):
	_name = 'tien.luong.lich.su.tra.luong.form'
	_description = ''
	_auto = False

	NHAN_VIEN_ID = fields.Many2one('res.partner',string='Nhân viên')
	name = fields.Char(string='Name', help='Name', oldname='NAME')
	
	TIEN_LUONG_LICH_SU_TRA_LUONG_FORM_CHI_TIET_IDS = fields.One2many('tien.luong.lich.su.tra.luong.form.chi.tiet', 'CHI_TIET_ID', string='Trả lương form tham số chi tiết')

	@api.model
	def lay_du_lieu_lich_su_tra_luong(self, args):
		new_line = [[5]]
		# if args.get('kho_id'):
		# 	kho_id = args.get('kho_id')
		# else:
		# 	kho_id = self.env['danh.muc.kho'].search([],limit=1).id
		# lich_su_tra_luong = self.ham_tra_du_lieu_sql_lich_su_tra_luong()
		# if lich_su_tra_luong:
		# 	for lstl in lich_su_tra_luong:
		# 		new_line += [(0,0,{
		# 			'NGAY_HACH_TOAN': lstl.get('NGAY_HACH_TOAN'),
		# 			'NGAY_CHUNG_TU': lstl.get('NGAY_CHUNG_TU'),
		# 			'SO_CHUNG_TU': lstl.get('SO_CHUNG_TU'),
		# 			'DIEN_GIAI' : lstl.get('DIEN_GIAI'),
		# 			'SO_PHAI_TRA': lstl.get('SO_PHAI_TRA'),
		# 			'SO_DA_TRA': lstl.get('SO_DA_TRA'),
		# 			'SO_CON_PHAI_TRA': lstl.get('SO_CON_PHAI_TRA'),
		# 			'ID_GOC': lstl.get('ID_CHUNG_TU'),
		# 			'MODEL_GOC': lstl.get('MODEL_CHUNG_TU'),
		# 			})]
		return {'TIEN_LUONG_LICH_SU_TRA_LUONG_FORM_CHI_TIET_IDS': new_line}

	def ham_tra_du_lieu_sql_lich_su_tra_luong(self):
		# param_sql={}
		query ="""
		DO LANGUAGE plpgsql $$
DECLARE


	nhan_vien_id                                  INTEGER := 81;

	chi_nhanh_id                                  INTEGER := 16;

	ngay_hach_toan_tren_chung_tu                  TIMESTAMP := '2019-08-21 00:00:00';

	--@SystemDate

	CACH_LAY_SO_TIEN_LUONG_PHAI_TRA_CHO_NHAN_VIEN VARCHAR(128);

	loai_chung_tu_tam_ung                         INTEGER := 6023;

	CASalary                                      INTEGER := 1026;

	BASalary                                      INTEGER := 1523;

	chi_tiet_theo_tai_khoan_doi_tuong_334         BOOLEAN := FALSE;

	dem                                           INTEGER;

	chi_tiet_theo_nhan_vien                       BOOLEAN;

	TU_NGAY_BAT_DAU_TAI_CHINH                     TIMESTAMP(128);

	so_con_phai_tra_temp                          DECIMAL(22, 8) :=0;

	rec                                           RECORD;


BEGIN

	IF EXISTS(SELECT *
			  FROM danh_muc_he_thong_tai_khoan
			  WHERE "SO_TAI_KHOAN" LIKE '334%%'
					AND "LA_TK_TONG_HOP" = FALSE
					AND "DOI_TUONG" = TRUE
					AND "DOI_TUONG_SELECTION" = '2')
	THEN
		SELECT value
		INTO CACH_LAY_SO_TIEN_LUONG_PHAI_TRA_CHO_NHAN_VIEN
		FROM ir_config_parameter
		WHERE key = 'he_thong.CACH_LAY_SO_TIEN_LUONG_PHAI_TRA_CHO_NHAN_VIEN'
		FETCH FIRST 1 ROW ONLY
		;

	ELSE
		CACH_LAY_SO_TIEN_LUONG_PHAI_TRA_CHO_NHAN_VIEN = 'LAY_THEO_SO_TIEN_LUONG_PHAI_TRA_TREN_BANG_LUONG'
		;
	END IF
	;

	IF CACH_LAY_SO_TIEN_LUONG_PHAI_TRA_CHO_NHAN_VIEN = 'LAY_THEO_SO_TIEN_LUONG_PHAI_TRA_TREN_BANG_LUONG'
	THEN


		DROP TABLE IF EXISTS TMP_SO_TAI_KHOAN
		;

		CREATE TEMP TABLE TMP_SO_TAI_KHOAN

			-- Bảng lưu các TK chi tiết theo nhân viên
		(
			"SO_TAI_KHOAN"  VARCHAR(20) PRIMARY KEY,
			"TEN_TAI_KHOAN" VARCHAR(255),
			"TINH_CHAT"     VARCHAR(255)
		)
		;

		INSERT INTO TMP_SO_TAI_KHOAN
			SELECT
				A."SO_TAI_KHOAN"
				, A."TEN_TAI_KHOAN"
				, A."TINH_CHAT"
			FROM danh_muc_he_thong_tai_khoan AS A
			WHERE "DOI_TUONG" = TRUE
				  AND "DOI_TUONG_SELECTION" = '2'
				  AND "LA_TK_TONG_HOP" = FALSE
				  AND "SO_TAI_KHOAN" LIKE '334%%'
			ORDER BY A."SO_TAI_KHOAN",
				A."TEN_TAI_KHOAN"
		;

		SELECT value
		INTO TU_NGAY_BAT_DAU_TAI_CHINH
		FROM ir_config_parameter
		WHERE key = 'he_thong.TU_NGAY_BAT_DAU_TAI_CHINH'
		FETCH FIRST 1 ROW ONLY
		;


		IF (SELECT COUNT(*)
			FROM TMP_SO_TAI_KHOAN
		   ) > 0
		THEN
			chi_tiet_theo_nhan_vien = TRUE
			;
		ELSE
			chi_tiet_theo_nhan_vien = FALSE
			;
		END IF
		;

		DROP TABLE IF EXISTS TMP_KET_QUA
		;

		CREATE TEMP TABLE TMP_KET_QUA


		(
			RowNum            INT PRIMARY KEY,
			"ID_CHUNG_TU"     INT,
			"MODEL_CHUNG_TU"  VARCHAR(500),
			"LOAI_CHUNG_TU"   INT,
			"NGAY_CHUNG_TU"   TIMESTAMP,
			"NGAY_HACH_TOAN"  TIMESTAMP,
			"SO_CHUNG_TU"     VARCHAR(25),
			"DIEN_GIAI"       VARCHAR(500),
			"SO_PHAI_TRA"     DECIMAL(22, 8),
			"SO_DA_TRA"       DECIMAL(22, 8),
			"SO_CON_PHAI_TRA" DECIMAL(22, 8),
			"OrderType"       INT
		)
		;

		INSERT INTO TMP_KET_QUA
			SELECT
				ROW_NUMBER()
				OVER (
					ORDER BY "OrderType", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU",
						"LOAI_CHUNG_TU" DESC ) AS "rownum"
				, -- Sắp xếp bảng lương tạm ứng trước
				*
			FROM (
					 /*Lấy bảng lương và bảng lương tạm ứng*/ SELECT
																	PSS."id"                AS "ID_CHUNG_TU"
																  , 'tien.luong.bang.luong' AS "MODEL_CHUNG_TU"
																  , PSS."LOAI_CHUNG_TU"

																  , CAST(SUBSTR(CAST(PSS."THANG" AS VARCHAR(2)), 1, 2)
																		 || '/01/'
																		 || SUBSTR(CAST(PSS."NAM" AS VARCHAR(4)), 1, 4)
																		 AS TIMESTAMP) + INTERVAL '1 month' +
																	INTERVAL '-1 day'       AS "NGAY_CHUNG_TU"


																  , CAST(SUBSTR(CAST(PSS."THANG" AS VARCHAR(2)), 1, 2)
																		 || '/01/'
																		 || SUBSTR(CAST(PSS."NAM" AS VARCHAR(4)), 1, 4)
																		 AS TIMESTAMP) + INTERVAL '1 month' +
																	INTERVAL '-1 day'       AS "NGAY_HACH_TOAN"
																  , 'BL'
																	|| CAST(PSS."THANG" AS VARCHAR(2))
																	|| '/'
																	|| CAST(PSS."NAM" AS
																			VARCHAR(4))     AS "SO_CHUNG_TU"
																  , PSS."TEN_BANG_LUONG"    AS "DIEN_GIAI"
																  , /*nếu là bảng tạm ứng*/
																	(CASE
																	 WHEN PSS."LOAI_CHUNG_TU" =
																		  loai_chung_tu_tam_ung
																		 THEN PSSD."SO_TIEN_TAM_UNG"
																	 ELSE (
																		 CASE
																		 WHEN
																			 PAD."MA_NHAN_VIEN"
																			 IS
																			 NULL
																			 THEN (CASE
																				   WHEN
																					   chi_tiet_theo_nhan_vien
																					   =
																					   FALSE
																					   THEN "SO_TIEN_CON_DUOC_LINH"
																				   ELSE
																					   "SO_TIEN_CON_DUOC_LINH"
																					   +
																					   COALESCE(
																						   PSSD."SO_TIEN_TAM_UNG",
																						   0)
																				   END)
																		 ELSE "SO_TIEN_CON_DUOC_LINH" /*nếu có bảng lương tạm ứng thì lấy ở dưới*/
																		 END)
																	 END)                   AS "SO_PHAI_TRA"
																  , 0                       AS "SO_DA_TRA"
																  , 0                       AS "SO_CON_PHAI_TRA"
																  , 1                       AS "OrderType"
															  FROM tien_luong_bang_luong_chi_tiet
																  AS PSSD
																  INNER JOIN tien_luong_bang_luong
																	  AS PSS ON PSS."id" = PSSD."CHI_TIET_ID"
																  --/*lấy bảng lương tạm ứng của tháng đó cho trường hợp convert dữ liệu từ 2012 lên ko có tạm ứng vẫn trả lương được*/
																  LEFT JOIN (SELECT DISTINCT
																				 P."THANG"
																				 , P."NAM"
																				 , PD1."MA_NHAN_VIEN"
																			 FROM
																				 tien_luong_bang_luong_chi_tiet
																					 AS PD1
																				 INNER JOIN tien_luong_bang_luong
																				 AS P ON PD1."CHI_TIET_ID" = P."id"
																			 WHERE
																				 P."LOAI_CHUNG_TU" = 6023
																				 AND P."CHI_NHANH_ID" = chi_nhanh_id
																			) AS PAD
																	  ON PSSD."MA_NHAN_VIEN" = PAD."MA_NHAN_VIEN"
																		 AND PAD."THANG" = PSS."THANG"
																		 AND PAD."NAM" = PSS."NAM"
															  WHERE ((PSS."THANG" <=
																	  CAST(EXTRACT(MONTH FROM
																				   ngay_hach_toan_tren_chung_tu) AS
																		   VARCHAR)
																	  AND
																	  PSS."NAM" = CAST(EXTRACT(YEAR FROM
																							   ngay_hach_toan_tren_chung_tu)
																					   AS VARCHAR)
																	 )
																	 OR (PSS."NAM" <
																		 CAST(EXTRACT(YEAR FROM
																					  ngay_hach_toan_tren_chung_tu) AS
																			  VARCHAR))
																	)

																	AND PSSD."MA_NHAN_VIEN" = nhan_vien_id
																	AND PSS."CHI_NHANH_ID" = chi_nhanh_id
															  UNION ALL
															  /*Các chứng từ chi trả lương  cho TH không chi tiết theo nhân viên của 334*/
															  SELECT
																  CA."id"
																  , 'account.ex.phieu.thu.chi' AS "MODEL_CHUNG_TU"
																  , CA."LOAI_CHUNG_TU"
																  , CA."NGAY_CHUNG_TU"
																  , CA."NGAY_HACH_TOAN"
																  , CA."SO_CHUNG_TU"
																  , CA."DIEN_GIAI"
																  , 0                          AS "SO_PHAI_TRA"
																  , CAD."SO_TRA"               AS "SO_DA_TRA"
																  , 0                          AS "SO_CON_PHAI_TRA"
																  , 1                          AS "OrderType"
															  FROM
																  tien_luong_uy_nhiem_chi_thong_tin_tra_luong_nhan_vien AS CAD
																  INNER JOIN account_ex_phieu_thu_chi AS CA
																	  ON CAD."THONG_TIN_TRA_LUONG_CHI_TIET_ID" =
																		 CA."id"
															  WHERE ((CA."state" = 'da_ghi_so'

															  )
																	)
																	AND CA."LOAI_CHUNG_TU" = CASalary
																	AND CA."CHI_NHANH_ID" = chi_nhanh_id
																	/*
																	 Chỉ lấy với TH ko chi tiết theo nhân viên vì chi tiết đã lấy ở dưới rồi
																	 */
																	AND chi_tiet_theo_nhan_vien = FALSE
																	AND CAD."MA_NHAN_VIEN" = nhan_vien_id
															  UNION ALL
															  /*các chứng từ ủy nhiệm chi trả lương cho TH không chi tiết theo nhân viên của 334*/
															  SELECT
																  CA."id"
																  , 'account.ex.phieu.thu.chi' AS "MODEL_CHUNG_TU"
																  , CA."LOAI_CHUNG_TU"
																  , CA."NGAY_CHUNG_TU"
																  , CA."NGAY_HACH_TOAN"
																  , CA."SO_CHUNG_TU"
																  , CA."DIEN_GIAI"
																  , 0                          AS "SO_PHAI_TRA"
																  , CAD."SO_TRA"               AS "SO_DA_TRA"
																  , 0                          AS "SO_CON_PHAI_TRA"
																  , 1                          AS "OrderType"
															  FROM
																  tien_luong_uy_nhiem_chi_thong_tin_tra_luong_nhan_vien AS CAD
																  INNER JOIN account_ex_phieu_thu_chi AS CA
																	  ON CAD."THONG_TIN_TRA_LUONG_CHI_TIET_ID" =
																		 CA."id"
															  WHERE ((CA."state" = 'da_ghi_so'

															  )
																	)
																	AND CA."LOAI_CHUNG_TU" = BASalary
																	AND CA."CHI_NHANH_ID" = chi_nhanh_id
																	/*
																	Chỉ lấy với TH ko chi tiết theo nhân viên vì chi tiết đã lấy ở dưới rồi
																	*/
																	AND chi_tiet_theo_nhan_vien = FALSE
																	AND CAD."MA_NHAN_VIEN" = nhan_vien_id
															  UNION ALL
															  ----Nếu tài khoản chi tiết theo nhân viên
															  /*Lấy số dư ban đầu và các chứng từ chi trả lương cho TH chi tiết theo nhân viên của 334*/
															  SELECT
																	CASE WHEN GL."NGAY_HACH_TOAN" <
																			  TU_NGAY_BAT_DAU_TAI_CHINH
																		THEN NULL
																	ELSE GL."ID_CHUNG_TU"
																	END AS "ID_CHUNG_TU"
																  , CASE WHEN GL."NGAY_HACH_TOAN" <
																			  TU_NGAY_BAT_DAU_TAI_CHINH
																  THEN NULL
																	ELSE GL."MODEL_CHUNG_TU"
																	END AS "MODEL_CHUNG_TU"
																  , CAST(GL."LOAI_CHUNG_TU" AS INT)
																  , GL."NGAY_CHUNG_TU"
																  , GL."NGAY_HACH_TOAN"
																  , GL."SO_CHUNG_TU"
																  , GL."DIEN_GIAI_CHUNG"
																  , /*Số phải trả*/
																  CASE WHEN GL."NGAY_HACH_TOAN" <
																			TU_NGAY_BAT_DAU_TAI_CHINH
																	  THEN 0
																  ELSE SUM(GL."GHI_CO")
																  END
																  , /*Số đã trả*/
																  CASE WHEN GL."NGAY_HACH_TOAN" <
																			TU_NGAY_BAT_DAU_TAI_CHINH
																	  THEN 0
																  ELSE SUM(GL."GHI_NO")
																  END
																  , /*số dư ban đầu thì lấy vào số còn phải trả
						  các trường hợp khác thì cộng đuổi ở dưới
						  */
																  CASE WHEN GL."NGAY_HACH_TOAN" <
																			TU_NGAY_BAT_DAU_TAI_CHINH
																	  THEN SUM(GL."GHI_CO"
																			   - GL."GHI_NO")
																  ELSE 0
																  END
																  , CASE WHEN GL."NGAY_HACH_TOAN" <
																			  TU_NGAY_BAT_DAU_TAI_CHINH
																  THEN 0
																	ELSE 1
																	END AS "OrderType"
															  FROM so_cai_chi_tiet AS GL
																  INNER JOIN TMP_SO_TAI_KHOAN AS tbl
																	  ON tbl."SO_TAI_KHOAN" = gl."MA_TAI_KHOAN"
															  WHERE GL."CHI_NHANH_ID" = chi_nhanh_id

																	/*KHông bao gồm hạch toán chi phí lương*/
																	/*Chỗ này bao gồm cả chứng từ trả lương và ủy nhiệm chi trả lương*/
																	AND GL."LOAI_CHUNG_TU" NOT IN ('6030')
																	-- Hạch toán chi phí lương
																	AND GL."NGAY_HACH_TOAN" <=
																		ngay_hach_toan_tren_chung_tu
																	AND GL."DOI_TUONG_ID" = nhan_vien_id
															  GROUP BY
																  CASE WHEN GL."NGAY_HACH_TOAN" <
																			TU_NGAY_BAT_DAU_TAI_CHINH
																	  THEN NULL
																  ELSE GL."ID_CHUNG_TU"
																  END,
																  CASE WHEN GL."NGAY_HACH_TOAN" <
																			TU_NGAY_BAT_DAU_TAI_CHINH
																	  THEN NULL
																  ELSE GL."MODEL_CHUNG_TU"
																  END,
																  CAST(GL."LOAI_CHUNG_TU" AS INT),
																  GL."NGAY_CHUNG_TU",
																  GL."NGAY_HACH_TOAN",
																  GL."SO_CHUNG_TU",
																  GL."DIEN_GIAI_CHUNG"
				 ) AS R
			ORDER BY
				"OrderType",
				"NGAY_HACH_TOAN",
				"NGAY_CHUNG_TU",
				"SO_CHUNG_TU"
		;


		FOR rec IN SELECT *
				   FROM TMP_KET_QUA
				   ORDER BY RowNum
		LOOP


			/*cộng đuổi số còn phải trả*/



			SELECT (CASE WHEN rec."OrderType" = 0
				THEN rec."SO_CON_PHAI_TRA"
					ELSE (so_con_phai_tra_temp
						  + rec."SO_PHAI_TRA"
						  - rec."SO_DA_TRA")
					END)
			INTO so_con_phai_tra_temp
		;

			rec."SO_CON_PHAI_TRA" = so_con_phai_tra_temp
		;

			UPDATE TMP_KET_QUA
			SET "SO_CON_PHAI_TRA" = rec."SO_CON_PHAI_TRA"
			WHERE RowNum = rec.RowNum
		;


		END LOOP
		;


	ELSE
		/*trả theo phát sinh của 334*/

		DROP TABLE IF EXISTS TMP_SO_TAI_KHOAN
		;

		CREATE TEMP TABLE TMP_SO_TAI_KHOAN

			-- Bảng lưu các TK chi tiết theo nhân viên
		(
			"SO_TAI_KHOAN"  VARCHAR(20) PRIMARY KEY,
			"TEN_TAI_KHOAN" VARCHAR(255),
			"TINH_CHAT"     VARCHAR(255)
		)
		;

		INSERT INTO TMP_SO_TAI_KHOAN
			SELECT
				A."SO_TAI_KHOAN"
				, A."TEN_TAI_KHOAN"
				, A."TINH_CHAT"
			FROM danh_muc_he_thong_tai_khoan AS A
			WHERE "DOI_TUONG" = TRUE
				  AND "DOI_TUONG_SELECTION" = '2'
				  AND "LA_TK_TONG_HOP" = FALSE
				  AND "SO_TAI_KHOAN" LIKE '334%%'
			ORDER BY A."SO_TAI_KHOAN",
				A."TEN_TAI_KHOAN"
		;

		SELECT value
		INTO TU_NGAY_BAT_DAU_TAI_CHINH
		FROM ir_config_parameter
		WHERE key = 'he_thong.TU_NGAY_BAT_DAU_TAI_CHINH'
		FETCH FIRST 1 ROW ONLY
		;


		IF (SELECT COUNT(*)
			FROM TMP_SO_TAI_KHOAN
		   ) > 0
		THEN
			chi_tiet_theo_nhan_vien = TRUE
			;
		ELSE
			chi_tiet_theo_nhan_vien = FALSE
			;
		END IF
		;

		DROP TABLE IF EXISTS TMP_KET_QUA
		;

		CREATE TEMP TABLE TMP_KET_QUA


		(
			RowNum            INT PRIMARY KEY,
			"ID_CHUNG_TU"     INT,
			"MODEL_CHUNG_TU"  VARCHAR(500),
			"LOAI_CHUNG_TU"   INT,
			"NGAY_CHUNG_TU"   TIMESTAMP,
			"NGAY_HACH_TOAN"  TIMESTAMP,
			"SO_CHUNG_TU"     VARCHAR(25),
			"DIEN_GIAI"       VARCHAR(500),
			"SO_PHAI_TRA"     DECIMAL(22, 8),
			"SO_DA_TRA"       DECIMAL(22, 8),
			"SO_CON_PHAI_TRA" DECIMAL(22, 8),
			"OrderType"       INT
		)
		;

		INSERT INTO TMP_KET_QUA
			SELECT
				ROW_NUMBER()
				OVER (
					ORDER BY "OrderType", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU", "LOAI_CHUNG_TU" DESC )
				, -- Sắp xếp bảng lương tạm ứng trước
				*
			FROM (

					 ----Nếu tài khoản chi tiết theo nhân viên
					 /*Lấy số dư ban đầu và các chứng từ chi trả lương cho TH chi tiết theo nhân viên của 334*/
					 SELECT
						   CASE WHEN GL."NGAY_HACH_TOAN" < TU_NGAY_BAT_DAU_TAI_CHINH
							   THEN NULL
						   ELSE GL."ID_CHUNG_TU" END    AS "ID_CHUNG_TU"
						 , CASE WHEN GL."NGAY_HACH_TOAN" < TU_NGAY_BAT_DAU_TAI_CHINH
						 THEN NULL
						   ELSE GL."MODEL_CHUNG_TU" END AS "MODEL_CHUNG_TU"
						 , CAST(GL."LOAI_CHUNG_TU" AS INT)
						 , GL."NGAY_CHUNG_TU"
						 , GL."NGAY_HACH_TOAN"
						 , GL."SO_CHUNG_TU"
						 , GL."DIEN_GIAI_CHUNG"
						 , /*Số phải trả*/
						   CASE WHEN GL."NGAY_HACH_TOAN" < TU_NGAY_BAT_DAU_TAI_CHINH
							   THEN 0
						   ELSE
							   CASE WHEN GL."LOAI_CHUNG_TU" = '6030'
								   THEN
									   SUM(GL."GHI_CO" - GL."GHI_NO")
							   ELSE
								   SUM(GL."GHI_CO")
							   END

						   END                          AS "SO_PHAI_TRA"
						 , /*Số đã trả*/
						   CASE WHEN GL."NGAY_HACH_TOAN" < TU_NGAY_BAT_DAU_TAI_CHINH OR GL."LOAI_CHUNG_TU" = '6030'
							   THEN 0
						   ELSE SUM(GL."GHI_NO")
						   END                          AS "SO_DA_TRA"
						 , /*số dư ban đầu thì lấy vào số còn phải trả
							  các trường hợp khác thì cộng đuổi ở dưới
							  */
						   CASE WHEN GL."NGAY_HACH_TOAN" < TU_NGAY_BAT_DAU_TAI_CHINH
							   THEN SUM(GL."GHI_CO"
										- GL."GHI_NO")
						   ELSE 0
						   END                          AS "SO_CON_PHAI_TRA"
						 , CASE WHEN GL."NGAY_HACH_TOAN" < TU_NGAY_BAT_DAU_TAI_CHINH
						 THEN 0
						   ELSE 1
						   END                          AS "OrderType"
					 FROM so_cai_chi_tiet AS GL
						 INNER JOIN TMP_SO_TAI_KHOAN AS tbl ON tbl."SO_TAI_KHOAN" = gl."MA_TAI_KHOAN"
					 WHERE GL."CHI_NHANH_ID" = chi_nhanh_id

						   /*KHông bao gồm hạch toán chi phí lương*/

						   AND GL."NGAY_HACH_TOAN" <= ngay_hach_toan_tren_chung_tu
						   AND GL."DOI_TUONG_ID" = nhan_vien_id
					 GROUP BY
						 CASE WHEN GL."NGAY_HACH_TOAN" < TU_NGAY_BAT_DAU_TAI_CHINH
							 THEN NULL
						 ELSE GL."ID_CHUNG_TU" END,
						 CASE WHEN GL."NGAY_HACH_TOAN" <
								   TU_NGAY_BAT_DAU_TAI_CHINH
							 THEN NULL
						 ELSE GL."MODEL_CHUNG_TU"
						 END,
						 GL."LOAI_CHUNG_TU" ,
						 GL."NGAY_CHUNG_TU",
						 GL."NGAY_HACH_TOAN",
						 GL."SO_CHUNG_TU",
						 GL."DIEN_GIAI_CHUNG"
				 ) AS R
			ORDER BY "OrderType",
				"NGAY_HACH_TOAN",
				"NGAY_CHUNG_TU",
				"SO_CHUNG_TU"
		;

		/*cộng đuổi số còn phải trả*/
		FOR rec IN SELECT *
				   FROM TMP_KET_QUA
				   ORDER BY RowNum
		LOOP


			/*cộng đuổi số còn phải trả*/



			SELECT (CASE WHEN rec."OrderType" = 0
				THEN rec."SO_CON_PHAI_TRA"
					ELSE (so_con_phai_tra_temp
						  + rec."SO_PHAI_TRA"
						  - rec."SO_DA_TRA")
					END)
			INTO so_con_phai_tra_temp
		;

			rec."SO_CON_PHAI_TRA" = so_con_phai_tra_temp
		;

			UPDATE TMP_KET_QUA
			SET "SO_CON_PHAI_TRA" = rec."SO_CON_PHAI_TRA"
			WHERE RowNum = rec.RowNum
		;


		END LOOP
		;


	END IF

	;

END $$
;

SELECT *
FROM TMP_KET_QUA

ORDER BY
   RowNum
;
		"""
		return self.execute(query)