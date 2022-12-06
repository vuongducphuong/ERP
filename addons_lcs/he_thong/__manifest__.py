# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Quản lý hệ thống',
    'version': '0.1',
    'category': 'Hệ thống',
    'sequence': 102,
    'summary': 'System, Access Control',
    'description': "",
    'depends': [
        'danh_muc',
    ],
    'data': [
		'views/he_thong_vai_tro_va_quyen_han_view.xml',
		'views/he_thong_quan_ly_nguoi_dung_view.xml',
		'views/he_thong_ngay_hach_toan_view.xml',
		'views/he_thong_chon_chi_nhanh_lam_viec_view.xml',
        # 'security/ir.model.access.csv',
        # 'views/he_thong_views.xml',
        'views/he_thong_templates.xml',
        'views/he_thong_tuy_chon.xml',
        'views/he_thong_thiet_lap_vai_tro.xml', 
        'views/he_thong_vai_tro_them_nguoi_dung.xml', 
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [
        # "static/src/xml/phan_quyen.xml",
        "static/src/xml/menu_update_database.xml",
    ],
}