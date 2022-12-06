# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.exceptions import ValidationError

class TONG_HOP_CHI_PHI_TRA_TRUOC(models.Model):
    _name = 'tong.hop.chi.phi.tra.truoc'
    _description = ''
    _inherit = ['mail.thread']
    MA_CHI_PHI_TRA_TRUOC = fields.Char(string='Mã CP trả trước', help='Mã chi phí trả trước')
    TEN_CHI_PHI_TRA_TRUOC = fields.Char(string='Tên CP trả trước', help='Tên chi phí trả trước')
    NGAY_GHI_NHAN = fields.Date(string='Ngày ghi nhận', help='Ngày ghi nhận',default=fields.Datetime.now)
    SO_TIEN = fields.Monetary(string='Số tiền', help='Số tiền', currency_field='base_currency_id')
    SO_TIEN_DA_PHAN_BO = fields.Monetary(string='Số tiền đã PB', help='Số tiền đã phân bổ', currency_field='base_currency_id')

    SO_KY_PHAN_BO = fields.Integer(string='Số kỳ phân bổ', help='Số kỳ phân bổ')
    SO_KY_DA_PHAN_BO = fields.Integer(string='Số kỳ đã PB', help='Số kỳ đã PB')
    SO_TIEN_PB_HANG_KY = fields.Monetary(string='Số tiền PB hàng kỳ', help='Số tiền PB hàng kỳ', currency_field='base_currency_id')
    TK_CHO_PHAN_BO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chờ phân bổ', help='TK chờ phân bổ')
    NGUNG_PHAN_BO = fields.Boolean(string='Ngừng phân bổ', help='Ngừng phân bổ')
    SO_DA_PB = fields.Float(string='Số đã phân bổ', help='Số đã phân bổ',digits=decimal_precision.get_precision('Product Price'))
    SO_CON_LAI = fields.Float(string='Số còn lại', help='Số còn lại',digits=decimal_precision.get_precision('Product Price'))
    name = fields.Char(string='Name', help='Name',related='MA_CHI_PHI_TRA_TRUOC',store=True, oldname='NAME')

    TONG_HOP_CHI_PHI_TRA_TRUOC_TAP_HOP_CHUNG_TU_IDS = fields.One2many('tong.hop.chi.phi.tra.truoc.tap.hop.chung.tu', 'CHI_PHI_TRA_TRUOC_ID', string='Chi phí trả trước tập hợp chứng từ')
    TONG_HOP_CHI_PHI_TRA_TRUOC_THIET_LAP_PHAN_BO_IDS = fields.One2many('tong.hop.chi.phi.tra.truoc.thiet.lap.phan.bo', 'CHI_PHI_TRA_TRUOC_ID', string='Chi phí trả trước thiết lập phân bổ')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')

  
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

    @api.model
    def default_get(self, fields):
        rec = super(TONG_HOP_CHI_PHI_TRA_TRUOC, self).default_get(fields)
        tk_cho_phan_bo = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like', '242%')], limit=1)
        if tk_cho_phan_bo:
            rec['TK_CHO_PHAN_BO_ID'] = tk_cho_phan_bo.id
        rec['SO_KY_PHAN_BO'] = 2
        rec['LOAI_CHUNG_TU'] = self.get_context('default_LOAI_CHUNG_TU')
        return rec

    @api.onchange('SO_TIEN','SO_KY_PHAN_BO')
    def _onchange_SO_TIEN(self):
        self.SO_TIEN_PB_HANG_KY = self.SO_TIEN/self.SO_KY_PHAN_BO

    
    # @api.model
    # def create(self, values):
    #     tong_ty_le = 0
    #     if values.get('TONG_HOP_CHI_PHI_TRA_TRUOC_THIET_LAP_PHAN_BO_IDS'):
    #         for tl in values.get('TONG_HOP_CHI_PHI_TRA_TRUOC_THIET_LAP_PHAN_BO_IDS'):
    #             tong_ty_le += tl[2].get('TY_LE_PB')
    #         if tong_ty_le < 100:
    #             raise ValidationError("Tổng tỷ lệ phân bổ phải lớn hơn 100%")
    #     else:
    #         raise ValidationError("Bạn phải nhập thiết lập phân bổ!")
    #     if values.get('SO_TIEN') <= 0:
    #         raise ValidationError("Số tiền phải lớn hơn 0")
    #     result = super(TONG_HOP_CHI_PHI_TRA_TRUOC, self).create(values)
    #     return result
    


