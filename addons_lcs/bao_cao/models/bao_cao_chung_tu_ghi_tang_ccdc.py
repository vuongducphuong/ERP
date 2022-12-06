# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_CHUNG_TU_GHI_TANG_CCDC(models.Model):
	_name = 'bao.cao.chung.tu.ghi.tang.ccdc'
	_auto = False

	rownum = fields.Integer(string='Rownum')
	GHI_TANG_ID = fields.Integer(string='SupplyID')
	
	TONG_SO_LUONG = fields.Float(string='GIA_TRI_CON_LAI', help='RemainAmount',digits= decimal_precision.get_precision('SO_LUONG'))
	TONG_THANH_TIEN = fields.Monetary(string='GIA_TRI_CON_LAI', help='RemainAmount',currency_field='base_currency_id')
	bang_tinh_khau_hao_ccdc_chi_tiet_IDS = fields.One2many('bao.cao.chung.tu.ghi.tang.ccdc.chi.tiet', 'NHAP_XUAT_ID')
	base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh())


class BAO_CAO_CHUNG_TU_GHI_TANG_CCDC_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_supplyincrementvouchergeneral'

	@api.model
	def get_report_values(self, docids, data=None):

		refTypeList, records = self.get_reftype_list(data)
		############### START SQL lấy dữ liệu ###############

		sql_result = self.ham_lay_du_lieu_sql_tra_ve(docids)

		for line in sql_result:
			key = 'supply.ghi.tang' + ',' + str(line.get('GHI_TANG_ID'))
			master_data = self.env['bao.cao.chung.tu.ghi.tang.ccdc'].convert_for_update(line)
			detail_data = self.env['bao.cao.chung.tu.ghi.tang.ccdc.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
				records[key].bang_tinh_khau_hao_ccdc_chi_tiet_IDS += self.env['bao.cao.chung.tu.ghi.tang.ccdc.chi.tiet'].new(detail_data)
		
		docs = [records.get(k) for k in records]

		for record in docs:
			sum_SO_LUONG = 0
			sum_THANH_TIEN = 0
			record.base_currency_id = self.lay_loai_tien_mac_dinh()
			for line in record.bang_tinh_khau_hao_ccdc_chi_tiet_IDS:
				line.base_currency_id = record.base_currency_id
				sum_SO_LUONG += line.SO_LUONG
				sum_THANH_TIEN += line.THANH_TIEN
				
			record.TONG_SO_LUONG = sum_SO_LUONG
			record.TONG_THANH_TIEN = sum_THANH_TIEN
			


		return {
			'docs': docs,
		}
	

	def ham_lay_du_lieu_sql_tra_ve(self,refTypeList):
    		
		params_sql = {
		'refTypeList':refTypeList, 
		}  

		query = """
		DO LANGUAGE plpgsql $$
DECLARE

    --ListIDchungtu                  VARCHAR := ',11;454,';

    rec                            RECORD;

    PHAN_THAP_PHAN_SO_TIEN_QUY_DOI INT;

    THANH_TIEN_TICH_LUY            FLOAT :=0;

    NEXT_GHI_TANG_ID               INT :=0;

    SL_VAT_PHAM_CUOI_CUNG          INT :=0;


BEGIN

    SELECT value
    INTO PHAN_THAP_PHAN_SO_TIEN_QUY_DOI
    FROM ir_config_parameter
    WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI'
    FETCH FIRST 1 ROW ONLY
    ;


    DROP TABLE IF EXISTS TMP_GHI_TANG
    ;

    CREATE TEMP TABLE TMP_GHI_TANG
        AS
            SELECT id
            FROM supply_ghi_tang
            WHERE id  = any (%(refTypeList)s) 
    ;

    ---Tham số ghi tăng


    DROP TABLE IF EXISTS TMP_KET_QUA

    ;

    DROP SEQUENCE IF EXISTS TMP_KET_QUA_seq
    ;

    CREATE TEMP SEQUENCE TMP_KET_QUA_seq
    ;


    CREATE TABLE TMP_KET_QUA
    (
        RowNum                 INT DEFAULT NEXTVAL('TMP_KET_QUA_seq')
            PRIMARY KEY,
        "GHI_TANG_ID"          INT,
        "GHI_TANG_CHI_TIET_ID" INT,
        "MA_CCDC"              VARCHAR(25),
        "TEN_CCDC"             VARCHAR(255),
        "MA_DON_VI"            VARCHAR(20),
        "TEN_DON_VI"           VARCHAR(128),
        "NGAY_CHUNG_TU"        TIMESTAMP,
        "SO_CHUNG_TU"          VARCHAR(20),
        "DVT"                  VARCHAR(20),
        "LY_DO_GHI_TANG"       VARCHAR(255),
        "SO_LUONG"             DECIMAL(25, 8),
        "DON_GIA"              DECIMAL(25, 8),
        "THANH_TIEN"           DECIMAL(25, 8),
        "TONG_SO_LUONG"        DECIMAL(25, 8),
        "TONG_THANH_TIEN"      DECIMAL(25, 8),
        "STT"                  INT
        ,
        "NumberDetail"         INT
    )
    ;

    INSERT INTO TMP_KET_QUA
    ("GHI_TANG_ID",
     "GHI_TANG_CHI_TIET_ID",
     "MA_CCDC",
     "TEN_CCDC",
     "MA_DON_VI",
     "TEN_DON_VI",
     "NGAY_CHUNG_TU",
     "SO_CHUNG_TU",
     "DVT",
     "LY_DO_GHI_TANG",
     "SO_LUONG",
     "DON_GIA",
     "THANH_TIEN",
     "TONG_SO_LUONG",
     "TONG_THANH_TIEN",
     "STT"
        , "NumberDetail"
    )

        SELECT
              SUI."id"                                                                                   AS "GHI_TANG_ID"
            ,
              SUIDD."id"                                                                                 AS "GHI_TANG_CHI_TIET_ID"
            , SUI."MA_CCDC"
            , SUI."TEN_CCDC"
            , OU."MA_DON_VI"
            , OU."TEN_DON_VI"
            , SUI."NGAY_GHI_TANG"
            , SUI."SO_CT_GHI_TANG"
            , SUI."DON_VI_TINH"
            , SUI."LY_DO_GHI_TANG"
            , SUIDD."SO_LUONG"
            , SUI."DON_GIA"
            , ROUND(CAST((SUI."DON_GIA" * SUIDD."SO_LUONG") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "THANH_TIEN"
            ,
              SUI."SO_LUONG"                                                                             AS "TONG_SO_LUONG"
            , ROUND(CAST((SUI."THANH_TIEN") AS NUMERIC),
                    PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)                                                      AS "TONG_THANH_TIEN"
            , SUIDD."sequence"                                                                           AS "SortOrder"
            , 1
        FROM supply_ghi_tang SUI
            INNER JOIN TMP_GHI_TANG F ON SUI."id" = F."id"
            LEFT JOIN supply_ghi_tang_don_vi_su_dung SUIDD ON SUIDD."GHI_TANG_DON_VI_SU_DUNG_ID" = SUI."id"
            LEFT JOIN danh_muc_to_chuc OU ON OU."id" = SUIDD."MA_DON_VI_ID"
        ORDER BY SUI."NGAY_GHI_TANG",
            SUI."SO_CT_GHI_TANG",
            SUI."MA_CCDC",
            SUIDD."sequence",
            SUIDD."id"
    ;

    DROP TABLE IF EXISTS TMP_CHENH_LECH_THANH_TIEN
    ;

    CREATE TEMP TABLE TMP_CHENH_LECH_THANH_TIEN

    (
        "GHI_TANG_ID"                       INT,
        "GHI_TANG_CHI_TIET_ID"              INT,
        "CHENH_LECH_THANH_TIEN"             DECIMAL(25, 8)
        ,
        "CAP_NHAT_TAT_CA"                   BOOLEAN
        ,
        "TONG_SO_LUONG_MAT_HANG_KO_BANG_KO" INT
    )
    ;

    INSERT INTO TMP_CHENH_LECH_THANH_TIEN
        SELECT
            T."GHI_TANG_ID"
            , D."GHI_TANG_CHI_TIET_ID"
            , T."TONG_THANH_TIEN" - T."SUM_THANH_TIEN"
            , CASE WHEN (T."SUM_THANH_TIEN" - T."TONG_THANH_TIEN") > D."THANH_TIEN"
            THEN TRUE
              ELSE FALSE END
            , I."TONG_SO_LUONG_MAT_HANG_KO_BANG_KO"
        FROM
            (
                SELECT
                    KQ."GHI_TANG_ID"
                    , SUM(KQ."THANH_TIEN") AS "SUM_THANH_TIEN"
                    , "TONG_THANH_TIEN"
                FROM TMP_KET_QUA KQ
                GROUP BY
                    "GHI_TANG_ID",
                    "TONG_THANH_TIEN"
                HAVING SUM(KQ."THANH_TIEN") <> "TONG_THANH_TIEN"
            ) T
            INNER JOIN LATERAL
                       (SELECT
                            "GHI_TANG_CHI_TIET_ID"
                            , "THANH_TIEN"
                        FROM TMP_KET_QUA KQ
                        WHERE KQ."GHI_TANG_ID" = T."GHI_TANG_ID"
                              AND "SO_LUONG" <> 0
                        ORDER BY "STT" DESC
                        FETCH FIRST 1 ROW ONLY

                       )
                       D ON TRUE
            INNER JOIN LATERAL
                       (
                       SELECT COUNT(*) AS "TONG_SO_LUONG_MAT_HANG_KO_BANG_KO"
                       FROM TMP_KET_QUA KQ
                       WHERE KQ."GHI_TANG_ID" = T."GHI_TANG_ID"
                             AND KQ."SO_LUONG" <> 0
                       FETCH FIRST 1 ROW ONLY
                       ) I ON TRUE
    ;


    -- Cập nhật dòng thành tiền bị lệch vào bảng TMP_KET_QUA: Cập nhật vào dòng cuối
    UPDATE TMP_KET_QUA R
    SET "THANH_TIEN" = "THANH_TIEN" + "CHENH_LECH_THANH_TIEN"
    FROM
        TMP_CHENH_LECH_THANH_TIEN D
    WHERE R."GHI_TANG_CHI_TIET_ID" = D."GHI_TANG_CHI_TIET_ID"
          AND D."CAP_NHAT_TAT_CA" = FALSE
    ;


    IF EXISTS(SELECT *
              FROM TMP_CHENH_LECH_THANH_TIEN
              WHERE "CAP_NHAT_TAT_CA" = TRUE )
    THEN


        FOR rec IN
        SELECT *
        FROM TMP_KET_QUA R
            INNER JOIN TMP_CHENH_LECH_THANH_TIEN D ON R."GHI_TANG_ID" = D."GHI_TANG_ID"
        WHERE D."CAP_NHAT_TAT_CA" = TRUE AND R."SO_LUONG" <> 0
        ORDER BY
            RowNum
        LOOP
            THANH_TIEN_TICH_LUY = 0
        ;

            NEXT_GHI_TANG_ID = 0
        ;

            SL_VAT_PHAM_CUOI_CUNG = 0
        ;


            SELECT (CASE WHEN rec."GHI_TANG_ID" <> NEXT_GHI_TANG_ID
                THEN 0
                    ELSE THANH_TIEN_TICH_LUY END)
            INTO THANH_TIEN_TICH_LUY
        ;

            SELECT (CASE WHEN rec."GHI_TANG_ID" <> NEXT_GHI_TANG_ID
                THEN 0
                    ELSE SL_VAT_PHAM_CUOI_CUNG END)
            INTO SL_VAT_PHAM_CUOI_CUNG
        ;


            NEXT_GHI_TANG_ID = rec."GHI_TANG_ID"
        ;

            THANH_TIEN_TICH_LUY = THANH_TIEN_TICH_LUY + rec."THANH_TIEN"
        ;

            SL_VAT_PHAM_CUOI_CUNG = SL_VAT_PHAM_CUOI_CUNG + 1
        ;

            rec."THANH_TIEN" = CASE WHEN THANH_TIEN_TICH_LUY <= rec."TONG_THANH_TIEN"
                THEN
                    CASE WHEN SL_VAT_PHAM_CUOI_CUNG = rec."TONG_SO_LUONG_MAT_HANG_KO_BANG_KO"
                        THEN
                            rec."THANH_TIEN" + (rec."TONG_THANH_TIEN" - THANH_TIEN_TICH_LUY)
                    ELSE
                        rec."THANH_TIEN"
                    END
                               ELSE
                                   CASE WHEN THANH_TIEN_TICH_LUY - rec."THANH_TIEN" < rec."TONG_THANH_TIEN"
                                       THEN
                                           rec."TONG_THANH_TIEN" - THANH_TIEN_TICH_LUY + rec."THANH_TIEN"
                                   ELSE 0
                                   END
                               END
        ;

            UPDATE TMP_KET_QUA
            SET "THANH_TIEN" = rec."THANH_TIEN"
            WHERE RowNum = rec.RowNum


        ;

        END LOOP
        ;

    END IF
    ;


    UPDATE TMP_KET_QUA R
    SET "NumberDetail" = T."CountNumberDetail"
    FROM
        (SELECT
             COUNT("GHI_TANG_ID") AS "CountNumberDetail"
             , "GHI_TANG_ID"
         FROM TMP_KET_QUA
         GROUP BY
             "GHI_TANG_ID"
         HAVING COUNT("GHI_TANG_ID") > 1) T WHERE R."GHI_TANG_ID" = T."GHI_TANG_ID"
    ;




END $$

;

SELECT *
FROM TMP_KET_QUA
ORDER BY Rownum

;
		"""
		return self.execute(query,params_sql)


	