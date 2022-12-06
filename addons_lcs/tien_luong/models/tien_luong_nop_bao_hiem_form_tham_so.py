# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError

class TIEN_LUONG_NOP_BAO_HIEM_FORM_THAM_SO(models.Model):
    _name = 'tien.luong.nop.bao.hiem.form.tham.so'
    _description = ''
    _auto = False

    NGAY_NOP_BAO_HIEM = fields.Date(string='Ngày nộp bảo hiểm', help='Ngày nộp bảo hiểm',default=fields.Datetime.now)
    PHUONG_THUC_THANH_TOAN = fields.Selection([('UY_NHIEM_CHI', 'Ủy nhiệm chi'), ('TIEN_MAT', 'Tiền mặt'), ], string='Phương thức thanh toán', help='Phương thức thanh toán',default='UY_NHIEM_CHI')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
   
    TIEN_LUONG_NOP_BAO_HIEM_FORM_THAM_SO_CHI_TIET_IDS = fields.One2many('tien.luong.nop.bao.hiem.form.tham.so.chi.tiet', 'CHI_TIET_ID', string='Nộp bảo hiểm form tham số chi tiết')
    
    @api.onchange('NGAY_NOP_BAO_HIEM')
    def _cap_nhat_lai_thong_tin_nop_bao_hiem(self):
        chi_nhanh_id = 0
        chi_nhanh_id = self.get_chi_nhanh()
        thong_tin_nop_bao_hiem_list = []
        danh_sach_thong_tin_nop_bao_hiem_sql = self.lay_du_lieu_sql_tra_ve_thong_tin_nop_bao_hiem(chi_nhanh_id,self.NGAY_NOP_BAO_HIEM)
        for thong_tin in danh_sach_thong_tin_nop_bao_hiem_sql:
            thong_tin_nop_bao_hiem_list += [(0,0,{
                'KHOAN_PHAI_NOP' : thong_tin.get('KHOAN_PHAI_NOP'),
                'SO_PHAI_NOP': thong_tin.get('SO_PHAI_NOP'),
                'SO_NOP_LAN_NAY' :thong_tin.get('SO_PHAI_NOP'),
                'SO_TAI_KHOAN_ID' :thong_tin.get('TAI_KHOAN_ID'),
            })]
        self.TIEN_LUONG_NOP_BAO_HIEM_FORM_THAM_SO_CHI_TIET_IDS = thong_tin_nop_bao_hiem_list


    def lay_du_lieu_sql_tra_ve_thong_tin_nop_bao_hiem(self,chi_nhanh_id,ngay_nop_bao_hiem):
        param_sql= {
        'chi_nhanh_id': chi_nhanh_id,
        'ngay_nop_bao_hiem': ngay_nop_bao_hiem,
        }
        query ="""
        DO LANGUAGE plpgsql $$
DECLARE

    chi_nhanh_id                                  INTEGER := %(chi_nhanh_id)s;

    ngay_hach_toan_tren_chung_tu                  TIMESTAMP := %(ngay_nop_bao_hiem)s;

    --@SystemDate

    CHE_DO_KE_TOAN                     VARCHAR(128);


    rec                                           RECORD;


BEGIN

        SELECT value
        INTO CHE_DO_KE_TOAN
        FROM ir_config_parameter
        WHERE key = 'he_thong.CHE_DO_KE_TOAN'
        FETCH FIRST 1 ROW ONLY
        ;



    DROP TABLE IF EXISTS TMP_KET_QUA;

    IF CHE_DO_KE_TOAN = '15'
THEN

    CREATE TEMP TABLE TMP_KET_QUA
        AS
    SELECT  CAST(0 AS BIT) AS Selected ,
            GL."TAI_KHOAN_ID" as "TAI_KHOAN_ID",
            GL."MA_TAI_KHOAN" AS "SO_TAI_KHOAN" ,
            A."TEN_TAI_KHOAN" AS "KHOAN_PHAI_NOP" ,
            SUM("GHI_CO" - "GHI_NO") AS "SO_PHAI_NOP" ,
            CAST(0 AS DECIMAL) AS "SO_NOP_LAN_NAY"
    FROM    so_cai_chi_tiet AS GL
            LEFT JOIN danh_muc_he_thong_tai_khoan AS A ON GL."MA_TAI_KHOAN" = A."SO_TAI_KHOAN"
    WHERE   "CHI_NHANH_ID" = chi_nhanh_id
            AND "NGAY_HACH_TOAN" <= ngay_hach_toan_tren_chung_tu

            AND (
				GL."MA_TAI_KHOAN" LIKE '3384%%'
				OR GL."MA_TAI_KHOAN" LIKE '3383%%'
				OR GL."MA_TAI_KHOAN" LIKE '3382%%'
				OR GL."MA_TAI_KHOAN" LIKE '3386%%'
            )
    GROUP BY  GL."TAI_KHOAN_ID",
            GL."MA_TAI_KHOAN" ,
            A."TEN_TAI_KHOAN"
    HAVING  ( SUM("GHI_CO" - "GHI_NO") ) > 0
    ORDER BY A."TEN_TAI_KHOAN" ;
END IF ;
---------------------------------




--Lấy dữ liệu cho thông tư 133
IF CHE_DO_KE_TOAN = '48'
THEN

     CREATE TEMP TABLE TMP_KET_QUA
        AS
    SELECT  CAST(0 AS BIT) AS Selected ,
        GL."TAI_KHOAN_ID" as "TAI_KHOAN_ID",
            GL."MA_TAI_KHOAN" AS "SO_TAI_KHOAN" ,
            A."TEN_TAI_KHOAN" AS "KHOAN_PHAI_NOP" ,
            SUM("GHI_CO" - "GHI_NO") AS "SO_PHAI_NOP",
            CAST(0 AS DECIMAL) AS "SO_NOP_LAN_NAY"
    FROM    so_cai_chi_tiet AS GL
            LEFT JOIN danh_muc_he_thong_tai_khoan AS A ON GL."MA_TAI_KHOAN" = A."SO_TAI_KHOAN"
    WHERE   "CHI_NHANH_ID" = chi_nhanh_id
            AND "NGAY_HACH_TOAN" <= ngay_hach_toan_tren_chung_tu

            AND (
				GL."MA_TAI_KHOAN" LIKE '3384%%'
				OR GL."MA_TAI_KHOAN" LIKE '3383%%'
				OR GL."MA_TAI_KHOAN" LIKE '3382%%'
				OR GL."MA_TAI_KHOAN" LIKE '3385%%'
            )
    GROUP BY GL."TAI_KHOAN_ID",
        GL."MA_TAI_KHOAN" ,
            A."TEN_TAI_KHOAN"
    HAVING  ( SUM("GHI_CO" - "GHI_NO") ) > 0
    ORDER BY A."TEN_TAI_KHOAN";
END    IF;

END $$
;

SELECT *
FROM TMP_KET_QUA

ORDER BY
  "KHOAN_PHAI_NOP"
;
        """
        return self.execute(query,param_sql)

