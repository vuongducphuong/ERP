# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SALE_EX_HOP_DONG_BAN_CHI_TIET_DU_KIEN_CHI(models.Model):
    _name = 'sale.ex.hop.dong.ban.chi.tiet.du.kien.chi'
    _description = ''
    _inherit = ['mail.thread']
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TY_LE_PHAN_TRAM = fields.Float(string='Tỷ lệ phần trăm', help='Tỷ lệ phần trăm')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    NGAY_DU_KIEN_CHI = fields.Date(string='Ngày dự kiến chi', help='Ngày dự kiến chi')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục cp', help='Khoản mục cp')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán', ondelete='cascade')

    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)
    GTHD_QUY_DOI_DETAIL = fields.Monetary(string='GTHĐ Detail', help='Tỷ lệ phần trăm',related="HOP_DONG_BAN_ID.GTHD_QUY_DOI",store=True, currency_field='base_currency_id')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    @api.onchange('TY_LE_PHAN_TRAM')
    def update_so_tien(self):
        self.SO_TIEN = self.TY_LE_PHAN_TRAM * self.GTHD_QUY_DOI_DETAIL/100