# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class PURCHASE_EX_CHON_TU_LENH_SAN_XUAT_FORM(models.Model):
	_name = 'purchase.ex.chon.tu.lenh.san.xuat.form'
	_description = ''
	_auto = False

	KHOANG_THOI_GIAN = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Khoảng thời gian', help='Khoảng thời gian', default='DAU_THANG_DEN_HIEN_TAI',required=True)
	TU_NGAY = fields.Date(string='Từ', help='Từ ngày',default=fields.Datetime.now)
	DEN_NGAY = fields.Date(string='Đến', help='Đến ngày',default=fields.Datetime.now)
	
	@api.onchange('KHOANG_THOI_GIAN')
	def _cap_nhat_ngay(self):
		self.onchange_time(self.KHOANG_THOI_GIAN, 'TU_NGAY', 'DEN_NGAY')
	#FIELD_IDS = fields.One2many('model.name')
	#@api.model
	#def default_get(self, fields_list):
	#   result = super(PURCHASE_EX_CHON_TU_LENH_SAN_XUAT_FORM, self).default_get(fields_list)
	#   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
	#   return result
	PURCHASE_EX_CHON_TU_LENH_SAN_XUAT_FORM_CHI_TIET_IDS = fields.One2many('purchase.ex.chon.tu.lenh.san.xuat.form.chi.tiet', 'CHI_TIET_ID', string='Chọn từ lệnh sản xuất form chi tiết')


	@api.model
	def thuc_hien_lay_du_lieu_cac_chung_tu(self, args):
		new_line = [[5]]
		# param ={}
		record =[]
		# query = """ 
		
		# """ 

		# record = self.execute(query, param)
		# for line in record:
		new_line += [(0,0,{'ID_THANH_PHAM':40,
			'SO' : 'LSX004',
			'NGAY' : '10-1-2018',
			'DA_LAP_DU_PX' :True,
			'DIEN_GIAI' : '',
			'MA_THANH_PHAM_ID' :'AO_SOMI_NAM',
			'TEN_THANH_PHAM' : 'Áo sơ mi nam',
			'SO_LUONG' :200,
			'SO_LUONG_SAN_XUAT' : 200,})] 
			
		new_line += [(0,0,{
			'ID_THANH_PHAM':51,
			'SO' : 'LSX004',
			'NGAY' : '10-1-2018',
			'DA_LAP_DU_PX' :True,
			'DIEN_GIAI' : '',
			'MA_THANH_PHAM_ID' :'AO_SOMI_NU',
			'TEN_THANH_PHAM' : 'Áo sơ mi nữ',
			'SO_LUONG' :200,
			'SO_LUONG_SAN_XUAT' : 200,})] 
		return new_line

	@api.model
	def thuc_hien_lay_chi_tiet_thanh_pham(self, args):
		danh_sach_chi_tiet_cau_thanh_thanh_pham = [[5]]
		if 'id_thanh_pham_list' in args:
			for i in args['id_thanh_pham_list']:
				id_thanh_pham = self.env['stock.ex.lenh.san.xuat.chi.tiet.thanh.pham'].search([('id', '=', i)],limit=1).MA_HANG_ID.id
				ma_thanh_pham = self.env['stock.ex.lenh.san.xuat.chi.tiet.thanh.pham'].search([('id', '=', i)],limit=1).MA_HANG_ID.MA
				id_lenh_san_xuat = 0
				so_lenh_san_xuat = ''
				lenh_san_xuat = self.env['stock.ex.lenh.san.xuat.chi.tiet.thanh.pham'].search([('id', '=', i)],limit=1).LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID
				if lenh_san_xuat:
					id_lenh_san_xuat = lenh_san_xuat.id
					so_lenh_san_xuat = lenh_san_xuat.SO_LENH
				danh_sach_chi_tiet_list = self.env['stock.ex.thanh.pham.chi.tiet.dinh.muc.xuat.nvl'].search([('THANH_PHAM_CHI_TIET_DINH_MUC_XUAT_NVL_ID', '=', i)]) 
				for line in danh_sach_chi_tiet_list :
					don_gia = 0
					thanh_tien = 0
					phan_tram_thue_id = 0
					phan_tram_thue_name = ''
					dien_giai_thue =''
					tien_thue_gtgt = 0
					if line.MA_HANG_ID:
						dien_giai_thue = 'Thuế GTGT - ' + str(line.MA_HANG_ID.TEN)
						don_gia = line.MA_HANG_ID.DON_GIA_BAN
						thanh_tien = don_gia * line.SO_LUONG_NVL
						thue_gtgt = line.MA_HANG_ID.THUE_SUAT_GTGT_ID
						if thue_gtgt:
							phan_tram_thue_id = thue_gtgt.id
							phan_tram_thue_name = thue_gtgt.name
							tien_thue_gtgt = (thue_gtgt.PHAN_TRAM_THUE_GTGT * thanh_tien) / 100
					danh_sach_chi_tiet_cau_thanh_thanh_pham += [(0,0,{
						'MA_HANG_ID':[line.MA_HANG_ID.id , line.MA_HANG_ID.MA],
						'name': line.TEN_NGUYEN_VAT_LIEU,
						'DVT_ID':[line.DVT_ID.id , line.DVT_ID.DON_VI_TINH],
						'SO_LUONG':line.SO_LUONG_NVL,
						'DON_GIA':don_gia,
						'THANH_TIEN':thanh_tien,
						'GIA_TRI_NHAP_KHO':thanh_tien,
						'LENH_SAN_XUAT_ID':[id_lenh_san_xuat, so_lenh_san_xuat],
						'THANH_PHAM_ID':[id_thanh_pham, ma_thanh_pham],
						'THUE_GTGT_ID':[phan_tram_thue_id, phan_tram_thue_name],
						'TIEN_THUE_GTGT':tien_thue_gtgt,
					})]
		return danh_sach_chi_tiet_cau_thanh_thanh_pham