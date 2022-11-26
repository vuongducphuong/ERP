# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, tools
from odoo import SUPERUSER_ID

class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    model_id = fields.Many2one('ir.model', string='Main model', compute='_compute_model_id')
    @api.depends('action')
    def _compute_model_id(self):
        MODEL_GETTER = {
            'ir.actions.act_window': lambda action: action.res_model,
            'ir.actions.report': lambda action: action.model,
            'ir.actions.server': lambda action: action.model_id.model,
        }
        for menu in self:
            if not menu.model_id and (menu.action):
                get_model = MODEL_GETTER.get(menu.action._name)
                if get_model:
                    model = get_model(menu.action)
                    if model in self.env:
                        menu.model_id = self.env['ir.model'].search([('model', '=', model)]).id

    # MSC_RegisPermisionForSubSystem
    permission_ids = fields.Many2many('he.thong.permission', 'msc_regis_permision_for_sub_system', 'menu_id', 'permission_id', string='Quyền hạn')
    # SubSystemCode = fields.Char('Menu code')

    def has_child(self, _id):
        return len(self.search([('parent_id', '=', _id)], limit=1)) > 0

    @api.model
    @tools.ormcache('frozenset(self.env.user.groups_id.ids)', 'debug')
    def _visible_menu_ids(self, debug=False):
        """ Return the ids of the menu items visible to the user. """
        # retrieve all menus, and determine which ones are visible
        context = {'ir.ui.menu.full_list': True}
        # full_domain = []
        # if not debug:
        #     setting = self.env.ref('base.menu_administration')
        #     full_domain += ['|', ('id', '>', setting.parent_right), ('id', '<', setting.parent_left)]
        menus = self.with_context(context).search([])

        groups = self.env.user.groups_id
        # Exception for Admin user
        if self.env.user.is_admin:
            groups = self.sudo().env['res.groups'].search([])
        if not debug:
            groups = groups - self.env.ref('base.group_no_one')
        # first discard all menus with groups the user does not have
        # Lọc các menu thỏa mãn 1 trong 2 điều kiện
        # 1. Không nằm trong groups nào (not menu.groups_id)
        # 2. Nằm trong ít nhất 1 group (menu.groups_id) mà group đó chứa user hiện tại(& groups)
        menus = menus.filtered(
            lambda menu: not menu.groups_id or menu.groups_id & groups)

        # take apart menus that have an action
        action_menus = menus.filtered(lambda m: m.action and m.action.exists())
        folder_menus = menus - action_menus
        visible = self.browse()

        # process action menus, check whether their action is allowed
        access = self.env['ir.model.access']
        MODEL_GETTER = {
            'ir.actions.act_window': lambda action: action.res_model,
            'ir.actions.report': lambda action: action.model,
            'ir.actions.server': lambda action: action.model_id.model,
        }
        for menu in action_menus:
            get_model = MODEL_GETTER.get(menu.action._name)
            if not get_model or not get_model(menu.action) or \
                    access.check(get_model(menu.action), 'view', False, menu=menu.id):
            # if (self._uid == 1) or (access.check(menu, 'view', False)):
                # make menu visible, and its folder ancestors, too
                visible += menu
                menu = menu.parent_id
                while menu and menu in folder_menus and menu not in visible:
                    visible += menu
                    menu = menu.parent_id

        return set(visible.ids)