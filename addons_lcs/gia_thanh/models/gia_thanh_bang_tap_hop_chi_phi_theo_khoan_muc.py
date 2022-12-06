# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_BANG_TAP_HOP_CHI_PHI_THEO_KHOAN_MUC(models.Model):
    _name = 'gia.thanh.bang.tap.hop.chi.phi.theo.khoan.muc'
    _description = ''
    _auto = False

    KY_TINH_GIA_THANH = fields.Char(string='Kỳ tính giá thành', help='Kỳ tính giá thành')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(GIA_THANH_BANG_TAP_HOP_CHI_PHI_THEO_YEU_TO, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result
    GIA_THANH_BANG_TAP_HOP_CHI_PHI_THEO_KHOAN_MUC_CHI_TIET_IDS = fields.One2many('gia.thanh.bang.tap.hop.chi.phi.theo.khoan.muc.chi.tiet', 'CHI_TIET_ID', string='Bảng tập hợp chi phí theo yếu tố chi tiết')


    def btn_lay_du_lieu_chi_phi_theo_khoan_muc(self, args):
        new_line_chi_phi_theo_khoan_muc = [[5]]
        ky_tinh_gia_thanh_id = args.get('ky_tinh_gia_thanh_id')
        chi_nhanh_id = self.get_chi_nhanh()
        du_lieu_chi_phi_theo_khoan_muc = self.lay_du_lieu_chi_phi_theo_khoan_muc(ky_tinh_gia_thanh_id,chi_nhanh_id)
        if du_lieu_chi_phi_theo_khoan_muc:
            for line in du_lieu_chi_phi_theo_khoan_muc:
                dien_giai = 'Kết chuyển chi phí ' + str(line.get('TK_CO')) + ' của đối tượng ' + str(line.get('TEN_DOI_TUONG_THCP'))
                new_line_chi_phi_theo_khoan_muc += [(0,0,{
							'MA_DOI_TUONG_THCP_ID' : [line.get('DOI_TUONG_THCP_ID'),line.get('MA_DOI_TUONG_THCP')],
							'TEN_DOI_TUONG_THCP' : line.get('TEN_DOI_TUONG_THCP'),
                            'LOAI_DOI_TUONG_THCP' : line.get('LOAI_DOI_TUONG_THCP'),
                            
                            # 'MA_CONG_TRINH_ID' : [line.get('CONG_TRINH_ID'),line.get('MA_CONG_TRINH')],
							# 'TEN_CONG_TRINH' : line.get('TEN_CONG_TRINH'),
                            # 'LOAI_CONG_TRINH' : [line.get('LOAI_CONG_TRINH'),line.get('TEN_LOAI_CONG_TRINH')],

                            # 'SO_DON_HANG_ID' : [line.get('DON_DAT_HANG_ID'),line.get('SO_DON_HANG')],
							# 'NGAY_DON_HANG' : line.get('NGAY_DON_HANG'),
                            # 'KHACH_HANG' : [line.get('KHACH_HANG_ID'),line.get('TEN_KHACH_HANG')],

                            # 'HOP_DONG_BAN_ID' : [line.get('HOP_DONG_ID'),line.get('SO_HOP_DONG')],
							# 'NGAY_KY' : line.get('NGAY_KY'),
                            # 'TRICH_YEU' : line.get('TRICH_YEU'),

							
							'TONG_GIA_THANH' : line.get('TONG_GIA_THANH'),
                            'NGUYEN_VAT_LIEU_DAU_KY' : line.get('DO_DANG_DAU_KY_NGUYEN_VAT_LIEU_TRUC_TIEP'),
                            'NHAN_CONG_DAU_KY' : line.get('DO_DANG_DAU_KY_NHAN_CONG_TRUC_TIEP'),
                            'CHI_PHI_KHAC_DAU_KY' : line.get('DO_DANG_DAU_KY_CHI_PHI_CHUNG'),
                            'TONG_DO_DANG_DAU_KY' : line.get('DO_DANG_DAU_KY_TONG'),
                            'NGUYEN_VAT_LIEU_TRONG_KY' : line.get('NGUYEN_VAT_LIEU_TRUC_TIEP'),
                            'NHAN_CONG_TRONG_KY' : line.get('NHAN_CONG_TRUC_TIEP'),
                            'CHI_PHI_KHAC_TRONG_KY' : line.get('CHI_PHI_CHUNG'),
                            'TONG_PHAT_SINH_TRONG_KY' : line.get('PHAT_SINH_TRONG_KY_TONG'),
                            'KHOAN_GIAM_GIA_THANH' : line.get('KHOAN_GIAM_GIA_THANH'),
                            'NGUYEN_VAT_LIEU_CUOI_KY' : line.get('DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP'),
                            'NHAN_CONG_CUOI_KY' : line.get('DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TEP'),
                            'CHI_PHI_KHAC_CUOI_KY' : line.get('DO_DANG_CUOI_KY_CHI_PHI_CHUNG'),
                            'TONG_DO_DANG_CUOI_KY' : line.get('DO_DANG_CUOI_KY_TONG'),
                            
                            })]
        return {'GIA_THANH_BANG_TAP_HOP_CHI_PHI_THEO_KHOAN_MUC_CHI_TIET_IDS' : new_line_chi_phi_theo_khoan_muc}



    def btn_chi_phi_theo_khoan_muc_ct_dh_hd(self, args):
        new_line_chi_phi_theo_khoan_muc = [[5]]
        ky_tinh_gia_thanh_id = args.get('ky_tinh_gia_thanh_id')
        chi_nhanh_id = self.get_chi_nhanh()
        du_lieu_chi_phi_theo_khoan_muc = self.lay_du_lieu_chi_phi_theo_khoan_muc_ct_dh_hd(ky_tinh_gia_thanh_id,chi_nhanh_id)
        if du_lieu_chi_phi_theo_khoan_muc:
            for line in du_lieu_chi_phi_theo_khoan_muc:
                dien_giai = 'Kết chuyển chi phí ' + str(line.get('TK_CO')) + ' của đối tượng ' + str(line.get('TEN_DOI_TUONG_THCP'))
                new_line_chi_phi_theo_khoan_muc += [(0,0,{
							# 'MA_DOI_TUONG_THCP_ID' : [line.get('DOI_TUONG_THCP_ID'),line.get('MA_DOI_TUONG_THCP')],
							# 'TEN_DOI_TUONG_THCP' : line.get('TEN_DOI_TUONG_THCP'),
                            # 'LOAI_DOI_TUONG_THCP' : line.get('LOAI_DOI_TUONG_THCP'),
                            
                            'MA_CONG_TRINH_ID' : [line.get('CONG_TRINH_ID'),line.get('MA_CONG_TRINH')],
							'TEN_CONG_TRINH' : line.get('TEN_CONG_TRINH'),
                            'LOAI_CONG_TRINH' : line.get('TEN_LOAI_CONG_TRINH'),

                            'SO_DON_HANG_ID' : [line.get('DON_DAT_HANG_ID'),line.get('SO_DON_HANG')],
							'NGAY_DON_HANG' : line.get('NGAY_DON_HANG'),
                            'KHACH_HANG' : line.get('TEN_KHACH_HANG'),

                            'HOP_DONG_BAN_ID' : [line.get('HOP_DONG_ID'),line.get('SO_HOP_DONG')],
							'NGAY_KY' : line.get('NGAY_KY'),
                            'TRICH_YEU' : line.get('TRICH_YEU'),

							
							'LUY_KE_CHI_PHI' : line.get('LUY_KE_CHI_PHI'),
                            'LUY_KE_DA_NGHIEM_THU' : line.get('LUY_KE_DA_NGHIEM_THU'),
                            'SO_CHUA_NGHIEM_THU_DAU_KY' : line.get('SO_CHUA_NGHIEM_THU_DAU_KY'),
                            'SO_CHUA_NGHIEM_THU_CUOI_KY' : line.get('SO_CHUA_NGHIEM_THU_CUOI_KY'),
                            'NGUYEN_VAT_LIEU_DAU_KY' : line.get('LUY_KE_KY_TRUOC_NVL_TRUC_TIEP'),
                            'NHAN_CONG_DAU_KY' : line.get('LUY_KE_KY_TRUOC_NC_TRUC_TIEP'),
                            'MAY_THI_CONG_DAU_KY' : line.get('LUY_KE_KY_TRUOC_MTC'),
                            'CHI_PHI_KHAC_DAU_KY' : line.get('LUY_KE_KY_TRUOC_CP_CHUNG'),
                            'TONG_DO_DANG_DAU_KY' : line.get('LUY_KE_KY_TRUOC_TONG'),
                            'NGUYEN_VAT_LIEU_TRONG_KY' : line.get('PHAT_SINH_NVL_TRUC_TIEP'),
                            'NHAN_CONG_TRONG_KY' : line.get('PHAT_SINH_NHAN_CONG_TRUC_TIEP'),
                            'MAY_THI_CONG_TRONG_KY' : line.get('PHAT_SINH_MAY_THI_CONG'),
                            'CHI_PHI_KHAC_TRONG_KY' : line.get('PHAT_SINH_CHI_PHI_CHUNG'),
                            'TONG_PHAT_SINH_TRONG_KY' : line.get('PHAT_SINH_TONG'),

                            'KHOAN_GIAM_GIA_THANH' : line.get('KHOAN_GIAM_GIA_THANH'),
                            'LUY_KE_NVL_TRUC_TIEP' : line.get('LUY_KE_CP_NVL_TRUC_TIEP'),
                            'LUY_KE_NHAN_CONG_TRUC_TIEP' : line.get('LUY_KE_CP_NC_TRUC_TIEP'),
                            'LUY_KE_MAY_THI_CONG' : line.get('LUY_KE_CP_MAY_THI_CONG'),
                            'LUY_KE_CHI_PHI_CHUNG' : line.get('LUY_KE_CP_CHI_PHI_CHUNG'),
                            'LUY_KE_TONG' : line.get('LUY_KE_CP_TONG'),
                            
                            })]
        return {'GIA_THANH_BANG_TAP_HOP_CHI_PHI_THEO_KHOAN_MUC_CHI_TIET_IDS' : new_line_chi_phi_theo_khoan_muc}


    
    def lay_du_lieu_chi_phi_theo_khoan_muc(self,ky_tinh_gia_thanh_id,chi_nhanh_id):
        params = {
            'KY_TINH_GIA_THANH_ID' : ky_tinh_gia_thanh_id,
            'CHI_NHANH_ID' : chi_nhanh_id,
            }
        query = """  

                DO LANGUAGE plpgsql $$
                DECLARE

                    ky_tinh_gia_thanh_id         INTEGER := %(KY_TINH_GIA_THANH_ID)s;


                    chi_nhanh_id                 INTEGER := %(CHI_NHANH_ID)s;

                    CHE_DO_KE_TOAN               VARCHAR;

                    tu_ngay                      TIMESTAMP;

                    den_ngay                     TIMESTAMP;

                    LOAI_GIA_THANH               VARCHAR;

                    ListJob                      VARCHAR;

                    --Tham số bên misa

                    MA_PHAN_CAP_NVLTT            VARCHAR(100);

                    MA_PHAN_CAP_NCTT             VARCHAR(100);

                    MA_PHAN_CAP_SXC              VARCHAR(100);


                    MA_PHAN_CAP_CPSX             VARCHAR(100);

                    CHI_TIET_THEO_DOI_TUONG_THCP BOOLEAN;


                BEGIN


                    SELECT value
                    INTO CHE_DO_KE_TOAN
                    FROM ir_config_parameter
                    WHERE key = 'he_thong.CHE_DO_KE_TOAN'
                    FETCH FIRST 1 ROW ONLY
                    ;

                    SELECT "TU_NGAY"
                    INTO tu_ngay
                    FROM gia_thanh_ky_tinh_gia_thanh AS JP
                    WHERE "id" = ky_tinh_gia_thanh_id
                    ;

                    SELECT "DEN_NGAY"
                    INTO den_ngay
                    FROM gia_thanh_ky_tinh_gia_thanh AS JP
                    WHERE "id" = ky_tinh_gia_thanh_id
                    ;

                    SELECT "LOAI_GIA_THANH"
                    INTO LOAI_GIA_THANH
                    FROM gia_thanh_ky_tinh_gia_thanh AS JP
                    WHERE "id" = ky_tinh_gia_thanh_id
                    ;

                    --     LOAI_GIA_THANH = '48'
                    --     ;


                    DROP TABLE IF EXISTS TMP_DOI_TUONG_THCP_CON
                    ;

                    CREATE TEMP TABLE TMP_DOI_TUONG_THCP_CON

                    (
                        "DOI_TUONG_THCP_ID"   INT,
                        "MA_DOI_TUONG_THCP"   VARCHAR(25),
                        "TEN_DOI_TUONG_THCP"  VARCHAR(128),
                        "LOAI_DOI_TUONG_THCP" VARCHAR(128),
                        "isparent"            BOOLEAN,
                        "parent_id"           INT,
                        "BAC"                 INT,
                        "MA_PHAN_CAP"         VARCHAR(100)
                    )
                    ;

                    --Bảng Job để lưu Các Job chi tiết nhất: Dùng để lấy dữ liệu
                    INSERT INTO TMP_DOI_TUONG_THCP_CON
                    ("DOI_TUONG_THCP_ID",
                    "MA_DOI_TUONG_THCP",
                    "TEN_DOI_TUONG_THCP",
                    "LOAI_DOI_TUONG_THCP",
                    "isparent",
                    "parent_id",
                    "BAC",
                    "MA_PHAN_CAP"
                    )
                        SELECT
                            J2."id"
                            , J2."MA_DOI_TUONG_THCP"
                            , J2."TEN_DOI_TUONG_THCP"
                            , J2."LOAI"
                            , J2."isparent"
                            , J2."parent_id"
                            , J2."BAC"
                            , J2."MA_PHAN_CAP"
                        FROM gia_thanh_ky_tinh_gia_thanh_chi_tiet AS JPD
                            INNER JOIN danh_muc_doi_tuong_tap_hop_chi_phi AS J ON JPD."MA_DOI_TUONG_THCP_ID" = J."id"
                            INNER JOIN danh_muc_doi_tuong_tap_hop_chi_phi AS J2 ON J2."MA_PHAN_CAP" LIKE J."MA_PHAN_CAP"
                                                                                                        || '%%%%'
                        WHERE "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                    ;

                    --
                    --     SELECT ListJob || CAST("DOI_TUONG_THCP_ID" AS VARCHAR(50)) || ','
                    --     INTO ListJob
                    --     FROM TMP_DOI_TUONG_THCP_CON AS J
                    --     ;

                    DROP TABLE IF EXISTS TMP_DOI_TUONG_THCP
                    ;

                    CREATE TEMP TABLE TMP_DOI_TUONG_THCP


                    (
                        "DOI_TUONG_THCP_ID"   INT,
                        "MA_DOI_TUONG_THCP"   VARCHAR(25),
                        "TEN_DOI_TUONG_THCP"  VARCHAR(128),
                        "LOAI_DOI_TUONG_THCP" VARCHAR(100),
                        "isparent"            BOOLEAN,
                        "parent_id"           INT,
                        "BAC"                 INT,
                        "MA_PHAN_CAP"         VARCHAR(100)
                    )
                    ;

                    INSERT INTO TMP_DOI_TUONG_THCP
                    (
                        "DOI_TUONG_THCP_ID",
                        "MA_DOI_TUONG_THCP",
                        "TEN_DOI_TUONG_THCP",
                        "LOAI_DOI_TUONG_THCP",
                        "isparent",
                        "parent_id",
                        "BAC",
                        "MA_PHAN_CAP"
                    )
                        SELECT
                            J."id"
                            , J."MA_DOI_TUONG_THCP"
                            , J."TEN_DOI_TUONG_THCP"
                            , CASE WHEN j."LOAI" = '0'
                            THEN N'Phân xưởng'
                            WHEN j."LOAI" = '1'
                                THEN N'Sản phẩm'
                            WHEN j."LOAI" = '2'
                                THEN N'Quy trình sản xuất'
                            WHEN j."LOAI" = '3'
                                THEN N'Công đoạn'
                            END AS "LOAI_DOI_TUONG_THCP"
                            , J."isparent"
                            , J."parent_id"
                            , J."BAC"
                            , J."MA_PHAN_CAP"
                        FROM danh_muc_doi_tuong_tap_hop_chi_phi AS J
                            LEFT JOIN TMP_DOI_TUONG_THCP_CON AS J2 ON J."id" = J2."DOI_TUONG_THCP_ID"
                            LEFT JOIN gia_thanh_ky_tinh_gia_thanh_chi_tiet AS JPD ON J."id" = JPD."MA_DOI_TUONG_THCP_ID"
                                                                                    AND "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                        WHERE (J2."DOI_TUONG_THCP_ID" IS NOT NULL
                            OR JPD."MA_DOI_TUONG_THCP_ID" IS NOT NULL
                        )
                        ORDER BY "MA_PHAN_CAP"
                    ;


                    SELECT "MA_PHAN_CAP"
                    INTO MA_PHAN_CAP_CPSX
                    FROM danh_muc_khoan_muc_cp
                    WHERE "MA_KHOAN_MUC_CP" = 'CPSX'
                    ;

                    SELECT "MA_PHAN_CAP"
                    INTO MA_PHAN_CAP_NVLTT
                    FROM danh_muc_khoan_muc_cp
                    WHERE "MA_KHOAN_MUC_CP" = 'NVLTT'
                    ;

                    SELECT "MA_PHAN_CAP"
                    INTO MA_PHAN_CAP_NCTT
                    FROM danh_muc_khoan_muc_cp
                    WHERE "MA_KHOAN_MUC_CP" = 'NCTT'
                    ;

                    SELECT "MA_PHAN_CAP"
                    INTO MA_PHAN_CAP_SXC
                    FROM danh_muc_khoan_muc_cp
                    WHERE "MA_KHOAN_MUC_CP" = 'SXC'
                    ;


                    DROP TABLE IF EXISTS TMP_KET_QUA
                    ;

                    CREATE TEMP TABLE TMP_KET_QUA
                    (
                        "DOI_TUONG_THCP_ID"                         INT            NULL,
                        "CONG_TRINH_ID"                             INT            NULL,
                        "DON_DAT_HANG_ID"                           INT            NULL,
                        "HOP_DONG_ID"                               INT            NULL,
                        "TONG_GIA_THANH"                            DECIMAL(22, 4) NULL,
                        "LUY_KE_DA_NGHIEM_THU"                      DECIMAL(22, 4) NULL,
                        "SO_CHUA_NGHIEM_THU"                        DECIMAL(22, 4) NULL,

                        "DO_DANG_DAU_KY_NGUYEN_VAT_LIEU_TRUC_TIEP"  DECIMAL(22, 4) NULL,
                        "DO_DANG_DAU_KY_NHAN_CONG_TRUC_TIEP"        DECIMAL(22, 4) NULL,

                        "DO_DANG_DAU_KY_CHI_PHI_CHUNG"              DECIMAL(22, 4) NULL,
                        "DO_DANG_DAU_KY_TONG"                       DECIMAL(22, 4) NULL,


                        "NGUYEN_VAT_LIEU_TRUC_TIEP"                 DECIMAL(22, 4) NULL,
                        "NHAN_CONG_TRUC_TIEP"                       DECIMAL(22, 4) NULL,


                        "CHI_PHI_CHUNG"                             DECIMAL(22, 4) NULL,
                        "PHAT_SINH_TRONG_KY_TONG"                   DECIMAL(22, 4) NULL,
                        "KHOAN_GIAM_GIA_THANH"                      DECIMAL(22, 4) NULL,

                        "DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP" DECIMAL(22, 4) NULL,
                        "DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TEP"        DECIMAL(22, 4) NULL,

                        "DO_DANG_CUOI_KY_CHI_PHI_CHUNG"             DECIMAL(22, 4) NULL,
                        "DO_DANG_CUOI_KY_TONG"                      DECIMAL(22, 4) NULL,


                        "MA_DOI_TUONG_THCP"                         VARCHAR(25)    NULL,
                        "TEN_DOI_TUONG_THCP"                        VARCHAR(128)   NULL,
                        "LOAI_DOI_TUONG_THCP"                       VARCHAR(128)   NULL,


                        "BAC"                                       INT,
                        "MA_PHAN_CAP"                               VARCHAR(100)

                    )
                    ;


                    SELECT "CHI_TIET_THEO_DTTHCP"
                    INTO CHI_TIET_THEO_DOI_TUONG_THCP
                    FROM gia_thanh_cau_hinh_so_du_dau_ky AS JC
                    ;

                    IF LOAI_GIA_THANH IN ('DON_GIAN', 'HE_SO_TY_LE', 'PHAN_BUOC') --Giản đơn/ hệ số tỷ lệ/ phân bước
                    THEN

                        --Dở dang đầu kỳ
                        DROP TABLE IF EXISTS TMP_DO_DANG_DAU_KY
                        ;

                        CREATE TEMP TABLE TMP_DO_DANG_DAU_KY

                        (
                            "DOI_TUONG_THCP_ID"       INT,
                            "KY_TINH_GIA_THANH_ID"    INT,
                            "OPN_NVL_TRUC_TIEP"       DECIMAL(18, 4),
                            "OPN_NHAN_CONG_TRUC_TIEP" DECIMAL(18, 4),
                            "OPN_CHI_PHI_CHUNG"       DECIMAL(18, 4)
                        )
                        ;

                        INSERT INTO TMP_DO_DANG_DAU_KY
                        ("DOI_TUONG_THCP_ID",
                        "KY_TINH_GIA_THANH_ID",
                        "OPN_NVL_TRUC_TIEP",
                        "OPN_NHAN_CONG_TRUC_TIEP",
                        "OPN_CHI_PHI_CHUNG"
                        )
                            SELECT
                                J."DOI_TUONG_THCP_ID"
                                , ky_tinh_gia_thanh_id
                                , SUM(CASE WHEN F."DOI_TUONG_THCP_ID" IS NULL
                                THEN COALESCE(J2."CHI_PHI_NVL_TRUC_TIEP", 0)
                                    ELSE COALESCE(F."NVL_TRUC_TIEP", 0)
                                    END) AS "OPN_NVL_TRUC_TIEP"
                                , SUM(CASE WHEN F."DOI_TUONG_THCP_ID" IS NULL
                                THEN COALESCE(J2."CHI_PHI_NHAN_CONG_TRUC_TIEP", 0)
                                    ELSE COALESCE(F."NHAN_CONG_TRUC_TIEP", 0)
                                    END) AS "OPN_NHAN_CONG_TRUC_TIEP"
                                , SUM(CASE WHEN F."DOI_TUONG_THCP_ID" IS NULL
                                THEN (CASE WHEN CHI_TIET_THEO_DOI_TUONG_THCP = TRUE
                                    THEN COALESCE(J2."NVL_GIAN_TIEP",
                                                0)
                                        + COALESCE(J2."CHI_PHI_NHAN_CONG_GIAN_TIEP",
                                                    0)
                                        + COALESCE(J2."KHAU_HAO",
                                                    0)
                                        + COALESCE(J2."CHI_PHI_MUA_NGOAI",
                                                    0)
                                        + COALESCE(J2."CHI_PHI_KHAC",
                                                    0)
                                    ELSE COALESCE(J2."CHI_PHI_KHAC",
                                                    0)
                                    END)
                                    ELSE COALESCE(F."NVL_GIAN_TIEP",
                                                    0)
                                        + COALESCE(F."NHAN_CONG_GIAN_TIEP",
                                                    0)
                                        + COALESCE(F."KHAU_HAO",
                                                    0)
                                        + COALESCE(F."GIA_TRI_MUA",
                                                    0)
                                        + COALESCE(F."CHI_PHI_KHAC",
                                                    0)

                                    END)    "OPN_CHI_PHI_CHUNG"
                            FROM TMP_DOI_TUONG_THCP_CON AS J
                                LEFT JOIN account_ex_chi_phi_do_dang AS J2 ON J."DOI_TUONG_THCP_ID" = J2."MA_DOI_TUONG_THCP_ID"

                                                                            AND "CHI_NHANH_ID" = chi_nhanh_id
                                LEFT JOIN LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP('{35}', --@ListJob
                                                                                            tu_ngay,
                                                                                            chi_nhanh_id
                                        )
                                    AS F ON F."DOI_TUONG_THCP_ID" = J."DOI_TUONG_THCP_ID"
                            GROUP BY J."DOI_TUONG_THCP_ID"
                        ;


                        --Phát sinh trong kỳ

                        DROP TABLE IF EXISTS TMP_PHAT_SINH_TRONG_KY
                        ;

                        CREATE TEMP TABLE TMP_PHAT_SINH_TRONG_KY


                        (
                            "DOI_TUONG_THCP_ID"    INT,
                            "KY_TINH_GIA_THANH_ID" INT,

                            "NVL_TRUC_TIEP"        DECIMAL(22, 4),

                            "NHAN_CONG_TRUC_TIEP"  DECIMAL(22, 4),

                            "CHI_PHI_CHUNG"        DECIMAL(22, 4)
                        )
                        ;

                        -- --Phân bổ chi phí chung trong kỳ


                        DROP TABLE IF EXISTS TMP_PHAN_BO_CHI_PHI_CHUNG_TRONG_KY
                        ;

                        CREATE TEMP TABLE TMP_PHAN_BO_CHI_PHI_CHUNG_TRONG_KY
                        (
                            "DOI_TUONG_THCP_ID"           INT,
                            "KY_TINH_GIA_THANH_ID"        INT,

                            "PHAN_BO_NVL_TRUC_TIEP"       DECIMAL(22, 4),

                            "PHAN_BO_NHAN_CONG_TRUC_TIEP" DECIMAL(22, 4),

                            "PHAN_BO_CHI_PHI_CHUNG"       DECIMAL(22, 4)
                        )
                        ;

                        IF CHE_DO_KE_TOAN = '15'
                        THEN

                            --Chi phí phát sinh
                            INSERT INTO TMP_PHAT_SINH_TRONG_KY
                            ("DOI_TUONG_THCP_ID",
                            "KY_TINH_GIA_THANH_ID",
                            "NVL_TRUC_TIEP",
                            "NHAN_CONG_TRUC_TIEP",
                            "CHI_PHI_CHUNG"

                            )
                                SELECT
                                    J."DOI_TUONG_THCP_ID"
                                    , ky_tinh_gia_thanh_id
                                    , SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '621%%'
                                                    OR ("MA_TAI_KHOAN" LIKE N'154%%' AND "LOAI_HACH_TOAN" = '1' AND
                                                        "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%' AND
                                                        "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%' AND
                                                        "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%')
                                    THEN COALESCE("GHI_NO", 0)
                                        - COALESCE("GHI_CO", 0)
                                        ELSE 0
                                        END) AS "NVL_TRUC_TIEP"
                                    , --621
                                    SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '622%%'
                                        THEN COALESCE("GHI_NO", 0)
                                            - COALESCE("GHI_CO", 0)
                                        ELSE 0
                                        END) AS "NHAN_CONG_TRUC_TIEP"
                                    , --622
                                    SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '627%%'
                                        THEN COALESCE("GHI_NO", 0)
                                            - COALESCE("GHI_CO", 0)
                                        ELSE 0
                                        END) AS "CHI_PHI_CHUNG" --627
                                FROM so_cai_chi_tiet AS GL
                                    INNER JOIN TMP_DOI_TUONG_THCP_CON AS J ON GL."DOI_TUONG_THCP_ID" = J."DOI_TUONG_THCP_ID"
                                WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                                    AND "CHI_NHANH_ID" = chi_nhanh_id
                                    AND
                                    (((("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND "LOAI_HACH_TOAN" = '2') OR
                                        "LOAI_HACH_TOAN" = '1'))

                                    OR ("MA_TAI_KHOAN" LIKE N'154%%' AND "LOAI_HACH_TOAN" = '1' AND
                                        "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%' AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%' AND
                                        "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%'))

                                GROUP BY J."DOI_TUONG_THCP_ID"

                            ;


                            INSERT INTO TMP_PHAN_BO_CHI_PHI_CHUNG_TRONG_KY
                            ("DOI_TUONG_THCP_ID",
                            "KY_TINH_GIA_THANH_ID",

                            "PHAN_BO_NVL_TRUC_TIEP",

                            "PHAN_BO_NHAN_CONG_TRUC_TIEP",

                            "PHAN_BO_CHI_PHI_CHUNG"
                            )
                                SELECT
                                    "MA_DOI_TUONG_THCP_ID"
                                    , ky_tinh_gia_thanh_id
                                    , SUM(CASE WHEN (SELECT "SO_TAI_KHOAN"
                                                    FROM danh_muc_he_thong_tai_khoan TK
                                                    WHERE TK.id = "TAI_KHOAN_ID") LIKE '621%%'
                                    THEN COALESCE("SO_TIEN",
                                                0)
                                        ELSE 0
                                        END)
                                    , SUM(CASE WHEN (SELECT "SO_TAI_KHOAN"
                                                    FROM danh_muc_he_thong_tai_khoan TK
                                                    WHERE TK.id = "TAI_KHOAN_ID") LIKE '622%%'
                                    THEN COALESCE("SO_TIEN",
                                                0)
                                        ELSE 0
                                        END)
                                    , SUM(CASE WHEN (SELECT "SO_TAI_KHOAN"
                                                    FROM danh_muc_he_thong_tai_khoan TK
                                                    WHERE TK.id = "TAI_KHOAN_ID") LIKE '627%%'
                                    THEN COALESCE("SO_TIEN",
                                                0)
                                        ELSE 0
                                        END)
                                FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung AS JCAD
                                WHERE "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id

                                GROUP BY "MA_DOI_TUONG_THCP_ID"

                            ;


                        ELSE


                            --Chi phí phát sinh
                            INSERT INTO TMP_PHAT_SINH_TRONG_KY
                            (
                                "DOI_TUONG_THCP_ID",
                                "KY_TINH_GIA_THANH_ID",
                                "NVL_TRUC_TIEP",
                                "NHAN_CONG_TRUC_TIEP",
                                "CHI_PHI_CHUNG"

                            )
                                SELECT
                                    J."DOI_TUONG_THCP_ID"
                                    , ky_tinh_gia_thanh_id
                                    , SUM(CASE WHEN EI."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT || '%%'
                                    THEN COALESCE("GHI_NO", 0)
                                        - COALESCE("GHI_CO", 0)
                                        ELSE 0
                                        END)
                                    , --621
                                    SUM(CASE WHEN EI."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT || '%%'
                                        THEN COALESCE("GHI_NO", 0)
                                            - COALESCE("GHI_CO", 0)
                                        ELSE 0
                                        END)
                                    , --622
                                    SUM(CASE WHEN EI."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC || '%%'
                                        THEN COALESCE("GHI_NO", 0)
                                            - COALESCE("GHI_CO", 0)
                                        ELSE 0
                                        END) --6274
                                FROM so_cai_chi_tiet AS GL
                                    INNER JOIN TMP_DOI_TUONG_THCP_CON AS J ON GL."DOI_TUONG_THCP_ID" = J."DOI_TUONG_THCP_ID"
                                    LEFT JOIN danh_muc_khoan_muc_cp AS EI ON GL."KHOAN_MUC_CP_ID" = EI."id"
                                WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

                                    AND (SELECT "SO_TAI_KHOAN"
                                        FROM danh_muc_he_thong_tai_khoan TK
                                        WHERE TK.id = "TAI_KHOAN_ID") LIKE '154%%'
                                    AND GL."KHOAN_MUC_CP_ID" IS NOT NULL

                                    AND "CHI_NHANH_ID" = chi_nhanh_id
                                GROUP BY J."DOI_TUONG_THCP_ID"

                            ;


                            INSERT INTO TMP_PHAN_BO_CHI_PHI_CHUNG_TRONG_KY
                            ("DOI_TUONG_THCP_ID",
                            "KY_TINH_GIA_THANH_ID",

                            "PHAN_BO_NVL_TRUC_TIEP",

                            "PHAN_BO_NHAN_CONG_TRUC_TIEP",

                            "PHAN_BO_CHI_PHI_CHUNG"
                            )
                                SELECT
                                    "MA_DOI_TUONG_THCP_ID"
                                    , ky_tinh_gia_thanh_id
                                    , SUM(CASE WHEN EI."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT || '%%'
                                    THEN COALESCE("SO_TIEN",
                                                0)
                                        ELSE 0
                                        END)
                                    , SUM(CASE WHEN EI."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT || '%%'
                                    THEN COALESCE("SO_TIEN",
                                                0)
                                        ELSE 0
                                        END)
                                    , SUM(CASE WHEN EI."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC || '%%'
                                    THEN COALESCE("SO_TIEN",
                                                0)
                                        ELSE 0
                                        END)
                                FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung AS JCAD
                                    LEFT JOIN danh_muc_khoan_muc_cp AS EI ON JCAD."KHOAN_MUC_CP_ID" = EI."id"
                                WHERE "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id

                                GROUP BY "MA_DOI_TUONG_THCP_ID"
                            ;

                        END IF
                        ;


                        --Khoản giảm giá thành
                        DROP TABLE IF EXISTS TMP_KHOAN_GIAM_GIA_THANH
                        ;

                        CREATE TEMP TABLE TMP_KHOAN_GIAM_GIA_THANH

                        (
                            "DOI_TUONG_THCP_ID"    INT,
                            "KY_TINH_GIA_THANH_ID" INT,
                            "KHOAN_GIAM_GIA_THANH" DECIMAL(22, 4)
                        )
                        ;

                        INSERT INTO TMP_KHOAN_GIAM_GIA_THANH
                        ("DOI_TUONG_THCP_ID",
                        "KY_TINH_GIA_THANH_ID",
                        "KHOAN_GIAM_GIA_THANH"

                        )
                            SELECT
                                J."DOI_TUONG_THCP_ID"
                                , ky_tinh_gia_thanh_id
                                , SUM(COALESCE("GHI_CO", 0)) AS "NVL_TRUC_TIEP"
                            FROM so_cai_chi_tiet AS GL
                                INNER JOIN TMP_DOI_TUONG_THCP_CON AS J ON GL."DOI_TUONG_THCP_ID" = J."DOI_TUONG_THCP_ID"
                                LEFT JOIN danh_muc_khoan_muc_cp AS EI ON GL."KHOAN_MUC_CP_ID" = EI."id"
                            WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                AND "MA_TAI_KHOAN" LIKE '154%%' AND "LOAI_HACH_TOAN" = '2'

                                AND (CHE_DO_KE_TOAN = '15'
                                    OR (CHE_DO_KE_TOAN = '48'
                                        AND (EI."id" IS NULL
                                                OR EI."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX || '%%'
                                        )
                                    )
                                )

                                AND "CHI_NHANH_ID" = chi_nhanh_id
                                AND "LOAI_CHUNG_TU" <> '2010'

                            GROUP BY J."DOI_TUONG_THCP_ID"

                        ;


                        --QĐ15 = Phát sinh Có TK 154 chi tiết theo đối tượng THCP trên chứng từ có ngày hạch toán thuộc kỳ tính giá thành (Không kể PSĐƯ Nợ 155,157/Có 154 chi tiết theo đối tượng tập hợp CP)
                        --QĐ48 = Phát sinh Có TK 154 chi tiết theo đối tượng THCP không chi tiết theo các KMCP sản xuất trên chứng từ có ngày hạch toán thuộc kỳ tính giá thành  (Không kể PSĐƯ Nợ 155,157/Có 154 không chi tiết theo KMCP CPSX chi tiết theo đối tượng tập hợp CP)


                        --     	Dở dang cuối kỳ :lấy trên form đánh giá dở dang của kỳ tính giá thành này
                        --
                        DROP TABLE IF EXISTS TMP_DO_DANG_CUOI_KY
                        ;

                        CREATE TEMP TABLE TMP_DO_DANG_CUOI_KY

                        (
                            "DOI_TUONG_THCP_ID"                         INT,
                            "KY_TINH_GIA_THANH_ID"                      INT,
                            "DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP" DECIMAL(22, 4),
                            "DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TIEP"       DECIMAL(22, 4),

                            "DO_DANG_CUOI_KY_CHI_PHI_CHUNG"             DECIMAL(22, 4)
                        )
                        ;


                        INSERT INTO TMP_DO_DANG_CUOI_KY
                        ("DOI_TUONG_THCP_ID",
                        "KY_TINH_GIA_THANH_ID",
                        "DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP",
                        "DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TIEP",

                        "DO_DANG_CUOI_KY_CHI_PHI_CHUNG"

                        )
                            SELECT
                                "MA_DOI_TUONG_THCP_ID"
                                , ky_tinh_gia_thanh_id
                                , SUM(COALESCE("NVL_TRUC_TIEP", 0))
                                , SUM(COALESCE("NHAN_CONG_TRUC_TIEP", 0))
                                , SUM(COALESCE("NHAN_CONG_GIAN_TIEP", 0)
                                    + COALESCE("NVL_GIAN_TIEP", 0)
                                    + COALESCE("CHI_PHI_MUA_NGOAI", 0)
                                    + COALESCE("CHI_PHI_KHAC", 0)
                                    + COALESCE("KHAU_HAO", 0))
                            FROM gia_thanh_ket_qua_chi_phi_do_dang_cuoi_ky_chi_tiet AS JUD
                            WHERE "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id

                            GROUP BY "MA_DOI_TUONG_THCP_ID"

                        ;


                        INSERT INTO TMP_KET_QUA
                        ("DOI_TUONG_THCP_ID",
                        "CONG_TRINH_ID",
                        "DON_DAT_HANG_ID",
                        "HOP_DONG_ID",
                        "TONG_GIA_THANH",
                        "LUY_KE_DA_NGHIEM_THU",
                        "SO_CHUA_NGHIEM_THU",

                        "DO_DANG_DAU_KY_NGUYEN_VAT_LIEU_TRUC_TIEP",
                        "DO_DANG_DAU_KY_NHAN_CONG_TRUC_TIEP",

                        "DO_DANG_DAU_KY_CHI_PHI_CHUNG",
                        "DO_DANG_DAU_KY_TONG",


                        "NGUYEN_VAT_LIEU_TRUC_TIEP",
                        "NHAN_CONG_TRUC_TIEP",


                        "CHI_PHI_CHUNG",
                        "PHAT_SINH_TRONG_KY_TONG",
                        "KHOAN_GIAM_GIA_THANH",

                        "DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP",
                        "DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TEP",

                        "DO_DANG_CUOI_KY_CHI_PHI_CHUNG",
                        "DO_DANG_CUOI_KY_TONG",


                        "MA_DOI_TUONG_THCP",
                        "TEN_DOI_TUONG_THCP",
                        "LOAI_DOI_TUONG_THCP",


                        "BAC",
                        "MA_PHAN_CAP"

                        )
                            SELECT
                                J."DOI_TUONG_THCP_ID"
                                , NULL AS "CONG_TRINH_ID"
                                , NULL AS "DON_DAT_HANG_ID"
                                , NULL AS "HOP_DONG_ID"
                                , COALESCE("OPN_NVL_TRUC_TIEP", 0)
                                + COALESCE("OPN_NHAN_CONG_TRUC_TIEP", 0)
                                + COALESCE("OPN_CHI_PHI_CHUNG", 0)
                                + COALESCE("NVL_TRUC_TIEP", 0)
                                + COALESCE("PHAN_BO_NVL_TRUC_TIEP", 0)
                                + COALESCE("NHAN_CONG_TRUC_TIEP", 0)
                                + COALESCE("PHAN_BO_NHAN_CONG_TRUC_TIEP", 0)
                                + COALESCE("CHI_PHI_CHUNG", 0)
                                + COALESCE("PHAN_BO_CHI_PHI_CHUNG", 0)
                                - COALESCE("KHOAN_GIAM_GIA_THANH", 0)
                                - COALESCE("DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP", 0)
                                - COALESCE("DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TIEP", 0)
                                - COALESCE("DO_DANG_CUOI_KY_CHI_PHI_CHUNG", 0) AS "TONG_GIA_THANH"
                                , 0 AS "LUY_KE_DA_NGHIEM_THU"
                                , 0 AS "SO_CHUA_NGHIEM_THU"
                                , COALESCE("OPN_NVL_TRUC_TIEP", 0) AS "DO_DANG_DAU_KY_NGUYEN_VAT_LIEU_TRUC_TIEP"
                                , COALESCE("OPN_NHAN_CONG_TRUC_TIEP", 0) AS "DO_DANG_DAU_KY_NHAN_CONG_TRUC_TIEP"

                                , COALESCE("OPN_CHI_PHI_CHUNG", 0) AS "DO_DANG_DAU_KY_CHI_PHI_CHUNG"
                                , COALESCE("OPN_NVL_TRUC_TIEP", 0)
                                + COALESCE("OPN_NHAN_CONG_TRUC_TIEP", 0)
                                + COALESCE("OPN_CHI_PHI_CHUNG", 0) AS "DO_DANG_DAU_KY_TONG"
                                , COALESCE("NVL_TRUC_TIEP", 0)
                                + COALESCE("PHAN_BO_NVL_TRUC_TIEP", 0) AS "NGUYEN_VAT_LIEU_TRUC_TIEP"
                                , COALESCE("NHAN_CONG_TRUC_TIEP", 0)
                                + COALESCE("PHAN_BO_NHAN_CONG_TRUC_TIEP", 0) AS "NHAN_CONG_TRUC_TIEP"

                                , COALESCE("CHI_PHI_CHUNG", 0)
                                + COALESCE("PHAN_BO_CHI_PHI_CHUNG", 0) AS "CHI_PHI_CHUNG"

                                , COALESCE("NVL_TRUC_TIEP", 0)
                                + COALESCE("PHAN_BO_NVL_TRUC_TIEP", 0)
                                + COALESCE("NHAN_CONG_TRUC_TIEP", 0)
                                + COALESCE("PHAN_BO_NHAN_CONG_TRUC_TIEP", 0)
                                + COALESCE("CHI_PHI_CHUNG", 0)
                                + COALESCE("PHAN_BO_CHI_PHI_CHUNG", 0) AS "PHAT_SINH_TRONG_KY_TONG"

                                , COALESCE("KHOAN_GIAM_GIA_THANH", 0) AS "KHOAN_GIAM_GIA_THANH"
                                , COALESCE("DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP", 0) AS "DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP"
                                , COALESCE("DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TIEP", 0) AS "DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TEP"

                                , COALESCE("DO_DANG_CUOI_KY_CHI_PHI_CHUNG", 0) AS "DO_DANG_CUOI_KY_CHI_PHI_CHUNG"
                                , COALESCE("DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP", 0)
                                + COALESCE("DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TIEP", 0)
                                + COALESCE("DO_DANG_CUOI_KY_CHI_PHI_CHUNG", 0) AS "DO_DANG_CUOI_KY_TONG"

                                , J."MA_DOI_TUONG_THCP"
                                , J."TEN_DOI_TUONG_THCP"
                                , J."LOAI_DOI_TUONG_THCP"

                                , J."BAC"
                                , J."MA_PHAN_CAP"
                            FROM TMP_DOI_TUONG_THCP AS J
                                LEFT JOIN TMP_DO_DANG_DAU_KY AS OPN ON J."DOI_TUONG_THCP_ID" = OPN."DOI_TUONG_THCP_ID"
                                LEFT JOIN TMP_PHAT_SINH_TRONG_KY AS U ON J."DOI_TUONG_THCP_ID" = U."DOI_TUONG_THCP_ID"
                                LEFT JOIN TMP_PHAN_BO_CHI_PHI_CHUNG_TRONG_KY AS A ON J."DOI_TUONG_THCP_ID" = A."DOI_TUONG_THCP_ID"
                                LEFT JOIN TMP_KHOAN_GIAM_GIA_THANH AS D ON J."DOI_TUONG_THCP_ID" = D."DOI_TUONG_THCP_ID"
                                LEFT JOIN TMP_DO_DANG_CUOI_KY AS C ON J."DOI_TUONG_THCP_ID" = C."DOI_TUONG_THCP_ID"
                            ORDER BY J."MA_PHAN_CAP"


                        ;

                    ELSE --Các PP khác


                        -- Lấy dữ liệu hiển thị lên giao diện
                        INSERT INTO TMP_KET_QUA
                        (
                            "DOI_TUONG_THCP_ID",
                            "CONG_TRINH_ID",
                            "DON_DAT_HANG_ID",
                            "HOP_DONG_ID",
                            "TONG_GIA_THANH",
                            "LUY_KE_DA_NGHIEM_THU",
                            "SO_CHUA_NGHIEM_THU",

                            "DO_DANG_DAU_KY_NGUYEN_VAT_LIEU_TRUC_TIEP",
                            "DO_DANG_DAU_KY_NHAN_CONG_TRUC_TIEP",

                            "DO_DANG_DAU_KY_CHI_PHI_CHUNG",
                            "DO_DANG_DAU_KY_TONG",


                            "NGUYEN_VAT_LIEU_TRUC_TIEP",
                            "NHAN_CONG_TRUC_TIEP",


                            "CHI_PHI_CHUNG",
                            "PHAT_SINH_TRONG_KY_TONG",
                            "KHOAN_GIAM_GIA_THANH",

                            "DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP",
                            "DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TEP",

                            "DO_DANG_CUOI_KY_CHI_PHI_CHUNG",
                            "DO_DANG_CUOI_KY_TONG",


                            "MA_DOI_TUONG_THCP",
                            "TEN_DOI_TUONG_THCP",
                            "LOAI_DOI_TUONG_THCP"


                        )
                            SELECT
                                JPJ."MA_DOI_TUONG_THCP_ID"
                                , JPJ."MA_CONG_TRINH_ID"
                                , JPJ."SO_DON_HANG_ID"
                                , JPJ."SO_HOP_DONG_ID"
                                , 0   AS "TONG_GIA_THANH"
                                , 0   AS "LUY_KE_DA_NGHIEM_THU"
                                , 0   AS "SO_CHUA_NGHIEM_THU"
                                , 0   AS "DO_DANG_DAU_KY_NVL_TRUC_TIEP"
                                , 0   AS "DO_DANG_DAU_KY_NHAN_CONG_TRUC_TIEP"

                                , 0   AS "DO_DANG_DAU_KY_CHI_PHI_CHUNG"
                                , 0   AS "DO_DANG_DAU_KY_TONG"
                                , 0   AS "NGUYEN_VAT_LIEU_TRUC_TIEP"
                                , 0   AS "NHAN_CONG_TRUC_TIEP"

                                , 0   AS "CHI_PHI_CHUNG"
                                , 0   AS "PHAT_SINH_TRONG_KY_TONG"
                                , 0   AS "KHOAN_GIAM_GIA_THANH"
                                , 0   AS "DO_DANG_CUOI_KY_NGUYEN_VAT_LIEU_TRUC_TIEP"
                                , 0   AS "DO_DANG_CUOI_KY_NHAN_CONG_TRUC_TEP"

                                , 0   AS "DO_DANG_CUOI_KY_CHI_PHI_CHUNG"
                                , 0   AS "DO_DANG_CUOI_KY_TONG"

                                , J."MA_DOI_TUONG_THCP"
                                , j."TEN_DOI_TUONG_THCP"
                                , CASE WHEN j."LOAI" = '0'
                                THEN N'Phân xưởng'
                                WHEN j."LOAI" = '1'
                                    THEN N'Sản phẩm'
                                WHEN j."LOAI" = '2'
                                    THEN N'Quy trình sản xuất'
                                WHEN j."LOAI" = '3'
                                    THEN N'Công đoạn'
                                END AS "LOAI_DOI_TUONG_THCP"
                            FROM gia_thanh_ky_tinh_gia_thanh_chi_tiet AS JPJ
                                LEFT JOIN account_ex_don_dat_hang AS SO ON so."id" = JPJ."SO_DON_HANG_ID"
                                LEFT JOIN danh_muc_cong_trinh AS PW ON JPJ."MA_CONG_TRINH_ID" = PW."id"
                                LEFT JOIN danh_muc_loai_cong_trinh AS PWC ON PW."LOAI_CONG_TRINH" = PWC."id"
                                LEFT JOIN sale_ex_hop_dong_ban AS CT ON JPJ."SO_HOP_DONG_ID" = CT."id"
                                LEFT JOIN res_partner AS AO ON CT."KHACH_HANG_ID" = AO."id"
                                LEFT JOIN danh_muc_doi_tuong_tap_hop_chi_phi AS J ON JPJ."MA_DOI_TUONG_THCP_ID" = J."id"
                            WHERE JPJ."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                            ORDER BY pW."BAC" ASC
                        ;


                    END IF
                    ;

                END $$
                ;


                SELECT *
                FROM TMP_KET_QUA

                ;
 
        """  
        return self.execute(query, params)


    def lay_du_lieu_chi_phi_theo_khoan_muc_ct_dh_hd(self,ky_tinh_gia_thanh_id,chi_nhanh_id):
        params = {
            'KY_TINH_GIA_THANH_ID' : ky_tinh_gia_thanh_id,
            'CHI_NHANH_ID' : chi_nhanh_id,
            }
        query = """  

                DO LANGUAGE plpgsql $$
                DECLARE

                    ky_tinh_gia_thanh_id INTEGER := %(KY_TINH_GIA_THANH_ID)s;


                    chi_nhanh_id         INTEGER := %(CHI_NHANH_ID)s;

                    CHE_DO_KE_TOAN       VARCHAR;

                    tu_ngay              TIMESTAMP;

                    den_ngay             TIMESTAMP;

                    LOAI_GIA_THANH       VARCHAR;


                    MA_PHAN_CAPMTC       VARCHAR(100);

                    MA_PHAN_CAPCPSX      VARCHAR(100);

                    MA_PHAN_CAP_NVLTT    VARCHAR(100);

                    MA_PHAN_CAP_NCTT     VARCHAR(100);

                    MA_PHAN_CAP_SXC      VARCHAR(100);


                    MA_PHAN_CAP_CPSX     VARCHAR(100);

                    MA_PHAN_CAP_MTC      VARCHAR(100);


                BEGIN


                    SELECT value
                    INTO CHE_DO_KE_TOAN
                    FROM ir_config_parameter
                    WHERE key = 'he_thong.CHE_DO_KE_TOAN'
                    FETCH FIRST 1 ROW ONLY
                    ;

                    SELECT "TU_NGAY"
                    INTO tu_ngay
                    FROM gia_thanh_ky_tinh_gia_thanh AS JP
                    WHERE "id" = ky_tinh_gia_thanh_id
                    ;

                    SELECT "DEN_NGAY"
                    INTO den_ngay
                    FROM gia_thanh_ky_tinh_gia_thanh AS JP
                    WHERE "id" = ky_tinh_gia_thanh_id
                    ;

                    SELECT "LOAI_GIA_THANH"
                    INTO LOAI_GIA_THANH
                    FROM gia_thanh_ky_tinh_gia_thanh AS JP
                    WHERE "id" = ky_tinh_gia_thanh_id
                    ;


                    SELECT "MA_PHAN_CAP"
                    INTO MA_PHAN_CAPCPSX
                    FROM danh_muc_khoan_muc_cp
                    WHERE "MA_KHOAN_MUC_CP" = 'CPSX'
                    ;


                    SELECT "MA_PHAN_CAP"
                    INTO MA_PHAN_CAPMTC
                    FROM danh_muc_khoan_muc_cp
                    WHERE "MA_KHOAN_MUC_CP" = 'MTC'
                    ;


                    DROP TABLE IF EXISTS TMP_KY_TINH_GIA_THANH_CHI_TIET
                    ;

                    CREATE TEMP TABLE TMP_KY_TINH_GIA_THANH_CHI_TIET


                    (
                        "KY_TINH_GIA_THANH_CHI_TIET_ID" INT,
                        "KY_TINH_GIA_THANH_ID"          INT,
                        "DOI_TUONG_THCP_ID"             INT,
                        "CONG_TRINH_ID"                 INT,
                        "DON_DAT_HANG_ID"               INT,
                        "HOP_DONG_ID"                   INT,
                        "STT"                           INT
                    )
                    ;

                    INSERT INTO TMP_KY_TINH_GIA_THANH_CHI_TIET
                    ("KY_TINH_GIA_THANH_CHI_TIET_ID",
                    "KY_TINH_GIA_THANH_ID",
                    "DOI_TUONG_THCP_ID",
                    "CONG_TRINH_ID",
                    "DON_DAT_HANG_ID",
                    "HOP_DONG_ID",
                    "STT"
                    )
                        SELECT
                            JPD.id
                            , JPD."KY_TINH_GIA_THANH_ID"
                            , JPD."MA_DOI_TUONG_THCP_ID"
                            , JPD."MA_CONG_TRINH_ID"
                            , JPD."SO_DON_HANG_ID"
                            , JPD."SO_HOP_DONG_ID"
                            , JPD."STT"


                        FROM gia_thanh_ky_tinh_gia_thanh_chi_tiet AS JPD
                        WHERE "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                        UNION
                        SELECT
                            0                    AS "KY_TINH_GIA_THANH_CHI_TIET_ID"
                            , ky_tinh_gia_thanh_id AS "KY_TINH_GIA_THANH_ID"
                            , NULL
                            , A."id"
                            , NULL
                            , NULL
                            , 0
                        FROM (SELECT DISTINCT Pw2.*
                            FROM gia_thanh_ky_tinh_gia_thanh_chi_tiet AS JPD
                                INNER JOIN gia_thanh_ky_tinh_gia_thanh AS JP ON JP."id" = JPD."KY_TINH_GIA_THANH_ID"
                                                                                AND LOAI_GIA_THANH = 'CONG_TRINH'
                                INNER JOIN danh_muc_cong_trinh AS PW ON PW."id" = JPD."MA_CONG_TRINH_ID"
                                INNER JOIN danh_muc_cong_trinh AS PW2 ON PW."MA_PHAN_CAP" LIKE PW2."MA_PHAN_CAP"
                                                                                                || '%%'
                            WHERE JPD."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                                    AND Pw2."isparent" = TRUE
                            ) A
                    ;


                    --          --1.3 Khai báo bảng lưu dữ liệu mực đích khai báo chỉ để Query trong JCOPN 1 lần, bảng phân bổ 1 lần, sổ 1 lần không phải vét nhiều lần trên bảng phân bổ và sổ

                    DROP TABLE IF EXISTS TMP_LUU_DU_LIEU_CHI_PHI
                    ;

                    CREATE TEMP TABLE TMP_LUU_DU_LIEU_CHI_PHI


                    (
                        "KY_TINH_GIA_THANH_ID"          INT,
                        "KY_TINH_GIA_THANH_CHI_TIET_ID" INT,
                        "SO_DA_NGHIEM_THU"              DECIMAL(18, 4) DEFAULT (0), -- Số lũy kế nghiệm thu
                        "OPN_SO_DA_NGHIEM_THU"          DECIMAL(18, 4) DEFAULT (0), -- Số lũy kế nghiệm thu
                        "OPN_NGUYEN_VAT_LIEU"           DECIMAL(18, 4) DEFAULT (0), --Số kỹ kế kỳ trước
                        "OPN_NHAN_CONG"                 DECIMAL(18, 4) DEFAULT (0), -- Nhân công trực tiếp
                        "OPN_MAY_THI_CONG"              DECIMAL(18, 4) DEFAULT (0), -- Máy thi công
                        "OPN_CHI_PHI_CHUNG"             DECIMAL(18, 4) DEFAULT (0), -- Sản xuất chung
                        "NGUYEN_VAT_LIEU"               DECIMAL(18, 4) DEFAULT (0), -- Phát sinh trong kỳ
                        "NHAN_CONG"                     DECIMAL(18, 4) DEFAULT (0),
                        "MAY_THI_CONG"                  DECIMAL(18, 4) DEFAULT (0),
                        "CHI_PHI_CHUNG"                 DECIMAL(18, 4) DEFAULT (0),
                        "KHOAN_GIAM_GIA_THANH"          DECIMAL(18, 4) DEFAULT (0)-- Khoản giảm giá thành
                    )
                    ;

                    --Khai báo các hằng số cho QD48


                    -- 			-- KMCP: Sản xuất
                    SELECT "MA_PHAN_CAP"
                    INTO MA_PHAN_CAP_CPSX
                    FROM danh_muc_khoan_muc_cp
                    WHERE "MA_KHOAN_MUC_CP" = 'CPSX'
                    ;

                    SELECT "MA_PHAN_CAP"
                    INTO MA_PHAN_CAP_NVLTT
                    FROM danh_muc_khoan_muc_cp
                    WHERE "MA_KHOAN_MUC_CP" = 'NVLTT'
                    ;

                    SELECT "MA_PHAN_CAP"
                    INTO MA_PHAN_CAP_NCTT
                    FROM danh_muc_khoan_muc_cp
                    WHERE "MA_KHOAN_MUC_CP" = 'NCTT'
                    ;

                    SELECT "MA_PHAN_CAP"
                    INTO MA_PHAN_CAP_MTC
                    FROM danh_muc_khoan_muc_cp
                    WHERE "MA_KHOAN_MUC_CP" = 'MTC'
                    ;

                    SELECT "MA_PHAN_CAP"
                    INTO MA_PHAN_CAP_SXC
                    FROM danh_muc_khoan_muc_cp
                    WHERE "MA_KHOAN_MUC_CP" = 'SXC'
                    ;

                    -- Chi phí sản xuất chung để lấy các phát sinh khác với CPSX

                    INSERT INTO TMP_LUU_DU_LIEU_CHI_PHI
                    ("KY_TINH_GIA_THANH_ID",
                    "KY_TINH_GIA_THANH_CHI_TIET_ID",
                    "SO_DA_NGHIEM_THU",
                    "OPN_SO_DA_NGHIEM_THU",
                    "OPN_NGUYEN_VAT_LIEU",
                    "OPN_NHAN_CONG",
                    "OPN_MAY_THI_CONG",
                    "OPN_CHI_PHI_CHUNG"
                    )
                        SELECT
                            JP."KY_TINH_GIA_THANH_ID"
                            , JP."KY_TINH_GIA_THANH_CHI_TIET_ID"
                            , SUM(JO."SO_DA_NGHIEM_THU")               AS "SO_DA_NGHIEM_THU"
                            , SUM(JO."SO_DA_NGHIEM_THU")               AS "OPN_SO_DA_NGHIEM_THU"
                            , SUM(JO."CHI_PHI_NVL_TRUC_TIEP")          AS "NGUYEN_VAT_LIEU"
                            , SUM(JO."CHI_PHI_NHAN_CONG_TRUC_TIEP")    AS "NHAN_CONG"
                            , SUM(JO."MTC_CHI_PHI_KHAU_HAO_DAU_KY"
                                + JO."MTC_CHI_PHI_NHAN_CONG"
                                + JO."MTC_CHI_PHI_NVL_GIAN_TIEP"
                                + JO."MTC_CHI_PHI_KHAC_CHUNG"
                                + JO."MTC_CHI_PHI_MUA_NGOAI_DAU_KY") AS "OPN_MAY_THI_CONG"
                            , SUM(JO."CHI_PHI_NHAN_CONG_GIAN_TIEP"
                                + JO."NVL_GIAN_TIEP"
                                + JO."KHAU_HAO"
                                + JO."CHI_PHI_MUA_NGOAI"
                                + JO."CHI_PHI_KHAC")                 AS "OPN_CHI_PHI_CHUNG"
                        FROM TMP_KY_TINH_GIA_THANH_CHI_TIET JP
                            LEFT JOIN account_ex_chi_phi_do_dang JO ON ((LOAI_GIA_THANH = 'CONG_TRINH'
                                                                        AND JO."MA_CONG_TRINH_ID" = JP."CONG_TRINH_ID"
                                                                        )
                                                                        OR (LOAI_GIA_THANH = 'DON_HANG'
                                                                            AND JO."DON_HANG_ID" = JP."DON_DAT_HANG_ID"
                                                                        )
                                                                        OR (LOAI_GIA_THANH = 'HOP_DONG'
                                                                            AND JO."HOP_DONG_ID" = JP."HOP_DONG_ID"
                                                                        )
                                )
                        WHERE JP."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                            AND JO."CHI_NHANH_ID" = chi_nhanh_id

                            AND (SELECT "SO_TAI_KHOAN"
                                FROM danh_muc_he_thong_tai_khoan TK
                                WHERE TK.id = JO."TAI_KHOAN_CPSXKD_DO_DANG_ID") LIKE N'154%%'
                        GROUP BY "KY_TINH_GIA_THANH_ID",
                            "KY_TINH_GIA_THANH_CHI_TIET_ID"
                    ;


                    IF (CHE_DO_KE_TOAN = '15')
                    THEN

                        INSERT INTO TMP_LUU_DU_LIEU_CHI_PHI
                        ("KY_TINH_GIA_THANH_ID",
                        "KY_TINH_GIA_THANH_CHI_TIET_ID",
                        --NVL
                        "OPN_NGUYEN_VAT_LIEU",
                        "NGUYEN_VAT_LIEU",
                        --NC
                        "OPN_NHAN_CONG",
                        "NHAN_CONG",
                        --MTC
                        "OPN_MAY_THI_CONG",
                        "MAY_THI_CONG",
                        -- CPC
                        "OPN_CHI_PHI_CHUNG",
                        "CHI_PHI_CHUNG"
                        )
                            SELECT
                                JP."KY_TINH_GIA_THANH_ID"
                                , JP."KY_TINH_GIA_THANH_CHI_TIET_ID"
                                , (CASE WHEN JCA."DEN_NGAY" < tu_ngay
                                            AND ((SELECT "SO_TAI_KHOAN"
                                                FROM danh_muc_he_thong_tai_khoan TK
                                                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '621%%')
                                THEN SUM(JCA."SO_TIEN")
                                ELSE 0
                                END)    AS "OPN_NGUYEN_VAT_LIEU"
                                , (-- Nếu có JCAJC"PHAT_SINH_TRONG_KY"DetailID=JP."KY_TINH_GIA_THANH_CHI_TIET_ID"
                                    CASE WHEN JCA."KY_TINH_GIA_THANH_CHI_TIET_ID" = JP."KY_TINH_GIA_THANH_CHI_TIET_ID"
                                                AND ((SELECT "SO_TAI_KHOAN"
                                                    FROM danh_muc_he_thong_tai_khoan TK
                                                    WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '621%%')
                                        THEN SUM(JCA."SO_TIEN")
                                    ELSE 0
                                    END) AS "NGUYEN_VAT_LIEU"
                                , (CASE WHEN JCA."DEN_NGAY" < tu_ngay
                                            AND ((SELECT "SO_TAI_KHOAN"
                                                FROM danh_muc_he_thong_tai_khoan TK
                                                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '622%%')
                                THEN SUM(JCA."SO_TIEN")
                                ELSE 0
                                END)    AS "OPN_NHAN_CONG"
                                , (CASE WHEN JCA."KY_TINH_GIA_THANH_CHI_TIET_ID" = JP."KY_TINH_GIA_THANH_CHI_TIET_ID"
                                            AND ((SELECT "SO_TAI_KHOAN"
                                                FROM danh_muc_he_thong_tai_khoan TK
                                                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '622%%')
                                THEN SUM(JCA."SO_TIEN")
                                ELSE 0
                                END)    AS "NHAN_CONG"
                                , (CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
                                            AND JCA."DEN_NGAY" < tu_ngay
                                            AND ((SELECT "SO_TAI_KHOAN"
                                                FROM danh_muc_he_thong_tai_khoan TK
                                                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '623%%')
                                THEN SUM(JCA."SO_TIEN")
                                ELSE 0
                                END)    AS "OPN_MAY_THI_CONG"
                                , (CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
                                            AND
                                            JCA."KY_TINH_GIA_THANH_CHI_TIET_ID" = JP."KY_TINH_GIA_THANH_CHI_TIET_ID"
                                            AND ((SELECT "SO_TAI_KHOAN"
                                                FROM danh_muc_he_thong_tai_khoan TK
                                                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '623%%')
                                THEN SUM(JCA."SO_TIEN")
                                ELSE 0
                                END)    AS "MAY_THI_CONG"
                                , (CASE WHEN JCA."DEN_NGAY" < tu_ngay
                                            AND ((SELECT "SO_TAI_KHOAN"
                                                FROM danh_muc_he_thong_tai_khoan TK
                                                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '627%%')
                                THEN SUM(JCA."SO_TIEN")
                                ELSE 0
                                END)    AS "OPN_CHI_PHI_CHUNG"
                                , (CASE WHEN JCA."KY_TINH_GIA_THANH_CHI_TIET_ID" = JP."KY_TINH_GIA_THANH_CHI_TIET_ID"
                                            AND ((SELECT "SO_TAI_KHOAN"
                                                FROM danh_muc_he_thong_tai_khoan TK
                                                WHERE TK.id = JCA."TAI_KHOAN_ID") LIKE '627%%')
                                THEN SUM(JCA."SO_TIEN")
                                ELSE 0
                                END)    AS "CHI_PHI_CHUNG"
                            FROM TMP_KY_TINH_GIA_THANH_CHI_TIET JP
                                -- Lấy ra các phân bổ của tất cả các kỳ tính giá thành trước đó và kỳ hiện tại có ĐTTHCP giống kỳ hiện tại
                                LEFT JOIN (SELECT
                                            JCAD.*
                                            , J."TU_NGAY"
                                            , J."DEN_NGAY"
                                        FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung JCAD
                                            INNER JOIN gia_thanh_ky_tinh_gia_thanh J ON J."id" = JCAD."KY_TINH_GIA_THANH_ID"
                                        WHERE J."DEN_NGAY" <=
                                                den_ngay --Lấy tất cả các lần phân bổ của kỳ tính giá thành hiện tại và trước đó

                                        ) JCA ON ((LOAI_GIA_THANH = 'CONG_TRINH'
                                                    AND JCA."MA_CONG_TRINH_ID" = JP."CONG_TRINH_ID"
                                                    )
                                                    OR (LOAI_GIA_THANH = 'DON_HANG'
                                                        AND JCA."SO_DON_HANG_ID" = JP."DON_DAT_HANG_ID"
                                                    )
                                                    OR (LOAI_GIA_THANH = 'HOP_DONG'
                                                        AND JCA."SO_HOP_DONG_ID" = JP."HOP_DONG_ID"
                                                    )
                                    )
                            WHERE JP."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id

                            GROUP BY
                                JP."KY_TINH_GIA_THANH_ID",
                                JP."KY_TINH_GIA_THANH_CHI_TIET_ID",
                                JCA."KY_TINH_GIA_THANH_CHI_TIET_ID",
                                JCA."DEN_NGAY",
                                (SELECT "SO_TAI_KHOAN"
                                FROM danh_muc_he_thong_tai_khoan TK
                                WHERE TK.id = JCA."TAI_KHOAN_ID")
                        ;


                        INSERT INTO TMP_LUU_DU_LIEU_CHI_PHI
                        ("KY_TINH_GIA_THANH_ID",
                        "KY_TINH_GIA_THANH_CHI_TIET_ID",
                        -- Số đã nghiệm thu
                        "SO_DA_NGHIEM_THU",
                        "OPN_SO_DA_NGHIEM_THU",
                        --NVL
                        "OPN_NGUYEN_VAT_LIEU",
                        "NGUYEN_VAT_LIEU",
                        --NC
                        "OPN_NHAN_CONG",
                        "NHAN_CONG",
                        --MTC
                        "OPN_MAY_THI_CONG",
                        "MAY_THI_CONG",
                        -- CPC
                        "OPN_CHI_PHI_CHUNG",
                        "CHI_PHI_CHUNG",
                        "KHOAN_GIAM_GIA_THANH"

                        )
                            SELECT
                                JP."KY_TINH_GIA_THANH_ID"
                                , JP."KY_TINH_GIA_THANH_CHI_TIET_ID"
                                , (CASE WHEN GL."NGAY_HACH_TOAN" <= den_ngay
                                            AND GL."MA_TAI_KHOAN" LIKE '632%%'
                                            AND GL."MA_TAI_KHOAN_DOI_UNG" LIKE '154%%'
                                THEN SUM("GHI_NO")
                                ELSE 0
                                END) AS "SO_DA_NGHIEM_THU"
                                , (CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                                            AND GL."MA_TAI_KHOAN" LIKE '632%%'
                                            AND GL."MA_TAI_KHOAN_DOI_UNG" LIKE '154%%'
                                THEN SUM("GHI_NO")
                                ELSE 0
                                END) AS "OPN_SO_DA_NGHIEM_THU"
                                , (CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                                            AND ((GL."MA_TAI_KHOAN" LIKE '621%%')
                                                AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
                                                        AND GL."LOAI_HACH_TOAN" = '2'
                                                    )
                                                    OR GL."LOAI_HACH_TOAN" = '1'
                                                )
                                                OR ("MA_TAI_KHOAN" LIKE N'154%%'
                                                    AND "LOAI_HACH_TOAN" = '1'
                                                    AND Gl."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%'
                                                    AND (LOAI_GIA_THANH <> 'CONG_TRINH'
                                                        OR (LOAI_GIA_THANH = 'CONG_TRINH'
                                                            AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '623%%'
                                                        )
                                                    )
                                                    AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%'
                                                    AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%'
                                                )
                                            ) -- các chứng từ PS Nợ TK 154 chi tiết theo từng đối tượng THCP
                                THEN SUM("GHI_NO"
                                        - "GHI_CO")
                                -- Chú ý: Với số lũy kế kỳ trước thì NVL đã trừ đi khoản giảm giá thành, còn phát sinh trong kỳ thì đưa ra 1 cột khoản giảm giá thành
                                WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                                        AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                                        AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '632%%'
                                            AND GL."LOAI_HACH_TOAN" = '2'
                                            )
                                            OR GL."LOAI_HACH_TOAN" = '1'
                                        )
                                    THEN -SUM("GHI_CO")
                                ELSE 0
                                END) AS "OPN_NGUYEN_VAT_LIEU"
                                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                                            AND ((GL."MA_TAI_KHOAN" LIKE '621%%')
                                                AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
                                                        AND GL."LOAI_HACH_TOAN" = '2'
                                                    )
                                                    OR GL."LOAI_HACH_TOAN" = '1'
                                                )
                                                OR ("MA_TAI_KHOAN" LIKE N'154%%'
                                                    AND "LOAI_HACH_TOAN" = '1'
                                                    AND Gl."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%'
                                                    AND (LOAI_GIA_THANH <> 'CONG_TRINH'
                                                        OR (LOAI_GIA_THANH = 'CONG_TRINH'
                                                            AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '623%%'
                                                        )
                                                    )
                                                    AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%'
                                                    AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%'
                                                )
                                            ) -- các chứng từ PS Nợ TK 154 chi tiết theo từng đối tượng THCP
                                THEN SUM("GHI_NO"
                                        - "GHI_CO")
                                ELSE 0
                                END) AS "NGUYEN_VAT_LIEU"
                                , --NC
                                (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay)
                                            AND (GL."MA_TAI_KHOAN" LIKE '622%%')
                                            AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
                                                AND GL."LOAI_HACH_TOAN" = '2'
                                                )
                                                OR GL."LOAI_HACH_TOAN" = '1'
                                            )
                                    THEN SUM("GHI_NO"
                                            - "GHI_CO")
                                ELSE 0
                                END) AS "OPN_NHAN_CONG"
                                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                                            AND (GL."MA_TAI_KHOAN" LIKE '622%%')
                                            AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
                                                AND GL."LOAI_HACH_TOAN" = '2'
                                                )
                                                OR GL."LOAI_HACH_TOAN" = '1'
                                            )
                                THEN SUM("GHI_NO"
                                        - "GHI_CO")
                                ELSE 0
                                END) AS "NHAN_CONG"
                                , --MTC
                                (CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
                                            AND (GL."NGAY_HACH_TOAN" < tu_ngay)
                                            AND (GL."MA_TAI_KHOAN" LIKE '623%%')
                                            AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
                                                AND GL."LOAI_HACH_TOAN" = '2'
                                                )
                                                OR GL."LOAI_HACH_TOAN" = '1'
                                            )
                                    THEN SUM("GHI_NO"
                                            - "GHI_CO")
                                ELSE 0
                                END) AS "OPN_MAY_THI_CONG"
                                , (CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
                                            AND (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                                            AND (GL."MA_TAI_KHOAN" LIKE '623%%')
                                            AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
                                                AND GL."LOAI_HACH_TOAN" = '2'
                                                )
                                                OR GL."LOAI_HACH_TOAN" = '1'
                                            )
                                THEN SUM("GHI_NO"
                                        - "GHI_CO")
                                ELSE 0
                                END) AS "MAY_THI_CONG"
                                , -- CPC
                                (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay)
                                            AND (GL."MA_TAI_KHOAN" LIKE '627%%')
                                            AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
                                                AND GL."LOAI_HACH_TOAN" = '2'
                                                )
                                                OR GL."LOAI_HACH_TOAN" = '1'
                                            )
                                    THEN SUM("GHI_NO"
                                            - "GHI_CO")
                                ELSE 0
                                END)    "OPN_CHI_PHI_CHUNG"
                                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                                            AND (GL."MA_TAI_KHOAN" LIKE '627%%')
                                            AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
                                                AND GL."LOAI_HACH_TOAN" = '2'
                                                )
                                                OR GL."LOAI_HACH_TOAN" = '1'
                                            )
                                THEN SUM("GHI_NO"
                                        - "GHI_CO")
                                ELSE 0
                                END) AS "CHI_PHI_CHUNG"
                                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                                            AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                                            AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '632%%'
                                                AND GL."LOAI_HACH_TOAN" = '2'
                                                )
                                                OR GL."LOAI_HACH_TOAN" = '1'
                                            )
                                THEN SUM(GL."GHI_CO")
                                ELSE 0
                                END) AS "KHOAN_GIAM_GIA_THANH"
                            FROM TMP_KY_TINH_GIA_THANH_CHI_TIET JP
                                LEFT JOIN so_cai_chi_tiet GL ON ((LOAI_GIA_THANH = 'CONG_TRINH'
                                                                AND GL."CONG_TRINH_ID" = JP."CONG_TRINH_ID"
                                                                )
                                                                OR (LOAI_GIA_THANH = 'DON_HANG'
                                                                    AND GL."DON_DAT_HANG_ID" = JP."DON_DAT_HANG_ID"
                                                                )
                                                                OR (LOAI_GIA_THANH = 'HOP_DONG'
                                                                    AND GL."HOP_DONG_BAN_ID" = JP."HOP_DONG_ID"
                                                                )
                                    )
                            WHERE JP."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                                AND GL."NGAY_HACH_TOAN" <= den_ngay
                                AND GL."CHI_NHANH_ID" = chi_nhanh_id

                                AND ((LOAI_GIA_THANH = 'CONG_TRINH'
                                        AND GL."CONG_TRINH_ID" IS NOT NULL
                                    )
                                    OR (LOAI_GIA_THANH = 'DON_HANG'
                                        AND GL."DON_DAT_HANG_ID" IS NOT NULL
                                    )
                                    OR (LOAI_GIA_THANH = 'HOP_DONG'
                                        AND GL."HOP_DONG_BAN_ID" IS NOT NULL
                                    )
                                )
                                -- Ntquang 12/07/2018 : sửa bug SMESEVEN-24596
                                AND (GL."LOAI_CHUNG_TU" <> '610'
                                    OR (GL."LOAI_CHUNG_TU" = '610'
                                        AND GL."MA_TAI_KHOAN" NOT LIKE '154%%'
                                    )
                                )
                            GROUP BY
                                JP."KY_TINH_GIA_THANH_ID",
                                JP."KY_TINH_GIA_THANH_CHI_TIET_ID",
                                GL."MA_TAI_KHOAN",
                                GL."CHI_NHANH_ID",
                                GL."NGAY_HACH_TOAN",
                                GL."MA_TAI_KHOAN_DOI_UNG",
                                GL."LOAI_HACH_TOAN"

                        ;


                    ELSE -- QD48--------------------------------------------------------


                        INSERT INTO TMP_LUU_DU_LIEU_CHI_PHI
                        ("KY_TINH_GIA_THANH_ID",
                        "KY_TINH_GIA_THANH_CHI_TIET_ID",
                        --NVL
                        "OPN_NGUYEN_VAT_LIEU",
                        "NGUYEN_VAT_LIEU",
                        --NC
                        "OPN_NHAN_CONG",
                        "NHAN_CONG",
                        --MTC
                        "OPN_MAY_THI_CONG",
                        "MAY_THI_CONG",
                        -- CPC
                        "OPN_CHI_PHI_CHUNG",
                        "CHI_PHI_CHUNG"
                        )
                            SELECT
                                JP."KY_TINH_GIA_THANH_ID"
                                , JP."KY_TINH_GIA_THANH_CHI_TIET_ID"
                                , (CASE WHEN JCA."DEN_NGAY" < tu_ngay
                                            AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                                                                        || '%%')
                                THEN SUM(JCA."SO_TIEN")
                                ELSE 0
                                END)    AS "OPN_NGUYEN_VAT_LIEU"
                                , (-- Nếu có JCAJC"PHAT_SINH_TRONG_KY"DetailID=JP."KY_TINH_GIA_THANH_CHI_TIET_ID"
                                    CASE WHEN JCA."KY_TINH_GIA_THANH_CHI_TIET_ID" = JP."KY_TINH_GIA_THANH_CHI_TIET_ID"
                                                AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                                                                            || '%%')
                                        THEN SUM(JCA."SO_TIEN")
                                    ELSE 0
                                    END) AS "NGUYEN_VAT_LIEU"
                                , (CASE WHEN JCA."DEN_NGAY" < tu_ngay
                                            AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                                                                        || '%%')
                                THEN SUM(JCA."SO_TIEN")
                                ELSE 0
                                END)    AS "OPN_NHAN_CONG"
                                , (CASE WHEN JCA."KY_TINH_GIA_THANH_CHI_TIET_ID" = JP."KY_TINH_GIA_THANH_CHI_TIET_ID"
                                            AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                                                                        || '%%')
                                THEN SUM(JCA."SO_TIEN")
                                ELSE 0
                                END)    AS "NHAN_CONG"
                                , (CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
                                            AND JCA."DEN_NGAY" < tu_ngay
                                            AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                                                                        || '%%')
                                THEN SUM(JCA."SO_TIEN")
                                ELSE 0
                                END)    AS "OPN_MAY_THI_CONG"
                                , (CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
                                            AND JCA."KY_TINH_GIA_THANH_CHI_TIET_ID" = JP."KY_TINH_GIA_THANH_CHI_TIET_ID"
                                            AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                                                                        || '%%')
                                THEN SUM(JCA."SO_TIEN")
                                ELSE 0
                                END)    AS "MAY_THI_CONG"
                                , (CASE WHEN JCA."DEN_NGAY" < tu_ngay
                                            AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                                                                        || '%%')
                                THEN SUM(JCA."SO_TIEN")
                                ELSE 0
                                END)    AS "OPN_CHI_PHI_CHUNG"
                                , (CASE WHEN JCA."KY_TINH_GIA_THANH_CHI_TIET_ID" = JP."KY_TINH_GIA_THANH_CHI_TIET_ID"
                                            AND (JCA."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                                                                        || '%%')
                                THEN SUM(JCA."SO_TIEN")
                                ELSE 0
                                END)    AS "CHI_PHI_CHUNG"
                            FROM TMP_KY_TINH_GIA_THANH_CHI_TIET JP
                                -- Lấy ra các phân bổ của tất cả các kỳ tính giá thành trước đó và kỳ hiện tại có ĐTTHCP giống kỳ hiện tại
                                LEFT JOIN (SELECT
                                            JCAD.*
                                            , J."TU_NGAY"
                                            , J."DEN_NGAY"
                                            , E."MA_PHAN_CAP"
                                        FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung JCAD
                                            INNER JOIN gia_thanh_ky_tinh_gia_thanh J ON J."id" = JCAD."KY_TINH_GIA_THANH_ID"
                                            LEFT JOIN danh_muc_khoan_muc_cp E ON E."id" = JCAD."KHOAN_MUC_CP_ID"
                                        WHERE J."DEN_NGAY" <=
                                                den_ngay --Lấy tất cả các lần phân bổ của kỳ tính giá thành hiện tại và trước đó

                                        ) JCA ON ((LOAI_GIA_THANH = 'CONG_TRINH'
                                                    AND JCA."MA_CONG_TRINH_ID" = JP."CONG_TRINH_ID"
                                                    )
                                                    OR (LOAI_GIA_THANH = 'DON_HANG'
                                                        AND JCA."SO_DON_HANG_ID" = JP."DON_DAT_HANG_ID"
                                                    )
                                                    OR (LOAI_GIA_THANH = 'HOP_DONG'
                                                        AND JCA."SO_HOP_DONG_ID" = JP."HOP_DONG_ID"
                                                    )
                                    )
                            WHERE JP."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id

                                AND JCA."KHOAN_MUC_CP_ID" IS NOT NULL
                            GROUP BY JP."KY_TINH_GIA_THANH_ID",
                                JP."KY_TINH_GIA_THANH_CHI_TIET_ID",
                                JCA."KY_TINH_GIA_THANH_CHI_TIET_ID",
                                JCA."DEN_NGAY",
                                (SELECT "SO_TAI_KHOAN"
                                FROM danh_muc_he_thong_tai_khoan TK
                                WHERE TK.id = JCA."TAI_KHOAN_ID"),
                                JCA."MA_PHAN_CAP"
                        ;


                        INSERT INTO TMP_LUU_DU_LIEU_CHI_PHI
                        ("KY_TINH_GIA_THANH_ID",
                        "KY_TINH_GIA_THANH_CHI_TIET_ID",
                        -- Số đã nghiệm thu
                        "SO_DA_NGHIEM_THU",
                        "OPN_SO_DA_NGHIEM_THU",
                        --NVL
                        "OPN_NGUYEN_VAT_LIEU",
                        "NGUYEN_VAT_LIEU",
                        --NC
                        "OPN_NHAN_CONG",
                        "NHAN_CONG",
                        --MTC
                        "OPN_MAY_THI_CONG",
                        "MAY_THI_CONG",
                        -- CPC
                        "OPN_CHI_PHI_CHUNG",
                        "CHI_PHI_CHUNG",

                        -- Khoản giảm giá thành
                        "KHOAN_GIAM_GIA_THANH"
                        )
                            SELECT
                                JP."KY_TINH_GIA_THANH_ID"
                                , JP."KY_TINH_GIA_THANH_CHI_TIET_ID"
                                , (CASE WHEN (GL."NGAY_HACH_TOAN" <= den_ngay)
                                            AND (GL."MA_TAI_KHOAN" LIKE '632%%')
                                            AND (GL."MA_TAI_KHOAN_DOI_UNG" LIKE '154%%')
                                            AND (GL."MA_PHAN_CAP" IS NULL
                                                OR GL."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX
                                                                            || '%%'
                                            )
                                THEN SUM("GHI_NO")
                                ELSE 0
                                END) AS "SO_DA_NGHIEM_THU"
                                , (CASE WHEN (GL."NGAY_HACH_TOAN" <= tu_ngay)
                                            AND (GL."MA_TAI_KHOAN" LIKE '632%%')
                                            AND (GL."MA_TAI_KHOAN_DOI_UNG" LIKE '154%%')
                                            AND (GL."MA_PHAN_CAP" IS NULL
                                                OR GL."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX
                                                                            || '%%'
                                            )
                                THEN SUM("GHI_NO")
                                ELSE 0
                                END) AS "OPN_SO_DA_NGHIEM_THU"
                                , (CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                                            AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                                            AND (GL."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                                                                        || '%%')
                                THEN SUM("GHI_NO"
                                        - "GHI_CO")
                                WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                                        AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                                        AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '632%%'
                                            AND GL."LOAI_HACH_TOAN" = '2'
                                            )
                                            OR GL."LOAI_HACH_TOAN" = '1'
                                        )
                                        AND (GL."MA_PHAN_CAP" IS NULL
                                            OR GL."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX
                                                                        || '%%'
                                        )
                                    THEN -SUM("GHI_CO")
                                ELSE 0
                                END)
                                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                                            AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                                            AND (GL."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                                                                        || '%%')
                                THEN SUM("GHI_NO"
                                        - "GHI_CO")
                                ELSE 0
                                END) AS "NGUYEN_VAT_LIEU"
                                , --NC
                                (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay)
                                            AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                                            AND (GL."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                                                                        || '%%')
                                    THEN SUM("GHI_NO"
                                            - "GHI_CO")
                                ELSE 0
                                END) AS "OPN_NHAN_CONG"
                                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                                            AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                                            AND (GL."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                                                                        || '%%')
                                THEN SUM("GHI_NO"
                                        - "GHI_CO")
                                ELSE 0
                                END) AS "NHAN_CONG"
                                , --MTC
                                (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay)
                                            AND LOAI_GIA_THANH = 'CONG_TRINH'
                                            AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                                            AND (GL."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                                                                        || '%%')
                                    THEN SUM("GHI_NO"
                                            - "GHI_CO")
                                ELSE 0
                                END) AS "OPN_MAY_THI_CONG"
                                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                                            AND LOAI_GIA_THANH = 'CONG_TRINH'
                                            AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                                            AND (GL."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                                                                        || '%%')
                                THEN SUM("GHI_NO"
                                        - "GHI_CO")
                                ELSE 0
                                END) AS "MAY_THI_CONG"
                                , -- CPC
                                (CASE WHEN (GL."NGAY_HACH_TOAN" < tu_ngay)
                                            AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                                            AND (GL."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                                                                        || '%%')
                                    THEN SUM("GHI_NO"
                                            - "GHI_CO")
                                ELSE 0
                                END) AS "OPN_CHI_PHI_CHUNG"
                                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                                            AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                                            AND (GL."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                                                                        || '%%')
                                THEN SUM("GHI_NO"
                                        - "GHI_CO")
                                ELSE 0
                                END) AS "CHI_PHI_CHUNG"
                                , (CASE WHEN (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)
                                            AND (GL."MA_TAI_KHOAN" LIKE '154%%')
                                            AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '632%%'
                                                AND GL."LOAI_HACH_TOAN" = '2'
                                                )
                                                OR GL."LOAI_HACH_TOAN" = '1'
                                            )
                                            AND (GL."MA_PHAN_CAP" IS NULL
                                                OR GL."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX
                                                                            || '%%'
                                            )
                                THEN SUM(GL."GHI_CO")
                                ELSE 0
                                END) AS "KHOAN_GIAM_GIA_THANH"
                            FROM TMP_KY_TINH_GIA_THANH_CHI_TIET JP
                                LEFT JOIN (SELECT
                                            GL.*
                                            , E."MA_PHAN_CAP"
                                        FROM so_cai_chi_tiet GL
                                            LEFT JOIN danh_muc_khoan_muc_cp E ON GL."KHOAN_MUC_CP_ID" = E."id"
                                        -- Ntquang 12/07/2018 : sửa bug SMESEVEN-24596
                                        WHERE (GL."LOAI_CHUNG_TU" <> '610'
                                                OR (GL."LOAI_CHUNG_TU" = '610'
                                                    AND GL."MA_TAI_KHOAN" NOT LIKE '154%%'
                                                )
                                        )
                                        ) GL ON ((LOAI_GIA_THANH = 'CONG_TRINH'
                                                    AND GL."CONG_TRINH_ID" = JP."CONG_TRINH_ID"
                                                )
                                                OR (LOAI_GIA_THANH = 'DON_HANG'
                                                    AND GL."DON_DAT_HANG_ID" = JP."DON_DAT_HANG_ID"
                                                )
                                                OR (LOAI_GIA_THANH = 'HOP_DONG'
                                                    AND GL."HOP_DONG_BAN_ID" = JP."HOP_DONG_ID"
                                                )
                                    )
                            WHERE JP."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                                AND GL."NGAY_HACH_TOAN" <= den_ngay
                                AND GL."CHI_NHANH_ID" = chi_nhanh_id

                                AND ((LOAI_GIA_THANH = 'CONG_TRINH'
                                        AND GL."CONG_TRINH_ID" IS NOT NULL
                                    )
                                    OR (LOAI_GIA_THANH = 'DON_HANG'
                                        AND GL."DON_DAT_HANG_ID" IS NOT NULL
                                    )
                                    OR (LOAI_GIA_THANH = 'HOP_DONG'
                                        AND GL."HOP_DONG_BAN_ID" IS NOT NULL
                                    )
                                )
                            GROUP BY JP."KY_TINH_GIA_THANH_ID",
                                "KY_TINH_GIA_THANH_CHI_TIET_ID",
                                GL."CHI_NHANH_ID",
                                GL."NGAY_HACH_TOAN",
                                GL."MA_TAI_KHOAN",
                                GL."MA_TAI_KHOAN_DOI_UNG",
                                GL."MA_PHAN_CAP",
                                GL."LOAI_HACH_TOAN"
                        ;
                    END IF
                    ;

                    DROP TABLE IF EXISTS TMP_KET_QUA
                    ;

                    CREATE TEMP TABLE TMP_KET_QUA
                        AS


                            SELECT

                                ROW_NUMBER()
                                OVER (
                                    ORDER BY
                                        PW."MA_PHAN_CAP",
                                        "BAC",
                                        PW."MA_CONG_TRINH",
                                        PWC."name",
                                        SO."NGAY_DON_HANG",
                                        SO."SO_DON_HANG",
                                        CASE WHEN LOAI_GIA_THANH = 'HOP_DONG'
                                            THEN CASE WHEN CT."THUOC_DU_AN_ID" IS NOT NULL
                                                THEN CT2."SO_HOP_DONG"
                                                ELSE CT."SO_HOP_DONG"
                                                END
                                        END,
                                        CT."SO_HOP_DONG",
                                        CT."NGAY_KY" )                                     AS "RowNumber"

                                , JP."DOI_TUONG_THCP_ID"
                                , JP."CONG_TRINH_ID"
                                , JP."DON_DAT_HANG_ID"
                                , JP."HOP_DONG_ID"
                                , -- Lũy kế chi phí
                                COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0))
                                        + SUM(COALESCE(CC."OPN_NHAN_CONG", 0))
                                        + SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0))
                                        + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0))
                                        + SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0))
                                        + SUM(COALESCE(CC."NHAN_CONG", 0))
                                        + SUM(COALESCE(CC."MAY_THI_CONG", 0))
                                        + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0))
                                        - SUM(COALESCE(CC."KHOAN_GIAM_GIA_THANH", 0)),
                                        0)                                                AS "LUY_KE_CHI_PHI"
                                , -- Lũy kế đã nghiệm thu
                                COALESCE(SUM(COALESCE(CC."SO_DA_NGHIEM_THU", 0)),
                                        0)                                                AS "LUY_KE_DA_NGHIEM_THU"
                                , COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU",
                                                        0))
                                        + SUM(COALESCE(CC."OPN_NHAN_CONG",
                                                        0))
                                        + SUM(COALESCE(CC."OPN_MAY_THI_CONG",
                                                        0))
                                        + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG",
                                                        0))

                                        - SUM(COALESCE(CC."OPN_SO_DA_NGHIEM_THU",
                                                        0)), 0)                            AS "SO_CHUA_NGHIEM_THU_DAU_KY"
                                , -- Số chưa nghiệm thu
                                COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0))
                                        + SUM(COALESCE(CC."OPN_NHAN_CONG", 0))
                                        + SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0))
                                        + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0))
                                        + SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0))
                                        + SUM(COALESCE(CC."NHAN_CONG", 0))
                                        + SUM(COALESCE(CC."MAY_THI_CONG", 0))
                                        + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0))
                                        - SUM(COALESCE(CC."KHOAN_GIAM_GIA_THANH", 0))
                                        - SUM(COALESCE(CC."SO_DA_NGHIEM_THU", 0)),
                                        0)                                                AS "SO_CHUA_NGHIEM_THU_CUOI_KY"
                                , -- Lũy kế kỳ trước
                                COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU",
                                                        0)), 0)                              AS "LUY_KE_KY_TRUOC_NVL_TRUC_TIEP"
                                , COALESCE(SUM(COALESCE(CC."OPN_NHAN_CONG",
                                                        0)), 0)                              AS "LUY_KE_KY_TRUOC_NC_TRUC_TIEP"
                                , COALESCE(SUM(COALESCE(CC."OPN_MAY_THI_CONG",
                                                        0)), 0)                              AS "LUY_KE_KY_TRUOC_MTC"
                                , COALESCE(SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG",
                                                        0)), 0)                              AS "LUY_KE_KY_TRUOC_CP_CHUNG"
                                , COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU",
                                                        0))
                                        + SUM(COALESCE(CC."OPN_NHAN_CONG",
                                                        0))
                                        + SUM(COALESCE(CC."OPN_MAY_THI_CONG",
                                                        0))
                                        + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG",
                                                        0)), 0)                            AS "LUY_KE_KY_TRUOC_TONG"
                                , -- Lũy kế phát sinh trong kỳ
                                COALESCE(SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0)),
                                        0)                                                AS "PHAT_SINH_NVL_TRUC_TIEP"
                                , COALESCE(SUM(COALESCE(CC."NHAN_CONG", 0)), 0)              AS "PHAT_SINH_NHAN_CONG_TRUC_TIEP"
                                , COALESCE(SUM(COALESCE(CC."MAY_THI_CONG", 0)), 0)           AS "PHAT_SINH_MAY_THI_CONG"
                                , COALESCE(SUM(COALESCE(CC."CHI_PHI_CHUNG", 0)), 0)          AS "PHAT_SINH_CHI_PHI_CHUNG"
                                , COALESCE(SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0))
                                        + SUM(COALESCE(CC."NHAN_CONG", 0))
                                        + SUM(COALESCE(CC."MAY_THI_CONG", 0))
                                        + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0)), 0)        AS "PHAT_SINH_TONG"
                                , -- Khoản giảm chi phí
                                COALESCE(SUM(COALESCE("KHOAN_GIAM_GIA_THANH", 0)), 0)      AS "KHOAN_GIAM_GIA_THANH"
                                , -- Lũy kế chi phí
                                COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU",
                                                        0))
                                        + SUM(COALESCE(CC."NGUYEN_VAT_LIEU",
                                                        0))
                                        - SUM(COALESCE("KHOAN_GIAM_GIA_THANH",
                                                        0)), 0)                            AS "LUY_KE_CP_NVL_TRUC_TIEP"
                                , COALESCE(SUM(COALESCE(CC."OPN_NHAN_CONG",
                                                        0))
                                        + SUM(COALESCE(CC."NHAN_CONG", 0)),
                                        0)                                                AS "LUY_KE_CP_NC_TRUC_TIEP"
                                , COALESCE(SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0))
                                        + SUM(COALESCE(CC."MAY_THI_CONG", 0)),
                                        0)                                                AS "LUY_KE_CP_MAY_THI_CONG"
                                , COALESCE(SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0))
                                        + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0)),
                                        0)                                                AS "LUY_KE_CP_CHI_PHI_CHUNG"
                                , COALESCE(SUM(COALESCE(CC."OPN_NGUYEN_VAT_LIEU", 0))
                                        + SUM(COALESCE(CC."OPN_NHAN_CONG", 0))
                                        + SUM(COALESCE(CC."OPN_MAY_THI_CONG", 0))
                                        + SUM(COALESCE(CC."OPN_CHI_PHI_CHUNG", 0))
                                        + SUM(COALESCE(CC."NGUYEN_VAT_LIEU", 0))
                                        + SUM(COALESCE(CC."NHAN_CONG", 0))
                                        + SUM(COALESCE(CC."MAY_THI_CONG", 0))
                                        + SUM(COALESCE(CC."CHI_PHI_CHUNG", 0)),
                                        0)
                                - COALESCE(SUM(COALESCE(CC."KHOAN_GIAM_GIA_THANH", 0)), 0) AS "LUY_KE_CP_TONG"
                                , (CASE WHEN LOAI_GIA_THANH = 'DON_HANG'
                                THEN SO."SO_DON_HANG"
                                WHEN LOAI_GIA_THANH = 'HOP_DONG'
                                    THEN CT."SO_HOP_DONG"
                                END)                                                      AS "SO_CHUNG_TU"
                                , (CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
                                THEN NULL
                                WHEN LOAI_GIA_THANH = 'DON_HANG'
                                    THEN SO."NGAY_DON_HANG"
                                WHEN LOAI_GIA_THANH = 'HOP_DONG'
                                    THEN CT."NGAY_KY"
                                END)                                                      AS "NGAY_CHUNG_TU"
                                , (CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
                                THEN PW."TEN_CONG_TRINH"
                                WHEN LOAI_GIA_THANH = 'DON_HANG'
                                    THEN AO."HO_VA_TEN"
                                WHEN LOAI_GIA_THANH = 'HOP_DONG'
                                    THEN AO."HO_VA_TEN"
                                END)                                                      AS "TEN_DOI_TUONG"
                                , (CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
                                THEN PWC."name"
                                WHEN LOAI_GIA_THANH = 'DON_HANG'
                                    THEN NULL
                                WHEN LOAI_GIA_THANH = 'HOP_DONG'
                                    THEN CT."TRICH_YEU"
                                END)                                                      AS "TRICH_YEU"


                                , (CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
                                THEN PW."BAC"
                                WHEN LOAI_GIA_THANH = 'DON_HANG'
                                    THEN 0
                                WHEN LOAI_GIA_THANH = 'HOP_DONG'
                                    THEN CASE WHEN CT."isparent" = TRUE
                                                    OR CT."THUOC_DU_AN_ID" IS NULL
                                                    OR NOT EXISTS(SELECT *
                                                                    FROM
                                                                        gia_thanh_ky_tinh_gia_thanh_chi_tiet
                                                                    WHERE
                                                                        "SO_HOP_DONG_ID" = CT."THUOC_DU_AN_ID")
                                        THEN 1
                                            ELSE 2
                                            END
                                END)                                                      AS "BAC"
                                , PW."MA_PHAN_CAP"


                                , PW."MA_CONG_TRINH"
                                , CT."SO_HOP_DONG"
                            FROM TMP_KY_TINH_GIA_THANH_CHI_TIET JP
                                LEFT JOIN TMP_LUU_DU_LIEU_CHI_PHI CC
                                    ON JP."KY_TINH_GIA_THANH_CHI_TIET_ID" = CC."KY_TINH_GIA_THANH_CHI_TIET_ID"
                                    AND JP."KY_TINH_GIA_THANH_ID" = CC."KY_TINH_GIA_THANH_ID"
                                LEFT JOIN danh_muc_cong_trinh AS PW ON (LOAI_GIA_THANH = 'CONG_TRINH'
                                                                        AND JP."CONG_TRINH_ID" = PW."id"
                                    )
                                LEFT JOIN danh_muc_loai_cong_trinh AS PWC ON PW."LOAI_CONG_TRINH" = PWC."id"
                                LEFT JOIN account_ex_don_dat_hang AS SO ON (LOAI_GIA_THANH = 'DON_HANG'
                                                                            AND so."id" = JP."DON_DAT_HANG_ID"
                                    )
                                LEFT JOIN sale_ex_hop_dong_ban AS CT ON LOAI_GIA_THANH = 'HOP_DONG'
                                                                        AND JP."HOP_DONG_ID" = CT."id"
                                LEFT JOIN sale_ex_hop_dong_ban CT2 ON CT."THUOC_DU_AN_ID" = CT2."id"
                                LEFT JOIN res_partner AS AO ON CT."KHACH_HANG_ID" = AO."id"
                                                            OR SO."KHACH_HANG_ID" = AO."id"
                            WHERE JP."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                            GROUP BY
                                JP."DOI_TUONG_THCP_ID",
                                JP."CONG_TRINH_ID",
                                JP."DON_DAT_HANG_ID",
                                JP."HOP_DONG_ID",
                                PW."MA_CONG_TRINH",
                                PW."TEN_CONG_TRINH",
                                PWC."name",
                                SO."SO_DON_HANG",
                                SO."NGAY_DON_HANG",
                                CT."SO_HOP_DONG",
                                CT."NGAY_KY",
                                AO."HO_VA_TEN",
                                CT."TRICH_YEU",

                                PW."BAC",
                                PW."MA_PHAN_CAP",

                                PW."parent_id",
                                CT."THUOC_DU_AN_ID",
                                CT2."SO_HOP_DONG",
                                CT."THUOC_DU_AN_ID",
                                CT."isparent"

                            ORDER BY
                                PW."MA_PHAN_CAP",
                                "BAC",
                                PW."MA_CONG_TRINH",
                                PWC."name",
                                SO."NGAY_DON_HANG",
                                SO."SO_DON_HANG",
                                CASE WHEN LOAI_GIA_THANH = 'HOP_DONG'
                                    THEN CASE WHEN CT."THUOC_DU_AN_ID" IS NOT NULL
                                        THEN CT2."SO_HOP_DONG"
                                        ELSE CT."SO_HOP_DONG"
                                        END
                                END,
                                CT."SO_HOP_DONG",
                                CT."NGAY_KY"
                    ;

                END $$
                ;

                SELECT
                    ct."MA_CONG_TRINH"
                    , ct."TEN_CONG_TRINH"
                    , lct.name AS "TEN_LOAI_CONG_TRINH"
                    , ddh."SO_DON_HANG"
                    , ddh."NGAY_DON_HANG"
                    , hdb."SO_HOP_DONG"
                    , hdb."NGAY_KY"
                    , CASE WHEN kq."DON_DAT_HANG_ID" NOTNULL
                    THEN ddh."TEN_KHACH_HANG"
                    WHEN kq."HOP_DONG_ID" NOTNULL
                        THEN hdb."TEN_KHACH_HANG"
                    ELSE '' END "TEN_KHACH_HANG",
                    kq.*
                FROM TMP_KET_QUA kq
                    LEFT JOIN danh_muc_cong_trinh ct ON kq."CONG_TRINH_ID" = ct.id
                    LEFT JOIN danh_muc_loai_cong_trinh lct ON ct."LOAI_CONG_TRINH" = lct.id
                    LEFT JOIN account_ex_don_dat_hang ddh ON kq."DON_DAT_HANG_ID" = ddh.id
                    LEFT JOIN sale_ex_hop_dong_ban hdb ON kq."HOP_DONG_ID" = hdb.id
                ORDER BY "RowNumber"
                ;

 
        """  
        return self.execute(query, params)