# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class HE_THONG_SUB_SYSTEM(models.Model):
    _name = 'he.thong.sub.system'
    _description = 'Hệ thống menu'

    SubSystemCode = fields.Char(string='Mã (*)')
    SubSystemName = fields.Char(string='Tên (*)')
    ParentSubSystemCode = fields.Char(string='Menu cha')
    SubSystemSerial = fields.Char(string='Mã phân cấp')
    name =  fields.Char(related='SubSystemName')

    _sql_constraints = [
        ('code_uniq', 'unique ("SubSystemCode","SubSystemName")', 'Menu code+name là duy nhất!')
    ]