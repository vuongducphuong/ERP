# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_02TT_PHIEU_CHI(models.Model):
    _name = 'bao.cao.02tt.phieu.chi'
    _auto = False

    ref = fields.Char(string='Reffence ID')
    ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
    MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')
    NGUOI_NHAN_NGUOI_NOP =  fields.Char(string='Người nhận người nộp')#ContactName
    NGAY_CHUNG_TU =  fields.Date(string='Ngày chứng từ') #RefDate
    NGAY_HACH_TOAN =  fields.Date(string='Ngày hạch toán') #PostedDate
    SO_CHUNG_TU =  fields.Char(string='Số chứng từ') #RefNo
    MA_KHACH_HANG =  fields.Char(string='Mã khách hàng') #AccountObjectCode
    TEN_KHACH_HANG =  fields.Char(string='Tên khách hàng') #AccountObjectName
    DIA_CHI =  fields.Char(string='Địa chỉ') #AccountObjectAddress
    DIEN_GIAI =  fields.Char(string='Diễn giải') #JournalMemo
    LOAI_TIEN =  fields.Char(string='Loại tiền') #CurrencyID
    TY_GIA =  fields.Monetary(string='Tỷ giá', currency_field='currency_id') #ExchangeRate
    SO_CT_GOC_KEM_THEO =  fields.Integer(string='Số chứng từ kèm theo') #DocumentIncluded

    TK_NO = fields.Char(string='TK Nợ', help='Tài khoản nợ')#DebitAccount
    TK_CO = fields.Char(string='TK Có', help='Tài khoản có')#CreditAccount
    

    
    LOAI_KHACH_HANG =  fields.Integer(string='Loại đối tượng') #AccountObjectType

    TONG_TIEN =  fields.Monetary(string='Tổng tiền', currency_field='currency_id')
    TONG_TIEN_QUY_DOI =  fields.Monetary(string='Tổng tiền quy đổi', currency_field='currency_id')
    
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())

    ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.02tt.phieu.chi.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')

    
