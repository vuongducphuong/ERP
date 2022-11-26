# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_TAP_HOP_CHI_PHI_TRUC_TIEP(models.Model):
    _name = 'gia.thanh.tap.hop.chi.phi.truc.tiep'
    _description = ''
    _auto = False

    KY_TINH_GIA_THANH = fields.Char(string='Kỳ tính giá thành', help='Kỳ tính giá thành')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(GIA_THANH_TAP_HOP_CHI_PHI_TRUC_TIEP, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result
    GIA_THANH_TAP_HOP_CHI_PHI_TRUC_TIEP_CHI_TIET_IDS = fields.One2many('gia.thanh.tap.hop.chi.phi.truc.tiep.chi.tiet', 'CHI_TIET_ID', string='Tập hợp chi phí trực tiếp chi tiết')
    CHE_DO_KE_TOAN = fields.Char(string='Chế độ kế toán', help='Chế độ kế toán')


    @api.model
    def default_get(self, fields):
        rec = super(GIA_THANH_TAP_HOP_CHI_PHI_TRUC_TIEP, self).default_get(fields)
        rec['CHE_DO_KE_TOAN'] = self.env['ir.config_parameter'].get_param('he_thong.CHE_DO_KE_TOAN')
        return rec


    def lay_du_lieu_tap_hop_chi_phi_truc_tiep(self, args):
        new_line_ket_chuyen_chi_phi_chi_tiet = [[5]]
        ky_tinh_gia_thanh_id = args.get('ky_tinh_gia_thanh_id')
        chi_nhanh_id = self.get_chi_nhanh()
        du_lieu_tap_hop_chi_phi_truc_tiep = self.lay_du_lieu_tap_hop_cptt(ky_tinh_gia_thanh_id,chi_nhanh_id)
        if du_lieu_tap_hop_chi_phi_truc_tiep:
            for line in du_lieu_tap_hop_chi_phi_truc_tiep:
                # dien_giai = 'Kết chuyển chi phí ' + str(line.get('TK_CO')) + ' của đối tượng ' + str(line.get('TEN_DOI_TUONG_THCP'))
                new_line_ket_chuyen_chi_phi_chi_tiet += [(0,0,{
                            'MA_DOI_TUONG_THCP_ID' : [line.get('DOI_TUONG_THCP_ID'),line.get('MA_DOI_TUONG_THCP')],
                            'MA_CONG_TRINH_ID' : [line.get('CONG_TRINH_ID'),line.get('MA_CONG_TRINH')],
                            'SO_DON_HANG_ID' : [line.get('DON_DAT_HANG_ID'),line.get('DON_DAT_HANG')],
                            'HOP_DONG_BAN_ID' : [line.get('HOP_DONG_BAN_ID'),line.get('SO_HOP_DONG')],

							'NGAY_HACH_TOAN' : line.get('NGAY_HACH_TOAN'),
                            'NGAY_CHUNG_TU' : line.get('NGAY_CHUNG_TU'),
                            'SO_CHUNG_TU' : line.get('SO_CHUNG_TU'),
							'LOAI_CHUNG_TU' : line.get('TEN_LOAI_CHUNG_TU'),
                            'DIEN_GIAI' : line.get('DIEN_GIAI_CHUNG'),
							'TK_CHI_PHI_ID' : [line.get('TAI_KHOAN_ID'),line.get('MA_TAI_KHOAN')],
                            'MA_KHOAN_MUC_CP' : line.get('MA_KHOAN_MUC_CP'),
                            'TEN_KHOAN_MUC_CP' : line.get('TEN_KHOAN_MUC_CP'),
							'SO_TIEN' : line.get('SO_TIEN'),
							'TEN_DOI_TUONG_THCP' : line.get('TEN_DOI_TUONG_THCP'),
                            'TEN_CONG_TRINH' : line.get('TEN_CONG_TRINH'),
                            })]
        return {'GIA_THANH_TAP_HOP_CHI_PHI_TRUC_TIEP_CHI_TIET_IDS' : new_line_ket_chuyen_chi_phi_chi_tiet}


    def lay_du_lieu_tap_hop_cptt(self,ky_tinh_gia_thanh_id,chi_nhanh_id):
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
                
                
                    IF LOAI_GIA_THANH = 'CONG_TRINH' -- Công trình
                    THEN
                
                        DROP TABLE IF EXISTS TMP_CONG_TRINH
                        ;
                
                        CREATE TEMP TABLE TMP_CONG_TRINH
                        (
                            "CONG_TRINH_ID"  INT,
                            "MA_CONG_TRINH"  VARCHAR(25),
                            "TEN_CONG_TRINH" VARCHAR(128)
                        )
                        ;
                
                        INSERT INTO TMP_CONG_TRINH
                        ("CONG_TRINH_ID",
                         "MA_CONG_TRINH",
                         "TEN_CONG_TRINH"
                        )
                            SELECT
                                JPD."MA_CONG_TRINH_ID"
                                , PW."MA_CONG_TRINH"
                                , PW."TEN_CONG_TRINH"
                            FROM gia_thanh_ky_tinh_gia_thanh_chi_tiet AS JPD
                                INNER JOIN danh_muc_cong_trinh AS PW ON JPD."MA_CONG_TRINH_ID" = PW."id"
                            WHERE "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                        ;
                
                        DROP TABLE IF EXISTS TMP_KET_QUA
                        ;
                
                        IF CHE_DO_KE_TOAN = '15'
                        THEN
                            CREATE TEMP TABLE TMP_KET_QUA
                                AS
                                    SELECT
                                        "ID_CHUNG_TU"
                                        , "MODEL_CHUNG_TU"
                                        , "SO_CHUNG_TU"
                                        , "LOAI_CHUNG_TU"
                                        , "TEN_LOAI_CHUNG_TU"
                                        , "NGAY_CHUNG_TU"
                                        , "NGAY_HACH_TOAN"
                                        , "DIEN_GIAI_CHUNG"
                                        , "TAI_KHOAN_ID"
                                        , "MA_TAI_KHOAN"
                                        , SUM(COALESCE("GHI_NO", 0)
                                              - COALESCE("GHI_CO", 0)) AS "SO_TIEN"
                                        ,GL."CONG_TRINH_ID"
                                        , "MA_CONG_TRINH"
                                        , "TEN_CONG_TRINH"
                                    FROM so_cai_chi_tiet AS GL
                                        INNER JOIN TMP_CONG_TRINH AS PW ON GL."CONG_TRINH_ID" = PW."CONG_TRINH_ID"
                                    WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                          AND (("MA_TAI_KHOAN" LIKE '621%%'
                                                OR "MA_TAI_KHOAN" LIKE '622%%'
                                                OR "MA_TAI_KHOAN" LIKE '623%%'
                                                OR "MA_TAI_KHOAN" LIKE '627%%'
                                               )
                                               AND (("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND "LOAI_HACH_TOAN" = '2') OR
                                                    "LOAI_HACH_TOAN" = '1')
                
                                               OR ("MA_TAI_KHOAN" LIKE N'154%%' AND "LOAI_HACH_TOAN" = '1' AND
                                                   "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%' AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%'
                                                   AND
                                                   "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '623%%' AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%'))
                
                                          AND "CHI_NHANH_ID" = chi_nhanh_id
                                    GROUP BY
                                        "ID_CHUNG_TU",
                                        "MODEL_CHUNG_TU",
                                        "SO_CHUNG_TU",
                                        "LOAI_CHUNG_TU",
                                        "TEN_LOAI_CHUNG_TU",
                                        "NGAY_CHUNG_TU",
                                        "NGAY_HACH_TOAN",
                                        "DIEN_GIAI_CHUNG",
                                        "TAI_KHOAN_ID",
                                        "MA_TAI_KHOAN",
                                        GL."CONG_TRINH_ID",
                                        "MA_CONG_TRINH",
                                        "TEN_CONG_TRINH"
                                    ORDER BY "MA_CONG_TRINH",GL."CONG_TRINH_ID", "TEN_CONG_TRINH", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU",
                                        "MA_TAI_KHOAN"
                            ;
                
                        ELSE
                            CREATE TEMP TABLE TMP_KET_QUA
                                AS
                
                                    SELECT
                                        "ID_CHUNG_TU"
                                        , "MODEL_CHUNG_TU"
                                        , "SO_CHUNG_TU"
                                        , "LOAI_CHUNG_TU"
                                        , "TEN_LOAI_CHUNG_TU"
                                        , "NGAY_CHUNG_TU"
                                        , "NGAY_HACH_TOAN"
                                        , "DIEN_GIAI_CHUNG"
                                        , "TAI_KHOAN_ID"
                                        , "MA_TAI_KHOAN"
                                        , SUM(COALESCE("GHI_NO", 0)
                                              - COALESCE("GHI_CO", 0)) AS "SO_TIEN"
                                        ,GL."CONG_TRINH_ID"
                                        , "MA_CONG_TRINH"
                                        , "TEN_CONG_TRINH"
                                        , "MA_KHOAN_MUC_CP"
                                        , "TEN_KHOAN_MUC_CP"
                                    FROM so_cai_chi_tiet AS GL
                                        INNER JOIN TMP_CONG_TRINH AS PW ON GL."CONG_TRINH_ID" = PW."CONG_TRINH_ID"
                                        LEFT JOIN danh_muc_khoan_muc_cp AS EI ON EI."id" = GL."KHOAN_MUC_CP_ID"
                                    WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                          AND "MA_TAI_KHOAN" LIKE '154%%'
                
                                          AND EI."id" IS NOT NULL
                                          AND EI."MA_PHAN_CAP" LIKE MA_PHAN_CAPCPSX || '%%'
                
                                          AND "CHI_NHANH_ID" = chi_nhanh_id
                                    GROUP BY
                                        "ID_CHUNG_TU",
                                        "MODEL_CHUNG_TU",
                                        "SO_CHUNG_TU",
                                        "LOAI_CHUNG_TU",
                                        "TEN_LOAI_CHUNG_TU",
                                        "NGAY_CHUNG_TU",
                                        "NGAY_HACH_TOAN",
                                        "DIEN_GIAI_CHUNG",
                                        "TAI_KHOAN_ID",
                                        "MA_TAI_KHOAN",
                                        GL."CONG_TRINH_ID",
                                        "MA_CONG_TRINH",
                                        "TEN_CONG_TRINH",
                                        "MA_KHOAN_MUC_CP",
                                        "TEN_KHOAN_MUC_CP"
                                    ORDER BY "MA_CONG_TRINH",GL."CONG_TRINH_ID", "TEN_CONG_TRINH", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU",
                                        "MA_KHOAN_MUC_CP"
                
                            ;
                        END IF
                        ;
                
                
                    ELSE
                        DROP TABLE IF EXISTS TMP_DON_HANG
                        ;
                
                        IF LOAI_GIA_THANH = 'DON_HANG' --Đơn hàng
                        THEN
                
                            CREATE TEMP TABLE TMP_DON_HANG
                
                            (
                                "DON_DAT_HANG_ID" INT,
                                "DON_DAT_HANG"    VARCHAR(255)
                            )
                            ;
                
                            INSERT INTO TMP_DON_HANG
                            ("DON_DAT_HANG_ID",
                             "DON_DAT_HANG"
                            )
                                SELECT
                                    JPD."SO_DON_HANG_ID"
                                    , "SO_DON_HANG"
                                FROM gia_thanh_ky_tinh_gia_thanh_chi_tiet AS JPD
                                    INNER JOIN account_ex_don_dat_hang AS SO ON JPD."SO_DON_HANG_ID" = SO."id"
                                WHERE "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                            ;
                
                            DROP TABLE IF EXISTS TMP_KET_QUA
                            ;
                
                            IF CHE_DO_KE_TOAN = '15'
                            THEN
                                CREATE TEMP TABLE TMP_KET_QUA
                                    AS
                                        SELECT
                                            "ID_CHUNG_TU"
                                            , "MODEL_CHUNG_TU"
                                            , GL."SO_CHUNG_TU"
                                            , "LOAI_CHUNG_TU"
                                            , "TEN_LOAI_CHUNG_TU"
                                            , "NGAY_CHUNG_TU"
                                            , "NGAY_HACH_TOAN"
                                            , "DIEN_GIAI_CHUNG"
                                            , "TAI_KHOAN_ID"
                                            , "MA_TAI_KHOAN"
                                            , SUM(COALESCE("GHI_NO", 0)
                                                  - COALESCE("GHI_CO", 0)) AS "SO_TIEN"
                                            , GL."DON_DAT_HANG_ID"
                                            , O."DON_DAT_HANG"
                                        FROM so_cai_chi_tiet AS GL
                                            INNER JOIN TMP_DON_HANG AS O ON GL."DON_DAT_HANG_ID" = O."DON_DAT_HANG_ID"
                                        WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                              AND (("MA_TAI_KHOAN" LIKE '621%%'
                                                    OR "MA_TAI_KHOAN" LIKE '622%%'
                
                                                    OR "MA_TAI_KHOAN" LIKE '627%%'
                                                   )
                                                   AND
                                                   (("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND "LOAI_HACH_TOAN" = '2') OR
                                                    "LOAI_HACH_TOAN" = '1')
                
                                                   OR ("MA_TAI_KHOAN" LIKE N'154%%' AND "LOAI_HACH_TOAN" = '1' AND
                                                       "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%' AND
                                                       "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%' AND
                                                       "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%'))
                
                                              AND "CHI_NHANH_ID" = chi_nhanh_id
                                        GROUP BY
                                            "ID_CHUNG_TU",
                                            "MODEL_CHUNG_TU",
                                            "SO_CHUNG_TU",
                                            "LOAI_CHUNG_TU",
                                            "TEN_LOAI_CHUNG_TU",
                                            "NGAY_CHUNG_TU",
                                            "NGAY_HACH_TOAN",
                                            "DIEN_GIAI_CHUNG",
                                            "TAI_KHOAN_ID",
                                            "MA_TAI_KHOAN",
                                            GL."DON_DAT_HANG_ID",
                                            "DON_DAT_HANG"
                                        ORDER BY O."DON_DAT_HANG", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU", "MA_TAI_KHOAN"
                                ;
                
                            ELSE
                                CREATE TEMP TABLE TMP_KET_QUA
                                    AS
                
                
                                        SELECT
                                            "ID_CHUNG_TU"
                                            , "MODEL_CHUNG_TU"
                                            , "SO_CHUNG_TU"
                                            , "LOAI_CHUNG_TU"
                                            , "TEN_LOAI_CHUNG_TU"
                                            , "NGAY_CHUNG_TU"
                                            , "NGAY_HACH_TOAN"
                                            , "DIEN_GIAI_CHUNG"
                                            , "TAI_KHOAN_ID"
                                            , "MA_TAI_KHOAN"
                                            , SUM(COALESCE("GHI_NO", 0)
                                                  - COALESCE("GHI_CO", 0)) AS "SO_TIEN"
                                            , GL."DON_DAT_HANG_ID"
                                            , O."DON_DAT_HANG"
                                            , "MA_KHOAN_MUC_CP"
                                            , "TEN_KHOAN_MUC_CP"
                                        FROM so_cai_chi_tiet AS GL
                                            INNER JOIN TMP_DON_HANG AS O ON GL."DON_DAT_HANG_ID" = O."DON_DAT_HANG_ID"
                                            LEFT JOIN danh_muc_khoan_muc_cp AS EI ON EI."id" = GL."KHOAN_MUC_CP_ID"
                                        WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                              AND "MA_TAI_KHOAN" LIKE '154%%'
                
                                              AND "CHI_NHANH_ID" = chi_nhanh_id
                                              AND EI."id" IS NOT NULL
                                              AND EI."MA_PHAN_CAP" LIKE MA_PHAN_CAPCPSX || '%%' AND
                                              EI."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPMTC || '%%'
                
                                        GROUP BY
                                            "ID_CHUNG_TU",
                                            "MODEL_CHUNG_TU",
                                            "SO_CHUNG_TU",
                                            "LOAI_CHUNG_TU",
                                            "TEN_LOAI_CHUNG_TU",
                                            "NGAY_CHUNG_TU",
                                            "NGAY_HACH_TOAN",
                                            "DIEN_GIAI_CHUNG",
                                            "TAI_KHOAN_ID",
                                            "MA_TAI_KHOAN",
                                            GL."DON_DAT_HANG_ID",
                                            O."DON_DAT_HANG",
                                            "MA_KHOAN_MUC_CP",
                                            "TEN_KHOAN_MUC_CP"
                                        ORDER BY O."DON_DAT_HANG", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU", "MA_TAI_KHOAN",
                                            "MA_KHOAN_MUC_CP"
                                ;
                
                            END IF
                            ;
                        ELSE
                
                            DROP TABLE IF EXISTS TMP_HOP_DONG
                            ;
                
                            IF LOAI_GIA_THANH = 'HOP_DONG' -- Hợp đồng
                            THEN
                
                                CREATE TEMP TABLE TMP_HOP_DONG
                                (
                                    "HOP_DONG_ID" INT,
                                    "SO_HOP_DONG" VARCHAR(50)
                                )
                                ;
                
                                INSERT INTO TMP_HOP_DONG
                                ("HOP_DONG_ID",
                                 "SO_HOP_DONG"
                                )
                                    SELECT
                                        JPD."SO_HOP_DONG_ID"
                                        , "SO_HOP_DONG"
                                    FROM gia_thanh_ky_tinh_gia_thanh_chi_tiet AS JPD
                                        INNER JOIN sale_ex_hop_dong_ban AS C ON JPD."SO_HOP_DONG_ID" = C."id"
                                    WHERE "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
                                ;
                
                
                                DROP TABLE IF EXISTS TMP_KET_QUA
                                ;
                
                                IF CHE_DO_KE_TOAN = '15'
                                THEN
                                    CREATE TEMP TABLE TMP_KET_QUA
                                        AS
                
                                            SELECT
                                                "ID_CHUNG_TU"
                                                , "MODEL_CHUNG_TU"
                                                , GL."SO_CHUNG_TU"
                                                , "LOAI_CHUNG_TU"
                                                , "TEN_LOAI_CHUNG_TU"
                                                , "NGAY_CHUNG_TU"
                                                , "NGAY_HACH_TOAN"
                                                , "DIEN_GIAI_CHUNG"
                                                , "TAI_KHOAN_ID"
                                                , "MA_TAI_KHOAN"
                                                , SUM(COALESCE("GHI_NO", 0)
                                                      - COALESCE("GHI_CO", 0)) AS "SO_TIEN"
                                                , GL."HOP_DONG_BAN_ID"
                                                , C."SO_HOP_DONG"
                                            FROM so_cai_chi_tiet AS GL
                                                INNER JOIN TMP_HOP_DONG AS C ON GL."HOP_DONG_BAN_ID" = C."HOP_DONG_ID"
                                            WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                  AND (("MA_TAI_KHOAN" LIKE '621%%'
                                                        OR "MA_TAI_KHOAN" LIKE '622%%'
                
                                                        OR "MA_TAI_KHOAN" LIKE '627%%'
                                                       )
                                                       AND (("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND "LOAI_HACH_TOAN" = '2') OR
                                                            "LOAI_HACH_TOAN" = '1') --1 là định khoản nợ/2 là định khoản có
                                                       OR ("MA_TAI_KHOAN" LIKE N'154%%' AND "LOAI_HACH_TOAN" = '1' AND
                                                           "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%' AND
                                                           "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%'
                                                           AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%'))
                                                  -- các chứng từ PS Nợ TK 154 chi tiết theo từng đối tượng THCP
                
                                                  AND "CHI_NHANH_ID" = chi_nhanh_id
                                            GROUP BY
                                                "ID_CHUNG_TU",
                                                "MODEL_CHUNG_TU",
                                                "SO_CHUNG_TU",
                                                "LOAI_CHUNG_TU",
                                                "TEN_LOAI_CHUNG_TU",
                                                "NGAY_CHUNG_TU",
                                                "NGAY_HACH_TOAN",
                                                "DIEN_GIAI_CHUNG",
                                                "TAI_KHOAN_ID",
                                                "MA_TAI_KHOAN",
                                                GL."HOP_DONG_BAN_ID",
                                                C."SO_HOP_DONG"
                                            ORDER BY C."SO_HOP_DONG", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU", "MA_TAI_KHOAN"
                                    ;
                
                                ELSE
                
                                    CREATE TEMP TABLE TMP_KET_QUA
                                        AS
                
                                            SELECT
                                                "ID_CHUNG_TU"
                                                , "MODEL_CHUNG_TU"
                                                , "SO_CHUNG_TU"
                                                , "LOAI_CHUNG_TU"
                                                , "TEN_LOAI_CHUNG_TU"
                                                , "NGAY_CHUNG_TU"
                                                , "NGAY_HACH_TOAN"
                                                , "DIEN_GIAI_CHUNG"
                                                , "TAI_KHOAN_ID"
                                                , "MA_TAI_KHOAN"
                                                , SUM(COALESCE("GHI_NO", 0)
                                                      - COALESCE("GHI_CO", 0)) AS "SO_TIEN"
                                                , GL."HOP_DONG_BAN_ID"
                                                , C."SO_HOP_DONG"
                                                , "MA_KHOAN_MUC_CP"
                                                , "TEN_KHOAN_MUC_CP"
                                            FROM so_cai_chi_tiet AS GL
                                                INNER JOIN TMP_HOP_DONG AS C ON GL."HOP_DONG_BAN_ID" = C."HOP_DONG_ID"
                                                LEFT JOIN danh_muc_khoan_muc_cp AS EI ON EI."id" = GL."KHOAN_MUC_CP_ID"
                                            WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                  AND "MA_TAI_KHOAN" LIKE '154%%'
                
                                                  AND "CHI_NHANH_ID" = chi_nhanh_id
                                                  AND EI."id" IS NOT NULL
                
                                                  AND EI."MA_PHAN_CAP" LIKE MA_PHAN_CAPCPSX || '%%' AND
                                                  EI."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPMTC || '%%'
                                            GROUP BY
                                                "ID_CHUNG_TU",
                                                "MODEL_CHUNG_TU",
                                                "SO_CHUNG_TU",
                                                "LOAI_CHUNG_TU",
                                                "TEN_LOAI_CHUNG_TU",
                                                "NGAY_CHUNG_TU",
                                                "NGAY_HACH_TOAN",
                                                "DIEN_GIAI_CHUNG",
                                                "TAI_KHOAN_ID",
                                                "MA_TAI_KHOAN",
                                                GL."HOP_DONG_BAN_ID",
                                                C."SO_HOP_DONG",
                                                "MA_KHOAN_MUC_CP",
                                                "TEN_KHOAN_MUC_CP"
                                            ORDER BY C."SO_HOP_DONG", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU", "MA_TAI_KHOAN",
                                                "MA_KHOAN_MUC_CP"
                                    ;
                
                                END IF
                                ;
                
                
                            ELSE
                                DROP TABLE IF EXISTS TMP_DOI_TUONG_THCP
                                ;
                
                                CREATE TEMP TABLE TMP_DOI_TUONG_THCP
                                (
                                    "DOI_TUONG_THCP_ID"  INT,
                                    "MA_DOI_TUONG_THCP"  VARCHAR(25),
                                    "TEN_DOI_TUONG_THCP" VARCHAR(128)
                                )
                                ;
                
                                INSERT INTO TMP_DOI_TUONG_THCP
                                ("DOI_TUONG_THCP_ID",
                                 "MA_DOI_TUONG_THCP",
                                 "TEN_DOI_TUONG_THCP"
                                )
                                    SELECT
                                        J2."id"
                                        , J2."MA_DOI_TUONG_THCP"
                                        , J2."TEN_DOI_TUONG_THCP"
                                    FROM gia_thanh_ky_tinh_gia_thanh_chi_tiet AS JPD
                                        INNER JOIN danh_muc_doi_tuong_tap_hop_chi_phi AS J ON JPD."MA_DOI_TUONG_THCP_ID" = J."id"
                                        INNER JOIN danh_muc_doi_tuong_tap_hop_chi_phi AS J2
                                            ON J2."MA_PHAN_CAP" LIKE J."MA_PHAN_CAP"
                                                                     || '%%'
                                    WHERE "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id AND J."isparent" = FALSE
                                ;
                
                
                                DROP TABLE IF EXISTS TMP_KET_QUA
                                ;
                
                                IF CHE_DO_KE_TOAN = '15'
                                THEN
                                    CREATE TEMP TABLE TMP_KET_QUA
                                        AS
                                            SELECT
                                                "ID_CHUNG_TU"
                                                , "MODEL_CHUNG_TU"
                                                , "SO_CHUNG_TU"
                                                , "LOAI_CHUNG_TU"
                                                , "TEN_LOAI_CHUNG_TU"
                                                , "NGAY_CHUNG_TU"
                                                , "NGAY_HACH_TOAN"
                                                , "DIEN_GIAI_CHUNG"
                                                , "MA_TAI_KHOAN"
                                                ,"TAI_KHOAN_ID"
                                                , SUM(COALESCE("GHI_NO", 0)
                                                      - COALESCE("GHI_CO", 0)) AS "SO_TIEN"
                                                , "MA_DOI_TUONG_THCP"
                                                , "TEN_DOI_TUONG_THCP"
                                                ,GL."DOI_TUONG_THCP_ID"
                                            FROM so_cai_chi_tiet AS GL
                                                INNER JOIN TMP_DOI_TUONG_THCP AS J ON GL."DOI_TUONG_THCP_ID" = J."DOI_TUONG_THCP_ID"
                                            WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                  AND ((("MA_TAI_KHOAN" LIKE '621%%'
                                                         OR "MA_TAI_KHOAN" LIKE '622%%'
                
                                                         OR "MA_TAI_KHOAN" LIKE '627%%'
                                                        )
                                                        AND (("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND "LOAI_HACH_TOAN" = '2') OR
                                                             "LOAI_HACH_TOAN" = '1')) --1 là định khoản nợ/2 là định khoản có
                                                       OR ("MA_TAI_KHOAN" LIKE N'154%%' AND "LOAI_HACH_TOAN" = '1' AND
                                                           "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%' AND
                                                           "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%'
                                                           AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%'))
                
                
                                                  AND "CHI_NHANH_ID" = chi_nhanh_id
                
                                            GROUP BY
                                                "ID_CHUNG_TU",
                                                "MODEL_CHUNG_TU",
                                                "SO_CHUNG_TU",
                                                "LOAI_CHUNG_TU",
                                                "TEN_LOAI_CHUNG_TU",
                                                "NGAY_CHUNG_TU",
                                                "NGAY_HACH_TOAN",
                                                "DIEN_GIAI_CHUNG",
                                                "MA_TAI_KHOAN",
                                                "MA_DOI_TUONG_THCP",
                                                "TEN_DOI_TUONG_THCP",
                                                GL."DOI_TUONG_THCP_ID",
                                                "TAI_KHOAN_ID"
                                            ORDER BY "MA_DOI_TUONG_THCP", "TEN_DOI_TUONG_THCP", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU",
                                                "SO_CHUNG_TU", "MA_TAI_KHOAN"
                                    ;
                
                                ELSE
                
                                    CREATE TEMP TABLE TMP_KET_QUA
                                        AS
                
                                            SELECT
                                                "ID_CHUNG_TU"
                                                , "MODEL_CHUNG_TU"
                                                , "SO_CHUNG_TU"
                                                , "LOAI_CHUNG_TU"
                                                , "TEN_LOAI_CHUNG_TU"
                                                , "NGAY_CHUNG_TU"
                                                , "NGAY_HACH_TOAN"
                                                , "DIEN_GIAI_CHUNG"
                                                , "MA_TAI_KHOAN"
                                                , "TAI_KHOAN_ID"
                                                , SUM(COALESCE("GHI_NO", 0)
                                                      - COALESCE("GHI_CO", 0)) AS "SO_TIEN"
                                                , "MA_DOI_TUONG_THCP"
                                                , "TEN_DOI_TUONG_THCP"
                                                , "MA_KHOAN_MUC_CP"
                                                , "TEN_KHOAN_MUC_CP"
                                                ,GL."DOI_TUONG_THCP_ID"
                                            FROM so_cai_chi_tiet AS GL
                                                INNER JOIN TMP_DOI_TUONG_THCP AS J ON GL."DOI_TUONG_THCP_ID" = J."DOI_TUONG_THCP_ID"
                                                LEFT JOIN danh_muc_khoan_muc_cp AS EI ON EI."id" = GL."KHOAN_MUC_CP_ID"
                                            WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                  AND "MA_TAI_KHOAN" LIKE '154%%'
                
                                                  AND "CHI_NHANH_ID" = chi_nhanh_id
                                                  AND EI."id" IS NOT NULL
                
                                                  AND EI."MA_PHAN_CAP" LIKE MA_PHAN_CAPCPSX || '%%' AND
                                                  EI."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPMTC || '%%'
                                            GROUP BY
                                                "ID_CHUNG_TU",
                                                "MODEL_CHUNG_TU",
                                                "SO_CHUNG_TU",
                                                "LOAI_CHUNG_TU",
                                                "TEN_LOAI_CHUNG_TU",
                                                "NGAY_CHUNG_TU",
                                                "NGAY_HACH_TOAN",
                                                "DIEN_GIAI_CHUNG",
                                                "MA_TAI_KHOAN",
                                                "MA_DOI_TUONG_THCP",
                                                "TEN_DOI_TUONG_THCP",
                                                "MA_KHOAN_MUC_CP",
                                                "TEN_KHOAN_MUC_CP",
                                                GL."DOI_TUONG_THCP_ID",
                                                "TAI_KHOAN_ID"
                                            ORDER BY "MA_DOI_TUONG_THCP", "TEN_DOI_TUONG_THCP", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU",
                                                "SO_CHUNG_TU", "MA_TAI_KHOAN", "MA_KHOAN_MUC_CP"
                                    ;
                
                
                                END IF
                                ;
                
                            END IF
                            ;
                
                        END IF
                        ;
                
                    END IF
                    ;
                
                END $$
                ;
                
                
                SELECT*
                FROM TMP_KET_QUA KQ
                
                ;
                

                
        """  
        return self.execute(query, params)