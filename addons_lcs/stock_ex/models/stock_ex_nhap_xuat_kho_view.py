# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import tools
from odoo import api, fields, models

class NHAP_XUAT_KHO_VIEW(models.Model):
    _name = "stock.ex.nhap.xuat.kho.view"
    _description = "Nhập xuất kho"
    _auto = False
    _order = 'NGAY_CHUNG_TU desc'

    name = fields.Char(string='Số chứng từ', help='Số chứng từ', related='SO_CHUNG_TU')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TONG_TIEN = fields.Float(string='Tổng tiền', help='Tổng tiền')
    NGUOI_GIAO_HANG_TEXT = fields.Char(string='Người giao/Người nhận', help='Người giao/Người nhận')
    NGUOI_NHAN_TEXT = fields.Char(string='Người giao/Người nhận', help='Người giao/Người nhận') 
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    TEN_NGUOI_GIAO_HANG = fields.Char(string='Tên người giao hàng', help='Tên người giao hàng')
    LOAI_CHUNG_TU_TEXT=fields.Char(string='Loại chứng từ')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng')
    DA_LAP_CT_BAN_HANG = fields.Char(string='Đã lập chứng từ bán hàng', help='Đã lập chứng từ bán hàng')
    # TEN_LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='Loại chứng từ')
    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')
    type = fields.Selection([('NHAP_KHO', 'Nhập kho'), ('XUAT_KHO', 'Xuất kho'), ('CHUYEN_KHO', 'Chuyển kho')], string='Loại chuyển kho')
    state = fields.Selection([('chua_ghi_so', 'Chưa ghi sổ'), ('da_ghi_so', 'Đã ghi sổ')], string='Trạng thái')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    LY_DO_XUAT = fields.Char(string='Lý do xuất', help='Lý do xuất')
    VE_VIEC = fields.Char(string='Về việc', help='Về việc')
    TEN_NGUOI_VAN_CHUYEN = fields.Char(string='Tên người vận chuyển', help='Tên người vận chuyển')
    NGAY_GHI_SO_CK= fields.Date(string='Ngày ghi sổ kho', help='Ngày ghi sổ kho')
    SOURCE_ID = fields.Reference(selection=[], string='Lập từ')
   
    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            SELECT
                CONCAT(R."MODEL_GOC", ',', R."ID_GOC") AS id
                , *
            FROM (
                    SELECT
                        MH.id               AS "ID_GOC"
                        , 'purchase.document' AS "MODEL_GOC"
                        , NULL :: VARCHAR(50) AS "SOURCE_ID"
                        , "NGAY_HACH_TOAN"
                        , "NGAY_CHUNG_TU"
                        , NULL :: DATE        AS "NGAY_GHI_SO_CK"
                        , "SO_CHUNG_TU"
                        , "DIEN_GIAI_CHUNG"   AS "DIEN_GIAI"
                        , "DIEN_GIAI_CHUNG"   AS "LY_DO_XUAT"
                        , "DIEN_GIAI_CHUNG"   AS "VE_VIEC"
                        , "TONG_TIEN_HANG"    AS "TONG_TIEN"
                        , "NGUOI_GIAO_HANG"   AS "NGUOI_GIAO_HANG_TEXT"
                        , "NGUOI_GIAO_HANG"   AS "NGUOI_NHAN_TEXT"
                        , "NGUOI_GIAO_HANG"   AS "TEN_NGUOI_VAN_CHUYEN"
                        , "DOI_TUONG_ID"
                        , AO."HO_VA_TEN"      AS "TEN_NGUOI_GIAO_HANG"
                        , AO."HO_VA_TEN"      AS "TEN_KHACH_HANG"
                        , ''                  AS "DA_LAP_CT_BAN_HANG"
                        , "LOAI_CHUNG_TU"     AS "LOAI_CHUNG_TU"
                        , RF."REFTYPENAME"    AS "LOAI_CHUNG_TU_TEXT"
                        , 'NHAP_KHO'          AS type
                        , state
                        , AO."CHI_NHANH_ID"
                    FROM purchase_document MH
                        LEFT JOIN danh_muc_reftype RF ON MH."LOAI_CHUNG_TU" = RF."REFTYPE"
                        LEFT JOIN res_partner AO ON MH."DOI_TUONG_ID" = AO.id
                    WHERE MH."LOAI_CHUNG_TU" IN
                        (302, 307, 308, 309, 310, 318, 319, 320, 321, 322, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2020, 2021, 2022, 2023, 2022, 2024, 2025, 2026, 2027, 3030, 3030, 3031, 3032, 3033, 3040, 3041, 3042, 3043)

                    UNION ALL

                    SELECT
                        XNK.id                   AS "ID_GOC"
                        , 'stock.ex.nhap.xuat.kho' AS "MODEL_GOC"
                        , "SOURCE_ID"              AS "SOURCE_ID"
                        , "NGAY_HACH_TOAN"
                        , "NGAY_CHUNG_TU"
                        , "NGAY_GHI_SO_CK"         AS "NGAY_GHI_SO_CK"
                        , "SO_CHUNG_TU"
                        , "DIEN_GIAI"
                        , "DIEN_GIAI"              AS "LY_DO_XUAT"
                        , "DIEN_GIAI"              AS "VE_VIEC"
                        , "TONG_TIEN"
                        , "NGUOI_GIAO_HANG_TEXT"
                        , "NGUOI_NHAN_TEXT"
                        , "TEN_NGUOI_VAN_CHUYEN"
                        , "DOI_TUONG_ID"
                        , "TEN_NGUOI_GIAO_HANG"
                        , "TEN_NGUOI_GIAO_HANG"    AS "TEN_KHACH_HANG"
                        , ''                       AS "DA_LAP_CT_BAN_HANG"
                        , "LOAI_CHUNG_TU"          AS "LOAI_CHUNG_TU"
                        , RF."REFTYPENAME"         AS "LOAI_CHUNG_TU_TEXT"
                        , type
                        , state
                        , "CHI_NHANH_ID"
                    FROM stock_ex_nhap_xuat_kho XNK
                        LEFT JOIN danh_muc_reftype RF ON XNK."LOAI_CHUNG_TU" = RF."REFTYPE"

                    UNION ALL

                    SELECT
                        TL.id                          AS "ID_GOC"
                        , 'purchase.ex.tra.lai.hang.mua' AS "MODEL_GOC"
                        , NULL :: VARCHAR(50)            AS "SOURCE_ID"
                        , "NGAY_HACH_TOAN"
                        , "NGAY_CHUNG_TU"
                        , NULL :: DATE                   AS "NGAY_GHI_SO_CK"
                        , "SO_CHUNG_TU"
                        , TL."DIEN_GIAI"
                        , TL."DIEN_GIAI"                 AS "LY_DO_XUAT"
                        , TL."DIEN_GIAI"                 AS "VE_VIEC"
                        , "TONG_TIEN_HANG"               AS "TONG_TIEN"
                        , "NGUOI_NHAN_HANG"              AS "NGUOI_GIAO_HANG_TEXT"
                        , "NGUOI_NHAN_HANG"              AS "NGUOI_NHAN_TEXT"
                        , "NGUOI_NHAN_HANG"              AS "TEN_NGUOI_VAN_CHUYEN"
                        , "DOI_TUONG_ID"
                        , AO."HO_VA_TEN"                 AS "TEN_NGUOI_GIAO_HANG"
                        , AO."HO_VA_TEN"                 AS "TEN_KHACH_HANG"
                        , ''                             AS "DA_LAP_CT_BAN_HANG"
                        , "LOAI_CHUNG_TU"                AS "LOAI_CHUNG_TU"
                        , RF."REFTYPENAME"               AS "LOAI_CHUNG_TU_TEXT"
                        , 'NHAP_KHO'                     AS type
                        , state
                        , TL."CHI_NHANH_ID"
                    FROM purchase_ex_tra_lai_hang_mua TL
                        LEFT JOIN danh_muc_reftype RF ON TL."LOAI_CHUNG_TU" = RF."REFTYPE"
                        LEFT JOIN res_partner AO ON TL."DOI_TUONG_ID" = AO.id
                    WHERE TL."LOAI_CHUNG_TU" IN
                        (302, 307, 308, 309, 310, 318, 319, 320, 321, 322, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2020, 2021, 2022, 2023, 2022, 2024, 2025, 2026, 2027, 3030, 3030, 3031, 3032, 3033, 3040, 3041, 3042, 3043)
                ) R
            )""" % (self._table,))