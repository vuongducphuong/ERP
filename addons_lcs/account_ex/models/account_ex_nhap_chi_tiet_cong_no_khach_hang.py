# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ACCOUNT_EX_NHAP_CHI_TIET_CONG_NO_KHACH_HANG(models.Model):
    _name = 'account.ex.nhap.chi.tiet.cong.no.khach.hang'
    _description = ''
    _inherit = ['mail.thread']
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên', help='Nhân viên')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    DU_NO = fields.Float(string='Dư nợ', help='Dư nợ',digits = decimal_precision.get_precision('Product Price'))
    DU_CO = fields.Float(string='Dư có', help='Dư có',digits = decimal_precision.get_precision('Product Price'))
    CONG_NO_KHACH_HANG_ID = fields.Many2one('account.ex.cong.no.khach.hang', string='Công nợ khách hàng', help='Công nợ khách hàng', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')