# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
class SO_KHO_CHI_TIET(models.Model):
    _inherit = 'so.kho.chi.tiet'

    CHUNG_TU_LAP_RAP_THAO_DO_ID = fields.Many2one('stock.ex.lap.rap.thao.do', string='Chứng từ lắp ráp tháo dỡ', help='AssemblyRefID')
    CHUNG_TU_LENH_SAN_XUAT_ID = fields.Many2one('stock.ex.lenh.san.xuat', string='Chứng từ lệnh sản xuất', help='ProductionOrderRefID')