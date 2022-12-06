# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
PARENT_REPORT = (
    'Báo cáo tài chính',
    'Quỹ',
    'Ngân hàng',
    'Mua hàng',
    'Bán hàng',
    'Kho',
    'Công cụ dụng cụ',
    'Tài sản cố định',
    'Tiền lương',
    'Giá thành',
    'Thuế',
    'Thủ kho',
    'Thủ quỹ',
    'Tổng hợp',
    'Hợp đồng',)

class TIEN_ICH_BAO_CAO(models.Model):
    _name = 'tien.ich.bao.cao'
    _parent_store = True
    _description = 'Báo cáo'

    permission_ids = fields.Many2many('he.thong.permission', 'msc_regis_permision_for_report', 'report_id', 'permission_id', string='Quyền hạn')
    TEN_BAO_CAO = fields.Char(string='Tên báo cáo', help='Tên báo cáo')
    TEN_BAO_CAO_TIENG_ANH = fields.Char(string='Tên bằng tiếng anh', help='Tên bằng tiếng anh')
    # group_id
    parent_id = fields.Many2one('tien.ich.bao.cao', string='Thuộc', help='Thuộc', oldname='THUOC_ID') 
    THUOC = fields.Char(string='Thuộc', help='Thuộc')
    active = fields.Boolean(string='Active' , help='Active' , oldname='ACTIVE', default=True)
    STT = fields.Integer(string='STT', help = 'Số thứ tự')
    name = fields.Char(string='Tên báo cáo', related='TEN_BAO_CAO')

    RES_MODEL = fields.Char(compute='_compute_REF')
    VIEW_ID = fields.Integer(compute='_compute_REF')
    child_ids = fields.One2many('tien.ich.bao.cao', 'parent_id', 'Chứa')
    has_child = fields.Boolean(compute='_compute_child')
    MA_PHAN_CAP = fields.Char(help='Mã phân cấp')
    form_size = fields.Char(string='Size', help='Kích thước của form tham số', default='large')

    @api.depends('child_ids')
    def _compute_child(self):
        for record in self:
            record.has_child = len(record.child_ids) > 0

    @api.depends('name')
    def _compute_REF(self):
        for record in self:
            # Tìm báo cáo theo tên
            act = self.env['ir.actions.act_window'].search([('name', '=', record.name.strip()), ('target','=','new'), ('view_id','!=', None)], limit=1)
            if act:
                record.RES_MODEL = act.res_model
                record.VIEW_ID = act.view_id.id
    
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        if not (self.env.user.is_admin or self.env.uid == 1):
            report_ids = self._get_accessible_report()
            domain = (domain or []) + ['|', ('id', 'in', tuple(report_ids)), ('TEN_BAO_CAO','in', PARENT_REPORT)]
        res = super(TIEN_ICH_BAO_CAO, self.with_context(active_test=(self.env.uid!=1))).search_read(domain, fields, offset, 0, order)
        result = []
        dic = {}
        dic_parent = {}
        for x in res:
            key = x.get('TEN_BAO_CAO')+str(x.get('parent_id'))
            if (x.get('TEN_BAO_CAO') in PARENT_REPORT or (x.get('RES_MODEL') and x.get('VIEW_ID'))) and key not in dic:
                result += [x]
                dic[key] = True
                if x.get('parent_id'):
                    dic_parent[x.get('parent_id')[0]] = True
        # Todo: Cần cải thiện 2 vòng for này
        # Vòng for thứ 2 để lọc bỏ các parent không có con
        final_result = []
        for r in result:
            if (not r.get('parent_id')) and (r.get('id') not in dic_parent) and r.get('TEN_BAO_CAO') in PARENT_REPORT:
                continue
            final_result += [r]
        return final_result

    def _get_accessible_report(self):
        vai_tro_ids = self.env.user.VAI_TRO_VA_QUYEN_HAN.ids
        report_ids =  self.env['he.thong.role.permission.mapping'].read_group([('VAI_TRO_ID', 'in', vai_tro_ids), ('report_id','!=', None)], fields=['report_id'], groupby=['report_id'])
        return [report.get('report_id')[0] for report in report_ids]

    