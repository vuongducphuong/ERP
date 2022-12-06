# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_MENH_GIA_LOAI_TIEN(models.Model):
    _name = 'danh.muc.menh.gia.loai.tien'
    _description = ''
    _inherit = ['mail.thread']
    STT = fields.Char(string='STT', help='Số thứ tự', auto_num='danh_muc_menh_gia_loai_tien_STT')
    MENH_GIA = fields.Float(string='Mệnh giá', help='Mệnh giá')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')