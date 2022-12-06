# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Công cụ dụng cụ',
    'version': '1.0',
    'sequence': 0,
    'summary': 'Quản lý công cụ dụng cụ',
    'depends': [
			'danh_muc',
			# 'account_ex',
    ],
    'data': [
		'views/supply_chon_chung_tu_ghi_giam_tscd_view.xml',
		'views/supply_ghi_tang_hang_loat_chi_tiet_view.xml',
		# 'views/supply_chon_chung_tu_dieu_chinh_cong_cu_dung_cu_chi_tiet_view.xml',
		'views/supply_chon_chung_tu_dieu_chinh_ccdc_form_view.xml',
		# 'views/supply_chon_chung_tu_nght_chi_tiet_view.xml',
		'views/supply_khai_bao_dau_ky_chi_tiet_view.xml',
		'views/supply_khai_bao_dau_ky_view.xml',
		# 'templates/supply_dieu_chuyen_template.xml',
		# 'templates/supply_dieu_chinh_template.xml',
		# 'templates/supply_ghi_tang_template.xml',
		# 'templates/supply_ghi_giam_template.xml',
		'views/supply_ghi_giam_view.xml',
		'views/supply_ghi_tang_hang_loat_view.xml',
		'views/supply_kiem_ke_view.xml',
		'views/supply_kiem_ke_tham_so_view.xml',
		'views/supply_phan_bo_chi_phi_view.xml',
		'views/supply_phan_bo_chi_phi_tham_so_view.xml',
		'views/supply_dieu_chuyen_view.xml',
		'views/supply_dieu_chinh_view.xml',
		'views/supply_ghi_tang_view.xml',	
		'templates/supply_templates.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
