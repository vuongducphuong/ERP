# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Phân tích',
    'version': '1.0',
    'sequence': 0,
    'summary': 'Phân tích tổng hợp',
    'depends': [
		'danh_muc',
		'account_ex',
		'stock_ex',
		'purchase_ex',
		'sale_ex',
		'gia_thanh',
    ],
    'data': [
        'views/phan_tich_doanh_thu_theo_san_pham_view.xml',
        'views/phan_tich_doanh_thu_va_chi_phi.xml',
        'views/he_thong_phan_tich.xml',
        'templates/phan_tich_templates.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
