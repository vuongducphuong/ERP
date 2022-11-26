# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_KHAI_BAO_DINH_MUC_PHAN_BO_CHI_PHI_THEO_DOI_TUONG_THCP_CHI_TIET(models.Model):
    _name = 'gia.thanh.kbdm.pbcp.theo.dt.thcp.chi.tiet'
    _description = ''
    
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng tập hợp chi phí')
    TEN_DOI_TUONG_THCP = fields.Char(string='Tên đối tượng THCP', help='Tên đối tượng tập hợp chi phí',related='DOI_TUONG_THCP_ID.TEN_DOI_TUONG_THCP')
    LOAI_DOI_TUONG_THCP = fields.Selection([('0', 'Phân xưởng'), ('1', 'Sản phẩm'), ('2', 'Quy trình sản xuất'), ('3', 'Công đoạn'), ],string='Loại đối tượng THCP', help='Loại đối tượng tập hợp chi phí',related='DOI_TUONG_THCP_ID.LOAI', )
    TK_621 = fields.Float(string='TK 621', help='Tài khoản 621')
    TK_622 = fields.Float(string='TK 622', help='Tài khoản 622')
    TK_6271 = fields.Float(string='TK 6271', help='Tài khoản 6271')
    TK_6272 = fields.Float(string='TK 6272', help='Tài khoản 6272')
    TK_6273 = fields.Float(string='TK 6273', help='Tài khoản 6273')
    TK_6274 = fields.Float(string='TK 6274', help='Tài khoản 6274')
    TK_6277 = fields.Float(string='TK 6277', help='Tài khoản 6277')
    TK_6278 = fields.Float(string='TK 6278', help='Tài khoản 6278')
    TONG_CONG = fields.Float(string='Tổng cộng', help='Tổng cộng')
    CHI_TIET_ID = fields.Many2one('gia.thanh.kbdm.pbcp.theo.doi.tuong.thcp.form', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')