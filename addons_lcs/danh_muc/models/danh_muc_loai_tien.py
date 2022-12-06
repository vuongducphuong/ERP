# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision
from num2words import num2words

class DANH_MUC_LOAI_TIEN(models.Model):
    _inherit = 'res.currency'
    _description = 'Danh mục loại tiền'
    _order = "MA_LOAI_TIEN"

    MA_LOAI_TIEN = fields.Char(string='Mã (*)', help='Mã loại tiền', related='name', store=True, required=True)
    TEN_LOAI_TIEN = fields.Char(string='Tên (*)', help='Tên loại tiền', required=True)
    PHEP_TINH_QUY_DOI = fields.Selection([('NHAN', '*'), ('CHIA', '/'), ], string='Phép tính quy đổi', help='Phép tính quy đổi',default='NHAN', required=True)
    TY_GIA_QUY_DOI = fields.Float(string='Tỷ giá quy đổi', help='Tỷ giá quy đổi', required=True)
    TK_TIEN_MAT_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK tiền mặt', help='Tài khoản tiền mặt')
    TK_TIEN_GUI_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK tiền gửi', help='Tài khoản tiền gửi')
    
    KY_HIEU_BAT_DAU = fields.Char(string='Ký hiệu bắt đầu', help='Ký hiệu bắt đầu')
    DOC_TEN_LOAI_TIEN = fields.Char(string='Đọc tên loại tiền', help='Đọc tên loại tiền', related='currency_unit_label', store=True)
    DOC_PHAN_CACH_THAP_PHAN = fields.Char(string='Đọc phân cách thập phân', help='Đọc phân cách thập phân')
    DOC_SO_TIEN_SAU_THAP_PHAN = fields.Char(string='Đọc số tiền sau thập phân', help='Đọc số tiền sau thập phân', related='currency_subunit_label', store=True)
    TY_LE_CHUYEN_DOI = fields.Float(string='Tỷ lệ chuyển đổi', help='Tỷ lệ chuyển đổi')
    KY_HIEU_KET_THUC = fields.Char(string='Ký hiệu kết thúc', help='Ký hiệu kết thúc')


    KY_HIEU_BAT_DAU_MAC_DINH = fields.Char(string='Ký hiệu bắt đầu mặc định', help='Ký hiệu bắt đầu')
    DOC_TEN_LOAI_TIEN_MAC_DINH = fields.Char(string='Đọc tên loại tiền mặc định', help='Đọc tên loại tiền')
    DOC_PHAN_CACH_THAP_PHAN_MAC_DINH = fields.Char(string='Đọc phân cách thập phân mặc định', help='Đọc phân cách thập phân')
    DOC_SO_TIEN_SAU_THAP_PHAN_MAC_DINH = fields.Char(string='Đọc số tiền sau thập phân mặc định', help='Đọc số tiền sau thập phân')
    TY_LE_CHUYEN_DOI_MAC_DINH = fields.Float(string='Tỷ lệ chuyển đổi mặc định', help='Tỷ lệ chuyển đổi')
    KY_HIEU_KET_THUC_MAC_DINH = fields.Char(string='Ký hiệu kết thúc', help='Ký hiệu kết thúc')

    KY_HIEU_BAT_DAU_TIENG_ANH = fields.Char(string='Ký hiệu bắt đầu tieng anh', help='Ký hiệu bắt đầu tieng anh')
    DOC_TEN_LOAI_TIEN_TIENG_ANH = fields.Char(string='Đọc tên loại tiền tieng anh', help='Đọc tên loại tiền tieng anh')
    DOC_PHAN_CACH_THAP_PHAN_TIENG_ANH = fields.Char(string='Đọc phân cách thập phân tiếng anh', help='Đọc phân cách thập phân tiếng anh')
    DOC_SO_TIEN_SAU_THAP_PHAN_TIENG_ANH = fields.Char(string='Đọc số tiền sau thập phân tiếng anh', help='Đọc số tiền sau thập phân tiếng anh')
    TY_LE_CHUYEN_DOI_TIENG_ANH = fields.Float(string='Tỷ lệ chuyển đổi tiếng anh', help='Tỷ lệ chuyển đổi tiếng anh')
    KY_HIEU_KET_THUC_TIENG_ANH = fields.Char(string='Ký hiệu kết thúc tiếng anh', help='Ký hiệu kết thúc tiếng anh')

    KY_HIEU_BAT_DAU_TIENG_ANH_MAC_DINH = fields.Char(string='Ký hiệu bắt đầu tieng anh mặc định', help='Ký hiệu bắt đầu tieng anh')
    DOC_TEN_LOAI_TIEN_TIENG_ANH_MAC_DINH = fields.Char(string='Đọc tên loại tiền tieng anh mặc định', help='Đọc tên loại tiền tieng anh')
    DOC_PHAN_CACH_THAP_PHAN_TIENG_ANH_MAC_DINH = fields.Char(string='Đọc phân cách thập phân tiếng anh mặc định', help='Đọc phân cách thập phân tiếng anh')
    DOC_SO_TIEN_SAU_THAP_PHAN_TIENG_ANH_MAC_DINH = fields.Char(string='Đọc số tiền sau thập phân tiếng anh mặc định', help='Đọc số tiền sau thập phân tiếng anh')
    TY_LE_CHUYEN_DOI_TIENG_ANH_MAC_DINH = fields.Float(string='Tỷ lệ chuyển đổi tiếng anh mặc định', help='Tỷ lệ chuyển đổi tiếng anh')
    KY_HIEU_KET_THUC_TIENG_ANH_MAC_DINH = fields.Char(string='Ký hiệu kết thúc tiếng anh mặc định', help='Ký hiệu kết thúc tiếng anh')

    NHAP_SO_TIEN = fields.Float(string='Nhập số tiền', help='Nhập số tiền', store=False, )
    DOC_SO_TIEN_BANG_CHU_TIENG_VIET = fields.Char(string='Đọc số tiền bằng chữ tiếng việt', help='Đọc số tiền bằng chữ tiếng việt', store=False)
    DOC_SO_TIEN_BANG_CHU_TIENG_ANH = fields.Char(string='Đọc số tiền bằng chữ tiếng anh', help='Đọc số tiền bằng chữ tiếng anh', store=False)
    LA_TIEN_CO_SO = fields.Boolean(compute='_compute_LA_TIEN_CO_SO', store=True)
    symbol = fields.Char(help="Currency sign, to be used when printing amounts.", default='_', required=True)
    DANH_MUC_MENH_GIA_LOAI_TIEN_IDS = fields.One2many('danh.muc.menh.gia.loai.tien', 'currency_id', string='Mệnh giá loại tiền', copy=True)

    _sql_constraints = [
        ('MA_LOAI_TIEN_uniq', 'unique ("MA_LOAI_TIEN")', 'Mã loại tiền <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]

    @api.model
    def create(self, values):
        if not values.get('MA_LOAI_TIEN'):
            raise ValidationError("<Mã > không được bỏ trống.")
        elif not values.get('TEN_LOAI_TIEN'):
            raise ValidationError("<Tên > không được bỏ trống.")
        elif not values.get('TY_GIA_QUY_DOI'):
            raise ValidationError("<Tỷ giá quy đổi> phải lớn hơn 0 .")
        result = super(DANH_MUC_LOAI_TIEN, self).create(values)

        return result
    
    @api.depends('TY_GIA_QUY_DOI')
    def _compute_LA_TIEN_CO_SO(self):
        for record in self:
            record.LA_TIEN_CO_SO = (record.TY_GIA_QUY_DOI == 1.0)

    @api.model
    def default_get(self, fields):
        rec = super(DANH_MUC_LOAI_TIEN, self).default_get(fields)
        rec['TK_TIEN_MAT_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '1111')],limit=1).id
        rec['TK_TIEN_GUI_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '1121')],limit=1).id
        return rec

    @api.onchange('NHAP_SO_TIEN','DOC_TEN_LOAI_TIEN','TY_LE_CHUYEN_DOI','DOC_PHAN_CACH_THAP_PHAN','DOC_SO_TIEN_SAU_THAP_PHAN')
    def _onchange_NHAP_SO_TIEN(self):
        if (self.NHAP_SO_TIEN > 0):
            # Đọc tiếng Việt
            self.DOC_SO_TIEN_BANG_CHU_TIENG_VIET = self.doc_so_tien_tieng_viet(self.NHAP_SO_TIEN)

            # In English
            self.DOC_SO_TIEN_BANG_CHU_TIENG_ANH = num2words(self.NHAP_SO_TIEN).capitalize()
            if self.DOC_TEN_LOAI_TIEN_TIENG_ANH:
                self.DOC_SO_TIEN_BANG_CHU_TIENG_ANH += ' ' + self.DOC_TEN_LOAI_TIEN_TIENG_ANH

    def doc_so_tien_tieng_viet(self, so_tien):
        from decimal import Decimal
        result = ''
        if (so_tien > 0):
            whole = int(so_tien)
            frac = float(Decimal(str(so_tien))%1)
            # frac = so_tien - whole
            if whole >= 1:
                result = helper.Obj.vietbangchu(int(whole))
                if self.DOC_TEN_LOAI_TIEN:
                    result += ' ' + self.DOC_TEN_LOAI_TIEN
            if frac > 0:
                tien_sau_thap_phan = frac * self.TY_LE_CHUYEN_DOI if self.TY_LE_CHUYEN_DOI else 0
                whole_thap_phan = int(tien_sau_thap_phan)
                frac_thap_phan = float(Decimal(tien_sau_thap_phan)%1) * 10
                if self.DOC_PHAN_CACH_THAP_PHAN:
                    result += ' ' + self.DOC_PHAN_CACH_THAP_PHAN + ' '
                result += helper.Obj.vietbangchu(int(whole_thap_phan), False)
                if frac_thap_phan >= 1:
                    result += ' phẩy ' + helper.Obj.vietbangchu(frac_thap_phan, False)
                if self.DOC_SO_TIEN_SAU_THAP_PHAN:
                    result += ' ' + self.DOC_SO_TIEN_SAU_THAP_PHAN
            else:
                result += ' chẵn.'
        return result