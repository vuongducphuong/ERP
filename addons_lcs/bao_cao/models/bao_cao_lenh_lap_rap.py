# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_LENH_LAP_RAP(models.Model):
	_name = 'bao.cao.lenh.lap.rap'
	_auto = False
		
	RowNumber = fields.Integer(string='RowNumber')
	ID_CHUNG_TU = fields.Integer(string='ID_CHUNG_TU')
	MODEL_CHUNG_TU = fields.Char(string='MODEL_CHUNG_TU')
	SO = fields.Char(string='SO', help='RefNo')
	NGAY = fields.Date(string='NGAY', help='RefDate')
	MA_HANG = fields.Char(string='MA_HANG', help='InventoryItemCode')
	TEN_HANG = fields.Char(string='TEN_HANG', help='InventoryItemName')
	DON_VI_TINH = fields.Char(string='DON_VI_TINH', help='UnitName')
	SO_LUONG = fields.Float(string='SO_LUONG', help='Quantity',digits=decimal_precision.get_precision('SO_LUONG'))
	DIEN_GIAI = fields.Char(string='DIEN_GIAI', help='JournalMemo')
	
	STT = fields.Integer(string='STT', help='SortOrderMaster')
	SortOrder = fields.Integer(string='SortOrder', help='SortOrder')

	ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.lenh.lap.rap.chi.tiet', 'PHIEU_THU_CHI_ID')

class BAO_CAO_LENH_LAP_RAP_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_vassembly'

	@api.model
	def get_report_values(self, docids, data=None):
		############### START SQL lấy dữ liệu ###############
		refTypeList, records = self.get_reftype_list(data)
		env = self.env['report.bao_cao.template_vdismantler']
		sql_result = env.ham_lay_du_lieu_sql_tra_ve(refTypeList)

		for line in sql_result:
			key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
			master_data = self.env['bao.cao.lenh.lap.rap'].convert_for_update(line)
			detail_data = self.env['bao.cao.lenh.lap.rap.chi.tiet'].convert_for_update(line)
		if records.get(key):
			records[key].update(master_data)
			records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.lenh.lap.rap.chi.tiet'].new(detail_data)

		docs = [records.get(k) for k in records]

		return {
			'docs': docs,
		}

	