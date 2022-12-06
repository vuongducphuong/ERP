# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class TONG_HOP_CHI_PHI_TRA_TRUOC_TAP_HOP_CHUNG_TU(models.Model):
    _name = 'tong.hop.chi.phi.tra.truoc.tap.hop.chung.tu'
    _description = ''
    _inherit = ['mail.thread']
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk nợ', help='Tk nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk có', help='Tk có')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('Product Price'))
    CHI_PHI_TRA_TRUOC_ID = fields.Many2one('tong.hop.chi.phi.tra.truoc', string='Chi phí trả trước', help='Chi phí trả trước', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')