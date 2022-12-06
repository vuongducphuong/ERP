# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class SUPPLY_CHI_TIET_DIEU_CHINH_CCDC(models.Model):
    _name = 'supply.dieu.chinh.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MA_CCDC = fields.Many2one('supply.ghi.tang',string='Mã CCDC', help='Mã công cụ dụng cụ')
    TEN_CCDC = fields.Char(string='Tên CCDC', help='Tên công cụ dụng cụ',related='MA_CCDC.TEN_CCDC')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    TAI_KHOAN_CHO_PHAN_BO = fields.Many2one('danh.muc.he.thong.tai.khoan',string='TK chờ phân bổ', help='Tài khoản chờ phân bổ')
    GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH = fields.Float(string='Giá trị còn lại trước điều chỉnh', help='Giá trị còn lại trước điều chỉnh',digits= decimal_precision.get_precision('VND'))
    GIA_TRI_CON_LAI_SAU_DIEU_CHINH = fields.Float(string='Giá trị còn lại sau điều chỉnh', help='Giá trị còn lại sau điều chỉnh',digits= decimal_precision.get_precision('VND'))
    CHENH_LECH_GIA_TRI = fields.Float(string='Chênh lệch', help='Chênh lệch giá trị',digits= decimal_precision.get_precision('VND'))
    SO_KY_PHAN_BO_CON_LAI_TRUOC_DIEU_CHINH = fields.Float(string='Số kỳ phân bố còn lại trước điều chỉnh', help='Số kỳ phân bố còn lại trước điều chỉnh',digits=decimal_precision.get_precision('VND'))
    SO_KY_CON_LAI_SAU_DIEU_CHINH = fields.Float(string='Số kỳ còn lại sau điều chỉnh', help='Số kỳ còn lại sau điều chỉnh',digits=decimal_precision.get_precision('VND'))
    CHENH_LENH_KY = fields.Float(string='Chênh lệnh', help='Chênh lệnh kỳ')
    GHI_CHU = fields.Char(string='Ghi chú', help='Ghi chú')
    SO_TIEN_PHAN_BO_HANG_KY = fields.Float(string='Số tiền PB hàng kỳ', help='Số tiền phân bổ hàng kỳ',digits= decimal_precision.get_precision('VND'))
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CHI_TIET_DIEU_CHINH_CCDC_ID_ID = fields.Many2one('supply.dieu.chinh', string='Chi tiết điều chỉnh ccdc id', help='Chi tiết điều chỉnh ccdc id', ondelete='cascade')
    NGAY_CHUNG_TU_MASTER = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ',related='CHI_TIET_DIEU_CHINH_CCDC_ID_ID.NGAY_CHUNG_TU')
    sequence = fields.Integer()

    @api.onchange('MA_CCDC')
    def laythongtinccdc(self):
        if self.MA_CCDC:
            # dieu_chinh_trc = self.env['supply.dieu.chinh.chi.tiet'].search([('MA_CCDC', '=', self.MA_CCDC.id)], order="NGAY_CHUNG_TU_MASTER asc", limit = 1)
            du_lieu_ccdc = self.lay_du_lieu_ccdc_khi_chi_tiet(self.NGAY_CHUNG_TU_MASTER,self.MA_CCDC.id)
            ccdc = self.env['supply.ghi.tang'].search([('id', '=', self.MA_CCDC.id)], limit = 1)

            if du_lieu_ccdc:
                tai_khoan_cho_phan_bo = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', du_lieu_ccdc[0].get('TK_CHO_PHAN_BO_ID'))],limit=1).id
                self.TEN_CCDC = du_lieu_ccdc[0].get('TEN_CCDC')
                self.SO_LUONG = du_lieu_ccdc[0].get('SO_LUONG')
                self.TAI_KHOAN_CHO_PHAN_BO = tai_khoan_cho_phan_bo
                self.GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH = du_lieu_ccdc[0].get('SO_TIEN')
                self.SO_KY_PHAN_BO_CON_LAI_TRUOC_DIEU_CHINH = du_lieu_ccdc[0].get('SO_KY_PHAN_BO')
            else:
                self.TEN_CCDC = ccdc.name
                self.SO_LUONG = ccdc.SO_LUONG
                self.TAI_KHOAN_CHO_PHAN_BO = ccdc.TK_CHO_PHAN_BO_ID.SO_TAI_KHOAN
                self.GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH = ccdc.GIA_TRI_PHAN_BO_CON_LAI
                self.SO_KY_PHAN_BO_CON_LAI_TRUOC_DIEU_CHINH = ccdc.SO_KY_PB_CON_LAI

            self.GIA_TRI_CON_LAI_SAU_DIEU_CHINH = self.GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH
            self.SO_KY_CON_LAI_SAU_DIEU_CHINH = self.SO_KY_PHAN_BO_CON_LAI_TRUOC_DIEU_CHINH
            self.CHENH_LECH_GIA_TRI = self.GIA_TRI_CON_LAI_SAU_DIEU_CHINH - self.GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH
            self.CHENH_LENH_KY = self.SO_KY_CON_LAI_SAU_DIEU_CHINH - self.SO_KY_PHAN_BO_CON_LAI_TRUOC_DIEU_CHINH
            if self.SO_KY_CON_LAI_SAU_DIEU_CHINH != 0:
                self.SO_TIEN_PHAN_BO_HANG_KY = self.GIA_TRI_CON_LAI_SAU_DIEU_CHINH/self.SO_KY_CON_LAI_SAU_DIEU_CHINH
            else:
                self.SO_TIEN_PHAN_BO_HANG_KY = 0

    @api.onchange('GIA_TRI_CON_LAI_SAU_DIEU_CHINH')
    def update_chenhlechgiatriconlai(self):
        if self.MA_CCDC:
            self.CHENH_LECH_GIA_TRI = self.GIA_TRI_CON_LAI_SAU_DIEU_CHINH - self.GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH
            if self.SO_KY_CON_LAI_SAU_DIEU_CHINH != 0:
                self.SO_TIEN_PHAN_BO_HANG_KY = self.GIA_TRI_CON_LAI_SAU_DIEU_CHINH/self.SO_KY_CON_LAI_SAU_DIEU_CHINH
            else:
                self.SO_TIEN_PHAN_BO_HANG_KY = 0

    @api.onchange('SO_KY_CON_LAI_SAU_DIEU_CHINH')
    def update_chenhlechsokyphanbo(self):
        if self.MA_CCDC:
            self.CHENH_LENH_KY = self.SO_KY_CON_LAI_SAU_DIEU_CHINH - self.SO_KY_PHAN_BO_CON_LAI_TRUOC_DIEU_CHINH
            if self.SO_KY_CON_LAI_SAU_DIEU_CHINH != 0:
                self.SO_TIEN_PHAN_BO_HANG_KY = self.GIA_TRI_CON_LAI_SAU_DIEU_CHINH/self.SO_KY_CON_LAI_SAU_DIEU_CHINH
            else:
                self.SO_TIEN_PHAN_BO_HANG_KY = 0


    def lay_du_lieu_ccdc_khi_chi_tiet(self,ngay,ccdc_id):
        params = {
            'NGAY_CHUNG_TU' : ngay,
            'CCDC_ID' : ccdc_id,
            'CHI_NHANH_ID' : self.get_chi_nhanh(),
            }
        query = """ 
            DO LANGUAGE plpgsql $$
            DECLARE
                v_ngay_chung_tu TIMESTAMP := %(NGAY_CHUNG_TU)s;

                v_chi_nhanh_id  INT := %(CHI_NHANH_ID)s;

                ccdc_id         INT :=%(CCDC_ID)s;

                rec             RECORD;

            BEGIN

                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA

                (
                    "CCDC_ID"                INT,
                    "MA_CCDC"                VARCHAR(25),
                    "TEN_CCDC"               VARCHAR(255),
                    "SO_KY_PHAN_BO_GHI_TANG" INT,
                    "SO_KY_PHAN_BO_GHI_GIAM" INT,
                    "SO_LUONG_GHI_TANG"      DECIMAL(22, 8),
                    "SL_GIAM_TRONG_KY"       DECIMAL(22, 8),
                    "SO_TIEN_GHI_TANG"       DECIMAL(18, 4),
                    "SO_TIEN_GHI_GIAM"       DECIMAL(18, 4),
                    "SO_DA_PHAN_BO"          DECIMAL(18, 4)

                )
                ;

                INSERT INTO TMP_KET_QUA
                ("CCDC_ID",
                "MA_CCDC",
                "TEN_CCDC",
                "SO_KY_PHAN_BO_GHI_TANG",
                "SO_KY_PHAN_BO_GHI_GIAM",
                "SO_LUONG_GHI_TANG",
                "SL_GIAM_TRONG_KY",
                "SO_TIEN_GHI_TANG",
                "SO_TIEN_GHI_GIAM",
                "SO_DA_PHAN_BO"


                )
                    SELECT
                        SL."CCDC_ID"
                        , SL."MA_CCDC"
                        , SL."TEN_CCDC"
                        , SUM(SL."SO_KY_PHAN_BO_GHI_TANG")
                        , SUM(SL."SO_KY_PHAN_BO_GHI_GIAM")
                        , SUM(SL."SO_LUONG_GHI_TANG")
                        , SUM(SL."SO_LUONG_GHI_GIAM")
                        , SUM(SL."SO_TIEN_GHI_TANG")
                        , SUM(SL."SO_TIEN_GHI_GIAM")
                        , SUM(SL."SO_TIEN_PHAN_BO")
                    FROM so_ccdc_chi_tiet AS SL
                    WHERE SL."NGAY_HACH_TOAN" <= v_ngay_chung_tu
                        AND SL."CHI_NHANH_ID" = v_chi_nhanh_id

                    GROUP BY SL."CCDC_ID",
                        SL."MA_CCDC",
                        SL."TEN_CCDC"
                ;


                DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG
                ;

                CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
                (
                    "CCDC_ID"               INT,
                    "MA_CCDC"               VARCHAR(25),
                    "TEN_CCDC"              VARCHAR(255),
                    "SO_KY_PHAN_BO"         INT,
                    "SO_LUONG"              DECIMAL(22, 8),
                    "SO_TIEN"               DECIMAL(18, 4),
                    "TAI_KHOAN_CHO_PHAN_BO" INT
                )
                ;

                INSERT INTO TMP_KET_QUA_CUOI_CUNG
                ("CCDC_ID",
                "MA_CCDC",
                "TEN_CCDC",
                "SO_KY_PHAN_BO",
                "SO_LUONG",
                "SO_TIEN",
                "TAI_KHOAN_CHO_PHAN_BO"

                )
                    SELECT
                        T."CCDC_ID"
                        , T."MA_CCDC"
                        , T."TEN_CCDC"
                        , CAST((T."SO_KY_PHAN_BO_GHI_TANG"
                                - T."SO_KY_PHAN_BO_GHI_GIAM") AS INT)                                               AS "SO_KY_PHAN_BO"
                        , CAST((T."SO_LUONG_GHI_TANG" - T."SL_GIAM_TRONG_KY") AS DECIMAL(22, 8))                    AS "SO_LUONG"
                        , CAST((T."SO_TIEN_GHI_TANG" - T."SO_TIEN_GHI_GIAM" - T."SO_DA_PHAN_BO") AS DECIMAL(22, 8)) AS "SO_TIEN"
                        , SI."TK_CHO_PHAN_BO_ID"
                    FROM TMP_KET_QUA AS T
                        INNER JOIN supply_ghi_tang AS SI ON T."CCDC_ID" = SI."id"
                    WHERE SI."SO_KY_PHAN_BO" > 1 AND "CCDC_ID" = ccdc_id
                ;


            END $$

            ;

            SELECT

                "CCDC_ID"
                , "MA_CCDC"
                , "TEN_CCDC"
                , "SO_KY_PHAN_BO"
                , "SO_LUONG"
                , "SO_TIEN"
                , (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = R."TAI_KHOAN_CHO_PHAN_BO") AS "TK_CHO_PB"
            FROM TMP_KET_QUA_CUOI_CUNG AS R
            WHERE R."SO_LUONG" > 0
            ORDER BY R."MA_CCDC"
            ;
        """  
        return self.execute(query, params)
    

