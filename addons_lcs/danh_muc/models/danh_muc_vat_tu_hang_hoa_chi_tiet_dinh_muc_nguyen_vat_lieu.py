# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class DANH_MUC_VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NGUYEN_VAT_LIEU(models.Model):
    _name = 'danh.muc.vat.tu.hang.hoa.chi.tiet.dinh.muc.nvl'
    _description = ''
    _inherit = ['mail.thread']
    MA_NGUYEN_VAT_LIEU_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã nguyên vật liệu', help='Mã nguyên vật liệu', required=True)
    TEN_NGUYEN_VAT_LIEU = fields.Char(string='Tên nguyên vật liệu', help='Tên nguyên vật liệu')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đvt')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    VAT_TU_HANG_HOA_CHI_TIET_DINH_MUC_NVL_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Vật tư hàng hóa chi tiết định mức nguyên vật liệu', help='Vật tư hàng hóa chi tiết định mức nguyên vật liệu', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    GIA_VON = fields.Float(string='Giá vốn', help=' Đơn giá mua cố định của nguyên vật liệu',related='MA_NGUYEN_VAT_LIEU_ID.DON_GIA_MUA_CO_DINH', digits=decimal_precision.get_precision('DON_GIA')) 
    THANH_TIEN = fields.Float(string='Thành tiền', help='Thành tiền', compute='_compute_thanh_tien', store=False,digits=decimal_precision.get_precision('VND'))
    sequence = fields.Integer()


    @api.onchange('MA_NGUYEN_VAT_LIEU_ID')
    def onchange_product_id(self):
        self.TEN_NGUYEN_VAT_LIEU = self.MA_NGUYEN_VAT_LIEU_ID.TEN
        self.DVT_ID = self.MA_NGUYEN_VAT_LIEU_ID.DVT_CHINH_ID

    @api.depends('GIA_VON','SO_LUONG')
    def _compute_thanh_tien(self):
        for record in self:
            if record.GIA_VON and record.SO_LUONG:
                record.THANH_TIEN = record.GIA_VON*record.SO_LUONG