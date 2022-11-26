# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET(models.Model):
    _name = 'gia.thanh.xac.dinh.do.dang.chi.tiet'
    _description = ''
    
    MA_THANH_PHAM_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã thành phẩm', help='Mã thành phẩm')
    TEN_THANH_PHAM = fields.Char(string='Tên thành phẩm', help='Tên thành phẩm')
    SL_DO_DANG_CUOI_KY = fields.Float(string='SL dở dang cuối kỳ', help='Số lượng dở dang cuối kỳ')
    PHAN_TRAM_HOAN_THANH = fields.Float(string='Phần trăm hoàn thành', help='Phần trăm hoàn thành')
    DON_GIA_DINH_MUC = fields.Float(string='Đơn giá định mức', help='Đơn giá định mức')
    MA_DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Mã đối tượng THCP', help='Mã đối tượng tập hợp chi phí')
    TEN_DOI_TUONG_THCP = fields.Char(string='Tên đối tượng THCP', help='Tên đối tượng tập hợp chi phí')
    CHI_TIET_ID = fields.Many2one('gia.thanh.tinh.gia.thanh', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    sequence = fields.Integer()
    GIA_THANH_KQ_CHI_PHI_DO_DANG_CHI_TIET_ID = fields.Many2one('gia.thanh.ket.qua.chi.phi.do.dang.cuoi.ky.chi.tiet', string='Gía thành kết quả chi phí dở dang chi tiết', help='Gía thành kết quả chi phí dở dang chi tiết', ondelete='cascade')
    KY_TINH_GIA_THANH_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    # KET_QUA_CHI_PHI_DO_DANG_CUOI_KY_CHI_TIET_ID = fields.Many2one('gia.thanh.ket.qua.chi.phi.do.dang.cuoi.ky.chi.tiet', string='Chi tiết', help='Chi tiết', ondelete='cascade')