# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision
from operator import itemgetter

class BAO_CAO_S35_DN_SO_CHI_TIET_BAN_HANG(models.Model):
	_name = 'bao.cao.s35.dn.so.chi.tiet.ban.hang'
	
	
	_auto = False

	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
	BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
	KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI',required=True)
	TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày', required=True )
	DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày', required=True)
	NHOM_VTHH_ID = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm VTHH', help='Nhóm vật tư hàng hóa')
	NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
	NGAY_CHUNG_TU = fields.Date(string='Ngày', help='Ngày')
	SO_HIEU_CHUNG_TU = fields.Char(string='Số hiệu', help='Số hiệu')
	NGAY_HOA_DON = fields.Date(string='Ngày', help='Ngày hóa đơn ')
	SO_HOA_DON = fields.Char(string='Số', help='Số hóa đơn')
	DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
	TAI_KHOAN_DOI_UNG = fields.Char(string='TK đối ứng', help='Tài khoản đối ứng')
	name = fields.Char(string='Name', help='Name', oldname='NAME')
	DVT = fields.Char(string='ĐVT', help='Đơn vị tính')
	SO_LUONG_BAN = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
	DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits= decimal_precision.get_precision('DON_GIA'))
	THANH_TIEN = fields.Float(string='Thành tiền', help='Thành tiền',digits= decimal_precision.get_precision('Product Price'))
	THUE = fields.Float(string='Thuế', help='Thuế',digits= decimal_precision.get_precision('Product Price'))
	KHAC_521 = fields.Char(string='Khác(521)', help='Khác(521)')
	LA_TONG_HOP = fields.Boolean()
	MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa')

	CHON_TAT_CA_SAN_PHAM = fields.Boolean('Tất cả sản phẩm', default=True)
	SAN_PHAM_MANY_IDS = fields.Many2many('danh.muc.vat.tu.hang.hoa','s35_dn_so_chi_tiet_ban_hang_danh_muc_vthh', string='Chọn sản phẩm')
	SAN_PHAM_IDS = fields.One2many('danh.muc.vat.tu.hang.hoa')
	MA_PC_NHOM_VTHH = fields.Char()

	@api.onchange('NGAY_HACH_TOAN')
	def _onchange_NGAY_HACH_TOAN(self):
		if self.NGAY_CHUNG_TU:
			self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN
	
	# Onchange cho các field relation Many2many-One2many
	@api.onchange('SAN_PHAM_IDS')
	def _onchange_SAN_PHAM_IDS(self):
		self.SAN_PHAM_MANY_IDS =self.SAN_PHAM_IDS.ids

	@api.onchange('SAN_PHAM_MANY_IDS')
	def _onchange_SAN_PHAM_MANY_IDS(self):
		self.SAN_PHAM_IDS =self.SAN_PHAM_MANY_IDS.ids
	
	@api.onchange('NHOM_VTHH_ID')
	def update_SAN_PHAM_IDS(self):
		# Khi thay đổi NHOM_VTHH_ID thì clear hết VTHH đã chọn
		self.SAN_PHAM_MANY_IDS = []
		self.MA_PC_NHOM_VTHH =self.NHOM_VTHH_ID.MA_PHAN_CAP
	
	

	# Hàm thay đổi thời gian khi chọn kỳ báo cáo  
	@api.onchange('KY_BAO_CAO')
	def _cap_nhat_ngay(self):
		self.onchange_time(self.KY_BAO_CAO, 'TU_NGAY', 'DEN_NGAY')

	### START IMPLEMENTING CODE ###
	@api.model
	def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
		record = []
		# Get paramerters here
		params = self._context
		if not params.get('active_model'):
			return
		chi_nhanh_id = params.get('CHI_NHANH_ID')
		bao_gom_du_lieu_chi_nhanh_phu_thuoc = params.get('BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC')
		tu_ngay = params.get('TU_NGAY')
		tu_ngay_f = datetime.strptime(tu_ngay, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		den_ngay = params.get('DEN_NGAY')
		den_ngay_f = datetime.strptime(den_ngay, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		
		NHOM_VTHH_ID = params.get('NHOM_VTHH_ID')
		MA_PC_NHOM_VTHH = params.get('MA_PC_NHOM_VTHH')

		if params.get('CHON_TAT_CA_SAN_PHAM'):
			domain = []
			if MA_PC_NHOM_VTHH:
				domain += [('LIST_MPC_NHOM_VTHH','ilike', '%'+ MA_PC_NHOM_VTHH +'%')]
			SAN_PHAM_IDS = self.env['danh.muc.vat.tu.hang.hoa'].search(domain).ids
		else:
			SAN_PHAM_IDS = params.get('SAN_PHAM_MANY_IDS')
			
		record = []
		thu_tu = 0
		cr = self.env.cr
		# Execute SQL query here
		params = {
			'tu_ngay':tu_ngay_f, 
			'den_ngay':den_ngay_f, 
			'ma_hang_ids':SAN_PHAM_IDS or None,
			'chi_nhanh_id': chi_nhanh_id, 
			'bao_gom_du_lieu_chi_nhanh_phu_thuoc':bao_gom_du_lieu_chi_nhanh_phu_thuoc,
			} 
		# Bảng chi tiết
		query = """
			SELECT  SL."NGAY_HACH_TOAN" ,
				SL."NGAY_CHUNG_TU" ,
				SL."SO_CHUNG_TU" ,
				SL."ID_CHUNG_TU" ,
				SL."LOAI_CHUNG_TU" ,
				SL."NGAY_HOA_DON" ,
				SL."SO_HOA_DON" ,
				SL."DIEN_GIAI_CHUNG" ,
				SL."MA_TK_NO" ,
				SL."DVT_ID" ,
				SL."TEN_DVT" ,
				SUM(SL."SO_LUONG") AS "SO_LUONG" ,
				CASE WHEN SL."SO_TIEN_GIAM_TRU" <> 0
						  OR SL."SO_TIEN_TRA_LAI" <> 0 THEN 0
					 ELSE SL."DON_GIA"
				END "DON_GIA" , -- Không lấy đơn giá của bán trả lại và giảm giá
				SUM(SL."SO_TIEN") "THANH_TIEN" ,
				SUM(SL."SO_TIEN_NHAP_KHAU") "SO_TIEN_THUE_VAT" ,
				SUM(SL."SO_TIEN_GIAM_TRU" + SL."SO_TIEN_TRA_LAI" + SL."SO_TIEN_CHIET_KHAU") "TONG_TIEN_GIAM_TRU" ,
				SL."MA_HANG_ID" ,
				SL."TEN_HANG" ,
				SL."MA_HANG"
		FROM    so_ban_hang_chi_tiet SL
				--LEFT JOIN dbo.Unit U ON U."DVT_ID" = SL."DVT_ID"
				--INNER JOIN @tblListchi_nhanh_id AS TLB ON SL.chi_nhanh_id = TLB.chi_nhanh_id
				--INNER JOIN @tblList"MA_HANG_ID" AS LII ON SL."MA_HANG_ID" = LII."MA_HANG_ID"
		WHERE   SL."NGAY_HACH_TOAN" BETWEEN %(tu_ngay)s AND %(den_ngay)s
				AND SL."MA_HANG_ID" = any (%(ma_hang_ids)s)
		GROUP BY SL."NGAY_HACH_TOAN" ,
				SL."NGAY_CHUNG_TU" ,
				SL."SO_CHUNG_TU" ,
				SL."ID_CHUNG_TU" ,
				SL."LOAI_CHUNG_TU" ,
				SL."NGAY_HOA_DON" ,
				SL."SO_HOA_DON" ,
				SL."DIEN_GIAI_CHUNG" ,
				SL."MA_TK_NO" ,
				SL."DVT_ID" ,
				SL."TEN_DVT" ,
				SL."SO_TIEN_TRA_LAI" ,
				SL."SO_TIEN_GIAM_TRU" ,
				SL."DON_GIA" ,
				SL."MA_HANG_ID" ,
				SL."TEN_HANG" ,
				SL."MA_HANG"
		ORDER BY SL."TEN_HANG" ,
				SL."NGAY_HACH_TOAN" ,
				SL."NGAY_CHUNG_TU" ,
				SL."SO_CHUNG_TU"
			"""
		cr.execute(query,params)
		for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
			record.append({
				'MA_HANG_ID': line.get('MA_HANG_ID', ''),
				"TEN_HANG": line.get('TEN_HANG', ''),
				'NGAY_HACH_TOAN': line.get('NGAY_HACH_TOAN', ''),
				'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU', ''),
				'SO_HIEU_CHUNG_TU': line.get('SO_CHUNG_TU', ''),
				'NGAY_HOA_DON': line.get('NGAY_HOA_DON', ''),
				'SO_HOA_DON':line.get('SO_HOA_DON', ''),
				'DIEN_GIAI': line.get('DIEN_GIAI_CHUNG', ''),
				'TAI_KHOAN_DOI_UNG': line.get('MA_TK_NO', ''),
				'DVT': line.get('TEN_DVT', ''),
				'SO_LUONG_BAN': line.get('SO_LUONG', ''),
				'DON_GIA': line.get('DON_GIA', ''),
				'THANH_TIEN':line.get('THANH_TIEN', ''),
				'THUE': line.get('SO_TIEN_THUE_VAT', ''),
				'KHAC_521': line.get('TONG_TIEN_GIAM_TRU', ''),
				'THU_TU': thu_tu,
				'LA_TONG_HOP': False,
				})
			thu_tu += 1
		sorted_record = sorted(record, key=itemgetter('MA_HANG_ID','THU_TU'))
		sorted_record += [{'MA_HANG_ID': None}] # Trick for the last record
		# Bảng tính giá vốn hàng bán
		query = """
			SELECT  LII."MA_HANG_ID" ,
				SUM(CASE WHEN IL."MA_TK_CO" LIKE '632%%'
						 THEN IL."SO_TIEN_XUAT" - IL."SO_TIEN_NHAP"
						 ELSE 0
					END) "GIA_VON"
		FROM    (SELECT DISTINCT
						SL."MA_HANG_ID",
						SL."TEN_HANG" ,
						SL."MA_HANG"
				FROM    so_ban_hang_chi_tiet SL
						--INNER JOIN @tblListchi_nhanh_id AS TLB ON SL.chi_nhanh_id = TLB.chi_nhanh_id
				WHERE   SL."NGAY_HACH_TOAN" BETWEEN %(tu_ngay)s AND %(den_ngay)s AND SL."MA_HANG_ID" = any (%(ma_hang_ids)s)
				GROUP BY SL."MA_HANG_ID" ,
						SL."TEN_HANG" ,
						SL."MA_HANG"
				) AS LII
				LEFT JOIN ( SELECT  IL1.*
							FROM    so_kho_chi_tiet IL1
									--INNER JOIN @tblListchi_nhanh_id AS TLB ON TLB.chi_nhanh_id = IL1.chi_nhanh_id AND IL1."NGAY_HACH_TOAN" BETWEEN @tu_ngay AND @den_ngay
						  ) AS IL ON LII."MA_HANG_ID" = IL."MA_HANG_ID"
		GROUP BY LII."MA_HANG_ID"
			"""
		cr.execute(query,params)
		gia_von = {}
		for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
			gia_von[line.get('MA_HANG_ID')] = line.get('GIA_VON', '')
		final_record = []
		sl_phat_sinh = 0.0
		tt_phat_sinh = 0.0
		ma_hang = ''
		for r in sorted_record:
			if ma_hang != r.get('MA_HANG_ID'):
				if (ma_hang != ''): # Tổng kết
					final_record += [{
						'MA_HANG_ID': ma_hang,
						'DIEN_GIAI': 'Cộng số phát sinh',
						'SO_LUONG': sl_phat_sinh,
						'THANH_TIEN': tt_phat_sinh,
						'LA_TONG_HOP': True,
						'DON_GIA': '',
						'THUE': '',
					}]
					final_record += [{
						'MA_HANG_ID': ma_hang,
						'DIEN_GIAI': '- Doanh thu thuần',
						'THANH_TIEN': tt_phat_sinh,
						'LA_TONG_HOP': True,
						'SO_LUONG_BAN': '',
						'DON_GIA': '',
						'THUE': '',
					}]
					final_record += [{
						'MA_HANG_ID': ma_hang,
						'DIEN_GIAI': '- Giá vốn hàng bán',
						'THANH_TIEN': gia_von[ma_hang],
						'LA_TONG_HOP': True,
						'SO_LUONG_BAN': '',
						'DON_GIA': '',
						'THUE': '',
					}]
					final_record += [{
						'MA_HANG_ID': ma_hang,
						'DIEN_GIAI': '- Lãi gộp',
						'THANH_TIEN': tt_phat_sinh - gia_von[ma_hang],
						'LA_TONG_HOP': True,
						'SO_LUONG_BAN': '',
						'DON_GIA': '',
						'THUE': '',
					}]
				# if (r.get('MA_HANG_ID') != None):
				#     final_record += [{
				#         'DIEN_GIAI': 'Tên sản phẩm: ' + r.get('TEN_HANG'),
				#         'LA_TONG_HOP': True,
				#         'SO_LUONG_BAN': '',
				#         'DON_GIA': '',
				#         'THANH_TIEN': '',
				#         'THUE': '',
				#     }]
				ma_hang = r.get('MA_HANG_ID')
				sl_phat_sinh = r.get('SO_LUONG_BAN', 0)
				tt_phat_sinh = r.get('THANH_TIEN', 0)
			else:
				sl_phat_sinh += r.get('SO_LUONG_BAN', 0)
				tt_phat_sinh += r.get('THANH_TIEN', 0)
			if (r.get('MA_HANG_ID') != None):
				final_record += [r]
		
		return final_record

	def _validate(self):
		params = self._context
		SAN_PHAM_IDS = params['SAN_PHAM_IDS'] if 'SAN_PHAM_IDS' in params.keys() else 'False'
		TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
		TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
		DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
		SAN_PHAM_MANY_IDS = params['SAN_PHAM_MANY_IDS'] if 'SAN_PHAM_MANY_IDS' in params.keys() else 'False'
		CHON_TAT_CA_SAN_PHAM = params['CHON_TAT_CA_SAN_PHAM'] if 'CHON_TAT_CA_SAN_PHAM' in params.keys() else 'False'

		if(TU_NGAY=='False'):
			raise ValidationError('<Từ ngày> không được bỏ trống.')
		elif(DEN_NGAY=='False'):
			raise ValidationError('<Đến ngày> không được bỏ trống.')
		elif(TU_NGAY_F > DEN_NGAY_F):
			raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')

		if CHON_TAT_CA_SAN_PHAM == 'False':
				if SAN_PHAM_MANY_IDS == []:
					raise ValidationError('Bạn chưa chọn <Hàng hóa>. Xin vui lòng chọn lại.')
	@api.model
	def default_get(self, fields_list):
		result = super(BAO_CAO_S35_DN_SO_CHI_TIET_BAN_HANG, self).default_get(fields_list)
		chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
		san_phams = self.env['danh.muc.vat.tu.hang.hoa'].search([])
		if chi_nhanh:
			result['CHI_NHANH_ID'] = chi_nhanh.id
		if san_phams:
			result['SAN_PHAM_IDS'] = san_phams.ids
		return result
	### END IMPLEMENTING CODE ###

	def _action_view_report(self):
		self._validate()
		TU_NGAY_F = self.get_vntime('TU_NGAY')
		DEN_NGAY_F = self.get_vntime('DEN_NGAY')
		param = 'Từ ngày: %s đến ngày %s' % (TU_NGAY_F, DEN_NGAY_F)
		action = self.env.ref('bao_cao.open_report__s35_dn_so_chi_tiet_ban_hang').read()[0]
		# action['options'] = {'clear_breadcrumbs': True}
		action['context'] = eval(action.get('context','{}'))
		action['context'].update({'breadcrumb_ex': param})
		return action