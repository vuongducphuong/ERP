# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from datetime import timedelta, datetime

class BAO_CAO_CHUNG_TU_KE_TOAN(models.Model):
    _name = 'bao.cao.chung.tu.ke.toan'
    _auto = False

    ref = fields.Char(string='Reffence ID')
    
    ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
    MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')
    LOAI_CHUNG_TU =  fields.Integer(string='Loại chứng từ')#RefType
    SO_CHUNG_TU =  fields.Char(string='Số chứng từ') #RefNo
    NGAY_CHUNG_TU =  fields.Date(string='Ngày chứng từ') #RefDate
    NGAY_HACH_TOAN =  fields.Date(string='Ngày hạch toán') #PostedDate
    HAN_THANH_TOAN =  fields.Date(string='Hạn thanh toán') #DueDate
    DOI_TUONG_ID = fields.Many2one('res.partner')#AccountObjectID
    TEN_KHACH_HANG =  fields.Char(string='Tên khách hàng') #AccountObjectName
    DIA_CHI =  fields.Char(string='Địa chỉ') #AccountObjectAddress
    DIEN_GIAI =  fields.Char(string='Diễn giải') #JournalMemo
    LOAI_TIEN =  fields.Char(string='Loại tiền') #CurrencyID
    TY_GIA = fields.Monetary(string='Tỷ giá', currency_field='currency_id')#ExchangeRate
    SortOrderMaster  = fields.Integer(string='Thứ tự sắp xếp')#SortOrderMaster

    TONG_TIEN =  fields.Monetary(string='Tổng tiền', currency_field='currency_id')
    TONG_TIEN_QUY_DOI =  fields.Float(string='Tổng tiền quy đổi',digits= decimal_precision.get_precision('VND'))


    

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    
    CHI_TIET_IDS = fields.One2many('bao.cao.chung.tu.ke.toan.chi.tiet', 'CHUNG_TU_ID')


