# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SUPPLY_GHI_TANG_NGUON_GOC_HINH_THANH(models.Model):
    _name = 'supply.ghi.tang.nguon.goc.hinh.thanh'
    _description = ''
    _inherit = ['mail.thread']
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Char( string='TK nợ', help='Tk nợ')
    TK_CO_ID = fields.Char( string='TK có', help='Tk có')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    GHI_TANG_NGUON_GOC_HINH_THANH_ID = fields.Many2one('supply.ghi.tang', string='Ghi tăng nguồn gốc hình thành', help='Ghi tăng nguồn gốc hình thành', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')