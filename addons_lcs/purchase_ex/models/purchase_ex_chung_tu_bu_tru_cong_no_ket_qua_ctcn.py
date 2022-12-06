# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class PURCHASE_EX_CHUNG_TU_BU_TRU_CONG_NO_KET_QUA_CTCN(models.Model):
    _name = 'purchase.ex.chung.tu.bu.tru.cong.no.ket.qua.ctcn'
    _description = ''
    _inherit = ['mail.thread']
    LOAI_CHUNG_TU_PHAI_THU = fields.Char(string='Loại chứng từ ', help='Loại chứng từ phải thu')
    NGAY_CHUNG_TU_PHAI_THU = fields.Char(string='Ngày chứng từ ', help='Ngày chứng từ phải thu')
    SO_CHUNG_TU_PHAI_THU = fields.Char(string='Số chứng từ ', help='Số chứng từ phải thu')
    SO_HOA_DON_CT_PHAI_THU = fields.Char(string='Số hóa đơn ', help='Số hóa đơn chứng từ phải thu')
    HAN_THANH_TOAN_CT_PHAI_THU = fields.Char(string='Hạn thanh toán ', help='Hạn thanh toán chứng từ phải thu')
    SO_TIEN_CT_PHAI_THU = fields.Float(string='Số tiền ', help='Số tiền chứng từ phải thu')
    SO_CHUA_THU_CT_PHAI_THU = fields.Float(string='Số chưa thu ', help='Số chưa thu chứng từ phải thu')
    SO_BU_TRU_CT_PHAI_THU = fields.Float(string='Số bù trừ ', help='Số bù trừ chứng từ phải thu')
    LOAI_CHUNG_TU_PHAI_TRA = fields.Char(string='Loại chứng từ ', help='Loại chứng từ phải trả')
    NGAY_CHUNG_TU_PHAI_TRA = fields.Char(string='Ngày chứng từ ', help='Ngày chứng từ phải trả')
    SO_CHUNG_TU_PHAI_TRA = fields.Char(string='Số chứng từ ', help='Số chứng từ phải trả')
    SO_HOA_DON_CT_PHAI_TRA = fields.Char(string='Số hóa đơn ', help='Số hóa đơn chứng từ phải trả')
    HAN_THANH_TOAN_CT_PHAI_TRA = fields.Char(string='Hạn thanh toán ', help='Hạn thanh toán chứng từ phải trả')
    SO_TIEN_CT_PHAI_TRA = fields.Float(string='Số tiền ', help='Số tiền chứng từ phải trả')
    SO_CON_NO_CT_PHAI_TRA = fields.Float(string='Số còn nợ ', help='Số còn nợ chứng từ phải trả')
    SO_BU_TRU_CT_PHAI_TRA = fields.Float(string='Số bù trừ ', help='Số bù trừ chứng từ phải trả')
    CHUNG_TU_BU_TRU_CONG_NO_KET_QUA_ID = fields.Many2one('purchase.ex.chung.tu.bu.tru.cong.no.ket.qua', string='Chứng từ bù trừ công nợ kết quả', help='Chứng từ bù trừ công nợ kết quả', ondelete='cascade')
    name = fields.Char(string='Name', oldname='NAME')