# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_GIAY_BAO_NO(models.Model):
	_name = 'bao.cao.giay.bao.no'
	_auto = False

	ref = fields.Char(string='Reffence ID')

	ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
	MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')

	SO_TAI_KHOAN_NGAN_HANG = fields.Char(string='Số tài khoản ngân hàng') #BankAccount
	TEN_NGAN_HANG = fields.Char(string='Tên ngân hàng')#BankName
	
	NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ') #RefDate
	
	SO_CHUNG_TU = fields.Char(string='Số chứng từ') #RefNo
	DIA_CHI = fields.Char(string='Địa chỉ') #AccountObjectAddress
	DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải') #JournalMemo
	LOAI_TIEN = fields.Char(string='Loại tiền') #CurrencyID
	TY_GIA = fields.Monetary(string='Tỷ giá', currency_field='currency_id') #ExchangeRate
	TEN_KHACH_HANG = fields.Char(string='Tên khách hàng') #AccountObjectName
	SO_TAI_KHOAN_NGAN_HANG_DOI_TUONG = fields.Char(string='Số tài khoản ngân hàng đối tượng') #AccountObjectBankAccount
	TEN_NGAN_HANG_DOI_TUONG = fields.Char(string='Tên ngân hàng đối tượng') #AccountObjectBankName

	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
	TONG_TIEN = fields.Monetary(string='Tổng tiền', currency_field='currency_id') #TotalAmountOC
	TONG_TIEN_QUY_DOI = fields.Monetary(string='Tổng tiền quy đổi', currency_field='currency_id') #TotalAmount

	TK_CONG_NO = fields.Char(string='TK công nợ') #AccountNumber
	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())

	ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.giay.bao.no.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')



