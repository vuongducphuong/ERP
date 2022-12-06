# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class ACCOUNT_EX_DOI_CHIEU_NGAN_HANG(models.Model):
    _name = 'account.ex.doi.chieu.ngan.hang'
    _description = ''
    _auto = False

    TK_NGAN_HANG_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='TK ngân hàng', help='Tài khoản ngân hàng')
    TEN_NH = fields.Char(string='Tên ngân hàng', help='Tên ngân hàng')
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày',default=fields.Datetime.now)
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày',default=fields.Datetime.now)
    SO_DU_DAU_KY_NGAY = fields.Float(string='Số dư đầu kỳ ngày', help='Số dư đầu kỳ ngày',digits=decimal_precision.get_precision('VND'))
    TONG_TIEN_THU_DOI_CHIEU_TRONG_KY = fields.Float(string='Tổng tiền thu đối chiếu trong kỳ', help='Tổng tiền thu đối chiếu trong kỳ',digits=decimal_precision.get_precision('VND'))
    TONG_TIEN_CHI_DOI_CHIEU_TRONG_KY = fields.Float(string='Tổng tiền chi đối chiếu trong kỳ', help='Tổng tiền chi đối chiếu trong kỳ',digits=decimal_precision.get_precision('VND'))
    SO_DU_CUOI_KY_SAU_DOI_CHIEU = fields.Float(string='Số dư cuối kỳ sau đối chiếu', help='Số dư cuối kỳ sau đối chiếu',digits=decimal_precision.get_precision('VND'))
    SO_DU_CUOI_KY_TREN_SO_NGAN_HANG = fields.Float(string='Số dư cuối kỳ trên sổ ngân hàng', help='Số dư cuối kỳ trên sổ ngân hàng',digits=decimal_precision.get_precision('VND'))
    CHENH_LENH = fields.Float(string='Chênh lệnh', help='Chênh lệnh',digits=decimal_precision.get_precision('VND'))
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    @api.model
    def default_get(self, fields_list):
      result = super(ACCOUNT_EX_DOI_CHIEU_NGAN_HANG, self).default_get(fields_list)
      result['TK_NGAN_HANG_ID'] = self.env['danh.muc.tai.khoan.ngan.hang'].search([],limit=1).id
      result['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')],limit=1).id
      return result

    ACCOUNT_EX_DOI_CHIEU_NGAN_HANG_CHUNG_TU_THU_TIEN_IDS = fields.One2many('account.ex.doi.chieu.ngan.hang.chung.tu.thu.tien', 'CHUNG_TU_THU_TIEN_CHI_TIET_ID', string='Đối chiếu ngân hàng chứng từ thu tiền')
    ACCOUNT_EX_DOI_CHIEU_NGAN_HANG_CHUNG_TU_CHI_TIEN_IDS = fields.One2many('account.ex.doi.chieu.ngan.hang.chung.tu.chi.tien', 'CHUNG_TU_CHI_TIET_ID', string='Đối chiếu ngân hàng chứng từ chi tiền')

    @api.onchange('TK_NGAN_HANG_ID')
    def update_TEN_NH(self):
        self.TEN_NH = self.TK_NGAN_HANG_ID.CHI_NHANH