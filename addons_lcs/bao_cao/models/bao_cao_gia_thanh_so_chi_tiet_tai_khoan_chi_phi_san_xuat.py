# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_GIA_THANH_SO_CHI_TIET_TAI_KHOAN_CHI_PHI_SAN_XUAT(models.Model):
    _name = 'bao.cao.gia.thanh.so.chi.tiet.tai.khoan.cpsx'
    _description = ''
    _inherit = ['mail.thread']
    _auto = False

    THONG_KE_THEO = fields.Selection([('DOI_TUONG_THCP', 'Đối tượng tập hợp chi phí'),('CONG_TRINH', 'Công trình'),('DON_HANG', 'Đơn hàng'),('HOP_DONG', 'Hợp đồng')], string='Thống kê theo', help='Thống kê theo',default='DOI_TUONG_THCP',required=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh', required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI', required='True')
    TU = fields.Date(string='Từ ', help='Từ ', required='True', default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến', required='True', default=fields.Datetime.now)
    
    SO_DON_HANG = fields.Char(string='SO_DON_HANG', help='JobCode')
    HOP_DONG_DU_AN = fields.Char(string='HOP_DONG_DU_AN', help='JobCode')
    TRICH_YEU = fields.Char(string='TRICH_YEU', help='JobCode')
    TEN_DOI_TUONG_THCP = fields.Char(string='TEN_DOI_TUONG_THCP', help='JobName')
    TEN_CONG_TRINH = fields.Char(string='TEN_CONG_TRINH', help='JobName')
    NGAY_DON_HANG = fields.Char(string='NGAY_DON_HANG', help='JobCode')
    SO_TAI_KHOAN = fields.Char(string='SO_TAI_KHOAN', help='AccountNumber')
    
    NGAY_HACH_TOAN = fields.Date(string='NGAY_HACH_TOAN', help='OpenDebitAmount')
    NGAY_CHUNG_TU = fields.Date(string='NGAY_CHUNG_TU', help='OpenDebitAmount')
    SO_CHUNG_TU = fields.Char(string='SO_CHUNG_TU', help='OpenDebitAmount')
    DIEN_GIAI = fields.Char(string='DIEN_GIAI', help='OpenDebitAmount')
    TK_DOI_UNG = fields.Char(string='TK_DOI_UNG', help='OpenDebitAmount')

    SO_TIEN_NO = fields.Float(string='SO_TIEN_NO', help='OpenCreditAmount',digits=decimal_precision.get_precision('VND'))
    SO_TIEN_CO = fields.Float(string='SO_TIEN_CO', help='DebitAmount',digits=decimal_precision.get_precision('VND'))
    
    TAI_KHOAN_IDS = fields.One2many('danh.muc.he.thong.tai.khoan')
    CHON_TAT_CA_TAI_KHOAN = fields.Boolean('Tất cả tài khoản', default=True)
    TAI_KHOAN_MANY_IDS = fields.Many2many('danh.muc.he.thong.tai.khoan','tong_hop_chi_phi_sxkd_httk', string='Chọn tài khoản') 

    DOI_TUONG_THCP_IDS = fields.One2many('danh.muc.doi.tuong.tap.hop.chi.phi')
    CHON_TAT_CA_DOI_TUONG_THCP = fields.Boolean('Tất cả đối tượng THCP', default=True)
    DOI_TUONG_THCP_MANY_IDS = fields.Many2many('danh.muc.doi.tuong.tap.hop.chi.phi','tong_hop_chi_phi_sxkd_dtthcp', string='Chọn đối tượng THCP') 

    CONG_TRINH_IDS = fields.One2many ('danh.muc.cong.trinh')
    CHON_TAT_CA_CONG_TRINH = fields.Boolean('Tất cả công trình', default=True)
    CONG_TRINH_MANY_IDS = fields.Many2many('danh.muc.cong.trinh','tong_hop_chi_phi_sxkd_cong_trinh', string='Chọn công trình') 

    DON_HANG_IDS = fields.One2many('account.ex.don.dat.hang')
    CHON_TAT_CA_DON_HANG = fields.Boolean('Tất cả đơn hàng', default=True)
    DON_HANG_MANY_IDS = fields.Many2many('account.ex.don.dat.hang','tong_hop_chi_phi_sxkd_don_hang', string='Chọn đơn hàng') 

    HOP_DONG_BAN_IDS = fields.One2many('sale.ex.hop.dong.ban')
    CHON_TAT_CA_HOP_DONG_BAN = fields.Boolean('Tất cả hợp đồng', default=True)
    HOP_DONG_BAN_MANY_IDS = fields.Many2many('sale.ex.hop.dong.ban','tong_hop_chi_phi_sxkd_hdb', string='Chọn hợp đồng') 

    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')

    @api.onchange('THONG_KE_THEO')
    def _onchange_THONG_KE_THEO(self):
        self.CHON_TAT_CA_TAI_KHOAN = True
        self.CHON_TAT_CA_DOI_TUONG_THCP = True
        self.CHON_TAT_CA_CONG_TRINH = True
        self.CHON_TAT_CA_DON_HANG = True
        self.CHON_TAT_CA_HOP_DONG_BAN = True
       
        self.TAI_KHOAN_MANY_IDS = []
        self.DOI_TUONG_THCP_MANY_IDS = []
        self.CONG_TRINH_MANY_IDS = []
        self.DON_HANG_MANY_IDS = []
        self.HOP_DONG_BAN_MANY_IDS = []

    # Tài khoản
    @api.onchange('TAI_KHOAN_IDS')
    def _onchange_TAI_KHOAN_IDS(self):
        self.TAI_KHOAN_MANY_IDS =self.TAI_KHOAN_IDS.ids

    @api.onchange('TAI_KHOAN_MANY_IDS')
    def _onchange_TAI_KHOAN_MANY_IDS(self):
        self.TAI_KHOAN_IDS =self.TAI_KHOAN_MANY_IDS.ids
    # end
    # đối tượng THCP
    @api.onchange('DOI_TUONG_THCP_IDS')
    def _onchange_DOI_TUONG_THCP_IDS(self):
        self.DOI_TUONG_THCP_MANY_IDS =self.DOI_TUONG_THCP_IDS.ids

    @api.onchange('DOI_TUONG_THCP_MANY_IDS')
    def _onchange_DOI_TUONG_THCP_MANY_IDS(self):
        self.DOI_TUONG_THCP_IDS =self.DOI_TUONG_THCP_MANY_IDS.ids
    # end
    # Công trình
    @api.onchange('CONG_TRINH_IDS')
    def update_CONG_TRINH_IDS(self):
        self.CONG_TRINH_MANY_IDS =self.CONG_TRINH_IDS.ids
        
    @api.onchange('CONG_TRINH_MANY_IDS')
    def _onchange_CONG_TRINH_MANY_IDS(self):
        self.CONG_TRINH_IDS = self.CONG_TRINH_MANY_IDS.ids
    # end  
    # Đơn đặt hàng
    @api.onchange('DON_HANG_IDS')
    def update_DON_HANG_IDS(self):
        self.DON_HANG_MANY_IDS =self.DON_HANG_IDS.ids
        
    @api.onchange('DON_HANG_MANY_IDS')
    def _onchange_DON_HANG_MANY_IDS(self):
        self.DON_HANG_IDS = self.DON_HANG_MANY_IDS.ids
    # end  

    # Hợp đồng bán
    @api.onchange('HOP_DONG_BAN_IDS')
    def update_HOP_DONG_BAN_IDS(self):
        self.HOP_DONG_BAN_MANY_IDS =self.HOP_DONG_BAN_IDS.ids
        
    @api.onchange('HOP_DONG_BAN_MANY_IDS')
    def _onchange_HOP_DONG_BAN_MANY_IDS(self):
        self.HOP_DONG_BAN_IDS = self.HOP_DONG_BAN_MANY_IDS.ids
    # end  


    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_GIA_THANH_SO_CHI_TIET_TAI_KHOAN_CHI_PHI_SAN_XUAT, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        return result
    
    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')

    def _validate(self):
        params = self._context
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        TU_NGAY = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

        CHON_TAT_CA_TAI_KHOAN = params['CHON_TAT_CA_TAI_KHOAN'] if 'CHON_TAT_CA_TAI_KHOAN' in params.keys() else 'False'
        TAI_KHOAN_MANY_IDS = params['TAI_KHOAN_MANY_IDS'] if 'TAI_KHOAN_MANY_IDS' in params.keys() else 'False'
        
        CHON_TAT_CA_DOI_TUONG_THCP = params['CHON_TAT_CA_DOI_TUONG_THCP'] if 'CHON_TAT_CA_DOI_TUONG_THCP' in params.keys() else 'False'
        DOI_TUONG_THCP_MANY_IDS = params['DOI_TUONG_THCP_MANY_IDS'] if 'DOI_TUONG_THCP_MANY_IDS' in params.keys() else 'False'
        
        CHON_TAT_CA_CONG_TRINH = params['CHON_TAT_CA_CONG_TRINH'] if 'CHON_TAT_CA_CONG_TRINH' in params.keys() else 'False'
        CONG_TRINH_MANY_IDS = params['CONG_TRINH_MANY_IDS'] if 'CONG_TRINH_MANY_IDS' in params.keys() else 'False'
        
        CHON_TAT_CA_DON_HANG = params['CHON_TAT_CA_DON_HANG'] if 'CHON_TAT_CA_DON_HANG' in params.keys() else 'False'
        DON_HANG_MANY_IDS = params['DON_HANG_MANY_IDS'] if 'DON_HANG_MANY_IDS' in params.keys() else 'False'
        
        CHON_TAT_CA_HOP_DONG_BAN = params['CHON_TAT_CA_HOP_DONG_BAN'] if 'CHON_TAT_CA_HOP_DONG_BAN' in params.keys() else 'False'
        HOP_DONG_BAN_MANY_IDS = params['HOP_DONG_BAN_MANY_IDS'] if 'HOP_DONG_BAN_MANY_IDS' in params.keys() else 'False'
        

        if(TU_NGAY=='False'):
            raise ValidationError('<Từ ngày> không được bỏ trống.')
        elif(DEN_NGAY=='False'):
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        elif(TU_NGAY_F > DEN_NGAY_F):
            raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')

        if THONG_KE_THEO == 'DOI_TUONG_THCP':
            if CHON_TAT_CA_DOI_TUONG_THCP == 'False':
                if DOI_TUONG_THCP_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Đối tượng THCP>. Xin vui lòng chọn lại.')
        
        if THONG_KE_THEO == 'CONG_TRINH':
            if CHON_TAT_CA_CONG_TRINH == 'False':
                if CONG_TRINH_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Công trình>. Xin vui lòng chọn lại.')

        if THONG_KE_THEO == 'DON_HANG':
            if CHON_TAT_CA_DON_HANG == 'False':
                if DON_HANG_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Đơn đặt hàng>. Xin vui lòng chọn lại.')

        if THONG_KE_THEO == 'HOP_DONG':
            if CHON_TAT_CA_HOP_DONG_BAN == 'False':
                if HOP_DONG_BAN_MANY_IDS == []:
                    raise ValidationError('Bạn chưa chọn <Hợp đồng/Dự án>. Xin vui lòng chọn lại.')

        if THONG_KE_THEO in ('DOI_TUONG_THCP','CONG_TRINH','DON_HANG','HOP_DONG'):
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
        TU_NGAY = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
        
        if params.get('CHON_TAT_CA_TAI_KHOAN'):
            domain = []
            TAI_KHOAN_IDS = self.env['danh.muc.he.thong.tai.khoan'].search(domain).ids
        else:
            TAI_KHOAN_IDS = params.get('TAI_KHOAN_MANY_IDS')
        
        if params.get('CHON_TAT_CA_DOI_TUONG_THCP'):
            domain = []
            DOI_TUONG_THCP_IDS = self.env['danh.muc.doi.tuong.tap.hop.chi.phi'].search(domain).ids
        else:
            DOI_TUONG_THCP_IDS = params.get('DOI_TUONG_THCP_MANY_IDS')

        if params.get('CHON_TAT_CA_CONG_TRINH'):
            domain = []
            CONG_TRINH_IDS = self.env['danh.muc.cong.trinh'].search(domain).ids
        else:
            CONG_TRINH_IDS = params.get('CONG_TRINH_MANY_IDS')

        if params.get('CHON_TAT_CA_DON_HANG'):
            domain = []
            DON_HANG_IDS = self.env['account.ex.don.dat.hang'].search(domain).ids
        else:
            DON_HANG_IDS = params.get('DON_HANG_MANY_IDS')

        if params.get('CHON_TAT_CA_HOP_DONG_BAN'):
            domain = []
            HOP_DONG_BAN_IDS = self.env['sale.ex.hop.dong.ban'].search(domain).ids
        else:
            HOP_DONG_BAN_IDS = params.get('HOP_DONG_BAN_MANY_IDS')

        params_sql = {
            'TU_NGAY':TU_NGAY_F, 
            'DEN_NGAY':DEN_NGAY_F, 
            'TAI_KHOAN_IDS':TAI_KHOAN_IDS, 
            'DOI_TUONG_THCP_IDS':DOI_TUONG_THCP_IDS, 
            'CONG_TRINH_IDS':CONG_TRINH_IDS, 
            'DON_HANG_IDS':DON_HANG_IDS, 
            'HOP_DONG_BAN_IDS':HOP_DONG_BAN_IDS, 
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'CHI_NHANH_ID':CHI_NHANH_ID,
            'limit': limit,
            'offset': offset, 
            }      
    
        # Execute SQL query here
        if THONG_KE_THEO=='DOI_TUONG_THCP':
            return self._lay_bao_cao_doi_tuong_thcp(params_sql)

        if THONG_KE_THEO=='CONG_TRINH':
            return self._lay_bao_cao_cong_trinh(params_sql)

        if THONG_KE_THEO=='DON_HANG':
            return self._lay_bao_cao_don_hang(params_sql)
        
        if THONG_KE_THEO == 'HOP_DONG':
            return self._lay_bao_cao_hop_dong(params_sql)

    ### END IMPLEMENTING CODE ###
    def _lay_bao_cao_doi_tuong_thcp(self, params_sql):      
        record = []
        query = """
            DO LANGUAGE plpgsql $$
            DECLARE
            tu_ngay                             TIMESTAMP :=  %(TU_NGAY)s; 

            den_ngay                            TIMESTAMP :=  %(DEN_NGAY)s;

            bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER :=  %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

            chi_nhanh_id                        INTEGER :=  %(CHI_NHANH_ID)s;


            TON_TAI_TK_154                      BOOLEAN;

            SO_TK_154                           VARCHAR;


            TAI_KHOAN_ID_154                    INTEGER;

            CHE_DO_KE_TOAN                      VARCHAR;

            rec                                 RECORD;

            --@@ListJobID --Tham số bên misa
            --@ListAccountID ----Tham số bên misa


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


            DROP TABLE IF EXISTS TMP_TAI_KHOAN_DUOC_CHON
            ;

            CREATE TEMP TABLE TMP_TAI_KHOAN_DUOC_CHON
                -- Bảng các tài khoản được chọn
            (
                "TK_CONG_NO_ID"  INT,
                "TK_CONG_NO"     VARCHAR(20) PRIMARY KEY,
                "TEN_TK_DOI_UNG" VARCHAR(255)
            )
            ;

            INSERT INTO TMP_TAI_KHOAN_DUOC_CHON
                SELECT
                    A.id
                    , A."SO_TAI_KHOAN"
                    , A."TEN_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan A
                WHERE A."id" = any (%(TAI_KHOAN_IDS)s) --@ListAccountID
            ;

            DROP TABLE IF EXISTS TMP_SO_TAI_KHOAN
            ;

            CREATE TEMP TABLE TMP_SO_TAI_KHOAN
                -- Lấy các tài khoản cha nhất để đối chiếu
            (

                "TAI_KHOAN_ID"         INT,
                "SO_TAI_KHOAN"         VARCHAR(20) PRIMARY KEY,
                "TEN_TAI_KHOAN"        VARCHAR(255),
                "AccountNumberPercent" VARCHAR(25)
            )
            ;

            SELECT "SO_TAI_KHOAN"
            INTO SO_TK_154
            FROM danh_muc_he_thong_tai_khoan
            WHERE "SO_TAI_KHOAN" LIKE '154%%' AND "LA_TK_TONG_HOP" = FALSE
            ORDER BY "SO_TAI_KHOAN"
            LIMIT 1
            ;

            SELECT "id"
            INTO TAI_KHOAN_ID_154
            FROM danh_muc_he_thong_tai_khoan
            WHERE "SO_TAI_KHOAN" LIKE '154%%' AND "LA_TK_TONG_HOP" = FALSE
            ORDER BY "SO_TAI_KHOAN"
            LIMIT 1
            ;


            INSERT INTO TMP_SO_TAI_KHOAN
                SELECT DISTINCT
                    SA."id"
                    , SA."SO_TAI_KHOAN"
                    , SA."TEN_TAI_KHOAN"
                    , SA."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                FROM danh_muc_he_thong_tai_khoan SA
                    INNER JOIN TMP_TAI_KHOAN_DUOC_CHON SAD ON SA."SO_TAI_KHOAN" LIKE SAD."TK_CONG_NO"
                                                                                    || '%%'
                WHERE sa."LA_TK_TONG_HOP" = FALSE
            ;


            DROP TABLE IF EXISTS TMP_DOI_TUONG_THCP
            ;

            CREATE TEMP TABLE TMP_DOI_TUONG_THCP

                -- Bảng đối tượng THCP
            (
                "DOI_TUONG_THCP_ID"  INT PRIMARY KEY,
                "MA_DOI_TUONG_THCP"  VARCHAR(25),
                "TEN_DOI_TUONG_THCP" VARCHAR(128),
                "MA_PHAN_CAP"        VARCHAR(100)
            )
            ;

            INSERT INTO TMP_DOI_TUONG_THCP
                SELECT
                    J."id"
                    , J."MA_DOI_TUONG_THCP"
                    , J."TEN_DOI_TUONG_THCP"
                    , J."MA_PHAN_CAP"
                FROM
                    danh_muc_doi_tuong_tap_hop_chi_phi J
                WHERE J."id" = any ( %(DOI_TUONG_THCP_IDS)s) --@ListJobID
            ;

            DROP TABLE IF EXISTS TMP_DS_DOI_TUONG_THCP
            ;

            CREATE TEMP TABLE TMP_DS_DOI_TUONG_THCP

                -- Bảng đối tượng THCP gồm toàn bộ đối tượng THCP con
            (
                "DOI_TUONG_THCP_ID"  INT PRIMARY KEY,
                "MA_DOI_TUONG_THCP"  VARCHAR(25),
                "TEN_DOI_TUONG_THCP" VARCHAR(128),
                "MA_PHAN_CAP"        VARCHAR(100)
            )
            ;

            INSERT INTO TMP_DS_DOI_TUONG_THCP
                SELECT
                    J."id"
                    , J."MA_DOI_TUONG_THCP"
                    , J."TEN_DOI_TUONG_THCP"
                    , J."MA_PHAN_CAP"
                FROM TMP_DOI_TUONG_THCP tJ
                    INNER JOIN danh_muc_doi_tuong_tap_hop_chi_phi J ON J."MA_PHAN_CAP" LIKE tJ."MA_PHAN_CAP"
                                                                                            || '%%'
                GROUP BY
                    J."id",
                    J."MA_DOI_TUONG_THCP",
                    J."TEN_DOI_TUONG_THCP",
                    J."MA_PHAN_CAP"
            ;


            DROP TABLE IF EXISTS TMP_CHUNG_TU
            ;

            CREATE TEMP TABLE TMP_CHUNG_TU

            (
                "DOI_TUONG_THCP_ID"  INT,
                "MA_DOI_TUONG_THCP"  VARCHAR(25),
                "TEN_DOI_TUONG_THCP" VARCHAR(128),
                "MA_PHAN_CAP"        VARCHAR(100),
                "ID_CHUNG_TU"        INT,
                "MODEL_CHUNG_TU"     VARCHAR(100),
                "NGAY_HACH_TOAN"     TIMESTAMP,
                "NGAY_CHUNG_TU"      TIMESTAMP,
                "SO_CHUNG_TU"        VARCHAR(20),
                "LOAI_CHUNG_TU"      VARCHAR(500),
                "NGAY_HOA_DON"       TIMESTAMP,
                "SO_HOA_DON"         VARCHAR(500),
                "DIEN_GIAI"          VARCHAR(255),
                "DIEN_GIAI_CHUNG"    VARCHAR(255),
                "TK_CONG_NO"         VARCHAR(20),
                "TK_DOI_UNG"         VARCHAR(20),
                "SO_TIEN_NO"         DECIMAL(18, 4),
                "SO_TIEN_CO"         DECIMAL(18, 4),

                "SortDetailOrder"    INT,
                "NGAY_CAN_CU"        TIMESTAMP,
                "TK_CONG_NO_ID"      INT,
                "TK_DOI_UNG_ID"      INT,
                "KHOAN_MUC_CP_ID"    INT,
                "MA_KHOAN_MUC_CP"    VARCHAR(20),
                "TEN_KHOAN_MUC_CP"   VARCHAR(255)


            )
            ;

            INSERT INTO TMP_CHUNG_TU
                SELECT
                    GL."DOI_TUONG_THCP_ID"
                    , J."MA_DOI_TUONG_THCP"
                    , J."TEN_DOI_TUONG_THCP"
                    , J."MA_PHAN_CAP"
                    , GL."ID_CHUNG_TU"
                    , GL."MODEL_CHUNG_TU"
                    , GL."NGAY_HACH_TOAN"
                    , GL."NGAY_CHUNG_TU"
                    , GL."SO_CHUNG_TU"
                    , GL."LOAI_CHUNG_TU"
                    , GL."NGAY_HOA_DON"
                    , GL."SO_HOA_DON"
                    , GL."DIEN_GIAI"
                    , GL."DIEN_GIAI_CHUNG"
                    , A."SO_TAI_KHOAN"
                    , GL."MA_TAI_KHOAN_DOI_UNG"
                    , GL."GHI_NO"
                    , GL."GHI_CO"

                    , GL."THU_TU_TRONG_CHUNG_TU"
                    , GL."NGAY_HACH_TOAN" AS "NGAY_CAN_CU"
                    , A."TAI_KHOAN_ID"
                    , GL."TAI_KHOAN_DOI_UNG_ID"
                    , GL."KHOAN_MUC_CP_ID"
                    , EI."MA_KHOAN_MUC_CP"
                    , EI."TEN_KHOAN_MUC_CP"


                FROM so_cai_chi_tiet GL
                    INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                    INNER JOIN TMP_SO_TAI_KHOAN A ON GL."MA_TAI_KHOAN" LIKE A."AccountNumberPercent"
                    INNER JOIN TMP_DS_DOI_TUONG_THCP J ON J."DOI_TUONG_THCP_ID" = GL."DOI_TUONG_THCP_ID"
                    LEFT JOIN danh_muc_khoan_muc_cp EI ON GL."KHOAN_MUC_CP_ID" = EI.id

                WHERE GL."NGAY_HACH_TOAN" <= den_ngay
                    AND (GL."LOAI_CHUNG_TU" <> '610' OR (GL."LOAI_CHUNG_TU" = '610' AND GL."MA_TAI_KHOAN" NOT LIKE '154%%'))

                UNION ALL
                -- QĐ 48 thì phân bổ chi phí cho bao giờ cũng phân bổ vào tài khoản 154 ( nhưng trong bảng Phân bổ chi phí không lưu lại tài khoản) -> khi lấy phát sinh theo đối tượng THCP thì luôn lấy vào tiết khoản đầu tiên
                SELECT
                    JCCAD."MA_DOI_TUONG_THCP_ID"
                    , J."MA_DOI_TUONG_THCP"
                    , J."TEN_DOI_TUONG_THCP"
                    , J."MA_PHAN_CAP"
                    , NULL                                "ID_CHUNG_TU"
                    , NULL                                "MODEL_CHUNG_TU"
                    , JCP."DEN_NGAY"                      "NGAY_HACH_TOAN"
                    , NULL                                "NGAY_CHUNG_TU"
                    , NULL                                "SO_CHUNG_TU"
                    , NULL                                "LOAI_CHUNG_TU"
                    , NULL                                "NGAY_HOA_DON"
                    , NULL                                "SO_HOA_DON"
                    , 'Phân bổ chi phí sản xuất chung' AS "DIEN_GIAI"
                    , 'Phân bổ chi phí sản xuất chung' AS "DIEN_GIAI_CHUNG"
                    , SO_TK_154
                    , NULL                                "TK_DOI_UNG"
                    , JCCAD."SO_TIEN"                  AS "SO_TIEN_NO"
                    , 0                                AS "SO_TIEN_CO"

                    , 0                                   SortDetailOrder
                    , JCP."DEN_NGAY"                      "NGAY_CAN_CU"
                    , TAI_KHOAN_ID_154
                    , NULL
                    , JCCAD."KHOAN_MUC_CP_ID"
                    , EI."MA_KHOAN_MUC_CP"
                    , EI."TEN_KHOAN_MUC_CP"

                FROM gia_thanh_ky_tinh_gia_thanh JCP
                    INNER JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung JCCAD ON JCCAD."KY_TINH_GIA_THANH_ID" = JCP."id"

                    INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCP."CHI_NHANH_ID"
                    INNER JOIN TMP_DS_DOI_TUONG_THCP J ON J."DOI_TUONG_THCP_ID" = JCCAD."MA_DOI_TUONG_THCP_ID"
                    LEFT JOIN danh_muc_khoan_muc_cp EI ON JCCAD."KHOAN_MUC_CP_ID" = EI.id

                WHERE JCP."DEN_NGAY" <= den_ngay AND CHE_DO_KE_TOAN = '48' AND EXISTS(SELECT "SO_TAI_KHOAN"
                                                                                    FROM TMP_SO_TAI_KHOAN
                                                                                    WHERE "SO_TAI_KHOAN" LIKE '154%%')

                UNION ALL
                -- Case riêng TH lấy số liệu phân bổ chi phí chung cho QĐ 15
                SELECT
                    JCCAD."MA_DOI_TUONG_THCP_ID"
                    , J."MA_DOI_TUONG_THCP"
                    , J."TEN_DOI_TUONG_THCP"
                    , J."MA_PHAN_CAP"
                    , NULL                                "ID_CHUNG_TU"
                    , NULL                                "MODEL_CHUNG_TU"
                    , JCP."DEN_NGAY"                      "NGAY_HACH_TOAN"
                    , NULL                                "NGAY_CHUNG_TU"
                    , NULL                                "SO_CHUNG_TU"
                    , NULL                                "LOAI_CHUNG_TU"
                    , NULL                                "NGAY_HOA_DON"
                    , NULL                                "SO_HOA_DON"
                    , 'Phân bổ chi phí sản xuất chung' AS "DIEN_GIAI"
                    , 'Phân bổ chi phí sản xuất chung' AS "DIEN_GIAI_CHUNG"
                    , A."SO_TAI_KHOAN"
                    , NULL                                "TK_DOI_UNG"
                    , JCCAD."SO_TIEN"                  AS "SO_TIEN_NO"
                    , 0                                AS "SO_TIEN_CO"

                    , 0                                   SortDetailOrder
                    , JCP."DEN_NGAY"                      "NGAY_CAN_CU"
                    , A."TAI_KHOAN_ID"
                    , NULL
                    , JCCAD."KHOAN_MUC_CP_ID"
                    , EI."MA_KHOAN_MUC_CP"
                    , EI."TEN_KHOAN_MUC_CP"

                FROM gia_thanh_ky_tinh_gia_thanh JCP
                    INNER JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung JCCAD ON JCCAD."KY_TINH_GIA_THANH_ID" = JCP."id"

                    INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCP."CHI_NHANH_ID"
                    INNER JOIN TMP_DS_DOI_TUONG_THCP J ON J."DOI_TUONG_THCP_ID" = JCCAD."MA_DOI_TUONG_THCP_ID"
                    INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN"
                                                    FROM danh_muc_he_thong_tai_khoan TK
                                                    WHERE TK.id = JCCAD."TAI_KHOAN_ID") LIKE A."AccountNumberPercent"
                    LEFT JOIN danh_muc_khoan_muc_cp EI ON JCCAD."KHOAN_MUC_CP_ID" = EI.id

                WHERE JCP."DEN_NGAY" <= den_ngay AND CHE_DO_KE_TOAN = '15'


                UNION ALL
                SELECT
                    JC."MA_DOI_TUONG_THCP_ID"
                    , J."MA_DOI_TUONG_THCP"
                    , J."TEN_DOI_TUONG_THCP"
                    , J."MA_PHAN_CAP"
                    , NULL                           "ID_CHUNG_TU"
                    , NULL                           "MODEL_CHUNG_TU"
                    , NULL                           "NGAY_HACH_TOAN"
                    , NULL                           "NGAY_CHUNG_TU"
                    , NULL                           "SO_CHUNG_TU"
                    , NULL                           "LOAI_CHUNG_TU"
                    , NULL                           "NGAY_HOA_DON"
                    , NULL                           "SO_HOA_DON"
                    , 'Chi phí dở dang'           AS "DIEN_GIAI"
                    , 'Chi phí dở dang'           AS "DIEN_GIAI_CHUNG"
                    , --HHSon 14.08.2015: lấy thêm Diễn giải chung (phân bổ CP sx chung thì fix diễn giải)
                    A."SO_TAI_KHOAN"
                    , NULL                           "TK_DOI_UNG"
                    , JC."TONG_CHI_PHI"              "SO_TIEN_NO"
                    , 0                              "SO_TIEN_CO"

                    , 0                              SortDetailOrder
                    , tu_ngay + INTERVAL '-1 day' AS "NGAY_CAN_CU"
                    , A."TAI_KHOAN_ID"
                    , NULL
                    , NULL :: INT
                    , NULL
                    , NULL


                FROM account_ex_chi_phi_do_dang JC
                    INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JC."CHI_NHANH_ID"
                    INNER JOIN TMP_DS_DOI_TUONG_THCP J ON J."DOI_TUONG_THCP_ID" = JC."MA_DOI_TUONG_THCP_ID"
                    INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN"
                                                    FROM danh_muc_he_thong_tai_khoan TK
                                                    WHERE TK.id = JC."TAI_KHOAN_CPSXKD_DO_DANG_ID") LIKE
                                                    A."AccountNumberPercent"

            ;


            DROP TABLE IF EXISTS TMP_KET_QUA
            ;

            CREATE TEMP TABLE TMP_KET_QUA
                AS
                    SELECT
                        ROW_NUMBER()
                        OVER (
                            ORDER BY "MA_DOI_TUONG_THCP", "TK_CONG_NO", "STT", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU",
                                SortDetailOrder ) AS RowNum
                        , *
                    FROM (
                            SELECT
                                J."DOI_TUONG_THCP_ID"
                                , J."MA_DOI_TUONG_THCP"
                                , J."TEN_DOI_TUONG_THCP"
                                , NULL           "ID_CHUNG_TU"
                                , NULL           "MODEL_CHUNG_TU"
                                , NULL           "NGAY_HACH_TOAN"
                                , NULL           "NGAY_CHUNG_TU"
                                , NULL           "SO_CHUNG_TU"
                                , NULL           "LOAI_CHUNG_TU"
                                , NULL           "NGAY_HOA_DON"
                                , NULL           "SO_HOA_DON"
                                , 'Số dư đầu kỳ' "DIEN_GIAI"
                                , NULL AS        "DIEN_GIAI_CHUNG"
                                , -- Đầu kỳ thì để trống
                                "TK_CONG_NO"
                                , NULL           "TK_DOI_UNG"
                                , CASE WHEN SUM("SO_TIEN_NO" - "SO_TIEN_CO") > 0
                                THEN SUM("SO_TIEN_NO" - "SO_TIEN_CO")
                                ELSE 0
                                END            "SO_TIEN_NO"
                                , CASE WHEN SUM("SO_TIEN_NO" - "SO_TIEN_CO") < 0
                                THEN SUM("SO_TIEN_CO" - "SO_TIEN_NO")
                                ELSE 0
                                END            "SO_TIEN_CO"

                                , 0              SortDetailOrder

                                , 0              "STT"
                                , "TK_CONG_NO_ID"
                                , NULL AS        "TK_DOI_UNG_ID"
                                , "KHOAN_MUC_CP_ID"
                                , "MA_KHOAN_MUC_CP"
                                , "TEN_KHOAN_MUC_CP"

                            FROM TMP_CHUNG_TU V
                                INNER JOIN TMP_DOI_TUONG_THCP J ON V."MA_PHAN_CAP" LIKE J."MA_PHAN_CAP"
                                                                                        || '%%'
                            WHERE "NGAY_CAN_CU" < tu_ngay
                            GROUP BY
                                J."DOI_TUONG_THCP_ID",
                                J."MA_DOI_TUONG_THCP",
                                J."TEN_DOI_TUONG_THCP",
                                "TK_CONG_NO",
                                "TK_CONG_NO_ID",
                                "KHOAN_MUC_CP_ID",
                                "MA_KHOAN_MUC_CP",
                                "TEN_KHOAN_MUC_CP"
                            HAVING SUM("SO_TIEN_NO" - "SO_TIEN_CO") <> 0

                            UNION ALL

                            SELECT
                                J."DOI_TUONG_THCP_ID"
                                , J."MA_DOI_TUONG_THCP"
                                , J."TEN_DOI_TUONG_THCP"
                                , "ID_CHUNG_TU"
                                , "MODEL_CHUNG_TU"
                                , "NGAY_HACH_TOAN"
                                , "NGAY_CHUNG_TU"
                                , "SO_CHUNG_TU"
                                , "LOAI_CHUNG_TU"
                                , "NGAY_HOA_DON"
                                , "SO_HOA_DON"
                                , "DIEN_GIAI"
                                , "DIEN_GIAI_CHUNG"
                                , "TK_CONG_NO"
                                , "TK_DOI_UNG"
                                , SUM("SO_TIEN_NO") "SO_TIEN_NO"
                                , SUM("SO_TIEN_CO") "SO_TIEN_CO"

                                , "SortDetailOrder"

                                , 1                 "STT"
                                , "TK_CONG_NO_ID"
                                , "TK_DOI_UNG_ID"
                                , "KHOAN_MUC_CP_ID"
                                , "MA_KHOAN_MUC_CP"
                                , "TEN_KHOAN_MUC_CP"

                            FROM TMP_CHUNG_TU V
                                INNER JOIN TMP_DOI_TUONG_THCP J ON V."MA_PHAN_CAP" LIKE J."MA_PHAN_CAP"
                                                                                        || '%%'
                            WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                            GROUP BY J."DOI_TUONG_THCP_ID",
                                J."MA_DOI_TUONG_THCP",
                                J."TEN_DOI_TUONG_THCP",
                                "ID_CHUNG_TU",
                                "MODEL_CHUNG_TU",
                                "NGAY_HACH_TOAN",
                                "NGAY_CHUNG_TU",
                                "SO_CHUNG_TU",
                                "LOAI_CHUNG_TU",
                                "NGAY_HOA_DON",
                                "SO_HOA_DON",
                                "DIEN_GIAI",
                                "DIEN_GIAI_CHUNG",
                                "TK_CONG_NO",
                                "TK_DOI_UNG",

                                "SortDetailOrder",
                                "TK_CONG_NO_ID",
                                "TK_DOI_UNG_ID",
                                "KHOAN_MUC_CP_ID",
                                "MA_KHOAN_MUC_CP",
                                "TEN_KHOAN_MUC_CP"

                            HAVING (SUM("SO_TIEN_NO") <> 0
                                    OR SUM("SO_TIEN_CO") <> 0
                            )

                            UNION ALL

                            SELECT
                                J."DOI_TUONG_THCP_ID"
                                , J."MA_DOI_TUONG_THCP"
                                , J."TEN_DOI_TUONG_THCP"
                                , NULL              "ID_CHUNG_TU"
                                , NULL              RefDetailID
                                , NULL              "NGAY_HACH_TOAN"
                                , NULL              "NGAY_CHUNG_TU"
                                , NULL              "SO_CHUNG_TU"
                                , NULL              "LOAI_CHUNG_TU"
                                , NULL              "NGAY_HOA_DON"
                                , NULL              "SO_HOA_DON"
                                , 'Cộng phát sinh'  "DIEN_GIAI"
                                , NULL        AS    "DIEN_GIAI_CHUNG"
                                , "TK_CONG_NO"
                                , NULL              "TK_DOI_UNG"
                                , SUM("SO_TIEN_NO") "SO_TIEN_NO"
                                , SUM("SO_TIEN_CO") "SO_TIEN_CO"

                                , 0                 SortDetailOrder

                                , 2                 "STT"
                                , "TK_CONG_NO_ID"
                                , NULL              "TK_DOI_UNG_ID"
                                , NULL :: INT AS    "KHOAN_MUC_CP_ID"
                                , NULL        AS    "MA_KHOAN_MUC_CP"
                                , NULL        AS    "TEN_KHOAN_MUC_CP"

                            FROM TMP_CHUNG_TU V
                                INNER JOIN TMP_DOI_TUONG_THCP J ON V."MA_PHAN_CAP" LIKE J."MA_PHAN_CAP"
                                                                                        || '%%'
                            WHERE "NGAY_CAN_CU" BETWEEN tu_ngay AND den_ngay
                            GROUP BY J."DOI_TUONG_THCP_ID",
                                J."MA_DOI_TUONG_THCP",
                                J."TEN_DOI_TUONG_THCP",
                                "TK_CONG_NO",
                                "TK_CONG_NO_ID"

                            HAVING (SUM("SO_TIEN_NO") <> 0
                                    OR SUM("SO_TIEN_CO") <> 0
                            )

                            UNION ALL

                            SELECT
                                J."DOI_TUONG_THCP_ID"
                                , J."MA_DOI_TUONG_THCP"
                                , J."TEN_DOI_TUONG_THCP"
                                , NULL            "ID_CHUNG_TU"
                                , NULL            "MODEL_CHUNG_TU"
                                , NULL            "NGAY_HACH_TOAN"
                                , NULL            "NGAY_CHUNG_TU"
                                , NULL            "SO_CHUNG_TU"
                                , NULL            "LOAI_CHUNG_TU"
                                , NULL            "NGAY_HOA_DON"
                                , NULL            "SO_HOA_DON"
                                , 'Số dư cuối kỳ' "DIEN_GIAI"
                                , NULL        AS  "DIEN_GIAI_CHUNG"
                                , "TK_CONG_NO"
                                , NULL            "TK_DOI_UNG"
                                , CASE WHEN SUM("SO_TIEN_NO" - "SO_TIEN_CO") > 0
                                THEN SUM("SO_TIEN_NO" - "SO_TIEN_CO")
                                ELSE 0
                                END             "SO_TIEN_NO"
                                , CASE WHEN SUM("SO_TIEN_NO" - "SO_TIEN_CO") < 0
                                THEN SUM("SO_TIEN_CO" - "SO_TIEN_NO")
                                ELSE 0
                                END             "SO_TIEN_CO"

                                , 0               SortDetailOrder

                                , 3               "STT"
                                , "TK_CONG_NO_ID"
                                , NULL            "TK_DOI_UNG_ID"
                                , NULL :: INT AS  "KHOAN_MUC_CP_ID"
                                , NULL        AS  "MA_KHOAN_MUC_CP"
                                , NULL        AS  "TEN_KHOAN_MUC_CP"

                            FROM TMP_CHUNG_TU V
                                INNER JOIN TMP_DOI_TUONG_THCP J ON V."MA_PHAN_CAP" LIKE J."MA_PHAN_CAP"
                                                                                        || '%%'
                            WHERE "NGAY_CAN_CU" <= den_ngay
                            GROUP BY J."DOI_TUONG_THCP_ID",
                                J."MA_DOI_TUONG_THCP",
                                J."TEN_DOI_TUONG_THCP",
                                "TK_CONG_NO",
                                "TK_CONG_NO_ID"

                            HAVING SUM("SO_TIEN_NO" - "SO_TIEN_CO") <> 0

                        ) tbl

            ;

        END $$
        ;

            SELECT 
            "TEN_DOI_TUONG_THCP" AS "TEN_DOI_TUONG_THCP",
            "TK_CONG_NO" AS "SO_TAI_KHOAN",
            "NGAY_HACH_TOAN" AS "NGAY_HACH_TOAN",
            "NGAY_CHUNG_TU" AS "NGAY_CHUNG_TU",
            "SO_CHUNG_TU" AS "SO_CHUNG_TU",
            "DIEN_GIAI" AS "DIEN_GIAI",
            "TK_DOI_UNG" AS "TK_DOI_UNG",
            "SO_TIEN_NO" AS "SO_TIEN_NO",
            "SO_TIEN_CO" AS "SO_TIEN_CO",
            "ID_CHUNG_TU" as "ID_GOC",
            "MODEL_CHUNG_TU" as "MODEL_GOC"

            FROM TMP_KET_QUA
            ORDER BY RowNum

            OFFSET %(offset)s
            LIMIT %(limit)s;
            """
        return self.execute(query,params_sql)

    #  Thống kê theo công trình
    def _lay_bao_cao_cong_trinh(self, params_sql):      
        record = []
        query = """
            DO LANGUAGE plpgsql $$
            DECLARE
             tu_ngay                             TIMESTAMP :=  %(TU_NGAY)s;

            den_ngay                            TIMESTAMP :=  %(DEN_NGAY)s;

            bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER :=  %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

            chi_nhanh_id                        INTEGER :=  %(CHI_NHANH_ID)s;

            TON_TAI_TK_154                      BOOLEAN;

            SO_TK_154                           VARCHAR;


            TAI_KHOAN_ID_154                    INTEGER;

            CHE_DO_KE_TOAN                      VARCHAR;

            rec                                 RECORD;

            --@ListProjectWorkID --Tham số bên misa
            --@ListAccountID ----Tham số bên misa


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


            DROP TABLE IF EXISTS TMP_TAI_KHOAN_DUOC_CHON
            ;

            CREATE TEMP TABLE TMP_TAI_KHOAN_DUOC_CHON
            -- Bảng các tài khoản được chọn
            (
            "TK_CONG_NO_ID"  INT,
            "TK_CONG_NO"     VARCHAR(20) PRIMARY KEY,
            "TEN_TK_DOI_UNG" VARCHAR(255)
            )
            ;

            INSERT INTO TMP_TAI_KHOAN_DUOC_CHON
            SELECT
            A.id
            , A."SO_TAI_KHOAN"
            , A."TEN_TAI_KHOAN"
            FROM danh_muc_he_thong_tai_khoan A
            WHERE A."id" = any (%(TAI_KHOAN_IDS)s) --@ListAccountID
            ;

            DROP TABLE IF EXISTS TMP_SO_TAI_KHOAN
            ;

            CREATE TEMP TABLE TMP_SO_TAI_KHOAN
            -- Lấy các tài khoản cha nhất để đối chiếu
            (

            "TAI_KHOAN_ID"            INT,
            "SO_TAI_KHOAN"            VARCHAR(20) PRIMARY KEY,
            "TEN_TAI_KHOAN"           VARCHAR(255),
            "AccountNumberPercent"    VARCHAR(25),
            "CHI_TIET_THEO_DOI_TUONG" VARCHAR(25)
            )
            ;

            SELECT "SO_TAI_KHOAN"
            INTO SO_TK_154
            FROM danh_muc_he_thong_tai_khoan
            WHERE "SO_TAI_KHOAN" LIKE '154%%' AND "LA_TK_TONG_HOP" = FALSE
            ORDER BY "SO_TAI_KHOAN"
            LIMIT 1
            ;

            SELECT "id"
            INTO TAI_KHOAN_ID_154
            FROM danh_muc_he_thong_tai_khoan
            WHERE "SO_TAI_KHOAN" LIKE '154%%' AND "LA_TK_TONG_HOP" = FALSE
            ORDER BY "SO_TAI_KHOAN"
            LIMIT 1
            ;


            INSERT INTO TMP_SO_TAI_KHOAN
            SELECT DISTINCT
            SA."id"
            , SA."SO_TAI_KHOAN"
            , SA."TEN_TAI_KHOAN"
            , SA."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
            , SA."CHI_TIET_THEO_DOI_TUONG"
            FROM danh_muc_he_thong_tai_khoan SA
            INNER JOIN TMP_TAI_KHOAN_DUOC_CHON SAD ON SA."SO_TAI_KHOAN" LIKE SAD."TK_CONG_NO"
            || '%%'
            WHERE sa."LA_TK_TONG_HOP" = FALSE
            ;


            DROP TABLE IF EXISTS TMP_CONG_TRINH
            ;

            CREATE TEMP TABLE TMP_CONG_TRINH

            -- Bảng công trình
            (
            "CONG_TRINH_ID"   INT PRIMARY KEY,
            "MA_CONG_TRINH"   VARCHAR(20),
            "TEN_CONG_TRINH"  VARCHAR(128),
            "LOAI_CONG_TRINH" INT,
            "MA_PHAN_CAP"     VARCHAR(100)
            )
            ;

            INSERT INTO TMP_CONG_TRINH
            SELECT
            PW."id"
            , PW."MA_CONG_TRINH"
            , PW."TEN_CONG_TRINH"
            , PW."LOAI_CONG_TRINH"
            , PW."MA_PHAN_CAP"
            FROM
            danh_muc_cong_trinh PW
            WHERE PW."id" = any (%(CONG_TRINH_IDS)s) --@ListProjectWorkID
            ;

            DROP TABLE IF EXISTS TMP_DS_CONG_TRINH
            ;

            CREATE TEMP TABLE TMP_DS_CONG_TRINH

            -- Bảng công trình gồm toàn bộ công trình con
            (
            "CONG_TRINH_ID"  INT PRIMARY KEY,
            "MA_CONG_TRINH"  VARCHAR(20),
            "TEN_CONG_TRINH" VARCHAR(128),
            "MA_PHAN_CAP"    VARCHAR(100)
            )
            ;

            INSERT INTO TMP_DS_CONG_TRINH
            SELECT
            PW."id"
            , PW."MA_CONG_TRINH"
            , PW."TEN_CONG_TRINH"
            , PW."MA_PHAN_CAP"
            FROM TMP_CONG_TRINH tPW
            INNER JOIN danh_muc_cong_trinh PW ON PW."MA_PHAN_CAP" LIKE tPW."MA_PHAN_CAP"
            || '%%'
            GROUP BY PW."id",
            PW."MA_CONG_TRINH",
            PW."TEN_CONG_TRINH",
            PW."MA_PHAN_CAP"
            ;

            DROP TABLE IF EXISTS TMP_CHUNG_TU
            ;

            CREATE TEMP TABLE TMP_CHUNG_TU

            (
            "CONG_TRINH_ID"   INT,
            "MA_CONG_TRINH"   VARCHAR(25),
            "TEN_CONG_TRINH"  VARCHAR(128),
            "MA_PHAN_CAP"     VARCHAR(100),
            "ID_CHUNG_TU"     INT,
            "MODEL_CHUNG_TU"  VARCHAR(100),
            "NGAY_HACH_TOAN"  TIMESTAMP,
            "NGAY_CHUNG_TU"   TIMESTAMP,
            "SO_CHUNG_TU"     VARCHAR(20),
            "LOAI_CHUNG_TU"   VARCHAR(500),
            "NGAY_HOA_DON"    TIMESTAMP,
            "SO_HOA_DON"      VARCHAR(500),
            "DIEN_GIAI"       VARCHAR(255),
            "DIEN_GIAI_CHUNG" VARCHAR(255),
            "TK_CONG_NO"      VARCHAR(20),
            "TK_DOI_UNG"      VARCHAR(20),
            "SO_TIEN_NO"      DECIMAL(18, 4),
            "SO_TIEN_CO"      DECIMAL(18, 4),

            "SortDetailOrder" INT,
            "NGAY_CAN_CU"     TIMESTAMP,
            "TK_CONG_NO_ID"   INT,
            "TK_DOI_UNG_ID"   INT


            )
            ;

            INSERT INTO TMP_CHUNG_TU
            SELECT
            GL."CONG_TRINH_ID"
            , PW."MA_CONG_TRINH"
            , PW."TEN_CONG_TRINH"
            , PW."MA_PHAN_CAP"
            , GL."ID_CHUNG_TU"
            , GL."MODEL_CHUNG_TU"
            , GL."NGAY_HACH_TOAN"
            , GL."NGAY_CHUNG_TU"
            , GL."SO_CHUNG_TU"
            , GL."LOAI_CHUNG_TU"
            , GL."NGAY_HOA_DON"
            , GL."SO_HOA_DON"
            , GL."DIEN_GIAI"
            , GL."DIEN_GIAI_CHUNG"
            , A."SO_TAI_KHOAN"
            , GL."MA_TAI_KHOAN_DOI_UNG"
            , GL."GHI_NO"
            , GL."GHI_CO"

            , GL."THU_TU_TRONG_CHUNG_TU"
            , GL."NGAY_HACH_TOAN" "NGAY_CAN_CU"
            , A."TAI_KHOAN_ID"
            , GL."TAI_KHOAN_DOI_UNG_ID"

            FROM so_cai_chi_tiet GL
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON GL."MA_TAI_KHOAN" LIKE A."AccountNumberPercent"
            INNER JOIN TMP_DS_CONG_TRINH PW ON PW."CONG_TRINH_ID" = GL."CONG_TRINH_ID"

            LEFT JOIN danh_muc_khoan_muc_cp EI ON EI."id" = GL."KHOAN_MUC_CP_ID"
            WHERE GL."NGAY_HACH_TOAN" <= den_ngay
            AND (GL."LOAI_CHUNG_TU" <> '610' OR (GL."LOAI_CHUNG_TU" = '610' AND GL."MA_TAI_KHOAN" NOT LIKE
            N'154%%')) -- ntquang 30/08/2017 - không lấy phát sinh của tk 154 ở số dư đầu kỳ
            UNION ALL
            SELECT
            JCCAD."MA_CONG_TRINH_ID"
            , PW."MA_CONG_TRINH"
            , PW."TEN_CONG_TRINH"
            , --  PWC."LOAI_CONG_TRINH"
            PW."MA_PHAN_CAP"
            , NULL                                  "ID_CHUNG_TU"
            , NULL                                  "MODEL_CHUNG_TU"
            , JCP."DEN_NGAY"                        "NGAY_HACH_TOAN"
            , NULL                                  "NGAY_CHUNG_TU"
            , NULL                                  "SO_CHUNG_TU"
            , NULL                                  "LOAI_CHUNG_TU"
            , NULL                                  "NGAY_HOA_DON"
            , NULL                                  "SO_HOA_DON"
            , N'Phân bổ chi phí sản xuất chung' AS "DIEN_GIAI"
            , N'Phân bổ chi phí sản xuất chung' AS "DIEN_GIAI_CHUNG"
            , A."SO_TAI_KHOAN"
            , NULL                                  "TK_DOI_UNG"
            , JCCAD."SO_TIEN"                       "SO_TIEN_NO"
            , 0                                     "SO_TIEN_CO"

            , 0                                     SortDetailOrer
            , JCP."DEN_NGAY"                        "NGAY_CAN_CU"
            , A."TAI_KHOAN_ID"
            , NULL                                  "TK_DOI_UNG_ID"

            FROM gia_thanh_ky_tinh_gia_thanh JCP
            INNER JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung JCCAD ON JCCAD."KY_TINH_GIA_THANH_ID" = JCP."id"

            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCP."CHI_NHANH_ID"
            INNER JOIN TMP_DS_CONG_TRINH PW ON PW."CONG_TRINH_ID" = JCCAD."MA_CONG_TRINH_ID"

            INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN"
            FROM danh_muc_he_thong_tai_khoan TK
            WHERE TK.id = JCCAD."TAI_KHOAN_ID") LIKE A."AccountNumberPercent"
            LEFT JOIN danh_muc_khoan_muc_cp EI ON EI."id" = JCCAD."KHOAN_MUC_CP_ID"
            WHERE JCP."DEN_NGAY" <= den_ngay
            AND CHE_DO_KE_TOAN = '15'

            UNION ALL
            SELECT
            JCCAD."MA_CONG_TRINH_ID"
            , PW."MA_CONG_TRINH"
            , PW."TEN_CONG_TRINH"
            , --  PWC."LOAI_CONG_TRINH",
            PW."MA_PHAN_CAP"
            , NULL                                  "ID_CHUNG_TU"
            , NULL                                  "MODEL_CHUNG_TU"
            , JCP."DEN_NGAY"                        "NGAY_HACH_TOAN"
            , NULL                                  "NGAY_CHUNG_TU"
            , NULL                                  "SO_CHUNG_TU"
            , NULL                                  "LOAI_CHUNG_TU"
            , NULL                                  "NGAY_HOA_DON"
            , NULL                                  "SO_HOA_DON"
            , N'Phân bổ chi phí sản xuất chung'    "DIEN_GIAI"
            , N'Phân bổ chi phí sản xuất chung' AS "DIEN_GIAI_CHUNG"
            , SO_TK_154
            , NULL                                  "TK_DOI_UNG"
            , JCCAD."SO_TIEN"                       "SO_TIEN_NO"
            , 0                                     "SO_TIEN_CO"

            , 0                                     SortDetailOrer
            , JCP."DEN_NGAY"                        "NGAY_CAN_CU"
            , TAI_KHOAN_ID_154
            , NULL                                  "TK_DOI_UNG_ID"
            FROM gia_thanh_ky_tinh_gia_thanh JCP
            INNER JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung JCCAD ON JCCAD."KY_TINH_GIA_THANH_ID" = JCP."id"

            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCP."CHI_NHANH_ID"
            INNER JOIN TMP_DS_CONG_TRINH PW ON PW."CONG_TRINH_ID" = JCCAD."MA_CONG_TRINH_ID"

            LEFT JOIN danh_muc_khoan_muc_cp EI ON EI."id" = JCCAD."KHOAN_MUC_CP_ID"
            WHERE JCP."DEN_NGAY" <= den_ngay
            AND CHE_DO_KE_TOAN = '48'
            AND EXISTS(SELECT "SO_TAI_KHOAN"
            FROM TMP_SO_TAI_KHOAN
            WHERE "SO_TAI_KHOAN" LIKE '154%%')

            UNION ALL
            SELECT
            JCAEDT."MA_DON_VI_ID" AS "CONG_TRINH_ID"
            , PW."MA_CONG_TRINH"
            , PW."TEN_CONG_TRINH"
            , -- PWC."LOAI_CONG_TRINH",
            PW."MA_PHAN_CAP"
            , JCAE."id"
            , NULL                     "MODEL_CHUNG_TU"
            , JCAE."NGAY_CHUNG_TU"     "NGAY_HACH_TOAN"
            , JCAE."NGAY_CHUNG_TU"
            , JCAE."SO_CHUNG_TU"
            , CAST(JCAE."LOAI_CHUNG_TU" AS VARCHAR(255))
            , NULL                     "NGAY_HOA_DON"
            , NULL                     "SO_HOA_DON"
            , JCAE."DIEN_GIAI"         "DIEN_GIAI"
            , JCAE."DIEN_GIAI"      AS "DIEN_GIAI_CHUNG"
            , A."SO_TAI_KHOAN"
            , NULL                     "TK_DOI_UNG"
            , JCAEDT."SO_TIEN"         "SO_TIEN_NO"
            , 0                        "SO_TIEN_CO"

            , 0                        SortDetailOrder
            , JCAE."NGAY_CHUNG_TU"     "NGAY_CAN_CU"
            , A."TAI_KHOAN_ID"
            , NULL                     "TK_DOI_UNG_ID"

            FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JCAE
            INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCAEDT
            ON JCAEDT."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JCAE."id"
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCAE."CHI_NHANH_ID"
            INNER JOIN TMP_DS_CONG_TRINH PW ON PW."CONG_TRINH_ID" = JCAEDT."MA_DON_VI_ID"

            INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN"
            FROM danh_muc_he_thong_tai_khoan TK
            WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE A."AccountNumberPercent"
            INNER JOIN danh_muc_reftype SYSRT ON SYSRT."REFTYPE" = JCAE."LOAI_CHUNG_TU"
            WHERE JCAE."NGAY_CHUNG_TU" <= den_ngay
            AND JCAEDT."CAP_TO_CHUC" = '1'

            UNION ALL
            SELECT
            JC."MA_CONG_TRINH_ID"
            , PW."MA_CONG_TRINH"
            , PW."TEN_CONG_TRINH"
            , --   PWC."LOAI_CONG_TRINH",
            PW."MA_PHAN_CAP"
            , NULL                           "ID_CHUNG_TU"
            , NULL                           "MODEL_CHUNG_TU"
            , NULL                           "NGAY_HACH_TOAN"
            , NULL                           "NGAY_CHUNG_TU"
            , NULL                           "SO_CHUNG_TU"
            , NULL                           "LOAI_CHUNG_TU"
            , NULL                           "NGAY_HOA_DON"
            , NULL                           "SO_HOA_DON"
            , N'Chi phí dở dang'            "DIEN_GIAI"
            , N'Chi phí dở dang'         AS "DIEN_GIAI_CHUNG"
            , A."SO_TAI_KHOAN"
            , NULL                           "TK_DOI_UNG"
            , JC."SO_CHUA_NGHIEM_THU"        "SO_TIEN_NO"
            , 0                              "SO_TIEN_CO"

            , 0                              SortDetailOrder
            , tu_ngay + INTERVAL '-1 day' AS "NGAY_CAN_CU"
            , A."TAI_KHOAN_ID"
            , NULL                           "TK_DOI_UNG_ID"

            FROM account_ex_chi_phi_do_dang JC
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JC."CHI_NHANH_ID"
            INNER JOIN TMP_DS_CONG_TRINH PW ON PW."CONG_TRINH_ID" = JC."MA_CONG_TRINH_ID"

            INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN"
            FROM danh_muc_he_thong_tai_khoan TK
            WHERE TK.id = JC."TAI_KHOAN_CPSXKD_DO_DANG_ID") LIKE
            A."AccountNumberPercent"
            ;


            DROP TABLE IF EXISTS TMP_KET_QUA
            ;

            CREATE TEMP TABLE TMP_KET_QUA
            AS

            SELECT
            ROW_NUMBER()
            OVER (
            ORDER BY "MA_CONG_TRINH", "TK_CONG_NO", "STT", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU",
            SortDetailOrder ) AS RowNum
            , *
            FROM (SELECT
            PW."CONG_TRINH_ID"
            , PW."MA_CONG_TRINH"
            , PW."TEN_CONG_TRINH"
            , PWC."name" AS "LOAI_CONG_TRINH"
            , NULL             "ID_CHUNG_TU"
            , NULL             "MODEL_CHUNG_TU"
            , NULL             "NGAY_HACH_TOAN"
            , NULL             "NGAY_CHUNG_TU"
            , NULL             "SO_CHUNG_TU"
            , NULL             "LOAI_CHUNG_TU"
            , NULL             "NGAY_HOA_DON"
            , NULL             "SO_HOA_DON"
            , N'Số dư đầu kỳ' "DIEN_GIAI"
            , NULL AS          "DIEN_GIAI_CHUNG"
            , "TK_CONG_NO"
            , NULL             "TK_DOI_UNG"
            , CASE WHEN SUM("SO_TIEN_NO" - "SO_TIEN_CO") > 0
            THEN SUM("SO_TIEN_NO" - "SO_TIEN_CO")
            ELSE 0
            END              "SO_TIEN_NO"
            , CASE WHEN SUM("SO_TIEN_NO" - "SO_TIEN_CO") < 0
            THEN SUM("SO_TIEN_CO" - "SO_TIEN_NO")
            ELSE 0
            END              "SO_TIEN_CO"

            , 0                SortDetailOrder

            , 0                "STT"
            , "TK_CONG_NO_ID"
            , NULL             "TK_DOI_UNG_ID"

            FROM TMP_CHUNG_TU V
            INNER JOIN TMP_CONG_TRINH PW ON V."MA_PHAN_CAP" LIKE PW."MA_PHAN_CAP"
            || '%%'
            LEFT JOIN danh_muc_loai_cong_trinh AS PWC ON PW."LOAI_CONG_TRINH" = PWC."id"
            WHERE "NGAY_CAN_CU" < tu_ngay
            GROUP BY PW."CONG_TRINH_ID",
            PW."MA_CONG_TRINH",
            PW."TEN_CONG_TRINH",
            PWc."name",
            "TK_CONG_NO",
            "TK_CONG_NO_ID"
            UNION ALL
            SELECT
            PW."CONG_TRINH_ID"
            , PW."MA_CONG_TRINH"
            , PW."TEN_CONG_TRINH"
            , PWC."name"
            , "ID_CHUNG_TU"
            , "MODEL_CHUNG_TU"
            , "NGAY_HACH_TOAN"
            , "NGAY_CHUNG_TU"
            , "SO_CHUNG_TU"
            , "LOAI_CHUNG_TU"
            , "NGAY_HOA_DON"
            , "SO_HOA_DON"
            , V."DIEN_GIAI"
            , "DIEN_GIAI_CHUNG"
            , "TK_CONG_NO"
            , "TK_DOI_UNG"
            , SUM("SO_TIEN_NO") "SO_TIEN_NO"
            , SUM("SO_TIEN_CO") "SO_TIEN_CO"

            , "SortDetailOrder"

            , 1                 "STT"
            , "TK_CONG_NO_ID"
            , "TK_DOI_UNG_ID"

            FROM TMP_CHUNG_TU V
            INNER JOIN TMP_CONG_TRINH PW ON V."MA_PHAN_CAP" LIKE PW."MA_PHAN_CAP"
            || '%%'
            LEFT JOIN danh_muc_loai_cong_trinh AS PWC ON PW."LOAI_CONG_TRINH" = PWC."id"
            WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            GROUP BY PW."CONG_TRINH_ID",
            PW."MA_CONG_TRINH",
            PW."TEN_CONG_TRINH",
            PWC."name",
            "ID_CHUNG_TU",
            "MODEL_CHUNG_TU",
            "NGAY_HACH_TOAN",
            "NGAY_CHUNG_TU",
            "SO_CHUNG_TU",
            "LOAI_CHUNG_TU",
            "NGAY_HOA_DON",
            "SO_HOA_DON",
            V."DIEN_GIAI",
            "DIEN_GIAI_CHUNG",
            "TK_CONG_NO",
            "TK_DOI_UNG",

            "SortDetailOrder",
            "TK_CONG_NO_ID",
            "TK_DOI_UNG_ID"


            UNION ALL
            SELECT
            PW."CONG_TRINH_ID"
            , PW."MA_CONG_TRINH"
            , PW."TEN_CONG_TRINH"
            , PWC."name"
            , NULL               "ID_CHUNG_TU"
            , NULL               "MODEL_CHUNG_TU"
            , NULL               "NGAY_HACH_TOAN"
            , NULL               "NGAY_CHUNG_TU"
            , NULL               "SO_CHUNG_TU"
            , NULL               "LOAI_CHUNG_TU"
            , NULL               "NGAY_HOA_DON"
            , NULL               "SO_HOA_DON"
            , N'Cộng phát sinh' "DIEN_GIAI"
            , NULL AS            "DIEN_GIAI_CHUNG"
            , "TK_CONG_NO"
            , NULL               "TK_DOI_UNG"
            , SUM("SO_TIEN_NO")  "SO_TIEN_NO"
            , SUM("SO_TIEN_CO")  "SO_TIEN_CO"

            , 0                  SortDetailOrder

            , 2                  "STT"
            , "TK_CONG_NO_ID"
            , NULL               "TK_DOI_UNG_ID"
            FROM TMP_CHUNG_TU V
            INNER JOIN TMP_CONG_TRINH PW ON V."MA_PHAN_CAP" LIKE PW."MA_PHAN_CAP"
            || '%%'
            LEFT JOIN danh_muc_loai_cong_trinh AS PWC ON PW."LOAI_CONG_TRINH" = PWC."id"
            WHERE "NGAY_CAN_CU" BETWEEN tu_ngay AND den_ngay
            GROUP BY PW."CONG_TRINH_ID",
            PW."MA_CONG_TRINH",
            PW."TEN_CONG_TRINH",
            PWC."name",
            "TK_CONG_NO",
            "TK_CONG_NO_ID"
            UNION ALL
            SELECT
            PW."CONG_TRINH_ID"
            , PW."MA_CONG_TRINH"
            , PW."TEN_CONG_TRINH"
            , PWC."name"
            , NULL              "ID_CHUNG_TU"
            , NULL              "MODEL_CHUNG_TU"
            , NULL              "NGAY_HACH_TOAN"
            , NULL              "NGAY_CHUNG_TU"
            , NULL              "SO_CHUNG_TU"
            , NULL              "LOAI_CHUNG_TU"
            , NULL              "NGAY_HOA_DON"
            , NULL              "SO_HOA_DON"
            , N'Số dư cuối kỳ' "DIEN_GIAI"
            , NULL AS           "DIEN_GIAI"
            , "TK_CONG_NO"
            , NULL              "TK_DOI_UNG"
            , CASE WHEN SUM("SO_TIEN_NO" - "SO_TIEN_CO") > 0
            THEN SUM("SO_TIEN_NO" - "SO_TIEN_CO")
            ELSE 0
            END               "SO_TIEN_NO"
            , CASE WHEN SUM("SO_TIEN_NO" - "SO_TIEN_CO") < 0
            THEN SUM("SO_TIEN_CO" - "SO_TIEN_NO")
            ELSE 0
            END               "SO_TIEN_CO"

            , 0                 SortDetailOrder

            , 3                 "STT"
            , "TK_CONG_NO_ID"
            , NULL              "TK_DOI_UNG_ID"
            FROM TMP_CHUNG_TU V
            INNER JOIN TMP_CONG_TRINH PW ON V."MA_PHAN_CAP" LIKE PW."MA_PHAN_CAP"
            || '%%'
            LEFT JOIN danh_muc_loai_cong_trinh AS PWC ON PW."LOAI_CONG_TRINH" = PWC."id"
            WHERE "NGAY_CAN_CU" <= den_ngay
            GROUP BY
            PW."CONG_TRINH_ID",
            PW."MA_CONG_TRINH",
            PW."TEN_CONG_TRINH",
            PWC."name",
            "TK_CONG_NO",
            "TK_CONG_NO_ID"
            ) tbl
            WHERE "SO_TIEN_NO" <> 0
            OR "SO_TIEN_CO" <> 0

            ;

            END $$
            ;

            SELECT 
           
            "TEN_CONG_TRINH" AS "TEN_CONG_TRINH",
            "TK_CONG_NO" AS "SO_TAI_KHOAN",
            "NGAY_HACH_TOAN" AS "NGAY_HACH_TOAN",
            "NGAY_CHUNG_TU" AS "NGAY_CHUNG_TU",
            "SO_CHUNG_TU" AS "SO_CHUNG_TU",
            "DIEN_GIAI" AS "DIEN_GIAI",
            "TK_DOI_UNG" AS "TK_DOI_UNG",
            "SO_TIEN_NO" AS "SO_TIEN_NO",
            "SO_TIEN_CO" AS "SO_TIEN_CO",
            "ID_CHUNG_TU" as "ID_GOC",
            "MODEL_CHUNG_TU" as "MODEL_GOC"

            FROM TMP_KET_QUA
            ORDER BY RowNum

            OFFSET %(offset)s
            LIMIT %(limit)s;
            """
        return self.execute(query,params_sql)

    def _lay_bao_cao_don_hang(self, params_sql):      
        record = []
        query = """
                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             TIMESTAMP :=  %(TU_NGAY)s;

                den_ngay                            TIMESTAMP :=  %(DEN_NGAY)s;

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER :=  %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

                chi_nhanh_id                        INTEGER :=  %(CHI_NHANH_ID)s;


                TON_TAI_TK_154                      BOOLEAN;

                SO_TK_154                           VARCHAR;


                TAI_KHOAN_ID_154                    INTEGER;

                CHE_DO_KE_TOAN                      VARCHAR;

                rec                                 RECORD;

                --@ListSAOrderID --Tham số bên misa
                --@ListAccountID ----Tham số bên misa


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


                DROP TABLE IF EXISTS TMP_TAI_KHOAN_DUOC_CHON
                ;

                CREATE TEMP TABLE TMP_TAI_KHOAN_DUOC_CHON
                    -- Bảng các tài khoản được chọn
                (
                    "TK_CONG_NO_ID"  INT,
                    "TK_CONG_NO"     VARCHAR(20) PRIMARY KEY,
                    "TEN_TK_DOI_UNG" VARCHAR(255)
                )
                ;

                INSERT INTO TMP_TAI_KHOAN_DUOC_CHON
                    SELECT
                        A.id
                        , A."SO_TAI_KHOAN"
                        , A."TEN_TAI_KHOAN"
                    FROM danh_muc_he_thong_tai_khoan A
                    WHERE A."id" = any (%(TAI_KHOAN_IDS)s) --@ListAccountID
                ;

                DROP TABLE IF EXISTS TMP_SO_TAI_KHOAN
                ;

                CREATE TEMP TABLE TMP_SO_TAI_KHOAN
                    -- Lấy các tài khoản cha nhất để đối chiếu
                (

                    "TAI_KHOAN_ID"         INT,
                    "SO_TAI_KHOAN"         VARCHAR(20) PRIMARY KEY,
                    "TEN_TAI_KHOAN"        VARCHAR(255),
                    "AccountNumberPercent" VARCHAR(25)

                )
                ;

                SELECT "SO_TAI_KHOAN"
                INTO SO_TK_154
                FROM danh_muc_he_thong_tai_khoan
                WHERE "SO_TAI_KHOAN" LIKE '154%%' AND "LA_TK_TONG_HOP" = FALSE
                ORDER BY "SO_TAI_KHOAN"
                LIMIT 1
                ;

                SELECT "id"
                INTO TAI_KHOAN_ID_154
                FROM danh_muc_he_thong_tai_khoan
                WHERE "SO_TAI_KHOAN" LIKE '154%%' AND "LA_TK_TONG_HOP" = FALSE
                ORDER BY "SO_TAI_KHOAN"
                LIMIT 1
                ;


                INSERT INTO TMP_SO_TAI_KHOAN
                    SELECT DISTINCT
                        SA."id"
                        , SA."SO_TAI_KHOAN"
                        , SA."TEN_TAI_KHOAN"
                        , SA."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"

                    FROM danh_muc_he_thong_tai_khoan SA
                        INNER JOIN TMP_TAI_KHOAN_DUOC_CHON SAD ON SA."SO_TAI_KHOAN" LIKE SAD."TK_CONG_NO"
                                                                                        || '%%'
                    WHERE sa."LA_TK_TONG_HOP" = FALSE
                ;


                DROP TABLE IF EXISTS TMP_DON_HANG
                ;

                CREATE TEMP TABLE TMP_DON_HANG
                    -- Bảng đơn hàng
                (
                    "ID_CHUNG_TU"   INT PRIMARY KEY,
                    "SO_CHUNG_TU"   VARCHAR(25),
                    "NGAY_CHUNG_TU" TIMESTAMP
                )
                ;

                INSERT INTO TMP_DON_HANG
                    SELECT
                        SAO."id"
                        , SAO."SO_DON_HANG"
                        , SAO."NGAY_DON_HANG"
                    FROM
                        account_ex_don_dat_hang SAO
                    WHERE SAO."id" = any (%(DON_HANG_IDS)s) --@ListSAOrderID
                ;

                DROP TABLE IF EXISTS TMP_CHUNG_TU
                ;

                CREATE TEMP TABLE TMP_CHUNG_TU

                (
                    "DON_HANG_ID"      INT,
                    "SO_DON_HANG"      VARCHAR(25),
                    "NGAY_DON_HANG"    TIMESTAMP,

                    "ID_CHUNG_TU"      INT,
                    "MODEL_CHUNG_TU"   VARCHAR(100),
                    "NGAY_HACH_TOAN"   TIMESTAMP,
                    "NGAY_CHUNG_TU"    TIMESTAMP,
                    "SO_CHUNG_TU"      VARCHAR(20),
                    "LOAI_CHUNG_TU"    VARCHAR(500),
                    "NGAY_HOA_DON"     TIMESTAMP,
                    "SO_HOA_DON"       VARCHAR(500),
                    "DIEN_GIAI"        VARCHAR(255),
                    "DIEN_GIAI_CHUNG"  VARCHAR(255),
                    "TK_CONG_NO"       VARCHAR(20),
                    "TK_DOI_UNG"       VARCHAR(20),
                    "SO_TIEN_NO"       DECIMAL(18, 4),
                    "SO_TIEN_CO"       DECIMAL(18, 4),

                    "SortDetailOrder"  INT,
                    "NGAY_CAN_CU"      TIMESTAMP,
                    "TK_CONG_NO_ID"    INT,
                    "TK_DOI_UNG_ID"    INT,
                    "KHOAN_MUC_CP_ID"  INT,
                    "MA_KHOAN_MUC_CP"  VARCHAR(20),
                    "TEN_KHOAN_MUC_CP" VARCHAR(255)


                )
                ;

                INSERT INTO TMP_CHUNG_TU
                    SELECT
                        GL."DON_DAT_HANG_ID"
                        , SAO."SO_CHUNG_TU"   AS "SO_DON_HANG"
                        , SAO."NGAY_CHUNG_TU" AS "NGAY_DON_HANG"

                        , GL."ID_CHUNG_TU"
                        , GL."MODEL_CHUNG_TU"
                        , GL."NGAY_HACH_TOAN"
                        , GL."NGAY_CHUNG_TU"
                        , GL."SO_CHUNG_TU"
                        , GL."LOAI_CHUNG_TU"
                        , GL."NGAY_HOA_DON"
                        , GL."SO_HOA_DON"
                        , GL."DIEN_GIAI"
                        , GL."DIEN_GIAI_CHUNG"
                        , A."SO_TAI_KHOAN"
                        , GL."MA_TAI_KHOAN_DOI_UNG"
                        , GL."GHI_NO"
                        , GL."GHI_CO"

                        , GL."THU_TU_TRONG_CHUNG_TU"
                        , GL."NGAY_HACH_TOAN"    "NGAY_CAN_CU"
                        , A."TAI_KHOAN_ID"
                        , GL."TAI_KHOAN_DOI_UNG_ID"
                        , GL."KHOAN_MUC_CP_ID"
                        , EI."MA_KHOAN_MUC_CP"
                        , EI."TEN_KHOAN_MUC_CP"

                    FROM so_cai_chi_tiet GL
                        INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                        INNER JOIN TMP_SO_TAI_KHOAN A ON GL."MA_TAI_KHOAN" LIKE A."AccountNumberPercent"
                        INNER JOIN TMP_DON_HANG SAO ON SAO."ID_CHUNG_TU" = GL."DON_DAT_HANG_ID"

                        LEFT JOIN danh_muc_khoan_muc_cp EI ON EI."id" = GL."KHOAN_MUC_CP_ID"
                    WHERE GL."NGAY_HACH_TOAN" <= den_ngay
                        AND (GL."LOAI_CHUNG_TU" <> '610' OR (GL."LOAI_CHUNG_TU" = '610' AND GL."MA_TAI_KHOAN" NOT LIKE
                                                                                            '154%%')) -- ntquang 30/08/2017 - không lấy phát sinh của tk 154 ở số dư đầu kỳ
                    UNION ALL
                    SELECT
                        JCCAD."SO_DON_HANG_ID"
                        , SAO."SO_CHUNG_TU"                AS "SO_DON_HANG"
                        , SAO."NGAY_CHUNG_TU"              AS "NGAY_DON_HANG"
                        , NULL                                "ID_CHUNG_TU"
                        , NULL                                "MODEL_CHUNG_TU"
                        , JCP."DEN_NGAY"                      "NGAY_HACH_TOAN"
                        , NULL                                "NGAY_CHUNG_TU"
                        , NULL                                "SO_CHUNG_TU"
                        , NULL                                "LOAI_CHUNG_TU"
                        , NULL                                "NGAY_HOA_DON"
                        , NULL                                "SO_HOA_DON"
                        , 'Phân bổ chi phí sản xuất chung' AS "DIEN_GIAI"
                        , 'Phân bổ chi phí sản xuất chung' AS "DIEN_GIAI_CHUNG"
                        , A."SO_TAI_KHOAN"
                        , NULL                                "TK_DOI_UNG"
                        , JCCAD."SO_TIEN"                     "SO_TIEN_NO"
                        , 0                                   "SO_TIEN_CO"

                        , 0                                   SortDetailOrer
                        , JCP."DEN_NGAY"                      "NGAY_CAN_CU"
                        , A."TAI_KHOAN_ID"
                        , NULL                                "TK_DOI_UNG_ID"
                        , JCCAD."KHOAN_MUC_CP_ID"
                        , EI."MA_KHOAN_MUC_CP"
                        , EI."TEN_KHOAN_MUC_CP"

                    FROM gia_thanh_ky_tinh_gia_thanh JCP
                        INNER JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung JCCAD ON JCCAD."KY_TINH_GIA_THANH_ID" = JCP."id"

                        INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCP."CHI_NHANH_ID"
                        INNER JOIN TMP_DON_HANG SAO ON SAO."ID_CHUNG_TU" = JCCAD."SO_DON_HANG_ID"

                        INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN"
                                                        FROM danh_muc_he_thong_tai_khoan TK
                                                        WHERE TK.id = JCCAD."TAI_KHOAN_ID") LIKE A."AccountNumberPercent"
                        LEFT JOIN danh_muc_khoan_muc_cp EI ON EI."id" = JCCAD."KHOAN_MUC_CP_ID"
                    WHERE JCP."DEN_NGAY" <= den_ngay
                        AND CHE_DO_KE_TOAN = '15'

                    UNION ALL
                    SELECT
                        JCCAD."SO_DON_HANG_ID"
                        , SAO."SO_CHUNG_TU"                AS "SO_DON_HANG"
                        , SAO."NGAY_CHUNG_TU"              AS "NGAY_DON_HANG"
                        , NULL                                "ID_CHUNG_TU"
                        , NULL                                "MODEL_CHUNG_TU"
                        , JCP."DEN_NGAY"                      "NGAY_HACH_TOAN"
                        , NULL                                "NGAY_CHUNG_TU"
                        , NULL                                "SO_CHUNG_TU"
                        , NULL                                "LOAI_CHUNG_TU"
                        , NULL                                "NGAY_HOA_DON"
                        , NULL                                "SO_HOA_DON"
                        , 'Phân bổ chi phí sản xuất chung'    "DIEN_GIAI"
                        , 'Phân bổ chi phí sản xuất chung' AS "DIEN_GIAI_CHUNG"
                        , SO_TK_154
                        , NULL                                "TK_DOI_UNG"
                        , JCCAD."SO_TIEN"                     "SO_TIEN_NO"
                        , 0                                   "SO_TIEN_CO"

                        , 0                                   SortDetailOrer
                        , JCP."DEN_NGAY"                      "NGAY_CAN_CU"
                        , TAI_KHOAN_ID_154
                        , NULL                                "TK_DOI_UNG_ID"
                        , JCCAD."KHOAN_MUC_CP_ID"
                        , EI."MA_KHOAN_MUC_CP"
                        , EI."TEN_KHOAN_MUC_CP"
                    FROM gia_thanh_ky_tinh_gia_thanh JCP
                        INNER JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung JCCAD ON JCCAD."KY_TINH_GIA_THANH_ID" = JCP."id"

                        INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCP."CHI_NHANH_ID"
                        INNER JOIN TMP_DON_HANG SAO ON SAO."ID_CHUNG_TU" = JCCAD."SO_DON_HANG_ID"

                        LEFT JOIN danh_muc_khoan_muc_cp EI ON EI."id" = JCCAD."KHOAN_MUC_CP_ID"
                    WHERE JCP."DEN_NGAY" <= den_ngay
                        AND CHE_DO_KE_TOAN = '48'
                        AND EXISTS(SELECT "SO_TAI_KHOAN"
                                    FROM TMP_SO_TAI_KHOAN
                                    WHERE "SO_TAI_KHOAN" LIKE '154%%')

                    UNION ALL
                    SELECT
                        JCAEDT."MA_DON_VI_ID" AS "DON_HANG_ID"
                        , SAO."SO_CHUNG_TU"     AS "SO_DON_HANG"
                        , SAO."NGAY_CHUNG_TU"   AS "NGAY_DON_HANG"
                        , JCAE."id"
                        , NULL                     "MODEL_CHUNG_TU"
                        , JCAE."NGAY_CHUNG_TU"     "NGAY_HACH_TOAN"
                        , JCAE."NGAY_CHUNG_TU"
                        , JCAE."SO_CHUNG_TU"
                        , CAST(JCAE."LOAI_CHUNG_TU" AS VARCHAR(255))
                        , NULL                     "NGAY_HOA_DON"
                        , NULL                     "SO_HOA_DON"
                        , JCAE."DIEN_GIAI"         "DIEN_GIAI"
                        , JCAE."DIEN_GIAI"      AS "DIEN_GIAI_CHUNG"
                        , A."SO_TAI_KHOAN"
                        , NULL                     "TK_DOI_UNG"
                        , JCAEDT."SO_TIEN"         "SO_TIEN_NO"
                        , 0                        "SO_TIEN_CO"

                        , 0                        SortDetailOrder
                        , JCAE."NGAY_CHUNG_TU"     "NGAY_CAN_CU"
                        , A."TAI_KHOAN_ID"
                        , NULL                     "TK_DOI_UNG_ID"
                        , NULL :: INT
                        , NULL
                        , NULL

                    FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JCAE
                        INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCAEDT
                            ON JCAEDT."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JCAE."id"
                        INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCAE."CHI_NHANH_ID"
                        INNER JOIN TMP_DON_HANG SAO ON SAO."ID_CHUNG_TU" = JCAEDT."MA_DON_VI_ID"

                        INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN"
                                                        FROM danh_muc_he_thong_tai_khoan TK
                                                        WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE A."AccountNumberPercent"
                        INNER JOIN danh_muc_reftype SYSRT ON SYSRT."REFTYPE" = JCAE."LOAI_CHUNG_TU"
                    WHERE JCAE."NGAY_CHUNG_TU" <= den_ngay
                        AND JCAEDT."CAP_TO_CHUC" = '1'

                    UNION ALL
                    SELECT
                        JC."DON_HANG_ID"
                        , SAO."SO_CHUNG_TU"           AS "SO_DON_HANG"
                        , SAO."NGAY_CHUNG_TU"         AS "NGAY_DON_HANG"
                        , NULL                           "ID_CHUNG_TU"
                        , NULL                           "MODEL_CHUNG_TU"
                        , NULL                           "NGAY_HACH_TOAN"
                        , NULL                           "NGAY_CHUNG_TU"
                        , NULL                           "SO_CHUNG_TU"
                        , NULL                           "LOAI_CHUNG_TU"
                        , NULL                           "NGAY_HOA_DON"
                        , NULL                           "SO_HOA_DON"
                        , 'Chi phí dở dang'              "DIEN_GIAI"
                        , 'Chi phí dở dang'           AS "DIEN_GIAI_CHUNG"
                        , A."SO_TAI_KHOAN"
                        , NULL                           "TK_DOI_UNG"
                        , JC."SO_CHUA_NGHIEM_THU"        "SO_TIEN_NO"
                        , 0                              "SO_TIEN_CO"

                        , 0                              SortDetailOrder
                        , tu_ngay + INTERVAL '-1 day' AS "NGAY_CAN_CU"
                        , A."TAI_KHOAN_ID"
                        , NULL                           "TK_DOI_UNG_ID"
                        , NULL :: INT
                        , NULL
                        , NULL

                    FROM account_ex_chi_phi_do_dang JC
                        INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JC."CHI_NHANH_ID"
                        INNER JOIN TMP_DON_HANG SAO ON SAO."ID_CHUNG_TU" = JC."DON_HANG_ID"

                        INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN"
                                                        FROM danh_muc_he_thong_tai_khoan TK
                                                        WHERE TK.id = JC."TAI_KHOAN_CPSXKD_DO_DANG_ID") LIKE
                                                        A."AccountNumberPercent"
                ;


                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA
                    AS

                        SELECT
                            ROW_NUMBER()
                            OVER (
                                ORDER BY "SO_DON_HANG", "TK_CONG_NO", "STT", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU",
                                    "TK_DOI_UNG", "SO_TIEN_NO", "SO_TIEN_CO"
                                ) AS RowNum
                            , *
                        FROM (SELECT
                                "DON_HANG_ID"
                                , "SO_DON_HANG"
                                , "NGAY_DON_HANG"

                                , NULL               "ID_CHUNG_TU"
                                , NULL               "MODEL_CHUNG_TU"
                                , NULL               "NGAY_HACH_TOAN"
                                , NULL               "NGAY_CHUNG_TU"
                                , NULL               "SO_CHUNG_TU"
                                , NULL               "LOAI_CHUNG_TU"
                                , NULL               "NGAY_HOA_DON"
                                , NULL               "SO_HOA_DON"
                                , 'Số dư đầu kỳ'     "DIEN_GIAI"
                                , NULL        AS     "DIEN_GIAI_CHUNG"
                                , "TK_CONG_NO"
                                , NULL               "TK_DOI_UNG"
                                , CASE WHEN SUM("SO_TIEN_NO" - "SO_TIEN_CO") > 0
                                THEN SUM("SO_TIEN_NO" - "SO_TIEN_CO")
                                    ELSE 0
                                    END                "SO_TIEN_NO"
                                , CASE WHEN SUM("SO_TIEN_NO" - "SO_TIEN_CO") < 0
                                THEN SUM("SO_TIEN_CO" - "SO_TIEN_NO")
                                    ELSE 0
                                    END                "SO_TIEN_CO"

                                , 0                  SortDetailOrder

                                , 0                  "STT"
                                , "TK_CONG_NO_ID"
                                , NULL               "TK_DOI_UNG_ID"
                                , CAST(1 AS BOOLEAN) "IsBold"
                                , NULL :: INT AS     "KHOAN_MUC_CP_ID"
                                , NULL        AS     "MA_KHOAN_MUC_CP"
                                , NULL        AS     "TEN_KHOAN_MUC_CP"

                            FROM TMP_CHUNG_TU V

                            WHERE "NGAY_CAN_CU" < tu_ngay
                            GROUP BY
                                "DON_HANG_ID",
                                "SO_DON_HANG",
                                "NGAY_DON_HANG",
                                "TK_CONG_NO",
                                "TK_CONG_NO_ID"
                            HAVING SUM("SO_TIEN_NO" - "SO_TIEN_CO") <> 0

                            UNION ALL
                            SELECT
                                "DON_HANG_ID"
                                , "SO_DON_HANG"
                                , "NGAY_DON_HANG"
                                , "ID_CHUNG_TU"
                                , "MODEL_CHUNG_TU"
                                , "NGAY_HACH_TOAN"
                                , "NGAY_CHUNG_TU"
                                , "SO_CHUNG_TU"
                                , "LOAI_CHUNG_TU"
                                , "NGAY_HOA_DON"
                                , "SO_HOA_DON"
                                , V."DIEN_GIAI"
                                , "DIEN_GIAI_CHUNG"
                                , "TK_CONG_NO"
                                , "TK_DOI_UNG"
                                , SUM("SO_TIEN_NO")  "SO_TIEN_NO"
                                , SUM("SO_TIEN_CO")  "SO_TIEN_CO"

                                , "SortDetailOrder"

                                , 1                  "STT"
                                , "TK_CONG_NO_ID"
                                , "TK_DOI_UNG_ID"
                                , CAST(0 AS BOOLEAN) "IsBold"
                                , "KHOAN_MUC_CP_ID"
                                , "MA_KHOAN_MUC_CP"
                                , "TEN_KHOAN_MUC_CP"

                            FROM TMP_CHUNG_TU V

                            WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                            GROUP BY
                                "DON_HANG_ID",
                                "SO_DON_HANG",
                                "NGAY_DON_HANG",
                                "ID_CHUNG_TU",
                                "MODEL_CHUNG_TU",
                                "NGAY_HACH_TOAN",
                                "NGAY_CHUNG_TU",
                                "SO_CHUNG_TU",
                                "LOAI_CHUNG_TU",
                                "NGAY_HOA_DON",
                                "SO_HOA_DON",
                                V."DIEN_GIAI",
                                "DIEN_GIAI_CHUNG",
                                "TK_CONG_NO",
                                "TK_DOI_UNG",

                                "SortDetailOrder",
                                "TK_CONG_NO_ID",
                                "TK_DOI_UNG_ID",
                                "KHOAN_MUC_CP_ID",
                                "MA_KHOAN_MUC_CP",
                                "TEN_KHOAN_MUC_CP"
                            HAVING SUM("SO_TIEN_NO") <> 0 OR SUM("SO_TIEN_CO") <> 0


                            UNION ALL
                            SELECT
                                "DON_HANG_ID"
                                , "SO_DON_HANG"
                                , "NGAY_DON_HANG"
                                , NULL               "ID_CHUNG_TU"
                                , NULL               "MODEL_CHUNG_TU"
                                , NULL               "NGAY_HACH_TOAN"
                                , NULL               "NGAY_CHUNG_TU"
                                , NULL               "SO_CHUNG_TU"
                                , NULL               "LOAI_CHUNG_TU"
                                , NULL               "NGAY_HOA_DON"
                                , NULL               "SO_HOA_DON"
                                , 'Cộng phát sinh'   "DIEN_GIAI"
                                , NULL        AS     "DIEN_GIAI_CHUNG"
                                , "TK_CONG_NO"
                                , NULL               "TK_DOI_UNG"
                                , SUM("SO_TIEN_NO")  "SO_TIEN_NO"
                                , SUM("SO_TIEN_CO")  "SO_TIEN_CO"

                                , 0                  SortDetailOrder

                                , 2                  "STT"
                                , "TK_CONG_NO_ID"
                                , NULL               "TK_DOI_UNG_ID"
                                , CAST(1 AS BOOLEAN) "IsBold"
                                , NULL :: INT AS     "KHOAN_MUC_CP_ID"
                                , NULL        AS     "MA_KHOAN_MUC_CP"
                                , NULL        AS     "TEN_KHOAN_MUC_CP"
                            FROM TMP_CHUNG_TU V

                            WHERE "NGAY_CAN_CU" BETWEEN tu_ngay AND den_ngay
                            GROUP BY
                                "DON_HANG_ID",
                                "SO_DON_HANG",
                                "NGAY_DON_HANG",
                                "TK_CONG_NO",
                                "TK_CONG_NO_ID"

                            HAVING SUM("SO_TIEN_NO") <> 0 OR SUM("SO_TIEN_CO") <> 0
                            UNION ALL
                            SELECT
                                "DON_HANG_ID"
                                , "SO_DON_HANG"
                                , "NGAY_DON_HANG"
                                , NULL            "ID_CHUNG_TU"
                                , NULL            "MODEL_CHUNG_TU"
                                , NULL            "NGAY_HACH_TOAN"
                                , NULL            "NGAY_CHUNG_TU"
                                , NULL            "SO_CHUNG_TU"
                                , NULL            "LOAI_CHUNG_TU"
                                , NULL            "NGAY_HOA_DON"
                                , NULL            "SO_HOA_DON"
                                , 'Số dư cuối kỳ' "DIEN_GIAI"
                                , NULL        AS  "DIEN_GIAI_CHUNG"
                                , "TK_CONG_NO"
                                , NULL            "TK_DOI_UNG"
                                , CASE WHEN SUM("SO_TIEN_NO" - "SO_TIEN_CO") > 0
                                THEN SUM("SO_TIEN_NO" - "SO_TIEN_CO")
                                    ELSE 0
                                    END             "SO_TIEN_NO"
                                , CASE WHEN SUM("SO_TIEN_NO" - "SO_TIEN_CO") < 0
                                THEN SUM("SO_TIEN_CO" - "SO_TIEN_NO")
                                    ELSE 0
                                    END             "SO_TIEN_CO"

                                , 0               SortDetailOrder

                                , 3               "STT"
                                , "TK_CONG_NO_ID"
                                , NULL            "TK_DOI_UNG_ID"
                                , TRUE        AS  "IsBold"
                                , NULL :: INT AS  "KHOAN_MUC_CP_ID"
                                , NULL        AS  "MA_KHOAN_MUC_CP"
                                , NULL        AS  "TEN_KHOAN_MUC_CP"
                            FROM TMP_CHUNG_TU V

                            WHERE "NGAY_CAN_CU" <= den_ngay
                            GROUP BY
                                "DON_HANG_ID",
                                "SO_DON_HANG",
                                "NGAY_DON_HANG",
                                "TK_CONG_NO",
                                "TK_CONG_NO_ID"
                            HAVING SUM("SO_TIEN_NO" - "SO_TIEN_CO") <> 0

                            ) tbl


                ;

            END $$
            ;


                SELECT
                CASE
                WHEN KQ."IsBold" = TRUE
                THEN 1
                ELSE
                0
                END AS "IsBold_1",
                "SO_DON_HANG" AS "SO_DON_HANG",
                "TK_CONG_NO" AS "SO_TAI_KHOAN",
                "NGAY_HACH_TOAN" AS "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU" AS "NGAY_CHUNG_TU",
                "SO_CHUNG_TU" AS "SO_CHUNG_TU",
                "DIEN_GIAI" AS "DIEN_GIAI",
                "TK_DOI_UNG" AS "TK_DOI_UNG",
                "SO_TIEN_NO" AS "SO_TIEN_NO",
                "SO_TIEN_CO" AS "SO_TIEN_CO",
                "ID_CHUNG_TU" as "ID_GOC",
                "MODEL_CHUNG_TU" as "MODEL_GOC"

                FROM TMP_KET_QUA KQ
                ORDER BY RowNum

                OFFSET %(offset)s
                LIMIT %(limit)s;
                """
        return self.execute(query,params_sql)
    
    def _lay_bao_cao_hop_dong(self, params_sql):      
        record = []
        query = """
                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             TIMESTAMP :=  %(TU_NGAY)s;

                den_ngay                            TIMESTAMP :=  %(DEN_NGAY)s;

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER :=  %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

                chi_nhanh_id                        INTEGER :=  %(CHI_NHANH_ID)s;

                SO_TK_154                           VARCHAR;


                TAI_KHOAN_ID_154                    INTEGER;

                CHE_DO_KE_TOAN                      VARCHAR;

                rec                                 RECORD;

                --@ListContractID--Tham số bên misa
                --@ListAccountID ----Tham số bên misa


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


                DROP TABLE IF EXISTS TMP_TAI_KHOAN_DUOC_CHON
                ;

                CREATE TEMP TABLE TMP_TAI_KHOAN_DUOC_CHON
                    -- Bảng các tài khoản được chọn
                (
                    "TK_CONG_NO_ID"  INT,
                    "TK_CONG_NO"     VARCHAR(20) PRIMARY KEY,
                    "TEN_TK_DOI_UNG" VARCHAR(255)
                )
                ;

                INSERT INTO TMP_TAI_KHOAN_DUOC_CHON
                    SELECT
                        A.id
                        , A."SO_TAI_KHOAN"
                        , A."TEN_TAI_KHOAN"
                    FROM danh_muc_he_thong_tai_khoan A
                    WHERE A."id" = any(%(TAI_KHOAN_IDS)s) --@ListAccountID
                ;

                DROP TABLE IF EXISTS TMP_SO_TAI_KHOAN
                ;

                CREATE TEMP TABLE TMP_SO_TAI_KHOAN
                    -- Lấy các tài khoản cha nhất để đối chiếu
                (

                    "TAI_KHOAN_ID"            INT,
                    "SO_TAI_KHOAN"            VARCHAR(20) PRIMARY KEY,
                    "TEN_TAI_KHOAN"           VARCHAR(255),
                    "AccountNumberPercent"    VARCHAR(25),
                    "CHI_TIET_THEO_DOI_TUONG" VARCHAR(255)

                )
                ;

                SELECT "SO_TAI_KHOAN"
                INTO SO_TK_154
                FROM danh_muc_he_thong_tai_khoan
                WHERE "SO_TAI_KHOAN" LIKE '154%%' AND "LA_TK_TONG_HOP" = FALSE
                ORDER BY "SO_TAI_KHOAN"
                LIMIT 1
                ;

                SELECT "id"
                INTO TAI_KHOAN_ID_154
                FROM danh_muc_he_thong_tai_khoan
                WHERE "SO_TAI_KHOAN" LIKE '154%%' AND "LA_TK_TONG_HOP" = FALSE
                ORDER BY "SO_TAI_KHOAN"
                LIMIT 1
                ;


                INSERT INTO TMP_SO_TAI_KHOAN
                    SELECT DISTINCT
                        SA."id"
                        , SA."SO_TAI_KHOAN"
                        , SA."TEN_TAI_KHOAN"
                        , SA."SO_TAI_KHOAN" || '%%' AS "AccountNumberPercent"
                        , SA."CHI_TIET_THEO_DOI_TUONG"

                    FROM danh_muc_he_thong_tai_khoan SA
                        INNER JOIN TMP_TAI_KHOAN_DUOC_CHON SAD ON SA."SO_TAI_KHOAN" LIKE SAD."TK_CONG_NO"
                                                                                        || '%%'
                    WHERE sa."LA_TK_TONG_HOP" = FALSE
                ;


                DROP TABLE IF EXISTS TMP_HOP_DONG_DU_AN
                ;

                CREATE TEMP TABLE TMP_HOP_DONG_DU_AN

                    -- Bảng hợp đồng/dự án
                (
                    "HOP_DONG_ID"    INT PRIMARY KEY,
                    "SO_HOP_DONG"    VARCHAR(50),
                    "TRICH_YEU"      VARCHAR(255),
                    "THUOC_DU_AN_ID" INT
                )
                ;

                INSERT INTO TMP_HOP_DONG_DU_AN
                    SELECT
                        C."id"
                        , C."SO_HOP_DONG"
                        , C."TRICH_YEU"
                        , C."THUOC_DU_AN_ID"
                    FROM sale_ex_hop_dong_ban C
                    WHERE C."id" = any (%(HOP_DONG_BAN_IDS)s)--@ListContractID
                ;


                DROP TABLE IF EXISTS TMP_HOP_DONG
                ;

                CREATE TEMP TABLE TMP_HOP_DONG -- Bảng gồm các hợp đồng con của dự án
                (
                    "HOP_DONG_ID"     INT,
                    "OUT_HOP_DONG_ID" INT
                )
                ;

                INSERT INTO TMP_HOP_DONG
                    SELECT DISTINCT
                        COALESCE(C."id", P."HOP_DONG_ID") "HOP_DONG_ID"
                        , P."HOP_DONG_ID"
                    FROM TMP_HOP_DONG_DU_AN P
                        LEFT JOIN sale_ex_hop_dong_ban C ON C."THUOC_DU_AN_ID" = P."HOP_DONG_ID" OR C."id" = P."HOP_DONG_ID"
                    GROUP BY COALESCE(C."id", P."HOP_DONG_ID"),
                        P."HOP_DONG_ID"
                ;


                DROP TABLE IF EXISTS TMP_CHUNG_TU
                ;

                CREATE TEMP TABLE TMP_CHUNG_TU

                (
                    "HOP_DONG_ID"      INT,
                    "ID_CHUNG_TU"      INT,
                    "MODEL_CHUNG_TU"   VARCHAR(100),
                    "NGAY_HACH_TOAN"   TIMESTAMP,
                    "NGAY_CHUNG_TU"    TIMESTAMP,
                    "SO_CHUNG_TU"      VARCHAR(20),
                    "LOAI_CHUNG_TU"    VARCHAR(500),
                    "NGAY_HOA_DON"     TIMESTAMP,
                    "SO_HOA_DON"       VARCHAR(500),
                    "DIEN_GIAI"        VARCHAR(255),
                    "DIEN_GIAI_CHUNG"  VARCHAR(255),
                    "TK_CONG_NO"       VARCHAR(20),
                    "TK_DOI_UNG"       VARCHAR(20),
                    "SO_TIEN_NO"       DECIMAL(18, 4),
                    "SO_TIEN_CO"       DECIMAL(18, 4),
                    "SortDetailOrder"  INT,
                    "NGAY_CAN_CU"      TIMESTAMP,
                    "TK_CONG_NO_ID"    INT,
                    "TK_DOI_UNG_ID"    INT,
                    "KHOAN_MUC_CP_ID"  INT,
                    "MA_KHOAN_MUC_CP"  VARCHAR(20),
                    "TEN_KHOAN_MUC_CP" VARCHAR(255)


                )
                ;

                INSERT INTO TMP_CHUNG_TU
                    SELECT
                        C."OUT_HOP_DONG_ID"


                        , GL."ID_CHUNG_TU"
                        , GL."MODEL_CHUNG_TU"
                        , GL."NGAY_HACH_TOAN"
                        , GL."NGAY_CHUNG_TU"
                        , GL."SO_CHUNG_TU"
                        , GL."LOAI_CHUNG_TU"
                        , GL."NGAY_HOA_DON"
                        , GL."SO_HOA_DON"
                        , GL."DIEN_GIAI"
                        , GL."DIEN_GIAI_CHUNG"
                        , A."SO_TAI_KHOAN"
                        , GL."MA_TAI_KHOAN_DOI_UNG"
                        , GL."GHI_NO"
                        , GL."GHI_CO"

                        , GL."THU_TU_TRONG_CHUNG_TU"
                        , GL."NGAY_HACH_TOAN" "NGAY_CAN_CU"
                        , A."TAI_KHOAN_ID"
                        , GL."TAI_KHOAN_DOI_UNG_ID"
                        , GL."KHOAN_MUC_CP_ID"
                        , EI."MA_KHOAN_MUC_CP"
                        , EI."TEN_KHOAN_MUC_CP"

                    FROM so_cai_chi_tiet GL
                        INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                        INNER JOIN TMP_SO_TAI_KHOAN A ON GL."MA_TAI_KHOAN" LIKE A."AccountNumberPercent"
                        INNER JOIN TMP_HOP_DONG C ON C."HOP_DONG_ID" = GL."HOP_DONG_BAN_ID"

                        LEFT JOIN danh_muc_khoan_muc_cp EI ON EI."id" = GL."KHOAN_MUC_CP_ID"
                    WHERE GL."NGAY_HACH_TOAN" <= den_ngay
                        AND (GL."LOAI_CHUNG_TU" <> '610' OR (GL."LOAI_CHUNG_TU" = '610' AND GL."MA_TAI_KHOAN" NOT LIKE
                                                                                            '154%%')) -- ntquang 30/08/2017 - không lấy phát sinh của tk 154 ở số dư đầu kỳ
                    UNION ALL
                    SELECT
                        C."OUT_HOP_DONG_ID"
                        , NULL                                "ID_CHUNG_TU"
                        , NULL                                "MODEL_CHUNG_TU"
                        , JCP."DEN_NGAY"                      "NGAY_HACH_TOAN"
                        , NULL                                "NGAY_CHUNG_TU"
                        , NULL                                "SO_CHUNG_TU"
                        , NULL                                "LOAI_CHUNG_TU"
                        , NULL                                "NGAY_HOA_DON"
                        , NULL                                "SO_HOA_DON"
                        , 'Phân bổ chi phí sản xuất chung' AS "DIEN_GIAI"
                        , 'Phân bổ chi phí sản xuất chung' AS "DIEN_GIAI_CHUNG"
                        , SO_TK_154
                        , NULL                                "TK_DOI_UNG"
                        , JCCAD."SO_TIEN"                     "SO_TIEN_NO"
                        , 0                                   "SO_TIEN_CO"

                        , 0                                   SortDetailOrer
                        , JCP."DEN_NGAY"                      "NGAY_CAN_CU"
                        , TAI_KHOAN_ID_154
                        , NULL                                "TK_DOI_UNG_ID"
                        , JCCAD."KHOAN_MUC_CP_ID"
                        , EI."MA_KHOAN_MUC_CP"
                        , EI."TEN_KHOAN_MUC_CP"

                    FROM gia_thanh_ky_tinh_gia_thanh JCP
                        INNER JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung JCCAD ON JCCAD."KY_TINH_GIA_THANH_ID" = JCP."id"

                        INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCP."CHI_NHANH_ID"
                        INNER JOIN TMP_HOP_DONG C ON C."HOP_DONG_ID" = JCCAD."SO_HOP_DONG_ID"
                        LEFT JOIN danh_muc_khoan_muc_cp EI ON EI."id" = JCCAD."KHOAN_MUC_CP_ID"

                    WHERE JCP."DEN_NGAY" <= den_ngay
                        AND CHE_DO_KE_TOAN = '48'
                        AND EXISTS(SELECT "SO_TAI_KHOAN"
                                    FROM TMP_SO_TAI_KHOAN
                                    WHERE "SO_TAI_KHOAN" LIKE '154%%')


                    UNION ALL
                    SELECT
                        C."OUT_HOP_DONG_ID"
                        , NULL                                "ID_CHUNG_TU"
                        , NULL                                "MODEL_CHUNG_TU"
                        , JCP."DEN_NGAY"                      "NGAY_HACH_TOAN"
                        , NULL                                "NGAY_CHUNG_TU"
                        , NULL                                "SO_CHUNG_TU"
                        , NULL                                "LOAI_CHUNG_TU"
                        , NULL                                "NGAY_HOA_DON"
                        , NULL                                "SO_HOA_DON"
                        , 'Phân bổ chi phí sản xuất chung'    "DIEN_GIAI"
                        , 'Phân bổ chi phí sản xuất chung' AS "DIEN_GIAI_CHUNG"
                        , A."SO_TAI_KHOAN"
                        , NULL                                "TK_DOI_UNG"
                        , JCCAD."SO_TIEN"                     "SO_TIEN_NO"
                        , 0                                   "SO_TIEN_CO"

                        , 0                                   SortDetailOrer
                        , JCP."DEN_NGAY"                      "NGAY_CAN_CU"
                        , A."TAI_KHOAN_ID"
                        , NULL                                "TK_DOI_UNG_ID"
                        , JCCAD."KHOAN_MUC_CP_ID"
                        , EI."MA_KHOAN_MUC_CP"
                        , EI."TEN_KHOAN_MUC_CP"
                    FROM gia_thanh_ky_tinh_gia_thanh JCP
                        INNER JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung JCCAD ON JCCAD."KY_TINH_GIA_THANH_ID" = JCP."id"

                        INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCP."CHI_NHANH_ID"
                        INNER JOIN TMP_HOP_DONG C ON C."HOP_DONG_ID" = JCCAD."SO_HOP_DONG_ID"

                        INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN"
                                                        FROM danh_muc_he_thong_tai_khoan TK
                                                        WHERE TK.id = JCCAD."TAI_KHOAN_ID") LIKE A."AccountNumberPercent"
                        LEFT JOIN danh_muc_khoan_muc_cp EI ON EI."id" = JCCAD."KHOAN_MUC_CP_ID"
                    WHERE JCP."DEN_NGAY" <= den_ngay
                        AND CHE_DO_KE_TOAN = '15'

                    UNION ALL
                    SELECT
                        C."OUT_HOP_DONG_ID"
                        , JCAE."id"
                        , NULL                 "MODEL_CHUNG_TU"
                        , JCAE."NGAY_CHUNG_TU" "NGAY_HACH_TOAN"
                        , JCAE."NGAY_CHUNG_TU"
                        , JCAE."SO_CHUNG_TU"
                        , CAST(JCAE."LOAI_CHUNG_TU" AS VARCHAR(255))
                        , NULL                 "NGAY_HOA_DON"
                        , NULL                 "SO_HOA_DON"
                        , JCAE."DIEN_GIAI"     "DIEN_GIAI"
                        , JCAE."DIEN_GIAI" AS  "DIEN_GIAI_CHUNG"
                        , A."SO_TAI_KHOAN"
                        , NULL                 "TK_DOI_UNG"
                        , JCAEDT."SO_TIEN"     "SO_TIEN_NO"
                        , 0                    "SO_TIEN_CO"

                        , 0                    SortDetailOrder
                        , JCAE."NGAY_CHUNG_TU" "NGAY_CAN_CU"
                        , A."TAI_KHOAN_ID"
                        , NULL                 "TK_DOI_UNG_ID"
                        , NULL :: INT
                        , NULL
                        , NULL

                    FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JCAE
                        INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCAEDT
                            ON JCAEDT."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JCAE."id"
                        INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCAE."CHI_NHANH_ID"
                        INNER JOIN TMP_HOP_DONG C ON C."HOP_DONG_ID" = JCAEDT."MA_DON_VI_ID"

                        INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN"
                                                        FROM danh_muc_he_thong_tai_khoan TK
                                                        WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE A."AccountNumberPercent"
                        INNER JOIN danh_muc_reftype SYSRT ON SYSRT."REFTYPE" = JCAE."LOAI_CHUNG_TU"
                    WHERE JCAE."NGAY_CHUNG_TU" <= den_ngay
                        AND JCAEDT."CAP_TO_CHUC" = '3'

                    UNION ALL
                    SELECT
                        C."OUT_HOP_DONG_ID"
                        , NULL                           "ID_CHUNG_TU"
                        , NULL                           "MODEL_CHUNG_TU"
                        , NULL                           "NGAY_HACH_TOAN"
                        , NULL                           "NGAY_CHUNG_TU"
                        , NULL                           "SO_CHUNG_TU"
                        , NULL                           "LOAI_CHUNG_TU"
                        , NULL                           "NGAY_HOA_DON"
                        , NULL                           "SO_HOA_DON"
                        , 'Chi phí dở dang'              "DIEN_GIAI"
                        , 'Chi phí dở dang'           AS "DIEN_GIAI_CHUNG"
                        , A."SO_TAI_KHOAN"
                        , NULL                           "TK_DOI_UNG"
                        , JC."SO_CHUA_NGHIEM_THU"        "SO_TIEN_NO"
                        , 0                              "SO_TIEN_CO"

                        , 0                              SortDetailOrder
                        , tu_ngay + INTERVAL '-1 day' AS "NGAY_CAN_CU"
                        , A."TAI_KHOAN_ID"
                        , NULL                           "TK_DOI_UNG_ID"
                        , NULL :: INT
                        , NULL
                        , NULL

                    FROM account_ex_chi_phi_do_dang JC
                        INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JC."CHI_NHANH_ID"
                        INNER JOIN TMP_HOP_DONG C ON C."HOP_DONG_ID" = JC."HOP_DONG_ID"

                        INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN"
                                                        FROM danh_muc_he_thong_tai_khoan TK
                                                        WHERE TK.id = JC."TAI_KHOAN_CPSXKD_DO_DANG_ID") LIKE
                                                        A."AccountNumberPercent"
                ;


                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA
                    AS

                        SELECT
                            ROW_NUMBER()
                            OVER (
                                ORDER BY "SO_HOP_DONG", "TK_CONG_NO", "STT", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU",
                                    SortDetailOrder
                                ) AS RowNum
                            , *
                        FROM (SELECT
                                P."HOP_DONG_ID"
                                , P."SO_HOP_DONG"
                                , P."TRICH_YEU"

                                , NULL               "ID_CHUNG_TU"
                                , NULL               "MODEL_CHUNG_TU"
                                , NULL               "NGAY_HACH_TOAN"
                                , NULL               "NGAY_CHUNG_TU"
                                , NULL               "SO_CHUNG_TU"
                                , NULL               "LOAI_CHUNG_TU"
                                , NULL               "NGAY_HOA_DON"
                                , NULL               "SO_HOA_DON"
                                , 'Số dư đầu kỳ'     "DIEN_GIAI"
                                , NULL AS            "DIEN_GIAI_CHUNG"
                                , "TK_CONG_NO"
                                , NULL               "TK_DOI_UNG"
                                , CASE WHEN SUM("SO_TIEN_NO" - "SO_TIEN_CO") > 0
                                THEN SUM("SO_TIEN_NO" - "SO_TIEN_CO")
                                    ELSE 0
                                    END                "SO_TIEN_NO"
                                , CASE WHEN SUM("SO_TIEN_NO" - "SO_TIEN_CO") < 0
                                THEN SUM("SO_TIEN_CO" - "SO_TIEN_NO")
                                    ELSE 0
                                    END                "SO_TIEN_CO"

                                , 0                  SortDetailOrder

                                , 0                  "STT"
                                , "TK_CONG_NO_ID"
                                , NULL               "TK_DOI_UNG_ID"
                                , CAST(1 AS BOOLEAN) "IsBold"
                                , NULL :: INT        "KHOAN_MUC_CP_ID"
                                , NULL               "MA_KHOAN_MUC_CP"
                                , NULL               "TEN_KHOAN_MUC_CP"

                            FROM TMP_CHUNG_TU V
                                INNER JOIN TMP_HOP_DONG_DU_AN P ON P."HOP_DONG_ID" = V."HOP_DONG_ID"

                            WHERE "NGAY_CAN_CU" < tu_ngay
                            GROUP BY
                                P."HOP_DONG_ID",
                                P."SO_HOP_DONG",
                                P."TRICH_YEU",
                                "TK_CONG_NO",
                                "TK_CONG_NO_ID"
                            HAVING SUM("SO_TIEN_NO" - "SO_TIEN_CO") <> 0

                            UNION ALL
                            SELECT
                                P."HOP_DONG_ID"
                                , P."SO_HOP_DONG"
                                , P."TRICH_YEU"
                                , "ID_CHUNG_TU"
                                , "MODEL_CHUNG_TU"
                                , "NGAY_HACH_TOAN"
                                , "NGAY_CHUNG_TU"
                                , "SO_CHUNG_TU"
                                , "LOAI_CHUNG_TU"
                                , "NGAY_HOA_DON"
                                , "SO_HOA_DON"
                                , V."DIEN_GIAI"
                                , "DIEN_GIAI_CHUNG"
                                , "TK_CONG_NO"
                                , "TK_DOI_UNG"
                                , SUM("SO_TIEN_NO")  "SO_TIEN_NO"
                                , SUM("SO_TIEN_CO")  "SO_TIEN_CO"

                                , "SortDetailOrder"

                                , 1                  "STT"
                                , "TK_CONG_NO_ID"
                                , "TK_DOI_UNG_ID"
                                , CAST(0 AS BOOLEAN) "IsBold"
                                , "KHOAN_MUC_CP_ID"
                                , "MA_KHOAN_MUC_CP"
                                , "TEN_KHOAN_MUC_CP"

                            FROM TMP_CHUNG_TU V
                                INNER JOIN TMP_HOP_DONG_DU_AN P ON P."HOP_DONG_ID" = V."HOP_DONG_ID"
                            WHERE "NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                            GROUP BY
                                P."HOP_DONG_ID",
                                P."SO_HOP_DONG",
                                P."TRICH_YEU",
                                "ID_CHUNG_TU",
                                "MODEL_CHUNG_TU",
                                "NGAY_HACH_TOAN",
                                "NGAY_CHUNG_TU",
                                "SO_CHUNG_TU",
                                "LOAI_CHUNG_TU",
                                "NGAY_HOA_DON",
                                "SO_HOA_DON",
                                V."DIEN_GIAI",
                                "DIEN_GIAI_CHUNG",
                                "TK_CONG_NO",
                                "TK_DOI_UNG",

                                "SortDetailOrder",
                                "TK_CONG_NO_ID",
                                "TK_DOI_UNG_ID",
                                "KHOAN_MUC_CP_ID",
                                "MA_KHOAN_MUC_CP",
                                "TEN_KHOAN_MUC_CP"
                            HAVING SUM("SO_TIEN_NO") <> 0 OR SUM("SO_TIEN_CO") <> 0


                            UNION ALL
                            SELECT
                                P."HOP_DONG_ID"
                                , P."SO_HOP_DONG"
                                , P."TRICH_YEU"
                                , NULL               "ID_CHUNG_TU"
                                , NULL               "MODEL_CHUNG_TU"
                                , NULL               "NGAY_HACH_TOAN"
                                , NULL               "NGAY_CHUNG_TU"
                                , NULL               "SO_CHUNG_TU"
                                , NULL               "LOAI_CHUNG_TU"
                                , NULL               "NGAY_HOA_DON"
                                , NULL               "SO_HOA_DON"
                                , 'Cộng phát sinh'   "DIEN_GIAI"
                                , NULL AS            "DIEN_GIAI_CHUNG"
                                , "TK_CONG_NO"
                                , NULL               "TK_DOI_UNG"
                                , SUM("SO_TIEN_NO")  "SO_TIEN_NO"
                                , SUM("SO_TIEN_CO")  "SO_TIEN_CO"

                                , 0                  SortDetailOrder

                                , 2                  "STT"
                                , "TK_CONG_NO_ID"
                                , NULL               "TK_DOI_UNG_ID"
                                , CAST(1 AS BOOLEAN) "IsBold"
                                , NULL :: INT        "KHOAN_MUC_CP_ID"
                                , NULL               "MA_KHOAN_MUC_CP"
                                , NULL               "TEN_KHOAN_MUC_CP"
                            FROM TMP_CHUNG_TU V
                                INNER JOIN TMP_HOP_DONG_DU_AN P ON P."HOP_DONG_ID" = V."HOP_DONG_ID"

                            WHERE "NGAY_CAN_CU" BETWEEN tu_ngay AND den_ngay
                            GROUP BY
                                P."HOP_DONG_ID",
                                P."SO_HOP_DONG",
                                P."TRICH_YEU",
                                "TK_CONG_NO",
                                "TK_CONG_NO_ID"

                            HAVING SUM("SO_TIEN_NO") <> 0 OR SUM("SO_TIEN_CO") <> 0
                            UNION ALL
                            SELECT
                                P."HOP_DONG_ID"
                                , P."SO_HOP_DONG"
                                , P."TRICH_YEU"
                                , NULL                  "ID_CHUNG_TU"
                                , NULL                  "MODEL_CHUNG_TU"
                                , NULL                  "NGAY_HACH_TOAN"
                                , NULL                  "NGAY_CHUNG_TU"
                                , NULL                  "SO_CHUNG_TU"
                                , NULL                  "LOAI_CHUNG_TU"
                                , NULL                  "NGAY_HOA_DON"
                                , NULL                  "SO_HOA_DON"
                                , 'Số dư cuối kỳ'       "DIEN_GIAI"
                                , NULL               AS "DIEN_GIAI_CHUNG"
                                , "TK_CONG_NO"
                                , NULL                  "TK_DOI_UNG"
                                , CASE WHEN SUM("SO_TIEN_NO" - "SO_TIEN_CO") > 0
                                THEN SUM("SO_TIEN_NO" - "SO_TIEN_CO")
                                    ELSE 0
                                    END                   "SO_TIEN_NO"
                                , CASE WHEN SUM("SO_TIEN_NO" - "SO_TIEN_CO") < 0
                                THEN SUM("SO_TIEN_CO" - "SO_TIEN_NO")
                                    ELSE 0
                                    END                   "SO_TIEN_CO"

                                , 0                     SortDetailOrder

                                , 3                     "STT"
                                , "TK_CONG_NO_ID"
                                , NULL                  "TK_DOI_UNG_ID"
                                , CAST(1 AS BOOLEAN) AS "IsBold"
                                , NULL :: INT           "KHOAN_MUC_CP_ID"
                                , NULL                  "MA_KHOAN_MUC_CP"
                                , NULL                  "TEN_KHOAN_MUC_CP"
                            FROM TMP_CHUNG_TU V
                                INNER JOIN TMP_HOP_DONG_DU_AN P ON P."HOP_DONG_ID" = V."HOP_DONG_ID"

                            WHERE "NGAY_CAN_CU" <= den_ngay
                            GROUP BY
                                P."HOP_DONG_ID",
                                P."SO_HOP_DONG",
                                P."TRICH_YEU",
                                "TK_CONG_NO",
                                "TK_CONG_NO_ID"
                            HAVING SUM("SO_TIEN_NO" - "SO_TIEN_CO") <> 0
                            ) tbl
                ;

            END $$
            ;


                SELECT 
                "SO_HOP_DONG" AS "HOP_DONG_DU_AN",
                "TK_CONG_NO" AS "SO_TAI_KHOAN",
                "NGAY_HACH_TOAN" AS "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU" AS "NGAY_CHUNG_TU",
                "SO_CHUNG_TU" AS "SO_CHUNG_TU",
                "DIEN_GIAI" AS "DIEN_GIAI",
                "TK_DOI_UNG" AS "TK_DOI_UNG",
                "SO_TIEN_NO" AS "SO_TIEN_NO",
                "SO_TIEN_CO" AS "SO_TIEN_CO",
                "ID_CHUNG_TU" as "ID_GOC",
                "MODEL_CHUNG_TU" as "MODEL_GOC"

                FROM TMP_KET_QUA KQ
                ORDER BY RowNum

                OFFSET %(offset)s
                LIMIT %(limit)s;
                """
        return self.execute(query,params_sql)
    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU')
        DEN_NGAY_F = self.get_vntime('DEN')
        THONG_KE_THEO = self.get_context('THONG_KE_THEO')
        param = 'Từ ngày: %s đến ngày %s' % (TU_NGAY_F, DEN_NGAY_F)
        if THONG_KE_THEO=='DOI_TUONG_THCP':
            action = self.env.ref('bao_cao.open_report_gia_thanh_so_chi_tiet_tai_khoan_cpsx_dtthcp').read()[0]
        elif THONG_KE_THEO=='CONG_TRINH':
            action = self.env.ref('bao_cao.open_report_gia_thanh_so_chi_tiet_tai_khoan_cpsx_cong_trinh').read()[0]
        elif THONG_KE_THEO=='DON_HANG':
            action = self.env.ref('bao_cao.open_report_gia_thanh_so_chi_tiet_tai_khoan_cpsx_don_hang').read()[0]
        elif THONG_KE_THEO=='HOP_DONG':
            action = self.env.ref('bao_cao.open_report_gia_thanh_so_chi_tiet_tai_khoan_cpsx_hop_dong').read()[0]
        
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action