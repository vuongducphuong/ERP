# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round
from datetime import timedelta, datetime

class BAO_CAO_DON_DAT_HANG_CTBH(models.Model):
	_name = 'bao.cao.don.dat.hang.tu.ctbh'
	_auto = False

	ref = fields.Char(string='Reffence ID')

	ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
	MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')

	TEN_KHACH_HANG = fields.Char(string='Tên khách hàng') #AccountObjectName
	MA_KHACH_HANG = fields.Char(string='Tên ngân hàng')#AccountObjectCode
	DIA_CHI = fields.Char(string='Địa chỉ') #AccountObjectAddress
	MA_SO_THUE = fields.Char(string='Địa chỉ') #AccountObjectTaxCode
	MA_NHAN_VIEN = fields.Char(string='Địa chỉ') #EmployeeCode
	TEN_NHAN_VIEN_BAN_HANG = fields.Char(string='Địa chỉ') #EmployeeName
	NGAY_DON_HANG = fields.Char(string='Địa chỉ') #RefDate
	DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải') #JournalMemo
	SO_DON_HANG = fields.Char(string='Diễn giải', help='Diễn giải') #RefNo
	LOAI_TIEN = fields.Char(string='Loại tiền') #CurrencyID
	TY_GIA = fields.Monetary(string='Tỷ giá', currency_field='currency_id') #ExchangeRate
	TONG_TIEN_QUY_DOI = fields.Float(string='Tổng tiền quy đổi',digits=decimal_precision.get_precision('VND')) #TotalAmount
	NGAY_GIAO_HANG = fields.Date(string='Ngày chứng từ') #DeliveryDate
	DIA_DIEM_GIAO_HANG = fields.Char(string='Loại tiền') #ShippingAddress
	DIEU_KHOAN_KHAC = fields.Char(string='Loại tiền') #OtherTerm
	TEN_DIEU_KHOAN = fields.Char(string='Loại tiền') #PaymentTermName
	SO_DIEN_THOAI = fields.Char(string='Loại tiền') #Tel
	FAX = fields.Char(string='Loại tiền') #Fax

	SO_TIEN_CHIET_KHAU = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalDiscount
	TONG_THANH_TIEN = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalAmount
	THUE_SUAT_GTGT = fields.Float(string='Số tiền chiết khấu',digits=decimal_precision.get_precision('VND')) #dVATRate
	TIEN_THUE_GTGT = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalVAT
	CONG_TIEN_HANG = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalAmount - dTotalDiscount

	TY_LE_CHIET_KHAU = fields.Float(string='Tỷ lệ chiết khấu') #dTotalDiscount / dTotalAmount

	TONG_TIEN_THANH_TOAN = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalAmount+dTotalVAT-dTotalDiscount
	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())


	
	
	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())

	ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.don.dat.hang.tu.ctbh.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')



