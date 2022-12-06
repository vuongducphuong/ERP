# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class TONG_HOP_PHAN_BO_CHI_PHI_TRA_TRUOC_XD_CHI_PHI(models.Model):
    _name = 'tong.hop.phan.bo.chi.phi.tra.truoc.xd.chi.phi'
    _description = ''
    _inherit = ['mail.thread']
    MA_CP_TRA_TRUOC_ID = fields.Many2one('tong.hop.chi.phi.tra.truoc',string='Mã CP trả trước', help='Mã cp trả trước')
    TEN_CP_TRA_TRUOC = fields.Char(string='Tên cp trả trước', help='Tên CP trả trước',related='MA_CP_TRA_TRUOC_ID.TEN_CHI_PHI_TRA_TRUOC')
    SO_TIEN = fields.Monetary(string='Số tiền', help='Số tiền', currency_field='base_currency_id')
    SO_TIEN_CHUA_PHAN_BO = fields.Monetary(string='Số tiền chưa phân bổ', help='Số tiền chưa phân bổ', currency_field='base_currency_id')
    SO_TIEN_PHAN_BO_TRONG_KY = fields.Monetary(string='Số tiền phân bổ trong kỳ', help='Số tiền phân bổ trong kỳ', currency_field='base_currency_id')
   
    PHAN_BO_CHI_PHI_TRA_TRUOC_ID = fields.Many2one('account.ex.chung.tu.nghiep.vu.khac', string='Phân bổ chi phí trả trước', help='Phân bổ chi phí trả trước', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)