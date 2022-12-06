# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class THUE_PL_BKBR_TTDB(models.Model):
    _name = 'thue.pl.bkbr.ttdb'
    _description = ''
    _inherit = ['mail.thread']
    STT = fields.Char(string='STT', help='STT')
    KY_HIEU_HOA_DON_BH = fields.Char(string='Ký hiệu', help='Ký hiệu hóa đơn bán hàng')
    SO_HOA_DON_BAN_HANG = fields.Char(string='Số', help='Số hóa đơn bán hàng')
    NGAY_THANG_NAM_PHAT_HANH = fields.Char(string='Ngày, tháng, năm phát hành', help='Ngày, tháng, năm phát hành')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    TEN_HANG_HOA_DICH_VU = fields.Char(string='Tên hàng hóa, dịch vụ', help='Tên hàng hóa, dịch vụ')
    NHOM_HANG_HOA_DICH_VU = fields.Char(string='Nhóm hàng hóa, dịch vụ', help='Nhóm hàng hóa, dịch vụ')
    SO_LUONG  = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA  = fields.Float(string='Đơn giá', help='Đơn giá', digits=decimal_precision.get_precision('DON_GIA'))
    DOANH_SO_BAN_CO_THUE  = fields.Float(string='Doanh số bán có thuế TTĐB (Không có thuế GTGT)', help='Doanh số bán có thuế TTĐB (Không có thuế GTGT)' , digits=decimal_precision.get_precision('VND'))
    
    CHI_TIET_ID = fields.Many2one('thue.thue', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')