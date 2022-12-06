# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
import json

class SALE_EX_DOI_TRU_CHUNG_TU_NHIEU_DOI_TUONG(models.Model):
	_name = 'sale.ex.doi.tru.chung.tu.nhieu.doi.tuong'
	_description = ''
	_auto = False
	TAI_KHOAN_PHAI_THU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản phải thu', help='Tài khoản phải thu')
	NGAY_DOI_TRU = fields.Date(string='Ngày đối trừ', help='Ngày đối trừ',default=fields.Datetime.now)
	currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
	name = fields.Char(string='Name', help='Name', oldname='NAME')
	LAY_DU_LIEU_JSON = fields.Text()
	JSON_DOI_TRU = fields.Text()

	IS_TY_GIA = fields.Boolean(string='Loại tiền', help='Loại tiền',default=True)
	STEP = fields.Integer(string='bước', help='bước',store=False)
	
	SALE_EX_DOI_TRU_CHUNG_TU_NHIEU_DOI_TUONG_CHI_TIET_IDS = fields.One2many('sale.ex.doi.tru.chung.tu.nhieu.doi.tuong.chi.tiet', 'DOI_TRU_CHUNG_TU_NHIEU_DOI_TUONG_CHI_TIET_ID', string='Đối trừ chứng từ nhiều đối tượng chi tiết')

	SALE_EX_DOI_TRU_CHUNG_TU_IDS = fields.One2many('sale.ex.doi.tru.chung.tu', 'DOI_TRU_CHUNG_TU_NHIEU_DOI_TUONG_ID', string='Đối trừ chứng từ')


	@api.model
	def default_get(self, fields):
		rec = super(SALE_EX_DOI_TRU_CHUNG_TU_NHIEU_DOI_TUONG, self).default_get(fields)
		loai_tien = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'VND')], limit = 1)
		tai_khoan_phai_thu = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '131')],limit=1)
		if loai_tien:
			rec['currency_id'] = loai_tien.id
		if tai_khoan_phai_thu:
			rec['TAI_KHOAN_PHAI_THU_ID'] = tai_khoan_phai_thu.id
		rec['STEP'] =1

		return rec
	
	@api.onchange('currency_id')
	def update_loai_tien(self):
		if self.currency_id.MA_LOAI_TIEN == 'VND':
			self.IS_TY_GIA = False
		else:
			self.IS_TY_GIA =True

	@api.model
	def thuc_hien_doi_tru(self, args):
		new_line = [[5]]
		if self.SALE_EX_DOI_TRU_CHUNG_TU_NHIEU_DOI_TUONG_CHI_TIET_IDS:
			for line in self.SALE_EX_DOI_TRU_CHUNG_TU_NHIEU_DOI_TUONG_CHI_TIET_IDS:
				# if line.AUTO_SELECT == True:
				chung_tu_thanh_toan = self.SALE_EX_DOI_TRU_CHUNG_TU_IDS.lay_chung_tu_thanh_toan(self.NGAY_DOI_TRU,line.MA_KHACH_HANG_ID.id,self.currency_id.id)
				chung_tu_cong_no = self.SALE_EX_DOI_TRU_CHUNG_TU_IDS.lay_chung_tu_cong_no(self.NGAY_DOI_TRU,line.MA_KHACH_HANG_ID.id,self.currency_id.id)
				arr_chung_tu_thanh_toan = []
				arr_chung_tu_cong_no = []

				for ct_tt in chung_tu_thanh_toan:
					for ct_cn in chung_tu_cong_no:
						ct_cn['SO_TIEN_CON_LAI'] = ct_cn.get('SO_TIEN') - ct_cn.get('SO_TIEN_DOI_TRU')
						#neu con no
						if ct_cn['SO_TIEN_CON_LAI'] > 0:
							#neu thua tien thanh toan                    
							if ct_cn['SO_TIEN_CON_LAI'] <= ct_tt.get('SO_TIEN'):
								ct_cn['CHON'] = 'True'                            
								ct_cn['SO_TIEN_DOI_TRU'] += ct_cn.get('SO_TIEN_CON_LAI')
							#neu tra khong du
							elif ct_cn['SO_TIEN_CON_LAI'] > ct_tt.get('SO_TIEN'):
								ct_cn['CHON'] = 'True'
								ct_cn['SO_TIEN_DOI_TRU'] += ct_tt.get('SO_TIEN')

							#chung tu thanh toan
							ct_tt['CHON'] = 'True'
							ct_tt['SO_TIEN_DOI_TRU'] += ct_cn['SO_TIEN_DOI_TRU']
							if(ct_tt['SO_TIEN_DOI_TRU'] == ct_tt['SO_TIEN']):
								break

				for ct in chung_tu_thanh_toan:
					ten_loai_chung_tu = self.env['danh.muc.reftype'].search([('REFTYPE', '=', ct.get('LOAI_CHUNG_TU'))], limit=1)
					arr_chung_tu_thanh_toan += [(0,0,{
						'NGAY_CHUNG_TU': ct.get('NGAY_CHUNG_TU'),
						'HAN_THANH_TOAN': ct.get('HAN_THANH_TOAN'),
						'SO_CHUNG_TU' : ct.get('SO_CHUNG_TU'),
						'DIEN_GIAI' : ct.get('DIEN_GIAI'),
						'NHAN_VIEN_ID' : ct.get('NHAN_VIEN_ID'),
						'TEN_NHAN_VIEN' : ct.get('TEN_NHAN_VIEN'),
						'SO_TIEN' : ct.get('SO_TIEN'),
						'SO_CHUA_DOI_TRU' : ct.get('SO_TIEN'),
						'SO_TIEN_DOI_TRU' : ct.get('SO_TIEN_DOI_TRU'),
						'TEN_LOAI_CHUNG_TU' : ten_loai_chung_tu.REFTYPENAME,
						'LOAI_CHUNG_TU' : ct.get('LOAI_CHUNG_TU'),
						'CHON' : ct.get('CHON'),
					})]

				for line_cong_no in chung_tu_cong_no:
					ten_loai_ct_cong_no = self.env['danh.muc.reftype'].search([('REFTYPE', '=', line_cong_no.get('LOAI_CHUNG_TU'))], limit=1)
					arr_chung_tu_cong_no += [(0,0,{
						'NGAY_CHUNG_TU': line_cong_no.get('NGAY_CHUNG_TU'),
						'HAN_THANH_TOAN': line_cong_no.get('HAN_THANH_TOAN'),
						'SO_CHUNG_TU' : line_cong_no.get('SO_CHUNG_TU'),
						'DIEN_GIAI' : line_cong_no.get('DIEN_GIAI'),
						'NHAN_VIEN_ID' : line_cong_no.get('NHAN_VIEN_ID'),
						'TEN_NHAN_VIEN' : line_cong_no.get('TEN_NHAN_VIEN'),
						'SO_TIEN' : line_cong_no.get('SO_TIEN'),
						'SO_CON_NO' : line_cong_no.get('SO_TIEN'),
						'SO_TIEN_DOI_TRU' : line_cong_no.get('SO_TIEN_DOI_TRU'),
						'TEN_LOAI_CHUNG_TU' : ten_loai_ct_cong_no.REFTYPENAME,
						'LOAI_CHUNG_TU' : line_cong_no.get('LOAI_CHUNG_TU'),
						'CHON' : line_cong_no.get('CHON'),
					})]

				new_line += [(0,0,{
					'KHACH_HANG_ID': line.MA_KHACH_HANG_ID.id,
					'TEN_KHACH_HANG' : line.MA_KHACH_HANG_ID.HO_VA_TEN,
					'TONG_SO_CHUA_DOI_TRU_TT' : 10,
					'TONG_SO_DOI_TRU_THANH_TOAN' : 10,
					'TONG_SO_CHUA_DOI_TRU_CN' : 10,
					'TONG_SO_DOI_TRU_CONG_NO' : 10,
					'XEM_CHI_TIET' : 'Xem chi tiết',
					'NGAY_DOI_TRU' : self.NGAY_DOI_TRU,
					'currency_id' : self.currency_id.id,
					'SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_IDS' : arr_chung_tu_thanh_toan,
					'SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_IDS' : arr_chung_tu_cong_no,
				})]
			
		return {'SALE_EX_DOI_TRU_CHUNG_TU_IDS': new_line}

	@api.onchange('LAY_DU_LIEU_JSON')
	def _onchange_LAY_DU_LIEU_JSON(self):
		if self.LAY_DU_LIEU_JSON:
			param = json.loads(self.LAY_DU_LIEU_JSON)
			if param:
				du_lieu = self.lay_thong_tin_doi_tru(param.get('NGAY'),param.get('currency_id'))
				if du_lieu:
					env_doi_tru_ct = self.env['sale.ex.doi.tru.chung.tu.nhieu.doi.tuong.chi.tiet']
					self.SALE_EX_DOI_TRU_CHUNG_TU_NHIEU_DOI_TUONG_CHI_TIET_IDS = []
					for ct in du_lieu:
						new_line = env_doi_tru_ct.new({
							'MA_KHACH_HANG_ID': ct.get('DOI_TUONG_ID'),
							'TEN_KHACH_HANG' : ct.get('TEN_DOI_TUONG'),
							# 'DIEN_GIAI' : ct.get('LOAI_KHACH_HANG'),
							'MA_SO_THUE' : ct.get('MA_SO_THUE'),
							'DIA_CHI' : ct.get('DIA_CHI'),
							'SO_THANH_TOAN_CHUA_DOI_TRU' : ct.get('SO_CHUA_DOI_TRU_THANH_TOAN'),
							'SO_CONG_NO_CHUA_DOI_TRU' : ct.get('SO_CHUA_DOI_TRU_CONG_NO'),
							
						})
						self.SALE_EX_DOI_TRU_CHUNG_TU_NHIEU_DOI_TUONG_CHI_TIET_IDS += new_line

	def lay_thong_tin_doi_tru(self,ngay,loai_tien):
		record = []
		params = {
			'DEN_NGAY': ngay,
			'DOI_TUONG_ID' : 594,
			'currency_id' : loai_tien
			}

		query = """   

		SELECT    (0) AS RefDetailID ,
				CAST(False AS BOOLEAN) AS Selected ,
				R."DOI_TUONG_ID" ,
				AO."MA_DOI_TUONG" ,
				AO."HO_VA_TEN" AS "TEN_DOI_TUONG" ,
				AO."LOAI_KHACH_HANG" ,
				AO."MA_SO_THUE" AS "MA_SO_THUE" ,
				AO."DIA_CHI" AS "DIA_CHI" ,
				coalesce(SUM(coalesce(R."SO_TIEN_THANH_TOAN", 0)), 0) AS "SO_CHUA_DOI_TRU_THANH_TOAN" ,
				coalesce(SUM(coalesce(R."SO_TIEN_THANH_TOAN_QUY_DOI", 0)), 0) AS "SO_CHUA_DOI_TRU_THANH_TOAN_QUY_DOI" ,
				CAST(0 AS DECIMAL) AS "SO_TIEN_THANH_TOAN" ,
				CAST(0 AS DECIMAL) AS "SO_TIEN_THANH_TOAN_QUY_DOI" ,
				coalesce(SUM(coalesce(R."SO_TIEN_CONG_NO", 0)), 0) AS "SO_CHUA_DOI_TRU_CONG_NO" ,
				coalesce(SUM(coalesce(R."SO_TIEN_CONG_NO_QUY_DOI", 0)), 0)  AS "SO_CHUA_DOI_TRU_CONG_NO_QUY_DOI" ,
				CAST(0 AS DECIMAL) AS "SO_TIEN_CONG_NO" ,
				CAST(0 AS DECIMAL) AS "SO_TIEN_CONG_NO_QUY_DOI" ,
				CAST(0 AS DECIMAL) AS "CHENH_LECH_SO_TIEN_QUY_DOI" ,
				0 AS "CHENH_LECH_SO_TIEN" ,
				N'Xem chi tiết' AS "CHI_TIET"
	  FROM      (


SELECT	Pay."DOI_TUONG_ID"
				,Pay."ID_CHUNG_TU"
				,Pay."NGAY_HOA_DON"
				,Pay."SO_HOA_DON"
				,coalesce(Pay."SO_TIEN_THANH_TOAN",0) - coalesce(SUM(FU."SO_TIEN"),0) AS "SO_TIEN_THANH_TOAN"
				,coalesce(Pay."SO_TIEN_THANH_TOAN_QUY_DOI",0) - coalesce(SUM(FU."SO_TIEN_QUY_DOI"),0) AS "SO_TIEN_THANH_TOAN_QUY_DOI"
				,0 AS "SO_TIEN_CONG_NO"
				,0 AS "SO_TIEN_CONG_NO_QUY_DOI"
		FROM	 (


SELECT	T."DOI_TUONG_ID",
						T."ID_CHUNG_TU",
						T."NGAY_HACH_TOAN",
						T."NGAY_HOA_DON",
						T."SO_HOA_DON",
						T."SO_HOA_DON_CHI_TIET",
						SUM(T."SO_TIEN_THANH_TOAN") AS "SO_TIEN_THANH_TOAN",
						SUM(T."SO_TIEN_THANH_TOAN_QUY_DOI") AS "SO_TIEN_THANH_TOAN_QUY_DOI"
				FROM (


						SELECT
							OAE."DOI_TUONG_ID",
							OAE.id AS "ID_CHUNG_TU",
							OAE."NGAY_HACH_TOAN",
							CASE WHEN OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL AND coalesce(OAEDI."SO_THU_TRUOC_NGUYEN_TE",0) <> 0 THEN OAEDI."NGAY_HOA_DON"
									ELSE OAE."NGAY_HACH_TOAN"
								END AS "NGAY_HOA_DON",
							CASE WHEN OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL AND coalesce(OAEDI."SO_THU_TRUOC_NGUYEN_TE",0) <> 0 THEN coalesce(OAEDI."SO_HOA_DON", '')
									ELSE N'OPN'
								END AS "SO_HOA_DON",
							1 AS "SO_HOA_DON_CHI_TIET",
							SUM(CASE WHEN OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NULL THEN OAE."DU_CO_NGUYEN_TE" - OAE."DU_NO_NGUYEN_TE"
									ELSE OAEDI."SO_THU_TRUOC_NGUYEN_TE"
								END) AS "SO_TIEN_THANH_TOAN",
							SUM(CASE WHEN OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NULL THEN OAE."DU_CO" - OAE."DU_NO"
									ELSE OAEDI."SO_CON_PHAI_THU"
								END) AS "SO_TIEN_THANH_TOAN_QUY_DOI"
					FROM account_ex_so_du_tai_khoan_chi_tiet AS OAE
						LEFT JOIN account_ex_sdtkct_theo_hoa_don AS OAEDI ON OAE.id = OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID"
					WHERE   OAE."TK_ID" = (SELECT id FROM danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN" = '131')
							AND OAE."currency_id" = %(currency_id)s
-- 							AND OAE."CHI_NHANH_ID" = (chi_nhanh_id)
							AND OAE."NGAY_HACH_TOAN" <= %(DEN_NGAY)s
					GROUP BY	OAE."DOI_TUONG_ID",
								OAE.id,
								OAE."NGAY_HACH_TOAN",
								CASE WHEN OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL AND coalesce(OAEDI."SO_THU_TRUOC_NGUYEN_TE",0) <> 0 THEN OAEDI."NGAY_HOA_DON"
									ELSE OAE."NGAY_HACH_TOAN"
								END,
								CASE WHEN OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL AND coalesce(OAEDI."SO_THU_TRUOC_NGUYEN_TE",0) <> 0 THEN coalesce(OAEDI."SO_HOA_DON", '')
									ELSE N'OPN'
								END
					HAVING SUM(CASE WHEN OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NULL THEN OAE."DU_CO_NGUYEN_TE" - OAE."DU_NO_NGUYEN_TE"
									ELSE OAEDI."SO_CON_PHAI_THU_NGUYEN_TE"
								END) > 0


					UNION ALL



						SELECT
											AL."DOI_TUONG_ID" ,
											AL."ID_CHUNG_TU",
											AL."NGAY_HACH_TOAN",
											AL."NGAY_CHUNG_TU",
											coalesce(AL."SO_CHUNG_TU", '') AS "SO_HOA_DON",
											0 AS "SO_HOA_DON_CHI_TIET",
											SUM(coalesce(AL."GHI_CO_NGUYEN_TE", 0) - coalesce(AL."GHI_NO_NGUYEN_TE", 0)) AS "SO_TIEN_THANH_TOAN",
											SUM(coalesce(AL."GHI_CO", 0) - coalesce(AL."GHI_NO", 0)) AS "SO_TIEN_THANH_TOAN_QUY_DOI"
									FROM    so_cong_no_chi_tiet AL
									WHERE   AL."TK_ID" = (SELECT id FROM danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN" = '131')
											AND AL."currency_id" = %(currency_id)s
				-- 							AND AL."CHI_NHANH_ID" = (chi_nhanh_id)
											AND AL."LOAI_CHUNG_TU" NOT IN (611,612,613,614,615,616,630)
											AND Al."NGAY_HACH_TOAN" <= %(DEN_NGAY)s
									GROUP BY AL."DOI_TUONG_ID" ,
											 AL."ID_CHUNG_TU",
											 AL."NGAY_HACH_TOAN",
											 AL."NGAY_CHUNG_TU",
											 coalesce(AL."SO_CHUNG_TU", '')
									HAVING  SUM(coalesce(AL."GHI_CO_NGUYEN_TE", 0) - coalesce(AL."GHI_NO_NGUYEN_TE", 0)) > 0

					) AS T
				GROUP BY	T."DOI_TUONG_ID",
							T."ID_CHUNG_TU",
							T."NGAY_HACH_TOAN",
							T."NGAY_HOA_DON",
							T."SO_HOA_DON",
							T."SO_HOA_DON_CHI_TIET"
				HAVING SUM(T."SO_TIEN_THANH_TOAN") > 0




) Pay
		LEFT JOIN(
	  			SELECT	F."DOI_TUONG_ID",
	  					F."ID_CHUNG_TU",
	  					F."NGAY_CHUNG_TU",
	  					F."SO_CHUNG_TU",
	  					SUM(coalesce(F."SO_TIEN",0)) AS "SO_TIEN",
	  					SUM(coalesce(F."SO_TIEN_QUY_DOI",0)) AS "SO_TIEN_QUY_DOI"
			 	FROM	(


					SELECT
CAST(GL."ID_CHUNG_TU_THANH_TOAN" AS INTEGER)AS"ID_CHUNG_TU"
,GL."NGAY_CHUNG_TU_THANH_TOAN"AS"NGAY_CHUNG_TU"
,GL."SO_CHUNG_TU_THANH_TOAN"AS"SO_CHUNG_TU"
,Gl."DOI_TUONG_ID"AS"DOI_TUONG_ID"
,TA."SO_TAI_KHOAN"
,SUM(coalesce(GL."SO_TIEN_THANH_TOAN",0))AS"SO_TIEN"
,SUM(coalesce(GL."SO_TIEN_THANH_TOAN_QUY_DOI",0))-SUM((CASE WHEN GL."LOAI_DOI_TRU"='1' THEN 0 ELSE coalesce(GL."CHENH_LECH_TY_GIA_SO_TIEN_QUY_DOI",0)END))AS"SO_TIEN_QUY_DOI"
FROM sale_ex_doi_tru_chi_tiet GL
INNER JOIN(
SELECT*FROM danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN"='131'
)TA ON TA.id = GL."TAI_KHOAN_ID"
WHERE
GL."currency_id"=%(currency_id)s
--ANDGL."CHI_NHANH_ID"=(chi_nhanh_id)
AND GL."CTTT_DA_GHI_SO"= True AND GL."CTCN_DA_GHI_SO"=True
-- AND(GL."DOI_TUONG_ID"=593 OR 593 ISNULL)
GROUP BY GL."ID_CHUNG_TU_THANH_TOAN",GL."DOI_TUONG_ID",TA."SO_TAI_KHOAN",GL."NGAY_CHUNG_TU_THANH_TOAN",GL."SO_CHUNG_TU_THANH_TOAN"


UNION ALL


SELECT
GLD."CHUNG_TU_NGHIEP_VU_KHAC_ID"AS"ID_CHUNG_TU"
,GL."NGAY_CHUNG_TU"AS"NGAY_CHUNG_TU"
,GL."SO_CHUNG_TU"AS"SO_CHUNG_TU"
,GLD."DOI_TUONG_NO_ID"AS"DOI_TUONG_ID"
,TA."SO_TAI_KHOAN"
,0AS"SO_TIEN"
,SUM(coalesce(GLD."CHENH_LECH_DANH_GIA_LAI",0))AS"SO_TIEN_QUY_DOI"
FROM account_ex_chung_tu_nghiep_vu_khac GL
INNER JOIN account_ex_chung_tu_nghiep_vu_khac_hach_toan GLD ON GLD."CHUNG_TU_NGHIEP_VU_KHAC_ID"=GL.id
INNER JOIN(
SELECT*FROM danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN"='131'
)TA ON GLD."TK_NO_ID"=TA.id
WHERE
GL."currency_id" = %(currency_id)s
--ANDGl."CHI_NHANH_ID"=(chi_nhanh_id)
AND(GLD."DOI_TUONG_NO_ID" = 593 OR 593 ISNULL)
GROUP BY GLD."CHUNG_TU_NGHIEP_VU_KHAC_ID",GLD."DOI_TUONG_NO_ID",TA."SO_TAI_KHOAN"
,GL."NGAY_CHUNG_TU",GL."SO_CHUNG_TU"



UNION ALL



SELECT
SA.id AS "ID_CHUNG_TU"
,SA."NGAY_CHUNG_TU"AS"NGAY_CHUNG_TU"
,SA."SO_CHUNG_TU"AS"SO_CHUNG_TU"
,SA."DOI_TUONG_ID"
,TA."SO_TAI_KHOAN"
,SUM(coalesce(SAD."THANH_TIEN",0)+coalesce(SAD."TIEN_THUE_GTGT",0)-coalesce(SAD."TIEN_CHIET_KHAU",0))AS"SO_TIEN"
,SUM(coalesce(SAD."THANH_TIEN_QUY_DOI",0)+coalesce(SAD."TIEN_THUE_GTGT_QUY_DOI",0)-coalesce(SAD."TIEN_CHIET_KHAU_QUY_DOI",0))AS"SO_TIEN_QUY_DOI"
FROM sale_ex_tra_lai_hang_ban SA
INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet SAD ON SAD."TRA_LAI_HANG_BAN_ID"=SA.id
INNER JOIN(
SELECT*FROM danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN"='131'
)TA ON SAD."TK_CO_ID"=TA.id
WHERE
SA."currency_id" = %(currency_id)s
--ANDSA."CHI_NHANH_ID"=(chi_nhanh_id)
AND SAD."TRA_LAI_HANG_BAN_ID" IS NOT NULL
-- AND(SA."DOI_TUONG_ID" = 593 OR 593 ISNULL)
GROUP BY SA.id,SA."DOI_TUONG_ID",TA."SO_TAI_KHOAN"
,SA."NGAY_CHUNG_TU"
,SA."SO_CHUNG_TU"

UNION ALL

SELECT
SA.id AS"ID_CHUNG_TU"
,SA."NGAY_CHUNG_TU"AS"NGAY_CHUNG_TU"
,SA."SO_CHUNG_TU"AS"SO_CHUNG_TU"
,SA."DOI_TUONG_ID"
,TA."SO_TAI_KHOAN"
,SUM(coalesce(SAD."THANH_TIEN",0)+coalesce(SAD."TIEN_THUE_GTGT",0)-coalesce(SAD."TIEN_CHIET_KHAU",0))AS"SO_TIEN"
,SUM(coalesce(SAD."THANH_TIEN_QUY_DOI",0)+coalesce(SAD."TIEN_THUE_GTGT_QUY_DOI",0)-coalesce(SAD."TIEN_CHIET_KHAU_QUY_DOI",0))AS"SO_TIEN_QUY_DOI"
FROM sale_ex_giam_gia_hang_ban SA
INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban SAD ON SAD."GIAM_GIA_HANG_BAN_ID"=SA.id
INNER JOIN(
SELECT*FROM danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN"='131'
)TA ON SAD."TK_CO_ID"=TA.id
WHERE
SA."currency_id" = %(currency_id)s
--ANDSA."CHI_NHANH_ID"=(chi_nhanh_id)
AND SAD."GIAM_GIA_HANG_BAN_ID"IS NOT NULL
-- AND(SA."DOI_TUONG_ID" = 593 OR 593 ISNULL)
GROUP BY SA.id,SA."DOI_TUONG_ID",TA."SO_TAI_KHOAN"
,SA."NGAY_CHUNG_TU"
,SA."SO_CHUNG_TU"



							) F
			 	GROUP BY F."ID_CHUNG_TU", F."DOI_TUONG_ID",F."NGAY_CHUNG_TU",F."SO_CHUNG_TU"
		) AS FU ON FU."ID_CHUNG_TU" = Pay."ID_CHUNG_TU" AND FU."DOI_TUONG_ID" = Pay."DOI_TUONG_ID"
				AND (Pay."SO_HOA_DON_CHI_TIET" = 0 OR (Pay."SO_HOA_DON_CHI_TIET" =1 AND coalesce(FU."SO_CHUNG_TU", '') = coalesce(Pay."SO_HOA_DON", '') AND coalesce(FU."NGAY_CHUNG_TU", %(DEN_NGAY)s) = coalesce(Pay."NGAY_HOA_DON", %(DEN_NGAY)s)))
				--AND Pay."SO_HOA_DON" = FU."SO_CHUNG_TU" AND Pay."NGAY_HOA_DON" = FU."NGAY_CHUNG_TU"
		GROUP BY Pay."DOI_TUONG_ID"
				,Pay."ID_CHUNG_TU"
				,Pay."NGAY_HOA_DON"
				,Pay."SO_HOA_DON"
				,coalesce(Pay."SO_TIEN_THANH_TOAN",0)
				,coalesce(Pay."SO_TIEN_THANH_TOAN_QUY_DOI",0)
		HAVING coalesce(Pay."SO_TIEN_THANH_TOAN",0) - coalesce(SUM(FU."SO_TIEN"),0) > 0




UNION ALL





		SELECT	Debt."DOI_TUONG_ID"
				,Debt."ID_CHUNG_TU"
				,Debt."NGAY_HOA_DON"
				,Debt."SO_HOA_DON"
				,0 AS "SO_TIEN_THANH_TOAN"
				,0 AS "SO_TIEN_THANH_QUY_DOI"
				,coalesce(Debt."SO_TIEN_CONG_NO",0) - coalesce(FU."SO_TIEN",0) AS "SO_TIEN_CONG_NO"
				,coalesce(Debt."SO_TIEN_CONG_NO_QUY_DOI",0) - coalesce(FU."SO_TIEN_QUY_DOI",0) AS "SO_TIEN_CONG_NO_QUY_DOI"
		FROM	 (


SELECT  AL."DOI_TUONG_ID" ,
					AL."ID_CHUNG_TU",
					AL."NGAY_HACH_TOAN",
					AL."NGAY_HOA_DON",
					Al."SO_HOA_DON",
					AL."SO_HOA_DON_CHI_TIET",
					SUM(coalesce(AL."GHI_NO_NGUYEN_TE", 0)) AS "SO_TIEN_CONG_NO" ,
					SUM(coalesce(AL."GHI_NO", 0)) AS "SO_TIEN_CONG_NO_QUY_DOI"
			FROM	(


SELECT
							OPN."DOI_TUONG_ID",
							OPN.id AS "ID_CHUNG_TU",
							OPN."NGAY_HACH_TOAN",
							SUM(CASE
								WHEN OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NULL THEN OPN."DU_NO_NGUYEN_TE" - OPN."DU_CO_NGUYEN_TE"
								ELSE OAEDI."SO_CON_PHAI_THU_NGUYEN_TE"
							END) AS "GHI_NO_NGUYEN_TE",
							SUM(CASE
								WHEN OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NULL THEN OPN."DU_NO" - OPN."DU_CO"
								ELSE OAEDI."SO_CON_PHAI_THU"
							END) AS "GHI_NO",
							OAEDI."NGAY_HOA_DON",
							coalesce(OAEDI."SO_HOA_DON", '') AS "SO_HOA_DON",
							1 AS "SO_HOA_DON_CHI_TIET"
				  FROM  account_ex_so_du_tai_khoan_chi_tiet AS OPN
					LEFT JOIN account_ex_sdtkct_theo_hoa_don AS OAEDI ON OPN.id = OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID"
					WHERE OPN."TK_ID" = (SELECT id FROM danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN" = '131')
						AND OPN."currency_id" = %(currency_id)s
-- 						AND OPN."CHI_NHANH_ID" = (chi_nhanh_id)
						AND OPN.state = 'da_ghi_so'
						AND OPN."NGAY_HACH_TOAN" <= %(DEN_NGAY)s
					GROUP BY	OPN."DOI_TUONG_ID",
								OPN.id,
								OPN."NGAY_HACH_TOAN",
								OAEDI."NGAY_HOA_DON",
								coalesce(OAEDI."SO_HOA_DON", '')
					HAVING SUM(CASE
								WHEN OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NULL THEN OPN."DU_NO_NGUYEN_TE" - OPN."DU_CO_NGUYEN_TE"
								ELSE OAEDI."SO_CON_PHAI_THU_NGUYEN_TE"
							END) > 0


UNION ALL



		SELECT	AOL."DOI_TUONG_ID" ,
							AOL."ID_CHUNG_TU",
							AOL."NGAY_HACH_TOAN",
							SUM(AOL."GHI_NO_NGUYEN_TE"-AOL."GHI_CO_NGUYEN_TE") AS "SO_TIEN_CONG_NO" ,
							SUM(AOL."GHI_NO"- AOL."GHI_CO") AS "SO_CONG_NO_TOAN_QUY_DOI",
							AOL."NGAY_HOA_DON",
							coalesce(AOL."SO_HOA_DON", '') AS "SO_HOA_DON",
							0 AS "SO_HOA_DON_CHI_TIET"
					FROM so_cong_no_chi_tiet AS AOL
					WHERE AOL."TK_ID" = (SELECT id FROM danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN" = '131')
						AND AOL."currency_id" = %(currency_id)s
-- 						AND AOL."CHI_NHANH_ID" = (chi_nhanh_id)
						AND AOL."NGAY_HACH_TOAN" <= %(DEN_NGAY)s
						AND AOL."LOAI_CHUNG_TU" NOT IN (611,612,613,614,615,616,630)
					GROUP BY	AOL."DOI_TUONG_ID",
								AOL."ID_CHUNG_TU",
								AOL."NGAY_HACH_TOAN",
								AOL."NGAY_HOA_DON",
								coalesce(AOL."SO_HOA_DON", '')
					HAVING SUM(AOL."GHI_NO_NGUYEN_TE"-AOL."GHI_CO_NGUYEN_TE") > 0


		) AS Al
			GROUP BY AL."DOI_TUONG_ID" ,
					 AL."ID_CHUNG_TU",
					 AL."NGAY_HACH_TOAN",
					 AL."NGAY_HOA_DON",
					Al."SO_HOA_DON",
					AL."SO_HOA_DON_CHI_TIET"
			HAVING  SUM(coalesce(AL."GHI_NO_NGUYEN_TE", 0)) > 0


) Debt
	  LEFT JOIN (
	  		SELECT	F."ID_CHUNG_TU",
	  				F."DOI_TUONG_ID",
	  				F."NGAY_HOA_DON",
	  				F."SO_HOA_DON",
	  				SUM(coalesce(F."SO_TIEN",0)) AS "SO_TIEN",
	  				SUM(coalesce(F."SO_TIEN_QUY_DOI",0)) AS "SO_TIEN_QUY_DOI"
	  		FROM (



					SELECT
cast(GL."ID_CHUNG_TU_CONG_NO" AS INTEGER)AS"ID_CHUNG_TU",
Gl."DOI_TUONG_ID"AS"DOI_TUONG_ID",
TA."SO_TAI_KHOAN",
(CASE WHEN GL."LOAI_CHUNG_TU_CONG_NO_ID"IN(610,612,613,614,620,330,331,332,333,334,352,357,358,359,360,362,363,364,365,366,368,369,370,371,372,374,375,376,377,378)
THEN GL."NGAY_CHUNG_TU_CONG_NO"
ELSE NULL
END)AS"NGAY_HOA_DON",
(CASE WHEN GL."LOAI_CHUNG_TU_CONG_NO_ID"IN(610,612,
613,614,620,
330,331,332,
333,334,352,
357,358,359,360,362,363,364,365,366,368,369,370,371,372,374,375,376,377,378)
THEN coalesce(GL."SO_HOA_DON_CONG_NO",'')
ELSE NULL
END)AS"SO_HOA_DON",
SUM(coalesce(GL."SO_TIEN_CONG_NO",0))AS"SO_TIEN",
SUM(coalesce(GL."SO_TIEN_CONG_NO_QUY_DOI",0))AS"SO_TIEN_QUY_DOI"
,GL."TY_GIA_CONG_NO"AS"TY_GIA"
FROM sale_ex_doi_tru_chi_tiet GL
INNER JOIN(SELECT*FROM danh_muc_he_thong_tai_khoan WHERE"SO_TAI_KHOAN"='131')TA ON TA.id=GL."TAI_KHOAN_ID"
WHERE GL."currency_id" = %(currency_id)s
--ANDGL."CHI_NHANH_ID"=(chi_nhanh_id)
AND GL."CTTT_DA_GHI_SO"=TRUE
AND GL."CTCN_DA_GHI_SO"=TRUE
-- AND(GL."DOI_TUONG_ID" = %(DOI_TUONG_ID)s OR %(DOI_TUONG_ID)s ISNULL)
GROUP BY GL."ID_CHUNG_TU_CONG_NO",
GL."DOI_TUONG_ID",
TA."SO_TAI_KHOAN",
GL."SO_HOA_DON_CONG_NO",
GL."NGAY_CHUNG_TU_CONG_NO",
GL."LOAI_CHUNG_TU_CONG_NO_ID"
,GL."TY_GIA_CONG_NO"



UNION ALL


SELECT
GLD."CHUNG_TU_NGHIEP_VU_KHAC_ID"AS"ID_CHUNG_TU",
GLD."DOI_TUONG_NO_ID"AS"DOI_TUONG_ID",
TA."SO_TAI_KHOAN",
(CASE WHEN GLD."LOAI_CHUNG_TU_ID"IN(610,612,613,614,620,330,331,332,333,334,352,357,358,359,360,362,363,364,365,366,368,369,370,371,372,374,375,376,377,378)
THEN GL."NGAY_CHUNG_TU"
ELSE NULL
END)AS"NGAY_HOA_DON",
(CASE WHEN GLD."LOAI_CHUNG_TU_ID"IN(610,612,613,614,620,330,331,332,333,334,352,357,358,359,360,362,363,364,365,366,368,369,370,371,372,374,375,376,377,378)
THEN coalesce(GL."SO_HOA_DON",'')
ELSE NULL
END)AS"SO_HOA_DON",
0 AS "SO_TIEN",
(-1)*SUM(coalesce(GLD."CHENH_LECH_DANH_GIA_LAI",0))AS"SO_TIEN_QUY_DOI"
,GL."TY_GIA"
FROM account_ex_chung_tu_nghiep_vu_khac GL
INNER JOIN account_ex_chung_tu_nghiep_vu_khac_hach_toan GLD ON GLD."CHUNG_TU_NGHIEP_VU_KHAC_ID"=GL.id
INNER JOIN(SELECT*FROM danh_muc_he_thong_tai_khoan WHERE"SO_TAI_KHOAN"='131')TA ON GLD."TK_NO_ID"=TA.id
WHERE GL."currency_id" = %(currency_id)s
--ANDGl."CHI_NHANH_ID"=(chi_nhanh_id)
AND(GLD."DOI_TUONG_NO_ID"= %(DOI_TUONG_ID)s
OR %(DOI_TUONG_ID)s ISNULL
)
GROUP BY GLD."CHUNG_TU_NGHIEP_VU_KHAC_ID",
GLD."DOI_TUONG_NO_ID",
TA."SO_TAI_KHOAN",
GL."NGAY_CHUNG_TU",
GL."NGAY_HOA_DON",
GLD."LOAI_CHUNG_TU_ID"
,GL."TY_GIA",
GL."SO_HOA_DON"

UNION ALL

SELECT SAD."TRA_LAI_HANG_BAN_ID"AS"ID_CHUNG_TU",
SA."DOI_TUONG_ID",
TA."SO_TAI_KHOAN",
NULL AS"NGAY_HOA_DON",
NULL AS"SO_HOA_DON",
SUM(coalesce(SAD."THANH_TIEN",0)
+coalesce(SAD."TIEN_THUE_GTGT",0)
-coalesce(SAD."TIEN_CHIET_KHAU",0)) AS "SO_TIEN",
SUM(coalesce(SAD."THANH_TIEN_QUY_DOI",0)
+coalesce(SAD."TIEN_THUE_GTGT_QUY_DOI",0)
-coalesce(SAD."TIEN_CHIET_KHAU_QUY_DOI",0))AS"SO_TIEN_QUY_DOI"
,SA."TY_GIA"
FROM sale_ex_tra_lai_hang_ban SA
INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet SAD ON SAD."TRA_LAI_HANG_BAN_ID"=SA.id
INNER JOIN(SELECT*FROM danh_muc_he_thong_tai_khoan WHERE"SO_TAI_KHOAN"='131')TA ON SAD."TK_CO_ID"=TA.id
WHERE SA."currency_id"=%(currency_id)s
--ANDSA."CHI_NHANH_ID"=(chi_nhanh_id)
AND SA.state='da_ghi_so'
AND SAD."CHUNG_TU_BAN_HANG_ID"IS NOT NULL
-- AND(SA."DOI_TUONG_ID" = %(DOI_TUONG_ID)s OR %(DOI_TUONG_ID)s ISNULL)
GROUP BY SAD."TRA_LAI_HANG_BAN_ID",
SA."DOI_TUONG_ID",
TA."SO_TAI_KHOAN"
,SA."TY_GIA"


UNION ALL

SELECT SAD."CHUNG_TU_BAN_HANG_ID"AS"ID_CHUNG_TU",
SA."DOI_TUONG_ID",
TA."SO_TAI_KHOAN",
NULL AS"NGAY_HOA_DON",
NULL AS"SO_HOA_DON",
SUM(coalesce(SAD."THANH_TIEN",0)
+coalesce(SAD."TIEN_THUE_GTGT",0)
-coalesce(SAD."TIEN_CHIET_KHAU",0)) AS "SO_TIEN",
SUM(coalesce(SAD."THANH_TIEN_QUY_DOI",0)
+coalesce(SAD."TIEN_THUE_GTGT_QUY_DOI",0)
-coalesce(SAD."TIEN_CHIET_KHAU_QUY_DOI",0))AS"SO_TIEN_QUY_DOI"
,SA."TY_GIA"
FROM sale_ex_giam_gia_hang_ban SA
INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban SAD ON SAD."GIAM_GIA_HANG_BAN_ID"=SA.id
INNER JOIN(SELECT*FROM danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN" = '131') TA ON SAD."TK_CO_ID"=TA.id
WHERE SA."currency_id" = %(currency_id)s
--ANDSA."CHI_NHANH_ID"=(chi_nhanh_id)
AND SA.state='da_ghi_so'
AND SAD."CHUNG_TU_BAN_HANG_ID"IS NOT NULL
-- AND(SA."DOI_TUONG_ID" = %(DOI_TUONG_ID)s OR %(DOI_TUONG_ID)s ISNULL)
GROUP BY SAD."CHUNG_TU_BAN_HANG_ID",
SA."DOI_TUONG_ID",
TA."SO_TAI_KHOAN"
,SA."TY_GIA"





						 ) F
	  		GROUP BY F."ID_CHUNG_TU", F."DOI_TUONG_ID",F."NGAY_HOA_DON",F."SO_HOA_DON"
	  ) AS FU ON FU."ID_CHUNG_TU" = Debt."ID_CHUNG_TU" AND FU."DOI_TUONG_ID" = Debt."DOI_TUONG_ID"
			AND (Debt."SO_HOA_DON_CHI_TIET" = 0 OR (Debt."SO_HOA_DON_CHI_TIET" =1 AND coalesce(FU."SO_HOA_DON", '') = coalesce(Debt."SO_HOA_DON", '') AND coalesce(FU."NGAY_HOA_DON", %(DEN_NGAY)s) = coalesce(Debt."NGAY_HOA_DON", %(DEN_NGAY)s)))
	  WHERE	coalesce(Debt."SO_TIEN_CONG_NO",0) - coalesce(FU."SO_TIEN",0) > 0
			AND Debt."NGAY_HACH_TOAN" <= %(DEN_NGAY)s


) R
				INNER JOIN res_partner AO ON R."DOI_TUONG_ID" = AO.id
	  WHERE		AO.active = TRUE
	  GROUP BY  R."DOI_TUONG_ID" ,
				AO."MA_DOI_TUONG" ,
				AO."HO_VA_TEN" ,
				AO."LOAI_KHACH_HANG" ,
				AO."MA_SO_THUE" ,
				AO."DIA_CHI"
	  HAVING    coalesce(SUM(coalesce(R."SO_TIEN_THANH_TOAN", 0)), 0) > 0
				AND coalesce(SUM(coalesce(R."SO_TIEN_CONG_NO", 0)), 0) > 0

		"""  
		cr = self.env.cr

		cr.execute(query, params)
		for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
			record.append({
				'DOI_TUONG_ID': line.get('DOI_TUONG_ID', ''),
				'TEN_DOI_TUONG': line.get('TEN_DOI_TUONG', ''),
				'LOAI_KHACH_HANG': line.get('LOAI_KHACH_HANG', ''),
				'MA_SO_THUE': line.get('MA_SO_THUE', ''),
				'DIA_CHI': line.get('DIA_CHI', ''),
				'SO_CHUA_DOI_TRU_THANH_TOAN': line.get('SO_CHUA_DOI_TRU_THANH_TOAN', ''),
				'SO_CHUA_DOI_TRU_CONG_NO': line.get('SO_CHUA_DOI_TRU_CONG_NO', ''),
			})
		
		return record
		
