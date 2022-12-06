# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class PURCHASE_EX_DOI_TRU_CHUNG_TU_CONG_NO(models.Model):
    _name = 'purchase.ex.doi.tru.chung.tu.cong.no'
    _description = ''
    _auto = False

    CHON = fields.Boolean(string='Chọn', help='Chọn')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    HAN_THANH_TOAN = fields.Date(string='Hạn thanh toán', help='Hạn thanh toán')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Mã nhân viên', help='Mã nhân viên')
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='Tên nhân viên')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('Product Price'))
    SO_CON_NO = fields.Float(string='Số còn nợ', help='Số còn nợ',digits=decimal_precision.get_precision('Product Price'))
    SO_TIEN_DOI_TRU = fields.Float(string='Số tiền đối trừ', help='Số tiền đối trừ',digits=decimal_precision.get_precision('Product Price'))
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    DOI_TRU_CHUNG_TU_ID = fields.Many2one('purchase.ex.doi.tru.chung.tu', string='Đối trừ chứng từ', help='Đối trừ chứng từ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    SO_TIEN_QUY_DOI = fields.Float(string='Số tiền quy đổi', help='Số tiền quy đổi')
    TY_GIA_DANH_GIA_LAI = fields.Float(string='Tỷ giá đánh giá lại', help='Tỷ giá đánh giá lại')
    SO_CON_NO_QUY_DOI = fields.Float(string='Số còn nợ quy đổi', help='Số còn nợ quy đổi')
    SO_TIEN_DOI_TRU_QUY_DOI = fields.Float(string='Số tiền đối trừ quy đổi', help='Số tiền đối trừ quy đổi')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(PURCHASE_EX_DOI_TRU_CHUNG_TU_CONG_NO, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result

    # def action_view_result(self):
    #     action = self.env.ref('purchase_ex.action_open_purchase_ex_doi_tru_chung_tu_cong_no_form').read()[0]
    #     # action['options'] = {'clear_breadcrumbs': True}
    #     return action

    # @api.onchange('CHON')
    # def update_CHON(self):
    #     if self.SO_TIEN_DOI_TRU == 0:
    #         if self.CHON == True:
    #             self.SO_TIEN_DOI_TRU = self.SO_CON_NO
    #     if self.SO_TIEN_DOI_TRU != 0:
    #         if self.CHON == False:
    #             self.SO_TIEN_DOI_TRU = 0