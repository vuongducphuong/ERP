# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision


class SUPPLY_CCDC_GHI_GIAM_CHI_TIET(models.Model):
    _name = 'supply.ghi.giam.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MA_CCDC_ID = fields.Many2one('supply.ghi.tang', string='Mã CCDC', help='Mã công cụ dụng cụ')
    TEN_CCDC = fields.Char(string='Tên CCDC', help='Tên công cụ dụng cụ',related='MA_CCDC_ID.TEN_CCDC')
    DON_VI_SU_DUNG_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị sử dụng', help='Đơn vị sử dụng')
    SO_LUONG_DANG_DUNG = fields.Float(string='Số lượng đang dùng', help='Số lượng đang dùng', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_GHI_GIAM = fields.Float(string='Số lượng ghi giảm', help='Số lượng ghi giảm', digits=decimal_precision.get_precision('SO_LUONG'))
    GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM = fields.Float(string='Giá trị còn lại của CCDC ghi giảm', help='Giá trị còn lại của công cụ dụng cụ ghi giảm' ,digits=decimal_precision.get_precision('VND'))
    CCDC_GHI_GIAM_ID = fields.Many2one('supply.ghi.giam', string='Công cụ dụng cụ ghi giảm', help='Công cụ dụng cụ ghi giảm', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ', related='CCDC_GHI_GIAM_ID.NGAY_CHUNG_TU')
    PHAN_BO_CHI_PHI_ID = fields.Many2one('supply.phan.bo.chi.phi', string='Phân bổ chi phí', help='SUAllocationID')
    sequence = fields.Integer()
    @api.onchange('MA_CCDC_ID')
    def _onchange_MA_CCDC_ID(self):
        self.thay_doi_thong_tin('ccdc')
    @api.onchange('SO_LUONG_GHI_GIAM')
    def _onchange_SO_LUONG_GHI_GIAM(self):
        self.thay_doi_thong_tin('so_luong')

    @api.onchange('DON_VI_SU_DUNG_ID')
    def _onchange_DON_VI_SU_DUNG_ID(self):
        self.thay_doi_thong_tin('don_vi')

    def thay_doi_thong_tin(self,truong_onchange):
        if self.MA_CCDC_ID:
            record = self.lay_du_lieu_ccdc(self.NGAY_CHUNG_TU,self.MA_CCDC_ID.id)
            if len(record) >0:
                dict_don_vi = {}
                ten_ccdc = record[0].get('TEN_CCDC')
                so_luong = record[0].get('SO_LUONG')
                don_vi_id = record[0].get('DON_VI_ID')
                gia_tri_con_lai = record[0].get('SO_TIEN')
                if truong_onchange == 'so_luong':
                    if self.SO_LUONG_DANG_DUNG>0:
                        self.GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM = (gia_tri_con_lai/self.SO_LUONG_DANG_DUNG)*self.SO_LUONG_GHI_GIAM
                else:
                    if self.DON_VI_SU_DUNG_ID:
                        for line in record:
                            dict_don_vi[line.get('DON_VI_ID')] = line.get('TEN_DON_VI')
                            if line.get('DON_VI_ID') == self.DON_VI_SU_DUNG_ID.id:
                                ten_ccdc = line.get('TEN_CCDC')
                                so_luong = line.get('SO_LUONG')
                                don_vi_id = line.get('DON_VI_ID')
                                gia_tri_con_lai = line.get('SO_TIEN')
                                return
                    if truong_onchange == 'ccdc':
                        self.TEN_CCDC = ten_ccdc
                        self.DON_VI_SU_DUNG_ID = don_vi_id
                        self.SO_LUONG_GHI_GIAM = so_luong
                        self.SO_LUONG_DANG_DUNG = so_luong
                        self.GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM = gia_tri_con_lai
                    elif truong_onchange == 'don_vi':
                        if self.DON_VI_SU_DUNG_ID.id not in dict_don_vi:
                            thong_bao = 'Công cụ dụng cụ <'  + str(self.MA_CCDC_ID.TEN_CCDC) + '> chỉ được phân bổ cho đơn vị <' + ",".join(dict_don_vi.values()) + '> Bạn vui lòng chọn đơn vị khác hoặc kiểm tra lại ghi tăng'
                            raise ValidationError(thong_bao)
                        self.TEN_CCDC = ten_ccdc
                        self.SO_LUONG_GHI_GIAM = so_luong
                        self.SO_LUONG_DANG_DUNG = so_luong
                        self.GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM = gia_tri_con_lai

    @api.model
    def create(self, values):
        if values.get('SO_LUONG_GHI_GIAM') > values.get('SO_LUONG_DANG_DUNG'):
            raise ValidationError("Số lượng ghi giảm phải nhỏ hơn hoặc bằng số lượng đang dùng. Vui lòng kiểm tra lại.")
        result = super(SUPPLY_CCDC_GHI_GIAM_CHI_TIET, self).create(values)
        return result



    def lay_du_lieu_ccdc(self,ngay,ccdc_id):
        params = {
            'NGAY':ngay, 
            'CCDC_ID' : ccdc_id,
            'CHI_NHANH_ID' : self.get_chi_nhanh(),
            }

        query = """   

            DO LANGUAGE plpgsql $$
            DECLARE
                v_ngay_chung_tu TIMESTAMP := %(NGAY)s;


                v_chi_nhanh_id  INT := %(CHI_NHANH_ID)s;

                ccdc_id         INT := %(CCDC_ID)s;

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
                "SO_DA_PHAN_BO"          DECIMAL(18, 4),
                "SO_TIEN_GHI_TANG"       DECIMAL(18, 4),
                "SO_TIEN_GHI_GIAM"       DECIMAL(18, 4)

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
            "SO_DA_PHAN_BO",
            "SO_TIEN_GHI_TANG",
            "SO_TIEN_GHI_GIAM"


            )
                SELECT
                    SL."CCDC_ID"
                    , SL."MA_CCDC"
                    , SL."TEN_CCDC"
                    , SUM(SL."SO_KY_PHAN_BO_GHI_TANG") AS "SO_KY_PHAN_BO_GHI_TANG"
                    , SUM(SL."SO_KY_PHAN_BO_GHI_GIAM") AS "SO_KY_PHAN_BO_GHI_GIAM"
                    , SUM(SL."SO_LUONG_GHI_TANG")      AS "SO_LUONG_GHI_TANG"
                    , SUM(SL."SO_LUONG_GHI_GIAM")      AS "SL_GIAM_TRONG_KY"
                    , SUM(SL."SO_TIEN_PHAN_BO")        AS "SO_DA_PHAN_BO"
                    , SUM(SL."SO_TIEN_GHI_TANG")       AS "SO_TIEN_GHI_TANG"
                    , SUM(SL."SO_TIEN_GHI_GIAM")       AS "SO_TIEN_GHI_GIAM"
                FROM so_ccdc_chi_tiet AS SL
                WHERE SL."NGAY_HACH_TOAN" <= v_ngay_chung_tu
                    AND SL."CHI_NHANH_ID" = v_chi_nhanh_id
                    AND "CCDC_ID" = ccdc_id

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
                    , SI."SO_KY_PHAN_BO"                                                AS "SO_KY_PHAN_BO"
                    , (T."SO_LUONG_GHI_TANG" - T."SL_GIAM_TRONG_KY")                    AS "SO_LUONG"
                    , (T."SO_TIEN_GHI_TANG" - T."SO_TIEN_GHI_GIAM" - T."SO_DA_PHAN_BO") AS "SO_TIEN"
                    , SI."TK_CHO_PHAN_BO_ID"
                FROM TMP_KET_QUA AS T
                    INNER JOIN supply_ghi_tang AS SI ON T."CCDC_ID" = SI."id"
            ;


        END $$

        ;

        SELECT

            R."CCDC_ID"
            , R."MA_CCDC"
            , R."TEN_CCDC"
            , R."SO_KY_PHAN_BO"
            , R."SO_LUONG"
            , R."SO_TIEN"
            , dv."MA_DON_VI_ID"                         AS "DON_VI_ID"
            , dv."TEN_DON_VI"
            , (SELECT "SO_TAI_KHOAN"
            FROM danh_muc_he_thong_tai_khoan TK
            WHERE TK.id = R."TAI_KHOAN_CHO_PHAN_BO") AS "TK_CHO_PB"
        FROM TMP_KET_QUA_CUOI_CUNG AS R
            LEFT JOIN supply_ghi_tang_don_vi_su_dung dv ON R."CCDC_ID" = dv."GHI_TANG_DON_VI_SU_DUNG_ID"
        WHERE R."SO_LUONG" > 0
        ORDER BY R."MA_CCDC"
        ;

        """  
        
        
        return self.execute(query, params)
