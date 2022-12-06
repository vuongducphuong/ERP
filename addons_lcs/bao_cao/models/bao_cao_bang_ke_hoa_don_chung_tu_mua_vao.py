# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU(models.Model):
	_name = 'bao.cao.bang.ke.hoa.don.chung.tu'
	
	
	_auto = False

	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
	BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
	KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI', required='True')
	TU = fields.Date(string='Từ', help='Từ', required='True', default=fields.Datetime.now)
	DEN = fields.Date(string='Đến', help='Đến', required='True', default=fields.Datetime.now)
	CONG_GOP_THEO_TUNG_HOA_DON = fields.Boolean(string='Cộng gộp theo từng hóa đơn', help='Cộng gộp theo từng hóa đơn')
	LAY_SO_LIEU_DVT_SO_LUONG_DON_GIA_LEN_BAO_CAO = fields.Boolean(string='Lấy số liệu ĐVT, Số lượng, Đơn giá lên báo cáo', help='Lấy số liệu đơn vị tính, số lượng, đơn giá lên báo cáo')
	NHOM_HHDV_MUA_VAO = fields.Char(string='Nhóm HHDV mua vào', help='Nhóm hàng hóa dịch vụ mua vào')
	SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
	SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
	NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
	TEN_NGUOI_BAN = fields.Char(string='Tên người bán', help='Tên người bán')
	MA_SO_THUE_NGUOI_BAN = fields.Char(string='Mã số thuế người bán', help='Mã số thuế người bán')#, auto_num='bao_cao_bang_ke_hoa_don_chung_tu_MA_SO_THUE_NGUOI_BAN')
	MAT_HANG = fields.Char(string='Mặt hàng', help='Mặt hàng')
	GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE = fields.Float(string='Giá trị HHDV mua vào chưa có thuế', help='Giá trị hàng hóa dịch vụ mua vào chưa có thuế',digits=decimal_precision.get_precision('VND'))
	THUE_SUAT = fields.Char(string='Thuế suất', help='Thuế suất')
	THUE_GTGT = fields.Float(string='Thuế GTGT', help='Thuế giá trị gia tăng',digits=decimal_precision.get_precision('VND'))
	TK_THUE = fields.Char(string='TK thuế', help='Tài khoản thuế')
	name = fields.Char(string='Name', help='Name', oldname='NAME')
	ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
	MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')

	BANG_KE_HOA_DON_CT_GROUP_ID = fields.Many2one('bao.cao.bang.ke.hoa.don.chung.tu.group')

	#FIELD_IDS = fields.One2many('model.name')
	# def _validate(self):
	#     params = self._context
	#     FIELDS_IDS = params['FIELDS_IDS'] if 'FIELDS_IDS' in params.keys() else 'False'
	#     if(not len(FIELDS_IDS)):
	#         raise ValidationError('Vui lòng kiểm tra lại!')
	@api.model
	def default_get(self, fields_list):
		result = super(BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU, self).default_get(fields_list)
		chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
		if chi_nhanh :
			result['CHI_NHANH_ID'] = chi_nhanh.id
		return result
	
	@api.onchange('KY_BAO_CAO')
	def _cap_nhat_ngay(self):
		self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')
	def _validate(self):
		params = self._context
		TU = params['TU'] if 'TU' in params.keys() else 'False'
		TU = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
		DEN = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

		if(TU=='False'):
			raise ValidationError('<Từ> không được bỏ trống.')
		elif(DEN=='False'):
			raise ValidationError('<Đến> không được bỏ trống.')
		elif(TU > DEN):
			raise ValidationError('<Đến> phải lớn hơn hoặc bằng <Từ>.')

	@api.model
	def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
		record = []
		# Get paramerters here
		params = self._context
		if not params.get('active_model'):
			return
		CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
		BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
		TU_NGAY = params['TU'] if 'TU' in params.keys() else 'False'
		TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		DEN_NGAY = params['DEN'] if 'DEN' in params.keys() else 'False'
		DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		CONG_GOP_THEO_TUNG_HOA_DON = 1 if 'CONG_GOP_THEO_TUNG_HOA_DON' in params.keys() and params['CONG_GOP_THEO_TUNG_HOA_DON'] != 'False' else 0
		LAY_SO_LIEU_DVT_SO_LUONG_DON_GIA_LEN_BAO_CAO = 1 if 'LAY_SO_LIEU_DVT_SO_LUONG_DON_GIA_LEN_BAO_CAO' in params.keys() and params['LAY_SO_LIEU_DVT_SO_LUONG_DON_GIA_LEN_BAO_CAO'] != 'False' else 0

		params_sql = {
			'TU_NGAY':TU_NGAY_F, 
			'DEN_NGAY':DEN_NGAY_F,
			'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
			'CONG_GOP_THEO_TUNG_HOA_DON':CONG_GOP_THEO_TUNG_HOA_DON,
			'LAY_SO_LIEU_DVT_SO_LUONG_DON_GIA_LEN_BAO_CAO':LAY_SO_LIEU_DVT_SO_LUONG_DON_GIA_LEN_BAO_CAO,
			'CHI_NHANH_ID':CHI_NHANH_ID,
			'limit': limit,
			'offset': offset,
		}

		query = """
		--BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU
	DO LANGUAGE plpgsql $$
	DECLARE
	v_tu_ngay                             DATE := %(TU_NGAY)s;

	--tham số từ

	v_den_ngay                            DATE := %(DEN_NGAY)s;

	--tham số đến

	v_bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

	--tham số bao gồm số liệu chi nhánh phụ thuộc

	v_chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

	--tham số chi nhánh


	v_cong_gop_theo_tung_hoa_don          INTEGER := %(CONG_GOP_THEO_TUNG_HOA_DON)s;

	--tham số cộng gộp theo từng hóa đơn

	v_lay_so_lieu_dvt_so_luong_don_gia    INTEGER := %(LAY_SO_LIEU_DVT_SO_LUONG_DON_GIA_LEN_BAO_CAO)s;

	--tham số lấy số liệu ĐVT, số lượng, đơn giá lên báo cáo


	rec                                   RECORD;

	PHAN_THAP_PHAN_SO_LUONG               INTEGER;


	BEGIN
	DROP TABLE IF EXISTS TMP_LIST_BRAND
			;

			CREATE TEMP TABLE TMP_LIST_BRAND
				AS
					SELECT *
					FROM LAY_DANH_SACH_CHI_NHANH(v_chi_nhanh_id, v_bao_gom_du_lieu_chi_nhanh_phu_thuoc)
			;

			DROP TABLE IF EXISTS TMP_KET_QUA
			;

			DROP SEQUENCE IF EXISTS TMP_KET_QUA_seq
			;

			CREATE TEMP SEQUENCE TMP_KET_QUA_seq
			;


			CREATE TEMP TABLE TMP_KET_QUA
			(
				KeyID                               INT DEFAULT NEXTVAL('TMP_KET_QUA_seq') PRIMARY KEY,
				"NHOM_HHDV_MUA_VAO"                 VARCHAR(500),
				"SO_CHUNG_TU"                       VARCHAR(500),
				"NGAY_HOA_DON"                      DATE,
				"SO_HOA_DON"                        VARCHAR(250),
				"ID_CHUNG_TU"                       INT,
				"MODEL_CHUNG_TU"                    VARCHAR(250),


				"TEN_NGUOI_BAN"                     VARCHAR(255),

				"MA_SO_THUE_NGUOI_BAN"              VARCHAR(127),
				"MAT_HANG"                          VARCHAR(255),

				"GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE" DECIMAL(18, 4),
				"THUE_SUAT"                         VARCHAR(10),
				"THUE_GTGT"                         DECIMAL(18, 4),
				"TK_THUE"                           VARCHAR(250),
				"MAU_SO_HOA_DON"                    VARCHAR(127),
				"KY_HIEU_HOA_DON"                   VARCHAR(255),
				"CHI_TIET_ID"                       INT,
				"CHI_TIET_MODEL"                    VARCHAR(250),

				 "CHI_NHANH_ID"                       INT,
				"JoinKey"                           VARCHAR(5000)




			)
			;




			DROP TABLE IF EXISTS TMP_KET_QUA_1
			;

			DROP SEQUENCE IF EXISTS TMP_KET_QUA_1_seq
			;


			CREATE TEMP SEQUENCE TMP_KET_QUA_1_seq
			;


			CREATE TABLE TMP_KET_QUA_1
			(
				KeyID                               INT DEFAULT NEXTVAL('TMP_KET_QUA_1_seq') PRIMARY KEY,
				"NHOM_HHDV_MUA_VAO"                 VARCHAR(500),
				"SO_CHUNG_TU"                       VARCHAR(250),
				"NGAY_HOA_DON"                      DATE,
				"SO_HOA_DON"                        VARCHAR(250),
				"ID_CHUNG_TU"                       INT,
				"MODEL_CHUNG_TU"                    VARCHAR(250),


				"TEN_NGUOI_BAN"                     VARCHAR(255),

				"MA_SO_THUE_NGUOI_BAN"              VARCHAR(127),
				"MAT_HANG"                          VARCHAR(255),

				"GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE" DECIMAL(18, 4),
				"THUE_SUAT"                         VARCHAR(10),
				"THUE_GTGT"                         DECIMAL(18, 4),
				"TK_THUE"                           VARCHAR(250),
				"MAU_SO_HOA_DON"                    VARCHAR(127),
				"KY_HIEU_HOA_DON"                   VARCHAR(255)
			)
			;





			INSERT INTO TMP_KET_QUA
			("NHOM_HHDV_MUA_VAO",

			 "SO_HOA_DON",
			 "NGAY_HOA_DON",
				 "SO_CHUNG_TU",
			 "ID_CHUNG_TU",
			 "MODEL_CHUNG_TU",
			 "TEN_NGUOI_BAN",
			 "MA_SO_THUE_NGUOI_BAN",
			 "MAT_HANG",
			 "GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE",
			 "THUE_SUAT",
			 "THUE_GTGT",
			 "TK_THUE",
			 "MAU_SO_HOA_DON",
			 "KY_HIEU_HOA_DON",
			 "CHI_TIET_ID",
			 "CHI_TIET_MODEL",
			"CHI_NHANH_ID",
			 "JoinKey"

			)

				SELECT
					TL."TEN_MUC_DICH_MUA_HANG"

					, TL."SO_HOA_DON"
					, TL."NGAY_HOA_DON"

					, TL."SO_CHUNG_TU"
					, TL."ID_CHUNG_TU"

					, TL."MODEL_CHUNG_TU"

					, TL."TEN_DOI_TUONG"
					, TL."MA_SO_THUE_DOI_TUONG"
					, "DIEN_GIAI"                 AS "MAT_HANG"
					, CASE
					  WHEN TL."LOAI_CHUNG_TU" IN ('3567')
						  THEN -1
					  ELSE 1
					  END * TL."SO_TIEN_CHIU_VAT" AS "GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE"
					,
					  CASE
					  WHEN TL."LOAI_CHUNG_TU" IN ('3569')
						  THEN ''
					  ELSE CASE TL."PHAN_TRAM_VAT"
						   WHEN -1
							   THEN N'KCT'
						   WHEN 0
							   THEN N'0 %%'
						   WHEN 5
							   THEN N'5 %%'
						   WHEN 10
							   THEN N'10 %%'
						   END
					  END                         AS "THUE_SUAT"
					, CASE
					  WHEN TL."LOAI_CHUNG_TU" IN ('3567')
						  THEN -1
					  ELSE 1
					  END * TL."SO_TIEN_VAT"      AS "THUE_GTGT"
					,
					"MA_TK_VAT"
					, TL."MAU_SO_HOA_DON"
					, TL."KY_HIEU_HOA_DON"
					, TL."CHI_TIET_ID"
					, TL."CHI_TIET_MODEL"
					 , TL."CHI_NHANH_ID"
					,COALESCE(TL."TEN_MUC_DICH_MUA_HANG", '')
								|| COALESCE(TL."MAU_SO_HOA_DON", '') || COALESCE(TL."KY_HIEU_HOA_DON",'')
								|| COALESCE(TL."SO_HOA_DON", '')
								|| COALESCE(CAST(TL."NGAY_HOA_DON" AS VARCHAR(255)), '')
								|| COALESCE(TL."TEN_DOI_TUONG", '')
								|| COALESCE(TL."MA_SO_THUE_DOI_TUONG", '')
								|| COALESCE(CAST(TL."CHI_NHANH_ID" AS VARCHAR(255)), '')
								|| COALESCE(CAST(TL."PHAN_TRAM_VAT" AS VARCHAR(255)), '')

				FROM so_thue_chi_tiet AS TL
					JOIN TMP_LIST_BRAND AS B ON TL."CHI_NHANH_ID" = B."CHI_NHANH_ID"
					LEFT JOIN sale_ex_hoa_don_ban_hang AS SI
						ON SI."id" = TL."ID_CHUNG_TU" AND TL."MODEL_CHUNG_TU" = 'sale.ex.hoa.don.ban.hang'
				WHERE
					TL."DS_LOAI_BANG" = 1
				  AND   TL."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay
					 AND TL."MUC_DICH_MUA_HANG_ID" IS NOT NULL
					   AND (TL."ID_CHUNG_TU_GOC" IS NULL -- Không phải là mua hàng nhập khẩu
						 OR TL."ID_CHUNG_TU_GOC" = 0 )-- Không phải là mua hàng nhập khẩu
					  AND (TL."LOAI_CHUNG_TU" IN ('3567', '3568', '3569') AND SI."LOAI_CHUNG_TU_DIEU_CHINH" = 3564
						   OR TL."LOAI_CHUNG_TU" NOT IN ('3567', '3568', '3569')
					  )



				UNION ALL
				SELECT
					TL."TEN_MUC_DICH_MUA_HANG"

					, TL."SO_HOA_DON"
					, TL."NGAY_HOA_DON"
					, TL."SO_CHUNG_TU_GOC"             AS "SO_CHUNG_TU"

					, TL."ID_CHUNG_TU_GOC"             AS "ID_CHUNG_TU"
					, TL."MODEL_CHUNG_TU_GOC"       AS "MODEL_CHUNG_TU"

					, TL."TEN_DOI_TUONG"
					, TL."MA_SO_THUE_DOI_TUONG"
					, "DIEN_GIAI"                      AS "MAT_HANG"
					, TL."SO_TIEN_CHIU_VAT"
					, CASE TL."PHAN_TRAM_VAT"
					  WHEN -1
						  THEN N'KCT'
					  WHEN 0
						  THEN N'0 %%'
					  WHEN 5
						  THEN N'5 %%'
					  WHEN 10
						  THEN N'10 %%'
					  END                              AS "THUE_SUAT"
					, SUM(TL."SO_TIEN_VAT")
					, "MA_TK_VAT"
					, TL."MAU_SO_HOA_DON"
					, TL."KY_HIEU_HOA_DON"
					, TL."CHI_TIET_ID_CHUNG_TU_GOC"    AS "CHI_TIET_ID"
					, TL."CHI_TIET_MODEL_CHUNG_TU_GOC" AS "CHI_TIET_MODEL"
					, TL."CHI_NHANH_ID"
					,COALESCE(TL."TEN_MUC_DICH_MUA_HANG", '')
								|| COALESCE(TL."MAU_SO_HOA_DON", '') || COALESCE(TL."KY_HIEU_HOA_DON",'')
								|| COALESCE(TL."SO_HOA_DON", '')
								|| COALESCE(CAST(TL."NGAY_HOA_DON" AS VARCHAR(255)), '')
								|| COALESCE(TL."TEN_DOI_TUONG", '')
								|| COALESCE(TL."MA_SO_THUE_DOI_TUONG", '')
								|| COALESCE(CAST(TL."CHI_NHANH_ID" AS VARCHAR(255)), '')
								|| COALESCE(CAST(TL."PHAN_TRAM_VAT" AS VARCHAR(255)), '')

				FROM so_thue_chi_tiet AS TL
					JOIN TMP_LIST_BRAND AS B ON TL."CHI_NHANH_ID" = B."CHI_NHANH_ID"
				WHERE TL."DS_LOAI_BANG" = 1
					  AND TL."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay

					  AND TL."MUC_DICH_MUA_HANG_ID" IS NOT NULL
					AND (TL."ID_CHUNG_TU_GOC" IS NOT NULL -- Mua hàng nhập khẩu
					  AND TL."ID_CHUNG_TU_GOC" <> 0 )-- Mua hàng nhập khẩu
				GROUP BY
					TL."TEN_MUC_DICH_MUA_HANG"

					, TL."SO_HOA_DON"
					, TL."NGAY_HOA_DON"
					, TL."SO_CHUNG_TU_GOC"

					, TL."ID_CHUNG_TU_GOC"
					, TL."MODEL_CHUNG_TU_GOC"

					, TL."TEN_DOI_TUONG"
					, TL."MA_SO_THUE_DOI_TUONG"
					, "DIEN_GIAI"
					, TL."SO_TIEN_CHIU_VAT"
					, TL."PHAN_TRAM_VAT"
					, "MA_TK_VAT"
					, TL."MAU_SO_HOA_DON"
					, TL."KY_HIEU_HOA_DON"
					, TL."CHI_TIET_ID_CHUNG_TU_GOC"
					, TL."CHI_TIET_MODEL_CHUNG_TU_GOC"
					 , TL."CHI_NHANH_ID"
			;


			UPDATE TMP_KET_QUA
			SET
				"SO_HOA_DON"          = COALESCE("SO_HOA_DON", ''),
				"TEN_NGUOI_BAN"        = COALESCE("TEN_NGUOI_BAN", ''),
				"MA_SO_THUE_NGUOI_BAN" = COALESCE("MA_SO_THUE_NGUOI_BAN", ''),
				"MAU_SO_HOA_DON"       = COALESCE("MAU_SO_HOA_DON", ''),
				"KY_HIEU_HOA_DON"      = COALESCE("KY_HIEU_HOA_DON", '')
			WHERE
				"SO_HOA_DON" IS NULL
				OR "TEN_NGUOI_BAN" IS NULL
				OR "MA_SO_THUE_NGUOI_BAN" IS NULL
				OR "MAU_SO_HOA_DON" IS NULL
				OR "KY_HIEU_HOA_DON" IS NULL
			;


			DROP TABLE IF EXISTS TMP_SO_CHUNG_TU
			;

			CREATE TEMP TABLE TMP_SO_CHUNG_TU
				AS
					SELECT
						"ID_CHUNG_TU"
						,"MODEL_CHUNG_TU_HD"
						, "SO_CHUNG_TU_FIRSTTAB"
						, "DIEN_GIAI"


					FROM (SELECT
							  DISTINCT
							  "ID_CHUNG_TU"
							  ,"MODEL_CHUNG_TU_HD"
							  , "SO_CHUNG_TU_FIRSTTAB"
							  , "DIEN_GIAI"
						  FROM GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO(NULL,
																				  NULL, NULL, ';')
						  UNION ALL
						  SELECT DISTINCT
							  R.sale_ex_hoa_don_ban_hang_id
							  ,'sale.ex.hoa.don.ban.hang' AS "MODEL_CHUNG_TU_HD"
							  , V."SO_CHUNG_TU"
							  , V."DIEN_GIAI"
						  FROM sale_ex_document_invoice_rel R
							  JOIN tim_kiem_so_chung_tu V ON R."sale_document_id" = V."ID_CHUNG_TU" AND V."MODEL_CHUNG_TU" ='sale.ex.hoa.don.ban.hang'
							 --WHERE     ReferenceType <> 0
						 ) V
			;

			DROP TABLE IF EXISTS TMP_SO_CHUNG_TU_GOC
			;

			CREATE TEMP TABLE TMP_SO_CHUNG_TU_GOC
				AS
					SELECT
						R1."ID_CHUNG_TU"
						 ,R1."MODEL_CHUNG_TU_HD"
						, (SELECT string_agg( A."SO_CHUNG_TU_FIRSTTAB",',') --R2."SO_HOA_DON"
						   FROM (SELECT "SO_CHUNG_TU_FIRSTTAB"
								 FROM TMP_SO_CHUNG_TU AS R2
								 WHERE

									 R2."ID_CHUNG_TU" = R1."ID_CHUNG_TU" and
									R2."MODEL_CHUNG_TU_HD" = R1."MODEL_CHUNG_TU_HD"

								 ORDER BY
									 R2."SO_CHUNG_TU_FIRSTTAB") A


						  ) AS "SO_CHUNG_TU"
						, R1."DIEN_GIAI"
					FROM TMP_SO_CHUNG_TU AS R1

			;
			DROP TABLE TMP_SO_CHUNG_TU;


							UPDATE  TMP_KET_QUA R
							SET     "SO_CHUNG_TU" = COALESCE(F."SO_CHUNG_TU", R."SO_CHUNG_TU")
							FROM     TMP_SO_CHUNG_TU_GOC AS F
							WHERE R."ID_CHUNG_TU" = F."ID_CHUNG_TU" AND R."MODEL_CHUNG_TU"  =F."MODEL_CHUNG_TU_HD";


		   --Không lấy hóa đơn mua hàng nhập khẩu mà được ghi sổ ở chức năng nộp thuế
			IF v_cong_gop_theo_tung_hoa_don = 0
			THEN

				IF v_lay_so_lieu_dvt_so_luong_don_gia = 0
				THEN
					INSERT INTO TMP_KET_QUA_1
					("NHOM_HHDV_MUA_VAO",
					 "SO_CHUNG_TU",
					 "NGAY_HOA_DON",
					 "SO_HOA_DON",
					 "ID_CHUNG_TU",
					 "MODEL_CHUNG_TU",
					 "TEN_NGUOI_BAN",
					 "MA_SO_THUE_NGUOI_BAN",
					 "MAT_HANG",
					 "GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE",
					 "THUE_SUAT",
					 "THUE_GTGT",
					 "TK_THUE",
					 "MAU_SO_HOA_DON",
					 "KY_HIEU_HOA_DON"
					)
						SELECT
							"NHOM_HHDV_MUA_VAO"
							, "SO_CHUNG_TU"
							, "NGAY_HOA_DON"
							, "SO_HOA_DON"
							, "ID_CHUNG_TU"
							, "MODEL_CHUNG_TU"
							, "TEN_NGUOI_BAN"
							, "MA_SO_THUE_NGUOI_BAN"
							, "MAT_HANG"
							, "GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE"
							, "THUE_SUAT"
							, "THUE_GTGT"
							, "TK_THUE"
							, "MAU_SO_HOA_DON"
							, "KY_HIEU_HOA_DON"

						FROM TMP_KET_QUA
					;

				ELSE
					INSERT INTO TMP_KET_QUA_1
					(
						"NHOM_HHDV_MUA_VAO",
						"SO_CHUNG_TU",
						"NGAY_HOA_DON",
						"SO_HOA_DON",
						"ID_CHUNG_TU",
						"MODEL_CHUNG_TU",
						"TEN_NGUOI_BAN",
						"MA_SO_THUE_NGUOI_BAN",
						"MAT_HANG",
						"GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE",
						"THUE_SUAT",
						"THUE_GTGT",
						"TK_THUE",
						"MAU_SO_HOA_DON",
						"KY_HIEU_HOA_DON"
					)
						SELECT
							"NHOM_HHDV_MUA_VAO"
							, "SO_CHUNG_TU"
							, "NGAY_HOA_DON"
							, "SO_HOA_DON"
							, "ID_CHUNG_TU"
							, "MODEL_CHUNG_TU"
							, "TEN_NGUOI_BAN"
							, "MA_SO_THUE_NGUOI_BAN"
							, "MAT_HANG"
							, "GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE"
							, "THUE_SUAT"
							, "THUE_GTGT"
							, "TK_THUE"
							, "MAU_SO_HOA_DON"
							, "KY_HIEU_HOA_DON"
						FROM TMP_KET_QUA R
							LEFT JOIN tim_kiem_so_chung_tu_chi_tiet
								AS V ON V.id = R."CHI_TIET_ID" AND V."MODEL_CHI_TIET" = R."CHI_TIET_MODEL"
					;
				END IF
				;


			ELSE -- IF v_cong_gop_theo_tung_hoa_don = 0


				INSERT INTO TMP_KET_QUA_1
				(
					"NHOM_HHDV_MUA_VAO",

					"SO_HOA_DON",
					"NGAY_HOA_DON",
					"SO_CHUNG_TU",
					"ID_CHUNG_TU",
					"MODEL_CHUNG_TU",
					"TEN_NGUOI_BAN",
					"MA_SO_THUE_NGUOI_BAN",
					"MAT_HANG",
					"GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE",
					"THUE_SUAT",
					"THUE_GTGT",
					"TK_THUE",
					"MAU_SO_HOA_DON",
					"KY_HIEU_HOA_DON"
				)
					SELECT
						R1."NHOM_HHDV_MUA_VAO"
						, R1."SO_HOA_DON"
						, R1."NGAY_HOA_DON"

						, CASE WHEN length(RTRIM(Temp1."SO_CHUNG_TU")) > 1
						THEN LEFT(RTRIM(Temp1."SO_CHUNG_TU"),
								  length(RTRIM(Temp1."SO_CHUNG_TU")) - 1)
						  ELSE ''
						  END  AS "SO_CHUNG_TU"
						, CASE WHEN Temp5."Count_ID_CHUNG_TU" > 1
						THEN NULL
						  ELSE R1."ID_CHUNG_TU"
						  END  AS "ID_CHUNG_TU"
						, CASE WHEN Temp6."Count_MODEL_CHUNG_TU" > 1
						THEN NULL
						  ELSE R1."MODEL_CHUNG_TU"
						  END  AS "MODEL_CHUNG_TU"
						, R1."TEN_NGUOI_BAN"
						, R1."MA_SO_THUE_NGUOI_BAN"
						, (SELECT "MAT_HANG"
						   FROM TMP_KET_QUA R2
						   WHERE (R2."ID_CHUNG_TU" = (CASE
													  WHEN Temp5."Count_ID_CHUNG_TU" > 1
														  THEN NULL
													  ELSE R1."ID_CHUNG_TU"
													  END)
								  OR Temp5."Count_ID_CHUNG_TU" > 1


								 )
								 AND
								 (R2."MODEL_CHUNG_TU" = (CASE
														 WHEN Temp6."Count_MODEL_CHUNG_TU" > 1
															 THEN NULL
														 ELSE R1."MODEL_CHUNG_TU"
														 END)
								  OR Temp6."Count_MODEL_CHUNG_TU" > 1


								 )
								 AND COALESCE(R2."SO_CHUNG_TU", '') = COALESCE(R1."SO_CHUNG_TU",
																			   '')
								 AND (R2."NGAY_HOA_DON" = R1."NGAY_HOA_DON"
									  OR R2."NGAY_HOA_DON" IS NULL
										 AND R1."NGAY_HOA_DON" IS NULL
								 )
								 AND COALESCE(R2."KY_HIEU_HOA_DON", '') = COALESCE(R1."KY_HIEU_HOA_DON",
																				   '')
								 AND COALESCE(R2."MAU_SO_HOA_DON", '') = COALESCE(R1."MAU_SO_HOA_DON",
																				  '')
								 AND COALESCE(R2."TEN_NGUOI_BAN",
											  '') = COALESCE(R1."TEN_NGUOI_BAN",
															 '')
								 AND COALESCE(R2."THUE_SUAT", '99') = COALESCE(R1."THUE_SUAT",
																			   '99')
						   ORDER BY ABS("GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE") DESC
						   FETCH FIRST 1 ROW ONLY
						  )    AS "MAT_HANG"
						, SUM(R1."GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE")
						, R1."THUE_SUAT"
						, SUM(R1."THUE_GTGT")
						, NULL AS "TK_THUE"
						, "MAU_SO_HOA_DON"
						, "KY_HIEU_HOA_DON"

					FROM TMP_KET_QUA R1
						LEFT JOIN LATERAL ( SELECT (SELECT string_agg
						(A."SO_CHUNG_TU", ',') || ',' FROM (SELECT A."SO_CHUNG_TU"
													FROM
														TMP_KET_QUA A
													WHERE
														A."JoinKey" = R1."JoinKey"
													GROUP BY
														A."SO_CHUNG_TU",
														A."JoinKey") A

												   ) AS "SO_CHUNG_TU"
								  ) Temp1 ON TRUE

						LEFT JOIN LATERAL ( SELECT COUNT(DISTINCT A."ID_CHUNG_TU") AS "Count_ID_CHUNG_TU"
											FROM TMP_KET_QUA A
											WHERE A."JoinKey" = R1."JoinKey"
								  ) Temp5 ON TRUE
						LEFT JOIN LATERAL ( SELECT COUNT(DISTINCT A."MODEL_CHUNG_TU") AS "Count_MODEL_CHUNG_TU"
											FROM TMP_KET_QUA A
											WHERE A."JoinKey" = R1."JoinKey"
								  ) Temp6 ON TRUE
					GROUP BY
						R1."NHOM_HHDV_MUA_VAO",

						R1."SO_HOA_DON",
						R1."NGAY_HOA_DON",

						Temp1."SO_CHUNG_TU",
						CASE WHEN Temp5."Count_ID_CHUNG_TU" > 1
							THEN NULL
						ELSE R1."ID_CHUNG_TU"
						END,
						Temp5."Count_ID_CHUNG_TU",
						CASE WHEN Temp6."Count_MODEL_CHUNG_TU" > 1
							THEN NULL
						ELSE R1."MODEL_CHUNG_TU"
						END,

						R1."TEN_NGUOI_BAN",
						R1."MA_SO_THUE_NGUOI_BAN",
						R1."THUE_SUAT",
						R1."ID_CHUNG_TU",
						Temp6."Count_MODEL_CHUNG_TU",
						R1."MODEL_CHUNG_TU",
						Temp1."SO_CHUNG_TU",
						R1."SO_CHUNG_TU",
						R1."KY_HIEU_HOA_DON",
						R1."MAU_SO_HOA_DON"


				;


			END IF
			;
		--
		--
		--     --             UPDATE  TMP_KET_QUA_1
		--     --             SET     "GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE" = 0 ,
		--     --                     "THUE_GTGT" = 0
		--     --             FROM    TMP_KET_QUA_1 ;
		--     --JOIN IPDeletedAnnouncement AS IPD ON IPD.SAInvoice"ID_CHUNG_TU" = R."ID_CHUNG_TU"


		END $$
		;


		SELECT
			  ROW_NUMBER()
			  OVER (
				  ORDER BY R."NHOM_HHDV_MUA_VAO", R."NGAY_HOA_DON", R."SO_HOA_DON" ) AS RowNum
			, "NHOM_HHDV_MUA_VAO"
			, "SO_HOA_DON"
			, "NGAY_HOA_DON"
			, "SO_CHUNG_TU"
			, "ID_CHUNG_TU"  AS "ID_GOC"
			, "MODEL_CHUNG_TU"  AS "MODEL_GOC"
			, "TEN_NGUOI_BAN"
			, "MA_SO_THUE_NGUOI_BAN"
			, "MAT_HANG"
			, "GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE"
			, "THUE_SUAT"
			, "THUE_GTGT"
			, "TK_THUE"
		FROM TMP_KET_QUA_1 AS R
		
	OFFSET %(offset)s
	LIMIT %(limit)s;
		"""
		return self.execute(query,params_sql)

		
	### END IMPLEMENTING CODE ###

	def _action_view_report(self):
		self._validate()
		TU = self.get_vntime('TU')
		DEN = self.get_vntime('DEN')
		param = 'Từ ngày: %s đến ngày %s' % (TU, DEN)
		action = self.env.ref('bao_cao.open_report_bang_ke_hoa_don_chung_tu').read()[0]
		# action['options'] = {'clear_breadcrumbs': True}
		action['context'] = eval(action.get('context','{}'))
		action['context'].update({'breadcrumb_ex': param})
		return action

	


	@api.model_cr
	def init(self):
		self.env.cr.execute(""" 
	DROP FUNCTION IF EXISTS GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO(IN ds_id_chung_tu  VARCHAR (500), ds_chi_nhanh_id  VARCHAR (500),--Func_Post_GetRelationRefIDFromVoucherRefID_TAX
														   ds_cac_bang_master       VARCHAR (500),
														   ngan_cach_giua_cac_ds    VARCHAR (500));
			
	CREATE OR REPLACE FUNCTION GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO(IN ds_id_chung_tu  VARCHAR (500), ds_chi_nhanh_id  VARCHAR (500),--Func_Post_GetRelationRefIDFromVoucherRefID_TAX
														   ds_cac_bang_master       VARCHAR (500),
														   ngan_cach_giua_cac_ds    VARCHAR (500))
	RETURNS TABLE("ID_CHUNG_TU"       INTEGER,
					 "MODEL_CHUNG_TU_HD"    VARCHAR(500),
				  "sale_document_id"     INTEGER,
				  "SO_CHUNG_TU_FINANCE"    VARCHAR(255),
				  "SO_CHUNG_TU_FIRSTTAB"   VARCHAR(255),
				  "PHAN_TRAM_TGTGT"       INTEGER,
				  "DIEN_GIAI"     VARCHAR(255),
				  "NGAY_CHUNG_TU"   DATE,
				  "NGAY_HACH_TOAN"       DATE

	) AS $$
	DECLARE



	BEGIN

	DROP TABLE IF EXISTS GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO_TMP_KET_QUA_CUOI_CUNG
	;

	CREATE TEMP TABLE GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO_TMP_KET_QUA_CUOI_CUNG (
		"ID_CHUNG_TU"       INTEGER,
		 "MODEL_CHUNG_TU_HD"    VARCHAR(500),
		  "sale_document_id"     INTEGER,
		  "SO_CHUNG_TU_FINANCE"    VARCHAR(500),
		  "SO_CHUNG_TU_FIRSTTAB"   VARCHAR(500),
		  "PHAN_TRAM_TGTGT"       INTEGER,
		  "DIEN_GIAI"     VARCHAR(500),
		  "NGAY_CHUNG_TU"   DATE,
		  "NGAY_HACH_TOAN"       DATE
	)
	;

 	DROP TABLE IF EXISTS GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO_TMP_KET_QUA
	;
	CREATE TEMP TABLE GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO_TMP_KET_QUA
		(
		 "ID_CHUNG_TU"       INTEGER,
		 "MODEL_CHUNG_TU_HD"    VARCHAR(500),
		  "sale_document_id"     INTEGER,
		  "SO_CHUNG_TU_FINANCE"    VARCHAR(500),
		  "SO_CHUNG_TU_FIRSTTAB"   VARCHAR(500),
		  "PHAN_TRAM_TGTGT"       INTEGER,
		  "DIEN_GIAI"     VARCHAR(500),
		  "NGAY_CHUNG_TU"   DATE,
		  "NGAY_HACH_TOAN"       DATE
		)
	;




	IF ds_cac_bang_master LIKE N'%%' || ngan_cach_giua_cac_ds || 'sale_document' || ngan_cach_giua_cac_ds || '%%'
	   OR ds_cac_bang_master IS NULL
	THEN

		INSERT  INTO GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO_TMP_KET_QUA
			 (
				  "ID_CHUNG_TU"      ,
				  "MODEL_CHUNG_TU_HD"  ,
				  "sale_document_id"     ,
				  "SO_CHUNG_TU_FINANCE"    ,
				  "SO_CHUNG_TU_FIRSTTAB"   ,
				  "PHAN_TRAM_TGTGT"       ,
				  "DIEN_GIAI"     ,
				  "NGAY_CHUNG_TU"   ,
				  "NGAY_HACH_TOAN"
			)


				SELECT
					  SAR."sale_ex_hoa_don_ban_hang_id" AS "ID_CHUNG_TU"
					, 'sale.ex.hoa.don.ban.hang'   AS "MODEL_CHUNG_TU_HD"
					 , SAR."sale_document_id"
					, SA."SO_CHUNG_TU"                  AS "SO_CHUNG_TU_FINANCE"
					, SA."SO_CHUNG_TU"                  AS "SO_CHUNG_TU_FIRSTTAB"
					, T."PHAN_TRAM_THUE_GTGT"                AS "PHAN_TRAM_TGTGT"
					, SA."DIEN_GIAI"
					, SA."NGAY_CHUNG_TU"
					, SA."NGAY_HACH_TOAN"
				FROM sale_ex_document_invoice_rel SAR
					JOIN sale_document SA ON SA."id" = SAR."sale_document_id"
					JOIN sale_document_line SAD ON SA."id" = SAD."SALE_DOCUMENT_ID"
					LEFT JOIN danh_muc_thue_suat_gia_tri_gia_tang T ON T."id" = SAD."THUE_GTGT_ID"
				WHERE

					(ds_id_chung_tu LIKE '%%' || ngan_cach_giua_cac_ds
										 || CAST(SAR."sale_document_id" AS VARCHAR(127))
										 || ngan_cach_giua_cac_ds || '%%'
					 OR ds_id_chung_tu IS NULL
					)
					AND SAR."sale_ex_hoa_don_ban_hang_id" IS NOT NULL
					AND (ds_chi_nhanh_id IS NULL
						 OR ds_chi_nhanh_id LIKE '%%'
												 || CAST(SA."CHI_NHANH_ID" AS VARCHAR(127)) || '%%'
					)
		;

	END IF
	;



	--     --sale_ex_giam_gia_hang_ban
	IF ds_cac_bang_master LIKE N'%%' || ngan_cach_giua_cac_ds || 'sale_ex_giam_gia_hang_ban' || ngan_cach_giua_cac_ds
							   || '%%'
	   OR ds_cac_bang_master IS NULL
	THEN

	   INSERT  INTO GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO_TMP_KET_QUA
			 (
				  "ID_CHUNG_TU"      ,
				  "MODEL_CHUNG_TU_HD"  ,
				  "sale_document_id"     ,
				  "SO_CHUNG_TU_FINANCE"    ,
				  "SO_CHUNG_TU_FIRSTTAB"   ,
				  "PHAN_TRAM_TGTGT"       ,
				  "DIEN_GIAI"     ,
				  "NGAY_CHUNG_TU"   ,
				  "NGAY_HACH_TOAN"
			)
				SELECT
					  D."HOA_DON_BAN_HANG_ID"          AS "ID_CHUNG_TU"
					 , 'sale.ex.hoa.don.ban.hang'   AS "MODEL_CHUNG_TU_HD"
					, D."id"                      AS "sale_document_id"
					, D."SO_CHUNG_TU"             AS "SO_CHUNG_TU_FINANCE"
					, D."SO_CHUNG_TU"             AS "SO_CHUNG_TU_FIRSTTAB"
					, T."PHAN_TRAM_THUE_GTGT"                AS "PHAN_TRAM_TGTGT"
					, D."DIEN_GIAI"
					, D."NGAY_CHUNG_TU"
					, D."NGAY_HACH_TOAN"
				FROM sale_ex_giam_gia_hang_ban AS D
					JOIN sale_ex_chi_tiet_giam_gia_hang_ban AS DD ON D."id" = DD."GIAM_GIA_HANG_BAN_ID"
					LEFT JOIN danh_muc_thue_suat_gia_tri_gia_tang T ON T."id" = DD."PHAN_TRAM_THUE_GTGT_ID"

				WHERE (ds_id_chung_tu LIKE '%%' || ngan_cach_giua_cac_ds
										   || CAST(D."id" AS VARCHAR(127)) || ngan_cach_giua_cac_ds || '%%'
					   OR ds_id_chung_tu IS NULL
					  )
					  AND D."HOA_DON_REF_ID" IS NOT NULL
					  AND (ds_chi_nhanh_id IS NULL
						   OR ds_chi_nhanh_id LIKE '%%'
												   || CAST("CHI_NHANH_ID" AS VARCHAR(127)) || '%%'
					  )
		;

	END IF
	;

	--PUReturn

	--
	IF ds_cac_bang_master LIKE N'%%' || ngan_cach_giua_cac_ds || 'PURCHASE_EX_TRA_LAI_HANG_MUA' || ngan_cach_giua_cac_ds || '%%'
	   OR ds_cac_bang_master IS NULL
	THEN

	   INSERT  INTO GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO_TMP_KET_QUA
			 (
				  "ID_CHUNG_TU"      ,
				  "MODEL_CHUNG_TU_HD"  ,
				  "sale_document_id"     ,
				  "SO_CHUNG_TU_FINANCE"    ,
				  "SO_CHUNG_TU_FIRSTTAB"   ,
				  "PHAN_TRAM_TGTGT"       ,
				  "DIEN_GIAI"     ,
				  "NGAY_CHUNG_TU"   ,
				  "NGAY_HACH_TOAN"
			)
				SELECT
					  R."HOA_DON_ID"          AS "ID_CHUNG_TU"
					 , 'sale.ex.hoa.don.ban.hang'   AS "MODEL_CHUNG_TU_HD"
					, R."id"                      AS "sale_document_id"
					, CASE "LOAI_CHUNG_TU"
					  WHEN 3031
						  THEN "SO_PHIEU_THU"
					  WHEN 3033
						  THEN "SO_PHIEU_THU"
					  ELSE R."SO_CHUNG_TU"
					  END                         AS "SO_CHUNG_TU_FINANCE"
					, R."SO_CHUNG_TU"             AS "SO_CHUNG_TU_FIRSTTAB"
					, T."PHAN_TRAM_THUE_GTGT"                AS "PHAN_TRAM_TGTGT"
					, CASE "LOAI_CHUNG_TU"
					  WHEN 3033
						  THEN R."LY_DO_NOP"
					  ELSE R."DIEN_GIAI" END      AS "DIEN_GIAI"
					, R."NGAY_CHUNG_TU"
					, R."NGAY_HACH_TOAN"
				FROM purchase_ex_tra_lai_hang_mua AS R
					JOIN purchase_ex_tra_lai_hang_mua_chi_tiet AS RD ON R."id" = RD."CHUNG_TU_TRA_LAI_HANG_MUA_ID"
					 LEFT JOIN danh_muc_thue_suat_gia_tri_gia_tang T ON T."id" = RD."PHAN_TRAM_THUE_GTGT_ID"
				WHERE (ds_id_chung_tu LIKE '%%' || ngan_cach_giua_cac_ds
										   || CAST(R."id" AS VARCHAR(127)) || ngan_cach_giua_cac_ds || '%%'
					   OR ds_id_chung_tu IS NULL
					  )
					  AND R."HOA_DON_REF_ID" IS NOT NULL
					  AND (ds_chi_nhanh_id IS NULL
						   OR ds_chi_nhanh_id LIKE '%%'
												   || CAST("CHI_NHANH_ID" AS VARCHAR(127)) || '%%'
					  )
		;

	END IF
	;

	--sale_ex_tra_lai_hang_ban


	IF ds_cac_bang_master LIKE
	   N'%%' || ngan_cach_giua_cac_ds || 'sale_ex_tra_lai_hang_ban' || ngan_cach_giua_cac_ds || '%%'
	   OR ds_cac_bang_master IS NULL
	THEN

		INSERT  INTO GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO_TMP_KET_QUA
			 (
				  "ID_CHUNG_TU"      ,
				  "MODEL_CHUNG_TU_HD"  ,
				  "sale_document_id"     ,
				  "SO_CHUNG_TU_FINANCE"    ,
				  "SO_CHUNG_TU_FIRSTTAB"   ,
				  "PHAN_TRAM_TGTGT"       ,
				  "DIEN_GIAI"     ,
				  "NGAY_CHUNG_TU"   ,
				  "NGAY_HACH_TOAN"
			)
				SELECT
					  R."HOA_DON_MUA_HANG_ID"          AS "ID_CHUNG_TU"
					 , 'purchase.ex.hoa.don.mua.hang'   AS "MODEL_CHUNG_TU_HD"
					, R."id"                      AS "sale_document_id"
					, "SO_CHUNG_TU"               AS "SO_CHUNG_TU_FINANCE"
					, "SO_CHUNG_TU"               AS "SO_CHUNG_TU_FIRSTTAB"
				   , T."PHAN_TRAM_THUE_GTGT"                AS "PHAN_TRAM_TGTGT"
					, R."DIEN_GIAI"
					, R."NGAY_CHUNG_TU"
					, R."NGAY_HACH_TOAN"
				FROM sale_ex_tra_lai_hang_ban AS R
					JOIN sale_ex_tra_lai_hang_ban_chi_tiet AS RD ON R."id" = RD."TRA_LAI_HANG_BAN_ID"
					 LEFT JOIN danh_muc_thue_suat_gia_tri_gia_tang T ON T."id" = RD."PHAN_TRAM_THUE_GTGT_ID"
				WHERE (ds_id_chung_tu LIKE '%%' || ngan_cach_giua_cac_ds
										   || CAST(R."id" AS VARCHAR(127)) || ngan_cach_giua_cac_ds || '%%'
					   OR ds_id_chung_tu IS NULL
					  )
					  AND R."HOA_DON_REF_ID" IS NOT NULL
					  AND (ds_chi_nhanh_id IS NULL
						   OR ds_chi_nhanh_id LIKE '%%'
												   || CAST("CHI_NHANH_ID" AS VARCHAR(127)) || '%%'
					  )
		;

	END IF
	;

	--PUDiscount

	IF ds_cac_bang_master LIKE N'%%' || ngan_cach_giua_cac_ds || 'purchase_ex_giam_gia_hang_mua' || ngan_cach_giua_cac_ds
							   || '%%'
	   OR ds_cac_bang_master IS NULL
	THEN

		INSERT  INTO GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO_TMP_KET_QUA
			 (
				  "ID_CHUNG_TU"      ,
				  "MODEL_CHUNG_TU_HD"  ,
				  "sale_document_id"     ,
				  "SO_CHUNG_TU_FINANCE"    ,
				  "SO_CHUNG_TU_FIRSTTAB"   ,
				  "PHAN_TRAM_TGTGT"       ,
				  "DIEN_GIAI"     ,
				  "NGAY_CHUNG_TU"   ,
				  "NGAY_HACH_TOAN"
			)
				SELECT
					  P."HOA_DON_MUA_HANG_ID"          AS "ID_CHUNG_TU"
					, 'purchase.ex.hoa.don.mua.hang'   AS "MODEL_CHUNG_TU_HD"
					, P."id"                      AS "sale_document_id"
					, P."SO_CHUNG_TU"             AS "SO_CHUNG_TU_FINANCE"
					, P."SO_CHUNG_TU"             AS "SO_CHUNG_TU_FIRSTTAB"
					, T."PHAN_TRAM_THUE_GTGT"                AS "PHAN_TRAM_TGTGT"
					, P."DIEN_GIAI"
					, P."NGAY_CHUNG_TU"
					, P."NGAY_HACH_TOAN"
				FROM purchase_ex_giam_gia_hang_mua AS P
					JOIN purchase_ex_giam_gia_hang_mua_chi_tiet AS PD ON P."id" = PD."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID"
					 LEFT JOIN danh_muc_thue_suat_gia_tri_gia_tang T ON T."id" = PD."PHAN_TRAM_THUE_GTGT_ID"
				WHERE (ds_id_chung_tu LIKE '%%' || ngan_cach_giua_cac_ds
										   || CAST(P."id" AS VARCHAR(127)) || ngan_cach_giua_cac_ds || '%%'
					   OR ds_id_chung_tu IS NULL
					  )
					  AND P."HOA_DON_REF_ID" IS NOT NULL
					  AND (ds_chi_nhanh_id IS NULL
						   OR ds_chi_nhanh_id LIKE '%%'
												   || CAST("CHI_NHANH_ID" AS VARCHAR(127)) || '%%'
					  )
		;

	END IF
	;

	--PUVoucher

	IF ds_cac_bang_master LIKE N'%%' || ngan_cach_giua_cac_ds || 'purchase_document' || ngan_cach_giua_cac_ds || '%%'
	   OR ds_cac_bang_master IS NULL
	THEN

		INSERT  INTO GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO_TMP_KET_QUA
			 (
				  "ID_CHUNG_TU"      ,
				  "MODEL_CHUNG_TU_HD"  ,
				  "sale_document_id"     ,
				  "SO_CHUNG_TU_FINANCE"    ,
				  "SO_CHUNG_TU_FIRSTTAB"   ,
				  "PHAN_TRAM_TGTGT"       ,
				  "DIEN_GIAI"     ,
				  "NGAY_CHUNG_TU"   ,
				  "NGAY_HACH_TOAN"
			)
				SELECT
					  COALESCE(P."HOA_DON_MUA_HANG_ID", P."id") AS "ID_CHUNG_TU"
					  ,'purchase.ex.hoa.don.mua.hang'   AS "MODEL_CHUNG_TU_HD"
					, P."id"                                    AS "sale_document_id"
					, CASE WHEN P."LOAI_CHUNG_TU" IN (302, 312, 318, 324)
					THEN "SO_PHIEU_NHAP"
					  ELSE "SO_CHUNG_TU"
					  END                                       AS "SO_CHUNG_TU_FINANCE"
					, COALESCE("SO_PHIEU_NHAP", "SO_CHUNG_TU")  AS "SO_CHUNG_TU_FIRSTTAB"
				   , T."PHAN_TRAM_THUE_GTGT"                AS "PHAN_TRAM_TGTGT"
					, CASE WHEN P."LOAI_CHUNG_TU" IN
								(313, 314, 315, 316, 325, 326, 327, 328, 363, 364, 365, 366, 375, 376, 377, 378)
					THEN P."LY_DO_CHI"
					  ELSE P."DIEN_GIAI_CHUNG" END              AS "DIEN_GIAI"
					, P."NGAY_CHUNG_TU"
					, P."NGAY_HACH_TOAN"

				FROM purchase_document AS P
					JOIN purchase_document_line AS PD ON P."id" = PD."order_id"
					LEFT JOIN danh_muc_thue_suat_gia_tri_gia_tang T ON T."id" = PD."THUE_GTGT_ID"
				WHERE (ds_id_chung_tu LIKE '%%' || ngan_cach_giua_cac_ds
										   || CAST(P."id" AS VARCHAR(127)) || ngan_cach_giua_cac_ds
										   || '%%'
					   OR ds_id_chung_tu IS NULL
					  )
					  AND (P."HOA_DON_MUA_HANG_ID" IS NOT NULL
						   OR P."LOAI_CHUNG_TU" IN (363, 364, 365, 366,
														 368, 369, 370, 371,
														 372, 374, 375, 376,
													377, 378)
					  )
					  AND (ds_chi_nhanh_id IS NULL
						   OR ds_chi_nhanh_id LIKE '%%'
												   || CAST("CHI_NHANH_ID" AS VARCHAR(127)) || '%%'
					  )
					  AND "LOAI_HOA_DON" = '1'
		;

	END IF
	;

	-------------------------------------------
	--Trong trường hợp nhận hóa đơn thì lấy số chứng từ của chứng từ nhận hóa đơn chứ không lấy của chứng từ mua hàng


	INSERT  INTO GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO_TMP_KET_QUA
			 (
				  "ID_CHUNG_TU"      ,
				  "MODEL_CHUNG_TU_HD"  ,
				  "sale_document_id"     ,
				  "SO_CHUNG_TU_FINANCE"    ,
				  "SO_CHUNG_TU_FIRSTTAB"   ,
				  "PHAN_TRAM_TGTGT"       ,
				  "DIEN_GIAI"     ,
				  "NGAY_CHUNG_TU"   ,
				  "NGAY_HACH_TOAN"
			)

			SELECT
				  I."id"                      AS "ID_CHUNG_TU"
				 ,'purchase.ex.hoa.don.mua.hang'  AS "MODEL_CHUNG_TU_HD"
				, V."id"                      AS "sale_document_id"
				, I."SO_CHUNG_TU"             AS "SO_CHUNG_TU_FINANCE"
				, I."SO_CHUNG_TU"             AS "SO_CHUNG_TU_FIRSTTAB"
				, T."PHAN_TRAM_THUE_GTGT"                AS "PHAN_TRAM_TGTGT"
				, NULL                        AS "DIEN_GIAI"
				, I."NGAY_CHUNG_TU"
				, I."NGAY_HACH_TOAN"
			FROM purchase_ex_hoa_don_mua_hang I
				JOIN purchase_ex_hoa_don_mua_hang_chi_tiet ID ON I."id" = ID."HOA_DON_MUA_HANG_ID"
				JOIN purchase_document V ON V."HOA_DON_MUA_HANG_ID" = I."id"
				LEFT JOIN danh_muc_thue_suat_gia_tri_gia_tang T ON T."id" = ID."PHAN_TRAM_THUE_GTGT_ID"
			WHERE

				(ds_chi_nhanh_id IS NULL
				 OR ds_chi_nhanh_id LIKE '%%'
										 || CAST(I."CHI_NHANH_ID" AS VARCHAR(127)) || '%%'
				)
				AND I."NHAN_HOA_DON" = '0'
	;


	 INSERT  INTO  GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO_TMP_KET_QUA_CUOI_CUNG(
				SELECT DISTINCT
						A."ID_CHUNG_TU"  ,
						 A."MODEL_CHUNG_TU_HD"  ,
						A."sale_document_id" ,
						A."SO_CHUNG_TU_FINANCE" ,
						A."SO_CHUNG_TU_FIRSTTAB" ,
						A."PHAN_TRAM_TGTGT" ,
						A."DIEN_GIAI" ,
						A."NGAY_CHUNG_TU" ,
						A."NGAY_HACH_TOAN"
				FROM    GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO_TMP_KET_QUA A) ;

	RETURN QUERY SELECT *
				 FROM GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO_TMP_KET_QUA_CUOI_CUNG
	;

	END
	;

	$$ LANGUAGE PLpgSQL
	;







		""")



		self.env.cr.execute("""

		  DROP VIEW IF EXISTS tim_kiem_so_chung_tu ;
		  CREATE or REPLACE VIEW tim_kiem_so_chung_tu as (--View_VoucherRefNoFinance


	SELECT
		  M."id"                     AS "ID_CHUNG_TU"
		, 'account.ex.phieu.thu.chi' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"            AS "SO_CHUNG_TU"
		, NULL :: INT                AS "THUE_SUAT_PHAN_TRAM"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM account_ex_phieu_thu_chi M
	WHERE M."LOAI_PHIEU" = 'PHIEU_THU' AND M."TYPE_NH_Q" = 'NGAN_HANG'

	UNION ALL
	SELECT
		  M."id"                     AS "ID_CHUNG_TU"
		, 'account.ex.phieu.thu.chi' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"            AS "SO_CHUNG_TU"
		, NULL :: INT                AS "THUE_SUAT_PHAN_TRAM"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM account_ex_phieu_thu_chi M
	WHERE M."LOAI_PHIEU" = 'PHIEU_CHUYEN_TIEN' AND M."TYPE_NH_Q" = 'NGAN_HANG'

	UNION ALL
	SELECT
		  M."id"                     AS "ID_CHUNG_TU"
		, 'account.ex.phieu.thu.chi' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"            AS "SO_CHUNG_TU"
		, D."PHAN_TRAM_THUE_GTGT_ID"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM account_ex_phieu_thu_chi M
		LEFT JOIN account_ex_phieu_thu_chi_thue D ON M."id" = D."PHIEU_THU_THUE_ID"
	WHERE M."LOAI_PHIEU" = 'PHIEU_CHI' AND M."TYPE_NH_Q" = 'NGAN_HANG'

	UNION ALL
	SELECT
		  M."id"                     AS "ID_CHUNG_TU"
		, 'account.ex.phieu.thu.chi' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"            AS "SO_CHUNG_TU"
		, NULL :: INT                AS "THUE_SUAT_PHAN_TRAM"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM account_ex_phieu_thu_chi M
		INNER JOIN account_ex_phieu_thu_chi_tiet D ON M."id" = D."PHIEU_THU_CHI_ID"
	WHERE M."LOAI_PHIEU" = 'PHIEU_CHI' AND M."TYPE_NH_Q" = 'QUY'
	UNION ALL
	SELECT
		  M."id"                     AS "ID_CHUNG_TU"
		, 'account.ex.phieu.thu.chi' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"            AS "SO_CHUNG_TU"
		, NULL :: INT                AS "THUE_SUAT_PHAN_TRAM"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM account_ex_phieu_thu_chi M
		INNER JOIN account_ex_phieu_thu_chi_tiet D ON M."id" = D."PHIEU_THU_CHI_ID"
	WHERE M."LOAI_PHIEU" = 'PHIEU_THU' AND M."TYPE_NH_Q" = 'QUY'



	--đánh giá lại--


	UNION ALL
	SELECT
		  M."id"               AS "ID_CHUNG_TU"
		, 'asset.danh.gia.lai' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"      AS "SO_CHUNG_TU"
		, NULL :: INT          AS "THUE_SUAT_PHAN_TRAM"

		, M."KET_LUAN"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM asset_danh_gia_lai M
		INNER JOIN asset_danh_gia_lai_hach_toan D ON M."id" = D."DANH_GIA_LAI_TAI_SAN_CO_DINH_ID"
	UNION ALL
	SELECT
		  M."id"               AS "ID_CHUNG_TU"
		, 'asset.danh.gia.lai' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"      AS "SO_CHUNG_TU"
		, NULL :: INT          AS "THUE_SUAT_PHAN_TRAM"

		, M."KET_LUAN"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM asset_danh_gia_lai M
		INNER JOIN asset_danh_gia_lai_chi_tiet_dieu_chinh D ON M."id" = D."DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_ID"

	--ghi giảm--

	-- UNION ALL
	-- SELECT
	-- 		 M.RefID AS RefID
	-- 		,M.RefNo AS RefNoFinance
	-- 		,NULL AS TaxRate
	-- 		,NULL AS TACareerGroupID
	-- 		,M.JournalMemo
	-- 		,M.RefDate
	-- 		,M.PostedDate
	-- FROM	FAChangeFinancialLeasingToOwner M
	-- 		INNER JOIN FAChangeFinancialLeasingToOwnerDetail D ON M.RefID = D.RefID


	UNION ALL
	SELECT
		  M."id"           AS "ID_CHUNG_TU"
		, 'asset.ghi.giam' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"  AS "SO_CHUNG_TU"
		, NULL :: INT      AS "THUE_SUAT_PHAN_TRAM"

		, M."LY_DO_GIAM"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM asset_ghi_giam M
		INNER JOIN asset_ghi_giam_hach_toan D ON M."id" = D."TAI_SAN_CO_DINH_GHI_GIAM_ID"
	UNION ALL
	SELECT
		  M."id"           AS "ID_CHUNG_TU"
		, 'asset.ghi.giam' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"  AS "SO_CHUNG_TU"
		, NULL :: INT      AS "THUE_SUAT_PHAN_TRAM"

		, M."LY_DO_GIAM"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM asset_ghi_giam M
		INNER JOIN asset_ghi_giam_tai_san D ON M."id" = D."TAI_SAN_CO_DINH_GHI_GIAM_ID"

	--tính khấu hao--

	UNION ALL
	SELECT
		  M."id"                AS "ID_CHUNG_TU"
		, 'asset.tinh.khau.hao' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"       AS "SO_CHUNG_TU"
		, NULL :: INT           AS "THUE_SUAT_PHAN_TRAM"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM asset_tinh_khau_hao M
		INNER JOIN asset_tinh_khau_hao_hach_toan D ON M."id" = D."TINH_KHAU_HAO_ID"
	UNION ALL
	SELECT
		  M."id"                AS "ID_CHUNG_TU"
		, 'asset.tinh.khau.hao' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"       AS "SO_CHUNG_TU"
		, NULL :: INT           AS "THUE_SUAT_PHAN_TRAM"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM asset_tinh_khau_hao M
		INNER JOIN asset_tinh_khau_hao_chi_tiet D ON M."id" = D."TINH_KHAU_HAO_ID"

	--điều chuyển--

	UNION ALL
	SELECT
		  M."id"                    AS "ID_CHUNG_TU"
		, 'asset.dieu.chuyen'       AS "MODEL_CHUNG_TU"
		, M."BIEN_BAN_GIAO_NHAN_SO" AS "SO_CHUNG_TU"
		, NULL :: INT               AS "THUE_SUAT_PHAN_TRAM"

		, M."LY_DO_DIEU_CHUYEN"
		, M."NGAY"
		, M."NGAY"
	FROM asset_dieu_chuyen M
		INNER JOIN asset_dieu_chuyen_chi_tiet D ON M."id" = D."DIEU_CHUYEN_TAI_KHOAN_CO_DINH_ID"

	--ghi tăng--
	UNION ALL
	SELECT
		  M."id"             AS "ID_CHUNG_TU"
		, 'asset.ghi.tang'   AS "MODEL_CHUNG_TU"
		, M."SO_CT_GHI_TANG" AS "SO_CHUNG_TU"
		, NULL :: INT        AS "THUE_SUAT_PHAN_TRAM"

		, NULL               AS "DIEN_GIAI"
		, M."NGAY_GHI_TANG"
		, M."NGAY_GHI_TANG"
	FROM asset_ghi_tang M
	--chứng từ nghiệp vụ khác
	UNION ALL
	SELECT
		  M."id"                               AS "ID_CHUNG_TU"
		, 'account.ex.chung.tu.nghiep.vu.khac' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"                      AS "SO_CHUNG_TU"
		, D."PHAN_TRAM_THUE_GTGT_ID"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM account_ex_chung_tu_nghiep_vu_khac M
		LEFT JOIN account_ex_thue D ON M."id" = D."CHUNG_TU_KHAC_THUE_ID"

	--nhập xuất kho--
	UNION ALL
	SELECT
		  M."id"                   AS "ID_CHUNG_TU"
		, 'stock.ex.nhap.xuat.kho' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"          AS "SO_CHUNG_TU"
		, NULL :: INT              AS "THUE_SUAT_PHAN_TRAM"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM stock_ex_nhap_xuat_kho M
		INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet D ON M."id" = D."NHAP_XUAT_ID"
	WHERE M."type" = 'NHAP_KHO'
	UNION ALL
	SELECT
		  M."id"                     AS "ID_CHUNG_TU"
		, 'stock.ex.nhap.xuat.kho'   AS "MODEL_CHUNG_TU"
		, (CASE WHEN M."LOAI_CHUNG_TU" = 2021
		THEN M."SO_CHUNG_TU_CK_READONLY"
		   ELSE M."SO_CHUNG_TU" END) AS "SO_CHUNG_TU"
		, NULL :: INT                AS "THUE_SUAT_PHAN_TRAM"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM stock_ex_nhap_xuat_kho M
		INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet D ON M."id" = D."NHAP_XUAT_ID"
	WHERE M."type" = 'XUAT_KHO'

	UNION ALL
	SELECT
		  M."id"                     AS "ID_CHUNG_TU"
		, 'stock.ex.nhap.xuat.kho'   AS "MODEL_CHUNG_TU"
		, (CASE WHEN M."LOAI_CHUNG_TU" = 2030
		THEN M."SO_CHUNG_TU_CK_READONLY"
		   ELSE M."SO_CHUNG_TU" END) AS "SO_CHUNG_TU"
		, NULL :: INT                AS "THUE_SUAT_PHAN_TRAM"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM stock_ex_nhap_xuat_kho M
		INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet D ON M."id" = D."NHAP_XUAT_ID"
	WHERE M."type" = 'CHUYEN_KHO'

	--giá thành nghiệm thu---
	UNION ALL
	SELECT
		  M."id"                 AS "ID_CHUNG_TU"
		, 'gia.thanh.nghiem.thu' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"        AS "SO_CHUNG_TU"
		, NULL :: INT            AS "THUE_SUAT_PHAN_TRAM"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM gia_thanh_nghiem_thu M
		INNER JOIN gia_thanh_nghiem_thu_hach_toan D ON M."id" = D."CHI_TIET_ID"
	-- tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi--
	UNION ALL
	SELECT
		  M."id"                                                     AS "ID_CHUNG_TU"
		, 'tong.hop.phan.bo.chi.phi.bh.qldn.chi.phi.khac.cho.don.vi' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"                                            AS "SO_CHUNG_TU"
		, NULL :: INT                                                AS "THUE_SUAT_PHAN_TRAM"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_CHUNG_TU"
	FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi M
		INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_chi_phi D
			ON M."id" = D."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID"


	--gia_thanh_ket_chuyen_chi_phi
	UNION ALL
	SELECT
		  M."id"                         AS "ID_CHUNG_TU"
		, 'gia.thanh.ket.chuyen.chi.phi' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"                AS "SO_CHUNG_TU"
		, NULL :: INT                    AS "THUE_SUAT_PHAN_TRAM"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM gia_thanh_ket_chuyen_chi_phi M
		INNER JOIN gia_thanh_ket_chuyen_chi_phi_hach_toan D ON M."id" = D."CHI_TIET_ID"
	--account_ex_chi_phi_do_dang
	UNION ALL
	SELECT
		  M."id"                       AS "ID_CHUNG_TU"
		, 'account.ex.chi.phi.do.dang' AS "MODEL_CHUNG_TU"
		, 'OPN'                        AS "SO_CHUNG_TU"
		, NULL :: INT                  AS "THUE_SUAT_PHAN_TRAM"

		, NULL                         AS "DIEN_GIAI"
		, NULL                         AS "NGAY_CHUNG_TU"
		, NULL                         AS "NGAY_HACH_TOAN"
	FROM account_ex_chi_phi_do_dang M

	--số dư tài khoản chi tiết
	UNION ALL
	SELECT
		  M."id"                                AS "ID_CHUNG_TU"
		, 'account.ex.so.du.tai.khoan.chi.tiet' AS "MODEL_CHUNG_TU"
		, 'OPN'                                 AS "SO_CHUNG_TU"
		, NULL :: INT                           AS "THUE_SUAT_PHAN_TRAM"

		, NULL                                  AS "DIEN_GIAI"
		, M."NGAY_HACH_TOAN"
		, M."NGAY_HACH_TOAN"
	FROM account_ex_so_du_tai_khoan_chi_tiet M
	WHERE M."LOAI_CHUNG_TU" NOT IN ('612', '613', '614')
	UNION ALL
	SELECT
		  M."id"                                AS "ID_CHUNG_TU"
		, 'account.ex.so.du.tai.khoan.chi.tiet' AS "MODEL_CHUNG_TU"
		, 'OPN'                                 AS "SO_CHUNG_TU"
		, NULL :: INT                           AS "THUE_SUAT_PHAN_TRAM"

		, NULL                                  AS "DIEN_GIAI"
		, M."NGAY_HACH_TOAN"
		, M."NGAY_HACH_TOAN"
	FROM account_ex_so_du_tai_khoan_chi_tiet M
		INNER JOIN account_ex_sdtkct_theo_hoa_don D ON M."id" = D."SO_DU_TAI_KHOAN_CHI_TIET_ID"
	UNION ALL
	SELECT
		  M."id"                                AS "ID_CHUNG_TU"
		, 'account.ex.so.du.tai.khoan.chi.tiet' AS "MODEL_CHUNG_TU"
		, 'OPN'                                 AS "SO_CHUNG_TU"
		, NULL :: INT                           AS "THUE_SUAT_PHAN_TRAM"

		, NULL                                  AS "DIEN_GIAI"
		, M."NGAY_HACH_TOAN"
		, M."NGAY_HACH_TOAN"
	FROM account_ex_so_du_tai_khoan_chi_tiet M
		INNER JOIN account_ex_sdtkct_theo_doi_tuong D ON M."id" = D."SO_DU_TAI_KHOAN_CHI_TIET_ID"
	WHERE M."LOAI_CHUNG_TU" IN ('612', '613', '614') AND EXISTS(SELECT *
																FROM account_ex_sdtkct_theo_hoa_don OPI
																WHERE OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" = M."id")
	UNION ALL
	SELECT
		  M."id"                                AS "ID_CHUNG_TU"
		, 'account.ex.so.du.tai.khoan.chi.tiet' AS "MODEL_CHUNG_TU"
		, 'OPN'                                 AS "SO_CHUNG_TU"
		, NULL :: INT                           AS "THUE_SUAT_PHAN_TRAM"

		, NULL                                  AS "DIEN_GIAI"
		, M."NGAY_HACH_TOAN"
		, M."NGAY_HACH_TOAN"
	FROM account_ex_so_du_tai_khoan_chi_tiet M
		LEFT JOIN account_ex_sdtkct_theo_doi_tuong D ON M."id" = D."SO_DU_TAI_KHOAN_CHI_TIET_ID"
	WHERE M."LOAI_CHUNG_TU" IN ('612', '613', '614') AND NOT EXISTS(SELECT *
																	FROM account_ex_sdtkct_theo_hoa_don OPI
																	WHERE OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" = M."id")


	-- số dư tồn kho vthh
	UNION ALL
	SELECT
		  M."id"                               AS "ID_CHUNG_TU"
		, 'account.ex.ton.kho.vat.tu.hang.hoa' AS "MODEL_CHUNG_TU"
		, COALESCE(M."SO_CHUNG_TU", N'OPN')   AS "SO_CHUNG_TU"
		, NULL :: INT                          AS "THUE_SUAT_PHAN_TRAM"

		, NULL                                 AS "DIEN_GIAI"
		, M."NGAY_HACH_TOAN"
		, M."NGAY_HACH_TOAN"
	FROM account_ex_ton_kho_vat_tu_hang_hoa M
	--tien_luong_hach_toan_chi_phi_luong
	UNION ALL
	SELECT
		  M."id"                               AS "ID_CHUNG_TU"
		, 'tien.luong.hach.toan.chi.phi.luong' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"                      AS "SO_CHUNG_TU"
		, NULL :: INT                          AS "THUE_SUAT_PHAN_TRAM"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM tien_luong_hach_toan_chi_phi_luong M
		INNER JOIN tien_luong_hach_toan_chi_phi_luong_chi_tiet D ON M."id" = D."CHI_TIET_ID"

	--purchase_ex_giam_gia_hang_mua
	UNION ALL
	SELECT
		  M."id"                          AS "ID_CHUNG_TU"
		, 'purchase.ex.giam.gia.hang.mua' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"                 AS "SO_CHUNG_TU"
		, D."PHAN_TRAM_THUE_GTGT_ID"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM purchase_ex_giam_gia_hang_mua M
		INNER JOIN purchase_ex_giam_gia_hang_mua_chi_tiet D ON M."id" = D."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID"
		LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."id" = M."HOA_DON_MUA_HANG_ID"
	UNION ALL
	SELECT
		  M."id"                          AS "ID_CHUNG_TU"
		, 'purchase.ex.giam.gia.hang.mua' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"                 AS "SO_CHUNG_TU"
		, D."PHAN_TRAM_THUE_GTGT_ID"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM purchase_ex_giam_gia_hang_mua M
		INNER JOIN purchase_ex_giam_gia_hang_mua_chi_tiet D ON M."id" = D."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID"
		LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."id" = M."HOA_DON_MUA_HANG_ID"
	WHERE D."TK_THUE_GTGT_ID" IS NOT NULL AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)

	--purchase_ex_hoa_don_mua_hang
	UNION ALL
	SELECT
		  M."id"                         AS "ID_CHUNG_TU"
		, 'purchase.ex.hoa.don.mua.hang' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"                AS "SO_CHUNG_TU"
		, D."PHAN_TRAM_THUE_GTGT_ID"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM purchase_ex_hoa_don_mua_hang M
		INNER JOIN purchase_ex_hoa_don_mua_hang_chi_tiet D ON M."id" = D."HOA_DON_MUA_HANG_ID"
	WHERE M."NHAN_HOA_DON" = '0'

	--purchase_ex_don_mua_hang
	UNION ALL
	SELECT
		  M."id"                     AS "ID_CHUNG_TU"
		, 'purchase.ex.don.mua.hang' AS "MODEL_CHUNG_TU"
		, M."SO_DON_HANG"            AS "SO_CHUNG_TU"
		, D."PHAN_TRAM_THUE_GTGT_ID"

		, M."DIEN_GIAI"
		, M."NGAY_DON_HANG"
		, M."NGAY_DON_HANG"
	FROM purchase_ex_don_mua_hang M
		INNER JOIN purchase_ex_don_mua_hang_chi_tiet D ON M."id" = D."DON_MUA_HANG_CHI_TIET_ID"

	--purchase_ex_tra_lai_hang_mua
	UNION ALL
	SELECT
		  M."id"                         AS "ID_CHUNG_TU"
		, 'purchase.ex.tra.lai.hang.mua' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"                AS "SO_CHUNG_TU"
		, D."PHAN_TRAM_THUE_GTGT_ID"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM purchase_ex_tra_lai_hang_mua M
		INNER JOIN purchase_ex_tra_lai_hang_mua_chi_tiet D ON M."id" = D."CHUNG_TU_TRA_LAI_HANG_MUA_ID"
		LEFT JOIN sale_ex_hoa_don_ban_hang D1 ON D1."id" = M."HOA_DON_ID"
	UNION ALL
	SELECT
		  M."id"                         AS "ID_CHUNG_TU"
		, 'purchase.ex.tra.lai.hang.mua' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"                AS "SO_CHUNG_TU"
		, D."PHAN_TRAM_THUE_GTGT_ID"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM purchase_ex_tra_lai_hang_mua M
		INNER JOIN purchase_ex_tra_lai_hang_mua_chi_tiet D ON M."id" = D."CHUNG_TU_TRA_LAI_HANG_MUA_ID"
		LEFT JOIN sale_ex_hoa_don_ban_hang D1 ON D1."id" = M."HOA_DON_ID"
	WHERE D."TK_THUE_GTGT_ID" IS NOT NULL AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)

	--purchase_document
	UNION ALL
	SELECT
		  M."id"              AS "ID_CHUNG_TU"
		, 'purchase.document' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"     AS "SO_CHUNG_TU"
		, D."THUE_GTGT_ID"

		, M."DIEN_GIAI_CHUNG"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM purchase_document M
		INNER JOIN purchase_document_line D ON M."id" = D."order_id"
	WHERE M.type = 'dich_vu'
	UNION ALL
	SELECT
		  M."id"              AS "ID_CHUNG_TU"
		, 'purchase.document' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"     AS "SO_CHUNG_TU"
		, D."THUE_GTGT_ID"

		, M."DIEN_GIAI_CHUNG"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM purchase_document M
		INNER JOIN purchase_document_line D ON M."id" = D."order_id"
	WHERE D."TK_THUE_GTGT_ID" IS NOT NULL AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)
		  AND M.type = 'dich_vu'
	UNION ALL
	SELECT
		  M."id"              AS "ID_CHUNG_TU"
		, 'purchase.document' AS "MODEL_CHUNG_TU"
		, M."SO_PHIEU_NHAP"   AS "SO_CHUNG_TU"
		, D."THUE_GTGT_ID"

		, M."DIEN_GIAI_CHUNG"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM purchase_document M
		INNER JOIN purchase_document_line D ON M."id" = D."order_id"
		LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."id" = M."HOA_DON_MUA_HANG_ID"
	WHERE M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324, 325, 326, 327, 328)
	UNION ALL
	SELECT
		  M."id"              AS "ID_CHUNG_TU"
		, 'purchase.document' AS "MODEL_CHUNG_TU"
		, M."SO_PHIEU_NHAP"   AS "SO_CHUNG_TU"
		, D."THUE_GTGT_ID"

		, M."DIEN_GIAI_CHUNG"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM purchase_document M
		INNER JOIN purchase_document_line D ON M."id" = D."order_id"
		LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."id" = M."HOA_DON_MUA_HANG_ID"
	WHERE M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324, 325, 326, 327, 328) AND D."TK_THUE_NK_ID" IS NOT NULL AND
		  (D."TIEN_THUE_NK" <> 0 OR D."TIEN_THUE_NK_QUY_DOI" <> 0)
	UNION ALL
	SELECT
		  M."id"              AS "ID_CHUNG_TU"
		, 'purchase.document' AS "MODEL_CHUNG_TU"
		, M."SO_PHIEU_NHAP"   AS "SO_CHUNG_TU"
		, D."THUE_GTGT_ID"

		, M."DIEN_GIAI_CHUNG"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM purchase_document M
		INNER JOIN purchase_document_line D ON M."id" = D."order_id"
		LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."id" = M."HOA_DON_MUA_HANG_ID"
	WHERE
		M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324, 325, 326, 327, 328) AND D."TK_THUE_TTDB_ID" IS NOT NULL AND
		(D."TIEN_THUE_TTDB" <> 0 OR D."TIEN_THUE_TTDB_QUY_DOI" <> 0)
	UNION ALL
	SELECT
		  M."id"              AS "ID_CHUNG_TU"
		, 'purchase.document' AS "MODEL_CHUNG_TU"
		, M."SO_PHIEU_NHAP"   AS "SO_CHUNG_TU"
		, D."THUE_GTGT_ID"

		, M."DIEN_GIAI_CHUNG"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM purchase_document M
		INNER JOIN purchase_document_line D ON M."id" = D."order_id"
		LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."id" = M."HOA_DON_MUA_HANG_ID"
	WHERE
		M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324, 325, 326, 327, 328) AND D."TK_THUE_GTGT_ID" IS NOT NULL AND
		D."TK_DU_THUE_GTGT_ID" IS NOT NULL AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)
	UNION ALL
	SELECT

		  M."id"              AS "ID_CHUNG_TU"
		, 'purchase.document' AS "MODEL_CHUNG_TU"
		, M."SO_PHIEU_NHAP"   AS "SO_CHUNG_TU"
		, D."THUE_GTGT_ID"

		, M."DIEN_GIAI_CHUNG"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM purchase_document M
		INNER JOIN purchase_document_line D ON M."id" = D."order_id"
		LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."id" = M."HOA_DON_MUA_HANG_ID"
	WHERE
		M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324, 325, 326, 327, 328) AND D."TK_THUE_GTGT_ID" IS NOT NULL AND
		D."TK_DU_THUE_GTGT_ID" IS NULL AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)
	UNION ALL
	SELECT
		  M."id"              AS "ID_CHUNG_TU"
		, 'purchase.document' AS "MODEL_CHUNG_TU"
		, M."SO_PHIEU_NHAP"   AS "SO_CHUNG_TU"
		, D."THUE_GTGT_ID"

		, M."DIEN_GIAI_CHUNG"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM purchase_document M
		INNER JOIN purchase_document_line D ON M."id" = D."order_id"
		LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."id" = M."HOA_DON_MUA_HANG_ID"
	WHERE M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324, 325, 326, 327, 328)


	UNION ALL
	SELECT
		  M."id"              AS "ID_CHUNG_TU"
		, 'purchase.document' AS "MODEL_CHUNG_TU"
		, M."SO_PHIEU_NHAP"   AS "SO_CHUNG_TU"
		, D."THUE_GTGT_ID"

		, M."DIEN_GIAI_CHUNG"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM purchase_document M
		INNER JOIN purchase_document_line D ON M."id" = D."order_id"
		LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."id" = M."HOA_DON_MUA_HANG_ID"
	WHERE M."LOAI_CHUNG_TU" NOT IN (318, 319, 320, 321, 322, 324, 325, 326, 327, 328) AND
		  (D."TK_THUE_GTGT_ID" IS NULL OR M."LOAI_HOA_DON" = '0')
	UNION ALL
	SELECT
		  M."id"              AS "ID_CHUNG_TU"
		, 'purchase.document' AS "MODEL_CHUNG_TU"
		, M."SO_PHIEU_NHAP"   AS "SO_CHUNG_TU"
		, D."THUE_GTGT_ID"

		, M."DIEN_GIAI_CHUNG"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM purchase_document M
		INNER JOIN purchase_document_line D ON M."id" = D."order_id"
		LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."id" = M."HOA_DON_MUA_HANG_ID"
	WHERE
		M."LOAI_CHUNG_TU" NOT IN (318, 319, 320, 321, 322, 324, 325, 326, 327, 328) AND D."TK_THUE_GTGT_ID" IS NOT NULL
		AND M."LOAI_HOA_DON" = '1' AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)
	UNION ALL
	SELECT
		  M."id"              AS "ID_CHUNG_TU"
		, 'purchase.document' AS "MODEL_CHUNG_TU"
		, M."SO_PHIEU_NHAP"   AS "SO_CHUNG_TU"
		, D."THUE_GTGT_ID"

		, M."DIEN_GIAI_CHUNG"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM purchase_document M
		INNER JOIN purchase_document_line D ON M."id" = D."order_id"
		LEFT JOIN purchase_ex_hoa_don_mua_hang D1 ON D1."id" = M."HOA_DON_MUA_HANG_ID"
	WHERE
		M."LOAI_CHUNG_TU" NOT IN (318, 319, 320, 321, 322, 324, 325, 326, 327, 328) AND D."TK_THUE_GTGT_ID" IS NOT NULL
		AND M."LOAI_HOA_DON" = '1'

	--sale_ex_giam_gia_hang_ban

	UNION ALL
	SELECT
		  M."id"                      AS "ID_CHUNG_TU"
		, 'sale.ex.giam.gia.hang.ban' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"             AS "SO_CHUNG_TU"
		, D."PHAN_TRAM_THUE_GTGT_ID"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM sale_ex_giam_gia_hang_ban M
		INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban D ON M."id" = D."GIAM_GIA_HANG_BAN_ID"
		LEFT JOIN sale_ex_hoa_don_ban_hang D1 ON M."HOA_DON_BAN_HANG_ID" = D1."id"
	UNION ALL
	SELECT
		  M."id"                      AS "ID_CHUNG_TU"
		, 'sale.ex.giam.gia.hang.ban' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"             AS "SO_CHUNG_TU"
		, D."PHAN_TRAM_THUE_GTGT_ID"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM sale_ex_giam_gia_hang_ban M
		INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban D ON M."id" = D."GIAM_GIA_HANG_BAN_ID"
		LEFT JOIN sale_ex_hoa_don_ban_hang D1 ON M."HOA_DON_BAN_HANG_ID" = D1."id"
	WHERE D."TK_THUE_GTGT_ID" IS NOT NULL AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)
	UNION ALL
	SELECT
		  M."id"                      AS "ID_CHUNG_TU"
		, 'sale.ex.giam.gia.hang.ban' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"             AS "SO_CHUNG_TU"
		, D."PHAN_TRAM_THUE_GTGT_ID"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM sale_ex_giam_gia_hang_ban M
		INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban D ON M."id" = D."GIAM_GIA_HANG_BAN_ID"
		LEFT JOIN sale_ex_hoa_don_ban_hang D1 ON M."HOA_DON_BAN_HANG_ID" = D1."id"
	WHERE D."TK_CHIET_KHAU_ID" IS NOT NULL AND (D."TIEN_CHIET_KHAU" <> 0 OR D."TIEN_CHIET_KHAU_QUY_DOI" <> 0)

	--sale_ex_hoa_don_ban_hang

	UNION ALL
	SELECT
		  M."id"                     AS "ID_CHUNG_TU"
		, 'sale.ex.hoa.don.ban.hang' AS "MODEL_CHUNG_TU"
		, M."SO_HOA_DON"             AS "SO_CHUNG_TU"
		, D."THUE_GTGT"

		, NULL                       AS "DIEN_GIAI"
		, M."NGAY_HOA_DON"
		, M."NGAY_HOA_DON"
	FROM sale_ex_hoa_don_ban_hang M
		INNER JOIN sale_ex_chi_tiet_hoa_don_ban_hang D ON M."id" = D."HOA_DON_ID_ID"
	WHERE M."LAP_KEM_HOA_DON" = '0'



	---account_ex_don_dat_hang


	UNION ALL
	SELECT
		  M."id"                    AS "ID_CHUNG_TU"
		, 'account.ex.don.dat.hang' AS "MODEL_CHUNG_TU"
		, M."SO_DON_HANG"           AS "SO_CHUNG_TU"
		, D."PHAN_TRAM_THUE_GTGT_ID"

		, M."DIEN_GIAI"
		, M."NGAY_DON_HANG"
		, M."NGAY_DON_HANG"
	FROM account_ex_don_dat_hang M
		INNER JOIN account_ex_don_dat_hang_chi_tiet D ON M."id" = D."DON_DAT_HANG_CHI_TIET_ID"

	--sale_ex_bao_gia
	UNION ALL
	SELECT
		  M."id"            AS "ID_CHUNG_TU"
		, 'sale.ex.bao.gia' AS "MODEL_CHUNG_TU"
		, M."SO_BAO_GIA"    AS "SO_CHUNG_TU"
		, D."PHAN_TRAM_THUE_GTGT_ID"

		, M."GHI_CHU"
		, M."NGAY_BAO_GIA"
		, M."NGAY_BAO_GIA"
	FROM sale_ex_bao_gia M
		INNER JOIN sale_ex_bao_gia_chi_tiet D ON M."id" = D."BAO_GIA_CHI_TIET_ID"

	--sale_ex_tra_lai_hang_ban
	UNION ALL
	SELECT
		  M."id"                     AS "ID_CHUNG_TU"
		, 'sale.ex.tra.lai.hang.ban' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"            AS "SO_CHUNG_TU"
		, D."PHAN_TRAM_THUE_GTGT_ID"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM sale_ex_tra_lai_hang_ban M
		INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet D ON M."id" = D."TRA_LAI_HANG_BAN_ID"
	UNION ALL
	SELECT
		  M."id"                     AS "ID_CHUNG_TU"
		, 'sale.ex.tra.lai.hang.ban' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"            AS "SO_CHUNG_TU"
		, D."PHAN_TRAM_THUE_GTGT_ID"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM sale_ex_tra_lai_hang_ban M
		INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet D ON M."id" = D."TRA_LAI_HANG_BAN_ID"
	WHERE D."TK_THUE_GTGT_ID" IS NOT NULL AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)
	UNION ALL
	SELECT
		  M."id"                     AS "ID_CHUNG_TU"
		, 'sale.ex.tra.lai.hang.ban' AS "MODEL_CHUNG_TU"
		, M."SO_CHUNG_TU"            AS "SO_CHUNG_TU"
		, D."PHAN_TRAM_THUE_GTGT_ID"

		, M."DIEN_GIAI"
		, M."NGAY_CHUNG_TU"
		, M."NGAY_HACH_TOAN"
	FROM sale_ex_tra_lai_hang_ban M
		INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet D ON M."id" = D."TRA_LAI_HANG_BAN_ID"
	WHERE D."TK_CHIET_KHAU" IS NOT NULL AND (D."TIEN_CHIET_KHAU" <> 0 AND D."TIEN_CHIET_KHAU_QUY_DOI" <> 0)

	--sale_document

	UNION ALL
	SELECT
			 M."id" AS "ID_CHUNG_TU"
			, 'sale.document' AS "MODEL_CHUNG_TU"
			,M."SO_CHUNG_TU" AS "SO_CHUNG_TU"
			,D."THUE_GTGT_ID"

			,M."DIEN_GIAI"
				,M."NGAY_CHUNG_TU"
			,M."NGAY_HACH_TOAN"
	FROM	sale_document M
			INNER JOIN sale_document_line D ON M."id" = D."SALE_DOCUMENT_ID"
	WHERE M."LOAI_CHUNG_TU" = 3532 AND D."TK_THUE_XK_ID" IS NOT NULL AND D."TIEN_THUE_XUAT_KHAU" <> 0
	UNION ALL
	SELECT
			 M."id" AS "ID_CHUNG_TU"
			, 'sale.document' AS "MODEL_CHUNG_TU"
			,M."SO_CHUNG_TU" AS "SO_CHUNG_TU"
			,D."THUE_GTGT_ID"

			,M."DIEN_GIAI"
				,M."NGAY_CHUNG_TU"
			,M."NGAY_HACH_TOAN"
	FROM	sale_document M
			INNER JOIN sale_document_line D ON M."id" = D."SALE_DOCUMENT_ID"
	WHERE M."LOAI_CHUNG_TU" IN (3534,3535,3536,3538)
	UNION ALL
	SELECT
			 M."id" AS "ID_CHUNG_TU"
			, 'sale.document' AS "MODEL_CHUNG_TU"
			,M."SO_CHUNG_TU" AS "SO_CHUNG_TU"
			,D."THUE_GTGT_ID"

			,M."DIEN_GIAI"
				,M."NGAY_CHUNG_TU"
			,M."NGAY_HACH_TOAN"
	FROM	sale_document M
			INNER JOIN sale_document_line D ON M."id" = D."SALE_DOCUMENT_ID"
	WHERE M."LOAI_CHUNG_TU" IN (3534,3535,3536,3538) AND D."TK_THUE_XK_ID" IS NOT NULL AND D."TIEN_THUE_XUAT_KHAU" <> 0
	UNION ALL
	SELECT
			 M."id" AS "ID_CHUNG_TU"
			, 'sale.document' AS "MODEL_CHUNG_TU"
			,M."SO_CHUNG_TU" AS "SO_CHUNG_TU"
			,D."THUE_GTGT_ID"

			,M."DIEN_GIAI"
				,M."NGAY_CHUNG_TU"
			,M."NGAY_HACH_TOAN"
	FROM	sale_document M
			INNER JOIN sale_document_line D ON M."id" = D."SALE_DOCUMENT_ID"
	WHERE M."LOAI_CHUNG_TU" NOT IN (3534,3535,3536,3538)
	UNION ALL
	SELECT
			 M."id" AS "ID_CHUNG_TU"
			, 'sale.document' AS "MODEL_CHUNG_TU"
			,M."SO_CHUNG_TU" AS "SO_CHUNG_TU"
			,D."THUE_GTGT_ID"

			,M."DIEN_GIAI"
				,M."NGAY_CHUNG_TU"
			,M."NGAY_HACH_TOAN"
	FROM	sale_document M
			INNER JOIN sale_document_line D ON M."id" = D."SALE_DOCUMENT_ID"
	WHERE M."LOAI_CHUNG_TU" NOT IN (3534,3535,3536,3538) AND D."TK_CHIET_KHAU_ID" IS NOT NULL AND (D."TIEN_CHIET_KHAU" <> 0 OR D."TIEN_CK_QUY_DOI" <> 0)
	UNION ALL
	SELECT
			 M."id" AS "ID_CHUNG_TU"
			, 'sale.document' AS "MODEL_CHUNG_TU"
			,M."SO_CHUNG_TU" AS "SO_CHUNG_TU"
			,D."THUE_GTGT_ID"

			,M."DIEN_GIAI"
				,M."NGAY_CHUNG_TU"
			,M."NGAY_HACH_TOAN"
	FROM	sale_document M
			INNER JOIN sale_document_line D ON M."id" = D."SALE_DOCUMENT_ID"
	WHERE M."LOAI_CHUNG_TU" NOT IN (3534,3535,3536,3538) AND D."TK_THUE_GTGT_ID" IS NOT NULL AND (D."TIEN_THUE_GTGT" <> 0 OR D."TIEN_THUE_GTGT_QUY_DOI" <> 0)

	--supply_dieu_chinh
	UNION ALL
	SELECT
			 M."id" AS "ID_CHUNG_TU"
			, 'supply.dieu.chinh' AS "MODEL_CHUNG_TU"
			,M."SO_CHUNG_TU" AS "SO_CHUNG_TU"
			,NULL ::INT AS "THUE_SUAT_PHAN_TRAM"

			,M."LY_DO_DIEU_CHINH"
				,M."NGAY_CHUNG_TU"
			,M."NGAY_CHUNG_TU"
	FROM	supply_dieu_chinh M
			INNER JOIN supply_dieu_chinh_chi_tiet D ON M."id" = D."CHI_TIET_DIEU_CHINH_CCDC_ID_ID"

		--supply_phan_bo_chi_phi
	UNION ALL
	SELECT
			 M."id" AS "ID_CHUNG_TU"
			, 'supply.phan.bo.chi.phi' AS "MODEL_CHUNG_TU"
			,M."SO_CHUNG_TU" AS "SO_CHUNG_TU"
			,NULL ::INT AS "THUE_SUAT_PHAN_TRAM"

			,M."DIEN_GIAI"
				,M."NGAY_CHUNG_TU"
			,M."NGAY_HACH_TOAN"
	FROM	supply_phan_bo_chi_phi M
			INNER JOIN supply_phan_bo_chi_phi_hach_toan D ON M."id" = D."PHAN_BO_CHI_PHI_ID"
	UNION ALL
	SELECT
			 M."id" AS "ID_CHUNG_TU"
			, 'supply.phan.bo.chi.phi' AS "MODEL_CHUNG_TU"
			,M."SO_CHUNG_TU" AS "SO_CHUNG_TU"
			,NULL ::INT AS "THUE_SUAT_PHAN_TRAM"

			,M."DIEN_GIAI"
				,M."NGAY_CHUNG_TU"
			,M."NGAY_HACH_TOAN"
	FROM	supply_phan_bo_chi_phi M
			INNER JOIN supply_phan_bo_chi_phi_muc_chi_phi D ON M."id" = D."PHAN_BO_CHI_PHI_ID"

		--supply_ghi_giam
	UNION ALL
	SELECT
			 M."id" AS "ID_CHUNG_TU"
			, 'supply.ghi.giam' AS "MODEL_CHUNG_TU"
			,M."SO_CHUNG_TU" AS "SO_CHUNG_TU"
			,NULL ::INT AS "THUE_SUAT_PHAN_TRAM"

			,M."LY_DO_GHI_GIAM"
				,M."NGAY_CHUNG_TU"
			,M."NGAY_CHUNG_TU"
	FROM	supply_ghi_giam M
			INNER JOIN supply_ghi_giam_chi_tiet D ON M."id" = D."CCDC_GHI_GIAM_ID"

		--supply_ghi_tang
	UNION ALL
	SELECT
			 M."id" AS "ID_CHUNG_TU"
			, 'supply.ghi.tang' AS "MODEL_CHUNG_TU"
			,M."SO_CT_GHI_TANG" AS "SO_CHUNG_TU"
			,NULL ::INT AS "THUE_SUAT_PHAN_TRAM"

			,NULL AS "DIEN_GIAI"
				,M."NGAY_GHI_TANG"
			,M."NGAY_GHI_TANG"
	FROM	supply_ghi_tang M
			INNER JOIN supply_ghi_tang_don_vi_su_dung D ON M."id" = D."GHI_TANG_DON_VI_SU_DUNG_ID"

		--supply_dieu_chuyen_cong_cu_dung_cu
	UNION ALL
	SELECT
			 M."id" AS "ID_CHUNG_TU"
			, 'supply.dieu.chuyen.cong.cu.dung.cu' AS "MODEL_CHUNG_TU"
			,M."BIEN_BAN_GIAO_NHAN_SO" AS "SO_CHUNG_TU"
			,NULL ::INT AS "THUE_SUAT_PHAN_TRAM"

			,M."LY_DO_DIEU_CHUYEN"
				,M."NGAY"
			,M."NGAY"
	FROM	supply_dieu_chuyen_cong_cu_dung_cu M
			INNER JOIN supply_dieu_chuyen_chi_tiet D ON M."id" = D."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID"
		--purchase_ex_hop_dong_mua_hang
	UNION ALL
	SELECT
			 M."id" AS "ID_CHUNG_TU"
			, 'purchase.ex.hop.dong.mua.hang' AS "MODEL_CHUNG_TU"
			,M."SO_HOP_DONG" AS "SO_CHUNG_TU"
			,NULL ::INT AS "THUE_SUAT_PHAN_TRAM"

			,NULL AS "DIEN_GIAI"
			,M."NGAY_KY"
			,M."NGAY_KY"
	FROM	purchase_ex_hop_dong_mua_hang M  ) ;







		  """)

		self.env.cr.execute(""" 
				 DROP VIEW IF EXISTS tim_kiem_so_chung_tu_chi_tiet ;
				CREATE or REPLACE VIEW tim_kiem_so_chung_tu_chi_tiet as ( --[View_VoucherPUInvoiceDetail]
	SELECT
			U."DON_VI_TINH" ,
			PUD."SO_LUONG" ,
			PUD."DON_GIA" ,
			PUD."THANH_TIEN" ,
			PUD."id",
			'purchase.document.line' AS "MODEL_CHI_TIET"
	FROM    purchase_document_line AS PUD
			LEFT JOIN danh_muc_don_vi_tinh U ON U."id" = PUD."DVT_ID"

	UNION ALL
	SELECT  U."DON_VI_TINH" ,
			PUD."SO_LUONG" ,
			PUD."DON_GIA" ,
			PUD."THANH_TIEN" ,
			PUD."id",
			'purchase.ex.giam.gia.hang.mua.chi.tiet' AS "MODEL_CHI_TIET"
	FROM    purchase_ex_giam_gia_hang_mua_chi_tiet AS PUD
			LEFT JOIN danh_muc_don_vi_tinh U ON U."id" = PUD."DVT_ID"
	UNION ALL
	SELECT  U."DON_VI_TINH" ,
			PUD."SO_LUONG" ,
			PUD."DON_GIA" ,
			PUD."THANH_TIEN" ,
			PUD."id",
			'purchase.ex.tra.lai.hang.mua.chi.tiet' AS "MODEL_CHI_TIET"
	FROM    purchase_ex_tra_lai_hang_mua_chi_tiet AS PUD
			LEFT JOIN danh_muc_don_vi_tinh U ON U."id" = PUD."DVT_ID"
	UNION ALL
	SELECT  U."DON_VI_TINH" ,
			PUD."SO_LUONG" ,
			PUD."DON_GIA" ,
			PUD."THANH_TIEN" ,
		   PUD."id",
			'sale.ex.tra.lai.hang.ban.chi.tiet' AS "MODEL_CHI_TIET"
	FROM    sale_ex_tra_lai_hang_ban_chi_tiet AS PUD
			LEFT JOIN danh_muc_don_vi_tinh U ON U."id" = PUD."DVT_ID"
	-- nhận hóa đơn
	UNION ALL
	SELECT  U."DON_VI_TINH" ,
			PUVD."SO_LUONG" ,
			PUVD."DON_GIA" ,
			PUVD."THANH_TIEN" ,
			PUD."id",
			'purchase.ex.hoa.don.mua.hang.chi.tiet' AS "MODEL_CHI_TIET"
	FROM    purchase_ex_hoa_don_mua_hang_chi_tiet AS PUD
			INNER JOIN purchase_document_line PUVD ON PUVD."id" = PUD."CHUNG_TU_MUA_HANG_CHI_TIET_ID"
			LEFT JOIN danh_muc_don_vi_tinh U ON U."id" = PUVD."DVT_ID" ) ;



		 """)

class BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_GROUP(models.Model):
	_name = 'bao.cao.bang.ke.hoa.don.chung.tu.group'
	_auto = False
	_description = 'Nhóm các hóa đơn chứng từ theo Nhóm HHDV'

	NHOM_HHDV_MUA_VAO = fields.Char()
	
	sum_GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE = fields.Monetary(currency_field='base_currency_id')
	sum_THUE_GTGT = fields.Monetary(currency_field='base_currency_id')
	base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)
	data = fields.One2many('bao.cao.bang.ke.hoa.don.chung.tu', 'BANG_KE_HOA_DON_CT_GROUP_ID')
		
class BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_bang_ke_hoa_don_chung_tu'


	TONG_GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE = fields.Monetary(currency_field='base_currency_id')
	TONG_THUE_GTGT = fields.Monetary(currency_field='base_currency_id')
	base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)
	
	@api.model
	def get_report_values(self, docids, data=None):
		env = self.env[data.get('model')]
		docs = [env.new(d) for d in env.with_context(data.get('context')).search_read()]
		
		grouped_data = {}
		for record in docs:			
			nhom_hhdv_mua_vao = record.NHOM_HHDV_MUA_VAO
			if not grouped_data.get(nhom_hhdv_mua_vao):
				grouped_data[nhom_hhdv_mua_vao] = self.env['bao.cao.bang.ke.hoa.don.chung.tu.group'].new({
					'data': [],
					'sum_GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE': 0,
					'sum_THUE_GTGT': 0,
					
					'NHOM_HHDV_MUA_VAO': record.NHOM_HHDV_MUA_VAO or '',
				})

			grouped_data[nhom_hhdv_mua_vao].data += record
			grouped_data[nhom_hhdv_mua_vao].sum_GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE += record.GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE
			grouped_data[nhom_hhdv_mua_vao].sum_THUE_GTGT += record.THUE_GTGT

		added_data = {
			'tieu_de_nguoi_ky': self.get_danh_sach_tieu_de_nguoi_ky(data.get('model')),
			'ten_nguoi_ky': self.get_danh_sach_ten_nguoi_ky(data.get('model')),
			'sub_title': data.get('breadcrumb'),
		}

		tong_GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE = 0
		tong_THUE_GTGT = 0
		for nhom_hhdv_mua_vao in grouped_data:
			tong_GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE += grouped_data[nhom_hhdv_mua_vao].sum_GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE
			tong_THUE_GTGT += grouped_data[nhom_hhdv_mua_vao].sum_THUE_GTGT
		
		tong_all = self.env['report.bao_cao.template_bang_ke_hoa_don_chung_tu'].new({
			'TONG_GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE': tong_GIA_TRI_HHDV_MUA_VAO_CHUA_CO_THUE,
			'TONG_THUE_GTGT': tong_THUE_GTGT,
			})
		
		return {
			'docs': docs,
			'grouped_data': grouped_data,
			'added_data': added_data,
			'o': tong_all,
		}