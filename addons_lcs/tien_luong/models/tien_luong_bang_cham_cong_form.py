# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError

class TIEN_LUONG_BANG_CHAM_CONG_FORM(models.Model):
	_name = 'tien.luong.bang.cham.cong.form'
	_description = ''
	_auto = False

	THANG = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ], string='Tháng', help='Tháng',required=True)
	NAM = fields.Integer(string='Năm', help='Năm')
	TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày')
	DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày')
	LOAI_CHAM_CONG = fields.Selection([('CHAM_CONG_THEO_BUOI', 'Chấm công theo buổi'), ('CHAM_CONG_THEO_GIO', 'Chấm công theo giờ'), ], string='Loại chấm công', help='Loại chấm công',default='CHAM_CONG_THEO_BUOI',required=True)
	TEN_BANG_CHAM_CONG = fields.Char(string='Tên bảng chấm công', help='Tên bảng chấm công')
	BANG_CHAM_CONG = fields.Many2one('tien.luong.bang.cham.cong.chi.tiet.master',string='Bảng chấm công', help='Bảng chấm công')
	LAY_TAT_CA_NHAN_VIEN_DA_NGUNG_THEO_DOI = fields.Boolean(string='Lấy tất cả nhân viên đã ngừng theo dõi', help='Lấy tất cả nhân viên đã ngừng theo dõi')
	HINH_THUC_TAO_CHAM_CONG = fields.Selection([('TAO_MOI', 'Tạo mới hoàn toàn'), ('LAY_DANH_SACH', 'Lấy danh sách nhân viên từ bảng chấm công khác'),  ], string=" ", help=" ",default='TAO_MOI',required=True)

	name = fields.Char(string='Name', oldname='NAME')
	tenLoaiChamCong = fields.Char(string='Tên loại bảng chấm công')

	DON_VI_IDS = fields.One2many('tien.luong.bang.cham.cong.form.chi.tiet','ID_TIEN_LUONG_BANG_CHAM_CONG')
	#FIELD_IDS = fields.One2many('model.name')

	@api.model
	def default_get(self, fields_list):
		result = super(TIEN_LUONG_BANG_CHAM_CONG_FORM, self).default_get(fields_list)
		thang = datetime.now().month
		result['THANG'] = str(thang)
		result['NAM'] = datetime.now().year
		new_line = [[5]]
		don_vis = self.env['danh.muc.to.chuc'].search([('CAP_TO_CHUC' ,'not in', ('1','2'))])
		if don_vis:
			for don_vi in don_vis:
					cap_to_chuc = don_vi.CAP_TO_CHUC
					ten_cap_to_chuc = ''
					if cap_to_chuc =='3':
						ten_cap_to_chuc = 'Văn phòng/Trung tâm'
					elif cap_to_chuc =='4':
						ten_cap_to_chuc = 'Phòng ban'
						
					new_line += [(0,0,{
					'MA_DON_VI': don_vi.MA_DON_VI,
					'TEN_DON_VI': don_vi.TEN_DON_VI,
					'CAP_TO_CHUC': ten_cap_to_chuc,
					'DON_VI_ID': don_vi.id,
					})]
			result['DON_VI_IDS'] = new_line
		return result

	@api.onchange('LOAI_CHAM_CONG','THANG','NAM')
	def update_DEN_NGAY(self):
		year = self.NAM
		month = self.THANG
		if not month:
			raise ValidationError('Tháng chấm công không được để trống.')
		if not year or year <1900:
			raise ValidationError('Năm chấm công không hợp lệ.')
		else:
			dinhDangNgay = str(year) +'-'+str(month)+'-'+'1'
			self.TU_NGAY = str(dinhDangNgay)
			self.DEN_NGAY = str(helper.Datetime.lay_ngay_cuoi_thang(year, month))
			if self.LOAI_CHAM_CONG=='CHAM_CONG_THEO_BUOI':
				self.tenLoaiChamCong = 'Bảng chấm công theo buổi'
				self.TEN_BANG_CHAM_CONG = 'Bảng chấm công theo buổi tháng ' + str(month) + ' năm ' + str(year)
			else:
				self.tenLoaiChamCong = 'Bảng chấm công theo giờ'
				self.TEN_BANG_CHAM_CONG = 'Bảng chấm công theo giờ tháng ' + str(month) + ' năm ' + str(year)

	@api.onuichange('LOAI_CHAM_CONG')
	def update_BANG_CHAM_CONG(self):
		if self.HINH_THUC_TAO_CHAM_CONG == 'LAY_DANH_SACH' and self.BANG_CHAM_CONG:
			self.BANG_CHAM_CONG = False

	def kiem_tra_ton_tai_bang_cham_cong(self, args):
		thang = args.get('thang')
		nam = args.get('nam')
		id_bang_cham_cong = 0
		if thang and nam:
			bang_cham_cong = self.env['tien.luong.bang.cham.cong.chi.tiet.master'].search([('thang', '=', thang),('nam', '=', str(nam))],limit=1)
			if bang_cham_cong:
				id_bang_cham_cong = bang_cham_cong.id
		return id_bang_cham_cong

class TIEN_LUONG_BANG_CHAM_CONG_CHI_TIET(models.Model):
	_name = 'tien.luong.bang.cham.cong.form.chi.tiet'
	_description = ''
	_auto = False
	_order = "MA_DON_VI"

	DON_VI_ID = fields.Integer()
	MA_DON_VI = fields.Char(string='Mã đơn vị')
	TEN_DON_VI = fields.Char(string='Tên đơn vị')
	CAP_TO_CHUC = fields.Char(string='Cấp tổ chức')
	AUTO_SELECT = fields.Boolean()
	ID_TIEN_LUONG_BANG_CHAM_CONG = fields.Many2one('tien.luong.bang.cham.cong.form')
	ID_TIEN_LUONG_BANG_TH_CHAM_CONG = fields.Many2one('tien.luong.tong.hop.cham.cong.tham.so')
	ID_TIEN_LUONG_BANG_BANG_LUONG = fields.Many2one('tien.luong.bang.luong.form.tham.so')

