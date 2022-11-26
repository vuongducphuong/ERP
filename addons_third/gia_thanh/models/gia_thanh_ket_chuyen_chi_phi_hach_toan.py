# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_KET_CHUYEN_CHI_PHI_HACH_TOAN(models.Model):
    _name = 'gia.thanh.ket.chuyen.chi.phi.hach.toan'
    _description = ''
    _inherit = ['mail.thread']
    MA_DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Mã đối tượng THCP', help='Mã đối tượng tập hợp chi phí')
    TEN_DOI_TUONG_THCP = fields.Char(string='Tên đối tượng THCP ', help='Tên đối tượng THCP' ,related='MA_DOI_TUONG_THCP_ID.TEN_DOI_TUONG_THCP', store=True)
    LOAI_DOI_TUONG_THCP = fields.Selection([('0', 'Phân xưởng'), ('1', 'Sản phẩm'), ('2', 'Quy trình sản xuất'), ('3', 'Công đoạn'),] ,related='MA_DOI_TUONG_THCP_ID.LOAI', store=True , string='Loại đối tượng THCP')
    
    MA_CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Mã công trình', help='Mã công trình')
    TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình' ,related='MA_CONG_TRINH_ID.TEN_CONG_TRINH', store=True)
    LOAI_CONG_TRINH = fields.Many2one('danh.muc.loai.cong.trinh', string='Loại công trình', help='Loại công trình',related='MA_CONG_TRINH_ID.LOAI_CONG_TRINH',store=True, )


    SO_DON_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Số đơn hàng', help='Số đơn hàng')
    NGAY_DON_HANG = fields.Date(string='Ngày đơn hàng', help='Ngày đơn hàng')
    KHACH_HANG = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng')

    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Số hợp đồng', help='Số hợp đồng')    
    NGAY_KY = fields.Date(string='Ngày ký', help='Ngày ký',related='HOP_DONG_BAN_ID.NGAY_KY', store=True)
    TRICH_YEU = fields.Text(string='Trích yếu', help='Trích yếu',related='HOP_DONG_BAN_ID.TRICH_YEU', store=True)

    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK nợ', help='Tài khoản nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK có', help='Tài khoản có')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    CHI_TIET_ID = fields.Many2one('gia.thanh.ket.chuyen.chi.phi', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    STT = fields.Integer(string='STT', help= 'Số thứ tự')


    @api.onchange('SO_DON_HANG_ID','HOP_DONG_BAN_ID')
    def lay_thong_tin_khach_hang(self):
        if self.SO_DON_HANG_ID:
            self.KHACH_HANG = self.SO_DON_HANG_ID.TEN_KHACH_HANG
        elif self.HOP_DONG_BAN_ID:
            self.KHACH_HANG = self.HOP_DONG_BAN_ID.TEN_KHACH_HANG