class BAO_CAO_GIAY_BAO_NO_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_debitannouncement'

	@api.model
	def get_report_values(self, docids, data=None):
		############### START SQL lấy dữ liệu ###############
		refTypeList, records = self.get_reftype_list(data)
		sql_result = self.ham_lay_du_lieu_sql_tra_ve(refTypeList)

		for line in sql_result:
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
			master_data = self.env['bao.cao.giay.bao.no'].convert_for_update(line)
			detail_data = self.env['bao.cao.giay.bao.no.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
				records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.giay.bao.no.chi.tiet'].new(detail_data)
		
		docs = [records.get(k) for k in records]

		for record in docs:
			if not record.LOAI_TIEN:
				record.currency_id = self.lay_loai_tien_mac_dinh()
			else:
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', record.LOAI_TIEN)],limit=1)
				if loai_tien_id:
					record.currency_id = loai_tien_id.id
			
			for line in record.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
				line.currency_id = record.currency_id

		return {
			'docs': docs,
        }

	def ham_lay_du_lieu_sql_tra_ve(self,refTypeList):
		query = """
		DO LANGUAGE plpgsql $$
		DECLARE
		
		ListParam                        VARCHAR := N'""" + refTypeList + """';

		rec                              RECORD;




		LOAI_TIEN_CHINH                  INT;

		CHE_DO_KE_TOAN                   VARCHAR;

		PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY VARCHAR;

		DIEN_GIAI_TY_GIA_XUAT_QUY        VARCHAR(100) := N'Chênh lệch tỷ giá xuất quỹ';


		BEGIN


		SELECT value
		INTO LOAI_TIEN_CHINH
		FROM ir_config_parameter
		WHERE key = 'he_thong.LOAI_TIEN_CHINH'
		FETCH FIRST 1 ROW ONLY
		;

		SELECT value
		INTO CHE_DO_KE_TOAN
		FROM ir_config_parameter
		WHERE key = 'he_thong.CHE_DO_KE_TOAN'
		FETCH FIRST 1 ROW ONLY
		;

		SELECT value
		INTO PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY
		FROM ir_config_parameter
		WHERE key = 'he_thong.PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY'
		FETCH FIRST 1 ROW ONLY
		;


		DROP TABLE IF EXISTS TMP_ID_CHUNG_TU
		;

		DROP SEQUENCE IF EXISTS TMP_ID_CHUNG_TU_seq
		;

		CREATE TEMP SEQUENCE TMP_ID_CHUNG_TU_seq
		;

		CREATE TEMP TABLE TMP_ID_CHUNG_TU
		(
		"ID_CHUNG_TU"     INT,
		"LOAI_CHUNG_TU"   INT,

		"MasterSortOrder" INT DEFAULT NEXTVAL('TMP_ID_CHUNG_TU_seq')
		PRIMARY KEY

		)
		;

		INSERT INTO TMP_ID_CHUNG_TU
		SELECT

		Value1
		, Value2


		FROM CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(ListParam, ',', ';') F
		INNER JOIN danh_muc_reftype R ON F.Value2 = R."REFTYPE"
		;

		DROP TABLE IF EXISTS TMP_KET_QUA
		;

		CREATE TEMP TABLE TMP_KET_QUA
		(
		"SO_TAI_KHOAN_NGAN_HANG"           VARCHAR(255),
		"TEN_NGAN_HANG"                    VARCHAR(255),
		"NGAY_CHUNG_TU"                    TIMESTAMP,
		"ID_CHUNG_TU"                      INT,
		"MODEL_CHUNG_TU"                   VARCHAR(255),
		"SO_CHUNG_TU"                      VARCHAR(255),
		"LOAI_CHUNG_TU"                    INT,
		"DIA_CHI"                          VARCHAR(255),
		"DIEN_GIAI"                        VARCHAR(255),
		"LOAI_TIEN"                        VARCHAR(15),
		"TY_GIA"                           DECIMAL(25, 8),
		"TEN_KHACH_HANG"                   VARCHAR(255),
		"SO_TAI_KHOAN_NGAN_HANG_DOI_TUONG" VARCHAR(255),
		"TEN_NGAN_HANG_DOI_TUONG"          VARCHAR(255),

		"THANH_TIEN"                       DECIMAL(25, 8),
		"THANH_TIEN_QUY_DOI"               DECIMAL(25, 8),
		"TK_NO"                            VARCHAR(255),
		"TK_CO"                            VARCHAR(255),
		"TK_CONG_NO"                       VARCHAR(255),
		"DIEN_GIAI_DETAIL"                 VARCHAR(255),

		"MasterSortOrder"                  INT,
		"STT"                              INT,
		"SortOrderDetail"                  VARCHAR(255) --Dòng hạch toán không liên quan đến xuất quỹ đứng trước, dòng liên quan đến xuất quỹ đứng sau
		)
		;


		FOR rec IN
		SELECT
		DISTINCT
		PR."ID_CHUNG_TU"   AS "ID_CHUNG_TU"
		, PR."LOAI_CHUNG_TU" AS "LOAI_CHUNG_TU"
		FROM
		TMP_ID_CHUNG_TU PR
		LOOP


		IF rec."LOAI_CHUNG_TU" = ANY ('{1510,1511,1512,1513,1514,1520,1521,1522,1523,1530,1531}' :: INT [])-- 'BAWithdraw'
		THEN
		INSERT INTO TMP_KET_QUA
		SELECT w.*
		FROM (SELECT
		BA."SO_TAI_KHOAN"
		, BAW."TEN_TK_CHI"
		, BAW."NGAY_CHUNG_TU"
		, BAW."id"
		, 'account.ex.phieu.thu.chi'                                           AS "MODEL_CHUNG_TU"
		, BAW."SO_CHUNG_TU"
		, BAW."LOAI_CHUNG_TU"
		, BAW."DIA_CHI"
		, BAW."DIEN_GIAI"
		, (SELECT "MA_LOAI_TIEN"
		FROM res_currency T
		WHERE T.id = BAW."currency_id")                                     AS "LOAI_TIEN"
		, BAW."TY_GIA"
		, CASE WHEN BAW."TEN_DOI_TUONG" IS NOT NULL
		AND BAW."TEN_DOI_TUONG" <> ''
		THEN BAW."TEN_DOI_TUONG"
		ELSE res_partner."HO_VA_TEN"
		END                                                                  AS "TEN_KHACH_HANG"
		, BAW."TAI_KHOAN_NHAN_UNC_NOP_TIEN"

		, BAW."TEN_TK_NHAN"

		, BAWD."SO_TIEN"
		,
		--Modify by thidv: Lấy số tiền quy đổi = min(của cột thành tiền và cột quy đổi theo tỷ giá xuất quỹ)
		(CASE WHEN BAWD."TK_XU_LY_CHENH_LECH"
		IS NOT NULL -- có chênh lệch tỷ giá
		AND PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY = 'BINH_QUAN_TUC_THOI'

		AND BAW."currency_id" <> LOAI_TIEN_CHINH  -- có hạch toán ngoại tệ
		AND BAWD."SO_TIEN_QUY_DOI" > BAWD."QUY_DOI_THEO_TGXQ"

		THEN
		BAWD."QUY_DOI_THEO_TGXQ"

		ELSE BAWD."SO_TIEN_QUY_DOI"
		END)                                                                AS "THANH_TIEN_QUY_DOI"
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_NO_ID")                                      AS "TK_NO"

		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_CO_ID")                                      AS "TK_CO"
		, LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_SEC_UY_NHIEM_CHI(BAW."id",
												'112') AS "TK_CONG_NO"
		, BAWD."DIEN_GIAI_DETAIL"


		, R."MasterSortOrder"                                                  AS "MasterSortOrder"
		, BAWD."THU_TU_SAP_XEP_CHI_TIET"                                       AS "STT"
		, CAST(0 AS
		VARCHAR(127))                                                    AS "SortOrderDetail"

		FROM account_ex_phieu_thu_chi BAW
		INNER JOIN TMP_ID_CHUNG_TU R ON BAW."id" = r."ID_CHUNG_TU"
		INNER JOIN account_ex_phieu_thu_chi_tiet BAWD ON BAW."id" = BAWD."PHIEU_THU_CHI_ID"
		LEFT JOIN res_partner ON res_partner."id" = BAW."DOI_TUONG_ID"
		LEFT JOIN res_partner AS AO ON BAWD."DOI_TUONG_ID" = AO."id"

		LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = BAW."TAI_KHOAN_CHI_GUI_ID"
		WHERE R."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
		R."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
		UNION ALL
		--Add by Thidv: Lấy thêm dòng định khoản chênh lệch tỷ giá xuất quỹ
		SELECT
		BA."SO_TAI_KHOAN"
		, BAW."TEN_TK_CHI"
		, BAW."NGAY_CHUNG_TU"
		, BAW."id"
		, 'account.ex.phieu.thu.chi'                                           AS "MODEL_CHUNG_TU"
		, BAW."SO_CHUNG_TU"                                                    AS "SO_CHUNG_TU"
		, BAW."LOAI_CHUNG_TU"
		, BAW."DIA_CHI"
		, BAW."DIEN_GIAI"
		, (SELECT "MA_LOAI_TIEN"
		FROM res_currency T
		WHERE T.id = BAW."currency_id")                                     AS "LOAI_TIEN"
		, BAW."TY_GIA"
		, CASE WHEN BAW."TEN_DOI_TUONG" IS NOT NULL
		AND BAW."TEN_DOI_TUONG" <> ''
		THEN BAW."TEN_DOI_TUONG"
		ELSE res_partner."HO_VA_TEN"
		END                                                                  AS "TEN_KHACH_HANG"
		, BAW."TAI_KHOAN_NHAN_UNC_NOP_TIEN"

		, BAW."TEN_TK_NHAN"
		, --Tiền nguyên tệ =0
		CAST(0 AS
		DECIMAL(18, 4))                                                 AS "THANH_TIEN"
		,
		--Modify by thidv: Lấy số tiền quy đổi = min(của cột thành tiền và cột quy đổi theo tỷ giá xuất quỹ)
		--Lấy tiền chênh lệch tỷ giá làm tiền quy đổi
		ABS(BAWD."QUY_DOI_THEO_TGXQ")
														AS "SO_TIEN"
		, (CASE WHEN BAWD."SO_TIEN_QUY_DOI" < BAWD."QUY_DOI_THEO_TGXQ"

		THEN (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_XU_LY_CHENH_LECH")

		ELSE (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_NO_ID")
		END)                                                                AS "TK_NO"
		, --Lãi thì lấy TK 515 là TK có, lãi TK có = TK có
		(CASE WHEN BAWD."SO_TIEN_QUY_DOI" <
		BAWD."QUY_DOI_THEO_TGXQ"

		THEN (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_CO_ID")
		ELSE (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_XU_LY_CHENH_LECH")
		END)                                                                AS "TK_CO"
		, LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_SEC_UY_NHIEM_CHI(BAW."id",
												'112') AS "TK_CONG_NO"
		, DIEN_GIAI_TY_GIA_XUAT_QUY


		, R."MasterSortOrder"                                                  AS "MasterSortOrder"
		, BAWD."THU_TU_SAP_XEP_CHI_TIET"                                       AS "STT"
		, CAST(1 AS VARCHAR(127))                                               AS "SortOrderDetail"

		FROM account_ex_phieu_thu_chi BAW
		INNER JOIN TMP_ID_CHUNG_TU R ON BAW."id" = r."ID_CHUNG_TU"
		INNER JOIN account_ex_phieu_thu_chi_tiet BAWD ON BAW."id" = BAWD."PHIEU_THU_CHI_ID"
		LEFT JOIN res_partner ON res_partner."id" = BAW."DOI_TUONG_ID"
		LEFT JOIN res_partner AS AO ON BAWD."DOI_TUONG_ID" = AO."id"

		LEFT JOIN res_partner AS EM ON EM."id" = BAW."NHAN_VIEN_ID"

		LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = BAW."TAI_KHOAN_CHI_GUI_ID"
		WHERE (
		BAWD."TK_XU_LY_CHENH_LECH" IS NOT NULL
		)


		AND PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY = 'BINH_QUAN_TUC_THOI'

		AND BAW."currency_id" <>
		LOAI_TIEN_CHINH
		AND R."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
		R."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"


		) W
		ORDER BY
		w."MasterSortOrder",
		W."STT",
		W."SortOrderDetail"
		;
		END IF
		;

		IF rec."LOAI_CHUNG_TU" = ANY ('{302,307,308,309,310,312,313,314,315,316,318,319,320,321,322,324,325,326,327,328,352,357,358,359,360,362,363,364,365,366,368,369,370,371,372,374,375,376,377,378}' :: INT [])-- 'PUVoucher'
		THEN
		INSERT INTO TMP_KET_QUA
		SELECT w.*
		FROM (
		SELECT
		BA."SO_TAI_KHOAN"
		, BAW."CHI_NHANH_TK_CHI"
		, BAW."NGAY_CHUNG_TU"
		, BAW."id"
		, 'purchase.document'                                                   AS "MODEL_CHUNG_TU"
		, CASE
		WHEN BAW."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
		THEN BAW."SO_UY_NHIEM_CHI"
		WHEN BAW."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
		THEN BAW."SO_SEC_CHUYEN_KHOAN"
		WHEN BAW."LOAI_THANH_TOAN" = 'sec_tien_mat'
		THEN BAW."SO_SEC_TIEN_MAT"
		ELSE
		BAW."SO_PHIEU_CHI"
		END                                                                   AS "SO_CHUNG_TU"

		, BAW."LOAI_CHUNG_TU"
		, CASE WHEN BAW."DIA_CHI" IS NOT NULL
		AND BAW."DIA_CHI" <> ''
		THEN BAW."DIA_CHI"
		ELSE res_partner."DIA_CHI"
		END                                                                   AS "DIA_CHI"
		, BAW."LY_DO_CHI"
		, (SELECT "MA_LOAI_TIEN"
		FROM res_currency T
		WHERE T.id =
		BAW."currency_id")                                             AS "LOAI_TIEN"
		, BAW."TY_GIA"
		, CASE WHEN BAW."TEN_DOI_TUONG" IS NOT NULL
		AND BAW."TEN_DOI_TUONG" <> ''
		THEN BAW."TEN_DOI_TUONG"
		ELSE res_partner."HO_VA_TEN"
		END                                                                   AS "TEN_KHACH_HANG"
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_doi_tuong_chi_tiet TK
		WHERE TK.id = BAW."TK_NHAN_ID")

		, BAW."CHI_NHANH_TK_NHAN"

		, (BAWD."THANH_TIEN" - BAWD."TIEN_CHIET_KHAU" + CASE WHEN "TK_THUE_GTGT_ID" IS NULL
		THEN BAWD."TIEN_THUE_GTGT"
									ELSE 0
									END)                    AS "THANH_TIEN"
		, (CASE WHEN BAWD."TK_XU_LY_CHENH_LECH"
		IS NOT NULL -- có chênh lệch tỷ giá
		AND PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY = 'BINH_QUAN_TUC_THOI'

		AND BAW."currency_id" <> LOAI_TIEN_CHINH  -- có hạch toán ngoại tệ
		AND (BAWD."THANH_TIEN_QUY_DOI" - BAWD."TIEN_CHIET_KHAU_QUY_DOI" +
		CASE WHEN "TK_THUE_GTGT_ID" IS NULL
		THEN BAWD."TIEN_THUE_GTGT_QUY_DOI"
		ELSE 0
		END) > (BAWD."THANH_TIEN_SAU_TY_GIA_XUAT_QUY"
		)
		THEN BAWD."THANH_TIEN_SAU_TY_GIA_XUAT_QUY"

		ELSE (BAWD."THANH_TIEN_QUY_DOI" - BAWD."TIEN_CHIET_KHAU_QUY_DOI" +
		CASE WHEN "TK_THUE_GTGT_ID" IS NULL
		THEN BAWD."TIEN_THUE_GTGT_QUY_DOI"
		ELSE 0
		END)
		END)                                                                 AS "SO_TIEN"
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_NO_ID")                                       AS "TK_NO"

		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_CO_ID")                                       AS "TK_CO"
		, LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_HANG_CHI_TIET(BAW."id",
													'112') AS "TK_CONG_NO"
		, BAWD."name"

		, R."MasterSortOrder"
		, BAWD."THU_TU_SAP_XEP_CHI_TIET"                                        AS "STT"
		, CAST(0 AS
		VARCHAR(127))                                                     AS "SortOrderDetail"

		FROM purchase_document BAW
		INNER JOIN TMP_ID_CHUNG_TU R ON BAW."id" = r."ID_CHUNG_TU"
		INNER JOIN purchase_document_line BAWD ON BAW."id" = BAWD."order_id"
		LEFT JOIN res_partner ON res_partner."id" = BAW."DOI_TUONG_ID"

		LEFT JOIN res_partner AS EM ON EM."id" = BAW."NHAN_VIEN_ID"

		LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = BAW."TK_CHI_ID"
		WHERE R."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
		R."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"

		UNION ALL
		--Add by Thidv: Lấy thêm dòng định khoản chênh lệch tỷ giá xuất quỹ
		SELECT
		BA."SO_TAI_KHOAN"
		, BAW."CHI_NHANH_TK_CHI"
		, BAW."NGAY_CHUNG_TU"
		, BAW."id"
		, 'purchase.document'                                                   AS "MODEL_CHUNG_TU"
		, CASE
		WHEN BAW."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
		THEN BAW."SO_UY_NHIEM_CHI"
		WHEN BAW."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
		THEN BAW."SO_SEC_CHUYEN_KHOAN"
		WHEN BAW."LOAI_THANH_TOAN" = 'sec_tien_mat'
		THEN BAW."SO_SEC_TIEN_MAT"
		ELSE
		BAW."SO_PHIEU_CHI"
		END                                                                   AS "SO_CHUNG_TU"
		, BAW."LOAI_CHUNG_TU"
		, CASE WHEN BAW."DIA_CHI" IS NOT NULL
		AND BAW."DIA_CHI" <> ''
		THEN BAW."DIA_CHI"
		ELSE res_partner."DIA_CHI"
		END                                                                   AS "DIA_CHI"
		, BAW."LY_DO_CHI"
		, (SELECT "MA_LOAI_TIEN"
		FROM res_currency T
		WHERE T.id =
		BAW."currency_id")                                             AS "LOAI_TIEN"
		, BAW."TY_GIA"
		, CASE WHEN BAW."TEN_DOI_TUONG" IS NOT NULL
		AND BAW."TEN_DOI_TUONG" <> ''
		THEN BAW."TEN_DOI_TUONG"
		ELSE res_partner."HO_VA_TEN"
		END                                                                   AS "TEN_KHACH_HANG"
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_doi_tuong_chi_tiet TK
		WHERE TK.id = BAW."TK_NHAN_ID")

		, BAW."CHI_NHANH_TK_NHAN"
		, --Tiền nguyên tệ =0
		CAST(0 AS
		DECIMAL(18, 4))                                                  AS "THANH_TIEN"
		, --Lấy tiền chênh lệch tỷ giá làm tiền quy đổi
		ABS(BAWD."CHENH_LECH")
															AS "SO_TIEN"
		, --Lỗ thì lấy TK 635 là TK Nợ, lãi thì lấy TK Nợ = TK Nợ
		(CASE WHEN BAWD."THANH_TIEN_QUY_DOI" < BAWD."THANH_TIEN_SAU_TY_GIA_XUAT_QUY"


		THEN (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_XU_LY_CHENH_LECH")

		ELSE (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_NO_ID")
		END)                                                                 AS "TK_NO"
		, --Lãi thì lấy TK 515 là TK có, lãi TK có = TK có
		(CASE WHEN BAWD."THANH_TIEN_QUY_DOI" < BAWD."THANH_TIEN_SAU_TY_GIA_XUAT_QUY"

		THEN (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_CO_ID")
		ELSE (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_XU_LY_CHENH_LECH")

		END)                                                                 AS "TK_CO"
		, LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_HANG_CHI_TIET(BAW."id",
													'112') AS "TK_CONG_NO"
		, DIEN_GIAI_TY_GIA_XUAT_QUY                                             AS "DIEN_GIAI"

		, R."MasterSortOrder"
		, BAWD."THU_TU_SAP_XEP_CHI_TIET"
		, CAST(1 AS VARCHAR(127))

		FROM purchase_document BAW
		INNER JOIN TMP_ID_CHUNG_TU R ON BAW."id" = r."ID_CHUNG_TU"
		INNER JOIN purchase_document_line BAWD ON BAW."id" = BAWD."order_id"
		LEFT JOIN res_partner ON res_partner."id" = BAW."DOI_TUONG_ID"

		LEFT JOIN res_partner AS EM ON EM."id" = BAW."NHAN_VIEN_ID"

		LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = BAW."TK_CHI_ID"
		WHERE (
		BAWD."TK_XU_LY_CHENH_LECH" IS NOT NULL
		)


		AND PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY = 'BINH_QUAN_TUC_THOI'

		AND BAW."currency_id" <>
		LOAI_TIEN_CHINH --Nếu không hạch toán ngoại tệ thì không in ra dòng xử lý chêch lệch(vì cũng có trường hợp VND mà giá trị ở cột CashOutDiff"TK_CONG_NO"Finance vẫn có. Xem funtiontest)
		AND R."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
		R."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"


		UNION ALL

		--Lấy dòng định khoản thuế của mua hàng
		SELECT
		BA."SO_TAI_KHOAN"
		, BAW."CHI_NHANH_TK_CHI"
		, BAW."NGAY_CHUNG_TU"
		, BAW."id"
		, 'purchase.document'                                                   AS "MODEL_CHUNG_TU"
		, CASE
		WHEN BAW."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
		THEN BAW."SO_UY_NHIEM_CHI"
		WHEN BAW."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
		THEN BAW."SO_SEC_CHUYEN_KHOAN"
		WHEN BAW."LOAI_THANH_TOAN" = 'sec_tien_mat'
		THEN BAW."SO_SEC_TIEN_MAT"
		ELSE
		BAW."SO_PHIEU_CHI"
		END                                                                   AS "SO_CHUNG_TU"
		, BAW."LOAI_CHUNG_TU"
		, CASE WHEN BAW."DIA_CHI" IS NOT NULL
		AND BAW."DIA_CHI" <> ''
		THEN BAW."DIA_CHI"
		ELSE res_partner."DIA_CHI"
		END                                                                   AS "DIA_CHI"
		, BAW."LY_DO_CHI"
		, (SELECT "MA_LOAI_TIEN"
		FROM res_currency T
		WHERE T.id =
		BAW."currency_id")                                             AS "LOAI_TIEN"
		, BAW."TY_GIA"
		, CASE WHEN BAW."TEN_DOI_TUONG" IS NOT NULL
		AND BAW."TEN_DOI_TUONG" <> ''
		THEN BAW."TEN_DOI_TUONG"
		ELSE res_partner."HO_VA_TEN"
		END                                                                   AS "TEN_KHACH_HANG"
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_doi_tuong_chi_tiet TK
		WHERE TK.id = BAW."TK_NHAN_ID")

		, BAW."CHI_NHANH_TK_NHAN"
		,
		--DVThi sửa lỗi: 114102 -Mua hàng\In giấy báo nợ mua hàng nhập khẩu TT ngay bằng ngoại tệ ngân hàng: Lỗi vẫn in ra tiền thuế GTGT nguyên tệ = (tiền hàng - chiết khấu) * thuế suất
		(CASE WHEN BAW."LOAI_CHUNG_TU" IN
		(318, 319, 320, 321, 322, 324, 325, 326, 327, 328, 368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
		THEN 0
		ELSE SUM(BAWD."TIEN_THUE_GTGT")
		END)
		, SUM((CASE WHEN BAWD."TK_XU_LY_CHENH_LECH"
		IS NOT NULL -- có chênh lệch tỷ giá
		AND PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY = 'BINH_QUAN_TUC_THOI'
		-- chỉ phương pháp tính giá bình quân tức thời mới in
		AND BAW."currency_id" <> LOAI_TIEN_CHINH  -- có hạch toán ngoại tệ
		AND BAWD."TIEN_THUE_GTGT_THEO_TGXQ"
		<> 0
		AND BAWD."TIEN_THUE_GTGT_QUY_DOI" > BAWD."TIEN_THUE_GTGT_THEO_TGXQ"

		THEN BAWD."TIEN_THUE_GTGT_THEO_TGXQ"

		ELSE BAWD."TIEN_THUE_GTGT_QUY_DOI"
		END))                                                            AS "SO_TIEN"
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_THUE_GTGT_ID")
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_CO_ID")
		, LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_HANG_CHI_TIET(BAW."id",
													'112') AS "TK_CONG_NO"
		, A."TEN_TAI_KHOAN"

		, R."MasterSortOrder"
		, 2000                                                                  AS "STT"

		, (CAST(BAWD."TK_THUE_GTGT_ID" AS VARCHAR) || CAST(20000 AS
									VARCHAR(5)))         AS "SortOrderDetail"

		FROM purchase_document BAW
		INNER JOIN TMP_ID_CHUNG_TU R ON BAW."id" = r."ID_CHUNG_TU"
		INNER JOIN purchase_document_line BAWD ON BAW."id" = BAWD."order_id"
		LEFT JOIN res_partner ON res_partner."id" = BAW."DOI_TUONG_ID"

		LEFT JOIN res_partner AS EM ON EM."id" = BAW."NHAN_VIEN_ID"

		LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = BAW."TK_CHI_ID"
		LEFT JOIN danh_muc_he_thong_tai_khoan A ON A."SO_TAI_KHOAN" = (SELECT "SO_TAI_KHOAN"
												FROM
													danh_muc_he_thong_tai_khoan TK
												WHERE TK.id =
														BAWD."TK_THUE_GTGT_ID")
		WHERE BAWD."TK_THUE_GTGT_ID" IS NOT NULL
		AND R."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
		R."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
		GROUP BY
		BA."SO_TAI_KHOAN"
		, BAW."CHI_NHANH_TK_CHI"
		, BAW."NGAY_CHUNG_TU"
		, BAW."id"
		, "MODEL_CHUNG_TU"
		, CASE
		WHEN BAW."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
		THEN BAW."SO_UY_NHIEM_CHI"
		WHEN BAW."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
		THEN BAW."SO_SEC_CHUYEN_KHOAN"
		WHEN BAW."LOAI_THANH_TOAN" = 'sec_tien_mat'
		THEN BAW."SO_SEC_TIEN_MAT"
		ELSE
		BAW."SO_PHIEU_CHI"
		END
		, BAW."LOAI_CHUNG_TU"
		, CASE WHEN BAW."DIA_CHI" IS NOT NULL
		AND BAW."DIA_CHI" <> ''
		THEN BAW."DIA_CHI"
		ELSE res_partner."DIA_CHI"
		END
		, BAW."LY_DO_CHI"
		, (SELECT "MA_LOAI_TIEN"
		FROM res_currency T
		WHERE T.id =
		BAW."currency_id")
		, BAW."TY_GIA"
		, CASE WHEN BAW."TEN_DOI_TUONG" IS NOT NULL
		AND BAW."TEN_DOI_TUONG" <> ''
		THEN BAW."TEN_DOI_TUONG"
		ELSE res_partner."HO_VA_TEN"
		END
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_doi_tuong_chi_tiet TK
		WHERE TK.id = BAW."TK_NHAN_ID")

		, BAW."CHI_NHANH_TK_NHAN"

		--DVThi sửa lỗi: 114102 -Mua hàng\In giấy báo nợ mua hàng nhập khẩu TT ngay bằng ngoại tệ ngân hàng: Lỗi vẫn in ra tiền thuế GTGT nguyên tệ = (tiền hàng - chiết khấu) * thuế suất

		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_THUE_GTGT_ID")
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_CO_ID")
		, LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_HANG_CHI_TIET(BAW."id",
													'112')
		, A."TEN_TAI_KHOAN"

		, R."MasterSortOrder"
		, BAWD."TK_THUE_GTGT_ID"
		HAVING SUM(BAWD."TIEN_THUE_GTGT") <> 0
		OR SUM(BAWD."TIEN_THUE_GTGT_QUY_DOI") <> 0


		UNION ALL
		SELECT
		BA."SO_TAI_KHOAN"
		, BAW."CHI_NHANH_TK_CHI"
		, BAW."NGAY_CHUNG_TU"
		, BAW."id"
		, 'purchase.document'                                                   AS "MODEL_CHUNG_TU"
		, CASE
		WHEN BAW."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
		THEN BAW."SO_UY_NHIEM_CHI"
		WHEN BAW."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
		THEN BAW."SO_SEC_CHUYEN_KHOAN"
		WHEN BAW."LOAI_THANH_TOAN" = 'sec_tien_mat'
		THEN BAW."SO_SEC_TIEN_MAT"
		ELSE
		BAW."SO_PHIEU_CHI"
		END                                                                   AS "SO_CHUNG_TU"
		, BAW."LOAI_CHUNG_TU"
		, CASE WHEN BAW."DIA_CHI" IS NOT NULL
		AND BAW."DIA_CHI" <> ''
		THEN BAW."DIA_CHI"
		ELSE res_partner."DIA_CHI"
		END                                                                   AS "DIA_CHI"
		, BAW."LY_DO_CHI"
		, (SELECT "MA_LOAI_TIEN"
		FROM res_currency T
		WHERE T.id =
		BAW."currency_id")
		, BAW."TY_GIA"
		, CASE WHEN BAW."TEN_DOI_TUONG" IS NOT NULL
		AND BAW."TEN_DOI_TUONG" <> ''
		THEN BAW."TEN_DOI_TUONG"
		ELSE res_partner."HO_VA_TEN"
		END                                                                   AS "TEN_KHACH_HANG"
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_doi_tuong_chi_tiet TK
		WHERE TK.id = BAW."TK_NHAN_ID")

		, BAW."CHI_NHANH_TK_NHAN"

		, --Tiền nguyên tệ =0
		CAST(0 AS
		DECIMAL(18, 4))                                                  AS "THANH_TIEN"
		,
		--Modify by thidv: Lấy số tiền quy đổi = min(của cột thành tiền và cột quy đổi theo tỷ giá xuất quỹ)
		--Lấy tiền chênh lệch tỷ giá làm tiền quy đổi
		SUM(ABS(BAWD."CHENH_LECH_TIEN_THUE_GTGT")
		)                                                                     AS "SO_TIEN"
		, --Lỗ thì lấy TK 635 là TK Nợ, lãi thì lấy "TK_THUE_GTGT" = TK Nợ
		(CASE WHEN (BAW."TY_GIA" < BAWD."TY_GIA_XUAT_QUY")

		THEN (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_XU_LY_CHENH_LECH")

		ELSE (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_THUE_GTGT_ID")
		END)                                                                 AS "TK_NO"
		, --Lãi thì lấy TK 515 là TK có, lãi TK có = TK có
		(CASE WHEN (BAW."TY_GIA" < BAWD."TY_GIA_XUAT_QUY")

		THEN (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_CO_ID")
		ELSE (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_XU_LY_CHENH_LECH")

		END)                                                                 AS "TK_CO"
		, LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_HANG_CHI_TIET(BAW."id",
													'112') AS "TK_CONG_NO"
		, DIEN_GIAI_TY_GIA_XUAT_QUY                                             AS "DIEN_GIAI"

		, R."MasterSortOrder"
		, 2000                                                                  AS "STT"
		, (CAST(BAWD."TK_THUE_GTGT_ID" AS VARCHAR) || CAST(20001 AS
									VARCHAR(5)))         AS "SortOrderDetail"


		FROM purchase_document BAW
		INNER JOIN TMP_ID_CHUNG_TU R ON BAW."id" = r."ID_CHUNG_TU"
		INNER JOIN purchase_document_line BAWD ON BAW."id" = BAWD."order_id"
		LEFT JOIN res_partner ON res_partner."id" = BAW."DOI_TUONG_ID"

		LEFT JOIN res_partner AS EM ON EM."id" = BAW."NHAN_VIEN_ID"

		LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = BAW."TK_CHI_ID"
		LEFT JOIN danh_muc_he_thong_tai_khoan A ON A."SO_TAI_KHOAN" = (SELECT "SO_TAI_KHOAN"
												FROM
													danh_muc_he_thong_tai_khoan TK
												WHERE TK.id =
														BAWD."TK_THUE_GTGT_ID")
		WHERE BAWD."TK_THUE_GTGT_ID" IS NOT NULL
		AND (BAWD."TK_XU_LY_CHENH_LECH" IS NOT NULL
		)

		-- có chênh lệch tỷ giá
		AND PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY = 'BINH_QUAN_TUC_THOI'
		-- chỉ phương pháp tính giá bình quân tức thời mới in
		AND BAW."currency_id" <> LOAI_TIEN_CHINH
		--Nếu không hạch toán ngoại tệ thì không in ra dòng xử lý chêch lệch(vì cũng có trường hợp VND mà giá trị ở cột CashOutDiff"TK_CONG_NO"Finance vẫn có. Xem funtiontest)
		AND (BAWD."CHENH_LECH_TIEN_THUE_GTGT" <> 0
		)
		AND R."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
		R."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"


		GROUP BY
		BA."SO_TAI_KHOAN"
		, BAW."CHI_NHANH_TK_CHI"
		, BAW."NGAY_CHUNG_TU"
		, BAW."id"
		, "MODEL_CHUNG_TU"
		, CASE
		WHEN BAW."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
		THEN BAW."SO_UY_NHIEM_CHI"
		WHEN BAW."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
		THEN BAW."SO_SEC_CHUYEN_KHOAN"
		WHEN BAW."LOAI_THANH_TOAN" = 'sec_tien_mat'
		THEN BAW."SO_SEC_TIEN_MAT"
		ELSE
		BAW."SO_PHIEU_CHI"
		END
		, BAW."LOAI_CHUNG_TU"
		, CASE WHEN BAW."DIA_CHI" IS NOT NULL
		AND BAW."DIA_CHI" <> ''
		THEN BAW."DIA_CHI"
		ELSE res_partner."DIA_CHI"
		END
		, BAW."LY_DO_CHI"
		, (SELECT "MA_LOAI_TIEN"
		FROM res_currency T
		WHERE T.id =
		BAW."currency_id")
		, BAW."TY_GIA"
		, CASE WHEN BAW."TEN_DOI_TUONG" IS NOT NULL
		AND BAW."TEN_DOI_TUONG" <> ''
		THEN BAW."TEN_DOI_TUONG"
		ELSE res_partner."HO_VA_TEN"
		END
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_doi_tuong_chi_tiet TK
		WHERE TK.id = BAW."TK_NHAN_ID")

		, BAW."CHI_NHANH_TK_NHAN"

		, BAWD."TK_THUE_GTGT_ID"

		, LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_HANG_CHI_TIET(BAW."id",
													'112')
		, A."TEN_TAI_KHOAN"

		, R."MasterSortOrder"
		, (CASE WHEN (BAW."TY_GIA" < BAWD."TY_GIA_XUAT_QUY")

		THEN (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_XU_LY_CHENH_LECH")

		ELSE (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_THUE_GTGT_ID")
		END)
		, --Lãi thì lấy TK 515 là TK có, lãi TK có = TK có
		(CASE WHEN (BAW."TY_GIA" < BAWD."TY_GIA_XUAT_QUY")

		THEN (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_CO_ID")
		ELSE (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_XU_LY_CHENH_LECH")

		END)

		HAVING SUM(BAWD."TIEN_THUE_GTGT") <> 0
		OR SUM(BAWD."TIEN_THUE_GTGT_QUY_DOI") <> 0
		) W
		ORDER BY
		W."MasterSortOrder",
		W."STT",
		W."SortOrderDetail"
		;
		END IF
		;


		IF rec."LOAI_CHUNG_TU" = ANY ('{330,331,332,333,334}' :: INT [])--  'PUService'
		THEN
		INSERT INTO TMP_KET_QUA
		SELECT w.*
		FROM (SELECT
		BA."SO_TAI_KHOAN"
		, BAW."CHI_NHANH_TK_CHI"
		, BAW."NGAY_CHUNG_TU"
		, BAW."id"
		, 'purchase.document'                                                            AS "MODEL_CHUNG_TU"
		, BAW."SO_CHUNG_TU"
		, BAW."LOAI_CHUNG_TU"
		, CASE WHEN BAW."DIA_CHI" IS NOT NULL
		AND BAW."DIA_CHI" <> ''
		THEN BAW."DIA_CHI"
		ELSE res_partner."DIA_CHI"
		END                                                                            AS "DIA_CHI"
		, BAW."DIEN_GIAI_CHUNG"
		, (SELECT "MA_LOAI_TIEN"
		FROM res_currency T
		WHERE T.id =
		BAW."currency_id")
		, BAW."TY_GIA"
		, CASE WHEN BAW."TEN_DOI_TUONG" IS NOT NULL
		AND BAW."TEN_DOI_TUONG" <> ''
		THEN BAW."TEN_DOI_TUONG"
		ELSE res_partner."HO_VA_TEN"
		END                                                                            AS "TEN_KHACH_HANG"
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_doi_tuong_chi_tiet TK
		WHERE TK.id = BAW."TK_NHAN_ID")

		, BAW."CHI_NHANH_TK_NHAN"
		, BAWD."THANH_TIEN"
		,
		--Modify by thidv: Lấy số tiền quy đổi = min(của cột thành tiền và cột quy đổi theo tỷ giá xuất quỹ)
		(CASE WHEN BAWD."TK_THUE_GTGT_ID"
		IS NOT NULL -- có chênh lệch tỷ giá
		AND PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY = 'BINH_QUAN_TUC_THOI'
		-- chỉ phương pháp tính giá bình quân tức thời mới in
		AND BAW."currency_id" <> LOAI_TIEN_CHINH  -- có hạch toán ngoại tệ
		AND BAWD."THANH_TIEN_QUY_DOI" > BAWD."THANH_TIEN_SAU_TY_GIA_XUAT_QUY"

		THEN BAWD."THANH_TIEN_SAU_TY_GIA_XUAT_QUY"

		ELSE BAWD."THANH_TIEN_QUY_DOI"
		END)                                                                          AS "SO_TIEN"

		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_NO_ID")
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_CO_ID")
		, LAY_TAI_KHOAN_TONG_HOP_CHUNG_TREN_SEC_UY_NHIEM_CHI_MUA_DICH_VU_CHI_TIET(BAW."id",
														'112') AS "TK_CONG_NO"
		, BAWD."name"

		, R."MasterSortOrder"
		, BAWD."THU_TU_SAP_XEP_CHI_TIET"                                                 AS "STT"
		, CAST(0 AS
		VARCHAR(127))                                                              AS "SortOrderDetail"

		FROM purchase_document BAW
		INNER JOIN TMP_ID_CHUNG_TU R ON BAW."id" = r."ID_CHUNG_TU"
		INNER JOIN purchase_document_line BAWD ON BAW."id" = BAWD."order_id"
		LEFT JOIN res_partner ON res_partner."id" = BAW."DOI_TUONG_ID"

		LEFT JOIN res_partner AS EM ON EM."id" = BAW."NHAN_VIEN_ID"

		LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = BAW."TK_CHI_ID"
		WHERE R."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
		R."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
		UNION ALL
		--Add by Thidv: Lấy thêm dòng định khoản chênh lệch tỷ giá xuất quỹ
		SELECT
		BA."SO_TAI_KHOAN"
		, BAW."CHI_NHANH_TK_CHI"
		, BAW."NGAY_CHUNG_TU"
		, BAW."id"
		, 'purchase.document'                                                            AS "MODEL_CHUNG_TU"
		, BAW."SO_CHUNG_TU"
		, BAW."LOAI_CHUNG_TU"
		, CASE WHEN BAW."DIA_CHI" IS NOT NULL
		AND BAW."DIA_CHI" <> ''
		THEN BAW."DIA_CHI"
		ELSE res_partner."DIA_CHI"
		END                                                                            AS "DIA_CHI"
		, BAW."DIEN_GIAI_CHUNG"
		, (SELECT "MA_LOAI_TIEN"
		FROM res_currency T
		WHERE T.id =
		BAW."currency_id")
		, BAW."TY_GIA"
		, CASE WHEN BAW."TEN_DOI_TUONG" IS NOT NULL
		AND BAW."TEN_DOI_TUONG" <> ''
		THEN BAW."TEN_DOI_TUONG"
		ELSE res_partner."HO_VA_TEN"
		END                                                                            AS "TEN_KHACH_HANG"
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_doi_tuong_chi_tiet TK
		WHERE TK.id = BAW."TK_NHAN_ID")

		, BAW."CHI_NHANH_TK_NHAN"
		, --Tiền nguyên tệ =0
		CAST(0 AS
		DECIMAL(18, 4))                                                           AS "THANH_TIEN"
		, --Lấy tiền chênh lệch tỷ giá làm tiền quy đổi
		ABS(BAWD."CHENH_LECH")
																AS "SO_TIEN"
		, --Lỗ thì lấy TK 635 là TK Nợ, lãi thì lấy TK Nợ = TK Nợ
		(CASE WHEN BAWD."THANH_TIEN_QUY_DOI" < BAWD."THANH_TIEN_SAU_TY_GIA_XUAT_QUY"

		THEN (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_THUE_GTGT_ID")

		ELSE (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_NO_ID")
		END)                                                                          AS "TK_NO"
		, --Lãi thì lấy TK 515 là TK có, lãi TK có = TK có
		(CASE WHEN BAWD."THANH_TIEN_QUY_DOI" < BAWD."THANH_TIEN_SAU_TY_GIA_XUAT_QUY"

		THEN (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_CO_ID")
		ELSE (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_THUE_GTGT_ID")

		END)                                                                          AS "TK_CO"
		, LAY_TAI_KHOAN_TONG_HOP_CHUNG_TREN_SEC_UY_NHIEM_CHI_MUA_DICH_VU_CHI_TIET(BAW."id",
														'112') AS "TK_CONG_NO"
		,
		DIEN_GIAI_TY_GIA_XUAT_QUY                                                      AS "DIEN_GIAI"

		, R."MasterSortOrder"
		, BAWD."THU_TU_SAP_XEP_CHI_TIET"                                                 AS "STT"
		, CAST(1 AS
		VARCHAR(127))                                                              AS "SortOrderDetail"

		FROM purchase_document BAW
		INNER JOIN TMP_ID_CHUNG_TU R ON BAW."id" = r."ID_CHUNG_TU"
		INNER JOIN purchase_document_line BAWD ON BAW."id" = BAWD."order_id"
		LEFT JOIN res_partner ON res_partner."id" = BAW."DOI_TUONG_ID"

		LEFT JOIN res_partner AS EM ON EM."id" = BAW."NHAN_VIEN_ID"

		LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = BAW."TK_CHI_ID"
		WHERE (
		BAWD."TK_THUE_GTGT_ID" IS NOT NULL
		)


		AND PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY = 'BINH_QUAN_TUC_THOI'
		-- chỉ phương pháp tính giá bình quân tức thời mới in
		AND BAW."currency_id" <>
		LOAI_TIEN_CHINH --Nếu không hạch toán ngoại tệ thì không in ra dòng xử lý chêch lệch(vì cũng có trường hợp VND mà giá trị ở cột CashOutDiff"TK_CONG_NO"Finance vẫn có. Xem funtiontest)

		AND R."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
		R."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"

		UNION ALL

		--Lấy hạch toán thuế khấu trừ
		SELECT
		BA."SO_TAI_KHOAN"
		, BAW."CHI_NHANH_TK_CHI"
		, BAW."NGAY_CHUNG_TU"
		, BAW."id"
		, 'purchase.document'                                                            AS "MODEL_CHUNG_TU"
		, BAW."SO_CHUNG_TU"
		, BAW."LOAI_CHUNG_TU"
		, CASE WHEN BAW."DIA_CHI" IS NOT NULL
		AND BAW."DIA_CHI" <> ''
		THEN BAW."DIA_CHI"
		ELSE res_partner."DIA_CHI"
		END                                                                            AS "DIA_CHI"
		, BAW."DIEN_GIAI_CHUNG"
		, (SELECT "MA_LOAI_TIEN"
		FROM res_currency T
		WHERE T.id =
		BAW."currency_id")
		, BAW."TY_GIA"
		, CASE WHEN BAW."TEN_DOI_TUONG" IS NOT NULL
		AND BAW."TEN_DOI_TUONG" <> ''
		THEN BAW."TEN_DOI_TUONG"
		ELSE res_partner."HO_VA_TEN"
		END                                                                            AS "TEN_KHACH_HANG"

		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_doi_tuong_chi_tiet TK
		WHERE TK.id = BAW."TK_NHAN_ID")

		, BAW."CHI_NHANH_TK_NHAN"
		, SUM(
		BAWD."TIEN_THUE_GTGT")                                                     AS "THANH_TIEN"
		,
		--Modify by thidv: Lấy số tiền quy đổi = min(của cột thành tiền và cột quy đổi theo tỷ giá xuất quỹ)
		SUM((CASE WHEN (BAWD."TK_THUE_GTGT_ID"
		IS NOT NULL -- có chênh lệch tỷ giá
		AND PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY = 'BINH_QUAN_TUC_THOI'
		-- chỉ phương pháp tính giá bình quân tức thời mới in
		AND BAW."currency_id" <> LOAI_TIEN_CHINH  -- có hạch toán ngoại tệ
		AND BAWD."TIEN_THUE_GTGT_QUY_DOI" > BAWD."TIEN_THUE_GTGT_THEO_TGXQ")

		THEN (BAWD."TIEN_THUE_GTGT_THEO_TGXQ"
		)
		ELSE BAWD."TIEN_THUE_GTGT_QUY_DOI"
		END))                                                                     AS "SO_TIEN"
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_THUE_GTGT_ID")                                         AS "TK_NO"
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_CO_ID")
		, LAY_TAI_KHOAN_TONG_HOP_CHUNG_TREN_SEC_UY_NHIEM_CHI_MUA_DICH_VU_CHI_TIET(BAW."id",
														'112') AS "TK_CONG_NO"
		,
		A."TEN_TAI_KHOAN"                                                              AS "DIEN_GIAI"

		, R."MasterSortOrder"
		, 20000                                                                          AS "STT"

		, (CAST(BAWD."TK_THUE_GTGT_ID" AS VARCHAR) || CAST(20000 AS
									VARCHAR(5)))                  AS "SortOrderDetail"

		FROM purchase_document BAW
		INNER JOIN TMP_ID_CHUNG_TU R ON BAW."id" = r."ID_CHUNG_TU"
		INNER JOIN purchase_document_line BAWD ON BAW."id" = BAWD."order_id"
		LEFT JOIN res_partner ON res_partner."id" = BAW."DOI_TUONG_ID"

		LEFT JOIN res_partner AS EM ON EM."id" = BAW."NHAN_VIEN_ID"

		LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = BAW."TK_CHI_ID"
		LEFT JOIN danh_muc_he_thong_tai_khoan A ON A."SO_TAI_KHOAN" = (SELECT "SO_TAI_KHOAN"
												FROM
													danh_muc_he_thong_tai_khoan TK
												WHERE TK.id =
													BAWD."TK_THUE_GTGT_ID")
		WHERE BAWD."TK_THUE_GTGT_ID" IS NOT NULL
		AND R."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
		R."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
		GROUP BY
		BA."SO_TAI_KHOAN"
		, BAW."CHI_NHANH_TK_CHI"
		, BAW."NGAY_CHUNG_TU"
		, BAW."id"
		, "MODEL_CHUNG_TU"
		, BAW."SO_CHUNG_TU"
		, BAW."LOAI_CHUNG_TU"
		, CASE WHEN BAW."DIA_CHI" IS NOT NULL
		AND BAW."DIA_CHI" <> ''
		THEN BAW."DIA_CHI"
		ELSE res_partner."DIA_CHI"
		END
		, BAW."DIEN_GIAI_CHUNG"
		, (SELECT "MA_LOAI_TIEN"
		FROM res_currency T
		WHERE T.id =
		BAW."currency_id")
		, BAW."TY_GIA"
		, CASE WHEN BAW."TEN_DOI_TUONG" IS NOT NULL
		AND BAW."TEN_DOI_TUONG" <> ''
		THEN BAW."TEN_DOI_TUONG"
		ELSE res_partner."HO_VA_TEN"
		END

		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_doi_tuong_chi_tiet TK
		WHERE TK.id = BAW."TK_NHAN_ID")

		, BAW."CHI_NHANH_TK_NHAN"

		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_THUE_GTGT_ID")
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_CO_ID")
		, LAY_TAI_KHOAN_TONG_HOP_CHUNG_TREN_SEC_UY_NHIEM_CHI_MUA_DICH_VU_CHI_TIET(BAW."id",
														'112')
		,
		A."TEN_TAI_KHOAN"

		, R."MasterSortOrder"
		, BAWD."TK_THUE_GTGT_ID"


		HAVING SUM(BAWD."TIEN_THUE_GTGT") <> 0
		OR SUM(BAWD."TIEN_THUE_GTGT_QUY_DOI") <> 0
		UNION ALL
		--Add by Thidv: Lấy thêm dòng định khoản chênh lệch tỷ giá xuất quỹ cho thuế khấu trừ
		SELECT
		BA."SO_TAI_KHOAN"
		, BAW."CHI_NHANH_TK_CHI"
		, BAW."NGAY_CHUNG_TU"
		, BAW."id"
		, 'purchase.document'                                                            AS "MODEL_CHUNG_TU"
		, BAW."SO_CHUNG_TU"
		, BAW."LOAI_CHUNG_TU"
		, (CASE WHEN BAW."DIA_CHI" IS NOT NULL
		AND BAW."DIA_CHI" <> ''
		THEN BAW."DIA_CHI"
		ELSE res_partner."DIA_CHI"
		END)                                                                          AS "DIA_CHI"
		, BAW."DIEN_GIAI_CHUNG"
		, (SELECT "MA_LOAI_TIEN"
		FROM res_currency T
		WHERE T.id =
		BAW."currency_id")
		, BAW."TY_GIA"
		, CASE WHEN BAW."TEN_DOI_TUONG" IS NOT NULL
		AND BAW."TEN_DOI_TUONG" <> ''
		THEN BAW."TEN_DOI_TUONG"
		ELSE res_partner."HO_VA_TEN"
		END                                                                            AS "TEN_KHACH_HANG"
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_doi_tuong_chi_tiet TK
		WHERE TK.id = BAW."TK_NHAN_ID")

		, BAW."CHI_NHANH_TK_NHAN"
		, --Tiền nguyên tệ =0
		CAST(0 AS
		DECIMAL(18, 4))                                                           AS "THANH_TIEN"
		, --Lấy tiền chênh lệch tỷ giá làm tiền quy đổi
		SUM((ABS(BAWD."CHENH_LECH_TIEN_THUE_GTGT")
		))                                                                         AS "SO_TIEN"
		, --Lỗ thì lấy TK 635 là TK Nợ, lãi thì lấy "TK_THUE_GTGT" = TK Nợ
		(CASE WHEN BAW."TY_GIA" < (BAWD."TY_GIA_XUAT_QUY"
		)
		THEN (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_XU_LY_CHENH_LECH")

		ELSE (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_THUE_GTGT_ID")
		END)                                                                          AS "TK_NO"
		, --Lãi thì lấy TK 515 là TK có, lãi TK có = TK có
		(CASE WHEN BAW."TY_GIA" < (BAWD."TY_GIA_XUAT_QUY"
		)
		THEN (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_CO_ID")
		ELSE (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_XU_LY_CHENH_LECH")
		END)                                                                          AS "TK_CO"
		, LAY_TAI_KHOAN_TONG_HOP_CHUNG_TREN_SEC_UY_NHIEM_CHI_MUA_DICH_VU_CHI_TIET(BAW."id",
														'112') AS "TK_CONG_NO"
		,
		DIEN_GIAI_TY_GIA_XUAT_QUY                                                      AS "DIEN_GIAI"

		, R."MasterSortOrder"
		, 20000                                                                          AS "STT"

		, (CAST(BAWD."TK_THUE_GTGT_ID" AS VARCHAR) || CAST(20001 AS
									VARCHAR(5)))                  AS "SortOrderDetail"


		FROM purchase_document BAW
		INNER JOIN TMP_ID_CHUNG_TU R ON BAW."id" = r."ID_CHUNG_TU"
		INNER JOIN purchase_document_line BAWD ON BAW."id" = BAWD."order_id"
		LEFT JOIN res_partner ON res_partner."id" = BAW."DOI_TUONG_ID"

		LEFT JOIN res_partner AS EM ON EM."id" = BAW."NHAN_VIEN_ID"

		LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = BAW."TK_CHI_ID"
		LEFT JOIN danh_muc_he_thong_tai_khoan A ON A."SO_TAI_KHOAN" = (SELECT "SO_TAI_KHOAN"
												FROM
													danh_muc_he_thong_tai_khoan TK
												WHERE TK.id =
													BAWD."TK_THUE_GTGT_ID")
		WHERE BAWD."TK_THUE_GTGT_ID" IS NOT NULL
		AND (BAWD."TK_THUE_GTGT_ID" IS NOT NULL
		)


		-- có chênh lệch tỷ giá
		AND PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY = 'BINH_QUAN_TUC_THOI'
		-- chỉ phương pháp tính giá bình quân tức thời mới in
		AND BAW."currency_id" <>
		LOAI_TIEN_CHINH --Nếu không hạch toán ngoại tệ thì không in ra dòng xử lý chêch lệch(vì cũng có trường hợp VND mà giá trị ở cột CashOutDiff"TK_CONG_NO"Finance vẫn có. Xem funtiontest)
		AND R."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
		R."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
		GROUP BY
		BA."SO_TAI_KHOAN"
		, BAW."CHI_NHANH_TK_CHI"
		, BAW."NGAY_CHUNG_TU"
		, BAW."id"
		, "MODEL_CHUNG_TU"
		, BAW."SO_CHUNG_TU"
		, BAW."LOAI_CHUNG_TU"
		, (CASE WHEN BAW."DIA_CHI" IS NOT NULL
		AND BAW."DIA_CHI" <> ''
		THEN BAW."DIA_CHI"
		ELSE res_partner."DIA_CHI"
		END)
		, BAW."DIEN_GIAI_CHUNG"
		, (SELECT "MA_LOAI_TIEN"
		FROM res_currency T
		WHERE T.id =
		BAW."currency_id")
		, BAW."TY_GIA"
		, CASE WHEN BAW."TEN_DOI_TUONG" IS NOT NULL
		AND BAW."TEN_DOI_TUONG" <> ''
		THEN BAW."TEN_DOI_TUONG"
		ELSE res_partner."HO_VA_TEN"
		END
		, (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_doi_tuong_chi_tiet TK
		WHERE TK.id = BAW."TK_NHAN_ID")

		, BAW."CHI_NHANH_TK_NHAN"

		, --Lỗ thì lấy TK 635 là TK Nợ, lãi thì lấy "TK_THUE_GTGT" = TK Nợ
		(CASE WHEN BAW."TY_GIA" < (BAWD."TY_GIA_XUAT_QUY"
		)
		THEN (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_XU_LY_CHENH_LECH")

		ELSE (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_THUE_GTGT_ID")
		END)
		, --Lãi thì lấy TK 515 là TK có, lãi TK có = TK có
		(CASE WHEN BAW."TY_GIA" < (BAWD."TY_GIA_XUAT_QUY"
		)
		THEN (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_CO_ID")
		ELSE (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_XU_LY_CHENH_LECH")
		END)
		, LAY_TAI_KHOAN_TONG_HOP_CHUNG_TREN_SEC_UY_NHIEM_CHI_MUA_DICH_VU_CHI_TIET(BAW."id",
														'112')
		, DIEN_GIAI_TY_GIA_XUAT_QUY

		, R."MasterSortOrder"
		, A."TEN_TAI_KHOAN"
		, BAWD."TK_THUE_GTGT_ID"


		HAVING SUM(BAWD."TIEN_THUE_GTGT") <> 0
		OR SUM(BAWD."TIEN_THUE_GTGT_QUY_DOI") <> 0
		) W
		ORDER BY
		w."MasterSortOrder",
		W."STT",
		W."SortOrderDetail"

		;
		END IF
		;


		IF rec."LOAI_CHUNG_TU" = ANY ('{1560}' :: INT [])-- 'BAInternalTransfer'
		THEN
		INSERT INTO TMP_KET_QUA
		SELECT w.*
		FROM (SELECT
		BA."SO_TAI_KHOAN"
		, CASE WHEN BAW."TEN_TK_CHI" IS NULL
		OR BAW."TEN_TK_CHI" = ''
		THEN B1."TEN_DAY_DU"
		ELSE BAW."TEN_TK_CHI"
		END

		, BAW."NGAY_CHUNG_TU"
		, BAW."id"
		, 'account.ex.phieu.thu.chi'                             AS "MODEL_CHUNG_TU"
		, BAW."SO_CHUNG_TU"                                      AS "SO_CHUNG_TU"
		, 150                                                    AS "LOAI_CHUNG_TU"
		, ''                                                     AS "DIA_CHI"
		, BAW."DIEN_GIAI"
		, (SELECT "MA_LOAI_TIEN"
		FROM res_currency T
		WHERE T.id =
		BAW."currency_id")
		, BAW."TY_GIA"
		, ''                                                     AS "TEN_KHACH_HANG"
		, BA2."SO_TAI_KHOAN"

		, CASE WHEN Baw."TEN_TK_NHAN_CTNB" IS NULL
		OR Baw."TEN_TK_NHAN_CTNB" = ''
		THEN B2."TEN_DAY_DU"
		ELSE Baw."TEN_TK_NHAN_CTNB"
		END

		, BAWD."SO_TIEN"
		,
		--Modify by thidv: Lấy số tiền quy đổi = min(của cột thành tiền và cột quy đổi theo tỷ giá xuất quỹ)
		(CASE WHEN BAWD."TK_XU_LY_CHENH_LECH"
		IS NOT NULL -- có chênh lệch tỷ giá
		AND PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY = 'BINH_QUAN_TUC_THOI'
		-- chỉ phương pháp tính giá bình quân tức thời mới in
		AND BAW."currency_id" <> LOAI_TIEN_CHINH  -- có hạch toán ngoại tệ
		AND BAWD."SO_TIEN_QUY_DOI" > BAWD."QUY_DOI_THEO_TGXQ"

		THEN BAWD."QUY_DOI_THEO_TGXQ"

		ELSE BAWD."SO_TIEN_QUY_DOI"
		END)                                                  AS "SO_TIEN"
		,  (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_NO_ID")
		,(SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_CO_ID")
		, LAY_TAI_KHOAN_TONG_HOP_CHUNG_CHUYEN_TIEN_NOI_BO(BAW."id",
								'112') AS "TK_CONG_NO"
		, BAWD."DIEN_GIAI_DETAIL"


		, R."MasterSortOrder"
		, BAWD."THU_TU_SAP_XEP_CHI_TIET"  AS "STT"
		, CAST(0 AS
		VARCHAR(127))                       AS "SortOrderDetail"

		FROM account_ex_phieu_thu_chi BAW
		INNER JOIN TMP_ID_CHUNG_TU R ON BAW."id" = r."ID_CHUNG_TU"
		INNER JOIN account_ex_phieu_thu_chi_tiet BAWD ON BAW."id" = BAWD."PHIEU_THU_CHI_ID"

		LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = BAW."TAI_KHOAN_CHI_GUI_ID"
		LEFT JOIN danh_muc_ngan_hang B1 ON B1."id" = BA."NGAN_HANG_ID"
		LEFT JOIN danh_muc_tai_khoan_ngan_hang BA2 ON BA2."id" = BAW."TAI_KHOAN_DEN_ID"
		LEFT JOIN danh_muc_ngan_hang B2 ON B2."id" = BA2."NGAN_HANG_ID"
		WHERE R."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
		R."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"

		UNION ALL --Add by Thidv: Lấy thêm dòng định khoản chênh lệch tỷ giá xuất quỹ
		SELECT
		BA."SO_TAI_KHOAN"
		, CASE WHEN BAW."TEN_TK_CHI" IS NULL
		OR BAW."TEN_TK_CHI" = ''
		THEN B1."TEN_DAY_DU"
		ELSE BAW."TEN_TK_CHI"
		END

		, BAW."NGAY_CHUNG_TU"
		, BAW."id"
		, 'account.ex.phieu.thu.chi'                             AS "MODEL_CHUNG_TU"
		, BAW."SO_CHUNG_TU"                                      AS "SO_CHUNG_TU"
		, 150                                                    AS "LOAI_CHUNG_TU"
		, ''                                                     AS "DIA_CHI"
		, BAW."DIEN_GIAI"
		, (SELECT "MA_LOAI_TIEN"
		FROM res_currency T
		WHERE T.id =
		BAW."currency_id")
		, BAW."TY_GIA"
		, ''                                                     AS "TEN_KHACH_HANG"
		, BA2."SO_TAI_KHOAN"

		, CASE WHEN Baw."TEN_TK_NHAN_CTNB" IS NULL
		OR Baw."TEN_TK_NHAN_CTNB" = ''
		THEN B2."TEN_DAY_DU"
		ELSE Baw."TEN_TK_NHAN_CTNB"
		END
		, --Tiền nguyên tệ =0
		CAST(0 AS
		DECIMAL(18, 4))                                   AS "THANH_TIEN"
		, --Lấy tiền chênh lệch tỷ giá làm tiền quy đổi
		ABS(BAWD."CHENH_LECH")
								AS "SO_TIEN"
		, --Lỗ thì lấy TK 635 là TK Nợ, lãi thì lấy TK Nợ = TK Nợ
		(CASE WHEN BAWD."SO_TIEN_QUY_DOI" <  BAWD."QUY_DOI_THEO_TGXQ"

		THEN   (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id =  BAWD."TK_XU_LY_CHENH_LECH")

		ELSE (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_NO_ID")
		END)                                                  AS "TK_NO"
		, --Lãi thì lấy TK 515 là TK có, lãi TK có = TK có
		(CASE WHEN BAWD."SO_TIEN_QUY_DOI" <  BAWD."QUY_DOI_THEO_TGXQ"

		THEN  (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id = BAWD."TK_CO_ID")
		ELSE   (SELECT "SO_TAI_KHOAN"
		FROM danh_muc_he_thong_tai_khoan TK
		WHERE TK.id =  BAWD."TK_XU_LY_CHENH_LECH")

		END)                                                  AS "TK_CO"
		, LAY_TAI_KHOAN_TONG_HOP_CHUNG_CHUYEN_TIEN_NOI_BO(BAW."id",
								'112') AS "TK_CONG_NO"
		, DIEN_GIAI_TY_GIA_XUAT_QUY                        AS "DIEN_GIAI"

		, R."MasterSortOrder"
		, BAWD."THU_TU_SAP_XEP_CHI_TIET" AS "STT"
		, CAST(1 AS
		VARCHAR(127))                                   AS "SortOrderDetail"

		FROM account_ex_phieu_thu_chi BAW
		INNER JOIN TMP_ID_CHUNG_TU R ON BAW."id" = r."ID_CHUNG_TU"
		INNER JOIN account_ex_phieu_thu_chi_tiet BAWD ON BAW."id" = BAWD."PHIEU_THU_CHI_ID"

		LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = BAW."TAI_KHOAN_CHI_GUI_ID"
		LEFT JOIN danh_muc_ngan_hang B1 ON B1."id" = BA."NGAN_HANG_ID"
		LEFT JOIN danh_muc_tai_khoan_ngan_hang BA2 ON BA2."id" = BAW."TAI_KHOAN_DEN_ID"
		LEFT JOIN danh_muc_ngan_hang B2 ON B2."id" = BA2."NGAN_HANG_ID"
		WHERE ((
		BAWD."TK_XU_LY_CHENH_LECH" IS NOT NULL
		)

		) -- có chênh lệch tỷ giá
		AND PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY = 'BINH_QUAN_TUC_THOI'
		-- chỉ phương pháp tính giá bình quân tức thời mới in
		AND BAW."currency_id" <>
		LOAI_TIEN_CHINH --Nếu không hạch toán ngoại tệ thì không in ra dòng xử lý chêch lệch(vì cũng có trường hợp VND mà giá trị ở cột CashOutDiff"TK_CONG_NO"Finance vẫn có. Xem funtiontest)
		AND R."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
		R."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"

		) W
		ORDER BY
		w."MasterSortOrder",
		W."STT",
		W."SortOrderDetail" 
		;
		END IF
		;

		END LOOP
		;


		DROP TABLE IF EXISTS TMP_TINH_TONG
		;

		CREATE TEMP TABLE TMP_TINH_TONG

		(
		"ID_CHUNG_TU" INT ,
		"MODEL_CHUNG_TU"                   VARCHAR(255),
		"TONG_TIEN_QUY_DOI" DECIMAL(25, 8) ,
		"TONG_TIEN" DECIMAL(25, 8)
		);

		INSERT INTO  TMP_TINH_TONG
		SELECT
		"ID_CHUNG_TU" ,
		"MODEL_CHUNG_TU" ,

		SUM(CASE WHEN "TK_CO" LIKE N'112%%' THEN "THANH_TIEN_QUY_DOI"
		ELSE CASE WHEN "TK_NO" LIKE N'112%%' THEN -"THANH_TIEN_QUY_DOI"
		ELSE 0
		END
		END) ,
		SUM(CASE WHEN "TK_CO" LIKE N'112%%' THEN "THANH_TIEN"
		ELSE CASE WHEN "TK_NO" LIKE N'112%%' THEN -"THANH_TIEN"
		ELSE 0
		END
		END)
		FROM    TMP_KET_QUA
		GROUP BY
		"ID_CHUNG_TU" ,
		"MODEL_CHUNG_TU"
		;

		DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
		;

		CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
		AS

		SELECT
		R."SO_TAI_KHOAN_NGAN_HANG" ,
		"TEN_NGAN_HANG" ,
		"NGAY_CHUNG_TU" ,
		R."ID_CHUNG_TU" ,
		R."MODEL_CHUNG_TU" ,
		"SO_CHUNG_TU" ,
		"LOAI_CHUNG_TU" ,
		"DIA_CHI" ,
		"DIEN_GIAI" ,
		"LOAI_TIEN" ,
		"TY_GIA" ,
		"TEN_KHACH_HANG" ,
		"SO_TAI_KHOAN_NGAN_HANG_DOI_TUONG" ,
		"TEN_NGAN_HANG_DOI_TUONG" ,
		"THANH_TIEN" ,
		"THANH_TIEN_QUY_DOI" ,
		"TK_NO" ,
		"TK_CO" ,
		"TK_CONG_NO" ,
		"DIEN_GIAI_DETAIL" ,

		"MasterSortOrder" ,
		"STT" ,
		"SortOrderDetail",
		COALESCE(S."TONG_TIEN_QUY_DOI", 0) AS "TONG_TIEN_QUY_DOI" ,
		COALESCE(S."TONG_TIEN", 0) AS "TONG_TIEN"
		FROM    TMP_KET_QUA R
		LEFT JOIN TMP_TINH_TONG S ON R."ID_CHUNG_TU" = S."ID_CHUNG_TU" AND R."MODEL_CHUNG_TU" = S."MODEL_CHUNG_TU"
		ORDER BY
		"MasterSortOrder" ,
		"STT"  ;


		END $$

		;


		SELECT *
		FROM TMP_KET_QUA_CUOI_CUNG 
		ORDER BY
		"MasterSortOrder" ,
		"STT"  ;

		;
		"""
		return self.execute(query)

	@api.model_cr
	def init(self):
		self.env.cr.execute(""" 
		DROP FUNCTION IF EXISTS LAY_TAI_KHOAN_TONG_HOP_CHUNG_CHUYEN_TIEN_NOI_BO( IN ID_CHUNG_TU INT, TK_CO VARCHAR(255) ) --Func_GetParentAccountOfBAInternalTransferDetail
		;

		CREATE OR REPLACE FUNCTION LAY_TAI_KHOAN_TONG_HOP_CHUNG_CHUYEN_TIEN_NOI_BO(IN ID_CHUNG_TU INT,
																									 TK_CO       VARCHAR(255))
			RETURNS VARCHAR
		AS $$
		DECLARE
			TAI_KHOAN           VARCHAR(255);

			TONG_TAI_KHOAN      INT;

			TAI_KHOAN_PHAN_TRAM VARCHAR(255);

			TK_CO_PHAN_TRAM     VARCHAR(255);


		BEGIN
			-- Lấy về tài khoản "TK_CO"


			TK_CO_PHAN_TRAM = TK_CO || '%%'
			;

			-- Lấy "TK_CO" nhỏ nhất
			TAI_KHOAN = (SELECT (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = CAD."TK_CO_ID")
						 FROM account_ex_phieu_thu_chi_tiet CAD
							 INNER JOIN danh_muc_he_thong_tai_khoan ACC ON (SELECT "SO_TAI_KHOAN"
																			FROM danh_muc_he_thong_tai_khoan TK
																			WHERE TK.id = CAD."TK_CO_ID") = ACC."SO_TAI_KHOAN"
						 WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																 FROM danh_muc_he_thong_tai_khoan TK
																 WHERE TK.id = CAD."TK_CO_ID") LIKE TK_CO_PHAN_TRAM
						 ORDER BY
							 ACC."BAC",
							 (SELECT "SO_TAI_KHOAN"
							  FROM danh_muc_he_thong_tai_khoan TK
							  WHERE TK.id = CAD."TK_CO_ID")
						 LIMIT 1)
			;


			TONG_TAI_KHOAN = (SELECT COUNT(*)
							  FROM account_ex_phieu_thu_chi_tiet CAD
							  WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																	  FROM danh_muc_he_thong_tai_khoan TK
																	  WHERE TK.id = CAD."TK_CO_ID") LIKE TK_CO_PHAN_TRAM
			)
			;


			TAI_KHOAN_PHAN_TRAM = TAI_KHOAN || '%%'
			;

			-- Trường hợp Count theo "TK_CO"%% nhỏ nhất không bằng tổng số "TK_CO" thì lấy Parent của "TK_CO" nhỏ nhất
			IF TONG_TAI_KHOAN <> (SELECT COUNT(*)
								  FROM account_ex_phieu_thu_chi_tiet CAD
								  WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																		  FROM danh_muc_he_thong_tai_khoan TK
																		  WHERE TK.id = CAD."TK_CO_ID") LIKE
																		 TAI_KHOAN_PHAN_TRAM)
			THEN
				TAI_KHOAN = (SELECT "SO_TAI_KHOAN"
							 FROM danh_muc_he_thong_tai_khoan
							 WHERE "id" = (SELECT "parent_id"
										   FROM danh_muc_he_thong_tai_khoan
										   WHERE "SO_TAI_KHOAN" = TAI_KHOAN))
				;
			END IF
			;

			IF TAI_KHOAN IS NULL OR TAI_KHOAN = ''
			THEN
				TAI_KHOAN = TK_CO
				;
			END IF
			;

			RETURN TAI_KHOAN
			;
		END
		;
		$$ LANGUAGE PLpgSQL
		;

		""")


		self.env.cr.execute(""" 
		DROP FUNCTION IF EXISTS LAY_TAI_KHOAN_TONG_HOP_CHUNG_TREN_SEC_UY_NHIEM_CHI_MUA_DICH_VU_CHI_TIET( IN ID_CHUNG_TU INT, TK_CO VARCHAR(255) ) --Func_GetParentAccountOfPUServiceDetail
		;

		CREATE OR REPLACE FUNCTION LAY_TAI_KHOAN_TONG_HOP_CHUNG_TREN_SEC_UY_NHIEM_CHI_MUA_DICH_VU_CHI_TIET(IN ID_CHUNG_TU INT,
																									 TK_CO       VARCHAR(255))
			RETURNS VARCHAR
		AS $$
		DECLARE
			TAI_KHOAN           VARCHAR(255);

			TONG_TAI_KHOAN      INT;

			TAI_KHOAN_PHAN_TRAM VARCHAR(255);

			TK_CO_PHAN_TRAM     VARCHAR(255);


		BEGIN
			-- Lấy về tài khoản "TK_CO"


			TK_CO_PHAN_TRAM = TK_CO || '%%'
			;

			-- Lấy "TK_CO" nhỏ nhất
			TAI_KHOAN = (SELECT (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = CAD."TK_CO_ID")
						 FROM purchase_document_line CAD
							 INNER JOIN danh_muc_he_thong_tai_khoan ACC ON (SELECT "SO_TAI_KHOAN"
																			FROM danh_muc_he_thong_tai_khoan TK
																			WHERE TK.id = CAD."TK_CO_ID") = ACC."SO_TAI_KHOAN"
						 WHERE CAD."order_id" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																 FROM danh_muc_he_thong_tai_khoan TK
																 WHERE TK.id = CAD."TK_CO_ID") LIKE TK_CO_PHAN_TRAM
						 ORDER BY
							 ACC."BAC",
							 (SELECT "SO_TAI_KHOAN"
							  FROM danh_muc_he_thong_tai_khoan TK
							  WHERE TK.id = CAD."TK_CO_ID")
						 LIMIT 1)
			;


			TONG_TAI_KHOAN = (SELECT COUNT(*)
							  FROM purchase_document_line CAD
							  WHERE CAD."order_id" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																	  FROM danh_muc_he_thong_tai_khoan TK
																	  WHERE TK.id = CAD."TK_CO_ID") LIKE TK_CO_PHAN_TRAM
			)
			;


			TAI_KHOAN_PHAN_TRAM = TAI_KHOAN || '%%'
			;

			-- Trường hợp Count theo "TK_CO"%% nhỏ nhất không bằng tổng số "TK_CO" thì lấy Parent của "TK_CO" nhỏ nhất
			IF TONG_TAI_KHOAN <> (SELECT COUNT(*)
								  FROM purchase_document_line CAD
								  WHERE CAD."order_id" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																		  FROM danh_muc_he_thong_tai_khoan TK
																		  WHERE TK.id = CAD."TK_CO_ID") LIKE
																		 TAI_KHOAN_PHAN_TRAM)
			THEN
				TAI_KHOAN = (SELECT "SO_TAI_KHOAN"
							 FROM danh_muc_he_thong_tai_khoan
							 WHERE "id" = (SELECT "parent_id"
										   FROM danh_muc_he_thong_tai_khoan
										   WHERE "SO_TAI_KHOAN" = TAI_KHOAN))
				;
			END IF
			;

			IF TAI_KHOAN IS NULL OR TAI_KHOAN = ''
			THEN
				TAI_KHOAN = TK_CO
				;
			END IF
			;

			RETURN TAI_KHOAN
			;

		END
		;
		$$ LANGUAGE PLpgSQL
		;
		""")

		self.env.cr.execute(""" 
				DROP FUNCTION IF EXISTS LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_SEC_UY_NHIEM_CHI( IN ID_CHUNG_TU INT, TK_CO VARCHAR(255) ) --Func_GetParentAccountOfBAWithdrawDetail
		;

		CREATE OR REPLACE FUNCTION LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_SEC_UY_NHIEM_CHI(IN ID_CHUNG_TU INT,
																									 TK_CO       VARCHAR(255))
			RETURNS VARCHAR
		AS $$
		DECLARE
			TAI_KHOAN           VARCHAR(255);

			TONG_TAI_KHOAN      INT;

			TAI_KHOAN_PHAN_TRAM VARCHAR(255);

			TK_CO_PHAN_TRAM     VARCHAR(255);


		BEGIN
			-- Lấy về tài khoản "TK_CO"


			TK_CO_PHAN_TRAM = TK_CO || '%%'
			;

			-- Lấy "TK_CO" nhỏ nhất
			TAI_KHOAN = (SELECT (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = CAD."TK_CO_ID")
						 FROM account_ex_phieu_thu_chi_tiet CAD
							 INNER JOIN danh_muc_he_thong_tai_khoan ACC ON (SELECT "SO_TAI_KHOAN"
																			FROM danh_muc_he_thong_tai_khoan TK
																			WHERE TK.id = CAD."TK_CO_ID") = ACC."SO_TAI_KHOAN"
						 WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																 FROM danh_muc_he_thong_tai_khoan TK
																 WHERE TK.id = CAD."TK_CO_ID") LIKE TK_CO_PHAN_TRAM
						 ORDER BY
							 ACC."BAC",
							 (SELECT "SO_TAI_KHOAN"
							  FROM danh_muc_he_thong_tai_khoan TK
							  WHERE TK.id = CAD."TK_CO_ID")
						 LIMIT 1)
			;


			TONG_TAI_KHOAN = (SELECT COUNT(*)
							  FROM account_ex_phieu_thu_chi_tiet CAD
							  WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																	  FROM danh_muc_he_thong_tai_khoan TK
																	  WHERE TK.id = CAD."TK_CO_ID") LIKE TK_CO_PHAN_TRAM
			)
			;


			TAI_KHOAN_PHAN_TRAM = TAI_KHOAN || '%%'
			;

			-- Trường hợp Count theo "TK_CO"%% nhỏ nhất không bằng tổng số "TK_CO" thì lấy Parent của "TK_CO" nhỏ nhất
			IF TONG_TAI_KHOAN <> (SELECT COUNT(*)
								  FROM account_ex_phieu_thu_chi_tiet CAD
								  WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																		  FROM danh_muc_he_thong_tai_khoan TK
																		  WHERE TK.id = CAD."TK_CO_ID") LIKE
																		 TAI_KHOAN_PHAN_TRAM)
			THEN
				TAI_KHOAN = (SELECT "SO_TAI_KHOAN"
							 FROM danh_muc_he_thong_tai_khoan
							 WHERE "id" = (SELECT "parent_id"
										   FROM danh_muc_he_thong_tai_khoan
										   WHERE "SO_TAI_KHOAN" = TAI_KHOAN))
				;
			END IF
			;

			IF TAI_KHOAN IS NULL OR TAI_KHOAN = ''
			THEN
				TAI_KHOAN = TK_CO
				;
			END IF
			;

			RETURN TAI_KHOAN
			;
		END
		;
		$$ LANGUAGE PLpgSQL
		;

		""")


		self.env.cr.execute(""" 
				DROP FUNCTION IF EXISTS LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_CHUNG_TU_BAN_HANG( IN ID_CHUNG_TU INT, SO_TAI_KHOAN VARCHAR(255) ) --Func_GetParentAccountOfSAInvoiceDetail
		;

		CREATE OR REPLACE FUNCTION LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_CHUNG_TU_BAN_HANG(IN ID_CHUNG_TU INT,
																									 SO_TAI_KHOAN       VARCHAR(255))
			RETURNS VARCHAR
		AS $$
		DECLARE
			TAI_KHOAN           VARCHAR(255);

			TONG_TAI_KHOAN      INT;

			TAI_KHOAN_PHAN_TRAM VARCHAR(255);

			TK_CO_PHAN_TRAM     VARCHAR(255);


		BEGIN
			-- Lấy về tài khoản "SO_TAI_KHOAN"


			TK_CO_PHAN_TRAM = SO_TAI_KHOAN || '%%'
			;

			-- Lấy "SO_TAI_KHOAN" nhỏ nhất
			TAI_KHOAN = (SELECT (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = CAD."TK_NO_ID")
						 FROM sale_document_line CAD
							 INNER JOIN danh_muc_he_thong_tai_khoan ACC ON (SELECT "SO_TAI_KHOAN"
																			FROM danh_muc_he_thong_tai_khoan TK
																			WHERE TK.id = CAD."TK_NO_ID") = ACC."SO_TAI_KHOAN"
						 WHERE CAD."SALE_DOCUMENT_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																 FROM danh_muc_he_thong_tai_khoan TK
																 WHERE TK.id = CAD."TK_NO_ID") LIKE TK_CO_PHAN_TRAM
						 ORDER BY
							 ACC."BAC",
							 (SELECT "SO_TAI_KHOAN"
							  FROM danh_muc_he_thong_tai_khoan TK
							  WHERE TK.id = CAD."TK_NO_ID")
						 LIMIT 1)
			;


			TONG_TAI_KHOAN = (SELECT COUNT(*)
							  FROM sale_document_line CAD
							  WHERE CAD."SALE_DOCUMENT_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																	  FROM danh_muc_he_thong_tai_khoan TK
																	  WHERE TK.id = CAD."TK_NO_ID") LIKE TK_CO_PHAN_TRAM
			)
			;


			TAI_KHOAN_PHAN_TRAM = TAI_KHOAN || '%%'
			;

			-- Trường hợp Count theo "SO_TAI_KHOAN"%% nhỏ nhất không bằng tổng số "SO_TAI_KHOAN" thì lấy Parent của "SO_TAI_KHOAN" nhỏ nhất
			IF TONG_TAI_KHOAN <> (SELECT COUNT(*)
								  FROM sale_document_line CAD
								  WHERE CAD."SALE_DOCUMENT_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																		  FROM danh_muc_he_thong_tai_khoan TK
																		  WHERE TK.id = CAD."TK_NO_ID") LIKE
																		 TAI_KHOAN_PHAN_TRAM)
			THEN
				TAI_KHOAN = (SELECT "SO_TAI_KHOAN"
							 FROM danh_muc_he_thong_tai_khoan
							 WHERE "id" = (SELECT "parent_id"
										   FROM danh_muc_he_thong_tai_khoan
										   WHERE "SO_TAI_KHOAN" = TAI_KHOAN))
				;
			END IF
			;

			IF TAI_KHOAN IS NULL OR TAI_KHOAN = ''
			THEN
				TAI_KHOAN = SO_TAI_KHOAN
				;
			END IF
			;

			RETURN TAI_KHOAN
			;


		END
		;
		$$ LANGUAGE PLpgSQL
		;
		""")


		self.env.cr.execute(""" 
				DROP FUNCTION IF EXISTS LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_TRA_TIEN_GUI( IN ID_CHUNG_TU INT, SO_TAI_KHOAN VARCHAR(255) ) --Func_GetParentAccountOfBADepositDetail
		;

		CREATE OR REPLACE FUNCTION LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_TRA_TIEN_GUI(IN ID_CHUNG_TU INT,
																									 SO_TAI_KHOAN       VARCHAR(255))
			RETURNS VARCHAR
		AS $$
		DECLARE
			TAI_KHOAN           VARCHAR(255);

			TONG_TAI_KHOAN      INT;

			TAI_KHOAN_PHAN_TRAM VARCHAR(255);

			TK_CO_PHAN_TRAM     VARCHAR(255);


		BEGIN
			-- Lấy về tài khoản "SO_TAI_KHOAN"


			TK_CO_PHAN_TRAM = SO_TAI_KHOAN || '%%'
			;

			-- Lấy "SO_TAI_KHOAN" nhỏ nhất
			TAI_KHOAN = (SELECT (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = CAD."TK_NO_ID")
						 FROM account_ex_phieu_thu_chi_tiet CAD
							 INNER JOIN danh_muc_he_thong_tai_khoan ACC ON (SELECT "SO_TAI_KHOAN"
																			FROM danh_muc_he_thong_tai_khoan TK
																			WHERE TK.id = CAD."TK_NO_ID") = ACC."SO_TAI_KHOAN"
						 WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																 FROM danh_muc_he_thong_tai_khoan TK
																 WHERE TK.id = CAD."TK_NO_ID") LIKE TK_CO_PHAN_TRAM
						 ORDER BY
							 ACC."BAC",
							 (SELECT "SO_TAI_KHOAN"
							  FROM danh_muc_he_thong_tai_khoan TK
							  WHERE TK.id = CAD."TK_NO_ID")
						 LIMIT 1)
			;


			TONG_TAI_KHOAN = (SELECT COUNT(*)
							  FROM account_ex_phieu_thu_chi_tiet CAD
							  WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																	  FROM danh_muc_he_thong_tai_khoan TK
																	  WHERE TK.id = CAD."TK_NO_ID") LIKE TK_CO_PHAN_TRAM
			)
			;


			TAI_KHOAN_PHAN_TRAM = TAI_KHOAN || '%%'
			;

			-- Trường hợp Count theo "SO_TAI_KHOAN"%% nhỏ nhất không bằng tổng số "SO_TAI_KHOAN" thì lấy Parent của "SO_TAI_KHOAN" nhỏ nhất
			IF TONG_TAI_KHOAN <> (SELECT COUNT(*)
								  FROM account_ex_phieu_thu_chi_tiet CAD
								  WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																		  FROM danh_muc_he_thong_tai_khoan TK
																		  WHERE TK.id = CAD."TK_NO_ID") LIKE
																		 TAI_KHOAN_PHAN_TRAM)
			THEN
				TAI_KHOAN = (SELECT "SO_TAI_KHOAN"
							 FROM danh_muc_he_thong_tai_khoan
							 WHERE "id" = (SELECT "parent_id"
										   FROM danh_muc_he_thong_tai_khoan
										   WHERE "SO_TAI_KHOAN" = TAI_KHOAN))
				;
			END IF
			;

			IF TAI_KHOAN IS NULL OR TAI_KHOAN = ''
			THEN
				TAI_KHOAN = SO_TAI_KHOAN
				;
			END IF
			;

			RETURN TAI_KHOAN
			;


		END
		;
		$$ LANGUAGE PLpgSQL
		;
		""")

