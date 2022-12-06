# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round
from datetime import timedelta, datetime

class BAO_CAO_DON_MUA_HANG(models.Model):
	_name = 'bao.cao.don.mua.hang'
	_auto = False

	ref = fields.Char(string='Reffence ID')

	ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
	MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')
	DIA_CHI = fields.Char(string='Địa chỉ') #AccountObjectAddress
	TEN_NHA_CUNG_CAP = fields.Char(string='Tên khách hàng') #AccountObjectName
	MA_SO_THUE = fields.Char(string='Địa chỉ') #CompanyTaxCode
	phone = fields.Char(string='Địa chỉ') #Phone
	FAX = fields.Char(string='Loại tiền') #Fax
	DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải') #JournalMemo
	NGAY_DON_HANG = fields.Char(string='Địa chỉ') #RefDate
	SO_DON_HANG = fields.Char(string='Diễn giải', help='Diễn giải') #RefNo
	LOAI_TIEN = fields.Char(string='Loại tiền') #CurrencyID
	TY_GIA = fields.Monetary(string='Tỷ giá', currency_field='currency_id') #ExchangeRate
	TONG_TIEN_QUY_DOI = fields.Monetary(string='Tổng tiền quy đổi', currency_field='currency_id') #TotalAmount
	TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='Tổng tiền quy đổi', currency_field='currency_id') #TotalVATAmount
	TIEN_THUE = fields.Monetary(string='Tổng tiền quy đổi', currency_field='currency_id') #TotalVATAmountOC
	TONG_TIEN = fields.Monetary(string='Tổng tiền quy đổi', currency_field='currency_id') #TotalAmountOC
	TIEN_CHIET_KHAU_QUY_DOI = fields.Monetary(string='Tổng tiền quy đổi', currency_field='currency_id') #TotalDiscountAmount
	TIEN_CHIET_KHAU = fields.Monetary(string='Tổng tiền quy đổi', currency_field='currency_id') #TotalDiscountAmountOC
	NGAY_GIAO_HANG = fields.Date(string='Ngày chứng từ') #ReceiveDate
	DIA_DIEM_GIAO_HANG = fields.Char(string='Loại tiền') #ReceiveAddress
	TEN_DIEU_KHOAN = fields.Char(string='Loại tiền') #PaymentTermName


	SO_TIEN_CHIET_KHAU = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalDiscount
	TONG_THANH_TIEN = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalAmount
	
	THUE_SUAT_GTGT = fields.Float(string='Số tiền chiết khấu',digits=decimal_precision.get_precision('VND')) #dVATRate
	TIEN_THUE_GTGT = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalVAT
	CONG_TIEN_HANG = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalAmount - dTotalDiscount

	TY_LE_CHIET_KHAU = fields.Float(string='Tỷ lệ chiết khấu') #TotalDiscountAmountOC / dTotalAmount
	SO_TIEN_QUY_DOI = fields.Float(string='Tỷ lệ chiết khấu', digits=decimal_precision.get_precision('VND')) #TotalDiscountAmountOC / dTotalAmount

	TONG_TIEN_THANH_TOAN = fields.Monetary(string='Số tiền chiết khấu', currency_field='currency_id') #dTotalAmount+dTotalVAT-dTotalDiscount



	
	
	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())

	ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.don.mua.hang.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')



