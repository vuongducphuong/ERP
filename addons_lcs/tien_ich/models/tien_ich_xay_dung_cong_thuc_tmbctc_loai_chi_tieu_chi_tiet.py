# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_CHI_TIET(models.Model):
    _name = 'tien.ich.xdct.tmbctc.loai.chi.tieu.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']

    PHEP_TINH = fields.Selection([('CONG', '+'), ('TRU', '-'), ], string='Phép tính', help='Phép tính',required=True,default='CONG')
    KY_HIEU = fields.Char(string='Ký hiệu', help='Ký hiệu')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản')
    TK_DOI_UNG_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK đối ứng', help='Tài khoản đối ứng')
    CHI_TIET_ID_1 = fields.Many2one('tien.ich.thuyet.minh.bao.cao.tai.chinh.chi.tiet', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    COT = fields.Selection([('CUOI_NAM', 'Cuối năm'), ('DAU_NAM', 'Đầu năm'), ], string='Tên cột')