class BAO_CAO_02TT_PHIEU_CHI_REPORT(models.AbstractModel):
    _name = 'report.bao_cao.template_v02_tt'

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
        "DIEN_GIAI_DETAIL"            VARCHAR(255)


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
                    , SUM(CASE WHEN (SELECT "SO_TAI_KHOAN"
                                     FROM danh_muc_he_thong_tai_khoan TK
                                     WHERE TK.id = CAPD."TK_CO_ID") LIKE N'111%%'
                    THEN CAPD."SO_TIEN"
                          ELSE -1 * CAPD."SO_TIEN"
                          END)                                                   AS "THANH_TIEN"
                    , SUM(CASE WHEN (SELECT "SO_TAI_KHOAN"
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
                       WHERE TK.id = CAPD."TK_NO_ID")                            AS "TK_NO"
                    , MIN(CAPD."THU_TU_SAP_XEP_CHI_TIET")                        AS "STT"
                    , RID."STT"
                    ,CAPD."DIEN_GIAI_DETAIL"

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
                    CAP."TY_GIA",
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = CAPD."TK_CO_ID"),
                    (SELECT "SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = CAPD."TK_NO_ID"),

                    RID."STT",
                    EX."ID_CHUNG_TU",
                    EX."FIRST_TY_GIA_XUAT_QUY"
                  ,CAPD."DIEN_GIAI_DETAIL"


            ;

        END IF
    ;


        IF rec."LOAI_CHUNG_TU" IN (307, 313, 357, 363)
        THEN
            INSERT INTO TMP_KET_QUA
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


                 AS   "SO_CHUNG_TU"
                    , PUI."NGUOI_NHAN"                                           AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            PUI."NGUOI_NHAN",
                                                            PUI."TEN_DOI_TUONG") AS "TEN_KHACH_HANG"
                    , PUI."DIA_CHI"
                    , PUI."LY_DO_CHI"                                            AS "DIEN_GIAI"
                    , PUI."KEM_THEO_PC"
                    , SUM(PUID."THANH_TIEN" - PUID."TIEN_CHIET_KHAU"
                          + CASE WHEN PUID."TK_THUE_GTGT_ID" IS NULL
                    THEN PUID."TIEN_THUE_GTGT"
                            ELSE 0
                            END)                                                 AS "THANH_TIEN"
                    ,
                    /*Với phiếu chi PS ngoại tệ và có xử lý chênh lệch tỷ giá xuất quỹ thi thực hiện lấy số tiền quy đổi theo tỷ giá xuất quỹ, ngược lại thì lấy quy đổi*/
                      SUM((CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                     AND EX."ID_CHUNG_TU" IS NOT NULL
                          THEN (CASE
                                WHEN
                                    PUID."THANH_TIEN_SAU_TY_GIA_XUAT_QUY" <> 0
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
                       WHERE TK.id = PUID."TK_NO_ID")
                    , MIN(PUID."THU_TU_SAP_XEP_CHI_TIET")                        AS sortOrder
                    , RID."STT"
                      ,PUID."name"

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
                GROUP BY
                    PUI."id",
                    "MODEL_CHUNG_TU",
                    PUI."NGAY_CHUNG_TU",
                    PUI."NGAY_HACH_TOAN",
                    PUI."SO_CHUNG_TU",

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
                     WHERE TK.id = PUID."TK_NO_ID"),

                    PUI."LY_DO_CHI",
                    (SELECT "MA_LOAI_TIEN"
                     FROM res_currency T
                     WHERE T.id = PUI."currency_id"),
                    PUI."TY_GIA",
                    RID."STT",
                    EX."ID_CHUNG_TU",
                    EX."FIRST_TY_GIA_XUAT_QUY",
                    PUID."THU_TU_SAP_XEP_CHI_TIET"
                    ,PUID."name"






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


                 AS   "SO_CHUNG_TU"
                    , PUI."NGUOI_NHAN"                                           AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            PUI."NGUOI_NHAN",
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
                    ,   A."TEN_TAI_KHOAN"
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
                    PUI."SO_CHUNG_TU",

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
                     WHERE TK.id = PUID."TK_THUE_GTGT_ID"),

                    PUI."LY_DO_CHI",
                    (SELECT "MA_LOAI_TIEN"
                     FROM res_currency T
                     WHERE T.id = PUI."currency_id"),
                    PUI."TY_GIA",
                    RID."STT",
                    EX."ID_CHUNG_TU",
                    EX."FIRST_TY_GIA_XUAT_QUY"
              ,   A."TEN_TAI_KHOAN"
            ;
        END IF
    ;


        IF rec."LOAI_CHUNG_TU" IN (319, 325, 369, 375)  --Mua hàng nhập khẩu (nhập kho, không qua kho) tiền mặt
        THEN
            INSERT INTO TMP_KET_QUA
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


                 AS   "SO_CHUNG_TU"
                    , PUI."NGUOI_NHAN"                                           AS "NGUOI_NHAN_NGUOI_NOP"
                    , AO."MA"
                    , LAY_CHUOI_ContactAndAccountObjectName(AO."LOAI_KHACH_HANG",
                                                            PUI."NGUOI_NHAN",
                                                            PUI."TEN_DOI_TUONG") AS "TEN_KHACH_HANG"
                    , PUI."DIA_CHI"
                    , PUI."LY_DO_CHI"                                            AS "DIEN_GIAI"
                    , PUI."KEM_THEO_PC"
                    , SUM(PUID."THANH_TIEN" - PUID."TIEN_CHIET_KHAU")            AS "THANH_TIEN"
                    ,
                    /*Với phiếu chi PS ngoại tệ và có xử lý chênh lệch tỷ giá xuất quỹ thi thực hiện lấy số tiền quy đổi theo tỷ giá xuất quỹ, ngược lại thì lấy quy đổi*/
                      SUM((CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
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
                       WHERE TK.id = PUID."TK_NO_ID")


                    , MIN(PUID."THU_TU_SAP_XEP_CHI_TIET")                        AS sortOrder
                    , RID."STT"
                    , PUID.name

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
                GROUP BY
                    PUI."id",
                    "MODEL_CHUNG_TU",
                    PUI."NGAY_CHUNG_TU",
                    PUI."NGAY_HACH_TOAN",
                    PUI."SO_CHUNG_TU",

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
                     WHERE TK.id = PUID."TK_NO_ID"),

                    PUI."LY_DO_CHI",
                    (SELECT "MA_LOAI_TIEN"
                     FROM res_currency T
                     WHERE T.id = PUI."currency_id"),
                    PUI."TY_GIA",
                    RID."STT",
                    EX."ID_CHUNG_TU",
                    EX."FIRST_TY_GIA_XUAT_QUY"
             , PUID.name
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
                    , SUM(PUID."THANH_TIEN" - PUID."TIEN_CHIET_KHAU"
                          + CASE WHEN PUID."TK_THUE_GTGT_ID" IS NULL
                    THEN "TIEN_THUE_GTGT"
                            ELSE 0
                            END)                                                 AS "THANH_TIEN"
                    ,
                    /*Với phiếu chi PS ngoại tệ và có xử lý chênh lệch tỷ giá xuất quỹ thi thực hiện lấy số tiền quy đổi theo tỷ giá xuất quỹ, ngược lại thì lấy quy đổi*/
                      SUM((CASE WHEN PUI."currency_id" <> LOAI_TIEN_CHINH
                                     AND EX."ID_CHUNG_TU" IS NOT NULL
                          THEN (CASE
                                WHEN
                                    PUID."THANH_TIEN_SAU_TY_GIA_XUAT_QUY" <> 0
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
                       WHERE TK.id = PUID."TK_NO_ID")

                    , MIN(PUID."THU_TU_SAP_XEP_CHI_TIET")                        AS sortOrder
                    , RID."STT"
                     , PUID.name

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
                     WHERE TK.id = PUID."TK_NO_ID")


                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = PUI."currency_id")
                    , PUI."TY_GIA"
                    , RID."STT"
                    , EX."ID_CHUNG_TU"
                    , EX."FIRST_TY_GIA_XUAT_QUY"
                     , PUID.name

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
                      ,   A."TEN_TAI_KHOAN"


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
              ,   A."TEN_TAI_KHOAN"


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
                      SUM(CASE WHEN SAR."LOAI_CHUNG_TU" = 3553
                          THEN SARD."THANH_TIEN"
                               - SARD."TIEN_CHIET_KHAU"
                               + SARD."TIEN_THUE_GTGT"
                          ELSE SARD."THANH_TIEN"
                               - SARD."TIEN_CHIET_KHAU"
                          END)                                                    AS "THANH_TIEN"
                    , SUM((CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                     AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN CASE WHEN SAR."LOAI_CHUNG_TU" = 3551
                        THEN (CASE
                              WHEN
                                  SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY" <> 0
                                  THEN SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY"

                              ELSE SARD."THANH_TIEN_QUY_DOI"
                              END)
                             - SARD."TIEN_CHIET_KHAU_QUY_DOI"
                         ELSE (CASE
                               WHEN
                                   SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY" <> 0
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
                                 ELSE SARD."THANH_TIEN_QUY_DOI"
                                      - SARD."TIEN_CHIET_KHAU_QUY_DOI"
                                 END)
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
                       WHERE TK.id = SARD."TK_NO_ID")

                    , MIN(SARD."THU_TU_SAP_XEP_CHI_TIET")                         AS "STT"
                    , RID."STT"
                     , SARD."DIEN_GIAI_THUE"


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
                       WHERE TK.id = SARD."TK_NO_ID")
                    , RID."STT"
                    , EX."ID_CHUNG_TU"
                    , EX."FIRST_TY_GIA_XUAT_QUY"
                    , SARD."DIEN_GIAI_THUE"

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
                                WHEN SARD."TIEN_THUE_GTGT_THEO_TGXQ" <> 0
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
                ,   A."TEN_TAI_KHOAN"


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
              ,   A."TEN_TAI_KHOAN"

            ;

        END IF
    ;


        IF rec."LOAI_CHUNG_TU" IN (3541, 3543, 3545)
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
                      SUM(CASE WHEN SAR."LOAI_CHUNG_TU" = 3543
                          THEN SARD."THANH_TIEN"
                               - SARD."TIEN_CHIET_KHAU"
                               + SARD."TIEN_THUE_GTGT"
                          ELSE SARD."THANH_TIEN"
                               - SARD."TIEN_CHIET_KHAU"
                          END)                                                    AS "THANH_TIEN"
                    , SUM((CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                     AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN CASE WHEN SAR."LOAI_CHUNG_TU" = 3541
                        THEN (CASE
                              WHEN
                                  SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY" <> 0
                                  THEN SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY"

                              ELSE SARD."THANH_TIEN_QUY_DOI"
                              END)
                             - SARD."TIEN_CHIET_KHAU_QUY_DOI"
                         ELSE (CASE
                               WHEN
                                   SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY" <> 0
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
                                 ELSE SARD."THANH_TIEN_QUY_DOI"
                                      - SARD."TIEN_CHIET_KHAU_QUY_DOI"
                                 END)
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
                       WHERE TK.id = SARD."TK_NO_ID")

                    , MIN(SARD."THU_TU_SAP_XEP_CHI_TIET")                         AS "STT"
                    , RID."STT"
                    , SARD."DIEN_GIAI_THUE"


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
                       WHERE TK.id = SARD."TK_NO_ID"),
                     RID."STT" ,
                     EX."ID_CHUNG_TU" ,
                     EX."FIRST_TY_GIA_XUAT_QUY"
                     , SARD."DIEN_GIAI_THUE"
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
                    , SUM(SARD."TIEN_THUE_GTGT") AS "THANH_TIEN"
                    ,
                    /*Với phiếu chi PS ngoại tệ và có xử lý chênh lệch tỷ giá xuất quỹ thi thực hiện lấy số tiền quy đổi theo tỷ giá xuất quỹ, ngược lại thì lấy quy đổi*/
                      SUM((CASE WHEN SAR."currency_id" <> LOAI_TIEN_CHINH
                                     AND EX."ID_CHUNG_TU" IS NOT NULL
                          THEN (CASE
                                WHEN
                                    SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY" <> 0
                                THEN SARD."THANH_TIEN_THEO_TY_GIA_XUAT_QUY"

                                ELSE SARD."TIEN_THUE_GTGT_QUY_DOI"
                                END)
                           ELSE SARD."TIEN_THUE_GTGT_QUY_DOI"
                           END))                 AS "THANH_TIEN_QUY_DOI"
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
                    , 2000 + MAX(SARD."THU_TU_SAP_XEP_CHI_TIET")     AS sortOrder
                    , RID."STT"
                    ,   A."TEN_TAI_KHOAN"


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
                     RID."STT" ,
                     EX."ID_CHUNG_TU" ,
                     EX."FIRST_TY_GIA_XUAT_QUY"
                      ,   A."TEN_TAI_KHOAN"

            ;

        END IF
    ;

    END LOOP
    ;


