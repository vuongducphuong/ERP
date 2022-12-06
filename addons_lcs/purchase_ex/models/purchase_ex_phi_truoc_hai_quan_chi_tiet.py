# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime
from odoo import api, fields, models, _, helper
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_round

class PurchasePhiTruocHaiQuan(models.Model):
    _name = "purchase.phi.truoc.hai.quan"
    _description = "Phí trước hải quan"
    _order = 'sequence'

    purchase_document_id = fields.Many2one('purchase.document', string='Chứng từ mua hàng', ondelete='cascade')
    sequence = fields.Integer()
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    # CHUNG_TU_ID = fields.Many2one('purchase.document', string='Số chứng từ')
    NGAY_HACH_TOAN = fields.Date('Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date('Ngày chứng từ')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Nhà cung cấp')
    TONG_CHI_PHI = fields.Monetary(string='Tổng chi phí', currency_field='base_currency_id')
    SO_PHAN_BO_LAN_NAY = fields.Monetary(string='Số phân bổ lần này', currency_field='base_currency_id')
    SO_PHAN_BO_LAN_NAY_QUY_DOI = fields.Monetary(string='Số phân bổ lần này quy đổi', currency_field='base_currency_id')
    LUY_KE_DA_PHAN_BO = fields.Monetary(string='Lũy kế đã phân bổ', currency_field='base_currency_id')
    ID_CHUNG_TU_GOC = fields.Integer(string='ID chứng từ gốc', help='ID chứng từ gốc')

    
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)