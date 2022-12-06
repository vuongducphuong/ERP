# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_01VT_NHAP_KHO(models.Model):
    _name = 'bao.cao.01vt.nhap.kho'
    _auto = False

    ref = fields.Char(string='Reffence ID')
    ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
    MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')
    NGAY_CHUNG_TU =  fields.Date(string='Ngày chứng từ') #RefDate
    NGAY_HACH_TOAN =  fields.Date(string='Ngày hạch toán') #PostedDate
    SO_CHUNG_TU =  fields.Char(string='Số chứng từ') #RefNoFinance
    TEN_KHACH_HANG =  fields.Char(string='Tên khách hàng') #AccountObjectName
    TEN_KHACH_HANG_HOA_DON =  fields.Char(string='Tên khách hàng hóa đơn') #InVoiceAccountObjectName
    NGUOI_GIAO_HANG =  fields.Char(string='Người giao hàng') #AccountObjectContactName
    SO_HOA_DON =  fields.Char(string='Số hóa đơn') #InvNo
    NGAY_HOA_DON =  fields.Date(string='Ngày hóa đơn') #InvDate
    TK_NO =  fields.Char(string='Tài khoản nợ') #DebitAccount
    TK_CO =  fields.Char(string='Tài khoản có') #CreditAccount
    DIA_DIEM_KHO =  fields.Char(string='Địa điểm kho') #StockDescription
    TEN_KHO =  fields.Char(string='Tên kho') #StockName
    SO_CT_GOC_KEM_THEO =  fields.Integer(string='Số chứng từ kèm theo') #DocumentIncluded

    
    LOAI_KHACH_HANG =  fields.Integer(string='Loại đối tượng') #AccountObjectType
    
    DIEN_GIAI_THEO_SO_HOA_DON =  fields.Char(string='Diễn giải theo số hóa đơn') 

    TONG_TIEN =  fields.Monetary(string='Tổng tiền', currency_field='currency_id')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())

    CHI_TIET_IDS = fields.One2many('bao.cao.01vt.nhap.kho.chi.tiet', 'NHAP_XUAT_ID')
   

