# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round
from datetime import timedelta, datetime

class BAO_CAO_BAO_GIA(models.Model):
  _name = 'bao.cao.bao.gia'

  _auto = False


  RowNumber = fields.Integer(string='RowNumber')
  ID_CHUNG_TU = fields.Integer(string='ID_CHUNG_TU')
  MODEL_CHUNG_TU = fields.Char(string='MODEL_CHUNG_TU')
  SO_BAO_GIA = fields.Char(string='SO_BAO_GIA', help='RefNo')
  GHI_CHU = fields.Char(string='SO_BAO_GIA', help='JournalMemo')
  NGAY_BAO_GIA = fields.Date(string='NGAY_BAO_GIA', help='RefDate')
  HIEU_LUC_DEN = fields.Date(string='HIEU_LUC_DEN', help='EffectiveDate')
  LOAI_CHUNG_TU = fields.Integer(string='LOAI_CHUNG_TU', help='RefType')

  CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

  TEN_KHACH_HANG = fields.Char(string='TEN_KHACH_HANG', help='AccountObjectName')
  DIA_CHI = fields.Char(string='DIA_CHI', help='AccountObjectAddress')
  MA_SO_THUE = fields.Char(string='MA_SO_THUE', help='AccountObjectTaxCode')
  SO_DIEN_THOAI = fields.Char(string='SO_DIEN_THOAI', help='Tel')
  FAX = fields.Char(string='FAX', help='Fax')
  NGUOI_LIEN_HE = fields.Char(string='NGUOI_LIEN_HE', help='AccountObjectContactName')
  LOAI_TIEN = fields.Char(string='LOAI_TIEN', help='CurrencyID')
  TY_GIA = fields.Monetary(string='Tỷ giá', currency_field='currency_id') #ExchangeRate
  TONG_TIEN_HANG = fields.Float(string='TONG_TIEN_HANG', help='TotalAmountOC')
  TONG_TIEN_THANH_TOAN = fields.Float(string='TONG_TIEN_THANH_TOAN', help='TotalAmount',digits=decimal_precision.get_precision('VND'))
  TONG_TIEN_CHIET_KHAU = fields.Float(string='TONG_TIEN_CHIET_KHAU', help='TotalDiscountAmountOC')
  TONG_TIEN_CHIET_KHAU_QUY_DOI = fields.Float(string='TONG_TIEN_CHIET_KHAU_QUY_DOI', help='TotalDiscountAmount')
  TONG_TIEN_THUE_GTGT = fields.Float(string='TONG_TIEN_THUE_GTGT', help='TotalVATAmountOC')
  TONG_TIEN_THUE_GTGT_QUY_DOI = fields.Float(string='TONG_TIEN_THUE_GTGT_QUY_DOI', help='TotalVATAmount')

  SO_TIEN_CHIET_KHAU = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalDiscount
  TONG_THANH_TIEN = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalAmount
  THUE_SUAT_GTGT = fields.Float(string='Số tiền chiết khấu',digits=decimal_precision.get_precision('VND')) #dVATRate
  TIEN_THUE_GTGT = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalVAT
  CONG_TIEN_HANG = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalAmount - dTotalDiscount

  TY_LE_CHIET_KHAU = fields.Float(string='Tỷ lệ chiết khấu') #dTotalDiscount / dTotalAmount

  TONG_SO_TIEN_THANH_TOAN = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalAmount+dTotalVAT-dTotalDiscount



  currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())

  ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.bao.gia.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')

	# bao_cao_bao_gia_chi_tiet_IDS = fields.One2many('bao.cao.bao.gia.chi.tiet', '_ID', string='')
