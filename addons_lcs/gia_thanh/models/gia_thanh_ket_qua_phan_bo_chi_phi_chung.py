# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class GIA_THANH_KET_QUA_PHAN_BO_CHI_PHI_CHUNG(models.Model):
    _name = 'gia.thanh.ket.qua.phan.bo.chi.phi.chung'
    _description = ''
    _inherit = ['mail.thread']
    PHAN_BO_CHI_TIET_ID = fields.Many2one('gia.thanh.ket.qua.phan.bo.chi.tiet', string='Phân bổ chi tiết', help='Phân bổ chi tiết')
    KY_TINH_GIA_THANH_CHI_TIET_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh.chi.tiet', string='Kỳ tính giá thành chi tiết', help='Kỳ tính giá thành chi tiết')
    KY_TINH_GIA_THANH_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh', string='Kỳ tính giá thành', help='Kỳ tính giá thành', ondelete='cascade')
    MA_DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Mã đối tượng tập hợp chi phí', help='Mã đối tượng tập hợp chi phí')
    MA_CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Mã công trình', help='Mã công trình')
    SO_DON_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Số đơn hàng', help='Số đơn hàng')
    SO_HOP_DONG_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Số hợp đồng', help='Số hợp đồng')
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản')
    SO_TAI_KHOAN = fields.Char(string='Số tài khoản', help='Số tài khoản')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục chi phí', help='Khoản mục chi phí')
    TY_LE = fields.Float(string='Tỷ lệ', help='Tỷ lệ',digits=decimal_precision.get_precision('TY_LE_PHAN_BO'))
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('VND'))
    TIEU_THUC_PHAN_BO = fields.Selection([('0', 'Nguyên vật liệu trực tiếp'), ('1', 'Nhân công trực tiếp'), ('2', 'Chi phí trực tiếp (NVLTT, NCTT)'), ('3', 'Định mức'), ], string='Tiêu thức phân bổ', help='Tiêu thức phân bổ')
    DA_PHAN_BO = fields.Boolean(string='Đã phân bổ', help='Đã phân bổ')
    NAME = fields.Char(string='Name', help='Name')