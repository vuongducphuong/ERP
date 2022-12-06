# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class BAO_CAO_S37_DN_THE_TINH_GIA_THANH_SAN_PHAM_DICH_VU_CHI_TIET(models.Model):
    _name = 'bao.cao.s37.dn.the.tinh.gia.thanh.san.pham.dich.vu.chi.tiet'
    
    MA_THANH_PHAM_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã thành phẩm', help='Mã thành phẩm')
    TEN_THANH_PHAM = fields.Char(string='Tên thành phẩm', help='Tên thành phẩm' ,related='MA_THANH_PHAM_ID.TEN', store=True)

    MA_DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Mã đối tượng THCP', help='Mã đối tượng THCP')
    TEN_DOI_TUONG_THCP = fields.Char(string='Tên đối tượng THCP', help='Tên đối tượng THCP' ,related='MA_DOI_TUONG_THCP_ID.TEN_DOI_TUONG_THCP', store=True)
   
    MA_CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Mã ', help='Mã ')
    TEN_CONG_TRINH = fields.Char(string='Tên', help='Tên',related='MA_CONG_TRINH_ID.TEN_CONG_TRINH', store=True)
    LOAI_CONG_TRINH = fields.Many2one('danh.muc.loai.cong.trinh', string='Loại công trình', help='Loại công trình',related='MA_CONG_TRINH_ID.LOAI_CONG_TRINH',store=True, )
    BAC = fields.Integer(string='Bậc', help='Bậc',related='MA_CONG_TRINH_ID.BAC',store=True, )
    

    