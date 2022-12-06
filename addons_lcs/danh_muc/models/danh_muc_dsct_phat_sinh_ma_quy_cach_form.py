# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_DSCT_PHAT_SINH_MA_QUY_CACH_FORM(models.Model):
	_name = 'danh.muc.dsct.phat.sinh.ma.quy.cach.form'
	_description = ''
	_auto = False

	name = fields.Char(string='Name', help='Name', oldname='NAME')
	#FIELD_IDS = fields.One2many('model.name', copy=True)
	#@api.model
	#def default_get(self, fields_list):
	#   result = super(DANH_MUC_DSCT_PHAT_SINH_MA_QUY_CACH_FORM, self).default_get(fields_list)
	#   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
	#   return result
	DANH_MUC_DSCT_PHAT_SINH_MA_QUY_CACH_CHI_TIET_IDS = fields.One2many('danh.muc.dsct.phat.sinh.ma.quy.cach.chi.tiet', 'CHI_TIET_ID', string='DSCT phát sinh mã quy cách chi tiết', copy=True)

	def lay_danh_sach_ma_quy_cach(self,args):
		new_line = [[5]]
		if (args['ma_vat_tu_hang_hoa']):
			id_vat_tu_hang_hoa = self.env['danh.muc.vat.tu.hang.hoa'].search([('MA', '=', args['ma_vat_tu_hang_hoa'])],limit=1).id
			param = {
				'id_vat_tu_hang_hoa':id_vat_tu_hang_hoa
				}
			record =[]
			query = """
			DO LANGUAGE plpgsql $$
			DECLARE
			tham_so_vthh_id INTEGER:= %(id_vat_tu_hang_hoa)s;
			BEGIN
			DROP TABLE IF EXISTS TMP_KET_QUA;
			CREATE TEMP TABLE TMP_KET_QUA
			AS
			SELECT
				DISTINCT VSV."ID_GOC" ,
				VSV."LOAI_CHUNG_TU" ,
				VSV."NGAY_CHUNG_TU" ,
				VSV."NGAY_HACH_TOAN" ,
				VSV."SO_CHUNG_TU" ,
				VSV."DIEN_GIAI" ,
				OU.name AS "TEN_CHI_NHANH"
			FROM    tien_ich_tim_kiem_chung_tu AS VSV
				INNER JOIN danh_muc_reftype AS SRT ON VSV."LOAI_CHUNG_TU" = SRT."REFTYPE"
				INNER JOIN danh_muc_to_chuc AS OU ON VSV."CHI_NHANH_ID" = OU.id
				INNER JOIN ( SELECT DISTINCT
						ISN."NHAP_XUAT_KHO_CHI_TIET_ID" AS "ID_CHUNG_TU",
						IIW."LA_PHIEU_NHAP_HANG_TRA_LAI" ,
						IIW."LA_PHIEU_XUAT_BAN_HANG"
					FROM   stock_ex_chung_tu_luu_ma_quy_cach AS ISN
						LEFT JOIN stock_ex_nhap_xuat_kho AS IIW ON ISN."ID_CHUNG_TU" = IIW.id
									AND (IIW."LOAI_CHUNG_TU" = 2013 or IIW."LOAI_CHUNG_TU" = 2020)
			--             WHERE  ISN."VAT_TU_HANG_HOA_ID" = tham_so_vthh_id
					) AS ISN ON VSV."CHI_TIET_ID" = ISN."ID_CHUNG_TU"
			WHERE   coalesce(ISN."LA_PHIEU_NHAP_HANG_TRA_LAI", FALSE ) <> TRUE
				AND coalesce(ISN."LA_PHIEU_XUAT_BAN_HANG", FALSE ) <> TRUE
			ORDER BY VSV."NGAY_HACH_TOAN", VSV."NGAY_CHUNG_TU", VSV."SO_CHUNG_TU";
			END $$;

			SELECT *FROM TMP_KET_QUA;
			
					""" 
			record = self.execute(query, param)
			for line in record:
				new_line += [(0,0,{
					'NGAY_HACH_TOAN' : line.get('NGAY_HACH_TOAN'),
					'NGAY_CHUNG_TU' : line.get('NGAY_CHUNG_TU'),
					'SO_CHUNG_TU_SO_TC' : line.get('SO_CHUNG_TU'),
					'SO_CHUNG_TU_SO_QT' : line.get('SO_CHUNG_TU'),
					'DIEN_GIAI' : line.get('DIEN_GIAI'),
					'LOAI_CHUNG_TU' : line.get('LOAI_CHUNG_TU'),
					'CHI_NHANH' : line.get('TEN_CHI_NHANH'),
					})]
		return new_line

