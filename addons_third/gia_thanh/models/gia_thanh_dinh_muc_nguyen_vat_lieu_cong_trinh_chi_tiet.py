# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class GIA_THANH_DINH_MUC_NGUYEN_VAT_LIEU_CONG_TRINH_CHI_TIET(models.Model):
    _name = 'gia.thanh.dinh.muc.nguyen.vat.lieu.cong.trinh.chi.tiet'
    _description = ''

    MA_NGUYEN_VAT_LIEU_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã nguyên vật liệu ', help='Mã nguyên vật liệu ')
    TEN_NGUYEN_VAT_LIEU = fields.Char(string='Tên nguyên vật liệu', help='Tên nguyên vật liệu', related='MA_NGUYEN_VAT_LIEU_ID.TEN',store=True, )
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đơn vị tính', related='MA_NGUYEN_VAT_LIEU_ID.DVT_CHINH_ID',store=True,)
    SO_LUONG_DINH_MUC = fields.Float(string='Số lượng định mức', help='Số lượng định mức', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA_DINH_MUC = fields.Float(string='Đơn giá định mức', help='Đơn giá định mức', related='MA_NGUYEN_VAT_LIEU_ID.DON_GIA_MUA_GAN_NHAT',store=True,digits= decimal_precision.get_precision('DON_GIA'))
    THANH_TIEN = fields.Float(string='Thành tiền', help='Thành tiền',digits=decimal_precision.get_precision('VND'))
    CHI_TIET_ID = fields.Many2one('gia.thanh.dinh.muc.nguyen.vat.lieu.cong.trinh', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    STT = fields.Integer (string='STT', help= 'Số thứ tự')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    @api.model
    def default_get(self, fields):
        rec = super(GIA_THANH_DINH_MUC_NGUYEN_VAT_LIEU_CONG_TRINH_CHI_TIET, self).default_get(fields)
        rec['SO_LUONG_DINH_MUC'] = 1
        return rec

    @api.onchange('SO_LUONG_DINH_MUC','DON_GIA_DINH_MUC')
    def _onchange_SO_LUONG_DINH_MUC(self):
        self.THANH_TIEN = self.SO_LUONG_DINH_MUC * self.DON_GIA_DINH_MUC