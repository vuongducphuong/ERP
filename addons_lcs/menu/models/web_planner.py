# -*- coding: utf-8 -*-
from odoo import api, models


class PlannerAccountEx(models.Model):

    _inherit = 'web.planner'

    def _get_planner_application(self):
        planner = super(PlannerAccountEx, self)._get_planner_application()
        planner.append(['planner_account_ex', 'Thiết lập ban đầu'])
        return planner

    def _prepare_planner_account_data(self):
        values = {
            'company_id': self.env.user.company_id,
            'is_coa_installed': bool(self.env['account.account'].search_count([])),
            'payment_term': self.env['account.payment.term'].search([]),
            'supplier_menu_id': self.env.ref('account.menu_account_supplier').id
        }
        return values
