# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_BCTC_CHON_NV_VA_HD_LCTT_CHI_TIET_KO_THEO_DT_FORM(models.Model):
    _name = 'tong.hop.bctc.chon.nv.va.hd.lctt.chi.tiet.ko.theo.dt.form'
    _description = ''
    _inherit = ['mail.thread']
    MA_TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Mã tài khoản', help='Mã tài khoản')
    TEN_TAI_KHOAN = fields.Char(string='Tên tài khoản', help='Tên tài khoản')
    DU_NO = fields.Float(string='Dư nợ', help='Dư nợ')
    DU_CO = fields.Float(string='Dư có', help='Dư có')
    KINH_DOANH = fields.Float(string='Kinh doanh', help='Kinh doanh')
    BCTC_CHON_NGHIEP_VU_VA_HOAT_DONG_LCTT_ID = fields.Many2one('tong.hop.bctc.chon.nghiep.vu.va.hoat.dong.lctt.form', string='Bctc chọn nghiệp vụ và hoạt động lctt', help='Bctc chọn nghiệp vụ và hoạt động lctt')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    DAU_TU = fields.Float(string='Đầu tư', help='Đầu tư')
    TAI_CHINH = fields.Float(string='Tài chính', help='Tài chính')