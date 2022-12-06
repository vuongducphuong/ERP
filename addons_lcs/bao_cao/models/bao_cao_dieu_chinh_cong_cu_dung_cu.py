# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision


class bao_cao_dieu_chinh_cong_cu_dung_cu(models.Model):
    _name = 'bao.cao.dieu.chinh.cong.cu.dung.cu'
    _description = ''
    _inherit = ['mail.thread']
    _auto = False

    RowNumber = fields.Integer(string='RowNumber')
    ID_CHUNG_TU = fields.Integer(string='ID_CHUNG_TU')
    MODEL_CHUNG_TU = fields.Char(string='MODEL_CHUNG_TU')
    SO_CHUNG_TU = fields.Char(string='SO_CHUNG_TU', help='RefNo')
    NGAY_CHUNG_TU = fields.Date(string='NGAY_CHUNG_TU', help='RefDate')
    LY_DO_DIEU_CHINH = fields.Char(string='LY_DO_DIEU_CHINH', help='JournalMemo')
    STT = fields.Integer(string='STT', help='SortOrderMaster')

    TONG_GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH = fields.Float(string='GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH', digits= decimal_precision.get_precision('VND'))
    TONG_GIA_TRI_CON_LAI_SAU_DIEU_CHINH = fields.Float(string='GIA_TRI_CON_LAI_SAU_DIEU_CHINH', digits= decimal_precision.get_precision('VND'))
    TONG_CHENH_LECH_GIA_TRI_CON_LAI = fields.Float(string='CHENH_LECH_GIA_TRI_CON_LAI',digits= decimal_precision.get_precision('VND'))
    
    TONG_SO_LUONG = fields.Float(string='SO_LUONG', help='CurrentRemainingAmount',digits= decimal_precision.get_precision('SO_LUONG'))
    
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh())
    bao_cao_dieu_chinh_cong_cu_dung_cu_chi_tiet_IDS = fields.One2many('bao.cao.dieu.chinh.cong.cu.dung.cu.chi.tiet', 'NHAP_XUAT_ID')

