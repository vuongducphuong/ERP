# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_BCTC_CHON_NV_VA_HD_LCTT_CHI_TIET_THEO_DT_FORM(models.Model):
    _name = 'tong.hop.bctc.chon.nv.va.hd.lctt.chi.tiet.theo.dt.form'
    _description = ''
    _inherit = ['mail.thread']
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản')
    MA_KHACH_HANG_ID = fields.Many2one('res.partner', string='Mã khách hàng', help='Mã khách hàng')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    DU_NO = fields.Float(string='Dư nợ', help='Dư nợ')
    DU_CO = fields.Float(string='Dư có', help='Dư có')
    HOAT_DONG = fields.Selection([('0', 'Hoạt động kinh doanh'), ('1', ' Hoạt động đầu tư'), ('2', ' Hoạt động tài chính'), ], string='Chọn hoạt động LCTT áp cho tất cả các chứng từ', help='Chọn hoạt động LCTT áp cho tất cả các chứng từ')
    BCTC_CHON_NGHIEP_VU_VA_HOAT_DONG_LCTT_ID = fields.Many2one('tong.hop.bctc.chon.nghiep.vu.va.hoat.dong.lctt.form', string='Bctc chọn nghiệp vụ và hoạt động lctt', help='Bctc chọn nghiệp vụ và hoạt động lctt')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    SO_TIEN_KINH_DOANH = fields.Float(string='Số tiền kinh doanh', help='Số tiền kinh doanh')
    SO_TIEN_DAU_TU = fields.Float(string='Số tiền đầu tư', help='Số tiền đầu tư')
    SO_TIEN_TAI_CHINH = fields.Float(string='Số tiền tài chính', help='Số tiền tài chính')
    LA_SO_DU_NO = fields.Boolean(string='Là số dư nợ', help='Là số dư nợ')