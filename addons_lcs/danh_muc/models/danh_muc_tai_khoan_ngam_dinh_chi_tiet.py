# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper

class DANH_MUC_TAI_KHOAN_NGAM_DINH_CHI_TIET(models.Model):
    _name = 'danh.muc.tai.khoan.ngam.dinh.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    TEN_COT = fields.Char(string='Tên cột', help='Tên cột')
    TEN_COT_CHUYEN_DOI = fields.Char(string='Tên cột', help='Tên cột')#, compute='_compute_TEN_COT_CHUYEN_DOI', store=True)
    LOC_TAI_KHOAN = fields.Many2many('danh.muc.he.thong.tai.khoan', 'he_thong_tai_khoan_tai_khoan_ngam_dinh_rel',string='Lọc tài khoản', help='Lọc tài khoản')
    TK_NGAM_DINH_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK ngầm định', help='Tk ngầm định')
    name = fields.Char(related='DANH_MUC_TAI_KHOAN_NGAM_DINH_ID.name',store=True)
    DANH_MUC_TAI_KHOAN_NGAM_DINH_ID = fields.Many2one('danh.muc.tai.khoan.ngam.dinh', string='Tài khoản ngầm định', help='Tài khoản ngầm định', ondelete='cascade')
    LOAI_CHUNG_TU = fields.Integer(related='DANH_MUC_TAI_KHOAN_NGAM_DINH_ID.LOAI_CHUNG_TU',store=True)
    NHOM_CHUNG_TU = fields.Integer()

    _sql_constraints = [
	    ('RefType_VoucherTypt_ColumnName_uniq', 'unique ("LOAI_CHUNG_TU","NHOM_CHUNG_TU","TEN_COT_CHUYEN_DOI")', 'Tài khoản ngầm định đã tồn tại!'),
	]

    # @api.depends('TEN_COT')
    # def _compute_TEN_COT_CHUYEN_DOI(self):
    #     for record in self:
    #         record.TEN_COT_CHUYEN_DOI = helper.Obj.convert_to_key(record.TEN_COT) + '_ID'
    
    