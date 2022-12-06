# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET(models.Model):
    _name = 'purchase.ex.chon.chung.tu.chi.phi.chi.tiet'
    _description = ''
    
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU_ID = fields.Many2one('purchase.ex.doi.tru.chung.tu.cong.no', string='Số chứng từ', help='Số chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Nhà cung cấp', help='Nhà cung cấp')
    TONG_CHI_PHI = fields.Float(string='Tổng chi phí', help='Tổng chi phí')
    SO_PHAN_BO_LAN_NAY = fields.Float(string='Số phân bổ lần này', help='Số phân bổ lần này')
    LUY_KE_SO_DA_PHAN_BO = fields.Float(string='Lũy kế số đã phân bổ', help='Lũy kế số đã phân bổ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    AUTO_SELECT = fields.Boolean()
    CHON_CHUNG_TU_CHI_PHI_ID = fields.Many2one('purchase.ex.chon.chung.tu.chi.phi', string='Chọn chứng từ chi phí', help='Chọn chứng từ chi phí')
    ID_CHUNG_TU_GOC = fields.Integer(string='ID chứng từ gốc', help='ID chứng từ gốc')

    @api.onchange('AUTO_SELECT')
    def _update_AUTO_SELECT(self):
        self.SO_PHAN_BO_LAN_NAY = self.TONG_CHI_PHI if self.AUTO_SELECT else 0