# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_DOI_TUONG_PHAN_BO(models.Model):
    _name = 'danh.muc.doi.tuong.phan.bo'
    _description = 'Đối tượng phân bổ'
    _inherit = ['mail.thread']
    code = fields.Char(string='Mã đối tượng phân bổ', help='Mã đối tượng phân bổ', auto_num='danh_muc_doi_tuong_phan_bo_MA_DOI_TUONG_PHAN_BO')
    name = fields.Char(string='Tên đối tượng phân bổ', help='Tên đối tượng phân bổ')
    type = fields.Selection([('DT_THCP', 'Đối tượng THCP'), ('CONG_TRINH', 'Công trình'), ('DON_VI', 'Đơn vị'), ], string='Loại', help='Loại',required=True,default='DON_VI')
    