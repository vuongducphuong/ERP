# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ACCOUNT_EX_SDTKCT_THEO_HOA_DON(models.Model):
    _name = 'account.ex.sdtkct.theo.hoa.don'
    _description = ''

    name = fields.Char(string='Name', help='Name')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên', help='Nhân viên')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    DU_NO = fields.Float(string='Dư nợ', help='Dư nợ')
    DU_CO = fields.Float(string='Dư có', help='Dư có')
    DU_NO_NGUYEN_TE = fields.Float(string='Dư nợ nguyên tệ', help='Dư nợ nguyên tệ')
    DU_CO_NGUYEN_TE = fields.Float(string='Dư có nguyên tệ', help='Dư có nguyên tệ')
    SO_DU_TAI_KHOAN_CHI_TIET_ID = fields.Many2one('account.ex.so.du.tai.khoan.chi.tiet', string='Số dư tài khoản', help='Số dư tài khoản', ondelete='cascade')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn/chứng từ',default=fields.Datetime.now)
    SO_HOA_DON = fields.Char(string='Số hóa đơn/chứng từ')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá',default=1)
    THU_TU_TRONG_CHUNG_TU = fields.Integer(string='Thứ tự trong chứng từ', help='Thứ tự trong chứng từ')
    SO_THU_TRUOC = fields.Float(string='Số thu trước', help='Số thu trước')
    SO_THU_TRUOC_NGUYEN_TE = fields.Float(string='Số thu trước nguyên tệ', help='Số thu trước nguyên tệ')
    SO_CON_PHAI_THU = fields.Float(string='Số còn phải thu/còn phải trả', help='Số còn phải thu/còn phải trả')
    SO_CON_PHAI_THU_NGUYEN_TE = fields.Float(string='Số còn phải thu/còn phải trả nguyên tệ', help='Số còn phải thu/còn phải trả nguyên tệ')
    HAN_THANH_TOAN = fields.Date(string='Hạn thanh toán')
    GIA_TRI_HOA_DON_NGUYEN_TE = fields.Float(string='Giá trị hóa đơn nguyên tệ', help='Giá trị hóa đơn nguyên tệ')
    GIA_TRI_HOA_DON = fields.Float(string='Giá trị hóa đơn')
    SO_CON_PHAI_TRA = fields.Float(string='Số còn phải trả')
    SO_TRA_TRUOC = fields.Float(string='Số trả trước')


    @api.model
    def create(self, values):
        master = self.env['account.ex.so.du.tai.khoan.chi.tiet'].search([('id', '=', values.get('SO_DU_TAI_KHOAN_CHI_TIET_ID'))])
        if master:
            if master.currency_id.MA_LOAI_TIEN == 'VND':
                values['SO_THU_TRUOC_NGUYEN_TE'] = values.get('SO_THU_TRUOC')
                values['SO_CON_PHAI_THU_NGUYEN_TE'] = values.get('SO_CON_PHAI_THU')
                values['GIA_TRI_HOA_DON_NGUYEN_TE'] = values.get('GIA_TRI_HOA_DON')
        result = super(ACCOUNT_EX_SDTKCT_THEO_HOA_DON, self).create(values)
        return result