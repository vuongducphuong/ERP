# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
import json

class TONG_HOP_CHUNG_TU_GHI_SO(models.Model):
    _name = 'tong.hop.chung.tu.ghi.so'
    _description = ''
    _inherit = ['mail.thread']
    _order = "NGAY_CHUNG_TU desc, SO_CHUNG_TU desc"
    DIEN_GIAI = fields.Text(string='Diễn giải', help='Diễn giải')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',default=fields.Datetime.now)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', auto_num='tong_hop_chung_tu_ghi_so_SO_CHUNG_TU')
    name = fields.Char(string='Name', help='Name',related='SO_CHUNG_TU',store=True, oldname='NAME')

    TONG_TIEN = fields.Float(string='Số tiền', help='Số tiền',compute='tinh_tong_tien',store=True,digits= decimal_precision.get_precision('VND'))
    TONG_HOP_CHUNG_TU_GHI_SO_CHI_TIET_IDS = fields.One2many('tong.hop.chung.tu.ghi.so.chi.tiet', 'CHUNG_TU_GHI_SO_ID', string='Chứng từ ghi sổ chi tiết')
    HIEN_THI_TREN_SO = fields.Boolean(string='Hiển thị trên sổ', help='Hiển thị trên sổ')
    ID_CHUNG_TU_GOC = fields.Boolean(string='ID chứng từ gốc', help='ID chứng từ gốc')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ') 
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

    CHUNG_TU_GOC_MAU_IN = fields.Integer(string='Chứng từ gốc mẫu in', help='Chứng từ gốc mẫu in') 



    @api.model
    def default_get(self, fields):
        rec = super(TONG_HOP_CHUNG_TU_GHI_SO, self).default_get(fields)
        rec['LOAI_CHUNG_TU'] = 4040
        return rec

    @api.depends('TONG_HOP_CHUNG_TU_GHI_SO_CHI_TIET_IDS')
    def tinh_tong_tien(self):
        for order in self:
            tong_tien =0.0
            for chi_tiet in order.TONG_HOP_CHUNG_TU_GHI_SO_CHI_TIET_IDS:
                tong_tien += chi_tiet.SO_TIEN
            
            order.update({
                'TONG_TIEN':tong_tien,
            })