# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class bao_cao_gia_thanh_tong_hop_chi_phi_sxkd(models.Model):
    _name = 'bao.cao.gia.thanh.tong.hop.chi.phi.sxkd'
    _description = ''
    _inherit = ['mail.thread']
    _auto = False

    THONG_KE_THEO = fields.Selection([('DOI_TUONG_THCP', 'Đối tượng THCP'),('CONG_TRINH', 'Công trình'),('DON_HANG', 'Đơn hàng'),('HOP_DONG', 'Hợp đồng')], string='Thống kê theo', help='Thống kê theo',default='DOI_TUONG_THCP',required=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh', required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI', required='True')
    TU = fields.Date(string='Từ ', help='Từ ', required='True', default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến', required='True', default=fields.Datetime.now)
    
    DOI_TUONG_THCP_ID = fields.Integer(string='DOI_TUONG_THCP_ID')
    MA_DOI_TUONG_THCP = fields.Char(string='MA_DOI_TUONG_THCP', help='JobCode')
    MA_CONG_TRINH = fields.Char(string='MA_CONG_TRINH', help='JobCode')
    SO_DON_HANG = fields.Char(string='SO_DON_HANG', help='JobCode')
    HOP_DONG_DU_AN = fields.Char(string='HOP_DONG_DU_AN', help='JobCode')
    TRICH_YEU = fields.Char(string='TRICH_YEU', help='JobCode')
    TEN_DOI_TUONG_THCP = fields.Char(string='TEN_DOI_TUONG_THCP', help='JobName')
    TEN_CONG_TRINH = fields.Char(string='TEN_CONG_TRINH', help='JobName')
    NGAY_DON_HANG = fields.Char(string='NGAY_DON_HANG', help='JobCode')
    SO_TAI_KHOAN = fields.Char(string='SO_TAI_KHOAN', help='AccountNumber')
    TAI_KHOAN_ID = fields.Integer(string='TAI_KHOAN_ID')
    NO_DAU_KY = fields.Float(string='NO_DAU_KY', help='OpenDebitAmount',digits=decimal_precision.get_precision('VND'))
    CO_DAU_KY = fields.Float(string='CO_DAU_KY', help='OpenCreditAmount',digits=decimal_precision.get_precision('VND'))
    PHAT_SINH_NO = fields.Float(string='PHAT_SINH_NO', help='DebitAmount',digits=decimal_precision.get_precision('VND'))
    PHAT_SINH_CO = fields.Float(string='PHAT_SINH_CO', help='CreditAmount',digits=decimal_precision.get_precision('VND'))
    NO_CUOI_KY = fields.Float(string='NO_CUOI_KY', help='CloseDebitAmount',digits=decimal_precision.get_precision('VND'))
    CO_CUOI_KY = fields.Float(string='CO_CUOI_KY', help='CloseCreditAmount',digits=decimal_precision.get_precision('VND'))

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
        result = super(bao_cao_gia_thanh_tong_hop_chi_phi_sxkd, self).default_get(fields_list)
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
            tu_ngay                             DATE := %(TU_NGAY)s;

            den_ngay                            DATE := %(DEN_NGAY)s;

            bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

            chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;


            TON_TAI_TK_154                      BOOLEAN;

            SO_TK_154                           VARCHAR;

            TAI_KHOAN_ID_154                    INTEGER;

            CHE_DO_KE_TOAN                      VARCHAR;

            rec                                 RECORD;

            --@ListJobID  --Tham số bên misa
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

            DROP TABLE IF EXISTS TMP_SO_TAI_KHOAN
            ;

            CREATE TEMP TABLE TMP_SO_TAI_KHOAN


            (
            "SO_TAI_KHOAN"         VARCHAR(20) PRIMARY KEY,
            "TAI_KHOAN_ID"         INT,
            "AccountNumberPercent" VARCHAR(25),
            "TINH_CHAT"            VARCHAR(25)
            )
            ;

            INSERT INTO TMP_SO_TAI_KHOAN
            SELECT
            A."SO_TAI_KHOAN"
            , A."id"
            , A."SO_TAI_KHOAN" || '%%'
            , A."TINH_CHAT"
            FROM danh_muc_he_thong_tai_khoan A
            WHERE id = any( %(TAI_KHOAN_IDS)s) --@ListAccountID
            ;


            IF EXISTS(SELECT "SO_TAI_KHOAN"
            FROM TMP_SO_TAI_KHOAN
            WHERE "SO_TAI_KHOAN" LIKE '154%%'
            LIMIT 1)
            THEN
            TON_TAI_TK_154 = TRUE
            ;
            ELSE
            TON_TAI_TK_154 = FALSE
            ;
            END IF
            ;


            SELECT "SO_TAI_KHOAN"
            INTO SO_TK_154
            FROM TMP_SO_TAI_KHOAN
            WHERE "SO_TAI_KHOAN" LIKE '154%%'
            ORDER BY "SO_TAI_KHOAN"
            LIMIT 1
            ;

            SELECT "TAI_KHOAN_ID"
            INTO TAI_KHOAN_ID_154
            FROM TMP_SO_TAI_KHOAN
            WHERE "SO_TAI_KHOAN" LIKE '154%%'
            ORDER BY "SO_TAI_KHOAN"
            LIMIT 1
            ;

            -- Lấy lên tiết khoản con đầu tiên


            DROP TABLE IF EXISTS TMP_DOI_TUONG_THCP
            ;

            CREATE TEMP TABLE TMP_DOI_TUONG_THCP
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
            FROM danh_muc_doi_tuong_tap_hop_chi_phi J
            WHERE id = any( %(DOI_TUONG_THCP_IDS)s) --@ListJobID
            ;


            DROP TABLE IF EXISTS TMP_DS_DOI_TUONG_THCP
            ;

            CREATE TEMP TABLE TMP_DS_DOI_TUONG_THCP -- Bảng công trình gồm toàn bộ công trình con
            (
            "DOI_TUONG_THCP_ID"     INT,
            "OUT_DOI_TUONG_THCP_ID" INT
            )
            ;

            INSERT INTO TMP_DS_DOI_TUONG_THCP
            SELECT
            J."id"
            , tJ."DOI_TUONG_THCP_ID"
            FROM TMP_DOI_TUONG_THCP tJ
            INNER JOIN danh_muc_doi_tuong_tap_hop_chi_phi J ON J."MA_PHAN_CAP" LIKE tJ."MA_PHAN_CAP"
                                    || '%%'
            GROUP BY
            J."id",
            tJ."DOI_TUONG_THCP_ID"
            ;

            DROP TABLE IF EXISTS TMP_BAC_DOI_TUONG_THCP
            ;

            CREATE TEMP TABLE TMP_BAC_DOI_TUONG_THCP -- Tính bậc để lùi dòng cho báo cáo hình cây
            (
            "DOI_TUONG_THCP_ID" INT PRIMARY KEY,
            "BAC"               INT
            )
            ;

            INSERT INTO TMP_BAC_DOI_TUONG_THCP
            SELECT
            P."DOI_TUONG_THCP_ID"
            , COUNT(PD."MA_PHAN_CAP") AS "BAC"
            FROM TMP_DOI_TUONG_THCP P
            LEFT JOIN TMP_DOI_TUONG_THCP PD ON P."MA_PHAN_CAP" LIKE PD."MA_PHAN_CAP"
                    || '%%'
            AND P."MA_PHAN_CAP" <> PD."MA_PHAN_CAP"
            GROUP BY P."DOI_TUONG_THCP_ID"
            ;


            -- Bảng các khoản mục CP cha được chọn trong đó có chọn cả con mà là cha
            DROP TABLE IF EXISTS TMP_DOI_TUONG_THCP_CHA
            ;

            CREATE TEMP TABLE TMP_DOI_TUONG_THCP_CHA
            (
            "DOI_TUONG_THCP_ID" INT PRIMARY KEY
            )
            ;

            INSERT INTO TMP_DOI_TUONG_THCP_CHA
            SELECT DISTINCT PD."DOI_TUONG_THCP_ID"
            FROM TMP_DOI_TUONG_THCP P
            LEFT JOIN TMP_DOI_TUONG_THCP PD ON P."MA_PHAN_CAP" LIKE PD."MA_PHAN_CAP"
                    || '%%'
            AND P."MA_PHAN_CAP" <> PD."MA_PHAN_CAP"
            WHERE PD."MA_PHAN_CAP" IS NOT NULL
            ;


            DROP TABLE IF EXISTS TMP_KET_QUA
            ;

            CREATE TEMP TABLE TMP_KET_QUA
            AS

            SELECT
            ROW_NUMBER()
            OVER (
            ORDER BY D."SO_TAI_KHOAN", P."MA_PHAN_CAP"
            )                 AS RowNum
            , D."DOI_TUONG_THCP_ID"

            , CONCAT(REPEAT('', cast(GP."BAC" * 4 AS INT)
            ), P."MA_DOI_TUONG_THCP")

            AS "MA_DOI_TUONG_THCP"
            , P."TEN_DOI_TUONG_THCP"
            , D."SO_TAI_KHOAN"
            , D."TAI_KHOAN_ID"

            , CASE WHEN SUM(D."SO_DU_DAU_KY"
            ) > 0
            THEN SUM(D."SO_DU_DAU_KY"
            )
            ELSE 0 END            AS "NO_DAU_KY"
            , CASE WHEN SUM(D."SO_DU_DAU_KY") < 0
            THEN -1 * SUM(D."SO_DU_DAU_KY")
            ELSE 0 END            AS "CO_DAU_KY"
            , SUM(D."PHAT_SINH_NO") AS "PHAT_SINH_NO"
            , SUM(D."QUY_DOI")      AS "PHAT_SINH_CO"
            , CASE WHEN SUM(D."SO_DU_DAU_KY" + D."PHAT_SINH_NO" - D."QUY_DOI") > 0
            THEN SUM(D."SO_DU_DAU_KY" + D."PHAT_SINH_NO" - D."QUY_DOI")
            ELSE 0 END            AS "NO_CUOI_KY"
            , CASE WHEN SUM(D."SO_DU_DAU_KY" + D."PHAT_SINH_NO" - D."QUY_DOI") < 0
            THEN SUM(D."QUY_DOI" - D."SO_DU_DAU_KY" - D."PHAT_SINH_NO")
            ELSE 0 END            AS "CO_CUOI_KY"

            FROM (SELECT
            J."OUT_DOI_TUONG_THCP_ID" AS "DOI_TUONG_THCP_ID"
            , A."SO_TAI_KHOAN"
            , A."TAI_KHOAN_ID"

            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
            THEN GL."GHI_NO" - GL."GHI_CO"
            ELSE 0
            END)                  AS "SO_DU_DAU_KY"
            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            THEN GL."GHI_NO"
            ELSE 0
            END)                  AS "PHAT_SINH_NO"
            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            THEN GL."GHI_CO"
            ELSE 0
            END)                  AS "QUY_DOI"
            FROM so_cai_chi_tiet GL
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON GL."MA_TAI_KHOAN" LIKE A."AccountNumberPercent"
            INNER JOIN TMP_DS_DOI_TUONG_THCP J ON J."DOI_TUONG_THCP_ID" = GL."DOI_TUONG_THCP_ID"
            WHERE GL."NGAY_HACH_TOAN" <= den_ngay
            AND (GL."LOAI_CHUNG_TU" <> '610' OR (GL."LOAI_CHUNG_TU" = '610' AND GL."MA_TAI_KHOAN" NOT LIKE
                                            N'154%%')) -- ntquang 30/08/2017 - không lấy phát sinh của tk 154 ở số dư đầu kỳ
            GROUP BY J."OUT_DOI_TUONG_THCP_ID",
            A."SO_TAI_KHOAN"
            UNION ALL
            SELECT
            J."OUT_DOI_TUONG_THCP_ID" AS "DOI_TUONG_THCP_ID"
            , SO_TK_154                 AS "SO_TAI_KHOAN"
            , TAI_KHOAN_ID_154          AS "TAI_KHOAN_ID"
            , SUM(CASE WHEN JCP."DEN_NGAY" < tu_ngay
            THEN JCCAD."SO_TIEN"
            ELSE 0
            END)
            , SUM(CASE WHEN JCP."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
            THEN JCCAD."SO_TIEN"
            ELSE 0
            END)
            , 0
            FROM gia_thanh_ky_tinh_gia_thanh JCP
            INNER JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung JCCAD
            ON JCCAD."KY_TINH_GIA_THANH_ID" = JCP."id"
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCP."CHI_NHANH_ID"
            INNER JOIN TMP_DS_DOI_TUONG_THCP J ON J."DOI_TUONG_THCP_ID" = JCCAD."MA_DOI_TUONG_THCP_ID"
            WHERE JCP."DEN_NGAY" <= den_ngay AND CHE_DO_KE_TOAN = '48' AND TON_TAI_TK_154 = TRUE


            GROUP BY J."OUT_DOI_TUONG_THCP_ID"

            UNION ALL
            SELECT
            J."OUT_DOI_TUONG_THCP_ID" AS "DOI_TUONG_THCP_ID"
            , A."SO_TAI_KHOAN"
            , A."TAI_KHOAN_ID"
            , SUM(CASE WHEN JCP."DEN_NGAY" < tu_ngay
            THEN JCCAD."SO_TIEN"
            ELSE 0
            END)
            , SUM(CASE WHEN JCP."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
            THEN JCCAD."SO_TIEN"
            ELSE 0
            END)
            , 0
            FROM gia_thanh_ky_tinh_gia_thanh JCP
            INNER JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung JCCAD
            ON JCCAD."KY_TINH_GIA_THANH_ID" = JCP."id"
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCP."CHI_NHANH_ID"
            INNER JOIN TMP_DS_DOI_TUONG_THCP J ON J."DOI_TUONG_THCP_ID" = JCCAD."MA_DOI_TUONG_THCP_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN"
            FROM danh_muc_he_thong_tai_khoan TK
            WHERE TK.id = JCCAD."TAI_KHOAN_ID") LIKE
            A."AccountNumberPercent"
            WHERE JCP."DEN_NGAY" <= den_ngay AND CHE_DO_KE_TOAN = '15'

            GROUP BY J."OUT_DOI_TUONG_THCP_ID",
            A."SO_TAI_KHOAN"

            UNION ALL
            SELECT
            J."OUT_DOI_TUONG_THCP_ID" AS "DOI_TUONG_THCP_ID"
            , A."SO_TAI_KHOAN"
            , A."TAI_KHOAN_ID"
            , SUM(JC."TONG_CHI_PHI")
            , 0
            , 0
            FROM account_ex_chi_phi_do_dang JC
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JC."CHI_NHANH_ID"
            INNER JOIN TMP_DS_DOI_TUONG_THCP J ON J."DOI_TUONG_THCP_ID" = JC."MA_DOI_TUONG_THCP_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN"
            FROM danh_muc_he_thong_tai_khoan TK
            WHERE TK.id = JC."TAI_KHOAN_CPSXKD_DO_DANG_ID") LIKE
            A."AccountNumberPercent"


            GROUP BY J."OUT_DOI_TUONG_THCP_ID",
            A."SO_TAI_KHOAN"
            ) D
            INNER JOIN TMP_DOI_TUONG_THCP P ON D."DOI_TUONG_THCP_ID" = P."DOI_TUONG_THCP_ID"
            LEFT JOIN TMP_DOI_TUONG_THCP_CHA PP ON PP."DOI_TUONG_THCP_ID" = D."DOI_TUONG_THCP_ID"
            INNER JOIN TMP_BAC_DOI_TUONG_THCP GP ON GP."DOI_TUONG_THCP_ID" = D."DOI_TUONG_THCP_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON A."SO_TAI_KHOAN" = D."SO_TAI_KHOAN"
            GROUP BY
            P."MA_PHAN_CAP",
            D."DOI_TUONG_THCP_ID",
            CONCAT(REPEAT('', cast(GP."BAC" * 4 AS INT)
            ), P."MA_DOI_TUONG_THCP"),
            P."TEN_DOI_TUONG_THCP",
            D."SO_TAI_KHOAN",
            CAST(CASE WHEN GP."BAC" = 0
            THEN 1
            ELSE 0
            END AS BIT
            ),
            CAST(CASE WHEN PP."DOI_TUONG_THCP_ID" IS NULL
            THEN 0
            ELSE 1
            END AS BIT
            ),
            A."TAI_KHOAN_ID",
            A."TINH_CHAT",
            D."TAI_KHOAN_ID"
            HAVING SUM(D."SO_DU_DAU_KY"
            ) <> 0
            OR SUM(D."PHAT_SINH_NO"
            ) <> 0
            OR SUM(D."QUY_DOI"
            ) <> 0
            ;


            END $$
            ;

            SELECT 
            "MA_DOI_TUONG_THCP" AS"MA_DOI_TUONG_THCP",
            "TEN_DOI_TUONG_THCP" AS "TEN_DOI_TUONG_THCP",
            "SO_TAI_KHOAN" AS "SO_TAI_KHOAN",
            "NO_DAU_KY" AS "NO_DAU_KY",
            "CO_DAU_KY" AS"CO_DAU_KY",
            "PHAT_SINH_NO" AS "PHAT_SINH_NO",
            "PHAT_SINH_CO" AS"PHAT_SINH_CO",
            "NO_CUOI_KY" AS "NO_CUOI_KY",
            "CO_CUOI_KY" AS"CO_CUOI_KY"
            
            FROM TMP_KET_QUA

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
            tu_ngay                             DATE := %(TU_NGAY)s;

            den_ngay                            DATE := %(DEN_NGAY)s;

            bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

            chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;


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

            DROP TABLE IF EXISTS TMP_SO_TAI_KHOAN
            ;

            CREATE TEMP TABLE TMP_SO_TAI_KHOAN


            (
            "SO_TAI_KHOAN"         VARCHAR(20) PRIMARY KEY,
            "TAI_KHOAN_ID"         INT,
            "AccountNumberPercent" VARCHAR(25),
            "TINH_CHAT"            VARCHAR(25)
            )
            ;

            INSERT INTO TMP_SO_TAI_KHOAN
            SELECT
            A."SO_TAI_KHOAN"
            , A."id"
            , A."SO_TAI_KHOAN" || '%%'
            , A."TINH_CHAT"
            FROM danh_muc_he_thong_tai_khoan A
            WHERE id = any(%(TAI_KHOAN_IDS)s) --@ListAccountID
            ;

            IF EXISTS(SELECT "SO_TAI_KHOAN"
            FROM TMP_SO_TAI_KHOAN
            WHERE "SO_TAI_KHOAN" LIKE '154%%'
            LIMIT 1)
            THEN
            TON_TAI_TK_154 = TRUE
            ;
            ELSE
            TON_TAI_TK_154 = FALSE
            ;
            END IF
            ;


            SELECT "SO_TAI_KHOAN"
            INTO SO_TK_154
            FROM TMP_SO_TAI_KHOAN
            WHERE "SO_TAI_KHOAN" LIKE '154%%'
            ORDER BY "SO_TAI_KHOAN"
            LIMIT 1
            ;

            SELECT "TAI_KHOAN_ID"
            INTO TAI_KHOAN_ID_154
            FROM TMP_SO_TAI_KHOAN
            WHERE "SO_TAI_KHOAN" LIKE '154%%'
            ORDER BY "SO_TAI_KHOAN"
            LIMIT 1
            ;

            -- Lấy lên tiết khoản con đầu tiên


            DROP TABLE IF EXISTS TMP_CONG_TRINH
            ;

            CREATE TEMP TABLE TMP_CONG_TRINH-- Bảng công trình được chọn từ form tham số
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

            FROM danh_muc_cong_trinh PW
            WHERE PW."id" = any (%(CONG_TRINH_IDS)s)

            ;

            DROP TABLE IF EXISTS TMP_DS_CONG_TRINH
            ;

            CREATE TEMP TABLE TMP_DS_CONG_TRINH
            -- Bảng công trình gồm toàn bộ công trình con
            (
            "CONG_TRINH_ID"     INT,
            "OUT_CONG_TRINH_ID" INT
            )
            ;

            INSERT INTO TMP_DS_CONG_TRINH
            SELECT
            PW."id"
            , tPW."CONG_TRINH_ID"
            FROM TMP_CONG_TRINH tPW
            INNER JOIN danh_muc_cong_trinh PW ON PW."MA_PHAN_CAP" LIKE tPW."MA_PHAN_CAP"
            || '%%'
            GROUP BY
            PW."id",
            tPW."CONG_TRINH_ID"
            ;


            DROP TABLE IF EXISTS TMP_BAC_CONG_TRINH
            ;

            CREATE TEMP TABLE TMP_BAC_CONG_TRINH -- Tính bậc để lùi dòng cho báo cáo hình cây
            (
            "CONG_TRINH_ID" INT PRIMARY KEY,
            "BAC"           INT
            )
            ;

            INSERT INTO TMP_BAC_CONG_TRINH
            SELECT
            P."CONG_TRINH_ID"
            , COUNT(PD."MA_PHAN_CAP") AS "BAC"
            FROM TMP_CONG_TRINH P
            LEFT JOIN TMP_CONG_TRINH PD ON P."MA_PHAN_CAP" LIKE PD."MA_PHAN_CAP"
            || '%%'
            AND P."MA_PHAN_CAP" <> PD."MA_PHAN_CAP"
            GROUP BY P."CONG_TRINH_ID"
            ;

            -- Bảng các khoản mục CP cha được chọn trong đó có chọn cả con mà là cha

            DROP TABLE IF EXISTS TMP_CONG_TRINH_CHA
            ;

            CREATE TEMP TABLE TMP_CONG_TRINH_CHA
            (
            "CONG_TRINH_ID" INT PRIMARY KEY
            )
            ;

            INSERT INTO TMP_CONG_TRINH_CHA
            SELECT DISTINCT PD."CONG_TRINH_ID"
            FROM TMP_CONG_TRINH P
            LEFT JOIN TMP_CONG_TRINH PD ON P."MA_PHAN_CAP" LIKE PD."MA_PHAN_CAP"
            || '%%'
            AND P."MA_PHAN_CAP" <> PD."MA_PHAN_CAP"
            WHERE PD."MA_PHAN_CAP" IS NOT NULL
            ;

            DROP TABLE IF EXISTS TMP_KET_QUA
            ;

            CREATE TEMP TABLE TMP_KET_QUA
            AS

            SELECT
            ROW_NUMBER()
            OVER (
            ORDER BY D."SO_TAI_KHOAN", P."MA_PHAN_CAP" )                 AS RowNum
            , D."CONG_TRINH_ID"
            , CONCAT(REPEAT('', CAST(GP."BAC" * 4 AS INT)), P."MA_CONG_TRINH") AS "MA_CONG_TRINH"
            , P."TEN_CONG_TRINH"
            , PWC."name"                                                       AS "LOAI_CONG_TRINH"
            , D."SO_TAI_KHOAN"
            , D."TAI_KHOAN_ID"
            , CASE WHEN SUM(D."SO_DU_DAU_KY") > 0
            THEN SUM(D."SO_DU_DAU_KY")
            ELSE 0
            END                                                              AS "NO_DAU_KY"
            , CASE WHEN SUM(D."SO_DU_DAU_KY") < 0
            THEN -1 * SUM(D."SO_DU_DAU_KY")
            ELSE 0
            END                                                              AS "CO_DAU_KY"
            , SUM(D."PHAT_SINH_NO")                                            AS "PHAT_SINH_NO"
            , SUM(D."QUY_DOI")                                                 AS "PHAT_SINH_CO"
            , CASE WHEN SUM(D."SO_DU_DAU_KY" + D."PHAT_SINH_NO"
            - D."QUY_DOI") > 0
            THEN SUM(D."SO_DU_DAU_KY" + D."PHAT_SINH_NO"
            - D."QUY_DOI")
            ELSE 0
            END                                                              AS "NO_CUOI_KY"
            , CASE WHEN SUM(D."SO_DU_DAU_KY" + D."PHAT_SINH_NO"
            - D."QUY_DOI") < 0
            THEN SUM(D."QUY_DOI" - D."SO_DU_DAU_KY"
            - D."PHAT_SINH_NO")
            ELSE 0
            END                                                              AS "CO_CUOI_KY"
            FROM (SELECT
            Pw."OUT_CONG_TRINH_ID" AS "CONG_TRINH_ID"
            , A."SO_TAI_KHOAN"
            , A."TAI_KHOAN_ID"
            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
            THEN GL."GHI_NO" - GL."GHI_CO"
            ELSE 0
            END)               AS "SO_DU_DAU_KY"
            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            THEN GL."GHI_NO"
            ELSE 0
            END)               AS "PHAT_SINH_NO"
            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            THEN GL."GHI_CO"
            ELSE 0
            END)               AS "QUY_DOI"
            FROM so_cai_chi_tiet GL
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON GL."MA_TAI_KHOAN" LIKE A."AccountNumberPercent"
            INNER JOIN TMP_DS_CONG_TRINH PW ON PW."CONG_TRINH_ID" = GL."CONG_TRINH_ID"
            WHERE GL."NGAY_HACH_TOAN" <= den_ngay
            AND (GL."LOAI_CHUNG_TU" <> '610' OR
            (GL."LOAI_CHUNG_TU" = '610' AND
            GL."MA_TAI_KHOAN" NOT LIKE
            N'154%%')) -- ntquang 30/08/2017 - không lấy phát sinh của tk 154 ở số dư đầu kỳ
            GROUP BY
            Pw."OUT_CONG_TRINH_ID",
            A."SO_TAI_KHOAN"
            UNION ALL
            SELECT
            Pw."OUT_CONG_TRINH_ID" AS "CONG_TRINH_ID"
            , A."SO_TAI_KHOAN"
            , A."TAI_KHOAN_ID"
            , SUM(CASE WHEN JCP."DEN_NGAY" < tu_ngay
            THEN JCCAD."SO_TIEN"
            ELSE 0
            END)
            , SUM(CASE WHEN JCP."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
            THEN JCCAD."SO_TIEN"
            ELSE 0
            END)
            , 0
            FROM gia_thanh_ky_tinh_gia_thanh JCP
            INNER JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung JCCAD
            ON JCCAD."KY_TINH_GIA_THANH_ID" = JCP."id"
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCP."CHI_NHANH_ID"
            INNER JOIN TMP_DS_CONG_TRINH PW ON PW."CONG_TRINH_ID" = JCCAD."MA_CONG_TRINH_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN"
            FROM danh_muc_he_thong_tai_khoan TK
            WHERE TK.id = JCCAD."TAI_KHOAN_ID") LIKE
            A."AccountNumberPercent"
            WHERE JCP."DEN_NGAY" <= den_ngay
            AND CHE_DO_KE_TOAN = '15'

            GROUP BY
            Pw."OUT_CONG_TRINH_ID",
            A."SO_TAI_KHOAN"
            UNION ALL
            SELECT
            Pw."OUT_CONG_TRINH_ID" AS "CONG_TRINH_ID"
            , SO_TK_154
            , TAI_KHOAN_ID_154
            , SUM(CASE WHEN JCP."DEN_NGAY" < tu_ngay
            THEN JCCAD."SO_TIEN"
            ELSE 0
            END)
            , SUM(CASE WHEN JCP."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
            THEN JCCAD."SO_TIEN"
            ELSE 0
            END)
            , 0
            FROM gia_thanh_ky_tinh_gia_thanh JCP
            INNER JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung JCCAD
            ON JCCAD."KY_TINH_GIA_THANH_ID" = JCP."id"
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCP."CHI_NHANH_ID"
            INNER JOIN TMP_DS_CONG_TRINH PW ON PW."CONG_TRINH_ID" = JCCAD."MA_CONG_TRINH_ID"

            WHERE JCP."DEN_NGAY" <= den_ngay
            AND CHE_DO_KE_TOAN = '48'
            AND TON_TAI_TK_154 = TRUE

            GROUP BY Pw."OUT_CONG_TRINH_ID"
            UNION ALL
            SELECT
            Pw."OUT_CONG_TRINH_ID" AS "CONG_TRINH_ID"
            , A."SO_TAI_KHOAN"
            , A."TAI_KHOAN_ID"
            , SUM(CASE WHEN JCAE."NGAY_CHUNG_TU" < tu_ngay
            THEN JCAEDT."SO_TIEN"
            ELSE 0
            END)
            , SUM(CASE WHEN JCAE."NGAY_CHUNG_TU" BETWEEN tu_ngay AND den_ngay
            THEN JCAEDT."SO_TIEN"
            ELSE 0
            END)
            , 0
            FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JCAE
            INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCAEDT
            ON JCAEDT."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JCAE."id"
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCAE."CHI_NHANH_ID"
            INNER JOIN TMP_DS_CONG_TRINH PW ON PW."CONG_TRINH_ID" = JCAEDT."MA_DON_VI_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN"
            FROM danh_muc_he_thong_tai_khoan TK
            WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE
            A."AccountNumberPercent"
            WHERE JCAE."NGAY_CHUNG_TU" <= den_ngay
            AND JCAEDT."CAP_TO_CHUC" = '1'

            GROUP BY
            Pw."OUT_CONG_TRINH_ID",
            A."SO_TAI_KHOAN"
            UNION ALL
            SELECT
            Pw."OUT_CONG_TRINH_ID" AS "CONG_TRINH_ID"
            , A."SO_TAI_KHOAN"
            , A."TAI_KHOAN_ID"
            , SUM(JC."SO_CHUA_NGHIEM_THU")
            , 0
            , 0
            FROM account_ex_chi_phi_do_dang JC
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JC."CHI_NHANH_ID"
            INNER JOIN TMP_DS_CONG_TRINH PW ON PW."CONG_TRINH_ID" = JC."MA_CONG_TRINH_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN"
            FROM danh_muc_he_thong_tai_khoan TK
            WHERE TK.id = JC."TAI_KHOAN_CPSXKD_DO_DANG_ID") LIKE
            A."AccountNumberPercent"

            GROUP BY Pw."OUT_CONG_TRINH_ID",
            A."SO_TAI_KHOAN"
            ) D
            INNER JOIN TMP_CONG_TRINH P ON D."CONG_TRINH_ID" = P."CONG_TRINH_ID"
            LEFT JOIN danh_muc_loai_cong_trinh PWC ON P."LOAI_CONG_TRINH" = PWC."id"
            LEFT JOIN TMP_CONG_TRINH_CHA PP ON PP."CONG_TRINH_ID" = D."CONG_TRINH_ID"
            INNER JOIN TMP_BAC_CONG_TRINH GP ON GP."CONG_TRINH_ID" = D."CONG_TRINH_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON A."SO_TAI_KHOAN" = D."SO_TAI_KHOAN"
            GROUP BY
            P."MA_PHAN_CAP",
            D."CONG_TRINH_ID",
            CONCAT(REPEAT('', CAST(GP."BAC" * 4 AS INT)), P."MA_CONG_TRINH"),
            P."TEN_CONG_TRINH",
            PWC."name",
            D."SO_TAI_KHOAN",
            CAST(CASE WHEN GP."BAC" = 0
            THEN 1
            ELSE 0
            END AS BIT
            ),
            CAST(CASE WHEN PP."CONG_TRINH_ID" IS NULL
            THEN 0
            ELSE 1
            END AS BIT
            ),
            A."TAI_KHOAN_ID",
            A."TINH_CHAT",
            D."TAI_KHOAN_ID"
            HAVING SUM(D."SO_DU_DAU_KY"
            ) <> 0
            OR SUM(D."PHAT_SINH_NO"
            ) <> 0
            OR SUM(D."QUY_DOI"
            ) <> 0
            ;


            END $$
            ;
            SELECT 
            "MA_CONG_TRINH" AS"MA_CONG_TRINH",
            "TEN_CONG_TRINH" AS "TEN_CONG_TRINH",
            "SO_TAI_KHOAN" AS "SO_TAI_KHOAN",
            "NO_DAU_KY" AS "NO_DAU_KY",
            "CO_DAU_KY" AS"CO_DAU_KY",
            "PHAT_SINH_NO" AS "PHAT_SINH_NO",
            "PHAT_SINH_CO" AS"PHAT_SINH_CO",
            "NO_CUOI_KY" AS "NO_CUOI_KY",
            "CO_CUOI_KY" AS"CO_CUOI_KY"

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
            tu_ngay                             DATE :=  %(TU_NGAY)s; 

            den_ngay                            DATE := %(DEN_NGAY)s; 

            bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s; 

            chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s; 


            TON_TAI_TK_154                      BOOLEAN;

            SO_TK_154                           VARCHAR;


            TAI_KHOAN_ID_154                    INTEGER;

            CHE_DO_KE_TOAN                      VARCHAR;

            rec                                 RECORD;

            --@@ListSAOrderID --Tham số bên misa
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

            DROP TABLE IF EXISTS TMP_SO_TAI_KHOAN
            ;

            CREATE TEMP TABLE TMP_SO_TAI_KHOAN


            (
            "SO_TAI_KHOAN"         VARCHAR(20) PRIMARY KEY,
            "TAI_KHOAN_ID"         INT,
            "AccountNumberPercent" VARCHAR(25),
            "TINH_CHAT"            VARCHAR(25)
            )
            ;

            INSERT INTO TMP_SO_TAI_KHOAN
            SELECT
            A."SO_TAI_KHOAN"
            , A."id"
            , A."SO_TAI_KHOAN" || '%%'
            , A."TINH_CHAT"
            FROM danh_muc_he_thong_tai_khoan A
            WHERE id = any (%(TAI_KHOAN_IDS)s) --@ListAccountID
            ;

            IF EXISTS(SELECT "SO_TAI_KHOAN"
            FROM TMP_SO_TAI_KHOAN
            WHERE "SO_TAI_KHOAN" LIKE '154%%'
            LIMIT 1)
            THEN
            TON_TAI_TK_154 = TRUE
            ;
            ELSE
            TON_TAI_TK_154 = FALSE
            ;
            END IF
            ;

            SELECT "SO_TAI_KHOAN"
            INTO SO_TK_154
            FROM TMP_SO_TAI_KHOAN
            WHERE "SO_TAI_KHOAN" LIKE '154%%'
            ORDER BY "SO_TAI_KHOAN"
            LIMIT 1
            ;
            SELECT "TAI_KHOAN_ID"
            INTO TAI_KHOAN_ID_154
            FROM TMP_SO_TAI_KHOAN
            WHERE "SO_TAI_KHOAN" LIKE '154%%'
            ORDER BY "SO_TAI_KHOAN"
            LIMIT 1
            ;

            DROP TABLE IF EXISTS TMP_DON_HANG
            ;

            CREATE TEMP TABLE TMP_DON_HANG

            (
            "ID_CHUNG_TU"   INT PRIMARY KEY,
            "SO_CHUNG_TU"   VARCHAR(25),
            "NGAY_CHUNG_TU" TIMESTAMP
            )
            ;
            INSERT INTO TMP_DON_HANG
            SELECT
            SAO."id" AS "DON_HANG_ID"
            , SAO."SO_DON_HANG"
            , SAO."NGAY_DON_HANG"
            FROM
            account_ex_don_dat_hang SAO
            WHERE SAO."id" = any (%(DON_HANG_IDS)s)
            ;
            --@ListSAOrderID

            DROP TABLE IF EXISTS TMP_KET_QUA
            ;

            CREATE TEMP TABLE TMP_KET_QUA
            AS

            SELECT
            ROW_NUMBER()
            OVER (
            ORDER BY D."SO_TAI_KHOAN", SAO."SO_CHUNG_TU" ) AS RowNum
            , D."ID_CHUNG_TU"                                  AS "DON_HANG_ID"
            , SAO."SO_CHUNG_TU"                                AS "SO_DON_HANG"
            , SAO."NGAY_CHUNG_TU"                              AS "NGAY_DON_HANG"
            , D."SO_TAI_KHOAN"
            , D."TAI_KHOAN_ID"
            , CASE WHEN SUM(D."SO_DU_DAU_KY") > 0
            THEN SUM(D."SO_DU_DAU_KY")
            ELSE 0
            END                                              AS "NO_DAU_KY"
            , CASE WHEN SUM(D."SO_DU_DAU_KY") < 0
            THEN -1 * SUM(D."SO_DU_DAU_KY")
            ELSE 0
            END                                              AS "CO_DAU_KY"
            , SUM(D."PHAT_SINH_NO")                            AS "PHAT_SINH_NO"
            , SUM(D."QUY_DOI")                                 AS "PHAT_SINH_CO"
            , CASE WHEN SUM(D."SO_DU_DAU_KY" + D."PHAT_SINH_NO"
            - D."QUY_DOI") > 0
            THEN SUM(D."SO_DU_DAU_KY" + D."PHAT_SINH_NO"
            - D."QUY_DOI")
            ELSE 0
            END                                              AS "NO_CUOI_KY"
            , CASE WHEN SUM(D."SO_DU_DAU_KY" + D."PHAT_SINH_NO"
            - D."QUY_DOI") < 0
            THEN SUM(D."QUY_DOI" - D."SO_DU_DAU_KY"
            - D."PHAT_SINH_NO")
            ELSE 0
            END                                              AS "CO_CUOI_KY"

            FROM (SELECT
            SAO."ID_CHUNG_TU"
            , A."SO_TAI_KHOAN"
            , A."TAI_KHOAN_ID"
            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
            THEN GL."GHI_NO" - GL."GHI_CO"
            ELSE 0
            END) AS "SO_DU_DAU_KY"
            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            THEN GL."GHI_NO"
            ELSE 0
            END) AS "PHAT_SINH_NO"
            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            THEN GL."GHI_CO"
            ELSE 0
            END) AS "QUY_DOI"
            FROM so_cai_chi_tiet GL
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON GL."MA_TAI_KHOAN" LIKE A."AccountNumberPercent"
            INNER JOIN TMP_DON_HANG SAO ON SAO."ID_CHUNG_TU" = GL."DON_DAT_HANG_ID"
            WHERE GL."NGAY_HACH_TOAN" <= den_ngay
            AND (GL."LOAI_CHUNG_TU" <> '610' OR (GL."LOAI_CHUNG_TU" = '610' AND GL."MA_TAI_KHOAN" NOT LIKE
                            N'154%%')) -- ntquang 30/08/2017 - không lấy phát sinh của tk 154 ở số dư đầu kỳ
            GROUP BY
            SAO."ID_CHUNG_TU",
            A."SO_TAI_KHOAN"
            UNION ALL
            SELECT
            SAO."ID_CHUNG_TU"
            , A."SO_TAI_KHOAN"
            , A."TAI_KHOAN_ID"
            , SUM(CASE WHEN JCP."DEN_NGAY" < tu_ngay
            THEN JCCAD."SO_TIEN"
            ELSE 0
            END) AS "SO_DU_DAU_KY"
            , SUM(CASE WHEN JCP."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
            THEN JCCAD."SO_TIEN"
            ELSE 0
            END) AS "PHAT_SINH_NO"
            , 0        AS "QUY_DOI"
            FROM gia_thanh_ky_tinh_gia_thanh JCP
            INNER JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung JCCAD
            ON JCCAD."KY_TINH_GIA_THANH_ID" = JCP."id"
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCP."CHI_NHANH_ID"
            INNER JOIN TMP_DON_HANG SAO ON SAO."ID_CHUNG_TU" = JCCAD."SO_DON_HANG_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN"  FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCCAD."TAI_KHOAN_ID") LIKE A."AccountNumberPercent"
            WHERE JCP."DEN_NGAY" <= den_ngay
            AND CHE_DO_KE_TOAN = '15'

            GROUP BY SAO."ID_CHUNG_TU",
            A."SO_TAI_KHOAN"
            UNION ALL
            SELECT
            SAO."ID_CHUNG_TU"
            , SO_TK_154
            ,TAI_KHOAN_ID_154
            , SUM(CASE WHEN JCP."DEN_NGAY" < tu_ngay
            THEN JCCAD."SO_TIEN"
            ELSE 0
            END) AS "SO_DU_DAU_KY"
            , SUM(CASE WHEN JCP."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
            THEN JCCAD."SO_TIEN"
            ELSE 0
            END) AS "PHAT_SINH_NO"
            , 0        AS "QUY_DOI"
            FROM gia_thanh_ky_tinh_gia_thanh JCP
            INNER JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung JCCAD
            ON JCCAD."KY_TINH_GIA_THANH_ID" = JCP."id"
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCP."CHI_NHANH_ID"
            INNER JOIN TMP_DON_HANG SAO ON SAO."ID_CHUNG_TU" = JCCAD."SO_DON_HANG_ID"

            WHERE JCP."DEN_NGAY" <= den_ngay
            AND CHE_DO_KE_TOAN = '48'
            AND TON_TAI_TK_154 = TRUE 

            GROUP BY SAO."ID_CHUNG_TU"
            UNION ALL
            SELECT
            SAO."ID_CHUNG_TU"
            , A."SO_TAI_KHOAN"
            , A."TAI_KHOAN_ID"
            , SUM(CASE WHEN JCAE."NGAY_CHUNG_TU" < tu_ngay
            THEN JCAEDT."SO_TIEN"
            ELSE 0
            END) AS "SO_DU_DAU_KY"
            , SUM(CASE WHEN JCAE."NGAY_CHUNG_TU" BETWEEN tu_ngay AND den_ngay
            THEN JCAEDT."SO_TIEN"
            ELSE 0
            END) AS "PHAT_SINH_NO"
            , 0        AS "QUY_DOI"
            FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JCAE
            INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCAEDT
            ON JCAEDT."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JCAE."id"
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCAE."CHI_NHANH_ID"
            INNER JOIN TMP_DON_HANG SAO ON SAO."ID_CHUNG_TU" = JCAEDT."MA_DON_VI_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE A."AccountNumberPercent"
            WHERE JCAE."NGAY_CHUNG_TU" <= den_ngay
            AND JCAEDT."CAP_TO_CHUC" = '2'

            GROUP BY
            SAO."ID_CHUNG_TU",
            A."SO_TAI_KHOAN"
            UNION ALL
            SELECT
            SAO."ID_CHUNG_TU"
            , A."SO_TAI_KHOAN"
            , A."TAI_KHOAN_ID"
            , SUM(JC."SO_CHUA_NGHIEM_THU") AS "SO_DU_DAU_KY"
            , 0                            AS "PHAT_SINH_NO"
            , 0                            AS "QUY_DOI"
            FROM account_ex_chi_phi_do_dang JC
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JC."CHI_NHANH_ID"
            INNER JOIN TMP_DON_HANG SAO ON SAO."ID_CHUNG_TU" = JC."DON_HANG_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id= JC."TAI_KHOAN_CPSXKD_DO_DANG_ID") LIKE A."AccountNumberPercent"

            GROUP BY 
            SAO."ID_CHUNG_TU",
            A."SO_TAI_KHOAN"
            ) D
            INNER JOIN TMP_DON_HANG SAO ON SAO."ID_CHUNG_TU" = D."ID_CHUNG_TU"
            INNER JOIN TMP_SO_TAI_KHOAN A ON A."SO_TAI_KHOAN" = D."SO_TAI_KHOAN"
            GROUP BY
            D."ID_CHUNG_TU",
            SAO."SO_CHUNG_TU",
            SAO."NGAY_CHUNG_TU",
            D."SO_TAI_KHOAN",
            A."TAI_KHOAN_ID",
            A."TINH_CHAT",
            D."TAI_KHOAN_ID"
            HAVING SUM(D."SO_DU_DAU_KY") <> 0
            OR SUM(D."PHAT_SINH_NO") <> 0
            OR SUM(D."QUY_DOI") <> 0
            ;


            END $$
            ;
            SELECT 
                "SO_DON_HANG" AS "SO_DON_HANG",
                "NGAY_DON_HANG" AS "NGAY_DON_HANG",
                "SO_TAI_KHOAN" AS "SO_TAI_KHOAN",
                "NO_DAU_KY" AS "NO_DAU_KY",
                "CO_DAU_KY" AS "CO_DAU_KY",
                "PHAT_SINH_NO" AS "PHAT_SINH_NO",
                "PHAT_SINH_CO" AS "PHAT_SINH_CO",
                "NO_CUOI_KY" AS "NO_CUOI_KY",
                "CO_CUOI_KY" AS "CO_CUOI_KY"

            FROM TMP_KET_QUA
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
            tu_ngay                             DATE := %(TU_NGAY)s;

            den_ngay                            DATE := %(DEN_NGAY)s;

            bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

            chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;


            TON_TAI_TK_154                      BOOLEAN;

            SO_TK_154                           VARCHAR;


            TAI_KHOAN_ID_154                    INTEGER;

            CHE_DO_KE_TOAN                      VARCHAR;

            rec                                 RECORD;

            --@ListContractID --Tham số bên misa
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

            DROP TABLE IF EXISTS TMP_SO_TAI_KHOAN
            ;

            CREATE TEMP TABLE TMP_SO_TAI_KHOAN


            (
            "SO_TAI_KHOAN"         VARCHAR(20) PRIMARY KEY,
            "TAI_KHOAN_ID"         INT,
            "AccountNumberPercent" VARCHAR(25),
            "TINH_CHAT"            VARCHAR(25)
            )
            ;

            INSERT INTO TMP_SO_TAI_KHOAN
            SELECT
            A."SO_TAI_KHOAN"
            , A."id"
            , A."SO_TAI_KHOAN" || '%%'
            , A."TINH_CHAT"
            FROM danh_muc_he_thong_tai_khoan A
            WHERE id = any (%(TAI_KHOAN_IDS)s) --@ListAccountID
            ;

            IF EXISTS(SELECT "SO_TAI_KHOAN"
            FROM TMP_SO_TAI_KHOAN
            WHERE "SO_TAI_KHOAN" LIKE '154%%'
            LIMIT 1)
            THEN
            TON_TAI_TK_154 = TRUE
            ;
            ELSE
            TON_TAI_TK_154 = FALSE
            ;
            END IF
            ;

            SELECT "SO_TAI_KHOAN"
            INTO SO_TK_154
            FROM TMP_SO_TAI_KHOAN
            WHERE "SO_TAI_KHOAN" LIKE '154%%'
            ORDER BY "SO_TAI_KHOAN"
            LIMIT 1
            ;

            SELECT "TAI_KHOAN_ID"
            INTO TAI_KHOAN_ID_154
            FROM TMP_SO_TAI_KHOAN
            WHERE "SO_TAI_KHOAN" LIKE '154%%'
            ORDER BY "SO_TAI_KHOAN"
            LIMIT 1
            ;


            DROP TABLE IF EXISTS TMP_HOP_DONG
            ;

            CREATE TEMP TABLE TMP_HOP_DONG
            -- Bảng công trình được chọn từ form tham số
            (
            "HOP_DONG_ID"    INT PRIMARY KEY,
            "SO_HOP_DONG"    VARCHAR(50),
            "TRICH_YEU"      VARCHAR(255),
            "THUOC_DU_AN_ID" INT
            )
            ;

            INSERT INTO TMP_HOP_DONG
            SELECT
            C."id"
            , C."SO_HOP_DONG"
            , C."TRICH_YEU"
            , C."THUOC_DU_AN_ID"
            FROM
            sale_ex_hop_dong_ban C
            WHERE C."id" = any (%(HOP_DONG_BAN_IDS)s) --ListContractID
            ;

            DROP TABLE IF EXISTS TMP_DS_HOP_DONG
            ;

            CREATE TEMP TABLE TMP_DS_HOP_DONG
            -- Bảng hợp đồng gồm toàn bộ hợp đồng con
            (
            "HOP_DONG_ID"     INT
            ,
            "OUT_HOP_DONG_ID" INT
            )
            ;

            INSERT INTO TMP_DS_HOP_DONG
            SELECT DISTINCT
            COALESCE(C."id", P."HOP_DONG_ID")
            , P."HOP_DONG_ID"
            FROM TMP_HOP_DONG P
            LEFT JOIN sale_ex_hop_dong_ban C ON C."THUOC_DU_AN_ID" = P."HOP_DONG_ID" OR C."id" = P."HOP_DONG_ID"

            GROUP BY COALESCE(C."id", P."HOP_DONG_ID"),
            P."HOP_DONG_ID"
            ;


            DROP TABLE IF EXISTS TMP_DU_AN
            ;

            CREATE TEMP TABLE TMP_DU_AN
            (
            "HOP_DONG_ID" INT
            ,
            "THUOC_DU_AN" VARCHAR(50)
            ,
            "STT"         INT
            )
            ;

            INSERT INTO TMP_DU_AN

            SELECT
            CT."HOP_DONG_ID"
            , COALESCE(C."SO_HOP_DONG", CT."SO_HOP_DONG")
            , CASE WHEN C."SO_HOP_DONG" IS NULL
            THEN 0
            ELSE 1 END
            FROM TMP_HOP_DONG CT
            LEFT JOIN TMP_HOP_DONG P ON P."HOP_DONG_ID" = CT."THUOC_DU_AN_ID"
            LEFT JOIN sale_ex_hop_dong_ban C ON C."id" = P."HOP_DONG_ID"
            GROUP BY CT."HOP_DONG_ID"
            , COALESCE(C."SO_HOP_DONG", CT."SO_HOP_DONG")
            , CASE WHEN C."SO_HOP_DONG" IS NULL
            THEN 0
            ELSE 1 END
            ;

            -- Bảng các Hợp đồng cha được chọn trong đó có chọn cả con mà là cha

            DROP TABLE IF EXISTS TMP_HOP_DONG_CHA
            ;

            CREATE TEMP TABLE TMP_HOP_DONG_CHA

            (
            "HOP_DONG_ID" INT PRIMARY KEY
            )
            ;

            INSERT INTO TMP_HOP_DONG_CHA
            SELECT DISTINCT PD."HOP_DONG_ID"
            FROM TMP_HOP_DONG P
            LEFT JOIN TMP_HOP_DONG PD ON P."THUOC_DU_AN_ID" = PD."HOP_DONG_ID"
            WHERE PD."HOP_DONG_ID" IS NOT NULL
            ;

            DROP TABLE IF EXISTS TMP_KET_QUA
            ;

            CREATE TEMP TABLE TMP_KET_QUA
            AS

            SELECT
            ROW_NUMBER()
            OVER (
            ORDER BY D."SO_TAI_KHOAN", P."THUOC_DU_AN", P."STT", CT."SO_HOP_DONG" ) AS RowNum
            , D."HOP_DONG_ID"
            , CASE WHEN CT."SO_HOP_DONG" = P."THUOC_DU_AN"
            THEN CT."SO_HOP_DONG"
            ELSE concat(REPEAT('',CAST(4 AS INT)) ,CT."SO_HOP_DONG") END                                        AS "HOP_DONG_DU_AN"
            , CT."TRICH_YEU"
            , D."SO_TAI_KHOAN"
            , D."TAI_KHOAN_ID"

            , CASE WHEN SUM(D."SO_DU_DAU_KY") > 0
            THEN SUM(D."SO_DU_DAU_KY")
            ELSE 0 END                                                                  AS "NO_DAU_KY"
            , CASE WHEN SUM(D."SO_DU_DAU_KY") < 0
            THEN -1 * SUM(D."SO_DU_DAU_KY")
            ELSE 0 END                                                                  AS "CO_DAU_KY"
            , SUM(D."PHAT_SINH_NO")                                                       AS "PHAT_SINH_NO"
            , SUM(D."QUY_DOI")                                                            AS "PHAT_SINH_CO"
            , CASE WHEN SUM(D."SO_DU_DAU_KY" + D."PHAT_SINH_NO" - D."QUY_DOI") > 0
            THEN SUM(D."SO_DU_DAU_KY" + D."PHAT_SINH_NO" - D."QUY_DOI")
            ELSE 0 END                                                                  AS "NO_CUOI_KY"
            , CASE WHEN SUM(D."SO_DU_DAU_KY" + D."PHAT_SINH_NO" - D."QUY_DOI") < 0
            THEN SUM(D."QUY_DOI" - D."SO_DU_DAU_KY" - D."PHAT_SINH_NO")
            ELSE 0 END                                                                  AS "CO_CUOI_KY"

            FROM
            (
            SELECT
            CT."OUT_HOP_DONG_ID" AS "HOP_DONG_ID"

            , A."SO_TAI_KHOAN"
            , A."TAI_KHOAN_ID"
            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
            THEN GL."GHI_NO" - GL."GHI_CO"
            ELSE 0 END) AS "SO_DU_DAU_KY"
            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            THEN GL."GHI_NO"
            ELSE 0
            END)        AS "PHAT_SINH_NO"
            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
            THEN GL."GHI_CO"
            ELSE 0
            END)        AS "QUY_DOI"
            FROM so_cai_chi_tiet GL
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON GL."MA_TAI_KHOAN" LIKE A."AccountNumberPercent"
            INNER JOIN TMP_DS_HOP_DONG CT ON CT."HOP_DONG_ID" = GL."HOP_DONG_BAN_ID"
            WHERE GL."NGAY_HACH_TOAN" <= den_ngay
            AND (GL."LOAI_CHUNG_TU" <> '610' OR
            (GL."LOAI_CHUNG_TU" = '610'
            AND
            GL."MA_TAI_KHOAN" NOT LIKE
            N'154%%'
            )) -- ntquang 30/08/2017 - không lấy phát sinh của tk 154 ở số dư đầu kỳ
            GROUP BY
            CT."OUT_HOP_DONG_ID",
            A."SO_TAI_KHOAN"

            UNION ALL
            SELECT
            CT."OUT_HOP_DONG_ID" AS "HOP_DONG_ID"
            , A."SO_TAI_KHOAN"
            , A."TAI_KHOAN_ID"
            , SUM(CASE WHEN JCP."DEN_NGAY" < tu_ngay
            THEN JCCAD."SO_TIEN"
            ELSE 0 END)
            , SUM(CASE WHEN JCP."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
            THEN JCCAD."SO_TIEN"
            ELSE 0 END)
            , 0
            FROM gia_thanh_ky_tinh_gia_thanh JCP
            INNER JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung JCCAD
            ON JCCAD."KY_TINH_GIA_THANH_ID" = JCP."id"
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCP."CHI_NHANH_ID"
            INNER JOIN TMP_DS_HOP_DONG CT ON CT."HOP_DONG_ID" = JCCAD."SO_HOP_DONG_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCCAD."TAI_KHOAN_ID") LIKE A."AccountNumberPercent"

            WHERE JCP."DEN_NGAY" <= den_ngay AND CHE_DO_KE_TOAN = '15'

            GROUP BY
            CT."OUT_HOP_DONG_ID",
            A."SO_TAI_KHOAN"


            UNION ALL
            SELECT
            CT."OUT_HOP_DONG_ID" AS "HOP_DONG_ID"
            , SO_TK_154
            , TAI_KHOAN_ID_154
            , SUM(CASE WHEN JCP."DEN_NGAY" < tu_ngay
            THEN JCCAD."SO_TIEN"
            ELSE 0 END)
            , SUM(CASE WHEN JCP."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
            THEN JCCAD."SO_TIEN"
            ELSE 0 END)
            , 0
            FROM gia_thanh_ky_tinh_gia_thanh JCP
            INNER JOIN gia_thanh_ket_qua_phan_bo_chi_phi_chung JCCAD
            ON JCCAD."KY_TINH_GIA_THANH_ID" = JCP."id"
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCP."CHI_NHANH_ID"
            INNER JOIN TMP_DS_HOP_DONG CT ON CT."HOP_DONG_ID" = JCCAD."SO_HOP_DONG_ID"
            WHERE JCP."DEN_NGAY" <= den_ngay AND CHE_DO_KE_TOAN = '48' AND TON_TAI_TK_154 = TRUE

            GROUP BY CT."OUT_HOP_DONG_ID"


            UNION ALL
            SELECT
            CT."OUT_HOP_DONG_ID" AS "HOP_DONG_ID"
            , A."SO_TAI_KHOAN"
            , A."TAI_KHOAN_ID"
            , SUM(CASE WHEN JCAE."NGAY_CHUNG_TU" < tu_ngay
            THEN JCAEDT."SO_TIEN"
            ELSE 0 END)
            , SUM(CASE WHEN JCAE."NGAY_CHUNG_TU" BETWEEN tu_ngay AND den_ngay
            THEN JCAEDT."SO_TIEN"
            ELSE 0 END)
            , 0
            FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JCAE
            INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCAEDT
            ON JCAEDT."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JCAE."id"
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCAE."CHI_NHANH_ID"
            INNER JOIN TMP_DS_HOP_DONG CT ON CT."HOP_DONG_ID" = JCAEDT."MA_DON_VI_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE A."AccountNumberPercent"
            WHERE JCAE."NGAY_CHUNG_TU" <= den_ngay
            AND JCAEDT."CAP_TO_CHUC" = '3'

            GROUP BY
            CT."OUT_HOP_DONG_ID",
            A."SO_TAI_KHOAN"

            UNION ALL
            SELECT
            CT."OUT_HOP_DONG_ID" AS "HOP_DONG_ID"
            , A."SO_TAI_KHOAN"
            , A."TAI_KHOAN_ID"
            , SUM(JC."SO_CHUA_NGHIEM_THU")
            , 0
            , 0
            FROM account_ex_chi_phi_do_dang JC
            INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JC."CHI_NHANH_ID"
            INNER JOIN TMP_DS_HOP_DONG CT ON CT."HOP_DONG_ID" = JC."HOP_DONG_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON (SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JC."TAI_KHOAN_CPSXKD_DO_DANG_ID") LIKE A."AccountNumberPercent"

            GROUP BY
            CT."OUT_HOP_DONG_ID",
            A."SO_TAI_KHOAN"

            ) D
            INNER JOIN TMP_HOP_DONG CT ON D."HOP_DONG_ID" = CT."HOP_DONG_ID"
            INNER JOIN TMP_DU_AN P ON P."HOP_DONG_ID" = CT."HOP_DONG_ID"
            LEFT JOIN TMP_HOP_DONG_CHA PP ON PP."HOP_DONG_ID" = CT."HOP_DONG_ID"
            INNER JOIN TMP_SO_TAI_KHOAN A ON A."SO_TAI_KHOAN" = D."SO_TAI_KHOAN"
            GROUP BY
            P."THUOC_DU_AN"
            , P."STT"
            , CT."SO_HOP_DONG"
            , D."HOP_DONG_ID"
            , CASE WHEN CT."SO_HOP_DONG" = P."THUOC_DU_AN"
            THEN CT."SO_HOP_DONG"
            ELSE concat(REPEAT('',CAST(4 AS INT)) ,CT."SO_HOP_DONG") END
            , CT."TRICH_YEU"
            , D."SO_TAI_KHOAN"
            , CAST(CASE WHEN CT."SO_HOP_DONG" = P."THUOC_DU_AN"
            THEN 1
            ELSE 0 END AS BIT)
            , CAST(CASE WHEN PP."HOP_DONG_ID" IS NULL
            THEN 0
            ELSE 1 END AS BIT)
            , A."TAI_KHOAN_ID"
            , A."TINH_CHAT"
            , D."TAI_KHOAN_ID"
            HAVING
            SUM(D."SO_DU_DAU_KY") <> 0
            OR SUM(D."PHAT_SINH_NO") <> 0
            OR SUM(D."QUY_DOI") <> 0 ;


            END $$
            ;
            SELECT 
                "HOP_DONG_DU_AN" AS "HOP_DONG_DU_AN",
                "TRICH_YEU" AS "TRICH_YEU",
                "SO_TAI_KHOAN" AS "SO_TAI_KHOAN",
                "NO_DAU_KY" AS "NO_DAU_KY",
                "CO_DAU_KY" AS "CO_DAU_KY",
                "PHAT_SINH_NO" AS "PHAT_SINH_NO",
                "PHAT_SINH_CO" AS "PHAT_SINH_CO",
                "NO_CUOI_KY" AS "NO_CUOI_KY",
                "CO_CUOI_KY" AS "CO_CUOI_KY"

            FROM TMP_KET_QUA
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
            action = self.env.ref('bao_cao.open_report_gia_thanh_tong_hop_chi_phi_sxkd_dtthcp').read()[0]
        elif THONG_KE_THEO=='CONG_TRINH':
            action = self.env.ref('bao_cao.open_report_gia_thanh_tong_hop_chi_phi_sxkd_cong_trinh').read()[0]
        elif THONG_KE_THEO=='DON_HANG':
            action = self.env.ref('bao_cao.open_report_gia_thanh_tong_hop_chi_phi_sxkd_don_hang').read()[0]
        elif THONG_KE_THEO=='HOP_DONG':
            action = self.env.ref('bao_cao.open_report_gia_thanh_tong_hop_chi_phi_sxkd_hop_dong').read()[0]
        
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action