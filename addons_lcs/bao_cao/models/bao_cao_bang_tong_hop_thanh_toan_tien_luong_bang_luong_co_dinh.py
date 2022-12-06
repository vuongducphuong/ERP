# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision
from datetime import timedelta, datetime


class BAO_CAO_BANG_TONG_HOP_THANH_TOAN_TIEN_LUONG_BANG_LUONG_CO_DINH(models.Model):
	_name = 'bao.cao.bang.tong.hop.thanh.toan.tien.luong.bang.luong.co.dinh'
	
	
	_auto = False

	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
	BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default=True)
	THANG = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ], string='Tháng', help='Tháng',required=True)
	NAM = fields.Integer(string='Năm', help='Năm')
	DON_VI = fields.Char(string='Đơn vị', help='Đơn vị')
	HO_VA_TEN = fields.Char(string='Họ và tên', help='Họ và tên')
	HE_SO_LUONG = fields.Float(string='Hệ số lương', help='Hệ số lương' ,digits= decimal_precision.get_precision('VND'))
	LUONG_CO_BAN = fields.Float(string='Lương cơ bản', help='Lương cơ bản' ,digits= decimal_precision.get_precision('VND'))
	PHU_CAP = fields.Float(string='Phụ cấp', help='Phụ cấp' ,digits= decimal_precision.get_precision('VND'))
	TONG_SO = fields.Float(string='Tổng số', help='Tổng số' ,digits= decimal_precision.get_precision('VND'))
	TAM_UNG_LUONG_TRONG_KY = fields.Float(string='Tạm ứng lương trong kỳ', help='Tạm ứng lương trong kỳ' ,digits= decimal_precision.get_precision('VND'))
	BHXH_KHAU_TRU = fields.Float(string='BHXH ', help='Bảo hiểm xã hội' ,digits= decimal_precision.get_precision('VND'))
	BHYT_KHAU_TRU = fields.Float(string='BHYT khấu trừ', help='Bảo hiểm y tế khấu trừ' ,digits= decimal_precision.get_precision('VND'))
	BHTN_KHAU_TRU = fields.Float(string='BHTN khấu trừ', help='Bảo hiểm thất nghiệp khấu trừ' ,digits= decimal_precision.get_precision('VND'))
	THUE_TNCN_PHAI_NOP = fields.Float(string='Thuế TNCN phải nộp', help='Thuế thu nhập cá nhân phải nộp' ,digits= decimal_precision.get_precision('VND'))
	CONG = fields.Float(string='Cộng', help='Cộng' ,digits= decimal_precision.get_precision('VND'))
	SO_TIEN_DUOC_LINH = fields.Float(string='Số tiền được lĩnh', help='Số tiền được lĩnh' ,digits= decimal_precision.get_precision('VND'))
	KY_NHAN = fields.Char(string='Ký nhận', help='Ký nhận')

	DON_VI_IDS = fields.One2many('danh.muc.to.chuc')

	### START IMPLEMENTING CODE ###
	@api.model
	def default_get(self, fields_list):
		result = super(BAO_CAO_BANG_TONG_HOP_THANH_TOAN_TIEN_LUONG_BANG_LUONG_CO_DINH, self).default_get(fields_list)

		thang = datetime.now().month
		result['THANG'] = str(thang)
		result['NAM'] = datetime.now().year
		
		chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
		don_vis = self.env['danh.muc.to.chuc'].search([('CAP_TO_CHUC' ,'not in', ('1','2'))])
		if chi_nhanh:
			result['CHI_NHANH_ID'] = chi_nhanh.id
		if don_vis:
			result['DON_VI_IDS'] = don_vis.ids
		
		return result

	def _validate(self):
		params = self._context
		NAM = params['NAM'] if 'NAM' in params.keys() else 'False'
		DON_VI_IDS = params['DON_VI_IDS'] if 'DON_VI_IDS' in params.keys() else 'False'
		if (DON_VI_IDS == 'False'):
			raise ValidationError('Bạn chưa chọn <Đơn vị>. Xin vui lòng chọn lại.')
		else: 
			if (NAM < 1700 or NAM > 9999  ):
				raise ValidationError('<Năm> phải nằm trong khoảng 1700 - 9999.')

	@api.model
	def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
		record = []
		# Get paramerters here
		params = self._context
		if not params.get('active_model'):
			return
		CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() and params['CHI_NHANH_ID'] != 'False' else None
		BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = 1 if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() and params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] != 'False' else 0
		THANG = params['THANG'] if 'THANG' in params.keys() else 'False'
		NAM = params['NAM'] if 'NAM' in params.keys() else 'False'
		DON_VI_IDS = [nh_kh['id'] for nh_kh in params['DON_VI_IDS']]  if 'DON_VI_IDS' in params.keys() and params['DON_VI_IDS'] != 'False' else None
		LOAI_CHUNG_TU = 6021 if params.get('THOI_GIAN_LUONG') == 'LUONG_THEO_BUOI' else 6022
		params_sql = {
			'CHI_NHANH_ID':CHI_NHANH_ID, 
			'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC':BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC,
			'THANG':str(THANG),
			'NAM':NAM,
			'DON_VI_IDS':DON_VI_IDS,
            'LOAI_CHUNG_TU': LOAI_CHUNG_TU,
            'limit': limit,
            'offset': offset, 
			}      
		# Execute SQL query here
		query = """
		DO LANGUAGE plpgsql $$
DECLARE


    chi_nhanh_id                        INTEGER := %(CHI_NHANH_ID)s;

    bao_gom_du_lieu_chi_nhanh_phu_thuoc INTEGER := %(BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC)s;

    --tham số bao gồm số liệu chi nhánh phụ thuộc

    bang_luong_thanh                    INTEGER := %(THANG)s;

    --@PASalarySheetMonth

    bang_luong_nam                       INTEGER := %(NAM)s;

    --@PASalarySheetYear

    don_vi_ids                          INTEGER := -1 ;

    --@OrganizationUnitID

    loai_chung_tu                       INTEGER := %(LOAI_CHUNG_TU)s;


BEGIN

    DROP TABLE IF EXISTS TMP_LIST_BRAND
    ;

    CREATE TEMP TABLE TMP_LIST_BRAND
        AS
            SELECT *
            FROM LAY_DANH_SACH_CHI_NHANH(chi_nhanh_id, bao_gom_du_lieu_chi_nhanh_phu_thuoc)
    ;


    DROP TABLE IF EXISTS TMP_DON_VI
    ;

    CREATE TEMP TABLE TMP_DON_VI

    (
        "DON_VI_ID"   INT PRIMARY KEY,
        "MA_DON_VI"   VARCHAR(20),
        "TEN_DON_VI"  VARCHAR(128),
        "MA_PHAN_CAP" VARCHAR(100),
        "BAC"         INT

    )
    ;

    IF don_vi_ids IS NOT NULL
    THEN
        INSERT INTO TMP_DON_VI
            SELECT
                "id" AS "DON_VI_ID"
                , "MA_DON_VI"
                , "TEN_DON_VI"
                , OU."MA_PHAN_CAP"
                , OU."BAC"

            FROM danh_muc_to_chuc OU
            WHERE OU."id" = any(%(DON_VI_IDS)s) --@OrganizationUnitID
        ;
    END IF
    ;


    DROP TABLE IF EXISTS TMP_KET_QUA
    ;

    CREATE TEMP TABLE TMP_KET_QUA
        AS


            SELECT
                PA."id" AS "ID_CHUNG_TU"
                 ,'tien.luong.bang.luong' AS "MODEL_CHUNG_TU"
                , PA."THANG"
                , PA."NAM"
                , PA."TEN_BANG_LUONG"

                , OU."MA_DON_VI" || ' - ' || OU."TEN_DON_VI"                                     AS "DON_VI"
                , AO."MA"                                                                      AS "MA_NHAN_VIEN"
                ,
                  AO."HO_VA_TEN"                                                               AS "TEN_NHAN_VIEN"
                , PAD."CHUC_DANH" --Chức danh lấy trên bảng lương
                , PAD."HE_SO_LUONG" AS "HE_SO_LUONG"
                , PAD."LUONG_CO_BAN"                                                           AS "LUONG_CO_BAN"
                , COALESCE(PAD."PHU_CAP_THUOC_QUY_LUONG", 0) + COALESCE(PAD."PHU_CAP_KHAC", 0) AS "PHU_CAP" -- phụ cấp
                , PAD."TONG_SO"
                ,
                  PAD."SO_TIEN_TAM_UNG"                                                        AS "TAM_UNG_LUONG_TRONG_KY"
                , PAD."TAM_UNG_141" -- tạm ứng 141
                , PAD."LUONG_DONG_BH" -- Lương ĐBH
                , PAD."KPCD_KHAU_TRU" --KPCĐ
                , PAD."BHXH_KHAU_TRU" -- BHXH
                , PAD."BHYT_KHAU_TRU" -- BHYT
                , PAD."BHTN_KHAU_TRU" -- BH thất nghiệp
                , PAD."THUE_TNCN_KHAU_TRU" -- Thuế Thu nhập cá nhân phải nộp
                , PAD."CONG_KHAU_TRU" -- Cộng các khoản khấu trừ

                , PAD."GIAM_TRU_GIA_CANH" -- Giảm trừ gia cảnh
                ,
                  PAD."THU_NHAP_TINH_THUE_TNCN"                                                AS "THU_NHAP_TINH_THUE_TNCN"
                -- Thu nhập tính thuế TNCN
                , PAD."BHXH_CONG_TY_DONG"
                , PAD."BHYT_CONG_TY_DONG"
                , PAD."BHTN_CONG_TY_DONG"
                , PAD."KPCD_CONG_TY_DONG"

                , PAD."SO_TIEN_CON_DUOC_LINH" -- Số tiền còn được lĩnh
                , "KY_NHAN"                                                                    AS "KY_NHAN" --ký nhận
                , PAD."STT"

            FROM tien_luong_bang_luong PA INNER JOIN tien_luong_bang_luong_chi_tiet PAD ON PAD."CHI_TIET_ID" = PA."id"
                INNER JOIN TMP_DON_VI OU ON PAD."DON_VI_ID" = OU."DON_VI_ID"
                INNER JOIN res_partner AO ON AO."id" = PAD."MA_NHAN_VIEN"
                INNER JOIN TMP_LIST_BRAND BIDL ON PA."CHI_NHANH_ID" = BIDL."CHI_NHANH_ID"
            WHERE PA."LOAI_CHUNG_TU" = loai_chung_tu
                  AND PA."NAM" = bang_luong_nam AND PA."THANG" = bang_luong_thanh

            ORDER BY
                "DON_VI",
                AO."HO_VA_TEN",
                "STT"
    ;


END $$
;
		SELECT 
                "TEN_NHAN_VIEN" AS "HO_VA_TEN",
                "HE_SO_LUONG" AS "HE_SO_LUONG",
                "LUONG_CO_BAN" AS "LUONG_CO_BAN",
                "PHU_CAP" AS "PHU_CAP",
                "TONG_SO" AS "TONG_SO",
                "TAM_UNG_LUONG_TRONG_KY" AS "TAM_UNG_LUONG_TRONG_KY",
                "BHXH_KHAU_TRU" AS "BHXH_KHAU_TRU",
                "BHYT_KHAU_TRU" AS "BHYT_KHAU_TRU",
                "BHTN_KHAU_TRU" AS "BHTN_KHAU_TRU",
                "THUE_TNCN_KHAU_TRU" AS "THUE_TNCN_PHAI_NOP",
                "CONG_KHAU_TRU" AS "CONG",
                "SO_TIEN_CON_DUOC_LINH" AS "SO_TIEN_DUOC_LINH",
                "KY_NHAN" AS "KY_NHAN",
                "DON_VI" AS "DON_VI"
                           
                FROM TMP_KET_QUA
  				ORDER BY
                "DON_VI",
               	"TEN_NHAN_VIEN",
                "STT"

                OFFSET %(offset)s
                LIMIT %(limit)s;
		"""

		return self.execute(query,params_sql)


	### END IMPLEMENTING CODE ###

	def _action_view_report(self):
		self._validate()
		THANG  = self.get_context('THANG')
		NAM  = self.get_context('NAM')
		param = ''
		if len (self.get_context('DON_VI_IDS')) == 1:
			DON_VI = self.get_context('DON_VI_IDS')[0]['TEN_DON_VI']
			param = ' Đơn vị: %s ;Tháng: %s năm %s' % (DON_VI, THANG , NAM)
		else:
			param = 'Tháng: %s năm %s' % (THANG , NAM)

		action = self.env.ref('bao_cao.open_report_bang_tong_hop_thanh_toan_tien_luong_bang_luong_co_dinh').read()[0]
		# action['options'] = {'clear_breadcrumbs': True}
		action['context'] = eval(action.get('context','{}'))
		action['context'].update({'breadcrumb_ex': param})
		return action