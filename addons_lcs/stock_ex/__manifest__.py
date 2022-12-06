# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Kho',
    'version': '1.0',
    'sequence': 0,
    'summary': 'Quản lý kho',
    'depends': [
        'danh_muc',
        # 'account_ex',
        # 'sale_ex',
    ],
    'data': [
        'views/stock_ex_kiem_ke_kho_chi_tiet.xml',
		'views/stock_ex_nhap_xuat_kho_chi_tiet_view.xml',
		'views/stock_ex_cap_nhat_gia_nhap_kho_thanh_pham_view.xml',
		# 'templates/stock_ex_kiem_ke_bang_kiem_ke_vat_tu_hang_hoa_form_template.xml',
		'views/stock_ex_kiem_ke_bang_kiem_ke_vat_tu_hang_hoa_form_view.xml',
		'views/stock_ex_kiem_ke_vat_tu_hang_hoa_view.xml',
		'views/stock_ex_tinh_gia_xuat_kho_chon_vat_tu_hang_hoa_form_view.xml',
		'views/stock_ex_tinh_gia_xuat_kho_view.xml',
		'views/stock_ex_lenh_san_xuat_lap_pn_form_view.xml',
		'views/stock_ex_lenh_san_xuat_chi_tiet_thanh_pham_view.xml',
		# 'templates/stock_ex_lap_rap_thao_do_template.xml',
		'views/stock_ex_lap_rap_thao_do_view.xml',
		# 'templates/stock_ex_lenh_san_xuat_template.xml',
		'views/stock_ex_lenh_san_xuat_view.xml',
        'views/stock_ex_chuyen_kho_view.xml',
        'views/stock_ex_xuat_kho_view.xml',
		'views/stock_ex_nhap_kho_view.xml',
        # 'templates/stock_ex_02_vt_phieu_xuat_kho_template.xml',
        # 'templates/stock_ex_01_vt_phieu_nhap_kho_template.xml',   

        'templates/stock_ex_template.xml',        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
