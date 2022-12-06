# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_BANG_CAN_DOI_TAI_KHOAN(models.Model):
    _name = 'bao.cao.bang.can.doi.tai.khoan'
 
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TU_NGAY = fields.Date(string='Từ', help='Từ ngày',required=True,default=fields.Datetime.now)
    DEN_NGAY = fields.Date(string='Đến', help='Đến ngày',required=True,default=fields.Datetime.now)
    BAC_TAI_KHOAN = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ], string='Bậc tài khoản', help='Bậc tài khoản',default='1',required=True)
    HIEN_THI_SO_DU_HAI_BEN = fields.Boolean(string='Hiển thị số dư 2 bên', help='Hiển thị số dư hai bên')
    BU_TRU_CONG_NO_CUA_CUNG_DOI_TUONG_GIUA_CAC_CHI_NHANH = fields.Boolean(string='Bù trừ công nợ của cùng đối tượng giữa các chi nhánh', help='Bù trừ công nợ của cùng đối tượng giữa các chi nhánh')
    
    SO_HIEU_TAI_KHOAN = fields.Char(string='Số hiệu tài khoản', help='Số hiệu tài khoản')
    TEN_TAI_KHOAN = fields.Char(string='Tên tài khoản', help='Tên tài khoản')
    NO_DAU_KY = fields.Float(string='Nợ đầu kỳ', help='Nợ đầu kỳ' ,digits= decimal_precision.get_precision('VND'))
    CO_DAU_KY = fields.Float(string='Có đầu kỳ', help='Có đầu kỳ' ,digits= decimal_precision.get_precision('VND'))
    NO_PHAT_SINH = fields.Float(string='Nợ phát sinh', help='Nợ phát sinh' ,digits= decimal_precision.get_precision('VND'))
    CO_PHAT_SINH = fields.Float(string='Có phát sinh', help='Có phát sinh' ,digits= decimal_precision.get_precision('VND'))
    NO_CUOI_KY = fields.Float(string='Nợ cuối kỳ', help='Nợ cuối kỳ' ,digits= decimal_precision.get_precision('VND'))
    CO_CUOI_KY = fields.Float(string='Có cuối kỳ', help='Có cuối kỳ' ,digits= decimal_precision.get_precision('VND'))
    BAC = fields.Integer(string='Bậc', help='Bậc')
    name = fields.Char(string='Name', help='Name', oldname='NAME')


    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU_NGAY', 'DEN_NGAY')

    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_BANG_CAN_DOI_TAI_KHOAN, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],order="MA_DON_VI",limit=1)
        if chi_nhanh:
          result['CHI_NHANH_ID'] = chi_nhanh.id
        return result


    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        # Execute SQL query here
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
        HIEN_THI_SO_DU_HAI_BEN = 1 if 'HIEN_THI_SO_DU_HAI_BEN' in params.keys() and params['HIEN_THI_SO_DU_HAI_BEN'] != 'False' else 0
        BU_TRU_CONG_NO_CUA_CUNG_DOI_TUONG_GIUA_CAC_CHI_NHANH = 1 if 'BU_TRU_CONG_NO_CUA_CUNG_DOI_TUONG_GIUA_CAC_CHI_NHANH' in params.keys() and params['BU_TRU_CONG_NO_CUA_CUNG_DOI_TUONG_GIUA_CAC_CHI_NHANH'] != 'False' else 0
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
        BAC_TAI_KHOAN = params['BAC_TAI_KHOAN'] if 'BAC_TAI_KHOAN' in params.keys() and params['BAC_TAI_KHOAN'] != 'False' else None

        bac_tai_khoan = int(BAC_TAI_KHOAN)
        
        params_sql = {
            'TU_NGAY':TU_NGAY_F, 
            'DEN_NGAY':DEN_NGAY_F,
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'HIEN_THI_SO_DU_HAI_BEN':HIEN_THI_SO_DU_HAI_BEN,
            'BU_TRU_CONG_NO_CUA_CUNG_DOI_TUONG_GIUA_CAC_CHI_NHANH':BU_TRU_CONG_NO_CUA_CUNG_DOI_TUONG_GIUA_CAC_CHI_NHANH,
            'CHI_NHANH_ID':CHI_NHANH_ID,
            'BAC_TAI_KHOAN':bac_tai_khoan,
        }
        query = """DO LANGUAGE plpgsql $$
                DECLARE
                chi_nhanh                     INTEGER := %(CHI_NHANH_ID)s;  --Chi nhánh

                bao_gom_chi_nhanh_phu_thuoc   INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;  --Lấy số liệu chi nhánh phụ thuộc

                tu_ngay                       DATE := %(TU_NGAY)s;  -- Đến ngày

                den_ngay                      DATE := %(DEN_NGAY)s;  --Từ ngày

                bac_tai_khoan                 INTEGER := %(BAC_TAI_KHOAN)s;   --Bậc tài khoản

                lay_so_lieu_tu_bao_cao_da_lap INTEGER := 0;  --Lấy số liệu từ báo cáo tài chính đã lập

                IsBalanceBothSide             INTEGER := %(HIEN_THI_SO_DU_HAI_BEN)s;  -- Hiển thị số dư hai bên

                IsSimilarBranch               INTEGER := %(BU_TRU_CONG_NO_CUA_CUNG_DOI_TUONG_GIUA_CAC_CHI_NHANH)s;


                AccountingSystem              INTEGER;

                SubAccountingSystem           INTEGER := 0;

                ngay_bat_dau                  DATE;

                loai_tien_chinh               INTEGER;
                IsExistForeinCurrency INTEGER;

                BEGIN

                SELECT value
                INTO AccountingSystem
                FROM ir_config_parameter
                WHERE key = 'he_thong.CHE_DO_KE_TOAN'
                FETCH FIRST 1 ROW ONLY
                ;

                SELECT value
                INTO loai_tien_chinh
                FROM ir_config_parameter
                WHERE key = 'he_thong.LOAI_TIEN_CHINH'
                FETCH FIRST 1 ROW ONLY
                ;

                DROP TABLE IF EXISTS TBL_BRANCH
                ;

                CREATE TEMP TABLE TBL_BRANCH
                AS
                SELECT DISTINCT
                OU.id           AS "CHI_NHANH_ID"
                , OU."MA_DON_VI"  AS "MA_CHI_NHANH"
                , OU."TEN_DON_VI" AS "TEN_CHI_NHANH"
                FROM danh_muc_to_chuc OU

                WHERE /*1. Lấy đúng CN được truyền ID vào*/
                OU.id = chi_nhanh
                /*2. Nếu yêu cầu lấy CN phụ thuộc → lấy thêm các dòng cấp là Chi Nhánh có tích chọn Phụ thuộc và có ParentID = ID truyền vào (để đảm bảo là đang truyền vào TCT)*/
                OR (bao_gom_chi_nhanh_phu_thuoc = 1 AND OU."HACH_TOAN_SELECTION" = 'DOC_LAP' AND "CAP_TO_CHUC" = '2' AND
                parent_id = chi_nhanh)
                /*3. Đơn chi nhánh hoặc truyền BranchID = NULL thì lấy tất cả chi nhánh*/
                OR (chi_nhanh IS NULL AND "CAP_TO_CHUC" IN ('1', '2'))
                ;

                SELECT value
                INTO ngay_bat_dau
                FROM ir_config_parameter
                WHERE key = 'he_thong.TU_NGAY_BAT_DAU_TAI_CHINH'
                FETCH FIRST 1 ROW ONLY
                ;

                IF lay_so_lieu_tu_bao_cao_da_lap = 1
                THEN
                IF EXISTS(
                SELECT  *
                FROM    tong_hop_bao_cao_tai_chinh_chi_tiet_b01_dn FRD
                INNER JOIN tong_hop_bao_cao_tai_chinh FR ON FR.id = FRD."BAO_CAO_TAI_CHINH_ID"
                WHERE   DATE_PART('day',FR."TU_NGAY_BAT_RA":: timestamp - tu_ngay:: timestamp) = 0
                AND DATE_PART('day',FR."DEN_NGAY_BAT_RA":: timestamp - den_ngay:: timestamp) = 0
                AND "LOAI_CHUNG_TU" = 4050
                AND ( AccountingSystem = @AccountingSystem
                OR "HE_THONG_TAI_KHOAN" = '2015'
                )
                AND "CHI_NHANH_ID" = chi_nhanh
                AND "MA_SO" LIKE N'007%%'
                AND ( "SO_DAU_QUY" <> 0
                OR "SO_DAU_QUY" <> 0
                OR "GHI_NO" <> 0
                OR "GHI_CO" <> 0
                OR "SO_DAU_QUY" <> 0
                OR "SO_DAU_QUY" <> 0
                )
                )
                THEN
                IsExistForeinCurrency := 1;
                ELSE
                IsExistForeinCurrency := 0;
                END IF;
                --             SELECT  FRD.* ,
                --                         FR.ReportCreatedDate ,
                --                         FR.ReportCreatedBy,--tthoa lấy thêm 6/2/2015 để phục vụ drilldown
                --                    FR.DirectorName,-- tthoa lấy thêm 24/10/2015 để hiển thị với các BCTC đã lập
                --                         A.DetailByAccountObject ,
                --                         A.AccountObjectType ,
                --                         @IsBalanceBothSide AS IsBalanceBothSide ,
                --                         --A.AccountNameEnglish ,-lấy trong bảng FRF01ReportDetail
                --                         --dvtien-03/10/2016 sửa bug14198 lấy thêm thông tin AccountingSystem
                --                         FR.AccountingSystem
                --                 FROM    dbo.FRF01ReportDetail FRD
                --                         INNER JOIN FRReportList FR ON FR.RefID = FRD.RefID
                --                         LEFT JOIN dbo.Account A ON FRD.AccountID = A.AccountID
                --                 WHERE   /*Modified by hoant 25.03.2016 sửa lỗi ngày tháng truyền có time dẫn đến không lấy lên số liệu*/
                --                         DAY(FromDate) = DAY(@FromDate)
                --                         AND MONTH(FromDate) = MONTH(@FromDate)
                --                         AND YEAR(FromDate) = YEAR(@FromDate)
                --                         AND DAY(ToDate) = DAY(@ToDate)
                --                         AND MONTH(ToDate) = MONTH(@ToDate)
                --                         AND YEAR(ToDate) = YEAR(@ToDate)
                --              --AND ToDate = @ToDate
                --                         AND Reftype = 4050
                --                          --dvtien-03/10/2016 sửa bug14198: rem bỏ vì khi convert từ 2015 lên thì AccountingSystem=2015
                --                         AND ( AccountingSystem = @AccountingSystem
                --                               OR AccountingSystem = 2015
                --                             )
                --                         AND BranchID = @BranchID
                --                         AND FRD.AccountNumber <> '' --dvtien 11/10/2016: vì trường hợp convert từ 2015 cần lấy lên cả những tài khoản ngoài bảng ( đã xóa khỏi hệ thống tk)
                --                         AND ( @IsWorkingWithManagementBook = 1
                --                               AND DisplayOnBook = 1
                --                               OR @IsWorkingWithManagementBook = 0
                --                               AND DisplayOnBook = 0
                --                             )
                --                         AND ( FRD.AccountNumber LIKE N'007%%'
                --                               AND @IsExistForeinCurrency = 1
                --                               AND ( FRD.IsParent = 1
                --                                     AND FRD.Grade <= @MaxAccountGrade
                --                                     OR FRD.IsParent = 0
                --                                     AND ( OpeningDebitAmount <> 0
                --                                           OR OpeningCreditAmount <> 0
                --                                           OR DebitAmount <> 0
                --                                           OR CreditAmount <> 0
                --                                           OR ClosingDebitAmount <> 0
                --                                           OR ClosingCreditAmount <> 0
                --                                         )
                --                                   )
                --                               OR ( FRD.AccountNumber NOT LIKE N'007%%'
                --                                    AND FRD.Grade <= @MaxAccountGrade
                --                                    AND ( OpeningDebitAmount <> 0
                --                                          OR OpeningCreditAmount <> 0
                --                                          OR DebitAmount <> 0
                --                                          OR CreditAmount <> 0
                --                                          OR ClosingDebitAmount <> 0
                --                                          OR ClosingCreditAmount <> 0
                --                                        )
                --                                  )
                --                             )
                --                 ORDER BY FRD.AccountKind ,
                --                         FRD.AccountNumber ,
                --                         FRD.SortOrder
                ELSE
                DROP TABLE IF EXISTS TMP_KET_QUA1
                ;

                CREATE TEMP TABLE TMP_KET_QUA1
                AS
                SELECT  FR.* ,
                CAST(NULL AS DATE) AS "NGAY_LAP_BAO_CAO" ,
                '' AS "NGUOI_TAO" ,
                '' AS "TEN_GIAM_DOC"
                --                     @IsBalanceBothSide AS IsBalanceBothSide ,
                --                     @AccountingSystem AS AccountingSystem --dvtien-03/10/2016 sửa bug14198 lấy thêm thông tin AccountingSystem
                FROM    FUNC_GLR_GETF01(chi_nhanh,bao_gom_chi_nhanh_phu_thuoc,tu_ngay,den_ngay,bac_tai_khoan,lay_so_lieu_tu_bao_cao_da_lap,IsBalanceBothSide,IsSimilarBranch) FR
                ORDER BY FR."TINH_CHAT" ,
                FR."MA_TAI_KHOAN" ,
                FR."THU_TU_TRONG_CHUNG_TU";
                END IF;

                END $$
                ;

                SELECT 
                            "MA_TAI_KHOAN" AS "SO_HIEU_TAI_KHOAN",
                            "TEN_TAI_KHOAN" AS"TEN_TAI_KHOAN",
                            "GHI_NO_DAU_KY" AS "NO_DAU_KY",
                            "GHI_CO_DAU_KY" AS"CO_DAU_KY",
                            "GHI_NO" AS "NO_PHAT_SINH",
                            "GHI_CO" AS"CO_PHAT_SINH",
                            "GHI_NO_CUOI_KY" AS "NO_CUOI_KY",
                            "GHI_CO_CUOI_KY" AS"CO_CUOI_KY",
                            "BAC"
                           
                FROM TMP_KET_QUA1
                ;
        """
        du_lieu_ids = self.execute(query,params_sql)
        tong_no_dau_ky = 0
        tong_co_dau_ky = 0
        tong_phat_sinh_no = 0
        tong_phat_sinh_co = 0
        tong_cuoi_ky_no = 0
        tong_cuoi_ky_co = 0
        for line in du_lieu_ids:
            if line.get('BAC') == 1:
                tong_no_dau_ky += line.get('NO_DAU_KY')
                tong_co_dau_ky += line.get('CO_DAU_KY')
                tong_phat_sinh_no += line.get('NO_PHAT_SINH')
                tong_phat_sinh_co += line.get('CO_PHAT_SINH')
                tong_cuoi_ky_no += line.get('NO_CUOI_KY')
                tong_cuoi_ky_co += line.get('CO_CUOI_KY')
        dict_dong_them = {
            'SO_HIEU_TAI_KHOAN' : '',
            'TEN_TAI_KHOAN' : 'Cộng',
            'NO_DAU_KY' : tong_no_dau_ky,
            'CO_DAU_KY' : tong_co_dau_ky,
            'NO_PHAT_SINH' : tong_phat_sinh_no,
            'CO_PHAT_SINH' : tong_phat_sinh_co,
            'NO_CUOI_KY' : tong_cuoi_ky_no,
            'CO_CUOI_KY' : tong_cuoi_ky_co,
            'BAC' : 1,
        }
        du_lieu_ids.append(dict_dong_them)
        return du_lieu_ids

    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        # self._validate()
        TU_NGAY_F = self.get_vntime('TU_NGAY')
        DEN_NGAY_F = self.get_vntime('DEN_NGAY')
        param = 'Từ ngày: %s đến ngày %s' % (TU_NGAY_F, DEN_NGAY_F)
        action = self.env.ref('bao_cao.open_report_bang_can_doi_tai_khoan').read()[0]
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        # action['options'] = {'clear_breadcrumbs': True}
        return action

    

    @api.model_cr
    def init(self):
        self.env.cr.execute(""" 
			-- DROP FUNCTION FUNC_GLR_GETF01(IN ma_tai_khoan VARCHAR(127),loai_tien_id INTEGER,chi_nhanh_id INTEGER,doi_tuong_id INTEGER)
            CREATE OR REPLACE FUNCTION FUNC_GLR_GETF01(IN chi_nhanh                     INTEGER,
                                                        bao_gom_chi_nhanh_phu_thuoc   INTEGER,
                                                        tu_ngay                       DATE, den_ngay DATE, bac_tai_khoan INTEGER,
                                                        lay_so_lieu_tu_bao_cao_da_lap INTEGER, IsBalanceBothSide INTEGER,
                                                        IsSimilarBranch               INTEGER)
                RETURNS TABLE("TAI_KHOAN_ID"            INTEGER,
                            "CHI_TIET_THEO_DOI_TUONG" BOOLEAN,
                            "DOI_TUONG_SELECTION"     VARCHAR(127),
                            "MA_TAI_KHOAN"            VARCHAR(127),
                            "TEN_TAI_KHOAN"           VARCHAR(127),
                            "TEN_TIENG_ANH"           VARCHAR(127),
                            "LOAI_TAI_KHOAN"          VARCHAR(127),
                            "LA_TK_TONG_HOP"          BOOLEAN,
                            "parent_id"               INTEGER,
                            "BAC"                     INTEGER,
                            "TINH_CHAT"               INTEGER,
                            "THU_TU_TRONG_CHUNG_TU"   INTEGER,
                            "GHI_NO_DAU_KY"           FLOAT,
                            "GHI_CO_DAU_KY"           FLOAT,
                            "GHI_NO"                  FLOAT,
                            "GHI_CO"                  FLOAT,
                            "GHI_NO_LUY_KY"           FLOAT,
                            "GHI_CO_LUY_KY"           FLOAT,
                            "GHI_NO_CUOI_KY"          FLOAT,
                            "GHI_CO_CUOI_KY"          FLOAT
                ) AS $$
            DECLARE

                AccountingSystem    INTEGER;

                SubAccountingSystem INTEGER := 0;

                ngay_bat_dau        DATE;

                loai_tien_chinh     INTEGER;

            BEGIN

                SELECT value
                INTO AccountingSystem
                FROM ir_config_parameter
                WHERE key = 'he_thong.CHE_DO_KE_TOAN'
                FETCH FIRST 1 ROW ONLY
                ;

                SELECT value
                INTO loai_tien_chinh
                FROM ir_config_parameter
                WHERE key = 'he_thong.LOAI_TIEN_CHINH'
                FETCH FIRST 1 ROW ONLY
                ;

                DROP TABLE IF EXISTS TBL_BRANCH
                ;

                CREATE TEMP TABLE TBL_BRANCH
                    AS
                        SELECT DISTINCT
                            OU.id           AS "CHI_NHANH_ID"
                            , OU."MA_DON_VI"  AS "MA_CHI_NHANH"
                            , OU."TEN_DON_VI" AS "TEN_CHI_NHANH"
                        FROM danh_muc_to_chuc OU

                        WHERE /*1. Lấy đúng CN được truyền ID vào*/
                            OU.id = chi_nhanh
                            /*2. Nếu yêu cầu lấy CN phụ thuộc → lấy thêm các dòng cấp là Chi Nhánh có tích chọn Phụ thuộc và có ParentID = ID truyền vào (để đảm bảo là đang truyền vào TCT)*/
                            OR (bao_gom_chi_nhanh_phu_thuoc = 1 AND OU."HACH_TOAN_SELECTION" = 'DOC_LAP' AND "CAP_TO_CHUC" = '2'
                                AND
                                OU.parent_id = chi_nhanh)
                            /*3. Đơn chi nhánh hoặc truyền "CHI_NHANH_ID" = NULL thì lấy tất cả chi nhánh*/
                            OR (chi_nhanh IS NULL AND "CAP_TO_CHUC" IN ('1', '2'))
                ;

                SELECT value
                INTO ngay_bat_dau
                FROM ir_config_parameter
                WHERE key = 'he_thong.TU_NGAY_BAT_DAU_TAI_CHINH'
                FETCH FIRST 1 ROW ONLY
                ;

                DROP TABLE IF EXISTS TMP_KET_QUA
                ;

                CREATE TEMP TABLE TMP_KET_QUA (
                    "TAI_KHOAN_ID"            INTEGER,
                    "CHI_TIET_THEO_DOI_TUONG" BOOLEAN,
                    "DOI_TUONG_SELECTION"     VARCHAR(127),
                    "MA_TAI_KHOAN"            VARCHAR(127),
                    "TEN_TAI_KHOAN"           VARCHAR(127),
                    "TEN_TIENG_ANH"           VARCHAR(127),
                    "LOAI_TAI_KHOAN"          VARCHAR(127),
                    "LA_TK_TONG_HOP"          BOOLEAN,
                    "parent_id"               INTEGER,
                    "BAC"                     INTEGER,
                    "TINH_CHAT"               INTEGER,
                    "THU_TU_TRONG_CHUNG_TU"   INTEGER,
                    "GHI_NO_DAU_KY"           FLOAT,
                    "GHI_CO_DAU_KY"           FLOAT,
                    "GHI_NO"                  FLOAT,
                    "GHI_CO"                  FLOAT,
                    "GHI_NO_LUY_KY"           FLOAT,
                    "GHI_CO_LUY_KY"           FLOAT,
                    "GHI_NO_CUOI_KY"          FLOAT,
                    "GHI_CO_CUOI_KY"          FLOAT
                )
                ;

                --     Mẫu 2 bên
                IF IsBalanceBothSide = 1
                THEN
                    DROP TABLE IF EXISTS TMP_SO_CAI_CHI_TIET_1
                    ;

                    CREATE TEMP TABLE TMP_SO_CAI_CHI_TIET_1
                        AS

                            SELECT G.*
                            FROM (
                                    SELECT
                                        GL."MA_TAI_KHOAN"
                                        , "DOI_TUONG_ID"
                                        , GL."CHI_NHANH_ID"
                                        , GL."currency_id"
                                        , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                                        THEN GL."GHI_NO" - GL."GHI_CO"
                                            ELSE 0
                                            END) AS "GHI_NO_DAU_KY"
                                        , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                        THEN (GL."GHI_NO")
                                            ELSE 0
                                            END) AS "GHI_NO"
                                        , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                        THEN (GL."GHI_CO")
                                            ELSE 0
                                            END) AS "GHI_CO"
                                        , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ngay_bat_dau AND den_ngay
                                        THEN (GL."GHI_NO")
                                            ELSE 0
                                            END) AS "GHI_NO_LUY_KE"
                                        , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ngay_bat_dau AND den_ngay
                                        THEN (GL."GHI_CO")
                                            ELSE 0
                                            END) AS "GHI_CO_LUY_KE"
                                        , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                                        THEN GL."GHI_NO_NGUYEN_TE" - GL."GHI_CO_NGUYEN_TE"
                                            ELSE 0
                                            END) AS "GHI_NO_NGUYEN_TE_DAU_KY"
                                        , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                        THEN (GL."GHI_NO_NGUYEN_TE")
                                            ELSE 0
                                            END) AS "GHI_NO_NGUYEN_TE"
                                        , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                        THEN (GL."GHI_CO_NGUYEN_TE")
                                            ELSE 0
                                            END) AS "GHI_CO_NGUYEN_TE"
                                        , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ngay_bat_dau AND den_ngay
                                        THEN (GL."GHI_NO_NGUYEN_TE")
                                            ELSE 0
                                            END) AS DebitAmountOCAccum
                                        , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ngay_bat_dau AND den_ngay
                                        THEN (GL."GHI_CO_NGUYEN_TE")
                                            ELSE 0
                                            END) AS CreditAmountOCAccum
                                    FROM so_cai_chi_tiet AS GL
                                    WHERE GL."NGAY_HACH_TOAN" <= den_ngay
                                    GROUP BY GL."MA_TAI_KHOAN",
                                        "DOI_TUONG_ID",
                                        GL."CHI_NHANH_ID",
                                        GL."currency_id"
                                ) G
                                JOIN (SELECT *
                                    FROM TBL_BRANCH) OU ON G."CHI_NHANH_ID" = OU."CHI_NHANH_ID"
                    ;


                    -- Phần không có TK Ngoại bảng Lấy cho cả QĐ 15 và 48
                    -- mtruong: sửa bảng cân đối tài khoản số dư 2 bên thì lấy dữ liệu cho những tài khoản chi tiết nhất, sau đó cộng gộp vào TK cha.
                    DROP TABLE IF EXISTS DU_LIEU_CHI_TIET
                    ;

                    CREATE TEMP TABLE DU_LIEU_CHI_TIET
                        AS
                            SELECT
                                F."MA_TAI_KHOAN"
                                , ''                     AS "currency_id"
                                , 0                      AS "THU_TU"
                                , SUM(CASE WHEN F."TINH_CHAT" = '0'
                                                OR (
                                                    F."TINH_CHAT" NOT IN ('0', '1')
                                                    AND F."GHI_NO_DAU_KY" > 0
                                                )
                                THEN F."GHI_NO_DAU_KY"
                                    ELSE 0
                                    END)               AS "GHI_NO_DAU_KY"
                                , SUM(CASE WHEN F."TINH_CHAT" = '1'
                                                OR (
                                                    F."TINH_CHAT" NOT IN ('0', '1')
                                                    AND F."GHI_NO_DAU_KY" < 0
                                                )
                                THEN -1 * F."GHI_NO_DAU_KY"
                                    ELSE 0
                                    END)               AS "GHI_CO_DAU_KY"
                                , SUM(F."GHI_NO")        AS "GHI_NO"
                                , SUM(F."GHI_CO")        AS "GHI_CO"
                                , SUM(F."GHI_NO_LUY_KE") AS "GHI_NO_LUY_KE"
                                , SUM(F."GHI_CO_LUY_KE") AS "GHI_CO_LUY_KE"
                                , SUM(CASE WHEN F."TINH_CHAT" = '0'
                                                OR (
                                                    F."TINH_CHAT" NOT IN ('0', '1')
                                                    AND F."GHI_NO_DAU_KY" + F."GHI_NO" - F."GHI_CO" > 0
                                                )
                                THEN F."GHI_NO_DAU_KY" + F."GHI_NO" - F."GHI_CO"
                                    ELSE 0
                                    END)               AS "GHI_NO_CUOI_KY"
                                , SUM(CASE WHEN F."TINH_CHAT" = '1'
                                                OR (
                                                    F."TINH_CHAT" NOT IN ('0', '1')
                                                    AND F."GHI_NO_DAU_KY" + F."GHI_NO" - F."GHI_CO" < 0
                                                )
                                THEN F."GHI_CO" - F."GHI_NO_DAU_KY" - F."GHI_NO"
                                    ELSE 0
                                    END)               AS "GHI_CO_CUOI_KY"
                            FROM (
                                    SELECT
                                        A."SO_TAI_KHOAN"        AS "MA_TAI_KHOAN"
                                        , SUM(GL."GHI_NO_DAU_KY") AS "GHI_NO_DAU_KY"
                                        , SUM(GL."GHI_NO")        AS "GHI_NO"
                                        , SUM(GL."GHI_CO")        AS "GHI_CO"
                                        , SUM(GL."GHI_NO_LUY_KE") AS "GHI_NO_LUY_KE"
                                        , SUM(GL."GHI_CO_LUY_KE") AS "GHI_CO_LUY_KE"
                                        , CASE A."CHI_TIET_THEO_DOI_TUONG"
                                        WHEN FALSE
                                            THEN NULL
                                        ELSE GL."DOI_TUONG_ID"
                                        END                     AS "DOI_TUONG_ID"
                                        , A."TINH_CHAT"
                                        ,
                                        -- nmtruong 10/10/2015: nếu TK chi tiết theo ĐT và không bù trừ theo chi nhánh thì lấy lên chi nhánh để phân biệt
                                        CASE WHEN A."CHI_TIET_THEO_DOI_TUONG" = TRUE
                                                    AND IsSimilarBranch = 0
                                            THEN GL."CHI_NHANH_ID"
                                        ELSE NULL
                                        END                     AS "CHI_NHANH_ID"
                                    FROM TMP_SO_CAI_CHI_TIET_1 AS GL
                                        INNER JOIN danh_muc_he_thong_tai_khoan A ON GL."MA_TAI_KHOAN" = A."SO_TAI_KHOAN"
                                    WHERE GL."MA_TAI_KHOAN" NOT LIKE '0%'
                                        AND A."LA_TK_TONG_HOP" = FALSE
                                    GROUP BY A."SO_TAI_KHOAN",
                                        CASE A."CHI_TIET_THEO_DOI_TUONG"
                                        WHEN FALSE
                                            THEN NULL
                                        ELSE GL."DOI_TUONG_ID"
                                        END,
                                        A."TINH_CHAT",
                                        CASE WHEN A."CHI_TIET_THEO_DOI_TUONG" = TRUE
                                                AND IsSimilarBranch = 0
                                            THEN GL."CHI_NHANH_ID"
                                        ELSE NULL
                                        END
                                    HAVING SUM(GL."GHI_NO_DAU_KY") <> 0
                                            OR SUM(GL."GHI_NO") <> 0
                                            OR SUM(GL."GHI_CO") <> 0
                                ) AS F
                            GROUP BY F."MA_TAI_KHOAN",
                                F."TINH_CHAT"
                    ;

                    -- Lấy TK ngoại bảng cho QD 48
                    IF AccountingSystem = 48 AND SubAccountingSystem = 0
                    THEN
                        -- Lấy TK Ngoại bảng khác 007
                        INSERT INTO DU_LIEU_CHI_TIET (
                            SELECT
                                F."MA_TAI_KHOAN"
                                , ''                     AS "currency_id"
                                , 0                      AS "THU_TU"
                                , SUM(CASE WHEN F."TINH_CHAT" = '0'
                                                OR (
                                                    F."TINH_CHAT" NOT IN ('0', '1')
                                                    AND F."GHI_NO_DAU_KY" > 0
                                                )
                                THEN F."GHI_NO_DAU_KY"
                                    ELSE 0
                                    END)               AS "GHI_NO_DAU_KY"
                                , SUM(CASE WHEN F."TINH_CHAT" = '1'
                                                OR (
                                                    F."TINH_CHAT" NOT IN ('0', '1')
                                                    AND F."GHI_NO_DAU_KY" < 0
                                                )
                                THEN -1 * F."GHI_NO_DAU_KY"
                                    ELSE 0
                                    END)               AS "GHI_CO_DAU_KY"
                                , SUM(F."GHI_NO")        AS "GHI_NO"
                                , SUM(F."GHI_CO")        AS "GHI_CO"
                                , SUM(F."GHI_NO_LUY_KE") AS "GHI_NO_LUY_KE"
                                , SUM(F."GHI_CO_LUY_KE") AS "GHI_CO_LUY_KE"
                                , SUM(CASE WHEN F."TINH_CHAT" = '0'
                                                OR (
                                                    F."TINH_CHAT" NOT IN ('0', '1')
                                                    AND F."GHI_NO_DAU_KY" + F."GHI_NO" - F."GHI_CO" > 0
                                                )
                                THEN F."GHI_NO_DAU_KY" + F."GHI_NO" - F."GHI_CO"
                                    ELSE 0
                                    END)               AS "GHI_NO_DAU_KY"
                                , SUM(CASE WHEN F."TINH_CHAT" = '1'
                                                OR (
                                                    F."TINH_CHAT" NOT IN ('0', '1')
                                                    AND F."GHI_NO_DAU_KY" + F."GHI_NO" - F."GHI_CO" < 0
                                                )
                                THEN F."GHI_CO" - F."GHI_NO_DAU_KY" - F."GHI_NO"
                                    ELSE 0
                                    END)               AS "GHI_CO_DAU_KY"
                            FROM (
                                    SELECT
                                        A."SO_TAI_KHOAN"        AS "MA_TAI_KHOAN"
                                        , SUM(GL."GHI_NO_DAU_KY") AS "GHI_NO_DAU_KY"
                                        , SUM(GL."GHI_NO")        AS "GHI_NO"
                                        , SUM(GL."GHI_CO")        AS "GHI_CO"
                                        , SUM(GL."GHI_NO_LUY_KE") AS "GHI_NO_LUY_KE"
                                        , SUM(GL."GHI_CO_LUY_KE") AS "GHI_CO_LUY_KE"
                                        , CASE A."CHI_TIET_THEO_DOI_TUONG"
                                        WHEN FALSE
                                            THEN NULL
                                        ELSE GL."DOI_TUONG_ID"
                                        END                     AS "DOI_TUONG_ID"
                                        , A."TINH_CHAT"
                                    FROM TMP_SO_CAI_CHI_TIET_1 AS GL
                                        INNER JOIN danh_muc_he_thong_tai_khoan A ON GL."MA_TAI_KHOAN" = A."SO_TAI_KHOAN"
                                    WHERE GL."MA_TAI_KHOAN" LIKE '0%'
                                        AND GL."MA_TAI_KHOAN" NOT LIKE '007%'
                                        AND A."LA_TK_TONG_HOP" = FALSE
                                    GROUP BY A."SO_TAI_KHOAN",
                                        CASE A."CHI_TIET_THEO_DOI_TUONG"
                                        WHEN FALSE
                                            THEN NULL
                                        ELSE GL."DOI_TUONG_ID"
                                        END,
                                        A."TINH_CHAT"
                                    HAVING SUM(GL."GHI_NO_DAU_KY") <> 0
                                            OR SUM(GL."GHI_NO") <> 0
                                            OR SUM(GL."GHI_CO") <> 0
                                ) AS F
                            GROUP BY F."MA_TAI_KHOAN",
                                F."TINH_CHAT")
                        ;

                        -----------------Lấy lên ngoại tệ các loại--------------------
                        IF bac_tai_khoan > 1
                        THEN
                            INSERT INTO DU_LIEU_CHI_TIET (
                                SELECT
                                    F."MA_TAI_KHOAN"
                                    , F."currency_id"
                                    , F."THU_TU_TRONG_CHUNG_TU"
                                    , SUM(CASE WHEN F."TINH_CHAT" = '0'
                                                    OR (
                                                        F."TINH_CHAT" NOT IN ('0', '1')
                                                        AND F."GHI_NO_DAU_KY" > 0
                                                    )
                                    THEN F."GHI_NO_DAU_KY"
                                        ELSE 0
                                        END)               AS "GHI_NO_DAU_KY"
                                    , SUM(CASE WHEN F."TINH_CHAT" = '1'
                                                    OR (
                                                        F."TINH_CHAT" NOT IN ('0', '1')
                                                        AND F."GHI_NO_DAU_KY" < 0
                                                    )
                                    THEN -1 * F."GHI_NO_DAU_KY"
                                        ELSE 0
                                        END)               AS "GHI_CO_DAU_KY"
                                    , SUM(F."GHI_NO")        AS "GHI_NO"
                                    , SUM(F."GHI_CO")        AS "GHI_CO"
                                    , SUM(F."GHI_NO_LUY_KE") AS "GHI_NO_LUY_KE"
                                    , SUM(F."GHI_CO_LUY_KE") AS "GHI_CO_LUY_KE"
                                    , SUM(CASE WHEN F."TINH_CHAT" = '0'
                                                    OR (
                                                        F."TINH_CHAT" NOT IN ('0', '1')
                                                        AND F."GHI_NO_DAU_KY" + F."GHI_NO" - F."GHI_CO" > 0
                                                    )
                                    THEN F."GHI_NO_DAU_KY" + F."GHI_NO" - F."GHI_CO"
                                        ELSE 0
                                        END)               AS "GHI_NO_DAU_KY"
                                    , SUM(CASE WHEN F."TINH_CHAT" = '1'
                                                    OR (
                                                        F."TINH_CHAT" NOT IN ('0', '1')
                                                        AND F."GHI_NO_DAU_KY" + F."GHI_NO" - F."GHI_CO" < 0
                                                    )
                                    THEN F."GHI_CO" - F."GHI_NO_DAU_KY" - F."GHI_NO"
                                        ELSE 0
                                        END)               AS "GHI_CO_DAU_KY"
                                FROM (
                                        SELECT
                                            A."SO_TAI_KHOAN"                  AS "MA_TAI_KHOAN"
                                            , GL."currency_id"
                                            , COALESCE(Y."id", 1)               AS "THU_TU_TRONG_CHUNG_TU"
                                            , SUM(GL."GHI_NO_NGUYEN_TE_DAU_KY") AS "GHI_NO_DAU_KY"
                                            , SUM(GL."GHI_NO_NGUYEN_TE")        AS "GHI_NO"
                                            , SUM(GL."GHI_CO_NGUYEN_TE")        AS "GHI_CO"
                                            , SUM(GL."GHI_NO_LUY_KE")           AS "GHI_NO_LUY_KE"
                                            , SUM(GL."GHI_CO_LUY_KE")           AS "GHI_CO_LUY_KE"
                                            , CASE A."CHI_TIET_THEO_DOI_TUONG"
                                            WHEN FALSE
                                                THEN NULL
                                            ELSE GL."DOI_TUONG_ID"
                                            END                               AS "DOI_TUONG_ID"
                                            , A."TINH_CHAT"
                                        FROM TMP_SO_CAI_CHI_TIET_1 AS GL
                                            INNER JOIN danh_muc_he_thong_tai_khoan A ON GL."MA_TAI_KHOAN" = A."SO_TAI_KHOAN"
                                            INNER JOIN res_currency Y ON GL."currency_id" = Y.id
                                        WHERE GL."MA_TAI_KHOAN" LIKE '007%'
                                            AND A."LA_TK_TONG_HOP" = FALSE
                                            AND Y.id <> loai_tien_chinh
                                        GROUP BY A."SO_TAI_KHOAN",
                                            GL."currency_id",
                                            COALESCE(Y.id, 1),
                                            CASE A."CHI_TIET_THEO_DOI_TUONG"
                                            WHEN FALSE
                                                THEN NULL
                                            ELSE GL."DOI_TUONG_ID"
                                            END,
                                            A."TINH_CHAT"
                                        HAVING SUM(GL."GHI_NO_NGUYEN_TE_DAU_KY") <> 0
                                                OR SUM(GL."GHI_NO_NGUYEN_TE") <> 0
                                                OR SUM(GL."GHI_CO_NGUYEN_TE") <> 0
                                    ) AS F
                                GROUP BY F."MA_TAI_KHOAN",
                                    F."currency_id",
                                    F."TINH_CHAT",
                                    F."THU_TU_TRONG_CHUNG_TU"
                            )
                            ;
                        ELSE
                            INSERT INTO DU_LIEU_CHI_TIET (
                                SELECT
                                    F."MA_TAI_KHOAN"
                                    , F."currency_id"
                                    , F."THU_TU_TRONG_CHUNG_TU"
                                    , SUM(CASE WHEN F."TINH_CHAT" = '0'
                                                    OR (
                                                        F."TINH_CHAT" NOT IN ('0', '1')
                                                        AND F."GHI_NO_DAU_KY" > 0
                                                    )
                                    THEN F."GHI_NO_DAU_KY"
                                        ELSE 0
                                        END)               AS "GHI_NO_DAU_KY"
                                    , SUM(CASE WHEN F."TINH_CHAT" = '1'
                                                    OR (
                                                        F."TINH_CHAT" NOT IN ('0', '1')
                                                        AND F."GHI_NO_DAU_KY" < 0
                                                    )
                                    THEN -1 * F."GHI_NO_DAU_KY"
                                        ELSE 0
                                        END)               AS "GHI_CO_DAU_KY"
                                    , SUM(F."GHI_NO")        AS "GHI_NO"
                                    , SUM(F."GHI_CO")        AS "GHI_CO"
                                    , SUM(F."GHI_NO_LUY_KE") AS "GHI_NO_LUY_KE"
                                    , SUM(F."GHI_CO_LUY_KE") AS "GHI_CO_LUY_KE"
                                    , SUM(CASE WHEN F."TINH_CHAT" = '0'
                                                    OR (
                                                        F."TINH_CHAT" NOT IN ('0', '1')
                                                        AND F."GHI_NO_DAU_KY" + F."GHI_NO" - F."GHI_CO" > 0
                                                    )
                                    THEN F."GHI_NO_DAU_KY" + F."GHI_NO" - F."GHI_CO"
                                        ELSE 0
                                        END)               AS "GHI_NO_DAU_KY"
                                    , SUM(CASE WHEN F."TINH_CHAT" = '1'
                                                    OR (
                                                        F."TINH_CHAT" NOT IN ('0', '1')
                                                        AND F."GHI_NO_DAU_KY" + F."GHI_NO" - F."GHI_CO" < 0
                                                    )
                                    THEN F."GHI_CO" - F."GHI_NO_DAU_KY" - F."GHI_NO"
                                        ELSE 0
                                        END)               AS "GHI_CO_DAU_KY"
                                FROM (
                                        SELECT
                                            A."SO_TAI_KHOAN"                  AS "MA_TAI_KHOAN"
                                            , GL."currency_id"
                                            , COALESCE(Y.id, 1)                 AS "THU_TU_TRONG_CHUNG_TU"
                                            , --nmtruong 29/3/2016: sửa lỗi sắp xếp TK ngoại tệ 96231
                                            SUM(GL."GHI_NO_NGUYEN_TE_DAU_KY") AS "GHI_NO_DAU_KY"
                                            , SUM(GL."GHI_NO_NGUYEN_TE")        AS "GHI_NO"
                                            , SUM(GL."GHI_CO_NGUYEN_TE")        AS "GHI_CO"
                                            , SUM(GL."GHI_NO_LUY_KE")           AS "GHI_NO_LUY_KE"
                                            , SUM(GL."GHI_CO_LUY_KE")           AS "GHI_CO_LUY_KE"
                                            , CASE A."CHI_TIET_THEO_DOI_TUONG"
                                            WHEN FALSE
                                                THEN NULL
                                            ELSE GL."DOI_TUONG_ID"
                                            END                               AS "DOI_TUONG_ID"
                                            , A."TINH_CHAT"
                                        FROM TMP_SO_CAI_CHI_TIET_1 AS GL
                                            INNER JOIN danh_muc_he_thong_tai_khoan A ON GL."MA_TAI_KHOAN" = A."SO_TAI_KHOAN"
                                            INNER JOIN res_currency Y ON GL."currency_id" = Y.id
                                        WHERE GL."MA_TAI_KHOAN" LIKE '007%'
                                            AND A."LA_TK_TONG_HOP" = FALSE
                                            AND Y.id <> loai_tien_chinh
                                            AND A."LA_TK_TONG_HOP" = FALSE
                                        GROUP BY A."SO_TAI_KHOAN",
                                            GL."currency_id",
                                            COALESCE(Y.id, 1),
                                            CASE A."CHI_TIET_THEO_DOI_TUONG"
                                            WHEN FALSE
                                                THEN NULL
                                            ELSE GL."DOI_TUONG_ID"
                                            END,
                                            A."TINH_CHAT"
                                        HAVING SUM(GL."GHI_NO_NGUYEN_TE_DAU_KY") <> 0
                                                OR SUM(GL."GHI_NO_NGUYEN_TE") <> 0
                                                OR SUM(GL."GHI_CO_NGUYEN_TE") <> 0
                                    ) AS F
                                GROUP BY F."MA_TAI_KHOAN",
                                    F."currency_id",
                                    F."TINH_CHAT",
                                    F."THU_TU_TRONG_CHUNG_TU"
                            )
                            ;
                        END IF
                        ;
                    END IF
                    ;

                    -- Cộng lên tài khoản cha
                    INSERT INTO TMP_KET_QUA (
                        SELECT
                            A.id             AS "TAI_KHOAN_ID"
                            , A."CHI_TIET_THEO_DOI_TUONG"
                            , A."DOI_TUONG_SELECTION"
                            , A."SO_TAI_KHOAN" AS "MA_TAI_KHOAN"
                            , CASE WHEN D."currency_id" <> ''
                            THEN D."currency_id"
                            ELSE A."TEN_TAI_KHOAN"
                            END
                            , CASE WHEN D."currency_id" <> ''
                            THEN D."currency_id"
                            ELSE A."TEN_TIENG_ANH"
                            END
                            , A."TINH_CHAT"
                            , A."LA_TK_TONG_HOP"
                            , A.parent_id
                            , CASE WHEN A."SO_TAI_KHOAN" LIKE '007%'
                                        AND D."currency_id" IS NOT NULL
                                        AND D."currency_id" <> ''
                            THEN bac_tai_khoan + 1
                            ELSE A."BAC"
                            END              AS "BAC"
                            , CASE WHEN A."SO_TAI_KHOAN" LIKE '0%'
                            THEN 5
                            ELSE 0
                            END              AS "TINH_CHAT" -- Tài khoản trong bảng, tài khoản ngoài bảng
                            , D."THU_TU"
                            , SUM(D."GHI_NO_DAU_KY")
                            , SUM(D."GHI_CO_DAU_KY")
                            , SUM(D."GHI_NO")
                            , SUM(D."GHI_CO")
                            , SUM(D."GHI_NO_LUY_KE")
                            , SUM(D."GHI_CO_LUY_KE")
                            , SUM(D."GHI_NO_CUOI_KY")
                            , SUM(D."GHI_CO_CUOI_KY")
                        FROM DU_LIEU_CHI_TIET D
                            INNER JOIN danh_muc_he_thong_tai_khoan A ON D."MA_TAI_KHOAN" LIKE concat(A."SO_TAI_KHOAN", '%')
                        WHERE A."BAC" <= bac_tai_khoan
                        GROUP BY A.id,
                            A."CHI_TIET_THEO_DOI_TUONG",
                            A."DOI_TUONG_SELECTION",
                            A."SO_TAI_KHOAN",
                            CASE WHEN D."currency_id" <> ''
                                THEN D."currency_id"
                            ELSE A."TEN_TAI_KHOAN"
                            END,
                            CASE WHEN D."currency_id" <> ''
                                THEN D."currency_id"
                            ELSE A."TEN_TIENG_ANH"
                            END,
                            A."TINH_CHAT",
                            A."LA_TK_TONG_HOP",
                            A."LA_TK_TONG_HOP",
                            CASE WHEN A."SO_TAI_KHOAN" LIKE '007%'
                                    AND D."currency_id" IS NOT NULL
                                    AND D."currency_id" <> ''
                                THEN bac_tai_khoan + 1
                            ELSE A."BAC"
                            END,
                            CASE WHEN A."SO_TAI_KHOAN" LIKE '0%'
                                THEN 5
                            ELSE 0
                            END -- Tài khoản trong bảng, tài khoản ngoài bảng
                            ,
                            D."THU_TU"
                        HAVING SUM(D."GHI_NO_DAU_KY") <> 0
                            OR SUM(D."GHI_CO_DAU_KY") <> 0
                            OR SUM(D."GHI_NO") <> 0
                            OR SUM(D."GHI_CO") <> 0
                            OR SUM(D."GHI_NO_CUOI_KY") <> 0
                            OR SUM(D."GHI_CO_CUOI_KY") <> 0)
                    ;


                ELSE ------------Mẫu 1 bên ----------------------
                    DROP TABLE IF EXISTS TMP_SO_CAI_CHI_TIET
                    ;

                    CREATE TEMP TABLE TMP_SO_CAI_CHI_TIET
                        AS
                            SELECT
                                GL."MA_TAI_KHOAN"
                                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                                THEN GL."GHI_NO" - GL."GHI_CO"
                                    ELSE 0
                                    END) AS "GHI_NO_DAU_KY"
                                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                THEN (GL."GHI_NO")
                                    ELSE 0
                                    END) AS "GHI_NO"
                                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                THEN (GL."GHI_CO")
                                    ELSE 0
                                    END) AS "GHI_CO"
                                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ngay_bat_dau AND den_ngay
                                THEN (GL."GHI_NO")
                                    ELSE 0
                                    END) AS "GHI_NO_LUY_KE"
                                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ngay_bat_dau AND den_ngay
                                THEN (GL."GHI_CO")
                                    ELSE 0
                                    END) AS "GHI_CO_LUY_KE"
                            FROM so_cai_chi_tiet AS GL
                                INNER JOIN TBL_BRANCH OU ON GL."CHI_NHANH_ID" = OU."CHI_NHANH_ID"
                            WHERE GL."NGAY_HACH_TOAN" <= den_ngay
                                AND GL."MA_TAI_KHOAN" NOT LIKE '007 % '
                            GROUP BY GL."MA_TAI_KHOAN"
                    ;

                    ---------------------------------------------
                    DROP TABLE IF EXISTS TMP_SO_CAI_CHI_TIET_007
                    ;

                    CREATE TEMP TABLE TMP_SO_CAI_CHI_TIET_007
                        AS
                            SELECT
                                GL."MA_TAI_KHOAN"
                                , "TEN_LOAI_TIEN"
                                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" < tu_ngay
                                THEN GL."GHI_NO_NGUYEN_TE" - GL."GHI_CO_NGUYEN_TE"
                                    ELSE 0
                                    END) AS "GHI_NO_DAU_KY"
                                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                THEN (GL."GHI_NO_NGUYEN_TE")
                                    ELSE 0
                                    END) AS "GHI_NO"
                                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN tu_ngay AND den_ngay
                                THEN (GL."GHI_CO_NGUYEN_TE")
                                    ELSE 0
                                    END) AS "GHI_CO"
                                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ngay_bat_dau AND den_ngay
                                THEN (GL."GHI_NO_NGUYEN_TE")
                                    ELSE 0
                                    END) AS "GHI_NO_LUY_KE"
                                , SUM(CASE WHEN GL."NGAY_HACH_TOAN" BETWEEN ngay_bat_dau AND den_ngay
                                THEN (GL."GHI_CO_NGUYEN_TE")
                                    ELSE 0
                                    END) AS "GHI_CO_LUY_KE"
                            FROM so_cai_chi_tiet AS GL
                                INNER JOIN TBL_BRANCH OU ON GL."CHI_NHANH_ID" = OU."CHI_NHANH_ID"
                            WHERE GL."NGAY_HACH_TOAN" <= den_ngay
                                AND GL."MA_TAI_KHOAN" LIKE '007 % '
                            GROUP BY GL."MA_TAI_KHOAN",
                                "TEN_LOAI_TIEN"
                    ;

                    -----------------------------------
                    INSERT INTO TMP_KET_QUA (
                        SELECT
                            A.id                AS "TAI_KHOAN_ID"
                            , A."CHI_TIET_THEO_DOI_TUONG"
                            , A."DOI_TUONG_SELECTION"
                            , A."SO_TAI_KHOAN"    AS "MA_TAI_KHOAN"
                            , CASE WHEN F."TEN_LOAI_TIEN" <> ''
                            THEN F."TEN_LOAI_TIEN"
                            ELSE A."TEN_TAI_KHOAN"
                            END
                            , CASE WHEN F."TEN_LOAI_TIEN" <> ''
                            THEN F."TEN_LOAI_TIEN"
                            ELSE A."TEN_TIENG_ANH"
                            END
                            , A."TINH_CHAT"
                            , A."LA_TK_TONG_HOP"
                            , A.parent_id
                            , CASE WHEN A."SO_TAI_KHOAN" LIKE '007%'
                                        AND F."TEN_LOAI_TIEN" IS NOT NULL
                                        AND F."TEN_LOAI_TIEN" <> ''
                            THEN bac_tai_khoan + 1
                            ELSE A."BAC"
                            END                 AS "BAC"
                            , F."TINH_CHAT" -- Tài khoản trong bảng, tài khoản ngoài bảng
                            , F."THU_TU_TRONG_CHUNG_TU"
                            , (CASE WHEN A."TINH_CHAT" = '0'
                                        OR (
                                            A."TINH_CHAT" NOT IN ('0', '1')
                                            AND F."GHI_NO_DAU_KY" > 0
                                        )
                            THEN F."GHI_NO_DAU_KY"
                            ELSE 0
                            END)               AS "GHI_NO_DAU_KY"
                            , (CASE WHEN A."TINH_CHAT" = '1'
                                        OR (
                                            A."TINH_CHAT" NOT IN ('0', '1')
                                            AND F."GHI_NO_DAU_KY" < 0
                                        )
                            THEN -1 * F."GHI_NO_DAU_KY"
                            ELSE 0
                            END)               AS "GHI_CO_DAU_KY"
                            , (F."GHI_NO")        AS "GHI_NO"
                            , (F."GHI_CO")        AS "GHI_CO"
                            , (F."GHI_NO_LUY_KE") AS "GHI_NO_LUY_KE"
                            , (F."GHI_CO_LUY_KE") AS "GHI_CO_LUY_KE"
                            , (CASE WHEN A."TINH_CHAT" = '0'
                                        OR (
                                            A."TINH_CHAT" NOT IN ('0', '1')
                                            AND F."GHI_NO_DAU_KY" + F."GHI_NO" - F."GHI_CO" > 0
                                        )
                            THEN F."GHI_NO_DAU_KY" + F."GHI_NO" - F."GHI_CO"
                            ELSE 0
                            END)               AS "GHI_NO_DAU_KY"
                            , (CASE WHEN A."TINH_CHAT" = '1'
                                        OR (
                                            A."TINH_CHAT" NOT IN ('0', '1')
                                            AND F."GHI_NO_DAU_KY" + F."GHI_NO" - F."GHI_CO" < 0
                                        )
                            THEN F."GHI_CO" - F."GHI_NO_DAU_KY" - F."GHI_NO"
                            ELSE 0
                            END)               AS "GHI_CO_DAU_KY"
                        FROM (
                                -- Lấy chung cho QD15 và 48: Không có TK ngoại bảng
                                SELECT
                                    A.id                    AS "TAI_KHOAN_ID"
                                    , A."CHI_TIET_THEO_DOI_TUONG"
                                    , A."DOI_TUONG_SELECTION"
                                    , A."SO_TAI_KHOAN"        AS "MA_TAI_KHOAN"
                                    , ''                      AS "TEN_LOAI_TIEN"
                                    , 0                       AS "THU_TU_TRONG_CHUNG_TU"
                                    , SUM(GL."GHI_NO_DAU_KY") AS "GHI_NO_DAU_KY"
                                    , SUM(GL."GHI_NO")        AS "GHI_NO"
                                    , SUM(GL."GHI_CO")        AS "GHI_CO"
                                    , SUM(GL."GHI_NO_LUY_KE") AS "GHI_NO_LUY_KE"
                                    , SUM(GL."GHI_CO_LUY_KE") AS "GHI_CO_LUY_KE"
                                    , 0                       AS "TINH_CHAT"
                                FROM TMP_SO_CAI_CHI_TIET AS GL
                                    INNER JOIN danh_muc_he_thong_tai_khoan A ON GL."MA_TAI_KHOAN" LIKE A."SO_TAI_KHOAN" ||
                                                                                                        '%' -- Mẫu số dư 1 bên thì cộng luôn lên tài khoản cha
                                WHERE A."BAC" <= bac_tai_khoan
                                    AND GL."MA_TAI_KHOAN" NOT LIKE '0%'
                                    AND (
                                        GL."GHI_NO_DAU_KY" <> 0
                                        OR GL."GHI_NO" <> 0
                                        OR GL."GHI_CO" <> 0
                                    )
                                GROUP BY A.id,
                                    A."CHI_TIET_THEO_DOI_TUONG",
                                    A."DOI_TUONG_SELECTION",
                                    A."SO_TAI_KHOAN"
                                -- Lấy TK ngoại bảng cho QĐ48
                                UNION ALL
                                SELECT
                                    A.id                    AS "TAI_KHOAN_ID"
                                    , A."CHI_TIET_THEO_DOI_TUONG"
                                    , A."DOI_TUONG_SELECTION"
                                    , A."SO_TAI_KHOAN"        AS "MA_TAI_KHOAN"
                                    , ''                      AS "TEN_LOAI_TIEN"
                                    , 0                       AS "THU_TU_TRONG_CHUNG_TU"
                                    , SUM(GL."GHI_NO_DAU_KY") AS "GHI_NO_DAU_KY"
                                    , SUM(GL."GHI_NO")        AS "GHI_NO"
                                    , SUM(GL."GHI_CO")        AS "GHI_CO"
                                    , SUM(GL."GHI_NO_LUY_KE") AS "GHI_NO_LUY_KE"
                                    , SUM(GL."GHI_CO_LUY_KE") AS "GHI_CO_LUY_KE"
                                    , 5                       AS "TINH_CHAT"
                                FROM TMP_SO_CAI_CHI_TIET AS GL
                                    INNER JOIN danh_muc_he_thong_tai_khoan A ON GL."MA_TAI_KHOAN" LIKE A."SO_TAI_KHOAN" ||
                                                                                                        '%' -- Mẫu số dư 1 bên thì cộng luôn lên tài khoản cha
                                WHERE AccountingSystem = 48
                                    AND SubAccountingSystem = 0
                                    AND A."BAC" <= bac_tai_khoan
                                    AND GL."MA_TAI_KHOAN" LIKE '0%'
                                    AND GL."MA_TAI_KHOAN" NOT LIKE '007%'
                                    AND (
                                        GL."GHI_NO_DAU_KY" <> 0
                                        OR GL."GHI_NO" <> 0
                                        OR GL."GHI_CO" <> 0
                                    )
                                GROUP BY A.id,
                                    A."CHI_TIET_THEO_DOI_TUONG",
                                    A."DOI_TUONG_SELECTION",
                                    A."SO_TAI_KHOAN"
                                UNION ALL
                                SELECT
                                    A.id                    AS "TAI_KHOAN_ID"
                                    , A."CHI_TIET_THEO_DOI_TUONG"
                                    , A."DOI_TUONG_SELECTION"
                                    , A."SO_TAI_KHOAN"        AS "MA_TAI_KHOAN"
                                    , GL."TEN_LOAI_TIEN"
                                    , COALESCE(Y.id, 1)       AS "THU_TU_TRONG_CHUNG_TU"
                                    , SUM(GL."GHI_NO_DAU_KY") AS "GHI_NO_DAU_KY"
                                    , SUM(GL."GHI_NO")        AS "GHI_NO"
                                    , SUM(GL."GHI_CO")        AS "GHI_CO"
                                    , SUM(GL."GHI_NO_LUY_KE") AS "GHI_NO_LUY_KE"
                                    , SUM(GL."GHI_CO_LUY_KE") AS "GHI_CO_LUY_KE"
                                    , CASE WHEN A."SO_TAI_KHOAN" LIKE '0%'
                                    THEN 5
                                    ELSE 0
                                    END                     AS AccountKind
                                FROM TMP_SO_CAI_CHI_TIET_007 AS GL
                                    INNER JOIN danh_muc_he_thong_tai_khoan A ON GL."MA_TAI_KHOAN" LIKE A."SO_TAI_KHOAN" || '%'
                                    -- Mẫu số dư 1 bên thì cộng luôn lên tài khoản cha
                                    INNER JOIN res_currency Y ON GL."TEN_LOAI_TIEN" = Y."MA_LOAI_TIEN"
                                WHERE AccountingSystem = 48
                                    AND SubAccountingSystem = 0
                                    AND A."BAC" <= bac_tai_khoan
                                    AND GL."MA_TAI_KHOAN" LIKE '007%'
                                    AND (
                                        bac_tai_khoan = 1
                                        OR A."LA_TK_TONG_HOP" = FALSE
                                    )
                                    AND Y.id <> loai_tien_chinh
                                    AND (
                                        GL."GHI_NO_DAU_KY" <> 0
                                        OR GL."GHI_NO" <> 0
                                        OR GL."GHI_CO" <> 0
                                    )
                                GROUP BY A.id,
                                    A."CHI_TIET_THEO_DOI_TUONG",
                                    A."DOI_TUONG_SELECTION",
                                    A."SO_TAI_KHOAN",
                                    GL."TEN_LOAI_TIEN",
                                    COALESCE(Y.id, 1)
                            ) AS F
                            INNER JOIN danh_muc_he_thong_tai_khoan A ON F."MA_TAI_KHOAN" = A."SO_TAI_KHOAN")
                    ;

                END IF
                ;

                IF EXISTS(SELECT *
                        FROM TMP_KET_QUA A
                        WHERE A."MA_TAI_KHOAN" LIKE '007 % ')
                THEN
                    INSERT INTO TMP_KET_QUA (
                        SELECT
                            A.id             AS "TAI_KHOAN_ID"
                            , A."CHI_TIET_THEO_DOI_TUONG"
                            , A."DOI_TUONG_SELECTION"
                            , A."SO_TAI_KHOAN" AS "MA_TAI_KHOAN"
                            , A."TEN_TAI_KHOAN"
                            , A."TEN_TIENG_ANH"
                            , A."TINH_CHAT"
                            , 1                AS "LA_TK_TONG_HOP"
                            , A.parent_id
                            , A."BAC"
                            , 5                AS "TINH_CHAT" --Tài khoản trong bảng, tài khoản ngoài bảng
                            , 0                AS "THU_TU_TRONG_CHUNG_TU"
                            , NULL             AS "GHI_NO_DAU_KY"
                            , NULL                "GHI_CO_DAU_KY"
                            , NULL             AS "GHI_NO"
                            , NULL                "GHI_CO"
                            , NULL             AS "GHI_NO_LUY_KE"
                            , NULL             AS "GHI_CO_LUY_KE"
                            , NULL             AS "GHI_NO_DAU_KY"
                            , NULL             AS "GHI_CO_DAU_KY"
                        FROM danh_muc_he_thong_tai_khoan A
                        WHERE A."SO_TAI_KHOAN" LIKE '007 % '
                            AND A."BAC" <= bac_tai_khoan -- AND A.Isparent = 1
                    )
                    ;

                    -- Nếu không có dòng TK 007 nào là parent thì thêm chính TK 007
                    IF NOT EXISTS(SELECT *
                                FROM TMP_KET_QUA A
                                WHERE A."MA_TAI_KHOAN" LIKE '007')
                    THEN
                        INSERT INTO TMP_KET_QUA (
                            SELECT
                                A.id             AS "TAI_KHOAN_ID"
                                , A."CHI_TIET_THEO_DOI_TUONG"
                                , A."DOI_TUONG_SELECTION"
                                , A."SO_TAI_KHOAN" AS "MA_TAI_KHOAN"
                                , A."TEN_TAI_KHOAN"
                                , A."TEN_TIENG_ANH"
                                , A."TINH_CHAT"
                                , 1                AS "LA_TK_TONG_HOP"
                                , A.parent_id
                                , A."BAC"
                                , 5                AS "TINH_CHAT" --Tài khoản trong bảng, tài khoản ngoài bảng
                                , 0                AS "THU_TU_TRONG_CHUNG_TU"
                                , NULL             AS "GHI_NO_DAU_KY"
                                , NULL                "GHI_CO_DAU_KY"
                                , NULL             AS "GHI_NO"
                                , NULL                "GHI_CO"
                                , NULL             AS "GHI_NO_LUY_KE"
                                , NULL             AS "GHI_CO_LUY_KE"
                                , NULL             AS "GHI_NO_DAU_KY"
                                , NULL             AS "GHI_CO_DAU_KY"
                            FROM danh_muc_he_thong_tai_khoan A
                            WHERE A."SO_TAI_KHOAN" = '007'
                        )
                        ;

                    END IF
                    ;

                END IF
                ;

            RETURN QUERY SELECT *
                        FROM TMP_KET_QUA
            ;

            END
            ;
            $$ LANGUAGE PLpgSQL
            ;
		""")

class BAO_CAO_BANG_CAN_DOI_TAI_KHOAN_REPORT(models.AbstractModel):
    _name = 'report.bao_cao.template_bang_can_doi_tai_khoan'

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