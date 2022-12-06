# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields
from odoo import SUPERUSER_ID

class CountryState(models.Model):
    _inherit = 'res.country.state'

    CAP = fields.Char(string='Cấp tổ chức')

class CountryStateDistrict(models.Model):
    _inherit = 'res.country.state.district'
    _order = 'name'

    CAP = fields.Char(string='Cấp tổ chức')
    TEN_DAY_DU =  fields.Char(string='Tên đầy đủ' , compute='_compute_ten_day_du_quan_huyen' , store=True)

    _sql_constraints = [
        ('name_state_uniq', 'unique (name,state_id)', 'Không được trùng tên!'),
    ]

    
    @api.multi
    @api.depends('CAP','name')
    def _compute_ten_day_du_quan_huyen(self):
        for record in self:
            record.TEN_DAY_DU = record.CAP + ' ' + record.name 
    
    

class CountryStateDistrictWard(models.Model):
    _inherit = 'res.country.state.district.ward'
    _order = 'name'

    CAP = fields.Char(string='Cấp tổ chức')
    TEN_DAY_DU =  fields.Char(string='Tên đầy đủ' , compute='_compute_ten_day_du_xa_phuong' , store=True)

    _sql_constraints = [
        ('name_district_uniq', 'unique (name,district_id)', 'Không được trùng tên!'),
    ]

    @api.multi
    @api.depends('CAP','name')
    def _compute_ten_day_du_xa_phuong(self):
        for record in self:
            record.TEN_DAY_DU = record.CAP + ' ' + record.name 
    
    