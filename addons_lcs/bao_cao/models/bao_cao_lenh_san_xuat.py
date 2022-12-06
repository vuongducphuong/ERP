# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_LENH_SAN_XUAT(models.Model):
	_name = 'bao.cao.lenh.san.xuat'
	_auto = False
	

	RowNumber = fields.Integer(string='RowNumber')
	ID_CHUNG_TU = fields.Integer(string='ID_CHUNG_TU')
	MODEL_CHUNG_TU = fields.Char(string='MODEL_CHUNG_TU')
	SO_LENH = fields.Char(string='SO_LENH', help='RefNo')
	NGAY = fields.Date(string='NGAY', help='RefDate')
	
	DIEN_GIAI = fields.Char(string='DIEN_GIAI', help='Description')
	STT = fields.Integer(string='STT', help='SortOrderMaster')
	SortOrder = fields.Integer(string='SortOrder', help='SortOrder')

	ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.lenh.san.xuat.chi.tiet', 'PHIEU_THU_CHI_ID')

class BAO_CAO_LENH_SAN_XUAT_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_vproductionorder'

	@api.model
	def get_report_values(self, docids, data=None):
		############### START SQL lấy dữ liệu ###############
		refTypeList, records = self.get_reftype_list(data)
		sql_result = self.ham_lay_du_lieu_sql_tra_ve(refTypeList)

		for line in sql_result:
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
			master_data = self.env['bao.cao.lenh.san.xuat'].convert_for_update(line)
			detail_data = self.env['bao.cao.lenh.san.xuat.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
				records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.lenh.san.xuat.chi.tiet'].new(detail_data)
		
		docs = [records.get(k) for k in records]

		return {
			'docs': docs,
		}

	def ham_lay_du_lieu_sql_tra_ve(self,refTypeList):
		query = """
		DO LANGUAGE plpgsql $$
DECLARE

	ListIDchungtu  VARCHAR := N'""" + refTypeList + """';


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


    DROP TABLE IF EXISTS TMP_LENH_SAN_XUAT
    ;

    CREATE TEMP TABLE TMP_LENH_SAN_XUAT
        AS


            SELECT
                  ROW_NUMBER()
                  OVER (
                      ORDER BY
                        R."STT", 
                        "sequence",
                        PP."id" )     AS "RowNumber"
               , PO."id" AS "ID_CHUNG_TU"
                ,'stock.ex.lenh.san.xuat' AS "MODEL_CHUNG_TU"
                , PO."SO_LENH"
                , PO."NGAY"
                , I."MA"
                , PP."TEN_THANH_PHAM" AS "TEN_HANG"
                , U."DON_VI_TINH"
                , PP."SO_LUONG"
                , J."MA_DOI_TUONG_THCP"
                , J."TEN_DOI_TUONG_THCP"
                ,PO."DIEN_GIAI"
                 ,R."STT"
                ,PP.sequence AS "SortOrder"

    FROM stock_ex_lenh_san_xuat_chi_tiet_thanh_pham AS PP
    INNER JOIN stock_ex_lenh_san_xuat PO ON PP."LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID" = PO."id"
    INNER JOIN TMP_ID_CHUNG_TU R ON R."ID_CHUNG_TU" = PO."id"
    LEFT JOIN danh_muc_vat_tu_hang_hoa I ON PP."MA_HANG_ID" = I."id"
    LEFT JOIN danh_muc_don_vi_tinh U ON PP."DVT_ID" = U."id"
    LEFT JOIN danh_muc_doi_tuong_tap_hop_chi_phi AS J ON PP."DOI_TUONG_THCP_ID" = J."id"

    ORDER BY
        R."STT", 
        "sequence",
        PP."id"
    ;


END $$

;

SELECT *
FROM TMP_LENH_SAN_XUAT

ORDER BY
    "RowNumber"
;
		"""
		return self.execute(query)