class BAO_CAO_BAO_GIA_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_saquotevoucher'

	@api.model
	def get_report_values(self, docids, data=None):
		############### START SQL lấy dữ liệu ###############
		refTypeList, records = self.get_reftype_list(data)
		sql_result = self.ham_lay_du_lieu_sql_tra_ve(refTypeList)

		for line in sql_result:
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
			master_data = self.env['bao.cao.bao.gia'].convert_for_update(line)
			detail_data = self.env['bao.cao.bao.gia.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
				records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.bao.gia.chi.tiet'].new(detail_data)
		
		docs = [records.get(k) for k in records]

		for record in docs:
			if not record.LOAI_TIEN:
				record.currency_id = self.lay_loai_tien_mac_dinh()
			else:
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', record.LOAI_TIEN)],limit=1)
				if loai_tien_id:
					record.currency_id = loai_tien_id.id

			# if record.NGAY_BAO_GIA:
			# 	record.NGAY_BAO_GIA = datetime.strptime(record.NGAY_BAO_GIA,'%Y-%m-%d').date().strftime('%d/%m/%Y')

			# if record.HIEU_LUC_DEN:
			# 	record.HIEU_LUC_DEN = datetime.strptime(record.HIEU_LUC_DEN,'%Y-%m-%d').date().strftime('%d/%m/%Y')

			tong_thanh_tien = 0
			tong_tien_chiet_khau = 0
			thue_max = 0 
			tong_tien_thue_gtgt = 0 
			for line in record.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
				line.currency_id = record.currency_id
				if not line.LA_HANG_KHUYEN_MAI:
					tong_thanh_tien += line.THANH_TIEN
					tong_tien_chiet_khau += line.TIEN_CHIET_KHAU
					tong_tien_thue_gtgt += line.TIEN_THUE_GTGT
					if thue_max < line.THUE_SUAT:
						thue_max = line.THUE_SUAT
					
			
			record.TONG_THANH_TIEN = tong_thanh_tien
			record.SO_TIEN_CHIET_KHAU = tong_tien_chiet_khau
			record.THUE_SUAT_GTGT = thue_max * 100
			record.TIEN_THUE_GTGT = tong_tien_thue_gtgt
			if record.TONG_THANH_TIEN != 0:
				record.TY_LE_CHIET_KHAU = float_round((record.SO_TIEN_CHIET_KHAU / record.TONG_THANH_TIEN) * 100 , 2)
			record.TONG_SO_TIEN_THANH_TOAN = record.TONG_THANH_TIEN + record.TIEN_THUE_GTGT - record.SO_TIEN_CHIET_KHAU
			record.CONG_TIEN_HANG = record.TONG_THANH_TIEN - record.SO_TIEN_CHIET_KHAU

			
		return {
			'docs': docs,
		}

	def ham_lay_du_lieu_sql_tra_ve(self,refTypeList):
		query = """
		DO LANGUAGE plpgsql $$
		DECLARE
		
		ListParam                        VARCHAR := N'""" + refTypeList + """';

		rec       RECORD;


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


        FROM CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(ListParam, ',', ';') F

    ;


    DROP TABLE IF EXISTS TMP_BAO_GIA
    ;

    CREATE TEMP TABLE TMP_BAO_GIA
        AS


            SELECT
                  ROW_NUMBER()
                  OVER (
                      ORDER BY
                          "THU_TU_SAP_XEP_CHI_TIET",
                          "STT" )               AS "RowNumber"
                , SQ."id"                       AS "ID_CHUNG_TU"
                , 'sale.ex.bao.gia'             AS "MODEL_CHUNG_TU"
                , SQ."SO_BAO_GIA"
                , SQ."NGAY_BAO_GIA"
                , SQ."HIEU_LUC_DEN"
                , SQ."LOAI_CHUNG_TU"
                , SQ."CHI_NHANH_ID"
                , SQ."KHACH_HANG_ID"
                , SQ."TEN_KHACH_HANG"
                , SQ."DIA_CHI"
                , SQ."MA_SO_THUE"
                , CASE WHEN A."LOAI_KHACH_HANG" = '0'
                THEN A."DIEN_THOAI"
                  ELSE A."DT_DI_DONG"
                  END                           AS "SO_DIEN_THOAI"
                , A."FAX"
                , SQ."NGUOI_LIEN_HE"

                , SQ."GHI_CHU"
                ,( SELECT "MA_LOAI_TIEN" FROM res_currency T WHERE T.id = SQ."currency_id") AS "LOAI_TIEN"
                , SQ."TY_GIA"
                , CASE WHEN "LA_HANG_KHUYEN_MAI" = TRUE
                THEN 0
                  ELSE SQ."TIEN_HANG"
                  END                           AS "TONG_TIEN_HANG"
                , SQ."THANH_TIEN_QUY_DOI" - SQ."TIEN_CHIET_KHAU_QUY_DOI"
                  + SQ."TIEN_THUE_GTGT_QUY_DOI" AS "TONG_TIEN_THANH_TOAN"
                , SQ."TIEN_CHIET_KHAU" AS "TONG_TIEN_CHIET_KHAU"
                , SQ."TIEN_CHIET_KHAU_QUY_DOI" AS "TONG_TIEN_CHIET_KHAU_QUY_DOI"
                , SQ."TIEN_THUE_GTGT" AS "TONG_TIEN_THUE_GTGT"
                , SQ."TIEN_THUE_GTGT_QUY_DOI" AS "TONG_TIEN_THUE_GTGT_QUY_DOI"
                , I."MA"                        AS "MA_HANG"
                , CASE WHEN SQD."LA_HANG_KHUYEN_MAI" = TRUE
                THEN SQD."TEN_HANG"
                     || N' (Hàng khuyến mại không thu tiền)'
                  ELSE SQD."TEN_HANG"
                  END                           AS "DIEN_GIAI_DETAIL"
                , --------------
                SQD."SO_LUONG"
                , SQD."DON_GIA"
                , SQD."THANH_TIEN"
                , SQD."THANH_TIEN_QUY_DOI"
                , SQD."TY_LE_CK" * 0.01         AS "TY_LE_CHIET_KHAU"
                , SQD."TIEN_CHIET_KHAU"
                , SQD."TIEN_CHIET_KHAU_QUY_DOI"
                , CASE WHEN ( SELECT "PHAN_TRAM_THUE_GTGT" FROM danh_muc_thue_suat_gia_tri_gia_tang T WHERE T.id = SQD."PHAN_TRAM_THUE_GTGT_ID") > 0
                THEN ( SELECT "PHAN_TRAM_THUE_GTGT" FROM danh_muc_thue_suat_gia_tri_gia_tang T WHERE T.id = SQD."PHAN_TRAM_THUE_GTGT_ID") * 0.01
                  ELSE ( SELECT "PHAN_TRAM_THUE_GTGT" FROM danh_muc_thue_suat_gia_tri_gia_tang T WHERE T.id = SQD."PHAN_TRAM_THUE_GTGT_ID")
                  END                           AS "THUE_SUAT"
                , SQD."TIEN_THUE_GTGT"
                , SQD."TIEN_THUE_GTGT_QUY_DOI"
                , U."DON_VI_TINH"

                , SQD."THU_TU_SAP_XEP_CHI_TIET"
                , F."STT"
                ,SQD."LA_HANG_KHUYEN_MAI"

            FROM sale_ex_bao_gia SQ
                INNER JOIN sale_ex_bao_gia_chi_tiet SQD ON SQ."id" = SQD."BAO_GIA_CHI_TIET_ID"
                INNER JOIN TMP_PARAM F ON F."ID_CHUNG_TU" = SQ."id"
                LEFT JOIN res_partner A ON SQ."KHACH_HANG_ID" = A."id"

                LEFT JOIN res_partner EM ON SQ."NV_MUA_HANG_ID" = EM."id"
                INNER JOIN danh_muc_vat_tu_hang_hoa I ON SQD."MA_HANG_ID" = I."id"
                LEFT JOIN danh_muc_don_vi_tinh U ON SQD."DVT_ID" = U."id"
                LEFT JOIN danh_muc_don_vi_tinh UM ON SQD."DVT_ID" = UM."id"


            ORDER BY
                "THU_TU_SAP_XEP_CHI_TIET",
                "STT"
    ;


END $$

;

SELECT *
FROM TMP_BAO_GIA

ORDER BY
    "RowNumber"
;
		"""
		return self.execute(query)