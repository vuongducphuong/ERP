# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round

class PURCHASE_DOCUMENT_LINE(models.Model):
    _inherit = 'purchase.document.line'

    # THU_KHO_GHI_CHU đồng thời cũng là trường để xác định có đang sử dụng phân hệ thủ kho
    # hay không? Nếu có thì có các chứng từ phải lấy theo SO_LUONG_YEU_CAU
    THU_KHO_GHI_CHU = fields.Char('Ghi chú', oldname='GHI_CHU')
    
    # @api.onchange('SO_LUONG_YEU_CAU', 'DON_GIA', 'TY_LE_CK', 'CHI_PHI_MUA_HANG', 'PHI_TRUOC_HAI_QUAN','CHI_PHI_MUA_HANG','currency_id')
    # def _compute_amount(self):
    #     self.THANH_TIEN = self.SO_LUONG_YEU_CAU*self.DON_GIA
    #     self.THANH_TIEN_QUY_DOI = float_round(self.THANH_TIEN*self.TY_GIA, 0)
    #     self.TIEN_CHIET_KHAU = (self.DON_GIA*self.SO_LUONG_YEU_CAU*self.TY_LE_CK)/100
    #     self.lay_gia_tri_nhap_kho()
    #     self.lay_gia_tri_tinh_thue_nk()