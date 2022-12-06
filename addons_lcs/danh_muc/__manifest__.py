# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Danh mục',
    'version': '1.0',
    'sequence': 0,
    'summary': 'Danh mục',
    'depends': [
        'base',
        'mail',
        'web',
				'decimal_precision',
				'auth_signup',
    ],
    'data': [
		'views/danh_muc_vat_tu_hang_hoa_thiet_lap_cong_thuc_tinh_so_luong_form_view.xml',
		'views/danh_muc_thue_suat_gia_tri_gia_tang_view.xml',
		'views/danh_muc_dsct_phat_sinh_ma_quy_cach_form_view.xml',
		'views/danh_muc_bieu_tinh_thue_thu_nhap_tien_luong_view.xml',
		'views/danh_muc_ky_hieu_cham_cong_tien_luong_view.xml',
		'views/danh_muc_nhom_vat_tu_hang_hoa_dich_vu_view.xml',
		'views/danh_muc_dinh_khoan_tu_dong_view.xml',
		'views/danh_muc_he_thong_tai_khoan_view.xml',
		'templates/danh_muc_lenh_san_xuat_template.xml',
		'views/danh_muc_lenh_san_xuat_view.xml',
		'views/danh_muc_don_vi_tinh_view.xml',
		'views/danh_muc_kho_view.xml',
		'views/danh_muc_vat_tu_hang_hoa_don_gia_mua_co_dinh_form_view.xml',
		'views/danh_muc_vat_tu_hang_hoa_don_gia_mua_gan_nhat_form_view.xml',
		'views/danh_muc_vat_tu_hang_hoa_nhap_don_gia_ban_form_view.xml',
		'views/danh_muc_ma_thong_ke_view.xml',
		'views/danh_muc_dieu_khoan_thanh_toan_view.xml',
		'views/danh_muc_tai_khoan_ngan_hang_view.xml',
		'views/danh_muc_khoan_muc_cp_view.xml',
		'views/danh_muc_nhom_khach_hang_nha_cung_cap_view.xml',
		'views/danh_muc_ngan_hang_view.xml',
		'views/danh_muc_loai_tai_san_co_dinh_view.xml',
		'views/danh_muc_loai_cong_cu_dung_cu_view.xml',
		'views/danh_muc_doi_tuong_view.xml',
		'views/danh_muc_co_cau_to_chuc_view.xml',
		'views/danh_muc_vat_tu_hang_hoa_view.xml',
		'views/danh_muc_doi_tuong_phan_bo_view.xml',
		'views/danh_muc_tai_khoan_ngam_dinh_view.xml',
		'views/danh_muc_bieu_thue_tieu_thu_dac_biet_view.xml',
		'views/danh_muc_bieu_thue_tai_nguyen_view.xml',
		'views/danh_muc_loai_cong_trinh_view.xml',
		'views/danh_muc_tai_khoan_ket_chuyen_view.xml',
		'views/danh_muc_import_dau_ky_views.xml',
		'views/danh_muc_res_partner_view.xml',
		'views/danh_muc_cong_trinh_view.xml',
		'views/danh_muc_doi_tuong_tap_hop_chi_phi_view.xml',
		'views/danh_muc_loai_chung_tu_view.xml',
		'views/danh_muc_mau_so_hd_view.xml',
		'views/danh_muc_nhom_hhdv_view.xml',
		'views/danh_muc_loai_tien_view.xml',
		'views/danh_muc_thanh_pham_view.xml',
		'views/danh_muc_ky_tinh_gia_thanh_view.xml',
		'templates/danh_muc_templates.xml',
		'data/danh_muc_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
