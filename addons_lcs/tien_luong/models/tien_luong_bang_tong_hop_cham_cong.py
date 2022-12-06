# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_LUONG_BANG_TONG_HOP_CHAM_CONG(models.Model):
    _name = 'tien.luong.bang.tong.hop.cham.cong'
    _description = 'Bảng tổng hợp chấm công'
    _inherit = ['mail.thread']
    THANG = fields.Integer(string='Tháng', help='Tháng')
    NAM = fields.Char(string='Năm', help='Năm')
    LOAI_CHAM_CONG = fields.Char(string='Loại chấm công', help='Loại chấm công')
    TEN_BANG_CHAM_CONG = fields.Char(string='Tên bảng chấm công', help='Tên bảng chấm công')
    LOAI_CHUNG_TU = fields.Integer(string='Tháng')
    name = fields.Char(string='Name', help='Name',related='TEN_BANG_CHAM_CONG',  oldname='NAME')

    
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

    TIEN_LUONG_BANG_TONG_HOP_CHAM_CONG_CHI_TIET_IDS = fields.One2many('tien.luong.bang.tong.hop.cham.cong.chi.tiet', 'CHI_TIET_ID', string='Bảng tổng hợp chấm công chi tiết')

    @api.model
    def default_get(self, fields):
        rec = super(TIEN_LUONG_BANG_TONG_HOP_CHAM_CONG, self).default_get(fields)
        thang = self._context.get('default_THANG')
        nam = self._context.get('default_NAM')
        if thang:
            rec['THANG'] = int(thang)
        if nam:
            rec['NAM'] = nam
        loai_cham_cong = self._context.get('default_loai_cham_cong')
        if loai_cham_cong:
            if loai_cham_cong == 'Tổng hợp chấm công theo buổi':
                rec['LOAI_CHAM_CONG'] = loai_cham_cong
                rec['LOAI_CHUNG_TU'] = 6010
            elif loai_cham_cong == 'Tổng hợp chấm công theo giờ':
                rec['LOAI_CHAM_CONG'] = loai_cham_cong
                rec['LOAI_CHUNG_TU'] = 6011
        rec['TEN_BANG_CHAM_CONG'] = self._context.get('default_TEN_BANG_CHAM_CONG')

        default_arr_list_don_vi = self._context.get('default_arr_list_don_vi')
        default_TONG_HOP_TU_CAC_BANG_CHAM_CONG_CHI_TIET = self._context.get('default_TONG_HOP_TU_CAC_BANG_CHAM_CONG_CHI_TIET')
        nhan_vien_list = []
        arr_list_don_vi = []
        if default_arr_list_don_vi:
            arr_list_don_vi = default_arr_list_don_vi
        
        chi_nhanh_id = self.get_chi_nhanh()
        if default_TONG_HOP_TU_CAC_BANG_CHAM_CONG_CHI_TIET: # Nếu là Tổng hợp chấm công dựa từ các bảng chấm công chi tiết
            is_tong_hop_cham_cong_theo_buoi = None #khai báo một biến để check xem đây là Bảng chấm công theo buổi hay theo giờ
            loai_chung_tu = 0
            if loai_cham_cong == 'Tổng hợp chấm công theo buổi':
                loai_chung_tu = 6000
                is_tong_hop_cham_cong_theo_buoi = True # = True nếu chấm công theo buổi
            elif loai_cham_cong == 'Tổng hợp chấm công theo giờ':
                loai_chung_tu = 6001
                is_tong_hop_cham_cong_theo_buoi = False # = False nếu chấm công theo giờ
            danh_sach_nhan_viens = self.lay_sql_tra_ve_danh_sach_nhan_vien_tong_hop_tu_cac_bang_cham_cong_chi_tiet(arr_list_don_vi,chi_nhanh_id,thang,nam,loai_chung_tu)
            for nhan_vien in danh_sach_nhan_viens:
                # Lần lượt lấy từng ngày công của nhân viên ra và kiểm tra : Nếu thuộc  ky_hieu_cong_huong_100 thì 
                con_om = 0
                hoi_nghi_hoc_tap = 0
                lao_dong_nghia_vu = 0
                luong_san_pham = 0
                luong_thoi_gian_ca_ngay = 0
                luong_thoi_gian_nua_ngay = 0
                nghi_bu = 0
                nghi_khong_luong = 0
                nghi_phep = 0
                ngung_viec = 0
                om_dieu_duong = 0
                tai_nan = 0
                thai_san = 0

                for i in range(1,32):
                    env_bang_cham_cong_chi_tiet = self.env['tien.luong.bang.cham.cong.chi.tiet.detail']
                    du_lieu_ngay = env_bang_cham_cong_chi_tiet.lay_du_lieu_chuan(nhan_vien.get('NGAY_' + str(i),''), is_tong_hop_cham_cong_theo_buoi)
                    
                    if is_tong_hop_cham_cong_theo_buoi == True: #Nếu chấm công là theo buổi
                        # For lần lượt trong du_lieu_ngay ={}
                        for ky_hieu in du_lieu_ngay:
                            if ky_hieu == 'Cô':
                                con_om += 1
                            if ky_hieu == 'Cô1/2':
                                con_om += 0.5
                            if ky_hieu == 'H':
                                hoi_nghi_hoc_tap += 1
                            if ky_hieu == 'H1/2':
                                hoi_nghi_hoc_tap += 0.5
                            if ky_hieu == 'LĐ':
                                lao_dong_nghia_vu += 1
                            if ky_hieu == 'LĐ1/2':
                                lao_dong_nghia_vu += 0.5
                            if ky_hieu == 'SP':
                                luong_san_pham += 1
                            if ky_hieu == '+':
                                luong_thoi_gian_ca_ngay += 1
                            if ky_hieu == '-':
                                luong_thoi_gian_nua_ngay += 0.5
                            if ky_hieu == 'NB':
                                nghi_bu += 1
                            if ky_hieu == 'NB1/2':
                                nghi_bu += 0.5
                            if ky_hieu == 'KL':
                                nghi_khong_luong += 1
                            if ky_hieu == 'KL1/2':
                                nghi_khong_luong += 0.5
                            if ky_hieu == 'P':
                                nghi_phep += 1
                            if ky_hieu == 'P1/2':
                                nghi_phep += 0.5
                            if ky_hieu == 'N':
                                ngung_viec += 1
                            if ky_hieu == 'N1/2':
                                ngung_viec += 0.5
                            if ky_hieu == 'Ô':
                                om_dieu_duong += 1
                            if ky_hieu == 'Ô1/2':
                                om_dieu_duong += 0.5
                            if ky_hieu == 'T':
                                tai_nan += 1
                            if ky_hieu == 'T1/2':
                                tai_nan += 0.5
                            if ky_hieu == 'TS':
                                thai_san += 1
                            if ky_hieu == 'TS1/2':
                                thai_san += 0.5
                    elif is_tong_hop_cham_cong_theo_buoi == False: #Nếu chấm công là theo giờ
                        # For lần lượt trong du_lieu_ngay ={}
                        for ky_hieu in du_lieu_ngay:
                            if ky_hieu == 'Cô' or ky_hieu == 'Cô1/2':
                                con_om += du_lieu_ngay[ky_hieu]
                            if ky_hieu == 'H' or ky_hieu == 'H1/2':
                                hoi_nghi_hoc_tap += du_lieu_ngay[ky_hieu]
                            if ky_hieu == 'LĐ' or ky_hieu == 'LĐ1/2':
                                lao_dong_nghia_vu += du_lieu_ngay[ky_hieu]
                            if ky_hieu == 'SP':
                                luong_san_pham += du_lieu_ngay[ky_hieu]
                            if ky_hieu == '+':
                                luong_thoi_gian_ca_ngay += du_lieu_ngay[ky_hieu]
                            if ky_hieu == '-':
                                luong_thoi_gian_nua_ngay += du_lieu_ngay[ky_hieu]
                            if ky_hieu == 'NB' or ky_hieu == 'NB1/2':
                                nghi_bu += du_lieu_ngay[ky_hieu]
                            if ky_hieu == 'KL'or ky_hieu == 'KL1/2':
                                nghi_khong_luong += du_lieu_ngay[ky_hieu]
                            if ky_hieu == 'P' or ky_hieu == 'P1/2':
                                nghi_phep += du_lieu_ngay[ky_hieu]
                            if ky_hieu == 'N' or ky_hieu == 'N1/2': 
                                ngung_viec += du_lieu_ngay[ky_hieu]
                            if ky_hieu == 'Ô' or ky_hieu == 'Ô1/2':
                                om_dieu_duong += du_lieu_ngay[ky_hieu]
                            if ky_hieu == 'T' or ky_hieu == 'T1/2':
                                tai_nan += du_lieu_ngay[ky_hieu]
                            if ky_hieu == 'TS' or ky_hieu == 'TS1/2':
                                thai_san += du_lieu_ngay[ky_hieu]
                            
                nhan_vien_list += [(0,0,{
                    'STT' : nhan_vien.get('SO_THU_TU'),
                    'PHONG_BAN': nhan_vien.get('PHONG_BAN'),
                    'MA_NHAN_VIEN': nhan_vien.get('MA_NHAN_VIEN'),
                    'TEN_NHAN_VIEN' :nhan_vien.get('TEN_NHAN_VIEN'),
                    'CON_OM' :con_om,
                    'HOI_NGHI_HOC_TAP' :hoi_nghi_hoc_tap,
                    'LAO_DONG_NGHIA_VU' :lao_dong_nghia_vu,
                    'LUONG_SAN_PHAM' :luong_san_pham,
                    'LUONG_THOI_GIAN_CA_NGAY' :luong_thoi_gian_ca_ngay,
                    'LUONG_THOI_GIAN_NUA_NGAY' :luong_thoi_gian_nua_ngay,
                    'NGHI_BU' :nghi_bu,
                    'NGHI_KHONG_LUONG' :nghi_khong_luong,
                    'NGHI_PHEP' :nghi_phep,
                    'NGUNG_VIEC' :ngung_viec,
                    'OM_DIEU_DUONG' :om_dieu_duong,
                    'TAI_NAN' :tai_nan,
                    'THAI_SAN' :thai_san,
                    'SO_CONG_HUONG' :nhan_vien.get('SO_CONG_HUONG'),
                    'SO_CONG_KHONG_HUONG' :nhan_vien.get('SO_CONG_KHONG_HUONG'),
                    'NGAY_THUONG_BAN_NGAY' :nhan_vien.get('NGAY_THUONG_BAN_NGAY'),
                    'THU_BAY_CHU_NHAT_BAN_NGAY' :nhan_vien.get('THU_BAY_CHU_NHAT_BAN_NGAY'),
                    'LE_TET_BAN_NGAY' :nhan_vien.get('LE_TET_BAN_NGAY'),
                    'NGAY_THUONG_BAN_DEM' :nhan_vien.get('NGAY_THUONG_BAN_DEM'),
                    'THU_BAY_CHU_NHAT_BAN_DEM' :nhan_vien.get('THU_7_CHU_NHAT_BAN_DEM'),
                    'LE_TET_BAN_DEM' :nhan_vien.get('LE_TET_BAN_DEM'),
                    'TONG' :nhan_vien.get('TONG_LAM_THEM'),
                })] 
        else: # Nếu là tạo mới hoàn toàn
            env = self.env['tien.luong.bang.cham.cong.chi.tiet.master']# Tạo 1 đối tượng là Tiền lương bảng chấm công để gọi hàm 
            danh_sach_nhan_viens = env.lay_sql_tra_ve_danh_sach_nhan_vien_truong_hop_tao_moi_hoan_toan(arr_list_don_vi)
            if danh_sach_nhan_viens:
                for nhan_vien in danh_sach_nhan_viens:
                    phong_ban = nhan_vien.get('MA_DON_VI') + ' - ' + nhan_vien.get('TEN_DON_VI') 
                    nhan_vien_list += [(0,0,{
                        'STT' : nhan_vien.get('RowNumber'),
                        'PHONG_BAN': phong_ban,
                        'MA_NHAN_VIEN': nhan_vien.get('NHAN_VIEN_ID'),
                        'TEN_NHAN_VIEN' :nhan_vien.get('TEN_NHAN_VIEN'),
                        'CON_OM' :0,
                        'HOI_NGHI_HOC_TAP' :0,
                        'LAO_DONG_NGHIA_VU' :0,
                        'LUONG_SAN_PHAM' :0,
                        'LUONG_THOI_GIAN_CA_NGAY' :0,
                        'LUONG_THOI_GIAN_NUA_NGAY' :0,
                        'NGHI_BU' :0,
                        'NGHI_KHONG_LUONG' :0,
                        'NGHI_PHEP' :0,
                        'NGUNG_VIEC' :0,
                        'OM_DIEU_DUONG' :0,
                        'TAI_NAN' :0,
                        'THAI_SAN' :0,
                        'SO_CONG_HUONG' :0,
                        'SO_CONG_KHONG_HUONG' :0,
                        'NGAY_THUONG_BAN_NGAY' :0,
                        'THU_BAY_CHU_NHAT_BAN_NGAY' :0,
                        'LE_TET_BAN_NGAY' :0,
                        'NGAY_THUONG_BAN_DEM' :0,
                        'THU_BAY_CHU_NHAT_BAN_DEM' :0,
                        'LE_TET_BAN_DEM' :0,
                        'TONG' :0,
                        })]
        rec['TIEN_LUONG_BANG_TONG_HOP_CHAM_CONG_CHI_TIET_IDS'] = nhan_vien_list
        return rec
    
    def lay_sql_tra_ve_danh_sach_nhan_vien_tong_hop_tu_cac_bang_cham_cong_chi_tiet(self,list_don_vi,chi_nhanh_id,thang,nam,loai_chung_tu):
        sql_param = {
            'don_vi_ids':list_don_vi ,
            'chi_nhanh_id':chi_nhanh_id ,
            'thang': int(thang),
            'nam': int(nam),
            'loai_chung_tu': loai_chung_tu,
        }
        query="""
            DO LANGUAGE plpgsql $$
DECLARE

    chi_nhanh_id       INTEGER := %(chi_nhanh_id)s;


    ky_cham_cong_thang INTEGER := %(thang)s;

    ky_cham_cong_nam   VARCHAR(100) := %(nam)s;

    loai_chung_tu      INTEGER := %(loai_chung_tu)s;

    id_chung_tu        INTEGER;


BEGIN


    SELECT "id"
    INTO id_chung_tu
    FROM tien_luong_bang_cham_cong_chi_tiet_master
    WHERE "CHI_NHANH_ID" = chi_nhanh_id
          AND "thang" = ky_cham_cong_thang
          AND "nam" = ky_cham_cong_nam
          AND "LOAI_CHUNG_TU" = loai_chung_tu
    ;

    DROP TABLE IF EXISTS TMP_TEMP
    ;

    CREATE TEMP TABLE TMP_TEMP


    (
        "DON_VI_ID" INT
    )
    ;

    INSERT INTO TMP_TEMP
    ("DON_VI_ID"
    )
        SELECT id

        FROM danh_muc_to_chuc
        WHERE id = any(%(don_vi_ids)s) --@ListOrgID
    ;

    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA
        AS

            SELECT
                PAD.*
                , COALESCE(AO."MA", '')         AS "MA_NHAN_VIEN_CHAM_CONG"
                , COALESCE(AO."HO_VA_TEN", '')  AS "TEN_NHAN_VIEN_CHAM_CONG"
                , COALESCE(OU."TEN_DON_VI", '') AS "TEN_DON_VI"
                , AO."CHUC_DANH"

            FROM tien_luong_bang_cham_cong_chi_tiet_detail PAD
                INNER JOIN tien_luong_bang_cham_cong_chi_tiet_master PA ON PAD."CHI_TIET_ID" = PA."id"
                LEFT JOIN res_partner AS AO ON PAD."MA_NHAN_VIEN" = AO."id"
                LEFT JOIN danh_muc_to_chuc AS OU ON OU."id" = AO."DON_VI_ID"
                INNER JOIN TMP_TEMP T ON PAD."DON_VI_ID" = T."DON_VI_ID"
            WHERE PA."LOAI_CHUNG_TU" = loai_chung_tu
                  AND PA."CHI_NHANH_ID" = chi_nhanh_id
                 AND
                  PA."thang" = ky_cham_cong_thang 
                 AND PA."nam" = ky_cham_cong_nam
    ;


END $$
;

SELECT *
FROM TMP_KET_QUA
order by "SO_THU_TU"
;
            """
        return self.execute(query,sql_param)
