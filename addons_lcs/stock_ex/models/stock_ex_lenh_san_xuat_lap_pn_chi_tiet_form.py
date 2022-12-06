# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class STOCK_EX_LENH_SAN_XUAT_LAP_PN_CHI_TIET_FORM(models.Model):
    _name = 'stock.ex.lenh.san.xuat.lap.pn.chi.tiet.form'
    _description = ''
    _inherit = ['mail.thread']
    AUTO_SELECT = fields.Boolean()

    CHON = fields.Boolean()
    MA_THANH_PHAM_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã thành phẩm', help='Mã thành phẩm')
    TEN_THANH_PHAM = fields.Char(string='Tên thành phẩm', help='Tên thành phẩm')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_SAN_XUAT = fields.Float(string='Số lượng sản xuất', help='Số lượng sản xuất', digits=decimal_precision.get_precision('SO_LUONG'))
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đơn vị tính')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng thcp')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    KHO_ID = fields.Many2one('danh.muc.kho', string='Kho', help='Kho')
    LENH_SAN_XUAT_ID = fields.Many2one('stock.ex.lenh.san.xuat', string='Lệnh sản xuất', help='Lệnh sản xuất')
    LAP_PN_CHI_TIET_ID = fields.Many2one('stock.ex.lenh.san.xuat.lap.pn.form', string='Lập pn chi tiết', help='Lập pn chi tiết')
    LENH_SAN_XUAT_THANH_PHAM_ID = fields.Integer(string='ID lệnh sản xuất thành phẩm', help='ID lệnh sản xuất thành phẩm')