END $$

;


SELECT *
FROM TMP_KET_QUA --WHERE  "SO_CHUNG_TU" ='PC00031' --AND "DIEN_GIAI_DETAIL" =N'Tủ lạnh Toshiba 110 lít'
  ORDER BY
                "MasterSortOrder" ,
                "NGAY_CHUNG_TU" ,
                "SO_CHUNG_TU" ,
                "STT"
        """
        sql_result = self.execute(query)
        dic_tk_no  = {}
        dic_tk_co  = {}

        for line in sql_result:
            key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))

            if key not in dic_tk_no:
                    dic_tk_no[key] = []
            if key not in dic_tk_co:
                dic_tk_co[key] = []

            if line.get('TK_NO') and line.get('TK_NO') not in dic_tk_no[key]:
                dic_tk_no[key] += [line.get('TK_NO')]

            if line.get('TK_CO') and line.get('TK_CO') not in dic_tk_co[key]:
                dic_tk_co[key] += [line.get('TK_CO')]


            master_data = self.env['bao.cao.02tt.phieu.chi'].convert_for_update(line)
            detail_data = self.env['bao.cao.02tt.phieu.chi.chi.tiet'].convert_for_update(line)
            if records.get(key):
                records[key].update(master_data)
                records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.02tt.phieu.chi.chi.tiet'].new(detail_data)
        
        for key in records:
            if key in dic_tk_no:
                records[key].TK_NO = ', '.join(dic_tk_no[key])
            if key in dic_tk_co:
                records[key].TK_CO = ', '.join(dic_tk_co[key])

        docs = [records.get(k) for k in records]

        for record in docs:
            
            if not record.LOAI_TIEN:
                record.currency_id = self.lay_loai_tien_mac_dinh()
            else:
                loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', record.LOAI_TIEN)],limit=1)
                if loai_tien_id:
                    record.currency_id = loai_tien_id.id

            tong_tien = 0
            tong_tien_quy_doi = 0
            for line in record.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
                line.currency_id = record.currency_id
                tong_tien += line.THANH_TIEN
                tong_tien_quy_doi += line.THANH_TIEN_QUY_DOI
            record.TONG_TIEN = tong_tien
            record.TONG_TIEN_QUY_DOI = tong_tien_quy_doi
           
        
        ####################### END SQL #######################

        # Tạo object để in
        
        return {
            'docs':docs,
        }


    @api.model_cr
    def init(self):
        self.env.cr.execute(""" 
