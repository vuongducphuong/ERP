# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_LENH_THAO_DO(models.Model):
	_name = 'bao.cao.lenh.thao.do'
	_auto = False
		
	RowNumber = fields.Integer(string='RowNumber')
	ID_CHUNG_TU = fields.Integer(string='ID_CHUNG_TU')
	MODEL_CHUNG_TU = fields.Char(string='MODEL_CHUNG_TU')
	SO = fields.Char(string='SO', help='RefNo')
	NGAY = fields.Date(string='NGAY', help='RefDate')
	MA_HANG = fields.Char(string='MA_HANG', help='InventoryItemCode')
	TEN_HANG = fields.Char(string='TEN_HANG', help='InventoryItemName')
	DON_VI_TINH = fields.Char(string='DON_VI_TINH', help='UnitName')
	SO_LUONG = fields.Float(string='SO_LUONG', help='Quantity',digits=decimal_precision.get_precision('SO_LUONG'))
	DIEN_GIAI = fields.Char(string='DIEN_GIAI', help='JournalMemo')
	
	STT = fields.Integer(string='STT', help='SortOrderMaster')
	SortOrder = fields.Integer(string='SortOrder', help='SortOrder')

	ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.lenh.thao.do.chi.tiet', 'PHIEU_THU_CHI_ID')

class BAO_CAO_LENH_THAO_DO_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_vdismantler'

	@api.model
	def get_report_values(self, docids, data=None):
		############### START SQL lấy dữ liệu ###############
		refTypeList, records = self.get_reftype_list(data)
		sql_result = self.ham_lay_du_lieu_sql_tra_ve(refTypeList)

		for line in sql_result:
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
			master_data = self.env['bao.cao.lenh.thao.do'].convert_for_update(line)
			detail_data = self.env['bao.cao.lenh.thao.do.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
				records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.lenh.thao.do.chi.tiet'].new(detail_data)
		
		docs = [records.get(k) for k in records]

		return {
			'docs': docs,
		}

	def ham_lay_du_lieu_sql_tra_ve(self,refTypeList):
		query = """
		DO LANGUAGE plpgsql $$
DECLARE

    ListIDchungtu VARCHAR := N'""" + refTypeList + """';


    rec           RECORD;


BEGIN

    DROP TABLE IF EXISTS TMP_ID_CHUNG_TU
    ;

    DROP SEQUENCE IF EXISTS TMP_ID_CHUNG_TU_seq
    ;

    CREATE TEMP SEQUENCE TMP_ID_CHUNG_TU_seq
    ;

    CREATE TEMP TABLE TMP_ID_CHUNG_TU
    (
        "ID_CHUNG_TU"   INT,
        "LOAI_CHUNG_TU" INT,


        "STT"           INT DEFAULT NEXTVAL('TMP_ID_CHUNG_TU_seq')
            PRIMARY KEY

    )
    ;

    INSERT INTO TMP_ID_CHUNG_TU
        SELECT

            Value1
            , Value2


        FROM CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(ListIDchungtu, ',', ';') F

    ;


    DROP TABLE IF EXISTS TMP_LAP_RAP_THAO_DO
    ;

    CREATE TEMP TABLE TMP_LAP_RAP_THAO_DO
        AS


            SELECT
                  ROW_NUMBER()
                  OVER (
                       ORDER BY
                            R."STT"
                            , IAD."sequence"
                            , IAD."id" )  AS "RowNumber"
               , IA."id" AS "ID_CHUNG_TU"
                ,'stock.ex.lap.rap.thao.do' AS "MODEL_CHUNG_TU"
                , IA."SO"
                , IA."NGAY"
                , II."MA" AS "MA_HANG"
                , II."TEN" AS "TEN_HANG"

                , U."DON_VI_TINH"
                , IA."SO_LUONG"
                , IA."DIEN_GIAI"
                , I."MA"           AS "MA_HANG_DETAIL"
                , IAD."TEN_HANG"   AS "TEN_HANG_DETAL"
                , UI."DON_VI_TINH" AS "DVT_DETAIL"
                , IAD."SO_LUONG"   AS "SO_LUONG_DEATAIL"
                , R."STT"
                , IAD."sequence" AS "SortOrder"
            FROM stock_ex_lap_rap_thao_do AS IA
                INNER JOIN TMP_ID_CHUNG_TU R ON R."ID_CHUNG_TU" = IA."id"
    INNER JOIN danh_muc_vat_tu_hang_hoa AS II ON IA."HANG_HOA_ID" = II."id"
    LEFT JOIN danh_muc_don_vi_tinh AS U ON IA."DVT_ID" = U."id"
    INNER JOIN stock_ex_lap_rap_thao_do_chi_tiet AS IAD ON IA."id" = IAD."LAP_RAP_THAO_DO_CHI_TIET_ID"
    LEFT JOIN danh_muc_vat_tu_hang_hoa AS I ON IAD."MA_HANG_ID" = I."id"
    LEFT JOIN danh_muc_don_vi_tinh AS UI ON IAD."DVT_ID" = UI."id"

    ORDER BY
        R."STT"
        , IAD."sequence"
        , IAD."id"
    ;


END $$

;

SELECT *
FROM TMP_LAP_RAP_THAO_DO

ORDER BY
    "RowNumber"
;
		"""
		return self.execute(query)