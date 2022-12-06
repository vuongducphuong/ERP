# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from operator import itemgetter
from odoo.addons import decimal_precision

class BAO_CAO_SO_KE_TOAN_CHI_TIET_QUY_TIEN_MAT(models.Model):
    _name = 'bao.cao.so.ke.toan.chi.tiet.quy.tien.mat'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm dữ liệu chi nhánh phụ thuộc', help='Bao gồm dữ liệu của chi nhánh phụ thuộc')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',required=True, default='DAU_THANG_DEN_HIEN_TAI')
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID',required=True)
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày')
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_PHIEU_THU = fields.Char(string='Số phiếu thu', help='Số phiếu thu')
    SO_PHIEU_CHI = fields.Char(string='Số phiếu chi', help='Số phiếu chi')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TAI_KHOAN = fields.Char(string='Tài khoản', help='Tài khoản')
    TK_DOI_UNG = fields.Char(string='TK đối ứng', help='TK đối ứng')
    PS_NO = fields.Float(string='Nợ', digits=decimal_precision.get_precision('VND'))
    PS_CO = fields.Float(string='Có', digits=decimal_precision.get_precision('VND'))
    SO_TON = fields.Float(string='Số tồn', help='Số tồn', digits=decimal_precision.get_precision('VND'))
    NGUOI_NHAN_NOP = fields.Char(string='Người nhận/Người nộp', help='Người nhận/Người nộp')
    LOAI_PHIEU = fields.Selection([('0', 'Số tồn'),('1', 'Phiếu thu'),('2', 'Phiếu chi')])
    CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = fields.Boolean(string='Cộng gộp các bút toán giống nhau')
    SAP_XEP_CHUNG_TU_THEO_THU_TU_LAP = fields.Boolean(string='Sắp xếp chứng từ theo thứ tự lập')

    TAI_KHOAN_IDS = fields.One2many('danh.muc.he.thong.tai.khoan')
    MODEL_GOC = fields.Char()
    ID_GOC = fields.Char()
	
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    ### START IMPLEMENTING CODE ###
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_SO_KE_TOAN_CHI_TIET_QUY_TIEN_MAT, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([], limit=1)
        loai_tien =  self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')],limit=1)
        tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=like','111%')])
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        if tai_khoan:
            result['TAI_KHOAN_IDS'] = tai_khoan.ids
        if loai_tien:
            result['currency_id'] = loai_tien.id
        return result

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU_NGAY', 'DEN_NGAY')

    def _validate(self):
        TAI_KHOAN_IDS = self.get_context('TAI_KHOAN_IDS')
        if TAI_KHOAN_IDS == None :
            raise ValidationError('Vui lòng chọn một tài khoản!')

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        if not self.get_context('active_model'):
            return
        record = []
        # Get paramerters here
        CHI_NHANH_ID = self.get_context('CHI_NHANH_ID')
        if not CHI_NHANH_ID:
            raise ValidationError('Vui lòng chọn tham số!')
        # Execute SQL query here
        cr = self.env.cr
        # Bổ sung thông tin tài khoản
        ########################################
        TU_NGAY = self.get_dbtime('TU_NGAY')
        DEN_NGAY = self.get_dbtime('DEN_NGAY')
        TAI_KHOAN_IDS = tuple([tk['id'] for tk in self.get_context('TAI_KHOAN_IDS')])
        CHI_NHANH_ID = self.get_context('CHI_NHANH_ID')
        currency_id = self.get_context('currency_id')
        CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = 1 if self.get_context('CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU') == 'True' else 0
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if self.get_context('BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC') == 'True' else 0
        SAP_XEP_CHUNG_TU_THEO_THU_TU_LAP = self.get_context('SAP_XEP_CHUNG_TU_THEO_THU_TU_LAP')
        TAI_KHOAN_GIAM_GIA = '5211%%'
        thu_tu = 0
        params = {
            'TU_NGAY':TU_NGAY, 
            'DEN_NGAY':DEN_NGAY, 
            # 'TU_NGAY':'2018-01-01', 
            # 'DEN_NGAY':'2019-01-05', 
            'TAI_KHOAN_IDS':TAI_KHOAN_IDS, 
            'CHI_NHANH_ID': CHI_NHANH_ID, 
            'currency_id':currency_id, 
            'CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU':CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU, 
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'SAP_XEP_CHUNG_TU_THEO_THU_TU_LAP': SAP_XEP_CHUNG_TU_THEO_THU_TU_LAP,
            'TAI_KHOAN_GIAM_GIA': TAI_KHOAN_GIAM_GIA,
            'limit': limit,
            'offset': offset,
            # 'CHI_NHANH_ID' : self.get_chi_nhanh(),
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
                so_ton FLOAT = 0;
                so_ton_oc FLOAT = 0;
                tai_khoan_tmp VARCHAR(200) = '';
                rec record;


                BEGIN

                DROP TABLE IF EXISTS TMP_TAI_KHOAN;
                CREATE TEMP TABLE TMP_TAI_KHOAN
                    AS
                    SELECT
                        "SO_TAI_KHOAN",
                        "TEN_TAI_KHOAN",
                        "TEN_TIENG_ANH",
                        concat("SO_TAI_KHOAN", '%%') AS "SO_TAI_KHOAN_PT",
                        "TINH_CHAT"
                    FROM danh_muc_he_thong_tai_khoan
                    WHERE id IN %(TAI_KHOAN_IDS)s;

                 DROP TABLE IF EXISTS TMP_KET_QUA
                ;
            
                DROP SEQUENCE IF EXISTS TMP_KET_QUA_seq
                ;
            
                CREATE TEMP SEQUENCE TMP_KET_QUA_seq
                ;
            
                DROP TABLE IF EXISTS TMP_KET_QUA
                ;
            
                CREATE TEMP TABLE TMP_KET_QUA (
                    RowNum                  INT DEFAULT NEXTVAL('TMP_KET_QUA_seq')
                        PRIMARY KEY,
                    "ID_CHUNG_TU"           INTEGER,
                    "MODEL_CHUNG_TU"        VARCHAR(200),
                    "NGAY_HACH_TOAN"        DATE,
                    "NGAY_CHUNG_TU"         DATE,
                    "SO_PHIEU_THU"          VARCHAR(200),
                    "SO_PHIEU_CHI"          VARCHAR(200),
                    "LOAI_CHUNG_TU"         VARCHAR(200),
                    "DIEN_GIAI_CHUNG"       VARCHAR(200),
                    "MA_TAI_KHOAN"          VARCHAR(200),
                    "MA_TAI_KHOAN_DOI_UNG"  VARCHAR(200),
                    "TY_GIA"                FLOAT,
                    "GHI_NO"                FLOAT,
                    "GHI_NO_NGUYEN_TE"      FLOAT,
                    "GHI_CO"                FLOAT,
                    "GHI_CO_NGUYEN_TE"      FLOAT,
                    "MA_DOI_TUONG"          VARCHAR(200),
                    "TEN_DOI_TUONG"         VARCHAR(200),
                    "LOAI_HACH_TOAN"        VARCHAR(200),
                    "SO_TON"                FLOAT,
                    "SO_TONOC"              FLOAT,
                    "LOAI_PHIEU"            VARCHAR(200),
                    "LOAI_DAT_HANG"         INTEGER,
                    "NGUOI_NOP_NHAN"        VARCHAR(200),
                    "THU_TU_TRONG_CHUNG_TU" INTEGER
            
            
                )
                ;
            
                INSERT INTO TMP_KET_QUA (
            
                    "ID_CHUNG_TU",
                    "MODEL_CHUNG_TU",
                    "NGAY_HACH_TOAN",
                    "NGAY_CHUNG_TU",
                    "SO_PHIEU_THU",
                    "SO_PHIEU_CHI",
                    "LOAI_CHUNG_TU",
                    "DIEN_GIAI_CHUNG",
                    "MA_TAI_KHOAN",
                    "MA_TAI_KHOAN_DOI_UNG",
                    "TY_GIA",
                    "GHI_NO",
                    "GHI_NO_NGUYEN_TE",
                    "GHI_CO",
                    "GHI_CO_NGUYEN_TE",
                    "MA_DOI_TUONG",
                    "TEN_DOI_TUONG",
                    "LOAI_HACH_TOAN",
                    "SO_TON",
                    "SO_TONOC",
                    "LOAI_PHIEU",
                    "LOAI_DAT_HANG",
                    "NGUOI_NOP_NHAN"
            
            
                )
            
            
                    SELECT
            
                          NULL :: INT       AS "ID_CHUNG_TU"
                        , ''                AS "MODEL_CHUNG_TU"
                        , NULL :: DATE      AS "NGAY_HACH_TOAN"
                        , NULL :: DATE         "NGAY_CHUNG_TU"
                        , ''                AS "SO_PHIEU_THU"
                        , ''                AS "SO_PHIEU_CHI"
                        , ''                AS "LOAI_CHUNG_TU"
                        , 'Số tồn đầu kỳ'   AS "DIEN_GIAI_CHUNG"
                        , OT."SO_TAI_KHOAN" AS "MA_TAI_KHOAN"
                        , ''                AS "MA_TAI_KHOAN_DOI_UNG"
                        , NULL :: FLOAT     AS "TY_GIA"
                        , NULL :: FLOAT     AS "GHI_NO"
                        , NULL :: FLOAT        " AS GHI_NO_NGUYEN_TE"
                        , NULL :: FLOAT     AS "GHI_CO"
                        , NULL :: FLOAT     AS "GHI_CO_NGUYEN_TE"
                        , NULL :: INTEGER   AS "DOI_TUONG_ID"
                        , ''                AS "TEN_DOI_TUONG"
                        , ''                AS "LOAI_HACH_TOAN"
                        , OT.SO_TON
                        , OT.SO_TONOC
                        , '0'               AS "LOAI_PHIEU"
                        , 0                 AS "LOAI_DAT_HANG"
                        , ''
                    FROM (
                             SELECT
                                 AC."SO_TAI_KHOAN"
                                 , AC."TEN_TAI_KHOAN"
                                 , SUM(GL."GHI_NO" - GL."GHI_CO")                     AS SO_TON
                                 , SUM(GL."GHI_NO_NGUYEN_TE" - GL."GHI_CO_NGUYEN_TE") AS SO_TONOC
                             FROM so_cai_chi_tiet AS GL
                                 INNER JOIN LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_chi_nhanh_phu_thuoc) BR
                                     ON BR."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                                 INNER JOIN TMP_TAI_KHOAN AC ON GL."MA_TAI_KHOAN" LIKE AC."SO_TAI_KHOAN_PT"
                             WHERE (GL."NGAY_HACH_TOAN" <= tu_ngay)
                                   AND (ts_currency_id IS NULL
                                        OR GL."currency_id" = ts_currency_id)
                             GROUP BY AC."SO_TAI_KHOAN", AC."TEN_TAI_KHOAN"
                         ) AS OT
                    WHERE OT.SO_TON <> 0
                          OR OT.SO_TONOC <> 0
                ;
            
                IF cong_gop_but_toan = 1
                THEN
                    INSERT INTO TMP_KET_QUA
                    (
            
                        "ID_CHUNG_TU",
                        "MODEL_CHUNG_TU",
                        "NGAY_HACH_TOAN",
                        "NGAY_CHUNG_TU",
                        "SO_PHIEU_THU",
                        "SO_PHIEU_CHI",
                        "LOAI_CHUNG_TU",
                        "DIEN_GIAI_CHUNG",
                        "MA_TAI_KHOAN",
                        "MA_TAI_KHOAN_DOI_UNG",
                        "TY_GIA",
                        "GHI_NO",
                        "GHI_NO_NGUYEN_TE",
                        "GHI_CO",
                        "GHI_CO_NGUYEN_TE",
                        "MA_DOI_TUONG",
                        "TEN_DOI_TUONG",
            
                        "SO_TON",
                        "SO_TONOC",
            
                        "LOAI_DAT_HANG",
                        "NGUOI_NOP_NHAN",
                        "THU_TU_TRONG_CHUNG_TU"
            
                    )
                                SELECT
            
                                    G."ID_CHUNG_TU"
                                    , G."MODEL_CHUNG_TU"
                                    , G."NGAY_HACH_TOAN"
                                    , G."NGAY_CHUNG_TU"
                                    , CASE WHEN G."GHI_NO" <> 0 OR G."GHI_NO_NGUYEN_TE" <> 0
                                    THEN G."SO_CHUNG_TU"
                                      ELSE '' END AS "SO_CHUNG_TU_PHIEU_THU"
                                    , CASE WHEN G."GHI_CO" <> 0 OR G."GHI_CO_NGUYEN_TE" <> 0
                                    THEN G."SO_CHUNG_TU"
                                      ELSE '' END AS "SO_CHUNG_TU_PHIEU_CHI"
                                    , G."LOAI_CHUNG_TU"
                                    , G."DIEN_GIAI_CHUNG"
                                    , G."SO_TAI_KHOAN"
                                    , G."MA_TAI_KHOAN_DOI_UNG"
                                    , G."TY_GIA"
                                    , G."GHI_NO"
                                    , G."GHI_NO_NGUYEN_TE"
                                    , G."GHI_CO"
                                    , G."GHI_CO_NGUYEN_TE"
                                    , G."MA_DOI_TUONG"
                                    , G."TEN_DOI_TUONG"
            
            
                                    , 0           AS "SO_TON"
                                    , 0           AS "SO_TONOC"
            
            
                                    , CASE WHEN "GHI_NO" <> 0 OR "GHI_NO_NGUYEN_TE" <> 0
                                    THEN 1
                                      WHEN "GHI_CO" <> 0 OR "GHI_CO_NGUYEN_TE" <> 0
                                          THEN 2
                                      ELSE 3
                                      END        AS    "LOAI_DAT_HANG"
                                    , G."NGUOI_LIEN_HE"
                                    , G."THU_TU_TRONG_CHUNG_TU"
            
                                FROM (
            
                        SELECT
            
                            GL."ID_CHUNG_TU"
                            , GL."MODEL_CHUNG_TU"
                            , GL."NGAY_HACH_TOAN"
                            , GL."NGAY_CHUNG_TU"
                            ,GL."SO_CHUNG_TU"
            
                            , GL."LOAI_CHUNG_TU"
                            , GL."DIEN_GIAI_CHUNG"
                            , AC."SO_TAI_KHOAN"
                            , GL."MA_TAI_KHOAN_DOI_UNG"
                            , GL."TY_GIA"
                            , SUM(GL."GHI_NO")           AS "GHI_NO"
                            , SUM(GL."GHI_NO_NGUYEN_TE") AS "GHI_NO_NGUYEN_TE"
                            , SUM("GHI_CO")              AS "GHI_CO"
                            , SUM("GHI_CO_NGUYEN_TE")    AS "GHI_CO_NGUYEN_TE"
                            , CASE WHEN GL1.AccountObjectCount > 1
                            THEN NULL
                              ELSE GL."MA_DOI_TUONG"
                              END                        AS "MA_DOI_TUONG"
                            , CASE WHEN GL1.AccountObjectCount > 1
                            THEN NULL
                              ELSE GL."TEN_DOI_TUONG"
                              END                        AS "TEN_DOI_TUONG"
            
            
                            , 0                          AS "SO_TON"
                            , 0                          AS "SO_TONOC"
                            , MIN(GL."THU_TU_TRONG_CHUNG_TU") AS "THU_TU_TRONG_CHUNG_TU"
                            , MIN(GL."LOAI_HACH_TOAN")   AS "LOAI_HACH_TOAN"
                            , MIN(GL."THU_TU_CHI_TIET_GHI_SO") AS "THU_TU_CHI_TIET_GHI_SO"
            
                            , GL."NGUOI_LIEN_HE"
            
                        FROM so_cai_chi_tiet AS GL
                            INNER JOIN LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_chi_nhanh_phu_thuoc) BR
                                ON BR."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                            INNER JOIN TMP_TAI_KHOAN AC ON GL."MA_TAI_KHOAN" LIKE AC."SO_TAI_KHOAN_PT"
                            LEFT JOIN LATERAL ( SELECT COUNT(DISTINCT GL1."DOI_TUONG_ID") AS AccountObjectCount
                                                FROM so_cai_chi_tiet GL1
                                                WHERE GL1."ID_CHUNG_TU" = GL."ID_CHUNG_TU"
                                                      AND GL1."MA_TAI_KHOAN" = GL."MA_TAI_KHOAN"
                                                      AND GL1."MA_TAI_KHOAN_DOI_UNG" = GL."MA_TAI_KHOAN_DOI_UNG"
                                      ) GL1 ON TRUE
                        WHERE GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            
                              AND (GL.currency_id IS NULL
                                   OR GL.currency_id = ts_currency_id
                              )
                        GROUP BY
                            GL."ID_CHUNG_TU",
                            GL."MODEL_CHUNG_TU",
                            GL."NGAY_HACH_TOAN",
                            GL."NGAY_CHUNG_TU",
                            GL."SO_CHUNG_TU",
                            GL."LOAI_CHUNG_TU",
                            GL."DIEN_GIAI_CHUNG",
                            AC."SO_TAI_KHOAN",
                            GL."MA_TAI_KHOAN_DOI_UNG",
            
                            GL."TY_GIA",
            
                            CASE WHEN GL1.AccountObjectCount > 1
                                THEN NULL
                            ELSE GL."MA_DOI_TUONG"
                            END,
                            CASE WHEN GL1.AccountObjectCount > 1
                                THEN NULL
                            ELSE GL."TEN_DOI_TUONG"
                            END,
                            CASE WHEN "GHI_NO" <> 0 OR "GHI_NO_NGUYEN_TE" <> 0
                                THEN 1
                            WHEN "GHI_CO" <> 0 OR "GHI_CO_NGUYEN_TE" <> 0
                                THEN 2
                            ELSE 3
                            END,
                            GL."NGUOI_LIEN_HE"
                        HAVING
                            SUM(GL."GHI_NO") <> 0
                            OR SUM(GL."GHI_NO_NGUYEN_TE") <> 0
                            OR SUM("GHI_CO") <> 0
                            OR SUM("GHI_CO_NGUYEN_TE") <> 0
            
                                ) G
            
                                ORDER BY
                                    "SO_TAI_KHOAN",
                                    "NGAY_HACH_TOAN",
            
                                    "NGAY_CHUNG_TU",
                                    "LOAI_DAT_HANG",
                                    "SO_CHUNG_TU",
                                    "LOAI_HACH_TOAN",
                                    "THU_TU_CHI_TIET_GHI_SO",
                                    "THU_TU_TRONG_CHUNG_TU"
            
                    ;
                ELSE
                    INSERT INTO TMP_KET_QUA
                    (
            
                        "ID_CHUNG_TU",
                        "MODEL_CHUNG_TU",
                        "NGAY_HACH_TOAN",
                        "NGAY_CHUNG_TU",
                        "SO_PHIEU_THU",
                        "SO_PHIEU_CHI",
                        "LOAI_CHUNG_TU",
                        "DIEN_GIAI_CHUNG",
                        "MA_TAI_KHOAN",
                        "MA_TAI_KHOAN_DOI_UNG",
                        "TY_GIA",
                        "GHI_NO",
                        "GHI_NO_NGUYEN_TE",
                        "GHI_CO",
                        "GHI_CO_NGUYEN_TE",
                        "MA_DOI_TUONG",
                        "TEN_DOI_TUONG",
                        "LOAI_HACH_TOAN",
                        "SO_TON",
                        "SO_TONOC",
                        "LOAI_PHIEU",
                        "LOAI_DAT_HANG",
                        "NGUOI_NOP_NHAN",
                        "THU_TU_TRONG_CHUNG_TU"
            
                    )
                        SELECT
            
                             GL."ID_CHUNG_TU"
                            , GL."MODEL_CHUNG_TU"
                            , GL."NGAY_HACH_TOAN"
                            , GL."NGAY_CHUNG_TU"
                            , CASE WHEN GL."GHI_NO" > 0 OR GL."GHI_NO_NGUYEN_TE" > 0
                            THEN GL."SO_CHUNG_TU"
                              ELSE '' END                                                                    AS "SO_CHUNG_TU_PHIEU_THU"
                            , CASE WHEN GL."GHI_CO" > 0 OR GL."GHI_CO_NGUYEN_TE" > 0
                            THEN GL."SO_CHUNG_TU"
                              ELSE '' END                                                                    AS "SO_CHUNG_TU_PHIEU_CHI"
                            , GL."LOAI_CHUNG_TU"
                            ,CASE WHEN GL."DIEN_GIAI" IS NULL
                                                  OR LTRIM(GL."DIEN_GIAI") = ''
                                             THEN GL."DIEN_GIAI_CHUNG"
                                             ELSE GL."DIEN_GIAI"
                                        END AS "DIEN_GIAI_CHUNG"
                            , AC."SO_TAI_KHOAN"
                            , GL."MA_TAI_KHOAN_DOI_UNG"
                            , GL."TY_GIA"
                            , GL."GHI_NO"
                            , GL."GHI_NO_NGUYEN_TE"
                            , GL."GHI_CO"
                            , GL."GHI_CO_NGUYEN_TE"
                            , CASE WHEN GL1.AccountObjectCount > 1
                            THEN NULL
                              ELSE GL."MA_DOI_TUONG"
                              END                                                                            AS "MA_DOI_TUONG"
                            , CASE WHEN GL1.AccountObjectCount > 1
                            THEN NULL
                              ELSE GL."TEN_DOI_TUONG"
                              END                                                                            AS "TEN_DOI_TUONG"
                            , GL."LOAI_HACH_TOAN"
                            , 0                                                                              AS "SO_TON"
                            , 0                                                                              AS "SO_TONOC"
                            , '0'                                                                            AS "LOAI_PHIEU"
                            , CASE WHEN "GHI_NO" <> 0 OR "GHI_NO_NGUYEN_TE" <> 0
                            THEN 1
                              WHEN "GHI_CO" <> 0 OR "GHI_CO_NGUYEN_TE" <> 0
                                  THEN 2
                              ELSE 3
                              END                                                                               "LOAI_DAT_HANG"
                            , GL."NGUOI_LIEN_HE"
                            , GL."THU_TU_TRONG_CHUNG_TU"
                        FROM so_cai_chi_tiet AS GL
                            INNER JOIN LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_chi_nhanh_phu_thuoc) BR
                                ON BR."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                            INNER JOIN TMP_TAI_KHOAN AC ON GL."MA_TAI_KHOAN" LIKE AC."SO_TAI_KHOAN_PT"
                            LEFT JOIN LATERAL ( SELECT COUNT(DISTINCT GL1."DOI_TUONG_ID") AS AccountObjectCount
                                                FROM so_cai_chi_tiet GL1
                                                WHERE GL1."ID_CHUNG_TU" = GL."ID_CHUNG_TU"
                                                      AND GL1."MA_TAI_KHOAN" = GL."MA_TAI_KHOAN"
                                                      AND GL1."MA_TAI_KHOAN_DOI_UNG" = GL."MA_TAI_KHOAN_DOI_UNG"
                                      ) GL1 ON TRUE
                        WHERE GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                              AND (GL.currency_id IS NULL
                                   OR GL.currency_id = ts_currency_id
                              )
                              AND (GL."GHI_CO" <> 0
                                   OR GL."GHI_NO" <> 0
                                   OR GL."GHI_CO_NGUYEN_TE" <> 0
                                   OR GL."GHI_NO_NGUYEN_TE" <> 0
                              )
                            ORDER BY
                                        AC."SO_TAI_KHOAN" ,
                                            "NGAY_HACH_TOAN" ,
            
                                            "NGAY_CHUNG_TU" ,
                                            "LOAI_DAT_HANG" ,
                                            "SO_CHUNG_TU" ,
                                            GL."LOAI_HACH_TOAN" ,
                                            GL."THU_TU_CHI_TIET_GHI_SO" ,
                                            GL."THU_TU_TRONG_CHUNG_TU"
            
                    ;
                END IF
                ;
            
                 DROP TABLE IF EXISTS TMP_KET_QUA_1
                ;
            
                DROP SEQUENCE IF EXISTS TMP_KET_QUA_1_seq
                ;
            
                CREATE TEMP SEQUENCE TMP_KET_QUA_1_seq
                ;
            
                CREATE TEMP TABLE TMP_KET_QUA_1 (
                    RowNum                  INT DEFAULT NEXTVAL('TMP_KET_QUA_1_seq')
                        PRIMARY KEY,
                    "ID_CHUNG_TU"           INTEGER,
                    "MODEL_CHUNG_TU"        VARCHAR(200),
                    "NGAY_HACH_TOAN"        DATE,
                    "NGAY_CHUNG_TU"         DATE,
                    "SO_PHIEU_THU"          VARCHAR(200),
                    "SO_PHIEU_CHI"          VARCHAR(200),
                    "LOAI_CHUNG_TU"         VARCHAR(200),
                    "DIEN_GIAI_CHUNG"       VARCHAR(200),
                    "MA_TAI_KHOAN"          VARCHAR(200),
                    "MA_TAI_KHOAN_DOI_UNG"  VARCHAR(200),
                    "TY_GIA"                FLOAT,
                    "GHI_NO"                FLOAT,
                    "GHI_NO_NGUYEN_TE"      FLOAT,
                    "GHI_CO"                FLOAT,
                    "GHI_CO_NGUYEN_TE"      FLOAT,
                    "MA_DOI_TUONG"          VARCHAR(200),
                    "TEN_DOI_TUONG"         VARCHAR(200),
                    "LOAI_HACH_TOAN"        VARCHAR(200),
                    "SO_TON"                FLOAT,
                    "SO_TONOC"              FLOAT,
                    "LOAI_PHIEU"            VARCHAR(200),
                    "LOAI_DAT_HANG"         INTEGER,
                    "NGUOI_NOP_NHAN"        VARCHAR(200),
                    "THU_TU_TRONG_CHUNG_TU" INTEGER
                )
                ;
            
                INSERT INTO TMP_KET_QUA_1 (
            
                    "ID_CHUNG_TU",
                    "MODEL_CHUNG_TU",
                    "NGAY_HACH_TOAN",
                    "NGAY_CHUNG_TU",
                    "SO_PHIEU_THU",
                    "SO_PHIEU_CHI",
                    "LOAI_CHUNG_TU",
                    "DIEN_GIAI_CHUNG",
                    "MA_TAI_KHOAN",
                    "MA_TAI_KHOAN_DOI_UNG",
                    "TY_GIA",
                    "GHI_NO",
                    "GHI_NO_NGUYEN_TE",
                    "GHI_CO",
                    "GHI_CO_NGUYEN_TE",
                    "MA_DOI_TUONG",
                    "TEN_DOI_TUONG",
                    "LOAI_HACH_TOAN",
                    "SO_TON",
                    "SO_TONOC",
                    "LOAI_PHIEU",
                    "LOAI_DAT_HANG",
                    "NGUOI_NOP_NHAN",
                    "THU_TU_TRONG_CHUNG_TU"
                )
            
                    SELECT
            
                    "ID_CHUNG_TU",
                    "MODEL_CHUNG_TU",
                    "NGAY_HACH_TOAN",
                    "NGAY_CHUNG_TU",
                    "SO_PHIEU_THU",
                    "SO_PHIEU_CHI",
                    "LOAI_CHUNG_TU",
                    "DIEN_GIAI_CHUNG",
                    "MA_TAI_KHOAN",
                    "MA_TAI_KHOAN_DOI_UNG",
                    "TY_GIA",
                    "GHI_NO",
                    "GHI_NO_NGUYEN_TE",
                    "GHI_CO",
                    "GHI_CO_NGUYEN_TE",
                    "MA_DOI_TUONG",
                    "TEN_DOI_TUONG",
                    "LOAI_HACH_TOAN",
                    "SO_TON",
                    "SO_TONOC",
                    "LOAI_PHIEU",
                    "LOAI_DAT_HANG",
                    "NGUOI_NOP_NHAN",
                        "THU_TU_TRONG_CHUNG_TU"
                    FROM TMP_KET_QUA
            
                        ORDER BY  "MA_TAI_KHOAN",
                                    RowNum;
            
            
            
                FOR rec IN
                SELECT *
                FROM TMP_KET_QUA_1
                ORDER BY
                    RowNum
                LOOP
            
                    SELECT CASE WHEN rec."LOAI_DAT_HANG" = 0
                        THEN rec."SO_TONOC"
                           WHEN tai_khoan_tmp <> rec."MA_TAI_KHOAN"
                               THEN rec."GHI_NO_NGUYEN_TE" - rec."GHI_CO_NGUYEN_TE"
                           ELSE so_ton_oc + coalesce(rec."GHI_NO_NGUYEN_TE", 0) - coalesce(rec."GHI_CO_NGUYEN_TE", 0)
                           END
                    INTO so_ton_oc
            
                ;
            
                    rec."SO_TONOC" =so_ton_oc;
            
                    UPDATE TMP_KET_QUA_1
                    SET "SO_TONOC" = rec."SO_TONOC"
                    WHERE RowNum = rec.RowNum
            
                ;
            
                    SELECT CASE WHEN rec."LOAI_DAT_HANG" = 0
                        THEN rec."SO_TON"
                           WHEN tai_khoan_tmp <> rec."MA_TAI_KHOAN"
                               THEN rec."GHI_NO" - rec."GHI_CO"
                           ELSE so_ton + coalesce(rec."GHI_NO", 0) - coalesce(rec."GHI_CO", 0)
                           END
                    INTO so_ton ;
            
                     rec."SO_TON" =so_ton;
            
                    UPDATE TMP_KET_QUA_1
                    SET "SO_TON" =  rec."SO_TON"
                    WHERE RowNum = rec.RowNum
                ;
            
                    tai_khoan_tmp := rec."MA_TAI_KHOAN"
                ;
            
                END LOOP
                ;
            
            
            END $$
            ;
            
            SELECT *
            FROM TMP_KET_QUA_1
            ORDER BY RowNum
            OFFSET %(offset)s
            LIMIT %(limit)s
            ;


        """
        cr.execute(query, params)
        for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
            record.append({
                'NGAY_HACH_TOAN': line.get('NGAY_HACH_TOAN', ''),
                'NGAY_CHUNG_TU': line.get('NGAY_CHUNG_TU', ''),
                'SO_PHIEU_THU': line.get('SO_PHIEU_THU', ''),
                'SO_PHIEU_CHI': line.get('SO_PHIEU_CHI', ''),
                'DIEN_GIAI': line.get('DIEN_GIAI_CHUNG', ''),
                'TAI_KHOAN': line.get('MA_TAI_KHOAN', ''),
                'TK_DOI_UNG': line.get('MA_TAI_KHOAN_DOI_UNG', ''),
                'PS_NO': line.get('GHI_NO', 0),
                'PS_CO': line.get('GHI_CO', 0),
                'SO_TON': line.get('SO_TON', 0),
                'NGUOI_NHAN_NOP': line.get('NGUOI_NOP_NHAN', ''),
                'LOAI_PHIEU': str(line.get('LOAI_PHIEU', 3)),
                'THU_TU': thu_tu,
              
                'MODEL_GOC' : line.get('MODEL_CHUNG_TU'),
                'ID_GOC' : line.get('ID_CHUNG_TU'),
                })
            thu_tu += 1
        
        ############################
        ######### SQL END ##########
        ############################
        SO_TON = 0
        TAI_KHOAN_IDS_tmp = ''
        sorted_record = sorted(record, key=itemgetter('TAI_KHOAN','THU_TU'))
        for r in sorted_record:
            if (r.get('LOAI_PHIEU') == '0'):
                SO_TON = r.get('SO_TON',0)
            elif TAI_KHOAN_IDS_tmp != r.get('TAI_KHOAN'):
                SO_TON = r.get('PS_NO',0) - r.get('PS_CO',0)
            else:
                try:
                    SO_TON = SO_TON + r.get('PS_NO',0) - r.get('PS_CO',0)
                except:
                    pass                
            r['SO_TON'] = SO_TON
            TAI_KHOAN_IDS_tmp = r.get('TAI_KHOAN')

        return sorted_record
    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        currency_id = self.get_context('currency_id')
        TU_NGAY_F = self.get_vntime('TU_NGAY')
        DEN_NGAY_F = self.get_vntime('DEN_NGAY')
        loai_tien = self.env['res.currency'].browse(currency_id).MA_LOAI_TIEN
        param = 'Loại tiền: %s; Từ ngày: %s đến ngày %s' % (loai_tien, TU_NGAY_F, DEN_NGAY_F)
        action = self.env.ref('bao_cao.open_report__so_ke_toan_chi_tiet_quy_tien_mat').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action