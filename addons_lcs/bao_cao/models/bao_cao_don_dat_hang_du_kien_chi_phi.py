# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round
from datetime import timedelta, datetime

class BAO_CAO_DON_DAT_HANG_DU_KIEN_CHI_PHI(models.Model):
	_name = 'bao.cao.don.dat.hang.chi.phi.du.kien'
	_auto = False

	ref = fields.Char(string='Reffence ID')

	RowNumber = fields.Integer(string='RowNumber')
	ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
	MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')

	TEN_KHACH_HANG = fields.Char(string='Tên khách hàng') #AccountObjectName
	DIA_CHI = fields.Char(string='Địa chỉ') #AccountObjectAddress
	
	NGAY_DON_HANG = fields.Char(string='Địa chỉ') #RefDate
	DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải') #JournalMemo
	SO_DON_HANG = fields.Char(string='Diễn giải', help='Diễn giải') #RefNo

	SO_DIEN_THOAI = fields.Char(string='Loại tiền') #Tel
	LOAI_TIEN = fields.Char(string='Loại tiền') #AccountObjectAddress

	TONG_CHI_PHI = fields.Monetary(string='Loại tiền',currency_field='currency_id') #AccountObjectAddress
	TONG_THANH_TIEN_BAN = fields.Monetary(string='Loại tiền',currency_field='currency_id') #AccountObjectAddress
	TONG_PHAN_TRAM_CHI_PHI = fields.Float(string='Loại tiền',digits=decimal_precision.get_precision('VND')) #AccountObjectAddress

	

	
	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())

	ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.don.dat.hang.chi.phi.du.kien.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')



