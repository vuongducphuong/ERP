# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_SO_NHAT_KY_CHUNG(models.Model):
    _name = 'bao.cao.so.nhat.ky.chung'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh', required='True')
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='true')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default='DAU_THANG_DEN_HIEN_TAI', required='True')
    TU = fields.Date(string='Từ', help='Từ',default=fields.Datetime.now, required='True')
    DEN = fields.Date(string='Đến', help='Đến',default=fields.Datetime.now, required='True')
    CONG_GOP_CAC_NUT_GIONG_NHAU = fields.Boolean(string='Cộng gộp các nút giống nhau', help='Cộng gộp các nút giống nhau')
    HIEN_THI_SO_LUY_KE_KY_TRUOC_CHUYEN_SANG = fields.Boolean(string='Hiển thị số lũy kế kỳ trước chuyển sang', help='Hiển thị số lũy kế kỳ trước chuyển sang')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hoạch toán', help='Ngày hoạch toán')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TAI_KHOAN = fields.Char(string='Tài khoản', help='Tài khoản')
    TK_DOI_UNG = fields.Char(string='TK đối ứng', help='Tài khoản đối ứng')
    PHAT_SINH_NO = fields.Float(string='Phát sinh nợ', help='Phát sinh nợ',digits=decimal_precision.get_precision('VND'))
    PHAT_SINH_CO = fields.Float(string='Phát sinh có', help='Phát sinh có',digits=decimal_precision.get_precision('VND'))

    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')

	
    @api.onchange('NGAY_HACH_TOAN')
    def _onchange_NGAY_HACH_TOAN(self):
        if self.NGAY_CHUNG_TU:
            self.NGAY_CHUNG_TU = self.NGAY_HACH_TOAN

    #FIELD_IDS = fields.One2many('model.name')
    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')

    def _validate(self):
        params = self._context
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        TU = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

        if(TU=='False'):
            raise ValidationError('<Từ> không được bỏ trống.')
        elif(DEN=='False'):
            raise ValidationError('<Đến> không được bỏ trống.')
        elif(TU > DEN):
            raise ValidationError('<Đến> phải lớn hơn hoặc bằng <Từ>.')


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
        CONG_GOP_CAC_NUT_GIONG_NHAU = 1 if 'CONG_GOP_CAC_NUT_GIONG_NHAU' in params.keys() and params['CONG_GOP_CAC_NUT_GIONG_NHAU'] != 'False' else 0
        HIEN_THI_SO_LUY_KE_KY_TRUOC_CHUYEN_SANG = 1 if 'HIEN_THI_SO_LUY_KE_KY_TRUOC_CHUYEN_SANG' in params.keys() and params['HIEN_THI_SO_LUY_KE_KY_TRUOC_CHUYEN_SANG'] != 'False' else 0
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None

        params_sql = {
            'TU_NGAY':TU_NGAY_F, 
            'DEN_NGAY':DEN_NGAY_F,
            'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
            'CONG_GOP_CAC_NUT_GIONG_NHAU':CONG_GOP_CAC_NUT_GIONG_NHAU,
            'HIEN_THI_SO_LUY_KE_KY_TRUOC_CHUYEN_SANG':HIEN_THI_SO_LUY_KE_KY_TRUOC_CHUYEN_SANG,
            'CHI_NHANH_ID':CHI_NHANH_ID,
            'nam_tai_chinh':self.env['ir.config_parameter'].get_param('he_thong.TU_NGAY_BAT_DAU_TAI_CHINH'),
            'limit': limit,
            'offset': offset,
        }

        query = """
        DO LANGUAGE plpgsql $$
DECLARE
  tu_ngay                                 DATE := %(TU_NGAY)s;
  --tham số từ
  den_ngay                                DATE := %(DEN_NGAY)s;
  --tham số đến
  nam_tai_chinh                           DATE := %(nam_tai_chinh)s;
  chi_nhanh_id                            INTEGER := %(CHI_NHANH_ID)s;
  bao_gom_du_lieu_chi_nhanh_phu_thuoc     INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;
  cong_gop_cac_but_toan_giong_nhau        INTEGER := %(CONG_GOP_CAC_NUT_GIONG_NHAU)s;
  hien_thi_so_luy_ke_ky_truoc_chuyen_sang INTEGER := %(HIEN_THI_SO_LUY_KE_KY_TRUOC_CHUYEN_SANG)s;
  dau_ky_tu_ngay DATE := '2017-12-31';
BEGIN

  DROP TABLE IF EXISTS TMP_LIST_BRAND;

  CREATE TEMP TABLE TMP_LIST_BRAND
    AS
      SELECT *
      FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc);

  DROP TABLE IF EXISTS TMP_KET_QUA;

  dau_ky_tu_ngay = tu_ngay + INTERVAL '-1 second';
  IF cong_gop_cac_but_toan_giong_nhau = 1
  THEN
    CREATE TEMP TABLE TMP_KET_QUA
      AS
        -- Lấy cộng trang trước chuyển sang
        SELECT
          NULL :: DATE                       AS "NGAY_HACH_TOAN",
          NULL :: DATE                       AS "NGAY_CHUNG_TU",
          NULL                               AS "SO_CHUNG_TU",
          N'Số lũy kế kỳ trước chuyển sang' AS "DIEN_GIAI",
          NULL                               AS "TAI_KHOAN_ID",
          NULL                               AS "TAI_KHOAN_DOI_UNG_ID",
          SUM(GL."GHI_NO")                   AS "GHI_NO",
          SUM(GL."GHI_CO")                   AS "GHI_CO",
          NULL :: INTEGER                    AS "ID_CHUNG_TU",
          NULL                               AS "MODEL_CHUNG_TU",
          NULL :: INTEGER                    AS "CHI_NHANH_ID"
        FROM so_cai_chi_tiet GL
          INNER JOIN TMP_LIST_BRAND B
            ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
        WHERE (
                hien_thi_so_luy_ke_ky_truoc_chuyen_sang = 1
                AND nam_tai_chinh < tu_ngay
              )

              AND GL."NGAY_HACH_TOAN"
              BETWEEN nam_tai_chinh AND dau_ky_tu_ngay
              AND GL."TAI_KHOAN_DOI_UNG_ID" IS NOT NULL
              AND GL."TAI_KHOAN_DOI_UNG_ID" <> 0
        HAVING SUM(GL."GHI_NO") <> 0
               OR SUM(GL."GHI_CO") <> 0
        UNION ALL
        -- lấy dữ liệu cộng gộp
        SELECT
          GL."NGAY_HACH_TOAN",
          GL."NGAY_CHUNG_TU",
          GL."SO_CHUNG_TU",
          GL."DIEN_GIAI_CHUNG" as DIEN_GIAI,
          GL."TAI_KHOAN_ID",
          GL."TAI_KHOAN_DOI_UNG_ID",
          SUM(GL."GHI_NO")              AS "GHI_NO",
          SUM(GL."GHI_CO")              AS "GHI_CO",
                    GL."ID_CHUNG_TU",
          GL."MODEL_CHUNG_TU",
          B."CHI_NHANH_ID"
        FROM so_cai_chi_tiet GL
          INNER JOIN TMP_LIST_BRAND B
            ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
        WHERE GL."NGAY_HACH_TOAN"
              BETWEEN tu_ngay AND den_ngay
              AND COALESCE(GL."TAI_KHOAN_DOI_UNG_ID", 0) <> 0
        GROUP BY GL."NGAY_HACH_TOAN",
          GL."NGAY_CHUNG_TU",
          GL."SO_CHUNG_TU",
          GL."DIEN_GIAI_CHUNG",
          GL."TAI_KHOAN_ID",
          GL."TAI_KHOAN_DOI_UNG_ID",
                    GL."ID_CHUNG_TU",
          GL."MODEL_CHUNG_TU",
          B."CHI_NHANH_ID"
        HAVING SUM(GL."GHI_NO") <> 0
               OR SUM(GL."GHI_CO") <> 0;

  ELSE
    CREATE TEMP TABLE TMP_KET_QUA
      AS
        -- Lấy cộng trang trước chuyển sang
        SELECT
          NULL :: DATE                       AS "NGAY_HACH_TOAN",
          NULL :: DATE                       AS "NGAY_CHUNG_TU",
          NULL                               AS "SO_CHUNG_TU",
          N'Số lũy kế kỳ trước chuyển sang' AS "DIEN_GIAI",
          NULL                               AS "TAI_KHOAN_ID",
          NULL                               AS "TAI_KHOAN_DOI_UNG_ID",
          SUM(GL."GHI_NO")                   AS "GHI_NO",
          SUM(GL."GHI_CO")                   AS "GHI_CO",
            NULL :: INTEGER                    AS "ID_CHUNG_TU",
          NULL                               AS "MODEL_CHUNG_TU",
          NULL :: INTEGER                    AS "CHI_NHANH_ID"
        FROM so_cai_chi_tiet GL
          INNER JOIN TMP_LIST_BRAND B
            ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
        WHERE (
                hien_thi_so_luy_ke_ky_truoc_chuyen_sang = 1
                AND nam_tai_chinh < tu_ngay
              )
              AND GL."NGAY_HACH_TOAN"
              BETWEEN nam_tai_chinh AND dau_ky_tu_ngay
              AND GL."TAI_KHOAN_DOI_UNG_ID" IS NOT NULL
              AND GL."TAI_KHOAN_DOI_UNG_ID" <> 0
        HAVING SUM(GL."GHI_NO") <> 0
               OR SUM(GL."GHI_CO") <> 0
        UNION ALL
        -- Lấy dữ liệu chi tiết
        SELECT
          GL."NGAY_HACH_TOAN",
          GL."NGAY_CHUNG_TU",
          GL."SO_CHUNG_TU",
          GL."DIEN_GIAI",
          GL."TAI_KHOAN_ID",
          GL."TAI_KHOAN_DOI_UNG_ID",
          GL."GHI_NO",
          GL."GHI_CO",
          GL."ID_CHUNG_TU",
          GL."MODEL_CHUNG_TU",
          B."CHI_NHANH_ID"
        FROM so_cai_chi_tiet GL
          INNER JOIN TMP_LIST_BRAND B
            ON B."CHI_NHANH_ID" = GL."CHI_NHANH_ID"
        WHERE GL."NGAY_HACH_TOAN"
              BETWEEN tu_ngay AND den_ngay
              AND COALESCE(GL."TAI_KHOAN_DOI_UNG_ID", 0) <> 0
              AND
              (
                GL."GHI_NO" <> 0
                OR GL."GHI_CO" <> 0
              );
  END IF;
END $$;

SELECT result."NGAY_HACH_TOAN" as "NGAY_HACH_TOAN" ,
result."NGAY_CHUNG_TU" as "NGAY_CHUNG_TU" ,
result."SO_CHUNG_TU" as "SO_CHUNG_TU" ,
result."DIEN_GIAI" as "DIEN_GIAI" ,
result."GHI_NO" as "PHAT_SINH_NO" ,
result."GHI_CO" as "PHAT_SINH_CO" ,
result."ID_CHUNG_TU" as "ID_GOC" ,
result."MODEL_CHUNG_TU" as "MODEL_GOC" ,
taiKhoan."SO_TAI_KHOAN" as "TAI_KHOAN", 
taiKhoanDoiUng."SO_TAI_KHOAN" as "TK_DOI_UNG"
FROM TMP_KET_QUA result
          LEFT JOIN danh_muc_he_thong_tai_khoan AS taiKhoan ON result."TAI_KHOAN_ID" = taiKhoan."id"
          LEFT JOIN danh_muc_he_thong_tai_khoan AS taiKhoanDoiUng ON result."TAI_KHOAN_DOI_UNG_ID" = taiKhoanDoiUng."id"
            OFFSET %(offset)s
            LIMIT %(limit)s;
        """
        return self.execute(query,params_sql)
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_SO_NHAT_KY_CHUNG, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        return result
    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        TU = self.get_vntime('TU')
        DEN = self.get_vntime('DEN')
        param = 'Từ ngày: %s đến ngày %s' % (TU, DEN)
        action = self.env.ref('bao_cao.open_report__so_nhat_ky_chung').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action