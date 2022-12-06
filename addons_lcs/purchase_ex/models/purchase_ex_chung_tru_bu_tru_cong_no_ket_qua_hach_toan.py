# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class PURCHASE_EX_CHUNG_TRU_BU_TRU_CONG_NO_KET_QUA_HACH_TOAN(models.Model):
    _name = 'purchase.ex.chung.tru.bu.tru.cong.no.ket.qua.hach.toan'
    _description = ''
    _inherit = ['mail.thread']
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Char(string='TK nợ', help='Tài khoản nợ')
    TK_CO_ID = fields.Char(string='TK có', help='Tài khoản có')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('Product Price'))
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên', help='Nhân viên')
    KHOAN_MUC_CP = fields.Char(string='Khoản mục CP', help='Khoản mục chi phí')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    CHUNG_TU_BU_TRU_CONG_NO_KET_QUA_ID = fields.Many2one('purchase.ex.chung.tu.bu.tru.cong.no.ket.qua', string='Chứng từ bù trừ công nợ kết quả ', help='Chứng từ bù trừ công nợ kết quả ', ondelete='cascade')