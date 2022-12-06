# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from datetime import timedelta, datetime

class BAO_CAO_CHUNG_TU_GHI_GIAM_CCDC(models.Model):
	_name = 'bao.cao.chung.tu.ghi.giam.ccdc'
	_auto = False

	ref = fields.Char(string='Reffence ID')
	ID_CHUNG_TU = fields.Integer(string='ID_CHUNG_TU')
	MODEL_CHUNG_TU = fields.Char(string='MODEL_CHUNG_TU')

	NGAY_CHUNG_TU = fields.Char(string='NGAY_CHUNG_TU') #RefDate
	SO_CHUNG_TU = fields.Char(string='SO_CHUNG_TU') #RefNo

	DIEN_GIAI = fields.Char(string='DIEN_GIAI') #JournalMemo
	
	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
	CT_GHI_GIAM_CCDC_CHI_TIETS = fields.One2many('bao.cao.chung.tu.ghi.giam.ccdc.chi.tiet', 'PHIEU_THU_CHI_ID')
	
	TONG_SL_GHI_GIAM =  fields.Float(digits=decimal_precision.get_precision('SO_LUONG'))
	TONG_GIA_TRI_CCDC =  fields.Float(digits=decimal_precision.get_precision('VND'))
	TONG_GIA_TRI_CON_LAI=  fields.Float(digits=decimal_precision.get_precision('VND'))

