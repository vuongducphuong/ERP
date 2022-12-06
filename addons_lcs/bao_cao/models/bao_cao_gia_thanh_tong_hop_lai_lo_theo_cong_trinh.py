# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class bao_cao_gia_thanh_tong_hop_lai_lo_theo_cong_trinh(models.Model):
    _name = 'bao.cao.gia.thanh.tong.hop.lai.lo.theo.cong.trinh'
    _description = ''
    _inherit = ['mail.thread']
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh', required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI', required='True')
    TU = fields.Date(string='Từ ', help='Từ ', required='True', default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến', required='True', default=fields.Datetime.now)

    RowNum = fields.Integer(string='RowNum', help='RowNum')
    MA_CONG_TRINH = fields.Char(string='MA_CONG_TRINH', help='ProjectWorkCode')
    TEN_CONG_TRINH = fields.Char(string='TEN_CONG_TRINH', help='ProjectWorkName')
    LOAI_CONG_TRINH = fields.Char(string='LOAI_CONG_TRINH', help='ProjectWorkCategoryName')
    CONG_TRINH_ID = fields.Integer(string='CONG_TRINH_ID')
    isbold = fields.Boolean(string='isbold', help='IsBold')
    DOANH_THU = fields.Float(string='DOANH_THU', help='SalesReceiptAmount',digits=decimal_precision.get_precision('VND'))
    DOANH_THU_THU_NHAP_KHAC = fields.Float(string='DOANH_THU_THU_NHAP_KHAC', help='OtherReceiptAmount',digits=decimal_precision.get_precision('VND'))
    TONG_THANH_TOAN = fields.Float(string='TONG_THANH_TOAN', help='ReceiptAmount',digits=decimal_precision.get_precision('VND'))
    GIAM_TRU_DOANH_THU = fields.Float(string='GIAM_TRU_DOANH_THU', help='ReduceReceiptAmount',digits=decimal_precision.get_precision('VND'))
    DOANH_THU_THUAN = fields.Float(string='DOANH_THU_THUAN', help='NetReceiptAmount',digits=decimal_precision.get_precision('VND'))
    GIA_VON_HANG_BAN = fields.Float(string='GIA_VON_HANG_BAN', help='SaleCostAmount',digits=decimal_precision.get_precision('VND'))
    CHI_PHI_BAN_HANG = fields.Float(string='CHI_PHI_BAN_HANG', help='SaleExpenditureAmount',digits=decimal_precision.get_precision('VND'))
    CHI_PHI_QUAN_LY = fields.Float(string='CHI_PHI_QUAN_LY', help='ManagementExpenditureAmount',digits=decimal_precision.get_precision('VND'))
    CHI_PHI_KHAC = fields.Float(string='CHI_PHI_KHAC', help='OtherExpenditureAmount',digits=decimal_precision.get_precision('VND'))
    DO_DANG_DAU_KY = fields.Float(string='DO_DANG_DAU_KY', help='OpenUncompletedAmount',digits=decimal_precision.get_precision('VND'))
    NGUYEN_VAT_LIEU = fields.Float(string='NGUYEN_VAT_LIEU', help='MatetialAmount',digits=decimal_precision.get_precision('VND'))
    NHAN_CONG = fields.Float(string='NHAN_CONG', help='LaborAmount',digits=decimal_precision.get_precision('VND'))
    MAY_THI_CONG = fields.Float(string='MAY_THI_CONG', help='MachineAmount',digits=decimal_precision.get_precision('VND'))
    CHI_PHI_CHUNG = fields.Float(string='CHI_PHI_CHUNG', help='GeneralAmount',digits=decimal_precision.get_precision('VND'))
    CONG = fields.Float(string='CONG', help='TotalCostAmount',digits=decimal_precision.get_precision('VND'))
    KHOAN_GIAM_GIA_THANH = fields.Float(string='KHOAN_GIAM_GIA_THANH', help='DiscountAmount',digits=decimal_precision.get_precision('VND'))
    DO_DANG_CUOI_KY = fields.Float(string='DO_DANG_CUOI_KY', help='CloseUncompletedAmount',digits=decimal_precision.get_precision('VND'))
    LAI_LO = fields.Float(string='LAI_LO', help='ProfitAmount',digits=decimal_precision.get_precision('VND'))
    TY_SUAT_LOI_NHUAN_DOANH_THU_PHAN_TRAM = fields.Float(string='TY_SUAT_LOI_NHUAN_DOANH_THU_PHAN_TRAM', help='ProfitRate',digits=decimal_precision.get_precision('VND'))


    CONG_TRINH_IDS = fields.One2many ('danh.muc.cong.trinh')
    CHON_TAT_CA_CONG_TRINH = fields.Boolean('Tất cả công trình', default=True)
    CONG_TRINH_MANY_IDS = fields.Many2many('danh.muc.cong.trinh','tong_hop_nxk_cong_trinh', string='Chọn công trình') 

    # Công trình
    @api.onchange('CONG_TRINH_IDS')
    def update_CONG_TRINH_IDS(self):
        self.CONG_TRINH_MANY_IDS =self.CONG_TRINH_IDS.ids
        
    @api.onchange('CONG_TRINH_MANY_IDS')
    def _onchange_CONG_TRINH_MANY_IDS(self):
        self.CONG_TRINH_IDS = self.CONG_TRINH_MANY_IDS.ids
    # end  

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')
    
    @api.model
    def default_get(self, fields_list):
        result = super(bao_cao_gia_thanh_tong_hop_lai_lo_theo_cong_trinh, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        return result
    
    def _validate(self):
        params = self._context
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        TU_NGAY = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

        CHON_TAT_CA_CONG_TRINH = params['CHON_TAT_CA_CONG_TRINH'] if 'CHON_TAT_CA_CONG_TRINH' in params.keys() else 'False'
        CONG_TRINH_MANY_IDS = params['CONG_TRINH_MANY_IDS'] if 'CONG_TRINH_MANY_IDS' in params.keys() else 'False'
        
        if(TU_NGAY=='False'):
            raise ValidationError('<Từ ngày> không được bỏ trống.')
        elif(DEN_NGAY=='False'):
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        elif(TU_NGAY_F > DEN_NGAY_F):
            raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')

        if CHON_TAT_CA_CONG_TRINH == 'False':
            if CONG_TRINH_MANY_IDS == []:
                raise ValidationError('Bạn chưa chọn <Công trình>. Xin vui lòng chọn lại.')

    
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        TU_NGAY = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
       
        if params.get('CHON_TAT_CA_CONG_TRINH'):
            domain = []
            CONG_TRINH_IDS = self.env['danh.muc.cong.trinh'].search(domain).ids
        else:
            CONG_TRINH_IDS = params.get('CONG_TRINH_MANY_IDS')

        params_sql = {
            'TU_NGAY':TU_NGAY_F, 
            'DEN_NGAY':DEN_NGAY_F, 
            'CONG_TRINH_IDS':CONG_TRINH_IDS, 
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'CHI_NHANH_ID':CHI_NHANH_ID,
            'limit': limit,
            'offset': offset, 
            }      
        
        # Execute SQL query here
       
        query = """
        DO LANGUAGE plpgsql $$
DECLARE
    tu_ngay           TIMESTAMP := %(TU_NGAY)s;

    den_ngay          TIMESTAMP := %(DEN_NGAY)s;

    chi_nhanh_id      INTEGER := %(CHI_NHANH_ID)s;
    bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    CHE_DO_KE_TOAN    VARCHAR;

    MA_PHAN_CAP_NVLTT VARCHAR(100);

    MA_PHAN_CAP_NCTT  VARCHAR(100);

    MA_PHAN_CAP_SXC   VARCHAR(100);

    MA_PHAN_CAP_CPSX  VARCHAR(100);

    MA_PHAN_CAP_MTC   VARCHAR(100);



    rec               RECORD;

    --@ListObjectID : tham số bên misa

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



    -- KMCP: Sản xuất
    SELECT concat("MA_PHAN_CAP",'%%')
    INTO MA_PHAN_CAP_CPSX
    FROM danh_muc_khoan_muc_cp
    WHERE "MA_KHOAN_MUC_CP" = 'CPSX'
    ;

    SELECT concat("MA_PHAN_CAP",'%%')
    INTO MA_PHAN_CAP_NVLTT
    FROM danh_muc_khoan_muc_cp
    WHERE "MA_KHOAN_MUC_CP" = 'NVLTT'
    ;

    SELECT concat("MA_PHAN_CAP",'%%')
    INTO MA_PHAN_CAP_NCTT
    FROM danh_muc_khoan_muc_cp
    WHERE "MA_KHOAN_MUC_CP" = 'NCTT'
    ;

    SELECT concat("MA_PHAN_CAP",'%%')
    INTO MA_PHAN_CAP_MTC
    FROM danh_muc_khoan_muc_cp
    WHERE "MA_KHOAN_MUC_CP" = 'MTC'
    ;

    SELECT concat("MA_PHAN_CAP",'%%')
    INTO MA_PHAN_CAP_SXC
    FROM danh_muc_khoan_muc_cp
    WHERE "MA_KHOAN_MUC_CP" = 'SXC'
    ;


    DROP TABLE  IF EXISTS  TMP_CONG_TRINH_DUOC_CHON;
    CREATE TEMP TABLE TMP_CONG_TRINH_DUOC_CHON


    
            (
              "CONG_TRINH_ID" INT ,
              "MA_PHAN_CAP" VARCHAR(100) ,
              "MA_CONG_TRINH" VARCHAR(20) ,
              "TEN_CONG_TRINH" VARCHAR(128) ,

              "LOAI_CONG_TRINH" VARCHAR(255)
            ) ;
			-- 1 bảng để lưu những CT đc chọn @Object
			-- 1 bảng để lưu những CT dùng để lấy dữ liệu (k lấy thằng cha)
			-- 1 bảng để
        INSERT INTO  TMP_CONG_TRINH_DUOC_CHON
                SELECT DISTINCT
                        EI."id" ,
                        EI."MA_PHAN_CAP" ,
                        EI."MA_CONG_TRINH" ,
                        EI."TEN_CONG_TRINH" ,

                        PC."name"
                FROM
                        danh_muc_cong_trinh AS EI
                        LEFT JOIN danh_muc_loai_cong_trinh PC ON EI."LOAI_CONG_TRINH" = PC."id"
                        WHERE EI."id" = any(%(CONG_TRINH_IDS)s); --@ListObjectID


     DROP TABLE  IF EXISTS  TMP_CONG_TRINH_DUOC_CHON_1;
    CREATE TEMP TABLE TMP_CONG_TRINH_DUOC_CHON_1
      
            (
              "CONG_TRINH_ID" INT PRIMARY KEY ,
              "MA_PHAN_CAP" VARCHAR(100) 
                                       NULL
            );
        INSERT INTO  TMP_CONG_TRINH_DUOC_CHON_1
                SELECT  S."CONG_TRINH_ID" ,
                        S."MA_PHAN_CAP"
                FROM    TMP_CONG_TRINH_DUOC_CHON S
                        LEFT  JOIN TMP_CONG_TRINH_DUOC_CHON S1 ON S1."MA_PHAN_CAP" LIKE S."MA_PHAN_CAP"
                                                              || '%%'
                                                              AND S."MA_PHAN_CAP" <> S1."MA_PHAN_CAP"
                WHERE   S1."MA_PHAN_CAP" IS NULL ;



    DROP TABLE IF EXISTS TMP_DS_CONG_TRINH;
    CREATE TEMP TABLE TMP_DS_CONG_TRINH

       -- Bảng khoản mục CP gồm toàn bộ khoản mục CP con
            (
              "CONG_TRINH_ID" INT ,
              "MA_PHAN_CAP" VARCHAR(100)
            ) ;


  DROP TABLE IF EXISTS TMP_BAC;
    CREATE TEMP TABLE TMP_BAC

       -- Tính bậc để lùi dòng cho báo cáo hình cây
            (
              "CONG_TRINH_ID" INT PRIMARY KEY ,
              "BAC" INT
            ) ;
        INSERT  INTO TMP_BAC
                SELECT  P."CONG_TRINH_ID" ,
                        COUNT(PD."MA_PHAN_CAP") Grade
                FROM    TMP_CONG_TRINH_DUOC_CHON P
                        LEFT JOIN TMP_CONG_TRINH_DUOC_CHON PD ON P."MA_PHAN_CAP" LIKE PD."MA_PHAN_CAP"
                                                              || '%%'
                                                              AND P."MA_PHAN_CAP" <> PD."MA_PHAN_CAP"
                GROUP BY P."CONG_TRINH_ID" ;

        -- Bảng các khoản mục CP cha được chọn trong đó có chọn cả con mà là cha

     DROP TABLE IF EXISTS TMP_CHA;
    CREATE TEMP TABLE TMP_CHA


            (
              "CONG_TRINH_ID" INT PRIMARY KEY
            ) ;
        INSERT  INTO TMP_CHA
                SELECT DISTINCT
                        PD."CONG_TRINH_ID"
                FROM    TMP_CONG_TRINH_DUOC_CHON P
                        LEFT JOIN TMP_CONG_TRINH_DUOC_CHON PD ON P."MA_PHAN_CAP" LIKE PD."MA_PHAN_CAP"
                                                              || '%%'
                                                              AND P."MA_PHAN_CAP" <> PD."MA_PHAN_CAP"
                WHERE   PD."MA_PHAN_CAP" IS NOT NULL ;


        INSERT  INTO TMP_DS_CONG_TRINH
                SELECT  DISTINCT
                        EI."id" ,
                        EI."MA_PHAN_CAP"
                FROM    danh_muc_cong_trinh EI
                        INNER JOIN TMP_CONG_TRINH_DUOC_CHON_1 SEI ON EI."MA_PHAN_CAP" LIKE SEI."MA_PHAN_CAP"
                                                              || '%%' ;

    DROP TABLE IF EXISTS TMP_DU_LIEU_SO_CAI;
    CREATE TEMP TABLE TMP_DU_LIEU_SO_CAI


            (
              "CONG_TRINH_ID" INT ,
              "MA_PHAN_CAP" VARCHAR(100) ,
              "DOANH_THU_DOANH_THU_BAN_HANG" DECIMAL(25, 4) ,
              "DOANH_THU_THU_NHAP_KHAC" DECIMAL(25, 4) ,
              "TONG_THANH_TOAN" DECIMAL(25, 4) ,
              "GIAM_TRU_DOANH_THU" DECIMAL(25, 4) ,
              "GIA_VON" DECIMAL(25, 4) ,  -- Giá vốn hàng bán
              "CHI_PHI_BAN_HANG" DECIMAL(25, 4) , -- Chi phí bán hàng
              "CHI_PHI_QUAN_LY" DECIMAL(25, 4) ,-- Chi phí quản lý
              "CHI_PHI_KHAC" DECIMAL(25, 4) , -- Chi phí khác
              "DO_DANG_DAU_KY" DECIMAL(25, 4) ,
              "NGUYEN_VAT_LIEU" DECIMAL(25, 4) ,
              "NHAN_CONG" DECIMAL(25, 4) ,
              "MAY_THI_CONG" DECIMAL(25, 4) ,
              "CHI_PHI_CHUNG" DECIMAL(25, 4) ,
              "KHOAN_GIAM_GIA_THANH" DECIMAL(25, 4) ,
              "DO_DANG_CUOI_KY" DECIMAL(25, 4)
            ) ;

        IF ( CHE_DO_KE_TOAN = '15' )
            THEN
                INSERT INTO  TMP_DU_LIEU_SO_CAI
                        SELECT  P."CONG_TRINH_ID" ,
                                P."MA_PHAN_CAP" ,
                                SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                              AND ( GL."MA_TAI_KHOAN" LIKE N'511%%'
                                                     --ntquang 14/10/1017 :  CR_149456_Tài khoản đối ứng của số dư đầu kỳ = NULL
                                                    AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG",'') NOT LIKE N'911%%'
                                                  ) THEN GL."GHI_CO"
                                         ELSE 0
                                    END)
                                - SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                AND GL."MA_TAI_KHOAN" LIKE '511%%'
                                                 --ntquang 14/10/1017 :  CR_149456_Tài khoản đối ứng của số dư đầu kỳ = NULL
                                                AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG",'') NOT LIKE N'911%%'
                                                AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG",'') NOT LIKE N'521%%'
                                           THEN GL."GHI_NO"
                                           ELSE 0
                                      END) AS "DOANH_THU_DOANH_THU_BAN_HANG" --Doanh thu bán hàng: (PS C 511 (Không bao gồm PS ĐƯ Nợ TK 911/Có TK511)– PS N 511 (không bao gồm PS ĐƯ Nợ TK511/Có TK 911, 521)) chi tiết theo từng công trình
                                ,
                                SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                              AND ( ( GL."MA_TAI_KHOAN" LIKE N'711%%'
                                                      OR GL."MA_TAI_KHOAN" LIKE '515%%'
                                                    )
                                                    --ntquang 14/10/1017 :  CR_149456_Tài khoản đối ứng của số dư đầu kỳ = NULL
                                                    AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG",'') NOT LIKE N'911%%'
                                                  ) THEN GL."GHI_CO"
                                         ELSE 0
                                    END)
                                - SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                AND ( GL."MA_TAI_KHOAN" LIKE N'711%%'
                                                      OR GL."MA_TAI_KHOAN" LIKE '515%%'
                                                    )
                                                    --ntquang 14/10/1017 :  CR_149456_Tài khoản đối ứng của số dư đầu kỳ = NULL
                                                AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG",'') NOT LIKE N'911%%'
                                           THEN GL."GHI_NO"
                                           ELSE 0
                                      END) AS "DOANH_THU_THU_NHAP_KHAC" --Doan thu khác: (PS C 515, 711 (Không bao gồm PS ĐƯ Nợ TK 911/Có TK515, 711) – PS N 515, 711 (không bao gồm PS ĐƯ Nợ TK515, 711/Có TK 911)) chi tiết theo từng công trình
                                ,
                                0 AS "TONG_THANH_TOAN" --Doan thu: Doanh thu bán hàng + Doanh thu khác
                                ,
                                SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                              AND GL."MA_TAI_KHOAN" LIKE N'521%%'
                                         THEN GL."GHI_NO"
                                         ELSE 0
                                    END)
                                - SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                AND GL."MA_TAI_KHOAN" LIKE N'5211%%'
                                           THEN GL."GHI_CO"
                                           ELSE 0
                                      END) AS "GIAM_TRU_DOANH_THU" --Giảm trừ doanh thu: Đối với TT200 = PS Nợ TK 521 - PS Có TK 5211 chi tiết theo từng công trình
                                ,
                                SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                              AND GL."MA_TAI_KHOAN" LIKE N'632%%'
                                         THEN GL."GHI_NO" - GL."GHI_CO"
                                         ELSE 0
                                    END) AS "GIA_VON" -- Giá vốn hàng bán: Đối với TT200 = (PSN632 – PSC632) chi tiết theo từng công trình
                                ,
                                SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                              AND GL."MA_TAI_KHOAN" LIKE N'641%%'
                                         THEN GL."GHI_NO" - GL."GHI_CO"
                                         ELSE 0
                                    END) AS "CHI_PHI_BAN_HANG" -- Chi phí bán hàng Đối với TT200 = (PSN 641 – PSC641) chi tiết theo từng công trình
                                ,
                                SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                              AND GL."MA_TAI_KHOAN" LIKE N'642%%'
                                         THEN GL."GHI_NO" - GL."GHI_CO"
                                         ELSE 0
                                    END) AS "CHI_PHI_QUAN_LY" -- Chi phí quản lý: Đối với TT200 = (PSN 642 – PSC642) chi tiết theo từng công trình
                                ,
                                SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                              AND ( GL."MA_TAI_KHOAN" LIKE N'811%%'
                                                    OR GL."MA_TAI_KHOAN" LIKE N'635%%'
                                                  )
                                         THEN GL."GHI_NO" - GL."GHI_CO"
                                         ELSE 0
                                    END) AS "CHI_PHI_KHAC" -- Chi phí khác Đối với TT200 =  (PSN 811, 635 – PSC 811, 635) chi tiết theo từng công trình
                                ,
                                SUM(CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                                              AND LEFT(GL."MA_TAI_KHOAN", 3) IN (
                                              '621', '622', '623', '627',
                                              '154' )
                                         THEN GL."GHI_NO" - GL."GHI_CO"
                                         ELSE 0
                                    END) AS "DO_DANG_DAU_KY" -- Tổng chi phí trên form form Nhập lũy kế chi phí phát sinh cho công trình kỳ trước + Tổng (PS Nợ - PS Có) của TK 621, 622, 623, 627 chi tiết theo từng công trình trên chứng từ có ngày hạch toán < “Từ ngày của kỳ báo cáo (không kể PSDU Nợ TK 154/Có TK 621, 622, 623, 627 chi tiết theo từng công trình) + Tổng PS Nợ TK 154 chi tiết theo từng ĐT THCP trên chứng từ có ngày hạch toán < “Từ ngày của kỳ báo cáo (không kể PSDU Nợ TK 154/Có TK 621, 622, 627, 623 chi tiết theo từng ĐT THCP)
                                ,
                                SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                         THEN CASE WHEN ( GL."MA_TAI_KHOAN" LIKE N'621%%'
                                                          AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'154%%'
                                                        )
                                                   THEN GL."GHI_NO"
                                                        - GL."GHI_CO"
                                                   WHEN GL."MA_TAI_KHOAN" LIKE N'154%%'
                                                        AND LEFT(GL."MA_TAI_KHOAN_DOI_UNG",
                                                              3) NOT IN (
                                                        '621', '622', '623',
                                                        '627' ) --nvtoan remove 22/03/2015: Sửa lỗi 95899, '154'
                                                        THEN GL."GHI_NO"
                                                   ELSE 0
                                              END
                                         ELSE 0
                                    END) AS "NGUYEN_VAT_LIEU" -- nguyên vật liệu trực tiếp: Đối với TT200: Tổng (PS Nợ - PS Có) của TK 621 chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo (không kể PSDU Nợ TK 154/Có TK 621 chi tiết theo từng công trình)
												--+ Tổng PS Nợ TK 154 chi tiết theo từng ĐT THCP trên chứng từ có ngày hạch toán thuộc kỳ tính giá thành (không kể PSDU Nợ TK 154/Có TK 621, 622, 627, 623 chi tiết theo từng ĐT THCP)
                                ,
                                SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                              AND ( GL."MA_TAI_KHOAN" LIKE N'622%%'
                                                    AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'154%%'
                                                  )
                                         THEN GL."GHI_NO" - GL."GHI_CO"
                                         ELSE 0
                                    END) AS "NHAN_CONG" -- Chi phí nhân công trực tiếp: Đối với TT200: Tổng (PS Nợ - PS Có) của TK 622 chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo (không kể PSDU Nợ TK 154/Có TK 622 chi tiết theo từng công trình)
                                ,
                                SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                              AND ( GL."MA_TAI_KHOAN" LIKE N'623%%'
                                                    AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'154%%'
                                                  )
                                         THEN GL."GHI_NO" - GL."GHI_CO"
                                         ELSE 0
                                    END) AS "MAY_THI_CONG" --Chi phí máy thi công Đối với TT200: Tổng (PS Nợ - PS Có) của TK 623 chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo (không kể PSDU Nợ TK 154/Có TK 623 chi tiết theo từng công trình)
                                ,
                                SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                              AND ( GL."MA_TAI_KHOAN" LIKE N'627%%'
                                                    AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'154%%'
                                                  )
                                         THEN GL."GHI_NO" - GL."GHI_CO"
                                         ELSE 0
                                    END) AS "CHI_PHI_CHUNG" --Chi phí chung: Đối với TT200: Tổng (PS Nợ - PS Có) của TK 627 chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo (không kể PSDU Nợ TK 154/Có TK 627 chi tiết theo từng công trình)
                                ,
                                SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                              AND ( GL."MA_TAI_KHOAN" LIKE N'154%%'
                                                    AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'632%%'
                                                  ) THEN GL."GHI_CO"
                                         ELSE 0
                                    END) AS "KHOAN_GIAM_GIA_THANH" --Giảm giá thành: TT200: PS Có TK 154 chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo (không kể PSDU Nợ TK 632/có TK 154 chi tiết theo từng công trình
                                ,
                                SUM(CASE WHEN GL."NGAY_HACH_TOAN" <= den_ngay
                                              AND LEFT(GL."MA_TAI_KHOAN", 3) IN (
                                              '621', '622', '623', '627',
                                              '154' )
                                         THEN GL."GHI_NO" - GL."GHI_CO"
                                         ELSE 0
                                    END) AS "DO_DANG_DAU_KY" -- Dở dang cuối kỳ
                        FROM    so_cai_chi_tiet GL
                                INNER JOIN TMP_DS_CONG_TRINH P ON GL."CONG_TRINH_ID" = P."CONG_TRINH_ID"
                                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                        WHERE   GL."NGAY_HACH_TOAN" <= den_ngay
                                AND ( "MA_TAI_KHOAN" LIKE N'511%%'
                                      OR "MA_TAI_KHOAN" LIKE N'711%%'
                                      OR "MA_TAI_KHOAN" LIKE N'515%%'
                                      OR "MA_TAI_KHOAN" LIKE N'521%%'
                                      OR "MA_TAI_KHOAN" LIKE N'632%%'
                                      OR "MA_TAI_KHOAN" LIKE N'62%%'
                                      OR "MA_TAI_KHOAN" LIKE N'154%%'
                                      OR "MA_TAI_KHOAN" LIKE N'641%%'
                                      OR "MA_TAI_KHOAN" LIKE N'642%%'
                                      OR "MA_TAI_KHOAN" LIKE N'811%%'
                                      OR "MA_TAI_KHOAN" LIKE N'635%%'
                                    )

		                        AND (GL."LOAI_CHUNG_TU" <> '610' OR (GL."LOAI_CHUNG_TU" = '610' AND GL."MA_TAI_KHOAN" NOT LIKE '154%%'))
                        GROUP BY P."CONG_TRINH_ID" ,
                                P."MA_PHAN_CAP"
                        UNION ALL
                        SELECT  P."CONG_TRINH_ID" ,
                                P."MA_PHAN_CAP" ,
                                0 AS "DOANH_THU_DOANH_THU_BAN_HANG" ,
                                0 AS "DOANH_THU_THU_NHAP_KHAC" ,
                                0 AS "TONG_THANH_TOAN" ,
                                0 AS "GIAM_TRU_DOANH_THU" ,
                                0 AS "GIA_VON" ,  -- Giá vốn hàng bán: + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 632 trên chứng từ phân bổ chi phí BH, QLDN, khác
                                0 AS "CHI_PHI_BAN_HANG" , -- Chi phí bán hàng + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 641 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                                0 AS "CHI_PHI_QUAN_LY" ,-- Chi phí quản lý + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 642 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                                0 AS "CHI_PHI_KHAC" , -- Chi phí khác + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 811, 635 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                                SUM(CASE WHEN J."DEN_NGAY" < tu_ngay
                                              AND LEFT((SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAD."TAI_KHOAN_ID"), 3) IN (
                                              '621', '622', '623', '627' )
                                         THEN JCAD."SO_TIEN"
                                         ELSE 0
                                    END) AS "DO_DANG_DAU_KY" ,	--  + Tổng số tiền phân bổ của TK 621, 622, 623, 627 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc < “Từ ngày của kỳ báo cáo - PS Có TK 154 chi tiết theo từng công trình trên các chứng từ có ngày hạch toán < "Từ ngày" của kỳ báo cáo + Số đã nghiệm thu trên form Nhập lũy kế chi phí phát sinh cho công trình/đơn hàng/hợp đồng kỳ trước tương ứng với TK 154
                                SUM(CASE WHEN J."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
                                              AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAD."TAI_KHOAN_ID") LIKE N'621%%'
                                         THEN JCAD."SO_TIEN"
                                         ELSE 0
                                    END) AS "NGUYEN_VAT_LIEU" , -- + Tổng số tiền phân bổ của TK 621 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                                SUM(CASE WHEN J."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
                                              AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAD."TAI_KHOAN_ID") LIKE N'622%%'
                                         THEN JCAD."SO_TIEN"
                                         ELSE 0
                                    END) AS "NHAN_CONG" ,-- + Tổng số tiền phân bổ của TK 622 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo
                                SUM(CASE WHEN J."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
                                              AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAD."TAI_KHOAN_ID") LIKE N'623%%'
                                         THEN JCAD."SO_TIEN"
                                         ELSE 0
                                    END) AS "MAY_THI_CONG" ,--+ Tổng số tiền phân bổ của TK 623 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                                SUM(CASE WHEN J."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
                                              AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAD."TAI_KHOAN_ID") LIKE N'627%%'
                                         THEN JCAD."SO_TIEN"
                                         ELSE 0
                                    END) AS "CHI_PHI_CHUNG" ,--+ Tổng số tiền phân bổ của TK 627 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                                0 AS "KHOAN_GIAM_GIA_THANH" ,
                                SUM(CASE WHEN J."DEN_NGAY" <= den_ngay
                                              AND LEFT( (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAD."TAI_KHOAN_ID"), 3) IN (
                                              '621', '622', '623', '627' )
                                         THEN JCAD."SO_TIEN"
                                         ELSE 0
                                    END) AS "DO_DANG_CUOI_KY"
                        FROM    gia_thanh_ket_qua_phan_bo_chi_phi_chung JCAD
                                INNER JOIN gia_thanh_ky_tinh_gia_thanh J ON J."id" = JCAD."KY_TINH_GIA_THANH_ID"
                                INNER JOIN TMP_DS_CONG_TRINH P ON P."CONG_TRINH_ID" = JCAD."MA_CONG_TRINH_ID"
                                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = J."CHI_NHANH_ID"
                        WHERE   J."DEN_NGAY" <= den_ngay --Lấy tất cả các lần phân bổ của kỳ tính giá thành hiện tại và trước đó

                        GROUP BY P."CONG_TRINH_ID" ,
                                P."MA_PHAN_CAP"
                        UNION ALL
                        SELECT  P."CONG_TRINH_ID" ,
                                P."MA_PHAN_CAP" ,
                                0 AS "DOANH_THU_DOANH_THU_BAN_HANG" ,
                                0 AS "DOANH_THU_THU_NHAP_KHAC" ,
                                0 AS "TONG_THANH_TOAN" ,
                                0 AS "GIAM_TRU_DOANH_THU" ,
                                SUM(CASE WHEN  (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'632%%'
                                         THEN JCED."SO_TIEN"
                                         ELSE 0
                                    END) AS "GIA_VON" ,  -- Giá vốn hàng bán: + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 632 trên chứng từ phân bổ chi phí BH, QLDN, khác
                                SUM(CASE WHEN (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'641%%'
                                         THEN JCED."SO_TIEN"
                                         ELSE 0
                                    END) AS "CHI_PHI_BAN_HANG" , -- Chi phí bán hàng + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 641 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                                SUM(CASE WHEN (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'642%%'
                                         THEN JCED."SO_TIEN"
                                         ELSE 0
                                    END) AS "CHI_PHI_QUAN_LY" ,-- Chi phí quản lý + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 642 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                                SUM(CASE WHEN ( (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'811%%'
                                                OR (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'635%%'
                                              ) THEN JCED."SO_TIEN"
                                         ELSE 0
                                    END) AS "CHI_PHI_KHAC" , -- Chi phí khác + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 811, 635 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                                0 AS "DO_DANG_DAU_KY" ,	--  + Tổng số tiền phân bổ của TK 621, 622, 623, 627 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc < “Từ ngày của kỳ báo cáo - PS Có TK 154 chi tiết theo từng công trình trên các chứng từ có ngày hạch toán < "Từ ngày" của kỳ báo cáo + Số đã nghiệm thu trên form Nhập lũy kế chi phí phát sinh cho công trình/đơn hàng/hợp đồng kỳ trước tương ứng với TK 154
                                0 AS "NGUYEN_VAT_LIEU" , -- + Tổng số tiền phân bổ của TK 621 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                                0 AS "NHAN_CONG" ,-- + Tổng số tiền phân bổ của TK 622 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo
                                0 AS "MAY_THI_CONG" ,--+ Tổng số tiền phân bổ của TK 623 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                                0 AS "CHI_PHI_CHUNG" ,--+ Tổng số tiền phân bổ của TK 627 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                                0 AS "KHOAN_GIAM_GIA_THANH" ,
                                0 AS "DO_DANG_CUOI_KY"
                        FROM    tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JC
                                INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCED ON JCED."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JC."id"
                                INNER JOIN TMP_DS_CONG_TRINH P ON P."CONG_TRINH_ID" = JCED."MA_DON_VI_ID"
                                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JC."CHI_NHANH_ID"
                        WHERE   JCED."CAP_TO_CHUC" = '1'
                                AND JC."NGAY_CHUNG_TU" BETWEEN tu_ngay AND den_ngay

                        GROUP BY P."CONG_TRINH_ID" ,
                                P."MA_PHAN_CAP"
            ;
        ELSE -- QD 48

                    INSERT INTO  TMP_DU_LIEU_SO_CAI
                            SELECT  P."CONG_TRINH_ID" ,
                                    P."MA_PHAN_CAP" ,

                                    SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                              AND ( GL."MA_TAI_KHOAN" LIKE N'511%%' AND GL."LOAI_NGHIEP_VU" IS  NULL
                                                     --ntquang 14/10/1017 :  CR_149456_Tài khoản đối ứng của số dư đầu kỳ = NULL
                                                    AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG",'') NOT LIKE N'911%%'
                                                  ) THEN GL."GHI_CO"
                                         ELSE 0
                                    END)
                                    - SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                AND GL."MA_TAI_KHOAN" LIKE '511%%' AND GL."LOAI_NGHIEP_VU" IS  NULL
                                                 --ntquang 14/10/1017 :  CR_149456_Tài khoản đối ứng của số dư đầu kỳ = NULL
                                                AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG",'') NOT LIKE N'911%%'
                                                --AND COALESCE(GL."TK_DOI_UNG",'') NOT LIKE N'521%%'
                                           THEN GL."GHI_NO"
                                           ELSE 0
                                      END) AS "DOANH_THU_DOANH_THU_BAN_HANG" --Doanh thu bán hàng: (PS C 511 (Không bao gồm PS ĐƯ Nợ TK 911/Có TK511)– PS N 511 (không bao gồm PS ĐƯ Nợ TK511/Có TK 911, 521)) chi tiết theo từng công trình
                                ,


                                    SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                  AND ( ( GL."MA_TAI_KHOAN" LIKE N'711%%'
                                                          OR GL."MA_TAI_KHOAN" LIKE '515%%'
                                                        )
                                                        --ntquang 14/10/1017 :  CR_149456_Tài khoản đối ứng của số dư đầu kỳ = NULL
                                                        AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG",'') NOT LIKE N'911%%'
                                                      ) THEN GL."GHI_CO"
                                             ELSE 0
                                        END)
                                    - SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                    AND ( GL."MA_TAI_KHOAN" LIKE N'711%%'
                                                          OR GL."MA_TAI_KHOAN" LIKE '515%%'
                                                        )
                                                    AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG",'') NOT LIKE N'911%%'
                                               THEN GL."GHI_NO"
                                               ELSE 0
                                          END) AS "DOANH_THU_THU_NHAP_KHAC" --Đối với QĐ 48 = PS C 515, 711 (Không bao gồm PS ĐƯ Nợ TK911/Có TK515, 711) – PS Nợ TK 515, 711 (không bao gồm PS ĐƯ Nợ TK 515, 711/Có TK 911) chi tiết theo từng công trình
                                    ,
                                    0 AS "TONG_THANH_TOAN" ,
                                --   --ptphuong2 22/09/2016 sửa cách lấy dữ liệu giảm trừ doanh thu theo thông tư 133/qđ 48
                                /*Đối với QĐ 48 = [(PS N511 – PS Có TK 511) chi tiết các nghiệp vụ: Chiết khấu thương mại (bán hàng), Giảm giá hàng bán, Trả lại hàng bán] chi tiết theo từng công trình trên từng chứng từ*/
                                    COALESCE(SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                    THEN CASE WHEN GL."MA_TAI_KHOAN" LIKE N'511%%'
                                                              AND GL."LOAI_HACH_TOAN" = '1'
                                                              AND GL."LOAI_NGHIEP_VU" IS NOT NULL
                                                              THEN GL."GHI_NO"
                                                              WHEN GL."MA_TAI_KHOAN" LIKE N'511%%'
                                                              AND GL."LOAI_HACH_TOAN" = '2'
                                                              AND GL."LOAI_NGHIEP_VU" IS NOT NULL
                                                              THEN -GL."GHI_CO"
                                                         END
                                                    ELSE 0
                                               END), 0) AS "GIAM_TRU_DOANH_THU" ,

                                    SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                  AND GL."MA_TAI_KHOAN" LIKE N'632%%'
                                             THEN GL."GHI_NO"
                                                  - GL."GHI_CO"
                                             ELSE 0
                                        END) AS "GIA_VON" -- Giá vốn hàng bán: Đối với Qd48 = (PSN632 – PSC632) chi tiết theo từng công trình
                                    ,
                                    SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                  AND GL."MA_TAI_KHOAN" LIKE N'6421%%'
                                             THEN GL."GHI_NO"
                                                  - GL."GHI_CO"
                                             ELSE 0
                                        END) AS "CHI_PHI_BAN_HANG" -- Chi phí bán hàng Đối với QĐ 48 = (PSN 6421 – PSC6421) chi tiết theo từng công trình
                                    ,
                                    SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                  AND GL."MA_TAI_KHOAN" LIKE N'6422%%'
                                             THEN GL."GHI_NO"
                                                  - GL."GHI_CO"
                                             ELSE 0
                                        END) AS "CHI_PHI_QUAN_LY" -- Chi phí quản lý: Đối với QĐ 48 = (PSN 6422 – PSC6422) chi tiết theo từng công trình
                                    ,
                                    SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                  AND ( GL."MA_TAI_KHOAN" LIKE N'811%%'
                                                        OR GL."MA_TAI_KHOAN" LIKE N'635%%'
                                                      )
                                             THEN GL."GHI_NO"
                                                  - GL."GHI_CO"
                                             ELSE 0
                                        END) AS "CHI_PHI_KHAC" -- Chi phí khác Đối với QD48 =  (PSN 811, 635 – PSC 811, 635) chi tiết theo từng công trình
                                    ,
                                    SUM(CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                                                  AND LEFT(GL."MA_TAI_KHOAN", 3) IN (
                                                  '154' )
                                                  AND ( E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_CPSX
                                                        OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                                                        OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                                                        OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                                                        OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                                                      )
                                             THEN GL."GHI_NO"
                                                  - GL."GHI_CO"
                                             ELSE 0
                                        END)
                                    - SUM(CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                                                    AND GL."MA_TAI_KHOAN" LIKE N'154%%'
                                                    AND ( E."MA_PHAN_CAP" IS NULL
                                                          OR E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX
                                                        ) THEN GL."GHI_CO"
                                               ELSE 0
                                          END) AS "DO_DANG_DAU_KY" -- QĐ 48 = Tổng chi phí trên form form Nhập lũy kế chi phí phát sinh cho công trình kỳ trước
													  --+ Tổng (PS Nợ - PS Có) của TK154 chi tiết theo KMCP NVLTT, NCTT, MTC, SXC chi tiết theo từng công trình trên chứng từ có ngày hạch toán < “Từ ngày của kỳ báo cáo  – PS Có TK 154 không chi tiết theo KMCP sản xuất có chi tiết theo từng công trình trên chứng từ có ngày hạch toán < "Từ ngày" của kỳ báo cáo + Số đã nghiệm thu trên form Nhập lũy kế chi phí phát sinh cho công trình/đơn hàng/hợp đồng kỳ trước tương ứng với TK 154
                                    ,
                                    SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                             THEN CASE WHEN ( GL."MA_TAI_KHOAN" LIKE N'154%%'
                                                              AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                                                            )
                                                       THEN GL."GHI_NO"
                                                            - GL."GHI_CO"
                                                       ELSE 0
                                                  END
                                             ELSE 0
                                        END) AS "NGUYEN_VAT_LIEU" -- nguyên vật liệu trực tiếp:Đối với QĐ 48: Tổng (PS Nợ - PS Có) của TK154 chi tiết theo KMCP NVLTT chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo
                                    ,
                                    SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                  AND ( GL."MA_TAI_KHOAN" LIKE N'154%%'
                                                        AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                                                      )
                                             THEN GL."GHI_NO"
                                                  - GL."GHI_CO"
                                             ELSE 0
                                        END) AS "NHAN_CONG" -- Chi phí nhân công trực tiếp: Đối với QĐ 48: Tổng (PS Nợ - PS Có) của TK 154 chi tiết theo KMCP NCTT chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo
                                    ,
                                    SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                  AND ( GL."MA_TAI_KHOAN" LIKE N'154%%'
                                                        AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                                                      )
                                             THEN GL."GHI_NO"
                                                  - GL."GHI_CO"
                                             ELSE 0
                                        END) AS "MAY_THI_CONG" --Chi phí máy thi công Đối với QĐ 48: Tổng (PS Nợ - PS Có) của TK 154 chi tiết theo các KMCP MTC chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo
                                    ,
                                    SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                  AND ( GL."MA_TAI_KHOAN" LIKE N'154%%'
                                                        AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                                                      )
                                             THEN GL."GHI_NO"
                                                  - GL."GHI_CO"
                                             ELSE 0
                                        END) AS "CHI_PHI_CHUNG" --Chi phí chung: Đối với QĐ 48: Tổng (PS Nợ - PS Có) của TK 154 chi tiết theo KMCP SXC chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo
                                    ,
                                    SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                                  AND ( GL."MA_TAI_KHOAN" LIKE N'154%%'
                                                        AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'632%%'
                                                      )
                                                  AND E."id" IS NULL
                                             THEN GL."GHI_CO"
                                             ELSE 0
                                        END) AS "KHOAN_GIAM_GIA_THANH" --Giảm giá thành: QĐ48: PS Có TK 154 chi tiết theo từng công trình trên chứng từ không chi tiết theo KMCP có ngày hạch toán thuộc kỳ báo cáo (không kể PSDU Nợ TK 632/có TK 154 chi tiết theo từng công trình
                                    ,
                                    SUM(CASE WHEN GL."NGAY_HACH_TOAN" <= den_ngay
                                                  AND GL."MA_TAI_KHOAN" LIKE N'154%%'
                                                  AND ( E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_CPSX
                                                        OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                                                        OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                                                        OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                                                        OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                                                      )
                                             THEN GL."GHI_NO"
                                                  - GL."GHI_CO"
                                             ELSE 0
                                        END)
                                    - SUM(CASE WHEN GL."NGAY_HACH_TOAN" <= den_ngay
                                                    AND GL."MA_TAI_KHOAN" LIKE N'154%%'
                                                    AND ( E."MA_PHAN_CAP" IS NULL
                                                          OR E."MA_PHAN_CAP" NOT LIKE MA_PHAN_CAP_CPSX
                                                        ) THEN GL."GHI_CO"
                                               ELSE 0
                                          END) AS "DO_DANG_DAU_KY" -- Dở dang cuối kỳ
                            FROM    so_cai_chi_tiet GL
                                    INNER JOIN TMP_DS_CONG_TRINH P ON GL."CONG_TRINH_ID" = P."CONG_TRINH_ID"
                                    INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                                    LEFT JOIN danh_muc_khoan_muc_cp E ON E."id" = GL."KHOAN_MUC_CP_ID"
                            WHERE   GL."NGAY_HACH_TOAN" <= den_ngay
                                    AND ( "MA_TAI_KHOAN" LIKE N'511%%'
                                          OR "MA_TAI_KHOAN" LIKE N'711%%'
                                          OR "MA_TAI_KHOAN" LIKE N'515%%'

                                          OR "MA_TAI_KHOAN" LIKE N'632%%'
                                          OR "MA_TAI_KHOAN" LIKE N'154%%'
                                          OR "MA_TAI_KHOAN" LIKE N'6421%%'
                                          OR "MA_TAI_KHOAN" LIKE N'6422%%'
                                          OR "MA_TAI_KHOAN" LIKE N'811%%'
                                          OR "MA_TAI_KHOAN" LIKE N'635%%'
                                        )

		                        AND (GL."LOAI_CHUNG_TU" <> '610' OR (GL."LOAI_CHUNG_TU" = '610' AND GL."MA_TAI_KHOAN" NOT LIKE '154%%'))
                            GROUP BY P."CONG_TRINH_ID" ,
                                    P."MA_PHAN_CAP"
                            UNION ALL
                            SELECT  P."CONG_TRINH_ID" ,
                                    P."MA_PHAN_CAP" ,
                                    0 AS "DOANH_THU_DOANH_THU_BAN_HANG" ,
                                    0 AS "DOANH_THU_THU_NHAP_KHAC" ,
                                    0 AS "TONG_THANH_TOAN" ,
                                    0 AS "GIAM_TRU_DOANH_THU" ,
                                    0 AS "GIA_VON" ,  -- Giá vốn hàng bán: + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 632 trên chứng từ phân bổ chi phí BH, QLDN, khác
                                    0 AS "CHI_PHI_BAN_HANG" , -- Chi phí bán hàng + + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 6421 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                                    0 AS "CHI_PHI_QUAN_LY" ,-- Chi phí quản lý + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 6422 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                                    0 AS "CHI_PHI_KHAC" , -- Chi phí khác + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 811, 635 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                                    SUM(CASE WHEN J."DEN_NGAY" < tu_ngay
                                              --AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAD."TAI_KHOAN_ID") LIKE N'154%%'
                                                  AND ( E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_CPSX
                                                        OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                                                        OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                                                        OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                                                        OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                                                      )
                                             THEN JCAD."SO_TIEN"
                                             ELSE 0
                                        END) AS "DO_DANG_DAU_KY" ,	-- + Tổng số tiền phân bổ của TK 154 của KMCP NVLTT, NCTT, MTC, SXC cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành < “Từ ngày của kỳ báo cáo
                                    SUM(CASE WHEN J."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
                                              --AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAD."TAI_KHOAN_ID") LIKE N'154%%'
                                                  AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                                             THEN JCAD."SO_TIEN"
                                             ELSE 0
                                        END) AS "NGUYEN_VAT_LIEU" , -- + + Tổng số tiền phân bổ của TK 154 của KMCP NVLTT cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                                    SUM(CASE WHEN J."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
                                              --AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAD."TAI_KHOAN_ID") LIKE N'154%%'
                                                  AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                                             THEN JCAD."SO_TIEN"
                                             ELSE 0
                                        END) AS "NHAN_CONG" ,-- +
                                    SUM(CASE WHEN J."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
                                              --AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAD."TAI_KHOAN_ID") LIKE N'154%%'
                                                  AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                                             THEN JCAD."SO_TIEN"
                                             ELSE 0
                                        END) AS "MAY_THI_CONG" ,--+ + Tổng số tiền phân bổ của TK 154 của KMCP MTC cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                                    SUM(CASE WHEN J."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
                                              --AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAD."TAI_KHOAN_ID") LIKE N'154%%'
                                                  AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                                             THEN JCAD."SO_TIEN"
                                             ELSE 0
                                        END) AS "CHI_PHI_CHUNG" ,--+ + Tổng số tiền phân bổ của TK 154 của KMCP SXC cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                                    0 AS "KHOAN_GIAM_GIA_THANH" ,
                                    SUM(CASE WHEN J."DEN_NGAY" <= den_ngay
                                              --AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAD."TAI_KHOAN_ID") LIKE N'154%%'
                                                  AND ( E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_CPSX
                                                        OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                                                        OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                                                        OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                                                        OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                                                      )
                                             THEN JCAD."SO_TIEN"
                                             ELSE 0
                                        END) AS "DO_DANG_CUOI_KY"
                            FROM    gia_thanh_ket_qua_phan_bo_chi_phi_chung JCAD
                                    INNER JOIN gia_thanh_ky_tinh_gia_thanh J ON J."id" = JCAD."KY_TINH_GIA_THANH_ID"
                                    INNER JOIN TMP_DS_CONG_TRINH P ON P."CONG_TRINH_ID" = JCAD."MA_CONG_TRINH_ID"
                                    INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = J."CHI_NHANH_ID"
                                    LEFT JOIN danh_muc_khoan_muc_cp E ON E."id" = JCAD."KHOAN_MUC_CP_ID"
                            WHERE   J."DEN_NGAY" <= den_ngay --Lấy tất cả các lần phân bổ của kỳ tính giá thành hiện tại và trước đó

                            GROUP BY P."CONG_TRINH_ID" ,
                                    P."MA_PHAN_CAP"
                            UNION ALL
                            SELECT  P."CONG_TRINH_ID" ,
                                    P."MA_PHAN_CAP" ,
                                    0 AS "DOANH_THU_DOANH_THU_BAN_HANG" ,
                                    0 AS "DOANH_THU_THU_NHAP_KHAC" ,
                                    0 AS "TONG_THANH_TOAN" ,
                                    0 AS "GIAM_TRU_DOANH_THU" ,
                                    SUM(CASE WHEN (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'632%%'
                                             THEN JCED."SO_TIEN"
                                             ELSE 0
                                        END) AS "GIA_VON" ,  -- Giá vốn hàng bán: + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 632 trên chứng từ phân bổ chi phí BH, QLDN, khác
                                    SUM(CASE WHEN (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'6421%%'
                                             THEN JCED."SO_TIEN"
                                             ELSE 0
                                        END) AS "CHI_PHI_BAN_HANG" , -- Chi phí bán hàng + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 641 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                                    SUM(CASE WHEN (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'6422%%'
                                             THEN JCED."SO_TIEN"
                                             ELSE 0
                                        END) AS "CHI_PHI_QUAN_LY" ,-- Chi phí quản lý + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 642 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                                    SUM(CASE WHEN ( (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'811%%'
                                                    OR (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'635%%'
                                                  ) THEN JCED."SO_TIEN"
                                             ELSE 0
                                        END) AS "CHI_PHI_KHAC" , -- Chi phí khác + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 811, 635 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                                    0 AS "DO_DANG_DAU_KY" ,	--  + Tổng số tiền phân bổ của TK 621, 622, 623, 627 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc < “Từ ngày của kỳ báo cáo - PS Có TK 154 chi tiết theo từng công trình trên các chứng từ có ngày hạch toán < "Từ ngày" của kỳ báo cáo + Số đã nghiệm thu trên form Nhập lũy kế chi phí phát sinh cho công trình/đơn hàng/hợp đồng kỳ trước tương ứng với TK 154
                                    0 AS "NGUYEN_VAT_LIEU" , -- + Tổng số tiền phân bổ của TK 621 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                                    0 AS "NHAN_CONG" ,-- + Tổng số tiền phân bổ của TK 622 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo
                                    0 AS "MAY_THI_CONG" ,--+ Tổng số tiền phân bổ của TK 623 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                                    0 AS "CHI_PHI_CHUNG" ,--+ Tổng số tiền phân bổ của TK 627 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                                    0 AS "KHOAN_GIAM_GIA_THANH" ,
                                    0 AS "DO_DANG_CUOI_KY"
                            FROM    tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JC
                                    INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCED ON JCED."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JC."id"
                                    INNER JOIN TMP_DS_CONG_TRINH P ON P."CONG_TRINH_ID" = JCED."MA_DON_VI_ID"
                                    INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JC."CHI_NHANH_ID"
                            WHERE   JCED."CAP_TO_CHUC" = '1'
                                    AND JC."NGAY_CHUNG_TU" BETWEEN tu_ngay AND den_ngay

                            GROUP BY P."CONG_TRINH_ID" ,
                                    P."MA_PHAN_CAP" ;



END IF ;

            -- Insert dở dang đầu kỳ
        INSERT INTO  TMP_DU_LIEU_SO_CAI
                SELECT  JP."CONG_TRINH_ID" ,
                        JP."MA_PHAN_CAP" ,
                        0 AS "DOANH_THU_DOANH_THU_BAN_HANG" ,
                        0 AS "DOANH_THU_THU_NHAP_KHAC" ,
                        0 AS "TONG_THANH_TOAN" ,
                        0 AS "GIAM_TRU_DOANH_THU" ,
                        0 AS "GIA_VON" ,  -- Giá vốn hàng bán
                        0 AS "CHI_PHI_BAN_HANG" , -- Chi phí bán hàng
                        0 AS "CHI_PHI_QUAN_LY" ,-- Chi phí quản lý
                        0 AS "CHI_PHI_KHAC" , -- Chi phí khác
                        SUM(JO."SO_CHUA_NGHIEM_THU") AS "DO_DANG_DAU_KY" ,
                        0 AS "NGUYEN_VAT_LIEU" ,
                        0 AS "NHAN_CONG" ,
                        0 AS "MAY_THI_CONG" ,
                        0 AS "CHI_PHI_CHUNG" ,
                        0 AS "KHOAN_GIAM_GIA_THANH" ,
                        SUM(JO."SO_CHUA_NGHIEM_THU") AS "DO_DANG_CUOI_KY"
                FROM   TMP_DS_CONG_TRINH JP
                        LEFT JOIN account_ex_chi_phi_do_dang JO ON JO."MA_CONG_TRINH_ID" = JP."CONG_TRINH_ID"
                        INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JO."CHI_NHANH_ID"
                WHERE   (SELECT  "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JO."TAI_KHOAN_CPSXKD_DO_DANG_ID") LIKE N'154%%'
                GROUP BY JP."CONG_TRINH_ID" ,
                        JP."MA_PHAN_CAP" ;

         -- Lấy số liệu trả ra


    DROP TABLE IF EXISTS TMP_KET_QUA ;
    CREATE TEMP TABLE TMP_KET_QUA
        AS

        SELECT  ROW_NUMBER() OVER ( ORDER BY JP."MA_PHAN_CAP", JP."MA_CONG_TRINH" ) AS "RowNum" ,
                CONCAT(REPEAT(' ',CAST(GP."BAC" * 5 AS INT)),JP."MA_CONG_TRINH") AS "MA_CONG_TRINH" ,
                JP."TEN_CONG_TRINH" ,
                JP."LOAI_CONG_TRINH" ,
                JP."CONG_TRINH_ID" ,

                CAST(CASE WHEN PP."CONG_TRINH_ID" IS NULL THEN 0
                          ELSE 1
                     END AS BOOLEAN) AS IsBold ,
                SUM("DOANH_THU_DOANH_THU_BAN_HANG") AS "DOANH_THU" ,
                SUM("DOANH_THU_THU_NHAP_KHAC") AS "DOANH_THU_THU_NHAP_KHAC" ,
                SUM("DOANH_THU_DOANH_THU_BAN_HANG" + "DOANH_THU_THU_NHAP_KHAC") AS "TONG_THANH_TOAN" ,
                SUM("GIAM_TRU_DOANH_THU") AS "GIAM_TRU_DOANH_THU" ,
                SUM("DOANH_THU_DOANH_THU_BAN_HANG" + "DOANH_THU_THU_NHAP_KHAC"
                    - "GIAM_TRU_DOANH_THU") AS "DOANH_THU_THUAN" , -- doanh thu thuần
                SUM("GIA_VON") AS "GIA_VON_HANG_BAN" ,  -- Giá vốn hàng bán
                SUM("CHI_PHI_BAN_HANG") AS "CHI_PHI_BAN_HANG" , -- Chi phí bán hàng
                SUM("CHI_PHI_QUAN_LY") AS "CHI_PHI_QUAN_LY" ,-- Chi phí quản lý
                SUM("CHI_PHI_KHAC") AS "CHI_PHI_KHAC" , -- Chi phí khác
                SUM("DO_DANG_DAU_KY") AS "DO_DANG_DAU_KY" ,
                SUM("NGUYEN_VAT_LIEU") AS "NGUYEN_VAT_LIEU" ,
                SUM("NHAN_CONG") AS "NHAN_CONG" ,
                SUM("MAY_THI_CONG") AS "MAY_THI_CONG" ,
                SUM("CHI_PHI_CHUNG") AS "CHI_PHI_CHUNG" ,
                SUM("NGUYEN_VAT_LIEU" + "NHAN_CONG" + "MAY_THI_CONG"
                    + "CHI_PHI_CHUNG") AS "CONG" ,
                SUM("KHOAN_GIAM_GIA_THANH") AS "KHOAN_GIAM_GIA_THANH" ,
                SUM("DO_DANG_CUOI_KY") AS "DO_DANG_CUOI_KY" ,
                SUM("DOANH_THU_DOANH_THU_BAN_HANG" + "DOANH_THU_THU_NHAP_KHAC"
                    - "GIAM_TRU_DOANH_THU" - "GIA_VON"
                    - "CHI_PHI_BAN_HANG" - "CHI_PHI_QUAN_LY"
                    - "CHI_PHI_KHAC") AS "LAI_LO" , --Lãi lỗ= Doanh thu thuần – Giá vốn hàng bán – CP bán hàng – CP quản lý – Chi phí khác
                CASE WHEN SUM("DOANH_THU_DOANH_THU_BAN_HANG" + "DOANH_THU_THU_NHAP_KHAC"
                              - "GIAM_TRU_DOANH_THU") > 0
                          AND SUM("DOANH_THU_DOANH_THU_BAN_HANG" + "DOANH_THU_THU_NHAP_KHAC"
                                  - "GIAM_TRU_DOANH_THU" - "GIA_VON"
                                  - "CHI_PHI_BAN_HANG"
                                  - "CHI_PHI_QUAN_LY"
                                  - "CHI_PHI_KHAC") > 0
                     THEN SUM("DOANH_THU_DOANH_THU_BAN_HANG" + "DOANH_THU_THU_NHAP_KHAC"
                              - "GIAM_TRU_DOANH_THU" - "GIA_VON"
                              - "CHI_PHI_BAN_HANG"
                              - "CHI_PHI_QUAN_LY"
                              - "CHI_PHI_KHAC") * 100
                          / SUM("DOANH_THU_DOANH_THU_BAN_HANG" + "DOANH_THU_THU_NHAP_KHAC"
                                - "GIAM_TRU_DOANH_THU")
                     ELSE 0
                END AS "TY_SUAT_LOI_NHUAN_DOANH_THU_PHAN_TRAM" -- Tỷ lệ = Lãi (lỗ)* 100%%/Doanh thu thuần
        FROM    TMP_CONG_TRINH_DUOC_CHON AS JP
                LEFT JOIN TMP_DU_LIEU_SO_CAI CC ON CC."MA_PHAN_CAP" LIKE JP."MA_PHAN_CAP"
                                              || '%%'
                LEFT JOIN TMP_CHA PP ON PP."CONG_TRINH_ID" = JP."CONG_TRINH_ID"
                LEFT JOIN TMP_BAC GP ON GP."CONG_TRINH_ID" = JP."CONG_TRINH_ID"
        GROUP BY
                CONCAT(REPEAT(' ',CAST(GP."BAC" * 5 AS INT)),JP."MA_CONG_TRINH") ,
                JP."TEN_CONG_TRINH" ,
                JP."LOAI_CONG_TRINH" ,
                JP."CONG_TRINH_ID" ,
                CAST(CASE WHEN PP."CONG_TRINH_ID" IS NULL THEN 1
                          ELSE 0
                     END AS BIT) ,
                CAST(CASE WHEN PP."CONG_TRINH_ID" IS NULL THEN 0
                          ELSE 1
                     END AS BOOLEAN) ,
                JP."MA_PHAN_CAP" ,
                JP."MA_CONG_TRINH"
        HAVING  SUM("TONG_THANH_TOAN") <> 0
                OR SUM("DOANH_THU_DOANH_THU_BAN_HANG") <> 0
                OR SUM("DOANH_THU_THU_NHAP_KHAC") <> 0
                OR SUM("GIAM_TRU_DOANH_THU") <> 0
                OR SUM("GIA_VON") <> 0
                OR SUM("CHI_PHI_BAN_HANG") <> 0
                OR SUM("CHI_PHI_QUAN_LY") <> 0
                OR SUM("CHI_PHI_KHAC") <> 0
                OR SUM("DO_DANG_DAU_KY") <> 0
                OR SUM("NGUYEN_VAT_LIEU") <> 0
                OR SUM("NHAN_CONG") <> 0
                OR SUM("MAY_THI_CONG") <> 0
                OR SUM("CHI_PHI_CHUNG") <> 0
                OR SUM("KHOAN_GIAM_GIA_THANH") <> 0
;


END $$
;

SELECT 
                "MA_CONG_TRINH" AS "MA_CONG_TRINH",
                "TEN_CONG_TRINH" AS "TEN_CONG_TRINH",
                "DOANH_THU" AS "DOANH_THU",
                "GIAM_TRU_DOANH_THU" AS "GIAM_TRU_DOANH_THU",
                "DOANH_THU_THUAN" AS "DOANH_THU_THUAN",
                "DO_DANG_DAU_KY" AS "DO_DANG_DAU_KY",
                "NGUYEN_VAT_LIEU" AS "NGUYEN_VAT_LIEU",
                "NHAN_CONG" AS "NHAN_CONG",
                "MAY_THI_CONG" AS "MAY_THI_CONG",
                "CHI_PHI_CHUNG" AS "CHI_PHI_CHUNG",
                "CONG" AS "CONG",
                "KHOAN_GIAM_GIA_THANH" AS "KHOAN_GIAM_GIA_THANH",
                "DO_DANG_CUOI_KY" AS "DO_DANG_CUOI_KY",
                "GIA_VON_HANG_BAN" AS "GIA_VON_HANG_BAN",
                "CHI_PHI_BAN_HANG" AS "CHI_PHI_BAN_HANG",
                "CHI_PHI_QUAN_LY" AS "CHI_PHI_QUAN_LY",
                "CHI_PHI_KHAC" AS "CHI_PHI_KHAC",
                "LAI_LO" AS "LAI_LO",
                "TY_SUAT_LOI_NHUAN_DOANH_THU_PHAN_TRAM" AS "TY_SUAT_LOI_NHUAN_DOANH_THU_PHAN_TRAM"
                
                FROM TMP_KET_QUA

                ORDER BY "RowNum"

                """
        return self.execute(query,params_sql)
     

    ### END IMPLEMENTING CODE ###

    @api.model_cr
    def init(self):
          self.env.cr.execute(""" 
                        DROP FUNCTION IF EXISTS LAY_SO_LIEU_SO_CAI_THEO_CT_THIET_LAP_BCTC_TRA_VE --Func_GetData_Ledger_FinanceReport
            ( IN TU_NGAY_BAT_DAU_TAI_CHINH TIMESTAMP,
            
            tu_ngay TIMESTAMP,
            
            den_ngay TIMESTAMP,
            
            ma_dinh_danh_bao_cao VARCHAR(50),
            
            loai_tien VARCHAR(3),
            
            chi_nhanh_id INTEGER,
            
            bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER
            
            )
            ;
            
            CREATE OR REPLACE FUNCTION LAY_SO_LIEU_SO_CAI_THEO_CT_THIET_LAP_BCTC_TRA_VE
                (IN TU_NGAY_BAT_DAU_TAI_CHINH           TIMESTAMP,
            
                    tu_ngay                             TIMESTAMP,
            
                    den_ngay                            TIMESTAMP,
            
                    ma_dinh_danh_bao_cao                VARCHAR(50),
            
                    loai_tien                           VARCHAR(3),
            
                    chi_nhanh_id                        INTEGER,
            
                    bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER
            
                )
            
            
                RETURNS TABLE(
                    "MA_BAO_CAO_VAT_TU_ID" INT,
                    "TEN_COT"              VARCHAR(50),
            
                    "DON_VI_ID"            INT,
                    "ID_CHUNG_TU"          INT,
                    "MODEL_CHUNG_TU"       VARCHAR(128),
                    "LOAI_CHUNG_TU"        VARCHAR(500),
                    "SO_CHUNG_TU"          VARCHAR(128),
                    "NGAY_CHUNG_TU"        TIMESTAMP,
                    "NGAY_HACH_TOAN"       TIMESTAMP,
            
                    "SO_HOA_DON"           VARCHAR(500),
                    "NGAY_HOA_DON"         TIMESTAMP,
            
                    "DOI_TUONG_ID"         INT,
                    "MA_KHACH_HANG"        VARCHAR(128),
                    "TEN_KHACH_HANG"       VARCHAR(128),
            
                    "SO_TIEN_QUY_DOI"      FLOAT,
                    "SO_TIEN"              FLOAT,
                    "DIEN_GIAI"            VARCHAR(255),
                    "DIEN_GIAI_DETAIL"     VARCHAR(255),
                    "STT"                  INT,
                    "CONG_TRINH_ID"        INT,
                    "DON_DAT_HANG_ID"      INT,
                    "HOP_DONG_ID"          INT
            
                ) AS $$
            
            DECLARE
            
            
                CHE_DO_KE_TOAN VARCHAR;
            
            
            BEGIN
            
            
                DROP TABLE IF EXISTS TMP_LAY_SO_LIEU_SO_CAI_THEO_CT_THIET_LAP_BCTC_TRA_VE_CUOI_CUNG
                ;
            
                CREATE TEMP TABLE TMP_LAY_SO_LIEU_SO_CAI_THEO_CT_THIET_LAP_BCTC_TRA_VE_CUOI_CUNG
            
            
                (
                    "MA_BAO_CAO_VAT_TU_ID" INT,
                    "TEN_COT"              VARCHAR(50),
            
                    "DON_VI_ID"            INT,
                    "ID_CHUNG_TU"          INT,
                    "MODEL_CHUNG_TU"       VARCHAR(128),
                    "LOAI_CHUNG_TU"        VARCHAR(500),
                    "SO_CHUNG_TU"          VARCHAR(128),
                    "NGAY_CHUNG_TU"        TIMESTAMP,
                    "NGAY_HACH_TOAN"       TIMESTAMP,
            
                    "SO_HOA_DON"           VARCHAR(500),
                    "NGAY_HOA_DON"         TIMESTAMP,
            
                    "DOI_TUONG_ID"         INT,
                    "MA_KHACH_HANG"        VARCHAR(128),
                    "TEN_KHACH_HANG"       VARCHAR(128),
            
                    "SO_TIEN_QUY_DOI"      FLOAT,
                    "SO_TIEN"              FLOAT,
                    "DIEN_GIAI"            VARCHAR(255),
                    "DIEN_GIAI_DETAIL"     VARCHAR(255),
                    "STT"                  INT,
                    "CONG_TRINH_ID"        INT,
                    "DON_DAT_HANG_ID"      INT,
                    "HOP_DONG_ID"          INT
                )
                ;
            
            
                SELECT value
                INTO CHE_DO_KE_TOAN
                FROM ir_config_parameter
                WHERE key = 'he_thong.CHE_DO_KE_TOAN'
                FETCH FIRST 1 ROW ONLY
                ;
            
            
                DROP TABLE IF EXISTS TMP_LAY_SO_LIEU_SO_CAI_THEO_CT_THIET_LAP_BCTC_TRA_VE
                ;
            
                CREATE TEMP TABLE TMP_LAY_SO_LIEU_SO_CAI_THEO_CT_THIET_LAP_BCTC_TRA_VE
            
            
                (
                    "MA_BAO_CAO_VAT_TU_ID" INT,
                    "TEN_COT"              VARCHAR(50),
            
                    "DON_VI_ID"            INT,
                    "ID_CHUNG_TU"          INT,
                    "MODEL_CHUNG_TU"       VARCHAR(128),
                    "LOAI_CHUNG_TU"        VARCHAR(500),
                    "SO_CHUNG_TU"          VARCHAR(128),
                    "NGAY_CHUNG_TU"        TIMESTAMP,
                    "NGAY_HACH_TOAN"       TIMESTAMP,
            
                    "SO_HOA_DON"           VARCHAR(500),
                    "NGAY_HOA_DON"         TIMESTAMP,
            
                    "DOI_TUONG_ID"         INT,
                    "MA_KHACH_HANG"        VARCHAR(128),
                    "TEN_KHACH_HANG"       VARCHAR(128),
            
                    "SO_TIEN_QUY_DOI"      FLOAT,
                    "SO_TIEN"              FLOAT,
                    "DIEN_GIAI"            VARCHAR(255),
                    "DIEN_GIAI_DETAIL"     VARCHAR(255),
                    "STT"                  INT,
                    "CONG_TRINH_ID"        INT,
                    "DON_DAT_HANG_ID"      INT,
                    "HOP_DONG_ID"          INT
                )
                ;
            
            
                INSERT INTO TMP_LAY_SO_LIEU_SO_CAI_THEO_CT_THIET_LAP_BCTC_TRA_VE
                ("MA_BAO_CAO_VAT_TU_ID",
                 "TEN_COT",
            
                 "DON_VI_ID",
                 "ID_CHUNG_TU",
                 "MODEL_CHUNG_TU",
                 "LOAI_CHUNG_TU",
                 "SO_CHUNG_TU",
                 "NGAY_CHUNG_TU",
                 "NGAY_HACH_TOAN",
            
                 "SO_HOA_DON",
                 "NGAY_HOA_DON",
            
                 "DOI_TUONG_ID",
                 "MA_KHACH_HANG",
                 "TEN_KHACH_HANG",
            
                 "SO_TIEN_QUY_DOI",
                 "SO_TIEN",
                 "DIEN_GIAI",
                 "DIEN_GIAI_DETAIL",
                 "STT",
                 "CONG_TRINH_ID",
                 "DON_DAT_HANG_ID",
                 "HOP_DONG_ID"
            
                )
                    SELECT
                        FFC."CAU_HINH_LAI_LO_CHO_CT_HD_DH_ID"
                        , FFC."TEN_COT"
            
                        , GL."CHI_NHANH_ID"
                        , GL."ID_CHUNG_TU"
                        , GL."MODEL_CHUNG_TU"
                        , GL."LOAI_CHUNG_TU"
                        , GL."SO_CHUNG_TU"
                        , GL."NGAY_CHUNG_TU"
                        , GL."NGAY_HACH_TOAN"
            
                        , GL."SO_HOA_DON"
                        , GL."NGAY_HOA_DON"
            
                        , GL."DOI_TUONG_ID"
                        , GL."MA_DOI_TUONG"
                        , GL."TEN_DOI_TUONG"
            
                        , (CASE WHEN FFC."MA_HAM" = 'PSCO'
                                     OR (FFC."MA_HAM" = 'PSCO_ChitietChietKhauThuongMai' AND GL."LOAI_NGHIEP_VU" = '0')
                                     OR (FFC."MA_HAM" = 'PSCO_ChitietGiamGiaHangBan' AND GL."LOAI_NGHIEP_VU" = '1')
                                     OR (FFC."MA_HAM" = 'PSCO_ChitietTraLaiHangBan' AND GL."LOAI_NGHIEP_VU" = '2')
                        THEN GL."GHI_CO"
                           WHEN FFC."MA_HAM" IN ('PSNO', 'PSDU')
                                OR (FFC."MA_HAM" IN ('PSNO_ChitietChietKhauThuongMai', 'PSDU_ChitietChietKhauThuongMai') AND
                                    GL."LOAI_NGHIEP_VU" = '0')
                                OR (FFC."MA_HAM" IN ('PSNO_ChitietGiamGiaHangBan', 'PSDU_ChitietGiamGiaHangBan') AND
                                    GL."LOAI_NGHIEP_VU" = '1')
                                OR (FFC."MA_HAM" IN ('PSNO_ChitietTraLaiHangBan', 'PSDU_ChitietTraLaiHangBan') AND
                                    GL."LOAI_NGHIEP_VU" = '2')
                               THEN GL."GHI_NO"
                           WHEN FFC."MA_HAM" = 'DUCO'
                                OR (FFC."MA_HAM" = 'DUCO_ChitietChietKhauThuongMai' AND GL."LOAI_NGHIEP_VU" = '0')
                                OR (FFC."MA_HAM" = 'DUCO_ChitietGiamGiaHangBan' AND GL."LOAI_NGHIEP_VU" = '1')
                                OR (FFC."MA_HAM" = 'DUCO_ChitietTraLaiHangBan' AND GL."LOAI_NGHIEP_VU" = '2')
                               THEN (GL."GHI_CO" - GL."GHI_NO")
                           WHEN FFC."MA_HAM" = 'DUNO'
                                OR (FFC."MA_HAM" = 'DUNO_ChitietChietKhauThuongMai' AND GL."LOAI_NGHIEP_VU" = '0')
                                OR (FFC."MA_HAM" = 'DUNO_ChitietGiamGiaHangBan' AND GL."LOAI_NGHIEP_VU" = '1')
                                OR (FFC."MA_HAM" = 'DUNO_ChitietTraLaiHangBan' AND GL."LOAI_NGHIEP_VU" = '2')
                               THEN (GL."GHI_NO" - GL."GHI_CO")
                           END) * FFC."AM_DUONG" AS "SO_TIEN"
                        , (CASE WHEN FFC."MA_HAM" = 'PSCO'
                                     OR (FFC."MA_HAM" = 'PSCO_ChitietChietKhauThuongMai' AND GL."LOAI_NGHIEP_VU" = '0')
                                     OR (FFC."MA_HAM" = 'PSCO_ChitietGiamGiaHangBan' AND GL."LOAI_NGHIEP_VU" = '1')
                                     OR (FFC."MA_HAM" = 'PSCO_ChitietTraLaiHangBan' AND GL."LOAI_NGHIEP_VU" = '2')
                        THEN GL."GHI_CO_NGUYEN_TE"
                           WHEN FFC."MA_HAM" IN ('PSNO', 'PSDU')
                                OR (FFC."MA_HAM" IN ('PSNO_ChitietChietKhauThuongMai', 'PSDU_ChitietChietKhauThuongMai') AND
                                    GL."LOAI_NGHIEP_VU" = '0')
                                OR (FFC."MA_HAM" IN ('PSNO_ChitietGiamGiaHangBan', 'PSDU_ChitietGiamGiaHangBan') AND
                                    GL."LOAI_NGHIEP_VU" = '1')
                                OR (FFC."MA_HAM" IN ('PSNO_ChitietTraLaiHangBan', 'PSDU_ChitietTraLaiHangBan') AND
                                    GL."LOAI_NGHIEP_VU" = '2')
                               THEN GL."GHI_NO_NGUYEN_TE"
                           WHEN FFC."MA_HAM" = 'DUCO'
                                OR (FFC."MA_HAM" = 'DUCO_ChitietChietKhauThuongMai' AND GL."LOAI_NGHIEP_VU" = '0')
                                OR (FFC."MA_HAM" = 'DUCO_ChitietGiamGiaHangBan' AND GL."LOAI_NGHIEP_VU" = '1')
                                OR (FFC."MA_HAM" = 'DUCO_ChitietTraLaiHangBan' AND GL."LOAI_NGHIEP_VU" = '2')
                               THEN (GL."GHI_CO_NGUYEN_TE" - GL."GHI_NO_NGUYEN_TE")
                           WHEN FFC."MA_HAM" = 'DUNO'
                                OR (FFC."MA_HAM" = 'DUNO_ChitietChietKhauThuongMai' AND GL."LOAI_NGHIEP_VU" = '0')
                                OR (FFC."MA_HAM" = 'DUNO_ChitietGiamGiaHangBan' AND GL."LOAI_NGHIEP_VU" = '1')
                                OR (FFC."MA_HAM" = 'DUNO_ChitietTraLaiHangBan' AND GL."LOAI_NGHIEP_VU" = '2')
                               THEN (GL."GHI_NO_NGUYEN_TE" - GL."GHI_CO_NGUYEN_TE")
                           END) * FFC."AM_DUONG" AS "THANH_TIEN"
                        , GL."DIEN_GIAI_CHUNG"
                        , GL."DIEN_GIAI"
                        , GL."THU_TU_TRONG_CHUNG_TU"
                        , GL."CONG_TRINH_ID"
                        , GL."DON_DAT_HANG_ID"
                        , GL."HOP_DONG_BAN_ID"
                    FROM TIEN_ICH_CAU_HINH_LAI_LO_CHO_CT_HD_DH_CONG_THUC AS FFC
                        INNER JOIN so_cai_chi_tiet AS GL ON GL."MA_TAI_KHOAN" LIKE FFC."MA_TAI_KHOAN" || '%%'
                                                            /*Lấy PS đối ứng*/
                                                            AND (
                                                                (GL."MA_TAI_KHOAN_DOI_UNG" LIKE FFC."TAI_KHOAN_DOI_UNG" || '%%'
                                                                 AND (FFC."MA_HAM" = 'PSDU'
                                                                      OR (FFC."MA_HAM" = 'PSDU_ChitietChietKhauThuongMai' AND
                                                                          GL."LOAI_NGHIEP_VU" = '0')
                                                                      OR (FFC."MA_HAM" = 'PSDU_ChitietGiamGiaHangBan' AND
                                                                          GL."LOAI_NGHIEP_VU" = '1')
                                                                      OR (FFC."MA_HAM" = 'PSDU_ChitietTraLaiHangBan' AND
                                                                          GL."LOAI_NGHIEP_VU" = '2')
                                                                 )
                                                                 OR FFC."MA_HAM" IN ('PSCO', 'PSNO', 'DUNO', 'DUCO')
                                                                 OR (FFC."MA_HAM" IN
                                                                     ('PSCO_ChitietChietKhauThuongMai', 'PSNO_ChitietChietKhauThuongMai', 'DUNO_ChitietChietKhauThuongMai', 'DUCO_ChitietChietKhauThuongMai')
                                                                     AND GL."LOAI_NGHIEP_VU" = '0')
                                                                 /*Phát sinh theo nghiệp vụ chiết khẩu thương mại*/
                                                                 OR (FFC."MA_HAM" IN
                                                                     ('PSCO_ChitietGiamGiaHangBan', 'PSNO_ChitietGiamGiaHangBan', 'DUNO_ChitietGiamGiaHangBan', 'DUCO_ChitietGiamGiaHangBan')
                                                                     AND GL."LOAI_NGHIEP_VU" = '1')
                                                                 /*Phát sinh theo nghiệp vụ giảm giá hàng bán*/
                                                                 OR (FFC."MA_HAM" IN
                                                                     ('PSCO_ChitietTraLaiHangBan', 'PSNO_ChitietTraLaiHangBan', 'DUNO_ChitietTraLaiHangBan', 'DUCO_ChitietTraLaiHangBan')
                                                                     AND GL."LOAI_NGHIEP_VU" = '2')))
                        /*Phát sinh theo nghiệp vụ trả lại hàng bán*/
            
                        INNER JOIN
                                LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc) OU
                            ON GL."CHI_NHANH_ID" = OU."CHI_NHANH_ID"
            
                    WHERE FFC."MA_BAO_CAO" = ma_dinh_danh_bao_cao
                          AND GL."NGAY_HACH_TOAN" <= den_ngay
            
                          AND (
                              -- Điều kiện lấy phát sinh
                              (GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                               AND FFC."MA_HAM" IN ('PSCO', 'PSNO', 'PSDU'
                                  , 'PSCO_ChitietChietKhauThuongMai', 'PSNO_ChitietChietKhauThuongMai', 'PSDU_ChitietChietKhauThuongMai'
                                  , 'PSCO_ChitietGiamGiaHangBan', 'PSNO_ChitietGiamGiaHangBan', 'PSDU_ChitietGiamGiaHangBan'
                                  , 'PSCO_ChitietTraLaiHangBan', 'PSNO_ChitietTraLaiHangBan', 'PSDU_ChitietTraLaiHangBan'
                              )
                               AND FFC."KY" = 11
                              )
                              OR (GL."NGAY_HACH_TOAN" < tu_ngay
                                  AND FFC."MA_HAM" IN ('PSCO', 'PSNO', 'PSDU'
                                  , 'PSCO_ChitietChietKhauThuongMai', 'PSNO_ChitietChietKhauThuongMai', 'PSDU_ChitietChietKhauThuongMai'
                                  , 'PSCO_ChitietGiamGiaHangBan', 'PSNO_ChitietGiamGiaHangBan', 'PSDU_ChitietGiamGiaHangBan'
                                  , 'PSCO_ChitietTraLaiHangBan', 'PSNO_ChitietTraLaiHangBan', 'PSDU_ChitietTraLaiHangBan'
                              )
                                  AND FFC."KY" = 12
                              )
                              OR (GL."NGAY_HACH_TOAN" <= den_ngay
                                  AND FFC."MA_HAM" IN ('PSCO', 'PSNO', 'PSDU'
                                  , 'PSCO_ChitietChietKhauThuongMai', 'PSNO_ChitietChietKhauThuongMai', 'PSDU_ChitietChietKhauThuongMai'
                                  , 'PSCO_ChitietGiamGiaHangBan', 'PSNO_ChitietGiamGiaHangBan', 'PSDU_ChitietGiamGiaHangBan'
                                  , 'PSCO_ChitietTraLaiHangBan', 'PSNO_ChitietTraLaiHangBan', 'PSDU_ChitietTraLaiHangBan'
                              )
                                  AND FFC."KY" = 13
                              )
            
                              OR (GL."NGAY_HACH_TOAN" BETWEEN TU_NGAY_BAT_DAU_TAI_CHINH
                                  AND tu_ngay + INTERVAL '-1 day'
                                  AND FFC."MA_HAM" IN ('PSCO', 'PSNO', 'PSDU'
                                  , 'PSCO_ChitietChietKhauThuongMai', 'PSNO_ChitietChietKhauThuongMai', 'PSDU_ChitietChietKhauThuongMai'
                                  , 'PSCO_ChitietGiamGiaHangBan', 'PSNO_ChitietGiamGiaHangBan', 'PSDU_ChitietGiamGiaHangBan'
                                  , 'PSCO_ChitietTraLaiHangBan', 'PSNO_ChitietTraLaiHangBan', 'PSDU_ChitietTraLaiHangBan'
                              )
                                  AND FFC."KY" = 14
                              )
            
            
                              OR (GL."NGAY_HACH_TOAN" BETWEEN TU_NGAY_BAT_DAU_TAI_CHINH AND den_ngay
                                  AND FFC."MA_HAM" IN ('PSCO', 'PSNO', 'PSDU'
                                  , 'PSCO_ChitietChietKhauThuongMai', 'PSNO_ChitietChietKhauThuongMai', 'PSDU_ChitietChietKhauThuongMai'
                                  , 'PSCO_ChitietGiamGiaHangBan', 'PSNO_ChitietGiamGiaHangBan', 'PSDU_ChitietGiamGiaHangBan'
                                  , 'PSCO_ChitietTraLaiHangBan', 'PSNO_ChitietTraLaiHangBan', 'PSDU_ChitietTraLaiHangBan'
                              )
                                  AND FFC."KY" = 15
                              )
                              -- Điều kiện lấy số dư
                              OR (GL."NGAY_HACH_TOAN" < TU_NGAY_BAT_DAU_TAI_CHINH
                                  AND FFC."MA_HAM" IN ('DUCO', 'DUNO'
                                  , 'DUCO_ChitietChietKhauThuongMai', 'DUNO_ChitietChietKhauThuongMai'
                                  , 'DUCO_ChitietGiamGiaHangBan', 'DUNO_ChitietGiamGiaHangBan'
                                  , 'DUCO_ChitietTraLaiHangBan', 'DUNO_ChitietTraLaiHangBan')
                                  AND FFC."KY" = 21
                              )
                              OR (GL."NGAY_HACH_TOAN" < tu_ngay
                                  AND FFC."MA_HAM" IN ('DUCO', 'DUNO'
                                  , 'DUCO_ChitietChietKhauThuongMai', 'DUNO_ChitietChietKhauThuongMai'
                                  , 'DUCO_ChitietGiamGiaHangBan', 'DUNO_ChitietGiamGiaHangBan'
                                  , 'DUCO_ChitietTraLaiHangBan', 'DUNO_ChitietTraLaiHangBan')
                                  AND FFC."KY" = 22
                              )
                              OR (GL."NGAY_HACH_TOAN" <= den_ngay
                                  AND FFC."MA_HAM" IN ('DUCO', 'DUNO'
                                  , 'DUCO_ChitietChietKhauThuongMai', 'DUNO_ChitietChietKhauThuongMai'
                                  , 'DUCO_ChitietGiamGiaHangBan', 'DUNO_ChitietGiamGiaHangBan'
                                  , 'DUCO_ChitietTraLaiHangBan', 'DUNO_ChitietTraLaiHangBan')
                                  AND FFC."KY" = 23
                              )
            
                          )
            
                          AND (FFC."HE_THONG_KE_TOAN" IS NULL
                               OR FFC."HE_THONG_KE_TOAN" = CHE_DO_KE_TOAN
                          )
            
                          AND (GL."TEN_LOAI_TIEN" = loai_tien
                               OR loai_tien IS NULL
                          )
            
            
                ;
            
                INSERT INTO TMP_LAY_SO_LIEU_SO_CAI_THEO_CT_THIET_LAP_BCTC_TRA_VE_CUOI_CUNG
                    (
                        SELECT
                            KQ."MA_BAO_CAO_VAT_TU_ID"
                            , KQ."TEN_COT"
                            , KQ."DON_VI_ID"
                            , KQ."ID_CHUNG_TU"
                            , KQ."MODEL_CHUNG_TU"
                            , KQ."LOAI_CHUNG_TU"
                            , KQ."SO_CHUNG_TU"
                            , KQ."NGAY_CHUNG_TU"
                            , KQ."NGAY_HACH_TOAN"
                            , KQ."SO_HOA_DON"
                            , KQ."NGAY_HOA_DON"
                            , KQ."DOI_TUONG_ID"
                            , KQ."MA_KHACH_HANG"
                            , KQ."TEN_KHACH_HANG"
                            , KQ."SO_TIEN_QUY_DOI"
                            , KQ."SO_TIEN"
                            , KQ."DIEN_GIAI"
                            , KQ."DIEN_GIAI_DETAIL"
                            , KQ."STT"
                            , KQ."CONG_TRINH_ID"
                            , KQ."DON_DAT_HANG_ID"
                            , KQ."HOP_DONG_ID"
            
                        FROM TMP_LAY_SO_LIEU_SO_CAI_THEO_CT_THIET_LAP_BCTC_TRA_VE AS KQ)
                ;
            
                RETURN QUERY SELECT *
                             FROM TMP_LAY_SO_LIEU_SO_CAI_THEO_CT_THIET_LAP_BCTC_TRA_VE_CUOI_CUNG
                ;
            
            END
            ;
            $$ LANGUAGE PLpgSQL
            ;

          """)



    def _action_view_report(self):
        # self._validate()
        self._validate()
        TU_NGAY_F = self.get_vntime('TU')
        DEN_NGAY_F = self.get_vntime('DEN')
        THONG_KE_THEO = self.get_context('THONG_KE_THEO')
        param = 'Từ ngày: %s đến ngày %s' % (TU_NGAY_F, DEN_NGAY_F)

        action = self.env.ref('bao_cao.open_report_gia_thanh_tong_hop_lai_lo_theo_cong_trinh').read()[0]
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action