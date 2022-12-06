# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.tools.float_utils import float_round

class GIA_THANH_TINH_GIA_THANH(models.Model):
	_name = 'gia.thanh.tinh.gia.thanh'
	_description = 'Tính giá thành'
	# _auto = False

	KY_TINH_GIA_THANH = fields.Char(string='Kỳ tính giá thành', help='Kỳ tính giá thành')
	MUC_DANH_GIA_DO_DANG = fields.Selection([('HOAN_THANH_TUONG_DUONG', 'Sản phẩm hoàn thành tương đương'), ('NGUYEN_VAT_LIEU_TRUC_TIEP', 'Theo nguyên vật liệu trực tiếp'), ('DINH_MUC', 'Theo định mức'), ], string='Mức đánh giá dở dang', help='Mức đánh giá dở dang',default='HOAN_THANH_TUONG_DUONG')
	HANG_MUC = fields.Selection([('PHAN_BO_CP_CHUNG', 'Phân bổ chi phí chung'), ('DANH_GIA_DO_DANG', 'Đánh giá dở dang'), ('XD_TY_LE_PHAN_BO', 'Xác định tỷ lệ phân bổ'), ('TINH_GIA_THANH', 'Tính giá thành'), ], string='Hạng mục', help='Hạng mục',default ='PHAN_BO_CP_CHUNG')
	LOAI_TINH_GIA_THANH = fields.Selection([('HE_SO_TY_LE', 'Hệ số tỷ lệ'), ('GIAN_DON', 'Giản đơn'), ('CONG_TRINH', 'Công trình'), ('DON_HANG', 'Đơn hàng'), ('HOP_DONG', 'Hợp đồng') ], string='Loại tính giá thành', help='Loại tính giá thành')
	#FIELD_IDS = fields.One2many('model.name') 
	# @api.model
	# def default_get(self, fields_list):
	#   result = super(GIA_THANH_TINH_GIA_THANH, self).default_get(fields_list)
	#   result['HANG_MUC'] = 'PHAN_BO_CP_CHUNG'
	#   return result
	GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS = fields.One2many('gia.thanh.xac.dinh.chi.phi.phan.bo.chi.tiet', 'CHI_TIET_ID', string='xác định chi phí phân bổ chi tiết')
	GIA_THANH_BANG_GIA_THANH_CHI_TIET_IDS = fields.One2many('gia.thanh.bang.gia.thanh.chi.tiet', 'CHI_TIET_ID', string='Bảng giá thành chi tiết')
	GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS = fields.One2many('gia.thanh.xac.dinh.do.dang.chi.tiet', 'CHI_TIET_ID', string='Xác định dở dang chi tiết')
	GIA_THANH_KET_QUA_CHI_PHI_DO_DANG_CUOI_KY_CHI_TIET_IDS = fields.One2many('gia.thanh.ket.qua.chi.phi.do.dang.cuoi.ky.chi.tiet', 'CHI_TIET_ID', string='Kết quả chi phí dở dang cuối kỳ chi tiết')
	GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS = fields.One2many('gia.thanh.ket.qua.phan.bo.chi.tiet', 'CHI_TIET_ID', string='Kết quả phân bổ chi tiết')
	GIA_THANH_CHI_TIET_CHUNG_TU_PHAN_BO_CHI_PHI_CHUNG_IDS = fields.One2many('gia.thanh.chi.tiet.chung.tu.phan.bo.chi.phi.chung', 'CHI_TIET_ID', string='Kết quả phân bổ chi tiết')

	GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS = fields.One2many('gia.thanh.xdtlpb.doi.tuong.tinh.gia.thanh.chi.tiet', 'CHI_TIET_ID', string='Xác định tỷ lệ phân bổ đối tượng tính giá thành chi tiết')
	GIA_THANH_TY_LE_PHAN_BO_DOI_TUONG_THCP_CHI_TIET_IDS = fields.One2many('gia.thanh.ty.le.phan.bo.doi.tuong.thcp.chi.tiet', 'CHI_TIET_ID', string='Tỷ lệ phân bổ đối tượng THCP chi tiết')

	TONG_SO_LUONG_THANH_PHAM_CHUAN = fields.Float(string='Tổng số lượng thành phầm chuẩn ở tab đối tượng tính giá thành', help='Tổng số lượng thành phầm chuẩn ở tab đối tượng tính giá thành',compute='tinh_ty_le_phan_bo_gia_thanh', store=False )
	PHUONG_PHAP_XAC_DINH = fields.Selection([('HE_SO', 'Hệ số'), ('TY_LE', ' Tỷ lệ'), ], string='Phương pháp xác định', help='Phương pháp xác định',default='HE_SO') 
	
	TONG_SO_DA_PHAN_BO_TK6271 = fields.Float(compute='tinh_tong_tien_so_phan_bo',store=True,)
	TONG_SO_DA_PHAN_BO_TK621 = fields.Float(compute='tinh_tong_tien_so_phan_bo',store=True,)
	TONG_SO_DA_PHAN_BO_TK6277 = fields.Float(compute='tinh_tong_tien_so_phan_bo',store=True,)

	TONG_SO_CHI_PHI = fields.Float(string='Tổng chi phí', compute='tinh_tong_chi_phi',store=True, )
	TONG_SO_DA_PHAN_BO = fields.Float(string='Tổng số đã phân bổ', compute='tinh_tong_tong_so_da_phan_bo',store=True, )

	KY_TINH_GIA_THANH_ONCHANGE = fields.Integer(store=False, )
	# KY_TINH_GIA_THANH_ONCHANGE_TINH_CPDD = fields.Integer(store=False, ) 
	ONCHANGE_CLICK_PHAN_BO = fields.Integer(store=False, )
	ONCHANGE_CLICK_TINH_CP_DD = fields.Integer(store=False, )
	ONCHANGE_CLICK_LAY_GIA_THANH_DINH_MUC = fields.Integer(store=False, )
	ONCHANGE_CLICK_TINH_GIA_THANH = fields.Integer(store=False, ) 
	ONCHANGE_CLICK_CAP_NHAT_GIA_NHAP_KHO = fields.Integer(store=False, ) 
	ONCHANGE_CLICK_CAP_NHAT_GIA_XUAT_KHO = fields.Integer(store=False, )
	TU_NGAY = fields.Date(store=False,)
	DEN_NGAY = fields.Date(store=False,) 
	CHE_DO_KE_TOAN = fields.Char(string='Chế độ kế toán', help='Chế độ kế toán')

	KY_TINH_GIA_THANH_CHI_TIET_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh.chi.tiet', string='Kỳ tính giá thành chi tiết', help='Kỳ tính giá thành chi tiết')


	@api.model
	def default_get(self, fields):
		rec = super(GIA_THANH_TINH_GIA_THANH, self).default_get(fields)
		rec['CHE_DO_KE_TOAN'] = self.env['ir.config_parameter'].get_param('he_thong.CHE_DO_KE_TOAN')
		return rec


	@api.depends('GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS')
	def tinh_tong_tien_so_phan_bo(self):
		tong_so_da_phan_bo_6271 = 0
		tong_so_da_phan_bo_621 = 0
		tong_so_da_phan_bo_6277 = 0
		for order in self:
			for line in order.GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS:
				tk_id = None
				if line.TAI_KHOAN_ID:
					tk_id = line.TAI_KHOAN_ID.id
				tai_khoan_id = self.env['danh.muc.he.thong.tai.khoan'].search([('id', '=', tk_id)],limit = 1)
				ten_tai_khoan = None
				if tai_khoan_id:
					ten_tai_khoan = tai_khoan_id.SO_TAI_KHOAN
				if ten_tai_khoan == '6271':
					tong_so_da_phan_bo_6271 =line.SO_PHAN_BO_LAN_NAY
				elif ten_tai_khoan == '621':
					tong_so_da_phan_bo_621 =line.SO_PHAN_BO_LAN_NAY
				elif ten_tai_khoan == '6277':
					tong_so_da_phan_bo_6277 =line.SO_PHAN_BO_LAN_NAY
			order.update({
                'TONG_SO_DA_PHAN_BO_TK6271':tong_so_da_phan_bo_6271,
                'TONG_SO_DA_PHAN_BO_TK621':tong_so_da_phan_bo_621,
                'TONG_SO_DA_PHAN_BO_TK6277':tong_so_da_phan_bo_6277,
            })
	
	@api.depends('GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS')
	def tinh_tong_chi_phi(self):
		tong_so_chi_phi = 0
		for order in self:
			for line in order.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
				tong_so_chi_phi +=line.TONG_CHI_PHI
			order.update({
                'TONG_SO_CHI_PHI':tong_so_chi_phi,
            })

	@api.depends('GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS')
	def tinh_tong_tong_so_da_phan_bo(self):
		tong_tong_so_da_phan_bo = 0
		for order in self:
			for line in order.GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS:
				tong_tong_so_da_phan_bo +=line.SO_PHAN_BO_LAN_NAY
			order.update({
                'TONG_SO_DA_PHAN_BO':tong_tong_so_da_phan_bo,
            })

	

	def lay_du_lieu_tinh_gia_thanh_sx_lien_tuc(self, args):
		new_line_xac_dinh_chi_phi_phan_bo = [[5]]
		new_line_ket_qua_phan_bo = [[5]]
		new_line_xac_dinh_do_dang = [[5]]
		new_line_ket_qua_chi_phi_do_dang_cuoi_ky = [[5]]
		new_line_doi_tuong_thcp = [[5]]
		new_line_xac_dinh_ty_le_phan_bo = [[5]]
		new_line_chi_tiet_chung_tu_phan_bo_chi_phi_chung = [[5]]

		ky_tinh_gia_thanh_id = self.KY_TINH_GIA_THANH_ONCHANGE
		chi_nhanh_id = self.get_chi_nhanh()
		du_lieu_xac_dinh_chi_phi_phan_bo = self.lay_du_lieu_xac_dinh_chi_phi_phan_bo(ky_tinh_gia_thanh_id,chi_nhanh_id)
		du_lieu_xac_dinh_chi_phi_phan_bo_ct_dh_hd = self.lay_du_lieu_xac_dinh_chi_phi_phan_bo_ct_dh_hd(ky_tinh_gia_thanh_id,chi_nhanh_id)
		du_lieu_ket_qua_phan_bo = self.lay_du_lieu_ket_qua_phan_bo(ky_tinh_gia_thanh_id)
		du_lieu_xac_dinh_do_dang = self.lay_du_lieu_xac_dinh_do_dang(ky_tinh_gia_thanh_id)
		# xd_ty_le_pb_doi_tuong_thcp_ids = self.lay_du_lieu_doi_tuong_thcp(ky_tinh_gia_thanh_id)
		
		du_lieu_xac_dinh_do_dang_da_luu = self.lay_du_lieu_xac_dinh_do_dang_da_luu(ky_tinh_gia_thanh_id)


		

		arr_dtthcp = []
		arr_cong_trinh = []
		arr_don_hang = []
		arr_hop_dong = []
		doi_tuong_thcp_ids = self.env['gia.thanh.ky.tinh.gia.thanh.chi.tiet'].search([('KY_TINH_GIA_THANH_ID', '=', ky_tinh_gia_thanh_id)])
		if doi_tuong_thcp_ids:
			for dtthcp in doi_tuong_thcp_ids:
				arr_dtthcp.append((4,dtthcp.MA_DOI_TUONG_THCP_ID.id)) 
				arr_hop_dong.append((4,dtthcp.SO_HOP_DONG_ID.id)) 
				arr_cong_trinh.append((4,dtthcp.MA_CONG_TRINH_ID.id)) 
				arr_don_hang.append((4,dtthcp.SO_DON_HANG_ID.id)) 

		dict_tai_khoan_so_tien_phan_bo = {}
		arr_tai_khoan = []

		du_lieu_xac_dinh_phan_bo_da_luu_ids = self.env['gia.thanh.xac.dinh.chi.phi.phan.bo.chi.tiet'].search([('KY_TINH_GIA_THANH_ID', '=', self.KY_TINH_GIA_THANH_ONCHANGE)])
		if du_lieu_xac_dinh_phan_bo_da_luu_ids:
			for chi_phi_pb in du_lieu_xac_dinh_phan_bo_da_luu_ids:
				new_line_xac_dinh_chi_phi_phan_bo += [(0,0,{
							'TAI_KHOAN_ID' : [chi_phi_pb.TAI_KHOAN_ID.id,chi_phi_pb.TAI_KHOAN_ID.SO_TAI_KHOAN],
							'TEN_TAI_KHOAN' : chi_phi_pb.TEN_TAI_KHOAN,
							'KHOAN_MUC_CP_ID' : [chi_phi_pb.KHOAN_MUC_CP_ID.id,chi_phi_pb.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP],
							'TEN_KHOAN_MUC_CP' : chi_phi_pb.TEN_KHOAN_MUC_CP,
							'TONG_SO_TIEN' : chi_phi_pb.TONG_SO_TIEN,
							'SO_CHUA_PHAN_BO' : chi_phi_pb.SO_CHUA_PHAN_BO,
							'PHAN_TRAM_PB_LAN_NAY' : chi_phi_pb.PHAN_TRAM_PB_LAN_NAY,
							'SO_PHAN_BO_LAN_NAY' : chi_phi_pb.SO_PHAN_BO_LAN_NAY,
							'TIEU_THUC_PHAN_BO' :'NGUYEN_VAT_LIEU',
							'DOI_TUONG_THCP_ID' : arr_dtthcp,
							'CONG_TRINH_ID' : arr_cong_trinh,
							'SO_DON_HANG_ID' : arr_don_hang,
							'HOP_DONG_BAN_ID' : arr_hop_dong,
							'CHI_TIET_CHUNG_TU' : 'Xem',
							})]
				# if self.LOAI_TINH_GIA_THANH in ('HE_SO_TY_LE','GIAN_DON'):
				# 	arr_tai_khoan.append(chi_phi_pb.TAI_KHOAN_ID.SO_TAI_KHOAN)
				# else:
				# 	arr_tai_khoan.append(chi_phi_pb.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP)

				if self.CHE_DO_KE_TOAN == '15':
					key = chi_phi_pb.TAI_KHOAN_ID.id
					arr_tai_khoan.append(chi_phi_pb.TAI_KHOAN_ID.SO_TAI_KHOAN)
				else:
					key = chi_phi_pb.KHOAN_MUC_CP_ID.id
					arr_tai_khoan.append(chi_phi_pb.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP)
				
				if key not in dict_tai_khoan_so_tien_phan_bo:
					dict_tai_khoan_so_tien_phan_bo[key] = {'TONG_TIEN_PHAN_BO_LAN_NAY' : 0,'PHAN_TRAM_PHAN_BO' : chi_phi_pb.PHAN_TRAM_PB_LAN_NAY}
				dict_tai_khoan_so_tien_phan_bo[key]['TONG_TIEN_PHAN_BO_LAN_NAY'] += chi_phi_pb.SO_PHAN_BO_LAN_NAY
		else:
			if self.LOAI_TINH_GIA_THANH in ('HE_SO_TY_LE','GIAN_DON'):
				if du_lieu_xac_dinh_chi_phi_phan_bo:
					for chi_phi_pb in du_lieu_xac_dinh_chi_phi_phan_bo:
						new_line_xac_dinh_chi_phi_phan_bo += [(0,0,{
									'TAI_KHOAN_ID' : [chi_phi_pb.get('ID_TAI_KHOAN'),chi_phi_pb.get('MA_TAI_KHOAN')],
									'TEN_TAI_KHOAN' : chi_phi_pb.get('TEN_TAI_KHOAN'),
									'KHOAN_MUC_CP_ID' : [chi_phi_pb.get('ID_TAI_KHOAN'),chi_phi_pb.get('MA_TAI_KHOAN')],
									'TEN_KHOAN_MUC_CP' : chi_phi_pb.get('TEN_TAI_KHOAN'),
									'TONG_SO_TIEN' : chi_phi_pb.get('TONG_SO_TIEN'),
									'SO_CHUA_PHAN_BO' : chi_phi_pb.get('SO_CHUA_PHAN_BO'),
									'PHAN_TRAM_PB_LAN_NAY' : chi_phi_pb.get('TY_LE_PB'),
									# 'PHAN_TRAM_PB_LAN_NAY' : 100,
									'SO_PHAN_BO_LAN_NAY' : chi_phi_pb.get('SO_TIEN_PB_LAN_NAY'),
									# 'SO_PHAN_BO_LAN_NAY' : chi_phi_pb.get('SO_CHUA_PHAN_BO'),
									'TIEU_THUC_PHAN_BO' :'NGUYEN_VAT_LIEU',
									'DOI_TUONG_THCP_ID' : arr_dtthcp,
									'CONG_TRINH_ID' : arr_cong_trinh,
									'SO_DON_HANG_ID' : arr_don_hang,
									'HOP_DONG_BAN_ID' : arr_hop_dong,
									'CHI_TIET_CHUNG_TU' : 'Xem',
									})]
						arr_tai_khoan.append(chi_phi_pb.get('MA_TAI_KHOAN'))
						key = chi_phi_pb.get('ID_TAI_KHOAN')
						if key not in dict_tai_khoan_so_tien_phan_bo:
							dict_tai_khoan_so_tien_phan_bo[key] = {'TONG_TIEN_PHAN_BO_LAN_NAY' : 0,'PHAN_TRAM_PHAN_BO' : chi_phi_pb.get('TY_LE_PB')}
						dict_tai_khoan_so_tien_phan_bo[key]['TONG_TIEN_PHAN_BO_LAN_NAY'] += chi_phi_pb.get('SO_TIEN_PB_LAN_NAY')
			else:
				if du_lieu_xac_dinh_chi_phi_phan_bo_ct_dh_hd:
					for chi_phi_pb in du_lieu_xac_dinh_chi_phi_phan_bo_ct_dh_hd:
						new_line_xac_dinh_chi_phi_phan_bo += [(0,0,{
									'TAI_KHOAN_ID' : [chi_phi_pb.get('TK_KHOAN_MUC_ID'),chi_phi_pb.get('MA_TK_KHOAN_MUC')],
									'TEN_TAI_KHOAN' : chi_phi_pb.get('TEN_TK_KHOAN_MUC'),
									'KHOAN_MUC_CP_ID' : [chi_phi_pb.get('TK_KHOAN_MUC_ID'),chi_phi_pb.get('MA_TK_KHOAN_MUC')],
									'TEN_KHOAN_MUC_CP' : chi_phi_pb.get('TEN_TK_KHOAN_MUC'),
									'TONG_SO_TIEN' : chi_phi_pb.get('TONG_SO_TIEN'),
									'SO_CHUA_PHAN_BO' : chi_phi_pb.get('TONG_SO_TIEN'),
									'PHAN_TRAM_PB_LAN_NAY' : chi_phi_pb.get('TY_LE'),
									# 'PHAN_TRAM_PB_LAN_NAY' : 100,
									'SO_PHAN_BO_LAN_NAY' : chi_phi_pb.get('SO_PHAN_BO_LAN_NAY'),
									# 'SO_PHAN_BO_LAN_NAY' : chi_phi_pb.get('SO_CHUA_PHAN_BO'),
									'TIEU_THUC_PHAN_BO' :'NGUYEN_VAT_LIEU',
									'DOI_TUONG_THCP_ID' : arr_dtthcp,
									'CONG_TRINH_ID' : arr_cong_trinh,
									'SO_DON_HANG_ID' : arr_don_hang,
									'HOP_DONG_BAN_ID' : arr_hop_dong,
									'CHI_TIET_CHUNG_TU' : 'Xem',
									})]
						arr_tai_khoan.append(chi_phi_pb.get('MA_TK_KHOAN_MUC'))
						key = chi_phi_pb.get('TK_KHOAN_MUC_ID')
						if key not in dict_tai_khoan_so_tien_phan_bo:
							dict_tai_khoan_so_tien_phan_bo[key] = {'TONG_TIEN_PHAN_BO_LAN_NAY' : 0,'PHAN_TRAM_PHAN_BO' : chi_phi_pb.get('TY_LE')}
						dict_tai_khoan_so_tien_phan_bo[key]['TONG_TIEN_PHAN_BO_LAN_NAY'] += chi_phi_pb.get('SO_PHAN_BO_LAN_NAY')

		if arr_tai_khoan:
			list_item = tuple(arr_tai_khoan)
			chi_tiet_chung_tu_ids = self.lay_du_lieu_chi_tiet_chung_tu(ky_tinh_gia_thanh_id,chi_nhanh_id,list_item)

			if chi_tiet_chung_tu_ids:
				for chi_tiet in chi_tiet_chung_tu_ids:

					if self.CHE_DO_KE_TOAN == '15':
						key = chi_tiet.get('TK_CONG_NO_ID')
					else:
						key = chi_tiet.get('KHOAN_MUC_CP_ID')
					
					so_tien_phan_bo_lan_nay = 0
					if key in dict_tai_khoan_so_tien_phan_bo:
						# tong_tien_phan_bo = dict_tai_khoan_so_tien_phan_bo[key]
					
						if chi_tiet.get('GIA_TRI_CON_LAI') < dict_tai_khoan_so_tien_phan_bo[key].get('TONG_TIEN_PHAN_BO_LAN_NAY') and chi_tiet.get('GIA_TRI_CON_LAI') > 0:
							so_tien_phan_bo_lan_nay = chi_tiet.get('GIA_TRI_CON_LAI')
							dict_tai_khoan_so_tien_phan_bo[key]['TONG_TIEN_PHAN_BO_LAN_NAY'] = dict_tai_khoan_so_tien_phan_bo[key].get('TONG_TIEN_PHAN_BO_LAN_NAY') - chi_tiet.get('GIA_TRI_CON_LAI')
						else:	
							so_tien_phan_bo_lan_nay = dict_tai_khoan_so_tien_phan_bo[key].get('TONG_TIEN_PHAN_BO_LAN_NAY')
							dict_tai_khoan_so_tien_phan_bo[key]['TONG_TIEN_PHAN_BO_LAN_NAY'] = 0

						if chi_tiet.get('GIA_TRI_CON_LAI') > 0:
							phan_tram_phan_bo = dict_tai_khoan_so_tien_phan_bo[key].get('PHAN_TRAM_PHAN_BO')
						else:
							phan_tram_phan_bo = 0
						new_line_chi_tiet_chung_tu_phan_bo_chi_phi_chung += [(0,0,{
								'NGAY_CHUNG_TU' : chi_tiet.get('NGAY_CHUNG_TU'),
								'SO_CHUNG_TU' : chi_tiet.get('SO_CHUNG_TU'),
								'LOAI_CHUNG_TU' : chi_tiet.get('LOAI_CHUNG_TU'),
								'DIEN_GIAI' : chi_tiet.get('DIEN_GIAI'),
								'TK_CHI_PHI_ID' : [chi_tiet.get('TK_CONG_NO_ID'),chi_tiet.get('TK_CONG_NO')],
								'SO_TIEN' : chi_tiet.get('SO_TIEN'),
								'SO_CHUA_PHAN_BO' : chi_tiet.get('GIA_TRI_CON_LAI'),
								'SO_PHAN_BO_LAN_NAY' : so_tien_phan_bo_lan_nay,
								'TY_LE_PHAN_BO' : phan_tram_phan_bo,
								'ID_GOC' : chi_tiet.get('ID_CHUNG_TU'),
								'MODEL_GOC' : chi_tiet.get('MODEL_CHUNG_TU'),
								'KHOAN_MUC_CP_ID' : chi_tiet.get('KHOAN_MUC_CP_ID'),
								'NGAY_HACH_TOAN' : chi_tiet.get('NGAY_HACH_TOAN'),
								# 'SO_TAI_KHOAN_CON_LAI' : chi_tiet.get('ID_TAI_KHOAN'),
								# 'SO_TAI_KHOAN_TONG_TIEN' : chi_tiet.get('ID_TAI_KHOAN'),
								})]

		# dict_du_lieu_ket_qua_phan_bo_da_luu = {}
		# ket_qua_phan_bo_cp_chung = self.env['gia.thanh.ket.qua.phan.bo.chi.phi.chung'].search([('KY_TINH_GIA_THANH_ID', '=', self.KY_TINH_GIA_THANH_ONCHANGE)])
		# if ket_qua_phan_bo_cp_chung:
		# 	for line in ket_qua_phan_bo_cp_chung:
		# 		key_dtthcp = False
		# 		if self.LOAI_TINH_GIA_THANH in ('HE_SO_TY_LE','GIAN_DON'):
		# 			key_dtthcp = line.MA_DOI_TUONG_THCP_ID.id
		# 		elif self.LOAI_TINH_GIA_THANH == 'CONG_TRINH':
		# 			key_dtthcp = line.MA_CONG_TRINH_ID.id
		# 		elif self.LOAI_TINH_GIA_THANH == 'DON_HANG':
		# 			key_dtthcp = line.SO_DON_HANG_ID.id
		# 		elif self.LOAI_TINH_GIA_THANH == 'HOP_DONG':
		# 			key_dtthcp = line.SO_HOP_DONG_ID.id

				
		# 		if key_dtthcp not in dict_du_lieu_ket_qua_phan_bo_da_luu:
		# 			dict_du_lieu_ket_qua_phan_bo_da_luu[key_dtthcp] = {
		# 				'TY_LE_PHAN_TRAM_621' : 0,
		# 				'SO_TIEN_621' : 0,
		# 				'TY_LE_PHAN_TRAM_622' : 0,
		# 				'SO_TIEN_622' : 0,
		# 				'TY_LE_PHAN_TRAM_6271' : 0,
		# 				'SO_TIEN_6271' : 0,
		# 				'TY_LE_PHAN_TRAM_6272' : 0,
		# 				'SO_TIEN_6272' : 0,
		# 				'TY_LE_PHAN_TRAM_6273' : 0,
		# 				'SO_TIEN_6273' : 0,
		# 				'TY_LE_PHAN_TRAM_6274' : 0,
		# 				'SO_TIEN_6274' : 0,
		# 				'TY_LE_PHAN_TRAM_6277' : 0,
		# 				'SO_TIEN_6277' : 0,
		# 				'TY_LE_PHAN_TRAM_6278' : 0,
		# 				'SO_TIEN_6278' : 0,
		# 			}
		# 		chi_tiet = dict_du_lieu_ket_qua_phan_bo_da_luu[key_dtthcp]
		# 		if line.SO_TAI_KHOAN == '621':
		# 			chi_tiet['TY_LE_PHAN_TRAM_621'] = line.TY_LE
		# 			chi_tiet['SO_TIEN_621'] = line.SO_TIEN
		# 		elif line.SO_TAI_KHOAN == '622':
		# 			chi_tiet['TY_LE_PHAN_TRAM_622'] = line.TY_LE
		# 			chi_tiet['SO_TIEN_622'] = line.SO_TIEN
		# 		elif line.SO_TAI_KHOAN == '6271':
		# 			chi_tiet['TY_LE_PHAN_TRAM_6271'] = line.TY_LE
		# 			chi_tiet['SO_TIEN_6271'] = line.SO_TIEN
		# 		elif line.SO_TAI_KHOAN == '6272':
		# 			chi_tiet['TY_LE_PHAN_TRAM_6272'] = line.TY_LE
		# 			chi_tiet['SO_TIEN_6272'] = line.SO_TIEN
		# 		elif line.SO_TAI_KHOAN == '6273':
		# 			chi_tiet['TY_LE_PHAN_TRAM_6273'] = line.TY_LE
		# 			chi_tiet['SO_TIEN_6273'] = line.SO_TIEN
		# 		elif line.SO_TAI_KHOAN == '6274':
		# 			chi_tiet['TY_LE_PHAN_TRAM_6274'] = line.TY_LE
		# 			chi_tiet['SO_TIEN_6274'] = line.SO_TIEN
		# 		elif line.SO_TAI_KHOAN == '6277':
		# 			chi_tiet['TY_LE_PHAN_TRAM_6277'] = line.TY_LE
		# 			chi_tiet['SO_TIEN_6277'] = line.SO_TIEN
		# 		elif line.SO_TAI_KHOAN == '6278':
		# 			chi_tiet['TY_LE_PHAN_TRAM_6278'] = line.TY_LE
		# 			chi_tiet['SO_TIEN_6278'] = line.SO_TIEN

		dict_ket_qua_chi_phi_do_dang_cuoi_ky = {}
		ket_qua_phan_bo_da_luu = self.env['gia.thanh.ket.qua.phan.bo.chi.tiet'].search([('KY_TINH_GIA_THANH_ID', '=', self.KY_TINH_GIA_THANH_ONCHANGE)])
		if ket_qua_phan_bo_da_luu:
			for kq_pb in ket_qua_phan_bo_da_luu:
				new_line_ket_qua_phan_bo += [(0,0,{
							'MA_DOI_TUONG_THCP_ID' : [kq_pb.MA_DOI_TUONG_THCP_ID.id,kq_pb.MA_DOI_TUONG_THCP_ID.MA_DOI_TUONG_THCP],
							'TEN_DOI_TUONG_THCP' : kq_pb.TEN_DOI_TUONG_THCP,
							'LOAI_DOI_TUONG_THCP' : kq_pb.LOAI_DOI_TUONG_THCP,

							'MA_CONG_TRINH_ID' : [kq_pb.MA_CONG_TRINH_ID.id,kq_pb.MA_CONG_TRINH_ID.MA_CONG_TRINH],
							'TEN_CONG_TRINH' : kq_pb.TEN_CONG_TRINH,
							'LOAI_CONG_TRINH' : [kq_pb.LOAI_CONG_TRINH.id,kq_pb.LOAI_CONG_TRINH.MA_LOAI_CONG_TRINH],

							'SO_DON_HANG_ID' : [kq_pb.SO_DON_HANG_ID.id,kq_pb.SO_DON_HANG_ID.SO_DON_HANG],
							'NGAY_DON_HANG' : kq_pb.NGAY_DON_HANG,
							'KHACH_HANG' : [kq_pb.KHACH_HANG.id,kq_pb.KHACH_HANG.HO_VA_TEN],

							'HOP_DONG_BAN_ID' : [kq_pb.HOP_DONG_BAN_ID.id,kq_pb.HOP_DONG_BAN_ID.SO_HOP_DONG],
							'NGAY_KY' : kq_pb.NGAY_KY,
							'TRICH_YEU' : kq_pb.TRICH_YEU,
							'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,

							'TY_LE_PHAN_TRAM_621' : kq_pb.TY_LE_PHAN_TRAM_621,
							'SO_TIEN_621' : kq_pb.SO_TIEN_621,
							'TY_LE_PHAN_TRAM_622' : kq_pb.TY_LE_PHAN_TRAM_622,
							'SO_TIEN_622' : kq_pb.SO_TIEN_622,
							'TY_LE_PHAN_TRAM_6271' : kq_pb.TY_LE_PHAN_TRAM_6271,
							'SO_TIEN_6271' : kq_pb.SO_TIEN_6271,
							'TY_LE_PHAN_TRAM_6272' : kq_pb.TY_LE_PHAN_TRAM_6272,
							'SO_TIEN_6272' : kq_pb.SO_TIEN_6272,
							'TY_LE_PHAN_TRAM_6273' : kq_pb.TY_LE_PHAN_TRAM_6273,
							'SO_TIEN_6273' : kq_pb.SO_TIEN_6273,
							'TY_LE_PHAN_TRAM_6274' : kq_pb.TY_LE_PHAN_TRAM_6274,
							'SO_TIEN_6274' : kq_pb.SO_TIEN_6274,
							'TY_LE_PHAN_TRAM_6277' : kq_pb.TY_LE_PHAN_TRAM_6277,
							'SO_TIEN_6277' : kq_pb.SO_TIEN_6277,
							'TY_LE_PHAN_TRAM_6278' : kq_pb.TY_LE_PHAN_TRAM_6278,
							'SO_TIEN_6278' : kq_pb.SO_TIEN_6278,
							'TONG_CHI_PHI' : kq_pb.TONG_CHI_PHI,


							})]
				if kq_pb.MA_DOI_TUONG_THCP_ID.id not in dict_ket_qua_chi_phi_do_dang_cuoi_ky:
					dict_ket_qua_chi_phi_do_dang_cuoi_ky[kq_pb.MA_DOI_TUONG_THCP_ID.id] = {'MA_DOI_TUONG_THCP' : kq_pb.MA_DOI_TUONG_THCP_ID.MA_DOI_TUONG_THCP,
																								'TEN_DOI_TUONG_THCP' : kq_pb.TEN_DOI_TUONG_THCP,}
		else:
			if du_lieu_ket_qua_phan_bo:
				for kq_pb in du_lieu_ket_qua_phan_bo:
					new_line_ket_qua_phan_bo += [(0,0,{
								'MA_DOI_TUONG_THCP_ID' : [kq_pb.get('MA_DOI_TUONG_THCP_ID'),kq_pb.get('MA_DOI_TUONG_THCP')],
								'TEN_DOI_TUONG_THCP' : kq_pb.get('TEN_DOI_TUONG_THCP'),
								'LOAI_DOI_TUONG_THCP' : kq_pb.get('LOAI'),

								'MA_CONG_TRINH_ID' : [kq_pb.get('MA_CONG_TRINH_ID'),kq_pb.get('MA_CONG_TRINH')],
								'TEN_CONG_TRINH' : kq_pb.get('TEN_CONG_TRINH'),
								'LOAI_CONG_TRINH' : [kq_pb.get('LOAI_CONG_TRINH'),kq_pb.get('TEN_LOAI_CONG_TRINH')],

								'SO_DON_HANG_ID' : [kq_pb.get('SO_DON_HANG_ID'),kq_pb.get('SO_DON_HANG')],
								'NGAY_DON_HANG' : kq_pb.get('NGAY_DON_HANG'),
								'KHACH_HANG' : [kq_pb.get('KHACH_HANG_ID'),kq_pb.get('TEN_KHACH_HANG')],

								'HOP_DONG_BAN_ID' : [kq_pb.get('HOP_DONG_BAN_ID'),kq_pb.get('SO_HOP_DONG')],
								'NGAY_KY' : kq_pb.get('NGAY_KY'),
								'TRICH_YEU' : kq_pb.get('TRICH_YEU'),
								'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,
								})]
					if kq_pb.get('MA_DOI_TUONG_THCP_ID') not in dict_ket_qua_chi_phi_do_dang_cuoi_ky:
						dict_ket_qua_chi_phi_do_dang_cuoi_ky[kq_pb.get('MA_DOI_TUONG_THCP_ID')] = {'MA_DOI_TUONG_THCP' : kq_pb.get('MA_DOI_TUONG_THCP'),
																									'TEN_DOI_TUONG_THCP' : kq_pb.get('TEN_DOI_TUONG_THCP'),
																							}

		dict_xac_dinh_do_dang_da_luu = {}
		if du_lieu_xac_dinh_do_dang_da_luu:
			for line in du_lieu_xac_dinh_do_dang_da_luu:
				key = line.get('MA_THANH_PHAM_ID')
				if key not in dict_xac_dinh_do_dang_da_luu:
					dict_xac_dinh_do_dang_da_luu[key] = {
						'SL_DO_DANG_CUOI_KY' : line.get('SL_DO_DANG_CUOI_KY'),
						'PHAN_TRAM_HOAN_THANH' : line.get('PHAN_TRAM_HOAN_THANH'),
					}

		dict_dtthcp_vthh = {}
		dict_gia_tri_dinh_muc = {}																						
		if du_lieu_xac_dinh_do_dang:
			for do_dang in du_lieu_xac_dinh_do_dang:
				key = do_dang.get('MA_HANG_ID')
				chi_tiet = False
				if key in dict_xac_dinh_do_dang_da_luu:
					chi_tiet = dict_xac_dinh_do_dang_da_luu[key]
				new_line_xac_dinh_do_dang += [(0,0,{
							'MA_THANH_PHAM_ID' : [do_dang.get('MA_HANG_ID'),do_dang.get('MA_HANG')],
							'TEN_THANH_PHAM' : do_dang.get('TEN_HANG'),
							'SL_DO_DANG_CUOI_KY' : chi_tiet.get('SL_DO_DANG_CUOI_KY') if chi_tiet != False else 0,
							'PHAN_TRAM_HOAN_THANH' : chi_tiet.get('PHAN_TRAM_HOAN_THANH') if chi_tiet != False else 0,
							'DON_GIA_DINH_MUC' : do_dang.get('GIA_THANH_DON_VI'),
							'MA_DOI_TUONG_THCP_ID' : [do_dang.get('DOI_TUONG_THCP_ID'),do_dang.get('MA_DOI_TUONG_THCP')],
							'TEN_DOI_TUONG_THCP' : do_dang.get('TEN_DOI_TUONG_THCP'),
							})]
				if key not in dict_gia_tri_dinh_muc:
					dict_gia_tri_dinh_muc[key] = 0
				dict_gia_tri_dinh_muc[key] += do_dang.get('GIA_THANH_DON_VI')
				key_dtthcp = do_dang.get('DOI_TUONG_THCP_ID')
				if key_dtthcp not in dict_dtthcp_vthh:
					dict_dtthcp_vthh[key_dtthcp] = []
				dict_dtthcp_vthh[key_dtthcp] += [do_dang.get('MA_HANG_ID')]

		arr_dtthcp_vthh = []
		if dict_dtthcp_vthh:
			for dtthcp in dict_dtthcp_vthh:
				chi_tiet_ids = dict_dtthcp_vthh[dtthcp]
				for line in chi_tiet_ids:
					dtthcp_vthh = str(line) + ';' + str(dtthcp)
					arr_dtthcp_vthh.append(dtthcp_vthh)
		list_vthh_dtthcp_ts = ',' + ",".join(arr_dtthcp_vthh) + ','
		doi_tuong_tinh_gia_thanh_ids = self.lay_du_lieu_doi_tuong_tinh_gia_thanh(ky_tinh_gia_thanh_id,chi_nhanh_id,list_vthh_dtthcp_ts)


		chi_phi_do_dang_cuoi_ky_da_luu = self.env['gia.thanh.ket.qua.chi.phi.do.dang.cuoi.ky.chi.tiet'].search([('KY_TINH_GIA_THANH_ID', '=', self.KY_TINH_GIA_THANH_ONCHANGE)])
		if chi_phi_do_dang_cuoi_ky_da_luu:
			for line in chi_phi_do_dang_cuoi_ky_da_luu:
				new_line_ket_qua_chi_phi_do_dang_cuoi_ky += [(0,0,{
							'MA_DOI_TUONG_THCP_ID' : [line.MA_DOI_TUONG_THCP_ID.id,line.MA_DOI_TUONG_THCP_ID.MA_DOI_TUONG_THCP],
							'TEN_DOI_TUONG_THCP' : line.MA_DOI_TUONG_THCP_ID.TEN_DOI_TUONG_THCP,
							'TONG_CHI_PHI' : line.TONG_CHI_PHI,
							'NVL_TRUC_TIEP' : line.NVL_TRUC_TIEP,
							'NVL_GIAN_TIEP' : line.NVL_GIAN_TIEP,
							'NHAN_CONG_TRUC_TIEP' : line.NHAN_CONG_TRUC_TIEP,
							'NHAN_CONG_GIAN_TIEP' : line.NHAN_CONG_GIAN_TIEP,
							'KHAU_HAO' : line.KHAU_HAO,
							'CHI_PHI_MUA_NGOAI' : line.CHI_PHI_MUA_NGOAI,
							'CHI_PHI_KHAC' : line.CHI_PHI_KHAC,
							})]
		else:
			if dict_ket_qua_chi_phi_do_dang_cuoi_ky:
				for kq_cuoi_ky in dict_ket_qua_chi_phi_do_dang_cuoi_ky:
					chi_tiet = dict_ket_qua_chi_phi_do_dang_cuoi_ky[kq_cuoi_ky]
					new_line_ket_qua_chi_phi_do_dang_cuoi_ky += [(0,0,{
								'MA_DOI_TUONG_THCP_ID' : [kq_cuoi_ky,chi_tiet.get('MA_DOI_TUONG_THCP')],
								'TEN_DOI_TUONG_THCP' : chi_tiet.get('TEN_DOI_TUONG_THCP'),
								'TONG_CHI_PHI' : 0,
								'NVL_TRUC_TIEP' :0,
								'NVL_GIAN_TIEP' : 0,
								'NHAN_CONG_TRUC_TIEP' :0,
								'NHAN_CONG_GIAN_TIEP' :0,
								'KHAU_HAO' :0,
								'CHI_PHI_MUA_NGOAI' :0,
								'CHI_PHI_KHAC' :0,
								})]

		xd_ty_le_pb_doi_tuong_thcp_search_ids = self.env['gia.thanh.ty.le.phan.bo.doi.tuong.thcp.chi.tiet'].search([('KY_TINH_GIA_THANH_ID', '=', self.KY_TINH_GIA_THANH_ONCHANGE)])
		xac_dinh_ty_le_phan_bo_dtthcp_ids = self.env['gia.thanh.ky.tinh.gia.thanh.chi.tiet'].search([('KY_TINH_GIA_THANH_ID', '=', self.KY_TINH_GIA_THANH_ONCHANGE)])

		if xd_ty_le_pb_doi_tuong_thcp_search_ids:
			for line in xd_ty_le_pb_doi_tuong_thcp_search_ids:
				new_line_doi_tuong_thcp += [(0,0,{
					'MA_DOI_TUONG_THCP_ID' : [line.MA_DOI_TUONG_THCP_ID.id,line.MA_DOI_TUONG_THCP_ID.MA_DOI_TUONG_THCP],
					'TEN_DOI_TUONG_THCP' : line.TEN_DOI_TUONG_THCP,
					'LOAI_DOI_TUONG_THCP' : line.LOAI_DOI_TUONG_THCP,
					'PHUONG_PHAP_XAC_DINH' : line.PHUONG_PHAP_XAC_DINH,
					
					})]
		else:
			if xac_dinh_ty_le_phan_bo_dtthcp_ids:
				for dtthcp in xac_dinh_ty_le_phan_bo_dtthcp_ids:
					new_line_doi_tuong_thcp += [(0,0,{
						'MA_DOI_TUONG_THCP_ID' : [dtthcp.MA_DOI_TUONG_THCP_ID.id,dtthcp.MA_DOI_TUONG_THCP_ID.MA_DOI_TUONG_THCP],
						'TEN_DOI_TUONG_THCP' : dtthcp.TEN_DOI_TUONG_THCP,
						'LOAI_DOI_TUONG_THCP' : dtthcp.LOAI,
						'PHUONG_PHAP_XAC_DINH' : 'HE_SO',
						
						})]
				
		doi_tuong_tinh_gia_thanh_search_ids = self.env['gia.thanh.xdtlpb.doi.tuong.tinh.gia.thanh.chi.tiet'].search([('KY_TINH_GIA_THANH_ID', '=', self.KY_TINH_GIA_THANH_ONCHANGE)])
		if doi_tuong_tinh_gia_thanh_search_ids:
			for line in doi_tuong_tinh_gia_thanh_search_ids:
				new_line_xac_dinh_ty_le_phan_bo += [(0,0,{
					'DOI_TUONG_THCP_ID' : [line.DOI_TUONG_THCP_ID.id,line.DOI_TUONG_THCP_ID.MA_DOI_TUONG_THCP],
					'MA_THANH_PHAM_ID' : [line.MA_THANH_PHAM_ID.id,line.MA_THANH_PHAM_ID.MA],
					'TEN_THANH_PHAM' : line.TEN_THANH_PHAM,
					'LA_THANH_PHAM_CHUAN' : line.LA_THANH_PHAM_CHUAN,
					'SO_LUONG_THANH_PHAM' : line.SO_LUONG_THANH_PHAM,
					'GIA_THANH_DINH_MUC' : line.GIA_THANH_DINH_MUC,
					'HE_SO' : line.HE_SO,
					'SO_LUONG_THANH_PHAM_CHUAN' : line.SO_LUONG_THANH_PHAM_CHUAN,
					'TY_LE_PHAN_BO_GIA_THANH' : line.TY_LE_PHAN_BO_GIA_THANH,
					
					})]
		else:
			if doi_tuong_tinh_gia_thanh_ids:
				for doi_tuong in doi_tuong_tinh_gia_thanh_ids:
					key = doi_tuong.get('MA_HANG_ID')
					gia_thanh_dinh_muc = 0
					if key in dict_gia_tri_dinh_muc:
						gia_thanh_dinh_muc = dict_gia_tri_dinh_muc[key]
					new_line_xac_dinh_ty_le_phan_bo += [(0,0,{
						'DOI_TUONG_THCP_ID' : [doi_tuong.get('MA_DOI_TUONG_THCP_ID'),doi_tuong.get('MA_DOI_TUONG_THCP')],
						'MA_THANH_PHAM_ID' : [doi_tuong.get('MA_HANG_ID'),doi_tuong.get('MA_HANG')],
						'TEN_THANH_PHAM' : doi_tuong.get('TEN_HANG'),
						'LA_THANH_PHAM_CHUAN' : False,
						'SO_LUONG_THANH_PHAM' : doi_tuong.get('SO_LUONG'),
						'GIA_THANH_DINH_MUC' : gia_thanh_dinh_muc,
						'HE_SO' : 0,
						'SO_LUONG_THANH_PHAM_CHUAN' : 0,
						'TY_LE_PHAN_BO_GIA_THANH' : 0,
						
						})]

		dict_ket_qua = {}
		if self.LOAI_TINH_GIA_THANH == 'HE_SO_TY_LE':
			dict_ket_qua = {'GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS': new_line_xac_dinh_chi_phi_phan_bo,
							'GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS': new_line_ket_qua_phan_bo,
							'GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS': new_line_xac_dinh_do_dang,
							'GIA_THANH_KET_QUA_CHI_PHI_DO_DANG_CUOI_KY_CHI_TIET_IDS': new_line_ket_qua_chi_phi_do_dang_cuoi_ky,
							'GIA_THANH_TY_LE_PHAN_BO_DOI_TUONG_THCP_CHI_TIET_IDS' : new_line_doi_tuong_thcp,
							'GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS' : new_line_xac_dinh_ty_le_phan_bo,
							'GIA_THANH_CHI_TIET_CHUNG_TU_PHAN_BO_CHI_PHI_CHUNG_IDS' : new_line_chi_tiet_chung_tu_phan_bo_chi_phi_chung,
							
					}
		elif self.LOAI_TINH_GIA_THANH == 'GIAN_DON':
			dict_ket_qua = {'GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS': new_line_xac_dinh_chi_phi_phan_bo,
							'GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS': new_line_ket_qua_phan_bo,
							'GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS': new_line_xac_dinh_do_dang,
							'GIA_THANH_KET_QUA_CHI_PHI_DO_DANG_CUOI_KY_CHI_TIET_IDS': new_line_ket_qua_chi_phi_do_dang_cuoi_ky,
							# 'GIA_THANH_TY_LE_PHAN_BO_DOI_TUONG_THCP_CHI_TIET_IDS' : new_line_doi_tuong_thcp,
							# 'GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS' : new_line_xac_dinh_ty_le_phan_bo,
							'GIA_THANH_CHI_TIET_CHUNG_TU_PHAN_BO_CHI_PHI_CHUNG_IDS' : new_line_chi_tiet_chung_tu_phan_bo_chi_phi_chung,
					}
		else:
			dict_ket_qua = {'GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS': new_line_xac_dinh_chi_phi_phan_bo,
							'GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS': new_line_ket_qua_phan_bo,
							'GIA_THANH_CHI_TIET_CHUNG_TU_PHAN_BO_CHI_PHI_CHUNG_IDS' : new_line_chi_tiet_chung_tu_phan_bo_chi_phi_chung,
					}
		return dict_ket_qua


	@api.onchange('ONCHANGE_CLICK_PHAN_BO')
	def _onchange_ONCHANGE_CLICK_PHAN_BO(self):
		if self.KY_TINH_GIA_THANH_ONCHANGE:
			ky_tinh_gia_thanh_id = self.KY_TINH_GIA_THANH_ONCHANGE
			chi_nhanh_id = self.get_chi_nhanh()
			phan_thap_phan = 0
			if self.env['ir.config_parameter'].get_param('he_thong.PHAN_THAP_PHAN_CUA_TY_LE_PHAN_BO'):
				# Cộng thêm 2 vì sau nhân với 100%
				phan_thap_phan = int(self.env['ir.config_parameter'].get_param('he_thong.PHAN_THAP_PHAN_CUA_TY_LE_PHAN_BO')) + 2



			if self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
				for line in self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
					line.TY_LE_PHAN_TRAM_621 = 0
					line.SO_TIEN_621 = 0
					line.TY_LE_PHAN_TRAM_622 = 0
					line.SO_TIEN_622 = 0
					line.TY_LE_PHAN_TRAM_6271 = 0
					line.SO_TIEN_6271 = 0
					line.TY_LE_PHAN_TRAM_6272 = 0
					line.SO_TIEN_6272 = 0
					line.TY_LE_PHAN_TRAM_6273 = 0
					line.SO_TIEN_6273 = 0
					line.TY_LE_PHAN_TRAM_6274 = 0
					line.SO_TIEN_6274 = 0
					line.TY_LE_PHAN_TRAM_6277 = 0
					line.SO_TIEN_6277 = 0
					line.TY_LE_PHAN_TRAM_6278 = 0
					line.SO_TIEN_6278 = 0
					line.TONG_CHI_PHI = 0

			if self.GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS:
				for line in self.GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS:
					arr_list_dtthcp_vthh = []
					loai_phan_bo = 0
					if line.TIEU_THUC_PHAN_BO == 'NGUYEN_VAT_LIEU':
						loai_phan_bo = 0
					elif line.TIEU_THUC_PHAN_BO == 'NHAN_CONG':
						loai_phan_bo = 1
					elif line.TIEU_THUC_PHAN_BO == 'CHI_PHI':
						loai_phan_bo = 2
					elif line.TIEU_THUC_PHAN_BO == 'DINH_MUC':
						loai_phan_bo = 3
					elif line.TIEU_THUC_PHAN_BO == 'DOANH_THU':
						loai_phan_bo = 4
					if self.LOAI_TINH_GIA_THANH in ('HE_SO_TY_LE','GIAN_DON'):
						if line.DOI_TUONG_THCP_ID:
							for dtthcp in line.DOI_TUONG_THCP_ID:
								dtthcp_vthh = str(dtthcp._name).replace(".", "_") + ',' + str(dtthcp.id)
								if dtthcp_vthh not in arr_list_dtthcp_vthh:
									arr_list_dtthcp_vthh.append(dtthcp_vthh)
					elif self.LOAI_TINH_GIA_THANH == 'CONG_TRINH':
						if line.CONG_TRINH_ID:
							for cong_trinh in line.CONG_TRINH_ID:
								cong_trinh_ts = str(cong_trinh._name).replace(".", "_") + ',' + str(cong_trinh.id)
								if cong_trinh_ts not in arr_list_dtthcp_vthh:
									arr_list_dtthcp_vthh.append(cong_trinh_ts)
					elif self.LOAI_TINH_GIA_THANH == 'DON_HANG':
						if line.SO_DON_HANG_ID:
							for don_hang in line.SO_DON_HANG_ID:
								don_hang_ts = str(don_hang._name).replace(".", "_") + ',' + str(don_hang.id)
								if don_hang_ts not in arr_list_dtthcp_vthh:
									arr_list_dtthcp_vthh.append(don_hang_ts)
					elif self.LOAI_TINH_GIA_THANH == 'HOP_DONG':
						if line.HOP_DONG_BAN_ID:
							for hop_dong in line.HOP_DONG_BAN_ID:
								hop_dong_ts = str(hop_dong._name).replace(".", "_") + ',' + str(hop_dong.id)
								if hop_dong_ts not in arr_list_dtthcp_vthh:
									arr_list_dtthcp_vthh.append(hop_dong_ts)
			# list_item = ",".join(arr_list_dtthcp_vthh)

					if self.LOAI_TINH_GIA_THANH in ('HE_SO_TY_LE','GIAN_DON'):
						du_lieu_phan_bo_ids = self.lay_du_lieu_btn_phan_bo(ky_tinh_gia_thanh_id,chi_nhanh_id,arr_list_dtthcp_vthh,loai_phan_bo)
					else:
						du_lieu_phan_bo_ids = self.lay_du_lieu_btn_phan_bo_cho_ct_dh_hd(ky_tinh_gia_thanh_id,chi_nhanh_id,arr_list_dtthcp_vthh,loai_phan_bo)
					tong_tien_phan_bo = 0
					dict_ty_le_phan_bo = {}
					if du_lieu_phan_bo_ids:
						for phan_bo in du_lieu_phan_bo_ids:
							tong_tien_phan_bo += phan_bo.get('SO_TIEN')
						i = 0
						ty_le_da_phan_no = 0
						for phan_bo in du_lieu_phan_bo_ids:
							key_phan_bo = str(phan_bo.get('MODEL_VAT_TU')) + ','+ str(phan_bo.get('ID_VAT_TU'))
							i += 1
							if tong_tien_phan_bo != 0:
								if key_phan_bo not in dict_ty_le_phan_bo:
									if i != len(du_lieu_phan_bo_ids):
										dict_ty_le_phan_bo[key_phan_bo] = float_round(phan_bo.get('SO_TIEN')/tong_tien_phan_bo,phan_thap_phan)
										ty_le_da_phan_no += float_round(phan_bo.get('SO_TIEN')/tong_tien_phan_bo,phan_thap_phan)
									else:
										dict_ty_le_phan_bo[key_phan_bo] = 1 - ty_le_da_phan_no
					else:
						if self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
							chi_tiet = self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS[0]
							key_phan_bo = str(chi_tiet.MA_DOI_TUONG_THCP_ID._name) + ','+ str(chi_tiet.MA_DOI_TUONG_THCP_ID.id)
							dict_ty_le_phan_bo[key_phan_bo] = 1
					
					
					tai_khoan_621 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '621')]).id
					tai_khoan_622 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '622')]).id
					tai_khoan_6271 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '6271')]).id
					tai_khoan_6272 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '6272')]).id
					tai_khoan_6273 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '6273')]).id
					tai_khoan_6274 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '6274')]).id
					tai_khoan_6277 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '6277')]).id
					tai_khoan_6278 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '6278')]).id
					
					# dict_xac_dinh_muc_chi_phi = {}
					tong_chi_phi_621 = 0
					tong_chi_phi_622 = 0
					tong_chi_phi_6271 = 0

					tong_chi_phi_6272 = 0
					tong_chi_phi_6273 = 0
					tong_chi_phi_6274 = 0

					tong_chi_phi_6277 = 0

					tong_chi_phi_6278 = 0

					# Check theo thông tư 133
					arr_tai_khoan_621 = ['NVLTT','NVLTT_CT','NVLTT_SX']
					arr_tai_khoan_622 = ['NCTT_CT','NCTT_SX','NCTT']
					arr_tai_khoan_6271 = ['BH.NV','MTC.NC','QL.NV','SXC.NVCT','SXC.NVPX','SXC.NVSX']
					arr_tai_khoan_6272 = ['BH.NL','MTC.VL','QL.VL','SXC.VL']
					arr_tai_khoan_6273 = ['BH.DC','MTC.DCSX','QL.DC','SXC.DCSX','MTC']
					arr_tai_khoan_6274 = ['BH.KH','MTC.KH','QL.KH','SXC.KH','SXC.KH.CT','SXC.KH.SX']
					arr_tai_khoan_6277 = ['BH.MN','MTC.MN','QL.DV','SXC.MN','SXC.MN.CT','SXC.MN.SX']
					arr_tai_khoan_6278 = ['BH.K','MTC.K','QL.K','SXC.K','SXC.K.CT','SXC.K.SX','CPBH','CPQL','CPSX','SXC']
					
					if self.CHE_DO_KE_TOAN == '15':
						# if self.GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS:
						# 	for line in self.GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS:
						if line.TAI_KHOAN_ID.id == tai_khoan_621:
							tong_chi_phi_621 += line.SO_PHAN_BO_LAN_NAY
						elif line.TAI_KHOAN_ID.id == tai_khoan_622:
							tong_chi_phi_622 += line.SO_PHAN_BO_LAN_NAY
						elif line.TAI_KHOAN_ID.id == tai_khoan_6271:
							tong_chi_phi_6271 += line.SO_PHAN_BO_LAN_NAY
						elif line.TAI_KHOAN_ID.id == tai_khoan_6272:
							tong_chi_phi_6272 += line.SO_PHAN_BO_LAN_NAY
						elif line.TAI_KHOAN_ID.id == tai_khoan_6273:
							tong_chi_phi_6273 += line.SO_PHAN_BO_LAN_NAY
						elif line.TAI_KHOAN_ID.id == tai_khoan_6274:
							tong_chi_phi_6274 += line.SO_PHAN_BO_LAN_NAY
						elif line.TAI_KHOAN_ID.id == tai_khoan_6277:
							tong_chi_phi_6277 += line.SO_PHAN_BO_LAN_NAY
						elif line.TAI_KHOAN_ID.id == tai_khoan_6278:
							tong_chi_phi_6278 += line.SO_PHAN_BO_LAN_NAY
					elif self.CHE_DO_KE_TOAN == '48':
						# if self.GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS:
						# 	for line in self.GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS:
						if line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP in arr_tai_khoan_621:
							tong_chi_phi_621 += line.SO_PHAN_BO_LAN_NAY
						elif line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP in arr_tai_khoan_622:
							tong_chi_phi_622 += line.SO_PHAN_BO_LAN_NAY
						elif line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP in arr_tai_khoan_6271:
							tong_chi_phi_6271 += line.SO_PHAN_BO_LAN_NAY
						elif line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP in arr_tai_khoan_6272:
							tong_chi_phi_6272 += line.SO_PHAN_BO_LAN_NAY
						elif line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP in arr_tai_khoan_6273:
							tong_chi_phi_6273 += line.SO_PHAN_BO_LAN_NAY
						elif line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP in arr_tai_khoan_6274:
							tong_chi_phi_6274 += line.SO_PHAN_BO_LAN_NAY
						elif line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP in arr_tai_khoan_6277:
							tong_chi_phi_6277 += line.SO_PHAN_BO_LAN_NAY
						elif line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP in arr_tai_khoan_6278:
							tong_chi_phi_6278 += line.SO_PHAN_BO_LAN_NAY
							
					so_tien_con_lai_621 = 0
					so_tien_con_lai_622 = 0
					so_tien_con_lai_6271 = 0
					so_tien_con_lai_6272 = 0
					so_tien_con_lai_6273 = 0
					so_tien_con_lai_6274 = 0
					so_tien_con_lai_6277 = 0
					so_tien_con_lai_6278 = 0
					i = 0
					so_dong = len(self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS)
					if self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
						for line in self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
							key_phan_bo = ''
							i += 1
							if self.LOAI_TINH_GIA_THANH in ('HE_SO_TY_LE','GIAN_DON'):
								key_phan_bo = str(line.MA_DOI_TUONG_THCP_ID._name) + ',' + str(line.MA_DOI_TUONG_THCP_ID.id)
							elif self.LOAI_TINH_GIA_THANH == 'CONG_TRINH':
								key_phan_bo = str(line.MA_CONG_TRINH_ID._name) + ',' + str(line.MA_CONG_TRINH_ID.id)
							elif self.LOAI_TINH_GIA_THANH == 'DON_HANG':
								key_phan_bo = str(line.SO_DON_HANG_ID._name) + ',' + str(line.SO_DON_HANG_ID.id)
							elif self.LOAI_TINH_GIA_THANH == 'HOP_DONG':
								key_phan_bo = str(line.HOP_DONG_BAN_ID._name) + ',' + str(line.HOP_DONG_BAN_ID.id)
							# Reset các hạng mục không chọn
							if key_phan_bo not in dict_ty_le_phan_bo:
								if tong_chi_phi_621 > 0:
									line.TY_LE_PHAN_TRAM_621 = 0
									line.SO_TIEN_621 = 0
								if tong_chi_phi_622 > 0:
									line.TY_LE_PHAN_TRAM_622 = 0
									line.SO_TIEN_622 = 0
								if tong_chi_phi_6271 > 0:
									line.TY_LE_PHAN_TRAM_6271 = 0
									line.SO_TIEN_6271 = 0
								if tong_chi_phi_6272 > 0:
									line.TY_LE_PHAN_TRAM_6272 = 0
									line.SO_TIEN_6272 = 0
								if tong_chi_phi_6273 > 0:
									line.TY_LE_PHAN_TRAM_6273 = 0
									line.SO_TIEN_6273 = 0
								if tong_chi_phi_6274 > 0:
									line.TY_LE_PHAN_TRAM_6274 = 0
									line.SO_TIEN_6274 = 0
								if tong_chi_phi_6277 > 0:
									line.TY_LE_PHAN_TRAM_6277 = 0
									line.SO_TIEN_6277 = 0
								if tong_chi_phi_6278 > 0:
									line.TY_LE_PHAN_TRAM_6278 = 0
									line.SO_TIEN_6278 = 0
							else:
								ty_le_phan_bo = dict_ty_le_phan_bo[key_phan_bo]
								if tong_chi_phi_621 > 0:
									line.TY_LE_PHAN_TRAM_621 = ty_le_phan_bo*100
									if i != so_dong:
										line.SO_TIEN_621 = ty_le_phan_bo*tong_chi_phi_621
									else:
										line.SO_TIEN_621 = tong_chi_phi_621 - so_tien_con_lai_621
									so_tien_con_lai_621 += line.SO_TIEN_621
								if tong_chi_phi_622 > 0:
									line.TY_LE_PHAN_TRAM_622 = ty_le_phan_bo*100
									if i != so_dong:
										line.SO_TIEN_622 = ty_le_phan_bo*tong_chi_phi_622
									else:
										line.SO_TIEN_622 = tong_chi_phi_622 - so_tien_con_lai_622
									so_tien_con_lai_622 += line.SO_TIEN_622
								if tong_chi_phi_6271 > 0:
									line.TY_LE_PHAN_TRAM_6271 = ty_le_phan_bo*100
									if i != so_dong:
										line.SO_TIEN_6271 = ty_le_phan_bo*tong_chi_phi_6271
									else:
										line.SO_TIEN_6271 = tong_chi_phi_6271 - so_tien_con_lai_6271
									so_tien_con_lai_6271 += line.SO_TIEN_6271
								if tong_chi_phi_6272 > 0:
									line.TY_LE_PHAN_TRAM_6272 = ty_le_phan_bo*100
									if i != so_dong:
										line.SO_TIEN_6272 = ty_le_phan_bo*tong_chi_phi_6272
									else:
										line.SO_TIEN_6272 = tong_chi_phi_6272 - so_tien_con_lai_6272
									so_tien_con_lai_6272 += line.SO_TIEN_6272
								if tong_chi_phi_6273 > 0:
									line.TY_LE_PHAN_TRAM_6273 = ty_le_phan_bo*100
									if i != so_dong:
										line.SO_TIEN_6273 = ty_le_phan_bo*tong_chi_phi_6273
									else:
										line.SO_TIEN_6273 = tong_chi_phi_6273 - so_tien_con_lai_6273
									so_tien_con_lai_6273 += line.SO_TIEN_6273
								if tong_chi_phi_6274 > 0:
									line.TY_LE_PHAN_TRAM_6274 = ty_le_phan_bo*100
									if i != so_dong:
										line.SO_TIEN_6274 = ty_le_phan_bo*tong_chi_phi_6274
									else:
										line.SO_TIEN_6274 = tong_chi_phi_6274 - so_tien_con_lai_6274
									so_tien_con_lai_6274 += line.SO_TIEN_6274
								if tong_chi_phi_6277 > 0:
									line.TY_LE_PHAN_TRAM_6277 = ty_le_phan_bo*100
									if i != so_dong:
										line.SO_TIEN_6277 = ty_le_phan_bo*tong_chi_phi_6277
									else:
										line.SO_TIEN_6277 = tong_chi_phi_6277 - so_tien_con_lai_6277
									so_tien_con_lai_6277 += line.SO_TIEN_6277
								if tong_chi_phi_6278 > 0:
									line.TY_LE_PHAN_TRAM_6278 = ty_le_phan_bo*100
									if i != so_dong:
										line.SO_TIEN_6278 = ty_le_phan_bo*tong_chi_phi_6278
									else:
										line.SO_TIEN_6278 = tong_chi_phi_6278 - so_tien_con_lai_6278
									so_tien_con_lai_6278 += line.SO_TIEN_6278
								
								
								line.TONG_CHI_PHI = line.SO_TIEN_621 + line.SO_TIEN_622 + line.SO_TIEN_6271 + line.SO_TIEN_6272 + line.SO_TIEN_6273 + line.SO_TIEN_6274 + line.SO_TIEN_6277 + line.SO_TIEN_6278


	def validate_tien_phan_bo(self, args):
		
		tai_khoan_621 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '621')]).id
		tai_khoan_622 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '622')]).id
		tai_khoan_6271 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '6271')]).id
		tai_khoan_6272 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '6272')]).id
		tai_khoan_6273 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '6273')]).id
		tai_khoan_6274 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '6274')]).id
		tai_khoan_6277 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '6277')]).id
		tai_khoan_6278 = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '6278')]).id

		tong_tien_phan_bo_621 = 0
		tong_tien_phan_bo_622 = 0
		tong_tien_phan_bo_6271 = 0
		tong_tien_phan_bo_6272 = 0
		tong_tien_phan_bo_6273 = 0
		tong_tien_phan_bo_6274 = 0
		tong_tien_phan_bo_6277 = 0
		tong_tien_phan_bo_6278 = 0

		# Check theo thông tư 133
		arr_tai_khoan_621 = ['NVLTT','NVLTT_CT','NVLTT_SX']
		arr_tai_khoan_622 = ['NCTT_CT','NCTT_SX','NCTT']
		arr_tai_khoan_6271 = ['BH.NV','MTC.NC','QL.NV','SXC.NVCT','SXC.NVPX','SXC.NVSX']
		arr_tai_khoan_6272 = ['BH.NL','MTC.VL','QL.VL','SXC.VL']
		arr_tai_khoan_6273 = ['BH.DC','MTC.DCSX','QL.DC','SXC.DCSX','MTC']
		arr_tai_khoan_6274 = ['BH.KH','MTC.KH','QL.KH','SXC.KH','SXC.KH.CT','SXC.KH.SX']
		arr_tai_khoan_6277 = ['BH.MN','MTC.MN','QL.DV','SXC.MN','SXC.MN.CT','SXC.MN.SX']
		arr_tai_khoan_6278 = ['BH.K','MTC.K','QL.K','SXC.K','SXC.K.CT','SXC.K.SX','CPBH','CPQL','CPSX','SXC']

		if self.CHE_DO_KE_TOAN == '15':
			if self.GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS:
				for line in self.GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS:
					if line.TAI_KHOAN_ID.id == tai_khoan_621:
						tong_tien_phan_bo_621 += line.SO_PHAN_BO_LAN_NAY
					elif line.TAI_KHOAN_ID.id == tai_khoan_622:
						tong_tien_phan_bo_622 += line.SO_PHAN_BO_LAN_NAY
					elif line.TAI_KHOAN_ID.id == tai_khoan_6271:
						tong_tien_phan_bo_6271 += line.SO_PHAN_BO_LAN_NAY
					elif line.TAI_KHOAN_ID.id == tai_khoan_6272:
						tong_tien_phan_bo_6272 += line.SO_PHAN_BO_LAN_NAY
					elif line.TAI_KHOAN_ID.id == tai_khoan_6273:
						tong_tien_phan_bo_6273 += line.SO_PHAN_BO_LAN_NAY
					elif line.TAI_KHOAN_ID.id == tai_khoan_6274:
						tong_tien_phan_bo_6274 += line.SO_PHAN_BO_LAN_NAY
					elif line.TAI_KHOAN_ID.id == tai_khoan_6277:
						tong_tien_phan_bo_6277 += line.SO_PHAN_BO_LAN_NAY
					elif line.TAI_KHOAN_ID.id == tai_khoan_6278:
						tong_tien_phan_bo_6278 += line.SO_PHAN_BO_LAN_NAY
		elif self.CHE_DO_KE_TOAN == '48':
			if self.GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS:
				for line in self.GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS:
					if line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP in arr_tai_khoan_621:
						tong_tien_phan_bo_621 += line.SO_PHAN_BO_LAN_NAY
					elif line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP in arr_tai_khoan_622:
						tong_tien_phan_bo_622 += line.SO_PHAN_BO_LAN_NAY
					elif line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP in arr_tai_khoan_6271:
						tong_tien_phan_bo_6271 += line.SO_PHAN_BO_LAN_NAY
					elif line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP in arr_tai_khoan_6272:
						tong_tien_phan_bo_6272 += line.SO_PHAN_BO_LAN_NAY
					elif line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP in arr_tai_khoan_6273:
						tong_tien_phan_bo_6273 += line.SO_PHAN_BO_LAN_NAY
					elif line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP in arr_tai_khoan_6274:
						tong_tien_phan_bo_6274 += line.SO_PHAN_BO_LAN_NAY
					elif line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP in arr_tai_khoan_6277:
						tong_tien_phan_bo_6277 += line.SO_PHAN_BO_LAN_NAY
					elif line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP in arr_tai_khoan_6278:
						tong_tien_phan_bo_6278 += line.SO_PHAN_BO_LAN_NAY

					
		tong_tien_da_phan_bo_621 = 0
		tong_tien_da_phan_bo_622 = 0
		tong_tien_da_phan_bo_6271 = 0
		tong_tien_da_phan_bo_6272 = 0
		tong_tien_da_phan_bo_6273 = 0
		tong_tien_da_phan_bo_6274 = 0
		tong_tien_da_phan_bo_6277 = 0
		tong_tien_da_phan_bo_6278 = 0

		if self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
			for line in self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
				tong_tien_da_phan_bo_621 += line.SO_TIEN_621
				tong_tien_da_phan_bo_622 += line.SO_TIEN_622
				tong_tien_da_phan_bo_6271 += line.SO_TIEN_6271
				tong_tien_da_phan_bo_6272 += line.SO_TIEN_6272
				tong_tien_da_phan_bo_6273 += line.SO_TIEN_6273
				tong_tien_da_phan_bo_6274 += line.SO_TIEN_6274
				tong_tien_da_phan_bo_6277 += line.SO_TIEN_6277
				tong_tien_da_phan_bo_6278 += line.SO_TIEN_6278
		loi = False
		thong_bao = ''
		if tong_tien_phan_bo_621 != tong_tien_da_phan_bo_621:
			thong_bao = 'Tổng số tiền phân bổ của TK <621> cho các đối tượng THCP phải bằng số phân bổ lần này của TK đó. Vui lòng kiểm tra lại.'
			loi = True
		elif tong_tien_phan_bo_622 != tong_tien_da_phan_bo_622:
			thong_bao = 'Tổng số tiền phân bổ của TK <622> cho các đối tượng THCP phải bằng số phân bổ lần này của TK đó. Vui lòng kiểm tra lại.'
			loi = True
		elif tong_tien_phan_bo_6271 != tong_tien_da_phan_bo_6271:
			thong_bao = 'Tổng số tiền phân bổ của TK <6271> cho các đối tượng THCP phải bằng số phân bổ lần này của TK đó. Vui lòng kiểm tra lại.'
			loi = True
		elif tong_tien_phan_bo_6272 != tong_tien_da_phan_bo_6272:
			thong_bao = 'Tổng số tiền phân bổ của TK <6272> cho các đối tượng THCP phải bằng số phân bổ lần này của TK đó. Vui lòng kiểm tra lại.'
			loi = True
		elif tong_tien_phan_bo_6273 != tong_tien_da_phan_bo_6273:
			thong_bao = 'Tổng số tiền phân bổ của TK <6273> cho các đối tượng THCP phải bằng số phân bổ lần này của TK đó. Vui lòng kiểm tra lại.'
			loi = True
		elif tong_tien_phan_bo_6274 != tong_tien_da_phan_bo_6274:
			thong_bao = 'Tổng số tiền phân bổ của TK <6274> cho các đối tượng THCP phải bằng số phân bổ lần này của TK đó. Vui lòng kiểm tra lại.'
			loi = True
		elif tong_tien_phan_bo_6277 != tong_tien_da_phan_bo_6277:
			thong_bao = 'Tổng số tiền phân bổ của TK <6277> cho các đối tượng THCP phải bằng số phân bổ lần này của TK đó. Vui lòng kiểm tra lại.'
			loi = True
		elif tong_tien_phan_bo_6278 != tong_tien_da_phan_bo_6278:
			thong_bao = 'Tổng số tiền phân bổ của TK <6271> cho các đối tượng THCP phải bằng số phân bổ lần này của TK đó. Vui lòng kiểm tra lại.'
			loi = True
		
		return {'loi' : loi,'thong_bao' : thong_bao}

	@api.onchange('MUC_DANH_GIA_DO_DANG')
	def _onchange_MUC_DANH_GIA_DO_DANG(self):
		if self.MUC_DANH_GIA_DO_DANG and self.MUC_DANH_GIA_DO_DANG == 'NGUYEN_VAT_LIEU_TRUC_TIEP':
			if self.GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS:
				for line in self.GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS:
					line.PHAN_TRAM_HOAN_THANH = 100

	@api.onchange('ONCHANGE_CLICK_TINH_CP_DD')
	def _onchange_ONCHANGE_CLICK_TINH_CP_DD(self):
		# công thức:
		# 	tổng giá trị = giá trị hoản thành(tab phân bổ chi phí chung) + giá trị dở dang(lấy trong sql)
		# 	tổng số lượng = số lượng dở dang(nhập trên tab xác định dở dang) + số lượng hoàn thành(trong sql)
		# 	kết quả trong tab chi phí dở dang cuối kỳ = (tổng giá trị / tổng số lượng) * số lượng trong tab xác định dở dang
		if self.KY_TINH_GIA_THANH_ONCHANGE:
			ky_tinh_gia_thanh_id = self.KY_TINH_GIA_THANH_ONCHANGE
			chi_nhanh_id = self.get_chi_nhanh()
					
			# Lấy dữ liệu từ tab xác định dở dang
			dict_xac_dinh_do_dang = {}
			arr_vthh_dtthcp = []
			if self.GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS:
				for line in self.GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS:
					key_dtthcp = line.MA_DOI_TUONG_THCP_ID.id
					key_thanh_pham = line.MA_THANH_PHAM_ID.id
					if key_dtthcp not in dict_xac_dinh_do_dang:
						dict_xac_dinh_do_dang[key_dtthcp] = {}
					if key_thanh_pham not in dict_xac_dinh_do_dang[key_dtthcp]:
						dict_xac_dinh_do_dang[key_dtthcp][key_thanh_pham] = {'SL_DO_DANG_CUOI_KY' : 0,'PHAN_TRAM_HOAN_THANH' : 0,'SL_DO_DANG_CUOI_KY_PHAN_TRAM' : 0}
					dict_xac_dinh_do_dang[key_dtthcp][key_thanh_pham]['SL_DO_DANG_CUOI_KY'] += line.SL_DO_DANG_CUOI_KY
					dict_xac_dinh_do_dang[key_dtthcp][key_thanh_pham]['PHAN_TRAM_HOAN_THANH'] += line.PHAN_TRAM_HOAN_THANH
					dict_xac_dinh_do_dang[key_dtthcp][key_thanh_pham]['SL_DO_DANG_CUOI_KY_PHAN_TRAM'] += (line.SL_DO_DANG_CUOI_KY*line.PHAN_TRAM_HOAN_THANH)/100
					list_vthh_dtthcp = str(line.MA_THANH_PHAM_ID.id) + ';' + str(line.MA_DOI_TUONG_THCP_ID.id)
					arr_vthh_dtthcp.append(list_vthh_dtthcp)
			list_vthh_dtthcp_ts = ',' + ",".join(arr_vthh_dtthcp) + ','
			du_lieu_so_luong_hoan_thanh = self.btn_tinh_chi_phi_do_dang_so_Luong_cuoi_ky(ky_tinh_gia_thanh_id,chi_nhanh_id,list_vthh_dtthcp_ts)
			if self.MUC_DANH_GIA_DO_DANG != 'DINH_MUC':
				dict_so_luong_hoan_thanh = {}
				for hoan_thanh in du_lieu_so_luong_hoan_thanh:
					key = hoan_thanh.get('MA_DOI_TUONG_THCP_ID')
					if key not in dict_so_luong_hoan_thanh:
						dict_so_luong_hoan_thanh[key] = 0
					dict_so_luong_hoan_thanh[key] += hoan_thanh.get('SO_LUONG')

				# Lấy dữ liệu từ tab kết quả phân bổ
				dict_gia_tri_hoan_thanh_chi_phi_nvl_truc_tiep = {} # 621
				dict_gia_tri_hoan_thanh_chi_phi_nhan_cong_tt = {} # 622
				dict_gia_tri_hoan_thanh_chi_phi_nhan_cong_gt = {} # 6271
				dict_gia_tri_hoan_thanh_chi_phi_vat_lieu = {} # 6272
				dict_gia_tri_hoan_thanh_chi_phi_cong_cu_san_xuat = {} # 6273
				dict_gia_tri_hoan_thanh_chi_phi_khau_hao_tscd = {} # 6274
				dict_gia_tri_hoan_thanh_chi_phi_mua_ngoai = {} # 6277
				dict_gia_tri_hoan_thanh_chi_phi_bang_tien_khac = {} # 6278
				
				if self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
					for line in self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
						key = line.MA_DOI_TUONG_THCP_ID.id
						if key not in dict_gia_tri_hoan_thanh_chi_phi_nvl_truc_tiep:
							dict_gia_tri_hoan_thanh_chi_phi_nvl_truc_tiep[key] = 0
						dict_gia_tri_hoan_thanh_chi_phi_nvl_truc_tiep[key] += line.SO_TIEN_621
						if key not in dict_gia_tri_hoan_thanh_chi_phi_mua_ngoai:
							dict_gia_tri_hoan_thanh_chi_phi_mua_ngoai[key] = 0
						dict_gia_tri_hoan_thanh_chi_phi_mua_ngoai[key] += line.SO_TIEN_6277

						if key not in dict_gia_tri_hoan_thanh_chi_phi_nhan_cong_tt:
							dict_gia_tri_hoan_thanh_chi_phi_nhan_cong_tt[key] = 0
						dict_gia_tri_hoan_thanh_chi_phi_nhan_cong_tt[key] += line.SO_TIEN_622
						if key not in dict_gia_tri_hoan_thanh_chi_phi_nhan_cong_gt:
							dict_gia_tri_hoan_thanh_chi_phi_nhan_cong_gt[key] = 0
						dict_gia_tri_hoan_thanh_chi_phi_nhan_cong_gt[key] += line.SO_TIEN_6271

						if key not in dict_gia_tri_hoan_thanh_chi_phi_vat_lieu:
							dict_gia_tri_hoan_thanh_chi_phi_vat_lieu[key] = 0
						dict_gia_tri_hoan_thanh_chi_phi_vat_lieu[key] += line.SO_TIEN_6272
						if key not in dict_gia_tri_hoan_thanh_chi_phi_cong_cu_san_xuat:
							dict_gia_tri_hoan_thanh_chi_phi_cong_cu_san_xuat[key] = 0
						dict_gia_tri_hoan_thanh_chi_phi_cong_cu_san_xuat[key] += line.SO_TIEN_6273
						if key not in dict_gia_tri_hoan_thanh_chi_phi_khau_hao_tscd:
							dict_gia_tri_hoan_thanh_chi_phi_khau_hao_tscd[key] = 0
						dict_gia_tri_hoan_thanh_chi_phi_khau_hao_tscd[key] += line.SO_TIEN_6274
						if key not in dict_gia_tri_hoan_thanh_chi_phi_bang_tien_khac:
							dict_gia_tri_hoan_thanh_chi_phi_bang_tien_khac[key] = 0
						dict_gia_tri_hoan_thanh_chi_phi_bang_tien_khac[key] += line.SO_TIEN_6278

				if self.GIA_THANH_KET_QUA_CHI_PHI_DO_DANG_CUOI_KY_CHI_TIET_IDS:
					for line in self.GIA_THANH_KET_QUA_CHI_PHI_DO_DANG_CUOI_KY_CHI_TIET_IDS:
						line.NVL_TRUC_TIEP = 0
						line.CHI_PHI_MUA_NGOAI = 0
						line.NHAN_CONG_TRUC_TIEP = 0
						line.NHAN_CONG_GIAN_TIEP = 0
						line.NVL_GIAN_TIEP = 0
						line.KHAU_HAO = 0
						line.CHI_PHI_KHAC = 0
						line.TONG_CHI_PHI = 0

						du_lieu_do_dang_cuoi_ky = self.btn_tinh_chi_phi_do_dang_ket_qua_cuoi_ky(ky_tinh_gia_thanh_id,chi_nhanh_id,line.MA_DOI_TUONG_THCP_ID.id)
						key = line.MA_DOI_TUONG_THCP_ID.id
						# Tính tổng giá trị nguyên vật liệu trực tiếp
						gia_tri_nvl_tt = 0
						gia_tri_nvl_tt_do_dang = 0
						if key in dict_gia_tri_hoan_thanh_chi_phi_nvl_truc_tiep:
							gia_tri_nvl_tt = dict_gia_tri_hoan_thanh_chi_phi_nvl_truc_tiep[key]
						if du_lieu_do_dang_cuoi_ky:
							gia_tri_nvl_tt_do_dang = du_lieu_do_dang_cuoi_ky[0].get('NVL_TRUC_TIEP')
						tong_gia_tri_nvl_tt = gia_tri_nvl_tt + gia_tri_nvl_tt_do_dang

						# Tính tổng giá trị chi phí mua ngoài
						gia_tri_mua_ngoai = 0
						gia_tri_mua_ngoai_do_dang = 0
						if key in dict_gia_tri_hoan_thanh_chi_phi_mua_ngoai:
							gia_tri_mua_ngoai = dict_gia_tri_hoan_thanh_chi_phi_mua_ngoai[key]
						if du_lieu_do_dang_cuoi_ky:
							gia_tri_mua_ngoai_do_dang = du_lieu_do_dang_cuoi_ky[0].get('GIA_TRI_MUA')
						tong_gia_tri_mua_ngoai = gia_tri_mua_ngoai + gia_tri_mua_ngoai_do_dang

						# Tính tổng giá trị nhân công trực tiếp
						gia_tri_nhan_cong_tt = 0
						gia_tri_nhan_cong_tt_do_dang = 0
						if key in dict_gia_tri_hoan_thanh_chi_phi_nhan_cong_tt:
							gia_tri_nhan_cong_tt = dict_gia_tri_hoan_thanh_chi_phi_nhan_cong_tt[key]
						if du_lieu_do_dang_cuoi_ky:
							gia_tri_nhan_cong_tt_do_dang = du_lieu_do_dang_cuoi_ky[0].get('NHAN_CONG_TRUC_TIEP')
						tong_gia_tri_nhan_cong_tt = gia_tri_nhan_cong_tt + gia_tri_nhan_cong_tt_do_dang

						# Tính tổng giá trị nhân công gián tiếp
						gia_tri_nhan_cong_gt = 0
						gia_tri_nhan_cong_gt_do_dang = 0
						if key in dict_gia_tri_hoan_thanh_chi_phi_nhan_cong_gt:
							gia_tri_nhan_cong_gt = dict_gia_tri_hoan_thanh_chi_phi_nhan_cong_gt[key]
						if du_lieu_do_dang_cuoi_ky:
							gia_tri_nhan_cong_gt_do_dang = du_lieu_do_dang_cuoi_ky[0].get('NHAN_CONG_GIAN_TIEP')
						tong_gia_tri_nhan_cong_gt = gia_tri_nhan_cong_gt + gia_tri_nhan_cong_gt_do_dang

						# Tính các chi phí nvl gián tiếp
						gia_tri_nvl_gian_tiep = 0
						gia_tri_nvl_gian_tiep_do_dang = 0
						if du_lieu_do_dang_cuoi_ky:
							gia_tri_nvl_gian_tiep = du_lieu_do_dang_cuoi_ky[0].get('NVL_GIAN_TIEP')
						if key in dict_gia_tri_hoan_thanh_chi_phi_vat_lieu:
							gia_tri_nvl_gian_tiep_do_dang = dict_gia_tri_hoan_thanh_chi_phi_vat_lieu[key]
						tong_gia_tri_nvl_gian_tiep = gia_tri_nvl_gian_tiep + gia_tri_nvl_gian_tiep_do_dang

						# Tính chi phí khấu hao
						gia_tri_khau_hao = 0
						gia_tri_khau_hao_do_dang = 0
						if du_lieu_do_dang_cuoi_ky:
							gia_tri_khau_hao = du_lieu_do_dang_cuoi_ky[0].get('KHAU_HAO')
						if key in dict_gia_tri_hoan_thanh_chi_phi_khau_hao_tscd:
							gia_tri_khau_hao_do_dang = dict_gia_tri_hoan_thanh_chi_phi_khau_hao_tscd[key]
						tong_gia_tri_khau_hao = gia_tri_khau_hao + gia_tri_khau_hao_do_dang

						# Tính chi phí khác
						gia_tri_cp_khac = 0
						gia_tri_cp_khac_do_dang = 0
						if du_lieu_do_dang_cuoi_ky:
							gia_tri_cp_khac = du_lieu_do_dang_cuoi_ky[0].get('CHI_PHI_KHAC')
						if key in dict_gia_tri_hoan_thanh_chi_phi_bang_tien_khac:
							gia_tri_cp_khac_do_dang = dict_gia_tri_hoan_thanh_chi_phi_bang_tien_khac[key]
						tong_gia_tri_cp_khac = gia_tri_cp_khac + gia_tri_cp_khac_do_dang

						# Tính tổng số lượng nguyên vật liệu trực tiếp
						so_luong_hoan_thanh = 0
						so_luong_do_dang = 0
						phan_tram_hoan_thanh = 0
						if key in dict_so_luong_hoan_thanh:
							so_luong_hoan_thanh = dict_so_luong_hoan_thanh[key]
						if key in dict_xac_dinh_do_dang:
							for dpdd_key in dict_xac_dinh_do_dang[key]:
								dpdd = dict_xac_dinh_do_dang[key][dpdd_key]
								so_luong_do_dang += dpdd.get('SL_DO_DANG_CUOI_KY_PHAN_TRAM')
								# phan_tram_hoan_thanh = dict_xac_dinh_do_dang[key].get('PHAN_TRAM_HOAN_THANH')
						tong_so_luong = so_luong_hoan_thanh + so_luong_do_dang

						if tong_so_luong > 0:
							if key in dict_xac_dinh_do_dang:
								for dpdd_key in dict_xac_dinh_do_dang[key]:
									dpdd = dict_xac_dinh_do_dang[key][dpdd_key]
									line.NVL_TRUC_TIEP += (tong_gia_tri_nvl_tt/tong_so_luong)*dpdd.get('SL_DO_DANG_CUOI_KY_PHAN_TRAM')
									if self.MUC_DANH_GIA_DO_DANG in ('HOAN_THANH_TUONG_DUONG','NGUYEN_VAT_LIEU_TRUC_TIEP'):
										line.CHI_PHI_MUA_NGOAI += (tong_gia_tri_mua_ngoai/tong_so_luong)*dpdd.get('SL_DO_DANG_CUOI_KY_PHAN_TRAM')
										line.NHAN_CONG_TRUC_TIEP += (tong_gia_tri_nhan_cong_tt/tong_so_luong)*dpdd.get('SL_DO_DANG_CUOI_KY_PHAN_TRAM')
										line.NHAN_CONG_GIAN_TIEP += (tong_gia_tri_nhan_cong_gt/tong_so_luong)*dpdd.get('SL_DO_DANG_CUOI_KY_PHAN_TRAM')

										line.NVL_GIAN_TIEP += (tong_gia_tri_nvl_gian_tiep/tong_so_luong)*dpdd.get('SL_DO_DANG_CUOI_KY_PHAN_TRAM')
										line.KHAU_HAO += (tong_gia_tri_khau_hao/tong_so_luong)*dpdd.get('SL_DO_DANG_CUOI_KY_PHAN_TRAM')
										line.CHI_PHI_KHAC += (tong_gia_tri_cp_khac/tong_so_luong)*dpdd.get('SL_DO_DANG_CUOI_KY_PHAN_TRAM')
									elif self.MUC_DANH_GIA_DO_DANG == 'NGUYEN_VAT_LIEU_TRUC_TIEP':
										line.CHI_PHI_MUA_NGOAI = line.NHAN_CONG_TRUC_TIEP = line.NHAN_CONG_GIAN_TIEP = line.NVL_GIAN_TIEP = line.KHAU_HAO = line.CHI_PHI_KHAC = 0
								line.TONG_CHI_PHI = line.NVL_TRUC_TIEP + line.CHI_PHI_MUA_NGOAI + line.NHAN_CONG_TRUC_TIEP + line.NHAN_CONG_GIAN_TIEP + line.NVL_GIAN_TIEP + line.KHAU_HAO + line.CHI_PHI_KHAC
			else:
				dict_vthh_theo_phan_xuong = {}
				# if du_lieu_so_luong_hoan_thanh:
				# 	for phan_xuong in du_lieu_so_luong_hoan_thanh:
				# 		key = phan_xuong.get('MA_DOI_TUONG_THCP_ID')
				# 		if key not in dict_vthh_theo_phan_xuong:
				# 			dict_vthh_theo_phan_xuong[key] = []
				# 		dict_vthh_theo_phan_xuong[key] = [phan_xuong]

				if self.GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS:
					for line in self.GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS:
						key = line.MA_DOI_TUONG_THCP_ID.id
						if key not in dict_vthh_theo_phan_xuong:
							dict_vthh_theo_phan_xuong[key] = []
						dict_vthh_theo_phan_xuong[key] += [line]



				if self.GIA_THANH_KET_QUA_CHI_PHI_DO_DANG_CUOI_KY_CHI_TIET_IDS:
					for line in self.GIA_THANH_KET_QUA_CHI_PHI_DO_DANG_CUOI_KY_CHI_TIET_IDS:

						line.NVL_TRUC_TIEP = 0
						line.CHI_PHI_MUA_NGOAI = 0
						line.NHAN_CONG_TRUC_TIEP = 0
						line.NHAN_CONG_GIAN_TIEP = 0
						line.NVL_GIAN_TIEP = 0
						line.KHAU_HAO = 0
						line.CHI_PHI_KHAC = 0

						key = line.MA_DOI_TUONG_THCP_ID.id
						# so_luong_do_dang = 0
						# phan_tram_hoan_thanh = 0
						so_luong_do_dang_phan_tram = 0
						if key in dict_xac_dinh_do_dang:
							for dpdd_key in dict_xac_dinh_do_dang[key]:
								dpdd = dict_xac_dinh_do_dang[key][dpdd_key]
						# 		so_luong_do_dang += dpdd.get('SL_DO_DANG_CUOI_KY')
								so_luong_do_dang_phan_tram += dpdd.get('SL_DO_DANG_CUOI_KY_PHAN_TRAM')
						# 		phan_tram_hoan_thanh += dpdd.get('PHAN_TRAM_HOAN_THANH')
						if key in dict_vthh_theo_phan_xuong:
							chi_tiet_ids = dict_vthh_theo_phan_xuong[key]
							for chi_tiet in chi_tiet_ids:
								du_lieu_do_dang_dau_ky = self.btn_tinh_chi_phi_do_dang_theo_dinh_muc(chi_tiet.MA_THANH_PHAM_ID.id)

								if key in dict_xac_dinh_do_dang:
									for dpdd_key in dict_xac_dinh_do_dang[key]:
										if dpdd_key == chi_tiet.MA_THANH_PHAM_ID.id:
											so_luong_do_dang_phan_tram = 0
											dpdd = dict_xac_dinh_do_dang[key][dpdd_key]
											so_luong_do_dang_phan_tram += dpdd.get('SL_DO_DANG_CUOI_KY_PHAN_TRAM')

											if du_lieu_do_dang_dau_ky:
												line.NVL_TRUC_TIEP += du_lieu_do_dang_dau_ky[0].get('NVL_TRUC_TIEP')*so_luong_do_dang_phan_tram
												line.CHI_PHI_MUA_NGOAI += du_lieu_do_dang_dau_ky[0].get('CHI_PHI_MUA_NGOAI')*so_luong_do_dang_phan_tram
												line.NHAN_CONG_TRUC_TIEP += du_lieu_do_dang_dau_ky[0].get('NHAN_CONG_TRUC_TIEP')*so_luong_do_dang_phan_tram
												line.NHAN_CONG_GIAN_TIEP += du_lieu_do_dang_dau_ky[0].get('NHAN_CONG_GIAN_TIEP')*so_luong_do_dang_phan_tram

												line.NVL_GIAN_TIEP += du_lieu_do_dang_dau_ky[0].get('NVL_GIAN_TIEP')*so_luong_do_dang_phan_tram
												line.KHAU_HAO += du_lieu_do_dang_dau_ky[0].get('KHAU_HAO')*so_luong_do_dang_phan_tram
												line.CHI_PHI_KHAC += du_lieu_do_dang_dau_ky[0].get('CHI_PHI_KHAC')*so_luong_do_dang_phan_tram

						line.TONG_CHI_PHI = line.NVL_TRUC_TIEP + line.CHI_PHI_MUA_NGOAI + line.NHAN_CONG_TRUC_TIEP + line.NHAN_CONG_GIAN_TIEP + line.NVL_GIAN_TIEP + line.KHAU_HAO + line.CHI_PHI_KHAC
				

	@api.onchange('ONCHANGE_CLICK_LAY_GIA_THANH_DINH_MUC')
	def _onchange_ONCHANGE_CLICK_LAY_GIA_THANH_DINH_MUC(self):
		if self.GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS:
			phan_thap_phan = 0
			if self.env['ir.config_parameter'].get_param('he_thong.PHAN_THAP_PHAN_CUA_TY_LE_PHAN_BO'):
				phan_thap_phan = int(self.env['ir.config_parameter'].get_param('he_thong.PHAN_THAP_PHAN_CUA_TY_LE_PHAN_BO')) + 2
			if self.PHUONG_PHAP_XAC_DINH == 'HE_SO':
				dict_doi_tuong = {}
				for line in self.GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS:
					key = line.DOI_TUONG_THCP_ID.id
					if key not in dict_doi_tuong:
						dict_doi_tuong[key] = 0
					if line.GIA_THANH_DINH_MUC > dict_doi_tuong[key]:
						dict_doi_tuong[key] = line.GIA_THANH_DINH_MUC
				
				dict_so_luong_thanh_pham_chuan = {}
				for line in self.GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS:
					key = line.DOI_TUONG_THCP_ID.id
					if key in dict_doi_tuong:
						if dict_doi_tuong[key] != 0:
							line.HE_SO = float_round(line.GIA_THANH_DINH_MUC/dict_doi_tuong[key],phan_thap_phan)
							line.SO_LUONG_THANH_PHAM_CHUAN = line.HE_SO*line.SO_LUONG_THANH_PHAM
					
					if key not in dict_so_luong_thanh_pham_chuan:
						dict_so_luong_thanh_pham_chuan[key] = 0
					dict_so_luong_thanh_pham_chuan[key] += line.SO_LUONG_THANH_PHAM_CHUAN
				
				for line in self.GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS:
					key = line.DOI_TUONG_THCP_ID.id
					if key in dict_so_luong_thanh_pham_chuan:
						if dict_so_luong_thanh_pham_chuan[key] != 0:
							line.TY_LE_PHAN_BO_GIA_THANH = float_round((line.SO_LUONG_THANH_PHAM_CHUAN/dict_so_luong_thanh_pham_chuan[key])*100,phan_thap_phan)
			else:
				dict_tieu_chuan_phan_bo = {}
				for line in self.GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS:
					key = line.DOI_TUONG_THCP_ID.id
					line.TIEU_CHUAN_PHAN_BO = line.SO_LUONG_THANH_PHAM*line.GIA_THANH_DINH_MUC
					if key not in dict_tieu_chuan_phan_bo:
						dict_tieu_chuan_phan_bo[key] = 0
					dict_tieu_chuan_phan_bo[key] += line.TIEU_CHUAN_PHAN_BO

				for line in self.GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS:
					key = line.DOI_TUONG_THCP_ID.id
					if key in dict_tieu_chuan_phan_bo:
						if dict_tieu_chuan_phan_bo[key] != 0:
							line.TY_LE_PHAN_BO_GIA_THANH = float_round((line.TIEU_CHUAN_PHAN_BO/dict_tieu_chuan_phan_bo[key])*100,phan_thap_phan)
				


	@api.onchange('ONCHANGE_CLICK_TINH_GIA_THANH')
	def _onchange_ONCHANGE_CLICK_TINH_GIA_THANH(self):
		if self.KY_TINH_GIA_THANH_ONCHANGE:

			phan_thap_phan_gia_thanh_don_vi = 0
			if self.env['ir.config_parameter'].get_param('he_thong.PHAN_THAP_PHAN_DON_GIA'):
				phan_thap_phan_gia_thanh_don_vi = int(self.env['ir.config_parameter'].get_param('he_thong.PHAN_THAP_PHAN_DON_GIA'))

			env = self.env['gia.thanh.bang.gia.thanh.chi.tiet']
			self.GIA_THANH_BANG_GIA_THANH_CHI_TIET_IDS = []
			dict_phan_tram = {}
			if self.GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS:
				for line in self.GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS:
					key = str(line.DOI_TUONG_THCP_ID.id) + ',' + str(line.MA_THANH_PHAM_ID.id)
					if key not in dict_phan_tram:
						dict_phan_tram[key] = 0
						dict_phan_tram[key] += line.TY_LE_PHAN_BO_GIA_THANH
					
					# [{
					# 		'DOI_TUONG_THCP_ID' : line.DOI_TUONG_THCP_ID.id,
					# 		'MA_DOI_TUONG_THCP' : line.DOI_TUONG_THCP_ID.MA_DOI_TUONG_THCP,
					# 		'TEN_DOI_TUONG_THCP' : line.DOI_TUONG_THCP_ID.TEN_DOI_TUONG_THCP,
					# 		'MA_THANH_PHAM_ID' : line.MA_THANH_PHAM_ID.id,
					# 		'MA_THANH_PHAM' : line.MA_THANH_PHAM_ID.MA,
					# 		'TEN_THANH_PHAM' : line.MA_THANH_PHAM_ID.TEN,
					# 		'DON_VI_TINH' : line.MA_THANH_PHAM_ID.DVT_CHINH_ID.id,
					# 		'TEN_DVT' : line.MA_THANH_PHAM_ID.DVT_CHINH_ID.DON_VI_TINH,
					# 		'TY_LE_PB_GIA_THANH' : line.TY_LE_PHAN_BO_GIA_THANH,
					# 	}]
			dict_phan_bo_chi_phi_chung = {}
			if self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
				for line in self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
					key = line.MA_DOI_TUONG_THCP_ID.id
					if key not in dict_phan_bo_chi_phi_chung:
						dict_phan_bo_chi_phi_chung[key] = {
							'DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
							'NVL_TRUC_TIEP' : line.SO_TIEN_621,
							'NHAN_CONG_TRUC_TIEP' : line.SO_TIEN_622,
							'NHAN_CONG_GIAN_TIEP' : line.SO_TIEN_6271,
							'CHI_PHI_NVL_GIAN_TIEP' : line.SO_TIEN_6272 + line.SO_TIEN_6273,
							# 'CHI_PHI_CONG_CU_SAN_XUAT' : line.SO_TIEN_6273,
							'CHI_PHI_KHAU_HAO' : line.SO_TIEN_6274,
							'CHI_PHI_MUA_NGOAI' : line.SO_TIEN_6277,
							'CHI_PHI_KHAC' : line.SO_TIEN_6278,
							
							
						}
			dict_chi_phi_do_dang_cuoi_ky = {}
			if self.GIA_THANH_KET_QUA_CHI_PHI_DO_DANG_CUOI_KY_CHI_TIET_IDS:
				for line in self.GIA_THANH_KET_QUA_CHI_PHI_DO_DANG_CUOI_KY_CHI_TIET_IDS:
					key = line.MA_DOI_TUONG_THCP_ID.id
					if key not in dict_chi_phi_do_dang_cuoi_ky:
						dict_chi_phi_do_dang_cuoi_ky[key] = {
							'NVL_TRUC_TIEP' : line.NVL_TRUC_TIEP,
							'NVL_GIAN_TIEP' : line.NVL_GIAN_TIEP,
							'NHAN_CONG_TRUC_TIEP' : line.NHAN_CONG_TRUC_TIEP,
							'NHAN_CONG_GIAN_TIEP' : line.NHAN_CONG_GIAN_TIEP,
							'KHAU_HAO' : line.KHAU_HAO,
							'CHI_PHI_MUA_NGOAI' : line.CHI_PHI_MUA_NGOAI,
							'CHI_PHI_KHAC' : line.CHI_PHI_KHAC,
						}
			# lấy tham số list vthh-dtthcp
			arr_vthh_dtthcp = []
			dict_dtthcp_vthh = {}
			if self.GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS:
				for line in self.GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS:
					list_vthh_dtthcp = str(line.MA_THANH_PHAM_ID.id) + ';' + str(line.MA_DOI_TUONG_THCP_ID.id)
					arr_vthh_dtthcp.append(list_vthh_dtthcp)
					key = line.MA_DOI_TUONG_THCP_ID.id
					if key not in dict_dtthcp_vthh:
						dict_dtthcp_vthh[key] = []
					dict_dtthcp_vthh[key] += [{
							'DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
							'MA_DOI_TUONG_THCP' : line.MA_DOI_TUONG_THCP_ID.MA_DOI_TUONG_THCP,
							'TEN_DOI_TUONG_THCP' : line.MA_DOI_TUONG_THCP_ID.TEN_DOI_TUONG_THCP,
							'MA_THANH_PHAM_ID' : line.MA_THANH_PHAM_ID.id,
							'MA_THANH_PHAM' : line.MA_THANH_PHAM_ID.MA,
							'TEN_THANH_PHAM' : line.MA_THANH_PHAM_ID.TEN,
							'DON_VI_TINH' : line.MA_THANH_PHAM_ID.DVT_CHINH_ID.id,
							'TEN_DVT' : line.MA_THANH_PHAM_ID.DVT_CHINH_ID.DON_VI_TINH,
							'TY_LE_PB_GIA_THANH' : 100,
						}]
			# cập nhật lại phần trăm pb giá thành khi tính theo hệ số tỷ lệ
			if dict_dtthcp_vthh:
				for dtthcp in dict_dtthcp_vthh:
					chi_tiet_ids = dict_dtthcp_vthh[dtthcp]
					for chi_tiet in chi_tiet_ids:
						key = str(chi_tiet.get('DOI_TUONG_THCP_ID')) + ',' + str(chi_tiet.get('MA_THANH_PHAM_ID'))
						if key in dict_phan_tram:
							chi_tiet['TY_LE_PB_GIA_THANH'] = dict_phan_tram[key]
					

			list_vthh_dtthcp_ts = ',' + ",".join(arr_vthh_dtthcp) + ','
			du_lieu_so_luong_hoan_thanh = self.btn_tinh_chi_phi_do_dang_so_Luong_cuoi_ky(self.KY_TINH_GIA_THANH_ONCHANGE,self.get_chi_nhanh(),list_vthh_dtthcp_ts)
			# Tính số lượng đầu kỳ
			dict_so_luong_hoan_thanh = {}
			if du_lieu_so_luong_hoan_thanh:
				for hoan_thanh in du_lieu_so_luong_hoan_thanh:
					key = hoan_thanh.get('MA_HANG_ID')
					if key not in dict_so_luong_hoan_thanh:
						dict_so_luong_hoan_thanh[key] = 0
					dict_so_luong_hoan_thanh[key] += hoan_thanh.get('SO_LUONG')
				
			if dict_dtthcp_vthh:
				for dtthcp in dict_dtthcp_vthh:
					chi_tiet_ids = dict_dtthcp_vthh[dtthcp]
					du_lieu_dau_ky = self.lay_du_lieu_tinh_gia_thanh(self.KY_TINH_GIA_THANH_ONCHANGE,dtthcp)
					
					so_luong_thanh_pham = 0
					
					# Tính dữ liệu đầu kỳ
					nvl_truc_tiep_dau_ky = 0
					nvl_gian_tiep_dau_ky = 0
					nhan_cong_truc_tiep_dau_ky = 0
					nhan_cong_gian_tiep_dau_ky = 0
					khau_hao_dau_ky = 0
					chi_phi_mua_ngoai_dau_ky = 0
					chi_phi_khac_dau_ky = 0
					if du_lieu_dau_ky:
						nvl_truc_tiep_dau_ky = du_lieu_dau_ky[0].get('NVL_TRUC_TIEP')
						nvl_gian_tiep_dau_ky = du_lieu_dau_ky[0].get('NVL_GIAN_TIEP')
						nhan_cong_truc_tiep_dau_ky = du_lieu_dau_ky[0].get('NHAN_CONG_TRUC_TIEP')
						nhan_cong_gian_tiep_dau_ky = du_lieu_dau_ky[0].get('NHAN_CONG_GIAN_TIEP')
						khau_hao_dau_ky = du_lieu_dau_ky[0].get('KHAU_HAO')
						chi_phi_mua_ngoai_dau_ky = du_lieu_dau_ky[0].get('GIA_TRI_MUA')
						chi_phi_khac_dau_ky = du_lieu_dau_ky[0].get('CHI_PHI_KHAC')
					
					# Tính chi phí phát sinh trong kỳ
					nvl_truc_tiep_trong_ky = 0
					nhan_cong_truc_tiep_trong_ky = 0
					chi_phi_mua_ngoai_trong_ky = 0
					nhan_cong_gian_tiep_trong_ky = 0
					if dtthcp in dict_phan_bo_chi_phi_chung:
						trong_ky = dict_phan_bo_chi_phi_chung[dtthcp]
						nvl_truc_tiep_trong_ky = trong_ky.get('NVL_TRUC_TIEP')
						nhan_cong_truc_tiep_trong_ky = trong_ky.get('NHAN_CONG_TRUC_TIEP')
						chi_phi_mua_ngoai_trong_ky = trong_ky.get('CHI_PHI_MUA_NGOAI')
						nhan_cong_gian_tiep_trong_ky = trong_ky.get('NHAN_CONG_GIAN_TIEP')

						nvl_gian_tiep_trong_ky = trong_ky.get('CHI_PHI_NVL_GIAN_TIEP')
						khau_hao_trong_ky = trong_ky.get('CHI_PHI_KHAU_HAO')
						khac_trong_ky = trong_ky.get('CHI_PHI_KHAC')
					
					# Tính chi phí dở dang
					nvl_truc_tiep_do_dang = 0
					nvl_gian_tiep_do_dang = 0
					nhan_cong_truc_tiep_do_dang = 0
					nhan_cong_gian_tiep_do_dang = 0
					khau_hao_do_dang = 0
					chi_phi_mua_ngoai_do_dang = 0
					chi_phi_khac_do_dang = 0
					if dtthcp in dict_chi_phi_do_dang_cuoi_ky:
						do_dang = dict_chi_phi_do_dang_cuoi_ky[dtthcp]
						nvl_truc_tiep_do_dang = do_dang.get('NVL_TRUC_TIEP')
						nvl_gian_tiep_do_dang = do_dang.get('NVL_GIAN_TIEP')
						nhan_cong_truc_tiep_do_dang = do_dang.get('NHAN_CONG_TRUC_TIEP')
						nhan_cong_gian_tiep_do_dang = do_dang.get('NHAN_CONG_GIAN_TIEP')
						khau_hao_do_dang = do_dang.get('KHAU_HAO')
						chi_phi_mua_ngoai_do_dang = do_dang.get('CHI_PHI_MUA_NGOAI')
						chi_phi_khac_do_dang = do_dang.get('CHI_PHI_KHAC')

					# Tính giá thành
					
					nvl_truc_tiep = nvl_truc_tiep_dau_ky + nvl_truc_tiep_trong_ky - nvl_truc_tiep_do_dang
					nvl_gian_tiep = nvl_gian_tiep_dau_ky + nvl_gian_tiep_trong_ky - nvl_gian_tiep_do_dang
					nhan_cong_truc_tiep = nhan_cong_truc_tiep_dau_ky + nhan_cong_truc_tiep_trong_ky - nhan_cong_truc_tiep_do_dang
					nhan_cong_gian_tiep = nhan_cong_gian_tiep_dau_ky + nhan_cong_gian_tiep_trong_ky - nhan_cong_gian_tiep_do_dang
					khau_hao = khau_hao_dau_ky + khau_hao_trong_ky - khau_hao_do_dang
					chi_phi_mua_ngoai = chi_phi_mua_ngoai_dau_ky + chi_phi_mua_ngoai_trong_ky - chi_phi_mua_ngoai_do_dang
					chi_phi_khac = chi_phi_khac_dau_ky + khac_trong_ky - chi_phi_khac_do_dang
					tong_chi_phi = nvl_truc_tiep + nvl_gian_tiep + nhan_cong_truc_tiep + nhan_cong_gian_tiep + khau_hao + chi_phi_mua_ngoai + chi_phi_khac

					arr_vthh_dtthcp = []
					if self.GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS:
						for line in self.GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS:
							arr_vthh_dtthcp.append(list_vthh_dtthcp)
					list_vthh_dtthcp_ts = ',' + ",".join(arr_vthh_dtthcp) + ','
					ky_tinh_gia_thanh_id = self.KY_TINH_GIA_THANH_ONCHANGE
					chi_nhanh_id = self.get_chi_nhanh()
					du_lieu_so_luong_hoan_thanh = self.btn_tinh_chi_phi_do_dang_so_Luong_cuoi_ky(ky_tinh_gia_thanh_id,chi_nhanh_id,list_vthh_dtthcp_ts)

					if du_lieu_so_luong_hoan_thanh:
					
						for chi_tiet in chi_tiet_ids:
							if chi_tiet.get('MA_THANH_PHAM_ID') in dict_so_luong_hoan_thanh:
								so_luong_thanh_pham = dict_so_luong_hoan_thanh[chi_tiet.get('MA_THANH_PHAM_ID')]

							ty_le_phan_bo_gia_thanh =  chi_tiet.get('TY_LE_PB_GIA_THANH')
							# if nvl_truc_tiep > 0 or nvl_gian_tiep > 0  or nhan_cong_truc_tiep > 0 or nhan_cong_gian_tiep > 0 or khau_hao > 0 or chi_phi_mua_ngoai > 0 or chi_phi_khac > 0:
							tong_chi_phi_cuoi = (tong_chi_phi*ty_le_phan_bo_gia_thanh)/100
							gia_thanh_don_vi = 0
							if so_luong_thanh_pham > 0:
								gia_thanh_don_vi = float_round(tong_chi_phi_cuoi/so_luong_thanh_pham,phan_thap_phan_gia_thanh_don_vi)
							new_line_bang_gia_thanh = env.new({
								# 'MA_THANH_PHAM_ID' : [chi_tiet.get('MA_THANH_PHAM_ID'),chi_tiet.get('MA_THANH_PHAM')],
								# 'TEN_THANH_PHAM' : chi_tiet.get('TEN_THANH_PHAM'),
								# 'MA_DOI_TUONG_THCP_ID' : [dtthcp,chi_tiet.get('MA_DOI_TUONG_THCP')],
								# 'TEN_DOI_TUONG_THCP' : chi_tiet.get('TEN_DOI_TUONG_THCP'),
								# 'DVT_ID' : [chi_tiet.get('DON_VI_TINH'),chi_tiet.get('TEN_DVT')],
								# 'TY_LE_PHAN_BO_GIA_THANH' : chi_tiet.get('TY_LE_PB_GIA_THANH'),

								'MA_THANH_PHAM_ID' : chi_tiet.get('MA_THANH_PHAM_ID'),
								'TEN_THANH_PHAM' : chi_tiet.get('TEN_THANH_PHAM'),
								'MA_DOI_TUONG_THCP_ID' : dtthcp,
								'TEN_DOI_TUONG_THCP' : chi_tiet.get('TEN_DOI_TUONG_THCP'),
								'DVT_ID' : chi_tiet.get('DON_VI_TINH'),
								'TY_LE_PHAN_BO_GIA_THANH' : ty_le_phan_bo_gia_thanh,

								'NVL_TRUC_TIEP' : (nvl_truc_tiep*ty_le_phan_bo_gia_thanh)/100,
								'NVL_GIAN_TIEP' : (nvl_gian_tiep*ty_le_phan_bo_gia_thanh)/100,
								'NHAN_CONG_TRUC_TIEP' : (nhan_cong_truc_tiep*ty_le_phan_bo_gia_thanh)/100,
								'NHAN_CONG_GIAN_TIEP' : (nhan_cong_gian_tiep*ty_le_phan_bo_gia_thanh)/100,
								'KHAU_HAO' : (khau_hao*ty_le_phan_bo_gia_thanh)/100,
								'CHI_PHI_MUA_NGOAI' : (chi_phi_mua_ngoai*ty_le_phan_bo_gia_thanh)/100,
								'CHI_PHI_KHAC' : (chi_phi_khac*ty_le_phan_bo_gia_thanh)/100,
								'TONG' : tong_chi_phi_cuoi,
								'SO_LUONG_THANH_PHAM' : so_luong_thanh_pham,
								'GIA_THANH_DON_VI' : gia_thanh_don_vi,
							})
							self.GIA_THANH_BANG_GIA_THANH_CHI_TIET_IDS += new_line_bang_gia_thanh 

	
	@api.onchange('ONCHANGE_CLICK_CAP_NHAT_GIA_NHAP_KHO')
	def _onchange_ONCHANGE_CLICK_CAP_NHAT_GIA_NHAP_KHO(self):
		if self.KY_TINH_GIA_THANH_ONCHANGE:
			if self.GIA_THANH_BANG_GIA_THANH_CHI_TIET_IDS:
				for line in self.GIA_THANH_BANG_GIA_THANH_CHI_TIET_IDS:
					vthh_id = line.MA_THANH_PHAM_ID.id
					dtthcp_id = line.MA_DOI_TUONG_THCP_ID.id
					tu_ngay = self.TU_NGAY
					den_ngay = self.DEN_NGAY
					chi_nhanh_id = self.get_chi_nhanh()
					tong_chi_phi = line.TONG
					don_gia_nhap = line.GIA_THANH_DON_VI
					self.cap_nhap_gia_nhap_kho(vthh_id,dtthcp_id,tu_ngay,den_ngay,chi_nhanh_id,tong_chi_phi,don_gia_nhap)

	
	@api.onchange('ONCHANGE_CLICK_CAP_NHAT_GIA_XUAT_KHO')
	def _onchange_ONCHANGE_CLICK_CAP_NHAT_GIA_XUAT_KHO(self):
		if self.KY_TINH_GIA_THANH_ONCHANGE:
			
			if self.GIA_THANH_BANG_GIA_THANH_CHI_TIET_IDS:
				list_vthh = ';'
				tu_ngay = self.TU_NGAY
				den_ngay = self.DEN_NGAY
				for line in self.GIA_THANH_BANG_GIA_THANH_CHI_TIET_IDS:
					list_vthh += str(line.MA_THANH_PHAM_ID.id)
					list_vthh += ';'
				self.env['stock.ex.tinh.gia.xuat.kho'].binh_quan_cuoi_ky(tu_ngay,den_ngay,list_vthh)
			# return {'warning': {
			# 					'title': 'Warning',
			# 					'message': 'My warning message.'
			# 				}
			# }

	@api.depends('GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS.SO_LUONG_THANH_PHAM_CHUAN','GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS.TIEU_CHUAN_PHAN_BO')
	def tinh_ty_le_phan_bo_gia_thanh(self):

		if self.GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS:
			# tong_so_luong_thanh_pham_chuan = 0
			dict_tong_sl = {}
			dict_tieu_chuan_pb = {}
			for line in self.GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS:
				key = line.DOI_TUONG_THCP_ID.id 
				if key not in dict_tong_sl:
					dict_tong_sl[key] = 0
				dict_tong_sl[key] += line.SO_LUONG_THANH_PHAM_CHUAN
				if key not in dict_tieu_chuan_pb:
					dict_tieu_chuan_pb[key] = 0
				dict_tieu_chuan_pb[key] += line.TIEU_CHUAN_PHAN_BO

			# for line in self.GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS:
			# 	key = line.DOI_TUONG_THCP_ID.id
			# 	# if key in dict_phuong_phap_xac_dinh:
			# 	if self.PHUONG_PHAP_XAC_DINH == 'HE_SO':
			# 		if key in dict_tong_sl and dict_tong_sl[key] != 0:
			# 			line.TY_LE_PHAN_BO_GIA_THANH = (line.SO_LUONG_THANH_PHAM_CHUAN/dict_tong_sl[key])*100
			# 	else:
			# 		if key in dict_tieu_chuan_pb and dict_tieu_chuan_pb[key] != 0:
			# 			line.TY_LE_PHAN_BO_GIA_THANH = (line.TIEU_CHUAN_PHAN_BO/dict_tieu_chuan_pb[key])*100
			
	
	# @api.model
	# def create(self, values):
	# 	result = super(GIA_THANH_TINH_GIA_THANH, self).create(values)
	# 	return result
	

	def luu_tinh_gia_thanh(self, args):
		# self.create()
		dict_unlink = {}
		dict_ky_tinh_gia_thanh_chi_tiet = {}

		# unlink phân bổ chi phí chung
		ket_qua_phan_bo_cp_chung_ids = self.env['gia.thanh.ket.qua.phan.bo.chi.phi.chung'].search([('KY_TINH_GIA_THANH_ID', '=', self.KY_TINH_GIA_THANH_ONCHANGE)])
		if ket_qua_phan_bo_cp_chung_ids:
			dict_unlink['gia.thanh.ket.qua.phan.bo.chi.phi.chung'] = []
			for chi_tiet in ket_qua_phan_bo_cp_chung_ids:
				dict_unlink['gia.thanh.ket.qua.phan.bo.chi.phi.chung'] += [chi_tiet.id]

		# unlink xác định dở dang
		chi_phi_do_dang_ids = self.env['gia.thanh.xac.dinh.do.dang'].search([('KY_TINH_GIA_THANH_ID', '=', self.KY_TINH_GIA_THANH_ONCHANGE)])
		if chi_phi_do_dang_ids:
			dict_unlink['gia.thanh.xac.dinh.do.dang'] = []
			for chi_tiet in chi_phi_do_dang_ids:
				dict_unlink['gia.thanh.xac.dinh.do.dang'] += [chi_tiet.id]

		# unlink bảng giá thành chi tiết
		bang_tinh_gia_thanh_chi_tiet_ids = self.env['gia.thanh.bang.gia.thanh.chi.tiet'].search([('KY_TINH_GIA_THANH_ID', '=', self.KY_TINH_GIA_THANH_ONCHANGE)])
		if bang_tinh_gia_thanh_chi_tiet_ids:
			dict_unlink['gia.thanh.bang.gia.thanh.chi.tiet'] = []
			for chi_tiet in bang_tinh_gia_thanh_chi_tiet_ids:
				dict_unlink['gia.thanh.bang.gia.thanh.chi.tiet'] += [chi_tiet.id]

		# unlink chi tiết chứng từ phân bổ chi phí chung
		chi_tiet_chung_tu_phan_bo_cp_chung_ids = self.env['gia.thanh.chi.tiet.chung.tu.phan.bo.chi.phi.chung'].search([('KY_TINH_GIA_THANH_ID', '=', self.KY_TINH_GIA_THANH_ONCHANGE)])
		if chi_tiet_chung_tu_phan_bo_cp_chung_ids:
			dict_unlink['gia.thanh.chi.tiet.chung.tu.phan.bo.chi.phi.chung'] = []
			for chi_tiet in chi_tiet_chung_tu_phan_bo_cp_chung_ids:
				dict_unlink['gia.thanh.chi.tiet.chung.tu.phan.bo.chi.phi.chung'] += [chi_tiet.id]

		# unlink chi tiết xác định tỷ lệ phân bổ đối tượng tính giá thánh
		xac_dinh_ty_le_phan_bo_doi_tuong_tinh_gia_thanh_ids = self.env['gia.thanh.xdtlpb.doi.tuong.tinh.gia.thanh.chi.tiet'].search([('KY_TINH_GIA_THANH_ID', '=', self.KY_TINH_GIA_THANH_ONCHANGE)])
		if xac_dinh_ty_le_phan_bo_doi_tuong_tinh_gia_thanh_ids:
			dict_unlink['gia.thanh.xdtlpb.doi.tuong.tinh.gia.thanh.chi.tiet'] = []
			for chi_tiet in xac_dinh_ty_le_phan_bo_doi_tuong_tinh_gia_thanh_ids:
				dict_unlink['gia.thanh.xdtlpb.doi.tuong.tinh.gia.thanh.chi.tiet'] += [chi_tiet.id]

		# unlink đối tượng thcp
		doi_tuong_thcp_ids = self.env['gia.thanh.ty.le.phan.bo.doi.tuong.thcp.chi.tiet'].search([('KY_TINH_GIA_THANH_ID', '=', self.KY_TINH_GIA_THANH_ONCHANGE)])
		if doi_tuong_thcp_ids:
			dict_unlink['gia.thanh.ty.le.phan.bo.doi.tuong.thcp.chi.tiet'] = []
			for chi_tiet in doi_tuong_thcp_ids:
				dict_unlink['gia.thanh.ty.le.phan.bo.doi.tuong.thcp.chi.tiet'] += [chi_tiet.id]

		# unlink xác định chi phí phân bổ
		xac_dinh_chi_phi_phan_bo_ids = self.env['gia.thanh.xac.dinh.chi.phi.phan.bo.chi.tiet'].search([('KY_TINH_GIA_THANH_ID', '=', self.KY_TINH_GIA_THANH_ONCHANGE)])
		if xac_dinh_chi_phi_phan_bo_ids:
			dict_unlink['gia.thanh.xac.dinh.chi.phi.phan.bo.chi.tiet'] = []
			for chi_tiet in xac_dinh_chi_phi_phan_bo_ids:
				dict_unlink['gia.thanh.xac.dinh.chi.phi.phan.bo.chi.tiet'] += [chi_tiet.id]

		# unlink kết quả phân bổ
		ket_phan_bo_ids = self.env['gia.thanh.ket.qua.phan.bo.chi.tiet'].search([('KY_TINH_GIA_THANH_ID', '=', self.KY_TINH_GIA_THANH_ONCHANGE)])
		if ket_phan_bo_ids:
			dict_unlink['gia.thanh.ket.qua.phan.bo.chi.tiet'] = []
			for chi_tiet in ket_phan_bo_ids:
				dict_unlink['gia.thanh.ket.qua.phan.bo.chi.tiet'] += [chi_tiet.id]

		if self.KY_TINH_GIA_THANH_ONCHANGE:
			ky_tinh_gia_thanh = self.env['gia.thanh.ky.tinh.gia.thanh'].browse(self.KY_TINH_GIA_THANH_ONCHANGE)
			if ky_tinh_gia_thanh:
				if ky_tinh_gia_thanh.GIA_THANH_KY_TINH_GIA_THANH_CHI_TIET_IDS:
					for chi_tiet in ky_tinh_gia_thanh.GIA_THANH_KY_TINH_GIA_THANH_CHI_TIET_IDS:

						if ky_tinh_gia_thanh.LOAI_GIA_THANH in ('DON_GIAN','HE_SO_TY_LE'):
							key = chi_tiet.MA_DOI_TUONG_THCP_ID.id
						elif ky_tinh_gia_thanh.LOAI_GIA_THANH == 'CONG_TRINH':
							key = chi_tiet.MA_CONG_TRINH_ID.id
						elif ky_tinh_gia_thanh.LOAI_GIA_THANH == 'DON_HANG':
							key = chi_tiet.SO_DON_HANG_ID.id
						elif ky_tinh_gia_thanh.LOAI_GIA_THANH == 'HOP_DONG':
							key = chi_tiet.SO_HOP_DONG_ID.id

						if key not in dict_ky_tinh_gia_thanh_chi_tiet:
							dict_ky_tinh_gia_thanh_chi_tiet[key] = chi_tiet.id

		arr_create_luu_theo_tk = []
		if self.CHE_DO_KE_TOAN == '15':
			if self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
				for line in self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
					ky_tinh_gia_thanh_chi_tiet = False

					if self.LOAI_TINH_GIA_THANH in ('HE_SO_TY_LE','GIAN_DON'):
						key = line.MA_DOI_TUONG_THCP_ID.id
					elif self.LOAI_TINH_GIA_THANH == 'CONG_TRINH':
						key = line.MA_CONG_TRINH_ID.id
					elif self.LOAI_TINH_GIA_THANH == 'DON_HANG':
						key = line.SO_DON_HANG_ID.id
					elif self.LOAI_TINH_GIA_THANH == 'HOP_DONG':
						key = line.HOP_DONG_BAN_ID.id

					if key in dict_ky_tinh_gia_thanh_chi_tiet:
						ky_tinh_gia_thanh_chi_tiet = dict_ky_tinh_gia_thanh_chi_tiet[key]
					if line.SO_TIEN_621 > 0:
						dict_luu_theo_tai_khoan = {
							'KY_TINH_GIA_THANH_ID' : line.KY_TINH_GIA_THANH_ID.id,
							'KY_TINH_GIA_THANH_CHI_TIET_ID' : ky_tinh_gia_thanh_chi_tiet,
							'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
							'MA_CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
							'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
							'SO_HOP_DONG_ID' : line.HOP_DONG_BAN_ID.id,
							'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('621'),
							'SO_TAI_KHOAN' : '621',
							'TY_LE' : line.TY_LE_PHAN_TRAM_621,
							'SO_TIEN' : line.SO_TIEN_621,
						}
						arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

					if line.SO_TIEN_622 > 0:
						dict_luu_theo_tai_khoan = {
							'KY_TINH_GIA_THANH_ID' : line.KY_TINH_GIA_THANH_ID.id,
							'KY_TINH_GIA_THANH_CHI_TIET_ID' : ky_tinh_gia_thanh_chi_tiet,
							'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
							'MA_CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
							'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
							'SO_HOP_DONG_ID' : line.HOP_DONG_BAN_ID.id,
							'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('622'),
							'SO_TAI_KHOAN' : '622',
							'TY_LE' : line.TY_LE_PHAN_TRAM_622,
							'SO_TIEN' : line.SO_TIEN_622,
						}
						arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

					if line.SO_TIEN_6271 > 0:
						dict_luu_theo_tai_khoan = {
							'KY_TINH_GIA_THANH_ID' : line.KY_TINH_GIA_THANH_ID.id,
							'KY_TINH_GIA_THANH_CHI_TIET_ID' : ky_tinh_gia_thanh_chi_tiet,
							'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
							'MA_CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
							'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
							'SO_HOP_DONG_ID' : line.HOP_DONG_BAN_ID.id,
							'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6271'),
							'SO_TAI_KHOAN' : '6271',
							'TY_LE' : line.TY_LE_PHAN_TRAM_6271,
							'SO_TIEN' : line.SO_TIEN_6271,
						}
						arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

					if line.SO_TIEN_6272 > 0:
						dict_luu_theo_tai_khoan = {
							'KY_TINH_GIA_THANH_ID' : line.KY_TINH_GIA_THANH_ID.id,
							'KY_TINH_GIA_THANH_CHI_TIET_ID' : ky_tinh_gia_thanh_chi_tiet,
							'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
							'MA_CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
							'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
							'SO_HOP_DONG_ID' : line.HOP_DONG_BAN_ID.id,
							'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6272'),
							'SO_TAI_KHOAN' : '6272',
							'TY_LE' : line.TY_LE_PHAN_TRAM_6272,
							'SO_TIEN' : line.SO_TIEN_6272,
						}
						arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

					if line.SO_TIEN_6273 > 0:
						dict_luu_theo_tai_khoan = {
							'KY_TINH_GIA_THANH_ID' : line.KY_TINH_GIA_THANH_ID.id,
							'KY_TINH_GIA_THANH_CHI_TIET_ID' : ky_tinh_gia_thanh_chi_tiet,
							'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
							'MA_CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
							'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
							'SO_HOP_DONG_ID' : line.HOP_DONG_BAN_ID.id,
							'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6273'),
							'SO_TAI_KHOAN' : '6273',
							'TY_LE' : line.TY_LE_PHAN_TRAM_6273,
							'SO_TIEN' : line.SO_TIEN_6273,
						}
						arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

					if line.SO_TIEN_6274 > 0:
						dict_luu_theo_tai_khoan = {
							'KY_TINH_GIA_THANH_ID' : line.KY_TINH_GIA_THANH_ID.id,
							'KY_TINH_GIA_THANH_CHI_TIET_ID' : ky_tinh_gia_thanh_chi_tiet,
							'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
							'MA_CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
							'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
							'SO_HOP_DONG_ID' : line.HOP_DONG_BAN_ID.id,
							'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6274'),
							'SO_TAI_KHOAN' : '6274',
							'TY_LE' : line.TY_LE_PHAN_TRAM_6274,
							'SO_TIEN' : line.SO_TIEN_6274,
						}
						arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

					if line.SO_TIEN_6277 > 0:
						dict_luu_theo_tai_khoan = {
							'KY_TINH_GIA_THANH_ID' : line.KY_TINH_GIA_THANH_ID.id,
							'KY_TINH_GIA_THANH_CHI_TIET_ID' : ky_tinh_gia_thanh_chi_tiet,
							'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
							'MA_CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
							'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
							'SO_HOP_DONG_ID' : line.HOP_DONG_BAN_ID.id,
							'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6277'),
							'SO_TAI_KHOAN' : '6277',
							'TY_LE' : line.TY_LE_PHAN_TRAM_6277,
							'SO_TIEN' : line.SO_TIEN_6277,
						}
						arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

					if line.SO_TIEN_6278 > 0:
						dict_luu_theo_tai_khoan = {
							'KY_TINH_GIA_THANH_ID' : line.KY_TINH_GIA_THANH_ID.id,
							'KY_TINH_GIA_THANH_CHI_TIET_ID' : ky_tinh_gia_thanh_chi_tiet,
							'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
							'MA_CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
							'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
							'SO_HOP_DONG_ID' : line.HOP_DONG_BAN_ID.id,
							'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6278'),
							'SO_TAI_KHOAN' : '6278',
							'TY_LE' : line.TY_LE_PHAN_TRAM_6278,
							'SO_TIEN' : line.SO_TIEN_6278,
						}
						arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

		elif self.CHE_DO_KE_TOAN == '48':

			ky_tinh_gia_thanh_chi_tiet = False
			if key in dict_ky_tinh_gia_thanh_chi_tiet:
				ky_tinh_gia_thanh_chi_tiet = dict_ky_tinh_gia_thanh_chi_tiet[key]

			arr_tai_khoan_621 = ['NVLTT','NVLTT_CT','NVLTT_SX']
			arr_tai_khoan_622 = ['NCTT_CT','NCTT_SX','NCTT']
			arr_tai_khoan_6271 = ['BH.NV','MTC.NC','QL.NV','SXC.NVCT','SXC.NVPX','SXC.NVSX']
			arr_tai_khoan_6272 = ['BH.NL','MTC.VL','QL.VL','SXC.VL']
			arr_tai_khoan_6273 = ['BH.DC','MTC.DCSX','QL.DC','SXC.DCSX','MTC']
			arr_tai_khoan_6274 = ['BH.KH','MTC.KH','QL.KH','SXC.KH','SXC.KH.CT','SXC.KH.SX']
			arr_tai_khoan_6277 = ['BH.MN','MTC.MN','QL.DV','SXC.MN','SXC.MN.CT','SXC.MN.SX']
			arr_tai_khoan_6278 = ['BH.K','MTC.K','QL.K','SXC.K','SXC.K.CT','SXC.K.SX','CPBH','CPQL','CPSX','SXC']


			dict_khoan_muc_cp = {}
			if self.GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS:
				for line in self.GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS:
					if line.SO_PHAN_BO_LAN_NAY > 0:
						key = line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP
						if key not in dict_khoan_muc_cp:
							dict_khoan_muc_cp[key] = line
						# arr_khoan_muc_cp.append(line.KHOAN_MUC_CP_ID.MA_KHOAN_MUC_CP)

			if dict_khoan_muc_cp:
				for khoan_muc in dict_khoan_muc_cp:
					xac_dinh_cp_pb = dict_khoan_muc_cp[khoan_muc]
					if self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
						for line in self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
							if khoan_muc in arr_tai_khoan_621:
								dict_luu_theo_tai_khoan = {
									'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,
									'KY_TINH_GIA_THANH_CHI_TIET_ID' : ky_tinh_gia_thanh_chi_tiet,
									'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
									'MA_CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
									'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
									'SO_HOP_DONG_ID' : line.HOP_DONG_BAN_ID.id,
									# 'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6278'),
									'KHOAN_MUC_CP_ID' : xac_dinh_cp_pb.KHOAN_MUC_CP_ID.id,
									'TY_LE' : line.TY_LE_PHAN_TRAM_621,
									'SO_TIEN' : (xac_dinh_cp_pb.SO_PHAN_BO_LAN_NAY*line.TY_LE_PHAN_TRAM_621)/100,
								}
								arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

							elif khoan_muc in arr_tai_khoan_622:
								dict_luu_theo_tai_khoan = {
									'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,
									'KY_TINH_GIA_THANH_CHI_TIET_ID' : ky_tinh_gia_thanh_chi_tiet,
									'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
									'MA_CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
									'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
									'SO_HOP_DONG_ID' : line.HOP_DONG_BAN_ID.id,
									# 'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6278'),
									'KHOAN_MUC_CP_ID' : xac_dinh_cp_pb.KHOAN_MUC_CP_ID.id,
									'TY_LE' : line.TY_LE_PHAN_TRAM_622,
									'SO_TIEN' : (xac_dinh_cp_pb.SO_PHAN_BO_LAN_NAY*line.TY_LE_PHAN_TRAM_622)/100,
								}
								arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)
							
							elif khoan_muc in arr_tai_khoan_6271:
								dict_luu_theo_tai_khoan = {
									'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,
									'KY_TINH_GIA_THANH_CHI_TIET_ID' : ky_tinh_gia_thanh_chi_tiet,
									'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
									'MA_CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
									'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
									'SO_HOP_DONG_ID' : line.HOP_DONG_BAN_ID.id,
									# 'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6278'),
									'KHOAN_MUC_CP_ID' : xac_dinh_cp_pb.KHOAN_MUC_CP_ID.id,
									'TY_LE' : line.TY_LE_PHAN_TRAM_6271,
									'SO_TIEN' : (xac_dinh_cp_pb.SO_PHAN_BO_LAN_NAY*line.TY_LE_PHAN_TRAM_6271)/100,
								}
								arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

							elif khoan_muc in arr_tai_khoan_6272:
								dict_luu_theo_tai_khoan = {
									'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,
									'KY_TINH_GIA_THANH_CHI_TIET_ID' : ky_tinh_gia_thanh_chi_tiet,
									'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
									'MA_CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
									'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
									'SO_HOP_DONG_ID' : line.HOP_DONG_BAN_ID.id,
									# 'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6278'),
									'KHOAN_MUC_CP_ID' : xac_dinh_cp_pb.KHOAN_MUC_CP_ID.id,
									'TY_LE' : line.TY_LE_PHAN_TRAM_6272,
									'SO_TIEN' : (xac_dinh_cp_pb.SO_PHAN_BO_LAN_NAY*line.TY_LE_PHAN_TRAM_6272)/100,
								}
								arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

							elif khoan_muc in arr_tai_khoan_6273:
								dict_luu_theo_tai_khoan = {
									'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,
									'KY_TINH_GIA_THANH_CHI_TIET_ID' : ky_tinh_gia_thanh_chi_tiet,
									'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
									'MA_CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
									'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
									'SO_HOP_DONG_ID' : line.HOP_DONG_BAN_ID.id,
									# 'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6278'),
									'KHOAN_MUC_CP_ID' : xac_dinh_cp_pb.KHOAN_MUC_CP_ID.id,
									'TY_LE' : line.TY_LE_PHAN_TRAM_6273,
									'SO_TIEN' : (xac_dinh_cp_pb.SO_PHAN_BO_LAN_NAY*line.TY_LE_PHAN_TRAM_6273)/100,
								}
								arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

							elif khoan_muc in arr_tai_khoan_6274:
								dict_luu_theo_tai_khoan = {
									'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,
									'KY_TINH_GIA_THANH_CHI_TIET_ID' : ky_tinh_gia_thanh_chi_tiet,
									'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
									'MA_CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
									'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
									'SO_HOP_DONG_ID' : line.HOP_DONG_BAN_ID.id,
									# 'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6278'),
									'KHOAN_MUC_CP_ID' : xac_dinh_cp_pb.KHOAN_MUC_CP_ID.id,
									'TY_LE' : line.TY_LE_PHAN_TRAM_6274,
									'SO_TIEN' : (xac_dinh_cp_pb.SO_PHAN_BO_LAN_NAY*line.TY_LE_PHAN_TRAM_6274)/100,
								}
								arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

							elif khoan_muc in arr_tai_khoan_6277:
								dict_luu_theo_tai_khoan = {
									'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,
									'KY_TINH_GIA_THANH_CHI_TIET_ID' : ky_tinh_gia_thanh_chi_tiet,
									'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
									'MA_CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
									'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
									'SO_HOP_DONG_ID' : line.HOP_DONG_BAN_ID.id,
									# 'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6278'),
									'KHOAN_MUC_CP_ID' : xac_dinh_cp_pb.KHOAN_MUC_CP_ID.id,
									'TY_LE' : line.TY_LE_PHAN_TRAM_6277,
									'SO_TIEN' : (xac_dinh_cp_pb.SO_PHAN_BO_LAN_NAY*line.TY_LE_PHAN_TRAM_6277)/100,
								}
								arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

							elif khoan_muc in arr_tai_khoan_6278:
								dict_luu_theo_tai_khoan = {
									'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,
									'KY_TINH_GIA_THANH_CHI_TIET_ID' : ky_tinh_gia_thanh_chi_tiet,
									'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
									'MA_CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
									'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
									'SO_HOP_DONG_ID' : line.HOP_DONG_BAN_ID.id,
									# 'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6278'),
									'KHOAN_MUC_CP_ID' : xac_dinh_cp_pb.KHOAN_MUC_CP_ID.id,
									'TY_LE' : line.TY_LE_PHAN_TRAM_6278,
									'SO_TIEN' : (xac_dinh_cp_pb.SO_PHAN_BO_LAN_NAY*line.TY_LE_PHAN_TRAM_6278)/100,
								}
								arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)


			

		dict_xac_dinh_do_dang_chi_tiet = {}
		if self.GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS:
			for line in self.GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS:
				key = line.MA_DOI_TUONG_THCP_ID.id
				if key not in dict_xac_dinh_do_dang_chi_tiet:
					dict_xac_dinh_do_dang_chi_tiet [key] = []
				
				ky_tinh_gia_thanh_chi_tiet = False
				if key in dict_ky_tinh_gia_thanh_chi_tiet:
					ky_tinh_gia_thanh_chi_tiet = dict_ky_tinh_gia_thanh_chi_tiet[key]
				dict_xac_dinh_do_dang_chi_tiet [key] += [(0,0,{
					'MA_THANH_PHAM_ID' : line.MA_THANH_PHAM_ID.id,
					'SL_DO_DANG_CUOI_KY' : line.SL_DO_DANG_CUOI_KY,
					'PHAN_TRAM_HOAN_THANH' : line.PHAN_TRAM_HOAN_THANH,
					'DON_GIA_DINH_MUC' : line.DON_GIA_DINH_MUC,

				})]
		
		# dict_ket_qua_chi_tiet_cuoi_ky = {}
		arr_create_xac_dinh_do_dang = []
		if self.GIA_THANH_KET_QUA_CHI_PHI_DO_DANG_CUOI_KY_CHI_TIET_IDS:
			for line in self.GIA_THANH_KET_QUA_CHI_PHI_DO_DANG_CUOI_KY_CHI_TIET_IDS:
				key = line.MA_DOI_TUONG_THCP_ID.id
				chi_tiet_ids = False
				if key in dict_xac_dinh_do_dang_chi_tiet:
					chi_tiet_ids = dict_xac_dinh_do_dang_chi_tiet[key]
				# if key not in dict_ket_qua_chi_tiet_cuoi_ky:
				# 	dict_ket_qua_chi_tiet_cuoi_ky[key] = []
				new_line_ket_qua_do_dang_cuoi_ky = [(0,0,{
						'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,
						'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
						'TONG_CHI_PHI' : line.TONG_CHI_PHI,
						'NVL_TRUC_TIEP' : line.NVL_TRUC_TIEP,
						'NVL_GIAN_TIEP' : line.NVL_GIAN_TIEP,
						'NHAN_CONG_TRUC_TIEP' : line.NHAN_CONG_TRUC_TIEP,
						'NHAN_CONG_GIAN_TIEP' : line.NHAN_CONG_GIAN_TIEP,
						'KHAU_HAO' : line.KHAU_HAO,
						'CHI_PHI_MUA_NGOAI' : line.CHI_PHI_MUA_NGOAI,
						'CHI_PHI_KHAC' : line.CHI_PHI_KHAC,
						'GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS' : chi_tiet_ids,
					})]
				ky_tinh_gia_thanh_chi_tiet = False
				if key in dict_ky_tinh_gia_thanh_chi_tiet:
					ky_tinh_gia_thanh_chi_tiet = dict_ky_tinh_gia_thanh_chi_tiet[key]
				new_line_xac_dinh_do_dang = {
							'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,
							'KY_TINH_GIA_THANH_CHI_TIET_ID' : ky_tinh_gia_thanh_chi_tiet,
							'DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
							'GIA_THANH_KET_QUA_CHI_PHI_DO_DANG_CUOI_KY_CHI_TIET_IDS' : new_line_ket_qua_do_dang_cuoi_ky,
					}
				
				arr_create_xac_dinh_do_dang.append(new_line_xac_dinh_do_dang)


		
		# Lưu bảng tính giá thành cuối cùng
		arr_create_bang_gia_thanh_cuoi = []
		if self.GIA_THANH_BANG_GIA_THANH_CHI_TIET_IDS:
			for line in self.GIA_THANH_BANG_GIA_THANH_CHI_TIET_IDS:
				# line.KY_TINH_GIA_THANH_ID = self.KY_TINH_GIA_THANH_ONCHANGE
				line_create = {
					'MA_THANH_PHAM_ID' : line.MA_THANH_PHAM_ID.id,
					'TEN_THANH_PHAM' : line.TEN_THANH_PHAM,
					'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
					'TEN_DOI_TUONG_THCP' : line.TEN_DOI_TUONG_THCP,
					'DVT_ID' : line.DVT_ID.id,
					'TY_LE_PHAN_BO_GIA_THANH' : line.TY_LE_PHAN_BO_GIA_THANH,
					'NVL_TRUC_TIEP' : line.NVL_TRUC_TIEP,
					'NVL_GIAN_TIEP' : line.NVL_GIAN_TIEP,
					'NHAN_CONG_TRUC_TIEP' : line.NHAN_CONG_TRUC_TIEP,
					'NHAN_CONG_GIAN_TIEP' : line.NHAN_CONG_GIAN_TIEP,
					'KHAU_HAO' : line.KHAU_HAO,
					'CHI_PHI_MUA_NGOAI' : line.CHI_PHI_MUA_NGOAI,
					'CHI_PHI_KHAC' : line.CHI_PHI_KHAC,
					'TONG' : line.TONG,
					'SO_LUONG_THANH_PHAM' : line.SO_LUONG_THANH_PHAM,
					'GIA_THANH_DON_VI' : line.GIA_THANH_DON_VI,
					'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,
				}
				
				arr_create_bang_gia_thanh_cuoi.append(line_create)


		
		# Lưu bảng giá thành chi tiết chứng từ phân bổ chi phí
		arr_create_chi_tiet_ct = []
		if self.GIA_THANH_CHI_TIET_CHUNG_TU_PHAN_BO_CHI_PHI_CHUNG_IDS:
			for line in self.GIA_THANH_CHI_TIET_CHUNG_TU_PHAN_BO_CHI_PHI_CHUNG_IDS:
				# line.KY_TINH_GIA_THANH_ID = self.KY_TINH_GIA_THANH_ONCHANGE
				line_create = {
					'NGAY_CHUNG_TU' : line.NGAY_CHUNG_TU,
					'SO_CHUNG_TU' : line.SO_CHUNG_TU,
					'LOAI_CHUNG_TU' : line.LOAI_CHUNG_TU,
					'DIEN_GIAI' : line.DIEN_GIAI,
					'TK_CHI_PHI_ID' : line.TK_CHI_PHI_ID.id,
					'SO_TIEN' : line.SO_TIEN,
					'SO_CHUA_PHAN_BO' : line.SO_CHUA_PHAN_BO,
					'SO_PHAN_BO_LAN_NAY' : line.SO_PHAN_BO_LAN_NAY,
					'TY_LE_PHAN_BO' : line.TY_LE_PHAN_BO,
					'ID_GOC' : line.ID_GOC,
					'MODEL_GOC' : line.MODEL_GOC,
					'KHOAN_MUC_CP_ID' : line.KHOAN_MUC_CP_ID.id,
					'NGAY_HACH_TOAN' : line.NGAY_HACH_TOAN,
					'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,
				}
				
				arr_create_chi_tiet_ct.append(line_create)

		arr_xac_dinh_ty_le_pb = []
		if self.GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS:
			for line in self.GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET_IDS:
				line_create = {
					'DOI_TUONG_THCP_ID' : line.DOI_TUONG_THCP_ID.id,
					'MA_THANH_PHAM_ID' : line.MA_THANH_PHAM_ID.id,
					'TEN_THANH_PHAM' : line.TEN_THANH_PHAM,
					'LA_THANH_PHAM_CHUAN' : line.LA_THANH_PHAM_CHUAN,
					'SO_LUONG_THANH_PHAM' : line.SO_LUONG_THANH_PHAM,
					'GIA_THANH_DINH_MUC' : line.GIA_THANH_DINH_MUC,
					'HE_SO' : line.HE_SO,
					'SO_LUONG_THANH_PHAM_CHUAN' : line.SO_LUONG_THANH_PHAM_CHUAN,
					'TIEU_CHUAN_PHAN_BO' : line.TIEU_CHUAN_PHAN_BO,
					'TY_LE_PHAN_BO_GIA_THANH' : line.TY_LE_PHAN_BO_GIA_THANH,
					'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,
				}
				arr_xac_dinh_ty_le_pb.append(line_create)

		arr_doi_tuong_thcp = []
		if self.GIA_THANH_TY_LE_PHAN_BO_DOI_TUONG_THCP_CHI_TIET_IDS:
			for line in self.GIA_THANH_TY_LE_PHAN_BO_DOI_TUONG_THCP_CHI_TIET_IDS:
				line_create = {
					'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
					'TEN_DOI_TUONG_THCP' : line.TEN_DOI_TUONG_THCP,
					'LOAI_DOI_TUONG_THCP' : line.LOAI_DOI_TUONG_THCP,
					'PHUONG_PHAP_XAC_DINH' : line.PHUONG_PHAP_XAC_DINH,
					'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,
				}
				arr_doi_tuong_thcp.append(line_create)

		arr_xac_dinh_chi_phi_phan_bo = []
		if self.GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS:
			for line in self.GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_IDS:
				line_create = {
					'TAI_KHOAN_ID' : line.TAI_KHOAN_ID.id if self.CHE_DO_KE_TOAN == '15' else False,
					'TEN_TAI_KHOAN' : line.TEN_TAI_KHOAN if self.CHE_DO_KE_TOAN == '15' else False,
					'KHOAN_MUC_CP_ID' : line.KHOAN_MUC_CP_ID.id if self.CHE_DO_KE_TOAN == '48' else False,
					'TEN_KHOAN_MUC_CP' : line.TEN_KHOAN_MUC_CP if self.CHE_DO_KE_TOAN == '48' else False,
					'TONG_SO_TIEN' : line.TONG_SO_TIEN,
					'SO_CHUA_PHAN_BO' : line.SO_CHUA_PHAN_BO,
					'PHAN_TRAM_PB_LAN_NAY' : line.PHAN_TRAM_PB_LAN_NAY,
					'SO_PHAN_BO_LAN_NAY' : line.SO_PHAN_BO_LAN_NAY,
					'TIEU_THUC_PHAN_BO' : line.TIEU_THUC_PHAN_BO,
					# 'DOI_TUONG_THCP_ID' : line.DOI_TUONG_THCP_ID.id,
					# 'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
					# 'CONG_TRINH_ID' : line.CONG_TRINH_ID.id,
					# 'HOP_DONG_BAN_ID' : line.HOP_DONG_BAN_ID.id,
					'CHI_TIET_CHUNG_TU' : line.CHI_TIET_CHUNG_TU,
					'CHI_TIET_ID' : line.CHI_TIET_ID.id,
					'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,
				}
				arr_xac_dinh_chi_phi_phan_bo.append(line_create)

		arr_ket_qua_phan_bo = []
		if self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
			for line in self.GIA_THANH_KET_QUA_PHAN_BO_CHI_TIET_IDS:
				line_create = {
					'MA_DOI_TUONG_THCP_ID' : line.MA_DOI_TUONG_THCP_ID.id,
					'TEN_DOI_TUONG_THCP' : line.TEN_DOI_TUONG_THCP,
					'LOAI_DOI_TUONG_THCP' : line.LOAI_DOI_TUONG_THCP,
					'MA_CONG_TRINH_ID' : line.MA_CONG_TRINH_ID.id,
					'TEN_CONG_TRINH' : line.TEN_CONG_TRINH,
					'LOAI_CONG_TRINH' : line.LOAI_CONG_TRINH.id,
					'SO_DON_HANG_ID' : line.SO_DON_HANG_ID.id,
					'NGAY_DON_HANG' : line.NGAY_DON_HANG,
					'KHACH_HANG' : line.KHACH_HANG.id,
					'HOP_DONG_BAN_ID' : line.HOP_DONG_BAN_ID.id,
					'NGAY_KY' : line.NGAY_KY,
					'TRICH_YEU' : line.TRICH_YEU,

					'TY_LE_PHAN_TRAM_621' : line.TY_LE_PHAN_TRAM_621,
					'SO_TIEN_621' : line.SO_TIEN_621,
					'TY_LE_PHAN_TRAM_622' : line.TY_LE_PHAN_TRAM_622,
					'SO_TIEN_622' : line.SO_TIEN_622,
					'TY_LE_PHAN_TRAM_6271' : line.TY_LE_PHAN_TRAM_6271,
					'SO_TIEN_6271' : line.SO_TIEN_6271,
					'TY_LE_PHAN_TRAM_6272' : line.TY_LE_PHAN_TRAM_6272,
					'SO_TIEN_6272' : line.SO_TIEN_6272,
					'TY_LE_PHAN_TRAM_6273' : line.TY_LE_PHAN_TRAM_6273,
					'SO_TIEN_6273' : line.SO_TIEN_6273,
					'TY_LE_PHAN_TRAM_6274' : line.TY_LE_PHAN_TRAM_6274,
					'SO_TIEN_6274' : line.SO_TIEN_6274,
					'TY_LE_PHAN_TRAM_6277' : line.TY_LE_PHAN_TRAM_6277,
					'SO_TIEN_6277' : line.SO_TIEN_6277,
					'TY_LE_PHAN_TRAM_6278' : line.TY_LE_PHAN_TRAM_6278,
					'SO_TIEN_6278' : line.SO_TIEN_6278,
					'TONG_CHI_PHI' : line.TONG_CHI_PHI,
					'KY_TINH_GIA_THANH_ID' : self.KY_TINH_GIA_THANH_ONCHANGE,
				}
				arr_ket_qua_phan_bo.append(line_create)

		# xóa các chứng từ cũ
		if dict_unlink:
			for model in dict_unlink:
				id_ids = dict_unlink[model]
				for id_xoa in id_ids:
					self.env[model].browse(id_xoa).unlink()

		# Tạo các chứng từ
		if arr_create_luu_theo_tk:
			for line in arr_create_luu_theo_tk:
				self.env['gia.thanh.ket.qua.phan.bo.chi.phi.chung'].create(line)
		if arr_create_chi_tiet_ct:
			for line in arr_create_chi_tiet_ct:
				self.env['gia.thanh.chi.tiet.chung.tu.phan.bo.chi.phi.chung'].create(line)
		if arr_create_bang_gia_thanh_cuoi:
			for line in arr_create_bang_gia_thanh_cuoi:
				self.env['gia.thanh.bang.gia.thanh.chi.tiet'].create(line)
		if arr_create_xac_dinh_do_dang:
			for line in arr_create_xac_dinh_do_dang:
				self.env['gia.thanh.xac.dinh.do.dang'].create(line)
		if arr_xac_dinh_ty_le_pb:
			for line in arr_xac_dinh_ty_le_pb:
				self.env['gia.thanh.xdtlpb.doi.tuong.tinh.gia.thanh.chi.tiet'].create(line)
		if arr_doi_tuong_thcp:
			for line in arr_doi_tuong_thcp:
				self.env['gia.thanh.ty.le.phan.bo.doi.tuong.thcp.chi.tiet'].create(line)
		if arr_xac_dinh_chi_phi_phan_bo:
			for line in arr_xac_dinh_chi_phi_phan_bo:
				self.env['gia.thanh.xac.dinh.chi.phi.phan.bo.chi.tiet'].create(line)
		if arr_ket_qua_phan_bo:
			for line in arr_ket_qua_phan_bo:
				self.env['gia.thanh.ket.qua.phan.bo.chi.tiet'].create(line)

	def get_id_by_so_tai_khoan(self,so_tai_khoan):
		id = False
		tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', so_tai_khoan)],limit=1)
		if tai_khoan:
			id = tai_khoan.id
		return id
	
	def lay_du_lieu_xac_dinh_chi_phi_phan_bo(self,ky_tinh_gia_thanh_id,chi_nhanh_id):
		params = {
			'KY_TINH_GIA_THANH_ID' : ky_tinh_gia_thanh_id,
			'CHI_NHANH_ID' : chi_nhanh_id,
			}
		query = """  
			DO LANGUAGE plpgsql $$
			DECLARE

				ky_tinh_gia_thanh_id           INTEGER := %(KY_TINH_GIA_THANH_ID)s;


				chi_nhanh_id                   INTEGER := %(CHI_NHANH_ID)s;

				CHE_DO_KE_TOAN                 VARCHAR;

				tu_ngay                        TIMESTAMP;

				den_ngay                       TIMESTAMP;

				LOAI_GIA_THANH                 VARCHAR;

				MA_PHAN_CAPNVLTT               VARCHAR(100);

				MA_PHAN_CAPNCTT                VARCHAR(100);

				MA_PHAN_CAPSXC                 VARCHAR(100);

				MA_PHAN_CAPDMTC                VARCHAR(100);


				PHAN_THAP_PHAN_SO_TIEN_QUY_DOI INT;

				KIEM_TRA_CHI_PHI_SAN_XUAT      BOOLEAN;


			BEGIN


				SELECT value
				INTO CHE_DO_KE_TOAN
				FROM ir_config_parameter
				WHERE key = 'he_thong.CHE_DO_KE_TOAN'
				FETCH FIRST 1 ROW ONLY
				;





				SELECT value
				INTO PHAN_THAP_PHAN_SO_TIEN_QUY_DOI
				FROM ir_config_parameter
				WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI'
				FETCH FIRST 1 ROW ONLY
				;

				SELECT "TU_NGAY"
				INTO tu_ngay
				FROM gia_thanh_ky_tinh_gia_thanh AS JP
				WHERE "id" = ky_tinh_gia_thanh_id
				;

				SELECT "DEN_NGAY"
				INTO den_ngay
				FROM gia_thanh_ky_tinh_gia_thanh AS JP
				WHERE "id" = ky_tinh_gia_thanh_id
				;

				SELECT "LOAI_GIA_THANH"
				INTO LOAI_GIA_THANH
				FROM gia_thanh_ky_tinh_gia_thanh AS JP
				WHERE "id" = ky_tinh_gia_thanh_id
				;


				DROP TABLE IF EXISTS TMP_KET_QUA
				;

				CREATE TEMP TABLE TMP_KET_QUA

				(
					"ID_TAI_KHOAN"       INT             NOT NULL, -- ID của TK/ Khoản mục
					"MA_TAI_KHOAN"       VARCHAR(20)     NOT NULL, -- Mã TK/khoản mục
					"TEN_TAI_KHOAN"      VARCHAR(255), -- Tên TK/Khoản mục
					"MA_PHAN_CAP"        VARCHAR(255), -- Tên TK/Khoản mục
					"TONG_SO_TIEN"       DECIMAL(22, 4)  NULL, -- Tổng số tiền
					"TONG_SO_TIEN_Blane" DECIMAL(22, 4)  NULL DEFAULT 0, -- Tổng số tiền
					"SO_CHUA_PHAN_BO"    DECIMAL(22, 4)  NULL, -- Số chưa phân bổ
					"TY_LE_PB"           DECIMAL(24, 10) NULL, -- Tỷ lệ
					"SO_TIEN_PB_LAN_NAY" DECIMAL(22, 4)  NULL -- Số tiền
				)
				;


				IF EXISTS(SELECT *
						FROM gia_thanh_ky_tinh_gia_thanh AS JP
							LEFT JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung AS JCAD ON JCAD."KY_TINH_GIA_THANH_ID" = JP."id"
							LEFT JOIN gia_thanh_ket_qua_chi_phi_do_dang_cuoi_ky_chi_tiet AS JUD
								ON JUD."KY_TINH_GIA_THANH_ID" = JP."id"
							LEFT JOIN gia_thanh_bang_gia_thanh_chi_tiet AS JPCD ON JPCD."KY_TINH_GIA_THANH_ID" = JP."id"
							LEFT JOIN gia_thanh_xdtlpb_doi_tuong_tinh_gia_thanh_chi_tiet AS JPCAC
								ON JP."id" = JPCAC."KY_TINH_GIA_THANH_ID"
						WHERE (JCAD.id IS NOT NULL
								OR JUD.id IS NOT NULL
								OR JPCD.id IS NOT NULL
								)
								AND JP."id" = ky_tinh_gia_thanh_id
						LIMIT 1)
				THEN
					KIEM_TRA_CHI_PHI_SAN_XUAT = TRUE
					;
				ELSE
					KIEM_TRA_CHI_PHI_SAN_XUAT = FALSE
					;
				END IF
				;


				IF PHAN_THAP_PHAN_SO_TIEN_QUY_DOI IS NULL
				THEN
					PHAN_THAP_PHAN_SO_TIEN_QUY_DOI = 0
					;
				END IF
				;


				DROP TABLE IF EXISTS TMP_TAI_KHOAN
				;

				IF CHE_DO_KE_TOAN = '15'
				--Quyết định 15, lấy theo tài khoản
				THEN


					CREATE TEMP TABLE TMP_TAI_KHOAN

					(
						"TAI_KHOAN_ID"  INT,
						"SO_TAI_KHOAN"  VARCHAR(20),
						"TEN_TAI_KHOAN" VARCHAR(128),
						"MA_PHAN_CAP"   VARCHAR(255)
					)
					;

					INSERT INTO TMP_TAI_KHOAN
					("TAI_KHOAN_ID",
					"SO_TAI_KHOAN",
					"TEN_TAI_KHOAN",
					"MA_PHAN_CAP"

					)
						SELECT
							"id" AS "TAI_KHOAN_ID"
							, "SO_TAI_KHOAN"
							, "TEN_TAI_KHOAN"
							, "MA_PHAN_CAP"
						FROM danh_muc_he_thong_tai_khoan AS A
						WHERE ("SO_TAI_KHOAN" LIKE '621%%'
							OR "SO_TAI_KHOAN" LIKE '622%%'
							OR "SO_TAI_KHOAN" LIKE '627%%'

							OR (LOAI_GIA_THANH = 'CONG_TRINH'
								AND "SO_TAI_KHOAN" LIKE '623%%'
							)
							)
							AND "LA_TK_TONG_HOP" = FALSE
					;


					INSERT INTO TMP_KET_QUA
					(
						"ID_TAI_KHOAN",
						"MA_TAI_KHOAN",
						"TEN_TAI_KHOAN",
						"MA_PHAN_CAP",
						"TONG_SO_TIEN",
						"SO_CHUA_PHAN_BO",
						"TY_LE_PB",
						"SO_TIEN_PB_LAN_NAY"
					)
						SELECT
							A."TAI_KHOAN_ID"
							, -- ItemID - INT
							A."SO_TAI_KHOAN"
							, -- "MA_TAI_KHOAN" - nvarchar(20)
							A."TEN_TAI_KHOAN"
							, -- "TEN_TAI_KHOAN" - nvarchar(255)
							A."MA_PHAN_CAP"
							, SUM(COALESCE(GL."GHI_NO", 0) - COALESCE(GL."GHI_CO", 0)) AS "TONG_SO_TIEN"
							, -- Tổng số tiền
							0
							, -- Số chưa phân bổ
							100
							, -- Ngầm định 100%%
							0 --"SO_TIEN_PB_LAN_NAY" - decimal
						FROM TMP_TAI_KHOAN AS A
							INNER JOIN so_cai_chi_tiet AS GL ON A."SO_TAI_KHOAN" = GL."MA_TAI_KHOAN"
																AND GL."CHI_NHANH_ID" = chi_nhanh_id

						WHERE GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

							AND GL."DOI_TUONG_THCP_ID" IS NULL
							AND GL."DON_DAT_HANG_ID" IS NULL
							AND GL."HOP_DONG_BAN_ID" IS NULL
							AND GL."CONG_TRINH_ID" IS NULL

							AND ((GL."LOAI_HACH_TOAN" = '2'
									AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
								)
								OR GL."LOAI_HACH_TOAN" = '1'
							)
						GROUP BY
							A."TAI_KHOAN_ID"
							, -- ItemID - INT
							A."SO_TAI_KHOAN"
							, -- "MA_TAI_KHOAN" - nvarchar(20)
							A."TEN_TAI_KHOAN"
							, -- "TEN_TAI_KHOAN" - nvarchar(255)
							A."MA_PHAN_CAP"
					;


					INSERT INTO TMP_KET_QUA
					(
						"ID_TAI_KHOAN",
						"MA_TAI_KHOAN",
						"TEN_TAI_KHOAN",
						"MA_PHAN_CAP",
						"TONG_SO_TIEN",
						"SO_CHUA_PHAN_BO",
						"TY_LE_PB",
						"SO_TIEN_PB_LAN_NAY"
					)
						SELECT
							A."TAI_KHOAN_ID"
							, A."SO_TAI_KHOAN"
							, A."TEN_TAI_KHOAN"
							, A."MA_PHAN_CAP"
							, 0
							, 0
							, 100
							, SUM("SO_PHAN_BO_LAN_NAY")
						FROM TMP_TAI_KHOAN AS A
							INNER JOIN gia_thanh_chi_tiet_chung_tu_phan_bo_chi_phi_chung AS JCV
								ON A."TAI_KHOAN_ID" = JCV."TK_CHI_PHI_ID"
							LEFT JOIN gia_thanh_ky_tinh_gia_thanh AS JP ON JCV."KY_TINH_GIA_THANH_ID" = JP."id"

						WHERE

							JCV."KY_TINH_GIA_THANH_ID" <> ky_tinh_gia_thanh_id
							AND "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
							AND "CHI_NHANH_ID" = chi_nhanh_id
						GROUP BY
							A."TAI_KHOAN_ID"
							, A."SO_TAI_KHOAN"
							, A."TEN_TAI_KHOAN"
							, A."MA_PHAN_CAP"
					;


					DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
					;

					CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
						AS

							SELECT
								"ID_TAI_KHOAN"
								, "MA_TAI_KHOAN"
								, "TEN_TAI_KHOAN"
								, "MA_PHAN_CAP"

								, ROUND(CAST(COALESCE(SUM("TONG_SO_TIEN"), 0) AS NUMERIC),
										PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "TONG_SO_TIEN"
								,
								ROUND(CAST(COALESCE(SUM("TONG_SO_TIEN" - "SO_TIEN_PB_LAN_NAY"), 0) AS NUMERIC),
										PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)

							AS "SO_CHUA_PHAN_BO"


								, CASE WHEN MAX("TEMP_SO_DA_PHAN_BO") IS NULL
								THEN CASE WHEN KIEM_TRA_CHI_PHI_SAN_XUAT = TRUE
									THEN 0
									ELSE 100
									END
								ELSE COALESCE(A."TY_LE_PHAN_BO", 100)
								END                                   AS "TY_LE_PB"
								, CASE WHEN MAX("TEMP_SO_DA_PHAN_BO") IS NULL
								THEN CASE WHEN KIEM_TRA_CHI_PHI_SAN_XUAT = TRUE
									THEN 0
									ELSE ROUND(CAST(COALESCE(SUM("TONG_SO_TIEN" - "SO_TIEN_PB_LAN_NAY"), 0) AS NUMERIC),
												PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
									END
								ELSE ROUND(CAST(COALESCE(MAX("TEMP_SO_DA_PHAN_BO"), 0) AS NUMERIC),
											PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
								END                                   AS "SO_TIEN_PB_LAN_NAY"

								, 0                                     AS "ID_CHUNG_TU_CHI_TIET"
							FROM TMP_KET_QUA AS R
								LEFT JOIN (SELECT
												(SELECT "SO_TAI_KHOAN"
												FROM danh_muc_he_thong_tai_khoan TK
												WHERE TK.id = "TK_CHI_PHI_ID") AS "SO_TAI_KHOAN"
											, SUM("SO_PHAN_BO_LAN_NAY")       AS "TEMP_SO_DA_PHAN_BO"
											, SUM("SO_TIEN")                  AS "TEMP_TONG_SO_TIEN"
											, MAX("TY_LE_PHAN_BO")            AS "TY_LE_PHAN_BO"
										FROM gia_thanh_chi_tiet_chung_tu_phan_bo_chi_phi_chung AS JCV
										WHERE "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
										GROUP BY
											"TK_CHI_PHI_ID"
										) A ON R."MA_TAI_KHOAN" = A."SO_TAI_KHOAN"
							GROUP BY
								"ID_TAI_KHOAN",
								"MA_TAI_KHOAN",
								"TEN_TAI_KHOAN",
								"MA_PHAN_CAP",
								a."TY_LE_PHAN_BO"
							HAVING
								ROUND(CAST(SUM("TONG_SO_TIEN" - "SO_TIEN_PB_LAN_NAY") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) >
								0
							ORDER BY "MA_TAI_KHOAN"
					;


				ELSE


					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPNVLTT
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'NVLTT'
					;

					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPNCTT
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'NCTT'
					;

					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPSXC
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'SXC'
					;

					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPDMTC
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'MTC'
					;


					DROP TABLE IF EXISTS TMP_KHOAN_MUC_CP
					;

					CREATE TEMP TABLE TMP_KHOAN_MUC_CP

					(
						"KHOAN_MUC_CP_ID"  INT,
						"MA_KHOAN_MUC_CP"  VARCHAR(20),
						"TEN_KHOAN_MUC_CP" VARCHAR(128),
						"MA_PHAN_CAP"      VARCHAR(255)
					);

					INSERT INTO TMP_KHOAN_MUC_CP
					(
						"KHOAN_MUC_CP_ID"  ,
						"MA_KHOAN_MUC_CP"  ,
						"TEN_KHOAN_MUC_CP" ,
						"MA_PHAN_CAP"

					)
					SELECT
						"id" AS "KHOAN_MUC_CP_ID"
						, "MA_KHOAN_MUC_CP"
						, "TEN_KHOAN_MUC_CP"
						, "MA_PHAN_CAP"
					FROM danh_muc_khoan_muc_cp AS EI
					WHERE ("MA_PHAN_CAP" LIKE MA_PHAN_CAPNVLTT || '%%'
																OR "MA_PHAN_CAP" LIKE MA_PHAN_CAPNCTT || '%%'
						OR "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC || '%%'
						)
						OR (LOAI_GIA_THANH = 'CONG_TRINH'
							AND "MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPDMTC || '%%'
							)
							--AND "LA_TK_TONG_HOP" = 0
					;



					INSERT INTO TMP_KET_QUA
					("ID_TAI_KHOAN",
					"MA_TAI_KHOAN",
					"TEN_TAI_KHOAN",
					"MA_PHAN_CAP",
					"TONG_SO_TIEN",
					"TONG_SO_TIEN_Blane",
					"SO_CHUA_PHAN_BO",
					"TY_LE_PB",
					"SO_TIEN_PB_LAN_NAY"
					)
						SELECT
							A."KHOAN_MUC_CP_ID"
							, -- ItemID - INT
							A."MA_KHOAN_MUC_CP"
							, -- "MA_TAI_KHOAN" - nvarchar(20)
							A."TEN_KHOAN_MUC_CP"
							, -- "TEN_TAI_KHOAN" - nvarchar(255)
							A."MA_PHAN_CAP"
							, SUM(COALESCE(GL."GHI_NO", 0) - COALESCE(GL."GHI_CO", 0)) AS "TONG_SO_TIEN"
							, -- Tổng số tiền
							SUM(COALESCE(GL."GHI_NO", 0) - COALESCE(GL."GHI_CO", 0)) AS "TONG_SO_TIEN"
							, -- Tổng số tiền
							0
							, -- Số chưa phân bổ
							100
							, -- Ngầm định 100%%
							0 --"SO_TIEN_PB_LAN_NAY" - decimal
						FROM TMP_KHOAN_MUC_CP AS A
					LEFT JOIN so_cai_chi_tiet AS GL ON A."KHOAN_MUC_CP_ID" = GL."KHOAN_MUC_CP_ID"
					AND GL."CHI_NHANH_ID" = chi_nhanh_id

					WHERE
					GL."NGAY_HACH_TOAN" <= den_ngay

					AND "DOI_TUONG_THCP_ID" IS NULL
					AND "DON_DAT_HANG_ID" IS NULL
					AND GL."HOP_DONG_BAN_ID" IS NULL
					AND "CONG_TRINH_ID" IS NULL

					AND "MA_TAI_KHOAN" LIKE '154%%'
					GROUP BY
						A."KHOAN_MUC_CP_ID",
						A."MA_KHOAN_MUC_CP",
						a."TEN_KHOAN_MUC_CP",
						A."MA_PHAN_CAP"
					;


					INSERT INTO TMP_KET_QUA
					("ID_TAI_KHOAN",
					"MA_TAI_KHOAN",
					"TEN_TAI_KHOAN",
					"MA_PHAN_CAP",
					"TONG_SO_TIEN",
					"TONG_SO_TIEN_Blane",
					"SO_CHUA_PHAN_BO",
					"TY_LE_PB",
					"SO_TIEN_PB_LAN_NAY"
					)

						SELECT
							A."KHOAN_MUC_CP_ID"
							, A."MA_KHOAN_MUC_CP"
							, A."TEN_KHOAN_MUC_CP"
							, A."MA_PHAN_CAP"
							, 0
							, (-1) * SUM(CASE WHEN JP."DEN_NGAY" < den_ngay
							THEN COALESCE("SO_PHAN_BO_LAN_NAY", 0)
										ELSE 0
										END)
							, 0
							, 100
							, SUM(COALESCE("SO_PHAN_BO_LAN_NAY", 0))
						FROM TMP_KHOAN_MUC_CP AS A
					INNER JOIN gia_thanh_chi_tiet_chung_tu_phan_bo_chi_phi_chung AS JCV ON A."KHOAN_MUC_CP_ID" = JCV."KHOAN_MUC_CP_ID"
					LEFT JOIN gia_thanh_ky_tinh_gia_thanh AS JP ON JCV."KY_TINH_GIA_THANH_ID" = JP."id"

					WHERE

					JCV."KY_TINH_GIA_THANH_ID" <> ky_tinh_gia_thanh_id
					AND "CHI_NHANH_ID" = chi_nhanh_id

					AND "NGAY_HACH_TOAN" <= den_ngay
					GROUP BY
						A."KHOAN_MUC_CP_ID",
					A."MA_KHOAN_MUC_CP",
					A."MA_PHAN_CAP",
					A."TEN_KHOAN_MUC_CP";



					DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
					;

					CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
						AS

					SELECT
						"ID_TAI_KHOAN"
						, "MA_TAI_KHOAN"
						, "TEN_TAI_KHOAN"
						, "MA_PHAN_CAP"
						, ROUND(CAST(SUM("TONG_SO_TIEN_Blane") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)                  AS "TONG_SO_TIEN"
						, ROUND(CAST(SUM("TONG_SO_TIEN" - "SO_TIEN_PB_LAN_NAY")AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "SO_CHUA_PHAN_BO"
						,
						CASE WHEN MAX("TEMP_SO_DA_PHAN_BO") IS NULL
							THEN CASE WHEN KIEM_TRA_CHI_PHI_SAN_XUAT = TRUE
								THEN 0
								ELSE 100
								END
						ELSE COALESCE(A."TY_LE_PHAN_BO", 100)
						END                                                                               AS "TY_LE_PB"
						,

						CASE WHEN MAX("TEMP_SO_DA_PHAN_BO") IS NULL
							THEN CASE WHEN KIEM_TRA_CHI_PHI_SAN_XUAT = TRUE
								THEN 0
								ELSE ROUND(CAST(COALESCE(SUM("TONG_SO_TIEN" - "SO_TIEN_PB_LAN_NAY"), 0) AS NUMERIC),
											PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
								END
						ELSE ROUND(CAST(COALESCE(MAX("TEMP_SO_DA_PHAN_BO"), 0) AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
						END                                                                               AS "SO_TIEN_PB_LAN_NAY"
						,0                                                                         AS "ID_CHUNG_TU_CHI_TIET"
					FROM TMP_KET_QUA AS R
						LEFT JOIN (SELECT
									"KHOAN_MUC_CP_ID"
									, SUM("SO_PHAN_BO_LAN_NAY") AS  "TEMP_SO_DA_PHAN_BO"
									, SUM("SO_TIEN")  AS  "TEMP_TONG_SO_TIEN"
									, MAX("TY_LE_PHAN_BO") AS "TY_LE_PHAN_BO"
								FROM gia_thanh_chi_tiet_chung_tu_phan_bo_chi_phi_chung AS JCV
								WHERE "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
								GROUP BY "KHOAN_MUC_CP_ID"
								) A ON R."ID_TAI_KHOAN" = A."KHOAN_MUC_CP_ID"
					GROUP BY
						"ID_TAI_KHOAN",
						"MA_TAI_KHOAN",
						"TEN_TAI_KHOAN",
						"MA_PHAN_CAP",
						A."TY_LE_PHAN_BO"
					HAVING ROUND(CAST(SUM("TONG_SO_TIEN" - "SO_TIEN_PB_LAN_NAY") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) > 0
					ORDER BY "MA_TAI_KHOAN" ;


				END IF
				;

			END $$
			;


			SELECT *
			FROM TMP_KET_QUA_CUOI_CUNG --where "MA_TAI_KHOAN" ='621'

			;
 
		"""  
		return self.execute(query, params)



	def lay_du_lieu_xac_dinh_chi_phi_phan_bo_ct_dh_hd(self,ky_tinh_gia_thanh_id,chi_nhanh_id):
		params = {
			'KY_TINH_GIA_THANH_ID' : ky_tinh_gia_thanh_id,
			'CHI_NHANH_ID' : chi_nhanh_id,
			}
		query = """   

			DO LANGUAGE plpgsql $$
			DECLARE


				ky_tinh_gia_thanh_id             INTEGER := %(KY_TINH_GIA_THANH_ID)s;

				v_chi_nhanh_id                   INTEGER := %(CHI_NHANH_ID)s;



				LOAI_GIA_THANH                   VARCHAR;


				v_tu_ngay                        TIMESTAMP;

				v_den_ngay                       TIMESTAMP;

				CHE_DO_KE_TOAN                   VARCHAR;

				PHAN_THAP_PHAN_SO_TIEN_QUY_DOI   INTEGER;

				MA_PHAN_CAP_NVLTT                VARCHAR(100);

				MA_PHAN_CAP_NCTT                 VARCHAR(100);

				MA_PHAN_CAP_SXC                  VARCHAR(100);

				MA_PHAN_CAP_MTC                  VARCHAR(100);


			BEGIN




				SELECT value
				INTO CHE_DO_KE_TOAN
				FROM ir_config_parameter
				WHERE key = 'he_thong.CHE_DO_KE_TOAN'
				FETCH FIRST 1 ROW ONLY
				;


				SELECT value
				INTO PHAN_THAP_PHAN_SO_TIEN_QUY_DOI
				FROM ir_config_parameter
				WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI'
				FETCH FIRST 1 ROW ONLY
				;


				SELECT "TU_NGAY"
				INTO v_tu_ngay


				FROM gia_thanh_ky_tinh_gia_thanh AS JP
				WHERE JP."id" = ky_tinh_gia_thanh_id
				;

				SELECT "DEN_NGAY"
				INTO v_den_ngay

				FROM gia_thanh_ky_tinh_gia_thanh AS JP
				WHERE JP."id" = ky_tinh_gia_thanh_id
				;

				SELECT "CHI_NHANH_ID"
				INTO v_chi_nhanh_id


				FROM gia_thanh_ky_tinh_gia_thanh AS JP
				WHERE JP."id" = ky_tinh_gia_thanh_id
				;

				SELECT "LOAI_GIA_THANH"
				INTO LOAI_GIA_THANH

				FROM gia_thanh_ky_tinh_gia_thanh AS JP
				WHERE JP."id" = ky_tinh_gia_thanh_id
				;


				DROP TABLE IF EXISTS TMP_KET_QUA
				;

				CREATE TEMP TABLE TMP_KET_QUA

				(
					"TK_KHOAN_MUC_ID"     INT            NOT NULL, -- ID của TK/ Khoản mục
					"MA_TK_KHOAN_MUC"     VARCHAR(20)    NOT NULL, -- Mã TK/khoản mục
					"TEN_TK_KHOAN_MUC"    VARCHAR(255), -- Tên TK/Khoản mục
					"TONG_SO_TIEN"        DECIMAL(22, 4) NULL, -- Tổng số tiền
					"TONG_SO_TIEN_BLANCE" DECIMAL(22, 4) NULL DEFAULT 0, -- Tổng số tiền
					"SO_CHUA_PHAN_BO"     DECIMAL(22, 4) NULL, -- Số chưa phân bổ
					"TY_LE"               DECIMAL(22, 4) NULL, -- Tỷ lệ
					"SO_PHAN_BO_LAN_NAY"  DECIMAL(22, 4) NULL, -- Số tiền,
					"MA_PHAN_CAP"         VARCHAR(255)
				)
				;


				IF PHAN_THAP_PHAN_SO_TIEN_QUY_DOI IS NULL
				THEN
					PHAN_THAP_PHAN_SO_TIEN_QUY_DOI = 0
					;

				END IF
				;


				-- Lấy dữ liệu hiển thị lên giao diện
				IF CHE_DO_KE_TOAN = '15'
				--Quyết định 15, lấy theo tài khoản
				THEN

					DROP TABLE IF EXISTS TMP_TAI_KHOAN
					;

					CREATE TEMP TABLE TMP_TAI_KHOAN

					(
						"TAI_KHOAN_ID"   INT,
						"TK_CONG_NO"     VARCHAR(20),
						"TEN_TK_DOI_UNG" VARCHAR(128),
						"MA_PHAN_CAP"    VARCHAR(255)
					)
					;

					INSERT INTO TMP_TAI_KHOAN
					(
						"TAI_KHOAN_ID",
						"TK_CONG_NO",
						"TEN_TK_DOI_UNG",
						"MA_PHAN_CAP"
					)
						SELECT
							"id"
							, "SO_TAI_KHOAN"
							, "TEN_TAI_KHOAN"
							, "MA_PHAN_CAP"
						FROM danh_muc_he_thong_tai_khoan AS A
						WHERE
							("SO_TAI_KHOAN" LIKE '621%%'
							OR "SO_TAI_KHOAN" LIKE '622%%'
							OR "SO_TAI_KHOAN" LIKE '627%%'
							--Nếu là công trình thì lấy thêm chi phí thi công chung để phân bổ
							OR (LOAI_GIA_THANH = 'CONG_TRINH' AND "SO_TAI_KHOAN" LIKE '623%%')
							) AND
							"LA_TK_TONG_HOP" = FALSE
					;


					INSERT INTO TMP_KET_QUA
					("TK_KHOAN_MUC_ID",
					"MA_TK_KHOAN_MUC",
					"TEN_TK_KHOAN_MUC",
					"MA_PHAN_CAP",
					"TONG_SO_TIEN",
					"SO_CHUA_PHAN_BO",
					"TY_LE",
					"SO_PHAN_BO_LAN_NAY"

					)
						SELECT
							A."TAI_KHOAN_ID"
							, -- "TK_KHOAN_MUC_ID" - INT
							A."TK_CONG_NO"
							, -- "MA_TK_KHOAN_MUC" - nvarchar(20)
							A."TEN_TK_DOI_UNG"
							, -- "TEN_TK_KHOAN_MUC" - nvarchar(255),
							A."MA_PHAN_CAP"
							, SUM(COALESCE(GL."SUM_GHI_NO", 0) - COALESCE(GL."SUM_GHI_CO", 0)) AS "TONG_SO_TIEN"
							, -- Tổng số tiền
							SUM(COALESCE(GL."SUM_GHI_NO", 0) - COALESCE(GL."SUM_GHI_CO", 0) -
								COALESCE(GL."SO_PHAN_BO_LAN_NAY", 0))
							, -- Số chưa phân bổ
							100
							, -- Ngầm định 100%%
							SUM(COALESCE(GL."SUM_GHI_NO", 0) - COALESCE(GL."SUM_GHI_CO", 0) -
								COALESCE(GL."SO_PHAN_BO_LAN_NAY", 0)) -- "SO_PHAN_BO_LAN_NAY" - decimal
						FROM TMP_TAI_KHOAN AS A
							INNER JOIN (
										SELECT DISTINCT
											GL."ID_CHUNG_TU"
											, GL."MA_TAI_KHOAN"
											, SUM(GL."GHI_NO")                                          AS "SUM_GHI_NO"
											, SUM(GL."GHI_CO")                                          AS "SUM_GHI_CO"
											, LAY_SO_TIEN_DA_PHAN_BO_CUA_CHUNG_TU(GL."ID_CHUNG_TU", GL."MA_TAI_KHOAN", NULL
										, CHE_DO_KE_TOAN,
																					ky_tinh_gia_thanh_id) AS "SO_PHAN_BO_LAN_NAY"
										FROM so_cai_chi_tiet AS GL

										WHERE GL."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay


												AND GL."CHI_NHANH_ID" = v_chi_nhanh_id
												AND (GL."CONG_TRINH_ID" IS NULL AND GL."DON_DAT_HANG_ID" IS NULL AND
													GL."HOP_DONG_BAN_ID" IS NULL AND GL."DOI_TUONG_THCP_ID" IS NULL)
												AND (
													(GL."MA_TAI_KHOAN" LIKE '621%%'
													OR GL."MA_TAI_KHOAN" LIKE '622%%'
													OR GL."MA_TAI_KHOAN" LIKE '627%%'

													OR (LOAI_GIA_THANH = 'CONG_TRINH' AND GL."MA_TAI_KHOAN" LIKE '623%%')
													)
													AND ((GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND "LOAI_HACH_TOAN" = '2') OR
														"LOAI_HACH_TOAN" = '1')
												)

										GROUP BY GL."ID_CHUNG_TU", GL."MA_TAI_KHOAN"
									) AS GL ON A."TK_CONG_NO" = GL."MA_TAI_KHOAN"

						GROUP BY A."TAI_KHOAN_ID",
							A."TK_CONG_NO",
							A."TEN_TK_DOI_UNG",
							A."MA_PHAN_CAP"

						HAVING SUM(COALESCE(GL."SUM_GHI_NO", 0) - COALESCE(GL."SUM_GHI_CO", 0) -
								COALESCE(GL."SO_PHAN_BO_LAN_NAY", 0)) > 0
					;


					DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
					;

					CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
						AS

							SELECT
								"TK_KHOAN_MUC_ID"
								, -- ID của TK/ Khoản mục
								"MA_TK_KHOAN_MUC"
								, -- Mã TK/khoản mục
								"TEN_TK_KHOAN_MUC"
								, -- Tên TK/Khoản mục
								ROUND(CAST(("TONG_SO_TIEN") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) AS "TONG_SO_TIEN"
								, -- Tổng số tiền
								ROUND(CAST(("SO_CHUA_PHAN_BO") AS NUMERIC),
										PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)                                    AS "SO_CHUA_PHAN_BO"
								, -- Số chưa phân bổ
								"TY_LE"
								, -- Tỷ lệ
								ROUND(CAST(("SO_PHAN_BO_LAN_NAY") AS NUMERIC),
										PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)                                    AS "SO_PHAN_BO_LAN_NAY"
								, -- Số tiền,
								"MA_PHAN_CAP"
								, N'Xem'                                                                  AS "CHI_TIET_CHENH_LECH"
							FROM TMP_KET_QUA
							ORDER BY "MA_TK_KHOAN_MUC"


					;

				ELSE


					--1. Lấy tất cả các khoản mục chi phí cho sản xuất: NVLTT, NCTT, SXC, MTC
					DROP TABLE IF EXISTS TMP_KHOAN_MUC_CHI_PHI
					;

					CREATE TEMP TABLE TMP_KHOAN_MUC_CHI_PHI


					(
						"KHOAN_MUC_CP_ID"  INT,
						"MA_KHOAN_MUC_CP"  VARCHAR(255),
						"TEN_KHOAN_MUC_CP" VARCHAR(255),
						"MA_PHAN_CAP"      VARCHAR(255)
					)
					;


					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAP_NVLTT
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'NVLTT'
					;

					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAP_NCTT
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'NCTT'
					;

					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAP_SXC
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'SXC'
					;

					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAP_MTC
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'MTC'
					;

					INSERT INTO TMP_KHOAN_MUC_CHI_PHI
					("KHOAN_MUC_CP_ID", "MA_KHOAN_MUC_CP", "TEN_KHOAN_MUC_CP", "MA_PHAN_CAP")
						SELECT
							E."id"
							, E."MA_KHOAN_MUC_CP"
							, E."TEN_KHOAN_MUC_CP"
							, E."MA_PHAN_CAP"
						FROM danh_muc_khoan_muc_cp E
						WHERE E."LA_TONG_HOP" = FALSE
							AND (
								(E."MA_PHAN_CAP" LIKE (MA_PHAN_CAP_NVLTT || '%%'))
								OR (E."MA_PHAN_CAP" LIKE (MA_PHAN_CAP_NCTT || '%%'))
								OR (E."MA_PHAN_CAP" LIKE (MA_PHAN_CAP_SXC || '%%'))
								OR (LOAI_GIA_THANH = 'CONG_TRINH' AND E."MA_PHAN_CAP" LIKE (MA_PHAN_CAP_MTC || '%%'))
							)
						ORDER BY "MA_PHAN_CAP" ASC
					;


					-- Lấy dữ liệu theo QD 48
					INSERT INTO TMP_KET_QUA
					("TK_KHOAN_MUC_ID",
					"MA_TK_KHOAN_MUC",
					"TEN_TK_KHOAN_MUC",
					"MA_PHAN_CAP",
					"TONG_SO_TIEN",
					"TONG_SO_TIEN_BLANCE",
					"SO_CHUA_PHAN_BO",
					"TY_LE",
					"SO_PHAN_BO_LAN_NAY"

					)
						SELECT
							A."KHOAN_MUC_CP_ID"
							, -- "TK_KHOAN_MUC_ID" - INT
							A."MA_KHOAN_MUC_CP"
							, -- "MA_TK_KHOAN_MUC" - nvarchar(20)
							A."TEN_KHOAN_MUC_CP"
							, -- "TEN_TK_KHOAN_MUC" - nvarchar(255)
							A."MA_PHAN_CAP"
							, SUM(COALESCE(GL."GHI_NO", 0)
								- COALESCE(GL."GHI_CO", 0)) AS "TONG_SO_TIEN"
							, -- Tổng số tiền
							SUM(COALESCE(GL."GHI_NO", 0)
								- COALESCE(GL."GHI_CO", 0)) AS "TONG_SO_TIEN"
							, -- Tổng số tiền
							0
							, -- Số chưa phân bổ
							100
							, -- Ngầm định 100%%
							0 -- "SO_PHAN_BO_LAN_NAY" - decimal
						FROM TMP_KHOAN_MUC_CHI_PHI AS A
							LEFT JOIN so_cai_chi_tiet AS GL ON A."KHOAN_MUC_CP_ID" = GL."KHOAN_MUC_CP_ID"
															AND GL."CHI_NHANH_ID" = v_chi_nhanh_id

						WHERE
							GL."NGAY_HACH_TOAN" <= v_den_ngay

							AND "DOI_TUONG_THCP_ID" IS NULL
							AND "DON_DAT_HANG_ID" IS NULL
							AND "HOP_DONG_BAN_ID" IS NULL
							AND "CONG_TRINH_ID" IS NULL

							AND "MA_TAI_KHOAN" LIKE '154%%'
						GROUP BY A."KHOAN_MUC_CP_ID",
							A."MA_KHOAN_MUC_CP",
							a."TEN_KHOAN_MUC_CP",
							A."MA_PHAN_CAP"
					;


					INSERT INTO TMP_KET_QUA
					("TK_KHOAN_MUC_ID",
					"MA_TK_KHOAN_MUC",
					"TEN_TK_KHOAN_MUC",
					"MA_PHAN_CAP",
					"TONG_SO_TIEN",
					"TONG_SO_TIEN_BLANCE",
					"SO_CHUA_PHAN_BO",
					"TY_LE",
					"SO_PHAN_BO_LAN_NAY"
					)
						SELECT
							A."KHOAN_MUC_CP_ID"
							, A."MA_KHOAN_MUC_CP"
							, A."TEN_KHOAN_MUC_CP"
							, A."MA_PHAN_CAP"
							, 0
							, (-1) * SUM(CASE WHEN JP."DEN_NGAY" < v_den_ngay
							THEN COALESCE("SO_PHAN_BO_LAN_NAY", 0)
										ELSE 0 END)
							, 0
							, 100
							, SUM(COALESCE("SO_PHAN_BO_LAN_NAY", 0))
						FROM TMP_KHOAN_MUC_CHI_PHI AS A
							INNER JOIN gia_thanh_chi_tiet_chung_tu_phan_bo_chi_phi_chung AS JCV
								ON A."KHOAN_MUC_CP_ID" = JCV."KHOAN_MUC_CP_ID"
							LEFT JOIN gia_thanh_ky_tinh_gia_thanh AS JP ON JCV."KY_TINH_GIA_THANH_ID" = JP."id"

						WHERE JCV."KY_TINH_GIA_THANH_ID" <> ky_tinh_gia_thanh_id
							AND "CHI_NHANH_ID" = v_chi_nhanh_id

							AND "NGAY_HACH_TOAN" <= v_den_ngay
						GROUP BY A."KHOAN_MUC_CP_ID",
							A."MA_KHOAN_MUC_CP",
							A."MA_PHAN_CAP",
							A."TEN_KHOAN_MUC_CP"
					;



					DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG;
					CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
						AS


					SELECT
						"TK_KHOAN_MUC_ID"
						, "MA_TK_KHOAN_MUC"
						, "TEN_TK_KHOAN_MUC"
						, "MA_PHAN_CAP"
						, ROUND(CAST(SUM("TONG_SO_TIEN_BLANCE") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)                 AS "TONG_SO_TIEN"
						, ROUND(CAST(SUM("TONG_SO_TIEN" - "SO_PHAN_BO_LAN_NAY") AS NUMERIC),
								PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)                                                              AS "SO_CHUA_PHAN_BO"
						,
						100                                                                                                AS "TY_LE"
						, ROUND(CAST(SUM("TONG_SO_TIEN" - "SO_PHAN_BO_LAN_NAY") AS NUMERIC),
								PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)                                                              AS "SO_PHAN_BO_LAN_NAY"
						,
						0                                                                                                  AS RefDetailID
					FROM TMP_KET_QUA AS R
						LEFT JOIN (SELECT
									"KHOAN_MUC_CP_ID"
									, SUM("SO_PHAN_BO_LAN_NAY") AS "Temp_SO_DA_PHAN_BO"
								FROM gia_thanh_chi_tiet_chung_tu_phan_bo_chi_phi_chung AS JCV
								WHERE "KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
								GROUP BY "KHOAN_MUC_CP_ID") A
							ON R."TK_KHOAN_MUC_ID" = A."KHOAN_MUC_CP_ID"
					GROUP BY "TK_KHOAN_MUC_ID",
						"MA_TK_KHOAN_MUC",
						"TEN_TK_KHOAN_MUC",
						"MA_PHAN_CAP"
					HAVING ROUND(CAST(SUM("TONG_SO_TIEN" - "SO_PHAN_BO_LAN_NAY") AS NUMERIC), PHAN_THAP_PHAN_SO_TIEN_QUY_DOI) > 0
					ORDER BY "MA_TK_KHOAN_MUC"
					;

				END IF
				;

			END $$
			;


			SELECT *
			FROM TMP_KET_QUA_CUOI_CUNG
			ORDER BY "MA_TK_KHOAN_MUC"  ;


		"""  
		return self.execute(query, params)

	def lay_du_lieu_ket_qua_phan_bo(self,ky_tinh_gia_thanh_id):
		params = {
			'KY_TINH_GIA_THANH' : ky_tinh_gia_thanh_id,
			}
		query = """   
				DO LANGUAGE plpgsql $$
				DECLARE
				
					ky_tinh_gia_thanh_id      INTEGER := %(KY_TINH_GIA_THANH)s;
				
				
				BEGIN
				
					DROP TABLE IF EXISTS TMP_KET_QUA_PHAN_BO;
					CREATE TEMP TABLE TMP_KET_QUA_PHAN_BO
						AS
				
					SELECT
								JC."id" AS "KY_TINH_GIA_THANH_CHI_TIET_ID",
								JC."KY_TINH_GIA_THANH_ID" ,
								JC."MA_DOI_TUONG_THCP_ID" ,
								J."MA_DOI_TUONG_THCP" ,
								J."TEN_DOI_TUONG_THCP" ,
								J."LOAI" ,
								JC."MA_CONG_TRINH_ID" ,
								CT."MA_CONG_TRINH" ,
								CT."TEN_CONG_TRINH" ,
								CT."LOAI_CONG_TRINH" ,
								LCT."name" AS "TEN_LOAI_CONG_TRINH",

								JC."SO_DON_HANG_ID",
								DDH."SO_DON_HANG",
								DDH."KHACH_HANG_ID",
								DDH."NGAY_DON_HANG",
								KH."HO_VA_TEN" AS "TEN_KHACH_HANG",

								JC."SO_HOP_DONG_ID" AS "HOP_DONG_BAN_ID",
								HDB."SO_HOP_DONG",
								HDB."NGAY_KY",
								HDB."TRICH_YEU",

								0 AS "TONG_TIEN_PHAN_BO" ,

								JC."STT"
						FROM    gia_thanh_ky_tinh_gia_thanh_chi_tiet JC
								LEFT JOIN danh_muc_doi_tuong_tap_hop_chi_phi J ON JC."MA_DOI_TUONG_THCP_ID" = J."id"
								LEFT JOIN danh_muc_cong_trinh CT ON JC."MA_CONG_TRINH_ID" = CT."id"
								LEFT JOIN danh_muc_loai_cong_trinh LCT ON CT."LOAI_CONG_TRINH" = LCT."id"
								LEFT JOIN account_ex_don_dat_hang DDH ON JC."SO_DON_HANG_ID" = DDH."id"
								LEFT JOIN res_partner KH ON DDH."KHACH_HANG_ID" = KH.id
								LEFT JOIN sale_ex_hop_dong_ban HDB ON JC."SO_HOP_DONG_ID" = HDB."id"
				
						WHERE   JC."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
						ORDER BY
						"STT" ;
				
				
				END $$
				;
				
				
				SELECT *
				FROM TMP_KET_QUA_PHAN_BO
		
		"""  
		return self.execute(query, params)


	def lay_du_lieu_btn_phan_bo_cho_ct_dh_hd(self,ky_tinh_gia_thanh,chi_nhanh_id,arr_list_dtthcp_vthh,loai_phan_bo):
		params = {
			'KY_TINH_GIA_THANH' : ky_tinh_gia_thanh,
			'CHI_NHANH_ID' : chi_nhanh_id,
			'arr_list_dtthcp_vthh' : arr_list_dtthcp_vthh,
			'loai_phan_bo' : loai_phan_bo,
			}
		query = """  
				DO LANGUAGE plpgsql $$
				DECLARE

					ky_tinh_gia_thanh_id           INTEGER := %(KY_TINH_GIA_THANH)s;


					ListItemID                     VARCHAR [] :=ARRAY [%(arr_list_dtthcp_vthh)s];

					chi_nhanh_id                   INTEGER := %(CHI_NHANH_ID)s;

					CHE_DO_KE_TOAN                 VARCHAR;

					tu_ngay                        TIMESTAMP;

					den_ngay                       TIMESTAMP;

					LOAI_PHAN_BO                   INT :=%(loai_phan_bo)s;

					LOAI_GIA_THANH                 VARCHAR;

					MA_PHAN_CAPNVLTT               VARCHAR(100);

					MA_PHAN_CAPNCTT                VARCHAR(100);


					PHAN_THAP_PHAN_SO_TIEN_QUY_DOI INT;


				BEGIN


					SELECT value
					INTO CHE_DO_KE_TOAN
					FROM ir_config_parameter
					WHERE key = 'he_thong.CHE_DO_KE_TOAN'
					FETCH FIRST 1 ROW ONLY
					;


					SELECT value
					INTO PHAN_THAP_PHAN_SO_TIEN_QUY_DOI
					FROM ir_config_parameter
					WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI'
					FETCH FIRST 1 ROW ONLY
					;

					SELECT "TU_NGAY"
					INTO tu_ngay
					FROM gia_thanh_ky_tinh_gia_thanh AS JP
					WHERE "id" = ky_tinh_gia_thanh_id
					;

					SELECT "DEN_NGAY"
					INTO den_ngay
					FROM gia_thanh_ky_tinh_gia_thanh AS JP
					WHERE "id" = ky_tinh_gia_thanh_id
					;


					SELECT "LOAI_GIA_THANH"
					INTO LOAI_GIA_THANH
					FROM gia_thanh_ky_tinh_gia_thanh AS JP
					WHERE "id" = ky_tinh_gia_thanh_id
					;


					DROP TABLE IF EXISTS TMP_DOI_TUONG_THCP
					;

					CREATE TEMP TABLE TMP_DOI_TUONG_THCP
					(
						"MODEL_CHUNG_TU" VARCHAR,
						"ID_CHUNG_TU"    INT
					)
					;

					INSERT INTO TMP_DOI_TUONG_THCP
					(
						"MODEL_CHUNG_TU",
						"ID_CHUNG_TU"
					)

						SELECT
							'danh_muc_cong_trinh'
							, id
						FROM danh_muc_cong_trinh
						WHERE ('danh_muc_cong_trinh,' || id) = ANY (%(arr_list_dtthcp_vthh)s) -- chú ý tham số này
						UNION ALL
						SELECT
							'account_ex_don_dat_hang'
							, id
						FROM account_ex_don_dat_hang
						WHERE ('account_ex_don_dat_hang,' || id) = ANY (%(arr_list_dtthcp_vthh)s)-- chú ý tham số này

						UNION ALL
						SELECT
							'sale_ex_hop_dong_ban'
							, id
						FROM sale_ex_hop_dong_ban
						WHERE ('sale_ex_hop_dong_ban,' || id) = ANY (%(arr_list_dtthcp_vthh)s)-- chú ý tham số này

						UNION ALL
						SELECT
							'danh_muc_doi_tuong_tap_hop_chi_phi'
							, id
						FROM danh_muc_doi_tuong_tap_hop_chi_phi
						WHERE ('danh_muc_doi_tuong_tap_hop_chi_phi,' || id) = ANY (%(arr_list_dtthcp_vthh)s)-- chú ý tham số này
					;


					DROP TABLE IF EXISTS TMP_TableTemp
					;

					CREATE TEMP TABLE TMP_TableTemp
					(
						"SO_TIEN"      FLOAT,
						"ID_VAT_TU"    INT,
						"MODEL_VAT_TU" VARCHAR
					)
					;


					IF (CHE_DO_KE_TOAN = '48')
					THEN
						SELECT "MA_PHAN_CAP"
						INTO MA_PHAN_CAPNVLTT
						FROM danh_muc_khoan_muc_cp
						WHERE "MA_KHOAN_MUC_CP" = 'NVLTT'
						;

						SELECT "MA_PHAN_CAP"
						INTO MA_PHAN_CAPNCTT
						FROM danh_muc_khoan_muc_cp
						WHERE "MA_KHOAN_MUC_CP" = 'NCTT'
						;
					END IF
					;

					IF LOAI_PHAN_BO = 0 -- NVL trực tiếp
					THEN
						-- Lấy tổng tiền của 1 đối tượng/Tổng tiền của tất cả các đối tượng trong kỳ tính giá thành
						INSERT INTO TMP_TableTemp
						(
							"SO_TIEN",
							"ID_VAT_TU",
							"MODEL_VAT_TU"
						)
							SELECT
								SUM(COALESCE(GL."GHI_NO", 0) - COALESCE(GL."GHI_CO", 0))
								, CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
								THEN GL."CONG_TRINH_ID"
								WHEN LOAI_GIA_THANH = 'DON_HANG'
									THEN GL."DON_DAT_HANG_ID"
								WHEN LOAI_GIA_THANH = 'HOP_DONG'
									THEN GL."HOP_DONG_BAN_ID"
								ELSE GL."DOI_TUONG_THCP_ID" END

								, CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
								THEN 'danh.muc.cong.trinh'
								WHEN LOAI_GIA_THANH = 'DON_HANG'
									THEN 'account.ex.don.dat.hang'
								WHEN LOAI_GIA_THANH = 'HOP_DONG'
									THEN 'sale.ex.hop.dong.ban'
								ELSE 'danh.muc.doi.tuong.tap.hop.chi.phi' END
							FROM so_cai_chi_tiet AS GL
							WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
								AND
								(-- Nếu là QD15 thì so sánh các TK có đầu 621 và có đối tượng tập hợp chi phí có trong kỳ tính giá thành
									(
										CHE_DO_KE_TOAN = '15' AND GL."MA_TAI_KHOAN" LIKE '621%%' AND
										(("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR
										GL."LOAI_HACH_TOAN" = '1')
									)
									-- Nếu là QD48 thì so sánh các khoản mục chi phí và đối tượng THCP
									OR (
										CHE_DO_KE_TOAN = '48' AND GL."MA_TAI_KHOAN" LIKE '154%%' AND EXISTS(SELECT E."id"
																											FROM
																												danh_muc_khoan_muc_cp E
																											WHERE E."id" =
																													GL."KHOAN_MUC_CP_ID"
																													AND
																													E."MA_PHAN_CAP" LIKE
																													MA_PHAN_CAPNVLTT ||
																													'%%')
									)

								)
								-- Với tất cả các công trình/đơn hàng/hợp đồng trên kỳ tính giá thành
								AND EXISTS(SELECT
												J."ID_CHUNG_TU"
												, J."MODEL_CHUNG_TU"
											FROM TMP_DOI_TUONG_THCP J
											WHERE (LOAI_GIA_THANH = 'CONG_TRINH' AND GL."CONG_TRINH_ID" = J."ID_CHUNG_TU" AND
													J."MODEL_CHUNG_TU" = 'danh_muc_cong_trinh')
												OR (LOAI_GIA_THANH = 'DON_HANG' AND GL."DON_DAT_HANG_ID" = J."ID_CHUNG_TU" AND
													J."MODEL_CHUNG_TU" = 'account_ex_don_dat_hang')
												OR (LOAI_GIA_THANH = 'HOP_DONG' AND GL."HOP_DONG_BAN_ID" = J."ID_CHUNG_TU" AND
													J."MODEL_CHUNG_TU" = 'sale_ex_hop_dong_ban')
												OR ((LOAI_GIA_THANH = 'DON_GIAN' OR LOAI_GIA_THANH = 'HE_SO_TY_LE' OR
														LOAI_GIA_THANH = 'PHAN_BUOC') AND
													GL."DOI_TUONG_THCP_ID" = J."ID_CHUNG_TU" AND
													J."MODEL_CHUNG_TU" = 'danh_muc_doi_tuong_tap_hop_chi_phi')
								)


								AND "CHI_NHANH_ID" = chi_nhanh_id
							GROUP BY CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
								THEN GL."CONG_TRINH_ID"
									WHEN LOAI_GIA_THANH = 'DON_HANG'
										THEN GL."DON_DAT_HANG_ID"
									WHEN LOAI_GIA_THANH = 'HOP_DONG'
										THEN GL."HOP_DONG_BAN_ID"
									ELSE GL."DOI_TUONG_THCP_ID" END

						;
					ELSE
						IF LOAI_PHAN_BO = 1 -- Nhân công trực tiếp
						THEN
							INSERT INTO TMP_TableTemp
							(
								"SO_TIEN",
								"ID_VAT_TU",
								"MODEL_VAT_TU"
							)
								SELECT

									SUM(COALESCE(GL."GHI_NO", 0) - COALESCE(GL."GHI_CO", 0))
									, CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
									THEN GL."CONG_TRINH_ID"
									WHEN LOAI_GIA_THANH = 'DON_HANG'
										THEN GL."DON_DAT_HANG_ID"
									WHEN LOAI_GIA_THANH = 'HOP_DONG'
										THEN GL."HOP_DONG_BAN_ID"
									ELSE GL."DOI_TUONG_THCP_ID" END
									, CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
									THEN 'danh.muc.cong.trinh'
									WHEN LOAI_GIA_THANH = 'DON_HANG'
										THEN 'account.ex.don.dat.hang'
									WHEN LOAI_GIA_THANH = 'HOP_DONG'
										THEN 'sale.ex.hop.dong.ban'
									ELSE 'danh.muc.doi.tuong.tap.hop.chi.phi' END

								FROM so_cai_chi_tiet AS GL
								WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
									AND
									(-- Nếu là QD15 thì so sánh các TK có đầu 621 và có đối tượng tập hợp chi phí có trong kỳ tính giá thành
										(
											CHE_DO_KE_TOAN = '15' AND GL."MA_TAI_KHOAN" LIKE '622%%' AND
											(("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR
											GL."LOAI_HACH_TOAN" = '1')
										)
										-- Nếu là QD48 thì so sánh các khoản mục chi phí và đối tượng THCP
										OR (
											CHE_DO_KE_TOAN = '48' AND GL."MA_TAI_KHOAN" LIKE '154%%' AND EXISTS(SELECT E."id"
																												FROM
																													danh_muc_khoan_muc_cp E
																												WHERE
																													E."id" =
																													GL."KHOAN_MUC_CP_ID"
																													AND
																													E."MA_PHAN_CAP"
																													LIKE
																													MA_PHAN_CAPNCTT ||
																													'%%')
										)

									)
									AND EXISTS(SELECT
													J."ID_CHUNG_TU"
													, J."MODEL_CHUNG_TU"
												FROM TMP_DOI_TUONG_THCP J
												WHERE
													(LOAI_GIA_THANH = 'CONG_TRINH' AND GL."CONG_TRINH_ID" = J."ID_CHUNG_TU" AND
													J."MODEL_CHUNG_TU" = 'danh_muc_cong_trinh')
													OR (LOAI_GIA_THANH = 'DON_HANG' AND GL."DON_DAT_HANG_ID" = J."ID_CHUNG_TU" AND
														J."MODEL_CHUNG_TU" = 'account_ex_don_dat_hang')
													OR (LOAI_GIA_THANH = 'HOP_DONG' AND GL."HOP_DONG_BAN_ID" = J."ID_CHUNG_TU" AND
														J."MODEL_CHUNG_TU" = 'sale_ex_hop_dong_ban')
													OR ((LOAI_GIA_THANH = 'DON_GIAN' OR LOAI_GIA_THANH = 'HE_SO_TY_LE' OR
														LOAI_GIA_THANH = 'PHAN_BUOC') AND
														GL."DOI_TUONG_THCP_ID" = J."ID_CHUNG_TU" AND
														J."MODEL_CHUNG_TU" = 'danh_muc_doi_tuong_tap_hop_chi_phi')
									)
									AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'

									AND "CHI_NHANH_ID" = chi_nhanh_id
								GROUP BY CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
									THEN GL."CONG_TRINH_ID"
										WHEN LOAI_GIA_THANH = 'DON_HANG'
											THEN GL."DON_DAT_HANG_ID"
										WHEN LOAI_GIA_THANH = 'HOP_DONG'
											THEN GL."HOP_DONG_BAN_ID"
										ELSE GL."DOI_TUONG_THCP_ID" END

							;
						ELSE
							IF LOAI_PHAN_BO = 2 -- Chi phí trực tiếp
							THEN


								INSERT INTO TMP_TableTemp
								(
									"SO_TIEN",
									"ID_VAT_TU",
									"MODEL_VAT_TU"
								)
									SELECT
										SUM(COALESCE(GL."GHI_NO", 0) - COALESCE(GL."GHI_CO", 0))
										, CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
										THEN GL."CONG_TRINH_ID"
										WHEN LOAI_GIA_THANH = 'DON_HANG'
											THEN GL."DON_DAT_HANG_ID"
										WHEN LOAI_GIA_THANH = 'HOP_DONG'
											THEN GL."HOP_DONG_BAN_ID"
										ELSE GL."DOI_TUONG_THCP_ID" END
										, CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
										THEN 'danh.muc.cong.trinh'
										WHEN LOAI_GIA_THANH = 'DON_HANG'
											THEN 'account.ex.don.dat.hang'
										WHEN LOAI_GIA_THANH = 'HOP_DONG'
											THEN 'sale.ex.hop.dong.ban'
										ELSE 'danh.muc.doi.tuong.tap.hop.chi.phi' END

									FROM so_cai_chi_tiet AS GL
									WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
										AND
										(-- Nếu là QD15 thì so sánh các TK có đầu 621 và có đối tượng tập hợp chi phí có trong kỳ tính giá thành
											(
												CHE_DO_KE_TOAN = '15' AND
												(GL."MA_TAI_KHOAN" LIKE '621%%' OR GL."MA_TAI_KHOAN" LIKE '622%%') AND
												(("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%' AND GL."LOAI_HACH_TOAN" = '2') OR
												GL."LOAI_HACH_TOAN" = '1')
											)
											-- Nếu là QD48 thì so sánh các khoản mục chi phí và đối tượng THCP
											OR (
												CHE_DO_KE_TOAN = '48' AND GL."MA_TAI_KHOAN" LIKE '154%%' AND EXISTS(SELECT E."id"
																													FROM
																														danh_muc_khoan_muc_cp E
																													WHERE
																														E."id" =
																														GL."KHOAN_MUC_CP_ID"
																														AND (
																															E."MA_PHAN_CAP"
																															LIKE
																															MA_PHAN_CAPNVLTT
																															|| '%%'
																															OR
																															E."MA_PHAN_CAP"
																															LIKE
																															MA_PHAN_CAPNCTT
																															|| '%%'))
											)

										)
										AND EXISTS(SELECT
														J."ID_CHUNG_TU"
														, J."MODEL_CHUNG_TU"
													FROM TMP_DOI_TUONG_THCP J
													WHERE
														(LOAI_GIA_THANH = 'CONG_TRINH' AND GL."CONG_TRINH_ID" = J."ID_CHUNG_TU" AND
														J."MODEL_CHUNG_TU" = 'danh_muc_cong_trinh')
														OR (LOAI_GIA_THANH = 'DON_HANG' AND GL."DON_DAT_HANG_ID" = J."ID_CHUNG_TU" AND
															J."MODEL_CHUNG_TU" = 'account_ex_don_dat_hang')
														OR (LOAI_GIA_THANH = 'HOP_DONG' AND GL."HOP_DONG_BAN_ID" = J."ID_CHUNG_TU" AND
															J."MODEL_CHUNG_TU" = 'sale_ex_hop_dong_ban')
														OR ((LOAI_GIA_THANH = 'DON_GIAN' OR LOAI_GIA_THANH = 'HE_SO_TY_LE' OR
															LOAI_GIA_THANH = 'PHAN_BUOC') AND
															GL."DOI_TUONG_THCP_ID" = J."ID_CHUNG_TU" AND
															J."MODEL_CHUNG_TU" = 'danh_muc_doi_tuong_tap_hop_chi_phi')
										)
										AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'

										AND "CHI_NHANH_ID" = chi_nhanh_id
									GROUP BY
										CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
											THEN GL."CONG_TRINH_ID"
										WHEN LOAI_GIA_THANH = 'DON_HANG'
											THEN GL."DON_DAT_HANG_ID"
										WHEN LOAI_GIA_THANH = 'HOP_DONG'
											THEN GL."HOP_DONG_BAN_ID"
										ELSE GL."DOI_TUONG_THCP_ID" END

								;

							ELSE

								--BTAnh - 27.07.2016
								--Phân bổ theo định mức: Hiện mới làm cho QĐ15, công trình vụ việc


								IF LOAI_PHAN_BO = 4 -- Đoanh thu
								THEN
									INSERT INTO TMP_TableTemp
									(
										"SO_TIEN",
										"ID_VAT_TU",
										"MODEL_VAT_TU"
									)
										SELECT
											SUM(COALESCE(GL."GHI_CO", 0) - COALESCE(GL."GHI_NO", 0))
											, CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
											THEN GL."CONG_TRINH_ID"
											WHEN LOAI_GIA_THANH = 'DON_HANG'
												THEN GL."DON_DAT_HANG_ID"
											WHEN LOAI_GIA_THANH = 'HOP_DONG'
												THEN GL."HOP_DONG_BAN_ID"
											ELSE GL."DOI_TUONG_THCP_ID" END
											, CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
											THEN 'danh.muc.cong.trinh'
											WHEN LOAI_GIA_THANH = 'DON_HANG'
												THEN 'account.ex.don.dat.hang'
											WHEN LOAI_GIA_THANH = 'HOP_DONG'
												THEN 'sale.ex.hop.dong.ban'
											ELSE 'danh.muc.doi.tuong.tap.hop.chi.phi' END

										FROM so_cai_chi_tiet GL
											INNER JOIN TMP_DOI_TUONG_THCP AS J ON
																				(LOAI_GIA_THANH = 'CONG_TRINH' AND
																					GL."CONG_TRINH_ID" = J."ID_CHUNG_TU" AND
																					J."MODEL_CHUNG_TU" = 'danh_muc_cong_trinh')
																				OR (LOAI_GIA_THANH = 'DON_HANG' AND
																					GL."DON_DAT_HANG_ID" = J."ID_CHUNG_TU" AND
																					J."MODEL_CHUNG_TU" = 'account_ex_don_dat_hang')
																				OR (LOAI_GIA_THANH = 'HOP_DONG' AND
																					GL."HOP_DONG_BAN_ID" = J."ID_CHUNG_TU" AND
																					J."MODEL_CHUNG_TU" = 'sale_ex_hop_dong_ban')
																				OR ((LOAI_GIA_THANH = 'DON_GIAN' OR
																						LOAI_GIA_THANH = 'HE_SO_TY_LE' OR
																						LOAI_GIA_THANH = 'PHAN_BUOC') AND
																					GL."DOI_TUONG_THCP_ID" = J."ID_CHUNG_TU" AND
																					J."MODEL_CHUNG_TU" =
																					'danh_muc_doi_tuong_tap_hop_chi_phi')
										WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay

											AND GL."CHI_NHANH_ID" = chi_nhanh_id
											AND
											((
												(CHE_DO_KE_TOAN = '48')
												/*
													dvha 16/09/2016:116746:DEV_Cập nhật nghiệp vụ chiết khấu_Giá thành
													TT133= PS Có 511, 711, 515(không bao gồm PS ĐƯ Nợ TK 911/Có TK511, 711, 515) - PS Nợ 511, 711, 515 (không bao gồm PS ĐƯ Nợ TK 511, 711, 515/Có TK 911)
												*/

												AND (
													/*PS Có 511, 711, 515(không bao gồm PS ĐƯ Nợ TK 911/Có TK511, 711, 515)*/
													(
														GL."LOAI_HACH_TOAN" = '2' AND (GL."MA_TAI_KHOAN" LIKE '511%%'
																						OR GL."MA_TAI_KHOAN" LIKE '515%%'
																						OR GL."MA_TAI_KHOAN" LIKE '711%%')
														AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '911%%'
													)

													/*PS Nợ 511, 711, 515 (không bao gồm PS ĐƯ Nợ TK 511, 711, 515/Có TK 911)*/
													OR (
														/*kdchien 12/10/2016:16091: lấy thêm TK 515, 711*/
														GL."LOAI_HACH_TOAN" = '1' AND
														(GL."MA_TAI_KHOAN" LIKE '511%%' OR GL."MA_TAI_KHOAN" LIKE '515%%' OR
															GL."MA_TAI_KHOAN" LIKE '711%%')
														AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE '911%%'
													)
												)
											)
											OR
											(CHE_DO_KE_TOAN = '15'
												/*TT200 = (PS Có 511x, 512x, 515x, 711x - Nợ 511x/3332x,3333x,3331x - PS Nợ 531x, 532x, 521x || PS Có 521x) */
												AND (--PS Có 511x, 512x, 515x, 711x
													(GL."LOAI_HACH_TOAN" = '2' AND
													(
														GL."MA_TAI_KHOAN" LIKE '511%%'
														OR GL."MA_TAI_KHOAN" LIKE '515%%'
														OR GL."MA_TAI_KHOAN" LIKE '711%%'
														OR GL."MA_TAI_KHOAN" LIKE '512%%'
													)
													)
													OR (--	- Nợ 511x/3332x,3333x,3331x
														GL."LOAI_HACH_TOAN" = '1' AND GL."MA_TAI_KHOAN" LIKE '511%%' AND
														(GL."MA_TAI_KHOAN_DOI_UNG" LIKE '3331%%'
														OR GL."MA_TAI_KHOAN_DOI_UNG" LIKE '3332%%'
														OR GL."MA_TAI_KHOAN_DOI_UNG" LIKE '3333%%'
														)
													)
													-- - PS Nợ 531x, 532x, 521x
													OR (
														GL."LOAI_HACH_TOAN" = '1' AND (GL."MA_TAI_KHOAN" LIKE '531%%'
																					OR (GL."MA_TAI_KHOAN" LIKE '532%%')
																					OR (GL."MA_TAI_KHOAN" LIKE '521%%')
														)
													)

													-- || PS Có 521x
													OR (GL."LOAI_HACH_TOAN" = '2' AND GL."MA_TAI_KHOAN" LIKE '521%%')
												)

											)

											)
										GROUP BY CASE WHEN LOAI_GIA_THANH = 'CONG_TRINH'
											THEN GL."CONG_TRINH_ID"
												WHEN LOAI_GIA_THANH = 'DON_HANG'
													THEN GL."DON_DAT_HANG_ID"
												WHEN LOAI_GIA_THANH = 'HOP_DONG'
													THEN GL."HOP_DONG_BAN_ID"
												ELSE GL."DOI_TUONG_THCP_ID" END
									;


								END IF
								;
							END IF
							;
						END IF
						;
					END IF
					;


				END $$
				;


				SELECT *
				FROM TMP_TableTemp
				WHERE "SO_TIEN" > 0

				;
 
		"""  
		return self.execute(query, params)


	def lay_du_lieu_btn_phan_bo(self,ky_tinh_gia_thanh,chi_nhanh_id,arr_list_dtthcp_vthh,loai_phan_bo):
		params = {
			'KY_TINH_GIA_THANH' : ky_tinh_gia_thanh,
			'CHI_NHANH_ID' : chi_nhanh_id,
			'arr_list_dtthcp_vthh' : arr_list_dtthcp_vthh,
			'loai_phan_bo' : loai_phan_bo,
			}
		query = """  

				DO LANGUAGE plpgsql $$
				DECLARE
				
					ky_tinh_gia_thanh_id           INTEGER := %(KY_TINH_GIA_THANH)s;
				
					doi_tuong_thcp_id              INTEGER := NULL;
				
				--	ListItemID                     VARCHAR [] := ARRAY [%(arr_list_dtthcp_vthh)s];
				
					ma_vat_tu                      VARCHAR :=N'6277';
				
					chi_nhanh_id                   INTEGER := %(CHI_NHANH_ID)s;
				
					CHE_DO_KE_TOAN                 VARCHAR;
				
					tu_ngay                        TIMESTAMP;
				
					den_ngay                       TIMESTAMP;
				
					LOAI_PHAN_BO                   INT :=%(loai_phan_bo)s;
				
					LOAI_GIA_THANH                 VARCHAR;
				
					MA_PHAN_CAPNVLTT               VARCHAR(100);
				
					MA_PHAN_CAPNCTT                VARCHAR(100);
				
					MA_PHAN_CAPSXC                 VARCHAR(100);
				
				
					PHAN_THAP_PHAN_SO_TIEN_QUY_DOI INT;
				
					Conut                          INT;
				
					MA_PHAN_CAPSXC_NVPX            VARCHAR(100);
				
					MA_PHAN_CAPSXC_VL              VARCHAR(100);
				
					MA_PHAN_CAPSXC_DCSX            VARCHAR(100);
				
					MA_PHAN_CAPSXC_KH              VARCHAR(100);
				
					MA_PHAN_CAPSXC_MN              VARCHAR(100);
				
				
					MA_PHAN_MA_VAT_TU              VARCHAR(100);
				
				
				BEGIN
				
				
					SELECT value
					INTO CHE_DO_KE_TOAN
					FROM ir_config_parameter
					WHERE key = 'he_thong.CHE_DO_KE_TOAN'
					FETCH FIRST 1 ROW ONLY
					;
				
				
					SELECT value
					INTO PHAN_THAP_PHAN_SO_TIEN_QUY_DOI
					FROM ir_config_parameter
					WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI'
					FETCH FIRST 1 ROW ONLY
					;
				
					SELECT "TU_NGAY"
					INTO tu_ngay
					FROM gia_thanh_ky_tinh_gia_thanh AS JP
					WHERE "id" = ky_tinh_gia_thanh_id
					;
				
					SELECT "DEN_NGAY"
					INTO den_ngay
					FROM gia_thanh_ky_tinh_gia_thanh AS JP
					WHERE "id" = ky_tinh_gia_thanh_id
					;
				
				
					SELECT "LOAI_GIA_THANH"
					INTO LOAI_GIA_THANH
					FROM gia_thanh_ky_tinh_gia_thanh AS JP
					WHERE "id" = ky_tinh_gia_thanh_id
					;
				
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPNVLTT
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'NVLTT'
					;
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPNCTT
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'NCTT'
					;
				
				
					DROP TABLE IF EXISTS TMP_DOI_TUONG_THCP
					;
				
					CREATE TEMP TABLE TMP_DOI_TUONG_THCP
					(
						"MODEL_CHUNG_TU" VARCHAR,
						"ID_CHUNG_TU"    INT
					)
					;
				
					INSERT INTO TMP_DOI_TUONG_THCP
					(
						"MODEL_CHUNG_TU",
						"ID_CHUNG_TU"
					)
				
						SELECT
							'danh_muc_cong_trinh'
							, id
						FROM danh_muc_cong_trinh
						WHERE ('danh_muc_cong_trinh,' || id) = ANY (%(arr_list_dtthcp_vthh)s) -- chú ý tham số này
						UNION ALL
						SELECT
							'account_ex_don_dat_hang'
							, id
						FROM account_ex_don_dat_hang
						WHERE ('account_ex_don_dat_hang,' || id) = ANY (%(arr_list_dtthcp_vthh)s)-- chú ý tham số này
				
						UNION ALL
						SELECT
							'sale_ex_hop_dong_ban'
							, id
						FROM sale_ex_hop_dong_ban
						WHERE ('sale_ex_hop_dong_ban,' || id) = ANY (%(arr_list_dtthcp_vthh)s)-- chú ý tham số này
				
						UNION ALL
						SELECT
							'danh_muc_doi_tuong_tap_hop_chi_phi'
							, id
						FROM danh_muc_doi_tuong_tap_hop_chi_phi
						WHERE ('danh_muc_doi_tuong_tap_hop_chi_phi,' || id) = ANY (%(arr_list_dtthcp_vthh)s)-- chú ý tham số này
					;
				
				
					DROP TABLE IF EXISTS TMP_TableTemp
					;

					CREATE TEMP TABLE TMP_TableTemp
					(
						"SO_TIEN"      FLOAT,
						"ID_VAT_TU"    INT,
						"MODEL_VAT_TU" VARCHAR
					)
					;


					IF LOAI_PHAN_BO = 0 -- NVL trực tiếp
					THEN

						IF LOAI_GIA_THANH = 'CONG_TRINH'
						THEN
							INSERT INTO TMP_TableTemp

							("SO_TIEN",
							"ID_VAT_TU",
							"MODEL_VAT_TU"

							)
								SELECT

									SUM(COALESCE(GL."GHI_NO", 0) - COALESCE(GL."GHI_CO", 0))
									, GL."CONG_TRINH_ID"
									, 'danh.muc.cong.trinh' AS "MODEL_VAT_TU"
								FROM so_cai_chi_tiet AS GL
									INNER JOIN TMP_DOI_TUONG_THCP AS J
										ON GL."CONG_TRINH_ID" = J."ID_CHUNG_TU" AND 'danh_muc_cong_trinh' = J."MODEL_CHUNG_TU"
									LEFT JOIN danh_muc_khoan_muc_cp E ON E."id" = Gl."KHOAN_MUC_CP_ID"
								WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
									AND ((CHE_DO_KE_TOAN = '15'
											AND GL."MA_TAI_KHOAN" LIKE '621%%'
											AND (("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
												AND "LOAI_HACH_TOAN" = '2'
												)
												OR "LOAI_HACH_TOAN" = '1'
											)
										)
										OR (CHE_DO_KE_TOAN = '48'
											AND GL."MA_TAI_KHOAN" LIKE '154%%'
											AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAPNVLTT
																		|| '%%'
										)
									)


									AND "CHI_NHANH_ID" = chi_nhanh_id
								GROUP BY GL."CONG_TRINH_ID"
							;


						ELSEIF LOAI_GIA_THANH = 'DON_HANG'
							THEN
								INSERT INTO TMP_TableTemp
								("SO_TIEN",
								"ID_VAT_TU",
								"MODEL_VAT_TU"

								)
									SELECT

										SUM(COALESCE(GL."GHI_NO", 0) - COALESCE(GL."GHI_CO", 0))
										, GL."DON_DAT_HANG_ID"
										, 'account.ex.don.dat.hang' AS "MODEL_VAT_TU"
									FROM so_cai_chi_tiet AS GL
										INNER JOIN TMP_DOI_TUONG_THCP AS J
											ON GL."DON_DAT_HANG_ID" = J."ID_CHUNG_TU" AND 'account_ex_don_dat_hang' = J."MODEL_CHUNG_TU"
										LEFT JOIN danh_muc_khoan_muc_cp E ON E."id" = Gl."KHOAN_MUC_CP_ID"
									WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
										AND ((CHE_DO_KE_TOAN = '15'
												AND GL."MA_TAI_KHOAN" LIKE '621%%'
												AND (("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
													AND "LOAI_HACH_TOAN" = '2'
													)
													OR "LOAI_HACH_TOAN" = '1'
												)
											)
											OR (CHE_DO_KE_TOAN = '48'
												AND GL."MA_TAI_KHOAN" LIKE '154%%'
												AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAPNVLTT
																			|| '%%'
											)
										)


										AND "CHI_NHANH_ID" = chi_nhanh_id
									GROUP BY GL."DON_DAT_HANG_ID"
								;


						ELSEIF LOAI_GIA_THANH = 'HOP_DONG'
							THEN
								INSERT INTO TMP_TableTemp
								("SO_TIEN",
								"ID_VAT_TU",
								"MODEL_VAT_TU"

								)
									SELECT

										SUM(COALESCE(GL."GHI_NO", 0) - COALESCE(GL."GHI_CO", 0))
										, GL."HOP_DONG_BAN_ID"
										, 'sale.ex.hop.dong.ban' AS "MODEL_VAT_TU"
									FROM so_cai_chi_tiet AS GL
										INNER JOIN TMP_DOI_TUONG_THCP AS J ON GL."HOP_DONG_BAN_ID" = J."ID_CHUNG_TU" AND
																			'sale_ex_hop_dong_ban' = J."MODEL_CHUNG_TU"
										LEFT JOIN danh_muc_khoan_muc_cp E ON E."id" = Gl."KHOAN_MUC_CP_ID"
									WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
										AND ((CHE_DO_KE_TOAN = '15'
												AND GL."MA_TAI_KHOAN" LIKE '621%%'
												AND (("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
													AND "LOAI_HACH_TOAN" = '2'
													)
													OR "LOAI_HACH_TOAN" = '1'
												)
											)
											OR (CHE_DO_KE_TOAN = '48'
												AND GL."MA_TAI_KHOAN" LIKE '154%%'
												AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAPNVLTT
																			|| '%%'
											)
										)


										AND "CHI_NHANH_ID" = chi_nhanh_id
									GROUP BY GL."HOP_DONG_BAN_ID"
								;


						ELSEIF LOAI_GIA_THANH = 'DON_GIAN'
							OR LOAI_GIA_THANH = 'HE_SO_TY_LE'
							OR LOAI_GIA_THANH = 'PHAN_BUOC'
							THEN
								INSERT INTO TMP_TableTemp
								("SO_TIEN",
								"ID_VAT_TU",
								"MODEL_VAT_TU"

								)
									SELECT

										SUM(COALESCE(GL."GHI_NO", 0) - COALESCE(GL."GHI_CO", 0))
										, GL."DOI_TUONG_THCP_ID"
										, 'danh.muc.doi.tuong.tap.hop.chi.phi' AS "MODEL_VAT_TU"
									FROM so_cai_chi_tiet AS GL
										INNER JOIN TMP_DOI_TUONG_THCP AS J ON GL."DOI_TUONG_THCP_ID" = J."ID_CHUNG_TU" AND
																			'danh_muc_doi_tuong_tap_hop_chi_phi' =
																			J."MODEL_CHUNG_TU"
										LEFT JOIN danh_muc_khoan_muc_cp E ON E."id" = Gl."KHOAN_MUC_CP_ID"
									WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
										AND ((CHE_DO_KE_TOAN = '15'
												AND GL."MA_TAI_KHOAN" LIKE '621%%'
												AND (("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
													AND "LOAI_HACH_TOAN" = '2'
													)
													OR "LOAI_HACH_TOAN" = '1'
												)
											)
											OR (CHE_DO_KE_TOAN = '48'
												AND GL."MA_TAI_KHOAN" LIKE '154%%'
												AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAPNVLTT
																			|| '%%'
											)
										)


										AND "CHI_NHANH_ID" = chi_nhanh_id
									GROUP BY GL."DOI_TUONG_THCP_ID"
								;
						END IF
						;

					ELSEIF LOAI_PHAN_BO = 1 -- Nhân công trực tiếp
						THEN
							IF LOAI_GIA_THANH = 'CONG_TRINH'
							THEN
								INSERT INTO TMP_TableTemp
								("SO_TIEN",
								"ID_VAT_TU",
								"MODEL_VAT_TU"

								)
									SELECT

										SUM(COALESCE(GL."GHI_NO", 0) - COALESCE(GL."GHI_CO", 0))
										, GL."CONG_TRINH_ID"
										, 'danh.muc.cong.trinh' AS "MODEL_VAT_TU"
									FROM so_cai_chi_tiet AS GL
										INNER JOIN TMP_DOI_TUONG_THCP AS J ON GL."CONG_TRINH_ID" = J."ID_CHUNG_TU" AND
																			'danh_muc_cong_trinh' = J."MODEL_CHUNG_TU"
										LEFT JOIN danh_muc_khoan_muc_cp E ON E."id" = Gl."KHOAN_MUC_CP_ID"
									WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
										AND ((CHE_DO_KE_TOAN = '15'
												AND GL."MA_TAI_KHOAN" LIKE '622%%'
												AND (("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
													AND "LOAI_HACH_TOAN" = '2'
													)
													OR "LOAI_HACH_TOAN" = '1'
												)
											)
											OR (CHE_DO_KE_TOAN = '48'
												AND GL."MA_TAI_KHOAN" LIKE '154%%'
												AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAPNCTT
																			|| '%%'
											)
										)


										AND "CHI_NHANH_ID" = chi_nhanh_id
									GROUP BY GL."CONG_TRINH_ID"
								;


							ELSEIF LOAI_GIA_THANH = 'DON_HANG'
								THEN
									INSERT INTO TMP_TableTemp
									("SO_TIEN",
									"ID_VAT_TU",
									"MODEL_VAT_TU"

									)
										SELECT
											SUM(COALESCE(GL."GHI_NO", 0) - COALESCE(GL."GHI_CO", 0))
											, GL."DON_DAT_HANG_ID"
											, 'account.ex.don.dat.hang' AS "MODEL_VAT_TU"
										FROM so_cai_chi_tiet AS GL
											INNER JOIN TMP_DOI_TUONG_THCP AS J
												ON GL."DON_DAT_HANG_ID" = J."ID_CHUNG_TU" AND
												'account_ex_don_dat_hang' = J."MODEL_CHUNG_TU"
											LEFT JOIN danh_muc_khoan_muc_cp E ON E."id" = Gl."KHOAN_MUC_CP_ID"
										WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
											AND ((CHE_DO_KE_TOAN = '15'
													AND GL."MA_TAI_KHOAN" LIKE '622%%'
													AND (("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
														AND "LOAI_HACH_TOAN" = '2'
														)
														OR "LOAI_HACH_TOAN" = '1'
													)
												)
												OR (CHE_DO_KE_TOAN = '48'
													AND GL."MA_TAI_KHOAN" LIKE '154%%'
													AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAPNCTT
																				|| '%%'
												)
											)


											AND "CHI_NHANH_ID" = chi_nhanh_id
										GROUP BY GL."DON_DAT_HANG_ID"
									;


							ELSEIF LOAI_GIA_THANH = 'HOP_DONG'
								THEN
									INSERT INTO TMP_TableTemp
									("SO_TIEN",
									"ID_VAT_TU",
									"MODEL_VAT_TU"

									)
										SELECT

											SUM(COALESCE(GL."GHI_NO", 0) - COALESCE(GL."GHI_CO", 0))
											, GL."HOP_DONG_BAN_ID"
											, 'sale.ex.hop.dong.ban' AS "MODEL_VAT_TU"
										FROM so_cai_chi_tiet AS GL
											INNER JOIN TMP_DOI_TUONG_THCP AS J
												ON GL."HOP_DONG_BAN_ID" = J."ID_CHUNG_TU" AND
												'sale_ex_hop_dong_ban' = J."MODEL_CHUNG_TU"
											LEFT JOIN danh_muc_khoan_muc_cp E ON E."id" = Gl."KHOAN_MUC_CP_ID"
										WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
											AND ((CHE_DO_KE_TOAN = '15'
													AND GL."MA_TAI_KHOAN" LIKE '622%%'
													AND (("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
														AND "LOAI_HACH_TOAN" = '2'
														)
														OR "LOAI_HACH_TOAN" = '1'
													)
												)
												OR (CHE_DO_KE_TOAN = '48'
													AND GL."MA_TAI_KHOAN" LIKE '154%%'
													AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAPNCTT
																				|| '%%'
												)
											)


											AND "CHI_NHANH_ID" = chi_nhanh_id
										GROUP BY GL."HOP_DONG_BAN_ID"
									;


							ELSEIF LOAI_GIA_THANH = 'DON_GIAN'
								OR LOAI_GIA_THANH = 'HE_SO_TY_LE'
								OR LOAI_GIA_THANH = 'PHAN_BUOC'
								THEN
									INSERT INTO TMP_TableTemp
									("SO_TIEN",
									"ID_VAT_TU",
									"MODEL_VAT_TU"

									)
										SELECT

											SUM(COALESCE(GL."GHI_NO", 0) - COALESCE(GL."GHI_CO", 0))
											, GL."DOI_TUONG_THCP_ID"
											, 'danh.muc.doi.tuong.tap.hop.chi.phi' AS "MODEL_VAT_TU"
										FROM so_cai_chi_tiet AS GL
											INNER JOIN TMP_DOI_TUONG_THCP AS J
												ON GL."DOI_TUONG_THCP_ID" = J."ID_CHUNG_TU" AND
												'danh_muc_doi_tuong_tap_hop_chi_phi' = J."MODEL_CHUNG_TU"
											LEFT JOIN danh_muc_khoan_muc_cp E
												ON E."id" = Gl."KHOAN_MUC_CP_ID"
										WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
											AND ((CHE_DO_KE_TOAN = '15'
													AND GL."MA_TAI_KHOAN" LIKE '622%%'
													AND (("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
														AND "LOAI_HACH_TOAN" = '2'
														)
														OR "LOAI_HACH_TOAN" = '1'
													)
												)
												OR (CHE_DO_KE_TOAN = '48'
													AND GL."MA_TAI_KHOAN" LIKE '154%%'
													AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAPNCTT
																				|| '%%'
												)
											)


											AND "CHI_NHANH_ID" = chi_nhanh_id
										GROUP BY GL."DOI_TUONG_THCP_ID"
									;
							END IF
							;

					ELSEIF LOAI_PHAN_BO = 2 -- Chi phí trực tiếp
						THEN

							IF LOAI_GIA_THANH = 'CONG_TRINH'
							THEN
								INSERT INTO TMP_TableTemp
								("SO_TIEN",
								"ID_VAT_TU",
								"MODEL_VAT_TU"

								)
									SELECT

										SUM(COALESCE(GL."GHI_NO", 0) - COALESCE(GL."GHI_CO", 0))
										, GL."CONG_TRINH_ID"
										, 'danh.muc.cong.trinh' AS "MODEL_VAT_TU"
									FROM so_cai_chi_tiet AS GL
										INNER JOIN TMP_DOI_TUONG_THCP AS J
											ON GL."CONG_TRINH_ID" = J."ID_CHUNG_TU" AND
											'danh_muc_cong_trinh' = J."MODEL_CHUNG_TU"
										LEFT JOIN danh_muc_khoan_muc_cp E
											ON E."id" = Gl."KHOAN_MUC_CP_ID"
									WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
										AND ((CHE_DO_KE_TOAN = '15'
												AND (GL."MA_TAI_KHOAN" LIKE '621%%'
													OR GL."MA_TAI_KHOAN" LIKE '622%%'
												)
												AND (("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
													AND "LOAI_HACH_TOAN" = '2'
													)
													OR "LOAI_HACH_TOAN" = '1'
												)
											)
											OR (CHE_DO_KE_TOAN = '48'
												AND GL."MA_TAI_KHOAN" LIKE '154%%'
												AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAPNCTT
																			|| '%%'
														OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAPNVLTT
																				|| '%%'
												)
											)
										)


										AND "CHI_NHANH_ID" = chi_nhanh_id
									GROUP BY GL."CONG_TRINH_ID"
								;


							ELSEIF LOAI_GIA_THANH = 'DON_HANG'
								THEN
									INSERT INTO TMP_TableTemp
									("SO_TIEN",
									"ID_VAT_TU",
									"MODEL_VAT_TU"

									)
										SELECT

											SUM(COALESCE(GL."GHI_NO", 0) - COALESCE(GL."GHI_CO", 0))
											, GL."DON_DAT_HANG_ID"
											, 'account.ex.don.dat.hang' AS "MODEL_VAT_TU"
										FROM so_cai_chi_tiet AS GL
											INNER JOIN TMP_DOI_TUONG_THCP AS J
												ON GL."DON_DAT_HANG_ID" = J."ID_CHUNG_TU" AND
												'account_ex_don_dat_hang' = J."MODEL_CHUNG_TU"
											LEFT JOIN danh_muc_khoan_muc_cp E
												ON E."id" = Gl."KHOAN_MUC_CP_ID"
										WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
											AND ((CHE_DO_KE_TOAN = '15'
													AND (GL."MA_TAI_KHOAN" LIKE '621%%'
														OR GL."MA_TAI_KHOAN" LIKE '622%%'
													)
													AND (("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
														AND "LOAI_HACH_TOAN" = '2'
														)
														OR "LOAI_HACH_TOAN" = '1'
													)
												)
												OR (CHE_DO_KE_TOAN = '48'
													AND GL."MA_TAI_KHOAN" LIKE '154%%'
													AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAPNCTT
																				|| '%%'
															OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAPNVLTT
																					|| '%%'
													)
												)
											)


											AND "CHI_NHANH_ID" = chi_nhanh_id
										GROUP BY GL."DON_DAT_HANG_ID"
									;

							ELSEIF LOAI_GIA_THANH = 'HOP_DONG'
								THEN
									INSERT INTO TMP_TableTemp
									("SO_TIEN",
									"ID_VAT_TU",
									"MODEL_VAT_TU"

									)
										SELECT

											SUM(COALESCE(GL."GHI_NO", 0) -
												COALESCE(GL."GHI_CO", 0))
											, GL."HOP_DONG_BAN_ID"
											, 'sale.ex.hop.dong.ban' AS "MODEL_VAT_TU"
										FROM so_cai_chi_tiet AS GL
											INNER JOIN TMP_DOI_TUONG_THCP AS J
												ON GL."HOP_DONG_BAN_ID" = J."ID_CHUNG_TU" AND
												'sale_ex_hop_dong_ban' = J."MODEL_CHUNG_TU"
											LEFT JOIN danh_muc_khoan_muc_cp E
												ON E."id" = Gl."KHOAN_MUC_CP_ID"
										WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
											AND ((CHE_DO_KE_TOAN = '15'
													AND (GL."MA_TAI_KHOAN" LIKE '621%%'
														OR GL."MA_TAI_KHOAN" LIKE '622%%'
													)
													AND
													(("MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
													AND "LOAI_HACH_TOAN" = '2'
													)
													OR "LOAI_HACH_TOAN" = '1'
													)
												)
												OR (CHE_DO_KE_TOAN = '48'
													AND GL."MA_TAI_KHOAN" LIKE '154%%'
													AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAPNCTT
																				|| '%%'
															OR E."MA_PHAN_CAP" LIKE
															MA_PHAN_CAPNVLTT
															|| '%%'
													)
												)
											)


											AND "CHI_NHANH_ID" = chi_nhanh_id
										GROUP BY GL."HOP_DONG_BAN_ID"

									;

							ELSEIF LOAI_GIA_THANH = 'DON_GIAN'
								OR LOAI_GIA_THANH = 'HE_SO_TY_LE'
								OR LOAI_GIA_THANH = 'PHAN_BUOC'
								THEN
									INSERT INTO TMP_TableTemp
									("SO_TIEN",
									"ID_VAT_TU",
									"MODEL_VAT_TU"

									)
										SELECT

											SUM(COALESCE(GL."GHI_NO", 0) -
												COALESCE(GL."GHI_CO", 0))
											, GL."DOI_TUONG_THCP_ID"
											, 'danh.muc.doi.tuong.tap.hop.chi.phi' AS "MODEL_VAT_TU"
										FROM so_cai_chi_tiet AS GL
											INNER JOIN TMP_DOI_TUONG_THCP AS J
												ON GL."DOI_TUONG_THCP_ID" = J."ID_CHUNG_TU"
												AND
												'danh_muc_doi_tuong_tap_hop_chi_phi' =
												J."MODEL_CHUNG_TU"
											LEFT JOIN danh_muc_khoan_muc_cp E
												ON E."id" = Gl."KHOAN_MUC_CP_ID"
										WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
											AND ((CHE_DO_KE_TOAN = '15'
													AND (GL."MA_TAI_KHOAN" LIKE '621%%'
														OR GL."MA_TAI_KHOAN" LIKE '622%%'
													)
													AND (("MA_TAI_KHOAN_DOI_UNG" NOT LIKE
														'154%%'
														AND "LOAI_HACH_TOAN" = '2'
														)
														OR "LOAI_HACH_TOAN" = '1'
													)
												)
												OR (CHE_DO_KE_TOAN = '48'
													AND GL."MA_TAI_KHOAN" LIKE '154%%'
													AND
													(E."MA_PHAN_CAP" LIKE MA_PHAN_CAPNCTT
																			|| '%%'
														OR E."MA_PHAN_CAP" LIKE
														MA_PHAN_CAPNVLTT
														|| '%%'
													)
												)
											)


											AND "CHI_NHANH_ID" = chi_nhanh_id
										GROUP BY GL."DOI_TUONG_THCP_ID"
									;

							END IF
							;
					ELSEIF LOAI_PHAN_BO = 3 -- Định mức
						THEN
							IF CHE_DO_KE_TOAN =
							'15' -- Nếu là quyết định 15 thì tính theo task 78122
							THEN


								--                 SELECT COUNT("KY_TINH_GIA_THANH_ID")
								--                 FROM
								--                     GIA_THANH_DINH_MUC_PHAN_BO_CP_THEO_THCP_VA_TK
								--                 WHERE
								--                     "KY_TINH_GIA_THANH_ID" =
								--                     ky_tinh_gia_thanh_id
								--                 ;

								INSERT INTO TMP_TableTemp
								("SO_TIEN",
								"ID_VAT_TU",
								"MODEL_VAT_TU"

								)
									SELECT
										SUM(JAQ."SO_TIEN")
										, JAQ."DOI_TUONG_THCP_ID"
										, 'danh.muc.doi.tuong.tap.hop.chi.phi' AS "MODEL_VAT_TU"
									FROM
										GIA_THANH_DINH_MUC_PHAN_BO_CP_THEO_THCP_VA_TK AS JAQ
										INNER JOIN TMP_DOI_TUONG_THCP AS J
											ON JAQ."DOI_TUONG_THCP_ID" =
											J."ID_CHUNG_TU" AND
											'danh_muc_doi_tuong_tap_hop_chi_phi'
											= J."MODEL_CHUNG_TU"
									WHERE
										(SELECT "SO_TAI_KHOAN"
										FROM danh_muc_he_thong_tai_khoan TK
										WHERE TK.id = JAQ."TAI_KHOAN_ID") =
										ma_vat_tu
										AND
										JAQ."KY_TINH_GIA_THANH_ID" =
										CASE WHEN Conut > 0
											THEN ky_tinh_gia_thanh_id
										ELSE 0 END
									GROUP BY
										JAQ."DOI_TUONG_THCP_ID",
										JAQ."TAI_KHOAN_ID"
								;

							ELSE


								SELECT "MA_PHAN_CAP"
								INTO MA_PHAN_CAPSXC_NVPX
								FROM danh_muc_khoan_muc_cp
								WHERE "MA_KHOAN_MUC_CP" = 'SXC.NVPX'
								;

								SELECT "MA_PHAN_CAP"
								INTO MA_PHAN_CAPSXC_VL
								FROM danh_muc_khoan_muc_cp
								WHERE "MA_KHOAN_MUC_CP" = 'SXC.VL'
								;

								SELECT "MA_PHAN_CAP"
								INTO MA_PHAN_CAPSXC_DCSX
								FROM danh_muc_khoan_muc_cp
								WHERE "MA_KHOAN_MUC_CP" = 'SXC.DCSX'
								;

								SELECT "MA_PHAN_CAP"
								INTO MA_PHAN_CAPSXC_KH
								FROM danh_muc_khoan_muc_cp
								WHERE "MA_KHOAN_MUC_CP" = 'SXC.KH'
								;

								SELECT "MA_PHAN_CAP"
								INTO MA_PHAN_CAPSXC_MN
								FROM danh_muc_khoan_muc_cp
								WHERE "MA_KHOAN_MUC_CP" = 'SXC.MN'
								;

								SELECT "MA_PHAN_CAP"
								INTO MA_PHAN_CAPSXC
								FROM danh_muc_khoan_muc_cp
								WHERE "MA_KHOAN_MUC_CP" = 'SXC'
								;


								SELECT "MA_PHAN_CAP"
								INTO MA_PHAN_MA_VAT_TU
								FROM danh_muc_khoan_muc_cp AS EI
								WHERE "MA_KHOAN_MUC_CP" = ma_vat_tu
								;


								INSERT INTO TMP_TableTemp
								("SO_TIEN",
								"ID_VAT_TU",
								"MODEL_VAT_TU"

								)
									SELECT

										CASE WHEN ma_vat_tu LIKE '621%%'
												OR MA_PHAN_MA_VAT_TU LIKE
													MA_PHAN_CAPNVLTT
													|| '%%'
											THEN

												SUM(COALESCE("NVL_TRUC_TIEP",
															0))
										WHEN ma_vat_tu LIKE '622%%'
											OR MA_PHAN_MA_VAT_TU LIKE
												MA_PHAN_CAPNCTT
												|| '%%'
											THEN

												SUM(COALESCE(
														"NHAN_CONG_TRUC_TIEP",
														0))
										WHEN ma_vat_tu LIKE '6271%%'
											OR MA_PHAN_MA_VAT_TU LIKE
												MA_PHAN_CAPSXC_NVPX
												|| '%%'
											THEN

												SUM(COALESCE(
														"NHAN_CONG_GIAN_TIEP",
														0))
										WHEN ma_vat_tu LIKE '6272%%'
											OR ma_vat_tu LIKE '6273%%'
											OR MA_PHAN_MA_VAT_TU LIKE
												MA_PHAN_CAPSXC_VL
												|| '%%'
											OR MA_PHAN_MA_VAT_TU LIKE
												MA_PHAN_CAPSXC_DCSX
												|| '%%'
											THEN

												SUM(COALESCE("NVL_GIAN_TIEP",
															0))
										WHEN ma_vat_tu LIKE '6274%%'
											OR MA_PHAN_MA_VAT_TU LIKE
												MA_PHAN_CAPSXC_KH
												|| '%%'
											THEN

												SUM(COALESCE("KHAU_HAO", 0))
										WHEN ma_vat_tu LIKE '6277%%'
											OR MA_PHAN_MA_VAT_TU LIKE
												MA_PHAN_CAPSXC_MN
												|| '%%'
											THEN

												SUM(COALESCE(
														"CHI_PHI_MUA_NGOAI", 0))
										WHEN ma_vat_tu LIKE '627%%'
											OR
											MA_PHAN_MA_VAT_TU LIKE
											MA_PHAN_CAPSXC
											|| '%%'
											THEN

												SUM(COALESCE("CHI_PHI_KHAC",
															0))
										ELSE 0
										END
										, JAQ."DOI_TUONG_THCP_ID"
										, 'danh.muc.doi.tuong.tap.hop.chi.phi' AS "MODEL_VAT_TU"
									FROM
										gia_thanh_khai_bao_dinh_muc_gttp_chi_tiet AS JAQ
										INNER JOIN TMP_DOI_TUONG_THCP AS J
											ON JAQ."DOI_TUONG_THCP_ID" =
											J."ID_CHUNG_TU" AND
											'danh_muc_doi_tuong_tap_hop_chi_phi'
											= J."MODEL_CHUNG_TU"
									GROUP BY
										JAQ."DOI_TUONG_THCP_ID"
								;


							END IF
							;

					END IF
					;


					IF LOAI_PHAN_BO = 4 -- Đoanh thu
					THEN
						INSERT INTO TMP_TableTemp
						("SO_TIEN",
						"ID_VAT_TU",
						"MODEL_VAT_TU"

						)
							SELECT

								SUM(COALESCE(GL."GHI_CO", 0) -
									COALESCE(GL."GHI_NO", 0))
								, GL."DOI_TUONG_THCP_ID"
								, 'danh.muc.doi.tuong.tap.hop.chi.phi' AS "MODEL_VAT_TU"
							FROM so_cai_chi_tiet GL
								INNER JOIN TMP_DOI_TUONG_THCP AS J
									ON GL."DOI_TUONG_THCP_ID" =
									J."ID_CHUNG_TU" AND
									'danh_muc_doi_tuong_tap_hop_chi_phi'
									= J."MODEL_CHUNG_TU"
							WHERE
								"NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
								AND ((CHE_DO_KE_TOAN = '15'
									AND (GL."MA_TAI_KHOAN" LIKE
										'511%%'
										OR GL."MA_TAI_KHOAN" LIKE
											'512%%'
										OR GL."MA_TAI_KHOAN" LIKE
											'515%%'
										OR GL."MA_TAI_KHOAN" LIKE
											'711%%'
										OR (GL."MA_TAI_KHOAN"
											LIKE '511%%'
											AND (
												GL."MA_TAI_KHOAN_DOI_UNG"
												LIKE '3331%%'
												OR
												GL."MA_TAI_KHOAN_DOI_UNG"
												LIKE '3332%%'
												OR
												GL."MA_TAI_KHOAN_DOI_UNG"
												LIKE '3333%%'
											)
										)
										OR
										(GL."MA_TAI_KHOAN" LIKE
											'531%%')
										OR
										(GL."MA_TAI_KHOAN" LIKE
											'532%%')
										OR
										(GL."MA_TAI_KHOAN" LIKE
											'521%%')
									)
									)
									OR (CHE_DO_KE_TOAN = '48'
										AND (GL."MA_TAI_KHOAN" LIKE
											'511%%'
											OR
											GL."MA_TAI_KHOAN" LIKE
											'512%%'
											OR
											GL."MA_TAI_KHOAN" LIKE
											'515%%'
											OR
											GL."MA_TAI_KHOAN" LIKE
											'711%%'
											OR (GL."MA_TAI_KHOAN"
												LIKE '511%%'
												AND (
													GL."MA_TAI_KHOAN_DOI_UNG"
													LIKE '3331%%'
													OR
													GL."MA_TAI_KHOAN_DOI_UNG"
													LIKE '3332%%'
													OR
													GL."MA_TAI_KHOAN_DOI_UNG"
													LIKE '3333%%'
												)
											)
											OR (GL."MA_TAI_KHOAN"
												LIKE '521%%')
										)
									)
								)
							GROUP BY GL."DOI_TUONG_THCP_ID"
						;


					END IF
					;

				END $$
				;


				SELECT *
				FROM TMP_TableTemp
				WHERE "SO_TIEN" > 0

				;
		
		"""  
		return self.execute(query, params)


	def lay_du_lieu_xac_dinh_do_dang_da_luu(self,ky_tinh_gia_thanh):
		params = {
			'KY_TINH_GIA_THANH_ID' : ky_tinh_gia_thanh,
			}
		query = """   
				DO LANGUAGE plpgsql $$
				DECLARE

					ky_tinh_gia_thanh_id INTEGER := %(KY_TINH_GIA_THANH_ID)s;


				BEGIN
					DROP TABLE IF EXISTS TMP_KET_QUA_PHAN_BO;
					CREATE TEMP TABLE TMP_KET_QUA_PHAN_BO
						AS

						SELECT
							JCD.id AS "XAC_DINH_DO_DANG_CHI_TIET_ID",
								JCD."GIA_THANH_KQ_CHI_PHI_DO_DANG_CHI_TIET_ID" ,
								JCD."MA_THANH_PHAM_ID" ,
								JCD."SL_DO_DANG_CUOI_KY" ,
								JCD."PHAN_TRAM_HOAN_THANH" ,
								JCD."DON_GIA_DINH_MUC",
								JPQ."TONG_CONG" AS "GIA_THANH_DON_VI" ,
								JCD."sequence" as "STT",
								JU."KY_TINH_GIA_THANH_CHI_TIET_ID",
								II."MA" AS "MA_HANG",
								II."TEN" AS "TEN_HANG",
								J."id" AS "DOI_TUONG_THCP_ID",
								J."MA_DOI_TUONG_THCP",
								J."TEN_DOI_TUONG_THCP"

						FROM    GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET AS JCD
								LEFT JOIN gia_thanh_ket_qua_chi_phi_do_dang_cuoi_ky_chi_tiet AS JUD ON JCD."GIA_THANH_KQ_CHI_PHI_DO_DANG_CHI_TIET_ID" = JUD."id"
								LEFT JOIN gia_thanh_tinh_gia_thanh AS JU ON JU."id" = JUD."CHI_TIET_ID"
								LEFT JOIN danh_muc_vat_tu_hang_hoa AS II ON JCD."MA_THANH_PHAM_ID" = II."id"
								LEFT JOIN gia_thanh_khai_bao_dinh_muc_gttp_chi_tiet AS JPQ ON JCD."MA_THANH_PHAM_ID" = JPQ."MA_THANH_PHAM_ID"
								LEFT JOIN danh_muc_doi_tuong_tap_hop_chi_phi AS J ON J."id" = JUD."MA_DOI_TUONG_THCP_ID"
						WHERE   JUD."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
						ORDER BY
							"MA_DOI_TUONG_THCP",
							"MA" ;
					END $$
				;

				SELECT *
				FROM TMP_KET_QUA_PHAN_BO

				;

		"""  
		return self.execute(query, params)

	

	def lay_du_lieu_xac_dinh_do_dang(self,ky_tinh_gia_thanh):
		params = {
			'KY_TINH_GIA_THANH_ID' : ky_tinh_gia_thanh,
			}
		query = """   

				DO LANGUAGE plpgsql $$
				DECLARE
				
					ky_tinh_gia_thanh_id INTEGER := %(KY_TINH_GIA_THANH_ID)s;
				
				
				BEGIN
				
					DROP TABLE IF EXISTS TMP_XAC_DINH_DO_DANG
					;
				
					CREATE TEMP TABLE TMP_XAC_DINH_DO_DANG
						AS
				
							SELECT
								JPD."id" AS "KY_TINH_GIA_THANH_CHI_TIET_ID"
								, JPD."MA_DOI_TUONG_THCP_ID"
								, JPD."KY_TINH_GIA_THANH_ID"
								, 0                                         AS "NVL_TRUC_TIEP"
								, 0                                         AS "NVL_GIAN_TIEP"
								, 0                                         AS "PHAT_SINH_TRONG_KY_NHAN_CONG_TRUC_TIEP"
								, 0                                         AS "NHAN_CONG_GIAN_TIEP"
								, 0                                         AS "KHAU_HAO"
								, 0                                         AS "GIA_TRI_MUA"
								, 0                                         AS "CHI_PHI_CHUNG"
								, 0                                         AS "SO_LUONG"
								, 0                                         AS "HOAN_THANH"
								, COALESCE(JPQ."TONG_CONG", 0) AS "GIA_THANH_DON_VI"
								, II."id" AS "MA_HANG_ID"
								, ii."MA" AS "MA_HANG"
								, ii."TEN" AS "TEN_HANG"
								, J.id AS "DOI_TUONG_THCP_ID"
								, j."MA_DOI_TUONG_THCP"
								, j."TEN_DOI_TUONG_THCP"
								, U."DON_VI_TINH"
							FROM gia_thanh_ky_tinh_gia_thanh_chi_tiet AS JPD INNER JOIN danh_muc_doi_tuong_tap_hop_chi_phi AS J
									ON JPD."MA_DOI_TUONG_THCP_ID" = J."id"
								LEFT JOIN danh_muc_chi_tiet_doi_tuong_tinh_gia_thanh AS JP
									ON J."id" = JP."DOI_TUONG_TONG_HOP_CHI_PHI_ID"
								LEFT JOIN danh_muc_vat_tu_hang_hoa AS II ON II."id" = (CASE WHEN J."CHON_THANH_PHAM" IS NULL
									THEN JP."MA_HANG_ID"
																					ELSE J."CHON_THANH_PHAM" END)
								LEFT JOIN danh_muc_don_vi_tinh AS U ON ii."DVT_CHINH_ID" = U."id"
								LEFT JOIN gia_thanh_khai_bao_dinh_muc_gttp_chi_tiet AS JPQ ON II."id" = JPQ."MA_THANH_PHAM_ID"
							WHERE JPD."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id
					AND II."id" IS NOT NULL
					ORDER BY
								"MA" ;
				
				
				END $$
				;
				
				
				SELECT *
				FROM TMP_XAC_DINH_DO_DANG
				ORDER BY
								"MA_HANG" ;		
		"""  
		return self.execute(query, params)


	def btn_tinh_chi_phi_do_dang_so_Luong_cuoi_ky(self,ky_tinh_gia_thanh_id,chi_nhanh_id,list_vthh_dtthcp_ts):
		params = {
			'KY_TINH_GIA_THANH_ID' : ky_tinh_gia_thanh_id,
			'CHI_NHANH_ID' : chi_nhanh_id,
			'list_vthh_dtthcp_ts' : list_vthh_dtthcp_ts,
			}
		query = """   
				DO LANGUAGE plpgsql $$
				DECLARE
				
					ky_tinh_gia_thanh_id INTEGER := %(KY_TINH_GIA_THANH_ID)s;
				
					chi_nhanh_id         INTEGER := %(CHI_NHANH_ID)s;
				
					tu_ngay              TIMESTAMP;
				
					den_ngay             TIMESTAMP;
				
					vthh_id_va_dtthcp    VARCHAR := N%(list_vthh_dtthcp_ts)s;
				
				BEGIN
				
					SELECT "TU_NGAY"
					INTO tu_ngay
					FROM gia_thanh_ky_tinh_gia_thanh AS JP
					WHERE "id" = ky_tinh_gia_thanh_id
					;
				
					SELECT "DEN_NGAY"
					INTO den_ngay
					FROM gia_thanh_ky_tinh_gia_thanh AS JP
					WHERE "id" = ky_tinh_gia_thanh_id
					;
				
				
					DROP TABLE IF EXISTS TMP_DOI_TUONG_TINH_GIA_THANH
					;
				
					CREATE TEMP TABLE TMP_DOI_TUONG_TINH_GIA_THANH
						AS
				
							SELECT
								COALESCE(SUM(COALESCE("SO_LUONG_NHAP_THEO_DVT_CHINH", 0)), 0) AS "SO_LUONG"
								, "MA_HANG_ID"
								, "MA_DOI_TUONG_THCP_ID"
							FROM so_kho_chi_tiet AS IL
								INNER JOIN CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(vthh_id_va_dtthcp, ',', ';') AS FCGGSIT
									ON FCGGSIT.Value1 = IL."MA_HANG_ID" AND Value2 = "MA_DOI_TUONG_THCP_ID"
							WHERE
								"MA_TK_CO" LIKE '154%%' AND ("MA_TK_NO" LIKE '15%%' AND "MA_TK_NO" NOT LIKE '154%%')
								AND
								"LOAI_CHUNG_TU" IN ('2010', '2011', '2012', '2013')
								AND "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
				
								AND "CHI_NHANH_ID" = chi_nhanh_id
							GROUP BY
								"MA_HANG_ID",
								"MA_DOI_TUONG_THCP_ID"
					;
				
				
				END $$
				;
				
				
				SELECT *
				FROM TMP_DOI_TUONG_TINH_GIA_THANH
				
				;		
		"""  
		return self.execute(query, params)


	def btn_tinh_chi_phi_do_dang_ket_qua_cuoi_ky(self,ky_tinh_gia_thanh_id,chi_nhanh_id,dtthcp_id):
		params = {
			'KY_TINH_GIA_THANH_ID' : ky_tinh_gia_thanh_id,
			'CHI_NHANH_ID' : chi_nhanh_id,
			'DOI_TUONG_THCP_ID' : dtthcp_id,
			}
		query = """   
				DO LANGUAGE plpgsql $$
				DECLARE
				
					ky_tinh_gia_thanh_id INTEGER := %(KY_TINH_GIA_THANH_ID)s;
				
				
					doi_tuong_thcp_id    INTEGER := %(DOI_TUONG_THCP_ID)s;
				
					chi_nhanh_id         INTEGER := %(CHI_NHANH_ID)s;
				
					CHE_DO_KE_TOAN       VARCHAR;
				
					tu_ngay              TIMESTAMP;
				
					den_ngay             TIMESTAMP;
				
					LOAI_GIA_THANH       VARCHAR;
				
					MA_PHAN_CAPNVLTT     VARCHAR(100);
				
					MA_PHAN_CAPNCTT      VARCHAR(100);
				
					MA_PHAN_CAPSXC       VARCHAR(100);
				
					MA_PHAN_CAPSXC_VL    VARCHAR(100);
				
					MA_PHAN_CAPSXC_DCSX  VARCHAR(100);
				
					MA_PHAN_CAPSXC_NVPX  VARCHAR(100);
				
					MA_PHAN_CAPSXC_KH    VARCHAR(100);
				
					MA_PHAN_CAPSXC_MN    VARCHAR(100);
				
					MA_PHAN_CAPCPSX      VARCHAR(100);
				
					CHI_TIET_THEO_DTTHCP BOOLEAN;

					--(JobID) tham số  mảng
				
				
				BEGIN
				
				
					SELECT value
					INTO CHE_DO_KE_TOAN
					FROM ir_config_parameter
					WHERE key = 'he_thong.CHE_DO_KE_TOAN'
					FETCH FIRST 1 ROW ONLY
					;
				
					SELECT "TU_NGAY"
					INTO tu_ngay
					FROM gia_thanh_ky_tinh_gia_thanh AS JP
					WHERE "id" = ky_tinh_gia_thanh_id
					;
				
					SELECT "DEN_NGAY"
					INTO den_ngay
					FROM gia_thanh_ky_tinh_gia_thanh AS JP
					WHERE "id" = ky_tinh_gia_thanh_id
					;
				
					SELECT "LOAI_GIA_THANH"
					INTO LOAI_GIA_THANH
					FROM gia_thanh_ky_tinh_gia_thanh AS JP
					WHERE "id" = ky_tinh_gia_thanh_id
					;
				
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPCPSX
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'CPSX'
					;
				
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPNVLTT
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'NVLTT'
					;
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPNCTT
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'NCTT'
					;
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPSXC
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'SXC'
					;
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPSXC_VL
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'SXC.VL'
						AND "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC || '%%'
					;
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPSXC_DCSX
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'SXC.DCSX'
						AND "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC || '%%'
					;
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPSXC_NVPX
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'SXC.NVPX'
						AND "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC || '%%'
					;
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPSXC_KH
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'SXC.KH'
						AND "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC || '%%'
					;
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPSXC_MN
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'SXC.MN'
						AND "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC || '%%'
					;
				
				
					SELECT "CHI_TIET_THEO_DTTHCP"
					INTO CHI_TIET_THEO_DTTHCP
					FROM gia_thanh_cau_hinh_so_du_dau_ky AS JC
					;
				
				
					DROP TABLE IF EXISTS TMP_DO_DANG
					;
				
					CREATE TEMP TABLE TMP_DO_DANG
					(
						"DOI_TUONG_THCP_ID"    INT,
						"KY_TINH_GIA_THANH_ID" INT,
						"NVL_TRUC_TIEP"        DECIMAL(22, 4),
						"NVL_GIAN_TIEP"        DECIMAL(22, 4),
						"NHAN_CONG_TRUC_TIEP"  DECIMAL(22, 4),
						"NHAN_CONG_GIAN_TIEP"  DECIMAL(22, 4),
						"KHAU_HAO"             DECIMAL(22, 4),
						"GIA_TRI_MUA"          DECIMAL(22, 4),
						"CHI_PHI_KHAC"        DECIMAL(22, 4)
					)
					;
				
				
					IF EXISTS(SELECT "id" AS "CHI_PHI_DO_DANG_ID"
							FROM account_ex_chi_phi_do_dang AS J
							WHERE "MA_DOI_TUONG_THCP_ID" = doi_tuong_thcp_id AND "CHI_NHANH_ID" = chi_nhanh_id
					)
					THEN
						INSERT INTO TMP_DO_DANG
						("DOI_TUONG_THCP_ID",
						"KY_TINH_GIA_THANH_ID",
						"NVL_TRUC_TIEP",
						"NVL_GIAN_TIEP",
						"NHAN_CONG_TRUC_TIEP",
						"NHAN_CONG_GIAN_TIEP",
						"KHAU_HAO",
						"GIA_TRI_MUA",
						"CHI_PHI_KHAC"
				
						)
							SELECT
								J."MA_DOI_TUONG_THCP_ID"
								, ky_tinh_gia_thanh_id
								, CASE WHEN JUD."DOI_TUONG_THCP_ID" IS NULL
								THEN J."CHI_PHI_NVL_TRUC_TIEP"
								ELSE JUD."NVL_TRUC_TIEP"
								END AS "OPN_NVL_TRUC_TIEP"
								, CASE WHEN JUD."DOI_TUONG_THCP_ID" IS NULL
								THEN J."NVL_GIAN_TIEP"
								ELSE JUD."NVL_GIAN_TIEP"
								END AS "OPN_NVL_GIAN_TIEP"
								, CASE WHEN JUD."DOI_TUONG_THCP_ID" IS NULL
								THEN J."CHI_PHI_NHAN_CONG_TRUC_TIEP"
								ELSE JUD."NHAN_CONG_TRUC_TIEP"
								END AS "OPN_NHAN_CONG_TRUC_TIEP"
								, CASE WHEN JUD."DOI_TUONG_THCP_ID" IS NULL
								THEN J."CHI_PHI_NHAN_CONG_GIAN_TIEP"
								ELSE JUD."NHAN_CONG_GIAN_TIEP"
								END AS "OPN_NHAN_CONG_GIAN_TIEP"
								, CASE WHEN JUD."DOI_TUONG_THCP_ID" IS NULL
								THEN J."KHAU_HAO"
								ELSE JUD."KHAU_HAO"
								END AS "OPN_KHAU_HAO"
								, CASE WHEN JUD."DOI_TUONG_THCP_ID" IS NULL
								THEN J."CHI_PHI_MUA_NGOAI"
								ELSE JUD."GIA_TRI_MUA"
								END AS "OPN_GIA_TRI_MUA"
								, CASE WHEN JUD."DOI_TUONG_THCP_ID" IS NULL
								THEN J."CHI_PHI_KHAC"
								ELSE JUD."CHI_PHI_KHAC"
								END AS "OPN_CHI_PHI_KHAC"
							FROM account_ex_chi_phi_do_dang AS J
								LEFT JOIN LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP('{%(DOI_TUONG_THCP_ID)s}', tu_ngay,
																					chi_nhanh_id
							) --JobID
									AS JUD ON JUD."DOI_TUONG_THCP_ID" = J."MA_DOI_TUONG_THCP_ID"
							WHERE J."MA_DOI_TUONG_THCP_ID" = doi_tuong_thcp_id
				
								AND "CHI_NHANH_ID" = chi_nhanh_id
						;
				
				
					ELSE
						INSERT INTO TMP_DO_DANG
						(
							"DOI_TUONG_THCP_ID",
							"KY_TINH_GIA_THANH_ID",
							"NVL_TRUC_TIEP",
							"NVL_GIAN_TIEP",
							"NHAN_CONG_TRUC_TIEP",
							"NHAN_CONG_GIAN_TIEP",
							"KHAU_HAO",
							"GIA_TRI_MUA",
							"CHI_PHI_KHAC"
				
						)
							SELECT
							"DOI_TUONG_THCP_ID"
								, ky_tinh_gia_thanh_id
								, "NVL_TRUC_TIEP"
								, "NVL_GIAN_TIEP"
								, "NHAN_CONG_TRUC_TIEP"
								, "NHAN_CONG_GIAN_TIEP"
								, "KHAU_HAO"
								, "GIA_TRI_MUA"
								, "CHI_PHI_KHAC"
							FROM LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP('{%(DOI_TUONG_THCP_ID)s}', tu_ngay,
																					chi_nhanh_id
							) --ghép tham số vào giá trị 21
						;
						END IF
						;
						IF CHE_DO_KE_TOAN = '15'
						THEN
				
							--Chi phí phát sinh
							INSERT INTO TMP_DO_DANG
							("DOI_TUONG_THCP_ID",
							"KY_TINH_GIA_THANH_ID",
							"NVL_TRUC_TIEP",
							"NVL_GIAN_TIEP",
							"NHAN_CONG_TRUC_TIEP",
							"NHAN_CONG_GIAN_TIEP",
							"KHAU_HAO",
							"GIA_TRI_MUA",
							"CHI_PHI_KHAC"
							)
								SELECT
									"DOI_TUONG_THCP_ID"
									, ky_tinh_gia_thanh_id
									, SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '621%%'
													OR ("MA_TAI_KHOAN" LIKE N'154%%'
														AND "LOAI_HACH_TOAN" = '1'
														AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%'
														AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%'
														AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%'
													)
									THEN COALESCE("GHI_NO", 0)
										- COALESCE("GHI_CO", 0)
										ELSE 0
										END) AS "NVL_TRUC_TIEP"
									, --621
									SUM(CASE WHEN ("MA_TAI_KHOAN" LIKE '6272%%'
													OR "MA_TAI_KHOAN" LIKE '6273%%'
									)
										THEN COALESCE("GHI_NO", 0)
											- COALESCE("GHI_CO", 0)
										ELSE 0
										END) AS "NVL_GIAN_TIEP"
									, --6272,6273
									SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '622%%'
										THEN COALESCE("GHI_NO", 0)
											- COALESCE("GHI_CO", 0)
										ELSE 0
										END) AS "NHAN_CONG_TRUC_TIEP"
									, --622
									SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '6271%%'
										THEN COALESCE("GHI_NO", 0)
											- COALESCE("GHI_CO", 0)
										ELSE 0
										END) AS "NHAN_CONG_GIAN_TIEP"
									, --6271
									SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '6274%%'
										THEN COALESCE("GHI_NO", 0)
											- COALESCE("GHI_CO", 0)
										ELSE 0
										END) AS "KHAU_HAO"
									, --6274
									SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '6277%%'
										THEN COALESCE("GHI_NO", 0)
											- COALESCE("GHI_CO", 0)
										ELSE 0
										END) AS "GIA_TRI_MUA"
									, --6277
									SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '627%%'
													AND "MA_TAI_KHOAN" NOT LIKE '6271%%'
													AND "MA_TAI_KHOAN" NOT LIKE '6272%%'
													AND "MA_TAI_KHOAN" NOT LIKE '6273%%'
													AND "MA_TAI_KHOAN" NOT LIKE '6274%%'
													AND "MA_TAI_KHOAN" NOT LIKE '6277%%'
										THEN COALESCE("GHI_NO", 0)
											- COALESCE("GHI_CO", 0)
										ELSE 0
										END) AS "CHI_PHI_KHAC" --627
								FROM so_cai_chi_tiet AS GL
								WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
							AND "DOI_TUONG_THCP_ID" = doi_tuong_thcp_id
				
							AND "CHI_NHANH_ID" = chi_nhanh_id
							AND ( ( (( "LOAI_HACH_TOAN" = '2'
							AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
							)
							OR "LOAI_HACH_TOAN" = '1')
							)
							OR ( "MA_TAI_KHOAN" LIKE N'154%%'
							AND "LOAI_HACH_TOAN" = '1'
							AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%'
							AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%'
							AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%'
							)
							)
				
							GROUP BY "DOI_TUONG_THCP_ID" ;
				
				
						ELSE
				
				
							--Chi phí phát sinh
							INSERT INTO TMP_DO_DANG
							( "DOI_TUONG_THCP_ID",
							"KY_TINH_GIA_THANH_ID",
							"NVL_TRUC_TIEP",
							"NVL_GIAN_TIEP",
							"NHAN_CONG_TRUC_TIEP",
							"NHAN_CONG_GIAN_TIEP",
							"KHAU_HAO",
							"GIA_TRI_MUA",
							"CHI_PHI_KHAC"
							)
							SELECT
								"DOI_TUONG_THCP_ID"
								, ky_tinh_gia_thanh_id
								, SUM(CASE WHEN "MA_PHAN_CAP" LIKE MA_PHAN_CAPNVLTT
																|| '%%'
								THEN "GHI_NO" - "GHI_CO"
									ELSE 0
									END) AS "NVL_TRUC_TIEP"
								, --621
								SUM(CASE WHEN ("MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC_VL
																	|| '%%'
												OR "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC_DCSX
																	|| '%%'
								)
									THEN "GHI_NO" - "GHI_CO"
									ELSE 0
									END) AS "NVL_GIAN_TIEP"
								, --6272,6273
								SUM(CASE WHEN "MA_PHAN_CAP" LIKE MA_PHAN_CAPNCTT
																|| '%%'
									THEN "GHI_NO" - "GHI_CO"
									ELSE 0
									END) AS "NHAN_CONG_TRUC_TIEP"
								, --622
								SUM(CASE WHEN "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC_NVPX
																|| '%%'
									THEN "GHI_NO" - "GHI_CO"
									ELSE 0
									END) AS "NHAN_CONG_GIAN_TIEP"
								, --6271
								SUM(CASE WHEN "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC_KH
																|| '%%'
									THEN "GHI_NO" - "GHI_CO"
									ELSE 0
									END) AS "KHAU_HAO"
								, --6274
								SUM(CASE WHEN "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC_MN
																|| '%%'
									THEN "GHI_NO" - "GHI_CO"
									ELSE 0
									END) AS "GIA_TRI_MUA"
								, --6277
								SUM(CASE WHEN "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC
																|| '%%'
												AND (EI."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPSXC_VL
																			|| '%%'
													OR MA_PHAN_CAPSXC_VL IS NULL
												)
												AND (EI."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPSXC_DCSX
																			|| '%%'
													OR MA_PHAN_CAPSXC_DCSX IS NULL
												)
												AND (EI."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPSXC_NVPX
																			|| '%%'
													OR MA_PHAN_CAPSXC_NVPX IS NULL
												)
												AND (EI."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPSXC_KH
																			|| '%%'
													OR MA_PHAN_CAPSXC_KH IS NULL
												)
												AND (EI."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPSXC_MN
																			|| '%%'
													OR MA_PHAN_CAPSXC_MN IS NULL
												)
									THEN "GHI_NO" - "GHI_CO"
									ELSE 0
									END) AS "CHI_PHI_KHAC" --627
							FROM so_cai_chi_tiet AS GL
								LEFT JOIN danh_muc_khoan_muc_cp AS EI ON GL."KHOAN_MUC_CP_ID" = EI."id"
							WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
							AND "DOI_TUONG_THCP_ID" = doi_tuong_thcp_id
							AND GL."KHOAN_MUC_CP_ID" IS NOT NULL
				
							AND "CHI_NHANH_ID" = chi_nhanh_id
							AND "MA_TAI_KHOAN" LIKE '154%%'
				
							GROUP BY "DOI_TUONG_THCP_ID"
							;
				
				
						END IF
						;
						
				
				
				
					DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG;
					CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
						AS
				
								SELECT
									"DOI_TUONG_THCP_ID"
									, "KY_TINH_GIA_THANH_ID"
									, SUM("NVL_TRUC_TIEP")                          AS "NVL_TRUC_TIEP"
									, SUM("NVL_GIAN_TIEP")                          AS "NVL_GIAN_TIEP"
									, SUM("NHAN_CONG_TRUC_TIEP") AS "NHAN_CONG_TRUC_TIEP"
									, SUM("NHAN_CONG_GIAN_TIEP")                    AS "NHAN_CONG_GIAN_TIEP"
									, SUM("KHAU_HAO")                               AS "KHAU_HAO"
									, SUM("GIA_TRI_MUA")                            AS "GIA_TRI_MUA"
									, SUM("CHI_PHI_KHAC")                          AS "CHI_PHI_KHAC"
								FROM TMP_DO_DANG AS UD
								GROUP BY "DOI_TUONG_THCP_ID",
									"KY_TINH_GIA_THANH_ID"
								;
				
				
					END $$
				;
				
				
				SELECT *
				FROM TMP_KET_QUA_CUOI_CUNG
				
				;
					
		"""  
		return self.execute(query, params)


	
	def btn_tinh_chi_phi_do_dang_theo_dinh_muc(self,ma_vthh):
		params = {
			'VTHH_ID' : ma_vthh,
			}
		query = """   

				DO LANGUAGE plpgsql $$
				DECLARE
				
					ma_vat_tu_id INTEGER := %(VTHH_ID)s;
				
				
				BEGIN
					DROP TABLE IF EXISTS TMP_KET_QUA;
					CREATE TEMP TABLE TMP_KET_QUA
						AS
				
							SELECT * FROM gia_thanh_khai_bao_dinh_muc_gttp_chi_tiet AS JPQ
								WHERE "MA_THANH_PHAM_ID" = ma_vat_tu_id
								;
				
					END $$
				;
				
				SELECT *
				FROM TMP_KET_QUA
				
				;
				
		"""  
		return self.execute(query, params)



	def lay_du_lieu_doi_tuong_thcp(self,ky_tinh_gia_thanh_id):
		params = {
			'KY_TINH_GIA_THANH_ID' : ky_tinh_gia_thanh_id,
			}
		query = """   

				DO LANGUAGE plpgsql $$
				DECLARE
				
					ky_tinh_gia_thanh_id INTEGER := %(KY_TINH_GIA_THANH_ID)s;
				
				
				BEGIN
				
					DROP TABLE IF EXISTS TMP_TY_LE_PHAN_BO_GIA_THANH_DOI_TUONG_THCP
					;
				
					CREATE TEMP TABLE TMP_TY_LE_PHAN_BO_GIA_THANH_DOI_TUONG_THCP
						AS
				
							SELECT
								JPD."id" AS "GIA_THANH_KY_TINH_GIA_THANH_CHI_TIET_ID"
								, JPD."MA_DOI_TUONG_THCP_ID"
								, JPD."KY_TINH_GIA_THANH_ID"
								, 0                                          AS "TIEU_THUC_PHAN_BO"
								, JP."MA_HANG_ID"
				
								, 0                                         AS "SO_LUONG"
								, COALESCE(JPQ."TONG_CONG", 0) AS "GIA_THANH_DON_VI"
								, 0                                         AS "TY_LE_PB_GIA_THANH_PHAN_TRAM"
				
								, 0                                         AS "TY_LE_PHAN_BO"
								, 0                                          AS "STT"
								, ii."MA" AS "MA_HANG"
								, ii."TEN" AS "TEN_HANG"
								, J."MA_DOI_TUONG_THCP"
								, J."TEN_DOI_TUONG_THCP"
								,J."LOAI"
								, U."DON_VI_TINH"
							FROM gia_thanh_ky_tinh_gia_thanh_chi_tiet AS JPD INNER JOIN danh_muc_doi_tuong_tap_hop_chi_phi AS J
									ON JPD."MA_DOI_TUONG_THCP_ID" = J."id"
								LEFT JOIN danh_muc_chi_tiet_doi_tuong_tinh_gia_thanh AS JP
									ON J."id" = JP."DOI_TUONG_TONG_HOP_CHI_PHI_ID"
								LEFT JOIN danh_muc_vat_tu_hang_hoa AS II ON II."id" = (CASE WHEN J."CHON_THANH_PHAM" IS NULL
									THEN JP."MA_HANG_ID"
																					ELSE J."CHON_THANH_PHAM" END)
								LEFT JOIN danh_muc_don_vi_tinh AS U ON ii."DVT_CHINH_ID" = U."id"
								LEFT JOIN gia_thanh_khai_bao_dinh_muc_gttp_chi_tiet AS JPQ ON II."id" = JPQ."MA_THANH_PHAM_ID"
							WHERE JPD."KY_TINH_GIA_THANH_ID" = ky_tinh_gia_thanh_id ;
				
				
				END $$
				;
				
				
				SELECT *
				FROM TMP_TY_LE_PHAN_BO_GIA_THANH_DOI_TUONG_THCP
				
				;
		
		"""  
		return self.execute(query, params)


	def lay_du_lieu_doi_tuong_tinh_gia_thanh(self,ky_tinh_gia_thanh,chi_nhanh_id,list_vthh_dtthcp_ts):
		params = {
			'KY_TINH_GIA_THANH_ID' : ky_tinh_gia_thanh,
			'CHI_NHANH_ID' : chi_nhanh_id,
			'list_vthh_dtthcp_ts' : list_vthh_dtthcp_ts,
			}
		query = """   
				DO LANGUAGE plpgsql $$
				DECLARE
				
					ky_tinh_gia_thanh_id INTEGER := %(KY_TINH_GIA_THANH_ID)s;
				
					chi_nhanh_id         INTEGER := %(CHI_NHANH_ID)s;
				
					tu_ngay              TIMESTAMP;
				
					den_ngay             TIMESTAMP;
				
					vthh_id_va_dtthcp    VARCHAR := N%(list_vthh_dtthcp_ts)s;
				
				BEGIN
				
					SELECT "TU_NGAY"
					INTO tu_ngay
					FROM gia_thanh_ky_tinh_gia_thanh AS JP
					WHERE "id" = ky_tinh_gia_thanh_id
					;
				
					SELECT "DEN_NGAY"
					INTO den_ngay
					FROM gia_thanh_ky_tinh_gia_thanh AS JP
					WHERE "id" = ky_tinh_gia_thanh_id
					;
				
				
					DROP TABLE IF EXISTS TMP_DOI_TUONG_TINH_GIA_THANH
					;
				
					CREATE TEMP TABLE TMP_DOI_TUONG_TINH_GIA_THANH
						AS
				
							SELECT
								COALESCE(SUM(COALESCE("SO_LUONG_NHAP_THEO_DVT_CHINH", 0)), 0) AS "SO_LUONG"
								, "MA_HANG_ID"
								, "MA_DOI_TUONG_THCP_ID"
							FROM so_kho_chi_tiet AS IL
								INNER JOIN CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(vthh_id_va_dtthcp, ',', ';') AS FCGGSIT
									ON FCGGSIT.Value1 = IL."MA_HANG_ID" AND Value2 = "MA_DOI_TUONG_THCP_ID"
							WHERE
								"MA_TK_CO" LIKE '154%%' AND ("MA_TK_NO" LIKE '15%%' AND "MA_TK_NO" NOT LIKE '154%%')
								AND
								"LOAI_CHUNG_TU" IN ('2010', '2011', '2012', '2013')
								AND "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
				
								AND "CHI_NHANH_ID" = chi_nhanh_id
							GROUP BY
								"MA_HANG_ID",
								"MA_DOI_TUONG_THCP_ID"
					;
				
				
				END $$
				;
				
				
				SELECT vthh."MA" AS "MA_HANG",vthh."TEN" AS "TEN_HANG",dtthcp."MA_DOI_TUONG_THCP",vthh."DVT_CHINH_ID",dvt."DON_VI_TINH" AS "TEN_DVT",KQ.*
				FROM TMP_DOI_TUONG_TINH_GIA_THANH KQ
				LEFT JOIN danh_muc_vat_tu_hang_hoa vthh ON KQ."MA_HANG_ID" = vthh.id
                LEFT JOIN danh_muc_doi_tuong_tap_hop_chi_phi dtthcp on dtthcp.id = KQ."MA_DOI_TUONG_THCP_ID"
				LEFT JOIN danh_muc_don_vi_tinh dvt ON vthh."DVT_CHINH_ID" = dvt.id
				;
	
		"""  
		return self.execute(query, params)


	def lay_du_lieu_tinh_gia_thanh(self,ky_tinh_gia_thanh_id,dtthcp_id):
		params = {
			'KY_TINH_GIA_THANH_ID' : ky_tinh_gia_thanh_id,
			'CHI_NHANH_ID' : self.get_chi_nhanh(),
			'DOI_TUONG_THCP_ID' : dtthcp_id,
			}

		query = """   

				DO LANGUAGE plpgsql $$
				DECLARE
				
					ky_tinh_gia_thanh_id INTEGER := %(KY_TINH_GIA_THANH_ID)s;
				
				
					doi_tuong_thcp_id    INTEGER := %(DOI_TUONG_THCP_ID)s;
				
					chi_nhanh_id         INTEGER := %(CHI_NHANH_ID)s;
				
					CHE_DO_KE_TOAN       VARCHAR;
				
					tu_ngay              TIMESTAMP;
				
					den_ngay             TIMESTAMP;
				
					LOAI_GIA_THANH       VARCHAR;
				
					MA_PHAN_CAPNVLTT     VARCHAR(100);
				
					MA_PHAN_CAPNCTT      VARCHAR(100);
				
					MA_PHAN_CAPSXC       VARCHAR(100);
				
					MA_PHAN_CAPSXC_VL    VARCHAR(100);
				
					MA_PHAN_CAPSXC_DCSX  VARCHAR(100);
				
					MA_PHAN_CAPSXC_NVPX  VARCHAR(100);
				
					MA_PHAN_CAPSXC_KH    VARCHAR(100);
				
					MA_PHAN_CAPSXC_MN    VARCHAR(100);
				
					MA_PHAN_CAPCPSX      VARCHAR(100);
				
					CHI_TIET_THEO_DTTHCP BOOLEAN;
				
				
				BEGIN
				
				
					SELECT value
					INTO CHE_DO_KE_TOAN
					FROM ir_config_parameter
					WHERE key = 'he_thong.CHE_DO_KE_TOAN'
					FETCH FIRST 1 ROW ONLY
					;
				
					SELECT "TU_NGAY"
					INTO tu_ngay
					FROM gia_thanh_ky_tinh_gia_thanh AS JP
					WHERE "id" = ky_tinh_gia_thanh_id
					;
				
					SELECT "DEN_NGAY"
					INTO den_ngay
					FROM gia_thanh_ky_tinh_gia_thanh AS JP
					WHERE "id" = ky_tinh_gia_thanh_id
					;
				
					SELECT "LOAI_GIA_THANH"
					INTO LOAI_GIA_THANH
					FROM gia_thanh_ky_tinh_gia_thanh AS JP
					WHERE "id" = ky_tinh_gia_thanh_id
					;
				
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPCPSX
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'CPSX'
					;
				
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPNVLTT
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'NVLTT'
					;
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPNCTT
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'NCTT'
					;
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPSXC
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'SXC'
					;
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPSXC_VL
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'SXC.VL'
						AND "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC || '%%'
					;
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPSXC_DCSX
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'SXC.DCSX'
						AND "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC || '%%'
					;
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPSXC_NVPX
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'SXC.NVPX'
						AND "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC || '%%'
					;
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPSXC_KH
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'SXC.KH'
						AND "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC || '%%'
					;
				
					SELECT "MA_PHAN_CAP"
					INTO MA_PHAN_CAPSXC_MN
					FROM danh_muc_khoan_muc_cp
					WHERE "MA_KHOAN_MUC_CP" = 'SXC.MN'
						AND "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC || '%%'
					;
				
				
					SELECT "CHI_TIET_THEO_DTTHCP"
					INTO CHI_TIET_THEO_DTTHCP
					FROM gia_thanh_cau_hinh_so_du_dau_ky AS JC
					;
				
				
					DROP TABLE IF EXISTS TMP_DO_DANG
					;
				
					CREATE TEMP TABLE TMP_DO_DANG
					(
						"DOI_TUONG_THCP_ID"    INT,
						"KY_TINH_GIA_THANH_ID" INT,
						"NVL_TRUC_TIEP"        DECIMAL(22, 4),
						"NVL_GIAN_TIEP"        DECIMAL(22, 4),
						"NHAN_CONG_TRUC_TIEP"  DECIMAL(22, 4),
						"NHAN_CONG_GIAN_TIEP"  DECIMAL(22, 4),
						"KHAU_HAO"             DECIMAL(22, 4),
						"GIA_TRI_MUA"          DECIMAL(22, 4),
						"CHI_PHI_KHAC"        DECIMAL(22, 4)
					)
					;
				
				
					IF EXISTS(SELECT "id" AS "CHI_PHI_DO_DANG_ID"
							FROM account_ex_chi_phi_do_dang AS J
							WHERE "MA_DOI_TUONG_THCP_ID" = doi_tuong_thcp_id AND "CHI_NHANH_ID" = chi_nhanh_id
					)
					THEN
						INSERT INTO TMP_DO_DANG
						("DOI_TUONG_THCP_ID",
						"KY_TINH_GIA_THANH_ID",
						"NVL_TRUC_TIEP",
						"NVL_GIAN_TIEP",
						"NHAN_CONG_TRUC_TIEP",
						"NHAN_CONG_GIAN_TIEP",
						"KHAU_HAO",
						"GIA_TRI_MUA",
						"CHI_PHI_KHAC"
				
						)
							SELECT
								J."MA_DOI_TUONG_THCP_ID"
								, ky_tinh_gia_thanh_id
								, CASE WHEN JUD."DOI_TUONG_THCP_ID" IS NULL
								THEN J."CHI_PHI_NVL_TRUC_TIEP"
								ELSE JUD."NVL_TRUC_TIEP"
								END AS "OPN_NVL_TRUC_TIEP"
								, CASE WHEN JUD."DOI_TUONG_THCP_ID" IS NULL
								THEN J."NVL_GIAN_TIEP"
								ELSE JUD."NVL_GIAN_TIEP"
								END AS "OPN_NVL_GIAN_TIEP"
								, CASE WHEN JUD."DOI_TUONG_THCP_ID" IS NULL
								THEN J."CHI_PHI_NHAN_CONG_TRUC_TIEP"
								ELSE JUD."NHAN_CONG_TRUC_TIEP"
								END AS "OPN_NHAN_CONG_TRUC_TIEP"
								, CASE WHEN JUD."DOI_TUONG_THCP_ID" IS NULL
								THEN J."CHI_PHI_NHAN_CONG_GIAN_TIEP"
								ELSE JUD."NHAN_CONG_GIAN_TIEP"
								END AS "OPN_NHAN_CONG_GIAN_TIEP"
								, CASE WHEN JUD."DOI_TUONG_THCP_ID" IS NULL
								THEN J."KHAU_HAO"
								ELSE JUD."KHAU_HAO"
								END AS "OPN_KHAU_HAO"
								, CASE WHEN JUD."DOI_TUONG_THCP_ID" IS NULL
								THEN J."CHI_PHI_MUA_NGOAI"
								ELSE JUD."GIA_TRI_MUA"
								END AS "OPN_GIA_TRI_MUA"
								, CASE WHEN JUD."DOI_TUONG_THCP_ID" IS NULL
								THEN J."CHI_PHI_KHAC"
								ELSE JUD."CHI_PHI_KHAC"
								END AS "OPN_CHI_PHI_KHAC"
							FROM account_ex_chi_phi_do_dang AS J
								LEFT JOIN LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP('{%(DOI_TUONG_THCP_ID)s}', tu_ngay,
																					chi_nhanh_id
							) --ghép tham số vào giá trị 21
									AS JUD ON JUD."DOI_TUONG_THCP_ID" = J."MA_DOI_TUONG_THCP_ID"
							WHERE J."MA_DOI_TUONG_THCP_ID" = doi_tuong_thcp_id
				
								AND "CHI_NHANH_ID" = chi_nhanh_id
						;
				
				
					ELSE
						INSERT INTO TMP_DO_DANG
						(
							"DOI_TUONG_THCP_ID",
							"KY_TINH_GIA_THANH_ID",
							"NVL_TRUC_TIEP",
							"NVL_GIAN_TIEP",
							"NHAN_CONG_TRUC_TIEP",
							"NHAN_CONG_GIAN_TIEP",
							"KHAU_HAO",
							"GIA_TRI_MUA",
							"CHI_PHI_KHAC"
				
						)
							SELECT
							"DOI_TUONG_THCP_ID"
								, ky_tinh_gia_thanh_id
								, "NVL_TRUC_TIEP"
								, "NVL_GIAN_TIEP"
								, "NHAN_CONG_TRUC_TIEP"
								, "NHAN_CONG_GIAN_TIEP"
								, "KHAU_HAO"
								, "GIA_TRI_MUA"
								, "CHI_PHI_KHAC"
							FROM LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP('{%(DOI_TUONG_THCP_ID)s}', tu_ngay,
																					chi_nhanh_id
							) ----JobID
						;
						END IF
						;
				
						IF CHE_DO_KE_TOAN = '15'
						THEN
				
							--Chi phí phát sinh
							INSERT INTO TMP_DO_DANG
							("DOI_TUONG_THCP_ID",
							"KY_TINH_GIA_THANH_ID",
							"NVL_TRUC_TIEP",
							"NVL_GIAN_TIEP",
							"NHAN_CONG_TRUC_TIEP",
							"NHAN_CONG_GIAN_TIEP",
							"KHAU_HAO",
							"GIA_TRI_MUA",
							"CHI_PHI_KHAC"
							)
								SELECT
									"DOI_TUONG_THCP_ID"
									, ky_tinh_gia_thanh_id
									, SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '621%%'
													OR ("MA_TAI_KHOAN" LIKE N'154%%'
														AND "LOAI_HACH_TOAN" = '1'
														AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%'
														AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%'
														AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%'
													)
									THEN COALESCE("GHI_NO", 0)
										- COALESCE("GHI_CO", 0)
										ELSE 0
										END) AS "NVL_TRUC_TIEP"
									, --621
									SUM(CASE WHEN ("MA_TAI_KHOAN" LIKE '6272%%'
													OR "MA_TAI_KHOAN" LIKE '6273%%'
									)
										THEN COALESCE("GHI_NO", 0)
											- COALESCE("GHI_CO", 0)
										ELSE 0
										END) AS "NVL_GIAN_TIEP"
									, --6272,6273
									SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '622%%'
										THEN COALESCE("GHI_NO", 0)
											- COALESCE("GHI_CO", 0)
										ELSE 0
										END) AS "NHAN_CONG_TRUC_TIEP"
									, --622
									SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '6271%%'
										THEN COALESCE("GHI_NO", 0)
											- COALESCE("GHI_CO", 0)
										ELSE 0
										END) AS "NHAN_CONG_GIAN_TIEP"
									, --6271
									SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '6274%%'
										THEN COALESCE("GHI_NO", 0)
											- COALESCE("GHI_CO", 0)
										ELSE 0
										END) AS "KHAU_HAO"
									, --6274
									SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '6277%%'
										THEN COALESCE("GHI_NO", 0)
											- COALESCE("GHI_CO", 0)
										ELSE 0
										END) AS "GIA_TRI_MUA"
									, --6277
									SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '627%%'
													AND "MA_TAI_KHOAN" NOT LIKE '6271%%'
													AND "MA_TAI_KHOAN" NOT LIKE '6272%%'
													AND "MA_TAI_KHOAN" NOT LIKE '6273%%'
													AND "MA_TAI_KHOAN" NOT LIKE '6274%%'
													AND "MA_TAI_KHOAN" NOT LIKE '6277%%'
										THEN COALESCE("GHI_NO", 0)
											- COALESCE("GHI_CO", 0)
										ELSE 0
										END) AS "CHI_PHI_KHAC" --627
								FROM so_cai_chi_tiet AS GL
								WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
							AND "DOI_TUONG_THCP_ID" = doi_tuong_thcp_id
				
							AND "CHI_NHANH_ID" = chi_nhanh_id
							AND ( ( (( "LOAI_HACH_TOAN" = '2'
							AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%'
							)
							OR "LOAI_HACH_TOAN" = '1')
							)
							OR ( "MA_TAI_KHOAN" LIKE N'154%%'
							AND "LOAI_HACH_TOAN" = '1'
							AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '621%%'
							AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '622%%'
							AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '627%%'
							)
							)
				
							GROUP BY "DOI_TUONG_THCP_ID" ;
				
				
						ELSE
				
				
							--Chi phí phát sinh
							INSERT INTO TMP_DO_DANG
							( "DOI_TUONG_THCP_ID",
							"KY_TINH_GIA_THANH_ID",
							"NVL_TRUC_TIEP",
							"NVL_GIAN_TIEP",
							"NHAN_CONG_TRUC_TIEP",
							"NHAN_CONG_GIAN_TIEP",
							"KHAU_HAO",
							"GIA_TRI_MUA",
							"CHI_PHI_KHAC"
							)
							SELECT
								"DOI_TUONG_THCP_ID"
								, ky_tinh_gia_thanh_id
								, SUM(CASE WHEN "MA_PHAN_CAP" LIKE MA_PHAN_CAPNVLTT
																|| '%%'
								THEN "GHI_NO" - "GHI_CO"
									ELSE 0
									END) AS "NVL_TRUC_TIEP"
								, --621
								SUM(CASE WHEN ("MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC_VL
																	|| '%%'
												OR "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC_DCSX
																	|| '%%'
								)
									THEN "GHI_NO" - "GHI_CO"
									ELSE 0
									END) AS "NVL_GIAN_TIEP"
								, --6272,6273
								SUM(CASE WHEN "MA_PHAN_CAP" LIKE MA_PHAN_CAPNCTT
																|| '%%'
									THEN "GHI_NO" - "GHI_CO"
									ELSE 0
									END) AS "NHAN_CONG_TRUC_TIEP"
								, --622
								SUM(CASE WHEN "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC_NVPX
																|| '%%'
									THEN "GHI_NO" - "GHI_CO"
									ELSE 0
									END) AS "NHAN_CONG_GIAN_TIEP"
								, --6271
								SUM(CASE WHEN "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC_KH
																|| '%%'
									THEN "GHI_NO" - "GHI_CO"
									ELSE 0
									END) AS "KHAU_HAO"
								, --6274
								SUM(CASE WHEN "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC_MN
																|| '%%'
									THEN "GHI_NO" - "GHI_CO"
									ELSE 0
									END) AS "GIA_TRI_MUA"
								, --6277
								SUM(CASE WHEN "MA_PHAN_CAP" LIKE MA_PHAN_CAPSXC
																|| '%%'
												AND (EI."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPSXC_VL
																			|| '%%'
													OR MA_PHAN_CAPSXC_VL IS NULL
												)
												AND (EI."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPSXC_DCSX
																			|| '%%'
													OR MA_PHAN_CAPSXC_DCSX IS NULL
												)
												AND (EI."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPSXC_NVPX
																			|| '%%'
													OR MA_PHAN_CAPSXC_NVPX IS NULL
												)
												AND (EI."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPSXC_KH
																			|| '%%'
													OR MA_PHAN_CAPSXC_KH IS NULL
												)
												AND (EI."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPSXC_MN
																			|| '%%'
													OR MA_PHAN_CAPSXC_MN IS NULL
												)
									THEN "GHI_NO" - "GHI_CO"
									ELSE 0
									END) AS "CHI_PHI_KHAC" --627
							FROM so_cai_chi_tiet AS GL
								LEFT JOIN danh_muc_khoan_muc_cp AS EI ON GL."KHOAN_MUC_CP_ID" = EI."id"
							WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
							AND "DOI_TUONG_THCP_ID" = doi_tuong_thcp_id
							AND GL."KHOAN_MUC_CP_ID" IS NOT NULL
				
							AND "CHI_NHANH_ID" = chi_nhanh_id
							AND "MA_TAI_KHOAN" LIKE '154%%'
				
							GROUP BY "DOI_TUONG_THCP_ID"
							;
				
				
						END IF
						;
						
				
				
									--Khoản giảm giá thành
									INSERT INTO  TMP_DO_DANG
									( "DOI_TUONG_THCP_ID",
									"KY_TINH_GIA_THANH_ID",
									"NVL_TRUC_TIEP",
									"NVL_GIAN_TIEP",
									"NHAN_CONG_TRUC_TIEP",
									"NHAN_CONG_GIAN_TIEP",
									"KHAU_HAO",
									"GIA_TRI_MUA",
									"CHI_PHI_KHAC"
				
									)
								SELECT
									doi_tuong_thcp_id
									, ky_tinh_gia_thanh_id
									, COALESCE(SUM(CASE WHEN "MA_TAI_KHOAN" LIKE '154%%'
				
															AND "LOAI_CHUNG_TU" <> '2010'
				
															AND (CHE_DO_KE_TOAN = '15'
																OR (CHE_DO_KE_TOAN = '48'
																	AND (GL."KHOAN_MUC_CP_ID" IS NULL
																		OR "MA_PHAN_CAP" NOT LIKE MA_PHAN_CAPCPSX
																									|| '%%'
																	)
																)
															)
									THEN (-1) * "GHI_CO"
												ELSE 0
												END), 0) AS "NVL_TRUC_TIEP"
									, 0
									, 0
									, 0
									, 0
									, 0
									, 0
								FROM so_cai_chi_tiet AS GL
									LEFT JOIN danh_muc_khoan_muc_cp AS EI ON GL."KHOAN_MUC_CP_ID" = EI."id"
								WHERE "DOI_TUONG_THCP_ID" = doi_tuong_thcp_id
									AND "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
				
								AND "LOAI_HACH_TOAN" = '2' --Chỉ lấy phát sinh có
								AND "CHI_NHANH_ID" = chi_nhanh_id ;
				
				
					DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG;
					CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
						AS
				
								SELECT
									"DOI_TUONG_THCP_ID"
									, "KY_TINH_GIA_THANH_ID"
									, SUM("NVL_TRUC_TIEP")                          AS "NVL_TRUC_TIEP"
									, SUM("NVL_GIAN_TIEP")                          AS "NVL_GIAN_TIEP"
									, SUM("NHAN_CONG_TRUC_TIEP") AS "NHAN_CONG_TRUC_TIEP"
									, SUM("NHAN_CONG_GIAN_TIEP")                    AS "NHAN_CONG_GIAN_TIEP"
									, SUM("KHAU_HAO")                               AS "KHAU_HAO"
									, SUM("GIA_TRI_MUA")                            AS "GIA_TRI_MUA"
									, SUM("CHI_PHI_KHAC")                          AS "CHI_PHI_KHAC"
								FROM TMP_DO_DANG AS UD
								GROUP BY "DOI_TUONG_THCP_ID",
									"KY_TINH_GIA_THANH_ID"
								;
				
				
					END $$
				;
				
				
				SELECT *
				FROM TMP_KET_QUA_CUOI_CUNG
				
				;
		
		
		"""  
		return self.execute(query, params)


	def cap_nhap_gia_nhap_kho(self,vthh_id,dtthcp_id,tu_ngay,den_ngay,chi_nhanh_id,tong_chi_phi,don_gia_nhap):
		params = {
			'VTHH_ID' : vthh_id,
			'DTTHCP_ID' : dtthcp_id,
			'TU_NGAY' : tu_ngay,
			'DEN_NGAY' : den_ngay,
			'TONG_CHI_PHI' : tong_chi_phi,
			'DON_GIA_NHAP' : don_gia_nhap,
			'CHI_NHANH_ID' : chi_nhanh_id,
			}
		query = """   
				DO LANGUAGE plpgsql $$
				DECLARE
				
					vat_tu_hang_hoa_id             INTEGER := %(VTHH_ID)s;
				
					doi_tuong_thcp_id              INTEGER := %(DTTHCP_ID)s;
				
					tu_ngay                        TIMESTAMP := %(TU_NGAY)s;
				
					den_ngay                       TIMESTAMP := %(DEN_NGAY)s;
				
					chi_nhanh_id                   INTEGER := %(CHI_NHANH_ID)s;
				
					TONG_CHI_PHI                   DECIMAL(18, 4) :=%(TONG_CHI_PHI)s;
				
					DON_GIA_NHAP                   DECIMAL(18, 4) :=%(DON_GIA_NHAP)s;
				
					PHAN_THAP_PHAN_DON_GIA         INTEGER;
				
					PHAN_THAP_PHAN_SO_TIEN_QUY_DOI INTEGER;
				
				
					rec                            RECORD;
				
					rec_2                          RECORD;
				
					DEM                            INTEGER;
				
					TONG_CONG                      DECIMAL(18, 4) :=0;
				
					TY_LE_CHUYEN_DOI_DVT           DECIMAL(18, 4);
				
					SO_LUONG                       DECIMAL(18, 4);
				
					DON_GIA                        DECIMAL(18, 4);
				
					TOAN_TU_QUY_DOI                VARCHAR(50);
				
					TONG_TIEN_VON                  DECIMAL(18, 4);
				
				
				BEGIN
				
				
					DROP TABLE IF EXISTS TMP_NHAP_KHO
					;
				
					CREATE TEMP TABLE TMP_NHAP_KHO
				
					(
						"ID_CHUNG_TU"               INT,
						"NHAP_XUAT_KHO_CHI_TIET_ID" INT,
						"Number"                    INT
					)
					;
				
				
					INSERT INTO TMP_NHAP_KHO
					("ID_CHUNG_TU",
					"NHAP_XUAT_KHO_CHI_TIET_ID",
					"Number"
					)
						SELECT
							II."id"                                                                         AS "ID_CHUNG_TU"
							,
							IID."id"                                                                        AS "NHAP_XUAT_KHO_CHI_TIET_ID"
							, ROW_NUMBER()
							OVER (
								ORDER BY "NGAY_HACH_TOAN", "STT_NHAP_CHUNG_TU", "THU_TU_SAP_XEP_CHI_TIET" ) AS "Number"
						FROM stock_ex_nhap_xuat_kho AS II
							INNER JOIN stock_ex_nhap_xuat_kho_chi_tiet AS IID ON II."id" = IID."NHAP_XUAT_ID"
				
						WHERE "LOAI_CHUNG_TU" IN ('2010')--Nhập kho
							AND "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
				
							AND "MA_HANG_ID" = vat_tu_hang_hoa_id
							AND "DOI_TUONG_THCP_ID" = doi_tuong_thcp_id
							AND ((SELECT "SO_TAI_KHOAN"
									FROM danh_muc_he_thong_tai_khoan TK
									WHERE TK.id = "TK_NO_ID") LIKE '15%%'
								AND (SELECT "SO_TAI_KHOAN"
										FROM danh_muc_he_thong_tai_khoan TK
										WHERE TK.id = "TK_CO_ID") LIKE '154%%'
								AND (SELECT "SO_TAI_KHOAN"
										FROM danh_muc_he_thong_tai_khoan TK
										WHERE TK.id = "TK_NO_ID") NOT LIKE '154%%'
							)
							AND (
				
				
								"state" = 'da_ghi_so'
				
							)
							AND "CHI_NHANH_ID" = chi_nhanh_id
					;
				
				
					SELECT value
					INTO PHAN_THAP_PHAN_DON_GIA
					FROM ir_config_parameter
					WHERE key = 'he_thong.PHAN_THAP_PHAN_DON_GIA'
					FETCH FIRST 1 ROW ONLY
					;
				
					SELECT value
					INTO PHAN_THAP_PHAN_SO_TIEN_QUY_DOI
					FROM ir_config_parameter
					WHERE key = 'he_thong.PHAN_THAP_PHAN_SO_TIEN_QUY_DOI'
					FETCH FIRST 1 ROW ONLY
					;
				
				
					SELECT COUNT("ID_CHUNG_TU")
					INTO DEM
					FROM TMP_NHAP_KHO AS II_
					;
				
				
					FOR rec IN
					SELECT
						"ID_CHUNG_TU"               AS "ID_CHUNG_TU"
						, "NHAP_XUAT_KHO_CHI_TIET_ID" AS "NHAP_XUAT_KHO_CHI_TIET_ID"
						, "Number"                    AS "Number"
				
					FROM TMP_NHAP_KHO R
					LOOP
				
						FOR rec_2 IN
				
				
						SELECT
							"TY_LE_CHUYEN_DOI_RA_DVT_CHINH" AS "TY_LE_CHUYEN_DOI_DVT"
							, "SO_LUONG"                      AS "SO_LUONG"
							, "TOAN_TU_QUY_DOI"               AS "TOAN_TU_QUY_DOI"
						FROM stock_ex_nhap_xuat_kho_chi_tiet AS IID
						WHERE "id" = rec."NHAP_XUAT_KHO_CHI_TIET_ID"
				
				
						LOOP
							DON_GIA =
							CASE WHEN rec_2."TOAN_TU_QUY_DOI" = '0'
								THEN
									ROUND(CAST((DON_GIA_NHAP * rec_2."TY_LE_CHUYEN_DOI_DVT") AS NUMERIC),
										PHAN_THAP_PHAN_DON_GIA)
							ELSE
								CASE WHEN rec_2."TY_LE_CHUYEN_DOI_DVT" = 0
									THEN 0
								ELSE ROUND(CAST((DON_GIA_NHAP
												/ rec_2."TY_LE_CHUYEN_DOI_DVT") AS NUMERIC),
										PHAN_THAP_PHAN_DON_GIA)
								END
							END
						;
				
				
							--Cập nhật chi tiết phiếu xuất kho
				
							UPDATE stock_ex_nhap_xuat_kho_chi_tiet
				
				
							SET "DON_GIA_DVT_CHINH" = ROUND(CAST((DON_GIA_NHAP) AS NUMERIC),
															PHAN_THAP_PHAN_DON_GIA),
				
								"DON_GIA_VON"       = DON_GIA
								,
				
								"TIEN_VON_QUY_DOI"  = CASE WHEN rec."Number" = DEM
									THEN ROUND(CAST((TONG_CHI_PHI
													- TONG_CONG) AS NUMERIC),
											PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
													ELSE ROUND(CAST((DON_GIA
																	* SO_LUONG) AS NUMERIC),
																PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
													END
								,
				
								"TIEN_VON"          =
								CASE WHEN rec."Number" = DEM
									THEN ROUND(CAST((TONG_CHI_PHI
													- TONG_CONG) AS NUMERIC),
											PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
								ELSE ROUND(CAST((DON_GIA
												* SO_LUONG) AS NUMERIC),
										PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
								END
							WHERE "id" = rec."NHAP_XUAT_KHO_CHI_TIET_ID"
						;
				
				
							SELECT SUM("TIEN_VON_QUY_DOI")
							INTO TONG_TIEN_VON
				
							FROM stock_ex_nhap_xuat_kho_chi_tiet AS IID
							WHERE "NHAP_XUAT_ID" = rec."ID_CHUNG_TU"
						;
				
							TONG_TIEN_VON = ROUND(CAST((TONG_TIEN_VON) AS NUMERIC),
												PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
						;
				
				
							UPDATE stock_ex_nhap_xuat_kho
							SET "TONG_TIEN" = TONG_TIEN_VON
				
							WHERE "id" = rec."ID_CHUNG_TU"
						;
				
				
							--Cập nhật trên sổ cái
				
							UPDATE so_cai_chi_tiet
							SET "GHI_NO"                 = CASE WHEN "LOAI_HACH_TOAN" = '1'
								THEN CASE WHEN rec."Number" = DEM
									THEN ROUND(CAST((TONG_CHI_PHI
													- TONG_CONG) AS NUMERIC),
											PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
									ELSE ROUND(CAST((DON_GIA
													* SO_LUONG) AS NUMERIC),
												PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
									END
														ELSE "GHI_NO"
														END,
								"GHI_NO_NGUYEN_TE"       = CASE WHEN "LOAI_HACH_TOAN" = '1'
									THEN CASE WHEN rec."Number" = DEM
										THEN ROUND(CAST((TONG_CHI_PHI
														- TONG_CONG) AS NUMERIC),
												PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
										ELSE ROUND(CAST((DON_GIA
														* SO_LUONG) AS NUMERIC),
													PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
										END
														ELSE "GHI_NO_NGUYEN_TE"
														END,
								"GHI_CO"                 = CASE WHEN "LOAI_HACH_TOAN" = '1'
									THEN "GHI_CO"
														ELSE CASE WHEN rec."Number" = DEM
															THEN ROUND(CAST((TONG_CHI_PHI
																				- TONG_CONG) AS NUMERIC),
																		PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
																ELSE ROUND(CAST((DON_GIA
																				* SO_LUONG) AS NUMERIC),
																		PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
																END
														END,
								"GHI_CO_NGUYEN_TE"       = CASE WHEN "LOAI_HACH_TOAN" = '1'
									THEN "GHI_CO_NGUYEN_TE"
														ELSE CASE WHEN rec."Number" = DEM
															THEN ROUND(CAST((TONG_CHI_PHI
																				- TONG_CONG) AS NUMERIC),
																		PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
																ELSE ROUND(CAST((DON_GIA
																				* SO_LUONG) AS NUMERIC),
																		PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
																END
														END,
								"DON_GIA"                = DON_GIA,
								"DON_GIA_NGUYEN_TE"      = DON_GIA,
								"DON_GIA_THEO_DVT_CHINH" = ROUND(CAST((DON_GIA_NHAP) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA)
							WHERE "CHI_TIET_ID" = rec."NHAP_XUAT_KHO_CHI_TIET_ID"  AND "CHI_TIET_MODEL" = 'stock.ex.nhap.xuat.kho.chi.tiet'
						;
				
				
							UPDATE so_kho_chi_tiet
							SET "DON_GIA"                = DON_GIA,
								"DON_GIA_THEO_DVT_CHINH" = DON_GIA_NHAP,
								"SO_TIEN_NHAP"           = CASE WHEN rec."Number" = DEM
									THEN ROUND(CAST((TONG_CHI_PHI - TONG_CONG) AS NUMERIC),
											PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
														ELSE ROUND(CAST((DON_GIA * SO_LUONG) AS NUMERIC),
																	PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
														END
							WHERE "CHI_TIET_ID" = rec."NHAP_XUAT_KHO_CHI_TIET_ID" AND "CHI_TIET_MODEL" = 'stock.ex.nhap.xuat.kho.chi.tiet'
						;
				
				
							UPDATE so_cong_no_chi_tiet
							SET "GHI_NO"                 = CASE WHEN "LOAI_HACH_TOAN" = '1'
								THEN CASE WHEN rec."Number" = DEM
									THEN ROUND(CAST((TONG_CHI_PHI
													- TONG_CONG) AS NUMERIC),
											PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
									ELSE ROUND(CAST((DON_GIA
													* SO_LUONG) AS NUMERIC),
												PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
									END
														ELSE "GHI_NO"
														END,
								"GHI_NO_NGUYEN_TE"       = CASE WHEN "LOAI_HACH_TOAN" = '1'
									THEN CASE WHEN rec."Number" = DEM
										THEN ROUND(CAST((TONG_CHI_PHI
														- TONG_CONG) AS NUMERIC),
												PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
										ELSE ROUND(CAST((DON_GIA
														* SO_LUONG) AS NUMERIC),
													PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
										END
														ELSE "GHI_NO_NGUYEN_TE"
														END,
								"GHI_CO"                 = CASE WHEN "LOAI_HACH_TOAN" = '1'
									THEN "GHI_CO"
														ELSE CASE WHEN rec."Number" = DEM
															THEN ROUND(CAST((TONG_CHI_PHI
																				- TONG_CONG) AS NUMERIC),
																		PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
																ELSE ROUND(CAST((DON_GIA
																				* SO_LUONG) AS NUMERIC),
																		PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
																END
														END,
								"GHI_CO_NGUYEN_TE"       = CASE WHEN "LOAI_HACH_TOAN" = '1'
									THEN "GHI_CO_NGUYEN_TE"
														ELSE CASE WHEN rec."Number" = DEM
															THEN ROUND(CAST((TONG_CHI_PHI
																				- TONG_CONG) AS NUMERIC),
																		PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
																ELSE ROUND(CAST((DON_GIA
																				* SO_LUONG) AS NUMERIC),
																		PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
																END
														END,
								"DON_GIA"                = DON_GIA,
								"DON_GIA_NGUYEN_TE"      = DON_GIA,
								"DON_GIA_THEO_DVT_CHINH" = ROUND(CAST((DON_GIA_NHAP) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA)
							WHERE "CHI_TIET_ID" = rec."NHAP_XUAT_KHO_CHI_TIET_ID" AND "CHI_TIET_MODEL" = 'stock.ex.nhap.xuat.kho.chi.tiet'
						;
				
				
							UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
							SET
								"SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH" = NULL,
								"TONG_GIA_TRI_LUY_KE_KHO"             = NULL,
								"DON_GIA_THEO_DVT_CHINH"              = ROUND(CAST((DON_GIA_NHAP) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA),
								"DON_GIA_DONG"                        = DON_GIA,
				
								"THANH_TIEN_DONG"                     =
								CASE WHEN rec."Number" = DEM
									THEN ROUND(CAST((TONG_CHI_PHI
													- TONG_CONG) AS NUMERIC),
											PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
								ELSE ROUND(CAST((DON_GIA
												* SO_LUONG) AS NUMERIC),
										PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
								END
				
				
								,
								"THANH_TIEN_DONG_DVT_CHINH"           =
								CASE WHEN rec."Number" = DEM
									THEN ROUND(CAST((TONG_CHI_PHI
													- TONG_CONG) AS NUMERIC),
											PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
								ELSE ROUND(CAST((DON_GIA_NHAP) AS NUMERIC)
										* "SO_LUONG_THEO_DVT_CHINH",
										PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
								END
				
							WHERE "ID_CHUNG_TU_CHI_TIET" = rec."NHAP_XUAT_KHO_CHI_TIET_ID"
						;
				
				
							UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
							SET
								"SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH" = NULL,
								"TONG_GIA_TRI_LUY_KE_KHO"             = NULL,
								"DON_GIA_THEO_DVT_CHINH"              = ROUND(CAST((DON_GIA_NHAP) AS NUMERIC), PHAN_THAP_PHAN_DON_GIA),
								"DON_GIA_DONG"                        = DON_GIA,
				
								"THANH_TIEN_DONG"                     =
								CASE WHEN rec."Number" = DEM
									THEN ROUND(CAST((TONG_CHI_PHI
													- TONG_CONG) AS NUMERIC),
											PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
								ELSE ROUND(CAST((DON_GIA
												* SO_LUONG) AS NUMERIC),
										PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
								END
				
				
								,
								"THANH_TIEN_DONG_DVT_CHINH"           =
								CASE WHEN rec."Number" = DEM
									THEN ROUND(CAST((TONG_CHI_PHI
													- TONG_CONG) AS NUMERIC),
											PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
								ELSE ROUND(CAST((DON_GIA_NHAP
												* "SO_LUONG_THEO_DVT_CHINH") AS NUMERIC),
										PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
								END
				
							WHERE "ID_CHUNG_TU_CHI_TIET" = rec."NHAP_XUAT_KHO_CHI_TIET_ID"
						;
				
				
							TONG_CONG = ROUND(CAST((TONG_CONG + DON_GIA * SO_LUONG) AS NUMERIC),
											PHAN_THAP_PHAN_SO_TIEN_QUY_DOI)
						;
				
						END LOOP
					;
				
					END LOOP
					;
				
				
					UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_theo_kho
				
					SET
						"SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH" = NULL,
						"TONG_GIA_TRI_LUY_KE_KHO"             = NULL
					WHERE
						"MA_HANG_ID" = vat_tu_hang_hoa_id
						AND "CHI_NHANH_ID" = chi_nhanh_id
				
						AND "NGAY_HACH_TOAN" >= tu_ngay
					;
				
					UPDATE stock_ex_tinh_gia_xuat_kho_tuc_thoi_khong_theo_kho
				
					SET
						"SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH" = NULL,
						"TONG_GIA_TRI_LUY_KE_KHO"             = NULL
					WHERE
						"MA_HANG_ID" = vat_tu_hang_hoa_id
						AND "CHI_NHANH_ID" = chi_nhanh_id
				
						AND "NGAY_HACH_TOAN" >= tu_ngay
					;
				
				END $$
				;
		
				
		"""  
		self.env.cr.execute(query, params)

	def lay_du_lieu_chi_tiet_chung_tu(self,ky_tinh_gia_thanh_id,chi_nhanh_id,list_item):
		params = {
			'KY_TINH_GIA_THANH_ID' : ky_tinh_gia_thanh_id,
			'CHI_NHANH_ID' : chi_nhanh_id,
			'LIST_ITEM' : list_item,
			}
		query = """   

			DO LANGUAGE plpgsql $$
			DECLARE


				ky_tinh_gia_thanh_id      INTEGER := %(KY_TINH_GIA_THANH_ID)s;

				v_chi_nhanh_id            INTEGER := %(CHI_NHANH_ID)s;

				rec                       RECORD;

				CHE_DO_KE_TOAN            VARCHAR(100);

				Itemlist                  VARCHAR(100) :='6271';

				v_tu_ngay                 TIMESTAMP;

				v_den_ngay                TIMESTAMP;

				TU_NGAY_BAT_DAU_TAI_CHINH TIMESTAMP;


			BEGIN


				SELECT value
				INTO CHE_DO_KE_TOAN
				FROM ir_config_parameter
				WHERE key = 'he_thong.CHE_DO_KE_TOAN'
				FETCH FIRST 1 ROW ONLY
				;

				SELECT value
				INTO TU_NGAY_BAT_DAU_TAI_CHINH
				FROM ir_config_parameter
				WHERE key = 'he_thong.TU_NGAY_BAT_DAU_TAI_CHINH'
				FETCH FIRST 1 ROW ONLY
				;





				SELECT "TU_NGAY"
				INTO v_tu_ngay


				FROM gia_thanh_ky_tinh_gia_thanh AS JP
				WHERE JP."id" = ky_tinh_gia_thanh_id
				;

				SELECT "DEN_NGAY"
				INTO v_den_ngay

				FROM gia_thanh_ky_tinh_gia_thanh AS JP
				WHERE JP."id" = ky_tinh_gia_thanh_id
				;




				DROP TABLE IF EXISTS TMP_SO_TAI_KHOAN_KQ
				;

				CREATE TEMP TABLE TMP_SO_TAI_KHOAN_KQ
				(
					"SO_TAI_KHOAN"         VARCHAR(20),
					"TEN_TAI_KHOAN"        VARCHAR(255),
					"AccountNumberPercent" VARCHAR(25),
					"TINH_CHAT"            VARCHAR(25)


				)
				;

				-- 				IF Itemlist IS NULL OR Itemlist = ''
-- 				THEN
					INSERT INTO TMP_SO_TAI_KHOAN_KQ
						SELECT
							A."SO_TAI_KHOAN"
							, A."TEN_TAI_KHOAN"
							, A."SO_TAI_KHOAN" || '%%'
							, A."TINH_CHAT"
						FROM danh_muc_he_thong_tai_khoan A
						WHERE A."active" = TRUE
							 AND "SO_TAI_KHOAN" IN %(LIST_ITEM)s OR %(LIST_ITEM)s IS NULL 
					;
-- 				ELSE
-- 					INSERT INTO TMP_SO_TAI_KHOAN_KQ
-- 						SELECT
-- 							A."SO_TAI_KHOAN"
-- 							, A."TEN_TAI_KHOAN"
-- 							, A."SO_TAI_KHOAN" || '%%'
-- 							, A."TINH_CHAT"
-- 						FROM danh_muc_he_thong_tai_khoan A
-- 						WHERE "SO_TAI_KHOAN" IN (Itemlist)
-- 					;
-- 				END IF
-- 				;


				DROP TABLE IF EXISTS TMP_KET_QUA
				;

				CREATE TEMP TABLE TMP_KET_QUA

				(
					"ID_CHUNG_TU"     INT,
					"MODEL_CHUNG_TU"  VARCHAR(255),
					"NGAY_CHUNG_TU"   TIMESTAMP,
					"NGAY_HACH_TOAN"  TIMESTAMP,
					"SO_CHUNG_TU"     VARCHAR(25),
					"LOAI_CHUNG_TU"   INT,
					"DIEN_GIAI"       VARCHAR(255),
					"TK_CONG_NO"      VARCHAR(20),
					"KHOAN_MUC_CP_ID" INT,
					"SO_TIEN"         DECIMAL(18, 4),
					"SO_TIEN_Blance"  DECIMAL(18, 4) DEFAULT 0,
					"GIA_TRI_CON_LAI" DECIMAL(18, 4),
					"TY_LE_PHAN_BO"   DECIMAL(18, 4),
					"SO_DA_PHAN_BO"   DECIMAL(18, 4),
					"TK_CONG_NO_ID"   INT

				)
				;


				IF CHE_DO_KE_TOAN = '15'
				THEN


					INSERT INTO TMP_KET_QUA
					("ID_CHUNG_TU",
					"MODEL_CHUNG_TU",
					"NGAY_CHUNG_TU",
					"NGAY_HACH_TOAN",
					"SO_CHUNG_TU",
					"LOAI_CHUNG_TU",
					"DIEN_GIAI",
					"TK_CONG_NO",
					"KHOAN_MUC_CP_ID",
					"SO_TIEN",
					"GIA_TRI_CON_LAI",
					"TY_LE_PHAN_BO",
					"SO_DA_PHAN_BO",
					"TK_CONG_NO_ID"


					)
						SELECT
							GL."ID_CHUNG_TU"
							, GL."MODEL_CHUNG_TU"
							, GL."NGAY_CHUNG_TU"
							, GL."NGAY_HACH_TOAN"
							, GL."SO_CHUNG_TU"
							, CAST(Gl."LOAI_CHUNG_TU" AS INT)
							, GL."DIEN_GIAI_CHUNG"
							, GL."MA_TAI_KHOAN"
							, GL."KHOAN_MUC_CP_ID"
							, SUM(COALESCE(Gl."GHI_NO", 0)
								- COALESCE(Gl."GHI_CO", 0)) AS "SO_TIEN"
							, 0                               AS GIA_TRI_CON_LAI
							, 0                               AS "TY_LE_PHAN_BO"
							, 0                               AS "SO_DA_PHAN_BO"
							, --Tỷ lệ phân bổ
							GL."TAI_KHOAN_ID"               AS "TK_CONG_NO_ID"


						FROM TMP_SO_TAI_KHOAN_KQ
							AS FCLANTT
							INNER JOIN so_cai_chi_tiet AS GL ON FCLANTT."SO_TAI_KHOAN" = GL."MA_TAI_KHOAN"

						WHERE GL."CHI_NHANH_ID" = v_chi_nhanh_id

							AND (("LOAI_HACH_TOAN" = '2' AND "MA_TAI_KHOAN_DOI_UNG" NOT LIKE '154%%') OR "LOAI_HACH_TOAN" = '1')

							AND GL."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay
							AND GL."DOI_TUONG_THCP_ID" IS NULL
							AND GL."DON_DAT_HANG_ID" IS NULL
							AND GL."HOP_DONG_BAN_ID" IS NULL
							AND GL."CONG_TRINH_ID" IS NULL
						GROUP BY
							GL."ID_CHUNG_TU",
							GL."MODEL_CHUNG_TU",
							GL."NGAY_CHUNG_TU",
							GL."NGAY_HACH_TOAN",
							GL."SO_CHUNG_TU",
							CAST(Gl."LOAI_CHUNG_TU" AS INT),
							GL."DIEN_GIAI_CHUNG",
							GL."MA_TAI_KHOAN",
							GL."KHOAN_MUC_CP_ID",
							GL."TAI_KHOAN_ID"
					;


					INSERT INTO TMP_KET_QUA
					(
						"ID_CHUNG_TU",
						"MODEL_CHUNG_TU",
						"NGAY_CHUNG_TU",
						"NGAY_HACH_TOAN",
						"SO_CHUNG_TU",
						"LOAI_CHUNG_TU",
						"DIEN_GIAI",
						"TK_CONG_NO",
						"KHOAN_MUC_CP_ID",
						"SO_TIEN",
						"GIA_TRI_CON_LAI",
						"TY_LE_PHAN_BO",
						"SO_DA_PHAN_BO",
						"TK_CONG_NO_ID"

					)
						SELECT
							"ID_GOC"
							, "MODEL_GOC"
							, "NGAY_CHUNG_TU"
							, "NGAY_HACH_TOAN"
							, "SO_CHUNG_TU"
							, "LOAI_CHUNG_TU"
							, "DIEN_GIAI"
							, (SELECT "SO_TAI_KHOAN"
							FROM danh_muc_he_thong_tai_khoan TK
							WHERE TK.id = JCV."TK_CHI_PHI_ID")
							, "KHOAN_MUC_CP_ID"
							, 0
							, 0
							, 0
							, SUM("SO_PHAN_BO_LAN_NAY")
							, JCV."TK_CHI_PHI_ID"

						FROM TMP_SO_TAI_KHOAN_KQ
							AS FCLANTT
							INNER JOIN GIA_THANH_CHI_TIET_CHUNG_TU_PHAN_BO_CHI_PHI_CHUNG AS JCV
								ON FCLANTT."SO_TAI_KHOAN" = (SELECT "SO_TAI_KHOAN"
															FROM danh_muc_he_thong_tai_khoan TK
															WHERE TK.id = JCV."TK_CHI_PHI_ID")
							LEFT JOIN gia_thanh_ky_tinh_gia_thanh AS JP
								ON JCV."KY_TINH_GIA_THANH_ID" = JP."id"
						WHERE
							"CHI_NHANH_ID" = v_chi_nhanh_id
							AND JCV."KY_TINH_GIA_THANH_ID" <> ky_tinh_gia_thanh_id
							AND "NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay
						GROUP BY
							"ID_GOC",
							"MODEL_GOC",
							"NGAY_CHUNG_TU",
							"NGAY_HACH_TOAN",
							"SO_CHUNG_TU",
							"LOAI_CHUNG_TU",
							"DIEN_GIAI",
							(SELECT "SO_TAI_KHOAN"
							FROM danh_muc_he_thong_tai_khoan TK
							WHERE TK.id = JCV."TK_CHI_PHI_ID"),
							"KHOAN_MUC_CP_ID",
							JCV."TK_CHI_PHI_ID"
					;


					DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
					;

					CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
						AS


							SELECT


								"ID_CHUNG_TU"
								, "MODEL_CHUNG_TU"
								, R."NGAY_CHUNG_TU"
								, "NGAY_HACH_TOAN"
								, "SO_CHUNG_TU"
								, R."LOAI_CHUNG_TU"
								, R."DIEN_GIAI"
								, "TK_CONG_NO"
								, R."KHOAN_MUC_CP_ID"
								, "MA_KHOAN_MUC_CP"
								, "TEN_KHOAN_MUC_CP"
								, SUM("SO_TIEN"
								)                 AS "SO_TIEN"
								, SUM("SO_TIEN" - "SO_DA_PHAN_BO"
								)                 AS "GIA_TRI_CON_LAI"
								, 0                 AS "TY_LE_PHAN_BO"
								, 0                 AS "SO_DA_PHAN_BO"

								, SRT."REFTYPENAME" AS "TEN_LOAI_CHUNG_TU"
								, R."TK_CONG_NO_ID"
							FROM TMP_KET_QUA AS R
								LEFT JOIN danh_muc_reftype AS SRT ON R."LOAI_CHUNG_TU" = SRT."REFTYPE"
								LEFT JOIN danh_muc_khoan_muc_cp AS EI ON R."KHOAN_MUC_CP_ID" = EI."id"
							GROUP BY
								"ID_CHUNG_TU"
								, "MODEL_CHUNG_TU"
								, R."NGAY_CHUNG_TU"
								, "NGAY_HACH_TOAN"
								, "SO_CHUNG_TU"
								, R."LOAI_CHUNG_TU"
								, R."DIEN_GIAI"
								, "TK_CONG_NO"
								, R."KHOAN_MUC_CP_ID"
								, "MA_KHOAN_MUC_CP"
								, "TEN_KHOAN_MUC_CP"


								, SRT."REFTYPENAME"
								, R."TK_CONG_NO_ID"
							HAVING SUM("SO_TIEN" - "SO_DA_PHAN_BO"
								) <> 0
							ORDER BY
								"NGAY_CHUNG_TU",
								"SO_CHUNG_TU"
					;


				ELSE


					INSERT INTO TMP_KET_QUA
					("ID_CHUNG_TU",
					"MODEL_CHUNG_TU",
					"NGAY_CHUNG_TU",
					"NGAY_HACH_TOAN",
					"SO_CHUNG_TU",
					"LOAI_CHUNG_TU",
					"DIEN_GIAI",
					"TK_CONG_NO",
					"KHOAN_MUC_CP_ID",
					"SO_TIEN",
					"SO_TIEN_Blance",
					"GIA_TRI_CON_LAI",
					"TY_LE_PHAN_BO",
					"SO_DA_PHAN_BO",
					"TK_CONG_NO_ID"

					)
						SELECT
							GL."ID_CHUNG_TU"
							, GL."MODEL_CHUNG_TU"
							, GL."NGAY_CHUNG_TU"
							, GL."NGAY_HACH_TOAN"
							, GL."SO_CHUNG_TU"
							,CAST( Gl."LOAI_CHUNG_TU" AS INT)
							, GL."DIEN_GIAI_CHUNG"
							, GL."MA_TAI_KHOAN"
							, GL."KHOAN_MUC_CP_ID"
							, SUM(COALESCE(Gl."GHI_NO", 0)
								- COALESCE(Gl."GHI_CO", 0)) AS "SO_TIEN"
							, SUM(COALESCE(Gl."GHI_NO", 0)
								- COALESCE(Gl."GHI_CO", 0)) AS "SO_TIEN_Blance"
							, 0                               AS GIA_TRI_CON_LAI
							, 0                               AS "TY_LE_PHAN_BO"

							, 0                               AS "SO_DA_PHAN_BO"
							, GL."TAI_KHOAN_ID"
						FROM danh_muc_khoan_muc_cp
							AS FCLANTT
							INNER JOIN so_cai_chi_tiet AS GL ON FCLANTT."id" = GL."KHOAN_MUC_CP_ID"

						WHERE "CHI_NHANH_ID" = v_chi_nhanh_id AND "MA_KHOAN_MUC_CP" IN %(LIST_ITEM)s

							AND "MA_TAI_KHOAN" LIKE '154%%'

							AND "NGAY_HACH_TOAN" <= v_den_ngay
							AND "DOI_TUONG_THCP_ID" IS NULL
							AND "DON_DAT_HANG_ID" IS NULL
							AND "HOP_DONG_BAN_ID" IS NULL
							AND "CONG_TRINH_ID" IS NULL
						GROUP BY
							GL."ID_CHUNG_TU",
							GL."MODEL_CHUNG_TU",
							GL."NGAY_CHUNG_TU",
							GL."NGAY_HACH_TOAN",
							GL."SO_CHUNG_TU",
						CAST( Gl."LOAI_CHUNG_TU" AS INT),
							GL."DIEN_GIAI_CHUNG",
							GL."TAI_KHOAN_ID",
							GL."KHOAN_MUC_CP_ID",
							GL."MA_TAI_KHOAN"
					;


					INSERT INTO TMP_KET_QUA
					("ID_CHUNG_TU",
					"MODEL_CHUNG_TU",
					"NGAY_CHUNG_TU",
					"NGAY_HACH_TOAN",
					"SO_CHUNG_TU",
					"LOAI_CHUNG_TU",
					"DIEN_GIAI",
					"TK_CONG_NO",
					"KHOAN_MUC_CP_ID",
					"SO_TIEN",
					"SO_TIEN_Blance",
					"GIA_TRI_CON_LAI",
					"TY_LE_PHAN_BO",
					"SO_DA_PHAN_BO",
					"TK_CONG_NO_ID"

					)
						SELECT
							"ID_GOC"
							, "MODEL_GOC"
							, "NGAY_CHUNG_TU"
							, "NGAY_HACH_TOAN"
							, "SO_CHUNG_TU"
							, "LOAI_CHUNG_TU"
							, JCV."DIEN_GIAI"
							, (SELECT
							"SO_TAI_KHOAN"
							FROM danh_muc_he_thong_tai_khoan TK
							WHERE TK.id = JCV."TK_CHI_PHI_ID")
							, "KHOAN_MUC_CP_ID"
							, 0
							, (-1) * SUM(CASE WHEN JP."DEN_NGAY" < v_den_ngay
							THEN COALESCE("SO_TIEN", 0)
										ELSE 0 END)
							, 0
							, 0
							, SUM("SO_TIEN")
							, JCV."TK_CHI_PHI_ID"

						FROM danh_muc_khoan_muc_cp
							AS FCLANTT
							INNER JOIN gia_thanh_chi_tiet_chung_tu_phan_bo_chi_phi_chung AS JCV
								ON FCLANTT.id = JCV."KHOAN_MUC_CP_ID"
							LEFT JOIN gia_thanh_ky_tinh_gia_thanh AS JP
								ON JCV."KY_TINH_GIA_THANH_ID" = JP."id"
						WHERE
							JCV."KY_TINH_GIA_THANH_ID" <> ky_tinh_gia_thanh_id
							AND "CHI_NHANH_ID" = v_chi_nhanh_id
							AND (FCLANTT."MA_KHOAN_MUC_CP" IN %(LIST_ITEM)s)

							AND "NGAY_HACH_TOAN" <= v_den_ngay
						GROUP BY
							"ID_GOC"
							, "MODEL_GOC"
							, "NGAY_CHUNG_TU"
							, "NGAY_HACH_TOAN"
							, "SO_CHUNG_TU"
							, "LOAI_CHUNG_TU"
							, JCV."DIEN_GIAI"
							, (SELECT "SO_TAI_KHOAN"
							FROM danh_muc_he_thong_tai_khoan TK
							WHERE TK.id = JCV."TK_CHI_PHI_ID")
							, "KHOAN_MUC_CP_ID"

							, JCV."TK_CHI_PHI_ID"
					;


					DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
					;

					CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
						AS


							SELECT

								"ID_CHUNG_TU"
								,"MODEL_CHUNG_TU"
								, R."NGAY_CHUNG_TU"
								, "NGAY_HACH_TOAN"
								, "SO_CHUNG_TU"
								, R."LOAI_CHUNG_TU"
								, R."DIEN_GIAI"
								, "TK_CONG_NO"
								, R."KHOAN_MUC_CP_ID"
								, "MA_KHOAN_MUC_CP"
								, "TEN_KHOAN_MUC_CP"
								, SUM("SO_TIEN")                   AS "SO_TIEN"
								, SUM("SO_TIEN" - "SO_DA_PHAN_BO") AS "GIA_TRI_CON_LAI"
								, 0                                                AS "TY_LE_PHAN_BO"
								, 0                                                AS "SO_DA_PHAN_BO"

								, SRT."REFTYPENAME" AS "TEN_LOAI_CHUNG_TU"
								,"TK_CONG_NO_ID"
							FROM TMP_KET_QUA AS R
								LEFT JOIN danh_muc_reftype AS SRT ON R."LOAI_CHUNG_TU" = SRT."REFTYPE"
								LEFT JOIN danh_muc_khoan_muc_cp AS EI ON R."KHOAN_MUC_CP_ID" = EI."id"
							GROUP BY
								"ID_CHUNG_TU"
								,"MODEL_CHUNG_TU"
								, R."NGAY_CHUNG_TU"
								, "NGAY_HACH_TOAN"
								, "SO_CHUNG_TU"
								, R."LOAI_CHUNG_TU"
								, R."DIEN_GIAI"
								, "TK_CONG_NO"
								, R."KHOAN_MUC_CP_ID"
								, "MA_KHOAN_MUC_CP"
								, "TEN_KHOAN_MUC_CP"


								, SRT."REFTYPENAME"
								,"TK_CONG_NO_ID"
							HAVING SUM("SO_TIEN" - "SO_DA_PHAN_BO") <> 0
							ORDER BY "NGAY_CHUNG_TU", "SO_CHUNG_TU"
					;

				END IF
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
		DROP FUNCTION IF EXISTS LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP( IN ds_doi_tuong_thcp INT [], tu_ngay TIMESTAMP, chi_nhanh_id INT )
        ;
        
        --Func_JC_GetOpeningUncompletedForJob
        
        CREATE OR REPLACE FUNCTION LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP(IN ds_doi_tuong_thcp INT [],
                                                                                         tu_ngay           TIMESTAMP,
                                                                                         chi_nhanh_id      INT)
        
        
            RETURNS TABLE
            (
                "DOI_TUONG_THCP_ID"                      INT,
                "NVL_TRUC_TIEP"                          DECIMAL(18, 4),
                "NVL_GIAN_TIEP"                          DECIMAL(18, 4),
                "NHAN_CONG_TRUC_TIEP" DECIMAL(18, 4),
                "NHAN_CONG_GIAN_TIEP"                    DECIMAL(18, 4),
                "KHAU_HAO"                               DECIMAL(18, 4),
                "GIA_TRI_MUA"                            DECIMAL(18, 4),
                "CHI_PHI_KHAC"                          DECIMAL(18, 4)
            )
        AS $$
        
        
        
        DECLARE
        
        
            rec RECORD;
        
        
        BEGIN
        
        
              DROP TABLE IF EXISTS LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP_TMP_KET_QUA_GIA_TRI_BANG
            ;
        
            CREATE TEMP TABLE LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP_TMP_KET_QUA_GIA_TRI_BANG
            (
                "DOI_TUONG_THCP_ID"                      INT,
                "NVL_TRUC_TIEP"                          DECIMAL(18, 4),
                "NVL_GIAN_TIEP"                          DECIMAL(18, 4),
                "NHAN_CONG_TRUC_TIEP" DECIMAL(18, 4),
                "NHAN_CONG_GIAN_TIEP"                    DECIMAL(18, 4),
                "KHAU_HAO"                               DECIMAL(18, 4),
                "GIA_TRI_MUA"                            DECIMAL(18, 4),
                "CHI_PHI_KHAC"                          DECIMAL(18, 4)
            )
            ;
        
        
        
            DROP TABLE IF EXISTS LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP_TMP_GIA_TRI_BANG
            ;
        
            CREATE TEMP TABLE LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP_TMP_GIA_TRI_BANG
            (
                "DOI_TUONG_THCP_ID"                      INT,
                "NVL_TRUC_TIEP"                          DECIMAL(18, 4),
                "NVL_GIAN_TIEP"                          DECIMAL(18, 4),
                "NHAN_CONG_TRUC_TIEP" DECIMAL(18, 4),
                "NHAN_CONG_GIAN_TIEP"                    DECIMAL(18, 4),
                "KHAU_HAO"                               DECIMAL(18, 4),
                "GIA_TRI_MUA"                            DECIMAL(18, 4),
                "CHI_PHI_KHAC"                          DECIMAL(18, 4)
            )
            ;
        
            DROP TABLE IF EXISTS LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP_TMP_DOI_TUONG_THCP
            ;
        
            CREATE TEMP TABLE LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP_TMP_DOI_TUONG_THCP
                AS
                    SELECT FCGSIT."id" AS "DOI_TUONG_THCP_ID"
                    FROM danh_muc_doi_tuong_tap_hop_chi_phi AS FCGSIT
                    WHERE "id" = ANY (ds_doi_tuong_thcp)
            ;
        
        
            FOR rec IN SELECT DT."DOI_TUONG_THCP_ID"
                       FROM LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP_TMP_DOI_TUONG_THCP DT
            LOOP
        
        
                IF (SELECT COUNT(JP."id")
                    FROM gia_thanh_ky_tinh_gia_thanh AS JP
                        INNER JOIN gia_thanh_ky_tinh_gia_thanh_chi_tiet AS JPD ON JP."id" = JPD."KY_TINH_GIA_THANH_ID"
                        LEFT JOIN gia_thanh_ket_qua_chi_phi_do_dang_cuoi_ky_chi_tiet AS JUD
                            ON JPD."KY_TINH_GIA_THANH_ID" = JUD."KY_TINH_GIA_THANH_ID"
                               AND JPD."MA_DOI_TUONG_THCP_ID" = JUD."MA_DOI_TUONG_THCP_ID"
                    WHERE JP."DEN_NGAY" < tu_ngay
        
                          AND JP."CHI_NHANH_ID" = chi_nhanh_id
                          AND JPD."MA_DOI_TUONG_THCP_ID" = rec."DOI_TUONG_THCP_ID"
                   ) > 0
                THEN
                    INSERT INTO LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP_TMP_GIA_TRI_BANG
                    ("DOI_TUONG_THCP_ID",
                     "NVL_TRUC_TIEP",
                     "NVL_GIAN_TIEP",
                     "NHAN_CONG_TRUC_TIEP",
                     "NHAN_CONG_GIAN_TIEP",
                     "KHAU_HAO",
                     "GIA_TRI_MUA",
                     "CHI_PHI_KHAC"
                    )
                        SELECT
        
                            JPD."MA_DOI_TUONG_THCP_ID"
                            , JUD."NVL_TRUC_TIEP"
                            , JUD."NVL_GIAN_TIEP"
                            , JUD."NHAN_CONG_TRUC_TIEP"
                            , JUD."NHAN_CONG_GIAN_TIEP"
                            , JUD."KHAU_HAO"
                            , JUD."CHI_PHI_MUA_NGOAI"
                            , JUD."CHI_PHI_KHAC"
                        FROM gia_thanh_ky_tinh_gia_thanh AS JP
                            INNER JOIN gia_thanh_ky_tinh_gia_thanh_chi_tiet AS JPD ON JP."id" = JPD."KY_TINH_GIA_THANH_ID"
                            LEFT JOIN gia_thanh_ket_qua_chi_phi_do_dang_cuoi_ky_chi_tiet AS JUD
                                ON JPD."KY_TINH_GIA_THANH_ID" = JUD."KY_TINH_GIA_THANH_ID"
                                   AND JPD."MA_DOI_TUONG_THCP_ID" = JUD."MA_DOI_TUONG_THCP_ID"
                        WHERE JP."DEN_NGAY" < tu_ngay
        
                              AND JP."CHI_NHANH_ID" = chi_nhanh_id
                              AND JPD."MA_DOI_TUONG_THCP_ID" = rec."DOI_TUONG_THCP_ID"
                        ORDER BY DATE_PART('day', "DEN_NGAY" :: TIMESTAMP, tu_ngay)
                        LIMIT 1
                    ;
        
                ELSE
        
                    INSERT INTO LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP_TMP_GIA_TRI_BANG
                    ("DOI_TUONG_THCP_ID",
                     "NVL_TRUC_TIEP",
                     "NVL_GIAN_TIEP",
                     "NHAN_CONG_TRUC_TIEP",
                     "NHAN_CONG_GIAN_TIEP",
                     "KHAU_HAO",
                     "GIA_TRI_MUA",
                     "CHI_PHI_KHAC"
                    )
                        SELECT
        
                            J."MA_DOI_TUONG_THCP_ID"
                            , J."CHI_PHI_NVL_TRUC_TIEP"
                            , J."NVL_GIAN_TIEP"
                            , J."CHI_PHI_NHAN_CONG_TRUC_TIEP"
                            , J."CHI_PHI_NHAN_CONG_GIAN_TIEP"
                            , J."KHAU_HAO"
                            , J."CHI_PHI_MUA_NGOAI"
                            , J."CHI_PHI_KHAC"
                        FROM account_ex_chi_phi_do_dang AS J
                        WHERE
        
                            J."CHI_NHANH_ID" = chi_nhanh_id
                            AND J."MA_DOI_TUONG_THCP_ID" = rec."DOI_TUONG_THCP_ID"
                        LIMIT 1
                    ;
        
                END IF
            ;
        
            END LOOP
            ;
            INSERT INTO LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP_TMP_KET_QUA_GIA_TRI_BANG(
                SELECT
                    KQ."DOI_TUONG_THCP_ID",
                      KQ."NVL_TRUC_TIEP",
                      KQ."NVL_GIAN_TIEP",
                      KQ."NHAN_CONG_TRUC_TIEP",
                      KQ."NHAN_CONG_GIAN_TIEP",
                      KQ."KHAU_HAO",
                      KQ."GIA_TRI_MUA",
                      KQ."CHI_PHI_KHAC"
                FROM LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP_TMP_GIA_TRI_BANG KQ );
        
              RETURN QUERY SELECT *
                                    FROM LAY_CHI_PHI_DO_DANG_DAU_KY_CUA_TUNG_DOI_TUONG_THCP_TMP_KET_QUA_GIA_TRI_BANG
                        ;
        END
         $$ LANGUAGE PLpgSQL
                    ;
        
       

		""")
		self.env.cr.execute(""" 
			DROP FUNCTION IF EXISTS LAY_SO_TIEN_DA_PHAN_BO_CUA_CHUNG_TU(IN id_chung_tu INTEGER,

			so_tai_khoan VARCHAR,
			khoan_muc_chi_phi_id INT,


			CHE_DO_KE_TOAN VARCHAR,
			ky_tinh_gia_thanh_id INTEGER

			) --GetAllocatedAmountOfVoucher
			;

			CREATE OR REPLACE FUNCTION LAY_SO_TIEN_DA_PHAN_BO_CUA_CHUNG_TU(IN id_chung_tu INTEGER,

			so_tai_khoan VARCHAR,
			khoan_muc_chi_phi_id INT,


			CHE_DO_KE_TOAN VARCHAR,
			ky_tinh_gia_thanh_id INTEGER

			)
			RETURNS DECIMAL(18, 4)
			AS $$
			DECLARE
			DECLARE




			dResult DECIMAL(18, 4);


			BEGIN


			IF CHE_DO_KE_TOAN = '15'
			THEN
			SELECT SUM(COALESCE(JV."SO_PHAN_BO_LAN_NAY", 0))
			INTO dResult
			FROM gia_thanh_chi_tiet_chung_tu_phan_bo_chi_phi_chung JV
			WHERE (SELECT "SO_TAI_KHOAN"
			FROM danh_muc_he_thong_tai_khoan TK
			WHERE TK.id = JV."TK_CHI_PHI_ID") = so_tai_khoan
			AND JV."ID_GOC" = id_chung_tu
			AND JV."KY_TINH_GIA_THANH_ID" <> ky_tinh_gia_thanh_id
			;
			ELSE

			SELECT SUM(COALESCE(JV."SO_PHAN_BO_LAN_NAY", 0))
			INTO dResult
			FROM gia_thanh_chi_tiet_chung_tu_phan_bo_chi_phi_chung JV
			WHERE JV."KHOAN_MUC_CP_ID" = khoan_muc_chi_phi_id
			AND JV."ID_GOC" = id_chung_tu
			AND JV."KY_TINH_GIA_THANH_ID" <> ky_tinh_gia_thanh_id
			;


			END IF
			;

			RETURN dResult
			;
			END
			;
			$$ LANGUAGE PLpgSQL
			;
		""")