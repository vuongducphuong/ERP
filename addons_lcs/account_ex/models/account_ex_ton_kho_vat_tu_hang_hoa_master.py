# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from datetime import timedelta, datetime

class ACCOUNT_EX_TON_KHO_VAT_TU_HANG_HOA_MASTER(models.Model):
	_name = 'account.ex.ton.kho.vat.tu.hang.hoa.master'
	_description = ''
	_inherit = ['mail.thread']
	KHO_ID = fields.Many2one('danh.muc.kho', string='Kho', help='Kho')
	NAME = fields.Char(string='Name', help='Name')

	ACCOUNT_EX_TON_KHO_VAT_TU_HANG_HOA_IDS = fields.One2many('account.ex.ton.kho.vat.tu.hang.hoa', 'TON_KHO_VAT_TU_HANG_HOA_MASTER_ID', string='Tồn kho vật tư hàng hóa')


	@api.model
	def default_get(self, fields):
		rec = super(ACCOUNT_EX_TON_KHO_VAT_TU_HANG_HOA_MASTER, self).default_get(fields)
		rec['KHO_ID'] = self.env['danh.muc.kho'].search([],limit=1).id
		return rec
	
	@api.model
	def create(self, values):
		ngay_bat_dau_nam_tai_chinh = self.env['ir.config_parameter'].get_param('he_thong.TU_NGAY_BAT_DAU_TAI_CHINH')
		if ngay_bat_dau_nam_tai_chinh:
			ngay_bat_dau_nam_tai_chinh_date = datetime.strptime(ngay_bat_dau_nam_tai_chinh, '%Y-%m-%d').date()
			ngay_hach_toan = ngay_bat_dau_nam_tai_chinh_date + timedelta(days=-1)
			ngay_hach_toan_str = ngay_hach_toan.strftime('%Y-%m-%d')
		kho = self.env['danh.muc.kho'].search([('id', '=', values.get('KHO_ID'))])
		if kho:
			if kho.TK_KHO_ID:
				so_tu_tai_khoan_chi_tiet = self.env['account.ex.so.du.tai.khoan.chi.tiet'].search([('TK_ID', '=', kho.TK_KHO_ID.id)])
				for sd_ct in so_tu_tai_khoan_chi_tiet:
					sd_ct.bo_ghi_so()
					sd_ct.unlink()
		
		chi_tiet_server = self.env['account.ex.ton.kho.vat.tu.hang.hoa'].search([('KHO_ID', '=', values.get('KHO_ID'))])
		master_server = self.env['account.ex.ton.kho.vat.tu.hang.hoa.master'].search([('KHO_ID', '=', values.get('KHO_ID'))])
		
		if chi_tiet_server:
			for vthh_chi_tiet in chi_tiet_server:
				vthh_chi_tiet.bo_ghi_so()
				vthh_chi_tiet.unlink()
		if master_server:
			for mt in master_server:
				mt.unlink()
		if values.get('ACCOUNT_EX_TON_KHO_VAT_TU_HANG_HOA_IDS'):
			for vthh in values.get('ACCOUNT_EX_TON_KHO_VAT_TU_HANG_HOA_IDS'):
				vthh[2]['KHO_ID'] = values.get('KHO_ID')
				vthh[2]['LOAI_CHUNG_TU'] = 611
				vthh[2]['NGAY_HACH_TOAN'] = ngay_hach_toan_str
		result = super(ACCOUNT_EX_TON_KHO_VAT_TU_HANG_HOA_MASTER, self).create(values)

		if values.get('ACCOUNT_EX_TON_KHO_VAT_TU_HANG_HOA_IDS'):
			thu_tu = 0
			for vthh_client in values.get('ACCOUNT_EX_TON_KHO_VAT_TU_HANG_HOA_IDS'):
				if vthh_client[2].get('SO_LUONG') > 0 or vthh_client[2].get('GIA_TRI_TON') > 0:
					# chi_tiet_server = self.env['account.ex.ton.kho.vat.tu.hang.hoa'].create(vthh_client[2])
					chi_tiet_server = self.env['account.ex.ton.kho.vat.tu.hang.hoa'].search([('MA_HANG_ID', '=', vthh_client[2].get('MA_HANG_ID'))])
					if chi_tiet_server:
						for chi_tiet in chi_tiet_server:
							chi_tiet.action_ghi_so(thu_tu)
							thu_tu += 1
		if result.KHO_ID:
			if result.KHO_ID.TK_KHO_ID:
				cac_kho_cung_tk = self.env['danh.muc.kho'].search([('TK_KHO_ID', '=', result.KHO_ID.TK_KHO_ID.id)])
				tong_tien = 0
				if cac_kho_cung_tk:
					for kho in cac_kho_cung_tk:
						ton_kho_vthh = self.env['account.ex.ton.kho.vat.tu.hang.hoa'].search([('KHO_ID', '=', kho.id)])
						if ton_kho_vthh:
							for line in ton_kho_vthh:
								tong_tien += line.GIA_TRI_TON
				loai_tien = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'VND')])
				if kho:
					if kho.TK_KHO_ID:
						self.env['account.ex.so.du.tai.khoan.chi.tiet'].create({
						'LOAI_CHUNG_TU': '610',
						'TK_ID' : result.KHO_ID.TK_KHO_ID.id,
						'currency_id' : loai_tien.id,
						'DU_NO' : tong_tien,
						'DU_NO_NGUYEN_TE' : tong_tien,
						})
						chi_tiet = self.env['account.ex.so.du.tai.khoan.chi.tiet'].search([('TK_ID', '=', result.KHO_ID.TK_KHO_ID.id),('currency_id','=',loai_tien.id),('LOAI_CHUNG_TU','=','610')], limit=1)
						chi_tiet.action_ghi_so()

		return result
	

	@api.model
	def ton_kho_vat_tu_hang_hoa(self, args):
		new_line = [[5]]
		if args.get('kho_id'):
			kho_id = args.get('kho_id')
		else:
			kho_id = self.env['danh.muc.kho'].search([],limit=1).id
		du_lieu_vthh = self.lay_du_lieu_vthh(kho_id,self.get_chi_nhanh())
		if du_lieu_vthh:
			for vthh in du_lieu_vthh:
				new_line += [(0,0,{
					'MA_HANG_ID': [vthh.get('MA_HANG_ID'),vthh.get('MA_HANG')],
					'TEN_HANG': vthh.get('TEN_HANG'),
					'LIST_NHOM_VTHH': vthh.get('LIST_NHOM_VTHH'),
					'DVT_ID': [vthh.get('DVT_ID'),vthh.get('TEN_DVT')],
					'KHO_ID': vthh.get('KHO_ID'),
					'SO_LUONG': vthh.get('SO_LUONG'),
					'GIA_TRI_TON': vthh.get('GIA_TRI_TON'),
					'SO_LO': vthh.get('SO_LO'),
					'HAN_SU_DUNG': vthh.get('HAN_SU_DUNG'),
					'SO_LUONG_THEO_DVT_CHINH': vthh.get('SO_LUONG_THEO_DVT_CHINH'),
					'NHAP_MA_QUY_CACH' : 'Nhập mã quy cách',
					'THEO_DOI_THEO_MA_QUY_CACH': vthh.get('THEO_DOI_THEO_MA_QUY_CACH'),
					'CHI_TIET_VTHH' : 1,
					})]
		return {'ACCOUNT_EX_TON_KHO_VAT_TU_HANG_HOA_IDS': new_line}



	def lay_du_lieu_vthh(self,kho_id,chi_nhanh):
		record = []
		phuong_phap_tinh_gia = self.env['ir.config_parameter'].get_param('he_thong.PHUONG_PHAP_TINH_GIA_XUAT_KHO')
		tham_so_phuong_thuc_tinh_gia = 0
		if phuong_phap_tinh_gia == 'GIA_DICH_DANH':
			tham_so_phuong_thuc_tinh_gia = 1
		elif phuong_phap_tinh_gia == 'BINH_QUAN_TUC_THOI':
			tham_so_phuong_thuc_tinh_gia = 2
		elif phuong_phap_tinh_gia == 'NHAP_TRUOC_XUAT_TRUOC':
			tham_so_phuong_thuc_tinh_gia = 3
		params = {
			'KHO_ID': kho_id,
			'CHI_NHANH_ID': chi_nhanh,
			'PHUONG_THUC_TINH_GIA' : tham_so_phuong_thuc_tinh_gia,
			}
		query = """   

DO LANGUAGE plpgsql $$ DECLARE

tham_so_kho_id  INTEGER := %(KHO_ID)s;
tham_so_chi_nhanh INTEGER := %(CHI_NHANH_ID)s ;
tham_so_la_chi_tiet INTEGER := 0 ;
tham_so_phuong_thuc_tinh_gia INTEGER := %(PHUONG_THUC_TINH_GIA)s ;



BEGIN

IF tham_so_phuong_thuc_tinh_gia = 0 OR tham_so_phuong_thuc_tinh_gia = 1
			THEN
			DROP TABLE IF EXISTS TMP_KET_QUA;
			CREATE TEMP TABLE TMP_KET_QUA
			AS
			SELECT
					O.id AS "ID_CHUNG_TU" ,
					O."LOAI_CHUNG_TU" ,
					O."NGAY_HACH_TOAN" ,
					O."SO_CHUNG_TU" ,
					o. state AS "TRANG_THAI_GHI_SO" ,
					O."MA_HANG_ID" ,
					I."MA" AS "MA_HANG" ,
					I."TEN" AS "TEN_HANG" ,
					O."KHO_ID" ,
					O."DVT_ID" ,
					U."DON_VI_TINH" AS "TEN_DVT",
					coalesce(O."SO_LUONG",0) AS "SO_LUONG",
					O."DON_GIA" ,
					O."GIA_TRI_TON" ,
					O."HAN_SU_DUNG" ,
					O."SO_LO" ,
					O."DVT_CHINH_ID" ,
					O."DON_GIA_THEO_DVT_CHINH" ,
					O."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH" ,
					O."SO_LUONG_THEO_DVT_CHINH" ,
					O."TOAN_TU_QUY_DOI" ,
					O."CHI_NHANH_ID" ,
					O."STT" ,
					O."THU_TU_CHUNG_TU" ,
			--         O.InventoryResaleTypeID,
					S."MA_KHO",
			--         I.InventoryItemCategoryName,
					I."LIST_NHOM_VTHH",
					I."THEO_DOI_THEO_MA_QUY_CACH"
			FROM    account_ex_ton_kho_vat_tu_hang_hoa O
					INNER JOIN danh_muc_vat_tu_hang_hoa I ON O."MA_HANG_ID" = I.id
					LEFT JOIN danh_muc_to_chuc AS OU ON O."CHI_NHANH_ID" = OU.id
					LEFT JOIN danh_muc_don_vi_tinh AS U ON O."DVT_ID" = U.id
					LEFT JOIN danh_muc_kho AS S ON O."KHO_ID" = S.id
			WHERE(O."KHO_ID" = tham_so_kho_id OR tham_so_kho_id = -1)
					AND ( ( tham_so_chi_nhanh IS NULL
							AND "HACH_TOAN_SELECTION" = 'PHU_THUOC'
						)
						OR ( tham_so_chi_nhanh IS NOT NULL
							AND O."CHI_NHANH_ID" = tham_so_chi_nhanh
							)
						)
			ORDER BY
			CASE tham_so_la_chi_tiet WHEN 0 THEN I.id	ELSE NULL END ,
					CASE tham_so_la_chi_tiet WHEN 0 THEN U.id			ELSE NULL END,
					O."THU_TU_CHUNG_TU", -- KDCHIEN 27.07.2018:243107: Bỏ sort trên giao diện thì phải Sort dưới store
					O."STT"; --bndinh 23/12/2015: sửa lỗi 83466, sắp xếp trên danh sách số dư theo RefOrder trước
			ELSE

					DROP TABLE IF EXISTS TMP_KET_QUA;
			CREATE TEMP TABLE TMP_KET_QUA
			AS
			SELECT
			O.id AS "ID_CHUNG_TU" ,
			O."LOAI_CHUNG_TU" ,
					O."NGAY_HACH_TOAN" ,
					O."SO_CHUNG_TU" ,
					o.state AS "TRANG_THAI_GHI_SO" ,
					O."MA_HANG_ID" ,
					I."MA" AS "MA_HANG" ,
					I."TEN" AS "TEN_HANG" ,
					O."KHO_ID" ,
					O."DVT_ID" ,
					U."DON_VI_TINH" AS "TEN_DVT",
					coalesce(O."SO_LUONG",0) AS "SO_LUONG",
					O."DON_GIA" ,
					O."GIA_TRI_TON" ,
					O."HAN_SU_DUNG" ,
					O."SO_LO" ,
					O."DVT_CHINH_ID" ,
					O."DON_GIA_THEO_DVT_CHINH" ,
					O."TY_LE_CHUYEN_DOI_THEO_DVT_CHINH" ,
					O."SO_LUONG_THEO_DVT_CHINH" ,
					O."TOAN_TU_QUY_DOI" ,
					O."CHI_NHANH_ID" ,
					O."STT" ,
					O."THU_TU_CHUNG_TU" ,
			--         O.InventoryResaleTypeID,
					S."MA_KHO",
			--         I.InventoryItemCategoryName,
					I."LIST_NHOM_VTHH",
					I."THEO_DOI_THEO_MA_QUY_CACH"
			FROM    account_ex_ton_kho_vat_tu_hang_hoa O
					INNER JOIN danh_muc_vat_tu_hang_hoa I ON O."MA_HANG_ID" = I.id
					LEFT JOIN danh_muc_to_chuc AS OU ON o."CHI_NHANH_ID" = OU.id
					LEFT JOIN danh_muc_don_vi_tinh AS U ON O."DVT_ID" = U.id
					LEFT JOIN danh_muc_kho AS S ON O."KHO_ID" = S.id
			WHERE   (O."KHO_ID" = tham_so_kho_id OR tham_so_kho_id = -1)
					AND ( ( tham_so_chi_nhanh IS NULL
							AND "HACH_TOAN_SELECTION" = 'PHU_THUOC'
						)
						OR ( tham_so_chi_nhanh IS NOT NULL
							AND O."CHI_NHANH_ID" = tham_so_chi_nhanh
							)
						)
			ORDER BY
			CASE tham_so_la_chi_tiet WHEN 0 THEN "NGAY_HACH_TOAN"			ELSE NULL END ,
					CASE tham_so_la_chi_tiet WHEN 0 THEN "SO_CHUNG_TU"			ELSE NULL END , --kdchien 26/12/2015:83699:Sắp xếp theo số chứng từ nữa
					CASE tham_so_la_chi_tiet WHEN 0 THEN I."MA"	ELSE NULL END ,
					CASE tham_so_la_chi_tiet WHEN 0 THEN U."DON_VI_TINH"			ELSE NULL END ,
					"THU_TU_CHUNG_TU",-- KDCHIEN 27.07.2018:243107: Bỏ sort trên giao diện thì phải Sort dưới store
					"STT"; --bndinh 23/12/2015: sửa lỗi 83466, sắp xếp trên danh sách số dư theo RefOrder trước
END IF;

END $$;

SELECT *FROM TMP_KET_QUA


		"""  
		record = self.execute(query, params)
		
		return record