# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class ASSET_TAI_SAN_CO_DINH_NGUON_GOC_HINH_THANH(models.Model):
    _name = 'asset.ghi.tang.nguon.goc.hinh.thanh'
    _description = ''
    _inherit = ['mail.thread']
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Text(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk nợ', help='Tk nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk có', help='Tk có')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    TAI_SAN_CO_DINH_GHI_TANG_ID = fields.Many2one('asset.ghi.tang', string='Tài sản cố định ghi tăng', help='Tài sản cố định ghi tăng', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    ID_GOC = fields.Integer()
    MODEL_GOC = fields.Char ()
    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết',help='Thứ tự sắp xếp các dòng chi tiết')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')
    