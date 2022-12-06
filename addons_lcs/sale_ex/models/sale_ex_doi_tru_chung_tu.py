# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
import json
import ast

class SALE_EX_DOI_TRU_CHUNG_TU(models.Model):
    _name = 'sale.ex.doi.tru.chung.tu'
    _description = ''
    _auto = False
    KHACH_HANG_ID = fields.Many2one('res.partner', string='Khách hàng', help='Khách hàng')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Nhà cung cấp', help='Nhà cung cấp')
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    TK_XU_LY_CL_LAI_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK xử lý CL lãi', help='Tài khoản xử lý chênh lệch lãi')
    TK_XU_LY_CL_LO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK xử lý CL lỗ', help='Tài khoản xử lý chênh lệch lỗ')
    TAI_KHOAN_PHAI_THU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản phải thu', help='Tài khoản phải thu')
    NGAY_DOI_TRU = fields.Date(string='Ngày đối trừ', help='Ngày đối trừ',default=fields.Datetime.now)
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    IS_TY_GIA = fields.Boolean(string='Loại tiền', help='Loại tiền',default=True)
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu', compute='doi_tru_cong_no')
    THAM_CHIEU2 = fields.Char(string='Tham chiếu', help='Tham chiếu', compute='doi_tru_chung_tu')
    LAY_DU_LIEU_JSON = fields.Text()
    DOI_TRU_JSON = fields.Text()
    LOAI_DOI_TRU = fields.Selection([('1', 'Đối trừ chứng từ'), ('2', 'đối trừ chứng từ nhiều đối tượng')], string='Trạng thái', default='1')
    LOAI_CHUNG_TU_DOI_TRU = fields.Selection([('BAN_HANG', 'Đối trừ chứng từ bán hàng'), ('MUA_HANG', 'Đối trừ chứng từ mua hàng')], string='Loại đối trừ chứng từ')

    TONG_SO_CHUA_DOI_TRU_TT = fields.Float(string='Tổng số chưa đối trừ thanh toán', help='Tổng số chưa đối trừ thanh toán')
    TONG_SO_DOI_TRU_THANH_TOAN = fields.Float(string='Tổng số đối trừ thanh toán', help='Tổng số đối trừ thanh toán')
    TONG_SO_CHUA_DOI_TRU_CN = fields.Float(string='Tổng số chưa đối trừ công nợ', help='Tổng số chưa đối trừ công nợ')
    TONG_SO_DOI_TRU_CONG_NO = fields.Float(string='Tổng số đối trừ công nợ', help='Tổng số đối trừ công nợ')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    DOI_TRU_CHUNG_TU_NHIEU_DOI_TUONG_ID = fields.Many2one('sale.ex.doi.tru.chung.tu.nhieu.doi.tuong', string='Đối trừ chứng từ nhiều đối tượng', help='Đối trừ chứng từ nhiều đối tượng')
    XEM_CHI_TIET = fields.Char()

    SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_IDS = fields.One2many('sale.ex.doi.tru.chung.tu.chi.tiet.thanh.toan', 'DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_ID', string='Đối trừ chứng từ chi tiết thanh toán')
    SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_IDS = fields.One2many('sale.ex.doi.tru.chung.tu.chi.tiet.cong.no', 'DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_ID', string='Đối trừ chứng từ chi tiết công nợ')

    @api.model
    def default_get(self, fields):
        rec = super(SALE_EX_DOI_TRU_CHUNG_TU, self).default_get(fields)
        rec['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')],limit=1).id
        tai_khoan_phai_thu_ban_hang = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','131')],limit=1)
        tai_khoan_phai_thu_mua_hang = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','331')],limit=1)
        if self.get_context('LOAI_CHUNG_TU_DOI_TRU') == 'BAN_HANG':
            if tai_khoan_phai_thu_ban_hang:
                rec['TAI_KHOAN_PHAI_THU_ID'] = tai_khoan_phai_thu_ban_hang.id
        elif self.get_context('LOAI_CHUNG_TU_DOI_TRU') == 'MUA_HANG':
            if tai_khoan_phai_thu_mua_hang:
                rec['TAI_KHOAN_PHAI_THU_ID'] = tai_khoan_phai_thu_mua_hang.id
        rec['TK_XU_LY_CL_LAI_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','515')],limit=1).id
        rec['TK_XU_LY_CL_LO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','635')],limit=1).id
        # rec['LOAI_DOI_TRU'] = '1'
        
        return rec

    @api.onchange('currency_id')
    def update_loai_tien(self):
        if self.currency_id.MA_LOAI_TIEN == 'VND':
            self.IS_TY_GIA = False
        else:
            self.IS_TY_GIA =True



    @api.onchange('LAY_DU_LIEU_JSON')
    def _onchange_LAY_DU_LIEU_JSON(self):
        if self.LAY_DU_LIEU_JSON:
            if self.DOI_TUONG_ID:
                param = ast.literal_eval(self.LAY_DU_LIEU_JSON)
                # param = {'NGAY' : '2019-04-04','DOI_TUONG_ID' : 594,'currency_id' : 24}
                if param:
                    self.them_dong_du_lieu(param.get('NGAY'),param.get('DOI_TUONG_ID'),param.get('currency_id'))
            else:
                raise ValidationError("<Khách hàng> không được bỏ trống")

    def lay_du_lieu_doi_tru(self, args):
        new_line_chung_tu_thanh_toan = [[5]]
        new_line_chung_tu_cong_no = [[5]]
        if args.get('LOAI_CHUNG_TU_DOI_TRU'):
            if args.get('LOAI_CHUNG_TU_DOI_TRU') == 'BAN_HANG':
                ct_thanh_toan = self.lay_chung_tu_thanh_toan(args.get('NGAY'),args.get('DOI_TUONG_ID'),args.get('currency_id'))
                ct_cong_no = self.lay_chung_tu_cong_no(args.get('NGAY'),args.get('DOI_TUONG_ID'),args.get('currency_id'))
                for ct in ct_thanh_toan:
                    ten_loai_chung_tu = self.env['danh.muc.reftype'].search([('REFTYPE', '=', ct.get('LOAI_CHUNG_TU'))], limit=1)
                    new_line_chung_tu_thanh_toan += [(0,0,{
                        'NGAY_CHUNG_TU': ct.get('NGAY_CHUNG_TU'),
                        'SO_CHUNG_TU' : ct.get('SO_CHUNG_TU'),
                        'DIEN_GIAI' : ct.get('DIEN_GIAI'),
                        'NHAN_VIEN_ID' : ct.get('NHAN_VIEN_ID'),
                        'TEN_NHAN_VIEN' : ct.get('TEN_NHAN_VIEN'),
                        'SO_TIEN' : ct.get('SO_TIEN'),
                        'SO_TIEN_QUY_DOI' : ct.get('SO_TIEN_QUY_DOI'),
                        'SO_CHUA_DOI_TRU' : ct.get('SO_TIEN_THU_QUY_DOI'),
                        'SO_CHUA_DOI_TRU_QUY_DOI' : ct.get('SO_TIEN_THU_QUY_DOI_QUY_DOI'),
                        'SO_TIEN_DOI_TRU' : ct.get('SO_TIEN_DOI_TRU'),
                        'TEN_LOAI_CHUNG_TU' : ten_loai_chung_tu.REFTYPENAME,
                        'LOAI_CHUNG_TU' : ct.get('LOAI_CHUNG_TU'),
                        'ID_CHUNG_TU_THANH_TOAN' : ct.get('ID_CHUNG_TU'),
                        'MODEL_CHUNG_TU_THANH_TOAN' : ct.get('MODEL_CHUNG_TU'),
                        'NGAY_HACH_TOAN' : ct.get('NGAY_HACH_TOAN'),
                        'NGAY_HOA_DON' : ct.get('NGAY_HOA_DON'),
                        'TY_GIA_DANH_GIA_LAI' : ct.get('TY_GIA_DANH_GIA_LAI'),
                    })]
                for line in ct_cong_no:
                    ten_loai_ct_cong_no = self.env['danh.muc.reftype'].search([('REFTYPE', '=', line.get('LOAI_CHUNG_TU'))], limit=1)
                    new_line_chung_tu_cong_no += [(0,0,{
                        'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU'),
                        'SO_CHUNG_TU' : line.get('SO_CHUNG_TU'),
                        'DIEN_GIAI' : line.get('DIEN_GIAI'),
                        'NHAN_VIEN_ID' : line.get('NHAN_VIEN_ID'),
                        'TEN_NHAN_VIEN' : line.get('TEN_NHAN_VIEN'),
                        'SO_TIEN' : line.get('SO_TIEN'),
                        'SO_TIEN_QUY_DOI' : line.get('SO_TIEN_QUY_DOI'),
                        'SO_CON_NO' : line.get('SO_TIEN_CONG_NO'),
                        'SO_CON_NO_QUY_DOI' : line.get('SO_TIEN_CONG_NO_QUY_DOI'),
                        'SO_TIEN_DOI_TRU' : line.get('SO_TIEN_DOI_TRU'),
                        'TEN_LOAI_CHUNG_TU' : ten_loai_ct_cong_no.REFTYPENAME,
                        'LOAI_CHUNG_TU' : line.get('LOAI_CHUNG_TU'),
                        'ID_CHUNG_TU_CONG_NO' : line.get('ID_CHUNG_TU'),
                        'MODEL_CHUNG_TU_CONG_NO' : line.get('MODEL_CHUNG_TU'),
                        'NGAY_HACH_TOAN' : line.get('NGAY_HACH_TOAN'),
                        'NGAY_HOA_DON' : line.get('NGAY_HOA_DON'),
                        'TY_GIA_DANH_GIA_LAI' : line.get('TY_GIA_DANH_GIA_LAI'),
                    })]

            elif args.get('LOAI_CHUNG_TU_DOI_TRU') == 'MUA_HANG':
                mua_hang_ct_thanh_toan = self.mua_hang_chung_tu_thanh_toan(args.get('NGAY'),args.get('DOI_TUONG_ID'),args.get('currency_id'))
                mua_hang_ct_mua_hang = self.mua_hang_chung_tu_cong_no(args.get('NGAY'),args.get('DOI_TUONG_ID'),args.get('currency_id'))
                for ct_mua_hang in mua_hang_ct_thanh_toan:
                    ten_loai_chung_tu = self.env['danh.muc.reftype'].search([('REFTYPE', '=', ct_mua_hang.get('LOAI_CHUNG_TU'))], limit=1)
                    new_line_chung_tu_thanh_toan += [(0,0,{
                        'NGAY_CHUNG_TU': ct_mua_hang.get('NGAY_CHUNG_TU'),
                        'SO_CHUNG_TU' : ct_mua_hang.get('SO_CHUNG_TU'),
                        'DIEN_GIAI' : ct_mua_hang.get('DIEN_GIAI'),
                        'NHAN_VIEN_ID' : ct_mua_hang.get('NHAN_VIEN_ID'),
                        'TEN_NHAN_VIEN' : ct_mua_hang.get('TEN_NHAN_VIEN'),
                        'SO_TIEN' : ct_mua_hang.get('SO_TIEN'),
                        'SO_TIEN_QUY_DOI' : ct_mua_hang.get('SO_TIEN_QUY_DOI'),
                        'SO_CHUA_DOI_TRU' : ct_mua_hang.get('SO_TIEN_THU'),
                        'SO_CHUA_DOI_TRU_QUY_DOI' : ct_mua_hang.get('SO_TIEN_THU_QUY_DOI'),
                        'SO_TIEN_DOI_TRU' : ct_mua_hang.get('SO_TIEN_DOI_TRU'),
                        'TEN_LOAI_CHUNG_TU' : ten_loai_chung_tu.REFTYPENAME,
                        'LOAI_CHUNG_TU' : ct_mua_hang.get('LOAI_CHUNG_TU'),
                        'ID_CHUNG_TU_THANH_TOAN' : ct_mua_hang.get('ID_CHUNG_TU'),
                        'MODEL_CHUNG_TU_THANH_TOAN' : ct_mua_hang.get('MODEL_CHUNG_TU'),
                        'NGAY_HACH_TOAN' : ct_mua_hang.get('NGAY_HACH_TOAN'),
                        'NGAY_HOA_DON' : ct_mua_hang.get('NGAY_HOA_DON'),
                        'TY_GIA' : ct_mua_hang.get('TY_GIA'),
                        'TY_GIA_DANH_GIA_LAI' : ct_mua_hang.get('TY_GIA_DANH_GIA_LAI'),
                    })]

                for line_ct_cong_no in mua_hang_ct_mua_hang:
                    ten_loai_ct_cong_no = self.env['danh.muc.reftype'].search([('REFTYPE', '=', line_ct_cong_no.get('LOAI_CHUNG_TU'))], limit=1)
                    new_line_chung_tu_cong_no += [(0,0,{
                        'NGAY_CHUNG_TU': line_ct_cong_no.get('NGAY_CHUNG_TU'),
                        'SO_CHUNG_TU' : line_ct_cong_no.get('SO_CHUNG_TU'),
                        'SO_HOA_DON' : line_ct_cong_no.get('SO_HOA_DON'),
                        'DIEN_GIAI' : line_ct_cong_no.get('DIEN_GIAI'),
                        'NHAN_VIEN_ID' : line_ct_cong_no.get('NHAN_VIEN_ID'),
                        'TEN_NHAN_VIEN' : line_ct_cong_no.get('TEN_NHAN_VIEN'),
                        'SO_TIEN' : line_ct_cong_no.get('SO_TIEN'),
                        'SO_TIEN_QUY_DOI' : line_ct_cong_no.get('SO_TIEN_QUY_DOI'),
                        'SO_CON_NO' : line_ct_cong_no.get('SO_TIEN_CONG_NO'),
                        'SO_CON_NO_QUY_DOI' : line_ct_cong_no.get('SO_TIEN_CONG_NO_QUY_DOI'),
                        'SO_TIEN_DOI_TRU' : line_ct_cong_no.get('SO_TIEN_DOI_TRU'),
                        'TEN_LOAI_CHUNG_TU' : ten_loai_ct_cong_no.REFTYPENAME,
                        'LOAI_CHUNG_TU' : line_ct_cong_no.get('LOAI_CHUNG_TU'),
                        'ID_CHUNG_TU_CONG_NO' : line_ct_cong_no.get('ID_CHUNG_TU'),
                        'MODEL_CHUNG_TU_CONG_NO' : line_ct_cong_no.get('MODEL_CHUNG_TU'),
                        'TY_GIA' : line_ct_cong_no.get('TY_GIA'),
                        'NGAY_HACH_TOAN' : line_ct_cong_no.get('NGAY_HACH_TOAN'),
                        'NGAY_HOA_DON' : line_ct_cong_no.get('NGAY_HOA_DON'),
                        'TY_GIA_DANH_GIA_LAI' : line_ct_cong_no.get('TY_GIA_DANH_GIA_LAI'),
                    })]
                
        return {'SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_IDS' : new_line_chung_tu_thanh_toan,
				'SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_IDS' : new_line_chung_tu_cong_no,
			}
            

    def lay_chung_tu_thanh_toan(self,ngay,doi_tuong,loai_tien):
        record = []
        params = {
            'DOI_TUONG_ID': doi_tuong,
            'currency_id' : loai_tien,
            'DEN_NGAY' : ngay,
			'CHI_NHANH_ID' : self.get_chi_nhanh()
            }

        query = """   

        DO LANGUAGE plpgsql $$
			DECLARE

			doi_tuong_id     INTEGER := %(DOI_TUONG_ID)s;
			den_ngay         DATE := %(DEN_NGAY)s;
			loai_tien_id     INTEGER := %(currency_id)s;
			chi_nhanh_id     INTEGER := %(CHI_NHANH_ID)s;


			BEGIN

            DROP TABLE IF EXISTS TMP_TABLE_1;
            CREATE TEMP TABLE TMP_TABLE_1
                AS
                SELECT
                    OPN.id                                AS "ID_CHUNG_TU",
                    'account.ex.so.du.tai.khoan.chi.tiet' AS "MODEL_CHUNG_TU",
                    OPN."LOAI_CHUNG_TU",
                    (CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL AND OPI."SO_THU_TRUOC" <> 0
                    THEN OPI."NGAY_HOA_DON"
                    ELSE OPN."NGAY_HACH_TOAN"
                    END)                                    "NGAY_CHUNG_TU",
                    OPN."NGAY_HACH_TOAN",
                    (CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL AND OPI."SO_THU_TRUOC" <> 0
                    THEN coalesce(OPI."SO_HOA_DON", '')
                    ELSE 'OPN'
                    END)                                 AS "SO_CHUNG_TU",
                    coalesce(OPI."SO_HOA_DON", '')        AS "SO_HOA_DON",
                    ''                                    AS "DIEN_GIAI",
                    (CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                    THEN coalesce(OPI."TY_GIA", 1)
                    ELSE coalesce(OPN."TY_GIA", 1)
                    END)                                 AS "TY_GIA",
                    SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                    THEN coalesce(OPI."SO_THU_TRUOC_NGUYEN_TE", 0)
                        ELSE coalesce(OPN."DU_NO_NGUYEN_TE", 0) - coalesce(OPN."DU_CO_NGUYEN_TE", 0)
                        END)                              AS "SO_TIEN",
                    SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                    THEN coalesce(OPI."SO_THU_TRUOC", 0)
                        ELSE coalesce(OPN."DU_CO", 0) - coalesce(OPN."DU_NO", 0)
                        END)                              AS "SO_TIEN_QUY_DOI",
                    SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                    THEN coalesce(OPI."SO_THU_TRUOC_NGUYEN_TE", 0)
                        ELSE coalesce(OPN."DU_CO", 0) - coalesce(OPN."DU_CO_NGUYEN_TE", 0)
                        END)                              AS "SO_TIEN_THU",
                    SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                    THEN coalesce(OPI."SO_THU_TRUOC", 0)
                        ELSE coalesce(OPN."DU_CO", 0) - coalesce(OPN."DU_NO", 0)
                        END)                              AS "SO_TIEN_THU_QUY_DOI",
                    doi_tuong_id                          AS "DOI_TUONG_ID",
                    OPN."SO_TAI_KHOAN",
                    1                                     AS "SO_HOA_DON_CHI_TIET",
                    OPID2."NHAN_VIEN_ID" --NVTOAN modify 14/04/2017 thực hiện CR 34929
                FROM account_ex_so_du_tai_khoan_chi_tiet OPN
                    INNER JOIN danh_muc_reftype RT ON cast(RT."REFTYPE" AS VARCHAR(50)) = OPN."LOAI_CHUNG_TU"
                    LEFT JOIN account_ex_sdtkct_theo_hoa_don OPI ON OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" = OPN.id
                    LEFT JOIN (
                                SELECT
                                OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID",
                                coalesce(OAEDI."NGAY_HOA_DON", NOW())      AS "NGAY_HOA_DON",
                                coalesce(OAEDI."SO_HOA_DON", '')           AS "SO_HOA_DON",
                                coalesce(OAEDI."TY_GIA", 0)                AS "TY_GIA",
                                OAEDI."NHAN_VIEN_ID",
                                ROW_NUMBER()
                                OVER (
                                    PARTITION BY OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID",
                                    coalesce(OAEDI."NGAY_HOA_DON", NOW()),
                                    coalesce(OAEDI."SO_HOA_DON", ''),
                                    coalesce(OAEDI."TY_GIA", 0)
                                    ORDER BY OAEDI."THU_TU_TRONG_CHUNG_TU" ) AS RowNumber
                                FROM account_ex_sdtkct_theo_hoa_don AS OAEDI
                                WHERE OAEDI."NHAN_VIEN_ID" IS NOT NULL
                            ) AS OPID2 ON OPN.id = OPID2."SO_DU_TAI_KHOAN_CHI_TIET_ID"
                                            AND OPID2.RowNumber = 1
                                            AND coalesce(OPI."SO_HOA_DON", '') = coalesce(OPID2."SO_HOA_DON", '')
                                            AND coalesce(OPI."NGAY_HOA_DON", NOW()) = coalesce(OPID2."NGAY_HOA_DON", NOW())
                                            AND coalesce(OPI."TY_GIA", 0) = coalesce(OPID2."TY_GIA", 0)
                --NVTOAN add 14/04/2017 thực hiện CR 34929
                WHERE
                    (OPN."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id ISNULL)
                    AND OPN."currency_id" = loai_tien_id
                    AND OPN."TK_ID" = (SELECT id
                                    FROM danh_muc_he_thong_tai_khoan
                                    WHERE "SO_TAI_KHOAN" = '131')
                    AND OPN."CHI_NHANH_ID" = (chi_nhanh_id)
                    AND OPN."NGAY_HACH_TOAN" <= den_ngay

                GROUP BY OPN.id,
                    (CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                            AND OPI."SO_THU_TRUOC" <> 0
                    THEN OPI."NGAY_HOA_DON"
                    ELSE OPN."NGAY_HACH_TOAN"
                    END),
                    (CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                    THEN coalesce(OPI."TY_GIA", 1)
                    ELSE coalesce(OPN."TY_GIA", 1)
                    END),
                    OPN."LOAI_CHUNG_TU",
                    RT."REFTYPENAME",
                    OPN."NGAY_HACH_TOAN",
                    (CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                            AND OPI."SO_THU_TRUOC" <> 0
                    THEN coalesce(OPI."SO_HOA_DON", '')
                    ELSE 'OPN'
                    END),
                    OPI."NGAY_HOA_DON",
                    coalesce(OPI."SO_HOA_DON", ''),
                    coalesce(OPI."TY_GIA", 1),
                    coalesce(OPN."TY_GIA", 1),
                    OPN."SO_TAI_KHOAN",
                    OPID2."NHAN_VIEN_ID" --NVTOAN modify 14/04/2017 thực hiện CR 34929
                HAVING SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                    THEN coalesce(OPI."SO_THU_TRUOC", 0)
                            ELSE coalesce(OPN."DU_CO_NGUYEN_TE", 0) - coalesce(OPN."DU_NO_NGUYEN_TE", 0)
                            END) > 0


                UNION ALL


                SELECT
                    AL."ID_CHUNG_TU",
                    AL."MODEL_CHUNG_TU",
                    cast(AL."LOAI_CHUNG_TU" AS VARCHAR(50)),
                    AL."NGAY_CHUNG_TU",
                    AL."NGAY_HACH_TOAN",
                    AL."SO_CHUNG_TU",
                    coalesce(AL."SO_HOA_DON", '')             AS "SO_HOA_DON",
                    coalesce(AL."DIEN_GIAI_CHUNG", '')        AS "DIEN_GIAI",
                    coalesce(AL."TY_GIA", 1)                  AS "TY_GIA",
                    SUM(coalesce(AL."GHI_CO_NGUYEN_TE", 0)
                        - coalesce(AL."GHI_NO_NGUYEN_TE", 0)) AS "SO_TIEN",
                    SUM(coalesce(AL."GHI_CO", 0)
                        - coalesce(AL."GHI_NO", 0))           AS "SO_TIEN_QUY_DOI",
                    SUM(coalesce(AL."GHI_CO_NGUYEN_TE", 0)
                        - coalesce(AL."GHI_NO_NGUYEN_TE", 0)) AS "SO_TIEN_THU",
                    SUM(coalesce(AL."GHI_CO", 0)
                        - coalesce(AL."GHI_NO", 0))           AS "SO_TIEN_THU_QUY_DOI",
                    doi_tuong_id                              AS "DOI_TUONG_ID",
                    AL."MA_TK"                                AS "SO_TAI_KHOAN",
                    0                                         AS "SO_HOA_DON_CHI_TIET",
                    CASE WHEN GVDT."ID_CHUNG_TU" IS NOT NULL
                    THEN GVDT."NHAN_VIEN_ID"
                    ELSE AL."NHAN_VIEN_ID"
                    END                                       AS "NHAN_VIEN_ID" --NVTOAN modify 14/04/2017 thực hiện CR 34929
                FROM so_cong_no_chi_tiet AS AL
                    LEFT JOIN (/*Lấy Nhân viên trên chứng từ nghiệp vụ khác*/
                                SELECT
                                AOL."ID_CHUNG_TU",
                                AOL."DOI_TUONG_ID",
                                AOL."MA_TK",
                                AOL."NHAN_VIEN_ID",
                                ROW_NUMBER()
                                OVER (
                                    PARTITION BY AOL."ID_CHUNG_TU",
                                    AOL."DOI_TUONG_ID",
                                    AOL."MA_TK"
                                    ORDER BY AOL."THU_TU_TRONG_CHUNG_TU" ) AS RowNumber
                                FROM so_cong_no_chi_tiet AS AOL
                                WHERE AOL."LOAI_CHUNG_TU" IN ('4010', '4011', '4012', '4014', '4015', '4018', '4020', '4030')
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
                    (AL."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id ISNULL)
                    AND AL."currency_id" = loai_tien_id
                    AND AL."TK_ID" = (SELECT id
                                    FROM danh_muc_he_thong_tai_khoan
                                    WHERE "SO_TAI_KHOAN" = '131')
                    AND AL."CHI_NHANH_ID" = chi_nhanh_id
                    --Không lấy các chứng từ Phiếu thu tiền khách hàng, Phiếu thu tiền khách hàng hàng loạt, Phiếu chi trả tiền nhà cung cấp, Phiếu thu tiền gửi khách hàng, Phiếu thu tiền gửi khách hàng hàng loạt, Trả tiền nhà cung cấp bằng Ủy nhiệm chi, Séc tiền mặt trả tiền nhà cung cấp, Séc chuyển khoản trả tiền nhà cung cấp, Chứng từ xử lý chênh lệch tỷ giá, Chứng từ bù trừ công nợ, Xử lý chênh lệch tỷ giá từ đánh giá lại tài khoản ngoại tệ, Xử lý chênh lệch tỷ giá từ tính tỷ giá xuất quỹ
                    AND AL."LOAI_CHUNG_TU" NOT IN
                        (1011, 1012, 1021, 1502, 1503, 1511, 1521, 1531, 4013, 4016, 4017, 611, 612, 613, 614, 615, 616, 630)
                    AND AL."NGAY_HACH_TOAN" <= den_ngay

                GROUP BY AL."ID_CHUNG_TU",
                    AL."MODEL_CHUNG_TU",
                    AL."LOAI_CHUNG_TU",
                    --           AL."LOAI_CHUNG_TU" ,
                    AL."NGAY_CHUNG_TU",
                    AL."NGAY_HACH_TOAN",
                    AL."SO_CHUNG_TU",
                    coalesce(AL."SO_HOA_DON", ''),
                    coalesce(AL."DIEN_GIAI_CHUNG", ''),
                    coalesce(AL."TY_GIA", 1),
                    AL."MA_TK",
                    CASE WHEN GVDT."ID_CHUNG_TU" IS NOT NULL
                    THEN GVDT."NHAN_VIEN_ID"
                    ELSE AL."NHAN_VIEN_ID"
                    END --NVTOAN modify 14/04/2017 thực hiện CR 34929
                HAVING SUM(coalesce(AL."GHI_CO_NGUYEN_TE", 0)
                            - coalesce(AL."GHI_NO_NGUYEN_TE", 0)) > 0;

            DROP TABLE IF EXISTS TMP_TABLE_2;
            CREATE TEMP TABLE TMP_TABLE_2
                AS
                SELECT
                    OPNTemp."ID_CHUNG_TU",
                    OPNTemp."MODEL_CHUNG_TU",
                    OPNTemp."LOAI_CHUNG_TU",
                    --                             OPNTemp."LOAI_CHUNG_TU" ,
                    OPNTemp."NGAY_CHUNG_TU",
                    OPNTemp."NGAY_HACH_TOAN",
                    -- nmtruong: 11/5/2016 sửa bug 101936 thay refdate = posteddate để ghi xuống bảng đối trừ đúng ngày hạch toán
                    OPNTemp."SO_CHUNG_TU",
                    OPNTemp."SO_HOA_DON",
                    OPNTemp."DIEN_GIAI",
                    OPNTemp."TY_GIA",
                    OPNTemp."SO_TIEN",
                    OPNTemp."SO_TIEN_QUY_DOI",
                    (OPNTemp."SO_TIEN_THU" - coalesce(SUM(GL."SO_TIEN"), 0))               AS "SO_TIEN_THU",
                    OPNTemp."SO_TIEN_THU_QUY_DOI" - coalesce(SUM(GL."SO_TIEN_QUY_DOI"), 0) AS "SO_TIEN_THU_QUY_DOI",
                    OPNTemp."DOI_TUONG_ID",
                    OPNTemp."SO_TAI_KHOAN",
                    OPNTemp."NHAN_VIEN_ID" --NVTOAN modify 14/04/2017 thực hiện CR 34929
                FROM TMP_TABLE_1 AS OPNTemp
                    LEFT JOIN (SELECT *
                            FROM FUNCTION_DOI_TRU_CHUNG_TU_BAN_HANG_THANH_TOAN('131', loai_tien_id, chi_nhanh_id,
                                                                                doi_tuong_id)) GL
                    ON cast(GL."ID_CHUNG_TU" AS INTEGER) = cast(OPNTemp."ID_CHUNG_TU" AS INTEGER)
                        AND GL."MODEL_CHUNG_TU" = OPNTemp."MODEL_CHUNG_TU"
                        AND GL."DOI_TUONG_ID" = OPNTemp."DOI_TUONG_ID"
                        AND GL."SO_TAI_KHOAN" = OPNTemp."SO_TAI_KHOAN"
                        AND (OPNTemp."SO_HOA_DON_CHI_TIET" = '0'
                            OR (OPNTemp."SO_HOA_DON_CHI_TIET" = '1'
                                AND coalesce(GL."SO_CHUNG_TU", '') = coalesce(OPNTemp."SO_CHUNG_TU", '')
                                AND coalesce(GL."NGAY_CHUNG_TU", den_ngay) = coalesce(OPNTemp."NGAY_CHUNG_TU", den_ngay)
                            )
                        )
                        AND coalesce(GL."SO_CHUNG_TU", '') = coalesce(OPNTemp."SO_CHUNG_TU", '')
                GROUP BY OPNTemp."ID_CHUNG_TU",
                    OPNTemp."MODEL_CHUNG_TU",
                    OPNTemp."LOAI_CHUNG_TU",
                    OPNTemp."LOAI_CHUNG_TU",
                    OPNTemp."NGAY_CHUNG_TU",
                    OPNTemp."NGAY_HACH_TOAN",
                    OPNTemp."SO_CHUNG_TU",
                    OPNTemp."SO_HOA_DON",
                    OPNTemp."DIEN_GIAI",
                    OPNTemp."TY_GIA",
                    OPNTemp."SO_TIEN",
                    OPNTemp."SO_TIEN_QUY_DOI",
                    OPNTemp."SO_TIEN_THU",
                    OPNTemp."SO_TIEN_THU_QUY_DOI",
                    OPNTemp."DOI_TUONG_ID",
                    OPNTemp."SO_TAI_KHOAN",
                    OPNTemp."NHAN_VIEN_ID" --NVTOAN modify 14/04/2017 thực hiện CR 34929
                HAVING OPNTemp."SO_TIEN_THU" - coalesce(SUM(GL."SO_TIEN"), 0) > 0;
            DROP TABLE IF EXISTS TMP_KET_QUA1;
            CREATE TEMP TABLE TMP_KET_QUA1
                AS
                SELECT
                    AL."ID_CHUNG_TU",
                    Al."MODEL_CHUNG_TU",
                    AL."LOAI_CHUNG_TU",
                    --                AL."LOAI_CHUNG_TU" ,
                    AL."NGAY_CHUNG_TU",
                    AL."NGAY_HACH_TOAN",
                    AL."SO_CHUNG_TU",
                    AL."SO_HOA_DON",
                    AL."DIEN_GIAI",
                    AL."TY_GIA",
                    coalesce(GV."TY_GIA",0) AS "TY_GIA_DANH_GIA_LAI",
                    round(cast(SUM(AL."SO_TIEN") AS NUMERIC),0)             AS "SO_TIEN",
                    SUM(AL."SO_TIEN_QUY_DOI")     AS "SO_TIEN_QUY_DOI",
                    round(cast(SUM(AL."SO_TIEN_THU") AS NUMERIC),0)         AS "SO_TIEN_THU",
                    SUM(AL."SO_TIEN_THU_QUY_DOI") AS "SO_TIEN_THU_QUY_DOI",
                    0                             AS "SO_TIEN_DOI_TRU",
                    0                             AS "SO_TIEN_DOI_TRU_QUY_DOI",
                    doi_tuong_id                  AS "DOI_TUONG_ID",
                    AL."NHAN_VIEN_ID",
                    --NVTOAN modify 14/04/2017 thực hiện CR 34929
                    E."MA"              AS "MA_NHAN_VIEN",
                    --nvtoan Modify 22/04/2017: Sửa lỗi 96455
                    E."HO_VA_TEN"                 AS "TEN_NHAN_VIEN"
                FROM TMP_TABLE_2 AS AL
                    LEFT JOIN (
                                -- Lấy danh sách chứng từ trả lại giảm giá chọn trực tiếp
                                SELECT "TRA_LAI_HANG_BAN_ID" AS "ID_CHUNG_TU"
                                FROM sale_ex_tra_lai_hang_ban_chi_tiet
                                WHERE "CHUNG_TU_BAN_HANG_ID" IS NOT NULL
                                UNION
                                SELECT "GIAM_GIA_HANG_BAN_ID" AS "ID_CHUNG_TU"
                                FROM sale_ex_chi_tiet_giam_gia_hang_ban
                                WHERE "CHUNG_TU_BAN_HANG_ID" IS NOT NULL
                            ) SR ON AL."ID_CHUNG_TU" = SR."ID_CHUNG_TU"
                    LEFT JOIN (
                                SELECT
                                CASE WHEN '15' = '15'
                                    THEN coalesce(GV."TY_GIA", 1)
                                ELSE coalesce(GV."TY_GIA", 1)
                                END                                                          AS "TY_GIA"
                                /* NBHIEU 12/05/2016 (bug 102978) Lấy tỷ giá đánh giá lại dưới chi tiết nếu là quyết dịnh 15*/,
                                GVD."ID_CHUNG_TU_GOC"                                        AS "ID_CHUNG_TU",
                                ROW_NUMBER()
                                OVER (
                                    PARTITION BY GVD."ID_CHUNG_TU_GOC"
                                    ORDER BY GVD."ID_CHUNG_TU_GOC", GV."NGAY_HACH_TOAN" DESC ) AS RowNumber
                                FROM account_ex_chung_tu_nghiep_vu_khac GV
                                INNER JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan GVD
                                    ON GVD."ID_CHUNG_TU_GOC" = GV.id
                                WHERE
                                --                                     GV."CHI_NHANH_ID" = (chi_nhanh_id)
                                --                                     AND
                                GV.currency_id = loai_tien_id
                                AND GVD."TK_CONG_NO_ID" = (SELECT id
                                                            FROM danh_muc_he_thong_tai_khoan
                                                            WHERE "SO_TAI_KHOAN" = '131')
                                AND GVD."DOI_TUONG_ID" = doi_tuong_id
                                AND GV."state" = 'da_ghi_so'

                            ) AS GV ON AL."ID_CHUNG_TU" = GV."ID_CHUNG_TU"
                                        AND GV.RowNumber = 1
                    LEFT JOIN res_partner E ON AL."NHAN_VIEN_ID" = E.id --NVTOAN modify 14/04/2017 thực hiện CR 34929
                GROUP BY AL."ID_CHUNG_TU",
                    AL."MODEL_CHUNG_TU",
                    AL."LOAI_CHUNG_TU",
                    AL."LOAI_CHUNG_TU",
                    AL."NGAY_CHUNG_TU",
                    AL."NGAY_HACH_TOAN",
                    AL."SO_CHUNG_TU",
                    AL."SO_HOA_DON",
                    AL."DIEN_GIAI",
                    AL."TY_GIA",
                    coalesce(GV."TY_GIA", 0),
                    AL."DOI_TUONG_ID",
                    AL."NHAN_VIEN_ID", --NVTOAN modify 14/04/2017 thực hiện CR 34929
                    E."MA", --nvtoan Modify 22/04/2017: Sửa lỗi 96455
                    E."HO_VA_TEN",
                    coalesce(GV."TY_GIA",0)
                HAVING SUM(AL."SO_TIEN_THU") > 0
                ORDER BY AL."NGAY_CHUNG_TU", --DATRUONG 25.08.2015 Chỉnh lại sort với chế độ tăng dần ngày chứng từ
                    AL."SO_CHUNG_TU",
                    coalesce(AL."SO_HOA_DON", '');
            END $$;

            SELECT *
            FROM TMP_KET_QUA1;


        """  
        
        
        return self.execute(query, params)





    

    def lay_chung_tu_cong_no(self,ngay,doi_tuong,loai_tien):
        params = {
            'DOI_TUONG_ID': doi_tuong,
            'currency_id' : loai_tien,
            'DEN_NGAY' : ngay,
			'CHI_NHANH_ID' : self.get_chi_nhanh()
            }

        query = """   

        DO LANGUAGE plpgsql $$
			DECLARE

			doi_tuong_id  INTEGER := %(DOI_TUONG_ID)s;
			den_ngay      DATE := %(DEN_NGAY)s;
			loai_tien_id  INTEGER := %(currency_id)s;
			chi_nhanh_id  INTEGER := %(CHI_NHANH_ID)s;


			BEGIN

            DROP TABLE IF EXISTS TMP_TABLE_1;
            CREATE TEMP TABLE TMP_TABLE_1
                AS
                SELECT
                    OPN.id                                AS "ID_CHUNG_TU",
                    'account.ex.so.du.tai.khoan.chi.tiet' AS "MODEL_CHUNG_TU",
                    OPN."LOAI_CHUNG_TU",
                    RT."REFTYPENAME"                      AS "TEN_LOAI_CHUNG_TU",
                    (CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                    THEN OPI."NGAY_HOA_DON"
                    ELSE OPN."NGAY_HACH_TOAN"
                    END)                                    "NGAY_CHUNG_TU",
                    OPN."NGAY_HACH_TOAN",
                    'OPN'                                 AS "SO_CHUNG_TU",
                    OPI."NGAY_HOA_DON",
                    coalesce(OPI."SO_HOA_DON", '')        AS "SO_HOA_DON",
                    ''                                    AS "DIEN_GIAI",
                    (CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                    THEN coalesce(OPI."TY_GIA", 1)
                    ELSE coalesce(OPN."TY_GIA", 1)
                    END)                                 AS "TY_GIA",
                    SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                    THEN coalesce(OPI."GIA_TRI_HOA_DON_NGUYEN_TE", 0)
                        ELSE coalesce(OPN."DU_NO_NGUYEN_TE", 0) - coalesce(OPN."DU_CO_NGUYEN_TE", 0)
                        END)                              AS "TONG_TIEN",
                    SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                    THEN coalesce(OPI."GIA_TRI_HOA_DON", 0)
                        ELSE coalesce(OPN."DU_NO", 0) - coalesce(OPN."DU_CO", 0)
                        END)                              AS "TONG_TIEN_QUY_DOI",
                    SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                    THEN coalesce(OPI."SO_CON_PHAI_THU_NGUYEN_TE", 0)
                        ELSE coalesce(OPN."DU_NO_NGUYEN_TE", 0) - coalesce(OPN."DU_CO_NGUYEN_TE", 0)
                        END)                              AS "SO_TIEN",
                    SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                    THEN coalesce(OPI."SO_CON_PHAI_THU", 0)
                        ELSE coalesce(OPN."DU_NO", 0) - coalesce(OPN."DU_CO", 0)
                        END)                              AS "SO_TIEN_QUY_DOI",
                    1                                     AS "SO_HOA_DON_CHI_TIET",
                    OPID."HAN_THANH_TOAN",
                    OPID2."NHAN_VIEN_ID"
                FROM account_ex_so_du_tai_khoan_chi_tiet OPN
                    INNER JOIN danh_muc_reftype RT ON cast(RT."REFTYPE" AS VARCHAR(50)) = OPN."LOAI_CHUNG_TU"
                    LEFT JOIN account_ex_sdtkct_theo_hoa_don OPI ON OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" = OPN.id
                    LEFT JOIN (SELECT
                                OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID",
                                coalesce(OAEDI."NGAY_HOA_DON", NOW())      AS "NGAY_HOA_DON",
                                coalesce(OAEDI."SO_HOA_DON", '')           AS "SO_HOA_DON",
                                coalesce(OAEDI."TY_GIA", 0)                AS "TY_GIA",
                                OAEDI."NHAN_VIEN_ID",
                                ROW_NUMBER()
                                OVER (
                                PARTITION BY OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID",
                                    coalesce(OAEDI."NGAY_HOA_DON", NOW()),
                                    coalesce(OAEDI."SO_HOA_DON", ''),
                                    coalesce(OAEDI."TY_GIA", 0)
                                ORDER BY OAEDI."THU_TU_TRONG_CHUNG_TU" ) AS RowNumber
                            FROM account_ex_sdtkct_theo_hoa_don AS OAEDI
                            WHERE OAEDI."NHAN_VIEN_ID" IS NOT NULL
                            ) AS OPID2 ON OPN.id = OPID2."SO_DU_TAI_KHOAN_CHI_TIET_ID"
                                            AND OPID2.RowNumber = 1
                                            AND coalesce(OPI."SO_HOA_DON", '') = coalesce(OPID2."SO_HOA_DON", '')
                                            AND coalesce(OPI."NGAY_HOA_DON", NOW()) = coalesce(OPID2."NGAY_HOA_DON", NOW())
                                            AND coalesce(OPI."TY_GIA", 0) = coalesce(OPID2."TY_GIA", 0)
                    LEFT JOIN (SELECT
                                OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID"        AS "ID_CHUNG_TU",
                                coalesce(OAEDI."NGAY_HOA_DON", den_ngay)   AS "NGAY_HOA_DON",
                                coalesce(OAEDI."SO_HOA_DON", '')           AS "SO_HOA_DON",
                                OAEDI."HAN_THANH_TOAN",
                                coalesce(OAEDI."TY_GIA", 0)                AS "TY_GIA",
                                ROW_NUMBER()
                                OVER (
                                PARTITION BY OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID",
                                    coalesce(OAEDI."NGAY_HOA_DON", den_ngay),
                                    coalesce(OAEDI."SO_HOA_DON", ''),
                                    coalesce(OAEDI."TY_GIA", 0)
                                ORDER BY OAEDI."THU_TU_TRONG_CHUNG_TU" ) AS RowNumber
                            FROM account_ex_sdtkct_theo_hoa_don AS OAEDI
                            WHERE OAEDI."HAN_THANH_TOAN" IS NOT NULL
                            ) AS OPID ON OPN.id = OPID."ID_CHUNG_TU"
                                        AND OPID.RowNumber = 1
                                        AND coalesce(OPI."SO_HOA_DON", '') = coalesce(OPID."SO_HOA_DON", '')
                                        AND coalesce(OPI."NGAY_HOA_DON", den_ngay) = coalesce(OPID."NGAY_HOA_DON", den_ngay)
                                        AND coalesce(OPI."TY_GIA", 0) = coalesce(OPID."TY_GIA", 0)


                WHERE (OPN."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id ISNULL)
                        AND OPN."currency_id" = loai_tien_id
                        AND OPN."TK_ID" = (SELECT id
                                        FROM danh_muc_he_thong_tai_khoan
                                        WHERE "SO_TAI_KHOAN" = '131')
                        AND OPN."CHI_NHANH_ID" = chi_nhanh_id
                        AND OPN."NGAY_HACH_TOAN" <= den_ngay
                --         AND OPN.state = 'da_ghi_so'

                GROUP BY OPN.id,
                    OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID",
                    OPN."LOAI_CHUNG_TU",
                    RT."REFTYPENAME",
                    OPN."NGAY_HACH_TOAN",
                    OPI."NGAY_HOA_DON",
                    coalesce(OPI."SO_HOA_DON", ''),
                    coalesce(OPI."TY_GIA", 1),
                    coalesce(OPN."TY_GIA", 1),
                    OPID."HAN_THANH_TOAN",
                    OPID2."NHAN_VIEN_ID"
                HAVING SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                    THEN coalesce(OPI."SO_CON_PHAI_THU", 0)
                            ELSE coalesce(OPN."DU_NO_NGUYEN_TE", 0)
                                - coalesce(OPN."DU_CO_NGUYEN_TE",
                                            0)
                            END) > 0


                UNION ALL


                SELECT
                    AL."ID_CHUNG_TU",
                    AL."MODEL_CHUNG_TU",
                    cast(AL."LOAI_CHUNG_TU" AS VARCHAR(50)),
                    RT."REFTYPENAME",
                    AL."NGAY_CHUNG_TU",
                    AL."NGAY_HACH_TOAN",
                    AL."SO_CHUNG_TU",
                    AL."NGAY_HOA_DON",
                    coalesce(AL."SO_HOA_DON", '')             AS "SO_HOA_DON",
                    coalesce(AL."DIEN_GIAI_CHUNG", '')        AS "DIEN_GIAI",
                    coalesce(AL."TY_GIA", 1)                  AS "TY_GIA",
                    SUM(coalesce(AL."GHI_NO_NGUYEN_TE", 0)
                        - coalesce(AL."GHI_CO_NGUYEN_TE", 0)) AS "TONG_TIEN",
                    SUM(coalesce(AL."GHI_NO", 0)
                        - coalesce(AL."GHI_CO", 0))           AS "TONG_TIEN_QUY_DOI",
                    SUM(coalesce(AL."GHI_NO_NGUYEN_TE", 0)
                        - coalesce(AL."GHI_CO_NGUYEN_TE", 0)) AS "SO_TIEN",
                    SUM(coalesce(AL."GHI_NO", 0)
                        - coalesce(AL."GHI_CO", 0))           AS "SO_TIEN_QUY_DOI",
                    0                                         AS "SO_HOA_DON_CHI_TIET",
                    AL."NGAY_HET_HAN",
                    /*Nếu chứng từ Nghiệp vụ khác thì sẽ lấy nhân viên đầu tiên trên form chi tiết*/
                    CASE WHEN GVDT."ID_CHUNG_TU" IS NOT NULL
                    THEN GVDT."NHAN_VIEN_ID"
                    ELSE AL."NHAN_VIEN_ID"
                    END                                       AS "NHAN_VIEN_ID"
                FROM so_cong_no_chi_tiet AL
                    LEFT JOIN danh_muc_reftype RT ON RT."REFTYPE" = AL."LOAI_CHUNG_TU"
                    LEFT JOIN (/*Lấy Nhân viên trên chứng từ nghiệp vụ khác*/
                                SELECT
                                AOL."ID_CHUNG_TU",
                                AOL."DOI_TUONG_ID",
                                AOL."MA_TK",
                                AOL."NHAN_VIEN_ID",
                                ROW_NUMBER()
                                OVER (
                                    PARTITION BY AOL."ID_CHUNG_TU",
                                    AOL."DOI_TUONG_ID",
                                    AOL."MA_TK"
                                    ORDER BY AOL."THU_TU_TRONG_CHUNG_TU" ) AS RowNumber
                                FROM so_cong_no_chi_tiet AS AOL
                                WHERE
                                AOL."LOAI_CHUNG_TU" IN (4010, 4011, 4012, 4014, 4015, 4018, 4020, 4030)
                                /*Chỉ lấy theo "LOAI_CHUNG_TU" của bảng GlVoucherDetail
                                Không lấy các chứng từ Chứng từ bù trừ công nợ, Xử lý chênh lệch tỷ giá từ đánh giá lại tài khoản ngoại tệ, Xử lý chênh lệch tỷ giá từ tính tỷ giá xuất quỹ
                                */
                                AND AOL."NHAN_VIEN_ID" IS NOT NULL
                            ) AS GVDT ON GVDT."ID_CHUNG_TU" = AL."ID_CHUNG_TU"
                                        AND GVDT."DOI_TUONG_ID" = AL."DOI_TUONG_ID"
                                        AND GVDT."MA_TK" = AL."MA_TK"
                                        AND GVDT.RowNumber = 1
                    LEFT JOIN (
                                /* Lấy danh sách chứng từ trả lại giảm giá chọn trực tiếp*/
                                SELECT "TRA_LAI_HANG_BAN_ID" AS "ID_CHUNG_TU"
                                FROM sale_ex_tra_lai_hang_ban_chi_tiet
                                WHERE "CHUNG_TU_BAN_HANG_ID" IS NOT NULL
                                UNION
                                SELECT "GIAM_GIA_HANG_BAN_ID" AS "ID_CHUNG_TU"
                                FROM sale_ex_chi_tiet_giam_gia_hang_ban
                                WHERE "CHUNG_TU_BAN_HANG_ID" IS NOT NULL
                            ) SR ON AL."ID_CHUNG_TU" = SR."ID_CHUNG_TU"
                WHERE (AL."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id ISNULL)
                        AND AL."currency_id" = loai_tien_id
                        AND AL."TK_ID" = (SELECT id
                                        FROM danh_muc_he_thong_tai_khoan
                                        WHERE "SO_TAI_KHOAN" = '131')
                        AND AL."CHI_NHANH_ID" = chi_nhanh_id
                        AND AL."NGAY_HACH_TOAN" <= den_ngay
                        /* Không lấy các chứng từ Phiếu thu tiền khách hàng, Phiếu thu tiền khách hàng hàng loạt, Phiếu chi trả tiền nhà cung cấp,
                        *  Phiếu thu tiền gửi khách hàng, Phiếu thu tiền gửi khách hàng hàng loạt, Trả tiền nhà cung cấp bằng Ủy nhiệm chi,
                        *  Séc tiền mặt trả tiền nhà cung cấp, Séc chuyển khoản trả tiền nhà cung cấp, Chứng từ xử lý chênh lệch tỷ giá,
                        *  Chứng từ bù trừ công nợ, Xử lý chênh lệch tỷ giá từ đánh giá lại tài khoản ngoại tệ, Xử lý chênh lệch tỷ giá từ tính tỷ giá xuất quỹ*/
                        AND AL."LOAI_CHUNG_TU" NOT IN (1011, 1012, 1021, 1502, 1503, 1511, 1521, 1531, 4013, 4016, 4017)
                        /*Không lấy số dư đầu kỳ do lấy ở trên rồi*/
                        AND AL."LOAI_CHUNG_TU" NOT IN (611, 612, 613, 614, 615, 616, 630)
                        /*Không lấy các chứng từ trả lại, giảm giá*/
                        AND SR."ID_CHUNG_TU" IS NULL

                GROUP BY AL."ID_CHUNG_TU",
                    AL."MODEL_CHUNG_TU",
                    AL."LOAI_CHUNG_TU",
                    RT."REFTYPENAME",
                    AL."NGAY_CHUNG_TU",
                    AL."NGAY_HACH_TOAN",
                    AL."SO_CHUNG_TU",
                    AL."NGAY_HOA_DON",
                    coalesce(AL."SO_HOA_DON", ''),
                    coalesce(AL."DIEN_GIAI_CHUNG", ''),
                    coalesce(AL."TY_GIA", 1),
                    AL."NGAY_HET_HAN",
                    CASE WHEN GVDT."ID_CHUNG_TU" IS NOT NULL
                    THEN GVDT."NHAN_VIEN_ID"
                    ELSE AL."NHAN_VIEN_ID"
                    END
                HAVING SUM(coalesce(AL."GHI_NO_NGUYEN_TE", 0)
                            - coalesce(AL."GHI_CO_NGUYEN_TE", 0)) > 0;

            DROP TABLE IF EXISTS TMP_TABLE_2;
            CREATE TEMP TABLE TMP_TABLE_2
                AS
                SELECT
                    TEM."ID_CHUNG_TU",
                    TEM."MODEL_CHUNG_TU",
                    TEM."LOAI_CHUNG_TU",
                    TEM."TEN_LOAI_CHUNG_TU",
                    TEM."NGAY_CHUNG_TU",
                    TEM."NGAY_HACH_TOAN",
                    TEM."SO_CHUNG_TU",
                    TEM."NGAY_HOA_DON",
                    TEM."SO_HOA_DON",
                    TEM."DIEN_GIAI",
                    TEM."TY_GIA",
                    coalesce(GV."TY_GIA", 0)                                                    AS "TY_GIA_DANH_GIA_LAI",
                    TEM."TONG_TIEN"                                                             AS "SO_TIEN",
                    TEM."TONG_TIEN_QUY_DOI"                                                     AS "SO_TIEN_QUY_DOI",
                    coalesce(TEM."SO_TIEN", 0) - SUM(coalesce(GL."SO_TIEN", 0))                 AS "SO_TIEN_CONG_NO",
                    coalesce(TEM."SO_TIEN_QUY_DOI", 0) - SUM(coalesce(GL."SO_TIEN_QUY_DOI", 0)) AS "SO_TIEN_CONG_NO_QUY_DOI",
                    CAST(0 AS DECIMAL)                                                          AS "SO_TIEN_DOI_TRU",
                    CAST(0 AS DECIMAL)                                                          AS "SO_TIEN_DOI_TRU_QUY_DOI",
                    doi_tuong_id                                                                AS "DOI_TUONG_ID",
                    TEM."HAN_THANH_TOAN",
                    TEM."NHAN_VIEN_ID",
                    E."MA"                                                                      AS "MA_NHAN_VIEN",
                    --nvtoan Modify 22/04/2017: Sửa lỗi 96455
                    E."HO_VA_TEN"                                                               AS "TEN_NHAN_VIEN" --NVTOAN modify 13/04/2017 thực hiện CR 34929
                FROM TMP_TABLE_1 AS TEM
                    LEFT JOIN (SELECT *
                            FROM FUNCTION_DOI_TRU_CHUNG_TU_BAN_HANG_CONG_NO('131', loai_tien_id, chi_nhanh_id, doi_tuong_id)) GL
                    ON GL."ID_CHUNG_TU" = TEM."ID_CHUNG_TU"
                        AND GL."MODEL_CHUNG_TU" = TEM."MODEL_CHUNG_TU"
                        AND (TEM."SO_HOA_DON_CHI_TIET" = 0
                            OR (TEM."SO_HOA_DON_CHI_TIET" = 1
                                AND coalesce(GL."SO_HOA_DON", '') = coalesce(TEM."SO_HOA_DON", '')
                                AND coalesce(GL."NGAY_HOA_DON", den_ngay) = coalesce(TEM."NGAY_HOA_DON", den_ngay)
                            )
                        )

                        AND ((GL."TY_GIA" = TEM."TY_GIA")
                            OR "LOAI_CHUNG_TU" NOT IN
                                ('611', '612', '613', '614', '615', '616', '630')--nvtoan modify 11/04/2017 Sửa lỗi 90132: Đối với chứng từ không phải số dư đầu thì không join qua "TY_GIA"
                        )
                    LEFT JOIN (
                                SELECT
                                CASE WHEN '15' = '15'
                                    THEN coalesce(GV."TY_GIA", 1)
                                ELSE coalesce(GV."TY_GIA", 1)
                                END                                                          AS "TY_GIA",
                                /* NBHIEU 12/05/2016 (bug 102978) Lấy tỷ giá đánh giá lại dưới chi tiết nếu là quyết dịnh 15*/
                                GVD."ID_CHUNG_TU_GOC"                                        AS "ID_CHUNG_TU",
                                ROW_NUMBER()
                                OVER (
                                    PARTITION BY GVD."ID_CHUNG_TU_GOC"
                                    ORDER BY GVD."ID_CHUNG_TU_GOC", GV."NGAY_HACH_TOAN" DESC ) AS RowNumber
                                FROM account_ex_chung_tu_nghiep_vu_khac GV
                                INNER JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan GVD
                                    ON GVD."ID_CHUNG_TU_GOC" = GV.id
                                WHERE
                                GV."CHI_NHANH_ID" = chi_nhanh_id AND
                                GV.currency_id = loai_tien_id
                                AND GVD."TK_CONG_NO_ID" = (SELECT id
                                                            FROM danh_muc_he_thong_tai_khoan
                                                            WHERE "SO_TAI_KHOAN" = '131')
                                AND (GVD."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id ISNULL)
                                AND GV.state = 'da_ghi_so'
                            ) AS GV ON TEM."ID_CHUNG_TU" = GV."ID_CHUNG_TU"
                                        AND GV.RowNumber = 1
                    LEFT JOIN res_partner E ON TEM."NHAN_VIEN_ID" = E.id --NVTOAN modify 13/04/2017 thực hiện CR 34929
                GROUP BY TEM."ID_CHUNG_TU",
                    TEM."MODEL_CHUNG_TU",
                    TEM."LOAI_CHUNG_TU",
                    TEM."TEN_LOAI_CHUNG_TU",
                    TEM."NGAY_CHUNG_TU",
                    TEM."NGAY_HACH_TOAN",
                    TEM."SO_CHUNG_TU",
                    TEM."NGAY_HOA_DON",
                    TEM."SO_HOA_DON",
                    TEM."DIEN_GIAI",
                    TEM."TY_GIA",
                    coalesce(GV."TY_GIA", 0),
                    TEM."SO_TIEN",
                    TEM."SO_TIEN_QUY_DOI",
                    TEM."TONG_TIEN",
                    TEM."TONG_TIEN_QUY_DOI",
                    TEM."HAN_THANH_TOAN",
                    TEM."NHAN_VIEN_ID",
                    E."MA", --nvtoan Modify 22/04/2017: Sửa lỗi 96455
                    E."HO_VA_TEN" --NVTOAN modify 13/04/2017 thực hiện CR 34929
                HAVING coalesce(TEM."SO_TIEN", 0) - SUM(coalesce(GL."SO_TIEN", 0)) > 0
                ORDER BY TEM."NGAY_CHUNG_TU",
                    TEM."NGAY_HACH_TOAN",
                    TEM."SO_CHUNG_TU",
                    TEM."NGAY_HOA_DON",
                    TEM."SO_HOA_DON";

            END $$;

            SELECT *
            FROM TMP_TABLE_2;


        """  
        
        return self.execute(query, params)


    

    def mua_hang_chung_tu_thanh_toan(self,ngay,doi_tuong,loai_tien):
        record = []
        params = {
            'DOI_TUONG_ID': doi_tuong,
            'currency_id' : loai_tien,
            'DEN_NGAY' : ngay,
            'CHI_NHANH_ID' : self.get_chi_nhanh(),
            }

        query = """   
                DO LANGUAGE plpgsql $$ DECLARE

                doi_tuong_id INTEGER := %(DOI_TUONG_ID)s;
                den_ngay     DATE := %(DEN_NGAY)s;
                loai_tien_id INTEGER :=%(currency_id)s;
                chi_nhanh_id INTEGER := %(CHI_NHANH_ID)s;

                BEGIN
                DROP TABLE IF EXISTS TMP_TBALE_1;
                CREATE TEMP TABLE TMP_TBALE_1
                    AS
                    SELECT
                        OPN.id                                AS "ID_CHUNG_TU",
                        'account.ex.so.du.tai.khoan.chi.tiet' AS "MODEL_CHUNG_TU",
                        OPN."LOAI_CHUNG_TU"
                        --         , RT."REFTYPENAME"               AS "TEN_LOAI_CHUNG_TU"
                        ,
                        (CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL AND OPI."SO_THU_TRUOC" <> 0
                        THEN OPI."NGAY_HOA_DON"
                        ELSE OPN."NGAY_HACH_TOAN"
                        END)                                    "NGAY_CHUNG_TU",
                        OPN."NGAY_HACH_TOAN",
                        (CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL AND OPI."SO_THU_TRUOC" <> 0
                        THEN coalesce(OPI."SO_HOA_DON", '')
                        ELSE 'OPN'
                        END)                                 AS "SO_CHUNG_TU",
                        coalesce(OPI."SO_HOA_DON", '')        AS "SO_HOA_DON",
                        ''                                    AS "DIEN_GIAI",
                        (CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                        THEN coalesce(OPI."TY_GIA", 1)
                        ELSE coalesce(OPN."TY_GIA", 1)
                        END)                                 AS "TY_GIA",
                        SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                        THEN coalesce(OPI."SO_THU_TRUOC", 0)
                            ELSE coalesce(OPN."DU_NO_NGUYEN_TE", 0) - coalesce(OPN."DU_CO_NGUYEN_TE", 0)
                            END)                              AS "SO_TIEN",
                        SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                        THEN coalesce(OPI."SO_THU_TRUOC", 0)
                            ELSE coalesce(OPN."DU_NO", 0) - coalesce(OPN."DU_CO", 0)
                            END)                              AS "SO_TIEN_QUY_DOI",
                        SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                        THEN coalesce(OPI."SO_THU_TRUOC", 0)
                            ELSE coalesce(OPN."DU_NO_NGUYEN_TE", 0) - coalesce(OPN."DU_CO_NGUYEN_TE", 0)
                            END)                              AS "SO_TIEN_THU",
                        SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                        THEN coalesce(OPI."SO_THU_TRUOC", 0)
                            ELSE coalesce(OPN."DU_NO", 0) - coalesce(OPN."DU_CO", 0)
                            END)                              AS "SO_TIEN_THU_QUY_DOI",
                        doi_tuong_id                          AS "DOI_TUONG_ID",
                        OPN."SO_TAI_KHOAN",
                        1                                     AS "SO_HOA_DON_CHI_TIET",
                        OPID2."NHAN_VIEN_ID" --NVTOAN modify 14/04/2017 thực hiện CR 34929
                    FROM account_ex_so_du_tai_khoan_chi_tiet OPN
                        INNER JOIN danh_muc_reftype RT ON cast(RT."REFTYPE" AS VARCHAR(50)) = OPN."LOAI_CHUNG_TU"
                        LEFT JOIN account_ex_sdtkct_theo_hoa_don OPI
                        ON OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" = OPN.id
                        LEFT JOIN (
                                    SELECT
                                    OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID",
                                    coalesce(OAEDI."NGAY_HOA_DON", NOW())      AS "NGAY_HOA_DON",
                                    coalesce(OAEDI."SO_HOA_DON", '')           AS "SO_HOA_DON",
                                    coalesce(OAEDI."TY_GIA", 0)                AS "TY_GIA",
                                    OAEDI."NHAN_VIEN_ID",
                                    ROW_NUMBER()
                                    OVER (
                                        PARTITION BY OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID",
                                        coalesce(OAEDI."NGAY_HOA_DON", NOW()),
                                        coalesce(OAEDI."SO_HOA_DON", ''),
                                        coalesce(OAEDI."TY_GIA", 0)
                                        ORDER BY OAEDI."THU_TU_TRONG_CHUNG_TU" ) AS RowNumber
                                    FROM account_ex_sdtkct_theo_hoa_don AS OAEDI
                                    WHERE OAEDI."NHAN_VIEN_ID" IS NOT NULL
                                ) AS OPID2 ON OPN.id = OPID2."SO_DU_TAI_KHOAN_CHI_TIET_ID"
                                                AND OPID2.RowNumber = 1
                                                AND coalesce(OPI."SO_HOA_DON", '') = coalesce(OPID2."SO_HOA_DON", '')
                                                AND coalesce(OPI."NGAY_HOA_DON", NOW()) = coalesce(OPID2."NGAY_HOA_DON", NOW())
                                                AND coalesce(OPI."TY_GIA", 0) = coalesce(OPID2."TY_GIA", 0)
                    --NVTOAN add 14/04/2017 thực hiện CR 34929
                    WHERE
                        (OPN."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id ISNULL)
                        AND OPN."currency_id" = loai_tien_id
                        AND OPN."SO_TAI_KHOAN" = (SELECT "SO_TAI_KHOAN"
                                                FROM danh_muc_he_thong_tai_khoan
                                                WHERE "SO_TAI_KHOAN" = '331')
                        AND OPN."CHI_NHANH_ID" = chi_nhanh_id
                        AND OPN."NGAY_HACH_TOAN" <= den_ngay

                    GROUP BY OPN.id,
                        (CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                                AND OPI."SO_THU_TRUOC" <> 0
                        THEN OPI."NGAY_HOA_DON"
                        ELSE OPN."NGAY_HACH_TOAN"
                        END),
                        (CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                        THEN coalesce(OPI."TY_GIA", 1)
                        ELSE coalesce(OPN."TY_GIA", 1)
                        END),
                        OPN."LOAI_CHUNG_TU",
                        --         RT."REFTYPENAME",
                        OPN."NGAY_HACH_TOAN",
                        (CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                                AND OPI."SO_THU_TRUOC" <> 0
                        THEN coalesce(OPI."SO_HOA_DON", '')
                        ELSE 'OPN'
                        END),
                        OPI."NGAY_HOA_DON",
                        coalesce(OPI."SO_HOA_DON", ''),
                        coalesce(OPI."TY_GIA", 1),
                        coalesce(OPN."TY_GIA", 1),
                        OPN."SO_TAI_KHOAN",
                        OPID2."NHAN_VIEN_ID" --NVTOAN modify 14/04/2017 thực hiện CR 34929
                    HAVING SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                        THEN coalesce(OPI."SO_THU_TRUOC", 0)
                                ELSE coalesce(OPN."DU_NO_NGUYEN_TE", 0) - coalesce(OPN."DU_CO_NGUYEN_TE", 0)
                                END) > 0;

                DROP TABLE IF EXISTS TMP_TBALE_2;
                CREATE TEMP TABLE TMP_TBALE_2
                    AS
                    SELECT
                        AL."ID_CHUNG_TU",
                        AL."MODEL_CHUNG_TU",
                        cast(AL."LOAI_CHUNG_TU" AS VARCHAR(50))   AS "LOAI_CHUNG_TU",
                        --           AL."LOAI_CHUNG_TU" ,
                        AL."NGAY_CHUNG_TU",
                        AL."NGAY_HACH_TOAN",
                        AL."SO_CHUNG_TU",
                        coalesce(AL."SO_HOA_DON", '')             AS "SO_HOA_DON",
                        coalesce(AL."DIEN_GIAI_CHUNG", '')        AS "DIEN_GIAI",
                        coalesce(AL."TY_GIA", 1)                  AS "TY_GIA",
                        SUM(coalesce(AL."GHI_NO_NGUYEN_TE", 0)
                            - coalesce(AL."GHI_CO_NGUYEN_TE", 0)) AS "SO_TIEN",
                        SUM(coalesce(AL."GHI_NO", 0)
                            - coalesce(AL."GHI_CO", 0))           AS "SO_TIEN_QUY_DOI",
                        SUM(coalesce(AL."GHI_NO_NGUYEN_TE", 0)
                            - coalesce(AL."GHI_CO_NGUYEN_TE", 0)) AS "SO_TIEN_THU",
                        SUM(coalesce(AL."GHI_NO", 0)
                            - coalesce(AL."GHI_CO", 0))           AS "SO_TIEN_THU_QUY_DOI",
                        doi_tuong_id                              AS "DOI_TUONG_ID",
                        AL."MA_TK",
                        0                                         AS "SO_HOA_DON_CHI_TIET",
                        CASE WHEN GVDT."ID_CHUNG_TU" IS NOT NULL
                        THEN GVDT."NHAN_VIEN_ID"
                        ELSE AL."NHAN_VIEN_ID"
                        END                                       AS "NHAN_VIEN_ID" --NVTOAN modify 14/04/2017 thực hiện CR 34929
                    FROM so_cong_no_chi_tiet AS AL
                        LEFT JOIN (/*Lấy Nhân viên trên chứng từ nghiệp vụ khác*/
                                    SELECT
                                    AOL."ID_CHUNG_TU",
                                    AOL."DOI_TUONG_ID",
                                    AOL."MA_TK",
                                    AOL."NHAN_VIEN_ID",
                                    ROW_NUMBER()
                                    OVER (
                                        PARTITION BY AOL."ID_CHUNG_TU",
                                        AOL."DOI_TUONG_ID",
                                        AOL."MA_TK"
                                        ORDER BY AOL."THU_TU_TRONG_CHUNG_TU" ) AS RowNumber
                                    FROM so_cong_no_chi_tiet AS AOL
                                    WHERE AOL."LOAI_CHUNG_TU" IN ('4010', '4011', '4012', '4014', '4015', '4018', '4020', '4030')
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
                        (AL."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id ISNULL)
                        AND AL."currency_id" = loai_tien_id
                        AND AL."TK_ID" = (SELECT id
                                        FROM danh_muc_he_thong_tai_khoan
                                        WHERE "SO_TAI_KHOAN" = '331')
                        --           AND AL."CHI_NHANH_ID" = (chi_nhanh_id)
                        --Không lấy các chứng từ Phiếu thu tiền khách hàng, Phiếu thu tiền khách hàng hàng loạt, Phiếu chi trả tiền nhà cung cấp, Phiếu thu tiền gửi khách hàng, Phiếu thu tiền gửi khách hàng hàng loạt, Trả tiền nhà cung cấp bằng Ủy nhiệm chi, Séc tiền mặt trả tiền nhà cung cấp, Séc chuyển khoản trả tiền nhà cung cấp, Chứng từ xử lý chênh lệch tỷ giá, Chứng từ bù trừ công nợ, Xử lý chênh lệch tỷ giá từ đánh giá lại tài khoản ngoại tệ, Xử lý chênh lệch tỷ giá từ tính tỷ giá xuất quỹ
                        AND AL."LOAI_CHUNG_TU" NOT IN
                            (1011, 1012, 1021, 1502, 1503, 1511, 1521, 1531, 4013, 4016, 4017, 611, 612, 613, 614, 615, 616, 630)
                        AND AL."NGAY_HACH_TOAN" <= den_ngay

                    GROUP BY AL."ID_CHUNG_TU",
                        AL."MODEL_CHUNG_TU",
                        AL."LOAI_CHUNG_TU",
                        --           AL."LOAI_CHUNG_TU" ,
                        AL."NGAY_CHUNG_TU",
                        AL."NGAY_HACH_TOAN",
                        AL."SO_CHUNG_TU",
                        coalesce(AL."SO_HOA_DON", ''),
                        coalesce(AL."DIEN_GIAI_CHUNG", ''),
                        coalesce(AL."TY_GIA", 1),
                        AL."MA_TK",
                        CASE WHEN GVDT."ID_CHUNG_TU" IS NOT NULL
                        THEN GVDT."NHAN_VIEN_ID"
                        ELSE AL."NHAN_VIEN_ID"
                        END --NVTOAN modify 14/04/2017 thực hiện CR 34929
                    HAVING SUM(coalesce(AL."GHI_NO_NGUYEN_TE", 0)
                                - coalesce(AL."GHI_CO_NGUYEN_TE", 0)) > 0;

                DROP TABLE IF EXISTS TMP_TBALE_3;
                CREATE TEMP TABLE TMP_TBALE_3
                    AS
                    SELECT
                        OPNTemp."ID_CHUNG_TU",
                        OPNTemp."MODEL_CHUNG_TU",
                        OPNTemp."LOAI_CHUNG_TU",
                        --                             OPNTemp."LOAI_CHUNG_TU" ,
                        OPNTemp."NGAY_CHUNG_TU",
                        OPNTemp."NGAY_HACH_TOAN",
                        -- nmtruong: 11/5/2016 sửa bug 101936 thay refdate = posteddate để ghi xuống bảng đối trừ đúng ngày hạch toán
                        OPNTemp."SO_CHUNG_TU",
                        OPNTemp."SO_HOA_DON",
                        OPNTemp."DIEN_GIAI",
                        OPNTemp."TY_GIA",
                        OPNTemp."SO_TIEN",
                        OPNTemp."SO_TIEN_QUY_DOI",
                        (OPNTemp."SO_TIEN_THU" - coalesce(SUM(GL."SO_TIEN"), 0))               AS "SO_TIEN_THU",
                        OPNTemp."SO_TIEN_THU_QUY_DOI" - coalesce(SUM(GL."SO_TIEN_QUY_DOI"), 0) AS "SO_TIEN_THU_QUY_DOI",
                        OPNTemp."DOI_TUONG_ID",
                        OPNTemp."SO_TAI_KHOAN",
                        OPNTemp."NHAN_VIEN_ID" --NVTOAN modify 14/04/2017 thực hiện CR 34929
                    FROM (
                            SELECT *
                            FROM TMP_TBALE_1
                            UNION ALL
                            SELECT *
                            FROM TMP_TBALE_2
                        ) AS OPNTemp
                        LEFT JOIN (SELECT *
                                FROM FUNCTION_DOI_TRU_MUA_HANG_THANH_TOAN('331', loai_tien_id, chi_nhanh_id, doi_tuong_id)) GL
                        ON cast(GL."ID_CHUNG_TU" AS INTEGER) = cast(OPNTemp."ID_CHUNG_TU" AS INTEGER)
                            AND GL."DOI_TUONG_ID" = OPNTemp."DOI_TUONG_ID"
                            AND GL."SO_TAI_KHOAN" = OPNTemp."SO_TAI_KHOAN"
                            AND (OPNTemp."SO_HOA_DON_CHI_TIET" = '0'
                                OR (OPNTemp."SO_HOA_DON_CHI_TIET" = '1'
                                    AND coalesce(GL."SO_CHUNG_TU", '') = coalesce(OPNTemp."SO_CHUNG_TU", '')
                                    AND
                                    coalesce(GL."NGAY_CHUNG_TU", den_ngay) = coalesce(OPNTemp."NGAY_CHUNG_TU", den_ngay)
                                )
                            )
                            AND GL."SO_CHUNG_TU" = OPNTemp."SO_CHUNG_TU"
                    GROUP BY OPNTemp."ID_CHUNG_TU",
                        OPNTemp."MODEL_CHUNG_TU",
                        OPNTemp."LOAI_CHUNG_TU",
                        OPNTemp."LOAI_CHUNG_TU",
                        OPNTemp."NGAY_CHUNG_TU",
                        OPNTemp."NGAY_HACH_TOAN",
                        OPNTemp."SO_CHUNG_TU",
                        OPNTemp."SO_HOA_DON",
                        OPNTemp."DIEN_GIAI",
                        OPNTemp."TY_GIA",
                        OPNTemp."SO_TIEN",
                        OPNTemp."SO_TIEN_QUY_DOI",
                        OPNTemp."SO_TIEN_THU",
                        OPNTemp."SO_TIEN_THU_QUY_DOI",
                        OPNTemp."DOI_TUONG_ID",
                        OPNTemp."SO_TAI_KHOAN",
                        OPNTemp."NHAN_VIEN_ID" --NVTOAN modify 14/04/2017 thực hiện CR 34929
                    HAVING OPNTemp."SO_TIEN_THU" - coalesce(SUM(GL."SO_TIEN"), 0) > 0;

                DROP TABLE IF EXISTS TMP_TBALE_4;
                CREATE TEMP TABLE TMP_TBALE_4
                    AS
                    SELECT
                        AL."ID_CHUNG_TU",
                        AL."MODEL_CHUNG_TU",
                        AL."LOAI_CHUNG_TU",
                        --                AL."LOAI_CHUNG_TU" ,
                        AL."NGAY_CHUNG_TU",
                        AL."NGAY_HACH_TOAN",
                        AL."SO_CHUNG_TU",
                        AL."SO_HOA_DON",
                        AL."DIEN_GIAI",
                        AL."TY_GIA",
                        coalesce(GV."TY_GIA",0) AS "TY_GIA_DANH_GIA_LAI",
                        SUM(AL."SO_TIEN")             AS "SO_TIEN",
                        SUM(AL."SO_TIEN_QUY_DOI")     AS "SO_TIEN_QUY_DOI",
                        SUM(AL."SO_TIEN_THU")         AS "SO_TIEN_THU",
                        SUM(AL."SO_TIEN_THU_QUY_DOI") AS "SO_TIEN_THU_QUY_DOI",
                        0                             AS "SO_TIEN_DOI_TRU",
                        0                             AS "SO_TIEN_DOI_TRU_QUY_DOI",
                        doi_tuong_id                  AS "DOI_TUONG_ID",
                        AL."NHAN_VIEN_ID",
                        --NVTOAN modify 14/04/2017 thực hiện CR 34929
                        E."MA"                        AS "MA_NHAN_VIEN",
                        --nvtoan Modify 22/04/2017: Sửa lỗi 96455
                        E."HO_VA_TEN"                 AS "TEN_NHAN_VIEN"
                    FROM TMP_TBALE_3 AS AL
                        LEFT JOIN (
                                    -- Lấy danh sách chứng từ trả lại giảm giá chọn trực tiếp
                                    SELECT "GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID" AS "ID_CHUNG_TU"
                                    FROM purchase_ex_giam_gia_hang_mua_chi_tiet
                                    WHERE "CHUNG_TU_MUA_HANG" IS NOT NULL
                                    UNION
                                    SELECT "GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID" AS "ID_CHUNG_TU"
                                    FROM purchase_ex_giam_gia_hang_mua_chi_tiet
                                    WHERE "CHUNG_TU_MUA_HANG" IS NOT NULL
                                ) SR ON AL."ID_CHUNG_TU" = SR."ID_CHUNG_TU"
                        LEFT JOIN (
                                    SELECT
                                    CASE WHEN '15' = '15'
                                        THEN coalesce(GV."TY_GIA", 1)
                                    ELSE coalesce(GV."TY_GIA", 1)
                                    END                                                          AS "TY_GIA"
                                    /* NBHIEU 12/05/2016 (bug 102978) Lấy tỷ giá đánh giá lại dưới chi tiết nếu là quyết dịnh 15*/,
                                    GVD."ID_CHUNG_TU_GOC"                                        AS "ID_CHUNG_TU",
                                    ROW_NUMBER()
                                    OVER (
                                        PARTITION BY GVD."ID_CHUNG_TU_GOC"
                                        ORDER BY GVD."ID_CHUNG_TU_GOC", GV."NGAY_HACH_TOAN" DESC ) AS RowNumber
                                    FROM account_ex_chung_tu_nghiep_vu_khac GV
                                    INNER JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan GVD
                                        ON GVD."ID_CHUNG_TU_GOC" = GV.id
                                    WHERE
                                    --                                     GV."CHI_NHANH_ID" = (chi_nhanh_id)
                                    --                                     AND
                                    GV.currency_id = loai_tien_id
                                    AND GVD."TK_CONG_NO_ID" = (SELECT id
                                                                FROM danh_muc_he_thong_tai_khoan
                                                                WHERE "SO_TAI_KHOAN" = '331')
                                    AND GVD."DOI_TUONG_ID" = doi_tuong_id
                                    AND GV."state" = 'da_ghi_so'

                                ) AS GV ON AL."ID_CHUNG_TU" = GV."ID_CHUNG_TU"
                                            AND GV.RowNumber = 1
                        LEFT JOIN res_partner E ON AL."NHAN_VIEN_ID" = E.id --NVTOAN modify 14/04/2017 thực hiện CR 34929
                    GROUP BY AL."ID_CHUNG_TU",
                        AL."MODEL_CHUNG_TU",
                        AL."LOAI_CHUNG_TU",
                        AL."LOAI_CHUNG_TU",
                        AL."NGAY_CHUNG_TU",
                        AL."NGAY_HACH_TOAN",
                        AL."SO_CHUNG_TU",
                        AL."SO_HOA_DON",
                        AL."DIEN_GIAI",
                        AL."TY_GIA",
                        AL."DOI_TUONG_ID",
                        AL."NHAN_VIEN_ID", --NVTOAN modify 14/04/2017 thực hiện CR 34929
                        E."MA", --nvtoan Modify 22/04/2017: Sửa lỗi 96455
                        E."HO_VA_TEN",
                        coalesce(GV."TY_GIA",0)
                    HAVING SUM(AL."SO_TIEN_THU") > 0
                    ORDER BY AL."NGAY_CHUNG_TU", --DATRUONG 25.08.2015 Chỉnh lại sort với chế độ tăng dần ngày chứng từ
                        AL."SO_CHUNG_TU",
                        coalesce(AL."SO_HOA_DON", '');
                END $$;

                SELECT *
                FROM TMP_TBALE_4

        

        """  
        
        return self.execute(query, params)


    def mua_hang_chung_tu_cong_no(self,ngay,doi_tuong,loai_tien):
        record = []
        params = {
            'DOI_TUONG_ID': doi_tuong,
            'currency_id' : loai_tien,
            'DEN_NGAY' : ngay,
            'CHI_NHANH_ID' : self.get_chi_nhanh(),
            }

        query = """   

                DO LANGUAGE plpgsql $$ DECLARE
                doi_tuong_id INTEGER := %(DOI_TUONG_ID)s;
                den_ngay     DATE := %(DEN_NGAY)s;
                loai_tien_id INTEGER :=%(currency_id)s;
                chi_nhanh_id INTEGER := %(CHI_NHANH_ID)s;


                BEGIN
                DROP TABLE IF EXISTS TMP_TBALE_1;
                CREATE TEMP TABLE TMP_TBALE_1
                    AS
                    SELECT
                        OPN.id                         AS "ID_CHUNG_TU",
                        'account.ex.so.du.tai.khoan.chi.tiet' AS "MODEL_CHUNG_TU",
                        OPN."LOAI_CHUNG_TU",
                        RT."REFTYPENAME"               AS "TEN_LOAI_CHUNG_TU",
                        (CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                        THEN OPI."NGAY_HOA_DON"
                        ELSE OPN."NGAY_HACH_TOAN"
                        END)                             "NGAY_CHUNG_TU",
                        OPN."NGAY_HACH_TOAN",
                        'OPN'                          AS "SO_CHUNG_TU",
                        OPI."NGAY_HOA_DON",
                        coalesce(OPI."SO_HOA_DON", '') AS "SO_HOA_DON",
                        ''                             AS "DIEN_GIAI",
                        (CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                        THEN coalesce(OPI."TY_GIA", 1)
                        ELSE coalesce(OPN."TY_GIA", 1)
                        END)                          AS "TY_GIA",
                        SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                        THEN coalesce(OPI."GIA_TRI_HOA_DON_NGUYEN_TE", 0)
                            ELSE coalesce(OPN."DU_CO_NGUYEN_TE", 0) - coalesce(OPN."DU_NO_NGUYEN_TE", 0)
                            END)                       AS "TONG_TIEN",
                        SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                        THEN coalesce(OPI."GIA_TRI_HOA_DON", 0)
                            ELSE coalesce(OPN."DU_CO", 0) - coalesce(OPN."DU_NO", 0)
                            END)                       AS "TONG_TIEN_QUY_DOI",
                        SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                        THEN coalesce(OPI."SO_CON_PHAI_THU_NGUYEN_TE", 0)
                            ELSE coalesce(OPN."DU_CO_NGUYEN_TE", 0) - coalesce(OPN."DU_NO_NGUYEN_TE", 0)
                            END)                       AS "SO_TIEN",
                        SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                        THEN coalesce(OPI."SO_CON_PHAI_THU", 0)
                            ELSE coalesce(OPN."DU_CO", 0) - coalesce(OPN."DU_NO", 0)
                            END)                       AS "SO_TIEN_QUY_DOI",
                        1                              AS "SO_HOA_DON_CHI_TIET",
                        OPID."HAN_THANH_TOAN",
                        OPID2."NHAN_VIEN_ID"
                    FROM account_ex_so_du_tai_khoan_chi_tiet OPN
                        INNER JOIN danh_muc_reftype RT ON cast(RT."REFTYPE" AS VARCHAR(50)) = OPN."LOAI_CHUNG_TU"
                        LEFT JOIN account_ex_sdtkct_theo_hoa_don OPI
                        ON OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" = OPN.id
                        LEFT JOIN (SELECT
                                    OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID",
                                    coalesce(OAEDI."NGAY_HOA_DON", NOW())      AS "NGAY_HOA_DON",
                                    coalesce(OAEDI."SO_HOA_DON", '')           AS "SO_HOA_DON",
                                    coalesce(OAEDI."TY_GIA", 0)                AS "TY_GIA",
                                    OAEDI."NHAN_VIEN_ID",
                                    ROW_NUMBER()
                                    OVER (
                                    PARTITION BY OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID",
                                        coalesce(OAEDI."NGAY_HOA_DON", NOW()),
                                        coalesce(OAEDI."SO_HOA_DON", ''),
                                        coalesce(OAEDI."TY_GIA", 0)
                                    ORDER BY OAEDI."THU_TU_TRONG_CHUNG_TU" ) AS RowNumber
                                FROM account_ex_sdtkct_theo_hoa_don AS OAEDI
                                WHERE OAEDI."NHAN_VIEN_ID" IS NOT NULL
                                ) AS OPID2 ON OPN.id = OPID2."SO_DU_TAI_KHOAN_CHI_TIET_ID"
                                                AND OPID2.RowNumber = 1
                                                AND coalesce(OPI."SO_HOA_DON", '') = coalesce(OPID2."SO_HOA_DON", '')
                                                AND coalesce(OPI."NGAY_HOA_DON", NOW()) = coalesce(OPID2."NGAY_HOA_DON", NOW())
                                                AND coalesce(OPI."TY_GIA", 0) = coalesce(OPID2."TY_GIA", 0)
                        LEFT JOIN (SELECT
                                    OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID"        AS "ID_CHUNG_TU",
                                    coalesce(OAEDI."NGAY_HOA_DON", den_ngay)   AS "NGAY_HOA_DON",
                                    coalesce(OAEDI."SO_HOA_DON", '')           AS "SO_HOA_DON",
                                    OAEDI."HAN_THANH_TOAN",
                                    coalesce(OAEDI."TY_GIA", 0)                AS "TY_GIA",
                                    ROW_NUMBER()
                                    OVER (
                                    PARTITION BY OAEDI."SO_DU_TAI_KHOAN_CHI_TIET_ID",
                                        coalesce(OAEDI."NGAY_HOA_DON", den_ngay),
                                        coalesce(OAEDI."SO_HOA_DON", ''),
                                        coalesce(OAEDI."TY_GIA", 0)
                                    ORDER BY OAEDI."THU_TU_TRONG_CHUNG_TU" ) AS RowNumber
                                FROM account_ex_sdtkct_theo_hoa_don AS OAEDI
                                WHERE OAEDI."HAN_THANH_TOAN" IS NOT NULL
                                ) AS OPID ON OPN.id = OPID."ID_CHUNG_TU"
                                            AND OPID.RowNumber = 1
                                            AND coalesce(OPI."SO_HOA_DON", '') = coalesce(OPID."SO_HOA_DON", '')
                                            AND coalesce(OPI."NGAY_HOA_DON", den_ngay) = coalesce(OPID."NGAY_HOA_DON", den_ngay)
                                            AND coalesce(OPI."TY_GIA", 0) = coalesce(OPID."TY_GIA", 0)


                    WHERE (OPN."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id ISNULL)
                            AND OPN."currency_id" = loai_tien_id
                            AND OPN."TK_ID" = (SELECT id
                                            FROM danh_muc_he_thong_tai_khoan
                                            WHERE "SO_TAI_KHOAN" = '331')
                            --         AND OPN."CHI_NHANH_ID" = (chi_nhanh_id)
                            AND OPN."NGAY_HACH_TOAN" <= den_ngay
                    --         AND OPN.state = 'da_ghi_so'

                    GROUP BY OPN.id,
                        OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID",
                        OPN."LOAI_CHUNG_TU",
                        RT."REFTYPENAME",
                        OPN."NGAY_HACH_TOAN",
                        OPI."NGAY_HOA_DON",
                        coalesce(OPI."SO_HOA_DON", ''),
                        coalesce(OPI."TY_GIA", 1),
                        coalesce(OPN."TY_GIA", 1),
                        OPID."HAN_THANH_TOAN",
                        OPID2."NHAN_VIEN_ID"
                    HAVING SUM(CASE WHEN OPI."SO_DU_TAI_KHOAN_CHI_TIET_ID" IS NOT NULL
                        THEN coalesce(OPI."SO_CON_PHAI_THU", 0)
                                ELSE coalesce(OPN."DU_CO_NGUYEN_TE", 0)
                                    - coalesce(OPN."DU_NO_NGUYEN_TE",
                                                0)
                                END) > 0;

                DROP TABLE IF EXISTS TMP_TBALE_2;
                CREATE TEMP TABLE TMP_TBALE_2
                    AS
                    SELECT
                        AL."ID_CHUNG_TU",
                        AL."MODEL_CHUNG_TU",
                        cast(AL."LOAI_CHUNG_TU" AS VARCHAR(50))   AS "LOAI_CHUNG_TU",
                        AL."TEN_LOAI_CHUNG_TU",
                        AL."NGAY_CHUNG_TU",
                        AL."NGAY_HACH_TOAN",
                        AL."SO_CHUNG_TU",
                        AL."NGAY_HOA_DON",
                        coalesce(AL."SO_HOA_DON", '')             AS "SO_HOA_DON",
                        coalesce(AL."DIEN_GIAI_CHUNG", '')        AS "DIEN_GIAI",
                        coalesce(AL."TY_GIA", 1)                  AS "TY_GIA",
                        SUM(coalesce(AL."GHI_CO_NGUYEN_TE", 0)
                            - coalesce(AL."GHI_NO_NGUYEN_TE", 0)) AS "TONG_TIEN",
                        SUM(coalesce(AL."GHI_CO", 0)
                            - coalesce(AL."GHI_NO", 0))           AS "TONG_TIEN_QUY_DOI",
                        SUM(coalesce(AL."GHI_CO_NGUYEN_TE", 0)
                            - coalesce(AL."GHI_NO_NGUYEN_TE", 0)) AS "SO_TIEN",
                        SUM(coalesce(AL."GHI_CO", 0)
                            - coalesce(AL."GHI_NO", 0))           AS "SO_TIEN_QUY_DOI",
                        (CASE WHEN AL."LOAI_CHUNG_TU" IN
                                (330, 331, 332, 333, 334, 352, 357, 358, 359, 360, 362, 363, 364, 365, 366, 368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
                        THEN 1 /*Với dịch vụ thì chi tiết theo từng hóa đơn*/
                        ELSE 0
                        END)                                     AS "HOA_DON_CHI_TIET",
                        AL."NGAY_HET_HAN",
                        /*Nếu chứng từ Nghiệp vụ khác thì sẽ lấy nhân viên đầu tiên trên form chi tiết*/
                        CASE WHEN GVDT."ID_CHUNG_TU" IS NOT NULL
                        THEN GVDT."NHAN_VIEN_ID"
                        ELSE AL."NHAN_VIEN_ID"
                        END                                       AS "NHAN_VIEN_ID"
                    FROM so_cong_no_chi_tiet AL
                        --          INNER JOIN "danh_muc_loai_chung_tu" RT ON RT.id = AL."LOAI_CHUNG_TU"
                        LEFT JOIN (/*Lấy Nhân viên trên chứng từ nghiệp vụ khác*/
                                    SELECT
                                    AOL."ID_CHUNG_TU",
                                    AOL."DOI_TUONG_ID",
                                    AOL."MA_TK",
                                    AOL."NHAN_VIEN_ID",
                                    ROW_NUMBER()
                                    OVER (
                                        PARTITION BY AOL."ID_CHUNG_TU",
                                        AOL."DOI_TUONG_ID",
                                        AOL."MA_TK"
                                        ORDER BY AOL."THU_TU_TRONG_CHUNG_TU" ) AS RowNumber
                                    FROM so_cong_no_chi_tiet AS AOL
                                    WHERE
                                    AOL."LOAI_CHUNG_TU" IN (4010, 4011, 4012, 4014, 4015, 4018, 4020, 4030)
                                    /*Chỉ lấy theo "LOAI_CHUNG_TU" của bảng GlVoucherDetail
                                    Không lấy các chứng từ Chứng từ bù trừ công nợ, Xử lý chênh lệch tỷ giá từ đánh giá lại tài khoản ngoại tệ, Xử lý chênh lệch tỷ giá từ tính tỷ giá xuất quỹ
                                    */
                                    AND AOL."NHAN_VIEN_ID" IS NOT NULL
                                ) AS GVDT ON GVDT."ID_CHUNG_TU" = AL."ID_CHUNG_TU"
                                            AND GVDT."DOI_TUONG_ID" = AL."DOI_TUONG_ID"
                                            AND GVDT."MA_TK" = AL."MA_TK"
                                            AND GVDT.RowNumber = 1
                        LEFT JOIN (
                                    /* Lấy danh sách chứng từ trả lại giảm giá chọn trực tiếp*/
                                    SELECT "CHUNG_TU_TRA_LAI_HANG_MUA_ID" AS "ID_CHUNG_TU"
                                    FROM purchase_ex_tra_lai_hang_mua_chi_tiet
                                    WHERE "CHUNG_TU_MUA_HANG" IS NOT NULL
                                    UNION
                                    SELECT "GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID" AS "ID_CHUNG_TU"
                                    FROM purchase_ex_giam_gia_hang_mua_chi_tiet
                                    WHERE "CHUNG_TU_MUA_HANG" IS NOT NULL
                                ) SR ON AL."ID_CHUNG_TU" = SR."ID_CHUNG_TU"
                    WHERE (AL."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id ISNULL)
                            AND AL."currency_id" = loai_tien_id
                            AND AL."TK_ID" = (SELECT id
                                            FROM danh_muc_he_thong_tai_khoan
                                            WHERE "SO_TAI_KHOAN" = '331')
                            --           AND AL."CHI_NHANH_ID" = (chi_nhanh_id)
                            AND AL."NGAY_HACH_TOAN" <= den_ngay
                            /* Không lấy các chứng từ Phiếu thu tiền khách hàng, Phiếu thu tiền khách hàng hàng loạt, Phiếu chi trả tiền nhà cung cấp,
                            *  Phiếu thu tiền gửi khách hàng, Phiếu thu tiền gửi khách hàng hàng loạt, Trả tiền nhà cung cấp bằng Ủy nhiệm chi,
                            *  Séc tiền mặt trả tiền nhà cung cấp, Séc chuyển khoản trả tiền nhà cung cấp, Chứng từ xử lý chênh lệch tỷ giá,
                            *  Chứng từ bù trừ công nợ, Xử lý chênh lệch tỷ giá từ đánh giá lại tài khoản ngoại tệ, Xử lý chênh lệch tỷ giá từ tính tỷ giá xuất quỹ*/
                            AND AL."LOAI_CHUNG_TU" NOT IN (1011, 1012, 1021, 1502, 1503, 1511, 1521, 1531, 4013, 4016, 4017)
                            /*Không lấy số dư đầu kỳ do lấy ở trên rồi*/
                            AND AL."LOAI_CHUNG_TU" NOT IN (611, 612, 613, 614, 615, 616, 630)
                            /*Không lấy các chứng từ trả lại, giảm giá*/
                            AND SR."ID_CHUNG_TU" IS NULL

                    GROUP BY AL."ID_CHUNG_TU",
                        AL."MODEL_CHUNG_TU",
                        AL."LOAI_CHUNG_TU",
                        AL."TEN_LOAI_CHUNG_TU",
                        AL."NGAY_CHUNG_TU",
                        AL."NGAY_HACH_TOAN",
                        AL."SO_CHUNG_TU",
                        AL."NGAY_HOA_DON",
                        coalesce(AL."SO_HOA_DON", ''),
                        coalesce(AL."DIEN_GIAI_CHUNG", ''),
                        coalesce(AL."TY_GIA", 1),
                        AL."NGAY_HET_HAN",
                        CASE WHEN GVDT."ID_CHUNG_TU" IS NOT NULL
                        THEN GVDT."NHAN_VIEN_ID"
                        ELSE AL."NHAN_VIEN_ID"
                        END
                    HAVING SUM(coalesce(AL."GHI_CO_NGUYEN_TE", 0)
                                - coalesce(AL."GHI_NO_NGUYEN_TE", 0)) > 0;

                DROP TABLE IF EXISTS TMP_TBALE_3;
                CREATE TEMP TABLE TMP_TBALE_3
                    AS
                    SELECT
                        TEM."ID_CHUNG_TU",
                        TEM."MODEL_CHUNG_TU",
                        TEM."LOAI_CHUNG_TU",
                        TEM."NGAY_CHUNG_TU",
                        TEM."NGAY_HACH_TOAN",
                        TEM."SO_CHUNG_TU",
                        TEM."NGAY_HOA_DON",
                        TEM."SO_HOA_DON",
                        TEM."DIEN_GIAI",
                        TEM."TY_GIA",
                        coalesce(GV."TY_GIA", 0)                                                    AS "TY_GIA_DANH_GIA_LAI",
                        TEM."TONG_TIEN"                                                             AS "SO_TIEN",
                        TEM."TONG_TIEN_QUY_DOI"                                                     AS "SO_TIEN_QUY_DOI",
                        coalesce(TEM."SO_TIEN", 0) - SUM(coalesce(GL."SO_TIEN", 0))                 AS "SO_TIEN_CONG_NO",
                        coalesce(TEM."SO_TIEN_QUY_DOI", 0) - SUM(coalesce(GL."SO_TIEN_QUY_DOI", 0)) AS "SO_TIEN_CONG_NO_QUY_DOI",
                        CAST(0 AS DECIMAL)                                                          AS "SO_TIEN_DOI_TRU",
                        CAST(0 AS DECIMAL)                                                          AS "SO_TIEN_DOI_TRU_QUY_DOI",
                        doi_tuong_id                                                                AS "DOI_TUONG_ID",
                        TEM."HAN_THANH_TOAN",
                        TEM."NHAN_VIEN_ID",
                        E."MA"                                                                      AS "MA_NHAN_VIEN",
                        --nvtoan Modify 22/04/2017: Sửa lỗi 96455
                        E."HO_VA_TEN"                                                               AS "TEN_NHAN_VIEN" --NVTOAN modify 13/04/2017 thực hiện CR 34929
                    FROM (
                            SELECT *
                            FROM TMP_TBALE_1
                            UNION ALL
                            SELECT *
                            FROM TMP_TBALE_2
                        ) AS TEM
                        LEFT JOIN (SELECT *
                                FROM FUNCTION_DOI_TRU_MUA_HANG_CONG_NO('331', loai_tien_id, chi_nhanh_id, doi_tuong_id)) GL
                        ON GL."ID_CHUNG_TU" = TEM."ID_CHUNG_TU" AND GL."MODEL_CHUNG_TU" = TEM."MODEL_CHUNG_TU"
                            AND (TEM."SO_HOA_DON_CHI_TIET" = 0
                                OR (TEM."SO_HOA_DON_CHI_TIET" = 1
                                    AND coalesce(GL."SO_HOA_DON", '') = coalesce(TEM."SO_HOA_DON", '')
                                    AND coalesce(GL."NGAY_HOA_DON", den_ngay) = coalesce(TEM."NGAY_HOA_DON", den_ngay)))
                            AND ((GL."TY_GIA" = TEM."TY_GIA")
                                OR "LOAI_CHUNG_TU" NOT IN
                                    ('611', '612', '613', '614', '615', '616', '630')--nvtoan modify 11/04/2017 Sửa lỗi 90132: Đối với chứng từ không phải số dư đầu thì không join qua "TY_GIA"
                            )
                        LEFT JOIN (
                                    SELECT
                                    CASE WHEN '15' = '15'
                                        THEN coalesce(GV."TY_GIA", 1)
                                    ELSE coalesce(GV."TY_GIA", 1)
                                    END                                                          AS "TY_GIA",
                                    /* NBHIEU 12/05/2016 (bug 102978) Lấy tỷ giá đánh giá lại dưới chi tiết nếu là quyết dịnh 15*/
                                    GVD."ID_CHUNG_TU_GOC"                                        AS "ID_CHUNG_TU",
                                    ROW_NUMBER()
                                    OVER (
                                        PARTITION BY GVD."ID_CHUNG_TU_GOC"
                                        ORDER BY GVD."ID_CHUNG_TU_GOC", GV."NGAY_HACH_TOAN" DESC ) AS RowNumber
                                    FROM account_ex_chung_tu_nghiep_vu_khac GV
                                    INNER JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan GVD
                                        ON GVD."ID_CHUNG_TU_GOC" = GV.id
                                    WHERE
                                    --                                     GV."CHI_NHANH_ID" = (chi_nhanh_id) AND
                                    GV.currency_id = loai_tien_id
                                    AND GVD."TK_CONG_NO_ID" = (SELECT id
                                                                FROM danh_muc_he_thong_tai_khoan
                                                                WHERE "SO_TAI_KHOAN" = '331')
                                    AND (GVD."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id ISNULL)
                                    AND GV.state = 'da_ghi_so'
                                ) AS GV ON TEM."ID_CHUNG_TU" = GV."ID_CHUNG_TU"
                                            AND GV.RowNumber = 1
                        LEFT JOIN res_partner E ON TEM."NHAN_VIEN_ID" = E.id --NVTOAN modify 13/04/2017 thực hiện CR 34929
                    GROUP BY TEM."ID_CHUNG_TU",
                        TEM."MODEL_CHUNG_TU",
                        TEM."LOAI_CHUNG_TU",
                        TEM."NGAY_CHUNG_TU",
                        TEM."NGAY_HACH_TOAN",
                        TEM."SO_CHUNG_TU",
                        TEM."NGAY_HOA_DON",
                        TEM."SO_HOA_DON",
                        TEM."DIEN_GIAI",
                        TEM."TY_GIA",
                        coalesce(GV."TY_GIA", 0),
                        TEM."SO_TIEN",
                        TEM."SO_TIEN_QUY_DOI",
                        TEM."TONG_TIEN",
                        TEM."TONG_TIEN_QUY_DOI",
                        TEM."HAN_THANH_TOAN",
                        TEM."NHAN_VIEN_ID",
                        E."MA", --nvtoan Modify 22/04/2017: Sửa lỗi 96455
                        E."HO_VA_TEN" --NVTOAN modify 13/04/2017 thực hiện CR 34929
                    HAVING coalesce(TEM."SO_TIEN", 0) - SUM(coalesce(GL."SO_TIEN", 0)) > 0
                    ORDER BY TEM."NGAY_CHUNG_TU",
                        TEM."NGAY_HACH_TOAN",
                        TEM."SO_CHUNG_TU",
                        TEM."NGAY_HOA_DON",
                        TEM."SO_HOA_DON";

                END $$;

                SELECT *
                FROM TMP_TBALE_3
        

        """  
        
        
        return self.execute(query, params)


    # @api.depends('SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_IDS.AUTO_SELECT')
    # def doi_tru_chung_tu_thanh_toan(self):
    #     tong_tien_thanh_toan = 0
    #     tong_tien_cong_no = 0
    #     for line in self.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_IDS:
    #         if line.AUTO_SELECT == True:
    #             tong_tien_thanh_toan += line.SO_CHUA_DOI_TRU
    #     for line in self.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_IDS:
    #         if line.AUTO_SELECT == True:
    #             tong_tien_cong_no += line.SO_CON_NO
    #     if tong_tien_cong_no > 0 and tong_tien_thanh_toan > 0:
    #         if tong_tien_thanh_toan > tong_tien_cong_no:
    #             for line in self.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_IDS:
    #                 if line.AUTO_SELECT == True:
    #                     line.SO_TIEN_DOI_TRU = line.SO_CON_NO
    #             for line1 in self.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_IDS:
    #                 if line1.AUTO_SELECT == True:
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
    #             for line1 in self.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_IDS:
    #                 if line1.AUTO_SELECT == True:
    #                     # if line1.SO_CHUA_DOI_TRU > tong_tien_cong_no:
    #                     #     line1.SO_TIEN_DOI_TRU = tong_tien_cong_no
    #                     #     tong_tien_cong_no = 0
    #                     line1.SO_TIEN_DOI_TRU = line1.SO_TIEN

    #             for line in self.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_IDS:
    #                 if line.AUTO_SELECT == True:
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

    # @api.depends('SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_IDS.AUTO_SELECT')
    # def doi_tru_cong_no(self):
    #     tong_tien_thanh_toan = 0
    #     tong_tien_cong_no = 0
    #     for line in self.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_IDS:
    #         if line.AUTO_SELECT == True:
    #             tong_tien_thanh_toan += line.SO_CHUA_DOI_TRU
    #     for line in self.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_IDS:
    #         if line.AUTO_SELECT == True:
    #             tong_tien_cong_no += line.SO_CON_NO
    #     if tong_tien_cong_no > 0 and tong_tien_thanh_toan > 0:
    #         if tong_tien_thanh_toan > tong_tien_cong_no:
    #             for line in self.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_IDS:
    #                 if line.AUTO_SELECT == True:
    #                     line.SO_TIEN_DOI_TRU = line.SO_CON_NO
    #             for line1 in self.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_IDS:
    #                 if line1.AUTO_SELECT == True:
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
    #             for line1 in self.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_IDS:
    #                 if line1.AUTO_SELECT == True:
    #                     # if line1.SO_CHUA_DOI_TRU > tong_tien_cong_no:
    #                     #     line1.SO_TIEN_DOI_TRU = tong_tien_cong_no
    #                     #     tong_tien_cong_no = 0
    #                     line1.SO_TIEN_DOI_TRU = line1.SO_TIEN

    #             for line in self.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_IDS:
    #                 if line.AUTO_SELECT == True:
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

    
    
    def doi_tru_chung_tu(self, args):
        # result = super(SALE_EX_DOI_TRU_CHUNG_TU, self).create(values)
        so_tien_doi_tru = 0
        dict_doi_tru_chi_tiet = {}
        if self.LOAI_DOI_TRU == '1' and self.IS_TY_GIA == False:
            if self.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_IDS and self.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_IDS:
                for ct_thanh_toan in self.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_THANH_TOAN_IDS:
                    if ct_thanh_toan.AUTO_SELECT == True:
                        for ct_cong_no in self.SALE_EX_DOI_TRU_CHUNG_TU_CHI_TIET_CONG_NO_IDS:
                            if ct_cong_no.AUTO_SELECT == True:
                                if ct_thanh_toan.SO_TIEN_DOI_TRU > ct_cong_no.SO_TIEN_DOI_TRU:
                                    so_tien_doi_tru = ct_cong_no.SO_TIEN_DOI_TRU
                                elif ct_thanh_toan.SO_TIEN_DOI_TRU == ct_cong_no.SO_TIEN_DOI_TRU:
                                    so_tien_doi_tru = ct_cong_no.SO_TIEN_DOI_TRU
                                else:
                                    so_tien_doi_tru = ct_thanh_toan.SO_TIEN_DOI_TRU
                                ct_cong_no.SO_TIEN_DOI_TRU = ct_cong_no.SO_TIEN_DOI_TRU - so_tien_doi_tru
                                ct_thanh_toan.SO_TIEN_DOI_TRU = ct_thanh_toan.SO_TIEN_DOI_TRU - so_tien_doi_tru
                                dict_doi_tru_chi_tiet = {
                                    'NGAY_CHUNG_TU_THANH_TOAN' : ct_thanh_toan.NGAY_CHUNG_TU,
                                    'NGAY_HACH_TOAN_THANH_TOAN' : ct_thanh_toan.NGAY_HACH_TOAN,
                                    'SO_CHUNG_TU_THANH_TOAN' : ct_thanh_toan.SO_CHUNG_TU,
                                    'SO_TIEN_THANH_TOAN': ct_thanh_toan.SO_CHUA_DOI_TRU,
                                    'SO_TIEN_THANH_TOAN_QUY_DOI': ct_thanh_toan.SO_CHUA_DOI_TRU_QUY_DOI,
                                    'LOAI_CHUNG_TU_THANH_TOAN' : ct_thanh_toan.LOAI_CHUNG_TU,
                                    'ID_CHUNG_TU_THANH_TOAN' : ct_thanh_toan.ID_CHUNG_TU_THANH_TOAN,
                                    'MODEL_CHUNG_TU_THANH_TOAN' : ct_thanh_toan.MODEL_CHUNG_TU_THANH_TOAN,
                                    'SO_CHUA_THANH_TOAN' : ct_thanh_toan.SO_TIEN,
                                    'SO_CHUA_THANH_TOAN_QUY_DOI' : ct_thanh_toan.SO_TIEN_QUY_DOI,
                                    'SO_THANH_TOAN_LAN_NAY' : so_tien_doi_tru,
                                    'SO_THANH_TOAN_LAN_NAY_QUY_DOI' : so_tien_doi_tru,

                                    'ID_CHUNG_TU_CONG_NO' : ct_cong_no.ID_CHUNG_TU_CONG_NO,
                                    'MODEL_CHUNG_TU_CONG_NO' : ct_cong_no.MODEL_CHUNG_TU_CONG_NO,
                                    'NGAY_CHUNG_TU_CONG_NO' : ct_cong_no.NGAY_CHUNG_TU,
                                    'NGAY_HOA_DON_CONG_NO' : ct_cong_no.NGAY_HOA_DON,
                                    'NGAY_HACH_TOAN_CONG_NO' : ct_cong_no.NGAY_HACH_TOAN,
                                    'SO_CHUNG_TU_CONG_NO' : ct_cong_no.SO_CHUNG_TU,
                                    'SO_HOA_DON_CONG_NO' : ct_cong_no.SO_HOA_DON,
                                    'SO_TIEN_CONG_NO' : ct_cong_no.SO_TIEN,
                                    'SO_TIEN_CONG_NO_QUY_DOI' : ct_cong_no.SO_TIEN,
                                    'SO_CONG_NO_THANH_TOAN_LAN_NAY' : so_tien_doi_tru,
                                    'SO_CONG_NO_THANH_TOAN_LAN_NAY_QUY_DOI' : so_tien_doi_tru,
                                    'SO_TIEN_CON_NO' : ct_cong_no.SO_TIEN,
                                    'SO_TIEN_CON_NO_QUY_DOI' : ct_cong_no.SO_TIEN_QUY_DOI,
                                    'TAI_KHOAN_ID' : self.TAI_KHOAN_PHAI_THU_ID.id,
                                    'LOAI_CHUNG_TU_CONG_NO' : ct_cong_no.LOAI_CHUNG_TU,
                                    'TY_GIA_CONG_NO' : ct_cong_no.TY_GIA,
                                    'DOI_TUONG_ID' : self.DOI_TUONG_ID.id,
                                    'currency_id' : self.currency_id.id,
                                    'LOAI_DOI_TRU' : '1',
                                    'CTCN_DA_GHI_SO' : True,
                                    'CTTT_DA_GHI_SO' : True,
                                    'CHI_NHANH_ID' : self.get_chi_nhanh(),
                                }
                                self.env['sale.ex.doi.tru.chi.tiet'].create(dict_doi_tru_chi_tiet)
                                if ct_thanh_toan.SO_TIEN_DOI_TRU == 0:
                                    break

                                











    @api.model_cr
    def init(self):
        self.env.cr.execute(""" 
			-- DROP FUNCTION LAY_SO_TIEN_TU_CHUNG_TU_CONG_NO(IN ma_tai_khoan VARCHAR(50),loai_tien_id INTEGER,chi_nhanh_id INTEGER,doi_tuong_id INTEGER)
            CREATE OR REPLACE FUNCTION FUNCTION_DOI_TRU_CHUNG_TU_BAN_HANG_THANH_TOAN(IN ma_tai_khoan VARCHAR(50),
                                                                                        loai_tien_id INTEGER, chi_nhanh_id INTEGER,
                                                                                        doi_tuong_id INTEGER)
            RETURNS TABLE("ID_CHUNG_TU"     INTEGER,
                            "MODEL_CHUNG_TU"  VARCHAR(50),
                            "NGAY_CHUNG_TU"   DATE,
                            "SO_CHUNG_TU"     VARCHAR(20),
                            "DOI_TUONG_ID"    INTEGER,
                            "SO_TAI_KHOAN"    VARCHAR(50),
                            "SO_TIEN"         FLOAT,
                            "SO_TIEN_QUY_DOI" FLOAT
            ) AS $$
            DECLARE

            BEGIN

            DROP TABLE IF EXISTS TBL_KET_QUA;
            CREATE TEMP TABLE TBL_KET_QUA (
                "ID_CHUNG_TU"     INTEGER,
                "MODEL_CHUNG_TU"  VARCHAR(50),
                "NGAY_CHUNG_TU"   DATE,
                "SO_CHUNG_TU"     VARCHAR(20),
                "DOI_TUONG_ID"    INTEGER,
                "SO_TAI_KHOAN"    VARCHAR(50),
                "SO_TIEN"         FLOAT,
                "SO_TIEN_QUY_DOI" FLOAT
            );
            INSERT INTO TBL_KET_QUA (
                SELECT
                A."ID_CHUNG_TU",
                A."MODEL_CHUNG_TU",
                A."NGAY_CHUNG_TU",
                A."SO_CHUNG_TU",
                A."DOI_TUONG_ID",
                A."SO_TAI_KHOAN",
                SUM(coalesce(A."SO_TIEN", 0))         AS "SO_TIEN",
                SUM(coalesce(A."SO_TIEN_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI"
                FROM (

                    SELECT
                        CAST(GL."ID_CHUNG_TU_THANH_TOAN" AS INTEGER)                          AS "ID_CHUNG_TU",
                        GL."MODEL_CHUNG_TU_THANH_TOAN"                                        AS "MODEL_CHUNG_TU",
                        GL."NGAY_CHUNG_TU_THANH_TOAN"                                         AS "NGAY_CHUNG_TU",
                        GL."SO_CHUNG_TU_THANH_TOAN"                                           AS "SO_CHUNG_TU",
                        Gl."DOI_TUONG_ID"                                                     AS "DOI_TUONG_ID",
                        TA."SO_TAI_KHOAN",
                        SUM(coalesce(GL."SO_THANH_TOAN_LAN_NAY", 0))                             AS "SO_TIEN",
                        SUM(coalesce(GL."SO_THANH_TOAN_LAN_NAY_QUY_DOI", 0)) - SUM((CASE WHEN GL."LOAI_DOI_TRU" = '1'
                        THEN 0
                                                                                ELSE coalesce(
                                                                                    GL."CHENH_LECH_TY_GIA_SO_TIEN_QUY_DOI",
                                                                                    0) END)) AS "SO_TIEN_QUY_DOI"
                    FROM sale_ex_doi_tru_chi_tiet GL
                        INNER JOIN (
                                    SELECT *
                                    FROM danh_muc_he_thong_tai_khoan A
                                    WHERE A."SO_TAI_KHOAN" = '131'
                                    ) TA ON TA.id = GL."TAI_KHOAN_ID"
                    WHERE
                        GL."currency_id" = loai_tien_id
                        AND GL."CHI_NHANH_ID" = chi_nhanh_id
                        AND GL."CTTT_DA_GHI_SO" = TRUE AND GL."CTCN_DA_GHI_SO" = TRUE
                        AND (GL."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id IS NULL)
                    GROUP BY GL."ID_CHUNG_TU_THANH_TOAN", GL."DOI_TUONG_ID", TA."SO_TAI_KHOAN", GL."NGAY_CHUNG_TU_THANH_TOAN",
                        GL."SO_CHUNG_TU_THANH_TOAN", GL."MODEL_CHUNG_TU_THANH_TOAN"


                    UNION ALL


                    SELECT
                        cast(GLD."ID_CHUNG_TU_GOC" AS INTEGER),
                        GLD."MODEL_CHUNG_TU_GOC"           AS "MODEL_CHUNG_TU",
                        GL."NGAY_CHUNG_TU"                 AS "NGAY_CHUNG_TU",
                        GL."SO_CHUNG_TU"                   AS "SO_CHUNG_TU",
                        GLD."DOI_TUONG_ID",
                        TA."SO_TAI_KHOAN",
                        0                                  AS "SO_TIEN",
                        SUM(coalesce(GLD."CHENH_LECH", 0)) AS "SO_TIEN_QUY_DOI"
                    FROM account_ex_chung_tu_nghiep_vu_khac GL
                        INNER JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan GLD ON GLD."ID_CHUNG_TU_GOC" = GL.id
                        INNER JOIN (
                                    SELECT *
                                    FROM danh_muc_he_thong_tai_khoan A
                                    WHERE A."SO_TAI_KHOAN" = '131'
                                    ) TA ON GLD."TK_CONG_NO_ID" = TA.id
                    WHERE
                        GL.currency_id = loai_tien_id
                        AND Gl."CHI_NHANH_ID" = chi_nhanh_id
                        AND (GLD."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id IS NULL)
                    GROUP BY GLD."ID_CHUNG_TU_GOC",
                        GLD."MODEL_CHUNG_TU_GOC",
                        GLD."DOI_TUONG_ID"
                        , TA."SO_TAI_KHOAN"
                        , GL."NGAY_CHUNG_TU"
                        , GL."SO_CHUNG_TU"


                    UNION ALL


                    SELECT
                        SAD."CHUNG_TU_BAN_HANG_ID"                      AS "ID_CHUNG_TU",
                        'sale.document'                                 AS "MODEL_CHUNG_TU",
                        SA."NGAY_CHUNG_TU"                              AS "NGAY_CHUNG_TU",
                        SA."SO_CHUNG_TU"                                AS "SO_CHUNG_TU",
                        SA."DOI_TUONG_ID",
                        TA."SO_TAI_KHOAN",
                        SUM(coalesce(SAD."THANH_TIEN", 0) + coalesce(SAD."TIEN_THUE_GTGT", 0) -
                            coalesce(SAD."TIEN_CHIET_KHAU", 0))         AS "SO_TIEN",
                        SUM(coalesce(SAD."THANH_TIEN_QUY_DOI", 0) + coalesce(SAD."TIEN_THUE_GTGT_QUY_DOI", 0) -
                            coalesce(SAD."TIEN_CHIET_KHAU_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI"
                    FROM sale_ex_tra_lai_hang_ban SA
                        INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet SAD ON SAD."TRA_LAI_HANG_BAN_ID" = SA.id
                        INNER JOIN (
                                    SELECT *
                                    FROM danh_muc_he_thong_tai_khoan A
                                    WHERE A."SO_TAI_KHOAN" = '131'
                                    ) TA ON SAD."TK_CO_ID" = TA.id
                    WHERE
                        SA.currency_id = loai_tien_id
                        AND SA."CHI_NHANH_ID" = chi_nhanh_id
                        AND SAD."CHUNG_TU_BAN_HANG_ID" IS NOT NULL
                        AND (SA."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id IS NULL)
                    GROUP BY SAD."CHUNG_TU_BAN_HANG_ID", SA."DOI_TUONG_ID", TA."SO_TAI_KHOAN"
                        , SA."NGAY_CHUNG_TU"
                        , SA."SO_CHUNG_TU"

                    UNION ALL

                    SELECT
                        SAD."CHUNG_TU_BAN_HANG_ID"                      AS "ID_CHUNG_TU",
                        'sale.document'                                 AS "MODEL_CHUNG_TU",
                        SA."NGAY_CHUNG_TU"                              AS "NGAY_CHUNG_TU",
                        SA."SO_CHUNG_TU"                                AS "SO_CHUNG_TU",
                        SA."DOI_TUONG_ID",
                        TA."SO_TAI_KHOAN",
                        SUM(coalesce(SAD."THANH_TIEN", 0) + coalesce(SAD."TIEN_THUE_GTGT", 0) -
                            coalesce(SAD."TIEN_CHIET_KHAU", 0))         AS "SO_TIEN",
                        SUM(coalesce(SAD."THANH_TIEN_QUY_DOI", 0) + coalesce(SAD."TIEN_THUE_GTGT_QUY_DOI", 0) -
                            coalesce(SAD."TIEN_CHIET_KHAU_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI"
                    FROM sale_ex_giam_gia_hang_ban SA
                        INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban SAD ON SAD."GIAM_GIA_HANG_BAN_ID" = SA.id
                        INNER JOIN (
                                    SELECT *
                                    FROM danh_muc_he_thong_tai_khoan A
                                    WHERE A."SO_TAI_KHOAN" = '131'
                                    ) TA ON SAD."TK_CO_ID" = TA.id
                    WHERE
                        SA.currency_id = loai_tien_id
                        AND SA."CHI_NHANH_ID" = chi_nhanh_id
                        AND SAD."CHUNG_TU_BAN_HANG_ID" IS NOT NULL
                        AND (SA."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id IS NULL)
                    GROUP BY SAD."CHUNG_TU_BAN_HANG_ID", SA."DOI_TUONG_ID", TA."SO_TAI_KHOAN"
                        , SA."NGAY_CHUNG_TU"
                        , SA."SO_CHUNG_TU") A
                GROUP BY
                A."ID_CHUNG_TU",
                A."MODEL_CHUNG_TU",
                A."NGAY_CHUNG_TU",
                A."SO_CHUNG_TU",
                A."DOI_TUONG_ID",
                A."SO_TAI_KHOAN"
            );
            RETURN QUERY SELECT *
                        FROM TBL_KET_QUA;
            END;
            $$ LANGUAGE PLpgSQL;
		""")

        self.env.cr.execute(""" 
			-- DROP FUNCTION LAY_SO_TIEN_CHUNG_TU_BAN_HANG_CONG_NO(IN ma_tai_khoan VARCHAR(50),loai_tien_id INTEGER,chi_nhanh_id INTEGER,doi_tuong_id INTEGER)
                CREATE OR REPLACE FUNCTION FUNCTION_DOI_TRU_CHUNG_TU_BAN_HANG_CONG_NO(IN ma_tai_khoan VARCHAR(50), loai_tien_id INTEGER,
                                                                                    chi_nhanh_id INTEGER, doi_tuong_id INTEGER)
                RETURNS TABLE("ID_CHUNG_TU"     INTEGER,
                                "MODEL_CHUNG_TU" VARCHAR(50),
                                "DOI_TUONG_ID"    INTEGER,
                                "SO_TAI_KHOAN"    VARCHAR(50),
                                "NGAY_HOA_DON"    DATE,
                                "SO_HOA_DON"      VARCHAR(20),
                                "SO_TIEN"         FLOAT,
                                "SO_TIEN_QUY_DOI" FLOAT,
                                "TY_GIA"          FLOAT
                ) AS $$
                DECLARE

                BEGIN

                DROP TABLE IF EXISTS TBL_KET_QUA;
                CREATE TEMP TABLE TBL_KET_QUA (
                    "ID_CHUNG_TU"     INTEGER,
                    "MODEL_CHUNG_TU" VARCHAR(50),
                    "DOI_TUONG_ID"    INTEGER,
                    "SO_TAI_KHOAN"    VARCHAR(50),
                    "NGAY_HOA_DON"    DATE,
                    "SO_HOA_DON"      VARCHAR(20),
                    "SO_TIEN"         FLOAT,
                    "SO_TIEN_QUY_DOI" FLOAT,
                    "TY_GIA"          FLOAT
                );
                INSERT INTO TBL_KET_QUA (
                    SELECT
                    A."ID_CHUNG_TU",
                    A."MODEL_CHUNG_TU",
                    A."DOI_TUONG_ID",
                    A."SO_TAI_KHOAN",
                    A."NGAY_HOA_DON",
                    A."SO_HOA_DON",
                    SUM(coalesce(A."SO_TIEN", 0))         AS "SO_TIEN",
                    SUM(coalesce(A."SO_TIEN_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI",
                    A."TY_GIA"
                    FROM (
                        SELECT
                            cast(GL."ID_CHUNG_TU_CONG_NO" AS INTEGER)      AS "ID_CHUNG_TU",
                            GL."MODEL_CHUNG_TU_CONG_NO"                    AS "MODEL_CHUNG_TU",
                            Gl."DOI_TUONG_ID"                              AS "DOI_TUONG_ID",
                            TA."SO_TAI_KHOAN",
                            (CASE WHEN GL."LOAI_CHUNG_TU_CONG_NO" IN
                                        (610, 612, 613, 614, 620, 330, 331, 332, 333, 334, 352, 357, 358, 359, 360, 362, 363, 364, 365, 366, 368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
                            THEN GL."NGAY_HOA_DON_CONG_NO"
                            ELSE NULL
                            END)                                          AS "NGAY_HOA_DON",
                            (CASE WHEN GL."LOAI_CHUNG_TU_CONG_NO" IN (610, 612,
                                                                            613, 614, 620,
                                                                            330, 331, 332,
                                                                            333, 334, 352,
                            357, 358, 359, 360, 362, 363, 364, 365, 366, 368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
                            THEN coalesce(GL."SO_HOA_DON_CONG_NO", '')
                            ELSE NULL
                            END)                                          AS "SO_HOA_DON",
                            SUM(coalesce(GL."SO_CONG_NO_THANH_TOAN_LAN_NAY", 0))         AS "SO_TIEN",
                            SUM(coalesce(GL."SO_CONG_NO_THANH_TOAN_LAN_NAY_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI",
                            GL."TY_GIA_CONG_NO"                            AS "TY_GIA"
                        FROM sale_ex_doi_tru_chi_tiet GL
                            INNER JOIN (SELECT *
                                        FROM danh_muc_he_thong_tai_khoan A
                                        WHERE A."SO_TAI_KHOAN" = '131') TA ON TA.id = GL."TAI_KHOAN_ID"
                        WHERE GL."currency_id" = loai_tien_id
                                AND GL."CHI_NHANH_ID" = chi_nhanh_id
                                AND GL."CTTT_DA_GHI_SO" = TRUE
                                AND GL."CTCN_DA_GHI_SO" = TRUE
                                AND (GL."DOI_TUONG_ID" = doi_tuong_id
                                    OR doi_tuong_id IS NULL
                                )
                        GROUP BY GL."ID_CHUNG_TU_CONG_NO",
                            GL."MODEL_CHUNG_TU_CONG_NO",
                            GL."DOI_TUONG_ID",
                            TA."SO_TAI_KHOAN",
                            GL."SO_HOA_DON_CONG_NO",
                            GL."NGAY_HOA_DON_CONG_NO",
                            GL."LOAI_CHUNG_TU_CONG_NO"
                            , GL."TY_GIA_CONG_NO"


                        UNION ALL


                        SELECT
                            GLD."ID_CHUNG_TU_GOC",
                            GLD."MODEL_CHUNG_TU_GOC"                  AS "MODEL_CHUNG_TU",
                            GLD."DOI_TUONG_ID",
                            TA."SO_TAI_KHOAN",
                            (CASE WHEN GLD."LOAI_CHUNG_TU" IN
                                        ('610', '612', '613', '614', '620', '330', '331', '332', '333', '334', '352', '357', '358', '359', '360', '362', '363', '364', '365', '366', '368', '369', '370', '371', '372', '374', '375', '376', '377', '378')
                            THEN GL."NGAY_CHUNG_TU"
                            ELSE NULL
                            END)                                     AS "NGAY_HOA_DON",
                            (CASE WHEN GLD."LOAI_CHUNG_TU" IN
                                        ('610', '612', '613', '614', '620', '330', '331', '332', '333', '334', '352', '357', '358', '359', '360', '362', '363', '364', '365', '366', '368', '369', '370', '371', '372', '374', '375', '376', '377', '378')
                            THEN coalesce(GL."SO_HOA_DON", '')
                            ELSE NULL
                            END)                                     AS "SO_HOA_DON",
                            0                                         AS "SO_TIEN",
                            (-1) * SUM(coalesce(GLD."CHENH_LECH", 0)) AS "SO_TIEN_QUY_DOI",
                            GL."TY_GIA"
                        FROM account_ex_chung_tu_nghiep_vu_khac GL
                            INNER JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan GLD ON GLD."CHUNG_TU_NGHIEP_VU_KHAC_ID" = GL.id
                            INNER JOIN (SELECT *
                                        FROM danh_muc_he_thong_tai_khoan A
                                        WHERE A."SO_TAI_KHOAN" = '131') TA ON GLD."TK_CONG_NO_ID" = TA.id
                        WHERE GL.currency_id = loai_tien_id
                                AND Gl."CHI_NHANH_ID" = chi_nhanh_id
                                AND (GLD."DOI_TUONG_ID" = doi_tuong_id
                                    OR doi_tuong_id IS NULL
                                )
                        GROUP BY GLD."ID_CHUNG_TU_GOC",
                            GLD."MODEL_CHUNG_TU_GOC",
                            GLD."DOI_TUONG_ID",
                            TA."SO_TAI_KHOAN",
                            GL."NGAY_CHUNG_TU",
                            GL."NGAY_HOA_DON",
                            GLD."LOAI_CHUNG_TU"
                            , GL."TY_GIA",
                            GL."SO_HOA_DON"

                        UNION ALL

                        SELECT
                            SAD."SO_CHUNG_TU_ID"                        AS "ID_CHUNG_TU",
                            'sale.document'                                   AS "MODEL_CHUNG_TU",
                            SA."DOI_TUONG_ID",
                            TA."SO_TAI_KHOAN",
                            NULL                                              AS "NGAY_HOA_DON",
                            NULL                                              AS "SO_HOA_DON",
                            SUM(coalesce(SAD."THANH_TIEN", 0)
                                + coalesce(SAD."TIEN_THUE_GTGT", 0)
                                - coalesce(SAD."TIEN_CHIET_KHAU", 0))         AS "SO_TIEN",
                            SUM(coalesce(SAD."THANH_TIEN_QUY_DOI", 0)
                                + coalesce(SAD."TIEN_THUE_GTGT_QUY_DOI", 0)
                                - coalesce(SAD."TIEN_CHIET_KHAU_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI",
                            SA."TY_GIA"
                        FROM sale_ex_tra_lai_hang_ban SA
                            INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet SAD ON SAD."TRA_LAI_HANG_BAN_ID" = SA.id
                            INNER JOIN (SELECT *
                                        FROM danh_muc_he_thong_tai_khoan A
                                        WHERE A."SO_TAI_KHOAN" = '131') TA ON SAD."TK_CO_ID" = TA.id
                        WHERE SA.currency_id = loai_tien_id
                                AND SA."CHI_NHANH_ID" = chi_nhanh_id
                                AND SA.state = 'da_ghi_so'
                                AND SAD."SO_CHUNG_TU_ID" IS NOT NULL
                                AND (SA."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id IS NULL)
                        GROUP BY SAD."SO_CHUNG_TU_ID",
                            SA."DOI_TUONG_ID",
                            TA."SO_TAI_KHOAN"
                            , SA."TY_GIA"


                        UNION ALL

                        SELECT
                            SAD."CHUNG_TU_BAN_HANG_ID"                        AS "ID_CHUNG_TU",
                            'sale.document'                                   AS "MODEL_CHUNG_TU",
                            SA."DOI_TUONG_ID",
                            TA."SO_TAI_KHOAN",
                            NULL                                              AS "NGAY_HOA_DON",
                            NULL                                              AS "SO_HOA_DON",
                            SUM(coalesce(SAD."THANH_TIEN", 0)
                                + coalesce(SAD."TIEN_THUE_GTGT", 0)
                                - coalesce(SAD."TIEN_CHIET_KHAU", 0))         AS "SO_TIEN",
                            SUM(coalesce(SAD."THANH_TIEN_QUY_DOI", 0)
                                + coalesce(SAD."TIEN_THUE_GTGT_QUY_DOI", 0)
                                - coalesce(SAD."TIEN_CHIET_KHAU_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI",
                            SA."TY_GIA"
                        FROM sale_ex_giam_gia_hang_ban SA
                            INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban SAD ON SAD."GIAM_GIA_HANG_BAN_ID" = SA.id
                            INNER JOIN (SELECT *
                                        FROM danh_muc_he_thong_tai_khoan A
                                        WHERE A."SO_TAI_KHOAN" = '131') TA ON SAD."TK_CO_ID" = TA.id
                        WHERE SA.currency_id = loai_tien_id
                                AND SA."CHI_NHANH_ID" = chi_nhanh_id
                                AND SA.state = 'da_ghi_so'
                                AND SAD."CHUNG_TU_BAN_HANG_ID" IS NOT NULL
                                AND (SA."DOI_TUONG_ID" = doi_tuong_id
                                    OR doi_tuong_id IS NULL
                                )
                        GROUP BY SAD."CHUNG_TU_BAN_HANG_ID",
                            SA."DOI_TUONG_ID",
                            TA."SO_TAI_KHOAN"
                            , SA."TY_GIA") A
                    GROUP BY
                    A."ID_CHUNG_TU",
                    A."MODEL_CHUNG_TU",
                    A."DOI_TUONG_ID",
                    A."SO_TAI_KHOAN",
                    A."NGAY_HOA_DON",
                    A."SO_HOA_DON",
                    A."TY_GIA"
                );
                RETURN QUERY SELECT *
                            FROM TBL_KET_QUA;
                END;
                $$ LANGUAGE PLpgSQL;
		""")

        self.env.cr.execute(""" 
			-- DROP FUNCTION FUNCTION_DOI_TRU_MUA_HANG_THANH_TOAN(IN ma_tai_khoan VARCHAR(50),loai_tien_id INTEGER,chi_nhanh_id INTEGER,doi_tuong_id INTEGER)
            CREATE OR REPLACE FUNCTION FUNCTION_DOI_TRU_MUA_HANG_THANH_TOAN(IN ma_tai_khoan VARCHAR(50), loai_tien_id INTEGER,
                                                                                chi_nhanh_id INTEGER, doi_tuong_id INTEGER)
            RETURNS TABLE("ID_CHUNG_TU"     INTEGER,
                            "MODEL_CHUNG_TU"  VARCHAR(50),
                            "DOI_TUONG_ID"    INTEGER,
                            "SO_TAI_KHOAN"    VARCHAR(50),
                            "NGAY_CHUNG_TU"    DATE,
                            "SO_CHUNG_TU"      VARCHAR(20),
                            "SO_TIEN"         FLOAT,
                            "SO_TIEN_QUY_DOI" FLOAT,
                            "TY_GIA"          FLOAT
            ) AS $$
            DECLARE

            BEGIN

            DROP TABLE IF EXISTS TBL_KET_QUA;
            CREATE TEMP TABLE TBL_KET_QUA (
                "ID_CHUNG_TU"     INTEGER,
                "MODEL_CHUNG_TU"  VARCHAR(50),
                "DOI_TUONG_ID"    INTEGER,
                "SO_TAI_KHOAN"    VARCHAR(50),
                "NGAY_CHUNG_TU"    DATE,
                "SO_CHUNG_TU"      VARCHAR(20),
                "SO_TIEN"         FLOAT,
                "SO_TIEN_QUY_DOI" FLOAT,
                "TY_GIA"          FLOAT
            );
            INSERT INTO TBL_KET_QUA (
                SELECT
                A."ID_CHUNG_TU",
                A."MODEL_CHUNG_TU",
                A."DOI_TUONG_ID",
                A."SO_TAI_KHOAN",
                A."NGAY_CHUNG_TU",
                A."SO_CHUNG_TU",
                sum(coalesce(a."SO_TIEN"))         AS "SO_TIEN",
                sum(coalesce(a."SO_TIEN_QUY_DOI")) AS "SO_TIEN_QUY_DOI"
                FROM (
                    SELECT
                        CAST(GL."ID_CHUNG_TU_THANH_TOAN" AS INTEGER)                          AS "ID_CHUNG_TU",
                        "MODEL_CHUNG_TU_THANH_TOAN"                                           AS "MODEL_CHUNG_TU",
                        GL."NGAY_CHUNG_TU_THANH_TOAN"                                        AS "NGAY_CHUNG_TU",
                        coalesce(GL."SO_CHUNG_TU_THANH_TOAN", '')                             AS "SO_CHUNG_TU",
                        Gl."DOI_TUONG_ID"                                                     AS "DOI_TUONG_ID",
                        TA."SO_TAI_KHOAN",
                        SUM(coalesce(GL."SO_THANH_TOAN_LAN_NAY", 0))                             AS "SO_TIEN",
                        SUM(coalesce(GL."SO_THANH_TOAN_LAN_NAY_QUY_DOI", 0)) - SUM((CASE WHEN GL."LOAI_DOI_TRU" = '1'
                        THEN 0
                                                                                ELSE coalesce(
                                                                                    GL."CHENH_LECH_TY_GIA_SO_TIEN_QUY_DOI",
                                                                                    0) END)) AS "SO_TIEN_QUY_DOI"
                    FROM sale_ex_doi_tru_chi_tiet GL
                        INNER JOIN (
                                    SELECT *
                                    FROM danh_muc_he_thong_tai_khoan AC
                                    WHERE AC."SO_TAI_KHOAN" = ma_tai_khoan
                                    ) TA ON TA.id = GL."TAI_KHOAN_ID"
                    WHERE
                        GL."currency_id" = loai_tien_id
                        AND GL."CHI_NHANH_ID" = chi_nhanh_id
                        AND GL."CTTT_DA_GHI_SO" = TRUE AND GL."CTCN_DA_GHI_SO" = TRUE
                        AND (GL."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id IS NULL)
                    GROUP BY GL."ID_CHUNG_TU_THANH_TOAN", GL."DOI_TUONG_ID", TA."SO_TAI_KHOAN",
                        GL."NGAY_CHUNG_TU_THANH_TOAN", GL."SO_CHUNG_TU_THANH_TOAN", "ID_CHUNG_TU_CONG_NO",
                        "NGAY_HACH_TOAN_THANH_TOAN", "SO_CHUNG_TU_CONG_NO", GL."MODEL_CHUNG_TU_THANH_TOAN"


                    UNION ALL


                    SELECT
                        cast(GLD."ID_CHUNG_TU_GOC" AS INTEGER) AS "ID_CHUNG_TU",
                        "MODEL_CHUNG_TU_GOC"                   AS "MODEL_CHUNG_TU",
                        GLD."NGAY_CHUNG_TU"                    AS "NGAY_CHUNG_TU",
                        coalesce(GLD."SO_CHUNG_TU", '')        AS "SO_CHUNG_TU",
                        GLD."DOI_TUONG_ID",
                        TA."SO_TAI_KHOAN",
                        0                                      AS "SO_TIEN",
                        SUM(coalesce(GLD."CHENH_LECH", 0))     AS "SO_TIEN_QUY_DOI"
                    FROM account_ex_chung_tu_nghiep_vu_khac GL
                        INNER JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan GLD ON GLD."ID_CHUNG_TU_GOC" = GL.id
                        INNER JOIN (
                                    SELECT *
                                    FROM danh_muc_he_thong_tai_khoan AC
                                    WHERE AC."SO_TAI_KHOAN" = '331'
                                    ) TA ON GLD."TK_CONG_NO_ID" = TA.id
                    WHERE
                        GL.currency_id = loai_tien_id
                        AND Gl."CHI_NHANH_ID" = chi_nhanh_id
                        AND (GLD."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id IS NULL)
                    GROUP BY GLD."ID_CHUNG_TU_GOC",
                        GLD."DOI_TUONG_ID"
                        , TA."SO_TAI_KHOAN"
                        , GL."NGAY_BU_TRU"
                        , GL."SO_CHUNG_TU"
                        , GLD."LOAI_CHUNG_TU"
                        , GLD."NGAY_CHUNG_TU"
                        , GLD."SO_CHUNG_TU"
                        , GLD."MODEL_CHUNG_TU_GOC"


                    UNION ALL


                    SELECT
                        PUD."CHUNG_TU_MUA_HANG"                                  AS "ID_CHUNG_TU",
                        'purchase.document'                                      AS "MODEL_CHUNG_TU",
                        PUV."NGAY_CHUNG_TU"                                      AS "NGAY_CHUNG_TU",
                        PUV."SO_CHUNG_TU"                                        AS "SO_CHUNG_TU",
                        PUV."DOI_TUONG_ID",
                        TA."SO_TAI_KHOAN",
                        SUM(coalesce(PUD."THANH_TIEN", 0) + coalesce(PUD."TIEN_THUE_GTGT",
                                                                    0))         AS "SO_TIEN",
                        SUM(coalesce(PUD."THANH_TIEN_QUY_DOI", 0) + coalesce(PUD."TIEN_THUE_GTGT_QUY_DOI",
                                                                            0)) AS "SO_TIEN_QUY_DOI"
                    FROM purchase_ex_tra_lai_hang_mua PUV
                        INNER JOIN purchase_ex_tra_lai_hang_mua_chi_tiet PUD
                        ON PUD."CHUNG_TU_TRA_LAI_HANG_MUA_ID" = PUV.id
                        INNER JOIN (
                                    SELECT *
                                    FROM danh_muc_he_thong_tai_khoan AC
                                    WHERE AC."SO_TAI_KHOAN" = '331'
                                    ) TA ON PUD."TK_CO_ID" = TA.id
                    WHERE
                        PUV.currency_id = loai_tien_id
                        AND PUV."CHI_NHANH_ID" = chi_nhanh_id
                        AND PUD."CHUNG_TU_MUA_HANG" IS NOT NULL
                        AND (PUV."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id IS NULL)
                    GROUP BY PUD."CHUNG_TU_MUA_HANG", PUV."DOI_TUONG_ID", TA."SO_TAI_KHOAN"
                        , PUV."NGAY_CHUNG_TU"
                        , PUV."SO_CHUNG_TU"

                    UNION ALL

                    SELECT
                        PUD."CHUNG_TU_MUA_HANG"                                  AS "ID_CHUNG_TU",
                        'purchase.document'                                      AS "MODEL_CHUNG_TU",
                        PUV."NGAY_CHUNG_TU"                                      AS "NGAY_CHUNG_TU",
                        PUV."SO_CHUNG_TU"                                        AS "SO_CHUNG_TU",
                        PUV."DOI_TUONG_ID",
                        TA."SO_TAI_KHOAN",
                        SUM(coalesce(PUD."THANH_TIEN", 0) + coalesce(PUD."TIEN_THUE_GTGT",
                                                                    0))         AS "SO_TIEN",
                        SUM(coalesce(PUD."THANH_TIEN_QUY_DOI", 0) + coalesce(PUD."TIEN_THUE_GTGT_QUY_DOI",
                                                                            0)) AS "SO_TIEN_QUY_DOI"
                    FROM purchase_ex_giam_gia_hang_mua PUV
                        INNER JOIN purchase_ex_giam_gia_hang_mua_chi_tiet PUD
                        ON PUD."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID" = PUV.id
                        INNER JOIN (
                                    SELECT *
                                    FROM danh_muc_he_thong_tai_khoan AC
                                    WHERE AC."SO_TAI_KHOAN" = '331'
                                    ) TA ON PUD."TK_CO_ID" = TA.id
                    WHERE
                        PUV.currency_id = loai_tien_id
                        AND PUV."CHI_NHANH_ID" = chi_nhanh_id
                        AND PUD."CHUNG_TU_MUA_HANG" IS NOT NULL
                        AND (PUV."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id IS NULL)
                    GROUP BY PUD."CHUNG_TU_MUA_HANG", PUV."DOI_TUONG_ID", TA."SO_TAI_KHOAN"
                        , PUV."NGAY_CHUNG_TU"
                        , PUV."SO_CHUNG_TU"
                    ) A
                LEFT JOIN res_partner AC ON A."DOI_TUONG_ID" = AC.id
                GROUP BY
                A."ID_CHUNG_TU",
                A."MODEL_CHUNG_TU",
                A."NGAY_CHUNG_TU",
                A."SO_CHUNG_TU",
                A."DOI_TUONG_ID",
                A."SO_TAI_KHOAN",
                AC."MA"
            );
            RETURN QUERY SELECT *
                        FROM TBL_KET_QUA;
            END;
            $$ LANGUAGE PLpgSQL;
		""")

        self.env.cr.execute(""" 
			-- DROP FUNCTION FUNCTION_DOI_TRU_MUA_HANG_CONG_NO(IN ma_tai_khoan VARCHAR(50),loai_tien_id INTEGER,chi_nhanh_id INTEGER,doi_tuong_id INTEGER)
            CREATE OR REPLACE FUNCTION FUNCTION_DOI_TRU_MUA_HANG_CONG_NO(IN ma_tai_khoan VARCHAR(50), loai_tien_id INTEGER,
                                                                            chi_nhanh_id INTEGER, doi_tuong_id INTEGER)
            RETURNS TABLE("ID_CHUNG_TU"     INTEGER,
                            "MODEL_CHUNG_TU"  VARCHAR(50),
                            "DOI_TUONG_ID"    INTEGER,
                            "SO_TAI_KHOAN"    VARCHAR(50),
                            "NGAY_HOA_DON"    DATE,
                            "SO_HOA_DON"      VARCHAR(20),
                            "SO_TIEN"         FLOAT,
                            "SO_TIEN_QUY_DOI" FLOAT,
                            "TY_GIA"          FLOAT
            ) AS $$
            DECLARE

            BEGIN

            DROP TABLE IF EXISTS TBL_KET_QUA;
            CREATE TEMP TABLE TBL_KET_QUA (
                "ID_CHUNG_TU"     INTEGER,
                "MODEL_CHUNG_TU"  VARCHAR(50),
                "DOI_TUONG_ID"    INTEGER,
                "SO_TAI_KHOAN"    VARCHAR(50),
                "NGAY_HOA_DON"    DATE,
                "SO_HOA_DON"      VARCHAR(20),
                "SO_TIEN"         FLOAT,
                "SO_TIEN_QUY_DOI" FLOAT,
                "TY_GIA"          FLOAT
            );
            INSERT INTO TBL_KET_QUA (
                SELECT
                A."ID_CHUNG_TU",
                A."MODEL_CHUNG_TU",
                A."DOI_TUONG_ID",
                A."SO_TAI_KHOAN",
                A."NGAY_HOA_DON",
                coalesce(A."SO_HOA_DON", '')          AS "SO_HOA_DON",
                SUM(coalesce(A."SO_TIEN", 0))         AS "SO_TIEN",
                SUM(coalesce(A."SO_TIEN_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI",
                A."TY_GIA"
                FROM
                (
                    SELECT
                    cast(GL."ID_CHUNG_TU_CONG_NO" AS INTEGER)      AS "ID_CHUNG_TU",
                    GL."MODEL_CHUNG_TU_CONG_NO"                    AS "MODEL_CHUNG_TU",
                    Gl."DOI_TUONG_ID"                              AS "DOI_TUONG_ID",
                    TA."SO_TAI_KHOAN",
                    (CASE WHEN GL."LOAI_CHUNG_TU_CONG_NO" IN
                                (610, 612, 613, 614, 620, 330, 331, 332, 333, 334, 352, 357, 358, 359, 360, 362, 363, 364, 365, 366, 368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
                        THEN GL."NGAY_HOA_DON_CONG_NO"
                    ELSE NULL
                    END)                                          AS "NGAY_HOA_DON",
                    (CASE WHEN GL."LOAI_CHUNG_TU_CONG_NO" IN (610, 612,
                                                                    613, 614, 620,
                                                                    330, 331, 332,
                                                                    333, 334, 352,
                        357, 358, 359, 360, 362, 363, 364, 365, 366, 368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
                        THEN coalesce(GL."SO_HOA_DON_CONG_NO", '')
                    ELSE NULL
                    END)                                          AS "SO_HOA_DON",
                    SUM(coalesce(GL."SO_CONG_NO_THANH_TOAN_LAN_NAY", 0))         AS "SO_TIEN",
                    SUM(coalesce(GL."SO_CONG_NO_THANH_TOAN_LAN_NAY_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI",
                    GL."TY_GIA_CONG_NO"                            AS "TY_GIA"
                    FROM sale_ex_doi_tru_chi_tiet GL
                    INNER JOIN (SELECT *
                                FROM danh_muc_he_thong_tai_khoan AC
                                WHERE AC."SO_TAI_KHOAN" = '331') TA ON TA.id = GL."TAI_KHOAN_ID"
                    WHERE GL."currency_id" = loai_tien_id
                        --           AND GL."CHI_NHANH_ID" = (chi_nhanh_id)
                        AND GL."CTTT_DA_GHI_SO" = TRUE
                        AND GL."CTCN_DA_GHI_SO" = TRUE
                        AND (GL."DOI_TUONG_ID" = doi_tuong_id
                            OR doi_tuong_id IS NULL
                        )
                    GROUP BY GL."ID_CHUNG_TU_CONG_NO",
                    GL."MODEL_CHUNG_TU_CONG_NO",
                    GL."DOI_TUONG_ID",
                    TA."SO_TAI_KHOAN",
                    GL."SO_HOA_DON_CONG_NO",
                    GL."NGAY_HOA_DON_CONG_NO",
                    GL."LOAI_CHUNG_TU_CONG_NO"
                    , GL."TY_GIA_CONG_NO"


                    UNION ALL


                    SELECT
                    GLD."ID_CHUNG_TU_GOC",
                    GLD."MODEL_CHUNG_TU_GOC"                  AS "MODEL_CHUNG_TU",
                    GLD."DOI_TUONG_ID",
                    TA."SO_TAI_KHOAN",
                    (CASE WHEN GLD."LOAI_CHUNG_TU" IN
                                ('610', '612', '613', '614', '620', '330', '331', '332', '333', '334', '352', '357', '358', '359', '360', '362', '363', '364', '365', '366', '368', '369', '370', '371', '372', '374', '375', '376', '377', '378')
                        THEN GL."NGAY_CHUNG_TU"
                    ELSE NULL
                    END)                                     AS "NGAY_HOA_DON",
                    (CASE WHEN GLD."LOAI_CHUNG_TU" IN
                                ('610', '612', '613', '614', '620', '330', '331', '332', '333', '334', '352', '357', '358', '359', '360', '362', '363', '364', '365', '366', '368', '369', '370', '371', '372', '374', '375', '376', '377', '378')
                        THEN coalesce(GL."SO_CHUNG_TU", '')
                    ELSE NULL
                    END)                                     AS "SO_HOA_DON",
                    0                                         AS "SO_TIEN",
                    (-1) * SUM(coalesce(GLD."CHENH_LECH", 0)) AS "SO_TIEN_QUY_DOI",
                    GL."TY_GIA"
                    FROM account_ex_chung_tu_nghiep_vu_khac GL
                    INNER JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan GLD ON GLD."ID_CHUNG_TU_GOC" = GL.id
                    INNER JOIN (SELECT *
                                FROM danh_muc_he_thong_tai_khoan AC
                                WHERE AC."SO_TAI_KHOAN" = '331') TA ON GLD."TK_CONG_NO_ID" = TA.id
                    WHERE GL.currency_id = loai_tien_id
                        --           AND Gl."CHI_NHANH_ID" = (chi_nhanh_id)
                        AND (GLD."DOI_TUONG_ID" = doi_tuong_id
                            OR doi_tuong_id IS NULL
                        )
                    GROUP BY GLD."ID_CHUNG_TU_GOC",
                    GLD."MODEL_CHUNG_TU_GOC",
                    GLD."DOI_TUONG_ID",
                    TA."SO_TAI_KHOAN",
                    GL."NGAY_CHUNG_TU",
                    GL."NGAY_HOA_DON",
                    GLD."LOAI_CHUNG_TU",
                    GL."TY_GIA",
                    GL."SO_HOA_DON",
                    GL."SO_CHUNG_TU"

                    UNION ALL

                    SELECT
                    PUD."CHUNG_TU_MUA_HANG"                          AS "ID_CHUNG_TU",
                    'purchase.document'                              AS "MODEL_CHUNG_TU",
                    PUV."DOI_TUONG_ID",
                    TA."SO_TAI_KHOAN",
                    (CASE WHEN PUV."LOAI_CHUNG_TU" IN
                                (610, 612, 613, 614, 620, 330, 331, 332, 333, 334, 352, 357, 358, 359, 360, 362, 363, 364, 365, 366, 368, 369, 370, 371, 372, 374, 375, 376, 377, 378)
                        THEN PUD."NGAY_HD_MUA_HANG"
                    ELSE NULL
                    END)                                            AS NGAY_HOA_DON,
                    (CASE WHEN PUV."LOAI_CHUNG_TU" IN (610, 612, 613,
                                                            614, 620, 330,
                                                            331, 332, 333,
                                                            334, 352, 357,
                                                                        358, 359, 360,
                                                                        362, 363, 364,
                                                                        365, 366, 368,
                                                        369, 370, 371,
                                                        372, 374, 375,
                                                        376, 377, 378)
                        THEN coalesce(PUD."SO_HD_MUA_HANG", '')
                    ELSE NULL
                    END)                                            AS "SO_HOA_DON",
                    SUM(coalesce(PUD."THANH_TIEN", 0)
                        + coalesce(PUD."TIEN_THUE_GTGT", 0))         AS "SO_TIEN",
                    SUM(coalesce(PUD."THANH_TIEN_QUY_DOI", 0)
                        + coalesce(PUD."TIEN_THUE_GTGT_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI",
                    PUV."TY_GIA"
                    FROM purchase_ex_tra_lai_hang_mua PUV
                    INNER JOIN purchase_ex_tra_lai_hang_mua_chi_tiet PUD
                        ON PUD."CHUNG_TU_TRA_LAI_HANG_MUA_ID" = PUV.id
                    INNER JOIN (SELECT *
                                FROM danh_muc_he_thong_tai_khoan AC
                                WHERE AC."SO_TAI_KHOAN" = '331') TA ON PUD."TK_CO_ID" = TA.id
                    WHERE PUV.currency_id = loai_tien_id
                        --           AND PUV."CHI_NHANH_ID" = (chi_nhanh_id)
                        AND PUV.state = 'da_ghi_so'
                        AND PUD."CHUNG_TU_MUA_HANG" IS NOT NULL
                        AND (PUV."DOI_TUONG_ID" = doi_tuong_id OR doi_tuong_id IS NULL)
                    GROUP BY PUD."CHUNG_TU_MUA_HANG",
                    PUV."DOI_TUONG_ID",
                    TA."SO_TAI_KHOAN"
                    , PUV."TY_GIA"
                    , PUV."LOAI_CHUNG_TU"
                    , "NGAY_HD_MUA_HANG"
                    , "SO_HD_MUA_HANG"


                    UNION ALL

                    SELECT
                    PUD."CHUNG_TU_MUA_HANG"                          AS "ID_CHUNG_TU",
                    'purchase.document'                              AS "MODEL_CHUNG_TU",
                    PUV."DOI_TUONG_ID",
                    TA."SO_TAI_KHOAN",
                    (CASE WHEN PUV."LOAI_CHUNG_TU" IN (610, 612, 613,
                                                            614, 620, 330,
                                                            331, 332, 333,
                                                            334, 352, 357,
                                                                        358, 359, 360,
                                                                        362, 363, 364,
                                                                        365, 366, 368,
                                                        369, 370, 371,
                                                        372, 374, 375,
                                                        376, 377, 378)
                        THEN PUD."NGAY_HD_MUA_HANG"
                    ELSE NULL
                    END)                                            AS "NGAY_HOA_DON",
                    (CASE WHEN PUV."LOAI_CHUNG_TU" IN (610, 612, 613,
                                                            614, 620, 330,
                                                            331, 332, 333,
                                                            334, 352, 357,
                                                                        358, 359, 360,
                                                                        362, 363, 364,
                                                                        365, 366, 368,
                                                        369, 370, 371,
                                                        372, 374, 375,
                                                        376, 377, 378)
                        THEN coalesce(PUD."SO_HD_MUA_HANG", '')
                    ELSE NULL
                    END)                                            AS "SO_HOA_DON",
                    SUM(coalesce(PUD."THANH_TIEN", 0)
                        + coalesce(PUD."TIEN_THUE_GTGT", 0))         AS "SO_TIEN",
                    SUM(coalesce(PUD."THANH_TIEN_QUY_DOI", 0)
                        + coalesce(PUD."TIEN_THUE_GTGT_QUY_DOI", 0)) AS "SO_TIEN_QUY_DOI",
                    PUV."TY_GIA"
                    FROM purchase_ex_giam_gia_hang_mua PUV
                    INNER JOIN purchase_ex_giam_gia_hang_mua_chi_tiet PUD
                        ON PUD."GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID" = PUV.id
                    INNER JOIN (SELECT *
                                FROM danh_muc_he_thong_tai_khoan AC
                                WHERE AC."SO_TAI_KHOAN" = '331') TA ON PUD."TK_CO_ID" = TA.id
                    WHERE PUV.currency_id = loai_tien_id
                        --                                     AND PUV."CHI_NHANH_ID" = (chi_nhanh_id)
                        AND PUV.state = 'da_ghi_so'
                        AND PUD."CHUNG_TU_MUA_HANG" IS NOT NULL
                        AND (PUV."DOI_TUONG_ID" = doi_tuong_id
                            OR doi_tuong_id IS NULL
                        )
                    GROUP BY PUD."CHUNG_TU_MUA_HANG",
                    PUV."DOI_TUONG_ID",
                    TA."SO_TAI_KHOAN"
                    , PUV."TY_GIA"
                    , "LOAI_CHUNG_TU"
                    , "NGAY_HD_MUA_HANG"
                    , "SO_HD_MUA_HANG"
                ) A
                GROUP BY
                A."ID_CHUNG_TU",
                A."MODEL_CHUNG_TU",
                A."DOI_TUONG_ID",
                A."SO_TAI_KHOAN",
                A."NGAY_HOA_DON",
                coalesce(A."SO_HOA_DON", ''),
                A."TY_GIA"
            );
            RETURN QUERY SELECT *
                        FROM TBL_KET_QUA;
            END;
            $$ LANGUAGE PLpgSQL;
		""")
    