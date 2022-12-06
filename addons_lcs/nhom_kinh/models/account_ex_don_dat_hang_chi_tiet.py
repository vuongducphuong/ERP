# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ACCOUNT_EX_DON_DAT_HANG_CHI_TIET(models.Model):
    _inherit = 'account.ex.don.dat.hang.chi.tiet'

    CHIEU_DAI = fields.Float(string='Chiều dài', help='Chiều dài (mm)', digits=decimal_precision.get_precision('KICH_THUOC'))
    CHIEU_RONG = fields.Float(string='Chiều rộng', help='Chiều rộng (mm)', digits=decimal_precision.get_precision('KICH_THUOC'))
    CHIEU_CAO = fields.Float(string='Độ dầy', help='Độ dầy (mm)', digits=decimal_precision.get_precision('KICH_THUOC'))
    LUONG = fields.Float(string='Lượng', help='Số lượng tính theo đơn vị cái', digits=decimal_precision.get_precision('SO_LUONG'), default=1)
    SO_LUONG_GIA_CONG_1 = fields.Float(string='Mét dài', digits=decimal_precision.get_precision('SO_LUONG'), compute='_compute_SO_LUONG_GIA_CONG_1', )
    SO_LUONG_GIA_CONG_2 = fields.Float(string='Khoan', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_GIA_CONG_3 = fields.Float(string='Khoét', digits=decimal_precision.get_precision('SO_LUONG'))

    DON_GIA_GIA_CONG_1 = fields.Float(string='Giá mài', digits=decimal_precision.get_precision('DON_GIA'))
    DON_GIA_GIA_CONG_2 = fields.Float(string='Giá khoan', digits=decimal_precision.get_precision('DON_GIA'))
    DON_GIA_GIA_CONG_3 = fields.Float(string='Giá khoét', digits=decimal_precision.get_precision('DON_GIA'))

    THANH_TIEN_GIA_CONG_1 = fields.Monetary(string='Tiền mài', currency_field='base_currency_id', compute='_compute_THANH_TIEN_GIA_CONG_1', store=True)
    THANH_TIEN_GIA_CONG_2 = fields.Monetary(string='Tiền khoan', currency_field='base_currency_id', compute='_compute_THANH_TIEN_GIA_CONG_2', store=True)
    THANH_TIEN_GIA_CONG_3 = fields.Monetary(string='Tiền khoét', currency_field='base_currency_id', compute='_compute_THANH_TIEN_GIA_CONG_3', store=True)
    THANH_TIEN_GIA_CONG = fields.Monetary(string='Thành tiền gia công', currency_field='base_currency_id', compute='_compute_THANH_TIEN_GIA_CONG', store=True)
    
    THANH_TIEN_TONG_CONG = fields.Monetary(string='Tổng', currency_field='base_currency_id', compute='_compute_THANH_TIEN_TONG_CONG', store=True)

    @api.multi
    @api.depends('CHIEU_DAI','CHIEU_RONG', 'LUONG')
    def _compute_SO_LUONG_GIA_CONG_1(self):
        for record in self:
            record.SO_LUONG_GIA_CONG_1 = (record.CHIEU_DAI + record.CHIEU_RONG) * 2 * record.LUONG / 1000 # Tính ra mét

    @api.onchange('CHIEU_DAI','CHIEU_RONG', 'LUONG')
    def onchange_kich_thuoc(self):
        if self.MA_HANG_ID:
            sl = self.MA_HANG_ID.tinh_so_luong_theo_cong_thuc(self.CHIEU_DAI, self.CHIEU_RONG, 0, 0, self.LUONG)
            if sl is not None:
                self.SO_LUONG = sl

    @api.multi
    @api.depends('SO_LUONG_GIA_CONG_1','DON_GIA_GIA_CONG_1')
    def _compute_THANH_TIEN_GIA_CONG_1(self):
        for record in self:
            record.THANH_TIEN_GIA_CONG_1 = record.SO_LUONG_GIA_CONG_1 * record.DON_GIA_GIA_CONG_1
    
    @api.multi
    @api.depends('SO_LUONG_GIA_CONG_2','DON_GIA_GIA_CONG_2')
    def _compute_THANH_TIEN_GIA_CONG_2(self):
        for record in self:
            record.THANH_TIEN_GIA_CONG_2 = record.SO_LUONG_GIA_CONG_2 * record.DON_GIA_GIA_CONG_2
    
    @api.multi
    @api.depends('SO_LUONG_GIA_CONG_3','DON_GIA_GIA_CONG_3')
    def _compute_THANH_TIEN_GIA_CONG_3(self):
        for record in self:
            record.THANH_TIEN_GIA_CONG_3 = record.SO_LUONG_GIA_CONG_3 * record.DON_GIA_GIA_CONG_3

    @api.multi
    @api.depends('THANH_TIEN_GIA_CONG_1','THANH_TIEN_GIA_CONG_2','THANH_TIEN_GIA_CONG_3')
    def _compute_THANH_TIEN_GIA_CONG(self):
        for record in self:
            record.THANH_TIEN_GIA_CONG = record.THANH_TIEN_GIA_CONG_1 + record.THANH_TIEN_GIA_CONG_2 + record.THANH_TIEN_GIA_CONG_3

    @api.multi
    @api.depends('THANH_TIEN_GIA_CONG','THANH_TIEN', 'TIEN_THUE_GTGT')
    def _compute_THANH_TIEN_TONG_CONG(self):
        for record in self:
            record.THANH_TIEN_TONG_CONG = record.THANH_TIEN_GIA_CONG + record.THANH_TIEN + record.TIEN_THUE_GTGT
    
    