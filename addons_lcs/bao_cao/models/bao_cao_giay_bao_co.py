# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_GIAY_BAO_CO(models.Model):
	_name = 'bao.cao.giay.bao.co'
	_auto = False

	ref = fields.Char(string='Reffence ID')

	ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
	MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')

	STK_TAI_KHOAN_NGAN_HANG = fields.Char(string='Số tài khoản ngân hàng') #BankAccount
	TEN_NGAN_HANG = fields.Char(string='Tên ngân hàng')#BankName
	
	NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ') #RefDate
	NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán') #PostedDate
	
	SO_CHUNG_TU = fields.Char(string='Số chứng từ') #RefNo
	MA_KHACH_HANG = fields.Char(string='Mã khách hàng') #AccountObjectCode
	TEN_KHACH_HANG = fields.Char(string='Tên khách hàng') #AccountObjectName

	DIA_CHI = fields.Char(string='Địa chỉ') #AccountObjectAddress
	DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải') #JournalMemo
	TONG_TIEN = fields.Monetary(string='Tổng tiền', currency_field='currency_id') #TotalAmountOC
	TONG_TIEN_QUY_DOI = fields.Monetary(string='Tổng tiền quy đổi', currency_field='currency_id') #TotalAmount
	TK_CONG_NO = fields.Char(string='TK công nợ') #AccountNumber

	LOAI_TIEN = fields.Char(string='Loại tiền') #CurrencyID
	TY_GIA = fields.Monetary(string='Tỷ giá', currency_field='currency_id') #ExchangeRate

	MasterSortOrder = fields.Integer(string='MasterSortOrder') #MasterSortOrder
	

	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
	

	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())

	ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.giay.bao.co.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')



