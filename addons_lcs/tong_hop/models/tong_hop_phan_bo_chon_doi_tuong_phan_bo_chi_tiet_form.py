# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_PHAN_BO_CHON_DOI_TUONG_PHAN_BO_CHI_TIET_FORM(models.Model):
    _name = 'tong.hop.phan.bo.chon.doi.tuong.phan.bo.chi.tiet.form'
    _description = ''
    _inherit = ['mail.thread']
    MA_DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Mã đơn vị', help='Mã đơn vị')
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng')
    CAP_TO_CHUC = fields.Char(string='Cấp tổ chức', help='Cấp tổ chức')

    DOI_TUONG_PB_ID = fields.Many2one('danh.muc.to.chuc', string='Đối tượng phân bổ', help='Đối tượng phân bổ')
    TEN_DOI_TUONG_PB = fields.Char(string='Tên đối tượng phân bổ', help='Tên đối tượng phân bổ')
    LOAI = fields.Char(string='Loại', help='Loại')
    PHAN_BO_CHON_DOI_TUONG_PHAN_BO_ID = fields.Many2one('tong.hop.phan.bo.chon.doi.tuong.phan.bo.form', string='Phân bổ chọn đối tượng phân bổ', help='Phân bổ chọn đối tượng phân bổ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')