# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from datetime import datetime
from odoo.exceptions import ValidationError

class TIEN_LUONG_TRA_LUONG_FORM_THAM_SO(models.Model):
    _name = 'tien.luong.tra.luong.form.tham.so'
    _description = ''
    _auto = False

    NGAY_TRA_LUONG = fields.Date(string='Ngày trả lương', help='Ngày trả lương',default=fields.Datetime.now)
    PHUONG_THUC_THANH_TOAN = fields.Selection([('UY_NHIEM_CHI', 'Ủy nhiệm chi'), ('TIEN_MAT', 'Tiền mặt'), ], string='Phương thức thanh toán', help='Phương thức thanh toán',default='UY_NHIEM_CHI',required=True)
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    
    TIEN_LUONG_TRA_LUONG_FORM_THAM_SO_CHI_TIET_IDS = fields.One2many('tien.luong.tra.luong.form.tham.so.chi.tiet', 'CHI_TIET_ID', string='Trả lương form tham số chi tiết')

    @api.model
    def default_get(self, fields):
        rec = super(TIEN_LUONG_TRA_LUONG_FORM_THAM_SO, self).default_get(fields)
        return rec
    
    @api.onchange('NGAY_TRA_LUONG')
    def _cap_nhat_lai_thong_tin_tra_luong(self):
        chi_nhanh_id = 0
        chi_nhanh_id = self.get_chi_nhanh()
        danh_sach_thong_tin_tra_luong_sql = self.lay_du_lieu_sql_tra_ve_thong_tin_tra_luong(chi_nhanh_id,self.NGAY_TRA_LUONG)
        self.TIEN_LUONG_TRA_LUONG_FORM_THAM_SO_CHI_TIET_IDS = self.ham_gan_du_lieu_vao_cac_cot_thong_tin_tra_luong(danh_sach_thong_tin_tra_luong_sql)
    
    def ham_gan_du_lieu_vao_cac_cot_thong_tin_tra_luong(self,danh_sach_thong_tin_tra_luong_sql):
        thong_tin_tra_luong_list =[]
        for thong_tin in danh_sach_thong_tin_tra_luong_sql:
            thong_tin_tra_luong_list += [(0,0,{
                'MA_NHAN_VIEN_ID' : thong_tin.get('MA_NHAN_VIEN_ID'),
                'DON_VI_ID' : thong_tin.get('DON_VI_ID'),
                'NGAN_HANG_ID' : thong_tin.get('ID_NGAN_HANG'),
                'MA_NHAN_VIEN' : thong_tin.get('MA_NHAN_VIEN'),
                'TEN_NHAN_VIEN': thong_tin.get('TEN_NHAN_VIEN'),
                'DON_VI' :thong_tin.get('TEN_DON_VI'),
                'SO_TAI_KHOAN' :thong_tin.get('SO_TAI_KHOAN'),
                'TEN_NGAN_HANG' :thong_tin.get('TEN_NGAN_HANG'),
                'SO_CON_PHAI_TRA' :thong_tin.get('SO_TIEN_CON_PHAI_TRA'),
                'SO_TRA' :thong_tin.get('SO_TIEN_CON_PHAI_TRA'),
                'LICH_SU_TRA_LUONG' :'Xem lịch sử trả lương',
            })]
        return thong_tin_tra_luong_list


    def lay_du_lieu_sql_tra_ve_thong_tin_tra_luong(self,chi_nhanh_id,ngay_tra_luong):
        param_sql= {
        'chi_nhanh_id': chi_nhanh_id,
        'ngay_tra_luong': ngay_tra_luong,
        }
        query ="""
        DO LANGUAGE plpgsql $$
DECLARE


    chi_nhanh_id                                  INTEGER := %(chi_nhanh_id)s;



    ngay_hach_toan_tren_chung_tu                  TIMESTAMP := %(ngay_tra_luong)s;

    --@SystemDate

    CACH_LAY_SO_TIEN_LUONG_PHAI_TRA_CHO_NHAN_VIEN VARCHAR(128);

    loai_chung_tu_tam_ung                         INTEGER := 6023;

    CASalary                                      INTEGER := 1026;

    BASalary                                      INTEGER := 1523;

    chi_tiet_theo_tai_khoan_doi_tuong_334         BOOLEAN := FALSE;

    dem                                           INTEGER;


BEGIN

    IF EXISTS(SELECT *
              FROM danh_muc_he_thong_tai_khoan
              WHERE "SO_TAI_KHOAN" LIKE '334%%'
                    AND "LA_TK_TONG_HOP" = FALSE
                    AND "DOI_TUONG" = TRUE
                    AND "DOI_TUONG_SELECTION" = '2')
    THEN
        SELECT value
        INTO CACH_LAY_SO_TIEN_LUONG_PHAI_TRA_CHO_NHAN_VIEN
        FROM ir_config_parameter
        WHERE key = 'he_thong.CACH_LAY_SO_TIEN_LUONG_PHAI_TRA_CHO_NHAN_VIEN'
        FETCH FIRST 1 ROW ONLY
        ;

    ELSE
        CACH_LAY_SO_TIEN_LUONG_PHAI_TRA_CHO_NHAN_VIEN = 'LAY_THEO_SO_TIEN_LUONG_PHAI_TRA_TREN_BANG_LUONG'
        ;
    END IF
    ;


    IF CACH_LAY_SO_TIEN_LUONG_PHAI_TRA_CHO_NHAN_VIEN = 'LAY_THEO_SO_TIEN_LUONG_PHAI_TRA_TREN_BANG_LUONG'
    THEN

        DROP TABLE IF EXISTS TMP_TAI_KHOAN
        ;

        CREATE TEMP TABLE TMP_TAI_KHOAN


        (
            "TK_CONG_NO" VARCHAR(20)
        )
        ;

        INSERT INTO TMP_TAI_KHOAN
            SELECT "SO_TAI_KHOAN"
            FROM danh_muc_he_thong_tai_khoan
            WHERE "SO_TAI_KHOAN" LIKE N'334%%'
                  AND "LA_TK_TONG_HOP" = FALSE
                  AND "DOI_TUONG" = TRUE
                  AND "DOI_TUONG_SELECTION" = '2'
        ;


        SELECT COUNT("TK_CONG_NO")
        INTO dem
        FROM TMP_TAI_KHOAN
        ;

        IF dem > 0
        THEN
            chi_tiet_theo_tai_khoan_doi_tuong_334 = TRUE
            ;
        END IF
        ;

        DROP TABLE IF EXISTS TMP_KET_QUA
        ;

        CREATE TEMP TABLE TMP_KET_QUA
            AS

                SELECT

                      CAST(0 AS BOOLEAN)                       AS Selected
                    , AO."id"                                  AS "MA_NHAN_VIEN_ID"
                    , AO."MA"                                  AS "MA_NHAN_VIEN"
                    , COALESCE(AO."HO_VA_TEN", '')             AS "TEN_NHAN_VIEN"
                    , OU."id"                                  AS "DON_VI_ID"
                    , COALESCE(OU."MA_DON_VI", '')             AS "MA_DON_VI"
                    , COALESCE(OU."TEN_DON_VI", '')            AS "TEN_DON_VI"
                     , AOB."id"                                AS "ID_NGAN_HANG"
                    , COALESCE(AOB."SO_TAI_KHOAN", '')         AS "SO_TAI_KHOAN"
                    , COALESCE(AOB."TEN_NGAN_HANG", '')        AS "TEN_NGAN_HANG"
                    , SUM(COALESCE("SO_TIEN_CON_PHAI_TRA", 0)) AS "SO_TIEN_CON_PHAI_TRA"
                    , CAST(0 AS FLOAT)                         AS "SO_TIEN"
                FROM
                    (
                        SELECT
                            PSSD."MA_NHAN_VIEN"
                            , SUM(COALESCE(CASE WHEN PSS."LOAI_CHUNG_TU" = loai_chung_tu_tam_ung
                            THEN 0
                                           ELSE (
                                               CASE
                                               WHEN
                                                   PAD."MA_NHAN_VIEN"
                                                   IS
                                                   NULL
                                                   THEN
                                                       CASE WHEN
                                                           chi_tiet_theo_tai_khoan_doi_tuong_334
                                                           =
                                                           FALSE
                                                           THEN
                                                               PSSD."SO_TIEN_CON_DUOC_LINH" --+ COALESCE(PSSD."TAM_UNG_LUONG_TRONG_KY",0)
                                                       ELSE
                                                           PSSD."SO_TIEN_CON_DUOC_LINH"
                                                           +
                                                           COALESCE(
                                                               PSSD."SO_TIEN_TAM_UNG",
                                                               0)
                                                       END

                                               ELSE PSSD."SO_TIEN_CON_DUOC_LINH" /*nếu có bảng lương tạm ứng thì lấy ở dưới*/
                                               END
                                           )
                                           END, 0))
                              + SUM(COALESCE(CASE WHEN PSS."LOAI_CHUNG_TU" = loai_chung_tu_tam_ung
                            THEN PSSD."SO_TIEN_TAM_UNG"
                                             ELSE 0
                                             END, 0)) AS "SO_TIEN_CON_PHAI_TRA"
                        FROM tien_luong_bang_luong_chi_tiet AS PSSD
                            INNER JOIN tien_luong_bang_luong AS PSS ON PSS."id" = PSSD."CHI_TIET_ID"

                            LEFT JOIN (SELECT DISTINCT
                                           P."THANG"
                                           , P."NAM"
                                           , PD1."MA_NHAN_VIEN"

                                       FROM tien_luong_bang_luong_chi_tiet AS PD1
                                           INNER JOIN tien_luong_bang_luong AS P ON PD1."CHI_TIET_ID" = P."id"
                                       WHERE P."LOAI_CHUNG_TU" = 6023
                                             AND P."CHI_NHANH_ID" = chi_nhanh_id
                                      ) AS PAD ON PSSD."MA_NHAN_VIEN" = PAD."MA_NHAN_VIEN"
                                                  AND PAD."THANG" = PSS."THANG"
                                                  AND PAD."NAM" = PSS."NAM"
                        WHERE
                            ((PSS."THANG" <= EXTRACT(MONTH FROM ngay_hach_toan_tren_chung_tu)
                              AND PSS."NAM" = EXTRACT(YEAR FROM ngay_hach_toan_tren_chung_tu)
                             )
                             OR (PSS."NAM" < EXTRACT(YEAR FROM ngay_hach_toan_tren_chung_tu) )
                            )

                            AND
                            PSS."CHI_NHANH_ID" = chi_nhanh_id
                        GROUP BY PSSD."MA_NHAN_VIEN"
                                              UNION ALL

                                              SELECT
                                                  CAP1."MA_NHAN_VIEN"
                                                  , -SUM(COALESCE(CAP1."SO_TIEN", 0)) AS "SO_TIEN_CON_PHAI_TRA"
                                              FROM (SELECT
                                                        CAD."MA_NHAN_VIEN"
                                                        , SUM(COALESCE(CAD."SO_TRA", 0)) AS "SO_TIEN"
                                                    FROM tien_luong_uy_nhiem_chi_thong_tin_tra_luong_nhan_vien AS CAD
                                                        INNER JOIN account_ex_phieu_thu_chi AS CA
                                                            ON CAD."THONG_TIN_TRA_LUONG_CHI_TIET_ID" = CA."id"
                                                    WHERE ((CA."state" = 'da_ghi_so'

                                                    )
                                                          )
                                                          AND CA."LOAI_CHUNG_TU" = CASalary
                                                          AND CA."CHI_NHANH_ID" = chi_nhanh_id

                                                          AND chi_tiet_theo_tai_khoan_doi_tuong_334 = FALSE
                                                    GROUP BY CAD."MA_NHAN_VIEN"
                                                    UNION ALL
                                                    SELECT
                                                        CAD."MA_NHAN_VIEN"
                                                        , SUM(COALESCE(CAD."SO_TRA", 0)) AS "SO_TIEN"
                                                    FROM tien_luong_uy_nhiem_chi_thong_tin_tra_luong_nhan_vien AS CAD
                                                        INNER JOIN account_ex_phieu_thu_chi AS CA
                                                            ON CAD."THONG_TIN_TRA_LUONG_CHI_TIET_ID" = CA."id"
                                                    WHERE ((CA."state" = 'da_ghi_so'

                                                    )
                                                          )
                                                          AND CA."LOAI_CHUNG_TU" = BASalary
                                                          AND CA."CHI_NHANH_ID" = chi_nhanh_id

                                                          AND chi_tiet_theo_tai_khoan_doi_tuong_334 = FALSE
                                                    GROUP BY CAD."MA_NHAN_VIEN"
                                                   ) AS CAP1
                                              GROUP BY "MA_NHAN_VIEN"
                                              UNION ALL
                                              ----
                                              SELECT
                                                  GL."DOI_TUONG_ID"
                                                  , SUM(GL."GHI_CO" - GL."GHI_NO") AS "SO_TIEN_CON_PHAI_TRA"
                                              FROM so_cai_chi_tiet AS GL
                                                  INNER JOIN TMP_TAI_KHOAN AS tbl ON tbl."TK_CONG_NO" = gl."MA_TAI_KHOAN"
                                              WHERE GL."CHI_NHANH_ID" = chi_nhanh_id


                                                    AND GL."LOAI_CHUNG_TU" NOT IN ('6030')-- Hạch toán chi phí lương

                                                    AND GL."NGAY_HACH_TOAN" <= ngay_hach_toan_tren_chung_tu
                                              GROUP BY GL."DOI_TUONG_ID"


                    ) AS PA
                    INNER JOIN res_partner AS AO ON PA."MA_NHAN_VIEN" = AO."id"
                    INNER JOIN danh_muc_to_chuc AS OU ON AO."DON_VI_ID" = OU."id"

                    LEFT JOIN danh_muc_doi_tuong_chi_tiet AS AOB ON AO."id" = AOB."DOI_TUONG_ID"
                                                                    AND AOB."id" = (SELECT "id"
                                                                                    FROM danh_muc_doi_tuong_chi_tiet
                                                                                    WHERE "DOI_TUONG_ID" = AO."id"
                                                                                    ORDER BY "STT"
                                                                                    LIMIT 1
                )
                GROUP BY AO."id",
                    AO."MA",
                    COALESCE(AO."HO_VA_TEN", ''),
                    OU."id",
                    COALESCE(OU."MA_DON_VI", ''),
                    COALESCE(OU."TEN_DON_VI", ''),

                    AOB."id",
                    COALESCE(AOB."SO_TAI_KHOAN", ''),
                    COALESCE(AOB."TEN_NGAN_HANG", '')
                HAVING SUM(COALESCE("SO_TIEN_CON_PHAI_TRA", 0)) > 0
                ORDER BY
                    "MA_NHAN_VIEN",
                    "TEN_NHAN_VIEN"


        ;

    ELSE
        /*trả theo phát sinh của 334*/

        DROP TABLE IF EXISTS TMP_TAI_KHOAN
        ;

        CREATE TEMP TABLE TMP_TAI_KHOAN


        (
            "TK_CONG_NO" VARCHAR(20)
        )
        ;

        INSERT INTO TMP_TAI_KHOAN
            SELECT "SO_TAI_KHOAN"
            FROM danh_muc_he_thong_tai_khoan
            WHERE "SO_TAI_KHOAN" LIKE N'334%%'
                  AND "LA_TK_TONG_HOP" = FALSE
                  AND "DOI_TUONG" = TRUE
                  AND "DOI_TUONG_SELECTION" = '2'
        ;


        SELECT COUNT("TK_CONG_NO")
        INTO dem
        FROM TMP_TAI_KHOAN
        ;

        IF dem > 0
        THEN
            chi_tiet_theo_tai_khoan_doi_tuong_334 = TRUE
            ;
        END IF
        ;

        DROP TABLE IF EXISTS TMP_KET_QUA
        ;

        CREATE TEMP TABLE TMP_KET_QUA
            AS


                SELECT
                      CAST(0 AS BOOLEAN)                       AS Selected
                    , AO."id"                                  AS "MA_NHAN_VIEN_ID"
                    , AO."MA"                                  AS "MA_NHAN_VIEN"
                    , COALESCE(AO."HO_VA_TEN", '')             AS "TEN_NHAN_VIEN"
                    , OU."id"                                  AS "DON_VI_ID"
                    , COALESCE(OU."MA_DON_VI", '')             AS "MA_DON_VI"
                    , COALESCE(OU."TEN_DON_VI", '')            AS "TEN_DON_VI"
                    , AOB."id"                               AS "ID_NGAN_HANG"
                    , COALESCE(AOB."SO_TAI_KHOAN", '')         AS "SO_TAI_KHOAN"
                    , COALESCE(AOB."TEN_NGAN_HANG", '')        AS "TEN_NGAN_HANG"

                    , SUM(COALESCE("SO_TIEN_CON_PHAI_TRA", 0)) AS "SO_TIEN_CON_PHAI_TRA"
                    , CAST(0 AS FLOAT)                         AS "SO_TIEN"
                FROM (SELECT *
                      FROM res_partner
                      WHERE "LA_NHAN_VIEN" = TRUE

                     ) AS AO
                    INNER JOIN danh_muc_to_chuc AS OU ON AO."DON_VI_ID" = OU."id"
                    INNER JOIN (SELECT
                                    GL."DOI_TUONG_ID"
                                    , SUM(GL."GHI_CO" - GL."GHI_NO") AS "SO_TIEN_CON_PHAI_TRA"
                                FROM so_cai_chi_tiet AS GL
                                    INNER JOIN TMP_TAI_KHOAN AS tbl ON tbl."TK_CONG_NO" = gl."MA_TAI_KHOAN"
                                WHERE GL."CHI_NHANH_ID" = chi_nhanh_id


                                      AND GL."NGAY_HACH_TOAN" <= ngay_hach_toan_tren_chung_tu
                                GROUP BY GL."DOI_TUONG_ID"
                               ) AS GL ON AO."id" = GL."DOI_TUONG_ID"

                    LEFT JOIN danh_muc_doi_tuong_chi_tiet AS AOB ON AO."id" = AOB."DOI_TUONG_ID"
                                                                    AND AOB."id" = (SELECT "id"
                                                                                    FROM danh_muc_doi_tuong_chi_tiet
                                                                                    WHERE "DOI_TUONG_ID" = AO."id"
                                                                                    ORDER BY "STT"
                                                                                    LIMIT 1
                    )
                GROUP BY AO."id",
                    AO."MA",
                    COALESCE(AO."HO_VA_TEN", ''),
                    OU."id",
                    COALESCE(OU."MA_DON_VI", ''),
                    COALESCE(OU."TEN_DON_VI", ''),

                    AOB."id",
                    COALESCE(AOB."SO_TAI_KHOAN", ''),
                    COALESCE(AOB."TEN_NGAN_HANG", '')
                HAVING SUM(COALESCE("SO_TIEN_CON_PHAI_TRA", 0)) > 0
                ORDER BY
                    "MA_NHAN_VIEN",
                    "TEN_NHAN_VIEN"

        ;


    END IF


    ;

END $$
;

SELECT *
FROM TMP_KET_QUA

ORDER BY
    "MA_NHAN_VIEN",
    "TEN_NHAN_VIEN"
;

        """
        return self.execute(query,param_sql)

