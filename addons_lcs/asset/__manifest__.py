# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Tài sản cố định',
    'version': '1.0',
    'sequence': 0,
    'summary': 'Quản lý tài sản cố định',
    'depends': [
      'danh_muc',
      # 'account_ex',
    ],
    'data': [
		# 'views/asset_chon_chung_tu_tscd_chi_tiet_view.xml',
		
		'views/asset_dieu_chuyen_view.xml',
		'views/asset_danh_gia_lai_view.xml',
		'views/asset_khai_bao_dau_ky_view.xml',
		'views/asset_ghi_giam_view.xml',
		'views/asset_kiem_ke_view.xml',
		'views/asset_kiem_ke_tham_so_view.xml',
		'views/asset_ghi_tang_view.xml',
		'views/asset_tinh_khau_hao_view.xml',
		'views/asset_chon_ky_tinh_khau_hao_view.xml',
		# 'templates/asset_ghi_tang_template.xml',
		# 'templates/asset_tinh_khau_hao_template.xml',
		'templates/asset_templates.xml',
	
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
