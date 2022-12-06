# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round

class BAO_CAO_PHIEU_XUAT_KHO_BAN_HANG(models.Model):
	_name = 'bao.cao.phieu.xuat.kho.ban.hang'
	_auto = False

	ref = fields.Char(string='Reffence ID')

	ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
	MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')
	LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ') #Reftype
	TEN_KHACH_HANG = fields.Char(string='Tên khách hàng') #AccountObjectName
	DIA_CHI = fields.Char(string='Địa chỉ') #AccountObjectAddress
	MA_SO_THUE = fields.Char(string='Mã số thuế') #AccountObjectTaxCode
	NGUOI_MUA = fields.Char(string='Người mua') #Buyer
	SO_CT_GOC_KEM_THEO = fields.Integer(string='Số CT gốc kèm theo') #DocumentIncluded
	SO_DIEN_THOAI = fields.Char(string='Số điện thoại') #Tel
	TEN_NHAN_VIEN_BAN_HANG = fields.Char(string='Tên nhân viên bán hàng') #EmployeeName
	DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải') #JournalMemo
	NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán') #PostedDate
	NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ') #RefDate
	SO_CHUNG_TU = fields.Char(string='Số chứng từ') #RefNo
	LOAI_TIEN = fields.Char(string='Loại tiền') #CurrencyID
	TY_GIA = fields.Monetary(string='Tỷ giá', currency_field='currency_id') #ExchangeRate

	TONG_TIEN = fields.Monetary(string='Tổng tiền', currency_field='currency_id') #TotalAmountOC
	TONG_TIEN_QUY_DOI = fields.Float(string='Tổng tiền quy đổi',digits=decimal_precision.get_precision('VND')) #TotalAmount
	TONG_TIEN_CHIET_KHAU = fields.Monetary(string='Tổng tiền chiết khấu', currency_field='currency_id') #TotalDiscountAmountOC
	TONG_TIEN_CHIET_KHAU_QD = fields.Float(string='Tổng tiền chiết khấu quy đổi',digits=decimal_precision.get_precision('VND')) #TotalDiscountAmount
	TONG_TIEN_THUE = fields.Monetary(string='Tổng tiền thuế', currency_field='currency_id') #TotalVATAmountOC
	TONG_TIEN_THUE_QD = fields.Float(string='Tổng tiền thuế quy đổi',digits=decimal_precision.get_precision('VND')) #TotalVATAmount
	
	TINH_CHAT = fields.Char(string='Tính chất') #InventoryItemType
	TEN_DIEU_KHOAN_THANH_TOAN = fields.Char(string='Tên điều khoản thanh toán') #PaymentTermName

	TK_NO = fields.Char(string='TK Nợ', help='Tài khoản nợ') #DebitAccount
	TK_CO = fields.Char(string='TK Có', help='Tài khoản có') #CreditAccount

	TONG_THANH_TIEN = fields.Monetary(string='Tổng tiền', currency_field='currency_id')

	TONG_THANH_TIEN_LA_KHUYEN_MAI =fields.Monetary(string='Tổng tiền', currency_field='currency_id')
	TONG_TIEN_CHIET_KHAU_LA_KHUYEN_MAI = fields.Monetary(string='Tổng tiền', currency_field='currency_id')
	TONG_TIEN_THUE_GTGT_LA_KHUYEN_MAI = fields.Monetary(string='Tổng tiền', currency_field='currency_id')
	MAX_THUE_SUAT = fields.Float(string='Thành tiền quy đổi',digits=decimal_precision.get_precision('VND')) #dVATRate
	TONG_TIEN_THANH_TOAN = fields.Monetary(string='Tổng tiền', currency_field='currency_id')
	TY_LE_CHIET_KHAU = fields.Monetary(string='Thành tiền quy đổi', help='Thành tiền quy đổi', currency_field='base_currency_id')
	CONG_TIEN_HANG_DA_TRU_CHIET_KHAU = fields.Monetary(string='Tổng tiền', currency_field='currency_id')
	
	
	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
	

	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
	base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh())

	ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.phieu.xuat.kho.ban.hang.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')



