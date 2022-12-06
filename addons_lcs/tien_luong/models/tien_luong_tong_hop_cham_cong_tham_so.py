# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError


class TIEN_LUONG_TONG_HOP_CHAM_CONG_THAM_SO(models.Model):
	_name = 'tien.luong.tong.hop.cham.cong.tham.so'
	_description = ''
	_auto = False

	LOAI_CHAM_CONG = fields.Selection([('CHAM_CONG_THEO_BUOI', 'Chấm công theo buổi'), ('CHAM_CONG_THEO_GIO', 'Chấm công theo giờ'), ], string='Loại chấm công', help='Loại chấm công',default='CHAM_CONG_THEO_BUOI',required=True)
	THANG = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ], string='Tháng', help='Tháng',required=True)
	NAM = fields.Integer(string='Năm', help='Năm')
	TEN_BANG_TONG_HOP_CHAM_CONG = fields.Char(string='Tên bảng tổng hợp chấm công', help='Tên bảng tổng hợp chấm công')
	TONG_HOP_TU_CAC_BANG_CHAM_CONG_CHI_TIET = fields.Boolean(string='Tổng hợp từ các bảng chấm công chi tiết', help='Tổng hợp từ các bảng chấm công chi tiết')
	name = fields.Char(string='Name', help='Name', oldname='NAME')
	tenLoaiChamCong = fields.Char(string='Tên loại bảng chấm công')

	DON_VI_IDS = fields.One2many('tien.luong.bang.cham.cong.form.chi.tiet','ID_TIEN_LUONG_BANG_TH_CHAM_CONG')

	@api.model
	def default_get(self, fields_list):
		result = super(TIEN_LUONG_TONG_HOP_CHAM_CONG_THAM_SO, self).default_get(fields_list)
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
		result['tenLoaiChamCong'] = 'Tổng hợp chấm công theo buổi'
		return result

	def kiem_tra_ton_tai_bang_tong_hop_cham_cong(self, args):
		thang = args.get('thang')
		nam = args.get('nam')
		id_bang_tong_hop_cham_cong = 0
		if thang and nam:
			bang_tong_hop_cham_cong = self.env['tien.luong.bang.tong.hop.cham.cong'].search([('THANG', '=', thang),('NAM', '=', str(nam))],limit=1)
			if bang_tong_hop_cham_cong:
				id_bang_tong_hop_cham_cong = bang_tong_hop_cham_cong.id
		return id_bang_tong_hop_cham_cong

	@api.onchange('LOAI_CHAM_CONG','THANG','NAM')
	def update_tenBangChamCong(self):
		
		year = self.NAM
		month = self.THANG
		
		if self.LOAI_CHAM_CONG=='CHAM_CONG_THEO_BUOI':
			self.tenLoaiChamCong = 'Tổng hợp chấm công theo buổi'
			self.TEN_BANG_TONG_HOP_CHAM_CONG = 'Bảng tổng hợp chấm công theo buổi tháng ' + str(month) + ' năm ' + str(year)
		else:
			self.tenLoaiChamCong = 'Tổng hợp chấm công theo giờ'
			self.TEN_BANG_TONG_HOP_CHAM_CONG = 'Bảng tổng hợp chấm công theo giờ tháng ' + str(month) + ' năm ' + str(year)
	