class BAO_CAO_01VT_NHAP_KHO_REPORT(models.AbstractModel):
    _name = 'report.bao_cao.template_01_vt'

    @api.model
    def get_report_values(self, docids, data=None):
        ############### START SQL lấy dữ liệu ###############
        refTypeList, records = self.get_reftype_list(data)
        
        query = """
        DO LANGUAGE plpgsql $$
DECLARE

    ListRefID                     VARCHAR := N'""" + refTypeList + """';

    rec                          RECORD;


    CONG_GOP_DON_GIA_DVT_MA_HANG BOOLEAN:=False;

    LOAI_TIEN_CHINH              INT;




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

    SELECT value
    INTO CONG_GOP_DON_GIA_DVT_MA_HANG
    FROM ir_config_parameter
    WHERE key = 'he_thong.CONG_GOP_DON_GIA_DVT_MA_HANG'
    FETCH FIRST 1 ROW ONLY
    ;

    SELECT value
    INTO LOAI_TIEN_CHINH
    FROM ir_config_parameter
    WHERE key = 'he_thong.LOAI_TIEN_CHINH'
    FETCH FIRST 1 ROW ONLY
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA
    (
        "ID_CHUNG_TU"            INT,
         "MODEL_CHUNG_TU"         VARCHAR(256),
        "NGAY_CHUNG_TU"          TIMESTAMP,
        "NGAY_HACH_TOAN"         TIMESTAMP,
        "SO_CHUNG_TU"            VARCHAR(255),
        "TEN_KHACH_HANG"         VARCHAR(256),
        "TEN_KHACH_HANG_HOA_DON" VARCHAR(256),
        "NGUOI_GIAO_HANG"        VARCHAR(256),
        "SO_HOA_DON"             VARCHAR,
        "NGAY_HOA_DON"           TIMESTAMP,
        "MA_HANG"                VARCHAR(255),
        "TEN_HANG"               VARCHAR(255),
        "DVT"                    VARCHAR(255),
        "TK_NO"                  VARCHAR,
        "TK_CO"                  VARCHAR,
        "TEN_KHO"                VARCHAR,
        "DIA_DIEM_KHO"           VARCHAR(256),
        "SO_LUONG"               DECIMAL(25, 8),
        "DON_GIA"                DECIMAL(25, 8),
        "SO_TIEN"                DECIMAL(25, 8),
        "SO_CT_GOC_KEM_THEO"     VARCHAR(255),
        "LOAI_KHACH_HANG"        VARCHAR(255),
        "LOAI_TIEN"              VARCHAR(255),
        "SortOrder"              INT,
        "MasterSortOrder"        INT

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

        IF rec."LOAI_CHUNG_TU" = ANY ('{2010,2011,2012,2013,2014,2015,2016,2017}' :: INT [])

        THEN
            INSERT INTO TMP_KET_QUA

                SELECT
                    P."id"
                    ,'stock.ex.nhap.xuat.kho' AS "MODEL_CHUNG_TU"
                    , P."NGAY_CHUNG_TU"
                    , P."NGAY_HACH_TOAN"
                    , P."SO_CHUNG_TU"
                    , P."TEN_NGUOI_GIAO_HANG"
                    , CASE WHEN P."LOAI_CHUNG_TU" = 2013

                    THEN
                        COALESCE(PU."TEN_NHA_CUNG_CAP", '')
                      ELSE NULL END                 AS "TEN_KHACH_HANG_HOA_DON"
                    , P."NGUOI_GIAO_HANG_TEXT"
                    , CASE WHEN P."LOAI_CHUNG_TU" = 2013
                    THEN PU."SO_HOA_DON"
                      ELSE NULL END                 AS "SO_HOA_DON"
                    , CASE WHEN P."LOAI_CHUNG_TU" = 2013
                    THEN PU."NGAY_HOA_DON"
                      ELSE NULL END                 AS "NGAY_HOA_DON"
                    , I."MA"
                    , CASE WHEN CONG_GOP_DON_GIA_DVT_MA_HANG = TRUE
                    THEN I."TEN"
                      ELSE PD."TEN_HANG"
                      END
                    , U."DON_VI_TINH"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PD."TK_NO_ID") AS "TK_NO"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PD."TK_CO_ID") AS "TK_CO"

                    , S."TEN_KHO"
                    , S."DIA_CHI"
                    , PD."SO_LUONG"
                    , CASE WHEN P."LOAI_CHUNG_TU" = 2017
                                AND COALESCE(P."currency_id",
                                             0) <> LOAI_TIEN_CHINH
                    THEN CASE
                         WHEN PD."SO_LUONG" <> 0
                             THEN PD."TIEN_VON_QUY_DOI"
                                  / PD."SO_LUONG"
                         ELSE 0
                         END
                      ELSE PD."DON_GIA_VON"
                      END
                    , PD."TIEN_VON_QUY_DOI"
                    , P."KEM_THEO_CHUNG_TU_GOC"
                      , A."LOAI_KHACH_HANG"
                       , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency TK
                       WHERE TK.id = P."currency_id") AS "LOAI_TIEN"
                    , PD."THU_TU_SAP_XEP_CHI_TIET"
                    , F."STT"


                FROM stock_ex_nhap_xuat_kho P
                    INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet PD ON P."id" = PD."NHAP_XUAT_ID"

                    LEFT JOIN sale_ex_tra_lai_hang_ban SAR ON SAR."id" = P."LAP_TU_HANG_BAN_TRA_LAI"
                    INNER JOIN TMP_PARAM F ON F."ID_CHUNG_TU" = P."id" AND F."LOAI_CHUNG_TU" = P."LOAI_CHUNG_TU"

                    LEFT JOIN purchase_ex_hoa_don_mua_hang PU ON PU."id" = SAR."HOA_DON_MUA_HANG_ID"
                    LEFT JOIN danh_muc_kho S ON PD."KHO_ID" = S."id"
                    LEFT JOIN res_partner A ON p."DOI_TUONG_ID" = A."id"
                    --Lấy bổ sung thông tin phiếu xuất
                    LEFT JOIN res_partner AS E ON P."NHAN_VIEN_ID" = E."id"
                    LEFT JOIN danh_muc_to_chuc OU ON E."DON_VI_ID" = OU."id"
                    LEFT JOIN stock_ex_lenh_san_xuat PO ON PD."LENH_SAN_XUAT_ID" = PO."id"
                    LEFT JOIN danh_muc_khoan_muc_cp EI ON PD."KHOAN_MUC_CP_ID" = ei."id"
                    LEFT JOIN danh_muc_doi_tuong_tap_hop_chi_phi J ON PD."DOI_TUONG_THCP_ID" = J."id"
                    LEFT JOIN danh_muc_cong_trinh PW ON PD."CONG_TRINH_ID" = PW."id"
                    LEFT JOIN sale_ex_hop_dong_ban C ON C."id" = PD."HOP_DONG_BAN_ID"
                    LEFT JOIN danh_muc_ma_thong_ke LI ON PD."MA_THONG_KE_ID" = LI."id"
                    LEFT JOIN account_ex_don_dat_hang SAO ON SAO."id" = PD."DON_DAT_HANG_ID"

                    LEFT JOIN danh_muc_vat_tu_hang_hoa I ON PD."MA_HANG_ID" = I."id"
                    LEFT JOIN danh_muc_don_vi_tinh U ON PD."DVT_ID" = U."id"

                    LEFT JOIN purchase_ex_hop_dong_mua_hang PUC ON PD."HOP_DONG_MUA_ID" = PUC."id"
                WHERE I."TINH_CHAT" <> '2'
                      AND F."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      F."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;


        END IF
    ;

        IF rec."LOAI_CHUNG_TU" = ANY
           ('{302,307,308,309,310,312,313,314,315,316,318,319,320,321,322,324,325,326,327,328,352,357,358,359,360,362,363,364,365,366,368,369,370,371,372,374,375,376,377,378}' :: INT [])

        THEN

            INSERT INTO TMP_KET_QUA
                SELECT
                    P."id"
                      ,'purchase.document' AS "MODEL_CHUNG_TU"
                    , P."NGAY_CHUNG_TU"
                    , P."NGAY_HACH_TOAN"
                    , P."SO_PHIEU_NHAP"
                    , P."TEN_DOI_TUONG"
                    , CASE WHEN P."LA_PHIEU_MUA_HANG" = FALSE
                    THEN COALESCE(PU."TEN_NHA_CUNG_CAP",
                                  '')
                      WHEN COALESCE(PU."TEN_NHA_CUNG_CAP",
                                    '') <> ''
                          THEN PU."TEN_NHA_CUNG_CAP"
                      ELSE (SELECT DT."TEN_NCC"
                            FROM purchase_document_line AS DT
                                LEFT JOIN danh_muc_vat_tu_hang_hoa
                                    AS II ON DT."MA_HANG_ID" = II."id"
                            WHERE DT."order_id" = P."id"
                                  AND II."TINH_CHAT" <> '2'
                                  AND COALESCE(DT."TEN_NCC",
                                               '') <> ''
                            ORDER BY DT."THU_TU_SAP_XEP_CHI_TIET"
                            LIMIT 1
                      )
                      END                           AS "TEN_KHACH_HANG_HOA_DON"
                    , P."NGUOI_GIAO_HANG"
                    , CASE WHEN P."LA_PHIEU_MUA_HANG" = FALSE
                    THEN PU."SO_HOA_DON"
                      ELSE lay_ds_so_hoa_don_ban_hang(P."id")
                      END                           AS "SO_HOA_DON"
                    ,
                    CASE WHEN P."LA_PHIEU_MUA_HANG" = FALSE
                    THEN PU."NGAY_HOA_DON"
                      ELSE (SELECT DT."NGAY_HOA_DON"
                            FROM purchase_document_line AS DT
                                LEFT JOIN danh_muc_vat_tu_hang_hoa
                                    AS II ON DT."MA_HANG_ID" = II."id"
                            WHERE DT."order_id" = P."id"
                                  AND II."TINH_CHAT" <> '2'
                                  AND DT."NGAY_HOA_DON" IS NOT NULL
                            ORDER BY DT."THU_TU_SAP_XEP_CHI_TIET"
                            LIMIT 1
                      )
                      END                           AS "NGAY_HOA_DON"
                    , I."MA"
                    , CASE WHEN CONG_GOP_DON_GIA_DVT_MA_HANG = TRUE
                    THEN I."TEN"
                      ELSE PD."name"
                      END
                    , U."DON_VI_TINH"

                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PD."TK_NO_ID") AS "TK_NO"
                    , (SELECT "SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = PD."TK_CO_ID") AS "TK_CO"
                    , S."TEN_KHO"
                    , S."DIA_CHI"
                    , PD."SO_LUONG"
                    , CASE WHEN COALESCE(PD."SO_LUONG", 0) <> 0
                    THEN PD."GIA_TRI_NHAP_KHO"
                         / PD."SO_LUONG"
                      ELSE 0
                      END
                    , PD."GIA_TRI_NHAP_KHO"
                    , P."KEM_THEO"
                      , A."LOAI_KHACH_HANG"
                       , (SELECT "MA_LOAI_TIEN"
                       FROM res_currency TK
                       WHERE TK.id = P."currency_id") AS "LOAI_TIEN"
                    , PD."THU_TU_SAP_XEP_CHI_TIET"
                    , F."STT"


                FROM purchase_document P
                    INNER JOIN purchase_document_line PD ON P."id" = PD."order_id"
                    INNER JOIN TMP_PARAM F ON F."ID_CHUNG_TU" = P."id" AND F."LOAI_CHUNG_TU" = P."LOAI_CHUNG_TU"
                    LEFT JOIN purchase_ex_hoa_don_mua_hang PU ON P."HOA_DON_MUA_HANG_ID" = PU."id"
                    LEFT JOIN danh_muc_kho S ON PD."KHO_ID" = S."id"
                    LEFT JOIN res_partner A ON p."DOI_TUONG_ID" = A."id"
                    --Lấy bổ sung thông tin phiếu xuất
                    LEFT JOIN res_partner AS E ON P."NHAN_VIEN_ID" = E."id"
                    LEFT JOIN danh_muc_to_chuc OU ON E."DON_VI_ID" = OU."id"
                    LEFT JOIN stock_ex_lenh_san_xuat PO ON PD."LENH_SAN_XUAT_ID" = PO."id"
                    LEFT JOIN danh_muc_khoan_muc_cp EI ON PD."KHOAN_MUC_CP_ID" = ei."id"
                    LEFT JOIN danh_muc_doi_tuong_tap_hop_chi_phi J ON PD."DOI_TUONG_THCP_ID" = J."id"
                    LEFT JOIN danh_muc_cong_trinh PW ON PD."CONG_TRINH_ID" = PW."id"
                    LEFT JOIN sale_ex_hop_dong_ban C ON C."id" = PD."HOP_DONG_BAN_ID"
                    LEFT JOIN danh_muc_ma_thong_ke LI ON pd."MA_THONG_KE_ID" = LI."id"
                    LEFT JOIN account_ex_don_dat_hang SAO ON PD."DON_DAT_HANG_ID" = SAO."id"
                    LEFT JOIN purchase_ex_don_mua_hang_chi_tiet PUOD ON PUOD."id" = PD."CHI_TIET_DON_MUA_HANG_ID"

                    LEFT JOIN danh_muc_vat_tu_hang_hoa I ON PD."MA_HANG_ID" = I."id"
                    LEFT JOIN danh_muc_don_vi_tinh U ON PD."DVT_ID" = U."id"

                    LEFT JOIN purchase_ex_hop_dong_mua_hang PUC ON PD."HOP_DONG_MUA_ID" = PUC."id"
                    LEFT JOIN danh_muc_nhom_hhdv PP ON PP."id" = PD."NHOM_HHDV_ID"
                    LEFT JOIN purchase_ex_don_mua_hang PUO ON PUO."id" = PD."DON_MUA_HANG_ID"
                WHERE I."TINH_CHAT" <> '2' AND F."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      F."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"

            ;

        END IF
    ;

    END LOOP
    ;


    IF CONG_GOP_DON_GIA_DVT_MA_HANG = TRUE
    THEN


        UPDATE TMP_KET_QUA R
        SET
            "TK_NO"   = R3."TK_NO",
            "TK_CO"   = R3."TK_CO",
            "TEN_KHO" = R3."TEN_KHO"
        FROM (

                 SELECT
                  "ID_CHUNG_TU"
                     ,"MODEL_CHUNG_TU"
                  , (select string_agg("TK_NO", ', ') FROM
                     (SELECT DISTINCT
                                    R2."TK_NO"
                               FROM TMP_KET_QUA AS R2
                               WHERE R2."ID_CHUNG_TU" = R1."ID_CHUNG_TU"
                                    AND  R2."MODEL_CHUNG_TU" = R1."MODEL_CHUNG_TU"
                    ) a ) AS "TK_NO"

                  , (select string_agg("TK_CO", ', ') FROM
                     (SELECT DISTINCT
                                    R2."TK_CO"
                               FROM TMP_KET_QUA AS R2
                               WHERE R2."ID_CHUNG_TU" = R1."ID_CHUNG_TU"
                                    AND  R2."MODEL_CHUNG_TU" = R1."MODEL_CHUNG_TU"
                    ) a ) AS "TK_CO"
                  , (select string_agg("TEN_KHO", ', ') FROM
                     (SELECT DISTINCT
                                    R2."TEN_KHO"
                               FROM TMP_KET_QUA AS R2
                               WHERE R2."ID_CHUNG_TU" = R1."ID_CHUNG_TU"
                                    AND  R2."MODEL_CHUNG_TU" = R1."MODEL_CHUNG_TU"
                    ) a ) AS "TEN_KHO"


              FROM TMP_KET_QUA AS R1

             ) R3
        WHERE R."ID_CHUNG_TU" = R3."ID_CHUNG_TU"
                AND  R."MODEL_CHUNG_TU" = R3."MODEL_CHUNG_TU"
        ;


    END IF
    ;


    IF CONG_GOP_DON_GIA_DVT_MA_HANG = FALSE
    THEN

        DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
        ;

        CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
            AS
                SELECT
                    ROW_NUMBER()
                  OVER (
                      ORDER BY "MasterSortOrder", MIN("SortOrder") )  AS "RowNumber"
                    ,"ID_CHUNG_TU"
                    ,"MODEL_CHUNG_TU"
                    , "NGAY_CHUNG_TU"
                    , "NGAY_HACH_TOAN"
                    , "SO_CHUNG_TU"
                    , "TEN_KHACH_HANG"
                    , "TEN_KHACH_HANG_HOA_DON"
                    , "NGUOI_GIAO_HANG"
                    , "SO_HOA_DON"
                    , "NGAY_HOA_DON"
                    , "MA_HANG"
                    , "TEN_HANG"
                    , "DVT"
                    , "TK_NO"
                                             "TK_CO"
                    , "TEN_KHO"
                    , MAX("DIA_DIEM_KHO") AS "DIA_DIEM_KHO"
                    , SUM("SO_LUONG")     AS "SO_LUONG"
                    , "DON_GIA"
                    , SUM("SO_TIEN")      AS "SO_TIEN"
                    , "SO_CT_GOC_KEM_THEO"
                      , "LOAI_KHACH_HANG"
                       , "LOAI_TIEN"
                    , MIN("SortOrder")    AS "SortOrder"
                    , "MasterSortOrder"

                FROM TMP_KET_QUA
                GROUP BY
                    "ID_CHUNG_TU",
                    "MODEL_CHUNG_TU",
                    "NGAY_CHUNG_TU",
                    "NGAY_HACH_TOAN",
                    "SO_CHUNG_TU",
                    "TEN_KHACH_HANG",
                    "TEN_KHACH_HANG_HOA_DON",
                    "NGUOI_GIAO_HANG",
                    "SO_HOA_DON",
                    "NGAY_HOA_DON",
                    "MA_HANG",
                    "TEN_HANG",
                    "DVT",
                    "TK_NO",
                    "TK_CO",
                    "TEN_KHO",

                    "DON_GIA",
                    "SO_CT_GOC_KEM_THEO",
                      "LOAI_KHACH_HANG"
                       , "LOAI_TIEN"
                    , "MasterSortOrder"
                ORDER BY "MasterSortOrder",
                    MIN("SortOrder")
        ;


    ELSE
        DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
        ;

        CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
            AS
               SELECT
                       ROW_NUMBER()
                  OVER (
                      ORDER BY ( "MasterSortOrder","SortOrder") )  AS "RowNumber"
                   , R.*
                FROM TMP_KET_QUA R
                ORDER BY
                    "MasterSortOrder",
                    "SortOrder"
        ;

    END IF
    ;

END $$

;


SELECT *
FROM TMP_KET_QUA_CUOI_CUNG
ORDER BY
   "RowNumber"

;
        """
        sql_result = self.execute(query)

        dic_tk_no  = {}
        dic_tk_co  = {}
        dic_kho  = {}

        # Tạo object để in
        for line in sql_result:
            key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))

            if key not in dic_tk_no:
                    dic_tk_no[key] = []
            if key not in dic_tk_co:
                dic_tk_co[key] = []
            
            if key not in dic_kho:
                dic_kho[key] = []

            if line.get('TK_NO') and line.get('TK_NO') not in dic_tk_no[key]:
                dic_tk_no[key] += [line.get('TK_NO')]

            if line.get('TK_CO') and line.get('TK_CO') not in dic_tk_co[key]:
                dic_tk_co[key] += [line.get('TK_CO')]

            
            if line.get('TEN_KHO') and line.get('TEN_KHO') not in dic_kho[key]:
                dic_kho[key] += [line.get('TEN_KHO')]

            master_data = self.env['bao.cao.01vt.nhap.kho'].convert_for_update(line)
            detail_data = self.env['bao.cao.01vt.nhap.kho.chi.tiet'].convert_for_update(line)
            if records.get(key):
                records[key].update(master_data)
                records[key].CHI_TIET_IDS += self.env['bao.cao.01vt.nhap.kho.chi.tiet'].new(detail_data)
        
        for key in records:
            if key in dic_tk_no:
                records[key].TK_NO = ', '.join(dic_tk_no[key])
            if key in dic_tk_co:
                records[key].TK_CO = ', '.join(dic_tk_co[key])

            if key in dic_kho:
                records[key].TEN_KHO = ', '.join(dic_kho[key])

        docs = [records.get(k) for k in records]
        for record in docs:

            strTenKhachHang = ''
            if record.TEN_KHACH_HANG == False:
                record.TEN_KHACH_HANG = ''
            if record.NGUOI_GIAO_HANG == False:
                record.NGUOI_GIAO_HANG = ''
            if record.TEN_KHACH_HANG != '' and record.NGUOI_GIAO_HANG != '':
                if record.LOAI_KHACH_HANG == 0:
                    strTenKhachHang = record.NGUOI_GIAO_HANG + ' - ' + record.TEN_KHACH_HANG
                else:
                    strTenKhachHang = record.NGUOI_GIAO_HANG
            else:
                if record.TEN_KHACH_HANG != '':
                    strTenKhachHang = record.TEN_KHACH_HANG
                elif record.NGUOI_GIAO_HANG != '':
                    strTenKhachHang = record.NGUOI_GIAO_HANG
                else:
                    strTenKhachHang = False
            record.TEN_KHACH_HANG  = strTenKhachHang

            strDienGiaiTheoHoaDon = ''
            if record.SO_HOA_DON  == '':
                record.SO_HOA_DON = False
            if record.SO_HOA_DON == False:
                strDienGiaiTheoHoaDon = ' ................'
            else :
                strDienGiaiTheoHoaDon = " " + 'hóa đơn số' + " " + record.SO_HOA_DON
            if not record.NGAY_HOA_DON:
                strDienGiaiTheoHoaDon += " " + 'ngày' + '........ '
            else:
                ngay_hoa_don = record.NGAY_HOA_DON
                strDienGiaiTheoHoaDon += " ngày {2} tháng {1} năm {0}".format(*ngay_hoa_don.split('-'))
            if not record.TEN_KHACH_HANG_HOA_DON :
                strDienGiaiTheoHoaDon += " " + 'của' + ' .....................................................'
            else:
                strDienGiaiTheoHoaDon += " " + 'của' + " " + record.TEN_KHACH_HANG_HOA_DON
            record.DIEN_GIAI_THEO_SO_HOA_DON = strDienGiaiTheoHoaDon

            tong_tien = 0
            if record.CHI_TIET_IDS:
                for line in record.CHI_TIET_IDS:
                    tong_tien +=  line.SO_TIEN
            record.TONG_TIEN = tong_tien

            if record.DIA_DIEM_KHO == '\n':
                record.DIA_DIEM_KHO = False
            record.currency_id = self.lay_loai_tien_mac_dinh()
        return {
            'docs': docs,
        }
        ####################### END SQL #######################

        

    @api.model_cr
    def init(self):
        self.env.cr.execute(""" 
		DROP FUNCTION IF EXISTS LAY_DS_SO_HOA_DON_BAN_HANG( IN ID_CHUNG_TU INT ) --Func_PU_GetListInvoiceForPULotVoucher
		;

		CREATE OR REPLACE FUNCTION LAY_DS_SO_HOA_DON_BAN_HANG(IN ID_CHUNG_TU INT)
			RETURNS VARCHAR
		AS $$
		DECLARE
			v_Result VARCHAR;

			rec      RECORD;

		BEGIN
			FOR rec IN

			SELECT DISTINCT PUD."SO_HOA_DON_DETAIL"
			FROM purchase_document_line PUD
			WHERE PUD."order_id" = ID_CHUNG_TU AND coalesce(PUD."SO_HOA_DON_DETAIL", '') <> REPEAT(' ', 0)
			LOOP


				SELECT (CASE WHEN coalesce(v_Result, '') = REPEAT(' ', 0)
					THEN ''
						ELSE coalesce(v_Result, '') || ', ' END) || rec."SO_HOA_DON_DETAIL"
				INTO v_Result

			;


			END LOOP
			;

			RETURN v_Result
			;

		END
		;
		$$ LANGUAGE PLpgSQL
		;

		



		""")
