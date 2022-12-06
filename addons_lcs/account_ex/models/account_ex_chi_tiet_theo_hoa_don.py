# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ACCOUNT_EX_CHI_TIET_THEO_HOA_DON(models.Model):
    _name = 'account.ex.chi.tiet.theo.hoa.don'
    _description = ''
    _inherit = ['mail.thread']
    NGAY_HOA_DON_CHUNG_TU = fields.Date(string='Ngày hóa đơn/ chứng từ', help='Ngày hóa đơn/ chứng từ')
    SO_HOA_DON_CHUNG_TU = fields.Char(string='Số hóa đơn/chứng từ', help='Số hóa đơn/chứng từ',digits=decimal_precision.get_precision('Product Price'))
    HAN_HACH_TOAN = fields.Date(string='Hạn hạch toán', help='Hạn hạch toán')
    GIA_TRI_HOA_DON = fields.Float(string='Giá trị hóa đơn', help='Giá trị hóa đơn',digits=decimal_precision.get_precision('Product Price'))
    SO_CON_PHAI_TRA = fields.Float(string='Số còn phải trả', help='Số còn phải trả',digits=decimal_precision.get_precision('Product Price'))
    SO_TRA_TRUOC = fields.Float(string='Số trả trước', help='Số trả trước',digits=decimal_precision.get_precision('Product Price'))
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên', help='Nhân viên')
    CONG_NO_NHA_CUNG_CAP_ID = fields.Many2one('account.ex.cong.no.nha.cung.cap', string='Công nợ nhà cung cấp', help='Công nợ nhà cung cấp', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')