class BAO_CAO_CHUNG_TU_KE_TOAN_REPORT(models.AbstractModel):
    _name = 'report.bao_cao.template_accountingvoucher'


    @api.model
    def get_report_values(self, docids, data=None):

        refTypeList, records = self.get_reftype_list(data)
        ############### START SQL lấy dữ liệu ###############

        sql_result = self.ham_lay_du_lieu_sql_tra_ve(refTypeList)

        for line in sql_result:
            key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
            master_data = self.env['bao.cao.chung.tu.ke.toan'].convert_for_update(line)
            detail_data = self.env['bao.cao.chung.tu.ke.toan.chi.tiet'].convert_for_update(line)
            if records.get(key):
                records[key].update(master_data)
                records[key].CHI_TIET_IDS += self.env['bao.cao.chung.tu.ke.toan.chi.tiet'].new(detail_data)
        
        docs = [records.get(k) for k in records]

        for records in docs:
            # if not records.NGAY_CHUNG_TU:
            #     records.NGAY_CHUNG_TU = ""
            # else:
            #     records.NGAY_CHUNG_TU = datetime.strptime(records.NGAY_CHUNG_TU,'%Y-%m-%d').date().strftime('%d/%m/%Y')
            
            if not records.LOAI_TIEN:
                records.currency_id = self.lay_loai_tien_mac_dinh()
            else:
                loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', records.LOAI_TIEN)],limit=1)
                if loai_tien_id:
                    records.currency_id = loai_tien_id.id
            
            tong_tien = 0
            tong_tien_quy_doi = 0
            
            for line in records.CHI_TIET_IDS:
                line.currency_id = records.currency_id
                tong_tien += line.THANH_TIEN
                tong_tien_quy_doi += line.THANH_TIEN_QUY_DOI
                
            records.TONG_TIEN = tong_tien
            records.TONG_TIEN_QUY_DOI = tong_tien_quy_doi
     
        return {
            'docs': docs,
        }

    def ham_lay_du_lieu_sql_tra_ve(self,refTypeList):
        query = """
        DO LANGUAGE plpgsql $$
DECLARE

    ListParam                        VARCHAR := N'""" + refTypeList + """';

    rec                              RECORD;


    PHUONG_PHAP_TINH_THUE            VARCHAR;

    LOAI_TIEN_CHINH                  INT;

    CHE_DO_KE_TOAN                   VARCHAR;

    PHUONG_PHAP_TINH_TY_GIA_XUAT_QUY VARCHAR;


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


    SELECT value
    INTO PHUONG_PHAP_TINH_THUE
    FROM ir_config_parameter
    WHERE key = 'he_thong.PHUONG_PHAP_TINH_THUE'
    FETCH FIRST 1 ROW ONLY
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA
    (
        "ID_CHUNG_TU"          INT,
        "MODEL_CHUNG_TU"       VARCHAR(255),
        "LOAI_CHUNG_TU"        INT,
        "SO_CHUNG_TU"          VARCHAR(127),
        "NGAY_CHUNG_TU"        TIMESTAMP,
        "NGAY_HACH_TOAN"       TIMESTAMP,
        "HAN_THANH_TOAN"       TIMESTAMP,
        "DOI_TUONG_ID"         INT,
        "TEN_KHACH_HANG"       VARCHAR(255),
        "DIA_CHI"              VARCHAR(255),
        "DIEN_GIAI_DETAIL"     VARCHAR(255),
        "TK_NO"                VARCHAR(255),
        "TK_CO"                VARCHAR(255),
        "THANH_TIEN"           DECIMAL(25, 8),
        "THANH_TIEN_QUY_DOI"   DECIMAL(25, 8),
        "PHEP_TINH_CHUYEN_DOI" VARCHAR(127),
        "LOAI_TIEN"            VARCHAR(15), -- CR 53239: Bổ sung Tỷ giá, Quy đổi
        "TY_GIA"               DECIMAL(22, 8), -- CR 53239: Bổ sung Tỷ giá, Quy đổi
        "STT"                  INT,

        "DIEN_GIAI"            VARCHAR(255),
        "TINH_CHAT"            INT,
        "RowOrder"             INT,
        "SortOrderMaster"      INT


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
        "ID_CHUNG_TU"     INT,
        "LOAI_CHUNG_TU"   INT,

        "STT"             INT DEFAULT NEXTVAL('TMP_PARAM_seq')
            PRIMARY KEY,
        "SortOrderMaster" INT
    )
    ;

    INSERT INTO TMP_PARAM
        SELECT

            Value1
            , Value2


        FROM CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(ListParam, ',', ';') F
            INNER JOIN danh_muc_reftype R ON F.Value2 = R."REFTYPE"
    ;

    UPDATE TMP_PARAM
    SET "SortOrderMaster" = "STT"
    ;

    INSERT INTO TMP_PARAM

        SELECT
            C."ID_CHUNG_TU_QUAN_HE" AS "ID_CHUNG_TU"
            , C."LOAI_CHUNG_TU_QUAN_HE"
        FROM TMP_PARAM A
            INNER JOIN LAY_RA_THONG_TIN_CUA_CAC_CHUNG_TU_CHINH_DUA_THEO_REFID_CUA_CHUNG_TU_PHU C
                ON A."ID_CHUNG_TU" = C."ID_CHUNG_TU"
            LEFT JOIN TMP_PARAM D ON C."ID_CHUNG_TU_QUAN_HE" = D."ID_CHUNG_TU"
        WHERE D."ID_CHUNG_TU" IS NULL
    ;


    FOR rec IN
    SELECT
        DISTINCT
          PR."ID_CHUNG_TU"   AS "ID_CHUNG_TU"
        , PR."LOAI_CHUNG_TU" AS "LOAI_CHUNG_TU"
    FROM
        TMP_PARAM PR
    LOOP


        IF rec."LOAI_CHUNG_TU" = ANY ('{1500,1501,1502,1503}' :: INT []) --'BADeposit'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'account.ex.phieu.thu.chi'     AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL                           AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_DOI_TUONG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , COALESCE(D."DIEN_GIAI_DETAIL", M."DIEN_GIAI")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")    AS "TK_NO"
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")    AS "TK_CO"
                    , D."SO_TIEN"
                    , D."SO_TIEN_QUY_DOI"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id") AS "LOAI_TIEN"
                    , M."TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , 0 --"TINH_CHAT"
                    , 0
                    , P."SortOrderMaster"

                FROM account_ex_phieu_thu_chi M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN account_ex_phieu_thu_chi_tiet D ON M."id" = D."PHIEU_THU_CHI_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A ON A."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                      FROM danh_muc_he_thong_tai_khoan T
                                                                                      WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
            ;
        END IF
    ;

        IF rec."LOAI_CHUNG_TU" = ANY
           ('{1560}' :: INT []) --'BAInternalTransfer' --AND @DetailTableName = 'BAInternalTransferDetail'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'account.ex.phieu.thu.chi'     AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL                           AS "HAN_THANH_TOAN"
                    , NULL
                    , NULL
                    , NULL
                    , COALESCE(D."DIEN_GIAI_DETAIL", M."DIEN_GIAI")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")    AS "TK_NO"
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")    AS "TK_CO"
                    , D."SO_TIEN"
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                                 AND ((SELECT T."SO_TAI_KHOAN"
                                       FROM danh_muc_he_thong_tai_khoan T
                                       WHERE T.id = D."TK_CO_ID") LIKE N'111%%'
                                      OR (SELECT T."SO_TAI_KHOAN"
                                          FROM danh_muc_he_thong_tai_khoan T
                                          WHERE T.id = D."TK_CO_ID") LIKE N'112%%'
                                 )
                    THEN (CASE WHEN D."QUY_DOI_THEO_TGXQ" <> 0
                        THEN D."QUY_DOI_THEO_TGXQ"

                          ELSE D."SO_TIEN_QUY_DOI"
                          END)
                       ELSE D."SO_TIEN_QUY_DOI"
                       END)                          AS "THANH_TIEN_QUY_DOI"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id") AS "LOAI_TIEN"
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                       ELSE M."TY_GIA"
                       END)                          AS "TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , 0 --"TINH_CHAT"
                    , 0
                    , P."SortOrderMaster"


                FROM account_ex_phieu_thu_chi M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN account_ex_phieu_thu_chi_tiet D ON M."id" = D."PHIEU_THU_CHI_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'account.ex.phieu.thu.chi.tiet'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU"
                                 AND M."currency_id" <> LOAI_TIEN_CHINH
                                 AND M."LOAI_CHUNG_TU" = 1560
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A ON A."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                      FROM danh_muc_he_thong_tai_khoan T
                                                                                      WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;

        IF rec."LOAI_CHUNG_TU" = ANY
           ('{1510,1511,1512,1513,1514,1520,1521,1522,1523,1530,1531}' :: INT [])-- 'BAWithDraw' --AND @DetailTableName = 'BAWithdrawDetail'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'account.ex.phieu.thu.chi'     AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL                           AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_DOI_TUONG", '')
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (1520, 1521)
                    THEN AO."DIA_CHI"
                      ELSE --CÁc chứng từ ...séc tiền mặt thì lấy thông tin địa chỉ trên danh mục
                          COALESCE(M."DIA_CHI",
                                   '')
                      END
                    , COALESCE(D."DIEN_GIAI_DETAIL", M."DIEN_GIAI")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")    AS "TK_NO"
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")    AS "TK_CO"
                    , D."SO_TIEN"
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                                 AND ((SELECT T."SO_TAI_KHOAN"
                                       FROM danh_muc_he_thong_tai_khoan T
                                       WHERE T.id = D."TK_CO_ID") LIKE N'111%%'
                                      OR (SELECT T."SO_TAI_KHOAN"
                                          FROM danh_muc_he_thong_tai_khoan T
                                          WHERE T.id = D."TK_CO_ID") LIKE N'112%%'
                                 )
                    THEN (CASE WHEN D."QUY_DOI_THEO_TGXQ" <> 0
                        THEN D."QUY_DOI_THEO_TGXQ"

                          ELSE D."SO_TIEN_QUY_DOI"
                          END)
                       ELSE D."SO_TIEN_QUY_DOI"
                       END)                          AS "THANH_TIEN_QUY_DOI"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id") AS "LOAI_TIEN"
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                       ELSE M."TY_GIA"
                       END)                          AS "TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , 0 --"TINH_CHAT"
                    , 0
                    , P."SortOrderMaster"


                FROM account_ex_phieu_thu_chi M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN account_ex_phieu_thu_chi_tiet D ON M."id" = D."PHIEU_THU_CHI_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN res_partner AO ON AO."id" = M."DOI_TUONG_ID"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'account.ex.phieu.thu.chi.tiet'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU"
                                 AND M."currency_id" <> LOAI_TIEN_CHINH
                                 AND M."LOAI_CHUNG_TU" IN (1510, 1511,
                                                           1520, 1521, 1530,
                                                           1531)
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A ON A."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                      FROM danh_muc_he_thong_tai_khoan T
                                                                                      WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;

        IF rec."LOAI_CHUNG_TU" = ANY
           ('{1020,1021,1022,1023,1024,1025,1026}' :: INT []) -- 'CAPayment' --AND @DetailTableName = 'CAPaymentDetail'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'account.ex.phieu.thu.chi'     AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL                           AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_DOI_TUONG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , COALESCE(D."DIEN_GIAI_DETAIL", M."DIEN_GIAI")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")    AS "TK_NO"
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")    AS "TK_CO"
                    , D."SO_TIEN"
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                                 AND ((SELECT T."SO_TAI_KHOAN"
                                       FROM danh_muc_he_thong_tai_khoan T
                                       WHERE T.id = D."TK_CO_ID") LIKE N'111%%'
                                      OR (SELECT T."SO_TAI_KHOAN"
                                          FROM danh_muc_he_thong_tai_khoan T
                                          WHERE T.id = D."TK_CO_ID") LIKE N'112%%'
                                 )
                    THEN (CASE WHEN D."QUY_DOI_THEO_TGXQ" <> 0
                        THEN D."QUY_DOI_THEO_TGXQ"

                          ELSE D."SO_TIEN_QUY_DOI"
                          END)
                       ELSE D."SO_TIEN_QUY_DOI"
                       END)                          AS "THANH_TIEN_QUY_DOI"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id") AS "LOAI_TIEN"
                    , --M."TY_GIA" ,
                      (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                          THEN EX."FIRST_TY_GIA_XUAT_QUY"
                       ELSE M."TY_GIA"
                       END)                          AS "TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , 0 --"TINH_CHAT"
                    , 0
                    , P."SortOrderMaster"


                FROM account_ex_phieu_thu_chi M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN account_ex_phieu_thu_chi_tiet D ON M."id" = D."PHIEU_THU_CHI_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'account.ex.phieu.thu.chi.tiet'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU"
                                 AND M."currency_id" <> LOAI_TIEN_CHINH
                                 AND M."LOAI_CHUNG_TU" IN (1020, 1021)
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A ON A."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                      FROM danh_muc_he_thong_tai_khoan T
                                                                                      WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;

        --
        IF rec."LOAI_CHUNG_TU" = ANY
           ('{1010,1011,1012,1013}' :: INT []) -- 'CAReceipt' --AND @DetailTableName = 'CAReceiptDetail'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'account.ex.phieu.thu.chi'     AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL                           AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_DOI_TUONG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , COALESCE(D."DIEN_GIAI_DETAIL", M."DIEN_GIAI")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")    AS "TK_NO"
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")    AS "TK_CO"
                    , D."SO_TIEN"
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                                 AND ((SELECT T."SO_TAI_KHOAN"
                                       FROM danh_muc_he_thong_tai_khoan T
                                       WHERE T.id = D."TK_CO_ID") LIKE N'111%%'
                                      OR (SELECT T."SO_TAI_KHOAN"
                                          FROM danh_muc_he_thong_tai_khoan T
                                          WHERE T.id = D."TK_CO_ID") LIKE N'112%%'
                                 )
                    THEN (CASE WHEN D."QUY_DOI_THEO_TGXQ" <> 0
                        THEN D."QUY_DOI_THEO_TGXQ"

                          ELSE D."SO_TIEN_QUY_DOI"
                          END)
                       ELSE D."SO_TIEN_QUY_DOI"
                       END)                          AS "THANH_TIEN_QUY_DOI"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id") AS "LOAI_TIEN"
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                       ELSE M."TY_GIA"
                       END)                          AS "TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , 0 --"TINH_CHAT"
                    , 0
                    , P."SortOrderMaster"


                FROM account_ex_phieu_thu_chi M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN account_ex_phieu_thu_chi_tiet D ON M."id" = D."PHIEU_THU_CHI_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'account.ex.phieu.thu.chi.tiet'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU"
                                 AND M."currency_id" <> LOAI_TIEN_CHINH
                                 AND M."LOAI_CHUNG_TU" = 1010
                                 AND M."LY_DO_NOP" = '10'
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A ON A."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                      FROM danh_muc_he_thong_tai_khoan T
                                                                                      WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;

        --
        IF rec."LOAI_CHUNG_TU" = ANY
           ('{252}' :: INT []) -- 'FAAdjustment' --AND @DetailTableName = 'FAAdjustmentDetail'
        THEN
            INSERT INTO TMP_KET_QUA

                SELECT
                    M."id"
                    , 'asset.danh.gia.lai'           AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL                           AS "HAN_THANH_TOAN"
                    , A."id"                         AS "DOI_TUONG_ID"
                    , A."HO_VA_TEN"
                    , A."DIA_CHI"
                    , D."DIEN_GIAI"
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")    AS "TK_NO"
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")    AS "TK_CO"
                    , D."SO_TIEN"
                    , D."SO_TIEN"
                    , 0
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = LOAI_TIEN_CHINH) AS "LOAI_TIEN"
                    , 1
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."KET_LUAN"
                    , 0 --"TINH_CHAT"
                    , 0
                    , P."SortOrderMaster"


                FROM asset_danh_gia_lai M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    LEFT JOIN asset_danh_gia_lai_hach_toan D ON M."id" = D."DANH_GIA_LAI_TAI_SAN_CO_DINH_ID"
                    LEFT JOIN res_partner A ON D."DOI_TUONG_ID" = A."id"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;

        IF rec."LOAI_CHUNG_TU" = ANY
           ('{251}' :: INT []) -- 'FAAdjustment' --AND @DetailTableName = 'FAAdjustmentDetail'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'asset.ghi.giam'                        AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL                                    AS "HAN_THANH_TOAN"
                    , A."id"                                  AS "DOI_TUONG_ID"
                    , A."HO_VA_TEN"
                    , A."DIA_CHI"
                    , COALESCE(D."DIEN_GIAI", M."LY_DO_GIAM") AS "DIEN_GIAI"
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")             AS "TK_NO"
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")             AS "TK_CO"
                    , D."SO_TIEN"
                    , D."SO_TIEN"
                    , '0'
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = LOAI_TIEN_CHINH)          AS "LOAI_TIEN"
                    , 1
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."LY_DO_GIAM"
                    , 0 --"TINH_CHAT"
                    , 0
                    , P."SortOrderMaster"


                FROM asset_ghi_giam M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"

                    LEFT JOIN asset_ghi_giam_hach_toan D ON M."id" = D."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                    LEFT JOIN res_partner A ON D."DOI_TUONG_ID" = A."id"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;


        --                 IF rec."LOAI_CHUNG_TU" = 'FAChangeFinancialLeasingToOwner' --AND @DetailTableName = 'FAChangeFinancialLeasingToOwnerDetail'
        --                     THEN
        --                         INSERT  INTO TMP_KET_QUA
        --                                 SELECT
        --                                         M."ID_CHUNG_TU" ,
        --                                         M."LOAI_CHUNG_TU" ,
        --                                         M."SO_CHUNG_TU" ,
        --                                         M."NGAY_CHUNG_TU" ,
        --                                         M."NGAY_HACH_TOAN" ,
        --                                         NULL AS "HAN_THANH_TOAN" ,
        --                                         NULL ,
        --                                         NULL ,
        --                                         NULL ,
        --                                         D."DIEN_GIAI" ,
        --                                         D."TK_NO" ,
        --                                         D."TK_CO" ,
        --                                         D."SO_TIEN" ,
        --                                         D."SO_TIEN" ,
        --                                         0 ,
        --                                         LOAI_TIEN_CHINH ,
        --                                         1 ,
        --                                        D."THU_TU_SAP_XEP_CHI_TIET" ,
        --
        --                                         M."DIEN_GIAI" ,
        --                                         0 --"TINH_CHAT"
        --
        --                                 FROM    FAChangeFinancialLeasingToOwner M
        --                                         INNER JOIN TMP_PARAM P ON M."ID_CHUNG_TU" = P."ID_CHUNG_TU"
        --                                         INNER JOIN FAChangeFinancialLeasingToOwnerDetail D ON M."ID_CHUNG_TU" = D."ID_CHUNG_TU"
        --                                         LEFT JOIN danh_muc_he_thong_tai_khoan AS A ON A."SO_TAI_KHOAN" = D."TK_CO"
        --                                         LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = D."TK_NO"
        --                     END IF ;

        IF rec."LOAI_CHUNG_TU" = ANY
           ('{254}' :: INT []) --  'FADepreciation' --AND @DetailTableName = 'FADepreciationDetail'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'asset.tinh.khau.hao'          AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL                           AS "HAN_THANH_TOAN"
                    , A."id"
                    , A."HO_VA_TEN"
                    , A."DIA_CHI"
                    , D."DIEN_GIAI"
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")    AS "TK_NO"
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")    AS "TK_CO"
                    , D."SO_TIEN"
                    , --SUM(D."SO_TIEN") ,
                    D."SO_TIEN"
                    , --SUM(D."SO_TIEN") ,
                    '0'
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = LOAI_TIEN_CHINH) AS "LOAI_TIEN"
                    , 1
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , --MIN(D."STT") ,


                    M."DIEN_GIAI"
                    , 0 --"TINH_CHAT"
                    , 0
                    , P."SortOrderMaster"


                FROM asset_tinh_khau_hao M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN asset_tinh_khau_hao_hach_toan D ON M."id" = D."TINH_KHAU_HAO_ID"
                    LEFT JOIN res_partner A ON COALESCE(D."DOI_TUONG_NO_ID",
                                                        D."DOI_TUONG_CO_ID") = A."id"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"

            ;
        END IF
    ;

        IF rec."LOAI_CHUNG_TU" =
        ANY
           ('{4010,4011,4012,4013,4014,4015,4016,4017,4018,4020,4030}' :: INT [])-- 'GLVoucher' --AND @DetailTableName = 'account_ex_chung_tu_nghiep_vu_khacDetail'
        THEN


            DROP TABLE IF EXISTS TMP_DOI_TUONG_GL
            ;

            CREATE TEMP TABLE TMP_DOI_TUONG_GL
                AS

                    SELECT
                        T."ID_CHUNG_TU"
                        , T."DOI_TUONG_ID"
                        , A."HO_VA_TEN" AS "TEN_KHACH_HANG"
                        , A."DIA_CHI"
                    FROM (
                             SELECT
                                   M."id"                                                       AS "ID_CHUNG_TU"
                                 , COALESCE(M."DOI_TUONG_ID",
                                            COALESCE(D."DOI_TUONG_NO_ID", D."DOI_TUONG_CO_ID")) AS "DOI_TUONG_ID"
                                 , ROW_NUMBER()
                                   OVER (
                                       PARTITION BY M."id"
                                       ORDER BY D."THU_TU_SAP_XEP_CHI_TIET" )                   AS "RowNumber"
                             FROM account_ex_chung_tu_nghiep_vu_khac M
                                 INNER JOIN account_ex_chung_tu_nghiep_vu_khac_hach_toan D
                                     ON D."CHUNG_TU_NGHIEP_VU_KHAC_ID" = M."id"
                                 INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                             WHERE M."DOI_TUONG_ID" IS NOT NULL OR D."DOI_TUONG_NO_ID" IS NOT NULL OR
                                   D."DOI_TUONG_CO_ID" IS NOT NULL
                         ) T
                        INNER JOIN res_partner A ON T."DOI_TUONG_ID" = A."id"
                    WHERE T."RowNumber" = 1
            ;

            INSERT INTO TMP_KET_QUA
                SELECT
                      M."id"                               AS "ID_CHUNG_TU"
                    , 'account.ex.chung.tu.nghiep.vu.khac' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , M."HAN_THANH_TOAN"
                    , T."DOI_TUONG_ID"
                    , T."TEN_KHACH_HANG"
                    , T."DIA_CHI"
                    , COALESCE(D."DIEN_GIAI", M."DIEN_GIAI")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")          AS "TK_NO"
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")          AS "TK_CO"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (4013, 4016,
                                                      4017) -- Các CT xử lý chênh lệch tỷ giá
                    THEN (D."SO_TIEN_QUY_DOI"
                          + (CASE
                             WHEN D."TK_THUE_GTGT_ID" IS NULL
                                  OR PHUONG_PHAP_TINH_THUE = 'PHUONG_PHAP_TRUC_TIEP_TREN_DOANH_THU'
                                 THEN D."TIEN_THUE_GTGT_QD"
                             ELSE 0
                             END))
                      ELSE (D."SO_TIEN"
                            + (CASE WHEN D."TK_THUE_GTGT_ID" IS NULL
                                         OR PHUONG_PHAP_TINH_THUE = 'PHUONG_PHAP_TRUC_TIEP_TREN_DOANH_THU'
                          THEN D."TIEN_THUE_GTGT"
                               ELSE 0
                               END))
                      END                                  AS "THANH_TIEN"
                    , (--D."SO_TIEN"
                          CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                    AND EX."ID_CHUNG_TU" IS NOT NULL
                                    AND ((SELECT T."SO_TAI_KHOAN"
                                          FROM danh_muc_he_thong_tai_khoan T
                                          WHERE T.id = D."TK_CO_ID") LIKE N'111%%'
                                         OR (SELECT T."SO_TAI_KHOAN"
                                             FROM danh_muc_he_thong_tai_khoan T
                                             WHERE T.id = D."TK_CO_ID") LIKE N'112%%'
                                    )
                              THEN (CASE WHEN
                                  D."THANH_TIEN_THEO_TY_GIA_XUAT_QUY" <> 0
                                  THEN D."THANH_TIEN_THEO_TY_GIA_XUAT_QUY"

                                    ELSE D."SO_TIEN_QUY_DOI"
                                    END)
                          ELSE D."SO_TIEN_QUY_DOI"
                          END
                          + CASE WHEN D."TK_THUE_GTGT_ID" IS NULL
                                      OR PHUONG_PHAP_TINH_THUE = TRUE
                              THEN D."TIEN_THUE_GTGT_QD"
                            ELSE 0
                            END)                           AS "THANH_TIEN_QUY_DOI"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (4013, 4016,
                                                       4017)
                    THEN'0'
                       ELSE CCY."PHEP_TINH_QUY_DOI"
                       END)                                AS "PHEP_TINH_CHUYEN_DOI"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (4013, 4016,
                                                       4017)
                    THEN (SELECT "MA_LOAI_TIEN"
                          FROM res_currency T
                          WHERE T.id = LOAI_TIEN_CHINH)
                       ELSE (SELECT T."MA_LOAI_TIEN"
                             FROM res_currency T
                             WHERE T.id = M."currency_id")
                       END)                                AS "LOAI_TIEN"
                    , (CASE WHEN M."LOAI_CHUNG_TU" IN (4013, 4016,
                                                       4017)
                    THEN 1
                       ELSE --M."TY_GIA"
                           (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                      AND EX."ID_CHUNG_TU" IS NOT NULL
                               THEN EX."FIRST_TY_GIA_XUAT_QUY"
                            ELSE M."TY_GIA"
                            END)
                       END)                                AS "TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"

                    , M."DIEN_GIAI"
                    , 0 --"TINH_CHAT"
                    , 0
                    , P."SortOrderMaster"


                FROM account_ex_chung_tu_nghiep_vu_khac M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN account_ex_chung_tu_nghiep_vu_khac_hach_toan D
                        ON M."id" = D."CHUNG_TU_NGHIEP_VU_KHAC_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'account.ex.chung.tu.nghiep.vu.khac.hach.toan'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU" AND M."currency_id" <> LOAI_TIEN_CHINH AND
                                 M."LOAI_CHUNG_TU" = 4010
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                    LEFT JOIN TMP_DOI_TUONG_GL T ON M."id" = T."ID_CHUNG_TU"
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;

            IF PHUONG_PHAP_TINH_THUE = 'PHUONG_PHAP_KHAU_TRU'
            THEN
                INSERT INTO TMP_KET_QUA
                    SELECT
                        M."id"
                        , 'account.ex.chung.tu.nghiep.vu.khac' AS "MODEL_CHUNG_TU"
                        , M."LOAI_CHUNG_TU"
                        , M."SO_CHUNG_TU"
                        , M."NGAY_CHUNG_TU"
                        , M."NGAY_HACH_TOAN"
                        , M."HAN_THANH_TOAN"
                        , T."DOI_TUONG_ID"
                        , T."TEN_KHACH_HANG"
                        , T."DIA_CHI"
                        , N'Thuế GTGT'
                        , (SELECT T."SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan T
                           WHERE T.id = D."TK_THUE_GTGT_ID")   AS "TK_NO"
                        , (SELECT T."SO_TAI_KHOAN"
                           FROM danh_muc_he_thong_tai_khoan T
                           WHERE T.id = D."TK_CO_ID")          AS "TK_CO"
                        , -- sửa bug 52280
                          (CASE WHEN M."LOAI_CHUNG_TU" IN (4013,
                                                           4016, 4017)
                              THEN D."TIEN_THUE_GTGT_QD"
                           ELSE D."TIEN_THUE_GTGT"
                           END)                                AS "THANH_TIEN"
                        , D."TIEN_THUE_GTGT_QD"                AS "SO_TIEN"
                        , (CASE WHEN M."LOAI_CHUNG_TU" IN (4013,
                                                           4016, 4017)
                        THEN'0'
                           ELSE CCY."PHEP_TINH_QUY_DOI"
                           END)                                AS "PHEP_TINH_CHUYEN_DOI"
                        , (CASE WHEN M."LOAI_CHUNG_TU" IN (4013,
                                                           4016, 4017)
                        THEN (SELECT "MA_LOAI_TIEN"
                              FROM res_currency T
                              WHERE T.id = LOAI_TIEN_CHINH)
                           ELSE (SELECT T."MA_LOAI_TIEN"
                                 FROM res_currency T
                                 WHERE T.id = M."currency_id")
                           END)                                AS "LOAI_TIEN"
                        , (CASE WHEN M."LOAI_CHUNG_TU" IN (4013,
                                                           4016, 4017)
                        THEN 1
                           ELSE M."TY_GIA"
                           END)                                AS "TY_GIA"
                        , D."THU_TU_SAP_XEP_CHI_TIET"


                        , M."DIEN_GIAI"
                        , 0 --"TINH_CHAT"
                        , 1
                        , P."SortOrderMaster"


                    FROM account_ex_chung_tu_nghiep_vu_khac M
                        INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                        INNER JOIN account_ex_chung_tu_nghiep_vu_khac_hach_toan D
                            ON M."id" = D."CHUNG_TU_NGHIEP_VU_KHAC_ID"
                        LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                        LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                            FROM
                                                                                                danh_muc_he_thong_tai_khoan T
                                                                                            WHERE T.id = D."TK_CO_ID")
                        LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                            FROM
                                                                                                danh_muc_he_thong_tai_khoan T
                                                                                            WHERE T.id =
                                                                                                  D."TK_THUE_GTGT_ID")
                        LEFT JOIN TMP_DOI_TUONG_GL T ON M."id" = T."ID_CHUNG_TU"
                    WHERE D."TIEN_THUE_GTGT_QD" <> 0
                          AND D."TK_THUE_GTGT_ID" IS NOT NULL
                          AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                          P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                ;

                -- Nếu ko nhập tài khoản thuế thì chỉ hiển thị 1 dòng
            END IF
            ;
        END IF
    ;


        IF rec."LOAI_CHUNG_TU" = ANY
           ('{2010,2011,2012,2013,2014,2015,2016,2017}' :: INT [])--'INInward' --AND @DetailTableName = 'IN"NHAP_KHO"Detail'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'stock.ex.nhap.xuat.kho' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL                     AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_NGUOI_GIAO_HANG", '')
                    , NULL
                    , CASE WHEN M."KIEM_TRA_PHIEU_NHAP_KHO" = TRUE
                    THEN N'Giá vốn hàng bán'
                      ELSE COALESCE(D."TEN_HANG",
                                    M."DIEN_GIAI")
                      END
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , D."TIEN_VON_QUY_DOI"     AS "THANH_TIEN"
                    , D."TIEN_VON_QUY_DOI"     AS "SO_TIEN"
                    , '0'
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = LOAI_TIEN_CHINH)
                    , 1
                    , D."THU_TU_SAP_XEP_CHI_TIET"

                    , M."DIEN_GIAI"
                    , 0 --"TINH_CHAT"
                    , CASE WHEN M."KIEM_TRA_PHIEU_NHAP_KHO" = TRUE
                    THEN 6
                      ELSE 0
                      END
                    , P."SortOrderMaster"


                FROM stock_ex_nhap_xuat_kho M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet D ON M."id" = D."NHAP_XUAT_ID"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;


        IF rec."LOAI_CHUNG_TU" = ANY
           ('{2020,2021,2022,2023,2024,2025,2026,2027}' :: INT [])--'INInward' --AND @DetailTableName = 'IN"XUAT_KHO"Detail'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'stock.ex.nhap.xuat.kho' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL                     AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_NGUOI_GIAO_HANG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , CASE WHEN M."KIEM_PHIEU_NHAP_XUAT_KHO" = TRUE
                    THEN N'Giá vốn hàng bán'
                      ELSE COALESCE(D."TEN_HANG",
                                    M."DIEN_GIAI")
                      END

                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , D."TIEN_VON"             AS "THANH_TIEN"
                    , D."TIEN_VON"             AS "SO_TIEN"
                    , '0'
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = LOAI_TIEN_CHINH)
                    , 1
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , 0 --"TINH_CHAT"
                    , CASE WHEN M."KIEM_PHIEU_NHAP_XUAT_KHO" = TRUE
                    THEN 6
                      ELSE 0
                      END
                    , P."SortOrderMaster"

                FROM stock_ex_nhap_xuat_kho M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet D ON M."id" = D."NHAP_XUAT_ID"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"

            ;
        END IF
    ;


        IF rec."LOAI_CHUNG_TU" = ANY
           ('{2030,2031,2032,9131}' :: INT [])-- 'INTransfer' --AND @DetailTableName = 'INTransferDetail'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'stock.ex.nhap.xuat.kho' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL                     AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , NULL
                    , NULL
                    , COALESCE(D."TEN_HANG", M."DIEN_GIAI")

                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , D."TIEN_VON"             AS "THANH_TIEN"
                    , D."TIEN_VON"             AS "SO_TIEN"
                    , '0'
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = LOAI_TIEN_CHINH)
                    , 1
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , 0 --"TINH_CHAT"
                    , 0
                    , P."SortOrderMaster"

                FROM stock_ex_nhap_xuat_kho M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet D ON M."id" = D."NHAP_XUAT_ID"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;


        IF rec."LOAI_CHUNG_TU" = ANY
           ('{4090,4091,4092}' :: INT [])-- 'JCAccepted' --AND @DetailTableName = 'JCAcceptedDetail'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"

                    , 'gia.thanh.nghiem.thu' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL                   AS "HAN_THANH_TOAN"
                    , NULL
                    , NULL
                    , NULL
                    , COALESCE(D."DIEN_GIAI", M."DIEN_GIAI")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , D."GIA_TRI_NGHIEM_THU"
                    , D."GIA_TRI_NGHIEM_THU"
                    , '0'
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = LOAI_TIEN_CHINH)
                    , 1
                    , D."STT"
                    , M."DIEN_GIAI"
                    , 0 --"TINH_CHAT"
                    , 0
                    , P."SortOrderMaster"


                FROM gia_thanh_nghiem_thu M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN gia_thanh_nghiem_thu_hach_toan D ON M."id" = D."CHI_TIET_ID"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;


        IF rec."LOAI_CHUNG_TU" = ANY
           ('{4080,4081,4082,4083}' :: INT [])--  'JCExpenseTranfer' --AND @DetailTableName = 'JCExpenseTranferDetail'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'gia.thanh.ket.chuyen.chi.phi' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , "SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL                           AS "HAN_THANH_TOAN"
                    , NULL
                    , NULL
                    , NULL
                    , COALESCE(D."DIEN_GIAI", M."DIEN_GIAI")

                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , D."SO_TIEN"
                    , D."SO_TIEN"
                    , '0'
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = LOAI_TIEN_CHINH)
                    , 1
                    , D."STT"
                    , M."DIEN_GIAI"
                    , 0 --"TINH_CHAT"
                    , 0
                    , P."SortOrderMaster"

                FROM gia_thanh_ket_chuyen_chi_phi M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN gia_thanh_ket_chuyen_chi_phi_hach_toan D ON M."id" = D."CHI_TIET_ID"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;

        IF rec."LOAI_CHUNG_TU" = ANY
           ('{6030}' :: INT [])--  'PASalaryExpense' --AND @DetailTableName = 'PASalaryExpenseDetail'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'tien.luong.hach.toan.chi.phi.luong' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL                                 AS "HAN_THANH_TOAN"
                    , NULL
                    , NULL
                    , NULL
                    , COALESCE(D."DIEN_GIAI", M."DIEN_GIAI")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , D."SO_TIEN"
                    , D."SO_TIEN"
                    , '0'
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = LOAI_TIEN_CHINH)
                    , 1
                    , D."STT"
                    , M."DIEN_GIAI"
                    , 0 --"TINH_CHAT"
                    , 0
                    , P."SortOrderMaster"

                FROM tien_luong_hach_toan_chi_phi_luong M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN tien_luong_hach_toan_chi_phi_luong_chi_tiet D ON M."id" = D."CHI_TIET_ID"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;

        IF rec."LOAI_CHUNG_TU" = ANY
           ('{3040,3041,3042,3043}' :: INT [])--  'PUDiscount' --AND @DetailTableName = 'purchase_ex_giam_gia_hang_mua_chi_tiet'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'purchase.ex.giam.gia.hang.mua' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL :: TIMESTAMP               AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_NHA_CUNG_CAP", '')
                    , NULL
                    , COALESCE(D."TEN_HANG", M."DIEN_GIAI")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , D."THANH_TIEN"
                      + (CASE WHEN D."TK_THUE_GTGT_ID" IS NULL
                                   OR PHUONG_PHAP_TINH_THUE = 'PHUONG_PHAP_TRUC_TIEP_TREN_DOANH_THU'
                    THEN D."TIEN_THUE_GTGT"
                         ELSE 0
                         END)                         AS "THANH_TIEN"
                    , D."THANH_TIEN_QUY_DOI"
                      + (CASE WHEN D."TK_THUE_GTGT_ID" IS NULL
                                   OR PHUONG_PHAP_TINH_THUE = 'PHUONG_PHAP_TRUC_TIEP_TREN_DOANH_THU'
                    THEN D."TIEN_THUE_GTGT_QUY_DOI"
                         ELSE 0
                         END)                         AS "SO_TIEN"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id")  AS "LOAI_TIEN"
                    , M."TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , CAST(COALESCE(II."TINH_CHAT", '0') AS INT)
                    , 0
                    , P."SortOrderMaster"

                FROM purchase_ex_giam_gia_hang_mua M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN purchase_ex_giam_gia_hang_mua_chi_tiet D ON M."id" = D."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN danh_muc_vat_tu_hang_hoa II ON II."id" = D."MA_HANG_ID"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                UNION ALL
                SELECT
                    M."id"
                    , 'purchase.ex.giam.gia.hang.mua' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL :: TIMESTAMP               AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_NHA_CUNG_CAP", '')
                    , NULL
                    , N'Thuế GTGT được khấu trừ của hàng hóa, dịch vụ'
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_THUE_GTGT_ID")


                    , D."TIEN_THUE_GTGT"
                    , D."TIEN_THUE_GTGT_QUY_DOI"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id")  AS "LOAI_TIEN"
                    , M."TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , CAST(COALESCE(II."TINH_CHAT", '0') AS INT)
                    , 1
                    , P."SortOrderMaster"

                FROM purchase_ex_giam_gia_hang_mua M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN purchase_ex_giam_gia_hang_mua_chi_tiet D ON M."id" = D."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN danh_muc_vat_tu_hang_hoa II ON II."id" = D."MA_HANG_ID"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE
                                                                                            T.id = D."TK_THUE_GTGT_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE D."TIEN_THUE_GTGT_QUY_DOI" <> 0
                      AND PHUONG_PHAP_TINH_THUE = 'PHUONG_PHAP_KHAU_TRU'
                      AND D."TK_THUE_GTGT_ID" IS NOT NULL
                      AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"

            ;
        END IF
    ;

        -- nmtruong sửa ngày 13/3/2015: lấy "THUE_GTGT" thay cho turnOver"SO_TIEN"
        IF rec."LOAI_CHUNG_TU" = ANY
           ('{3400,3402,3403}' :: INT [])--   'PUInvoice' --AND @DetailTableName = 'PUInvoiceDetail'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'purchase.ex.hoa.don.mua.hang' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , M."HAN_THANH_TOAN"             AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_NHA_CUNG_CAP", '')
                    , COALESCE(M."DIA_CHI", '')
                    , COALESCE(D."TEN_HANG", M."DIEN_GIAI")

                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_THUE_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , D."TIEN_THUE_GTGT"
                    , D."TIEN_THUE_GTGT_QUY_DOI"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id") AS "LOAI_TIEN"
                    , M."TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , CAST(COALESCE(II."TINH_CHAT", '0') AS INT)
                    , 0
                    , P."SortOrderMaster"

                FROM purchase_ex_hoa_don_mua_hang M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN purchase_ex_hoa_don_mua_hang_chi_tiet D ON M."id" = D."HOA_DON_MUA_HANG_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN danh_muc_vat_tu_hang_hoa II ON II."id" = D."MA_HANG_ID"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_THUE_ID")

                WHERE M."NHAN_HOA_DON" = FALSE AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                UNION ALL
                SELECT
                    M."id"
                    , 'purchase.ex.hoa.don.mua.hang' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , M."HAN_THANH_TOAN"             AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_NHA_CUNG_CAP", '')
                    , COALESCE(M."DIA_CHI", '')
                    , COALESCE(D."name", M."DIEN_GIAI")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , D."THANH_TIEN"
                    , D."THANH_TIEN_QUY_DOI"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id") AS "LOAI_TIEN"
                    , M."TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , CAST(COALESCE(II."TINH_CHAT", '0') AS INT)
                    , 0
                    , P."SortOrderMaster"

                FROM purchase_ex_hoa_don_mua_hang M

                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN purchase_document_line D ON M."id" = D."HOA_DON_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN danh_muc_vat_tu_hang_hoa II ON II."id" = D."MA_HANG_ID"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE M."NHAN_HOA_DON" = FALSE AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;


        IF rec."LOAI_CHUNG_TU" = ANY
           ('{3030,3031,3032,3033}' :: INT [])-- 'PUReturn' --AND @DetailTableName = 'purchase_ex_tra_lai_hang_mua_chi_tiet'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'purchase.ex.tra.lai.hang.mua' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL :: TIMESTAMP              AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_NHA_CUNG_CAP", '')
                    , NULL
                    , COALESCE(D."TEN_HANG", M."DIEN_GIAI")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , D."THANH_TIEN"
                    , D."THANH_TIEN_QUY_DOI"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id") AS "LOAI_TIEN"
                    , M."TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3031, 3033)
                    THEN M."LY_DO_NOP"
                      ELSE M."DIEN_GIAI"
                      END
                    , CAST(COALESCE(II."TINH_CHAT", '0') AS INT)
                    , 0
                    , P."SortOrderMaster"


                FROM purchase_ex_tra_lai_hang_mua M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN purchase_ex_tra_lai_hang_mua_chi_tiet D ON M."id" = D."CHUNG_TU_TRA_LAI_HANG_MUA_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN danh_muc_vat_tu_hang_hoa II ON II."id" = D."MA_HANG_ID"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"

                UNION ALL
                SELECT
                    M."id"
                    , 'purchase.ex.tra.lai.hang.mua' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL :: TIMESTAMP              AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_NHA_CUNG_CAP", '')
                    , NULL
                    , N'Thuế GTGT được khấu trừ của hàng hóa, dịch vụ'

                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_THUE_GTGT_ID")

                    , D."TIEN_THUE_GTGT"
                    , D."TIEN_THUE_GTGT_QUY_DOI"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id") AS "LOAI_TIEN"
                    , M."TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3031, 3033)
                    THEN M."LY_DO_NOP"
                      ELSE M."DIEN_GIAI"
                      END
                    , 0 --"TINH_CHAT"
                    , 1
                    , P."SortOrderMaster"

                FROM purchase_ex_tra_lai_hang_mua M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN purchase_ex_tra_lai_hang_mua_chi_tiet D ON M."id" = D."CHUNG_TU_TRA_LAI_HANG_MUA_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE
                                                                                            T.id = D."TK_THUE_GTGT_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE D."TIEN_THUE_GTGT_QUY_DOI" <> 0
                      AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;


        IF rec."LOAI_CHUNG_TU" = ANY
           ('{330,331,332,333,334}' :: INT [])-- 'PUService' --AND @DetailTableName = 'PUServiceDetail'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'purchase.document'            AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , M."HAN_THANH_TOAN"             AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_DOI_TUONG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , COALESCE(D."name", M."DIEN_GIAI_CHUNG")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , (D."THANH_TIEN" - D."TIEN_CHIET_KHAU"
                       + CASE WHEN D."TK_THUE_GTGT_ID" IS NULL
                    THEN D."TIEN_THUE_GTGT"
                         ELSE 0
                         END)                        AS "THANH_TIEN"
                    , (--D."SO_TIEN"
                          (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                     AND EX."ID_CHUNG_TU" IS NOT NULL
                              THEN (CASE WHEN
                                  D."THANH_TIEN_SAU_TY_GIA_XUAT_QUY" <> 0
                                  THEN D."THANH_TIEN_SAU_TY_GIA_XUAT_QUY"

                                    ELSE D."THANH_TIEN_QUY_DOI"
                                         - D."TIEN_CHIET_KHAU_QUY_DOI"
                                    END)
                           ELSE D."THANH_TIEN_QUY_DOI"
                                - D."TIEN_CHIET_KHAU_QUY_DOI"
                           END)
                          /*- D."KHOAN_GIAM_GIA_THANH"*/
                          + CASE WHEN D."TK_THUE_GTGT_ID" IS NULL
                              THEN --D."THUE_GTGT"
                                  (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                             AND EX."ID_CHUNG_TU" IS NOT NULL
                                      THEN (CASE
                                            WHEN
                                                D."TIEN_THUE_GTGT_THEO_TGXQ" <> 0
                                                THEN D."TIEN_THUE_GTGT_THEO_TGXQ"

                                            ELSE D."TIEN_THUE_GTGT_QUY_DOI"
                                            END)
                                   ELSE D."TIEN_THUE_GTGT_QUY_DOI"
                                   END)
                            ELSE 0
                            END)                     AS "SO_TIEN"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id") AS "LOAI_TIEN"
                    , --M."TY_GIA" ,
                      (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                          THEN EX."FIRST_TY_GIA_XUAT_QUY"
                       ELSE M."TY_GIA"
                       END)                          AS "TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI_CHUNG"
                    , CAST(COALESCE(II."TINH_CHAT", '0') AS INT)
                    , 0
                    , P."SortOrderMaster"

                FROM purchase_document M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN purchase_document_line D ON M."id" = D."order_id"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN danh_muc_vat_tu_hang_hoa II ON II."id" = D."MA_HANG_ID"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'purchase.document.line'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU"
                                 AND M."currency_id" <> LOAI_TIEN_CHINH
                                 AND M."LOAI_CHUNG_TU" IN (331, 332,
                                                           333, 334)
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                UNION ALL
                SELECT
                    M."id"
                    , 'purchase.document'            AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , M."HAN_THANH_TOAN"             AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_DOI_TUONG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , N'Thuế GTGT được khấu trừ của hàng hóa, dịch vụ'
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_THUE_GTGT_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")

                    , D."TIEN_THUE_GTGT"
                    , --D."THUE_GTGT" ,
                      (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                          THEN (CASE WHEN
                              D."TIEN_THUE_GTGT_THEO_TGXQ" <> 0
                              THEN D."TIEN_THUE_GTGT_THEO_TGXQ"

                                ELSE D."TIEN_THUE_GTGT_QUY_DOI"
                                END)
                       ELSE D."TIEN_THUE_GTGT_QUY_DOI"
                       END)                          AS "THUE_GTGT"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id") AS "LOAI_TIEN"
                    , --M."TY_GIA" ,
                      (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                          THEN EX."FIRST_TY_GIA_XUAT_QUY"
                       ELSE M."TY_GIA"
                       END)                          AS "TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI_CHUNG"
                    , 0 --"TINH_CHAT"
                    , 1
                    , P."SortOrderMaster"

                FROM purchase_document M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN purchase_document_line D ON M."id" = D."order_id"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'purchase.document.line'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU"
                                 AND M."currency_id" <> LOAI_TIEN_CHINH
                                 AND M."LOAI_CHUNG_TU" IN (331, 332,
                                                           333, 334)
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE
                                                                                            T.id = D."TK_THUE_GTGT_ID")
                WHERE D."TIEN_THUE_GTGT_QUY_DOI" <> 0
                      AND D."TK_THUE_GTGT_ID" IS NOT NULL AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"


            ;
        END IF
    ;


        --HHSon2: Chứng từ mua hàng nhập khẩu thì luôn lấy tiền quy đổi
        IF rec."LOAI_CHUNG_TU" = ANY
           ('{302,307,308,309,310,312,313,314,315,316,318,319,320,321,322,324,325,326,327,328,352,357,358,359,360,362,363,364,365,366,368,369,370,371,372,374,375,376,377,378}' :: INT [])--  'PUVoucher' --AND @DetailTableName = 'PUVoucherDetail'
        THEN


            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'purchase.document' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (313,
                    314, 315, 316,
                    325, 326, 327,
                    328, 363, 364,
                    365, 366, 375,
                                                      376, 377, 378)
                    THEN
                        CASE
                        WHEN M."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
                            THEN M."SO_UY_NHIEM_CHI"
                        WHEN M."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
                            THEN M."SO_SEC_CHUYEN_KHOAN"
                        WHEN M."LOAI_THANH_TOAN" = 'sec_tien_mat'
                            THEN M."SO_SEC_TIEN_MAT"
                        ELSE
                            M."SO_PHIEU_CHI"
                        END
                      ELSE M."SO_CHUNG_TU"
                      END
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , M."HAN_THANH_TOAN"  AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , M."TEN_DOI_TUONG"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (334, 310, 316,
                                                      322, 328, 360,
                                                      366, 372, 378)
                    THEN AO."DIA_CHI"
                      ELSE --CÁc chứng từ ...séc tiền mặt thì lấy thông tin địa chỉ trên danh mục
                          M."DIA_CHI"
                      END
                    , COALESCE(D."name", M."DIEN_GIAI_CHUNG")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , /*Với mua nhập khẩu thì Số tiền luôn lấy từ quy đổi*/
                      CASE WHEN M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324, 325, 326, 327, 328, 368, 369,
                                                      370, 371, 372, 374, 375, 376, 377, 378)
                          THEN
                              (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH AND EX."ID_CHUNG_TU" IS NOT NULL
                                  THEN (CASE WHEN D."THANH_TIEN_SAU_TY_GIA_XUAT_QUY" <> 0
                                      THEN D."THANH_TIEN_SAU_TY_GIA_XUAT_QUY"

                                        ELSE D."THANH_TIEN_QUY_DOI"
                                             - D."TIEN_CHIET_KHAU_QUY_DOI"
                                        END)
                               ELSE D."THANH_TIEN_QUY_DOI" - D."TIEN_CHIET_KHAU_QUY_DOI"
                               END)

                      ELSE (D."THANH_TIEN" - D."TIEN_CHIET_KHAU"
                            + CASE WHEN PHUONG_PHAP_TINH_THUE = 'PHUONG_PHAP_TRUC_TIEP_TREN_DOANH_THU' OR D."TK_THUE_GTGT_ID" IS NULL
                          THEN D."TIEN_THUE_GTGT"
                              ELSE 0
                              END)
                      END                 AS "THANH_TIEN"
                    , CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN (CASE WHEN D."THANH_TIEN_SAU_TY_GIA_XUAT_QUY" <> 0
                        THEN D."THANH_TIEN_SAU_TY_GIA_XUAT_QUY"

                          ELSE
                              (CASE WHEN (M."LOAI_CHUNG_TU" IN (302, 307, 308, 309, 310, 312, 313, 314, 315, 316, 352,
                                                                357,
                                                                358,
                                                                359,
                                                                360,
                                                                362, 363, 364, 365, 366) AND
                                          D."TK_THUE_GTGT_ID" IS NULL)
                                  THEN "THANH_TIEN_QUY_DOI" - "TIEN_CHIET_KHAU_QUY_DOI" + "TIEN_THUE_GTGT_QUY_DOI"
                               ELSE "THANH_TIEN_QUY_DOI" - "TIEN_CHIET_KHAU_QUY_DOI"
                               END)
                          END)
                      ELSE
                          (CASE WHEN (M."LOAI_CHUNG_TU" IN
                                      (302, 307, 308, 309, 310, 312, 313, 314, 315, 316, 352, 357, 358, 359, 360, 362, 363, 364, 365, 366)
                                      AND D."TK_THUE_GTGT_ID" IS NULL)
                              THEN "THANH_TIEN_QUY_DOI" - "TIEN_CHIET_KHAU_QUY_DOI" + "TIEN_THUE_GTGT_QUY_DOI"
                           ELSE "THANH_TIEN_QUY_DOI" - "TIEN_CHIET_KHAU_QUY_DOI"
                           END)
                      END                 AS "SO_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (318, 319, 320,
                                                           321, 322, 324,
                                                           325, 326, 327,
                                                           328, 368, 369,
                                                      370, 371, 372,
                                                      374, 375, 376,
                                                      377, 378)
                    THEN'0'
                      ELSE CCY."PHEP_TINH_QUY_DOI"
                      END                 AS "PHEP_TINH_CHUYEN_DOI"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (318, 319, 320,
                                                           321, 322, 324,
                                                           325, 326, 327,
                                                           328, 368, 369,
                                                      370, 371, 372,
                                                      374, 375, 376,
                                                      377, 378)
                    THEN (SELECT "MA_LOAI_TIEN"
                          FROM res_currency T
                          WHERE T.id = LOAI_TIEN_CHINH)
                      ELSE (SELECT T."MA_LOAI_TIEN"
                            FROM res_currency T
                            WHERE T.id = M."currency_id")
                      END                 AS "LOAI_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (318, 319, 320,
                                                           321, 322, 324,
                                                           325, 326, 327,
                                                           328, 368, 369,
                                                      370, 371, 372,
                                                      374, 375, 376,
                                                      377, 378)
                    THEN 1
                      ELSE --M."TY_GIA"
                          (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                     AND EX."ID_CHUNG_TU" IS NOT NULL
                              THEN EX."FIRST_TY_GIA_XUAT_QUY"
                           ELSE M."TY_GIA"
                           END)
                      END                 AS "TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"

                    , CASE WHEN M."LOAI_CHUNG_TU" IN (313, 314, 315,
                                                           316, 325, 326,
                                                           327, 328, 363,
                                                           364, 365, 366,
                                                      375, 376, 377,
                                                      378)
                    THEN M."LY_DO_CHI"
                      ELSE M."DIEN_GIAI_CHUNG"
                      END
                    , CAST(COALESCE(II."TINH_CHAT", '0') AS INT)
                    , 0
                    , P."SortOrderMaster"

                FROM purchase_document M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN purchase_document_line D ON M."id" = D."order_id"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN res_partner AO ON AO."id" = M."DOI_TUONG_ID"
                    LEFT JOIN danh_muc_vat_tu_hang_hoa II ON II."id" = D."MA_HANG_ID"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'purchase.document.line'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU"
                                 AND M."currency_id" <> LOAI_TIEN_CHINH
                                 AND M."LOAI_CHUNG_TU" IN (307, 308,
                                                                309, 310, 313,
                                                                314, 315, 316,
                                                                357, 358, 359,
                        360, 363, 364,
                        365, 366, 319,
                        320, 321, 322,
                        325, 326, 327,
                             328, 369, 370,
                             371, 372, 375,
                             376, 377, 378)
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                UNION ALL
                --Các loại thuế nhập khẩu, tiêu thụ ĐB, bảo vệ MT (mua hàng NK): luôn lấy quy đổi
                SELECT
                    M."id"
                    , 'purchase.document' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (313,
                    314, 315, 316,
                    325, 326, 327,
                    328, 363, 364,
                    365, 366, 375,
                                                      376, 377, 378)
                    THEN
                        CASE
                        WHEN M."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
                            THEN M."SO_UY_NHIEM_CHI"
                        WHEN M."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
                            THEN M."SO_SEC_CHUYEN_KHOAN"
                        WHEN M."LOAI_THANH_TOAN" = 'sec_tien_mat'
                            THEN M."SO_SEC_TIEN_MAT"
                        ELSE
                            M."SO_PHIEU_CHI"
                        END
                      ELSE M."SO_CHUNG_TU"
                      END
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , M."HAN_THANH_TOAN"  AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , M."TEN_DOI_TUONG"
                    , M."DIA_CHI"
                    , N'Thuế nhập khẩu'

                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_THUE_NK_ID")
                    , D."TIEN_THUE_NK_QUY_DOI"
                    , D."TIEN_THUE_NK_QUY_DOI"
                    , '0'
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = LOAI_TIEN_CHINH)
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                       ELSE M."TY_GIA"
                       END)               AS "TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"

                    , CASE WHEN M."LOAI_CHUNG_TU" IN (313, 314, 315,
                                                           316, 325, 326,
                                                           327, 328, 363,
                                                           364, 365, 366,
                                                      375, 376, 377,
                                                      378)
                    THEN M."LY_DO_CHI"
                      ELSE M."DIEN_GIAI_CHUNG"
                      END
                    , 0 --"TINH_CHAT"
                    , 1
                    , P."SortOrderMaster"

                FROM purchase_document M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN purchase_document_line D ON M."id" = D."order_id"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'purchase.document.line'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU"
                                 AND M."currency_id" <> LOAI_TIEN_CHINH
                                 AND M."LOAI_CHUNG_TU" IN (307, 308,
                                                                309, 310, 313,
                                                                314, 315, 316,
                                                                357, 358, 359,
                        360, 363, 364,
                        365, 366, 319,
                        320, 321, 322,
                        325, 326, 327,
                             328, 369, 370,
                             371, 372, 375,
                             376, 377, 378)
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_THUE_NK_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE "TIEN_THUE_NK" <> 0 AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"

                UNION ALL
                SELECT
                    M."id"
                    , 'purchase.document' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (313,
                    314, 315, 316,
                    325, 326, 327,
                    328, 363, 364,
                    365, 366, 375,
                                                      376, 377, 378)
                    THEN
                        CASE
                        WHEN M."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
                            THEN M."SO_UY_NHIEM_CHI"
                        WHEN M."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
                            THEN M."SO_SEC_CHUYEN_KHOAN"
                        WHEN M."LOAI_THANH_TOAN" = 'sec_tien_mat'
                            THEN M."SO_SEC_TIEN_MAT"
                        ELSE
                            M."SO_PHIEU_CHI"
                        END
                      ELSE M."SO_CHUNG_TU"
                      END
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , M."HAN_THANH_TOAN"  AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , M."TEN_DOI_TUONG"
                    , M."DIA_CHI"
                    , N'Thuế tiêu thụ đặc biệt'

                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_THUE_TTDB_ID")
                    , D."TIEN_THUE_TTDB_QUY_DOI"
                    , D."TIEN_THUE_TTDB_QUY_DOI"
                    , '0'
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = LOAI_TIEN_CHINH)
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                       ELSE M."TY_GIA"
                       END)               AS "TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"

                    , CASE WHEN M."LOAI_CHUNG_TU" IN (313, 314, 315,
                                                           316, 325, 326,
                                                           327, 328, 363,
                                                           364, 365, 366,
                                                      375, 376, 377,
                                                      378)
                    THEN M."LY_DO_CHI"
                      ELSE M."DIEN_GIAI_CHUNG"
                      END
                    , 0
                    , 2
                    , P."SortOrderMaster"

                FROM purchase_document M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN purchase_document_line D ON M."id" = D."order_id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'purchase.document.line'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU"
                                 AND M."currency_id" <> LOAI_TIEN_CHINH
                                 AND M."LOAI_CHUNG_TU" IN (307, 308,
                                                                309, 310, 313,
                                                                314, 315, 316,
                                                                357, 358, 359,
                        360, 363, 364,
                        365, 366, 319,
                        320, 321, 322,
                        325, 326, 327,
                             328, 369, 370,
                             371, 372, 375,
                             376, 377, 378)
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE
                                                                                            T.id = D."TK_THUE_TTDB_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE D."TIEN_THUE_TTDB_QUY_DOI" <> 0 AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"

                UNION ALL
                SELECT
                    M."id"
                    , 'purchase.document' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (313,
                    314, 315, 316,
                    325, 326, 327,
                    328, 363, 364,
                    365, 366, 375,
                                                      376, 377, 378)
                    THEN
                        CASE
                        WHEN M."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
                            THEN M."SO_UY_NHIEM_CHI"
                        WHEN M."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
                            THEN M."SO_SEC_CHUYEN_KHOAN"
                        WHEN M."LOAI_THANH_TOAN" = 'sec_tien_mat'
                            THEN M."SO_SEC_TIEN_MAT"
                        ELSE
                            M."SO_PHIEU_CHI"
                        END
                      ELSE M."SO_CHUNG_TU"
                      END
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , M."HAN_THANH_TOAN"  AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , M."TEN_DOI_TUONG"
                    , M."DIA_CHI"
                    , N'Thuế bảo vệ môi trường'


                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_THUE_BVMT")
                    , D."TIEN_THUE_BVMT_QUY_DOI"
                    , D."TIEN_THUE_BVMT_QUY_DOI"
                    , '0'
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = LOAI_TIEN_CHINH)
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                       ELSE M."TY_GIA"
                       END)               AS "TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"

                    , CASE WHEN M."LOAI_CHUNG_TU" IN (313, 314, 315,
                                                           316, 325, 326,
                                                           327, 328, 363,
                                                           364, 365, 366,
                                                      375, 376, 377,
                                                      378)
                    THEN M."LY_DO_CHI"
                      ELSE M."DIEN_GIAI_CHUNG"
                      END
                    , 0
                    , 3
                    , P."SortOrderMaster"

                FROM purchase_document M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN purchase_document_line D ON M."id" = D."order_id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'purchase.document.line'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU"
                                 AND M."currency_id" <> LOAI_TIEN_CHINH
                                 AND M."LOAI_CHUNG_TU" IN (307, 308,
                                                                309, 310, 313,
                                                                314, 315, 316,
                                                                357, 358, 359,
                        360, 363, 364,
                        365, 366, 319,
                        320, 321, 322,
                        325, 326, 327,
                             328, 369, 370,
                             371, 372, 375,
                             376, 377, 378)
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1
                        ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                FROM
                                                    danh_muc_he_thong_tai_khoan T
                                                WHERE T.id = D."TK_THUE_BVMT")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE D."TIEN_THUE_BVMT_QUY_DOI" <> 0 AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"


                UNION ALL
                /*Mua nhập khẩu hạch toán Nợ TKĐƯ thuế (hoặc TK Nợ), Có TK thuế GTGT,
                Mua trong nước hạch toán Nợ TK thuế GTGT, Có TK Có*/
                SELECT
                    M."id"
                    , 'purchase.document' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (313,
                    314, 315, 316,
                    325, 326, 327,
                    328, 363, 364,
                    365, 366, 375,
                                                      376, 377, 378)
                    THEN
                        CASE
                        WHEN M."LOAI_THANH_TOAN" = 'uy_nhiem_chi'
                            THEN M."SO_UY_NHIEM_CHI"
                        WHEN M."LOAI_THANH_TOAN" = 'sec_chuyen_khoan'
                            THEN M."SO_SEC_CHUYEN_KHOAN"
                        WHEN M."LOAI_THANH_TOAN" = 'sec_tien_mat'
                            THEN M."SO_SEC_TIEN_MAT"
                        ELSE
                            M."SO_PHIEU_CHI"
                        END
                      ELSE M."SO_CHUNG_TU"
                      END
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , M."HAN_THANH_TOAN"  AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , M."TEN_DOI_TUONG"
                    , M."DIA_CHI"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (318, 319, 320,
                                                           321, 322, 324,
                                                           325, 326, 327,
                                                           328, 368, 369,
                                                      370, 371, 372,
                                                      374, 375, 376,
                                                      377, 378)
                    THEN N'Thuế GTGT hàng nhập khẩu'
                      ELSE N'Thuế GTGT được khấu trừ của hàng hóa, dịch vụ'
                      END
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (318, 319, 320,
                                                           321, 322, 324,
                                                           325, 326, 327,
                                                           328, 368, 369,
                                                      370, 371, 372,
                                                      374, 375, 376,
                                                      377, 378)
                    THEN
                        COALESCE(
                            (SELECT T."SO_TAI_KHOAN"
                             FROM
                                 danh_muc_he_thong_tai_khoan T
                             WHERE T.id = D."TK_DU_THUE_GTGT_ID"), (SELECT T."SO_TAI_KHOAN"
                                                                    FROM
                                                                        danh_muc_he_thong_tai_khoan T
                                                                    WHERE T.id = D."TK_NO_ID"))
                      ELSE (SELECT T."SO_TAI_KHOAN"
                            FROM
                                danh_muc_he_thong_tai_khoan T
                            WHERE T.id = D."TK_THUE_GTGT_ID")
                      END                 AS "TK_NO"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (318, 319, 320,
                                                           321, 322, 324,
                                                           325, 326, 327,
                                                           328, 368, 369,
                                                      370, 371, 372,
                                                      374, 375, 376,
                                                      377, 378)
                    THEN (SELECT T."SO_TAI_KHOAN"
                          FROM
                              danh_muc_he_thong_tai_khoan T
                          WHERE T.id = D."TK_THUE_GTGT_ID")
                      ELSE (SELECT T."SO_TAI_KHOAN"
                            FROM
                                danh_muc_he_thong_tai_khoan T
                            WHERE T.id = D."TK_CO_ID")
                      END
                                          AS "TK_CO"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (318, 319, 320,
                                                           321, 322, 324,
                                                           325, 326, 327,
                                                           328, 368, 369,
                                                      370, 371, 372,
                                                      374, 375, 376,
                                                      377, 378)
                    THEN D."TIEN_THUE_GTGT_QUY_DOI"
                      ELSE D."TIEN_THUE_GTGT"
                      END                 AS "THANH_TIEN"
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN (CASE WHEN
                        D."TIEN_THUE_GTGT_THEO_TGXQ" <> 0
                        THEN D."TIEN_THUE_GTGT_THEO_TGXQ"

                          ELSE D."TIEN_THUE_GTGT_QUY_DOI"
                          END)
                       ELSE D."TIEN_THUE_GTGT_QUY_DOI"
                       END)               AS "SO_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (318, 319, 320,
                                                           321, 322, 324,
                                                           325, 326, 327,
                                                           328, 368, 369,
                                                      370, 371, 372,
                                                      374, 375, 376,
                                                      377, 378)
                    THEN'0'
                      ELSE CCY."PHEP_TINH_QUY_DOI"
                      END                 AS "PHEP_TINH_CHUYEN_DOI"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (318, 319, 320,
                                                           321, 322, 324,
                                                           325, 326, 327,
                                                           328, 368, 369,
                                                      370, 371, 372,
                                                      374, 375, 376,
                                                      377, 378)
                    THEN (SELECT "MA_LOAI_TIEN"
                          FROM res_currency T
                          WHERE T.id = LOAI_TIEN_CHINH)
                      ELSE (SELECT T."MA_LOAI_TIEN"
                            FROM res_currency T
                            WHERE T.id = M."currency_id")
                      END                 AS "LOAI_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (318, 319, 320,
                                                           321, 322, 324,
                                                           325, 326, 327,
                                                           328, 368, 369,
                                                      370, 371, 372,
                                                      374, 375, 376,
                                                      377, 378)
                    THEN 1
                      ELSE
                          (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                     AND EX."ID_CHUNG_TU" IS NOT NULL
                              THEN EX."FIRST_TY_GIA_XUAT_QUY"
                           ELSE M."TY_GIA"
                           END)
                      END                 AS "TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"

                    , CASE WHEN M."LOAI_CHUNG_TU" IN (313, 314, 315,
                                                           316, 325, 326,
                                                           327, 328, 363,
                                                           364, 365, 366,
                                                      375, 376, 377,
                                                      378)
                    THEN M."LY_DO_CHI"
                      ELSE M."DIEN_GIAI_CHUNG"
                      END
                    , 0
                    , 4
                    , P."SortOrderMaster"


                FROM purchase_document M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN purchase_document_line D ON M."id" = D."order_id"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'purchase.document.line'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU"
                                 AND M."currency_id" <> LOAI_TIEN_CHINH
                                 AND M."LOAI_CHUNG_TU" IN (307, 308,
                                                                309, 310, 313,
                                                                314, 315, 316,
                                                                357, 358, 359,
                        360, 363, 364,
                        365, 366, 319,
                        320, 321, 322,
                        325, 326, 327,
                             328, 369, 370,
                             371, 372, 375,
                             376, 377, 378)
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS CA ON CA."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS DA ON DA."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS DDA ON DDA."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                          FROM
                                                                                              danh_muc_he_thong_tai_khoan T
                                                                                          WHERE T.id =
                                                                                                D."TK_DU_THUE_GTGT_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS VA ON VA."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE
                                                                                            T.id = D."TK_THUE_GTGT_ID")
                WHERE "TIEN_THUE_GTGT_QUY_DOI" <> 0
                      AND (M."LOAI_CHUNG_TU" IN (318, 319, 320, 321, 322, 324, 325, 326, 327, 328, 368, 369,
                                                 370, 371, 372, 374, 375, 376, 377, 378)
                           OR (D."TK_THUE_GTGT_ID" IS NOT NULL AND PHUONG_PHAP_TINH_THUE = 'PHUONG_PHAP_KHAU_TRU')
                      )
                      AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;


        IF rec."LOAI_CHUNG_TU" = ANY
           ('{3550,3551,3552,3553,3554,3555}' :: INT [])--  'SADiscount' --AND @DetailTableName = 'sale_ex_chi_tiet_giam_gia_hang_ban'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'sale.ex.giam.gia.hang.ban' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL :: TIMESTAMP           AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_KHACH_HANG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , COALESCE(D."TEN_HANG", M."DIEN_GIAI")

                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , CASE WHEN M."LOAI_CHUNG_TU" = 3553
                                OR M."LOAI_CHUNG_TU" = 3552
                    THEN D."THANH_TIEN"
                         - D."TIEN_CHIET_KHAU"
                         + D."TIEN_THUE_GTGT"
                      WHEN M."LOAI_CHUNG_TU" = 3555
                           OR M."LOAI_CHUNG_TU" = 3554
                          THEN D."THANH_TIEN"
                               - D."TIEN_CHIET_KHAU"
                      ELSE D."THANH_TIEN"
                      END                         AS "THANH_TIEN"
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN CASE WHEN M."LOAI_CHUNG_TU" = 3551
                        THEN (CASE
                              WHEN
                                  D."THANH_TIEN_THEO_TY_GIA_XUAT_QUY" <> 0
                                  THEN D."THANH_TIEN_THEO_TY_GIA_XUAT_QUY"

                              ELSE D."THANH_TIEN_QUY_DOI"
                              END)
                         ELSE (CASE
                               WHEN
                                   D."THANH_TIEN_THEO_TY_GIA_XUAT_QUY" <> 0
                                   THEN D."THANH_TIEN_THEO_TY_GIA_XUAT_QUY"

                               ELSE (CASE
                                     WHEN M."LOAI_CHUNG_TU" = 3553
                                         THEN D."THANH_TIEN_QUY_DOI"
                                              - D."TIEN_CHIET_KHAU_QUY_DOI"
                                              + D."TIEN_THUE_GTGT_QUY_DOI"
                                     ELSE D."THANH_TIEN_QUY_DOI"
                                          - D."TIEN_CHIET_KHAU_QUY_DOI"
                                     END)
                               END)
                         END
                       ELSE (CASE WHEN M."LOAI_CHUNG_TU" = 3553
                                       OR M."LOAI_CHUNG_TU" = 3552
                           THEN D."THANH_TIEN_QUY_DOI"
                                - D."TIEN_CHIET_KHAU_QUY_DOI"
                                + D."TIEN_THUE_GTGT_QUY_DOI"
                             WHEN M."LOAI_CHUNG_TU" = 3555
                                  OR M."LOAI_CHUNG_TU" = 3554
                                 THEN D."THANH_TIEN_QUY_DOI"
                                      - D."TIEN_CHIET_KHAU_QUY_DOI"
                             ELSE D."THANH_TIEN_QUY_DOI"
                             END)
                       END)                       AS "SO_TIEN"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id")
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                       ELSE M."TY_GIA"
                       END)                       AS "TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , CAST(COALESCE(II."TINH_CHAT", '0') AS INT)
                    , 0
                    , P."SortOrderMaster"


                FROM sale_ex_giam_gia_hang_ban M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban D ON M."id" = D."GIAM_GIA_HANG_BAN_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN danh_muc_vat_tu_hang_hoa II ON II."id" = d."MA_HANG_ID"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'sale.ex.chi.tiet.giam.gia.hang.ban'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU"
                                 AND M."currency_id" <> LOAI_TIEN_CHINH
                                 AND M."LOAI_CHUNG_TU" IN (3551, 3553,
                                                           3555)
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                UNION ALL
                SELECT
                    M."id"
                    , 'sale.ex.giam.gia.hang.ban' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL :: TIMESTAMP           AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_KHACH_HANG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , N'Chiết khấu bán hàng'

                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CHIET_KHAU_ID")


                    , D."TIEN_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU_QUY_DOI"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id")
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                       ELSE M."TY_GIA"
                       END)                       AS "TY_GIA"
                    , d."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , 0
                    , 5
                    , P."SortOrderMaster"

                FROM sale_ex_giam_gia_hang_ban M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban D ON M."id" = D."GIAM_GIA_HANG_BAN_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'sale.ex.chi.tiet.giam.gia.hang.ban'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU"
                                 AND M."currency_id" <> LOAI_TIEN_CHINH
                                 AND M."LOAI_CHUNG_TU" IN (3551, 3553,
                                                           3555)
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE
                                                                                            T.id = D."TK_CHIET_KHAU_ID")
                WHERE D."TIEN_CHIET_KHAU_QUY_DOI" <> 0
                      AND (M."LOAI_CHUNG_TU" = 3551
                           OR M."LOAI_CHUNG_TU" = 3550
                      ) /*Chỉ in dòng chiết khấu của bán giảm giá từ bán hàng trong nước*/
                      AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"


                UNION ALL
                SELECT
                    M."id"
                    , 'sale.ex.giam.gia.hang.ban' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL :: TIMESTAMP           AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_KHACH_HANG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , N'Thuế GTGT'

                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_THUE_GTGT_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , D."TIEN_THUE_GTGT"
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN (CASE WHEN
                        D."TIEN_THUE_GTGT_THEO_TGXQ" <> 0
                        THEN D."TIEN_THUE_GTGT_THEO_TGXQ"

                          ELSE D."TIEN_THUE_GTGT_QUY_DOI"
                          END)
                       ELSE D."TIEN_THUE_GTGT_QUY_DOI"
                       END)                       AS "THUE_GTGT"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id")
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                       ELSE M."TY_GIA"
                       END)                       AS "TY_GIA"
                    , d."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , 0
                    , 2
                    , P."SortOrderMaster"

                FROM sale_ex_giam_gia_hang_ban M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban D ON M."id" = D."GIAM_GIA_HANG_BAN_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'sale.ex.chi.tiet.giam.gia.hang.ban'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU"
                                 AND M."currency_id" <> LOAI_TIEN_CHINH
                                 AND M."LOAI_CHUNG_TU" IN (3551, 3553,
                                                           3555)
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE
                                                                                            T.id = D."TK_THUE_GTGT_ID")
                WHERE "TIEN_THUE_GTGT_QUY_DOI" <> 0
                      AND (M."LOAI_CHUNG_TU" = 3551
                           OR M."LOAI_CHUNG_TU" = 3550
                      ) /*Chỉ in dòng thuế của bán giảm giá từ bán hàng trong nước*/
                      AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;


        IF rec."LOAI_CHUNG_TU" =
        ANY
           ('{3540,3541,3542,3543,3544,3545}' :: INT [])--  'SAReturn' --AND @DetailTableName = 'purchase_ex_chi_tiet_tra_lai_hang_ban'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'sale.ex.tra.lai.hang.ban' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL :: TIMESTAMP          AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_KHACH_HANG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , COALESCE(D."TEN_HANG", M."DIEN_GIAI")

                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , CASE WHEN M."LOAI_CHUNG_TU" = 3543
                                OR M."LOAI_CHUNG_TU" = 3542
                    THEN D."THANH_TIEN"
                         - D."TIEN_CHIET_KHAU"
                         + D."TIEN_THUE_GTGT"
                      WHEN M."LOAI_CHUNG_TU" = 3545
                           OR M."LOAI_CHUNG_TU" = 3544
                          THEN D."THANH_TIEN"
                               - D."TIEN_CHIET_KHAU"
                      ELSE D."THANH_TIEN"
                      END                        AS "THANH_TIEN"
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN CASE WHEN M."LOAI_CHUNG_TU" = 3541
                        THEN (CASE
                              WHEN
                                  D."THANH_TIEN_THEO_TY_GIA_XUAT_QUY" <> 0
                                  THEN D."THANH_TIEN_THEO_TY_GIA_XUAT_QUY"

                              ELSE D."THANH_TIEN_QUY_DOI"
                              END)
                         ELSE (CASE
                               WHEN
                                   D."THANH_TIEN_THEO_TY_GIA_XUAT_QUY" <> 0
                                   THEN D."THANH_TIEN_THEO_TY_GIA_XUAT_QUY"

                               ELSE (CASE
                                     WHEN M."LOAI_CHUNG_TU" = 3543
                                         THEN D."THANH_TIEN_QUY_DOI"
                                              - D."TIEN_CHIET_KHAU_QUY_DOI"
                                              + D."TIEN_THUE_GTGT_QUY_DOI"
                                     ELSE D."THANH_TIEN_QUY_DOI"
                                          - D."TIEN_CHIET_KHAU_QUY_DOI"
                                     END)
                               END)
                         END
                       ELSE (CASE WHEN M."LOAI_CHUNG_TU" = 3543
                                       OR M."LOAI_CHUNG_TU" = 3542
                           THEN D."THANH_TIEN_QUY_DOI"
                                - D."TIEN_CHIET_KHAU_QUY_DOI"
                                + D."TIEN_THUE_GTGT_QUY_DOI"
                             WHEN M."LOAI_CHUNG_TU" = 3545
                                  OR M."LOAI_CHUNG_TU" = 3544
                                 THEN D."THANH_TIEN_QUY_DOI"
                                      - D."TIEN_CHIET_KHAU_QUY_DOI"
                             ELSE D."THANH_TIEN_QUY_DOI"
                             END)
                       END)                      AS "SO_TIEN"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id")
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                       ELSE M."TY_GIA"
                       END)                      AS "TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , 0
                    , 0
                    , P."SortOrderMaster"

                FROM sale_ex_tra_lai_hang_ban M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet D ON M."id" = D."TRA_LAI_HANG_BAN_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN danh_muc_vat_tu_hang_hoa II ON II."id" = d."MA_HANG_ID"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'sale.ex.tra.lai.hang.ban.chi.tiet'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU"
                                 AND M."currency_id" <> LOAI_TIEN_CHINH
                                 AND M."LOAI_CHUNG_TU" IN (3541, 3543,
                                                           3545)
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                UNION ALL
                SELECT
                    M."id"
                    , 'sale.ex.tra.lai.hang.ban' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL :: TIMESTAMP          AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_KHACH_HANG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , N'Chiết khấu bán hàng'
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CHIET_KHAU")

                    , D."TIEN_CHIET_KHAU"
                    , D."TIEN_CHIET_KHAU_QUY_DOI"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id")
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN EX."FIRST_TY_GIA_XUAT_QUY"
                       ELSE M."TY_GIA"
                       END)                      AS "TY_GIA"
                    , d."THU_TU_SAP_XEP_CHI_TIET"

                    , M."DIEN_GIAI"
                    , 0
                    , 5
                    , P."SortOrderMaster"

                FROM sale_ex_tra_lai_hang_ban M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet D ON M."id" = D."TRA_LAI_HANG_BAN_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'sale.ex.tra.lai.hang.ban.chi.tiet'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU"
                                 AND M."currency_id" <> LOAI_TIEN_CHINH
                                 AND M."LOAI_CHUNG_TU" IN (3541, 3543,
                                                           3545)
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE D."TIEN_CHIET_KHAU_QUY_DOI" <> 0
                      AND (M."LOAI_CHUNG_TU" = 3541
                           OR M."LOAI_CHUNG_TU" = 3540
                      ) /*Chỉ in dòng chiết khấu của bán trả lại từ bán hàng trong nước*/
                      AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                UNION ALL
                SELECT
                    M."id"
                    , 'sale.ex.tra.lai.hang.ban' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL :: TIMESTAMP          AS "HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_KHACH_HANG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , N'Thuế GTGT'

                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_THUE_GTGT_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , D."TIEN_THUE_GTGT"
                    , (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                    THEN (CASE WHEN
                        D."TIEN_THUE_GTGT_QUY_DOI_THEO_TGXQ" <> 0
                        THEN D."TIEN_THUE_GTGT_QUY_DOI_THEO_TGXQ"

                          ELSE D."TIEN_THUE_GTGT_QUY_DOI"
                          END)
                       ELSE D."TIEN_THUE_GTGT_QUY_DOI"
                       END)                      AS "THUE_GTGT"
                    , CCY."PHEP_TINH_QUY_DOI"
                    , (SELECT T."MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = M."currency_id")
                    , --M."TY_GIA" ,
                      (CASE WHEN M."currency_id" <> LOAI_TIEN_CHINH
                                 AND EX."ID_CHUNG_TU" IS NOT NULL
                          THEN EX."FIRST_TY_GIA_XUAT_QUY"
                       ELSE M."TY_GIA"
                       END)                      AS "TY_GIA"
                    , d."THU_TU_SAP_XEP_CHI_TIET"

                    , M."DIEN_GIAI"
                    , 0
                    , 2
                    , P."SortOrderMaster"

                FROM sale_ex_tra_lai_hang_ban M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet D ON M."id" = D."TRA_LAI_HANG_BAN_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN LAY_DS_CAC_LOAI_TY_GIA_TREN_CHUNG_TU_NGOAI_TE(ListParam,
                                                                            'sale.ex.tra.lai.hang.ban.chi.tiet'
                              )
                        AS EX ON M."id" = EX."ID_CHUNG_TU"
                                 AND M."currency_id" <> LOAI_TIEN_CHINH
                                 AND M."LOAI_CHUNG_TU" IN (3541, 3543,
                                                           3545)
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE
                                                                                            T.id = D."TK_THUE_GTGT_ID")
                WHERE D."TIEN_THUE_GTGT_QUY_DOI" <> 0
                      AND (M."LOAI_CHUNG_TU" = 3541
                           OR M."LOAI_CHUNG_TU" = 3540
                      ) /*Chỉ in dòng thuế của bán trả lại từ bán hàng trong nước*/
                      AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"

            ;
        END IF
    ;

        --HHSon1: CT bán hàng, nếu là bán hàng xuất khẩu, uỷ thác XK thì luôn lấy quy đổi
        IF rec."LOAI_CHUNG_TU" = ANY
           ('{3530,3531,3532,3534,3535,3536,3537,3538}' :: INT [])-- '"SAVoucher"' --AND @DetailTableName = '"sale_document"Detail'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'sale.document' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , M."HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_KHACH_HANG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , COALESCE(D."TEN_HANG", M."DIEN_GIAI")

                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , CASE WHEN M."LOAI_CHUNG_TU" = 3532 -- Nếu là bán hàng XK thì luôn lấy quy đổi
                    THEN (D."THANH_TIEN_QUY_DOI"
                          - D."TIEN_THUE_XUAT_KHAU") --- nvtoan loại tiền này ra theo lỗi 93565
                      WHEN M."LOAI_CHUNG_TU" = 3536 --Nếu là bán hàng uỷ thác XK
                          THEN (D."THANH_TIEN_QUY_DOI"
                                - D."TIEN_THUE_XUAT_KHAU"
                                - D."TIEN_CK_QUY_DOI") --nvtoan:07/04/2016 Sửa lỗi bán hàng ủy thác chưa trừ đi giảm giá
                      WHEN M."LOAI_CHUNG_TU" IN (3534, 3535,
                                                 3538) -- Nếu là bán hàng đại lý bán đúng giá
                          THEN D."THANH_TIEN"
                               - D."TIEN_CHIET_KHAU"
                               + D."TIEN_THUE_GTGT"
                      ELSE D."THANH_TIEN"
                      END             AS "THANH_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" = 3532 -- Nếu là bán hàng XK thì luôn lấy quy đổi
                    THEN (D."THANH_TIEN_QUY_DOI"
                          -
                          D."TIEN_THUE_XUAT_KHAU") ----- nvtoan loại tiền này ra theo lỗi 93565 - D."KHOAN_GIAM_GIA_THANH"
                      WHEN M."LOAI_CHUNG_TU" = 3536 -- Nếu là bán hàng uỷ thác XK thì luôn lấy quy đổi
                          THEN (D."THANH_TIEN_QUY_DOI"
                                - D."TIEN_THUE_XUAT_KHAU"
                                - D."TIEN_CK_QUY_DOI") --nvtoan:07/04/2016 Sửa lỗi bán hàng ủy thác chưa trừ đi giảm giá
                      WHEN M."LOAI_CHUNG_TU" IN (3534, 3535,
                                                 3538) -- Nếu là bán hàng đại lý bán đúng giá
                          THEN D."THANH_TIEN_QUY_DOI"
                               - D."TIEN_CK_QUY_DOI"
                               + D."TIEN_THUE_GTGT_QUY_DOI"
                      ELSE D."THANH_TIEN_QUY_DOI"
                      END             AS "SO_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN'0'
                      ELSE CCY."PHEP_TINH_QUY_DOI"
                      END             AS "PHEP_TINH_CHUYEN_DOI"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN (SELECT "MA_LOAI_TIEN"
                          FROM res_currency T
                          WHERE T.id = LOAI_TIEN_CHINH)
                      ELSE (SELECT T."MA_LOAI_TIEN"
                            FROM res_currency T
                            WHERE T.id = M."currency_id")
                      END             AS "LOAI_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN 1
                      ELSE M."TY_GIA"
                      END             AS "TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , CAST(COALESCE(II."TINH_CHAT", '0') AS INT)
                    , 0
                    , P."SortOrderMaster"

                FROM sale_document M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN sale_document_line D ON M."id" = D."SALE_DOCUMENT_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN danh_muc_vat_tu_hang_hoa II ON II."id" = d."MA_HANG_ID"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE (CHE_DO_KE_TOAN = '15') AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                UNION ALL
                SELECT
                    M."id"
                    , 'sale.document'     AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , M."HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_KHACH_HANG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , N'Chiết khấu bán hàng'


                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CHIET_KHAU_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN D."TIEN_CK_QUY_DOI"
                      ELSE D."TIEN_CHIET_KHAU"
                      END                 AS "THANH_TIEN"
                    , D."TIEN_CK_QUY_DOI" AS "SO_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN'0'
                      ELSE CCY."PHEP_TINH_QUY_DOI"
                      END                 AS "PHEP_TINH_CHUYEN_DOI"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN (SELECT "MA_LOAI_TIEN"
                          FROM res_currency T
                          WHERE T.id = LOAI_TIEN_CHINH)
                      ELSE (SELECT T."MA_LOAI_TIEN"
                            FROM res_currency T
                            WHERE T.id = M."currency_id")
                      END                 AS "LOAI_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN 1
                      ELSE M."TY_GIA"
                      END                 AS "TY_GIA"
                    , d."THU_TU_SAP_XEP_CHI_TIET"

                    , M."DIEN_GIAI"
                    , 0
                    , 5
                    , P."SortOrderMaster"

                FROM sale_document M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN sale_document_line D ON M."id" = D."SALE_DOCUMENT_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE
                                                                                            T.id = D."TK_CHIET_KHAU_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE (CHE_DO_KE_TOAN = '15')
                      AND D."TIEN_CK_QUY_DOI" <> 0

                      AND M."LOAI_CHUNG_TU" NOT IN (3534, 3535,
                                                    3538, 3536)
                      AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                UNION ALL
                --- QD 48
                SELECT
                    M."id"
                    , 'sale.document' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , M."HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_KHACH_HANG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , COALESCE(D."TEN_HANG", M."DIEN_GIAI")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , CASE
                      /*thêm trường hợp hàng bán đại lý đúng giá by hoant 16.06.2015 sửa bug 58066*/
                      WHEN M."LOAI_CHUNG_TU" IN (3534, 3535,
                                                 3538) -- Nếu là bán hàng đại lý bán đúng giá
                          THEN D."THANH_TIEN"
                               - D."TIEN_CHIET_KHAU"
                               + D."TIEN_THUE_GTGT"
                      ELSE (CASE WHEN M."LOAI_CHUNG_TU" IN (
                          3532, 3536)
                          THEN D."THANH_TIEN_QUY_DOI"
                            ELSE D."THANH_TIEN"
                            END
                            - CASE WHEN M."LOAI_CHUNG_TU" = 3536
                          THEN D."TIEN_CK_QUY_DOI"
                              ELSE 0
                              END)
                      END             AS "THANH_TIEN"
                    , CASE
                      /*thêm trường hợp hàng bán đại lý đúng giá by hoant 16.06.2015 sửa bug 58066*/
                      WHEN M."LOAI_CHUNG_TU" IN (3534, 3535,
                                                 3538) -- Nếu là bán hàng đại lý bán đúng giá
                          THEN D."THANH_TIEN_QUY_DOI"
                               - D."TIEN_CK_QUY_DOI"
                               + D."TIEN_THUE_GTGT_QUY_DOI"
                      ELSE (D."THANH_TIEN_QUY_DOI"
                            - CASE WHEN M."LOAI_CHUNG_TU" = 3536
                          THEN D."TIEN_CK_QUY_DOI"
                              ELSE 0
                              END)
                      END             AS "SO_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN'0'
                      ELSE CCY."PHEP_TINH_QUY_DOI"
                      END             AS "PHEP_TINH_CHUYEN_DOI"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN (SELECT "MA_LOAI_TIEN"
                          FROM res_currency T
                          WHERE T.id = LOAI_TIEN_CHINH)
                      ELSE (SELECT T."MA_LOAI_TIEN"
                            FROM res_currency T
                            WHERE T.id = M."currency_id")
                      END             AS "LOAI_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN 1
                      ELSE M."TY_GIA"
                      END             AS "TY_GIA"
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , CAST(COALESCE(II."TINH_CHAT", '0') AS INT)
                    , 0
                    , P."SortOrderMaster"


                FROM sale_document M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN sale_document_line D ON M."id" = D."SALE_DOCUMENT_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN danh_muc_vat_tu_hang_hoa II ON II."id" = d."MA_HANG_ID"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE CHE_DO_KE_TOAN = '48' AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                UNION ALL
                SELECT
                    M."id"
                    , 'sale.document'     AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , M."HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_KHACH_HANG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , N'Chiết khấu bán hàng'


                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CHIET_KHAU_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN D."TIEN_CK_QUY_DOI"
                      ELSE D."TIEN_CHIET_KHAU"
                      END                 AS "THANH_TIEN"
                    , D."TIEN_CK_QUY_DOI" AS "SO_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN'0'
                      ELSE CCY."PHEP_TINH_QUY_DOI"
                      END                 AS "PHEP_TINH_CHUYEN_DOI"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN (SELECT "MA_LOAI_TIEN"
                          FROM res_currency T
                          WHERE T.id = LOAI_TIEN_CHINH)
                      ELSE (SELECT T."MA_LOAI_TIEN"
                            FROM res_currency T
                            WHERE T.id = M."currency_id")
                      END                 AS "LOAI_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN 1
                      ELSE M."TY_GIA"
                      END                 AS "TY_GIA"
                    , d."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , 0
                    , 5
                    , P."SortOrderMaster"

                FROM sale_document M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN sale_document_line D ON M."id" = D."SALE_DOCUMENT_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE
                                                                                            T.id = D."TK_CHIET_KHAU_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE CHE_DO_KE_TOAN = '48'
                      AND D."TIEN_CK_QUY_DOI" <> 0
                      --AND M."LOAI_CHUNG_TU" <> 3536
                      AND M."LOAI_CHUNG_TU" NOT IN (3534, 3535,
                                                    3538, 3536)
                      AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                UNION ALL
                SELECT
                    M."id"
                    , 'sale.document'            AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , M."HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_KHACH_HANG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , N'Thuế GTGT'
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")

                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_THUE_GTGT_ID")
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN D."TIEN_THUE_GTGT_QUY_DOI"
                      ELSE D."TIEN_THUE_GTGT"
                      END                        AS "THANH_TIEN"
                    , D."TIEN_THUE_GTGT_QUY_DOI" AS "SO_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN'0'
                      ELSE CCY."PHEP_TINH_QUY_DOI"
                      END                        AS "PHEP_TINH_CHUYEN_DOI"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN (SELECT "MA_LOAI_TIEN"
                          FROM res_currency T
                          WHERE T.id = LOAI_TIEN_CHINH)
                      ELSE (SELECT T."MA_LOAI_TIEN"
                            FROM res_currency T
                            WHERE T.id = M."currency_id")
                      END                        AS "LOAI_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN 1
                      ELSE M."TY_GIA"
                      END                        AS "TY_GIA"
                    , d."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , 0
                    , 2
                    , P."SortOrderMaster"

                FROM sale_document M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN sale_document_line D ON M."id" = D."SALE_DOCUMENT_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE
                                                                                            T.id = D."TK_THUE_GTGT_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE D."TIEN_THUE_GTGT_QUY_DOI" <> 0

                      AND M."LOAI_CHUNG_TU" NOT IN (3534, 3535,
                                                    3538, 3536, 3532)
                      AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                UNION ALL
                SELECT
                    M."id"
                    , 'sale.document' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , M."HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_KHACH_HANG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , N'Tiền thuế xuất khẩu'
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_THUE_XK_ID")

                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN D."TIEN_THUE_XUAT_KHAU"
                      ELSE 0
                      END             AS "THANH_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN D."TIEN_THUE_XUAT_KHAU"
                      ELSE 0
                      END             AS "SO_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN'0'
                      ELSE CCY."PHEP_TINH_QUY_DOI"
                      END             AS "PHEP_TINH_CHUYEN_DOI"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN (SELECT "MA_LOAI_TIEN"
                          FROM res_currency T
                          WHERE T.id = LOAI_TIEN_CHINH)
                      ELSE (SELECT T."MA_LOAI_TIEN"
                            FROM res_currency T
                            WHERE T.id = M."currency_id")
                      END             AS "LOAI_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN 1
                      ELSE M."TY_GIA"
                      END             AS "TY_GIA"
                    , d."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , 0
                    , 3
                    , P."SortOrderMaster"


                FROM sale_document M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN sale_document_line D ON M."id" = D."SALE_DOCUMENT_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_THUE_XK_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE CHE_DO_KE_TOAN = '15'
                      AND D."TIEN_THUE_XUAT_KHAU" <> 0
                      AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
                UNION ALL
                SELECT
                    M."id"
                    , 'sale.document' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , M."HAN_THANH_TOAN"
                    , M."DOI_TUONG_ID"
                    , COALESCE(M."TEN_KHACH_HANG", '')
                    , COALESCE(M."DIA_CHI", '')
                    , N'Tiền thuế xuất khẩu'

                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_THUE_XK_ID")
                    , --SUM(D."THUE_XUAT_KHAU") ,
                      CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                          THEN D."TIEN_THUE_XUAT_KHAU"
                      ELSE 0
                      END             AS "THANH_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN D."TIEN_THUE_XUAT_KHAU"
                      ELSE 0
                      END             AS "SO_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN'0'
                      ELSE CCY."PHEP_TINH_QUY_DOI"
                      END             AS "PHEP_TINH_CHUYEN_DOI"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN (SELECT "MA_LOAI_TIEN"
                          FROM res_currency T
                          WHERE T.id = LOAI_TIEN_CHINH)
                      ELSE (SELECT T."MA_LOAI_TIEN"
                            FROM res_currency T
                            WHERE T.id = M."currency_id")
                      END             AS "LOAI_TIEN"
                    , CASE WHEN M."LOAI_CHUNG_TU" IN (3532, 3536)
                    THEN 1
                      ELSE M."TY_GIA"
                      END             AS "TY_GIA"
                    , d."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , 0
                    , 3
                    , P."SortOrderMaster"

                FROM sale_document M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN sale_document_line D ON M."id" = D."SALE_DOCUMENT_ID"
                    LEFT JOIN res_currency AS CCY ON M."currency_id" = CCY."id"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_THUE_XK_ID")
                WHERE CHE_DO_KE_TOAN = '48'
                      AND D."TIEN_THUE_XUAT_KHAU" <> 0
                      AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"

            ;
        END IF
    ;

        -- Đang validate phần CCDC nên chờ ổn định DB thì sửa lại
        IF rec."LOAI_CHUNG_TU" = ANY ('{453}' :: INT []) --AND @DetailTableName = 'SUAllocationDetail'
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    M."id"
                    , 'supply.phan.bo.chi.phi' AS "MODEL_CHUNG_TU"
                    , M."LOAI_CHUNG_TU"
                    , M."SO_CHUNG_TU"
                    , M."NGAY_CHUNG_TU"
                    , M."NGAY_HACH_TOAN"
                    , NULL                     AS "HAN_THANH_TOAN"
                    , COALESCE(D."DOI_TUONG_NO_ID",
                               D."DOI_TUONG_CO_ID")
                    , NULL
                    , NULL
                    , D."DIEN_GIAI"
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_NO_ID")
                    , (SELECT T."SO_TAI_KHOAN"
                       FROM
                           danh_muc_he_thong_tai_khoan T
                       WHERE T.id = D."TK_CO_ID")
                    , D."SO_TIEN"
                    , D."SO_TIEN"
                    , '0'
                    , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency T
                       WHERE T.id = LOAI_TIEN_CHINH)
                    , 1
                    , D."THU_TU_SAP_XEP_CHI_TIET"
                    , M."DIEN_GIAI"
                    , 0
                    , 0
                    , P."SortOrderMaster"

                FROM supply_phan_bo_chi_phi M
                    INNER JOIN TMP_PARAM P ON M."id" = P."ID_CHUNG_TU"
                    INNER JOIN supply_phan_bo_chi_phi_hach_toan D ON M."id" = D."PHAN_BO_CHI_PHI_ID"
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_CO_ID")
                    LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = (SELECT T."SO_TAI_KHOAN"
                                                                                        FROM
                                                                                            danh_muc_he_thong_tai_khoan T
                                                                                        WHERE T.id = D."TK_NO_ID")
                WHERE P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;

    END LOOP
    ;

    DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
    ;

    CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
        AS

            SELECT
                  CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                      THEN C."ID_CHUNG_TU"
                  ELSE R."ID_CHUNG_TU"
                  END                          AS "ID_CHUNG_TU"
                , CASE WHEN C."MODEL_CHUNG_TU" IS NOT NULL
                THEN C."MODEL_CHUNG_TU"
                  ELSE R."MODEL_CHUNG_TU"
                  END                          AS "MODEL_CHUNG_TU"
                , CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                THEN C."LOAI_CHUNG_TU"
                  ELSE R."LOAI_CHUNG_TU"
                  END                          AS "LOAI_CHUNG_TU"
                , CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                THEN C."SO_CHUNG_TU"

                  ELSE R."SO_CHUNG_TU"
                  END                          AS "SO_CHUNG_TU"
                , CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                THEN C."NGAY_CHUNG_TU"
                  ELSE R."NGAY_CHUNG_TU"
                  END                          AS "NGAY_CHUNG_TU"
                , R."NGAY_HACH_TOAN"
                , R."HAN_THANH_TOAN"
                , R."DOI_TUONG_ID"
                , COALESCE(CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                THEN C."TEN_KHACH_HANG"
                           ELSE R."TEN_KHACH_HANG"
                           END, A."HO_VA_TEN") AS "TEN_KHACH_HANG"
                , COALESCE(CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                THEN C."DIA_CHI"
                           ELSE R."DIA_CHI"
                           END, A."DIA_CHI")   AS "DIA_CHI"
                , CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                THEN C."DIEN_GIAI"
                  ELSE R."DIEN_GIAI"
                  END                          AS "DIEN_GIAI"
                , R."DIEN_GIAI_DETAIL"
                , R."TK_NO"
                , R."TK_CO"
                , R."PHEP_TINH_CHUYEN_DOI"
                , CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                THEN (SELECT T."MA_LOAI_TIEN"
                      FROM res_currency T
                      WHERE T.id = C."currency_id")
                  ELSE R."LOAI_TIEN"
                  END                          AS "LOAI_TIEN"
                , CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                THEN C."TY_GIA"
                  ELSE R."TY_GIA"
                  END                          AS "TY_GIA"
                , ROW_NUMBER()
                  OVER (
                      ORDER BY MIN(R."STT") )  AS RowNumber
                , SUM(R."THANH_TIEN")          AS "THANH_TIEN"
                , SUM(R."THANH_TIEN_QUY_DOI")  AS "THANH_TIEN_QUY_DOI"
                , R."SortOrderMaster"
                , R."RowOrder"

            FROM TMP_KET_QUA R
                LEFT JOIN res_partner A ON A."id" = R."DOI_TUONG_ID"
                LEFT JOIN LAY_RA_THONG_TIN_CUA_CAC_CHUNG_TU_CHINH_DUA_THEO_REFID_CUA_CHUNG_TU_PHU C
                    ON R."ID_CHUNG_TU" = C."ID_CHUNG_TU_QUAN_HE" AND R."MODEL_CHUNG_TU" = C."MODEL_CHUNG_TU_QUAN_HE"
                LEFT JOIN danh_muc_he_thong_tai_khoan AS A1 ON A1."SO_TAI_KHOAN" = R."TK_CO"
                LEFT JOIN danh_muc_he_thong_tai_khoan AS A2 ON A2."SO_TAI_KHOAN" = R."TK_NO"
            WHERE R."THANH_TIEN" <> 0
                  OR R."THANH_TIEN_QUY_DOI" <> 0
                  OR R."TINH_CHAT" = 3
            GROUP BY
                CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                    THEN C."ID_CHUNG_TU"
                ELSE R."ID_CHUNG_TU"
                END
                , CASE WHEN C."MODEL_CHUNG_TU" IS NOT NULL
                THEN C."MODEL_CHUNG_TU"
                  ELSE R."MODEL_CHUNG_TU"
                  END
                , CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                THEN C."LOAI_CHUNG_TU"
                  ELSE R."LOAI_CHUNG_TU"
                  END
                , CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                THEN C."SO_CHUNG_TU"

                  ELSE R."SO_CHUNG_TU"
                  END
                , CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                THEN C."NGAY_CHUNG_TU"
                  ELSE R."NGAY_CHUNG_TU"
                  END
                , R."NGAY_HACH_TOAN"
                , R."HAN_THANH_TOAN"
                , R."DOI_TUONG_ID"
                , COALESCE(CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                THEN C."TEN_KHACH_HANG"
                           ELSE R."TEN_KHACH_HANG"
                           END, A."HO_VA_TEN")
                , COALESCE(CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                THEN C."DIA_CHI"
                           ELSE R."DIA_CHI"
                           END, A."DIA_CHI")
                , CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                THEN C."DIEN_GIAI"
                  ELSE R."DIEN_GIAI"
                  END
                , R."DIEN_GIAI_DETAIL"
                , R."TK_NO"
                , R."TK_CO"
                , R."PHEP_TINH_CHUYEN_DOI"
                , CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                THEN (SELECT T."MA_LOAI_TIEN"
                      FROM res_currency T
                      WHERE T.id = C."currency_id")
                  ELSE R."LOAI_TIEN"
                  END
                , CASE WHEN C."ID_CHUNG_TU" IS NOT NULL
                THEN C."TY_GIA"
                  ELSE R."TY_GIA"
                  END
                , R."SortOrderMaster"
                , R."RowOrder"


            ORDER BY
                "SortOrderMaster",
                "RowOrder",

                RowNumber
    ;


END $$

;


SELECT *
FROM TMP_KET_QUA_CUOI_CUNG

;
        """
        return self.execute(query)

    @api.model_cr
    def init(self):
        self.env.cr.execute(""" 
		                
                DROP VIEW IF EXISTS LAY_RA_THONG_TIN_CUA_CAC_CHUNG_TU_CHINH_DUA_THEO_REFID_CUA_CHUNG_TU_PHU;
                CREATE VIEW LAY_RA_THONG_TIN_CUA_CAC_CHUNG_TU_CHINH_DUA_THEO_REFID_CUA_CHUNG_TU_PHU --View_RelationVoucher
                
                AS
                SELECT
                    --Thông tin chứng từ gốc
                
                        SV."id" AS "ID_CHUNG_TU",
                        'sale.document' AS "MODEL_CHUNG_TU",
                        SV."LOAI_CHUNG_TU" ,
                        SV."NGAY_CHUNG_TU" ,
                        SV."TEN_KHACH_HANG" ,
                        SV."DIA_CHI" ,
                        SV."DIEN_GIAI" ,
                        SV."currency_id" ,
                        SV."TY_GIA",
                        SV."NGAY_HACH_TOAN" AS "NGAY_HACH_TOAN" ,
                        SV."state" AS "TRANG_THAI_GHI_SO" ,
                        NULL AS "INRefOrder" ,
                        SV."SO_CHUNG_TU" AS "SO_CHUNG_TU" ,
                
                        R."id" AS "ID_CHUNG_TU_QUAN_HE" ,
                         'stock.ex.nhap.xuat.kho' AS "MODEL_CHUNG_TU_QUAN_HE",
                        R."LOAI_CHUNG_TU" AS "LOAI_CHUNG_TU_QUAN_HE",
                        R."NGAY_HACH_TOAN" AS "NGAY_HACH_TOAN_QUAN_HE" ,
                        R."state" AS "TRANG_THAI_GHI_SO_QUAN_HE" ,
                
                        R."SO_CHUNG_TU" AS "SO_CHUNG_TU_QUAN_HE"
                
                 FROM    sale_document AS SV
                        INNER  JOIN sale_ex_document_outward_rel AS SOR ON SOR."sale_document_id" = SV."id"
                        INNER JOIN stock_ex_nhap_xuat_kho R ON Sor."stock_ex_nhap_xuat_kho_id"=R."id"
                --WHERE   SOR.ReferenceType = 0
                
                UNION ALL
                SELECT
                        SV."id" ,
                        'sale.ex.tra.lai.hang.ban' AS "MODEL_CHUNG_TU",
                        SV."LOAI_CHUNG_TU" ,
                        SV."NGAY_CHUNG_TU" ,
                        sv."TEN_KHACH_HANG" ,
                        SV."DIA_CHI" ,
                        SV."DIEN_GIAI" ,
                        SV."currency_id" ,
                        SV."TY_GIA",
                        SV."NGAY_HACH_TOAN" AS "NGAY_HACH_TOAN" ,
                        SV."state" AS "TRANG_THAI_GHI_SO" ,
                
                        NULL AS "INRefOrder" ,
                
                        SV."SO_CHUNG_TU" AS "SO_CHUNG_TU" ,
                
                
                        R."id" AS "ID_CHUNG_TU_QUAN_HE" ,
                         'stock.ex.nhap.xuat.kho' AS "MODEL_CHUNG_TU_QUAN_HE",
                        R."LOAI_CHUNG_TU" AS "LOAI_CHUNG_TU_QUAN_HE",
                        R."NGAY_HACH_TOAN" AS "NGAY_HACH_TOAN_QUAN_HE" ,
                        R."state" AS "TRANG_THAI_GHI_SO_QUAN_HE" ,
                
                        R."SO_CHUNG_TU" AS "SO_CHUNG_TU_QUAN_HE"
                
                FROM    sale_ex_tra_lai_hang_ban SV
                INNER JOIN stock_ex_nhap_xuat_kho R ON sv."PHIEU_NHAP_ID"=R."id"
                WHERE   SV."KIEM_TRA_PHIEU_NHAP_KHO" = TRUE  ;
                
                
                
                
                
                


		



		""")
