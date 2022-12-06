# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class bao_cao_tong_hop_lai_lo_theo_hop_dong(models.Model):
    _name = 'bao.cao.tong.hop.lai.lo.theo.hop.dong'
    _description = ''
    _inherit = ['mail.thread']
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh', required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI', required='True')
    TU = fields.Date(string='Từ ', help='Từ ', required='True', default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến', required='True', default=fields.Datetime.now)

    RowNum = fields.Integer(string='RowNum', help='RowNum')
    HOP_DONG_ID = fields.Integer(string='HOP_DONG_ID')
    SO_HOP_DONG = fields.Char(string='SO_HOP_DONG', help='ContractCode')
    NGAY_KY = fields.Date(string='NGAY_KY')
    TRICH_YEU = fields.Char(string='TRICH_YEU')
    MA_KHACH_HANG = fields.Char(string='MA_KHACH_HANG', help='AccountObjectCode')
    TEN_KHACH_HANG = fields.Char(string='TEN_KHACH_HANG', help='AccountObjectName')
    DOANH_THU = fields.Float(string='DOANH_THU', help='ReceiptAmount',digits=decimal_precision.get_precision('VND'))
    DOANH_THU_BAN_HANG = fields.Float(string='DOANH_THU_BAN_HANG', help='SaleReceiptAmount',digits=decimal_precision.get_precision('VND'))
    DOANH_THU_KHAC = fields.Float(string='DOANH_THU_KHAC', help='OtherReceiptAmount',digits=decimal_precision.get_precision('VND'))
    GIAM_TRU_DOANH_THU = fields.Float(string='GIAM_TRU_DOANH_THU', help='ReduceReceiptAmount',digits=decimal_precision.get_precision('VND'))
    DOANH_THU_THUAN = fields.Float(string='DOANH_THU_THUAN', help='PureReceiptAmount',digits=decimal_precision.get_precision('VND'))
    GIA_VON_HANG_BAN = fields.Float(string='GIA_VON_HANG_BAN', help='SaleFundAmount',digits=decimal_precision.get_precision('VND'))
    CHI_PHI_BAN_HANG = fields.Float(string='CHI_PHI_BAN_HANG', help='SaleExpenditureAmount',digits=decimal_precision.get_precision('VND'))
    CHI_PHI_QUAN_LY = fields.Float(string='CHI_PHI_QUAN_LY', help='ManagementExpenditureAmount',digits=decimal_precision.get_precision('VND'))
    CHI_PHI_KHAC = fields.Float(string='CHI_PHI_KHAC', help='OtherExpenditureAmount',digits=decimal_precision.get_precision('VND'))
    LAI_LO = fields.Float(string='LAI_LO', help='ProfitAmount',digits=decimal_precision.get_precision('VND'))
    TY_SUAT_LOI_NHUAN_DOANH_THU_PHAN_TRAM = fields.Float(string='TY_SUAT_LOI_NHUAN_DOANH_THU_PHAN_TRAM', help='ProfitRate',digits=decimal_precision.get_precision('VND'))

    CHON_TAT_CA_HOP_DONG = fields.Boolean('Tất cả hợp đồng', default=True)
    HOP_DONG_MANY_IDS = fields.Many2many('sale.ex.hop.dong.ban','tong_hop_lai_lo_theo_hd_hdb', string='Chọn hợp đồng')
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
        result = super(bao_cao_tong_hop_lai_lo_theo_hop_dong, self).default_get(fields_list)
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
        
        query = """
        DO LANGUAGE plpgsql $$
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

    BAO_CAO_ID                          VARCHAR :='CTIncomeSummaryByContract';

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
        WHERE C."id" = any (%(HOP_DONG_IDS)s) --HOP_DONG_IDS
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

    DROP TABLE IF EXISTS TMP_KET_QUA;
    CREATE TEMP TABLE TMP_KET_QUA


            (
              "RowNum" INT ,
              "HOP_DONG_ID" INT ,
              "SO_HOP_DONG" VARCHAR(255) ,
              "NGAY_KY" TIMESTAMP ,
              "TRICH_YEU" VARCHAR ,
              "MA_KHACH_HANG" VARCHAR(255) ,
              "TEN_KHACH_HANG" VARCHAR(255) ,
              "DOANH_THU" DECIMAL(18, 4) ,
              "DOANH_THU_BAN_HANG" DECIMAL(18, 4) , --nvtoan add 15/05/2017: Thực hiện CR 98283
              "DOANH_THU_KHAC" DECIMAL(18, 4) ,
              "GIAM_TRU_DOANH_THU" DECIMAL(18, 4) ,
              "DOANH_THU_THUAN" DECIMAL(18, 4) ,
              "GIA_VON_HANG_BAN" DECIMAL(18, 4) ,
              "CHI_PHI_BAN_HANG" DECIMAL(18, 4) ,
              "CHI_PHI_QUAN_LY" DECIMAL(18, 4) ,
              "CHI_PHI_KHAC" DECIMAL(18, 4) ,
              "LAI_LO" DECIMAL(18, 4) ,
              "TY_SUAT_LOI_NHUAN_DOANH_THU_PHAN_TRAM" DECIMAL(18, 4) 
             

            ) ;
        INSERT  INTO TMP_KET_QUA
                SELECT  ROW_NUMBER() OVER ( ORDER BY C."SO_HOP_DONG" NULLS FIRST , C."NGAY_KY" NULLS FIRST, C."MA_KHACH_HANG" NULLS FIRST) AS "RowNum" ,
                        C."HOP_DONG_ID" ,
                        C."SO_HOP_DONG" ,
                        C."NGAY_KY" ,
                        C."TRICH_YEU" ,
                        C."MA_KHACH_HANG" ,
                        C."TEN_KHACH_HANG" ,
                        SUM(CASE WHEN tbl."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay --nvtoan modify 15/05/2018: Thực hiện CR 98283
                                      THEN tbl."DOANH_THU_BAN_HANG" + tbl."DOANH_THU_KHAC"
                                 ELSE 0
                            END) "TONG_THANH_TOAN" ,
                        SUM(CASE WHEN tbl."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                 THEN tbl."DOANH_THU_BAN_HANG"
                                 ELSE 0
                            END) "DOANH_THU_BAN_HANG" ,
                        SUM(CASE WHEN tbl."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                 THEN tbl."DOANH_THU_KHAC"
                                 ELSE 0
                            END) "DOANH_THU_KHAC" ,
                        SUM(CASE WHEN tbl."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                 THEN tbl."GIAM_TRU_DOANH_THU"
                                 ELSE 0
                            END) "GIAM_TRU_DOANH_THU" ,
                        SUM(CASE WHEN tbl."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                 THEN tbl."DOANH_THU_THUAN"
                                 ELSE 0
                            END) "DOANH_THU_THUAN" ,
                        SUM(CASE WHEN tbl."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                 THEN tbl."GIA_VON_HANG_BAN"
                                 ELSE 0
                            END) "GIA_VON_HANG_BAN" ,
                        SUM(CASE WHEN tbl."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                 THEN tbl."CHI_PHI_BAN_HANG"
                                 ELSE 0
                            END) AS "CHI_PHI_BAN_HANG" ,
                        SUM(CASE WHEN tbl."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                 THEN tbl."CHI_PHI_QUAN_LY"
                                 ELSE 0
                            END) AS "CHI_PHI_QUAN_LY" ,
                        SUM(CASE WHEN tbl."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                 THEN tbl."CHI_PHI_KHAC"
                                 ELSE 0
                            END) AS "CHI_PHI_KHAC" ,
                        SUM(CASE WHEN tbl."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                 THEN tbl."DOANH_THU_THUAN" - tbl."GIA_VON_HANG_BAN"
                                      - tbl."CHI_PHI_BAN_HANG"
                                      - tbl."CHI_PHI_QUAN_LY"
                                      - tbl."CHI_PHI_KHAC"
                                 ELSE 0
                            END) AS "LAI_LO" ,
                        CASE WHEN SUM(CASE WHEN tbl."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                           THEN tbl."DOANH_THU_THUAN" - tbl."GIA_VON_HANG_BAN"
                                                - tbl."CHI_PHI_BAN_HANG"
                                                - tbl."CHI_PHI_QUAN_LY"
                                                - tbl."CHI_PHI_KHAC"
                                           ELSE 0
                                      END) > 0
                             THEN SUM(CASE WHEN tbl."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                           THEN tbl."DOANH_THU_THUAN" - tbl."GIA_VON_HANG_BAN"
                                                - tbl."CHI_PHI_BAN_HANG"
                                                - tbl."CHI_PHI_QUAN_LY"
                                                - tbl."CHI_PHI_KHAC"
                                           ELSE 0
                                      END)
                                  / CASE WHEN SUM(CASE WHEN tbl."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                       THEN tbl."DOANH_THU_THUAN"
                                                       ELSE 0
                                                  END) <> 0
                                         THEN SUM(CASE WHEN tbl."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                       THEN tbl."DOANH_THU_THUAN"
                                                       ELSE 0
                                                  END)
                                         ELSE 1
                                    END * 100
                             ELSE 0
                        END "TY_SUAT_LOI_NHUAN_DOANH_THU_PHAN_TRAM" 
                       
                FROM    ( SELECT    GL."NGAY_HACH_TOAN" ,
                                    GL."HOP_DONG_ID" ,
                                    LC."THUOC_DU_AN_ID" ,
                                    CASE WHEN GL."TEN_COT" = 'SaleReceipt' --nvtoan modify 15/05/2018: Thực hiện CR 98283
                                              THEN GL."SO_TIEN"
                                         ELSE 0
                                    END "DOANH_THU_BAN_HANG" ,
                                    CASE WHEN GL."TEN_COT" = 'OtherReceipt'
                                         THEN GL."SO_TIEN"
                                         ELSE 0
                                    END "DOANH_THU_KHAC" ,
                                    CASE WHEN GL."TEN_COT" = 'ReduceReceipt'
                                         THEN GL."SO_TIEN"
                                         ELSE 0
                                    END "GIAM_TRU_DOANH_THU" ,
                                    CASE GL."TEN_COT"
                                      WHEN 'SaleReceipt' THEN GL."SO_TIEN" --nvtoan modify 15/05/2018: Thực hiện CR 98283
                                      WHEN 'OtherReceipt' THEN GL."SO_TIEN"
                                      WHEN 'ReduceReceipt' THEN -GL."SO_TIEN"
                                      ELSE 0
                                    END "DOANH_THU_THUAN" ,
                                    CASE WHEN GL."TEN_COT" = 'SaleFund'
                                         THEN GL."SO_TIEN"
                                         ELSE 0
                                    END "GIA_VON_HANG_BAN" ,
                                    CASE WHEN GL."TEN_COT" = 'SaleExpenditure'
                                         THEN GL."SO_TIEN"
                                         ELSE 0
                                    END "CHI_PHI_BAN_HANG" ,
                                    CASE WHEN GL."TEN_COT" = 'ManagementExpenditure'
                                         THEN GL."SO_TIEN"
                                         ELSE 0
                                    END "CHI_PHI_QUAN_LY" ,
                                    CASE WHEN GL."TEN_COT" = 'OtherExpenditure'
                                         THEN GL."SO_TIEN"
                                         ELSE 0
                                    END "CHI_PHI_KHAC"
                          FROM      LAY_SO_LIEU_SO_CAI_THEO_CT_THIET_LAP_BCTC_TRA_VE(NULL,
                                                              TU_NGAY_BAT_DAU_TAI_CHINH,
                                                              den_ngay,
                                                              BAO_CAO_ID, NULL,
                                                              chi_nhanh_id,
                                                              bao_gom_du_lieu_chi_nhanh_phu_thuoc) GL
                                    INNER JOIN TMP_DS_HOP_DONG LC ON LC."HOP_DONG_ID" = GL."HOP_DONG_ID"
                          UNION ALL
                          SELECT    JCAE."NGAY_CHUNG_TU" ,
                                    JCAEDT."MA_DON_VI_ID" "HOP_DONG_ID" ,
                                    LC."THUOC_DU_AN_ID" ,
                                    0 "DOANH_THU_BAN_HANG" , --nvtoan modify 15/05/2018: Thực hiện CR 98283
                                    0 "DOANH_THU_KHAC" ,
                                    0 "GIAM_TRU_DOANH_THU" ,
                                    0 "DOANH_THU_THUAN" ,
                                    CASE WHEN  (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '632%%'
                                         THEN JCAEDT."SO_TIEN"
                                         ELSE 0
                                    END "GIA_VON_HANG_BAN" ,
                                    CASE WHEN CHE_DO_KE_TOAN = '15'
                                              AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '641%%'
                                         THEN JCAEDT."SO_TIEN"
                                         WHEN CHE_DO_KE_TOAN = '48'
                                              AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '6421%%'
                                         THEN JCAEDT."SO_TIEN"
                                         ELSE 0
                                    END "CHI_PHI_BAN_HANG" ,
                                    CASE WHEN CHE_DO_KE_TOAN = '15'
                                              AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '642%%'
                                         THEN JCAEDT."SO_TIEN"
                                         WHEN CHE_DO_KE_TOAN = '48'
                                              AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '6422%%'
                                         THEN JCAEDT."SO_TIEN"
                                         ELSE 0
                                    END "CHI_PHI_QUAN_LY" ,
                                    CASE WHEN (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '811%%'
                                              OR (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '635%%'
                                         THEN JCAEDT."SO_TIEN"
                                         ELSE 0
                                    END
                          FROM      tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JCAE
                                    INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCAEDT ON JCAEDT."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JCAE."id"
                                    INNER JOIN TMP_DS_HOP_DONG LC ON LC."HOP_DONG_ID" = JCAEDT."MA_DON_VI_ID"
                                    INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCAE."CHI_NHANH_ID"
                          WHERE     JCAEDT."CAP_TO_CHUC" = '3'
                                    AND JCAE."NGAY_CHUNG_TU" BETWEEN TU_NGAY_BAT_DAU_TAI_CHINH AND den_ngay

                        ) tbl
                        INNER JOIN LATERAL ( SELECT
                                                tSC."HOP_DONG_ID" ,
                                                tSC."SO_HOP_DONG" ,
                                                tSC."NGAY_KY" ,
                                                tSC."TRICH_YEU" ,
                                                tSC."DOI_TUONG_ID" ,
                                                AO."MA" AS "MA_KHACH_HANG" ,
                                                
                                                tSC."TEN_KHACH_HANG" ,

                                                tSC."DOANH_THU_LUY_KE" ,
                                                tSC."LUY_KE_CHI_PHI" ,
                                                tSC."CHI_PHI_KHAC"

                                      FROM      TMP_HOP_DONG_DU_AN_DUOC_CHON tSC
                                                LEFT JOIN res_partner AO ON AO."id" = tSC."DOI_TUONG_ID"
                                      WHERE     tSC."HOP_DONG_ID" = tbl."HOP_DONG_ID"
                                                OR tSC."HOP_DONG_ID" = tbl."THUOC_DU_AN_ID"
                                      ORDER BY  tSC."THUOC_DU_AN_ID" DESC
                                    FETCH FIRST 1 ROW ONLY
                                    ) C  ON TRUE
                GROUP BY 
                        C."HOP_DONG_ID" ,
                        C."SO_HOP_DONG" ,
                        C."NGAY_KY" ,
                        C."TRICH_YEU" ,
                        C."MA_KHACH_HANG" ,
                        C."TEN_KHACH_HANG" ,
                      
                        C."DOANH_THU_LUY_KE" ,
                        C."LUY_KE_CHI_PHI" ,
                        C."CHI_PHI_KHAC" ;


    DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG;
    CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
        AS
    
        SELECT  *
        FROM    TMP_KET_QUA
        WHERE   "DOANH_THU_BAN_HANG" <> 0 --nvtoan modify 15/05/2017:Thực hiện CR 98283
                OR "DOANH_THU_KHAC" <> 0
                OR "GIAM_TRU_DOANH_THU" <> 0
                OR "DOANH_THU_THUAN" <> 0
                OR "GIA_VON_HANG_BAN" <> 0
                OR "CHI_PHI_BAN_HANG" <> 0
                OR "CHI_PHI_QUAN_LY" <> 0
                OR "CHI_PHI_KHAC" <> 0
                OR "LAI_LO" <> 0
        ORDER BY  "RowNum"

    ;

END $$
;
SELECT 

"SO_HOP_DONG" AS "SO_HOP_DONG",
"TEN_KHACH_HANG" AS "TEN_KHACH_HANG",
"DOANH_THU" AS "DOANH_THU",
"GIAM_TRU_DOANH_THU" AS "GIAM_TRU_DOANH_THU",
"DOANH_THU_THUAN" AS "DOANH_THU_THUAN",
"GIA_VON_HANG_BAN" AS "GIA_VON_HANG_BAN",
"CHI_PHI_BAN_HANG" AS "CHI_PHI_BAN_HANG",
"CHI_PHI_QUAN_LY" AS "CHI_PHI_QUAN_LY",
"CHI_PHI_KHAC" AS "CHI_PHI_KHAC",
"LAI_LO" AS "LAI_LO",
"TY_SUAT_LOI_NHUAN_DOANH_THU_PHAN_TRAM" AS "TY_SUAT_LOI_NHUAN_DOANH_THU_PHAN_TRAM"

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
        action = self.env.ref('bao_cao.open_report_tong_hop_lai_lo_theo_hop_dong').read()[0]
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action