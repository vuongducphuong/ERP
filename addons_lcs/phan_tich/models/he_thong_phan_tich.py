# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class HE_THONG_PHAN_TICH(models.Model):
    _name = 'he.thong.phan.tich'
    _parent_store = True
    _description = 'Phân tích'

    # permission_ids = fields.Many2many('he.thong.permission', 'msc_regis_permision_for_report', 'report_id', 'permission_id', string='Quyền hạn')
    TEN_PHAN_TICH = fields.Char(string='Nội dung phân tích', help='Tên phân tích')
    parent_id = fields.Many2one('he.thong.phan.tich', string='Thuộc', help='Thuộc') 
    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Tên phân tích', related='TEN_PHAN_TICH')
    ACTION_ID = fields.Integer(compute='_compute_REF')
    # RES_MODEL = fields.Char(compute='_compute_REF')
    # VIEW_ID = fields.Integer(compute='_compute_REF')
    child_ids = fields.One2many('he.thong.phan.tich', 'parent_id', 'Chứa')
    # has_child = fields.Boolean(compute='_compute_child')
    MA_PHAN_CAP = fields.Char(help='Mã phân cấp')
    form_size = fields.Char(string='Size', help='Kích thước của form tham số', default='large')

    # @api.depends('child_ids')
    # def _compute_child(self):
    #     for record in self:
    #         record.has_child = len(record.child_ids) > 0

    @api.depends('name')
    def _compute_REF(self):
        for record in self:
            # Tìm phân tích theo tên
            act = self.env['ir.actions.act_window'].search([('name', '=', record.TEN_PHAN_TICH.strip())], limit=1)
            if act:
                record.ACTION_ID = act.id
                # record.RES_MODEL = act.res_model
                # record.VIEW_ID = act.view_id.id
    
    # @api.model
    # def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
    #     if not (self.env.user.is_admin or self.env.uid == 1):
    #         report_ids = self._get_accessible_report()
    #         domain = (domain or []) + ['|', ('id', 'in', tuple(report_ids)), ('TEN_PHAN_TICH','in', PARENT_REPORT)]
    #     res = super(HE_THONG_PHAN_TICH, self.with_context(active_test=(self.env.uid!=1))).search_read(domain, fields, offset, 0, order)
    #     result = []
    #     dic = {}
    #     dic_parent = {}
    #     for x in res:
    #         key = x.get('TEN_PHAN_TICH')+str(x.get('parent_id'))
    #         if (x.get('TEN_PHAN_TICH') in PARENT_REPORT or (x.get('RES_MODEL') and x.get('VIEW_ID'))) and key not in dic:
    #             result += [x]
    #             dic[key] = True
    #             if x.get('parent_id'):
    #                 dic_parent[x.get('parent_id')[0]] = True
    #     # Todo: Cần cải thiện 2 vòng for này
    #     # Vòng for thứ 2 để lọc bỏ các parent không có con
    #     final_result = []
    #     for r in result:
    #         if (not r.get('parent_id')) and (r.get('id') not in dic_parent) and r.get('TEN_PHAN_TICH') in PARENT_REPORT:
    #             continue
    #         final_result += [r]
    #     return final_result

    # def _get_accessible_report(self):
    #     vai_tro_ids = self.env.user.VAI_TRO_VA_QUYEN_HAN.ids
    #     report_ids =  self.env['he.thong.role.permission.mapping'].read_group([('VAI_TRO_ID', 'in', vai_tro_ids), ('report_id','!=', None)], fields=['report_id'], groupby=['report_id'])
    #     return [report.get('report_id')[0] for report in report_ids]

    