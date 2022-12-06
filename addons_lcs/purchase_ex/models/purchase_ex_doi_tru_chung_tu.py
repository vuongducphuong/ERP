# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
import json

class PURCHASE_EX_DOI_TRU_CHUNG_TU(models.Model):
    _name = 'purchase.ex.doi.tru.chung.tu'
    _description = ''
    _auto = False

    DOI_TUONG_ID = fields.Many2one('res.partner', string='Nhà cung cấp', help='Nhà cung cấp')
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    TAI_KHOAN_PHAI_TRA_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản phải trả', help='Tài khoản phải trả')
    NGAY_DOI_TRU = fields.Date(string='Ngày đối trừ', help='Ngày đối trừ',default=fields.Datetime.now)
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    TK_XU_LY_CL_LAI_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK xử lý CL lãi', help='Tài khoản xử lý chênh lệch lãi')
    TK_XU_LY_CL_LO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK xử lý CL lỗ', help='Tài khoản xử lý chênh lệch lỗ')
    IS_TY_GIA = fields.Boolean(string='Loại tiền', help='Loại tiền',default=True)
    LAY_DU_LIEU_JSON = fields.Text()

    #FIELD_IDS = fields.One2many('model.name')
    @api.model
    def default_get(self,default_fields):
        res = super(PURCHASE_EX_DOI_TRU_CHUNG_TU, self).default_get(default_fields)
        res['TAI_KHOAN_PHAI_TRA_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like','331%')], limit=1).id
        res['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=like','VND%')], limit=1).id
        res['TK_XU_LY_CL_LAI_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','515')]).id
        res['TK_XU_LY_CL_LO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','635')]).id
        return res

    PURCHASE_EX_DOI_TRU_CHUNG_TU_THANH_TOAN_IDS = fields.One2many('purchase.ex.doi.tru.chung.tu.thanh.toan', 'DOI_TRU_CHUNG_TU_ID', string='Đối trừ chứng từ thanh toán')
    PURCHASE_EX_DOI_TRU_CHUNG_TU_CONG_NO_IDS = fields.One2many('purchase.ex.doi.tru.chung.tu.cong.no', 'DOI_TRU_CHUNG_TU_ID', string='Đối trừ chứng từ công nợ')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())



    @api.onchange('LAY_DU_LIEU_JSON')
    def _onchange_LAY_DU_LIEU_JSON(self):
        if self.LAY_DU_LIEU_JSON:
            if self.DOI_TUONG_ID:
                param = json.loads(self.LAY_DU_LIEU_JSON)
                if param:
                    self.them_dong_du_lieu(param.get('NGAY'),param.get('DOI_TUONG_ID'),param.get('currency_id'))
            else:
                raise ValidationError("<Khách hàng> không được bỏ trống")


    def them_dong_du_lieu(self,ngay,khach_hang,loai_tien):
        ct_thanh_toan = self.lay_chung_tu_thanh_toan(ngay,khach_hang,loai_tien)
        ct_cong_no = self.lay_chung_tu_cong_no(ngay,khach_hang,loai_tien)
        env = self.env['purchase.ex.doi.tru.chung.tu.thanh.toan']
        env1 = self.env['purchase.ex.doi.tru.chung.tu.cong.no']
        self.PURCHASE_EX_DOI_TRU_CHUNG_TU_THANH_TOAN_IDS = []
        self.PURCHASE_EX_DOI_TRU_CHUNG_TU_CONG_NO_IDS = []
        for ct in ct_thanh_toan:
            ten_loai_chung_tu = self.env['danh.muc.reftype'].search([('REFTYPE', '=', ct.get('LOAI_CHUNG_TU'))], limit=1)
            new_line = env.new({
                'NGAY_CHUNG_TU': ct.get('NGAY_CHUNG_TU'),
                'SO_CHUNG_TU' : ct.get('SO_CHUNG_TU'),
                'DIEN_GIAI' : ct.get('DIEN_GIAI'),
                'NHAN_VIEN_ID' : ct.get('NHAN_VIEN_ID'),
                'TEN_NHAN_VIEN' : ct.get('TEN_NHAN_VIEN'),
                'SO_TIEN' : ct.get('SO_TIEN'),
                'SO_CHUA_DOI_TRU' : ct.get('SO_TIEN'),
                'SO_TIEN_DOI_TRU' : ct.get('SO_TIEN_DOI_TRU'),
                'TEN_LOAI_CHUNG_TU' : ten_loai_chung_tu.REFTYPENAME,
                'LOAI_CHUNG_TU' : ct.get('LOAI_CHUNG_TU'),
            })
            self.PURCHASE_EX_DOI_TRU_CHUNG_TU_THANH_TOAN_IDS += new_line
        for line in ct_cong_no:
            ten_loai_ct_cong_no = self.env['danh.muc.reftype'].search([('REFTYPE', '=', line.get('LOAI_CHUNG_TU'))], limit=1)
            new_line1 = env1.new({
                'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU'),
                'SO_CHUNG_TU' : line.get('SO_CHUNG_TU'),
                'DIEN_GIAI' : line.get('DIEN_GIAI'),
                'NHAN_VIEN_ID' : line.get('NHAN_VIEN_ID'),
                'TEN_NHAN_VIEN' : line.get('TEN_NHAN_VIEN'),
                'SO_TIEN' : line.get('SO_TIEN'),
                'SO_CON_NO' : line.get('SO_TIEN'),
                'SO_TIEN_DOI_TRU' : line.get('SO_TIEN_DOI_TRU'),
                'TEN_LOAI_CHUNG_TU' : ten_loai_ct_cong_no.REFTYPENAME,
                'LOAI_CHUNG_TU' : line.get('LOAI_CHUNG_TU'),
            })
            self.PURCHASE_EX_DOI_TRU_CHUNG_TU_CONG_NO_IDS += new_line1


    @api.onchange('currency_id')
    def update_loai_tien(self):
        if self.currency_id.MA_LOAI_TIEN == 'VND':
            self.IS_TY_GIA = False
        else:
            self.IS_TY_GIA =True

    # def action_view_result(self):
    #     tong_tien_thanh_toan = 0
    #     tong_tien_cong_no = 0
    #     for line in self.get_context('PURCHASE_EX_DOI_TRU_CHUNG_TU_THANH_TOAN_IDS'):
    #         if line['CHON'] == 'True':
    #             tong_tien_thanh_toan += line['SO_TIEN_DOI_TRU']
    #     for line in self.get_context('PURCHASE_EX_DOI_TRU_CHUNG_TU_CONG_NO_IDS'):
    #         if line['CHON'] == 'True':
    #             tong_tien_cong_no += line['SO_TIEN_DOI_TRU']
    #     if tong_tien_cong_no != tong_tien_thanh_toan:
    #         raise ValidationError('Tổng số tiền đối trừ của <Chứng từ thanh toán> phải bằn tổng số tiền đối trừ chứng từ của <Chứng từ còn nợ>.')
    #     # action = self.env.ref('purchase_ex.action_open_purchase_ex_doi_tru_chung_tu_form').read()[0]
    #     # # action['options'] = {'clear_breadcrumbs': True}
    #     # return action

    # @api.depends('PURCHASE_EX_DOI_TRU_CHUNG_TU_THANH_TOAN_IDS.CHON')
    # def doi_tru_chung_tu(self):
    #     tong_tien_thanh_toan = 0
    #     tong_tien_cong_no = 0
    #     for line in self.PURCHASE_EX_DOI_TRU_CHUNG_TU_THANH_TOAN_IDS:
    #         if line.CHON == True:
    #             tong_tien_thanh_toan += line.SO_CHUA_DOI_TRU
    #     for line in self.PURCHASE_EX_DOI_TRU_CHUNG_TU_CONG_NO_IDS:
    #         if line.CHON == True:
    #             tong_tien_cong_no += line.SO_CON_NO
    #     if tong_tien_cong_no > 0 and tong_tien_thanh_toan > 0:
    #         if tong_tien_thanh_toan > tong_tien_cong_no:
    #             for line in self.PURCHASE_EX_DOI_TRU_CHUNG_TU_CONG_NO_IDS:
    #                 if line.CHON == True:
    #                     line.SO_TIEN_DOI_TRU = line.SO_CON_NO
    #             for line1 in self.PURCHASE_EX_DOI_TRU_CHUNG_TU_THANH_TOAN_IDS:
    #                 if line1.CHON == True:
    #                     if tong_tien_cong_no == 0:
    #                     #     line1.SO_TIEN_DOI_TRU = line1.SO_CHUA_DOI_TRU
    #                     # if tong_tien_cong_no == 1:
    #                         line1.SO_TIEN_DOI_TRU = 0
    #                     elif line1.SO_CHUA_DOI_TRU < tong_tien_cong_no:
    #                         line1.SO_TIEN_DOI_TRU = line1.SO_CHUA_DOI_TRU
    #                         tong_tien_cong_no = tong_tien_cong_no - line1.SO_TIEN_DOI_TRU
    #                     elif line1.SO_CHUA_DOI_TRU > tong_tien_cong_no:
    #                         line1.SO_TIEN_DOI_TRU = tong_tien_cong_no
    #                         tong_tien_cong_no = 0
    #         elif tong_tien_thanh_toan < tong_tien_cong_no:
    #             for line1 in self.PURCHASE_EX_DOI_TRU_CHUNG_TU_THANH_TOAN_IDS:
    #                 if line1.CHON == True:
    #                     # if line1.SO_CHUA_DOI_TRU > tong_tien_cong_no:
    #                     #     line1.SO_TIEN_DOI_TRU = tong_tien_cong_no
    #                     #     tong_tien_cong_no = 0
    #                     line1.SO_TIEN_DOI_TRU = line1.SO_TIEN

    #             for line in self.PURCHASE_EX_DOI_TRU_CHUNG_TU_CONG_NO_IDS:
    #                 if line.CHON == True:
    #                     if tong_tien_thanh_toan == 0:
    #                         #line.SO_TIEN_DOI_TRU = line.SO_CON_NO
    #                     # if tong_tien_thanh_toan == 1:
    #                         line.SO_TIEN_DOI_TRU = 0
    #                     elif tong_tien_thanh_toan > line.SO_CON_NO:
    #                         line.SO_TIEN_DOI_TRU = line.SO_CON_NO
    #                         tong_tien_thanh_toan = tong_tien_thanh_toan - line.SO_TIEN_DOI_TRU
    #                     elif tong_tien_thanh_toan  < line.SO_CON_NO:
    #                         line.SO_TIEN_DOI_TRU = tong_tien_thanh_toan
    #                         tong_tien_thanh_toan = 0

    # @api.depends('PURCHASE_EX_DOI_TRU_CHUNG_TU_CONG_NO_IDS.CHON')
    # def doi_tru_cong_no(self):
    #     tong_tien_thanh_toan = 0
    #     tong_tien_cong_no = 0
    #     for line in self.PURCHASE_EX_DOI_TRU_CHUNG_TU_THANH_TOAN_IDS:
    #         if line.CHON == True:
    #             tong_tien_thanh_toan += line.SO_CHUA_DOI_TRU
    #     for line in self.PURCHASE_EX_DOI_TRU_CHUNG_TU_CONG_NO_IDS:
    #         if line.CHON == True:
    #             tong_tien_cong_no += line.SO_CON_NO
    #     if tong_tien_cong_no > 0 and tong_tien_thanh_toan > 0:
    #         if tong_tien_thanh_toan > tong_tien_cong_no:
    #             for line in self.PURCHASE_EX_DOI_TRU_CHUNG_TU_CONG_NO_IDS:
    #                 if line.CHON == True:
    #                     line.SO_TIEN_DOI_TRU = line.SO_CON_NO
    #             for line1 in self.PURCHASE_EX_DOI_TRU_CHUNG_TU_THANH_TOAN_IDS:
    #                 if line1.CHON == True:
    #                     if tong_tien_cong_no == 0:
    #                     #     line1.SO_TIEN_DOI_TRU = line1.SO_CHUA_DOI_TRU
    #                     # if tong_tien_cong_no == 1:
    #                         line1.SO_TIEN_DOI_TRU = 0
    #                     elif line1.SO_CHUA_DOI_TRU < tong_tien_cong_no:
    #                         line1.SO_TIEN_DOI_TRU = line1.SO_CHUA_DOI_TRU
    #                         tong_tien_cong_no = tong_tien_cong_no - line1.SO_TIEN_DOI_TRU
    #                     elif line1.SO_CHUA_DOI_TRU > tong_tien_cong_no:
    #                         line1.SO_TIEN_DOI_TRU = tong_tien_cong_no
    #                         tong_tien_cong_no = 0
    #         elif tong_tien_thanh_toan < tong_tien_cong_no:
    #             for line1 in self.PURCHASE_EX_DOI_TRU_CHUNG_TU_THANH_TOAN_IDS:
    #                 if line1.CHON == True:
    #                     # if line1.SO_CHUA_DOI_TRU > tong_tien_cong_no:
    #                     #     line1.SO_TIEN_DOI_TRU = tong_tien_cong_no
    #                     #     tong_tien_cong_no = 0
    #                     line1.SO_TIEN_DOI_TRU = line1.SO_TIEN

    #             for line in self.PURCHASE_EX_DOI_TRU_CHUNG_TU_CONG_NO_IDS:
    #                 if line.CHON == True:
    #                     if tong_tien_thanh_toan == 0:
    #                         #line.SO_TIEN_DOI_TRU = line.SO_CON_NO
    #                     # if tong_tien_thanh_toan == 1:
    #                         line.SO_TIEN_DOI_TRU = 0
    #                     elif tong_tien_thanh_toan > line.SO_CON_NO:
    #                         line.SO_TIEN_DOI_TRU = line.SO_CON_NO
    #                         tong_tien_thanh_toan = tong_tien_thanh_toan - line.SO_TIEN_DOI_TRU
    #                     elif tong_tien_thanh_toan  < line.SO_CON_NO:
    #                         line.SO_TIEN_DOI_TRU = tong_tien_thanh_toan
    #                         tong_tien_thanh_toan = 0

    #     # for line2 in self.PURCHASE_EX_DOI_TRU_CHUNG_TU_CONG_NO_IDS:
    #     #     if line2.CHON == True:
    #     #         if tong_tien_doi_tru > line2.SO_CON_NO:
    #     #             line2.SO_TIEN_DOI_TRU = line2.SO_CON_NO
    #     #             tong_tien_doi_tru = tong_tien_doi_tru - line2.SO_CON_NO
    #     #         elif tong_tien_doi_tru < line2.SO_CON_NO:
    #     #             line2.SO_TIEN_DOI_TRU = tong_tien_doi_tru
    #     #             tong_tien_doi_tru = 0

    

    def lay_chung_tu_thanh_toan(self,ngay,doi_tuong,loai_tien):
        record = []
        params = {
            'DOI_TUONG_ID': 594,
            'currency_id' : loai_tien,
            'DEN_NGAY' : ngay,
            }

        query = """   

           

          SELECT  AL."ID_CHUNG_TU" ,
                AL."LOAI_CHUNG_TU" ,
--                AL."LOAI_CHUNG_TU" ,
                AL."NGAY_CHUNG_TU" ,
                AL."NGAY_HACH_TOAN" ,
                AL."SO_CHUNG_TU" ,
                AL."SO_HOA_DON" ,
                AL."DIEN_GIAI" ,
                AL."TY_GIA" ,
                coalesce(GV."TY_GIA", 0) AS "TY_GIA" ,
                SUM(AL."SO_TIEN") AS "SO_TIEN" ,
                SUM(AL."SO_TIEN_QUY_DOI") AS "SO_TIEN_QUY_DOI" ,
                SUM(AL."SO_TIEN_THU") AS "SO_TIEN_THU" ,
                SUM(AL."SO_TIEN_THU_QUY_DOI") AS "SO_TIEN_THU_QUY_DOI" ,
                0 AS "SO_TIEN_DOI_TRU" ,
                0 AS "SO_TIEN_DOI_TRU_QUY_DOI" ,
                594 AS "DOI_TUONG_ID" ,
                AL."NHAN_VIEN_ID" , --NVTOAN modify 14/04/2017 thực hiện CR 34929
                E."MA_DOI_TUONG" AS "MA_NHAN_VIEN" , --nvtoan Modify 22/04/2017: Sửa lỗi 96455
                E.name AS "TEN_NHAN_VIEN"
        FROM    (


SELECT
                            OPNTemp."ID_CHUNG_TU" ,
                            OPNTemp."LOAI_CHUNG_TU" ,
--                             OPNTemp."LOAI_CHUNG_TU" ,
                            OPNTemp."NGAY_CHUNG_TU" ,
                            OPNTemp."NGAY_HACH_TOAN", -- nmtruong: 11/5/2016 sửa bug 101936 thay refdate = posteddate để ghi xuống bảng đối trừ đúng ngày hạch toán
                            OPNTemp."SO_CHUNG_TU" ,
                            OPNTemp."SO_HOA_DON" ,
                            OPNTemp."DIEN_GIAI" ,
                            OPNTemp."TY_GIA" ,
                            OPNTemp."SO_TIEN" ,
                            OPNTemp."SO_TIEN_QUY_DOI" ,
                            (OPNTemp."SO_TIEN_THU" - coalesce(SUM(GL."SO_TIEN"),0)) AS "SO_TIEN_THU" ,
                            OPNTemp."SO_TIEN_THU_QUY_DOI" - coalesce(SUM(GL."SO_TIEN_QUY_DOI"), 0) AS "SO_TIEN_THU_QUY_DOI" ,
                            OPNTemp."DOI_TUONG_ID" ,
                            OPNTemp."SO_TAI_KHOAN" ,
                            OPNTemp."NHAN_VIEN_ID"  --NVTOAN modify 14/04/2017 thực hiện CR 34929
                  FROM      (



                              SELECT
          OPN.id AS "ID_CHUNG_TU" ,
          OPN."LOAI_CHUNG_TU" ,
--           RT."TEN_LOAI" AS "TEN_LOAI_CHUNG_TU" ,
          ( CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL AND OPI."SO_THU_TRUOC" <> 0
                 THEN OPI."NGAY_HOA_DON"
                 ELSE OPN."NGAY_HACH_TOAN"
            END ) "NGAY_CHUNG_TU" ,
          OPN."NGAY_HACH_TOAN" ,
          ( CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL AND OPI."SO_THU_TRUOC" <> 0
                 THEN coalesce(OPI."SO_HOA_DON", '')
                 ELSE N'OPN'
            END ) AS "SO_CHUNG_TU",
          coalesce(OPI."SO_HOA_DON", '') AS "SO_HOA_DON" ,
          '' AS "DIEN_GIAI" ,
          ( CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                 THEN coalesce(OPI."TY_GIA", 1)
                 ELSE coalesce(OPN."TY_GIA", 1)
            END ) AS "TY_GIA",
          SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                   THEN coalesce(OPI."SO_THU_TRUOC",0)
                   ELSE coalesce(OPN."DU_NO_NGUYEN_TE",0)- coalesce(OPN."DU_CO_NGUYEN_TE",0)
              END) AS "SO_TIEN" ,
          SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                   THEN coalesce(OPI."SO_THU_TRUOC", 0)
                   ELSE coalesce(OPN."DU_NO",0)- coalesce(OPN."DU_CO",0)
              END) AS "SO_TIEN_QUY_DOI" ,
          SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                   THEN coalesce(OPI."SO_THU_TRUOC",0)
                   ELSE coalesce(OPN."DU_NO_NGUYEN_TE",0)- coalesce(OPN."DU_CO_NGUYEN_TE",0)
              END) AS "SO_TIEN_THU",
          SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                   THEN coalesce(OPI."SO_THU_TRUOC", 0)
                   ELSE coalesce(OPN."DU_NO",0) - coalesce(OPN."DU_CO",0)
              END) AS "SO_TIEN_THU_QUY_DOI" ,
          594 AS "DOI_TUONG_ID" ,
          OPN."SO_TAI_KHOAN" ,
          1 AS "SO_HOA_DON_CHI_TIET" ,
          OPID2."NHAN_VIEN_ID"--NVTOAN modify 14/04/2017 thực hiện CR 34929
FROM      account_ex_so_du_tai_khoan_chi_tiet OPN
          INNER JOIN danh_muc_loai_chung_tu RT ON RT.id = OPN."LOAI_CHUNG_TU"
          LEFT JOIN account_ex_sdtkct_theo_hoa_don OPI ON OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" = OPN.id
          LEFT JOIN (
                      SELECT  OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID" ,
                              coalesce(OAEDI."NGAY_HOA_DON",NOW()) AS "NGAY_HOA_DON" ,
                              coalesce(OAEDI."SO_HOA_DON",'') AS "SO_HOA_DON" ,
                              coalesce(OAEDI."TY_GIA",0) AS "TY_GIA" ,
                              OAEDI."NHAN_VIEN_ID" ,
                              ROW_NUMBER() OVER ( PARTITION BY OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID",
                                coalesce(OAEDI."NGAY_HOA_DON",NOW()),
                                coalesce(OAEDI."SO_HOA_DON",''),
                                coalesce(OAEDI."TY_GIA",0)
                      ORDER BY OAEDI."THU_TU_TRONG_CHUNG_TU" ) AS RowNumber
                      FROM    account_ex_sdtkct_theo_hoa_don AS OAEDI
                      WHERE   OAEDI."NHAN_VIEN_ID" IS NOT NULL
                    ) AS OPID2 ON OPN.id = OPID2."SO_DU_TAI_KHOAN_CHI_TIET_ID"
                                AND OPID2.RowNumber = 1
                                AND coalesce(OPI."SO_HOA_DON",'') = coalesce(OPID2."SO_HOA_DON",'')
                                AND coalesce(OPI."NGAY_HOA_DON",NOW()) = coalesce(OPID2."NGAY_HOA_DON",NOW())
                                AND coalesce(OPI."TY_GIA",0) = coalesce(OPID2."TY_GIA",0)
                      --NVTOAN add 14/04/2017 thực hiện CR 34929
WHERE
          OPN."DOI_TUONG_ID" = 594
          AND OPN."currency_id" = %(currency_id)s
--           AND OPN."MA_TK" = (SELECT id FROM danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN" = '331')
--           AND OPN."CHI_NHANH_ID" = (chi_nhanh_id)
          AND OPN."NGAY_HACH_TOAN" <= '2019-02-28'

GROUP BY  OPN.id ,
          ( CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                      AND OPI."SO_THU_TRUOC" <> 0
                 THEN OPI."NGAY_HOA_DON"
                 ELSE OPN."NGAY_HACH_TOAN"
            END ) ,
          ( CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                 THEN coalesce(OPI."TY_GIA", 1)
                 ELSE coalesce(OPN."TY_GIA", 1)
            END ) ,
          OPN."LOAI_CHUNG_TU" ,
          RT."TEN_LOAI" ,
          OPN."NGAY_HACH_TOAN" ,
          ( CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                      AND OPI."SO_THU_TRUOC" <> 0
                 THEN coalesce(OPI."SO_HOA_DON", '')
                 ELSE N'OPN'
            END ) ,
          OPI."NGAY_HOA_DON" ,
          coalesce(OPI."SO_HOA_DON", '') ,
          coalesce(OPI."TY_GIA", 1) ,
          coalesce(OPN."TY_GIA", 1) ,
          OPN."SO_TAI_KHOAN" ,
          OPID2."NHAN_VIEN_ID"--NVTOAN modify 14/04/2017 thực hiện CR 34929
HAVING    SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                   THEN coalesce(OPI."SO_THU_TRUOC",0)
                   ELSE coalesce(OPN."DU_NO_NGUYEN_TE",0)- coalesce(OPN."DU_CO_NGUYEN_TE",0)
              END) > 0


UNION ALL


SELECT
          AL."ID_CHUNG_TU" ,
          AL."LOAI_CHUNG_TU" ,
--           AL."LOAI_CHUNG_TU" ,
          AL."NGAY_CHUNG_TU" ,
          AL."NGAY_HACH_TOAN" ,
          AL."SO_CHUNG_TU",
          coalesce(AL."SO_HOA_DON", '') AS "SO_HOA_DON",
          coalesce(AL."DIEN_GIAI_CHUNG", '') AS "DIEN_GIAI" ,
          coalesce(AL."TY_GIA", 1) AS "TY_GIA",
          SUM(coalesce(AL."GHI_NO_NGUYEN_TE", 0)
              - coalesce(AL."GHI_CO_NGUYEN_TE", 0)) AS "SO_TIEN" ,
          SUM(coalesce(AL."GHI_NO", 0)
              - coalesce(AL."GHI_CO", 0)) AS "SO_TIEN_QUY_DOI" ,
          SUM(coalesce(AL."GHI_NO_NGUYEN_TE", 0)
              - coalesce(AL."GHI_CO_NGUYEN_TE", 0)) AS "SO_TIEN_THU" ,
          SUM(coalesce(AL."GHI_NO", 0)
              - coalesce(AL."GHI_CO", 0)) AS "SO_TIEN_THU_QUY_DOI" ,
          594 AS "DOI_TUONG_ID" ,
          AL."MA_TK" ,
          0 AS "SO_HOA_DON_CHI_TIET" ,
          CASE WHEN GVDT."ID_CHUNG_TU" IS NOT NULL
               THEN GVDT."NHAN_VIEN_ID"
               ELSE AL."NHAN_VIEN_ID"
          END AS "NHAN_VIEN_ID"--NVTOAN modify 14/04/2017 thực hiện CR 34929
FROM      so_cong_no_chi_tiet AS AL
          LEFT JOIN (/*Lấy Nhân viên trên chứng từ nghiệp vụ khác*/
                                SELECT
                                  AOL."ID_CHUNG_TU" ,
                                  AOL."DOI_TUONG_ID" ,
                                  AOL."MA_TK" ,
                                  AOL."NHAN_VIEN_ID" ,
                                  ROW_NUMBER() OVER ( PARTITION BY AOL."ID_CHUNG_TU",
                                  AOL."DOI_TUONG_ID",
                                  AOL."MA_TK" ORDER BY AOL."THU_TU_TRONG_CHUNG_TU" ) AS RowNumber
                                FROM so_cong_no_chi_tiet AS AOL
                                WHERE AOL."LOAI_CHUNG_TU" IN ('4010', '4011', '4012','4014', '4015', '4018','4020', '4030' )
/*Chỉ lấy theo "LOAI_CHUNG_TU" của bảng GlVoucherDetail
Không lấy các chứng từ Chứng từ bù trừ công nợ, Xử lý chênh lệch tỷ giá từ đánh giá lại tài khoản ngoại tệ, Xử lý chênh lệch tỷ giá từ tính tỷ giá xuất quỹ
*/
                                AND AOL."NHAN_VIEN_ID" IS NOT NULL
                    ) AS GVDT ON GVDT."ID_CHUNG_TU" = AL."ID_CHUNG_TU"
                                AND GVDT."DOI_TUONG_ID" = AL."DOI_TUONG_ID"
                                AND GVDT."MA_TK" = AL."MA_TK"
                                AND GVDT.RowNumber = 1
                      --NVTOAN add 14/04/2017 thực hiện CR 34929
WHERE
          AL."DOI_TUONG_ID" = 594
          AND AL."currency_id" = %(currency_id)s
          AND AL."TK_ID" = (SELECT id FROM danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN" = '331')
--           AND AL."CHI_NHANH_ID" = (chi_nhanh_id)
--Không lấy các chứng từ Phiếu thu tiền khách hàng, Phiếu thu tiền khách hàng hàng loạt, Phiếu chi trả tiền nhà cung cấp, Phiếu thu tiền gửi khách hàng, Phiếu thu tiền gửi khách hàng hàng loạt, Trả tiền nhà cung cấp bằng Ủy nhiệm chi, Séc tiền mặt trả tiền nhà cung cấp, Séc chuyển khoản trả tiền nhà cung cấp, Chứng từ xử lý chênh lệch tỷ giá, Chứng từ bù trừ công nợ, Xử lý chênh lệch tỷ giá từ đánh giá lại tài khoản ngoại tệ, Xử lý chênh lệch tỷ giá từ tính tỷ giá xuất quỹ
          AND AL."LOAI_CHUNG_TU" NOT IN ( 1011, 1012,1021, 1502, 1503,1511, 1521, 1531,4013, 4016, 4017,611, 612, 613,614, 615, 616,630 )
          AND AL."NGAY_HACH_TOAN" <= '2019-02-28'

GROUP BY  AL."ID_CHUNG_TU" ,
          AL."LOAI_CHUNG_TU" ,
--           AL."LOAI_CHUNG_TU" ,
          AL."NGAY_CHUNG_TU" ,
          AL."NGAY_HACH_TOAN" ,
          AL."SO_CHUNG_TU" ,
          coalesce(AL."SO_HOA_DON", '') ,
          coalesce(AL."DIEN_GIAI_CHUNG", '') ,
          coalesce(AL."TY_GIA", 1) ,
          AL."MA_TK" ,
          CASE WHEN GVDT."ID_CHUNG_TU" IS NOT NULL
               THEN GVDT."NHAN_VIEN_ID"
               ELSE AL."NHAN_VIEN_ID"
          END --NVTOAN modify 14/04/2017 thực hiện CR 34929
HAVING    SUM(coalesce(AL."GHI_NO_NGUYEN_TE", 0)
              - coalesce(AL."GHI_CO_NGUYEN_TE", 0)) > 0




                            ) AS OPNTemp
                            LEFT JOIN (




SELECT
				CAST(GL."ID_CHUNG_TU_THANH_TOAN" AS INTEGER) AS "ID_CHUNG_TU"
				,GL."NGAY_CHUNG_TU_THANH_TOAN" AS "NGAY_CHUNG_TU"
				,GL."SO_CHUNG_TU_THANH_TOAN" AS "SO_CHUNG_TU"
				,Gl."DOI_TUONG_ID" AS "DOI_TUONG_ID"
				,TA."SO_TAI_KHOAN"
				,SUM(coalesce(GL."SO_TIEN_THANH_TOAN",0)) AS "SO_TIEN"
				,SUM(coalesce(GL."SO_TIEN_THANH_TOAN_QUY_DOI",0)) - SUM((CASE WHEN GL."LOAI_DOI_TRU" = '1' THEN 0 ELSE coalesce(GL."CHENH_LECH_TY_GIA_SO_TIEN_QUY_DOI",0) END)) AS "SO_TIEN_QUY_DOI"
		FROM 	sale_ex_doi_tru_chi_tiet GL
				INNER JOIN (
							SELECT*FROM danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN" = '331'
									 ) TA ON TA.id = GL."TAI_KHOAN_ID"
		WHERE
				GL."currency_id" = %(currency_id)s
-- 				AND GL."CHI_NHANH_ID" = (chi_nhanh_id)
				AND GL."CTTT_DA_GHI_SO" = True AND GL."CTCN_DA_GHI_SO" = True
				AND (GL."DOI_TUONG_ID" = 594 OR 594 IS NULL)
		GROUP BY GL."ID_CHUNG_TU_THANH_TOAN", GL."DOI_TUONG_ID",TA."SO_TAI_KHOAN",GL."NGAY_CHUNG_TU_THANH_TOAN",GL."SO_CHUNG_TU_THANH_TOAN"


UNION ALL


		SELECT
				cast(GLD."ID_CHUNG_TU" AS INTEGER)
				,GL."NGAY_CHUNG_TU" AS "NGAY_CHUNG_TU"
				,GL."SO_CHUNG_TU"  AS "SO_CHUNG_TU"
				,GLD."DOI_TUONG_ID"
				,TA."SO_TAI_KHOAN"
				,0 AS "SO_TIEN"
				,SUM(coalesce(GLD."CHENH_LECH",0)) AS "SO_TIEN_QUY_DOI"
		FROM	account_ex_chung_tu_nghiep_vu_khac GL
				INNER JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan GLD ON GLD."ID_CHUNG_TU_ID" = GL.id
				INNER JOIN (
							SELECT*FROM danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN" = '331'
									 ) TA ON GLD."TK_CONG_NO_ID" = TA.id
		WHERE
				GL."currency_id" = %(currency_id)s
-- 				AND Gl."CHI_NHANH_ID" = (chi_nhanh_id)
				AND (GLD."DOI_TUONG_ID" = 594 OR 594 IS NULL)
		GROUP BY GLD."ID_CHUNG_TU",
        GLD."DOI_TUONG_ID"
        ,TA."SO_TAI_KHOAN"
				,GL."NGAY_CHUNG_TU"
        ,GL."SO_CHUNG_TU"



UNION ALL



		SELECT
				SA. id AS "ID_CHUNG_TU"
				,SA."NGAY_CHUNG_TU" AS "NGAY_CHUNG_TU"
				,SA."SO_CHUNG_TU" AS "SO_CHUNG_TU"
				,SA."DOI_TUONG_ID"
				,TA."SO_TAI_KHOAN"
				,SUM(coalesce(SAD."THANH_TIEN",0) + coalesce(SAD."TIEN_THUE_GTGT",0) - coalesce(SAD."TIEN_CHIET_KHAU",0)) AS "SO_TIEN"
				,SUM(coalesce(SAD."THANH_TIEN_QUY_DOI",0) + coalesce(SAD."TIEN_THUE_GTGT_QUY_DOI",0) - coalesce(SAD."TIEN_CHIET_KHAU_QUY_DOI",0)) AS "SO_TIEN_QUY_DOI"
		FROM	sale_ex_tra_lai_hang_ban SA
				INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet SAD ON SAD."TRA_LAI_HANG_BAN_ID" = SA.id
				INNER JOIN (
							SELECT*FROM danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN" = '331'
									 ) TA ON SAD."TK_CO_ID" = TA.id
		WHERE
				SA."currency_id" = %(currency_id)s
-- 				AND SA."CHI_NHANH_ID" = (chi_nhanh_id)
				AND SAD."TRA_LAI_HANG_BAN_ID" IS NOT NULL
				AND (SA."DOI_TUONG_ID" = 594 OR 594 IS NULL)
		GROUP BY SA.id, SA."DOI_TUONG_ID",TA."SO_TAI_KHOAN"
				,SA."NGAY_CHUNG_TU"
				,SA."SO_CHUNG_TU"

UNION ALL

SELECT
				SA.id AS "ID_CHUNG_TU"
				,SA."NGAY_CHUNG_TU" AS "NGAY_CHUNG_TU"
				,SA."SO_CHUNG_TU" AS "SO_CHUNG_TU"
				,SA."DOI_TUONG_ID"
				,TA."SO_TAI_KHOAN"
				,SUM(coalesce(SAD."THANH_TIEN",0) + coalesce(SAD."TIEN_THUE_GTGT",0) - coalesce(SAD."TIEN_CHIET_KHAU",0)) AS "SO_TIEN"
				,SUM(coalesce(SAD."THANH_TIEN_QUY_DOI",0) + coalesce(SAD."TIEN_THUE_GTGT_QUY_DOI",0) - coalesce(SAD."TIEN_CHIET_KHAU_QUY_DOI",0)) AS "SO_TIEN_QUY_DOI"
		FROM	sale_ex_giam_gia_hang_ban SA
				INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban SAD ON SAD."GIAM_GIA_HANG_BAN_ID" = SA.id
				INNER JOIN (
							SELECT*FROM danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN" = '331'
									 ) TA ON SAD."TK_CO_ID" = TA.id
		WHERE
				SA."currency_id" = %(currency_id)s
-- 				AND SA."CHI_NHANH_ID" = (chi_nhanh_id)
				AND SAD."GIAM_GIA_HANG_BAN_ID" IS NOT NULL
				AND (SA."DOI_TUONG_ID" = 594 OR 594 IS NULL)
		GROUP BY SA.id, SA."DOI_TUONG_ID",TA."SO_TAI_KHOAN"
				,SA."NGAY_CHUNG_TU"
				,SA."SO_CHUNG_TU"





                                      ) GL ON cast(GL."ID_CHUNG_TU" AS INTEGER) = cast(OPNTemp."ID_CHUNG_TU" AS INTEGER)
                                                              AND GL."DOI_TUONG_ID" = OPNTemp."DOI_TUONG_ID"
                                                              AND GL."SO_TAI_KHOAN" = OPNTemp."SO_TAI_KHOAN"
                                                              AND ( OPNTemp."SO_HOA_DON_CHI_TIET" = '0'
                                                              OR ( OPNTemp."SO_HOA_DON_CHI_TIET" = '1'
                                                              AND coalesce(GL."SO_CHUNG_TU",'') = coalesce(OPNTemp."SO_CHUNG_TU",'')
                                                              AND coalesce(GL."NGAY_CHUNG_TU",'2019-02-28') = coalesce(OPNTemp."NGAY_CHUNG_TU",'2019-02-28')
                                                              )
                                                              )
					                                                    AND GL."SO_CHUNG_TU" = OPNTemp."SO_CHUNG_TU"
                  GROUP BY  OPNTemp."ID_CHUNG_TU" ,
                            OPNTemp."LOAI_CHUNG_TU" ,
                            OPNTemp."LOAI_CHUNG_TU" ,
                            OPNTemp."NGAY_CHUNG_TU" ,
                            OPNTemp."NGAY_HACH_TOAN" ,
                            OPNTemp."SO_CHUNG_TU" ,
                            OPNTemp."SO_HOA_DON" ,
                            OPNTemp."DIEN_GIAI" ,
                            OPNTemp."TY_GIA" ,
                            OPNTemp."SO_TIEN" ,
                            OPNTemp."SO_TIEN_QUY_DOI" ,
                            OPNTemp."SO_TIEN_THU" ,
                            OPNTemp."SO_TIEN_THU_QUY_DOI" ,
                            OPNTemp."DOI_TUONG_ID" ,
                            OPNTemp."SO_TAI_KHOAN" ,
                            OPNTemp."NHAN_VIEN_ID"--NVTOAN modify 14/04/2017 thực hiện CR 34929
                  HAVING    OPNTemp."SO_TIEN_THU" - coalesce(SUM(GL."SO_TIEN"),0) > 0


                ) AS AL
                LEFT JOIN (
				 -- Lấy danh sách chứng từ trả lại giảm giá chọn trực tiếp
                            SELECT  "CHUNG_TU_TRA_LAI_HANG_MUA_ID" AS "ID_CHUNG_TU"
                            FROM    purchase_ex_tra_lai_hang_mua_chi_tiet
                            WHERE   "CHUNG_TU_MUA_HANG" IS NOT NULL
                            UNION
                            SELECT  "GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID" AS "ID_CHUNG_TU"
                            FROM    purchase_ex_giam_gia_hang_mua_chi_tiet
                            WHERE   "CHUNG_TU_MUA_HANG" IS NOT NULL
                          ) SR ON AL."ID_CHUNG_TU" = SR."ID_CHUNG_TU"
                LEFT JOIN (
                            SELECT  CASE WHEN '15' = '15'
                                         THEN coalesce(GV."TY_GIA",1)
                                         ELSE coalesce(GV."TY_GIA", 1)
                                    END AS "TY_GIA" /* NBHIEU 12/05/2016 (bug 102978) Lấy tỷ giá đánh giá lại dưới chi tiết nếu là quyết dịnh 15*/ ,
                                    GVD."ID_CHUNG_TU_ID" AS "ID_CHUNG_TU",
                                    ROW_NUMBER() OVER ( PARTITION BY GVD."ID_CHUNG_TU_ID" ORDER BY GVD."ID_CHUNG_TU_ID", GV."NGAY_HACH_TOAN" DESC ) AS RowNumber
                            FROM    account_ex_chung_tu_nghiep_vu_khac GV
                                    INNER JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan GVD ON GVD."ID_CHUNG_TU_ID" = GV.id
                            WHERE
--                                     GV."CHI_NHANH_ID" = (chi_nhanh_id)
--                                     AND
                                        GV."currency_id" = %(currency_id)s
                                    AND GVD."TK_CONG_NO_ID" = (SELECT id FROM danh_muc_he_thong_tai_khoan WHERE "SO_TAI_KHOAN" = '331')
                                    AND GVD."DOI_TUONG_ID" = 594
                                    AND GV."state" = 'da_ghi_so'

                          ) AS GV ON AL."ID_CHUNG_TU" = GV."ID_CHUNG_TU"
                                     AND GV.RowNumber = 1
                LEFT JOIN res_partner E ON AL."NHAN_VIEN_ID" = E.id --NVTOAN modify 14/04/2017 thực hiện CR 34929
        GROUP BY AL."ID_CHUNG_TU" ,
                AL."LOAI_CHUNG_TU" ,
                AL."LOAI_CHUNG_TU" ,
                AL."NGAY_CHUNG_TU" ,
                AL."NGAY_HACH_TOAN" ,
                AL."SO_CHUNG_TU" ,
                AL."SO_HOA_DON" ,
                AL."DIEN_GIAI" ,
                AL."TY_GIA" ,
                coalesce(GV."TY_GIA", 0) ,
                AL."DOI_TUONG_ID" ,
                AL."NHAN_VIEN_ID" ,--NVTOAN modify 14/04/2017 thực hiện CR 34929
                E."MA_DOI_TUONG" , --nvtoan Modify 22/04/2017: Sửa lỗi 96455
                E.name
        HAVING  SUM(AL."SO_TIEN_THU") > 0
        ORDER BY AL."NGAY_CHUNG_TU" ,--DATRUONG 25.08.2015 Chỉnh lại sort với chế độ tăng dần ngày chứng từ
                AL."SO_CHUNG_TU" ,
                coalesce(AL."SO_HOA_DON", '')

        

        """  
        cr = self.env.cr

        cr.execute(query, params)
        for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
            record.append({
                'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU', ''),
                'SO_CHUNG_TU': line.get('SO_CHUNG_TU', ''),
                'DIEN_GIAI': line.get('DIEN_GIAI', ''),
                'NHAN_VIEN_ID': line.get('NHAN_VIEN_ID', ''),
                'TEN_NHAN_VIEN': line.get('TEN_NHAN_VIEN', ''),
                'SO_TIEN': line.get('SO_TIEN', ''),
                'SO_TIEN_DOI_TRU': line.get('SO_TIEN_DOI_TRU', ''),
                'LOAI_CHUNG_TU': line.get('LOAI_CHUNG_TU', ''),
            })
        
        return record

    