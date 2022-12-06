# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError

class bao_cao_bang_tinh_khau_hao_tscd(models.Model):
    _name = 'bao.cao.bang.tinh.khau.hao.tscd'
    _description = ''
    _inherit = ['mail.thread']
    _auto = False

    RowNumber = fields.Integer(string='RowNumber')
    NGAY_HACH_TOAN = fields.Date(string='NGAY_HACH_TOAN', help='PostedDate')
    ID_CHUNG_TU = fields.Integer(string='ID_CHUNG_TU')
    ID_CHUNG_TU_GHI_TANG = fields.Integer(string='ID_CHUNG_TU_GHI_TANG')
    MODEL_CHUNG_TU = fields.Char(string='MODEL_CHUNG_TU')
    STT = fields.Integer(string='STT', help='SortOrderMaster')
    bang_tinh_khau_hao_tscd_chi_tiet_IDS = fields.One2many('bao.cao.bang.tinh.khau.hao.tscd.chi.tiet', 'NHAP_XUAT_ID')

    TONG_GIA_TRI_TINH_KHAU_HAO = fields.Monetary(string='GIA_TRI_CON_LAI', help='RemainAmount',currency_field='base_currency_id')
    TONG_GIA_TRI_KH_THANG = fields.Monetary(string='GIA_TRI_CON_LAI', help='RemainAmount',currency_field='base_currency_id')
    TONG_HAO_MON_LUY_KE = fields.Monetary(string='GIA_TRI_CON_LAI', help='RemainAmount',currency_field='base_currency_id')
    TONG_GIA_TRI_CON_LAI = fields.Monetary(string='GIA_TRI_CON_LAI', help='RemainAmount',currency_field='base_currency_id')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh())

class bao_cao_bang_tinh_khau_hao_tscd_report(models.AbstractModel):
    _name = 'report.bao_cao.template_fadepreciation'

    @api.model
    def get_report_values(self, docids, data=None):

        refTypeList, records = self.get_reftype_list(data)
        ############### START SQL lấy dữ liệu ###############

        sql_result = self.ham_lay_du_lieu_sql_tra_ve(refTypeList)

        for line in sql_result:
            key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
            master_data = self.env['bao.cao.bang.tinh.khau.hao.tscd'].convert_for_update(line)
            detail_data = self.env['bao.cao.bang.tinh.khau.hao.tscd.chi.tiet'].convert_for_update(line)
            if records.get(key):
                records[key].update(master_data)
                records[key].bang_tinh_khau_hao_tscd_chi_tiet_IDS += self.env['bao.cao.bang.tinh.khau.hao.tscd.chi.tiet'].new(detail_data)
        
        docs = [records.get(k) for k in records]

        for record in docs:
            sum_GIA_TRI_TINH_KHAU_HAO = 0
            sum_GIA_TRI_KH_THANG = 0
            sum_HAO_MON_LUY_KE = 0
            sum_GIA_TRI_CON_LAI = 0

            for line in record.bang_tinh_khau_hao_tscd_chi_tiet_IDS:
                sum_GIA_TRI_TINH_KHAU_HAO += line.GIA_TRI_TINH_KHAU_HAO
                sum_GIA_TRI_KH_THANG += line.GIA_TRI_KH_THANG
                sum_HAO_MON_LUY_KE += line.HAO_MON_LUY_KE
                sum_GIA_TRI_CON_LAI += line.GIA_TRI_CON_LAI
            
            record.TONG_GIA_TRI_TINH_KHAU_HAO = sum_GIA_TRI_TINH_KHAU_HAO
            record.TONG_GIA_TRI_KH_THANG = sum_GIA_TRI_KH_THANG
            record.TONG_HAO_MON_LUY_KE = sum_HAO_MON_LUY_KE
            record.TONG_GIA_TRI_CON_LAI = sum_GIA_TRI_CON_LAI


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


    DROP TABLE IF EXISTS TMP_TINH_KHAU_HAO_TSCD
    ;

    CREATE TEMP TABLE TMP_TINH_KHAU_HAO_TSCD
        AS


            SELECT
                  ROW_NUMBER()
                  OVER (
                      ORDER BY
                          "STT",
                          "sequence" )                                         AS "RowNumber"
                , FD."NGAY_HACH_TOAN"
                , RID."ID_CHUNG_TU"

                , FDD."MA_TAI_SAN_ID" AS "ID_CHUNG_TU_GHI_TANG"
                ,'asset.ghi.tang' AS "MODEL_CHUNG_TU"
                , FA."MA_TAI_SAN"
                , FA."TEN_TAI_SAN"
                , OU."TEN_DON_VI"
                , FL."GIA_TRI_TINH_KHAU_HAO"          AS "GIA_TRI_TINH_KHAU_HAO"
                , FDD."GIA_TRI_KH_THANG" -- Gias tri khau hao thang
                , FL."GIA_TRI_HAO_MON_LUY_KE" + FDD."GIA_TRI_KH_THANG"                 AS "HAO_MON_LUY_KE"    -- Hao mòn lũy kế
                , FL."GIA_TRI_TINH_KHAU_HAO" - FL."GIA_TRI_HAO_MON_LUY_KE" - FDD."GIA_TRI_KH_THANG" AS "GIA_TRI_CON_LAI" -- Còn lại
                , RID."STT"
                , FDD."sequence"         AS "SortOrder"
            FROM TMP_ID_CHUNG_TU AS RID
                INNER JOIN asset_tinh_khau_hao FD ON RID."ID_CHUNG_TU" = FD."id"
                INNER JOIN asset_tinh_khau_hao_chi_tiet FDD ON FD."id" = FDD."TINH_KHAU_HAO_ID"
                INNER JOIN asset_ghi_tang FA ON FDD."MA_TAI_SAN_ID" = FA."id"
                LEFT JOIN danh_muc_to_chuc OU ON OU."id" = FDD."DON_VI_SU_DUNG_ID"
                INNER JOIN LATERAL (SELECT
                                        FL."GIA_TRI_TINH_KHAU_HAO"
                                        , FL."GIA_TRI_HAO_MON_LUY_KE" +
                                          FL."TONG_CHENH_LECH_GIA_TRI_HAO_MON_LUY_KE" AS "GIA_TRI_HAO_MON_LUY_KE"
                                    FROM so_tscd_chi_tiet FL
                                    WHERE FL."TSCD_ID" = FDD."MA_TAI_SAN_ID"
                                          AND FL.
                                              "NGAY_HACH_TOAN"
                                              <= FD.
                                              "NGAY_HACH_TOAN"

                                          AND FL."ID_CHUNG_TU" <> FDD."TINH_KHAU_HAO_ID" -- Không lấy lên dòng hiện tại

                                          AND FL."LOAI_CHUNG_TU" <> 251
                                    ORDER BY "NGAY_HACH_TOAN" DESC, "THU_TU_CHUNG_TU_NHAP_TRUOC_NHAP_SAU" DESC
                                    FETCH FIRST 1 ROW ONLY

                           ) AS FL  ON TRUE
            ORDER BY
                "STT",
                "sequence"
    ;


END $$

;

SELECT *
FROM TMP_TINH_KHAU_HAO_TSCD

ORDER BY
    "RowNumber"
;
        """
        return self.execute(query)
