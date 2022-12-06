# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class bao_cao_chi_tiet_lai_lo_theo_hop_dong(models.Model):
    _name = 'bao.cao.chi.tiet.lai.lo.theo.hop.dong'
    _description = ''
    _inherit = ['mail.thread']
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh', required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI', required='True')
    TU = fields.Date(string='Từ ', help='Từ ', required='True', default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến', required='True', default=fields.Datetime.now)

    RowNum = fields.Integer(string='RowNum', help='RowNum')
    STT = fields.Char(string='STT', help='SortOrder')
    TEN_CHI_TIEU = fields.Char(string='TEN_CHI_TIEU')
    HOP_DONG_ID = fields.Integer(string='HOP_DONG_ID')
    SO_HOP_DONG = fields.Char(string='SO_HOP_DONG', help='ContractCode')
    NGAY_KY = fields.Date(string='NGAY_KY')
    TRICH_YEU = fields.Char(string='TRICH_YEU')
    DOI_TUONG_ID = fields.Integer(string='DOI_TUONG_ID')
    MA_KHACH_HANG = fields.Char(string='MA_KHACH_HANG')
    TEN_KHACH_HANG = fields.Char(string='TEN_KHACH_HANG')
    SO_CHUNG_TU = fields.Char(string='SO_CHUNG_TU', help='RefNo')
    ID_CHUNG_TU = fields.Integer(string='ID_CHUNG_TU')
    MODEL_CHUNG_TU = fields.Char(string='MODEL_CHUNG_TU')
    LOAI_CHUNG_TU = fields.Char(string='LOAI_CHUNG_TU')
    NGAY_HACH_TOAN = fields.Date(string='NGAY_HACH_TOAN', help='PostedDate')
    NGAY_CHUNG_TU = fields.Date(string='NGAY_CHUNG_TU', help='RefDate')
    NGAY_HOA_DON = fields.Date(string='NGAY_HOA_DON', help='InvDate')
    SO_HOA_DON = fields.Char(string='SO_HOA_DON', help='InvNo')
    DIEN_GIAI = fields.Char(string='DIEN_GIAI', help='JournalMemo')
    SO_TIEN = fields.Float(string='SO_TIEN', help='Amount',digits=decimal_precision.get_precision('VND'))
    isbold = fields.Boolean(string='isbold', help='IsBold')

    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')

    CHON_TAT_CA_HOP_DONG = fields.Boolean('Tất cả hợp đồng', default=True)
    HOP_DONG_MANY_IDS = fields.Many2many('sale.ex.hop.dong.ban','chi_tiet_lai_lo_theo_hd_hdb', string='Chọn hợp đồng')
    HOP_DONG_IDS = fields.One2many('sale.ex.hop.dong.ban')

    # Hợp đồng
    @api.onchange('HOP_DONG_IDS')
    def update_HOP_DONG_IDS(self):
        self.HOP_DONG_MANY_IDS =self.HOP_DONG_IDS.ids
        
    @api.onchange('HOP_DONG_MANY_IDS')
    def _onchange_HOP_DONG_MANY_IDS(self):
        self.HOP_DONG_IDS = self.HOP_DONG_MANY_IDS.ids
    # end  

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')

    @api.model
    def default_get(self, fields_list):
        result = super(bao_cao_chi_tiet_lai_lo_theo_hop_dong, self).default_get(fields_list)
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

        CHON_TAT_CA_HOP_DONG = params['CHON_TAT_CA_HOP_DONG'] if 'CHON_TAT_CA_HOP_DONG' in params.keys() else 'False'
        HOP_DONG_MANY_IDS = params['HOP_DONG_MANY_IDS'] if 'HOP_DONG_MANY_IDS' in params.keys() else 'False'
        
        if(TU_NGAY=='False'):
            raise ValidationError('<Từ ngày> không được bỏ trống.')
        elif(DEN_NGAY=='False'):
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        elif(TU_NGAY_F > DEN_NGAY_F):
            raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')

        if CHON_TAT_CA_HOP_DONG == 'False':
            if HOP_DONG_MANY_IDS == []:
                raise ValidationError('Bạn chưa chọn <Hợp đồng>. Xin vui lòng chọn lại.')

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
       
        if params.get('CHON_TAT_CA_HOP_DONG'):
            domain = []
            HOP_DONG_IDS = self.env['sale.ex.hop.dong.ban'].search(domain).ids
        else:
            HOP_DONG_IDS = params.get('HOP_DONG_MANY_IDS')

        params_sql = {
            'TU_NGAY':TU_NGAY_F, 
            'DEN_NGAY':DEN_NGAY_F, 
            'HOP_DONG_IDS':HOP_DONG_IDS, 
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'CHI_NHANH_ID':CHI_NHANH_ID,
            'limit': limit,
            'offset': offset, 
            }   
        
        query = """DO LANGUAGE plpgsql $$
DECLARE
    tu_ngay                             TIMESTAMP := %(TU_NGAY)s;

    --tham số từ

    den_ngay                            TIMESTAMP := %(DEN_NGAY)s;

    --tham số đến

    bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    --tham số bao gồm số liệu chi nhánh phụ thuộc

    chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s; 

    --tham số chi nhánh

    CHE_DO_KE_TOAN                      VARCHAR;

    BAO_CAO_ID                          VARCHAR :='CTIncomeDetailByContract';

    TU_NGAY_BAT_DAU_TAI_CHINH           DATE;


BEGIN

    SELECT value
    INTO CHE_DO_KE_TOAN
    FROM ir_config_parameter
    WHERE key = 'he_thong.CHE_DO_KE_TOAN'
    FETCH FIRST 1 ROW ONLY
    ;

    SELECT value
    INTO TU_NGAY_BAT_DAU_TAI_CHINH
    FROM ir_config_parameter
    WHERE key = 'he_thong.TU_NGAY_BAT_DAU_TAI_CHINH'
    FETCH FIRST 1 ROW ONLY
    ;

    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


    DROP TABLE IF EXISTS TMP_HOP_DONG_DU_AN_DUOC_CHON
    ;

    CREATE TEMP TABLE TMP_HOP_DONG_DU_AN_DUOC_CHON


    (
        "HOP_DONG_ID"      INT PRIMARY KEY,
        "SO_HOP_DONG"      VARCHAR(50),
        "THUOC_DU_AN_ID"   INT,
        "NGAY_KY"          TIMESTAMP,
        "TRICH_YEU"        VARCHAR(255)
        ,
        "DOI_TUONG_ID"     INT,

        "DOANH_THU_LUY_KE" DECIMAL(18, 4),
        "LUY_KE_CHI_PHI"   DECIMAL(18, 4),
        "CHI_PHI_KHAC"     DECIMAL(18, 4)

        ,
        "TEN_KHACH_HANG"   VARCHAR(255)
    )
    ;

    INSERT INTO TMP_HOP_DONG_DU_AN_DUOC_CHON
        SELECT
            C."id"
            , C."SO_HOP_DONG"
            , c."THUOC_DU_AN_ID"
            , C."NGAY_KY"
            , C."TRICH_YEU"
            , C."KHACH_HANG_ID"
            , C."DOANH_THU"
            , C."GIA_VON_HANG_BAN"
            , C."CHI_PHI_KHAC"

            , C."TEN_KHACH_HANG" AS "TEN_KHACH_HANG_DUOC_CHON"
        FROM sale_ex_hop_dong_ban C
        WHERE C."id" = any(%(HOP_DONG_IDS)s) --HOP_DONG_IDS
    ;


    DROP TABLE IF EXISTS TMP_DS_HOP_DONG
    ;

    CREATE TEMP TABLE TMP_DS_HOP_DONG


    (
        "HOP_DONG_ID"      INT PRIMARY KEY,
        "THUOC_DU_AN_ID"   INT,

        "DOANH_THU_LUY_KE" DECIMAL(18, 4),
        "LUY_KE_CHI_PHI"   DECIMAL(18, 4),
        "CHI_PHI_KHAC"     DECIMAL(18, 4)
    )
    ;

    INSERT INTO TMP_DS_HOP_DONG
        SELECT DISTINCT
            C."id"
            , C."THUOC_DU_AN_ID"
            , C."DOANH_THU"
            , C."GIA_VON_HANG_BAN"
            , C."CHI_PHI_KHAC"
        FROM TMP_HOP_DONG_DU_AN_DUOC_CHON tSC
            INNER JOIN sale_ex_hop_dong_ban C ON C."id" = tSC."HOP_DONG_ID"
                                                 OR C."THUOC_DU_AN_ID" = tSC."HOP_DONG_ID"
    ;


    UPDATE TMP_HOP_DONG_DU_AN_DUOC_CHON S1
    SET "DOANH_THU_LUY_KE" = A."DOANH_THU_LUY_KE" + S."DOANH_THU_LUY_KE",
        "LUY_KE_CHI_PHI"   = A."LUY_KE_CHI_PHI" + S."LUY_KE_CHI_PHI",
        "CHI_PHI_KHAC"     = A."CHI_PHI_KHAC" + S."CHI_PHI_KHAC"
    FROM TMP_HOP_DONG_DU_AN_DUOC_CHON S
        JOIN (SELECT
                    C."THUOC_DU_AN_ID"        AS "HOP_DONG_ID"
                  , SUM(C."DOANH_THU_LUY_KE") AS "DOANH_THU_LUY_KE"
                  , SUM(C."LUY_KE_CHI_PHI")   AS "LUY_KE_CHI_PHI"
                  , SUM(C."CHI_PHI_KHAC")     AS "CHI_PHI_KHAC"
              FROM TMP_DS_HOP_DONG C

              WHERE C."THUOC_DU_AN_ID" IS NOT NULL
              GROUP BY C."THUOC_DU_AN_ID"
             ) AS A ON S."HOP_DONG_ID" = A."HOP_DONG_ID"
    WHERE S1."HOP_DONG_ID" = S."HOP_DONG_ID"
    ;


    DROP TABLE IF EXISTS TMP_CHUNG_TU_GHI_SO_DA_TINH_PHAN_BO
    ;

    CREATE TEMP TABLE TMP_CHUNG_TU_GHI_SO_DA_TINH_PHAN_BO


    (
        "STT"                            VARCHAR(20), --NVTOAN modify '12'/05/2017
        "TEN_CHI_TIEU"                    VARCHAR(255)
        ,
        "HOP_DONG_ID"                     INT,
        "THUOC_DU_AN_ID"                  INT,
        "NGAY_HACH_TOAN"                  TIMESTAMP,
        "NGAY_CHUNG_TU"                   TIMESTAMP,
        "SO_CHUNG_TU"                     VARCHAR(20),
        "ID_CHUNG_TU"                     INT,
        "MODEL_CHUNG_TU"                  VARCHAR(255),
        "LOAI_CHUNG_TU"                   VARCHAR(255),
        "NGAY_HOA_DON"                    TIMESTAMP,
        "SO_HOA_DON"                      VARCHAR(500),
        "DIEN_GIAI"                       VARCHAR(255),
        "SO_TIEN"                         FLOAT,
        "SO_TIEN_LUY_KE"                  FLOAT,
        "CAU_HINH_LAI_LO_CHO_CT_HD_DH_ID" INT,
        "MA_CHI_TIEU_DINH_DANH"           VARCHAR(20)

    )
    ;

    INSERT INTO TMP_CHUNG_TU_GHI_SO_DA_TINH_PHAN_BO
        SELECT
              CASE CAST(SRT."sequence" AS VARCHAR(20))
              WHEN '10'
                  THEN '90'
              WHEN '11'
                  THEN '91'
              WHEN '12'
                  THEN '92'
              WHEN '13'
                  THEN '93'
              ELSE CAST(SRT."sequence" AS VARCHAR(20))
              END                                             AS "STT"
            , SRT."TEN_CHI_TIEU"
            , GL."HOP_DONG_ID"
            , COALESCE(LC."THUOC_DU_AN_ID", LC."HOP_DONG_ID") AS "THUOC_DU_AN_ID"
            , GL."NGAY_HACH_TOAN"
            , GL."NGAY_CHUNG_TU"
            , GL."SO_CHUNG_TU"
            , GL."ID_CHUNG_TU"
            , GL."MODEL_CHUNG_TU"
            , GL."LOAI_CHUNG_TU"
            , GL."NGAY_HOA_DON"
            , GL."SO_HOA_DON"
            , GL."DIEN_GIAI"
            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            THEN GL."SO_TIEN"
                  ELSE 0
                  END)                                           "SO_TIEN"
            , SUM(GL."SO_TIEN")                                  "SO_TIEN_LUY_KE"
            , GL."MA_BAO_CAO_VAT_TU_ID"
            , SRT."MA_CHI_TIEU_DINH_DANH"

        FROM tien_ich_cau_hinh_lai_lo_cho_ct_hd_dh SRT
            LEFT JOIN LAY_SO_LIEU_SO_CAI_THEO_CT_THIET_LAP_BCTC_TRA_VE(NULL,
                                                                       TU_NGAY_BAT_DAU_TAI_CHINH,
                                                                       den_ngay,
                                                                       BAO_CAO_ID, NULL,
                                                                       chi_nhanh_id,
                                                                       bao_gom_du_lieu_chi_nhanh_phu_thuoc
                      ) GL ON GL."MA_BAO_CAO_VAT_TU_ID" = SRT.id
            INNER JOIN TMP_DS_HOP_DONG LC ON LC."HOP_DONG_ID" = GL."HOP_DONG_ID" --AND LC."THUOC_DU_AN_ID" IS NULL
        GROUP BY CASE CAST(SRT."sequence" AS VARCHAR(20))
                 WHEN '10'
                     THEN '90'
                 WHEN '11'
                     THEN '91'
                 WHEN '12'
                     THEN '92'
                 WHEN '13'
                     THEN '93'
                 ELSE CAST(SRT."sequence" AS VARCHAR(20))
                 END,
            SRT."TEN_CHI_TIEU",
            GL."HOP_DONG_ID",
            COALESCE(LC."THUOC_DU_AN_ID", LC."HOP_DONG_ID"),
            GL."NGAY_HACH_TOAN",
            GL."NGAY_CHUNG_TU",
            GL."SO_CHUNG_TU",
            GL."ID_CHUNG_TU",
            GL."MODEL_CHUNG_TU",
            GL."LOAI_CHUNG_TU",
            GL."NGAY_HOA_DON",
            GL."SO_HOA_DON",
            GL."DIEN_GIAI",
            GL."MA_BAO_CAO_VAT_TU_ID",
            SRT."MA_CHI_TIEU_DINH_DANH"

        UNION ALL
        SELECT
              CASE CAST(SRT."sequence" AS VARCHAR(20))
              WHEN '10'
                  THEN '90'
              WHEN '11'
                  THEN '91'
              WHEN '12'
                  THEN '92'
              WHEN '13'
                  THEN '93'
              ELSE CAST(SRT."sequence" AS VARCHAR(20))
              END      AS       "STT"
            , SRT."TEN_CHI_TIEU"
            , LC."THUOC_DU_AN_ID"
            , LC."THUOC_DU_AN_ID"
            , GL."NGAY_HACH_TOAN"
            , GL."NGAY_CHUNG_TU"
            , GL."SO_CHUNG_TU"
            , GL."ID_CHUNG_TU"
            , GL."MODEL_CHUNG_TU"
            , GL."LOAI_CHUNG_TU"
            , GL."NGAY_HOA_DON"
            , GL."SO_HOA_DON"
            , GL."DIEN_GIAI"
            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            THEN GL."SO_TIEN"
                  ELSE 0
                  END) AS       "SO_TIEN"
            , SUM(GL."SO_TIEN") "SO_TIEN_LUY_KE"
            , GL."MA_BAO_CAO_VAT_TU_ID"
            , SRT."MA_CHI_TIEU_DINH_DANH"

        FROM tien_ich_cau_hinh_lai_lo_cho_ct_hd_dh SRT
            LEFT JOIN LAY_SO_LIEU_SO_CAI_THEO_CT_THIET_LAP_BCTC_TRA_VE(NULL,
                                                                       TU_NGAY_BAT_DAU_TAI_CHINH,
                                                                       den_ngay,
                                                                       BAO_CAO_ID, NULL,
                                                                       chi_nhanh_id,
                                                                       bao_gom_du_lieu_chi_nhanh_phu_thuoc) GL
                ON GL."MA_BAO_CAO_VAT_TU_ID" = SRT.id
            INNER JOIN TMP_DS_HOP_DONG LC ON LC."HOP_DONG_ID" = GL."HOP_DONG_ID"
                                             AND LC."THUOC_DU_AN_ID" IS NOT NULL
        GROUP BY CASE CAST(SRT."sequence" AS VARCHAR(20))
                 WHEN '10'
                     THEN '90'
                 WHEN '11'
                     THEN '91'
                 WHEN '12'
                     THEN '92'
                 WHEN '13'
                     THEN '93'
                 ELSE CAST(SRT."sequence" AS VARCHAR(20))
                 END, --NVTOAN Modify '13'/05/2017
            SRT."TEN_CHI_TIEU",
            GL."HOP_DONG_ID",
            LC."THUOC_DU_AN_ID",
            GL."NGAY_HACH_TOAN",
            GL."NGAY_CHUNG_TU",
            GL."SO_CHUNG_TU",
            GL."ID_CHUNG_TU",
            GL."MODEL_CHUNG_TU",
            GL."LOAI_CHUNG_TU",
            GL."NGAY_HOA_DON",
            GL."SO_HOA_DON",
            GL."DIEN_GIAI",
            GL."MA_BAO_CAO_VAT_TU_ID",
            SRT."MA_CHI_TIEU_DINH_DANH"


        UNION ALL
        SELECT
              '7'                                                             "STT"
            , N'Giá vốn hàng bán'                                          "TEN_CHI_TIEU"
            , JCAEDT."MA_DON_VI_ID"                                         "HOP_DONG_ID"
            , LC."THUOC_DU_AN_ID"
            , JCAE."NGAY_CHUNG_TU"                                          "NGAY_HACH_TOAN"
            , JCAE."NGAY_CHUNG_TU"
            , JCAE."SO_CHUNG_TU"
            , JCAE."id"
            , 'tong.hop.phan.bo.chi.phi.bh.qldn.chi.phi.khac.cho.don.vi' AS "MODEL_CHUNG_TU"
            , CAST(JCAE."LOAI_CHUNG_TU" AS VARCHAR(255))
            , NULL :: TIMESTAMP                                             "NGAY_HOA_DON"
            , NULL                                                          "SO_HOA_DON"
            , JCAE."DIEN_GIAI"
            , SUM(CASE WHEN JCAE."NGAY_CHUNG_TU" BETWEEN tu_ngay AND den_ngay
            THEN JCAEDT."SO_TIEN"
                  ELSE 0
                  END)                                                   AS "SO_TIEN"
            , SUM(JCAEDT."SO_TIEN")                                         "SO_TIEN_LUY_KE"
            , NULL :: INT                                                   ReportItemID
            , '03'                                                          "MA_CHI_TIEU_DINH_DANH"

        FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JCAE
            INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCAEDT
                ON JCAEDT."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JCAE."id"
            INNER JOIN TMP_DS_HOP_DONG LC ON LC."HOP_DONG_ID" = JCAEDT."MA_DON_VI_ID"
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCAE."CHI_NHANH_ID"
        WHERE JCAEDT."CAP_TO_CHUC" = '3'
              AND JCAE."NGAY_CHUNG_TU" BETWEEN TU_NGAY_BAT_DAU_TAI_CHINH AND den_ngay
              AND (SELECT "SO_TAI_KHOAN"
                   FROM danh_muc_he_thong_tai_khoan TK
                   WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '632%%'

        GROUP BY
            JCAEDT."MA_DON_VI_ID",
            LC."THUOC_DU_AN_ID",
            JCAE."NGAY_CHUNG_TU",
            JCAE."SO_CHUNG_TU",
            JCAE."id",
            CAST(JCAE."LOAI_CHUNG_TU" AS VARCHAR(255)),
            JCAE."DIEN_GIAI"

        /*các hợp đồng con của dự án*/
        UNION ALL
        SELECT
              '7'                                                             "STT"
            , --NVTOAN modify '12'/05/2017
              N'Giá vốn hàng bán'                                          "TEN_CHI_TIEU"
            , LC."THUOC_DU_AN_ID"                                        AS "HOP_DONG_ID"
            , LC."THUOC_DU_AN_ID"
            , JCAE."NGAY_CHUNG_TU"                                          "NGAY_HACH_TOAN"
            , JCAE."NGAY_CHUNG_TU"
            , JCAE."SO_CHUNG_TU"
            , JCAE."id"
            , 'tong.hop.phan.bo.chi.phi.bh.qldn.chi.phi.khac.cho.don.vi' AS "MODEL_CHUNG_TU"
            , CAST(JCAE."LOAI_CHUNG_TU" AS VARCHAR(255))
            , NULL :: TIMESTAMP                                             "NGAY_HOA_DON"
            , NULL                                                          "SO_HOA_DON"
            , JCAE."DIEN_GIAI"
            , SUM(CASE WHEN JCAE."NGAY_CHUNG_TU" BETWEEN tu_ngay AND den_ngay
            THEN JCAEDT."SO_TIEN"
                  ELSE 0
                  END)                                                   AS "SO_TIEN"
            , SUM(JCAEDT."SO_TIEN")                                         "SO_TIEN_LUY_KE"
            , NULL                                                          ReportItemID
            , '03'                                                          "MA_CHI_TIEU_DINH_DANH"

        FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JCAE
            INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCAEDT
                ON JCAEDT."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JCAE."id"
            INNER JOIN TMP_DS_HOP_DONG LC ON LC."HOP_DONG_ID" = JCAEDT."MA_DON_VI_ID"
                                             AND LC."THUOC_DU_AN_ID" IS NOT NULL
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCAE."CHI_NHANH_ID"
        WHERE JCAEDT."CAP_TO_CHUC" = '3'
              AND JCAE."NGAY_CHUNG_TU" BETWEEN TU_NGAY_BAT_DAU_TAI_CHINH AND den_ngay
              AND (SELECT "SO_TAI_KHOAN"
                   FROM danh_muc_he_thong_tai_khoan TK
                   WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '632%%'

        GROUP BY
            JCAEDT."MA_DON_VI_ID",
            LC."THUOC_DU_AN_ID",
            JCAE."NGAY_CHUNG_TU",
            JCAE."SO_CHUNG_TU",
            JCAE."id",
            CAST(JCAE."LOAI_CHUNG_TU" AS VARCHAR(255)),
            JCAE."DIEN_GIAI"

        UNION ALL
        SELECT
              '90'                                                            "STT"
            , --NVTOAN modify '12'/05/2017
              N'Chi phí khác'                                              "TEN_CHI_TIEU"
            , JCAEDT."MA_DON_VI_ID"                                         "HOP_DONG_ID"
            , LC."THUOC_DU_AN_ID"
            , JCAE."NGAY_CHUNG_TU"                                          "NGAY_HACH_TOAN"
            , JCAE."NGAY_CHUNG_TU"
            , JCAE."SO_CHUNG_TU"
            , JCAE."id"
            , 'tong.hop.phan.bo.chi.phi.bh.qldn.chi.phi.khac.cho.don.vi' AS "MODEL_CHUNG_TU"
            , CAST(JCAE."LOAI_CHUNG_TU" AS VARCHAR(255))
            , NULL :: TIMESTAMP                                             "NGAY_HOA_DON"
            , NULL                                                          "SO_HOA_DON"
            , JCAE."DIEN_GIAI"
            , SUM(CASE WHEN JCAE."NGAY_CHUNG_TU" BETWEEN tu_ngay AND den_ngay
            THEN CASE WHEN CHE_DO_KE_TOAN = '15'
                           AND LEFT((SELECT "SO_TAI_KHOAN"
                                     FROM danh_muc_he_thong_tai_khoan TK
                                     WHERE TK.id = JCAEDT."TAI_KHOAN_ID"),
                                    3) IN ('641', '642',
                                           '811', '635')
                THEN JCAEDT."SO_TIEN"
                 WHEN CHE_DO_KE_TOAN = '48'
                      AND LEFT((SELECT "SO_TAI_KHOAN"
                                FROM danh_muc_he_thong_tai_khoan TK
                                WHERE TK.id = JCAEDT."TAI_KHOAN_ID"),
                               3) IN ('642', '811',
                                      '635')
                     THEN JCAEDT."SO_TIEN"
                 ELSE 0
                 END
                  ELSE 0
                  END)                                                   AS "SO_TIEN"
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
                  END)                                                      "SO_TIEN_LUY_KE"
            , NULL                                                          ReportItemID
            , '04'                                                          "MA_CHI_TIEU_DINH_DANH"

        FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JCAE
            INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCAEDT
                ON JCAEDT."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JCAE."id"
            INNER JOIN TMP_DS_HOP_DONG LC ON LC."HOP_DONG_ID" = JCAEDT."MA_DON_VI_ID"
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCAE."CHI_NHANH_ID"
        WHERE JCAEDT."CAP_TO_CHUC" = '3'
              AND JCAE."NGAY_CHUNG_TU" BETWEEN TU_NGAY_BAT_DAU_TAI_CHINH AND den_ngay
              AND LEFT((SELECT "SO_TAI_KHOAN"
                        FROM danh_muc_he_thong_tai_khoan TK
                        WHERE TK.id = JCAEDT."TAI_KHOAN_ID"), 3) IN ('641', '642',
                                                                     '811', '635')

        GROUP BY JCAEDT."MA_DON_VI_ID",
            LC."THUOC_DU_AN_ID",
            JCAE."NGAY_CHUNG_TU",
            JCAE."SO_CHUNG_TU",
            JCAE."id",
            CAST(JCAE."LOAI_CHUNG_TU" AS VARCHAR(255)),
            JCAE."DIEN_GIAI"


        UNION ALL
        /*hợp đồng con của dự án*/
        SELECT
              '90'                                                            "STT"
            , N'Chi phí khác'                                              "TEN_CHI_TIEU"
            , LC."THUOC_DU_AN_ID"                                        AS "HOP_DONG_ID"
            , LC."THUOC_DU_AN_ID"
            , JCAE."NGAY_CHUNG_TU"                                          "NGAY_HACH_TOAN"
            , JCAE."NGAY_CHUNG_TU"
            , JCAE."SO_CHUNG_TU"
            , JCAE."id"
            , 'tong.hop.phan.bo.chi.phi.bh.qldn.chi.phi.khac.cho.don.vi' AS "MODEL_CHUNG_TU"
            , CAST(JCAE."LOAI_CHUNG_TU" AS VARCHAR(255))
            , NULL :: TIMESTAMP                                             "NGAY_HOA_DON"
            , NULL                                                          "SO_HOA_DON"
            , JCAE."DIEN_GIAI"
            , SUM(CASE WHEN JCAE."NGAY_CHUNG_TU" BETWEEN tu_ngay AND den_ngay
            THEN CASE WHEN CHE_DO_KE_TOAN = '15'
                           AND LEFT((SELECT "SO_TAI_KHOAN"
                                     FROM danh_muc_he_thong_tai_khoan TK
                                     WHERE TK.id = JCAEDT."TAI_KHOAN_ID"),
                                    3) IN ('641', '642',
                                           '811', '635')
                THEN JCAEDT."SO_TIEN"
                 WHEN CHE_DO_KE_TOAN = '48'
                      AND LEFT((SELECT "SO_TAI_KHOAN"
                                FROM danh_muc_he_thong_tai_khoan TK
                                WHERE TK.id = JCAEDT."TAI_KHOAN_ID"),
                               3) IN ('642', '811',
                                      '635')
                     THEN JCAEDT."SO_TIEN"
                 ELSE 0
                 END
                  ELSE 0
                  END)                                                   AS "SO_TIEN"
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
                  END)                                                      "SO_TIEN_LUY_KE"
            , NULL                                                          ReportItemID
            , '04'                                                          "MA_CHI_TIEU_DINH_DANH"

        FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JCAE
            INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCAEDT
                ON JCAEDT."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JCAE."id"
            INNER JOIN TMP_DS_HOP_DONG LC ON LC."HOP_DONG_ID" = JCAEDT."MA_DON_VI_ID"
                                             AND LC."THUOC_DU_AN_ID" IS NOT NULL
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCAE."CHI_NHANH_ID"
        WHERE JCAEDT."CAP_TO_CHUC" = '3'
              AND JCAE."NGAY_CHUNG_TU" BETWEEN TU_NGAY_BAT_DAU_TAI_CHINH AND den_ngay
              AND LEFT((SELECT "SO_TAI_KHOAN"
                        FROM danh_muc_he_thong_tai_khoan TK
                        WHERE TK.id = JCAEDT."TAI_KHOAN_ID"), 3) IN ('641', '642',
                                                                     '811', '635')

        GROUP BY
            JCAEDT."MA_DON_VI_ID",
            LC."THUOC_DU_AN_ID",
            JCAE."NGAY_CHUNG_TU",
            JCAE."SO_CHUNG_TU",
            JCAE."id",
            CAST(JCAE."LOAI_CHUNG_TU" AS VARCHAR(255)),
            JCAE."DIEN_GIAI"

    ;


    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA


    (
        "STT"            VARCHAR(20), --NVTOAN modify '12'/05/2017
        "TEN_CHI_TIEU"   VARCHAR(255),
        "HOP_DONG_ID"    INT,
        "SO_HOP_DONG"    VARCHAR(255),
        "NGAY_KY"        TIMESTAMP,
        "TRICH_YEU"      VARCHAR(255),
        "DOI_TUONG_ID"   INT,

        "TEN_KHACH_HANG" VARCHAR(255),
        "SO_CHUNG_TU"    VARCHAR(255),
        "ID_CHUNG_TU"    INT,
        "MODEL_CHUNG_TU" VARCHAR(255),
        "LOAI_CHUNG_TU"  VARCHAR(255),
        "NGAY_HACH_TOAN" TIMESTAMP,
        "NGAY_CHUNG_TU"  TIMESTAMP,
        "NGAY_HOA_DON"   TIMESTAMP,
        "SO_HOA_DON"     VARCHAR,
        "DIEN_GIAI"      VARCHAR(255),
        "SO_TIEN"        DECIMAL(18, 4),
        IsBold           BOOLEAN

    )
    ;


    INSERT INTO TMP_KET_QUA
        SELECT
              '0'                                  "STT"
            , --NVTOAN modify '12'/05/2017
              N'DOANH THU LŨY KẾ'                 "TEN_CHI_TIEU"
            , C."HOP_DONG_ID"
            , C."SO_HOP_DONG"
            , C."NGAY_KY"
            , C."TRICH_YEU"
            , C."DOI_TUONG_ID"
            , /*Rem by hoant 28.'10'.2017 theo cr 150432 lấy tên "TEN_KHACH_HANG" trên form Hợp đồng đến cuối thì join*/
            /*
            C."MA_KHACH_HANG" ,*/
            C."TEN_KHACH_HANG"
            , NULL                                 "SO_CHUNG_TU"
            , NULL :: INT                          "ID_CHUNG_TU"
            , NULL                                 "MODEL_CHUNG_TU"
            , NULL                                 "LOAI_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HACH_TOAN"
            , NULL :: TIMESTAMP                    "NGAY_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HOA_DON"
            , NULL                                 "SO_HOA_DON"
            , N'DOANH THU LŨY KẾ'                 "DIEN_GIAI"
            , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" IN ('01.01', '01.03') --NVTOAN modify '12'/05/2017
            THEN GL."SO_TIEN_LUY_KE"
                  WHEN GL."MA_CHI_TIEU_DINH_DANH" = '01.02'
                      THEN -1 * GL."SO_TIEN_LUY_KE"
                  ELSE 0
                  END) + (C."DOANH_THU_LUY_KE") AS "SO_TIEN"
            , CAST(1 AS BOOLEAN)                   IsBold

        FROM TMP_CHUNG_TU_GHI_SO_DA_TINH_PHAN_BO GL --CROSS APPLY

            INNER JOIN TMP_HOP_DONG_DU_AN_DUOC_CHON C ON GL."HOP_DONG_ID" = C."HOP_DONG_ID"


        GROUP BY
            C."HOP_DONG_ID",
            C."SO_HOP_DONG",
            C."NGAY_KY",
            C."TRICH_YEU",
            C."DOI_TUONG_ID",
            /*
            C."MA_KHACH_HANG" ,*/
            C."TEN_KHACH_HANG",
            C."DOANH_THU_LUY_KE"
        UNION ALL
        SELECT
              '1'                "STT"
            , --NVTOAN modify '12'/05/2017
              'DOANH THU'        "TEN_CHI_TIEU"
            , C."HOP_DONG_ID"
            , C."SO_HOP_DONG"
            , C."NGAY_KY"
            , C."TRICH_YEU"
            , C."DOI_TUONG_ID"
            , C."TEN_KHACH_HANG"
             , NULL                                 "SO_CHUNG_TU"
            , NULL :: INT                          "ID_CHUNG_TU"
            , NULL                                 "MODEL_CHUNG_TU"
            , NULL                                 "LOAI_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HACH_TOAN"
            , NULL :: TIMESTAMP                    "NGAY_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HOA_DON"
            , NULL                                 "SO_HOA_DON"
            , 'DOANH THU'        "DIEN_GIAI"
            , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" IN ('01.01', '01.03') --NVTOAN modify '12'/05/2017
            THEN GL."SO_TIEN"
                  WHEN GL."MA_CHI_TIEU_DINH_DANH" = '01.02'
                      THEN -1 * GL."SO_TIEN"
                  ELSE 0
                  END)           "SO_TIEN"
            , CAST(1 AS BOOLEAN) IsBold

        FROM TMP_CHUNG_TU_GHI_SO_DA_TINH_PHAN_BO GL --CROSS APPLY

            INNER JOIN TMP_HOP_DONG_DU_AN_DUOC_CHON C ON GL."HOP_DONG_ID" = C."HOP_DONG_ID"


        GROUP BY C."HOP_DONG_ID",
            C."SO_HOP_DONG",
            C."NGAY_KY",
            C."TRICH_YEU",
            C."DOI_TUONG_ID",

            C."TEN_KHACH_HANG"
        UNION ALL

        SELECT
              '1.01'                             "STT"
            , --NVTOAN modify '12'/05/2017
              N'Doanh thu bán hàng, dịch vụ' AS "TEN_CHI_TIEU"
            , C."HOP_DONG_ID"
            , C."SO_HOP_DONG"
            , C."NGAY_KY"
            , C."TRICH_YEU"
            , C."DOI_TUONG_ID"
            , C."TEN_KHACH_HANG"
            , NULL                                 "SO_CHUNG_TU"
            , NULL :: INT                          "ID_CHUNG_TU"
            , NULL                                 "MODEL_CHUNG_TU"
            , NULL                                 "LOAI_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HACH_TOAN"
            , NULL :: TIMESTAMP                    "NGAY_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HOA_DON"
            , NULL                                 "SO_HOA_DON"
            , N'Doanh thu bán hàng, dịch vụ'    "DIEN_GIAI"
            , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '01.01'
            THEN GL."SO_TIEN"
                  ELSE 0
                  END)                           "SO_TIEN"
            , CAST(1 AS BOOLEAN)                 IsBold

        FROM TMP_CHUNG_TU_GHI_SO_DA_TINH_PHAN_BO GL --CROSS APPLY
            /*Rem by hoant 28.'10'.2017 theo cr 150432 lấy tên "TEN_KHACH_HANG" trên form Hợp đồng thay bằng inner join TMP_HOP_DONG_DU_AN_DUOC_CHON */
            INNER JOIN TMP_HOP_DONG_DU_AN_DUOC_CHON C ON GL."HOP_DONG_ID" = C."HOP_DONG_ID"

        GROUP BY C."HOP_DONG_ID",
            C."SO_HOP_DONG",
            C."NGAY_KY",
            C."TRICH_YEU",
            C."DOI_TUONG_ID",
            /*C."MA_KHACH_HANG" ,*/
            C."TEN_KHACH_HANG"
        UNION ALL
        SELECT
              '1.02'                              "STT"
            , --NVTOAN modify '12'/05/2017
              N'Các khoản giảm trừ doanh thu' AS "TEN_CHI_TIEU"
            , C."HOP_DONG_ID"
            , C."SO_HOP_DONG"
            , C."NGAY_KY"
            , C."TRICH_YEU"
            , C."DOI_TUONG_ID"
            , C."TEN_KHACH_HANG"
            , NULL                                 "SO_CHUNG_TU"
            , NULL :: INT                          "ID_CHUNG_TU"
            , NULL                                 "MODEL_CHUNG_TU"
            , NULL                                 "LOAI_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HACH_TOAN"
            , NULL :: TIMESTAMP                    "NGAY_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HOA_DON"
            , NULL                                 "SO_HOA_DON"
            , N'Các khoản giảm trừ doanh thu'    "DIEN_GIAI"
            , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '01.02'
            THEN GL."SO_TIEN"
                  ELSE 0
                  END)                            "SO_TIEN"
            , CAST(1 AS BOOLEAN)                  IsBold

        FROM TMP_CHUNG_TU_GHI_SO_DA_TINH_PHAN_BO GL --CROSS APPLY
            /*Rem by hoant 28.'10'.2017 theo cr 150432 lấy tên "TEN_KHACH_HANG" trên form Hợp đồng thay bằng inner join TMP_HOP_DONG_DU_AN_DUOC_CHON */
            INNER JOIN TMP_HOP_DONG_DU_AN_DUOC_CHON C ON GL."HOP_DONG_ID" = C."HOP_DONG_ID"

        GROUP BY C."HOP_DONG_ID",
            C."SO_HOP_DONG",
            C."NGAY_KY",
            C."TRICH_YEU",
            C."DOI_TUONG_ID",
            /*C."MA_KHACH_HANG" ,*/
            C."TEN_KHACH_HANG"
        UNION ALL
        SELECT
              '1.03'                          "STT"
            , --NVTOAN modify '12'/05/2017
              N'Doanh thu, thu nhập khác' AS "TEN_CHI_TIEU"
            , C."HOP_DONG_ID"
            , C."SO_HOP_DONG"
            , C."NGAY_KY"
            , C."TRICH_YEU"
            , C."DOI_TUONG_ID"
            , C."TEN_KHACH_HANG"
            , NULL                                 "SO_CHUNG_TU"
            , NULL :: INT                          "ID_CHUNG_TU"
            , NULL                                 "MODEL_CHUNG_TU"
            , NULL                                 "LOAI_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HACH_TOAN"
            , NULL :: TIMESTAMP                    "NGAY_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HOA_DON"
            , NULL                                 "SO_HOA_DON"
            , N'Doanh thu, thu nhập khác'    "DIEN_GIAI"
            , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '01.03'
            THEN GL."SO_TIEN"
                  ELSE 0
                  END)                        "SO_TIEN"
            , CAST(1 AS BOOLEAN)              IsBold

        FROM TMP_CHUNG_TU_GHI_SO_DA_TINH_PHAN_BO GL --CROSS APPLY

            INNER JOIN TMP_HOP_DONG_DU_AN_DUOC_CHON C ON GL."HOP_DONG_ID" = C."HOP_DONG_ID"

        GROUP BY C."HOP_DONG_ID",
            C."SO_HOP_DONG",
            C."NGAY_KY",
            C."TRICH_YEU",
            C."DOI_TUONG_ID",
            /*C."MA_KHACH_HANG" ,*/
            C."TEN_KHACH_HANG"
        UNION ALL
        SELECT
              '3'                                                 "STT"
            , --NVTOAN modify '12'/05/2017
              N'CHI PHÍ LŨY KẾ'                                    "TEN_CHI_TIEU"
            , C."HOP_DONG_ID"
            , C."SO_HOP_DONG"
            , C."NGAY_KY"
            , C."TRICH_YEU"
            , C."DOI_TUONG_ID"
            , C."TEN_KHACH_HANG"
            , NULL                                 "SO_CHUNG_TU"
            , NULL :: INT                          "ID_CHUNG_TU"
            , NULL                                 "MODEL_CHUNG_TU"
            , NULL                                 "LOAI_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HACH_TOAN"
            , NULL :: TIMESTAMP                    "NGAY_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HOA_DON"
            , NULL                                 "SO_HOA_DON"
            , N'CHI PHÍ LŨY KẾ'                                    "DIEN_GIAI"
            , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '03'
                            OR GL."MA_CHI_TIEU_DINH_DANH" = '04'
            THEN GL."SO_TIEN_LUY_KE"
                  ELSE 0
                  END) + (C."LUY_KE_CHI_PHI" + C."CHI_PHI_KHAC") AS "SO_TIEN"
            , CAST(1 AS BOOLEAN)                                    IsBold

        FROM TMP_CHUNG_TU_GHI_SO_DA_TINH_PHAN_BO GL --CROSS APPLY

            INNER JOIN TMP_HOP_DONG_DU_AN_DUOC_CHON C ON GL."HOP_DONG_ID" = C."HOP_DONG_ID"

        GROUP BY C."HOP_DONG_ID",
            C."SO_HOP_DONG",
            C."NGAY_KY",
            C."TRICH_YEU",
            C."DOI_TUONG_ID",

            C."TEN_KHACH_HANG",
            C."LUY_KE_CHI_PHI",
            C."CHI_PHI_KHAC"
        UNION ALL
        SELECT
              '4'                "STT"
            , --NVTOAN modify '12'/05/2017
              N'CHI PHÍ'        "TEN_CHI_TIEU"
            , C."HOP_DONG_ID"
            , C."SO_HOP_DONG"
            , C."NGAY_KY"
            , C."TRICH_YEU"
            , C."DOI_TUONG_ID"
            , C."TEN_KHACH_HANG"
            , NULL                                 "SO_CHUNG_TU"
            , NULL :: INT                          "ID_CHUNG_TU"
            , NULL                                 "MODEL_CHUNG_TU"
            , NULL                                 "LOAI_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HACH_TOAN"
            , NULL :: TIMESTAMP                    "NGAY_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HOA_DON"
            , NULL                                 "SO_HOA_DON"
            , N'CHI PHÍ'        "DIEN_GIAI"
            , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '03'
                            OR GL."MA_CHI_TIEU_DINH_DANH" = '04'
            THEN GL."SO_TIEN"
                  ELSE 0
                  END)           "SO_TIEN"
            , CAST(1 AS BOOLEAN) IsBold

        FROM TMP_CHUNG_TU_GHI_SO_DA_TINH_PHAN_BO GL

            INNER JOIN TMP_HOP_DONG_DU_AN_DUOC_CHON C ON GL."HOP_DONG_ID" = C."HOP_DONG_ID"

        GROUP BY C."HOP_DONG_ID",
            C."SO_HOP_DONG",
            C."NGAY_KY",
            C."TRICH_YEU",
            C."DOI_TUONG_ID",
            /*C."MA_KHACH_HANG" ,*/
            C."TEN_KHACH_HANG"
        UNION ALL
        SELECT
              '5'                               "STT"
            , --NVTOAN modify '12'/05/2017
              N'Giá vốn hàng bán lũy kế'        "TEN_CHI_TIEU"
            , C."HOP_DONG_ID"
            , C."SO_HOP_DONG"
            , C."NGAY_KY"
            , C."TRICH_YEU"
            , C."DOI_TUONG_ID"
            , C."TEN_KHACH_HANG"
            , NULL                                 "SO_CHUNG_TU"
            , NULL :: INT                          "ID_CHUNG_TU"
            , NULL                                 "MODEL_CHUNG_TU"
            , NULL                                 "LOAI_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HACH_TOAN"
            , NULL :: TIMESTAMP                    "NGAY_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HOA_DON"
            , NULL                                 "SO_HOA_DON"
            , N'Giá vốn hàng bán lũy kế'        "DIEN_GIAI"
            , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '03'
            THEN GL."SO_TIEN_LUY_KE"
                  ELSE 0
                  END) + (C."LUY_KE_CHI_PHI") AS "SO_TIEN"
            , CAST(1 AS BOOLEAN)                 IsBold

        FROM TMP_CHUNG_TU_GHI_SO_DA_TINH_PHAN_BO GL

            INNER JOIN TMP_HOP_DONG_DU_AN_DUOC_CHON C ON GL."HOP_DONG_ID" = C."HOP_DONG_ID"

        GROUP BY C."HOP_DONG_ID",
            C."SO_HOP_DONG",
            C."NGAY_KY",
            C."TRICH_YEU",
            C."DOI_TUONG_ID",
            /*
            C."MA_KHACH_HANG" ,*/
            C."TEN_KHACH_HANG",
            C."LUY_KE_CHI_PHI"
        UNION ALL
        SELECT
              '6'                "STT"
            , --NVTOAN modify '12'/05/2017
              N'Giá vốn hàng bán' "TEN_CHI_TIEU"
            , C."HOP_DONG_ID"
            , C."SO_HOP_DONG"
            , C."NGAY_KY"
            , C."TRICH_YEU"
            , C."DOI_TUONG_ID"
            , C."TEN_KHACH_HANG"
            , NULL                                 "SO_CHUNG_TU"
            , NULL :: INT                          "ID_CHUNG_TU"
            , NULL                                 "MODEL_CHUNG_TU"
            , NULL                                 "LOAI_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HACH_TOAN"
            , NULL :: TIMESTAMP                    "NGAY_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HOA_DON"
            , NULL                                 "SO_HOA_DON"
            , N'Giá vốn hàng bán' "DIEN_GIAI"
            , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '03'
            THEN GL."SO_TIEN"
                  ELSE 0
                  END)             "SO_TIEN"
            , CAST(1 AS BOOLEAN)   IsBold

        FROM TMP_CHUNG_TU_GHI_SO_DA_TINH_PHAN_BO GL

            INNER JOIN TMP_HOP_DONG_DU_AN_DUOC_CHON C ON GL."HOP_DONG_ID" = C."HOP_DONG_ID"

        GROUP BY C."HOP_DONG_ID",
            C."SO_HOP_DONG",
            C."NGAY_KY",
            C."TRICH_YEU",
            C."DOI_TUONG_ID",
            /*C."MA_KHACH_HANG" ,*/
            C."TEN_KHACH_HANG"
        UNION ALL
        SELECT
              '8'                             "STT"
            , --NVTOAN modify '12'/05/2017
              N'Chi phí khác lũy kế'          "TEN_CHI_TIEU"
            , C."HOP_DONG_ID"
            , C."SO_HOP_DONG"
            , C."NGAY_KY"
            , C."TRICH_YEU"
            , C."DOI_TUONG_ID"
            , C."TEN_KHACH_HANG"
             , NULL                                 "SO_CHUNG_TU"
            , NULL :: INT                          "ID_CHUNG_TU"
            , NULL                                 "MODEL_CHUNG_TU"
            , NULL                                 "LOAI_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HACH_TOAN"
            , NULL :: TIMESTAMP                    "NGAY_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HOA_DON"
            , NULL                                 "SO_HOA_DON"
            , N'Chi phí khác lũy kế'          "DIEN_GIAI"
            , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '04'
            THEN GL."SO_TIEN_LUY_KE"
                  ELSE 0
                  END) + (C."CHI_PHI_KHAC") AS "SO_TIEN"
            , CAST(1 AS BOOLEAN)               IsBold

        FROM TMP_CHUNG_TU_GHI_SO_DA_TINH_PHAN_BO GL

            INNER JOIN TMP_HOP_DONG_DU_AN_DUOC_CHON C ON GL."HOP_DONG_ID" = C."HOP_DONG_ID"

        GROUP BY C."HOP_DONG_ID",
            C."SO_HOP_DONG",
            C."NGAY_KY",
            C."TRICH_YEU",
            C."DOI_TUONG_ID",

            C."TEN_KHACH_HANG",
            C."CHI_PHI_KHAC"
        UNION ALL
        SELECT
              '9'               "STT"
            , --NVTOAN modify '12'/05/2017
              N'Chi phí khác'   "TEN_CHI_TIEU"
            , C."HOP_DONG_ID"
            , C."SO_HOP_DONG"
            , C."NGAY_KY"
            , C."TRICH_YEU"
            , C."DOI_TUONG_ID"
            , C."TEN_KHACH_HANG"
             , NULL                                 "SO_CHUNG_TU"
            , NULL :: INT                          "ID_CHUNG_TU"
            , NULL                                 "MODEL_CHUNG_TU"
            , NULL                                 "LOAI_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HACH_TOAN"
            , NULL :: TIMESTAMP                    "NGAY_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HOA_DON"
            , NULL                                 "SO_HOA_DON"
            , N'Chi phí khác'   "DIEN_GIAI"
            , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '04'
            THEN GL."SO_TIEN"
                  ELSE 0
                  END)           "SO_TIEN"
            , CAST(1 AS BOOLEAN) IsBold

        FROM TMP_CHUNG_TU_GHI_SO_DA_TINH_PHAN_BO GL

            INNER JOIN TMP_HOP_DONG_DU_AN_DUOC_CHON C ON GL."HOP_DONG_ID" = C."HOP_DONG_ID"

        GROUP BY C."HOP_DONG_ID",
            C."SO_HOP_DONG",
            C."NGAY_KY",
            C."TRICH_YEU",
            C."DOI_TUONG_ID",

            C."TEN_KHACH_HANG"
        UNION ALL
        SELECT
              '91'                                 "STT"
            , --NVTOAN modify '12'/05/2017
              N'LỢI NHUẬN LŨY KẾ'               "TEN_CHI_TIEU"
            , C."HOP_DONG_ID"
            , C."SO_HOP_DONG"
            , C."NGAY_KY"
            , C."TRICH_YEU"
            , C."DOI_TUONG_ID"
            , C."TEN_KHACH_HANG"
            , NULL                                 "SO_CHUNG_TU"
            , NULL :: INT                          "ID_CHUNG_TU"
            , NULL                                 "MODEL_CHUNG_TU"
            , NULL                                 "LOAI_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HACH_TOAN"
            , NULL :: TIMESTAMP                    "NGAY_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HOA_DON"
            , NULL                                 "SO_HOA_DON"
            , N'LỢI NHUẬN LŨY KẾ'               "DIEN_GIAI"
            , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" IN ('01.01', '01.03') --nvtoan modify '12'/05/2017
            THEN GL."SO_TIEN_LUY_KE"
                  WHEN GL."MA_CHI_TIEU_DINH_DANH" = '01.02'
                      THEN -1 * GL."SO_TIEN_LUY_KE"
                  ELSE CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '03'
                                 OR GL."MA_CHI_TIEU_DINH_DANH" = '04'
                      THEN -GL."SO_TIEN_LUY_KE"
                       ELSE 0
                       END
                  END) + (C."DOANH_THU_LUY_KE" - C."LUY_KE_CHI_PHI"
                          - C."CHI_PHI_KHAC") AS "SO_TIEN"
            , CAST(1 AS BOOLEAN)                 IsBold

        FROM TMP_CHUNG_TU_GHI_SO_DA_TINH_PHAN_BO GL

            INNER JOIN TMP_HOP_DONG_DU_AN_DUOC_CHON C ON GL."HOP_DONG_ID" = C."HOP_DONG_ID"


        GROUP BY C."HOP_DONG_ID",
            C."SO_HOP_DONG",
            C."NGAY_KY",
            C."TRICH_YEU",
            C."DOI_TUONG_ID",

            C."TEN_KHACH_HANG",
            C."DOANH_THU_LUY_KE",
            C."LUY_KE_CHI_PHI",
            C."CHI_PHI_KHAC"
        UNION ALL
        SELECT
              '92'                 "STT"
            , --NVTOAN modify '12'/05/2017
              N'LỢI NHUẬN'      "TEN_CHI_TIEU"
            , C."HOP_DONG_ID"
            , C."SO_HOP_DONG"
            , C."NGAY_KY"
            , C."TRICH_YEU"
            , C."DOI_TUONG_ID"
            , C."TEN_KHACH_HANG"
            , NULL                                 "SO_CHUNG_TU"
            , NULL :: INT                          "ID_CHUNG_TU"
            , NULL                                 "MODEL_CHUNG_TU"
            , NULL                                 "LOAI_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HACH_TOAN"
            , NULL :: TIMESTAMP                    "NGAY_CHUNG_TU"
            , NULL :: TIMESTAMP                    "NGAY_HOA_DON"
            , NULL                                 "SO_HOA_DON"
            , N'LỢI NHUẬN'      "DIEN_GIAI"
            , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" IN ('01.01', '01.03')
            THEN GL."SO_TIEN" --NVTOAN modify '12'/05/2017
                  WHEN GL."MA_CHI_TIEU_DINH_DANH" = '01.02'
                      THEN -1 * GL."SO_TIEN"
                  ELSE CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '03'
                                 OR GL."MA_CHI_TIEU_DINH_DANH" = '04'
                      THEN -GL."SO_TIEN"
                       ELSE 0
                       END
                  END)           "SO_TIEN"
            , CAST(1 AS BOOLEAN) IsBold

        FROM TMP_CHUNG_TU_GHI_SO_DA_TINH_PHAN_BO GL

            INNER JOIN TMP_HOP_DONG_DU_AN_DUOC_CHON C ON GL."HOP_DONG_ID" = C."HOP_DONG_ID"


        GROUP BY C."HOP_DONG_ID",
            C."SO_HOP_DONG",
            C."NGAY_KY",
            C."TRICH_YEU",
            C."DOI_TUONG_ID",

            C."TEN_KHACH_HANG"
        UNION ALL
        SELECT
            "STT"
            , GL."TEN_CHI_TIEU"
            , C."HOP_DONG_ID"
            , C."SO_HOP_DONG"
            , C."NGAY_KY"
            , C."TRICH_YEU"
            , C."DOI_TUONG_ID"
            , C."TEN_KHACH_HANG"
            , GL."SO_CHUNG_TU"
            , GL."ID_CHUNG_TU"
            , GL."MODEL_CHUNG_TU"
            , GL."LOAI_CHUNG_TU"
            , GL."NGAY_HACH_TOAN"
            , GL."NGAY_CHUNG_TU"
            , GL."NGAY_HOA_DON"
            , GL."SO_HOA_DON"
            , GL."DIEN_GIAI"
            , GL."SO_TIEN"
            , CAST(0 AS BOOLEAN) IsBold

        FROM TMP_CHUNG_TU_GHI_SO_DA_TINH_PHAN_BO GL

            INNER JOIN TMP_HOP_DONG_DU_AN_DUOC_CHON C ON GL."HOP_DONG_ID" = C."HOP_DONG_ID"

        WHERE GL."SO_TIEN" <> 0
    ;


    /*Xóa bỏ các dòng phát sinh trong tháng =0*/
    DELETE FROM TMP_KET_QUA
    WHERE "SO_TIEN" = 0
          AND isBold = FALSE
    ;

    --/*xóa bỏ các HĐ không có ps trong tháng*/
    DELETE FROM TMP_KET_QUA
    WHERE "HOP_DONG_ID" IN (
        SELECT "HOP_DONG_ID"
        FROM (SELECT
                  "HOP_DONG_ID"
                  , SUM(CASE WHEN "STT" IN ('1.01')
                THEN "SO_TIEN" --NVTOAN modify '12'/05/2017
                        ELSE 0
                        END) AS "SO_TIEN_1"
                  , SUM(CASE WHEN "STT" = '4'
                THEN "SO_TIEN"
                        ELSE 0
                        END) AS "SO_TIEN_2"
                  , SUM(CASE WHEN "STT" = '93'
                THEN "SO_TIEN"
                        ELSE 0
                        END) AS "SO_TIEN_3"
                  , SUM(CASE WHEN "STT" = '1.02'
                THEN "SO_TIEN"
                        ELSE 0
                        END) AS "SO_TIEN_4"
                  , SUM(CASE WHEN "STT" = '1.03'
                THEN "SO_TIEN"
                        ELSE 0
                        END) AS "SO_TIEN_5"
              FROM TMP_KET_QUA
              WHERE "STT" IN ('1.01', '1.02', '1.03',
                              '4', '93')--NVTOAN modify '12'/05/2017
                    AND isBold = TRUE
              GROUP BY "HOP_DONG_ID"
             ) A
        WHERE "SO_TIEN_1" = 0
              AND "SO_TIEN_2" = 0
              AND "SO_TIEN_3" = 0
              AND "SO_TIEN_4" = 0 AND "SO_TIEN_5" = 0)
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG;
    CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
        AS

    SELECT
        ROW_NUMBER()
        OVER (
            ORDER BY A."SO_HOP_DONG" NULLS FIRST , A."HOP_DONG_ID" NULLS FIRST , A."STT" NULLS FIRST , A."NGAY_HACH_TOAN" NULLS FIRST , A."NGAY_CHUNG_TU" NULLS FIRST , A."SO_CHUNG_TU" NULLS FIRST ,
                A."NGAY_HOA_DON" NULLS FIRST , A."SO_HOA_DON" NULLS FIRST  ) AS "RowNum"
        , A."STT"
        , A."TEN_CHI_TIEU"
        , A."HOP_DONG_ID"
        , A."SO_HOP_DONG"
        , A."NGAY_KY"
        , A."TRICH_YEU"
        , A."DOI_TUONG_ID"

        , AO."MA" AS "MA_KHACH_HANG"

        , A."TEN_KHACH_HANG"
        , A."SO_CHUNG_TU"
        , A."ID_CHUNG_TU"
        , A."MODEL_CHUNG_TU"
        , A."LOAI_CHUNG_TU"
        , A."NGAY_HACH_TOAN"
        , A."NGAY_CHUNG_TU"
        , A."NGAY_HOA_DON"
        , A."SO_HOA_DON"
        , A."DIEN_GIAI"
        , A."SO_TIEN"
        , A.IsBold

    FROM TMP_KET_QUA A

        LEFT JOIN res_partner AO ON AO."id" = A."DOI_TUONG_ID"

    ORDER BY
        A."SO_HOP_DONG",
        A."HOP_DONG_ID",
        A."STT",
        A."NGAY_HACH_TOAN",
        A."NGAY_CHUNG_TU",
        A."SO_CHUNG_TU",
        A."NGAY_HOA_DON",
        A."SO_HOA_DON"

    ;

END $$
;
SELECT 

"SO_HOP_DONG" AS "SO_HOP_DONG",
"NGAY_HACH_TOAN" AS "NGAY_HACH_TOAN",
"NGAY_CHUNG_TU" AS "NGAY_CHUNG_TU",
"SO_CHUNG_TU" AS "SO_CHUNG_TU",
"DIEN_GIAI" AS "DIEN_GIAI",
"SO_TIEN" AS "SO_TIEN",
"isbold" AS "isbold",
"ID_CHUNG_TU" AS "ID_GOC",
"MODEL_CHUNG_TU" AS "MODEL_GOC"

FROM TMP_KET_QUA_CUOI_CUNG
ORDER BY "RowNum"
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
        action = self.env.ref('bao_cao.open_report_chi_tiet_lai_lo_theo_hop_dong').read()[0]
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action