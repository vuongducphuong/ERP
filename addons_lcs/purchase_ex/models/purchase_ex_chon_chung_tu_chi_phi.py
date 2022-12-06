# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper

class PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI(models.Model):
    _name = 'purchase.ex.chon.chung.tu.chi.phi'
    _auto = False
    _description = ''

    DOI_TUONG_ID = fields.Many2one('res.partner', string='Nhà cung cấp', help='Nhà cung cấp')
    TEN_NCC = fields.Char(string='Tên NCC', help='Tên nhà cung cấp')
    KHOANG_THOI_GIAN = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Khoảng thời gian', help='Khoảng thời gian', default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày')
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày')
    name = fields.Char(string='Name', help='Name')

    PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET_IDS = fields.One2many('purchase.ex.chon.chung.tu.chi.phi.chi.tiet', 'CHON_CHUNG_TU_CHI_PHI_ID', string='Chọn chứng từ chi phí chi tiết')

    @api.onchange('KHOANG_THOI_GIAN')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KHOANG_THOI_GIAN, 'TU_NGAY', 'DEN_NGAY') 

    @api.onchange('DOI_TUONG_ID')
    def _onchange_DOI_TUONG_ID(self):
        if self.DOI_TUONG_ID:
            self.TEN_NCC = self.DOI_TUONG_ID.HO_VA_TEN
    
    # @api.onchange('DOI_TUONG_ID','TU_NGAY','DEN_NGAY')
    # def _update_chi_phi(self):
    #     self.PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET_IDS = []
    #     chung_tu_ids = self.env['purchase.document'].search([('LA_CHI_PHI_MUA_HANG', '=', True), ('DOI_TUONG_ID', '=', self.DOI_TUONG_ID.id), ('NGAY_HACH_TOAN', '>=', self.TU_NGAY), ('NGAY_HACH_TOAN', '<=', self.DEN_NGAY)])
    #     for line in chung_tu_ids:
    #         new_line = line.convert_to_dict()
    #         new_line.update({
    #             'TONG_CHI_PHI': line.TONG_TIEN_HANG,
    #             'SO_PHAN_BO_LAN_NAY': line.TONG_TIEN_HANG,
    #         })
    #         self.PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET_IDS += self.env['purchase.ex.chon.chung.tu.chi.phi.chi.tiet'].new(new_line)


    def lay_du_lieu_chung_tu(self, args):
        new_line = [[5]]
        id_chung_tu = -1
        if type(args.get('id_chung_tu')) == type(1):
            id_chung_tu = args.get('id_chung_tu')
        du_lieu = self.sql_lay_du_lieu_chung_tu(args.get('doi_tuong_id'),args.get('tu_ngay'),args.get('den_ngay'),id_chung_tu)
        if du_lieu:
            for line in du_lieu:
                new_line += [(0,0,{
						'NGAY_HACH_TOAN' : line.get('NGAY_HACH_TOAN'),
						'NGAY_CHUNG_TU' : line.get('NGAY_CHUNG_TU'),
						'SO_CHUNG_TU' : line.get('SO_CHUNG_TU'),
						'SO_HOA_DON' : line.get('SO_HOA_DON'),
						'NGAY_HOA_DON' : line.get('NGAY_HOA_DON'),
						'DIEN_GIAI' : line.get('DIEN_GIAI_CHUNG'),
						'DOI_TUONG_ID' : [line.get('DOI_TUONG_ID'),line.get('TEN_DOI_TUONG')],
						'TONG_CHI_PHI' : line.get('TONG_CHI_PHI_QUY_DOI'),
						'SO_PHAN_BO_LAN_NAY' : line.get('SO_PHAN_BO_LAN_NAY_QUY_DOI'),
						'LUY_KE_SO_DA_PHAN_BO' : 0,
                        'ID_CHUNG_TU_GOC' : line.get('ID_CHUNG_TU'),
						})]
        return new_line

    def sql_lay_du_lieu_chung_tu(self,doi_tuong_id,tu_ngay,den_ngay,id_chung_tu):
        params = {
            'DOI_TUONG_ID' : doi_tuong_id,
            'TU_NGAY' : tu_ngay,
            'DEN_NGAY' : den_ngay,
            'CHI_NHANH_ID' : self.get_chi_nhanh(),
            'ID_CHUNG_TU' : id_chung_tu,
            }
        query = """   

                DO LANGUAGE plpgsql $$ DECLARE

                doi_tuong_id  INTEGER := %(DOI_TUONG_ID)s;
                tu_ngay DATE:= %(TU_NGAY)s;
                den_ngay DATE := %(DEN_NGAY)s;
                loai_hach_toan INTEGER:=0; /*1: Phí trước hải quan, 0: Phí hàng về kho*/
                chi_nhanh_id INTEGER := %(CHI_NHANH_ID)s;
                id_chung_tu_mua_hang INTEGER := %(ID_CHUNG_TU)s;

                loai_tien_chinh_id INTEGER;


                BEGIN

                SELECT value
                INTO loai_tien_chinh_id
                FROM ir_config_parameter
                WHERE key = 'he_thong.LOAI_TIEN_CHINH'
                FETCH FIRST 1 ROW ONLY;

                DROP TABLE IF EXISTS TMP_KET_QUA;
                CREATE TEMP TABLE TMP_KET_QUA
                    AS
                    SELECT
                        PS.id                        AS "ID_CHUNG_TU"
                        , loai_hach_toan               AS "LOAI_HACH_TOAN"
                        , PS."NGAY_HACH_TOAN"
                        , PS."NGAY_CHUNG_TU"
                        , PS."LOAI_CHUNG_TU"
                        , PS."SO_CHUNG_TU_MUA_DICH_VU" AS "SO_CHUNG_TU"
                        , PS."DIEN_GIAI_CHUNG"
                        , PS."DOI_TUONG_ID"
                        , PS."SO_HOA_DON"
                        , PS."TEN_DOI_TUONG"
                        , CASE WHEN PS."currency_id" = loai_tien_chinh_id
                        THEN 0
                        ELSE (SELECT SUM(CASE coalesce(DT."TK_THUE_GTGT_ID", -1)
                                        WHEN -1
                                            THEN (coalesce(DT."THANH_TIEN", 0) - coalesce(DT."TIEN_CHIET_KHAU", 0)
                                                + coalesce(DT."TIEN_THUE_GTGT", 0))
                                        ELSE (coalesce(DT."THANH_TIEN", 0) - coalesce(DT."TIEN_CHIET_KHAU", 0))
                                        END) AS "TONG_CHI_PHI_NGUYEN_TE"
                                FROM purchase_document_line DT
                                WHERE order_id = PS.id
                        )
                        END                          AS "TONG_CHI_PHI_NGUYEN_TE"
                        , (SELECT SUM(CASE coalesce(DT."TK_THUE_GTGT_ID", -1)
                                    WHEN -1
                                        THEN (coalesce(DT."THANH_TIEN_QUY_DOI", 0) - coalesce(DT."TIEN_CHIET_KHAU_QUY_DOI", 0) +
                                            coalesce(DT."TIEN_THUE_GTGT_QUY_DOI", 0))
                                    ELSE (coalesce(DT."THANH_TIEN_QUY_DOI", 0) - coalesce(DT."TIEN_CHIET_KHAU_QUY_DOI", 0))
                                    END) AS "TONG_CHI_PHI_QUY_DOI"
                        FROM purchase_document_line DT
                        WHERE order_id = PS.id
                        )                            AS "TONG_CHI_PHI_QUY_DOI"
                        , /*hoant 26.06.2017*/
                        CASE WHEN PS."currency_id" = loai_tien_chinh_id
                            THEN 0
                        ELSE (SELECT SUM(CASE coalesce(DT."TK_THUE_GTGT_ID", -1)
                                        WHEN -1
                                            THEN (coalesce(DT."THANH_TIEN", 0) - coalesce(DT."TIEN_CHIET_KHAU", 0)
                                                + coalesce(DT."TIEN_THUE_GTGT", 0))
                                        ELSE (coalesce(DT."THANH_TIEN", 0) - coalesce(DT."TIEN_CHIET_KHAU", 0))
                                        END) AS "TONG_CHI_PHI_CHUNG"
                                FROM purchase_document_line DT
                                WHERE order_id = PS.id
                            )
                            - (SELECT coalesce(SUM(coalesce(PVDC."SO_PHAN_BO_LAN_NAY", 0)), 0)
                                FROM purchase_chi_phi PVDC
                                    INNER JOIN purchase_document PV ON PVDC."purchase_document_id" = PV.id
                                WHERE PVDC."purchase_document_id" = PS.id
                                        AND PVDC."purchase_document_id" <> id_chung_tu_mua_hang
                            )
                        END                          AS "SO_PHAN_BO_LAN_NAY"
                        , /*end */
                        (SELECT SUM(CASE coalesce(DT."TK_THUE_GTGT_ID", -1)
                                    WHEN -1
                                        THEN (coalesce(DT."THANH_TIEN_QUY_DOI", 0) - coalesce(DT."TIEN_CHIET_KHAU_QUY_DOI", 0) +
                                            coalesce(DT."TIEN_THUE_GTGT_QUY_DOI", 0))
                                    ELSE (coalesce(DT."THANH_TIEN_QUY_DOI", 0) - coalesce(DT."TIEN_CHIET_KHAU_QUY_DOI", 0))
                                    END) AS "TONG_CHI_PHI_QUY_DOI"
                        FROM purchase_document_line DT
                        WHERE order_id = PS.id
                        )
                        - (SELECT coalesce(SUM(coalesce(PVDC."SO_PHAN_BO_LAN_NAY_QUY_DOI", 0)), 0)
                            FROM purchase_chi_phi PVDC
                            INNER JOIN purchase_document PV ON PVDC."purchase_document_id" = PV.id
                            WHERE PVDC."purchase_document_id" = PS.id
                                AND PVDC."purchase_document_id" <> id_chung_tu_mua_hang
                        )                            AS "SO_PHAN_BO_LAN_NAY_QUY_DOI"
                        , (SELECT "NGAY_HOA_DON"
                        FROM purchase_document_line AS PVSD
                        WHERE PVSD.order_id = PS.id
                                AND PVSD."NGAY_HOA_DON" IS NOT NULL
                        FETCH FIRST 1 ROW ONLY
                        )                            AS "NGAY_HOA_DON"
                        , PS."currency_id"
                        , PS."TY_GIA"
                    FROM purchase_document PS
                    WHERE type = 'dich_vu'
                            AND (doi_tuong_id IS NULL
                                OR "DOI_TUONG_ID" = doi_tuong_id
                            )
                            AND "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                            AND PS."LA_CHI_PHI_MUA_HANG" = TRUE
                            AND PS."TONG_TIEN_HANG_QUY_DOI" - Ps."TONG_TIEN_CK_GTGT_QUY_DOI" > 0
                            AND (((SELECT SUM(CASE coalesce(DT."TK_THUE_GTGT_ID", -1)
                                            WHEN -1
                                                THEN (coalesce(DT."THANH_TIEN_QUY_DOI", 0) - coalesce(DT."TIEN_CHIET_KHAU_QUY_DOI", 0)
                                                    + coalesce(DT."TIEN_THUE_GTGT_QUY_DOI", 0))
                                            ELSE (coalesce(DT."THANH_TIEN_QUY_DOI", 0) - coalesce(DT."TIEN_CHIET_KHAU_QUY_DOI", 0))
                                            END) AS "TONG_CHI_PHI_QUY_DOI"
                                FROM purchase_document_line DT
                                WHERE DT.order_id = PS.id
                                )
                                - (SELECT coalesce(SUM(coalesce("SO_PHAN_BO_LAN_NAY", 0)), 0)
                                    FROM purchase_chi_phi PVDC
                                    INNER JOIN purchase_document PV ON PVDC."purchase_document_id" = PV.id
                                    WHERE PVDC."ID_CHUNG_TU_GOC" = PS.id
                                        AND PVDC."purchase_document_id" <> id_chung_tu_mua_hang
                                ) > 0)
                            )
                            AND PS."CHI_NHANH_ID" = chi_nhanh_id
                            AND PS.state = 'da_ghi_so'
                ;

                END $$;

                SELECT *
                FROM TMP_KET_QUA

        """  
        return self.execute(query, params)

