# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_PHIEU_THU_MAU_DAY_DU(models.Model):
    _name = 'bao.cao.phieu.thu.mau.day.du'
    _auto = False

    ref = fields.Char(string='Reffence ID')
    ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
    MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')
    NGAY_CHUNG_TU =  fields.Date(string='Ngày chứng từ') #RefDate
    NGAY_HACH_TOAN =  fields.Date(string='Ngày hạch toán') #PostedDate
    SO_CHUNG_TU =  fields.Char(string='Số chứng từ') #RefNoFinance
    MA_KHACH_HANG =  fields.Char(string='Mã khách hàng') #AccountObjectCode
    TEN_KHACH_HANG =  fields.Char(string='Tên khách hàng') #AccountObjectName
    KHACH_HANG =  fields.Char(string='Khách hàng') #AccountObjectContactName
    DIA_CHI =  fields.Char(string='Địa chỉ') #AccountObjectAddress
    TEN_NHAN_VIEN =  fields.Char(string='Tên nhân viên') #EmployeeName
    MA_NHAN_VIEN =  fields.Char(string='Mã nhân viên') #EmployeeCode
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

    LOAI_KHACH_HANG =  fields.Integer(string='Loại khách hàng') #AccountObjectType


    ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.phieu.thu.mau.day.du.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')

