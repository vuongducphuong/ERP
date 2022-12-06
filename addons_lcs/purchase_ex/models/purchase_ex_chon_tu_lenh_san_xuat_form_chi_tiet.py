# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class PURCHASE_EX_CHON_TU_LENH_SAN_XUAT_FORM_CHI_TIET(models.Model):
    _name = 'purchase.ex.chon.tu.lenh.san.xuat.form.chi.tiet'
    _description = ''
    _auto = False

    SO = fields.Char(string='Số', help='Số')
    NGAY = fields.Date(string='Ngày', help='Ngày')
    DA_LAP_DU_PX = fields.Boolean(string='Đã lập đủ PX', help='Đã lập đủ phiếu xuất')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    MA_THANH_PHAM_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã thành phẩm', help='Mã thành phẩm')
    TEN_THANH_PHAM = fields.Char(string='Tên thành phẩm', help='Tên thành phẩm')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    SO_LUONG_SAN_XUAT = fields.Float(string='Số lượng sản xuất', help='Số lượng sản xuất', digits=decimal_precision.get_precision('SO_LUONG'))
    CHI_TIET_ID = fields.Many2one('purchase.ex.chon.tu.lenh.san.xuat.form', string='Chi tiết', help='Chi tiết')
    
    ID_THANH_PHAM = fields.Integer(string='id thành phẩm')
    AUTO_SELECT = fields.Boolean()

    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(PURCHASE_EX_CHON_TU_LENH_SAN_XUAT_FORM_CHI_TIET, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result