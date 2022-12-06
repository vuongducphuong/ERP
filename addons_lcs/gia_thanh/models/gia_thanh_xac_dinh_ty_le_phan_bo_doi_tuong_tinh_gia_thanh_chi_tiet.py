# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class GIA_THANH_XAC_DINH_TY_LE_PHAN_BO_DOI_TUONG_TINH_GIA_THANH_CHI_TIET(models.Model):
    _name = 'gia.thanh.xdtlpb.doi.tuong.tinh.gia.thanh.chi.tiet'
    _description = ''
    
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng tập hợp chi phí')
    MA_THANH_PHAM_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã thành phẩm', help='Mã thành phẩm')
    TEN_THANH_PHAM = fields.Char(string='Tên thành phẩm', help='Tên thành phẩm')
    LA_THANH_PHAM_CHUAN = fields.Boolean(string='Là thành phẩm chuẩn', help='Là thành phẩm chuẩn')
    SO_LUONG_THANH_PHAM = fields.Float(string='Số lượng thành phẩm', help='Số lượng thành phẩm', digits=decimal_precision.get_precision('SO_LUONG'))
    GIA_THANH_DINH_MUC = fields.Float(string='Giá thành định mức', help='Giá thành định mức')
    HE_SO = fields.Float(string='Hệ số', help='Hệ số',digits=decimal_precision.get_precision('TY_LE_PHAN_BO'))
    SO_LUONG_THANH_PHAM_CHUAN = fields.Float(string='Số lượng thành phẩm chuẩn', help='Số lượng thành phẩm chuẩn', digits=decimal_precision.get_precision('SO_LUONG'))
    TIEU_CHUAN_PHAN_BO = fields.Float(string='Tiêu chuẩn phân bổ', help='Tiêu chuẩn phân bổ')
    TY_LE_PHAN_BO_GIA_THANH = fields.Float(string='Tỷ lệ phân bổ giá thành', help='Tỷ lệ phân bổ giá thành',digits=decimal_precision.get_precision('TY_LE_PHAN_BO'))
    CHI_TIET_ID = fields.Many2one('gia.thanh.tinh.gia.thanh', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    KY_TINH_GIA_THANH_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh', string='Kỳ tính giá thành', help='Kỳ tính giá thành', ondelete='cascade')
    sequence = fields.Integer()

    @api.onchange('HE_SO')
    def _onchange_HE_SO(self):
        self.SO_LUONG_THANH_PHAM_CHUAN = self.HE_SO*self.SO_LUONG_THANH_PHAM

    @api.onchange('GIA_THANH_DINH_MUC')
    def _onchange_GIA_THANH_DINH_MUC(self):
        self.TIEU_CHUAN_PHAN_BO = self.GIA_THANH_DINH_MUC*self.SO_LUONG_THANH_PHAM