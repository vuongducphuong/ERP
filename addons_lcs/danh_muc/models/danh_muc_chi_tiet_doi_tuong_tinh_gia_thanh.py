# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_CHI_TIET_DOI_TUONG_TONG_HOP_CHI_PHI(models.Model):
    _name = 'danh.muc.chi.tiet.doi.tuong.tinh.gia.thanh'
    _description = ''
    _inherit = ['mail.thread']
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã thành phẩm', help='Mã Thành phẩm')
    TEN_THANH_PHAM = fields.Char(string='Tên thành phẩm', help='Tên thành phẩm')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    
    DOI_TUONG_TONG_HOP_CHI_PHI_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng tổng hợp chi phí', help='Đối tượng tổng hợp chi phí', ondelete='cascade')

    @api.onchange('MA_HANG_ID')
    def _onchange_MA_HANG_ID(self):
        if self.MA_HANG_ID:
            self.TEN_THANH_PHAM = self.MA_HANG_ID.TEN
    