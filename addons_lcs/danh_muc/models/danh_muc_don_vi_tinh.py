# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_DON_VI_TINH(models.Model):
    _name = 'danh.muc.don.vi.tinh'
    _description = 'Đơn vị tính'
    _inherit = ['mail.thread']
    _order = "DON_VI_TINH"

    DON_VI_TINH = fields.Char(string='Đơn vị tính (*)', help='Đơn vị tính', required=True)
    MO_TA = fields.Text(string='Mô tả', help='Mô tả')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    name = fields.Char(string='Name', help='Name',related='DON_VI_TINH',store=True)

    _sql_constraints = [
        ('DON_VI_TINH_uniq', 'unique ("DON_VI_TINH")', 'Đơn vị tính <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]

    @api.model
    def name_search_extend(self, name='', args=None, operator='ilike', limit=100, fields=[], record={}, extends=None):
        ma_hang_id = record.get('MA_HANG_ID')
        if ma_hang_id:
            ma_hang = self.env['danh.muc.vat.tu.hang.hoa'].browse(ma_hang_id.get('res_id'))
            if ma_hang: 
                if ma_hang.DVT_CHINH_ID:
                    dvt = [ma_hang.DVT_CHINH_ID.id]
                    dvt += [dvcd.DVT_ID.id for dvcd in ma_hang.DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI_IDS]
                    return {
                        'total_count': len(dvt),
                        'records': self.browse(dvt).name_get_extend(fields),
                    }
                else:
                    return {
                        'total_count': 0,
                        'records': [],
                    }
        return super(DANH_MUC_DON_VI_TINH, self).name_search_extend(name, args, operator, limit, fields)