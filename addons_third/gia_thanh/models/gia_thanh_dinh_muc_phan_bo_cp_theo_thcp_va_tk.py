# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_DINH_MUC_PHAN_BO_CP_THEO_THCP_VA_TK(models.Model):
    _name = 'gia.thanh.dinh.muc.phan.bo.cp.theo.thcp.va.tk'
    _description = ''
    _inherit = ['mail.thread']
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng tập hợp chi phí', help='Đối tượng tập hợp chi phí')
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    name = fields.Char(string='Name', help='Name')
    KY_TINH_GIA_THANH_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh', string='Kỳ tính giá thành', help='Kỳ tính giá thành')