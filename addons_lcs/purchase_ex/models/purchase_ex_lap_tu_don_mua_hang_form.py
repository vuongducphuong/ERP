# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class PURCHASE_EX_LAP_TU_DON_MUA_HANG_FORM(models.Model):
	_name = 'purchase.ex.lap.tu.don.mua.hang.form'
	_description = ''
	_auto = False

	SO_DON_HANG_ID = fields.Many2one('purchase.ex.don.mua.hang', string='Số đơn hàng', help='Số đơn hàng')
	NHA_CUNG_CAP_ID = fields.Many2one('res.partner', string='Nhà cung cấp', help='Nhà cung cấp')
	KHOANG_THOI_GIAN = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Khoảng thời gian', help='Khoảng thời gian', default='DAU_THANG_DEN_HIEN_TAI',required=True)
	TU_NGAY = fields.Date(string='Từ', help='Từ ngày',default=fields.Datetime.now)
	DEN_NGAY = fields.Date(string='Đến', help='Đến ngày',default=fields.Datetime.now)

	NHA_CUNG_CAP_ID_VIEW = fields.Many2one('res.partner', string='Nhà cung cấp', help='Nhà cung cấp')
  
	
	PURCHASE_EX_LAP_TU_DON_MUA_HANG_CHI_TIET_IDS = fields.One2many('purchase.ex.lap.tu.don.mua.hang.chi.tiet', 'CHI_TIET_ID', string='Lập từ đơn mua hàng chi tiết ')

	# def default_get(self, fields_list):
	#   result = super(PURCHASE_EX_LAP_TU_DON_MUA_HANG_FORM, self).default_get(fields_list)
	#   result['SO_DON_HANG_ID'] = self.env['purchase.ex.don.mua.hang'].search([],limit=1).id
	#   result['NHA_CUNG_CAP_ID'] = self.env['res.partner'].search([],limit=1).id
	#   return result

	@api.onchange('KHOANG_THOI_GIAN')
	def _cap_nhat_ngay(self):
		self.onchange_time(self.KHOANG_THOI_GIAN, 'TU_NGAY', 'DEN_NGAY')

	@api.model
	def thuc_hien_lay_du_lieu_cac_chung_tu(self, args):
		new_line = [[5]]
		nha_cung_cap_id = 0
		ma_nha_cung_cap = ''
		so_don_hang_id = 0
		loai_chung_tu_mua_hang = args.get('loai_chung_tu_mua_hang')
		loai_tien_ct_mua_hang = args.get('loai_tien_ct_mua_hang').get('display_name')
		param ={}
		tham_so = ''
		query_dieu_kien = """"""
		if 'nha_cung_cap_id' in args:
			param = {
			'DOI_TUONG_ID': args['nha_cung_cap_id'],
			'TU_NGAY': args['tu_ngay'],
			'DEN_NGAY': args['den_ngay'],
			'CHI_NHANH_ID' : self.get_chi_nhanh(),
			}
			nha_cung_cap_id = args['nha_cung_cap_id']
			if nha_cung_cap_id:
				ma_nha_cung_cap = self.env['res.partner'].search([('id', '=', nha_cung_cap_id)],limit=1).name

			tham_so = """  
					tham_so_doi_tuong INTEGER:= %(DOI_TUONG_ID)s;
					tham_so_tu_ngay DATE:=%(TU_NGAY)s;
					tham_so_den_ngay DATE :=%(DEN_NGAY)s;
					tham_so_chi_nhanh INTEGER:= %(CHI_NHANH_ID)s;
			"""

			query_dieu_kien = """WHERE PO."NHA_CUNG_CAP_ID" = tham_so_doi_tuong
						AND PO."NGAY_DON_HANG" BETWEEN tham_so_tu_ngay AND tham_so_den_ngay
						AND (( POD."SO_LUONG" > POD."SO_LUONG_NHAN"
						OR ( POD."SO_LUONG" = 0
						AND POD.id NOT IN (
						SELECT   "CHI_TIET_DON_MUA_HANG_ID"
						FROM     purchase_document_line
						WHERE    "CHI_TIET_DON_MUA_HANG_ID" IS NOT NULL )
						)

						)OR PVD.order_id = tham_so_id_chung_tu
						)
						AND PO."CHI_NHANH_ID" = tham_so_chi_nhanh """
		else:
			
			param = {
			'SO_DON_HANG_ID': args['so_don_hang_id'],
			}



			nha_cung_cap = self.env['purchase.ex.don.mua.hang'].search([('id', '=', args['so_don_hang_id'])],limit=1).NHA_CUNG_CAP_ID
			if nha_cung_cap:
				nha_cung_cap_id = nha_cung_cap.id
				ma_nha_cung_cap = nha_cung_cap.name


			tham_so = """  
					tham_so_id_don_mua_hang INTEGER:=%(SO_DON_HANG_ID)s;
					"""

			query_dieu_kien = """WHERE PO.id = tham_so_id_don_mua_hang"""        

		record =[]
		query = """ 
		DO LANGUAGE plpgsql $$
		DECLARE
		tham_so_id_chung_tu INTEGER:= 1;--   ở form đơn mua hàng có 1 trường liên kết ngầm đến chứng từ mua hàng (nếu k tìm được thì ghi lại)
		"""+tham_so+"""
		
		BEGIN
		DROP TABLE IF EXISTS TMP_KET_QUA;
		CREATE TEMP TABLE TMP_KET_QUA
		AS
		SELECT DISTINCT
		PO.id AS "DON_MUA_HANG_ID",
		POD.id AS "DON_MUA_HANG_CHI_TIET_ID",
		PO."NGAY_DON_HANG" ,
		PO."SO_DON_HANG",
		POD."MA_HANG_ID" ,
		POD."DVT_ID",
		II.name AS "TEN_HANG",
		POD."SO_LUONG" - POD."SO_LUONG_NHAN" + SUM(CASE WHEN PVD.order_id = tham_so_id_chung_tu THEN coalesce(PVD."SO_LUONG",0) ELSE 0 END) AS "SO_LUONG_CHUA_NHAN",
		POD."DON_GIA",
		POD."SO_LUONG" - POD."SO_LUONG_NHAN" + SUM(CASE WHEN PVD.order_id = tham_so_id_chung_tu THEN coalesce(PVD."SO_LUONG",0) ELSE 0 END) AS "SO_LUONG_NHAN"
		FROM    purchase_ex_don_mua_hang PO
		INNER JOIN purchase_ex_don_mua_hang_chi_tiet POD ON PO.id = POD."DON_MUA_HANG_CHI_TIET_ID"
		LEFT JOIN purchase_document_line PVD ON POD.id = PVD."CHI_TIET_DON_MUA_HANG_ID"
		--         LEFT JOIN res_partner AO ON AO.id = PO."NHA_CUNG_CAP_ID"
		INNER JOIN danh_muc_vat_tu_hang_hoa II ON POD."MA_HANG_ID" = II.id
		--         LEFT JOIN purchase_ex_hop_dong_mua_hang PCT ON POD."HOP_DONG_MUA_ID"=PCT.id
		--         LEFT JOIN danh_muc_hop_dong_mua CT ON POD."HOP_DONG_MUA_ID" = CT.id
		--         LEFT JOIN sale_ex_don_dat_hang SA ON POD."DON_DAT_HANG_ID" = SA.id
		--         LEFT JOIN stock_ex_lenh_san_xuat AS IPO ON POD."LENH_SAN_XUAT_ID" = IPO.id
		--         LEFT JOIN stock_ex_lenh_san_xuat_chi_tiet_thanh_pham AS IPOP ON POD."LENH_SAN_XUAT_CHI_TIET_ID" = IPOP.id
		--         LEFT JOIN danh_muc_vat_tu_hang_hoa AS II2 ON IPOP."MA_HANG_ID" = II2.id
		-- ntquang 25/12/2017 - CR 155560 - bổ sung tên công trình
		--         LEFT JOIN danh_muc_cong_trinh AS PW ON PW.id = POD."CONG_TRINH_ID"
		
		"""+query_dieu_kien+"""
		
		GROUP BY
		PO.id,
		POD.id,
		PO."NGAY_DON_HANG" ,
		PO."SO_DON_HANG",
		POD."MA_HANG_ID" ,
		II.name,
		POD."DON_GIA",
		POD."SO_LUONG",
		POD."SO_LUONG_NHAN"
		ORDER BY PO."NGAY_DON_HANG" DESC;
		END $$;

		SELECT *FROM TMP_KET_QUA;

		""" 

		record = self.execute(query, param)
		for line in record:
			
			hang = self.env['danh.muc.vat.tu.hang.hoa'].search([('id', '=', line.get('MA_HANG_ID'))],limit=1)
			ten_hang = hang.TEN
			thanh_tien = line.get('DON_GIA') * line.get('SO_LUONG_NHAN')
			# tai_khoan_ngam_dinh = self.env['purchase.document.line'].lay_tai_khoan_ngam_dinh(loai_chung_tu_mua_hang, 0, loai_tien_ct_mua_hang!='VND')
			# tk_no = tai_khoan_ngam_dinh.get('TK_NO_ID')
			# if loai_chung_tu_mua_hang in (307,308,309,310,319,320,321,322):
			# 	tk_no = hang.TAI_KHOAN_KHO_ID.id
			
			new_line += [(0,0,{
				'NGAY_DON_HANG' : line.get('NGAY_DON_HANG'),
				'SO_DON_HANG' : line.get('SO_DON_HANG'),
				'MA_HANG' : [line.get('MA_HANG_ID'),hang.MA],
				'TEN_HANG' : ten_hang,
				'DVT_ID' : line.get('DVT_ID'),
				'SO_LUONG_CHUA_NHAN' : line.get('SO_LUONG'),
				'DON_GIA' : line.get('DON_GIA'),
				'THANH_TIEN' :thanh_tien,
				'SO_LUONG_NHAN' : line.get('SO_LUONG_NHAN'),
				'DOI_TUONG_ID' : [nha_cung_cap_id,ma_nha_cung_cap],
				'DON_MUA_HANG_ID' : [line.get('DON_MUA_HANG_ID'),line.get('SO_DON_HANG')],
				# 'KHO_ID' : hang.KHO_NGAM_DINH_ID.id,
				# 'TK_KHO_ID' : tk_kho,
				# 'TK_CO_ID' : tai_khoan_ngam_dinh.get('TK_CO_ID'),
				# 'TK_NO_ID' : tk_no,
				# 'TK_THUE_GTGT_ID' : tai_khoan_ngam_dinh.get('TK_THUE_GTGT_ID'),
				# 'DON_MUA_HANG_CHI_TIET_ID' : [line.get('DON_MUA_HANG_CHI_TIET_ID'),'line'],
				'ID_DON_MUA_HANG_CT' : line.get('DON_MUA_HANG_CHI_TIET_ID'),
				})] 
		return new_line



