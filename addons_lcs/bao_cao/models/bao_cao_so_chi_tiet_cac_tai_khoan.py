# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_SO_CHI_TIET_CAC_TAI_KHOAN(models.Model):
    _name = 'bao.cao.so.chi.tiet.cac.tai.khoan'
    
    
    _auto = False

    THONG_KE_THEO = fields.Selection([('SO_DU_VA_PHAT_SINH', 'Số dư và phát sinh'), ('CHI_CO_PHAT_SINH', ' Chỉ có phát sinh'), ], string='Thống kê theo', help='Thống kê theo', required='True', default='SO_DU_VA_PHAT_SINH')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh', required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI', required='True')
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID', required=True)
    TU = fields.Date(string='Từ ', help='Từ ', required='True', default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến', required='True', default=fields.Datetime.now)
    CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = fields.Boolean(string='Cộng gộp các bút toán giống nhau', help='Cộng gộp các bút toán giống nhau')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hoạch toán', help='Ngày hoạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TAI_KHOAN = fields.Char(string='Tài khoản', help='Tài khoản')
    TK_DOI_UNG = fields.Char(string='TK đối ứng', help='Tài khoản đối ứng')
    PHAT_SINH_NO = fields.Float(string='Phát sinh nợ', help='Phát sinh nợ',digits=decimal_precision.get_precision('VND'))
    PHAT_SINH_NO_SO_TIEN = fields.Float(string='Số tiền', help='Phát sinh nợ số tiền',digits=decimal_precision.get_precision('VND'))
    PHAT_SINH_NO_QUY_DOI = fields.Float(string='Quy đổi', help='Phát sinh nợ quy đổi',digits=decimal_precision.get_precision('VND'))
    PHAT_SINH_CO = fields.Float(string='Phát sinh có', help='Phát sinh có',digits=decimal_precision.get_precision('VND'))
    PHAT_SINH_CO_SO_TIEN = fields.Float(string='Số tiền', help='Phát sinh có số tiền',digits=decimal_precision.get_precision('VND'))
    PHAT_SINH_CO_QUY_DOI = fields.Float(string='Quy đổi', help='Phát sinh có quy đổi',digits=decimal_precision.get_precision('VND'))
    DU_NO = fields.Float(string='Dư nợ', help='Dư nợ',digits=decimal_precision.get_precision('VND'))
    DU_CO = fields.Float(string='Dư có', help='Dư có',digits=decimal_precision.get_precision('VND'))
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    
    TAI_KHOAN_IDS = fields.One2many('danh.muc.he.thong.tai.khoan')
    CHON_TAT_CA_TAI_KHOAN = fields.Boolean('Tất cả tài khoản', default=True)
    TAI_KHOAN_MANY_IDS = fields.Many2many('danh.muc.he.thong.tai.khoan','so_chi_tiet_tk_httk', string='Chọn tài khoản') 

    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')

    @api.onchange('TAI_KHOAN_IDS')
    def _onchange_TAI_KHOAN_IDS(self):
        self.TAI_KHOAN_MANY_IDS =self.TAI_KHOAN_IDS.ids

    @api.onchange('TAI_KHOAN_MANY_IDS')
    def _onchange_TAI_KHOAN_MANY_IDS(self):
        self.TAI_KHOAN_IDS =self.TAI_KHOAN_MANY_IDS.ids
	
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    #FIELD_IDS = fields.One2many('model.name')

    ## START IMPLEMENTING CODE ###
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_SO_CHI_TIET_CAC_TAI_KHOAN, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        loai_tien = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')],limit=1)
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        if loai_tien:
            result['currency_id'] = loai_tien.id
        return result

    # Hàm thay đổi thời gian khi chọn kỳ báo cáo  
    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')

    def _validate(self):
        params = self._context
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        TU = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        
        currency_id = params['currency_id'] if 'currency_id' in params.keys() else 'False'

        CHON_TAT_CA_TAI_KHOAN = params['CHON_TAT_CA_TAI_KHOAN'] if 'CHON_TAT_CA_TAI_KHOAN' in params.keys() else 'False'
        TAI_KHOAN_MANY_IDS = params['TAI_KHOAN_MANY_IDS'] if 'TAI_KHOAN_MANY_IDS' in params.keys() else 'False'

        if(TU=='False'):
            raise ValidationError('<Từ> không được bỏ trống.')
        elif(DEN=='False'):
            raise ValidationError('<Đến> không được bỏ trống.')
        elif(currency_id=='False'):
            raise ValidationError('<Loại tiền> không được bỏ trống.')
        elif(TU > DEN):
            raise ValidationError('<Đến> phải lớn hơn hoặc bằng <Từ>.')

        if CHON_TAT_CA_TAI_KHOAN == 'False':
          if TAI_KHOAN_MANY_IDS == []:
              raise ValidationError('Bạn chưa chọn <Tài khoản>. Xin vui lòng chọn lại.')

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
        CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU = 1 if 'CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU' in params.keys() and params['CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU'] != 'False' else 0
        TU_NGAY = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        currency_id = params['currency_id'] if 'currency_id' in params.keys() and params['currency_id'] != 'False' else None
        
        if params.get('CHON_TAT_CA_TAI_KHOAN'):
          domain = []
          TAI_KHOAN_IDS = self.env['danh.muc.he.thong.tai.khoan'].search(domain).ids
        else:
          TAI_KHOAN_IDS = params.get('TAI_KHOAN_MANY_IDS')
        
        params_sql = {
            'TU_NGAY':TU_NGAY_F, 
            'DEN_NGAY':DEN_NGAY_F, 
            'CHI_NHANH_ID':CHI_NHANH_ID,
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' : BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU' : CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU,
            'currency_id' : currency_id,
            'TAI_KHOAN_IDS' : TAI_KHOAN_IDS or None,
            'limit': limit,
            'offset': offset,
        }


        if THONG_KE_THEO=='SO_DU_VA_PHAT_SINH' :
            return self._lay_bao_cao_so_du_va_phat_sinh(params_sql)
        # Thống kê theo Mặt hàng và khách hàng
        elif THONG_KE_THEO=='CHI_CO_PHAT_SINH' :
            return self._lay_bao_cao_chi_co_phat_sinh(params_sql)  
        
        # Execute SQL query here
    def _lay_bao_cao_so_du_va_phat_sinh(self, params_sql):      
        record = []
        query = """
        --BAO_CAO_SO_CHI_TIET_CAC_TAI_KHOAN
DO LANGUAGE plpgsql $$
DECLARE
    v_tu_ngay                             DATE := %(TU_NGAY)s;

    --tham số từ

    v_den_ngay                            DATE := %(DEN_NGAY)s;

    --tham số đến

    v_bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    --tham số bao gồm số liệu chi nhánh phụ thuộc

    v_chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    --tham số chi nhánh


    v_loai_tien_id                        INTEGER := %(currency_id)s;

    --tham số loại tiền


    v_cong_gop_cac_but_toan_giong_nhau    INTEGER := %(CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU)s;

    --cộng gộp các bút toán giống nhau


    TAI_KHOAN_IDS                         INTEGER := -1;

    --tham số hàng hóa


    rec                                   RECORD;

    PHAN_THAP_PHAN_SO_LUONG               INTEGER;


    LOAI_HINH_KD_0                        VARCHAR(127) := N'Chiết khấu thương mại (bán hàng)';

    LOAI_HINH_KD_1                        VARCHAR(127) := N'Giảm giá hàng bán';

    LOAI_HINH_KD_2                        VARCHAR(127) := N'Trả lại hàng bán';

    LOAI_HINH_KD_3                        VARCHAR(127) := N'Khấu trừ thuế hoạt động sản xuất kinh doanh';

    LOAI_HINH_KD_4                        VARCHAR(127) :=  N'Khấu trừ thuế hoạt động đầu tư';

    IsVietNamese                          INTEGER := 1;

    SO_DU_CUOI_KY_NGOAI_TE_TMP            FLOAT :=0;

    SO_DU_CUOI_KY_TMP                     FLOAT :=0;

    SO_TAI_KHOAN_TMP                      VARCHAR(127) :=N'';


BEGIN
    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(v_chi_nhanh_id, v_bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;

    DROP TABLE IF EXISTS DS_TAI_KHOAN
    ;

    CREATE TEMP TABLE DS_TAI_KHOAN
        AS
            SELECT
                A."SO_TAI_KHOAN"
                , --TAI_KHOAN
                A."TEN_TAI_KHOAN"
                , A."TEN_TIENG_ANH"
                , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                , --TAI_KHOAN
                A."TINH_CHAT"
            FROM danh_muc_he_thong_tai_khoan A --tham số tài khoản
            WHERE (id = any (%(TAI_KHOAN_IDS)s))
    ;

    DROP TABLE IF EXISTS TMP_KET_QUA
            ;
        
            DROP SEQUENCE IF EXISTS TMP_KET_QUA_seq
            ;
        
            CREATE TEMP SEQUENCE TMP_KET_QUA_seq
            ;
        
            CREATE TEMP TABLE TMP_KET_QUA
            (
                RowNum                  INT DEFAULT NEXTVAL('TMP_KET_QUA_seq')
                    PRIMARY KEY,
                KeyID                   VARCHAR(100),
                "ID_CHUNG_TU"           INT,
                "MODEL_CHUNG_TU"        VARCHAR(127),
                "LOAI_CHUNG_TU"         VARCHAR(127),
                "NGAY_HACH_TOAN"        DATE,
                "SO_CHUNG_TU"           VARCHAR(127), --SO_CHUNG_TU
                "NGAY_CHUNG_TU"         DATE, --NGAY_CHUNG_TU
        
                "DIEN_GIAI"             VARCHAR(255),
                "SO_TAI_KHOAN"          VARCHAR(127),
                "TEN_TAI_KHOAN"         VARCHAR(127),
        
                "TINH_CHAT"             VARCHAR(127),
        
        
                "TK_DOI_UNG"            VARCHAR(127),
                "PHAT_SINH_NO_NGUYEN_TE" FLOAT, -- Phát sinh nợ--PHAT_SINH_NO_NGUYEN_TE
                "PHAT_SINH_NO"          FLOAT, --Phát sinh nợ quy đổi--PHAT_SINH_NO
                "PHAT_SINH_CO_NGUYEN_TE" FLOAT, -- Phát sinh Có--PHAT_SINH_CO_NGUYEN_TE
                "PHAT_SINH_CO"          FLOAT, -- Phát sinh Có quy đổi--PHAT_SINH_CO
                "DU_NO_NGUYEN_TE"        FLOAT, --Dư nợ--DU_NO_NGUYEN_TE
                "DU_NO"                 FLOAT, -- Dư nợ quy đổi--DU_NO
                "DU_CO_NGUYEN_TE"        FLOAT, -- Dư có--DU_CO_NGUYEN_TE
                "DU_CO"                 FLOAT, -- Dư có quy đổi--DU_CO
                "OrderType"             INT,
                "MA_THONG_KE_ID"             INT,
                "DOI_TUONG_THCP_ID"             INT,
                "CONG_TRINH_ID"                INT,
                "DON_DAT_HANG_ID"             INT,
                "KHOAN_MUC_CP_ID"             INT,
                "OrderNumber"                INT,
                "SortOrder"             INT,
                "THU_TU_CHI_TIET_GHI_SO"             INT
        
            )
            ;
        
            ----------------------------------
        
        
            DROP TABLE IF EXISTS TMP_KET_QUA_1
            ;
        
            DROP SEQUENCE IF EXISTS TMP_KET_QUA_1_seq
            ;
        
            CREATE TEMP SEQUENCE TMP_KET_QUA_1_seq
            ;
        
            CREATE TEMP TABLE TMP_KET_QUA_1
            (
                RowNum                  INT DEFAULT NEXTVAL('TMP_KET_QUA_1_seq')
                    PRIMARY KEY,
                KeyID                   VARCHAR(100),
                "ID_CHUNG_TU"           INT,
                "MODEL_CHUNG_TU"        VARCHAR(127),
                "LOAI_CHUNG_TU"         VARCHAR(127),
                "NGAY_HACH_TOAN"        DATE, --NGAY_HACH_TOAN
                "SO_CHUNG_TU"           VARCHAR(127), --SO_CHUNG_TU
                "NGAY_CHUNG_TU"         DATE, --NGAY_CHUNG_TU
        
                "DIEN_GIAI"             VARCHAR(255), --DIEN_GIAI
                "SO_TAI_KHOAN"          VARCHAR(127),
                "TEN_TAI_KHOAN"         VARCHAR(127),
                "TINH_CHAT"             VARCHAR(127),
        
                "TK_DOI_UNG"            VARCHAR(127), --TK_DOI_UNG
                "PHAT_SINH_NO_NGUYEN_TE" FLOAT, -- Phát sinh nợ--PHAT_SINH_NO_NGUYEN_TE
                "PHAT_SINH_NO"          FLOAT, --Phát sinh nợ quy đổi--PHAT_SINH_NO
                "PHAT_SINH_CO_NGUYEN_TE" FLOAT, -- Phát sinh Có--PHAT_SINH_CO_NGUYEN_TE
                "PHAT_SINH_CO"          FLOAT, -- Phát sinh Có quy đổi--PHAT_SINH_CO
                "DU_NO_NGUYEN_TE"        FLOAT, --Dư nợ--DU_NO_NGUYEN_TE
                "DU_NO"                 FLOAT, -- Dư nợ quy đổi--DU_NO
                "DU_CO_NGUYEN_TE"        FLOAT, -- Dư có--DU_CO_NGUYEN_TE
                "DU_CO"                 FLOAT, -- Dư có quy đổi--DU_CO
                "OrderType"             INT,
        
                "MA_THONG_KE_ID"             INT,
                "DOI_TUONG_THCP_ID"             INT,
                "CONG_TRINH_ID"                INT,
                "DON_DAT_HANG_ID"             INT,
                "KHOAN_MUC_CP_ID"             INT,
                 "OrderNumber"                INT,
                "SortOrder"             INT,
                "THU_TU_CHI_TIET_GHI_SO"               INT
        
            )
            ;
        
        
            -- Lấy số dư đầu kỳ cho các tài khoản
            INSERT INTO TMP_KET_QUA
            (
                KeyID,
        
                "SO_TAI_KHOAN",
                "TEN_TAI_KHOAN",
                "TINH_CHAT",
                "DIEN_GIAI",
        
        
                "DU_NO_NGUYEN_TE", --Dư nợ--DU_NO_NGUYEN_TE
                "DU_NO", -- Dư nợ quy đổi--DU_NO
                "DU_CO_NGUYEN_TE", -- Dư có--DU_CO_NGUYEN_TE
                "DU_CO", -- Dư có quy đổi--DU_CO
                "OrderType"
            )
                SELECT
                        N'SDDK' || "SO_TAI_KHOAN"
        
                    , "SO_TAI_KHOAN"
                    , --TAI_KHOAN
                    "TEN_TAI_KHOAN"
        
                    , "TINH_CHAT"
                    , N'Số dư đầu kỳ'
        
                    , CASE WHEN "TINH_CHAT" = '0'
                    THEN "SO_TIEN_MO"
                      WHEN "TINH_CHAT" = '1'
                          THEN 0
                      ELSE CASE WHEN "SO_TIEN_MO" > 0
                          THEN "SO_TIEN_MO"
                           ELSE 0
                           END
                      END AS "DU_NO"
                    , --DU_NO
                      CASE WHEN "TINH_CHAT" = '0'
                          THEN "SO_TIEN_MO_NGUYEN_TE"
                      WHEN "TINH_CHAT" = '1'
                          THEN 0
                      ELSE CASE WHEN "SO_TIEN_MO_NGUYEN_TE" > 0
                          THEN "SO_TIEN_MO_NGUYEN_TE"
                           ELSE 0
                           END
                      END AS "DU_NO_NGUYEN_TE"
                    , --DU_NO_NGUYEN_TE
                      CASE WHEN "TINH_CHAT" = '1'
                          THEN -1 * "SO_TIEN_MO"
                      WHEN "TINH_CHAT" = '0'
                          THEN 0
                      ELSE CASE WHEN "SO_TIEN_MO" < 0
                          THEN -1 * "SO_TIEN_MO"
                           ELSE 0
                           END
                      END AS "DU_CO"
                    , --DU_CO
                      CASE WHEN "TINH_CHAT" = '1'
                          THEN -1 * "SO_TIEN_MO_NGUYEN_TE"
                      WHEN "TINH_CHAT" = '0'
                          THEN 0
                      ELSE CASE WHEN "SO_TIEN_MO_NGUYEN_TE" < 0
                          THEN -1 * "SO_TIEN_MO_NGUYEN_TE"
                           ELSE 0
                           END
                      END AS "DU_CO_NGUYEN_TE" --DU_CO_NGUYEN_TE
                    , 0
                FROM (SELECT
                          AC."SO_TAI_KHOAN"
                          , --TAI_KHOAN
                          AC."TEN_TAI_KHOAN"
        
                          , --TAI_KHOAN
                          AC."TINH_CHAT"
                          , SUM(GL."GHI_NO" - GL."GHI_CO") AS "SO_TIEN_MO"
                          , --PHAT_SINH_NO
                            SUM(GL."GHI_NO_NGUYEN_TE" -
                                GL."GHI_CO_NGUYEN_TE")     AS "SO_TIEN_MO_NGUYEN_TE" --PHAT_SINH_NO_NGUYEN_TE
                      FROM so_cai_chi_tiet AS GL
                          INNER JOIN DS_TAI_KHOAN AC ON GL."MA_TAI_KHOAN" LIKE AC."AccountNumberPercent"
                          --#tblTAI_KHOAN
                          INNER JOIN TMP_LIST_BRAND OU ON GL."CHI_NHANH_ID" = OU."CHI_NHANH_ID"
                      WHERE (GL."NGAY_HACH_TOAN" < v_tu_ngay)--NGAY_HACH_TOAN
        
                            AND (v_loai_tien_id IS NULL
                                 OR GL."currency_id" = v_loai_tien_id
                            )
                      GROUP BY
                          AC."SO_TAI_KHOAN", --TAI_KHOAN
                          AC."TEN_TAI_KHOAN",
                          AC."TEN_TIENG_ANH",
                          AC."TINH_CHAT"
                     ) AS OT
                WHERE OT."SO_TIEN_MO" <> 0
                      OR OT."SO_TIEN_MO_NGUYEN_TE" <> 0
            ;
        
        
            --Lấy dữ liệu trong kỳ
            IF v_cong_gop_cac_but_toan_giong_nhau = 0  -- Không cộng gộp dl
            THEN
                INSERT INTO TMP_KET_QUA
                (KeyID,
                 "ID_CHUNG_TU",
                 "MODEL_CHUNG_TU",
                 "LOAI_CHUNG_TU",
                 "NGAY_HACH_TOAN", --NGAY_HACH_TOAN
                 "SO_CHUNG_TU", --SO_CHUNG_TU
                 "NGAY_CHUNG_TU", --NGAY_CHUNG_TU
        
                 "DIEN_GIAI", --DIEN_GIAI
                 "SO_TAI_KHOAN",
                 "TEN_TAI_KHOAN",
                 "TINH_CHAT",
        
                 "TK_DOI_UNG", --TK_DOI_UNG
                 "PHAT_SINH_NO_NGUYEN_TE", -- Phát sinh nợ--PHAT_SINH_NO_NGUYEN_TE
                 "PHAT_SINH_NO", --Phát sinh nợ quy đổi--PHAT_SINH_NO
                 "PHAT_SINH_CO_NGUYEN_TE", -- Phát sinh Có--PHAT_SINH_CO_NGUYEN_TE
                 "PHAT_SINH_CO", -- Phát sinh Có quy đổi--PHAT_SINH_CO
                 "DU_NO_NGUYEN_TE", --Dư nợ--DU_NO_NGUYEN_TE
                 "DU_NO", -- Dư nợ quy đổi--DU_NO
                 "DU_CO_NGUYEN_TE", -- Dư có--DU_CO_NGUYEN_TE
                 "DU_CO", -- Dư có quy đổi--DU_CO
                 "OrderType",
        
                "MA_THONG_KE_ID"             ,
                "DOI_TUONG_THCP_ID"             ,
                "CONG_TRINH_ID"                ,
                "DON_DAT_HANG_ID"             ,
                "KHOAN_MUC_CP_ID" ,
                "OrderNumber"              ,
                "SortOrder",
                "THU_TU_CHI_TIET_GHI_SO"
        
                )
                    SELECT
                          CAST(GL."id" AS VARCHAR(255)) || '-' || AC."SO_TAI_KHOAN" AS KeyID
                        , --( KeyID ,--TAI_KHOAN
                          GL."ID_CHUNG_TU"                                         AS "ID_CHUNG_TU"
                        , GL."MODEL_CHUNG_TU"                                      AS "MODEL_CHUNG_TU"
                        , --  "ID_CHUNG_TU" ,
                          GL."LOAI_CHUNG_TU"                                       AS "LOAI_CHUNG_TU"
                        , --  "LOAI_CHUNG_TU" ,
                          GL."NGAY_HACH_TOAN"                                      AS "NGAY_HACH_TOAN"
                        , --  "NGAY_HACH_TOAN" ,--NGAY_HACH_TOAN
                          GL."SO_CHUNG_TU"                                         AS "SO_CHUNG_TU"
                        , --  "SO_CHUNG_TU" ,--SO_CHUNG_TU
                          GL."NGAY_CHUNG_TU"                                       AS "NGAY_CHUNG_TU"
        
                        , GL."DIEN_GIAI"                                           AS "DIEN_GIAI"
                        , --  "DIEN_GIAI" ,--DIEN_GIAI
                          AC."SO_TAI_KHOAN"                                        AS "SO_TAI_KHOAN"
                        , --  "TAI_KHOAN" ,--TAI_KHOAN
                          AC."TEN_TAI_KHOAN"                                       AS "TEN_TAI_KHOAN"
        
                        , AC."TINH_CHAT"                                           AS "TINH_CHAT"
                        --  "TEN_TAI_KHOAN" ,
                        , GL."MA_TAI_KHOAN_DOI_UNG"                                AS "MA_TAI_KHOAN_DOI_UNG"
                        --  "TK_DOI_UNG" ,--TK_DOI_UNG
        
                        , --  "TINH_CHAT" ,
                          GL."GHI_NO"                                              AS "PHAT_SINH_NO"
                        , --  "PHAT_SINH_NO" , -- Phát sinh nợ--PHAT_SINH_NO
                          GL."GHI_NO_NGUYEN_TE"                                    AS "PHAT_SINH_NO_NGUYEN_TE"
                        , --  "PHAT_SINH_NO_NGUYEN_TE" , -- Phát sinh nợ quy đổi--PHAT_SINH_NO_NGUYEN_TE
                          GL."GHI_CO"                                              AS "PHAT_SINH_CO"
                        , --  "PHAT_SINH_CO" , -- Phát sinh có--PHAT_SINH_CO
                          GL."GHI_CO_NGUYEN_TE"                                    AS "PHAT_SINH_CO_NGUYEN_TE"
        
        
                        , --  "DU_NO" , -- Dư Nợ--DU_NO,
                          COALESCE(R."DU_NO_NGUYEN_TE", 0)                          AS "DU_NO_NGUYEN_TE"
                        , --  "PHAT_SINH_CO_NGUYEN_TE" , -- Phát sinh có quy đổi--PHAT_SINH_CO_NGUYEN_TE
                          COALESCE(R."DU_NO", 0)                                   AS "DU_NO"
        
                        , COALESCE(R."DU_CO_NGUYEN_TE",
                                   0)                                              AS "DU_CO_NGUYEN_TE"
                        --  "DU_CO_NGUYEN_TE" , -- Dư Có quy đ
                        , --  "DU_NO_NGUYEN_TE" , -- Dư Nợ quy đổi--DU_NO_NGUYEN_TE,
                          COALESCE(R."DU_CO", 0)                                   AS "DU_CO"
        
        
                        , 1
                        ,GL."MA_THONG_KE_ID"
                        ,GL."DOI_TUONG_THCP_ID"
                        ,GL."CONG_TRINH_ID"
                        ,GL."DON_DAT_HANG_ID"
                        ,GL."KHOAN_MUC_CP_ID"
                        , CASE WHEN ((GL."MA_TAI_KHOAN" LIKE N'11%%' OR GL."MA_TAI_KHOAN" LIKE N'15%%' AND gl."MA_TAI_KHOAN" NOT LIKE N'154%%')
                                        AND GL."GHI_NO" <> 0) THEN 0 ELSE 1 END AS "OrderNumber"
        
                         ,GL."THU_TU_TRONG_CHUNG_TU"
                        ,GL."THU_TU_CHI_TIET_GHI_SO"
        
        
        
                    FROM so_cai_chi_tiet AS GL
                        LEFT JOIN TMP_KET_QUA AS R ON (GL."MA_TAI_KHOAN" = R."SO_TAI_KHOAN"--TAI_KHOAN
                                                       AND R.KeyID = N'SDDK'
                                                                     || GL."MA_TAI_KHOAN"--TAI_KHOAN
                            )
                        INNER JOIN DS_TAI_KHOAN AC ON GL."MA_TAI_KHOAN" LIKE AC."AccountNumberPercent"
        
                        INNER JOIN TMP_LIST_BRAND OU ON GL."CHI_NHANH_ID" = OU."CHI_NHANH_ID"
                        LEFT JOIN danh_muc_to_chuc AS OU2 ON GL."DVT_ID" = OU2."id"
        
                    WHERE GL."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay--NGAY_HACH_TOAN
        
                          AND (GL."GHI_NO_NGUYEN_TE" <> 0--PHAT_SINH_NO_NGUYEN_TE
                               OR GL."GHI_CO_NGUYEN_TE" <> 0--PHAT_SINH_CO_NGUYEN_TE
                               OR GL."GHI_NO" <> 0--PHAT_SINH_NO
                               OR GL."GHI_CO" <> 0--PHAT_SINH_CO
                          )
                          AND (v_loai_tien_id IS NULL
                               OR GL."currency_id" = v_loai_tien_id
                          )
                ;
        
        
            ELSE --Cộng gộp các bút toán giống nhau
                INSERT INTO TMP_KET_QUA
                (KeyID,
                 "ID_CHUNG_TU",
                 "MODEL_CHUNG_TU",
                 "LOAI_CHUNG_TU",
                 "NGAY_HACH_TOAN", --NGAY_HACH_TOAN
                 "SO_CHUNG_TU", --SO_CHUNG_TU
                 "NGAY_CHUNG_TU", --NGAY_CHUNG_TU
        
                 "DIEN_GIAI", --DIEN_GIAI
        
                 "SO_TAI_KHOAN",
                 "TEN_TAI_KHOAN", --TEN_TAI_KHOAN,
                 "TK_DOI_UNG", --TK_DOI_UNG
                 "TINH_CHAT",
                 "PHAT_SINH_NO", --PHAT_SINH_NO
                 "PHAT_SINH_NO_NGUYEN_TE", --PHAT_SINH_NO_NGUYEN_TE
                 "PHAT_SINH_CO", --PHAT_SINH_CO
                 "PHAT_SINH_CO_NGUYEN_TE", --PHAT_SINH_CO_NGUYEN_TE
                 "DU_NO", -- Dư Nợ--DU_NO
                 "DU_NO_NGUYEN_TE", -- Dư Nợ quy đổi--DU_NO_NGUYEN_TE
                 "DU_CO", -- Dư Có--DU_CO
                 "DU_CO_NGUYEN_TE", -- Dư Có quy đổi --DU_CO_NGUYEN_TE
                 "OrderType",
                    "OrderNumber",
               -- "SortOrder"
                "THU_TU_CHI_TIET_GHI_SO"
        
                )
                    SELECT
                        RSNS.KeyID
                        , RSNS."ID_CHUNG_TU"
                        , RSNS."MODEL_CHUNG_TU"
                        , RSNS."LOAI_CHUNG_TU"
                        , RSNS."NGAY_HACH_TOAN"
                        , --NGAY_HACH_TOAN
                        RSNS."SO_CHUNG_TU"
                        , --SO_CHUNG_TU
                        RSNS."NGAY_CHUNG_TU"
                        , --NGAY_CHUNG_TU
        
                        RSNS."DIEN_GIAI"
                        , --DIEN_GIAI
                        RSNS."SO_TAI_KHOAN"
                        , --TAI_KHOAN
                        RSNS."TEN_TAI_KHOAN"
                        , RSNS."TK_DOI_UNG"
                        , --TK_DOI_UNG
                        RSNS."TINH_CHAT"
                        , RSNS."PHAT_SINH_NO"
                        , --PHAT_SINH_NO
                        RSNS."PHAT_SINH_NO_NGUYEN_TE"
                        , --PHAT_SINH_NO_NGUYEN_TE
                        RSNS."PHAT_SINH_CO"
                        , --PHAT_SINH_CO
                        RSNS."PHAT_SINH_CO_NGUYEN_TE"
                        , --PHAT_SINH_CO_NGUYEN_TE
                        RSNS."DU_NO"
                        , -- Dư Nợ--DU_NO
                        RSNS."DU_NO_NGUYEN_TE"
                        , -- Dư Nợ quy đổi--DU_NO_NGUYEN_TE
                        RSNS."DU_CO"
                        , -- Dư Có--DU_CO
                        RSNS."DU_CO_NGUYEN_TE"
        
                        ,1 AS "OrderType"
                          ,RSNS."OrderNumber"
                        ,"THU_TU_CHI_TIET_GHI_SO"
        
        
                    FROM (SELECT
                                CAST(MAX(GL."id") AS VARCHAR(255))
                                || '-' || AC."SO_TAI_KHOAN"     AS KeyID
                              , --TAI_KHOAN
                                GL."MODEL_CHUNG_TU"             AS "MODEL_CHUNG_TU"
                              , GL."ID_CHUNG_TU"                AS "ID_CHUNG_TU"
                              , GL."LOAI_CHUNG_TU"              AS "LOAI_CHUNG_TU"
                              , GL."NGAY_HACH_TOAN"             AS "NGAY_HACH_TOAN"
                              , --NGAY_HACH_TOAN
                                GL."SO_CHUNG_TU"                AS "SO_CHUNG_TU"
                              , --SO_CHUNG_TU
                                GL."NGAY_CHUNG_TU"              AS "NGAY_CHUNG_TU"
                              , --NGAY_CHUNG_TU
        
                                GL."DIEN_GIAI_CHUNG"            AS "DIEN_GIAI"
                              , --DIEN_GIAI
                                AC."SO_TAI_KHOAN"               AS "SO_TAI_KHOAN"
                              , --TAI_KHOAN
                                AC."TEN_TAI_KHOAN"              AS "TEN_TAI_KHOAN"
                              , GL."MA_TAI_KHOAN_DOI_UNG"       AS "TK_DOI_UNG"
                              , --TK_DOI_UNG
                                AC."TINH_CHAT"                  AS "TINH_CHAT"
                              , SUM(GL."GHI_NO")                AS "PHAT_SINH_NO"
                              , --PHAT_SINH_NO)
                                SUM(GL."GHI_NO_NGUYEN_TE")      AS "PHAT_SINH_NO_NGUYEN_TE"
                              , --PHAT_SINH_NO_NGUYEN_TE)
                                SUM(GL."GHI_CO")                AS "PHAT_SINH_CO"
                              , --PHAT_SINH_CO)
                                SUM(GL."GHI_CO_NGUYEN_TE")      AS "PHAT_SINH_CO_NGUYEN_TE"
                              , --PHAT_SINH_CO_NGUYEN_TE)
                                COALESCE(R."DU_NO", 0)          AS "DU_NO"
                              , --DU_NO,
                                COALESCE(R."DU_NO_NGUYEN_TE", 0) AS "DU_NO_NGUYEN_TE"
                              , --DU_NO_NGUYEN_TE,
                                COALESCE(R."DU_CO", 0)          AS "DU_CO"
                              , --DU_CO,
                                COALESCE(R."DU_CO_NGUYEN_TE", 0) AS "DU_CO_NGUYEN_TE" --DU_CO_NGUYEN_TE,
                              , CASE WHEN (AC."SO_TAI_KHOAN" LIKE N'11%%' OR AC."SO_TAI_KHOAN" LIKE N'15%%' AND AC."SO_TAI_KHOAN" NOT LIKE N'154%%')
                                        AND SUM(GL."GHI_NO") <> 0 THEN 0 ELSE 1 END AS "OrderNumber"
                              ,GL."THU_TU_CHI_TIET_GHI_SO"
        
                          FROM so_cai_chi_tiet AS GL
                              LEFT JOIN TMP_KET_QUA AS R ON (GL."MA_TAI_KHOAN" = R."SO_TAI_KHOAN"--TAI_KHOAN
                                                             AND R.KeyID = N'SDDK'
                                                                           || GL."MA_TAI_KHOAN"--TAI_KHOAN
                                  )
                              INNER JOIN DS_TAI_KHOAN AC ON GL."MA_TAI_KHOAN" LIKE AC."AccountNumberPercent"
                              --#tblTAI_KHOAN
                              INNER JOIN TMP_LIST_BRAND OU ON GL."CHI_NHANH_ID" = OU."CHI_NHANH_ID"
                              LEFT JOIN danh_muc_to_chuc AS OU2 ON GL."DVT_ID" = OU2."id"
        
                          WHERE (GL."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay)--NGAY_HACH_TOAN
        
                                AND (v_loai_tien_id IS NULL
                                     OR GL."currency_id" = v_loai_tien_id
                                )
                          GROUP BY GL."ID_CHUNG_TU",
                              GL."MODEL_CHUNG_TU",
                              GL."LOAI_CHUNG_TU",
                              GL."NGAY_HACH_TOAN", --NGAY_HACH_TOAN
                              GL."SO_CHUNG_TU", --SO_CHUNG_TU
                              GL."NGAY_CHUNG_TU", --NGAY_CHUNG_TU
        
                              GL."DIEN_GIAI_CHUNG", --DIEN_GIAI
                              AC."SO_TAI_KHOAN", --TAI_KHOAN
                              AC."TEN_TAI_KHOAN",
        
                              GL."MA_TAI_KHOAN_DOI_UNG", --TK_DOI_UNG
                              AC."TINH_CHAT",
        
        
                              R."DU_NO", --DU_NO
                              R."DU_NO_NGUYEN_TE", --DU_NO_NGUYEN_TE
                              R."DU_CO", --DU_CO
                              R."DU_CO_NGUYEN_TE", --DU_CO_NGUYEN_TE
                               GL."THU_TU_CHI_TIET_GHI_SO"
        
                          HAVING SUM(GL."GHI_NO_NGUYEN_TE") <> 0--PHAT_SINH_NO_NGUYEN_TE)
                                 OR SUM(GL."GHI_CO_NGUYEN_TE") <> 0--PHAT_SINH_CO_NGUYEN_TE)
                                 OR SUM(GL."GHI_NO") <> 0--PHAT_SINH_NO)
                                 OR SUM(GL."GHI_CO") <> 0--PHAT_SINH_CO)
                         ) AS RSNS
                    GROUP BY
                        RSNS.KeyID,
                        RSNS."ID_CHUNG_TU",
                        RSNS."MODEL_CHUNG_TU",
                        RSNS."LOAI_CHUNG_TU",
                        RSNS."NGAY_HACH_TOAN", --NGAY_HACH_TOAN
                        RSNS."SO_CHUNG_TU", --SO_CHUNG_TU
                        RSNS."NGAY_CHUNG_TU", --NGAY_CHUNG_TU
        
                        RSNS."DIEN_GIAI", --DIEN_GIAI
        
                        RSNS."SO_TAI_KHOAN",
                        RSNS."TEN_TAI_KHOAN", --TEN_TAI_KHOAN,
                        RSNS."TK_DOI_UNG", --TK_DOI_UNG
                        RSNS."TINH_CHAT",
                        RSNS."PHAT_SINH_NO", --PHAT_SINH_NO
                        RSNS."PHAT_SINH_NO_NGUYEN_TE", --PHAT_SINH_NO_NGUYEN_TE
                        RSNS."PHAT_SINH_CO", --PHAT_SINH_CO
                        RSNS."PHAT_SINH_CO_NGUYEN_TE", --PHAT_SINH_CO_NGUYEN_TE
                        RSNS."DU_NO", -- Dư Nợ--DU_NO
                        RSNS."DU_NO_NGUYEN_TE", -- Dư Nợ quy đổi--DU_NO_NGUYEN_TE
                        RSNS."DU_CO", -- Dư Có--DU_CO
                        RSNS."DU_CO_NGUYEN_TE",  -- Dư Có quy đổi --DU_CO_NGUYEN_TE
                         RSNS."OrderNumber",
                           RSNS."THU_TU_CHI_TIET_GHI_SO"
                ;
            END IF
            ;
        
                -- Thêm dòng tổng cộng
                INSERT INTO TMP_KET_QUA
                (KeyID,
                 "SO_TAI_KHOAN", --TAI_KHOAN
                 "TEN_TAI_KHOAN",
        
                 "TINH_CHAT",
                 "DIEN_GIAI", --DIEN_GIAI
        
                 "PHAT_SINH_NO", --PHAT_SINH_NO
                 "PHAT_SINH_NO_NGUYEN_TE", --PHAT_SINH_NO_NGUYEN_TE
                 "PHAT_SINH_CO", --PHAT_SINH_CO
                 "PHAT_SINH_CO_NGUYEN_TE", --PHAT_SINH_CO_NGUYEN_TE
                 "OrderType"
        
                )
                    SELECT
                            N'TC' || "SO_TAI_KHOAN"
                        , --TAI_KHOAN
        
                        "SO_TAI_KHOAN"
                        , "TEN_TAI_KHOAN"
                        , "TINH_CHAT"
                        , N'Cộng'
                        , SUM("PHAT_SINH_NO")
                        , --SUM(PHAT_SINH_NO)
                        SUM("PHAT_SINH_NO_NGUYEN_TE")
                        , --SUM(PHAT_SINH_NO_NGUYEN_TE)
                        SUM("PHAT_SINH_CO")
                        , --SUM(PHAT_SINH_CO)
                        SUM("PHAT_SINH_CO_NGUYEN_TE")
                        , --SUM(PHAT_SINH_CO_NGUYEN_TE)
                        2
                    FROM TMP_KET_QUA
                    WHERE "OrderType" = 1
                    GROUP BY
        
                        "SO_TAI_KHOAN",
                        "TEN_TAI_KHOAN", --TEN_TAI_KHOAN,
                        "TINH_CHAT"
                ;
        
                -- Thêm dòng Số dư cuối kỳ
        
                INSERT INTO TMP_KET_QUA
                (KeyID,
        
                 "SO_TAI_KHOAN",
                 "TEN_TAI_KHOAN", --TEN_TAI_KHOAN,
                 "TINH_CHAT",
                 "DIEN_GIAI", --DIEN_GIAI
        
                 "DU_NO", -- Dư Nợ--DU_NO
                 "DU_NO_NGUYEN_TE", -- Dư Nợ quy đổi--DU_NO_NGUYEN_TE
                 "DU_CO", -- Dư Có--DU_CO
                 "DU_CO_NGUYEN_TE", -- Dư Có quy đổi --DU_CO_NGUYEN_TE
                 "OrderType"
                )
                    SELECT
                            N'SDCK' || "SO_TAI_KHOAN"
                        , --TAI_KHOAN
        
                        "SO_TAI_KHOAN"
                        , "TEN_TAI_KHOAN"
                        , --TEN_TAI_KHOAN,
                        "TINH_CHAT"
                        , N'Số dư cuối kỳ'
                        , CASE WHEN "TINH_CHAT" = '0'
                        THEN "SO_DU_CUOI_KY"
                          WHEN "TINH_CHAT" = '1'
                              THEN 0
                          ELSE CASE WHEN "SO_DU_CUOI_KY" > 0
                              THEN "SO_DU_CUOI_KY"
                               ELSE 0
                               END
                          END AS "DebitBalance"
                        , CASE WHEN "TINH_CHAT" = '0'
                        THEN "SO_DU_CUOI_KY_NGOAI_TE"
                          WHEN "TINH_CHAT" = '1'
                              THEN 0
                          ELSE CASE WHEN "SO_DU_CUOI_KY_NGOAI_TE" > 0
                              THEN "SO_DU_CUOI_KY_NGOAI_TE"
                               ELSE 0
                               END
                          END AS "DebitBalanceOC"
                        , CASE WHEN "TINH_CHAT" = '1'
                        THEN -1 * "SO_DU_CUOI_KY"
                          WHEN "TINH_CHAT" = '0'
                              THEN 0
                          ELSE CASE WHEN "SO_DU_CUOI_KY" < 0
                              THEN -1 * "SO_DU_CUOI_KY"
                               ELSE 0
                               END
                          END AS "CreditBalance"
                        , CASE WHEN "TINH_CHAT" = '1'
                        THEN -1 * "SO_DU_CUOI_KY_NGOAI_TE"
                          WHEN "TINH_CHAT" = '0'
                              THEN 0
                          ELSE CASE WHEN "SO_DU_CUOI_KY_NGOAI_TE" < 0
                              THEN -1 * "SO_DU_CUOI_KY_NGOAI_TE"
                               ELSE 0
                               END
                          END AS "CreditBalanceOC"
                        , 3
        
        
                    FROM (SELECT
                              "SO_TAI_KHOAN"
                              ,
        
                              "TEN_TAI_KHOAN"
                              , --TEN_TAI_KHOAN,
                              "TINH_CHAT"
                              , (COALESCE(SUM("DU_NO"--COALESCE(SUM(DU_NO
                                              - "DU_CO"), 0)--DU_CO),
                                 + COALESCE(SUM("PHAT_SINH_NO" - "PHAT_SINH_CO"), --COALESCE(SUM(PHAT_SINH_NO
                                            0)) AS "SO_DU_CUOI_KY"
                              , (COALESCE(SUM("DU_NO_NGUYEN_TE"--COALESCE(SUM(DU_NO_NGUYEN_TE
                                              - "DU_CO_NGUYEN_TE"), 0)--DU_CO_NGUYEN_TE),
                                 + COALESCE(SUM("PHAT_SINH_NO_NGUYEN_TE"--COALESCE(SUM(PHAT_SINH_NO_NGUYEN_TE
                                                - "PHAT_SINH_CO_NGUYEN_TE"),
                                            0)) AS "SO_DU_CUOI_KY_NGOAI_TE" --PHAT_SINH_CO_NGUYEN_TE),
                          FROM TMP_KET_QUA
                          WHERE "OrderType" IN ('0', '2')
                          GROUP BY
                              "SO_TAI_KHOAN", --TAI_KHOAN
        
                              "TEN_TAI_KHOAN", --TEN_TAI_KHOAN,
                              "TINH_CHAT"
                         ) OT
                ;
        
        
                /*Thêm đoạn này by hoant 22.04.2015 do là các bạn làm trước đã inser theo kiểu ko thể sort để cộng đuổi nên phải chế ra đoạn này*/
                INSERT INTO TMP_KET_QUA_1
                (KeyID,
                 "ID_CHUNG_TU",
                 "MODEL_CHUNG_TU",
                 "LOAI_CHUNG_TU",
                 "NGAY_HACH_TOAN", --NGAY_HACH_TOAN
                 "SO_CHUNG_TU", --SO_CHUNG_TU
                 "NGAY_CHUNG_TU", --NGAY_CHUNG_TU
        
                 "DIEN_GIAI", --DIEN_GIAI
                 "SO_TAI_KHOAN", --TAI_KHOAN
                 "TINH_CHAT",
        
                 "TEN_TAI_KHOAN", --TEN_TAI_KHOAN,
                 "TK_DOI_UNG", --TK_DOI_UNG
                 "PHAT_SINH_NO_NGUYEN_TE", --PHAT_SINH_NO_NGUYEN_TE
                 "PHAT_SINH_NO", --PHAT_SINH_NO
                 "PHAT_SINH_CO_NGUYEN_TE", --PHAT_SINH_CO_NGUYEN_TE
                 "PHAT_SINH_CO", --PHAT_SINH_CO
                 "DU_NO_NGUYEN_TE", --DU_NO_NGUYEN_TE
                 "DU_NO", --DU_NO
                 "DU_CO_NGUYEN_TE", --DU_CO_NGUYEN_TE
                 "DU_CO", --DU_CO
                 "OrderType",
                 "MA_THONG_KE_ID"             ,
                "DOI_TUONG_THCP_ID"             ,
                "CONG_TRINH_ID"                ,
                "DON_DAT_HANG_ID"             ,
                "KHOAN_MUC_CP_ID",
                "OrderNumber"             ,
                "SortOrder",
                     "THU_TU_CHI_TIET_GHI_SO"
        
                )
                    SELECT
                        KeyID
                        , "ID_CHUNG_TU"
                        , "MODEL_CHUNG_TU"
                        , "LOAI_CHUNG_TU"
                        , "NGAY_HACH_TOAN"
                        , --NGAY_HACH_TOAN
                        "SO_CHUNG_TU"
                        , --SO_CHUNG_TU
                        "NGAY_CHUNG_TU"
                        , --NGAY_CHUNG_TU
        
                        "DIEN_GIAI"
                        , --DIEN_GIAI
                        "SO_TAI_KHOAN"
                        , --TAI_KHOAN
                        "TINH_CHAT"
                        , "TEN_TAI_KHOAN"
                        , --TEN_TAI_KHOAN,
                        "TK_DOI_UNG"
                        , --TK_DOI_UNG
                        "PHAT_SINH_NO_NGUYEN_TE"
                        , --PHAT_SINH_NO_NGUYEN_TE
                        "PHAT_SINH_NO"
                        , --PHAT_SINH_NO
                        "PHAT_SINH_CO_NGUYEN_TE"
                        , --PHAT_SINH_CO_NGUYEN_TE
                        "PHAT_SINH_CO"
                        , --PHAT_SINH_CO
                        "DU_NO_NGUYEN_TE"
                        , --DU_NO_NGUYEN_TE
                        "DU_NO"
                        , --DU_NO
                        "DU_CO_NGUYEN_TE"
                        , --DU_CO_NGUYEN_TE
                        "DU_CO"
                        --DU_CO
                        ,"OrderType"
                         ,"MA_THONG_KE_ID"
                        ,"DOI_TUONG_THCP_ID"
                        ,"CONG_TRINH_ID"
                        ,"DON_DAT_HANG_ID"
                        ,"KHOAN_MUC_CP_ID"
                        ,"OrderNumber"
                        ,"SortOrder"
                        ,"THU_TU_CHI_TIET_GHI_SO"
        
        
                    FROM TMP_KET_QUA
                    ORDER BY
                        "SO_TAI_KHOAN", --TAI_KHOAN
                        "OrderType",
                        "NGAY_HACH_TOAN", --NGAY_HACH_TOAN
                        "NGAY_CHUNG_TU", --NGAY_CHUNG_TU
                          "OrderNumber",
                        "SO_CHUNG_TU",--SO_CHUNG_TU
        
                        "SortOrder",
                         "THU_TU_CHI_TIET_GHI_SO",
                        "TK_DOI_UNG"
        
                ;
        
        --      DELETE FROM   TMP_KET_QUA_1 WHERE "SO_CHUNG_TU" <> 'PT00001'    ;
        
                FOR rec IN
                SELECT *
                FROM TMP_KET_QUA_1
                     WHERE  "OrderType" <> 3
                                 AND "OrderType" <> 2
                ORDER BY
                    RowNum
                LOOP
                    SELECT (CASE WHEN rec."OrderType" = 0
                        THEN (CASE WHEN rec."DU_NO_NGUYEN_TE" = 0 --DU_NO_NGUYEN_TE
                            THEN rec."DU_CO_NGUYEN_TE" --DU_CO_NGUYEN_TE
                              ELSE -1
                                   * rec."DU_NO_NGUYEN_TE" --DU_NO_NGUYEN_TE
                              END)
                            WHEN SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN" --@TAI_KHOAN_tmp
                                THEN rec."PHAT_SINH_CO_NGUYEN_TE" - rec."PHAT_SINH_NO_NGUYEN_TE" --PHAT_SINH_CO_NGUYEN_TE
                            ELSE SO_DU_CUOI_KY_NGOAI_TE_TMP + rec."PHAT_SINH_CO_NGUYEN_TE"--PHAT_SINH_CO_NGUYEN_TE
                                 - rec."PHAT_SINH_NO_NGUYEN_TE" --PHAT_SINH_NO_NGUYEN_TE
                            END)
                    INTO SO_DU_CUOI_KY_NGOAI_TE_TMP
        
                ;
                    rec."DU_NO_NGUYEN_TE" = ( CASE WHEN  rec."TINH_CHAT" = '0'--DU_NO_NGUYEN_TE
                                                      THEN -1 * SO_DU_CUOI_KY_NGOAI_TE_TMP
                                                      WHEN  rec."TINH_CHAT" = '1'
                                                      THEN 0
                                                      ELSE CASE WHEN SO_DU_CUOI_KY_NGOAI_TE_TMP < 0
                                                                THEN -1
                                                                     * SO_DU_CUOI_KY_NGOAI_TE_TMP
                                                                ELSE 0
                                                           END
                                                 END );
                        UPDATE TMP_KET_QUA_1
                        SET "DU_NO_NGUYEN_TE" = rec."DU_NO_NGUYEN_TE"
                          WHERE RowNum =rec.RowNum
                    ;
        
                      rec."DU_CO_NGUYEN_TE" = ( CASE WHEN  rec."TINH_CHAT" = '1'--DU_CO_NGUYEN_TE
                                                       THEN SO_DU_CUOI_KY_NGOAI_TE_TMP
                                                       WHEN  rec."TINH_CHAT" = '0'
                                                       THEN 0
                                                       ELSE CASE WHEN SO_DU_CUOI_KY_NGOAI_TE_TMP > 0
                                                                 THEN SO_DU_CUOI_KY_NGOAI_TE_TMP
                                                                 ELSE 0
                                                            END
                                                  END );
                     UPDATE TMP_KET_QUA_1
                        SET "DU_CO_NGUYEN_TE" = rec."DU_CO_NGUYEN_TE"
                          WHERE RowNum =rec.RowNum
                    ;
        
                      SELECT (CASE WHEN rec."OrderType" = 0
                        THEN (CASE WHEN rec."DU_NO" = 0 --DU_NO_NGUYEN_TE
                            THEN rec."DU_CO" --DU_CO_NGUYEN_TE
                              ELSE -1
                                   * rec."DU_NO" --DU_NO_NGUYEN_TE
                              END)
                            WHEN SO_TAI_KHOAN_TMP <> rec."SO_TAI_KHOAN" --@TAI_KHOAN_tmp
                                THEN rec."PHAT_SINH_CO" - rec."PHAT_SINH_NO" --PHAT_SINH_CO_NGUYEN_TE
                            ELSE SO_DU_CUOI_KY_TMP + rec."PHAT_SINH_CO"--PHAT_SINH_CO_NGUYEN_TE
                                 - rec."PHAT_SINH_NO" --PHAT_SINH_NO_NGUYEN_TE
                            END)
                    INTO SO_DU_CUOI_KY_TMP
                ;
        
                             rec."DU_NO" = ( CASE WHEN  rec."TINH_CHAT" = '0'--DU_NO_NGUYEN_TE
                                                      THEN -1 * SO_DU_CUOI_KY_TMP
                                                      WHEN  rec."TINH_CHAT" = '1'
                                                      THEN 0
                                                      ELSE CASE WHEN SO_DU_CUOI_KY_TMP < 0
                                                                THEN -1
                                                                     * SO_DU_CUOI_KY_TMP
                                                                ELSE 0
                                                           END
                                                 END );
        
                        UPDATE TMP_KET_QUA_1
                        SET "DU_NO" = rec."DU_NO"
                        WHERE RowNum =rec.RowNum
                    ;
        
        
                             rec."DU_CO" = ( CASE WHEN  rec."TINH_CHAT" = '1'--DU_CO_NGUYEN_TE
                                                       THEN SO_DU_CUOI_KY_TMP
                                                       WHEN  rec."TINH_CHAT" = '0'
                                                       THEN 0
                                                       ELSE CASE WHEN SO_DU_CUOI_KY_TMP > 0
                                                                 THEN SO_DU_CUOI_KY_TMP
                                                                 ELSE 0
                                                            END
                                                  END );
        
                        UPDATE TMP_KET_QUA_1
                        SET "DU_CO" = rec."DU_CO"
                        WHERE RowNum =rec.RowNum
                    ;
        
                    SELECT rec."SO_TAI_KHOAN" INTO
                     SO_TAI_KHOAN_TMP
                         from TMP_KET_QUA_1 kq1
                                        ;
                     UPDATE TMP_KET_QUA_1
                        SET "SO_TAI_KHOAN" = rec."SO_TAI_KHOAN"
                        WHERE RowNum =rec.RowNum
                    ;
        
                END LOOP
                ;
        
        
        
        END $$
        ;
                        SELECT
                        GL.RowNum ,
                        GL."SO_TAI_KHOAN" as "TAI_KHOAN" ,         --TAI_KHOAN
                        GL."TEN_TAI_KHOAN"      ,--TEN_TAI_KHOAN
                        GL."NGAY_HACH_TOAN" as "NGAY_HACH_TOAN" ,--NGAY_HACH_TOAN
                        GL."NGAY_CHUNG_TU" as "NGAY_CHUNG_TU",--NGAY_CHUNG_TU
                        GL."SO_CHUNG_TU" as "SO_CHUNG_TU" ,               --SO_CHUNG_TU
                        GL."ID_CHUNG_TU" as "ID_GOC" , 
                         GL."MODEL_CHUNG_TU" as "MODEL_GOC",
                        GL."LOAI_CHUNG_TU" ,

                        GL."DIEN_GIAI" as "DIEN_GIAI" ,                --DIEN_GIAI
                        GL."TK_DOI_UNG" as "TK_DOI_UNG" ,--TK_DOI_UNG
                        GL."PHAT_SINH_NO_NGUYEN_TE"  ,--PHAT_SINH_NO_NGOAI_TE
                        GL."PHAT_SINH_NO" as "PHAT_SINH_NO" ,--PHAT_SINH_NO
                        GL."PHAT_SINH_CO_NGUYEN_TE" ,--PHAT_SINH_CO_NGOAI_TE
                        GL."PHAT_SINH_CO" as "PHAT_SINH_CO" ,--PHAT_SINH_CO
                        GL."DU_NO" as "DU_NO" , -- Dư Nợ--DU_NO
                        GL."DU_NO_NGUYEN_TE" , -- Dư Nợ quy đổi--DU_NO_NGOAI_TE
                        GL."DU_CO" as "DU_CO" , -- Dư Có--DU_CO
                        GL."DU_CO_NGUYEN_TE"  -- Dư Có quy đổi --DU_CO_NGOAI_TE

                FROM    TMP_KET_QUA_1 GL
                        LEFT JOIN account_ex_don_dat_hang SAO ON Gl."DON_DAT_HANG_ID" = SAO."id"
                        LEFT JOIN danh_muc_ma_thong_ke LI ON LI."id" = GL."MA_THONG_KE_ID"
                        LEFT JOIN danh_muc_cong_trinh PW ON PW."id" = GL."CONG_TRINH_ID"
                        LEFT JOIN danh_muc_doi_tuong_tap_hop_chi_phi JO ON JO."id" = GL."DOI_TUONG_THCP_ID"
                        LEFT JOIN danh_muc_khoan_muc_cp EI ON EI."id" = GL."KHOAN_MUC_CP_ID"
                ORDER BY rowNUm 
                OFFSET %(offset)s
                LIMIT %(limit)s;


;

        """
        return self.execute(query,params_sql)

    def _lay_bao_cao_chi_co_phat_sinh(self, params_sql):      
        record = []
        query = """
        --BAO_CAO_SO_CHI_TIET_CAC_TAI_KHOAN: chỉ lấy phát sinh
DO LANGUAGE plpgsql $$
DECLARE
    v_tu_ngay                             DATE := %(TU_NGAY)s;

    --tham số từ

    v_den_ngay                            DATE := %(DEN_NGAY)s;

    --tham số đến

    v_bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    --tham số bao gồm số liệu chi nhánh phụ thuộc

    v_chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    --tham số chi nhánh


    v_loai_tien_id                        INTEGER := %(currency_id)s;

    --tham số loại tiền


    v_cong_gop_cac_but_toan_giong_nhau    INTEGER := %(CONG_GOP_CAC_BUT_TOAN_GIONG_NHAU)s;

    --cộng gộp các bút toán giống nhau


 

   


    rec                                   RECORD;

   


    LOAI_HINH_KD_0                        VARCHAR(127) := N'Chiết khấu thương mại (bán hàng)';

    LOAI_HINH_KD_1                        VARCHAR(127) := N'Giảm giá hàng bán';

    LOAI_HINH_KD_2                        VARCHAR(127) := N'Trả lại hàng bán';

    LOAI_HINH_KD_3                        VARCHAR(127) := N'Khấu trừ thuế hoạt động sản xuất kinh doanh';

    LOAI_HINH_KD_4                        VARCHAR(127) :=  N'Khấu trừ thuế hoạt động đầu tư';

    IsVietNamese                          INTEGER := 1;


BEGIN
    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(v_chi_nhanh_id, v_bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;

    DROP TABLE IF EXISTS DS_TAI_KHOAN
    ;

    CREATE TEMP TABLE DS_TAI_KHOAN
        AS
            SELECT
                A."SO_TAI_KHOAN"
                , --TAI_KHOAN
                A."TEN_TAI_KHOAN"
                , A."TEN_TIENG_ANH"
                , A."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                , --TAI_KHOAN
                A."TINH_CHAT"
            FROM danh_muc_he_thong_tai_khoan A --tham số tài khoản
            WHERE (id = any (%(TAI_KHOAN_IDS)s))
    ;

    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    DROP SEQUENCE IF EXISTS TMP_KET_QUA_seq
    ;

    CREATE TEMP SEQUENCE TMP_KET_QUA_seq
    ;

    CREATE TEMP TABLE TMP_KET_QUA
    (
        RowNum                  INT DEFAULT NEXTVAL('TMP_KET_QUA_seq')
            PRIMARY KEY,

        "ID_CHUNG_TU"           INT,
        "MODEL_CHUNG_TU"        VARCHAR(127),
        "LOAI_CHUNG_TU"         VARCHAR(127),
        "NGAY_HACH_TOAN"        DATE,
        "NGAY_CHUNG_TU"         DATE,
        "SO_CHUNG_TU"           VARCHAR(127), --SO_CHUNG_TU
        "DIEN_GIAI"             VARCHAR(255),
        "SO_TAI_KHOAN"          VARCHAR(127),
        "TEN_TAI_KHOAN"         VARCHAR(127),
        "TINH_CHAT"             VARCHAR(127),
        "TK_DOI_UNG"            VARCHAR(127),
        "PHAT_SINH_NO_NGUYEN_TE" FLOAT, -- Phát sinh nợ--PHAT_SINH_NO_NGUYEN_TE
        "PHAT_SINH_NO"          FLOAT, --Phát sinh nợ quy đổi--PHAT_SINH_NO
        "PHAT_SINH_CO_NGUYEN_TE" FLOAT, -- Phát sinh Có--PHAT_SINH_CO_NGUYEN_TE
        "PHAT_SINH_CO"          FLOAT, -- Phát sinh Có quy đổi--PHAT_SINH_CO
        "MA_THONG_KE_ID"        INT,
        "DOI_TUONG_THCP_ID"     INT,
        "CONG_TRINH_ID"         INT,
        "DON_DAT_HANG_ID"       INT,
        "KHOAN_MUC_CP_ID"       INT

    )
    ;

    ----------------------------------


    --Lấy dữ liệu trong kỳ
    IF v_cong_gop_cac_but_toan_giong_nhau = 0  -- Không cộng gộp dl
    THEN
        INSERT INTO TMP_KET_QUA
        (
            "ID_CHUNG_TU",
            "MODEL_CHUNG_TU",
            "LOAI_CHUNG_TU",
            "NGAY_HACH_TOAN", --NGAY_HACH_TOAN
            "SO_CHUNG_TU", --SO_CHUNG_TU
            "NGAY_CHUNG_TU", --NGAY_CHUNG_TU
            "DIEN_GIAI", --DIEN_GIAI
            "SO_TAI_KHOAN",
            "TEN_TAI_KHOAN",
            "TINH_CHAT",
            "TK_DOI_UNG", --TK_DOI_UNG
            "PHAT_SINH_NO_NGUYEN_TE", -- Phát sinh nợ--PHAT_SINH_NO_NGUYEN_TE
            "PHAT_SINH_NO", --Phát sinh nợ quy đổi--PHAT_SINH_NO
            "PHAT_SINH_CO_NGUYEN_TE", -- Phát sinh Có--PHAT_SINH_CO_NGUYEN_TE
            "PHAT_SINH_CO", -- Phát sinh Có quy đổi--PHAT_SINH_CO
            "MA_THONG_KE_ID",
            "DOI_TUONG_THCP_ID",
            "CONG_TRINH_ID",
            "DON_DAT_HANG_ID",
            "KHOAN_MUC_CP_ID"

        )
            SELECT


                  GL."ID_CHUNG_TU"          AS "ID_CHUNG_TU"
                , GL."MODEL_CHUNG_TU"       AS "MODEL_CHUNG_TU"
                , --  "ID_CHUNG_TU" ,
                  GL."LOAI_CHUNG_TU"        AS "LOAI_CHUNG_TU"
                , --  "LOAI_CHUNG_TU" ,
                  GL."NGAY_HACH_TOAN"       AS "NGAY_HACH_TOAN"
                , --  "NGAY_HACH_TOAN" ,--NGAY_HACH_TOAN
                  GL."SO_CHUNG_TU"          AS "SO_CHUNG_TU"
                , --  "SO_CHUNG_TU" ,--SO_CHUNG_TU
                  GL."NGAY_CHUNG_TU"        AS "NGAY_CHUNG_TU"

                , GL."DIEN_GIAI"            AS "DIEN_GIAI"
                , --  "DIEN_GIAI" ,--DIEN_GIAI
                  AC."SO_TAI_KHOAN"         AS "SO_TAI_KHOAN"
                , --  "TAI_KHOAN" ,--TAI_KHOAN
                  AC."TEN_TAI_KHOAN"        AS "TEN_TAI_KHOAN"

                , AC."TINH_CHAT"            AS "TINH_CHAT"
                --  "TEN_TAI_KHOAN" ,
                , GL."MA_TAI_KHOAN_DOI_UNG" AS "MA_TAI_KHOAN_DOI_UNG"
                --  "TK_DOI_UNG" ,--TK_DOI_UNG

                , --  "TINH_CHAT" ,
                  GL."GHI_NO"               AS "PHAT_SINH_NO"
                , --  "PHAT_SINH_NO" , -- Phát sinh nợ--PHAT_SINH_NO
                  GL."GHI_NO_NGUYEN_TE"     AS "PHAT_SINH_NO_NGUYEN_TE"
                , --  "PHAT_SINH_NO_NGUYEN_TE" , -- Phát sinh nợ quy đổi--PHAT_SINH_NO_NGUYEN_TE
                  GL."GHI_CO"               AS "PHAT_SINH_CO"
                , --  "PHAT_SINH_CO" , -- Phát sinh có--PHAT_SINH_CO
                  GL."GHI_CO_NGUYEN_TE"     AS "PHAT_SINH_CO_NGUYEN_TE"


                , GL."MA_THONG_KE_ID"
                , GL."DOI_TUONG_THCP_ID"
                , GL."CONG_TRINH_ID"
                , GL."DON_DAT_HANG_ID"
                , GL."KHOAN_MUC_CP_ID"


            FROM so_cai_chi_tiet AS GL

                INNER JOIN DS_TAI_KHOAN AC ON GL."MA_TAI_KHOAN" LIKE AC."AccountNumberPercent"

                INNER JOIN TMP_LIST_BRAND OU ON GL."CHI_NHANH_ID" = OU."CHI_NHANH_ID"
                LEFT JOIN danh_muc_to_chuc AS OU2 ON GL."DVT_ID" = OU2."id"

            WHERE GL."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay--NGAY_HACH_TOAN

                  AND (GL."GHI_NO_NGUYEN_TE" <> 0--PHAT_SINH_NO_NGUYEN_TE
                       OR GL."GHI_CO_NGUYEN_TE" <> 0--PHAT_SINH_CO_NGUYEN_TE
                       OR GL."GHI_NO" <> 0--PHAT_SINH_NO
                       OR GL."GHI_CO" <> 0--PHAT_SINH_CO
                  )
                  AND (v_loai_tien_id IS NULL
                       OR GL."currency_id" = v_loai_tien_id
                  )
            ORDER BY
                "SO_TAI_KHOAN",
                "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU",
                "SO_CHUNG_TU"

        ;


    ELSE --Cộng gộp các bút toán giống nhau
        INSERT INTO TMP_KET_QUA
        (
            "ID_CHUNG_TU",
            "MODEL_CHUNG_TU",
            "LOAI_CHUNG_TU",
            "NGAY_HACH_TOAN", --NGAY_HACH_TOAN
            "SO_CHUNG_TU", --SO_CHUNG_TU
            "NGAY_CHUNG_TU", --NGAY_CHUNG_TU
            "DIEN_GIAI", --DIEN_GIAI
            "SO_TAI_KHOAN",
            "TEN_TAI_KHOAN", --TEN_TAI_KHOAN,
            "TK_DOI_UNG", --TK_DOI_UNG
            "TINH_CHAT",
            "PHAT_SINH_NO", --PHAT_SINH_NO
            "PHAT_SINH_NO_NGUYEN_TE", --PHAT_SINH_NO_NGUYEN_TE
            "PHAT_SINH_CO", --PHAT_SINH_CO
            "PHAT_SINH_CO_NGUYEN_TE" --PHAT_SINH_CO_NGUYEN_TE


        )
            SELECT
                  GL."ID_CHUNG_TU"           AS "ID_CHUNG_TU"
                , GL."MODEL_CHUNG_TU"        AS "MODEL_CHUNG_TU"
                , GL."LOAI_CHUNG_TU"         AS "LOAI_CHUNG_TU"
                , GL."NGAY_HACH_TOAN"        AS "NGAY_HACH_TOAN"
                , --NGAY_HACH_TOAN
                  GL."SO_CHUNG_TU"           AS "SO_CHUNG_TU"
                , --SO_CHUNG_TU
                  GL."NGAY_CHUNG_TU"         AS "NGAY_CHUNG_TU"
                , --NGAY_CHUNG_TU
                  GL."DIEN_GIAI_CHUNG"       AS "DIEN_GIAI"
                , --DIEN_GIAI
                  AC."SO_TAI_KHOAN"          AS "SO_TAI_KHOAN"
                , --TAI_KHOAN
                  AC."TEN_TAI_KHOAN"         AS "TEN_TAI_KHOAN"
                , GL."MA_TAI_KHOAN_DOI_UNG"  AS "TK_DOI_UNG"
                , --TK_DOI_UNG
                  AC."TINH_CHAT"             AS "TINH_CHAT"
                , SUM(GL."GHI_NO")           AS "PHAT_SINH_NO"
                , --PHAT_SINH_NO)
                  SUM(GL."GHI_NO_NGUYEN_TE") AS "PHAT_SINH_NO_NGUYEN_TE"
                , --PHAT_SINH_NO_NGUYEN_TE)
                  SUM(GL."GHI_CO")           AS "PHAT_SINH_CO"
                , --PHAT_SINH_CO)
                  SUM(GL."GHI_CO_NGUYEN_TE") AS "PHAT_SINH_CO_NGUYEN_TE"


            FROM so_cai_chi_tiet AS GL

                INNER JOIN DS_TAI_KHOAN AC ON GL."MA_TAI_KHOAN" LIKE AC."AccountNumberPercent"
                --#tblTAI_KHOAN
                INNER JOIN TMP_LIST_BRAND OU ON GL."CHI_NHANH_ID" = OU."CHI_NHANH_ID"
                LEFT JOIN danh_muc_to_chuc AS OU2 ON GL."DVT_ID" = OU2."id"

            WHERE (GL."NGAY_HACH_TOAN" BETWEEN v_tu_ngay AND v_den_ngay)--NGAY_HACH_TOAN

                  AND (v_loai_tien_id IS NULL
                       OR GL."currency_id" = v_loai_tien_id
                  )
            GROUP BY
                GL."ID_CHUNG_TU",
                GL."MODEL_CHUNG_TU",
                GL."LOAI_CHUNG_TU",
                GL."NGAY_HACH_TOAN", --NGAY_HACH_TOAN
                GL."SO_CHUNG_TU", --SO_CHUNG_TU
                GL."NGAY_CHUNG_TU", --NGAY_CHUNG_TU
                GL."DIEN_GIAI_CHUNG", --DIEN_GIAI
                AC."SO_TAI_KHOAN", --TAI_KHOAN
                AC."TEN_TAI_KHOAN",
                GL."MA_TAI_KHOAN_DOI_UNG", --TK_DOI_UNG
                AC."TINH_CHAT"
            HAVING SUM(GL."GHI_NO_NGUYEN_TE") <> 0--PHAT_SINH_NO_NGUYEN_TE)
                   OR SUM(GL."GHI_CO_NGUYEN_TE") <> 0--PHAT_SINH_CO_NGUYEN_TE)
                   OR SUM(GL."GHI_NO") <> 0--PHAT_SINH_NO)
                   OR SUM(GL."GHI_CO") <> 0--PHAT_SINH_CO)
            ORDER BY
                "SO_TAI_KHOAN",
                "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU",
                "SO_CHUNG_TU"

        ;
    END IF
    ;

END $$
;

SELECT
    GL.RowNum

    , GL."ID_CHUNG_TU" AS "ID_GOC"
    , --NGAY_HACH_TOAN
    GL."MODEL_CHUNG_TU"    AS "MODEL_GOC"

    , GL."NGAY_HACH_TOAN" AS "NGAY_HACH_TOAN"
    , --NGAY_HACH_TOAN
    GL."NGAY_CHUNG_TU"    AS "NGAY_CHUNG_TU"
    , --NGAY_CHUNG_TU
    GL."SO_CHUNG_TU"       AS "SO_CHUNG_TU"
    , --SO_CHUNG_TU
    GL."DIEN_GIAI"        AS "DIEN_GIAI"
    , GL."SO_TAI_KHOAN"     AS "TAI_KHOAN"
    , --TAI_KHOAN


    GL."TK_DOI_UNG"           AS "TK_DOI_UNG"
    , --TK_DOI_UNG
    GL."PHAT_SINH_NO_NGUYEN_TE"    AS "PHAT_SINH_NO_SO_TIEN"
    , --PHAT_SINH_NO_NGUYEN_TE
    GL."PHAT_SINH_NO"           AS "PHAT_SINH_NO_QUY_DOI"
    , --PHAT_SINH_NO
    GL."PHAT_SINH_CO_NGUYEN_TE"      AS "PHAT_SINH_CO_SO_TIEN"
    , --PHAT_SINH_CO_NGUYEN_TE
    GL."PHAT_SINH_CO"      AS "PHAT_SINH_CO_QUY_DOI"


FROM TMP_KET_QUA GL
    LEFT JOIN account_ex_don_dat_hang SAO ON Gl."DON_DAT_HANG_ID" = SAO."id"
    LEFT JOIN danh_muc_ma_thong_ke LI ON LI."id" = GL."MA_THONG_KE_ID"
    LEFT JOIN danh_muc_cong_trinh PW ON PW."id" = GL."CONG_TRINH_ID"
    LEFT JOIN danh_muc_doi_tuong_tap_hop_chi_phi JO ON JO."id" = GL."DOI_TUONG_THCP_ID"
    LEFT JOIN danh_muc_khoan_muc_cp EI ON EI."id" = GL."KHOAN_MUC_CP_ID"
ORDER BY rowNUm
OFFSET %(offset)s
LIMIT %(limit)s;
        """
        return self.execute(query,params_sql)

    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        TU = self.get_vntime('TU')
        DEN = self.get_vntime('DEN')
        TAI_KHOAN_ID = self.get_context('TAI_KHOAN_ID')
        currency_id = self.get_context('currency_id')
        THONG_KE_THEO = self.get_context('THONG_KE_THEO')
        tai_khoan = ''
        loai_tien = ''
        if TAI_KHOAN_ID :
            tai_khoan=self.env['danh.muc.he.thong.tai.khoan'].browse(TAI_KHOAN_ID).SO_TAI_KHOAN
        if currency_id : 
            loai_tien = self.env['res.currency'].browse(currency_id).MA_LOAI_TIEN
        if THONG_KE_THEO=='SO_DU_VA_PHAT_SINH':
            action = self.env.ref('bao_cao.open_report_bao_cao_so_chi_tiet_cac_tai_khoan_so_du_va_phat_sinh').read()[0]
        elif THONG_KE_THEO=='CHI_CO_PHAT_SINH':
            action = self.env.ref('bao_cao.open_report_bao_cao_so_chi_tiet_cac_tai_khoan_chi_co_phat_sinh').read()[0]
        param = 'Loại tiền: %s; Tài khoản: %s; Từ ngày: %s đến ngày %s' % (loai_tien, tai_khoan, TU, DEN)
        # action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action