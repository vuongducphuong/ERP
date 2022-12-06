# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class bao_cao_gia_thanh_chi_tiet_lai_lo_theo_cong_trinh(models.Model):
    _name = 'bao.cao.gia.thanh.chi.tiet.lai.lo.theo.cong.trinh'
    _description = ''
    _inherit = ['mail.thread']
    _auto = False

    HIEN_THI_THEO = fields.Selection([('MAU_DOC', 'Mẫu dọc'),('MAU_NGANG', 'Mẫu ngang')], string='Hiển thị theo', help='Hiển thị theo',default='MAU_DOC',required=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh', required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI', required='True')
    TU = fields.Date(string='Từ ', help='Từ ', required='True', default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến', required='True', default=fields.Datetime.now)

    RowNum = fields.Integer(string='RowNum', help='RowNum')
    STT = fields.Integer(string='STT', help='SortOrder')
    TEN_BAO_CAO_VAT_TU = fields.Char(string='TEN_BAO_CAO_VAT_TU', help='ReportItemName')
    MA_CONG_TRINH = fields.Char(string='MA_CONG_TRINH', help='ProjectWorkCode')
    TEN_CONG_TRINH = fields.Char(string='TEN_CONG_TRINH', help='ProjectWorkName')
    LOAI_CONG_TRINH = fields.Char(string='LOAI_CONG_TRINH', help='ProjectWorkCategoryName')
    ID_CHUNG_TU = fields.Integer(string='ID_CHUNG_TU')
    MODEL_CHUNG_TU = fields.Char(string='MODEL_CHUNG_TU')
    LOAI_CHUNG_TU = fields.Char(string='LOAI_CHUNG_TU', help='RefType')
    SO_CHUNG_TU = fields.Char(string='SO_CHUNG_TU', help='RefNo')
    NGAY_HACH_TOAN = fields.Date(string='NGAY_HACH_TOAN', help='PostedDate')
    NGAY_CHUNG_TU = fields.Date(string='NGAY_CHUNG_TU', help='RefDate')
    NGAY_HOA_DON = fields.Date(string='NGAY_HOA_DON')
    SO_HOA_DON = fields.Char(string='SO_HOA_DON')
    DIEN_GIAI = fields.Char(string='DIEN_GIAI', help='Description')
    SO_TIEN = fields.Float(string='SO_TIEN', help='Amount',digits= decimal_precision.get_precision('VND'))
    isbold = fields.Boolean(string='isbold', help='IsBold')

    CONG_TRINH_ID = fields.Integer(string='CONG_TRINH_ID')
    MA_PHAN_CAP = fields.Char(string='MA_PHAN_CAP')
    DOANH_THU_PHAT_SINH = fields.Float(string='DOANH_THU_PHAT_SINH', help='SalesReceiptAmount',digits= decimal_precision.get_precision('VND'))
    DOANH_THU_THU_NHAP_KHAC = fields.Float(string='DOANH_THU_THU_NHAP_KHAC',digits= decimal_precision.get_precision('VND'))
    GIAM_TRU_DOANH_THU = fields.Float(string='GIAM_TRU_DOANH_THU', help='ReduceReceiptAmount',digits= decimal_precision.get_precision('VND'))
    GIA_VON = fields.Float(string='GIA_VON', help='SaleCostAmount',digits= decimal_precision.get_precision('VND'))
    CHI_PHI_BAN_HANG = fields.Float(string='CHI_PHI_BAN_HANG', help='SaleExpenditureAmount',digits= decimal_precision.get_precision('VND'))
    CHI_PHI_QUAN_LY = fields.Float(string='CHI_PHI_QUAN_LY', help='ManagementExpenditureAmount',digits= decimal_precision.get_precision('VND'))
    CHI_PHI_KHAC = fields.Float(string='CHI_PHI_KHAC', help='OtherExpenditureAmount',digits= decimal_precision.get_precision('VND'))
    DO_DANG_DAU_KY = fields.Float(string='DO_DANG_DAU_KY', help='OpenUncompletedAmount',digits= decimal_precision.get_precision('VND'))
    NGUYEN_VAT_LIEU = fields.Float(string='NGUYEN_VAT_LIEU', help='MatetialAmount',digits= decimal_precision.get_precision('VND'))
    NHAN_CONG = fields.Float(string='NHAN_CONG', help='LaborAmount',digits= decimal_precision.get_precision('VND'))
    MAY_THI_CONG = fields.Float(string='MAY_THI_CONG', help='MachineAmount',digits= decimal_precision.get_precision('VND'))
    CHI_PHI_CHUNG = fields.Float(string='CHI_PHI_CHUNG', help='GeneralAmount',digits= decimal_precision.get_precision('VND'))
    KHOAN_GIAM_GIA_THANH = fields.Float(string='KHOAN_GIAM_GIA_THANH', help='DiscountAmount',digits= decimal_precision.get_precision('VND'))
    DO_DANG_CUOI_KY = fields.Float(string='DO_DANG_CUOI_KY', help='CloseUncompletedAmount',digits= decimal_precision.get_precision('VND'))
    TONG_THANH_TOAN = fields.Float(string='TONG_THANH_TOAN', help='ReceiptAmount',digits= decimal_precision.get_precision('VND'))
    DOANH_THU_THUAN = fields.Float(string='DOANH_THU_THUAN', help='OrgReceiptAmount',digits= decimal_precision.get_precision('VND'))
    CHI_PHI_PHAT_SINH_CONG = fields.Float(string='CHI_PHI_PHAT_SINH_CONG', help='SumCostAmount',digits= decimal_precision.get_precision('VND'))
    LAI_LO = fields.Float(string='LAI_LO', help='ProfitAmount',digits= decimal_precision.get_precision('VND'))

    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')


    CONG_TRINH_IDS = fields.One2many ('danh.muc.cong.trinh')
    CHON_TAT_CA_CONG_TRINH = fields.Boolean('Tất cả công trình', default=True)
    CONG_TRINH_MANY_IDS = fields.Many2many('danh.muc.cong.trinh','chi_tiet_lai_lo_cong_trinh', string='Chọn công trình') 

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
        result = super(bao_cao_gia_thanh_chi_tiet_lai_lo_theo_cong_trinh, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        return result
    
    def _validate(self):
        params = self._context
        HIEN_THI_THEO = params['HIEN_THI_THEO'] if 'HIEN_THI_THEO' in params.keys() else 'False'
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
        HIEN_THI_THEO = params['HIEN_THI_THEO'] if 'HIEN_THI_THEO' in params.keys() else 'False'
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
       
        if HIEN_THI_THEO=='MAU_DOC':
            return self._lay_du_lieu_hien_thi_theo_mau_doc(params_sql)

        if HIEN_THI_THEO=='MAU_NGANG':
            return self._lay_du_lieu_hien_thi_theo_mau_ngang(params_sql)
    
    def _lay_du_lieu_hien_thi_theo_mau_doc(self, params_sql):
        record = []
        query = """
                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             TIMESTAMP := %(TU_NGAY)s;

                den_ngay                            TIMESTAMP := %(DEN_NGAY)s;

                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

                CHE_DO_KE_TOAN                      VARCHAR;

                MA_PHAN_CAP_NVLTT                   VARCHAR(100);

                MA_PHAN_CAP_NCTT                    VARCHAR(100);

                MA_PHAN_CAP_SXC                     VARCHAR(100);

                MA_PHAN_CAP_CPSX                    VARCHAR(100);

                MA_PHAN_CAP_MTC                     VARCHAR(100);

                ma_dinh_danh_bao_cao                VARCHAR(50):= 'JCIncomeDetailByProjectWork';


                rec                                 RECORD;

                --@ListProjectWorkID : tham số bên misa

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
                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_CPSX
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'CPSX'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_NVLTT
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'NVLTT'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_NCTT
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'NCTT'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_MTC
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'MTC'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_SXC
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'SXC'
                ;


                DROP TABLE IF EXISTS TMP_CONG_TRINH_DUOC_CHON
                ;

                CREATE TEMP TABLE TMP_CONG_TRINH_DUOC_CHON


                -- Bảng các công trình được chọn
                (
                "CONG_TRINH_ID"   INT,
                "MA_PHAN_CAP"     VARCHAR(100),
                "MA_CONG_TRINH"   VARCHAR(20),
                "TEN_CONG_TRINH"  VARCHAR(128),
                "LOAI_CONG_TRINH" INT
                )
                ;

                INSERT INTO TMP_CONG_TRINH_DUOC_CHON
                SELECT DISTINCT
                PW."id"
                , PW."MA_PHAN_CAP"
                , PW."MA_CONG_TRINH"
                , PW."TEN_CONG_TRINH"
                , PW."LOAI_CONG_TRINH"
                FROM danh_muc_cong_trinh PW
                WHERE PW."id" = any(%(CONG_TRINH_IDS)s) --@ListProjectWorkID
                ;

                DROP TABLE IF EXISTS TMP_DS_CONG_TRINH
                ;
                CREATE TEMP TABLE TMP_DS_CONG_TRINH
                -- Bảng gồm toàn bộ các công trình con từ các công trình được chọn
                (
                "CONG_TRINH_ID"  INT,
                "MA_PHAN_CAP"    VARCHAR(100),
                "MA_CONG_TRINH"  VARCHAR(20),
                "TEN_CONG_TRINH" VARCHAR(128)
                )
                ;

                INSERT INTO TMP_DS_CONG_TRINH
                SELECT DISTINCT
                PW."id"
                , PW."MA_PHAN_CAP"
                , PW."MA_CONG_TRINH"
                , PW."TEN_CONG_TRINH"
                FROM TMP_CONG_TRINH_DUOC_CHON SPW
                INNER JOIN danh_muc_cong_trinh PW ON PW."MA_PHAN_CAP" LIKE SPW."MA_PHAN_CAP"
                || '%%'

                ;
                DROP TABLE IF EXISTS TMP_CHUNG_TU_GHI_SO_TINH_PHAN_BO
                ;
                CREATE TEMP TABLE TMP_CHUNG_TU_GHI_SO_TINH_PHAN_BO
                -- Bảng chứng từ ghi sổ đã được tính phân bổ
                (
                "STT"                   INT,
                "TEN_BAO_CAO_VAT_TU"    VARCHAR(255),
                "MA_CONG_TRINH"         VARCHAR(20),
                "TEN_CONG_TRINH"        VARCHAR(128),
                "MA_PHAN_CAP"           VARCHAR(100),
                "ID_CHUNG_TU"           INT,
                "MODEL_CHUNG_TU"        VARCHAR(255),
                "LOAI_CHUNG_TU"         VARCHAR(255),
                "SO_CHUNG_TU"           VARCHAR(20),
                "NGAY_HACH_TOAN"        TIMESTAMP,
                "NGAY_CHUNG_TU"         TIMESTAMP,
                "NGAY_HOA_DON"          TIMESTAMP,
                "SO_HOA_DON"            VARCHAR(500),
                "DIEN_GIAI"             VARCHAR(255),
                "SO_TIEN"               FLOAT,
                "MA_CHI_TIEU_DINH_DANH" VARCHAR(255)
                )
                ;
                INSERT INTO TMP_CHUNG_TU_GHI_SO_TINH_PHAN_BO
                SELECT
                SRT."sequence"
                , SRT."TEN_CHI_TIEU"
                , LPW."MA_CONG_TRINH"
                , LPW."TEN_CONG_TRINH"
                , LPW."MA_PHAN_CAP"
                , GL."ID_CHUNG_TU"
                , GL."MODEL_CHUNG_TU"
                , GL."LOAI_CHUNG_TU"
                , GL."SO_CHUNG_TU"
                , GL."NGAY_HACH_TOAN"
                , GL."NGAY_CHUNG_TU"
                , GL."NGAY_HOA_DON"
                , GL."SO_HOA_DON"
                , GL."DIEN_GIAI"
                , SUM(GL."SO_TIEN_QUY_DOI") "SO_TIEN"
                , SRT."MA_CHI_TIEU_DINH_DANH"
                FROM TIEN_ICH_CAU_HINH_LAI_LO_CHO_CT_HD_DH SRT
                LEFT JOIN LAY_SO_LIEU_SO_CAI_THEO_CT_THIET_LAP_BCTC_TRA_VE( NULL,
                tu_ngay,
                den_ngay,
                ma_dinh_danh_bao_cao, NULL,
                chi_nhanh_id,
                bao_gom_du_lieu_chi_nhanh_phu_thuoc
                ) GL ON GL."MA_BAO_CAO_VAT_TU_ID" = SRT."id" AND SRT."MA_BAO_CAO" = ma_dinh_danh_bao_cao
                INNER JOIN TMP_DS_CONG_TRINH LPW ON LPW."CONG_TRINH_ID" = GL."CONG_TRINH_ID"
                GROUP BY
                SRT."sequence"
                , SRT."TEN_CHI_TIEU"
                , LPW."MA_CONG_TRINH"
                , LPW."TEN_CONG_TRINH"
                , LPW."MA_PHAN_CAP"
                , GL."ID_CHUNG_TU"
                , GL."MODEL_CHUNG_TU"
                , GL."LOAI_CHUNG_TU"
                , GL."SO_CHUNG_TU"
                , GL."NGAY_HACH_TOAN"
                , GL."NGAY_CHUNG_TU"
                , GL."NGAY_HOA_DON"
                , GL."SO_HOA_DON"
                , GL."DIEN_GIAI"
                , SRT."MA_CHI_TIEU_DINH_DANH"
                UNION ALL
                SELECT
                3                     "STT"
                , N'Giá vốn hàng bán'  "TEN_BAO_CAO_VAT_TU"
                , LPW."MA_CONG_TRINH"
                , LPW."TEN_CONG_TRINH"
                , LPW."MA_PHAN_CAP"
                , JCAE."id"
                ,'tong.hop.phan.bo.chi.phi.bh.qldn.chi.phi.khac.cho.don.vi' AS "MODEL_CHUNG_TU"
                ,CAST( JCAE."LOAI_CHUNG_TU" AS VARCHAR(255))
                , JCAE."SO_CHUNG_TU"
                , JCAE."NGAY_CHUNG_TU"  "NGAY_HACH_TOAN"
                , JCAE."NGAY_CHUNG_TU"
                , NULL :: TIMESTAMP     "NGAY_HOA_DON"
                , NULL                  "SO_HOA_DON"
                , JCAE."DIEN_GIAI"
                , SUM(JCAEDT."SO_TIEN") "SO_TIEN"
                , '03' AS  "MA_CHI_TIEU_DINH_DANH"

                FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JCAE
                INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCAEDT
                ON JCAEDT."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JCAE."id"
                INNER JOIN TMP_DS_CONG_TRINH LPW ON LPW."CONG_TRINH_ID" = JCAEDT."MA_DON_VI_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCAE."CHI_NHANH_ID"
                WHERE JCAEDT."CAP_TO_CHUC" = '1'
                AND JCAE."NGAY_CHUNG_TU" BETWEEN tu_ngay AND den_ngay
                AND (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCAEDT."TAI_KHOAN_ID") LIKE '632%%'

                GROUP BY
                LPW."MA_CONG_TRINH",
                LPW."TEN_CONG_TRINH",
                LPW."MA_PHAN_CAP",
                JCAE."id",
                CAST( JCAE."LOAI_CHUNG_TU" AS VARCHAR(255)),
                JCAE."SO_CHUNG_TU",
                JCAE."NGAY_CHUNG_TU",
                JCAE."DIEN_GIAI"


                UNION ALL
                SELECT
                4                    "STT"
                , N'Chi phí khác'     "TEN_BAO_CAO_VAT_TU"
                , LPW."MA_CONG_TRINH"
                , LPW."TEN_CONG_TRINH"
                , LPW."MA_PHAN_CAP"
                , JCAE."id"
                ,'tong.hop.phan.bo.chi.phi.bh.qldn.chi.phi.khac.cho.don.vi' AS "MODEL_CHUNG_TU"
                ,CAST( JCAE."LOAI_CHUNG_TU" AS VARCHAR(255))
                , JCAE."SO_CHUNG_TU"
                , JCAE."NGAY_CHUNG_TU" "NGAY_HACH_TOAN"
                , JCAE."NGAY_CHUNG_TU"
                , NULL                 "NGAY_HOA_DON"
                , NULL                 "SO_HOA_DON"
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
                END)             "SO_TIEN"
                , '04' AS  "MA_CHI_TIEU_DINH_DANH"

                FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JCAE
                INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCAEDT
                ON JCAEDT."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JCAE."id"
                INNER JOIN TMP_DS_CONG_TRINH LPW ON LPW."CONG_TRINH_ID" = JCAEDT."MA_DON_VI_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JCAE."CHI_NHANH_ID"
                WHERE JCAEDT."CAP_TO_CHUC" = '1'
                AND JCAE."NGAY_CHUNG_TU" BETWEEN tu_ngay AND den_ngay
                AND LEFT((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCAEDT."TAI_KHOAN_ID"), 3) IN ('641', '642',
                '811', '635')

                GROUP BY
                LPW."MA_CONG_TRINH",
                LPW."TEN_CONG_TRINH",
                LPW."MA_PHAN_CAP",
                JCAE."id",
                CAST( JCAE."LOAI_CHUNG_TU" AS VARCHAR(255)),
                JCAE."SO_CHUNG_TU",
                JCAE."NGAY_CHUNG_TU",
                JCAE."DIEN_GIAI"
                ;


                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA
                AS

                SELECT
                ROW_NUMBER()
                OVER (
                ORDER BY "MA_CONG_TRINH" NULLS FIRST, "TEN_CONG_TRINH" NULLS FIRST, "STT" NULLS FIRST, "NGAY_HACH_TOAN" NULLS FIRST, "NGAY_CHUNG_TU" NULLS FIRST,
                "SO_CHUNG_TU" NULLS FIRST ) AS "RowNum"
                , *
                FROM (SELECT
                1                  "STT"
                , 'DOANH THU'        "TEN_BAO_CAO_VAT_TU"
                , SPW."MA_CONG_TRINH"
                , SPW."TEN_CONG_TRINH"
                , SPW."name" AS "LOAI_CONG_TRINH"
                , NULL  ::INT             "ID_CHUNG_TU"
                , NULL               "MODEL_CHUNG_TU"
                , NULL               "LOAI_CHUNG_TU"
                , NULL               "SO_CHUNG_TU"
                , NULL  ::TIMESTAMP             "NGAY_HACH_TOAN"
                , NULL   ::TIMESTAMP             "NGAY_CHUNG_TU"
                , NULL   ::TIMESTAMP             "NGAY_HOA_DON"
                , NULL               "SO_HOA_DON"
                , 'DOANH THU'        "DIEN_GIAI"
                , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '01'
                THEN GL."SO_TIEN"
                ELSE 0
                END)           "SO_TIEN"
                , CAST(1 AS BOOLEAN) IsBold

                FROM TMP_CHUNG_TU_GHI_SO_TINH_PHAN_BO GL


                INNER JOIN LATERAL ( SELECT
                tSPW."MA_CONG_TRINH"
                , tSPW."TEN_CONG_TRINH"
                , PWC."name"
                FROM TMP_CONG_TRINH_DUOC_CHON tSPW
                LEFT JOIN danh_muc_loai_cong_trinh AS PWC
                ON tSPW."LOAI_CONG_TRINH" = PWC."id"
                WHERE GL."MA_PHAN_CAP" LIKE tSPW."MA_PHAN_CAP"
                || '%%'
                ORDER BY tSPW."MA_PHAN_CAP" DESC
                LIMIT 1
                ) SPW ON TRUE
                GROUP BY SPW."MA_CONG_TRINH",
                SPW."TEN_CONG_TRINH",
                SPW."name"

                UNION ALL
                SELECT
                2                  "STT"
                , N'CHI PHÍ'        "TEN_BAO_CAO_VAT_TU"
                , SPW."MA_CONG_TRINH"
                , SPW."TEN_CONG_TRINH"
                , SPW."name"
                , NULL  ::INT             "ID_CHUNG_TU"
                , NULL               "MODEL_CHUNG_TU"
                , NULL               "LOAI_CHUNG_TU"
                , NULL               "SO_CHUNG_TU"
                , NULL  ::TIMESTAMP             "NGAY_HACH_TOAN"
                , NULL   ::TIMESTAMP             "NGAY_CHUNG_TU"
                , NULL   ::TIMESTAMP             "NGAY_HOA_DON"
                , NULL               "SO_HOA_DON"
                , N'CHI PHÍ'        "DIEN_GIAI"
                , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '03'
                OR GL."MA_CHI_TIEU_DINH_DANH" = '04'
                THEN GL."SO_TIEN"
                ELSE 0
                END)           "SO_TIEN"
                , CAST(1 AS BOOLEAN) IsBold

                FROM TMP_CHUNG_TU_GHI_SO_TINH_PHAN_BO GL


                INNER JOIN LATERAL ( SELECT
                tSPW."MA_CONG_TRINH"
                , tSPW."TEN_CONG_TRINH"
                , PWC."name"
                FROM TMP_CONG_TRINH_DUOC_CHON tSPW
                LEFT JOIN danh_muc_loai_cong_trinh AS PWC
                ON tSPW."LOAI_CONG_TRINH" = PWC."id"
                WHERE GL."MA_PHAN_CAP" LIKE tSPW."MA_PHAN_CAP"
                || '%%'
                ORDER BY tSPW."MA_PHAN_CAP" DESC
                LIMIT 1
                ) SPW ON TRUE
                GROUP BY SPW."MA_CONG_TRINH",
                SPW."TEN_CONG_TRINH",
                SPW."name"
                UNION ALL
                SELECT
                3                    "STT"
                , N'Giá vốn hàng bán' "TEN_BAO_CAO_VAT_TU"
                , SPW."MA_CONG_TRINH"
                , SPW."TEN_CONG_TRINH"
                , SPW."name"
                , NULL  ::INT             "ID_CHUNG_TU"
                , NULL               "MODEL_CHUNG_TU"
                , NULL               "LOAI_CHUNG_TU"
                , NULL               "SO_CHUNG_TU"
                , NULL  ::TIMESTAMP             "NGAY_HACH_TOAN"
                , NULL   ::TIMESTAMP             "NGAY_CHUNG_TU"
                , NULL   ::TIMESTAMP             "NGAY_HOA_DON"
                , NULL                 "SO_HOA_DON"
                , N'Giá vốn hàng bán' "DIEN_GIAI"
                , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '03'
                THEN GL."SO_TIEN"
                ELSE 0
                END)             "SO_TIEN"
                , CAST(1 AS BOOLEAN)   IsBold

                FROM TMP_CHUNG_TU_GHI_SO_TINH_PHAN_BO GL

                INNER JOIN LATERAL ( SELECT
                tSPW."MA_CONG_TRINH"
                , tSPW."TEN_CONG_TRINH"
                , PWC."name"
                FROM TMP_CONG_TRINH_DUOC_CHON tSPW
                LEFT JOIN danh_muc_loai_cong_trinh AS PWC
                ON tSPW."LOAI_CONG_TRINH" = PWC."id"
                WHERE GL."MA_PHAN_CAP" LIKE tSPW."MA_PHAN_CAP"
                || '%%'
                ORDER BY tSPW."MA_PHAN_CAP" DESC
                LIMIT 1
                ) SPW ON TRUE
                GROUP BY SPW."MA_CONG_TRINH",
                SPW."TEN_CONG_TRINH",
                SPW."name"
                UNION ALL
                SELECT
                4                  "STT"
                , N'Chi phí khác'   "TEN_BAO_CAO_VAT_TU"
                , SPW."MA_CONG_TRINH"
                , SPW."TEN_CONG_TRINH"
                , SPW."name"
                , NULL  ::INT             "ID_CHUNG_TU"
                , NULL               "MODEL_CHUNG_TU"
                , NULL               "LOAI_CHUNG_TU"
                , NULL               "SO_CHUNG_TU"
                , NULL  ::TIMESTAMP             "NGAY_HACH_TOAN"
                , NULL   ::TIMESTAMP             "NGAY_CHUNG_TU"
                , NULL   ::TIMESTAMP             "NGAY_HOA_DON"
                , NULL               "SO_HOA_DON"
                , N'Chi phí khác'   "DIEN_GIAI"
                , SUM(CASE WHEN GL."MA_CHI_TIEU_DINH_DANH" = '04'
                THEN GL."SO_TIEN"
                ELSE 0
                END)           "SO_TIEN"
                , CAST(1 AS BOOLEAN) IsBold

                FROM TMP_CHUNG_TU_GHI_SO_TINH_PHAN_BO GL

                INNER JOIN LATERAL ( SELECT
                tSPW."MA_CONG_TRINH"
                , tSPW."TEN_CONG_TRINH"
                , PWC."name"
                FROM TMP_CONG_TRINH_DUOC_CHON tSPW
                LEFT JOIN danh_muc_loai_cong_trinh AS PWC
                ON tSPW."LOAI_CONG_TRINH" = PWC."id"
                WHERE GL."MA_PHAN_CAP" LIKE tSPW."MA_PHAN_CAP"
                || '%%'
                ORDER BY tSPW."MA_PHAN_CAP" DESC
                LIMIT 1
                ) SPW ON TRUE
                GROUP BY SPW."MA_CONG_TRINH",
                SPW."TEN_CONG_TRINH",
                SPW."name"
                UNION ALL
                SELECT
                5                  "STT"
                , N'LỢI NHUẬN'      "TEN_BAO_CAO_VAT_TU"
                , SPW."MA_CONG_TRINH"
                , SPW."TEN_CONG_TRINH"
                , SPW."name"
                , NULL  ::INT             "ID_CHUNG_TU"
                , NULL               "MODEL_CHUNG_TU"
                , NULL               "LOAI_CHUNG_TU"
                , NULL               "SO_CHUNG_TU"
                , NULL  ::TIMESTAMP             "NGAY_HACH_TOAN"
                , NULL   ::TIMESTAMP             "NGAY_CHUNG_TU"
                , NULL   ::TIMESTAMP             "NGAY_HOA_DON"
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

                FROM TMP_CHUNG_TU_GHI_SO_TINH_PHAN_BO GL


                INNER JOIN LATERAL ( SELECT
                tSPW."MA_CONG_TRINH"
                , tSPW."TEN_CONG_TRINH"
                , PWC."name"
                FROM TMP_CONG_TRINH_DUOC_CHON tSPW
                LEFT JOIN danh_muc_loai_cong_trinh AS PWC
                ON tSPW."LOAI_CONG_TRINH" = PWC."id"
                WHERE GL."MA_PHAN_CAP" LIKE tSPW."MA_PHAN_CAP"
                || '%%'
                ORDER BY tSPW."MA_PHAN_CAP" DESC
                LIMIT 1
                ) SPW ON TRUE
                GROUP BY SPW."MA_CONG_TRINH",
                SPW."TEN_CONG_TRINH",
                SPW."name"
                UNION ALL
                SELECT
                GL."STT"
                , GL."TEN_BAO_CAO_VAT_TU"
                , SPW."MA_CONG_TRINH"
                , SPW."TEN_CONG_TRINH"
                , SPW."name"
                , GL."ID_CHUNG_TU"
                , GL."MODEL_CHUNG_TU"
                , GL."LOAI_CHUNG_TU"
                , GL."SO_CHUNG_TU"
                , GL."NGAY_HACH_TOAN"
                , GL."NGAY_CHUNG_TU"
                , GL."NGAY_HOA_DON"
                , GL."SO_HOA_DON"
                , GL."DIEN_GIAI"     "DIEN_GIAI"
                , GL."SO_TIEN"       "SO_TIEN"
                , CAST(0 AS BOOLEAN) IsBold

                FROM TMP_CHUNG_TU_GHI_SO_TINH_PHAN_BO GL


                INNER JOIN LATERAL ( SELECT
                tSPW."MA_CONG_TRINH"
                , tSPW."TEN_CONG_TRINH"
                , PWC."name"
                FROM TMP_CONG_TRINH_DUOC_CHON tSPW
                LEFT JOIN danh_muc_loai_cong_trinh AS PWC
                ON tSPW."LOAI_CONG_TRINH" = PWC."id"
                WHERE GL."MA_PHAN_CAP" LIKE tSPW."MA_PHAN_CAP"
                || '%%'
                ORDER BY tSPW."MA_PHAN_CAP" DESC
                LIMIT 1
                ) SPW ON TRUE
                WHERE GL."SO_TIEN" <> 0
                ) tbl
                ;
                END $$
                ;
                SELECT 
                "TEN_CONG_TRINH" AS "TEN_CONG_TRINH",
                "NGAY_HACH_TOAN" AS "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU" AS "NGAY_CHUNG_TU",
                "SO_CHUNG_TU" AS "SO_CHUNG_TU",
                "DIEN_GIAI" AS "DIEN_GIAI",
                "SO_TIEN" AS "SO_TIEN",
                "ID_CHUNG_TU" AS "ID_GOC",
                "MODEL_CHUNG_TU" AS "MODEL_GOC",
                "isbold" AS "isbold"

                FROM TMP_KET_QUA
                ORDER BY "RowNum" 
                OFFSET %(offset)s
                LIMIT %(limit)s;
                """
        return self.execute(query,params_sql)

    def _lay_du_lieu_hien_thi_theo_mau_ngang(self, params_sql):
        record = []
        query = """
                DO LANGUAGE plpgsql $$
                DECLARE
                tu_ngay                             TIMESTAMP :=  %(TU_NGAY)s;

                den_ngay                            TIMESTAMP := %(DEN_NGAY)s;

                chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

                bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

                CHE_DO_KE_TOAN                      VARCHAR;

                MA_PHAN_CAP_NVLTT                   VARCHAR(100);

                MA_PHAN_CAP_NCTT                    VARCHAR(100);

                MA_PHAN_CAP_SXC                     VARCHAR(100);

                MA_PHAN_CAP_CPSX                    VARCHAR(100);

                MA_PHAN_CAP_MTC                     VARCHAR(100);


                rec                                 RECORD;

                --@ListProjectWorkID : tham số bên misa

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
                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_CPSX
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'CPSX'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_NVLTT
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'NVLTT'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_NCTT
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'NCTT'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_MTC
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'MTC'
                ;

                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_SXC
                FROM danh_muc_khoan_muc_cp
                WHERE "MA_KHOAN_MUC_CP" = 'SXC'
                ;


                DROP TABLE IF EXISTS TMP_CONG_TRINH_DUOC_CHON
                ;

                CREATE TEMP TABLE TMP_CONG_TRINH_DUOC_CHON


                (
                "CONG_TRINH_ID"   INT,
                "MA_PHAN_CAP"     VARCHAR(100),
                "MA_CONG_TRINH"   VARCHAR(20),
                "TEN_CONG_TRINH"  VARCHAR(128),

                "LOAI_CONG_TRINH" VARCHAR(255)
                )
                ;

                -- 1 bảng để lưu những CT đc chọn @Object
                -- 1 bảng để lưu những CT dùng để lấy dữ liệu (k lấy thằng cha)
                -- 1 bảng để
                INSERT INTO TMP_CONG_TRINH_DUOC_CHON
                SELECT DISTINCT
                EI."id"
                , EI."MA_PHAN_CAP"
                , EI."MA_CONG_TRINH"
                , EI."TEN_CONG_TRINH"
                , PC."name"
                FROM
                danh_muc_cong_trinh AS EI
                LEFT JOIN danh_muc_loai_cong_trinh PC ON EI."LOAI_CONG_TRINH" = PC."id"
                WHERE EI."id" = any(%(CONG_TRINH_IDS)s) --@ListProjectWorkID
                ;




                DROP TABLE IF EXISTS TMP_CONG_TRINH_DUOC_CHON_1
                ;

                CREATE TEMP TABLE TMP_CONG_TRINH_DUOC_CHON_1

                (
                "CONG_TRINH_ID"   INT PRIMARY KEY,
                "MA_PHAN_CAP"     VARCHAR(100)
                NULL,
                "LOAI_CONG_TRINH" VARCHAR(255),
                "MA_CONG_TRINH"   VARCHAR(20),
                "TEN_CONG_TRINH"  VARCHAR(128)
                )
                ;

                INSERT INTO TMP_CONG_TRINH_DUOC_CHON_1
                SELECT
                S."CONG_TRINH_ID"
                , S."MA_PHAN_CAP"
                , S."LOAI_CONG_TRINH"
                , S."MA_CONG_TRINH"
                , S."TEN_CONG_TRINH"
                FROM TMP_CONG_TRINH_DUOC_CHON S
                LEFT JOIN TMP_CONG_TRINH_DUOC_CHON S1 ON S1."MA_PHAN_CAP" LIKE S."MA_PHAN_CAP"
                || '%%'
                AND S."MA_PHAN_CAP" <> S1."MA_PHAN_CAP"
                WHERE S1."MA_PHAN_CAP" IS NULL
                ;


                DROP TABLE IF EXISTS TMP_DS_CONG_TRINH
                ;

                CREATE TEMP TABLE TMP_DS_CONG_TRINH


                (
                "CONG_TRINH_ID"   INT,
                "MA_PHAN_CAP"     VARCHAR(100),
                "MA_CONG_TRINH"   VARCHAR(20),
                "TEN_CONG_TRINH"  VARCHAR(128),

                "LOAI_CONG_TRINH" VARCHAR(255)
                )
                ;


                INSERT INTO TMP_DS_CONG_TRINH
                SELECT DISTINCT
                EI."id"
                , EI."MA_PHAN_CAP"
                , EI."MA_CONG_TRINH"
                , EI."TEN_CONG_TRINH"
                , SEI."LOAI_CONG_TRINH"
                FROM danh_muc_cong_trinh EI
                INNER JOIN TMP_CONG_TRINH_DUOC_CHON_1 SEI ON EI."MA_PHAN_CAP" LIKE SEI."MA_PHAN_CAP"
                || '%%'
                ;


                DROP TABLE IF EXISTS TMP_DU_LIEU_SO_CAI
                ;

                CREATE TEMP TABLE TMP_DU_LIEU_SO_CAI

                (
                "ID_CHUNG_TU"                  INT,
                "MODEL_CHUNG_TU"               VARCHAR(255),

                "NGAY_HACH_TOAN"               TIMESTAMP,
                "NGAY_CHUNG_TU"                TIMESTAMP,
                "SO_CHUNG_TU"                  VARCHAR(25),
                "NGAY_HOA_DON"                 TIMESTAMP,
                "SO_HOA_DON"                   VARCHAR,
                "DIEN_GIAI"                    VARCHAR(255),
                "CONG_TRINH_ID"                INT,
                "MA_PHAN_CAP"                  VARCHAR(100),
                "DOANH_THU_PHAT_SINH" DECIMAL(25, 4),
                "DOANH_THU_THU_NHAP_KHAC"      DECIMAL(25, 4),
                "GIAM_TRU_DOANH_THU"           DECIMAL(25, 4),
                "GIA_VON"                      DECIMAL(25, 4), -- Giá vốn hàng bán
                "CHI_PHI_BAN_HANG"             DECIMAL(25, 4), -- Chi phí bán hàng
                "CHI_PHI_QUAN_LY"              DECIMAL(25, 4), -- Chi phí quản lý
                "CHI_PHI_KHAC"                 DECIMAL(25, 4), -- Chi phí khác
                "DO_DANG_DAU_KY"               DECIMAL(25, 4),
                "NGUYEN_VAT_LIEU"              DECIMAL(25, 4),
                "NHAN_CONG"                    DECIMAL(25, 4),
                "MAY_THI_CONG"                 DECIMAL(25, 4),
                "CHI_PHI_CHUNG"                DECIMAL(25, 4),
                "KHOAN_GIAM_GIA_THANH"         DECIMAL(25, 4),
                "DO_DANG_CUOI_KY"              DECIMAL(25, 4)

                )
                ;


                IF (CHE_DO_KE_TOAN = '15')
                THEN
                INSERT INTO TMP_DU_LIEU_SO_CAI
                (
                "ID_CHUNG_TU",
                "MODEL_CHUNG_TU",

                "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU",
                "SO_CHUNG_TU",
                "NGAY_HOA_DON",
                "SO_HOA_DON",
                "DIEN_GIAI",
                "CONG_TRINH_ID",
                "MA_PHAN_CAP",
                "DOANH_THU_PHAT_SINH",
                "DOANH_THU_THU_NHAP_KHAC",
                "GIAM_TRU_DOANH_THU",
                "GIA_VON", -- Giá vốn hàng bán
                "CHI_PHI_BAN_HANG", -- Chi phí bán hàng
                "CHI_PHI_QUAN_LY", -- Chi phí quản lý
                "CHI_PHI_KHAC", -- Chi phí khác
                "DO_DANG_DAU_KY",
                "NGUYEN_VAT_LIEU",
                "NHAN_CONG",
                "MAY_THI_CONG",
                "CHI_PHI_CHUNG",
                "KHOAN_GIAM_GIA_THANH",
                "DO_DANG_CUOI_KY"

                )

                SELECT
                GL."ID_CHUNG_TU"
                , GL."MODEL_CHUNG_TU"

                , GL."NGAY_HACH_TOAN"
                , GL."NGAY_CHUNG_TU"
                , GL."SO_CHUNG_TU"
                , GL."NGAY_HOA_DON"
                , GL."SO_HOA_DON"
                , GL."DIEN_GIAI_CHUNG"
                , P."CONG_TRINH_ID"
                , P."MA_PHAN_CAP"
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (GL."MA_TAI_KHOAN" LIKE N'511%%'
                AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG", '') NOT LIKE
                N'911%%' --ntquang 14/10/1017 :  CR_149456
                )
                THEN GL."GHI_CO"
                ELSE 0
                END)
                - SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND GL."MA_TAI_KHOAN" LIKE '511%%'
                --ntquang 14/10/1017 :  CR_149456
                AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG", '') NOT LIKE N'911%%'
                AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG", '') NOT LIKE N'521%%'
                THEN GL."GHI_NO"
                ELSE 0
                END) AS "DOANH_THU_PHAT_SINH"
                --Doanh thu bán hàng: (PS C 511 (Không bao gồm PS ĐƯ Nợ TK 911/Có TK511)– PS N 511 (không bao gồm PS ĐƯ Nợ TK511/Có TK 911, 521)) chi tiết theo từng công trình
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND ((GL."MA_TAI_KHOAN" LIKE N'711%%'
                OR GL."MA_TAI_KHOAN" LIKE '515%%'
                )
                --ntquang 14/10/1017 :  CR_149456
                AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG", '') NOT LIKE N'911%%'
                )
                THEN GL."GHI_CO"
                ELSE 0
                END)
                - SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (GL."MA_TAI_KHOAN" LIKE N'711%%'
                OR GL."MA_TAI_KHOAN" LIKE '515%%'
                )
                --ntquang 14/10/1017 :  CR_149456
                AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG", '') NOT LIKE N'911%%'
                THEN GL."GHI_NO"
                ELSE 0
                END) AS "DOANH_THU_THU_NHAP_KHAC"
                --Doan thu khác: (PS C 515, 711 (Không bao gồm PS ĐƯ Nợ TK 911/Có TK515, 711) – PS N 515, 711 (không bao gồm PS ĐƯ Nợ TK515, 711/Có TK 911)) chi tiết theo từng công trình
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND GL."MA_TAI_KHOAN" LIKE N'521%%'
                THEN GL."GHI_NO"
                ELSE 0
                END)
                - SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND GL."MA_TAI_KHOAN" LIKE N'5211%%'
                THEN GL."GHI_CO"
                ELSE 0
                END) AS "GIAM_TRU_DOANH_THU"
                --Giảm trừ doanh thu: Đối với TT200 = PS Nợ TK 521 - PS Có TK 5211 chi tiết theo từng công trình
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND GL."MA_TAI_KHOAN" LIKE N'632%%'
                THEN GL."GHI_NO" - GL."GHI_CO"
                ELSE 0
                END)   AS "GIA_VON"
                -- Giá vốn hàng bán: Đối với TT200 = (PSN632 – PSC632) chi tiết theo từng công trình
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND GL."MA_TAI_KHOAN" LIKE N'641%%'
                THEN GL."GHI_NO" - GL."GHI_CO"
                ELSE 0
                END)   AS "CHI_PHI_BAN_HANG"
                -- Chi phí bán hàng Đối với TT200 = (PSN 641 – PSC641) chi tiết theo từng công trình
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND GL."MA_TAI_KHOAN" LIKE N'642%%'
                THEN GL."GHI_NO" - GL."GHI_CO"
                ELSE 0
                END)   AS "CHI_PHI_QUAN_LY"
                -- Chi phí quản lý: Đối với TT200 = (PSN 642 – PSC642) chi tiết theo từng công trình
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (GL."MA_TAI_KHOAN" LIKE N'811%%'
                OR GL."MA_TAI_KHOAN" LIKE N'635%%'
                )
                THEN GL."GHI_NO" - GL."GHI_CO"
                ELSE 0
                END)   AS "CHI_PHI_KHAC"
                -- Chi phí khác Đối với TT200 =  (PSN 811, 635 – PSC 811, 635) chi tiết theo từng công trình
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                AND LEFT(GL."MA_TAI_KHOAN", 3) IN (
                '621', '622', '623', '627',
                '154')
                THEN GL."GHI_NO" - GL."GHI_CO"
                ELSE 0
                END)   AS "DO_DANG_DAU_KY"
                -- Tổng chi phí trên form form Nhập lũy kế chi phí phát sinh cho công trình kỳ trước + Tổng (PS Nợ - PS Có) của TK 621, 622, 623, 627 chi tiết theo từng công trình trên chứng từ có ngày hạch toán < “Từ ngày của kỳ báo cáo (không kể PSDU Nợ TK 154/Có TK 621, 622, 623, 627 chi tiết theo từng công trình) + Tổng PS Nợ TK 154 chi tiết theo từng ĐT THCP trên chứng từ có ngày hạch toán < “Từ ngày của kỳ báo cáo (không kể PSDU Nợ TK 154/Có TK 621, 622, 627, 623 chi tiết theo từng ĐT THCP)
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                THEN CASE WHEN (GL."MA_TAI_KHOAN" LIKE N'621%%'
                AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'154%%'
                )
                THEN GL."GHI_NO"
                - GL."GHI_CO"
                WHEN GL."MA_TAI_KHOAN" LIKE N'154%%'
                -- nmtruong 16/5/2016: sửa lỗi 103504: Like 154 chưa có dấu %%
                AND LEFT(GL."MA_TAI_KHOAN_DOI_UNG",
                3) NOT IN (
                '621', '622', '623',
                '627', '154')
                THEN GL."GHI_NO"
                ELSE 0
                END
                ELSE 0
                END)   AS "NGUYEN_VAT_LIEU"
                -- nguyên vật liệu trực tiếp: Đối với TT200: Tổng (PS Nợ - PS Có) của TK 621 chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo (không kể PSDU Nợ TK 154/Có TK 621 chi tiết theo từng công trình)
                --+ Tổng PS Nợ TK 154 chi tiết theo từng ĐT THCP trên chứng từ có ngày hạch toán thuộc kỳ tính giá thành (không kể PSDU Nợ TK 154/Có TK 621, 622, 627, 623 chi tiết theo từng ĐT THCP)
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (GL."MA_TAI_KHOAN" LIKE N'622%%'
                AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'154%%'
                )
                THEN GL."GHI_NO" - GL."GHI_CO"
                ELSE 0
                END)   AS "NHAN_CONG"
                -- Chi phí nhân công trực tiếp: Đối với TT200: Tổng (PS Nợ - PS Có) của TK 622 chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo (không kể PSDU Nợ TK 154/Có TK 622 chi tiết theo từng công trình)
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (GL."MA_TAI_KHOAN" LIKE N'623%%'
                AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'154%%'
                )
                THEN GL."GHI_NO" - GL."GHI_CO"
                ELSE 0
                END)   AS "MAY_THI_CONG"
                --Chi phí máy thi công Đối với TT200: Tổng (PS Nợ - PS Có) của TK 623 chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo (không kể PSDU Nợ TK 154/Có TK 623 chi tiết theo từng công trình)
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (GL."MA_TAI_KHOAN" LIKE N'627%%'
                AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'154%%'
                )
                THEN GL."GHI_NO" - GL."GHI_CO"
                ELSE 0
                END)   AS "CHI_PHI_CHUNG"
                --Chi phí chung: Đối với TT200: Tổng (PS Nợ - PS Có) của TK 627 chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo (không kể PSDU Nợ TK 154/Có TK 627 chi tiết theo từng công trình)
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (GL."MA_TAI_KHOAN" LIKE N'154%%'
                AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'632%%'
                )
                THEN GL."GHI_CO"
                ELSE 0
                END)   AS "KHOAN_GIAM_GIA_THANH"
                --Giảm giá thành: TT200: PS Có TK 154 chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo (không kể PSDU Nợ TK 632/có TK 154 chi tiết theo từng công trình
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" <= den_ngay
                AND LEFT(GL."MA_TAI_KHOAN", 3) IN (
                '621', '622', '623', '627',
                '154')
                THEN GL."GHI_NO" - GL."GHI_CO"
                ELSE 0
                END)   AS "DO_DANG_DAU_KY" -- Dở dang cuối kỳ

                FROM so_cai_chi_tiet GL
                INNER JOIN TMP_DS_CONG_TRINH P ON GL."CONG_TRINH_ID" = P."CONG_TRINH_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                /*DDKhanh CR133811 31/08/2017 Lấy thêm các trường mở rộng*/
                --                                 LEFT JOIN CustomField"SO_CAI" CFL ON GL."CHI_TIET_ID" = CFL.RefDetailID AND CFL.IsPostToManagementBook = @IsWorkingWithManagementBook
                WHERE GL."NGAY_HACH_TOAN" <= den_ngay
                AND ("MA_TAI_KHOAN" LIKE N'511%%'
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

                GROUP BY
                P."CONG_TRINH_ID",
                P."MA_PHAN_CAP",
                GL."NGAY_HACH_TOAN",
                GL."NGAY_CHUNG_TU",
                GL."SO_CHUNG_TU",
                GL."NGAY_HOA_DON",
                GL."SO_HOA_DON",
                GL."DIEN_GIAI_CHUNG",
                GL."ID_CHUNG_TU",

                GL."MODEL_CHUNG_TU"

                UNION ALL

                SELECT
                J."id"
                , 'gia.thanh.ky.tinh.gia.thanh' AS "MODEL_CHUNG_TU"

                , J."DEN_NGAY"
                , J."DEN_NGAY"
                , ''                            AS "SO_CHUNG_TU"
                , NULL :: TIMESTAMP             AS "NGAY_HOA_DON"
                , NULL                          AS "SO_HOA_DON"
                , J."TEN"
                , P."CONG_TRINH_ID"
                , P."MA_PHAN_CAP"
                , 0                             AS "DOANH_THU_PHAT_SINH"
                , 0                             AS "DOANH_THU_THU_NHAP_KHAC"
                , 0                             AS "GIAM_TRU_DOANH_THU"
                , 0                             AS "GIA_VON"
                ,
                -- Giá vốn hàng bán: + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 632 trên chứng từ phân bổ chi phí BH, QLDN, khác
                0                             AS "CHI_PHI_BAN_HANG"
                ,
                -- Chi phí bán hàng + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 641 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                0                             AS "CHI_PHI_QUAN_LY"
                ,
                -- Chi phí quản lý + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 642 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                0                             AS "CHI_PHI_KHAC"
                ,
                -- Chi phí khác + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 811, 635 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                SUM(CASE WHEN J."DEN_NGAY" < tu_ngay
                AND LEFT((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCAD."TAI_KHOAN_ID"), 3) IN (
                '621', '622', '623', '627')
                THEN JCAD."SO_TIEN"
                ELSE 0
                END)                      AS "DO_DANG_DAU_KY"
                ,
                --  + Tổng số tiền phân bổ của TK 621, 622, 623, 627 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc < “Từ ngày của kỳ báo cáo - PS Có TK 154 chi tiết theo từng công trình trên các chứng từ có ngày hạch toán < "Từ ngày" của kỳ báo cáo + Số đã nghiệm thu trên form Nhập lũy kế chi phí phát sinh cho công trình/đơn hàng/hợp đồng kỳ trước tương ứng với TK 154
                SUM(CASE WHEN J."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
                AND (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCAD."TAI_KHOAN_ID") LIKE N'621%%'
                THEN JCAD."SO_TIEN"
                ELSE 0
                END)                      AS "NGUYEN_VAT_LIEU"
                ,
                -- + Tổng số tiền phân bổ của TK 621 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                SUM(CASE WHEN J."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
                AND (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCAD."TAI_KHOAN_ID") LIKE N'622%%'
                THEN JCAD."SO_TIEN"
                ELSE 0
                END)                      AS "NHAN_CONG"
                ,
                -- + Tổng số tiền phân bổ của TK 622 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo
                SUM(CASE WHEN J."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
                AND (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCAD."TAI_KHOAN_ID") LIKE N'623%%'
                THEN JCAD."SO_TIEN"
                ELSE 0
                END)                      AS "MAY_THI_CONG"
                ,
                --+ Tổng số tiền phân bổ của TK 623 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                SUM(CASE WHEN J."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
                AND (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCAD."TAI_KHOAN_ID") LIKE N'627%%'
                THEN JCAD."SO_TIEN"
                ELSE 0
                END)                      AS "CHI_PHI_CHUNG"
                ,
                --+ Tổng số tiền phân bổ của TK 627 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                0                             AS "KHOAN_GIAM_GIA_THANH"
                , SUM(CASE WHEN J."DEN_NGAY" <= den_ngay
                AND LEFT((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCAD."TAI_KHOAN_ID"), 3) IN (
                '621', '622', '623', '627')
                THEN JCAD."SO_TIEN"
                ELSE 0
                END)                      AS "DO_DANG_CUOI_KY"

                FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung JCAD
                INNER JOIN gia_thanh_ky_tinh_gia_thanh J ON J."id" = JCAD."KY_TINH_GIA_THANH_ID"
                INNER JOIN TMP_DS_CONG_TRINH P ON P."CONG_TRINH_ID" = JCAD."MA_CONG_TRINH_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = J."CHI_NHANH_ID"
                WHERE J."DEN_NGAY" <= den_ngay --Lấy tất cả các lần phân bổ của kỳ tính giá thành hiện tại và trước đó

                GROUP BY
                P."CONG_TRINH_ID",
                P."MA_PHAN_CAP",
                J."DEN_NGAY",
                J."DEN_NGAY",
                J."TEN",
                J."id"


                UNION ALL
                SELECT
                JC."id"
                , 'tong.hop.phan.bo.chi.phi.bh.qldn.chi.phi.khac.cho.don.vi' AS "MODEL_CHUNG_TU"

                , JC."NGAY_CHUNG_TU"
                , JC."NGAY_CHUNG_TU"
                , JC."SO_CHUNG_TU"
                , NULL                                                       AS "NGAY_HOA_DON"
                , NULL                                                       AS "SO_HOA_DON"
                , JC."DIEN_GIAI"
                , P."CONG_TRINH_ID"
                , P."MA_PHAN_CAP"
                , 0                                                          AS "DOANH_THU_PHAT_SINH"
                , 0                                                          AS "DOANH_THU_THU_NHAP_KHAC"
                , 0                                                          AS "GIAM_TRU_DOANH_THU"
                , SUM(CASE WHEN (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'632%%'
                THEN JCED."SO_TIEN"
                ELSE 0
                END)                                                   AS "GIA_VON"
                ,
                -- Giá vốn hàng bán: + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 632 trên chứng từ phân bổ chi phí BH, QLDN, khác
                SUM(CASE WHEN (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'641%%'
                THEN JCED."SO_TIEN"
                ELSE 0
                END)                                                   AS "CHI_PHI_BAN_HANG"
                ,
                -- Chi phí bán hàng + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 641 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                SUM(CASE WHEN (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'642%%'
                THEN JCED."SO_TIEN"
                ELSE 0
                END)                                                   AS "CHI_PHI_QUAN_LY"
                ,
                -- Chi phí quản lý + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 642 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                SUM(CASE WHEN ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'811%%'
                OR (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'635%%'
                )
                THEN JCED."SO_TIEN"
                ELSE 0
                END)                                                   AS "CHI_PHI_KHAC"
                ,
                -- Chi phí khác + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 811, 635 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                0                                                          AS "DO_DANG_DAU_KY"
                ,
                --  + Tổng số tiền phân bổ của TK 621, 622, 623, 627 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc < “Từ ngày của kỳ báo cáo - PS Có TK 154 chi tiết theo từng công trình trên các chứng từ có ngày hạch toán < "Từ ngày" của kỳ báo cáo + Số đã nghiệm thu trên form Nhập lũy kế chi phí phát sinh cho công trình/đơn hàng/hợp đồng kỳ trước tương ứng với TK 154
                0                                                          AS "NGUYEN_VAT_LIEU"
                ,
                -- + Tổng số tiền phân bổ của TK 621 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                0                                                          AS "NHAN_CONG"
                ,
                -- + Tổng số tiền phân bổ của TK 622 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo
                0                                                          AS "MAY_THI_CONG"
                ,
                --+ Tổng số tiền phân bổ của TK 623 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                0                                                          AS "CHI_PHI_CHUNG"
                ,
                --+ Tổng số tiền phân bổ của TK 627 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                0                                                          AS "KHOAN_GIAM_GIA_THANH"
                , 0                                                          AS "DO_DANG_CUOI_KY"

                FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JC
                INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCED
                ON JCED."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JC."id"
                INNER JOIN TMP_DS_CONG_TRINH P ON P."CONG_TRINH_ID" = JCED."MA_DON_VI_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JC."CHI_NHANH_ID"
                WHERE JCED."CAP_TO_CHUC" = '1'
                AND JC."NGAY_CHUNG_TU" BETWEEN tu_ngay AND den_ngay

                GROUP BY P."CONG_TRINH_ID",
                P."MA_PHAN_CAP",
                JC."NGAY_CHUNG_TU",
                JC."NGAY_CHUNG_TU",
                JC."SO_CHUNG_TU",
                JC."DIEN_GIAI",
                JC."id"

                ;


                ELSE -- QD 48


                INSERT INTO TMP_DU_LIEU_SO_CAI
                SELECT
                GL."ID_CHUNG_TU"
                , GL."MODEL_CHUNG_TU"
                , GL."NGAY_HACH_TOAN"
                , GL."NGAY_CHUNG_TU"
                , GL."SO_CHUNG_TU"
                , GL."NGAY_HOA_DON"
                , GL."SO_HOA_DON"
                , GL."DIEN_GIAI_CHUNG"
                , P."CONG_TRINH_ID"
                , P."MA_PHAN_CAP"
                , --ntquang 14/10/1017 :  CR_149456 - thay đổi lại cách lấy số liệu để lấy được cả các dòng đầu kỳ
                SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (GL."MA_TAI_KHOAN" LIKE N'511%%' AND GL."LOAI_NGHIEP_VU" IS NULL
                --ntquang 14/10/1017 :  CR_149456_Tài khoản đối ứng của số dư đầu kỳ = NULL
                AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG", '') NOT LIKE N'911%%'
                )
                THEN GL."GHI_CO"
                ELSE 0
                END)
                - SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND GL."MA_TAI_KHOAN" LIKE '511%%' AND GL."LOAI_NGHIEP_VU" IS NULL
                --ntquang 14/10/1017 :  CR_149456_Tài khoản đối ứng của số dư đầu kỳ = NULL
                AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG", '') NOT LIKE N'911%%'

                THEN GL."GHI_NO"
                ELSE 0
                END)            AS "DOANH_THU_PHAT_SINH"
                ,
                --Doanh thu bán hàng: (PS C 511 (Không bao gồm PS ĐƯ Nợ TK 911/Có TK511)– PS N 511 (không bao gồm PS ĐƯ Nợ TK511/Có TK 911, 521)) chi tiết theo từng công trình

                SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND ((GL."MA_TAI_KHOAN" LIKE N'711%%'
                OR GL."MA_TAI_KHOAN" LIKE '515%%'
                )
                --ntquang 14/10/1017 :  CR_149456_Tài khoản đối ứng của số dư đầu kỳ = NULL
                AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG", '') NOT LIKE N'911%%'
                )
                THEN GL."GHI_CO"
                ELSE 0
                END)
                - SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (GL."MA_TAI_KHOAN" LIKE N'711%%'
                OR GL."MA_TAI_KHOAN" LIKE '515%%'
                )
                --ntquang 14/10/1017 :  CR_149456_Tài khoản đối ứng của số dư đầu kỳ = NULL
                AND COALESCE(GL."MA_TAI_KHOAN_DOI_UNG", '') NOT LIKE N'911%%'
                THEN GL."GHI_NO"
                ELSE 0
                END)            AS "DOANH_THU_THU_NHAP_KHAC"
                --Đối với QĐ 48 = PS C 515, 711 (Không bao gồm PS ĐƯ Nợ TK911/Có TK515, 711) – PS Nợ TK 515, 711 (không bao gồm PS ĐƯ Nợ TK 515, 711/Có TK 911) chi tiết theo từng công trình
                , --ptphuong2 21/09/2016 sửa cách lấy dữ liệu giảm trừ doanh thu theo thông tư 133/qđ 48
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
                END), 0) AS "GIAM_TRU_DOANH_THU"
                , --giảm trừ doanh thu
                SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND GL."MA_TAI_KHOAN" LIKE N'632%%'
                THEN GL."GHI_NO"
                - GL."GHI_CO"
                ELSE 0
                END)              AS "GIA_VON"
                -- Giá vốn hàng bán: Đối với Qd48 = (PSN632 – PSC632) chi tiết theo từng công trình
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND GL."MA_TAI_KHOAN" LIKE N'6421%%'
                THEN GL."GHI_NO"
                - GL."GHI_CO"
                ELSE 0
                END)              AS "CHI_PHI_BAN_HANG"
                -- Chi phí bán hàng Đối với QĐ 48 = (PSN 6421 – PSC6421) chi tiết theo từng công trình
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND GL."MA_TAI_KHOAN" LIKE N'6422%%'
                THEN GL."GHI_NO"
                - GL."GHI_CO"
                ELSE 0
                END)              AS "CHI_PHI_QUAN_LY"
                -- Chi phí quản lý: Đối với QĐ 48 = (PSN 6422 – PSC6422) chi tiết theo từng công trình
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (GL."MA_TAI_KHOAN" LIKE N'811%%'
                OR GL."MA_TAI_KHOAN" LIKE N'635%%'
                )
                THEN GL."GHI_NO"
                - GL."GHI_CO"
                ELSE 0
                END)              AS "CHI_PHI_KHAC"
                -- Chi phí khác Đối với QD48 =  (PSN 811, 635 – PSC 811, 635) chi tiết theo từng công trình
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                AND LEFT(GL."MA_TAI_KHOAN", 3) IN (
                '154')
                AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_CPSX
                OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                )
                THEN GL."GHI_NO"
                - GL."GHI_CO"
                ELSE 0
                END)              AS "DO_DANG_DAU_KY"
                -- QĐ 48 = Tổng chi phí trên form form Nhập lũy kế chi phí phát sinh cho công trình kỳ trước
                --+ Tổng (PS Nợ - PS Có) của TK154 chi tiết theo KMCP NVLTT, NCTT, MTC, SXC chi tiết theo từng công trình trên chứng từ có ngày hạch toán < “Từ ngày của kỳ báo cáo  – PS Có TK 154 không chi tiết theo KMCP sản xuất có chi tiết theo từng công trình trên chứng từ có ngày hạch toán < "Từ ngày" của kỳ báo cáo + Số đã nghiệm thu trên form Nhập lũy kế chi phí phát sinh cho công trình/đơn hàng/hợp đồng kỳ trước tương ứng với TK 154
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                THEN CASE WHEN (GL."MA_TAI_KHOAN" LIKE N'154%%'
                AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                )
                THEN GL."GHI_NO"
                - GL."GHI_CO"
                ELSE 0
                END
                ELSE 0
                END)              AS "NGUYEN_VAT_LIEU"
                -- nguyên vật liệu trực tiếp:Đối với QĐ 48: Tổng (PS Nợ - PS Có) của TK154 chi tiết theo KMCP NVLTT chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (GL."MA_TAI_KHOAN" LIKE N'154%%'
                AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                )
                THEN GL."GHI_NO"
                - GL."GHI_CO"
                ELSE 0
                END)              AS "NHAN_CONG"
                -- Chi phí nhân công trực tiếp: Đối với QĐ 48: Tổng (PS Nợ - PS Có) của TK 154 chi tiết theo KMCP NCTT chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (GL."MA_TAI_KHOAN" LIKE N'154%%'
                AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                )
                THEN GL."GHI_NO"
                - GL."GHI_CO"
                ELSE 0
                END)              AS "MAY_THI_CONG"
                --Chi phí máy thi công Đối với QĐ 48: Tổng (PS Nợ - PS Có) của TK 154 chi tiết theo các KMCP MTC chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (GL."MA_TAI_KHOAN" LIKE N'154%%'
                AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                )
                THEN GL."GHI_NO"
                - GL."GHI_CO"
                ELSE 0
                END)              AS "CHI_PHI_CHUNG"
                --Chi phí chung: Đối với QĐ 48: Tổng (PS Nợ - PS Có) của TK 154 chi tiết theo KMCP SXC chi tiết theo từng công trình trên chứng từ có ngày hạch toán thuộc kỳ báo cáo
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                AND (GL."MA_TAI_KHOAN" LIKE N'154%%'
                AND GL."MA_TAI_KHOAN_DOI_UNG" NOT LIKE N'632%%'
                )
                AND E."id" IS NULL
                THEN GL."GHI_CO"
                ELSE 0
                END)              AS "KHOAN_GIAM_GIA_THANH"
                --Giảm giá thành: QĐ48: PS Có TK 154 chi tiết theo từng công trình trên chứng từ không chi tiết theo KMCP có ngày hạch toán thuộc kỳ báo cáo (không kể PSDU Nợ TK 632/có TK 154 chi tiết theo từng công trình
                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" <= den_ngay
                AND GL."MA_TAI_KHOAN" LIKE N'154%%'
                AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_CPSX
                OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                )
                THEN GL."GHI_NO"
                - GL."GHI_CO"
                ELSE 0
                END)              AS "DO_DANG_DAU_KY" -- Dở dang cuối kỳ

                FROM so_cai_chi_tiet GL
                INNER JOIN TMP_DS_CONG_TRINH P ON GL."CONG_TRINH_ID" = P."CONG_TRINH_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
                LEFT JOIN danh_muc_khoan_muc_cp E ON E."id" = GL."KHOAN_MUC_CP_ID"
                /*DDKhanh CR133811 31/08/2017 Lấy thêm các trường mở rộng*/
                --                                     LEFT JOIN CustomField"SO_CAI" CFL ON GL."CHI_TIET_ID" = CFL.RefDetailID AND CFL.IsPostToManagementBook = @IsWorkingWithManagementBook
                WHERE GL."NGAY_HACH_TOAN" <= den_ngay
                AND ("MA_TAI_KHOAN" LIKE N'511%%'
                OR "MA_TAI_KHOAN" LIKE N'711%%'
                OR "MA_TAI_KHOAN" LIKE N'515%%'

                OR ("MA_TAI_KHOAN" LIKE N'521%%'
                AND CHE_DO_KE_TOAN = '15'
                )
                OR ("MA_TAI_KHOAN" LIKE N'511%%'
                AND GL."LOAI_NGHIEP_VU" IS NOT NULL
                AND CHE_DO_KE_TOAN = '48'
                )
                OR "MA_TAI_KHOAN" LIKE N'632%%'
                OR "MA_TAI_KHOAN" LIKE N'154%%'
                OR "MA_TAI_KHOAN" LIKE N'6421%%'
                OR "MA_TAI_KHOAN" LIKE N'6422%%'
                OR "MA_TAI_KHOAN" LIKE N'811%%'
                OR "MA_TAI_KHOAN" LIKE N'635%%'
                )

                GROUP BY P."CONG_TRINH_ID",
                P."MA_PHAN_CAP",
                GL."NGAY_HACH_TOAN",
                GL."NGAY_CHUNG_TU",
                GL."SO_CHUNG_TU",
                GL."NGAY_HOA_DON",
                GL."SO_HOA_DON",
                GL."DIEN_GIAI_CHUNG",
                GL."ID_CHUNG_TU",
                GL."MODEL_CHUNG_TU"

                UNION ALL
                SELECT
                J."id"
                , 'gia.thanh.ky.tinh.gia.thanh' AS "MODEL_CHUNG_TU"
                , J."DEN_NGAY"
                , J."DEN_NGAY"
                , ''                            AS "SO_CHUNG_TU"
                , NULL :: TIMESTAMP             AS "NGAY_HOA_DON"
                , ''                            AS "SO_HOA_DON"
                , J."TEN"
                , P."CONG_TRINH_ID"
                , P."MA_PHAN_CAP"
                , 0                             AS "DOANH_THU_PHAT_SINH"
                , 0                             AS "DOANH_THU_THU_NHAP_KHAC"
                , 0                             AS "GIAM_TRU_DOANH_THU"
                , 0                             AS "GIA_VON"
                ,
                -- Giá vốn hàng bán: + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 632 trên chứng từ phân bổ chi phí BH, QLDN, khác
                0                             AS "CHI_PHI_BAN_HANG"
                ,
                -- Chi phí bán hàng + + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 6421 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                0                             AS "CHI_PHI_QUAN_LY"
                ,
                -- Chi phí quản lý + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 6422 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                0                             AS "CHI_PHI_KHAC"
                ,
                -- Chi phí khác + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 811, 635 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                SUM(CASE WHEN J."DEN_NGAY" < tu_ngay

                AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_CPSX
                OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                )
                THEN JCAD."SO_TIEN"
                ELSE 0
                END)                      AS "DO_DANG_DAU_KY"
                , SUM(CASE WHEN J."DEN_NGAY" BETWEEN tu_ngay AND den_ngay

                AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                THEN JCAD."SO_TIEN"
                ELSE 0
                END)                      AS "NGUYEN_VAT_LIEU"
                , SUM(CASE WHEN J."DEN_NGAY" BETWEEN tu_ngay AND den_ngay

                AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                THEN JCAD."SO_TIEN"
                ELSE 0
                END)                      AS "NHAN_CONG"
                , -- +
                SUM(CASE WHEN J."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
                --AND ( SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAD."TAI_KHOAN_ID") LIKE N'154%%'
                AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                THEN JCAD."SO_TIEN"
                ELSE 0
                END)                      AS "MAY_THI_CONG"
                ,
                --+ + Tổng số tiền phân bổ của TK 154 của KMCP MTC cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                SUM(CASE WHEN J."DEN_NGAY" BETWEEN tu_ngay AND den_ngay
                --AND ( SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAD."TAI_KHOAN_ID") LIKE N'154%%'
                AND E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                THEN JCAD."SO_TIEN"
                ELSE 0
                END)                      AS "CHI_PHI_CHUNG"
                ,
                --+ + Tổng số tiền phân bổ của TK 154 của KMCP SXC cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                0                             AS "KHOAN_GIAM_GIA_THANH"
                , SUM(CASE WHEN J."DEN_NGAY" <= den_ngay
                --AND ( SELECT "SO_TAI_KHOAN" FROM danh_muc_he_thong_tai_khoan TK WHERE TK.id = JCAD."TAI_KHOAN_ID") LIKE N'154%%'
                AND (E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_CPSX
                OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NVLTT
                OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_NCTT
                OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_MTC
                OR E."MA_PHAN_CAP" LIKE MA_PHAN_CAP_SXC
                )
                THEN JCAD."SO_TIEN"
                ELSE 0
                END)                      AS "DO_DANG_CUOI_KY"

                FROM gia_thanh_ket_qua_phan_bo_chi_phi_chung JCAD
                INNER JOIN gia_thanh_ky_tinh_gia_thanh J ON J."id" = JCAD."KY_TINH_GIA_THANH_ID"
                INNER JOIN TMP_DS_CONG_TRINH P ON P."CONG_TRINH_ID" = JCAD."MA_CONG_TRINH_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = J."CHI_NHANH_ID"
                LEFT JOIN danh_muc_khoan_muc_cp E ON E."id" = JCAD."KHOAN_MUC_CP_ID"
                WHERE J."DEN_NGAY" <= den_ngay --Lấy tất cả các lần phân bổ của kỳ tính giá thành hiện tại và trước đó

                GROUP BY
                P."CONG_TRINH_ID",
                P."MA_PHAN_CAP",
                J."DEN_NGAY",
                J."DEN_NGAY",
                J."TEN",
                J."id"

                UNION ALL
                SELECT
                JC."id"
                , 'tong.hop.phan.bo.chi.phi.bh.qldn.chi.phi.khac.cho.don.vi' AS "MODEL_CHUNG_TU"
                , JC."NGAY_CHUNG_TU"
                , JC."NGAY_CHUNG_TU"
                , JC."SO_CHUNG_TU"
                , NULL :: TIMESTAMP                                          AS "NGAY_HOA_DON"
                , ''                                                         AS "SO_HOA_DON"
                , JC."DIEN_GIAI"
                , P."CONG_TRINH_ID"
                , P."MA_PHAN_CAP"
                , 0                                                          AS "DOANH_THU_PHAT_SINH"
                , 0                                                          AS "DOANH_THU_THU_NHAP_KHAC"
                , 0                                                          AS "GIAM_TRU_DOANH_THU"
                , SUM(CASE WHEN (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'632%%'
                THEN JCED."SO_TIEN"
                ELSE 0
                END)                                                   AS "GIA_VON"
                ,
                -- Giá vốn hàng bán: + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 632 trên chứng từ phân bổ chi phí BH, QLDN, khác
                SUM(CASE WHEN (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'6421%%'
                THEN JCED."SO_TIEN"
                ELSE 0
                END)                                                   AS "CHI_PHI_BAN_HANG"
                ,
                -- Chi phí bán hàng + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 641 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                SUM(CASE WHEN (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'6422%%'
                THEN JCED."SO_TIEN"
                ELSE 0
                END)                                                   AS "CHI_PHI_QUAN_LY"
                ,
                -- Chi phí quản lý + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 642 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                SUM(CASE WHEN ((SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'811%%'
                OR (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JCED."TAI_KHOAN_ID") LIKE N'635%%'
                )
                THEN JCED."SO_TIEN"
                ELSE 0
                END)                                                   AS "CHI_PHI_KHAC"
                ,
                -- Chi phí khác + số tiền phân bổ cho từng công trình tương ứng với TK chi phí là 811, 635 trên chứng từ phân bổ chi phí bán hàng, chi phí quản lý DN, khác
                0                                                          AS "DO_DANG_DAU_KY"
                ,
                --  + Tổng số tiền phân bổ của TK 621, 622, 623, 627 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc < “Từ ngày của kỳ báo cáo - PS Có TK 154 chi tiết theo từng công trình trên các chứng từ có ngày hạch toán < "Từ ngày" của kỳ báo cáo + Số đã nghiệm thu trên form Nhập lũy kế chi phí phát sinh cho công trình/đơn hàng/hợp đồng kỳ trước tương ứng với TK 154
                0                                                          AS "NGUYEN_VAT_LIEU"
                ,
                -- + Tổng số tiền phân bổ của TK 621 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                0                                                          AS "NHAN_CONG"
                ,
                -- + Tổng số tiền phân bổ của TK 622 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo
                0                                                          AS "MAY_THI_CONG"
                ,
                --+ Tổng số tiền phân bổ của TK 623 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                0                                                          AS "CHI_PHI_CHUNG"
                ,
                --+ Tổng số tiền phân bổ của TK 627 cho từng công trình trên bảng phân bổ chi phí chung của kỳ tính giá thành có ngày cuối của kỳ tính giá thành thuộc kỳ xem báo cáo này
                0                                                          AS "KHOAN_GIAM_GIA_THANH"
                , 0                                                          AS "DO_DANG_CUOI_KY"

                FROM tong_hop_phan_bo_chi_phi_bh_qldn_chi_phi_khac_cho_don_vi JC
                INNER JOIN tong_hop_phan_bo_chi_phi_bh_qldn_chi_tiet_phan_bo JCED
                ON JCED."PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID" = JC."id"
                INNER JOIN TMP_DS_CONG_TRINH P ON P."CONG_TRINH_ID" = JCED."MA_DON_VI_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JC."CHI_NHANH_ID"
                WHERE JCED."CAP_TO_CHUC" = '1'
                AND JC."NGAY_CHUNG_TU" BETWEEN tu_ngay AND den_ngay

                GROUP BY
                P."CONG_TRINH_ID",
                P."MA_PHAN_CAP",
                JC."NGAY_CHUNG_TU",
                JC."NGAY_CHUNG_TU",
                JC."SO_CHUNG_TU",
                JC."DIEN_GIAI",
                JC."id"

                ;


                END IF
                ;


                -- Insert dở dang đầu kỳ
                INSERT INTO TMP_DU_LIEU_SO_CAI
                SELECT
                JO."id"
                , 'account.ex.chi.phi.do.dang' AS "MODEL_CHUNG_TU"

                , NULL :: TIMESTAMP            AS "NGAY_HACH_TOAN"
                , NULL :: TIMESTAMP            AS "NGAY_CHUNG_TU"
                , 'OPN'                        AS "SO_CHUNG_TU"
                , NULL :: TIMESTAMP            AS "NGAY_HOA_DON"
                , ''                           AS "SO_HOA_DON"
                , ''                           AS "DIEN_GIAI"
                , JP."CONG_TRINH_ID"
                , JP."MA_PHAN_CAP"
                , 0                            AS "DOANH_THU_PHAT_SINH"
                , 0                            AS "DOANH_THU_THU_NHAP_KHAC"
                , 0                            AS "GIAM_TRU_DOANH_THU"
                , 0                            AS "GIA_VON"
                , -- Giá vốn hàng bán
                0                            AS "CHI_PHI_BAN_HANG"
                , -- Chi phí bán hàng
                0                            AS "CHI_PHI_QUAN_LY"
                , -- Chi phí quản lý
                0                            AS "CHI_PHI_KHAC"
                , -- Chi phí khác
                SUM(JO."SO_CHUA_NGHIEM_THU") AS "DO_DANG_DAU_KY"
                , 0                            AS "NGUYEN_VAT_LIEU"
                , 0                            AS "NHAN_CONG"
                , 0                            AS "MAY_THI_CONG"
                , 0                            AS "CHI_PHI_CHUNG"
                , 0                            AS "KHOAN_GIAM_GIA_THANH"
                , SUM(JO."SO_CHUA_NGHIEM_THU") AS "DO_DANG_CUOI_KY"

                FROM TMP_DS_CONG_TRINH JP
                LEFT JOIN account_ex_chi_phi_do_dang JO ON JO."MA_CONG_TRINH_ID" = JP."CONG_TRINH_ID"
                INNER JOIN TMP_LIST_BRAND B ON B."CHI_NHANH_ID" = JO."CHI_NHANH_ID"
                WHERE (SELECT "SO_TAI_KHOAN"
                FROM danh_muc_he_thong_tai_khoan TK
                WHERE TK.id = JO."TAI_KHOAN_CPSXKD_DO_DANG_ID") LIKE N'154%%'
                GROUP BY
                JP."CONG_TRINH_ID",
                JP."MA_PHAN_CAP",
                JO."id"
                ;


                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA
                AS

                SELECT
                ROW_NUMBER()
                OVER (
                ORDER BY JP."TEN_CONG_TRINH", "NGAY_HACH_TOAN", "NGAY_CHUNG_TU", "SO_CHUNG_TU" ) AS "RowNum"
                , CC.*
                , CC."DOANH_THU_PHAT_SINH" +
                CC."DOANH_THU_THU_NHAP_KHAC"                                                         AS "TONG_THANH_TOAN"
                , /*Doanh thu thuần*/
                CC."DOANH_THU_PHAT_SINH" + CC."DOANH_THU_THU_NHAP_KHAC"
                -
                "GIAM_TRU_DOANH_THU"                                                                 AS "DOANH_THU_THUAN"
                , /*Cột cộng chi phí phát sinh*/
                "NGUYEN_VAT_LIEU" + "NHAN_CONG" + "MAY_THI_CONG" +
                "CHI_PHI_CHUNG"                                                                      AS "CHI_PHI_PHAT_SINH_CONG"
                , /*Lãi lỗ */
                CC."DOANH_THU_PHAT_SINH" + CC."DOANH_THU_THU_NHAP_KHAC"
                - "GIAM_TRU_DOANH_THU" - "GIA_VON"   -- Giá vốn hàng bán
                - "CHI_PHI_BAN_HANG" -- Chi phí bán hàng
                - "CHI_PHI_QUAN_LY"-- Chi phí quản lý
                - "CHI_PHI_KHAC" -- Chi phí khác
                AS "LAI_LO"
                ,
                JP."MA_CONG_TRINH"                                                                   AS "MA_CONG_TRINH"
                , JP."TEN_CONG_TRINH"
                , JP."LOAI_CONG_TRINH"
                FROM TMP_DU_LIEU_SO_CAI CC
                LEFT JOIN TMP_CONG_TRINH_DUOC_CHON_1 AS JP ON CC."MA_PHAN_CAP" LIKE JP."MA_PHAN_CAP"
                || '%%'
                WHERE (CC."DOANH_THU_PHAT_SINH" + CC."DOANH_THU_THU_NHAP_KHAC") <> 0
                OR ("GIAM_TRU_DOANH_THU") <> 0
                OR ("GIA_VON") <> 0
                OR ("CHI_PHI_BAN_HANG") <> 0
                OR ("CHI_PHI_QUAN_LY") <> 0
                OR ("CHI_PHI_KHAC") <> 0
                OR ("NGUYEN_VAT_LIEU") <> 0
                OR ("NHAN_CONG") <> 0
                OR ("MAY_THI_CONG") <> 0
                OR ("CHI_PHI_CHUNG") <> 0
                OR ("KHOAN_GIAM_GIA_THANH") <> 0
                ;
                END $$
                ;
                SELECT 
                "TEN_CONG_TRINH" AS "TEN_CONG_TRINH",
                "NGAY_HACH_TOAN" AS "NGAY_HACH_TOAN",
                "NGAY_CHUNG_TU" AS "NGAY_CHUNG_TU",
                "SO_CHUNG_TU" AS "SO_CHUNG_TU",
                "DIEN_GIAI" AS "DIEN_GIAI",
                "DOANH_THU_PHAT_SINH" AS "DOANH_THU_PHAT_SINH",
                "GIAM_TRU_DOANH_THU" AS "GIAM_TRU_DOANH_THU",
                "DOANH_THU_THUAN" AS "DOANH_THU_THUAN",
                "NGUYEN_VAT_LIEU" AS "NGUYEN_VAT_LIEU",
                "NHAN_CONG" AS "NHAN_CONG",
                "MAY_THI_CONG" AS "MAY_THI_CONG",
                "CHI_PHI_CHUNG" AS "CHI_PHI_CHUNG",
                "CHI_PHI_PHAT_SINH_CONG" AS "CHI_PHI_PHAT_SINH_CONG",
                "KHOAN_GIAM_GIA_THANH" AS "KHOAN_GIAM_GIA_THANH",
                "GIA_VON" AS "GIA_VON",
                "CHI_PHI_BAN_HANG" AS "CHI_PHI_BAN_HANG",
                "CHI_PHI_QUAN_LY" AS "CHI_PHI_QUAN_LY",
                "CHI_PHI_KHAC" AS "CHI_PHI_KHAC",
                "LAI_LO" AS "LAI_LO",
                "ID_CHUNG_TU" AS "ID_GOC",
                "MODEL_CHUNG_TU" AS "MODEL_GOC"

                FROM TMP_KET_QUA
                ORDER BY "RowNum"
                
                OFFSET %(offset)s
                LIMIT %(limit)s;
                ;
                """
        return self.execute(query,params_sql)

    def _action_view_report(self):
        # self._validate()
        self._validate()
        TU_NGAY_F = self.get_vntime('TU')
        DEN_NGAY_F = self.get_vntime('DEN')
        HIEN_THI_THEO = self.get_context('HIEN_THI_THEO')
        param = 'Từ ngày: %s đến ngày %s' % (TU_NGAY_F, DEN_NGAY_F)
        if HIEN_THI_THEO=='MAU_DOC':
            action = self.env.ref('bao_cao.open_report_gia_thanh_chi_tiet_lai_lo_theo_cong_trinh_mau_doc').read()[0]
        if HIEN_THI_THEO=='MAU_NGANG':
            action = self.env.ref('bao_cao.open_report_gia_thanh_chi_tiet_lai_lo_theo_cong_trinh_mau_ngang').read()[0]
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action