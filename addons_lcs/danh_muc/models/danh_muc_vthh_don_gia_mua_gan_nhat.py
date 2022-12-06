# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class DANH_MUC_VTHH_DON_GIA_MUA_GAN_NHAT(models.Model):
    _name = 'danh.muc.vthh.don.gia.mua.gan.nhat'
    _description = ''
    _inherit = ['mail.thread']
    VAT_TU_HANG_HOA_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Vật tư hàng hóa chi tiết', help='Vật tư hàng hóa chi tiết', ondelete='cascade')
    VAT_TU_HANG_HOA_CHI_TIET = fields.Integer(string='Vật tư hàng hóa', help='Vật tư hàng hóa')
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    DON_VI_TINH_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Đơn vị tính', help='Đơn vị tính')
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits=decimal_precision.get_precision('DON_GIA'))
    THU_TU = fields.Integer(string='Thứ tự', help='Thứ tự')
    name = fields.Char(string='Name', help='Name', oldname='NAME')