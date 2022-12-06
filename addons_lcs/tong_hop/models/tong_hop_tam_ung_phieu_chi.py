# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class ACCOUNT_EX_TAM_UNG_PHIEU_CHI(models.Model):
    _name = 'account.ex.tam.ung.phieu.chi'
    _description = ''
    _inherit = ['mail.thread']
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk nợ', help='Tk nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk có', help='Tk có')
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền')
    QUYET_TOAN_LAN_NAY = fields.Float(string='Quyết toán lần này', help='Quyết toán lần này')
    QUYET_TOAN_LAN_NAY_QD = fields.Float(string='Quyết toán lần này QĐ', help='Quyết toán lần này quy đổi')
    
    CHUNG_TU_TAM_UNG_ID = fields.Many2one('account.ex.chung.tu.nghiep.vu.khac', string='Chứng từ tạm ứng', help='Chứng từ tạm ứng', ondelete='cascade')
	
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

