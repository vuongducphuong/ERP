# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_TONG_HOP_MAC_DINH(models.Model):
    _name = 'tien.ich.xdct.tmbctc.tong.hop.mac.dinh'

    PHEP_TINH = fields.Selection([('CONG', '+'), ('TRU', '-')], string='Phép tính', required=True, default='CONG')
    MA_CHI_TIEU = fields.Char(string='Mã chỉ tiêu', help='Mã chỉ tiêu')
    MA_CHI_TIEU_ID = fields.Many2one('tien.ich.bao.cao.tai.chinh.chi.tiet.mac.dinh', string='Mã chỉ tiêu', help='Mã chỉ tiêu')
    TEN_CHI_TIEU = fields.Char(string='Tên chỉ tiêu', help='Tên chỉ tiêu')
    MAC_DINH_ID_1 = fields.Many2one('tien.ich.thuyet.minh.bao.cao.tai.chinh.chi.tiet.mac.dinh', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')