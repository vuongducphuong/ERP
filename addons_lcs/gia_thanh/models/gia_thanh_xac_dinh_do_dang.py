# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_XAC_DINH_DO_DANG(models.Model):
    _name = 'gia.thanh.xac.dinh.do.dang'
    _description = ''
    _inherit = ['mail.thread']
    KY_TINH_GIA_THANH_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh', string='Kỳ tính giá thành', help='Kỳ tính giá thành', ondelete='cascade')
    KY_TINH_GIA_THANH_CHI_TIET_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh.chi.tiet', string='Kỳ tính giá thành chi tiết', help='Kỳ tính giá thành chi tiết')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Mã đối tượng THCP', help='Mã đối tượng tập hợp chi phí')
    GIA_THANH_KET_QUA_CHI_PHI_DO_DANG_CUOI_KY_CHI_TIET_IDS = fields.One2many('gia.thanh.ket.qua.chi.phi.do.dang.cuoi.ky.chi.tiet', 'XAC_DINH_DO_DANG_ID', string='Xác định dở dang chi tiết')