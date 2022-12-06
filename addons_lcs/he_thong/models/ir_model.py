# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details

import logging

from odoo import api, fields, models, SUPERUSER_ID, tools,  _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.modules.registry import Registry
from odoo.tools import pycompat

_logger = logging.getLogger(__name__)
FUNCTION_ACCESS = {
    'create': 'create',
    'write': 'write',
    'unlink': 'unlink',
    'action_ghi_so': 'Post',
    'action_bo_ghi_so': 'UnPost',
    'print': 'Print',
}
NEED_CHECK_MENU = ('account.ex.phieu.thu.chi','stock.ex.nhap.xuat.kho','purchase.document','account.ex.chung.tu.nghiep.vu.khac',)

class IrModelAccess(models.Model):
    _inherit = 'ir.model.access'

    perm_view = fields.Boolean(string='View Access')

    def check_multi(self, kw):
        method = kw.get('method')
        model = kw.get('model')
        menu = False
        # if model in NEED_CHECK_MENU and kw.get('kwargs'):
            # menu = kw.get('kwargs').get('active_menu')
            # if self.env.uid == 1 and not menu:
                # raise ValidationError("Không thể kiểm tra quyền truy cập. Vui lòng liên hệ QTV!") 
        if method == 'rpc_action':
            method = kw.get('args')[1]
        if FUNCTION_ACCESS.get(method):
            self.check(model=model, mode=FUNCTION_ACCESS.get(method), menu=menu)

    # The context parameter is useful when the method translates error messages.
    # But as the method raises an exception in that case,  the key 'lang' might
    # not be really necessary as a cache key, unless the `ormcache_context`
    # decorator catches the exception (it does not at the moment.)
    @api.model
    @tools.ormcache_context('self._uid', 'model', 'mode', 'raise_exception', 'menu', keys=('lang',))
    def check(self, model, mode='read', raise_exception=True, menu=None):
        if self._uid == 1 or self.env.user.is_admin:
            # User root have all accesses
            return True
        if 'read' == mode:
            return True

        assert isinstance(model, pycompat.string_types), 'Not a model name: %s' % (model,)
        assert mode in ('read', 'write', 'create', 'unlink', 'view', 'Post', 'UnPost', 'Print'), 'Invalid access mode'

        # TransientModel records have no access rights, only an implicit access rule
        if model not in self.env:
            _logger.error('Missing model %s', model)
        # Check quyền của Tùy chọn
        # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/3769
        elif model != 'res.config.settings' and self.env[model].is_transient():
            return True
        CONVERT_DICT = {
            'view': 'Use', 
            'write': 'Edit', 
            'create': 'Add', 
            'unlink': 'Delete', 
        }
        # We check if a specific rule exists
        if menu:
            self._cr.execute("""SELECT * 
                                    FROM he_thong_role_permission_mapping map
                                    JOIN ir_model m ON (m.id = map.model_id)
                                    JOIN he_thong_vai_tro_va_quyen_han_res_users_rel gu ON (gu.he_thong_vai_tro_va_quyen_han_id = map."VAI_TRO_ID")
                                    JOIN he_thong_permission per ON (per.id = map.permission_id)
                                WHERE m.model = %s
                                    AND map.menu_id = %s
                                    AND gu.res_users_id = %s
                                    AND per."PermissionID" = %s
                                LIMIT 1""", (model, menu, self._uid, CONVERT_DICT.get(mode, mode)))
        else:
            self._cr.execute("""SELECT * 
                                    FROM he_thong_role_permission_mapping map
                                    JOIN ir_model m ON (m.id = map.model_id)
                                    JOIN he_thong_vai_tro_va_quyen_han_res_users_rel gu ON (gu.he_thong_vai_tro_va_quyen_han_id = map."VAI_TRO_ID")
                                    JOIN he_thong_permission per ON (per.id = map.permission_id)
                                WHERE m.model = %s
                                    AND gu.res_users_id = %s
                                    AND per."PermissionID" = %s
                                LIMIT 1""", (model, self._uid, CONVERT_DICT.get(mode, mode)))
        r = self._cr.fetchone()
        if mode in ('read', 'write', 'create', 'unlink'):
            if not r:
                self._cr.execute("""SELECT MAX(CASE WHEN perm_{mode} THEN 1 ELSE 0 END)
                                FROM ir_model_access a
                                JOIN ir_model m ON (m.id = a.model_id)
                                JOIN res_groups_users_rel gu ON (gu.gid = a.group_id)
                                WHERE m.model = %s
                                AND gu.uid = %s
                                AND a.active IS TRUE""".format(mode=mode),
                            (model, self._uid,))
                r = self._cr.fetchone()[0]
            if not r:
                # there is no specific rule. We check the generic rule
                self._cr.execute("""SELECT MAX(CASE WHEN perm_{mode} THEN 1 ELSE 0 END)
                                    FROM ir_model_access a
                                    JOIN ir_model m ON (m.id = a.model_id)
                                    WHERE a.group_id IS NULL
                                    AND m.model = %s
                                    AND a.active IS TRUE""".format(mode=mode),
                                (model,))
                r = self._cr.fetchone()[0]
            
            # Updated 2019-06-22 by anhtuan:
            # Nếu model không được định nghĩa bất kỳ quyền gì trong he_thong_role_permission_mapping
            # thì mọi user được toàn quyền
            # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/2301
            if not r:
                self._cr.execute("""SELECT * 
                                    FROM he_thong_role_permission_mapping map
                                    JOIN ir_model m ON (m.id = map.model_id)
                                    WHERE m.model = %s""",(model,))
                if not self._cr.fetchone():
                    return True

        if not r and raise_exception:
            # groups = '\n\t'.join('- %s' % g for g in self.group_names_with_access(model, mode))
            msg_heads = {
                # Messages are declared in extenso so they are properly exported in translation terms
                'read': _("Sorry, you are not allowed to access this document."),
                'write':  _("Sorry, you are not allowed to modify this document."),
                'create': _("Sorry, you are not allowed to create this kind of document."),
                'unlink': _("Sorry, you are not allowed to delete this document."),
            }
            # if groups:
            #     msg_tail = _("Only users with the following access level are currently allowed to do that") + ":\n%s\n\n(" + _("Document model") + ": %s)"
            #     msg_params = (groups, model)
            # else:
            msg_tail = _("Vui lòng liên hệ với quản trị viên.") + "\n\n(" + _("Loại Chứng từ/Danh mục") + ": %s)"
            msg_params = (model,)
            _logger.info('Access Denied by ACLs for operation: %s, uid: %s, model: %s', mode, self._uid, model)
            msg = '%s %s' % (msg_heads.get(mode, 'Bạn chưa có quyền thực hiện tác vụ này!'), msg_tail)
            raise AccessError(msg % msg_params)

        return bool(r)