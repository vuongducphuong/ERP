# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_NGHIEM_THU_HACH_TOAN(models.Model):
    _name = 'gia.thanh.nghiem.thu.hach.toan'
    _description = ''
    _inherit = ['mail.thread']
    MA_CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Mã công trình', help='Mã công trình')
    TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình')
    LOAI_CONG_TRINH = fields.Many2one('danh.muc.loai.cong.trinh', string='Loại công trình', help='Loại công trình')

    SO_DON_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Số đơn hàng', help='Số đơn hàng')
    NGAY_DON_HANG = fields.Date(string='Ngày đơn hàng', help='Ngày đơn hàng')
    KHACH_HANG = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng')

    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Số hợp đồng', help='Số hợp đồng')    
    NGAY_KY = fields.Date(string='Ngày ký', help='Ngày ký')
    TRICH_YEU = fields.Char(string='Trích yếu', help='Trích yếu')

    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK nợ', help='Tài khoản nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK có', help='Tài khoản có')
    DOANH_THU = fields.Float(string='Doanh thu', help='Doanh thu')
    SO_CHUA_NGHIEM_THU = fields.Float(string='Số chưa nghiệm thu', help='Số chưa nghiệm thu')
    PHAN_TRAM_NGHIEM_THU = fields.Float(string='% nghiệm thu', help='Phần trăm nghiệm thu')
    GIA_TRI_NGHIEM_THU = fields.Float(string='Giá trị nghiệm thu', help='Giá trị nghiệm thu')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục CP', help='Khoản mục chi phí')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    CHI_TIET_ID = fields.Many2one('gia.thanh.nghiem.thu', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    STT = fields.Integer(string='STT', help ='Số thứ tự')

    