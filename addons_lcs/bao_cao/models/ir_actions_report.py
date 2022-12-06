# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import UserError
import random

class BAO_CAO_QUAN_LY_MAU_IN(models.Model):
    _inherit = 'ir.actions.report'
    _description = 'Quản lý mẫu in'

    help = fields.Text(string='HTML', help='HTML cho mẫu in', translate=False)

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        if not self.help:
            template_view = self.env['ir.ui.view'].search([('name','=', self.report_name.split('.')[1])], limit=1)
            ir_data_view = self.env['ir.model.data'].search([('name','=', self.report_name.split('.')[1])], limit=1)
            if template_view and ir_data_view:
                sub_view_name = template_view.name.replace('template_','')
                template_sub_view = self.env['ir.ui.view'].search([('name','=', sub_view_name)], limit=1)
                if template_sub_view:
                    rnd = '->' +str(random.randint(0,999))
                    new_template_name = template_view.name + rnd
                    default = default or {}
                    qweb = ("""<?xml version="1.0"?>
                    <t t-name="template_%s">
                        <t t-call="web.html_container">
                            <t t-foreach="docs" t-as="o">
                                %s
                            </t>
                        </t>
                    </t>
                    """ % (template_view.name, template_sub_view.arch_db.replace('<?xml version="1.0"?>', ''))).replace(sub_view_name,sub_view_name+rnd)
                    default.update({
                        'help': qweb,
                    })
                # Clone view
                temp = template_view.copy({'name': new_template_name, 'key': 'bao_cao.' + new_template_name})
                temp.write({'arch_db': qweb})
                # Clone ir_model_data
                ir_data_view.copy({'name': new_template_name,'res_id':temp.id,'noupdate':True})
                default.update({
                    'report_file': 'bao_cao.' + new_template_name,
                    'report_name': 'bao_cao.' + new_template_name,
                })
        return super(BAO_CAO_QUAN_LY_MAU_IN, self).copy(default)

    @api.multi
    def write(self, values):
        if len(self)==1 and values.get('help'):
            template_view = self.env['ir.ui.view'].search([('name','=', self.report_name.split('.')[1])], limit=1)
            if template_view:
                template_view.write({'arch_db': values.get('help')})

        return super(BAO_CAO_QUAN_LY_MAU_IN, self).write(values)

    
    @api.multi
    def unlink(self):
        if not(self.env.user.id == 1 or '->' in self.report_name):
            raise UserError("Không thể xóa mẫu in của hệ thống!")
        # Unlink view
        self.env['ir.ui.view'].search([('name','=', self.report_name.split('.')[1])], limit=1).unlink()
        # Clone ir_model_data
        self.env['ir.model.data'].search([('name','=', self.report_name.split('.')[1])], limit=1).unlink()
        return super(BAO_CAO_QUAN_LY_MAU_IN, self).unlink()
    