# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class PURCHASE_EX_DOI_TRU_CHUNG_TU_NHIEU_DOI_TUONG(models.Model):
    _name = 'purchase.ex.doi.tru.chung.tu.nhieu.doi.tuong'
    _description = ''
    _auto = False

    TAI_KHOAN_PHAI_TRA_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản phải trả', help='Tài khoản phải trả')
    NGAY_DOI_TRU = fields.Date(string='Ngày đối trừ', help='Ngày đối trừ',default=fields.Datetime.now)
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    IS_TY_GIA = fields.Boolean(string='Loại tiền', help='Loại tiền',default=True)
    STEP = fields.Integer(string='bước', help='bước',store=False)
    PURCHASE_EX_DOI_TRU_CHUNG_TU_NHIEU_DOI_TUONG_CHI_TIET_IDS = fields.One2many('purchase.ex.doi.tru.chung.tu.nhieu.doi.tuong.chi.tiet', 'DOI_TRU_CHUNG_TU_NHIEU_DOI_TUONG_CHI_TIET_ID', string='Đối trừ chứng từ nhiều đối tượng chi tiết')


    @api.model
    def default_get(self, fields):
        rec = super(PURCHASE_EX_DOI_TRU_CHUNG_TU_NHIEU_DOI_TUONG, self).default_get(fields)
        loai_tien = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', 'VND')],limit=1)
        tai_khoan_phai_tra = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '331')],limit=1)
        if loai_tien:
            rec['currency_id'] =loai_tien.id
        if tai_khoan_phai_tra:
            rec['TAI_KHOAN_PHAI_TRA_ID'] = tai_khoan_phai_tra.id
        rec['STEP'] =1
        return rec

    @api.onchange('currency_id')
    def update_loai_tien(self):
        if self.currency_id.MA_LOAI_TIEN == 'VND':
            self.IS_TY_GIA = False
        else:
            self.IS_TY_GIA =True