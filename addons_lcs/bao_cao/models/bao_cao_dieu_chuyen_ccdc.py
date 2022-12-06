# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round
from datetime import timedelta, datetime

class BAO_CAO_DIEU_CHUYEN_CCDC(models.Model):
	_name = 'bao.cao.dieu.chuyen.ccdc'
	_auto = False
 
	RowNumber = fields.Integer(string='RowNumber')
	ID_CHUNG_TU = fields.Integer(string='ID_CHUNG_TU')
	MODEL_CHUNG_TU = fields.Char(string='MODEL_CHUNG_TU')
	LOAI_CHUNG_TU = fields.Integer(string='LOAI_CHUNG_TU', help='RefType')
	NGAY = fields.Date(string='NGAY', help='RefDate')
	BIEN_BAN_GIAO_NHAN_SO = fields.Char(string='BIEN_BAN_GIAO_NHAN_SO', help='RefNo')
	NGUOI_TIEP_NHAN = fields.Char(string='NGUOI_TIEP_NHAN', help='ReceiptName')
	NGUOI_BAN_GIAO = fields.Char(string='NGUOI_BAN_GIAO', help='DeliveryName')
	LY_DO_DIEU_CHUYEN = fields.Char(string='LY_DO_DIEU_CHUYEN', help='JournalMemo')
	STT = fields.Integer(string='STT', help='SortOrderMaster')

	BAO_CAO_DIEU_CHUYEN_CCDC_CHI_TIET_IDS = fields.One2many('bao.cao.dieu.chuyen.ccdc.chi.tiet', 'PHIEU_THU_CHI_ID')

class BAO_CAO_DIEU_CHUYEN_CCDC_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_vsutransfer'

	@api.model
	def get_report_values(self, docids, data=None):
		############### START SQL lấy dữ liệu ###############
		refTypeList, records = self.get_reftype_list(data)
		
		sql_result = self.ham_lay_du_lieu_sql_tra_ve(refTypeList)

		for line in sql_result:
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
			master_data = self.env['bao.cao.dieu.chuyen.ccdc'].convert_for_update(line)
			detail_data = self.env['bao.cao.dieu.chuyen.ccdc.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
				records[key].BAO_CAO_DIEU_CHUYEN_CCDC_CHI_TIET_IDS += self.env['bao.cao.dieu.chuyen.ccdc.chi.tiet'].new(detail_data)
		
		docs = [records.get(k) for k in records]

		return {
			'docs': docs,
		}
	
	def ham_lay_du_lieu_sql_tra_ve(self,refTypeList):
		query = """
		DO LANGUAGE plpgsql $$
		DECLARE
		
		ListIDchungtu                         VARCHAR := N'""" + refTypeList + """';

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


    DROP TABLE IF EXISTS TMP_DIEU_CHUYEN_CCDC
    ;

    CREATE TEMP TABLE TMP_DIEU_CHUYEN_CCDC
        AS


            SELECT
                  ROW_NUMBER()
                  OVER (
                      ORDER BY
                          "STT"
                          , SUTD."THU_TU_SAP_XEP") AS "RowNumber"
                , SUT."id" AS "ID_CHUNG_TU"
                ,'supply.dieu.chuyen.cong.cu.dung.cu' AS "MODEL_CHUNG_TU"
                , SUT."LOAI_CHUNG_TU"
                , SUT."NGAY"
                , SUT."BIEN_BAN_GIAO_NHAN_SO"
                , SUT."NGUOI_TIEP_NHAN"
                , SUT."NGUOI_BAN_GIAO"
                , SU."MA_CCDC"
                , SU."TEN_CCDC"
                , SUT."LY_DO_DIEU_CHUYEN"
                , FD."TEN_DON_VI"                 AS "TU_DON_VI"
                , TD."TEN_DON_VI"                 AS "DEN_DON_VI"
                , SUTD."SO_LUONG_DANG_DUNG"
                , SUTD."SO_LUONG_DIEU_CHUYEN"
                , RID."STT"
                , SUTD."THU_TU_SAP_XEP"
            FROM supply_dieu_chuyen_cong_cu_dung_cu SUT
                INNER JOIN TMP_ID_CHUNG_TU AS RID ON RID."ID_CHUNG_TU" = SUT."id"
                INNER JOIN supply_dieu_chuyen_chi_tiet SUTD ON SUT."id" = SUTD."DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID"
                INNER JOIN supply_ghi_tang SU ON SUTD."MA_CCDC_ID" = SU."id"
                LEFT JOIN danh_muc_to_chuc FD ON FD."id" = SUTD."TU_DON_VI_ID"
                LEFT JOIN danh_muc_to_chuc TD ON TD."id" = SUTD."DEN_DON_VI_ID"

            ORDER BY
                "STT"
                , SUTD."THU_TU_SAP_XEP"
    ;


END $$

;

SELECT *
FROM TMP_DIEU_CHUYEN_CCDC

ORDER BY
    "RowNumber"
;
		"""
		return self.execute(query)