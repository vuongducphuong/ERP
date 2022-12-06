# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Thuế',
    'version': '1.0',
    'sequence': 0,
    'summary': 'Module mẫu',
    'depends': [
        'danh_muc',
        'account_ex',
        'tong_hop',
    ],
    'data': [
		'views/thue_thiet_lap_thong_tin_co_quan_thue_view.xml',
		'views/thue_nop_thue_form_view.xml',
		'views/thue_chung_tu_khong_hop_le_view.xml',
		'views/thue_chon_ky_tinh_thue_khau_tru_thue_gtgt_view.xml',
		'views/thue_chon_ky_tinh_thue_view.xml',
		'views/thue_thue_view.xml',
		'templates/thue_templates.xml',

	
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
