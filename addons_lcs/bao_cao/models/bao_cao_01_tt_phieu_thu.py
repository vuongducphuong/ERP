# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_01TT_PHIEU_THU(models.Model):
    _name = 'bao.cao.01tt.phieu.thu'
    _auto = False

    ref = fields.Char(string='Reffence ID')
    ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
    MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')
    NGUOI_NHAN_NGUOI_NOP =  fields.Char(string='Người nhận người nộp')#ContactName
    NGAY_CHUNG_TU =  fields.Date(string='Ngày chứng từ') #RefDate
    NGAY_HACH_TOAN =  fields.Date(string='Ngày hạch toán') #PostedDate
    SO_CHUNG_TU =  fields.Char(string='Số chứng từ') #RefNo
    MA_KHACH_HANG =  fields.Char(string='Mã khách hàng') #AccountObjectName
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
    
    ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.01tt.phieu.thu.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')

    
class BAO_CAO_01TT_PHIEU_THU_REPORT(models.AbstractModel):
    _name = 'report.bao_cao.template_v01_tt'

    @api.model
    def get_report_values(self, docids, data=None):

        refTypeList, records = self.get_reftype_list(data)
        ############### START SQL lấy dữ liệu ###############

        sql_result = self.ham_lay_du_lieu_sql_tra_ve(refTypeList)
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

            master_data = self.env['bao.cao.01tt.phieu.thu'].convert_for_update(line)
            detail_data = self.env['bao.cao.01tt.phieu.thu.chi.tiet'].convert_for_update(line)
            if records.get(key):
                records[key].update(master_data)
                records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.01tt.phieu.thu.chi.tiet'].new(detail_data)
        
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
                tong_tien_quy_doi += line.SO_TIEN
            record.TONG_TIEN = tong_tien
            record.TONG_TIEN_QUY_DOI = tong_tien_quy_doi
           
        
        return {
            'docs': docs,
        }
        
    def ham_lay_du_lieu_sql_tra_ve(self,refTypeList):
        query = """
           DO LANGUAGE plpgsql $$
DECLARE

    ListRefID VARCHAR := N'""" + refTypeList + """';


    rec       RECORD;


BEGIN

    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA
    (
        "ID_CHUNG_TU"          INT,
        "MODEL_CHUNG_TU"       VARCHAR(128),
        "NGUOI_NHAN_NGUOI_NOP" VARCHAR(128),
        "LOAI_CHUNG_TU"        INT,
        "NGAY_CHUNG_TU"        TIMESTAMP,
        "NGAY_HACH_TOAN"       TIMESTAMP,
        "SO_CHUNG_TU"          VARCHAR(255),
        "MA_KHACH_HANG"        VARCHAR,

        "TEN_KHACH_HANG"       VARCHAR(300), -- tthoa edit 6/10/2014 : do có cộng chuỗi nên phải tăng độ dài lên
        "DIA_CHI"              VARCHAR(255),
        "DIEN_GIAI"            VARCHAR(255),
        "SO_CT_GOC_KEM_THEO"   VARCHAR(255),
        "LOAI_TIEN"            VARCHAR(15),
        "TY_GIA"               DECIMAL(22, 4), -- nmtruong 6/5/2016: sửa lỗi 101997 không hiển thị phần thập phân của tỷ giá
        "SO_TIEN"              DECIMAL(22, 4),
        "THANH_TIEN"           DECIMAL(22, 4),
        "TK_NO"                VARCHAR(255),
        "TK_CO"                VARCHAR(255),
        "SortOrderMaster"      INT,
        "SortOrder"            INT


    )
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

    ;

    FOR rec IN
    SELECT
        DISTINCT

         PR."LOAI_CHUNG_TU" AS "LOAI_CHUNG_TU"
    FROM
        TMP_PARAM PR
    LOOP

        IF rec."LOAI_CHUNG_TU" IN (1010, 1011, 1012, 1013)
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    CA."id"
                    , 'account.ex.phieu.thu.chi'      AS "MODEL_CHUNG_TU"
                    , CA."NGUOI_NOP"                  AS "NGUOI_NHAN_NGUOI_NOP"
                    , CA."LOAI_CHUNG_TU"
                    , CA."NGAY_CHUNG_TU"
                    , CA."NGAY_HACH_TOAN"
                    , CA."SO_CHUNG_TU"
                    , AO."MA"
                    , CASE WHEN ao."LOAI_KHACH_HANG" = '0'
                    THEN (CASE WHEN LENGTH(COALESCE(Ca."NGUOI_NOP",
                                                    '')) = 0
                                    OR LENGTH(COALESCE(CA."TEN_DOI_TUONG",
                                                       '')) = 0
                        THEN COALESCE(CA."NGUOI_NOP",
                                      '')
                             || COALESCE(CA."TEN_DOI_TUONG",
                                         '')
                          ELSE CA."NGUOI_NOP"
                               || ' - '
                               || CA."TEN_DOI_TUONG"
                          END)
                      ELSE (CASE WHEN LENGTH(COALESCE("NGUOI_NOP",
                                                      '')) = 0
                          THEN CA."TEN_DOI_TUONG"
                            ELSE "NGUOI_NOP"
                            END)
                      END                             AS "TEN_KHACH_HANG"
                    , CA."DIA_CHI"
                    , CA."DIEN_GIAI"
                    , CA."KEM_THEO_CHUNG_TU_GOC"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = CA."currency_id") AS "LOAI_TIEN"
                    , CA."TY_GIA"
                    , SUM(CASE WHEN
                    (SELECT TK."SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = CAD."TK_NO_ID") LIKE N'111%%'
                    THEN CAD."SO_TIEN_QUY_DOI"
                          ELSE -1 * CAD."SO_TIEN_QUY_DOI"
                          END)                        AS "SO_TIEN"
                    , SUM(CASE WHEN
                    (SELECT TK."SO_TAI_KHOAN"
                     FROM danh_muc_he_thong_tai_khoan TK
                     WHERE TK.id = CAD."TK_NO_ID")
                    LIKE N'111%%'
                    THEN CAD."SO_TIEN"
                          ELSE -1 * CAD."SO_TIEN"
                          END)                        AS "THANH_TIEN"
                    , (SELECT TK."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CAD."TK_NO_ID")  AS "TK_NO"

                    , (SELECT TK."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CAD."TK_CO_ID")  AS "TK_CO"
                    ,P."STT"
                    , MIN(CAD."THU_TU_SAP_XEP_CHI_TIET") AS "SortOrder"


                FROM account_ex_phieu_thu_chi CA
                    INNER JOIN account_ex_phieu_thu_chi_tiet CAD ON CA."id" = CAD."PHIEU_THU_CHI_ID"
                    INNER JOIN TMP_PARAM P ON (P."ID_CHUNG_TU" = CA."id"
                                               AND P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                        )
                    LEFT JOIN res_partner AO ON CA."DOI_TUONG_ID" = AO."id"


                WHERE (SELECT TK."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = CAD."TK_CO_ID") LIKE N'111%%'
                      OR (SELECT TK."SO_TAI_KHOAN"
                          FROM danh_muc_he_thong_tai_khoan TK
                          WHERE TK.id = CAD."TK_NO_ID") LIKE N'111%%'





                GROUP BY
                    CA."id",
                    "MODEL_CHUNG_TU",
                    CA."NGUOI_NOP",
                    CA."LOAI_CHUNG_TU",
                    CA."NGAY_CHUNG_TU",
                    CA."NGAY_HACH_TOAN",
                    CA."SO_CHUNG_TU",
                    AO."MA",
                    CA."TEN_DOI_TUONG",
                    CASE WHEN ao."LOAI_KHACH_HANG" = '0'
                        THEN (CASE WHEN LENGTH(COALESCE(Ca."NGUOI_NOP",
                                                        '')) = 0
                                        OR LENGTH(COALESCE(CA."TEN_DOI_TUONG",
                                                           '')) = 0
                            THEN COALESCE(CA."NGUOI_NOP",
                                          '')
                                 || COALESCE(CA."TEN_DOI_TUONG",
                                             '')
                              ELSE CA."NGUOI_NOP"
                                   || ' - '
                                   || CA."TEN_DOI_TUONG"
                              END)
                    ELSE (CASE WHEN LENGTH(COALESCE("NGUOI_NOP",
                                                    '')) = 0
                        THEN CA."TEN_DOI_TUONG"
                          ELSE "NGUOI_NOP"
                          END)
                    END,
                    CA."DIA_CHI",
                    CA."DIEN_GIAI",
                    CA."KEM_THEO_CHUNG_TU_GOC",
                    CA."currency_id",
                    CA."TY_GIA",
                    CAD."TK_NO_ID",
                    CAD."TK_CO_ID",
                     P."STT"
            ;


            -- 			--Hàng mua trả lại - Tiền mặt, Hàng mua trả lại - Tiền mặt - Không qua kho
        ELSE

            IF rec."LOAI_CHUNG_TU" IN (3031, 3033)
            THEN
                INSERT INTO TMP_KET_QUA
                    SELECT
                        PR."id"
                        , 'purchase.ex.tra.lai.hang.mua'  AS "MODEL_CHUNG_TU"
                        , PR."NGUOI_NOP"                  AS "NGUOI_NHAN_NGUOI_NOP"
                        , -- người nộp
                        PR."LOAI_CHUNG_TU"
                         ,
                        PR."NGAY_CHUNG_TU"
                        , PR."NGAY_HACH_TOAN"
                        , PR."SO_PHIEU_THU"
                        , AO."MA"
                        , CASE WHEN ao."LOAI_KHACH_HANG" = '0'
                        THEN (CASE WHEN LENGTH(COALESCE(PR."NGUOI_NOP",
                                                        '')) = 0
                                        OR LENGTH(COALESCE(PR."TEN_NHA_CUNG_CAP",
                                                           '')) = 0
                            THEN COALESCE(PR."NGUOI_NOP",
                                          '')
                                 || COALESCE(PR."TEN_NHA_CUNG_CAP",
                                             '')
                              ELSE PR."NGUOI_NOP"
                                   || ' - '
                                   || PR."TEN_NHA_CUNG_CAP"
                              END)
                          ELSE (CASE WHEN LENGTH(COALESCE("NGUOI_NOP",
                                                          '')) = 0
                              THEN PR."TEN_NHA_CUNG_CAP"
                                ELSE "NGUOI_NOP"
                                END)
                          END                             AS "TEN_KHACH_HANG"
                        , PR."DIA_CHI_NGUOI_NOP"          AS "DIA_CHI"
                        , PR."LY_DO_NOP"                  AS "DIEN_GIAI"
                        , PR."KEM_THEO_PT"                AS "SO_CT_GOC_KEM_THEO"
                        , (SELECT T."MA_LOAI_TIEN"
                           FROM res_currency T
                           WHERE T.id = PR."currency_id") AS "LOAI_TIEN"
                        , PR."TY_GIA"
                        , SUM(PRD."THANH_TIEN_QUY_DOI"
                              + CASE WHEN PRD."TK_THUE_GTGT_ID" IS NULL
                        THEN PRD."TIEN_THUE_GTGT_QUY_DOI"
                                ELSE 0
                                END)
                        , SUM(PRD."THANH_TIEN"
                              + CASE WHEN PRD."TK_THUE_GTGT_ID" IS NULL
                        THEN PRD."TIEN_THUE_GTGT"
                                ELSE 0
                                END)
                        , CASE WHEN
                        (SELECT "SO_TAI_KHOAN"
                         FROM danh_muc_he_thong_tai_khoan TK
                         WHERE TK.id = PRD."TK_NO_ID") NOT LIKE '111%%'
                        THEN NULL
                          ELSE (SELECT "SO_TAI_KHOAN"
                                FROM danh_muc_he_thong_tai_khoan TK
                                WHERE TK.id = PRD."TK_NO_ID")
                          END
                        , (SELECT "SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan TK
                           WHERE TK.id = PRD."TK_CO_ID")
                          ,P."STT"
                          , MIN(PRD."THU_TU_SAP_XEP_CHI_TIET") AS "SortOrder"


                    FROM purchase_ex_tra_lai_hang_mua AS PR

                        INNER JOIN purchase_ex_tra_lai_hang_mua_chi_tiet AS PRD
                            ON PR."id" = PRD."CHUNG_TU_TRA_LAI_HANG_MUA_ID"
                         INNER JOIN TMP_PARAM P ON (P."ID_CHUNG_TU" = PR."id"
                                               AND P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU")

                        LEFT JOIN res_partner AS AO ON AO."id" = PR."DOI_TUONG_ID"


                    WHERE (SELECT "SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan TK
                           WHERE TK.id = PRD."TK_NO_ID") LIKE N'111%%'




                    GROUP BY
                        PR."id",
                        "MODEL_CHUNG_TU",
                        PR."NGUOI_NOP",
                        PR."LOAI_CHUNG_TU",
                        PR."NGAY_CHUNG_TU",
                        PR."NGAY_HACH_TOAN",
                        PR."SO_PHIEU_THU",

                        AO."MA",
                        pr."TEN_NHA_CUNG_CAP",
                        CASE WHEN AO."LOAI_KHACH_HANG" = '0'
                            THEN (CASE WHEN LENGTH(COALESCE(PR."NGUOI_NOP",
                                                            '')) = 0
                                            OR LENGTH(COALESCE(PR."TEN_NHA_CUNG_CAP",
                                                               '')) = 0
                                THEN COALESCE(PR."NGUOI_NOP",
                                              '')
                                     || COALESCE(PR."TEN_NHA_CUNG_CAP",
                                                 '')
                                  ELSE PR."NGUOI_NOP"
                                       || ' - '
                                       || PR."TEN_NHA_CUNG_CAP"
                                  END)
                        ELSE (CASE WHEN LENGTH(COALESCE("NGUOI_NOP",
                                                        '')) = 0
                            THEN PR."TEN_NHA_CUNG_CAP"
                              ELSE "NGUOI_NOP"
                              END)
                        END,
                        PR."DIA_CHI_NGUOI_NOP",
                        PR."LY_DO_NOP",
                        PR."KEM_THEO_PT",
                        (SELECT T."MA_LOAI_TIEN"
                         FROM res_currency T
                         WHERE T.id = PR."currency_id"),
                        PR."TY_GIA",
                        CASE WHEN
                            (SELECT "SO_TAI_KHOAN"
                             FROM danh_muc_he_thong_tai_khoan TK
                             WHERE TK.id = PRD."TK_NO_ID") NOT LIKE '111%%'
                            THEN NULL
                        ELSE (SELECT "SO_TAI_KHOAN"
                              FROM danh_muc_he_thong_tai_khoan TK
                              WHERE TK.id = PRD."TK_NO_ID")
                        END,
                        (SELECT "SO_TAI_KHOAN"
                         FROM danh_muc_he_thong_tai_khoan TK
                         WHERE TK.id = PRD."TK_CO_ID"),
                        P."STT"


                    UNION ALL
                    SELECT
                        PR."id"
                        , 'purchase.ex.tra.lai.hang.mua'    AS "MODEL_CHUNG_TU"
                        , PR."NGUOI_NOP"                    AS "NGUOI_NHAN_NGUOI_NOP"
                        , PR."LOAI_CHUNG_TU"
                         ,
                        PR."NGAY_CHUNG_TU"
                        , PR."NGAY_HACH_TOAN"
                        , PR."SO_PHIEU_THU"
                        , AO."MA"
                        , CASE WHEN ao."LOAI_KHACH_HANG" = '0'
                        THEN (CASE WHEN LENGTH(COALESCE(PR."NGUOI_NOP",
                                                        '')) = 0
                                        OR LENGTH(COALESCE(PR."TEN_NHA_CUNG_CAP",
                                                           '')) = 0
                            THEN COALESCE(PR."NGUOI_NOP",
                                          '')
                                 || COALESCE(PR."TEN_NHA_CUNG_CAP",
                                             '')
                              ELSE PR."NGUOI_NOP"
                                   || ' - '
                                   || PR."TEN_NHA_CUNG_CAP"
                              END)
                          ELSE (CASE WHEN LENGTH(COALESCE("NGUOI_NOP",
                                                          '')) = 0
                              THEN PR."TEN_NHA_CUNG_CAP"
                                ELSE "NGUOI_NOP"
                                END)
                          END                               AS "TEN_KHACH_HANG"
                        , PR."DIA_CHI_NGUOI_NOP"            AS "DIA_CHI"
                        , PR."LY_DO_NOP"                    AS "DIEN_GIAI"
                        , PR."KEM_THEO_PT"                  AS "SO_CT_GOC_KEM_THEO"


                        , (SELECT T."MA_LOAI_TIEN"
                           FROM res_currency T
                           WHERE T.id = PR."currency_id")   AS "LOAI_TIEN"
                        , PR."TY_GIA"
                        , SUM(PRD."TIEN_THUE_GTGT_QUY_DOI") AS "SO_TIEN"
                        , SUM(PRD."TIEN_THUE_GTGT")         AS "THANH_TIEN"
                        , (SELECT "SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan TK
                           WHERE TK.id = PRD."TK_NO_ID")
                        , (SELECT "SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan TK
                           WHERE TK.id = PRD."TK_THUE_GTGT_ID")
                          ,P."STT"
                          , 20000 + MAX(PRD."THU_TU_SAP_XEP_CHI_TIET")

                    FROM purchase_ex_tra_lai_hang_mua AS PR
                         INNER JOIN TMP_PARAM P ON (P."ID_CHUNG_TU" = PR."id"
                                               AND P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU")
                        INNER JOIN purchase_ex_tra_lai_hang_mua_chi_tiet AS PRD
                            ON PR."id" = PRD."CHUNG_TU_TRA_LAI_HANG_MUA_ID"
                        LEFT JOIN res_partner AS AO ON AO."id" = PR."DOI_TUONG_ID"
                        LEFT JOIN res_partner AOE ON PR."NHAN_VIEN_ID" = AOE."id"

                    WHERE (SELECT "SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan TK
                           WHERE TK.id = PRD."TK_NO_ID") LIKE N'111%%'
                          AND

                          (SELECT "SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan TK
                           WHERE TK.id = PRD."TK_THUE_GTGT_ID")

                          IS NOT NULL
                          AND (SELECT "SO_TAI_KHOAN"
                               FROM danh_muc_he_thong_tai_khoan TK
                               WHERE TK.id = PRD."TK_THUE_GTGT_ID") <> ''
                          AND PRD."TIEN_THUE_GTGT_QUY_DOI" <> 0


                    GROUP BY
                        PR."id",
                        "MODEL_CHUNG_TU",
                        PR."NGUOI_NOP",
                        PR."LOAI_CHUNG_TU",
                        PR."NGAY_CHUNG_TU",
                        PR."NGAY_HACH_TOAN",
                        PR."SO_PHIEU_THU",
                        AO."MA",
                        pr."TEN_NHA_CUNG_CAP",
                        CASE WHEN ao."LOAI_KHACH_HANG" = '0'
                            THEN (CASE WHEN LENGTH(COALESCE(PR."NGUOI_NOP",
                                                            '')) = 0
                                            OR LENGTH(COALESCE(PR."TEN_NHA_CUNG_CAP",
                                                               '')) = 0
                                THEN COALESCE(PR."NGUOI_NOP",
                                              '')
                                     || COALESCE(PR."TEN_NHA_CUNG_CAP",
                                                 '')
                                  ELSE PR."NGUOI_NOP"
                                       || ' - '
                                       || PR."TEN_NHA_CUNG_CAP"
                                  END)
                        ELSE (CASE WHEN LENGTH(COALESCE("NGUOI_NOP",
                                                        '')) = 0
                            THEN PR."TEN_NHA_CUNG_CAP"
                              ELSE "NGUOI_NOP"
                              END)
                        END,
                        PR."DIA_CHI_NGUOI_NOP",
                        PR."LY_DO_NOP",
                        PR."KEM_THEO_PT",
                        (SELECT T."MA_LOAI_TIEN"
                         FROM res_currency T
                         WHERE T.id = PR."currency_id"),
                        PR."TY_GIA",

                        (SELECT "SO_TAI_KHOAN"
                         FROM danh_muc_he_thong_tai_khoan TK
                         WHERE TK.id = PRD."TK_NO_ID"),
                        (SELECT "SO_TAI_KHOAN"
                         FROM danh_muc_he_thong_tai_khoan TK
                         WHERE TK.id = PRD."TK_THUE_GTGT_ID")
                          ,P."STT"
                ;


                -- Hàng mua giảm giá - Tiền mặt, Hàng mua giảm giá - Tiền mặt - Không qua kho
            ELSE
                IF rec."LOAI_CHUNG_TU" IN (3041, 3043)
                THEN
                    INSERT INTO TMP_KET_QUA
                        SELECT
                            PR."id"
                            , 'purchase.ex.giam.gia.hang.mua' AS "MODEL_CHUNG_TU"
                            , PR."NGUOI_NOP"                  AS "NGUOI_NHAN_NGUOI_NOP"
                            , -- người nộp
                            PR."LOAI_CHUNG_TU"
                            , PR."NGAY_CHUNG_TU"
                            , PR."NGAY_HACH_TOAN"
                            , PR."SO_CHUNG_TU"
                            , AO."MA"
                            , CASE WHEN ao."LOAI_KHACH_HANG" = '0'
                            THEN (CASE
                                  WHEN LENGTH(COALESCE(PR."NGUOI_NOP",
                                                       '')) = 0
                                       OR LENGTH(COALESCE(PR."TEN_NHA_CUNG_CAP",
                                                          '')) = 0
                                      THEN COALESCE(PR."NGUOI_NOP",
                                                    '')
                                           || COALESCE(PR."TEN_NHA_CUNG_CAP",
                                                       '')
                                  ELSE PR."NGUOI_NOP"
                                       || ' - '
                                       || PR."TEN_NHA_CUNG_CAP"
                                  END)
                              ELSE (CASE
                                    WHEN LENGTH(COALESCE("NGUOI_NOP",
                                                         '')) = 0
                                        THEN PR."TEN_NHA_CUNG_CAP"
                                    ELSE "NGUOI_NOP"
                                    END)
                              END                             AS "TEN_KHACH_HANG"
                            , PR."DIA_CHI"                    AS "DIA_CHI"
                            , PR."DIEN_GIAI"
                            , PR."KEM_THEO_CT_GOC"
                            , (SELECT T."MA_LOAI_TIEN"
                               FROM res_currency T
                               WHERE T.id = PR."currency_id") AS "LOAI_TIEN"
                            , PR."TY_GIA"
                            , SUM(PRD."THANH_TIEN_QUY_DOI"
                                  + CASE WHEN PRD."TK_THUE_GTGT_ID" IS NULL
                            THEN PRD."TIEN_THUE_GTGT_QUY_DOI"
                                    ELSE 0
                                    END)
                            , SUM(PRD."THANH_TIEN"
                                  + CASE WHEN PRD."TK_THUE_GTGT_ID" IS NULL
                            THEN PRD."TIEN_THUE_GTGT"
                                    ELSE 0
                                    END)
                            , (SELECT "SO_TAI_KHOAN"
                               FROM danh_muc_he_thong_tai_khoan TK
                               WHERE TK.id = PRD."TK_NO_ID")  AS "TK_NO"
                            , (SELECT "SO_TAI_KHOAN"
                               FROM danh_muc_he_thong_tai_khoan TK
                               WHERE TK.id = PRD."TK_CO_ID")  AS "TK_CO"
                              ,P."STT"
                               , MIN(PRD."THU_TU_SAP_XEP_CHI_TIET")



                        FROM purchase_ex_giam_gia_hang_mua AS PR
                            INNER JOIN TMP_PARAM P ON (P."ID_CHUNG_TU" = PR."id"
                                                       AND P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                                )
                            INNER JOIN purchase_ex_giam_gia_hang_mua_chi_tiet
                                AS PRD ON PR."id" = PRD."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID"
                            LEFT JOIN res_partner AS AO ON AO."id" = PR."DOI_TUONG_ID"
                            LEFT JOIN res_partner AOE ON PR."NHAN_VIEN_ID" = AOE."id"

                        WHERE (SELECT "SO_TAI_KHOAN"
                               FROM danh_muc_he_thong_tai_khoan TK
                               WHERE TK.id = PRD."TK_NO_ID") LIKE N'111%%'


                        GROUP BY
                            PR."id",
                            "MODEL_CHUNG_TU",
                            PR."NGUOI_NOP",
                            PR."selection_chung_tu_giam_gia_hang_mua",
                            PR."NGAY_CHUNG_TU",
                            PR."NGAY_HACH_TOAN",
                            PR."SO_CHUNG_TU",
                            AO."MA",
                            pr."TEN_NHA_CUNG_CAP",
                            CASE WHEN ao."LOAI_KHACH_HANG" = '0'
                                THEN (CASE
                                      WHEN LENGTH(COALESCE(PR."NGUOI_NOP",
                                                           '')) = 0
                                           OR LENGTH(COALESCE(PR."TEN_NHA_CUNG_CAP",
                                                              '')) = 0
                                          THEN COALESCE(PR."NGUOI_NOP",
                                                        '')
                                               || COALESCE(PR."TEN_NHA_CUNG_CAP",
                                                           '')
                                      ELSE PR."NGUOI_NOP"
                                           || ' - '
                                           || PR."TEN_NHA_CUNG_CAP"
                                      END)
                            ELSE (CASE
                                  WHEN LENGTH(COALESCE("NGUOI_NOP",
                                                       '')) = 0
                                      THEN PR."TEN_NHA_CUNG_CAP"
                                  ELSE "NGUOI_NOP"
                                  END)
                            END,
                            PR."DIA_CHI",
                            PR."DIEN_GIAI",
                            PR."KEM_THEO_CT_GOC",
                            (SELECT T."MA_LOAI_TIEN"
                             FROM res_currency T
                             WHERE T.id = PR."currency_id"),
                            PR."TY_GIA",

                            (SELECT "SO_TAI_KHOAN"
                             FROM danh_muc_he_thong_tai_khoan TK
                             WHERE TK.id = PRD."TK_NO_ID"),
                            (SELECT "SO_TAI_KHOAN"
                             FROM danh_muc_he_thong_tai_khoan TK
                             WHERE TK.id = PRD."TK_CO_ID")
                              ,P."STT"


                        UNION ALL -- Lấy tài khoản thuế
                        SELECT
                            PR."id"
                            , 'purchase.ex.giam.gia.hang.mua'   AS "MODEL_CHUNG_TU"
                            , PR."NGUOI_NOP"                    AS "NGUOI_NHAN_NGUOI_NOP"
                            , -- người nộp
                            PR."LOAI_CHUNG_TU"
                            , PR."NGAY_CHUNG_TU"
                            , PR."NGAY_HACH_TOAN"
                            , PR."SO_CHUNG_TU"
                            , AO."MA"
                            , CASE WHEN ao."LOAI_KHACH_HANG" = '0'
                            THEN (CASE
                                  WHEN LENGTH(COALESCE(PR."NGUOI_NOP",
                                                       '')) = 0
                                       OR LENGTH(COALESCE(PR."TEN_NHA_CUNG_CAP",
                                                          '')) = 0
                                      THEN COALESCE(PR."NGUOI_NOP",
                                                    '')
                                           || COALESCE(PR."TEN_NHA_CUNG_CAP",
                                                       '')
                                  ELSE PR."NGUOI_NOP"
                                       || ' - '
                                       || PR."TEN_NHA_CUNG_CAP"
                                  END)
                              ELSE (CASE
                                    WHEN LENGTH(COALESCE("NGUOI_NOP",
                                                         '')) = 0
                                        THEN PR."TEN_NHA_CUNG_CAP"
                                    ELSE "NGUOI_NOP"
                                    END)
                              END                               AS "TEN_KHACH_HANG"
                            , PR."DIA_CHI"                      AS "DIA_CHI"
                            , PR."DIEN_GIAI"
                            , PR."KEM_THEO_CT_GOC"
                            , (SELECT T."MA_LOAI_TIEN"
                               FROM res_currency T
                               WHERE T.id = PR."currency_id")   AS "LOAI_TIEN"
                            , PR."TY_GIA"
                            , SUM(PRD."TIEN_THUE_GTGT_QUY_DOI") AS "SO_TIEN"
                            , SUM(PRD."TIEN_THUE_GTGT")         AS "THANH_TIEN"
                            , (SELECT "SO_TAI_KHOAN"
                               FROM danh_muc_he_thong_tai_khoan TK
                               WHERE TK.id = PRD."TK_NO_ID")
                            , (SELECT "SO_TAI_KHOAN"
                               FROM danh_muc_he_thong_tai_khoan TK
                               WHERE TK.id = PRD."TK_THUE_GTGT_ID")
                              ,P."STT"
                               , 20000 + MAX(PRD."THU_TU_SAP_XEP_CHI_TIET")

                        FROM purchase_ex_giam_gia_hang_mua AS PR
                            INNER JOIN TMP_PARAM P ON (P."ID_CHUNG_TU" = PR."id"
                                                       AND P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                                )
                            INNER JOIN purchase_ex_giam_gia_hang_mua_chi_tiet
                                AS PRD ON PR."id" = PRD."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID"
                            LEFT JOIN res_partner AS AO ON AO."id" = PR."DOI_TUONG_ID"
                            LEFT JOIN res_partner AOE ON PR."NHAN_VIEN_ID" = AOE."id"

                        WHERE (SELECT "SO_TAI_KHOAN"
                               FROM danh_muc_he_thong_tai_khoan TK
                               WHERE TK.id = PRD."TK_NO_ID") LIKE N'111%%'
                              AND

                              (SELECT "SO_TAI_KHOAN"
                               FROM danh_muc_he_thong_tai_khoan TK
                               WHERE TK.id = PRD."TK_THUE_GTGT_ID")

                              IS NOT NULL
                              AND (SELECT "SO_TAI_KHOAN"
                                   FROM danh_muc_he_thong_tai_khoan TK
                                   WHERE TK.id = PRD."TK_THUE_GTGT_ID") <> ''
                              AND PRD."TIEN_THUE_GTGT_QUY_DOI" <> 0



                        GROUP BY
                            PR."id"
                            , "MODEL_CHUNG_TU"
                            , PR."NGUOI_NOP"
                            , -- người nộp
                            PR."LOAI_CHUNG_TU"
                            , PR."NGAY_CHUNG_TU"
                            , PR."NGAY_HACH_TOAN"
                            , PR."SO_CHUNG_TU"
                            , AO."MA"
                            , CASE WHEN ao."LOAI_KHACH_HANG" = '0'
                            THEN (CASE
                                  WHEN LENGTH(COALESCE(PR."NGUOI_NOP",
                                                       '')) = 0
                                       OR LENGTH(COALESCE(PR."TEN_NHA_CUNG_CAP",
                                                          '')) = 0
                                      THEN COALESCE(PR."NGUOI_NOP",
                                                    '')
                                           || COALESCE(PR."TEN_NHA_CUNG_CAP",
                                                       '')
                                  ELSE PR."NGUOI_NOP"
                                       || ' - '
                                       || PR."TEN_NHA_CUNG_CAP"
                                  END)
                              ELSE (CASE
                                    WHEN LENGTH(COALESCE("NGUOI_NOP",
                                                         '')) = 0
                                        THEN PR."TEN_NHA_CUNG_CAP"
                                    ELSE "NGUOI_NOP"
                                    END)
                              END
                            , PR."DIA_CHI"
                            , PR."DIEN_GIAI"
                            , PR."KEM_THEO_CT_GOC"
                            , (SELECT T."MA_LOAI_TIEN"
                               FROM res_currency T
                               WHERE T.id = PR."currency_id")
                            , PR."TY_GIA"

                            , (SELECT "SO_TAI_KHOAN"
                               FROM danh_muc_he_thong_tai_khoan TK
                               WHERE TK.id = PRD."TK_NO_ID")
                            , (SELECT "SO_TAI_KHOAN"
                               FROM danh_muc_he_thong_tai_khoan TK
                               WHERE TK.id = PRD."TK_THUE_GTGT_ID")
                              ,P."STT"
                    ;


                    -- Bán hàng hóa, dịch vụ trong nước - Tiền mặt, Bán hàng đại lý bán đúng giá - Tiền mặt
                ELSE
                    IF rec."LOAI_CHUNG_TU" IN (3531, 3535)
                    THEN
                        INSERT INTO TMP_KET_QUA
                            SELECT
                                SV."id"
                                , 'sale.document'                 AS "MODEL_CHUNG_TU"
                                , SV."NGUOI_LIEN_HE"              AS "NGUOI_NHAN_NGUOI_NOP"
                                , SV."LOAI_CHUNG_TU"
                                , SV."NGAY_CHUNG_TU"
                                , SV."NGAY_HACH_TOAN"
                                , SV."SO_CHUNG_TU"
                                , AO."MA"

                                , CASE WHEN ao."LOAI_KHACH_HANG" = '0'
                                THEN (CASE
                                      WHEN LENGTH(COALESCE(SV."NGUOI_LIEN_HE",
                                                           '')) = 0
                                           OR LENGTH(COALESCE(SV."TEN_KHACH_HANG",
                                                              '')) = 0
                                          THEN COALESCE(SV."NGUOI_LIEN_HE",
                                                        '')
                                               || COALESCE(SV."TEN_KHACH_HANG",
                                                           '')
                                      ELSE SV."NGUOI_LIEN_HE"
                                           || ' - '
                                           || SV."TEN_KHACH_HANG"
                                      END)
                                  ELSE (CASE
                                        WHEN LENGTH(COALESCE("NGUOI_LIEN_HE",
                                                             '')) = 0
                                            THEN SV."TEN_KHACH_HANG"
                                        ELSE "NGUOI_LIEN_HE"
                                        END)
                                  END                             AS "TEN_KHACH_HANG"
                                , SV."DIA_CHI"
                                , SV."DIEN_GIAI"
                                , SV."KEM_THEO_CHUNG_TU_GOC"
                                , (SELECT T."MA_LOAI_TIEN"
                                   FROM res_currency T
                                   WHERE T.id = SV."currency_id") AS "LOAI_TIEN"
                                , SV."TY_GIA"
                                , SUM(SVD."THANH_TIEN_QUY_DOI"
                                      - SVD."TIEN_CK_QUY_DOI"
                                      + CASE
                                        WHEN SVD."TK_THUE_GTGT_ID" IS NULL
                                            THEN SVD."TIEN_THUE_GTGT_QUY_DOI"
                                        ELSE 0
                                        END)
                                , SUM(SVD."THANH_TIEN"
                                      - SVD."TIEN_CHIET_KHAU"
                                      + CASE
                                        WHEN SVD."TK_THUE_GTGT_ID" IS NULL
                                            THEN SVD."TIEN_THUE_GTGT"
                                        ELSE 0
                                        END)
                                , (SELECT "SO_TAI_KHOAN"
                                   FROM danh_muc_he_thong_tai_khoan TK
                                   WHERE TK.id = SVD."TK_NO_ID")
                                , (SELECT "SO_TAI_KHOAN"
                                   FROM danh_muc_he_thong_tai_khoan TK
                                   WHERE TK.id = SVD."TK_CO_ID")
                                  ,P."STT"
                                    , MIN(SVD."THU_TU_SAP_XEP_CHI_TIET")


                            FROM sale_document AS SV
                                INNER JOIN TMP_PARAM P ON (P."ID_CHUNG_TU" = SV."id"
                                                           AND P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                                    )
                                INNER JOIN sale_document_line
                                    AS SVD ON SV."id" = SVD."SALE_DOCUMENT_ID"
                                LEFT JOIN res_partner
                                    AS AO ON AO."id" = SV."DOI_TUONG_ID"
                                LEFT JOIN res_partner AOE ON SV."NHAN_VIEN_ID" = AOE."id"

                            WHERE (SELECT "SO_TAI_KHOAN"
                                   FROM danh_muc_he_thong_tai_khoan TK
                                   WHERE TK.id = SVD."TK_NO_ID") LIKE N'111%%'


                            GROUP BY
                                SV."id",
                                "MODEL_CHUNG_TU",
                                SV."NGUOI_LIEN_HE",
                                SV."LOAI_NGHIEP_VU",
                                SV."NGAY_CHUNG_TU",
                                SV."NGAY_HACH_TOAN",
                                SV."SO_CHUNG_TU",
                                AO."MA",
                                sv."TEN_KHACH_HANG",
                                CASE WHEN ao."LOAI_KHACH_HANG" = '0'
                                    THEN (CASE
                                          WHEN LENGTH(COALESCE(SV."NGUOI_LIEN_HE",
                                                               '')) = 0
                                               OR LENGTH(COALESCE(SV."TEN_KHACH_HANG",
                                                                  '')) = 0
                                              THEN COALESCE(SV."NGUOI_LIEN_HE",
                                                            '')
                                                   || COALESCE(SV."TEN_KHACH_HANG",
                                                               '')
                                          ELSE SV."NGUOI_LIEN_HE"
                                               || ' - '
                                               || SV."TEN_KHACH_HANG"
                                          END)
                                ELSE (CASE
                                      WHEN LENGTH(COALESCE("NGUOI_LIEN_HE",
                                                           '')) = 0
                                          THEN SV."TEN_KHACH_HANG"
                                      ELSE "NGUOI_LIEN_HE"
                                      END)
                                END,
                                SV."DIA_CHI",
                                SV."DIEN_GIAI",
                                SV."KEM_THEO_CHUNG_TU_GOC",
                                (SELECT T."MA_LOAI_TIEN"
                                 FROM res_currency T
                                 WHERE T.id = SV."currency_id"),

                                SV."TY_GIA",


                                (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = SVD."TK_NO_ID"),
                                (SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = SVD."TK_CO_ID")
                                  ,P."STT"


                            UNION ALL -- Lấy TK thuế GTGT
                            SELECT
                                SV."id"
                                , 'sale.document'                 AS "MODEL_CHUNG_TU"
                                , SV."NGUOI_LIEN_HE"              AS "NGUOI_NHAN_NGUOI_NOP"
                                , SV."LOAI_CHUNG_TU"
                                , SV."NGAY_CHUNG_TU"
                                , SV."NGAY_HACH_TOAN"
                                , SV."SO_CHUNG_TU"
                                , AO."MA"

                                , CASE WHEN ao."LOAI_KHACH_HANG" = '0'
                                THEN (CASE
                                      WHEN LENGTH(COALESCE(SV."NGUOI_LIEN_HE",
                                                           '')) = 0
                                           OR LENGTH(COALESCE(SV."TEN_KHACH_HANG",
                                                              '')) = 0
                                          THEN COALESCE(SV."NGUOI_LIEN_HE",
                                                        '')
                                               || COALESCE(SV."TEN_KHACH_HANG",
                                                           '')
                                      ELSE SV."NGUOI_LIEN_HE"
                                           || ' - '
                                           || SV."TEN_KHACH_HANG"
                                      END)
                                  ELSE (CASE
                                        WHEN LENGTH(COALESCE("NGUOI_LIEN_HE",
                                                             '')) = 0
                                            THEN SV."TEN_KHACH_HANG"
                                        ELSE "NGUOI_LIEN_HE"
                                        END)
                                  END                             AS "TEN_KHACH_HANG"
                                , SV."DIA_CHI"
                                , SV."DIEN_GIAI"
                                , SV."KEM_THEO_CHUNG_TU_GOC"
                                , (SELECT T."MA_LOAI_TIEN"
                                   FROM res_currency T
                                   WHERE T.id = SV."currency_id") AS "LOAI_TIEN"
                                , SV."TY_GIA"
                                , SUM(SVD."TIEN_THUE_GTGT_QUY_DOI")
                                , SUM(SVD."TIEN_THUE_GTGT")
                                , (SELECT "SO_TAI_KHOAN"
                                   FROM danh_muc_he_thong_tai_khoan TK
                                   WHERE TK.id = SVD."TK_NO_ID")
                                , (SELECT "SO_TAI_KHOAN"
                                   FROM danh_muc_he_thong_tai_khoan TK
                                   WHERE TK.id = SVD."TK_THUE_GTGT_ID")
                                  ,P."STT"
                                   , 20000 + MAX(SVD."THU_TU_SAP_XEP_CHI_TIET")

                            FROM sale_document AS SV
                                INNER JOIN TMP_PARAM P ON (P."ID_CHUNG_TU" = SV."id"
                                                           AND P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                                    )
                                INNER JOIN sale_document_line
                                    AS SVD ON SV."id" = SVD."SALE_DOCUMENT_ID"
                                LEFT JOIN res_partner
                                    AS AO ON AO."id" = SV."DOI_TUONG_ID"
                                LEFT JOIN res_partner AOE ON SV."NHAN_VIEN_ID" = AOE."id"


                            WHERE (SELECT "SO_TAI_KHOAN"
                                   FROM danh_muc_he_thong_tai_khoan TK
                                   WHERE TK.id = SVD."TK_NO_ID") LIKE N'111%%'
                                  AND

                                  (SELECT "SO_TAI_KHOAN"
                                   FROM danh_muc_he_thong_tai_khoan TK
                                   WHERE TK.id = SVD."TK_THUE_GTGT_ID")

                                  IS NOT NULL
                                  AND (SELECT "SO_TAI_KHOAN"
                                       FROM danh_muc_he_thong_tai_khoan TK
                                       WHERE TK.id = SVD."TK_THUE_GTGT_ID") <> ''
                                  AND SVD."TIEN_THUE_GTGT_QUY_DOI" <> 0




                            GROUP BY
                                SV."id"
                                , "MODEL_CHUNG_TU"
                                , SV."NGUOI_LIEN_HE"
                                , SV."LOAI_CHUNG_TU"
                                , SV."NGAY_CHUNG_TU"
                                , SV."NGAY_HACH_TOAN"
                                , SV."SO_CHUNG_TU"
                                , AO."MA"

                                , CASE WHEN ao."LOAI_KHACH_HANG" = '0'
                                THEN (CASE
                                      WHEN LENGTH(COALESCE(SV."NGUOI_LIEN_HE",
                                                           '')) = 0
                                           OR LENGTH(COALESCE(SV."TEN_KHACH_HANG",
                                                              '')) = 0
                                          THEN COALESCE(SV."NGUOI_LIEN_HE",
                                                        '')
                                               || COALESCE(SV."TEN_KHACH_HANG",
                                                           '')
                                      ELSE SV."NGUOI_LIEN_HE"
                                           || ' - '
                                           || SV."TEN_KHACH_HANG"
                                      END)
                                  ELSE (CASE
                                        WHEN LENGTH(COALESCE("NGUOI_LIEN_HE",
                                                             '')) = 0
                                            THEN SV."TEN_KHACH_HANG"
                                        ELSE "NGUOI_LIEN_HE"
                                        END)
                                  END
                                , SV."DIA_CHI"
                                , SV."DIEN_GIAI"
                                , SV."KEM_THEO_CHUNG_TU_GOC"
                                , (SELECT T."MA_LOAI_TIEN"
                                   FROM res_currency T
                                   WHERE T.id = SV."currency_id")
                                , SV."TY_GIA"
                                , (SELECT "SO_TAI_KHOAN"
                                   FROM danh_muc_he_thong_tai_khoan TK
                                   WHERE TK.id = SVD."TK_NO_ID")
                                , (SELECT "SO_TAI_KHOAN"
                                   FROM danh_muc_he_thong_tai_khoan TK
                                   WHERE TK.id = SVD."TK_THUE_GTGT_ID")
                                  ,P."STT"
                        ;

                    END IF
                    ;
                END IF
                ;

            END IF
            ;

        END IF
    ;

    END LOOP
    ;


END $$

;
SELECT *
FROM TMP_KET_QUA
ORDER BY
    "SortOrderMaster",
    "SortOrder"

        """
        return self.execute(query)

        
        