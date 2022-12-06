# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
class TONG_HOP_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE_SO_DU_NGOAI_TE(models.Model):
    _name = 'tong.hop.danh.gia.lai.tai.khoan.ngoai.te.so.du.ngoai.te'
    _description = ''
    _inherit = ['mail.thread']

    AUTO_SELECT = fields.Boolean()
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản')
    TK_NGAN_HANG_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='TK ngân hàng', help='Tk ngân hàng')
    TEN_NGAN_HANG = fields.Char(string='Tên ngân hàng', help='Tên ngân hàng')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    SO_TIEN_DU_NO = fields.Monetary(string='Số tiền', help='Số tiền dư nợ',currency_field='currency_id')
    QUY_DOI_DU_NO = fields.Monetary(string='Quy đổi', help='Quy đổi dư nợ' , currency_field='base_currency_id')
    DANH_GIA_LAI_DU_NO = fields.Monetary(string='Đánh giá lại', help='Đánh giá lại dư nợ', currency_field='base_currency_id')
    CHENH_LECH_DU_NO = fields.Monetary(string='Chênh lệch', help='Chênh lệch dư nợ', currency_field='base_currency_id')
    SO_TIEN_DU_CO = fields.Monetary(string='Số tiền', help='Số tiền dư có',currency_field='currency_id')
    QUY_DOI_DU_CO = fields.Monetary(string='Quy đổi', help='Quy đổi dư có', currency_field='base_currency_id')
    DANH_GIA_LAI_DU_CO = fields.Monetary(string='Đánh giá lại', help='Đánh giá lại dư có', currency_field='base_currency_id')
    CHENH_LECH_DU_CO = fields.Monetary(string='Chênh lệch', help='Chênh lệch dư có', currency_field='base_currency_id')
    DANH_GIA_LAI_TAI_KHOAN_NGUYEN_TE_ID = fields.Many2one('tong.hop.danh.gia.lai.tai.khoan.ngoai.te', string='Đánh giá lại tài khoản nguyên tệ', help='Đánh giá lại tài khoản nguyên tệ')
    name = fields.Char(string='Name', oldname='NAME')

    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='DANH_GIA_LAI_TAI_KHOAN_NGUYEN_TE_ID.DANH_GIA_NGOAI_TE_ID', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)

    LOAI_TIEN = fields.Integer(string='Tên nhãn', help='Tên nhãn',related='DANH_GIA_LAI_TAI_KHOAN_NGUYEN_TE_ID.DANH_GIA_NGOAI_TE_ID.id')

    @api.onchange('TY_GIA')
    def _onchange_TY_GIA(self):
        if (self.TY_GIA):
            danh_gia_lai_du_no= self.TY_GIA * self.SO_TIEN_DU_NO
            danh_gia_lai_du_co= self.TY_GIA * self.SO_TIEN_DU_CO
            self.DANH_GIA_LAI_DU_NO = danh_gia_lai_du_no
            self.CHENH_LECH_DU_NO = self.QUY_DOI_DU_NO - danh_gia_lai_du_no
            self.DANH_GIA_LAI_DU_CO = danh_gia_lai_du_co
            self.CHENH_LECH_DU_CO = self.QUY_DOI_DU_CO - danh_gia_lai_du_co