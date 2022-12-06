# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class TIEN_LUONG_HACH_TOAN_CHI_PHI_LUONG_CHI_TIET(models.Model):
    _name = 'tien.luong.hach.toan.chi.phi.luong.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK nợ', help='Tài khoản nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK có', help='Tài khoản có')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits= decimal_precision.get_precision('VND'))
    DOI_TUONG_NO_ID = fields.Many2one('res.partner', string='Đối tượng Nợ', help='Đối tượng nợ')
    TEN_DOI_TUONG_NO = fields.Char(string='Tên đối tượng Nợ', help='Tên đối tượng nợ')
    DOI_TUONG_CO_ID = fields.Many2one('res.partner', string='Đối tượng Có', help='Đối tượng có')
    TEN_DOI_TUONG_CO = fields.Char(string='Tên đối tượng Có', help='Tên đối tượng có')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục CP ', help='Khoản mục chi phí ')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng tập hợp chi phí')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban',string='Hợp đồng bán', help='Hợp đồng bán')
    CP_KHONG_HOP_LY = fields.Boolean(string='CP không hợp lý', help='Chi phí không hợp lý')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    CHI_TIET_ID = fields.Many2one('tien.luong.hach.toan.chi.phi.luong', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', oldname='NAME')
    STT = fields.Integer(string='STT', help='Số thứ tự')

    @api.onchange('DOI_TUONG_NO_ID','DOI_TUONG_CO_ID')
    def update_TenDoiTuong(self):
        self.TEN_DOI_TUONG_NO = self.DOI_TUONG_NO_ID.HO_VA_TEN
        self.TEN_DOI_TUONG_CO = self.DOI_TUONG_CO_ID.HO_VA_TEN
