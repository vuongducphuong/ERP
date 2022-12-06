# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SALE_EX_THU_TIEN_KHACH_HANG_CHI_TIET(models.Model):
    _name = 'sale.ex.thu.tien.khach.hang.chi.tiet'
    _description = ''
    _auto = False

    CHON = fields.Boolean(string='Chọn', help='Chọn')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    HAN_THANH_TOAN = fields.Date(string='Hạn thanh toán', help='Hạn thanh toán')
    SO_PHAI_THU = fields.Float(string='Số phải thu', help='Số phải thu')
    SO_CHUA_THU = fields.Float(string='Số chưa thu', help='Số chưa thu')
    SO_THU = fields.Float(string='Số thu', help='Số thu')
    TK_PHAI_THU = fields.Char(string='Tk phải thu', help='Tk phải thu')
    DIEU_KHOAN_THANH_TOAN = fields.Char(string='Điều khoản thanh toán', help='Điều khoản thanh toán')
    TY_LE_CK = fields.Float(string='Tỷ lệ ck', help='Tỷ lệ ck')
    TIEN_CHIET_KHAU = fields.Float(string='Tiền chiết khấu', help='Tiền chiết khấu')
    TK_CHIET_KHAU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk chiết khấu', help='Tk chiết khấu')
    THU_TIEN_KHACH_HANG_ID = fields.Many2one('sale.ex.thu.tien.khach.hang', string='Thu tiền khách hàng', help='Thu tiền khách hàng')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    @api.model
    def default_get(self, fields_list):
      result = super(SALE_EX_THU_TIEN_KHACH_HANG_CHI_TIET, self).default_get(fields_list)
      result['TK_CHIET_KHAU_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=like','635%')]).ids
      return result

    @api.onchange('CHON')
    def update_CHON(self):
        if  self.CHON == True:
            if self.SO_THU == 0:
                self.SO_THU = self.SO_CHUA_THU
        if self.CHON == False:
            self.SO_THU = 0

    @api.onchange('SO_THU')
    def update_SO_THU(self):
        if self.SO_THU > 0:
            self.CHON = True

    @api.onchange('TY_LE_CK')
    def update_TY_LE_CK(self):
        self.TIEN_CHIET_KHAU = (self.TY_LE_CK*self.SO_THU)/100