class BAO_CAO_DON_DAT_HANG_CTBH_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_saordervoucherctbh'

	@api.model
	def get_report_values(self, docids, data=None):
		############### START SQL lấy dữ liệu ###############
		new_data = []
		for id in docids:
			sale_document = self.env['sale.document'].browse(id)
			for don_dat_hang in sale_document.LAP_TU_DON_DAT_HANG_IDS:
				new_data += ['account.ex.don.dat.hang,'+ str(don_dat_hang.id)]
		data['ids'] = new_data
		##########################
		refTypeList, records = self.get_reftype_list(data)
		sql_result = self.ham_lay_du_lieu_sql_tra_ve(refTypeList)

		for line in sql_result:
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
			master_data = self.env['bao.cao.don.dat.hang.tu.ctbh'].convert_for_update(line)
			detail_data = self.env['bao.cao.don.dat.hang.tu.ctbh.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
				records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.don.dat.hang.tu.ctbh.chi.tiet'].new(detail_data)
		
		docs = [records.get(k) for k in records]

		for record in docs:
			if not record.LOAI_TIEN:
				record.currency_id = self.lay_loai_tien_mac_dinh()
			else:
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', record.LOAI_TIEN)],limit=1)
				if loai_tien_id:
					record.currency_id = loai_tien_id.id

			if record.NGAY_DON_HANG:
				record.NGAY_DON_HANG = 	datetime.strptime(record.NGAY_DON_HANG,'%Y-%m-%d').date().strftime('%d/%m/%Y')

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
			record.TONG_TIEN_THANH_TOAN = record.TONG_THANH_TIEN + record.TIEN_THUE_GTGT - record.SO_TIEN_CHIET_KHAU
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
                SD."sequence" ,
                SD."id"  )  AS "RowNumber"
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
                , I."MA" AS "MA_HANG"
                , CASE WHEN SD."LA_HANG_KHUYEN_MAI" = TRUE
                THEN SD."TEN_HANG" || N' (Hàng khuyến mại không thu tiền)'
                  ELSE SD."TEN_HANG" END                                                                       AS "DIEN_GIAI_DETAIL"
                , U."DON_VI_TINH"
                , SD."SO_LUONG"
                , SD."DON_GIA"
                , SD."THANH_TIEN"
                , CASE WHEN ( select "PHAN_TRAM_THUE_GTGT" from danh_muc_thue_suat_gia_tri_gia_tang T WHERE T.id = SD."PHAN_TRAM_THUE_GTGT_ID") > 0
                THEN ( select "PHAN_TRAM_THUE_GTGT" from danh_muc_thue_suat_gia_tri_gia_tang T WHERE T.id = SD."PHAN_TRAM_THUE_GTGT_ID") * 0.01
                  ELSE ( select "PHAN_TRAM_THUE_GTGT" from danh_muc_thue_suat_gia_tri_gia_tang T WHERE T.id = SD."PHAN_TRAM_THUE_GTGT_ID")
                  END                                                                                          AS "THUE_SUAT"
                , SD."TIEN_THUE_GTGT"
                , SD."PHAN_TRAM_CHIET_KHAU" *
                  0.01                                                                                         AS "TY_LE_CHIET_KHAU"
                , SD."TIEN_CHIET_KHAU"
               , SD."sequence"
                ,
                  F."STT"
                , SD."LA_HANG_KHUYEN_MAI"
                  , SD."id"

            FROM account_ex_don_dat_hang S
                INNER JOIN account_ex_don_dat_hang_chi_tiet SD ON S."id" = SD."DON_DAT_HANG_CHI_TIET_ID"
                INNER JOIN TMP_PARAM F ON F."ID_CHUNG_TU" = S."id"
                LEFT JOIN res_partner A ON S."KHACH_HANG_ID" = A."id"
                LEFT JOIN res_partner E ON S."NV_BAN_HANG_ID" = E."id"
                INNER JOIN danh_muc_vat_tu_hang_hoa I ON SD."MA_HANG_ID" = I."id"
                LEFT JOIN danh_muc_don_vi_tinh U ON SD."DVT_ID" = U."id"
                LEFT JOIN danh_muc_dieu_khoan_thanh_toan AS PT ON S."DIEU_KHOAN_TT_ID" = PT."id"

                LEFT JOIN danh_muc_don_vi_tinh AS UM ON SD."DVT_ID" = UM."id"

             ORDER BY
                F."STT",
                SD."sequence" ,
                SD."id"

            ;



END $$

;