DROP FUNCTION IF EXISTS LAY_CHUOI_ContactAndAccountObjectName( IN LOAI_KHACH_HANG VARCHAR,HO_VA_TEN_LIEN_HE VARCHAR,HO_VA_TEN VARCHAR  ) --Func_ConcatContactAndAccountObjectName
		;

		CREATE OR REPLACE FUNCTION LAY_CHUOI_ContactAndAccountObjectName( IN LOAI_KHACH_HANG VARCHAR,HO_VA_TEN_LIEN_HE VARCHAR,HO_VA_TEN VARCHAR  )
			RETURNS VARCHAR
		AS $$
		DECLARE
			v_Result VARCHAR;

			rec      RECORD;

        BEGIN

        v_Result ='';

		IF LOAI_KHACH_HANG = '1' -- Nếu là cá nhân
		THEN
			IF COALESCE(HO_VA_TEN_LIEN_HE,'') <>''
                THEN
				 v_Result = HO_VA_TEN_LIEN_HE ;
			ELSE
				 v_Result = HO_VA_TEN ;
            END IF ;

		ELSE -- Nếu là tổ chức

			IF COALESCE(HO_VA_TEN_LIEN_HE,'') <>'' AND COALESCE(HO_VA_TEN,'')<>''
                THEN
				v_Result = HO_VA_TEN_LIEN_HE  ||  ' - ' || HO_VA_TEN ;
			ELSE

				IF COALESCE(HO_VA_TEN_LIEN_HE,'') = ''
                    THEN
					 v_Result = HO_VA_TEN ;
				ELSE
					 v_Result = HO_VA_TEN_LIEN_HE ;
			END IF;
		END IF;
            END IF;

			RETURN v_Result
			;

		END
		;
		$$ LANGUAGE PLpgSQL
		;

		""")

        self.env.cr.execute(""" 
        DROP  FUNCTION IF EXISTS LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(IN ListRefID        VARCHAR(500),
                                                                                    TEN_BANG       VARCHAR(500) --Func_CA_GetAllExchangeRate
                                                                                 );
        CREATE OR REPLACE FUNCTION LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(IN ListRefID        VARCHAR(500),
                                                                                    TEN_BANG       VARCHAR(500) --Func_CA_GetAllExchangeRate
                                                                                 )
            RETURNS TABLE
                        (   "ID_CHUNG_TU"           INT,
                            "MAX_TY_GIA_XUAT_QUY"   DECIMAL(20, 6),
                            "MIN_TY_GIA_XUAT_QUY"   DECIMAL(20, 6),
                            "AVG_TY_GIA_XUAT_QUY"   DECIMAL(20, 6),
                            "FIRST_TY_GIA_XUAT_QUY" DECIMAL(20, 6)
        
            ) AS $$
        DECLARE
        
        
            PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY VARCHAR;
        
        
        BEGIN
        
            DROP TABLE IF EXISTS LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE_TMP_KET_QUA_CUOI_CUNG
            ;
        
            CREATE TEMP TABLE LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE_TMP_KET_QUA_CUOI_CUNG
            (
        
                "ID_CHUNG_TU"           INT,
                "MAX_TY_GIA_XUAT_QUY"   DECIMAL(20, 6),
                "MIN_TY_GIA_XUAT_QUY"   DECIMAL(20, 6),
                "AVG_TY_GIA_XUAT_QUY"   DECIMAL(20, 6),
                "FIRST_TY_GIA_XUAT_QUY" DECIMAL(20, 6)
            )
            ;
        
        
        
            /*Phương pháp tính tỷ giá xuất quỹ: 0: Bình quân cuối kỳ; 1: Bình quân tức thời*/
        
        
        
        
            DROP TABLE IF EXISTS TMP_KQ_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE
            ;
        
            CREATE TEMP TABLE TMP_KQ_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE
            (
        
                "ID_CHUNG_TU"           INT,
                "MAX_TY_GIA_XUAT_QUY"   DECIMAL(20, 6),
                "MIN_TY_GIA_XUAT_QUY"   DECIMAL(20, 6),
                "AVG_TY_GIA_XUAT_QUY"   DECIMAL(20, 6),
                "FIRST_TY_GIA_XUAT_QUY" DECIMAL(20, 6)
            )
            ;
        
            SELECT value
            INTO PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY
            FROM ir_config_parameter
            WHERE key = 'he_thong.PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY'
            FETCH FIRST 1 ROW ONLY
            ;
        
            DROP TABLE IF EXISTS TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE
            ;
        
            CREATE TEMP TABLE TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE
            (
                "ID_CHUNG_TU"   INT,
                "LOAI_CHUNG_TU" INT
        
        
            )
            ;
        
            INSERT INTO TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE
                SELECT
        
                      Value1 AS "ID_CHUNG_TU"
                    , Value2 AS "LOAI_CHUNG_TU"
        
                FROM CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(ListRefID, ',', ';') F
        
            ;
        
            /*Lấy dữ liệu từ cột sổ tài chính*/
            IF PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY = 'BINH_QUAN_TUC_THOI'
            THEN
                IF TEN_BANG =N'sale.ex.tra.lai.hang.ban.chi.tiet'
                THEN
                    INSERT INTO TMP_KQ_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE
                        SELECT
                            A."ID_CHUNG_TU"
                            , A."MAX_TY_GIA_XUAT_QUY"
                            , A."MIN_TY_GIA_XUAT_QUY"
                            , A."AVG_TY_GIA_XUAT_QUY"
                            , B."FIRST_TY_GIA_XUAT_QUY"
                        FROM (SELECT
                                    D."order_id"             AS "ID_CHUNG_TU"
                                  , MAX(D."TY_GIA_XUAT_QUY") AS "MAX_TY_GIA_XUAT_QUY"
                                  , MIN(D."TY_GIA_XUAT_QUY") AS "MIN_TY_GIA_XUAT_QUY"
                                  , AVG(D."TY_GIA_XUAT_QUY") AS "AVG_TY_GIA_XUAT_QUY"
                              FROM purchase_document_line D
                                  INNER JOIN TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T ON
                                                                                                           D."order_id" =
                                                                                                           T."ID_CHUNG_TU"
                              WHERE COALESCE(D."TY_GIA_XUAT_QUY", 0) <> 0
                              GROUP BY D."order_id"
                             ) AS A
                            INNER JOIN (SELECT
                                            A."ID_CHUNG_TU"
                                            , "TY_GIA_XUAT_QUY" AS "FIRST_TY_GIA_XUAT_QUY"
                                        FROM (SELECT
                                                    D."order_id"                             AS "ID_CHUNG_TU"
                                                  , D."TY_GIA_XUAT_QUY"
                                                  , ROW_NUMBER()
                                                    OVER (
                                                        PARTITION BY D."order_id"
                                                        ORDER BY "THU_TU_SAP_XEP_CHI_TIET" ) AS RowNumber
                                              FROM purchase_document_line D
                                                  INNER JOIN TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T
                                                      ON D."order_id" = T."ID_CHUNG_TU"
                                              WHERE COALESCE(D."TY_GIA_XUAT_QUY",
                                                             0) <> 0
                                             ) AS A
                                        WHERE A.RowNumber = 1
                                       ) AS B ON A."ID_CHUNG_TU" = B."ID_CHUNG_TU"
                    ;
                ELSE
                    IF TEN_BANG =N'sale.ex.tra.lai.hang.ban.chi.tiet'
                    THEN
                        INSERT INTO TMP_KQ_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE
                            SELECT
                                A."ID_CHUNG_TU"
                                , A."MAX_TY_GIA_XUAT_QUY"
                                , A."MIN_TY_GIA_XUAT_QUY"
                                , A."AVG_TY_GIA_XUAT_QUY"
                                , B."FIRST_TY_GIA_XUAT_QUY"
                            FROM (SELECT
                                        D."TRA_LAI_HANG_BAN_ID"  AS "ID_CHUNG_TU"
                                      , MAX(D."TY_GIA_XUAT_QUY") AS "MAX_TY_GIA_XUAT_QUY"
                                      , MIN(D."TY_GIA_XUAT_QUY") AS "MIN_TY_GIA_XUAT_QUY"
                                      , AVG(D."TY_GIA_XUAT_QUY") AS "AVG_TY_GIA_XUAT_QUY"
                                  FROM sale_ex_tra_lai_hang_ban_chi_tiet D
                                      INNER JOIN TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T
                                          ON D."TRA_LAI_HANG_BAN_ID" = T."ID_CHUNG_TU"
                                  WHERE COALESCE(D."TY_GIA_XUAT_QUY", 0) <> 0
                                  GROUP BY D."TRA_LAI_HANG_BAN_ID"
                                 ) AS A
                                INNER JOIN (SELECT
                                                 A."ID_CHUNG_TU"
                                                , "TY_GIA_XUAT_QUY" AS "FIRST_TY_GIA_XUAT_QUY"
                                            FROM (SELECT
                                                        D."TRA_LAI_HANG_BAN_ID"                  AS "ID_CHUNG_TU"
                                                      , D."TY_GIA_XUAT_QUY"
                                                      , ROW_NUMBER()
                                                        OVER (
                                                            PARTITION BY D."TRA_LAI_HANG_BAN_ID"
                                                            ORDER BY "THU_TU_SAP_XEP_CHI_TIET" ) AS RowNumber
                                                  FROM sale_ex_tra_lai_hang_ban_chi_tiet D
                                                      INNER JOIN TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T
                                                          ON D."TRA_LAI_HANG_BAN_ID" = T."ID_CHUNG_TU"
                                                  WHERE COALESCE(D."TY_GIA_XUAT_QUY",
                                                                 0) <> 0
                                                 ) AS A
                                            WHERE A.RowNumber = 1
                                           ) AS B ON A."ID_CHUNG_TU" = B."ID_CHUNG_TU"
                        ;
                    ELSE
                        IF TEN_BANG =N'sale.ex.chi.tiet.giam.gia.hang.ban'
                        THEN
                            INSERT INTO TMP_KQ_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE
                                SELECT
                                    A."ID_CHUNG_TU"
                                    , A.MAX_TY_GIA_XUAT_QUY
                                    , A."MIN_TY_GIA_XUAT_QUY"
                                    , A."AVG_TY_GIA_XUAT_QUY"
                                    , B."FIRST_TY_GIA_XUAT_QUY"
                                FROM (SELECT
                                            D."GIAM_GIA_HANG_BAN_ID" AS "ID_CHUNG_TU"
                                          , MAX(D."TY_GIA_XUAT_QUY") AS MAX_TY_GIA_XUAT_QUY
                                          , MIN(D."TY_GIA_XUAT_QUY") AS "MIN_TY_GIA_XUAT_QUY"
                                          , AVG(D."TY_GIA_XUAT_QUY") AS "AVG_TY_GIA_XUAT_QUY"
                                      FROM sale_ex_chi_tiet_giam_gia_hang_ban D
                                          INNER JOIN TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T
                                              ON D."GIAM_GIA_HANG_BAN_ID" = T."ID_CHUNG_TU"
                                      WHERE COALESCE(D."TY_GIA_XUAT_QUY", 0) <> 0
                                      GROUP BY D."GIAM_GIA_HANG_BAN_ID"
                                     ) AS A
                                    INNER JOIN (SELECT
                                                    A."ID_CHUNG_TU"
                                                    , "TY_GIA_XUAT_QUY" AS "FIRST_TY_GIA_XUAT_QUY"
                                                FROM (SELECT
                                                            D."GIAM_GIA_HANG_BAN_ID"                 AS "ID_CHUNG_TU"
                                                          , D."TY_GIA_XUAT_QUY"
                                                          , ROW_NUMBER()
                                                            OVER (
                                                                PARTITION BY D."GIAM_GIA_HANG_BAN_ID"
                                                                ORDER BY "THU_TU_SAP_XEP_CHI_TIET" ) AS RowNumber
                                                      FROM sale_ex_chi_tiet_giam_gia_hang_ban D
                                                          INNER JOIN TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T
                                                              ON D."GIAM_GIA_HANG_BAN_ID" = T."ID_CHUNG_TU"
                                                      WHERE COALESCE(D."TY_GIA_XUAT_QUY",
                                                                     0) <> 0
                                                     ) AS A
                                                WHERE A.RowNumber = 1
                                               ) AS B ON A."ID_CHUNG_TU" = B."ID_CHUNG_TU"
                            ;
                        ELSE
                            IF TEN_BANG =N'purchase.document.line'
                            THEN
                                INSERT INTO TMP_KQ_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE
                                    SELECT
                                        A."ID_CHUNG_TU"
                                        , A.MAX_TY_GIA_XUAT_QUY
                                        , A."MIN_TY_GIA_XUAT_QUY"
                                        , A."AVG_TY_GIA_XUAT_QUY"
                                        , B."FIRST_TY_GIA_XUAT_QUY"
                                    FROM (SELECT
                                                D."order_id"             AS "ID_CHUNG_TU"
                                              , MAX(D."TY_GIA_XUAT_QUY") AS MAX_TY_GIA_XUAT_QUY
                                              , MIN(D."TY_GIA_XUAT_QUY") AS "MIN_TY_GIA_XUAT_QUY"
                                              , AVG(D."TY_GIA_XUAT_QUY") AS "AVG_TY_GIA_XUAT_QUY"
                                          FROM purchase_document_line D
                                              INNER JOIN TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T
                                                  ON D."order_id" = T."ID_CHUNG_TU"
                                          WHERE COALESCE(D."TY_GIA_XUAT_QUY", 0) <> 0
                                          GROUP BY D."order_id"
                                         ) AS A
                                        INNER JOIN (SELECT
                                                         A."ID_CHUNG_TU"
                                                        , "TY_GIA_XUAT_QUY" AS "FIRST_TY_GIA_XUAT_QUY"
                                                    FROM (SELECT
                                                                D."order_id"                             AS "ID_CHUNG_TU"
                                                              , D."TY_GIA_XUAT_QUY"
                                                              , ROW_NUMBER()
                                                                OVER (
                                                                    PARTITION BY D."order_id"
                                                                    ORDER BY "THU_TU_SAP_XEP_CHI_TIET" ) AS RowNumber
                                                          FROM purchase_document_line D
                                                              INNER JOIN
                                                              TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T
                                                                  ON D."order_id" = T."ID_CHUNG_TU"
                                                          WHERE COALESCE(D."TY_GIA_XUAT_QUY",
                                                                         0) <> 0
                                                         ) AS A
                                                    WHERE A.RowNumber = 1
                                                   ) AS B ON A."ID_CHUNG_TU" = B."ID_CHUNG_TU"
                                ;
                            ELSE
                                IF TEN_BANG =N'account.ex.chung.tu.nghiep.vu.khac.hach.toan'
                                THEN
                                    INSERT INTO TMP_KQ_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE
                                        SELECT
                                            A."ID_CHUNG_TU"
                                            , A.MAX_TY_GIA_XUAT_QUY
                                            , A."MIN_TY_GIA_XUAT_QUY"
                                            , A."AVG_TY_GIA_XUAT_QUY"
                                            , B."FIRST_TY_GIA_XUAT_QUY"
                                        FROM (SELECT
                                                    D."CHUNG_TU_NGHIEP_VU_KHAC_ID" AS "ID_CHUNG_TU"
                                                  , MAX(D."TY_GIA_XUAT_QUY")       AS MAX_TY_GIA_XUAT_QUY
                                                  , MIN(D."TY_GIA_XUAT_QUY")       AS "MIN_TY_GIA_XUAT_QUY"
                                                  , AVG(D."TY_GIA_XUAT_QUY")       AS "AVG_TY_GIA_XUAT_QUY"
                                              FROM account_ex_chung_tu_nghiep_vu_khac_hach_toan D
                                                  INNER JOIN TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T
                                                      ON D."CHUNG_TU_NGHIEP_VU_KHAC_ID" = T."ID_CHUNG_TU"
                                              WHERE COALESCE(D."TY_GIA_XUAT_QUY", 0) <> 0
                                              GROUP BY D."CHUNG_TU_NGHIEP_VU_KHAC_ID"
                                             ) AS A
                                            INNER JOIN (SELECT
                                                             A."ID_CHUNG_TU"
                                                            , "TY_GIA_XUAT_QUY" AS "FIRST_TY_GIA_XUAT_QUY"
                                                        FROM (SELECT
                                                                    D."CHUNG_TU_NGHIEP_VU_KHAC_ID"           AS "ID_CHUNG_TU"
                                                                  , D."TY_GIA_XUAT_QUY"
                                                                  , ROW_NUMBER()
                                                                    OVER (
                                                                        PARTITION BY D."CHUNG_TU_NGHIEP_VU_KHAC_ID"
                                                                        ORDER BY "THU_TU_SAP_XEP_CHI_TIET" ) AS RowNumber
                                                              FROM account_ex_chung_tu_nghiep_vu_khac_hach_toan D
                                                                  INNER JOIN
                                                                  TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T
                                                                      ON D."CHUNG_TU_NGHIEP_VU_KHAC_ID" = T."ID_CHUNG_TU"
                                                              WHERE COALESCE(D."TY_GIA_XUAT_QUY",
                                                                             0) <> 0
                                                             ) AS A
                                                        WHERE A.RowNumber = 1
                                                       ) AS B ON A."ID_CHUNG_TU" = B."ID_CHUNG_TU"
                                    ;
                                ELSE
                                    IF TEN_BANG =N'account.ex.phieu.thu.chi.tiet'
                                    THEN
                                        INSERT INTO TMP_KQ_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE
                                            SELECT
                                                A."ID_CHUNG_TU"
                                                , A.MAX_TY_GIA_XUAT_QUY
                                                , A."MIN_TY_GIA_XUAT_QUY"
                                                , A."AVG_TY_GIA_XUAT_QUY"
                                                , B."FIRST_TY_GIA_XUAT_QUY"
                                            FROM (SELECT
                                                        D."PHIEU_THU_CHI_ID"     AS "ID_CHUNG_TU"
                                                      , MAX(D."TY_GIA_XUAT_QUY") AS MAX_TY_GIA_XUAT_QUY
                                                      , MIN(D."TY_GIA_XUAT_QUY") AS "MIN_TY_GIA_XUAT_QUY"
                                                      , AVG(D."TY_GIA_XUAT_QUY") AS "AVG_TY_GIA_XUAT_QUY"
                                                  FROM account_ex_phieu_thu_chi_tiet D
                                                      INNER JOIN TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T
                                                          ON D."PHIEU_THU_CHI_ID" = T."ID_CHUNG_TU"
                                                  WHERE COALESCE(D."TY_GIA_XUAT_QUY",
                                                                 0) <> 0
                                                  GROUP BY D."PHIEU_THU_CHI_ID"
                                                 ) AS A
                                                INNER JOIN (SELECT
                                                                 A."ID_CHUNG_TU"
                                                                , "TY_GIA_XUAT_QUY" AS "FIRST_TY_GIA_XUAT_QUY"
                                                            FROM (SELECT
                                                                        D."PHIEU_THU_CHI_ID"                     AS "ID_CHUNG_TU"
                                                                      , D."TY_GIA_XUAT_QUY"
                                                                      , ROW_NUMBER()
                                                                        OVER (
                                                                            PARTITION BY D."PHIEU_THU_CHI_ID"
                                                                            ORDER BY "THU_TU_SAP_XEP_CHI_TIET" ) AS RowNumber
                                                                  FROM account_ex_phieu_thu_chi_tiet D
                                                                      INNER JOIN
                                                                      TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T
                                                                          ON D."PHIEU_THU_CHI_ID" = T."ID_CHUNG_TU"
                                                                  WHERE COALESCE(D."TY_GIA_XUAT_QUY",
                                                                                 0) <> 0
                                                                 ) AS A
                                                            WHERE A.RowNumber = 1
                                                           ) AS B ON A."ID_CHUNG_TU" = B."ID_CHUNG_TU"
                                        ;
                                    ELSE
                                        IF TEN_BANG =N'account.ex.phieu.thu.chi.tiet'
                                        THEN
                                            INSERT INTO TMP_KQ_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE
                                                SELECT
                                                    A."ID_CHUNG_TU"
                                                    , A.MAX_TY_GIA_XUAT_QUY
                                                    , A."MIN_TY_GIA_XUAT_QUY"
                                                    , A."AVG_TY_GIA_XUAT_QUY"
                                                    , B."FIRST_TY_GIA_XUAT_QUY"
                                                FROM (SELECT
                                                            D."PHIEU_THU_CHI_ID"     AS "ID_CHUNG_TU"
                                                          , MAX(D."TY_GIA_XUAT_QUY") AS MAX_TY_GIA_XUAT_QUY
                                                          , MIN(D."TY_GIA_XUAT_QUY") AS "MIN_TY_GIA_XUAT_QUY"
                                                          , AVG(D."TY_GIA_XUAT_QUY") AS "AVG_TY_GIA_XUAT_QUY"
                                                      FROM account_ex_phieu_thu_chi_tiet D
                                                          INNER JOIN TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T
                                                              ON D."PHIEU_THU_CHI_ID" = T."ID_CHUNG_TU"
                                                      WHERE COALESCE(D."TY_GIA_XUAT_QUY",
                                                                     0) <> 0
                                                      GROUP BY D."PHIEU_THU_CHI_ID"
                                                     ) AS A
                                                    INNER JOIN (SELECT
                                                                    A."ID_CHUNG_TU"
                                                                    , "TY_GIA_XUAT_QUY" AS "FIRST_TY_GIA_XUAT_QUY"
                                                                FROM (SELECT
                                                                            D."PHIEU_THU_CHI_ID"                AS "ID_CHUNG_TU"
                                                                          , D."TY_GIA_XUAT_QUY"
                                                                          , ROW_NUMBER()
                                                                            OVER (
                                                                                PARTITION BY D."PHIEU_THU_CHI_ID"
                                                                                ORDER BY
                                                                                    "THU_TU_SAP_XEP_CHI_TIET" ) AS RowNumber
                                                                      FROM
                                                                          account_ex_phieu_thu_chi_tiet D
                                                                          INNER JOIN
                                                                          TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T
                                                                              ON D."PHIEU_THU_CHI_ID" = T."ID_CHUNG_TU"
                                                                      WHERE
                                                                          COALESCE(D."TY_GIA_XUAT_QUY",
                                                                                   0) <> 0
                                                                     ) AS A
                                                                WHERE A.RowNumber = 1
                                                               ) AS B ON A."ID_CHUNG_TU" = B."ID_CHUNG_TU"
                                            ;
                                        ELSE
                                            IF TEN_BANG =N'account.ex.phieu.thu.chi.tiet'
                                            THEN
                                                INSERT INTO TMP_KQ_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE
                                                    SELECT
                                                        A."ID_CHUNG_TU"
                                                        , A.MAX_TY_GIA_XUAT_QUY
                                                        , A."MIN_TY_GIA_XUAT_QUY"
                                                        , A."AVG_TY_GIA_XUAT_QUY"
                                                        , B."FIRST_TY_GIA_XUAT_QUY"
                                                    FROM (SELECT
                                                                D."PHIEU_THU_CHI_ID"     AS "ID_CHUNG_TU"
                                                              , MAX(D."TY_GIA_XUAT_QUY") AS MAX_TY_GIA_XUAT_QUY
                                                              , MIN(D."TY_GIA_XUAT_QUY") AS "MIN_TY_GIA_XUAT_QUY"
                                                              , AVG(D."TY_GIA_XUAT_QUY") AS "AVG_TY_GIA_XUAT_QUY"
                                                          FROM account_ex_phieu_thu_chi_tiet D
                                                              INNER JOIN
                                                              TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T
                                                                  ON D."PHIEU_THU_CHI_ID" = T."ID_CHUNG_TU"
                                                          WHERE COALESCE(D."TY_GIA_XUAT_QUY",
                                                                         0) <> 0
                                                          GROUP BY D."PHIEU_THU_CHI_ID"
                                                         ) AS A
                                                        INNER JOIN (SELECT
                                                                         A."ID_CHUNG_TU"
                                                                        , "TY_GIA_XUAT_QUY" AS "FIRST_TY_GIA_XUAT_QUY"
                                                                    FROM (SELECT
                                                                                D."PHIEU_THU_CHI_ID"                AS "ID_CHUNG_TU"
                                                                              , D."TY_GIA_XUAT_QUY"
                                                                              , ROW_NUMBER()
                                                                                OVER (
                                                                                    PARTITION BY D."PHIEU_THU_CHI_ID"
                                                                                    ORDER BY
                                                                                        "THU_TU_SAP_XEP_CHI_TIET" ) AS RowNumber
                                                                          FROM
                                                                              account_ex_phieu_thu_chi_tiet D
                                                                              INNER JOIN
                                                                              TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T
                                                                                  ON D."PHIEU_THU_CHI_ID" = T."ID_CHUNG_TU"
                                                                          WHERE
                                                                              COALESCE(D."TY_GIA_XUAT_QUY",
                                                                                       0) <> 0
                                                                         ) AS A
                                                                    WHERE A.RowNumber = 1
                                                                   ) AS B ON A."ID_CHUNG_TU" = B."ID_CHUNG_TU"
                                                ;
                                            ELSE
                                                IF TEN_BANG =N'account.ex.phieu.thu.chi.tiet'
                                                THEN
                                                    INSERT INTO TMP_KQ_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE
                                                        SELECT
                                                            A."ID_CHUNG_TU"
                                                            , A.MAX_TY_GIA_XUAT_QUY
                                                            , A."MIN_TY_GIA_XUAT_QUY"
                                                            , A."AVG_TY_GIA_XUAT_QUY"
                                                            , B."FIRST_TY_GIA_XUAT_QUY"
                                                        FROM (SELECT
                                                                    D."PHIEU_THU_CHI_ID"     AS "ID_CHUNG_TU"
                                                                  , MAX(D."TY_GIA_XUAT_QUY") AS MAX_TY_GIA_XUAT_QUY
                                                                  , MIN(D."TY_GIA_XUAT_QUY") AS "MIN_TY_GIA_XUAT_QUY"
                                                                  , AVG(D."TY_GIA_XUAT_QUY") AS "AVG_TY_GIA_XUAT_QUY"
                                                              FROM account_ex_phieu_thu_chi_tiet D
                                                                  INNER JOIN
                                                                  TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T
                                                                      ON D."PHIEU_THU_CHI_ID" = T."ID_CHUNG_TU"
                                                              WHERE COALESCE(D."TY_GIA_XUAT_QUY",
                                                                             0) <> 0
                                                              GROUP BY D."PHIEU_THU_CHI_ID"
                                                             ) AS A
                                                            INNER JOIN (SELECT
                                                                            A."ID_CHUNG_TU"
                                                                            , "TY_GIA_XUAT_QUY" AS "FIRST_TY_GIA_XUAT_QUY"
                                                                        FROM (SELECT
                                                                                    D."PHIEU_THU_CHI_ID"                     AS "ID_CHUNG_TU"
                                                                                  , D."TY_GIA_XUAT_QUY"
                                                                                  , ROW_NUMBER()
                                                                                    OVER (
                                                                                        PARTITION BY D."PHIEU_THU_CHI_ID"
                                                                                        ORDER BY
                                                                                            "THU_TU_SAP_XEP_CHI_TIET" )      AS RowNumber
                                                                              FROM
                                                                                  account_ex_phieu_thu_chi_tiet D
                                                                                  INNER JOIN
                                                                                  TMP_PARAM_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE T
                                                                                      ON D."PHIEU_THU_CHI_ID" = T."ID_CHUNG_TU"
                                                                              WHERE
                                                                                  COALESCE(D."TY_GIA_XUAT_QUY",
                                                                                           0) <> 0
                                                                             ) AS A
                                                                        WHERE
                                                                            A.RowNumber = 1
                                                                       ) AS B ON A."ID_CHUNG_TU" = B."ID_CHUNG_TU"
                                                    ;
        
        
                                                END IF
                                                ;
                                            END IF
                                            ;
                                        END IF
                                        ;
                                    END IF
                                    ;
                                END IF
                                ;
                            END IF
                            ;
                        END IF
                        ;
                    END IF
                    ;
                END IF
                ;
            END IF
            ;
        
        
             INSERT  INTO  LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE_TMP_KET_QUA_CUOI_CUNG(
                        SELECT DISTINCT
                                A."ID_CHUNG_TU"  ,
                                 A."MAX_TY_GIA_XUAT_QUY"  ,
                                A."MIN_TY_GIA_XUAT_QUY" ,
                                A."AVG_TY_GIA_XUAT_QUY" ,
                                A."FIRST_TY_GIA_XUAT_QUY"
        
                        FROM    TMP_KQ_LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE A) ;
        
            RETURN QUERY SELECT *
                         FROM LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE_TMP_KET_QUA_CUOI_CUNG
            ;
        END
        ;
        
        $$ LANGUAGE PLpgSQL
        ;
        
        


		""")
