# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields,helper
from odoo.addons import decimal_precision
class TONG_HOP_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE(models.Model):
	_name = 'tong.hop.danh.gia.lai.tai.khoan.ngoai.te'
	_description = ''
	_auto = False

	DANH_GIA_NGOAI_TE_ID = fields.Many2one('res.currency', string='Đánh giá ngoại tệ', help='Đánh giá ngoại tệ',default=lambda self: self.lay_loai_tien_mac_dinh())
	DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày',default=fields.Datetime.now)
	TK_XU_LY_LAI_CHENH_LECH_TY_GIA_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK xử lý lãi chênh lệch tỷ giá', help='Tk xử lý lãi chênh lệch tỷ giá')
	TY_GIA_MUA = fields.Float(string='Tỷ giá mua', help='Tỷ giá mua',digits= decimal_precision.get_precision('VND'))
	TY_GIA_BAN = fields.Float(string='Tỷ giá bán', help='Tỷ giá bán',digits= decimal_precision.get_precision('VND'))
	TK_XU_LY_LO_CHENH_LECH_TY_GIA_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK xử lý lỗ chênh lệch tỷ giá', help='Tk xử lý lỗ chênh lệch tỷ giá')
	name = fields.Char(string='Name', help='Name', oldname='NAME')
	SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
	#FIELD_IDS = fields.One2many('model.name')
	#@api.model
	#def default_get(self, fields_list):
	#   result = super(TONG_HOP_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE, self).default_get(fields_list)
	#   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
	#   return result
	TONG_HOP_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE_CONG_NO_THANH_TOAN_IDS = fields.One2many('tong.hop.danh.gia.lai.tai.khoan.ngoai.te.cong.no.thanh.toan', 'DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE_ID', string='Đánh giá lại tài khoản ngoại tệ công nợ thanh toán')
	TONG_HOP_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE_SO_DU_NGOAI_TE_IDS = fields.One2many('tong.hop.danh.gia.lai.tai.khoan.ngoai.te.so.du.ngoai.te', 'DANH_GIA_LAI_TAI_KHOAN_NGUYEN_TE_ID', string='Đánh giá lại tài khoản ngoại tệ số dư ngoại tệ')


	@api.model
	def default_get(self, fields):
		rec = super(TONG_HOP_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE, self).default_get(fields)
		rec['TK_XU_LY_LAI_CHENH_LECH_TY_GIA_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '515')],limit=1).id
		rec['TK_XU_LY_LO_CHENH_LECH_TY_GIA_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '635')],limit=1).id
		rec['DANH_GIA_NGOAI_TE_ID'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'USD')],limit=1).id
		return rec

	# Hàm thực hiện thay đổi tỷ giá ở các dòng số dư ngoại tệ khi thay đổi tỷ giá mua , tỷ giá bán
	@api.onchange('TY_GIA_MUA','TY_GIA_BAN')
	def update_ty_gia_so_du_ngoai_te(self):
		if self.TONG_HOP_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE_SO_DU_NGOAI_TE_IDS:
			for line in self.TONG_HOP_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE_SO_DU_NGOAI_TE_IDS:
				# Todo -  Tạm thời đang fix TK ngân hàng = False 
				line.TK_NGAN_HANG_ID = False
				# nếu tài khoản chi tiết theo nhân viên thì không thay đổi loại tiền
				if line.TAI_KHOAN_ID.DOI_TUONG_SELECTION != '2':
				# Nếu số tiền dư nợ > 0  thì tỷ giá  = tỷ giá mua
					if line.SO_TIEN_DU_NO > 0:
						line.TY_GIA = self.TY_GIA_MUA
				# nếu số tiền dư có > 0 thì tỷ giá =  tỷ giá bán
					elif line.SO_TIEN_DU_CO > 0 : 
						line.TY_GIA = self.TY_GIA_BAN

	@api.onchange('DANH_GIA_NGOAI_TE_ID')
	def update_ty_gia(self):
		self.TY_GIA_MUA = self.DANH_GIA_NGOAI_TE_ID.TY_GIA_QUY_DOI
		self.TY_GIA_BAN = self.DANH_GIA_NGOAI_TE_ID.TY_GIA_QUY_DOI

	#  Hàm lấy dữ liệu khi thay đổi Đánh giá ngoại tệ
	@api.model
	def load_ud(self,args):
		new_line_so_ngoai_te = [[5]]
		new_line_chung_tu_cong_no_va_thanh_toan = [[5]]
		loai_tien_id = False
		if (args['loai_tien_id']):
			loai_tien_id = args['loai_tien_id']
		dl_tab_1 = self.lay_du_lieu(loai_tien_id,1)
		for record in dl_tab_1 :
			# danh gia lai =  tygia *  so tien
			ty_gia_hien_tai = self.DANH_GIA_NGOAI_TE_ID.TY_GIA_QUY_DOI
			danh_gia_lai_du_no = ty_gia_hien_tai * record['SO_TIEN_DU_NO']
			danh_gia_lai_du_co =  ty_gia_hien_tai * record['SO_TIEN_DU_CO']
			# chenh lech = quy doi - danh gia lai
			chenh_lech_du_no = danh_gia_lai_du_no - record['SO_TIEN_QUY_DOI_DU_NO']
			chenh_lech_du_co = danh_gia_lai_du_co - record['SO_TIEN_QUY_DOI_DU_CO']


			new_line_so_ngoai_te += [(0, 0, {
					'TAI_KHOAN_ID': [record['TAI_KHOAN_ID'],record['MA_TAI_KHOAN']],
					'TK_NGAN_HANG_ID': [record['TK_NGAN_HANG_ID'],record['SO_TAI_KHOAN_NGAN_HANG']],
					'TEN_NGAN_HANG': record['TEN_NGAN_HANG'],
					'DOI_TUONG_ID': [record['DOI_TUONG_ID'],record['MA_DOI_TUONG']],
					'TY_GIA':  ty_gia_hien_tai,
					'SO_TIEN_DU_NO': record['SO_TIEN_DU_NO'],
					'QUY_DOI_DU_NO': record['SO_TIEN_QUY_DOI_DU_NO'],
					'DANH_GIA_LAI_DU_NO': danh_gia_lai_du_no,
					'CHENH_LECH_DU_NO': chenh_lech_du_no,
					'SO_TIEN_DU_CO': record['SO_TIEN_DU_CO'],
					'QUY_DOI_DU_CO': record['SO_TIEN_QUY_DOI_DU_CO'],
					'DANH_GIA_LAI_DU_CO': danh_gia_lai_du_co,
					'CHENH_LECH_DU_CO': chenh_lech_du_co,
					})]
		dl_tab_2 = self.lay_du_lieu(loai_tien_id,2)
		for record_cnva_tt in dl_tab_2 :
			new_line_chung_tu_cong_no_va_thanh_toan += [(0, 0, {
					'LOAI_CHUNG_TU': record_cnva_tt['TEN_LOAI_CHUNG_TU'],
					'NGAY_CHUNG_TU':  record_cnva_tt['NGAY_CHUNG_TU'],
					'SO_CHUNG_TU':  record_cnva_tt['SO_CHUNG_TU'],
					'SO_HOA_DON':  record_cnva_tt['SO_HOA_DON'],
					'DIEN_GIAI':  record_cnva_tt['DIEN_GIAI_CHUNG'],
					'TK_CONG_NO_ID':  [record_cnva_tt['TAI_KHOAN_ID'],record_cnva_tt['MA_TAI_KHOAN']],
					'DOI_TUONG_ID':   [record_cnva_tt['DOI_TUONG_ID'],record_cnva_tt['MA_DOI_TUONG']],
					'TY_GIA_TREN_CT':  record_cnva_tt['TY_GIA'],
					'TY_GIA_DANH_GIA_LAI_GAN_NHAT':  record_cnva_tt['TY_GIA_DANH_GIA_LAI_GAN_NHAT'],
					'SO_CHUA_DOI_TRU':  record_cnva_tt['SO_CHUA_DOI_TRU'],
					'SO_CHUA_DOI_TRU_QUY_DOI':  record_cnva_tt['SO_CHUA_DOI_TRU_QUY_DOI'],
					'DANH_GIA_LAI':  record_cnva_tt['SO_CHUA_DOI_TRU_QUY_DOI'],
					'CHENH_LECH':  record_cnva_tt['CHENH_LECH'],
					'ID_CHUNG_TU_GOC':  record_cnva_tt['CHUNG_TU_ID'],
					'MODEL_CHUNG_TU_GOC':  record_cnva_tt['MODEL_CHUNG_TU'],
					'ID_TK_VA_ID_DOI_TUONG' : str(record_cnva_tt['TAI_KHOAN_ID']) + ',' + str(record_cnva_tt['DOI_TUONG_ID']),
					})]
		return {
			'TONG_HOP_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE_SO_DU_NGOAI_TE_IDS':new_line_so_ngoai_te ,
			'TONG_HOP_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE_CONG_NO_THANH_TOAN_IDS':new_line_chung_tu_cong_no_va_thanh_toan,
		}

	# Hàm lấy dữ liệu khi load form
	@api.model
	def load_UI(self,args):
		new_line_so_ngoai_te = [[5]]
		new_line_chung_tu_cong_no_va_thanh_toan = [[5]]
		loai_tien_id = False
		tien_usd = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'USD')],limit=1)
		if (self.DANH_GIA_NGOAI_TE_ID.id):
			loai_tien_id = self.DANH_GIA_NGOAI_TE_ID.id
		dl_tab_1 = self.lay_du_lieu(loai_tien_id,1)
		for record in dl_tab_1 :
			# danh gia lai =  tygia *  so tien
			ty_gia_hien_tai = self.DANH_GIA_NGOAI_TE_ID.TY_GIA_QUY_DOI
			danh_gia_lai_du_no = ty_gia_hien_tai * record['SO_TIEN_DU_NO']
			danh_gia_lai_du_co =  ty_gia_hien_tai * record['SO_TIEN_DU_CO']
			# chenh lech = quy doi - danh gia lai
			chenh_lech_du_no = danh_gia_lai_du_no - record['SO_TIEN_QUY_DOI_DU_NO']
			chenh_lech_du_co = danh_gia_lai_du_co - record['SO_TIEN_QUY_DOI_DU_CO']


			new_line_so_ngoai_te += [(0, 0, {
					'TAI_KHOAN_ID': [record['TAI_KHOAN_ID'],record['MA_TAI_KHOAN']],
					'TK_NGAN_HANG_ID': [record['TK_NGAN_HANG_ID'],record['SO_TAI_KHOAN_NGAN_HANG']],
					'TEN_NGAN_HANG': record['TEN_NGAN_HANG'],
					'DOI_TUONG_ID': [record['DOI_TUONG_ID'],record['MA_DOI_TUONG']],
					'TY_GIA':  ty_gia_hien_tai,
					'SO_TIEN_DU_NO': record['SO_TIEN_DU_NO'],
					'QUY_DOI_DU_NO': record['SO_TIEN_QUY_DOI_DU_NO'],
					'DANH_GIA_LAI_DU_NO': danh_gia_lai_du_no,
					'CHENH_LECH_DU_NO': chenh_lech_du_no,
					'SO_TIEN_DU_CO': record['SO_TIEN_DU_CO'],
					'QUY_DOI_DU_CO': record['SO_TIEN_QUY_DOI_DU_CO'],
					'DANH_GIA_LAI_DU_CO': danh_gia_lai_du_co,
					'CHENH_LECH_DU_CO': chenh_lech_du_co,
                    'currency_id' : [tien_usd.id,tien_usd.MA_LOAI_TIEN],
					})]
		dl_tab_2 = self.lay_du_lieu(loai_tien_id,2)
		for record_cnva_tt in dl_tab_2 :
			new_line_chung_tu_cong_no_va_thanh_toan += [(0, 0, {
					'LOAI_CHUNG_TU': record_cnva_tt['TEN_LOAI_CHUNG_TU'],
					'NGAY_CHUNG_TU':  record_cnva_tt['NGAY_CHUNG_TU'],
					'SO_CHUNG_TU':  record_cnva_tt['SO_CHUNG_TU'],
					'SO_HOA_DON':  record_cnva_tt['SO_HOA_DON'],
					'DIEN_GIAI':  record_cnva_tt['DIEN_GIAI_CHUNG'],
					'TK_CONG_NO_ID':  [record_cnva_tt['TAI_KHOAN_ID'],record_cnva_tt['MA_TAI_KHOAN']],
					'DOI_TUONG_ID':   [record_cnva_tt['DOI_TUONG_ID'],record_cnva_tt['MA_DOI_TUONG']],
					'TY_GIA_TREN_CT':  record_cnva_tt['TY_GIA'],
					'TY_GIA_DANH_GIA_LAI_GAN_NHAT':  record_cnva_tt['TY_GIA_DANH_GIA_LAI_GAN_NHAT'],
					'SO_CHUA_DOI_TRU':  record_cnva_tt['SO_CHUA_DOI_TRU'],
					'SO_CHUA_DOI_TRU_QUY_DOI':  record_cnva_tt['SO_CHUA_DOI_TRU_QUY_DOI'],
					'DANH_GIA_LAI':  record_cnva_tt['SO_CHUA_DOI_TRU_QUY_DOI'],
					'CHENH_LECH':  record_cnva_tt['CHENH_LECH'],
					'ID_CHUNG_TU_GOC':  record_cnva_tt['CHUNG_TU_ID'],
					'MODEL_CHUNG_TU_GOC':  record_cnva_tt['MODEL_CHUNG_TU'],
					'ID_TK_VA_ID_DOI_TUONG' : str(record_cnva_tt['TAI_KHOAN_ID']) + ',' + str(record_cnva_tt['DOI_TUONG_ID']),
					})]
		return {
			'TONG_HOP_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE_SO_DU_NGOAI_TE_IDS':new_line_so_ngoai_te ,
			'TONG_HOP_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE_CONG_NO_THANH_TOAN_IDS':new_line_chung_tu_cong_no_va_thanh_toan,
		}


	


	def lay_du_lieu(self, loai_tien_id ,tab):		
		record =[]
		params = {
			'currency_id': loai_tien_id,
			'CHI_NHANH_ID' : self.get_chi_nhanh(),
			}
		query_dk = ''
		if tab == 1 :
			query_dk = """SELECT *FROM TMP_TABLE_1;"""
		elif tab == 2:
			query_dk = """SELECT *FROM TMP_TABLE_2;"""

		query = """  
				DO LANGUAGE plpgsql $$
				DECLARE
				tham_so_chi_nhanh_id INTEGER:= %(CHI_NHANH_ID)s;
				tham_so_loai_tien_id INTEGER:=%(currency_id)s;
				tham_so_den_ngay DATE := now();
				phep_tinh_quy_doi INTEGER:= 0;
				dinh_dang_kieu_tien INTEGER:=0;
				dinh_dang_kieu_ty_gia INTEGER:=2;
				PHAN_THAP_PHAN_TY_GIA INTEGER;

				BEGIN

                SELECT value
                INTO PHAN_THAP_PHAN_TY_GIA
                FROM ir_config_parameter
                WHERE key = 'he_thong.PHAN_THAP_PHAN_TY_GIA'
                FETCH FIRST 1 ROW ONLY
                ;


                SELECT CASE WHEN "PHEP_TINH_QUY_DOI" = 'NHAN'
                    THEN 0
                       ELSE 1 END
                INTO phep_tinh_quy_doi
                FROM res_currency
                WHERE id = tham_so_loai_tien_id
                ;

                DROP TABLE IF EXISTS TMP_ACCOUNT
                ;

                CREATE TEMP TABLE TMP_ACCOUNT
                    AS
                        SELECT
                              A.id                    AS "TAI_KHOAN_ID"
                            , A."SO_TAI_KHOAN"        AS "MA_TAI_KHOAN"
                            , A."TINH_CHAT"
                            , A."CHI_TIET_THEO_DOI_TUONG"
                            , A."DOI_TUONG_SELECTION" AS "LOAI_DOI_TUONG"
                            , A."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG"
                        FROM danh_muc_he_thong_tai_khoan AS A
                        WHERE A."CO_HACH_TOAN_NGOAI_TE" = TRUE
                              AND A."LA_TK_TONG_HOP" = FALSE
                              AND left(A."SO_TAI_KHOAN", 1) <> '0'
                              AND active = TRUE
                ;

                DROP TABLE IF EXISTS TMP_SO_CAI
                ;

                CREATE TEMP TABLE TMP_SO_CAI
                    AS
                        /*
                        Insert vào bảng #GeneralLedger số dư các tài khoản:
                        - Có theo dõi ngoại tệ
                        - Chi tiết theo:
                        +) RefDetailID
                        +) Đối tượng
                        +) Tài khoản
                        - Không bao gồm số dư đầu kỳ (vì số dư đầu cần lấy các thông tin chi tiết từ chứng từ gốc)
                        */
                        SELECT
                            GL."ID_CHUNG_TU"

                            , GL."CHI_TIET_ID"

                            , NULL :: INT                                                       AS "LA_CHUNG_TU_GHI_NO"
                            , GL."LOAI_CHUNG_TU"
                            , GL."NGAY_CHUNG_TU"
                            , GL."NGAY_HACH_TOAN"
                            , GL."SO_CHUNG_TU"
                            , GL."SO_HOA_DON"
                            , GL."NGAY_HOA_DON"
                            , GL."DIEN_GIAI_CHUNG"
                            , GL."MA_TAI_KHOAN"
                            , GL."TAI_KHOAN_ID"
                            , A."TINH_CHAT"                                                     AS "TINH_CHAT_TAI_KHOAN"
                            , GL."DOI_TUONG_ID"
                            , AO."MA"                                                           AS "MA_DOI_TUONG"
                            , AO."HO_VA_TEN"                                                    AS "TEN_DOI_TUONG"
                            , A."CHI_TIET_THEO_DOI_TUONG"
                            , A."LOAI_DOI_TUONG"
                            , A."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG"
                            , CASE WHEN A."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG" = TRUE
                            THEN GL."TAI_KHOAN_NGAN_HANG_ID"
                              ELSE NULL
                              END                                                               AS "TK_NGAN_HANG_ID"
                            , /*ntlieu 07/09/2016 sửa bug 116847
                                            Khi chứng từ chi có 2 phát sinh tỷ giá xuất quỹ thì 1 dòng chi tiết hiển thị thành 2 dòng do khác tỷ giá xuất quỹ -> số tồn nguyên tệ, quy đổi tính sai*/
                              MAX(ROUND(CAST((GL."TY_GIA") AS NUMERIC), PHAN_THAP_PHAN_TY_GIA)) AS "TY_GIA"
                            , SUM(GL."GHI_NO_NGUYEN_TE")                                        AS "GHI_NO_NGUYEN_TE"
                            , SUM(GL."GHI_NO")                                                  AS "GHI_NO"
                            , SUM(GL."GHI_CO_NGUYEN_TE")                                        AS "GHI_CO_NGUYEN_TE"
                            , SUM(GL."GHI_CO")                                                  AS "GHI_CO"
                            , "MODEL_CHUNG_TU"
                            , GL."CHI_TIET_MODEL"
                        FROM so_cai_chi_tiet AS GL
                            INNER JOIN TMP_ACCOUNT AS A ON GL."MA_TAI_KHOAN" = A."MA_TAI_KHOAN"
                            LEFT JOIN res_partner AO ON GL."DOI_TUONG_ID" = AO.id
                        WHERE GL."CHI_NHANH_ID" = tham_so_chi_nhanh_id
                              AND GL."NGAY_HACH_TOAN" <= tham_so_den_ngay
                              AND GL."currency_id" = tham_so_loai_tien_id
                              AND GL."LOAI_CHUNG_TU" NOT IN ('612', '613')  -- Không bao gồm số dư đầu kỳ
                              --ntquang edited 27.09.2017: Sửa bug 145960
                              AND (GL."LOAI_CHUNG_TU" NOT IN ('4016') OR A."CHI_TIET_THEO_DOI_TUONG" =
                                                                         FALSE   --BTAnh 24/06/2015: lấy những dòng đánh giá lại tài khoản ngoại tệ mà không chi tiết theo đối tượng
                              )
                              -- ptnam edit 14-06-2018 : Sửa bug 230444
                              AND ((A."CHI_TIET_THEO_DOI_TUONG" = FALSE) OR
                                   ((A."CHI_TIET_THEO_DOI_TUONG" = TRUE) AND AO.id IS NOT NULL))
                        GROUP BY
                            GL."ID_CHUNG_TU",
                            GL."CHI_TIET_ID",
                            GL."LOAI_CHUNG_TU",
                            GL."NGAY_CHUNG_TU",
                            GL."NGAY_HACH_TOAN",
                            GL."SO_CHUNG_TU",
                            GL."SO_HOA_DON",
                            GL."NGAY_HOA_DON",
                            GL."DIEN_GIAI_CHUNG",
                            GL."TAI_KHOAN_ID",
                            GL."MA_TAI_KHOAN",
                            A."TINH_CHAT",
                            GL."DOI_TUONG_ID",
                            AO."MA",
                            AO."HO_VA_TEN",
                            A."CHI_TIET_THEO_DOI_TUONG",
                            A."LOAI_DOI_TUONG",
                            A."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG",
                            CASE WHEN A."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG" = TRUE
                                THEN GL."TAI_KHOAN_NGAN_HANG_ID"
                            ELSE NULL
                            END,
                            "MODEL_CHUNG_TU",
                            GL."CHI_TIET_MODEL"
                ;

                --,
                -- ROUND(GL.ExchangeRate,@ExchangRateDecimalDigits)
                INSERT INTO TMP_SO_CAI
                    (
                        SELECT
                              GLD."ID_CHUNG_TU_GOC"                                                 AS "ID_CHUNG_TU"
                            , GLD.id                                                                AS "CHI_TIET_ID"
                            , NULL :: INT                                                           AS LA_CHUNG_TU_GHI_NO
                            , (SELECT "REFTYPE"
                               FROM danh_muc_reftype RT
                               WHERE RT.id = GLD."LOAI_CHUNG_TU_ID")                                AS "LOAI_CHUNG_TU"
                            , GLD."NGAY_CHUNG_TU"
                            , GLD."NGAY_HACH_TOAN"                                                  AS "NGAY_HACH_TOAN"
                            , '#'                                                                   AS "SO_CHUNG_TU"
                            , GLD."SO_HOA_DON"
                            , GLD."NGAY_HOA_DON"                                                    AS "NGAY_HOA_DON"
                            , N''                                                                  AS "DIEN_GIAI_CHUNG"
                            , AC."SO_TAI_KHOAN"                                                     AS "MA_TAI_KHOAN"
                            , GLD."TK_CONG_NO_ID"                                                   AS "TAI_KHOAN_ID"
                            , A."TINH_CHAT"
                            , GLD."DOI_TUONG_ID"
                            , AO."MA"                                                               AS "MA_DOI_TUONG"
                            , AO."HO_VA_TEN"                                                        AS "TEN_DOI_TUONG"
                            , A."CHI_TIET_THEO_DOI_TUONG"
                            , A."LOAI_DOI_TUONG"
                            , A."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG"
                            , CAST(NULL AS INTEGER)                                                 AS "TK_NGAN_HANG_ID"
                            , --Tạm thế này
                              ROUND(CAST((GLD."TY_GIA_TREN_CT") AS NUMERIC), PHAN_THAP_PHAN_TY_GIA) AS "TY_GIA"
                            , 0                                                                        "GHI_NO_NGUYEN_TE"
                            , SUM(CASE WHEN A."LOAI_DOI_TUONG" = '1'
                            THEN GLD."CHENH_LECH"
                                  ELSE 0
                                  END)                                                              AS "GHI_NO"
                            , 0                                                                     AS "GHI_CO_NGUYEN_TE"
                            , SUM(CASE WHEN A."LOAI_DOI_TUONG" = '0'
                            THEN GLD."CHENH_LECH"
                                  ELSE 0
                                  END)                                                              AS "GHI_CO"
                            , GLD."MODEL_CHUNG_TU_GOC"                                              AS "MODEL_CHUNG_TU"
                            , 'tong.hop.chung.tu.nghiep.vu.khac.cong.no.thanh.toan'                 AS "CHI_TIET_MODEL"
                        FROM account_ex_chung_tu_nghiep_vu_khac AS GL
                            JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan AS GLD
                                ON GL.id = GLD."CHUNG_TU_NGHIEP_VU_KHAC_ID"
                            INNER JOIN TMP_ACCOUNT AS A ON GLD."TK_CONG_NO_ID" = A."TAI_KHOAN_ID"
                            LEFT JOIN res_partner AS AO ON GLD."DOI_TUONG_ID" = AO.id
                            LEFT JOIN danh_muc_he_thong_tai_khoan AC ON GLD."TK_CONG_NO_ID" = AC.id
                        WHERE GL."NGAY_HACH_TOAN" <= tham_so_den_ngay
                              AND GL."currency_id" = tham_so_loai_tien_id
                              AND GL."CHI_NHANH_ID" = tham_so_chi_nhanh_id
                              AND GL.state = 'da_ghi_so'
                        GROUP BY
                            GLD."ID_CHUNG_TU_GOC",
                            GLD.id,
                            (SELECT "REFTYPE"
                             FROM danh_muc_reftype RT
                             WHERE RT.id = GLD."LOAI_CHUNG_TU_ID"),
                            GLD."NGAY_CHUNG_TU",
                            GLD."NGAY_HACH_TOAN",
                            GLD."SO_HOA_DON",
                            GLD."NGAY_HOA_DON",
                            GLD."DIEN_GIAI",
                            AC."SO_TAI_KHOAN",
                            GLD."TK_CONG_NO_ID",
                            A."TINH_CHAT",
                            GLD."DOI_TUONG_ID",
                            AO."MA",
                            AO."HO_VA_TEN",
                            A."CHI_TIET_THEO_DOI_TUONG",
                            A."LOAI_DOI_TUONG",
                            A."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG",
                            ROUND(CAST((GLD."TY_GIA_TREN_CT") AS NUMERIC), PHAN_THAP_PHAN_TY_GIA),
                            "MODEL_CHUNG_TU",
                            "CHI_TIET_MODEL"
                    )
                ;

                -- Insert vào bảng #GeneralLedger số dư ban đầu (do bên trên chưa lấy)
                INSERT INTO TMP_SO_CAI
                    (
                        SELECT
                              OPN.id                                                                    AS "ID_CHUNG_TU"
                            , OPND.id                                                                   AS "CHI_TIET_ID"
                            , NULL :: INT                                                               AS "LA_CHUNG_TU_GHI_NO"
                            , OPN."LOAI_CHUNG_TU"
                            , CASE WHEN OPND.id IS NOT NULL AND coalesce(OPND."SO_THU_TRUOC_NGUYEN_TE", 0) <> 0
                            THEN OPND."NGAY_HOA_DON"
                              ELSE OPN."NGAY_HACH_TOAN" END                                             AS "NGAY_CHUNG_TU"
                            , OPN."NGAY_HACH_TOAN"
                            , CASE WHEN OPND.id IS NOT NULL AND coalesce(OPND."SO_THU_TRUOC_NGUYEN_TE", 0) <> 0
                            THEN OPND."SO_HOA_DON"
                              ELSE N'OPN' END                                                          AS "SO_CHUNG_TU"
                            , CASE WHEN OPND.id IS NOT NULL
                            THEN OPND."SO_HOA_DON"
                              ELSE N'' END                                                             AS "SO_HOA_DON"
                            , OPND."NGAY_HOA_DON"
                            , N''                                                                      AS "DIEN_GIAI_CHUNG"
                            , OPN."SO_TAI_KHOAN"                                                        AS "MA_TAI_KHOAN"
                            , OPN."TK_ID"                                                               AS "TAI_KHOAN_ID"
                            , A."TINH_CHAT"
                            , OPN."DOI_TUONG_ID"
                            , AO."MA"                                                                   AS "MA_DOI_TUONG"
                            , AO."HO_VA_TEN"                                                            AS "TEN_DOI_TUONG"
                            , A."CHI_TIET_THEO_DOI_TUONG"
                            , A."LOAI_DOI_TUONG"
                            , A."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG"
                            , CASE WHEN A."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG" = TRUE
                            THEN OPN."TK_NGAN_HANG_ID"
                              ELSE NULL
                              END                                                                       AS "TK_NGAN_HANG_ID"
                            , ROUND(cast(coalesce(OPND."TY_GIA", 0) AS NUMERIC), PHAN_THAP_PHAN_TY_GIA) AS "TY_GIA"
                            , SUM(CASE WHEN A."LOAI_DOI_TUONG" = '1'
                                            AND OPND.id IS NOT NULL AND coalesce(OPND."SO_THU_TRUOC_NGUYEN_TE", 0) = 0
                            THEN OPND."SO_CON_PHAI_THU_NGUYEN_TE"
                                  WHEN A."LOAI_DOI_TUONG" = '1'
                                       AND OPND.id IS NULL
                                      THEN OPN."DU_NO_NGUYEN_TE"
                                  WHEN A."LOAI_DOI_TUONG" = '0'
                                       AND OPND.id IS NOT NULL AND coalesce(OPND."SO_THU_TRUOC_NGUYEN_TE", 0) <> 0
                                      THEN coalesce(OPND."SO_THU_TRUOC_NGUYEN_TE", 0)
                                  ELSE 0
                                  END)                                                                  AS "GHI_NO_NGUYEN_TE"
                            , SUM(CASE WHEN A."LOAI_DOI_TUONG" = '1'
                                            AND OPND.id IS NOT NULL AND coalesce(OPND."SO_THU_TRUOC", 0) = 0
                            THEN OPND."SO_CON_PHAI_THU"
                                  WHEN A."LOAI_DOI_TUONG" = '1'
                                       AND OPND.id IS NULL
                                      THEN OPN."DU_NO"
                                  WHEN A."LOAI_DOI_TUONG" = '0'
                                       AND OPND.id IS NOT NULL AND coalesce(OPND."SO_THU_TRUOC", 0) <> 0
                                      THEN coalesce(OPND."SO_THU_TRUOC", 0)
                                  ELSE 0
                                  END)                                                                  AS "DU_NO"
                            , SUM(CASE WHEN A."LOAI_DOI_TUONG" = '0'
                                            AND OPND.id IS NOT NULL AND coalesce(OPND."SO_THU_TRUOC_NGUYEN_TE", 0) = 0
                            THEN OPND."SO_CON_PHAI_THU_NGUYEN_TE"
                                  WHEN A."LOAI_DOI_TUONG" = '0'
                                       AND OPND.id IS NULL
                                      THEN OPN."DU_CO_NGUYEN_TE"
                                  WHEN A."LOAI_DOI_TUONG" = '1'
                                       AND OPND.id IS NOT NULL AND coalesce(OPND."SO_THU_TRUOC_NGUYEN_TE", 0) <> 0
                                      THEN coalesce(OPND."SO_THU_TRUOC_NGUYEN_TE", 0)
                                  ELSE 0
                                  END)                                                                  AS "GHI_CO_NGUYEN_TE"
                            , SUM(CASE WHEN A."LOAI_DOI_TUONG" = '0'
                                            AND OPND.id IS NOT NULL AND coalesce(OPND."SO_THU_TRUOC", 0) = 0
                            THEN OPND."SO_CON_PHAI_THU"
                                  WHEN A."LOAI_DOI_TUONG" = '0'
                                       AND OPND.id IS NULL
                                      THEN OPN."DU_CO"
                                  WHEN A."LOAI_DOI_TUONG" = '1'
                                       AND OPND.id IS NOT NULL AND coalesce(OPND."SO_THU_TRUOC", 0) <> 0
                                      THEN coalesce(OPND."SO_THU_TRUOC", 0)
                                  ELSE 0
                                  END)                                                                  AS "GHI_CO"
                            , 'account.ex.so.du.tai.khoan.chi.tiet'                                     AS "MODEL_CHUNG_TU"
                            , 'account.ex.sdtkct.theo.hoa.don'                                          AS "CHI_TIET_MODEL"
                        FROM account_ex_so_du_tai_khoan_chi_tiet AS OPN
                            INNER JOIN TMP_ACCOUNT AS A ON OPN."TK_ID" = A."TAI_KHOAN_ID"
                            INNER JOIN res_partner AS AO ON OPN."DOI_TUONG_ID" = AO.id
                            LEFT JOIN account_ex_sdtkct_theo_hoa_don AS OPND
                                ON OPN.id = OPND."SO_DU_TAI_KHOAN_CHI_TIET_ID"
                        WHERE OPN."CHI_NHANH_ID" = tham_so_chi_nhanh_id
                              AND OPN.state = 'da_ghi_so'
                              AND OPN."NGAY_HACH_TOAN" <= tham_so_den_ngay
                              AND OPN."currency_id" = tham_so_loai_tien_id
                              AND OPN."LOAI_CHUNG_TU" IN ('612', '613')
                        GROUP BY OPN.id,
                            OPND.id,
                            OPN."LOAI_CHUNG_TU",
                            CASE WHEN OPND.id IS NOT NULL AND coalesce(OPND."SO_THU_TRUOC_NGUYEN_TE", 0) <> 0
                                THEN OPND."NGAY_HOA_DON"
                            ELSE OPN."NGAY_HACH_TOAN" END,
                            CASE WHEN OPND.id IS NOT NULL AND coalesce(OPND."SO_THU_TRUOC_NGUYEN_TE", 0) <> 0
                                THEN OPND."SO_HOA_DON"
                            ELSE N'OPN' END,
                            OPN."NGAY_HACH_TOAN",
                            CASE WHEN OPND.id IS NOT NULL
                                THEN OPND."SO_HOA_DON"
                            ELSE N'' END,
                            OPND."NGAY_HOA_DON",
                            OPN."TK_ID",
                            OPN."SO_TAI_KHOAN",
                            A."TINH_CHAT",
                            OPN."DOI_TUONG_ID",
                            AO."MA",
                            AO."HO_VA_TEN",
                            A."CHI_TIET_THEO_DOI_TUONG",
                            A."LOAI_DOI_TUONG",
                            A."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG",
                            CASE WHEN A."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG" = TRUE
                                THEN OPN."TK_NGAN_HANG_ID"
                            ELSE NULL
                            END,
                            ROUND(cast(coalesce(OPND."TY_GIA", 0) AS NUMERIC), PHAN_THAP_PHAN_TY_GIA)
                        --Thêm điều kiện having: Chỉ lấy những phát sinh có số tiền nguyên tệ <> 0
                        HAVING SUM(CASE WHEN A."LOAI_DOI_TUONG" = '1'
                                             AND OPND.id IS NOT NULL AND coalesce(OPND."SO_THU_TRUOC_NGUYEN_TE", 0) = 0
                            THEN OPND."SO_CON_PHAI_THU_NGUYEN_TE"
                                   WHEN A."LOAI_DOI_TUONG" = '1'
                                        AND OPND.id IS NULL
                                       THEN OPN."DU_NO_NGUYEN_TE"
                                   WHEN A."LOAI_DOI_TUONG" = '0'
                                        AND OPND.id IS NOT NULL AND coalesce(OPND."SO_THU_TRUOC_NGUYEN_TE", 0) <> 0
                                       THEN coalesce(OPND."SO_THU_TRUOC_NGUYEN_TE", 0)
                                   ELSE 0
                                   END) <> 0
                               OR SUM(CASE WHEN A."LOAI_DOI_TUONG" = '0'
                                                AND OPND.id IS NOT NULL AND coalesce(OPND."SO_THU_TRUOC_NGUYEN_TE", 0) = 0
                            THEN OPND."SO_CON_PHAI_THU_NGUYEN_TE"
                                      WHEN A."LOAI_DOI_TUONG" = '0'
                                           AND OPND.id IS NULL
                                          THEN OPN."DU_CO_NGUYEN_TE"
                                      WHEN A."LOAI_DOI_TUONG" = '1'
                                           AND OPND.id IS NOT NULL AND coalesce(OPND."SO_THU_TRUOC_NGUYEN_TE", 0) <> 0
                                          THEN coalesce(OPND."SO_THU_TRUOC_NGUYEN_TE", 0)
                                      ELSE 0
                                      END) <> 0
                    )
                ;

                UPDATE TMP_SO_CAI GL
                SET "SO_CHUNG_TU" = GL1."SO_CHUNG_TU"
                FROM
                    TMP_SO_CAI GL1
                WHERE GL."ID_CHUNG_TU" = GL1."ID_CHUNG_TU"
                      AND GL."SO_CHUNG_TU" = '#'
                      AND GL1."SO_CHUNG_TU" <> '#'
                ;

                UPDATE TMP_SO_CAI GL1
                SET "DIEN_GIAI_CHUNG" = AO."DIEN_GIAI_CHUNG"
                FROM TMP_SO_CAI GL LEFT JOIN
                    so_cong_no_chi_tiet AO
                        ON
                            GL."ID_CHUNG_TU" = AO."ID_CHUNG_TU" AND GL."MODEL_CHUNG_TU" =
                                                                    AO."MODEL_CHUNG_TU"
                    AND ((GL."SO_HOA_DON" IS NULL AND AO."SO_HOA_DON" IS NULL) OR (GL."SO_HOA_DON"= AO."SO_HOA_DON"))
                --AND coalesce(GL."SO_HOA_DON", '') = coalesce(AO."SO_HOA_DON", '')
                WHERE GL."ID_CHUNG_TU" = GL1."ID_CHUNG_TU" AND GL."MODEL_CHUNG_TU" = GL1."MODEL_CHUNG_TU"
                      AND coalesce(GL."DIEN_GIAI_CHUNG", '') = '' AND GL."LOAI_CHUNG_TU" NOT IN ('612', '613')
                ;

                DROP TABLE IF EXISTS TMP_DEC_TABLE
                ;

                CREATE TEMP TABLE TMP_DEC_TABLE
                    AS
                        SELECT
                            PL."ID_CHUNG_TU"
                            , PL."MODEL_CHUNG_TU"
                            , PL."CHI_TIET_ID"
                            , PL."CHI_TIET_MODEL"
                            , PL."SO_TIEN_TRA_LAI_NGUYEN_TE" + PL."SO_TIEN_GIAM_TRU_NGUYEN_TE" - PL."SO_TIEN_VAT_NGUYEN_TE"
                              + PL."SO_TIEN_CHIET_KHAU_NGUYEN_TE" AS "DEC_SO_TIEN_NGUYEN_TE"
                            , PL."SO_TIEN_TRA_LAI" + PL."SO_TIEN_GIAM_TRU" - PL."SO_TIEN_VAT"
                              + PL."SO_TIEN_CHIET_KHAU"           AS "DEC_SO_TIEN"
                            , PL."CHUNG_TU_MUA_HANG_ID"
                            , PL."CHUNG_TU_MUA_HANG_CHI_TIET_ID"
                        FROM so_mua_hang_chi_tiet AS PL
                            JOIN so_mua_hang_chi_tiet AS PLV
                                ON PL."CHUNG_TU_MUA_HANG_ID" = PLV."ID_CHUNG_TU" AND PLV."MODEL_CHUNG_TU" = 'purchase.document'
                                   AND PL."CHUNG_TU_MUA_HANG_CHI_TIET_ID" = PLV."CHI_TIET_ID" AND
                                   PLV."CHI_TIET_MODEL" = 'purchase.document.line'
                        WHERE PL."CHI_NHANH_ID" = tham_so_chi_nhanh_id
                              AND PL."NGAY_HACH_TOAN" <= tham_so_den_ngay
                              AND PL."currency_id" = tham_so_loai_tien_id
                              AND PL."CHUNG_TU_MUA_HANG_ID" IS NOT NULL
                              AND PL."MA_TK_CO" = PLV."MA_TK_CO"
                ;

                UPDATE TMP_SO_CAI AS GL
                SET "GHI_NO_NGUYEN_TE" = GL."GHI_NO_NGUYEN_TE" - D."DEC_SO_TIEN_NGUYEN_TE",
                    "GHI_NO"           = GL."GHI_NO" - D."DEC_SO_TIEN"
                FROM TMP_DEC_TABLE AS D
                WHERE GL."ID_CHUNG_TU" = D."ID_CHUNG_TU" AND GL."MODEL_CHUNG_TU" = D."MODEL_CHUNG_TU"
                      AND GL."CHI_TIET_ID" = D."CHI_TIET_ID" AND GL."CHI_TIET_MODEL" = D."CHI_TIET_MODEL"
                ;


                UPDATE TMP_SO_CAI AS GL
                SET "GHI_CO_NGUYEN_TE" = "GHI_CO_NGUYEN_TE" - D."DEC_SO_TIEN_NGUYEN_TE",
                    "GHI_CO"           = "GHI_CO" - D."DEC_SO_TIEN"
                FROM
                    (SELECT
                         "CHUNG_TU_MUA_HANG_ID"
                         , "CHUNG_TU_MUA_HANG_CHI_TIET_ID"
                         , SUM("DEC_SO_TIEN_NGUYEN_TE") AS "DEC_SO_TIEN_NGUYEN_TE"
                         , SUM("DEC_SO_TIEN")           AS "DEC_SO_TIEN"
                     FROM TMP_DEC_TABLE
                     GROUP BY "CHUNG_TU_MUA_HANG_ID",
                         "CHUNG_TU_MUA_HANG_CHI_TIET_ID"
                    ) AS D
                WHERE GL."ID_CHUNG_TU" = D."CHUNG_TU_MUA_HANG_ID" AND GL."MODEL_CHUNG_TU" = 'purchase.document'
                      AND GL."CHI_TIET_ID" = D."CHUNG_TU_MUA_HANG_CHI_TIET_ID" AND GL."CHI_TIET_MODEL" = 'purchase.document.line'
                ;


                DROP TABLE IF EXISTS TMP_SALE_DEC_TABLE
                ;

                CREATE TEMP TABLE TMP_SALE_DEC_TABLE
                    AS
                        SELECT
                            SL."ID_CHUNG_TU"
                            , SL."MODEL_CHUNG_TU"
                            , SL."CHI_TIET_ID"
                            , SL."CHI_TIET_MODEL"
                            , SL."SO_TIEN_TRA_LAI_NGUYEN_TE" + SL."SO_TIEN_GIAM_TRU_NGUYEN_TE" - SL."SO_TIEN_VAT_NGUYEN_TE"
                              + SL."SO_TIEN_CHIET_KHAU_NGUYEN_TE" AS "DEC_SO_TIEN_NGUYEN_TE"
                            , SL."SO_TIEN_TRA_LAI" + SL."SO_TIEN_GIAM_TRU" - SL."SO_TIEN_VAT"
                              + SL."SO_TIEN_CHIET_KHAU"           AS "DEC_SO_TIEN"
                            , SL."CHUNG_TU_BAN_HANG_ID"
                            , SL."CHUNG_TU_BAN_HANG_CHI_TIET_ID"
                            , SL."TK_NO_ID"
                            , SL."MA_TK_NO"
                        FROM so_ban_hang_chi_tiet AS SL
                            JOIN so_ban_hang_chi_tiet AS SLV
                                ON SL."CHUNG_TU_BAN_HANG_ID" = SLV."ID_CHUNG_TU" AND SLV."MODEL_CHUNG_TU" = 'sale.document'
                                   AND SL."CHUNG_TU_BAN_HANG_CHI_TIET_ID" = SLV."CHI_TIET_ID" AND
                                   SLV."CHI_TIET_MODEL" = 'sale.document.line'
                        WHERE SL."CHI_NHANH_ID" = tham_so_chi_nhanh_id
                              AND SL."NGAY_HACH_TOAN" <= tham_so_den_ngay
                              AND SL."currency_id" = tham_so_loai_tien_id
                              AND SL."CHUNG_TU_BAN_HANG_ID" IS NOT NULL
                              AND SL."TK_NO_ID" = SLV."TK_NO_ID"
                ;

                UPDATE TMP_SO_CAI AS GL
                SET "GHI_CO_NGUYEN_TE" = "GHI_CO_NGUYEN_TE" - D."DEC_SO_TIEN_NGUYEN_TE",
                    "GHI_CO"           = "GHI_CO" - D."DEC_SO_TIEN"
                FROM TMP_SALE_DEC_TABLE AS D
                WHERE GL."ID_CHUNG_TU" = D."ID_CHUNG_TU" AND GL."MODEL_CHUNG_TU" = D."MODEL_CHUNG_TU"
                      AND GL."CHI_TIET_ID" = D."CHI_TIET_ID" AND GL."CHI_TIET_MODEL" = D."CHI_TIET_MODEL"
                      AND GL."MA_TAI_KHOAN" = D."MA_TK_NO"
                ;

                UPDATE TMP_SO_CAI AS GL
                SET "GHI_NO_NGUYEN_TE" = "GHI_NO_NGUYEN_TE" - D."DEC_SO_TIEN_NGUYEN_TE",
                    "GHI_CO"           = "GHI_CO" - D."DEC_SO_TIEN"
                FROM
                    (SELECT
                         "CHUNG_TU_BAN_HANG_ID"
                         , "CHUNG_TU_BAN_HANG_CHI_TIET_ID"
                         , "MA_TK_NO"
                         , SUM("DEC_SO_TIEN_NGUYEN_TE") AS "DEC_SO_TIEN_NGUYEN_TE"
                         , SUM("DEC_SO_TIEN")           AS "DEC_SO_TIEN"
                     FROM TMP_SALE_DEC_TABLE
                     GROUP BY "CHUNG_TU_BAN_HANG_ID",
                         "CHUNG_TU_BAN_HANG_CHI_TIET_ID",
                         "MA_TK_NO"
                    ) AS D
                WHERE GL."ID_CHUNG_TU" = D."CHUNG_TU_BAN_HANG_ID" AND GL."MODEL_CHUNG_TU" = 'sale.document'
                      AND GL."CHI_TIET_ID" = D."CHUNG_TU_BAN_HANG_CHI_TIET_ID" AND GL."CHI_TIET_MODEL" = 'sale.document.line'
                      AND GL."MA_TAI_KHOAN" = D."MA_TK_NO"
                ;


                UPDATE TMP_SO_CAI
                SET "LA_CHUNG_TU_GHI_NO" = CASE WHEN ("CHI_TIET_THEO_DOI_TUONG" = TRUE
                                                      AND "LOAI_DOI_TUONG" = '1'
                                                      AND ("GHI_NO_NGUYEN_TE" <> 0
                                                           -- kdchien 15/07/2015:61261:Đánh giá lại ngoại tệ lần 2 thì chương trình chưa cộng, trừ các chênh lệch của chứng từ trước
                                                           OR "GHI_NO" <>
                                                              0        -- btanh 16.03.2016 danh giá lần 2 thì số nguyên tệ = 0, số quy đổi âm thì isDebtVoucher vẫn phải = 1 để khi insert vào bảng #GeneralLedger1 không bị tách thành 2 dòng
                                                      )
                                                     )
                                                     OR ("CHI_TIET_THEO_DOI_TUONG" = TRUE
                                                         AND "LOAI_DOI_TUONG" = '0'
                                                         AND ("GHI_CO_NGUYEN_TE" <> 0
                                                              OR "GHI_CO" <> 0
                                                         )
                                                     )
                    THEN 1
                                           ELSE NULL
                                           END
                ;

                UPDATE TMP_SO_CAI
                SET "LA_CHUNG_TU_GHI_NO" = B."LA_CHUNG_TU_GHI_NO"
                FROM TMP_SO_CAI A
                    INNER JOIN TMP_SO_CAI B ON A."ID_CHUNG_TU" = B."ID_CHUNG_TU"
                                               AND A."DOI_TUONG_ID" = B."DOI_TUONG_ID"
                                               AND A."MA_TAI_KHOAN" = B."MA_TAI_KHOAN"
                                               AND coalesce(A."SO_HOA_DON", '') = coalesce(B."SO_HOA_DON", '')
                                               AND ((A."NGAY_HOA_DON" IS NULL AND B."NGAY_HOA_DON" IS NULL) OR
                                                    (A."NGAY_HOA_DON" = B."NGAY_HOA_DON"))
                WHERE A."LA_CHUNG_TU_GHI_NO" IS NULL AND B."LA_CHUNG_TU_GHI_NO" IS NOT NULL
                ;

                DROP TABLE IF EXISTS TMP_SO_CAI_1
                ;

                CREATE TEMP TABLE TMP_SO_CAI_1
                    AS
                        SELECT
                            "ID_CHUNG_TU"
                            , "LA_CHUNG_TU_GHI_NO"
                            , "LOAI_CHUNG_TU"
                            , CAST(MIN("NGAY_CHUNG_TU") AS DATE)      AS "NGAY_CHUNG_TU"
                            , CAST(MIN("NGAY_HACH_TOAN") AS DATE)     AS "NGAY_HACH_TOAN"
                            , CAST(MIN("SO_CHUNG_TU") AS VARCHAR(25)) AS "SO_CHUNG_TU"
                            , coalesce("SO_HOA_DON", '')              AS "SO_HOA_DON"
                            , "NGAY_HOA_DON"
                            , 1                                       AS "CHI_TIET_THEO_HOA_DON"
                            , "DIEN_GIAI_CHUNG"
                            , "MA_TAI_KHOAN"
                            , "TAI_KHOAN_ID"
                            , "TINH_CHAT_TAI_KHOAN"
                            , "DOI_TUONG_ID"
                            , "MA_DOI_TUONG"
                            , "TEN_DOI_TUONG"
                            , "CHI_TIET_THEO_DOI_TUONG"
                            , "LOAI_DOI_TUONG"
                            , "CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG"
                            , "TK_NGAN_HANG_ID"
                            , MAX("TY_GIA")                           AS "TY_GIA"
                            , SUM("GHI_NO_NGUYEN_TE")                 AS "GHI_NO_NGUYEN_TE"
                            , SUM("GHI_NO")                           AS "GHI_NO"
                            , SUM("GHI_CO_NGUYEN_TE")                 AS "GHI_CO_NGUYEN_TE"
                            , SUM("GHI_CO")                           AS "GHI_CO"
                            , "MODEL_CHUNG_TU"
                        FROM TMP_SO_CAI A
                        WHERE "LOAI_CHUNG_TU" IN
                              ('612', '613', '352', '357', '358', '359', '360', '362', '363', '364', '365', '366', '368', '369', '370', '371', '372', '374', '375', '376', '377', '378', '330', '331', '332', '333', '334')
                        GROUP BY
                            "ID_CHUNG_TU",
                            "LA_CHUNG_TU_GHI_NO",
                            "LOAI_CHUNG_TU",
                            coalesce("SO_HOA_DON", ''),
                            "NGAY_HOA_DON",
                            "DIEN_GIAI_CHUNG",
                            "MA_TAI_KHOAN",
                            "TAI_KHOAN_ID",
                            "TINH_CHAT_TAI_KHOAN",
                            "DOI_TUONG_ID",
                            "MA_DOI_TUONG",
                            "TEN_DOI_TUONG",
                            "CHI_TIET_THEO_DOI_TUONG",
                            "LOAI_DOI_TUONG",
                            "CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG",
                            "TK_NGAN_HANG_ID",
                            "MODEL_CHUNG_TU"
                        HAVING SUM("GHI_NO_NGUYEN_TE") <> 0
                               OR SUM("GHI_NO") <> 0
                               OR SUM("GHI_CO_NGUYEN_TE") <> 0
                               OR SUM("GHI_CO") <> 0
                        UNION ALL
                        SELECT
                            "ID_CHUNG_TU"
                            , "LA_CHUNG_TU_GHI_NO"
                            , "LOAI_CHUNG_TU"
                            , CAST(MIN("NGAY_CHUNG_TU") AS DATE)      AS "NGAY_CHUNG_TU"
                            , CAST(MIN("NGAY_HACH_TOAN") AS DATE)     AS "NGAY_HACH_TOAN"
                            , CAST(MIN("SO_CHUNG_TU") AS VARCHAR(25)) AS "SO_CHUNG_TU"
                            , MIN(coalesce("SO_HOA_DON", ''))         AS "SO_HOA_DON"
                            , MIN("NGAY_HOA_DON")                     AS "NGAY_HOA_DON"
                            , 0                                       AS "CHI_TIET_THEO_HOA_DON"
                            , "DIEN_GIAI_CHUNG"
                            , "MA_TAI_KHOAN"
                            , "TAI_KHOAN_ID"
                            , "TINH_CHAT_TAI_KHOAN"
                            , "DOI_TUONG_ID"
                            , "MA_DOI_TUONG"
                            , "TEN_DOI_TUONG"
                            , "CHI_TIET_THEO_DOI_TUONG"
                            , "LOAI_DOI_TUONG"
                            , "CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG"
                            , "TK_NGAN_HANG_ID"
                            , MAX("TY_GIA")                           AS "TY_GIA"
                            , SUM("GHI_NO_NGUYEN_TE")                 AS "GHI_NO_NGUYEN_TE"
                            , SUM("GHI_NO")                           AS "GHI_NO"
                            , SUM("GHI_CO_NGUYEN_TE")                 AS "GHI_CO_NGUYEN_TE"
                            , SUM("GHI_CO")                           AS "GHI_CO"
                            , "MODEL_CHUNG_TU"
                        FROM TMP_SO_CAI
                        WHERE "LOAI_CHUNG_TU" NOT IN
                              ('612', '613', '352', '357', '358', '359', '360', '362', '363', '364', '365', '366', '368', '369', '370', '371', '372', '374', '375', '376', '377', '378', '330', '331', '332', '333', '334')
                        GROUP BY
                            "ID_CHUNG_TU",
                            "LA_CHUNG_TU_GHI_NO",
                            "LOAI_CHUNG_TU",
                            "DIEN_GIAI_CHUNG",
                            "MA_TAI_KHOAN",
                            "TAI_KHOAN_ID",
                            "TINH_CHAT_TAI_KHOAN",
                            "DOI_TUONG_ID",
                            "MA_DOI_TUONG",
                            "TEN_DOI_TUONG",
                            "CHI_TIET_THEO_DOI_TUONG",
                            "LOAI_DOI_TUONG",
                            "CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG",
                            "TK_NGAN_HANG_ID"
                            , "MODEL_CHUNG_TU"
                        HAVING SUM("GHI_NO_NGUYEN_TE") <> 0
                               OR SUM("GHI_NO") <> 0
                               OR SUM("GHI_CO_NGUYEN_TE") <> 0
                               OR SUM("GHI_CO") <> 0
                ;

                DROP TABLE IF EXISTS TMP_BALANCE
                ;

                CREATE TEMP TABLE TMP_BALANCE
                    AS
                        SELECT
                            B."ID_CHUNG_TU"
                            , B."LA_CHUNG_TU_GHI_NO"
                            , B."LOAI_CHUNG_TU"
                            , B."NGAY_CHUNG_TU"
                            , B."NGAY_HACH_TOAN"
                            , B."SO_CHUNG_TU"
                            , B."SO_HOA_DON"
                            , B."NGAY_HOA_DON"
                            , B."DIEN_GIAI_CHUNG"
                            , B."TAI_KHOAN_ID"
                            , B."MA_TAI_KHOAN"
                            , B."TINH_CHAT_TAI_KHOAN"
                            , B."DOI_TUONG_ID"
                            , B."MA_DOI_TUONG"
                            , B."TEN_DOI_TUONG"
                            , B."CHI_TIET_THEO_DOI_TUONG"
                            , B."LOAI_DOI_TUONG"
                            , B."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG"
                            , B."TK_NGAN_HANG_ID"
                            , B."TY_GIA"
                            , B."GHI_NO_NGUYEN_TE" - (CASE WHEN B."LOAI_DOI_TUONG" = '1'
                            THEN coalesce(SUM(GD."SO_TIEN_CONG_NO"), 0)
                                                      ELSE coalesce(SUM(GP."SO_TIEN_THANH_TOAN"), 0) END)      AS "GHI_NO_NGUYEN_TE"
                            , B."GHI_NO" - (CASE WHEN B."LOAI_DOI_TUONG" = '1'
                            THEN coalesce(SUM(GD."SO_TIEN_CONG_NO"), 0)
                                            ELSE coalesce(SUM(GP."SO_TIEN_THANH_TOAN"), 0) -
                                                 coalesce(SUM(GP."CHENH_LECH_TY_GIA_SO_TIEN_QUY_DOI"), 0) END) AS "GHI_NO"
                            ,
                            /*Edited by ntlieu 04/11/2015 sửa bug 76210: Với chứng từ thanh toán hiển thị bên tab chứng từ khi còn số quy đổi thì không trừ đi chênh lệch tỷ giá*/
                              B."GHI_NO" - (CASE WHEN B."LOAI_DOI_TUONG" = '1'
                                  THEN coalesce(SUM(GD."SO_TIEN_CONG_NO_QUY_DOI"), 0)
                                            ELSE coalesce(SUM(GP."SO_TIEN_THANH_TOAN_QUY_DOI"), 0) END)           "GHI_NO_CUA_CHUNG_TU"

                            , B."GHI_CO_NGUYEN_TE" - (CASE WHEN B."LOAI_DOI_TUONG" = '1'
                            THEN coalesce(SUM(GP."SO_TIEN_THANH_TOAN"), 0)
                                                      ELSE coalesce(SUM(GD."SO_TIEN_CONG_NO"), 0) END)         AS "GHI_CO_NGUYEN_TE"
                            ,
                            -- ntquang 25/10/2017 : sửa bug 151164 - thay GD.ExchangeDiffAmount = GP.ExchangeDiffAmount và chuyển thành coalesce(SUM(GP.PayAmount),0) -  coalesce(SUM(GP.ExchangeDiffAmount),0) thay cho
                            -- coalesce(SUM(GD.DebtAmount),0)-  coalesce(SUM(GP.ExchangeDiffAmount),0) để lấy được chênh lệch tỉ giá từ các chứng từ thanh toán
                              B."GHI_CO" - (CASE WHEN B."LOAI_DOI_TUONG" = '1'
                                  THEN coalesce(SUM(GP."SO_TIEN_THANH_TOAN_QUY_DOI"), 0) -
                                       coalesce(SUM(GP."CHENH_LECH_TY_GIA_SO_TIEN_QUY_DOI"), 0)
                                            ELSE coalesce(SUM(GD."SO_TIEN_CONG_NO_QUY_DOI"), 0) END)           AS "GHI_CO"
                            ,
                            /*Edited by ntlieu 04/11/2015 sửa bug 76210: Với chứng từ thanh toán hiển thị bên tab chứng từ khi còn số quy đổi thì không trừ đi chênh lệch tỷ giá*/
                              B."GHI_CO" - (CASE WHEN B."LOAI_DOI_TUONG" = '1'
                                  THEN coalesce(SUM(GP."SO_TIEN_THANH_TOAN_QUY_DOI"), 0)
                                            ELSE coalesce(SUM(GD."SO_TIEN_CONG_NO_QUY_DOI"),
                                                          0) END)                                              AS "GHI_CO_CUA_CHUNG_TU"
                            , "MODEL_CHUNG_TU"
                        FROM TMP_SO_CAI_1 AS B
                            LEFT JOIN sale_ex_doi_tru_chi_tiet AS GD ON B."TAI_KHOAN_ID" = GD."TAI_KHOAN_ID"
                                                                        AND
                                                                        B."ID_CHUNG_TU" = cast(GD."ID_CHUNG_TU_CONG_NO" AS INTEGER)
                                                                        AND
                                                                        ((B."LOAI_DOI_TUONG" = '1' AND B."GHI_NO_NGUYEN_TE" > 0) OR
                                                                         (B."LOAI_DOI_TUONG" = '0' AND B."GHI_CO_NGUYEN_TE" > 0))
                                                                        AND B."DOI_TUONG_ID" = GD."DOI_TUONG_ID"
                                                                        AND (B."CHI_TIET_THEO_HOA_DON" = 0
                                                                             OR
                                                                             (coalesce(B."SO_HOA_DON", '') =
                                                                              coalesce(GD."SO_HOA_DON_CONG_NO", '')
                                                                              AND
                                                                              ((B."NGAY_HOA_DON" = GD."NGAY_CHUNG_TU_CONG_NO") OR
                                                                               (B."NGAY_HOA_DON" IS NULL AND
                                                                                GD."NGAY_CHUNG_TU_CONG_NO" IS NULL))
                                                                             )
                                                                        )
                                                                        AND GD."CTCN_DA_GHI_SO" = TRUE
                            LEFT JOIN sale_ex_doi_tru_chi_tiet AS GP ON B."TAI_KHOAN_ID" = GP."TAI_KHOAN_ID"
                                                                        AND B."ID_CHUNG_TU" =
                                                                            cast(GP."ID_CHUNG_TU_THANH_TOAN" AS INTEGER)
                                                                        AND
                                                                        ((B."LOAI_DOI_TUONG" = '1' AND B."GHI_CO_NGUYEN_TE" > '0')
                                                                         OR
                                                                         (B."LOAI_DOI_TUONG" = '0' AND B."GHI_NO_NGUYEN_TE" > 0))
                                                                        AND B."DOI_TUONG_ID" = GP."DOI_TUONG_ID"
                                                                        /*KDCHIEN 17/01/2017:31306:Với thanh toán phải có IsDebtVoucher <> 1
                                                                        14/02/2017: Rollback*/
                                                                        AND ((B."LOAI_CHUNG_TU" IN
                                                                              ('611', '612', '613', '614', '615', '616', '630') AND
                                                                              B."SO_CHUNG_TU" = GP."SO_CHUNG_TU_THANH_TOAN" AND
                                                                              B."NGAY_CHUNG_TU" = GP."NGAY_CHUNG_TU_THANH_TOAN")
                                                                             OR (B."LOAI_CHUNG_TU" NOT IN
                                                                                 ('611', '612', '613', '614', '615', '616', '630'))
                                                                        )
                                                                        AND GP."CTTT_DA_GHI_SO" = TRUE

                        GROUP BY B."ID_CHUNG_TU",
                            B."LA_CHUNG_TU_GHI_NO",
                            B."LOAI_CHUNG_TU",
                            B."NGAY_CHUNG_TU",
                            B."NGAY_HACH_TOAN",
                            B."SO_CHUNG_TU",
                            B."SO_HOA_DON",
                            B."NGAY_HOA_DON",
                            B."DIEN_GIAI_CHUNG",
                            B."TAI_KHOAN_ID",
                            B."MA_TAI_KHOAN",
                            B."TINH_CHAT_TAI_KHOAN",
                            B."DOI_TUONG_ID",
                            B."MA_DOI_TUONG",
                            B."TEN_DOI_TUONG",
                            B."CHI_TIET_THEO_DOI_TUONG",
                            B."LOAI_DOI_TUONG",
                            B."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG",
                            B."TK_NGAN_HANG_ID",
                            B."TY_GIA",
                            B."GHI_NO_NGUYEN_TE",
                            B."GHI_NO",
                            B."GHI_CO_NGUYEN_TE",
                            B."GHI_CO"
                            , B."MODEL_CHUNG_TU"
                        HAVING (B."GHI_NO_NGUYEN_TE"
                                + SUM(-coalesce(CASE WHEN B."LOAI_DOI_TUONG" = '1'
                            THEN GD."SO_TIEN_CONG_NO"
                                                ELSE 0
                                                END, 0)
                                      - coalesce(CASE WHEN B."LOAI_DOI_TUONG" = '0'
                            THEN GP."SO_TIEN_THANH_TOAN"
                                                 ELSE 0
                                                 END, 0)) <> 0)
                               OR (B."GHI_NO"
                                   + SUM(-coalesce(CASE WHEN B."LOAI_DOI_TUONG" = '1'
                            THEN GD."SO_TIEN_CONG_NO_QUY_DOI"
                                                   ELSE 0
                                                   END, 0)
                                         - coalesce(CASE WHEN B."LOAI_DOI_TUONG" = '0'
                            THEN GP."SO_TIEN_THANH_TOAN" - GP."CHENH_LECH_TY_GIA_SO_TIEN_QUY_DOI"
                                                    ELSE 0
                                                    END, 0)) <> 0)
                               OR (B."GHI_CO_NGUYEN_TE"
                                   + SUM(-coalesce(CASE WHEN B."LOAI_DOI_TUONG" = '0'
                            THEN GD."SO_TIEN_CONG_NO"
                                                   ELSE 0
                                                   END, 0)
                                         - coalesce(CASE WHEN B."LOAI_DOI_TUONG" = '1'
                            THEN GP."SO_TIEN_THANH_TOAN"
                                                    ELSE 0
                                                    END, 0)) <> 0)
                               OR (B."GHI_CO"
                                   + SUM(-coalesce(CASE WHEN B."LOAI_DOI_TUONG" = '0'
                            THEN GD."SO_TIEN_CONG_NO_QUY_DOI"
                                                   ELSE 0
                                                   END, 0)
                                         - coalesce(CASE WHEN B."LOAI_DOI_TUONG" = '1'
                            THEN GP."SO_TIEN_THANH_TOAN" - GP."CHENH_LECH_TY_GIA_SO_TIEN_QUY_DOI"
                                                    ELSE 0
                                                    END, 0)) <> 0)
                ;


                DROP TABLE IF EXISTS TMP_TABLE_0
                ;

                CREATE TEMP TABLE TMP_TABLE_0
                    AS
                        SELECT
                            B."MA_TAI_KHOAN"
                            , B."TAI_KHOAN_ID"
                            , B."TINH_CHAT_TAI_KHOAN"
                            , B."CHI_TIET_THEO_DOI_TUONG"
                            , B."LOAI_DOI_TUONG"
                            , B."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG"
                            , CASE WHEN B."CHI_TIET_THEO_DOI_TUONG" = TRUE
                            THEN B."DOI_TUONG_ID"
                              ELSE NULL
                              END                                          AS "DOI_TUONG_ID"
                            , CASE WHEN B."CHI_TIET_THEO_DOI_TUONG" = TRUE
                            THEN B."MA_DOI_TUONG"
                              ELSE NULL
                              END                                          AS "MA_DOI_TUONG"
                            , CASE WHEN B."CHI_TIET_THEO_DOI_TUONG" = TRUE
                            THEN B."TEN_DOI_TUONG"
                              ELSE NULL
                              END                                          AS "TEN_DOI_TUONG"
                            , B."TK_NGAN_HANG_ID"
                            , SUM("GHI_NO_NGUYEN_TE" - "GHI_CO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
                            , SUM("GHI_NO" - "GHI_CO")                     AS "GHI_NO"
                            , CAST(0 AS FLOAT)                             AS "GHI_CO_NGUYEN_TE"
                            , CAST(0 AS FLOAT)                             AS "GHI_CO"
                        FROM TMP_BALANCE AS B
                        GROUP BY B."MA_TAI_KHOAN",
                            B."TAI_KHOAN_ID",
                            B."TINH_CHAT_TAI_KHOAN",
                            B."CHI_TIET_THEO_DOI_TUONG",
                            B."LOAI_DOI_TUONG",
                            B."CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG",
                            CASE WHEN B."CHI_TIET_THEO_DOI_TUONG" = TRUE
                                THEN B."DOI_TUONG_ID"
                            ELSE NULL
                            END,
                            CASE WHEN B."CHI_TIET_THEO_DOI_TUONG" = TRUE
                                THEN B."MA_DOI_TUONG"
                            ELSE NULL
                            END,
                            CASE WHEN B."CHI_TIET_THEO_DOI_TUONG" = TRUE
                                THEN B."TEN_DOI_TUONG"
                            ELSE NULL
                            END,
                            B."TK_NGAN_HANG_ID"
                ;

                UPDATE TMP_TABLE_0
                SET "GHI_CO_NGUYEN_TE" = -"GHI_NO_NGUYEN_TE",
                    "GHI_NO_NGUYEN_TE" = 0
                WHERE "TINH_CHAT_TAI_KHOAN" = '1'
                      OR ("TINH_CHAT_TAI_KHOAN" IN ('2', '3')
                          AND "GHI_NO_NGUYEN_TE" < 0
                      )
                ;

                UPDATE TMP_TABLE_0
                SET "GHI_CO" = -"GHI_NO",
                    "GHI_NO" = 0
                WHERE "TINH_CHAT_TAI_KHOAN" = '1'
                      OR ("TINH_CHAT_TAI_KHOAN" IN ('2', '3')
                          AND "GHI_CO_NGUYEN_TE" > 0
                      )
                ;

                ----Lấy ra ết quaả choab 1ts
                DROP TABLE IF EXISTS TMP_TABLE_1
                ;

                CREATE TEMP TABLE TMP_TABLE_1
                    AS
                        SELECT
                              row_number()
                              OVER (
                                  PARTITION BY TRUE :: BOOLEAN ) AS "ID_CHUNG_TU"
                            , row_number()
                              OVER (
                                  PARTITION BY TRUE :: BOOLEAN ) AS "CHI_TIET_ID"
                            , T."TAI_KHOAN_ID"
                            , T."MA_TAI_KHOAN"
                            , T."DOI_TUONG_ID"
                            , AO."MA"                            AS "MA_DOI_TUONG"
                            , AO."HO_VA_TEN"                     AS "TEN_DOI_TUONG"
                            , T."TK_NGAN_HANG_ID"
                            , BA."SO_TAI_KHOAN"                  AS "SO_TAI_KHOAN_NGAN_HANG"
                            , CASE
                              --Nếu tài khoản chi tiết theo nhà cung cấp HOẶC tài khoản có số dư Nợ < 0 thì đặt = 0
                              WHEN (T."CHI_TIET_THEO_DOI_TUONG" = TRUE
                                    AND T."LOAI_DOI_TUONG" = '0'
                                   )
                                   OR ("TINH_CHAT_TAI_KHOAN" = '0'
                                       AND T."GHI_NO_NGUYEN_TE" < 0
                                   )
                                  THEN 0
                              ELSE T."GHI_NO_NGUYEN_TE"
                              END                                AS "SO_TIEN_DU_NO"
                            , CASE WHEN (T."CHI_TIET_THEO_DOI_TUONG" = TRUE
                                         AND T."LOAI_DOI_TUONG" = '0'
                                        )
                                        OR ("TINH_CHAT_TAI_KHOAN" = '0'
                                            AND T."GHI_NO_NGUYEN_TE" < 0
                                        )
                            THEN 0
                              ELSE T."GHI_NO"
                              END                                AS "SO_TIEN_QUY_DOI_DU_NO"
                            , CASE WHEN (T."CHI_TIET_THEO_DOI_TUONG" = TRUE
                                         AND T."LOAI_DOI_TUONG" = '1'
                                        )
                                        OR ("TINH_CHAT_TAI_KHOAN" = '1'
                                            AND T."GHI_CO_NGUYEN_TE" < 0
                                        )
                            THEN 0
                              ELSE T."GHI_CO_NGUYEN_TE"
                              END                                AS "SO_TIEN_DU_CO"
                            , CASE WHEN (T."CHI_TIET_THEO_DOI_TUONG" = TRUE
                                         AND T."LOAI_DOI_TUONG" = '1'
                                        )
                                        OR ("TINH_CHAT_TAI_KHOAN" = '1'
                                            AND T."GHI_CO_NGUYEN_TE" < 0
                                        )
                            THEN 0
                              ELSE T."GHI_CO"
                              END                                AS "SO_TIEN_QUY_DOI_DU_CO"
                            , B."TEN_DAY_DU"                     AS "TEN_NGAN_HANG"
                        FROM TMP_TABLE_0 AS T
                            LEFT JOIN res_partner AS AO ON T."DOI_TUONG_ID" = AO.id
                            LEFT JOIN danh_muc_tai_khoan_ngan_hang AS BA ON T."TK_NGAN_HANG_ID" = BA.id
                            LEFT JOIN danh_muc_ngan_hang AS B ON BA."NGAN_HANG_ID" = B.id
                        WHERE CASE WHEN (T."CHI_TIET_THEO_DOI_TUONG" = TRUE
                                         AND T."LOAI_DOI_TUONG" = '0'
                                        )
                                        OR ("TINH_CHAT_TAI_KHOAN" = '0'
                                            AND T."GHI_NO_NGUYEN_TE" < 0
                                        )
                            THEN 0
                              ELSE T."GHI_NO_NGUYEN_TE"
                              END <> 0
                              OR CASE WHEN (T."CHI_TIET_THEO_DOI_TUONG" = TRUE
                                            AND T."LOAI_DOI_TUONG" = '1'
                                           )
                                           OR ("TINH_CHAT_TAI_KHOAN" = '1'
                                               AND T."GHI_CO_NGUYEN_TE" < 0
                                           )
                            THEN 0
                                 ELSE T."GHI_CO_NGUYEN_TE"
                                 END <> 0
                        ORDER BY T."MA_TAI_KHOAN",
                            coalesce(BA."SO_TAI_KHOAN", ''),
                            coalesce(AO."MA_DOI_TUONG", '')
                ;


                DROP TABLE IF EXISTS TMP_LAST_EXCHANGE_RATE
                ;

                CREATE TEMP TABLE TMP_LAST_EXCHANGE_RATE
                    AS
                        SELECT DISTINCT
                            B."ID_CHUNG_TU"
                            , (SELECT *
                               FROM LAY_TY_GIA_DANH_GIA_LAI_GAN_NHAT(B."ID_CHUNG_TU", B."SO_HOA_DON", B."NGAY_HOA_DON" :: TIMESTAMP,
                                                                     tham_so_chi_nhanh_id)) AS "TY_GIA_DANH_GIA_LAI_GAN_NHAT"
                        FROM TMP_BALANCE AS B
                ;

                ---Lấy ra kết quả cho tab 2--------------------------------------------------
                DROP TABLE IF EXISTS TMP_TABLE_2
                ;

                CREATE TEMP TABLE TMP_TABLE_2
                    AS
                        SELECT
                              row_number()
                              OVER (
                                  PARTITION BY TRUE :: BOOLEAN )             AS "CHI_TIET_ID"
                            , row_number()
                              OVER (
                                  PARTITION BY TRUE :: BOOLEAN )             AS "ID_CHUNG_TU"
                            , B."ID_CHUNG_TU"                                AS "CHUNG_TU_ID"
                            , B."LA_CHUNG_TU_GHI_NO"
                            , B."LOAI_CHUNG_TU"
                            , T."REFTYPENAME"                                AS "TEN_LOAI_CHUNG_TU"
                            , B."NGAY_CHUNG_TU"
                            , B."NGAY_HACH_TOAN"
                            , B."SO_HOA_DON"
                            , B."SO_CHUNG_TU"
                            , B."NGAY_HOA_DON"
                            , B."DIEN_GIAI_CHUNG"
                            , B."MA_TAI_KHOAN"
                            , B."TAI_KHOAN_ID"
                            , B."LOAI_DOI_TUONG"
                            , B."DOI_TUONG_ID"
                            , AO."MA" AS "MA_DOI_TUONG"
                            , B."TK_NGAN_HANG_ID"
                            , coalesce(B."TY_GIA", 0)                        AS "TY_GIA"
                            , coalesce(LE."TY_GIA_DANH_GIA_LAI_GAN_NHAT", 0) AS "TY_GIA_DANH_GIA_LAI_GAN_NHAT"
                            ,
                            /*Sửa bug 77930: Khi TK chi tiết theo KH thì lấy Nợ - Có, TK chi tiết theo NCC thì lấy Có - Nợ. Xem lại bug 70492*/

                              coalesce(SUM(CASE WHEN B."LOAI_DOI_TUONG" = '1'
                                  THEN B."GHI_NO_NGUYEN_TE" - B."GHI_CO_NGUYEN_TE"
                                           WHEN B."LOAI_DOI_TUONG" = '0'
                                               THEN B."GHI_CO_NGUYEN_TE" - B."GHI_NO_NGUYEN_TE"
                                           ELSE 0
                                           END), 0)                          AS "SO_CHUA_DOI_TRU"

                            , coalesce(SUM(CASE WHEN B."LOAI_DOI_TUONG" = '1'
                            THEN B."GHI_NO_CUA_CHUNG_TU" - B."GHI_CO_CUA_CHUNG_TU"
                                           WHEN B."LOAI_DOI_TUONG" = '0'
                                               THEN B."GHI_CO_CUA_CHUNG_TU" - B."GHI_NO_CUA_CHUNG_TU"
                                           ELSE 0
                                           END), 0)                          AS "SO_CHUA_DOI_TRU_QUY_DOI"

                            , 0                                              AS "DANH_GIA_LAI"
                            , 0                                              AS "CHENH_LECH"
                            , "MODEL_CHUNG_TU"
                        FROM TMP_BALANCE AS B
                            INNER JOIN danh_muc_reftype AS T ON B."LOAI_CHUNG_TU" = cast(T."REFTYPE" AS VARCHAR(20))
                            LEFT JOIN TMP_LAST_EXCHANGE_RATE AS LE ON B."ID_CHUNG_TU" = LE."ID_CHUNG_TU"
                            LEFT JOIN res_partner AS AO ON B."DOI_TUONG_ID" = AO.id
                        WHERE B."CHI_TIET_THEO_DOI_TUONG" = TRUE
                              AND B."LOAI_DOI_TUONG" IN ('0', '1') --KH, NCC
                        GROUP BY B."ID_CHUNG_TU",
                            B."LA_CHUNG_TU_GHI_NO",
                            B."LOAI_CHUNG_TU",
                            T."REFTYPENAME",
                            B."NGAY_CHUNG_TU",
                            B."NGAY_HACH_TOAN",
                            B."SO_CHUNG_TU",
                            B."SO_HOA_DON",
                            B."NGAY_HOA_DON",
                            B."DIEN_GIAI_CHUNG",
                            B."MA_TAI_KHOAN",
                            B."TAI_KHOAN_ID",
                            B."LOAI_DOI_TUONG",
                            B."DOI_TUONG_ID",
                            AO."MA",
                            B."TK_NGAN_HANG_ID",
                            B."TY_GIA",
                            LE."TY_GIA_DANH_GIA_LAI_GAN_NHAT"
                            , "MODEL_CHUNG_TU"

                        HAVING coalesce(SUM(CASE WHEN B."LOAI_DOI_TUONG" = '1'
                            THEN B."GHI_NO_NGUYEN_TE" - B."GHI_CO_NGUYEN_TE"
                                            WHEN B."LOAI_DOI_TUONG" = '0'
                                                THEN B."GHI_CO_NGUYEN_TE" - B."GHI_NO_NGUYEN_TE"
                                            ELSE 0
                                            END), 0) <> 0
                ;

                DELETE FROM TMP_TABLE_2
                WHERE concat("MA_TAI_KHOAN", CAST("DOI_TUONG_ID" AS VARCHAR(20))) NOT IN (
                    SELECT concat("MA_TAI_KHOAN", CAST("DOI_TUONG_ID" AS VARCHAR(20)))
                    FROM TMP_TABLE_1
                    WHERE "DOI_TUONG_ID" IS NOT NULL)
                ;

            END $$
            ;

				"""+query_dk+"""
		 		"""
				
		record = self.execute(query, params)
		
		return record

	
	
	@api.model_cr
	def init(self):
		self.env.cr.execute(""" 
			




DROP FUNCTION  IF EXISTS LAY_TY_GIA_DANH_GIA_LAI_GAN_NHAT(id_chung_tu integer, so_hoa_don VARCHAR, ngay_hoa_don TIMESTAMP, chi_nhanh_id integer);
CREATE OR REPLACE FUNCTION LAY_TY_GIA_DANH_GIA_LAI_GAN_NHAT(id_chung_tu integer, so_hoa_don VARCHAR, ngay_hoa_don TIMESTAMP, chi_nhanh_id integer)
				RETURNS FLOAT
				LANGUAGE plpgsql
				AS $$
				DECLARE
                        CHE_DO_KE_TOAN VARCHAR(20);
                        ty_gia_gan_nhat FLOAT:=NULL ;
                        BEGIN

                        SELECT value INTO CHE_DO_KE_TOAN FROM ir_config_parameter
                        WHERE key='he_thong.CHE_DO_KE_TOAN'FETCH FIRST 1 ROW ONLY;


                        IF CHE_DO_KE_TOAN = '15'
                        THEN
                        SELECT coalesce (VF."TY_GIA",VD."TY_GIA_DANH_GIA_LAI")
                                INTO ty_gia_gan_nhat
                        FROM account_ex_chung_tu_nghiep_vu_khac AS V
                        LEFT JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan AS VD ON V.id = VD."CHUNG_TU_NGHIEP_VU_KHAC_ID"
                        LEFT JOIN TONG_HOP_CHUNG_TU_NGHIEP_VU_KHAC_SO_DU_NGOAI_TE AS VF ON VD."CHUNG_TU_NGHIEP_VU_KHAC_ID" = VF."CHUNG_TU_NGHIEP_VU_KHAC_ID"
                        AND coalesce(VD."TK_CONG_NO_ID",0)= coalesce(VF."TAI_KHOAN_ID",0)
                        AND coalesce(VD."DOI_TUONG_ID",0) = coalesce(VF."DOI_TUONG_ID",0)
                        WHERE   V."CHI_NHANH_ID" = chi_nhanh_id
                                AND VD."ID_CHUNG_TU_GOC" = id_chung_tu
                                AND ( (  VD."SO_HOA_DON" = so_hoa_don
                                                AND  VD."NGAY_HOA_DON" = ngay_hoa_don
                                                AND  VD."LOAI_CHUNG_TU" = '612'
                                            )
                                           OR  VD."LOAI_CHUNG_TU" <> '612'
                                )
                        ORDER BY V."NGAY_HACH_TOAN" DESC
                        FETCH FIRST 1 ROW ONLY
                        ;

                        ELSE

                        SELECT V."TY_GIA" INTO ty_gia_gan_nhat
                        FROM account_ex_chung_tu_nghiep_vu_khac AS V
                        INNER JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan AS VD ON V.id = VD."CHUNG_TU_NGHIEP_VU_KHAC_ID"
                        WHERE   V."CHI_NHANH_ID" = chi_nhanh_id
                                                AND VD."ID_CHUNG_TU_GOC" = id_chung_tu
                                                AND ( (  VD."NGAY_HOA_DON" = ngay_hoa_don
                                                                AND  VD."SO_HOA_DON" = so_hoa_don
                                                                AND  VD."LOAI_CHUNG_TU" = '612'
                                                            )
                                                            OR  VD."LOAI_CHUNG_TU" <> '612'
                                                )
                        ORDER BY V."NGAY_HACH_TOAN" DESC;

                        END IF;

                        RETURN ty_gia_gan_nhat;
                        END;
						$$;




		""")