class BAO_CAO_GIAY_BAO_CO_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_creditannouncement'

	@api.model
	def get_report_values(self, docids, data=None):
		############### START SQL lấy dữ liệu ###############
		refTypeList, records = self.get_reftype_list(data)
		sql_result = self.ham_lay_du_lieu_sql_tra_ve(refTypeList)

		for line in sql_result:
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
			master_data = self.env['bao.cao.giay.bao.co'].convert_for_update(line)
			detail_data = self.env['bao.cao.giay.bao.co.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
				records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.giay.bao.co.chi.tiet'].new(detail_data)
		
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

ListParam VARCHAR := N'""" + refTypeList + """';

rec       RECORD;


BEGIN


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
        "ID_CHUNG_TU"             INT
        ,
        "MODEL_CHUNG_TU"          VARCHAR(255)
        ,
        "LOAI_CHUNG_TU"           INT
        ,
        "NGAY_CHUNG_TU"           TIMESTAMP
        ,
        "NGAY_HACH_TOAN"          TIMESTAMP
        ,
        "SO_CHUNG_TU"             VARCHAR(255)
        ,
        "MA_KHACH_HANG"           VARCHAR(127)
        ,
        "TEN_KHACH_HANG"          VARCHAR(255)
        ,
        "DIA_CHI"                 VARCHAR(255)
        ,
        "DIEN_GIAI"               VARCHAR(255)
        ,
        "TONG_TIEN"               DECIMAL(25, 8)
        ,
        "TONG_TIEN_QUY_DOI"       DECIMAL(25, 8)
        ,
        "THANH_TIEN"              DECIMAL(25, 8)
        ,
        "THANH_TIEN_QUY_DOI"      DECIMAL(25, 8)
        ,
        "DIEN_GIAI_DETAIL"        VARCHAR(255)
        ,
        "TK_NO"                   VARCHAR(255)
        ,
        "TK_CO"                   VARCHAR(255)
        ,
        "TK_CONG_NO"              VARCHAR(255)

        ,
        "TY_GIA"                  DECIMAL(25, 8)
        ,
        "LOAI_TIEN"               VARCHAR(15)

        ,
        "STK_TAI_KHOAN_NGAN_HANG" VARCHAR(127)
        ,
        "TEN_NGAN_HANG"           VARCHAR(255)

        ,
        "MasterSortOrder"         INT
        ,
        "STT"                     INT
        ,
        "RowOrder"                  INT
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


        IF rec."LOAI_CHUNG_TU" = ANY
           ('{3530,3531,3532,3534,3535,3536,3537,3538}' :: INT [])--  '"sale_document"'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    SA."id"
                    , --"ID_CHUNG_TU" INT
                      'sale.document'                                                                 AS "MODEL_CHUNG_TU"
                    , SA."LOAI_CHUNG_TU"
                    , --,"LOAI_CHUNG_TU" INT
                    SA."NGAY_CHUNG_TU"
                    , --,"NGAY_CHUNG_TU" TIMESTAMP
                    SA."NGAY_HACH_TOAN"
                    , --,"NGAY_HACH_TOAN" TIMESTAMP
                    SA."SO_CHUNG_TU"
                    , --,"SO_CHUNG_TU" VARCHAR(255)
                      AO."MA"                                                                        AS "MA_KHACH_HANG"
                    , --,"MA_KHACH_HANG"  VARCHAR(127)
                    SA."TEN_KHACH_HANG"
                    , --,"TEN_KHACH_HANG"  VARCHAR(255)
                    SA."DIA_CHI"
                    , --,"DIA_CHI" VARCHAR(255)
                    SA."DIEN_GIAI"
                    , --,"DIEN_GIAI"  VARCHAR(255)
                    SA."TONG_TIEN_THANH_TOAN"
                    , --,"TONG_TIEN" DECIMAL(25,8)
                    SA."TONG_TIEN_THANH_TOAN_QĐ"
                    , --,"PHAT_SINH_TRONG_KY_TONG" DECIMAL(25,8)
                      SAD."THANH_TIEN"
                      + CASE WHEN SAD."TK_THUE_GTGT_ID" IS NULL
                          THEN SAD."TIEN_THUE_GTGT"
                        ELSE 0 END
                      - CASE WHEN SA."LOAI_CHUNG_TU" = 3538
                          THEN SAD."TIEN_CHIET_KHAU"
                        ELSE 0 END                                                                   AS "THANH_TIEN"
                    , --,"THANH_TIEN" DECIMAL(25,8)
                    SAD."THANH_TIEN_QUY_DOI"
                    + CASE WHEN SAD."TK_THUE_GTGT_ID" IS NULL
                        THEN SAD."TIEN_THUE_GTGT_QUY_DOI"
                      ELSE 0 END
                    - CASE WHEN SA."LOAI_CHUNG_TU" = 3538
                        THEN SAD."TIEN_CK_QUY_DOI"
                      ELSE 0 END
                    , --,"SO_TIEN" DECIMAL(25,8)
                    SAD."TEN_HANG"
                    , --,["DIEN_GIAI"]  VARCHAR(255)
                      (SELECT TK."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SAD."TK_NO_ID")                                                 AS "TK_NO"
                    , --,"TK_NO"  VARCHAR(255)
                      (SELECT TK."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SAD."TK_CO_ID")                                                 AS "TK_CO"
                    , --,"TK_CO"  VARCHAR(255)
                      LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_CHUNG_TU_BAN_HANG(SA."id", '112') AS "TK_CONG_NO"

                    , --,"TK_THUE_GTGT"Attach VARCHAR(255)
                    SA."TY_GIA"
                    , --,"TY_GIA" DECIMAL(25,8)
                      (SELECT TK."MA_LOAI_TIEN"
                       FROM res_currency TK
                       WHERE TK.id = SA."currency_id")                                               AS "LOAI_TIEN"


                    , --,CurrencyName VARCHAR(255)
                    BA."SO_TAI_KHOAN"
                    , --,"TAI_KHOAN_NGAN_HANG"  VARCHAR(127)
                    SA."TEN_TK"

                    --,IsNotGetParameter BIT
                    , R."MasterSortOrder"
                    --,Master"STT" INT
                    , SAD."THU_TU_SAP_XEP_CHI_TIET"                                                  AS "STT"
                    --,"STT" INT
                    ,
                      0                                                                              AS "RowOrder" --,RowOrder INT
                FROM sale_document SA
                    INNER JOIN TMP_ID_CHUNG_TU R ON R."ID_CHUNG_TU" = SA."id"
                    INNER JOIN sale_document_line SAD ON SA."id" = SAD."SALE_DOCUMENT_ID"
                    LEFT JOIN res_partner AO ON SA."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_currency ON SA."currency_id" = res_currency."id"
                    LEFT JOIN res_partner AS Employee ON (SA."NHAN_VIEN_ID" = Employee."id"
                                                          AND Employee."LA_NHAN_VIEN" = TRUE
                        )

                    LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = SA."NOP_VAO_TK_ID"
                     WHERE R."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      R."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"

                --Tách riêng các dòng chiết khấu
                UNION ALL
                SELECT
                    SA."id"
                    , --"ID_CHUNG_TU" INT
                      'sale.document'                                                                AS "MODEL_CHUNG_TU"
                    , SA."LOAI_CHUNG_TU"
                    , --,"LOAI_CHUNG_TU" INT
                    SA."NGAY_CHUNG_TU"
                    , --,"NGAY_CHUNG_TU" TIMESTAMP
                    SA."NGAY_HACH_TOAN"
                    , --,"NGAY_HACH_TOAN" TIMESTAMP
                    SA."SO_CHUNG_TU"
                    , --,"SO_CHUNG_TU" VARCHAR(255)
                      AO."MA"                                                                        AS "MA_KHACH_HANG"
                    , --,"MA_KHACH_HANG"  VARCHAR(127)
                    SA."TEN_KHACH_HANG"
                    , --,"TEN_KHACH_HANG"  VARCHAR(255)
                    SA."DIA_CHI"
                    , --,"DIA_CHI" VARCHAR(255)
                    SA."DIEN_GIAI"
                    , --,"DIEN_GIAI"  VARCHAR(255)
                    SA."TONG_TIEN_THANH_TOAN"
                    , --,"TONG_TIEN" DECIMAL(25,8)
                    SA."TONG_TIEN_THANH_TOAN_QĐ"
                    , --,"PHAT_SINH_TRONG_KY_TONG" DECIMAL(25,8)
                      SAD."TIEN_CHIET_KHAU"                                                          AS "THANH_TIEN"
                    , --,"THANH_TIEN" DECIMAL(25,8)
                      SAD."TIEN_CK_QUY_DOI"                                                          AS "SO_TIEN"
                    , --,"SO_TIEN" DECIMAL(25,8)
                    SAD."TEN_HANG"
                    , --,["DIEN_GIAI"]  VARCHAR(255)
                      (SELECT TK."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SAD."TK_CHIET_KHAU_ID")                                         AS "TK_NO"
                    , (SELECT TK."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SAD."TK_NO_ID")                                                 AS "TK_CO"
                    , --,"TK_CO"  VARCHAR(255)
                      LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_CHUNG_TU_BAN_HANG(SA."id", '112') AS "TK_CONG_NO"

                    , --,"TK_THUE_GTGT"Attach VARCHAR(255)
                    SA."TY_GIA"
                    , --,"TY_GIA" DECIMAL(25,8)
                      (SELECT TK."MA_LOAI_TIEN"
                       FROM res_currency TK
                       WHERE TK.id = SA."currency_id")                                               AS "LOAI_TIEN"


                    , --,CurrencyName VARCHAR(255)
                    BA."SO_TAI_KHOAN"
                    , --,"TAI_KHOAN_NGAN_HANG"  VARCHAR(127)
                    SA."TEN_TK"

                    --,IsNotGetParameter BIT
                    , R."MasterSortOrder"
                    --,Master"STT" INT
                    , SAD."THU_TU_SAP_XEP_CHI_TIET"                                                  AS "STT"
                    --,"STT" INT
                    ,
                      1                                                                              AS "RowOrder" --,RowOrder INT
                FROM sale_document SA
                    INNER JOIN TMP_ID_CHUNG_TU R ON R."ID_CHUNG_TU" = SA."id"
                    INNER JOIN sale_document_line SAD ON SA."id" = SAD."SALE_DOCUMENT_ID"
                    LEFT JOIN res_partner AO ON SA."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_currency ON SA."currency_id" = res_currency."id"
                    LEFT JOIN res_partner AS Employee ON (SA."NHAN_VIEN_ID" = Employee."id"
                                                          AND Employee."LA_NHAN_VIEN" = TRUE
                        )

                    LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = SA."NOP_VAO_TK_ID"
                WHERE
                    SA."LOAI_CHUNG_TU" <> 3538 -- Nếu là bán hàng đại lý đúng giá thì không lấy lên dòng chiết khấu
                    AND SAD."TIEN_CHIET_KHAU" <> 0
                     AND R."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      R."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"

                --Nối thêm dòng thuế
                UNION ALL
                SELECT
                    SA."id"
                    , --"ID_CHUNG_TU" INT
                      'sale.document'                                                                AS "MODEL_CHUNG_TU"
                    , SA."LOAI_CHUNG_TU"
                    , --,"LOAI_CHUNG_TU" INT
                    SA."NGAY_CHUNG_TU"
                    , --,"NGAY_CHUNG_TU" TIMESTAMP
                    SA."NGAY_HACH_TOAN"
                    , --,"NGAY_HACH_TOAN" TIMESTAMP
                    SA."SO_CHUNG_TU"
                    , --,"SO_CHUNG_TU" VARCHAR(255)
                      AO."MA"                                                                        AS "MA_KHACH_HANG"
                    , --,"MA_KHACH_HANG"  VARCHAR(127)
                    SA."TEN_KHACH_HANG"
                    , --,"TEN_KHACH_HANG"  VARCHAR(255)
                    SA."DIA_CHI"
                    , --,"DIA_CHI" VARCHAR(255)
                    SA."DIEN_GIAI"
                    , --,"DIEN_GIAI"  VARCHAR(255)
                      0                                                                              AS "TONG_TIEN"
                    , --,"TONG_TIEN" DECIMAL(25,8)
                      0                                                                              AS "PHAT_SINH_TRONG_KY_TONG"
                    , --,"PHAT_SINH_TRONG_KY_TONG" DECIMAL(25,8)
                      SAD."TIEN_THUE_GTGT"                                                           AS "THANH_TIEN"
                    , --,"THANH_TIEN" DECIMAL(25,8)
                      SAD."TIEN_THUE_GTGT_QUY_DOI"                                                   AS "SO_TIEN"
                    , --,"SO_TIEN" DECIMAL(25,8)
                      danh_muc_he_thong_tai_khoan."TEN_TAI_KHOAN"                                    AS "DIEN_GIAI"
                    , --,["DIEN_GIAI"]  VARCHAR(255)
                      (SELECT TK."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SAD."TK_NO_ID")                                                 AS "TK_NO"
                    , --,"TK_NO"  VARCHAR(255)
                      (SELECT TK."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SAD."TK_THUE_GTGT_ID")                                          AS "TK_CO"
                    , --,"TK_CO"  VARCHAR(255)
                      LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_CHUNG_TU_BAN_HANG(SA."id", '112') AS "TK_CONG_NO"

                    , --,"TK_THUE_GTGT"Attach VARCHAR(255)
                    SA."TY_GIA"
                    , --,"TY_GIA" DECIMAL(25,8)
                      (SELECT TK."MA_LOAI_TIEN"
                       FROM res_currency TK
                       WHERE TK.id = SA."currency_id")                                               AS "LOAI_TIEN"

                    , --,CurrencyName VARCHAR(255)
                    BA."SO_TAI_KHOAN"
                    , --,"TAI_KHOAN_NGAN_HANG"  VARCHAR(127)
                    SA."TEN_TK"

                    , R."MasterSortOrder"
                    --,Master"STT" INT
                    , SAD."THU_TU_SAP_XEP_CHI_TIET"                                                  AS "STT"
                    --,"STT" INT
                    ,
                      2                                                                              AS "RowOrder" --,RowOrder INT
                FROM sale_document SA
                    INNER JOIN TMP_ID_CHUNG_TU R ON R."ID_CHUNG_TU" = SA."id"
                    INNER JOIN sale_document_line SAD ON SA."id" = SAD."SALE_DOCUMENT_ID"
                    LEFT JOIN res_partner AO ON SA."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_currency ON SA."currency_id" = res_currency."id"
                    LEFT JOIN res_partner AS Employee ON (SA."NHAN_VIEN_ID" = Employee."id"
                                                          AND Employee."LA_NHAN_VIEN" = TRUE
                        )

                    INNER JOIN danh_muc_he_thong_tai_khoan
                        ON (SELECT TK."SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = SAD."TK_THUE_GTGT_ID") = danh_muc_he_thong_tai_khoan."SO_TAI_KHOAN"
                    LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = SA."NOP_VAO_TK_ID"
                WHERE SAD."TK_THUE_GTGT_ID" IS NOT NULL
                     AND R."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      R."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"

                ORDER BY
                    "MasterSortOrder"
                    , "STT"
                    , "RowOrder"
            ;
        END IF
    ;

        IF rec."LOAI_CHUNG_TU" = ANY
           ('{1500,1501,1502,1503}' :: INT [])-- 'BADeposit'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    SA."id"
                    , --"ID_CHUNG_TU" INT
                      'account.ex.phieu.thu.chi'                                                                AS "MODEL_CHUNG_TU"
                  ,  SA."LOAI_CHUNG_TU"
                    , --,"LOAI_CHUNG_TU" INT
                    SA."NGAY_CHUNG_TU"
                    , --,"NGAY_CHUNG_TU" TIMESTAMP
                    SA."NGAY_HACH_TOAN"
                    , --,"NGAY_HACH_TOAN" TIMESTAMP
                   SA."SO_CHUNG_TU"
                    , --,"SO_CHUNG_TU" VARCHAR(255)
                      AO."MA"                                                                    AS "MA_KHACH_HANG"
                    , --,"MA_KHACH_HANG"  VARCHAR(127)
                    SA."TEN_DOI_TUONG"
                    , --,"TEN_KHACH_HANG"  VARCHAR(255)
                    SA."DIA_CHI"
                    , --,"DIA_CHI" VARCHAR(255)
                    SA."DIEN_GIAI"
                    , --,"DIEN_GIAI"  VARCHAR(255)
                    SA."SO_TIEN_1"
                    , --,"TONG_TIEN" DECIMAL(25,8)
                    SA."SO_TIEN_TREE"
                    , --,"PHAT_SINH_TRONG_KY_TONG" DECIMAL(25,8)
                    SAD."SO_TIEN"
                    , --,"THANH_TIEN" DECIMAL(25,8)
                    SAD."SO_TIEN_QUY_DOI"
                    , --,"SO_TIEN" DECIMAL(25,8)
                    SAD."DIEN_GIAI_DETAIL"
                    ,
                      (SELECT TK."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SAD."TK_NO_ID")                                                 AS "TK_NO"
                    ,
                      (SELECT TK."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SAD."TK_CO_ID")                                                 AS "TK_CO"
                    , --,"TK_CO"  VARCHAR(255)
                      LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_TRA_TIEN_GUI(SA."id", '112') AS "TK_CONG_NO"


                    , --,"TK_THUE_GTGT"Attach VARCHAR(255)
                    SA."TY_GIA"
                    , --,"TY_GIA" DECIMAL(25,8)
                   (SELECT TK."MA_LOAI_TIEN"
                       FROM res_currency TK
                       WHERE TK.id = SA."currency_id")                                               AS "LOAI_TIEN"
                    , --,"LOAI_TIEN" VARCHAR(15)

                    BA."SO_TAI_KHOAN"
                    , --,"TAI_KHOAN_NGAN_HANG"  VARCHAR(127)
                    SA."TEN_TK_THU"

                    , R."MasterSortOrder"
                    --,Master"STT" INT
                    , SAD."THU_TU_SAP_XEP_CHI_TIET"
                    --,"STT" INT
                    ,
                      0                                                                          AS RowOrder --,RowOrder INT
                FROM account_ex_phieu_thu_chi SA
                    INNER JOIN TMP_ID_CHUNG_TU R ON R."ID_CHUNG_TU" = SA."id"
                    INNER JOIN account_ex_phieu_thu_chi_tiet SAD ON SA."id" = SAD."PHIEU_THU_CHI_ID"
                    LEFT JOIN res_partner AO ON SA."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_currency ON SA."currency_id" = res_currency."id"
                    LEFT JOIN res_partner AS Employee ON (SA."NHAN_VIEN_ID" = Employee."id"
                                                          AND Employee."LA_NHAN_VIEN" = TRUE
                        )

            LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA."id" = SA."TAI_KHOAN_NOP_ID"
             WHERE R."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      R."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;


    END LOOP
    ;



        DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
        ;

        CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
            AS
            SELECT    *
    		  FROM      TMP_KET_QUA R
    		  ORDER BY
                            "MasterSortOrder",
    						"STT",
    						"RowOrder"
    ;


END $$

;


SELECT *
FROM TMP_KET_QUA_CUOI_CUNG
 ORDER BY
                            "MasterSortOrder",
    						"STT",
    						"RowOrder"

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

