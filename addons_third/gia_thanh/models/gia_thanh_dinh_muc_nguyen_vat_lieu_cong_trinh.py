# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_DINH_MUC_NGUYEN_VAT_LIEU_CONG_TRINH(models.Model):
    _name = 'gia.thanh.dinh.muc.nguyen.vat.lieu.cong.trinh'
    _description = ''
    _inherit = ['mail.thread']
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình', related='CONG_TRINH_ID.TEN_CONG_TRINH')
    TU_NGAY = fields.Date(string='Áp dụng từ ngày (*)', help='Áp dụng từ ngày')
    DEN_NGAY = fields.Date(string='Đến ngày (*)', help='Đến ngày')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    ACTIVE = fields.Boolean(string='Active', help='Ngừng theo dõi')
    name = fields.Char(string='Name', help='Name' , related='CONG_TRINH_ID.MA_CONG_TRINH', oldname='NAME')

    GIA_THANH_DINH_MUC_NGUYEN_VAT_LIEU_CONG_TRINH_CHI_TIET_IDS = fields.One2many('gia.thanh.dinh.muc.nguyen.vat.lieu.cong.trinh.chi.tiet', 'CHI_TIET_ID', string='Định mức nguyên vật liệu công trình chi tiết')