# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
class TONG_HOP_BCTC_CHON_NV_VA_HD_LCTT_CHI_TIET_DIEU_CHINH_FORM(models.Model):
    _name = 'tong.hop.bctc.chon.nv.va.hd.lctt.chi.tiet.dieu.chinh.form'
    _description = ''
    _inherit = ['mail.thread']

    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Float(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK Nợ', help='Tk nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK Có', help='Tk có')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits= decimal_precision.get_precision('VND'))
    NGHIEP_VU = fields.Selection([('NGHIEP_VU_THANH_LY_NHUONG_BAN_TSCD_BDSDT', 'Nghiệp vụ thanh lý nhượng bán TSCĐ BĐSĐT'), ('DANH_GIA_LAI_TAI_SAN_GOP_VON_DAU_TU', ' Đánh giá lại tài sản góp vốn đầu tư'), ('BAN_THU_HOI_CAC_KHOAN_DAU_TU_TAI_CHINH', ' Bán thu hồi các khoản đầu tư tài chính'), ('LAI_CHO_VAY_LAI_TIEN_GUI_CO_TUC_VA_LOI_NHUAN_DUOC_CHIA_LAI_DAU_TU_DINH_KY', ' Lãi cho vay lãi tiền gửi cổ tức và lợi nhuận được chia lãi đầu tư định kỳ'), ('CHI_PHI_LAI_VAY_CHI_TRA_LAI_VAY', ' Chi phí lãi vay chi trả lãi vay '), ], string='nghiệp vụ', help='nghiệp vụ')
    BCTC_CHON_NGHIEP_VU_VA_HOAT_DONG_LCTT_ID = fields.Many2one('tong.hop.bctc.chon.nghiep.vu.va.hoat.dong.lctt.form', string='Bctc chọn nghiệp vụ và hoạt động lctt', help='Bctc chọn nghiệp vụ và hoạt động lctt')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CHI_TIET_ID = fields.Integer(string='chi tiết id', help='id của các chứng từ chi tiết')
    CHI_TIET_MODEL = fields.Char(string='model chi tiết', help='model chi tiết')