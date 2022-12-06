# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Tiện ích',
    'version': '1.0',
    'sequence': 0,
    'summary': 'Module tiện ích',
    'depends': [
        'danh_muc',
        'account_ex',
        'stock_ex',
        'he_thong',
    ],
    'data': [
        'views/tien_ich_thuyet_minh_bao_cao_tai_chinh_chi_tiet_view.xml',
        'views/tong_hop_bctc_them_phu_luc_form_view.xml',
		'templates/tong_hop_bao_cao_tai_chinh_template.xml',
		'views/tong_hop_bctc_chon_nghiep_vu_va_hoat_dong_lctt_form_view.xml',
		'views/tong_hop_bctc_chon_lai_hoat_dong_lctt_form_view.xml',
		'views/tong_hop_bctc_chon_nghiep_vu_cho_cac_chung_tu_form_view.xml',
		'views/tong_hop_bctc_kiem_tra_bang_ke_toan_khong_can_form_view.xml',
		'views/tong_hop_bao_cao_tai_chinh_view.xml',
		'views/tong_hop_lap_bao_cao_tai_chinh_view.xml',
		'views/tien_ich_tinh_hinh_thnvdvnnpnkt_chi_tiet_view.xml',
		'views/tien_ich_tinh_hinh_thnvdvnnpntk_chi_tiet_view.xml',
		'views/tien_ich_tinh_hinh_thnvdvnndntk_chi_tiet_view.xml',
		'views/tien_ich_bao_cao_tai_chinh_chi_tiet_view.xml',
        'views/tien_ich_kiem_tra_cong_thuc_thiet_lap_trung_lap_view.xml',
        'views/tien_ich_thiet_lap_bao_cao_tai_chinh_view.xml',
        'views/tien_ich_bao_tri_du_lieu_view.xml',
        'views/tien_ich_kiem_tra_doi_chieu_chung_tu_so_sach_view.xml',
        'views/tien_ich_bao_cao_view.xml',
        'views/tien_ich_tim_kiem_chung_tu_view.xml',
        # 'views/tien_ich_tim_kiem_chung_tu_cac_dieu_kien_da_chon_view.xml',
        # 'views/tien_ich_tim_kiem_chung_tu_ket_qua_tim_kiem_view.xml',
        'views/tien_ich_ghi_so_hoac_bo_ghi_so_theo_lo_view.xml',
        # 'views/tien_ich_ghi_so_hoac_bo_ghi_so_theo_lo_phan_he_view.xml',
        # 'views/tien_ich_danh_lai_so_chung_tu_chi_tiet_view.xml',
        'views/tien_ich_danh_lai_so_chung_tu_view.xml',
        'templates/tien_ich_templates.xml',


    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
