# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_TY_LE_PHAN_BO_DOI_TUONG_THCP_CHI_TIET(models.Model):
    _name = 'gia.thanh.ty.le.phan.bo.doi.tuong.thcp.chi.tiet'
    _description = ''
    
    MA_DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Mã đối tượng THCP', help='Mã đối tượng tập hợp chi phí')
    TEN_DOI_TUONG_THCP = fields.Char(string='Tên đối tượng THCP', help='Tên đối tượng tập hợp chi phí')
    LOAI_DOI_TUONG_THCP = fields.Selection([('0', 'Phân xưởng'), ('1', 'Sản phẩm'), ('2', 'Quy trình sản xuất'), ('3', 'Công đoạn'), ], string='Loại đối tượng THCP', help='Loại đối tượng THCP',default='0')
    PHUONG_PHAP_XAC_DINH = fields.Selection([('HE_SO', 'Hệ số'), ('TY_LE', ' Tỷ lệ'), ], string='Phương pháp xác định', help='Phương pháp xác định',related='CHI_TIET_ID.PHUONG_PHAP_XAC_DINH')
    CHI_TIET_ID = fields.Many2one('gia.thanh.tinh.gia.thanh', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    KY_TINH_GIA_THANH_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')