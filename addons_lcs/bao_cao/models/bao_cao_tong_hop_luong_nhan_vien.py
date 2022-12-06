# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision
from datetime import datetime


class BAO_CAO_TONG_HOP_LUONG_NHAN_VIEN(models.Model):
	_name = 'bao.cao.tong.hop.luong.nhan.vien'
	
	
	_auto = False

	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
	BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default=True)
	KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI',required=True)
	TU_NGAY = fields.Date(string='Từ', help='Từ ngày',default=fields.Datetime.now)
	DEN_NGAY = fields.Date(string='Đến', help='Đến ngày',default=fields.Datetime.now)
	DON_VI = fields.Char(string='Đơn vị', help='Đơn vị')
	MA_NHAN_VIEN = fields.Char(string='Mã nhân viên', help='Mã nhân viên')
	TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='Tên nhân viên')
	THU_NHAP_CHIU_THUE_TNCN = fields.Float(string='Thu nhập chịu thuế TNCN', help='Thu nhập chịu thuế thu nhập cá nhân',digits=decimal_precision.get_precision('VND'))
	GIA_CANH_GIAM_TRU = fields.Float(string='Gia cảnh giảm trừ', help='Gia cảnh giảm trừ',digits=decimal_precision.get_precision('VND'))
	BAO_HIEM_GIAM_TRU = fields.Float(string='Bảo hiểm giảm trừ', help='Bảo hiểm giảm trừ',digits=decimal_precision.get_precision('VND'))
	TONG_GIAM_TRU = fields.Float(string='Tổng giảm trừ', help='Tổng giảm trừ',digits=decimal_precision.get_precision('VND'))
	THU_NHAP_TINH_THUE_TNCN = fields.Float(string='Thu nhập tính thuế TNCN', help='Thu nhập tính thuế thu nhập cá nhân',digits=decimal_precision.get_precision('VND'))
	THUE_TNCN_DA_KHAU_TRU = fields.Float(string='Thuế TNCN đã khấu trừ', help='Thuế thu nhập cá nhân đã khấu trừ',digits=decimal_precision.get_precision('VND'))
	THU_NHAP_SAU_THUE = fields.Float(string='Thu nhập sau thuế', help='Thu nhập sau thuế',digits=decimal_precision.get_precision('VND'))
	name = fields.Char(string='Name', help='Name', oldname='NAME')

	DON_VI_IDS = fields.One2many('danh.muc.to.chuc')


	@api.model
	def default_get(self, fields_list):
		result = super(BAO_CAO_TONG_HOP_LUONG_NHAN_VIEN, self).default_get(fields_list)
		
		chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
		don_vis = self.env['danh.muc.to.chuc'].search([('CAP_TO_CHUC' ,'not in', ('1','2'))])
		if chi_nhanh:
			result['CHI_NHANH_ID'] = chi_nhanh.id
		if don_vis:
			result['DON_VI_IDS'] = don_vis.ids
		
		return result

	@api.onchange('KY_BAO_CAO')
	def _cap_nhat_ngay(self):
		self.onchange_time(self.KY_BAO_CAO, 'TU_NGAY', 'DEN_NGAY')

	def _validate(self):
		params = self._context
		TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
		TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
		DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		DON_VI_IDS = params['DON_VI_IDS'] if 'DON_VI_IDS' in params.keys() else 'False'
		if (DON_VI_IDS == 'False'):
			raise ValidationError('Bạn chưa chọn <Đơn vị>. Xin vui lòng chọn lại.')
		elif(TU_NGAY=='False'):
			raise ValidationError('<Từ ngày> không được bỏ trống.')
		elif(DEN_NGAY=='False'):
			raise ValidationError('<Đến ngày> không được bỏ trống.')
		elif(TU_NGAY_F > DEN_NGAY_F):
			raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')

	

	@api.model
	def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
		record = []
		# Get paramerters here
		params = self._context
		if not params.get('active_model'):
			return
		CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
		BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
		
		TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
		TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
		DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

		NAM = params['NAM'] if 'NAM' in params.keys() else 'False'
		DON_VI_IDS = [nh_kh['id'] for nh_kh in params['DON_VI_IDS']]  if 'DON_VI_IDS' in params.keys() and params['DON_VI_IDS'] != 'False' else None
		
		params_sql = {
			'TU_NGAY':TU_NGAY_F, 
			'DEN_NGAY':DEN_NGAY_F, 
			'CHI_NHANH_ID':CHI_NHANH_ID, 
			'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
			'DON_VI_IDS':DON_VI_IDS,
			'limit': limit,
			'offset': offset, 
			}      
		# Execute SQL query here
		query = """
		DO LANGUAGE plpgsql $$
DECLARE


	chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

	bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

	--tham số bao gồm số liệu chi nhánh phụ thuộc

	tu_ngay                             TIMESTAMP := %(TU_NGAY)s;

	den_ngay                            TIMESTAMP := %(DEN_NGAY)s;

	don_vi_ids                          INTEGER := -1;

	--@OrganizationUnitID


BEGIN

	DROP TABLE IF EXISTS TMP_LIST_BRAND
	;

	CREATE TEMP TABLE TMP_LIST_BRAND
		AS
			SELECT *
			FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
	;


	DROP TABLE IF EXISTS TMP_DON_VI
	;

	CREATE TEMP TABLE TMP_DON_VI

	(
		"DON_VI_ID"   INT PRIMARY KEY,
		"MA_DON_VI"   VARCHAR(20),
		"TEN_DON_VI"  VARCHAR(128),
		"MA_PHAN_CAP" VARCHAR(100),
		"BAC"         INT

	)
	;

	IF don_vi_ids IS NOT NULL
	THEN
		INSERT INTO TMP_DON_VI
			SELECT
				"id" AS "DON_VI_ID"
				, "MA_DON_VI"
				, "TEN_DON_VI"
				, OU."MA_PHAN_CAP"
				, OU."BAC"

			FROM danh_muc_to_chuc OU
			WHERE OU."id" = any(%(DON_VI_IDS)s) --@OrganizationUnitID
		;
	END IF
	;


	/*vhanh edited 20.01.2017: Bảng tạm lưu các thông tin của nhân viên đồng thời có cả lương cơ bản và chức vụ cuối trên bảng lương chi tiết (CR 27149)*/

	DROP TABLE IF EXISTS TMP_THONG_TIN_NHAN_VIEN
	;

	CREATE TEMP TABLE TMP_THONG_TIN_NHAN_VIEN

	(
		"MA_NHAN_VIEN_ID"        INT,
		"MA_NHAN_VIEN"           VARCHAR(25),
		"TEN_NHAN_VIEN"          VARCHAR(128),
		/*Lấy cả thông tin phòng ban để lấy đúng thông tin lương cơ bản, chức danh trong trường hợp nhân viên chuyển phòng ban*/
		"DON_VI_ID"              INT,
		"SO_TAI_KHOAN_NGAN_HANG" VARCHAR(50),
		"TEN_NGAN_HANG"          VARCHAR(128),
		"MA_SO_THUE"             VARCHAR(50),
		"LUONG_CO_BAN"           DECIMAL(18, 4),
		"CHUC_DANH"              VARCHAR(128)
	)
	;

	IF EXTRACT(YEAR FROM tu_ngay)  =
	   EXTRACT(YEAR FROM den_ngay)  --Nếu thời gian xem báo cáo cùng năm
	THEN
		INSERT INTO TMP_THONG_TIN_NHAN_VIEN
			SELECT
				"MA_NHAN_VIEN_ID"
				, "MA_NHAN_VIEN"
				, "TEN_NHAN_VIEN"
				, "DON_VI_ID"
				, "SO_TAI_KHOAN_NGAN_HANG"
				, "TEN_NGAN_HANG"
				, "MA_SO_THUE"
				, "LUONG_CO_BAN" AS "LUONG_CO_BAN"
				, "CHUC_DANH"    AS "CHUC_DANH"
			FROM (
					 SELECT
						   ROW_NUMBER()
						   OVER (
							   PARTITION BY PAD."MA_NHAN_VIEN", PAD."DON_VI_ID"
							   ORDER BY PA."NAM" DESC, PA."THANG" DESC ) AS "RowNum"
						 , AO."id"                                       AS "MA_NHAN_VIEN_ID"
						 , AO."MA"                                       AS "MA_NHAN_VIEN"
						 , AO."HO_VA_TEN"                                AS "TEN_NHAN_VIEN"
						 , PAD."DON_VI_ID"
						 , AOB."SO_TAI_KHOAN"                            AS "SO_TAI_KHOAN_NGAN_HANG"
						 , AOB."TEN_NGAN_HANG"
						 , AO."MA_SO_THUE"
						 , PAD."LUONG_CO_BAN"   AS  "LUONG_CO_BAN"
						 , PAD."CHUC_DANH"
					 FROM tien_luong_bang_luong_chi_tiet PAD INNER JOIN tien_luong_bang_luong PA
							 ON PA."id" = PAD."CHI_TIET_ID"
						 LEFT JOIN res_partner AO ON AO."id" = PAD."MA_NHAN_VIEN"
						 LEFT JOIN danh_muc_doi_tuong_chi_tiet AS AOB ON AO."id" = AOB."DOI_TUONG_ID"
																		 AND AOB."id" = (SELECT "id"
																						 FROM
																							 danh_muc_doi_tuong_chi_tiet
																						 WHERE "DOI_TUONG_ID" = AO."id"
																						 ORDER BY "STT"
																						 LIMIT 1
						 )
					 WHERE PA."LOAI_CHUNG_TU" IN (6020, 6021, 6022)

						   AND "NAM" = EXTRACT(YEAR FROM tu_ngay) 
						   AND "THANG" <= EXTRACT(MONTH FROM den_ngay) 
				 ) S
			WHERE S."RowNum" = 1

		;


		DROP TABLE IF EXISTS TMP_KET_QUA
		;

		CREATE TEMP TABLE TMP_KET_QUA
			AS
				SELECT
					  ROW_NUMBER()
					  OVER (
						  ORDER BY OU."MA_DON_VI"
								   || ' - ' || OU."TEN_DON_VI", AO."MA_NHAN_VIEN", AO."TEN_NHAN_VIEN" ) AS "RowNum"
					, OU."MA_DON_VI" || ' - '
					  || OU."TEN_DON_VI"                                                                AS "DON_VI"
					, -- Mã đơn vị - tên đơn vị
					  AO."MA_NHAN_VIEN"                                                                 AS "MA_NHAN_VIEN"
					, -- Mã nhân viên
					  AO."TEN_NHAN_VIEN"                                                                AS "TEN_NHAN_VIEN"
					, -- Tên nhân viên
					AO."CHUC_DANH"
					, -- Chức danh trong tháng cuối được tính lương (CR 27149)
					AO."SO_TAI_KHOAN_NGAN_HANG"
					, -- Số TK ngân hàng
					AO."TEN_NGAN_HANG"
					, -- Tên ngân hàng
					AO."LUONG_CO_BAN"
					, -- Lương cơ bản trong tháng cuối được tính lương
					  SUM(COALESCE(PAD."TONG_THU_NHAP_CHIU_THUE_TNCN",
								   CAST(0 AS
										DECIMAL)))                                                      AS "THU_NHAP_CHIU_THUE_TNCN"
					, -- Tổng thu nhập chịu thuế
					  SUM(
						  PAD."GIAM_TRU_GIA_CANH")                                                      AS "GIAM_TRU_GIA_CANH"
					, -- Giảm trừ gia cảnh
					  SUM(PAD."BHXH_KHAU_TRU"
						  + PAD."BHYT_KHAU_TRU"
						  +
						  PAD."BHTN_KHAU_TRU")                                                          AS "BAO_HIEM_DUOC_TRU"
					, -- Bảo hiểm được trừ
					  SUM(PAD."GIAM_TRU_GIA_CANH"
						  + PAD."BHXH_KHAU_TRU"
						  + PAD."BHYT_KHAU_TRU"
						  + PAD."BHTN_KHAU_TRU")                                                        AS "TONG"
					, -- Tổng các khoản giảm trừ
					  CASE WHEN SUM(COALESCE(PAD."TONG_THU_NHAP_CHIU_THUE_TNCN",
											 CAST(0 AS DECIMAL))
									- PAD."GIAM_TRU_GIA_CANH"
									- PAD."BHXH_KHAU_TRU"
									- PAD."BHYT_KHAU_TRU"
									- PAD."BHTN_KHAU_TRU") < 0
						  THEN 0
					  ELSE SUM(COALESCE(PAD."TONG_THU_NHAP_CHIU_THUE_TNCN",
										CAST(0 AS DECIMAL))
							   - PAD."GIAM_TRU_GIA_CANH"
							   - PAD."BHXH_KHAU_TRU"
							   - PAD."BHYT_KHAU_TRU"
							   - PAD."BHTN_KHAU_TRU")
					  END                                                                               AS "THU_NHAP_TINH_THUE_TNCN"
					, -- Thu nhập tính thuế TNCN (không lấy từ bảng lương)
					  SUM(
						  PAD."THUE_TNCN_KHAU_TRU")                                                     AS "THUE_TNCN_DA_KHAU_TRU"
					, -- Thuế Thu nhập cá nhân
					  SUM(COALESCE(PAD."TONG_THU_NHAP_CHIU_THUE_TNCN",
								   CAST(0 AS DECIMAL))
						  - PAD."BHXH_KHAU_TRU"
						  - PAD."BHYT_KHAU_TRU"
						  - PAD."BHTN_KHAU_TRU"
						  -
						  PAD."THUE_TNCN_KHAU_TRU")                                                     AS "THU_NHAP_SAU_THUE"
					, -- Thu nhập sau thuế

					  AO."MA_SO_THUE"                                                                   AS "MA_SO_THUE"
				FROM tien_luong_bang_luong PA
					INNER JOIN tien_luong_bang_luong_chi_tiet PAD ON PAD."CHI_TIET_ID" = PA."id"
					INNER JOIN TMP_DON_VI OU ON PAD."DON_VI_ID" = OU."DON_VI_ID"
					INNER JOIN TMP_LIST_BRAND BIDL ON PA."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
					LEFT JOIN TMP_THONG_TIN_NHAN_VIEN AO
						ON PAD."MA_NHAN_VIEN" = AO."MA_NHAN_VIEN_ID" AND PAD."DON_VI_ID" = AO."DON_VI_ID"
				WHERE PA."LOAI_CHUNG_TU" IN (6020, 6021, 6022)

					  AND PA."NAM" = EXTRACT(YEAR FROM den_ngay) 
					  AND PA."THANG" BETWEEN EXTRACT(MONTH FROM tu_ngay) 
					  AND EXTRACT(MONTH FROM den_ngay) 
				GROUP BY
					OU."MA_DON_VI" || ' - '
					|| OU."TEN_DON_VI", -- Mã đơn vị - tên đơn vị
					AO."MA_NHAN_VIEN", -- Mã nhân viên
					AO."TEN_NHAN_VIEN", -- Tên nhân viên
					AO."SO_TAI_KHOAN_NGAN_HANG", -- Số TK ngân hàng
					AO."TEN_NGAN_HANG", -- Tên ngân hàng
					AO."MA_SO_THUE",
					AO."CHUC_DANH",
					AO."LUONG_CO_BAN"
				ORDER BY
					"DON_VI",
					AO."MA_NHAN_VIEN",
					AO."TEN_NHAN_VIEN"
		;

	ELSE -- Xem từ năm này đến năm kia

		INSERT INTO TMP_THONG_TIN_NHAN_VIEN
			SELECT
				"MA_NHAN_VIEN_ID"
				, "MA_NHAN_VIEN"
				, "TEN_NHAN_VIEN"
				, "DON_VI_ID"
				, "SO_TAI_KHOAN_NGAN_HANG"
				, "TEN_NGAN_HANG"
				, "MA_SO_THUE"
				, "LUONG_CO_BAN"   AS "LUONG_CO_BAN"
				, "CHUC_DANH" AS "CHUC_DANH"
			FROM (
					 SELECT
						 ROW_NUMBER()
						 OVER (
							 PARTITION BY PAD."MA_NHAN_VIEN", PAD."DON_VI_ID"
							 ORDER BY PA."NAM" DESC, PA."THANG" DESC ) AS "RowNum"
						 , AO."id" AS "MA_NHAN_VIEN_ID"
						 , AO."MA" AS "MA_NHAN_VIEN"
						 , AO."HO_VA_TEN" AS "TEN_NHAN_VIEN"
						 , PAD."DON_VI_ID"
						 , AOB."SO_TAI_KHOAN" AS "SO_TAI_KHOAN_NGAN_HANG"
						 , AOB."TEN_NGAN_HANG"
						 , AO."MA_SO_THUE"
						 , PAD."LUONG_CO_BAN"
						 , PAD."CHUC_DANH"
					 FROM tien_luong_bang_luong_chi_tiet PAD INNER JOIN tien_luong_bang_luong PA
							 ON PA."id" = PAD."CHI_TIET_ID"
						 LEFT JOIN res_partner AO ON AO."id" = PAD."MA_NHAN_VIEN"
						 LEFT JOIN danh_muc_doi_tuong_chi_tiet AS AOB ON AO."id" = AOB."DOI_TUONG_ID"
																		 AND AOB."id" = (SELECT "id"
																						 FROM
																							 danh_muc_doi_tuong_chi_tiet
																						 WHERE "DOI_TUONG_ID" = AO."id"
																						 ORDER BY "STT"
																						 LIMIT 1
						 )

					 WHERE PA."LOAI_CHUNG_TU" IN (6020, 6021, 6022)

						   AND ((PA."NAM" =   EXTRACT(YEAR FROM tu_ngay) 
								 AND PA."THANG" >=  EXTRACT(MONTH FROM tu_ngay) 
								)
								OR (PA."NAM" =  EXTRACT(YEAR FROM den_ngay) 
									AND PA."THANG" <=  EXTRACT(MONTH FROM den_ngay) 
								)
								OR (PA."NAM" >   EXTRACT(YEAR FROM tu_ngay) 
									AND PA."NAM" <  EXTRACT(YEAR FROM den_ngay) 
								)
						   )
				 ) S
			WHERE S."RowNum" = 1
		;

		DROP TABLE IF EXISTS TMP_KET_QUA
		;

		CREATE TEMP TABLE TMP_KET_QUA
			AS

				SELECT
					-- PA."ID_CHUNG_TU" ,
					--ptphuong2 01/12/2016 bổ sung Row_Number để sắp xếp hiển thị khi in báo cáo (sửa bug 20528)
					  ROW_NUMBER()
					  OVER (
						  ORDER BY OU."MA_DON_VI"
								   || ' - ' || OU."TEN_DON_VI", AO."MA_NHAN_VIEN", AO."TEN_NHAN_VIEN" ) AS "RowNum"
					, OU."MA_DON_VI" || ' - '
					  || OU."TEN_DON_VI"                                                                 AS "DON_VI"
					, -- Mã đơn vị - tên đơn vị
					  AO."MA_NHAN_VIEN"                                                                AS "MA_NHAN_VIEN"
					, -- Mã nhân viên
					  AO."TEN_NHAN_VIEN"                                                               AS "TEN_NHAN_VIEN"
					, -- Tên nhân viên
					  AO."CHUC_DANH"                                                                    AS "CHUC_DANH"
					, --Chức danh trong tháng lương cuối được tính (CR 27149)
					AO."SO_TAI_KHOAN_NGAN_HANG"
					, -- Số TK ngân hàng
					AO."TEN_NGAN_HANG"
					, -- Tên ngân hàng
					AO."LUONG_CO_BAN"
					, -- Lương cơ bản
					  SUM(COALESCE(PAD."TONG_THU_NHAP_CHIU_THUE_TNCN",
								   CAST(0 AS
										DECIMAL)))                                                      AS "THU_NHAP_CHIU_THUE_TNCN"
					, -- Tổng thu nhập chịu thuế
					  SUM(
						  PAD."GIAM_TRU_GIA_CANH")                                                      AS "GIAM_TRU_GIA_CANH"
					, -- Giảm trừ gia cảnh
					  SUM(PAD."BHXH_KHAU_TRU"
						  + PAD."BHYT_KHAU_TRU"
						  +
						  PAD."BHTN_KHAU_TRU")                                                          AS "BAO_HIEM_DUOC_TRU"
					, -- Bảo hiểm được trừ
					  SUM(PAD."GIAM_TRU_GIA_CANH"
						  + PAD."BHXH_KHAU_TRU"
						  + PAD."BHYT_KHAU_TRU"
						  + PAD."BHTN_KHAU_TRU")                                                        AS "TONG"
					, -- Tổng các khoản giảm trừ
					  CASE WHEN SUM(COALESCE(PAD."TONG_THU_NHAP_CHIU_THUE_TNCN",
											 CAST(0 AS DECIMAL))
									- PAD."GIAM_TRU_GIA_CANH"
									- PAD."BHXH_KHAU_TRU"
									- PAD."BHYT_KHAU_TRU"
									- PAD."BHTN_KHAU_TRU") < 0
						  THEN 0
					  ELSE SUM(COALESCE(PAD."TONG_THU_NHAP_CHIU_THUE_TNCN",
										CAST(0 AS DECIMAL))
							   - PAD."GIAM_TRU_GIA_CANH"
							   - PAD."BHXH_KHAU_TRU"
							   - PAD."BHYT_KHAU_TRU"
							   - PAD."BHTN_KHAU_TRU")
					  END                                                                               AS "THU_NHAP_TINH_THUE_TNCN"
					, -- Thu nhập tính thuế TNCN (không lấy từ bảng lương)
					  SUM(
						  PAD."THUE_TNCN_KHAU_TRU")                                                     AS "THUE_TNCN_DA_KHAU_TRU"
					, -- Thuế Thu nhập cá nhân
					  SUM(COALESCE(PAD."TONG_THU_NHAP_CHIU_THUE_TNCN",
								   CAST(0 AS DECIMAL))
						  - PAD."BHXH_KHAU_TRU"
						  - PAD."BHYT_KHAU_TRU"
						  - PAD."BHTN_KHAU_TRU"
						  - PAD."THUE_TNCN_KHAU_TRU")                                                   AS "THU_NHAP_SAU_THUE"
					, -- Thu nhập sau thuế

					  AO."MA_SO_THUE"                                                                   AS "MA_SO_THUE"
				FROM tien_luong_bang_luong PA
					INNER JOIN tien_luong_bang_luong_chi_tiet PAD ON PAD."CHI_TIET_ID" = PA."id"
					INNER JOIN TMP_DON_VI OU ON PAD."DON_VI_ID" = OU."DON_VI_ID"
					INNER JOIN TMP_LIST_BRAND BIDL ON PA."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
					LEFT JOIN TMP_THONG_TIN_NHAN_VIEN AO
						ON PAD."MA_NHAN_VIEN" = AO."MA_NHAN_VIEN_ID" AND PAD."DON_VI_ID" = AO."DON_VI_ID"
				WHERE PA."LOAI_CHUNG_TU" IN (6020, 6021, 6022)

					  AND ((PA."NAM" =    EXTRACT(YEAR FROM tu_ngay) 
							AND PA."THANG" >=   EXTRACT(MONTH FROM tu_ngay) 
						   )
						   OR (PA."NAM" = EXTRACT(YEAR FROM den_ngay) 
							   AND PA."THANG" <=   EXTRACT(MONTH FROM den_ngay) 
						   )
						   OR (PA."NAM" >   EXTRACT(YEAR FROM tu_ngay) 
							   AND PA."NAM" <  EXTRACT(YEAR FROM den_ngay) 
						   )
					  )
				GROUP BY
					OU."MA_DON_VI" || ' - '
						 || OU."TEN_DON_VI", -- Mã đơn vị - tên đơn vị
					AO."MA_NHAN_VIEN", -- Mã nhân viên
					AO."TEN_NHAN_VIEN", -- Tên nhân viên
					AO."SO_TAI_KHOAN_NGAN_HANG", -- Số TK ngân hàng
					AO."TEN_NGAN_HANG", -- Tên ngân hàng
					AO."MA_SO_THUE",
					AO."CHUC_DANH",
					AO."LUONG_CO_BAN"
				ORDER BY
					"DON_VI",
					AO."MA_NHAN_VIEN",
					AO."TEN_NHAN_VIEN"
		;

	END IF
	;

END $$
;
		SELECT 
				"MA_NHAN_VIEN" AS "MA_NHAN_VIEN",
				"TEN_NHAN_VIEN" AS "TEN_NHAN_VIEN",
				"THU_NHAP_CHIU_THUE_TNCN" AS "THU_NHAP_CHIU_THUE_TNCN",
				"GIAM_TRU_GIA_CANH" AS "GIA_CANH_GIAM_TRU",
				"BAO_HIEM_DUOC_TRU" AS "BAO_HIEM_GIAM_TRU",
				"TONG" AS "TONG_GIAM_TRU",
				"THU_NHAP_TINH_THUE_TNCN" AS "THU_NHAP_TINH_THUE_TNCN",
				"THUE_TNCN_DA_KHAU_TRU" AS "THUE_TNCN_DA_KHAU_TRU",
				"THU_NHAP_SAU_THUE" AS "THU_NHAP_SAU_THUE",
				"DON_VI" AS "DON_VI"
			
				FROM TMP_KET_QUA
				ORDER BY
				"RowNum"

				OFFSET %(offset)s
				LIMIT %(limit)s;
		"""
		return self.execute(query,params_sql)

	### END IMPLEMENTING CODE ###

	def _action_view_report(self):
		self._validate()
		TU_NGAY_F = self.get_vntime('TU_NGAY')
		DEN_NGAY_F = self.get_vntime('DEN_NGAY')
		param =''
		if len (self.get_context('DON_VI_IDS')) == 1:
			DON_VI = self.get_context('DON_VI_IDS')[0]['TEN_DON_VI']
			if TU_NGAY_F==DEN_NGAY_F:
				param = ' Đơn vị: %s ; %s' % (DON_VI, TU_NGAY_F)
			else:
				param = ' Đơn vị: %s ; Từ ngày %s đến ngày %s' % (DON_VI, TU_NGAY_F, DEN_NGAY_F)
		else:
			if TU_NGAY_F==DEN_NGAY_F:
				param = ' %s' % (TU_NGAY_F)
			else:
				param = ' Từ ngày %s đến ngày %s' % (TU_NGAY_F, DEN_NGAY_F)
		action = self.env.ref('bao_cao.open_report_tong_hop_luong_nhan_vien').read()[0]
		# action['options'] = {'clear_breadcrumbs': True}
		action['context'] = eval(action.get('context','{}'))
		action['context'].update({'breadcrumb_ex': param})
		return action