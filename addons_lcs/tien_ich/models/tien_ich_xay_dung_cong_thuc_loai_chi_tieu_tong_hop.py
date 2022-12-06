# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_TONG_HOP(models.Model):
    _name = 'tien.ich.xay.dung.cong.thuc.loai.chi.tieu.tong.hop'
    _description = ''

    PHEP_TINH = fields.Selection([('CONG', '+'), ('TRU', '-'), ], string='Phép tính', help='Phép tính',required=True,default='CONG')
    MA_CHI_TIEU = fields.Char(string='Mã chỉ tiêu', help='Mã chỉ tiêu')
    TEN_CHI_TIEU = fields.Char(string='Tên chỉ tiêu', help='Tên chỉ tiêu')
    CHI_TIET_ID = fields.Many2one('tien.ich.bao.cao.tai.chinh.chi.tiet', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    ID_CHI_TIEU = fields.Char(string='GUID', help='trường lưu id của master chỉ tiêu', compute='_compute_ID_CHI_TIEU', store=True, )
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    @api.depends('MA_CHI_TIEU')
    def _compute_ID_CHI_TIEU(self):
        for record in self:
            record.ID_CHI_TIEU = record.TEN_CHI_TIEU.split('_,_')[0] if record.TEN_CHI_TIEU else None
    
    # @api.model
    # def default_get(self, fields):
    #     rec = super(TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_TONG_HOP, self).default_get(fields)
    #     rec['MA_CHI_TIEU'] = self.env['tien.ich.bao.cao.tai.chinh.chi.tiet'].search([('Trường', '=', ' Giá trị')])
    #     return rec

    