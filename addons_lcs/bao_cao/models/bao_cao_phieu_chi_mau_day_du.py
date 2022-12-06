# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_PHIEU_CHI_MAU_DAY_DU(models.Model):
    _name = 'bao.cao.phieu.chi.mau.day.du'
    _auto = False

    ref = fields.Char(string='Reffence ID')
    ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
    MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')
    NGAY_CHUNG_TU =  fields.Date(string='Ngày chứng từ') #RefDate
    NGAY_HACH_TOAN =  fields.Date(string='Ngày hạch toán') #PostedDate
    SO_CHUNG_TU =  fields.Char(string='Số chứng từ') #RefNo
    NGUOI_NHAN_NGUOI_NOP =  fields.Char(string='Người nhận người nộp') #ContactName
    MA_KHACH_HANG =  fields.Char(string='Mã khách hàng') #AccountObjectCode
    TEN_KHACH_HANG =  fields.Char(string='Tên khách hàng') #AccountObjectName
    DIA_CHI =  fields.Char(string='Địa chỉ') #AccountObjectAddress
    DIEN_GIAI =  fields.Char(string='Diễn giải') #JournalMemo
    TK_CONG_NO = fields.Char(string='TK công nợ', help='TK công nợ')#AccountNumber
    TY_GIA = fields.Monetary(string='Tỷ giá', currency_field='currency_id')#ExchangeRate
    
    SO_CT_GOC_KEM_THEO =  fields.Integer(string='Số chứng từ kèm theo') #DocumentIncluded
    LOAI_TIEN =  fields.Char(string='Loại tiền') #CurrencyID
    TIEU_DE_COT_STNT =  fields.Char(string='Tiêu đề cột số tiền nguyên tệ')
    TIEU_DE_COT_ST =  fields.Char(string='Tiêu đề cột số tiền')

    TONG_TIEN =  fields.Monetary(string='Tổng tiền', currency_field='currency_id')

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())

    ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.phieu.chi.mau.day.du.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')



