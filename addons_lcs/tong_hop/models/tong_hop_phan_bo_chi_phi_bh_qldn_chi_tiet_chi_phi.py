# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_PHAN_BO_CHI_PHI_BH_QLDN_CHI_TIET_CHI_PHI(models.Model):
    _name = 'tong.hop.phan.bo.chi.phi.bh.qldn.chi.tiet.chi.phi'
    _description = ''
    _inherit = ['mail.thread']
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản')
    TEN_TAI_KHOAN = fields.Char(string='Tên tài khoản', help='Tên tài khoản')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Mã khoản mục CP', help='Mã khoản mục cp', oldname='MA_KHOAN_MUC_CP_ID')
    TEN_KHOAN_MUC_CHI_PHI = fields.Char(string='Tên khoản mục CP', help='Tên khoản mục chi phí')
    TONG_CHI_PHI = fields.Monetary(string='Tổng chi phí', help='Tổng chi phí', currency_field='base_currency_id')
    TY_LE_PHAN_BO = fields.Float(string='Tỷ lệ phân bổ(%)', help='Tỷ lệ phân bổ')
    SO_TIEN_PHAN_BO = fields.Monetary(string='Số tiền phân bổ', help='Số tiền phân bổ', currency_field='base_currency_id')
    PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID = fields.Many2one('tong.hop.phan.bo.chi.phi.bh.qldn.chi.phi.khac.cho.don.vi', string='Phân bổ chi phí bh qldn chi phí khác cho đơn vị', help='Phân bổ chi phí bh qldn chi phí khác cho đơn vị', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)