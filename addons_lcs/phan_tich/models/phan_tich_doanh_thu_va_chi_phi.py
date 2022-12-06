# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools


class PHAN_TICH_DOANH_THU_THEO_SAN_PHAM(models.Model):
    _name = "phan.tich.doanh.thu.va.chi.phi"
    _description = "Phân tích doanh thu và chi phí"
    _order = 'NGAY_HACH_TOAN'
    _auto = False

    name = fields.Char(string='Phát sinh', readonly=True)
    doanh_thu = fields.Float(string='Doanh thu')
    la_doanh_thu = fields.Boolean(string='Doanh thu')
    la_chi_phi = fields.Boolean(string='Chi phí')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán')
    THANG_HACH_TOAN = fields.Integer(string='Tháng hạch toán')
    active_id = fields.Boolean(default=True)

    def get_query_from_clause(self):
        return """
            (SELECT
                scct.id as id,
                CASE WHEN scct."GHI_NO" > 0 
                THEN
                    scct."GHI_NO"
                ELSE  
                    scct."GHI_CO" 
                END as doanh_thu,
                CASE WHEN scct."GHI_NO" > 0 THEN True ELSE False END AS la_doanh_thu,
                CASE WHEN scct."GHI_CO" > 0 THEN True ELSE False END AS la_chi_phi,
                scct."GHI_CO" as chi_phi,
                scct."NGAY_HACH_TOAN" as "NGAY_HACH_TOAN",
                EXTRACT(MONTH FROM scct."NGAY_HACH_TOAN") as "THANG_HACH_TOAN"
            FROM so_cai_chi_tiet scct
            INNER JOIN danh_muc_he_thong_tai_khoan dmhttk ON scct."TAI_KHOAN_ID" = dmhttk.id
            WHERE dmhttk."SO_TAI_KHOAN" like '5%' or dmhttk."SO_TAI_KHOAN" like '6%') as phan_tich_doanh_thu_va_chi_phi"""