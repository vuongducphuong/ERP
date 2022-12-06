# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU(models.Model):
    _name = 'sale.ex.bu.tru.cong.no.chung.tu.phai.thu'
    _description = ''
    _auto = False

    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
    SO_CHUNG_TU = fields.Char(string='Số chừng từ', help='Số chừng từ')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    HAN_THANH_TOAN = fields.Date(string='Hạn thanh toán', help='Hạn thanh toán')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('Product Price'))
    SO_CHUA_THU = fields.Float(string='Số chưa thu', help='Số chưa thu',digits=decimal_precision.get_precision('Product Price'))
    SO_TIEN_BU_TRU = fields.Float(string='Số tiền bù trừ', help='Số tiền bù trừ',digits=decimal_precision.get_precision('Product Price'))
    TEN_LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')
    BU_TRU_CONG_NO_ID = fields.Many2one('sale.ex.bu.tru.cong.no', string='Bù trừ công nợ', help='Bù trừ công nợ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    # CHON = fields.Boolean(string='Chọn', help='Chọn')
    AUTO_SELECT = fields.Boolean()
    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')


    SO_TIEN_QUY_DOI = fields.Float(string='Số tiền quy đổi', help='Số tiền quy đổi',digits=decimal_precision.get_precision('Product Price'))
    TY_GIA_DANH_GIA_LAI = fields.Float(string='Tỷ giá đánh giá lại', help='Tỷ giá đánh giá lại')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    SO_CHUA_THU_QUY_DOI = fields.Float(string='Số chưa thu quy đổi', help='Số chưa thu quy đổi',digits=decimal_precision.get_precision('Product Price'))
    SO_TIEN_BU_TRU_QUY_DOI = fields.Float(string='Số tiền bù trừ quy đổi', help='Số tiền bù trừ quy đổi',digits=decimal_precision.get_precision('Product Price'))
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result
    
    # Remove vì đã thực hiện onchange ở client, và tăng tốc khi change selection
    # @api.onchange('SO_TIEN_BU_TRU')
    # def _onchange_SO_TIEN_BU_TRU(self):
    #     if self.SO_TIEN_BU_TRU:
    #         self.SO_TIEN_BU_TRU_QUY_DOI = self.SO_TIEN_BU_TRU*self.TY_GIA_DANH_GIA_LAI

    def action_view_result(self):
        action = self.env.ref('sale_ex.action_open_sale_ex_bu_tru_cong_no_chung_tu_phai_thu_form').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        return action