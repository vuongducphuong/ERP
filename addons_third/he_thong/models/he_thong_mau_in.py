# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class HE_THONG_MAU_IN(models.Model):
    _name = 'he.thong.mau.in'
    _description = 'Danh sách mẫu in'

    name = fields.Char(string='name', related='ReportName')
    ReportID = fields.Char(string='ID mẫu in')
    ReportName = fields.Char(string='Tên mẫu in')
    RefTypeList = fields.Char(string='Danh sách RefType')
    Description = fields.Char(string='Mô tả')
    ReportTitle = fields.Char(string='Tiêu đề')