class BAO_CAO_DON_DAT_HANG_DU_KIEN_CHI_PHI_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_saordervoucher3520dkcp'

	@api.model
	def get_report_values(self, docids, data=None):
		############### START SQL lấy dữ liệu ###############
		refTypeList, records = self.get_reftype_list(data)
		
		sql_result = self.ham_lay_du_lieu_sql_tra_ve(refTypeList)

		

		rowspan_dict = {}
		# Tìm số lượng thành phần nguyên liệu của mỗi món ăn
		for line in sql_result:
			row_key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU')) + line.get('TEN_THANH_PHAM')
			rowspan_dict[row_key] = rowspan_dict.get(row_key, 0) + 1

		last_row_key = ''
		
		for line in sql_result:
    			
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
			row_key = key + line.get('TEN_THANH_PHAM')
			if row_key != last_row_key:
				last_row_key = row_key
				line['ROWSPAN'] = rowspan_dict.get(row_key)
				
			master_data = self.env['bao.cao.don.dat.hang.chi.phi.du.kien'].convert_for_update(line)
			detail_data = self.env['bao.cao.don.dat.hang.chi.phi.du.kien.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
				records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.don.dat.hang.chi.phi.du.kien.chi.tiet'].new(detail_data)
		
		docs = [records.get(k) for k in records]

		for record in docs:

			# tính tổng chi phí , thành tiền bán và phần trăm
			if record.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
				dict_don_hang = {}
				for line in record.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
					key_ten_thanh_pham = line.TEN_THANH_PHAM
					if key_ten_thanh_pham not in dict_don_hang:
						dict_don_hang[key_ten_thanh_pham] = []
					dict_don_hang[key_ten_thanh_pham] += [line]

				dict_cap_nhat = {}
				if dict_don_hang != {}:
					for thanh_pham in dict_don_hang:
						chi_tiet_ids = dict_don_hang[thanh_pham]
						if chi_tiet_ids:
							tong_chi_phi = 0
							for chi_tiet in chi_tiet_ids:
								tong_chi_phi += chi_tiet.THANH_TIEN
							if thanh_pham not in dict_cap_nhat:
								dict_cap_nhat[thanh_pham] = tong_chi_phi

				for ket_qua in record.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
					key = ket_qua.TEN_THANH_PHAM
					if key in dict_cap_nhat:
						ket_qua.TONG_CHI_PHI = dict_cap_nhat[key]
						if ket_qua.THANH_TIEN_BAN > 0:
							ket_qua.PT_CHI_PHI = float_round((dict_cap_nhat[key]/ket_qua.THANH_TIEN_BAN)*100,2)

		# ------------------------------end------------------------------------------------------------------------
			if not record.LOAI_TIEN:
				record.currency_id = self.lay_loai_tien_mac_dinh()
			else:
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', record.LOAI_TIEN)],limit=1)
				if loai_tien_id:
					record.currency_id = loai_tien_id.id

			if record.NGAY_DON_HANG:
				record.NGAY_DON_HANG = 	datetime.strptime(record.NGAY_DON_HANG,'%Y-%m-%d').date().strftime('%d/%m/%Y')

			tong_chi_phi = 0 
			tong_thanh_tien_ban = 0
			# tong_phan_tram_chi_phi = 0

			dict_thanh_pham = {}
			for line in record.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
				key = line.TEN_THANH_PHAM
				if key not in dict_thanh_pham:
					dict_thanh_pham[key] = line

			# for line in record.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
			# 	tong_chi_phi += line.TONG_CHI_PHI
			# 	tong_thanh_tien_ban += line.THANH_TIEN_BAN
			# 	tong_phan_tram_chi_phi += line.PT_CHI_PHI
			for thanh_pham in dict_thanh_pham:
				tong_chi_phi += dict_thanh_pham[thanh_pham].TONG_CHI_PHI
				tong_thanh_tien_ban += dict_thanh_pham[thanh_pham].THANH_TIEN_BAN
				# tong_phan_tram_chi_phi += dict_thanh_pham[thanh_pham].PT_CHI_PHI

			record.TONG_CHI_PHI = tong_chi_phi
			record.TONG_THANH_TIEN_BAN = tong_thanh_tien_ban
			if tong_thanh_tien_ban > 0:
				record.TONG_PHAN_TRAM_CHI_PHI = float_round((tong_chi_phi/tong_thanh_tien_ban)*100,2)

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

	DROP SEQUENCE IF EXISTS TMP_ID_CHUNG_TU_seq
	;

	CREATE TEMP SEQUENCE TMP_ID_CHUNG_TU_seq
	;

	CREATE TEMP TABLE TMP_PARAM
	(
		"ID_CHUNG_TU"   INT,
		"LOAI_CHUNG_TU" INT,


		"STT"           INT DEFAULT NEXTVAL('TMP_ID_CHUNG_TU_seq')
			PRIMARY KEY

	)
	;

	INSERT INTO TMP_PARAM
		SELECT *


		FROM CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(ListParam, ',', ';')

	;

	DROP TABLE IF EXISTS TMP_DON_DAT_HANG
	;

	CREATE TEMP TABLE TMP_DON_DAT_HANG
		AS


			SELECT
				  ROW_NUMBER()
				  OVER (
					  ORDER BY
				F."STT",
				SD."sequence",
				SD.id,
				dmnvl.id,
				vthhnvl."MA",
				dmnvl."sequence",
				SD."THU_TU_SAP_XEP_CHI_TIET"  )  AS "RowNumber"
				,S."id" AS "ID_CHUNG_TU"
				,'account.ex.don.dat.hang' AS "MODEL_CHUNG_TU"
				, S."TEN_KHACH_HANG"
				,
				A."MA" AS "MA_KHACH_HANG"
				, S."DIA_CHI"
				, S."MA_SO_THUE"
				, e."MA"                                                                                       AS "MA_NHAN_VIEN"
				,
				  e."HO_VA_TEN"                                                                                AS "TEN_NHAN_VIEN_BAN_HANG"
				, S."DIEN_GIAI"
				, S."NGAY_DON_HANG"
				, S."SO_DON_HANG"
				,( SELECT "MA_LOAI_TIEN" FROM res_currency T WHERE T.id = S."currency_id") AS "LOAI_TIEN"
				, S."TY_GIA"
				, S."TONG_TIEN_HANG_QUY_DOI" - S."TONG_CHIET_KHAU_QUY_DOI" +  S."TONG_TIEN_THUE_GTGT_QUY_DOI"                         AS "TONG_TIEN_QUY_DOI"
				, S."NGAY_GIAO_HANG"
				, S."DIA_DIEM_GIAO_HANG"
				, S."DIEU_KHOAN_KHAC"
				, PT."TEN_DIEU_KHOAN"
				, CASE WHEN A."LOAI_KHACH_HANG" = '0'
				THEN A."DIEN_THOAI"
				  ELSE A."DT_DI_DONG"
				  END                                                                                          AS "SO_DIEN_THOAI"
				, A."FAX"
				,I."TEN" AS "TEN_THANH_PHAM"
				,vthhnvl."TEN" AS "TEN_NGUYEN_VAT_LIEU"
				,dvt."DON_VI_TINH" AS "DVT_NGUYEN_VAT_LIEU"
				,SD."SO_LUONG" AS "SO_LUONG_DAT"
				,dmnvl."SO_LUONG" AS "DINH_MUC_NVL_1_MON"
				,coalesce(SD."SO_LUONG",0)*coalesce(dmnvl."SO_LUONG",0) AS "TONG_KHOI_LUONG_NVL"
				,vthhnvl."DON_GIA_MUA_CO_DINH" AS "DON_GIA_MUA"
				,coalesce(vthhnvl."DON_GIA_MUA_CO_DINH",0)*coalesce(SD."SO_LUONG",0)*coalesce(dmnvl."SO_LUONG",0) AS "THANH_TIEN"
				,cast(0 AS FLOAT) AS "TONG_CHI_PHI"
				,coalesce(SD."THANH_TIEN") AS "THANH_TIEN_BAN"
				,cast(0 AS FLOAT) AS "PT_CHI_PHI"

			FROM account_ex_don_dat_hang S
				INNER JOIN account_ex_don_dat_hang_chi_tiet SD ON S."id" = SD."DON_DAT_HANG_CHI_TIET_ID"
				INNER JOIN TMP_PARAM F ON F."ID_CHUNG_TU" = S."id"
				LEFT JOIN res_partner A ON S."KHACH_HANG_ID" = A."id"
				LEFT JOIN res_partner E ON S."NV_BAN_HANG_ID" = E."id"
				INNER JOIN danh_muc_vat_tu_hang_hoa I ON SD."MA_HANG_ID" = I."id"
				LEFT JOIN danh_muc_dieu_khoan_thanh_toan AS PT ON S."DIEU_KHOAN_TT_ID" = PT."id"
				LEFT JOIN danh_muc_vat_tu_hang_hoa_chi_tiet_dinh_muc_nvl dmnvl ON SD."MA_HANG_ID" = dmnvl."VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_ID"
				LEFT JOIN danh_muc_vat_tu_hang_hoa vthhnvl ON dmnvl."MA_NGUYEN_VAT_LIEU_ID" = vthhnvl.id
				LEFT JOIN  danh_muc_don_vi_tinh dvt ON vthhnvl."DVT_CHINH_ID" = dvt.id

			ORDER BY
				F."STT",
				SD."sequence",
				SD.id,
				SD."THU_TU_SAP_XEP_CHI_TIET",
				dmnvl.id,
				dmnvl."sequence",
				vthhnvl."MA";



END $$

;

SELECT  * FROM TMP_DON_DAT_HANG

 ORDER BY
	 "RowNumber"
		"""
		return self.execute(query)

	
