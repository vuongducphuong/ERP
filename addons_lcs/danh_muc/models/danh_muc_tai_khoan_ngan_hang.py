# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_TAI_KHOAN_NGAN_HANG(models.Model):
    _name = 'danh.muc.tai.khoan.ngan.hang'
    _description = ''
    _order = "SO_TAI_KHOAN, CHI_NHANH"

    NGAN_HANG_ID = fields.Many2one('danh.muc.ngan.hang', string='Ngân hàng')
    CHI_NHANH = fields.Char(string='Chi nhánh', help='Chi nhánh')
    TINH_TP = fields.Char(string='Tỉnh tp', help='Tỉnh tp')
    DIA_CHI_CN = fields.Char(string='Địa chỉ CN', help='Địa chỉ cn')
    CHU_TAI_KHOAN = fields.Char(string='Chủ tài khoản', help='Chủ tài khoản')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    name = fields.Char(string='Name', help='Name',related='SO_TAI_KHOAN',store=True)
    SO_TAI_KHOAN = fields.Char(string='Số tài khoản', help='Số tài khoản')
    CHI_NHANH_2 = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh')

    image = fields.Binary("Image", attachment=True,
       help="Chọn logo",store=True,compute='_compute_anh_ngan_hang')

    _sql_constraints = [
        ('SO_TAI_KHOAN_uniq', 'unique ("SO_TAI_KHOAN")', 'Số tài khoản ngân hàng <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]

       
    # Hàm tiện ích lấy ra tên của Ngân hàng
    def get_Ten_Ngan_hang(self,soTaiKhoan):
        tenTaiKhoan = ''
        if soTaiKhoan:
            if soTaiKhoan.NGAN_HANG_ID.TEN_DAY_DU:
                tenTaiKhoan =  str (soTaiKhoan.NGAN_HANG_ID.TEN_DAY_DU) 
            if soTaiKhoan.CHI_NHANH:
                tenTaiKhoan = str (soTaiKhoan.CHI_NHANH)
            if soTaiKhoan.NGAN_HANG_ID.TEN_DAY_DU and soTaiKhoan.CHI_NHANH:
                ngang = '-'
                tenTaiKhoan = str(soTaiKhoan.NGAN_HANG_ID.TEN_DAY_DU) + ngang + str(soTaiKhoan.CHI_NHANH)
            return tenTaiKhoan
        else:
            return tenTaiKhoan
    
    # depend để lấy ảnh ngân hàng
    @api.depends('NGAN_HANG_ID')
    def _compute_anh_ngan_hang(self):
        for record in self: 
            record.image = record.NGAN_HANG_ID.image

    
    
    