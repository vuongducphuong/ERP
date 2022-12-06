# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from datetime import timedelta, datetime

class BAO_CAO_UNC_AGRIBANK(models.Model):
	_name = 'bao.cao.uy.nhiem.chi.agribank'
	_auto = False

	ref = fields.Char(string='Reffence ID')
	ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
	MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')
	LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ')#RefType
	NGAY_CHUNG_TU = fields.Char(string='Ngày chứng từ')#RefDate
	STK_NGAN_HANG = fields.Char(string='STK ngân hàng')#BankAccountNumber
	TEN_NGAN_HANG = fields.Char(string='Tên ngân hàng')#BankName
	CHI_NHANH_CUA_NGAN_HANG = fields.Char(string='Chi nhánh ngân hàng')#BranchOfBank
	TEN_NGAN_HANG_DI = fields.Char(string='Tên ngân hàng DI')#DIBankName
	CHU_TK_NGAN_HANG = fields.Char(string='Chủ TK ngân hàng')#BankOwner
	STK_NGAN_HANG_DOI_TUONG = fields.Char(string='Số tài khoản ngân hàng đối tượng')#AccountObjectBankAccount
	TEN_DOI_TUONG = fields.Char(string='Tên đối tượng')#AccountObjectName
	DIA_CHI_DOI_TUONG = fields.Char(string='Địa chỉ đối tượng')#AccountObjectAddress
	DIA_CHI_DOI_TUONG_DI = fields.Char(string='Địa chỉ đối tượng DI')#AccountObjectAddressDI
	TEN_NGAN_HANG_DOI_TUONG = fields.Char(string='Tên ngân hàng đối tượng')#AccountObjectBankName
	CHI_NHANH_NGAN_HANG_DOI_TUONG = fields.Char(string='Chi nhánh ngân hàng đối tượng')#BranchOfAccountObjectBank
	SO_CMND = fields.Char(string='Số CMND')#IdentificationNumber
	NGAY_CMND = fields.Date(string='Ngày CMND')#IssueDate
	NOI_CAP_CMND = fields.Char(string='Nơi cấp CMND')#IssueBy
	SO_DIEN_THOAI = fields.Char(string='Số điện thoại')#Tel
	DIEN_GIAI = fields.Char(string='Diễn giải')#JournalMemo
	LOAI_TIEN = fields.Char(string='Loại tiền')#CurrencyID
	TONG_TIEN = fields.Monetary(string='Tổng tiền',currency_field='currency_id')#TotalAmountOC
	SO_CHUNG_TU = fields.Char(string='Số chứng từ')#RefNo
	NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán')#PostedDate
	MA_CHI_NHANH = fields.Char(string='Mã chi nhánh')#BranchCode
	TAI_KHOAN_NGAN_HANG = fields.Char(string='Tài khoản ngân hàng')#BankAccount
	THONG_TIN_TEN_NGAN_HANG = fields.Char(string='Thông tin tên ngân hàng')#InfoBankName
	THONG_TIN_DIA_CHI_NGAN_HANG = fields.Char(string='Thông tin địa chỉ ngân hàng')#InfoBankAddress
	DIA_CHI_NGAN_HANG = fields.Char(string='Địa chỉ ngân hàng')#Address
	TEN_CHI_NHANH_NGAN_HANG = fields.Char(string='Tên chi nhánh ngân hàng')#BankBranchName
	TAI_KHOAN_DOI_TUONG = fields.Char(string='Tài khoản đối tượng')#AccountingObjectCode
	TY_GIA = fields.Float(string='Tỷ giá')#ExchangeRate
	TONG_TIEN_QUY_DOI = fields.Float(string='Tổng tiền quy đổi')#TotalAmount
	

	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
	
	ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.uy.nhiem.chi.agribank.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')

	

