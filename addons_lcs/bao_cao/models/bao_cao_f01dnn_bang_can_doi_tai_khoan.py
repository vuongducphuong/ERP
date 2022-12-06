# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_F01DNN_BANG_CAN_DOI_TAI_KHOAN(models.Model):
    _name = 'bao.cao.f01dnn.bang.can.doi.tai.khoan'
    
    _auto = False

    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TU_NGAY = fields.Date(string='Từ', help='Từ ngày ',required=True ,default=fields.Datetime.now)
    DEN_NGAY = fields.Date(string='Đến', help='Đến ngày',required=True,default=fields.Datetime.now)
    BAC_TAI_KHOAN = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ], string='Bậc tài khoản', help='Bậc tài khoản',default='1',required=True)
    HIEN_THI_SO_DU_HAI_BEN = fields.Boolean(string='Hiển thị số dư 2 bên', help='Hiển thị số dư hai bên')
    LAY_DU_LIEU_TU_BAO_CAO_TAI_CHINH_DA_LAP = fields.Boolean(string='Lấy dữ liệu từ báo cáo tài chính đã lập', help='Lấy dữ liệu từ báo cáo tài chính đã lập')
    SO_HIEU_TAI_KHOAN = fields.Char(string='Số hiệu tài khoản', help='Số hiệu tài khoản')
    TEN_TAI_KHOAN = fields.Char(string='Tên tài khoản', help='Tên tài khoản')
    NO_SO_DU_DAU_KY = fields.Float(string='Nợ', help='Nợ số dư đầu kỳ',digits= decimal_precision.get_precision('VND'))
    CO_SO_DU_DAU_KY = fields.Float(string='Có', help='Có số dư đầu kỳ',digits= decimal_precision.get_precision('VND'))
    NO_SO_PHAT_SINH_TRONG_KY = fields.Float(string='Nợ', help='Nợ số phát sinh trong kỳ',digits= decimal_precision.get_precision('VND'))
    CO_SO_PHAT_SINH_TRONG_KY = fields.Float(string='Có', help='Có số phát sinh trong kỳ',digits= decimal_precision.get_precision('VND'))
    NO_SO_DU_CUOI_KY = fields.Float(string='Nợ', help='Nợ số dư cuối kỳ',digits= decimal_precision.get_precision('VND'))
    CO_SO_DU_CUOI_KY = fields.Float(string='Có', help='Có số dư cuối kỳ',digits= decimal_precision.get_precision('VND'))
    BAC = fields.Integer(string='Bậc', help='Bậc')
    name = fields.Char(string='Name', help='Name', oldname='NAME')


    #FIELD_IDS = fields.One2many('model.name')
    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU_NGAY', 'DEN_NGAY')
    ### START IMPLEMENTING CODE ###
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        # Execute SQL query here
        if not params.get('active_model'):
            return
        # Execute SQL query here
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        HIEN_THI_SO_DU_HAI_BEN = 1 if 'HIEN_THI_SO_DU_HAI_BEN' in params.keys() and params['HIEN_THI_SO_DU_HAI_BEN'] != 'False' else 0
        LAY_DU_LIEU_TU_BAO_CAO_TAI_CHINH_DA_LAP = 1 if 'LAY_DU_LIEU_TU_BAO_CAO_TAI_CHINH_DA_LAP' in params.keys() and params['LAY_DU_LIEU_TU_BAO_CAO_TAI_CHINH_DA_LAP'] != 'False' else 0
        CHI_NHANH_ID =  self.get_chi_nhanh() # vì form không có tham số chi nhánh nên phải lấy mặc định chi nhánh
        BAC_TAI_KHOAN = params['BAC_TAI_KHOAN'] if 'BAC_TAI_KHOAN' in params.keys() and params['BAC_TAI_KHOAN'] != 'False' else None

        params_sql = {
            'TU_NGAY':TU_NGAY_F, 
            'DEN_NGAY':DEN_NGAY_F,
            'HIEN_THI_SO_DU_HAI_BEN':HIEN_THI_SO_DU_HAI_BEN,
            'LAY_DU_LIEU_TU_BAO_CAO_TAI_CHINH_DA_LAP':LAY_DU_LIEU_TU_BAO_CAO_TAI_CHINH_DA_LAP,
            'CHI_NHANH_ID':CHI_NHANH_ID,
            'BAC_TAI_KHOAN':int(BAC_TAI_KHOAN),
            'limit': limit,
            'offset': offset,
        }
        query = """DO LANGUAGE plpgsql $$
                DECLARE
                chi_nhanh                     INTEGER := %(CHI_NHANH_ID)s;  --Chi nhánh

                bao_gom_chi_nhanh_phu_thuoc   INTEGER := 0;  --Lấy số liệu chi nhánh phụ thuộc

                tu_ngay                       DATE := %(TU_NGAY)s;  -- Đến ngày

                den_ngay                      DATE := %(DEN_NGAY)s;  --Từ ngày

                bac_tai_khoan                 INTEGER := %(BAC_TAI_KHOAN)s;   --Bậc tài khoản

                lay_so_lieu_tu_bao_cao_da_lap INTEGER := %(LAY_DU_LIEU_TU_BAO_CAO_TAI_CHINH_DA_LAP)s; --Lấy số liệu từ báo cáo tài chính đã lập

                IsBalanceBothSide             INTEGER := %(HIEN_THI_SO_DU_HAI_BEN)s;  -- Hiển thị số dư hai bên

                IsSimilarBranch               INTEGER := 0;


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
                            "TEN_TAI_KHOAN" AS "TEN_TAI_KHOAN",
                            "GHI_NO_DAU_KY" AS "NO_SO_DU_DAU_KY",
                            "GHI_CO_DAU_KY" AS "CO_SO_DU_DAU_KY",
                            "GHI_NO" AS "NO_SO_PHAT_SINH_TRONG_KY",
                            "GHI_CO" AS "CO_SO_PHAT_SINH_TRONG_KY",
                            "GHI_NO_CUOI_KY" AS "NO_SO_DU_CUOI_KY",
                            "GHI_CO_CUOI_KY" AS "CO_SO_DU_CUOI_KY",
                            "BAC"
                           
                FROM TMP_KET_QUA1
                OFFSET %(offset)s
                LIMIT %(limit)s;
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
                tong_no_dau_ky += line.get('NO_SO_DU_DAU_KY')
                tong_co_dau_ky += line.get('CO_SO_DU_DAU_KY')
                tong_phat_sinh_no += line.get('NO_SO_PHAT_SINH_TRONG_KY')
                tong_phat_sinh_co += line.get('CO_SO_PHAT_SINH_TRONG_KY')
                tong_cuoi_ky_no += line.get('NO_SO_DU_CUOI_KY')
                tong_cuoi_ky_co += line.get('CO_SO_DU_CUOI_KY')
        dict_dong_them = {
            'SO_HIEU_TAI_KHOAN' : '',
            'TEN_TAI_KHOAN' : 'Cộng',
            'NO_SO_DU_DAU_KY' : tong_no_dau_ky,
            'CO_SO_DU_DAU_KY' : tong_co_dau_ky,
            'NO_SO_PHAT_SINH_TRONG_KY' : tong_phat_sinh_no,
            'CO_SO_PHAT_SINH_TRONG_KY' : tong_phat_sinh_co,
            'NO_SO_DU_CUOI_KY' : tong_cuoi_ky_no,
            'CO_SO_DU_CUOI_KY' : tong_cuoi_ky_co,
            'BAC' : 1,
        }
        du_lieu_ids.append(dict_dong_them)
        return du_lieu_ids

    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        # self._validate()
        action = self.env.ref('bao_cao.open_report_f01dnn_bang_can_doi_tai_khoan').read()[0]
        action['options'] = {'clear_breadcrumbs': True}
        return action

class BAO_CAO_F01DNN_BANG_CAN_DOI_TAI_KHOAN_REPORT(models.AbstractModel):
    _name = 'report.bao_cao.template_f01dnn_bang_can_doi_tai_khoan'

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