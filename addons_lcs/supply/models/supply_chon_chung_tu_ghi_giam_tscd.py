# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
import json
import ast

class SUPPLY_CHON_CHUNG_TU_GHI_GIAM_TSCD(models.Model):
    _name = 'supply.chon.chung.tu.ghi.giam.tscd'
    _description = ''
    _auto = False

    KY = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ', help='Kỳ báo cáo', default='THANG_NAY',required=True)
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày')
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    SUPPLY_CHON_CHUNG_TU_GHI_GIAM_TSCD_CHI_TIET_IDS = fields.One2many('supply.chon.chung.tu.ghi.giam.tscd.chi.tiet', 'CHON_CHUNG_TU_GHI_GIAM_TSCD_ID', string='Chọn chứng từ ghi giảm tscd chi tiết')
    CHUNG_TU_DA_CHON_JSON = fields.Text(string='Tên nhãn', help='Tên nhãn')
    LAY_DU_LIEU_JSON = fields.Text()

    # def action_view_result(self):
    #     action = self.env.ref('supply.action_open_supply_chon_chung_tu_ghi_giam_tscd_form').read()[0]
    #     # action['options'] = {'clear_breadcrumbs': True}
    #     return action

    @api.onchange('KY')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY, 'TU_NGAY', 'DEN_NGAY')


    @api.onchange('LAY_DU_LIEU_JSON')
    def _onchange_LAY_DU_LIEU_JSON(self):
        if self.LAY_DU_LIEU_JSON:
            param = ast.literal_eval(self.LAY_DU_LIEU_JSON)
            if param:
                chung_tu = self.lay_du_ghi_giam_tscd(param.get('TU_NGAY'),param.get('DEN'))
                if chung_tu:
                    env = self.env['supply.chon.chung.tu.ghi.giam.tscd.chi.tiet']
                    self.SUPPLY_CHON_CHUNG_TU_GHI_GIAM_TSCD_CHI_TIET_IDS = []
                    for line in chung_tu:
                        chon = False
                        if self.CHUNG_TU_DA_CHON_JSON:
                            dict_ct_da_chon = ast.literal_eval(self.CHUNG_TU_DA_CHON_JSON)
                            for line_ct in dict_ct_da_chon:
                                if line_ct.get('ID_GOC') == line.get('ID_GOC') and line_ct.get('MODEL_GOC') == line.get('MODEL_GOC'):
                                    chon = True
                        new_line = env.new({
                            'MA_TAI_SAN_ID': line.get('TSCD_ID'),
                            'TEN_TAI_SAN': line.get('TEN_TSCD'),
                            'NGAY_HACH_TOAN': line.get('NGAY_HACH_TOAN'),
                            'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU'),
                            'SO_CHUNG_TU': line.get('SO_CHUNG_TU'),
                            'GIA_TRI_CON_LAI': line.get('GIA_TRI_CON_LAI'),
                            'TK_XU_LY_GIA_TRI_CON_LAI_ID': line.get('TK_XU_LY_GIA_TRI_CON_LAI_ID'),
                            'ID_GOC': line.get('ID_GOC'),
                            'MODEL_GOC': line.get('MODEL_GOC'),
                            'CHON' : chon,
                        })
                        self.SUPPLY_CHON_CHUNG_TU_GHI_GIAM_TSCD_CHI_TIET_IDS += new_line
                else:
                    self.SUPPLY_CHON_CHUNG_TU_GHI_GIAM_TSCD_CHI_TIET_IDS = []

    @api.model
    def default_get(self, fields):
        rec = super(SUPPLY_CHON_CHUNG_TU_GHI_GIAM_TSCD, self).default_get(fields)
        arr_chung_tu_da_chon = []
        chung_tu_da_chon = self._context.get('SUPPLY_CHON_CHUNG_TU_GHI_GIAM_TSCD_CHI_TIET_IDS')
        if chung_tu_da_chon:
        # if len(chung_tu_da_chon) > 0:
                for line in chung_tu_da_chon:
                        arr_chung_tu_da_chon.append({
                                'ID_GOC' : line.get('ID_GOC'),
                                'MODEL_GOC' : line.get('MODEL_GOC'),
                        })
                rec['CHUNG_TU_DA_CHON_JSON'] = json.dumps(arr_chung_tu_da_chon)
        return rec

    def lay_du_ghi_giam_tscd(self,tu_ngay,den_ngay):
        params = {
            'TU_NGAY': tu_ngay,
            'DEN_NGAY' : den_ngay,
            'CHI_NHANH_ID' : self.get_chi_nhanh(),
            }

        query = """   

            DO LANGUAGE plpgsql $$
            DECLARE
            tu_ngay                     DATE := %(TU_NGAY)s;
            den_ngay                    DATE := %(DEN_NGAY)s;
            chi_nhanh_id                INTEGER := %(CHI_NHANH_ID)s;

            BEGIN
            DROP TABLE IF EXISTS TMP_KET_QUA;
            CREATE TEMP TABLE TMP_KET_QUA
                AS
                SELECT
                            FA.id AS "ID_GOC" ,
                            'asset.ghi.giam' AS "MODEL_GOC",
                            FAD."MA_TAI_SAN" AS "TSCD_ID",
                            FIA."MA_TAI_SAN" ,
                            FIA.name AS "TEN_TSCD" ,
                            FA."NGAY_CHUNG_TU" ,
                            "NGAY_HACH_TOAN" ,
                            FA."SO_CHUNG_TU" ,
                            FAD."GIA_TRI_CON_LAI" ,
            --                 coalesce(FAD."TK_XU_LY_GIA_TRI_CON_LAI_ID", 0) "TK_XU_LY_GIA_TRI_CON_LAI_ID" ,
                            FAD."DON_VI_SU_DUNG_ID" ,
                            FAD."TK_XU_LY_GIA_TRI_CON_LAI_ID" ,
                            FA."LOAI_CHUNG_TU"
                    FROM    asset_ghi_giam AS FA
                            INNER JOIN asset_ghi_giam_tai_san AS FAD ON FA.id = FAD."TAI_SAN_CO_DINH_GHI_GIAM_ID"
                            INNER JOIN asset_ghi_tang AS FIA ON FAD."MA_TAI_SAN" = FIA.id
                            INNER JOIN (
            --                         F @AccountingSystem = 48 AND @SubAccountSystem = 133 SET @List"MA_TK" = '642,242,154'
            --                           IF @AccountingSystem = 48 AND @SubAccountSystem = 0 SET @List"MA_TK" = ',642,142,242,154'
                                    SELECT *FROM danh_muc_he_thong_tai_khoan where "SO_TAI_KHOAN" in ('6412','6413','6422','6423','6272','6273','6232','6233','242')
                                    ) T ON FAD."TK_XU_LY_GIA_TRI_CON_LAI_ID" = T.id


                            -- nmtruong 30/6/2016: 105414 Không lấy lên ở phần Điều chỉnh công cụ dụng cụ
                            LEFT JOIN ( SELECT  SR.*
                                        FROM    supply_dieu_chinh_chi_tiet SR
                                                INNER JOIN supply_dieu_chinh M1 ON M1.id = SR."CHI_TIET_DIEU_CHINH_CCDC_ID_ID"
                                        WHERE   M1."CHI_NHANH_ID" = chi_nhanh_id
                                    ) ADV ON ADV."CHI_TIET_DIEU_CHINH_CCDC_ID_ID" = FA.id
                            -- nmtruong 30/6/2016: 105414 Không lấy lên ở phần Chi phí trả trước
                            LEFT JOIN (
                                        SELECT  SR.*
                                        FROM    tong_hop_chi_phi_tra_truoc_tap_hop_chung_tu SR
                                        INNER JOIN tong_hop_chi_phi_tra_truoc M ON M.id = SR."CHI_PHI_TRA_TRUOC_ID"
                                            WHERE   M."CHI_NHANH_ID" = chi_nhanh_id
                                        GROUP BY SR."CHI_PHI_TRA_TRUOC_ID",
                                                SR.id
                                    ) PR ON FA.id = PR."CHI_PHI_TRA_TRUOC_ID"
                            -- nmtruong 30/6/2016: 105414 Không lấy lên ở phần Ghi tăng công cụ dụng cụ
                            LEFT JOIN ( SELECT  SR.*
                                        FROM    supply_ghi_tang_nguon_goc_hinh_thanh SR
                                        INNER JOIN asset_ghi_tang M ON M.id = SR."GHI_TANG_NGUON_GOC_HINH_THANH_ID"
                                            WHERE   M."CHI_NHANH_ID" = chi_nhanh_id
                                        GROUP BY SR."GHI_TANG_NGUON_GOC_HINH_THANH_ID",
                                                SR.id
                                    ) SR ON FA.id = SR."GHI_TANG_NGUON_GOC_HINH_THANH_ID"
                    WHERE   FA."NGAY_CHUNG_TU" BETWEEN tu_ngay AND den_ngay
                            AND FA."CHI_NHANH_ID" = chi_nhanh_id
                            AND PR."CHI_PHI_TRA_TRUOC_ID" IS NULL
                            AND SR."GHI_TANG_NGUON_GOC_HINH_THANH_ID" IS NULL
                            AND ADV."CHI_TIET_DIEU_CHINH_CCDC_ID_ID" IS NULL
                    ORDER BY FA."NGAY_HACH_TOAN" ,
                            FA."NGAY_CHUNG_TU" ,
                            Fa."SO_CHUNG_TU"
            ;

            END $$;

            SELECT *
            FROM TMP_KET_QUA;


        """  
        
        return self.execute(query, params)

