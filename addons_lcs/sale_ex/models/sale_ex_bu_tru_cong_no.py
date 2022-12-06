# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class SALE_EX_BU_TRU_CONG_NO(models.Model):
		_name = 'sale.ex.bu.tru.cong.no'
		_description = 'Bù trừ công nợ'
		_auto = False

		DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng')
		TK_PHAI_THU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK phải thu', help='Tài khoản phải thu')
		TK_PHAI_TRA_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK phải trả', help='Tài khoản phải trả')
		NGAY_BU_TRU = fields.Date(string='Ngày bù trừ', help='Ngày bù trừ',default=fields.Datetime.now)
		currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
		name = fields.Char(string='Name', help='Name', oldname='NAME')
		IS_TY_GIA = fields.Boolean(string='Loại tiền', help='Loại tiền',default=True)
		CHENH_LECH_BU_TRU_QUY_DOI = fields.Float(string='Chênh lệch bù trừ quy đổi(phải trả - phải thu)', help='Chênh lệch bù trừ quy đổi',digits=decimal_precision.get_precision('Product Price'))

		THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu', compute='doi_tru_cong_no')
		THAM_CHIEU2 = fields.Char(string='Tham chiếu', help='Tham chiếu', compute='doi_tru_chung_tu')
		TK_XU_LY_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK xử lý', help='TK xử lý')

		#FIELD_IDS = fields.One2many('model.name')
		@api.model
		def default_get(self, fields_list):
			result = super(SALE_EX_BU_TRU_CONG_NO, self).default_get(fields_list)
			# doi_tuong_ids = self.env['res.partner'].search(['|',('LA_NHA_CUNG_CAP','=','True'),('LA_KHACH_HANG','=','True')])
			tk_phai_thu = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','131')],limit=1)
			tk_phai_tra = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','331')],limit=1)
			loai_tien = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')],limit=1)
			if tk_phai_thu:
				result['TK_PHAI_THU_ID'] = tk_phai_thu.id
			if tk_phai_tra:
				result['TK_PHAI_TRA_ID'] = tk_phai_tra.id
			if loai_tien:
				result['currency_id'] = loai_tien.id
			# if doi_tuong_ids:
			# 	result['DOI_TUONG_ID'] = doi_tuong_ids
			return result
		SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS = fields.One2many('sale.ex.bu.tru.cong.no.chung.tu.phai.tra', 'BU_TRU_CONG_NO_ID', string='Bù trừ công nợ chứng từ phải trả')
		SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS = fields.One2many('sale.ex.bu.tru.cong.no.chung.tu.phai.thu', 'BU_TRU_CONG_NO_ID', string='Bù trừ công nợ chứng từ phải thu')


		def btn_bu_tru(self):
			return {}

		def lay_tai_khoan_xu_ly(self, args):
			tai_khoan_xu_ly_lai = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like', '515%')],limit=1)
			tai_khoan_xu_ly_lo = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like', '635%')],limit=1)
			ma_tai_khoan_lai = ''
			tai_khoan_lai_id = False
			ma_tai_khoan_lo = ''
			tai_khoan_lo_id = False
			if tai_khoan_xu_ly_lai:
				ma_tai_khoan_lai = tai_khoan_xu_ly_lai.SO_TAI_KHOAN
				tai_khoan_lai_id = tai_khoan_xu_ly_lai.id
			if tai_khoan_xu_ly_lo:
				ma_tai_khoan_lo = tai_khoan_xu_ly_lo.SO_TAI_KHOAN
				tai_khoan_lo_id = tai_khoan_xu_ly_lo.id
			dict_ket_qua = {'tai_khoan_xu_ly_lai' : [tai_khoan_lai_id,ma_tai_khoan_lai],
							'tai_khoan_xu_ly_lo' : [tai_khoan_lo_id,ma_tai_khoan_lo],
						}
			return dict_ket_qua

		@api.onchange('currency_id')
		def update_loai_tien(self):
				if self.currency_id.MA_LOAI_TIEN == 'VND':
						self.IS_TY_GIA = False
				else:
						self.IS_TY_GIA =True
		# tungdztodo:laydulieu
		def lay_du_lieu_doi_tru(self, args):
			new_line_chung_tu_phai_thu = [[5]]
			new_line_chung_tu_phai_tra = [[5]]
			if args.get('doi_tuong_id'):
				chung_tu_phai_thu = self.chung_tu_phai_thu(args.get('ngay_bu_tru'),args.get('doi_tuong_id'),args.get('currency_id'))
				ct_phai_tra = self.chung_tu_phai_tra(args.get('ngay_bu_tru'),args.get('doi_tuong_id'),args.get('currency_id'))
				# env = self.env['sale.ex.bu.tru.cong.no.chung.tu.phai.tra']
				# env1 = self.env['sale.ex.bu.tru.cong.no.chung.tu.phai.thu']
				# self.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS = []
				# self.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS = []

				if chung_tu_phai_thu:
					for ct in chung_tu_phai_thu:
						ten_loai_chung_tu = self.env['danh.muc.reftype'].search([('REFTYPE', '=', ct.get('LOAI_CHUNG_TU'))], limit=1)
						new_line_chung_tu_phai_thu += [(0,0,{
								'NGAY_CHUNG_TU': ct.get('NGAY_CHUNG_TU'),
								'SO_CHUNG_TU' : ct.get('SO_CHUNG_TU'),
								'SO_HOA_DON' : ct.get('SO_HOA_DON'),
								'HAN_THANH_TOAN' : ct.get('HAN_THANH_TOAN'),
								'DIEN_GIAI' : ct.get('DIEN_GIAI'),
								'SO_TIEN' : ct.get('SO_TIEN'),
								'SO_TIEN_QUY_DOI' : ct.get('SO_TIEN_QUY_DOI'),
								'SO_CHUA_THU' : ct.get('SO_TIEN_THANH_TOAN'),
								'SO_CHUA_THU_QUY_DOI' : ct.get('SO_TIEN_THANH_QUY_DOI'),
								'TY_GIA_DANH_GIA_LAI' : ct.get('TY_GIA_DANH_GIA_LAI'),
								'TY_GIA' : ct.get('TY_GIA'),
								'TEN_LOAI_CHUNG_TU' : ten_loai_chung_tu.REFTYPENAME if ten_loai_chung_tu else '',
								'ID_GOC' : ct.get('ID_CHUNG_TU'),
								'MODEL_GOC' : ct.get('MODEL_CHUNG_TU'),
								'LOAI_CHUNG_TU' : ct.get('LOAI_CHUNG_TU'),
								'NGAY_HOA_DON' : ct.get('NGAY_HOA_DON'),
						})]
						# self.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS += new_line
				if ct_phai_tra:
					for line in ct_phai_tra:
						ten_loai_ct_phai_thu = ''
						loai_ct_phai_thu = self.env['danh.muc.reftype'].search([('REFTYPE', '=', line.get('LOAI_CHUNG_TU'))], limit=1)
						if loai_ct_phai_thu:
							ten_loai_ct_phai_thu = loai_ct_phai_thu.REFTYPENAME
						new_line_chung_tu_phai_tra += [(0,0,{
								'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU'),
								'SO_CHUNG_TU' : line.get('SO_CHUNG_TU'),
								'SO_HOA_DON' : line.get('SO_HOA_DON'),
								'HAN_THANH_TOAN' : line.get('NGAY_HET_HAN'),
								'DIEN_GIAI' : line.get('DIEN_GIAI'),
								'SO_TIEN' : line.get('SO_TIEN'),
								'SO_TIEN_QUY_DOI' : line.get('SO_TIEN_QUY_DOI'),
								'SO_CON_NO' : line.get('SO_TIEN_PHAI_TRA'),
								'SO_CON_NO_QUY_DOI' : line.get('SO_TIEN_PHAI_TRA_QUY_DOI'),
								'SO_TIEN_BU_TRU' : line.get('SO_TIEN_BU_TRU_QUY_DOI'),
								'TEN_LOAI_CHUNG_TU' : ten_loai_ct_phai_thu,
								'TY_GIA_DANH_GIA_LAI' : line.get('TY_GIA_DANH_GIA_LAI'),
								'TY_GIA' : line.get('TY_GIA'),
								'ID_GOC' : line.get('ID_CHUNG_TU'),
								'MODEL_GOC' : line.get('MODEL_CHUNG_TU'),
								'LOAI_CHUNG_TU' : line.get('LOAI_CHUNG_TU'),
								'NGAY_HOA_DON' : line.get('NGAY_HOA_DON'),
							})]
							# self.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS += new_line1
			return {'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS' : new_line_chung_tu_phai_thu,
					'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS' : new_line_chung_tu_phai_tra,
			}


		def chung_tu_phai_tra(self,ngay,doi_tuong,loai_tien):
			params = {
					'DEN_NGAY': ngay,
					'DOI_TUONG_ID' : doi_tuong,
					'currency_id' : loai_tien,
					'CHI_NHANH_ID' : self.get_chi_nhanh()
					}

			query = """   

				DO LANGUAGE plpgsql $$ DECLARE

				doi_tuong_id INTEGER := %(DOI_TUONG_ID)s;
				chi_nhanh_id INTEGER := %(CHI_NHANH_ID)s;
				den_ngay     DATE := %(DEN_NGAY)s;
				loai_tien_id INTEGER := %(currency_id)s;



				BEGIN

				DROP TABLE IF EXISTS TMP_TABLE1;
				CREATE TEMP TABLE TMP_TABLE1
					AS
					SELECT
						OPN.id                                AS "ID_CHUNG_TU",
						OPN."LOAI_CHUNG_TU"
						--					,RT."REFTYPENAME" AS "TEN_LOAI_CHUNG_TU"
						,
						(CASE
						WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
						THEN OPI."NGAY_HOA_DON"
						ELSE OPN."NGAY_HACH_TOAN"
						END)                                 AS "NGAY_CHUNG_TU",
						OPN."NGAY_HACH_TOAN",
						'OPN'                                 AS "SO_CHUNG_TU",
						OPI."NGAY_HOA_DON",
						coalesce(OPI."SO_HOA_DON", '')        AS "SO_HOA_DON",
						''                                    AS "DIEN_GIAI",
						(CASE
						WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
						THEN coalesce(OPI."TY_GIA", 1)
						ELSE coalesce(OPN."TY_GIA", 1)
						END)                                 AS "TY_GIA",
						SUM(CASE
							WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
							THEN coalesce(OPI."GIA_TRI_HOA_DON_NGUYEN_TE", 0)
							ELSE coalesce(OPN."DU_CO_NGUYEN_TE", 0) - coalesce(OPN."DU_NO_NGUYEN_TE", 0)
							END)                              AS "TONG_TIEN",
						SUM(CASE
							WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
							THEN coalesce(OPI."GIA_TRI_HOA_DON", 0)
							ELSE coalesce(OPN."DU_CO", 0) - coalesce(OPN."DU_NO", 0)
							END)                              AS "TONG_TIEN_QUY_DOI",
						SUM(CASE
							WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
							THEN OPI."SO_CON_PHAI_THU_NGUYEN_TE" - OPI."SO_THU_TRUOC_NGUYEN_TE"
							ELSE coalesce(OPN."DU_CO_NGUYEN_TE", 0) - coalesce(OPN."DU_NO_NGUYEN_TE", 0)
							END)                              AS "SO_TIEN",
						SUM(CASE
							WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
							THEN OPI."SO_CON_PHAI_THU" - OPI."SO_THU_TRUOC"
							ELSE coalesce(OPN."DU_CO", 0) - coalesce(OPN."DU_NO", 0)
							END)                              AS "SO_TIEN_QUY_DOI",
						1                                     AS "SO_HOA_DON_CHI_TIET",
						OPID."HAN_THANH_TOAN",
						OPID2."NHAN_VIEN_ID",
						'account.ex.so.du.tai.khoan.chi.tiet' AS "MODEL_CHUNG_TU"

					FROM account_ex_so_du_tai_khoan_chi_tiet OPN
						INNER JOIN danh_muc_reftype RT ON cast(RT."REFTYPE" AS VARCHAR(50)) = OPN."LOAI_CHUNG_TU"
						LEFT JOIN account_ex_sdtkct_theo_hoa_don OPI
						ON OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" = OPN.id
						LEFT JOIN (SELECT
									OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID",
									coalesce(OAEDI."NGAY_HOA_DON", den_ngay)                     AS "NGAY_HOA_DON",
									coalesce(OAEDI."SO_HOA_DON", '')                             AS "SO_HOA_DON",
									coalesce(OAEDI."TY_GIA", 0)                                  AS "TY_GIA",
									OAEDI."NHAN_VIEN_ID",
									ROW_NUMBER()
									OVER (
									PARTITION BY OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID", coalesce(OAEDI."NGAY_HOA_DON",
																								den_ngay), coalesce(
										OAEDI."SO_HOA_DON", ''), coalesce(OAEDI."TY_GIA", 0) ) AS RowNumber
								FROM account_ex_sdtkct_theo_hoa_don AS OAEDI
								WHERE OAEDI."NHAN_VIEN_ID" IS NOT NULL) AS OPID2
						ON OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" = OPID2."SO_DU_TAI_KHOAN_CHI_TIET_ID"
							AND OPID2.RowNumber = 1
							AND coalesce(OPI."SO_HOA_DON", '') = coalesce(OPID2."SO_HOA_DON", '')
							AND coalesce(OPI."NGAY_HOA_DON", den_ngay) = coalesce(OPID2."NGAY_HOA_DON", den_ngay)
							AND coalesce(OPI."TY_GIA", 0) = coalesce(OPID2."TY_GIA", 0)
						LEFT JOIN (SELECT
									OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID",
									coalesce(OAEDI."NGAY_HOA_DON", den_ngay)                     AS "NGAY_HOA_DON",
									coalesce(OAEDI."SO_HOA_DON", '')                             AS "SO_HOA_DON",
									OAEDI."HAN_THANH_TOAN",
									coalesce(OAEDI."TY_GIA", 0)                                  AS "TY_GIA",
									ROW_NUMBER()
									OVER (
									PARTITION BY OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID", coalesce(OAEDI."NGAY_HOA_DON",
																								den_ngay), coalesce(
										OAEDI."SO_HOA_DON", ''), coalesce(OAEDI."TY_GIA", 0) ) AS RowNumber
								FROM account_ex_sdtkct_theo_hoa_don AS OAEDI
								WHERE OAEDI."HAN_THANH_TOAN" IS NOT NULL) AS OPID ON OPN.id = OPID."SO_DU_TAI_KHOAN_CHI_TIET_ID"
																						AND OPID.RowNumber = 1
																						AND coalesce(OPI."SO_HOA_DON", '') =
																							coalesce(OPID."SO_HOA_DON", '')
																						AND
																						coalesce(OPI."NGAY_HOA_DON", den_ngay)
																						=
																						coalesce(OPID."NGAY_HOA_DON", den_ngay)
																						AND coalesce(OPI."TY_GIA", 0) =
																							coalesce(OPID."TY_GIA", 0)
					WHERE (OPN."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id ISNULL)
							AND OPN."currency_id" = loai_tien_id
							AND OPN."TK_ID" = (SELECT id
											FROM danh_muc_he_thong_tai_khoan
											WHERE "SO_TAI_KHOAN" = '331')
							AND OPN."CHI_NHANH_ID" = chi_nhanh_id
							AND OPN."NGAY_HACH_TOAN" <= den_ngay

					GROUP BY OPN.id
						, OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID"
						, OPN."LOAI_CHUNG_TU"
						--					,RT."REFTYPENAME"
						, OPN."NGAY_HACH_TOAN"
						, OPI."NGAY_HOA_DON"
						, coalesce(OPI."SO_HOA_DON", '')
						, coalesce(OPI."TY_GIA", 1)
						, coalesce(OPN."TY_GIA", 1)
						, OPID."HAN_THANH_TOAN"
						, OPID2."NHAN_VIEN_ID"
					HAVING SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
						THEN OPI."SO_CON_PHAI_THU_NGUYEN_TE" - OPI."SO_THU_TRUOC_NGUYEN_TE"
								ELSE coalesce(OPN."DU_CO_NGUYEN_TE", 0) - coalesce(OPN."DU_NO_NGUYEN_TE", 0) END) > 0;

				DROP TABLE IF EXISTS TMP_TABLE2;
				CREATE TEMP TABLE TMP_TABLE2
					AS
					SELECT
						AL."ID_CHUNG_TU",
						cast(AL."LOAI_CHUNG_TU" AS VARCHAR(50))
						--					,RT."REFTYPENAME" AS "TEN_LOAI_CHUNG_TU"
						,
						AL."NGAY_CHUNG_TU",
						AL."NGAY_HACH_TOAN",
						AL."SO_CHUNG_TU",
						AL."NGAY_HOA_DON",
						coalesce(AL."SO_HOA_DON", '')                                                AS "SO_HOA_DON",
						coalesce(AL."DIEN_GIAI_CHUNG", '')                                           AS "DIEN_GIAI",
						coalesce(AL."TY_GIA", 1)                                                     AS "TY_GIA",
						SUM(coalesce(AL."GHI_CO_NGUYEN_TE", 0) - coalesce(AL."GHI_NO_NGUYEN_TE", 0)) AS "TONG_TIEN",
						SUM(coalesce(AL."GHI_CO", 0) - coalesce(AL."GHI_NO", 0))                     AS "TONG_TIEN_QUY_DOI",
						SUM(coalesce(AL."GHI_CO_NGUYEN_TE", 0) - coalesce(AL."GHI_NO_NGUYEN_TE", 0)) AS "SO_TIEN",
						SUM(coalesce(AL."GHI_CO", 0) - coalesce(AL."GHI_NO", 0))                     AS "SO_TIEN_QUY_DOI",
						(CASE
						WHEN AL."LOAI_CHUNG_TU" IN
							(330, 331, 332, 333, 334, 352, 357, 358, 359, 360, 362, 363, 364, 365, 366, 368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
						THEN 1 /*Với dịch vụ và mua hàng nhiều hóa đơn thì chi tiết theo từng hóa đơn*/
						ELSE 0
						END)                                                                        AS "SO_HOA_DON_CHI_TIET",
						AL."NGAY_HET_HAN"
						/*Nếu chứng từ Nghiệp vụ khác thì sẽ lấy nhân viên đầu tiên trên form chi tiết*/,
						CASE WHEN GVDT."ID_CHUNG_TU" IS NOT NULL
						THEN GVDT."NHAN_VIEN_ID"
						ELSE AL."NHAN_VIEN_ID" END                                                   AS "NHAN_VIEN_ID",
						"MODEL_CHUNG_TU"
					FROM so_cong_no_chi_tiet AL
						--					INNER JOIN danh_muc_reftype RT ON RT."REFTYPE" = AL."LOAI_CHUNG_TU"
						LEFT JOIN (/*Lấy Nhân viên trên chứng từ nghiệp vụ khác*/
									SELECT
									AOL."ID_CHUNG_TU",
									AOL."DOI_TUONG_ID",
									AOL."MA_TK",
									AOL."NHAN_VIEN_ID",
									ROW_NUMBER()
									OVER (
										PARTITION BY AOL."ID_CHUNG_TU", AOL."DOI_TUONG_ID", AOL."MA_TK"
										ORDER BY AOL."THU_TU_TRONG_CHUNG_TU" ) AS RowNumber
									FROM so_cong_no_chi_tiet AS AOL
									WHERE AOL."LOAI_CHUNG_TU" IN (4010, 4011, 4012, 4014, 4015, 4018, 4020, 4030)
										/*Chỉ lấy theo "LOAI_CHUNG_TU" của bảng GlVoucherDetail
										Không lấy các chứng từ Chứng từ bù trừ công nợ, Xử lý chênh lệch tỷ giá từ đánh giá lại tài khoản ngoại tệ, Xử lý chênh lệch tỷ giá từ tính tỷ giá xuất quỹ
										*/
										AND AOL."NHAN_VIEN_ID" IS NOT NULL) AS GVDT ON GVDT."ID_CHUNG_TU" = AL."ID_CHUNG_TU"
																						AND
																						GVDT."DOI_TUONG_ID" = AL."DOI_TUONG_ID"
																						AND GVDT."MA_TK" = AL."MA_TK"
																						AND GVDT.RowNumber = 1
						LEFT JOIN (
									/* Lấy danh sách chứng từ trả lại giảm giá chọn trực tiếp*/
									SELECT "TRA_LAI_HANG_BAN_ID" AS "ID_CHUNG_TU"
									FROM sale_ex_tra_lai_hang_ban_chi_tiet
									WHERE "CHUNG_TU_BAN_HANG_ID" IS NOT NULL
									UNION
									SELECT "GIAM_GIA_HANG_BAN_ID" AS "ID_CHUNG_TU"
									FROM sale_ex_chi_tiet_giam_gia_hang_ban
									WHERE "CHUNG_TU_BAN_HANG_ID" IS NOT NULL
								) SR ON AL."ID_CHUNG_TU" = SR."ID_CHUNG_TU"
					WHERE (AL."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id ISNULL)
							AND AL."currency_id" = loai_tien_id
							AND AL."TK_ID" = (SELECT id
											FROM danh_muc_he_thong_tai_khoan
											WHERE "SO_TAI_KHOAN" = '331')
							AND AL."CHI_NHANH_ID" = chi_nhanh_id
							AND AL."NGAY_HACH_TOAN" <= den_ngay
							/* Không lấy các chứng từ Phiếu thu tiền khách hàng, Phiếu thu tiền khách hàng hàng loạt, Phiếu chi trả tiền nhà cung cấp,
							*  Phiếu thu tiền gửi khách hàng, Phiếu thu tiền gửi khách hàng hàng loạt, Trả tiền nhà cung cấp bằng Ủy nhiệm chi,
							*  Séc tiền mặt trả tiền nhà cung cấp, Séc chuyển khoản trả tiền nhà cung cấp, Chứng từ xử lý chênh lệch tỷ giá,
							*  Chứng từ bù trừ công nợ, Xử lý chênh lệch tỷ giá từ đánh giá lại tài khoản ngoại tệ, Xử lý chênh lệch tỷ giá từ tính tỷ giá xuất quỹ*/
							AND
							AL."LOAI_CHUNG_TU" NOT IN (1011, 1012, 1021, 1502, 1503, 1511, 1521, 1531, 4013, 4014, 4016, 4017)
							/*Không lấy số dư đầu kỳ do lấy ở trên rồi*/
							AND AL."LOAI_CHUNG_TU" NOT IN (611, 612, 613, 614, 615, 616, 630)
							/*Không lấy các chứng từ trả lại, giảm giá*/
							AND SR."ID_CHUNG_TU" IS NULL
					GROUP BY AL."ID_CHUNG_TU"
						, AL."LOAI_CHUNG_TU"
						--					,RT."REFTYPENAME"
						, AL."NGAY_CHUNG_TU"
						, AL."NGAY_HACH_TOAN"
						, AL."SO_CHUNG_TU"
						, AL."NGAY_HOA_DON"
						, coalesce(AL."SO_HOA_DON", '')
						, coalesce(AL."DIEN_GIAI_CHUNG", '')
						, coalesce(AL."TY_GIA", 1)
						, AL."NGAY_HET_HAN"
						, CASE WHEN GVDT."ID_CHUNG_TU" IS NOT NULL
						THEN GVDT."NHAN_VIEN_ID"
						ELSE AL."NHAN_VIEN_ID" END
						, "MODEL_CHUNG_TU"
					HAVING SUM(coalesce(AL."GHI_CO_NGUYEN_TE", 0) - coalesce(AL."GHI_NO_NGUYEN_TE", 0)) > 0;


				DROP TABLE IF EXISTS TMP_KET_QUA;
				CREATE TEMP TABLE TMP_KET_QUA
					AS

					SELECT
						CAST(TRUE AS BOOLEAN)                                                       AS Selected,
						TEM."ID_CHUNG_TU",
						TEM."LOAI_CHUNG_TU"
						--				 ,TEM."TEN_LOAI_CHUNG_TU"
						,
						TEM."NGAY_CHUNG_TU",
						TEM."NGAY_HACH_TOAN",
						TEM."SO_CHUNG_TU",
						TEM."NGAY_HOA_DON",
						TEM."SO_HOA_DON",
						TEM."DIEN_GIAI",
						CASE WHEN TEM."TY_GIA" = 0 THEN 1 ELSE TEM."TY_GIA" END "TY_GIA",
						coalesce(GV."TY_GIA", 0)                                                    AS "TY_GIA_DANH_GIA_LAI",
						TEM."TONG_TIEN"                                                             AS "SO_TIEN",
						TEM."TONG_TIEN_QUY_DOI"                                                     AS "SO_TIEN_QUY_DOI",
						coalesce(TEM."SO_TIEN", 0) - SUM(coalesce(GL."SO_TIEN", 0))                 AS "SO_TIEN_PHAI_TRA",
						coalesce(TEM."SO_TIEN_QUY_DOI", 0) - SUM(coalesce(GL."SO_TIEN_QUY_DOI", 0)) AS "SO_TIEN_PHAI_TRA_QUY_DOI",
						CAST(0 AS DECIMAL)                                                          AS "SO_TIEN_BU_TRU",
						CAST(0 AS DECIMAL)                                                          AS "SO_TIEN_BU_TRU_QUY_DOI",
						doi_tuong_id                                                                AS "DOI_TUONG_ID",
						TEM."HAN_THANH_TOAN",
						Tem."NHAN_VIEN_ID",
						TEM."MODEL_CHUNG_TU"
					FROM (
							SELECT *
							FROM TMP_TABLE1

							UNION ALL

							SELECT *
							FROM TMP_TABLE2

						) AS TEM
						LEFT JOIN (SELECT *
								FROM PU_LAY_SO_TIEN_DA_TRA_CUA_CHUNG_TU_CONG_NO('331', loai_tien_id, chi_nhanh_id, doi_tuong_id)) GL
						ON GL."ID_CHUNG_TU" = TEM."ID_CHUNG_TU" AND GL."MODEL_CHUNG_TU" = TEM."MODEL_CHUNG_TU"
							AND (TEM."SO_HOA_DON_CHI_TIET" = 0 OR (TEM."SO_HOA_DON_CHI_TIET" = 1 AND
																	coalesce(GL."NGAY_HOA_DON", den_ngay) =
																	coalesce(TEM."NGAY_HOA_DON", den_ngay)))
						LEFT JOIN (
									/* NBHIEU 12/05/2016 (bug 102978) Lấy tỷ giá đánh giá lại dưới chi tiết nếu là quyết dịnh 15*/
									SELECT
									CASE WHEN '15' = '15'
										THEN coalesce(GVD."TY_GIA_DANH_GIA_LAI", 1)
									ELSE coalesce(GV."TY_GIA", 1) END                            AS "TY_GIA",
									GVD."ID_CHUNG_TU_GOC",
									ROW_NUMBER()
									OVER (
										PARTITION BY GVD."ID_CHUNG_TU_GOC"
										ORDER BY GVD."ID_CHUNG_TU_GOC", GV."NGAY_HACH_TOAN" DESC ) AS RowNumber
									FROM account_ex_chung_tu_nghiep_vu_khac GV
									INNER JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan GVD
										ON GVD."CHUNG_TU_NGHIEP_VU_KHAC_ID" = GV.id
									WHERE GV.currency_id = loai_tien_id
										-- 	 				AND GV."CHI_NHANH_ID" = (chi_nhanh_id)
										AND GVD."TK_CONG_NO_ID" = (SELECT id
																	FROM danh_muc_he_thong_tai_khoan
																	WHERE "SO_TAI_KHOAN" = '331')
										AND GVD."DOI_TUONG_ID" = doi_tuong_id
								) AS GV ON TEM."ID_CHUNG_TU" = GV."ID_CHUNG_TU_GOC" AND GV.RowNumber = 1
					GROUP BY TEM."ID_CHUNG_TU"
						, TEM."LOAI_CHUNG_TU"
						--				 ,TEM."TEN_LOAI_CHUNG_TU"
						, TEM."NGAY_CHUNG_TU"
						, TEM."NGAY_HACH_TOAN"
						, TEM."SO_CHUNG_TU"
						, TEM."NGAY_HOA_DON"
						, TEM."SO_HOA_DON"
						, TEM."DIEN_GIAI"
						, CASE WHEN TEM."TY_GIA" = 0 THEN 1 ELSE TEM."TY_GIA" END
						--         , coalesce(GV."TY_GIA", 0)
						, TEM."SO_TIEN"
						, TEM."SO_TIEN_QUY_DOI"
						, TEM."TONG_TIEN"
						, TEM."TONG_TIEN_QUY_DOI"
						, TEM."HAN_THANH_TOAN"
						, Tem."NHAN_VIEN_ID"
						, TEM."MODEL_CHUNG_TU"
						, GV."TY_GIA"
					HAVING coalesce(TEM."SO_TIEN", 0) - SUM(coalesce(GL."SO_TIEN", 0)) > 0
					ORDER BY TEM."NGAY_CHUNG_TU", TEM."NGAY_HACH_TOAN", TEM."SO_CHUNG_TU", TEM."NGAY_HOA_DON", TEM."SO_HOA_DON";


				END $$;

				SELECT *
				FROM TMP_KET_QUA

				"""  
			
			return self.execute(query, params)

		def chung_tu_phai_thu(self,ngay,doi_tuong,loai_tien):
				params = {
						'DEN_NGAY': ngay,
						'DOI_TUONG_ID' : doi_tuong,
						'currency_id' : loai_tien,
						'CHI_NHANH_ID' : self.get_chi_nhanh(),
						}

				query = """   

				DO LANGUAGE plpgsql $$ DECLARE

				doi_tuong_id INTEGER := %(DOI_TUONG_ID)s;
				chi_nhanh_id INTEGER := %(CHI_NHANH_ID)s;
				den_ngay     DATE := %(DEN_NGAY)s;
				loai_tien_id INTEGER := %(currency_id)s;


				BEGIN

				DROP TABLE IF EXISTS TMP_TABLE1;
				CREATE TEMP TABLE TMP_TABLE1
					AS
					SELECT
									OPN.id AS "ID_CHUNG_TU"
									,OPN."LOAI_CHUNG_TU"
				--					,RT."REFTYPENAME" AS "TEN_LOAI_CHUNG_TU"
									,(CASE
										WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL THEN OPI."NGAY_HOA_DON"
										ELSE OPN."NGAY_HACH_TOAN"
									END) AS "NGAY_CHUNG_TU"
									,OPN."NGAY_HACH_TOAN"
									,'OPN' AS "SO_CHUNG_TU"
									,OPI."NGAY_HOA_DON"
									,coalesce(OPI."SO_HOA_DON",'') AS "SO_HOA_DON"
									,'' AS "DIEN_GIAI"
									,(CASE
										WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL THEN coalesce(OPI."TY_GIA",1)
										ELSE coalesce(OPN."TY_GIA",1)
									END) AS "TY_GIA"
									,SUM(CASE
										WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL THEN coalesce(OPI."GIA_TRI_HOA_DON_NGUYEN_TE",0)
										ELSE coalesce(OPN."DU_NO_NGUYEN_TE",0) - coalesce(OPN."DU_CO_NGUYEN_TE",0)
									END) AS "TONG_TIEN"
									,SUM(CASE
										WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL THEN coalesce(OPI."GIA_TRI_HOA_DON",0)
										ELSE coalesce(OPN."DU_NO",0) - coalesce(OPN."DU_CO",0)
									END) AS "TONG_TIEN_QUY_DOI"
									,SUM(CASE
										WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL THEN OPI."SO_CON_PHAI_THU_NGUYEN_TE" - OPI."SO_THU_TRUOC_NGUYEN_TE"
										ELSE coalesce(OPN."DU_NO_NGUYEN_TE",0) - coalesce(OPN."DU_CO_NGUYEN_TE",0)
									END) AS "SO_TIEN"
									,SUM(CASE
										WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL THEN OPI."SO_CON_PHAI_THU" - OPI."SO_THU_TRUOC"
										ELSE coalesce(OPN."DU_NO",0) - coalesce(OPN."DU_CO",0)
									END) AS "SO_TIEN_QUY_DOI"
									,1 AS "SO_HOA_DON_CHI_TIET"
									,OPID."HAN_THANH_TOAN"
									,OPID2."NHAN_VIEN_ID"
									,'account.ex.so.du.tai.khoan.chi.tiet' AS "MODEL_CHUNG_TU"
									,OPN."DOI_TUONG_ID"
						FROM		account_ex_so_du_tai_khoan_chi_tiet OPN
									INNER JOIN danh_muc_reftype RT ON cast(RT."REFTYPE" AS VARCHAR(50)) = OPN."LOAI_CHUNG_TU"
									LEFT JOIN account_ex_sdtkct_theo_hoa_don OPI ON OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" = OPN.id
									LEFT JOIN (	SELECT  OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID" ,
																			coalesce(OAEDI."NGAY_HOA_DON",NOW()) AS "NGAY_HOA_DON" ,
																			coalesce(OAEDI."SO_HOA_DON",'') AS "SO_HOA_DON" ,
																			coalesce(OAEDI."TY_GIA",0) AS "TY_GIA" ,
																			OAEDI."NHAN_VIEN_ID" ,
																ROW_NUMBER() OVER(PARTITION BY OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID",coalesce(OAEDI."NGAY_HOA_DON",den_ngay),coalesce(OAEDI."SO_HOA_DON",''),coalesce(OAEDI."TY_GIA",0)) AS RowNumber
														FROM account_ex_sdtkct_theo_hoa_don AS OAEDI
														WHERE OAEDI."NHAN_VIEN_ID" IS NOT NULL) AS OPID2 ON OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" = OPID2."SO_DU_TAI_KHOAN_CHI_TIET_ID"
																							AND OPID2.RowNumber = 1
																							AND coalesce(OPI."SO_HOA_DON",'') = coalesce(OPID2."SO_HOA_DON",'')
																							AND coalesce(OPI."NGAY_HOA_DON",den_ngay) = coalesce(OPID2."NGAY_HOA_DON",den_ngay)
																							AND coalesce(OPI."TY_GIA",0) = coalesce(OPID2."TY_GIA",0)
									LEFT JOIN (	SELECT	OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID",
														coalesce(OAEDI."NGAY_HOA_DON",den_ngay) AS "NGAY_HOA_DON",
														coalesce(OAEDI."SO_HOA_DON",'') AS "SO_HOA_DON",
														OAEDI."HAN_THANH_TOAN",
														coalesce(OAEDI."TY_GIA",0) AS "TY_GIA",
														ROW_NUMBER() OVER(PARTITION BY OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID",coalesce(OAEDI."NGAY_HOA_DON",den_ngay),coalesce(OAEDI."SO_HOA_DON",''),coalesce(OAEDI."TY_GIA",0)) AS RowNumber
												FROM account_ex_sdtkct_theo_hoa_don AS OAEDI
												WHERE OAEDI."HAN_THANH_TOAN" IS NOT NULL) AS OPID ON OPN.id = OPID."SO_DU_TAI_KHOAN_CHI_TIET_ID"
																					AND OPID.RowNumber = 1
																					AND coalesce(OPI."SO_HOA_DON",'') = coalesce(OPID."SO_HOA_DON",'')
																					AND coalesce(OPI."NGAY_HOA_DON",den_ngay) = coalesce(OPID."NGAY_HOA_DON",den_ngay)
																					AND coalesce(OPI."TY_GIA",0) = coalesce(OPID."TY_GIA",0)
						WHERE		(OPN."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id ISNULL )
									AND OPN."currency_id" = loai_tien_id
									AND OPN."TK_ID" = (SELECT id from danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN" = '131')
				-- 					AND OPN."CHI_NHANH_ID" =(chi_nhanh_id)
									AND	OPN."NGAY_HACH_TOAN" <= den_ngay

						GROUP BY	OPN.id
									,OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID"
									,OPN."LOAI_CHUNG_TU"
				--					,RT."REFTYPENAME"
									,OPN."NGAY_HACH_TOAN"
									,OPI."NGAY_HOA_DON"
									,coalesce(OPI."SO_HOA_DON",'')
									,coalesce(OPI."TY_GIA",1)
									,coalesce(OPN."TY_GIA",1)
									,OPID."HAN_THANH_TOAN"
									,OPID2."NHAN_VIEN_ID"
									,OPN."DOI_TUONG_ID"
				HAVING		SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL THEN OPI."SO_CON_PHAI_THU_NGUYEN_TE"-OPI."SO_THU_TRUOC_NGUYEN_TE" ELSE coalesce(OPN."DU_NO_NGUYEN_TE",0) - coalesce(OPN."DU_CO_NGUYEN_TE",0) END) > 0
				;

				DROP TABLE IF EXISTS TMP_TABLE2;
				CREATE TEMP TABLE TMP_TABLE2
					AS
					SELECT
									AL."ID_CHUNG_TU"
									,cast(AL."LOAI_CHUNG_TU" AS VARCHAR(50))
				--					,RT."REFTYPENAME" AS "TEN_LOAI_CHUNG_TU"
									,AL."NGAY_CHUNG_TU"
									,AL."NGAY_HACH_TOAN"
									,AL."SO_CHUNG_TU"
									,AL."NGAY_HOA_DON"
									,coalesce(AL."SO_HOA_DON", '') AS "SO_HOA_DON"
									,coalesce(AL."DIEN_GIAI_CHUNG", '') AS "DIEN_GIAI"
									,coalesce(AL."TY_GIA", 1) AS "TY_GIA"
									,SUM(coalesce(AL."GHI_NO_NGUYEN_TE", 0) - coalesce(AL."GHI_CO_NGUYEN_TE", 0)) AS "TONG_TIEN"
									,SUM(coalesce(AL."GHI_NO", 0) - coalesce(AL."GHI_CO", 0)) AS "TONG_TIEN_QUY_DOI"
									,SUM(coalesce(AL."GHI_NO_NGUYEN_TE", 0) - coalesce(AL."GHI_CO_NGUYEN_TE", 0)) AS "SO_TIEN"
									,SUM(coalesce(AL."GHI_NO", 0) - coalesce(AL."GHI_CO", 0)) AS "SO_TIEN_QUY_DOI"
									,0 AS "SO_HOA_DON_CHI_TIET"
									,AL."NGAY_HET_HAN"
									/*Nếu chứng từ Nghiệp vụ khác thì sẽ lấy nhân viên đầu tiên trên form chi tiết*/
														,CASE WHEN GVDT."ID_CHUNG_TU" IS NOT NULL THEN GVDT."NHAN_VIEN_ID" ELSE AL."NHAN_VIEN_ID" END AS "NHAN_VIEN_ID"
									,AL."MODEL_CHUNG_TU"
									,AL."DOI_TUONG_ID"
							FROM      so_cong_no_chi_tiet AL
				--					INNER JOIN danh_muc_reftype RT ON RT."REFTYPE" = AL."LOAI_CHUNG_TU"
									LEFT JOIN(/*Lấy Nhân viên trên chứng từ nghiệp vụ khác*/
												SELECT	AOL."ID_CHUNG_TU",
														AOL."DOI_TUONG_ID",
														AOL."MA_TK",
														AOL."NHAN_VIEN_ID",
														ROW_NUMBER() OVER(PARTITION BY AOL."ID_CHUNG_TU",AOL."DOI_TUONG_ID",AOL."MA_TK" ORDER BY AOL."THU_TU_TRONG_CHUNG_TU") AS RowNumber
												FROM so_cong_no_chi_tiet AS AOL
												WHERE AOL."LOAI_CHUNG_TU" IN (4010,4011,4012,4014,4015,4018,4020,4030)
																/*Chỉ lấy theo "LOAI_CHUNG_TU" của bảng GlVoucherDetail
																Không lấy các chứng từ Chứng từ bù trừ công nợ, Xử lý chênh lệch tỷ giá từ đánh giá lại tài khoản ngoại tệ, Xử lý chênh lệch tỷ giá từ tính tỷ giá xuất quỹ
																*/
													AND AOL."NHAN_VIEN_ID" IS NOT NULL) AS GVDT ON GVDT."ID_CHUNG_TU" = AL."ID_CHUNG_TU"
																							AND GVDT."DOI_TUONG_ID" = AL."DOI_TUONG_ID"
																							AND GVDT."MA_TK" = AL."MA_TK"
																							AND GVDT.RowNumber = 1
									LEFT JOIN (
										/* Lấy danh sách chứng từ trả lại giảm giá chọn trực tiếp*/
										SELECT "TRA_LAI_HANG_BAN_ID" AS "ID_CHUNG_TU" FROM sale_ex_tra_lai_hang_ban_chi_tiet WHERE "CHUNG_TU_BAN_HANG_ID" IS NOT NULL
										UNION
										SELECT "GIAM_GIA_HANG_BAN_ID" AS "ID_CHUNG_TU" FROM sale_ex_chi_tiet_giam_gia_hang_ban WHERE "CHUNG_TU_BAN_HANG_ID" IS NOT NULL
									) SR ON AL."ID_CHUNG_TU" = SR."ID_CHUNG_TU"
							WHERE     (AL."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id ISNULL )
									AND AL."currency_id" = loai_tien_id
									AND AL."TK_ID" = (SELECT id from danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN" = '131')
				-- 					AND AL."CHI_NHANH_ID" = (chi_nhanh_id)
									AND AL."NGAY_HACH_TOAN" <= den_ngay
									/* Không lấy các chứng từ Phiếu thu tiền khách hàng, Phiếu thu tiền khách hàng hàng loạt, Phiếu chi trả tiền nhà cung cấp,
									*  Phiếu thu tiền gửi khách hàng, Phiếu thu tiền gửi khách hàng hàng loạt, Trả tiền nhà cung cấp bằng Ủy nhiệm chi,
									*  Séc tiền mặt trả tiền nhà cung cấp, Séc chuyển khoản trả tiền nhà cung cấp, Chứng từ xử lý chênh lệch tỷ giá,
									*  Chứng từ bù trừ công nợ, Xử lý chênh lệch tỷ giá từ đánh giá lại tài khoản ngoại tệ, Xử lý chênh lệch tỷ giá từ tính tỷ giá xuất quỹ*/
									AND AL."LOAI_CHUNG_TU" NOT IN (1011, 1012, 1021, 1502, 1503, 1511, 1521, 1531, 4013, 4014, 4016, 4017)
									/*Không lấy số dư đầu kỳ do lấy ở trên rồi*/
									AND AL."LOAI_CHUNG_TU" NOT IN (611,612,613,614,615,616,630)
									/*Không lấy các chứng từ trả lại, giảm giá*/
									AND SR."ID_CHUNG_TU" IS NULL
							GROUP BY  AL."ID_CHUNG_TU"
									,AL."LOAI_CHUNG_TU"
				--					,RT."REFTYPENAME"
									,AL."NGAY_CHUNG_TU"
									,AL."NGAY_HACH_TOAN"
									,AL."SO_CHUNG_TU"
									,AL."NGAY_HOA_DON"
									,coalesce(AL."SO_HOA_DON", '')
									,coalesce(AL."DIEN_GIAI_CHUNG", '')
									,coalesce(AL."TY_GIA", 1)
									,AL."NGAY_HET_HAN"
									,CASE WHEN GVDT."ID_CHUNG_TU" IS NOT NULL THEN GVDT."NHAN_VIEN_ID" ELSE AL."NHAN_VIEN_ID" END
									,AL."MODEL_CHUNG_TU"
									,AL."DOI_TUONG_ID"
						HAVING		SUM(coalesce(AL."GHI_NO_NGUYEN_TE", 0) - coalesce(AL."GHI_CO_NGUYEN_TE", 0)) > 0
				;


				DROP TABLE IF EXISTS TMP_KET_QUA3;
				CREATE TEMP TABLE TMP_KET_QUA3
					AS

					SELECT CAST(TRUE AS BOOLEAN) AS Selected
								,TEM."ID_CHUNG_TU"
								,TEM."LOAI_CHUNG_TU"
								,dt."MA"
								,TEM."NGAY_CHUNG_TU"
								,TEM."NGAY_HACH_TOAN"
								,TEM."SO_CHUNG_TU"
								,TEM."NGAY_HOA_DON"
								,TEM."SO_HOA_DON"
								,TEM."DIEN_GIAI"
								,CASE WHEN TEM."TY_GIA" = 0 THEN 1 ELSE TEM."TY_GIA" END "TY_GIA"
								,coalesce(GV."TY_GIA",0) AS "TY_GIA_DANH_GIA_LAI"
								,TEM."TONG_TIEN" AS "SO_TIEN"
								,TEM."TONG_TIEN_QUY_DOI" AS "SO_TIEN_QUY_DOI"
								,coalesce(TEM."SO_TIEN",0) - SUM(coalesce(GL."SO_TIEN",0)) AS "SO_TIEN_THANH_TOAN"
								,coalesce(TEM."SO_TIEN_QUY_DOI",0) - SUM(coalesce(GL."SO_TIEN_QUY_DOI",0)) AS "SO_TIEN_THANH_QUY_DOI"
								,CAST(0 AS DECIMAL) AS "SO_TIEN_BU_TRU"
									,CAST(0 AS DECIMAL) AS "SO_TIEN_BU_TRU_QUY_DOI"
									,doi_tuong_id AS "DOI_TUONG_ID"
									,TEM."HAN_THANH_TOAN"
									,TEM."NHAN_VIEN_ID"
									,TEM."MODEL_CHUNG_TU"

					FROM	 (
							SELECT *
							FROM TMP_TABLE1

							UNION ALL

							SELECT *
							FROM TMP_TABLE2

						) AS TEM
						LEFT JOIN (SELECT *FROM SA_LAY_SO_TIEN_DA_THU_CUA_CHUNG_TU_CONG_NO('331',loai_tien_id,chi_nhanh_id,doi_tuong_id)) GL
							ON	GL."ID_CHUNG_TU" = TEM."ID_CHUNG_TU" AND GL."MODEL_CHUNG_TU" = TEM."MODEL_CHUNG_TU"
								AND (TEM."SO_HOA_DON_CHI_TIET" = 0 OR (TEM."SO_HOA_DON_CHI_TIET" =1 AND coalesce(GL."NGAY_HOA_DON", den_ngay) = coalesce(TEM."NGAY_HOA_DON", den_ngay)))
						LEFT JOIN (
							/* NBHIEU 12/05/2016 (bug 102978) Lấy tỷ giá đánh giá lại dưới chi tiết nếu là quyết dịnh 15*/
							SELECT	CASE WHEN '15' ='15' THEN coalesce(GVD."TY_GIA_DANH_GIA_LAI",1) ELSE coalesce(GV."TY_GIA",1) END AS "TY_GIA"
									,GVD."ID_CHUNG_TU_GOC"
									,ROW_NUMBER () OVER (PARTITION BY GVD."ID_CHUNG_TU_GOC" ORDER BY GVD."ID_CHUNG_TU_GOC", GV."NGAY_HACH_TOAN" DESC ) AS RowNumber
							FROM	account_ex_chung_tu_nghiep_vu_khac GV
									INNER JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan GVD ON GVD."CHUNG_TU_NGHIEP_VU_KHAC_ID" = GV.id
							WHERE	GV.currency_id = loai_tien_id
					 				AND GV."CHI_NHANH_ID" = (chi_nhanh_id)
									AND GVD."TK_CONG_NO_ID" = (SELECT id from danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN" = '131')
									AND (GVD."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id ISNULL )
						) AS GV ON TEM."ID_CHUNG_TU" = GV."ID_CHUNG_TU_GOC" AND GV.RowNumber = 1
					LEFT JOIN res_partner dt ON TEM."DOI_TUONG_ID" = dt.id
					WHERE dt."LA_KHACH_HANG" = TRUE  AND "LA_NHA_CUNG_CAP" = TRUE
					GROUP BY  TEM."ID_CHUNG_TU"
								,TEM."LOAI_CHUNG_TU"
								,TEM."NGAY_CHUNG_TU"
								,TEM."NGAY_HACH_TOAN"
								,TEM."SO_CHUNG_TU"
								,TEM."NGAY_HOA_DON"
								,TEM."SO_HOA_DON"
								,TEM."DIEN_GIAI"
								,CASE WHEN TEM."TY_GIA" = 0 THEN 1 ELSE TEM."TY_GIA" END
								,TEM."SO_TIEN"
								,TEM."SO_TIEN_QUY_DOI"
								,TEM."TONG_TIEN"
								,TEM."TONG_TIEN_QUY_DOI"
								,TEM."HAN_THANH_TOAN"
								,TEM."NHAN_VIEN_ID"
								,TEM."MODEL_CHUNG_TU"
								,dt."MA"
								,coalesce(GV."TY_GIA",0)
					HAVING coalesce(TEM."SO_TIEN",0) - SUM(coalesce(GL."SO_TIEN",0)) > 0
					ORDER BY TEM."NGAY_CHUNG_TU", TEM."NGAY_HACH_TOAN", TEM."SO_CHUNG_TU",TEM."NGAY_HOA_DON" , TEM."SO_HOA_DON"
					;


				END $$;

				SELECT *
				FROM TMP_KET_QUA3

				"""  
				return self.execute(query, params)

		# @api.depends('SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS.AUTO_SELECT')
		# def doi_tru_chung_tu(self):
		# 		tong_tien_phai_tra = 0
		# 		tong_tien_phai_thu = 0
		# 		for line in self.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS:
		# 				if line.AUTO_SELECT == True:
		# 						tong_tien_phai_tra += line.SO_CON_NO
		# 		for line in self.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS:
		# 				if line.AUTO_SELECT == True:
		# 						tong_tien_phai_thu += line.SO_CHUA_THU
		# 		if tong_tien_phai_thu > 0 and tong_tien_phai_tra > 0:
		# 				if tong_tien_phai_tra > tong_tien_phai_thu:
		# 						for line in self.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS:
		# 								if line.AUTO_SELECT == True:
		# 										line.SO_TIEN_BU_TRU = line.SO_CHUA_THU
		# 						for line1 in self.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS:
		# 								if line1.AUTO_SELECT == True:
		# 										if tong_tien_phai_thu == 0:
		# 										#     line1.SO_TIEN_BU_TRU = line1.SO_CHUA_THU
		# 										# if tong_tien_phai_thu == 1:
		# 												line1.SO_TIEN_BU_TRU = 0
		# 										elif line1.SO_CON_NO < tong_tien_phai_thu:
		# 												line1.SO_TIEN_BU_TRU = line1.SO_CON_NO
		# 												tong_tien_phai_thu = tong_tien_phai_thu - line1.SO_TIEN_BU_TRU
		# 										elif line1.SO_CON_NO > tong_tien_phai_thu:
		# 												line1.SO_TIEN_BU_TRU = tong_tien_phai_thu
		# 												tong_tien_phai_thu = 0
		# 				elif tong_tien_phai_tra < tong_tien_phai_thu:
		# 						for line1 in self.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS:
		# 								if line1.AUTO_SELECT == True:
		# 										# if line1.SO_CHUA_THU > tong_tien_phai_thu:
		# 										#     line1.SO_TIEN_BU_TRU = tong_tien_phai_thu
		# 										#     tong_tien_phai_thu = 0
		# 										line1.SO_TIEN_BU_TRU = line1.SO_TIEN

		# 						for line in self.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS:
		# 								if line.AUTO_SELECT == True:
		# 										if tong_tien_phai_tra == 0:
		# 												#line.SO_TIEN_BU_TRU = line.SO_CON_NO
		# 										# if tong_tien_phai_tra == 1:
		# 												line.SO_TIEN_BU_TRU = 0
		# 										elif tong_tien_phai_tra > line.SO_CHUA_THU:
		# 												line.SO_TIEN_BU_TRU = line.SO_CHUA_THU
		# 												tong_tien_phai_tra = tong_tien_phai_tra - line.SO_TIEN_BU_TRU
		# 										elif tong_tien_phai_tra  < line.SO_CHUA_THU:
		# 												line.SO_TIEN_BU_TRU = tong_tien_phai_tra
		# 												tong_tien_phai_tra = 0
		# @api.depends('SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS.AUTO_SELECT')
		# def doi_tru_cong_no(self):
		# 		tong_tien_phai_tra = 0
		# 		tong_tien_phai_thu = 0
		# 		for line in self.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS:
		# 				if line.AUTO_SELECT == True:
		# 						tong_tien_phai_tra += line.SO_CON_NO
		# 		for line in self.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS:
		# 				if line.AUTO_SELECT == True:
		# 						tong_tien_phai_thu += line.SO_CHUA_THU
		# 		if tong_tien_phai_thu > 0 and tong_tien_phai_tra > 0:
		# 				if tong_tien_phai_tra > tong_tien_phai_thu:
		# 						for line in self.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS:
		# 								if line.AUTO_SELECT == True:
		# 										line.SO_TIEN_BU_TRU = line.SO_CHUA_THU
		# 						for line1 in self.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS:
		# 								if line1.AUTO_SELECT == True:
		# 										if tong_tien_phai_thu == 0:
		# 										#     line1.SO_TIEN_BU_TRU = line1.SO_CHUA_THU
		# 										# if tong_tien_phai_thu == 1:
		# 												line1.SO_TIEN_BU_TRU = 0
		# 										elif line1.SO_CON_NO < tong_tien_phai_thu:
		# 												line1.SO_TIEN_BU_TRU = line1.SO_CON_NO
		# 												tong_tien_phai_thu = tong_tien_phai_thu - line1.SO_TIEN_BU_TRU
		# 										elif line1.SO_CON_NO > tong_tien_phai_thu:
		# 												line1.SO_TIEN_BU_TRU = tong_tien_phai_thu
		# 												tong_tien_phai_thu = 0
		# 				elif tong_tien_phai_tra < tong_tien_phai_thu:
		# 						for line1 in self.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS:
		# 								if line1.AUTO_SELECT == True:
		# 										# if line1.SO_CHUA_THU > tong_tien_phai_thu:
		# 										#     line1.SO_TIEN_BU_TRU = tong_tien_phai_thu
		# 										#     tong_tien_phai_thu = 0
		# 										line1.SO_TIEN_BU_TRU = line1.SO_TIEN

		# 						for line in self.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS:
		# 								if line.AUTO_SELECT == True:
		# 										if tong_tien_phai_tra == 0:
		# 												#line.SO_TIEN_BU_TRU = line.SO_CON_NO
		# 										# if tong_tien_phai_tra == 1:
		# 												line.SO_TIEN_BU_TRU = 0
		# 										elif tong_tien_phai_tra > line.SO_CHUA_THU:
		# 												line.SO_TIEN_BU_TRU = line.SO_CHUA_THU
		# 												tong_tien_phai_tra = tong_tien_phai_tra - line.SO_TIEN_BU_TRU
		# 										elif tong_tien_phai_tra  < line.SO_CHUA_THU:
		# 												line.SO_TIEN_BU_TRU = tong_tien_phai_tra
		# 												tong_tien_phai_tra = 0
		



		@api.model_cr
		def init(self):
			self.env.cr.execute(""" 
							-- DROP FUNCTION PU_LAY_SO_TIEN_DA_TRA_CUA_CHUNG_TU_CONG_NO(IN ma_tai_khoan VARCHAR(50),loai_tien_id INTEGER,chi_nhanh_id INTEGER,doi_tuong_id INTEGER)
							CREATE OR REPLACE FUNCTION PU_LAY_SO_TIEN_DA_TRA_CUA_CHUNG_TU_CONG_NO(IN ma_tai_khoan VARCHAR(50), loai_tien_id INTEGER,
																									chi_nhanh_id INTEGER, doi_tuong_id INTEGER)
							RETURNS TABLE("ID_CHUNG_TU"     INTEGER,
											"MODEL_CHUNG_TU" VARCHAR(50),
											"DOI_TUONG_ID"    INTEGER,
											"SO_TAI_KHOAN"    VARCHAR(20),
											"NGAY_HOA_DON"    DATE,
											"SO_HOA_DON"      VARCHAR(50),
											"SO_TIEN"         FLOAT,
											"SO_TIEN_QUY_DOI" FLOAT,
											"TY_GIA"          FLOAT
							) AS $$
							DECLARE

							BEGIN

							DROP TABLE IF EXISTS TBL_KET_QUA;
							CREATE TEMP TABLE TBL_KET_QUA (
								"ID_CHUNG_TU"     INTEGER,
								"MODEL_CHUNG_TU" VARCHAR(50),
								"DOI_TUONG_ID"    INTEGER,
								"SO_TAI_KHOAN"    VARCHAR(20),
								"NGAY_HOA_DON"    DATE,
								"SO_HOA_DON"      VARCHAR(20),
								"SO_TIEN"         FLOAT,
								"SO_TIEN_QUY_DOI" FLOAT,
								"TY_GIA"          FLOAT
							);
							INSERT INTO TBL_KET_QUA (
								SELECT
								A."ID_CHUNG_TU",
								A."MODEL_CHUNG_TU",
								A."DOI_TUONG_ID",
								A."SO_TAI_KHOAN",
								A."NGAY_HOA_DON",
								coalesce(A."SO_HOA_DON", ''),
								sum(coalesce(A."SO_TIEN", 0))         AS "SO_TIEN",
								sum(coalesce(A."SO_TIEN_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI",
								A."TY_GIA"
								FROM (
									SELECT
										cast(GL."ID_CHUNG_TU_CONG_NO" AS INTEGER)      AS "ID_CHUNG_TU",
										"MODEL_CHUNG_TU_CONG_NO"                       AS "MODEL_CHUNG_TU",
										Gl."DOI_TUONG_ID"                              AS "DOI_TUONG_ID",
										TA."SO_TAI_KHOAN",
										(CASE WHEN GL."LOAI_CHUNG_TU_CONG_NO" IN
													(610, 612, 613, 614, 620, 330, 331, 332, 333, 334, 352, 357, 358, 359, 360, 362, 363, 364, 365, 366, 368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
										THEN GL."NGAY_HOA_DON_CONG_NO"
										ELSE NULL
										END)                                          AS "NGAY_HOA_DON",
										(CASE WHEN GL."LOAI_CHUNG_TU_CONG_NO" IN (610, 612,
																						613, 614, 620,
																						330, 331, 332,
																						333, 334, 352,
										357, 358, 359, 360, 362, 363, 364, 365, 366, 368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
										THEN coalesce(GL."SO_HOA_DON_CONG_NO", '')
										ELSE NULL
										END)                                          AS "SO_HOA_DON",
										SUM(coalesce(GL."SO_CONG_NO_THANH_TOAN_LAN_NAY", 0))         AS "SO_TIEN",
										SUM(coalesce(GL."SO_CONG_NO_THANH_TOAN_LAN_NAY_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI",
										GL."TY_GIA_CONG_NO"                            AS "TY_GIA"
									FROM sale_ex_doi_tru_chi_tiet GL
										INNER JOIN (SELECT *
													FROM danh_muc_he_thong_tai_khoan A
													WHERE A."SO_TAI_KHOAN" = ma_tai_khoan) TA ON TA.id = GL."TAI_KHOAN_ID"
									WHERE GL."currency_id" = loai_tien_id
											AND GL."CHI_NHANH_ID" = (chi_nhanh_id)
											AND GL."CTTT_DA_GHI_SO" = TRUE
											AND GL."CTCN_DA_GHI_SO" = TRUE
											AND (GL."DOI_TUONG_ID" = doi_tuong_id
												OR doi_tuong_id IS NULL
											)
									GROUP BY GL."ID_CHUNG_TU_CONG_NO",
										GL."DOI_TUONG_ID",
										TA."SO_TAI_KHOAN",
										GL."SO_HOA_DON_CONG_NO",
										GL."NGAY_HOA_DON_CONG_NO",
										GL."LOAI_CHUNG_TU_CONG_NO"
										, GL."TY_GIA_CONG_NO"
										, GL."MODEL_CHUNG_TU_CONG_NO"


									UNION ALL


									SELECT
										GLD."ID_CHUNG_TU_GOC",
										"MODEL_CHUNG_TU_GOC"                      AS "MODEL_CHUNG_TU",
										GLD."DOI_TUONG_ID",
										TA."SO_TAI_KHOAN",
										(CASE WHEN GLD."LOAI_CHUNG_TU" IN
													('610', '612', '613', '614', '620', '330', '331', '332', '333', '334', '352', '357', '358', '359', '360', '362', '363', '364', '365', '366', '368', '369', '370', '371', '372', '374', '375', '376', '377', '378')
										THEN GL."NGAY_CHUNG_TU"
										ELSE NULL
										END)                                     AS "NGAY_HOA_DON",
										(CASE WHEN GLD."LOAI_CHUNG_TU" IN
													('610', '612', '613', '614', '620', '330', '331', '332', '333', '334', '352', '357', '358', '359', '360', '362', '363', '364', '365', '366', '368', '369', '370', '371', '372', '374', '375', '376', '377', '378')
										THEN coalesce(GL."SO_HOA_DON", '')
										ELSE NULL
										END)                                     AS "SO_HOA_DON",
										0                                         AS "SO_TIEN",
										(-1) * SUM(coalesce(GLD."CHENH_LECH", 0)) AS "SO_TIEN_QUY_DOI",
										GL."TY_GIA"
									FROM account_ex_chung_tu_nghiep_vu_khac GL
										INNER JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan GLD ON GLD."ID_CHUNG_TU_GOC" = GL.id
										INNER JOIN (SELECT *
													FROM danh_muc_he_thong_tai_khoan A
													WHERE A."SO_TAI_KHOAN" = ma_tai_khoan) TA ON GLD."TK_CONG_NO_ID" = TA.id
									WHERE GL.currency_id = loai_tien_id
											AND Gl."CHI_NHANH_ID" = (chi_nhanh_id)
											AND (GLD."DOI_TUONG_ID" = doi_tuong_id
												OR doi_tuong_id IS NULL
											)
									GROUP BY GLD."ID_CHUNG_TU_GOC",
										GLD."DOI_TUONG_ID",
										TA."SO_TAI_KHOAN",
										GL."NGAY_CHUNG_TU",
										GLD."LOAI_CHUNG_TU"
										, GL."TY_GIA",
										GL."SO_HOA_DON"
										, GLD."MODEL_CHUNG_TU_GOC"

									UNION ALL

									SELECT
										PUD."CHUNG_TU_MUA_HANG"                          AS "ID_CHUNG_TU",
										'purchase_document'                              AS "MODEL_CHUNG_TU",
										PUV."DOI_TUONG_ID",
										TA."SO_TAI_KHOAN",
										(CASE WHEN PUV."LOAI_CHUNG_TU" IN
													(610, 612, 613, 614, 620, 330, 331, 332, 333, 334, 352, 357, 358, 359, 360, 362, 363, 364, 365, 366, 368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
										THEN PUD."NGAY_HD_MUA_HANG"
										ELSE NULL
										END)                                            AS NGAY_HOA_DON,
										(CASE WHEN PUV."LOAI_CHUNG_TU" IN (610, 612, 613,
																				614, 620, 330,
																				331, 332, 333,
																				334, 352, 357,
																						358, 359, 360,
																						362, 363, 364,
																						365, 366, 368,
																			369, 370, 371,
																			372, 374, 375,
																			376, 377, 378)
										THEN coalesce(PUD."SO_HD_MUA_HANG", '')
										ELSE NULL
										END)                                            AS "SO_HOA_DON",
										SUM(coalesce(PUD."THANH_TIEN", 0)
											+ coalesce(PUD."TIEN_THUE_GTGT", 0))         AS "SO_TIEN",
										SUM(coalesce(PUD."THANH_TIEN_QUY_DOI", 0)
											+ coalesce(PUD."TIEN_THUE_GTGT_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI",
										PUV."TY_GIA"
									FROM purchase_ex_tra_lai_hang_mua PUV
										INNER JOIN purchase_ex_tra_lai_hang_mua_chi_tiet PUD ON PUD."CHUNG_TU_TRA_LAI_HANG_MUA_ID" = PUV.id
										INNER JOIN (SELECT *
													FROM danh_muc_he_thong_tai_khoan A
													WHERE A."SO_TAI_KHOAN" = ma_tai_khoan) TA ON PUD."TK_CO_ID" = TA.id
									WHERE PUV.currency_id = loai_tien_id
											AND PUV."CHI_NHANH_ID" = (chi_nhanh_id)
											AND PUV.state = 'da_ghi_so'
											AND PUD."CHUNG_TU_MUA_HANG" IS NOT NULL
											AND (PUV."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id IS NULL)
									GROUP BY PUD."CHUNG_TU_MUA_HANG",
										PUV."DOI_TUONG_ID",
										TA."SO_TAI_KHOAN"
										, PUV."TY_GIA"
										, PUV."LOAI_CHUNG_TU"
										, "NGAY_HD_MUA_HANG"
										, "SO_HD_MUA_HANG"


									UNION ALL

									SELECT
										PUD."CHUNG_TU_MUA_HANG"                          AS "ID_CHUNG_TU",
										'purchase_document'                              AS "MODEL_CHUNG_TU",
										PUV."DOI_TUONG_ID",
										TA."SO_TAI_KHOAN",
										(CASE WHEN PUV."LOAI_CHUNG_TU" IN (610, 612, 613,
																				614, 620, 330,
																				331, 332, 333,
																				334, 352, 357,
																						358, 359, 360,
																						362, 363, 364,
																						365, 366, 368,
																			369, 370, 371,
																			372, 374, 375,
																			376, 377, 378)
										THEN PUD."NGAY_HD_MUA_HANG"
										ELSE NULL
										END)                                            AS "NGAY_HOA_DON",
										(CASE WHEN PUV."LOAI_CHUNG_TU" IN (610, 612, 613,
																				614, 620, 330,
																				331, 332, 333,
																				334, 352, 357,
																						358, 359, 360,
																						362, 363, 364,
																						365, 366, 368,
																			369, 370, 371,
																			372, 374, 375,
																			376, 377, 378)
										THEN coalesce(PUD."SO_HD_MUA_HANG", '')
										ELSE NULL
										END)                                            AS "SO_HOA_DON",
										SUM(coalesce(PUD."THANH_TIEN", 0)
											+ coalesce(PUD."TIEN_THUE_GTGT", 0))         AS "SO_TIEN",
										SUM(coalesce(PUD."THANH_TIEN_QUY_DOI", 0)
											+ coalesce(PUD."TIEN_THUE_GTGT_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI",
										PUV."TY_GIA"
									FROM purchase_ex_giam_gia_hang_mua PUV
										INNER JOIN purchase_ex_giam_gia_hang_mua_chi_tiet PUD ON PUD."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID" = PUV.id
										INNER JOIN (SELECT *
													FROM danh_muc_he_thong_tai_khoan A
													WHERE A."SO_TAI_KHOAN" = ma_tai_khoan) TA ON PUD."TK_CO_ID" = TA.id
									WHERE PUV.currency_id = loai_tien_id
											AND PUV."CHI_NHANH_ID" = (chi_nhanh_id)
											AND PUV.state = 'da_ghi_so'
											AND PUD."CHUNG_TU_MUA_HANG" IS NOT NULL
											AND (PUV."DOI_TUONG_ID" = doi_tuong_id
												OR doi_tuong_id IS NULL
											)
									GROUP BY PUD."CHUNG_TU_MUA_HANG",
										PUV."DOI_TUONG_ID",
										TA."SO_TAI_KHOAN"
										, PUV."TY_GIA"
										, "LOAI_CHUNG_TU"
										, "NGAY_HD_MUA_HANG"
										, "SO_HD_MUA_HANG"
									) AS A
								GROUP BY
								A."ID_CHUNG_TU",
								A."MODEL_CHUNG_TU",
								A."DOI_TUONG_ID",
								A."SO_TAI_KHOAN",
								A."NGAY_HOA_DON",
								A."SO_HOA_DON",
								A."TY_GIA"
							);
							RETURN QUERY SELECT *
										FROM TBL_KET_QUA;
							END;
							$$ LANGUAGE PLpgSQL;
		""")

			# Func_SA_GetPaiedAmountForDebtVoucher - Funtion lấy số tiền đã thu của các chứng từ công nợ
			self.env.cr.execute(""" 
			-- DROP FUNCTION SA_LAY_SO_TIEN_DA_THU_CUA_CHUNG_TU_CONG_NO(IN ma_tai_khoan VARCHAR(50),loai_tien_id INTEGER,chi_nhanh_id INTEGER,doi_tuong_id INTEGER)
				CREATE OR REPLACE FUNCTION SA_LAY_SO_TIEN_DA_THU_CUA_CHUNG_TU_CONG_NO(IN ma_tai_khoan VARCHAR(50), loai_tien_id INTEGER,
																			chi_nhanh_id INTEGER, doi_tuong_id INTEGER)
				RETURNS TABLE("ID_CHUNG_TU"     INTEGER,
								"MODEL_CHUNG_TU" VARCHAR(50),
								"DOI_TUONG_ID"    INTEGER,
								"SO_TAI_KHOAN"    VARCHAR(20),
								"NGAY_HOA_DON"    DATE,
								"SO_HOA_DON"      VARCHAR(50),
								"SO_TIEN"         FLOAT,
								"SO_TIEN_QUY_DOI" FLOAT,
								"TY_GIA"          FLOAT
				) AS $$
				DECLARE

				BEGIN

				DROP TABLE IF EXISTS TBL_KET_QUA;
				CREATE TEMP TABLE TBL_KET_QUA (
					"ID_CHUNG_TU"     INTEGER,
					"MODEL_CHUNG_TU" VARCHAR(50),
					"DOI_TUONG_ID"    INTEGER,
					"SO_TAI_KHOAN"    VARCHAR(20),
					"NGAY_HOA_DON"    DATE,
					"SO_HOA_DON"      VARCHAR(20),
					"SO_TIEN"         FLOAT,
					"SO_TIEN_QUY_DOI" FLOAT,
					"TY_GIA"          FLOAT
				);
				INSERT INTO TBL_KET_QUA (
					SELECT
						A."ID_CHUNG_TU",
						A."MODEL_CHUNG_TU",
						A."DOI_TUONG_ID",
						A."SO_TAI_KHOAN",
						A."NGAY_HOA_DON",
						A."SO_HOA_DON",
						sum(coalesce(A."SO_TIEN", 0))         AS "SO_TIEN",
						sum(coalesce(A."SO_TIEN_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI",
						A."TY_GIA"
					FROM (
							SELECT
							cast(GL."ID_CHUNG_TU_CONG_NO" AS INTEGER)      AS "ID_CHUNG_TU",
							GL."MODEL_CHUNG_TU_CONG_NO" AS "MODEL_CHUNG_TU",
							Gl."DOI_TUONG_ID"                              AS "DOI_TUONG_ID",
							TA."SO_TAI_KHOAN",
							(CASE WHEN GL."LOAI_CHUNG_TU_CONG_NO" IN
										(610, 612, 613, 614, 620, 330, 331, 332, 333, 334, 352, 357, 358, 359, 360, 362, 363, 364, 365, 366, 368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
								THEN GL."NGAY_HOA_DON_CONG_NO"
								ELSE NULL
								END)                                          AS "NGAY_HOA_DON",
							(CASE WHEN GL."LOAI_CHUNG_TU_CONG_NO" IN (610, 612,
																			613, 614, 620,
																			330, 331, 332,
																			333, 334, 352,
								357, 358, 359, 360, 362, 363, 364, 365, 366, 368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
								THEN coalesce(GL."SO_HOA_DON_CONG_NO", '')
								ELSE NULL
								END)                                          AS "SO_HOA_DON",
							SUM(coalesce(GL."SO_CONG_NO_THANH_TOAN_LAN_NAY", 0))         AS "SO_TIEN",
							SUM(coalesce(GL."SO_CONG_NO_THANH_TOAN_LAN_NAY_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI",
							GL."TY_GIA_CONG_NO"                            AS "TY_GIA"
							FROM sale_ex_doi_tru_chi_tiet GL
							INNER JOIN (SELECT *
										FROM danh_muc_he_thong_tai_khoan A
										WHERE A."SO_TAI_KHOAN" = '131') TA ON TA.id = GL."TAI_KHOAN_ID"
							WHERE GL."currency_id" = loai_tien_id
								AND GL."CHI_NHANH_ID" = (chi_nhanh_id)
								AND GL."CTTT_DA_GHI_SO" = TRUE
								AND GL."CTCN_DA_GHI_SO" = TRUE
								AND (GL."DOI_TUONG_ID" = doi_tuong_id
										OR doi_tuong_id IS NULL
								)
							GROUP BY GL."ID_CHUNG_TU_CONG_NO",
							GL."DOI_TUONG_ID",
							GL."MODEL_CHUNG_TU_CONG_NO",
							TA."SO_TAI_KHOAN",
							GL."SO_HOA_DON_CONG_NO",
							GL."NGAY_HOA_DON_CONG_NO",
							GL."LOAI_CHUNG_TU_CONG_NO"
							, GL."TY_GIA_CONG_NO"


							UNION ALL


							SELECT
							GLD."ID_CHUNG_TU_GOC",
							GLD."MODEL_CHUNG_TU_GOC" AS "MODEL_CHUNG_TU",
							GLD."DOI_TUONG_ID",
							TA."SO_TAI_KHOAN",
							(CASE WHEN GLD."LOAI_CHUNG_TU" IN
										('610', '612', '613', '614', '620', '330', '331', '332', '333', '334', '352', '357', '358', '359', '360', '362', '363', '364', '365', '366', '368', '369', '370', '371', '372', '374', '375', '376', '377', '378')
								THEN GL."NGAY_CHUNG_TU"
								ELSE NULL
								END)                                     AS "NGAY_HOA_DON",
							(CASE WHEN GLD."LOAI_CHUNG_TU" IN
										('610', '612', '613', '614', '620', '330', '331', '332', '333', '334', '352', '357', '358', '359', '360', '362', '363', '364', '365', '366', '368', '369', '370', '371', '372', '374', '375', '376', '377', '378')
								THEN coalesce(GL."SO_HOA_DON", '')
								ELSE NULL
								END)                                     AS "SO_HOA_DON",
							0                                         AS "SO_TIEN",
							(-1) * SUM(coalesce(GLD."CHENH_LECH", 0)) AS "SO_TIEN_QUY_DOI",
							GL."TY_GIA"
							FROM account_ex_chung_tu_nghiep_vu_khac GL
							INNER JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan GLD ON GLD."CHUNG_TU_NGHIEP_VU_KHAC_ID" = GL.id
							INNER JOIN (SELECT *
										FROM danh_muc_he_thong_tai_khoan A
										WHERE A."SO_TAI_KHOAN" = '131') TA ON GLD."TK_CONG_NO_ID" = TA.id
							WHERE GL.currency_id = loai_tien_id
								AND Gl."CHI_NHANH_ID" = chi_nhanh_id
								AND (GLD."DOI_TUONG_ID" = doi_tuong_id
										OR doi_tuong_id IS NULL
								)
							GROUP BY GLD."ID_CHUNG_TU_GOC",
							GLD."DOI_TUONG_ID",
							TA."SO_TAI_KHOAN",
							GL."NGAY_CHUNG_TU",
							GLD."LOAI_CHUNG_TU"
							, GL."TY_GIA",
							GL."SO_HOA_DON",
							GLD."MODEL_CHUNG_TU_GOC"

							UNION ALL

							SELECT
							SAD."SO_CHUNG_TU_ID"                         AS "ID_CHUNG_TU",
							'sale.document' AS "MODEL_CHUNG_TU",
							SA."DOI_TUONG_ID",
							TA."SO_TAI_KHOAN",
							NULL                                              AS "NGAY_HOA_DON",
							NULL                                              AS "SO_HOA_DON",
							SUM(coalesce(SAD."THANH_TIEN", 0)
								+ coalesce(SAD."TIEN_THUE_GTGT", 0)
								- coalesce(SAD."TIEN_CHIET_KHAU", 0))         AS "SO_TIEN",
							SUM(coalesce(SAD."THANH_TIEN_QUY_DOI", 0)
								+ coalesce(SAD."TIEN_THUE_GTGT_QUY_DOI", 0)
								- coalesce(SAD."TIEN_CHIET_KHAU_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI",
							SA."TY_GIA"
							FROM sale_ex_tra_lai_hang_ban SA
							INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet SAD ON SAD."TRA_LAI_HANG_BAN_ID" = SA.id
							INNER JOIN (SELECT *
										FROM danh_muc_he_thong_tai_khoan A
										WHERE A."SO_TAI_KHOAN" = '131') TA ON SAD."TK_CO_ID" = TA.id
							WHERE SA.currency_id = loai_tien_id
								AND SA."CHI_NHANH_ID" = chi_nhanh_id
								AND SA.state = 'da_ghi_so'
								AND SAD."SO_CHUNG_TU_ID" IS NOT NULL
								AND (SA."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id IS NULL)
							GROUP BY SAD."SO_CHUNG_TU_ID",
							SA."DOI_TUONG_ID",
							TA."SO_TAI_KHOAN"
							, SA."TY_GIA"


							UNION ALL

							SELECT
							SAD."CHUNG_TU_BAN_HANG_ID"                        AS "ID_CHUNG_TU",
							'sale.document' AS "MODEL_CHUNG_TU",
							SA."DOI_TUONG_ID",
							TA."SO_TAI_KHOAN",
							NULL                                              AS "NGAY_HOA_DON",
							NULL                                              AS "SO_HOA_DON",
							SUM(coalesce(SAD."THANH_TIEN", 0)
								+ coalesce(SAD."TIEN_THUE_GTGT", 0)
								- coalesce(SAD."TIEN_CHIET_KHAU", 0))         AS "SO_TIEN",
							SUM(coalesce(SAD."THANH_TIEN_QUY_DOI", 0)
								+ coalesce(SAD."TIEN_THUE_GTGT_QUY_DOI", 0)
								- coalesce(SAD."TIEN_CHIET_KHAU_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI",
							SA."TY_GIA"
							FROM sale_ex_giam_gia_hang_ban SA
							INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban SAD ON SAD."GIAM_GIA_HANG_BAN_ID" = SA.id
							INNER JOIN (SELECT *
										FROM danh_muc_he_thong_tai_khoan A
										WHERE A."SO_TAI_KHOAN" = '131') TA ON SAD."TK_CO_ID" = TA.id
							WHERE SA.currency_id = loai_tien_id
								AND SA."CHI_NHANH_ID" = chi_nhanh_id
								AND SA.state = 'da_ghi_so'
								AND SAD."CHUNG_TU_BAN_HANG_ID" IS NOT NULL
								AND (SA."DOI_TUONG_ID" = doi_tuong_id
										OR doi_tuong_id IS NULL
								)
							GROUP BY SAD."CHUNG_TU_BAN_HANG_ID",
							SA."DOI_TUONG_ID",
							TA."SO_TAI_KHOAN"
							, SA."TY_GIA"
						) AS A
					GROUP BY
						A."ID_CHUNG_TU",
						A."MODEL_CHUNG_TU",
						A."DOI_TUONG_ID",
						A."SO_TAI_KHOAN",
						A."NGAY_HOA_DON",
						A."SO_HOA_DON",
						A."TY_GIA"
				);
				RETURN QUERY SELECT *
							FROM TBL_KET_QUA;
				END;
				$$ LANGUAGE PLpgSQL;

		""")