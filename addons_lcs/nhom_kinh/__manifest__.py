# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Nhôm kính',
    'version': '1.0',
    'sequence': 0,
    'summary': 'Phân hệ dành riêng cho các doanh nghiệp sản xuất nhôm kính',
    'website': 'https://cloudify.vn/',
    'depends': [
      'danh_muc',
      'sale_ex',
      'purchase_ex',
    ],
    'data': [
        'views/account_ex_don_dat_hang.xml',
        'views/sale_ex_chung_tu_ban_hang_view.xml',
        'views/purchase_ex_chung_tu_mua_hang_view.xml',
        'data/nhom_kinh_data.xml',
        'templates/nhom_kinh_don_dat_hang_template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
