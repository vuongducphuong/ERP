# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision

class BAO_CAO_TONG_HOP_TON_KHO(models.Model):
	_name = 'bao.cao.tong.hop.ton.kho'
	
	
	_auto = False

	THONG_KE_THEO = fields.Selection([('KHONG_CHON', '<<Không chọn>>'), ('TONG_HOP_TREN_NHIEU_KHO', 'Tổng hợp trên nhiều kho'), ('HAN_SU_DUNG', 'Hạn sử dụng'), ('SO_LO', ' Số lô'),], string='Thống kê theo', help='Thống kê theo',default='KHONG_CHON')
	# THONG_KE_THEO = fields.Selection([('KHONG_CHON', '<<Không chọn>>'), ('TONG_HOP_TREN_NHIEU_KHO', 'Tổng hợp trên nhiều kho'), ('HAN_SU_DUNG', 'Hạn sử dụng'), ('SO_LO', ' Số lô'), ('MA_QUY_CACH', 'Mã quy cách'), ], string='Thống kê theo', help='Thống kê theo',default='KHONG_CHON')
	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
	BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
	KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default='DAU_THANG_DEN_HIEN_TAI')
	TU = fields.Date(string='Từ', help='Từ',default=fields.Datetime.now)
	DEN = fields.Date(string='Đến', help='Đến',default=fields.Datetime.now)
	NHOM_VTHH_ID = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm VTHH', help='Nhóm vật tư hàng hóa')
	DON_VI_TINH = fields.Selection([('0', 'Đơn vị tính chính'), ('1', 'Đơn vị chuyển đổi 1'), ('2', 'Đơn vị chuyển đổi 2'), ], string='Đơn vị tính', help='Đơn vị tính',default='0')
	KHO_ID_MASTER = fields.Many2one('danh.muc.kho', string='Kho', help='Kho')
	# HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Hàng', help='Hàng')
	MA_HANG = fields.Char(string='Mã hàng', help='Mã hàng')
	TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng')
	TEN_KHO = fields.Char(string='Tên kho', help='Tên kho')
	MA_KHO = fields.Char(string='Mã kho', help='Mã kho')

	DVT = fields.Char(string='ĐVT', help='Đơn vị tính')
	SO_LUONG_DAU_KY = fields.Float(string='Số lượng', help='Số lượng đầu kỳ', digits=decimal_precision.get_precision('SO_LUONG'))
	GIA_TRI_DAU_KY = fields.Float(string='Giá trị', help='Giá trị đầu kỳ',digits= decimal_precision.get_precision('VND'))
	SO_LUONG_NHAP_KHO = fields.Float(string='Số lượng', help='Số lượng nhập kho', digits=decimal_precision.get_precision('SO_LUONG'))
	GIA_TRI_NHAP_KHO = fields.Float(string='Giá trị', help='Giá trị nhập kho',digits= decimal_precision.get_precision('VND'))
	SO_LUONG_XUAT_KHO = fields.Float(string='Số lượng', help='Số lượng xuất kho', digits=decimal_precision.get_precision('SO_LUONG'))
	GIA_TRI_XUAT = fields.Float(string='Giá trị', help='Giá trị xuất kho',digits= decimal_precision.get_precision('VND'))
	SO_LUONG_CUOI_KY = fields.Float(string='Số lượng', help='Số luộng cuối kỳ', digits=decimal_precision.get_precision('SO_LUONG'))
	GIA_TRI_CUOI_KY = fields.Float(string='Giá trị', help='Giá trị cuối kỳ',digits= decimal_precision.get_precision('VND'))


	SO_LO = fields.Char(string='Số lô', help='Số lô')
	HAN_SU_DUNG = fields.Date(string='Hạn sử dụng', help='Hạn sử dụng')
	SO_LUONG_TON = fields.Float(string='Số lượng tồn', help='Số lượng tồn', digits=decimal_precision.get_precision('SO_LUONG'))
	NHOM_HAN_SU_DUNG = fields.Char(string='Nhóm hạn sử dụng', help='Nhóm hạn sử dụng')
	SO_NGAY_CON_HAN = fields.Integer(string='Số ngày còn hạn', help='Số ngày còn hạn')
	SO_NGAY_QUA_HAN = fields.Integer(string='Số ngày quá hạn', help='Số ngày quá hạn')
	MA_QUY_CACH_1 = fields.Char(string='Mã quy cách 1', help='Mã quy cách 1')
	MA_QUY_CACH_2 = fields.Char(string='Mã quy cách 2', help='Mã quy cách 2')
	SL_TON_DAU_KY = fields.Integer(string='Sl tồn đầu kỳ', help='Sl tồn đầu kỳ')
	SO_LUONG_NHAP = fields.Float(string='Số lượng nhập', help='Số lượng nhập', digits=decimal_precision.get_precision('SO_LUONG'))
	SO_LUONG_XUAT = fields.Float(string='Số lượng xuất', help='Số lượng xuất', digits=decimal_precision.get_precision('SO_LUONG'))
	SL_TON_CUOI_KY = fields.Integer(string='Sl tồn cuối kỳ', help='Sl tồn cuối kỳ')
	GIA_TRI_TON = fields.Float(string='Giá trị tồn', help='Giá trị tồn')

	KHO_IDS = fields.One2many('danh.muc.kho')
	CHON_TAT_CA_KHO = fields.Boolean('Tất cả kho', default=True)
	KHO_MANY_IDS = fields.Many2many('danh.muc.kho','tong_hop_ton_kho_danh_muc_kho', string='Chọn kho')
   
	HANG_IDS = fields.One2many('danh.muc.vat.tu.hang.hoa')
	CHON_TAT_CA_SAN_PHAM = fields.Boolean('Tất cả sản phẩm', default=True)
	SAN_PHAM_MANY_IDS = fields.Many2many('danh.muc.vat.tu.hang.hoa','tong_hop_ton_kho_danh_muc_vthh', string='Chọn sản phẩm')
	MA_PC_NHOM_VTHH = fields.Char()

	@api.onchange('HANG_IDS')
	def update_SAN_PHAM_IDS(self):
		self.SAN_PHAM_MANY_IDS = self.HANG_IDS.ids
	   
	@api.onchange('NHOM_VTHH_ID')
	def update_NHOM_VTHH_ID(self):
		self.SAN_PHAM_MANY_IDS = []
		self.MA_PC_NHOM_VTHH =self.NHOM_VTHH_ID.MA_PHAN_CAP

	@api.onchange('SAN_PHAM_MANY_IDS')
	def _onchange_SAN_PHAM_MANY_IDS(self):
		self.HANG_IDS = self.SAN_PHAM_MANY_IDS.ids
	
	@api.onchange('KHO_IDS')
	def update_KHO_IDS(self):
		self.KHO_MANY_IDS = self.KHO_IDS.ids
	
	@api.onchange('KHO_MANY_IDS')
	def _onchange_KHO_MANY_IDS(self):
		self.KHO_IDS = self.KHO_MANY_IDS.ids

	@api.onchange('THONG_KE_THEO')
	def _onchange_THONG_KE_THEO(self):

		self.NHOM_VTHH_ID = False
		self.CHON_TAT_CA_SAN_PHAM = True
		self.CHON_TAT_CA_KHO = True
	   
		self.SAN_PHAM_MANY_IDS = []
		self.KHO_MANY_IDS = []

	def _validate(self):
		params = self._context
		THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
		TU_NGAY = params['TU'] if 'TU' in params.keys() else 'False'
		TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		DEN_NGAY = params['DEN'] if 'DEN' in params.keys() else 'False'
		DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

		CHON_TAT_CA_SAN_PHAM = params['CHON_TAT_CA_SAN_PHAM'] if 'CHON_TAT_CA_SAN_PHAM' in params.keys() else 'False'
		CHON_TAT_CA_KHO = params['CHON_TAT_CA_KHO'] if 'CHON_TAT_CA_KHO' in params.keys() else 'False'
	   
		SAN_PHAM_MANY_IDS = params['SAN_PHAM_MANY_IDS'] if 'SAN_PHAM_MANY_IDS' in params.keys() else 'False'
		KHO_MANY_IDS = params['KHO_MANY_IDS'] if 'KHO_MANY_IDS' in params.keys() else 'False'
		
		if(TU_NGAY=='False'):
			raise ValidationError('<Từ ngày> không được bỏ trống.')
		elif(DEN_NGAY=='False'):
			raise ValidationError('<Đến ngày> không được bỏ trống.')
		elif(TU_NGAY_F > DEN_NGAY_F):
			raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')

		if THONG_KE_THEO in ('KHONG_CHON','TONG_HOP_TREN_NHIEU_KHO','HAN_SU_DUNG','SO_LO'):
			if CHON_TAT_CA_KHO == 'False':
				if KHO_MANY_IDS == []:
					raise ValidationError('Bạn chưa chọn <Kho>. Xin vui lòng chọn lại.')

		# if THONG_KE_THEO == 'MA_QUY_CACH':
		#     if CHON_TAT_CA_SAN_PHAM == 'False':
		#         if KHO_MANY_IDS == []:
		#             raise ValidationError('Bạn chưa chọn <Kho>. Xin vui lòng chọn lại.')
	
		
	@api.model
	def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
		record = []
		# Get paramerters here
		params = self._context
		if not params.get('active_model'):
			return
		THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
		HIEN_THI = params['selection_tong_hop_tren_nhieu_kho'] if 'selection_tong_hop_tren_nhieu_kho' in params.keys() else 'False'
		CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
		BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC =  1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
		KY_BAO_CAO = params['KY_BAO_CAO'] if 'KY_BAO_CAO' in params.keys() else 'False'
		TU_NGAY = params['TU'] if 'TU' in params.keys() else 'False'
		TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		DEN_NGAY = params['DEN'] if 'DEN' in params.keys() else 'False'
		DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		NHOM_VTHH_ID = params['NHOM_VTHH_ID'] if 'NHOM_VTHH_ID' in params.keys() and params['NHOM_VTHH_ID'] != 'False' else None
		DON_VI_TINH = params['DON_VI_TINH'] if 'DON_VI_TINH' in params.keys() else 'False'

		if params.get('CHON_TAT_CA_KHO'):
			domain = []
			KHO_IDS =  self.env['danh.muc.kho'].search(domain).ids
		else:
			KHO_IDS =  params.get('KHO_MANY_IDS')


		params_sql = {
			'TU_NGAY':TU_NGAY_F, 
			'DEN_NGAY':DEN_NGAY_F, 
			'KHO_IDS' : KHO_IDS or None,
			# 'SAN_PHAM_IDS' : SAN_PHAM_IDS,
			'CHI_NHANH_ID' : CHI_NHANH_ID,
			'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' : BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
			'DON_VI_TINH' : int(DON_VI_TINH),
			'NHOM_VTHH_ID' : NHOM_VTHH_ID,
			'HIEN_THI' : int(HIEN_THI),
		}

		# Thống kê theo không chọn
		if THONG_KE_THEO=='KHONG_CHON' :
			return self._lay_bao_theo_khong_chon(params_sql)

		# Thống kê theo Tổng hợp trên nhiều kho
		elif THONG_KE_THEO=='TONG_HOP_TREN_NHIEU_KHO' :
			return self._lay_bao_cao_tong_hop_tren_nhieu_kho(params_sql)

		# Thống kê theo Hạn sử dụng
		elif THONG_KE_THEO=='HAN_SU_DUNG' :
			return self._lay_bao_cao_theo_han_su_dung(params_sql)
		# Thống kê theo Số lô
		elif THONG_KE_THEO=='SO_LO' :
			return self._lay_bao_cao_theo_so_lo(params_sql)

	def _lay_bao_theo_khong_chon(self, params_sql):      
		record = []
		query = """
				DO LANGUAGE plpgsql $$
				DECLARE
				tu_ngay                             DATE := %(TU_NGAY)s;

				--%(TU_NGAY)s

				den_ngay                            DATE := %(DEN_NGAY)s;

				--%(DEN_NGAY)s

				bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

				--%(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s

				chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

				--%(CHI_NHANH_ID)s


				don_vi_tinh                         INTEGER := %(DON_VI_TINH)s;

				nhom_vthh_id                        INTEGER := %(NHOM_VTHH_ID)s;


				KHO_IDS                             INTEGER := -1;


				rec                                 RECORD;

				CHE_DO_KE_TOAN                      INTEGER;

				PHAN_THAP_PHAN_SO_LUONG             INTEGER:=2;

				MA_PHAN_CAP_VTHH                    VARCHAR(100);


				BEGIN


				SELECT value
				INTO CHE_DO_KE_TOAN
				FROM ir_config_parameter
				WHERE key = 'he_thong.CHE_DO_KE_TOAN'
				FETCH FIRST 1 ROW ONLY
				;

				--     SELECT value
				--     INTO PHAN_THAP_PHAN_SO_LUONG
				--     FROM ir_config_parameter
				--     WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
				--     FETCH FIRST 1 ROW ONLY
				--     ;

				SELECT "MA_PHAN_CAP"
				INTO MA_PHAN_CAP_VTHH
				FROM danh_muc_nhom_vat_tu_hang_hoa_dich_vu

				WHERE id = nhom_vthh_id
				;


				DROP TABLE IF EXISTS TMP_KHO
				;

				CREATE TEMP TABLE TMP_KHO
				AS
				SELECT
				"id" AS "KHO_ID"
				, "MA_KHO"
				, "TEN_KHO"
				FROM danh_muc_kho S

				WHERE (id = any(%(KHO_IDS)s))----%(KHO_IDS)s

				;


				DROP TABLE IF EXISTS TMP_KET_QUA
				;

				CREATE TEMP TABLE TMP_KET_QUA
				AS
				SELECT
				S."KHO_ID"
				, --S.StockID
				S."MA_KHO"
				, --S.StockCode
				S."TEN_KHO"
				, --S.StockName
				I."id"                                                    AS "MA_HANG_ID"
				, I."MA"
				, I."TEN"
				, U."DON_VI_TINH"
				, COALESCE(IIUC."DON_GIA_BAN_1", I."GIA_BAN_1")             AS "GIA_BAN_1"
				, --						ISNULL(IIUC."DON_GIA_BAN_1",--I.SalePrice1)
				COALESCE(IIUC."DON_GIA_BAN_2", I."GIA_BAN_2")             AS "GIA_BAN_2"
				, --						ISNULL(IIUC."DON_GIA_BAN_2",--I.SalePrice2)
				COALESCE(IIUC."DON_GIA_BAN_3", I."GIA_BAN_3")             AS "GIA_BAN_3"
				, --						ISNULL(IIUC."DON_GIA_BAN_3",--I.SalePrice3)
				COALESCE(IIUC."DON_GIA_CO_DINH", I."GIA_CO_DINH")         AS "GIA_CO_DINH"
				, --						ISNULL(IIUC."DON_GIA_CO_DINH",--I.FixedSalePrice)
				-- Đầu kỳ

				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" >= tu_ngay
				THEN 0 --@FromDate
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_NHAP"
				- IL."SO_LUONG_XUAT"
				ELSE (IL."SO_LUONG_NHAP_THEO_DVT_CHINH"--IL.MainInwardQuantity
				- IL."SO_LUONG_XUAT_THEO_DVT_CHINH")--IL.MainOutwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1) --ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SO_LUONG_DAU_KY"
				, --@QuantityDecimalDigits)--OriginalQuantity
				SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay --@FromDate
				THEN IL."SO_TIEN_NHAP" - IL."SO_TIEN_XUAT"
				ELSE 0
				END)                                                  AS "GIA_TRI_DAU_KY"
				, --OriginalAmount
				-- Nhập trong kỳ

				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay--@FromDate
				OR IL."LOAI_CHUNG_TU" <> '2010'
				THEN 0
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_NHAP"
				ELSE IL."SO_LUONG_NHAP_THEO_DVT_CHINH"--IL.MainInwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
				--ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SO_LUONG_NHAP_THANH_PHAM"
				, --@QuantityDecimalDigits)--ProductInQuantity

				SUM(CASE WHEN (IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND
				IL."LOAI_CHUNG_TU" = '2010' --@FromDate--@ToDate)
				THEN IL."SO_TIEN_NHAP"
				ELSE 0
				END)                                                  AS "GIA_TRI_NHAP_THANH_PHAM"
				, --ProductInAmount
				----------------------------------------------------

				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay--@FromDate
				OR IL."LOAI_CHUNG_TU" NOT IN ('2011', '2012')
				THEN 0
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_NHAP"
				ELSE IL."SO_LUONG_NHAP_THEO_DVT_CHINH"--IL.MainInwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
				--ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SL_NHAP_THANH_PHAM_LR_TD"
				, --@QuantityDecimalDigits)--ProductCollapsingInQuantity
				-- nhyen - 7/9/2017 (CR 94462): Giá trị lắp ráp tháo rỡ
				SUM(CASE WHEN (IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND
				IL."LOAI_CHUNG_TU" IN ('2011', '2012') --@FromDate--@ToDate)
				THEN IL."SO_TIEN_NHAP"
				ELSE 0
				END)                                                  AS "GT_NHAP_THANH_PHAM_LR_TD"
				, --ProductCollapsingInAmount
				--------------------------------------
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				WHEN IL."LOAI_CHUNG_TU" <> '2014'
				THEN 0
				WHEN IL."MA_TK_NO" NOT LIKE '152%%'
				AND IL."MA_TK_NO" NOT LIKE '153%%'
				THEN 0
				WHEN (CHE_DO_KE_TOAN = '15'--@AccountingSystem
				AND IL."MA_TK_CO" NOT LIKE '621%%'
				AND IL."MA_TK_CO" NOT LIKE '627%%'
				AND IL."MA_TK_CO" NOT LIKE '623%%'
				)
				OR (CHE_DO_KE_TOAN = '48'--@AccountingSystem
				AND IL."MA_TK_CO" NOT LIKE '154%%'
				)
				THEN 0
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_NHAP"
				ELSE IL."SO_LUONG_NHAP_THEO_DVT_CHINH"--IL.MainInwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1) --ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SL_NVL_NHAP_LAI"
				, -- SL NVL nhập lại--@QuantityDecimalDigits)--MaterialInQuantity

				SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				WHEN IL."LOAI_CHUNG_TU" <> '2014'
				THEN 0
				WHEN IL."MA_TK_NO" NOT LIKE '152%%' AND IL."MA_TK_NO" NOT LIKE '153%%'
				THEN 0
				WHEN (CHE_DO_KE_TOAN = '15'--@AccountingSystem
				AND IL."MA_TK_CO" NOT LIKE '621%%'
				AND IL."MA_TK_CO" NOT LIKE '627%%'
				AND IL."MA_TK_CO" NOT LIKE '623%%'
				) OR (CHE_DO_KE_TOAN = '48'--@AccountingSystem
				AND IL."MA_TK_CO" NOT LIKE '154%%')
				THEN 0
				ELSE IL."SO_TIEN_NHAP"
				END)                                                  AS "GT_NVL_NHAP_LAI"
				, --MaterialInAmount
				----------------------------------------------
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				WHEN IL."LOAI_CHUNG_TU" NOT IN ('302', '307', '308',
				'309', '310', '318',
				'319', '320', '321',
				'322',
				'352', -- nmtruong 7/12/2015: thêm các chứng từ nhập kho nhiều hóa đơn
				'357',
				'358',
				'359',
				'360',
				'368',
				'369',
				'370',
				'371',
				'372')
				THEN 0
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_NHAP"
				ELSE IL."SO_LUONG_NHAP_THEO_DVT_CHINH"--IL.MainInwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1) --ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SO_LUONG_MUA_HANG"
				, --Mua hàng--@QuantityDecimalDigits)--PUVoucherQuantity

				SUM(CASE WHEN (IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)--@FromDate--@ToDate)
				AND IL."LOAI_CHUNG_TU" IN
				('302', '307', '308', '309', '310', '318', '319', '320', '321', '322', '352', '357', '358', '359', '360', '368', '369', '370', '371', '372')
				THEN IL."SO_TIEN_NHAP"
				ELSE 0
				END)                                                  AS "GIA_TRI_MUA_HANG"
				, --PUVoucherAmount
				-----------------------------------------------
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				WHEN IL."LOAI_CHUNG_TU" <> '2013'
				THEN 0
				WHEN IL."LA_HANG_KHUYEN_MAI" <> '1'
				THEN 0
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_NHAP"
				ELSE IL."SO_LUONG_NHAP_THEO_DVT_CHINH"--IL.MainInwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1) --ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SL_BAN_KM_TRA_LAI"
				, --Bán trả lại KM--@QuantityDecimalDigits)--SAReturnPromotionQuantity

				SUM(CASE WHEN (IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)--@FromDate--@ToDate)
				AND IL."LOAI_CHUNG_TU" = '2013'
				AND IL."LA_HANG_KHUYEN_MAI" = '1'
				THEN IL."SO_TIEN_NHAP"
				ELSE 0
				END)                                                  AS "GT_BAN_KM_TRA_LAI"
				, --Bán trả lại KM--SAReturnPromotionAmount
				---------------------------------------------------
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				WHEN IL."LOAI_CHUNG_TU" <> '2013'
				THEN 0
				WHEN IL."LA_HANG_KHUYEN_MAI" <> '0'
				THEN 0
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_NHAP"
				ELSE IL."SO_LUONG_NHAP_THEO_DVT_CHINH"--IL.MainInwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1) --ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SL_BAN_TRA_LAI"
				, -- Bán trả lại khác--@QuantityDecimalDigits)

				SUM(CASE WHEN (IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)--@FromDate--@ToDate)
				AND IL."LOAI_CHUNG_TU" = '2013'
				AND IL."LA_HANG_KHUYEN_MAI" = '0'
				THEN IL."SO_TIEN_NHAP"
				ELSE 0
				END)                                                  AS "GT_BAN_TRA_LAI"
				, --SAReturnAmount
				---------------------------------------------------
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				WHEN IL."LOAI_CHUNG_TU" NOT IN ('2030', '2031',
				'2032')
				THEN 0
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_NHAP"
				ELSE IL."SO_LUONG_NHAP_THEO_DVT_CHINH"--IL.MainInwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1) --ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SL_DIEU_CHUYEN"
				, --Điều chuyển--@QuantityDecimalDigits)--TransferInQuantity

				SUM(CASE WHEN (IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND
				IL."LOAI_CHUNG_TU" IN ('2030', '2031', '2032') --@FromDate--@ToDate)
				THEN IL."SO_TIEN_NHAP"
				ELSE 0
				END)                                                  AS "GT_DIEU_CHUYEN"
				, --TransferInAmount
				--------------------------------------------------------------
				/*
				2016	Nhập kho từ kiểm kê (Có điều chỉnh giá trị)
				2027	Xuất kho từ kiểm kê (Có điều chỉnh giá trị)
				*/
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				WHEN IL."LOAI_CHUNG_TU" NOT IN ('2015', '2016')
				THEN 0
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_NHAP"
				ELSE IL."SO_LUONG_NHAP_THEO_DVT_CHINH"--IL.MainInwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1) --ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SL_DIEU_CHINH"
				, --Điều chỉnh--@QuantityDecimalDigits)--AdjustInQuantity

				SUM(CASE WHEN (IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND
				IL."LOAI_CHUNG_TU" IN ('2015', '2016') --@FromDate--@ToDate)
				THEN IL."SO_TIEN_NHAP"
				ELSE 0
				END)                                                  AS "GT_DIEU_CHINH"
				, --AdjustInAmount
				------------------------------------------------------
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_NHAP"
				ELSE IL."SO_LUONG_NHAP_THEO_DVT_CHINH"--IL.MainInwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1) --ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "TONG_SL_NHAP"
				, --@QuantityDecimalDigits)--TotalInQuantity
				SUM(CASE WHEN IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay --@FromDate--@ToDate
				THEN IL."SO_TIEN_NHAP"
				ELSE 0
				END)                                                  AS "TONG_GT_NHAP"
				, --TotalInAmount
				---Xuất
				-- nhyen_12/4/2017_cr77103: Xuất sản xuất
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				WHEN IL."LOAI_CHUNG_TU" <> '2023'
				THEN 0
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_XUAT"
				ELSE IL."SO_LUONG_XUAT_THEO_DVT_CHINH"--IL.MainOutwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1) --ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SL_XUAT_THANH_PHAM"
				, --@QuantityDecimalDigits)--ProductOutQuantity
				-- nhyen - 7/9/2017 (CR 94462): Giá trị sản xuất
				SUM(CASE WHEN (IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND
				IL."LOAI_CHUNG_TU" = '2023' --@FromDate--@ToDate)
				THEN IL."SO_TIEN_XUAT"
				ELSE 0
				END)                                                  AS "GT_XUAT_KHO_THANH_PHAM"
				, --ProductOutStockAmount
				-------------------------------

				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				WHEN IL."LOAI_CHUNG_TU" NOT IN ('2024', '2025')
				THEN 0
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_XUAT"
				ELSE IL."SO_LUONG_XUAT_THEO_DVT_CHINH"--IL.MainOutwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1) --ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SL_XUAT_THANH_PHAM_LR_TD"
				, --@QuantityDecimalDigits)--CollapsingOutQuantity

				SUM(CASE WHEN (IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND
				IL."LOAI_CHUNG_TU" IN ('2024', '2025') --@FromDate--@ToDate)
				THEN IL."SO_TIEN_XUAT"
				ELSE 0
				END)                                                  AS "GT_XUAT_THANH_PHAM_LR_TD"
				, --CollapsingOutAmount
				--------------------------------
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				WHEN IL."LOAI_CHUNG_TU" NOT IN ('3030', '3031')
				THEN 0
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_XUAT"
				ELSE IL."SO_LUONG_XUAT_THEO_DVT_CHINH"--IL.MainOutwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1) --ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SL_MUA_TRA_LAI"
				, --Mua trả lại--@QuantityDecimalDigits)--PUReturnQuantity

				SUM(CASE WHEN (IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND
				IL."LOAI_CHUNG_TU" IN ('3030', '3031', '3040', '3041') --@FromDate--@ToDate)
				THEN IL."SO_TIEN_XUAT"
				ELSE 0
				END)                                                  AS "GT_MUA_TRA_LAI"
				, --PUReturnAmount
				-----------------------------------
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				WHEN IL."LOAI_CHUNG_TU" <> '2020'
				THEN 0
				WHEN IL."LA_HANG_KHUYEN_MAI" <> '0'
				THEN 0
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_XUAT"
				ELSE IL."SO_LUONG_XUAT_THEO_DVT_CHINH"--IL.MainOutwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1) --ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SL_BAN_HANG"
				, -- Bán hàng--@QuantityDecimalDigits)--SAVoucherQuantity

				SUM(CASE WHEN (IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)--@FromDate--@ToDate)
				AND IL."LOAI_CHUNG_TU" = '2020'
				AND IL."LA_HANG_KHUYEN_MAI" = '0'
				THEN IL."SO_TIEN_XUAT"
				ELSE 0
				END)                                                  AS "GT_BAN_HANG"
				, --SAVoucherAmount
				----------------------------------
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				WHEN IL."LOAI_CHUNG_TU" <> '2020'
				THEN 0
				WHEN IL."LA_HANG_KHUYEN_MAI" <> '1'
				THEN 0
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_XUAT"
				ELSE IL."SO_LUONG_XUAT_THEO_DVT_CHINH"--IL.MainOutwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1) --ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SO_LUONG_KHUYEN_MAI"
				, --Khuyến mại--@QuantityDecimalDigits)--PromotionQuantity
				-- nhyen - 7/9/2017 (CR 94462): Giá trị khuyến mại
				SUM(CASE WHEN (IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay)--@FromDate--@ToDate)
				AND IL."LOAI_CHUNG_TU" = '2020'
				AND IL."LA_HANG_KHUYEN_MAI" = '1'
				THEN IL."SO_TIEN_XUAT"
				ELSE 0
				END)                                                  AS "GIA_TRI_KHUYEN_MAI"
				, --PromotionAmount
				-----------------------------------
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				WHEN IL."LOAI_CHUNG_TU" NOT IN ('2030', '2031',
				'2032')
				THEN 0
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_XUAT"
				ELSE IL."SO_LUONG_XUAT_THEO_DVT_CHINH"--IL.MainOutwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1) --ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SL_XUAT_DIEU_CHUYEN"
				, -- Điều chuyển--@QuantityDecimalDigits)--TransferOutQuantity

				SUM(CASE WHEN (IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND
				IL."LOAI_CHUNG_TU" IN ('2030', '2031', '2032') --@FromDate--@ToDate)
				THEN IL."SO_TIEN_XUAT"
				ELSE 0
				END)                                                  AS "GT_XUAT_DIEU_CHUYEN"
				, --TransferOutAmount
				-----------------------------------------
				/*
				2016	Nhập kho từ kiểm kê (Có điều chỉnh giá trị)
				2027	Xuất kho từ kiểm kê (Có điều chỉnh giá trị)
				*/
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				WHEN IL."LOAI_CHUNG_TU" NOT IN ('2027', '2026')
				THEN 0
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_XUAT"
				ELSE IL."SO_LUONG_XUAT_THEO_DVT_CHINH"--IL.MainOutwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1) --ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SL_XUAT_DIEU_CHINH"
				, -- Điều chỉnh--@QuantityDecimalDigits)--TransferOutQuantity

				SUM(CASE WHEN (IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay) AND
				IL."LOAI_CHUNG_TU" IN ('2027', '2026') --@FromDate--@ToDate)
				THEN IL."SO_TIEN_XUAT"
				ELSE 0
				END)                                                  AS "GT_XUAT_DIEU_CHINH"
				, --AdjustOutAmount
				------------------------------------------
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_XUAT"
				ELSE IL."SO_LUONG_XUAT_THEO_DVT_CHINH"--IL.MainOutwardQuantity
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1) --ISNULL(UC.ConvertRate,
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "TONG_SL_XUAT"
				, -- Tổng SL xuất--@QuantityDecimalDigits)--TotalOutQuantity
				SUM(CASE WHEN IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay --@FromDate--@ToDate
				THEN IL."SO_TIEN_XUAT"
				ELSE 0
				END)                                                  AS "TONG_GT_XUAT"
				, --Tổng giá trị xuất--TotalOutAmount

				SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				WHEN IL."LOAI_CHUNG_TU" NOT IN ('2023', '2024',
				'2025')
				THEN 0
				ELSE IL."SO_TIEN_XUAT"
				END)                                                  AS "GT_XUAT_THANH_PHAM"
				, --ProductOutAmount,
				---------------------------------
				ROUND(CAST(I."SO_LUONG_TON_TOI_THIEU" * COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
				--ISNULL(UC.ConvertRate,
				AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG)          AS "SO_LUONG_TON_TOI_THIEU"

				, UI."DON_VI_TINH"                                          AS "DON_VI_TINH_CHINH"
				, --MainUnitName
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" >= tu_ngay
				THEN 0 --@FromDate
				ELSE (IL."SO_LUONG_NHAP_THEO_DVT_CHINH"--IL.MainInwardQuantity
				- IL."SO_LUONG_XUAT_THEO_DVT_CHINH") --IL.MainOutwardQuantity
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SL_THEO_DVT_CHINH_DAU_KY"
				, --@QuantityDecimalDigits)--MainOriginalQuantity
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				ELSE IL."SO_LUONG_NHAP_THEO_DVT_CHINH" --IL.MainInwardQuantity
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "TONG_SL_NHAP_THEO_DVC"
				, -- Tổng SL nhập theo ĐVC--@QuantityDecimalDigits)--MainTotalInQuantity
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 --@FromDate
				ELSE IL."SO_LUONG_XUAT_THEO_DVT_CHINH" --IL.MainOutwardQuantity
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "TONG_SL_XUAT_THEO_DVC"
				, -- Tổng SL xuất theo ĐVC--@QuantityDecimalDigits)--MainTotalOutQuantity
				0                                                         AS "TONG_SL_THEO_DVC_CUOI_KY"

				FROM so_kho_chi_tiet IL
				INNER JOIN danh_muc_to_chuc OU ON IL."CHI_NHANH_ID" = OU."id"
				INNER JOIN TMP_KHO S ON IL."KHO_ID" = S."KHO_ID"
				--S.StockID
				INNER JOIN danh_muc_vat_tu_hang_hoa I ON IL."MA_HANG_ID" = I."id"
				LEFT JOIN danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
				ON I."id" = IIUC."VAT_TU_HANG_HOA_ID" AND IIUC."STT" = don_vi_tinh
				--@UnitType
				LEFT JOIN danh_muc_don_vi_tinh UI ON I."DVT_CHINH_ID" = UI."id"
				LEFT JOIN (SELECT
				IIUC."VAT_TU_HANG_HOA_ID"
				, IIUC."DVT_ID"
				, (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = '/'
				THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
				WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
				THEN 1
				ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
				END
				) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" --ConvertRate
				FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
				WHERE IIUC."STT" = don_vi_tinh--@UnitType
				) UC ON I."id" = UC."VAT_TU_HANG_HOA_ID"
				--UC.InventoryItemID
				LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL --UC.InventoryItemID
				AND U."id" = I."DVT_CHINH_ID"
				)
				OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL --UC.InventoryItemID
				AND UC."DVT_ID" = U."id"--UC.UnitID
				)
				WHERE (don_vi_tinh IS NULL --@UnitType
				OR don_vi_tinh = 0--@UnitType
				OR UC."VAT_TU_HANG_HOA_ID" IS NOT NULL --UC.InventoryItemID
				)
				AND IL."NGAY_HACH_TOAN" <= den_ngay
				AND (nhom_vthh_id IS NULL --@InventoryItemCategoryID
				OR I."LIST_MPC_NHOM_VTHH" LIKE '%%;'--I.InventoryItemCategoryList
				|| MA_PHAN_CAP_VTHH || '%%'--@InventoryCategoryMISACodeID
				)
				AND (OU."id" = chi_nhanh_id
				)  --@BranchID
				OR (bao_gom_du_lieu_chi_nhanh_phu_thuoc = 1--@IncludeDependentBranch
				AND OU."HACH_TOAN_SELECTION" = '1'
				)


				AND I."TINH_CHAT" IN ('0', '1') -- Không lấy mặt hàng có tính chất là dịch vụ hoặc diễn giải

				GROUP BY
				S."KHO_ID", --S.StockID
				S."MA_KHO", --S.StockCode
				S."TEN_KHO", --S.StockName
				I."id",
				I."MA",
				I."TEN",
				COALESCE(IIUC."DON_GIA_BAN_1", I."GIA_BAN_1"
				), --						ISNULL(IIUC."DON_GIA_BAN_1",--I.SalePrice1)
				COALESCE(IIUC."DON_GIA_BAN_2", I."GIA_BAN_2"
				), --						ISNULL(IIUC."DON_GIA_BAN_2",--I.SalePrice2)
				COALESCE(IIUC."DON_GIA_BAN_3", I."GIA_BAN_3"
				), --						ISNULL(IIUC."DON_GIA_BAN_3",--I.SalePrice3)
				COALESCE(IIUC."DON_GIA_CO_DINH", I."GIA_CO_DINH"
				), --						ISNULL(IIUC."DON_GIA_CO_DINH",--I.FixedSalePrice)
				U."DON_VI_TINH",
				UI."DON_VI_TINH",
				I."SO_LUONG_TON_TOI_THIEU",
				COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1
				)
				;

				DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
				;

				CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
				AS
				SELECT
				ROW_NUMBER()
				OVER (
				ORDER BY "TEN_KHO", "MA_KHO", "MA" ) AS RowNum
				, --StockName,--StockCode,--InventoryItemCode
				"KHO_ID"
				, --StockID
				"MA_KHO"
				, --StockCode
				"TEN_KHO"
				, --StockName
				"MA_HANG_ID"
				, --InventoryItemID
				"MA"
				, --InventoryItemCode
				"TEN"
				, --InventoryItemName
				"DON_VI_TINH"
				, --UnitName
				"GIA_BAN_1"
				, --				SalePrice1
				"GIA_BAN_2"
				, --				SalePrice2
				"GIA_BAN_3"
				, --				SalePrice3
				"GIA_CO_DINH"
				, --				FixedSalePrice
				"SO_LUONG_DAU_KY"

				, "GIA_TRI_DAU_KY"


				, "SO_LUONG_NHAP_THANH_PHAM"
				, --ProductInQuantity
				"GIA_TRI_NHAP_THANH_PHAM"
				, -- nhyen - 7/9/2017 (CR 94462): Giá trị nhập thành phẩm--ProductInAmount
				"SL_NHAP_THANH_PHAM_LR_TD"
				, -- nhyen_12/4/2017_cr77103: số lượng nhập TP lắp ráp tháo rỡ--ProductCollapsingInQuantity
				"GT_NHAP_THANH_PHAM_LR_TD"
				, -- nhyen - 7/9/2017 (CR 94462): Giá trị lắp ráp tháo rỡ--ProductCollapsingInAmount
				"SL_NVL_NHAP_LAI"
				, --MaterialInQuantity
				"GT_NVL_NHAP_LAI"
				, -- nhyen - 7/9/2017 (CR 94462): Giá trị NVL nhập lại--MaterialInAmount
				"SO_LUONG_MUA_HANG"
				, --PUVoucherQuantity
				"GIA_TRI_MUA_HANG"
				, -- nhyen - 7/9/2017 (CR 94462): Giá trị mua hàng--PUVoucherAmount
				"SL_BAN_KM_TRA_LAI"
				, --SAReturnPromotionQuantity
				"GT_BAN_KM_TRA_LAI"
				, -- nhyen - 7/9/2017 (CR 94462): Giá trị bán trả lại KM--SAReturnPromotionAmount
				"SL_BAN_TRA_LAI"
				, --SAReturnQuantity
				"GT_BAN_TRA_LAI"
				, -- nhyen - 7/9/2017 (CR 94462): Giá trị bán trả lại khác--SAReturnAmount
				"SL_DIEU_CHUYEN"
				, --TransferInQuantity
				"GT_DIEU_CHUYEN"
				, -- nhyen - 7/9/2017 (CR 94462): Giá trị điều chuyển--TransferInAmount
				"SL_DIEU_CHINH"
				, --AdjustInQuantity
				"GT_DIEU_CHINH"
				, "TONG_SL_NHAP"
				- "SO_LUONG_NHAP_THANH_PHAM" - "SL_NHAP_THANH_PHAM_LR_TD" - "SL_NVL_NHAP_LAI"
				- "SO_LUONG_MUA_HANG" - "SL_BAN_KM_TRA_LAI" - "SL_BAN_TRA_LAI" - "SL_DIEU_CHUYEN" -
				"SL_DIEU_CHINH"                          AS "SL_NHAP_KHAC"


				, "TONG_GT_NHAP"
				- "GIA_TRI_NHAP_THANH_PHAM" - "GT_NHAP_THANH_PHAM_LR_TD" - "GT_NVL_NHAP_LAI"
				- "GIA_TRI_MUA_HANG" - "GT_BAN_KM_TRA_LAI" - "GT_BAN_TRA_LAI" - "GT_DIEU_CHUYEN" -
				"GT_DIEU_CHINH"                          AS "GT_NHAP_KHAC"


				, --SAReturnPromotionAmount--SAReturnAmount---TransferInAmount---AdjustInAmount--OtherInAmount
				"TONG_SL_NHAP"
				, --TotalInQuantity
				"TONG_GT_NHAP"
				, --TotalInAmount
				-- Xuất
				"SL_XUAT_THANH_PHAM"
				, --ProductOutQuantity
				"GT_XUAT_KHO_THANH_PHAM"
				, "SL_XUAT_THANH_PHAM_LR_TD"
				, --
				"GT_XUAT_THANH_PHAM_LR_TD"
				, -- nhyen -
				"SL_MUA_TRA_LAI"
				, --PUReturnQuantity
				"GT_MUA_TRA_LAI"
				, --
				"SL_BAN_HANG"
				, --SAVoucherQuantity
				"GT_BAN_HANG"
				, --
				"SO_LUONG_KHUYEN_MAI"
				, --PromotionQuantity
				"GIA_TRI_KHUYEN_MAI"
				, --
				"SL_XUAT_DIEU_CHUYEN"
				, "GT_XUAT_DIEU_CHUYEN"
				, "SL_XUAT_DIEU_CHINH"
				, "GT_XUAT_DIEU_CHINH"

				, "TONG_SL_XUAT" - "SL_XUAT_THANH_PHAM" - "SL_XUAT_THANH_PHAM_LR_TD" - "SL_MUA_TRA_LAI"
				- "SL_BAN_HANG" - "SO_LUONG_KHUYEN_MAI" - "SL_XUAT_DIEU_CHUYEN" -
				"SL_XUAT_DIEU_CHINH"                     AS "SL_XUAT_KHAC"

				, "TONG_GT_XUAT"
				- "GT_XUAT_KHO_THANH_PHAM" - "GT_XUAT_THANH_PHAM_LR_TD" - "GT_MUA_TRA_LAI"
				- "GT_BAN_HANG" - "GIA_TRI_KHUYEN_MAI" - "GT_BAN_TRA_LAI" - "GT_XUAT_DIEU_CHUYEN" -
				"GT_XUAT_DIEU_CHINH"                     AS "GT_XUAT_KHAC"

				, "TONG_SL_XUAT"
				, --TotalOutQuantity
				"TONG_GT_XUAT"
				, --TotalOutAmount
				"GT_XUAT_THANH_PHAM"
				, /*Giá trị xuất sản xuất*/--				ProductOutAmount,/*Giá
				("SO_LUONG_DAU_KY" + "TONG_SL_NHAP"
				- "TONG_SL_XUAT")                          AS "SO_LUONG_CUOI_KY"

				, --OriginalQuantity--TotalInQuantity--TotalOutQuantity--ExitsQuantity

				"GIA_TRI_DAU_KY" + "TONG_GT_NHAP" -
				"TONG_GT_XUAT"                           AS "GIA_TRI_CUOI_KY"
				, --OriginalAmount--TotalInAmount--TotalOutAmount--ExitsAmount
				"SO_LUONG_TON_TOI_THIEU"
				, --MinimumStock

				"DON_VI_TINH_CHINH"
				, -- ĐVT chính--MainUnitName
				"SL_THEO_DVT_CHINH_DAU_KY"
				, --SL đầu kỳ theo ĐVC--MainOriginalQuantity
				"TONG_SL_NHAP_THEO_DVC"
				, -- SL nhập thành phẩm theo ĐVC--MainTotalInQuantity
				"TONG_SL_XUAT_THEO_DVC"
				, ("SL_THEO_DVT_CHINH_DAU_KY" + "TONG_SL_NHAP_THEO_DVC" -
				"TONG_SL_XUAT_THEO_DVC")                AS "TONG_SL_THEO_DVC_CUOI_KY"


				FROM TMP_KET_QUA
				WHERE "SO_LUONG_DAU_KY" <> 0--OriginalQuantity
				OR "GIA_TRI_DAU_KY" <> 0--OriginalAmount
				OR "SO_LUONG_NHAP_THANH_PHAM" <> 0 OR "GIA_TRI_NHAP_THANH_PHAM" <> 0--ProductInQuantity--ProductInAmount
				OR "SL_NVL_NHAP_LAI" <> 0 OR "GT_NVL_NHAP_LAI" <> 0--MaterialInQuantity--MaterialInAmount
				OR "SO_LUONG_MUA_HANG" <> 0 OR "GIA_TRI_MUA_HANG" <> 0--PUVoucherQuantity--PUVoucherAmount
				OR "SL_BAN_KM_TRA_LAI" <> 0 OR "GT_BAN_KM_TRA_LAI" <> 0--SAReturnPromotionQuantity--SAReturnPromotionAmount
				OR "SL_BAN_TRA_LAI" <> 0 OR "GT_BAN_TRA_LAI" <> 0--SAReturnQuantity--SAReturnAmount
				OR "SL_DIEU_CHUYEN" <> 0 OR "GT_DIEU_CHUYEN" <> 0--TransferInQuantity--TransferInAmount
				OR "SL_DIEU_CHINH" <> 0 OR "GT_DIEU_CHINH" <> 0--AdjustInQuantity--AdjustInAmount
				OR "TONG_SL_NHAP" <> 0--TotalInQuantity
				OR "TONG_GT_NHAP" <> 0--TotalInAmount
				OR "SL_XUAT_THANH_PHAM" <> 0 OR "GT_XUAT_KHO_THANH_PHAM" <> 0--ProductOutQuantity--ProductOutStockAmount
				OR "SL_MUA_TRA_LAI" <> 0 OR "GT_MUA_TRA_LAI" <> 0--PUReturnQuantity--PUReturnAmount
				OR "SL_BAN_HANG" <> 0 OR "GT_BAN_HANG" <> 0--SAVoucherQuantity--SAVoucherAmount
				OR "SO_LUONG_KHUYEN_MAI" <> 0 OR "GIA_TRI_KHUYEN_MAI" <> 0--PromotionQuantity--PromotionAmount
				OR "SL_XUAT_DIEU_CHUYEN" <> 0 OR "GT_XUAT_DIEU_CHUYEN" <> 0--TransferOutQuantity--TransferOutAmount
				OR "SL_XUAT_DIEU_CHINH" <> 0 OR "GT_XUAT_DIEU_CHINH" <> 0--AdjustOutQuantity--AdjustOutAmount
				OR "TONG_SL_XUAT" <> 0--TotalOutQuantity
				OR "TONG_GT_XUAT" <> 0--TotalOutAmount
				OR "SL_THEO_DVT_CHINH_DAU_KY" <> 0--MainOriginalQuantity
				OR "TONG_SL_NHAP" <> 0--TotalInQuantity
				OR "TONG_SL_XUAT" <> 0--TotalOutQuantity
				OR "TONG_SL_THEO_DVC_CUOI_KY" <> 0--MainTotalExitsQuantity
				;


				END $$
				;

				SELECT
							"TEN_KHO" AS "TEN_KHO",
							"MA" AS "MA_HANG",
							"TEN" AS "TEN_HANG",
							"DON_VI_TINH" AS "DVT",
							"SO_LUONG_DAU_KY" AS "SO_LUONG_DAU_KY",
							"GIA_TRI_DAU_KY" AS "GIA_TRI_DAU_KY",
							"TONG_SL_NHAP" AS "SO_LUONG_NHAP_KHO",
							"TONG_GT_NHAP" AS "GIA_TRI_NHAP_KHO",
							"TONG_SL_XUAT" AS "SO_LUONG_XUAT_KHO",
							"TONG_GT_XUAT" AS "GIA_TRI_XUAT",
							"SO_LUONG_CUOI_KY" AS "SO_LUONG_CUOI_KY",
							"GIA_TRI_CUOI_KY" AS "GIA_TRI_CUOI_KY"


				FROM TMP_KET_QUA_CUOI_CUNG --WHERE  "MA" ='AO_SM_NAM' AND "MA_KHO" = 'KHH'
				;
				"""
		return self.execute(query,params_sql)

	def _lay_bao_cao_tong_hop_tren_nhieu_kho(self, params_sql):      
		record = []
		query = """
				DO LANGUAGE plpgsql $$
				DECLARE
				tu_ngay                             DATE := %(TU_NGAY)s;

				--Từ

				den_ngay                            DATE := %(DEN_NGAY)s;

				--đến

				bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

				--bao gồm số liệu chi nhánh phụ thuộc

				chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

				--chi nhánh


				don_vi_tinh                         INTEGER := %(DON_VI_TINH)s;
				--đơn vị tính

				hien_thi_tuy_chon                   INTEGER :=  %(HIEN_THI)s;
				-- hiển thị

				nhom_vthh_id                        INTEGER :=  %(NHOM_VTHH_ID)s;
				--nhóm VTHH


				--KHO_IDS                             INTEGER := -1;
				-- Kho


				rec                                 RECORD;

				CHE_DO_KE_TOAN                      INTEGER;

				PHAN_THAP_PHAN_SO_LUONG             INTEGER ;

				LOAI_TIEN_CHINH                     INTEGER;


				MA_PHAN_CAP_VTHH                    VARCHAR(100);

				DEM_SO_KHO                          INTEGER;


				BEGIN


				SELECT value
				INTO CHE_DO_KE_TOAN
				FROM ir_config_parameter
				WHERE key = 'he_thong.CHE_DO_KE_TOAN'
				FETCH FIRST 1 ROW ONLY
				;

				SELECT value
				INTO LOAI_TIEN_CHINH
				FROM ir_config_parameter
				WHERE key = 'he_thong.LOAI_TIEN_CHINH'
				FETCH FIRST 1 ROW ONLY
				;

				SELECT value
				INTO PHAN_THAP_PHAN_SO_LUONG
				FROM ir_config_parameter
				WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_LUONG'
				FETCH FIRST 1 ROW ONLY
				;

				SELECT "MA_PHAN_CAP"
				INTO MA_PHAN_CAP_VTHH
				FROM danh_muc_nhom_vat_tu_hang_hoa_dich_vu

				WHERE id = nhom_vthh_id
				;

				DROP TABLE IF EXISTS BANG_CHI_TIET_DON_GIA_MUA_VTHH
				;

				CREATE TEMP TABLE BANG_CHI_TIET_DON_GIA_MUA_VTHH
				AS
				SELECT DISTINCT
				"VAT_TU_HANG_HOA_ID"
				, "DON_VI_TINH_ID"
				, "currency_id"
				, CAST(0 AS DECIMAL(18, 4)) AS "DON_GIA" --SMEFIVE-9126

				FROM danh_muc_vthh_don_gia_mua_gan_nhat
				;

				UPDATE BANG_CHI_TIET_DON_GIA_MUA_VTHH
				SET "DON_GIA" = COALESCE(R."DON_GIA", 0)
				FROM BANG_CHI_TIET_DON_GIA_MUA_VTHH T
				JOIN danh_muc_vthh_don_gia_mua_gan_nhat R ON T."VAT_TU_HANG_HOA_ID" = R."VAT_TU_HANG_HOA_ID"
				AND T."DON_VI_TINH_ID" = R."DON_VI_TINH_ID"
				AND T."currency_id" = R."currency_id"
				;


				DROP TABLE IF EXISTS TMP_KHO
				;

				CREATE TEMP TABLE TMP_KHO
				AS
				SELECT
				"id" AS "KHO_ID"
				, "MA_KHO"
				, "TEN_KHO"
				FROM danh_muc_kho S

				WHERE (id = any(%(KHO_IDS)s))----Kho

				;

				DEM_SO_KHO = (SELECT COUNT(*)
				FROM TMP_KHO)
				;


				DROP TABLE IF EXISTS TMP_DON_VI_CHUYEN_DOI
				;

				CREATE TEMP TABLE TMP_DON_VI_CHUYEN_DOI
				AS
				SELECT
				IIUC."VAT_TU_HANG_HOA_ID"
				, "DVT_ID"
				, (CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = '/'
				THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
				WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
				THEN 1
				ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
				END) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
				FROM danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
				WHERE IIUC."STT" = don_vi_tinh
				;


				DROP TABLE IF EXISTS TMP_KET_QUA
				;

				CREATE TEMP TABLE TMP_KET_QUA
				AS
				SELECT
				I."id"
				, -- Số lượng đầu kỳ
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" >= tu_ngay
				THEN 0
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_NHAP"
				- IL."SO_LUONG_XUAT"
				ELSE (IL."SO_LUONG_NHAP_THEO_DVT_CHINH"
				- IL."SO_LUONG_XUAT_THEO_DVT_CHINH")
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SO_LUONG_DAU_KY"
				, -- Giá trị đầu lỳ
				SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN IL."SO_TIEN_NHAP" - IL."SO_TIEN_XUAT"
				ELSE 0
				END)                                                  AS "GIA_TRI_DAU_KY"
				, -- Số lượng nhập trong kỳ
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 -- OR IL."LOAI_CHUNG_TU" NOT IN ( 2010, 2011, 2012 )
				ELSE CASE WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_NHAP"
				ELSE IL."SO_LUONG_NHAP_THEO_DVT_CHINH"
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
				1)
				END
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SO_LUONG_NHAP_TRONG_KY"
				, -- Giá trị nhập trong kỳ
				SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0
				ELSE IL."SO_TIEN_NHAP"
				END)                                                  AS "GIA_TRI_NHAP_TRONG_KY"
				, ---Số lượng xuất trong kỳ
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 -- WHEN IL."LOAI_CHUNG_TU" NOT IN ( 2023, 2024, 2025 ) THEN 0
				ELSE CASE WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_XUAT"
				ELSE IL."SO_LUONG_XUAT_THEO_DVT_CHINH"
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
				1)
				END
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SO_LUONG_XUAT_TRONG_KY"
				, --Giá trị xuất trong kỳ
				SUM(CASE WHEN IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
				THEN IL."SO_TIEN_XUAT"
				ELSE 0
				END)                                                  AS "GIA_TRI_XUAT_TRONG_KY"
				FROM so_kho_chi_tiet IL
				INNER JOIN danh_muc_to_chuc OU ON IL."CHI_NHANH_ID" = OU."id"
				INNER JOIN TMP_KHO S ON IL."KHO_ID" = S."KHO_ID"
				INNER JOIN danh_muc_vat_tu_hang_hoa I ON IL."MA_HANG_ID" = I."id"
				LEFT JOIN TMP_DON_VI_CHUYEN_DOI UC ON I."id" = UC."VAT_TU_HANG_HOA_ID"
				LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
				AND U."id" = I."DVT_CHINH_ID"
				)
				OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
				AND UC."DVT_ID" = U."id"
				)
				WHERE (don_vi_tinh IS NULL
				OR don_vi_tinh = 0
				OR UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
				)
				AND IL."NGAY_HACH_TOAN" <= den_ngay
				AND (nhom_vthh_id IS NULL
				OR I."LIST_MPC_NHOM_VTHH" LIKE '%%;'
				|| MA_PHAN_CAP_VTHH || '%%'
				)
				AND (OU."id" = chi_nhanh_id
				OR (bao_gom_du_lieu_chi_nhanh_phu_thuoc = 1
				AND OU."HACH_TOAN_SELECTION" = '1'
				)
				)
				AND I."TINH_CHAT" IN ('0', '1') -- Là vật tư hàng hóa hoặc thành phẩm

				AND (DEM_SO_KHO = 1
				OR (DEM_SO_KHO <> 1  -- Không lấy lên xuất chuyển kho nội bộ
				AND IL."LOAI_CHUNG_TU" NOT IN ('2030', '2031', '2032')
				)
				)
				GROUP BY
				I."id"
				;

				-- Nếu số lượng kho chọn khác 1 thì xem xét trường hợp chuyển kho
				IF DEM_SO_KHO <> 1
				THEN
				INSERT INTO TMP_KET_QUA

				SELECT
				I."id"
				, -- Số lượng đầu kỳ
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" >= tu_ngay
				THEN 0
				WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_NHAP"
				- IL."SO_LUONG_XUAT"
				ELSE (IL."SO_LUONG_NHAP_THEO_DVT_CHINH"
				- IL."SO_LUONG_XUAT_THEO_DVT_CHINH")
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SO_LUONG_DAU_KY"
				, -- Giá trị đầu lỳ
				SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN IL."SO_TIEN_NHAP"
				- IL."SO_TIEN_XUAT"
				ELSE 0
				END)                                                  AS "GIA_TRI_DAU_KY"
				, -- Số lượng nhập trong kỳ
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0
				ELSE CASE WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_NHAP"
				ELSE IL."SO_LUONG_NHAP_THEO_DVT_CHINH"
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
				1)
				END
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SO_LUONG_NHAP_TRONG_KY"
				, -- Giá trị nhập trong kỳ
				SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0
				ELSE IL."SO_TIEN_NHAP"
				END)                                                  AS "GIA_TRI_NHAP_TRONG_KY"
				, ---Số lượng xuất trong kỳ
				ROUND(CAST(SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN 0 -- WHEN IL."LOAI_CHUNG_TU" NOT IN ( 2023, 2024, 2025 ) THEN 0
				ELSE CASE WHEN U."id" IS NOT NULL
				AND IL."DVT_ID" = U."id"
				THEN IL."SO_LUONG_XUAT"
				ELSE IL."SO_LUONG_XUAT_THEO_DVT_CHINH"
				* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH",
				1)
				END
				END) AS NUMERIC), PHAN_THAP_PHAN_SO_LUONG) AS "SO_LUONG_XUAT_TRONG_KY"
				, --Giá trị xuất trong kỳ
				SUM(CASE WHEN IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
				THEN IL."SO_TIEN_XUAT"
				ELSE 0
				END)                                                  AS "GIA_TRI_XUAT_TRONG_KY"
				FROM so_kho_chi_tiet IL
				INNER JOIN danh_muc_to_chuc OU ON IL."CHI_NHANH_ID" = OU."id"
				INNER JOIN TMP_KHO S ON IL."KHO_ID" = S."KHO_ID"
				INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet TD ON IL."CHI_TIET_ID" = TD."id"
				LEFT JOIN TMP_KHO S1 ON TD."XUAT_TAI_KHO_ID" = S1."KHO_ID"
				LEFT JOIN TMP_KHO S2 ON TD."NHAP_TAI_KHO_ID" = S2."KHO_ID"
				INNER JOIN danh_muc_vat_tu_hang_hoa I ON IL."MA_HANG_ID" = I."id"
				LEFT JOIN TMP_DON_VI_CHUYEN_DOI UC ON I."id" = UC."VAT_TU_HANG_HOA_ID"
				LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
				AND U."id" = I."DVT_CHINH_ID"
				)
				OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
				AND UC."DVT_ID" = U."id"
				)
				WHERE (don_vi_tinh IS NULL
				OR don_vi_tinh = 0
				OR UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
				)
				AND IL."NGAY_HACH_TOAN" <= den_ngay
				AND (nhom_vthh_id IS NULL
				OR I."LIST_MPC_NHOM_VTHH" LIKE '%%;'
				|| MA_PHAN_CAP_VTHH || '%%'
				)
				AND (OU."id" = chi_nhanh_id
				OR (bao_gom_du_lieu_chi_nhanh_phu_thuoc = 1
				AND OU."HACH_TOAN_SELECTION" = '1'
				)
				)
				AND I."TINH_CHAT" IN ('0', '1'
				) -- Là vật tư hàng hóa hoặc thành phẩm

				AND IL."LOAI_CHUNG_TU" IN ('2030', '2031', '2032'
				)
				AND (S1."KHO_ID" IS NULL
				OR S2."KHO_ID" IS NULL
				)
				GROUP BY I."id"
				;

				END IF
				;

				DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
				;

				-- 1: Tất cả: Lên tất cả các vật tư, kể cả VTHH không có nhập, xuất, tồn
				IF hien_thi_tuy_chon = 1
				THEN
				-- Lấy lên từ danh mục vật tư hàng hóa, nếu VTHH nào không có số liệu thì để bằng 0
				CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
				AS
				SELECT
				ROW_NUMBER()
				OVER (
				ORDER BY I."MA" )                                                        AS RowNum
				, I."id"
				, I."MA"
				, I."TEN"
				, U."DON_VI_TINH"
				, SUM("SO_LUONG_DAU_KY")                                                       AS "SO_LUONG_DAU_KY"
				, SUM("GIA_TRI_DAU_KY")                                                        AS "GIA_TRI_DAU_KY"
				, SUM(
				"SO_LUONG_NHAP_TRONG_KY")                                                AS "SO_LUONG_NHAP_TRONG_KY"
				, SUM(
				"GIA_TRI_NHAP_TRONG_KY")                                                 AS "GIA_TRI_NHAP_TRONG_KY"
				, SUM(
				"SO_LUONG_XUAT_TRONG_KY")                                                AS "SO_LUONG_XUAT_TRONG_KY"
				, SUM(
				"GIA_TRI_XUAT_TRONG_KY")                                                 AS "GIA_TRI_XUAT_TRONG_KY"
				, SUM("SO_LUONG_DAU_KY" + "SO_LUONG_NHAP_TRONG_KY" - "SO_LUONG_XUAT_TRONG_KY") AS "SO_LUONG_TON"
				, SUM("GIA_TRI_DAU_KY" + "GIA_TRI_NHAP_TRONG_KY" - "GIA_TRI_XUAT_TRONG_KY")    AS "GIA_TRI_TON"

				FROM danh_muc_vat_tu_hang_hoa I
				LEFT JOIN TMP_KET_QUA R ON I."id" = R."id"
				LEFT JOIN TMP_DON_VI_CHUYEN_DOI UC ON I."id" = UC."VAT_TU_HANG_HOA_ID"
				LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
				AND U."id" = I."DVT_CHINH_ID"
				)
				OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
				AND UC."DVT_ID" = U."id"
				)
				LEFT JOIN BANG_CHI_TIET_DON_GIA_MUA_VTHH P ON (don_vi_tinh <> 0
				AND p."VAT_TU_HANG_HOA_ID" =
				uc."VAT_TU_HANG_HOA_ID"
				AND p."DON_VI_TINH_ID" = UC."DVT_ID"
				OR don_vi_tinh = 0
				AND p.
				"VAT_TU_HANG_HOA_ID"
				= I."id"
				AND p."DON_VI_TINH_ID"
				= I."DVT_CHINH_ID"
				)
				AND P."currency_id" = LOAI_TIEN_CHINH
				WHERE I."TINH_CHAT" IN ('0', '1') -- Là vật tư hàng hóa hoặc thành phẩm
				AND (nhom_vthh_id IS NULL
				OR I."LIST_MPC_NHOM_VTHH" LIKE '%%;'
				|| MA_PHAN_CAP_VTHH || '%%'
				)
				AND (don_vi_tinh IS NULL
				OR don_vi_tinh = 0
				OR UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
				)
				GROUP BY
				I."id",
				I."MA",
				I."TEN",
				U."DON_VI_TINH"


				;
				END IF
				;


				--  2: Có nhập xuất tồn: Lên các vật tư có nhập hoặc xuất hoặc tồn
				IF hien_thi_tuy_chon = 2
				THEN

				CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
				AS
				SELECT
				ROW_NUMBER()
				OVER (
				ORDER BY i."MA" )                                                        AS RowNum
				, i."id"
				, i."MA"
				, i."TEN"
				, u."DON_VI_TINH"
				, SUM("SO_LUONG_DAU_KY")                                                       AS "SO_LUONG_DAU_KY"
				, SUM("GIA_TRI_DAU_KY")                                                        AS "GIA_TRI_DAU_KY"
				, SUM(
				"SO_LUONG_NHAP_TRONG_KY")                                                AS "SO_LUONG_NHAP_TRONG_KY"
				, SUM(
				"GIA_TRI_NHAP_TRONG_KY")                                                 AS "GIA_TRI_NHAP_TRONG_KY"
				, SUM(
				"SO_LUONG_XUAT_TRONG_KY")                                                AS "SO_LUONG_XUAT_TRONG_KY"
				, SUM(
				"GIA_TRI_XUAT_TRONG_KY")                                                 AS "GIA_TRI_XUAT_TRONG_KY"
				, SUM("SO_LUONG_DAU_KY" + "SO_LUONG_NHAP_TRONG_KY" - "SO_LUONG_XUAT_TRONG_KY") AS "SO_LUONG_TON"
				, SUM("GIA_TRI_DAU_KY" + "GIA_TRI_NHAP_TRONG_KY" - "GIA_TRI_XUAT_TRONG_KY")    AS "GIA_TRI_TON"


				FROM danh_muc_vat_tu_hang_hoa I
				INNER JOIN TMP_KET_QUA R ON I."id" = R."id"
				LEFT JOIN TMP_DON_VI_CHUYEN_DOI UC ON I."id" = UC."VAT_TU_HANG_HOA_ID"
				LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
				AND U."id" = I."DVT_CHINH_ID"
				)
				OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
				AND UC."DVT_ID" = U."id"
				)
				LEFT JOIN BANG_CHI_TIET_DON_GIA_MUA_VTHH P ON (don_vi_tinh <> 0
				AND p."VAT_TU_HANG_HOA_ID" = uc."VAT_TU_HANG_HOA_ID"
				AND p."DON_VI_TINH_ID" = UC."DVT_ID"
				OR don_vi_tinh = 0
				AND p."VAT_TU_HANG_HOA_ID" = I."id"
				AND p."DON_VI_TINH_ID" = I."DVT_CHINH_ID"
				)
				AND P.currency_id = LOAI_TIEN_CHINH
				WHERE I."TINH_CHAT" IN ('0', '1') -- Là vật tư hàng hóa hoặc thành phẩm
				GROUP BY I."id",
				I."MA",
				I."TEN",
				U."DON_VI_TINH"

				HAVING SUM("SO_LUONG_NHAP_TRONG_KY") <> 0
				OR SUM("GIA_TRI_NHAP_TRONG_KY") <> 0
				OR SUM("SO_LUONG_XUAT_TRONG_KY") <> 0
				OR SUM("GIA_TRI_XUAT_TRONG_KY") <> 0
				OR SUM("SO_LUONG_DAU_KY" + "SO_LUONG_NHAP_TRONG_KY" - "SO_LUONG_XUAT_TRONG_KY") <> 0
				OR SUM("GIA_TRI_DAU_KY" + "GIA_TRI_NHAP_TRONG_KY" - "GIA_TRI_XUAT_TRONG_KY") <> 0
				;
				END IF
				;

				IF hien_thi_tuy_chon = 3
				THEN

				CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
				AS
				-- 3: Phát sinh nhập xuất: Chỉ lên các vật tư có nhập hoặc xuất
				SELECT
				ROW_NUMBER()
				OVER (
				ORDER BY i."MA" )                                                        AS RowNum
				, i."id"
				, i."MA"
				, i."TEN"
				, U."DON_VI_TINH"
				, SUM("SO_LUONG_DAU_KY")                                                       AS "SO_LUONG_DAU_KY"
				, SUM("GIA_TRI_DAU_KY")                                                        AS "GIA_TRI_DAU_KY"
				, SUM(
				"SO_LUONG_NHAP_TRONG_KY")                                                AS "SO_LUONG_NHAP_TRONG_KY"
				, SUM(
				"GIA_TRI_NHAP_TRONG_KY")                                                 AS "GIA_TRI_NHAP_TRONG_KY"
				, SUM(
				"SO_LUONG_XUAT_TRONG_KY")                                                AS "SO_LUONG_XUAT_TRONG_KY"
				, SUM(
				"GIA_TRI_XUAT_TRONG_KY")                                                 AS "GIA_TRI_XUAT_TRONG_KY"
				, SUM("SO_LUONG_DAU_KY" + "SO_LUONG_NHAP_TRONG_KY" - "SO_LUONG_XUAT_TRONG_KY") AS "SO_LUONG_TON"
				, SUM("GIA_TRI_DAU_KY" + "GIA_TRI_NHAP_TRONG_KY" - "GIA_TRI_XUAT_TRONG_KY")    AS "GIA_TRI_TON"

				FROM danh_muc_vat_tu_hang_hoa I
				INNER JOIN TMP_KET_QUA R ON I."id" = R."id"
				LEFT JOIN TMP_DON_VI_CHUYEN_DOI UC ON I."id" = UC."VAT_TU_HANG_HOA_ID"
				LEFT JOIN danh_muc_don_vi_tinh U ON (UC."VAT_TU_HANG_HOA_ID" IS NULL
				AND U."id" = I."DVT_CHINH_ID"
				)
				OR (UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
				AND UC."DVT_ID" = U."id"
				)
				LEFT JOIN BANG_CHI_TIET_DON_GIA_MUA_VTHH P ON (don_vi_tinh <> 0
				AND p."VAT_TU_HANG_HOA_ID" =
				uc."VAT_TU_HANG_HOA_ID"
				AND p."DON_VI_TINH_ID" = UC."DVT_ID"
				OR don_vi_tinh = 0
				AND p."VAT_TU_HANG_HOA_ID" = I."id"
				AND p."DON_VI_TINH_ID" = I."DVT_CHINH_ID"
				)
				AND P.currency_id = LOAI_TIEN_CHINH
				WHERE I."TINH_CHAT" IN ('0', '1') -- Là vật tư hàng hóa hoặc thành phẩm
				GROUP BY I."id",
				I."MA",
				I."TEN",
				U."DON_VI_TINH"

				HAVING SUM("SO_LUONG_NHAP_TRONG_KY") <> 0
				OR SUM("GIA_TRI_NHAP_TRONG_KY") <> 0
				OR SUM("SO_LUONG_XUAT_TRONG_KY") <> 0
				OR SUM("GIA_TRI_XUAT_TRONG_KY") <> 0
				;
				END IF
				;

				END $$
				;

				SELECT 
	  
							"MA" AS "MA_HANG",
							"TEN" AS "TEN_HANG",
							"DON_VI_TINH" AS "DVT",
							"SO_LUONG_DAU_KY" AS "SO_LUONG_DAU_KY",
							"GIA_TRI_DAU_KY" AS "GIA_TRI_DAU_KY",
							"SO_LUONG_NHAP_TRONG_KY" AS "SO_LUONG_NHAP_KHO",
							"GIA_TRI_NHAP_TRONG_KY" AS "GIA_TRI_NHAP_KHO",
							"SO_LUONG_XUAT_TRONG_KY" AS "SO_LUONG_XUAT_KHO",
							"GIA_TRI_XUAT_TRONG_KY" AS "GIA_TRI_XUAT",
							"SO_LUONG_TON" AS "SO_LUONG_CUOI_KY",
							"GIA_TRI_TON" AS "GIA_TRI_CUOI_KY"

				FROM TMP_KET_QUA_CUOI_CUNG
				;
				""" 
		return self.execute(query,params_sql)

	def _lay_bao_cao_theo_han_su_dung(self, params_sql):      
		record = []
		query ="""
		
		DO LANGUAGE plpgsql $$
		DECLARE
		den_ngay                            DATE := %(DEN_NGAY)s;
		--đến ngày
		bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

		--bao gồm số liệu chi nhánh phụ thuộc
		chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

		--chi nhánh

		don_vi_tinh                         INTEGER := %(DON_VI_TINH)s;
		--đơn vị tính
		nhom_vthh_id                        INTEGER := %(NHOM_VTHH_ID)s;
		--nhóm VTHH

		KHO_IDS                             INTEGER := -1;
		-- Kho
		rec                                 RECORD;
		CHE_DO_KE_TOAN                      INTEGER;

		MA_PHAN_CAP_VTHH                    VARCHAR(100);


		BEGIN


		SELECT value
		INTO CHE_DO_KE_TOAN
		FROM ir_config_parameter
		WHERE key = 'he_thong.CHE_DO_KE_TOAN'
		FETCH FIRST 1 ROW ONLY
		;


		SELECT "MA_PHAN_CAP" INTO MA_PHAN_CAP_VTHH
		FROM danh_muc_nhom_vat_tu_hang_hoa_dich_vu

		WHERE id = nhom_vthh_id
		;

		DROP TABLE IF EXISTS TMP_KHO
		;

		CREATE TEMP TABLE TMP_KHO
		AS
		SELECT
		"id" AS "KHO_ID"
		, "MA_KHO"
		, "TEN_KHO"
		FROM danh_muc_kho S

		WHERE (id = any(%(KHO_IDS)s))----Kho

		;


		DROP TABLE IF EXISTS TMP_KET_QUA
		;

		CREATE TEMP TABLE TMP_KET_QUA
		AS
		SELECT
		S."KHO_ID" ,
		S."MA_KHO" ,
		S."TEN_KHO" ,
		I."id" ,
		I."MA" ,
		I."TEN" ,

		IL."SO_LO" ,
		IL."NGAY_HET_HAN" ,
		U."DON_VI_TINH" ,
		SUM(CASE WHEN IL."NGAY_HACH_TOAN" > den_ngay THEN 0
		WHEN U."id" IS NOT NULL
		AND IL."DVT_ID" = U."id" --Nếu đơn vị tính trên chứng từ = đơn vị tính được chọn thì lấy trên chứng từ
		THEN IL."SO_LUONG_NHAP"
		- IL."SO_LUONG_XUAT"
		ELSE ( IL."SO_LUONG_NHAP_THEO_DVT_CHINH" -- Nếu đơn vị tính trên chứng từ <> đơn vị tính được chọn thì lấy số lượng ĐVC * Tỷ lệ chuyển đổi trên danh mục
		- IL."SO_LUONG_XUAT_THEO_DVT_CHINH" )
		* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
		END) AS "SO_LUONG_TON" ,
		CASE WHEN  DATE_PART( 'day', CAST(IL."NGAY_HET_HAN" AS TIMESTAMP)-CAST(den_ngay AS TIMESTAMP)    ) >= 0
		AND  DATE_PART( 'day', CAST(IL."NGAY_HET_HAN" AS TIMESTAMP)-CAST(den_ngay AS TIMESTAMP)    ) <= 30
		THEN N'Sắp hết hạn 1 tháng'
		WHEN  DATE_PART( 'day', CAST(IL."NGAY_HET_HAN" AS TIMESTAMP)-CAST(den_ngay AS TIMESTAMP)    ) > 30
		AND  DATE_PART( 'day', CAST(IL."NGAY_HET_HAN" AS TIMESTAMP)-CAST(den_ngay AS TIMESTAMP)    ) <= 90
		THEN N'Sắp hết hạn 3 tháng'
		WHEN  DATE_PART( 'day', CAST(IL."NGAY_HET_HAN" AS TIMESTAMP)-CAST(den_ngay AS TIMESTAMP)    ) > 90
		AND  DATE_PART( 'day', CAST(IL."NGAY_HET_HAN" AS TIMESTAMP)-CAST(den_ngay AS TIMESTAMP)    ) <= 180
		THEN N'Sắp hết hạn 6 tháng'
		WHEN  DATE_PART( 'day', CAST(IL."NGAY_HET_HAN" AS TIMESTAMP)-CAST(den_ngay AS TIMESTAMP)    ) > 180
		THEN N'Sắp hết hạn trên 6 tháng'
		WHEN  DATE_PART( 'day', CAST(IL."NGAY_HET_HAN" AS TIMESTAMP)-CAST(den_ngay AS TIMESTAMP)    ) < 0
		THEN N'Quá hạn'
		ELSE ''
		END AS "NHOM_NGAY_HET_HAN" ,
		-- Sử lý lấy số ngày còn hạn -by ddnhan -10-05-2016 Công thức tính bằng ngày hết hạn-ngày chọn đến
		CASE WHEN IL."NGAY_HET_HAN" IS NOT NULL
		AND  DATE_PART( 'day', CAST(IL."NGAY_HET_HAN" AS TIMESTAMP)-CAST(den_ngay AS TIMESTAMP)    ) > 0
		THEN  DATE_PART( 'day', CAST(IL."NGAY_HET_HAN" AS TIMESTAMP)-CAST(den_ngay AS TIMESTAMP)    )
		ELSE 0
		END AS "SO_NGAY_CON_HAN" ,
		-- Sử lý lấy số ngày đã hết hạn -by ddnhan -10-05-2016 Công thức tính bằng ngày chọn đến-ngày ngày hết hạn
		CASE WHEN IL."NGAY_HET_HAN" IS NOT NULL
		AND  DATE_PART( 'day', CAST(IL."NGAY_HET_HAN" AS TIMESTAMP)-CAST(den_ngay AS TIMESTAMP)    ) < 0
		THEN  DATE_PART( 'day',  CAST(den_ngay AS TIMESTAMP) -CAST(IL."NGAY_HET_HAN" AS TIMESTAMP) )
		ELSE 0
		END AS "SO_NGAY_QUA_HAN"

		FROM    so_kho_chi_tiet IL
		INNER JOIN danh_muc_to_chuc OU ON IL."CHI_NHANH_ID" = OU."id"
		INNER JOIN TMP_KHO S ON IL."KHO_ID" = S."KHO_ID"
		INNER JOIN danh_muc_vat_tu_hang_hoa I ON IL."MA_HANG_ID" = I."id"
		LEFT JOIN ( SELECT  IIUC."VAT_TU_HANG_HOA_ID" ,
		"DVT_ID" ,
		( CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = '/'
			  THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
			  WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
			  THEN 1
			  ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
		END ) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
		FROM    danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
		WHERE   IIUC."STT" = don_vi_tinh
		) UC ON I."id" = UC."VAT_TU_HANG_HOA_ID"
		LEFT JOIN danh_muc_don_vi_tinh U ON ( UC."VAT_TU_HANG_HOA_ID" IS NULL
			AND U."id" = I."DVT_CHINH_ID"
		  )
		  OR ( UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
				AND UC."DVT_ID" = U."id"
			  )
		WHERE   ( don_vi_tinh IS NULL
		OR don_vi_tinh = 0
		OR UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
		)
		AND IL."NGAY_HACH_TOAN" <= den_ngay
		AND ( nhom_vthh_id IS NULL
		OR I."LIST_MPC_NHOM_VTHH" LIKE '%%;'
		||  MA_PHAN_CAP_VTHH  ||'%%'
		)
		AND ( OU."id" = chi_nhanh_id
		OR ( bao_gom_du_lieu_chi_nhanh_phu_thuoc = 1
		AND OU."HACH_TOAN_SELECTION" = '1'
		)
		)

		GROUP BY
		S."KHO_ID" ,
		S."MA_KHO" ,
		S."TEN_KHO" ,
		I."id" ,
		I."MA" ,
		I."TEN" ,

		IL."SO_LO" ,
		IL."NGAY_HET_HAN" ,
		U."DON_VI_TINH" ,
		UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"






		;

		END $$
		;

		SELECT  ROW_NUMBER() OVER ( ORDER BY "TEN_KHO" , "MA_KHO" , "MA", "SO_LO", "NGAY_HET_HAN" ) AS RowNum ,
							"TEN_KHO" AS "TEN_KHO",
							"MA" AS "MA_HANG",
							"TEN" AS "TEN_HANG",
							"SO_LO" AS "SO_LO",
							"NGAY_HET_HAN" AS "HAN_SU_DUNG",
							"DON_VI_TINH" AS "DVT",
							"SO_LUONG_TON" AS "SO_LUONG_TON",
							"NHOM_NGAY_HET_HAN" AS "NHOM_HAN_SU_DUNG",
							"SO_NGAY_CON_HAN" AS "SO_NGAY_CON_HAN",
							"SO_NGAY_QUA_HAN" AS "SO_NGAY_QUA_HAN"
						   
		FROM    TMP_KET_QUA
		WHERE   "SO_LUONG_TON" <> 0 
		;




		"""
		return self.execute(query,params_sql)
	
	def _lay_bao_cao_theo_so_lo(self, params_sql):      
		record = []
		query ="""
		--BAO_CAO_TONG_HOP_TON_KHO--số lô
		DO LANGUAGE plpgsql $$
		DECLARE

		tu_ngay                             DATE := %(TU_NGAY)s;

		--Từ
		den_ngay                            DATE := %(DEN_NGAY)s;
		--đến
		bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

		--bao gồm số liệu chi nhánh phụ thuộc
		chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;


		--chi nhánh

		don_vi_tinh                         INTEGER := %(DON_VI_TINH)s;
		--đơn vị tính
		nhom_vthh_id                        INTEGER := %(NHOM_VTHH_ID)s;
		--nhóm VTHH

		KHO_IDS                             INTEGER := -1;
		-- Kho
		rec                                 RECORD;
		CHE_DO_KE_TOAN                      INTEGER;

		MA_PHAN_CAP_VTHH                    VARCHAR(100);


		BEGIN


		SELECT value
		INTO CHE_DO_KE_TOAN
		FROM ir_config_parameter
		WHERE key = 'he_thong.CHE_DO_KE_TOAN'
		FETCH FIRST 1 ROW ONLY
		;


		SELECT "MA_PHAN_CAP" INTO MA_PHAN_CAP_VTHH
		FROM danh_muc_nhom_vat_tu_hang_hoa_dich_vu

		WHERE id = nhom_vthh_id
		;

		DROP TABLE IF EXISTS TMP_KHO
		;

		CREATE TEMP TABLE TMP_KHO
		AS
		SELECT
		"id" AS "KHO_ID"
		, "MA_KHO"
		, "TEN_KHO"
		FROM danh_muc_kho S

		WHERE (id = any(%(KHO_IDS)s))----Kho

		;


		DROP TABLE IF EXISTS TMP_KET_QUA
		;

		CREATE TEMP TABLE TMP_KET_QUA
		AS
		SELECT
		S."KHO_ID" ,
		S."MA_KHO" ,
		S."TEN_KHO" ,
		I."id" ,
		I."MA" ,
		I."TEN" ,

		IL."SO_LO" ,
		IL."NGAY_HET_HAN" ,
		U."DON_VI_TINH" ,
		SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN ( CASE WHEN U."id" IS NOT NULL
								AND IL."DVT_ID" = U."id" --Nếu đơn vị tính trên chứng từ = đơn vị tính được chọn thì lấy trên chứng từ
								THEN IL."SO_LUONG_NHAP"
								- IL."SO_LUONG_XUAT"
							ELSE ( IL."SO_LUONG_NHAP_THEO_DVT_CHINH" -- Nếu đơn vị tính trên chứng từ <> đơn vị tính được chọn thì lấy số lượng ĐVC * Tỷ lệ chuyển đổi trên danh mục
								  - IL."SO_LUONG_XUAT_THEO_DVT_CHINH" )
								* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
					  END )
				ELSE 0
		  END) AS "SO_LUONG_DAU_KY" , -- Tổng SL tồn đầu kỳ
		SUM(CASE WHEN IL."NGAY_HACH_TOAN" < tu_ngay
				THEN IL."SO_TIEN_NHAP" - IL."SO_TIEN_XUAT"
				ELSE 0
		  END) AS "GIA_TRI_DAU_KY" ,
		SUM(CASE WHEN IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
				THEN ( CASE WHEN U."id" IS NOT NULL
								AND IL."DVT_ID" = U."id" --Nếu đơn vị tính trên chứng từ = đơn vị tính được chọn thì lấy trên chứng từ
								THEN IL."SO_LUONG_NHAP"
							ELSE IL."SO_LUONG_NHAP_THEO_DVT_CHINH" -- Nếu đơn vị tính trên chứng từ <> đơn vị tính được chọn thì lấy số lượng ĐVC * Tỷ lệ chuyển đổi trên danh mục
								* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
					  END )
				ELSE 0
		  END) AS "NHAP_KHO_SO_LUONG" ,   -- Tổng SL nhập
		SUM(CASE WHEN IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
				THEN IL."SO_TIEN_NHAP"
				ELSE 0
		  END) AS "NHAP_KHO_GIA_TRI" ,
		SUM(CASE WHEN IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
				THEN ( CASE WHEN U."id" IS NOT NULL
								AND IL."DVT_ID" = U."id" --Nếu đơn vị tính trên chứng từ = đơn vị tính được chọn thì lấy trên chứng từ
								THEN IL."SO_LUONG_XUAT"
							ELSE IL."SO_LUONG_XUAT_THEO_DVT_CHINH" -- Nếu đơn vị tính trên chứng từ <> đơn vị tính được chọn thì lấy số lượng ĐVC * Tỷ lệ chuyển đổi trên danh mục
								* COALESCE(UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH", 1)
					  END )
				ELSE 0
		  END) AS "XUAT_KHO_SO_LUONG" ,    -- Tổng SL xuất
		SUM(CASE WHEN IL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
				THEN IL."SO_TIEN_XUAT"
				ELSE 0
		  END) AS "XUAT_KHO_GIA_TRI"  --Tổng giá trị xuất


		FROM    so_kho_chi_tiet IL
		INNER JOIN danh_muc_to_chuc OU ON IL."CHI_NHANH_ID" = OU."id"
		INNER JOIN TMP_KHO S ON IL."KHO_ID" = S."KHO_ID"
		INNER JOIN danh_muc_vat_tu_hang_hoa I ON IL."MA_HANG_ID" = I."id"
		LEFT JOIN ( SELECT  IIUC."VAT_TU_HANG_HOA_ID" ,
						  "DVT_ID" ,
						  ( CASE WHEN IIUC."PHEP_TINH_CHUYEN_DOI" = '/'
								  THEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
								  WHEN IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH" = 0
								  THEN 1
								  ELSE 1 / IIUC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
							END ) AS "TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"
				  FROM    danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi IIUC
				  WHERE   IIUC."STT" = don_vi_tinh
				) UC ON I."id" = UC."VAT_TU_HANG_HOA_ID"
		LEFT JOIN danh_muc_don_vi_tinh U ON ( UC."VAT_TU_HANG_HOA_ID" IS NULL
								AND U."id" = I."DVT_CHINH_ID"
							  )
							  OR ( UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
									AND UC."DVT_ID" = U."id"
								  )
		WHERE   ( don_vi_tinh IS NULL
		OR don_vi_tinh = 0
		OR UC."VAT_TU_HANG_HOA_ID" IS NOT NULL
		)
		AND IL."NGAY_HACH_TOAN" <= den_ngay
		AND ( nhom_vthh_id IS NULL
			OR I."LIST_MPC_NHOM_VTHH" LIKE '%%;'
			|| MA_PHAN_CAP_VTHH || '%%'
		  )
		AND ( OU."id" = chi_nhanh_id
			OR ( bao_gom_du_lieu_chi_nhanh_phu_thuoc = 1
				  AND OU."HACH_TOAN_SELECTION" = '1'
				)
		  )

		GROUP BY S."KHO_ID" ,
		S."MA_KHO" ,
		S."TEN_KHO" ,
		I."id" ,
		I."MA" ,
		I."TEN" ,

		IL."SO_LO" ,
		IL."NGAY_HET_HAN" ,
		U."DON_VI_TINH" ,
		UC."TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH"



		;

		END $$
		;
		SELECT  ROW_NUMBER() OVER ( ORDER BY "TEN_KHO" , "MA_KHO" , "MA" ) AS RowNum ,
	   "TEN_KHO" AS "TEN_KHO",
							"MA_KHO" AS "MA_KHO",
							"MA" AS "MA_HANG",
							"TEN" AS "TEN_HANG",
							"SO_LO" AS "SO_LO",
							"NGAY_HET_HAN" AS "HAN_SU_DUNG",
							"DON_VI_TINH" AS "DVT",
							"SO_LUONG_DAU_KY" AS "SO_LUONG_DAU_KY",
							"GIA_TRI_DAU_KY" AS "GIA_TRI_DAU_KY",
							"NHAP_KHO_SO_LUONG" AS "SO_LUONG_NHAP_KHO",
							"NHAP_KHO_GIA_TRI" AS "GIA_TRI_NHAP_KHO",
							"XUAT_KHO_SO_LUONG" AS "SO_LUONG_XUAT_KHO",
							"XUAT_KHO_GIA_TRI" AS "GIA_TRI_XUAT",
							"SO_LUONG_DAU_KY" + "NHAP_KHO_SO_LUONG" - "XUAT_KHO_SO_LUONG" AS "SO_LUONG_CUOI_KY" ,
							"GIA_TRI_DAU_KY" + "NHAP_KHO_GIA_TRI" - "XUAT_KHO_GIA_TRI" AS "GIA_TRI_CUOI_KY"


		FROM    TMP_KET_QUA
		WHERE   "SO_LUONG_DAU_KY" <> 0
		OR "GIA_TRI_DAU_KY" <> 0
		OR "NHAP_KHO_SO_LUONG" <> 0
		OR "NHAP_KHO_GIA_TRI" <> 0
		OR "XUAT_KHO_SO_LUONG" <> 0
		OR "XUAT_KHO_GIA_TRI" <> 0

		;
		"""
		return self.execute(query,params_sql)

	### END IMPLEMENTING CODE ###

	def _action_view_report(self):
		self._validate()
		TU_NGAY_F = self.get_vntime('TU')
		DEN_NGAY_F = self.get_vntime('DEN')
		THONG_KE_THEO = self.get_context('THONG_KE_THEO')
		param = 'Từ ngày %s đến ngày %s' % ( TU_NGAY_F, DEN_NGAY_F)
		if( THONG_KE_THEO=='KHONG_CHON'):
			
			action = self.env.ref('bao_cao.open_report_tong_hop_ton_kho_khong_chon').read()[0]
		elif( THONG_KE_THEO=='TONG_HOP_TREN_NHIEU_KHO'):
			
			action = self.env.ref('bao_cao.open_report_tong_hop_ton_kho_tren_nhieu_kho').read()[0]
		elif( THONG_KE_THEO=='HAN_SU_DUNG'):
			
			action = self.env.ref('bao_cao.open_report_tong_hop_ton_kho_han_su_dung').read()[0]
		elif( THONG_KE_THEO=='SO_LO'):
			kho4s = self._context.get('KHO_ID_4')
			
			action = self.env.ref('bao_cao.open_report_tong_hop_ton_kho_so_lo').read()[0]
		else:
			action = self.env.ref('bao_cao.open_report_tong_hop_ton_kho_ma_quy_cach').read()[0]
		action['context'] = eval(action.get('context','{}').replace('\n',''))
		action['context'].update({'breadcrumb_ex': param})
		return action

	@api.model
	def default_get(self,default_fields):
		res = super(BAO_CAO_TONG_HOP_TON_KHO, self).default_get(default_fields)
		# res['KHO_ID_MASTER'] = -1
		chi_nhanh =  self.env['danh.muc.to.chuc'].search([],order="MA_DON_VI",limit=1)
		if chi_nhanh:
		  res['CHI_NHANH_ID'] = chi_nhanh.id

		return res

	@api.onchange('KY_BAO_CAO')
	def _cap_nhat_ngay(self):
		self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')

	selection_tong_hop_tren_nhieu_kho = fields.Selection([
		('1', 'Tất cả'),
		('2','Có nhập xuất tồn'),
		 ('3','Phát sinh nhập xuất'),
		], default='2',string="Hiển thị")

