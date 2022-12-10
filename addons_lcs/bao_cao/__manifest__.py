# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Báo cáo',
    'version': '1.0',
    'sequence': 0,
    'summary': 'Báo cáo tổng hợp',
    'depends': [
		'danh_muc',
		'account_ex',
		'stock_ex',
		'purchase_ex',
		'sale_ex',
		'gia_thanh',
    ],
    'data': [
		'views/bao_cao_tong_hop_lai_lo_theo_hop_dong_view.xml',
		'views/bao_cao_chi_tiet_lai_lo_theo_hop_dong_view.xml',
		'views/bao_cao_chi_tiet_lai_lo_theo_don_hang_view.xml',
		'views/bao_cao_gia_thanh_chi_tiet_lai_lo_theo_cong_trinh_view.xml',
		'views/bao_cao_gia_thanh_tong_hop_lai_lo_theo_cong_trinh_view.xml',
		'views/bao_cao_gia_thanh_bang_tong_hop_chi_phi_view.xml',
		'views/bao_cao_gia_thanh_bang_ke_phieu_nhap_phieu_xuat_theo_doi_tuong_view.xml',
		'views/bao_cao_gia_thanh_tong_hop_nhap_xuat_kho_theo_doi_tuong_view.xml',
		'views/bao_cao_gia_thanh_so_chi_tiet_tai_khoan_chi_phi_san_xuat.xml',
		'views/bao_cao_gia_thanh_tong_hop_chi_phi_sxkd_view.xml',
		'templates/bao_cao_dieu_chuyen_ccdc_template.xml',
		'templates/bao_cao_don_dat_hang_chi_phi_du_kien_template.xml',
		'views/bao_cao_chi_phi_du_kien_theo_don_dat_hang_view.xml',
		'templates/bao_cao_don_dat_hang_chi_co_so_luong_template.xml',
		'templates/bao_cao_don_dat_hang_bao_gom_nguyen_vat_lieu_template.xml',
		'templates/bao_cao_lenh_thao_do_template.xml',
		'templates/bao_cao_lenh_lap_rap_template.xml',
		'templates/bao_cao_lenh_san_xuat_template.xml',
		'templates/bao_cao_bao_gia_template.xml',
		'views/bao_cao_f01dnn_bang_can_doi_tai_khoan_view.xml',
		'views/bao_cao_b02dn_bao_cao_ket_qua_hoat_dong_kinh_doanh_view.xml',
		'views/bao_cao_b03dn_bao_cao_luu_chuyen_tien_te_pp_truc_tiep_view.xml',
		'views/bao_cao_b03dn_gt_bao_cao_luu_chuyen_tien_te_pp_gian_tiep_view.xml',
		'views/bao_cao_tong_hop_cong_no_nhan_vien_view.xml',
		'views/bao_cao_bang_ke_hoa_don_chung_tu_ban_ra_view.xml',
		'views/bao_cao_tinh_hinh_thuc_hien_don_dat_hang_view.xml',
		'views/bao_cao_b01dn_bang_can_doi_ke_toan_view.xml',
		'views/bao_cao_bang_can_doi_tai_khoan_view.xml',
		'views/bao_cao_tong_hop_luong_nhan_vien_view.xml',
		'views/bao_cao_bang_tong_hop_thanh_toan_tien_luong_bang_luong_thoi_gian_view.xml',
		'views/bao_cao_bang_tong_hop_thanh_toan_tien_luong_bang_luong_co_dinh_view.xml',
		'views/bao_cao_bang_ke_hoa_don_chung_tu_mua_vao_view.xml',
		'views/bao_cao_bang_tong_hop_quyet_toan_thue_gtgt_nam_view.xml',
		# 'templates/bao_cao_s34_dn_template.xml',
		# 'templates/bao_cao_bao_cao_tien_do_san_xuat_template.xml',
		'views/bao_cao_tong_hop_ban_hang_view.xml',
		# 'templates/bao_cao_so_tai_san_co_dinh_template.xml',
		# 'templates/bao_cao_s21_dn_so_tai_san_co_dinh_template.xml',
		'views/bao_cao_s21_dn_so_tai_san_co_dinh_view.xml',
		'views/bao_cao_so_theo_doi_cong_cu_dung_cu_view.xml',
		# 'templates/bao_cao_so_theo_doi_cong_cu_dung_cu_template.xml',
		'views/bao_cao_so_chi_tiet_vat_tu_hang_hoa_view.xml',
		'views/bao_cao_s10_dn_so_chi_tiet_vat_lieu_cong_cu_view.xml',
		'views/bao_cao_tong_hop_ton_kho_view.xml',
		'views/bao_cao_tong_hop_mua_hang_view.xml',
		'views/bao_cao_s01_dn_nhat_ky_so_cai_view.xml',
		'views/bao_cao_s02b_dn_so_dang_ky_chung_tu_ghi_so_view.xml',
		'views/bao_cao_s02_c1_dn_so_cai_hinh_thuc_chung_tu_ghi_so_view.xml',
		'views/bao_cao_so3b_dn_so_cai_hinh_thuc_nhat_ky_chung_view.xml',
		'views/bao_cao_so_chi_tiet_cac_tai_khoan_view.xml',
		'views/bao_cao_s03_a2_dn_so_nhat_ky_chi_tien_view.xml',
		'views/bao_cao_s03a1_dn_so_nhat_ky_thu_tien_view.xml',
		'views/bao_cao_bang_tinh_gia_thanh_view.xml',
		# 'views/bao_cao_s37_dn_the_tinh_gia_thanh_san_pham_dich_vu_view.xml',
		# 'views/bao_cao_s36_dn_so_chi_phi_san_xuat_va_kinh_doanh_view.xml',
		'views/bao_cao_so_ke_toan_chi_tiet_quy_tien_mat_view.xml',
		'views/bao_cao_bao_cao_so_sanh_so_luong_ban_va_doanh_so_theo_ky_view.xml',
		'views/bao_cao_phan_tich_so_luong_ban_va_doanh_so_theo_nam_view.xml',
		'views/bao_cao_tong_hop_lai_lo_theo_don_hang_view.xml',
		'views/bao_cao_phan_tich_cong_no_phai_thu_theo_tuoi_no_view.xml',
		'views/bao_cao_chi_tiet_cong_no_phai_thu_khach_hang_view.xml',
		'views/bao_cao_tong_hop_ton_kho_theo_lo_view.xml',
		'views/bao_cao_so_quy_tien_mat_view.xml',
		'views/bao_cao_so_chi_tiet_tai_khoan_theo_doi_tuong_tap_hop_chi_phi_va_khoan_muc_chi_phi_view.xml',
		'views/bao_cao_so_chi_tiet_tai_khoan_theo_doi_tuong_view.xml',
		'views/bao_cao_s34_dn_view.xml',
		'views/bao_cao_so_31_dn_so_chi_tiet_thanh_toan_nguoi_mua_hoac_nguoi_ban_view.xml',
		'views/bao_cao_so_nhat_ky_chung_view.xml',
		'views/bao_cao_bien_ban_doi_chieu_va_xac_nhan_cong_no_phai_tra_view.xml',
		'views/bao_cao_phan_tich_cong_no_phai_tra_theo_tuoi_no_view.xml',
		'views/bao_cao_chi_tiet_cong_no_phai_tra_nha_cung_cap_view.xml',
		'views/bao_cao_tong_hop_cong_no_phai_tra_view.xml',
		'views/bao_cao_so_chi_tiet_mua_hang_view.xml',
		'views/bao_cao_bang_ke_thu_mua_hang_view.xml',
		'views/bao_cao_so_tai_san_co_dinh_view.xml',
		'views/bao_cao_tai_san_co_dinh_view.xml',
		'views/bao_cao_so_chi_tiet_ban_hang_view.xml',
		'views/bao_cao_tong_hop_cong_no_phai_thu_khach_hang_view.xml',
		'views/bao_cao_s35_dn_so_chi_tiet_ban_hang_view.xml',
		
		'views/bao_cao_loai_ccdc_view.xml',
		'views/bao_cao_the_kho_view.xml',
		'views/bao_cao_bao_cao_tien_do_san_xuat_view.xml',
		'views/bao_cao_so_chi_tiet_vat_lieu_cong_cu_view.xml',
		'views/bao_cao_nhom_vthh_view.xml',
        'views/bao_cao_bang_ke_so_du_ngan_hang_view.xml',
		'views/bao_cao_so_tien_gui_ngan_hang_view.xml',
		'views/bao_cao_thong_bao_cong_no.xml',
		'views/bao_cao_tuy_chon_in.xml',
		'views/bao_cao_tuy_chinh_tieu_de.xml',
		'views/bao_cao_quan_ly_mau_in.xml',		
		'templates/bao_cao_thong_bao_cong_no_template.xml',
		'templates/bao_cao_templates.xml',
		'templates/bao_cao_so_tien_gui_ngan_hang_template.xml',		
		'templates/bao_cao_02_vt_phieu_xuat_kho_template.xml',		
		'templates/bao_cao_01_vt_phieu_nhap_kho_template.xml',		
		'templates/bao_cao_phieu_thu_mau_day_du_template.xml',		
		'templates/bao_cao_01_TT_phieu_thu_a5_template.xml',
		'templates/bao_cao_01_TT_phieu_thu_mau_2_lien_template.xml',
		'templates/bao_cao_01_TT_phieu_thu_template.xml',
		'templates/bao_cao_02_TT_phieu_chi_template.xml',
		'templates/bao_cao_02_TT_phieu_chi_mau_2_lien_template.xml',
		'templates/bao_cao_02_TT_phieu_chi_a5_template.xml',
		'templates/bao_cao_phieu_chi_mau_day_du_template.xml',
		'templates/bao_cao_giay_bao_no_template.xml',
		'templates/bao_cao_uy_nhiem_chi_shb_template.xml',
		'templates/bao_cao_uy_nhiem_chi_agribank_template.xml',
		'templates/bao_cao_uy_nhiem_chi_mb_template.xml',
		'templates/bao_cao_uy_nhiem_chi_techcombank_template.xml',
		'templates/bao_cao_uy_nhiem_chi_vietcombank_template.xml',
		'templates/bao_cao_uy_nhiem_chi_viettinbank_template.xml', 
		'templates/bao_cao_uy_nhiem_chi_bidv_template.xml', 
		'templates/bao_cao_uy_nhiem_chi_pvcombank_template.xml', 
		'templates/bao_cao_phieu_xuat_kho_02vt_mau_a5_template.xml',
		'templates/bao_cao_chung_tu_ke_toan_template.xml',
		'templates/bao_cao_giay_bao_co_template.xml',
		'templates/bao_cao_phieu_xuat_kho_ban_hang_template.xml',
		'templates/bao_cao_chung_tu_ghi_tang_tscd_template.xml',
		'templates/bao_cao_don_dat_hang_template.xml',
		'templates/bao_cao_don_mua_hang_template.xml',
		'templates/bao_cao_hop_dong_ban_ben_A_ban_template.xml',
		'templates/bao_cao_hop_dong_ban_ben_A_mua_template.xml',
		'templates/bao_cao_chung_tu_ghi_giam_ccdc_template.xml',
		'templates/bao_cao_bien_ban_kiem_ke_template.xml',
		'templates/bao_cao_bang_tinh_khau_hao_tscd_template.xml',
		'templates/bao_cao_dieu_chinh_cong_cu_dung_cu_template.xml',
		'templates/bao_cao_chung_tu_ghi_tang_ccdc_template.xml',
		'templates/bao_cao_bang_can_doi_tai_khoan_template.xml',
		'templates/bao_cao_f01dnn_bang_can_doi_tai_khoan_template.xml',
		'templates/bao_cao_b01dn_bang_can_doi_ke_toan_template.xml',
		'templates/bao_cao_b02dn_bao_cao_ket_qua_hoat_dong_kinh_doanh_template.xml',
		'templates/bao_cao_b03dn_bao_cao_luu_chuyen_tien_te_pp_truc_tiep_template.xml',
		'templates/bao_cao_phieu_xuat_kho_ban_hang_mau_a5_template.xml',
		'templates/bao_cao_b03dngt_bao_cao_luu_chuyen_tien_te_pp_gian_tiep_template.xml',
		'templates/bao_cao_bang_ke_hoa_don_chung_tu_hang_hoa_dich_vu_mua_vao_template.xml',
		'templates/bao_cao_phieu_xuat_kho_ban_hang_mau_a5_doc_template.xml',
		'templates/bao_cao_bang_ke_hoa_don_chung_tu_hang_hoa_dich_vu_ban_ra_template.xml',
		'templates/bao_cao_s10_dn_so_chi_tiet_vat_lieu_dung_cu_template.xml',
		'templates/bao_cao_s21_dn_so_tai_san_co_dinh_template.xml',
		'templates/bao_cao_don_dat_hang_tu_chung_tu_ban_hang_template.xml',
		'templates/bao_cao_phieu_xuat_kho_tong_hop_template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}