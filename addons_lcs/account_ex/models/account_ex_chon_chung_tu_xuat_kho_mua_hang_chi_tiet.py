# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ACCOUNT_EX_CHON_CHUNG_TU_XUAT_KHO_MUA_HANG_CHI_TIET(models.Model):
    _name = 'account.ex.chon.chung.tu.xuat.kho.mua.hang.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng')
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk nợ', help='Tài nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk có', help='Tài có')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Đvt', help='Đơn vị tính')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá', digits=decimal_precision.get_precision('DON_GIA'))
    THANH_TIEN = fields.Float(string='Thành tiền', help='Thành tiền',digits=decimal_precision.get_precision('VND'))
    CHON_CHUNG_TU_XUAT_KHO_MUA_HANG_ID = fields.Many2one('account.ex.chon.chung.tu.xuat.kho.mua.hang', string='Chọn chứng từ xuất kho mua hàng', help='Chọn chứng từ xuất kho mua hàng', ondelete='cascade')

    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')
    CHON = fields.Boolean(string='Chọn', help='Chọn', default=False)
    AUTO_SELECT = fields.Boolean()