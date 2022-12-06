# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
class STOCK_EX_LAP_RAP_THAO_DO_CHI_TIET(models.Model):
    _name = 'stock.ex.lap.rap.thao.do.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='Mã hàng')
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')
    KHO_ID = fields.Many2one('danh.muc.kho', string='Kho', help='Kho')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đơn vị tính')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits=decimal_precision.get_precision('DON_GIA'))
    THANH_TIEN = fields.Float(string='Thành tiền', help='Thành tiền',digits= decimal_precision.get_precision('VND'))
    LAP_RAP_THAO_DO_CHI_TIET_ID = fields.Many2one('stock.ex.lap.rap.thao.do', string='Lắp ráp tháo dỡ chi tiết', help='Lắp ráp tháo dỡ chi tiết', ondelete='cascade')
    sequence = fields.Integer()
    @api.onchange('MA_HANG_ID')
    def onchange_product_id(self):
        for record in self:
            record.SO_LUONG = 1
            record.TEN_HANG = record.MA_HANG_ID.TEN
            record.DVT_ID = record.MA_HANG_ID.DVT_CHINH_ID
            record.KHO_ID = record.MA_HANG_ID.KHO_NGAM_DINH_ID

    @api.onchange('MA_HANG_ID','DVT_ID')
    def onchange_dvt_id(self):
        if self.MA_HANG_ID:
            self.DON_GIA = self.MA_HANG_ID.compute_DON_GIA_BAN(self.DVT_ID.id)
