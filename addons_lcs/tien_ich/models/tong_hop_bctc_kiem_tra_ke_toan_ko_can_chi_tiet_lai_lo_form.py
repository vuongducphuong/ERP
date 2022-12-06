# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
class TONG_HOP_BCTC_KIEM_TRA_KE_TOAN_KO_CAN_CHI_TIET_LAI_LO_FORM(models.Model):
    _name = 'tong.hop.bctc.kiem.tra.ke.toan.ko.can.chi.tiet.lai.lo.form'
    _description = ''
    _inherit = ['mail.thread']
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản')
    DU_NO_DAU_KY = fields.Float(string='Dư nợ đầu kỳ', help='Dư nợ đầu kỳ',digits= decimal_precision.get_precision('VND'))
    DU_CO_DAU_KY = fields.Float(string='Dư có đầu kỳ', help='Dư có đầu kỳ',digits= decimal_precision.get_precision('VND'))
    DU_NO_CUOI_KY = fields.Float(string='Dư nợ cuối kỳ', help='Dư nợ cuối kỳ',digits= decimal_precision.get_precision('VND'))
    DU_CO_CUOI_KY = fields.Float(string='Dư có cuối kỳ', help='Dư có cuối kỳ',digits= decimal_precision.get_precision('VND'))
    BCTC_KIEM_TRA_KE_TOAN_KO_CAN_ID = fields.Many2one('tong.hop.bctc.kiem.tra.bang.ke.toan.khong.can.form', string='Bctc kiểm tra kế toán ko cân', help='Bctc kiểm tra kế toán ko cân')
    name = fields.Char(string='Name', help='Name', oldname='NAME')