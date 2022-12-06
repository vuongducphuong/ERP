# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ACCOUNT_EX_CHI_TIET_THEO_HOA_DON_KHACH_HANG(models.Model):
    _name = 'account.ex.chi.tiet.theo.hoa.don.khach.hang'
    _description = ''
    _inherit = ['mail.thread']
    NGAY_HOA_DON_CHUNG_TU = fields.Date(string='Ngày hóa đơn/ chứng từ', help='Ngày hóa đơn/ chứng từ')
    SO_HOA_DON_CHUNG_TU = fields.Char(string='Số hóa đơn/chứng từ', help='Số hóa đơn/chứng từ')
    HAN_HACH_TOAN = fields.Date(string='Hạn hạch toán', help='Hạn hạch toán')
    GIA_TRI_HOA_DON = fields.Float(string='Giá trị hóa đơn', help='Giá trị hóa đơn',digits=decimal_precision.get_precision('Product Price'))
    SO_CON_PHAI_TRA = fields.Float(string='Số còn phải trả', help='Số còn phải trả')
    SO_TRA_TRUOC = fields.Float(string='Số trả trước', help='Số trả trước')
    SO_THU_TRUOC = fields.Float(string='Số thu trước', help='Số thu trước',digits=decimal_precision.get_precision('Product Price'))
    SO_CON_PHAI_THU = fields.Float(string='Số còn phải thu', help='Số còn phải thu',digits=decimal_precision.get_precision('Product Price'))
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên', help='Nhân viên')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CONG_NO_THEO_KHACH_HANG_ID = fields.Many2one('account.ex.cong.no.khach.hang', string='Công nợ theo khách hàng', help='Công nợ theo khách hàng', ondelete='cascade')