class BAO_CAO_PHIEU_XUAT_KHO_BAN_HANG_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_outwardstockbysalevoucher'

	@api.model
	def get_report_values(self, docids, data=None):
		############### START SQL lấy dữ liệu ###############
		refTypeList, records = self.get_reftype_list(data)
		sql_result = self.ham_lay_du_lieu_sql_tra_ve(refTypeList)
		dic_tk_no  = {}
		dic_tk_co  = {}

		for line in sql_result:
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))

			if key not in dic_tk_no:
				dic_tk_no[key] = []
			if key not in dic_tk_co:
				dic_tk_co[key] = []

			if line.get('TK_NO') and line.get('TK_NO') not in dic_tk_no[key]:
				dic_tk_no[key] += [line.get('TK_NO')]

			if line.get('TK_CO') and line.get('TK_CO') not in dic_tk_co[key]:
				dic_tk_co[key] += [line.get('TK_CO')]
				
			master_data = self.env['bao.cao.phieu.xuat.kho.ban.hang'].convert_for_update(line)
			detail_data = self.env['bao.cao.phieu.xuat.kho.ban.hang.chi.tiet'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
				records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.phieu.xuat.kho.ban.hang.chi.tiet'].new(detail_data)
		
		for key in records:
			if key in dic_tk_no:
				records[key].TK_NO = ', '.join(dic_tk_no[key])
			if key in dic_tk_co:
				records[key].TK_CO = ', '.join(dic_tk_co[key])

		docs = [records.get(k) for k in records]

		for record in docs:
			if not record.LOAI_TIEN:
				record.currency_id = self.lay_loai_tien_mac_dinh()
				record.base_currency_id = self.lay_loai_tien_mac_dinh()
			else:
				loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', record.LOAI_TIEN)],limit=1)
				if loai_tien_id:
					record.currency_id = loai_tien_id.id
					record.base_currency_id = loai_tien_id.id

			tong_thanh_tien = 0 
			tong_thanh_tien_la_khuyen_mai = 0
			tong_tien_chiet_khau_la_khuyen_mai = 0
			tong_tien_thue_gtgt_la_khuyen_mai = 0
			thue_suat_max = 0 
			for line in record.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
				tong_thanh_tien += line.THANH_TIEN 
				line.currency_id = record.currency_id
				if line.LA_HANG_KHUYEN_MAI == 0:
					tong_thanh_tien_la_khuyen_mai += line.THANH_TIEN
					tong_tien_chiet_khau_la_khuyen_mai += line.TIEN_CHIET_KHAU
					tong_tien_thue_gtgt_la_khuyen_mai += line.TIEN_THUE_GTGT
				if line.THUE_SUAT > thue_suat_max:
					thue_suat_max = line.THUE_SUAT

			record.TONG_THANH_TIEN = tong_thanh_tien

			record.TONG_THANH_TIEN_LA_KHUYEN_MAI = tong_thanh_tien_la_khuyen_mai
			record.TONG_TIEN_CHIET_KHAU_LA_KHUYEN_MAI = tong_tien_chiet_khau_la_khuyen_mai
			record.MAX_THUE_SUAT = thue_suat_max * 100
			record.TONG_TIEN_THUE_GTGT_LA_KHUYEN_MAI = tong_tien_thue_gtgt_la_khuyen_mai

			record.TONG_TIEN_THANH_TOAN = record.TONG_THANH_TIEN_LA_KHUYEN_MAI + record.TONG_TIEN_THUE_GTGT_LA_KHUYEN_MAI - record.TONG_TIEN_CHIET_KHAU_LA_KHUYEN_MAI
			if record.TONG_THANH_TIEN_LA_KHUYEN_MAI != 0:
				record.TY_LE_CHIET_KHAU = float_round( (record.TONG_TIEN_CHIET_KHAU_LA_KHUYEN_MAI / record.TONG_THANH_TIEN_LA_KHUYEN_MAI ) * 100 , 2)
			
			record.CONG_TIEN_HANG_DA_TRU_CHIET_KHAU = record.TONG_THANH_TIEN_LA_KHUYEN_MAI - record.TONG_TIEN_CHIET_KHAU_LA_KHUYEN_MAI
			

		return {
			'docs': docs,
		}

	def ham_lay_du_lieu_sql_tra_ve(self,refTypeList):
		query = """
		DO LANGUAGE plpgsql $$
DECLARE

		ListParam                            VARCHAR := N'""" + refTypeList + """';

		rec                                  RECORD;


    CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO BOOLEAN:=False;

    CO_PHAT_SINH_BAN_HANG_SAU_THUE       BOOLEAN:=False;


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
    INTO CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO
    FROM ir_config_parameter
    WHERE key = 'he_thong.CONG_GOP_DON_GIA_DVT_MA_HANG'
    FETCH FIRST 1 ROW ONLY
    ;

    SELECT value
    INTO CO_PHAT_SINH_BAN_HANG_SAU_THUE
    FROM ir_config_parameter
    WHERE key = 'he_thong.CO_PHAT_SINH_BAN_HANG_SAU_THUE'
    FETCH FIRST 1 ROW ONLY
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA
    (
        "ID_CHUNG_TU"             INT,
        "MODEL_CHUNG_TU"          VARCHAR(255),
        "CHI_NHANH_ID"            INT,
        "LOAI_CHUNG_TU"           INT,
        "DOI_TUONG_ID"            INT,
        --Lấy thông tin KH tab đầu
        "TEN_KHACH_HANG"          VARCHAR(128),
        "DIA_CHI"                 VARCHAR(255),
        "MA_SO_THUE"              VARCHAR(127),
        --Lấy thông tin KH tab hoá đơn
        "NGUOI_MUA"               VARCHAR(128),
        "SO_CT_GOC_KEM_THEO"      VARCHAR(255),
        "SO_DIEN_THOAI"           VARCHAR(127),
        "TEN_NHAN_VIEN_BAN_HANG"  VARCHAR(128),
        "DIEN_GIAI"               VARCHAR(255),
        "NGAY_HACH_TOAN"          TIMESTAMP,
        "NGAY_CHUNG_TU"           TIMESTAMP,
        "SO_CHUNG_TU"             VARCHAR(255),
        "LOAI_TIEN"               VARCHAR(15),
        "TY_GIA"                  DECIMAL(22, 8),
        "TONG_TIEN"               DECIMAL(22, 8),
        "TONG_TIEN_QUY_DOI"       DECIMAL(22, 8),
        "TONG_TIEN_CHIET_KHAU"    DECIMAL(22, 8),
        "TONG_TIEN_CHIET_KHAU_QD" DECIMAL(22, 8),
        "TONG_TIEN_THUE"          DECIMAL(22, 8),
        "TONG_TIEN_THUE_QD"       DECIMAL(22, 8),
        "MA_HANG"                 VARCHAR(255),
        "TINH_CHAT"               VARCHAR(255),
        "DIEN_GIAI_DETAIL"        VARCHAR(255),
        "TK_NO"                   VARCHAR,
        "TK_CO"                   VARCHAR,
        "DVT"                     VARCHAR(255),
        "SO_LUONG"                DECIMAL(22, 8),

        "DON_GIA"                 DECIMAL(22, 8),

        "THANH_TIEN"              DECIMAL(22, 8),
        "THANH_TIEN_QUY_DOI"      DECIMAL(22, 8),
        "TY_LE_CHIET_KHAU"        DECIMAL(22, 8),
        "TIEN_CHIET_KHAU"         DECIMAL(22, 8),
        "TIEN_CHIET_KHAU_QUY_DOI" DECIMAL(22, 8),
        "TK_CHIET_KHAU"           VARCHAR(255),
        "THUE_SUAT"               DECIMAL(22, 8),
        "TIEN_THUE_GTGT"          DECIMAL(22, 8),
        "TIEN_THUE_GTGT_QUY_DOI"  DECIMAL(22, 8),
        "TK_THUE_GTGT"            VARCHAR(255),

        "SortOrder"               INT,
        "MinSortOrder"            INT,

        "RefIDSortOrder"          INT,
        "GIAM_GIA"                BOOLEAN,
        "LA_HANG_KHUYEN_MAI"      BOOLEAN,
           "TEN_DIEU_KHOAN_THANH_TOAN"        VARCHAR(255)


    )
    ;

    INSERT INTO TMP_KET_QUA
        SELECT
            SV."id"
            , 'sale.document'                    AS "MODEL_CHUNG_TU"
            , SV."CHI_NHANH_ID"
            , SV."LOAI_CHUNG_TU"

            , SV."DOI_TUONG_ID"

            , CASE WHEN sv."LAP_KEM_HOA_DON" = TRUE
            THEN SI."TEN_KHACH_HANG"
              ELSE SV."TEN_KHACH_HANG"
              END                                AS "TEN_KHACH_HANG"

            , CASE WHEN sv."LAP_KEM_HOA_DON" = TRUE
            THEN SI."DIA_CHI"
              ELSE SV."DIA_CHI"
              END                                AS "DIA_CHI"
            , CASE WHEN sv."LAP_KEM_HOA_DON" = TRUE
            THEN SI."MA_SO_THUE"
              ELSE CASE WHEN SV."LOAI_CHUNG_TU" IN (3530, 3532, 3534,
                                                    3536) /*Chưa thu tiền*/
                  THEN SV."MA_SO_THUE"
                   ELSE A."MA_SO_THUE"
                   END
              END                                AS "MA_SO_THUE"


            , SI."NGUOI_MUA_HANG"

            , SV."KEM_THEO_CHUNG_TU_GOC"

            , CASE WHEN sv."LAP_KEM_HOA_DON" = TRUE
            THEN CASE WHEN IA."LOAI_KHACH_HANG" = '0'
                THEN IA."DIEN_THOAI"
                 ELSE IA."DT_DI_DONG"
                 END
              ELSE CASE WHEN A."LOAI_KHACH_HANG" = '0'
                  THEN A."DIEN_THOAI"
                   ELSE A."DT_DI_DONG"
                   END
              END                                AS "SO_DIEN_THOAI"
            , E."HO_VA_TEN"
            , SV."DIEN_GIAI"
            , SV."NGAY_HACH_TOAN"
            , SV."NGAY_CHUNG_TU"
            , SV."SO_CHUNG_TU"
            , (SELECT "MA_LOAI_TIEN"
               FROM res_currency T
               WHERE T.id = SV."currency_id")    AS "LOAI_TIEN"
            , SV."TY_GIA"

            , SV."TONG_TIEN_THANH_TOAN"
            , SV."TONG_TIEN_THANH_TOAN_QĐ"
            , SV."TONG_TIEN_CHIET_KHAU"
            , SV."TONG_TIEN_CHIET_KHAU_QĐ"
            , SV."TONG_TIEN_THUE_GTGT"
            , SV."TONG_TIEN_THUE_GTGT_QĐ"

            , I."MA"
            , I."TINH_CHAT"


            , SVD."TEN_HANG"


            , TEMP."TK_NO"

            , TEMP."TK_CO"
            , U."DON_VI_TINH"
            , SUM(SVD."SO_LUONG")

            , SVD."DON_GIA"

            , SUM(SVD."THANH_TIEN")              AS "THANH_TIEN"
            , SUM(SVD."THANH_TIEN_QUY_DOI")      AS "SO_TIEN"
            , CASE WHEN CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO = TRUE
            THEN NULL
              ELSE SVD."TY_LE_CK"
              END                                AS "TY_LE_CHIET_KHAU"
            , SUM(CASE WHEN SVD."LA_HANG_KHUYEN_MAI" = TRUE
            THEN 0
                  ELSE SVD."TIEN_CHIET_KHAU"
                  END)                           AS "CHIET_KHAU_NT"
            , SUM(CASE WHEN SVD."LA_HANG_KHUYEN_MAI" = TRUE
            THEN 0
                  ELSE SVD."TIEN_CK_QUY_DOI"
                  END)                           AS "KHOAN_GIAM_GIA_THANH"
            , CASE WHEN CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO = TRUE
            THEN NULL
              ELSE (SELECT "SO_TAI_KHOAN"
                    FROM danh_muc_he_thong_tai_khoan TK
                    WHERE TK.id = SVD."TK_CHIET_KHAU_ID")
              END                                AS "TK_CHIET_KHAU"
            , MAX(CASE WHEN SVD."LA_HANG_KHUYEN_MAI" = TRUE
            THEN -1
                  WHEN ( select "PHAN_TRAM_THUE_GTGT" from danh_muc_thue_suat_gia_tri_gia_tang T WHERE T.id = SVD."THUE_GTGT_ID") > 0
                      THEN ( select "PHAN_TRAM_THUE_GTGT" from danh_muc_thue_suat_gia_tri_gia_tang T WHERE T.id = SVD."THUE_GTGT_ID") * 0.01
                  ELSE ( select "PHAN_TRAM_THUE_GTGT" from danh_muc_thue_suat_gia_tri_gia_tang T WHERE T.id = SVD."THUE_GTGT_ID")
                  END)                           AS "THUE_SUAT"
            , SUM(CASE WHEN SVD."LA_HANG_KHUYEN_MAI" = TRUE
            THEN 0
                  ELSE SVD."TIEN_THUE_GTGT"
                  END)                           AS "THUE_GTGT_NT"
            , SUM(CASE WHEN SVD."LA_HANG_KHUYEN_MAI" = TRUE
            THEN 0
                  ELSE SVD."TIEN_THUE_GTGT_QUY_DOI"
                  END)                           AS "THUE_GTGT"
            , CASE WHEN CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO = TRUE
            THEN NULL
              ELSE (SELECT "SO_TAI_KHOAN"
                    FROM danh_muc_he_thong_tai_khoan TK
                    WHERE TK.id = SVD."TK_THUE_GTGT_ID")
              END                                AS "TK_THUE_GTGT"

            , CASE WHEN CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO = TRUE
            THEN 0
              ELSE SVD."THU_TU_SAP_XEP_CHI_TIET"
              END                                AS "SortOrder"
            , MIN(SVD."THU_TU_SAP_XEP_CHI_TIET") AS "MinSortOrder"

            , F."STT"                            AS "RefIDSortOrder"
            , TRUE
            , SVD."LA_HANG_KHUYEN_MAI"
            ,PT."TEN_DIEU_KHOAN"

        FROM sale_document SV
            INNER JOIN sale_document_line SVD ON SV."id" = SVD."SALE_DOCUMENT_ID"

            LEFT JOIN res_partner AS AOD ON AOD."id" = SVD."DOI_TUONG_ID"
            INNER JOIN danh_muc_vat_tu_hang_hoa I ON SVD."MA_HANG_ID" = I."id"
            INNER JOIN TMP_PARAM F ON SV."id" = F."ID_CHUNG_TU" AND SV."LOAI_CHUNG_TU" = F."LOAI_CHUNG_TU"
            LEFT JOIN danh_muc_don_vi_tinh U ON SVD."DVT_ID" = U."id"

            LEFT JOIN sale_ex_document_invoice_rel SR ON SR.sale_document_id = SV.id AND sv."LAP_KEM_HOA_DON" = TRUE
            LEFT JOIN sale_ex_hoa_don_ban_hang SI ON SR.sale_ex_hoa_don_ban_hang_id = SI.id

            LEFT JOIN sale_ex_document_outward_detail_ref AS SORD ON SVD.id = SORD.sale_document_line_id
                                                                     AND SV."KIEM_PHIEU_NHAP_XUAT_KHO" = TRUE
            LEFT JOIN stock_ex_nhap_xuat_kho_chi_tiet AS IOD ON SORD.stock_ex_nhap_xuat_kho_chi_tiet_id = IOD.id
            LEFT JOIN danh_muc_kho AS S ON IOD."KHO_ID" = S."id"
            LEFT JOIN stock_ex_nhap_xuat_kho AS IO ON IOD."NHAP_XUAT_ID" = IO."id"

            LEFT JOIN res_partner A_IO ON A_IO."id" = IO."DOI_TUONG_ID"

            LEFT JOIN res_partner A ON SV."DOI_TUONG_ID" = A."id"
            LEFT JOIN res_partner AS IA ON SI."DOI_TUONG_ID" = IA."id"
            LEFT JOIN res_partner E ON SV."NHAN_VIEN_ID" = E."id"

            LEFT JOIN danh_muc_to_chuc AS OU ON SVD."DON_VI_ID" = OU."id"
            LEFT JOIN danh_muc_don_vi_tinh AS MU ON SVD."DVT_ID" = MU."id"
            LEFT JOIN danh_muc_dieu_khoan_thanh_toan AS PT ON SV."DIEU_KHOAN_TT_ID" = PT.id


            LEFT JOIN (SELECT
                           SVD."SALE_DOCUMENT_ID"
                           , sVD.id
                           , sVD."MA_HANG_ID"


                           , (SELECT string_agg("SO_TAI_KHOAN",N'; ' )
                              FROM (SELECT DISTINCT TK."SO_TAI_KHOAN"


                                    FROM sale_document_line SAVD
                                        LEFT JOIN danh_muc_he_thong_tai_khoan TK
                                            ON TK.id = SAVD."TK_NO_ID"

                                    WHERE SAVD."SALE_DOCUMENT_ID" = SV."id"
                                          AND (SAVD."id" = SVD."id"
                                               OR (CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO = TRUE
                                                   AND SAVD."id" IN (
                                        SELECT "id"
                                        FROM
                                            sale_document_line VD
                                        WHERE
                                            COALESCE(VD."TEN_HANG",
                                                     '') = COALESCE(SVD."TEN_HANG",
                                                                    '')
                                            AND COALESCE(CAST(VD."DVT_ID" AS VARCHAR(100)),
                                                         '') = COALESCE(CAST(SVD."DVT_ID" AS VARCHAR(100)),
                                                                        '')
                                            AND VD."DON_GIA" = SVD."DON_GIA"

                                    )
                                               )
                                          )
                                          AND SAVD."MA_HANG_ID" = SVD."MA_HANG_ID") A) AS "TK_NO"



                           , (SELECT string_agg("SO_TAI_KHOAN",N'; ')
                              FROM
                                  (SELECT DISTINCT "SO_TAI_KHOAN"

                                   FROM sale_document_line SAVD
                                       LEFT JOIN danh_muc_he_thong_tai_khoan TK
                                           ON TK.id = SAVD."TK_CO_ID"
                                   WHERE SAVD."SALE_DOCUMENT_ID" = SV."id"
                                         AND (SAVD."id" = SVD."id"
                                              OR (CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO = TRUE
                                                  AND SAVD."id" IN
                                                      (
                                                          SELECT "id"
                                                          FROM
                                                              sale_document_line VD
                                                          WHERE
                                                              COALESCE(VD."TEN_HANG", '') = COALESCE(SVD."TEN_HANG", '')
                                                              AND COALESCE(CAST(VD."DVT_ID" AS VARCHAR(100)), '') =
                                                                  COALESCE(CAST(SVD."DVT_ID" AS VARCHAR(100)), '')
                                                              AND VD."DON_GIA" = SVD."DON_GIA"

                                                      )
                                              )
                                         )
                                         AND SAVD."MA_HANG_ID" = SVD."MA_HANG_ID"
                                  ) B)                                                 AS "TK_CO"

                       FROM sale_document SV
                           INNER JOIN sale_document_line SVD ON SVD."SALE_DOCUMENT_ID" = SV."id"
                           INNER JOIN TMP_PARAM F ON SV."id" = F."ID_CHUNG_TU"
                      ) TEMP ON TEMP."SALE_DOCUMENT_ID" = SV."id"
                                AND TEMP.id = SVD."id"
                                AND TEMP."MA_HANG_ID" = SVD."MA_HANG_ID"


        GROUP BY

            SV."id"
            , "MODEL_CHUNG_TU"
            , SV."CHI_NHANH_ID"
            , SV."LOAI_CHUNG_TU"

            , SV."DOI_TUONG_ID"

            , CASE WHEN sv."LAP_KEM_HOA_DON" = TRUE
            THEN SI."TEN_KHACH_HANG"
              ELSE SV."TEN_KHACH_HANG"
              END

            , CASE WHEN sv."LAP_KEM_HOA_DON" = TRUE
            THEN SI."DIA_CHI"
              ELSE SV."DIA_CHI"
              END
            , CASE WHEN sv."LAP_KEM_HOA_DON" = TRUE
            THEN SI."MA_SO_THUE"
              ELSE CASE WHEN SV."LOAI_CHUNG_TU" IN (3530, 3532, 3534,
                                                    3536) /*Chưa thu tiền*/
                  THEN SV."MA_SO_THUE"
                   ELSE A."MA_SO_THUE"
                   END
              END


            , SI."NGUOI_MUA_HANG"

            , SV."KEM_THEO_CHUNG_TU_GOC"

            , CASE WHEN sv."LAP_KEM_HOA_DON" = TRUE
            THEN CASE WHEN IA."LOAI_KHACH_HANG" = '0'
                THEN IA."DIEN_THOAI"
                 ELSE IA."DT_DI_DONG"
                 END
              ELSE CASE WHEN A."LOAI_KHACH_HANG" = '0'
                  THEN A."DIEN_THOAI"
                   ELSE A."DT_DI_DONG"
                   END
              END
            , E."HO_VA_TEN"
            , SV."DIEN_GIAI"
            , SV."NGAY_HACH_TOAN"
            , SV."NGAY_CHUNG_TU"
            , SV."SO_CHUNG_TU"
            , SV."currency_id"
            , SV."TY_GIA"

            , SV."TONG_TIEN_THANH_TOAN"
            , SV."TONG_TIEN_THANH_TOAN_QĐ"
            , SV."TONG_TIEN_CHIET_KHAU"
            , SV."TONG_TIEN_CHIET_KHAU_QĐ"
            , SV."TONG_TIEN_THUE_GTGT"
            , SV."TONG_TIEN_THUE_GTGT_QĐ"

            , I."MA"
            , I."TINH_CHAT"


            , SVD."TEN_HANG"

            , U."DON_VI_TINH"


            , SVD."DON_GIA"


            , CASE WHEN CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO = TRUE
            THEN NULL
              ELSE SVD."TY_LE_CK"
              END

            , CASE WHEN CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO = TRUE
            THEN NULL
              ELSE (SELECT "SO_TAI_KHOAN"
                    FROM danh_muc_he_thong_tai_khoan TK
                    WHERE TK.id = SVD."TK_CHIET_KHAU_ID")
              END

            , CASE WHEN CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO = TRUE
            THEN NULL
              ELSE (SELECT "SO_TAI_KHOAN"
                    FROM danh_muc_he_thong_tai_khoan TK
                    WHERE TK.id = SVD."TK_THUE_GTGT_ID")
              END

            , CASE WHEN CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO = TRUE
            THEN 0
              ELSE SVD."THU_TU_SAP_XEP_CHI_TIET"
              END


            , F."STT"
            , TEMP."TK_NO"

            , TEMP."TK_CO"
            , SVD."LA_HANG_KHUYEN_MAI"
            ,PT."TEN_DIEU_KHOAN"

    ;

    -- ---------------------------------------------------
    UPDATE TMP_KET_QUA R
    SET "GIAM_GIA" = FALSE
    FROM
        (SELECT "ID_CHUNG_TU"
         FROM TMP_KET_QUA
         WHERE "LA_HANG_KHUYEN_MAI" = FALSE
        ) S
    WHERE R."ID_CHUNG_TU" = S."ID_CHUNG_TU"
    ;

    --
    -- --LDNGOC 10.11.2015: Lấy công nợ theo Option-----------------------------------------------------------------------------------------------------------------------------------------
    -- IF @GetOld"PHAT_SINH_NO" = 1
    -- BEGIN
    --     DECLARE @"DOI_TUONG_ID" List VARCHAR
    --     SET @"DOI_TUONG_ID" LIST = ( SELECT '|'
    --     || CAST ("DOI_TUONG_ID" AS VARCHAR (36))
    --     || ';'
    --     || CONVERT ( VARCHAR (10), "NGAY_HACH_TOAN", 20)
    --     || ';'
    --     || CAST (RefOrder AS VARCHAR (10))
    --     || ';'
    --     || CAST ("ID_CHUNG_TU" AS VARCHAR (36))
    --     FROM ( SELECT DISTINCT
    --     "DOI_TUONG_ID",
    --     "NGAY_HACH_TOAN",
    --     RefOrder,
    --     "ID_CHUNG_TU"
    --     FROM TMP_KET_QUA
    --     ) A
    --     FOR
    --     XML PATH ('')
    --     ) || '|'
    --     UPDATE R
    --     SET R.Old "PHAT_SINH_NO" = A."TONG_CONG"OLD"SO_TIEN""DEN_NGAY"
    --     FROM TMP_KET_QUA R
    --     LEFT JOIN ( SELECT *
    --     FROM Func_GetBalanceByListres_partner(@"DOI_TUONG_ID" LIST,
    --     0, %(chi_nhanh_id) S,
    --     @IsManageBook,
    --     @IsIncludeDependBranch)
    --     ) A ON R."DOI_TUONG_ID" = A."DOI_TUONG_ID"
    --     AND R."NGAY_HACH_TOAN" = A."NGAY_HACH_TOAN"
    --     AND R."ID_CHUNG_TU" = A."ID_CHUNG_TU"
    -- END
    --     -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    --
    INSERT INTO TMP_KET_QUA
    (
        "ID_CHUNG_TU",
        "MODEL_CHUNG_TU",
        "DIEN_GIAI_DETAIL",
        "NGUOI_MUA",

        "RefIDSortOrder",
        "THUE_SUAT",
        --Lấy thông tin KH tab đầu

        "TEN_KHACH_HANG",

        "DIA_CHI",
        "MA_SO_THUE",

        "SO_DIEN_THOAI",
        "TEN_NHAN_VIEN_BAN_HANG",
        "DIEN_GIAI",
        "NGAY_HACH_TOAN",
        "NGAY_CHUNG_TU",
        "SO_CHUNG_TU"

    )
        SELECT
            "ID_CHUNG_TU"
            , "MODEL_CHUNG_TU"
            , N'(Hàng khuyến mại không thu tiền)'
            , "NGUOI_MUA"

            , "RefIDSortOrder"
            , -1 -- nmtruong: nếu là hàng KM thì set "THUE_SUAT" <0 để hiển thị dấu x

            , "TEN_KHACH_HANG"

            , "DIA_CHI"
            , "MA_SO_THUE"

            , "SO_DIEN_THOAI"
            , "TEN_NHAN_VIEN_BAN_HANG"
            , "DIEN_GIAI"
            , "NGAY_HACH_TOAN"
            , "NGAY_CHUNG_TU"
            , "SO_CHUNG_TU"

        FROM TMP_KET_QUA
        WHERE "GIAM_GIA" = TRUE
        GROUP BY

            "ID_CHUNG_TU"
            , "MODEL_CHUNG_TU"

            , "NGUOI_MUA"
            , "RefIDSortOrder"


            , "TEN_KHACH_HANG"

            , "DIA_CHI"
            , "MA_SO_THUE"

            , "SO_DIEN_THOAI"
            , "TEN_NHAN_VIEN_BAN_HANG"
            , "DIEN_GIAI"
            , "NGAY_HACH_TOAN"
            , "NGAY_CHUNG_TU"
            , "SO_CHUNG_TU"
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
    ;

    CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
        AS

            SELECT
                ROW_NUMBER()
                OVER (
                    ORDER BY "RefIDSortOrder",
                        "ID_CHUNG_TU",

                        CASE WHEN CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO = TRUE
                            THEN "MinSortOrder"
                        ELSE "SortOrder"
                        END ) AS "RowNumber"
                , R.*

            FROM TMP_KET_QUA R
            ORDER BY
                "RefIDSortOrder",
                "ID_CHUNG_TU",

                CASE WHEN CONG_GOP_SO_LIEU_THEO_HANG_HOA_SO_LO = TRUE
                    THEN "MinSortOrder"
                ELSE "SortOrder"
                END
    ;

END $$

;

SELECT *
FROM TMP_KET_QUA_CUOI_CUNG --where "SO_CHUNG_TU" = 'BH00001'
ORDER BY
   "RowNumber" ;
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

