# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime

class ACCOUNT_EX_KHAI_BAO_CHI_PHI_CHUNG_CAN_PHAN_BO(models.Model):
	_name = 'account.ex.khai.bao.chi.phi.chung.can.phan.bo'
	_description = ''

	name = fields.Char(string='Name', help='Name', oldname='NAME')
	SO_TIEN = fields.Float(string='Chi phí chung', help='Chi phí chung')
	KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục chi phí', help='Khoản mục chi phí')
	TEN_KHOAN_MUC_CP = fields.Char(string='Tên khoản mục chi phí', help='Tên khoản mục chi phí')
	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
	SO_DU_BAN_DAU_ID = fields.Many2one('account.ex.nhap.so.du.ban.dau', string='Số dư ban đầu', help='Số dư ban đầu', ondelete='cascade')
	CHI_PHI_DO_DANG_MASTER_ID = fields.Many2one('account.ex.chi.phi.do.dang.master', string='Chi phí dở dang master', help='Chi phí dở dang master', ondelete='cascade')
	LA_TONG_HOP = fields.Boolean(string='Làổng hợp', store=True)
		