class BAO_CAO_PHIEU_THU_MAU_DAY_DU_REPORT(models.AbstractModel):
    _name = 'report.bao_cao.template_receiptvoucherfull'

    @api.model
    def get_report_values(self, docids, data=None):
        refTypeList, records = self.get_reftype_list(data)
        
        ############### START SQL lấy dữ liệu ###############
        query = """
           DO LANGUAGE plpgsql $$
DECLARE

    ListRefID    VARCHAR := N'""" + refTypeList + """';


    rec          RECORD;




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

            Value1
            , Value2


        FROM CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(ListRefID, ',', ';') F
            INNER JOIN danh_muc_reftype R ON F.Value2 = R."REFTYPE"
    ;

    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA
    (
        "ID_CHUNG_TU"        INT,
        "MODEL_CHUNG_TU"     VARCHAR(255),
        "NGAY_CHUNG_TU"      TIMESTAMP,
        "NGAY_HACH_TOAN"     TIMESTAMP,
        "SO_CHUNG_TU"        VARCHAR,
        "MA_KHACH_HANG"      VARCHAR,
        "TEN_KHACH_HANG"     VARCHAR(128),
        "KHACH_HANG"         VARCHAR(128),

        "DIA_CHI"            VARCHAR(255),
        "TEN_NHAN_VIEN"      VARCHAR(128),
        "MA_NHAN_VIEN"       VARCHAR,
        "DIEN_GIAI"          VARCHAR(255),
        "SO_CT_GOC_KEM_THEO" VARCHAR(255),
        "LOAI_TIEN"          VARCHAR(255),

        "DIEN_GIAI_DETAIL"   VARCHAR(255),
        "TK_NO"              VARCHAR(255),
        "TK_CO"              VARCHAR(255),

        "TK_THUE_GTGT"       VARCHAR(255),
        "TK_CHIET_KHAU"      VARCHAR(255),

        "TK_CONG_NO"         VARCHAR(255),
        "SO_TIEN_QUY_DOI"    DECIMAL(18, 4),
        "SO_TIEN"            DECIMAL(18, 4),
        "TIEN_THUE_QUY_DOI"  DECIMAL(18, 4),
        "TIEN_THUE"          DECIMAL(18, 4),
        "TIEN_CK_QUY_DOI"    DECIMAL(18, 4),
        "TIEN_CK"            DECIMAL(18, 4),
         "SortOrder" INT ,
        "MasterSortOrder" INT,
         "LOAI_KHACH_HANG"         VARCHAR(200),
         "TY_GIA"    DECIMAL(18, 4)

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

        IF rec."LOAI_CHUNG_TU" = ANY ('{1010,1011,1012,1013}' :: INT [])
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                      C."id"                         AS "ID_CHUNG_TU"
                    , 'account.ex.phieu.thu.chi'     AS "MODEL_CHUNG_TU"
                    , C."NGAY_CHUNG_TU"
                    , C."NGAY_HACH_TOAN"
                    , C."SO_CHUNG_TU"

                    , A."MA"
                    , C."TEN_DOI_TUONG"
                    , C."NGUOI_NOP"

                    , C."DIA_CHI"
                    , E."HO_VA_TEN"                  AS "TEN_NHAN_VIEN"
                    , E."MA"                         AS "MA_NHAN_VIEN"
                    , C."DIEN_GIAI"
                    , C."KEM_THEO_CHUNG_TU_GOC"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = C."currency_id") AS "LOAI_TIEN"

                    , CD."DIEN_GIAI_DETAIL"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CD."TK_NO_ID")  AS "TK_NO"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CD."TK_CO_ID")  AS "TK_CO"

                    , NULL
                     , NULL
                     , NULL
                    , CASE WHEN (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = CD."TK_NO_ID") LIKE '111%%'
                    THEN CD."SO_TIEN_QUY_DOI"
                      WHEN (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = CD."TK_CO_ID") LIKE '111%%'
                          THEN -CD."SO_TIEN_QUY_DOI"
                      ELSE 0
                      END
                    , CASE WHEN (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = CD."TK_NO_ID") LIKE '111%%'
                    THEN CD."SO_TIEN"
                      WHEN (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = CD."TK_CO_ID") LIKE '111%%'
                          THEN -CD."SO_TIEN"
                      ELSE 0
                      END
                    ,0
                    ,0
                    ,0
                    ,0
                    ,CD."THU_TU_SAP_XEP_CHI_TIET"
                    ,F."STT"
                     , A."LOAI_KHACH_HANG"
                     , C."TY_GIA"
                FROM account_ex_phieu_thu_chi C
                    INNER JOIN account_ex_phieu_thu_chi_tiet CD ON C."id" = CD."PHIEU_THU_CHI_ID"
                    INNER JOIN TMP_PARAM F ON C."id" = F."ID_CHUNG_TU"
                    LEFT JOIN res_partner A ON C."DOI_TUONG_ID" = A."id"
                    LEFT JOIN res_partner E ON C."NHAN_VIEN_ID" = E."id"
                WHERE F."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND F."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;

        END IF
    ;

        IF rec."LOAI_CHUNG_TU" = ANY ('{3040,3041,3042,3043}' :: INT [])
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    C."id"
                    , 'purchase.ex.giam.gia.hang.mua' AS "MODEL_CHUNG_TU"
                    , C."NGAY_CHUNG_TU"
                    , C."NGAY_HACH_TOAN"
                    , C."SO_CHUNG_TU"
                    , A."MA"
                    , C."TEN_NHA_CUNG_CAP"
                    , C."NGUOI_NOP"
                    , C."DIA_CHI"
                    , E."HO_VA_TEN"                   AS "TEN_NHAN_VIEN"
                    , E."MA"                          AS "MA_NHAN_VIEN"
                    , C."DIEN_GIAI"
                    , C."KEM_THEO_CT_GOC"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = C."currency_id")  AS "LOAI_TIEN"
                    , CD."TEN_HANG"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CD."TK_NO_ID")   AS "TK_NO"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CD."TK_CO_ID")   AS "TK_CO"
                     , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CD."TK_THUE_GTGT_ID")   AS "TK_THUE_GTGT"

                    , NULL
                     , NULL
                    , CASE WHEN (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = CD."TK_NO_ID") LIKE '111%%'
                    THEN CD."THANH_TIEN_QUY_DOI"
                      WHEN (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = CD."TK_CO_ID") LIKE '111%%'
                          THEN -CD."THANH_TIEN_QUY_DOI"
                      ELSE 0
                      END
                    , CASE WHEN (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = CD."TK_NO_ID") LIKE '111%%'
                    THEN CD."THANH_TIEN"
                      WHEN (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = CD."TK_CO_ID") LIKE '111%%'
                          THEN -CD."THANH_TIEN"
                      ELSE 0
                      END
                     , CASE WHEN (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = CD."TK_NO_ID") LIKE '111%%'
                    THEN CD."TIEN_THUE_GTGT_QUY_DOI"
                      WHEN (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = CD."TK_THUE_GTGT_ID") LIKE '111%%'
                          THEN -CD."TIEN_THUE_GTGT_QUY_DOI"
                      ELSE 0
                      END
                    , CASE WHEN (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = CD."TK_NO_ID") LIKE '111%%'
                    THEN CD."TIEN_THUE_GTGT"
                      WHEN (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = CD."TK_THUE_GTGT_ID") LIKE '111%%'
                          THEN -CD."TIEN_THUE_GTGT"
                      ELSE 0
                      END
                    ,0
                    ,0
                    ,CD."THU_TU_SAP_XEP_CHI_TIET"
                    ,F."STT"
                    , A."LOAI_KHACH_HANG"
                     , C."TY_GIA"


                FROM purchase_ex_giam_gia_hang_mua C
                    INNER JOIN purchase_ex_giam_gia_hang_mua_chi_tiet CD
                        ON C."id" = CD."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID"
                    INNER JOIN TMP_PARAM F ON C."id" = F."ID_CHUNG_TU"
                    LEFT JOIN res_partner A ON C."DOI_TUONG_ID" = A."id"
                    LEFT JOIN res_partner E ON C."NHAN_VIEN_ID" = E."id"
                WHERE F."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND F."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"

            ;

        END IF
    ;


        IF rec."LOAI_CHUNG_TU" = ANY ('{3030,3031,3032,3033}' :: INT []) --'PUReturn'
        THEN


            INSERT INTO TMP_KET_QUA
                SELECT
                    C."id"
                    , 'purchase.ex.tra.lai.hang.mua' AS "MODEL_CHUNG_TU"
                    , C."NGAY_CHUNG_TU"
                    , C."NGAY_HACH_TOAN"
                    , C."SO_PHIEU_THU"
                    , A."MA"
                    , C."TEN_NHA_CUNG_CAP"
                    , C."NGUOI_NOP"

                    , C."DIA_CHI"
                    , E."HO_VA_TEN"
                    , E."MA"
                    , C."LY_DO_NOP"
                    , NULL                           AS "SO_CT_GOC_KEM_THEO"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = C."currency_id") AS "LOAI_TIEN"
                    , CD."TEN_HANG"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CD."TK_NO_ID")  AS "TK_NO"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CD."TK_CO_ID")  AS "TK_CO"
                     , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CD."TK_THUE_GTGT_ID")  AS "TK_THUE_GTGT"

                    , NULL
                      , NULL
                    , CASE WHEN (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = CD."TK_NO_ID") LIKE '111%%'
                    THEN CD."THANH_TIEN_QUY_DOI"
                      WHEN (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = CD."TK_CO_ID") LIKE '111%%'
                          THEN -CD."THANH_TIEN_QUY_DOI"
                      ELSE 0
                      END
                    , CASE WHEN (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = CD."TK_NO_ID") LIKE '111%%'
                    THEN CD."THANH_TIEN"
                      WHEN (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = CD."TK_CO_ID") LIKE '111%%'
                          THEN -CD."THANH_TIEN"
                      ELSE 0
                      END
                     , CASE WHEN (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = CD."TK_NO_ID") LIKE '111%%'
                    THEN CD."TIEN_THUE_GTGT_QUY_DOI"
                      WHEN (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = CD."TK_THUE_GTGT_ID") LIKE '111%%'
                          THEN -CD."TIEN_THUE_GTGT_QUY_DOI"
                      ELSE 0
                      END
                    , CASE WHEN (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = CD."TK_NO_ID") LIKE '111%%'
                    THEN CD."TIEN_THUE_GTGT"
                      WHEN (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = CD."TK_THUE_GTGT_ID") LIKE '111%%'
                          THEN -CD."TIEN_THUE_GTGT"
                      ELSE 0
                      END
                    ,0
                    ,0
                    ,CD."THU_TU_SAP_XEP_CHI_TIET"
                    ,F."STT"
                    , A."LOAI_KHACH_HANG"
                     , C."TY_GIA"


                FROM purchase_ex_tra_lai_hang_mua C
                    INNER JOIN purchase_ex_tra_lai_hang_mua_chi_tiet CD ON C."id" = CD."CHUNG_TU_TRA_LAI_HANG_MUA_ID"
                    INNER JOIN TMP_PARAM F ON C."id" = F."ID_CHUNG_TU"
                    LEFT JOIN res_partner A ON C."DOI_TUONG_ID" = A."id"
                    LEFT JOIN res_partner E ON C."NHAN_VIEN_ID" = E."id"
                WHERE F."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND F."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"


            ;

        END IF
    ;

        IF rec."LOAI_CHUNG_TU" = ANY ('{3530,3531,3532,3534,3535,3536,3537,3538}' :: INT []) --'"sale_document"'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    C."id"
                    , 'sale.document'                AS "MODEL_CHUNG_TU"
                    , C."NGAY_CHUNG_TU"
                    , C."NGAY_HACH_TOAN"
                    , C."SO_CHUNG_TU"

                    , A."MA"
                    , C."TEN_KHACH_HANG"
                    , C."NGUOI_LIEN_HE"

                    , C."DIA_CHI"
                    , E."HO_VA_TEN"
                    , E."MA"
                    , C."DIEN_GIAI"
                    , C."KEM_THEO_CHUNG_TU_GOC"
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = C."currency_id") AS "LOAI_TIEN"
                    , CD."TEN_HANG"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CD."TK_NO_ID")  AS "TK_NO"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CD."TK_CO_ID")  AS "TK_CO"
                     , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CD."TK_THUE_GTGT_ID")  AS "TK_THUE_GTGT"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CD."TK_CHIET_KHAU_ID")  AS "TK_CHIET_KHAU"

                    , NULL
                    , CASE WHEN (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = CD."TK_NO_ID") LIKE '111%%'
                    THEN CD."THANH_TIEN_QUY_DOI"
                      WHEN (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = CD."TK_CO_ID") LIKE '111%%'
                          THEN -CD."THANH_TIEN_QUY_DOI"
                      ELSE 0
                      END
                    , CASE WHEN (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = CD."TK_NO_ID") LIKE '111%%'
                    THEN CD."THANH_TIEN"
                      WHEN (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = CD."TK_CO_ID") LIKE '111%%'
                          THEN -CD."THANH_TIEN"
                      ELSE 0
                      END


                     , CASE WHEN (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = CD."TK_NO_ID") LIKE '111%%'
                    THEN CD."TIEN_THUE_GTGT_QUY_DOI"
                      WHEN (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = CD."TK_THUE_GTGT_ID") LIKE '111%%'
                          THEN -CD."TIEN_THUE_GTGT_QUY_DOI"
                      ELSE 0
                      END
                    , CASE WHEN (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = CD."TK_NO_ID") LIKE '111%%'
                    THEN CD."TIEN_THUE_GTGT"
                      WHEN (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = CD."TK_THUE_GTGT_ID") LIKE '111%%'
                          THEN -CD."TIEN_THUE_GTGT"
                      ELSE 0
                      END

                     , CASE WHEN (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = CD."TK_CHIET_KHAU_ID") LIKE '111%%'
                    THEN CD."TIEN_CK_QUY_DOI"
                      WHEN (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = CD."TK_NO_ID") LIKE '111%%'
                          THEN -CD."TIEN_CK_QUY_DOI"
                      ELSE 0
                      END
                    , CASE WHEN (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = CD."TK_CHIET_KHAU_ID") LIKE '111%%'
                    THEN CD."TIEN_CHIET_KHAU"
                      WHEN (SELECT "SO_TAI_KHOAN"
                            FROM danh_muc_he_thong_tai_khoan TK
                            WHERE TK.id = CD."TK_NO_ID") LIKE '111%%'
                          THEN -CD."TIEN_CHIET_KHAU"
                      ELSE 0
                      END
                    ,CD."THU_TU_SAP_XEP_CHI_TIET"
                    ,F."STT"
                    , A."LOAI_KHACH_HANG"
                     , C."TY_GIA"

                FROM sale_document C
                    INNER JOIN sale_document_line CD ON C."id" = CD."SALE_DOCUMENT_ID"
                    INNER JOIN TMP_PARAM F ON C."id" = F."ID_CHUNG_TU"
                    LEFT JOIN res_partner A ON C."DOI_TUONG_ID" = A."id"
                    LEFT JOIN res_partner E ON C."NHAN_VIEN_ID" = E."id"
                WHERE F."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND F."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"


            ;
        END IF
    ;

    END LOOP
    ;


    DROP TABLE IF EXISTS TMP_SO_TAI_KHOAN_ID_CHUNG_TU
    ;

    CREATE TEMP TABLE TMP_SO_TAI_KHOAN_ID_CHUNG_TU
    (
        "MIN_TK_CONG_NO" VARCHAR(255),
        "MAX_TK_CONG_NO" VARCHAR(255),
        "ID_CHUNG_TU"    INT,
        "MODEL_CHUNG_TU" VARCHAR(255)
    )
    ;

    INSERT INTO TMP_SO_TAI_KHOAN_ID_CHUNG_TU

        SELECT
            MIN("TK_NO")
            , MAX("TK_NO")
            , "ID_CHUNG_TU"
            , "MODEL_CHUNG_TU"
        FROM TMP_KET_QUA
        WHERE "TK_NO" LIKE '111%%'
        GROUP BY
            "ID_CHUNG_TU",
            "MODEL_CHUNG_TU"


    ;

    UPDATE TMP_KET_QUA R
    SET "TK_CONG_NO" = S."RightAccountNumber"
    FROM
        (SELECT
             MAX(A."SO_TAI_KHOAN") AS "RightAccountNumber"
             , "ID_CHUNG_TU"
             , "MODEL_CHUNG_TU"
         FROM danh_muc_he_thong_tai_khoan A
             INNER JOIN TMP_SO_TAI_KHOAN_ID_CHUNG_TU AR ON AR."MIN_TK_CONG_NO" LIKE A."SO_TAI_KHOAN"
                                                                                    || '%%'
                                                           AND AR."MAX_TK_CONG_NO" LIKE A."SO_TAI_KHOAN"
                                                                                        || '%%'
         GROUP BY
             AR."ID_CHUNG_TU",
             AR."MODEL_CHUNG_TU"
        ) S
    WHERE
        R."ID_CHUNG_TU" = S."ID_CHUNG_TU" AND R."MODEL_CHUNG_TU" = S."MODEL_CHUNG_TU"
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
    ;

    CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
        AS

            SELECT
                "ID_CHUNG_TU"
                , "MODEL_CHUNG_TU"
                , "NGAY_CHUNG_TU"
                , "NGAY_HACH_TOAN"
                , "SO_CHUNG_TU"
                , "MA_KHACH_HANG"
                , "TEN_KHACH_HANG"
                , "KHACH_HANG"
                , "DIA_CHI"
                , "TEN_NHAN_VIEN"
                , "MA_NHAN_VIEN"
                , "DIEN_GIAI"
                , "SO_CT_GOC_KEM_THEO"
                , "LOAI_TIEN"
                , "DIEN_GIAI_DETAIL"
                , "TK_NO"
                , "TK_CO"
                , "TK_CONG_NO"
                , "SO_TIEN_QUY_DOI"
                , "SO_TIEN"
                ,"SortOrder"
                ,"MasterSortOrder"
                , "LOAI_KHACH_HANG"
                 , "TY_GIA"

            FROM TMP_KET_QUA
            UNION ALL
            SELECT
                "ID_CHUNG_TU"
                , "MODEL_CHUNG_TU"
                , "NGAY_CHUNG_TU"
                , "NGAY_HACH_TOAN"
                , "SO_CHUNG_TU"
                , "MA_KHACH_HANG"
                , "TEN_KHACH_HANG"
                , "KHACH_HANG"
                , "DIA_CHI"
                , "TEN_NHAN_VIEN"
                , "MA_NHAN_VIEN"
                , "DIEN_GIAI"
                , "SO_CT_GOC_KEM_THEO"
                , "LOAI_TIEN"
                , N'Thuế GTGT'       AS "DIEN_GIAI_DETAIL"
                , "TK_NO"
                , "TK_THUE_GTGT"
                , "TK_CONG_NO"
                , SUM("TIEN_THUE_QUY_DOI")    AS "SO_TIEN_QUY_DOI"
                , SUM("TIEN_THUE") AS "SO_TIEN"
                ,1000 AS "SortOrder"
               ,"MasterSortOrder"
                 , "LOAI_KHACH_HANG"
                 , "TY_GIA"


            FROM TMP_KET_QUA
            GROUP BY
                "ID_CHUNG_TU"
                , "MODEL_CHUNG_TU"
                , "NGAY_CHUNG_TU"
                , "NGAY_HACH_TOAN"
                , "SO_CHUNG_TU"
                , "MA_KHACH_HANG"
                , "TEN_KHACH_HANG"
                , "KHACH_HANG"
                , "DIA_CHI"
                , "TEN_NHAN_VIEN"
                , "MA_NHAN_VIEN"
                , "DIEN_GIAI"
                , "SO_CT_GOC_KEM_THEO"
                , "LOAI_TIEN"

                , "TK_NO"
                , "TK_THUE_GTGT"
                , "TK_CONG_NO"
                 ,"MasterSortOrder"
                 , "LOAI_KHACH_HANG"
                 , "TY_GIA"


            HAVING SUM("TIEN_THUE_QUY_DOI") <> 0
                   OR SUM("TIEN_THUE") <> 0


            UNION ALL
            SELECT
                "ID_CHUNG_TU"
                  , "MODEL_CHUNG_TU"
                , "NGAY_CHUNG_TU"
                , "NGAY_HACH_TOAN"
                , "SO_CHUNG_TU"
                , "MA_KHACH_HANG"
                , "TEN_KHACH_HANG"
                , "KHACH_HANG"

                , "DIA_CHI"
                , "TEN_NHAN_VIEN"
                , "MA_NHAN_VIEN"
                , "DIEN_GIAI"
                , "SO_CT_GOC_KEM_THEO"
                , "LOAI_TIEN"

                , N'Chiết khấu'              AS "DIEN_GIAI_DEATAIL"
                , "TK_CHIET_KHAU"
                , "TK_NO"
                , "TK_CONG_NO"
                , SUM("TIEN_CK_QUY_DOI") AS "THANH_TIEN_QUY_DOI"
                , SUM("TIEN_CK")        AS "THANH_TIEN"
                 ,1000 AS "SortOrder"
                ,"MasterSortOrder"
                 , "LOAI_KHACH_HANG"
                 , "TY_GIA"


            FROM TMP_KET_QUA
            GROUP BY
                 "ID_CHUNG_TU"
                  , "MODEL_CHUNG_TU"
                , "NGAY_CHUNG_TU"
                , "NGAY_HACH_TOAN"
                , "SO_CHUNG_TU"
                , "MA_KHACH_HANG"
                , "TEN_KHACH_HANG"
                , "KHACH_HANG"

                , "DIA_CHI"
                , "TEN_NHAN_VIEN"
                , "MA_NHAN_VIEN"
                , "DIEN_GIAI"
                , "SO_CT_GOC_KEM_THEO"
                , "LOAI_TIEN"


                , "TK_CHIET_KHAU"
                , "TK_NO"
                , "TK_CONG_NO"
                  ,"MasterSortOrder"
                     , "LOAI_KHACH_HANG"
                 , "TY_GIA"


            HAVING SUM("TIEN_CK_QUY_DOI") <> 0
                   OR SUM("TIEN_CK") <> 0
                   ORDER BY
                "MasterSortOrder" ,
                "SortOrder"

    ;


END $$

;


SELECT *
FROM TMP_KET_QUA_CUOI_CUNG
ORDER BY
                "MasterSortOrder" ,
                "SortOrder"
;
        """
        sql_result = self.execute(query)

        for line in sql_result:
            key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
            master_data = self.env['bao.cao.phieu.thu.mau.day.du'].convert_for_update(line)
            detail_data = self.env['bao.cao.phieu.thu.mau.day.du.chi.tiet'].convert_for_update(line)
            if records.get(key):
                records[key].update(master_data)
                records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.phieu.thu.mau.day.du.chi.tiet'].new(detail_data)

        docs = [records.get(k) for k in records]
        for record in docs:
            strTenKhachHang = ''
            if record.TEN_KHACH_HANG == False:
                record.TEN_KHACH_HANG = ''
            if record.KHACH_HANG == False:
                record.KHACH_HANG = ''
            if record.TEN_KHACH_HANG != '' and record.KHACH_HANG != '':
                if record.LOAI_KHACH_HANG == 0:
                    strTenKhachHang = record.KHACH_HANG + ' - ' + record.TEN_KHACH_HANG
                else:
                    strTenKhachHang = record.KHACH_HANG
            else:
                if record.TEN_KHACH_HANG != '':
                    strTenKhachHang = record.TEN_KHACH_HANG
                elif record.KHACH_HANG != '':
                    strTenKhachHang = record.KHACH_HANG
                else:
                    strTenKhachHang = False
            record.TEN_KHACH_HANG  = strTenKhachHang

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
                tong_tien += line.SO_TIEN
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
            
        return {
            'docs': docs,
        }