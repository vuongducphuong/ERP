# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.http import request
import datetime

class HE_THONG_NGAY_HACH_TOAN(models.Model):
    _name = 'he.thong.ngay.hach.toan'
    _description = 'Chọn ngày hạch toán'
    _auto = False

    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    
    # Thiết lập ngày hạch toán
    def action_view_report(self):
        request.session.ngay_thay_doi_hach_toan = datetime.datetime.now().date()
        request.session.ngay_hach_toan = datetime.datetime.strptime(self.get_dbtime('NGAY_HACH_TOAN'),'%Y-%m-%d').date()
    