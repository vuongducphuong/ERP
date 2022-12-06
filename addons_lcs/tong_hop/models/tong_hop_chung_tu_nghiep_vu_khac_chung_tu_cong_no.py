# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_CHUNG_TU_NGHIEP_VU_KHAC_CHUNG_TU_CONG_NO(models.Model):
    _name = 'tong.hop.chung.tu.nghiep.vu.khac.chung.tu.cong.no'
    _description = ''
    _inherit = ['mail.thread']
    LOAI_CHUNG_TU_PHAI_THU_ID = fields.Many2one('danh.muc.reftype',string='Loại chứng từ', help='Loại chứng từ phải thu')
    LOAI_CHUNG_TU_PHAI_THU_TEXT = fields.Char(string='Loại chứng từ', help='Loại chứng từ phải thu',related='LOAI_CHUNG_TU_PHAI_THU_ID.REFTYPENAME',store=True)
    
    NGAY_CHUNG_TU_PHAI_THU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ phải thu')
    SO_CHUNG_TU_PHAI_THU = fields.Char(string='Số chứng từ', help='Số chứng từ phải thu')
    SO_HOA_DON_PHAI_THU = fields.Char(string='Số hóa đơn', help='Số hóa đơn phải thu')
    HAN_THANH_TOAN_PHAI_THU = fields.Date(string='Hạn thanh toán', help='Hạn thanh toán phải thu')
    SO_TIEN_PHAI_THU = fields.Monetary(string='Số tiền', help='Số tiền phải thu', currency_field='base_currency_id')
    SO_CHUA_THU_PHAI_THU = fields.Monetary(string='Số chưa thu', help='Số chưa thu phải thu', currency_field='base_currency_id')
    SO_BU_TRU_PHAI_THU = fields.Monetary(string='Số bù trừ', help='Số bù trừ phải thu', currency_field='base_currency_id')
    
    LOAI_CHUNG_TU_PHAI_TRA_ID = fields.Many2one('danh.muc.reftype',string='Loại chứng từ', help='Loại chứng từ phải trả')
    LOAI_CHUNG_TU_PHAI_TRA_TEXT = fields.Char(string='Loại chứng từ', help='Loại chứng từ phải trả',related='LOAI_CHUNG_TU_PHAI_TRA_ID.REFTYPENAME',store=True)
    
    
    NGAY_CHUNG_TU_PHAI_TRA = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ phải trả')
    SO_CHUNG_TU_PHAI_TRA = fields.Char(string='Số chứng từ', help='Số chứng từ phải trả')
    SO_HOA_DON_PHAI_TRA = fields.Char(string='Số hóa đơn', help='Số hóa đơn phải trả')
    HAN_THANH_TOAN_PHAI_TRA = fields.Date(string='Hạn thanh toán', help='Hạn thanh toán phải trả')
    SO_TIEN_PHAI_TRA = fields.Monetary(string='Số tiền', help='Số tiền phải trả', currency_field='base_currency_id')
    SO_CHUA_THU_PHAI_TRA = fields.Monetary(string='Số còn nợ', help='Số chưa thu phải trả', currency_field='base_currency_id')
    SO_BU_TRU_PHAI_TRA = fields.Monetary(string='Số bù trừ', help='Số bù trừ phải trả', currency_field='base_currency_id')
    CHUNG_TU_NGHIEP_VU_KHAC_ID = fields.Many2one('account.ex.chung.tu.nghiep.vu.khac', string='Chứng từ nghiệp vụ khác', help='Chứng từ nghiệp vụ khác', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='CHUNG_TU_NGHIEP_VU_KHAC_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)

    # @api.depends('LOAI_CHUNG_TU_PHAI_THU','LOAI_CHUNG_TU_PHAI_TRA')
    # def set_loai_chung_tu(self):
    #         if self.LOAI_CHUNG_TU_PHAI_THU == 3530:
    #             self.LOAI_CHUNG_TU_PHAI_THU_TEXT = ''
    #         elif self.LOAI_CHUNG_TU_PHAI_TRA == 2015:
    #             self.LOAI_CHUNG_TU= self.LOAI_CHUNG_TU_2
                