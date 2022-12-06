# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_KHOAN_MUC_CP(models.Model):
    _name = 'danh.muc.khoan.muc.cp'
    _description = 'Khoản mục chi phí'
    _parent_store = True
    _inherit = ['mail.thread']


    MA_KHOAN_MUC_CP = fields.Char(string='Mã (*)', help='Mã',required=True)
    TEN_KHOAN_MUC_CP = fields.Char(string='Tên (*)', help='Tên',required=True)
    parent_id = fields.Many2one('danh.muc.khoan.muc.cp', string='Thuộc', help='Thuộc')
    DIEN_GIAI = fields.Text(string='Diễn giải', help='Diễn giải')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    name = fields.Char(string='Name', help='Name', related='MA_KHOAN_MUC_CP', store=True)
    MA_PHAN_CAP = fields.Char(string='Mã phân cấp', help='Mã phân cấp')
    BAC = fields.Integer(string='Bậc', help='Bậc')
    LA_TONG_HOP = fields.Boolean(string='Làổng hợp', compute='_compute_LA_TONG_HOP', store=True)
    child_ids = fields.One2many('danh.muc.khoan.muc.cp', 'parent_id', 'Chứa', copy=True) 

    @api.depends('child_ids')
    def _compute_LA_TONG_HOP(self):
        for record in self:
            record.LA_TONG_HOP = True if record.child_ids else False 

    _sql_constraints = [
        ('MA_KHOAN_MUC_CP_uniq', 'unique ("MA_KHOAN_MUC_CP")', 'Mã khoản mục CP <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]

    
    @api.model
    def _name_search_extend(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None, record={}, fields=[]):
        return super(DANH_MUC_KHOAN_MUC_CP, self)._name_search_extend(name, args, operator, limit=None, fields=fields, record={})
    
    # @api.model
    # def create(self, vals): 
    #     # if not vals.get('move_lines'):
    #        # raise ValidationError("Bạn phải nhập chứng từ chi tiết!")
    #     if (vals.get('TEN_KHOAN_MUC_CP')):
    #         vals['name'] = vals.get('TEN_KHOAN_MUC_CP')
    #     result = super(DANH_MUC_KHOAN_MUC_CP, self).create(vals)
    #     return result