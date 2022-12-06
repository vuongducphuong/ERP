# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from operator import itemgetter

class BAO_CAO_SO_TIEN_GUI_NGAN_HANG(models.Model):
    _name = 'bao.cao.so.tien.gui.ngan.hang'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh ', help='Chi nhánh ',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default="True")
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default="DAU_THANG_DEN_HIEN_TAI")
    TU = fields.Date(string='Từ', help='Từ',required=True, default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến',required=True, default=fields.Datetime.now)
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản',required=True)
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID',required=True)
    TK_NGAN_HANG_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='TK Ngân hàng', help='Tài khoản Ngân hàng')
    CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = fields.Boolean(string='Cộng gộp các bút toán giống nhau', help='Cộng gộp các bút toán giống nhau',default="True")
    SAP_XEP_CHUNG_TU_THEO_THU_TU_LAP = fields.Boolean(string='Sắp xếp chứng từ theo thứ tự lập', help='Sắp xếp chứng từ theo thứ tự lập')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán ', help='Ngày hạch toán ')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ ', help='Số chứng từ ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_DOI_UNG = fields.Char(string='TK đối ứng', help='Tài khoản đối ứng')
    THU = fields.Float(string='Thu ', help='Thu ')
    CHI = fields.Float(string='Chi', help='Chi')
    TON = fields.Float(string='Tồn', help='Tồn')
    TAI_KHOAN_NGAN_HANG = fields.Char(string='Tài khoản ngân hàng', help='Tài khoản ngân hàng')

    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')


    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')
		
		
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN



    #FIELD_IDS = fields.One2many('model.name')
    def _validate(self):
       params = self._context
       TU = params['TU'] if 'TU' in params.keys() else 'False'
       DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
       if(TU=='False'):
           raise ValidationError('Vui lòng nhập thời gian cho Từ !')
       if(DEN=='False'):
           raise ValidationError('Vui lòng nhập thời gian cho Đến !')
    ### START IMPLEMENTING CODE ###
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() else 'False'
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() else 'False'
        KY_BAO_CAO = params['KY_BAO_CAO'] if 'KY_BAO_CAO' in params.keys() else 'False'
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

        # NHAN_VIEN_ID = params['NHAN_VIEN_ID'] if 'NHAN_VIEN_ID' in params.keys() and params['NHAN_VIEN_ID'] != 'False' else -1
        TAI_KHOAN_ID = params['TAI_KHOAN_ID'] if 'TAI_KHOAN_ID' in params.keys() and params['TAI_KHOAN_ID'] != 'False' else -1 
        currency_id = params['currency_id'] if 'currency_id' in params.keys() and params['currency_id'] != 'False' else -1 
        TK_NGAN_HANG_ID = params['TK_NGAN_HANG_ID'] if 'TK_NGAN_HANG_ID' in params.keys() and params['TK_NGAN_HANG_ID'] != 'False' else None
        CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = params['CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU'] if 'CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU' in params.keys() else 'False'
        SAP_XEP_CHUNG_TU_THEO_THU_TU_LAP = params['SAP_XEP_CHUNG_TU_THEO_THU_TU_LAP'] if 'SAP_XEP_CHUNG_TU_THEO_THU_TU_LAP' in params.keys() else 'False'
        # Execute SQL query here
        MA_TK = self.env['danh.muc.he.thong.tai.khoan'].search([('id', '=', TAI_KHOAN_ID)], limit=1).SO_TAI_KHOAN
        # TEN_LOAI_TIEN = self.env['res.currency'].search([('id', '=', currency_id)], limit=1).TEN_LOAI_TIEN
        loai_tien = ''
        if currency_id == 'False':
            currency_id = -1
        record = []
        params = {
            'TU_NGAY':TU_NGAY_F, 
            'DEN_NGAY':DEN_NGAY_F, 
            # 'MA_TK':MA_TK, 
            'CHI_NHANH_ID': CHI_NHANH_ID, 
            'currency_id':currency_id, 
            'TAI_KHOAN_ID' : TAI_KHOAN_ID,
            'TK_NGAN_HANG_ID' : TK_NGAN_HANG_ID,
            'CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU':1 if CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU == 'True' else 0, 
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':1 if BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC == 'True' else 0,
            'limit': limit,
            'offset': offset,
            # 'SAP_XEP_CHUNG_TU_THEO_THU_TU_LAP': SAP_XEP_CHUNG_TU_THEO_THU_TU_LAP,
            }      

        query = """
        DO LANGUAGE plpgsql $$
        DECLARE
        ts_currency_id              INTEGER := %(currency_id)s;
        tu_ngay                     DATE := %(TU_NGAY)s;
        den_ngay                    DATE := %(DEN_NGAY)s;
        chi_nhanh_id                INTEGER := %(CHI_NHANH_ID)s;
        bao_gom_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;
        cong_gop_but_toan           INTEGER := %(CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU)s;
        so_ton                      FLOAT = 0;
        rec                         RECORD;
        tai_khoan_ngan_hang_id      INTEGER := %(TK_NGAN_HANG_ID)s;
        tai_khoan_id                INTEGER := %(TAI_KHOAN_ID)s;
        tai_khoan_pt                VARCHAR(255);
        tai_khoan_ngan_hang VARCHAR(500);


        BEGIN

        SELECT concat("SO_TAI_KHOAN", '%%')
        INTO tai_khoan_pt
        FROM danh_muc_he_thong_tai_khoan
        WHERE id = tai_khoan_id;

        DROP TABLE IF EXISTS TMP_KET_QUA;

         DROP SEQUENCE IF EXISTS TMP_KET_QUA_seq
            ;

        CREATE TEMP SEQUENCE TMP_KET_QUA_seq
        ;
        CREATE TEMP TABLE TMP_KET_QUA (
            RowNum             INT DEFAULT NEXTVAL('TMP_KET_QUA_seq')
            PRIMARY KEY,

            "TAI_KHOAN_NGAN_HANG"  VARCHAR(500),
            "ID_CHUNG_TU"          INTEGER,
            "MODEL_CHUNG_TU"       VARCHAR(127),
            "NGAY_HACH_TOAN"       DATE,
            "NGAY_CHUNG_TU"        DATE,
            "SO_CHUNG_TU"          VARCHAR(127),
            "DIEN_GIAI"            VARCHAR(200),
            "MA_TAI_KHOAN_DOI_UNG" VARCHAR(127),
            "SO_TIEN_THU"          FLOAT,
            "SO_TIEN_CHI"          FLOAT,
            "SO_TIEN_TON"          FLOAT,
            "LOAI_DAT_HANG"        INTEGER,
            "LOAI_THANH_TOAN" INTEGER
        );

        DROP TABLE IF EXISTS TMP_KET_QUA_1;

         DROP SEQUENCE IF EXISTS TMP_KET_QUA_1_seq
            ;

        CREATE TEMP SEQUENCE TMP_KET_QUA_1_seq
        ;
        CREATE TEMP TABLE TMP_KET_QUA_1 (
            RowNum             INT DEFAULT NEXTVAL('TMP_KET_QUA_1_seq')
            PRIMARY KEY,

            "TAI_KHOAN_NGAN_HANG"  VARCHAR(500),
            "ID_CHUNG_TU"          INTEGER,
            "MODEL_CHUNG_TU"       VARCHAR(127),
            "NGAY_HACH_TOAN"       DATE,
            "NGAY_CHUNG_TU"        DATE,
            "SO_CHUNG_TU"          VARCHAR(127),
            "DIEN_GIAI"            VARCHAR(200),
            "MA_TAI_KHOAN_DOI_UNG" VARCHAR(127),
            "SO_TIEN_THU"          FLOAT,
            "SO_TIEN_CHI"          FLOAT,
            "SO_TIEN_TON"          FLOAT,
            "LOAI_DAT_HANG"        INTEGER,
            "LOAI_THANH_TOAN" INTEGER
        );




             INSERT INTO TMP_KET_QUA
                 (
                        "TAI_KHOAN_NGAN_HANG" ,
                        "ID_CHUNG_TU"          ,
                        "MODEL_CHUNG_TU"      ,
                        "NGAY_HACH_TOAN"       ,
                        "NGAY_CHUNG_TU"        ,
                        "SO_CHUNG_TU"         ,
                        "DIEN_GIAI"           ,
                        "MA_TAI_KHOAN_DOI_UNG" ,
                        "SO_TIEN_THU"          ,
                        "SO_TIEN_CHI"          ,
                        "SO_TIEN_TON"          ,
                        "LOAI_DAT_HANG"        ,
                        "LOAI_THANH_TOAN"
                 )


            SELECT

            CASE WHEN tai_khoan_ngan_hang_id IS NULL
                THEN ''
            ELSE CASE WHEN NH."TEN_DAY_DU" IS NOT NULL
                THEN concat(coalesce(GL."SO_TAI_KHOAN_NGAN_HANG", ''), ' - ', coalesce(NH."TEN_DAY_DU", ''))
                ELSE coalesce(GL."SO_TAI_KHOAN_NGAN_HANG", '')
                END
            END,
            NULL :: INT                                 AS "ID_CHUNG_TU",
            ''                                          AS "MODEL_CHUNG_TU",
            NULL :: DATE                                AS "NGAY_HACH_TOAN",
            NULL :: DATE                                AS "NGAY_CHUNG_TU",
            ''                                          AS "SO_CHUNG_TU",
            N'Số dư đầu kỳ'                            AS "DIEN_GIAI",
            ''                                          AS "MA_TAI_KHOAN_DOI_UNG",
            0                                           AS "SO_TIEN_THU",
            0                                           AS "SO_TIEN_CHI",
            COALESCE(SUM(GL."GHI_NO" - GL."GHI_CO"), 0) AS "TON",
            0                                           AS "LOAI_DAT_HANG",
            NULL ::INT AS "LOAI_THANH_TOAN"

            FROM so_cai_chi_tiet AS GL
            INNER JOIN LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_chi_nhanh_phu_thuoc) BR
                ON BR."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
            LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA.id = GL."TAI_KHOAN_NGAN_HANG_ID"
            LEFT JOIN danh_muc_ngan_hang NH ON BA."NGAN_HANG_ID" = NH.id


            WHERE GL."NGAY_HACH_TOAN" < tu_ngay
                AND GL."MA_TAI_KHOAN" LIKE tai_khoan_pt
                          AND ( tai_khoan_ngan_hang_id IS NULL
                OR ( (GL."TAI_KHOAN_NGAN_HANG_ID" = tai_khoan_ngan_hang_id
                     AND tai_khoan_ngan_hang_id <> -1 )
                   )
                OR tai_khoan_ngan_hang_id = -1 OR tai_khoan_ngan_hang_id  IS NULL
                    )
                AND (ts_currency_id  = -1
                    OR GL.currency_id = ts_currency_id
                )

            GROUP BY
            CASE WHEN tai_khoan_ngan_hang_id IS NULL
                THEN ''
            ELSE CASE WHEN NH."TEN_DAY_DU" IS NOT NULL
                THEN concat(coalesce(GL."SO_TAI_KHOAN_NGAN_HANG", ''), ' - ', coalesce(NH."TEN_DAY_DU", ''))
                ELSE coalesce(GL."SO_TAI_KHOAN_NGAN_HANG", '')
                END
            END,
            GL."SO_TAI_KHOAN_NGAN_HANG"
            HAVING COALESCE(SUM(GL."GHI_NO_NGUYEN_TE" - GL."GHI_CO_NGUYEN_TE"), 0) <> 0
                OR COALESCE(SUM(GL."GHI_NO" - GL."GHI_CO"), 0) <> 0

        ;

        IF cong_gop_but_toan = 1
        THEN
            INSERT INTO TMP_KET_QUA
                 (
                        "TAI_KHOAN_NGAN_HANG" ,
                        "ID_CHUNG_TU"          ,
                        "MODEL_CHUNG_TU"      ,
                        "NGAY_HACH_TOAN"       ,
                        "NGAY_CHUNG_TU"        ,
                        "SO_CHUNG_TU"         ,
                        "DIEN_GIAI"           ,
                        "MA_TAI_KHOAN_DOI_UNG" ,
                        "SO_TIEN_THU"          ,
                        "SO_TIEN_CHI"          ,
                        "SO_TIEN_TON"          ,
                        "LOAI_DAT_HANG"        ,
                        "LOAI_THANH_TOAN"
                 )
            SELECT

                CASE WHEN tai_khoan_ngan_hang_id IS NULL
                THEN ''
                ELSE CASE WHEN NH."TEN_DAY_DU" IS NOT NULL
                THEN concat(coalesce(GL."SO_TAI_KHOAN_NGAN_HANG", ''), ' - ', coalesce(NH."TEN_DAY_DU", ''))
                    ELSE coalesce(GL."SO_TAI_KHOAN_NGAN_HANG", '')
                    END
                END AS "TAI_KHOAN_NGAN_HANG",
                GL."ID_CHUNG_TU",
                GL."MODEL_CHUNG_TU",
                GL."NGAY_HACH_TOAN"           AS "NGAY_HACH_TOAN",
                GL."NGAY_CHUNG_TU",
                GL."SO_CHUNG_TU"              AS "SO_CHUNG_TU",
                GL."DIEN_GIAI_CHUNG"          AS "DIEN_GIAI",
                GL."MA_TAI_KHOAN_DOI_UNG",
                COALESCE(SUM(GL."GHI_NO"), 0) AS "SO_TIEN_THU",
                COALESCE(SUM("GHI_CO"), 0)    AS "SO_TIEN_CHI",
                0                             AS "SO_TIEN_TON",
                1                             AS "LOAI_DAT_HANG",
                CASE WHEN SUM("GHI_NO") <> 0 THEN 0
                    ELSE 1
                END AS "LOAI_THANH_TOAN"
            FROM so_cai_chi_tiet AS GL
                LEFT JOIN LATERAL ( SELECT COUNT(DISTINCT GL1."DOI_TUONG_ID") AS AccountObjectCount
                                    FROM so_cai_chi_tiet GL1
                                    WHERE GL1."ID_CHUNG_TU" = GL."ID_CHUNG_TU"
                                        AND GL1."MA_TAI_KHOAN" = GL."MA_TAI_KHOAN"
                                        AND GL1."MA_TAI_KHOAN_DOI_UNG" = GL."MA_TAI_KHOAN_DOI_UNG"
                        --                                                     AND (@BankAccountID IS NULL OR GL1.BankAccountID = GL.BankAccountID)
                        --                                           GROUP BY  GL1."ID_CHUNG_TU" ,
                        --                                                     GL1."MA_TK" ,
                        --                                                     GL1."MA_TAI_KHOAN_DOI_UNG" ,
                        --                                                     CASE WHEN @BankAccountID IS NULL THEN @BankAccountAll ELSE  GL1.BankAccountID END
                        ) GL1 ON TRUE
                INNER JOIN (SELECT *
                            FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_chi_nhanh_phu_thuoc)) BR
                ON BR."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA.id = GL."TAI_KHOAN_NGAN_HANG_ID"
                LEFT JOIN danh_muc_ngan_hang NH ON BA."NGAN_HANG_ID" = NH.id
            WHERE GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                    AND GL."MA_TAI_KHOAN" LIKE tai_khoan_pt
                    AND (tai_khoan_ngan_hang_id = -1 OR tai_khoan_ngan_hang_id  IS NULL
                        OR ((GL."TAI_KHOAN_NGAN_HANG_ID" = tai_khoan_ngan_hang_id
                            AND tai_khoan_ngan_hang_id <> -1)
                        )
                    )
                    AND (ts_currency_id  = -1
                        OR GL.currency_id = ts_currency_id
                    )
            GROUP BY GL."ID_CHUNG_TU",
                GL."NGAY_HACH_TOAN",
                GL."NGAY_CHUNG_TU",
                GL."SO_CHUNG_TU",
                GL."LOAI_CHUNG_TU",
                GL."DIEN_GIAI_CHUNG",
                GL."MA_TAI_KHOAN_DOI_UNG",
                GL."TY_GIA",
                GL."CHI_NHANH_ID",
                BR."MA_CHI_NHANH",
                BR."TEN_CHI_NHANH",
                GL."MODEL_CHUNG_TU",
                CASE WHEN tai_khoan_ngan_hang_id IS NULL
                THEN ''
                ELSE CASE WHEN NH."TEN_DAY_DU" IS NOT NULL
                THEN concat(coalesce(GL."SO_TAI_KHOAN_NGAN_HANG", ''), ' - ', coalesce(NH."TEN_DAY_DU", ''))
                    ELSE coalesce(GL."SO_TAI_KHOAN_NGAN_HANG", '')
                    END
                END,
                CASE WHEN GL1.AccountObjectCount > 1
                THEN NULL
                ELSE GL."MA_DOI_TUONG"
                END, --NVTOAN add 09/08/2017: Thực hiện PBI 125410
                CASE WHEN GL1.AccountObjectCount > 1
                THEN NULL
                ELSE GL."TEN_DOI_TUONG"
                END
            HAVING COALESCE(SUM(GL."GHI_NO_NGUYEN_TE"), 0) <> 0
                    OR COALESCE(SUM("GHI_CO_NGUYEN_TE"), 0) <> 0
                    OR COALESCE(SUM(GL."GHI_NO"), 0) <> 0
                    OR COALESCE(SUM("GHI_CO"), 0) <> 0
            ORDER BY
                "TAI_KHOAN_NGAN_HANG",
                 "NGAY_HACH_TOAN",
                 "NGAY_CHUNG_TU",
                "LOAI_THANH_TOAN",
                "SO_CHUNG_TU",
                 "MA_TAI_KHOAN_DOI_UNG"
            ;
        ELSE
           INSERT INTO TMP_KET_QUA
                 (
                        "TAI_KHOAN_NGAN_HANG" ,
                        "ID_CHUNG_TU"          ,
                        "MODEL_CHUNG_TU"      ,
                        "NGAY_HACH_TOAN"       ,
                        "NGAY_CHUNG_TU"        ,
                        "SO_CHUNG_TU"         ,
                        "DIEN_GIAI"           ,
                        "MA_TAI_KHOAN_DOI_UNG" ,
                        "SO_TIEN_THU"          ,
                        "SO_TIEN_CHI"          ,
                        "SO_TIEN_TON"          ,
                        "LOAI_DAT_HANG"        ,
                        "LOAI_THANH_TOAN"
                 )
            SELECT


                CASE WHEN tai_khoan_ngan_hang_id IS NULL
                THEN ''
                ELSE CASE WHEN NH."TEN_DAY_DU" IS NOT NULL
                THEN concat(coalesce(GL."SO_TAI_KHOAN_NGAN_HANG", ''), ' - ', coalesce(NH."TEN_DAY_DU", ''))
                    ELSE coalesce(GL."SO_TAI_KHOAN_NGAN_HANG", '')
                    END
                END AS "TAI_KHOAN_NGAN_HANG",
                GL."ID_CHUNG_TU",
                GL."MODEL_CHUNG_TU",
                GL."NGAY_HACH_TOAN",
                GL."NGAY_CHUNG_TU",
                GL."SO_CHUNG_TU",
                CASE WHEN GL."DIEN_GIAI" IS NULL
                                      OR LTRIM(GL."DIEN_GIAI") = ''
                                 THEN GL."DIEN_GIAI_CHUNG"
                                 ELSE GL."DIEN_GIAI"
                            END AS "DIEN_GIAI_CHUNG" ,

                GL."MA_TAI_KHOAN_DOI_UNG",
                GL."GHI_NO" AS "SO_TIEN_THU",
                GL."GHI_CO" AS "SO_TIEN_CHI",
                0           AS "SO_TIEN_TON",
                1           AS "LOAI_DAT_HANG",
                CASE WHEN "GHI_NO" <> 0 THEN 0
                    ELSE 1
                END AS "LOAI_THANH_TOAN"
            FROM so_cai_chi_tiet AS GL
                INNER JOIN LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_chi_nhanh_phu_thuoc) BR
                ON BR."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                LEFT JOIN LATERAL ( SELECT COUNT(DISTINCT GL1."DOI_TUONG_ID") AS AccountObjectCount
                                    FROM so_cai_chi_tiet GL1
                                    WHERE GL1."ID_CHUNG_TU" = GL."ID_CHUNG_TU"
                                        AND GL1."MA_TAI_KHOAN" = GL."MA_TAI_KHOAN"
                                        AND GL1."MA_TAI_KHOAN_DOI_UNG" = GL."MA_TAI_KHOAN_DOI_UNG"
                        ) GL1 ON TRUE
                LEFT JOIN danh_muc_tai_khoan_ngan_hang BA ON BA.id = GL."TAI_KHOAN_NGAN_HANG_ID"
                LEFT JOIN danh_muc_ngan_hang NH ON BA."NGAN_HANG_ID" = NH.id
            WHERE GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                    AND GL."MA_TAI_KHOAN" LIKE tai_khoan_pt
                    AND (tai_khoan_ngan_hang_id = -1 OR tai_khoan_ngan_hang_id  IS NULL
                        OR ((GL."TAI_KHOAN_NGAN_HANG_ID" = tai_khoan_ngan_hang_id
                            AND tai_khoan_ngan_hang_id <> -1)
                        )
                    )
                    AND (ts_currency_id IS NULL
                        OR GL.currency_id = ts_currency_id
                    )
                    AND (GL."GHI_NO_NGUYEN_TE" <> 0
                        OR GL."GHI_CO_NGUYEN_TE" <> 0
                        OR GL."GHI_NO" <> 0
                        OR GL."GHI_CO" <> 0
                    )
            ORDER BY
                "TAI_KHOAN_NGAN_HANG",
                "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU",
                "LOAI_THANH_TOAN" ,
                "SO_CHUNG_TU",
                 "MA_TAI_KHOAN_DOI_UNG"
            ;
        END IF;

        INSERT INTO TMP_KET_QUA_1
                 (
                        "TAI_KHOAN_NGAN_HANG" ,
                        "ID_CHUNG_TU"          ,
                        "MODEL_CHUNG_TU"      ,
                        "NGAY_HACH_TOAN"       ,
                        "NGAY_CHUNG_TU"        ,
                        "SO_CHUNG_TU"         ,
                        "DIEN_GIAI"           ,
                        "MA_TAI_KHOAN_DOI_UNG" ,
                        "SO_TIEN_THU"          ,
                        "SO_TIEN_CHI"          ,
                        "SO_TIEN_TON"          ,
                        "LOAI_DAT_HANG"        ,
                        "LOAI_THANH_TOAN"
                 )
            SELECT


                        "TAI_KHOAN_NGAN_HANG" ,
                        "ID_CHUNG_TU"          ,
                        "MODEL_CHUNG_TU"      ,
                        "NGAY_HACH_TOAN"       ,
                        "NGAY_CHUNG_TU"        ,
                        "SO_CHUNG_TU"         ,
                        "DIEN_GIAI"           ,
                        "MA_TAI_KHOAN_DOI_UNG" ,
                        "SO_TIEN_THU"          ,
                        "SO_TIEN_CHI"          ,
                        "SO_TIEN_TON"          ,
                        "LOAI_DAT_HANG"        ,
                        "LOAI_THANH_TOAN"
            FROM TMP_KET_QUA
                ORDER BY "TAI_KHOAN_NGAN_HANG","LOAI_DAT_HANG","NGAY_HACH_TOAN","NGAY_CHUNG_TU","LOAI_THANH_TOAN","SO_CHUNG_TU", "MA_TAI_KHOAN_DOI_UNG"
        ;

        FOR rec IN
        SELECT *
        FROM TMP_KET_QUA_1
             ORDER BY
            RowNum
        LOOP
            SELECT CASE WHEN rec."LOAI_DAT_HANG" = 0
            THEN (CASE WHEN rec."SO_TIEN_TON" = 0
                THEN 0
                    ELSE rec."SO_TIEN_TON"
                    END)
                WHEN tai_khoan_ngan_hang <> rec."TAI_KHOAN_NGAN_HANG"
                    THEN rec."SO_TIEN_THU" - rec."SO_TIEN_CHI"
                ELSE so_ton + rec."SO_TIEN_THU"
                        - rec."SO_TIEN_CHI"
                END
            INTO so_ton;

            rec."SO_TIEN_TON" = so_ton;

            UPDATE TMP_KET_QUA_1
            SET "SO_TIEN_TON" =  rec."SO_TIEN_TON"
            WHERE  RowNum = rec.RowNum ;
            tai_khoan_ngan_hang := rec."TAI_KHOAN_NGAN_HANG";
        END LOOP;


        END $$;

        SELECT *
        FROM TMP_KET_QUA_1
        ORDER BY "TAI_KHOAN_NGAN_HANG","LOAI_DAT_HANG","NGAY_HACH_TOAN","NGAY_CHUNG_TU","LOAI_THANH_TOAN","SO_CHUNG_TU"
        OFFSET %(offset)s
        LIMIT %(limit)s

        ;

"""
        # Số dư đầu kỳ
        cr = self.env.cr
        cr.execute(query,params)
        # Get and show result
        for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
            record.append({
                'NGAY_HACH_TOAN': line.get('NGAY_HACH_TOAN', ''),
                'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU', ''),
                'SO_CHUNG_TU': line.get('SO_CHUNG_TU', ''),
                'DIEN_GIAI': line.get('DIEN_GIAI', ''),
                'TK_DOI_UNG': line.get('MA_TAI_KHOAN_DOI_UNG', ''),
                'THU': line.get('SO_TIEN_THU', ''),
                'CHI': line.get('SO_TIEN_CHI', ''),
                'TON': line.get('SO_TIEN_TON', ''),
                'TAI_KHOAN_NGAN_HANG': line.get('TAI_KHOAN_NGAN_HANG', ''),
                'ID_GOC': line.get('ID_CHUNG_TU', ''),
                'MODEL_GOC': line.get('MODEL_CHUNG_TU', ''),
                })
        return record

        # Phát sinh trong kỳ
        # phat_sinh = self.execute(query,params)
        # ton = 0
        # for line in phat_sinh:
        #     ton = ton + float(line.get('Thu',0)) - float(line.get('Chi',0))
        #     line['TON'] = ton
            
        # record += phat_sinh
        # return helper.List.update(record, fields)


    @api.model
    def default_get(self, fields_list):
       result = super(BAO_CAO_SO_TIEN_GUI_NGAN_HANG, self).default_get(fields_list)
       result['CHI_NHANH_ID'] = self.env['danh.muc.to.chuc'].search([],limit=1).id
       result['TAI_KHOAN_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('CHI_TIET_THEO_TAI_KHOAN_NGAN_HANG','=','True')],limit=1).id
       result['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')],limit=1).id
       result['TK_NGAN_HANG_ID'] = self.env['danh.muc.tai.khoan.ngan.hang'].search([],limit=1).id
       return result

    
   
    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU')
        DEN_NGAY_F = self.get_vntime('DEN')
        currency_id = self.get_context('currency_id')
        loai_tien = self.env['res.currency'].browse(currency_id).name
        TAI_KHOAN_ID = self.get_context('TAI_KHOAN_ID')
        tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].browse(TAI_KHOAN_ID).SO_TAI_KHOAN
        param = 'Tài khoản: %s; Loại tiền: %s; Từ ngày: %s đến ngày %s' % (tai_khoan, loai_tien, TU_NGAY_F, DEN_NGAY_F)
        action = self.env.ref('bao_cao.open_report__so_tien_gui_ngan_hang').read()[0]

        # # action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action

class BAO_CAO_SO_TIEN_GUI_NGAN_HANG_REPORT(models.AbstractModel):
    _name = 'report.bao_cao.template_so_tien_gui_ngan_hang'

    @api.model
    def get_report_values(self, docids, data=None):
        env = self.env[data.get('model')]
        docs = [env.new(d) for d in env.with_context(data.get('context')).search_read()]
        
        added_data = {
            'tieu_de_nguoi_ky': self.get_danh_sach_tieu_de_nguoi_ky(data.get('model')),
            'ten_nguoi_ky': self.get_danh_sach_ten_nguoi_ky(data.get('model')),
            'sub_title': data.get('breadcrumb')
        }
        return {
            'docs': docs,
            'added_data': added_data,
            'o': self,
        }