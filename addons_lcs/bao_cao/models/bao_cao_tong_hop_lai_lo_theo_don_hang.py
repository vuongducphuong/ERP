# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_TONG_HOP_LAI_LO_THEO_DON_HANG(models.Model):
    _name = 'bao.cao.tong.hop.lai.lo.theo.don.hang'
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI', required='True')
    TU = fields.Date(string='Từ ', help='Từ ', required='True', default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến', required='True', default=fields.Datetime.now)
    
    SO_DON_HANG = fields.Char(string='Số đơn hàng', help='Số đơn hàng')
    NGAY_DON_HANG = fields.Date(string='Ngày đơn hàng', help='Ngày đơn hàng')
    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')
    DOANH_THU = fields.Float(string='Doanh thu', help='Doanh thu',digits= decimal_precision.get_precision('VND'))
    GIAM_TRU_DOANH_THU = fields.Float(string='Giảm trừ doanh thu', help='Giảm trừ doanh thu',digits= decimal_precision.get_precision('VND'))
    DOANH_THU_THUAN = fields.Float(string='Doanh thu thuần', help='Doanh thu thuần',digits= decimal_precision.get_precision('VND'))
    GIA_VON_HANG_BAN = fields.Float(string='Giá vốn hàng bán', help='Giá vốn hàng bán',digits= decimal_precision.get_precision('VND'))
    CP_BAN_HANG = fields.Float(string='CP bán hàng', help='CP bán hàng',digits= decimal_precision.get_precision('VND'))
    CP_QUAN_LY = fields.Float(string='CP quản lý', help='CP quản lý',digits= decimal_precision.get_precision('VND'))
    CP_KHAC = fields.Float(string='CP khác', help='CP khác',digits= decimal_precision.get_precision('VND'))
    LAI_LO = fields.Float(string='Lãi/lỗ', help='Lãi_lỗ',digits= decimal_precision.get_precision('VND'))
    TY_SUAT_LOI_NHUAN_DOANH_THU = fields.Float(string='Tỷ suất lợi nhuận/doanh thu(%)', help='Tỷ suất lợi nhuận_doanh thu')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    CHON_TAT_CA_DON_DAT_HANG = fields.Boolean('Tất cả đơn hàng', default=True)
    DON_DAT_HANG_MANY_IDS = fields.Many2many('account.ex.don.dat.hang', 'tong_hop_lai_lo_theo_don_hang', string='Chọn đơn hàng')
    DON_DAT_HANG_IDS = fields.One2many('account.ex.don.dat.hang')

    # Đơn đặt hàng
    @api.onchange('DON_DAT_HANG_IDS')
    def update_DON_DAT_HANG_IDS(self):
        self.DON_DAT_HANG_IDS =self.DON_DAT_HANG_IDS.ids
        
    @api.onchange('DON_DAT_HANG_MANY_IDS')
    def _onchange_DON_DAT_HANG_MANY_IDS(self):
        self.DON_DAT_HANG_IDS = self.DON_DAT_HANG_MANY_IDS.ids
    # end  

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')
    
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_TONG_HOP_LAI_LO_THEO_DON_HANG, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        return result

    ### START IMPLEMENTING CODE ###
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

    den_ngay                            TIMESTAMP := %(DEN_NGAY)s;

    --tham số đến

    bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    --tham số bao gồm số liệu chi nhánh phụ thuộc

    chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s; 

    --tham số chi nhánh

    CHE_DO_KE_TOAN                      VARCHAR;

    BAO_CAO_ID                          VARCHAR :='SummaryIncomeBySAOrder';


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
        "ID_CHUNG_TU"   INT PRIMARY KEY,
        "SO_CHUNG_TU"   VARCHAR(25),
        "NGAY_CHUNG_TU" TIMESTAMP,
        "DOI_TUONG_ID"  INT

    )
    ;

    INSERT INTO TMP_DS_DON_DAT_HANG
        SELECT
            SAO."id"
            , SAO."SO_DON_HANG"
            , SAO."NGAY_DON_HANG"
            , SAO."KHACH_HANG_ID"


        FROM account_ex_don_dat_hang SAO

        WHERE SAO.id = any(%(DON_DAT_HANG_IDS)s) -- DON_DAT_HANG_IDS
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA
        AS

            SELECT
                  ROW_NUMBER()
                  OVER (
                      ORDER BY tbl."SO_CHUNG_TU" ) AS                            RowNum
                , tbl."DON_DAT_HANG_ID"
                , tbl."SO_CHUNG_TU"                AS                            "DON_DAT_HANG"
                , tbl."NGAY_CHUNG_TU"              AS                            "NGAY_DON_HANG"
                , AO."MA"                          AS                            "MA_KHACH_HANG"
                , AO."HO_VA_TEN"                   AS                            "TEN_KHACH_HANG"
                , SUM(tbl."DOANH_THU")             AS                            "DOANH_THU" --Receipt
                , SUM(tbl."GIAM_TRU_DOANH_THU")    AS                            "GIAM_TRU_DOANH_THU" --ReduceReceipt
                , SUM(tbl."DOANH_THU_THUAN")       AS                            "DOANH_THU_THUAN" --PureReceipt
                , SUM(tbl."GIA_VON_HANG_BAN")      AS                            "GIA_VON_HANG_BAN" --SaleFund
                , SUM(tbl."CP_BAN_HANG")           AS                            "CHI_PHI_BAN_HANG" --SaleExpenditure
                , SUM(tbl."CP_QUAN_LY")            AS                            "CHI_PHI_QUAN_LY" --ManagementExpenditure
                , SUM(tbl."CP_KHAC")               AS                            "CHI_PHI_KHAC" --OtherExpenditure
                , SUM(tbl."DOANH_THU_THUAN" - tbl."GIA_VON_HANG_BAN" - tbl."CP_BAN_HANG"
                      - tbl."CP_QUAN_LY" - tbl."CP_KHAC") "LAI_LO"
                , CASE WHEN SUM(tbl."DOANH_THU_THUAN" - tbl."GIA_VON_HANG_BAN"
                                - tbl."CP_BAN_HANG"
                                - tbl."CP_QUAN_LY"
                                - tbl."CP_KHAC") > 0
                THEN SUM(tbl."DOANH_THU_THUAN" - tbl."GIA_VON_HANG_BAN"
                         - tbl."CP_BAN_HANG"
                         - tbl."CP_QUAN_LY"
                         - tbl."CP_KHAC")
                     / CASE WHEN SUM(tbl."DOANH_THU_THUAN") <> 0
                    THEN SUM(tbl."DOANH_THU_THUAN")
                       ELSE 1
                       END * 100
                  ELSE 0
                  END                                                            "TY_SUAT_LOI_NHUAN_DOANH_THU_PHAN_TRAM"

            FROM (SELECT
                      GL."DON_DAT_HANG_ID"
                      , LSAO."SO_CHUNG_TU"
                      , LSAO."NGAY_CHUNG_TU"
                      , LSAO."DOI_TUONG_ID"
                      , CASE WHEN GL."TEN_COT" = 'Receipt'
                    THEN GL."SO_TIEN"
                        ELSE 0
                        END "DOANH_THU"
                      , CASE WHEN GL."TEN_COT" = 'ReduceReceipt'
                    THEN GL."SO_TIEN"
                        ELSE 0
                        END "GIAM_TRU_DOANH_THU"
                      , CASE GL."TEN_COT"
                        WHEN 'Receipt'
                            THEN GL."SO_TIEN"
                        WHEN 'ReduceReceipt'
                            THEN -GL."SO_TIEN"
                        ELSE 0
                        END "DOANH_THU_THUAN"
                      , CASE WHEN GL."TEN_COT" = 'SaleFund'
                    THEN GL."SO_TIEN"
                        ELSE 0
                        END "GIA_VON_HANG_BAN"
                      , CASE WHEN GL."TEN_COT" = 'SaleExpenditure'
                    THEN GL."SO_TIEN"
                        ELSE 0
                        END "CP_BAN_HANG"
                      , CASE WHEN GL."TEN_COT" = 'ManagementExpenditure'
                    THEN GL."SO_TIEN"
                        ELSE 0
                        END "CP_QUAN_LY"
                      , CASE WHEN GL."TEN_COT" = 'OtherExpenditure'
                    THEN GL."SO_TIEN"
                        ELSE 0
                        END "CP_KHAC"

                  FROM LAY_SO_LIEU_SO_CAI_THEO_CT_THIET_LAP_BCTC_TRA_VE(NULL,
                                                                        tu_ngay,
                                                                        den_ngay,
                                                                        BAO_CAO_ID, NULL,
                                                                        chi_nhanh_id,
                                                                        bao_gom_du_lieu_chi_nhanh_phu_thuoc
                       ) GL
                      INNER JOIN TMP_DS_DON_DAT_HANG LSAO ON LSAO."ID_CHUNG_TU" = GL."DON_DAT_HANG_ID"
                  UNION ALL
                  SELECT
                        JCAEDT."MA_DON_VI_ID" "DON_DAT_HANG_ID"
                      , LSAO."SO_CHUNG_TU"
                      , LSAO."NGAY_CHUNG_TU"
                      , LSAO."DOI_TUONG_ID"
                      , 0                     "DOANH_THU"
                      , 0                     "GIAM_TRU_DOANH_THU"
                      , 0                     "DOANH_THU_THUAN"
                      , CASE WHEN (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '632%%'
                      THEN JCAEDT."SO_TIEN"
                        ELSE 0
                        END                   "GIA_VON_HANG_BAN"
                      , CASE WHEN CHE_DO_KE_TOAN = '15'
                                  AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '641%%'
                      THEN JCAEDT."SO_TIEN"
                        WHEN CHE_DO_KE_TOAN = '48'
                             AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '6421%%'
                            THEN JCAEDT."SO_TIEN"
                        ELSE 0
                        END                   "CP_BAN_HANG"
                      , CASE WHEN CHE_DO_KE_TOAN = '15'
                                  AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '642%%'
                      THEN JCAEDT."SO_TIEN"
                        WHEN CHE_DO_KE_TOAN = '48'
                             AND (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '6422%%'
                            THEN JCAEDT."SO_TIEN"
                        ELSE 0
                        END                   "CP_QUAN_LY"
                      , CASE WHEN (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '811%%'
                                  OR (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '635%%'
                      THEN JCAEDT."SO_TIEN"
                        ELSE 0
                        END

                  FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JCAE
                      INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCAEDT
                          ON JCAEDT."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JCAE."id"
                      INNER JOIN TMP_DS_DON_DAT_HANG LSAO ON LSAO."ID_CHUNG_TU" = JCAEDT."MA_DON_VI_ID"
                      INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCAE."CHI_NHANH_ID"
                  WHERE JCAEDT."CAP_TO_CHUC" = '2'
                        AND JCAE."NGAY_CHUNG_TU" BETWEEN tu_ngay AND den_ngay

                 ) tbl
                LEFT JOIN res_partner AO ON AO."id" = tbl."DOI_TUONG_ID"
            GROUP BY
                tbl."DON_DAT_HANG_ID",
                tbl."SO_CHUNG_TU",
                tbl."NGAY_CHUNG_TU",
                AO."MA",
                AO."HO_VA_TEN"
    ;

END $$
;

SELECT 

"DON_DAT_HANG" AS "SO_DON_HANG",
"NGAY_DON_HANG" AS "NGAY_DON_HANG",
"TEN_KHACH_HANG" AS "TEN_KHACH_HANG",
"DOANH_THU" AS "DOANH_THU",
"GIAM_TRU_DOANH_THU" AS "GIAM_TRU_DOANH_THU",
"DOANH_THU_THUAN" AS "DOANH_THU_THUAN",
"GIA_VON_HANG_BAN" AS "GIA_VON_HANG_BAN",
"CHI_PHI_BAN_HANG" AS "CP_BAN_HANG",
"CHI_PHI_QUAN_LY" AS "CP_QUAN_LY",
"CHI_PHI_KHAC" AS "CP_KHAC",
"LAI_LO" AS "LAI_LO",
"TY_SUAT_LOI_NHUAN_DOANH_THU_PHAN_TRAM" AS "TY_SUAT_LOI_NHUAN_DOANH_THU"

FROM TMP_KET_QUA

ORDER BY RowNum
OFFSET %(offset)s
LIMIT %(limit)s;
;
        """
        return self.execute(query,params_sql)
        
    ### END IMPLEMENTING CODE ###
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



    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU')
        DEN_NGAY_F = self.get_vntime('DEN')
        param = 'Từ ngày: %s đến ngày %s' % (TU_NGAY_F, DEN_NGAY_F)
        action = self.env.ref('bao_cao.open_report_tong_hop_lai_lo_theo_don_hang').read()[0]
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action