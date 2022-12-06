# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round
from datetime import timedelta, datetime

class BAO_CAO_HOP_DONG_BAN_BEN_A_MUA(models.Model):
	_name = 'bao.cao.hop.dong.ban.ben.a.mua'
	_auto = False

	ref = fields.Char(string='Reffence ID')

	ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
	MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')
	LOAI_CHUNG_TU = fields.Integer(string='Địa chỉ') #RefType
	NGAY_KY = fields.Date(string='Địa chỉ') #SignDate
	NGAY_KY_BANG_CHU = fields.Char(string='Địa chỉ') #SignDateInWord
	SO_HOP_DONG = fields.Char(string='Địa chỉ') #ContractCode
	TEN_KHACH_HANG = fields.Char(string='Tên khách hàng') #CustomerName
	MA_KHACH_HANG = fields.Char(string='Tên ngân hàng')#CustomerCode
	THUOC_DU_AN = fields.Char(string='Tên ngân hàng')#ProjectCode
	TRICH_YEU = fields.Char(string='Tên ngân hàng')#ContractSubject
	LOAI_TIEN = fields.Char(string='Loại tiền') #CurrencyID
	TY_GIA = fields.Monetary(string='Tỷ giá', currency_field='currency_id') #ExchangeRate
	HAN_THANH_TOAN = fields.Date(string='Địa chỉ') #PaymentDate
	DON_VI_SU_DUNG = fields.Char(string='Loại tiền') #DepartmentName
	TEN_NHAN_VIEN_BAN_HANG = fields.Char(string='Địa chỉ') #EmployeeName
	MA_SO_THUE = fields.Char(string='Địa chỉ') #AccountObjectTaxCode
	DIEN_THOAI_KHACH_HANG = fields.Char(string='Địa chỉ') #AccountObjectTel
	EMAIL_KHACH_HANG = fields.Char(string='Địa chỉ') #AccountObjectEmail
	WEBSITE_KHACH_HANG = fields.Char(string='Địa chỉ') #AccountObjectWebsite
	FAX_KHACH_HANG = fields.Char(string='Địa chỉ') #AccountObjectFax
	DIA_CHI_KHACH_HANG = fields.Char(string='Địa chỉ') #AccountObjectAddress
	NGUOI_DAI_DIEN = fields.Char(string='Địa chỉ') #AccountObjectContactName
	CHUC_VU = fields.Char(string='Địa chỉ') #AccountObjectContactTitle
	DIA_DIEM_GIAO_HANG_STRING = fields.Char(string='Địa chỉ') #ShippingAddress
	HAN_GIAO_HANG = fields.Date(string='Địa chỉ') #DeliveryDate
	STK_NGANG_HANG_DOI_TUONG = fields.Char(string='Địa chỉ') #AccountObjectBankAccount
	TEN_NGANG_HANG_DOI_TUONG = fields.Char(string='Địa chỉ') #AccountObjectBankName
	MAX_PHAN_TRAM_THUE = fields.Float(string='Địa chỉ') #MAXVATRate
	TONG_TIEN_BAN = fields.Float(string='Địa chỉ') #TotalSaleAmountOC
	TONG_TIEN_BAN_QUY_DOI = fields.Float(string='Địa chỉ') #TotalSaleAmount
	TONG_TIEN_CHIET_KHAU = fields.Float(string='Địa chỉ') #TotalDiscountAmountOC
	TONG_TIEN_CHIET_KHAU_QUY_DOI = fields.Float(string='Địa chỉ') #TotalDiscountAmount
	TONG_TIEN_THUE = fields.Float(string='Địa chỉ') #TotalVATAmountOC
	TONG_TIEN_THUE_QUY_DOI = fields.Float(string='Địa chỉ',digits=decimal_precision.get_precision('VND')) #TotalVATAmount
	TONG_TIEN = fields.Float(string='Địa chỉ') #TotalAmountOC
	TONG_TIEN_QUY_DOI = fields.Float(string='Địa chỉ') #TotalAmount
	OffsetsAmountDiscount = fields.Float(string='Địa chỉ',digits=decimal_precision.get_precision('VND')) #OffsetsAmountDiscount
	AVGDiscountRate = fields.Float(string='Địa chỉ') #AVGDiscountRate

	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
	base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh())

	ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.hop.dong.ban.ben.a.mua.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')

	TONG_CONG_TIEN_THANH_TOAN = fields.Monetary(string='Địa chỉ', currency_field='currency_id') 
	TONG_THANH_TIEN = fields.Float(string='Tổng thành tiền', digits=decimal_precision.get_precision('VND')) 

