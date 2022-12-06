# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class SALE_EX_BU_TRU_CONG_NO(models.Model):
	_inherit = 'sale.ex.bu.tru.cong.no'

	def btn_bu_tru(self):
		action = self.env.ref('tong_hop.action_open_bu_tru_cong_no_form').read()[0]

		tong_tien_bu_tru = 0
		tk_no = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '331')],limit=1).id
		tk_co = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '131')],limit=1).id
		arr_hach_toan = []
		arr_chung_tu_cong_no = []
		if self.get_context('SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS'):
			for line in self.get_context('SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS'):
					tong_tien_bu_tru += line.get('SO_TIEN_BU_TRU')

			arr_hach_toan = [(0, 0, {
				'DIEN_GIAI' : 'Bù trừ công nợ phải thu, phải trả',
				'TK_NO_ID': tk_no,
				'TK_CO_ID': tk_co,
				'SO_TIEN': tong_tien_bu_tru,
				})]
		so_tien_bu_tru = 0
		if self.get_context('SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS') and self.get_context('SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS'):
			for ct_phai_tra in self.get_context('SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS'):
				for ct_phai_thu in self.get_context('SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS'):
					if ct_phai_tra.get('AUTO_SELECT') == 'True' and ct_phai_thu.get('AUTO_SELECT') == 'True':
						if ct_phai_tra.get('SO_TIEN_BU_TRU') > ct_phai_thu.get('SO_TIEN_BU_TRU'):
								so_tien_bu_tru = ct_phai_thu.get('SO_TIEN_BU_TRU')
						elif ct_phai_tra.get('SO_TIEN_BU_TRU') == ct_phai_thu.get('SO_TIEN_BU_TRU'):
								so_tien_bu_tru = ct_phai_thu.get('SO_TIEN_BU_TRU')
						else:
								so_tien_bu_tru = ct_phai_tra.get('SO_TIEN_BU_TRU')
						arr_chung_tu_cong_no += [(0, 0, {
								'LOAI_CHUNG_TU_PHAI_THU' : ct_phai_thu.get('LOAI_CHUNG_TU'),
								'NGAY_CHUNG_TU_PHAI_THU' : ct_phai_thu.get('NGAY_CHUNG_TU'),
								'SO_CHUNG_TU_PHAI_THU': ct_phai_thu.get('SO_CHUNG_TU'),
								'SO_HOA_DON_PHAI_THU' : ct_phai_thu.get('SO_HOA_DON'),
								'HAN_THANH_TOAN_PHAI_THU' : ct_phai_thu.get('HAN_THANH_TOAN'),
								'SO_TIEN_PHAI_THU' : ct_phai_thu.get('SO_TIEN'),
								'SO_CHUA_THU' : ct_phai_thu.get('SO_CHUA_THU'),
								'SO_BU_TRU_PHAI_THU' : so_tien_bu_tru,

								'LOAI_CHUNG_TU_PHAI_TRA' : ct_phai_tra.get('LOAI_CHUNG_TU'),
								'NGAY_CHUNG_TU_PHAI_TRA' : ct_phai_tra.get('NGAY_CHUNG_TU'),
								'SO_CHUNG_TU_PHAI_TRA' : ct_phai_tra.get('SO_CHUNG_TU'),
								'SO_HOA_DON_PHAI_TRA' : ct_phai_tra.get('SO_HOA_DON'),
								'HAN_THANH_TOAN_PHAI_TRA' : ct_phai_tra.get('HAN_THANH_TOAN'),
								'SO_TIEN_PHAI_TRA' : ct_phai_tra.get('SO_TIEN'),
								'SO_CON_NO' : ct_phai_tra.get('SO_CON_NO'),
								'SO_BU_TRU_PHAI_TRA' : so_tien_bu_tru,
						})]


		ten_doi_tuong = self.env['res.partner'].search([('id', '=', self.get_context('DOI_TUONG_ID'))],limit=1).HO_VA_TEN
		context = {
		'default_DOI_TUONG_ID': self.get_context('DOI_TUONG_ID'),
		'default_LY_DO_BU_TRU': 'Bù trừ công nợ phải thu, phải trả với' +str(ten_doi_tuong),
		'default_TK_PHAI_THU': tk_no,
					'default_TK_PHAI_TRA': tk_co,
		'default_ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS' : arr_hach_toan,
					'default_ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_CT_CN_IDS' : arr_hach_toan,
		}

		action['context'] = helper.Obj.merge(context, action.get('context'))
		# action['options'] = {'clear_breadcrumbs': True}
		return action