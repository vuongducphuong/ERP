# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ACCOUNT_EX_SDTKCT_CHI_TIET_THEO_DOI_TUONG(models.Model):
    _name = 'account.ex.sdtkct.theo.doi.tuong'
    _description = ''

    name = fields.Char(string='Name', help='Name')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên', help='Nhân viên')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    DON_MUA_HANG_ID = fields.Many2one('purchase.ex.don.mua.hang', string='Đơn mua hàng', help='Đơn mua hàng')
    HOP_DONG_MUA_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang', string='Hợp đồng mua', help='Hợp đồng mua')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục CP', help='Khoản mục CP')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng THCP')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    DU_NO = fields.Float(string='Dư nợ', help='Dư nợ')
    DU_CO = fields.Float(string='Dư có', help='Dư có')
    DU_NO_NGUYEN_TE = fields.Float(string='Dư nợ nguyên tệ', help='Dư nợ nguyên tệ')
    DU_CO_NGUYEN_TE = fields.Float(string='Dư có nguyên tệ', help='Dư có nguyên tệ')
    SO_DU_TAI_KHOAN_CHI_TIET_ID = fields.Many2one('account.ex.so.du.tai.khoan.chi.tiet', string='Số dư tài khoản', help='Số dư tài khoản', ondelete='cascade')

    
    @api.model
    def create(self, values):
        master = self.env['account.ex.so.du.tai.khoan.chi.tiet'].search([('id', '=', values.get('SO_DU_TAI_KHOAN_CHI_TIET_ID'))])
        if master:
            if master.currency_id.MA_LOAI_TIEN == 'VND':
                values['DU_NO_NGUYEN_TE'] = values.get('DU_NO')
                values['DU_CO_NGUYEN_TE'] = values.get('DU_CO')
        result = super(ACCOUNT_EX_SDTKCT_CHI_TIET_THEO_DOI_TUONG, self).create(values)
        return result
    