class BAO_CAO_HOP_DONG_BAN_BEN_A_MUA_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_hopdongban9041amua'

	@api.model
	def get_report_values(self, docids, data=None):
		############### START SQL lấy dữ liệu ###############
		refTypeList, records = self.get_reftype_list(data)
		sql_result_master = self.ham_lay_du_lieu_sql_tra_ve_master(refTypeList)
		sql_result_detail = self.ham_lay_du_lieu_sql_tra_ve_detail(refTypeList)

		for line in sql_result_master:
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
			master_data = self.env['bao.cao.hop.dong.ban.ben.a.mua'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
		
		# 2. Update detail
		for line in sql_result_detail:
			key = 'sale.ex.hop.dong.ban' + ',' + str(line.get('ID_CHUNG_TU'))
			detail_data1 = self.env['bao.cao.hop.dong.ban.ben.a.mua.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.hop.dong.ban.ben.a.mua.chi.tiet'].new(detail_data1)
		
		docs = [records.get(k) for k in records]
		
		for records in docs:
    			
			records.base_currency_id = self.lay_loai_tien_mac_dinh()

			if not records.LOAI_TIEN:
				records.currency_id = self.lay_loai_tien_mac_dinh()
			else:
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', records.LOAI_TIEN)],limit=1)
				if loai_tien_id:
					records.currency_id = loai_tien_id.id
			
			tong_tien = 0 
			for line in records.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS : 
				tong_tien += line.THANH_TIEN_QUY_DOI
			
			records.TONG_THANH_TIEN = tong_tien
			records.TONG_CONG_TIEN_THANH_TOAN = records.TONG_TIEN_CHIET_KHAU_QUY_DOI + records.OffsetsAmountDiscount + records.TONG_TIEN_THUE_QUY_DOI

		return {
			'docs': docs,
		}

	def ham_lay_du_lieu_sql_tra_ve_master(self,refTypeList):
		query = """
		DO LANGUAGE plpgsql $$
		DECLARE

		ListParam                        VARCHAR := N'""" + refTypeList + """';

		rec                                          RECORD;


		CACH_LAY_SL_DA_GIAO_CUA_VTHH_TREN_DON_DH_HDB BOOLEAN;

		PHAN_THAP_PHAN_CUA_HE_SO_TY_LE               INT;


		BEGIN


		SELECT value
		INTO CACH_LAY_SL_DA_GIAO_CUA_VTHH_TREN_DON_DH_HDB
		FROM ir_config_parameter
		WHERE key = 'he_thong.CACH_LAY_SL_DA_GIAO_CUA_VTHH_TREN_DON_DH_HDB'
		FETCH FIRST 1 ROW ONLY
		;

		SELECT value
		INTO PHAN_THAP_PHAN_CUA_HE_SO_TY_LE
		FROM ir_config_parameter
		WHERE key = 'he_thong.PHAN_THAP_PHAN_CUA_HE_SO_TY_LE'
		FETCH FIRST 1 ROW ONLY
		;


		DROP TABLE IF EXISTS TMP_PARAM
		;

		DROP SEQUENCE IF EXISTS TMP_ID_CHUNG_TU_seq
		;

		CREATE TEMP SEQUENCE TMP_ID_CHUNG_TU_seq
		;

		CREATE TEMP TABLE TMP_PARAM
		(
		"ID_CHUNG_TU"        INT,
		"LOAI_CHUNG_TU"      INT,
		"MAX_PHAN_TRAM_THUE" FLOAT,

		"STT"                INT DEFAULT NEXTVAL('TMP_ID_CHUNG_TU_seq')
		PRIMARY KEY

		)
		;

		INSERT INTO TMP_PARAM
		SELECT

		Value1
		, Value2
		, NULL


		FROM CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(ListParam, ',', ';') F
		INNER JOIN danh_muc_reftype R ON F.Value2 = R."REFTYPE"
		;

		UPDATE TMP_PARAM P1
		SET "MAX_PHAN_TRAM_THUE" = R."MAX_PHAN_TRAM_THUE"
		FROM TMP_PARAM AS P
		LEFT JOIN LATERAL (    SELECT MAX((SELECT "PHAN_TRAM_THUE_GTGT" FROM danh_muc_thue_suat_gia_tri_gia_tang T WHERE T.id = CDI."PHAN_TRAM_THUE_GTGT_ID")) AS "MAX_PHAN_TRAM_THUE"
		FROM sale_ex_hop_dong_ban_chi_tiet_hang_hoa_dich_vu AS CDI
		WHERE CDI."HOP_DONG_BAN_ID" = P."ID_CHUNG_TU"
		FETCH FIRST 1 ROW ONLY
		) AS R ON TRUE
		WHERE p."ID_CHUNG_TU" = p1."ID_CHUNG_TU"
		;


		DROP TABLE IF EXISTS TMP_MASTER
		;

		CREATE TEMP TABLE TMP_MASTER
		AS


		/*Thông tin trên master*/
		SELECT
		CT."ID_CHUNG_TU"
		,CT."MODEL_CHUNG_TU"

		, CT."LOAI_CHUNG_TU"
		, CT."NGAY_KY"
		, N'ngày ' || ' ' || SUBSTR(TO_CHAR(CT."NGAY_KY", 'dd/mm/yyyy'), 1, 2) || N' tháng ' || ' ' ||
		SUBSTR(TO_CHAR(CT."NGAY_KY", 'mm/dd/yyyy'), 1, 2) || N' năm ' || ' ' || TO_CHAR(CT."NGAY_KY", 'YYYY') AS "NGAY_KY_BANG_CHU"
		, CT."SO_HOP_DONG"
		, CT."MA_KHACH_HANG"
		, CT."TEN_KHACH_HANG"
		, CT."THUOC_DU_AN"
		, CT."TRICH_YEU"
		,(SELECT "MA_LOAI_TIEN" FROM res_currency T WHERE T.id = CT."currency_id") AS "LOAI_TIEN"
		, CT."TY_GIA"
		, CT."HAN_THANH_TOAN"
		, CT."DON_VI_SU_DUNG"
		, CT."TEN_NHAN_VIEN_BAN_HANG"
		, CT."DIEU_KHOAN_KHAC"
		, CASE WHEN AO."LOAI_KHACH_HANG" = '0'
		THEN AO."MA_SO_THUE"
		ELSE ''
		END                                          AS "MA_SO_THUE"
		, CASE WHEN AO."LOAI_KHACH_HANG" = '0'
		THEN AO."DIEN_THOAI"
		ELSE AO."DT_DI_DONG"
		END                                          AS "DIEN_THOAI_KHACH_HANG"
		, AO."EMAIL"                                   AS "EMAIL_KHACH_HANG"
		, AO."WEBSITE"                                 AS "WEBSITE_KHACH_HANG"
		, CASE WHEN AO."LOAI_KHACH_HANG" = '0'
		THEN AO."FAX"
		ELSE ''
		END                                          AS "FAX_KHACH_HANG"
		, AO."DIA_CHI"                                 AS "DIA_CHI_KHACH_HANG"
		, CASE WHEN AO."LOAI_KHACH_HANG" = '0'
		THEN AO."HO_VA_TEN_LIEN_HE"
		ELSE AO."HO_VA_TEN"
		END                                          AS "NGUOI_DAI_DIEN"
		, AO."CHUC_DANH"                               AS "CHUC_VU"
		, AO."DIA_DIEM_GIAO_HANG_STRING"
		, CT."HAN_GIAO_HANG"
		, COALESCE(AOB."STK_NGANG_HANG_DOI_TUONG", '') AS "STK_NGANG_HANG_DOI_TUONG"

		, COALESCE(AOB."TEN_NGANG_HANG_DOI_TUONG", '') AS "TEN_NGANG_HANG_DOI_TUONG"
		, P."MAX_PHAN_TRAM_THUE"


		, SUM(CTDI."THANH_TIEN")                       AS "TONG_TIEN_BAN"
		, SUM(CTDI."THANH_TIEN_QUY_DOI")               AS "TONG_TIEN_BAN_QUY_DOI"
		, SUM("TIEN_CHIET_KHAU")                       AS "TONG_TIEN_CHIET_KHAU"
		, SUM(
		"TIEN_CHIET_KHAU_QUY_DOI")               AS "TONG_TIEN_CHIET_KHAU_QUY_DOI"
		, SUM("TIEN_THUE_GTGT")                        AS "TONG_TIEN_THUE"
		, SUM("TIEN_THUE_GTGT_QUY_DOI")                AS "TONG_TIEN_THUE_QUY_DOI"
		, SUM("TONG_TIEN")                                                     AS "TONG_TIEN"
		, SUM("TONG_TIEN_QUY_DOI")                                       AS "TONG_TIEN_QUY_DOI"

		,SUM(CTDI."THANH_TIEN_QUY_DOI") - SUM(CTDI."TIEN_CHIET_KHAU_QUY_DOI") AS "OffsetsAmountDiscount"
		,CASE WHEN SUM(CTDI."THANH_TIEN_QUY_DOI") = 0 THEN 0
		ELSE CAST(SUM(CTDI."TIEN_CHIET_KHAU_QUY_DOI")/SUM(CTDI."THANH_TIEN_QUY_DOI") * 100 AS DECIMAL(28,2))
		END AS "AVGDiscountRate"


		FROM view_hop_dong_ban CT
		INNER JOIN TMP_PARAM P ON P."ID_CHUNG_TU" = CT."ID_CHUNG_TU"
		LEFT JOIN res_partner AO ON AO."id" = CT."KHACH_HANG_ID"
		LEFT JOIN sale_ex_hop_dong_ban_chi_tiet_hang_hoa_dich_vu CTDI
		ON CTDI."HOP_DONG_BAN_ID" = CT."ID_CHUNG_TU"
		LEFT JOIN LATERAL (    SELECT
		COALESCE(ABA."SO_TAI_KHOAN", '') AS "STK_NGANG_HANG_DOI_TUONG"
		, CASE WHEN COALESCE(ABA."CHI_NHANH", '') = ''
		THEN COALESCE(ABA."TEN_NGAN_HANG", '')
		WHEN COALESCE(ABA."TEN_NGAN_HANG", '') = ''
		THEN ''
		ELSE ABA."TEN_NGAN_HANG" || ' - ' || ABA."CHI_NHANH"
		END                              AS "TEN_NGANG_HANG_DOI_TUONG"
		FROM danh_muc_doi_tuong_chi_tiet ABA
		WHERE ABA."DOI_TUONG_ID" = CT."KHACH_HANG_ID"
		ORDER BY ABA."STT"
		FETCH FIRST 1 ROW ONLY
		) AS AOB ON TRUE
		GROUP BY
		CT."ID_CHUNG_TU"
		,CT."MODEL_CHUNG_TU"
		, CT."LOAI_CHUNG_TU"
		, CT."NGAY_KY"

		, CT."SO_HOP_DONG"
		, CT."MA_KHACH_HANG"
		, CT."TEN_KHACH_HANG"
		, CT."THUOC_DU_AN"
		, CT."TRICH_YEU"
		, CT."currency_id"
		, CT."TY_GIA"
		, CT."HAN_THANH_TOAN"
		, CT."DON_VI_SU_DUNG"
		, CT."TEN_NHAN_VIEN_BAN_HANG"
		, CT."DIEU_KHOAN_KHAC"
		, CASE WHEN AO."LOAI_KHACH_HANG" = '0'
		THEN AO."MA_SO_THUE"
		ELSE ''
		END
		, CASE WHEN AO."LOAI_KHACH_HANG" = '0'
		THEN AO."DIEN_THOAI"
		ELSE AO."DT_DI_DONG"
		END
		, AO."EMAIL"
		, AO."WEBSITE"
		, CASE WHEN AO."LOAI_KHACH_HANG" = '0'
		THEN AO."FAX"
		ELSE ''
		END
		, AO."DIA_CHI"
		, CASE WHEN AO."LOAI_KHACH_HANG" = '0'
		THEN AO."HO_VA_TEN_LIEN_HE"
		ELSE AO."HO_VA_TEN"
		END
		, AO."CHUC_DANH"
		, AO."DIA_DIEM_GIAO_HANG_STRING"
		, CT."HAN_GIAO_HANG"
		, COALESCE(AOB."STK_NGANG_HANG_DOI_TUONG", '')

		, COALESCE(AOB."TEN_NGANG_HANG_DOI_TUONG", '')
		, P."MAX_PHAN_TRAM_THUE"

		;

		/*Thông tin chi tiết*/

		DROP TABLE IF EXISTS TMP_CHI_TIET
		;

		CREATE TEMP TABLE TMP_CHI_TIET
		AS
		SELECT
		P."ID_CHUNG_TU"
		, COALESCE(CTDI."STT", -1) AS "STT"
		, II."MA"
		, CTDI."TEN_HANG"          AS "TEN_HANG"
		, CTDI."SO_LUONG_YEU_CAU"
		, CASE WHEN CACH_LAY_SL_DA_GIAO_CUA_VTHH_TREN_DON_DH_HDB = TRUE
		THEN CTDI."SO_LUONG_DA_GIAO"
		ELSE "SO_LUONG_DA_GIAO"
		END                      AS "SO_LUONG_DA_GIAO"
		, CASE WHEN CACH_LAY_SL_DA_GIAO_CUA_VTHH_TREN_DON_DH_HDB = TRUE
		THEN CTDI."SO_LUONG_DA_GIAO"
		ELSE "SO_LUONG_DA_GIAO_NAM_TRUOC"
		END                      AS "SO_LUONG_DA_GIAO_NAM_TRUOC"

		, CTDI."DON_GIA"           AS "DON_GIA"
		, CASE WHEN CTDI."SO_LUONG_YEU_CAU" = 0
		THEN 0
		ELSE CTDI."THANH_TIEN_QUY_DOI" / CTDI."SO_LUONG_YEU_CAU"
		END                      AS "DON_GIA_QUY_DOI"
		, CTDI."THANH_TIEN"
		, CTDI."THANH_TIEN_QUY_DOI"
		, CTDI."TY_LE_CK"
		, CTDI."TIEN_CHIET_KHAU"
		, CTDI."TIEN_CHIET_KHAU_QUY_DOI"
		,(SELECT "PHAN_TRAM_THUE_GTGT" FROM danh_muc_thue_suat_gia_tri_gia_tang T WHERE T.id = CTDI."PHAN_TRAM_THUE_GTGT_ID")
		, CTDI."TIEN_THUE_GTGT"
		, CTDI."TIEN_THUE_GTGT_QUY_DOI"
		, U1."DON_VI_TINH"         AS "DVT"
		, U2."DON_VI_TINH"         AS "DVT_CHINH_DVC"


		FROM TMP_PARAM P
		LEFT JOIN sale_ex_hop_dong_ban_chi_tiet_hang_hoa_dich_vu CTDI
		ON CTDI."HOP_DONG_BAN_ID" = P."ID_CHUNG_TU"
		LEFT JOIN danh_muc_vat_tu_hang_hoa II ON II."id" = CTDI."MA_HANG_ID"
		LEFT JOIN danh_muc_don_vi_tinh U1 ON U1."id" = CTDI."DVT_ID"
		LEFT JOIN danh_muc_don_vi_tinh U2 ON U2."id" = CTDI."DVT_ID"
		ORDER BY CTDI."STT"
		;


		END $$

		;


		SELECT *
		FROM TMP_MASTER

		;
		"""
		return self.execute(query)
	
	def ham_lay_du_lieu_sql_tra_ve_detail(self,refTypeList):
		query = """
		DO LANGUAGE plpgsql $$
		DECLARE

		ListParam                        VARCHAR := N'""" + refTypeList + """';

		rec                                          RECORD;


		CACH_LAY_SL_DA_GIAO_CUA_VTHH_TREN_DON_DH_HDB BOOLEAN;

		PHAN_THAP_PHAN_CUA_HE_SO_TY_LE               INT;


		BEGIN


		SELECT value
		INTO CACH_LAY_SL_DA_GIAO_CUA_VTHH_TREN_DON_DH_HDB
		FROM ir_config_parameter
		WHERE key = 'he_thong.CACH_LAY_SL_DA_GIAO_CUA_VTHH_TREN_DON_DH_HDB'
		FETCH FIRST 1 ROW ONLY
		;

		SELECT value
		INTO PHAN_THAP_PHAN_CUA_HE_SO_TY_LE
		FROM ir_config_parameter
		WHERE key = 'he_thong.PHAN_THAP_PHAN_CUA_HE_SO_TY_LE'
		FETCH FIRST 1 ROW ONLY
		;


		DROP TABLE IF EXISTS TMP_PARAM
		;

		DROP SEQUENCE IF EXISTS TMP_ID_CHUNG_TU_seq
		;

		CREATE TEMP SEQUENCE TMP_ID_CHUNG_TU_seq
		;

		CREATE TEMP TABLE TMP_PARAM
		(
		"ID_CHUNG_TU"        INT,
		"LOAI_CHUNG_TU"      INT,
		"MAX_PHAN_TRAM_THUE" FLOAT,

		"STT"                INT DEFAULT NEXTVAL('TMP_ID_CHUNG_TU_seq')
		PRIMARY KEY

		)
		;

		INSERT INTO TMP_PARAM
		SELECT

		Value1
		, Value2
		, NULL


		FROM CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(ListParam, ',', ';') F
		INNER JOIN danh_muc_reftype R ON F.Value2 = R."REFTYPE"
		;

		UPDATE TMP_PARAM P1
		SET "MAX_PHAN_TRAM_THUE" = R."MAX_PHAN_TRAM_THUE"
		FROM TMP_PARAM AS P
		LEFT JOIN LATERAL (    SELECT MAX((SELECT "PHAN_TRAM_THUE_GTGT" FROM danh_muc_thue_suat_gia_tri_gia_tang T WHERE T.id = CDI."PHAN_TRAM_THUE_GTGT_ID")) AS "MAX_PHAN_TRAM_THUE"
		FROM sale_ex_hop_dong_ban_chi_tiet_hang_hoa_dich_vu AS CDI
		WHERE CDI."HOP_DONG_BAN_ID" = P."ID_CHUNG_TU"
		FETCH FIRST 1 ROW ONLY
		) AS R ON TRUE
		WHERE p."ID_CHUNG_TU" = p1."ID_CHUNG_TU"
		;


		DROP TABLE IF EXISTS TMP_MASTER
		;

		CREATE TEMP TABLE TMP_MASTER
		AS


		/*Thông tin trên master*/
		SELECT
		CT."ID_CHUNG_TU"
		,CT."MODEL_CHUNG_TU"

		, CT."LOAI_CHUNG_TU"
		, CT."NGAY_KY"
		, N'ngày ' || ' ' || SUBSTR(TO_CHAR(CT."NGAY_KY", 'dd/mm/yyyy'), 1, 2) || N' tháng ' || ' ' ||
		SUBSTR(TO_CHAR(CT."NGAY_KY", 'mm/dd/yyyy'), 1, 2) || N' năm ' || ' ' || TO_CHAR(CT."NGAY_KY", 'YYYY') AS "NGAY_KY_BANG_CHU"
		, CT."SO_HOP_DONG"
		, CT."MA_KHACH_HANG"
		, CT."TEN_KHACH_HANG"
		, CT."THUOC_DU_AN"
		, CT."TRICH_YEU"
		,(SELECT "MA_LOAI_TIEN" FROM res_currency T WHERE T.id = CT."currency_id") AS "LOAI_TIEN"
		, CT."TY_GIA"
		, CT."HAN_THANH_TOAN"
		, CT."DON_VI_SU_DUNG"
		, CT."TEN_NHAN_VIEN_BAN_HANG"
		, CT."DIEU_KHOAN_KHAC"
		, CASE WHEN AO."LOAI_KHACH_HANG" = '0'
		THEN AO."MA_SO_THUE"
		ELSE ''
		END                                          AS "MA_SO_THUE"
		, CASE WHEN AO."LOAI_KHACH_HANG" = '0'
		THEN AO."DIEN_THOAI"
		ELSE AO."DT_DI_DONG"
		END                                          AS "DIEN_THOAI_KHACH_HANG"
		, AO."EMAIL"                                   AS "EMAIL_KHACH_HANG"
		, AO."WEBSITE"                                 AS "WEBSITE_KHACH_HANG"
		, CASE WHEN AO."LOAI_KHACH_HANG" = '0'
		THEN AO."FAX"
		ELSE ''
		END                                          AS "FAX_KHACH_HANG"
		, AO."DIA_CHI"                                 AS "DIA_CHI_KHACH_HANG"
		, CASE WHEN AO."LOAI_KHACH_HANG" = '0'
		THEN AO."HO_VA_TEN_LIEN_HE"
		ELSE AO."HO_VA_TEN"
		END                                          AS "NGUOI_DAI_DIEN"
		, AO."CHUC_DANH"                               AS "CHUC_VU"
		, AO."DIA_DIEM_GIAO_HANG_STRING"
		, CT."HAN_GIAO_HANG"
		, COALESCE(AOB."STK_NGANG_HANG_DOI_TUONG", '') AS "STK_NGANG_HANG_DOI_TUONG"

		, COALESCE(AOB."TEN_NGANG_HANG_DOI_TUONG", '') AS "TEN_NGANG_HANG_DOI_TUONG"
		, P."MAX_PHAN_TRAM_THUE"


		, SUM(CTDI."THANH_TIEN")                       AS "TONG_TIEN_BAN"
		, SUM(CTDI."THANH_TIEN_QUY_DOI")               AS "TONG_TIEN_BAN_QUY_DOI"
		, SUM("TIEN_CHIET_KHAU")                       AS "TONG_TIEN_CHIET_KHAU"
		, SUM(
		"TIEN_CHIET_KHAU_QUY_DOI")               AS "TONG_TIEN_CHIET_KHAU_QUY_DOI"
		, SUM("TIEN_THUE_GTGT")                        AS "TONG_TIEN_THUE"
		, SUM("TIEN_THUE_GTGT_QUY_DOI")                AS "TONG_TIEN_THUE_QUY_DOI"
		, SUM("TONG_TIEN")                                                     AS "TONG_TIEN"
		, SUM("TONG_TIEN_QUY_DOI")                                       AS "TONG_TIEN_QUY_DOI"

		,SUM(CTDI."THANH_TIEN_QUY_DOI") - SUM(CTDI."TIEN_CHIET_KHAU_QUY_DOI") AS "OffsetsAmountDiscount"
		,CASE WHEN SUM(CTDI."THANH_TIEN_QUY_DOI") = 0 THEN 0
		ELSE CAST(SUM(CTDI."TIEN_CHIET_KHAU_QUY_DOI")/SUM(CTDI."THANH_TIEN_QUY_DOI") * 100 AS DECIMAL(28,2))
		END AS "AVGDiscountRate"


		FROM view_hop_dong_ban CT
		INNER JOIN TMP_PARAM P ON P."ID_CHUNG_TU" = CT."ID_CHUNG_TU"
		LEFT JOIN res_partner AO ON AO."id" = CT."KHACH_HANG_ID"
		LEFT JOIN sale_ex_hop_dong_ban_chi_tiet_hang_hoa_dich_vu CTDI
		ON CTDI."HOP_DONG_BAN_ID" = CT."ID_CHUNG_TU"
		LEFT JOIN LATERAL (    SELECT
		COALESCE(ABA."SO_TAI_KHOAN", '') AS "STK_NGANG_HANG_DOI_TUONG"
		, CASE WHEN COALESCE(ABA."CHI_NHANH", '') = ''
		THEN COALESCE(ABA."TEN_NGAN_HANG", '')
		WHEN COALESCE(ABA."TEN_NGAN_HANG", '') = ''
		THEN ''
		ELSE ABA."TEN_NGAN_HANG" || ' - ' || ABA."CHI_NHANH"
		END                              AS "TEN_NGANG_HANG_DOI_TUONG"
		FROM danh_muc_doi_tuong_chi_tiet ABA
		WHERE ABA."DOI_TUONG_ID" = CT."KHACH_HANG_ID"
		ORDER BY ABA."STT"
		FETCH FIRST 1 ROW ONLY
		) AS AOB ON TRUE
		GROUP BY
		CT."ID_CHUNG_TU"
		,CT."MODEL_CHUNG_TU"
		, CT."LOAI_CHUNG_TU"
		, CT."NGAY_KY"

		, CT."SO_HOP_DONG"
		, CT."MA_KHACH_HANG"
		, CT."TEN_KHACH_HANG"
		, CT."THUOC_DU_AN"
		, CT."TRICH_YEU"
		, CT."currency_id"
		, CT."TY_GIA"
		, CT."HAN_THANH_TOAN"
		, CT."DON_VI_SU_DUNG"
		, CT."TEN_NHAN_VIEN_BAN_HANG"
		, CT."DIEU_KHOAN_KHAC"
		, CASE WHEN AO."LOAI_KHACH_HANG" = '0'
		THEN AO."MA_SO_THUE"
		ELSE ''
		END
		, CASE WHEN AO."LOAI_KHACH_HANG" = '0'
		THEN AO."DIEN_THOAI"
		ELSE AO."DT_DI_DONG"
		END
		, AO."EMAIL"
		, AO."WEBSITE"
		, CASE WHEN AO."LOAI_KHACH_HANG" = '0'
		THEN AO."FAX"
		ELSE ''
		END
		, AO."DIA_CHI"
		, CASE WHEN AO."LOAI_KHACH_HANG" = '0'
		THEN AO."HO_VA_TEN_LIEN_HE"
		ELSE AO."HO_VA_TEN"
		END
		, AO."CHUC_DANH"
		, AO."DIA_DIEM_GIAO_HANG_STRING"
		, CT."HAN_GIAO_HANG"
		, COALESCE(AOB."STK_NGANG_HANG_DOI_TUONG", '')

		, COALESCE(AOB."TEN_NGANG_HANG_DOI_TUONG", '')
		, P."MAX_PHAN_TRAM_THUE"

		;

		/*Thông tin chi tiết*/

		DROP TABLE IF EXISTS TMP_CHI_TIET
		;

		CREATE TEMP TABLE TMP_CHI_TIET
		AS
		SELECT
		P."ID_CHUNG_TU"
		, COALESCE(CTDI."STT", -1) AS "STT"
		, II."MA"
		, CTDI."TEN_HANG"          AS "TEN_HANG"
		, CTDI."SO_LUONG_YEU_CAU"
		, CASE WHEN CACH_LAY_SL_DA_GIAO_CUA_VTHH_TREN_DON_DH_HDB = TRUE
		THEN CTDI."SO_LUONG_DA_GIAO"
		ELSE "SO_LUONG_DA_GIAO"
		END                      AS "SO_LUONG_DA_GIAO"
		, CASE WHEN CACH_LAY_SL_DA_GIAO_CUA_VTHH_TREN_DON_DH_HDB = TRUE
		THEN CTDI."SO_LUONG_DA_GIAO"
		ELSE "SO_LUONG_DA_GIAO_NAM_TRUOC"
		END                      AS "SO_LUONG_DA_GIAO_NAM_TRUOC"

		, CTDI."DON_GIA"           AS "DON_GIA"
		, CASE WHEN CTDI."SO_LUONG_YEU_CAU" = 0
		THEN 0
		ELSE CTDI."THANH_TIEN_QUY_DOI" / CTDI."SO_LUONG_YEU_CAU"
		END                      AS "DON_GIA_QUY_DOI"
		, CTDI."THANH_TIEN"
		, CTDI."THANH_TIEN_QUY_DOI"
		, CTDI."TY_LE_CK"
		, CTDI."TIEN_CHIET_KHAU"
		, CTDI."TIEN_CHIET_KHAU_QUY_DOI"
		,(SELECT "PHAN_TRAM_THUE_GTGT" FROM danh_muc_thue_suat_gia_tri_gia_tang T WHERE T.id = CTDI."PHAN_TRAM_THUE_GTGT_ID")
		, CTDI."TIEN_THUE_GTGT"
		, CTDI."TIEN_THUE_GTGT_QUY_DOI"
		, U1."DON_VI_TINH"         AS "DVT"
		, U2."DON_VI_TINH"         AS "DVT_CHINH_DVC"


		FROM TMP_PARAM P
		LEFT JOIN sale_ex_hop_dong_ban_chi_tiet_hang_hoa_dich_vu CTDI
		ON CTDI."HOP_DONG_BAN_ID" = P."ID_CHUNG_TU"
		LEFT JOIN danh_muc_vat_tu_hang_hoa II ON II."id" = CTDI."MA_HANG_ID"
		LEFT JOIN danh_muc_don_vi_tinh U1 ON U1."id" = CTDI."DVT_ID"
		LEFT JOIN danh_muc_don_vi_tinh U2 ON U2."id" = CTDI."DVT_ID"
		ORDER BY CTDI."STT"
		;


		END $$

		;


		SELECT *
		FROM TMP_CHI_TIET
		ORDER BY "STT"

		;
		"""
		return self.execute(query)
