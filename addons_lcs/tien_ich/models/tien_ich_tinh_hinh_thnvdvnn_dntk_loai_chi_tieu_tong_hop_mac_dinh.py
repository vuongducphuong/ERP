# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_TONG_HOP_MAC_DINH(models.Model):
    _name = 'tien.ich.ththnvdvnndntk.lct.tong.hop.mac.dinh'
    _description = ''
    _inherit = ['mail.thread']
    PHEP_TINH = fields.Selection([('CONG', '+'), ('TRU', '-'), ], string='Phép tính', help='Phép tính',required=True,default='CONG')
    MA_CHI_TIEU = fields.Char(string='Mã chỉ tiêu', help='Mã chỉ tiêu')
    TEN_CHI_TIEU = fields.Char(string='Tên chỉ tiêu', help='Tên chỉ tiêu')
    CHI_TIET_ID = fields.Many2one('tien.ich.thuc.hien.nghia.vu.doi.voi.nha.nuoc.mac.dinh', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')