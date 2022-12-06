# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_BAN_RA(models.Model):
	_name = 'bang.ke.hoa.don.chung.tu.ban.ra'
	
	
	_auto = False

	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
	BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
	KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI', required='True')
	TU = fields.Date(string='Từ', help='Từ', required='True', default=fields.Datetime.now)
	DEN = fields.Date(string='Đến', help='Đến', required='True', default=fields.Datetime.now)
	CONG_GOP_THEO_TUNG_HOA_DON = fields.Boolean(string='Cộng gộp theo từng hóa đơn', help='Cộng gộp theo từng hóa đơn')
	LAY_SO_LIEU_DVT_SO_LUONG_DON_GIA_LEN_BAO_CAO = fields.Boolean(string='Lấy số liệu ĐVT, Số lượng, Đơn giá lên báo cáo', help='Lấy số liệu đơn vị tính. Số lượng. Đơn giá lên báo cáo')
	NHOM_HHDV_BAN_RA = fields.Char(string='Nhóm HHDV', help='Nhóm hàng hóa dịch vụ bán ra')
	SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
	SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
	NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
	TEN_NGUOI_MUA = fields.Char(string='Tên người mua', help='Tên người mua')
	MA_SO_THUE_NGUOI_MUA = fields.Char(string='Mã số thuế người mua', help='Mã số thuế người mua')#, auto_num='bao_cao_bang_ke_hoa_don_chung_tu_MA_SO_THUE_NGUOI_BAN')
	MAT_HANG = fields.Char(string='Mặt hàng', help='Mặt hàng')
	DOANH_SO_BAN_CHUA_CO_THUE_GTGT = fields.Float(string='Doanh số bán chưa có thuế GTGT', help='Doanh số bán chưa có thuế giá trị gia tăng',digits=decimal_precision.get_precision('VND'))
	THUE_GTGT = fields.Float(string='Thuế GTGT', help='Thuế giá trị gia tăng',digits=decimal_precision.get_precision('VND'))
	TK_THUE = fields.Char(string='TK thuế', help='Tài khoản thuế')
	name = fields.Char(string='Name', help='Name', oldname='NAME')
	ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
	MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')

	BANG_KE_HOA_DON_CT_GROUP_ID = fields.Many2one('bang.ke.hoa.don.chung.tu.ban.ra.group')
  
	@api.model
	def default_get(self, fields_list):
		result = super(BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_BAN_RA, self).default_get(fields_list)
		chi_nhanh = self.env['danh.muc.to.chuc'].search([],order="MA_DON_VI",limit=1)
		if chi_nhanh :
			result['CHI_NHANH_ID'] = chi_nhanh.id
		return result
	
	@api.onchange('KY_BAO_CAO')
	def _cap_nhat_ngay(self):
		self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')
	def _validate(self):
		params = self._context
		TU = params['TU'] if 'TU' in params.keys() else 'False'
		TU = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
		DEN = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

		if(TU=='False'):
			raise ValidationError('<Từ> không được bỏ trống.')
		elif(DEN=='False'):
			raise ValidationError('<Đến> không được bỏ trống.')
		elif(TU > DEN):
			raise ValidationError('<Đến> phải lớn hơn hoặc bằng <Từ>.')

	@api.model
	def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
		record = []
		# Get paramerters here
		params = self._context
		if not params.get('active_model'):
			return
		CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
		BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
		TU_NGAY = params['TU'] if 'TU' in params.keys() else 'False'
		TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		DEN_NGAY = params['DEN'] if 'DEN' in params.keys() else 'False'
		DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		CONG_GOP_THEO_TUNG_HOA_DON = 1 if 'CONG_GOP_THEO_TUNG_HOA_DON' in params.keys() and params['CONG_GOP_THEO_TUNG_HOA_DON'] != 'False' else 0
		LAY_SO_LIEU_DVT_SO_LUONG_DON_GIA_LEN_BAO_CAO = 1 if 'LAY_SO_LIEU_DVT_SO_LUONG_DON_GIA_LEN_BAO_CAO' in params.keys() and params['LAY_SO_LIEU_DVT_SO_LUONG_DON_GIA_LEN_BAO_CAO'] != 'False' else 0

		params_sql = {
			'TU_NGAY':TU_NGAY_F, 
			'DEN_NGAY':DEN_NGAY_F,
			'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
			'CONG_GOP_THEO_TUNG_HOA_DON':CONG_GOP_THEO_TUNG_HOA_DON,
			'LAY_SO_LIEU_DVT_SO_LUONG_DON_GIA_LEN_BAO_CAO':LAY_SO_LIEU_DVT_SO_LUONG_DON_GIA_LEN_BAO_CAO,
			'CHI_NHANH_ID':CHI_NHANH_ID,
			'limit': limit,
			'offset': offset,
		}



		query = """
			--BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_BAN_RA
DO LANGUAGE plpgsql $$
DECLARE
	v_tu_ngay                             DATE := %(TU_NGAY)s;

	--tham số từ

	v_den_ngay                            DATE := %(DEN_NGAY)s;

	--tham số đến

	v_bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

	--tham số bao gồm số liệu chi nhánh phụ thuộc

	v_chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

	--tham số chi nhánh


	v_cong_gop_theo_tung_hoa_don          INTEGER := %(CONG_GOP_THEO_TUNG_HOA_DON)s;

	--tham số cộng gộp theo từng hóa đơn

	v_lay_so_lieu_dvt_so_luong_don_gia    INTEGER := %(LAY_SO_LIEU_DVT_SO_LUONG_DON_GIA_LEN_BAO_CAO)s;


	--tham số lấy số liệu ĐVT, số lượng, đơn giá lên báo cáo


	rec                                   RECORD;




BEGIN
				DROP TABLE IF EXISTS TMP_LIST_BRAND
				;
			
				CREATE TEMP TABLE TMP_LIST_BRAND
					AS
						SELECT *
						FROM LAY_DANH_SACH_CHI_NHANH(v_chi_nhanh_id, v_bao_gom_du_lieu_chi_nhanh_phu_thuoc)
				;
			
				DROP TABLE IF EXISTS TMP_KET_QUA
				;
			
				DROP SEQUENCE IF EXISTS TMP_KET_QUA_seq
				;
			
				CREATE TEMP SEQUENCE TMP_KET_QUA_seq
				;
			
			
				CREATE TEMP TABLE TMP_KET_QUA
				(
					KeyID                       INT DEFAULT NEXTVAL('TMP_KET_QUA_seq') PRIMARY KEY,
					"NHOM_HHDV"                 VARCHAR(500),
					"THUE_SUAT"                 DECIMAL(18, 4),
					"MAU_SO_HOA_DON"            VARCHAR(127),
					"KY_HIEU_HOA_DON"           VARCHAR(255),
					"SO_HOA_DON"                VARCHAR(100),
					"NGAY_HOA_DON"              DATE,
					"ID_CHUNG_TU"               INT,
					"MODEL_CHUNG_TU"            VARCHAR(100),
			
					"TEN_NGUOI_MUA"             VARCHAR(255),
			
					"MA_SO_THUE_NGUOI_MUA"      VARCHAR(127),
					"MAT_HANG"                  VARCHAR(255),
			
					"DOANH_SO_BAN_CHUA_CO_THUE" DECIMAL(18, 4),
					"THUE_GTGT"                 DECIMAL(18, 4),
					"TK_THUE"                   VARCHAR(255),
					"CHI_NHANH_ID"              INT,
					"JoinKey"                   VARCHAR(1000),
					"CHI_TIET_ID"               INT,
					"CHI_TIET_MODEL"            VARCHAR(100)
			
			
				)
				;
			
			
				INSERT INTO TMP_KET_QUA
				("NHOM_HHDV",
				 "THUE_SUAT",
				 "MAU_SO_HOA_DON",
				 "KY_HIEU_HOA_DON",
				 "SO_HOA_DON",
				 "NGAY_HOA_DON",
				 "ID_CHUNG_TU",
				 "MODEL_CHUNG_TU",
				 "TEN_NGUOI_MUA",
				 "MA_SO_THUE_NGUOI_MUA",
				 "MAT_HANG",
			
				 "DOANH_SO_BAN_CHUA_CO_THUE",
				 "THUE_GTGT",
				 "TK_THUE",
				 "CHI_NHANH_ID",
				 "JoinKey",
				 "CHI_TIET_ID",
				 "CHI_TIET_MODEL"
			
				)
			
					SELECT
						  CASE WHEN TL."HHDV_KO_TONG_HOP_TREN_TO_KHAI_GTGT" = '1'
							  THEN N'5. Hàng hóa, dịch vụ không phải tổng hợp lên tờ khai 01/GTGT'
						  ELSE CASE WHEN TL."PHAN_TRAM_VAT" = -1
							  THEN N'1. Hàng hóa, dịch vụ không chịu thuế GTGT'
							   WHEN TL."PHAN_TRAM_VAT" = 0
								   THEN N'2. Hàng hóa, dịch vụ chịu thuế suất thuế GTGT 0%%'
							   WHEN TL."PHAN_TRAM_VAT" = 5
								   THEN N'3. Hàng hóa, dịch vụ chịu thuế suất thuế GTGT 5%%'
							   WHEN TL."PHAN_TRAM_VAT" = 10
								   THEN N'4. Hàng hóa, dịch vụ chịu thuế suất thuế GTGT 10%%'
							   END
						  END                      AS "NHOM_HHDV"
						, TL."PHAN_TRAM_VAT"
						, TL."MAU_SO_HOA_DON"
						, TL."KY_HIEU_HOA_DON"
						, TL."SO_HOA_DON"
						, TL."NGAY_HOA_DON"
			
						, CASE WHEN TL."ID_CHUNG_TU_GOC" = 0 OR TL."ID_CHUNG_TU_GOC" = NULL
						THEN TL."ID_CHUNG_TU"
						  ELSE
							  TL."ID_CHUNG_TU_GOC"
						  END
												   AS "ID_CHUNG_TU"
			
			
						, TL."MODEL_CHUNG_TU"
						, TL."TEN_DOI_TUONG"
						, TL."MA_SO_THUE_DOI_TUONG"
						, "DIEN_GIAI"              AS "MAT_HANG"
						, CASE
						  WHEN TL."LOAI_CHUNG_TU" = '3569'
							  THEN 0
						  WHEN TL."LOAI_CHUNG_TU" = '3568'
							  THEN CASE WHEN SI."LOAI_CHUNG_TU_DIEU_CHINH" IN (3560, --Hóa đơn bán hàng hóa, dịch vụ trong nước
																			   3561, --Hóa đơn bán hàng xuất khẩu
																			   3562, --Hóa đơn bán hàng đại lý bán đúng giá
																			   3563, --Hóa đơn bán hàng ủy thác xuất khẩu
																			   3564    --Hóa đơn trả lại hàng mua
							  )
								  THEN -1
								   ELSE 1 END
						  WHEN TL."LOAI_CHUNG_TU" = '3567'
							  THEN CASE WHEN SI."LOAI_CHUNG_TU_DIEU_CHINH" IN (3560, --Hóa đơn bán hàng hóa, dịch vụ trong nước
																			   3561, --Hóa đơn bán hàng xuất khẩu
																			   3562, --Hóa đơn bán hàng đại lý bán đúng giá
																			   3563, --Hóa đơn bán hàng ủy thác xuất khẩu
																			   3564    --Hóa đơn trả lại hàng mua
							  )
								  THEN 1
								   ELSE -1 END
						  ELSE 1
						  END * "SO_TIEN_CHIU_VAT" AS "DOANH_SO_BAN_CHUA_CO_THUE_GTGT"
						, CASE
						  WHEN TL."LOAI_CHUNG_TU" = '3569'
							  THEN 0
						  WHEN TL."LOAI_CHUNG_TU" = '3568'
							  THEN CASE WHEN SI."LOAI_CHUNG_TU_DIEU_CHINH" IN (3560, --Hóa đơn bán hàng hóa, dịch vụ trong nước
																			   3561, --Hóa đơn bán hàng xuất khẩu
																			   3562, --Hóa đơn bán hàng đại lý bán đúng giá
																			   3563, --Hóa đơn bán hàng ủy thác xuất khẩu
																			   3564    --Hóa đơn trả lại hàng mua
							  )
								  THEN -1
								   ELSE 1 END
						  WHEN TL."LOAI_CHUNG_TU" = '3567'
							  THEN CASE WHEN SI."LOAI_CHUNG_TU_DIEU_CHINH" IN (3560, --Hóa đơn bán hàng hóa, dịch vụ trong nước
																			   3561, --Hóa đơn bán hàng xuất khẩu
																			   3562, --Hóa đơn bán hàng đại lý bán đúng giá
																			   3563, --Hóa đơn bán hàng ủy thác xuất khẩu
																			   3564    --Hóa đơn trả lại hàng mua
							  )
								  THEN 1
								   ELSE -1 END
						  ELSE 1
						  END * "SO_TIEN_VAT"      AS "THUE_GTGT"
						, "MA_TK_VAT"
						, TL."CHI_NHANH_ID"
						, CASE WHEN TL."HHDV_KO_TONG_HOP_TREN_TO_KHAI_GTGT" = '1'
						THEN N'5. Hàng hóa, dịch vụ không phải tổng hợp lên tờ khai 01/GTGT'
						  ELSE CASE WHEN TL."PHAN_TRAM_VAT" = -1
							  THEN N'1. Hàng hóa, dịch vụ không chịu thuế GTGT'
							   WHEN TL."PHAN_TRAM_VAT" = 0
								   THEN N'2. Hàng hóa, dịch vụ chịu thuế suất thuế GTGT 0%%'
							   WHEN TL."PHAN_TRAM_VAT" = 5
								   THEN N'3. Hàng hóa, dịch vụ chịu thuế suất thuế GTGT 5%%'
							   WHEN TL."PHAN_TRAM_VAT" = 10
								   THEN N'4. Hàng hóa, dịch vụ chịu thuế suất thuế GTGT 10%%'
							   END
						  END || COALESCE(TL."MAU_SO_HOA_DON", '') || COALESCE(TL."KY_HIEU_HOA_DON", '')
						  || COALESCE(TL."SO_HOA_DON", '')
						  || COALESCE(CAST(TL."NGAY_HOA_DON" AS VARCHAR(255)), '')
						  || COALESCE(TL."TEN_DOI_TUONG", '')
						  || COALESCE(TL."MA_SO_THUE_DOI_TUONG", '')
						  || COALESCE(CAST(TL."CHI_NHANH_ID" AS VARCHAR(255)), '')
						  || COALESCE(CAST(TL."PHAN_TRAM_VAT" AS VARCHAR(255)), '')
						, TL."CHI_TIET_ID"
						, TL."CHI_TIET_MODEL"
					FROM so_thue_chi_tiet AS TL
						JOIN TMP_LIST_BRAND AS B ON TL."CHI_NHANH_ID" = B."CHI_NHANH_ID"
						LEFT JOIN sale_ex_hoa_don_ban_hang AS SI ON TL."ID_CHUNG_TU" = SI."id"
					WHERE TL."DS_LOAI_BANG" = 0
						  AND TL."NGAY_HOA_DON" BETWEEN v_tu_ngay AND v_den_ngay
			
						  AND (TL."PHAN_TRAM_VAT" IN (0, 5, 10, -1)
							   OR TL."HHDV_KO_TONG_HOP_TREN_TO_KHAI_GTGT" = '1'
						  )
						  AND TL."LOAI_CHUNG_TU" NOT IN ('3562', '3563')
						  -- Không bao gồm hóa đơn đại lý bán đúng giá, ủy thác xuất khẩu
						  AND (SI."LOAI_CHUNG_TU_DIEU_CHINH" IS NULL
			
							   OR SI."LOAI_CHUNG_TU_DIEU_CHINH" NOT IN (3561, 3562, 3563)
						  )
				;
			
			
				--Insert nhóm 5---------------------
				--Chứng từ bán hàng kèm Hóa đơn
				INSERT INTO TMP_KET_QUA
				("NHOM_HHDV",
				 "THUE_SUAT",
				 "MAU_SO_HOA_DON",
				 "KY_HIEU_HOA_DON",
				 "SO_HOA_DON",
				 "NGAY_HOA_DON",
				 "ID_CHUNG_TU",
				 "MODEL_CHUNG_TU",
				 "TEN_NGUOI_MUA",
				 "MA_SO_THUE_NGUOI_MUA",
				 "MAT_HANG",
			
				 "DOANH_SO_BAN_CHUA_CO_THUE",
				 "THUE_GTGT",
				 "TK_THUE",
				 "CHI_NHANH_ID",
				 "JoinKey",
				 "CHI_TIET_ID",
				 "CHI_TIET_MODEL"
			
				)
					SELECT
							N'5. Hàng hóa, dịch vụ không phải tổng hợp lên tờ khai 01/GTGT'
						, 99
						, I."MAU_SO_HD_ID"
						, I."KY_HIEU_HD"
						, I."SO_HOA_DON"
						, I."NGAY_HOA_DON"
						, I."id"
						, 'sale.ex.hoa.don.ban.hang' AS "MODEL_CHUNG_TU"
						, I."TEN_KHACH_HANG"
						, I."MA_SO_THUE"
						, VD."TEN_HANG"
						, VD."THANH_TIEN_QUY_DOI" - VD."TIEN_CK_QUY_DOI"
						, VD."TIEN_THUE_GTGT_QUY_DOI"
						, VD."TK_THUE_GTGT_ID"
						, I."CHI_NHANH_ID"
						, N'5. Hàng hóa, dịch vụ không phải tổng hợp lên tờ khai 01/GTGT'
						  || COALESCE(CAST(I."MAU_SO_HD_ID" AS VARCHAR(100)), '') || COALESCE(I."KY_HIEU_HD", '')
						  || COALESCE(I."SO_HOA_DON", '')
						  || COALESCE(CAST(I."NGAY_HOA_DON" AS VARCHAR(255)), '')
						  || COALESCE(I."TEN_KHACH_HANG", '')
						  || COALESCE(I."MA_SO_THUE", '')
						  || COALESCE(CAST(I."CHI_NHANH_ID" AS VARCHAR(255)), '')
						, VD."id"
						, 'sale.document.line'       AS "CHI_TIET_MODEL"
					FROM sale_ex_hoa_don_ban_hang AS I
						JOIN sale_document_line AS VD ON I."id" = VD."HOA_DON_ID"
						JOIN sale_document V ON VD."SALE_DOCUMENT_ID" = V."id"
						JOIN TMP_LIST_BRAND AS B ON I."CHI_NHANH_ID" = B."CHI_NHANH_ID"
					WHERE I."NGAY_HOA_DON" BETWEEN v_tu_ngay AND v_den_ngay
			
						  AND (I."LOAI_CHUNG_TU" IN (3562, 3563)    --Đại lý bán đúng giá, Ủy thác xuất khẩu
							   OR VD."LA_HANG_KHUYEN_MAI" = '1'
						  )
						  AND V."state" = 'da_ghi_so'
					--
					UNION ALL
					--Giảm giá hàng bán
					SELECT
							N'5. Hàng hóa, dịch vụ không phải tổng hợp lên tờ khai 01/GTGT'
						, 99
						, I."MAU_SO_HD_ID"
						, I."KY_HIEU_HD"
						, I."SO_HOA_DON"
						, I."NGAY_HOA_DON"
						, I."id"
						, 'sale.ex.hoa.don.ban.hang' AS "MODEL_CHUNG_TU"
						, I."TEN_KHACH_HANG"
						, I."MA_SO_THUE"
						, VD."TEN_HANG"
						, -(VD."THANH_TIEN_QUY_DOI" - VD."TIEN_CHIET_KHAU_QUY_DOI")
						, -VD."TIEN_THUE_GTGT_QUY_DOI"
						, VD."TK_THUE_GTGT_ID"
						, I."CHI_NHANH_ID"
						, N'5. Hàng hóa, dịch vụ không phải tổng hợp lên tờ khai 01/GTGT'
						  || COALESCE(CAST(I."MAU_SO_HD_ID" AS VARCHAR(100)), '') || COALESCE(I."KY_HIEU_HD", '')
						  || COALESCE(I."SO_HOA_DON", '')
						  || COALESCE(CAST(I."NGAY_HOA_DON" AS VARCHAR(255)), '')
						  || COALESCE(I."TEN_KHACH_HANG", '')
						  || COALESCE(I."MA_SO_THUE", '')
						  || COALESCE(CAST(I."CHI_NHANH_ID" AS VARCHAR(255)), '')
						, VD."id"
						, 'sale.document.line'       AS "CHI_TIET_MODEL"
					FROM sale_ex_hoa_don_ban_hang AS I
						JOIN sale_ex_chi_tiet_giam_gia_hang_ban AS VD ON I."id" = VD."HOA_DON_BAN_HANG_ID"
						JOIN sale_ex_giam_gia_hang_ban AS D ON VD."GIAM_GIA_HANG_BAN_ID" = D."id"
						JOIN TMP_LIST_BRAND AS B ON I."CHI_NHANH_ID" = B."CHI_NHANH_ID"
					WHERE I."NGAY_HOA_DON" BETWEEN v_tu_ngay AND v_den_ngay
			
						  AND I."LOAI_CHUNG_TU" IN (3565)
						  AND D."LOAI_CHUNG_TU" IN (3552, 3553, 3554, 3555)
						  --Giảm giá hàng bán - đại lý bán đúng giá, ủy thác xuất khẩu
						  AND D."state" = 'da_ghi_so'
			
			
					UNION ALL
					--Trả lại hàng bán
					SELECT
							N'5. Hàng hóa, dịch vụ không phải tổng hợp lên tờ khai 01/GTGT'
						, 99
						, I."MAU_SO_HD_ID"
						, I."KY_HIEU_HD"
						, I."SO_HOA_DON"
						, I."NGAY_HOA_DON"
						, I."id"
						, 'purchase.ex.hoa.don.mua.hang'      AS "MODEL_CHUNG_TU"
						, I."TEN_NHA_CUNG_CAP"
						, I."MA_SO_THUE"
						, RD."TEN_HANG"
						, -(RD."THANH_TIEN_QUY_DOI" - RD."TIEN_CHIET_KHAU_QUY_DOI")
						, -RD."TIEN_THUE_GTGT_QUY_DOI"
						, RD."TK_THUE_GTGT_ID"
						, I."CHI_NHANH_ID"
						, N'5. Hàng hóa, dịch vụ không phải tổng hợp lên tờ khai 01/GTGT'
						  || COALESCE(CAST(I."MAU_SO_HD_ID" AS VARCHAR(100)), '') || COALESCE(I."KY_HIEU_HD", '')
						  || COALESCE(I."SO_HOA_DON", '')
						  || COALESCE(CAST(I."NGAY_HOA_DON" AS VARCHAR(255)), '')
						  || COALESCE(I."TEN_NHA_CUNG_CAP", '')
						  || COALESCE(I."MA_SO_THUE", '')
						  || COALESCE(CAST(I."CHI_NHANH_ID" AS VARCHAR(255)), '')
						, RD."id"
						, 'sale.ex.tra.lai.hang.ban.chi.tiet' AS "CHI_TIET_MODEL"
					FROM purchase_ex_hoa_don_mua_hang AS I
						JOIN sale_ex_tra_lai_hang_ban_chi_tiet AS RD ON I."id" = RD."HOA_DON_ID"
						JOIN sale_ex_tra_lai_hang_ban AS R ON RD."TRA_LAI_HANG_BAN_ID" = R."id"
						JOIN TMP_LIST_BRAND AS B ON I."CHI_NHANH_ID" = B."CHI_NHANH_ID"
					WHERE I."NGAY_HOA_DON" BETWEEN v_tu_ngay AND v_den_ngay
			
						  AND I."LOAI_CHUNG_TU" IN (3403)
						  AND (R."LOAI_CHUNG_TU" IN (3542, 3543, 3544, 3545)
							   --Trả lại hàng bán - đại lý bán đúng giá, ủy thác xuất khẩu
							   OR RD."LA_HANG_KHUYEN_MAI" = '1'
						  )
						  AND R."state" = 'da_ghi_so'
					UNION ALL
					-- Hóa đơn bán hàng không kèm
					SELECT
							N'5. Hàng hóa, dịch vụ không phải tổng hợp lên tờ khai 01/GTGT'
						, 99
						, I."MAU_SO_HD_ID"
						, I."KY_HIEU_HD"
						, I."SO_HOA_DON"
						, I."NGAY_HOA_DON"
						, I."id"
						, 'sale.ex.hoa.don.ban.hang'          AS "MODEL_CHUNG_TU"
						, I."TEN_KHACH_HANG"
						, I."MA_SO_THUE"
						, ID."TEN_HANG"
						, (ID."THANH_TIEN_QUY_DOI" - ID."TIEN_CHIET_KHAU_QUY_DOI")
						  *
			
						  (CASE
						   WHEN I."LOAI_CHUNG_TU" = 3569
							   THEN 0
						   WHEN I."LOAI_CHUNG_TU" = 3568
							   THEN CASE WHEN I."LOAI_CHUNG_TU_DIEU_CHINH" IN (3560, --Hóa đơn bán hàng hóa, dịch vụ trong nước
																			   3561, --Hóa đơn bán hàng xuất khẩu
																			   3562, --Hóa đơn bán hàng đại lý bán đúng giá
																			   3563, --Hóa đơn bán hàng ủy thác xuất khẩu
																			   3564    --Hóa đơn trả lại hàng mua
							   )
								   THEN -1
									ELSE 1 END
						   WHEN I."LOAI_CHUNG_TU" = 3567
							   THEN CASE WHEN I."LOAI_CHUNG_TU_DIEU_CHINH" IN (3560, --Hóa đơn bán hàng hóa, dịch vụ trong nước
																			   3561, --Hóa đơn bán hàng xuất khẩu
																			   3562, --Hóa đơn bán hàng đại lý bán đúng giá
																			   3563, --Hóa đơn bán hàng ủy thác xuất khẩu
																			   3564    --Hóa đơn trả lại hàng mua
							   )
								   THEN 1
									ELSE -1 END
						   ELSE 1
						   END)
						, ID."TIEN_THUE_GTGT_QUY_DOI"
						  *
			
						  (CASE
						   WHEN I."LOAI_CHUNG_TU" = 3569
							   THEN 0
						   WHEN I."LOAI_CHUNG_TU" = 3568
							   THEN CASE WHEN I."LOAI_CHUNG_TU_DIEU_CHINH" IN (3560, --Hóa đơn bán hàng hóa, dịch vụ trong nước
																			   3561, --Hóa đơn bán hàng xuất khẩu
																			   3562, --Hóa đơn bán hàng đại lý bán đúng giá
																			   3563, --Hóa đơn bán hàng ủy thác xuất khẩu
																			   3564    --Hóa đơn trả lại hàng mua
							   )
								   THEN -1
									ELSE 1 END
						   WHEN I."LOAI_CHUNG_TU" = 3567
							   THEN CASE WHEN I."LOAI_CHUNG_TU_DIEU_CHINH" IN (3560, --Hóa đơn bán hàng hóa, dịch vụ trong nước
																			   3561, --Hóa đơn bán hàng xuất khẩu
																			   3562, --Hóa đơn bán hàng đại lý bán đúng giá
																			   3563, --Hóa đơn bán hàng ủy thác xuất khẩu
																			   3564    --Hóa đơn trả lại hàng mua
							   )
								   THEN 1
									ELSE -1 END
						   ELSE 1
						   END)
						, ID."TK_THUE_GTGT_ID"
						, I."CHI_NHANH_ID"
						, N'5. Hàng hóa, dịch vụ không phải tổng hợp lên tờ khai 01/GTGT'
						  || COALESCE(CAST(I."MAU_SO_HD_ID" AS VARCHAR(100)), '') || COALESCE(I."KY_HIEU_HD", '')
						  || COALESCE(I."SO_HOA_DON", '')
						  || COALESCE(CAST(I."NGAY_HOA_DON" AS VARCHAR(255)), '')
						  || COALESCE(I."TEN_KHACH_HANG", '')
						  || COALESCE(I."MA_SO_THUE", '')
						  || COALESCE(CAST(I."CHI_NHANH_ID" AS VARCHAR(255)), '')
						, ID."id"
						, 'sale.ex.chi.tiet.hoa.don.ban.hang' AS "CHI_TIET_MODEL"
					FROM sale_ex_hoa_don_ban_hang AS I
						JOIN sale_ex_chi_tiet_hoa_don_ban_hang AS ID ON I."id" = ID."HOA_DON_ID_ID"
						JOIN TMP_LIST_BRAND AS B ON I."CHI_NHANH_ID" = B."CHI_NHANH_ID"
					WHERE I."NGAY_HOA_DON" BETWEEN v_tu_ngay AND v_den_ngay
			
						  AND (I."LOAI_CHUNG_TU" IN (3562, 3563)    --Đại lý bán đúng giá, Ủy thác xuất khẩu
			
							   OR (I."LOAI_CHUNG_TU" IN (3567, 3568, 3569) AND I."LOAI_CHUNG_TU_DIEU_CHINH" IN (3562, 3563))
							   OR ID."LA_HANG_KHUYEN_MAI" = '1'
						  )
				;
			
			
				/*hoant 133863-Bảng kê hàng hóa, dịch vụ mua vào_Lỗi: Thông tin lấy lên cột Số chứng từ bị sai khi tích chọn Cộng gộp*/
				UPDATE TMP_KET_QUA
				SET "MAU_SO_HOA_DON"       = COALESCE("MAU_SO_HOA_DON", ''),
					"KY_HIEU_HOA_DON"      = COALESCE("KY_HIEU_HOA_DON", ''),
					"SO_HOA_DON"           = COALESCE("SO_HOA_DON", ''),
					"TEN_NGUOI_MUA"        = COALESCE("TEN_NGUOI_MUA", ''),
					"MA_SO_THUE_NGUOI_MUA" = COALESCE("MA_SO_THUE_NGUOI_MUA", '')
				WHERE "MAU_SO_HOA_DON" IS NULL
					  OR "KY_HIEU_HOA_DON" IS NULL
					  OR "SO_HOA_DON" IS NULL
					  OR "TEN_NGUOI_MUA" IS NULL
					  OR "MA_SO_THUE_NGUOI_MUA" IS NULL
				;
			
			
				DROP TABLE IF EXISTS TMP_SO_CHUNG_TU
				;
			
				CREATE TEMP TABLE TMP_SO_CHUNG_TU
					AS
						SELECT
							"ID_CHUNG_TU"
							, "MODEL_CHUNG_TU_HD"
							, "SO_CHUNG_TU_FINANCE" AS "SO_CHUNG_TU"
							, "PHAN_TRAM_TGTGT"
							, "DIEN_GIAI"
							, "NGAY_CHUNG_TU"
							, "NGAY_HACH_TOAN"
			
						FROM (SELECT
								  DISTINCT
								  "ID_CHUNG_TU"
								  , "MODEL_CHUNG_TU_HD"
								  , "SO_CHUNG_TU_FINANCE"
								  , "PHAN_TRAM_TGTGT"
								  , "DIEN_GIAI"
								  , "NGAY_CHUNG_TU"
								  , "NGAY_HACH_TOAN"
							  FROM GET_BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_HD_DV_MUA_VAO(NULL,
																					  NULL, NULL, ';')
							  UNION ALL
							  SELECT DISTINCT
								  R.sale_ex_hoa_don_ban_hang_id
								  , 'sale.ex.hoa.don.ban.hang' AS "MODEL_CHUNG_TU_HD"
								  , V."SO_CHUNG_TU"
								  , V."THUE_SUAT_PHAN_TRAM"
								  , V."DIEN_GIAI"
								  , V."NGAY_CHUNG_TU"
								  , V."NGAY_HACH_TOAN"
							  FROM sale_ex_document_invoice_rel R
								  JOIN tim_kiem_so_chung_tu V
									  ON R."sale_document_id" = V."ID_CHUNG_TU" AND V."MODEL_CHUNG_TU" = 'sale.ex.hoa.don.ban.hang'
								 --WHERE     ReferenceType <> 0
							 ) V
				;
			
				DROP TABLE IF EXISTS TMP_SO_CHUNG_TU_GOC
				;
			
				CREATE TEMP TABLE TMP_SO_CHUNG_TU_GOC
					AS
						SELECT
							R1."ID_CHUNG_TU"
							, R1."MODEL_CHUNG_TU_HD"
							, "PHAN_TRAM_TGTGT"
							, (SELECT string_agg(A."SO_CHUNG_TU", ',')
							   FROM (SELECT "SO_CHUNG_TU"
									 FROM TMP_SO_CHUNG_TU AS R2
									 WHERE R2."ID_CHUNG_TU" = R1."ID_CHUNG_TU"
										   AND
										   R2."MODEL_CHUNG_TU_HD" = R1."MODEL_CHUNG_TU_HD"
										   AND R2."PHAN_TRAM_TGTGT" = R1."PHAN_TRAM_TGTGT"
			
									 ORDER BY
										 R2."SO_CHUNG_TU") A
			
			
							  )   AS "SO_CHUNG_TU"
			
			
							, CASE WHEN CR."COUNT_SO_CHUNG_TU" > 1
							THEN NULL
							  ELSE "DIEN_GIAI"
							  END AS "DIEN_GIAI"
							, "NGAY_CHUNG_TU"
							, "NGAY_HACH_TOAN"
						FROM TMP_SO_CHUNG_TU AS R1
							LEFT JOIN LATERAL ( SELECT COUNT(DISTINCT "SO_CHUNG_TU") AS "COUNT_SO_CHUNG_TU"
												FROM TMP_SO_CHUNG_TU R
												WHERE R."ID_CHUNG_TU" = R1."ID_CHUNG_TU"
													  AND R."MODEL_CHUNG_TU_HD" = R1."MODEL_CHUNG_TU_HD"
									  ) AS CR ON TRUE
			
				;
			
			
				-- -------------------------------------
			
				--         UPDATE  TMP_KET_QUA R
				--         SET     "SO_CHUNG_TU" = COALESCE(F."SO_CHUNG_TU", R."SO_CHUNG_TU")
				--
				--          FROM     TMP_SO_CHUNG_TU_GOC AS F
				--                 WHERE R."ID_CHUNG_TU" = F."ID_CHUNG_TU" AND R."MODEL_CHUNG_TU"  =F."MODEL_CHUNG_TU_HD";
			
			
				-- ---------------------------------------------------
				DROP TABLE IF EXISTS TMP_KET_QUA_1
				;
			
				CREATE TABLE TMP_KET_QUA_1
				(
					"NHOM_HHDV"                 VARCHAR(500),
					"THUE_SUAT"                 DECIMAL(18, 4),
					"MAU_SO_HOA_DON"            VARCHAR(127),
					"KY_HIEU_HOA_DON"           VARCHAR(255),
					"SO_HOA_DON"                VARCHAR(100),
					"NGAY_HOA_DON"              DATE,
					"ID_CHUNG_TU"               INT,
					"MODEL_CHUNG_TU"            VARCHAR(100),
			
					"TEN_NGUOI_MUA"             VARCHAR(255),
			
					"MA_SO_THUE_NGUOI_MUA"      VARCHAR(127),
					"MAT_HANG"                  VARCHAR(255),
			
					"DOANH_SO_BAN_CHUA_CO_THUE" DECIMAL(18, 4),
					"THUE_GTGT"                 DECIMAL(18, 4),
					"TK_THUE"                   VARCHAR(255)
			
				)
				;
			
			
				IF v_cong_gop_theo_tung_hoa_don = 0
				THEN
			
					IF v_lay_so_lieu_dvt_so_luong_don_gia = 1
					THEN
						INSERT INTO TMP_KET_QUA_1
						("NHOM_HHDV",
						 "THUE_SUAT",
						 "MAU_SO_HOA_DON",
						 "KY_HIEU_HOA_DON",
						 "SO_HOA_DON",
						 "NGAY_HOA_DON",
						 "ID_CHUNG_TU",
						 "MODEL_CHUNG_TU",
						 "TEN_NGUOI_MUA",
						 "MA_SO_THUE_NGUOI_MUA",
						 "MAT_HANG",
			
						 "DOANH_SO_BAN_CHUA_CO_THUE",
						 "THUE_GTGT",
						 "TK_THUE"
			
						)
							SELECT
								"NHOM_HHDV"
								, "THUE_SUAT"
								, "MAU_SO_HOA_DON"
								, "KY_HIEU_HOA_DON"
								, "SO_HOA_DON"
								, "NGAY_HOA_DON"
								, "ID_CHUNG_TU"
								, "MODEL_CHUNG_TU"
								, "TEN_NGUOI_MUA"
								, "MA_SO_THUE_NGUOI_MUA"
								, "MAT_HANG"
								, "DOANH_SO_BAN_CHUA_CO_THUE"
								, "THUE_GTGT"
								, "TK_THUE"
			
							FROM TMP_KET_QUA R
								LEFT JOIN tim_kiem_so_chung_tu_chi_tiet
									AS V ON V.id = R."CHI_TIET_ID" AND V."MODEL_CHI_TIET" = R."CHI_TIET_MODEL"
						;
			
					ELSE
						INSERT INTO TMP_KET_QUA_1
						(
							"NHOM_HHDV",
							"THUE_SUAT",
							"MAU_SO_HOA_DON",
							"KY_HIEU_HOA_DON",
							"SO_HOA_DON",
							"NGAY_HOA_DON",
							"ID_CHUNG_TU",
							"MODEL_CHUNG_TU",
							"TEN_NGUOI_MUA",
							"MA_SO_THUE_NGUOI_MUA",
							"MAT_HANG",
			
							"DOANH_SO_BAN_CHUA_CO_THUE",
							"THUE_GTGT",
							"TK_THUE"
						)
							SELECT
								"NHOM_HHDV"
								, "THUE_SUAT"
								, "MAU_SO_HOA_DON"
								, "KY_HIEU_HOA_DON"
								, "SO_HOA_DON"
								, "NGAY_HOA_DON"
								, "ID_CHUNG_TU"
								, "MODEL_CHUNG_TU"
								, "TEN_NGUOI_MUA"
								, "MA_SO_THUE_NGUOI_MUA"
								, "MAT_HANG"
								, "DOANH_SO_BAN_CHUA_CO_THUE"
								, "THUE_GTGT"
								, "TK_THUE"
							FROM TMP_KET_QUA R
			
						;
					END IF
					;
			
			
				ELSE -- IF v_cong_gop_theo_tung_hoa_don = 0
			
			
					INSERT INTO TMP_KET_QUA_1
					(
						"NHOM_HHDV",
						"THUE_SUAT",
						"MAU_SO_HOA_DON",
						"KY_HIEU_HOA_DON",
						"SO_HOA_DON",
						"NGAY_HOA_DON",
						"ID_CHUNG_TU",
						"MODEL_CHUNG_TU",
						"TEN_NGUOI_MUA",
						"MA_SO_THUE_NGUOI_MUA",
						"MAT_HANG",
			
						"DOANH_SO_BAN_CHUA_CO_THUE",
						"THUE_GTGT",
						"TK_THUE"
					)
						SELECT
						"NHOM_HHDV"
						 , "THUE_SUAT"
						 , "MAU_SO_HOA_DON"
						 , "KY_HIEU_HOA_DON"
						 , "SO_HOA_DON"
						 , "NGAY_HOA_DON"
						 , "ID_CHUNG_TU"
						 , "MODEL_CHUNG_TU"
			
						 , "TEN_NGUOI_MUA"
						 , "MA_SO_THUE_NGUOI_MUA"
						 ,  "MAT_HANG"
						 , SUM("DOANH_SO_BAN_CHUA_CO_THUE") AS "DOANH_SO_BAN_CHUA_CO_THUE"
			
						 , SUM("THUE_GTGT") AS "THUE_GTGT"
						 , NULL AS "TK_THUE"
			
			FROM (
					 SELECT
						 "NHOM_HHDV"
						 , "THUE_SUAT"
						 , "MAU_SO_HOA_DON"
						 , "KY_HIEU_HOA_DON"
						 , "SO_HOA_DON"
						 , "NGAY_HOA_DON"
						 , CASE
						   WHEN Temp5."Count_ID_CHUNG_TU" > 1
							   THEN NULL
						   ELSE R1."ID_CHUNG_TU"
						   END  AS "ID_CHUNG_TU"
						 , CASE WHEN Temp6."Count_MODEL_CHUNG_TU" > 1
						 THEN NULL
						   ELSE R1."MODEL_CHUNG_TU"
						   END  AS "MODEL_CHUNG_TU"
			
						 , R1."TEN_NGUOI_MUA"
						 , R1."MA_SO_THUE_NGUOI_MUA"
						 , (SELECT "MAT_HANG"
							FROM TMP_KET_QUA R2
							WHERE (R2."ID_CHUNG_TU" = (CASE
													   WHEN Temp5."Count_ID_CHUNG_TU" > 1
														   THEN NULL
													   ELSE R1."ID_CHUNG_TU"
													   END)
								   OR Temp5."Count_ID_CHUNG_TU" > 1
			
			
								  )
								  AND
								  (R2."MODEL_CHUNG_TU" = (CASE
														  WHEN Temp6."Count_MODEL_CHUNG_TU" > 1
															  THEN NULL
														  ELSE R1."MODEL_CHUNG_TU"
														  END)
								   OR Temp6."Count_MODEL_CHUNG_TU" > 1
			
			
								  )
								  AND COALESCE(R2."SO_HOA_DON", '') = COALESCE(R1."SO_HOA_DON",
																			   '')
								  AND (R2."NGAY_HOA_DON" = R1."NGAY_HOA_DON"
									   OR R2."NGAY_HOA_DON" IS NULL
										  AND R1."NGAY_HOA_DON" IS NULL
								  )
								  AND COALESCE(R2."KY_HIEU_HOA_DON", '') = COALESCE(R1."KY_HIEU_HOA_DON",
																					'')
								  AND COALESCE(R2."MAU_SO_HOA_DON", '') = COALESCE(R1."MAU_SO_HOA_DON",
																				   '')
								  AND COALESCE(R2."TEN_NGUOI_MUA",
											   '') = COALESCE(R1."TEN_NGUOI_MUA",
															  '')
								  AND R2."THUE_SUAT" = R1."THUE_SUAT"
			
							ORDER BY ABS("DOANH_SO_BAN_CHUA_CO_THUE") DESC
							FETCH FIRST 1 ROW ONLY
						   )    AS "MAT_HANG"
						 , R1."DOANH_SO_BAN_CHUA_CO_THUE"
			
						 , R1."THUE_GTGT"
						 , NULL AS "TK_THUE"
			
			
					 FROM TMP_KET_QUA R1
			
			
						 LEFT JOIN LATERAL ( SELECT COUNT(DISTINCT A."ID_CHUNG_TU") AS "Count_ID_CHUNG_TU"
											 FROM TMP_KET_QUA A
											 WHERE A."JoinKey" = R1."JoinKey"
								   ) Temp5 ON TRUE
						 LEFT JOIN LATERAL ( SELECT COUNT(DISTINCT A."MODEL_CHUNG_TU") AS "Count_MODEL_CHUNG_TU"
											 FROM TMP_KET_QUA A
											 WHERE A."JoinKey" = R1."JoinKey"
								   ) Temp6 ON TRUE) A
			GROUP BY
			
				"NHOM_HHDV",
				"THUE_SUAT",
				"SO_HOA_DON",
				"NGAY_HOA_DON",
				"KY_HIEU_HOA_DON",
				"MAU_SO_HOA_DON",
				 "MAT_HANG"
				 , "ID_CHUNG_TU"
				 , "MODEL_CHUNG_TU",
				"TEN_NGUOI_MUA",
				"MA_SO_THUE_NGUOI_MUA"
			
					;
			
			
				END IF
				;
			
			END $$
			;
			
			
			SELECT
				  ROW_NUMBER()
				  OVER (
				ORDER BY R."NHOM_HHDV", R."NGAY_HOA_DON", R."SO_HOA_DON" ) AS RowNum
				, "NHOM_HHDV" AS "NHOM_HHDV_BAN_RA"
				, "SO_HOA_DON"
				, "NGAY_HOA_DON"
			
				, "ID_CHUNG_TU" AS "ID_GOC"
				, "MODEL_CHUNG_TU"   AS "MODEL_GOC"
				, "TEN_NGUOI_MUA"
				, "MA_SO_THUE_NGUOI_MUA" AS "MA_SO_THUE_NGUOI_MUA"
				, "MAT_HANG"
				, "DOANH_SO_BAN_CHUA_CO_THUE"  AS "DOANH_SO_BAN_CHUA_CO_THUE_GTGT"
			
				, "THUE_GTGT"
				, "TK_THUE"
			FROM TMP_KET_QUA_1 AS R
			OFFSET %(offset)s
			LIMIT %(limit)s;

			""" 
		return self.execute(query,params_sql)

	### END IMPLEMENTING CODE ###

	def _action_view_report(self):
		self._validate()
		TU = self.get_vntime('TU')
		DEN = self.get_vntime('DEN')
		param = 'Từ ngày: %s đến ngày %s' % (TU, DEN)
		action = self.env.ref('bao_cao.open_report_bang_ke_hoa_don_chung_tu_ban_ra').read()[0]
		# action['options'] = {'clear_breadcrumbs': True}
		action['context'] = eval(action.get('context','{}'))
		action['context'].update({'breadcrumb_ex': param})
		return action

class BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_BAN_RA_GROUP(models.Model):
	_name = 'bang.ke.hoa.don.chung.tu.ban.ra.group'
	_auto = False
	_description = 'Nhóm các hóa đơn chứng từ theo Nhóm HHDV'

	NHOM_HHDV_BAN_RA = fields.Char()
	
	sum_DOANH_SO_BAN_CHUA_CO_THUE_GTGT = fields.Monetary(currency_field='base_currency_id')
	sum_THUE_GTGT = fields.Monetary(currency_field='base_currency_id')
	base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)
	data = fields.One2many('bang.ke.hoa.don.chung.tu.ban.ra', 'BANG_KE_HOA_DON_CT_GROUP_ID')

		
class BAO_CAO_BANG_KE_HOA_DON_CHUNG_TU_BAN_RA_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_bang_ke_hoa_don_chung_tu_ban_ra'

	TONG_DOANH_SO_BAN_CHUA_CO_THUE_GTGT = fields.Monetary(currency_field='base_currency_id')
	TONG_THUE_GTGT = fields.Monetary(currency_field='base_currency_id')
	base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)
	

	@api.model
	def get_report_values(self, docids, data=None):
		env = self.env[data.get('model')]
		docs = [env.new(d) for d in env.with_context(data.get('context')).search_read()]
		
		grouped_data = {}
		for record in docs:
			nhom_hhdv_ban_ra = record.NHOM_HHDV_BAN_RA
			if not grouped_data.get(nhom_hhdv_ban_ra):
				grouped_data[nhom_hhdv_ban_ra] = self.env['bang.ke.hoa.don.chung.tu.ban.ra.group'].new({
					'data': [],
					'sum_DOANH_SO_BAN_CHUA_CO_THUE_GTGT': 0,
					'sum_THUE_GTGT': 0,
					
					'NHOM_HHDV_BAN_RA': record.NHOM_HHDV_BAN_RA or '',
				})

			grouped_data[nhom_hhdv_ban_ra].data += record
			grouped_data[nhom_hhdv_ban_ra].sum_DOANH_SO_BAN_CHUA_CO_THUE_GTGT += record.DOANH_SO_BAN_CHUA_CO_THUE_GTGT
			grouped_data[nhom_hhdv_ban_ra].sum_THUE_GTGT += record.THUE_GTGT
			

		added_data = {
			'tieu_de_nguoi_ky': self.get_danh_sach_tieu_de_nguoi_ky(data.get('model')),
			'ten_nguoi_ky': self.get_danh_sach_ten_nguoi_ky(data.get('model')),
			'sub_title': data.get('breadcrumb'),

		}

		tong_sum_DOANH_SO_BAN_CHUA_CO_THUE_GTGT = 0
		tong_THUE_GTGT = 0
		for nhom_hhdv_ban_ra in grouped_data:
			tong_sum_DOANH_SO_BAN_CHUA_CO_THUE_GTGT += grouped_data[nhom_hhdv_ban_ra].sum_DOANH_SO_BAN_CHUA_CO_THUE_GTGT
			tong_THUE_GTGT += grouped_data[nhom_hhdv_ban_ra].sum_THUE_GTGT
		
		tong_all = self.env['report.bao_cao.template_bang_ke_hoa_don_chung_tu_ban_ra'].new({
			'TONG_DOANH_SO_BAN_CHUA_CO_THUE_GTGT': tong_sum_DOANH_SO_BAN_CHUA_CO_THUE_GTGT,
			'TONG_THUE_GTGT': tong_THUE_GTGT,
			})
			
		return {
			'docs': docs,
			'grouped_data': grouped_data,
			'added_data': added_data,
			'o': tong_all,
		}