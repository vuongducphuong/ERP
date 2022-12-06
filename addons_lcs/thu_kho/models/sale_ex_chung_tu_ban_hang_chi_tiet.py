# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class SALE_DOCUMENT_LINE(models.Model):
    _inherit = 'sale.document.line'

    # THU_KHO_GHI_CHU đồng thời cũng là trường để xác định có đang sử dụng phân hệ thủ kho
    # hay không? Nếu có thì có các chứng từ phải lấy theo SO_LUONG_YEU_CAU
    THU_KHO_GHI_CHU = fields.Char('Ghi chú', oldname='GHI_CHU')

    # @api.onchange('DON_GIA','SO_LUONG_YEU_CAU')
    # def update_thanh_tien_theo_sl_yeu_cau(self):
    #     self.THANH_TIEN = self.DON_GIA*self.SO_LUONG_YEU_CAU
    
    # @api.onchange('SO_LUONG_YEU_CAU','DON_GIA_VON')
    # def update_Tien_von_theo_sl_yeu_cau(self):
    #     self.TIEN_VON = self.SO_LUONG_YEU_CAU*self.DON_GIA_VON