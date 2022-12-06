# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_NHAP_XUAT_KHO(models.Model):
    _name = 'bao.cao.nhap.xuat.kho'
    _auto = False

    ref = fields.Char(string='Reffence ID')
   
    ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
    LOAI_CHUNG_TU =  fields.Integer(string='Loại chứng từ') #RefType
    LOAI_KHACH_HANG =  fields.Integer(string='Loại đối tượng') #AccountObjectType
    MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')
    ID_CHUNG_TU_CHI_TIET =  fields.Integer(string='ID chứng từ chi tiết')
    NGAY_CHUNG_TU =  fields.Date(string='Ngày chứng từ')
    SO_CHUNG_TU =  fields.Char(string='Số chứng từ')
    TEN_KHACH_HANG =  fields.Char(string='Tên khách hàng')
    TEN_NGUOI_NHAN_NOP =  fields.Char(string='Tên người nhận nộp')
    DIA_CHI =  fields.Char(string='Địa chỉ')
    DIEN_GIAI =  fields.Char(string='Diễn giải')
    LIST_TK_KHO =  fields.Char(string='Danh sách tài khoản kho')
    LIST_TK_NO =  fields.Char(string='Danh sách tài khoản nợ')
    LIST_TK_CO =  fields.Char(string='Danh sách tài khoản có')
    DIA_DIEM_KHO =  fields.Char(string='Địa điểm kho')
    SO_CT_GOC_KEM_THEO =  fields.Integer(string='Số chứng từ kèm theo')
    STT =  fields.Integer(string='Số thứ tự')
    TONG_TIEN =  fields.Monetary(string='Tổng tiền', currency_field='currency_id')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    NGUOI_NHAN_HANG =  fields.Char(string='Người nhận hàng')
    CHI_TIET_IDS = fields.One2many('bao.cao.nhap.xuat.kho.chi.tiet', 'NHAP_XUAT_ID')



