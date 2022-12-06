# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_LOAI_TAI_SAN(models.Model):
    _inherit = 'account.asset.category'
    
    MA_LOAI = fields.Char(string='Mã loại', help='Mã loại')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')

    @api.model
    def default_get(self,default_fields):
        res = super(DANH_MUC_LOAI_TAI_SAN, self).default_get(default_fields)
        tk_nguyen_gia = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=like','211%')],limit=1).id
        tk_khau_hao = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=like','214%')],limit=1).id
        tk_chi_phi = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=like','21%')],limit=1).id
        journal_id = self.env['account.journal'].search([],limit=1).id
        if tk_nguyen_gia:
            res['account_asset_id'] = tk_nguyen_gia
        if tk_khau_hao:
            res['account_depreciation_id'] = tk_khau_hao
        if tk_chi_phi:
            res['account_depreciation_expense_id'] = tk_chi_phi
        if journal_id:
            res['journal_id'] = journal_id
        return res