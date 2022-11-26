# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_KHAI_BAO_DINH_MUC_PHAN_BO_CHI_PHI_THEO_CONG_TRINH_FORM(models.Model):
    _name = 'gia.thanh.kbdm.pbcp.theo.cong.trinh.form'
    _description = ''
    _inherit = ['mail.thread']
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    GIA_THANH_KHAI_BAO_DINH_MUC_PHAN_BO_CHI_PHI_THEO_CONG_TRINH_CHI_TIET_IDS = fields.One2many('gia.thanh.kbdm.pbcp.theo.cong.trinh.chi.tiet', 'CHI_TIET_ID', string='Khai báo định mức phân bổ chi phí theo đối tượng THCP chi tiết')