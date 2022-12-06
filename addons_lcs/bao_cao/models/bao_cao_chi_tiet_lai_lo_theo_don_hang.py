# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class bao_cao_chi_tiet_lai_lo_theo_don_hang(models.Model):
    _name = 'bao.cao.chi.tiet.lai.lo.theo.don.hang'
    _description = ''
    _inherit = ['mail.thread']
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh', required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI', required='True')
    TU = fields.Date(string='Từ ', help='Từ ', required='True', default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến', required='True', default=fields.Datetime.now)

    rownum = fields.Integer(string='rownum', help='RowNum')
    STT = fields.Integer(string='STT', help='SortOrder')
    TEN_CHI_TIEU = fields.Char(string='TEN_CHI_TIEU')
    SO_DON_HANG = fields.Char(string='SO_DON_HANG', help='SAOrderRefNo')
    NGAY_DON_HANG = fields.Date(string='NGAY_DON_HANG', help='SAOrderDate')
    ID_CHUNG_TU = fields.Integer(string='ID_CHUNG_TU')
    MODEL_CHUNG_TU = fields.Char(string='MODEL_CHUNG_TU')
    LOAI_CHUNG_TU = fields.Integer(string='LOAI_CHUNG_TU')
    SO_CHUNG_TU = fields.Char(string='SO_CHUNG_TU', help='RefNo')
    NGAY_HACH_TOAN = fields.Date(string='NGAY_HACH_TOAN', help='PostedDate')
    NGAY_CHUNG_TU = fields.Date(string='NGAY_CHUNG_TU', help='RefDate')
    MA_KHACH_HANG = fields.Char(string='MA_KHACH_HANG')
    TEN_KHACH_HANG = fields.Char(string='TEN_KHACH_HANG')
    NGAY_HOA_DON = fields.Date(string='NGAY_HOA_DON')
    SO_HOA_DON = fields.Char(string='SO_HOA_DON')
    DIEN_GIAI = fields.Char(string='DIEN_GIAI', help='Description')
    SO_TIEN = fields.Float(string='SO_TIEN', help='Amount',digits= decimal_precision.get_precision('VND'))
    isbold = fields.Boolean(string='isbold', help='IsBold')

    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')

    CHON_TAT_CA_DON_DAT_HANG = fields.Boolean('Tất cả đơn hàng', default=True)
    DON_DAT_HANG_MANY_IDS = fields.Many2many('account.ex.don.dat.hang', 'chi_tiet_lai_lo_theo_don_hang', string='Chọn đơn hàng')
    DON_DAT_HANG_IDS = fields.One2many('account.ex.don.dat.hang')

    # Đơn đặt hàng
    @api.onchange('DON_DAT_HANG_IDS')
    def update_DON_DAT_HANG_IDS(self):
        self.DON_DAT_HANG_MANY_IDS =self.DON_DAT_HANG_IDS.ids
        
    @api.onchange('DON_DAT_HANG_MANY_IDS')
    def _onchange_DON_DAT_HANG_MANY_IDS(self):
        self.DON_DAT_HANG_IDS = self.DON_DAT_HANG_MANY_IDS.ids
    # end  

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')

    @api.model
    def default_get(self, fields_list):
        result = super(bao_cao_chi_tiet_lai_lo_theo_don_hang, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        return result
    
    def _validate(self):
        params = self._context
        TU_NGAY = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

        CHON_TAT_CA_DON_DAT_HANG = params['CHON_TAT_CA_DON_DAT_HANG'] if 'CHON_TAT_CA_DON_DAT_HANG' in params.keys() else 'False'
        DON_DAT_HANG_MANY_IDS = params['DON_DAT_HANG_MANY_IDS'] if 'DON_DAT_HANG_MANY_IDS' in params.keys() else 'False'
        
        if(TU_NGAY=='False'):
            raise ValidationError('<Từ ngày> không được bỏ trống.')
        elif(DEN_NGAY=='False'):
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        elif(TU_NGAY_F > DEN_NGAY_F):
            raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')

        if CHON_TAT_CA_DON_DAT_HANG == 'False':
            if DON_DAT_HANG_MANY_IDS == []:
                raise ValidationError('Bạn chưa chọn <Đơn hàng>. Xin vui lòng chọn lại.')

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        TU_NGAY = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
       
        if params.get('CHON_TAT_CA_DON_DAT_HANG'):
            domain = []
            DON_DAT_HANG_IDS = self.env['account.ex.don.dat.hang'].search(domain).ids
        else:
            DON_DAT_HANG_IDS = params.get('DON_DAT_HANG_MANY_IDS')

        params_sql = {
            'TU_NGAY':TU_NGAY_F, 
            'DEN_NGAY':DEN_NGAY_F, 
            'DON_DAT_HANG_IDS':DON_DAT_HANG_IDS, 
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'CHI_NHANH_ID':CHI_NHANH_ID,
            'limit': limit,
            'offset': offset, 
            }   
        
        query = """
        DO LANGUAGE plpgsql $$
DECLARE
    tu_ngay                             TIMESTAMP := %(TU_NGAY)s;

    --tham số từ

    den_ngay                            TIMESTAMP :=  %(DEN_NGAY)s;

    --tham số đến

    bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    --tham số bao gồm số liệu chi nhánh phụ thuộc

    chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s; 

    --tham số chi nhánh

    CHE_DO_KE_TOAN                      VARCHAR;

    BAO_CAO_ID                          VARCHAR :='IncomeDetailBySAOrder';



BEGIN

    SELECT value
    INTO CHE_DO_KE_TOAN
    FROM ir_config_parameter
    WHERE key = 'he_thong.CHE_DO_KE_TOAN'
    FETCH FIRST 1 ROW ONLY
    ;

    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


    DROP TABLE IF EXISTS TMP_DS_DON_DAT_HANG
    ;

    CREATE TEMP TABLE TMP_DS_DON_DAT_HANG


    (
        "ID_CHUNG_TU"    INT PRIMARY KEY,
        "SO_CHUNG_TU"    VARCHAR(25),
        "NGAY_CHUNG_TU"  TIMESTAMP,
        "DOI_TUONG_ID"   INT,
        "MA_KHACH_HANG"  VARCHAR(25),
        "TEN_KHACH_HANG" VARCHAR(128)
    )
    ;

    INSERT INTO TMP_DS_DON_DAT_HANG
        SELECT
            SAO."id"
            , SAO."SO_DON_HANG"
            , SAO."NGAY_DON_HANG"
            , SAO."KHACH_HANG_ID"
            , AO."MA"
            , SAO."TEN_KHACH_HANG"
        FROM account_ex_don_dat_hang SAO
            LEFT JOIN res_partner AO ON AO."id" = SAO."KHACH_HANG_ID"
        WHERE SAO.id = any(%(DON_DAT_HANG_IDS)s) -- DON_DAT_HANG_IDS
    ;

    DROP TABLE IF EXISTS TMP_BANG_CHUNG_TU_GHI_SO_DA_DUOC_TINH_PHAN_BO
    ;

    CREATE TEMP TABLE TMP_BANG_CHUNG_TU_GHI_SO_DA_DUOC_TINH_PHAN_BO

        -- Bảng chứng từ ghi sổ đã được tính phân bổ
    (
        "STT"                             INT,
        "TEN_CHI_TIEU"                    VARCHAR(255),
        "DON_DAT_HANG"                    VARCHAR(25),
        "NGAY_DON_HANG"                   TIMESTAMP,
        "ID_CHUNG_TU"                     INT,
        "MODEL_CHUNG_TU"                  VARCHAR(255),
        "LOAI_CHUNG_TU"                   INT,
        "SO_CHUNG_TU"                     VARCHAR(20),
        "NGAY_HACH_TOAN"                  TIMESTAMP,
        "NGAY_CHUNG_TU"                   TIMESTAMP,
        "MA_KHACH_HANG"                   VARCHAR(25),
        "TEN_KHACH_HANG"                  VARCHAR(128),
        "NGAY_HOA_DON"                    TIMESTAMP,
        "SO_HOA_DON"                      VARCHAR(500),
        "DIEN_GIAI"                       VARCHAR(255),
        "SO_TIEN"                         FLOAT,
        "CAU_HINH_LAI_LO_CHO_CT_HD_DH_ID" INT,
        "MA_CHI_TIEU_DINH_DANH"           VARCHAR(20)

    )
    ;

    INSERT INTO TMP_BANG_CHUNG_TU_GHI_SO_DA_DUOC_TINH_PHAN_BO
        SELECT
            SRT."sequence"
            , SRT."TEN_CHI_TIEU"
            , SAO."SO_CHUNG_TU"   AS "DON_DAT_HANG"
            , SAO."NGAY_CHUNG_TU" AS "NGAY_DON_HANG"
            , GL."ID_CHUNG_TU"
            , GL."MODEL_CHUNG_TU"
            , CAST(GL."LOAI_CHUNG_TU" AS INT)
            , GL."SO_CHUNG_TU"
            , GL."NGAY_HACH_TOAN"
            , GL."NGAY_CHUNG_TU"
            , SAO."MA_KHACH_HANG"
            , SAO."TEN_KHACH_HANG"
            , GL."NGAY_HOA_DON"
            , GL."SO_HOA_DON"
            , GL."DIEN_GIAI"
            , SUM(GL."SO_TIEN")
            , GL."MA_BAO_CAO_VAT_TU_ID"
            , SRT."MA_CHI_TIEU_DINH_DANH"

        FROM tien_ich_cau_hinh_lai_lo_cho_ct_hd_dh SRT
            LEFT JOIN LAY_SO_LIEU_SO_CAI_THEO_CT_THIET_LAP_BCTC_TRA_VE(NULL,
                                                                       tu_ngay,
                                                                       den_ngay,
                                                                       BAO_CAO_ID, NULL,
                                                                       chi_nhanh_id,
                                                                       bao_gom_du_lieu_chi_nhanh_phu_thuoc
                      ) GL ON GL."MA_BAO_CAO_VAT_TU_ID" = SRT.id
            INNER JOIN TMP_DS_DON_DAT_HANG SAO ON SAO."ID_CHUNG_TU" = GL."DON_DAT_HANG_ID"

        GROUP BY
            SRT."sequence",
            SRT."TEN_CHI_TIEU",
            SAO."SO_CHUNG_TU",
            SAO."NGAY_CHUNG_TU",
            GL."ID_CHUNG_TU",
            GL."MODEL_CHUNG_TU",
            CAST(GL."LOAI_CHUNG_TU" AS INT),
            GL."SO_CHUNG_TU",
            GL."NGAY_HACH_TOAN",
            GL."NGAY_CHUNG_TU",
            SAO."MA_KHACH_HANG",
            SAO."TEN_KHACH_HANG",
            GL."NGAY_HOA_DON",
            GL."SO_HOA_DON",
            GL."DIEN_GIAI",
            GL."MA_BAO_CAO_VAT_TU_ID",
            SRT."MA_CHI_TIEU_DINH_DANH"

        UNION ALL
        SELECT
              3                                                             "STT"
            , N'Giá vốn hàng bán'                                          "TEN_CHI_TIEU"
            , SAO."SO_CHUNG_TU"                                             "DON_DAT_HANG"
            , SAO."NGAY_CHUNG_TU"                                           "NGAY_DON_HANG"
            , JCAE."id"
            , 'tong.hop.phan.bo.chi.phi.bh.qldn.chi.phi.khac.cho.don.vi' AS "MODEL_CHUNG_TU"
            , JCAE."LOAI_CHUNG_TU"
            , JCAE."SO_CHUNG_TU"
            , JCAE."NGAY_CHUNG_TU"                                          "NGAY_HACH_TOAN"
            , JCAE."NGAY_CHUNG_TU"
            , SAO."MA_KHACH_HANG"
            , SAO."TEN_KHACH_HANG"
            , NULL                                                          "NGAY_HOA_DON"
            , NULL                                                          "SO_HOA_DON"
            , JCAE."DIEN_GIAI"
            , SUM(JCAEDT."SO_TIEN")                                         "SO_TIEN"
            , NULL                                                          "MA_BAO_CAO_VAT_TU_ID"
            , '03'                                                          "MA_CHI_TIEU_DINH_DANH"

        FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JCAE
            INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCAEDT
                ON JCAEDT."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JCAE."id"
            INNER JOIN TMP_DS_DON_DAT_HANG SAO ON SAO."ID_CHUNG_TU" = JCAEDT."MA_DON_VI_ID"
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCAE."CHI_NHANH_ID"

        WHERE JCAEDT."CAP_TO_CHUC" = '2'
              AND JCAE."NGAY_CHUNG_TU" BETWEEN tu_ngay AND den_ngay
              AND (SELECT "SO_TAI_KHOAN"
                   FROM danh_muc_he_thong_tai_khoan TK
                   WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '632%%'

        GROUP BY
            SAO."SO_CHUNG_TU",
            SAO."NGAY_CHUNG_TU",
            JCAE."id",

            JCAE."LOAI_CHUNG_TU",
            JCAE."SO_CHUNG_TU",
            JCAE."NGAY_CHUNG_TU",
            SAO."MA_KHACH_HANG",
            SAO."TEN_KHACH_HANG",
            JCAE."DIEN_GIAI"

        UNION ALL
        SELECT
              4                                                             "STT"
            , N'Chi phí khác'                                              "TEN_CHI_TIEU"
            , SAO."SO_CHUNG_TU"                                             "DON_DAT_HANG"
            , SAO."NGAY_CHUNG_TU"                                           "NGAY_DON_HANG"
            , JCAE."id"
            , 'tong.hop.phan.bo.chi.phi.bh.qldn.chi.phi.khac.cho.don.vi' AS "MODEL_CHUNG_TU"
            , JCAE."LOAI_CHUNG_TU"
            , JCAE."SO_CHUNG_TU"
            , JCAE."NGAY_CHUNG_TU"                                          "NGAY_HACH_TOAN"
            , JCAE."NGAY_CHUNG_TU"
            , SAO."MA_KHACH_HANG"
            , SAO."TEN_KHACH_HANG"
            , NULL                                                          "NGAY_HOA_DON"
            , NULL                                                          "SO_HOA_DON"
            , JCAE."DIEN_GIAI"
            , SUM(CASE WHEN CHE_DO_KE_TOAN = '15'
                            AND LEFT((SELECT "SO_TAI_KHOAN"
                                      FROM danh_muc_he_thong_tai_khoan TK
                                      WHERE TK.id = JCAEDT."TAI_KHOAN_ID"), 3) IN (
                                    '641', '642', '811', '635')
            THEN JCAEDT."SO_TIEN"
                  WHEN CHE_DO_KE_TOAN = '48'
                       AND LEFT((SELECT "SO_TAI_KHOAN"
                                 FROM danh_muc_he_thong_tai_khoan TK
                                 WHERE TK.id = JCAEDT."TAI_KHOAN_ID"), 3) IN (
                               '642', '811', '635')
                      THEN JCAEDT."SO_TIEN"
                  ELSE 0
                  END)                                                      "SO_TIEN"
            , NULL                                                          "MA_BAO_CAO_VAT_TU_ID"
            , '04'                                                          "MA_CHI_TIEU_DINH_DANH"

        FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JCAE
            INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCAEDT
                ON JCAEDT."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JCAE."id"
            INNER JOIN TMP_DS_DON_DAT_HANG SAO ON SAO."ID_CHUNG_TU" = JCAEDT."MA_DON_VI_ID"
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCAE."CHI_NHANH_ID"

        WHERE JCAEDT."CAP_TO_CHUC" = '2'
              AND JCAE."NGAY_CHUNG_TU" BETWEEN tu_ngay AND den_ngay
              AND LEFT((SELECT "SO_TAI_KHOAN"
                        FROM danh_muc_he_thong_tai_khoan TK
                        WHERE TK.id = JCAEDT."TAI_KHOAN_ID"), 3) IN ('641', '642',
                                                                     '811', '635')

        GROUP BY
            SAO."SO_CHUNG_TU",
            SAO."NGAY_CHUNG_TU",
            JCAE."id",
            JCAE."LOAI_CHUNG_TU",
            JCAE."SO_CHUNG_TU",
            JCAE."NGAY_CHUNG_TU",
            SAO."MA_KHACH_HANG",
            SAO."TEN_KHACH_HANG",
            JCAE."DIEN_GIAI"
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA
        AS

            SELECT
                ROW_NUMBER()
                OVER (
                    ORDER BY "SO_DON_HANG"  NULLS FIRST, "STT" NULLS FIRST, "NGAY_HACH_TOAN" NULLS FIRST, "NGAY_CHUNG_TU" NULLS FIRST, "SO_CHUNG_TU" NULLS FIRST, "NGAY_HOA_DON" NULLS FIRST,
                        "SO_HOA_DON" NULLS FIRST ) AS RowNum
                , *
            FROM (SELECT
                        1                    "STT"
                      , 'DOANH THU'          "TEN_CHI_TIEU"
                      , GL."DON_DAT_HANG" AS "SO_DON_HANG"
                      , GL."NGAY_DON_HANG"
                      , NULL :: INT          "ID_CHUNG_TU"
                      , NULL                 "MODEL_CHUNG_TU"
                      , NULL :: INT          "LOAI_CHUNG_TU"
                      , NULL                 "SO_CHUNG_TU"
                      , NULL :: TIMESTAMP    "NGAY_HACH_TOAN"
                      , NULL :: TIMESTAMP    "NGAY_CHUNG_TU"
                      , GL."MA_KHACH_HANG"
                      , GL."TEN_KHACH_HANG"
                      , NULL     :: TIMESTAMP            "NGAY_HOA_DON"
                      , NULL                 "SO_HOA_DON"
                      , 'DOANH THU'          "DIEN_GIAI"
                      , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '01'
                    THEN GL."SO_TIEN"
                            ELSE 0
                            END)             "SO_TIEN"

                      , CAST(1 AS BOOLEAN)   IsBold
                  FROM TMP_BANG_CHUNG_TU_GHI_SO_DA_DUOC_TINH_PHAN_BO GL
                  GROUP BY GL."DON_DAT_HANG",
                      GL."NGAY_DON_HANG",
                      GL."MA_KHACH_HANG",
                      GL."TEN_KHACH_HANG"
                  UNION ALL
                  SELECT
                        2                  "STT"
                      , N'CHI PHÍ'        "TEN_CHI_TIEU"
                      , GL."DON_DAT_HANG"
                      , GL."NGAY_DON_HANG"
                      , NULL :: INT        "ID_CHUNG_TU"
                      , NULL               "MODEL_CHUNG_TU"
                      , NULL :: INT        "LOAI_CHUNG_TU"
                      , NULL               "SO_CHUNG_TU"
                      , NULL :: TIMESTAMP  "NGAY_HACH_TOAN"
                      , NULL :: TIMESTAMP  "NGAY_CHUNG_TU"
                      , GL."MA_KHACH_HANG"
                      , GL."TEN_KHACH_HANG"
                      , NULL   :: TIMESTAMP            "NGAY_HOA_DON"
                      , NULL               "SO_HOA_DON"
                      , N'CHI PHÍ'        "DIEN_GIAI"
                      , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '03'
                                      OR GL."MA_CHI_TIEU_DINH_DANH" = '04'
                      THEN GL."SO_TIEN"
                            ELSE 0
                            END)           "SO_TIEN"

                      , CAST(1 AS BOOLEAN) IsBold
                  FROM TMP_BANG_CHUNG_TU_GHI_SO_DA_DUOC_TINH_PHAN_BO GL
                  GROUP BY GL."DON_DAT_HANG",
                      GL."NGAY_DON_HANG",
                      GL."MA_KHACH_HANG",
                      GL."TEN_KHACH_HANG"
                  UNION ALL
                  SELECT
                        3                    "STT"
                      , N'Giá vốn hàng bán' "TEN_CHI_TIEU"
                      , GL."DON_DAT_HANG"
                      , GL."NGAY_DON_HANG"
                      , NULL :: INT          "ID_CHUNG_TU"
                      , NULL                 "MODEL_CHUNG_TU"
                      , NULL :: INT          "LOAI_CHUNG_TU"
                      , NULL                 "SO_CHUNG_TU"
                      , NULL :: TIMESTAMP    "NGAY_HACH_TOAN"
                      , NULL :: TIMESTAMP    "NGAY_CHUNG_TU"
                      , GL."MA_KHACH_HANG"
                      , GL."TEN_KHACH_HANG"
                     , NULL   :: TIMESTAMP            "NGAY_HOA_DON"
                      , NULL                 "SO_HOA_DON"
                      , N'Giá vốn hàng bán' "DIEN_GIAI"
                      , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '03'
                      THEN GL."SO_TIEN"
                            ELSE 0
                            END)             "SO_TIEN"

                      , CAST(1 AS BOOLEAN)   IsBold
                  FROM TMP_BANG_CHUNG_TU_GHI_SO_DA_DUOC_TINH_PHAN_BO GL
                  GROUP BY GL."DON_DAT_HANG",
                      GL."NGAY_DON_HANG",
                      GL."MA_KHACH_HANG",
                      GL."TEN_KHACH_HANG"
                  UNION ALL
                  SELECT
                        4                  "STT"
                      , N'Chi phí khác'   "TEN_CHI_TIEU"
                      , GL."DON_DAT_HANG"
                      , GL."NGAY_DON_HANG"
                      , NULL :: INT        "ID_CHUNG_TU"
                      , NULL               "MODEL_CHUNG_TU"
                      , NULL :: INT        "LOAI_CHUNG_TU"
                      , NULL               "SO_CHUNG_TU"
                      , NULL :: TIMESTAMP  "NGAY_HACH_TOAN"
                      , NULL :: TIMESTAMP  "NGAY_CHUNG_TU"
                      , GL."MA_KHACH_HANG"
                      , GL."TEN_KHACH_HANG"
                       , NULL   :: TIMESTAMP            "NGAY_HOA_DON"
                      , NULL               "SO_HOA_DON"
                      , N'Chi phí khác'   "DIEN_GIAI"
                      , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '04'
                      THEN GL."SO_TIEN"
                            ELSE 0
                            END)           "SO_TIEN"

                      , CAST(1 AS BOOLEAN) IsBold
                  FROM TMP_BANG_CHUNG_TU_GHI_SO_DA_DUOC_TINH_PHAN_BO GL
                  GROUP BY GL."DON_DAT_HANG",
                      GL."NGAY_DON_HANG",
                      GL."MA_KHACH_HANG",
                      GL."TEN_KHACH_HANG"
                  UNION ALL
                  SELECT
                        5                  "STT"
                      , N'LỢI NHUẬN'      "TEN_CHI_TIEU"
                      , GL."DON_DAT_HANG"
                      , GL."NGAY_DON_HANG"
                      , NULL :: INT        "ID_CHUNG_TU"
                      , NULL               "MODEL_CHUNG_TU"
                      , NULL :: INT        "LOAI_CHUNG_TU"
                      , NULL               "SO_CHUNG_TU"
                      , NULL :: TIMESTAMP  "NGAY_HACH_TOAN"
                      , NULL :: TIMESTAMP  "NGAY_CHUNG_TU"
                      , GL."MA_KHACH_HANG"
                      , GL."TEN_KHACH_HANG"
                      , NULL   :: TIMESTAMP            "NGAY_HOA_DON"
                      , NULL               "SO_HOA_DON"
                      , N'LỢI NHUẬN'      "DIEN_GIAI"
                      , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '01'
                      THEN GL."SO_TIEN"
                            ELSE CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '03'
                                           OR GL."MA_CHI_TIEU_DINH_DANH" = '04'
                                THEN -GL."SO_TIEN"
                                 ELSE 0
                                 END
                            END)           "SO_TIEN"

                      , CAST(1 AS BOOLEAN) IsBold
                  FROM TMP_BANG_CHUNG_TU_GHI_SO_DA_DUOC_TINH_PHAN_BO GL
                  GROUP BY GL."DON_DAT_HANG",
                      GL."NGAY_DON_HANG",
                      GL."MA_KHACH_HANG",
                      GL."TEN_KHACH_HANG"
                  UNION ALL
                  SELECT
                      "STT"
                      , GL."TEN_CHI_TIEU"
                      , GL."DON_DAT_HANG"
                      , GL."NGAY_DON_HANG"
                      , GL."ID_CHUNG_TU"
                      , GL."MODEL_CHUNG_TU"
                      , CAST(GL."LOAI_CHUNG_TU" AS INT)
                      , GL."SO_CHUNG_TU"
                      , GL."NGAY_HACH_TOAN"
                      , GL."NGAY_CHUNG_TU"
                      , GL."MA_KHACH_HANG"
                      , GL."TEN_KHACH_HANG"
                      , GL."NGAY_HOA_DON"
                      , GL."SO_HOA_DON"
                      , GL."DIEN_GIAI"     "DIEN_GIAI"
                      , GL."SO_TIEN"       "SO_TIEN"
                      , CAST(0 AS BOOLEAN) IsBold
                  FROM TMP_BANG_CHUNG_TU_GHI_SO_DA_DUOC_TINH_PHAN_BO GL
                  WHERE GL."SO_TIEN" <> 0
                 ) ABC
    ;

END $$
;

SELECT 

"SO_DON_HANG" AS "SO_DON_HANG",
"NGAY_HACH_TOAN" AS "NGAY_HACH_TOAN",
"NGAY_CHUNG_TU" AS "NGAY_CHUNG_TU",
"SO_CHUNG_TU" AS "SO_CHUNG_TU",
"DIEN_GIAI" AS "DIEN_GIAI",
"SO_TIEN" AS "SO_TIEN",
"isbold" AS "isbold",
"ID_CHUNG_TU" AS "ID_GOC",
"MODEL_CHUNG_TU" AS "MODEL_GOC"

FROM TMP_KET_QUA

ORDER BY RowNum
OFFSET %(offset)s
LIMIT %(limit)s;
;
        """
        return self.execute(query,params_sql)

    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        # self._validate()
        self._validate()
        TU_NGAY_F = self.get_vntime('TU')
        DEN_NGAY_F = self.get_vntime('DEN')
        param = 'Từ ngày: %s đến ngày %s' % (TU_NGAY_F, DEN_NGAY_F)
        action = self.env.ref('bao_cao.open_report_chi_tiet_lai_lo_theo_don_hang').read()[0]
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action