# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_VAT_TU_HANG_HOA_DAC_TINH_HINH_ANH(models.Model):
    _name = 'danh.muc.vat.tu.hang.hoa.dac.tinh.hinh.anh'
    _description = ''
    _inherit = ['mail.thread']
    DAC_TINH = fields.Char(string='Đặc tính', help='Đặc tính')
    VAT_TU_HANG_HOA_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Vật tư hàng hóa', help='Vật tư hàng hóa', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    image = fields.Binary("Image", attachment=True,
       help="Chọn logo",)