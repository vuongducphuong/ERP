# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision

class bao_cao_bien_ban_kiem_ke(models.Model):
	_name = 'bao.cao.bien.ban.kiem.ke'
	_auto = False

	id = fields.Integer(string='id')
	SO = fields.Char(string='SO', help='RefNo')
	NGAY = fields.Date(string='NGAY', help='RefDate')
	GIO = fields.Char(string='GIO')
	MUC_DICH = fields.Char(string='MUC_DICH', help='JournalMemo')
	DEN_NGAY = fields.Date(string='DEN_NGAY', help='AuditDate')
	KET_LUAN = fields.Char(string='KET_LUAN', help='Summary')
	DA_XU_LY_CHENH_LECH = fields.Boolean(string='DA_XU_LY_CHENH_LECH', help='IsExecuted')
	SortOrderMaster = fields.Integer(string='SortOrderMaster', help='SortOrderMaster')

	strDateTime = fields.Char()
	bao_cao_bien_ban_kiem_ke_thanh_vien_tham_gia_IDS = fields.One2many('bao.cao.bien.ban.kiem.ke.thanh.vien.tham.gia', 'BIEN_BAN_KIEM_KE_ID')
	bao_cao_bien_ban_kiem_ke_vthh_dieu_chinh_IDS = fields.One2many('bao.cao.bien.ban.kiem.ke.vthh.can.dieu.chinh', 'BIEN_BAN_KIEM_KE_ID')

class bao_cao_bien_ban_kiem_ke_group(models.Model):
	_name = 'bao.cao.bien.ban.kiem.ke.group'
	_auto = False
	_description = 'Nhóm các biên bản kiêm kê theo kho'

	MA_KHO = fields.Char()
	TEN_KHO = fields.Char()
	sum_SO_LUONG_SO_KE_TOAN = fields.Float(digits=decimal_precision.get_precision('SO_LUONG'))
	sum_SO_LUONG_KIEM_KE = fields.Float(digits=decimal_precision.get_precision('SO_LUONG'))
	sum_SO_LUONG_CHENH_LECH = fields.Float(digits=decimal_precision.get_precision('SO_LUONG'))
	sum_GIA_TRI_SO_KE_TOAN = fields.Monetary(currency_field='base_currency_id')
	sum_GIA_TRI_KIEM_KE = fields.Monetary(currency_field='base_currency_id')
	sum_GIA_TRI_CHENH_LECH = fields.Monetary(currency_field='base_currency_id')
	base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)

	data = fields.One2many('bao.cao.bien.ban.kiem.ke.vthh.can.dieu.chinh', 'BIEN_BAN_KIEM_KE_GROUP_ID')

