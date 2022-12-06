# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class THUE_PL_011_GTGT(models.Model):
    _name = 'thue.pl.011.gtgt'
    _description = ''
    _inherit = ['mail.thread']
    STT = fields.Char(string='STT', help='STT')
    SO_HOA_DON = fields.Char(string='Số hóa đơn ', help='Số hóa đơn ')
    NGAY_THANG_NAM_LAP_HOA_DON = fields.Char(string='Ngày, tháng, năm lập hóa đơn', help='Ngày tháng năm lập hóa đơn')
    TEN_NGUOI_MUA = fields.Char(string='Tên người mua', help='Tên người mua')
    MA_SO_THUE_NGUOI_MUA = fields.Char(string='Mã số thuế người mua', help='Mã số thuế người mua')
    GHI_CHU = fields.Char(string='Ghi chú', help='Ghi chú')
    DOANH_THU_CHUA_CO_THUE_GTGT = fields.Float(string='Doanh thu chưa có thuế GTGT', help='Doanh thu chưa có thuế giá trị gia tăng', digits=decimal_precision.get_precision('VND'))
    THUE_GTGT = fields.Float(string='Thuế GTGT', help='Thuế giá trị gia tăng', digits=decimal_precision.get_precision('VND'))
    NHOM_HHDV = fields.Selection([('1', '1. Hàng hóa, dịch vụ không chịu thuế giá trị gia tăng (GTGT)'), ('2', '2. Hàng hóa,dịch vụ chịu thuế suất thuế GTGT 0%'), ('3', '3. Hàng hóa,dịch vụ chịu thuế suất thuế GTGT 5%'), ('4', '4. Hàng hóa,dịch vụ chịu thuế suất thuế GTGT 10%'), ], string='Nhóm HHDV', help='Nhóm hàng hóa dịch vụ')
    CHI_TIET_ID = fields.Many2one('thue.thue', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')