SELECT  * FROM TMP_DON_DAT_HANG

 ORDER BY
     "RowNumber"
		"""
		return self.execute(query)

	@api.model_cr
	def init(self):
		self.env.cr.execute(""" 
		DROP FUNCTION IF EXISTS LAY_TAI_KHOAN_TONG_HOP_CHUNG_CHUYEN_TIEN_NOI_BO( IN ID_CHUNG_TU INT, TK_CO VARCHAR(255) ) --Func_GetParentAccountOfBAInternalTransferDetail
		;

		CREATE OR REPLACE FUNCTION LAY_TAI_KHOAN_TONG_HOP_CHUNG_CHUYEN_TIEN_NOI_BO(IN ID_CHUNG_TU INT,
																									 TK_CO       VARCHAR(255))
			RETURNS VARCHAR
		AS $$
		DECLARE
			TAI_KHOAN           VARCHAR(255);

			TONG_TAI_KHOAN      INT;

			TAI_KHOAN_PHAN_TRAM VARCHAR(255);

			TK_CO_PHAN_TRAM     VARCHAR(255);


		BEGIN
			-- Lấy về tài khoản "TK_CO"


			TK_CO_PHAN_TRAM = TK_CO || '%%'
			;

			-- Lấy "TK_CO" nhỏ nhất
			TAI_KHOAN = (SELECT (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = CAD."TK_CO_ID")
						 FROM account_ex_phieu_thu_chi_tiet CAD
							 INNER JOIN danh_muc_he_thong_tai_khoan ACC ON (SELECT "SO_TAI_KHOAN"
																			FROM danh_muc_he_thong_tai_khoan TK
																			WHERE TK.id = CAD."TK_CO_ID") = ACC."SO_TAI_KHOAN"
						 WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																 FROM danh_muc_he_thong_tai_khoan TK
																 WHERE TK.id = CAD."TK_CO_ID") LIKE TK_CO_PHAN_TRAM
						 ORDER BY
							 ACC."BAC",
							 (SELECT "SO_TAI_KHOAN"
							  FROM danh_muc_he_thong_tai_khoan TK
							  WHERE TK.id = CAD."TK_CO_ID")
						 LIMIT 1)
			;


			TONG_TAI_KHOAN = (SELECT COUNT(*)
							  FROM account_ex_phieu_thu_chi_tiet CAD
							  WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																	  FROM danh_muc_he_thong_tai_khoan TK
																	  WHERE TK.id = CAD."TK_CO_ID") LIKE TK_CO_PHAN_TRAM
			)
			;


			TAI_KHOAN_PHAN_TRAM = TAI_KHOAN || '%%'
			;

			-- Trường hợp Count theo "TK_CO"%% nhỏ nhất không bằng tổng số "TK_CO" thì lấy Parent của "TK_CO" nhỏ nhất
			IF TONG_TAI_KHOAN <> (SELECT COUNT(*)
								  FROM account_ex_phieu_thu_chi_tiet CAD
								  WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																		  FROM danh_muc_he_thong_tai_khoan TK
																		  WHERE TK.id = CAD."TK_CO_ID") LIKE
																		 TAI_KHOAN_PHAN_TRAM)
			THEN
				TAI_KHOAN = (SELECT "SO_TAI_KHOAN"
							 FROM danh_muc_he_thong_tai_khoan
							 WHERE "id" = (SELECT "parent_id"
										   FROM danh_muc_he_thong_tai_khoan
										   WHERE "SO_TAI_KHOAN" = TAI_KHOAN))
				;
			END IF
			;

			IF TAI_KHOAN IS NULL OR TAI_KHOAN = ''
			THEN
				TAI_KHOAN = TK_CO
				;
			END IF
			;

			RETURN TAI_KHOAN
			;
		END
		;
		$$ LANGUAGE PLpgSQL
		;

		""")


		self.env.cr.execute(""" 
		DROP FUNCTION IF EXISTS LAY_TAI_KHOAN_TONG_HOP_CHUNG_TREN_SEC_UY_NHIEM_CHI_MUA_DICH_VU_CHI_TIET( IN ID_CHUNG_TU INT, TK_CO VARCHAR(255) ) --Func_GetParentAccountOfPUServiceDetail
		;

		CREATE OR REPLACE FUNCTION LAY_TAI_KHOAN_TONG_HOP_CHUNG_TREN_SEC_UY_NHIEM_CHI_MUA_DICH_VU_CHI_TIET(IN ID_CHUNG_TU INT,
																									 TK_CO       VARCHAR(255))
			RETURNS VARCHAR
		AS $$
		DECLARE
			TAI_KHOAN           VARCHAR(255);

			TONG_TAI_KHOAN      INT;

			TAI_KHOAN_PHAN_TRAM VARCHAR(255);

			TK_CO_PHAN_TRAM     VARCHAR(255);


		BEGIN
			-- Lấy về tài khoản "TK_CO"


			TK_CO_PHAN_TRAM = TK_CO || '%%'
			;

			-- Lấy "TK_CO" nhỏ nhất
			TAI_KHOAN = (SELECT (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = CAD."TK_CO_ID")
						 FROM purchase_document_line CAD
							 INNER JOIN danh_muc_he_thong_tai_khoan ACC ON (SELECT "SO_TAI_KHOAN"
																			FROM danh_muc_he_thong_tai_khoan TK
																			WHERE TK.id = CAD."TK_CO_ID") = ACC."SO_TAI_KHOAN"
						 WHERE CAD."order_id" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																 FROM danh_muc_he_thong_tai_khoan TK
																 WHERE TK.id = CAD."TK_CO_ID") LIKE TK_CO_PHAN_TRAM
						 ORDER BY
							 ACC."BAC",
							 (SELECT "SO_TAI_KHOAN"
							  FROM danh_muc_he_thong_tai_khoan TK
							  WHERE TK.id = CAD."TK_CO_ID")
						 LIMIT 1)
			;


			TONG_TAI_KHOAN = (SELECT COUNT(*)
							  FROM purchase_document_line CAD
							  WHERE CAD."order_id" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																	  FROM danh_muc_he_thong_tai_khoan TK
																	  WHERE TK.id = CAD."TK_CO_ID") LIKE TK_CO_PHAN_TRAM
			)
			;


			TAI_KHOAN_PHAN_TRAM = TAI_KHOAN || '%%'
			;

			-- Trường hợp Count theo "TK_CO"%% nhỏ nhất không bằng tổng số "TK_CO" thì lấy Parent của "TK_CO" nhỏ nhất
			IF TONG_TAI_KHOAN <> (SELECT COUNT(*)
								  FROM purchase_document_line CAD
								  WHERE CAD."order_id" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																		  FROM danh_muc_he_thong_tai_khoan TK
																		  WHERE TK.id = CAD."TK_CO_ID") LIKE
																		 TAI_KHOAN_PHAN_TRAM)
			THEN
				TAI_KHOAN = (SELECT "SO_TAI_KHOAN"
							 FROM danh_muc_he_thong_tai_khoan
							 WHERE "id" = (SELECT "parent_id"
										   FROM danh_muc_he_thong_tai_khoan
										   WHERE "SO_TAI_KHOAN" = TAI_KHOAN))
				;
			END IF
			;

			IF TAI_KHOAN IS NULL OR TAI_KHOAN = ''
			THEN
				TAI_KHOAN = TK_CO
				;
			END IF
			;

			RETURN TAI_KHOAN
			;

		END
		;
		$$ LANGUAGE PLpgSQL
		;
		""")

		self.env.cr.execute(""" 
				DROP FUNCTION IF EXISTS LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_SEC_UY_NHIEM_CHI( IN ID_CHUNG_TU INT, TK_CO VARCHAR(255) ) --Func_GetParentAccountOfBAWithdrawDetail
		;

		CREATE OR REPLACE FUNCTION LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_SEC_UY_NHIEM_CHI(IN ID_CHUNG_TU INT,
																									 TK_CO       VARCHAR(255))
			RETURNS VARCHAR
		AS $$
		DECLARE
			TAI_KHOAN           VARCHAR(255);

			TONG_TAI_KHOAN      INT;

			TAI_KHOAN_PHAN_TRAM VARCHAR(255);

			TK_CO_PHAN_TRAM     VARCHAR(255);


		BEGIN
			-- Lấy về tài khoản "TK_CO"


			TK_CO_PHAN_TRAM = TK_CO || '%%'
			;

			-- Lấy "TK_CO" nhỏ nhất
			TAI_KHOAN = (SELECT (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = CAD."TK_CO_ID")
						 FROM account_ex_phieu_thu_chi_tiet CAD
							 INNER JOIN danh_muc_he_thong_tai_khoan ACC ON (SELECT "SO_TAI_KHOAN"
																			FROM danh_muc_he_thong_tai_khoan TK
																			WHERE TK.id = CAD."TK_CO_ID") = ACC."SO_TAI_KHOAN"
						 WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																 FROM danh_muc_he_thong_tai_khoan TK
																 WHERE TK.id = CAD."TK_CO_ID") LIKE TK_CO_PHAN_TRAM
						 ORDER BY
							 ACC."BAC",
							 (SELECT "SO_TAI_KHOAN"
							  FROM danh_muc_he_thong_tai_khoan TK
							  WHERE TK.id = CAD."TK_CO_ID")
						 LIMIT 1)
			;


			TONG_TAI_KHOAN = (SELECT COUNT(*)
							  FROM account_ex_phieu_thu_chi_tiet CAD
							  WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																	  FROM danh_muc_he_thong_tai_khoan TK
																	  WHERE TK.id = CAD."TK_CO_ID") LIKE TK_CO_PHAN_TRAM
			)
			;


			TAI_KHOAN_PHAN_TRAM = TAI_KHOAN || '%%'
			;

			-- Trường hợp Count theo "TK_CO"%% nhỏ nhất không bằng tổng số "TK_CO" thì lấy Parent của "TK_CO" nhỏ nhất
			IF TONG_TAI_KHOAN <> (SELECT COUNT(*)
								  FROM account_ex_phieu_thu_chi_tiet CAD
								  WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																		  FROM danh_muc_he_thong_tai_khoan TK
																		  WHERE TK.id = CAD."TK_CO_ID") LIKE
																		 TAI_KHOAN_PHAN_TRAM)
			THEN
				TAI_KHOAN = (SELECT "SO_TAI_KHOAN"
							 FROM danh_muc_he_thong_tai_khoan
							 WHERE "id" = (SELECT "parent_id"
										   FROM danh_muc_he_thong_tai_khoan
										   WHERE "SO_TAI_KHOAN" = TAI_KHOAN))
				;
			END IF
			;

			IF TAI_KHOAN IS NULL OR TAI_KHOAN = ''
			THEN
				TAI_KHOAN = TK_CO
				;
			END IF
			;

			RETURN TAI_KHOAN
			;
		END
		;
		$$ LANGUAGE PLpgSQL
		;

		""")


		self.env.cr.execute(""" 
				DROP FUNCTION IF EXISTS LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_CHUNG_TU_BAN_HANG( IN ID_CHUNG_TU INT, SO_TAI_KHOAN VARCHAR(255) ) --Func_GetParentAccountOfSAInvoiceDetail
		;

		CREATE OR REPLACE FUNCTION LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_CHUNG_TU_BAN_HANG(IN ID_CHUNG_TU INT,
																									 SO_TAI_KHOAN       VARCHAR(255))
			RETURNS VARCHAR
		AS $$
		DECLARE
			TAI_KHOAN           VARCHAR(255);

			TONG_TAI_KHOAN      INT;

			TAI_KHOAN_PHAN_TRAM VARCHAR(255);

			TK_CO_PHAN_TRAM     VARCHAR(255);


		BEGIN
			-- Lấy về tài khoản "SO_TAI_KHOAN"


			TK_CO_PHAN_TRAM = SO_TAI_KHOAN || '%%'
			;

			-- Lấy "SO_TAI_KHOAN" nhỏ nhất
			TAI_KHOAN = (SELECT (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = CAD."TK_NO_ID")
						 FROM sale_document_line CAD
							 INNER JOIN danh_muc_he_thong_tai_khoan ACC ON (SELECT "SO_TAI_KHOAN"
																			FROM danh_muc_he_thong_tai_khoan TK
																			WHERE TK.id = CAD."TK_NO_ID") = ACC."SO_TAI_KHOAN"
						 WHERE CAD."SALE_DOCUMENT_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																 FROM danh_muc_he_thong_tai_khoan TK
																 WHERE TK.id = CAD."TK_NO_ID") LIKE TK_CO_PHAN_TRAM
						 ORDER BY
							 ACC."BAC",
							 (SELECT "SO_TAI_KHOAN"
							  FROM danh_muc_he_thong_tai_khoan TK
							  WHERE TK.id = CAD."TK_NO_ID")
						 LIMIT 1)
			;


			TONG_TAI_KHOAN = (SELECT COUNT(*)
							  FROM sale_document_line CAD
							  WHERE CAD."SALE_DOCUMENT_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																	  FROM danh_muc_he_thong_tai_khoan TK
																	  WHERE TK.id = CAD."TK_NO_ID") LIKE TK_CO_PHAN_TRAM
			)
			;


			TAI_KHOAN_PHAN_TRAM = TAI_KHOAN || '%%'
			;

			-- Trường hợp Count theo "SO_TAI_KHOAN"%% nhỏ nhất không bằng tổng số "SO_TAI_KHOAN" thì lấy Parent của "SO_TAI_KHOAN" nhỏ nhất
			IF TONG_TAI_KHOAN <> (SELECT COUNT(*)
								  FROM sale_document_line CAD
								  WHERE CAD."SALE_DOCUMENT_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																		  FROM danh_muc_he_thong_tai_khoan TK
																		  WHERE TK.id = CAD."TK_NO_ID") LIKE
																		 TAI_KHOAN_PHAN_TRAM)
			THEN
				TAI_KHOAN = (SELECT "SO_TAI_KHOAN"
							 FROM danh_muc_he_thong_tai_khoan
							 WHERE "id" = (SELECT "parent_id"
										   FROM danh_muc_he_thong_tai_khoan
										   WHERE "SO_TAI_KHOAN" = TAI_KHOAN))
				;
			END IF
			;

			IF TAI_KHOAN IS NULL OR TAI_KHOAN = ''
			THEN
				TAI_KHOAN = SO_TAI_KHOAN
				;
			END IF
			;

			RETURN TAI_KHOAN
			;


		END
		;
		$$ LANGUAGE PLpgSQL
		;
		""")


		self.env.cr.execute(""" 
				DROP FUNCTION IF EXISTS LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_TRA_TIEN_GUI( IN ID_CHUNG_TU INT, SO_TAI_KHOAN VARCHAR(255) ) --Func_GetParentAccountOfBADepositDetail
		;

		CREATE OR REPLACE FUNCTION LAY_TAI_KHOAN_TONG_HOP_CHUNG_CUA_CAC_TK_TREN_TRA_TIEN_GUI(IN ID_CHUNG_TU INT,
																									 SO_TAI_KHOAN       VARCHAR(255))
			RETURNS VARCHAR
		AS $$
		DECLARE
			TAI_KHOAN           VARCHAR(255);

			TONG_TAI_KHOAN      INT;

			TAI_KHOAN_PHAN_TRAM VARCHAR(255);

			TK_CO_PHAN_TRAM     VARCHAR(255);


		BEGIN
			-- Lấy về tài khoản "SO_TAI_KHOAN"


			TK_CO_PHAN_TRAM = SO_TAI_KHOAN || '%%'
			;

			-- Lấy "SO_TAI_KHOAN" nhỏ nhất
			TAI_KHOAN = (SELECT (SELECT "SO_TAI_KHOAN"
								 FROM danh_muc_he_thong_tai_khoan TK
								 WHERE TK.id = CAD."TK_NO_ID")
						 FROM account_ex_phieu_thu_chi_tiet CAD
							 INNER JOIN danh_muc_he_thong_tai_khoan ACC ON (SELECT "SO_TAI_KHOAN"
																			FROM danh_muc_he_thong_tai_khoan TK
																			WHERE TK.id = CAD."TK_NO_ID") = ACC."SO_TAI_KHOAN"
						 WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																 FROM danh_muc_he_thong_tai_khoan TK
																 WHERE TK.id = CAD."TK_NO_ID") LIKE TK_CO_PHAN_TRAM
						 ORDER BY
							 ACC."BAC",
							 (SELECT "SO_TAI_KHOAN"
							  FROM danh_muc_he_thong_tai_khoan TK
							  WHERE TK.id = CAD."TK_NO_ID")
						 LIMIT 1)
			;


			TONG_TAI_KHOAN = (SELECT COUNT(*)
							  FROM account_ex_phieu_thu_chi_tiet CAD
							  WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																	  FROM danh_muc_he_thong_tai_khoan TK
																	  WHERE TK.id = CAD."TK_NO_ID") LIKE TK_CO_PHAN_TRAM
			)
			;


			TAI_KHOAN_PHAN_TRAM = TAI_KHOAN || '%%'
			;

			-- Trường hợp Count theo "SO_TAI_KHOAN"%% nhỏ nhất không bằng tổng số "SO_TAI_KHOAN" thì lấy Parent của "SO_TAI_KHOAN" nhỏ nhất
			IF TONG_TAI_KHOAN <> (SELECT COUNT(*)
								  FROM account_ex_phieu_thu_chi_tiet CAD
								  WHERE CAD."PHIEU_THU_CHI_ID" = ID_CHUNG_TU AND (SELECT "SO_TAI_KHOAN"
																		  FROM danh_muc_he_thong_tai_khoan TK
																		  WHERE TK.id = CAD."TK_NO_ID") LIKE
																		 TAI_KHOAN_PHAN_TRAM)
			THEN
				TAI_KHOAN = (SELECT "SO_TAI_KHOAN"
							 FROM danh_muc_he_thong_tai_khoan
							 WHERE "id" = (SELECT "parent_id"
										   FROM danh_muc_he_thong_tai_khoan
										   WHERE "SO_TAI_KHOAN" = TAI_KHOAN))
				;
			END IF
			;

			IF TAI_KHOAN IS NULL OR TAI_KHOAN = ''
			THEN
				TAI_KHOAN = SO_TAI_KHOAN
				;
			END IF
			;

			RETURN TAI_KHOAN
			;


		END
		;
		$$ LANGUAGE PLpgSQL
		;
		""")

