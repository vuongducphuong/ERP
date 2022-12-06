# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError

class SALE_EX_TINH_GIA_BAN(models.Model):
	_name = 'sale.ex.tinh.gia.ban'
	_description = ''
	_auto = False
	currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
	DON_VI_TINH = fields.Selection([('DON_VI_TINH_CHINH', 'Đơn vị tính chính'), ('DON_VI_CHUYEN_DOI_1', 'Đơn vị chuyển đổi 1'), ('DON_VI_CHUYEN_DOI_2', 'Đơn vị chuyển đổi 2'), ], string='Đơn vị tính', help='Đơn vị tính',default='DON_VI_TINH_CHINH')
	
	TY_LE_PHAN_TRAM = fields.Float(string='Tỷ lệ %', help='Tỷ lệ phần trăm')
	SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
	GIA_BAN_1 = fields.Boolean(string='Giá bán 1', help='Giá bán 1',default=True)
	GIA_BAN_2 = fields.Boolean(string='Giá bán 2', help='Giá bán 2')
	GIA_BAN_3 = fields.Boolean(string='Giá bán 3', help='Giá bán 3')
	name = fields.Char(string='Name', help='Name', oldname='NAME')
	SALE_EX_TINH_GIA_BAN_CHI_TIET_IDS = fields.One2many('sale.ex.tinh.gia.ban.chi.tiet', 'TINH_GIA_BAN_CHI_TIET_ID', string='Tính giá bán chi tiết')



	thay_doi_gia_ban_dua_tren = fields.Selection([
		('gia_ban_trong_danh_muc', 'Giá bán trong danh mục'),
		('gia_ban_co_dinh', 'Giá bán cố định'),
		('gia_mua_gan_nhat_trong_danh_muc','Giá mua gần nhất trong danh mục'),
		('gia_mua_co_dinh','Giá mua cố định'),
		], default='gia_ban_trong_danh_muc')
	
	thay_doi_gia_ban_theo = fields.Selection([
		('ty_le_bt', 'Tỷ lệ %'),
		('so_tien_bt', 'Số tiền'),
		], default='ty_le_bt' )

	
	@api.model
	def tinh_gia_ban(self, args):
		new_line = [[5]]
		if self.SALE_EX_TINH_GIA_BAN_CHI_TIET_IDS:
			check = False
			for chi_tiet in self.SALE_EX_TINH_GIA_BAN_CHI_TIET_IDS:
				so_tien = 0
				vat_tu_hang_hoa = self.env['danh.muc.vat.tu.hang.hoa'].search([('id', '=', chi_tiet.MA_HANG_ID.id)],limit=1)
				if self.thay_doi_gia_ban_dua_tren == 'gia_ban_trong_danh_muc':
					so_tien = vat_tu_hang_hoa.DON_GIA_BAN
				elif self.thay_doi_gia_ban_dua_tren == 'gia_ban_co_dinh':
					so_tien = chi_tiet.GIA_BAN_CO_DINH
				elif self.thay_doi_gia_ban_dua_tren == 'gia_mua_gan_nhat_trong_danh_muc':
					so_tien = vat_tu_hang_hoa.DON_GIA_MUA_GAN_NHAT
				elif self.thay_doi_gia_ban_dua_tren == 'gia_mua_co_dinh':
					so_tien = chi_tiet.GIA_MUA_CO_DINH

				if chi_tiet.AUTO_SELECT == True:
					if self.thay_doi_gia_ban_theo == 'so_tien_bt':
						if self.GIA_BAN_1 == True:
							chi_tiet.GIA_BAN_1 = so_tien + self.SO_TIEN 
						if self.GIA_BAN_2 == True:
							chi_tiet.GIA_BAN_2 = so_tien + self.SO_TIEN
						if self.GIA_BAN_3 == True:
							chi_tiet.GIA_BAN_3 = so_tien + self.SO_TIEN
					elif self.thay_doi_gia_ban_theo == 'ty_le_bt':
						if self.GIA_BAN_1 == True:
							chi_tiet.GIA_BAN_1 = so_tien + (so_tien*self.TY_LE_PHAN_TRAM)/100
						if self.GIA_BAN_2 == True:
							chi_tiet.GIA_BAN_2 = so_tien + (so_tien*self.TY_LE_PHAN_TRAM)/100
						if self.GIA_BAN_3 == True:
							chi_tiet.GIA_BAN_3 = so_tien + (so_tien*self.TY_LE_PHAN_TRAM)/100
					check = True
				new_line += [(0,0,{
					'MA_HANG_ID' : chi_tiet.MA_HANG_ID.id,
					'TEN_HANG' : chi_tiet.TEN_HANG,
					'NHOM_VTHH_ID' : chi_tiet.NHOM_VTHH_ID,
					'DON_VI_TINH_ID' : chi_tiet.DON_VI_TINH_ID.id,
					'GIA_NHAP_GAN_NHAT' : chi_tiet.GIA_NHAP_GAN_NHAT,
					'GIA_MUA_CO_DINH' : chi_tiet.GIA_MUA_CO_DINH,
					'GIA_BAN_CO_DINH' : chi_tiet.GIA_BAN_CO_DINH,
					'GIA_BAN_1' : chi_tiet.GIA_BAN_1,
					'GIA_BAN_2' : chi_tiet.GIA_BAN_2,
					'GIA_BAN_3' : chi_tiet.GIA_BAN_3,
				})]
			if check == False:
				raise ValidationError("Bạn phải chọn ít nhất một vật tư, hàng hóa để tính giá bán")
		return {'SALE_EX_TINH_GIA_BAN_CHI_TIET_IDS' : new_line}
			
	@api.model
	def default_get(self, fields):
		rec = super(SALE_EX_TINH_GIA_BAN, self).default_get(fields)
		rec['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')]).id

		
		rec['SALE_EX_TINH_GIA_BAN_CHI_TIET_IDS'] = []
		rec['SALE_EX_TINH_GIA_BAN_CHI_TIET_IDS'] = self.lay_du_lieu()
		return rec

	
	@api.model
	def xu_ly_hoan(self, args):
		new_line = [[5]]
		new_line += self.lay_du_lieu()
		return {'SALE_EX_TINH_GIA_BAN_CHI_TIET_IDS' : new_line}
	
	def lay_du_lieu(self):
		arr_vthh = []
		du_lieu = self.lay_du_lieu_vthh(848,'DON_VI_TINH_CHINH',81)
		if du_lieu:
			for line in du_lieu:
				arr_vthh += [(0,0,{
					'MA_HANG_ID': line.get('MA_HANG_ID'),
					'TEN_HANG': line.get('TEN_HANG'),
					# 'NHOM_VTHH_ID': line.get('MA_HANG_ID'),
					'DON_VI_TINH_ID': line.get('DVT_CHINH_ID'),
					'GIA_NHAP_GAN_NHAT': line.get('DON_GIA_NHAP_GAN_NHAT'),
					'GIA_MUA_CO_DINH': line.get('DON_GIA_MUA_CO_DINH'),
					'GIA_BAN_CO_DINH': line.get('DON_GIA_BAN_CO_DINH'),
					'GIA_BAN_1': line.get('GIA_BAN_1'),
					'GIA_BAN_2': line.get('GIA_BAN_2'),
					'GIA_BAN_3': line.get('GIA_BAN_3'),
					'LIST_NHOM_VTHH': line.get('NHOM_VTHH'),
				})]
		return arr_vthh

	def lay_du_lieu_vthh(self,loai_tien,dvt,chi_nhanh):
		record = []
		don_vi_tinh = 0
		if dvt == 'DON_VI_CHUYEN_DOI_1':
			don_vi_tinh = 1
		elif dvt == 'DON_VI_CHUYEN_DOI_2':
			don_vi_tinh = 2
		params = {
			'currency_id': loai_tien,
			'DVT' : don_vi_tinh,
			'CHI_NHANH_ID' : chi_nhanh,
			}

		query = """   
DO LANGUAGE plpgsql $$

DECLARE
tham_so_loai_tien INTEGER:= %(currency_id)s;
tham_so_don_vi_chinh INTEGER:= 0;
tham_so_chi_nhanh INTEGER:= 81;
tham_so_kho_rieng_biet INTEGER:= 0;

BEGIN
DROP TABLE if exists TMP_KET_QUA;
IF tham_so_don_vi_chinh = 0
THEN
  CREATE TEMP TABLE TMP_KET_QUA
  AS
  SELECT DISTINCT  ii.id AS"MA_HANG_ID" ,
		ii."CHI_NHANH_ID" ,
		ii."BAR_CODE" ,
		ii."MA" AS "MA_HANG" ,
		ii."TEN" AS "TEN_HANG" ,
		ii."TINH_CHAT" ,
		ii."MA_PHAN_CAP" ,
		ii."MA_NHOM_VTHH" ,
		ii."LIST_NHOM_VTHH",
		ii."DIEN_GIAI_KHI_MUA" ,
		ii."DVT_CHINH_ID" ,
		ii."THOI_HAN_BH" ,
		ii."SO_LUONG_TON_TOI_THIEU" ,
		ii."NGUON_GOC" ,
		ii."KHO_NGAM_DINH_ID" ,
		ii."TAI_KHOAN_KHO_ID" ,
		ii."TK_NO_ID" ,
		ii."TK_DOANH_THU_ID" ,
		ii."TY_LE_CKMH",
		coalesce(IIPUP."DON_GIA", 0) AS "DON_GIA_NHAP_GAN_NHAT" ,
--         Đơn giá mua cố định
		coalesce(IIPFUP."DON_GIA", 0) AS "DON_GIA_CO_DINH" ,
		ii."GIA_BAN_1" ,
		ii."GIA_BAN_2" ,
		ii."GIA_BAN_3" ,
		ii."GIA_CO_DINH" ,
		ii."LA_DON_GIA_SAU_THUE" ,
		ii."THUE_SUAT_GTGT_ID" ,
		ii."THUE_SUAT_THUE_NK" ,
		ii."THUE_SUAT_THUE_XK" ,
		ii."NHOM_HHDV_CHIU_THUE_TTDB_ID" ,
		ii."LA_HE_THONG" ,
		ii.active ,
		--ii.IsSet"DON_GIA"ByUnitConvert ,
		ii."CHIET_KHAU" ,
		ii."LOAI_CHIET_KHAU" ,
		ii."THEO_DOI_THEO_MA_QUY_CACH" ,
		ii."PHUONG_PHAP_TINH_GIA" ,
  --         ii.CreatedDate ,
  --         ii.CreatedBy ,
  --         ii.ModifiedDate ,
  --         ii.ModifiedBy ,
		  U.name AS "TEN_DVT" ,
		  ii."GIA_BAN_1" AS "DON_GIA_BAN"
  FROM    danh_muc_vat_tu_hang_hoa AS II
		  LEFT JOIN danh_muc_don_vi_tinh AS U ON II."DVT_CHINH_ID" = U.id
		  LEFT JOIN danh_muc_vthh_don_gia_mua_gan_nhat IIPUP ON II.id = IIPUP."VAT_TU_HANG_HOA_ID"
													AND IIPUP."currency_id" = tham_so_loai_tien
													AND ( IIPUP."DON_VI_TINH_ID" = II."DVT_CHINH_ID"
													OR ( II."DVT_CHINH_ID" IS NULL
													AND IIPUP."DON_VI_TINH_ID" IS NULL
													)
													)
  LEFT JOIN danh_muc_vthh_don_gia_mua_co_dinh AS IIPFUP ON IIPFUP."VAT_TU_HANG_HOA_ID" = II.id
					  AND IIPFUP."currency_id" = tham_so_loai_tien
					  AND (IIPFUP."DON_VI_TINH_ID" = II."DVT_CHINH_ID"
						  OR ( II."DVT_CHINH_ID" IS NULL
							AND IIPFUP."DON_VI_TINH_ID" IS NULL ))
  WHERE   ( ( tham_so_kho_rieng_biet = 0 )
			OR ( tham_so_kho_rieng_biet = 1
				 AND II."CHI_NHANH_ID" = tham_so_chi_nhanh
			   )
		  )
		  AND ii."TINH_CHAT" <> '2';
END IF;
IF tham_so_don_vi_chinh <> 0
THEN
  CREATE TEMP TABLE TMP_KET_QUA
  AS
  SELECT DISTINCT  ii.id AS"MA_HANG_ID" ,
		ii."CHI_NHANH_ID" ,
		ii."BAR_CODE" ,
		ii."MA" AS "MA_HANG" ,
		ii."TEN" AS "TEN_HANG" ,
		ii."TINH_CHAT" ,
		ii."MA_PHAN_CAP" ,
		ii."MA_NHOM_VTHH" ,
		ii."LIST_NHOM_VTHH",
		ii."DIEN_GIAI_KHI_MUA" ,
		ii."DVT_CHINH_ID" ,
		ii."THOI_HAN_BH" ,
		ii."SO_LUONG_TON_TOI_THIEU" ,
		ii."NGUON_GOC" ,
		ii."KHO_NGAM_DINH_ID" ,
		ii."TAI_KHOAN_KHO_ID" ,
		ii."TK_NO_ID" ,
		ii."TK_DOANH_THU_ID" ,
		ii."TY_LE_CKMH",
		coalesce(IIPUP."DON_GIA", 0) AS "DON_GIA_NHAP_GAN_NHAT" ,
--         Đơn giá mua cố định
		coalesce(IIPFUP."DON_GIA", 0) AS "DON_GIA_CO_DINH" ,
		ii."GIA_BAN_1" ,
		ii."GIA_BAN_2" ,
		ii."GIA_BAN_3" ,
		ii."GIA_CO_DINH" ,
		ii."LA_DON_GIA_SAU_THUE" ,
		ii."THUE_SUAT_GTGT_ID" ,
		ii."THUE_SUAT_THUE_NK" ,
		ii."THUE_SUAT_THUE_XK" ,
		ii."NHOM_HHDV_CHIU_THUE_TTDB_ID" ,
		ii."LA_HE_THONG" ,
		ii.active ,
		--ii.IsSet"DON_GIA"ByUnitConvert ,
		ii."CHIET_KHAU" ,
		ii."LOAI_CHIET_KHAU" ,
		ii."THEO_DOI_THEO_MA_QUY_CACH" ,
		ii."PHUONG_PHAP_TINH_GIA" ,
  --         ii.CreatedDate ,
  --         ii.CreatedBy ,
  --         ii.ModifiedDate ,
  --         ii.ModifiedBy ,
		  U.name AS "TEN_DVT" ,
		  ii."GIA_BAN_1" AS "DON_GIA_BAN"
  FROM    danh_muc_vat_tu_hang_hoa AS II
		  LEFT JOIN danh_muc_don_vi_tinh AS U ON II."DVT_CHINH_ID" = U.id
		  LEFT JOIN danh_muc_vat_tu_hang_hoa_don_vi_chuyen_doi AS IIUC ON II.id = IIUC."VAT_TU_HANG_HOA_ID"
		  LEFT JOIN danh_muc_vthh_don_gia_mua_gan_nhat IIPUP ON II.id = IIPUP."VAT_TU_HANG_HOA_ID"
													AND IIPUP."currency_id" = tham_so_loai_tien
													AND ( IIPUP."DON_VI_TINH_ID" = II."DVT_CHINH_ID"
													OR ( II."DVT_CHINH_ID" IS NULL
													AND IIPUP."DON_VI_TINH_ID" IS NULL
													)
													)
  LEFT JOIN danh_muc_vthh_don_gia_mua_co_dinh AS IIPFUP ON IIPFUP."VAT_TU_HANG_HOA_ID" = II.id
					  AND IIPFUP."currency_id" = tham_so_loai_tien
					  AND (IIPFUP."DON_VI_TINH_ID" = II."DVT_CHINH_ID"
						  OR ( II."DVT_CHINH_ID" IS NULL
							AND IIPFUP."DON_VI_TINH_ID" IS NULL ))
  WHERE   IIUC."STT" = tham_so_don_vi_chinh
		  AND ( ( tham_so_kho_rieng_biet = 0 )
				OR ( tham_so_kho_rieng_biet = 1
					 AND II."CHI_NHANH_ID" = tham_so_chi_nhanh
				   )
			  )
		  AND ii."TINH_CHAT" <> '2';
END IF;


END $$;


SELECT * FROM TMP_KET_QUA;

-- DROP TABLE TMP_KET_QUA;


		"""  
		cr = self.env.cr

		cr.execute(query, params)
		for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
			record.append({
				'MA_HANG_ID': line.get('MA_HANG_ID', ''),
				'TEN_HANG': line.get('TEN_HANG', ''),
				'DVT_CHINH_ID': line.get('DVT_CHINH_ID', ''),
				'DON_GIA_NHAP_GAN_NHAT': line.get('DON_GIA_NHAP_GAN_NHAT', ''),
				'DON_GIA_MUA_CO_DINH': line.get('DON_GIA_CO_DINH', ''),
				'GIA_BAN_1': line.get('GIA_BAN_1', ''),
				'GIA_BAN_2': line.get('GIA_BAN_2', ''),
				'GIA_BAN_3': line.get('GIA_BAN_3', ''),
				'DON_GIA_BAN_CO_DINH': line.get('GIA_CO_DINH', ''),
				'NHOM_VTHH': line.get('LIST_NHOM_VTHH', ''),   
			})
		
		return record