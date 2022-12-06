# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
import datetime

class TIEN_LUONG_BANG_CHAM_CONG_CHI_TIET_MASTER(models.Model):
    _name = 'tien.luong.bang.cham.cong.chi.tiet.master'
    _description = 'Bảng chấm công'
    _inherit = ['mail.thread']
    TEN_BANG_CHAM_CONG = fields.Char(string='Tên bảng chấm công', help='Tên bảng chấm công')
    name = fields.Char(string='Name', help='Name',related='TEN_BANG_CHAM_CONG', oldname='NAME')
    TIEN_LUONG_BANG_CHAM_CONG_CHI_TIET_DETAIL_IDS = fields.One2many('tien.luong.bang.cham.cong.chi.tiet.detail', 'CHI_TIET_ID', string='Bảng chấm công chi tiết detail')
    ten_loai_cham_cong = fields.Char(string='Loại chấm công')
    LOAI_CHUNG_TU = fields.Integer(string='Tháng')
    thang = fields.Integer(string='Tháng', required=True)
    nam = fields.Char(string='Năm', required=True)
    so_ngay_cua_thang = fields.Integer(string="Số ngày của tháng")
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    LOAI_CHAM_CONG = fields.Selection([('CHAM_CONG_THEO_BUOI', 'Chấm công theo buổi'), ('CHAM_CONG_THEO_GIO', 'Chấm công theo giờ'), ], string='Loại chấm công', default='CHAM_CONG_THEO_BUOI')

    @api.model
    def default_get(self, fields):
        rec = super(TIEN_LUONG_BANG_CHAM_CONG_CHI_TIET_MASTER, self).default_get(fields)
        thang = self._context.get('default_thang')
        nam = self._context.get('default_nam')
        hinh_thuc_tao_cham_cong = self._context.get('default_hinh_thuc_tao_cham_cong')
        hinh_thuc_tao_cham_cong = self._context.get('default_hinh_thuc_tao_cham_cong')
        default_arr_list_don_vi = self._context.get('default_arr_list_don_vi')
        if thang and nam :
            rec['so_ngay_cua_thang'] = int(helper.Datetime.lay_so_ngay_trong_thang(int(nam),int(thang)))
        Loai_cham_cong = self._context.get('default_loai_cham_cong')
        ten_bang_cham_cong = self._context.get('default_ten_bang_cham_cong')
        if ten_bang_cham_cong:
            rec['TEN_BANG_CHAM_CONG'] = ten_bang_cham_cong

        cham_thu_bay = self.env['ir.config_parameter'].get_param('he_thong.LAM_VIEC_NGAY_THU_7')
        cham_chu_nhat = self.env['ir.config_parameter'].get_param('he_thong.LAM_VIEC_NGAY_CHU_NHAT')
        #sql tra ve 1 list employees
        nhan_vien_list = []
        arr_list_don_vi = []
        if default_arr_list_don_vi:
            arr_list_don_vi = default_arr_list_don_vi
        if hinh_thuc_tao_cham_cong == 'TAO_MOI':
            danh_sach_nhan_viens = self.lay_sql_tra_ve_danh_sach_nhan_vien_truong_hop_tao_moi_hoan_toan(arr_list_don_vi)
            for nhan_vien in danh_sach_nhan_viens:
                phong_ban = nhan_vien.get('MA_DON_VI') + ' - ' + nhan_vien.get('TEN_DON_VI') 
                nhan_vien_list += [(0,0,{
                    'SO_THU_TU' : nhan_vien.get('RowNumber'),
                    'PHONG_BAN': phong_ban,
                    'MA_NHAN_VIEN': nhan_vien.get('NHAN_VIEN_ID'),
                    'TEN_NHAN_VIEN' :nhan_vien.get('TEN_NHAN_VIEN'),
                })] 
        elif hinh_thuc_tao_cham_cong == 'LAY_DANH_SACH':
            default_bang_cham_cong_id = self._context.get('default_bang_cham_cong_id') #Lấy id của bảng chấm công truyền sang khi tích chọn là Lấy danh sách nhân viên của bảng chấm công khác
            default_LAY_TAT_CA_NHAN_VIEN_DA_NGUNG_THEO_DOI = self._context.get('default_LAY_TAT_CA_NHAN_VIEN_DA_NGUNG_THEO_DOI') #Lấy giá trị true hoặc false của trường lấy tất cả nhân viên đã ngừng theo dõi
            danh_sach_nhan_viens = self.lay_sql_tra_ve_danh_sach_nhan_vien_truong_hop_lay_danh_sach_nhan_vien_tu_bang_cham_cong_khac(arr_list_don_vi,default_bang_cham_cong_id,default_LAY_TAT_CA_NHAN_VIEN_DA_NGUNG_THEO_DOI)
            
            for nhan_vien in danh_sach_nhan_viens:
                phong_ban = nhan_vien.get('MA_DON_VI') + ' - ' + nhan_vien.get('TEN_DON_VI') 
                nhan_vien_list += [(0,0,{
                    'SO_THU_TU' : nhan_vien.get('STT'),
                    'PHONG_BAN': phong_ban,
                    'MA_NHAN_VIEN': nhan_vien.get('NHAN_VIEN_ID'),
                    'TEN_NHAN_VIEN' :nhan_vien.get('TEN_NHAN_VIEN_BAN_HANG'),
                    'LOAI_CHAM_CONG' :self._context.get('default_LOAI_CHAM_CONG'),
                })] 

        if Loai_cham_cong == 'Bảng chấm công theo buổi':
            rec['LOAI_CHUNG_TU'] = 6000
            rec['ten_loai_cham_cong'] = Loai_cham_cong
            for record in nhan_vien_list:
                so_cong = 0
                #get config xem co cham thu 7, chu nhat khong
                for i in range(1,rec['so_ngay_cua_thang']+1):
                    # ngay = 'NGAY_'+str(i)
                    #check xem hom do la thu may
                    check_thu_may = datetime.datetime(year=int(nam), month=int(thang), day=i).weekday()
                    if check_thu_may == 5: #
                        if cham_thu_bay == 'True':
                            record[2]['NGAY_'+str(i)] = '+'
                            so_cong += 1
                    elif check_thu_may == 6: #
                        if cham_chu_nhat == 'True':
                            record[2]['NGAY_'+str(i)] = '+'
                            so_cong += 1
                    else:
                        record[2]['NGAY_'+str(i)] = '+'
                        so_cong += 1
                record[2]['SO_CONG_HUONG'] = so_cong
        elif Loai_cham_cong == 'Bảng chấm công theo giờ':
            rec['LOAI_CHUNG_TU'] = 6001
            rec['ten_loai_cham_cong'] = Loai_cham_cong
            for record in nhan_vien_list:
                so_cong = 0
                #get config xem co cham thu 7, chu nhat khong
                for i in range(1,rec['so_ngay_cua_thang']+1):
                    # ngay = 'NGAY_'+str(i)
                    #check xem hom do la thu may
                    check_thu_may = datetime.datetime(year=int(nam), month=int(thang), day=i).weekday()
                    if check_thu_may == 5: #
                        if cham_thu_bay == 'True':
                            record[2]['NGAY_'+str(i)] = '+:8'
                            so_cong += 8
                    elif check_thu_may == 6: #
                        if cham_chu_nhat == 'True':
                            record[2]['NGAY_'+str(i)] = '+:8'
                            so_cong += 8
                    else:
                        record[2]['NGAY_'+str(i)] = '+:8'
                        so_cong += 8
                record[2]['SO_CONG_HUONG'] = so_cong
        
        rec ['TIEN_LUONG_BANG_CHAM_CONG_CHI_TIET_DETAIL_IDS'] = nhan_vien_list
                
        return rec
    
    def lay_sql_tra_ve_danh_sach_nhan_vien_truong_hop_lay_danh_sach_nhan_vien_tu_bang_cham_cong_khac(self,list_don_vi,id_bang_cham_cong,lay_tat_ca_nhan_vien_da_ngung_theo_doi):
        sql_param = {
            'don_vi_ids':list_don_vi ,
            'id_bang_cham_cong_khac': id_bang_cham_cong,
            'lay_tat_ca_nhan_vien_da_ngung_theo_doi': lay_tat_ca_nhan_vien_da_ngung_theo_doi,
        }
        query="""
            DO LANGUAGE plpgsql $$
            DECLARE

            id_bang_cham_cong_dua_tren      INTEGER := %(id_bang_cham_cong_khac)s;

            --@RefFollowID

            --id_bang_cham_cong_tao_moi       INTEGER := 16;

            --@RefID

            lay_ca_nhan_vien_ngung_theo_doi BOOLEAN := %(lay_tat_ca_nhan_vien_da_ngung_theo_doi)s;

            --@AddInactiveEmployee


            BEGIN


            DROP TABLE IF EXISTS TMMP_DON_VI
            ;

            CREATE TEMP TABLE TMMP_DON_VI

            (
            "DON_VI_ID" INT PRIMARY KEY
            )
            ;

            /*bảng chứa phòng ban được chọn*/
            INSERT INTO TMMP_DON_VI
            SELECT id

            FROM danh_muc_to_chuc
            WHERE id = any(%(don_vi_ids)s) --@OrganizationUnitIDList
            ;

            DROP TABLE IF EXISTS TMP_DON_VI_TU_BANG_CHAM_CONG_KHAC
            ;

            CREATE TEMP TABLE TMP_DON_VI_TU_BANG_CHAM_CONG_KHAC


            (
            "DON_VI_ID" INT
            )
            ;

            INSERT INTO TMP_DON_VI_TU_BANG_CHAM_CONG_KHAC
            SELECT A."DON_VI_ID"
            FROM tien_luong_bang_cham_cong_chi_tiet_detail A
            WHERE A."CHI_TIET_ID" = id_bang_cham_cong_dua_tren
            GROUP BY A."DON_VI_ID"
            ;

            DROP TABLE IF EXISTS TMP_KET_QUA
            ;

            CREATE TEMP TABLE TMP_KET_QUA

            (

            "NHAN_VIEN_ID"           INT,
            "DON_VI_ID"              INT,
            "MA_NHAN_VIEN"           VARCHAR(25),
            "TEN_NHAN_VIEN_BAN_HANG" VARCHAR(128),
            "MA_DON_VI"              VARCHAR(20),
            "TEN_DON_VI"             VARCHAR(128),
            "STT"                    INT
            )
            ;

            -- Lấy ra các dòng chi tiết
            INSERT INTO TMP_KET_QUA

            SELECT
            AO."id"         AS "NHAN_VIEN_ID"
            , G."DON_VI_ID"   AS "DON_VI_ID"
            , AO."MA"         AS "MA_NHAN_VIEN"
            , AO."HO_VA_TEN"  AS "TEN_NHAN_VIEN_BAN_HANG"
            , OU."MA_DON_VI"  AS "MA_DON_VI"
            , OU."TEN_DON_VI" AS "TEN_DON_VI"
            , PD."SO_THU_TU"

            FROM res_partner AS AO
            INNER JOIN TMMP_DON_VI AS G ON G."DON_VI_ID" = AO."DON_VI_ID"
                AND "LA_NHAN_VIEN" = TRUE
            INNER JOIN danh_muc_to_chuc OU ON AO."DON_VI_ID" = OU."id"
            INNER JOIN tien_luong_bang_cham_cong_chi_tiet_detail PD
            ON PD."MA_NHAN_VIEN" = AO."id"
            WHERE PD."CHI_TIET_ID" = id_bang_cham_cong_dua_tren
            AND (AO."active" = TRUE
            OR (AO."active" = FALSE AND lay_ca_nhan_vien_ngung_theo_doi = TRUE)
            )
            ;

            INSERT INTO TMP_KET_QUA
            SELECT
            AO."id"         AS "NHAN_VIEN_ID"
            , OU."id"         AS "DON_VI_ID"
            , AO."MA"         AS "MA_NHAN_VIEN"
            , AO."HO_VA_TEN"  AS "TEN_NHAN_VIEN_BAN_HANG"
            , OU."MA_DON_VI"  AS "MA_DON_VI"
            , OU."TEN_DON_VI" AS "TEN_DON_VI"
            , 0               AS "STT"

            FROM res_partner AS AO
            INNER JOIN danh_muc_to_chuc OU ON AO."DON_VI_ID" = OU."id"
            INNER JOIN TMMP_DON_VI AS G ON G."DON_VI_ID" = AO."DON_VI_ID"
            LEFT JOIN TMP_KET_QUA R ON AO."id" = R."NHAN_VIEN_ID"
            WHERE
            "LA_NHAN_VIEN" = TRUE
            AND (AO."active" = TRUE
            OR (AO."active" = FALSE AND lay_ca_nhan_vien_ngung_theo_doi = TRUE)
            )
            AND OU."id" NOT IN (SELECT "DON_VI_ID"
            FROM TMP_DON_VI_TU_BANG_CHAM_CONG_KHAC)
            AND R."NHAN_VIEN_ID" IS NULL
            ;


            DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
            ;

            CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
            AS


            SELECT
            ROW_NUMBER()
            OVER (
            ORDER BY
            "TEN_DON_VI"
            , "STT"
            , "MA_NHAN_VIEN" )  AS "RowNumber"
            , "NHAN_VIEN_ID"
            , "DON_VI_ID"
            , "MA_NHAN_VIEN"
            , "TEN_NHAN_VIEN_BAN_HANG"
            , "MA_DON_VI"
            , "TEN_DON_VI"
            , "STT"
            FROM TMP_KET_QUA

            ORDER BY
            "TEN_DON_VI"
            , "STT"
            , "MA_NHAN_VIEN"
            ;


            END $$
            ;

            SELECT *
            FROM TMP_KET_QUA_CUOI_CUNG

            ORDER BY "STT"
            ;
            """
        return self.execute(query,sql_param)
    
    def lay_sql_tra_ve_danh_sach_nhan_vien_truong_hop_tao_moi_hoan_toan(self,list_don_vi):
        sql_param = {
            'don_vi_ids':list_don_vi,
        }
        query="""
            DO LANGUAGE plpgsql $$
            DECLARE


            --id_chung_tu      INTEGER := 2; --@RefID

            che_do_chinh_sua INTEGER := 2;

            -- @EditMode

            BEGIN

            DROP TABLE IF EXISTS TMP_DON_VI
            ;

            CREATE TEMP TABLE TMP_DON_VI

            (
            "DON_VI_ID" INT
            )
            ;
            INSERT INTO TMP_DON_VI
            SELECT id
            FROM danh_muc_to_chuc
            WHERE id = any(%(don_vi_ids)s) --@OrganizationUnitID
            ;
            DROP TABLE IF EXISTS TMP_KET_QUA
            ;
            CREATE TEMP TABLE TMP_KET_QUA
            AS

            SELECT
            ROW_NUMBER()
            OVER (
            ORDER BY OU."MA_DON_VI", AO."MA" )  AS "RowNumber"

            ,0               AS "ID_CHUNG_TU_CHI_TIET"
            , AO."id"         AS "NHAN_VIEN_ID"
            , DRI."DON_VI_ID" AS "DON_VI_ID"
            , AO."MA"         AS "MA_NHAN_VIEN"
            , AO."HO_VA_TEN"  AS "TEN_NHAN_VIEN"
            , OU."TEN_DON_VI" AS "TEN_DON_VI"
            , OU."MA_DON_VI"  AS "MA_DON_VI"
            FROM TMP_DON_VI AS DRI
            INNER JOIN danh_muc_to_chuc AS OU ON DRI."DON_VI_ID" = OU."id"
            LEFT JOIN res_partner AS AO ON AO."DON_VI_ID" = DRI."DON_VI_ID"
            WHERE AO."LA_NHAN_VIEN" = TRUE AND (che_do_chinh_sua = 2 AND AO."active" = TRUE)
            ORDER BY OU."MA_DON_VI", AO."MA"
            ;

            END $$
            ;
            SELECT *
            FROM TMP_KET_QUA
            ORDER BY
            "RowNumber"
            ;
        """
        return self.execute(query,sql_param)





