# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{ 
    'name': 'Quản lý Menu',
    'version': '7.5',    
    'category': 'Hệ thống',
    'sequence': 102,
    'summary': 'System, Menu Control',
    'description': "",
    'website': '',
    'depends': [
        'calendar',
        'danh_muc',
        'he_thong',
        'account_ex',
        'stock_ex',
        'asset',
        'supply',
        'purchase_ex',
        'sale_ex',
        'tien_luong',
        'tong_hop',
        'tien_ich',
        'base_import_ex',
        'bao_cao',
        'phan_tich',
        'gia_thanh',
        'thue',
    ],
    'data': [
        'views/menu_views.xml',
        'views/web_planner_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}