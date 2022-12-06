# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class SO_CCDC(models.Model):
    _name = 'so.ccdc'
    _description = 'Sổ công cụ dụng cụ'

    name = fields.Char()
    line_ids = fields.One2many('so.ccdc.chi.tiet', 'SO_CCDC_ID')

class SO_CCDC_CHI_TIET(models.Model):
    _name = 'so.ccdc.chi.tiet'
    _description = 'Sổ công cụ dụng cụ chi tiết'

    name = fields.Char(string="name")
    SO_CCDC_ID = fields.Many2one('so.ccdc', ondelete="cascade")
    ID_CHUNG_TU = fields.Integer(string='Id chứng từ', help='Id chứng từ', required=True)
    MODEL_CHUNG_TU = fields.Char(string='Model chứng từ', help='Model chứng từ', required=True)
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='RefType')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='RefNo')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='RefDate')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='PostedDate', required=True)
    DIEN_GIAI_CHUNG = fields.Char(string='Diễn giải chứng từ', help='JournalMemo')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Description')
    SO_KY_PHAN_BO_GHI_TANG = fields.Integer(string='Số kỳ phân bổ ghi tăng', help='IncrementAllocationTime')
    SO_KY_PHAN_BO_GHI_GIAM = fields.Integer(string='Số kỳ phân bổ ghi giảm', help='DecrementAllocationTime')
    SO_LUONG_GHI_TANG = fields.Float(string='Số lượng ghi tăng', help='IncrementQuantity', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_GHI_GIAM = fields.Float(string='Số lượng ghi giảm', help='DecrementQuantity', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_TIEN_GHI_TANG = fields.Float(string='Số tiền ghi tăng', help='IncrementAmount')
    SO_TIEN_GHI_GIAM = fields.Float(string='Số tiền ghi giảm', help='DecrementAmount')
    SO_TIEN_PHAN_BO = fields.Float(string='Số tiền phân bổ', help='AllocationAmount')
    SO_TIEN_PHAN_BO_HANG_KY = fields.Float(string='Số tiền phân bổ hàng kỳ', help='TermlyAllocationAmount')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='BranchID', default=lambda self: self.get_chi_nhanh(), readonly=True)
    THU_TU_TRONG_CHUNG_TU = fields.Integer(string='Thứ tự trong chứng từ', help='SortOrder')
    LOAI_CCDC_ID = fields.Many2one('danh.muc.loai.cong.cu.dung.cu', string='Loại ccdc', help='SupplyCategoryID')
    DOI_TUONG_PHAN_BO_ID = fields.Many2one('danh.muc.to.chuc', string='Đối tượng phân bổ', help='OrganizationUnitID')

    
    @api.model
    def create(self, values):
        result = super(SO_CCDC_CHI_TIET, self).create(values)
    
        return result
    