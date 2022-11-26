# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields
from odoo import SUPERUSER_ID

class ResGroup(models.Model):
    _name = 'res.groups'
    _inherit = 'res.groups'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        res = super(ResGroup, self).search(args, offset=offset, limit=limit, order=order, count=count)
        if SUPERUSER_ID == self._uid:
            return res
        # return only groups that include current user
        return res & self.env.user.groups_id