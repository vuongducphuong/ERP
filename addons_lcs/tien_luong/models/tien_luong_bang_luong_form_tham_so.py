# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError

class TIEN_LUONG_BANG_LUONG_FORM_THAM_SO(models.Model):
	_name = 'tien.luong.bang.luong.form.tham.so'
	_description = ''
	_auto = False

	LOAI_BANG_LUONG = fields.Selection([('LUONG_CO_DINH', 'Lương cố định(không dựa trên bảng chấm công)'), ('LUONG_THOI_GIAN_THEO_BUOI', 'Lương thời gian theo buổi'), ('LUONG_THOI_GIAN_THEO_GIO', 'Lương thời gian theo giờ'), ('LUONG_TAM_UNG', 'Lương tạm ứng'), ], string='Loại bảng lương', help='Loại bảng lương',default='LUONG_CO_DINH',required=True)
	THANG = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ], string='Tháng', help='Tháng',required=True)
	NAM = fields.Integer(string='Năm', help='Năm')
	
	TEN_BANG_LUONG = fields.Char(string='Tên bảng lương', help='Tên bảng lương')
	HINH_THUC_TAO_BANG_LUONG = fields.Selection([('TAO_MOI_HOAN_TOAN', 'Tạo mới hoàn toàn'), ('DUA_TREN_BANG_LUONG_KHAC', 'Dựa trên bảng lương khác'), ], string=" ", help=" ",default='TAO_MOI_HOAN_TOAN')
	BANG_LUONG = fields.Many2one('tien.luong.bang.luong',string='Bảng lương ', help='Bảng lương')
	TU_DONG_THEM_VAO_CAC_NHAN_VIEN_MOI = fields.Boolean(string='Tự động thêm vào các nhân viên mới', help='Tự động thêm vào các nhân viên mới',default=True)
	LAY_CA_NHAN_VIEN_NGUNG_THEO_DOI = fields.Boolean(string='Lấy cả nhân viên ngừng theo dõi', help='Lấy cả nhân viên ngừng theo dõi')
	name = fields.Char(string='Name', help='Name', oldname='NAME')

	DON_VI_IDS = fields.One2many('tien.luong.bang.cham.cong.form.chi.tiet','ID_TIEN_LUONG_BANG_BANG_LUONG')

	#FIELD_IDS = fields.One2many('model.name')
	@api.model
	def default_get(self, fields_list):
		result = super(TIEN_LUONG_BANG_LUONG_FORM_THAM_SO, self).default_get(fields_list)
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

	def kiem_tra_ton_tai_bang_luong(self, args):
		thang = args.get('thang')
		nam = args.get('nam')
		id_bang_luong = 0
		if thang and nam:
			bang_luong = self.env['tien.luong.bang.luong'].search([('THANG', '=', thang),('NAM', '=', nam)],limit=1)
			if bang_luong:
				id_bang_luong = bang_luong.id
		return id_bang_luong


	@api.onchange('LOAI_BANG_LUONG','THANG','NAM')
	def update_tenBangChamCong(self):
		
		year = self.NAM
		month = self.THANG

		if self.LOAI_BANG_LUONG=='LUONG_CO_DINH':
			self.TEN_BANG_LUONG = 'Bảng lương cố định tháng ' + str(month) + ' năm ' + str(year)
		elif self.LOAI_BANG_LUONG=='LUONG_THOI_GIAN_THEO_BUOI':
			self.TEN_BANG_LUONG = 'Bảng lương thời gian theo buổi tháng ' + str(month) + ' năm ' + str(year)
		elif self.LOAI_BANG_LUONG=='LUONG_THOI_GIAN_THEO_GIO':
			self.TEN_BANG_LUONG = 'Bảng lương thời gian theo giờ tháng ' + str(month) + ' năm ' + str(year)
		else :
			self.TEN_BANG_LUONG = 'Bảng lương tạm ứng tháng ' + str(month) + ' năm ' + str(year)
	
	@api.onchange('LOAI_BANG_LUONG')
	def update_tenBangLuong(self):
		self.BANG_LUONG = False