class bao_cao_dieu_chinh_cong_cu_dung_cu_report(models.AbstractModel):
    _name = 'report.bao_cao.template_vsuadjustment'

    @api.model
    def get_report_values(self, docids, data=None):

        refTypeList, records = self.get_reftype_list(data)
        ############### START SQL lấy dữ liệu ###############

        sql_result = self.ham_lay_du_lieu_sql_tra_ve(refTypeList)

        for line in sql_result:
            key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
            master_data = self.env['bao.cao.dieu.chinh.cong.cu.dung.cu'].convert_for_update(line)
            detail_data = self.env['bao.cao.dieu.chinh.cong.cu.dung.cu.chi.tiet'].convert_for_update(line)
            if records.get(key):
                records[key].update(master_data)
                records[key].bao_cao_dieu_chinh_cong_cu_dung_cu_chi_tiet_IDS += self.env['bao.cao.dieu.chinh.cong.cu.dung.cu.chi.tiet'].new(detail_data)
        
        docs = [records.get(k) for k in records]

        for record in docs:
            sum_GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH = 0
            sum_GIA_TRI_CON_LAI_SAU_DIEU_CHINH = 0
            sum_CHENH_LECH_GIA_TRI_CON_LAI = 0
            sum_SO_LUONG = 0

            for line in record.bao_cao_dieu_chinh_cong_cu_dung_cu_chi_tiet_IDS:
                sum_GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH += line.GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH
                sum_GIA_TRI_CON_LAI_SAU_DIEU_CHINH += line.GIA_TRI_CON_LAI_SAU_DIEU_CHINH
                sum_CHENH_LECH_GIA_TRI_CON_LAI += line.CHENH_LECH_GIA_TRI_CON_LAI
                sum_SO_LUONG += line.SO_LUONG
            
            record.TONG_GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH = sum_GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH
            record.TONG_GIA_TRI_CON_LAI_SAU_DIEU_CHINH = sum_GIA_TRI_CON_LAI_SAU_DIEU_CHINH
            record.TONG_CHENH_LECH_GIA_TRI_CON_LAI = sum_CHENH_LECH_GIA_TRI_CON_LAI
            record.TONG_SO_LUONG = sum_SO_LUONG

        return {
            'docs': docs,
        }
    
    def ham_lay_du_lieu_sql_tra_ve(self,refTypeList):
        query = """
        DO LANGUAGE plpgsql $$
DECLARE

    ListIDchungtu VARCHAR := N'""" + refTypeList + """';

    rec           RECORD;

BEGIN
    DROP TABLE IF EXISTS TMP_ID_CHUNG_TU
    ;

    DROP SEQUENCE IF EXISTS TMP_ID_CHUNG_TU_seq
    ;

    CREATE TEMP SEQUENCE TMP_ID_CHUNG_TU_seq
    ;

    CREATE TEMP TABLE TMP_ID_CHUNG_TU
    (
        "ID_CHUNG_TU"   INT,
        "LOAI_CHUNG_TU" INT,


        "STT"           INT DEFAULT NEXTVAL('TMP_ID_CHUNG_TU_seq')
            PRIMARY KEY

    )
    ;

    INSERT INTO TMP_ID_CHUNG_TU
        SELECT

            Value1
            , Value2


        FROM CHUYEN_CHUOI_DINH_DANH_GUID_INT_THANH_BANG(ListIDchungtu, ',', ';') F

    ;


    DROP TABLE IF EXISTS TMP_DIEU_CHINH_CCDC
    ;

    CREATE TEMP TABLE TMP_DIEU_CHINH_CCDC
        AS


            SELECT
                  ROW_NUMBER()
                  OVER (
                      ORDER BY
                RID."STT",
                SUAD."sequence",
                  SUAD."id" )                   AS "RowNumber"
                , SUA."id"                                    AS "ID_CHUNG_TU"
                , 'supply.dieu.chinh'                         AS "MODEL_CHUNG_TU"
                , SUA."SO_CHUNG_TU"
                , SUA."NGAY_CHUNG_TU"
                , SUA."LY_DO_DIEU_CHINH"
                , SUAD."MA_CCDC"                              AS "MA_CCDC_ID"
                , SUAD."SO_LUONG"
                , (SELECT "SO_TAI_KHOAN"
                   FROM danh_muc_he_thong_tai_khoan T
                   WHERE T.id = SUAD."TAI_KHOAN_CHO_PHAN_BO") AS "TK_CHO_PB"
                , SUAD."GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH"
                , SUAD."GIA_TRI_CON_LAI_SAU_DIEU_CHINH"
                , SUAD."SO_KY_PHAN_BO_CON_LAI_TRUOC_DIEU_CHINH"
                , SUAD."SO_KY_CON_LAI_SAU_DIEU_CHINH"
                , SUAD."SO_TIEN_PHAN_BO_HANG_KY"
                , SUAD."GHI_CHU"
                , SUAD."CHENH_LECH_GIA_TRI"                   AS "CHENH_LECH_GIA_TRI_CON_LAI"
                , SUAD."CHENH_LENH_KY"
                , SUAD."sequence"                             AS "SortOrderDetail"
                , RID."STT"
                , SI."MA_CCDC"
                , SI."TEN_CCDC"
            FROM supply_dieu_chinh SUA
                LEFT JOIN supply_dieu_chinh_chi_tiet AS SUAD ON SUA."id" = SUAD."CHI_TIET_DIEU_CHINH_CCDC_ID_ID"
                INNER JOIN supply_ghi_tang AS SI ON SUAD."MA_CCDC" = SI."id"
                INNER JOIN TMP_ID_CHUNG_TU AS RID ON RID."ID_CHUNG_TU" = SUAD."CHI_TIET_DIEU_CHINH_CCDC_ID_ID"

            ORDER BY
                RID."STT",
                SUAD."sequence",
                  SUAD."id"
    ;


END $$

;

SELECT *
FROM TMP_DIEU_CHINH_CCDC

ORDER BY
    "RowNumber"
;
        """
        return self.execute(query)