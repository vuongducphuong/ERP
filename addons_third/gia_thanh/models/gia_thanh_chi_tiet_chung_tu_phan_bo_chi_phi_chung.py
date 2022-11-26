# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_CHI_TIET_CHUNG_TU_PHAN_BO_CHI_PHI_CHUNG(models.Model):
    _name = 'gia.thanh.chi.tiet.chung.tu.phan.bo.chi.phi.chung'
    _description = ''
    _inherit = ['mail.thread']
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_CHI_PHI_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk chi phí', help='Tk chi phí')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    SO_CHUA_PHAN_BO = fields.Float(string='Số chưa phân bổ', help='Số chưa phân bổ')
    SO_PHAN_BO_LAN_NAY = fields.Float(string='Số phân bổ lần này', help='Số phân bổ lần này')
    TY_LE_PHAN_BO = fields.Float(string='Tỷ lệ phân bổ', help='Tỷ lệ phân bổ')
    ID_GOC = fields.Integer(string='Id gốc', help='Id gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')
    KY_TINH_GIA_THANH_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh', string='Kỳ tính giá thành', help='Kỳ tính giá thành', ondelete='cascade')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục chi phí', help='Khoản mục chi phí')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    SO_TAI_KHOAN_CON_LAI = fields.Float(string='Số tài khoản còn lại', help='Số tài khoản còn lại')
    SO_TAI_KHOAN_TONG_TIEN = fields.Float(string='Số tài khoản tổng tiền', help='Số tài khoản tổng tiền')
    CHI_TIET_ID = fields.Many2one('gia.thanh.tinh.gia.thanh', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_ID = fields.Many2one('gia.thanh.tinh.gia.thanh', string='Chi tiết', help='Chi tiết', ondelete='cascade')