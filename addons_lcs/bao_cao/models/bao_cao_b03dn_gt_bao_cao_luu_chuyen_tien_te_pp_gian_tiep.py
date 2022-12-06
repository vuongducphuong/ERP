# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_B03DN_GT_BAO_CAO_LUU_CHUYEN_TIEN_TE_PP_GIAN_TIEP(models.Model):
    _name = 'b03dngt.luu.chuyen.tien.te.pp.gian.tiep'
   
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    # KY_BAO_CAO = fields.Selection([('THANG_NAY', 'Tháng này'), ('QUY_NAY', 'Quý này'), ('NAM_NAY', 'Năm nay'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='THANG_NAY',required=True)
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

    IN_DAM = fields.Boolean(string='In đậm', help='In đậm')
    IN_NGHIENG = fields.Boolean(string='In nghiêng', help='In nghiêng')
    KHONG_IN = fields.Boolean(string='Không in', help='Không in')



    ### START IMPLEMENTING CODE ###
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_B03DN_GT_BAO_CAO_LUU_CHUYEN_TIEN_TE_PP_GIAN_TIEP, self).default_get(fields_list)
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
            'CHI_NHANH_ID':CHI_NHANH_ID,
            'TU_NGAY_BAO_CAO_TRUOC' : tu_ngay_ky_truoc,
            'DEN_NGAY_BAO_CAO_TRUOC' : den_ngay_ky_truoc,
            'limit': limit,
            'offset': offset,
        }
        # Execute SQL query here

        query = """
        DO LANGUAGE plpgsql $$
            DECLARE
                ts_chi_nhanh_id                                  INTEGER := %(CHI_NHANH_ID)s;  -- chi nhánh

                ts_bao_gom_chi_nhanh_phu_thuoc                   INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;   -- bao gốm số liệu chi nhánh phụ thuộc

                ts_tu_ngay                                       DATE := %(TU_NGAY)s;  -- từ ngày

                ts_den_ngay                                      DATE := %(DEN_NGAY)s;   -- đến ngày

                ts_PrevFromDate                                  DATE := %(TU_NGAY_BAO_CAO_TRUOC)s;

                ts_PrevToDate                                    DATE := %(DEN_NGAY_BAO_CAO_TRUOC)s;

                ts_lay_so_lieu_tu_bao_cao_da_lap                 INTEGER := %(LAY_DU_LIEU_TU_BCTC_DA_LAP)s;   -- lấy số liệu từ BCTC đã lập

                ts_khong_hien_thi_cac_chi_tieu_co_so_lieu_bang_0 INTEGER := %(KHONG_HIEN_THI_CAC_CHI_TIEU_CO_SO_LIEU_BANG_KHONG)s;  -- Không hiển thị các chỉ tiêu có số liệu = 0
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

                --         SELECT  @RefID = RefID ,
                --                         @ReportCreatedDate = ReportCreatedDate ,
                --                         @ReportCreatedBy = ReportCreatedBy ,
                --                         @DirectorName = DirectorName
                --                 FROM    dbo.FrReportlist
                --                 WHERE   --FromDate = @FromDate
                --              --AND ToDate = @ToDate
                --                         DAY(FromDate) = DAY(@FromDate)
                --                         AND MONTH(FromDate) = MONTH(@FromDate)
                --                         AND YEAR(FromDate) = YEAR(@FromDate)
                --                         AND DAY(ToDate) = DAY(@ToDate)
                --                         AND MONTH(ToDate) = MONTH(@ToDate)
                --                         AND YEAR(ToDate) = YEAR(@ToDate)
                --                         AND Reftype = 4050
                --                         AND BranchID = @BranchID
                --                         AND ( AccountingSystem = @AccountingSystem
                --                               OR ( @AccountingSystem = '48'
                --                                    AND AccountingSystem = '2015'
                --                                  )
                --                             )
                --                         AND ( @IsWorkingWithManagementBook = 1
                --                               AND DisplayOnBook = 1
                --                               OR @IsWorkingWithManagementBook = 0
                --                               AND DisplayOnBook = 0
                --                             )
                --                 SELECT  ReportDetailID ,
                --                         FRReportList.RefID ,
                --                         ReportType ,
                --                         ItemID ,
                --                         ItemCode ,
                --                         ItemName ,
                --                         -- LVDiep 09/07/2016: Nếu chỉ tiêu tiếng anh để trống thì lấy chỉ tiêu tiếng việt để hiển thị trên báo cáo
                --                         --ItemNameEnglish ,
                --                         ISNULL(ItemNameEnglish, ItemName) AS ItemNameEnglish ,
                --                         ItemIndex ,
                --                         Description ,
                --                         FormulaType ,
                --                         FormulaFrontEnd ,
                --                         Amount ,
                --                         PrevAmount ,
                --                         Hidden ,
                --                         IsBold ,
                --                         IsItalic ,
                --                         SortOrder ,
                --                         Category ,
                --                         Formula ,
                --                         @ReportCreatedDate AS ReportCreatedDate ,
                --                         @ReportCreatedBy AS ReportCreatedBy ,
                --                         @DirectorName AS DirectorName ,
                --                         --ddnhan:20-09-2016 bổ sung thêm cột này để phục vụ cho CR 116742
                --                         AccountingSystem
                --                 FROM    FRReportDetail
                --                         INNER JOIN dbo.FRReportList ON FRReportDetail.RefID = FRReportList.RefID
                --                 WHERE   FRReportList.RefID = @RefID
                --                         AND ReportType = '6'
                --                         AND Hidden = 0
                --                         -- Ntquang 26/10/2017 - CR150420- bổ sung tùy chọn: Không hiển thị các chỉ tiêu có số liệu = 0
                --                         -- cho phép hiển thị các chỉ tiêu tổng hợp, không thiết lập công thức có số liệu = 0
                --                         AND ( @NonDisplayItemHasNoData = 0
                --                               OR ( @NonDisplayItemHasNoData = 1
                --                                    AND ( ( Amount <> 0
                --                                            OR PrevAmount <> 0
                --                                          )
                --                                          -- Luôn cho phép hiển thị các chỉ tiêu tổng hợp, không thiết lập công thức
                --                                          OR ( FormulaType = 1
                --                                               AND ISNULL(FormulaFrontEnd, '') = ''
                --                                             )
                --                                        )
                --                                  )
                --                             )
                --                 ORDER BY ItemIndex

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
                            , FR."SO_TIEN_NAM_TRUOC"
                        FROM GET_BAO_CAO_TAI_CHINH_B03_DN_GIAN_TIEP(ts_chi_nhanh_id, ts_bao_gom_chi_nhanh_phu_thuoc, ts_tu_ngay,
                                                                    ts_den_ngay, ts_PrevFromDate, ts_PrevToDate) FR
                        WHERE FR."KHONG_IN" = FALSE
                            -- cho phép hiển thị các chỉ tiêu tổng hợp, không thiết lập công thức có số liệu = 0
                            AND (ts_khong_hien_thi_cac_chi_tieu_co_so_lieu_bang_0 = 0
                                OR (ts_khong_hien_thi_cac_chi_tieu_co_so_lieu_bang_0 = 1
                                    AND ((FR."SO_TIEN" <> 0
                                            OR FR."SO_TIEN_NAM_TRUOC" <> 0
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
                "SO_TIEN_NAM_TRUOC" as "KY_TRUOC",
                "SO_TIEN" as "KY_NAY",
                "IN_DAM" as "IN_DAM",
                "IN_NGHIENG" as "IN_NGHIENG",
                "KHONG_IN" as "KHONG_IN"
                
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
        action = self.env.ref('bao_cao.open_report_b03dn_gt_bao_cao_luu_chuyen_tien_te_pp_gian_tiep').read()[0]
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action


    @api.model_cr
    def init(self):
        self.env.cr.execute(""" 
			DROP FUNCTION if EXISTS GET_BAO_CAO_TAI_CHINH_B03_DN_GIAN_TIEP(IN ts_chi_nhanh_id INTEGER,ts_IncludeDependentBranch INTEGER,ts_tu_ngay DATE,ts_den_ngay DATE,ts_PrevFromDate DATE,ts_PrevToDate DATE);
            CREATE OR REPLACE FUNCTION GET_BAO_CAO_TAI_CHINH_B03_DN_GIAN_TIEP(IN ts_chi_nhanh_id INTEGER,ts_bao_gom_chi_nhanh_phu_thuoc INTEGER,ts_tu_ngay DATE,ts_den_ngay DATE,ts_PrevFromDate DATE,ts_PrevToDate DATE)
            RETURNS TABLE("ID_CHI_TIEU" VARCHAR(500),
                        "MA_CHI_TIEU" VARCHAR(500),
                        "TEN_CHI_TIEU" VARCHAR(500),
                        "TEN_TIENG_ANH" VARCHAR(500),
                        "SO_THU_TU" INTEGER,
                        "THUYET_MINH" VARCHAR(500),
                        "LOAI_CHI_TIEU" VARCHAR(500),
                        "CONG_THUC" VARCHAR(500),
                        "KHONG_IN" BOOLEAN,
                        "IN_DAM" BOOLEAN,
                        "IN_NGHIENG" BOOLEAN,
                        "SO_TIEN" FLOAT,
                        "SO_TIEN_NAM_TRUOC" FLOAT
            ) AS $$
            DECLARE

            --   ts_chi_nhanh_id INTEGER:= 81;
            --   ts_IncludeDependentBranch INTEGER:= 1;
            --   ts_tu_ngay DATE := '2019-01-01';
            --   ts_den_ngay DATE := '2019-12-31';
            --   ts_PrevFromDate DATE := '2018-01-01';
            --   ts_PrevToDate DATE := '2018-12-31';

                AccountingSystem     INTEGER;

                ten_bao_cao          VARCHAR(500) :='BAO_CAO_LUU_CHUYEN_TIEN_TE_GIAN_TIEP';

                report_id INTEGER:=6;

                ma_chi_tieu          VARCHAR(500);

                ngay_bat_dau         DATE;

                ngay_dau_ky          DATE;

                id_chi_tieu          VARCHAR(500);

                B02ProfitBeforeTaxID VARCHAR(500);

                ItemProfitBeforeTax  VARCHAR(500);

            BEGIN

            DROP TABLE IF EXISTS B03_TMP_KET_QUA;
            CREATE TEMP TABLE B03_TMP_KET_QUA(
                "ID_CHI_TIEU" VARCHAR(500),
                "MA_CHI_TIEU" VARCHAR(500),
                "TEN_CHI_TIEU" VARCHAR(500),
                "TEN_TIENG_ANH" VARCHAR(500),
                "SO_THU_TU" INTEGER,
                "THUYET_MINH" VARCHAR(500),
                "LOAI_CHI_TIEU" VARCHAR(500),
                "CONG_THUC" VARCHAR(500),
                "KHONG_IN" BOOLEAN,
                "IN_DAM" BOOLEAN,
                "IN_NGHIENG" BOOLEAN,
                "SO_TIEN" FLOAT,
                "SO_TIEN_NAM_TRUOC" FLOAT
            );

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
                        SELECT
                            id           AS "CHI_NHANH_ID"
                            , "MA_DON_VI"  AS "MA_CHI_NHANH"
                            , "TEN_DON_VI" AS "TEN_CHI_NHANH"
                        FROM danh_muc_to_chuc
                        WHERE id = ts_chi_nhanh_id
                            OR (ts_bao_gom_chi_nhanh_phu_thuoc = 1 AND "HACH_TOAN_SELECTION" = 'PHU_THUOC' AND "CAP_TO_CHUC" = '2'
                                AND parent_id = ts_chi_nhanh_id)
                            OR (ts_chi_nhanh_id ISNULL AND "CAP_TO_CHUC" IN ('1', '2'))
                ;

                SELECT value
                INTO ngay_bat_dau
                FROM ir_config_parameter
                WHERE key = 'he_thong.TU_NGAY_BAT_DAU_TAI_CHINH'
                ;

                SELECT DT."ID_CHI_TIEU"
                INTO id_chi_tieu
                FROM tien_ich_bao_cao_tai_chinh_chi_tiet DT
                    INNER JOIN tien_ich_thiet_lap_bao_cao_tai_chinh MT ON MT.id = DT."CHI_TIET_ID"
                WHERE DT."MA_CHI_TIEU" = '01'
                    AND MT."TEN_BAO_CAO" = 'BAO_CAO_LUU_CHUYEN_TIEN_TE_GIAN_TIEP'
                    AND "CHE_DO_KE_TOAN" = cast(AccountingSystem AS VARCHAR(500))
                ;


                DROP TABLE IF EXISTS TBL_ITEM
                ;

                CREATE TEMP TABLE TBL_ITEM
                    AS
                        SELECT
                            DT."ID_CHI_TIEU"
                            , DT."MA_CHI_TIEU"
                            , DT."TEN_CHI_TIEU"
                            , DT."SO_THU_TU"
                            , CASE WHEN CT."PHEP_TINH" = 'CONG'
                            THEN 1
                            ELSE -1 END    AS "PHEP_TINH"
                            , CT."KY_HIEU"
                            , CT."TAI_KHOAN" AS "MA_TAI_KHOAN"
                            , CASE WHEN CT."TAI_KHOAN" <> ''
                            THEN concat(CT."TAI_KHOAN", '%')
                            ELSE '' END    AS "MA_TAI_KHOAN_PT"
                            , CASE WHEN CT."TK_DOI_UNG" <> ''
                            THEN concat(CT."TK_DOI_UNG", '%')
                            ELSE '' END    AS "MA_TAI_KHOAN_DOI_UNG_PT"
                            , CASE WHEN CT."KY_HIEU" LIKE '%ChiTietTheoTKvaDT' OR CT."KY_HIEU" LIKE '%_TKvaDT'
                            THEN 1
                            ELSE CASE WHEN CT."KY_HIEU" LIKE '%ChitietTheoTK' OR CT."KY_HIEU" LIKE '%_TK'
                                THEN 2
                                ELSE 0 END
                            END            AS "LOAI_CHI_TIET_THEO_DOI_TUONG"
                            , NULL           AS "TINH_CHAT"
                            , CASE WHEN CT."KY_HIEU" NOT LIKE '%ChiTietTheoHD%'
                            THEN -1
                            ELSE CASE WHEN CT."KY_HIEU" LIKE '%ChiTietTheoHD_SXKD%'
                                THEN 0
                                WHEN CT."KY_HIEU" LIKE '%ChiTietTheoHD_DAUTU%'
                                    THEN 1
                                ELSE 2 END
                            END            AS "HOAT_DONG"
                        FROM tien_ich_thiet_lap_bao_cao_tai_chinh MT
                            INNER JOIN tien_ich_bao_cao_tai_chinh_chi_tiet DT ON MT.id = DT."CHI_TIET_ID"
                            LEFT JOIN tien_ich_xay_dung_cong_thuc_loai_chi_tieu_chi_tiet CT ON DT.id = CT."CHI_TIET_ID"
                        WHERE MT."CHE_DO_KE_TOAN" = cast(AccountingSystem AS VARCHAR(500))
                            AND DT."ReportID" = report_id
                            AND DT."LOAI_CHI_TIEU" = '0'
                            AND DT."CONG_THUC" NOTNULL
                            AND DT."ID_CHI_TIEU" <> id_chi_tieu
                            AND CT."KY_HIEU" NOT IN (
                            'PhatsinhDU_ChiTietThanhlyTSCD_BDSDT',
                            'PhatsinhDU_ChiTietChiPhiLaiVayChiTraLaiVay',
                            'PhatsinhDU_ChitietTienChitraLaivay',
                            'PhatsinhNO_ChiTietThanhlyTSCD_BDSDT',
                            'PhatsinhNO_ChiTietDGLaiTSGVDT',
                            'PhatsinhNO_ChiTietBanThuHoiDTTC',
                            'PhatsinhNO_ChiTietChiPhiLaiVayChiTraLaiVay',
                            'PhatsinhCO_ChiTietThanhlyTSCD_BDSDT',
                            'PhatsinhCO_ChiTietDGLaiTSGVDT',
                            'PhatsinhCO_ChiTietBanThuHoiDTTC',
                            'PhatsinhCO_ChiTietLai')
                ;

                -- Thêm accountkind cho
                UPDATE TBL_ITEM
                SET "TINH_CHAT" = A."TINH_CHAT"
                FROM danh_muc_he_thong_tai_khoan A
                WHERE A."SO_TAI_KHOAN" = TBL_ITEM."MA_TAI_KHOAN"
                ;

                DROP TABLE IF EXISTS TBL_ACCOUNT_BALANCE
                ;

                CREATE TEMP TABLE TBL_ACCOUNT_BALANCE
                    AS
                        SELECT
                            A."SO_TAI_KHOAN" AS "MA_TAI_KHOAN"
                            , A."TINH_CHAT"
                            , B."LOAI_CHI_TIET_THEO_DOI_TUONG"
                            , B."HOAT_DONG"
                            , B."MA_TAI_KHOAN" AS "MA_TAI_KHOAN_ITEM"
                        FROM danh_muc_he_thong_tai_khoan A
                            INNER JOIN TBL_ITEM B ON A."SO_TAI_KHOAN" LIKE B."MA_TAI_KHOAN_PT"
                                                    AND b."KY_HIEU" LIKE 'DU%'
                        GROUP BY A."SO_TAI_KHOAN",
                            A."TINH_CHAT",
                            B."LOAI_CHI_TIET_THEO_DOI_TUONG",
                            B."HOAT_DONG",
                            B."MA_TAI_KHOAN"
                ;

                DROP TABLE IF EXISTS TBL_BALANCE_ALL
                ;

                CREATE TEMP TABLE TBL_BALANCE_ALL
                    AS
                        SELECT
                            CASE WHEN A."LOAI_CHI_TIET_THEO_DOI_TUONG" = 0
                                THEN A."MA_TAI_KHOAN_ITEM"
                            ELSE GL."MA_TAI_KHOAN"
                            END AS   "MA_TAI_KHOAN"
                            , CASE WHEN A."LOAI_CHI_TIET_THEO_DOI_TUONG" = 0
                                        AND A."MA_TAI_KHOAN_ITEM" <> '11'
                            THEN A."TINH_CHAT"
                            ELSE A."TINH_CHAT"
                            END AS   "TINH_CHAT"
                            , CASE WHEN A."LOAI_CHI_TIET_THEO_DOI_TUONG" = 1
                            THEN GL."DOI_TUONG_ID"
                            ELSE NULL
                            END AS   "DOI_TUONG_ID"
                            , A."LOAI_CHI_TIET_THEO_DOI_TUONG"
                            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < ts_PrevFromDate
                            THEN GL."GHI_NO" - GL."GHI_CO"
                                ELSE 0
                                END) "GHI_NO_DAU_KY_DAU_NAM"
                            , cast(0 AS FLOAT)   AS   "GHI_CO_DAU_KY_DAU_NAM"
                            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < ts_tu_ngay
                            THEN GL."GHI_NO" - GL."GHI_CO"
                                ELSE 0
                                END) "GHI_NO_DAU_KY"
                            , cast(0 AS FLOAT)   AS   "GHI_CO_DAU_KY"
                            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" <= ts_den_ngay
                            THEN GL."GHI_NO" - "GHI_CO"
                                ELSE 0
                                END) "GHI_NO_TON"
                            , cast(0 AS FLOAT)   AS   "GHI_CO_TON"
                            -- nếu TK chi tiết theo tài khoản và không bù trừ nợ có giữa các chi nhánh thì lấy lên branchID
                            , CASE WHEN A."LOAI_CHI_TIET_THEO_DOI_TUONG" = 1
                            THEN GL."CHI_NHANH_ID"
                            ELSE NULL
                            END AS   "CHI_NHANH_ID"
                            , CASE A."HOAT_DONG"
                            WHEN -1
                                THEN '-1'
                            --nvtoan modify 30/09/2016: Nếu không có dữ liệu trong bảng AC mới lấy giá trị mặc định, còn lại phải lấy theo AC
                            WHEN 0
                                THEN CASE WHEN AC."CHI_TIET_ID" IS NULL
                                    THEN '0'
                                    ELSE Ac."HOAT_DONG"
                                    END
                            ELSE AC."HOAT_DONG"
                            END AS   "HOAT_DONG"
                        FROM so_cai_chi_tiet GL
                            INNER JOIN TBL_ACCOUNT_BALANCE A ON GL."MA_TAI_KHOAN" = A."MA_TAI_KHOAN"
                            INNER JOIN danh_muc_he_thong_tai_khoan ACC ON A."MA_TAI_KHOAN" = Acc."SO_TAI_KHOAN"
                            INNER JOIN TBL_BRANCH B ON GL."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                            LEFT JOIN tong_hop_bctc_chon_lai_hoat_dong_lctt_chi_tiet_form AC
                                ON GL."CHI_TIET_ID" = Ac."CHI_TIET_ID" AND GL."CHI_TIET_MODEL" = AC."CHI_TIET_MODEL"
                            LEFT JOIN tong_hop_bctc_chon_nv_va_hd_lctt_chi_tiet_theo_dt_form OPN
                                ON GL."NGAY_HACH_TOAN" < ngay_bat_dau--GL."SO_CHUNG_TU" = 'OPN'
                                AND ACC.id = OPN."TAI_KHOAN_ID"
                                AND GL."CHI_NHANH_ID" = OPN."CHI_NHANH_ID"
                                AND (ACC."CHI_TIET_THEO_DOI_TUONG" = FALSE
                                        OR A."LOAI_CHI_TIET_THEO_DOI_TUONG" IN (0, 2)
                                )
                        WHERE GL."NGAY_HACH_TOAN" <= ts_den_ngay
                            AND OPN."TAI_KHOAN_ID" IS NULL
                        GROUP BY
                            CASE WHEN A."LOAI_CHI_TIET_THEO_DOI_TUONG" = 0
                                THEN A."MA_TAI_KHOAN_ITEM"
                            ELSE GL."MA_TAI_KHOAN"
                            END,
                            CASE WHEN A."LOAI_CHI_TIET_THEO_DOI_TUONG" = 0
                                    AND A."MA_TAI_KHOAN_ITEM" <> '11'
                                THEN A."TINH_CHAT"
                            ELSE A."TINH_CHAT"
                            END,
                            CASE WHEN A."LOAI_CHI_TIET_THEO_DOI_TUONG" = 1
                                THEN GL."DOI_TUONG_ID"
                            ELSE NULL
                            END,
                            A."LOAI_CHI_TIET_THEO_DOI_TUONG"
                            -- nếu TK chi tiết theo tài khoản và không bù trừ nợ có giữa các chi nhánh thì lấy lên branchID
                            ,
                            CASE WHEN A."LOAI_CHI_TIET_THEO_DOI_TUONG" = 1
                                THEN GL."CHI_NHANH_ID"
                            ELSE NULL
                            END,
                            CASE A."HOAT_DONG"
                            WHEN -1
                                THEN '-1'
                            --nvtoan modify 30/09/2016: Nếu không có dữ liệu trong bảng AC mới lấy giá trị mặc định, còn lại phải lấy theo AC
                            WHEN 0
                                THEN CASE WHEN AC."CHI_TIET_ID" IS NULL
                                    THEN '0'
                                    ELSE Ac."HOAT_DONG"
                                    END
                            ELSE AC."HOAT_DONG"
                            END
                ;

                SELECT (cast(ngay_bat_dau AS DATE) - INTERVAL '1 day')
                INTO ngay_dau_ky
                ;

                DROP TABLE IF EXISTS TBL_ACTIVITY
                ;

                CREATE TEMP TABLE TBL_ACTIVITY
                    AS
                        SELECT -1 AS "HOAT_DONG"
                        UNION ALL
                        SELECT 0 AS "HOAT_DONG"
                        UNION ALL
                        SELECT 1 AS "HOAT_DONG"
                        UNION ALL
                        SELECT 2 AS "HOAT_DONG"
                ;

                INSERT INTO TBL_BALANCE_ALL (
                    SELECT
                        AC."SO_TAI_KHOAN"
                        , A."TINH_CHAT"
                        , NULL                    AS "DOI_TUONG_ID"
                        , A."LOAI_CHI_TIET_THEO_DOI_TUONG"
                        , cast(SUM(CASE WHEN ts_PrevFromDate > ngay_dau_ky
                        THEN CASE WHEN OPN."LA_SO_DU_NO" = TRUE
                            THEN CASE T."HOAT_DONG"
                                WHEN 0
                                    THEN cast(OPN."SO_TIEN_KINH_DOANH" AS FLOAT)
                                WHEN 1
                                    THEN cast(OPN."SO_TIEN_DAU_TU" AS FLOAT)
                                WHEN 2
                                    THEN cast(OPN."SO_TIEN_TAI_CHINH" AS FLOAT)
                                END
                            ELSE 0
                            END
                                ELSE 0
                                END) AS FLOAT) AS "GHI_CO_DAU_KY_DAU_NAM"
                        , cast(SUM(CASE WHEN ts_PrevFromDate > ngay_dau_ky
                        THEN CASE WHEN OPN."LA_SO_DU_NO" = FALSE
                            THEN CASE T."HOAT_DONG"
                                WHEN 0
                                    THEN cast(OPN."SO_TIEN_KINH_DOANH" AS FLOAT)
                                WHEN 1
                                    THEN cast(OPN."SO_TIEN_DAU_TU" AS FLOAT)
                                WHEN 2
                                    THEN cast(OPN."SO_TIEN_TAI_CHINH" AS FLOAT)
                                END
                            ELSE 0
                            END
                                ELSE 0
                                END) AS FLOAT) AS "GHI_CO_DAU_KY_DAU_NAM"
                        , cast(SUM(CASE WHEN ts_tu_ngay > ngay_dau_ky
                        THEN CASE WHEN OPN."LA_SO_DU_NO" = TRUE
                            THEN CASE T."HOAT_DONG"
                                WHEN 0
                                    THEN cast(OPN."SO_TIEN_KINH_DOANH" AS FLOAT)
                                WHEN 1
                                    THEN cast(OPN."SO_TIEN_DAU_TU" AS FLOAT)
                                WHEN 2
                                    THEN cast(OPN."SO_TIEN_TAI_CHINH" AS FLOAT)
                                END
                            ELSE 0
                            END
                                ELSE 0
                                END) AS FLOAT) AS "GHI_NO_DAU_KY"
                        , cast(SUM(CASE WHEN ts_tu_ngay > ngay_dau_ky
                        THEN CASE WHEN OPN."LA_SO_DU_NO" = FALSE
                            THEN CASE T."HOAT_DONG"
                                WHEN 0
                                    THEN cast(OPN."SO_TIEN_KINH_DOANH" AS FLOAT)
                                WHEN 1
                                    THEN cast(OPN."SO_TIEN_DAU_TU" AS FLOAT)
                                WHEN 2
                                    THEN cast(OPN."SO_TIEN_TAI_CHINH" AS FLOAT)
                                END
                            ELSE 0
                            END
                                ELSE 0
                                END) AS FLOAT) AS "GHI_CO_DAU_KY"
                        , cast(SUM(CASE WHEN ts_den_ngay >= ngay_dau_ky
                        THEN CASE WHEN OPN."LA_SO_DU_NO" = TRUE
                            THEN CASE T."HOAT_DONG"
                                WHEN 0
                                    THEN cast(OPN."SO_TIEN_KINH_DOANH" AS FLOAT)
                                WHEN 1
                                    THEN cast(OPN."SO_TIEN_DAU_TU" AS FLOAT)
                                WHEN 2
                                    THEN cast(OPN."SO_TIEN_TAI_CHINH" AS FLOAT)
                                END
                            ELSE 0
                            END
                                ELSE 0
                                END) AS FLOAT) AS "GHI_NO_TON"
                        , cast(SUM(CASE WHEN ts_den_ngay >= ngay_dau_ky
                        THEN CASE WHEN OPN."LA_SO_DU_NO" = FALSE
                            THEN CASE T."HOAT_DONG"
                                WHEN 0
                                    THEN cast(OPN."SO_TIEN_KINH_DOANH" AS FLOAT)
                                WHEN 1
                                    THEN cast(OPN."SO_TIEN_DAU_TU" AS FLOAT)
                                WHEN 2
                                    THEN cast(OPN."SO_TIEN_TAI_CHINH" AS FLOAT)
                                END
                            ELSE 0
                            END
                                ELSE 0
                                END) AS FLOAT) AS "GHI_CO_TON"
                        -- nếu TK chi tiết theo tài khoản và không bù trừ nợ có giữa các chi nhánh thì lấy lên branchID
                        , NULL                    AS "CHI_NHANH_ID"
                        , T."HOAT_DONG"           AS "HOAT_DONG" -- Hoạt động kinh doanh
                    FROM tong_hop_bctc_chon_nv_va_hd_lctt_chi_tiet_theo_dt_form OPN
                        INNER JOIN danh_muc_he_thong_tai_khoan AC ON OPN."TAI_KHOAN_ID" = AC.id
                        INNER JOIN TBL_ACCOUNT_BALANCE A ON AC."SO_TAI_KHOAN" = A."MA_TAI_KHOAN"
                        INNER JOIN TBL_BRANCH B ON OPN."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                        , TBL_ACTIVITY T
                    WHERE (AC."CHI_TIET_THEO_DOI_TUONG" = FALSE
                        OR A."LOAI_CHI_TIET_THEO_DOI_TUONG" IN (0, 2)
                    )
                    GROUP BY AC."SO_TAI_KHOAN",
                        A."TINH_CHAT",
                        A."LOAI_CHI_TIET_THEO_DOI_TUONG",
                        T."HOAT_DONG"
                )
                ;


                DROP TABLE IF EXISTS TBL_BALANCE
                ;

                CREATE TEMP TABLE TBL_BALANCE
                    AS
                        SELECT
                            "MA_TAI_KHOAN"
                            , "TINH_CHAT"
                            , "DOI_TUONG_ID"
                            , "LOAI_CHI_TIET_THEO_DOI_TUONG"
                            , SUM("GHI_NO_DAU_KY_DAU_NAM" - "GHI_CO_DAU_KY_DAU_NAM") AS "GHI_NO_DAU_KY_DAU_NAM"
                            , cast(0 AS FLOAT)                                                      AS "GHI_CO_DAU_KY_DAU_NAM"
                            , SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY")                 AS "GHI_NO_DAU_KY"
                            , cast(0 AS FLOAT)                                                      AS "GHI_CO_DAU_KY"
                            , SUM("GHI_NO_TON" - "GHI_CO_TON")                       AS "GHI_NO_TON"
                            , cast(0 AS FLOAT)                                                      AS "GHI_CO_TON"
                            , "CHI_NHANH_ID"
                            , "HOAT_DONG"
                        FROM TBL_BALANCE_ALL B
                        GROUP BY "MA_TAI_KHOAN",
                            "TINH_CHAT",
                            "DOI_TUONG_ID",
                            "LOAI_CHI_TIET_THEO_DOI_TUONG",
                            "CHI_NHANH_ID",
                            "HOAT_DONG"
                        HAVING SUM("GHI_NO_DAU_KY_DAU_NAM" - "GHI_CO_DAU_KY_DAU_NAM") <> 0
                            OR SUM("GHI_NO_DAU_KY" - "GHI_CO_DAU_KY") <> 0
                            OR SUM("GHI_NO_TON" - "GHI_CO_TON") <> 0
                ;


                UPDATE TBL_BALANCE
                SET "GHI_CO_DAU_KY_DAU_NAM" = -"GHI_NO_DAU_KY_DAU_NAM",
                    "GHI_NO_DAU_KY_DAU_NAM" = 0
                WHERE "TINH_CHAT" = '1'
                    OR ("TINH_CHAT" NOT IN ('0', '1')
                        AND "GHI_NO_DAU_KY_DAU_NAM" < 0
                    )
                ;

                UPDATE TBL_BALANCE
                SET "GHI_CO_DAU_KY" = -"GHI_NO_DAU_KY",
                    "GHI_NO_DAU_KY" = 0
                WHERE "TINH_CHAT" = '1'
                    OR ("TINH_CHAT" NOT IN ('0', '1')
                        AND "GHI_NO_DAU_KY" < 0
                    )
                ;

                UPDATE TBL_BALANCE
                SET "GHI_CO_TON" = -"GHI_NO_TON",
                    "GHI_NO_TON" = 0
                WHERE "TINH_CHAT" = '1'
                    OR ("TINH_CHAT" NOT IN ('0', '1')
                        AND "GHI_NO_TON" < 0
                    )
                ;

                DROP TABLE IF EXISTS TBL_DEBIT_ACCOUNT
                ;

                CREATE TEMP TABLE TBL_DEBIT_ACCOUNT
                    AS
                        SELECT
                            DISTINCT A."SO_TAI_KHOAN" AS "MA_TAI_KHOAN"
                        FROM danh_muc_he_thong_tai_khoan A
                            INNER JOIN TBL_ITEM B ON A."SO_TAI_KHOAN" LIKE B."MA_TAI_KHOAN_PT"
                                                    AND (b."KY_HIEU" LIKE 'PhatsinhNO%'
                                                        OR b."KY_HIEU" LIKE 'PhatsinhDU%'
                                                    )
                ;

                DROP TABLE IF EXISTS TBL_DEBIT_BALANCE
                ;

                CREATE TEMP TABLE TBL_DEBIT_BALANCE (
                    "MA_TAI_KHOAN"         VARCHAR(500),
                    "MA_TAI_KHOAN_DOI_UNG" VARCHAR(500),
                    "SO_TIEN_DAU_NAM"      FLOAT,
                    "SO_TIEN"              FLOAT,
                    "HOAT_DONG"            VARCHAR(500)
                )
                ;

                INSERT INTO TBL_DEBIT_BALANCE (
                    SELECT
                        GL."MA_TAI_KHOAN"
                        , GL."MA_TAI_KHOAN_DOI_UNG"
                        , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ts_PrevFromDate AND ts_PrevToDate
                        THEN GL."GHI_NO"
                            ELSE 0
                            END)
                        , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ts_tu_ngay AND ts_den_ngay
                        THEN GL."GHI_NO"
                            ELSE 0
                            END)
                        ,
                        --nvtoan modify 01/10/2016: Nếu không có dữ liệu trong bảng AC mới lấy giá trị mặc định, còn lại phải lấy theo AC
                        CASE WHEN AC."CHI_TIET_ID" IS NULL
                            THEN '0'
                        ELSE Ac."HOAT_DONG"
                        END AS "HOAT_DONG"
                    --ISNULL(Ac."HOAT_DONG", -1)
                    FROM so_cai_chi_tiet AS GL
                        INNER JOIN TBL_BRANCH B ON GL."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                        INNER JOIN TBL_DEBIT_ACCOUNT I ON (GL."MA_TAI_KHOAN" = I."MA_TAI_KHOAN")
                        LEFT JOIN tong_hop_bctc_chon_lai_hoat_dong_lctt_chi_tiet_form AC
                            ON GL."CHI_TIET_ID" = Ac."CHI_TIET_ID" AND GL."CHI_TIET_MODEL" = AC."CHI_TIET_MODEL"
                    WHERE GL."NGAY_HACH_TOAN" < ts_den_ngay
                    GROUP BY GL."MA_TAI_KHOAN",
                        GL."MA_TAI_KHOAN_DOI_UNG",
                        CASE WHEN AC."CHI_TIET_ID" IS NULL
                            THEN '0'
                        ELSE Ac."HOAT_DONG"
                        END
                )
                ;

                DROP TABLE IF EXISTS TBL_CREDIT_ACCOUNT
                ;

                CREATE TEMP TABLE TBL_CREDIT_ACCOUNT
                    AS
                        SELECT DISTINCT A."SO_TAI_KHOAN" AS "MA_TAI_KHOAN"
                        FROM danh_muc_he_thong_tai_khoan A
                            INNER JOIN TBL_ITEM B ON A."SO_TAI_KHOAN" LIKE B."MA_TAI_KHOAN_PT"
                                                    AND (b."KY_HIEU" LIKE 'PhatsinhCO%')
                ;

                DROP TABLE IF EXISTS TBL_CREDIT_BALANCE
                ;

                CREATE TEMP TABLE TBL_CREDIT_BALANCE (
                    "MA_TAI_KHOAN"    VARCHAR(500),
                    "SO_TIEN_DAU_NAM" FLOAT,
                    "SO_TIEN"         FLOAT,
                    "HOAT_DONG"       VARCHAR(500)
                )
                ;

                INSERT INTO TBL_CREDIT_BALANCE (
                    SELECT
                        GL."MA_TAI_KHOAN"
                        , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ts_PrevFromDate AND ts_PrevToDate
                        THEN "GHI_CO"
                            ELSE 0
                            END)
                        , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ts_tu_ngay AND ts_den_ngay
                        THEN "GHI_CO"
                            ELSE 0
                            END)
                        , CASE WHEN AC."CHI_TIET_ID" IS NULL
                        THEN '0'
                        ELSE Ac."HOAT_DONG"
                        END AS "HOAT_DONG"

                    --ISNULL(Ac."HOAT_DONG", -1)
                    FROM so_cai_chi_tiet AS GL
                        INNER JOIN TBL_BRANCH B ON GL."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                        INNER JOIN TBL_CREDIT_ACCOUNT I ON (GL."MA_TAI_KHOAN" = I."MA_TAI_KHOAN")
                        LEFT JOIN tong_hop_bctc_chon_lai_hoat_dong_lctt_chi_tiet_form AC
                            ON GL."CHI_TIET_ID" = Ac."CHI_TIET_ID" AND GL."CHI_TIET_MODEL" = AC."CHI_TIET_MODEL"
                    WHERE GL."NGAY_HACH_TOAN" < ts_den_ngay
                    GROUP BY GL."MA_TAI_KHOAN",
                        CASE WHEN AC."CHI_TIET_ID" IS NULL
                            THEN '0'
                        ELSE Ac."HOAT_DONG"
                        END
                )
                ;

                DROP TABLE IF EXISTS TBL_ITEM_BUSSINES
                ;

                CREATE TEMP TABLE TBL_ITEM_BUSSINES
                    AS
                        SELECT
                            DT."ID_CHI_TIEU"
                            , DT."MA_CHI_TIEU"
                            , DT."SO_THU_TU"
                            , DT."TEN_CHI_TIEU"
                            , CASE WHEN CT."PHEP_TINH" = 'CONG'
                            THEN 1
                            ELSE -1 END    AS "PHEP_TINH"
                            , CT."KY_HIEU"
                            , CT."TAI_KHOAN" AS "MA_TAI_KHOAN"
                            , CASE WHEN CT."TAI_KHOAN" <> ''
                            THEN concat(CT."TAI_KHOAN", '%')
                            ELSE '' END    AS "MA_TAI_KHOAN_PT"
                            , CASE WHEN CT."TK_DOI_UNG" <> ''
                            THEN concat(CT."TK_DOI_UNG", '%')
                            ELSE '' END    AS "MA_TAI_KHOAN_DOI_UNG_PT"
                            , CASE WHEN CT."KY_HIEU" LIKE '%ChiTietTheoTKvaDT' OR CT."KY_HIEU" LIKE '%_TKvaDT'
                            THEN 1
                            ELSE CASE WHEN CT."KY_HIEU" LIKE '%ChitietTheoTK' OR CT."KY_HIEU" LIKE '%_TK'
                                THEN 2 END
                            END            AS "LOAI_CHI_TIET_THEO_DOI_TUONG"
                            , NULL           AS "TINH_CHAT"

                        FROM tien_ich_thiet_lap_bao_cao_tai_chinh MT
                            INNER JOIN tien_ich_bao_cao_tai_chinh_chi_tiet DT ON MT.id = DT."CHI_TIET_ID"
                            LEFT JOIN tien_ich_xay_dung_cong_thuc_loai_chi_tieu_chi_tiet CT ON DT.id = CT."CHI_TIET_ID"
                        WHERE MT."CHE_DO_KE_TOAN" = cast(AccountingSystem AS VARCHAR(200))
                            AND "ReportID" = report_id
                            AND DT."LOAI_CHI_TIEU" = '0'
                            AND DT."CONG_THUC" NOTNULL
                            --   AND DT."ID_CHI_TIEU" = id_chi_tieu
                            AND CT."KY_HIEU" IN (
                            'PhatsinhDU_ChiTietThanhlyTSCD_BDSDT',
                            'PhatsinhDU_ChiTietChiPhiLaiVayChiTraLaiVay',
                            'PhatsinhDU_ChitietTienChitraLaivay',
                            'PhatsinhNO_ChiTietThanhlyTSCD_BDSDT',
                            'PhatsinhNO_ChiTietDGLaiTSGVDT',
                            'PhatsinhNO_ChiTietBanThuHoiDTTC',
                            'PhatsinhNO_ChiTietChiPhiLaiVayChiTraLaiVay',
                            'PhatsinhCO_ChiTietThanhlyTSCD_BDSDT',
                            'PhatsinhCO_ChiTietDGLaiTSGVDT',
                            'PhatsinhCO_ChiTietBanThuHoiDTTC',
                            'PhatsinhCO_ChiTietLai')
                ;

                UPDATE TBL_ITEM_BUSSINES
                SET "TINH_CHAT" = A."TINH_CHAT"
                FROM danh_muc_he_thong_tai_khoan A
                WHERE A."SO_TAI_KHOAN" = TBL_ITEM_BUSSINES."MA_TAI_KHOAN"
                ;

                DROP TABLE IF EXISTS TBL_DEBIT_ACCOUNT_BUSSINESS
                ;

                CREATE TEMP TABLE TBL_DEBIT_ACCOUNT_BUSSINESS
                    AS
                        SELECT
                            DISTINCT A."SO_TAI_KHOAN" AS "MA_TAI_KHOAN"
                        FROM danh_muc_he_thong_tai_khoan A
                            INNER JOIN TBL_ITEM_BUSSINES B ON A."SO_TAI_KHOAN" LIKE B."MA_TAI_KHOAN_PT"
                                                            AND (b."KY_HIEU" LIKE 'PhatsinhNO%'
                                                                OR b."KY_HIEU" LIKE 'PhatsinhDU%'
                                                            )
                ;

                DROP TABLE IF EXISTS TBL_DEBIT_BALANCR_BUSSINESS
                ;

                CREATE TEMP TABLE TBL_DEBIT_BALANCR_BUSSINESS
                    AS
                        SELECT
                            GL."MA_TAI_KHOAN"
                            , GL."MA_TAI_KHOAN_DOI_UNG"
                            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ts_PrevFromDate AND ts_PrevToDate
                            THEN GL."GHI_NO"
                                ELSE 0
                                END) AS "SO_TIEN_DAU_NAM"
                            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ts_tu_ngay AND ts_den_ngay
                            THEN GL."GHI_NO"
                                ELSE 0
                                END) AS "SO_TIEN"
                            , "NGHIEP_VU"
                        FROM so_cai_chi_tiet AS GL
                            INNER JOIN TBL_BRANCH B ON GL."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                            INNER JOIN TBL_DEBIT_ACCOUNT_BUSSINESS I ON (GL."MA_TAI_KHOAN" = I."MA_TAI_KHOAN")
                            INNER JOIN tong_hop_bctc_nghiep_vu_cho_ct_chi_tiet_form AB
                                ON GL."CHI_TIET_ID" = AB."CHI_TIET_ID" AND GL."CHI_TIET_MODEL" = AB."CHI_TIET_MODEL"
                        WHERE GL."NGAY_HACH_TOAN" < ts_den_ngay
                        GROUP BY GL."MA_TAI_KHOAN",
                            GL."MA_TAI_KHOAN_DOI_UNG",
                            "NGHIEP_VU"
                ;

                DROP TABLE IF EXISTS TBL_CREDIT_ACCOUNT_BUSSINESS
                ;

                CREATE TEMP TABLE TBL_CREDIT_ACCOUNT_BUSSINESS
                    AS
                        SELECT
                            DISTINCT A."SO_TAI_KHOAN" AS "MA_TAI_KHOAN"
                        FROM danh_muc_he_thong_tai_khoan A
                            INNER JOIN TBL_ITEM_BUSSINES B ON A."SO_TAI_KHOAN" LIKE B."MA_TAI_KHOAN_PT"
                                                            AND (b."KY_HIEU" LIKE 'PhatsinhCO%')
                ;


                DROP TABLE IF EXISTS TBL_CREDIT_BALANCE_BUSSINESS
                ;

                CREATE TEMP TABLE TBL_CREDIT_BALANCE_BUSSINESS
                    AS
                        SELECT
                            GL."MA_TAI_KHOAN"
                            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ts_PrevFromDate AND ts_PrevToDate
                            THEN "GHI_CO"
                                ELSE 0
                                END) AS "SO_TIEN_DAU_NAM"
                            , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ts_tu_ngay AND ts_den_ngay
                            THEN "GHI_CO"
                                ELSE 0
                                END) AS "SO_TIEN"
                            , "NGHIEP_VU"
                        FROM so_cai_chi_tiet AS GL
                            INNER JOIN TBL_BRANCH B ON GL."CHI_NHANH_ID" = B."CHI_NHANH_ID"
                            INNER JOIN TBL_CREDIT_ACCOUNT_BUSSINESS I ON (GL."MA_TAI_KHOAN" = I."MA_TAI_KHOAN")
                            INNER JOIN tong_hop_bctc_nghiep_vu_cho_ct_chi_tiet_form AB
                                ON GL."CHI_TIET_ID" = AB."CHI_TIET_ID" AND GL."CHI_TIET_MODEL" = AB."CHI_TIET_MODEL"
                        WHERE GL."NGAY_HACH_TOAN" < ts_den_ngay
                        GROUP BY GL."MA_TAI_KHOAN",
                            "NGHIEP_VU"
                ;

                DROP TABLE IF EXISTS B03_GT_TBL_MASTER_DETAIL
                ;

                CREATE TEMP TABLE B03_GT_TBL_MASTER_DETAIL (
                    "ID_CHI_TIEU"          VARCHAR(500),
                    "MA_CHI_TIEU"          VARCHAR(500),
                    "ID_CHI_TIEU_CHI_TIET" VARCHAR(500),
                    "PHEP_TINH"            INTEGER,
                    "BAC"                  INTEGER,
                    "SO_TIEN_DAU_NAM"      FLOAT,
                    "SO_TIEN"              FLOAT
                )
                ;

                INSERT INTO B03_GT_TBL_MASTER_DETAIL (
                    SELECT
                        I."ID_CHI_TIEU"
                        , I."MA_CHI_TIEU"
                        , NULL                                    AS "ID_CHI_TIEU_CHI_TIET"
                        , 1                                       AS "PHEP_TINH"
                        , -1                                      AS "BAC"
                        , cast(SUM(I."SO_TIEN_DAU_NAM") AS FLOAT) AS "SO_TIEN_DAU_NAM"
                        , cast(SUM(I."SO_TIEN") AS FLOAT)         AS "SO_TIEN"
                    FROM (SELECT
                            I."ID_CHI_TIEU"
                            , I."MA_CHI_TIEU"
                            , cast(SUM(CASE WHEN I."KY_HIEU" = 'PhatsinhDU'
                                                OR I."KY_HIEU" = 'PhatsinhDUChiTietTheoHD_DAUTU'
                                                    AND B."HOAT_DONG" = '1'
                                                OR I."KY_HIEU" = 'PhatsinhDUChiTietTheoHD_TAICHINH'
                                                    AND B."HOAT_DONG" = '2'
                                                OR I."KY_HIEU" = 'PhatsinhDUChiTietTheoHD_SXKD'
                                                    AND B."HOAT_DONG" = '0'
                            THEN b."SO_TIEN_DAU_NAM"
                                        ELSE 0
                                        END * I."PHEP_TINH") AS FLOAT) AS "SO_TIEN_DAU_NAM"
                            , cast(SUM(CASE WHEN I."KY_HIEU" = 'PhatsinhDU'
                                                OR I."KY_HIEU" = 'PhatsinhDUChiTietTheoHD_DAUTU'
                                                    AND B."HOAT_DONG" = '1'
                                                OR I."KY_HIEU" = 'PhatsinhDUChiTietTheoHD_TAICHINH'
                                                    AND B."HOAT_DONG" = '2'
                                                OR I."KY_HIEU" = 'PhatsinhDUChiTietTheoHD_SXKD'
                                                    AND B."HOAT_DONG" = '0'
                            THEN (b."SO_TIEN")
                                        ELSE 0
                                        END * I."PHEP_TINH") AS FLOAT) AS "SO_TIEN"
                        FROM TBL_ITEM I
                            INNER JOIN TBL_DEBIT_BALANCE B ON (B."MA_TAI_KHOAN" LIKE I."MA_TAI_KHOAN_PT")
                                                                AND (B."MA_TAI_KHOAN_DOI_UNG" LIKE I."MA_TAI_KHOAN_DOI_UNG_PT")
                        WHERE LEFT(I."KY_HIEU", 10) = 'PhatsinhDU'
                        GROUP BY I."MA_CHI_TIEU", I."ID_CHI_TIEU"

                        -- Lấy phát sinh Nợ
                        UNION ALL
                        SELECT
                            I."ID_CHI_TIEU"
                            , I."MA_CHI_TIEU"
                            , cast(SUM(CASE WHEN I."KY_HIEU" = 'PhatsinhNO'
                                                OR I."KY_HIEU" = 'PhatsinhNO_ChiTietTheoHD_SXKD'
                                                    AND B."HOAT_DONG" = '0'
                            THEN b."SO_TIEN_DAU_NAM"
                                        ELSE 0
                                        END * I."PHEP_TINH") AS FLOAT) AS "SO_TIEN_DAU_NAM"
                            , cast(SUM(CASE WHEN I."KY_HIEU" = 'PhatsinhNO'
                                                OR I."KY_HIEU" = 'PhatsinhNO_ChiTietTheoHD_SXKD'
                                                    AND B."HOAT_DONG" = '0'
                            THEN b."SO_TIEN"
                                        ELSE 0
                                        END * I."PHEP_TINH") AS FLOAT) AS "SO_TIEN"
                        FROM TBL_ITEM I
                            INNER JOIN TBL_DEBIT_BALANCE B ON (B."MA_TAI_KHOAN" LIKE I."MA_TAI_KHOAN_PT")
                        WHERE LEFT(I."KY_HIEU", 10) = 'PhatsinhNO'
                        GROUP BY I."MA_CHI_TIEU", I."ID_CHI_TIEU"
                        UNION ALL
                        SELECT
                            I."ID_CHI_TIEU"
                            , I."MA_CHI_TIEU"
                            , cast(SUM(CASE WHEN I."KY_HIEU" = 'PhatsinhCO'
                                                OR I."KY_HIEU" = 'PhatsinhCO_ChiTietTheoHD_SXKD'
                                                    AND B."HOAT_DONG" = '0'
                            THEN b."SO_TIEN_DAU_NAM"
                                        ELSE 0
                                        END * I."PHEP_TINH") AS FLOAT) AS "SO_TIEN_DAU_NAM"
                            , cast(SUM(CASE WHEN I."KY_HIEU" = 'PhatsinhNO'
                                                OR I."KY_HIEU" = 'PhatsinhCO_ChiTietTheoHD_SXKD'
                                                    AND B."HOAT_DONG" = '0'
                            THEN b."SO_TIEN"
                                        ELSE 0
                                        END * I."PHEP_TINH") AS FLOAT) AS "SO_TIEN"
                        FROM TBL_ITEM I
                            INNER JOIN TBL_CREDIT_BALANCE B ON (B."MA_TAI_KHOAN" LIKE I."MA_TAI_KHOAN_PT")
                        WHERE LEFT(I."KY_HIEU", 10) = 'PhatsinhCO'
                        GROUP BY I."MA_CHI_TIEU", I."ID_CHI_TIEU"

                        -- Lấy lên phát sinh nợ có theo nghiệp vụ
                        UNION ALL
                        SELECT
                            I."ID_CHI_TIEU"
                            , I."MA_CHI_TIEU"
                            , cast(SUM(CASE WHEN I."KY_HIEU" = 'PhatsinhDU_ChiTietChiPhiLaiVayChiTraLaiVay'
                                                AND B."NGHIEP_VU" = '5'
                                                OR I."KY_HIEU" = 'PhatsinhDU_ChiTietThanhlyTSCD_BDSDT'
                                                    AND B."NGHIEP_VU" = '0'
                            THEN b."SO_TIEN_DAU_NAM"
                                        ELSE 0
                                        END * I."PHEP_TINH") AS FLOAT) AS "SO_TIEN_DAU_NAM"
                            , cast(SUM(CASE WHEN I."KY_HIEU" = 'PhatsinhDU_ChiTietChiPhiLaiVayChiTraLaiVay'
                                                AND B."NGHIEP_VU" = '5'
                                                OR I."KY_HIEU" = 'PhatsinhDU_ChiTietThanhlyTSCD_BDSDT'
                                                    AND B."NGHIEP_VU" = '0'
                            THEN (b."SO_TIEN")
                                        ELSE 0
                                        END * I."PHEP_TINH") AS FLOAT) AS "SO_TIEN"
                        FROM TBL_ITEM_BUSSINES I
                            INNER JOIN TBL_DEBIT_BALANCR_BUSSINESS B ON (B."MA_TAI_KHOAN" LIKE I."MA_TAI_KHOAN_PT")
                                                                        AND (B."MA_TAI_KHOAN_DOI_UNG" LIKE
                                                                            I."MA_TAI_KHOAN_DOI_UNG_PT")
                        WHERE LEFT(I."KY_HIEU", 10) = 'PhatsinhDU'
                        GROUP BY I."MA_CHI_TIEU", I."ID_CHI_TIEU"

                        -- Lấy phát sinh Nợ
                        UNION ALL
                        SELECT
                            I."ID_CHI_TIEU"
                            , I."MA_CHI_TIEU"
                            , cast(SUM(CASE WHEN I."KY_HIEU" = 'PhatsinhNO_ChiTietThanhlyTSCD_BDSDT'
                                                AND B."NGHIEP_VU" = '0'
                                                OR I."KY_HIEU" = 'PhatsinhNO_ChiTietDGLaiTSGVDT'
                                                    AND B."NGHIEP_VU" = '1'
                                                OR I."KY_HIEU" = 'PhatsinhNO_ChiTietBanThuHoiDTTC'
                                                    AND B."NGHIEP_VU" = '2'
                                                OR I."KY_HIEU" = 'PhatsinhNO_ChiTietChiPhiLaiVayChiTraLaiVay'
                                                    AND B."NGHIEP_VU" = '5'
                            THEN b."SO_TIEN_DAU_NAM"
                                        ELSE 0
                                        END * I."PHEP_TINH") AS FLOAT) AS "SO_TIEN_DAU_NAM"
                            , cast(SUM(CASE WHEN I."KY_HIEU" = 'PhatsinhNO_ChiTietThanhlyTSCD_BDSDT'
                                                AND B."NGHIEP_VU" = '0'
                                                OR I."KY_HIEU" = 'PhatsinhNO_ChiTietDGLaiTSGVDT'
                                                    AND B."NGHIEP_VU" = '1'
                                                OR I."KY_HIEU" = 'PhatsinhNO_ChiTietBanThuHoiDTTC'
                                                    AND B."NGHIEP_VU" = '2'
                                                OR I."KY_HIEU" = 'PhatsinhNO_ChiTietChiPhiLaiVayChiTraLaiVay'
                                                    AND B."NGHIEP_VU" = '5'
                            THEN b."SO_TIEN"
                                        ELSE 0
                                        END * I."PHEP_TINH") AS FLOAT) AS "SO_TIEN"
                        FROM TBL_ITEM_BUSSINES I
                            INNER JOIN TBL_DEBIT_BALANCR_BUSSINESS B ON (B."MA_TAI_KHOAN" LIKE I."MA_TAI_KHOAN_PT")
                        WHERE LEFT(I."KY_HIEU", 10) = 'PhatsinhNO'
                        GROUP BY I."MA_CHI_TIEU", I."ID_CHI_TIEU"
                        UNION ALL
                        SELECT
                            I."ID_CHI_TIEU"
                            , I."MA_CHI_TIEU"
                            , cast(SUM(CASE WHEN I."KY_HIEU" = 'PhatsinhCO_ChiTietThanhlyTSCD_BDSDT'
                                                AND B."NGHIEP_VU" = '0'
                                                OR I."KY_HIEU" = 'PhatsinhCO_ChiTietDGLaiTSGVDT'
                                                    AND B."NGHIEP_VU" = '1'
                                                OR I."KY_HIEU" = 'PhatsinhCO_ChiTietBanThuHoiDTTC'
                                                    AND B."NGHIEP_VU" = '2'
                                                OR I."KY_HIEU" = 'PhatsinhCO_ChiTietLai'
                                                    AND B."NGHIEP_VU" = '3'
                            THEN b."SO_TIEN_DAU_NAM"
                                        ELSE 0
                                        END * I."PHEP_TINH") AS FLOAT) AS "SO_TIEN_DAU_NAM"
                            , cast(SUM(CASE WHEN I."KY_HIEU" = 'PhatsinhCO_ChiTietThanhlyTSCD_BDSDT'
                                                AND B."NGHIEP_VU" = '0'
                                                OR I."KY_HIEU" = 'PhatsinhCO_ChiTietDGLaiTSGVDT'
                                                    AND B."NGHIEP_VU" = '1'
                                                OR I."KY_HIEU" = 'PhatsinhCO_ChiTietBanThuHoiDTTC'
                                                    AND B."NGHIEP_VU" = '2'
                                                OR I."KY_HIEU" = 'PhatsinhCO_ChiTietLai'
                                                    AND B."NGHIEP_VU" = '3'
                            THEN b."SO_TIEN"
                                        ELSE 0
                                        END * I."PHEP_TINH") AS FLOAT) AS "SO_TIEN"
                        FROM TBL_ITEM_BUSSINES I
                            INNER JOIN TBL_CREDIT_BALANCE_BUSSINESS B ON (B."MA_TAI_KHOAN" LIKE I."MA_TAI_KHOAN_PT")
                        WHERE LEFT(I."KY_HIEU", 10) = 'PhatsinhCO'
                        GROUP BY I."MA_CHI_TIEU", I."ID_CHI_TIEU"


                        -- Lấy số dư
                        UNION ALL
                        SELECT
                            I."ID_CHI_TIEU"
                            , I."MA_CHI_TIEU"
                            , cast(SUM((CASE WHEN LEFT(I."KY_HIEU", 6) = 'DUNODK'
                            THEN B."GHI_NO_DAU_KY_DAU_NAM"
                                        WHEN LEFT(I."KY_HIEU", 6) = 'DUCODK'
                                            THEN B."GHI_CO_DAU_KY_DAU_NAM"
                                        WHEN LEFT(I."KY_HIEU", 6) = 'DUNOCK'
                                            THEN B."GHI_NO_DAU_KY"
                                        WHEN LEFT(I."KY_HIEU", 6) = 'DUCOCK'
                                            THEN B."GHI_CO_DAU_KY"
                                        ELSE 0
                                        END) * I."PHEP_TINH") AS FLOAT) AS "SO_TIEN_DAU_NAM"
                            , cast(SUM((CASE WHEN LEFT(I."KY_HIEU", 6) = 'DUNODK'
                            THEN B."GHI_NO_DAU_KY"
                                        WHEN LEFT(I."KY_HIEU", 6) = 'DUCODK'
                                            THEN B."GHI_CO_DAU_KY"
                                        WHEN LEFT(I."KY_HIEU", 6) = 'DUNOCK'
                                            THEN B."GHI_NO_TON"
                                        WHEN LEFT(I."KY_HIEU", 6) = 'DUCOCK'
                                            THEN B."GHI_CO_TON"
                                        ELSE 0
                                        END) * I."PHEP_TINH") AS FLOAT) AS "SO_TIEN"
                        FROM TBL_ITEM I
                            INNER JOIN TBL_BALANCE B ON B."MA_TAI_KHOAN" LIKE I."MA_TAI_KHOAN_PT"
                                                        AND B."LOAI_CHI_TIET_THEO_DOI_TUONG" = I."LOAI_CHI_TIET_THEO_DOI_TUONG"
                                                        AND cast(I."HOAT_DONG" AS VARCHAR(127)) = B."HOAT_DONG"
                        GROUP BY I."MA_CHI_TIEU", I."ID_CHI_TIEU"
                        ) AS I
                    GROUP BY I."MA_CHI_TIEU", I."ID_CHI_TIEU")
                ;

                SELECT DT."ID_CHI_TIEU"
                INTO B02ProfitBeforeTaxID
                FROM tien_ich_thiet_lap_bao_cao_tai_chinh MT
                    INNER JOIN tien_ich_bao_cao_tai_chinh_chi_tiet DT ON MT.id = DT."CHI_TIET_ID"
                WHERE "TEN_BAO_CAO" = 'BAO_CAO_KET_QUA_HOAT_DONG_KINH_DOANH'
                    AND "CHE_DO_KE_TOAN" = cast(AccountingSystem AS VARCHAR(500))
                    AND DT."MA_CHI_TIEU" = '50'
                ;


                SELECT DT."ID_CHI_TIEU"
                INTO ItemProfitBeforeTax
                FROM tien_ich_thiet_lap_bao_cao_tai_chinh MT
                    INNER JOIN tien_ich_bao_cao_tai_chinh_chi_tiet DT ON MT.id = DT."CHI_TIET_ID"
                WHERE DT."MA_CHI_TIEU" = '01'
                    AND "CHE_DO_KE_TOAN" = '15'
                    AND "ReportID" = 6
                ;

                DROP TABLE IF EXISTS TBL_GET_B02
                ;

                CREATE TEMP TABLE TBL_GET_B02
                    AS
                        SELECT *
                        FROM GET_BAO_CAO_TAI_CHINH_B02_DN(16, 0, ts_tu_ngay, ts_den_ngay, ts_PrevFromDate, ts_PrevToDate) F
                        WHERE F."ID_CHI_TIEU" = B02ProfitBeforeTaxID
                ;


                INSERT INTO B03_GT_TBL_MASTER_DETAIL (
                    SELECT
                        ItemProfitBeforeTax
                        , NULL :: VARCHAR(500)
                        , NULL :: VARCHAR(500)
                        , 1
                        , -1
                        , cast(coalesce(F."SO_TIEN_DAU_NAM", 0) AS FLOAT) AS "SO_TIEN"
                        , cast(coalesce(F."SO_TIEN", 0) AS FLOAT)         AS "SO_TIEN_DAU_NAM"

                    FROM TBL_GET_B02 F
                )
                ;


                INSERT INTO B03_GT_TBL_MASTER_DETAIL (
                    SELECT
                        DT."ID_CHI_TIEU"
                        , DT."MA_CHI_TIEU"
                        , TH."ID_CHI_TIEU" AS "ID_CHI_TIEU_CHI_TIET"
                        , CASE WHEN TH."PHEP_TINH" = 'CONG'
                        THEN 1
                        ELSE -1 END      AS "PHEP_TINH"
                        , 0                AS "BAC"
                        , cast(0 AS FLOAT)                AS "SO_TIEN_DAU_NAM"
                        , cast(0 AS FLOAT)                AS "SO_TIEN"
                    FROM tien_ich_thiet_lap_bao_cao_tai_chinh MT
                        INNER JOIN tien_ich_bao_cao_tai_chinh_chi_tiet DT ON MT.id = DT."CHI_TIET_ID"
                        LEFT JOIN tien_ich_xay_dung_cong_thuc_loai_chi_tieu_tong_hop TH ON DT.id = TH."CHI_TIET_ID"
                    WHERE "CHE_DO_KE_TOAN" = cast(AccountingSystem AS VARCHAR(500))
                        AND "ReportID" = report_id
                        AND DT."LOAI_CHI_TIEU" = '1'
                        AND DT."CONG_THUC" IS NOT NULL
                )
                ;

                -- Cộng chỉ tiêu con lên chỉ tiêu cha
                WITH RECURSIVE V ( "ID_CHI_TIEU", "ID_CHI_TIEU_CHI_TIET", "SO_TIEN_DAU_NAM", "SO_TIEN", "PHEP_TINH" )
                AS ( SELECT
                        A."ID_CHI_TIEU"
                        , A."ID_CHI_TIEU_CHI_TIET"
                        , A."SO_TIEN_DAU_NAM"
                        , A."SO_TIEN"
                        , A."PHEP_TINH"
                    FROM B03_GT_TBL_MASTER_DETAIL A
                    WHERE "BAC" = -1
                    UNION ALL
                    SELECT
                        B."ID_CHI_TIEU"
                        , B."ID_CHI_TIEU_CHI_TIET"
                        , V."SO_TIEN_DAU_NAM"
                        , V."SO_TIEN"
                        , B."PHEP_TINH" * V."PHEP_TINH" AS "PHEP_TINH"
                    FROM B03_GT_TBL_MASTER_DETAIL B,
                        V
                    WHERE B."ID_CHI_TIEU_CHI_TIET" = V."ID_CHI_TIEU"
                )

            INSERT INTO B03_TMP_KET_QUA(
            SELECT
                    FR."ID_CHI_TIEU" ,
                    FR."MA_CHI_TIEU" ,
                    FR."TEN_CHI_TIEU" ,
                    FR."TEN_TIENG_ANH" ,
                    FR."SO_THU_TU" ,
                    FR."THUYET_MINH" ,
                    FR."LOAI_CHI_TIEU" ,
                    CASE WHEN FR."LOAI_CHI_TIEU" = '1' THEN FR."CONG_THUC"
                        ELSE ''
                    END AS "CONG_THUC" ,
                    FR."KHONG_IN" ,
                    FR."IN_DAM" ,
                    FR."IN_NGHIENG" ,
                    coalesce(X."SO_TIEN_NAM_NAY", 0) AS "SO_TIEN_NAM_NAY",
                    coalesce(X."SO_TIEN_DAU_NAM", 0) AS "SO_TIEN_DAU_NAM"

            FROM    ( SELECT    V."ID_CHI_TIEU" ,
                                SUM(V."PHEP_TINH" * V."SO_TIEN_DAU_NAM") AS "SO_TIEN_DAU_NAM" ,
                                SUM(V."PHEP_TINH" * V."SO_TIEN") AS "SO_TIEN_NAM_NAY"
                    FROM      V
                    GROUP BY  V."ID_CHI_TIEU"
                    ) AS X
                    RIGHT JOIN (SELECT
                                        MT."CHE_DO_KE_TOAN"
                                        , MT."TEN_BAO_CAO"
                                        , DT.*
                                    FROM tien_ich_thiet_lap_bao_cao_tai_chinh MT
                                        INNER JOIN tien_ich_bao_cao_tai_chinh_chi_tiet DT ON MT.id = DT."CHI_TIET_ID") FR
                            ON FR."ID_CHI_TIEU" = X."ID_CHI_TIEU"
            WHERE   "CHE_DO_KE_TOAN" = cast(AccountingSystem AS VARCHAR(127))
                    AND FR."ReportID" = report_id
            );

            RETURN QUERY SELECT *FROM B03_TMP_KET_QUA;
            END;
            $$ LANGUAGE PLpgSQL;


            -- SELECT *FROM GET_BAO_CAO_TAI_CHINH_B03_DN_GIAN_TIEP(16, 0, '2018-01-01', '2019-06-20', '2016-07-14', '2017-12-31')
		""")
    
    class BAO_CAO_B03DN_GT_BAO_CAO_LUU_CHUYEN_TIEN_TE_PP_GIAN_TIEP_REPORT(models.AbstractModel):
        _name = 'report.bao_cao.template_b03dngt_luu_chuyen_tien_te_pp_gian_tiep'

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