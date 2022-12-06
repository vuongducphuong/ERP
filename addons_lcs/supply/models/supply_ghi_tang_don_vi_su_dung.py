# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class SUPPLY_GHI_TANG_DON_VI_SU_DUNG(models.Model):
    _name = 'supply.ghi.tang.don.vi.su.dung'
    _description = ''
    _inherit = ['mail.thread']
    MA_DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Mã đơn vị', help='Mã đơn vị', required=True)
    TEN_DON_VI = fields.Char(string='Tên đơn vị', help='Tên đơn vị',related='MA_DON_VI_ID.TEN_DON_VI',store=True)
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'), default=1)
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    GHI_TANG_DON_VI_SU_DUNG_ID = fields.Many2one('supply.ghi.tang', string='Ghi tăng đơn vị sử dụng', help='ghi tăng đơn vị sử dụng', ondelete='cascade')
    # GHI_TANG_CCDC_HANG_LOAT_ID = fields.Many2one('supply.ghi.tang.hang.loat', string='Ghi tăng ccdc hàng loạt', help='Ghi tăng ccdc hàng loạt')
    GHI_TANG_HANG_LOAT_CHI_TIET_ID = fields.Many2one('supply.ghi.tang.hang.loat.chi.tiet', string='Ghi tăng hàng loạt chi tiết', help='Ghi tăng hàng loạt chi tiết', ondelete='set null')
    sequence = fields.Integer()
    