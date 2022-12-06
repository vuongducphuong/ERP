# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class ASSET_DANH_GIA_LAI_TAI_SAN_CO_DINH_HACH_TOAN(models.Model):
    _name = 'asset.danh.gia.lai.hach.toan'
    _description = ''
    _inherit = ['mail.thread']
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK Nợ ', help='Tài khoản nợ ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK Có', help='Tài khoản có')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('VND'))
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng')
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng',related='DOI_TUONG_ID.HO_VA_TEN',store=True)
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục CP', help='Khoản mục chi phí')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng tập hợp chi phí')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    CP_KHONG_HOP_LY = fields.Boolean(string='CP không hợp lý', help='Chi phí không hợp lý')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    DANH_GIA_LAI_TAI_SAN_CO_DINH_ID = fields.Many2one('asset.danh.gia.lai', string='Đánh giá lại tài sản cố định', help='Đánh giá lại tài sản cố định', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    SO_TIEN_QUY_DOI = fields.Float(string='Số tiền quy đổi', help='Số tiền quy đổi')
    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết',help='Thứ tự sắp xếp các dòng chi tiết')
    @api.onchange('DOI_TUONG_ID')
    def update_Trường(self):
        self.TEN_DOI_TUONG = self.env['res.partner'].search([('id', '=' , self.DOI_TUONG_ID.id)],limit=1).HO_VA_TEN