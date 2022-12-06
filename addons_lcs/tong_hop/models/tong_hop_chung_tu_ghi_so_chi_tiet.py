# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
class TONG_HOP_CHUNG_TU_GHI_SO_CHI_TIET(models.Model):
    _name = 'tong.hop.chung.tu.ghi.so.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK nợ', help='Tk nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK có', help='Tk có')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits= decimal_precision.get_precision('VND'))
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    CHUNG_TU_GHI_SO_ID = fields.Many2one('tong.hop.chung.tu.ghi.so', string='Chứng từ ghi sổ', help='Chứng từ ghi sổ', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    MA_TK_NO = fields.Char(string='Mã tài khoản nợ', help='Mã tài khoản nợ',related='TK_NO_ID.SO_TAI_KHOAN')
    MA_TK_CO = fields.Char(string='Mã tài khoản có', help='Mã tài khoản có',related='TK_CO_ID.SO_TAI_KHOAN')
    ID_CHUNG_TU_GOC = fields.Integer(string='ID chứng từ gốc', help='ID chứng từ gốc')
    MODEL_GOC = fields.Char(string='MODEL gốc', help='MODEL gốc')
    STT = fields.Integer(string='Số thứ tự dòng', help='Số thứ tự dòng')
    GHI_CHU = fields.Char(string='Ghi chú', help='Ghi chú')
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())