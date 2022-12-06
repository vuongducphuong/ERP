# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class PURCHASE_EX_CHUNG_TU_BU_TRU_CONG_NO_KET_QUA(models.Model):
    _name = 'purchase.ex.chung.tu.bu.tru.cong.no.ket.qua'
    _description = 'Bù trừ công nợ'
    _inherit = ['mail.thread']
    DOI_TUONG = fields.Char(string='Đối tượng', help='Đối tượng')
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng')
    LY_DO = fields.Char(string='Lý do', help='Lý do')
    TK_PHAI_THU = fields.Char(string='TK phải thu', help='Tài khoản phải thu')
    TK_PHAI_TRA = fields.Char(string='TK phải trả', help='Tài khoản phải trả')
    NGAY_BU_TRU = fields.Char(string='Ngày bù trừ', help='Ngày bù trừ')
    LOAI_TIEN = fields.Char(string='Loại tiền', help='Loại tiền')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán',required=True)
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',default=fields.Datetime.now,required=True)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ', auto_num='purchase_ex_chung_tu_bu_tru_cong_no_ket_qua_SO_CHUNG_TU')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')

    PURCHASE_EX_CHUNG_TRU_BU_TRU_CONG_NO_KET_QUA_HACH_TOAN_IDS = fields.One2many('purchase.ex.chung.tru.bu.tru.cong.no.ket.qua.hach.toan', 'CHUNG_TU_BU_TRU_CONG_NO_KET_QUA_ID', string='Chứng trừ bù trừ công nợ kết quả hạch toán ')
    PURCHASE_EX_CHUNG_TU_BU_TRU_CONG_NO_KET_QUA_CTCN_IDS = fields.One2many('purchase.ex.chung.tu.bu.tru.cong.no.ket.qua.ctcn', 'CHUNG_TU_BU_TRU_CONG_NO_KET_QUA_ID', string='Chứng từ bù trừ công nợ kết quả ctcn')

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ' , store=True)
	
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    @api.model
    def default_get(self, fields):
        rec = super(PURCHASE_EX_CHUNG_TU_BU_TRU_CONG_NO_KET_QUA, self).default_get(fields)
        rec['LOAI_CHUNG_TU'] = 4014
        return rec



