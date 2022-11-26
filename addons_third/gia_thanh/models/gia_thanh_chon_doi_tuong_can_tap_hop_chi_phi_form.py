# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_CHON_DOI_TUONG_CAN_TAP_HOP_CHI_PHI_FORM(models.Model):
	_name = 'gia.thanh.chon.doi.tuong.can.tap.hop.chi.phi.form'
	_description = ''
	_auto = False

	name = fields.Char(string='Name', help='Name', oldname='NAME')
	#FIELD_IDS = fields.One2many('model.name')
	#@api.model
	#def default_get(self, fields_list):
	#   result = super(GIA_THANH_CHON_DOI_TUONG_CAN_TAP_HOP_CHI_PHI_FORM, self).default_get(fields_list)
	#   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
	#   return result
	GIA_THANH_CHON_DOI_TUONG_CAN_TAP_HOP_CHI_PHI_CHI_TIET_IDS = fields.One2many('gia.thanh.chon.doi.tuong.can.tap.hop.chi.phi.chi.tiet', 'CHI_TIET_ID', string='Chọn đối tượng cần tập hợp chi phí chi tiết')

	def lay_du_lieu_doi_tuong_thcp_hang_hoa_loai_san_pham(self, args):
		new_line = [[5]]
		chi_nhanh_id = self.get_chi_nhanh()
		doi_tuong_thcp_loai_san_pham = self.lay_du_lieu_ky_gia_thanh_chi_tiet(0,chi_nhanh_id)
		if doi_tuong_thcp_loai_san_pham :
			for doi_tuong in doi_tuong_thcp_loai_san_pham:
				new_line += [(0,0,{
						'MA_SAN_PHAM_ID': [doi_tuong.get('DOI_TUONG_THCP_ID'),doi_tuong.get('MA_DOI_TUONG_THCP')],
						'TEN_SAN_PHAM' : doi_tuong.get('TEN_DOI_TUONG_THCP'),
						'LOAI' : '1',
						})]
		return {'GIA_THANH_CHON_DOI_TUONG_CAN_TAP_HOP_CHI_PHI_CHI_TIET_IDS': new_line}

	def lay_du_lieu_doi_tuong_thcp_hang_hoa_loai_phan_xuong(self, args):
		new_line = [[5]]
		chi_nhanh_id = self.get_chi_nhanh()
		doi_tuong_thcp_loai_phan_xuong = self.lay_du_lieu_ky_gia_thanh_chi_tiet(1,chi_nhanh_id)
		if doi_tuong_thcp_loai_phan_xuong :
			for doi_tuong in doi_tuong_thcp_loai_phan_xuong:
				new_line += [(0,0,{
						'MA_SAN_PHAM_ID': [doi_tuong.get('DOI_TUONG_THCP_ID'), doi_tuong.get('MA_DOI_TUONG_THCP')],
						'TEN_SAN_PHAM' : doi_tuong.get('TEN_DOI_TUONG_THCP'),
						'LOAI' : '0',
						})]
		return {'GIA_THANH_CHON_DOI_TUONG_CAN_TAP_HOP_CHI_PHI_CHI_TIET_IDS': new_line}
	
	def lay_du_lieu_doi_tuong_thcp_cong_trinh(self, args):
		new_line = [[5]]
		chi_nhanh_id = self.get_chi_nhanh()
		doi_tuong_thcp_cong_trinh = self.lay_du_lieu_ky_gia_thanh_chi_tiet(3,chi_nhanh_id)
		if doi_tuong_thcp_cong_trinh :
			for doi_tuong in doi_tuong_thcp_cong_trinh:
				new_line += [(0,0,{
						'MA_CONG_TRINH_ID': [doi_tuong.get('CONG_TRINH_ID'), doi_tuong.get('MA_CONG_TRINH')],
						'TEN_CONG_TRINH' : doi_tuong.get('TEN_CONG_TRINH'),
						'LOAI_CONG_TRINH' : [doi_tuong.get('LOAI_CONG_TRINH_ID'),doi_tuong.get('LOAI_CONG_TRINH')],
						})]
		return {'GIA_THANH_CHON_DOI_TUONG_CAN_TAP_HOP_CHI_PHI_CHI_TIET_IDS': new_line}
	
	def lay_du_lieu_doi_tuong_thcp_don_hang(self, args):
		new_line = [[5]]
		chi_nhanh_id = self.get_chi_nhanh()
		doi_tuong_thcp_don_hang = self.lay_du_lieu_ky_gia_thanh_chi_tiet(4,chi_nhanh_id)
		if doi_tuong_thcp_don_hang :
			for doi_tuong in doi_tuong_thcp_don_hang:
				new_line += [(0,0,{
						'SO_DON_HANG_ID': [doi_tuong.get('DON_DAT_HANG_ID'), doi_tuong.get('SO_CHUNG_TU')],
						'NGAY_DON_HANG' : doi_tuong.get('NGAY_CHUNG_TU'),
						'KHACH_HANG' : doi_tuong.get('TEN_KHACH_HANG'),
						})]
		return {'GIA_THANH_CHON_DOI_TUONG_CAN_TAP_HOP_CHI_PHI_CHI_TIET_IDS': new_line}
	
	def lay_du_lieu_doi_tuong_thcp_hop_dong(self, args):
		new_line = [[5]]
		chi_nhanh_id = self.get_chi_nhanh()
		doi_tuong_thcp_hop_dong = self.lay_du_lieu_ky_gia_thanh_chi_tiet(5,chi_nhanh_id)
		if doi_tuong_thcp_hop_dong :
			for doi_tuong in doi_tuong_thcp_hop_dong:
				new_line += [(0,0,{
						'SO_HOP_DONG_ID': [doi_tuong.get('HOP_DONG_ID'), doi_tuong.get('SO_HOP_DONG')],
						'NGAY_HOP_DONG' : doi_tuong.get('NGAY_KY'),
						'TRICH_YEU' : doi_tuong.get('TRICH_YEU'),
						'KHACH_HANG' : doi_tuong.get('KHACH_HANG'),
						})]
		return {'GIA_THANH_CHON_DOI_TUONG_CAN_TAP_HOP_CHI_PHI_CHI_TIET_IDS': new_line}

	
	def lay_du_lieu_ky_gia_thanh_chi_tiet(self,loai_giam_gia_thanh,chi_nhanh_id):
		params = {
			'LOAI_GIAM_GIA_THANH' : loai_giam_gia_thanh,
			'CHI_NHANH_ID' : chi_nhanh_id,
			}
		query = """   

				DO LANGUAGE plpgsql $$
					DECLARE

					LOAI_GIA_THANH   INT:= %(LOAI_GIAM_GIA_THANH)s ;

					ds_da_chon   VARCHAR:=';' ;

					chi_nhanh_id    INT:= %(CHI_NHANH_ID)s;

					bao_gom_chi_nhanh_phu_thuoc    INT:=1;

					rec       RECORD;


			BEGIN


				DROP TABLE IF EXISTS TMP_KET_QUA
				;

				CREATE TEMP TABLE TMP_KET_QUA

				(
					"DOI_TUONG_THCP_ID"   INT,
					"MA_DOI_TUONG_THCP"   VARCHAR(25),
					"TEN_DOI_TUONG_THCP"  VARCHAR(255),
					"LOAI_DOI_TUONG_THCP" VARCHAR(255),
					"CONG_TRINH_ID"       INT,
					"MA_CONG_TRINH"       VARCHAR(20),
					"TEN_CONG_TRINH"      VARCHAR(255),
					"LOAI_CONG_TRINH_ID"     VARCHAR(255),
					"LOAI_CONG_TRINH"     VARCHAR(255),
					"DON_DAT_HANG_ID"     INT,
					"SO_CHUNG_TU"         VARCHAR(25),
					"NGAY_CHUNG_TU"       TIMESTAMP,
					"TEN_KHACH_HANG"      VARCHAR(255),
					"HOP_DONG_ID"         INT,
					"SO_HOP_DONG"         VARCHAR(50),
					"NGAY_KY"             TIMESTAMP,
					"TRICH_YEU"           VARCHAR(255),
					"KHACH_HANG"          VARCHAR(255),
					"CHI_NHANH_ID"        INT,
					"MA_PHAN_CAP"         VARCHAR(255)

				)
				;

				-- Sản xuất liên tục giản đơn
				IF LOAI_GIA_THANH = 0
				THEN
					INSERT INTO TMP_KET_QUA
					("DOI_TUONG_THCP_ID",
					"MA_DOI_TUONG_THCP",
					"TEN_DOI_TUONG_THCP",
					"LOAI_DOI_TUONG_THCP",

					"CHI_NHANH_ID"
					)
						SELECT
							"id"
							, "MA_DOI_TUONG_THCP"
							, "TEN_DOI_TUONG_THCP"
							, "LOAI"
							, "CHI_NHANH_ID"
						FROM danh_muc_doi_tuong_tap_hop_chi_phi J
							LEFT JOIN CHUYEN_CHUOI_CAC_GUI_THANH_BANG_CHUA_CAC_GUI(ds_da_chon,
																				';') F ON J."id" = F.Value
						WHERE F.Value IS NULL
							AND "LOAI" = '1' --Sản phẩm
							AND "parent_id" IS NULL -- Không thuộc công đoạn nào
							AND J."active" = TRUE
							AND (J."CHI_NHANH_ID" = chi_nhanh_id
								OR (bao_gom_chi_nhanh_phu_thuoc = 1
									AND J."CHI_NHANH_ID" IN (
							SELECT OU."id"
							FROM danh_muc_to_chuc OU
							WHERE OU."parent_id" = chi_nhanh_id
								AND "HACH_TOAN_SELECTION" = 'PHU_THUOC')
								)
								OR (chi_nhanh_id IS NULL)
							)
						ORDER BY J."MA_PHAN_CAP"
					;
				END IF
				;

				-- Sản xuất liên tục hệ số tỷ lệ
				IF LOAI_GIA_THANH = 1
				THEN
					INSERT INTO TMP_KET_QUA
					("DOI_TUONG_THCP_ID",
					"MA_DOI_TUONG_THCP",
					"TEN_DOI_TUONG_THCP",
					"LOAI_DOI_TUONG_THCP",
					"MA_PHAN_CAP",
					"CHI_NHANH_ID"
					)
						SELECT
							"id"
							, "MA_DOI_TUONG_THCP"
							, "TEN_DOI_TUONG_THCP"
							, "LOAI"
							, "MA_PHAN_CAP"
							, "CHI_NHANH_ID"
						FROM danh_muc_doi_tuong_tap_hop_chi_phi J
							LEFT JOIN CHUYEN_CHUOI_CAC_GUI_THANH_BANG_CHUA_CAC_GUI(ds_da_chon,
																				';') F ON J."id" = F.Value
						WHERE F.Value IS NULL
							AND "LOAI" = '0' -- Phân xưởng
							AND J."active" = TRUE
							AND (J."CHI_NHANH_ID" = chi_nhanh_id
								OR (bao_gom_chi_nhanh_phu_thuoc = 1
									AND J."CHI_NHANH_ID" IN (
							SELECT OU."id"
							FROM danh_muc_to_chuc OU
							WHERE OU."parent_id" = chi_nhanh_id
								AND "HACH_TOAN_SELECTION" = 'PHU_THUOC')
								)
								OR (chi_nhanh_id IS NULL)
							)
						ORDER BY J."MA_PHAN_CAP"
					;
				END IF
				;

				-- Sản xuất l iên tục phân cấp
				IF LOAI_GIA_THANH = 2
				THEN
					INSERT INTO TMP_KET_QUA
					("DOI_TUONG_THCP_ID",
					"MA_DOI_TUONG_THCP",
					"TEN_DOI_TUONG_THCP",
					"LOAI_DOI_TUONG_THCP",
					"MA_PHAN_CAP",
					"CHI_NHANH_ID"
					)
						SELECT
							"id"
							, "MA_DOI_TUONG_THCP"
							, "TEN_DOI_TUONG_THCP"
							, "LOAI"
							, "MA_PHAN_CAP"
							, "CHI_NHANH_ID"
						FROM danh_muc_doi_tuong_tap_hop_chi_phi J
							LEFT JOIN CHUYEN_CHUOI_CAC_GUI_THANH_BANG_CHUA_CAC_GUI(ds_da_chon,
																				';') F ON J."id" = F.Value
						WHERE F.Value IS NULL
							AND "LOAI" = '2'  --  quy trình
							AND J."active" = TRUE
							AND (J."CHI_NHANH_ID" = chi_nhanh_id
								OR (bao_gom_chi_nhanh_phu_thuoc = 1
									AND J."CHI_NHANH_ID" IN (
							SELECT OU."id"
							FROM danh_muc_to_chuc OU
							WHERE OU."parent_id" = chi_nhanh_id
								AND "HACH_TOAN_SELECTION" = 'PHU_THUOC')
								)
								OR (chi_nhanh_id IS NULL)
							)
						ORDER BY J."MA_PHAN_CAP"
					;
				END IF
				;

				-- Công trình vụ việc
				IF LOAI_GIA_THANH = 3
				THEN


					INSERT INTO TMP_KET_QUA
					("CONG_TRINH_ID",
					"MA_CONG_TRINH",
					"TEN_CONG_TRINH",
					"LOAI_CONG_TRINH_ID",
					"LOAI_CONG_TRINH",
					"CHI_NHANH_ID",


					"MA_PHAN_CAP"

					)
						SELECT
							P."id"
							, "MA_CONG_TRINH"
							, "TEN_CONG_TRINH"
							, "LOAI_CONG_TRINH"
							, PC.name
							, "CHI_NHANH_ID"
							, "MA_PHAN_CAP"

						FROM danh_muc_cong_trinh P
							LEFT JOIN danh_muc_loai_cong_trinh PC ON PC."id" = P."LOAI_CONG_TRINH"
							LEFT JOIN CHUYEN_CHUOI_CAC_GUI_THANH_BANG_CHUA_CAC_GUI(ds_da_chon,
																				';') F ON P."id" = F.Value
						WHERE ((F.Value IS NULL)
							-- Vẫn phải lấy các node cha còn có con lên mặc dù cha đã được chọn ở chỗ khác
							OR (F.Value IS NOT NULL
								AND P."isparent" = TRUE
								AND EXISTS(SELECT "id"
											FROM danh_muc_cong_trinh PW
											WHERE PW."parent_id" = F.Value
													AND NOT EXISTS(SELECT Value
																FROM
																			CHUYEN_CHUOI_CAC_GUI_THANH_BANG_CHUA_CAC_GUI(
																				ds_da_chon,
																				';') FT
																WHERE
																	FT.Value = PW."id"))
							)
							)
							AND P."active" = TRUE
							AND (P."CHI_NHANH_ID" = chi_nhanh_id
								OR (bao_gom_chi_nhanh_phu_thuoc = 1
									AND P."CHI_NHANH_ID" IN (
							SELECT "CHI_NHANH_ID"
							FROM danh_muc_to_chuc OU
							WHERE OU."parent_id" = chi_nhanh_id
								AND "HACH_TOAN_SELECTION" = 'PHU_THUOC')
								)
								OR (chi_nhanh_id IS NULL)
							)
						ORDER BY P."MA_PHAN_CAP",
							P."MA_CONG_TRINH",
							P."TEN_CONG_TRINH"
					;
				END IF
				;

				-- Đơn hàng
				IF LOAI_GIA_THANH = 4
				THEN
					INSERT INTO TMP_KET_QUA
					("DON_DAT_HANG_ID",
					"SO_CHUNG_TU",
					"NGAY_CHUNG_TU",
					"TEN_KHACH_HANG",
					"CHI_NHANH_ID"
					)
						SELECT
							"id"
							, "SO_DON_HANG"
							, "NGAY_DON_HANG"
							, "TEN_KHACH_HANG"
							, "CHI_NHANH_ID"
						FROM account_ex_don_dat_hang S
							LEFT JOIN CHUYEN_CHUOI_CAC_GUI_THANH_BANG_CHUA_CAC_GUI(ds_da_chon,
																				';' :: VARCHAR) F ON S."id" = F.Value
						WHERE F.Value IS NULL
							AND (S."TINH_GIA_THANH" = TRUE)
							AND (S."TINH_TRANG" = '0'
								OR S."TINH_TRANG" = '1'
								OR S."TINH_TRANG" = '2'
							) --nvtoan modify 30/06/2016: Lấy cả đơn hàng đã hoàn thành theo yêu cầu 108085
							AND (S."CHI_NHANH_ID" = chi_nhanh_id
								OR (bao_gom_chi_nhanh_phu_thuoc = 1
									AND S."CHI_NHANH_ID" IN (
							SELECT "CHI_NHANH_ID"
							FROM danh_muc_to_chuc OU
							WHERE OU."parent_id" = chi_nhanh_id
								AND "HACH_TOAN_SELECTION" = 'PHU_THUOC')
								)
							)
						ORDER BY S."NGAY_DON_HANG",
							S."SO_DON_HANG",
							S."TEN_KHACH_HANG"
					;
				END IF
				;

				-- hợp đồng
				IF LOAI_GIA_THANH = 5
				THEN
					INSERT INTO TMP_KET_QUA
					("HOP_DONG_ID",
					"SO_HOP_DONG",
					"NGAY_KY",
					"TRICH_YEU",
					"TEN_KHACH_HANG",
					"CHI_NHANH_ID"
					)
						SELECT
							C."id"
							, "SO_HOP_DONG"
							, "NGAY_KY"
							, "TRICH_YEU"
							, AC."HO_VA_TEN"
							, C."CHI_NHANH_ID"
						FROM sale_ex_hop_dong_ban C
							LEFT JOIN CHUYEN_CHUOI_CAC_GUI_THANH_BANG_CHUA_CAC_GUI(ds_da_chon,
																				';') F ON C."id" = F.Value
							LEFT JOIN res_partner AC ON Ac."id" = C."KHACH_HANG_ID"
						WHERE F.Value IS NULL
							AND (C."TINH_GIA_THANH" = TRUE)
							AND (C."TINH_TRANG_HOP_DONG" = '0'
								OR C."TINH_TRANG_HOP_DONG" = '1'
								OR C."TINH_TRANG_HOP_DONG" = '3'
								OR C."TINH_TRANG_HOP_DONG" = '4'
							)
							AND (c."CHI_NHANH_ID" = chi_nhanh_id
								OR (bao_gom_chi_nhanh_phu_thuoc = 1
									AND C."CHI_NHANH_ID" IN (
							SELECT OU."id"
							FROM danh_muc_to_chuc OU
							WHERE OU."parent_id" = chi_nhanh_id
								AND "HACH_TOAN_SELECTION" = 'PHU_THUOC')
								)
							)
						ORDER BY C."SO_HOP_DONG",
							C."NGAY_KY",
							C."TRICH_YEU"
					;
				END IF
				;


				DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
				;

				CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
					AS
						SELECT
							CAST(0 AS BOOLEAN) AS Selected
							, *
						FROM TMP_KET_QUA
				;


			END $$

			;

			SELECT *
			FROM TMP_KET_QUA_CUOI_CUNG


				"""
		return self.execute(query, params)



	@api.model_cr
	def init(self):
		self.env.cr.execute("""
			DROP FUNCTION IF EXISTS CHUYEN_CHUOI_CAC_GUI_THANH_BANG_CHUA_CAC_GUI( IN v_GUIString VARCHAR,

			v_SeparateCharacter VARCHAR )
			;

			CREATE OR REPLACE FUNCTION CHUYEN_CHUOI_CAC_GUI_THANH_BANG_CHUA_CAC_GUI(IN v_GUIString         VARCHAR,

																					v_SeparateCharacter VARCHAR)--Func_ConvertGUIStringIntoTable
				RETURNS TABLE(

					Value INT

				) AS $$



			DECLARE


				v_ValueListLength  INTEGER;

				v_StartingPosition INTEGER;

				v_Value            VARCHAR(50);

				v_SecondPosition   INTEGER;


			BEGIN


				v_GUIString := coalesce(v_GUIString, '') || coalesce(v_SeparateCharacter, '')
				;

				v_ValueListLength := LENGTH(v_GUIString)
				;

				v_StartingPosition := 1
				;

				v_Value := REPEAT(' ', 0)
				;


				DROP TABLE IF EXISTS tt_VALUETABLE CASCADE
				;

				CREATE TEMPORARY TABLE tt_VALUETABLE
				(
					Value INT
				)
				;


				WHILE v_StartingPosition < v_ValueListLength LOOP
					-- V? trí k? ti?p xu?t hi?n ký t? phân cách
					v_SecondPosition := CASE WHEN
						POSITION(v_SeparateCharacter IN SUBSTR(v_GUIString, v_StartingPosition :: INT + 1)) > 0
						THEN POSITION(v_SeparateCharacter IN SUBSTR(v_GUIString, v_StartingPosition :: INT + 1)) +
							v_StartingPosition :: INT + 1 - 1
										ELSE 0 END
				;

					-- Trích ra giá tr? t? chu?i
					v_Value := SUBSTR(v_GUIString, v_StartingPosition :: INT + 1,
									v_SecondPosition :: INT - v_StartingPosition :: INT - 1)
				;

					-- Thi?t l?p l?i giá tr? b?t d?u
					v_StartingPosition := v_SecondPosition
				;

					IF v_Value <> REPEAT(' ', 0)
					THEN
						INSERT INTO tt_VALUETABLE (Value) VALUES (CAST(v_Value AS INT))
						;
					END IF
				;

				END LOOP
				;


				RETURN QUERY SELECT *
							FROM tt_VALUETABLE
				;

			END
			;

			$$ LANGUAGE PLpgSQL
			;

		""")