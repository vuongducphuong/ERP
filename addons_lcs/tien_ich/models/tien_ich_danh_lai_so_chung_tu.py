# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError

class TIEN_ICH_DANH_LAI_SO_CHUNG_TU(models.Model):
	_name = 'tien.ich.danh.lai.so.chung.tu'
	_description = 'Đánh lại số chứng từ'
	_auto = False

	KHOANG_THOI_GIAN = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI',required=True)
	TU_NGAY = fields.Date(string='Từ', help='Từ ngày' ,default=fields.Datetime.now,required=True)
	DEN_NGAY = fields.Date(string='Đến', help='Đến ngày',default=fields.Datetime.now,required=True)
	BAO_GOM_CHUNG_TU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm chứng từ chi nhánh phụ thuộc', help='Bao gồm chứng từ chi nhánh phụ thuộc',default='True')
	# LOAI_CHUNG_TU = fields.Selection([('PHIEU_THU', 'Phiếu thu'), ('PHIEU_CHI', ' Phiếu chi'), ('KIEM_KE_QUY', ' Kiểm kê quỹ'), ('THU_TIEN_GUI', ' Thu tiền gửi'), ('UY_NHIEM_CHI', ' Ủy nhiệm chi'), ('SEC_TIEN_MAT', ' Séc tiền mặt'), ('SEC_CHUYEN_KHOAN', ' Séc chuyển khoản'), ('CHUYEN_TIEN_NOI_BO', ' Chuyển tiền nội bộ'), ('NHAP_KHO', ' Nhập kho'), ('XUAT_KHO', ' Xuất kho'), ('CHUYEN_KHO', ' Chuyển kho'), ('LENH_SAN_XUAT', ' Lệnh sản xuất   '), ], string='Loại chứng từ', help='Loại chứng từ',default='PHIEU_THU', required=True)
	NHOM_LOAI_CHUNG_TU_ID = fields.Many2one('danh.muc.nhom.chung.tu', string='Loại chứng từ', help='Loại chứng từ')
	TIEN_TO = fields.Char(string='Tiền tố', help='Tiền tố')
	GIA_TRI_BAT_DAU_PHAN_SO = fields.Integer(string='Giá trị bắt đầu phần số', help='Giá trị bắt đầu phần số')
	TONG_SO_KY_TU_PHAN_SO = fields.Integer(string='Tổng số ký tự phần số', help='Tổng số ký tự phần số')
	HAU_TO = fields.Char(string='Hậu tố', help='Hậu tố')
	name = fields.Char(string='Name', help='Name', oldname='NAME')

	TIEN_ICH_DANH_LAI_SO_CHUNG_TU_CHI_TIET_IDS = fields.One2many('tien.ich.danh.lai.so.chung.tu.chi.tiet', 'DANH_LAI_SO_CHUNG_TU_ID', string='Đánh lại số chứng từ chi tiết')
	
	

	@api.onchange('KHOANG_THOI_GIAN')
	def laychungtu(self):
		self.onchange_time(self.KHOANG_THOI_GIAN, 'TU_NGAY', 'DEN_NGAY')

	@api.model
	def default_get(self, fields):
		rec = super(TIEN_ICH_DANH_LAI_SO_CHUNG_TU, self).default_get(fields)
		rec['NHOM_LOAI_CHUNG_TU_ID'] = self.env['danh.muc.nhom.chung.tu'].search([('TEN_NHOM_LOAI_CHUNG_TU', '=like', 'Phiếu thu%')],limit=1).id
		return rec

	
	@api.model
	def lay_du_lieu_khi_click(self, args):
		new_line = [[5]]
		du_lieu = self.lay_du_lieu_chung_tu(args.get('nhom_loai_ct_id'),args.get('tu_ngay'),args.get('den_ngay'))
		if du_lieu:
			for line in du_lieu:
				ref_type = self.env['danh.muc.reftype'].search([('REFTYPE', '=', line.get('LOAI_CHUNG_TU'))],limit=1).REFTYPENAME
				new_line += [(0,0,{
					'LOAI_CHUNG_TU' : ref_type,
					'NGAY_HACH_TOAN' : line.get('NGAY_HACH_TOAN'),
					'NGAY_CHUNG_TU' : line.get('NGAY_CHUNG_TU'),
					'SO_CHUNG_TU' : line.get('SO_CHUNG_TU'),
					'SO_HOA_DON' : line.get('SO_HOA_DON',''),
					'DIEN_GIAI' : line.get('DIEN_GIAI',''),
					'ID_GOC' : line.get('ID_GOC'),
					'MODEL_GOC' : line.get('MODEL_GOC'),
					'ID_AND_MODEL' : line.get('ID_AND_MODEL'),
					'REF_TYPE' : line.get('LOAI_CHUNG_TU'),
					})]
		return {'TIEN_ICH_DANH_LAI_SO_CHUNG_TU_CHI_TIET_IDS': new_line}

	@api.model
	def btn_cat(self, args):
		arr_chi_tiet = []
		cac_chung_tu_trung = ''
		if args.get('chi_tiet_ids'):
			for chi_tiet in args.get('chi_tiet_ids'):
				arr_chi_tiet.append(chi_tiet.get('ID_AND_MODEL'))
			list_chung_tu = tuple(arr_chi_tiet)
			for ct in args.get('chi_tiet_ids'):
				dem = self.check_so_chung_tu(list_chung_tu,ct.get('SO_CHUNG_TU_MOI'))
				if dem[0].get('DEM') > 0:
					if cac_chung_tu_trung == '':
						cac_chung_tu_trung = str(ct.get('SO_CHUNG_TU_MOI'))
					else:
						cac_chung_tu_trung += ',' + str(ct.get('SO_CHUNG_TU_MOI'))
			if cac_chung_tu_trung == '':
				for line in args.get('chi_tiet_ids'):
					if line.get('SO_CHUNG_TU_MOI'):
						self.env[line.get('MODEL_GOC')].search([('id', '=', line.get('ID_GOC'))], limit=1).write({'SO_CHUNG_TU' : line.get('SO_CHUNG_TU_MOI')})
						# self.cap_nhat_cac_so(line.get('ID_GOC'),line.get('REF_TYPE'),line.get('SO_CHUNG_TU'),line.get('SO_CHUNG_TU_MOI'))
			else:
				raise ValidationError("Số chứng từ <"+cac_chung_tu_trung+"> đã tồn tại, Đánh lại số chứng từ không thành công.")


	def check_so_chung_tu(self,list_chung_tu,so_ct_moi):
		params = {
			'LIST_CHUNG_TU' : list_chung_tu,
			'SO_CHUNG_TU_MOI' : so_ct_moi,
			}
		query = """  

			SELECT count(*) AS "DEM" FROM tien_ich_tim_kiem_chung_tu
			WHERE "ID_AND_MODEL" not in %(LIST_CHUNG_TU)s
			AND "SO_CHUNG_TU" = %(SO_CHUNG_TU_MOI)s
		"""  
		return self.execute(query, params)

	def lay_du_lieu_chung_tu(self,nhom_ct,tu_ngay,den_ngay):
		params = {
			'ID_NHOM_CHUNG_TU' : nhom_ct,
			'TU_NGAY' : tu_ngay,
			'DEN_NGAY' : den_ngay,
			}

		query = """   

			SELECT *FROM tien_ich_tim_kiem_chung_tu
			WHERE "LOAI_CHUNG_TU" IN
				(
					SELECT "REFTYPE"
					FROM danh_muc_reftype
					WHERE id IN (
							SELECT danh_muc_reftype_id
							FROM danh_muc_nhom_chung_tu_danh_muc_reftype_rel
							WHERE danh_muc_nhom_chung_tu_id = %(ID_NHOM_CHUNG_TU)s
					)
				)
			AND "NGAY_HACH_TOAN" BETWEEN %(TU_NGAY)s AND %(DEN_NGAY)s

		"""  
		return self.execute(query, params)


	def cap_nhat_cac_so(self,id_chung_tu,loai_ct,so_ct_cu,so_chung_tu_moi):
		params = {
			'ID_CHUNG_TU' : id_chung_tu,
			'LOAI_CT' : loai_ct,
			'SO_CHUNG_TU_CU' : so_ct_cu,
			'SO_CHUNG_TU_MOI' : so_chung_tu_moi,
			}
		query = """


			DO LANGUAGE plpgsql $$
			DECLARE

			tham_so_id_chung_tu INTEGER:= %(ID_CHUNG_TU)s;
			tham_so_loai_chung_tu INTEGER:= %(LOAI_CT)s;
			tham_so_so_chung_tu_cu VARCHAR(50):= %(SO_CHUNG_TU_CU)s;
			tham_so_so_chung_tu_moi VARCHAR(50):= %(SO_CHUNG_TU_MOI)s;

			tham_so_ref_no VARCHAR(50):= '';
			tham_so_ref_no_2 VARCHAR(50):= '';

			BEGIN

			-- IF tham_so_loai_chung_tu in ( 307, 308, 309, 310, 319, 320, 321, 322 )
			-- THEN
			--   SELECT "SO_CHUNG_TU" INTO tham_so_ref_no
			--   FROM purchase_document
			--   WHERE id = tham_so_id_chung_tu
			--   FETCH FIRST 1 ROW ONLY;
			--
			--   UPDATE so_cai_chi_tiet
			--   SET "SO_CHUNG_TU" = tham_so_ref_no
			--   WHERE "ID_CHUNG_TU" = tham_so_id_chung_tu;
			-- END IF;
			-- -- Hàng mua trả lại qua kho thanh toán bằng tiền mặt
			-- IF tham_so_loai_chung_tu in (3031)
			-- THEN
			--   SELECT "SO_CHUNG_TU" INTO tham_so_ref_no
			--   FROM purchase_ex_tra_lai_hang_mua
			--   WHERE id = tham_so_id_chung_tu;
			--   UPDATE so_cai_chi_tiet
			--   SET "SO_CHUNG_TU" = tham_so_ref_no
			--   WHERE id = tham_so_id_chung_tu;
			-- END IF;
			-- 2. Cập nhập sổ công nợ
			UPDATE so_cong_no_chi_tiet
			SET "SO_CHUNG_TU" = tham_so_so_chung_tu_moi
			WHERE id = tham_so_id_chung_tu;
			-- 3. Cập nhập sổ TSCD
			UPDATE so_tscd_chi_tiet
			SET "SO_CHUNG_TU" = tham_so_so_chung_tu_moi
			WHERE "ID_CHUNG_TU" = tham_so_id_chung_tu;

			-- 4. Cập nhập sổ Cái
			-- Trường hợp này vẫn tạm chấp nhận update dựa theo oldRefNo giống 2012. Khi nào có cơ chế cập nhập lại refno theo config thì sửa lại
			UPDATE so_cai_chi_tiet
			SET "SO_CHUNG_TU" = tham_so_so_chung_tu_moi
			WHERE "ID_CHUNG_TU" = tham_so_id_chung_tu;

			-- 5. Cập nhập sổ Kho
			UPDATE so_kho_chi_tiet
			SET "SO_CHUNG_TU" = tham_so_so_chung_tu_moi
			WHERE "ID_CHUNG_TU" = tham_so_id_chung_tu;

			-- 6. Cập nhập sổ Mua hàng
			UPDATE so_mua_hang_chi_tiet
			SET "SO_CHUNG_TU" = tham_so_so_chung_tu_moi
			WHERE "ID_CHUNG_TU" = tham_so_id_chung_tu;

			-- 7. Cập nhập sổ Bán hàng
			UPDATE so_ban_hang_chi_tiet
			SET "SO_CHUNG_TU" = tham_so_so_chung_tu_moi
			WHERE "ID_CHUNG_TU" = tham_so_id_chung_tu;

			--  8. Cập nhập sổ CCDC
			UPDATE so_ccdc_chi_tiet
			SET "SO_CHUNG_TU" = tham_so_so_chung_tu_moi
			WHERE "ID_CHUNG_TU" = tham_so_id_chung_tu;

			--   9. Cập nhập sổ thuế
			UPDATE so_thue_chi_tiet
			SET "SO_CHUNG_TU" = tham_so_so_chung_tu_moi
			WHERE "ID_CHUNG_TU" = tham_so_id_chung_tu;

			-- 10. Cập nhập thu/trả tiền
			UPDATE sale_ex_doi_tru_chi_tiet
			SET "SO_CHUNG_TU_CONG_NO" = cast(tham_so_so_chung_tu_moi AS VARCHAR(50))
			WHERE "ID_CHUNG_TU_CONG_NO" = tham_so_id_chung_tu;

			UPDATE sale_ex_doi_tru_chi_tiet
			SET "SO_CHUNG_TU_THANH_TOAN" = tham_so_so_chung_tu_moi
			WHERE "ID_CHUNG_TU_THANH_TOAN" = tham_so_id_chung_tu;
			-- 11.Cập nhập chứng từ ghi sổ
			UPDATE tong_hop_chung_tu_ghi_so
			SET "SO_CHUNG_TU" = tham_so_so_chung_tu_moi
			WHERE id = tham_so_id_chung_tu;
			-- Cập nhập đánh giá tk ngoại tệ
			--   UPDATE danh_gia_lai_tai_khoan_ngoai_te
			--   SET "SO_CHUNG_TU" = tham_so_so_chung_tu_moi
			--   WHERE id = tham_so_id_chung_tu;
			PERFORM CAP_NHAT_SO_THUE();

			END $$;

			-- SELECT *FROM TMP_SO_DONG;


		"""  
		return self.execute(query,params)
	   

	# @api.multi  
	# def action_invoice_open(self):
	#     gt_bat_dau_phan_so = self.GIA_TRI_BAT_DAU_PHAN_SO
	#     tien_to = self.TIEN_TO
	#     hau_to = self.HAU_TO 
	#     str_0= ''
	#     tong_gia_tri_phan_so = self.TONG_SO_KY_TU_PHAN_SO
	#     for listct in self.TIEN_ICH_DANH_LAI_SO_CHUNG_TU_CHI_TIET_IDS:
			
	#         str_0 = '0' * (tong_gia_tri_phan_so - len(str(gt_bat_dau_phan_so)))

	#         listct.SO_CHUNG_TU_MOI = str(tien_to) + str_0 + str(gt_bat_dau_phan_so) + str(hau_to)
	#         gt_bat_dau_phan_so += 1
		

	# @api.model
	# def create(self, vals):
	#     # line = super(TIEN_ICH_DANH_LAI_SO_CHUNG_TU, self).create(vals)
	#     for line in vals.get('TIEN_ICH_DANH_LAI_SO_CHUNG_TU_CHI_TIET_IDS'):
	#         chung_tu = self.env['account.ex.phieu.thu.chi'].search([('SO_CHUNG_TU','=', line[2].get('SO_CHUNG_TU'))], limit=1)
	#         if chung_tu :
	#             chung_tu.write({'SO_CHUNG_TU':line[2].get('SO_CHUNG_TU_MOI')})

	
			

		
