# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
class TONG_HOP_BCTC_KIEM_TRA_BANG_KE_TOAN_KHONG_CAN_FORM(models.Model):
    _name = 'tong.hop.bctc.kiem.tra.bang.ke.toan.khong.can.form'
    _description = ''
    _auto = False

    TONG_DU_NO = fields.Float(string='Tổng dư nợ', help='Tổng dư nợ',digits= decimal_precision.get_precision('VND'))
    TONG_DU_CO = fields.Float(string='Tổng dư có', help='Tổng dư có',digits= decimal_precision.get_precision('VND'))
    CHENH_LECH = fields.Float(string='Chênh lệch', help='Chênh lệch',digits= decimal_precision.get_precision('VND'))
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(TONG_HOP_BCTC_KIEM_TRA_BANG_KE_TOAN_KHONG_CAN_FORM, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result
    TONG_HOP_BCTC_KIEM_TRA_KE_TOAN_KO_CAN_CHI_TIET_LAI_LO_FORM_IDS = fields.One2many('tong.hop.bctc.kiem.tra.ke.toan.ko.can.chi.tiet.lai.lo.form', 'BCTC_KIEM_TRA_KE_TOAN_KO_CAN_ID', string='BCTC kiểm tra kế toán ko cân chi tiết lãi lỗ form')
    TONG_HOP_BCTC_KIEM_TRA_KE_TOAN_KO_CAN_CHI_TIET_CHI_TIEU_FORM_IDS = fields.One2many('tong.hop.bctc.kiem.tra.ke.toan.ko.can.chi.tiet.chi.tieu.form', 'BCTC_KIEM_TRA_CAN_DOI_KE_TOAN_KO_CAN_ID', string='BCTC kiểm tra kế toán ko cân chi tiết chỉ tiêu form')
    TONG_HOP_BCTC_KIEM_TRA_KE_TOAN_KO_CAN_CHI_TIET_TK_FORM_IDS = fields.One2many('tong.hop.bctc.kiem.tra.ke.toan.ko.can.chi.tiet.tk.form', 'BCTC_KIEM_TRA_KE_TOAN_KO_CAN_ID', string='BCTC kiểm tra kế toán ko cân chi tiết TK form')