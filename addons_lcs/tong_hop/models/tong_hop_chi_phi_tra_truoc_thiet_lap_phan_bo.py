# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_CHI_PHI_TRA_TRUOC_THIET_LAP_PHAN_BO(models.Model):
    _name = 'tong.hop.chi.phi.tra.truoc.thiet.lap.phan.bo'
    _description = ''
    _inherit = ['mail.thread']
    DOI_TUONG_PHAN_BO_ID = fields.Many2one('danh.muc.to.chuc', string='Đối tượng phân bổ', help='Đối tượng phân bổ')
    TEN_DOI_TUONG_PHAN_BO = fields.Char(string='Tên đối tượng phân bổ', help='Tên đối tượng phân bổ')
    TY_LE_PB = fields.Float(string='Tỷ lệ PB(%)', help='Tỷ lệ pb')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chi phí', help='Tk chi phí')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục CP', help='Khoản mục cp')
    CHI_PHI_TRA_TRUOC_ID = fields.Many2one('tong.hop.chi.phi.tra.truoc', string='Chi phí trả trước', help='Chi phí trả trước', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    @api.onchange('DOI_TUONG_PHAN_BO_ID')
    def _onchange_DOI_TUONG_PHAN_BO_ID(self):
        self.TEN_DOI_TUONG_PHAN_BO = self.DOI_TUONG_PHAN_BO_ID.TEN_DON_VI