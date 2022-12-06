# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Thủ kho',
    'version': '1.0',
    'sequence': 0,
    'summary': 'Phân hệ dành riêng cho các doanh nghiệp có thủ kho',
    'website': 'https://cloudify.vn/',
    'depends': [
      	'danh_muc',
      	'sale_ex',
      	'purchase_ex',
    ],
    'data': [
        'views/purchase_ex_chung_tu_mua_hang_view.xml',
        'views/sale_ex_chung_tu_ban_hang_view.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
