# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_PHAN_BO_CHI_PHI_TRA_TRUOC_PHAN_BO(models.Model):
    _name = 'tong.hop.phan.bo.chi.phi.tra.truoc.phan.bo'
    _description = ''
    _inherit = ['mail.thread']
    MA_CP_TRA_TRUOC_ID = fields.Many2one('tong.hop.chi.phi.tra.truoc',string='Mã CP trả trước', help='Mã cp trả trước')
    TEN_CP_TRA_TRUOC = fields.Char(string='Tên cp trả trước', help='Tên cp trả trước',related='MA_CP_TRA_TRUOC_ID.TEN_CHI_PHI_TRA_TRUOC')
    CHI_PHI_PHAN_BO = fields.Monetary(string='Chi phí phân bổ', help='Chi phí phân bổ', currency_field='base_currency_id')
    DOI_TUONG_PHAN_BO_ID = fields.Many2one('danh.muc.to.chuc', string='Đối tượng phân bổ', help='Đối tượng phân bổ')
    TEN_DOI_TUONG_PHAN_BO = fields.Char(string='Tên đối tượng phân bổ', help='Tên đối tượng phân bổ',related='DOI_TUONG_PHAN_BO_ID.TEN_DON_VI',store=True)
    TY_LE = fields.Float(string='Tỷ lệ', help='Tỷ lệ')
    SO_TIEN = fields.Monetary(string='Số tiền', help='Số tiền',currency_field='base_currency_id')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk chi phí', help='Tk chi phí')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục cp', help='Khoản mục cp')
    PHAN_BO_CHI_PHI_TRA_TRUOC_ID = fields.Many2one('account.ex.chung.tu.nghiep.vu.khac', string='Phân bổ chi phí trả trước', help='Phân bổ chi phí trả trước', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='PHAN_BO_CHI_PHI_TRA_TRUOC_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)


    @api.onchange('TY_LE')
    def _onchange_TY_LE(self):
        self.SO_TIEN = self.TY_LE*self.CHI_PHI_PHAN_BO/100