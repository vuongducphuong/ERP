# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_DANH_SACH_KET_CHUYEN_CHI_PHI_CHI_TIET(models.Model):
    _name = 'gia.thanh.danh.sach.ket.chuyen.chi.phi.chi.tiet'
    _description = ''
    
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    KY_TINH_GIA_THANH = fields.Char(string='Kỳ tính giá thành', help='Kỳ tính giá thành')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    CHI_TIET_ID = fields.Many2one('gia.thanh.danh.sach.ket.chuyen.chi.phi', string='Chi tiết', help='Chi tiết')
    name = fields.Char(string='Name', help='Name', oldname='NAME')