# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class SALE_DOCUMENT(models.Model):
    _inherit = 'sale.document'

    XAC_NHAN_DU_SO_LUONG = fields.Boolean('Xác nhận xuất đủ số lượng hàng hóa')
    
    @api.onchange('XAC_NHAN_DU_SO_LUONG')
    def _onchange_XAC_NHAN_DU_SO_LUONG(self):
        for line in self.SALE_DOCUMENT_LINE_IDS:
            line.SO_LUONG = line.SO_LUONG_YEU_CAU if self.XAC_NHAN_DU_SO_LUONG else 0

    @api.multi
    def action_ghi_so(self):
        for record in self:
            can_be_posted = True
            for line in self.SALE_DOCUMENT_LINE_IDS:
                if line.SO_LUONG == 0 or line.SO_LUONG != line.SO_LUONG_YEU_CAU:
                    can_be_posted = False
                    break
            if can_be_posted:
                return super(SALE_DOCUMENT, record).action_ghi_so()