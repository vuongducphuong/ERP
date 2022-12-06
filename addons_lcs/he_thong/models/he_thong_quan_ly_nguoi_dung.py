# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo import SUPERUSER_ID

class HE_THONG_NGUOI_DUNG(models.Model):
    _inherit = 'res.users'

    # @api.model
    # def _get_chi_nhanh(self):
    #     if self.env.user.CHI_NHANH_ID:
    #         return self.env.user.CHI_NHANH_ID
    #     else:
    #         chi_nhanh = self.env['danh.muc.to.chuc'].search([('CAP_TO_CHUC','in',['1','2'])],limit=1)
    #         self.env.user.write({'CHI_NHANH_ID': chi_nhanh.id})
    #         return chi_nhanh

    CHUC_DANH = fields.Char(string='Chức danh', help='Chức danh')
    # NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên', help='Nhân viên')
    DIEN_GIAI = fields.Text(string='Diễn giải', help='Diễn giải')
    VAI_TRO_VA_QUYEN_HAN = fields.Many2many('he.thong.vai.tro.va.quyen.han', string='Chọn vai trò và quyền hạn', help='Chọn vai trò và quyền hạn')
    # CHI_NHANH_IDS = fields.Many2many('danh.muc.to.chuc', string='Làm việc với chi nhánh', help='Các chi nhánh được làm việc', domain=[('CAP_TO_CHUC','in',['1','2'])], default=_get_chi_nhanh)
    # CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh đang làm việc', help='Chi nhánh đang làm việc', domain=[('CAP_TO_CHUC','in',['1','2'])],default=_get_chi_nhanh, required=True)
    # DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    CHO_PHEP_SAO_CHEP_DU_LIEU_KHI_THEM_DONG_CHUNG_TU_MOI = fields.Boolean(string='Cho phép sao chép dữ liệu khi thêm dòng mới')
    HAN_CHE_TAI_KHOAN_KHI_NHAP_CHUNG_TU = fields.Boolean(string='Hạn chế tài khoản khi nhập chứng từ')
    # BAO_GOM_CHUNG_TU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm chứng từ chi nhánh phụ thuộc')

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        if self.env.user.id != SUPERUSER_ID:
            domain = (domain or []) + [('id', '!=', SUPERUSER_ID)]
        return super(HE_THONG_NGUOI_DUNG, self).search_read(domain, fields, offset, limit, order)

    @api.onchange('VAI_TRO_VA_QUYEN_HAN')
    def update_is_admin(self):
        admin_role = self.env['he.thong.vai.tro.va.quyen.han'].search([('MA_VAI_TRO', '=', 'Admin')], limit=1)
        self.is_admin = admin_role and admin_role.id in self.VAI_TRO_VA_QUYEN_HAN.ids

    @api.model
    def create(self, values): 
        record = super(HE_THONG_NGUOI_DUNG, self).create(values)
        if values.get('name'):
            record.write({'name': values.get('name')})
        return record

    @api.multi
    def write(self, vals):
        # default_template_user is always admin
        company_admin = self.env.ref('auth_signup.default_template_user')
        if 'is_admin' in vals and company_admin.id in self.ids:
           vals['is_admin'] = True
        return super(HE_THONG_NGUOI_DUNG, self).write(vals)
