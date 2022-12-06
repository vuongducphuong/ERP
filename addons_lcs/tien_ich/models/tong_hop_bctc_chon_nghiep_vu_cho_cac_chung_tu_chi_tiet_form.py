# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
class TONG_HOP_BCTC_CHON_NGHIEP_VU_CHO_CAC_CHUNG_TU_CHI_TIET_FORM(models.Model):
    _name = 'tong.hop.bctc.nghiep.vu.cho.ct.chi.tiet.form'
    _description = ''
    _inherit = ['mail.thread']
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Float(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK Nợ', help='Tk nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK Có', help='Tk có')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits= decimal_precision.get_precision('VND'))
    NGHIEP_VU = fields.Selection([('0', 'Nghiệp vụ thanh lý nhượng bán TSCĐ BĐSĐT'), ('1', ' Đánh giá lại tài sản góp vốn đầu tư'), ('2', ' Bán thu hồi các khoản đầu tư tài chính'), ('3', ' Lãi cho vay lãi tiền gửi cổ tức và lợi nhuận được chia lãi đầu tư định kỳ'), ('4', ' Chi phí lãi vay chi trả lãi vay '), ], string='Chọn nghiệp vụ cho các chứng từ', help='Chọn nghiệp vụ cho các chứng từ')
    BCTC_CHON_NGHIEP_VU_CHO_CAC_CHUNG_TU_ID = fields.Many2one('tong.hop.bctc.chon.nghiep.vu.cho.cac.chung.tu.form', string='Bctc chọn nghiệp vụ cho các chứng từ', help='Bctc chọn nghiệp vụ cho các chứng từ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CHI_TIET_ID = fields.Integer(string='chi tiết id', help='id của các chứng từ chi tiết')
    CHI_TIET_MODEL = fields.Char(string='model chi tiết', help='model chi tiết')
    
    