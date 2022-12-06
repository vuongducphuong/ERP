# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_TAI_KHOAN_KET_CHUYEN(models.Model):
    _name = 'danh.muc.tai.khoan.ket.chuyen'
    _description = ''
    _inherit = ['mail.thread']
    _order = "THU_TU_KET_CHUYEN"
    MA_KET_CHUYEN = fields.Char(string='Mã kết chuyển', help='Mã kết chuyển',required=True)# auto_num='danh_muc_tai_khoan_ket_chuyen_MA_KET_CHUYEN')
    LOAI_KET_CHUYEN = fields.Selection([('KET_CHUYEN_CHI_PHI_SAN_XUAT', 'Kết chuyển chi phí sản xuất'), ('KET_CHUYEN_XAC_DINH_KET_QUA_KINH_DOANH', 'Kết chuyển xác định kết quả kinh doanh'), ], string='Loại kết chuyển', help='Loại kết chuyển',default='KET_CHUYEN_XAC_DINH_KET_QUA_KINH_DOANH',required=True)
    KET_CHUYEN_TU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Kết chuyển từ', help='Kết chuyển từ',required=True)
    KET_CHUYEN_DEN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Kết chuyển đến', help='Kết chuyển đến',required=True)
    THU_TU_KET_CHUYEN = fields.Integer(string='Thứ tự kết chuyển', help='Thứ tự kết chuyển',required=True)
    BEN_KET_CHUYEN = fields.Selection([('NO', 'Nợ'), ('CO', 'Có'), ('HAI_BEN', 'Hai bên'), ], string='Bên kết chuyển', help='Bên kết chuyển',required=True)
    DIEN_GIAI = fields.Text(string='Diễn giải', help='Diễn giải')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    name = fields.Char(string='Name', help='Name',related='MA_KET_CHUYEN',store=True, oldname='NAME')
    MA_TAI_KHOAN_TU = fields.Char(string='Mã tài khoản kết chuyển từ', help='Mã tài khoản kết chuyển từ', compute='_compute_ket_chuyen_tu', store=True)
    MA_TAI_KHOAN_DEN = fields.Char(string='Mã tài khoản kết chuyển đến', help='Mã tài khoản kết chuyển đến', compute='_compute_ket_chuyen_den', store=True)

    _sql_constraints = [
	('MA_KET_CHUYEN_uniq', 'unique ("MA_KET_CHUYEN")', 'Mã kết chuyển <<>> đã tồn tại!'),
	]

    @api.depends('KET_CHUYEN_TU_ID')
    def _compute_ket_chuyen_tu(self):
        for record in self:
            record.MA_TAI_KHOAN_TU = record.KET_CHUYEN_TU_ID.SO_TAI_KHOAN

    @api.depends('KET_CHUYEN_DEN_ID')
    def _compute_ket_chuyen_den(self):
        for record in self:
            record.MA_TAI_KHOAN_DEN = record.KET_CHUYEN_DEN_ID.SO_TAI_KHOAN