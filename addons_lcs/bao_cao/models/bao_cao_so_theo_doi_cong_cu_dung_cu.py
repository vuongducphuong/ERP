# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_SO_THEO_DOI_CONG_CU_DUNG_CU(models.Model):
    _name = 'bao.cao.so.theo.doi.cong.cu.dung.cu'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phục vụ', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default='DAU_THANG_DEN_HIEN_TAI',required='True')
    TU = fields.Date(string='Từ', help='Từ',default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến',default=fields.Datetime.now)
    LOAI_CCDC_ID = fields.Many2one('danh.muc.loai.cong.cu.dung.cu', string='Loại CCDC', help='Loại công cụ dụng cụ')
    LOAI_CONG_CU_DUNG_CU = fields.Char(string='Loại CCDC', help='Loại công cụ dụng cụ')
    MA_CCDC = fields.Char(string='Mã CCDC', help='Mã công cụ dụng cụ')
    TEN_CCDC = fields.Char(string='Tên CCDC', help='Tên công cụ dụng cụ')
    LY_DO_GHI_TANG = fields.Char(string='Lý do ghi tăng', help='Lý do ghi tăng')
    NGAY_GHI_TANG = fields.Date(string='Ngày ghi tăng', help='Ngày ghi tăng')
    SO_CT_GHI_TANG = fields.Char(string='Sổ CT ghi tăng', help='Sổ chứng từ ghi tăng')
    SO_KY_PHAN_BO = fields.Float(string='Số kỳ phân bổ', help='Số kỳ phân bổ',digits=decimal_precision.get_precision('VND'))
    SO_KY_PHAN_BO_CON_LAI = fields.Float(string='Số kỳ PB còn lại', help='Số kỳ phân bổ còn lại',digits=decimal_precision.get_precision('VND'))
    DVT = fields.Char(string='ĐVT', help='Đơn vị tính')
    LUY_KE_SL_DA_GIAM = fields.Float(string='Lũy kế SL đã giảm', help='Lũy kế số lượng đã giảm')
    SL_CON_LAI = fields.Float(string='SL còn lại', help='Số lượng còn lại',digits=decimal_precision.get_precision('VND'))
    GIA_TRI_CCDC = fields.Float(string='Giá trị CCDC', help='Giá trị công cụ dụng cụ',digits=decimal_precision.get_precision('VND'))
    GIA_TRI_PB_HANG_KY = fields.Float(string='Giá trị PB hàng kỳ', help='Giá trị phân bổ hàng kỳ',digits=decimal_precision.get_precision('VND'))
    PHAN_BO_TRONG_KY = fields.Float(string='Phân bổ trong kỳ', help='Phân bổ trong kỳ',digits=decimal_precision.get_precision('VND'))
    LUY_KE_DA_PB = fields.Float(string='Lũy kế đã PB', help='Lũy kế đã PB',digits=decimal_precision.get_precision('VND'))
    GIA_TRI_CON_LAI = fields.Float(string='Giá trị còn lại', help='Giá trị còn lại',digits=decimal_precision.get_precision('VND'))
    SO_TAI_KHOAN = fields.Char( string='TK chờ phân bổ', help='Tài khoản chờ phân bổ')
    SO_LUONG_GHI_TANG = fields.Float(string='SL ghi tăng', help='Số lượng ghi tăng', digits=decimal_precision.get_precision('SO_LUONG'))
    name = fields.Char(string='Name', oldname='NAME')

    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')


    #FIELD_IDS = fields.One2many('model.name')

    ### START IMPLEMENTING CODE ###
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_SO_THEO_DOI_CONG_CU_DUNG_CU, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        cong_cu_dung_cu = self.env['danh.muc.loai.cong.cu.dung.cu'].search([],limit=1)
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        if cong_cu_dung_cu:
            result['LOAI_CCDC_ID'] = cong_cu_dung_cu.id
        return result

    def _validate(self):
        params = self._context
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        if(TU=='False'):
            raise ValidationError('<Từ> không được bỏ trống.')
        elif(DEN=='False'):
            raise ValidationError('<Đến> không được bỏ trống.')
        # comment do đã nhập từ ngày nhỏ hơn đến ngày nhưng vẫn báo
        # elif(TU > DEN):
        #     raise ValidationError('<Đến> phải lớn hơn hoặc bằng <Từ>.')
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else -1 
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] else 0
        KY_BAO_CAO = params['KY_BAO_CAO'] if 'KY_BAO_CAO' in params.keys() else 'False'
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        LOAI_CCDC_ID = params['LOAI_CCDC_ID'] if 'LOAI_CCDC_ID' in params.keys() and params['LOAI_CCDC_ID'] != 'False' else -1 
        if LOAI_CCDC_ID == 'False':
          MA_PHAN_CAP = ''
        else:
          pc = self.env['danh.muc.loai.cong.cu.dung.cu'].search([('id', '=', LOAI_CCDC_ID)],limit=1).MA_PHAN_CAP
          if pc:
            MA_PHAN_CAP = pc
          else:
            MA_PHAN_CAP = ''
        MA_PC = str(MA_PHAN_CAP) + '%'

        paramSQL = {
            'CHI_NHANH_ID':CHI_NHANH_ID, 
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC, 
            'KY_BAO_CAO':KY_BAO_CAO, 
            'TU':TU, 
            'DEN':DEN, 
            'LOAI_CCDC_ID':LOAI_CCDC_ID,
            'MA_PHAN_CAP' : MA_PC,
            }      
        # Execute SQL query here
        cr = self.env.cr
        query = """
        DO LANGUAGE plpgsql $$
              DECLARE

                CHI_NHANH_ID                        INTEGER :=%(CHI_NHANH_ID)s;
                TU                                  DATE := %(TU)s;
                DEN                                 DATE := %(DEN)s;
                LOAI_CCDC_ID                        INTEGER := %(LOAI_CCDC_ID)s;
                BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC INTEGER :=%(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

                rec                                 RECORD;
                MA_PHAN_CAP_DON_VI                  VARCHAR(100);
                MA_PHAN_CAP_LOAI_CCDC               VARCHAR(100);
                NGAY_BAT_DAU_NAM_TC                 DATE;


              BEGIN
                SELECT "MA_PHAN_CAP"
                INTO MA_PHAN_CAP_LOAI_CCDC
                FROM danh_muc_loai_cong_cu_dung_cu SC
                WHERE id = LOAI_CCDC_ID;

                SELECT "value"
                INTO NGAY_BAT_DAU_NAM_TC
                FROM ir_config_parameter
                WHERE KEY = 'he_thong.TU_NGAY_BAT_DAU_TAI_CHINH';

                DROP TABLE IF EXISTS TMP_KET_QUA_CUOI_CUNG;
                CREATE TEMP TABLE TMP_KET_QUA_CUOI_CUNG
                  AS

                    SELECT
                      ROW_NUMBER()
                      OVER (
                        ORDER BY SUI."NGAY_GHI_TANG", SUI."MA_CCDC" )                        AS RowNum,
                      SUI.id                                                                 AS "ID_CHUNG_TU",
                      SUI."LOAI_CHUNG_TU",

                      -- Mã CCDC
                      SUI."MA_CCDC",
                      -- Tên CCDC
                      SUI."TEN_CCDC",
                      --Loại CCDC
                      SUC."TEN"                                                              AS "TEN_LOAI_CCDC",
                      SUI."NHOM_CCDC"                                                        AS "MA_LOAI_CCDC",
                      --nvtoan add 13/07/2017
                      SUI."NGAY_GHI_TANG",
                      -- Ngày ghi tăng
                      SUI."SO_CT_GHI_TANG",
                      -- Số CT ghi tăng
                      SUI."LY_DO_GHI_TANG",

                      -- Lý do ghi tăng
                      --Số kỳ phân bổ trên ghi tăng hoặc khai báo CCDC đầu kỳ + Chênh lệch điều chỉnh số kỳ phân bổ còn lại trên chứng từ điều chỉnh có ngày điều chỉnh <= Đến ngày của kỳ báo cáo
                      SUI."SO_KY_PHAN_BO" + SUM(CASE WHEN SL."LOAI_CHUNG_TU" <> '454'
                        THEN 0
                                                ELSE SL."SO_KY_PHAN_BO_GHI_TANG"
                                                    - SL."SO_KY_PHAN_BO_GHI_GIAM"
                                                END)                                         AS "SO_KY_PHAN_BO",
                      -- Số kỳ phân bổ
                      --Số kỳ PB còn lại = Số kỳ phân bổ trên khai cáo chi tiết CCDC còn lại – Số tháng đã phân bổ (căn cứ vào chứng từ phân bổ có ngày hạch toán <= đến ngày của kỳ báo cáo) + Chênh lệch điều chỉnh số kỳ phân bổ còn lại trên chứng từ điều chỉnh có ngày điều chỉnh <= Đến ngày của kỳ báo cáo

                      CASE WHEN COALESCE(SUI."SO_KY_PB_CON_LAI", 0)  -- Lấy tạm trường này do chưa có trường SO_KY_PHAN_BO_CON_LAI
                                + SUM(CASE WHEN SL."LOAI_CHUNG_TU" = '450'
                                                OR SL."LOAI_CHUNG_TU" = '457'
                        THEN 0
                                      ELSE COALESCE(SL."SO_KY_PHAN_BO_GHI_TANG", 0)
                                          - COALESCE(SL."SO_KY_PHAN_BO_GHI_GIAM", 0)
                                      END) < 0
                        THEN 0
                      --ELSE SUI."SO_KY_PHAN_BO_CON_LAI"
                      ELSE COALESCE(SUI."SO_KY_PB_CON_LAI", 0)
                          + SUM(CASE WHEN SL."LOAI_CHUNG_TU" = '450'
                                          OR SL."LOAI_CHUNG_TU" = '457'
                        THEN 0
                                ELSE COALESCE(SL."SO_KY_PHAN_BO_GHI_TANG", 0)
                                      - COALESCE(SL."SO_KY_PHAN_BO_GHI_GIAM", 0)
                                END)
                      END                                                                    AS "SO_KY_PHAN_BO_CON_LAI",
                      -- Số kỳ phân bổ còn lại
                      SUI."DON_VI_TINH",
                      SUI."SO_LUONG",
                      -- Số lượng ghi tăng
                      SUM(CASE WHEN SL."NGAY_HACH_TOAN" < TU
                                    OR SL."LOAI_CHUNG_TU" <> '452'
                        THEN 0
                          ELSE SL."SO_LUONG_GHI_GIAM"
                          END)                                                               AS "SO_LUONG_GHI_GIAM",
                      -- Số lượng giảm trong kỳ
                      SUM(CASE WHEN SL."LOAI_CHUNG_TU" <> '452'
                        THEN 0
                          ELSE SL."SO_LUONG_GHI_GIAM"
                          END)                                                               AS "SO_LUONG_GHI_GIAM_LUY_KE",
                      -- Số lượng giảm lũy kế
                      SUI."SO_LUONG" - SUM(CASE WHEN SL."LOAI_CHUNG_TU" <> '452'
                        THEN 0
                                          ELSE SL."SO_LUONG_GHI_GIAM"
                                          END)                                              AS "SO_LUONG_CON_LAI",
                      -- SL còn lại
                      SUI."THANH_TIEN" + SUM(CASE WHEN SL."LOAI_CHUNG_TU" <> '454'
                        THEN 0
                                            ELSE SL."SO_TIEN_GHI_TANG"
                                                  - SL."SO_TIEN_GHI_GIAM"
                                            END)                                            AS "SO_TIEN",
                      COALESCE(SL2."SO_TIEN_PHAN_BO_HANG_KY", SUI."SO_TIEN_PHAN_BO_HANG_KY") AS "SO_TIEN_PHAN_BO_HANG_KY",
                      -- Giá trị PB hàng kỳ (tạm)
                      --         SELECT coalesce(SL2."SO_TIEN_PHAN_BO_HANG_KY", SUI."SO_TIEN_PHAN_BO_HANG_KY", 'Empty') AS "SO_TIEN_PHAN_BO_HANG_KY",
                      SUM(CASE WHEN SUI."SO_KY_PHAN_BO" = 1
                        THEN 0 -- SL."SO_TIEN_PHAN_BO"
                          WHEN SL."NGAY_HACH_TOAN" < TU
                              OR SL."LOAI_CHUNG_TU" <> '453'
                            THEN 0
                          ELSE SL."SO_TIEN_PHAN_BO"
                          END)                                                               AS "SO_TIEN_PHAN_BO",
                      -- Phân bổ trong kỳ
                      SUM(CASE WHEN SUI."SO_KY_PHAN_BO" = 1
                        THEN SL."SO_TIEN_PHAN_BO"
                          WHEN SL."LOAI_CHUNG_TU" <> '453'
                              AND SL."LOAI_CHUNG_TU" <> '457'
                              AND SL."LOAI_CHUNG_TU" <> '450'
                            THEN 0
                          ELSE SL."SO_TIEN_PHAN_BO"
                          END)                                                               AS "SO_TIEN_PHAN_BO_LUY_KE",
                      -- Lũy kế phân bổ
                      CASE WHEN SUI."SO_KY_PHAN_BO" = 1
                        THEN 0
                      ELSE SUI."THANH_TIEN" + SUM(CASE WHEN SL."LOAI_CHUNG_TU" <> '454'
                        THEN 0
                                                  ELSE SL."SO_TIEN_GHI_TANG"
                                                      - SL."SO_TIEN_GHI_GIAM"
                                                  END)
                          - SUM(CASE WHEN SL."LOAI_CHUNG_TU" <> '453'
                                          AND SL."LOAI_CHUNG_TU" <> '457'
                        THEN 0
                                ELSE SL."SO_TIEN_PHAN_BO"
                                END)
                      END                                                                    AS "SO_TIEN_CON_LAI",
                      -- Giá trị còn lại
                      TK."SO_TAI_KHOAN",
                      -- Tài khoản chờ phân bổ
                      SUI."id"                                                               AS "ID_GOC",
                      'supply.ghi.tang'                                                      AS "MODEL_GOC"

                    FROM supply_ghi_tang SUI
                      INNER JOIN so_ccdc_chi_tiet SL ON SL."CCDC_ID" = SUI.id
                      LEFT JOIN danh_muc_loai_cong_cu_dung_cu SUC ON SUC.id = SUI."LOAI_CCDC_ID"
                      INNER JOIN danh_muc_to_chuc OU ON SUI."CHI_NHANH_ID" = OU.id
                      --         --Giá trị phân bổ hàng kỳ
                      LEFT JOIN LATERAL ( SELECT SL2."SO_TIEN_PHAN_BO_HANG_KY"
                                          FROM so_ccdc_chi_tiet SL2
                                          WHERE SL2."CCDC_ID" = SL."CCDC_ID"
                                                AND SL2."NGAY_HACH_TOAN" <= DEN
                                                AND SL2."LOAI_CHUNG_TU" IN ('450', '454', '457')
                                          ORDER BY SL2."NGAY_HACH_TOAN" DESC,
                                            SL2."THU_TU_TRONG_CHUNG_TU" DESC
                                          FETCH FIRST 1 ROW ONLY

                                ) SL2 ON TRUE
                      --Giá trị phân bổ hàng kỳ


                      -- Lấy chứng từ ghi giảm cuối cùng
                      LEFT JOIN LATERAL (
                                SELECT SL2."NGAY_HACH_TOAN"
                                FROM so_ccdc_chi_tiet SL2
                                WHERE SL2."CCDC_ID" = SL."CCDC_ID"
                                      AND SL2."NGAY_HACH_TOAN" <= DEN
                                      AND SL2."LOAI_CHUNG_TU" = '452'
                                ORDER BY SL2."NGAY_HACH_TOAN" DESC,
                                  SL2."THU_TU_TRONG_CHUNG_TU" DESC
                                FETCH FIRST 1 ROW ONLY
                                ) AS SL3 ON TRUE
                      LEFT JOIN danh_muc_he_thong_tai_khoan TK ON SUI."TK_CHO_PHAN_BO_ID" = TK.id
                    WHERE SL."NGAY_HACH_TOAN" <= DEN
                          AND (LOAI_CCDC_ID = -1
                              OR
                              SUC."MA_PHAN_CAP" LIKE MA_PHAN_CAP_LOAI_CCDC
                          )
                          AND (OU.id = CHI_NHANH_ID
                              OR
                              (BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1
                                AND OU."HACH_TOAN_SELECTION" = 'PHU_THUOC'
                              )
                          )

                    GROUP BY SUI.id,
                      --SUI."LOAI_CHUNG_TU",
                      SUI.id,
                      SUI."MA_CCDC",
                      SUI."TEN_CCDC",
                      SUC."TEN",
                      SUI."LY_DO_GHI_TANG",
                      --SUC."LOAI_CCDC",
                      SUI."NHOM_CCDC", --nvtoan add 13/07/2017
                      SUI."NGAY_GHI_TANG",
                      SUI."SO_CT_GHI_TANG",
                      SUI."SO_KY_PHAN_BO",

                      SUI."SO_KY_PB_CON_LAI",
                      SUI."DON_VI_TINH",
                      SUI."SO_LUONG",
                      SUI."THANH_TIEN",
                      COALESCE(SL2."SO_TIEN_PHAN_BO_HANG_KY", SUI."SO_TIEN_PHAN_BO_HANG_KY"),
                      TK."SO_TAI_KHOAN",
                      SL3."NGAY_HACH_TOAN"
                    --          SL."ID_CHUNG_TU",
                    --          SL."MODEL_CHUNG_TU"
                    --OU."TEN_DON_VI"
                    HAVING --nvtoan modify 04/04/2016: Sửa lỗi số lượng CCDC còn trong kỳ nhưng không lên báo cáo (Error 97527)
                      (SUI."SO_LUONG" - SUM(CASE WHEN SL."LOAI_CHUNG_TU" <> '452'
                        THEN 0
                                            ELSE CASE WHEN SL."NGAY_HACH_TOAN" < TU
                                              THEN SL."SO_LUONG_GHI_GIAM"
                                                ELSE 0
                                                END
                                            END) > 0)
                      OR SL3."NGAY_HACH_TOAN" BETWEEN TU AND DEN;

              END $$;

              SELECT *
              FROM TMP_KET_QUA_CUOI_CUNG;

              """
        cr.execute(query,paramSQL)
        # Get and show result
        for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
            record.append({
                'MA_CCDC': line.get('MA_CCDC', ''),
                'TEN_CCDC': line.get('TEN_CCDC', ''),
                'LY_DO_GHI_TANG': line.get('LY_DO_GHI_TANG', ''),
                'NGAY_GHI_TANG': line.get('NGAY_GHI_TANG', ''),
                'SO_CT_GHI_TANG': line.get('SO_CT_GHI_TANG', ''),
                'SO_KY_PHAN_BO': line.get('SO_KY_PHAN_BO', ''),
                'SO_KY_PHAN_BO_CON_LAI': line.get('SO_KY_PHAN_BO_CON_LAI', ''),
                'DVT': line.get('DON_VI_TINH', ''),
                'SO_LUONG_GHI_TANG': line.get('SO_LUONG', ''),
                'LUY_KE_SL_DA_GIAM': line.get('SO_LUONG_GHI_GIAM_LUY_KE', ''),
                'SL_CON_LAI': line.get('SO_LUONG_CON_LAI', ''),
                'GIA_TRI_CCDC': line.get('SO_TIEN', ''),
                'GIA_TRI_PB_HANG_KY': line.get('SO_TIEN_PHAN_BO_HANG_KY', ''),
                'PHAN_BO_TRONG_KY': line.get('SO_TIEN_PHAN_BO', ''),
                'LUY_KE_DA_PB': line.get('SO_TIEN_PHAN_BO_LUY_KE', ''),
                'GIA_TRI_CON_LAI': line.get('SO_TIEN_CON_LAI', ''),
                'SO_TAI_KHOAN': line.get('SO_TAI_KHOAN', ''),
                'name': line.get('', ''),
                'ID_GOC': line.get('ID_GOC', ''),
                'MODEL_GOC': line.get('MODEL_GOC', ''),
                'LOAI_CONG_CU_DUNG_CU': line.get('TEN_LOAI_CCDC', ''),
                })
        return record

    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU')
        DEN_NGAY_F = self.get_vntime('DEN')
        param = 'Từ ngày %s đến ngày %s' % (TU_NGAY_F, DEN_NGAY_F)
        action = self.env.ref('bao_cao.open_report_so_theo_doi_cong_cu_dung_cu').read()[0]
        action['context'] = eval(action.get('context','{}').replace('\n',''))
        action['context'].update({'breadcrumb_ex': param})
        return action
    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')