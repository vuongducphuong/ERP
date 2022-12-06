# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_B02DN_BAO_CAO_KET_QUA_HOAT_DONG_KINH_DOANH(models.Model):
    _name = 'bao.cao.b02dn.bao.cao.kq.hoat.dong.kinh.doanh'
   
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TU_NGAY = fields.Date(string='Từ', help='Từ ngày',required=True,default=fields.Datetime.now)
    DEN_NGAY = fields.Date(string='Đến', help='Đến ngày',required=True,default=fields.Datetime.now)
    DOANH_NGHIEP_SELECTION = fields.Selection([('DOANH_NGHIEP_DAP_UNG_GIA_DINH_HOAT_DONG_LIEN_TUC', 'Doanh nghiệp đáp ứng giả định hoạt động liên tục'), ('DOANH_NGHIEP_KHONG_DAP_UNG_GIA_DINH_HOAT_DONG_LIEN_TUC', 'Doanh nghiệp không đáp ứng giả định hoạt động liên tục'), ], string='NO_SAVE',default='DOANH_NGHIEP_DAP_UNG_GIA_DINH_HOAT_DONG_LIEN_TUC')
    LAY_DU_LIEU_TU_BCTC_DA_LAP = fields.Boolean(string='Lấy dữ liệu từ BCTC đã lập', help='Lấy dữ liệu từ báo cáo tài chính đã lập')
    BU_TRU_CONG_NO_CUA_CUNG_DOI_TUONG_GIUA_CAC_CHI_NHANH = fields.Boolean(string='Bù trừ công nợ của cùng đối tượng giữa các chi nhánh', help='Bù trừ công nợ của cùng đối tượng giữa các chi nhánh')
    KHONG_HIEN_THI_CAC_CHI_TIEU_CO_SO_LIEU_BANG_KHONG = fields.Boolean(string='Không hiển thị các chỉ tiêu có số liệu = 0', help='Không hiển thị các chỉ tiêu có số liệu bằng không')
    BCTC_DA_DUOC_KIEM_TOAN = fields.Boolean(string='BCTC đã được kiểm toán', help='Báo cáo tài chính đã được kiểm toán')
    Y_KIEN_KIEM_TOAN = fields.Selection([('Y_KIEN_TRAI_NGUOC', 'Ý kiến trái ngược'), ('Y_KIEN_TU_CHOI_DUA_RA_Y_KIEN', 'Ý kiến từ chối đưa ra ý kiến'), ('Y_KIEN_NGOAI_TRU', 'Ý kiến ngoại trừ'), ('Y_KIEN_CHAP_NHAN_TOAN_PHAN', 'Ý kiến chấp nhận toàn phần'), ], string='Ý kiến kiểm toán', help='Ý kiến kiểm toán')
    GIAM_DOC = fields.Char(string='Giám đốc', help='Giám đốc')
    NGAY_LAP = fields.Date(string='Ngày lập', help='Ngày lập',required=True,default=fields.Datetime.now)
    CHI_TIEU = fields.Char(string='Chỉ tiêu', help='Chỉ tiêu')
    MA_SO = fields.Char(string='Mã số', help='Mã số')
    THUYET_MINH = fields.Char(string='Thuyết minh', help='Thuyết minh')
    KY_NAY = fields.Float(string='Kỳ này', help='Kỳ này',digits= decimal_precision.get_precision('VND'))
    KY_TRUOC = fields.Float(string='Kỳ trước', help='Kỳ trước',digits= decimal_precision.get_precision('VND'))


    ### START IMPLEMENTING CODE ###
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_B02DN_BAO_CAO_KET_QUA_HOAT_DONG_KINH_DOANH, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],order="MA_DON_VI",limit=1)
        if chi_nhanh:
          result['CHI_NHANH_ID'] = chi_nhanh.id
        result['GIAM_DOC'] = self.get_giam_doc()
        arr_lap_bao_cao_tai_chinh_chi_tiet = []
        return result

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU_NGAY', 'DEN_NGAY')

    @api.onchange('BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC')
    def _onchange_bao_gom_so_lieu_chi_nhanh_phu_thuoc(self):
        if self.LAY_DU_LIEU_TU_BCTC_DA_LAP == True:
            self.LAY_DU_LIEU_TU_BCTC_DA_LAP = False
            
    
    @api.onchange('LAY_DU_LIEU_TU_BCTC_DA_LAP')
    def _onchange_LAY_DU_LIEU_TU_BCTC_DA_LAP(self):
        self.Y_KIEN_KIEM_TOAN = None
        if self.BCTC_DA_DUOC_KIEM_TOAN ==True:
            self.BCTC_DA_DUOC_KIEM_TOAN = False


    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DOANH_NGHIEP_SELECTION = params['DOANH_NGHIEP_SELECTION'] if 'DOANH_NGHIEP_SELECTION' in params.keys() else 'False'
        Y_KIEN_KIEM_TOAN = params['Y_KIEN_KIEM_TOAN'] if 'Y_KIEN_KIEM_TOAN' in params.keys() else 'False'
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
        LAY_DU_LIEU_TU_BCTC_DA_LAP = 1 if 'LAY_DU_LIEU_TU_BCTC_DA_LAP' in params.keys() and params['LAY_DU_LIEU_TU_BCTC_DA_LAP'] != 'False' else 0
        BU_TRU_CONG_NO_CUA_CUNG_DOI_TUONG_GIUA_CAC_CHI_NHANH = 1 if 'BU_TRU_CONG_NO_CUA_CUNG_DOI_TUONG_GIUA_CAC_CHI_NHANH' in params.keys() and params['BU_TRU_CONG_NO_CUA_CUNG_DOI_TUONG_GIUA_CAC_CHI_NHANH'] != 'False' else 0
        KHONG_HIEN_THI_CAC_CHI_TIEU_CO_SO_LIEU_BANG_KHONG = 1 if 'KHONG_HIEN_THI_CAC_CHI_TIEU_CO_SO_LIEU_BANG_KHONG' in params.keys() and params['KHONG_HIEN_THI_CAC_CHI_TIEU_CO_SO_LIEU_BANG_KHONG'] != 'False' else 0
        BCTC_DA_DUOC_KIEM_TOAN = 1 if 'BCTC_DA_DUOC_KIEM_TOAN' in params.keys() and params['BCTC_DA_DUOC_KIEM_TOAN'] != 'False' else 0
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None


        tu_ngay = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z')
        den_ngay = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z')
        so_ngay_trong_thang = helper.Datetime.lay_so_ngay_trong_thang(den_ngay.year, den_ngay.month)
        ngay_cuoi_thang = '%s-%s-%s' % (den_ngay.year,den_ngay.month,so_ngay_trong_thang)
        ngay_cuoi_thang_datetiome = datetime.strptime(ngay_cuoi_thang, '%Y-%m-%d').date()
        hieu_thang = den_ngay.month - tu_ngay.month

        tu_ngay_ky_truoc = False
        den_ngay_ky_truoc = False

        thang_den_ngay_ky_truoc = 0
        nam_den_ngay_ky_truoc = 0

        if hieu_thang == 0:
            if tu_ngay.month == 1:
                tu_ngay_ky_truoc = '%s-%s-%s' % (tu_ngay.year - 1,12,1)
                # den_ngay_ky_truoc = '%s-%s-%s' % (tu_ngay.year - 1,12,31)
                nam_den_ngay_ky_truoc = tu_ngay.year - 1
                thang_den_ngay_ky_truoc = 12
            else:
                tu_ngay_ky_truoc = '%s-%s-%s' % (tu_ngay.year,tu_ngay.month - 1,1)
                # den_ngay_ky_truoc = '%s-%s-%s' % (den_ngay.year,den_ngay.month - 1,ngay_cuoi_thang_datetiome.day)
                nam_den_ngay_ky_truoc = den_ngay.year
                thang_den_ngay_ky_truoc = den_ngay.month - 1
        elif hieu_thang == 2:
            if tu_ngay.month == 1:
                tu_ngay_ky_truoc = '%s-%s-%s' % (tu_ngay.year - 1,10,1)
                # den_ngay_ky_truoc = '%s-%s-%s' % (den_ngay.year - 1,12,31)
                nam_den_ngay_ky_truoc = den_ngay.year - 1
                thang_den_ngay_ky_truoc = 12
            else:
                tu_ngay_ky_truoc = '%s-%s-%s' % (tu_ngay.year,tu_ngay.month - 3,1)
                # den_ngay_ky_truoc = '%s-%s-%s' % (den_ngay.year,den_ngay.month - 3,ngay_cuoi_thang_datetiome.day)
                nam_den_ngay_ky_truoc = den_ngay.year
                thang_den_ngay_ky_truoc = den_ngay.month - 3
        elif hieu_thang == 11:
            tu_ngay_ky_truoc = '%s-%s-%s' % (tu_ngay.year -1,1,1)
            # den_ngay_ky_truoc = '%s-%s-%s' % (den_ngay.year -1,12,31)
            nam_den_ngay_ky_truoc = den_ngay.year -1
            thang_den_ngay_ky_truoc = 12
        
        so_ngay_trong_thang_den_ngay_ky_sau = helper.Datetime.lay_so_ngay_trong_thang(nam_den_ngay_ky_truoc, thang_den_ngay_ky_truoc)
        den_ngay_ky_truoc = '%s-%s-%s' % (nam_den_ngay_ky_truoc,thang_den_ngay_ky_truoc,so_ngay_trong_thang_den_ngay_ky_sau)

        params_sql = {
            'TU_NGAY':TU_NGAY_F,
            'DEN_NGAY':DEN_NGAY_F,
            'DOANH_NGHIEP_SELECTION':DOANH_NGHIEP_SELECTION,
            'Y_KIEN_KIEM_TOAN':Y_KIEN_KIEM_TOAN,
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'LAY_DU_LIEU_TU_BCTC_DA_LAP':LAY_DU_LIEU_TU_BCTC_DA_LAP,
            'BU_TRU_CONG_NO_CUA_CUNG_DOI_TUONG_GIUA_CAC_CHI_NHANH':BU_TRU_CONG_NO_CUA_CUNG_DOI_TUONG_GIUA_CAC_CHI_NHANH,
            'KHONG_HIEN_THI_CAC_CHI_TIEU_CO_SO_LIEU_BANG_KHONG':KHONG_HIEN_THI_CAC_CHI_TIEU_CO_SO_LIEU_BANG_KHONG,
            'BCTC_DA_DUOC_KIEM_TOAN':BCTC_DA_DUOC_KIEM_TOAN,
            'TU_NGAY_BAO_CAO_TRUOC' : tu_ngay_ky_truoc,
            'DEN_NGAY_BAO_CAO_TRUOC' : den_ngay_ky_truoc,
            'CHI_NHANH_ID':CHI_NHANH_ID,
            'limit': limit,
            'offset': offset,
        }

        query = """
        DO LANGUAGE plpgsql $$
        DECLARE
            ts_chi_nhanh_id                                  INTEGER := %(CHI_NHANH_ID)s;  -- chi nhánh

            ts_bao_gom_chi_nhanh_phu_thuoc                   INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;  -- bao gốm số liệu chi nhánh phụ thuộc

            ts_tu_ngay                                       DATE := %(TU_NGAY)s;  -- từ ngày

            ts_den_ngay                                      DATE := %(DEN_NGAY)s;   -- đến ngày

            ts_PrevFromDate                                  DATE := %(TU_NGAY_BAO_CAO_TRUOC)s;

            ts_PrevToDate                                    DATE := %(DEN_NGAY_BAO_CAO_TRUOC)s;

            ts_lay_so_lieu_tu_bao_cao_da_lap                 INTEGER := %(LAY_DU_LIEU_TU_BCTC_DA_LAP)s;  -- lấy số liệu từ BCTC đã lập

            ts_khong_hien_thi_cac_chi_tieu_co_so_lieu_bang_0 INTEGER := %(KHONG_HIEN_THI_CAC_CHI_TIEU_CO_SO_LIEU_BANG_KHONG)s; -- Không hiển thị các chỉ tiêu có số liệu = 0
        BEGIN
            IF ts_lay_so_lieu_tu_bao_cao_da_lap = 1
            THEN
                DROP TABLE IF EXISTS TMP_KET_QUA1
                ;

                CREATE TEMP TABLE TMP_KET_QUA1
                    AS
                        SELECT *
                        FROM danh_muc_he_thong_tai_khoan
                ;

                --             SELECT  @RefID = RefID ,
                --                         @ReportCreatedDate = ReportCreatedDate ,
                --                         @ReportCreatedBy = ReportCreatedBy ,
                --                         @DirectorName = DirectorName
                --                 FROM    dbo.FrReportlist
                --                 WHERE   --FromDate = @FromDate

                --                         --AND ToDate = @ToDate
                --                         DAY(FromDate) = DAY(@FromDate)
                --                         AND MONTH(FromDate) = MONTH(@FromDate)
                --                         AND YEAR(FromDate) = YEAR(@FromDate)
                --                         AND DAY(ToDate) = DAY(@ToDate)
                --                         AND MONTH(ToDate) = MONTH(@ToDate)
                --                         AND YEAR(ToDate) = YEAR(@ToDate)
                --                         AND Reftype = 4050
                --                         AND ( AccountingSystem = @AccountingSystem
                --                               OR ( @AccountingSystem = 48
                --                                    AND AccountingSystem = 2015
                --                                  )
                --                             )/*add by hoant 16.09.2016 theo cr 116741*/
                --                         AND BranchID = @BranchID
                --                         AND ( @IsWorkingWithManagementBook = 1
                --                               AND DisplayOnBook = 1
                --                               OR @IsWorkingWithManagementBook = 0
                --                               AND DisplayOnBook = 0
                --                             )
                --                 SELECT  A.ReportDetailID ,
                --                         A.RefID ,
                --                         A.ReportType ,
                --                         A.ItemID ,
                --                         A.ItemCode ,
                --                         A.ItemName ,
                --                         -- LVDiep 09/07/2016: Nếu chỉ tiêu tiếng anh là trống thì lấy chỉ tiêu tiếng việt để hiển thị trên báo cáo
                --                         --ItemNameEnglish ,
                --                         ISNULL(A.ItemNameEnglish, A.ItemName) AS ItemNameEnglish ,
                --                         A.ItemIndex ,
                --                         A.Description ,
                --                         A.FormulaType ,
                --                         A.FormulaFrontEnd ,
                --                         A.Amount ,
                --                         A.PrevAmount ,
                --                         A.Hidden ,
                --                         A.IsBold ,
                --                         A.IsItalic ,
                --                         A.SortOrder ,
                --                         A.Category ,
                --                         A.Formula ,
                --                         @ReportCreatedDate AS ReportCreatedDate ,
                --                         @ReportCreatedBy AS ReportCreatedBy ,
                --                         @DirectorName AS DirectorName ,
                --                         FRL.AccountingSystem/*add by hoant 16.09.2016 theo cr 116741*/
                --                 FROM    FRReportDetail A
                --                         INNER JOIN dbo.FRReportList AS FRL ON A.RefID = FRL.RefID
                --                 WHERE   A.RefID = @RefID
                --                         AND A.ReportType = '2'
                --                         AND A.Hidden = 0
                --                         -- Ntquang 26/10/2017 - CR150420- bổ sung tùy chọn: Không hiển thị các chỉ tiêu có số liệu = 0
                --                         -- cho phép hiển thị các chỉ tiêu tổng hợp, không thiết lập công thức có số liệu = 0
                --                         AND ( @NonDisplayItemHasNoData = 0
                --                               OR ( @NonDisplayItemHasNoData = 1
                --                                    AND ( ( A.Amount <> 0
                --                                            OR A.PrevAmount <> 0
                --                                          )
                --                                          -- Luôn cho phép hiển thị các chỉ tiêu tổng hợp, không thiết lập công thức
                --                                          OR ( A.FormulaType = 1
                --                                               AND ISNULL(A.FormulaFrontEnd, '') = ''
                --                                             )
                --                                        )
                --                                  )
                --                             )
                --                 ORDER BY A.ItemIndex

            ELSE
                DROP TABLE IF EXISTS TMP_KET_QUA1
                ;

                CREATE TEMP TABLE TMP_KET_QUA1
                    AS
                        SELECT
                            FR."ID_CHI_TIEU"
                            , FR."MA_CHI_TIEU"
                            , FR."TEN_CHI_TIEU"
                            , coalesce(FR."TEN_TIENG_ANH", FR."TEN_CHI_TIEU") AS "TEN_TIENG_ANH"
                            , FR."SO_THU_TU"
                            , FR."THUYET_MINH"
                            , FR."LOAI_CHI_TIEU"
                            , FR."CONG_THUC"
                            , FR."KHONG_IN"
                            , FR."IN_DAM"
                            , FR."IN_NGHIENG"
                            , FR."SO_TIEN"
                            , FR."SO_TIEN_DAU_NAM"
                        --                 @ReportCreatedDate AS ReportCreatedDate ,
                        --                 @ReportCreatedBy AS ReportCreatedBy ,
                        --                 @DirectorName AS DirectorName ,
                        --                 @AccountingSystem AS AccountingSystem
                        FROM GET_BAO_CAO_TAI_CHINH_B02_DN(ts_chi_nhanh_id, ts_bao_gom_chi_nhanh_phu_thuoc, ts_tu_ngay,
                                                        ts_den_ngay,
                                                        ts_PrevFromDate, ts_PrevToDate) FR
                        WHERE FR."KHONG_IN" = FALSE
                            -- cho phép hiển thị các chỉ tiêu tổng hợp, không thiết lập công thức có số liệu = 0
                            AND (ts_khong_hien_thi_cac_chi_tieu_co_so_lieu_bang_0 = 0
                                OR (ts_khong_hien_thi_cac_chi_tieu_co_so_lieu_bang_0 = 1
                                    AND ((FR."SO_TIEN" <> 0
                                            OR FR."SO_TIEN_DAU_NAM" <> 0
                                            )
                                            -- Luôn cho phép hiển thị các chỉ tiêu tổng hợp, không thiết lập công thức
                                            OR (FR."LOAI_CHI_TIEU" = '1'
                                                AND coalesce(FR."CONG_THUC", '') = ''
                                            )
                                    )
                                )
                            )
                        ORDER BY "SO_THU_TU"
                ;

            END IF
            ;


        END $$
        ;

        SELECT 

            "TEN_CHI_TIEU" as "CHI_TIEU",
            "MA_CHI_TIEU" as "MA_SO",
            "THUYET_MINH" as "THUYET_MINH",
            "SO_TIEN_DAU_NAM" as "KY_TRUOC",
            "SO_TIEN" as "KY_NAY" 

        FROM TMP_KET_QUA1
        OFFSET %(offset)s
        LIMIT %(limit)s;
 """
        return self.execute(query,params_sql)

    ### END IMPLEMENTING CODE ###

    def _validate(self):
        params = self._context
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        if(TU_NGAY=='False'):
            raise ValidationError('Vui lòng nhập thời gian cho Từ ngày !')
        if(DEN_NGAY=='False'):
            raise ValidationError('Vui lòng nhập thời gian cho Đến ngày !')
        # if(TU_NGAY > DEN_NGAY):
        #     raise ValidationError('Từ ngày không được lớn hơn đến ngày !')
        loi = True
        tu_ngay = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z')
        den_ngay = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z')
        so_ngay_trong_thang = helper.Datetime.lay_so_ngay_trong_thang(den_ngay.year, den_ngay.month)
        ngay_cuoi_thang = '%s-%s-%s' % (den_ngay.year,den_ngay.month,so_ngay_trong_thang)
        ngay_cuoi_thang_datetiome = datetime.strptime(ngay_cuoi_thang, '%Y-%m-%d').date()

        if tu_ngay.year == den_ngay.year and tu_ngay.day == 1 and den_ngay.day == ngay_cuoi_thang_datetiome.day:
            # check cùng tháng
            if tu_ngay.month == den_ngay.month:
                loi = False
            # check cùng quý
            if (tu_ngay.month == 1 and den_ngay.month == 3) or (tu_ngay.month == 4 and den_ngay.month == 6) or (tu_ngay.month == 7 and den_ngay.month == 9) or (tu_ngay.month == 10 and den_ngay.month == 12):
                loi = False
            # check cùng năm
            if tu_ngay.month == 1 and den_ngay.month == 12:
                loi = False
        else:
            raise ValidationError('Bạn chỉ có thể xem dữ liệu trong 1 năm và từ ngày là ngày đâu tháng, đến ngày là ngày cuối tháng')

        if loi == True:
            raise ValidationError('Bạn chỉ có thể xem dữ liệu là theo tháng, theo quý, theo năm')

    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU_NGAY')
        DEN_NGAY_F = self.get_vntime('DEN_NGAY')
        param = 'Từ ngày: %s đến ngày %s' % (TU_NGAY_F, DEN_NGAY_F)
        action = self.env.ref('bao_cao.open_report_b02dn_bao_cao_ket_qua_hoat_dong_kinh_doanh').read()[0]
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action


    @api.model_cr
    def init(self):
        self.env.cr.execute(""" 
			DROP FUNCTION IF EXISTS GET_BAO_CAO_TAI_CHINH_B02_DN(IN ts_chi_nhanh_id INTEGER, ts_bao_gom_chi_nhanh_phu_thuoc INTEGER,
                                                           ts_tu_ngay      DATE, ts_den_ngay DATE, ts_PrevFromDate DATE,
                                                           ts_PrevToDate   DATE);
            CREATE OR REPLACE FUNCTION GET_BAO_CAO_TAI_CHINH_B02_DN(IN ts_chi_nhanh_id INTEGER, ts_bao_gom_chi_nhanh_phu_thuoc INTEGER,
                                                                    ts_tu_ngay      DATE, ts_den_ngay DATE, ts_PrevFromDate DATE,
                                                                    ts_PrevToDate   DATE)
                RETURNS TABLE("ID_CHI_TIEU"     VARCHAR(200),
                            "MA_CHI_TIEU"     VARCHAR(255),
                            "TEN_CHI_TIEU"    VARCHAR(255),
                            "TEN_TIENG_ANH"   VARCHAR(255),
                            "SO_THU_TU"       INTEGER,
                            "THUYET_MINH"     VARCHAR(255),
                            "LOAI_CHI_TIEU"   VARCHAR(255),
                            "CONG_THUC"       VARCHAR(255),
                            "KHONG_IN"        BOOLEAN,
                            "IN_DAM"          BOOLEAN,
                            "IN_NGHIENG"      BOOLEAN,
                            "SO_TIEN"         FLOAT,
                            "SO_TIEN_DAU_NAM" FLOAT
                ) AS $$
            DECLARE

                -- ts_chi_nhanh_id INTEGER:= 81;
                -- ts_IncludeDependentBranch INTEGER:= 1;
                -- ts_tu_ngay DATE := '2019-01-01';
                -- ts_den_ngay DATE := '2019-12-31';
                -- ts_PrevFromDate DATE := '2018-01-01';
                -- ts_PrevToDate DATE := '2018-12-31';

                AccountingSystem INTEGER :=15;

                ten_bao_cao      VARCHAR(127) :='BAO_CAO_KET_QUA_HOAT_DONG_KINH_DOANH';

                report_id INTEGER:= 2;

            BEGIN

                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA (
                    "ID_CHI_TIEU"     VARCHAR(200),
                    "MA_CHI_TIEU"     VARCHAR(200),
                    "TEN_CHI_TIEU"    VARCHAR(200),
                    "TEN_TIENG_ANH"   VARCHAR(200),
                    "SO_THU_TU"       INTEGER,
                    "THUYET_MINH"     VARCHAR(200),
                    "LOAI_CHI_TIEU"   VARCHAR(200),
                    "CONG_THUC"       VARCHAR(200),
                    "KHONG_IN"        BOOLEAN,
                    "IN_DAM"          BOOLEAN,
                    "IN_NGHIENG"      BOOLEAN,
                    "SO_TIEN"         FLOAT,
                    "SO_TIEN_DAU_NAM" FLOAT
                )
                ;

                SELECT value
                INTO AccountingSystem
                FROM ir_config_parameter
                WHERE key = 'he_thong.CHE_DO_KE_TOAN'
                FETCH FIRST 1 ROW ONLY
                ;

                DROP TABLE IF EXISTS TBL_BRANCH
                ;

                CREATE TEMP TABLE TBL_BRANCH
                    AS
                        SELECT *FROM LAY_DANH_SACH_CHI_NHANH(ts_chi_nhanh_id,ts_bao_gom_chi_nhanh_phu_thuoc)
                ;

                DROP TABLE IF EXISTS TBL_ITEM
                ;

                CREATE TEMP TABLE TBL_ITEM
                    AS
                        SELECT
                            DT."ID_CHI_TIEU"
                            , DT."MA_CHI_TIEU"
                            , DT."TEN_CHI_TIEU"
                            , CASE WHEN CT."PHEP_TINH" = 'CONG'
                            THEN 1
                            ELSE -1 END AS "PHEP_TINH"
                            , CT."KY_HIEU"
                            , CASE WHEN A."SO_TAI_KHOAN" <> ''
                            THEN concat(A."SO_TAI_KHOAN", '%')
                            ELSE '' END AS "SO_TAI_KHOAN_PT"
                            , CASE WHEN A1."SO_TAI_KHOAN" <> ''
                            THEN concat(A1."SO_TAI_KHOAN", '%')
                            ELSE '' END AS "SO_TAI_KHOAN_DOI_UNG_PT"
                            , CASE WHEN DT."LOAI_CHI_TIEU" = '0'
                            THEN 0
                            ELSE 1 END  AS "CHI_TIEU_CHI_TIET_LON_HON_0"

                        FROM tien_ich_thiet_lap_bao_cao_tai_chinh MT
                            INNER JOIN tien_ich_bao_cao_tai_chinh_chi_tiet DT ON MT.id = DT."CHI_TIET_ID"
                            LEFT JOIN tien_ich_xay_dung_cong_thuc_loai_chi_tieu_chi_tiet CT ON DT.id = CT."CHI_TIET_ID"
                            --   LEFT JOIN tien_ich_xay_dung_cong_thuc_loai_chi_tieu_tong_hop TH ON DT.id = TH."CHI_TIET_ID"
                            LEFT JOIN danh_muc_he_thong_tai_khoan A ON A.id = CT."TAI_KHOAN_ID"
                            LEFT JOIN danh_muc_he_thong_tai_khoan A1 ON A1.id = CT."TK_DOI_UNG_ID"
                        WHERE MT."CHE_DO_KE_TOAN" = cast(AccountingSystem AS VARCHAR(127))
                            AND DT."ReportID" = report_id
                            AND (DT."LOAI_CHI_TIEU" = '0' OR DT."LOAI_CHI_TIEU" = '2')
                            AND DT."CONG_THUC" NOTNULL
                ;


                DROP TABLE IF EXISTS BALANCE
                ;

                CREATE TEMP TABLE BALANCE
                    AS
                        SELECT
                            GL."MA_TAI_KHOAN"
                            , GL."MA_TAI_KHOAN_DOI_UNG"
                            , GL."NGAY_HACH_TOAN"
                            , SUM(coalesce("GHI_CO", 0)) AS "GHI_CO"
                            , SUM(coalesce(GL."GHI_NO", 0)) AS "GHI_NO"
                            , SUM(CASE WHEN AC."CHI_TIET_ID" IS NOT NULL
                            THEN coalesce("GHI_CO", 0)
                                ELSE 0
                                END)                   AS "GHI_CO_THEO_CHI_TIET"
                            , SUM(CASE WHEN AC."CHI_TIET_ID" IS NOT NULL
                            THEN coalesce(GL."GHI_NO", 0)
                                ELSE 0
                                END)                   AS "GHI_NO_THEO_CHI_TIET"
                            , CASE WHEN AC."CHI_TIET_ID" IS NULL
                            THEN 0
                            ELSE 1
                            END                        AS "LA_CHI_TIET_THEO"
                            , /*add by hoant 16.09.2016 theo cr 116741*/

                            SUM(CASE WHEN GL."LOAI_NGHIEP_VU" = '0'
                                THEN coalesce("GHI_CO", 0)
                                ELSE 0
                                END)                   AS "GHI_CO_LOAI_NGHIEP_VU_0"
                            , SUM(CASE WHEN GL."LOAI_NGHIEP_VU" = '1'
                            THEN coalesce("GHI_CO", 0)
                                ELSE 0
                                END)                   AS "GHI_CO_LOAI_NGHIEP_VU_1"
                            , SUM(CASE WHEN GL."LOAI_NGHIEP_VU" = '2'
                            THEN coalesce("GHI_CO", 0)
                                ELSE 0
                                END)                   AS "GHI_CO_LOAI_NGHIEP_VU_2"
                            , SUM(CASE WHEN GL."LOAI_NGHIEP_VU" = '0'
                            THEN coalesce(GL."GHI_NO", 0)
                                ELSE 0
                                END)                   AS "GHI_NO_LOAI_NGHIEP_VU_0"
                            , SUM(CASE WHEN GL."LOAI_NGHIEP_VU" = '1'
                            THEN coalesce(GL."GHI_NO", 0)
                                ELSE 0
                                END)                   AS "GHI_NO_LOAI_NGHIEP_VU_1"
                            , SUM(CASE WHEN GL."LOAI_NGHIEP_VU" = '2'
                            THEN coalesce(GL."GHI_NO", 0)
                                ELSE 0
                                END)                   AS "GHI_NO_LOAI_NGHIEP_VU_2"
                        FROM so_cai_chi_tiet GL
                            INNER JOIN TBL_BRANCH B ON GL."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                            LEFT JOIN (
                                        SELECT
                                            "CHI_TIET_ID"
                                            , "CHI_TIET_MODEL"
                                        FROM tong_hop_bctc_nghiep_vu_cho_ct_chi_tiet_form
                                        WHERE "NGHIEP_VU" = '0'
                                    ) AC ON GL."CHI_TIET_ID" = Ac."CHI_TIET_ID" AND GL."CHI_TIET_MODEL" = AC."CHI_TIET_MODEL"
                        WHERE "NGAY_HACH_TOAN" BETWEEN ts_PrevFromDate AND ts_den_ngay
                        GROUP BY GL."MA_TAI_KHOAN",
                            GL."MA_TAI_KHOAN_DOI_UNG",
                            GL."NGAY_HACH_TOAN",
                            /*hoant sửa group by 13.04.2016 */
                            CASE WHEN AC."CHI_TIET_ID" IS NULL
                                THEN 0
                            ELSE 1
                            END
                ;


                DROP TABLE IF EXISTS TBL_MASTER_DETAIL
                ;

                CREATE TEMP TABLE TBL_MASTER_DETAIL
                    AS
                        SELECT
                            I."ID_CHI_TIEU"
                            , I."MA_CHI_TIEU"
                            , NULL AS "ID_CHI_TIEU_CHI_TIET"
                            , 1    AS "PHEP_TINH"
                            , -1   AS "BAC"
                            , -- Là chỉ tiêu chi tiết
                            CASE WHEN I."CHI_TIEU_CHI_TIET_LON_HON_0" = 0
                                        OR (SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ts_tu_ngay AND ts_den_ngay
                                THEN (CASE WHEN I."KY_HIEU" = 'PhatsinhCO'
                                    THEN GL."GHI_CO"
                                        WHEN I."KY_HIEU" IN (
                                            'PhatsinhNO',
                                            'PhatsinhDU')
                                            THEN GL."GHI_NO"
                                        /*add by hoant 16.09.2016 theo cr 116741*/
                                        WHEN I."KY_HIEU" = 'PhatsinhNO_ChitietChietKhauThuongmai'
                                            THEN
                                                GL."GHI_NO_LOAI_NGHIEP_VU_0"
                                        WHEN I."KY_HIEU" = 'PhatsinhNO_ChitietGiamgiaHangBan'
                                            THEN
                                                GL."GHI_NO_LOAI_NGHIEP_VU_1"
                                        WHEN I."KY_HIEU" = 'PhatsinhNO_ChitietTralaiHangBan'
                                            THEN
                                                GL."GHI_NO_LOAI_NGHIEP_VU_2"
                                        WHEN I."KY_HIEU" = 'PhatsinhCO_ChitietChietKhauThuongmai'
                                            THEN
                                                GL."GHI_CO_LOAI_NGHIEP_VU_0"
                                        WHEN I."KY_HIEU" = 'PhatsinhCO_ChitietGiamgiaHangBan'
                                            THEN
                                                GL."GHI_CO_LOAI_NGHIEP_VU_1"
                                        WHEN I."KY_HIEU" = 'PhatsinhCO_ChitietTralaiHangBan'
                                            THEN
                                                GL."GHI_CO_LOAI_NGHIEP_VU_2"
                                        /*end by hoant 16.09.2016 theo cr 116741*/

                                        WHEN I."KY_HIEU" IN (
                                            'PhatsinhCO_ChiTietThanhlyTSCD_BDSDT')
                                            AND GL."LA_CHI_TIET_THEO" = 1
                                            THEN GL."GHI_CO_THEO_CHI_TIET"
                                        WHEN I."KY_HIEU" IN (
                                            'PhatsinhNO_ChiTietThanhlyTSCD_BDSDT')
                                            AND GL."LA_CHI_TIET_THEO" = 1
                                            THEN GL."GHI_NO_THEO_CHI_TIET"
                                        ELSE 0
                                        END) * I."PHEP_TINH"
                                                ELSE 0
                                                END)) > 0
                                THEN (SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ts_tu_ngay AND ts_den_ngay
                                    THEN (CASE WHEN I."KY_HIEU" = 'PhatsinhCO'
                                        THEN GL."GHI_CO"
                                            WHEN I."KY_HIEU" IN (
                                                'PhatsinhNO',
                                                'PhatsinhDU')
                                                THEN GL."GHI_NO"
                                            /*add by hoant 16.09.2016 theo cr 116741*/
                                            WHEN I."KY_HIEU" = 'PhatsinhNO_ChitietChietKhauThuongmai'
                                                THEN
                                                    GL."GHI_NO_LOAI_NGHIEP_VU_0"
                                            WHEN I."KY_HIEU" = 'PhatsinhNO_ChitietGiamgiaHangBan'
                                                THEN
                                                    GL."GHI_NO_LOAI_NGHIEP_VU_1"
                                            WHEN I."KY_HIEU" = 'PhatsinhNO_ChitietTralaiHangBan'
                                                THEN
                                                    GL."GHI_NO_LOAI_NGHIEP_VU_2"
                                            WHEN I."KY_HIEU" = 'PhatsinhCO_ChitietChietKhauThuongmai'
                                                THEN
                                                    GL."GHI_CO_LOAI_NGHIEP_VU_0"
                                            WHEN I."KY_HIEU" = 'PhatsinhCO_ChitietGiamgiaHangBan'
                                                THEN
                                                    GL."GHI_CO_LOAI_NGHIEP_VU_1"
                                            WHEN I."KY_HIEU" = 'PhatsinhCO_ChitietTralaiHangBan'
                                                THEN
                                                    GL."GHI_CO_LOAI_NGHIEP_VU_2"
                                            /*end by hoant 16.09.2016 theo cr 116741*/

                                            WHEN I."KY_HIEU" IN (
                                                'PhatsinhCO_ChiTietThanhlyTSCD_BDSDT')
                                                AND GL."LA_CHI_TIET_THEO" = 1
                                                THEN GL."GHI_CO_THEO_CHI_TIET"
                                            WHEN I."KY_HIEU" IN (
                                                'PhatsinhNO_ChiTietThanhlyTSCD_BDSDT')
                                                AND GL."LA_CHI_TIET_THEO" = 1
                                                THEN GL."GHI_NO_THEO_CHI_TIET"
                                            ELSE 0
                                            END) * I."PHEP_TINH"
                                            ELSE 0
                                            END))
                            ELSE 0
                            END  AS "GHI_NO"
                            , CASE WHEN I."CHI_TIEU_CHI_TIET_LON_HON_0" = 0
                                        OR (SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ts_PrevFromDate
                        AND
                        ts_PrevToDate
                            THEN CASE WHEN I."KY_HIEU" = 'PhatsinhCO'
                                THEN GL."GHI_CO"
                                WHEN I."KY_HIEU" IN (
                                    'PhatsinhNO',
                                    'PhatsinhDU')
                                    THEN GL."GHI_NO"
                                /*add by hoant 16.09.2016 theo cr 116741*/
                                WHEN I."KY_HIEU" = 'PhatsinhNO_ChitietChietKhauThuongmai'
                                    THEN
                                        GL."GHI_NO_LOAI_NGHIEP_VU_0"
                                WHEN I."KY_HIEU" = 'PhatsinhNO_ChitietGiamgiaHangBan'
                                    THEN
                                        GL."GHI_NO_LOAI_NGHIEP_VU_1"
                                WHEN I."KY_HIEU" = 'PhatsinhNO_ChitietTralaiHangBan'
                                    THEN
                                        GL."GHI_NO_LOAI_NGHIEP_VU_2"
                                WHEN I."KY_HIEU" = 'PhatsinhCO_ChitietChietKhauThuongmai'
                                    THEN
                                        GL."GHI_CO_LOAI_NGHIEP_VU_0"
                                WHEN I."KY_HIEU" = 'PhatsinhCO_ChitietGiamgiaHangBan'
                                    THEN
                                        GL."GHI_CO_LOAI_NGHIEP_VU_1"
                                WHEN I."KY_HIEU" = 'PhatsinhCO_ChitietTralaiHangBan'
                                    THEN
                                        GL."GHI_CO_LOAI_NGHIEP_VU_2"
                                /*end by hoant 16.09.2016 theo cr 116741*/


                                WHEN I."KY_HIEU" IN (
                                    'PhatsinhCO_ChiTietThanhlyTSCD_BDSDT')
                                    AND GL."LA_CHI_TIET_THEO" = 1
                                    THEN GL."GHI_CO_THEO_CHI_TIET"
                                WHEN I."KY_HIEU" IN (
                                    'PhatsinhNO_ChiTietThanhlyTSCD_BDSDT')
                                    AND GL."LA_CHI_TIET_THEO" = 1
                                    THEN GL."GHI_NO_THEO_CHI_TIET"
                                ELSE 0
                                END * I."PHEP_TINH"
                                                ELSE 0
                                                END)) > 0
                            THEN SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ts_PrevFromDate
                            AND
                            ts_PrevToDate
                                THEN CASE WHEN I."KY_HIEU" = 'PhatsinhCO'
                                    THEN GL."GHI_CO"
                                    WHEN I."KY_HIEU" IN (
                                        'PhatsinhNO',
                                        'PhatsinhDU')
                                        THEN GL."GHI_NO"
                                    /*add by hoant 16.09.2016 theo cr 116741*/
                                    WHEN I."KY_HIEU" = 'PhatsinhNO_ChitietChietKhauThuongmai'
                                        THEN
                                            GL."GHI_NO_LOAI_NGHIEP_VU_0"
                                    WHEN I."KY_HIEU" = 'PhatsinhNO_ChitietGiamgiaHangBan'
                                        THEN
                                            GL."GHI_NO_LOAI_NGHIEP_VU_1"
                                    WHEN I."KY_HIEU" = 'PhatsinhNO_ChitietTralaiHangBan'
                                        THEN
                                            GL."GHI_NO_LOAI_NGHIEP_VU_2"
                                    WHEN I."KY_HIEU" = 'PhatsinhCO_ChitietChietKhauThuongmai'
                                        THEN
                                            GL."GHI_CO_LOAI_NGHIEP_VU_0"
                                    WHEN I."KY_HIEU" = 'PhatsinhCO_ChitietGiamgiaHangBan'
                                        THEN
                                            GL."GHI_CO_LOAI_NGHIEP_VU_1"
                                    WHEN I."KY_HIEU" = 'PhatsinhCO_ChitietTralaiHangBan'
                                        THEN
                                            GL."GHI_CO_LOAI_NGHIEP_VU_2"
                                    /*end by hoant 16.09.2016 theo cr 116741*/


                                    WHEN I."KY_HIEU" IN (
                                        'PhatsinhCO_ChiTietThanhlyTSCD_BDSDT')
                                        AND GL."LA_CHI_TIET_THEO" = 1
                                        THEN GL."GHI_CO_THEO_CHI_TIET"
                                    WHEN I."KY_HIEU" IN (
                                        'PhatsinhNO_ChiTietThanhlyTSCD_BDSDT')
                                        AND GL."LA_CHI_TIET_THEO" = 1
                                        THEN GL."GHI_NO_THEO_CHI_TIET"
                                    ELSE 0
                                    END * I."PHEP_TINH"
                                    ELSE 0
                                    END)
                            ELSE 0
                            END  AS "GHI_NO_DAU_NAM"
                        FROM TBL_ITEM I
                            INNER JOIN BALANCE AS GL ON (GL."MA_TAI_KHOAN" LIKE I."SO_TAI_KHOAN_PT")
                                                        AND (I."KY_HIEU" <> 'PhatsinhDU'
                                                            OR (I."KY_HIEU" = 'PhatsinhDU'
                                                                AND GL."MA_TAI_KHOAN_DOI_UNG" LIKE I."SO_TAI_KHOAN_DOI_UNG_PT"
                                                            )
                                                        )
                        GROUP BY I."ID_CHI_TIEU",
                            I."MA_CHI_TIEU",
                            I."CHI_TIEU_CHI_TIET_LON_HON_0"
                ;

                INSERT INTO TBL_MASTER_DETAIL (

                    SELECT
                        DT."ID_CHI_TIEU"
                        , DT."MA_CHI_TIEU"
                        , TH."ID_CHI_TIEU" AS "ID_CHI_TIEU_CHI_TIET"
                        , CASE TH."PHEP_TINH"
                        WHEN 'CONG'
                            THEN 1
                        ELSE -1 END      AS "PHEP_TINH"
                        , 0                AS "BAC"
                        , 0                AS "GHI_NO"
                        , 0                AS "GHI_NO_DAU_NAM"
                    FROM tien_ich_thiet_lap_bao_cao_tai_chinh MT
                        INNER JOIN tien_ich_bao_cao_tai_chinh_chi_tiet DT ON MT.id = DT."CHI_TIET_ID"
                        --   LEFT JOIN tien_ich_xay_dung_cong_thuc_loai_chi_tieu_chi_tiet CT ON DT.id = CT."CHI_TIET_ID"
                        LEFT JOIN tien_ich_xay_dung_cong_thuc_loai_chi_tieu_tong_hop TH ON DT.id = TH."CHI_TIET_ID"
                    WHERE MT."CHE_DO_KE_TOAN" = cast(AccountingSystem AS VARCHAR(255))
                        AND "ReportID" = report_id
                        AND DT."LOAI_CHI_TIEU" = '1'
                        AND DT."CONG_THUC" NOTNULL
                )
                ;

                -- Cộng chỉ tiêu con lên chỉ tiêu cha
                WITH RECURSIVE V ( "ID_CHI_TIEU", "ID_CHI_TIEU_CHI_TIET", "GHI_NO", "GHI_NO_DAU_NAM", "PHEP_TINH" )
                AS ( SELECT
                        A."ID_CHI_TIEU"
                        , A."ID_CHI_TIEU_CHI_TIET"
                        , A."GHI_NO"
                        , A."GHI_NO_DAU_NAM"
                        , A."PHEP_TINH"
                    FROM TBL_MASTER_DETAIL A
                    WHERE "BAC" = -1
                    UNION ALL
                    SELECT
                        B."ID_CHI_TIEU"
                        , B."ID_CHI_TIEU_CHI_TIET"
                        , V."GHI_NO"
                        , V."GHI_NO_DAU_NAM"
                        , B."PHEP_TINH" * V."PHEP_TINH" AS "PHEP_TINH"
                    FROM TBL_MASTER_DETAIL B,
                        V
                    WHERE B."ID_CHI_TIEU_CHI_TIET" = V."ID_CHI_TIEU"
                )

                INSERT INTO TMP_KET_QUA (
                    SELECT
                        FR."ID_CHI_TIEU"
                        , FR."MA_CHI_TIEU"
                        , FR."TEN_CHI_TIEU"
                        , FR."TEN_TIENG_ANH"
                        , FR."SO_THU_TU"
                        , FR."THUYET_MINH"
                        , FR."LOAI_CHI_TIEU"
                        , CASE WHEN FR."LOAI_CHI_TIEU" = '1'
                        THEN FR."CONG_THUC"
                        ELSE ''
                        END                              AS "CONG_THUC"
                        , FR."KHONG_IN"
                        , FR."IN_DAM"
                        , FR."IN_NGHIENG"
                        , coalesce(X."SO_TIEN", 0)         AS "SO_CUOI_NAM"
                        , coalesce(X."SO_TIEN_DAU_NAM", 0) AS "SO_DAU_NAM"
                    FROM (SELECT
                            V."ID_CHI_TIEU"
                            , SUM(V."PHEP_TINH" * V."GHI_NO")         AS "SO_TIEN"
                            , SUM(V."PHEP_TINH" * V."GHI_NO_DAU_NAM") AS "SO_TIEN_DAU_NAM"
                        FROM V
                        GROUP BY V."ID_CHI_TIEU"
                        ) AS X
                        RIGHT JOIN (SELECT
                                        MT."CHE_DO_KE_TOAN"
                                        , MT."TEN_BAO_CAO"
                                        , DT.*
                                    FROM tien_ich_thiet_lap_bao_cao_tai_chinh MT
                                        INNER JOIN tien_ich_bao_cao_tai_chinh_chi_tiet DT ON MT.id = DT."CHI_TIET_ID") FR
                            ON FR."ID_CHI_TIEU" = X."ID_CHI_TIEU"
                    WHERE FR."CHE_DO_KE_TOAN" = cast(AccountingSystem AS VARCHAR(127))
                        AND "ReportID" = report_id)
                ;

                RETURN QUERY SELECT *
                            FROM TMP_KET_QUA
                ;

            END
            ;

            $$ LANGUAGE PLpgSQL
            ;

            -- SELECT *FROM GET_BAO_CAO_TAI_CHINH_B02_DN(16,0,'2018-01-01','2019-06-20','2016-07-14','2017-12-31')
		""")
    class BAO_CAO_B02DN_BAO_CAO_KET_QUA_HOAT_DONG_KINH_DOANH_REPORT(models.AbstractModel):
        _name = 'report.bao_cao.template_b02dn_bao_cao_kq_hoat_dong_kinh_doanh'

        @api.model
        def get_report_values(self, docids, data=None):
            env = self.env[data.get('model')]
            docs = [env.new(d) for d in env.with_context(data.get('context')).search_read()]
            
            added_data = {
                'tieu_de_nguoi_ky': self.get_danh_sach_tieu_de_nguoi_ky(data.get('model')),
                'ten_nguoi_ky': self.get_danh_sach_ten_nguoi_ky(data.get('model')),
                'sub_title': data.get('breadcrumb'),

            }
            return {
                'docs': docs,
                'added_data': added_data,
                'o': self,
            }