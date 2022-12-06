# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_CHUNG_TU_GHI_TANG_TSCD(models.Model):
	_name = 'bao.cao.chung.tu.ghi.tang.tscd'
	_auto = False

	ref = fields.Char(string='Reffence ID')

	id =  fields.Integer(string='ID chứng từ')
	# MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')

	MA_TAI_SAN = fields.Char(string='Mã tài sản') #FixedAssetCode
	TEN_TAI_SAN = fields.Char(string='Tên tài sản') #FixedAssetName

	MA = fields.Char(string= 'Mã loại tài sản') #FixedAssetCategoryCode
	TEN = fields.Char(string= 'Tên loại tài sản') #FixedAssetCategoryName
	TINH_TRANG_GHI_TANG = fields.Integer(string= 'Tình trạng ghi tăng') #State
	MA_DON_VI = fields.Char(string= 'Mã đơn vị') #OrganizationUnitCode
	TEN_DON_VI = fields.Char(string= 'Tên đơn vị') #OrganizationUnitName
	LOAI_CHUNG_TU = fields.Integer(string= 'Loại chứng từ') #RefType
	NGAY_GHI_TANG = fields.Date(string= 'Ngày ghi tăng') #RefDate
	SO_CT_GHI_TANG = fields.Char(string= 'Số chứng từ ghi tăng') #RefNo
	NGUYEN_GIA = fields.Float(string= 'Nguyên giá' , digits=decimal_precision.get_precision('VND')) #OrgPrice
	GIA_TRI_TINH_KHAU_HAO = fields.Float(string= 'Giá trị tính khấu hao',digits=decimal_precision.get_precision('VND')) #DepreciationAmount

	
	

	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
	

	currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())

	TSCD_NGUON_GOC_HINH_THANH_CHI_TIETS = fields.One2many('bao.cao.chung.tu.ghi.tang.tscd.nght', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')
	TSCD_BO_PHAN_CAU_THANH_THANH_CHI_TIETS = fields.One2many('bao.cao.chung.tu.ghi.tang.tscd.bpct', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')
	TSCD_DUNG_CU_PHU_TUNG_KEM_THEO_CHI_TIETS = fields.One2many('bao.cao.chung.tu.ghi.tang.tscd.dcptkt', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')


class BAO_CAO_CHUNG_TU_GHI_TANG_TSCD_REPORT(models.AbstractModel):
	_name = 'report.bao_cao.template_fixedassetincrementvoucher'

	@api.model
	def get_report_values(self, docids, data=None):
		############### START SQL lấy dữ liệu ###############
		# Ví dụ với asset_ghi_tang có id in (92, 94)
		# data['ids'] = ('asset.ghi.tang,92','asset.ghi.tang,94')
		refTypeList, records = self.get_reftype_list(data)

		# sql_result = self.ham_lay_du_lieu_sql_tra_ve(refTypeList)
		
		sql_master = self.ham_lay_du_lieu_sql_tra_ve_master(docids)
		sql_detail_nght = self.ham_lay_du_lieu_sql_tra_ve_detail_nght(docids)
		sql_detail_bpct = self.ham_lay_du_lieu_sql_tra_ve_detail_bpct(docids)
		sql_detail_dcptkt = self.ham_lay_du_lieu_sql_tra_ve_detail_dcptkt(docids)

		# 1. Update master
		for line in sql_master:
			key = 'asset.ghi.tang' + ',' + str(line.get('id'))
			master_data = self.env['bao.cao.chung.tu.ghi.tang.tscd'].convert_for_update(line)
			if records.get(key):
				records[key].update(master_data)
		
		# 2. Update detail_nght
		for line in sql_detail_nght:
			key = 'asset.ghi.tang' + ',' + str(line.get('id'))
			detail_data1 = self.env['bao.cao.chung.tu.ghi.tang.tscd.nght'].convert_for_update(line)
			if records.get(key):
				records[key].TSCD_NGUON_GOC_HINH_THANH_CHI_TIETS += self.env['bao.cao.chung.tu.ghi.tang.tscd.nght'].new(detail_data1)
		
		# 2. Update detail_bpct
		for line in sql_detail_bpct:
			key = 'asset.ghi.tang' + ',' + str(line.get('id'))
			detail_data2 = self.env['bao.cao.chung.tu.ghi.tang.tscd.bpct'].convert_for_update(line)
			if records.get(key):
				records[key].TSCD_BO_PHAN_CAU_THANH_THANH_CHI_TIETS += self.env['bao.cao.chung.tu.ghi.tang.tscd.bpct'].new(detail_data2)

		# 2. Update detail_dcptkt
		for line in sql_detail_dcptkt:
			key = 'asset.ghi.tang' + ',' + str(line.get('id'))
			detail_data3 = self.env['bao.cao.chung.tu.ghi.tang.tscd.dcptkt'].convert_for_update(line)
			if records.get(key):
				records[key].TSCD_DUNG_CU_PHU_TUNG_KEM_THEO_CHI_TIETS += self.env['bao.cao.chung.tu.ghi.tang.tscd.dcptkt'].new(detail_data3)
		
		docs = []
		for k in records:
			doc = records.get(k)
			if len(doc.TSCD_NGUON_GOC_HINH_THANH_CHI_TIETS) == 0:
				records[k].TSCD_NGUON_GOC_HINH_THANH_CHI_TIETS = self.env['bao.cao.chung.tu.ghi.tang.tscd.nght'].new({})
			
			if len(doc.TSCD_BO_PHAN_CAU_THANH_THANH_CHI_TIETS) == 0:
				records[k].TSCD_BO_PHAN_CAU_THANH_THANH_CHI_TIETS = self.env['bao.cao.chung.tu.ghi.tang.tscd.bpct'].new({})
			
			if len(doc.TSCD_DUNG_CU_PHU_TUNG_KEM_THEO_CHI_TIETS) == 0:
				records[k].TSCD_DUNG_CU_PHU_TUNG_KEM_THEO_CHI_TIETS = self.env['bao.cao.chung.tu.ghi.tang.tscd.dcptkt'].new({})
			docs += doc

		# docs = [records.get(k) for k in records]


		return {
			'docs': docs,
	}

	def ham_lay_du_lieu_sql_tra_ve_master(self,refTypeList):
		params_sql = {
		'refTypeList':refTypeList, 
		}  

		query = """
		DO LANGUAGE plpgsql $$
		DECLARE



		rec       RECORD;


		BEGIN

		DROP TABLE IF EXISTS TMP_GHI_TANG_TSCD
		;

		CREATE TEMP TABLE TMP_GHI_TANG_TSCD
		AS
		--Bảng FixedAsset
		SELECT  FA."id" ,
		FA."MA_TAI_SAN" ,
		FA."TEN_TAI_SAN" ,
		FC."MA" ,
		FC."TEN" ,
		FA."TINH_TRANG_GHI_TANG" ,
		FA."CHI_NHANH_ID" ,
		OU."MA_DON_VI" ,
		OU."TEN_DON_VI" ,

		FA."LOAI_CHUNG_TU" ,
		FA."NGAY_GHI_TANG" ,
		FA."SO_CT_GHI_TANG" ,
		FA."NGUYEN_GIA" ,
		FA."GIA_TRI_TINH_KHAU_HAO"
		FROM    asset_ghi_tang FA
		INNER JOIN danh_muc_loai_tai_san_co_dinh FC ON FC."id" = FA."LOAI_TAI_SAN_ID"
		LEFT JOIN danh_muc_to_chuc OU ON OU."id" = FA."DON_VI_SU_DUNG_ID"
		WHERE FA."id" = any (%(refTypeList)s) 

		ORDER BY FA."NGAY_GHI_TANG" DESC ,
		FA."SO_CT_GHI_TANG" DESC ,
		fa."MA_TAI_SAN" ,
		fa."TEN_TAI_SAN" ;
		--Bảng FixedAssetDetailSource

		DROP TABLE IF EXISTS TMP_GHI_TANG_NGUON_GOC_HINH_THANH_TSCD
		;

		CREATE TEMP TABLE TMP_GHI_TANG_NGUON_GOC_HINH_THANH_TSCD
		AS
		SELECT
		FA."id" ,

		GL."LOAI_CHUNG_TU" ,
		GL."NGAY_CHUNG_TU" ,
		GL."SO_CHUNG_TU" ,
		GL."DIEN_GIAI_CHUNG" ,
		GL."GHI_NO" AS "SO_TIEN" ,
		GL."TAI_KHOAN_ID" AS "TK_NO" ,
		GL."TAI_KHOAN_DOI_UNG_ID" AS "TK_CO" ,
		FADS."THU_TU_SAP_XEP_CHI_TIET"
		FROM    asset_ghi_tang FA
		LEFT JOIN asset_ghi_tang_nguon_goc_hinh_thanh FADS ON FADS."TAI_SAN_CO_DINH_GHI_TANG_ID" = FA."id"
		LEFT JOIN so_cai_chi_tiet AS GL ON FADS.id = GL."CHI_TIET_ID"
		AND FADS."TK_CO_ID" = GL."TAI_KHOAN_DOI_UNG_ID"
		AND FADS."TK_NO_ID" = GL."TAI_KHOAN_ID"

		AND ( GL."LOAI_HACH_TOAN" = '1'
			AND LEFT((select "SO_TAI_KHOAN" from danh_muc_he_thong_tai_khoan as TK where TK.id =   GL."TAI_KHOAN_ID"),
					3) IN ( '211',
					'213', '212',
					'217' )
			)

		WHERE   FADS.id IS NOT NULL  AND FA."id" = any (%(refTypeList)s) 

		UNION ALL
		SELECT  FA."id" ,

		GL."LOAI_CHUNG_TU" ,
		GL."NGAY_CHUNG_TU" ,
		GL."SO_CHUNG_TU" ,
		GL."DIEN_GIAI_CHUNG" ,
		GL."GHI_NO" AS "SO_TIEN" ,
		GL."TAI_KHOAN_ID" AS "TK_KHO" ,
		GL."TAI_KHOAN_DOI_UNG_ID" AS "TK_CO" ,
		FADS."THU_TU_SAP_XEP_CHI_TIET"
		FROM    asset_ghi_tang FA
		LEFT JOIN asset_ghi_tang_nguon_goc_hinh_thanh FADS ON FADS."TAI_SAN_CO_DINH_GHI_TANG_ID" = FA."id"
		LEFT JOIN so_cai_chi_tiet AS GL ON FADS."id" = GL."CHI_TIET_ID"
		AND ( GL."LOAI_HACH_TOAN" = '1'
			AND LEFT((select "SO_TAI_KHOAN" from danh_muc_he_thong_tai_khoan as TK where TK.id =   GL."TAI_KHOAN_ID"),
					3) IN ( '211',
					'213', '212',
					'217' )
			)

		WHERE   FADS."TAI_SAN_CO_DINH_GHI_TANG_ID" IS NOT NULL
		AND FADS.id IS NULL
		AND
		FA."id" = any (%(refTypeList)s) 

		ORDER BY "THU_TU_SAP_XEP_CHI_TIET"
		;--DESC


		DROP TABLE IF EXISTS TMP_GHI_TANG_BO_PHAN_CAU_THANH_TSCD
		;

		CREATE TEMP TABLE TMP_GHI_TANG_BO_PHAN_CAU_THANH_TSCD
		AS
		SELECT  FA."id" ,
		FAD."BO_PHAN" ,
		FAD."DON_VI_TINH" ,
		FAD."SO_LUONG" ,
		FAD."THOI_HAN_BAO_HANH" ,
		fad."THU_TU_SAP_XEP_CHI_TIET"
		FROM    asset_ghi_tang FA
		LEFT JOIN asset_ghi_tang_bo_phan_cau_thanh FAD ON FAD."TAI_SAN_CO_DINH_GHI_TANG_ID" = FA."id"
		WHERE FA."id" = any (%(refTypeList)s) 


		ORDER BY fad."THU_TU_SAP_XEP_CHI_TIET" ;--DESC


		DROP TABLE IF EXISTS TMP_GHI_TANG_DUNG_CU_PHU_TUNG_TSCD
		;

		CREATE TEMP TABLE TMP_GHI_TANG_DUNG_CU_PHU_TUNG_TSCD
		AS
		SELECT  FA."id" ,
		FADA."TEN_QUY_CACH_DUNG_CU_PHU_TUNG" ,
		FADA."DON_VI_TINH" ,
		FADA."SO_LUONG" ,
		FADA."GIA_TRI" ,
		FADA."THU_TU_SAP_XEP_CHI_TIET"
		FROM    asset_ghi_tang FA
		LEFT JOIN asset_ghi_tang_dung_cu_phu_tung FADA ON FADA."TAI_SAN_CO_DINH_GHI_TANG_ID" = FA."id"
		WHERE FA."id" = any (%(refTypeList)s) 

		ORDER BY FADA."THU_TU_SAP_XEP_CHI_TIET"  ;--DESC

		END $$

		;


		SELECT

		*
		FROM TMP_GHI_TANG_TSCD GT 

		;
		"""
		return self.execute(query,params_sql)

	def ham_lay_du_lieu_sql_tra_ve_detail_nght(self,refTypeList):
		
		params_sql = {
		'refTypeList':refTypeList, 
		}  

		query = """
		DO LANGUAGE plpgsql $$
		DECLARE



		rec       RECORD;


		BEGIN

		DROP TABLE IF EXISTS TMP_GHI_TANG_TSCD
		;

		CREATE TEMP TABLE TMP_GHI_TANG_TSCD
		AS
		--Bảng FixedAsset
		SELECT  FA."id" ,
		FA."MA_TAI_SAN" ,
		FA."TEN_TAI_SAN" ,
		FC."MA" ,
		FC."TEN" ,
		FA."TINH_TRANG_GHI_TANG" ,
		FA."CHI_NHANH_ID" ,
		OU."MA_DON_VI" ,
		OU."TEN_DON_VI" ,

		FA."LOAI_CHUNG_TU" ,
		FA."NGAY_GHI_TANG" ,
		FA."SO_CT_GHI_TANG" ,
		FA."NGUYEN_GIA" ,
		FA."GIA_TRI_TINH_KHAU_HAO"
		FROM    asset_ghi_tang FA
		INNER JOIN danh_muc_loai_tai_san_co_dinh FC ON FC."id" = FA."LOAI_TAI_SAN_ID"
		LEFT JOIN danh_muc_to_chuc OU ON OU."id" = FA."DON_VI_SU_DUNG_ID"
		WHERE FA."id" = any (%(refTypeList)s) 

		ORDER BY FA."NGAY_GHI_TANG" DESC ,
		FA."SO_CT_GHI_TANG" DESC ,
		fa."MA_TAI_SAN" ,
		fa."TEN_TAI_SAN" ;
		--Bảng FixedAssetDetailSource

		DROP TABLE IF EXISTS TMP_GHI_TANG_NGUON_GOC_HINH_THANH_TSCD
		;

		CREATE TEMP TABLE TMP_GHI_TANG_NGUON_GOC_HINH_THANH_TSCD
		AS
		SELECT
		FA."id" ,

		GL."LOAI_CHUNG_TU" ,
		GL."NGAY_CHUNG_TU" ,
		GL."SO_CHUNG_TU" ,
		GL."DIEN_GIAI_CHUNG" ,
		GL."GHI_NO" AS "SO_TIEN" ,
		GL."TAI_KHOAN_ID" AS "TK_NO" ,
		GL."TAI_KHOAN_DOI_UNG_ID" AS "TK_CO" ,
		FADS."THU_TU_SAP_XEP_CHI_TIET",
		FADS."LOAI_CHUNG_TU" AS "LOAI_CHUNG_TU_NGUON_GOC_HINH_THANH"
		FROM    asset_ghi_tang FA
		LEFT JOIN asset_ghi_tang_nguon_goc_hinh_thanh FADS ON FADS."TAI_SAN_CO_DINH_GHI_TANG_ID" = FA."id"
		LEFT JOIN so_cai_chi_tiet AS GL ON FADS.id = GL."CHI_TIET_ID"
					AND FADS."TK_CO_ID" = GL."TAI_KHOAN_DOI_UNG_ID"
					AND FADS."TK_NO_ID" = GL."TAI_KHOAN_ID"

					AND ( GL."LOAI_HACH_TOAN" = '1'
						AND LEFT((select "SO_TAI_KHOAN" from danh_muc_he_thong_tai_khoan as TK where TK.id =   GL."TAI_KHOAN_ID"),
								3) IN ( '211',
								'213', '212',
								'217' )
						)

		WHERE   FADS.id IS NOT NULL  AND FA."id" = any (%(refTypeList)s) 

		UNION ALL
		SELECT  FA."id" ,

		GL."LOAI_CHUNG_TU" ,
		GL."NGAY_CHUNG_TU" ,
		GL."SO_CHUNG_TU" ,
		GL."DIEN_GIAI_CHUNG" ,
		GL."GHI_NO" AS "SO_TIEN" ,
		GL."TAI_KHOAN_ID" AS "TK_NO" ,
		GL."TAI_KHOAN_DOI_UNG_ID" AS "TK_CO" ,
		FADS."THU_TU_SAP_XEP_CHI_TIET",
		FADS."LOAI_CHUNG_TU" AS "LOAI_CHUNG_TU_NGUON_GOC_HINH_THANH"
		FROM    asset_ghi_tang FA
		LEFT JOIN asset_ghi_tang_nguon_goc_hinh_thanh FADS ON FADS."TAI_SAN_CO_DINH_GHI_TANG_ID" = FA."id"
		LEFT JOIN so_cai_chi_tiet AS GL ON FADS."id" = GL."CHI_TIET_ID"
					AND ( GL."LOAI_HACH_TOAN" = '1'
						AND LEFT((select "SO_TAI_KHOAN" from danh_muc_he_thong_tai_khoan as TK where TK.id =   GL."TAI_KHOAN_ID"),
								3) IN ( '211',
								'213', '212',
								'217' )
						)

		WHERE
		FADS."TAI_SAN_CO_DINH_GHI_TANG_ID" IS NOT NULL
		AND FADS.id IS NULL
		AND
		FA."id" = any (%(refTypeList)s) 

		ORDER BY "THU_TU_SAP_XEP_CHI_TIET"
		;--DESC


		DROP TABLE IF EXISTS TMP_GHI_TANG_BO_PHAN_CAU_THANH_TSCD
		;

		CREATE TEMP TABLE TMP_GHI_TANG_BO_PHAN_CAU_THANH_TSCD
		AS
		SELECT  FA."id" ,
		FAD."BO_PHAN" ,
		FAD."DON_VI_TINH" ,
		FAD."SO_LUONG" ,
		FAD."THOI_HAN_BAO_HANH" ,
		fad."THU_TU_SAP_XEP_CHI_TIET"
		FROM    asset_ghi_tang FA
		LEFT JOIN asset_ghi_tang_bo_phan_cau_thanh FAD ON FAD."TAI_SAN_CO_DINH_GHI_TANG_ID" = FA."id"
		WHERE FA."id" = any (%(refTypeList)s) 


		ORDER BY fad."THU_TU_SAP_XEP_CHI_TIET" ;--DESC


		DROP TABLE IF EXISTS TMP_GHI_TANG_DUNG_CU_PHU_TUNG_TSCD
		;

		CREATE TEMP TABLE TMP_GHI_TANG_DUNG_CU_PHU_TUNG_TSCD
		AS
		SELECT  FA."id" ,
		FADA."TEN_QUY_CACH_DUNG_CU_PHU_TUNG" ,
		FADA."DON_VI_TINH" ,
		FADA."SO_LUONG" ,
		FADA."GIA_TRI" ,
		FADA."THU_TU_SAP_XEP_CHI_TIET"
		FROM    asset_ghi_tang FA
		LEFT JOIN asset_ghi_tang_dung_cu_phu_tung FADA ON FADA."TAI_SAN_CO_DINH_GHI_TANG_ID" = FA."id"
		WHERE FA."id" = any (%(refTypeList)s) 

		ORDER BY FADA."THU_TU_SAP_XEP_CHI_TIET"  ;--DESC

		END $$

		;


		SELECT

		*
		FROM TMP_GHI_TANG_NGUON_GOC_HINH_THANH_TSCD GT

		;
		"""
		return self.execute(query,params_sql)


	def ham_lay_du_lieu_sql_tra_ve_detail_bpct(self,refTypeList):
		
		params_sql = {
		'refTypeList':refTypeList, 
		}  

		query = """
		DO LANGUAGE plpgsql $$
		DECLARE



		rec       RECORD;


		BEGIN

		DROP TABLE IF EXISTS TMP_GHI_TANG_TSCD
		;

		CREATE TEMP TABLE TMP_GHI_TANG_TSCD
		AS
		--Bảng FixedAsset
		SELECT  FA."id" ,
		FA."MA_TAI_SAN" ,
		FA."TEN_TAI_SAN" ,
		FC."MA" ,
		FC."TEN" ,
		FA."TINH_TRANG_GHI_TANG" ,
		FA."CHI_NHANH_ID" ,
		OU."MA_DON_VI" ,
		OU."TEN_DON_VI" ,

		FA."LOAI_CHUNG_TU" ,
		FA."NGAY_GHI_TANG" ,
		FA."SO_CT_GHI_TANG" ,
		FA."NGUYEN_GIA" ,
		FA."GIA_TRI_TINH_KHAU_HAO"
		FROM    asset_ghi_tang FA
		INNER JOIN danh_muc_loai_tai_san_co_dinh FC ON FC."id" = FA."LOAI_TAI_SAN_ID"
		LEFT JOIN danh_muc_to_chuc OU ON OU."id" = FA."DON_VI_SU_DUNG_ID"
		WHERE FA."id" = any (%(refTypeList)s) 

		ORDER BY FA."NGAY_GHI_TANG" DESC ,
		FA."SO_CT_GHI_TANG" DESC ,
		fa."MA_TAI_SAN" ,
		fa."TEN_TAI_SAN" ;
		--Bảng FixedAssetDetailSource

		DROP TABLE IF EXISTS TMP_GHI_TANG_NGUON_GOC_HINH_THANH_TSCD
		;

		CREATE TEMP TABLE TMP_GHI_TANG_NGUON_GOC_HINH_THANH_TSCD
		AS
		SELECT
		FA."id" ,

		GL."LOAI_CHUNG_TU" ,
		GL."NGAY_CHUNG_TU" ,
		GL."SO_CHUNG_TU" ,
		GL."DIEN_GIAI_CHUNG" ,
		GL."GHI_NO" AS "SO_TIEN" ,
		GL."TAI_KHOAN_ID" AS "TK_NO" ,
		GL."TAI_KHOAN_DOI_UNG_ID" AS "TK_CO" ,
		FADS."THU_TU_SAP_XEP_CHI_TIET",
		FADS."LOAI_CHUNG_TU" AS "LOAI_CHUNG_TU_NGUON_GOC_HINH_THANH"
		FROM    asset_ghi_tang FA
		LEFT JOIN asset_ghi_tang_nguon_goc_hinh_thanh FADS ON FADS."TAI_SAN_CO_DINH_GHI_TANG_ID" = FA."id"
		LEFT JOIN so_cai_chi_tiet AS GL ON FADS.id = GL."CHI_TIET_ID"
			AND FADS."TK_CO_ID" = GL."TAI_KHOAN_DOI_UNG_ID"
			AND FADS."TK_NO_ID" = GL."TAI_KHOAN_ID"

			AND ( GL."LOAI_HACH_TOAN" = '1'
				AND LEFT((select "SO_TAI_KHOAN" from danh_muc_he_thong_tai_khoan as TK where TK.id =   GL."TAI_KHOAN_ID"),
						3) IN ( '211',
						'213', '212',
						'217' )
				)

		WHERE   FADS.id IS NOT NULL  AND FA."id" = any (%(refTypeList)s) 

		UNION ALL
		SELECT  FA."id" ,

		GL."LOAI_CHUNG_TU" ,
		GL."NGAY_CHUNG_TU" ,
		GL."SO_CHUNG_TU" ,
		GL."DIEN_GIAI_CHUNG" ,
		GL."GHI_NO" AS "SO_TIEN" ,
		GL."TAI_KHOAN_ID" AS "TK_KHO" ,
		GL."TAI_KHOAN_DOI_UNG_ID" AS "TK_CO" ,
		FADS."THU_TU_SAP_XEP_CHI_TIET",
		FADS."LOAI_CHUNG_TU" AS "LOAI_CHUNG_TU_NGUON_GOC_HINH_THANH"
		FROM    asset_ghi_tang FA
		LEFT JOIN asset_ghi_tang_nguon_goc_hinh_thanh FADS ON FADS."TAI_SAN_CO_DINH_GHI_TANG_ID" = FA."id"
		LEFT JOIN so_cai_chi_tiet AS GL ON FADS."id" = GL."CHI_TIET_ID"
			AND ( GL."LOAI_HACH_TOAN" = '1'
				AND LEFT((select "SO_TAI_KHOAN" from danh_muc_he_thong_tai_khoan as TK where TK.id =   GL."TAI_KHOAN_ID"),
						3) IN ( '211',
						'213', '212',
						'217' )
				)

		WHERE
		FADS."TAI_SAN_CO_DINH_GHI_TANG_ID" IS NOT NULL
		AND FADS.id IS NULL
		AND
		FA."id" = any (%(refTypeList)s) 

		ORDER BY "THU_TU_SAP_XEP_CHI_TIET"
		;--DESC


		DROP TABLE IF EXISTS TMP_GHI_TANG_BO_PHAN_CAU_THANH_TSCD
		;

		CREATE TEMP TABLE TMP_GHI_TANG_BO_PHAN_CAU_THANH_TSCD
		AS
		SELECT  FA."id" ,
		FAD."BO_PHAN" ,
		FAD."DON_VI_TINH" ,
		FAD."SO_LUONG" ,
		FAD."THOI_HAN_BAO_HANH" ,
		fad."THU_TU_SAP_XEP_CHI_TIET"
		FROM    asset_ghi_tang FA
		LEFT JOIN asset_ghi_tang_bo_phan_cau_thanh FAD ON FAD."TAI_SAN_CO_DINH_GHI_TANG_ID" = FA."id"
		WHERE FA."id" = any (%(refTypeList)s) 


		ORDER BY fad."THU_TU_SAP_XEP_CHI_TIET" ;--DESC


		DROP TABLE IF EXISTS TMP_GHI_TANG_DUNG_CU_PHU_TUNG_TSCD
		;

		CREATE TEMP TABLE TMP_GHI_TANG_DUNG_CU_PHU_TUNG_TSCD
		AS
		SELECT  FA."id" ,
		FADA."TEN_QUY_CACH_DUNG_CU_PHU_TUNG" ,
		FADA."DON_VI_TINH" ,
		FADA."SO_LUONG" ,
		FADA."GIA_TRI" ,
		FADA."THU_TU_SAP_XEP_CHI_TIET"
		FROM    asset_ghi_tang FA
		LEFT JOIN asset_ghi_tang_dung_cu_phu_tung FADA ON FADA."TAI_SAN_CO_DINH_GHI_TANG_ID" = FA."id"
		WHERE FA."id" = any (%(refTypeList)s) 

		ORDER BY FADA."THU_TU_SAP_XEP_CHI_TIET"  ;--DESC

		END $$

		;


		SELECT

		*
		FROM TMP_GHI_TANG_BO_PHAN_CAU_THANH_TSCD GT

		;

		"""
		return self.execute(query,params_sql)


	def ham_lay_du_lieu_sql_tra_ve_detail_dcptkt(self,refTypeList):
		
		params_sql = {
		'refTypeList':refTypeList, 
		}  

		query = """
		DO LANGUAGE plpgsql $$
		DECLARE



		rec       RECORD;


		BEGIN

		DROP TABLE IF EXISTS TMP_GHI_TANG_TSCD
		;

		CREATE TEMP TABLE TMP_GHI_TANG_TSCD
		AS
		--Bảng FixedAsset
		SELECT  FA."id" ,
		FA."MA_TAI_SAN" ,
		FA."TEN_TAI_SAN" ,
		FC."MA" ,
		FC."TEN" ,
		FA."TINH_TRANG_GHI_TANG" ,
		FA."CHI_NHANH_ID" ,
		OU."MA_DON_VI" ,
		OU."TEN_DON_VI" ,

		FA."LOAI_CHUNG_TU" ,
		FA."NGAY_GHI_TANG" ,
		FA."SO_CT_GHI_TANG" ,
		FA."NGUYEN_GIA" ,
		FA."GIA_TRI_TINH_KHAU_HAO"
		FROM    asset_ghi_tang FA
		INNER JOIN danh_muc_loai_tai_san_co_dinh FC ON FC."id" = FA."LOAI_TAI_SAN_ID"
		LEFT JOIN danh_muc_to_chuc OU ON OU."id" = FA."DON_VI_SU_DUNG_ID"
		WHERE FA."id"  = any (%(refTypeList)s) 

		ORDER BY FA."NGAY_GHI_TANG" DESC ,
		FA."SO_CT_GHI_TANG" DESC ,
		fa."MA_TAI_SAN" ,
		fa."TEN_TAI_SAN" ;
		--Bảng FixedAssetDetailSource

		DROP TABLE IF EXISTS TMP_GHI_TANG_NGUON_GOC_HINH_THANH_TSCD
		;

		CREATE TEMP TABLE TMP_GHI_TANG_NGUON_GOC_HINH_THANH_TSCD
		AS
		SELECT
		FA."id" ,

		GL."LOAI_CHUNG_TU" ,
		GL."NGAY_CHUNG_TU" ,
		GL."SO_CHUNG_TU" ,
		GL."DIEN_GIAI_CHUNG" ,
		GL."GHI_NO" AS "SO_TIEN" ,
		GL."TAI_KHOAN_ID" AS "TK_NO" ,
		GL."TAI_KHOAN_DOI_UNG_ID" AS "TK_CO" ,
		FADS."THU_TU_SAP_XEP_CHI_TIET",
		FADS."LOAI_CHUNG_TU" AS "LOAI_CHUNG_TU_NGUON_GOC_HINH_THANH"
		FROM    asset_ghi_tang FA
		LEFT JOIN asset_ghi_tang_nguon_goc_hinh_thanh FADS ON FADS."TAI_SAN_CO_DINH_GHI_TANG_ID" = FA."id"
		LEFT JOIN so_cai_chi_tiet AS GL ON FADS.id = GL."CHI_TIET_ID"
		AND FADS."TK_CO_ID" = GL."TAI_KHOAN_DOI_UNG_ID"
		AND FADS."TK_NO_ID" = GL."TAI_KHOAN_ID"

		AND ( GL."LOAI_HACH_TOAN" = '1'
		AND LEFT((select "SO_TAI_KHOAN" from danh_muc_he_thong_tai_khoan as TK where TK.id =   GL."TAI_KHOAN_ID"),
		3) IN ( '211',
		'213', '212',
		'217' )
		)

		WHERE   FADS.id IS NOT NULL  AND FA."id"  = any (%(refTypeList)s) 

		UNION ALL
		SELECT  FA."id" ,

		GL."LOAI_CHUNG_TU" ,
		GL."NGAY_CHUNG_TU" ,
		GL."SO_CHUNG_TU" ,
		GL."DIEN_GIAI_CHUNG" ,
		GL."GHI_NO" AS "SO_TIEN" ,
		GL."TAI_KHOAN_ID" AS "TK_KHO" ,
		GL."TAI_KHOAN_DOI_UNG_ID" AS "TK_CO" ,
		FADS."THU_TU_SAP_XEP_CHI_TIET",
		FADS."LOAI_CHUNG_TU" AS "LOAI_CHUNG_TU_NGUON_GOC_HINH_THANH"
		FROM    asset_ghi_tang FA
		LEFT JOIN asset_ghi_tang_nguon_goc_hinh_thanh FADS ON FADS."TAI_SAN_CO_DINH_GHI_TANG_ID" = FA."id"
		LEFT JOIN so_cai_chi_tiet AS GL ON FADS."id" = GL."CHI_TIET_ID"
		AND ( GL."LOAI_HACH_TOAN" = '1'
		AND LEFT((select "SO_TAI_KHOAN" from danh_muc_he_thong_tai_khoan as TK where TK.id =   GL."TAI_KHOAN_ID"),
		3) IN ( '211',
		'213', '212',
		'217' )
		)

		WHERE
		FADS."TAI_SAN_CO_DINH_GHI_TANG_ID" IS NOT NULL
		AND FADS.id IS NULL
		AND
		FA."id"  = any (%(refTypeList)s) 

		ORDER BY "THU_TU_SAP_XEP_CHI_TIET"
		;--DESC


		DROP TABLE IF EXISTS TMP_GHI_TANG_BO_PHAN_CAU_THANH_TSCD
		;

		CREATE TEMP TABLE TMP_GHI_TANG_BO_PHAN_CAU_THANH_TSCD
		AS
		SELECT  FA."id" ,
		FAD."BO_PHAN" ,
		FAD."DON_VI_TINH" ,
		FAD."SO_LUONG" ,
		FAD."THOI_HAN_BAO_HANH" ,
		fad."THU_TU_SAP_XEP_CHI_TIET"
		FROM    asset_ghi_tang FA
		LEFT JOIN asset_ghi_tang_bo_phan_cau_thanh FAD ON FAD."TAI_SAN_CO_DINH_GHI_TANG_ID" = FA."id"
		WHERE FA."id"  = any (%(refTypeList)s) 


		ORDER BY fad."THU_TU_SAP_XEP_CHI_TIET" ;--DESC


		DROP TABLE IF EXISTS TMP_GHI_TANG_DUNG_CU_PHU_TUNG_TSCD
		;

		CREATE TEMP TABLE TMP_GHI_TANG_DUNG_CU_PHU_TUNG_TSCD
		AS
		SELECT  FA."id" ,
		FADA."TEN_QUY_CACH_DUNG_CU_PHU_TUNG" ,
		FADA."DON_VI_TINH" ,
		FADA."SO_LUONG" ,
		FADA."GIA_TRI" ,
		FADA."THU_TU_SAP_XEP_CHI_TIET"
		FROM    asset_ghi_tang FA
		LEFT JOIN asset_ghi_tang_dung_cu_phu_tung FADA ON FADA."TAI_SAN_CO_DINH_GHI_TANG_ID" = FA."id"
		WHERE FA."id"  = any (%(refTypeList)s) 

		ORDER BY FADA."THU_TU_SAP_XEP_CHI_TIET"  ;--DESC

		END $$

		;


		SELECT

		*
		FROM TMP_GHI_TANG_DUNG_CU_PHU_TUNG_TSCD GT

		;
		"""
		return self.execute(query,params_sql)


	