class BAO_CAO_PHIEU_CHI_MAU_DAY_DU_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_vcashpayment_full'

	@api.model
	def get_report_values(self, docids, data=None):

		refTypeList, records = self.get_reftype_list(data)
		############### START SQL lấy dữ liệu ###############
		query = """
            DO LANGUAGE plpgsql $$
DECLARE

    ListRefID                        VARCHAR := N'""" + refTypeList + """';


    rec                              RECORD;

    LOAI_TIEN_CHINH                  INT;

    PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY VARCHAR;


BEGIN


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
    INTO LOAI_TIEN_CHINH
    FROM ir_config_parameter
    WHERE key = 'he_thong.LOAI_TIEN_CHINH'
    FETCH FIRST 1 ROW ONLY
    ;

    SELECT value
    INTO PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY
    FROM ir_config_parameter
    WHERE key = 'he_thong.PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY'
    FETCH FIRST 1 ROW ONLY
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA
    (
        "ID_CHUNG_TU"          INT,
        "MODEL_CHUNG_TU"       VARCHAR(1000),
        "NGAY_CHUNG_TU"        TIMESTAMP,
        "NGAY_HACH_TOAN"       TIMESTAMP,
        "SO_CHUNG_TU"          VARCHAR(255),
        "NGUOI_NHAN_NGUOI_NOP" VARCHAR(128),
        "MA_KHACH_HANG"        VARCHAR(255),
        "TEN_KHACH_HANG"       VARCHAR(1000),
        "DIA_CHI"              VARCHAR(255),
        "DIEN_GIAI"            VARCHAR(255),
        "SO_CT_GOC_KEM_THEO"   VARCHAR(255),
        "THANH_TIEN"           DECIMAL(22, 8),
        "THANH_TIEN_QUY_DOI"   DECIMAL(22, 8),
        "LOAI_TIEN"            VARCHAR(15),
        "TY_GIA"               DECIMAL(22, 8),
        "TK_CO"                VARCHAR(255),
        "TK_NO"                VARCHAR(255),
        "STT"                  INT,
        "MasterSortOrder"      INT,
        "DIEN_GIAI_DETAIL"     VARCHAR(255),
        "TK_CONG_NO"           VARCHAR(255)


    )
    ;


    FOR rec IN
    SELECT
        DISTINCT PR."LOAI_CHUNG_TU" AS "LOAI_CHUNG_TU"
    FROM
        TMP_PARAM PR
    LOOP

        IF rec."LOAI_CHUNG_TU" IN (1020, 1021, 1022, 1023, 1024, 1025, 1026)
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                      CAP."id"                                                   AS "ID_CHUNG_TU"
                    , 'account.ex.phieu.thu.chi'                                 AS "MODEL_CHUNG_TU"
                    , CAP."NGAY_CHUNG_TU"
                    , CAP."NGAY_HACH_TOAN"
                    , CAP."SO_CHUNG_TU"
                    , CAP."NGUOI_NOP"                                            AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            CAP."NGUOI_NOP",
                                                            CAP."TEN_DOI_TUONG") AS "TEN_KHACH_HANG"
                    , CAP."DIA_CHI"
                    , CAP."DIEN_GIAI"
                    , CAP."KEM_THEO_CHUNG_TU_GOC"
                    , (CASE WHEN (SELECT "SO_TAI_KHOAN"
                                  FROM danh_muc_he_thong_tai_khoan TK
                                  WHERE TK.id = CAPD."TK_CO_ID") LIKE N'111%%'
                    THEN CAPD."SO_TIEN"
                       ELSE -1 * CAPD."SO_TIEN"
                       END)                                                      AS "THANH_TIEN"
                    , (CASE WHEN (SELECT "SO_TAI_KHOAN"
                                  FROM danh_muc_he_thong_tai_khoan TK
                                  WHERE TK.id = CAPD."TK_CO_ID") LIKE N'111%%'
                    THEN (CASE WHEN CAP."currency_id" <> LOAI_TIEN_CHINH
                                    AND EX."ID_CHUNG_TU" IS NOT NULL
                        THEN (CASE
                              WHEN
                                  CAPD."QUY_DOI_THEO_TGXQ" <> 0
                                  THEN CAPD."QUY_DOI_THEO_TGXQ"

                              ELSE CAPD."SO_TIEN_QUY_DOI"
                              END)
                          ELSE CAPD."SO_TIEN_QUY_DOI"
                          END)
                       ELSE -1 * CAPD."SO_TIEN_QUY_DOI"
                       END)                                                      AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = CAP."currency_id")                           AS "LOAI_TIEN"
                    , CASE WHEN CAP."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE CAP."TY_GIA"
                      END
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CAPD."TK_CO_ID")                            AS "TK_CO"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CAPD."TK_NO_ID")                            AS "TK_NO"
                    , (CAPD."THU_TU_SAP_XEP_CHI_TIET")                           AS "STT"
                    , RID."STT"
                    , CAPD."DIEN_GIAI_DETAIL"
                    , lay_tai_khoan_tong_hop_chung_tk_no_phieu_thu(CAP."id")     AS "TK_CONG_NO"

                FROM TMP_PARAM AS RID
                    INNER JOIN account_ex_phieu_thu_chi CAP ON RID."ID_CHUNG_TU" = CAP."id"
                                                               AND CAP."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN account_ex_phieu_thu_chi_tiet CAPD ON CAP."id" = CAPD."PHIEU_THU_CHI_ID"
                    LEFT JOIN res_partner AO ON CAP."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON CAP."NHAN_VIEN_ID" = AOE."id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                            'account.ex.phieu.thu.chi.tiet'
                              )
                        AS EX ON CAP."id" = EX."ID_CHUNG_TU"
                                 AND CAP."currency_id" <> LOAI_TIEN_CHINH
                                 AND (CAP."LOAI_CHUNG_TU" = 1020
                                      OR CAP."LOAI_CHUNG_TU" = 1021
                                 )

                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CAPD."TK_CO_ID") LIKE N'111%%'
                      OR (SELECT "SO_TAI_KHOAN"
                          FROM danh_muc_he_thong_tai_khoan TK
                          WHERE TK.id = CAPD."TK_NO_ID") LIKE N'111%%'

                UNION ALL
                /*Dòng chênh lệch lỗ tỷ giá xuất quỹ với chứng từ chi ngoại tệ*/
                SELECT
                    CAP."id"
                    , 'account.ex.phieu.thu.chi'                                 AS "MODEL_CHUNG_TU"
                    , CAP."NGAY_CHUNG_TU"
                    , CAP."NGAY_HACH_TOAN"
                    , CAP."SO_CHUNG_TU"
                    , CAP."NGUOI_NOP"                                            AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            CAP."NGUOI_NOP",
                                                            CAP."TEN_DOI_TUONG") AS "TEN_KHACH_HANG"
                    , CAP."DIA_CHI"
                    , CAP."DIEN_GIAI"
                    , CAP."KEM_THEO_CHUNG_TU_GOC"
                    , -- nmtruong sửa lỗi Số tiền = PS Có TK 111x - PS Nợ TK 111x(không kể PSĐU Nợ TK 111x/Có TK 111x)
                      0                                                          AS "THANH_TIEN"
                    , SUM(CASE WHEN CAP."currency_id" <> LOAI_TIEN_CHINH
                                    AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN (CASE
                          WHEN CAPD."CHENH_LECH" <> 0
                              THEN CAPD."CHENH_LECH"

                          ELSE 0
                          END)
                          ELSE 0
                          END)                                                   AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = CAP."currency_id")                           AS "LOAI_TIEN"
                    , CASE WHEN CAP."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE CAP."TY_GIA"
                      END
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CAPD."TK_CO_ID")                            AS "TK_CO"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CAPD."TK_XU_LY_CHENH_LECH")                 AS "TK_NO"
                    , 1000 + MAX(CAPD."THU_TU_SAP_XEP_CHI_TIET")                 AS "STT"
                    , RID."STT"
                    , N'Xử lý chênh lệch tỷ giá'                                AS "DIEN_GIAI_DETAIL"
                    , lay_tai_khoan_tong_hop_chung_tk_no_phieu_thu(CAP."id")     AS "TK_CONG_NO"

                FROM TMP_PARAM AS RID
                    INNER JOIN account_ex_phieu_thu_chi CAP ON RID."ID_CHUNG_TU" = CAP."id"
                                                               AND CAP."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN account_ex_phieu_thu_chi_tiet CAPD ON CAP."id" = CAPD."PHIEU_THU_CHI_ID"
                    LEFT JOIN res_partner AO ON CAP."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON CAP."NHAN_VIEN_ID" = AOE."id"
                    INNER JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                             'account.ex.phieu.thu.chi.tiet'
                               )
                        AS EX ON CAP."id" = EX."ID_CHUNG_TU"
                                 AND CAP."currency_id" <> LOAI_TIEN_CHINH
                                 AND (CAP."LOAI_CHUNG_TU" = 1020
                                      OR CAP."LOAI_CHUNG_TU" = 1021
                                 )

                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CAPD."TK_CO_ID") LIKE N'111%'
                      AND (CAPD."CHENH_LECH" > 0)


                GROUP BY
                    CAP."id",
                    "MODEL_CHUNG_TU",
                    CAP."NGAY_CHUNG_TU",
                    CAP."NGAY_HACH_TOAN",
                    CAP."SO_CHUNG_TU",
                    CAP."NGUOI_NOP",
                    AO."MA",
                    CAP."TEN_DOI_TUONG",
                    LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                          CAP."NGUOI_NOP",
                                                          CAP."TEN_DOI_TUONG"),
                    CAP."DIA_CHI",
                    CAP."DIEN_GIAI",
                    CAP."KEM_THEO_CHUNG_TU_GOC",
                    (SELECT "MA_LOAI_TIEN"
                     FROM res_currency T
                     WHERE T.id = CAP."currency_id"),

                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = CAPD."TK_CO_ID"),
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = CAPD."TK_XU_LY_CHENH_LECH"),
                    CASE WHEN CAP."currency_id" <> LOAI_TIEN_CHINH
                              AND EX."ID_CHUNG_TU" IS NOT NULL
                        THEN EX."FIRST_TY_GIA_XUAT_QUY"
                    ELSE CAP."TY_GIA"
                    END,

                    RID."STT",
                    EX."ID_CHUNG_TU",
                    EX."FIRST_TY_GIA_XUAT_QUY",
                    CAPD."DIEN_GIAI_DETAIL",
                    CAP."TY_GIA",
                    lay_tai_khoan_tong_hop_chung_tk_no_phieu_thu(CAP."id")


            ;

        END IF
    ;


        IF rec."LOAI_CHUNG_TU" IN (307, 313, 357, 363)
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    PUI."id"
                    , 'purchase.document'                                                             AS "MODEL_CHUNG_TU"
                    , PUI."NGAY_CHUNG_TU"
                    , PUI."NGAY_HACH_TOAN"
                    , CASE
                      WHEN PUI."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
                          THEN PUI."SO_UY_NHIEM_CHI"
                      WHEN PUI."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
                          THEN PUI."SO_SEC_CHUYEN_KHOAN"
                      WHEN PUI."LOAI_THANH_TOAN" = 'sec_tien_mat'
                          THEN PUI."SO_SEC_TIEN_MAT"
                      ELSE
                          PUI."SO_PHIEU_CHI"
                      END

                                                                                                      AS "SO_CHUNG_TU"

                    ,
                      PUI."NGUOI_NHAN"                                                                AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            PUI."NGUOI_NHAN",
                                                            PUI."TEN_DOI_TUONG")                      AS "TEN_KHACH_HANG"
                    , PUI."DIA_CHI"
                    , PUI."LY_DO_CHI"                                                                 AS "DIEN_GIAI"
                    , PUI."KEM_THEO_PC"
                    , (PUID."THANH_TIEN" - PUID."TIEN_CHIET_KHAU"
                       + CASE WHEN PUID."TK_THUE_GTGT_ID" IS NULL
                    THEN PUID."TIEN_THUE_GTGT"
                         ELSE 0
                         END)                                                                         AS "THANH_TIEN"
                    , (CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN (CASE
                          WHEN
                              PUID."THANH_TIEN_SAU_TY_GIA_XUAT_QUY" <> 0
                              AND PUID."CHENH_LECH" < 0
                              THEN PUID."THANH_TIEN_SAU_TY_GIA_XUAT_QUY"

                          ELSE (PUID."THANH_TIEN_QUY_DOI"
                                - PUID."TIEN_CHIET_KHAU_QUY_DOI"
                                + CASE
                                  WHEN PUID."TK_THUE_GTGT_ID" IS NULL
                                      THEN PUID."TIEN_THUE_GTGT_QUY_DOI"
                                  ELSE 0
                                  END)
                          END)
                       ELSE (PUID."THANH_TIEN_QUY_DOI"
                             - PUID."TIEN_CHIET_KHAU_QUY_DOI"
                             + CASE
                               WHEN PUID."TK_THUE_GTGT_ID" IS NULL
                                   THEN PUID."TIEN_THUE_GTGT_QUY_DOI"
                               ELSE 0
                               END
                       )
                       END)                                                                           AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = PUI."currency_id")                                                AS "LOAI_TIEN"
                    , CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE PUI."TY_GIA"
                      END                                                                             AS "TY_GIA"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_NO_ID")
                    , (PUID."THU_TU_SAP_XEP_CHI_TIET")                                                AS sortOrder
                    , RID."STT"
                    , PUID."name"
                    , LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_HANG_CHI_TIET(PUI."id", '111') AS "TK_CONG_NO"

                FROM TMP_PARAM AS RID
                    INNER JOIN purchase_document PUI ON RID."ID_CHUNG_TU" = PUI."id"
                                                        AND PUI."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN purchase_document_line PUID ON PUI."id" = PUID."order_id"
                    LEFT JOIN res_partner AO ON PUI."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON PUI."NHAN_VIEN_ID" = AOE."id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                            'purchase.document.line'
                              )
                        AS EX ON PUI."id" = EX."ID_CHUNG_TU"
                                 AND PUI."currency_id" <> LOAI_TIEN_CHINH

                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID") LIKE N'111%%'
                --
                UNION ALL
                /*Dòng hạch toán lỗ chênh lệch tỷ giá của tiền hàng*/
                SELECT
                    PUI."id"
                    , 'purchase.document'                                                   AS "MODEL_CHUNG_TU"
                    , PUI."NGAY_CHUNG_TU"
                    , PUI."NGAY_HACH_TOAN"
                    , CASE
                      WHEN PUI."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
                          THEN PUI."SO_UY_NHIEM_CHI"
                      WHEN PUI."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
                          THEN PUI."SO_SEC_CHUYEN_KHOAN"
                      WHEN PUI."LOAI_THANH_TOAN" = 'sec_tien_mat'
                          THEN PUI."SO_SEC_TIEN_MAT"
                      ELSE
                          PUI."SO_PHIEU_CHI"
                      END


                                                                                            AS "SO_CHUNG_TU"

                    , PUI."NGUOI_NHAN"                                                      AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"

                    , LAY_CHUOI_ContactAndAccountObjectName
                      (AO."LOAI_KHACH_HANG",
                       PUI."NGUOI_NHAN",
                       PUI."TEN_DOI_TUONG")                                                 AS "TEN_KHACH_HANG"
                    , PUI."DIA_CHI"
                    , PUI."LY_DO_CHI"                                                       AS "DIEN_GIAI"
                    , PUI."KEM_THEO_PC"
                    , 0                                                                     AS "THANH_TIEN"
                    , SUM(CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                    AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN (CASE WHEN

                        PUID."CHENH_LECH" <> 0
                        THEN PUID."CHENH_LECH"

                          ELSE 0
                          END)
                          ELSE 0
                          END)                                                              AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = PUI."currency_id")                                      AS "LOAI_TIEN"
                    , CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE PUI."TY_GIA"
                      END                                                                   AS "TY_GIA"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_XU_LY_CHENH_LECH")

                    , 900 + MAX(PUID."THU_TU_SAP_XEP_CHI_TIET")                             AS "STT"
                    , RID."STT"
                    , N'Xử lý chênh lệch tỷ giá tiền hàng'                                    "DIEN_GIAI_DETAIL"
                    , LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_HANG_CHI_TIET(PUI."id",
                                                                                     '111') AS "TK_CONG_NO"


                FROM TMP_PARAM AS RID
                    INNER JOIN purchase_document PUI ON RID."ID_CHUNG_TU" = PUI."id"
                                                        AND PUI."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN purchase_document_line PUID ON PUI."id" = PUID."order_id"
                    LEFT JOIN res_partner AO ON PUI."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON PUI."NHAN_VIEN_ID" = AOE."id"
                    INNER JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                             'purchase.document.line'
                               )
                        AS EX ON PUI."id" = EX."ID_CHUNG_TU"
                                 AND PUI."currency_id" <> LOAI_TIEN_CHINH
                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID") LIKE N'111%'
                      AND (PUID."CHENH_LECH" > 0)


                GROUP BY
                    PUI."id",
                    "MODEL_CHUNG_TU",
                    PUI."NGAY_CHUNG_TU",
                    PUI."NGAY_HACH_TOAN",
                    CASE
                    WHEN PUI."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
                        THEN PUI."SO_UY_NHIEM_CHI"
                    WHEN PUI."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
                        THEN PUI."SO_SEC_CHUYEN_KHOAN"
                    WHEN PUI."LOAI_THANH_TOAN" = 'sec_tien_mat'
                        THEN PUI."SO_SEC_TIEN_MAT"
                    ELSE
                        PUI."SO_PHIEU_CHI"
                    END,

                    PUI."NGUOI_NHAN",
                    AO."MA",
                    PUI."TEN_DOI_TUONG",
                    LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                          PUI."NGUOI_NHAN",
                                                          PUI."TEN_DOI_TUONG"),
                    PUI."DIA_CHI",
                    PUI."KEM_THEO_PC",
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = PUID."TK_CO_ID"),
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = PUID."TK_XU_LY_CHENH_LECH"),

                    PUI."LY_DO_CHI",
                    (SELECT "MA_LOAI_TIEN"
                     FROM res_currency T
                     WHERE T.id = PUI."currency_id"),
                    PUI."TY_GIA",
                    RID."STT",
                    EX."ID_CHUNG_TU",
                    EX."FIRST_TY_GIA_XUAT_QUY",
                    PUID."THU_TU_SAP_XEP_CHI_TIET",

                    LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_HANG_CHI_TIET(PUI."id",
                                                                                   '111')






                -- -- Lấy TK GTGT
                UNION ALL
                SELECT
                    PUI."id"
                    , 'purchase.document'                                        AS "MODEL_CHUNG_TU"
                    , PUI."NGAY_CHUNG_TU"
                    , PUI."NGAY_HACH_TOAN"
                    , CASE
                      WHEN PUI."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
                          THEN PUI."SO_UY_NHIEM_CHI"
                      WHEN PUI."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
                          THEN PUI."SO_SEC_CHUYEN_KHOAN"
                      WHEN PUI."LOAI_THANH_TOAN" = 'sec_tien_mat'
                          THEN PUI."SO_SEC_TIEN_MAT"
                      ELSE
                          PUI."SO_PHIEU_CHI"
                      END


                                                                                 AS "SO_CHUNG_TU"

                    , PUI."NGUOI_NHAN"                                           AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            PUI."NGUOI_GIAO_HANG",
                                                            PUI."TEN_DOI_TUONG") AS "TEN_KHACH_HANG"
                    , PUI."DIA_CHI"
                    , PUI."LY_DO_CHI"                                            AS "DIEN_GIAI"
                    , PUI."KEM_THEO_PC"
                    , SUM(PUID."TIEN_THUE_GTGT")                                 AS "THANH_TIEN"
                    ,
                    /*Với phiếu chi PS ngoại tệ và có xử lý chênh lệch tỷ giá xuất quỹ thi thực hiện lấy số tiền quy đổi theo tỷ giá xuất quỹ, ngược lại thì lấy quy đổi*/
                      SUM((CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                     AND EX."ID_CHUNG_TU" IS NOT NULL
                          THEN (CASE
                                WHEN
                                    PUID."TIEN_THUE_GTGT_THEO_TGXQ" <> 0
                                    AND PUID."CHENH_LECH_TIEN_THUE_GTGT" < 0
                                    THEN PUID."TIEN_THUE_GTGT_THEO_TGXQ"

                                ELSE PUID."TIEN_THUE_GTGT_QUY_DOI"
                                END)
                           ELSE PUID."TIEN_THUE_GTGT_QUY_DOI"
                           END))                                                 AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = PUI."currency_id")                           AS "LOAI_TIEN"
                    , CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE PUI."TY_GIA"
                      END                                                        AS "TY_GIA"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID")                            AS "TK_CO"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_THUE_GTGT_ID")                     AS "TK_NO"
                    , 1000 + MAX(PUID."THU_TU_SAP_XEP_CHI_TIET")                 AS "STT"
                    , RID."STT"
                    , A."TEN_TAI_KHOAN"
                    , ''
                FROM TMP_PARAM AS RID
                    INNER JOIN purchase_document PUI ON RID."ID_CHUNG_TU" = PUI."id"
                                                        AND PUI."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN purchase_document_line PUID ON PUI."id" = PUID."order_id"
                    LEFT JOIN res_partner AO ON PUI."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON PUI."NHAN_VIEN_ID" = AOE."id"
                    LEFT JOIN danh_muc_he_thong_tai_khoan A ON A."SO_TAI_KHOAN" = (SELECT "SO_TAI_KHOAN"
                                                                                   FROM danh_muc_he_thong_tai_khoan TK
                                                                                   WHERE TK.id = PUID."TK_THUE_GTGT_ID")
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                            'purchase.document.line'
                              )
                        AS EX ON PUI."id" = EX."ID_CHUNG_TU"
                                 AND PUI."currency_id" <> LOAI_TIEN_CHINH

                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID") LIKE N'111%%'
                      AND PUID."TK_THUE_GTGT_ID" IS NOT NULL
                      AND (SELECT "SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan TK
                           WHERE TK.id = PUID."TK_THUE_GTGT_ID") <> ''
                      AND PUID."TIEN_THUE_GTGT_QUY_DOI" <> 0

                GROUP BY
                    PUI."id",
                    "MODEL_CHUNG_TU",
                    PUI."NGAY_CHUNG_TU",
                    PUI."NGAY_HACH_TOAN",
                    CASE
                    WHEN PUI."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
                        THEN PUI."SO_UY_NHIEM_CHI"
                    WHEN PUI."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
                        THEN PUI."SO_SEC_CHUYEN_KHOAN"
                    WHEN PUI."LOAI_THANH_TOAN" = 'sec_tien_mat'
                        THEN PUI."SO_SEC_TIEN_MAT"
                    ELSE
                        PUI."SO_PHIEU_CHI"
                    END,

                    PUI."NGUOI_NHAN",
                    AO."MA",
                    PUI."TEN_DOI_TUONG",
                    LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                          PUI."NGUOI_GIAO_HANG",
                                                          PUI."TEN_DOI_TUONG"),
                    PUI."DIA_CHI",
                    PUI."KEM_THEO_PC",
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = PUID."TK_CO_ID"),
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = PUID."TK_THUE_GTGT_ID"),

                    PUI."LY_DO_CHI",
                    (SELECT "MA_LOAI_TIEN"
                     FROM res_currency T
                     WHERE T.id = PUI."currency_id"),
                    PUI."TY_GIA",
                    RID."STT",
                    EX."ID_CHUNG_TU",
                    EX."FIRST_TY_GIA_XUAT_QUY"
                    , A."TEN_TAI_KHOAN"

                UNION ALL
                /*Dòng xử lý chênh lệch tỷ giá tiền thuế*/
                SELECT
                    PUI."id"
                    , 'purchase.document'                                        AS "MODEL_CHUNG_TU"
                    , PUI."NGAY_CHUNG_TU"
                    , PUI."NGAY_HACH_TOAN"
                    , CASE
                      WHEN PUI."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
                          THEN PUI."SO_UY_NHIEM_CHI"
                      WHEN PUI."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
                          THEN PUI."SO_SEC_CHUYEN_KHOAN"
                      WHEN PUI."LOAI_THANH_TOAN" = 'sec_tien_mat'
                          THEN PUI."SO_SEC_TIEN_MAT"
                      ELSE
                          PUI."SO_PHIEU_CHI"
                      END


                                                                                 AS "SO_CHUNG_TU"

                    , PUI."NGUOI_NHAN"                                           AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            PUI."NGUOI_GIAO_HANG",
                                                            PUI."TEN_DOI_TUONG") AS "TEN_KHACH_HANG"
                    , PUI."DIA_CHI"
                    , PUI."LY_DO_CHI"                                            AS "DIEN_GIAI"
                    , PUI."KEM_THEO_PC"
                    , 0                                                          AS "THANH_TIEN"
                    , SUM(CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                    AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN (CASE WHEN

                        PUID."CHENH_LECH_TIEN_THUE_GTGT" <> 0
                        THEN PUID."CHENH_LECH_TIEN_THUE_GTGT"

                          ELSE 0
                          END)
                          ELSE 0
                          END)                                                   AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = PUI."currency_id")                           AS "LOAI_TIEN"
                    , CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE PUI."TY_GIA"
                      END                                                        AS "TY_GIA"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID")                            AS "TK_CO"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_XU_LY_CHENH_LECH")                 AS "TK_NO"
                    , 1000 + MAX(PUID."THU_TU_SAP_XEP_CHI_TIET")                 AS "STT"
                    , RID."STT"
                    , N'Xử lý chênh lệch tỷ giá tiền thuế'
                    , ''

                FROM TMP_PARAM AS RID
                    INNER JOIN purchase_document PUI ON RID."ID_CHUNG_TU" = PUI."id"
                                                        AND PUI."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN purchase_document_line PUID ON PUI."id" = PUID."order_id"
                    LEFT JOIN res_partner AO ON PUI."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON PUI."NHAN_VIEN_ID" = AOE."id"
                    INNER JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                             'purchase.document.line'
                               )
                        AS EX ON PUI."id" = EX."ID_CHUNG_TU"
                                 AND PUI."currency_id" <> LOAI_TIEN_CHINH
                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID") LIKE N'111%'
                      AND PUID."TK_THUE_GTGT_ID" IS NOT NULL
                      AND (SELECT "SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan TK
                           WHERE TK.id = PUID."TK_THUE_GTGT_ID") <> ''
                      AND PUID."TIEN_THUE_GTGT_QUY_DOI" <> 0
                      AND (PUID."CHENH_LECH_TIEN_THUE_GTGT" > 0

                      )


                GROUP BY
                    PUI."id",
                    "MODEL_CHUNG_TU",
                    PUI."NGAY_CHUNG_TU",
                    PUI."NGAY_HACH_TOAN",
                    CASE
                    WHEN PUI."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
                        THEN PUI."SO_UY_NHIEM_CHI"
                    WHEN PUI."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
                        THEN PUI."SO_SEC_CHUYEN_KHOAN"
                    WHEN PUI."LOAI_THANH_TOAN" = 'sec_tien_mat'
                        THEN PUI."SO_SEC_TIEN_MAT"
                    ELSE
                        PUI."SO_PHIEU_CHI"
                    END,

                    PUI."NGUOI_NHAN",
                    AO."MA",
                    PUI."TEN_DOI_TUONG",
                    LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                          PUI."NGUOI_GIAO_HANG",
                                                          PUI."TEN_DOI_TUONG"),
                    PUI."DIA_CHI",
                    PUI."KEM_THEO_PC",
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = PUID."TK_CO_ID"),
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = PUID."TK_XU_LY_CHENH_LECH"),

                    PUI."LY_DO_CHI",
                    (SELECT "MA_LOAI_TIEN"
                     FROM res_currency T
                     WHERE T.id = PUI."currency_id"),
                    PUI."TY_GIA",
                    RID."STT",
                    EX."ID_CHUNG_TU",
                    EX."FIRST_TY_GIA_XUAT_QUY"


            ;

        END IF
    ;


        IF rec."LOAI_CHUNG_TU" IN (319, 325, 369, 375)  -- mua nhập khẩu
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    PUI."id"
                    , 'purchase.document'                                                   AS "MODEL_CHUNG_TU"
                    , PUI."NGAY_CHUNG_TU"
                    , PUI."NGAY_HACH_TOAN"
                    , PUI."SO_CHUNG_TU"

                    , PUI."NGUOI_NHAN"                                                      AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            PUI."NGUOI_GIAO_HANG",
                                                            PUI."TEN_DOI_TUONG")            AS "TEN_KHACH_HANG"
                    , PUI."DIA_CHI"
                    , PUI."LY_DO_CHI"                                                       AS "DIEN_GIAI"
                    , PUI."KEM_THEO_PC"
                    , (PUID."THANH_TIEN" -
                       PUID."TIEN_CHIET_KHAU")                                              AS "THANH_TIEN"
                    ,
                    /*Với phiếu chi PS ngoại tệ và có xử lý chênh lệch tỷ giá xuất quỹ thi thực hiện lấy số tiền quy đổi theo tỷ giá xuất quỹ, ngược lại thì lấy quy đổi*/
                      ((CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                  AND EX."ID_CHUNG_TU" IS NOT NULL
                          THEN (CASE
                                WHEN
                                    PUID."THANH_TIEN_SAU_TY_GIA_XUAT_QUY" <> 0
                                    THEN PUID."THANH_TIEN_SAU_TY_GIA_XUAT_QUY"

                                ELSE (PUID."THANH_TIEN_QUY_DOI"
                                      - PUID."TIEN_CHIET_KHAU_QUY_DOI")
                                END)
                        ELSE (PUID."THANH_TIEN_QUY_DOI"
                              - PUID."TIEN_CHIET_KHAU_QUY_DOI")
                        END))                                                               AS "THANH_TIEN_QUY_DOI"

                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = PUI."currency_id")                                      AS "LOAI_TIEN"
                    , CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE PUI."TY_GIA"
                      END                                                                   AS "TY_GIA"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_NO_ID")


                    , (PUID."THU_TU_SAP_XEP_CHI_TIET")                                      AS sortOrder
                    , RID."STT"
                    , PUID.name
                    , LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_HANG_CHI_TIET(PUI."id",
                                                                                     '111') AS "TK_CONG_NO"

                FROM TMP_PARAM AS RID
                    INNER JOIN purchase_document PUI ON RID."ID_CHUNG_TU" = PUI."id"
                                                        AND PUI."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN purchase_document_line PUID ON PUI."id" = PUID."order_id"
                    LEFT JOIN res_partner AO ON PUI."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON PUI."NHAN_VIEN_ID" = AOE."id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                            'purchase.document.line'
                              )
                        AS EX ON PUI."id" = EX."ID_CHUNG_TU"
                                 AND PUI."currency_id" <> LOAI_TIEN_CHINH


                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID") LIKE N'111%%'

                UNION ALL
                /*Dòng hạch toán lỗ chênh lệch tỷ giá của tiền hàng*/
                SELECT
                    PUI."id"
                    , 'purchase.document'                                                   AS "MODEL_CHUNG_TU"
                    , PUI."NGAY_CHUNG_TU"
                    , PUI."NGAY_HACH_TOAN"

                    , CASE
                      WHEN PUI."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
                          THEN PUI."SO_UY_NHIEM_CHI"
                      WHEN PUI."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
                          THEN PUI."SO_SEC_CHUYEN_KHOAN"
                      WHEN PUI."LOAI_THANH_TOAN" = 'sec_tien_mat'
                          THEN PUI."SO_SEC_TIEN_MAT"
                      ELSE
                          PUI."SO_PHIEU_CHI"
                      END


                                                                                            AS "SO_CHUNG_TU"
                    , PUI."NGUOI_NHAN"                                                      AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"

                    , LAY_CHUOI_ContactAndAccountObjectName
                      (AO."LOAI_KHACH_HANG",
                       PUI."NGUOI_NHAN",
                       PUI."TEN_DOI_TUONG")                                                 AS "TEN_KHACH_HANG"
                    , PUI."DIA_CHI"
                    , PUI."LY_DO_CHI"                                                       AS "DIEN_GIAI"
                    , PUI."KEM_THEO_PC"
                    , 0                                                                     AS "THANH_TIEN"
                    , SUM(CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                    AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN (CASE WHEN

                        PUID."CHENH_LECH" <> 0
                        THEN PUID."CHENH_LECH"

                          ELSE 0
                          END)
                          ELSE 0
                          END)                                                              AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = PUI."currency_id")                                      AS "LOAI_TIEN"
                    , CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE PUI."TY_GIA"
                      END                                                                   AS "TY_GIA"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_XU_LY_CHENH_LECH")

                    , 900 + MAX(PUID."THU_TU_SAP_XEP_CHI_TIET")                             AS "STT"
                    , RID."STT"
                    , N'Xử lý chênh lệch tỷ giá tiền hàng'                                    "DIEN_GIAI_DETAIL"
                    , LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_HANG_CHI_TIET(PUI."id",
                                                                                     '111') AS "TK_CONG_NO"


                FROM TMP_PARAM AS RID
                    INNER JOIN purchase_document PUI ON RID."ID_CHUNG_TU" = PUI."id"
                                                        AND PUI."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN purchase_document_line PUID ON PUI."id" = PUID."order_id"
                    LEFT JOIN res_partner AO ON PUI."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON PUI."NHAN_VIEN_ID" = AOE."id"
                    INNER JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                             'purchase.document.line'
                               )
                        AS EX ON PUI."id" = EX."ID_CHUNG_TU"
                                 AND PUI."currency_id" <> LOAI_TIEN_CHINH
                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID") LIKE N'111%'
                      AND ((PUID."CHENH_LECH" > 0

                )

                      )


                GROUP BY
                    PUI."id",
                    "MODEL_CHUNG_TU",
                    PUI."NGAY_CHUNG_TU",
                    PUI."NGAY_HACH_TOAN",
                    CASE
                    WHEN PUI."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
                        THEN PUI."SO_UY_NHIEM_CHI"
                    WHEN PUI."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
                        THEN PUI."SO_SEC_CHUYEN_KHOAN"
                    WHEN PUI."LOAI_THANH_TOAN" = 'sec_tien_mat'
                        THEN PUI."SO_SEC_TIEN_MAT"
                    ELSE
                        PUI."SO_PHIEU_CHI"
                    END,

                    PUI."NGUOI_NHAN",
                    AO."MA",
                    PUI."TEN_DOI_TUONG",
                    LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                          PUI."NGUOI_NHAN",
                                                          PUI."TEN_DOI_TUONG"),
                    PUI."DIA_CHI",
                    PUI."KEM_THEO_PC",
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = PUID."TK_CO_ID"),
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = PUID."TK_XU_LY_CHENH_LECH"),

                    PUI."LY_DO_CHI",
                    (SELECT "MA_LOAI_TIEN"
                     FROM res_currency T
                     WHERE T.id = PUI."currency_id"),
                    PUI."TY_GIA",
                    RID."STT",
                    EX."ID_CHUNG_TU",
                    EX."FIRST_TY_GIA_XUAT_QUY"
                    , LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_HANG_CHI_TIET(PUI."id",
                                                                                     '111')
            ;

        END IF
    ;


        IF rec."LOAI_CHUNG_TU" = 331
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    PUI."id"
                    , 'purchase.document'                                        AS "MODEL_CHUNG_TU"
                    , PUI."NGAY_CHUNG_TU"
                    , PUI."NGAY_HACH_TOAN"
                    , PUI."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(PUI."NGUOI_NHAN",
                                            '') <> ''
                        THEN PUI."NGUOI_NHAN"
                         ELSE PUI."TEN_DOI_TUONG"
                         END
                      ELSE PUI."NGUOI_NHAN"
                      END                                                        AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            PUI."NGUOI_NHAN",
                                                            PUI."TEN_DOI_TUONG") AS "TEN_KHACH_HANG"
                    , PUI."DIA_CHI"
                    , PUI."DIEN_GIAI_CHUNG"                                      AS "DIEN_GIAI"
                    , PUI."KEM_THEO_PC"
                    , (PUID."THANH_TIEN" - PUID."TIEN_CHIET_KHAU"
                       + CASE WHEN PUID."TK_THUE_GTGT_ID" IS NULL
                    THEN "TIEN_THUE_GTGT"
                         ELSE 0
                         END)                                                    AS "THANH_TIEN"
                    ,
                    /*Với phiếu chi PS ngoại tệ và có xử lý chênh lệch tỷ giá xuất quỹ thi thực hiện lấy số tiền quy đổi theo tỷ giá xuất quỹ, ngược lại thì lấy quy đổi*/
                      (CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                          THEN (CASE
                                WHEN
                                    PUID."THANH_TIEN_SAU_TY_GIA_XUAT_QUY" <> 0
                                    AND PUID."CHENH_LECH" < 0
                                    THEN PUID."THANH_TIEN_SAU_TY_GIA_XUAT_QUY"

                                ELSE (PUID."THANH_TIEN_QUY_DOI"
                                      - "TIEN_CHIET_KHAU_QUY_DOI"
                                      + CASE
                                        WHEN PUID."TK_THUE_GTGT_ID" IS NULL
                                            THEN "TIEN_THUE_GTGT_QUY_DOI"
                                        ELSE 0
                                        END)
                                END)
                       ELSE (PUID."THANH_TIEN_QUY_DOI"
                             - PUID."TIEN_CHIET_KHAU_QUY_DOI"
                             + CASE
                               WHEN PUID."TK_THUE_GTGT_ID" IS NULL
                                   THEN "TIEN_THUE_GTGT_QUY_DOI"
                               ELSE 0
                               END)
                       END)                                                      AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = PUI."currency_id")                           AS "LOAI_TIEN"
                    , CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE PUI."TY_GIA"
                      END                                                        AS "TY_GIA"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_NO_ID")

                    , (PUID."THU_TU_SAP_XEP_CHI_TIET")                           AS sortOrder
                    , RID."STT"
                    , PUID.name
                    , LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_DICH_VU_CHI_TIET(PUI."id"
                )

                FROM TMP_PARAM AS RID
                    INNER JOIN purchase_document PUI ON RID."ID_CHUNG_TU" = PUI."id"
                                                        AND PUI."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN purchase_document_line PUID ON PUI."id" = PUID."order_id"
                    LEFT JOIN res_partner AO ON PUI."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON PUI."NHAN_VIEN_ID" = AOE."id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                            'purchase.document.line'
                              )
                        AS EX ON PUI."id" = EX."ID_CHUNG_TU"
                                 AND PUI."currency_id" <> LOAI_TIEN_CHINH

                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID") LIKE N'111%%'

                UNION ALL
                /*Dòng hạch toán lỗ chênh lệch tỷ giá của tiền hàng*/
                SELECT
                    PUI."id"
                    , 'purchase.document'                                        AS "MODEL_CHUNG_TU"
                    , PUI."NGAY_CHUNG_TU"
                    , PUI."NGAY_HACH_TOAN"
                    , PUI."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(PUI."NGUOI_NHAN",
                                            '') <> ''
                        THEN PUI."NGUOI_NHAN"
                         ELSE PUI."TEN_DOI_TUONG"
                         END
                      ELSE PUI."NGUOI_NHAN"
                      END                                                        AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            PUI."NGUOI_NHAN",
                                                            PUI."TEN_DOI_TUONG") AS "TEN_KHACH_HANG"
                    , PUI."DIA_CHI"
                    , PUI."DIEN_GIAI_CHUNG"                                      AS "DIEN_GIAI"
                    , PUI."KEM_THEO_PC"
                    , 0                                                          AS "THANH_TIEN"
                    , SUM(CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                    AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN (CASE WHEN
                        PUID."CHENH_LECH" <> 0
                        THEN PUID."CHENH_LECH"

                          ELSE 0
                          END)
                          ELSE 0
                          END)                                                   AS "THANH_TIEN_QUY_DOI"

                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = PUI."currency_id")                           AS "LOAI_TIEN"
                    , CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE PUI."TY_GIA"
                      END                                                        AS "TY_GIA"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_XU_LY_CHENH_LECH")

                    , 900 + MAX(PUID."THU_TU_SAP_XEP_CHI_TIET")                  AS sortOrder
                    , RID."STT"
                    , N'Xử lý chênh lệch tỷ giá tiền hàng'
                    , LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_DICH_VU_CHI_TIET(PUI."id")

                FROM TMP_PARAM AS RID
                    INNER JOIN purchase_document PUI ON RID."ID_CHUNG_TU" = PUI."id"
                                                        AND PUI."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN purchase_document_line PUID ON PUI."id" = PUID."order_id"
                    LEFT JOIN res_partner AO ON PUI."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON PUI."NHAN_VIEN_ID" = AOE."id"
                    INNER JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                             'purchase.document.line'
                               )
                        AS EX ON PUI."id" = EX."ID_CHUNG_TU"
                                 AND PUI."currency_id" <> LOAI_TIEN_CHINH
                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID") LIKE N'111%'
                      AND ((PUID."CHENH_LECH" > 0

                )

                      )


                GROUP BY
                    PUI."id"
                    , "MODEL_CHUNG_TU"
                    , PUI."NGAY_CHUNG_TU"
                    , PUI."NGAY_HACH_TOAN"
                    , PUI."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(PUI."NGUOI_NHAN",
                                            '') <> ''
                        THEN PUI."NGUOI_NHAN"
                         ELSE PUI."TEN_DOI_TUONG"
                         END
                      ELSE PUI."NGUOI_NHAN"
                      END
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            PUI."NGUOI_NHAN",
                                                            PUI."TEN_DOI_TUONG")
                    , PUI."DIA_CHI"
                    , PUI."DIEN_GIAI_CHUNG"
                    , PUI."KEM_THEO_PC"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID"),
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = PUID."TK_XU_LY_CHENH_LECH")


                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = PUI."currency_id")
                    , PUI."TY_GIA"
                    , RID."STT"
                    , EX."ID_CHUNG_TU"
                    , EX."FIRST_TY_GIA_XUAT_QUY"
                    , LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_DICH_VU_CHI_TIET(PUI."id")

                -- Lấy TK GTGT
                UNION ALL
                SELECT
                    PUI."id"
                    , 'purchase.document'                                        AS "MODEL_CHUNG_TU"
                    , PUI."NGAY_CHUNG_TU"
                    , PUI."NGAY_HACH_TOAN"
                    , PUI."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(PUI."NGUOI_NHAN",
                                            '') <> ''
                        THEN PUI."NGUOI_NHAN"
                         ELSE PUI."TEN_DOI_TUONG"
                         END
                      ELSE PUI."NGUOI_NHAN"
                      END                                                        AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            PUI."NGUOI_NHAN",
                                                            PUI."TEN_DOI_TUONG") AS "TEN_KHACH_HANG"
                    , PUI."DIA_CHI"
                    , PUI."DIEN_GIAI_CHUNG"                                      AS "DIEN_GIAI"
                    , PUI."KEM_THEO_PC"
                    , SUM(PUID."TIEN_THUE_GTGT")                                 AS "THANH_TIEN"
                    ,
                    /*Với phiếu chi PS ngoại tệ và có xử lý chênh lệch tỷ giá xuất quỹ thi thực hiện lấy số tiền quy đổi theo tỷ giá xuất quỹ, ngược lại thì lấy quy đổi*/
                      SUM((CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                     AND EX."ID_CHUNG_TU" IS NOT NULL
                          THEN (CASE
                                WHEN
                                    PUID."TIEN_THUE_GTGT_THEO_TGXQ" <> 0
                                    AND PUID."CHENH_LECH_TIEN_THUE_GTGT" < 0
                                    THEN PUID."TIEN_THUE_GTGT_THEO_TGXQ"

                                ELSE PUID."TIEN_THUE_GTGT_QUY_DOI"
                                END)
                           ELSE PUID."TIEN_THUE_GTGT_QUY_DOI"
                           END))                                                 AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = PUI."currency_id")                           AS "LOAI_TIEN"
                    , CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE PUI."TY_GIA"
                      END                                                        AS "TY_GIA"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_THUE_GTGT_ID")
                                                                                 AS "TK_NO"

                    , 1000 + MAX(PUID."THU_TU_SAP_XEP_CHI_TIET")                 AS sortOrder
                    , RID."STT"
                    , A."TEN_TAI_KHOAN"
                    , ''


                FROM TMP_PARAM AS RID
                    INNER JOIN purchase_document PUI ON RID."ID_CHUNG_TU" = PUI."id"
                                                        AND PUI."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN purchase_document_line PUID ON PUI."id" = PUID."order_id"
                    LEFT JOIN res_partner AO ON PUI."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON PUI."NHAN_VIEN_ID" = AOE."id"
                    LEFT JOIN danh_muc_he_thong_tai_khoan A ON a."SO_TAI_KHOAN" = (SELECT "SO_TAI_KHOAN"
                                                                                   FROM danh_muc_he_thong_tai_khoan TK
                                                                                   WHERE TK.id = PUID."TK_THUE_GTGT_ID")
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                            'purchase.document.line'
                              )
                        AS EX ON PUI."id" = EX."ID_CHUNG_TU"
                                 AND PUI."currency_id" <> LOAI_TIEN_CHINH

                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID") LIKE N'111%%'
                      AND PUID."TK_THUE_GTGT_ID" IS NOT NULL
                      AND (SELECT "SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan TK
                           WHERE TK.id = PUID."TK_THUE_GTGT_ID") <> ''
                      AND PUID."TIEN_THUE_GTGT_QUY_DOI" <> 0
                GROUP BY
                    PUI."id"
                    , "MODEL_CHUNG_TU"
                    , PUI."NGAY_CHUNG_TU"
                    , PUI."NGAY_HACH_TOAN"
                    , PUI."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(PUI."NGUOI_NHAN",
                                            '') <> ''
                        THEN PUI."NGUOI_NHAN"
                         ELSE PUI."TEN_DOI_TUONG"
                         END
                      ELSE PUI."NGUOI_NHAN"
                      END
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            PUI."NGUOI_NHAN",
                                                            PUI."TEN_DOI_TUONG")
                    , PUI."DIA_CHI"
                    , PUI."DIEN_GIAI_CHUNG"
                    , PUI."KEM_THEO_PC"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID"),
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = PUID."TK_THUE_GTGT_ID")


                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = PUI."currency_id")
                    , PUI."TY_GIA"
                    , RID."STT"
                    , EX."ID_CHUNG_TU"
                    , EX."FIRST_TY_GIA_XUAT_QUY"
                    , A."TEN_TAI_KHOAN"

                UNION ALL
                /*Dòng xử lý chênh lệch tỷ giá tiền thuế*/
                SELECT
                    PUI."id"
                    , 'purchase.document'                                        AS "MODEL_CHUNG_TU"
                    , PUI."NGAY_CHUNG_TU"
                    , PUI."NGAY_HACH_TOAN"
                    , PUI."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(PUI."NGUOI_NHAN",
                                            '') <> ''
                        THEN PUI."NGUOI_NHAN"
                         ELSE PUI."TEN_DOI_TUONG"
                         END
                      ELSE PUI."NGUOI_NHAN"
                      END                                                        AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            PUI."NGUOI_NHAN",
                                                            PUI."TEN_DOI_TUONG") AS "TEN_KHACH_HANG"
                    , PUI."DIA_CHI"
                    , PUI."DIEN_GIAI_CHUNG"                                      AS "DIEN_GIAI"
                    , PUI."KEM_THEO_PC"
                    , 0                                                          AS "THANH_TIEN"
                    , SUM(CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                    AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN (CASE WHEN
                        PUID."CHENH_LECH_TIEN_THUE_GTGT" <> 0
                        THEN PUID."CHENH_LECH_TIEN_THUE_GTGT"

                          ELSE 0
                          END)
                          ELSE 0
                          END)                                                   AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = PUI."currency_id")                           AS "LOAI_TIEN"
                    , CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE PUI."TY_GIA"
                      END                                                        AS "TY_GIA"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_XU_LY_CHENH_LECH")
                                                                                 AS "TK_NO"

                    , 1001 + MAX(PUID."THU_TU_SAP_XEP_CHI_TIET")                 AS sortOrder
                    , RID."STT"
                    , N'Xử lý chênh lệch tỷ giá tiền thuế'
                    , ''

                FROM TMP_PARAM AS RID
                    INNER JOIN purchase_document PUI ON RID."ID_CHUNG_TU" = PUI."id"
                                                        AND PUI."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN purchase_document_line PUID ON PUI."id" = PUID."order_id"
                    LEFT JOIN res_partner AO ON PUI."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON PUI."NHAN_VIEN_ID" = AOE."id"
                    INNER JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                             'purchase.document.line'
                               )
                        AS EX ON PUI."id" = EX."ID_CHUNG_TU"
                                 AND PUI."currency_id" <> LOAI_TIEN_CHINH
                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID") LIKE N'111%'
                      AND PUID."TK_THUE_GTGT_ID" IS NOT NULL
                      AND (SELECT "SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan TK
                           WHERE TK.id = PUID."TK_THUE_GTGT_ID") <> ''
                      AND PUID."TIEN_THUE_GTGT_QUY_DOI" <> 0
                      AND ((PUID."CHENH_LECH_TIEN_THUE_GTGT" > 0

                )
                      )
                GROUP BY
                    PUI."id"
                    , "MODEL_CHUNG_TU"
                    , PUI."NGAY_CHUNG_TU"
                    , PUI."NGAY_HACH_TOAN"
                    , PUI."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(PUI."NGUOI_NHAN",
                                            '') <> ''
                        THEN PUI."NGUOI_NHAN"
                         ELSE PUI."TEN_DOI_TUONG"
                         END
                      ELSE PUI."NGUOI_NHAN"
                      END
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            PUI."NGUOI_NHAN",
                                                            PUI."TEN_DOI_TUONG")
                    , PUI."DIA_CHI"
                    , PUI."DIEN_GIAI_CHUNG"
                    , PUI."KEM_THEO_PC"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PUID."TK_CO_ID"),
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = PUID."TK_XU_LY_CHENH_LECH")


                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = PUI."currency_id")
                    , PUI."TY_GIA"
                    , RID."STT"
                    , EX."ID_CHUNG_TU"
                    , EX."FIRST_TY_GIA_XUAT_QUY"


            ;

        END IF
    ;


        IF rec."LOAI_CHUNG_TU" IN (3551, 3553, 3555)
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    SAR."id"
                    , 'sale.ex.giam.gia.hang.ban'                                 AS "MODEL_CHUNG_TU"
                    , SAR."NGAY_CHUNG_TU"
                    , SAr."NGAY_HACH_TOAN"
                    , SAR."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                            '') <> ''
                        THEN SAR."NGUOI_NHAN"
                         ELSE SAR."TEN_KHACH_HANG"
                         END
                      ELSE SAR."NGUOI_NHAN"
                      END                                                         AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            SAR."NGUOI_NHAN",
                                                            SAR."TEN_KHACH_HANG") AS "TEN_KHACH_HANG"
                    , SAR."DIA_CHI"
                    , SAR."DIEN_GIAI"                                             AS "DIEN_GIAI"
                    , SAR."KEM_THEO_CT_GOC"
                    , /*Với bán giảm giá đại lý thì thành tiền - chiết khấu + thuế*/
                      CASE WHEN SAR."LOAI_CHUNG_TU" = 3553
                          THEN SARD."THANH_TIEN"
                               - SARD."TIEN_CHIET_KHAU"
                               + SARD."TIEN_THUE_GTGT"
                      ELSE SARD."THANH_TIEN"
                           - SARD."TIEN_CHIET_KHAU"
                      END                                                         AS "THANH_TIEN"
                    , (CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN CASE WHEN SAR."LOAI_CHUNG_TU" = 3551
                        THEN (CASE
                              WHEN
                                  SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY" <> 0
                                  AND SARD."CHENH_LECH" < 0
                                  THEN SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY"

                              ELSE SARD."THANH_TIEN_QUY_DOI"
                              END)

                         ELSE (CASE
                               WHEN
                                   SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY" <> 0
                                   AND SARD."CHENH_LECH" < 0
                                   THEN SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY"

                               ELSE (CASE
                                     WHEN SAR."LOAI_CHUNG_TU" = 3553
                                         THEN SARD."THANH_TIEN_QUY_DOI"
                                              - SARD."TIEN_CHIET_KHAU_QUY_DOI"
                                              + SARD."TIEN_THUE_GTGT_QUY_DOI"
                                     ELSE SARD."THANH_TIEN_QUY_DOI"
                                          - SARD."TIEN_CHIET_KHAU_QUY_DOI"
                                     END)
                               END)
                         END
                       ELSE (CASE
                             WHEN SAR."LOAI_CHUNG_TU" = 3553
                                 THEN SARD."THANH_TIEN_QUY_DOI"
                                      - SARD."TIEN_CHIET_KHAU_QUY_DOI"
                                      + SARD."TIEN_THUE_GTGT_QUY_DOI"
                             WHEN SAR."LOAI_CHUNG_TU" = 3555
                                 THEN SARD."THANH_TIEN_QUY_DOI"
                                      - SARD."TIEN_CHIET_KHAU_QUY_DOI"
                             ELSE SARD."THANH_TIEN_QUY_DOI"

                             END)
                       END)                                                       AS "THANH_TIEN_QUY_DOI"


                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = SAR."currency_id")                            AS "LOAI_TIEN"
                    , CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE SAR."TY_GIA"
                      END
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_NO_ID")

                    , (SARD."THU_TU_SAP_XEP_CHI_TIET")                            AS "STT"
                    , RID."STT"
                    , SARD."TEN_HANG"
                    , LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_GIAM_GIA_HANG_BAN_CHI_TIET(SAR."id")


                FROM TMP_PARAM AS RID
                    INNER JOIN sale_ex_giam_gia_hang_ban SAR ON RID."ID_CHUNG_TU" = SAR."id"
                                                                AND RID."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban SARD ON SAR."id" = SARD."GIAM_GIA_HANG_BAN_ID"
                    LEFT JOIN res_partner AO ON SAR."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON SAR."NHAN_VIEN_ID" = AOE."id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                            'sale.ex.chi.tiet.giam.gia.hang.ban'
                              )
                        AS EX ON SAR."id" = EX."ID_CHUNG_TU"
                                 AND SAR."currency_id" <> LOAI_TIEN_CHINH

                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID") LIKE '111%%'

                UNION ALL
                /*Dòng xử lý chênh lệch tỷ giá tiền hàng*/
                SELECT
                    SAR."id"
                    , 'sale.ex.giam.gia.hang.ban'                                 AS "MODEL_CHUNG_TU"
                    , SAR."NGAY_CHUNG_TU"
                    , SAr."NGAY_HACH_TOAN"
                    , SAR."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                            '') <> ''
                        THEN SAR."NGUOI_NHAN"
                         ELSE SAR."TEN_KHACH_HANG"
                         END
                      ELSE SAR."NGUOI_NHAN"
                      END                                                         AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            SAR."NGUOI_NHAN",
                                                            SAR."TEN_KHACH_HANG") AS "TEN_KHACH_HANG"
                    , SAR."DIA_CHI"
                    , SAR."DIEN_GIAI"                                             AS "DIEN_GIAI"
                    , SAR."KEM_THEO_CT_GOC"
                    , 0                                                           AS "THANH_TIEN"
                    , SUM(CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                    AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN (CASE WHEN
                        SARD."CHENH_LECH" <> 0
                        THEN SARD."CHENH_LECH"

                          ELSE 0
                          END)
                          ELSE 0
                          END)                                                    AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = SAR."currency_id")                            AS "LOAI_TIEN"
                    , CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE SAR."TY_GIA"
                      END
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_XU_LY_CHENH_LECH")

                    , 900 + MAX(SARD."THU_TU_SAP_XEP_CHI_TIET")                   AS "STT"
                    , RID."STT"
                    , CASE WHEN SAR."LOAI_CHUNG_TU" = 3551
                    THEN N'Xử lý chênh lệch tỷ giá tiền hàng'
                      ELSE N'Xử lý chênh lệch tỷ giá tổng tiền thanh toán'
                      END
                    , LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_GIAM_GIA_HANG_BAN_CHI_TIET(SAR."id")

                FROM TMP_PARAM AS RID
                    INNER JOIN sale_ex_giam_gia_hang_ban SAR ON RID."ID_CHUNG_TU" = SAR."id"
                                                                AND RID."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban SARD ON SAR."id" = SARD."GIAM_GIA_HANG_BAN_ID"
                    LEFT JOIN res_partner AO ON SAR."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON SAR."NHAN_VIEN_ID" = AOE."id"
                    INNER JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                             'sale.ex.chi.tiet.giam.gia.hang.ban'
                               )
                        AS EX ON SAR."id" = EX."ID_CHUNG_TU"
                                 AND SAR."currency_id" <> LOAI_TIEN_CHINH

                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID") LIKE N'111%'
                      AND ((SARD."CHENH_LECH" > 0

                )
                      )


                GROUP BY
                    SAR."id"
                    , "MODEL_CHUNG_TU"
                    , SAR."NGAY_CHUNG_TU"
                    , SAr."NGAY_HACH_TOAN"
                    , SAR."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                            '') <> ''
                        THEN SAR."NGUOI_NHAN"
                         ELSE SAR."TEN_KHACH_HANG"
                         END
                      ELSE SAR."NGUOI_NHAN"
                      END
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            SAR."NGUOI_NHAN",
                                                            SAR."TEN_KHACH_HANG")
                    , SAR."DIA_CHI"
                    , SAR."DIEN_GIAI"
                    , SAR."KEM_THEO_CT_GOC"
                    , SAR."TY_GIA"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = SAR."currency_id")

                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_XU_LY_CHENH_LECH")
                    , RID."STT"
                    , EX."ID_CHUNG_TU"
                    , EX."FIRST_TY_GIA_XUAT_QUY"
                    , SAR."LOAI_CHUNG_TU"

                -- Lấy các dòng Thuế giá trị gia tăng
                UNION ALL
                SELECT
                    SAR."id"
                    , 'sale.ex.giam.gia.hang.ban'                                 AS "MODEL_CHUNG_TU"
                    , SAR."NGAY_CHUNG_TU"
                    , SAr."NGAY_HACH_TOAN"
                    , SAR."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                            '') <> ''
                        THEN SAR."NGUOI_NHAN"
                         ELSE SAR."TEN_KHACH_HANG"
                         END
                      ELSE SAR."NGUOI_NHAN"
                      END                                                         AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            SAR."NGUOI_NHAN",
                                                            SAR."TEN_KHACH_HANG") AS "TEN_KHACH_HANG"
                    , SAR."DIA_CHI"
                    , SAR."DIEN_GIAI"                                             AS "DIEN_GIAI"
                    , SAR."KEM_THEO_CT_GOC"
                    , SUM(SARD."TIEN_THUE_GTGT")                                  AS "THANH_TIEN"
                    ,
                    /*Với phiếu chi PS ngoại tệ và có xử lý chênh lệch tỷ giá xuất quỹ thi thực hiện lấy số tiền quy đổi theo tỷ giá xuất quỹ, ngược lại thì lấy quy đổi*/
                      SUM((CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                     AND EX."ID_CHUNG_TU" IS NOT NULL
                          THEN (CASE
                                WHEN
                                    SARD."TIEN_THUE_GTGT_THEO_TGXQ" <> 0
                                    AND SARD."CHENH_LECH_TIEN_THUE_GTGT" < 0
                                    THEN SARD."TIEN_THUE_GTGT_THEO_TGXQ"

                                ELSE SARD."TIEN_THUE_GTGT_QUY_DOI"
                                END)
                           ELSE SARD."TIEN_THUE_GTGT_QUY_DOI"
                           END))                                                  AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = SAR."currency_id")                            AS "LOAI_TIEN"
                    , CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE SAR."TY_GIA"
                      END
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_THUE_GTGT_ID")

                    , 2000 + MAX(SARD."THU_TU_SAP_XEP_CHI_TIET")                  AS sortOrder
                    , RID."STT"
                    , A."TEN_TAI_KHOAN"
                    , ''


                FROM TMP_PARAM AS RID
                    INNER JOIN sale_ex_giam_gia_hang_ban SAR ON RID."ID_CHUNG_TU" = SAR."id"
                                                                AND RID."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban SARD ON SAR."id" = SARD."GIAM_GIA_HANG_BAN_ID"
                    LEFT JOIN res_partner AO ON SAR."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON SAR."NHAN_VIEN_ID" = AOE."id"
                    LEFT JOIN danh_muc_he_thong_tai_khoan A ON a."SO_TAI_KHOAN" = (SELECT "SO_TAI_KHOAN"
                                                                                   FROM danh_muc_he_thong_tai_khoan TK
                                                                                   WHERE TK.id = SARD."TK_THUE_GTGT_ID")
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                            'sale.ex.chi.tiet.giam.gia.hang.ban'
                              )
                        AS EX ON SAR."id" = EX."ID_CHUNG_TU"
                                 AND SAR."currency_id" <> LOAI_TIEN_CHINH

                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID") LIKE N'111%%'
                      AND SARD."TK_THUE_GTGT_ID" IS NOT NULL
                      AND (SELECT "SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan TK
                           WHERE TK.id = SARD."TK_THUE_GTGT_ID") <> ''
                      AND SARD."TIEN_THUE_GTGT_QUY_DOI" <> 0
                      AND
                      SAR."LOAI_CHUNG_TU" = 3551 /*Chỉ loại giảm giá từ bán hàng hóa dịch vụ thì mới có hạch toán thuế*/
                GROUP BY
                    SAR."id"
                    , "MODEL_CHUNG_TU"
                    , SAR."NGAY_CHUNG_TU"
                    , SAr."NGAY_HACH_TOAN"
                    , SAR."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                            '') <> ''
                        THEN SAR."NGUOI_NHAN"
                         ELSE SAR."TEN_KHACH_HANG"
                         END
                      ELSE SAR."NGUOI_NHAN"
                      END
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            SAR."NGUOI_NHAN",
                                                            SAR."TEN_KHACH_HANG")
                    , SAR."DIA_CHI"
                    , SAR."DIEN_GIAI"
                    , SAR."KEM_THEO_CT_GOC"
                    , SAR."TY_GIA"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = SAR."currency_id")

                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_THUE_GTGT_ID")
                    , RID."STT"
                    , EX."ID_CHUNG_TU"
                    , EX."FIRST_TY_GIA_XUAT_QUY"
                    , A."TEN_TAI_KHOAN"


                UNION ALL
                /*Dòng xử lý chênh lệch tỷ giá tiền thuế*/
                SELECT
                    SAR."id"
                    , 'sale.ex.giam.gia.hang.ban'                                 AS "MODEL_CHUNG_TU"
                    , SAR."NGAY_CHUNG_TU"
                    , SAr."NGAY_HACH_TOAN"
                    , SAR."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                            '') <> ''
                        THEN SAR."NGUOI_NHAN"
                         ELSE SAR."TEN_KHACH_HANG"
                         END
                      ELSE SAR."NGUOI_NHAN"
                      END                                                         AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            SAR."NGUOI_NHAN",
                                                            SAR."TEN_KHACH_HANG") AS "TEN_KHACH_HANG"
                    , SAR."DIA_CHI"
                    , SAR."DIEN_GIAI"                                             AS "DIEN_GIAI"
                    , SAR."KEM_THEO_CT_GOC"
                    , 0                                                           AS "THANH_TIEN"
                    , SUM(CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                    AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN (CASE WHEN SARD."CHENH_LECH_TIEN_THUE_GTGT" <> 0
                        THEN SARD."CHENH_LECH_TIEN_THUE_GTGT"

                          ELSE 0
                          END)
                          ELSE 0
                          END)                                                    AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = SAR."currency_id")                            AS "LOAI_TIEN"
                    , CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE SAR."TY_GIA"
                      END
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_XU_LY_CHENH_LECH")

                    , 2001 + MAX(SARD."THU_TU_SAP_XEP_CHI_TIET")                  AS sortOrder
                    , RID."STT"
                    , N'Xử lý chênh lệch tỷ giá tiền thuế'
                    , ''

                FROM TMP_PARAM AS RID
                    INNER JOIN sale_ex_giam_gia_hang_ban SAR ON RID."ID_CHUNG_TU" = SAR."id"
                                                                AND RID."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban SARD ON SAR."id" = SARD."GIAM_GIA_HANG_BAN_ID"
                    LEFT JOIN res_partner AO ON SAR."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON SAR."NHAN_VIEN_ID" = AOE."id"
                    INNER JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                             'sale.ex.chi.tiet.giam.gia.hang.ban'
                               )
                        AS EX ON SAR."id" = EX."ID_CHUNG_TU"
                                 AND SAR."currency_id" <> LOAI_TIEN_CHINH
                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID") LIKE N'111%'
                      AND SARD."TK_THUE_GTGT_ID" IS NOT NULL
                      AND (SELECT "SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan TK
                           WHERE TK.id = SARD."TK_THUE_GTGT_ID") <> ''
                      AND SARD."TIEN_THUE_GTGT_QUY_DOI" <> 0
                      AND SAR."LOAI_CHUNG_TU" = 3551
                      AND ((SARD."CHENH_LECH_TIEN_THUE_GTGT" > 0

                )
                      )
                GROUP BY
                    SAR."id"
                    , "MODEL_CHUNG_TU"
                    , SAR."NGAY_CHUNG_TU"
                    , SAr."NGAY_HACH_TOAN"
                    , SAR."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                            '') <> ''
                        THEN SAR."NGUOI_NHAN"
                         ELSE SAR."TEN_KHACH_HANG"
                         END
                      ELSE SAR."NGUOI_NHAN"
                      END
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            SAR."NGUOI_NHAN",
                                                            SAR."TEN_KHACH_HANG")
                    , SAR."DIA_CHI"
                    , SAR."DIEN_GIAI"
                    , SAR."KEM_THEO_CT_GOC"
                    , SAR."TY_GIA"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = SAR."currency_id")

                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_XU_LY_CHENH_LECH")
                    , RID."STT"
                    , EX."ID_CHUNG_TU"
                    , EX."FIRST_TY_GIA_XUAT_QUY"



                -- Chiết khấu
                UNION ALL
                SELECT
                    SAR."id"
                    , 'sale.ex.giam.gia.hang.ban'                                 AS "MODEL_CHUNG_TU"
                    , SAR."NGAY_CHUNG_TU"
                    , SAr."NGAY_HACH_TOAN"
                    , SAR."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                            '') <> ''
                        THEN SAR."NGUOI_NHAN"
                         ELSE SAR."TEN_KHACH_HANG"
                         END
                      ELSE SAR."NGUOI_NHAN"
                      END                                                         AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            SAR."NGUOI_NHAN",
                                                            SAR."TEN_KHACH_HANG") AS "TEN_KHACH_HANG"
                    , SAR."DIA_CHI"
                    , SAR."DIEN_GIAI"                                             AS "DIEN_GIAI"
                    , SAR."KEM_THEO_CT_GOC"
                    , -SUM(SARD."TIEN_CHIET_KHAU")                                AS "THANH_TIEN"
                    , -SUM(SARD."TIEN_CHIET_KHAU_QUY_DOI")                        AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = SAR."currency_id")                            AS "LOAI_TIEN"
                    , CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE SAR."TY_GIA"
                      END
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CHIET_KHAU_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID")

                    , 2003 + MAX(SARD."THU_TU_SAP_XEP_CHI_TIET")                  AS sortOrder
                    , RID."STT"
                    , A."TEN_TAI_KHOAN"
                    , ''

                FROM TMP_PARAM AS RID
                    INNER JOIN sale_ex_giam_gia_hang_ban SAR ON RID."ID_CHUNG_TU" = SAR."id"
                                                                AND RID."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban SARD ON SAR."id" = SARD."GIAM_GIA_HANG_BAN_ID"
                    LEFT JOIN res_partner AO ON SAR."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON SAR."NHAN_VIEN_ID" = AOE."id"
                    LEFT JOIN danh_muc_he_thong_tai_khoan A ON a."SO_TAI_KHOAN" = (SELECT "SO_TAI_KHOAN"
                                                                                   FROM danh_muc_he_thong_tai_khoan TK
                                                                                   WHERE
                                                                                       TK.id = SARD."TK_CHIET_KHAU_ID")
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                            'sale.ex.chi.tiet.giam.gia.hang.ban'
                              )
                        AS EX ON SAR."id" = EX."ID_CHUNG_TU"
                                 AND SAR."currency_id" <> LOAI_TIEN_CHINH
                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID") LIKE N'111%'
                      AND SARD."TK_CHIET_KHAU_ID" IS NOT NULL
                      AND (SELECT "SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan TK
                           WHERE TK.id = SARD."TK_CHIET_KHAU_ID") <> ''
                      AND SARD."TIEN_CHIET_KHAU_QUY_DOI" <> 0
                      AND SAR."LOAI_CHUNG_TU" = 3551

                GROUP BY
                    SAR."id"
                    , "MODEL_CHUNG_TU"
                    , SAR."NGAY_CHUNG_TU"
                    , SAr."NGAY_HACH_TOAN"
                    , SAR."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                            '') <> ''
                        THEN SAR."NGUOI_NHAN"
                         ELSE SAR."TEN_KHACH_HANG"
                         END
                      ELSE SAR."NGUOI_NHAN"
                      END
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            SAR."NGUOI_NHAN",
                                                            SAR."TEN_KHACH_HANG")
                    , SAR."DIA_CHI"
                    , SAR."DIEN_GIAI"
                    , SAR."KEM_THEO_CT_GOC"
                    , SAR."TY_GIA"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = SAR."currency_id")

                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CHIET_KHAU_ID")
                    , RID."STT"
                    , EX."ID_CHUNG_TU"
                    , EX."FIRST_TY_GIA_XUAT_QUY"
                    , A."TEN_TAI_KHOAN"


            ;

        END IF
    ;


        IF rec."LOAI_CHUNG_TU" IN (3541, 3543, 3545) -- Hàng bán trả lại
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    SAR."id"
                    , 'sale.ex.tra.lai.hang.ban'                                  AS "MODEL_CHUNG_TU"
                    , SAR."NGAY_CHUNG_TU"
                    , SAr."NGAY_HACH_TOAN"
                    , SAR."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                            '') <> ''
                        THEN SAR."NGUOI_NHAN"
                         ELSE SAR."TEN_KHACH_HANG"
                         END
                      ELSE SAR."NGUOI_NHAN"
                      END                                                         AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            SAR."NGUOI_NHAN",
                                                            SAR."TEN_KHACH_HANG") AS "TEN_KHACH_HANG"
                    , SAR."DIA_CHI"
                    , SAR."DIEN_GIAI"                                             AS "DIEN_GIAI"
                    , SAR."KEM_THEO"
                    , /*Với bán giảm giá đại lý thì thành tiền - chiết khấu + thuế*/
                      (CASE WHEN SAR."LOAI_CHUNG_TU" = 3543
                          THEN SARD."THANH_TIEN"
                               - SARD."TIEN_CHIET_KHAU"
                               + SARD."TIEN_THUE_GTGT"
                       ELSE SARD."THANH_TIEN"
                            - SARD."TIEN_CHIET_KHAU"
                       END)                                                       AS "THANH_TIEN"
                    , (CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN CASE WHEN SAR."LOAI_CHUNG_TU" = 3541
                        THEN (CASE
                              WHEN
                                  SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY" <> 0
                                  AND SARD."CHENH_LECH" < 0
                                  THEN SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY"

                              ELSE SARD."THANH_TIEN_QUY_DOI"
                              END)

                         ELSE (CASE
                               WHEN
                                   SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY" <> 0
                                   AND SARD."CHENH_LECH" < 0
                                   THEN SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY"

                               ELSE (CASE
                                     WHEN SAR."LOAI_CHUNG_TU" = 3543
                                         THEN SARD."THANH_TIEN_QUY_DOI"
                                              - SARD."TIEN_CHIET_KHAU_QUY_DOI"
                                              + SARD."TIEN_THUE_GTGT_QUY_DOI"
                                     ELSE SARD."THANH_TIEN_QUY_DOI"
                                          - SARD."TIEN_CHIET_KHAU_QUY_DOI"
                                     END)
                               END)
                         END
                       ELSE (CASE
                             WHEN SAR."LOAI_CHUNG_TU" = 3543
                                 THEN SARD."THANH_TIEN_QUY_DOI"
                                      - SARD."TIEN_CHIET_KHAU_QUY_DOI"
                                      + SARD."TIEN_THUE_GTGT_QUY_DOI"
                             WHEN SAR."LOAI_CHUNG_TU" = 3545
                                 THEN SARD."THANH_TIEN_QUY_DOI"
                                      - SARD."TIEN_CHIET_KHAU_QUY_DOI"
                             ELSE SARD."THANH_TIEN_QUY_DOI"

                             END)
                       END)                                                       AS "THANH_TIEN_QUY_DOI"

                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = SAR."currency_id")                            AS "LOAI_TIEN"
                    , CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE SAR."TY_GIA"
                      END
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_NO_ID")

                    , (SARD."THU_TU_SAP_XEP_CHI_TIET")                            AS "STT"
                    , RID."STT"
                    , SARD."DIEN_GIAI_THUE"
                    , LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_TRA_LAI_HANG_BAN_CHI_TIET(SAR."id")


                FROM TMP_PARAM AS RID
                    INNER JOIN sale_ex_tra_lai_hang_ban SAR ON RID."ID_CHUNG_TU" = SAR."id"
                                                               AND
                                                               SAR."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet SARD ON SAR."id" = SARD."TRA_LAI_HANG_BAN_ID"
                    LEFT JOIN res_partner AO ON SAR."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON SAR."NHAN_VIEN_ID" = AOE."id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                            'sale.ex.tra.lai.hang.ban.chi.tiet'
                              )
                        AS EX ON SAR."id" = EX."ID_CHUNG_TU"
                                 AND SAR."currency_id" <> LOAI_TIEN_CHINH

                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID") LIKE '111%%'


                UNION ALL
                /*Dòng xử lý chênh lệch tỷ giá tiền hàng*/
                SELECT
                    SAR."id"
                    , 'sale.ex.tra.lai.hang.ban'                                                       AS "MODEL_CHUNG_TU"
                    , SAR."NGAY_CHUNG_TU"
                    , SAr."NGAY_HACH_TOAN"
                    , SAR."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                            '') <> ''
                        THEN SAR."NGUOI_NHAN"
                         ELSE SAR."TEN_KHACH_HANG"
                         END
                      ELSE SAR."NGUOI_NHAN"
                      END                                                                              AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            SAR."NGUOI_NHAN",
                                                            SAR."TEN_KHACH_HANG")                      AS "TEN_KHACH_HANG"
                    , SAR."DIA_CHI"
                    , SAR."DIEN_GIAI"                                                                  AS "DIEN_GIAI"
                    , SAR."KEM_THEO"
                    , 0                                                                                AS "THANH_TIEN"
                    , SUM(CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                    AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN (CASE WHEN
                        SARD."CHENH_LECH" <> 0
                        THEN SARD."CHENH_LECH"

                          ELSE 0
                          END)
                          ELSE 0
                          END)                                                                         AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = SAR."currency_id")                                                 AS "LOAI_TIEN"
                    , CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE SAR."TY_GIA"
                      END
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_XU_LY_CHENH_LECH")

                    , 900 + MAX(SARD."THU_TU_SAP_XEP_CHI_TIET")                                        AS "STT"
                    , RID."STT"
                    , CASE WHEN SAR."LOAI_CHUNG_TU" = 3541
                    THEN N'Xử lý chênh lệch tỷ giá tiền hàng'
                      ELSE N'Xử lý chênh lệch tỷ giá tổng tiền thanh toán'
                      END                                                                                 "DIEN_GIAI"
                    , LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_TRA_LAI_HANG_BAN_CHI_TIET(SAR."id") AS "TK_CONG_NO"


                FROM TMP_PARAM AS RID
                    INNER JOIN sale_ex_tra_lai_hang_ban SAR ON RID."ID_CHUNG_TU" = SAR."id"
                                                               AND RID."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet SARD ON SAR."id" = SARD."TRA_LAI_HANG_BAN_ID"
                    LEFT JOIN res_partner AO ON SAR."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON SAR."NHAN_VIEN_ID" = AOE."id"
                    INNER JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                             'sale.ex.tra.lai.hang.ban.chi.tiet'
                               )
                        AS EX ON SAR."id" = EX."ID_CHUNG_TU"
                                 AND SAR."currency_id" <> LOAI_TIEN_CHINH
                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID") LIKE N'111%'
                      AND ((SARD."CHENH_LECH" > 0

                )
                      )


                GROUP BY
                    SAR."id",
                    "MODEL_CHUNG_TU",
                    SAR."NGAY_CHUNG_TU",
                    SAr."NGAY_HACH_TOAN",
                    SAR."SO_CHUNG_TU",
                    CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                        THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                                '') <> ''
                            THEN SAR."NGUOI_NHAN"
                             ELSE SAR."TEN_KHACH_HANG"
                             END
                    ELSE SAR."NGUOI_NHAN"
                    END,
                    AO."MA",
                    SAR."TEN_KHACH_HANG",
                    LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                          SAR."NGUOI_NHAN",
                                                          SAR."TEN_KHACH_HANG"),
                    SAR."DIA_CHI",
                    SAR."DIEN_GIAI",
                    SAR."KEM_THEO",
                    (SELECT "MA_LOAI_TIEN"
                     FROM res_currency T
                     WHERE T.id = SAR."currency_id"),

                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = SARD."TK_CO_ID"),
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = SARD."TK_XU_LY_CHENH_LECH"),
                    RID."STT",
                    EX."ID_CHUNG_TU",
                    EX."FIRST_TY_GIA_XUAT_QUY"
                    , CASE WHEN SAR."LOAI_CHUNG_TU" = 3541
                    THEN N'Xử lý chênh lệch tỷ giá tiền hàng'
                      ELSE N'Xử lý chênh lệch tỷ giá tổng tiền thanh toán'
                      END
                    , SAR."LOAI_CHUNG_TU"



                -- Lấy các dòng Thuế giá trị gia tăng
                UNION ALL
                SELECT
                    SAR."id"
                    , 'sale.ex.tra.lai.hang.ban'                                  AS "MODEL_CHUNG_TU"
                    , SAR."NGAY_CHUNG_TU"
                    , SAr."NGAY_HACH_TOAN"
                    , SAR."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                            '') <> ''
                        THEN SAR."NGUOI_NHAN"
                         ELSE SAR."TEN_KHACH_HANG"
                         END
                      ELSE SAR."NGUOI_NHAN"
                      END                                                         AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            SAR."NGUOI_NHAN",
                                                            SAR."TEN_KHACH_HANG") AS "TEN_KHACH_HANG"
                    , SAR."DIA_CHI"
                    , SAR."DIEN_GIAI"                                             AS "DIEN_GIAI"
                    , SAR."KEM_THEO"
                    , SUM(SARD."TIEN_THUE_GTGT")                                  AS "THANH_TIEN"
                    ,
                    /*Với phiếu chi PS ngoại tệ và có xử lý chênh lệch tỷ giá xuất quỹ thi thực hiện lấy số tiền quy đổi theo tỷ giá xuất quỹ, ngược lại thì lấy quy đổi*/
                      SUM((CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                     AND EX."ID_CHUNG_TU" IS NOT NULL
                          THEN (CASE
                                WHEN
                                    SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY" <> 0
                                    AND SARD."CHENH_LECH_TIEN_THUE_GTGT" < 0
                                    THEN SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY"

                                ELSE SARD."TIEN_THUE_GTGT_QUY_DOI"
                                END)
                           ELSE SARD."TIEN_THUE_GTGT_QUY_DOI"
                           END))                                                  AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = SAR."currency_id")                            AS "LOAI_TIEN"
                    , CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE SAR."TY_GIA"
                      END
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_THUE_GTGT_ID")
                    , 1499 + MAX(SARD."THU_TU_SAP_XEP_CHI_TIET")                  AS sortOrder
                    , RID."STT"
                    , A."TEN_TAI_KHOAN"
                    , ''


                FROM TMP_PARAM AS RID
                    INNER JOIN sale_ex_tra_lai_hang_ban SAR ON RID."ID_CHUNG_TU" = SAR."id"
                                                               AND RID."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet SARD ON SAR."id" = SARD."TRA_LAI_HANG_BAN_ID"
                    LEFT JOIN res_partner AO ON SAR."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON SAR."NHAN_VIEN_ID" = AOE."id"
                    LEFT JOIN danh_muc_he_thong_tai_khoan A ON a."SO_TAI_KHOAN" = (SELECT "SO_TAI_KHOAN"
                                                                                   FROM danh_muc_he_thong_tai_khoan TK
                                                                                   WHERE TK.id = SARD."TK_THUE_GTGT_ID")
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                            'sale.ex.tra.lai.hang.ban.chi.tiet'
                              )
                        AS EX ON SAR."id" = EX."ID_CHUNG_TU"
                                 AND SAR."currency_id" <> LOAI_TIEN_CHINH

                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID") LIKE N'111%%'
                      AND SARD."TK_THUE_GTGT_ID" IS NOT NULL
                      AND (SELECT "SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan TK
                           WHERE TK.id = SARD."TK_THUE_GTGT_ID") <> ''
                      AND SARD."TIEN_THUE_GTGT_QUY_DOI" <> 0
                      AND SAR."LOAI_CHUNG_TU" = 3541
                GROUP BY
                    SAR."id",
                    "MODEL_CHUNG_TU",
                    SAR."NGAY_CHUNG_TU",
                    SAr."NGAY_HACH_TOAN",
                    SAR."SO_CHUNG_TU",
                    CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                        THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                                '') <> ''
                            THEN SAR."NGUOI_NHAN"
                             ELSE SAR."TEN_KHACH_HANG"
                             END
                    ELSE SAR."NGUOI_NHAN"
                    END,
                    AO."MA",
                    SAR."TEN_KHACH_HANG",
                    LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                          SAR."NGUOI_NHAN",
                                                          SAR."TEN_KHACH_HANG"),
                    SAR."DIA_CHI",
                    SAR."DIEN_GIAI",
                    SAR."KEM_THEO",
                    (SELECT "MA_LOAI_TIEN"
                     FROM res_currency T
                     WHERE T.id = SAR."currency_id"),

                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = SARD."TK_CO_ID"),
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = SARD."TK_THUE_GTGT_ID"),
                    RID."STT",
                    EX."ID_CHUNG_TU",
                    EX."FIRST_TY_GIA_XUAT_QUY"
                    , A."TEN_TAI_KHOAN"

                UNION ALL
                /*Dòng xử lý chênh lệch tỷ giá tiền thuế*/
                SELECT
                    SAR."id"
                    , 'sale.ex.tra.lai.hang.ban'                                  AS "MODEL_CHUNG_TU"
                    , SAR."NGAY_CHUNG_TU"
                    , SAr."NGAY_HACH_TOAN"
                    , SAR."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                            '') <> ''
                        THEN SAR."NGUOI_NHAN"
                         ELSE SAR."TEN_KHACH_HANG"
                         END
                      ELSE SAR."NGUOI_NHAN"
                      END                                                         AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            SAR."NGUOI_NHAN",
                                                            SAR."TEN_KHACH_HANG") AS "TEN_KHACH_HANG"
                    , SAR."DIA_CHI"
                    , SAR."DIEN_GIAI"                                             AS "DIEN_GIAI"
                    , SAR."KEM_THEO"
                    , 0                                                           AS "THANH_TIEN"
                    , SUM(CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                    AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN (CASE WHEN
                        SARD."CHENH_LECH_TIEN_THUE_GTGT" <> 0
                        THEN SARD."CHENH_LECH_TIEN_THUE_GTGT"

                          ELSE 0
                          END)
                          ELSE 0
                          END)                                                    AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = SAR."currency_id")                            AS "LOAI_TIEN"
                    , CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE SAR."TY_GIA"
                      END
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_XU_LY_CHENH_LECH")
                    , 1500 + MAX(SARD."THU_TU_SAP_XEP_CHI_TIET")                  AS sortOrder
                    , RID."STT"
                    , N'Xử lý chênh lệch tỷ giá tiền thuế'
                    , ''

                FROM TMP_PARAM AS RID
                    INNER JOIN sale_ex_tra_lai_hang_ban SAR ON RID."ID_CHUNG_TU" = SAR."id"
                                                               AND RID."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet SARD ON SAR."id" = SARD."TRA_LAI_HANG_BAN_ID"
                    LEFT JOIN res_partner AO ON SAR."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON SAR."NHAN_VIEN_ID" = AOE."id"
                    INNER JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                             'sale.ex.tra.lai.hang.ban.chi.tiet'
                               )
                        AS EX ON SAR."id" = EX."ID_CHUNG_TU"
                                 AND SAR."currency_id" <> LOAI_TIEN_CHINH
                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID") LIKE N'111%'
                      AND SARD."TK_THUE_GTGT_ID" IS NOT NULL
                      AND (SELECT "SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan TK
                           WHERE TK.id = SARD."TK_THUE_GTGT_ID") <> ''
                      AND SARD."TIEN_THUE_GTGT_QUY_DOI" <> 0
                      AND SAR."LOAI_CHUNG_TU" = 3541
                      AND ((SARD."CHENH_LECH_TIEN_THUE_GTGT" > 0

                )
                      )
                GROUP BY
                    SAR."id",
                    "MODEL_CHUNG_TU",
                    SAR."NGAY_CHUNG_TU",
                    SAr."NGAY_HACH_TOAN",
                    SAR."SO_CHUNG_TU",
                    CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                        THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                                '') <> ''
                            THEN SAR."NGUOI_NHAN"
                             ELSE SAR."TEN_KHACH_HANG"
                             END
                    ELSE SAR."NGUOI_NHAN"
                    END,
                    AO."MA",
                    SAR."TEN_KHACH_HANG",
                    LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                          SAR."NGUOI_NHAN",
                                                          SAR."TEN_KHACH_HANG"),
                    SAR."DIA_CHI",
                    SAR."DIEN_GIAI",
                    SAR."KEM_THEO",
                    (SELECT "MA_LOAI_TIEN"
                     FROM res_currency T
                     WHERE T.id = SAR."currency_id"),

                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = SARD."TK_CO_ID"),
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = SARD."TK_XU_LY_CHENH_LECH"),
                    RID."STT",
                    EX."ID_CHUNG_TU",
                    EX."FIRST_TY_GIA_XUAT_QUY"


                -- chiết khấu
                UNION ALL
                SELECT
                    SAR."id"
                    , 'sale.ex.tra.lai.hang.ban'                                  AS "MODEL_CHUNG_TU"
                    , SAR."NGAY_CHUNG_TU"
                    , SAr."NGAY_HACH_TOAN"
                    , SAR."SO_CHUNG_TU"
                    , CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                    THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                            '') <> ''
                        THEN SAR."NGUOI_NHAN"
                         ELSE SAR."TEN_KHACH_HANG"
                         END
                      ELSE SAR."NGUOI_NHAN"
                      END                                                         AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            SAR."NGUOI_NHAN",
                                                            SAR."TEN_KHACH_HANG") AS "TEN_KHACH_HANG"
                    , SAR."DIA_CHI"
                    , SAR."DIEN_GIAI"                                             AS "DIEN_GIAI"
                    , SAR."KEM_THEO"
                    , -SUM(SARD."TIEN_CHIET_KHAU")                                AS "THANH_TIEN"
                    , -SUM(SARD."TIEN_CHIET_KHAU_QUY_DOI")                        AS "THANH_TIEN_QUY_DOI"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = SAR."currency_id")                            AS "LOAI_TIEN"
                    , CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                      ELSE SAR."TY_GIA"
                      END
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CHIET_KHAU")
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID")
                    , 2000 + MAX(SARD."THU_TU_SAP_XEP_CHI_TIET")                  AS sortOrder
                    , RID."STT"
                    , A."TEN_TAI_KHOAN"
                    , ''

                FROM TMP_PARAM AS RID
                    INNER JOIN sale_ex_tra_lai_hang_ban SAR ON RID."ID_CHUNG_TU" = SAR."id"
                                                               AND RID."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                    INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet SARD ON SAR."id" = SARD."TRA_LAI_HANG_BAN_ID"
                    LEFT JOIN res_partner AO ON SAR."DOI_TUONG_ID" = AO."id"
                    LEFT JOIN res_partner AOE ON SAR."NHAN_VIEN_ID" = AOE."id"
                    LEFT JOIN danh_muc_he_thong_tai_khoan A ON a."SO_TAI_KHOAN" = (SELECT "SO_TAI_KHOAN"
                                                                                   FROM danh_muc_he_thong_tai_khoan TK
                                                                                   WHERE TK.id = SARD."TK_CHIET_KHAU")
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListRefID,
                                                                            'sale.ex.tra.lai.hang.ban.chi.tiet'
                              )
                        AS EX ON SAR."id" = EX."ID_CHUNG_TU"
                                 AND SAR."currency_id" <> LOAI_TIEN_CHINH
                WHERE (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = SARD."TK_CO_ID") LIKE N'111%'
                      AND SARD."TK_CHIET_KHAU" IS NOT NULL
                      AND (SELECT "SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan TK
                           WHERE TK.id = SARD."TK_CHIET_KHAU") <> ''
                      AND SARD."TIEN_CHIET_KHAU_QUY_DOI" <> 0
                      AND SAR."LOAI_CHUNG_TU" = 3541

                GROUP BY
                    SAR."id",
                    "MODEL_CHUNG_TU",
                    SAR."NGAY_CHUNG_TU",
                    SAr."NGAY_HACH_TOAN",
                    SAR."SO_CHUNG_TU",
                    CASE WHEN AO."LOAI_KHACH_HANG" = '1'
                        THEN CASE WHEN COALESCE(SAR."NGUOI_NHAN",
                                                '') <> ''
                            THEN SAR."NGUOI_NHAN"
                             ELSE SAR."TEN_KHACH_HANG"
                             END
                    ELSE SAR."NGUOI_NHAN"
                    END,
                    AO."MA",
                    SAR."TEN_KHACH_HANG",
                    LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                          SAR."NGUOI_NHAN",
                                                          SAR."TEN_KHACH_HANG"),
                    SAR."DIA_CHI",
                    SAR."DIEN_GIAI",
                    SAR."KEM_THEO",
                    (SELECT "MA_LOAI_TIEN"
                     FROM res_currency T
                     WHERE T.id = SAR."currency_id"),

                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = SARD."TK_CO_ID"),
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = SARD."TK_CHIET_KHAU"),
                    RID."STT",
                    EX."ID_CHUNG_TU",
                    EX."FIRST_TY_GIA_XUAT_QUY"
                    , A."TEN_TAI_KHOAN"


            ;

        END IF
    ;

    END LOOP
    ;


END $$

;


SELECT *
FROM TMP_KET_QUA
--WHERE "SO_CHUNG_TU" = 'PC00005' --AND "DIEN_GIAI_DETAIL" =N'Tủ lạnh Toshiba 110 lít'
ORDER BY
    "MasterSortOrder",
    "NGAY_CHUNG_TU",
    "SO_CHUNG_TU",
    "STT"
        """
		sql_result = self.execute(query)
		dic_tk_cong_no  = {}
      
		for line in sql_result:
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))

			if key not in dic_tk_cong_no:
				dic_tk_cong_no[key] = []
			
			if line.get('TK_CONG_NO') and line.get('TK_CONG_NO') not in dic_tk_cong_no[key]:
				dic_tk_cong_no[key] += [line.get('TK_CONG_NO')]

			master_data = self.env['bao.cao.phieu.chi.mau.day.du'].convert_for_update(line)
			detail_data = self.env['bao.cao.phieu.chi.mau.day.du.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
				records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.phieu.chi.mau.day.du.chi.tiet'].new(detail_data)
		
		for key in records:
			if key in dic_tk_cong_no:
				records[key].TK_CONG_NO = ', '.join(dic_tk_cong_no[key])
           

		docs = [records.get(k) for k in records]

		for record in docs:
			
			strNgayChungTu = ''
			if not record.NGAY_CHUNG_TU:
				record.NGAY_CHUNG_TU = strNgayChungTu
			else:
				strNgayChungTu = record.NGAY_CHUNG_TU
			record.NGAY_CHUNG_TU = strNgayChungTu

			if not record.LOAI_TIEN:
				record.currency_id = self.lay_loai_tien_mac_dinh()
			else:
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', record.LOAI_TIEN)],limit=1)
				if loai_tien_id:
					record.currency_id = loai_tien_id.id

			tong_tien = 0
			for line in record.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
				line.currency_id = record.currency_id
				tong_tien += line.THANH_TIEN
			record.TONG_TIEN = tong_tien

			cot_st_nguyen_te = 'Số tiền nguyên tệ'
			cot_st= 'Số tiền'
			if not record.LOAI_TIEN:
				cot_st_nguyen_te += " (VND)"
				cot_st += " (VND)"
			else:
				cot_st_nguyen_te += " (" + record.LOAI_TIEN +")"
				cot_st += " (" + record.LOAI_TIEN +")"
			record.TIEU_DE_COT_STNT = cot_st_nguyen_te
			record.TIEU_DE_COT_ST = cot_st
            
           
        
        ####################### END SQL #######################

        # Tạo object để in
        
		return {
			'docs':docs,
		}



	@api.model_cr
	def init(self):
		self.env.cr.execute(""" 
		DROP FUNCTION IF EXISTS LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU( IN ID_CHUNG_TU INT ) --Func_GetParentCreditAccountOfCAPaymentDetail
		;

		CREATE OR REPLACE FUNCTION LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU(IN ID_CHUNG_TU INT)
			RETURNS VARCHAR
		AS $$
		DECLARE
			TAI_KHOAN           VARCHAR(255);

			TONG_TAI_KHOAN      INT;

			TAI_KHOAN_PHAN_TRAM VARCHAR(255);


		BEGIN
			-- Lấy về tài khoản "TK_CO"

			-- Lấy "TK_CO" nhỏ nhất
			TAI_KHOAN = (SELECT (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = CAD."TK_CO_ID")
						 FROM account_ex_phieu_thu_chi_tiet CAD
							 INNER JOIN danh_muc_he_thong_tai_khoan ACC ON (SELECT "SO_TAI_KHOAN"
																			FROM danh_muc_he_thong_tai_khoan TK
																			WHERE TK.id = CAD."TK_CO_ID") = ACC."SO_TAI_KHOAN"
						 WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU
							   AND (SELECT "SO_TAI_KHOAN"
									FROM danh_muc_he_thong_tai_khoan TK
									WHERE TK.id = CAD."TK_CO_ID") LIKE N'111%%'
						 ORDER BY ACC."BAC",
							 CAD."TK_CO_ID"
						 LIMIT 1
			)
			;

			TONG_TAI_KHOAN = (SELECT COUNT(*)
							  FROM account_ex_phieu_thu_chi_tiet CAD
							  WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU
									AND (SELECT "SO_TAI_KHOAN"
										 FROM danh_muc_he_thong_tai_khoan TK
										 WHERE TK.id = CAD."TK_CO_ID") LIKE N'111%%'
			)
			;

			TAI_KHOAN_PHAN_TRAM = TAI_KHOAN || '%%'
			;

			-- Trường hợp Count theo "TK_CO"%% nhỏ nhất không bằng tổng số "TK_CO" thì lấy Parent của "TK_CO" nhỏ nhất
			IF TONG_TAI_KHOAN <> (SELECT COUNT(*)
								  FROM account_ex_phieu_thu_chi_tiet CAD
								  WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU
										AND (SELECT "SO_TAI_KHOAN"
											 FROM danh_muc_he_thong_tai_khoan TK
											 WHERE TK.id = CAD."TK_CO_ID") LIKE TAI_KHOAN_PHAN_TRAM
			)
			THEN
				TAI_KHOAN = (SELECT "SO_TAI_KHOAN"
							 FROM danh_muc_he_thong_tai_khoan
							 WHERE "id" = (SELECT "parent_id"
										   FROM danh_muc_he_thong_tai_khoan
										   WHERE "SO_TAI_KHOAN" = TAI_KHOAN
							 )
				)
				;
			END IF
			;

			IF TAI_KHOAN IS NULL
			   OR TAI_KHOAN = ''
			THEN
				TAI_KHOAN = '111'
				;
			END IF
			;

			RETURN TAI_KHOAN
			;

		END
		;
		$$ LANGUAGE PLpgSQL
		;


		-- SELECT * FROM  LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU( 15 )


		""")

		self.env.cr.execute(""" 
		DROP FUNCTION IF EXISTS LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_HANG_CHI_TIET( IN ID_CHUNG_TU INT, TK_CO VARCHAR(255) ) --Func_GetParentCreditAccountOfPUVoucherDetail
;

CREATE OR REPLACE FUNCTION LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_HANG_CHI_TIET(IN ID_CHUNG_TU INT,
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
				DROP FUNCTION IF EXISTS LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_DICH_VU_CHI_TIET( IN ID_CHUNG_TU INT ) --Func_GetParentCreditAccountOfPUServiceDetail
		;

		CREATE OR REPLACE FUNCTION LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_MUA_DICH_VU_CHI_TIET(IN ID_CHUNG_TU INT)
			RETURNS VARCHAR
		AS $$
		DECLARE
			TAI_KHOAN           VARCHAR(255);

			TONG_TAI_KHOAN      INT;

			TAI_KHOAN_PHAN_TRAM VARCHAR(255);


		BEGIN
			-- Lấy về tài khoản "TK_CO"

			-- Lấy "TK_CO" nhỏ nhất
			TAI_KHOAN = (SELECT (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = CAD."TK_CO_ID")
						 FROM purchase_document_line CAD
							 INNER JOIN danh_muc_he_thong_tai_khoan ACC ON (SELECT "SO_TAI_KHOAN"
																			FROM danh_muc_he_thong_tai_khoan TK
																			WHERE TK.id = CAD."TK_CO_ID") = ACC."SO_TAI_KHOAN"
						 WHERE CAD."order_id" = ID_CHUNG_TU
							   AND (SELECT "SO_TAI_KHOAN"
									FROM danh_muc_he_thong_tai_khoan TK
									WHERE TK.id = CAD."TK_CO_ID") LIKE N'111%%'
						 ORDER BY ACC."BAC",
							 (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = CAD."TK_CO_ID")
						 LIMIT 1
			)
			;

			TONG_TAI_KHOAN = (SELECT COUNT(*)
							  FROM purchase_document_line CAD
							  WHERE CAD."order_id" = ID_CHUNG_TU
									AND (SELECT "SO_TAI_KHOAN"
										 FROM danh_muc_he_thong_tai_khoan TK
										 WHERE TK.id = CAD."TK_CO_ID") LIKE N'111%%'
			)
			;

			TAI_KHOAN_PHAN_TRAM = TAI_KHOAN || '%%'
			;

			-- Trường hợp Count theo "TK_CO"%% nhỏ nhất không bằng tổng số "TK_CO" thì lấy Parent của "TK_CO" nhỏ nhất
			IF TONG_TAI_KHOAN <> (SELECT COUNT(*)
								  FROM purchase_document_line CAD
								  WHERE CAD."order_id" = ID_CHUNG_TU
										AND (SELECT "SO_TAI_KHOAN"
											 FROM danh_muc_he_thong_tai_khoan TK
											 WHERE TK.id = CAD."TK_CO_ID") LIKE TAI_KHOAN_PHAN_TRAM
			)
			THEN
				TAI_KHOAN = (SELECT "SO_TAI_KHOAN"
							 FROM danh_muc_he_thong_tai_khoan
							 WHERE "id" = (SELECT "parent_id"
										   FROM danh_muc_he_thong_tai_khoan
										   WHERE "SO_TAI_KHOAN" = TAI_KHOAN
							 )
				)
				;
			END IF
			;

			IF TAI_KHOAN IS NULL
			   OR TAI_KHOAN = ''
			THEN
				TAI_KHOAN = '111'
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
					DROP FUNCTION IF EXISTS LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_GIAM_GIA_HANG_BAN_CHI_TIET( IN ID_CHUNG_TU INT ) --Func_GetParentCreditAccountOfSADiscountDetail
		;

		CREATE OR REPLACE FUNCTION LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_GIAM_GIA_HANG_BAN_CHI_TIET(IN ID_CHUNG_TU INT)
			RETURNS VARCHAR
		AS $$
		DECLARE
			TAI_KHOAN           VARCHAR(255);

			TONG_TAI_KHOAN      INT;

			TAI_KHOAN_PHAN_TRAM VARCHAR(255);


		BEGIN
			-- Lấy về tài khoản "TK_CO"

			-- Lấy "TK_CO" nhỏ nhất
			TAI_KHOAN = (SELECT (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = CAD."TK_CO_ID")
						 FROM sale_ex_chi_tiet_giam_gia_hang_ban CAD
							 INNER JOIN danh_muc_he_thong_tai_khoan ACC ON (SELECT "SO_TAI_KHOAN"
																			FROM danh_muc_he_thong_tai_khoan TK
																			WHERE TK.id = CAD."TK_CO_ID") = ACC."SO_TAI_KHOAN"
						 WHERE CAD."GIAM_GIA_HANG_BAN_ID" = ID_CHUNG_TU
							   AND (SELECT "SO_TAI_KHOAN"
									FROM danh_muc_he_thong_tai_khoan TK
									WHERE TK.id = CAD."TK_CO_ID") LIKE N'111%%'
						 ORDER BY ACC."BAC",
							 (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = CAD."TK_CO_ID")
						 LIMIT 1
			)
			;

			TONG_TAI_KHOAN = (SELECT COUNT(*)
							  FROM sale_ex_chi_tiet_giam_gia_hang_ban CAD
							  WHERE CAD."GIAM_GIA_HANG_BAN_ID" = ID_CHUNG_TU
									AND (SELECT "SO_TAI_KHOAN"
										 FROM danh_muc_he_thong_tai_khoan TK
										 WHERE TK.id = CAD."TK_CO_ID") LIKE N'111%%'
			)
			;

			TAI_KHOAN_PHAN_TRAM = TAI_KHOAN || '%%'
			;

			-- Trường hợp Count theo "TK_CO"%% nhỏ nhất không bằng tổng số "TK_CO" thì lấy Parent của "TK_CO" nhỏ nhất
			IF TONG_TAI_KHOAN <> (SELECT COUNT(*)
								  FROM sale_ex_chi_tiet_giam_gia_hang_ban CAD
								  WHERE CAD."GIAM_GIA_HANG_BAN_ID" = ID_CHUNG_TU
										AND (SELECT "SO_TAI_KHOAN"
											 FROM danh_muc_he_thong_tai_khoan TK
											 WHERE TK.id = CAD."TK_CO_ID") LIKE TAI_KHOAN_PHAN_TRAM
			)
			THEN
				TAI_KHOAN = (SELECT "SO_TAI_KHOAN"
							 FROM danh_muc_he_thong_tai_khoan
							 WHERE "id" = (SELECT "parent_id"
										   FROM danh_muc_he_thong_tai_khoan
										   WHERE "SO_TAI_KHOAN" = TAI_KHOAN
							 )
				)
				;
			END IF
			;

			IF TAI_KHOAN IS NULL
			   OR TAI_KHOAN = ''
			THEN
				TAI_KHOAN = '111'
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
					DROP FUNCTION IF EXISTS LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_TRA_LAI_HANG_BAN_CHI_TIET( IN ID_CHUNG_TU INT ) --Func_GetParentCreditAccountOfSADiscountDetail
		;

		CREATE OR REPLACE FUNCTION LAY_TAI_KHOAN_TONG_HOP_CHUNG_TK_NO_PHIEU_THU_TRA_LAI_HANG_BAN_CHI_TIET(IN ID_CHUNG_TU INT)
			RETURNS VARCHAR
		AS $$
		DECLARE
			TAI_KHOAN           VARCHAR(255);

			TONG_TAI_KHOAN      INT;

			TAI_KHOAN_PHAN_TRAM VARCHAR(255);


		BEGIN
			-- Lấy về tài khoản "TK_CO"

			-- Lấy "TK_CO" nhỏ nhất
			TAI_KHOAN = (SELECT (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = CAD."TK_CO_ID")
						 FROM sale_ex_tra_lai_hang_ban_chi_tiet CAD
							 INNER JOIN danh_muc_he_thong_tai_khoan ACC ON (SELECT "SO_TAI_KHOAN"
																			FROM danh_muc_he_thong_tai_khoan TK
																			WHERE TK.id = CAD."TK_CO_ID") = ACC."SO_TAI_KHOAN"
						 WHERE CAD."TRA_LAI_HANG_BAN_ID" = ID_CHUNG_TU
							   AND (SELECT "SO_TAI_KHOAN"
									FROM danh_muc_he_thong_tai_khoan TK
									WHERE TK.id = CAD."TK_CO_ID") LIKE N'111%%'
						 ORDER BY ACC."BAC",
							 (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = CAD."TK_CO_ID")
						 LIMIT 1
			)
			;

			TONG_TAI_KHOAN = (SELECT COUNT(*)
							  FROM sale_ex_tra_lai_hang_ban_chi_tiet CAD
							  WHERE CAD."TRA_LAI_HANG_BAN_ID" = ID_CHUNG_TU
									AND (SELECT "SO_TAI_KHOAN"
										 FROM danh_muc_he_thong_tai_khoan TK
										 WHERE TK.id = CAD."TK_CO_ID") LIKE N'111%%'
			)
			;

			TAI_KHOAN_PHAN_TRAM = TAI_KHOAN || '%%'
			;

			-- Trường hợp Count theo "TK_CO"%% nhỏ nhất không bằng tổng số "TK_CO" thì lấy Parent của "TK_CO" nhỏ nhất
			IF TONG_TAI_KHOAN <> (SELECT COUNT(*)
								  FROM sale_ex_tra_lai_hang_ban_chi_tiet CAD
								  WHERE CAD."TRA_LAI_HANG_BAN_ID" = ID_CHUNG_TU
										AND (SELECT "SO_TAI_KHOAN"
											 FROM danh_muc_he_thong_tai_khoan TK
											 WHERE TK.id = CAD."TK_CO_ID") LIKE TAI_KHOAN_PHAN_TRAM
			)
			THEN
				TAI_KHOAN = (SELECT "SO_TAI_KHOAN"
							 FROM danh_muc_he_thong_tai_khoan
							 WHERE "id" = (SELECT "parent_id"
										   FROM danh_muc_he_thong_tai_khoan
										   WHERE "SO_TAI_KHOAN" = TAI_KHOAN
							 )
				)
				;
			END IF
			;

			IF TAI_KHOAN IS NULL
			   OR TAI_KHOAN = ''
			THEN
				TAI_KHOAN = '111'
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