class BAO_CAO_CHUNG_TU_GHI_GIAM_CCDC_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_vsudecrement'

	@api.model
	def get_report_values(self, docids, data=None):
		refTypeList, records = self.get_reftype_list(data)
		############### START SQL lấy dữ liệu ###############

		sql_result = self.ham_lay_du_lieu_sql_tra_ve(refTypeList)

		for line in sql_result:
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
			master_data = self.env['bao.cao.chung.tu.ghi.giam.ccdc'].convert_for_update(line)
			detail_data = self.env['bao.cao.chung.tu.ghi.giam.ccdc.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
				records[key].CT_GHI_GIAM_CCDC_CHI_TIETS += self.env['bao.cao.chung.tu.ghi.giam.ccdc.chi.tiet'].new(detail_data)
		
		docs = [records.get(k) for k in records]

		for records in docs:
			tong_sl_ghi_giam = 0
			tong_gia_tri_ccdc = 0
			tong_gia_tri_con_lai = 0
			for line in records.CT_GHI_GIAM_CCDC_CHI_TIETS:
				tong_sl_ghi_giam += line.SO_LUONG_GHI_GIAM
				tong_gia_tri_ccdc += line.GIA_TRI_CCDC
				tong_gia_tri_con_lai += line.GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM
			
			records.NGAY_CHUNG_TU = datetime.strptime(records.NGAY_CHUNG_TU,'%Y-%m-%d').date().strftime('%d/%m/%Y')
			records.TONG_SL_GHI_GIAM = tong_sl_ghi_giam
			records.TONG_GIA_TRI_CCDC = tong_gia_tri_ccdc
			records.TONG_GIA_TRI_CON_LAI = tong_gia_tri_con_lai
			
		return {
			'docs': docs,
		}

	def ham_lay_du_lieu_sql_tra_ve(self,refTypeList):
		query = """
				DO LANGUAGE plpgsql $$
				DECLARE

				ListIDchungtu   VARCHAR := N'""" + refTypeList + """';


				rec            RECORD;


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


				DROP TABLE IF EXISTS TMP_GHI_GIAM_CCDC
				;

				CREATE TEMP TABLE TMP_GHI_GIAM_CCDC
				AS


				SELECT
				ROW_NUMBER()
				OVER (
				ORDER BY
				"STT",
				SUD."sequence",
				 SUD."id" ) AS "RowNumber"
				, SUA."id"                 AS "ID_CHUNG_TU"
				, 'supply.ghi.giam'        AS "MODEL_CHUNG_TU"
				, SUA."LOAI_CHUNG_TU"
				, SUA."NGAY_CHUNG_TU"
				, SUA."SO_CHUNG_TU"
				,CASE WHEN  SUA."LY_DO_GHI_GIAM" ='NHUONG_BAN_THANH_LY'
				THEN 'Nhượng bán, thanh lý'
				WHEN  SUA."LY_DO_GHI_GIAM" ='PHAT_HIEN_THIEU_KHI_KIEM_KE'
				THEN 'Phát hiện thiếu khi kiểm kê'
				ELSE
				'Khác'
				END AS "DIEN_GIAI"


				, SU."MA_CCDC"
				, SU."TEN_CCDC"
				, o."TEN_DON_VI"
				, SUD."SO_LUONG_GHI_GIAM"
				, CASE WHEN SU."SO_LUONG" <> 0
				THEN SUD."SO_LUONG_GHI_GIAM" * (COALESCE(SL."SO_TIEN_GHI_TANG", 0)
					- COALESCE(SL."SO_TIEN_GHI_GIAM_KO_BAO_GOM_GHI_GIAM_CHO_GIA_TRI_CCDC",
								0)) / SU."SO_LUONG"
				ELSE 0
				END                      AS "GIA_TRI_CCDC"
				, SUD."GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM"
				, RID."STT"
				, SUD."sequence" AS "SortOrder"
				
				FROM supply_ghi_giam SUA
				INNER JOIN TMP_ID_CHUNG_TU AS RID ON RID."ID_CHUNG_TU" = SUA."id"
				INNER JOIN supply_ghi_giam_chi_tiet SUD ON SUA."id" = SUD."CCDC_GHI_GIAM_ID"
				INNER JOIN supply_ghi_tang SU ON SUD."MA_CCDC_ID" = SU."id"
				INNER JOIN danh_muc_to_chuc O ON SUD."DON_VI_SU_DUNG_ID" = o."id"
				LEFT JOIN (SELECT
				so_ccdc_chi_tiet."CCDC_ID"
				, SUM(CASE WHEN so_ccdc_chi_tiet."LOAI_CHUNG_TU" = '451'
				THEN 0
				ELSE "SO_LUONG_GHI_TANG"
				END
				) AS "SO_LUONG_GHI_TANG"
				, SUM(CASE WHEN so_ccdc_chi_tiet."LOAI_CHUNG_TU" = '451'
				THEN 0
				ELSE "SO_LUONG_GHI_GIAM"
				END
				) AS "SL_GIAM_TRONG_KY"
				, (SUM(CASE WHEN so_ccdc_chi_tiet."LOAI_CHUNG_TU" = '451'
				THEN 0
				ELSE "SO_LUONG_GHI_TANG"
				END
				)
				- SUM(CASE WHEN so_ccdc_chi_tiet."LOAI_CHUNG_TU" = '451'
				THEN 0
				ELSE "SO_LUONG_GHI_GIAM"
				END
				)
				) AS "SO_LUONG_CON_LAI"
				, SUM("SO_TIEN_PHAN_BO"
				) AS "SO_DA_PHAN_BO"
				, SUM("SO_TIEN_GHI_TANG"
				) AS "SO_TIEN_GHI_TANG"
				, SUM("SO_TIEN_GHI_GIAM"
				) AS "SO_TIEN_GHI_GIAM"
				, /*giá trị ghi giảm không bao gồm chứng từ ghi giảm lấy cho giá trị ccdc*/
				SUM(CASE WHEN so_ccdc_chi_tiet."LOAI_CHUNG_TU" = '452'
				THEN 0
				ELSE "SO_TIEN_GHI_GIAM"
				END
				) AS "SO_TIEN_GHI_GIAM_KO_BAO_GOM_GHI_GIAM_CHO_GIA_TRI_CCDC"
				, SUM("SO_KY_PHAN_BO_GHI_TANG"
				) AS "SO_KY_PHAN_BO_GHI_TANG"
				, SUM("SO_KY_PHAN_BO_GHI_GIAM"
				) AS "SO_KY_PHAN_BO_GHI_GIAM"
				FROM so_ccdc_chi_tiet

				GROUP BY
				so_ccdc_chi_tiet."CCDC_ID"
				) AS SL ON sl."CCDC_ID" = SUD."MA_CCDC_ID"
				ORDER BY
				"STT",
				SUD."sequence",
				 SUD."id"
				;


				END $$

				;

				SELECT *
				FROM TMP_GHI_GIAM_CCDC

				ORDER BY
				"RowNumber"
				;
				"""
		return self.execute(query)

	

	

