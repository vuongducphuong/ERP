# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class GIA_THANH_KHAI_BAO_DINH_MUC_PHAN_BO_CHI_PHI_THEO_CONG_TRINH_CHI_TIET(models.Model):
    _name = 'gia.thanh.kbdm.pbcp.theo.cong.trinh.chi.tiet'
    _description = ''

    MA_CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Mã công trình', help='Mã công trình')
    TEN_CONG_TRINH = fields.Char(string='Tên công trình', help='Tên công trình', related='MA_CONG_TRINH_ID.TEN_CONG_TRINH')
    TK_621 = fields.Float(string='TK 621', help='Tài khoản 621', digits=decimal_precision.get_precision('VND'))
    TK_622 = fields.Float(string='TK 622', help='Tài khoản 622' , digits=decimal_precision.get_precision('VND'))
    TK_6231 = fields.Float(string='TK 6231', help='Tài khoản 6231', digits=decimal_precision.get_precision('VND'))
    TK_6232 = fields.Float(string='TK 6232', help='Tài khoản 6232', digits=decimal_precision.get_precision('VND'))
    TK_6233 = fields.Float(string='TK 6233', help='Tài khoản 6233' ,digits=decimal_precision.get_precision('VND'))
    TK_6234 = fields.Float(string='TK 6234', help='Tài khoản 6234', digits=decimal_precision.get_precision('VND'))
    TK_6237 = fields.Float(string='TK 6237', help='Tài khoản 6237', digits=decimal_precision.get_precision('VND'))
    TK_6238 = fields.Float(string='TK 6238', help='Tài khoản 6238', digits=decimal_precision.get_precision('VND'))
    TK_6271 = fields.Float(string='TK 6271', help='Tài khoản 6271', digits=decimal_precision.get_precision('VND'))
    TK_6272 = fields.Float(string='TK 6272', help='Tài khoản 6272', digits=decimal_precision.get_precision('VND'))
    TK_6273 = fields.Float(string='TK 6273', help='Tài khoản 6273', digits=decimal_precision.get_precision('VND'))
    TK_6274 = fields.Float(string='TK 6274', help='Tài khoản 6274', digits=decimal_precision.get_precision('VND'))
    TK_6277 = fields.Float(string='TK 6277', help='Tài khoản 6277', digits=decimal_precision.get_precision('VND'))
    TK_6278 = fields.Float(string='TK 6278', help='Tài khoản 6278', digits=decimal_precision.get_precision('VND'))
    TONG_CONG = fields.Float(string='Tổng cộng', help='Tổng cộng', digits=decimal_precision.get_precision('VND'))
    CHI_TIET_ID = fields.Many2one('gia.thanh.kbdm.pbcp.theo.cong.trinh.form', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    @api.onchange('TK_621','TK_622','TK_6231','TK_6232','TK_6233','TK_6234','TK_6237','TK_6238','TK_6271','TK_6272','TK_6273','TK_6274','TK_6277','TK_6278')
    def _onchange_TONG_CONG(self):
        self.TONG_CONG = self.TK_621 + self.TK_622 + self.TK_6231 + self.TK_6232 + self.TK_6233 + self.TK_6234 + self.TK_6237 + self.TK_6238 + self.TK_6271 + self.TK_6272 + self.TK_6273 + self.TK_6274 + self.TK_6277 + self.TK_6278 