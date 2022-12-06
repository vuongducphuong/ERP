# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED
from odoo import api, models, fields

class ACCOUNT_EX_PHIEU_THU_CHI(models.Model):
    _inherit = 'account.ex.phieu.thu.chi'

    SOURCE_ID = fields.Reference(selection_add=[
        ('sale.document', 'Chứng từ bán hàng'),
        ('sale.ex.tra.lai.hang.ban', 'Chứng từ trả lại hàng bán'),
        ('sale.ex.giam.gia.hang.ban', 'Chứng từ giảm giá hàng bán'),
        ], string='Lập từ')