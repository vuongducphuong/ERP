# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ACCOUNT_EX_CHI_TIET_THEO_NV_DV_CT_DH_HD(models.Model):
    _name = 'account.ex.chi.tiet.theo.nv.dv.ct.dh.hd'
    _description = ''
    _inherit = ['mail.thread']
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên', help='Nhân viên')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    DON_MUA_HANG_ID = fields.Many2one('purchase.ex.don.mua.hang', string='Đơn mua hàng', help='Đơn mua hàng')
    HOP_DONG_MUA_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang', string='Hợp đồng mua', help='Hợp đồng mua')
    DU_NO = fields.Float(string='Dư nợ', help='Dư nợ',digits=decimal_precision.get_precision('Product Price'))
    DU_CO = fields.Float(string='Dư có', help='Dư có',digits=decimal_precision.get_precision('Product Price'))
    CONG_NO_NHA_CUNG_CAP_ID = fields.Many2one('account.ex.cong.no.nha.cung.cap', string='Công nợ nhà cung cấp', help='Công nợ nhà cung cấp', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')