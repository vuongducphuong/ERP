# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
class TONG_HOP_CHUNG_TU_NGHIEP_VU_KHAC_SO_DU_NGOAI_TE(models.Model):
    _name = 'tong.hop.chung.tu.nghiep.vu.khac.so.du.ngoai.te'
    _description = ''
    _inherit = ['mail.thread']

    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản')
    TK_NGAN_HANG_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='TK ngân hàng', help='Tk ngân hàng')
    TEN_NGAN_HANG = fields.Char(string='Tên ngân hàng', help='Tên ngân hàng',related='TK_NGAN_HANG_ID.NGAN_HANG_ID.name',store=True)
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng')

    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    SO_TIEN_DU_NO = fields.Monetary(string='Số tiền', help='Số tiền dư nợ', currency_field='currency_id')
    QUY_DOI_DU_NO = fields.Monetary(string='Quy đổi', help='Quy đổi dư nợ' , currency_field='base_currency_id')
    DANH_GIA_LAI_DU_NO = fields.Monetary(string='Đánh giá lại', help='Đánh giá lại dư nợ', currency_field='base_currency_id')
    CHENH_LECH_DU_NO = fields.Monetary(string='Chênh lệch', help='Chênh lệch dư nợ', currency_field='base_currency_id')
    SO_TIEN_DU_CO = fields.Monetary(string='Số tiền', help='Số tiền dư có', currency_field='currency_id')
    QUY_DOI_DU_CO = fields.Monetary(string='Quy đổi', help='Quy đổi dư có', currency_field='base_currency_id')
    DANH_GIA_LAI_DU_CO = fields.Monetary(string='Đánh giá lại', help='Đánh giá lại dư có', currency_field='base_currency_id')
    CHENH_LECH_DU_CO = fields.Monetary(string='Chênh lệch', help='Chênh lệch dư có', currency_field='base_currency_id')
    
    CHUNG_TU_NGHIEP_VU_KHAC_ID = fields.Many2one('account.ex.chung.tu.nghiep.vu.khac', string='Chứng từ nghiệp vụ khác', help='Chứng từ nghiệp vụ khác', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='CHUNG_TU_NGHIEP_VU_KHAC_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)

    #vu them
    MA_TAI_KHOAN = fields.Char(string='Mã tài khoản', help='Mã tài khoản', compute='_compute_tai_khoan', store=True)

    @api.depends('TAI_KHOAN_ID')
    def _compute_tai_khoan(self):
        for record in self:
            if record.TAI_KHOAN_ID:
                record.MA_TAI_KHOAN = record.TAI_KHOAN_ID.SO_TAI_KHOAN