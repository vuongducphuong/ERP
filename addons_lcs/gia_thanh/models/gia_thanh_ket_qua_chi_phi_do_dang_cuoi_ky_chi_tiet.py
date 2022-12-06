# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class GIA_THANH_KET_QUA_CHI_PHI_DO_DANG_CUOI_KY_CHI_TIET(models.Model):
    _name = 'gia.thanh.ket.qua.chi.phi.do.dang.cuoi.ky.chi.tiet'
    _description = ''

    MA_DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Mã đối tượng THCP', help='Mã đối tượng tập hợp chi phí')
    TEN_DOI_TUONG_THCP = fields.Char(string='Tên đối tượng THCP', help='Tên đối tượng tập hợp chi phí')
    TONG_CHI_PHI = fields.Float(string='Tổng chi phí', help='Tổng chi phí',digits=decimal_precision.get_precision('VND'))
    NVL_TRUC_TIEP = fields.Float(string='NVL trực tiếp', help='Nguyên vật liệu trực tiếp',digits=decimal_precision.get_precision('VND'))
    NVL_GIAN_TIEP = fields.Float(string='NVL gián tiếp', help='Nguyên vật liệu gián tiếp',digits=decimal_precision.get_precision('VND'))
    NHAN_CONG_TRUC_TIEP = fields.Float(string='Nhân công trực tiếp', help='Nhân công trực tiếp',digits=decimal_precision.get_precision('VND'))
    NHAN_CONG_GIAN_TIEP = fields.Float(string='Nhân công gián tiếp', help='Nhân công gián tiếp',digits=decimal_precision.get_precision('VND'))
    KHAU_HAO = fields.Float(string='Khấu hao', help='Khấu hao',digits=decimal_precision.get_precision('VND'))
    CHI_PHI_MUA_NGOAI = fields.Float(string='Chi phí mua ngoài', help='Chi phí mua ngoài',digits=decimal_precision.get_precision('VND'))
    CHI_PHI_KHAC = fields.Float(string='Chi phí khác', help='Chi phí khác',digits=decimal_precision.get_precision('VND'))
    CHI_TIET_ID = fields.Many2one('gia.thanh.tinh.gia.thanh', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    KY_TINH_GIA_THANH_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh', string='Kỳ tính giá thành', help='Kỳ tính giá thành', ondelete='cascade')
    XAC_DINH_DO_DANG_ID = fields.Many2one('gia.thanh.xac.dinh.do.dang', string='Xác định dở dang', help='Xác định dở dang', ondelete='cascade')
    GIA_THANH_XAC_DINH_DO_DANG_CHI_TIET_IDS = fields.One2many('gia.thanh.xac.dinh.do.dang.chi.tiet', 'GIA_THANH_KQ_CHI_PHI_DO_DANG_CHI_TIET_ID', string='Xác định dở dang chi tiết')
    sequence = fields.Integer()

    