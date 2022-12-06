# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class ACCOUNT_EX_TAM_UNG_HOA_DON(models.Model):
    _name = 'account.ex.tam.ung.hoa.don'
    _description = ''
    _inherit = ['mail.thread']
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    KHONG_CO_HOA_DON = fields.Boolean(string='Không có hóa đơn', help='Không có hóa đơn')
    MAU_SO_HD_ID = fields.Many2one('danh.muc.mau.so.hd', string='Mẫu số HĐ', help='Mẫu số hđ')
    KY_HIEU_HD = fields.Char(string='Ký hiệu HĐ', help='Ký hiệu hđ')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    NHOM_HHDV_MUA_VAO_ID = fields.Many2one('danh.muc.nhom.hhdv', string='Nhóm HHDV mua vào', help='Nhóm hhdv mua vào', default=lambda self: self.lay_nhom_hhdv_mac_dinh())
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Mã đối tượng', help='Mã đối tượng')
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    TAM_UNG_HOA_DON_ID = fields.Many2one('account.ex.chung.tu.nghiep.vu.khac', string='Tạm ứng hóa đơn', help='Tạm ứng hóa đơn')
    name = fields.Char(string='Name', help='Name', oldname='NAME')



    @api.onchange('DOI_TUONG_ID')
    def thaydoidt(self):
        self.TEN_DOI_TUONG=self.DOI_TUONG_ID.HO_VA_TEN
        self.MA_SO_THUE=self.DOI_TUONG_ID.MA_SO_THUE
        self.DIA_CHI=self.DOI_TUONG_ID.DIA_CHI