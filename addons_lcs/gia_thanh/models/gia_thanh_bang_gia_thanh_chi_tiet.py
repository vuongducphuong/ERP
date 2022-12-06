# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class GIA_THANH_BANG_GIA_THANH_CHI_TIET(models.Model):
    _name = 'gia.thanh.bang.gia.thanh.chi.tiet'
    _description = ''

    MA_THANH_PHAM_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã thành phẩm', help='Mã thành phẩm')
    TEN_THANH_PHAM = fields.Char(string='Tên thành phẩm', help='Tên thành phẩm')
    MA_DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Mã đối tượng THCP', help='Mã đối tượng tập hợp chi phí')
    TEN_DOI_TUONG_THCP = fields.Char(string='Tên đối tượng THCP', help='Tên đối tượng tập hợp chi phí')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Đơn vị tính', help='Đơn vị tính')
    TY_LE_PHAN_BO_GIA_THANH = fields.Float(string='Tỷ lệ phân bổ giá thành', help='Tỷ lệ phân bổ giá thành',digits=decimal_precision.get_precision('TY_LE_PHAN_BO'))
    NVL_TRUC_TIEP = fields.Float(string='NVL trực tiếp', help='Nguyên vật liệu trực tiếp',digits=decimal_precision.get_precision('VND'))
    NVL_GIAN_TIEP = fields.Float(string='NVL gián tiếp', help='Nguyên vật liệu gián tiếp',digits=decimal_precision.get_precision('VND'))
    NHAN_CONG_TRUC_TIEP = fields.Float(string='Nhân công trực tiếp', help='Nhân công trực tiếp',digits=decimal_precision.get_precision('VND'))
    NHAN_CONG_GIAN_TIEP = fields.Float(string='Nhân công gián tiếp', help='Nhân công gián tiếp',digits=decimal_precision.get_precision('VND'))
    KHAU_HAO = fields.Float(string='Khấu hao', help='Khấu hao',digits=decimal_precision.get_precision('VND'))
    CHI_PHI_MUA_NGOAI = fields.Float(string='Chi phí mua ngoài', help='Chi phí mua ngoài',digits=decimal_precision.get_precision('VND'))
    CHI_PHI_KHAC = fields.Float(string='Chi phí khác', help='Chi phí khác',digits=decimal_precision.get_precision('VND'))
    TONG = fields.Float(string='Tổng', help='Tổng',digits=decimal_precision.get_precision('VND'))
    SO_LUONG_THANH_PHAM = fields.Float(string='Số lượng thành phẩm', help='Số lượng thành phẩm', digits=decimal_precision.get_precision('SO_LUONG'))
    GIA_THANH_DON_VI = fields.Float(string='Giá thành đơn vị', help='Giá thành đơn vị',digits=decimal_precision.get_precision('DON_GIA'))
    CHI_TIET_ID = fields.Many2one('gia.thanh.tinh.gia.thanh', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    KY_TINH_GIA_THANH_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh', string='Kỳ tính giá thành', help='Kỳ tính giá thành', ondelete='cascade')
    sequence = fields.Integer()


# class GIA_THANH_BANG_GIA_THANH_CHI_TIET_VTHH(models.Model):
#     _name = 'gia.thanh.ky.tinh.gia.thanh.vat.tu.hang.hoa.chi.tiet'
#     _description = ''
#     

# class GIA_THANH_KY_TINH_GIA_THANH_HOP_DONG_CHI_TIET(models.Model):
#     _name = 'gia.thanh.ky.tinh.gia.thanh.hop.dong.chi.tiet'
#     _description = ''
#     

# class GIA_THANH_KY_TINH_GIA_THANH_DON_HANG_CHI_TIET(models.Model):
#     _name = 'gia.thanh.ky.tinh.gia.thanh.don.hang.chi.tiet'
#     _description = ''
#     

# class GIA_THANH_KY_TINH_GIA_THANH_CONG_TRINH_CHI_TIET(models.Model):
#     _name = 'gia.thanh.ky.tinh.gia.thanh.cong.trinh.chi.tiet'
#     _description = ''
#     