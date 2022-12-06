# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class SUPPLY_PHAN_BO_CHI_PHI_HACH_TOAN(models.Model):
    _name = 'supply.phan.bo.chi.phi.hach.toan'
    _description = ''
    _inherit = ['mail.thread']
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk nợ', help='Tk nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk có', help='Tk có')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('VND'))
    DOI_TUONG_NO_ID = fields.Many2one('res.partner', string='Đối tượng nợ', help='Đối tượng nợ')
    TEN_DOI_TUONG_NO = fields.Char(string='Tên đối tượng nợ', help='Tên đối tượng nợ',related='DOI_TUONG_NO_ID.HO_VA_TEN',store=True)
    DOI_TUONG_CO_ID = fields.Many2one('res.partner', string='Đối tượng có', help='Đối tượng có')
    TEN_DOI_TUONG_CO = fields.Char(string='Tên đối tượng có', help='Tên đối tượng có',related='DOI_TUONG_CO_ID.HO_VA_TEN',store=True)
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục cp', help='Khoản mục cp')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng thcp', help='Đối tượng thcp')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    CB_KHONG_HOP_LY = fields.Boolean(string='Cb không hợp lý', help='Cb không hợp lý')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    PHAN_BO_CHI_PHI_ID = fields.Many2one('supply.phan.bo.chi.phi', string='Phân bổ chi phí', help='Phân bổ chi phí', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    SO_TIEN_QUY_DOI = fields.Float(string='Số tiền quy đổi', help='Số tiền quy đổi')
    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết',help='Thứ tự sắp xếp các dòng chi tiết')