# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class SUPPLY_CHON_CHUNG_TU_GHI_GIAM_TSCD_CHI_TIET(models.Model):
    _name = 'supply.chon.chung.tu.ghi.giam.tscd.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MA_TAI_SAN_ID = fields.Many2one('asset.ghi.tang', string='Mã tài sản', help='Mã tài sản')
    TEN_TAI_SAN = fields.Char(string='Tên tài sản', help='Tên tài sản')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    GIA_TRI_CON_LAI = fields.Float(string='Giá trị còn lại', help='Giá trị còn lại',digits=decimal_precision.get_precision('VND'))
    TK_XU_LY_GIA_TRI_CON_LAI_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK xử lý giá trị còn lại', help='Tài khoản xử lý giá trị còn lại')
    CHON_CHUNG_TU_GHI_GIAM_TSCD_ID = fields.Many2one('supply.chon.chung.tu.ghi.giam.tscd', string='Chọn chứng từ ghi giảm tscd', help='Chọn chứng từ ghi giảm tscd')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')
    CHON = fields.Boolean(string='Chọn', help='Chọn', default=False)
    AUTO_SELECT = fields.Boolean()