class bao_cao_bien_ban_kiem_ke_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_vinaudit'

	@api.model
	def get_report_values(self, docids, data=None):
			
		refTypeList, records = self.get_reftype_list(data)
		sql_master = self.ham_lay_du_lieu_sql_tra_ve_master(refTypeList)
		sql_detail_thanh_vien_tham_gia = self.ham_lay_du_lieu_sql_tra_ve_thanh_vien_tham_gia(refTypeList)
		sql_detail_vthh_can_dieu_chinh = self.ham_lay_du_lieu_sql_tra_ve_vthh_can_dieu_chinh(refTypeList)
		
		# 1. Update master
		for line in sql_master:
			key = 'stock.ex.kiem.ke.bang.kiem.ke.vat.tu.hang.hoa.form' + ',' + str(line.get('id'))
			master_data = self.env['bao.cao.bien.ban.kiem.ke'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
		
		# 2. Update detail_thanh_vien_tham_gia
		for line in sql_detail_thanh_vien_tham_gia:
			key = 'stock.ex.kiem.ke.bang.kiem.ke.vat.tu.hang.hoa.form' + ',' + str(line.get('ID_CHUNG_TU'))
			detail_data1 = self.env['bao.cao.bien.ban.kiem.ke.thanh.vien.tham.gia'].convert_for_update(line)
			if records.get(key):
				records[key].bao_cao_bien_ban_kiem_ke_thanh_vien_tham_gia_IDS += self.env['bao.cao.bien.ban.kiem.ke.thanh.vien.tham.gia'].new(detail_data1)
		
		# 2. Update detail_vthh_can_dieu_chinh
		for line in sql_detail_vthh_can_dieu_chinh:
			key = 'stock.ex.kiem.ke.bang.kiem.ke.vat.tu.hang.hoa.form' + ',' + str(line.get('ID_CHUNG_TU'))
			detail_data2 = self.env['bao.cao.bien.ban.kiem.ke.vthh.can.dieu.chinh'].convert_for_update(line)
			if records.get(key):
				records[key].bao_cao_bien_ban_kiem_ke_vthh_dieu_chinh_IDS += self.env['bao.cao.bien.ban.kiem.ke.vthh.can.dieu.chinh'].new(detail_data2)

		# records = self.env['tien.luong.bang.cham.cong.chi.tiet.master'].browse(docids)
		
		docs = [records.get(k) for k in records]
		grouped_datas = {}
		for record in docs:
			grouped_data = {}
			for line in record.bao_cao_bien_ban_kiem_ke_vthh_dieu_chinh_IDS:
				kho = line.MA_KHO_ID
				if not grouped_data.get(kho):
					grouped_data[kho] = self.env['bao.cao.bien.ban.kiem.ke.group'].new({
						'data': [],
						'sum_SO_LUONG_SO_KE_TOAN': 0,
						'sum_SO_LUONG_KIEM_KE': 0,
						'sum_SO_LUONG_CHENH_LECH': 0,
						'sum_GIA_TRI_SO_KE_TOAN': 0,
						'sum_GIA_TRI_KIEM_KE': 0,
						'sum_GIA_TRI_CHENH_LECH': 0,
						'MA_KHO': line.MA_KHO or '',
						'TEN_KHO': line.TEN_KHO or '',
					})

				grouped_data[kho].data += line
				grouped_data[kho].sum_SO_LUONG_SO_KE_TOAN += line.SO_LUONG_SO_KE_TOAN
				grouped_data[kho].sum_SO_LUONG_KIEM_KE += line.SO_LUONG_KIEM_KE
				grouped_data[kho].sum_SO_LUONG_CHENH_LECH += line.SO_LUONG_CHENH_LECH
				grouped_data[kho].sum_GIA_TRI_SO_KE_TOAN += line.GIA_TRI_SO_KE_TOAN
				grouped_data[kho].sum_GIA_TRI_KIEM_KE += line.GIA_TRI_KIEM_KE
				grouped_data[kho].sum_GIA_TRI_CHENH_LECH += line.GIA_TRI_CHENH_LECH
			
			grouped_datas[record.id] = grouped_data

		return {
			'docs': docs,
			'grouped_datas': grouped_datas,
	}

	def ham_lay_du_lieu_sql_tra_ve_master(self,refTypeList):
		
		query = """
				DO LANGUAGE plpgsql $$
				DECLARE

				ListIDchungtu 	VARCHAR := N'""" + refTypeList + """';

				rec           	RECORD;

				BEGIN
				DROP TABLE IF EXISTS TMP_ID_CHUNG_TU
				;

				DROP SEQUENCE IF EXISTS TMP_ID_CHUNG_TU_seq
				;

				CREATE TEMP SEQUENCE TMP_ID_CHUNG_TU_seq
				;

				CREATE TEMP TABLE TMP_ID_CHUNG_TU
				(
				"ID_CHUNG_TU"     INT,
				"LOAI_CHUNG_TU"   INT,
				"SortOrderMaster" INT DEFAULT NEXTVAL('TMP_ID_CHUNG_TU_seq')
				PRIMARY KEY

				)
				;

				INSERT INTO TMP_ID_CHUNG_TU
				SELECT

				Value1
				, Value2


				FROM CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(ListIDchungtu, ',', ';') F

				;

				-- Trả ra bảng master
				DROP TABLE IF EXISTS TMP_MASTER
				;

				CREATE TEMP TABLE TMP_MASTER
				AS

				SELECT
				INA."id"
				, INA."SO"
				, INA."NGAY"
				, INA."GIO"
				, INA."MUC_DICH"
				, INA."DEN_NGAY"
				, INA."KET_LUAN"
				, INA."DA_XU_LY_CHENH_LECH"

				, R."SortOrderMaster"
				FROM stock_ex_kiem_ke_bang_kiem_ke_vat_tu_hang_hoa_form INA
				INNER JOIN TMP_ID_CHUNG_TU R ON R."ID_CHUNG_TU" = INA."id"

				ORDER BY R."SortOrderMaster"
				;


				---------------
				DROP TABLE IF EXISTS TMP_THANH_VIEN_THAM_GIA
				;

				CREATE TEMP TABLE TMP_THANH_VIEN_THAM_GIA
				AS


				SELECT
				R."ID_CHUNG_TU"
				, INAM."HO_VA_TEN"
				, INAM."CHUC_DANH"
				, INAM."DAI_DIEN"
				, R."SortOrderMaster"
				, COALESCE(INAM."sequence", 1) AS "STT"
				FROM TMP_ID_CHUNG_TU R
				LEFT JOIN stock_ex_bang_kiem_ke_vthh_tv_tham_gia_chi_tiet_form INAM
				ON R."ID_CHUNG_TU" = INAM."BANG_KIEM_KE_VTHH_ID"
				UNION ALL
				SELECT
				R."ID_CHUNG_TU"
				, INAM."HO_VA_TEN"
				, INAM."CHUC_DANH"
				, INAM."DAI_DIEN"
				, R."SortOrderMaster"
				, 2 AS "STT"
				FROM TMP_ID_CHUNG_TU R
				LEFT JOIN stock_ex_bang_kiem_ke_vthh_tv_tham_gia_chi_tiet_form INAM
				ON R."ID_CHUNG_TU" = INAM."BANG_KIEM_KE_VTHH_ID"
				WHERE INAM."BANG_KIEM_KE_VTHH_ID" IS NULL
				UNION ALL
				SELECT
				R."ID_CHUNG_TU"
				, INAM."HO_VA_TEN"
				, INAM."CHUC_DANH"
				, INAM."DAI_DIEN"
				, R."SortOrderMaster"
				, 3 AS "STT"
				FROM TMP_ID_CHUNG_TU R
				LEFT JOIN stock_ex_bang_kiem_ke_vthh_tv_tham_gia_chi_tiet_form INAM
				ON R."ID_CHUNG_TU" = INAM."BANG_KIEM_KE_VTHH_ID"
				WHERE INAM."BANG_KIEM_KE_VTHH_ID" IS NULL
				ORDER BY
				"SortOrderMaster",
				"STT"
				;

				-- Lấy ra bảng chi tiết

				DROP TABLE IF EXISTS TMP_CHI_TIET
				;

				CREATE TEMP TABLE TMP_CHI_TIET
				AS

				SELECT
				 ROW_NUMBER()
                  OVER (
                     ORDER BY
				R."SortOrderMaster",
				S."MA_KHO",
				S."TEN_KHO",
				INAD."sequence",
				INAD."id"  )  AS "RowNumber"

				,R."ID_CHUNG_TU"
				, II."TEN"
				, II."MA"
				, INAD."MA_KHO_ID"
				, S."MA_KHO"
				, S."TEN_KHO"
				, UNIT."DON_VI_TINH" AS "DVT"

				, INAD."SO_LUONG_SO_KE_TOAN"
				, --Số lượng trên số kế toán
				INAD."GIA_TRI_SO_KE_TOAN"
				, --Thành tiền trên số kế toán
				INAD."SO_LUONG_KIEM_KE"
				, --Số lượng kiểm kê
				INAD."GIA_TRI_KIEM_KE"
				, --Thành tiền kiểm kê
				INAD."SO_LUONG_CHENH_LECH"
				, --Số lượng chênh lệch
				INAD."GIA_TRI_CHENH_LECH"
				, --Số tiền chênh lệch
				INAD."PHAM_CHAT_CON_TOT"
				, --Số lượng còn tốt
				INAD."KEM_PHAM_CHAT"
				, --Số lương kém phẩm chất
				INAD."MAT_PHAM_CHAT"
				, R."SortOrderMaster"
				, INAD."sequence"
				, SUM(INAD."SO_LUONG_SO_KE_TOAN")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_SL_SO_KE_TOAN"
				, SUM(INAD."GIA_TRI_SO_KE_TOAN")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_GIA_TRI_SO_KE_TOAN"
				, SUM(INAD."SO_LUONG_KIEM_KE")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_SL_KIEM_KE"
				, SUM(INAD."GIA_TRI_KIEM_KE")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_GIA_TRI_KIEM_KE"
				, SUM(INAD."SO_LUONG_CHENH_LECH")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_SL_CHENH_LECH"
				, SUM(INAD."GIA_TRI_CHENH_LECH")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_GIA_TRI_CHENH_LECH"
				FROM TMP_ID_CHUNG_TU R
				LEFT JOIN stock_ex_bang_kiem_ke_vthh_can_dieu_chinh_chi_tiet_form INAD --nvtoan modify 07/11/2016
				ON R."ID_CHUNG_TU" = INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID"
				LEFT JOIN danh_muc_vat_tu_hang_hoa II ON INAD."MA_HANG_ID" = II."id"
				--nvtoan modify 07/11/2016
				LEFT JOIN danh_muc_don_vi_tinh AS UNIT ON INAD."DVT_ID" = UNIT."id"
				LEFT JOIN danh_muc_kho S ON S."id" = INAD."MA_KHO_ID"
				ORDER BY
				R."SortOrderMaster",
				S."MA_KHO",
				S."TEN_KHO",
				INAD."sequence",
				INAD."id"
				;


				END $$

				;

				SELECT *
				FROM TMP_MASTER
				ORDER BY "SortOrderMaster"

				;
				"""
		return self.execute(query)
	
	def ham_lay_du_lieu_sql_tra_ve_thanh_vien_tham_gia(self,refTypeList):
			
		query = """
				DO LANGUAGE plpgsql $$
				DECLARE

				ListIDchungtu 	VARCHAR := N'""" + refTypeList + """';

				rec           	RECORD;

				BEGIN
				DROP TABLE IF EXISTS TMP_ID_CHUNG_TU
				;

				DROP SEQUENCE IF EXISTS TMP_ID_CHUNG_TU_seq
				;

				CREATE TEMP SEQUENCE TMP_ID_CHUNG_TU_seq
				;

				CREATE TEMP TABLE TMP_ID_CHUNG_TU
				(
				"ID_CHUNG_TU"     INT,
				"LOAI_CHUNG_TU"   INT,
				"SortOrderMaster" INT DEFAULT NEXTVAL('TMP_ID_CHUNG_TU_seq')
				PRIMARY KEY

				)
				;

				INSERT INTO TMP_ID_CHUNG_TU
				SELECT

				Value1
				, Value2


				FROM CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(ListIDchungtu, ',', ';') F

				;

				-- Trả ra bảng master
				DROP TABLE IF EXISTS TMP_MASTER
				;

				CREATE TEMP TABLE TMP_MASTER
				AS

				SELECT
				INA."id"
				, INA."SO"
				, INA."NGAY"
				, INA."GIO"
				, INA."MUC_DICH"
				, INA."DEN_NGAY"
				, INA."KET_LUAN"
				, INA."DA_XU_LY_CHENH_LECH"

				, R."SortOrderMaster"
				FROM stock_ex_kiem_ke_bang_kiem_ke_vat_tu_hang_hoa_form INA
				INNER JOIN TMP_ID_CHUNG_TU R ON R."ID_CHUNG_TU" = INA."id"

				ORDER BY R."SortOrderMaster"
				;


				---------------
				DROP TABLE IF EXISTS TMP_THANH_VIEN_THAM_GIA
				;

				CREATE TEMP TABLE TMP_THANH_VIEN_THAM_GIA
				AS


				SELECT
				R."ID_CHUNG_TU"
				, INAM."HO_VA_TEN"
				, INAM."CHUC_DANH"
				, INAM."DAI_DIEN"
				, R."SortOrderMaster"
				, COALESCE(INAM."sequence", 1) AS "STT"
				FROM TMP_ID_CHUNG_TU R
				LEFT JOIN stock_ex_bang_kiem_ke_vthh_tv_tham_gia_chi_tiet_form INAM
				ON R."ID_CHUNG_TU" = INAM."BANG_KIEM_KE_VTHH_ID"
				UNION ALL
				SELECT
				R."ID_CHUNG_TU"
				, INAM."HO_VA_TEN"
				, INAM."CHUC_DANH"
				, INAM."DAI_DIEN"
				, R."SortOrderMaster"
				, 2 AS "STT"
				FROM TMP_ID_CHUNG_TU R
				LEFT JOIN stock_ex_bang_kiem_ke_vthh_tv_tham_gia_chi_tiet_form INAM
				ON R."ID_CHUNG_TU" = INAM."BANG_KIEM_KE_VTHH_ID"
				WHERE INAM."BANG_KIEM_KE_VTHH_ID" IS NULL
				UNION ALL
				SELECT
				R."ID_CHUNG_TU"
				, INAM."HO_VA_TEN"
				, INAM."CHUC_DANH"
				, INAM."DAI_DIEN"
				, R."SortOrderMaster"
				, 3 AS "STT"
				FROM TMP_ID_CHUNG_TU R
				LEFT JOIN stock_ex_bang_kiem_ke_vthh_tv_tham_gia_chi_tiet_form INAM
				ON R."ID_CHUNG_TU" = INAM."BANG_KIEM_KE_VTHH_ID"
				WHERE INAM."BANG_KIEM_KE_VTHH_ID" IS NULL
				ORDER BY
				"SortOrderMaster",
				"STT"
				;

				-- Lấy ra bảng chi tiết

				DROP TABLE IF EXISTS TMP_CHI_TIET
				;

				CREATE TEMP TABLE TMP_CHI_TIET
				AS

				SELECT
				R."ID_CHUNG_TU"
				, II."TEN"
				, II."MA"
				, INAD."MA_KHO_ID"
				, S."MA_KHO"
				, S."TEN_KHO"
				, UNIT."DON_VI_TINH" AS "DVT"

				, INAD."SO_LUONG_SO_KE_TOAN"
				, --Số lượng trên số kế toán
				INAD."GIA_TRI_SO_KE_TOAN"
				, --Thành tiền trên số kế toán
				INAD."SO_LUONG_KIEM_KE"
				, --Số lượng kiểm kê
				INAD."GIA_TRI_KIEM_KE"
				, --Thành tiền kiểm kê
				INAD."SO_LUONG_CHENH_LECH"
				, --Số lượng chênh lệch
				INAD."GIA_TRI_CHENH_LECH"
				, --Số tiền chênh lệch
				INAD."PHAM_CHAT_CON_TOT"
				, --Số lượng còn tốt
				INAD."KEM_PHAM_CHAT"
				, --Số lương kém phẩm chất
				INAD."MAT_PHAM_CHAT"
				, R."SortOrderMaster"
				, INAD."sequence"
				, SUM(INAD."SO_LUONG_SO_KE_TOAN")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_SL_SO_KE_TOAN"
				, SUM(INAD."GIA_TRI_SO_KE_TOAN")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_GIA_TRI_SO_KE_TOAN"
				, SUM(INAD."SO_LUONG_KIEM_KE")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_SL_KIEM_KE"
				, SUM(INAD."GIA_TRI_KIEM_KE")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_GIA_TRI_KIEM_KE"
				, SUM(INAD."SO_LUONG_CHENH_LECH")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_SL_CHENH_LECH"
				, SUM(INAD."GIA_TRI_CHENH_LECH")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_GIA_TRI_CHENH_LECH"
				FROM TMP_ID_CHUNG_TU R
				LEFT JOIN stock_ex_bang_kiem_ke_vthh_can_dieu_chinh_chi_tiet_form INAD --nvtoan modify 07/11/2016
				ON R."ID_CHUNG_TU" = INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID"
				LEFT JOIN danh_muc_vat_tu_hang_hoa II ON INAD."MA_HANG_ID" = II."id"
				--nvtoan modify 07/11/2016
				LEFT JOIN danh_muc_don_vi_tinh AS UNIT ON INAD."DVT_ID" = UNIT."id"
				LEFT JOIN danh_muc_kho S ON S."id" = INAD."MA_KHO_ID"
				ORDER BY
				R."SortOrderMaster",
				S."MA_KHO",
				S."TEN_KHO",
				INAD."sequence",
				INAD."id"
				;


				END $$

				;

				SELECT *
				FROM TMP_THANH_VIEN_THAM_GIA
				ORDER BY
				"SortOrderMaster",
				"STT"

				;
				"""
		return self.execute(query)
	
	def ham_lay_du_lieu_sql_tra_ve_vthh_can_dieu_chinh(self,refTypeList):		
		query = """
				DO LANGUAGE plpgsql $$
				DECLARE

				ListIDchungtu  VARCHAR := N'""" + refTypeList + """';

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
				"ID_CHUNG_TU"     INT,
				"LOAI_CHUNG_TU"   INT,
				"SortOrderMaster" INT DEFAULT NEXTVAL('TMP_ID_CHUNG_TU_seq')
				PRIMARY KEY

				)
				;

				INSERT INTO TMP_ID_CHUNG_TU
				SELECT

				Value1
				, Value2


				FROM CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(ListIDchungtu, ',', ';') F

				;

				-- Trả ra bảng master
				DROP TABLE IF EXISTS TMP_MASTER
				;

				CREATE TEMP TABLE TMP_MASTER
				AS

				SELECT
				INA."id"
				, INA."SO"
				, INA."NGAY"
				, INA."GIO"
				, INA."MUC_DICH"
				, INA."DEN_NGAY"
				, INA."KET_LUAN"
				, INA."DA_XU_LY_CHENH_LECH"

				, R."SortOrderMaster"
				FROM stock_ex_kiem_ke_bang_kiem_ke_vat_tu_hang_hoa_form INA
				INNER JOIN TMP_ID_CHUNG_TU R ON R."ID_CHUNG_TU" = INA."id"

				ORDER BY R."SortOrderMaster"
				;


				---------------
				DROP TABLE IF EXISTS TMP_THANH_VIEN_THAM_GIA
				;

				CREATE TEMP TABLE TMP_THANH_VIEN_THAM_GIA
				AS


				SELECT
				R."ID_CHUNG_TU"
				, INAM."HO_VA_TEN"
				, INAM."CHUC_DANH"
				, INAM."DAI_DIEN"
				, R."SortOrderMaster"
				, COALESCE(INAM."sequence", 1) AS "STT"
				FROM TMP_ID_CHUNG_TU R
				LEFT JOIN stock_ex_bang_kiem_ke_vthh_tv_tham_gia_chi_tiet_form INAM
				ON R."ID_CHUNG_TU" = INAM."BANG_KIEM_KE_VTHH_ID"
				UNION ALL
				SELECT
				R."ID_CHUNG_TU"
				, INAM."HO_VA_TEN"
				, INAM."CHUC_DANH"
				, INAM."DAI_DIEN"
				, R."SortOrderMaster"
				, 2 AS "STT"
				FROM TMP_ID_CHUNG_TU R
				LEFT JOIN stock_ex_bang_kiem_ke_vthh_tv_tham_gia_chi_tiet_form INAM
				ON R."ID_CHUNG_TU" = INAM."BANG_KIEM_KE_VTHH_ID"
				WHERE INAM."BANG_KIEM_KE_VTHH_ID" IS NULL
				UNION ALL
				SELECT
				R."ID_CHUNG_TU"
				, INAM."HO_VA_TEN"
				, INAM."CHUC_DANH"
				, INAM."DAI_DIEN"
				, R."SortOrderMaster"
				, 3 AS "STT"
				FROM TMP_ID_CHUNG_TU R
				LEFT JOIN stock_ex_bang_kiem_ke_vthh_tv_tham_gia_chi_tiet_form INAM
				ON R."ID_CHUNG_TU" = INAM."BANG_KIEM_KE_VTHH_ID"
				WHERE INAM."BANG_KIEM_KE_VTHH_ID" IS NULL
				ORDER BY
				"SortOrderMaster",
				"STT"
				;

				-- Lấy ra bảng chi tiết

				DROP TABLE IF EXISTS TMP_CHI_TIET
				;

				CREATE TEMP TABLE TMP_CHI_TIET
				AS

				SELECT
				 ROW_NUMBER()
                  OVER (
                     ORDER BY
				R."SortOrderMaster",
				S."MA_KHO",
				S."TEN_KHO",
				INAD."sequence",
				INAD."id"  )  AS "RowNumber"

				,R."ID_CHUNG_TU"
				, II."TEN"  AS "TEN_HANG"
				, II."MA" AS "MA_HANG"
				, INAD."MA_KHO_ID"
				, S."MA_KHO"
				, S."TEN_KHO"
				, UNIT."DON_VI_TINH" AS "DVT"

				, INAD."SO_LUONG_SO_KE_TOAN"
				, --Số lượng trên số kế toán
				INAD."GIA_TRI_SO_KE_TOAN"
				, --Thành tiền trên số kế toán
				INAD."SO_LUONG_KIEM_KE"
				, --Số lượng kiểm kê
				INAD."GIA_TRI_KIEM_KE"
				, --Thành tiền kiểm kê
				INAD."SO_LUONG_CHENH_LECH"
				, --Số lượng chênh lệch
				INAD."GIA_TRI_CHENH_LECH"
				, --Số tiền chênh lệch
				INAD."PHAM_CHAT_CON_TOT"
				, --Số lượng còn tốt
				INAD."KEM_PHAM_CHAT"
				, --Số lương kém phẩm chất
				INAD."MAT_PHAM_CHAT"
				, R."SortOrderMaster"
				, INAD."sequence" AS "SortOrder"
				, SUM(INAD."SO_LUONG_SO_KE_TOAN")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_SL_SO_KE_TOAN"
				, SUM(INAD."GIA_TRI_SO_KE_TOAN")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_GIA_TRI_SO_KE_TOAN"
				, SUM(INAD."SO_LUONG_KIEM_KE")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_SL_KIEM_KE"
				, SUM(INAD."GIA_TRI_KIEM_KE")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_GIA_TRI_KIEM_KE"
				, SUM(INAD."SO_LUONG_CHENH_LECH")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_SL_CHENH_LECH"
				, SUM(INAD."GIA_TRI_CHENH_LECH")
				OVER (
				PARTITION BY INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID",
				INAD."MA_KHO_ID" )         AS "TONG_GIA_TRI_CHENH_LECH"
				FROM TMP_ID_CHUNG_TU R
				LEFT JOIN stock_ex_bang_kiem_ke_vthh_can_dieu_chinh_chi_tiet_form INAD --nvtoan modify 07/11/2016
				ON R."ID_CHUNG_TU" = INAD."KIEM_KE_BANG_KIEM_KE_VTHH_ID"
				LEFT JOIN danh_muc_vat_tu_hang_hoa II ON INAD."MA_HANG_ID" = II."id"
				--nvtoan modify 07/11/2016
				LEFT JOIN danh_muc_don_vi_tinh AS UNIT ON INAD."DVT_ID" = UNIT."id"
				LEFT JOIN danh_muc_kho S ON S."id" = INAD."MA_KHO_ID"
				ORDER BY
				R."SortOrderMaster",
				S."MA_KHO",
				S."TEN_KHO",
				INAD."sequence",
				INAD."id"
				;


				END $$

				;

				SELECT *
				FROM TMP_CHI_TIET
				ORDER BY
				"RowNumber"

				;
				"""
		return self.execute(query)