# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class STOCK_EX_CHUNG_TU_LUU_MA_QUY_CACH(models.Model):
	_name = 'stock.ex.chung.tu.luu.ma.quy.cach'
	_description = ''
	_inherit = ['mail.thread']
	MA_QUY_CACH = fields.Char(string='Mã quy cách', help='Mã quy cách')
	TEN_MA_QUY_CACH = fields.Char(string='Tên mã quy cách', help='Tên mã quy cách')
	ID_CHUNG_TU = fields.Integer(string='Id chứng từ', help='Id chứng từ')
	name = fields.Char(string='Name', help='Name', oldname='NAME')
	KHO_NHAP = fields.Many2one('danh.muc.kho', string='Kho nhập, kho trả lại', help='Kho nhập, kho trả lại')
	KHO_XUAT_ID = fields.Many2one('danh.muc.kho', string='Kho xuất', help='Kho xuất')
	LOAI_SERI = fields.Selection([('0', 'Loại 0'), ('1', 'Loại 1')], string='SerialType')
	VAT_TU_HANG_HOA_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Vật tư hàng hóa', help='Vật tư hàng hóa')
	NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán')
	CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc')
	CHI_TIET_ID = fields.Integer(string='ID chứng từ chi tiết', help='ID chứng từ chi tiết')
	LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')
	SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='Số chứng từ')
	

	SO_LUONG_NHAP = fields.Float(string='Số lượng nhập', help='Số lượng nhập', digits=decimal_precision.get_precision('SO_LUONG'))
	SO_LUONG_XUAT = fields.Float(string='Số lượng xuất', help='Số lượng xuất', digits=decimal_precision.get_precision('SO_LUONG'))
	MAU_SAC = fields.Char(string='Màu sắc', help='Màu sắc')
	KICH_CO = fields.Char(string='Kích cỡ', help='Kích cỡ')
	SO_LUONG_TON = fields.Float(string='Số lượng tốt', help='Số lượng tốt', digits=decimal_precision.get_precision('SO_LUONG'))
	SO_LUONG_KIEM_KE = fields.Float(string='Số lượng theo kiểm kê', help='Số lượng theo kiểm kê', digits=decimal_precision.get_precision('SO_LUONG'))

	MA_QUY_CACH_1 = fields.Char(string='Mã quy cách 1', help='Mã quy cách 1')
	MA_QUY_CACH_2 = fields.Char(string='Mã quy cách 1', help='Mã quy cách 2')
	MA_QUY_CACH_3 = fields.Char(string='Mã quy cách 1', help='Mã quy cách 3')
	MA_QUY_CACH_4 = fields.Char(string='Mã quy cách 1', help='Mã quy cách 4')
	MA_QUY_CACH_5 = fields.Char(string='Mã quy cách 1', help='Mã quy cách 5')

	NHAP_XUAT_KHO_CHI_TIET_ID = fields.Many2one('stock.ex.nhap.xuat.kho.chi.tiet', string='Nhập xuất kho chi tiết', help='Nhập xuất kho chi tiết', ondelete='cascade')
	KIEM_KE_KHO_CHI_TIET_ID = fields.Many2one('stock.ex.bang.kiem.ke.vthh.can.dieu.chinh.chi.tiet.form', string='Kiểm kê kho chi tiết', help='Kiểm kê kho chi tiết', ondelete='set null')

	@api.model
	def default_get(self, fields):
		rec = super(STOCK_EX_CHUNG_TU_LUU_MA_QUY_CACH, self).default_get(fields)
		# du_lieu = self.lay_du_lieu_phan_bo(1,3568)
		# if du_lieu:
		#     for line in du_lieu:
		#         rec['KHO_NHAP'] = line.get('KHO_NHAP')
		#         rec['MA_QUY_CACH_1'] = line.get('MA_QUY_CACH_1')
		#         rec['MA_QUY_CACH_2'] = line.get('MA_QUY_CACH_2')
		#         rec['SO_LUONG_TON'] = line.get('SO_LUONG_TON')
		#         rec['SO_LUONG_XUAT'] = line.get('SO_LUONG_XUAT')
		return rec

	

	def lay_du_lieu_phan_bo(self,loai_serial,loai_chung_tu):
		record = []
		params = {
			'DEN_NGAY':'2019-03-05',
			'CHI_NHANH_ID' : self.get_chi_nhanh(),
			'MA_HANG_ID' : 714,
			'ID_CHUNG_TU' : 1,
			'CHI_TIET_ID' : 1,
			'LOAI_SERIAL' : '2',
			'KHO_ID' : 94,
			}
		if loai_serial == 4:
			query = """   
				SELECT 
				0 AS "SO_HIEU_TREN_SO_ID" ,
				ISN."VAT_TU_HANG_HOA_ID" ,
				ISN."MA_QUY_CACH_1" ,
				ISN."MA_QUY_CACH_2" ,
				ISN."MA_QUY_CACH_3" ,
				ISN."MA_QUY_CACH_4" ,
				ISN."MA_QUY_CACH_5" ,
				ISN."KHO_NHAP" ,
				SUM(coalesce(CASE WHEN ISN."CHI_TIET_ID" <> %(CHI_TIET_ID)s THEN 0 ELSE ISN."SO_LUONG_NHAP" END,0)) AS "SO_LUONG_XUAT" ,
				SUM(coalesce( CASE WHEN ISN."LOAI_SERI" = '2' then ISN."SO_LUONG_XUAT" ELSE 0 END,0)) - SUM(coalesce(CASE WHEN ISN."CHI_TIET_ID" = %(CHI_TIET_ID)s OR ISN."LOAI_SERI" <> '4' THEN 0 ELSE ISN."SO_LUONG_NHAP" END,0)) AS "SO_LUONG_NHAP" ,
				CAST(0 AS BIT) AS Selected,
				/*Tổng số lượng đã chọn xuất trên chứng từ hiện tại, không kể dòng Detail đang nhập liệu*/
				SUM(coalesce(CASE WHEN ISN."ID_CHUNG_TU" = 112 AND ISN."CHI_TIET_ID" <> %(CHI_TIET_ID)s THEN ISN."SO_LUONG_XUAT" ELSE 0 END,0)) AS "SL_XUAT_THEO_CHUNG_TU_CHI_TIET"
		FROM	stock_ex_chung_tu_luu_ma_quy_cach ISN
		WHERE	ISN."VAT_TU_HANG_HOA_ID" = %(MA_HANG_ID)s
				AND (	
						ISN."NGAY_HACH_TOAN" < %(DEN_NGAY)s
						OR 
						(	ISN."NGAY_HACH_TOAN" = %(DEN_NGAY)s
							AND 
							(%(ID_CHUNG_TU)s IS NULL OR ISN."ID_CHUNG_TU" <= %(ID_CHUNG_TU)s)
						)
					) 
				AND ISN."CHI_NHANH_ID" = %(CHI_NHANH_ID)s
				AND (ISN."LOAI_SERI" = '4' OR ISN."LOAI_SERI" = '2')
		GROUP BY 
				ISN."VAT_TU_HANG_HOA_ID" ,
				ISN."MA_QUY_CACH_1" ,
				ISN."MA_QUY_CACH_2" ,
				ISN."MA_QUY_CACH_3" ,
				ISN."MA_QUY_CACH_4" ,
				ISN."MA_QUY_CACH_5" ,
				ISN."KHO_NHAP"
		--REM BY LDNGOC 08.12.2015: vẫn lấy lên các dòng tồn < 0 và lên form tính toán số lượng tồn ngay tại thời điểm nhập liệu và ẩn các dòng tồn <= 0 đi
		--HAVING	SUM(coalesce( CASE WHEN ISN."LOAI_SERI" = '2' then ISN."SO_LUONG_XUAT" ELSE 0 END,0)) - SUM(coalesce(CASE WHEN ISN."CHI_TIET_ID" = %(CHI_TIET_ID)s OR ISN."LOAI_SERI" <> '4' THEN 0 ELSE ISN."SO_LUONG_NHAP" END,0)) > 0
		ORDER BY 
				ISN."MA_QUY_CACH_1" ,
				ISN."MA_QUY_CACH_2" ,
				ISN."MA_QUY_CACH_3" ,
				ISN."MA_QUY_CACH_4" ,
				ISN."MA_QUY_CACH_5" 
				

			"""  
		elif loai_serial == 2 or (loai_serial == 3 and loai_chung_tu == 3568):
			query = """   

				SELECT
				0 AS "SO_HIEU_TREN_SO_ID" ,
				ISN."VAT_TU_HANG_HOA_ID" ,
				ISN."MA_QUY_CACH_1" ,
				ISN."MA_QUY_CACH_2" ,
				ISN."MA_QUY_CACH_3" ,
				ISN."MA_QUY_CACH_4" ,
				ISN."MA_QUY_CACH_5" ,
				ISN."KHO_NHAP" ,
				-- kdchien 06.06.2018:189377: Số lượng tồn MQC  =  Tổng nhập kho - Chuyển kho - Số lượng đã xuất hóa đơn thông thường - Số lượng đã xuất hóa đơn điều chỉnh tăng + Số lượng đã xuất hóa đơn điều chỉnh giảm
				SUM(coalesce(ISN."SO_LUONG_NHAP",0)) - SUM(coalesce(CASE WHEN ISN."CHI_TIET_ID" = %(CHI_TIET_ID)s THEN 0 ELSE ISN."SO_LUONG_XUAT" END,0)) AS "SO_LUONG_TON" ,
				SUM(coalesce(CASE WHEN ISN."CHI_TIET_ID" <> %(CHI_TIET_ID)s THEN 0 ELSE ISN."SO_LUONG_XUAT" END,0)) AS "SO_LUONG_XUAT",
				CAST(0 AS BIT) AS Selected,
				/*Tổng số lượng đã chọn xuất trên chứng từ hiện tại, không kể dòng Detail đang nhập liệu*/
				SUM(coalesce(CASE WHEN ISN."ID_CHUNG_TU" = %(ID_CHUNG_TU)s AND ISN."CHI_TIET_ID" <> %(CHI_TIET_ID)s THEN ISN."SO_LUONG_XUAT" ELSE 0 END,0)) AS "SL_XUAT_THEO_CHUNG_TU_CHI_TIET"
		FROM	stock_ex_chung_tu_luu_ma_quy_cach ISN
				LEFT JOIN danh_muc_kho S ON ISN."KHO_NHAP" = S.id
				LEFT JOIN sale_document_line AS SVD ON SVD.id = ISN."CHI_TIET_ID"
				LEFT JOIN sale_document AS SV ON SV.id = SVD."SALE_DOCUMENT_ID"
		WHERE	ISN."VAT_TU_HANG_HOA_ID" = 594
				AND (	ISN."NGAY_HACH_TOAN" < %(DEN_NGAY)s
						OR
						(	ISN."NGAY_HACH_TOAN" = %(DEN_NGAY)s
							AND
							(%(ID_CHUNG_TU)s IS NULL OR ISN."ID_CHUNG_TU" <= %(ID_CHUNG_TU)s)
						)
					)
				AND (	ISN."LOAI_SERI" = %(LOAI_SERIAL)s
						OR ISN."LOAI_SERI" = '0'
						OR ( ISN."LOAI_SERI" = '1'
							AND ISN."LOAI_CHUNG_TU" IN (2030,2031,3032)
							)

						OR (%(LOAI_SERIAL)s = '3'										-- KDCHIEN 21.06.2018:230433:Chứng từ bán hàng kèm hóa đơn_Lỗi hóa đơn lập kèm chứng từ không lưu mã quy cách đã chọn khi lập chứng từ
							AND (ISN."LOAI_SERI" = '2' AND SV."LAP_KEM_HOA_DON" = TRUE )	-- Nếu hóa đơn thông thường thì lấy các MQC của chứng từ bán hàng kèm hóa đơn
							)

					) --57368 Thêm điều kiện trừ đi các mã quy cách được chuyển sang kho khác
				AND ISN."CHI_NHANH_ID" = %(CHI_NHANH_ID)s
	   GROUP BY
			ISN."VAT_TU_HANG_HOA_ID" ,
			ISN."MA_QUY_CACH_1" ,
			ISN."MA_QUY_CACH_2" ,
			ISN."MA_QUY_CACH_3" ,
			ISN."MA_QUY_CACH_4" ,
			ISN."MA_QUY_CACH_5" ,
			ISN."KHO_NHAP" ,
			S."MA_KHO"
		--REM BY LDNGOC 08.12.2015: vẫn lấy lên các dòng tồn < 0 và lên form tính toán số lượng tồn ngay tại thời điểm nhập liệu và ẩn các dòng tồn <= 0 đi
		--HAVING SUM(coalesce(ISN."SO_LUONG_NHAP",0)) - SUM(coalesce(CASE WHEN ISN."CHI_TIET_ID" = %(CHI_TIET_ID)s THEN 0 ELSE ISN."SO_LUONG_XUAT" END,0)) > 0
		ORDER BY S."MA_KHO",
				ISN."MA_QUY_CACH_1" ,
				ISN."MA_QUY_CACH_2" ,
				ISN."MA_QUY_CACH_3" ,
				ISN."MA_QUY_CACH_4" ,
				ISN."MA_QUY_CACH_5"

			"""  
		elif loai_serial == 3 and loai_chung_tu == 3568:
			query = """   

				SELECT
				0 AS "SO_HIEU_TREN_SO_ID" ,
				ISN."VAT_TU_HANG_HOA_ID" ,
				ISN."MA_QUY_CACH_1" ,
				ISN."MA_QUY_CACH_2" ,
				ISN."MA_QUY_CACH_3" ,
				ISN."MA_QUY_CACH_4" ,
				ISN."MA_QUY_CACH_5" ,
				ISN."KHO_NHAP" ,
				SUM(coalesce(CASE WHEN ISN."CHI_TIET_ID" = %(CHI_TIET_ID)s THEN 0 ELSE ISN."SO_LUONG_XUAT" END,0))
				/*hoant 13.06.2018 sửa lỗi 230473*/
				- SUM(coalesce(SA."SO_LUONG_NHAP",0))
				 AS "SO_LUONG_TON" ,
				SUM(coalesce(CASE WHEN ISN."CHI_TIET_ID" <> %(CHI_TIET_ID)s THEN 0 ELSE ISN."SO_LUONG_XUAT" END,0)) AS "SO_LUONG_XUAT",
				CAST(0 AS BIT) AS Selected,
				/*Tổng số lượng đã chọn xuất trên chứng từ hiện tại, không kể dòng Detail đang nhập liệu*/
				SUM(coalesce(CASE WHEN ISN."ID_CHUNG_TU" = %(ID_CHUNG_TU)s AND ISN."CHI_TIET_ID" <> %(CHI_TIET_ID)s THEN ISN."SO_LUONG_XUAT" ELSE 0 END,0)) AS "SL_XUAT_THEO_CHUNG_TU_CHI_TIET"
		FROM	stock_ex_chung_tu_luu_ma_quy_cach ISN
				LEFT JOIN danh_muc_kho S ON ISN."KHO_NHAP" = S.id
				/*hoant 13.06.2018 sửa lỗi 230473*/
				LEFT JOIN
					(
						SELECT	INS1."VAT_TU_HANG_HOA_ID",
								INS1."MA_QUY_CACH_1",
								INS1."MA_QUY_CACH_2",
								INS1."MA_QUY_CACH_3",
								INS1."MA_QUY_CACH_4",
								INS1."MA_QUY_CACH_5",
								SUM(coalesce(INS1."SO_LUONG_NHAP", 0)) AS "SO_LUONG_NHAP"
						from stock_ex_chung_tu_luu_ma_quy_cach INS1
						INNER JOIN sale_ex_hoa_don_ban_hang AS SA ON SA.id = INS1."ID_CHUNG_TU"
						WHERE	SA.id = 1
								AND SA."LOAI_CHUNG_TU" = 3568
								AND INS1."VAT_TU_HANG_HOA_ID" = %(MA_HANG_ID)s
								AND INS1."CHI_NHANH_ID" = %(CHI_NHANH_ID)s
								AND INS1."CHI_TIET_ID" <> %(CHI_TIET_ID)s
						GROUP BY
								INS1."VAT_TU_HANG_HOA_ID",
								INS1."MA_QUY_CACH_1",
								INS1."MA_QUY_CACH_2",
								INS1."MA_QUY_CACH_3",
								INS1."MA_QUY_CACH_4",
								INS1."MA_QUY_CACH_5"
					) AS SA ON ISN."VAT_TU_HANG_HOA_ID" = SA."VAT_TU_HANG_HOA_ID"
								AND coalesce(ISN."MA_QUY_CACH_1", '') = coalesce(SA."MA_QUY_CACH_1", '')
								AND coalesce(ISN."MA_QUY_CACH_2", '') = coalesce(SA."MA_QUY_CACH_2", '')
								AND coalesce(ISN."MA_QUY_CACH_3", '') = coalesce(SA."MA_QUY_CACH_3", '')
								AND coalesce(ISN."MA_QUY_CACH_4", '') = coalesce(SA."MA_QUY_CACH_4", '')
								AND coalesce(ISN."MA_QUY_CACH_5", '') = coalesce(SA."MA_QUY_CACH_5", '')
		WHERE	ISN."VAT_TU_HANG_HOA_ID" = %(MA_HANG_ID)s
-- 				AND ISN."ID_CHUNG_TU" = coalesce(@temp"ID_CHUNG_TU",@Adjust"ID_CHUNG_TU")
				AND ISN."CHI_NHANH_ID" = %(CHI_NHANH_ID)s
	   GROUP BY
			ISN."VAT_TU_HANG_HOA_ID" ,
			ISN."MA_QUY_CACH_1" ,
			ISN."MA_QUY_CACH_2" ,
			ISN."MA_QUY_CACH_3" ,
			ISN."MA_QUY_CACH_4" ,
			ISN."MA_QUY_CACH_5" ,
			ISN."KHO_NHAP" ,
			S."MA_KHO"
		ORDER BY S."MA_KHO",
				ISN."MA_QUY_CACH_1" ,
				ISN."MA_QUY_CACH_2" ,
				ISN."MA_QUY_CACH_3" ,
				ISN."MA_QUY_CACH_4" ,
				ISN."MA_QUY_CACH_5"

			"""  
		else:
			query = """   

				SELECT
				0 AS "SO_HIEU_TREN_SO_ID" ,
				ISN."VAT_TU_HANG_HOA_ID" ,
				ISN."MA_QUY_CACH_1" ,
				ISN."MA_QUY_CACH_2" ,
				ISN."MA_QUY_CACH_3" ,
				ISN."MA_QUY_CACH_4" ,
				ISN."MA_QUY_CACH_5" ,
				ISN."KHO_NHAP" ,
				SUM(coalesce(ISN."SO_LUONG_NHAP",0)) - SUM(coalesce(CASE WHEN ISN."CHI_TIET_ID" = %(CHI_TIET_ID)s THEN 0 ELSE ISN."SO_LUONG_XUAT" END,0)) AS "SO_LUONG_TON" ,
				SUM(coalesce(CASE WHEN ISN."CHI_TIET_ID" <> %(CHI_TIET_ID)s THEN 0 ELSE ISN."SO_LUONG_XUAT" END,0)) AS "SO_LUONG_XUAT",
				CAST(0 AS BIT) AS Selected,
				/*Tổng số lượng đã chọn xuất trên chứng từ hiện tại, không kể dòng Detail đang nhập liệu*/
				SUM(coalesce(CASE WHEN ISN."ID_CHUNG_TU" = %(ID_CHUNG_TU)s AND ISN."CHI_TIET_ID" <> %(CHI_TIET_ID)s THEN ISN."SO_LUONG_XUAT" ELSE 0 END,0)) AS "SL_XUAT_THEO_CHUNG_TU_CHI_TIET"
		FROM	stock_ex_chung_tu_luu_ma_quy_cach ISN
				LEFT JOIN danh_muc_kho S ON ISN."KHO_NHAP" = S.id
		WHERE
				ISN."VAT_TU_HANG_HOA_ID" = %(MA_HANG_ID)s
				AND (%(KHO_ID)s IS NULL OR ISN."KHO_NHAP" = %(KHO_ID)s)
				AND (	ISN."NGAY_HACH_TOAN" < %(DEN_NGAY)s
						OR
						(	ISN."NGAY_HACH_TOAN" = %(DEN_NGAY)s
--							AND
--							(%(ID_CHUNG_TU)s IS NULL OR ISN."ID_CHUNG_TU" <= %(ID_CHUNG_TU)s)
						)
					)
				AND ISN."CHI_NHANH_ID" = %(CHI_NHANH)s
	   GROUP BY
				ISN."VAT_TU_HANG_HOA_ID" ,
				ISN."MA_QUY_CACH_1" ,
				ISN."MA_QUY_CACH_2" ,
				ISN."MA_QUY_CACH_3" ,
				ISN."MA_QUY_CACH_4" ,
				ISN."MA_QUY_CACH_5" ,
				ISN."KHO_NHAP" ,
				S."MA_KHO"
		--REM BY LDNGOC 08.12.2015: vẫn lấy lên các dòng tồn < 0 và lên form tính toán số lượng tồn ngay tại thời điểm nhập liệu và ẩn các dòng tồn <= 0 đi
		--HAVING	SUM(coalesce(ISN."SO_LUONG_NHAP",0)) - SUM(coalesce(CASE WHEN ISN."CHI_TIET_ID" = %(CHI_TIET_ID)s THEN 0 ELSE ISN."SO_LUONG_XUAT" END,0)) > 0
		ORDER BY
				S."MA_KHO",
				ISN."MA_QUY_CACH_1" ,
				ISN."MA_QUY_CACH_2" ,
				ISN."MA_QUY_CACH_3" ,
				ISN."MA_QUY_CACH_4" ,
				ISN."MA_QUY_CACH_5"

			"""  
		cr = self.env.cr

		cr.execute(query, params)
		for line in [{d.name: row[i] for i, d in enumerate(cr.description)} for row in cr.fetchall()]:
			record.append({
				'VAT_TU_HANG_HOA_ID': line.get('VAT_TU_HANG_HOA_ID', ''),
				'MA_QUY_CACH_1': line.get('MA_QUY_CACH_1', ''),
				'MA_QUY_CACH_2': line.get('MA_QUY_CACH_2', ''),
				'MA_QUY_CACH_3': line.get('MA_QUY_CACH_3', ''),
				'SO_LUONG_TON': line.get('SO_LUONG_TON', ''),
				'SO_LUONG_XUAT': line.get('SO_LUONG_XUAT', ''),
			})
		
		return record