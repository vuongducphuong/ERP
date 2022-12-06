# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools


class PHAN_TICH_DOANH_THU_THEO_SAN_PHAM(models.Model):
    _name = "phan.tich.doanh.thu.theo.san.pham"
    _description = "Phân tích doanh thu theo sản phẩm"
    _order = 'name desc'
    _auto = False

    name = fields.Char(string='Sản phẩm', readonly=True)
    doanh_thu = fields.Float(string='Doanh thu')

    def get_query_from_clause(self):
        return """
            (SELECT id, 
                "TEN" as name,
                100 as doanh_thu
                FROM    danh_muc_vat_tu_hang_hoa) as phan_tich_doanh_thu_theo_san_pham """