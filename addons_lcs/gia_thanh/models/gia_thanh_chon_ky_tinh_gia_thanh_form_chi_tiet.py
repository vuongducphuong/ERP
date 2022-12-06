# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_CHON_KY_TINH_GIA_THANH_FORM_CHI_TIET(models.Model):
    _name = 'gia.thanh.chon.ky.tinh.gia.thanh.form.chi.tiet'
    _description = ''
    
    
    AUTO_SELECT = fields.Boolean()
    MA_CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Mã công trình', help='Mã công trình')
    TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình')

    SO_DON_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Số đơn hàng', help='Số đơn hàng')
    NGAY_DON_HANG = fields.Date(string='Ngày đơn hàng', help='Ngày đơn hàng')
    KHACH_HANG = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng')
    
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Số hợp đồng', help='Số hợp đồng')    
    NGAY_KY = fields.Date(string='Ngày ký', help='Ngày ký')
    TRICH_YEU = fields.Char(string='Trích yếu', help='Trích yếu')

    DOANH_THU = fields.Float(string='Doanh thu', help='Doanh thu')
    SO_CHUA_NGHIEM_THU = fields.Float(string='Số chưa nghiệm thu', help='Số chưa nghiệm thu')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CHI_TIET_ID = fields.Many2one('gia.thanh.chon.ky.tinh.gia.thanh.form', string='Chi tiết', help='Chi tiết')