class BAO_CAO_02_VT_PHIEU_XUAT_KHO(models.AbstractModel):
    _name = 'report.bao_cao.template_02_vt'

    @api.model
    def get_report_values(self, docids, data=None):
        ############### START SQL lấy dữ liệu ###############
        refTypeList, records = self.get_reftype_list(data,'stock.ex.nhap.xuat.kho')
        
        # env = self.self.env['Ten.bang']
        sql_result = self.ham_lay_du_lieu_sql(refTypeList)
        ####################### END SQL #######################

        # Tạo object để in
        for line in sql_result:
            key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
            master_data = self.env['bao.cao.nhap.xuat.kho'].convert_for_update(line)
            detail_data = self.env['bao.cao.nhap.xuat.kho.chi.tiet'].convert_for_update(line)
            if records.get(key):
                records[key].update(master_data)
                records[key].CHI_TIET_IDS += self.env['bao.cao.nhap.xuat.kho.chi.tiet'].new(detail_data)
        
        docs = [records.get(k) for k in records]
        for record in docs:
            if record.LIST_TK_CO:
                if len(record.LIST_TK_CO) > 2 :
                    record.LIST_TK_CO = record.LIST_TK_CO[0 : len(record.LIST_TK_CO) - 2]

            if record.LIST_TK_NO:
                if len(record.LIST_TK_NO) > 2 :
                    record.LIST_TK_NO = record.LIST_TK_NO[0 : len(record.LIST_TK_NO) - 2]

            if record.LIST_TK_KHO:
                if len(record.LIST_TK_KHO) > 2 :
                    record.LIST_TK_KHO = record.LIST_TK_KHO[0 : len(record.LIST_TK_KHO) - 2]

            if record.DIA_DIEM_KHO == '\n':
                record.DIA_DIEM_KHO = False

            if record.LOAI_CHUNG_TU == 2023 or record.LOAI_CHUNG_TU == 2024 or  record.LOAI_CHUNG_TU == 2025: 
                record.NGUOI_NHAN_HANG = record.TEN_KHACH_HANG
            else:
                record.NGUOI_NHAN_HANG = record.TEN_NGUOI_NHAN_NOP

            strTenKhachHang = ''

            if record.TEN_KHACH_HANG == False:
                record.TEN_KHACH_HANG = ''
            if record.TEN_NGUOI_NHAN_NOP == False:
                record.TEN_NGUOI_NHAN_NOP = ''
            if record.TEN_KHACH_HANG != '' and record.TEN_NGUOI_NHAN_NOP != '':
                if record.LOAI_KHACH_HANG == 0:
                    strTenKhachHang = record.TEN_NGUOI_NHAN_NOP + ' - ' + record.TEN_KHACH_HANG
                else:
                    strTenKhachHang = record.TEN_NGUOI_NHAN_NOP
            else:
                if record.TEN_KHACH_HANG != '':
                    strTenKhachHang = record.TEN_KHACH_HANG
                elif record.TEN_NGUOI_NHAN_NOP != '':
                    strTenKhachHang = record.TEN_NGUOI_NHAN_NOP
                else:
                    strTenKhachHang = False
            record.TEN_KHACH_HANG  = strTenKhachHang


            tong_tien = 0
            if record.CHI_TIET_IDS:
                for line in record.CHI_TIET_IDS:
                    tong_tien +=  line.SO_TIEN
            record.TONG_TIEN = tong_tien
            record.currency_id = self.lay_loai_tien_mac_dinh()
        return {
            'docs': docs,
        }

    def ham_lay_du_lieu_sql(self,refTypeList):
        query = """
        DO LANGUAGE plpgsql $$
DECLARE

    ListRefID                            VARCHAR := N'""" + refTypeList + """';

    PrintOutwardWithUnitType             INT := -1;


    rec                                  RECORD;

    rec_2                                RECORD;

    CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO BOOLEAN:=False;

    LOAI_TIEN_CHINH                      INT;

    PHAN_THAP_PHAN_DON_GIA               INT;

    PHAN_THAP_PHAN_SO_LUONG              INT;

    LIST_KHO                             VARCHAR :='';

    LIST_TK_NO                           VARCHAR :='';

    LIST_TK_CO                           VARCHAR :='';

    DIA_DIEM_KHO                         VARCHAR :='';


BEGIN


    SELECT value
    INTO CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO
    FROM ir_config_parameter
    WHERE key = 'he_thong.CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO'
    FETCH FIRST 1 ROW ONLY
    ;


    SELECT value
    INTO LOAI_TIEN_CHINH
    FROM ir_config_parameter
    WHERE key = 'he_thong.LOAI_TIEN_CHINH'
    FETCH FIRST 1 ROW ONLY
    ;


    SELECT value
    INTO PHAN_THAP_PHAN_DON_GIA
    FROM ir_config_parameter
    WHERE key = 'he_thong.PHAN_THAP_PHAN_DON_GIA'
    FETCH FIRST 1 ROW ONLY
    ;

    SELECT value
    INTO PHAN_THAP_PHAN_SO_LUONG
    FROM ir_config_parameter
    WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
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

            Value1
            , Value2


        FROM CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(ListRefID, ',', ';') F
            INNER JOIN danh_muc_reftype R ON F.Value2 = R."REFTYPE"
    ;

    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA
    (
        "ID_CHUNG_TU"          INT,
         "MODEL_CHUNG_TU"         VARCHAR(255),
        "ID_CHUNG_TU_CHI_TIET" INT,
        "NGAY_CHUNG_TU"        TIMESTAMP,
        "SO_CHUNG_TU"          VARCHAR(255),
        "TEN_KHACH_HANG"       VARCHAR(128),
        "TEN_NGUOI_NHAN_NOP"   VARCHAR(128),
        "DIA_CHI"              VARCHAR(255),
        "DIEN_GIAI"            VARCHAR(255),
        "MA_HANG"              VARCHAR(255),
        "TEN_HANG"             VARCHAR(255),
        "DVT"                  VARCHAR(255),
        "TK_NO"                VARCHAR(255),
        "TK_CO"                VARCHAR(255),
        "MA_KHO_ID"            INT,
        "TEN_KHO"              VARCHAR(128),
        "LIST_TK_NO"           VARCHAR,
        "LIST_TK_CO"           VARCHAR,
        "LIST_TK_KHO"          VARCHAR,
        "DIA_DIEM_KHO"         VARCHAR(255),
        "SO_LUONG"             DECIMAL(22, 8),
        "SO_LUONG_YEU_CAU"     DECIMAL(22, 8),
        "DON_GIA"              DECIMAL(22, 8),
        "SO_TIEN"              DECIMAL(22, 8),
        "SO_CT_GOC_KEM_THEO"   VARCHAR(255),
        "STT"                  INT,
        "SO_LUONG_DVT_CHINH"   DECIMAL(22, 8),
        "DON_GIA_DVT_CHINH"    DECIMAL(22, 8),
        "DVT_ID"               INT,
         "LOAI_KHACH_HANG"              VARCHAR(128)
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

        IF rec."LOAI_CHUNG_TU" = ANY ('{3030,3031,3032,3033}' :: INT [])

        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                      I."id"                        AS "ID_CHUNG_TU"
                    , 'purchase.ex.tra.lai.hang.mua'                      AS "MODEL_CHUNG_TU"
                    , ID."id"                       AS "ID_CHUNG_TU_CHI_TIET"
                    , I."NGAY_CHUNG_TU"
                    , I."SO_CHUNG_TU"
                    , I."TEN_NHA_CUNG_CAP"
                    , CASE WHEN A."LA_NHAN_VIEN" = TRUE
                    THEN ''
                      ELSE I."NGUOI_NHAN_HANG"
                      END
                    , I."DIA_CHI"
                    , I."DIEN_GIAI"
                    , II."MA"                       AS "MA_HANG"
                    , ID."TEN_HANG"
                    , U."DON_VI_TINH"
                    , (SELECT TK."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = ID."TK_NO_ID") AS "TK_NO"
                    , (SELECT TK."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = ID."TK_CO_ID") AS "TK_CO"
                    , S."id"                        AS "MA_KHO_ID"
                    , S."TEN_KHO"
                    , NULL
                    , NULL
                    , NULL
                    , S."DIA_CHI"
                    , ID."SO_LUONG"
                    , 0 as "SO_LUONG_YEU_CAU"
                    , CASE WHEN I."currency_id" <> LOAI_TIEN_CHINH
                    THEN CAST(ID."THANH_TIEN_QUY_DOI" / ID."SO_LUONG" AS DECIMAL(22,
                    8))
                      ELSE ID."DON_GIA"
                      END                           AS "DON_GIA"
                    , ID."THANH_TIEN_QUY_DOI"
                    , I."KEM_THEO"
                    , P."STT"
                    , ID."SO_LUONG_DVT_CHINH"
                    , ID."DON_GIA_DVT_CHINH"
                    , U."id"                        AS "DVT_ID"
                     , A."LOAI_KHACH_HANG"
                FROM purchase_ex_tra_lai_hang_mua I
                    INNER JOIN purchase_ex_tra_lai_hang_mua_chi_tiet ID ON I."id" = ID."CHUNG_TU_TRA_LAI_HANG_MUA_ID"
                    INNER JOIN TMP_PARAM P ON I."id" = P."ID_CHUNG_TU" AND I."LOAI_CHUNG_TU" = P."LOAI_CHUNG_TU"
                    LEFT JOIN danh_muc_kho S ON ID."KHO_ID" = S."id"
                    LEFT JOIN res_partner A ON I."DOI_TUONG_ID" = A."id"
                    LEFT JOIN res_partner AS E ON I."NHAN_VIEN_ID" = E."id"
                    LEFT JOIN danh_muc_to_chuc OU ON E."DON_VI_ID" = OU."id"
                    LEFT JOIN danh_muc_khoan_muc_cp EI ON ID."KHOAN_MUC_CP_ID" = ei."id"
                    LEFT JOIN danh_muc_doi_tuong_tap_hop_chi_phi J ON ID."DOI_TUONG_THCP_ID" = J."id"
                    LEFT JOIN danh_muc_cong_trinh PW ON ID."CONG_TRINH_ID" = PW."id"
                    LEFT JOIN sale_ex_hop_dong_ban C ON C."id" = ID."HOP_DONG_BAN_ID"
                    LEFT JOIN danh_muc_ma_thong_ke LI ON ID."MA_THONG_KE_ID" = LI."id"
                    LEFT JOIN danh_muc_vat_tu_hang_hoa II ON ID."MA_HANG_ID" = II."id"
                    LEFT JOIN danh_muc_don_vi_tinh U ON ID."DVT_ID" = U."id"
                    LEFT JOIN purchase_ex_hop_dong_mua_hang PUC ON ID."HOP_DONG_MUA_ID" = PUC."id"
                WHERE II."TINH_CHAT" <> '2' AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;

        END IF
    ;

        IF rec."LOAI_CHUNG_TU" = ANY ('{2030,2031,2032,9131}' :: INT [])
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    I."id"
                    ,'stock.ex.nhap.xuat.kho'   AS "MODEL_CHUNG_TU"
                    , ID."id"
                    , I."NGAY_CHUNG_TU"
                    , I."SO_CHUNG_TU"
                    , I."TEN_NGUOI_VAN_CHUYEN"
                    , I."TEN_NGUOI_VAN_CHUYEN"
                    , ''
                    , I."DIEN_GIAI"
                    , II."MA"
                    , ID."TEN_HANG"
                    , U."DON_VI_TINH"
                    , (SELECT TK."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = ID."TK_NO_ID") AS "TK_NO"
                    , (SELECT TK."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = ID."TK_CO_ID") AS "TK_CO"
                    , S."id"
                    , S."TEN_KHO"
                    , NULL
                    , NULL
                    , NULL
                    , S."DIA_CHI"
                    , ID."SO_LUONG"
                    , ID."SO_LUONG_YEU_CAU"
                    , ID."DON_GIA_VON"
                    , ID."TIEN_VON"                 AS "SO_TIEN"
                    , I."KEM_THEO_CHUNG_TU_GOC"
                    , P."STT"
                    , ID."SO_LUONG_THEO_DVT_CHINH"
                    , ID."DON_GIA_DVT_CHINH"
                    , U."id"                        AS "DVT_ID"
                     ,'1'

                FROM stock_ex_nhap_xuat_kho I
                    INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet ID ON I."id" = ID."NHAP_XUAT_ID"

                    INNER JOIN TMP_PARAM P ON I."id" = P."ID_CHUNG_TU" AND I."LOAI_CHUNG_TU" = P."LOAI_CHUNG_TU"
                    LEFT JOIN danh_muc_kho S ON ID."XUAT_TAI_KHO_ID" = S."id"
                    LEFT JOIN danh_muc_vat_tu_hang_hoa II ON ID."MA_HANG_ID" = II."id"
                    LEFT JOIN danh_muc_don_vi_tinh U ON ID."DVT_ID" = U."id"


                WHERE II."TINH_CHAT" <> '2' AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND
                      P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;


        IF rec."LOAI_CHUNG_TU" = ANY ('{2020,2021,2022,2023,2024,2025,2026,2027}' :: INT [])
        THEN
            INSERT INTO TMP_KET_QUA
                SELECT
                    I."id"
                    ,'stock.ex.nhap.xuat.kho'   AS "MODEL_CHUNG_TU"
                    , ID."id"
                    , I."NGAY_CHUNG_TU"

                    , I."SO_CHUNG_TU"
                    , I."TEN_NGUOI_GIAO_HANG"
                    , CASE WHEN A."LA_NHAN_VIEN" = TRUE
                    THEN ''
                      ELSE I."NGUOI_NHAN_TEXT"
                      END
                    , I."DIA_CHI"
                    , I."DIEN_GIAI"
                    , II."MA"
                    , ID."TEN_HANG"
                    , U."DON_VI_TINH"
                    , (SELECT TK."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = ID."TK_NO_ID") AS "TK_NO"
                    , (SELECT TK."SO_TAI_KHOAN"
                       FROM danh_muc_he_thong_tai_khoan TK
                       WHERE TK.id = ID."TK_CO_ID") AS "TK_CO"
                    , S."id"
                    , S."TEN_KHO"
                    , NULL
                    , NULL
                    , NULL
                    , S."DIA_CHI"
                    , ID."SO_LUONG"
                    , ID."SO_LUONG_YEU_CAU"
                    , ID."DON_GIA_VON"              AS "DON_GIA"
                    , ID."TIEN_VON"                 AS "SO_TIEN"
                    , I."KEM_THEO_CHUNG_TU_GOC"
                    , P."STT"
                    , ID."SO_LUONG_THEO_DVT_CHINH"
                    , ID."DON_GIA_DVT_CHINH"
                    , U."id"                        AS "DVT_ID"
                    ,A."LOAI_KHACH_HANG"


                FROM stock_ex_nhap_xuat_kho I
                    INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet ID ON I."id" = ID."NHAP_XUAT_ID"
                    LEFT JOIN res_partner AD ON ID."DOI_TUONG_ID" = AD."id"
                    INNER JOIN TMP_PARAM P ON I."id" = P."ID_CHUNG_TU" AND I."LOAI_CHUNG_TU" = P."LOAI_CHUNG_TU"
                    LEFT JOIN danh_muc_kho S ON ID."KHO_ID" = S."id"
                    LEFT JOIN res_partner A ON I."DOI_TUONG_ID" = A."id"
                    LEFT JOIN res_partner AS E ON I."NHAN_VIEN_ID" = E."id"
                    LEFT JOIN danh_muc_to_chuc OU ON E."DON_VI_ID" = OU."id"
                    LEFT JOIN stock_ex_lenh_san_xuat PO ON ID."LENH_SAN_XUAT_ID" = PO."id"
                    LEFT JOIN danh_muc_khoan_muc_cp EI ON ID."KHOAN_MUC_CP_ID" = ei."id"
                    LEFT JOIN danh_muc_doi_tuong_tap_hop_chi_phi J ON ID."DOI_TUONG_THCP_ID" = J."id"
                    LEFT JOIN danh_muc_cong_trinh PW ON ID."CONG_TRINH_ID" = PW."id"
                    LEFT JOIN sale_ex_hop_dong_ban C ON C."id" = ID."HOP_DONG_BAN_ID"
                    LEFT JOIN danh_muc_ma_thong_ke LI ON Id."MA_THONG_KE_ID" = LI."id"

                    LEFT JOIN (SELECT
                                     SAOD."id"            AS "DON_DAT_HANG_ID_CHI_TIET"
                                   , SAO."id"             AS "DON_DAT_HANG_ID"
                                   , SAO."SO_DON_HANG"
                                   , SUM(SAOD."SO_LUONG") AS "SO_LUONG"

                               FROM account_ex_don_dat_hang_chi_tiet
                                   AS SAOD
                                   INNER JOIN account_ex_don_dat_hang
                                       AS SAO ON SAOD."DON_DAT_HANG_CHI_TIET_ID" = SAO."id"
                               GROUP BY SAOD."id",
                                   SAO."id",
                                   SAO."SO_DON_HANG"
                              ) AS TempSAOBH ON ID."DON_DAT_HANG_ID" = TempSAOBH."DON_DAT_HANG_ID"
                                                AND (I."LOAI_CHUNG_TU" = '2020'
                                                     AND TempSAOBH."DON_DAT_HANG_ID_CHI_TIET" = ID.id
                                                )
                    LEFT JOIN (SELECT
                                   SAO."id"
                                   , SAO."SO_DON_HANG"
                                   , SUM(SAOD."SO_LUONG") AS "SO_LUONG"

                               FROM account_ex_don_dat_hang_chi_tiet
                                   AS SAOD
                                   INNER JOIN account_ex_don_dat_hang
                                       AS SAO ON SAOD."DON_DAT_HANG_CHI_TIET_ID" = SAO."id"
                               GROUP BY SAO."id",
                                   SAO."SO_DON_HANG"
                              ) AS TempSAOSX ON ID."DON_DAT_HANG_ID" = TempSAOSX."id"
                                                AND I."LOAI_CHUNG_TU" <> '2020'
                    LEFT JOIN danh_muc_vat_tu_hang_hoa II ON ID."MA_HANG_ID" = II."id"
                    LEFT JOIN danh_muc_don_vi_tinh U ON ID."DVT_ID" = U."id"
                    LEFT JOIN purchase_ex_hop_dong_mua_hang PUC ON ID."HOP_DONG_MUA_ID" = PUC."id"
                WHERE II."TINH_CHAT" <> '2'
                      AND P."ID_CHUNG_TU" = rec."ID_CHUNG_TU" AND P."LOAI_CHUNG_TU" = rec."LOAI_CHUNG_TU"
            ;
        END IF
    ;

    END LOOP
    ;


    FOR rec IN
    SELECT "ID_CHUNG_TU" AS "ID_CHUNG_TU_TEMP"

    FROM TMP_KET_QUA
    --WHERE "SO_CHUNG_TU" = '0122112'
    GROUP BY "ID_CHUNG_TU"

    LOOP


        LIST_KHO = ''
    ;

        LIST_TK_NO = ''
    ;

        LIST_TK_CO = ''
    ;

        DIA_DIEM_KHO = ''
    ;

        FOR rec_2 IN
        SELECT  "MA_KHO_ID",
            "TEN_KHO"
        FROM TMP_KET_QUA
        WHERE "ID_CHUNG_TU" = rec."ID_CHUNG_TU_TEMP"
        GROUP BY
            "MA_KHO_ID",
            "TEN_KHO"
        ORDER BY "TEN_KHO"
        LOOP


            SELECT LIST_KHO
                   || CASE WHEN LTRIM(RTRIM(COALESCE(rec_2."TEN_KHO", ''))) = ''
                THEN ''
                      ELSE rec_2."TEN_KHO" || ', '
                      END
            INTO LIST_KHO

        ;

        END LOOP
    ;


        FOR rec_2 IN
        SELECT "TK_NO"

        FROM TMP_KET_QUA
        WHERE "ID_CHUNG_TU" = rec."ID_CHUNG_TU_TEMP" AND COALESCE("TK_NO", '') <> ''
        GROUP BY "TK_NO"
        ORDER BY "TK_NO"
        LOOP
            SELECT LIST_TK_NO || rec_2."TK_NO"
                   || ', '
            INTO LIST_TK_NO


        ;

        END LOOP
    ;

        FOR rec_2 IN
        SELECT "TK_CO"
        FROM TMP_KET_QUA
        WHERE "ID_CHUNG_TU" = rec."ID_CHUNG_TU_TEMP" AND COALESCE("TK_CO", '') <> ''
        GROUP BY "TK_CO"
        ORDER BY "TK_CO"
        LOOP
            SELECT LIST_TK_CO
                   || rec_2."TK_CO" || ', '
            INTO LIST_TK_CO

        ;

        END LOOP
    ;

        FOR rec_2 IN
        SELECT "DIA_DIEM_KHO"
        FROM TMP_KET_QUA
            WHERE "DIA_DIEM_KHO" IS NOT NULL
                  AND "ID_CHUNG_TU" = rec."ID_CHUNG_TU_TEMP"
            ORDER BY "STT"
            LIMIT 1

        LOOP

            SELECT rec_2."DIA_DIEM_KHO"
            INTO DIA_DIEM_KHO

        ;

        END LOOP
    ;
--
--         RAISE NOTICE '%', LIST_TK_CO
--     ;

        UPDATE TMP_KET_QUA
        SET
            "LIST_TK_CO"   = LIST_TK_CO,
            "LIST_TK_NO"   = LIST_TK_NO,
            "LIST_TK_KHO"  = LIST_KHO,
            "DIA_DIEM_KHO" = DIA_DIEM_KHO

        WHERE "ID_CHUNG_TU" = rec."ID_CHUNG_TU_TEMP"

    ;


    END LOOP
    ;

    DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
    ;

    CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
        AS
            SELECT
                R."ID_CHUNG_TU"
                 ,R."MODEL_CHUNG_TU"
                , CASE WHEN CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO = TRUE
                THEN NULL
                  ELSE R."ID_CHUNG_TU_CHI_TIET"
                  END                                                       AS "ID_CHUNG_TU_CHI_TIET"
                , R."NGAY_CHUNG_TU"
                , R."SO_CHUNG_TU"
                , R."TEN_KHACH_HANG"
                , R."TEN_NGUOI_NHAN_NOP"
                , R."DIA_CHI"
                , R."DIEN_GIAI"
                , R."MA_HANG"
                , R."TEN_HANG"
                , CASE PrintOutwardWithUnitType
                  WHEN -1
                      THEN R."DVT" --Đơn vị trên chứng từ
                  WHEN 0
                      THEN R."DVT" -- Đơn vị chính
                  ELSE COALESCE(U."DON_VI_TINH", R."DVT")
                  END                                                       AS "DVT"
                , --Lấy theo đơn vị chỉ định, nếu không có thì lấy theo đơn vị trên chứng từ
                R."LIST_TK_KHO"
                , R."LIST_TK_NO"
                , R."LIST_TK_CO"
                , R."DIA_DIEM_KHO"
                , ROUND(CAST(SUM(CASE WHEN (PrintOutwardWithUnitType = -1)
                THEN R."SO_LUONG" --Đơn vị trên chứng từ
                                 WHEN (PrintOutwardWithUnitType = 0)
                                     THEN R."SO_LUONG_DVT_CHINH" -- Đơn vị chính
                                 ELSE (CASE WHEN UC."VAT_TU_HANG_HOA_ID" IS NULL
                                                 OR (R."DVT_ID" IS NOT NULL
                                                     AND UC."DVT_ID" IS NOT NULL
                                                     AND R."DVT_ID" = UC."DVT_ID"
                                                 )
                                     THEN R."SO_LUONG"
                                       ELSE --Nếu đơn vị được chọn là đơn vị trên chứng từ và đơn vị của dòng này không phải là đơn vị đang chọn in
                                           (CASE UC."PHEP_TINH_CHUYEN_DOI"
                                            WHEN '*'
                                                THEN R."SO_LUONG_DVT_CHINH"
                                                     / (CASE UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                                                        WHEN 0
                                                            THEN 1
                                                        ELSE UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                                                        END)
                                            ELSE R."SO_LUONG_DVT_CHINH"
                                                 * UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                                            END)
                                       END)
                                 END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SO_LUONG"
                , SUM(R."SO_LUONG_YEU_CAU") as "SO_LUONG_YEU_CAU"
                , ROUND(CAST((CASE WHEN (PrintOutwardWithUnitType = -1)
                THEN R."DON_GIA" --Đơn vị trên chứng từ
                              WHEN (PrintOutwardWithUnitType = 0)
                                  THEN R."DON_GIA_DVT_CHINH" -- Đơn vị chính
                              ELSE (CASE WHEN UC."VAT_TU_HANG_HOA_ID" IS NULL
                                              OR (R."DVT_ID" IS NOT NULL
                                                  AND UC."DVT_ID" IS NOT NULL
                                                  AND R."DVT_ID" = UC."DVT_ID"
                                              )
                                  THEN R."DON_GIA"
                                    ELSE --Nếu đơn vị được chọn là đơn vị trên chứng từ và đơn vị của dòng này không phải là đơn vị đang chọn in
                                        (CASE UC."PHEP_TINH_CHUYEN_DOI"
                                         WHEN '*'
                                             THEN R."DON_GIA_DVT_CHINH"
                                                  * UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                                         ELSE R."DON_GIA_DVT_CHINH"
                                              / (CASE UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                                                 WHEN 0
                                                     THEN 1
                                                 ELSE UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                                                 END)
                                         END)
                                    END)
                              END) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA)     AS "DON_GIA"
                , SUM(R."SO_TIEN")                                          AS "SO_TIEN"
                , R."SO_CT_GOC_KEM_THEO"
                , R."STT"
                ,P."LOAI_CHUNG_TU"
                  , R."LOAI_KHACH_HANG"


            FROM TMP_KET_QUA R
                INNER JOIN TMP_PARAM P ON P."ID_CHUNG_TU" = R."ID_CHUNG_TU"
                INNER JOIN danh_muc_vat_tu_hang_hoa II ON R."MA_HANG" = II."MA"
                LEFT JOIN danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi UC ON UC."VAT_TU_HANG_HOA_ID" = II."id"
                                                                           AND (UC."STT" =
                                                                                PrintOutwardWithUnitType --từ bảng UC lấy tỷ lệ chuyển đổi từ đơn vị tính chính ra đơn vị trên tham số
                                                                           )
                LEFT JOIN danh_muc_don_vi_tinh U ON U."id" = UC."DVT_ID"
            GROUP BY
                R."ID_CHUNG_TU",
                R."MODEL_CHUNG_TU",
                CASE WHEN CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO = TRUE
                    THEN NULL
                ELSE R."ID_CHUNG_TU_CHI_TIET"
                END,
                R."NGAY_CHUNG_TU",

                R."SO_CHUNG_TU",
                R."TEN_KHACH_HANG",
                R."TEN_NGUOI_NHAN_NOP",

                R."DIA_CHI",
                R."DIEN_GIAI",
                R."MA_HANG",
                R."TEN_HANG",

                CASE PrintOutwardWithUnitType
                WHEN -1
                    THEN R."DVT" --Đơn vị trên chứng từ
                WHEN 0
                    THEN R."DVT" -- Đơn vị chính
                ELSE COALESCE(U."DON_VI_TINH", R."DVT")
                END,

                R."LIST_TK_KHO",
                R."LIST_TK_NO",
                R."LIST_TK_CO",
                R."DIA_DIEM_KHO",
                ROUND(CAST((CASE WHEN (PrintOutwardWithUnitType = -1)
                    THEN R."DON_GIA" --Đơn vị trên chứng từ
                            WHEN (PrintOutwardWithUnitType = 0)
                                THEN R."DON_GIA_DVT_CHINH" -- Đơn vị chính
                            ELSE (CASE WHEN UC."VAT_TU_HANG_HOA_ID" IS NULL
                                            OR (R."DVT_ID" IS NOT NULL
                                                AND UC."DVT_ID" IS NOT NULL
                                                AND R."DVT_ID" = UC."DVT_ID"
                                            )
                                THEN R."DON_GIA"
                                  ELSE --Nếu đơn vị được chọn là đơn vị trên chứng từ và đơn vị của dòng này không phải là đơn vị đang chọn in
                                      (CASE UC."PHEP_TINH_CHUYEN_DOI"
                                       WHEN '*'
                                           THEN R."DON_GIA_DVT_CHINH"
                                                * UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                                       ELSE R."DON_GIA_DVT_CHINH"
                                            / (CASE UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                                               WHEN 0
                                                   THEN 1
                                               ELSE UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
                                               END)
                                       END)
                                  END)
                            END) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA),
                R."SO_CT_GOC_KEM_THEO",
                R."STT"
                 ,P."LOAI_CHUNG_TU"
                 , R."LOAI_KHACH_HANG"


            ORDER BY "STT"
    ;


END $$

;


SELECT *
FROM TMP_KET_QUA_CUOI_CUNG
 ORDER BY "STT"
;
        """
        return self.execute(query)


    @api.model_cr
    def init(self):
        self.env.cr.execute(""" 
DROP FUNCTION IF EXISTS CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG( IN v_pListString VARCHAR,
v_SeparateCharacter1 VARCHAR,
v_SeparateCharacter2 VARCHAR )
;

CREATE OR REPLACE FUNCTION CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(IN v_pListString        VARCHAR,
                                                                         v_SeparateCharacter1 VARCHAR,
                                                                         v_SeparateCharacter2 VARCHAR)--Func_Convert_GUID_INT_StringIntoTable
    RETURNS TABLE(
        Value1 INT,
        Value2 INT

    ) AS $$



DECLARE


    v_ValueListLength  INTEGER;

    v_StartingPosition INTEGER;

    v_Value            VARCHAR(100);

    v_SecondPosition   INTEGER;

    v_PositionSplit    INTEGER;

    v_Value1           VARCHAR(127);

    v_Value2           VARCHAR(127);


BEGIN


    DROP TABLE IF EXISTS tt_VALUETABLE CASCADE
    ;

    CREATE TEMPORARY TABLE tt_VALUETABLE
    (
        Value1 INT,
        Value2 INT
    )
    ;

    v_ValueListLength := LENGTH(v_pListString)
    ;

    v_StartingPosition := 1
    ;

    v_Value := REPEAT(' ', 0)
    ;


    WHILE v_StartingPosition < v_ValueListLength LOOP
        v_PositionSplit := 0
    ;

        v_Value1 := REPEAT(' ', 0)
    ;

        v_Value2 := REPEAT(' ', 0)
    ;

        -- Vị trí kế tiếp xuất hiện ký tự phân cách
        v_SecondPosition := CASE WHEN
            POSITION(v_SeparateCharacter1 IN SUBSTRING(v_pListString, v_StartingPosition :: INT + 1)) > 0
            THEN POSITION(v_SeparateCharacter1 IN SUBSTRING(v_pListString, v_StartingPosition :: INT + 1)) +
                 v_StartingPosition :: INT + 1 - 1
                            ELSE 0 END
    ;

        -- Trích ra giá trị từ chuỗi

        v_Value := SUBSTRING(v_pListString, v_StartingPosition :: INT + 1,
                             v_SecondPosition :: INT - v_StartingPosition :: INT - 1)
    ;

        --1 Tìm vị trí của ký tự phân tách 2 giá trị
        v_PositionSplit := CASE WHEN POSITION(v_SeparateCharacter2 IN SUBSTRING(v_Value, v_PositionSplit :: INT + 1)) >
                                     0
            THEN POSITION(v_SeparateCharacter2 IN SUBSTRING(v_Value, v_PositionSplit :: INT + 1)) +
                 v_PositionSplit :: INT + 1 - 1
                           ELSE 0 END
    ;

        --2 Lấy lại giá trị 1, giá trị 2
        v_Value1 := SUBSTRING(v_Value, 1, v_PositionSplit)
    ;

        v_Value2 := SUBSTRING(v_Value, v_PositionSplit :: INT + 1, 100)
    ;

        --100 LA SO FIX CUNG

        -- Thiết lập lại giá trị bắt đầu
        v_StartingPosition := v_SecondPosition
    ;

        IF (v_Value <> REPEAT(' ', 0)
            AND v_Value1 <> REPEAT(' ', 0)
            AND v_Value2 <> REPEAT(' ', 0))
        THEN
            INSERT INTO tt_VALUETABLE (Value1,
                                       Value2)
            VALUES (CAST(SUBSTRING(v_Value1, 1, LENGTH(v_Value1) - 1) AS INT),
                   CAST(v_Value2 as INT))
            ;

        END IF
    ;

    END LOOP
    ;


    RETURN QUERY SELECT *
             FROM tt_VALUETABLE ;
END
;

$$ LANGUAGE PLpgSQL
;

		""")
