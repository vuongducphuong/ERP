# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class PURCHASE_EX_LAP_TU_CHUNG_TU_BAN_HANG_FORM(models.Model):
	_name = 'purchase.ex.lap.tu.chung.tu.ban.hang.form'
	_description = ''
	_auto = False

	KHACH_HANG_ID = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng')
	TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng', related='KHACH_HANG_ID.HO_VA_TEN', )
	KHOANG_THOI_GIAN = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Khoảng thời gian', help='Khoảng thời gian', default='DAU_THANG_DEN_HIEN_TAI',required=True)
	TU_NGAY = fields.Date(string='Từ', help='Từ ngày',default=fields.Datetime.now)
	DEN_NGAY = fields.Date(string='Đến', help='Đến ngày',default=fields.Datetime.now)
	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh')

	@api.onchange('KHOANG_THOI_GIAN')
	def _cap_nhat_ngay(self):
		self.onchange_time(self.KHOANG_THOI_GIAN, 'TU_NGAY', 'DEN_NGAY')
	#FIELD_IDS = fields.One2many('model.name')
	@api.model
	def default_get(self, fields_list):
	  result = super(PURCHASE_EX_LAP_TU_CHUNG_TU_BAN_HANG_FORM, self).default_get(fields_list)
	  result['CHI_NHANH_ID'] = self.env['danh.muc.to.chuc'].search([],limit=1).id
	  return result
	PURCHASE_EX_LAP_TU_CHUNG_TU_BAN_HANG_FORM_CHI_TIET_IDS = fields.One2many('purchase.ex.lap.tu.chung.tu.ban.hang.form.chi.tiet', 'CHI_TIET_ID', string='Lập từ chứng từ bán hàng form chi tiết')

	@api.model
	def thuc_hien_lay_du_lieu_cac_chung_tu(self, args):
		new_line = [[5]]
		# param ={}
		record =[]
		# query = """ 
		
		# """ 

		# record = self.execute(query, param)
		# for line in record:
		new_line += [(0,0,{'ID_CHUNG_TU_BAN_HANG': 1029,
			'NGAY_HACH_TOAN' : '03-12-2018',
			'NGAY_CHUNG_TU' :'03-12-2018',
			'SO_CHUNG_TU' : 'BH0035',
			'NGAY_HOA_DON' :'03-12-2018',
			'SO_HOA_DON' :'',
			'currency_id' : 'VND',
			'TY_GIA' :1,
			'TEN_DOI_TUONG' :'Cục thuế quận Ba Đình',
			'DIEN_GIAI' :'Bán hàng Cục thuế quận Ba Đình',
			'SO_TIEN' :585900,
			'TEN_CHI_NHANH' :'Công ty Cổ phần ABC',})] 
		return new_line

	@api.model
	def thuc_hien_lay_chi_tiet_cac_chung_tu(self, args):
		danh_sach_chi_tiet_cac_chung_tu = [[5]]
		if 'list_id_chung_tu_ban_hang' in args:
			for i in args['list_id_chung_tu_ban_hang']:
				danh_sach_chi_tiet_list = self.env['sale.document.line'].search([('SALE_DOCUMENT_ID', '=', i)]) 
				for line in danh_sach_chi_tiet_list : 
					dien_giai_thue =''
					if line.MA_HANG_ID:
						dien_giai_thue = 'Thuế GTGT - ' + str(line.MA_HANG_ID.TEN)
					danh_sach_chi_tiet_cac_chung_tu += [(0,0,{
						'MA_HANG_ID':[line.MA_HANG_ID.id , line.MA_HANG_ID.MA],
						'name': line.TEN_HANG,
						'DVT_ID':[line.DVT_ID.id , line.DVT_ID.DON_VI_TINH],
						'SO_LUONG':line.SO_LUONG,
						'DON_GIA':line.DON_GIA,
						'THANH_TIEN':line.THANH_TIEN,
						'TY_LE_CK':line.TY_LE_CK,
						'TIEN_CHIET_KHAU':line.TIEN_CHIET_KHAU,
						'THANH_TIEN_QUY_DOI':line.THANH_TIEN_QUY_DOI,
						'TONG_GIA_TRI':line.THANH_TIEN,
						'DIEN_GIAI_THUE':dien_giai_thue,
						'THUE_GTGT_ID':[line.THUE_GTGT_ID.id , line.THUE_GTGT_ID.name],
						'TIEN_THUE_GTGT':line.TIEN_THUE_GTGT,
					})]
		return danh_sach_chi_tiet_cac_chung_tu

				