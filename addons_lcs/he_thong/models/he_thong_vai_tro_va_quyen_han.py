# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import UserError

class HE_THONG_VAI_TRO_VA_QUYEN_HAN(models.Model):
    _name = 'he.thong.vai.tro.va.quyen.han'
    _description = 'Vai trò'
    _inherit = ['mail.thread']
    
    MA_VAI_TRO = fields.Char(string='Mã vai trò (*)', help='Mã vai trò')
    TEN_VAI_TRO = fields.Char(string='Tên vai trò (*)', help='Tên vai trò')
    MO_TA = fields.Text(string='Mô tả', help='Mô tả')
    name = fields.Char(string='Name', help='Name', related='TEN_VAI_TRO')
    user_ids = fields.Many2many('res.users','he_thong_vai_tro_va_quyen_han_res_users_rel','he_thong_vai_tro_va_quyen_han_id', 'res_users_id', string='Chọn người dùng', help='Chọn người dùng')
    # permission = fields.Many2many('he.thong.permission', string='Quyền hạn')
    CHI_TIET_IDS = fields.One2many('he.thong.vai.tro.va.quyen.han.chi.tiet', 'VAI_TRO_ID', string='Vai trò và Quyền hạn chi tiết')
    THUOC_HE_THONG = fields.Boolean(string='Là quyền thuộc hệ thống', default=False)

    def action_add_user(self):
        action = self.env.ref('he_thong.open_he_thong_vai_tro_them_nguoi_dung_form').read()[0]
        chi_tiet = []
        user_list = self.env['res.users'].search([])
        for user in user_list:
            chi_tiet += [(0, 0, {
                'user_id': user.id,
                'TEN_DANG_NHAP': user.login,
                'HO_VA_TEN': user.name,
                'CHUC_DANH': user.CHUC_DANH,
            })]
        context = {
            'default_VAI_TRO_ID': self.id,
            'default_CHI_TIET_IDS': chi_tiet,
        }
        action['context'] = context
        return action

    def action_phan_quyen(self):
        if self.MA_VAI_TRO == 'Admin':
            raise UserError('<Admin> là vai trò thuộc hệ thống. Bạn không được phép phân quyền lại.')
        action = self.env.ref('he_thong.open_he_thong_thiet_lap_vai_tro_tham_so_form').read()[0]
        # permission_list = self.get_permissions()
        chi_tiet = []
        bao_cao_menu = False
        # Lấy từ menu
        # menu_list = self.env['ir.ui.menu'].search([], order='sequence')
        res_ids = self.env['ir.model.data'].search([('model', '=', 'ir.ui.menu'), ('module', 'in', ('menu','thu_kho'))]).mapped('res_id')
        menu_list = self.env['ir.ui.menu'].search([('id', 'in', res_ids)], order='sequence')
        for menu_id in menu_list:
            if menu_id.name == 'Báo cáo':
                bao_cao_menu = menu_id.id
            chi_tiet += [(0, 0, {
                'menu_id': menu_id.id,
                'menu': menu_id.id,
                'parent': menu_id.parent_id.id,
                'parent_menu_id': menu_id.parent_id.id,
                'name': menu_id.name,
            })]
            if not len(menu_id.child_id):
                offset = 0
                for per in menu_id.permission_ids:
                    if per.active:
                        has_permission = self.env['he.thong.role.permission.mapping'].search([('VAI_TRO_ID','=',self.id),('menu_id','=',menu_id.id),('permission_id','=',per.id)], limit=1)
                        chi_tiet += [(0, 0, {
                            'menu': menu_id.id * 1000 + offset,
                            'parent': menu_id.id ,
                            'parent_menu_id': menu_id.id,
                            'name': per.PermissionName,
                            'permission_id': per.id,
                            'AUTO_SELECT': bool(has_permission),
                        })]         
                        offset += 1    
        # Lấy từ báo cáo
        report_list = self.env['tien.ich.bao.cao'].search([])
        for report in report_list:
            chi_tiet += [(0, 0, {
                'report_id': report.id,
                'menu': report.id*1000000,
                'parent': report.parent_id.id*1000000 or bao_cao_menu,
                'parent_report_id': report.parent_id.id,
                'name': report.TEN_BAO_CAO,
            })]
            if not report.has_child:
                offset = 1
                for per in report.permission_ids:
                    # if per.active
                    has_permission = self.env['he.thong.role.permission.mapping'].search([('VAI_TRO_ID','=',self.id),('report_id','=',report.id),('permission_id','=',per.id)], limit=1)
                    chi_tiet += [(0, 0, {
                        'menu': report.id * 1000000 + offset,
                        'parent': report.id * 1000000,
                        'parent_report_id': report.id ,
                        'name': per.PermissionName,
                        'permission_id': per.id,
                        'AUTO_SELECT': bool(has_permission),
                    })]         
                    offset += 1

        context = {
            'default_VAI_TRO_ID': self.id,
            'default_CHI_TIET_IDS': chi_tiet,
        }
        action['context'] = context
        return action

    # Thiết lập lại cây chức năng
    def action_reset(self):
        query = """
        DELETE FROM ir_model_data WHERE model like 'he.thong.%';
        DELETE FROM msc_regis_permision_for_sub_system;
        DELETE FROM msc_regis_permision_for_report;
        DELETE FROM he_thong_role_permission_mapping;
        DELETE FROM he_thong_permission;
        DELETE FROM he_thong_vai_tro_va_quyen_han;
        DELETE FROM he_thong_sub_system;
        """
        self.env.cr.execute(query)
        return True

    _sql_constraints = [
        ('MA_VAI_TRO_uniq', 'unique ("MA_VAI_TRO")', 'Mã vai trò <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]

    @api.multi
    def write(self, vals):
        result = super(HE_THONG_VAI_TRO_VA_QUYEN_HAN, self).write(vals)
        if 'user_ids' in vals:
            for record in self:
                if record.MA_VAI_TRO == 'Admin':
                    record.user_ids.write({'is_admin': True})
        return result