class BAO_CAO_DON_MUA_HANG_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_vpurchaseorder301'

	@api.model
	def get_report_values(self, docids, data=None):
		############### START SQL lấy dữ liệu ###############
		refTypeList, records = self.get_reftype_list(data)
		sql_result = self.ham_lay_du_lieu_sql_tra_ve(refTypeList)

		for line in sql_result:
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
			master_data = self.env['bao.cao.don.mua.hang'].convert_for_update(line)
			detail_data = self.env['bao.cao.don.mua.hang.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
				records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.don.mua.hang.chi.tiet'].new(detail_data)
		
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

			tong_tien = 0
			thue_max = 0
			for line in record.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
				line.currency_id = record.currency_id
				tong_tien += line.THANH_TIEN
				if thue_max < line.PHAN_TRAM_THUE:
					thue_max =  line.PHAN_TRAM_THUE
			
			record.THUE_SUAT_GTGT = thue_max
			 
			record.TONG_THANH_TIEN = tong_tien

			if record.TONG_TIEN == 0:
				record.TY_LE_CHIET_KHAU = 0
			else:
				record.TY_LE_CHIET_KHAU  = record.TIEN_CHIET_KHAU / record.TONG_THANH_TIEN

			record.CONG_TIEN_HANG = record.TONG_TIEN - record.TIEN_CHIET_KHAU

			record.TONG_TIEN_THANH_TOAN = record.TONG_TIEN + record.TIEN_THUE - record.TIEN_CHIET_KHAU
			
			record.SO_TIEN_QUY_DOI = record.TONG_TIEN_QUY_DOI + record.TIEN_THUE_GTGT_QUY_DOI - record.TIEN_CHIET_KHAU_QUY_DOI
				
				
			

		return {
			'docs': docs,
        }

	def ham_lay_du_lieu_sql_tra_ve(self,refTypeList):
		query = """
		DO LANGUAGE plpgsql $$
		DECLARE
		
		ListParam                        VARCHAR := N'""" + refTypeList + """';

		LOAI_TIEN_CHINH INT;

    rec             RECORD;


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
            INNER JOIN danh_muc_reftype R ON F.Value2 = R."REFTYPE"
    ;

    SELECT value
    INTO LOAI_TIEN_CHINH
    FROM ir_config_parameter
    WHERE key = 'he_thong.LOAI_TIEN_CHINH'
    FETCH FIRST 1 ROW ONLY
    ;


    DROP TABLE IF EXISTS TMP_DON_MUA_HANG
    ;

    CREATE TEMP TABLE TMP_DON_MUA_HANG
        AS


            SELECT
                  ROW_NUMBER()
                  OVER (
                      ORDER BY
                          F."STT",
                          PUD."THU_TU_CAC_DONG_CHI_TIET" )    AS "RowNumber"
                , PUD."THU_TU_CAC_DONG_CHI_TIET"
                , PU."id" as "ID_CHUNG_TU"
                ,'purchase.ex.don.mua.hang' AS "MODEL_CHUNG_TU"
                , PU."DIA_CHI"
                , PU."TEN_NHA_CUNG_CAP"
                , PU."MA_SO_THUE"                             AS "MA_SO_THUE"
                , CASE WHEN AC."LOAI_KHACH_HANG" = '1'
                THEN AC."DT_DI_DONG"
                  ELSE AC."DIEN_THOAI"
                  END                                         AS Phone
                , CASE WHEN AC."LOAI_KHACH_HANG" = '1'
                THEN ''
                  ELSE AC."FAX"
                  END                                         AS "FAX"


                , PU."DIEN_GIAI"
                , PU."NGAY_DON_HANG"
                , PU."SO_DON_HANG"
                , (SELECT "MA_LOAI_TIEN"
                   FROM res_currency T
                   WHERE T.id = PU."currency_id")             AS "LOAI_TIEN"
                , II."MA"                                     AS "MA_HANG"
                , PUD."TEN_HANG"                              AS "DIEN_GIAI_DETAIL"

                , danh_muc_don_vi_tinh."DON_VI_TINH"
                , PUD."DON_GIA"
                , PUD."SO_LUONG"
                , PUD."THANH_TIEN"
                , PUD."THANH_TIEN_QUY_DOI"
                , PUD."TY_LE_CHIET_KHAU"
                , (SELECT "PHAN_TRAM_THUE_GTGT"
                   FROM danh_muc_thue_suat_gia_tri_gia_tang T
                   WHERE T.id = PUD."PHAN_TRAM_THUE_GTGT_ID") AS "PHAN_TRAM_THUE"
                , PU."TIEN_CHIET_KHAU"
                , PU."TIEN_CHIET_KHAU_QUY_DOI"
                , PU."TONG_TIEN_HANG"                   AS "TONG_TIEN"
                , PU."TIEN_THUE"
                , PU."TIEN_THUE_GTGT_QUY_DOI"
                , PU."TY_GIA"
                , PU."TONG_TIEN_HANG_QUY_DOI"   AS "TONG_TIEN_QUY_DOI"
                , PU."NGAY_GIAO_HANG"
                , PU."DIA_DIEM_GIAO_HANG"
                , danh_muc_dieu_khoan_thanh_toan."TEN_DIEU_KHOAN"


            FROM purchase_ex_don_mua_hang AS PU
                INNER JOIN TMP_PARAM F ON F."ID_CHUNG_TU" = PU."id" AND F."LOAI_CHUNG_TU" = PU."LOAI_CHUNG_TU"
                INNER JOIN purchase_ex_don_mua_hang_chi_tiet AS PUD ON PU."id" = PUD."DON_MUA_HANG_CHI_TIET_ID"
                LEFT JOIN res_partner AS AC ON AC."id" = PU."NHA_CUNG_CAP_ID"
                LEFT JOIN danh_muc_vat_tu_hang_hoa AS II ON II."id" = PUD."MA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh ON PUD."DVT_ID" = danh_muc_don_vi_tinh."id"
                LEFT JOIN danh_muc_dieu_khoan_thanh_toan ON PU."DIEU_KHOAN_TT_ID" = danh_muc_dieu_khoan_thanh_toan."id"
                LEFT JOIN res_partner AS ace ON ace."id" = pu."NV_MUA_HANG_ID"
                LEFT JOIN danh_muc_don_vi_tinh AS UM ON PUD."DVT_ID" = UM."id"

                LEFT JOIN account_ex_don_dat_hang SA ON PUD."DON_DAT_HANG_ID" = SA."id"




            ORDER BY
                F."STT",
                PUD."THU_TU_CAC_DONG_CHI_TIET"
    ;


END $$

;

SELECT *
FROM TMP_DON_MUA_HANG

ORDER BY
   "RowNumber"
;
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

