# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_PHAN_TICH_CONG_NO_PHAI_THU_THEO_TUOI_NO(models.Model):
    _name = 'bao.cao.phan.tich.cong.no.phai.thu.theo.tuoi.no'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày', default=fields.Datetime.now, required=True)
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản',required=True)
    NHOM_KH_ID = fields.Many2one('danh.muc.nhom.khach.hang.nha.cung.cap', string='Nhóm KH', help='Nhóm khách hàng')
    MA_NHOM_KH = fields.Char(string='Mã nhóm khách hàng', help='Mã nhóm khách hàng')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    MA_KHACH_HANG = fields.Char(string='Mã khách hàng', help='Mã khách hàng')#, auto_num='bao_cao_phan_tich_cong_no_phai_thu_theo_tuoi_no_MA_KHACH_HANG')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    TONG_NO = fields.Float(string='Tổng nợ', help='Tổng nợ',digits= decimal_precision.get_precision('VND'))
    KHONG_CO_HAN_NO = fields.Float(string='Không có hạn nợ', help='Không có hạn nợ',digits= decimal_precision.get_precision('VND'))
    KHONG_DEN_30_NGAY_TRUOC_HAN = fields.Float(string='0-30 ngày ', help='0-30 ngày trước hạn',digits= decimal_precision.get_precision('VND'))
    BAMOT_DEN_60_NGAY_TRUOC_HAN = fields.Float(string='31-60 ngày ', help='31-60 ngày trước hạn',digits= decimal_precision.get_precision('VND'))
    SAUMOT_DEN_90_NGAY_TRUOC_HAN = fields.Float(string='61-90 ngày ', help='61-90 ngày trước hạn',digits= decimal_precision.get_precision('VND'))
    CHINMOT_DEN_120_NGAY_TRUOC_HAN = fields.Float(string='91-120 ngày ', help='91-120 ngày trước hạn',digits= decimal_precision.get_precision('VND'))
    TREN_120_NGAY_TRUOC_HAN = fields.Float(string='Trên 120 ngày ', help='Trên 120 ngày trước hạn',digits= decimal_precision.get_precision('VND'))
    TONG_TRUOC_HAN = fields.Float(string='Tổng ', help='Tổng trước hạn',digits= decimal_precision.get_precision('VND'))
    MOT_DEN30_NGAY_QUA_HAN = fields.Float(string='1-30 ngày ', help='1-30 ngày quá hạn',digits= decimal_precision.get_precision('VND'))
    BAMOT_DEN_60_NGAY_QUA_HAN = fields.Float(string='31-60 ngày ', help='31-60 ngày quá hạn',digits= decimal_precision.get_precision('VND'))
    SAUMOT_DEN_90_NGAY_QUA_HAN = fields.Float(string='61-90 ngày ', help='61-90 ngày quá hạn',digits= decimal_precision.get_precision('VND'))
    CHINMOT_DEN_120_NGAY_QUA_HAN = fields.Float(string='91-120 ngày ', help='91-120 ngày quá hạn',digits= decimal_precision.get_precision('VND'))
    TREN_120_NGAY_QUA_HAN = fields.Float(string='Trên 120 ngày ', help='Trên 120 ngày quá hạn',digits= decimal_precision.get_precision('VND'))
    TONG_QUA_HAN = fields.Float(string='Tổng ', help='Tổng quá hạn',digits= decimal_precision.get_precision('VND'))
    TEN_NHOM_KHACH_HANG = fields.Char(string='Tên nhóm khách hàng', help='Tên nhóm khách hàng')

    KHACH_HANG_IDS = fields.One2many('res.partner')

    CHON_TAT_CA_KHACH_HANG = fields.Boolean('Tất cả khách hàng', default=True)    
    KHACH_HANG_MANY_IDS = fields.Many2many('res.partner','phan_tich_cong_no_phai_thu_tn_res_partner', domain=[('LA_KHACH_HANG', '=', True)], string='Chọn KH', help='Chọn khách hàng')
    MA_PC_NHOM_KH = fields.Char()

    @api.onchange('KHACH_HANG_IDS')
    def update_KHACH_HANG_IDS(self):
        self.KHACH_HANG_MANY_IDS =self.KHACH_HANG_IDS.ids

    @api.onchange('NHOM_KH_ID')
    def update_NHOM_KHACH_HANG_ID(self):
        self.KHACH_HANG_MANY_IDS = []
        self.MA_PC_NHOM_KH =self.NHOM_KH_ID.MA_PHAN_CAP

    @api.onchange('KHACH_HANG_MANY_IDS')
    def _onchange_KHACH_HANG_MANY_IDS(self):
        self.KHACH_HANG_IDS = self.KHACH_HANG_MANY_IDS.ids
        
   
    ### START IMPLEMENTING CODE ###
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        TAI_KHOAN_ID = params['TAI_KHOAN_ID'] if 'TAI_KHOAN_ID' in params.keys() and params['TAI_KHOAN_ID'] != 'False' else None
        if  TAI_KHOAN_ID == -1:
            TAI_KHOAN_ID = None
        else:
            TAI_KHOAN_ID = self.env['danh.muc.he.thong.tai.khoan'].search([('id','=',TAI_KHOAN_ID)],limit=1).SO_TAI_KHOAN

        NHOM_KH_ID = params['NHOM_KH_ID'] if 'NHOM_KH_ID' in params.keys() and params['NHOM_KH_ID'] != 'False' else None
        MA_PC_NHOM_KH = params.get('MA_PC_NHOM_KH')
        if params.get('CHON_TAT_CA_KHACH_HANG'):
            domain = [('LA_KHACH_HANG','=', True)]
            if MA_PC_NHOM_KH:
                domain += [('LIST_MPC_NHOM_KH_NCC','ilike', '%'+ MA_PC_NHOM_KH +'%')]
            KHACH_HANG_IDS =  self.env['res.partner'].search(domain).ids
        else:
            KHACH_HANG_IDS = params.get('KHACH_HANG_MANY_IDS')

        # Execute SQL query here
        params_sql = {
            'DEN_NGAY':DEN_NGAY_F,
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'CHI_NHANH_ID':CHI_NHANH_ID,
            'NHOM_KH_ID':NHOM_KH_ID,
            'TAI_KHOAN_ID':TAI_KHOAN_ID,
            'KHACH_HANG_IDS':KHACH_HANG_IDS or None,
            'limit': limit,
            'offset': offset,
        }

        query = """
        --BAO_CAO_PHAN_TICH_CONG_NO_PHAI_THU_THEO_TUOI_NO
DO LANGUAGE plpgsql $$
DECLARE


    den_ngay                            DATE := %(DEN_NGAY)s;

    --tham số đến ngày

    bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    --tham số bao gồm số liệu chi nhánh phụ thuộc

    chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    --tham số chi nhánh

    tai_khoan                         VARCHAR(100) := %(TAI_KHOAN_ID)s;

    --tham số tài khoản

    nhom_kh_id                          INTEGER := %(NHOM_KH_ID)s;

    --tham số nhóm KH


   

    rec                                 RECORD;

    MA_PHAN_CAP_KHACH_HANG              VARCHAR(100);

    TU_NGAY_BAT_DAU_TAI_CHINH           DATE;

BEGIN


    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


    DROP TABLE IF EXISTS DS_KHACH_HANG
    ;

    CREATE TEMP TABLE DS_KHACH_HANG
        AS
            SELECT V."id" AS "KHACH_HANG_ID"
            FROM res_partner V

            WHERE (id = any (%(KHACH_HANG_IDS)s))--tham số KHÁCH HÀNG

    ;


    SELECT concat("MA_PHAN_CAP", '%%')
    INTO MA_PHAN_CAP_KHACH_HANG
    FROM danh_muc_nhom_khach_hang_nha_cung_cap

    WHERE id = nhom_kh_id
    ;

    DROP TABLE IF EXISTS TMP_NHOM_KH
    ;

    CREATE TEMP TABLE TMP_NHOM_KH
        AS
            SELECT
                AO."id"
                , AO."MA_KHACH_HANG"
                , AO."HO_VA_TEN"
                , AO."MA_SO_THUE"                   AS "MA_SO_THUE"
                , COALESCE(AOG."MA", N'<<Khác>>')  AS "MA_NHOM_KHACH_HANG"
                , COALESCE(AOG."TEN", N'<<Khác>>') AS "TEN_NHOM_KHACH_HANG"
                , AO."DIA_CHI"                      AS "DIA_CHI_KHACH_HANG"
            FROM DS_KHACH_HANG tbAO
                INNER JOIN res_partner AO ON tbAO."KHACH_HANG_ID" = AO."id"
                LEFT JOIN danh_muc_nhom_khach_hang_nha_cung_cap AOG
                    ON AO."LIST_MPC_NHOM_KH_NCC" LIKE '%%;' || AOG."MA_PHAN_CAP" || ';%%'
            WHERE MA_PHAN_CAP_KHACH_HANG IS NULL OR AOG."MA_PHAN_CAP" LIKE MA_PHAN_CAP_KHACH_HANG
    ;


    DROP TABLE IF EXISTS TMP_TAI_KHOAN
    ;

        IF tai_khoan IS NOT NULL
        THEN
            CREATE TEMP TABLE TMP_TAI_KHOAN
                AS
                    SELECT
                        A."SO_TAI_KHOAN"

                        , A."TINH_CHAT"
                    FROM danh_muc_he_thong_tai_khoan AS A
                    WHERE "SO_TAI_KHOAN" = tai_khoan
                            AND "CHI_TIET_THEO_DOI_TUONG" = '1'
                            AND "DOI_TUONG_SELECTION" = '1'
                    ORDER BY A."SO_TAI_KHOAN",
                        A."TEN_TAI_KHOAN"
            ;

        ELSE
    CREATE TEMP TABLE TMP_TAI_KHOAN
        AS
            SELECT
                A.id
                , A."SO_TAI_KHOAN"

                , A."TINH_CHAT"
            FROM danh_muc_he_thong_tai_khoan AS A
            WHERE "CHI_TIET_THEO_DOI_TUONG" = '1'
                  AND "DOI_TUONG_SELECTION" = '1'
                  AND "LA_TK_TONG_HOP" = '0'
            ORDER BY A."SO_TAI_KHOAN",
                A."TEN_TAI_KHOAN"
    ;

        END IF
        ;

    SELECT value
    INTO TU_NGAY_BAT_DAU_TAI_CHINH
    FROM ir_config_parameter
    WHERE key = 'he_thong.TU_NGAY_BAT_DAU_TAI_CHINH'
    FETCH FIRST 1 ROW ONLY
    ;

    DROP TABLE IF EXISTS TMP_CONG_NO_KH
    ;

    CREATE TEMP TABLE TMP_CONG_NO_KH
        AS
            SELECT
                GL."DOI_TUONG_ID"
                , GL."ID_CHUNG_TU"
                , GL."MODEL_CHUNG_TU"
                , NULL                                                                       AS "SO_HOA_DON"
                , NULL                                                                       AS "NGAY_HOA_DON"
                , /*Ngày hóa đơn*/
                  SUM(GL."GHI_NO" -
                      GL."GHI_CO")                                                           AS "GIA_TRI_HOA_DON"
                , CASE WHEN "NGAY_HET_HAN" IS NULL
                THEN 0 -- Không có hạn nợ
                  WHEN "NGAY_HET_HAN" >= den_ngay
                      THEN 1 -- Nợ trước hạn
                  ELSE 2 -- Nợ quá hạn "NGAY_HET_HAN"<Todate
                  END                                                                        AS "DebtPeriodType"
                , -- "DebtPeriodType" - int
                  ABS(DATE_PART('day', CAST("NGAY_HET_HAN" AS TIMESTAMP) - CAST(den_ngay AS
                                                                                TIMESTAMP))) AS "SO_NGAY_NO_CON_LAI"
            FROM so_cong_no_chi_tiet GL
                INNER JOIN TMP_LIST_BRAND BR ON GL."CHI_NHANH_ID" = BR."CHI_NHANH_ID"
                INNER JOIN DS_KHACH_HANG AO ON GL."DOI_TUONG_ID" = AO."KHACH_HANG_ID"
                INNER JOIN TMP_TAI_KHOAN TBAN ON GL."MA_TK" LIKE TBAN."SO_TAI_KHOAN" || '%%'

            WHERE
                GL."LOAI_CHUNG_TU" NOT IN ('4013', '4014', '4016', '612', '613')
                AND GL."NGAY_HACH_TOAN" <= den_ngay
            GROUP BY
                GL."DOI_TUONG_ID",
                GL."ID_CHUNG_TU",
                GL."MODEL_CHUNG_TU",
                CASE WHEN "NGAY_HET_HAN" IS NULL
                    THEN 0 -- Không có hạn nợ
                WHEN "NGAY_HET_HAN" >= den_ngay
                    THEN 1 -- Nợ trước hạn
                ELSE 2 -- Nợ quá hạn "NGAY_HET_HAN"<Todate
                END, -- "DebtPeriodType" - int
                ABS(DATE_PART('day', CAST("NGAY_HET_HAN" AS TIMESTAMP) - CAST(den_ngay AS TIMESTAMP)))
            HAVING SUM(GL."GHI_NO" - GL."GHI_CO") > 0

            --Bảng số dư hóa đơn đầu kỳ
            UNION ALL
            SELECT
                OAE."DOI_TUONG_ID"
                , OAI."SO_DU_TAI_KHOAN_CHI_TIET_ID"
                , 'account.ex.so.du.tai.khoan.chi.tiet'                                        AS "MODEL_CHUNG_TU"
                , OAI."SO_HOA_DON"
                , OAI."NGAY_HOA_DON"
                , /*Ngày hóa đơn trên số dư đầu kỳ*/

                  SUM(OAI."SO_CON_PHAI_THU")                                                   AS "QUY_DOI"
                , CASE WHEN OAI."HAN_THANH_TOAN" IS NULL
                THEN 0 -- Không có hạn nợ
                  WHEN OAI."HAN_THANH_TOAN" >= den_ngay
                      THEN 1 -- Nợ trước hạn
                  ELSE 2 -- Nợ quá hạn "NGAY_HET_HAN"<Todate
                  END                                                                          AS "DebtPeriodType"
                , -- "DebtPeriodType" - int
                  ABS(DATE_PART('day', CAST("HAN_THANH_TOAN" AS TIMESTAMP) - CAST(den_ngay AS
                                                                                  TIMESTAMP))) AS "SO_NGAY_NO_CON_LAI"
            FROM account_ex_so_du_tai_khoan_chi_tiet OAE
                INNER JOIN account_ex_sdtkct_theo_hoa_don OAI ON OAE."id" = OAI."SO_DU_TAI_KHOAN_CHI_TIET_ID"
                INNER JOIN TMP_LIST_BRAND BR ON OAE."CHI_NHANH_ID" = BR."CHI_NHANH_ID"
                INNER JOIN DS_KHACH_HANG AO ON OAE."DOI_TUONG_ID" = AO."KHACH_HANG_ID"
                INNER JOIN TMP_TAI_KHOAN TBAN ON OAE."SO_TAI_KHOAN" LIKE TBAN."SO_TAI_KHOAN" || '%%'
                LEFT JOIN res_partner E ON E."id" = OAI."NHAN_VIEN_ID"

            WHERE
                (TU_NGAY_BAT_DAU_TAI_CHINH <= den_ngay OR OAI."NGAY_HOA_DON" <= den_ngay)
            GROUP BY
                OAE."DOI_TUONG_ID",
                OAI."SO_DU_TAI_KHOAN_CHI_TIET_ID",
                OAI."SO_HOA_DON",
                OAI."NGAY_HOA_DON",
                CASE WHEN OAI."HAN_THANH_TOAN" IS NULL
                    THEN 0 -- Không có hạn nợ
                WHEN OAI."HAN_THANH_TOAN" >= den_ngay
                    THEN 1 -- Nợ trước hạn
                ELSE 2 -- Nợ quá hạn "NGAY_HET_HAN"<Todate
                END, -- "DebtPeriodType" - int
                ABS(DATE_PART('day', CAST("HAN_THANH_TOAN" AS TIMESTAMP) - CAST(den_ngay AS TIMESTAMP)))
    ;


    DROP TABLE IF EXISTS TMP_GL
    ;

    CREATE TEMP TABLE TMP_GL
        AS
            SELECT
                AO."MA_KHACH_HANG"
                , AO."HO_VA_TEN"
                , AO."DIA_CHI_KHACH_HANG"
                , AO."MA_SO_THUE"
                , AO."MA_NHOM_KHACH_HANG"
                , AO."TEN_NHOM_KHACH_HANG"
                , REPLACE(CAST(P."LOAI_KHOANG_THOI_GIAN_NO" || P."TEN_KHOANG_THOI_GIAN_NO" AS VARCHAR(500)), '-', '')                     AS "DebtColumnName"
                , P."LOAI_KHOANG_THOI_GIAN_NO"
                , SUM(RTB."GIA_TRI_HOA_DON" - RTB."SO_DA_TRA" - RTB."TRA_LAI_GIAM_GIA" + RTB."CHENH_LECH_TY_GIA_DO_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE") AS "SO_TIEN_THANH_TOAN"
            FROM (
                     -- Lấy dữ liệu bảng chưa thanh toán union alls với các bảng còn lại
                     SELECT
                         NPD."DOI_TUONG_ID"
                         , NPD."ID_CHUNG_TU"
                         , NPD."MODEL_CHUNG_TU"
                         , NPD."GIA_TRI_HOA_DON"
                         , 0 AS "CHENH_LECH_TY_GIA_DO_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE"
                         , 0 AS "TRA_LAI_GIAM_GIA"
                         , 0 AS "CK_THANH_TOAN_GIAM_TRU_KHAC"
                         , 0 AS "SO_DA_TRA"
                         , NPD."SO_NGAY_NO_CON_LAI"
                         , NPD."DebtPeriodType"
                     FROM TMP_CONG_NO_KH NPD
                     UNION ALL
                     -- Bảng trả lại hàng bán
                     SELECT
                         NPD."DOI_TUONG_ID"
                         , NPD."ID_CHUNG_TU"
                         , NPD."MODEL_CHUNG_TU"
                         , 0                         AS "GIA_TRI_HOA_DON"
                         , 0                         AS "CHENH_LECH_TY_GIA_DO_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE"
                         , GL."GHI_CO" - GL."GHI_NO" AS "TRA_LAI_GIAM_GIA"
                         , 0                         AS "CK_THANH_TOAN_GIAM_TRU_KHAC"
                         , 0                         AS "SO_DA_TRA"
                         , NPD."SO_NGAY_NO_CON_LAI"
                         , NPD."DebtPeriodType"
                     FROM TMP_CONG_NO_KH AS NPD
                         INNER JOIN sale_ex_tra_lai_hang_ban_chi_tiet SARD
                             ON (SARD."SO_CHUNG_TU_ID" = NPD."ID_CHUNG_TU" AND NPD."MODEL_CHUNG_TU" = 'sale.document')
                         INNER JOIN so_cong_no_chi_tiet GL
                             ON (SARD."id" = GL."CHI_TIET_ID" AND
                                 GL."CHI_TIET_MODEL" = 'sale.ex.tra.lai.hang.ban.chi.tiet')

                         INNER JOIN TMP_TAI_KHOAN TBAN ON GL."MA_TK" LIKE TBAN."SO_TAI_KHOAN" || '%%'
                     WHERE

                         GL."NGAY_HACH_TOAN" <= den_ngay

                     UNION ALL
                     -- Bảng giảm giá hàng bán
                     SELECT
                         NPD."DOI_TUONG_ID"
                         , NPD."ID_CHUNG_TU"
                         , NPD."MODEL_CHUNG_TU"
                         , 0                         AS "GIA_TRI_HOA_DON"
                         , 0                         AS "CHENH_LECH_TY_GIA_DO_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE"
                         , GL."GHI_CO" - GL."GHI_NO" AS "TRA_LAI_GIAM_GIA"
                         , 0                         AS "CK_THANH_TOAN_GIAM_TRU_KHAC"
                         , 0                         AS "SO_DA_TRA"
                         , NPD."SO_NGAY_NO_CON_LAI"
                         , NPD."DebtPeriodType"
                     FROM TMP_CONG_NO_KH AS NPD
                         INNER JOIN sale_ex_chi_tiet_giam_gia_hang_ban SARD
                             ON (SARD."CHUNG_TU_BAN_HANG_ID" = NPD."ID_CHUNG_TU" AND
                                 NPD."MODEL_CHUNG_TU" = 'sale.document')
                         INNER JOIN so_cong_no_chi_tiet GL ON GL."CHI_TIET_ID" = SARD."id"
                         INNER JOIN TMP_TAI_KHOAN TBAN ON GL."MA_TK" LIKE TBAN."SO_TAI_KHOAN" || '%%'
                     WHERE GL."NGAY_HACH_TOAN" <= den_ngay

                     UNION ALL
                     -- Đối trừ chứng từ , phiếu thu và thu tiền khách hàng ( với tất cả các loại chứng từ)
                     SELECT
                         NPD."DOI_TUONG_ID"
                         , NPD."ID_CHUNG_TU"
                         , NPD."MODEL_CHUNG_TU"
                         , 0                                                                            AS "GIA_TRI_HOA_DON"
                         ,
                           0                                                                            AS "CHENH_LECH_TY_GIA_DO_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE"
                         ,
                           0                                                                            AS "TRA_LAI_GIAM_GIA"
                         ,
                           GLVC."SO_TIEN_CHIET_KHAU"                                                    AS "SO_TIEN_CHIET_KHAU_THANH_TOAN"
                         , GLVC."SO_TIEN_THANH_TOAN_QUY_DOI" - GLVC."CHENH_LECH_TY_GIA_SO_TIEN_QUY_DOI" AS "SO_DA_TRA"
                         , NPD."SO_NGAY_NO_CON_LAI"
                         , NPD."DebtPeriodType"
                     FROM TMP_CONG_NO_KH AS NPD
                         INNER JOIN sale_ex_doi_tru_chi_tiet GLVC
                             ON (GLVC."ID_CHUNG_TU_CONG_NO" = NPD."ID_CHUNG_TU" AND
                                 GLVC."MODEL_CHUNG_TU_CONG_NO" = NPD."MODEL_CHUNG_TU" )
                                AND (GLVC."DOI_TUONG_ID" = NPD."DOI_TUONG_ID")

                                AND (NPD."NGAY_HOA_DON" IS NULL
                                     OR (NPD."NGAY_HOA_DON" IS NOT
                                         NULL)--AND GLVC.Debt"NGAY_HOA_DON" IS NOT NULL AND GLVC.Debt"NGAY_HOA_DON" = NPD."NGAY_HOA_DON" )
                                )
                                AND (NPD."SO_HOA_DON" IS NULL
                                     OR (NPD."SO_HOA_DON" IS NOT NULL AND GLVC."SO_HOA_DON_CONG_NO" = NPD."SO_HOA_DON")
                                )
                         INNER JOIN TMP_TAI_KHOAN TBAN ON GLVC."MA_TAI_KHOAN" LIKE TBAN."SO_TAI_KHOAN" || '%%'
                         /*Chuyển từ điều kiện Where vào đây để lấy tất cả mọi loại chứng từ sửa bug SMEFIVE-4670 by hoan 13.07.2015*/
                         INNER JOIN (SELECT
                                         GL."ID_CHUNG_TU",
                                         GL."MODEL_CHUNG_TU"
                                     FROM so_cai_chi_tiet GL
                                         INNER JOIN DS_KHACH_HANG AO ON GL."DOI_TUONG_ID" = AO."KHACH_HANG_ID"
                                         INNER JOIN TMP_LIST_BRAND B ON GL."CHI_NHANH_ID" = B."CHI_NHANH_ID"

                                     GROUP BY
                                         GL."ID_CHUNG_TU",
                                        GL."MODEL_CHUNG_TU"
                                    ) AS CAR ON CAR."ID_CHUNG_TU" = GLVC."ID_CHUNG_TU_THANH_TOAN" AND  CAR."MODEL_CHUNG_TU" = GLVC."MODEL_CHUNG_TU_THANH_TOAN"
                     WHERE GLVC."NGAY_HACH_TOAN_THANH_TOAN" <= den_ngay
                     UNION ALL
                     -- Đánh giá lại ngoại tệ
                     SELECT
                        NPD."DOI_TUONG_ID"
                         , NPD."ID_CHUNG_TU"
                         , NPD."MODEL_CHUNG_TU"
                         , 0                AS "GIA_TRI_HOA_DON"
                         , GLD."CHENH_LECH" AS "CHENH_LECH_TY_GIA_DO_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE"
                         , 0                AS "TRA_LAI_GIAM_GIA"
                         , 0                AS "CK_THANH_TOAN_GIAM_TRU_KHAC"
                         , 0                AS "SO_DA_TRA"
                         , NPD."SO_NGAY_NO_CON_LAI"
                         , NPD."DebtPeriodType"

                     FROM TMP_CONG_NO_KH AS NPD
                         INNER JOIN tong_hop_chung_tu_nghiep_vu_khac_cong_no_thanh_toan GLD
                             ON (GLD."ID_CHUNG_TU_GOC" = NPD."ID_CHUNG_TU" AND
                             GLD."MODEL_CHUNG_TU_GOC"  =   NPD."MODEL_CHUNG_TU" )
                         INNER JOIN account_ex_chung_tu_nghiep_vu_khac GL ON GL."id" = GLD."CHUNG_TU_NGHIEP_VU_KHAC_ID"
                         INNER JOIN TMP_TAI_KHOAN TBAN ON GLD."MA_TAI_KHOAN" LIKE TBAN."SO_TAI_KHOAN" || '%%'
                     WHERE GL."NGAY_HACH_TOAN" <= den_ngay
                           AND (GLD."ID_CHUNG_TU_GOC" = NPD."ID_CHUNG_TU" AND
                                 GLD."MODEL_CHUNG_TU_GOC"  =   NPD."MODEL_CHUNG_TU"
                           )

                 ) AS RTB

                INNER JOIN purchase_ex_khoang_thoi_gian_theo_doi_no P
                    ON
                        P."LOAI_KHOANG_THOI_GIAN_NO" = RTB."DebtPeriodType"
                        AND (P."TU_NGAY" = 0 AND P."DEN_NGAY" = 0
                           OR  P."TU_NGAY" <> 0 AND P."DEN_NGAY" = 0 AND RTB."SO_NGAY_NO_CON_LAI" >= P."TU_NGAY"
                             OR P."TU_NGAY" <> 0 AND P."DEN_NGAY" <> 0 AND RTB."SO_NGAY_NO_CON_LAI" BETWEEN P."TU_NGAY" AND P."DEN_NGAY"
                        )
                INNER JOIN TMP_NHOM_KH AO ON AO.id = RTB."DOI_TUONG_ID"
            WHERE P."MA_BAO_CAO" = 'ReceivableSummaryByAgeOfDebt'
            GROUP BY
                AO."MA_KHACH_HANG",
                AO."HO_VA_TEN",
                AO."DIA_CHI_KHACH_HANG",
                AO."MA_SO_THUE",
                AO."MA_NHOM_KHACH_HANG",
                AO."TEN_NHOM_KHACH_HANG",
                REPLACE(CAST(P."LOAI_KHOANG_THOI_GIAN_NO" || P."TEN_KHOANG_THOI_GIAN_NO" AS VARCHAR(500)), '-', '') ,
                P."LOAI_KHOANG_THOI_GIAN_NO"
            HAVING SUM(RTB."GIA_TRI_HOA_DON" - RTB."SO_DA_TRA" - RTB."TRA_LAI_GIAM_GIA" +
                      RTB."CHENH_LECH_TY_GIA_DO_DANH_GIA_LAI_TAI_KHOAN_NGOAI_TE") <> 0
    ;





END $$
;




 SELECT
          ROW_NUMBER()
          OVER (
              ORDER BY "MA_NHOM_KHACH_HANG", "TEN_NHOM_KHACH_HANG" ) AS RowNum
        , "MA_NHOM_KHACH_HANG"  AS "MA_NHOM_KH"
        ,"TEN_NHOM_KHACH_HANG"
        , "MA_KHACH_HANG"
        , "HO_VA_TEN"  AS "TEN_KHACH_HANG"
        , "DIA_CHI_KHACH_HANG"   AS "DIA_CHI"
        , SUM("SO_TIEN_THANH_TOAN")                                          AS "TONG_NO"
        , SUM(CASE WHEN "DebtColumnName" = N'0Không có hạn nợ'
        THEN "SO_TIEN_THANH_TOAN"
              ELSE 0 END) AS "KHONG_CO_HAN_NO"
        , SUM(CASE WHEN "DebtColumnName" = N'10-30 ngày'
        THEN "SO_TIEN_THANH_TOAN"
              ELSE 0 END) AS "KHONG_DEN_30_NGAY_TRUOC_HAN"
        , SUM(CASE WHEN "DebtColumnName" = N'131-60 ngày'
        THEN "SO_TIEN_THANH_TOAN"
              ELSE 0 END) AS "BAMOT_DEN_60_NGAY_TRUOC_HAN"
        , SUM(CASE WHEN "DebtColumnName" = N'161-90 ngày'
        THEN "SO_TIEN_THANH_TOAN"
              ELSE 0 END) AS "SAUMOT_DEN_90_NGAY_TRUOC_HAN"
        , SUM(CASE WHEN "DebtColumnName" = N'191-120 ngày'
        THEN "SO_TIEN_THANH_TOAN"
              ELSE 0 END) AS "CHINMOT_DEN_120_NGAY_TRUOC_HAN"
        , SUM(CASE WHEN "DebtColumnName" = N'1Trên 120 ngày'
        THEN "SO_TIEN_THANH_TOAN"
              ELSE 0 END) AS "TREN_120_NGAY_TRUOC_HAN"
        , SUM(CASE WHEN "LOAI_KHOANG_THOI_GIAN_NO" = 1
        THEN "SO_TIEN_THANH_TOAN"
              ELSE 0 END) AS "TONG_TRUOC_HAN"
        , SUM(CASE WHEN "DebtColumnName" = N'21-30 ngày'
        THEN "SO_TIEN_THANH_TOAN"
              ELSE 0 END) AS "MOT_DEN30_NGAY_QUA_HAN"
        , SUM(CASE WHEN "DebtColumnName" = N'231-60 ngày'
        THEN "SO_TIEN_THANH_TOAN"
              ELSE 0 END) AS "BAMOT_DEN_60_NGAY_QUA_HAN"
        , SUM(CASE WHEN "DebtColumnName" = N'261-90 ngày'
        THEN "SO_TIEN_THANH_TOAN"
              ELSE 0 END) AS "SAUMOT_DEN_90_NGAY_QUA_HAN"
        , SUM(CASE WHEN "DebtColumnName" = N'291-120 ngày'
        THEN "SO_TIEN_THANH_TOAN"
              ELSE 0 END) AS "CHINMOT_DEN_120_NGAY_QUA_HAN"
        , SUM(CASE WHEN "DebtColumnName" = N'2Trên 120 ngày'
        THEN "SO_TIEN_THANH_TOAN"
              ELSE 0 END) AS "TREN_120_NGAY_QUA_HAN"
        , SUM(CASE WHEN "LOAI_KHOANG_THOI_GIAN_NO" = 2
        THEN "SO_TIEN_THANH_TOAN"
              ELSE 0 END) AS "TONG_QUA_HAN"
    FROM TMP_GL
    GROUP BY
        "MA_NHOM_KHACH_HANG",
       "TEN_NHOM_KHACH_HANG",
        "MA_KHACH_HANG",
        "HO_VA_TEN",
        "DIA_CHI_KHACH_HANG"
    
    OFFSET %(offset)s
    LIMIT %(limit)s;


        """
        return self.execute(query,params_sql)
   
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_PHAN_TICH_CONG_NO_PHAI_THU_THEO_TUOI_NO, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','131')],limit=1)
       
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        if tai_khoan:
            result['TAI_KHOAN_ID'] = tai_khoan.id
        
        return result
    ### END IMPLEMENTING CODE ###

    def _validate(self):
        params = self._context

        CHON_TAT_CA_KHACH_HANG = params['CHON_TAT_CA_KHACH_HANG'] if 'CHON_TAT_CA_KHACH_HANG' in params.keys() else 'False'
        KHACH_HANG_MANY_IDS = params['KHACH_HANG_MANY_IDS'] if 'KHACH_HANG_MANY_IDS' in params.keys() else 'False'

        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
       
        if DEN_NGAY == 'False':
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        
        if CHON_TAT_CA_KHACH_HANG == 'False':
            if KHACH_HANG_MANY_IDS == []:
                raise ValidationError('Bạn chưa chọn <Khách hàng>. Xin vui lòng chọn lại.')

    def _action_view_report(self):
        self._validate()
        DEN_NGAY_F = self.get_vntime('DEN_NGAY')
        TAI_KHOAN_ID = self.get_context('TAI_KHOAN_ID')
        tai_khoan = ''
        tai_khoan_id = self.env['danh.muc.he.thong.tai.khoan'].browse(TAI_KHOAN_ID)
        if tai_khoan_id:
            tai_khoan = tai_khoan_id.SO_TAI_KHOAN
        param = 'Tài khoản: %s; Đến ngày %s' % (tai_khoan, DEN_NGAY_F)
        action = self.env.ref('bao_cao.open_report__phan_tich_cong_no_phai_thu_theo_tuoi_no').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}').replace('\n',''))
        action['context'].update({'breadcrumb_ex': param})
        return action