class BAO_CAO_UNC_AGRIBANK_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_agribankunc'

	@api.model
	def get_report_values(self, docids, data=None):

		refTypeList, records = self.get_reftype_list(data)
		sql_result = self.ham_lay_du_lieu_tra_ve(refTypeList)
		############### START SQL lấy dữ liệu ###############
		
		for line in sql_result:
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
			
			master_data = self.env['bao.cao.uy.nhiem.chi.agribank'].convert_for_update(line)
			detail_data = self.env['bao.cao.uy.nhiem.chi.agribank.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
				records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.uy.nhiem.chi.agribank.chi.tiet'].new(detail_data)
		
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

			str_tai_ngan_hang_doi_tuong = record.TEN_NGAN_HANG_DOI_TUONG
			if not record.CHI_NHANH_NGAN_HANG_DOI_TUONG:
				str_tai_ngan_hang_doi_tuong = record.TEN_NGAN_HANG_DOI_TUONG
			else:
				str_tai_ngan_hang_doi_tuong = record.TEN_NGAN_HANG_DOI_TUONG + ' - ' + record.CHI_NHANH_NGAN_HANG_DOI_TUONG
			record.TEN_NGAN_HANG_DOI_TUONG = str_tai_ngan_hang_doi_tuong
			
			str_ngay_chung_tu = ""

			if not record.NGAY_CHUNG_TU:
				record.NGAY_CHUNG_TU = str_ngay_chung_tu
			else:
				record.NGAY_CHUNG_TU = datetime.strptime(record.NGAY_CHUNG_TU,'%Y-%m-%d %H:%M:%S').date().strftime('%d/%m/%Y')
				
		# Tạo object để in
		return {
			'docs':docs,
		}
	
	def ham_lay_du_lieu_tra_ve(self , refTypeList):
		query = """
			DO LANGUAGE plpgsql $$--AgribankUNC
DECLARE

		ListRefID                            VARCHAR := N'""" + refTypeList + """';

--     ListRefID                            VARCHAR := N',105;4010,';

	rec                                  RECORD;

	CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO BOOLEAN:=False;


	CHE_DO_KE_TOAN                       VARCHAR;

BEGIN

	SELECT value
	INTO CHE_DO_KE_TOAN
	FROM ir_config_parameter
	WHERE key = 'he_thong.CHE_DO_KE_TOAN'
	FETCH FIRST 1 ROW ONLY
	;


	DROP TABLE IF EXISTS TMP_PARAM
	;

	DROP SEQUENCE IF EXISTS TMP_PARAM_seq
	;

	CREATE TEMP SEQUENCE TMP_PARAM_seq
	;

	CREATE TEMP TABLE TMP_PARAM
	(
		"ID_CHUNG_TU"   INT,
		"LOAI_CHUNG_TU" INT,

		"STT"           INT DEFAULT NEXTVAL('TMP_PARAM_seq')
			PRIMARY KEY
	)
	;


	INSERT INTO TMP_PARAM
		SELECT

			  Value1 AS "ID_CHUNG_TU"
			, Value2 AS "LOAI_CHUNG_TU"

		FROM CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(ListRefID, ',', ';') F
			INNER JOIN danh_muc_reftype R ON F.Value2 = R."REFTYPE"

	;


	SELECT value
	INTO CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO
	FROM ir_config_parameter
	WHERE key = 'he_thong.CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO'
	FETCH FIRST 1 ROW ONLY
	;


	DROP TABLE IF EXISTS TMP_KET_QUA
	;

	CREATE TEMP TABLE TMP_KET_QUA

	(
		"ID_CHUNG_TU"                   INT,
		"MODEL_CHUNG_TU"                VARCHAR(255),
		"LOAI_CHUNG_TU"                 INT,
		"NGAY_CHUNG_TU"                 TIMESTAMP,
		/* == Bên chuyển == */
		"STK_NGAN_HANG"                 VARCHAR(255),
		"TEN_NGAN_HANG"                 VARCHAR(255),
		"CHI_NHANH_CUA_NGAN_HANG"       VARCHAR(255),
		"TEN_NGAN_HANG_DI"              VARCHAR(255), /*TienHM thi công 109005 bổ sung Tên Ngân hàng lấy từ danh mục Ngân hàng phục vụ Mẫu của BIDV*/
		"CHU_TK_NGAN_HANG"              VARCHAR(255),
		/* == Bên hưởng == */
		"STK_NGAN_HANG_DOI_TUONG"       VARCHAR(255),
		"TEN_DOI_TUONG"                 VARCHAR(255),
		"DIA_CHI_DOI_TUONG"             VARCHAR(255),
		"DIA_CHI_DOI_TUONG_DI"          VARCHAR(255), /*Địa chỉ đối tượng trong danh mục*/
		"TEN_NGAN_HANG_DOI_TUONG"       VARCHAR(255),
		"CHI_NHANH_NGAN_HANG_DOI_TUONG" VARCHAR(255),
		"SO_CMND"                       VARCHAR(255),
		"NGAY_CMND"                     TIMESTAMP,
		"NOI_CAP_CMND"                  VARCHAR(255),
		"SO_DIEN_THOAI"                 VARCHAR(127),


		"DIEN_GIAI"                     VARCHAR(255),
		"LOAI_TIEN"                     VARCHAR(15),
		"TONG_TIEN"                     DECIMAL(22, 8),
		--Các trường có ở mẫu UNC 2012 -bổ sung trên 2015
		"SO_CHUNG_TU"                   VARCHAR(255), -- Số chứng từ
		"NGAY_HACH_TOAN"                TIMESTAMP, -- ngày ghi sổ
		"MA_CHI_NHANH"                  VARCHAR(127),
		"TAI_KHOAN_NGAN_HANG"           VARCHAR(255), -- Số tài khoản
		"THONG_TIN_TEN_NGAN_HANG"       VARCHAR(255),
		"THONG_TIN_DIA_CHI_NGAN_HANG"   VARCHAR(255),
		"DIA_CHI_NGAN_HANG"             VARCHAR(255), -- địa chỉ ngân hàng
		"TEN_CHI_NHANH_NGAN_HANG"       VARCHAR(255),
		"TAI_KHOAN_DOI_TUONG"           VARCHAR(127),
		"TY_GIA"                        DECIMAL(22, 8),
		"TONG_TIEN_QUY_DOI"             DECIMAL(22, 8), -- Số tiền quy đổi
		"TK_NO"                         VARCHAR(255), -- Tài khoản
		"TK_CO"                         VARCHAR(255), -- Tài khoản
		"DIEN_GIAI_DEATAIL"             VARCHAR(255), -- Diễn giải chi tiết
		"THANH_TIEN_QUY_DOI"            DECIMAL(22, 8),
		"THANH_TIEN"                    DECIMAL(22, 8),
        "SortOrder"              INT,
        "SortOrderDetail"        INT

	)
	;

	FOR rec IN
	SELECT
		DISTINCT
		  PR."ID_CHUNG_TU"   AS "ID_CHUNG_TU"
		, PR."LOAI_CHUNG_TU" AS "LOAI_CHUNG_TU"
	FROM
		TMP_PARAM PR
	LOOP

		IF rec."LOAI_CHUNG_TU" = ANY
		   ('{302,307,308,309,310,312,313,314,315,316,318,319,320,321,322,324,325,326,327,328,352,357,358,359,360,362,363,364,365,366,368,369,370,371,372,374,375,376,377,378}' :: INT [])-- 'PUVoucher'  --PUService BAWithDraw
		THEN

			INSERT INTO TMP_KET_QUA

				SELECT
					SV."id"
					, 'purchase.document'              AS "MODEL_CHUNG_TU"
					, SV."LOAI_CHUNG_TU"
					, SV."NGAY_CHUNG_TU"
					, -- Phần đề nghị ghi nợ TK
					  BA."SO_TAI_KHOAN"                AS "STK_NGAN_HANG"
					, SV."CHI_NHANH_TK_CHI"            AS "TEN_NGAN_HANG"
					, BA."CHI_NHANH"                   AS "CHI_NHANH_CUA_NGAN_HANG"
					, --OU."TEN_DON_VI",
					  B."TEN_DAY_DU"                   AS "TEN_NGAN_HANG_DI"
					, /*TienHM thi công 109005 bổ sung Tên Ngân hàng lấy từ danh mục Ngân hàng phục vụ Mẫu của BIDV*/
					BA."CHU_TAI_KHOAN"
					, -- Ghi có TK
					  (SELECT "SO_TAI_KHOAN"
					   FROM danh_muc_doi_tuong_chi_tiet TK
					   WHERE TK.id = SV."TK_NHAN_ID")  AS "STK_NGAN_HANG_DOI_TUONG"
					, SV."TEN_DOI_TUONG"
					, SV."DIA_CHI"
					, A."DIA_CHI"                      AS "DIA_CHI_DOI_TUONG_DI"
					, /*nhyen - 6/10/2017 (Bug148005): Địa chỉ đối tượng nhận trong danh mục */
					  SV."CHI_NHANH_TK_NHAN"           AS "TEN_NGAN_HANG_DOI_TUONG"
					, ABA."CHI_NHANH"
					,
					/*nhyen - 18/4/2018 (Bug 212077): Sửa lại cách lấy thông tin Chi nhánh và Tính/ TP của chi nhánh bên hưởng */

					  CASE WHEN A."LOAI_KHACH_HANG" = '0'
						  THEN NULL
					  ELSE A."SO_CMND"
					  END                              AS "SO_CMND"
					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN NULL
					  ELSE A."NGAY_CAP"
					  END                              AS "NGAY_CMND"
					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN NULL
					  ELSE A."NOI_CAP"
					  END                              AS "NOI_CAP_CMND"
					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN A."DIEN_THOAI"
					  ELSE A."DT_DI_DONG"
					  END                              AS "SO_DIEN_THOAI"
					, SV."LY_DO_CHI"
					, (SELECT "MA_LOAI_TIEN"
					   FROM res_currency TK
					   WHERE TK.id = SV."currency_id") AS "LOAI_TIEN"
					, CASE WHEN (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = SVD."TK_CO_ID") NOT LIKE N'112%%'
								AND (SELECT "SO_TAI_KHOAN"
									 FROM danh_muc_he_thong_tai_khoan TK
									 WHERE TK.id = SVD."TK_CO_ID") NOT LIKE N'311%%'
								AND (SELECT "SO_TAI_KHOAN"
									 FROM danh_muc_he_thong_tai_khoan TK
									 WHERE TK.id = SVD."TK_CO_ID") NOT LIKE N'341%%'
					THEN 0
					  WHEN SV."LOAI_CHUNG_TU" IN (307, 308, 309, 310, 312, 313, 314, 315, 316, 357, 358,
												  359, 360, 362, 363, 364, 365, 366)
						  THEN SVD."THANH_TIEN_QUY_DOI" - SVD."TIEN_CHIET_KHAU_QUY_DOI" + SVD."TIEN_THUE_GTGT_QUY_DOI"
					  ELSE SVD."THANH_TIEN_QUY_DOI" - SVD."TIEN_CHIET_KHAU_QUY_DOI"
					  END
					, --Các trường bổ sung cho giống mẫu UNC 2012
					  CASE
					  WHEN SV."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
						  THEN SV."SO_UY_NHIEM_CHI"
					  WHEN SV."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
						  THEN SV."SO_SEC_CHUYEN_KHOAN"
					  WHEN SV."LOAI_THANH_TOAN" = 'sec_tien_mat'
						  THEN SV."SO_SEC_TIEN_MAT"
					  ELSE
						  SV."SO_PHIEU_CHI"
					  END                              AS "SO_CHUNG_TU"
					, SV."NGAY_HACH_TOAN"
					, OU."MA_DON_VI"                   AS "MA_CHI_NHANH"
					, BA."SO_TAI_KHOAN"                AS "TAI_KHOAN_NGAN_HANG"
					, BA."CHI_NHANH"                   AS "THONG_TIN_TEN_NGAN_HANG"
					, BA."DIA_CHI_CN"                  AS "THONG_TIN_DIA_CHI_NGAN_HANG"
					, BA."DIA_CHI_CN"
					, BA."CHI_NHANH"
					, A."MA"
					, SV."TY_GIA"
					, SV."TONG_TIEN_HANG_QUY_DOI"
					, (SELECT "SO_TAI_KHOAN"
					   FROM danh_muc_he_thong_tai_khoan TK
					   WHERE TK.id = SVD."TK_NO_ID")
					, (SELECT "SO_TAI_KHOAN"
					   FROM danh_muc_he_thong_tai_khoan TK
					   WHERE TK.id = SVD."TK_CO_ID")
					, SVD."name"
					, CASE WHEN (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = SVD."TK_CO_ID") NOT LIKE N'112%%'
								AND (SELECT "SO_TAI_KHOAN"
									 FROM danh_muc_he_thong_tai_khoan TK
									 WHERE TK.id = SVD."TK_CO_ID") NOT LIKE N'311%%'
								AND (SELECT "SO_TAI_KHOAN"
									 FROM danh_muc_he_thong_tai_khoan TK
									 WHERE TK.id = SVD."TK_CO_ID") NOT LIKE N'341%%'
					THEN 0
					  WHEN SV."LOAI_CHUNG_TU" IN (307, 308, 309, 310, 312, 313, 314, 315, 316, 357, 358,
												  359, 360, 362, 363, 364, 365, 366)
						  THEN SVD."THANH_TIEN_QUY_DOI" - SVD."TIEN_CHIET_KHAU_QUY_DOI" + SVD."TIEN_THUE_GTGT_QUY_DOI"
					  ELSE SVD."THANH_TIEN_QUY_DOI" - SVD."TIEN_CHIET_KHAU_QUY_DOI"
					  END
					, CASE WHEN (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = SVD."TK_CO_ID") NOT LIKE N'112%%'
								AND (SELECT "SO_TAI_KHOAN"
									 FROM danh_muc_he_thong_tai_khoan TK
									 WHERE TK.id = SVD."TK_CO_ID") NOT LIKE N'311%%'
								AND (SELECT "SO_TAI_KHOAN"
									 FROM danh_muc_he_thong_tai_khoan TK
									 WHERE TK.id = SVD."TK_CO_ID") NOT LIKE N'341%%'
					THEN 0
					  WHEN SV."LOAI_CHUNG_TU" IN (307, 308, 309, 310, 312, 313, 314, 315, 316, 357, 358,
												  359, 360, 362, 363, 364, 365, 366)
						  THEN SVD."THANH_TIEN" - SVD."TIEN_CHIET_KHAU" + SVD."TIEN_THUE_GTGT"
					  ELSE SVD."THANH_TIEN" - SVD."TIEN_CHIET_KHAU"
					  END
					, P."STT"
                	,SVD."THU_TU_SAP_XEP_CHI_TIET"

				FROM purchase_document SV
					INNER JOIN purchase_document_line SVD ON SV."id" = SVD."order_id"
					INNER JOIN TMP_PARAM P ON SV."id" = P."ID_CHUNG_TU"
					LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = SV."TK_CHI_ID"
					LEFT JOIN res_partner A ON SV."DOI_TUONG_ID" = A."id"
					LEFT JOIN (SELECT
								   "DOI_TUONG_ID"
								   , "SO_TAI_KHOAN"
								   , "CHI_NHANH"
								   , "TINH_TP_CUA_NGAN_HANG"
								   , ROW_NUMBER()
									 OVER (
										 PARTITION BY
											 "DOI_TUONG_ID",
											 "SO_TAI_KHOAN"
										 ORDER BY "CHI_NHANH" ) AS RowNum
							   FROM danh_muc_doi_tuong_chi_tiet
							  ) ABA ON A."id" = ABA."DOI_TUONG_ID"
									   AND (SELECT "SO_TAI_KHOAN"
											FROM danh_muc_doi_tuong_chi_tiet TK
											WHERE TK.id = SV."TK_NHAN_ID") = ABA."SO_TAI_KHOAN"
									   AND ABA.RowNum = 1
					LEFT JOIN danh_muc_to_chuc OU ON BA."CHI_NHANH_2" = OU."id"
					LEFT JOIN danh_muc_ngan_hang B ON B."id" = BA."NGAN_HANG_ID"

					WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND P."LOAI_CHUNG_TU" =rec."LOAI_CHUNG_TU"
			;


		END IF
	;

		IF rec."LOAI_CHUNG_TU" = ANY ('{330,331,332,333,334}' :: INT [])--'PUService'
		THEN
			INSERT INTO TMP_KET_QUA
				SELECT
					SV."id"
					, 'purchase.document'              AS "MODEL_CHUNG_TU"
					, SV."LOAI_CHUNG_TU"
					, SV."NGAY_CHUNG_TU"
					, -- Phần đề nghị ghi nợ TK
					  BA."SO_TAI_KHOAN"                AS "STK_NGAN_HANG"
					, SV."CHI_NHANH_TK_CHI"            AS "TEN_NGAN_HANG"
					, BA."CHI_NHANH"                   AS "CHI_NHANH_CUA_NGAN_HANG"
					, --OU."TEN_DON_VI",
					  B."TEN_DAY_DU"                   AS "TEN_NGAN_HANG_DI"
					, /*TienHM thi công 109005 bổ sung Tên Ngân hàng lấy từ danh mục Ngân hàng phục vụ Mẫu của BIDV*/
					BA."CHU_TAI_KHOAN"
					, -- Ghi có TK
					  (SELECT "SO_TAI_KHOAN"
					   FROM danh_muc_doi_tuong_chi_tiet TK
					   WHERE TK.id = SV."TK_NHAN_ID")  AS "STK_NGAN_HANG_DOI_TUONG"
					, SV."TEN_DOI_TUONG"
					, SV."DIA_CHI"
					, A."DIA_CHI"                      AS "DIA_CHI_DOI_TUONG_DI"
					, /*nhyen - 6/10/2017 (Bug148005): Địa chỉ đối tượng nhận trong danh mục */
					  SV."CHI_NHANH_TK_NHAN"           AS "TEN_NGAN_HANG_DOI_TUONG"
					, ABA."CHI_NHANH"
					,
					/*nhyen - 18/4/2018 (Bug 212077): Sửa lại cách lấy thông tin Chi nhánh và Tính/ TP của chi nhánh bên hưởng */

					  CASE WHEN A."LOAI_KHACH_HANG" = '0'
						  THEN NULL
					  ELSE A."SO_CMND"
					  END                              AS "SO_CMND"
					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN NULL
					  ELSE A."NGAY_CAP"
					  END                              AS "NGAY_CMND"
					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN NULL
					  ELSE A."NOI_CAP"
					  END                              AS "NOI_CAP_CMND"
					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN A."DIEN_THOAI"
					  ELSE A."DT_DI_DONG"
					  END                              AS "SO_DIEN_THOAI"
					, SV."LY_DO_CHI"
					, (SELECT "MA_LOAI_TIEN"
					   FROM res_currency TK
					   WHERE TK.id = SV."currency_id") AS "LOAI_TIEN"
					, CASE WHEN (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = SVD."TK_CO_ID") LIKE '112%%' --AND SVD."TK_CO" NOT LIKE '112%%'
					THEN SVD."THANH_TIEN" - SVD."TIEN_CHIET_KHAU" + SVD."TIEN_THUE_GTGT"
					  ELSE 0
					  END - CASE WHEN (SELECT "SO_TAI_KHOAN"
									   FROM danh_muc_he_thong_tai_khoan TK
									   WHERE TK.id = SVD."TK_NO_ID") LIKE '112%%'
									  AND (SELECT "SO_TAI_KHOAN"
										   FROM danh_muc_he_thong_tai_khoan TK
										   WHERE TK.id = SVD."TK_CO_ID") NOT LIKE '112%%'
					THEN SVD."THANH_TIEN" - SVD."TIEN_CHIET_KHAU" + SVD."TIEN_THUE_GTGT"
							ELSE 0
							END + CASE WHEN (SELECT "SO_TAI_KHOAN"
											 FROM danh_muc_he_thong_tai_khoan TK
											 WHERE TK.id = SVD."TK_CO_ID") LIKE '311%%'
					THEN SVD."THANH_TIEN" - SVD."TIEN_CHIET_KHAU" + SVD."TIEN_THUE_GTGT"
								  ELSE 0
								  END + CASE --hhson
										WHEN (SELECT "SO_TAI_KHOAN"
											  FROM danh_muc_he_thong_tai_khoan TK
											  WHERE TK.id = SVD."TK_CO_ID") LIKE '341%%'
											THEN SVD."THANH_TIEN" - SVD."TIEN_CHIET_KHAU"
												 + SVD."TIEN_THUE_GTGT"
										ELSE 0
										END            AS "THANH_TIEN_QUY_DOI"


					, --Các trường bổ sung cho giống mẫu UNC 2012
					SV."SO_CHUNG_TU"
					, SV."NGAY_HACH_TOAN"
					, OU."MA_DON_VI"                   AS "MA_CHI_NHANH"
					, BA."SO_TAI_KHOAN"                AS "TAI_KHOAN_NGAN_HANG"
					, BA."CHI_NHANH"                   AS "THONG_TIN_TEN_NGAN_HANG"
					, BA."DIA_CHI_CN"                  AS "THONG_TIN_DIA_CHI_NGAN_HANG"
					, BA."DIA_CHI_CN"
					, BA."CHI_NHANH"
					, A."MA"
					, SV."TY_GIA"
					, SV."TONG_TIEN_HANG_QUY_DOI"
					, (SELECT "SO_TAI_KHOAN"
					   FROM danh_muc_he_thong_tai_khoan TK
					   WHERE TK.id = SVD."TK_NO_ID")
					, (SELECT "SO_TAI_KHOAN"
					   FROM danh_muc_he_thong_tai_khoan TK
					   WHERE TK.id = SVD."TK_CO_ID")
					, SVD."name"
					, SVD."THANH_TIEN_QUY_DOI" -
					  SVD."TIEN_CHIET_KHAU_QUY_DOI" +
					  SVD."TIEN_THUE_GTGT_QUY_DOI"
					, SVD."THANH_TIEN" -
					  SVD."TIEN_CHIET_KHAU" +
					  SVD."TIEN_THUE_GTGT"
					    , P."STT"
                    ,SVD."THU_TU_SAP_XEP_CHI_TIET"

				FROM purchase_document SV
					INNER JOIN purchase_document_line SVD ON SV."id" = SVD."order_id"
					INNER JOIN TMP_PARAM P ON SV."id" = P."ID_CHUNG_TU"
					LEFT JOIN
					danh_muc_tai_khoan_ngan_hang
					BA ON BA."id" = SV."TK_CHI_ID"
					LEFT JOIN
					res_partner A ON SV."DOI_TUONG_ID" = A."id"
					LEFT JOIN (SELECT
								   "DOI_TUONG_ID"
								   , "SO_TAI_KHOAN"
								   , "CHI_NHANH"
								   , "TINH_TP_CUA_NGAN_HANG"
								   , ROW_NUMBER()
									 OVER (
										 PARTITION BY "DOI_TUONG_ID",
											 "SO_TAI_KHOAN"
										 ORDER BY "CHI_NHANH" ) AS RowNum
							   FROM
								   danh_muc_doi_tuong_chi_tiet
							  ) ABA ON A."id" = ABA."DOI_TUONG_ID"
									   AND (SELECT "SO_TAI_KHOAN"
											FROM danh_muc_doi_tuong_chi_tiet TK
											WHERE TK.id =
												  SV."TK_NHAN_ID") = ABA."SO_TAI_KHOAN"
									   AND ABA.RowNum = 1
					LEFT JOIN danh_muc_to_chuc OU ON BA."CHI_NHANH_2" = OU."id"

					LEFT JOIN danh_muc_ngan_hang B ON B."id" = BA."NGAN_HANG_ID"

			WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND P."LOAI_CHUNG_TU" =rec."LOAI_CHUNG_TU"
			;


		END IF
	;


		IF rec."LOAI_CHUNG_TU" = ANY ('{3530,3531,3532,3534,3535,3536,3537,3538}' :: INT [])--SAVoucher
		THEN
			INSERT INTO TMP_KET_QUA
				SELECT
					SV."id"
					, 'sale.document'                  AS "MODEL_CHUNG_TU"
					, SV."LOAI_CHUNG_TU"

					, SV."NGAY_CHUNG_TU"
					, -- Phần đề nghị ghi nợ TK
					BA."SO_TAI_KHOAN"
					, SV."TEN_TK"
					, BA."CHI_NHANH"
					, B."TEN_DAY_DU"                   AS "TEN_NGAN_HANG_DI"
					, /*TienHM thi công 109005 bổ sung Tên Ngân hàng lấy từ danh mục TK Ngân hàng phục vụ Mẫu của BIDV*/
					BA."CHU_TAI_KHOAN"

					, -- Ghi có TK
					NULL
					, SV."TEN_KHACH_HANG"
					, SV."DIA_CHI"
					, A."DIA_CHI"                      AS "DIA_CHI_DOI_TUONG_DI"
					, /*nhyen - 6/10/2017 (Bug148005): Địa chỉ đối tượng nhận trong danh mục */
					NULL
					, --NULL ,
					--dvtien-03/08/2016: bs thêm tỉnh/thành tk ngân hàng
					"TEN_CHI_NHANH_NGAN_HANG" = (CASE WHEN A."LA_NHAN_VIEN" = '0'
						THEN NULL
												 ELSE A."TEN_CHI_NHANH_NGAN_HANG"
												 END)
					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN NULL
					  ELSE A."SO_CMND"
					  END                              AS "SO_CMND"
					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN NULL
					  ELSE A."NGAY_CAP"
					  END                              AS "NGAY_CMND"
					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN NULL
					  ELSE A."NOI_CAP"
					  END                              AS "NOI_CAP_CMND"
					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN A."DIEN_THOAI"
					  ELSE A."DT_DI_DONG"
					  END
					, SV."DIEN_GIAI"
					, (SELECT "MA_LOAI_TIEN"
					   FROM res_currency TK
					   WHERE TK.id = SV."currency_id") AS "LOAI_TIEN"
					, CASE WHEN (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = SVD."TK_CO_ID") LIKE '112%%' --AND SVD."TK_CO" NOT LIKE '112%%'
					THEN SVD."THANH_TIEN" - SVD."TIEN_CHIET_KHAU" + SVD."TIEN_THUE_GTGT"
					  ELSE 0
					  END - CASE WHEN (SELECT "SO_TAI_KHOAN"
									   FROM danh_muc_he_thong_tai_khoan TK
									   WHERE TK.id = SVD."TK_NO_ID") LIKE '112%%'
									  AND (SELECT "SO_TAI_KHOAN"
										   FROM danh_muc_he_thong_tai_khoan TK
										   WHERE TK.id = SVD."TK_CO_ID") NOT LIKE '112%%'
					THEN SVD."THANH_TIEN" - SVD."TIEN_CHIET_KHAU" + SVD."TIEN_THUE_GTGT"
							ELSE 0
							END + CASE WHEN (SELECT "SO_TAI_KHOAN"
											 FROM danh_muc_he_thong_tai_khoan TK
											 WHERE TK.id = SVD."TK_CO_ID") LIKE '311%%'
					THEN SVD."THANH_TIEN" - SVD."TIEN_CHIET_KHAU" + SVD."TIEN_THUE_GTGT"
								  ELSE 0
								  END + CASE --hhson
										WHEN (SELECT "SO_TAI_KHOAN"
											  FROM danh_muc_he_thong_tai_khoan TK
											  WHERE TK.id = SVD."TK_CO_ID") LIKE '341%%'
											THEN SVD."THANH_TIEN" - SVD."TIEN_CHIET_KHAU"
												 + SVD."TIEN_THUE_GTGT"
										ELSE 0
										END            AS "TONG_TIEN"
					, SV."SO_CHUNG_TU"
					, SV."NGAY_HACH_TOAN"
					, OU."MA_DON_VI"                   AS "MA_CHI_NHANH"
					, BA."SO_TAI_KHOAN"
					, BA."CHI_NHANH"
					, BA."DIA_CHI_CN"
					, BA."DIA_CHI_CN"
					, BA."CHI_NHANH"
					, A."MA"
					, -- NULL AS Province ,

					SV."TY_GIA"

					, "TONG_TIEN_THANH_TOAN_QĐ"
					, (SELECT "SO_TAI_KHOAN"
					   FROM danh_muc_he_thong_tai_khoan TK
					   WHERE TK.id = SVD."TK_NO_ID")
					, (SELECT "SO_TAI_KHOAN"
					   FROM danh_muc_he_thong_tai_khoan TK
					   WHERE TK.id = SVD."TK_CO_ID")
					, SVD."TEN_HANG"
					, "THANH_TIEN_QUY_DOI"
					, "THANH_TIEN"
					, P."STT"
                    ,SVD."THU_TU_SAP_XEP_CHI_TIET"

				FROM sale_document SV
					INNER JOIN sale_document_line SVD ON SV."id" = SVD."SALE_DOCUMENT_ID"
					INNER JOIN TMP_PARAM P ON SV."id" = P."ID_CHUNG_TU"
					LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = SV."NOP_VAO_TK_ID"
					LEFT JOIN res_partner A ON SV."DOI_TUONG_ID" = A."id"
					LEFT JOIN danh_muc_to_chuc OU ON BA."CHI_NHANH_2" = OU."id"


					LEFT JOIN danh_muc_ngan_hang B ON B."id" = BA."NGAN_HANG_ID"
			WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND P."LOAI_CHUNG_TU" =rec."LOAI_CHUNG_TU"
			;

		END IF
	;


		IF rec."LOAI_CHUNG_TU" = ANY ('{1510,1511,1512,1513,1514,1520,1521,1522,1523,1530,1531}' :: INT [])
		--'BAWithDraw' AND 'BAWithdrawDetail'

		THEN
			INSERT INTO TMP_KET_QUA
				SELECT
					SV."id"
					, 'account.ex.phieu.thu.chi'       AS "MODEL_CHUNG_TU"
					, SV."LOAI_CHUNG_TU"

					, SV."NGAY_CHUNG_TU"
					, -- Phần đề nghị ghi nợ TK
					BA."SO_TAI_KHOAN"
					, SV."TEN_TK_CHI"
					, BA."CHI_NHANH"
					, B."TEN_DAY_DU"                   AS "TEN_NGAN_HANG_DI"
					, /*TienHM thi công 109005 bổ sung Tên Ngân hàng lấy từ danh mục TK Ngân hàng phục vụ Mẫu của BIDV*/
					BA."CHU_TAI_KHOAN"

					, -- Ghi có TK
					SV."TAI_KHOAN_NHAN_UNC_NOP_TIEN"
					, SV."TEN_DOI_TUONG"
					, SV."DIA_CHI"
					, A."DIA_CHI"                      AS "DIA_CHI_DOI_TUONG_DI"
					, /*nhyen - 6/10/2017 (Bug148005): Địa chỉ đối tượng nhận trong danh mục */
					SV."TEN_TK_NHAN"
					, ABA."CHI_NHANH"

					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN NULL
					  ELSE A."SO_CMND"
					  END                              AS "SO_CMND"
					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN NULL
					  ELSE A."NGAY_CAP"
					  END                              AS "NGAY_CMND"
					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN NULL
					  ELSE A."NOI_CAP"
					  END                              AS "NOI_CAP_CMND"
					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN A."DIEN_THOAI"
					  ELSE A."DT_DI_DONG"
					  END
					, SV."DIEN_GIAI"
					, (SELECT "MA_LOAI_TIEN"
					   FROM res_currency TK
					   WHERE TK.id = SV."currency_id") AS "LOAI_TIEN"
					, CASE WHEN (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = SVD."TK_CO_ID") LIKE '112%%' --AND SVD."TK_CO" NOT LIKE '112%%'
					THEN SVD."SO_TIEN"
					  ELSE 0
					  END - CASE WHEN (SELECT "SO_TAI_KHOAN"
									   FROM danh_muc_he_thong_tai_khoan TK
									   WHERE TK.id = SVD."TK_NO_ID") LIKE '112%%'
									  AND (SELECT "SO_TAI_KHOAN"
										   FROM danh_muc_he_thong_tai_khoan TK
										   WHERE TK.id = SVD."TK_CO_ID") NOT LIKE '112%%'
					THEN SVD."SO_TIEN"
							ELSE 0
							END + CASE WHEN (SELECT "SO_TAI_KHOAN"
											 FROM danh_muc_he_thong_tai_khoan TK
											 WHERE TK.id = SVD."TK_CO_ID") LIKE '311%%'
					THEN SVD."SO_TIEN"
								  ELSE 0
								  END + CASE --hhson
										WHEN (SELECT "SO_TAI_KHOAN"
											  FROM danh_muc_he_thong_tai_khoan TK
											  WHERE TK.id = SVD."TK_CO_ID") LIKE '341%%'
											THEN SVD."SO_TIEN"
										ELSE 0
										END            AS "TONG_TIEN"

					, --Các trường bổ sung cho giống mẫu UNC 2012
					SV."SO_CHUNG_TU"
					, SV."NGAY_HACH_TOAN"
					, OU."MA_DON_VI"                   AS "MA_CHI_NHANH"
					, BA."SO_TAI_KHOAN"
					, BA."CHI_NHANH"
					, BA."DIA_CHI_CN"
					, BA."DIA_CHI_CN"
					, BA."CHI_NHANH"
					, A."MA"
					, SV."TY_GIA"
					, SV."SO_TIEN_TREE"
					, (SELECT "SO_TAI_KHOAN"
					   FROM danh_muc_he_thong_tai_khoan TK
					   WHERE TK.id = SVD."TK_NO_ID")
					, (SELECT "SO_TAI_KHOAN"
					   FROM danh_muc_he_thong_tai_khoan TK
					   WHERE TK.id = SVD."TK_CO_ID")
					, SVD."DIEN_GIAI_DETAIL"
					, SVD."SO_TIEN_QUY_DOI"
					, SVD."SO_TIEN"
					, P."STT"
                    ,SVD."THU_TU_SAP_XEP_CHI_TIET"

				FROM account_ex_phieu_thu_chi SV
					INNER JOIN account_ex_phieu_thu_chi_tiet SVD ON SV."id" = SVD."PHIEU_THU_CHI_ID"
					INNER JOIN TMP_PARAM P ON SV."id" = P."ID_CHUNG_TU"
					LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = SV."TAI_KHOAN_CHI_GUI_ID"
					LEFT JOIN res_partner A ON SV."DOI_TUONG_ID" = A."id"
					LEFT JOIN (SELECT
								   "DOI_TUONG_ID"
								   , "SO_TAI_KHOAN"
								   , "CHI_NHANH"
								   , "TINH_TP_CUA_NGAN_HANG"
								   , ROW_NUMBER()
									 OVER (
										 PARTITION BY "DOI_TUONG_ID",
											 "SO_TAI_KHOAN"
										 ORDER BY "CHI_NHANH" ) AS RowNum
							   FROM danh_muc_doi_tuong_chi_tiet
							  ) ABA ON A."id" = ABA."DOI_TUONG_ID"
									   AND SV."TAI_KHOAN_NHAN_UNC_NOP_TIEN" = ABA."SO_TAI_KHOAN"
									   AND ABA.RowNum = 1
					LEFT JOIN danh_muc_to_chuc OU ON BA."CHI_NHANH_2" = OU."id"

					LEFT JOIN danh_muc_ngan_hang B ON B."id" = BA."NGAN_HANG_ID"
			WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND P."LOAI_CHUNG_TU" =rec."LOAI_CHUNG_TU"
			;
		END IF
	;


--         IF rec."LOAI_CHUNG_TU" = ANY
--            ('{1512,1513}' :: INT [])--'BAWithDraw' AND  BAWithdrawDetailTax
--         THEN
--
--             INSERT INTO TMP_KET_QUA
--                 SELECT
--                     SV."id"
--                     , 'account.ex.phieu.thu.chi'       AS "MODEL_CHUNG_TU"
--                     , SV."LOAI_CHUNG_TU"
--
--                     , SV."NGAY_CHUNG_TU"
--                     , -- Phần đề nghị ghi nợ TK
--                     BA."SO_TAI_KHOAN"
--                     , SV."TEN_TK_CHI"
--                     , BA."CHI_NHANH"
--                     , B."TEN_DAY_DU"                   AS "TEN_NGAN_HANG_DI"
--                     , /*TienHM thi công 109005 bổ sung Tên Ngân hàng lấy từ danh mục TK Ngân hàng phục vụ Mẫu của BIDV*/
--                     BA."CHU_TAI_KHOAN"
--
--                     , -- Ghi có TK
--                     SV."TAI_KHOAN_NHAN_UNC_NOP_TIEN"
--                     , SV."TEN_DOI_TUONG"
--                     , SV."DIA_CHI"
--                     , A."DIA_CHI"                      AS "DIA_CHI_DOI_TUONG_DI"
--                     , /*nhyen - 6/10/2017 (Bug148005): Địa chỉ đối tượng nhận trong danh mục */
--                     SV."TEN_TK_NHAN"
--                     , ABA."CHI_NHANH"
--
--                     , CASE WHEN A."LOAI_KHACH_HANG" = '0'
--                     THEN NULL
--                       ELSE A."SO_CMND"
--                       END                              AS "SO_CMND"
--                     , CASE WHEN A."LOAI_KHACH_HANG" = '0'
--                     THEN NULL
--                       ELSE A."NGAY_CAP"
--                       END                              AS "NGAY_CMND"
--                     , CASE WHEN A."LOAI_KHACH_HANG" = '0'
--                     THEN NULL
--                       ELSE A."NOI_CAP"
--                       END                              AS "NOI_CAP_CMND"
--                     , CASE WHEN A."LOAI_KHACH_HANG" = '0'
--                     THEN A."DIEN_THOAI"
--                       ELSE A."DT_DI_DONG"
--                       END
--                     , SV."DIEN_GIAI"
--                     , (SELECT "MA_LOAI_TIEN"
--                        FROM res_currency TK
--                        WHERE TK.id = SV."currency_id") AS "LOAI_TIEN"
--                     , SVD."SO_TIEN_QUY_DOI"            AS "SO_TIEN"
--                     , --Các trường bổ sung cho giống mẫu UNC 2012
--                     SV."SO_CHUNG_TU"
--                     , SV."NGAY_HACH_TOAN"
--                     , OU."MA_DON_VI"                   AS "MA_CHI_NHANH"
--                     , BA."SO_TAI_KHOAN"
--                     , BA."CHI_NHANH"
--                     , BA."DIA_CHI_CN"
--                     , BA."DIA_CHI_CN"
--                     , BA."CHI_NHANH"
--                     , A."MA"
--                     , SV."TY_GIA"
--                     , SV."SO_TIEN_TREE"
--                     , (SELECT "SO_TAI_KHOAN"
--                        FROM danh_muc_he_thong_tai_khoan TK
--                        WHERE TK.id = SVD."TK_NO_ID")
--                     , (SELECT "SO_TAI_KHOAN"
--                        FROM danh_muc_he_thong_tai_khoan TK
--                        WHERE TK.id = SVD."TK_CO_ID")
--                     , SVD."DIEN_GIAI_DETAIL"
--                     , SVD."SO_TIEN_QUY_DOI"
--                     , SVD."SO_TIEN"
--
--
--                 FROM account_ex_phieu_thu_chi SV
--                     INNER JOIN account_ex_phieu_thu_chi_tiet SVD ON SV."id" = SVD."PHIEU_THU_CHI_ID"
--                     INNER JOIN TMP_PARAM P ON SV."id" = P."ID_CHUNG_TU"
--                     LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = SV."TAI_KHOAN_CHI_GUI_ID"
--                     LEFT JOIN res_partner A ON SV."DOI_TUONG_ID" = A."id"
--                     LEFT JOIN (SELECT
--                                    "DOI_TUONG_ID"
--                                    , "SO_TAI_KHOAN"
--                                    , "CHI_NHANH"
--                                    , "TINH_TP_CUA_NGAN_HANG"
--                                    , ROW_NUMBER()
--                                      OVER (
--                                          PARTITION BY "DOI_TUONG_ID",
--                                              "SO_TAI_KHOAN"
--                                          ORDER BY "CHI_NHANH" ) AS RowNum
--                                FROM danh_muc_doi_tuong_chi_tiet
--                               ) ABA ON A."id" = ABA."DOI_TUONG_ID"
--                                        AND SV."TAI_KHOAN_NHAN_UNC_NOP_TIEN" = ABA."CHI_NHANH"
--                                        AND ABA.RowNum = 1
--                     LEFT JOIN danh_muc_to_chuc OU ON BA."CHI_NHANH_2" = OU."id"
--
--                     LEFT JOIN danh_muc_ngan_hang B ON B."id" = BA."NGAN_HANG_ID"
--             WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND P."LOAI_CHUNG_TU" =rec."LOAI_CHUNG_TU"
--             ;
--         END IF
--     ;


		IF rec."LOAI_CHUNG_TU" = ANY ('{1560}' :: INT [])--'BAInternalTransfer'
		THEN
			INSERT INTO TMP_KET_QUA
				SELECT
					SV."id"
					, 'account.ex.phieu.thu.chi'       AS "MODEL_CHUNG_TU"
					, SV."LOAI_CHUNG_TU"

					, SV."NGAY_CHUNG_TU"
					, -- Phần đề nghị ghi nợ TK
					BA."SO_TAI_KHOAN"
					, SV."TEN_TK_CHI"
					, BA."CHI_NHANH"
					, B."TEN_DAY_DU"                   AS "TEN_NGAN_HANG_DI"
					, BA."CHU_TAI_KHOAN"

					, -- Ghi có TK
					BA2."SO_TAI_KHOAN"
					, NULL                             AS "TEN_DOI_TUONG"
					, NULL                             AS "DIA_CHI_DOI_TUONG"
					, NULL                             AS "DIA_CHI_DOI_TUONG_DI"
					, SV."TEN_TK_NHAN_CTNB"
					, BA2."CHI_NHANH"
					, NULL                             AS "SO_CMND"
					, NULL                             AS "NGAY_CMND"
					, NULL                             AS "NOI_CAP_CMND"
					, OU."DIEN_THOAI"                  AS "SO_DIEN_THOAI"
					, --NVTOAN modify 10/07/2017
					SV."DIEN_GIAI"
					, (SELECT "MA_LOAI_TIEN"
					   FROM res_currency TK
					   WHERE TK.id = SV."currency_id") AS "LOAI_TIEN"
					, CASE WHEN (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = SVD."TK_CO_ID") LIKE '112%%'
								OR (SELECT "SO_TAI_KHOAN"
									FROM danh_muc_he_thong_tai_khoan TK
									WHERE TK.id = SVD."TK_CO_ID") LIKE '311%%'
								OR (SELECT "SO_TAI_KHOAN"
									FROM danh_muc_he_thong_tai_khoan TK
									WHERE TK.id = SVD."TK_CO_ID") LIKE '341%%'
					THEN SVD."SO_TIEN"
					  WHEN (SELECT "SO_TAI_KHOAN"
							FROM danh_muc_he_thong_tai_khoan TK
							WHERE TK.id = SVD."TK_NO_ID") LIKE '112%%'
						   AND (SELECT "SO_TAI_KHOAN"
								FROM danh_muc_he_thong_tai_khoan TK
								WHERE TK.id = SVD."TK_CO_ID") NOT LIKE '112%%'
						  THEN -(SVD."SO_TIEN")
					  ELSE 0
					  END                              AS "TONG_TIEN"

					, --Các trường bổ sung cho giống mẫu UNC 2012

					SV."SO_CHUNG_TU"
					, SV."NGAY_HACH_TOAN"
					, OU."MA_DON_VI"                   AS "MA_CHI_NHANH"
					, BA."SO_TAI_KHOAN"
					, BA."CHI_NHANH"
					, BA."DIA_CHI_CN"
					, BA."DIA_CHI_CN"
					, BA."CHI_NHANH"
					, NULL                             AS "MA_KHACH_HANG"

					, SV."TY_GIA"
					, SV."SO_TIEN_TREE"                AS "TONG_TIEN_QUY_DOI"
					, (SELECT "SO_TAI_KHOAN"
					   FROM danh_muc_he_thong_tai_khoan TK
					   WHERE TK.id = SVD."TK_NO_ID")
					, (SELECT "SO_TAI_KHOAN"
					   FROM danh_muc_he_thong_tai_khoan TK
					   WHERE TK.id = SVD."TK_CO_ID")
					, SVD."DIEN_GIAI_DETAIL"
					, SVD."SO_TIEN_QUY_DOI"
					, SVD."SO_TIEN"
					, P."STT"
                	,SVD."THU_TU_SAP_XEP_CHI_TIET"


				FROM account_ex_phieu_thu_chi SV
					INNER JOIN account_ex_phieu_thu_chi_tiet SVD ON SV."id" = SVD."PHIEU_THU_CHI_ID"
					INNER JOIN TMP_PARAM P ON SV."id" = P."ID_CHUNG_TU"
					LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = SV."TAI_KHOAN_CHI_GUI_ID"
					LEFT JOIN danh_muc_tai_khoan_ngan_hang BA2 ON BA2."id" = SV."TAI_KHOAN_DEN_ID"
					LEFT JOIN danh_muc_to_chuc OU ON BA."CHI_NHANH_2" = OU."id"

					LEFT JOIN danh_muc_ngan_hang B ON B."id" = BA."NGAN_HANG_ID"
			WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND P."LOAI_CHUNG_TU" =rec."LOAI_CHUNG_TU"
			;


		END IF
	;


		IF rec."LOAI_CHUNG_TU" = ANY
		   ('{4010,4011,4012,4013,4014,4015,4016,4017,4018,4020,4030}' :: INT [])  --'GLVoucher'
		THEN
			-- nmtruong 11/9/2015 lấy theo tài khoản ngân hàng đầu tiên
			DROP TABLE IF EXISTS TMP_THONG_TIN_MASTER
			;

			CREATE TEMP TABLE TMP_THONG_TIN_MASTER

			(
				"ID_CHUNG_TU"                   INT PRIMARY KEY,
				"DOI_TUONG_ID"                  INT,
				"TK_NGAN_HANG_ID"               INT,
				"SO_TAI_KHOAN_NGAN_HANG_DT_NO"  VARCHAR(100),
				"TEN_TAI_KHOAN_NGAN_HANG_DT_NO" VARCHAR(255),
				"CHI_NHANH_NGAN_HANG"           VARCHAR(255),
				"TINH_THANH_PHO"                VARCHAR(255),
				"STT"                           INT
			)
			;

			-- TTHOA 24/11/2016: Lấy thông tin theo dòng đầu tiên có chọn tài khoản ngân hàng
			-- (Thay đổi theo tài liệu khi làm CR 18984)
			INSERT INTO TMP_THONG_TIN_MASTER
				SELECT
					GLD."ID_CHUNG_TU"
					, GLD."DOI_TUONG_NO_ID"
					, GLD."TK_NGAN_HANG_ID"
					, GLD."SO_TAI_KHOAN_NGAN_HANG_DT_NO"
					, GLD."TEN_TAI_KHOAN_NGAN_HANG_DT_NO"
					, AOB."CHI_NHANH"
					, AOB."TINH_TP_CUA_NGAN_HANG"
					, GLD."MasterSortOrder"
				FROM (SELECT
						  P."ID_CHUNG_TU"
						  , D."DOI_TUONG_NO_ID"
						  , D."TK_NGAN_HANG_ID"
						  , D."SO_TAI_KHOAN_NGAN_HANG_DT_NO"
						  , D."TEN_TAI_KHOAN_NGAN_HANG_DT_NO"
						  , ROW_NUMBER()
							OVER (
								PARTITION BY P."ID_CHUNG_TU"
								ORDER BY D."THU_TU_SAP_XEP_CHI_TIET" ) AS "RowID"
						  , P."STT"                                    AS "MasterSortOrder"
					  FROM TMP_PARAM P
						  LEFT JOIN account_ex_chung_tu_nghiep_vu_khac_hach_toan D
							  ON D."CHUNG_TU_NGHIEP_VU_KHAC_ID" = P."ID_CHUNG_TU"
								 AND D."TK_NGAN_HANG_ID" IS NOT NULL
					 ) AS GLD
					LEFT JOIN danh_muc_doi_tuong_chi_tiet AOB ON GLD."DOI_TUONG_NO_ID" = AOB."DOI_TUONG_ID"
																 AND
																 GLD."SO_TAI_KHOAN_NGAN_HANG_DT_NO" = AOB."SO_TAI_KHOAN"
				WHERE GLD."RowID" = 1
			;

			INSERT INTO TMP_KET_QUA
				SELECT
					SV."id"
					, 'account.ex.chung.tu.nghiep.vu.khac' AS "MODEL_CHUNG_TU"
					, SV."LOAI_CHUNG_TU"

					, SV."NGAY_CHUNG_TU"
					, BA."SO_TAI_KHOAN"
					, B."TEN_DAY_DU" || CASE WHEN BA."CHI_NHANH" IS NOT NULL
												  AND LTRIM(BA."CHI_NHANH") <> ''
					THEN' - ' || BA."CHI_NHANH"
										ELSE ''
										END
					, BA."CHI_NHANH"
					, B."TEN_DAY_DU"                       AS "TEN_NGAN_HANG_DI"
					, BA."CHU_TAI_KHOAN"

					, P."SO_TAI_KHOAN_NGAN_HANG_DT_NO"
					, A."HO_VA_TEN"
					, A."DIA_CHI"                          AS "DIA_CHI_DOI_TUONG"
					, A."DIA_CHI"                          AS "DIA_CHI_DOI_TUONG_DI"
					, P."TEN_TAI_KHOAN_NGAN_HANG_DT_NO"
					, P."CHI_NHANH_NGAN_HANG"

					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN NULL
					  ELSE A."SO_CMND"
					  END                                  AS "SO_CMND"
					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN NULL
					  ELSE A."NGAY_CAP"
					  END                                  AS "NGAY_CMND"
					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN NULL
					  ELSE A."NOI_CAP"
					  END                                  AS "NOI_CAP_CMND"
					, CASE WHEN A."LOAI_KHACH_HANG" = '0'
					THEN A."DIEN_THOAI"
					  ELSE A."DT_DI_DONG"
					  END                                  AS "SO_DIEN_THOAI"
					, SV."DIEN_GIAI"
					, (SELECT "MA_LOAI_TIEN"
					   FROM res_currency TK
					   WHERE TK.id = SV."currency_id")     AS "LOAI_TIEN"
					, CASE WHEN (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = SVD."TK_CO_ID") LIKE '112%%'
								OR (SELECT "SO_TAI_KHOAN"
									FROM danh_muc_he_thong_tai_khoan TK
									WHERE TK.id = SVD."TK_CO_ID") LIKE '311%%'
								OR (SELECT "SO_TAI_KHOAN"
									FROM danh_muc_he_thong_tai_khoan TK
									WHERE TK.id = SVD."TK_CO_ID") LIKE '341%%'
					THEN SVD."SO_TIEN"
					  WHEN (SELECT "SO_TAI_KHOAN"
							FROM danh_muc_he_thong_tai_khoan TK
							WHERE TK.id = SVD."TK_NO_ID") LIKE '112%%'
						   AND (SELECT "SO_TAI_KHOAN"
								FROM danh_muc_he_thong_tai_khoan TK
								WHERE TK.id = SVD."TK_CO_ID") NOT LIKE '112%%'
						  THEN -SVD."SO_TIEN"
					  ELSE 0
					  END                                  AS "TONG_TIEN"

					, SV."SO_CHUNG_TU"
					, SV."NGAY_HACH_TOAN"
					, OU."MA_DON_VI"                       AS "MA_CHI_NHANH"
					, BA."SO_TAI_KHOAN"
					, BA."CHI_NHANH"
					, BA."DIA_CHI_CN"
					, BA."DIA_CHI_CN"
					, BA."CHI_NHANH"
					, A."MA"

					, SV."TY_GIA"
					, CASE WHEN (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = SVD."TK_CO_ID") LIKE '112%%'
								OR (SELECT "SO_TAI_KHOAN"
									FROM danh_muc_he_thong_tai_khoan TK
									WHERE TK.id = SVD."TK_CO_ID") LIKE '311%%'
								OR (SELECT "SO_TAI_KHOAN"
									FROM danh_muc_he_thong_tai_khoan TK
									WHERE TK.id = SVD."TK_CO_ID") LIKE '341%%'
					THEN SVD."SO_TIEN_QUY_DOI"
					  WHEN (SELECT "SO_TAI_KHOAN"
							FROM danh_muc_he_thong_tai_khoan TK
							WHERE TK.id = SVD."TK_NO_ID") LIKE '112%%'
						   AND (SELECT "SO_TAI_KHOAN"
								FROM danh_muc_he_thong_tai_khoan TK
								WHERE TK.id = SVD."TK_CO_ID") NOT LIKE '112%%'
						  THEN -SVD."SO_TIEN_QUY_DOI"
					  ELSE 0
					  END                                  AS "TONG_TIEN_QUY_DOI"
					, (SELECT "SO_TAI_KHOAN"
					   FROM danh_muc_he_thong_tai_khoan TK
					   WHERE TK.id = SVD."TK_NO_ID")
					, (SELECT "SO_TAI_KHOAN"
					   FROM danh_muc_he_thong_tai_khoan TK
					   WHERE TK.id = SVD."TK_CO_ID")
					, SVD."DIEN_GIAI"
					, SVD."SO_TIEN_QUY_DOI"
					, SVD."SO_TIEN"
					 , P."STT"
                	,SVD."THU_TU_SAP_XEP_CHI_TIET"


				FROM account_ex_chung_tu_nghiep_vu_khac SV
					INNER JOIN TMP_THONG_TIN_MASTER P ON SV."id" = P."ID_CHUNG_TU"
					INNER JOIN account_ex_chung_tu_nghiep_vu_khac_hach_toan SVD
						ON P."ID_CHUNG_TU" = SVD."CHUNG_TU_NGHIEP_VU_KHAC_ID"

						   -- (Thay đổi theo tài liệu khi làm CR 18984)
						   AND ((P."TK_NGAN_HANG_ID" = SVD."TK_NGAN_HANG_ID"
								 OR P."TK_NGAN_HANG_ID" IS NULL
								)
								AND (P."DOI_TUONG_ID" = SVD."DOI_TUONG_NO_ID"
									 OR (P."DOI_TUONG_ID" IS NULL
										 AND SVD."DOI_TUONG_NO_ID" IS NULL
									 )
								)
						   )
					LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = SVD."TK_NGAN_HANG_ID"
					LEFT JOIN danh_muc_ngan_hang B ON BA."NGAN_HANG_ID" = B."id"
					LEFT JOIN res_partner A ON P."DOI_TUONG_ID" = A."id"
					LEFT JOIN danh_muc_to_chuc OU ON BA."CHI_NHANH_2" = OU."id"
			;

		END IF
	;

	END LOOP
	;


	UPDATE TMP_KET_QUA R1
	SET "TONG_TIEN_QUY_DOI" = R2."TONG_TIEN_QUY_DOI",
		"TONG_TIEN"         = R2."TONG_TIEN"
	FROM
		(SELECT
			 "ID_CHUNG_TU"
			,"LOAI_CHUNG_TU"
			 , SUM(CASE WHEN "TK_CO" LIKE '112%%'
							 OR "TK_CO" LIKE '311%%'
							 OR "TK_CO" LIKE '341%%'
				THEN "THANH_TIEN_QUY_DOI"
				   ELSE 0
				   END - CASE WHEN "TK_NO" LIKE '112%%'
								   AND "TK_CO" NOT LIKE '112%%'
				THEN "THANH_TIEN_QUY_DOI"
						 ELSE 0
						 END) AS "TONG_TIEN_QUY_DOI"
			 , SUM(CASE WHEN "TK_CO" LIKE '112%%'
							 OR "TK_CO" LIKE '311%%'
							 OR "TK_CO" LIKE '341%%'
				THEN "THANH_TIEN"
				   ELSE 0
				   END - CASE WHEN "TK_NO" LIKE '112%%'
								   AND "TK_CO" NOT LIKE '112%%'
				THEN "THANH_TIEN"
						 ELSE 0
						 END) AS "TONG_TIEN"
		 FROM TMP_KET_QUA
		 GROUP BY
			 "ID_CHUNG_TU",
			 "LOAI_CHUNG_TU"
		) R2
	WHERE R1."ID_CHUNG_TU" = R2."ID_CHUNG_TU" AND R1."LOAI_CHUNG_TU" = R2."LOAI_CHUNG_TU"

	;


	UPDATE TMP_KET_QUA
	SET "THANH_TIEN_QUY_DOI" = (CASE WHEN "TK_CO" LIKE '112%%'
										  OR "TK_CO" LIKE '311%%'
										  OR "TK_CO" LIKE '341%%'
		THEN "THANH_TIEN_QUY_DOI"
								ELSE 0
								END - CASE WHEN "TK_NO" LIKE '112%%'
												AND "TK_CO" NOT LIKE '112%%'
		THEN "THANH_TIEN_QUY_DOI"
									  ELSE 0
									  END),
		"THANH_TIEN"         = (CASE WHEN "TK_CO" LIKE '112%%'
										  OR "TK_CO" LIKE '311%%'
										  OR "TK_CO" LIKE '341%%'
			THEN "THANH_TIEN"
								ELSE 0
								END - CASE WHEN "TK_NO" LIKE '112%%'
												AND "TK_CO" NOT LIKE '112%%'
			THEN "THANH_TIEN"
									  ELSE 0
									  END)
	;


END $$

;

SELECT *
FROM TMP_KET_QUA 
ORDER BY
                "SortOrder" ,
                "SortOrderDetail";
		"""
		return self.execute(query) 