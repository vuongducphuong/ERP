# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ACCOUNT_EX_CONG_NO_NHA_CUNG_CAP(models.Model):
    _name = 'account.ex.cong.no.nha.cung.cap'
    _description = ''

    SO_TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Số tài khoản', help='Số tài khoản')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Mã nhà cung cấp', help='Mã nhà cung cấp')
    TEN_NHA_CUNG_CAP = fields.Char(string='Tên nhà cung cấp', help='Tên nhà cung cấp')
    DU_NO = fields.Float(string='Dư nợ', help='Dư nợ',digits=decimal_precision.get_precision('Product Price'))
    DU_CO = fields.Float(string='Dư có', help='Dư có',digits=decimal_precision.get_precision('Product Price'))
    SO_DU_BAN_DAU_ID = fields.Many2one('account.ex.nhap.so.du.ban.dau', string='Số dư ban đầu', help='Số dư ban đầu', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    DU_NO_NGUYEN_TE = fields.Float(string='Dư nợ nguyên tệ', help='Dư nợ nguyên tệ')
    DU_CO_NGUYEN_TE = fields.Float(string='Dư có nguyên tệ', help='Dư có nguyên tệ')
    CHI_TIET_SO_DU = fields.Char()
    CHI_TIET_THEO_DOI_TUONG = fields.Integer(string='Chi tiết theo đối tượng', help='Chi tiết theo đối tượng')
    LOAI_DOI_TUONG = fields.Integer(string='Loại đối tượng', help='Loại đối tượng')

    ACCOUNT_EX_CHI_TIET_THEO_HOA_DON_IDS = fields.One2many('account.ex.chi.tiet.theo.hoa.don', 'CONG_NO_NHA_CUNG_CAP_ID', string='Chi tiết theo hóa đơn')
    ACCOUNT_EX_CHI_TIET_THEO_NV_DV_CT_DH_HD_IDS = fields.One2many('account.ex.chi.tiet.theo.nv.dv.ct.dh.hd', 'CONG_NO_NHA_CUNG_CAP_ID', string='chi tiết theo nv dv ct đh hd')