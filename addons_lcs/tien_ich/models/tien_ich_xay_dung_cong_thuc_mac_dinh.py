# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_XAY_DUNG_CONG_THUC_MAC_DINH(models.Model):
    _name = 'tien.ich.xay.dung.cong.thuc.mac.dinh'

    PHEP_TINH = fields.Selection([('CONG', '+'), ('TRU', '-')], string='Phép tính', required=True, default='CONG')
    MA_CHI_TIEU = fields.Char(string='Mã chỉ tiêu', help='Mã chỉ tiêu')
    MA_CHI_TIEU_ID = fields.Many2one('tien.ich.bao.cao.tai.chinh.chi.tiet.mac.dinh', string='Mã chỉ tiêu', help='Mã chỉ tiêu')
    TEN_CHI_TIEU = fields.Char(string='Tên chỉ tiêu', help='Tên chỉ tiêu')
    MAC_DINH_ID = fields.Many2one('tien.ich.bao.cao.tai.chinh.chi.tiet.mac.dinh', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    ID_CHI_TIEU = fields.Char(string='GUID', help='trường lưu id của master chỉ tiêu', compute='_compute_ID_CHI_TIEU', store=True, )
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    @api.depends('MA_CHI_TIEU')
    def _compute_ID_CHI_TIEU(self):
        for record in self:
            record.ID_CHI_TIEU = record.TEN_CHI_TIEU.split('_,_')[0] if record.TEN_CHI_TIEU else None