# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class PURCHASE_EX_LAP_TU_DON_MUA_HANG_CHI_TIET(models.Model):
    _name = 'purchase.ex.lap.tu.don.mua.hang.chi.tiet'
    _description = ''
    _auto = False

    SO_DON_HANG = fields.Char(string='Số đơn hàng', help='Số đơn hàng')
    MA_HANG = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng')
    TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng')
    SO_LUONG_CHUA_NHAN = fields.Float(string='Số lượng chưa nhận', help='Số lượng chưa nhận', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits=decimal_precision.get_precision('DON_GIA'))
    THANH_TIEN = fields.Float(string='Thành tiền', help='Thành tiền',digits=decimal_precision.get_precision('VND'))
    SO_LUONG_NHAN = fields.Float(string='Số lượng nhận', help='Số lượng nhận', digits=decimal_precision.get_precision('SO_LUONG'))
    CHI_TIET_ID = fields.Many2one('purchase.ex.lap.tu.don.mua.hang.form', string='Chi tiết', help='Chi tiết')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    NGAY_DON_HANG = fields.Date(string='Ngày đơn hàng', help='Ngày đơn hàng')
    AUTO_SELECT = fields.Boolean()
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng')
    DON_MUA_HANG_ID = fields.Many2one('purchase.ex.don.mua.hang', string='Đơn mua hàng', help='Đơn mua hàng')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đơn vị tính')
    # TK_KHO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK kho', help='Tài khoản kho')  
    # TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK nợ', help='Tài khoản nợ')
    # TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK có', help='Tài khoản có')
    # KHO_ID = fields.Many2one('danh.muc.kho', string='Kho')
    # TK_THUE_GTGT_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK thuế GTGT', help='TK thuế GTGT')
    # CHI_TIET_DON_MUA_HANG_ID = fields.Many2one('purchase.ex.don.mua.hang.chi.tiet',string='Đơn mua hàng chi tiết', help='Đơn mua hàng chi tiết')
    ID_DON_MUA_HANG_CT = fields.Integer(string='ID của đơn mua hàng chi tiết', help='ID của đơn mua hàng chi tiết')
    #FIELD_IDS = fields.One2many('model.name') 
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(PURCHASE_EX_LAP_TU_DON_MUA_HANG_CHI_TIET, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result