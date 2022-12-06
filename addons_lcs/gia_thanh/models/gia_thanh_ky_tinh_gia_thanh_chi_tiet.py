# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_KY_TINH_GIA_THANH_CHI_TIET(models.Model):
    _name = 'gia.thanh.ky.tinh.gia.thanh.chi.tiet'
    _description = ''

    STT = fields.Integer(string='STT',help ='Số thứ tự')
    MA_DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Mã ', help='Mã ')
    TEN_DOI_TUONG_THCP = fields.Char(string='Tên ', help='Tên' ,related='MA_DOI_TUONG_THCP_ID.TEN_DOI_TUONG_THCP', store=True)
    LOAI = fields.Selection([('0', 'Phân xưởng'), ('1', 'Sản phẩm'), ('2', 'Quy trình sản xuất'), ('3', 'Công đoạn'),] ,related='MA_DOI_TUONG_THCP_ID.LOAI', store=True,string='Loại')
    MA_CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Mã ', help='Mã ')
    TEN_CONG_TRINH = fields.Char(string='Tên', help='Tên',related='MA_CONG_TRINH_ID.TEN_CONG_TRINH', store=True)
    LOAI_CONG_TRINH = fields.Many2one('danh.muc.loai.cong.trinh', string='Loại công trình', help='Loại công trình',related='MA_CONG_TRINH_ID.LOAI_CONG_TRINH',store=True, )
    SO_HOP_DONG_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Số hợp đồng', help='Số hợp đồng')
    NGAY_KY = fields.Date(string='Ngày ký', help='Ngày ký',related='SO_HOP_DONG_ID.NGAY_KY', store=True)
    TRICH_YEU = fields.Text(string='Trích yếu', help='Trích yếu',related='SO_HOP_DONG_ID.TRICH_YEU', store=True)
    KHACH_HANG_HOP_DONG = fields.Char(string='Khách hàng', help='Khách hàng',related='SO_HOP_DONG_ID.TEN_KHACH_HANG', store=True)
    SO_DON_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Số đơn hàng', help='Số đơn hàng')
    NGAY_DON_HANG = fields.Date(string='Ngày đơn hàng', help='Ngày đơn hàng',related='SO_DON_HANG_ID.NGAY_DON_HANG', store=True)
    KHACH_HANG_DON_HANG = fields.Char(string='Khách hàng', help='Khách hàng',related='SO_DON_HANG_ID.TEN_KHACH_HANG', store=True)
    KY_TINH_GIA_THANH_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh', string='Kỳ tính giá thành', help='Kỳ tính giá thành', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')