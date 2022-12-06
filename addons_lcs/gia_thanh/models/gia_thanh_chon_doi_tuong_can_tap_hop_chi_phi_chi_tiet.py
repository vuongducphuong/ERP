# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_CHON_DOI_TUONG_CAN_TAP_HOP_CHI_PHI_CHI_TIET(models.Model):
    _name = 'gia.thanh.chon.doi.tuong.can.tap.hop.chi.phi.chi.tiet'
    _description = ''
    
    MA_SAN_PHAM_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã sản phẩm', help='Mã sản phẩm')
    TEN_SAN_PHAM = fields.Char(string='Tên sản phẩm', help='Tên sản phẩm')
    LOAI = fields.Selection([('0', 'Phân xưởng'), ('1', 'Sản phẩm'), ('2', 'Quy trình sản xuất'), ('3', 'Công đoạn'),] ,string='Loại')
    MA_CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Mã công trình', help='Mã công trình')
    TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình')
    LOAI_CONG_TRINH = fields.Many2one('danh.muc.loai.cong.trinh', string='Loại công trình', help='Loại công trình')
    SO_DON_HANG_ID = fields.Many2one('sale.ex.don.dat.hang', string='Số đơn hàng', help='Số đơn hàng')
    NGAY_DON_HANG = fields.Date(string='Ngày đơn hàng', help='Ngày đơn hàng')
    KHACH_HANG = fields.Char(string='Khách hàng', help='Khách hàng')
    SO_HOP_DONG_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Số hợp đồng', help='Số hợp đồng')
    NGAY_HOP_DONG = fields.Date(string='Ngày hợp đồng', help='Ngày hợp đồng')
    TRICH_YEU = fields.Char(string='Trích yếu', help='Trích yếu')
    AUTO_SELECT = fields.Boolean(string='Auto_select')
    CHI_TIET_ID = fields.Many2one('gia.thanh.chon.doi.tuong.can.tap.hop.chi.phi.form', string='Chi tiết')
    name = fields.Char(string='Name', oldname='NAME')