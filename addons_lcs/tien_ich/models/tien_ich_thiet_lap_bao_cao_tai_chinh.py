# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_THIET_LAP_BAO_CAO_TAI_CHINH(models.Model):
	_name = 'tien.ich.thiet.lap.bao.cao.tai.chinh'
	_description = 'Thiết lập báo cáo tài chính'
	_inherit = ['mail.thread']

	MA_BAO_CAO = fields.Char(string='Mã báo cáo', help='Mã báo cáo')
	TEN_BAO_CAO = fields.Selection([('BANG_CAN_DOI_KE_TOAN', 'Bảng cân đối kế toán'), ('BAO_CAO_KET_QUA_HOAT_DONG_KINH_DOANH', 'Báo cáo kết quả hoạt động kinh doanh'), ('BAO_CAO_LUU_CHUYEN_TIEN_TE_TRUC_TIEP', 'Báo cáo lưu chuyển tiền tệ (theo phương pháp trực tiếp)'), ('BAO_CAO_LUU_CHUYEN_TIEN_TE_GIAN_TIEP', 'Báo cáo lưu chuyển tiền tệ (theo phương pháp gián tiếp)'), ('THUYET_MINH_BAO_CAO_TAI_CHINH', 'Thuyết minh báo cáo tài chính'), ('TINH_HINH_THUC_HIEN_NGHIA_VU_DOI_VOI_NHA_NUOC', 'Tình hình thực hiện nghĩa vụ đối với nhà nước'), ], string='Tên báo cáo', help='Tên báo cáo',default='BANG_CAN_DOI_KE_TOAN',required=True)
	name = fields.Char(string='Name', help='Name',related='MA_BAO_CAO',store=True, oldname='NAME')
	CHE_DO_KE_TOAN = fields.Char(string='Chế độ kế toán')
	TIEN_ICH_THUYET_MINH_BAO_CAO_TAI_CHINH_CHI_TIET_IDS = fields.One2many('tien.ich.thuyet.minh.bao.cao.tai.chinh.chi.tiet', 'CHI_TIET_ID_1', string='Thuyết minh báo cáo tài chính chi tiết')
	TIEN_ICH_BAO_CAO_TAI_CHINH_CHI_TIET_IDS = fields.One2many('tien.ich.bao.cao.tai.chinh.chi.tiet', 'CHI_TIET_ID', string='Báo cáo tài chính chi tiết')
	TIEN_ICH_TINH_HINH_THUC_HIEN_NGHIA_VU_DOI_VOI_NHA_NUOC_CHI_TIET_IDS = fields.One2many('tien.ich.thuc.hien.nghia.vu.doi.voi.nha.nuoc.chi.tiet', 'CHI_TIET_ID_2', string='Tình hình thực hiện nghĩa vụ đối với nhà nước chi tiết')

	THUYET_MINH_BAO_CAO_TAI_CHINH_TAB = fields.Selection([
        ('1', '1.Thông tin chung'),
        ('2', '2.Thông tin bổ sung'),
        ('3', '3.Đầu tư tài chính'),
		('4', '4.Phải thu khác'),
        ('5', '5.Nợ xấu'),
        ('6', '6.Hàng tồn kho'),
		('7', '7.TS dở dang dài hạn'),
        ('8', '8.TSCĐ hữu hình'),
        ('9', '9.TSCĐ vô hình'),
		('10', '10.TSCĐ thuê tài chính'),
        ('11', '11.Tăng giảm BĐS đầu tư'),
        ('12', '12.Các khoản vay'),
		('13', '13.Nợ thuê tài chính'),
		('14', '14.Thuế và các khoản phải nộp'),
        ('15', '15.Trái phiếu phát hành'),
        ('16', '16.Biến động vốn CSH'),
		('17', '17.Tài sản thiếu chờ xử lý'),
        ('18', '18. Phải trả người bán'),
        ], default='1', string='NO_SAVE')
		
	def thuc_hien_lay_gia_tri_mac_dinh(self, args):
		new_line = [[5]]
		if self.TEN_BAO_CAO =='BANG_CAN_DOI_KE_TOAN':
			listchitietmacdinh = self.env['tien.ich.bao.cao.tai.chinh.chi.tiet.mac.dinh'].search([('ReportID', '=', '1')])
			for chitietmacdinh in listchitietmacdinh:
				cong_thuc_tong_hop =[[5]]
				cong_thuc_tien_ich=[[5]]
				for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_XAY_DUNG_CONG_THUC_IDS:
					cong_thuc_tong_hop += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'MA_CHI_TIEU' : chitiet_baocaotcchitiet.MA_CHI_TIEU,
					'TEN_CHI_TIEU' : chitiet_baocaotcchitiet.TEN_CHI_TIEU,
				})]

				for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_XAY_DUNG_CONG_THUC_LCT_CHI_TIET_IDS:
					cong_thuc_tien_ich += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'KY_HIEU' : chitiet_baocaotcchitiet.KY_HIEU,
					'DIEN_GIAI' : chitiet_baocaotcchitiet.DIEN_GIAI,
					'TAI_KHOAN_ID' : chitiet_baocaotcchitiet.TAI_KHOAN_ID.id,
					'TK_DOI_UNG_ID' : chitiet_baocaotcchitiet.TK_DOI_UNG_ID.id,
				})]
				new_line += [(0,0,{
					'MA_CHI_TIEU': chitietmacdinh.MA_CHI_TIEU,
					'TEN_CHI_TIEU' : chitietmacdinh.TEN_CHI_TIEU,
					'TEN_TIENG_ANH' : chitietmacdinh.TEN_TIENG_ANH,
					'THUYET_MINH' : chitietmacdinh.THUYET_MINH,
					'LOAI_CHI_TIEU' : chitietmacdinh.LOAI_CHI_TIEU,
					'CONG_THUC' : chitietmacdinh.CONG_THUC,
					'KHONG_IN' : chitietmacdinh.KHONG_IN,
					'IN_DAM' : chitietmacdinh.IN_DAM,
					'IN_NGHIENG' : chitietmacdinh.IN_NGHIENG,
					'DA_SUA_CT_MAC_DINH' : chitietmacdinh.DA_SUA_CT_MAC_DINH,
					'SO_THU_TU' : chitietmacdinh.SO_THU_TU,
					'TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_TONG_HOP_IDS': cong_thuc_tong_hop ,
					'TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_CHI_TIET_IDS': cong_thuc_tien_ich,
					})]

			return {'TIEN_ICH_BAO_CAO_TAI_CHINH_CHI_TIET_IDS': new_line}
		elif self.TEN_BAO_CAO =='BAO_CAO_KET_QUA_HOAT_DONG_KINH_DOANH':
			listchitietmacdinh = self.env['tien.ich.bao.cao.tai.chinh.chi.tiet.mac.dinh'].search([('ReportID', '=', '2')])
			for chitietmacdinh in listchitietmacdinh:
				cong_thuc_tong_hop =[[5]]
				cong_thuc_tien_ich=[[5]]
				for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_XAY_DUNG_CONG_THUC_IDS:
					cong_thuc_tong_hop += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'MA_CHI_TIEU' : chitiet_baocaotcchitiet.MA_CHI_TIEU,
					'TEN_CHI_TIEU' : chitiet_baocaotcchitiet.TEN_CHI_TIEU,
				})]

				for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_XAY_DUNG_CONG_THUC_LCT_CHI_TIET_IDS:
					cong_thuc_tien_ich += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'KY_HIEU' : chitiet_baocaotcchitiet.KY_HIEU,
					'DIEN_GIAI' : chitiet_baocaotcchitiet.DIEN_GIAI,
					'TAI_KHOAN_ID' : chitiet_baocaotcchitiet.TAI_KHOAN_ID,
					'TK_DOI_UNG_ID' : chitiet_baocaotcchitiet.TK_DOI_UNG_ID,
				})]
				new_line += [(0,0,{
					'MA_CHI_TIEU': chitietmacdinh.MA_CHI_TIEU,
					'TEN_CHI_TIEU' : chitietmacdinh.TEN_CHI_TIEU,
					'TEN_TIENG_ANH' : chitietmacdinh.TEN_TIENG_ANH,
					'THUYET_MINH' : chitietmacdinh.THUYET_MINH,
					'LOAI_CHI_TIEU' : chitietmacdinh.LOAI_CHI_TIEU,
					'CONG_THUC' : chitietmacdinh.CONG_THUC,
					'KHONG_IN' : chitietmacdinh.KHONG_IN,
					'IN_DAM' : chitietmacdinh.IN_DAM,
					'IN_NGHIENG' : chitietmacdinh.IN_NGHIENG,
					'DA_SUA_CT_MAC_DINH' : chitietmacdinh.DA_SUA_CT_MAC_DINH,
					'SO_THU_TU' : chitietmacdinh.SO_THU_TU,
					'TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_TONG_HOP_IDS': cong_thuc_tong_hop ,
					'TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_CHI_TIET_IDS': cong_thuc_tien_ich,
					})]
			return {'TIEN_ICH_BAO_CAO_TAI_CHINH_CHI_TIET_IDS': new_line}
		elif self.TEN_BAO_CAO =='BAO_CAO_LUU_CHUYEN_TIEN_TE_TRUC_TIEP':
			listchitietmacdinh = self.env['tien.ich.bao.cao.tai.chinh.chi.tiet.mac.dinh'].search([('ReportID', '=', '3')])
			for chitietmacdinh in listchitietmacdinh:
				cong_thuc_tong_hop =[[5]]
				cong_thuc_tien_ich=[[5]]
				for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_XAY_DUNG_CONG_THUC_IDS:
					cong_thuc_tong_hop += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'MA_CHI_TIEU' : chitiet_baocaotcchitiet.MA_CHI_TIEU,
					'TEN_CHI_TIEU' : chitiet_baocaotcchitiet.TEN_CHI_TIEU,
				})]

				for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_XAY_DUNG_CONG_THUC_LCT_CHI_TIET_IDS:
					cong_thuc_tien_ich += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'KY_HIEU' : chitiet_baocaotcchitiet.KY_HIEU,
					'DIEN_GIAI' : chitiet_baocaotcchitiet.DIEN_GIAI,
					'TAI_KHOAN_ID' : chitiet_baocaotcchitiet.TAI_KHOAN_ID,
					'TK_DOI_UNG_ID' : chitiet_baocaotcchitiet.TK_DOI_UNG_ID,
				})]
				new_line += [(0,0,{
					'MA_CHI_TIEU': chitietmacdinh.MA_CHI_TIEU,
					'TEN_CHI_TIEU' : chitietmacdinh.TEN_CHI_TIEU,
					'TEN_TIENG_ANH' : chitietmacdinh.TEN_TIENG_ANH,
					'THUYET_MINH' : chitietmacdinh.THUYET_MINH,
					'LOAI_CHI_TIEU' : chitietmacdinh.LOAI_CHI_TIEU,
					'CONG_THUC' : chitietmacdinh.CONG_THUC,
					'KHONG_IN' : chitietmacdinh.KHONG_IN,
					'IN_DAM' : chitietmacdinh.IN_DAM,
					'IN_NGHIENG' : chitietmacdinh.IN_NGHIENG,
					'DA_SUA_CT_MAC_DINH' : chitietmacdinh.DA_SUA_CT_MAC_DINH,
					'SO_THU_TU' : chitietmacdinh.SO_THU_TU,
					'TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_TONG_HOP_IDS': cong_thuc_tong_hop ,
					'TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_CHI_TIET_IDS': cong_thuc_tien_ich,
					})]
			return {'TIEN_ICH_BAO_CAO_TAI_CHINH_CHI_TIET_IDS': new_line}
		elif self.TEN_BAO_CAO =='BAO_CAO_LUU_CHUYEN_TIEN_TE_GIAN_TIEP':
			listchitietmacdinh = self.env['tien.ich.bao.cao.tai.chinh.chi.tiet.mac.dinh'].search([('ReportID', '=', '6')])
			for chitietmacdinh in listchitietmacdinh:
				cong_thuc_tong_hop =[[5]]
				cong_thuc_tien_ich=[[5]]
				for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_XAY_DUNG_CONG_THUC_IDS:
					cong_thuc_tong_hop += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'MA_CHI_TIEU' : chitiet_baocaotcchitiet.MA_CHI_TIEU,
					'TEN_CHI_TIEU' : chitiet_baocaotcchitiet.TEN_CHI_TIEU,
				})]

				for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_XAY_DUNG_CONG_THUC_LCT_CHI_TIET_IDS:
					cong_thuc_tien_ich += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'KY_HIEU' : chitiet_baocaotcchitiet.KY_HIEU,
					'DIEN_GIAI' : chitiet_baocaotcchitiet.DIEN_GIAI,
					'TAI_KHOAN_ID' : chitiet_baocaotcchitiet.TAI_KHOAN_ID,
					'TK_DOI_UNG_ID' : chitiet_baocaotcchitiet.TK_DOI_UNG_ID,
				})]
				new_line += [(0,0,{
					'MA_CHI_TIEU': chitietmacdinh.MA_CHI_TIEU,
					'TEN_CHI_TIEU' : chitietmacdinh.TEN_CHI_TIEU,
					'TEN_TIENG_ANH' : chitietmacdinh.TEN_TIENG_ANH,
					'THUYET_MINH' : chitietmacdinh.THUYET_MINH,
					'LOAI_CHI_TIEU' : chitietmacdinh.LOAI_CHI_TIEU,
					'CONG_THUC' : chitietmacdinh.CONG_THUC,
					'KHONG_IN' : chitietmacdinh.KHONG_IN,
					'IN_DAM' : chitietmacdinh.IN_DAM,
					'IN_NGHIENG' : chitietmacdinh.IN_NGHIENG,
					'DA_SUA_CT_MAC_DINH' : chitietmacdinh.DA_SUA_CT_MAC_DINH,
					'SO_THU_TU' : chitietmacdinh.SO_THU_TU,
					'TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_TONG_HOP_IDS': cong_thuc_tong_hop ,
					'TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_CHI_TIET_IDS': cong_thuc_tien_ich,
					})]
			return {'TIEN_ICH_BAO_CAO_TAI_CHINH_CHI_TIET_IDS': new_line}
		elif self.TEN_BAO_CAO =='THUYET_MINH_BAO_CAO_TAI_CHINH':
			data = self.env['tien.ich.thuyet.minh.bao.cao.tai.chinh.chi.tiet.mac.dinh'].search([],limit=10)
			for line in data:
				cong_thuc_tong_hop_tmbctc =[[5]]
				cong_thuc_tien_ich_tmbctc=[[5]]
				for chitiet_baocaotcchitiet in line.TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_IDS:
					cong_thuc_tong_hop_tmbctc += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'MA_CHI_TIEU' : chitiet_baocaotcchitiet.MA_CHI_TIEU,
					'TEN_CHI_TIEU' : chitiet_baocaotcchitiet.TEN_CHI_TIEU,
				})]

				for chitiet_baocaotcchitiet in line.TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LCT_CHI_TIET_IDS:
					cong_thuc_tien_ich_tmbctc += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'KY_HIEU' : chitiet_baocaotcchitiet.KY_HIEU,
					'DIEN_GIAI' : chitiet_baocaotcchitiet.DIEN_GIAI,
					'TAI_KHOAN_ID' : chitiet_baocaotcchitiet.TAI_KHOAN_ID,
					'TK_DOI_UNG_ID' : chitiet_baocaotcchitiet.TK_DOI_UNG_ID,
				})]
				new_line += [(0,0,{
					'MA_CHI_TIEU': line.MA_CHI_TIEU,
					'TEN_CHI_TIEU' : line.TEN_CHI_TIEU,
					'TEN_TIENG_ANH' : line.TEN_TIENG_ANH,
					'NOI_DUNG' : line.NOI_DUNG,
					'LOAI_CHI_TIEU' : line.LOAI_CHI_TIEU,
					'THUOC_PHAN' : line.THUOC_PHAN,
					'KHONG_IN' : line.KHONG_IN,
					'IN_DAM' : line.IN_DAM,
					'IN_NGHIENG' : line.IN_NGHIENG,
					'CUOI_NAM' : line.CUOI_NAM,
					'DAU_NAM' : line.DAU_NAM,
					'GIA_TRI_HOP_LY_GHI_SO_CUOI_NAM' : line.GIA_TRI_HOP_LY_GHI_SO_CUOI_NAM,
					'DU_PHONG_CUOI_NAM' : line.DU_PHONG_CUOI_NAM,
					'DU_PHONG_DAU_NAM' : line.DU_PHONG_DAU_NAM,
					'NHA_CUA_VAT_CHAT_KIEN_TRUC' : line.NHA_CUA_VAT_CHAT_KIEN_TRUC,
					'PHUONG_TIEN_VAN_TAI_TRUYEN_DAN' : line.PHUONG_TIEN_VAN_TAI_TRUYEN_DAN,
					'CAY_LAU_NAM_SUC_VAT_LAM_VIEC_CHO_SAN_PHAM' : line.CAY_LAU_NAM_SUC_VAT_LAM_VIEC_CHO_SAN_PHAM,
					'KET_CAU_HA_TANG_DNNDTXD' : line.KET_CAU_HA_TANG_DNNDTXD,
					'TAI_SAN_CO_DINH_HUU_HINH_KHAC' : line.TAI_SAN_CO_DINH_HUU_HINH_KHAC,
					'TONG_CONG' : line.TONG_CONG,
					'SO_DAU_NAM' : line.SO_DAU_NAM,
					'SO_CUOI_NAM' : line.SO_CUOI_NAM,
					'SO_CUOI_NAM' : line.SO_CUOI_NAM,
					'GIA_TRI_DAU_NAM_12' : line.GIA_TRI_DAU_NAM_12,
					'GIAM_TRONG_NAM_12' : line.GIAM_TRONG_NAM_12,
					'TANG_TRONG_NAM_12' : line.TANG_TRONG_NAM_12,
					'GIA_TRI_CUOI_NAM_12' : line.GIA_TRI_CUOI_NAM_12,
					'CUOI_NAM_14' : line.CUOI_NAM_14,
					'DAU_NAM_14' : line.DAU_NAM_14,
					'GIA_TRI_DAU_NAM_15' : line.GIA_TRI_DAU_NAM_15,
					'GIA_TRI_CUOI_NAM_15' : line.GIA_TRI_CUOI_NAM_15,
					'GIA_TRI_DAU_NAM_17' : line.GIA_TRI_DAU_NAM_17,
					'GIA_TRI_CUOI_NAM_17' : line.GIA_TRI_CUOI_NAM_17,
					'GIA_TRI_CUOI_NAM_18' : line.GIA_TRI_CUOI_NAM_18,
					'TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_TONG_HOP_IDS': cong_thuc_tong_hop_tmbctc ,
					'TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_CHI_TIET_IDS': cong_thuc_tien_ich_tmbctc,
				})]
			return {'TIEN_ICH_THUYET_MINH_BAO_CAO_TAI_CHINH_CHI_TIET_IDS': new_line}
		else :
			listchitietmacdinh = self.env['tien.ich.thuc.hien.nghia.vu.doi.voi.nha.nuoc.mac.dinh'].search([])
			for chitietmacdinh in listchitietmacdinh:
				phai_nop_ky_truoc_cong_thuc_tong_hop =[[5]]
				phai_nop_ky_truoc_cong_thuc_chi_tiet=[[5]]
				phai_nop_trong_ky_cong_thuc_tong_hop =[[5]]
				phai_nop_trong_ky_cong_thuc_chi_tiet=[[5]]
				da_nop_trong_ky_cong_thuc_tong_hop =[[5]]
				da_nop_trong_ky_cong_thuc_chi_tiet=[[5]]
				for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_TONG_HOP_MD_IDS:
					phai_nop_ky_truoc_cong_thuc_tong_hop += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'MA_CHI_TIEU' : chitiet_baocaotcchitiet.MA_CHI_TIEU,
					'TEN_CHI_TIEU' : chitiet_baocaotcchitiet.TEN_CHI_TIEU,
				})]


				for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_TONG_HOP_MD_IDS:
					phai_nop_trong_ky_cong_thuc_tong_hop += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'MA_CHI_TIEU' : chitiet_baocaotcchitiet.MA_CHI_TIEU,
					'TEN_CHI_TIEU' : chitiet_baocaotcchitiet.TEN_CHI_TIEU,
				})]


				for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_TONG_HOP_MD_IDS:
					da_nop_trong_ky_cong_thuc_tong_hop += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'MA_CHI_TIEU' : chitiet_baocaotcchitiet.MA_CHI_TIEU,
					'TEN_CHI_TIEU' : chitiet_baocaotcchitiet.TEN_CHI_TIEU,
				})]


				for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_CHI_TIET_MD_IDS:
					phai_nop_ky_truoc_cong_thuc_chi_tiet += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'KY_HIEU' : chitiet_baocaotcchitiet.KY_HIEU,
					'DIEN_GIAI' : chitiet_baocaotcchitiet.DIEN_GIAI,
					'TAI_KHOAN_ID' : chitiet_baocaotcchitiet.TAI_KHOAN_ID,
					'TK_DOI_UNG_ID' : chitiet_baocaotcchitiet.TK_DOI_UNG_ID,
				})]

				for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_CHI_TIET_MD_IDS:
					phai_nop_trong_ky_cong_thuc_chi_tiet += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'KY_HIEU' : chitiet_baocaotcchitiet.KY_HIEU,
					'DIEN_GIAI' : chitiet_baocaotcchitiet.DIEN_GIAI,
					'TAI_KHOAN_ID' : chitiet_baocaotcchitiet.TAI_KHOAN_ID,
					'TK_DOI_UNG_ID' : chitiet_baocaotcchitiet.TK_DOI_UNG_ID,
				})]
					
				for chitiet_baocaotcchitiet in chitietmacdinh.TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_CHI_TIET_MD_IDS:
					da_nop_trong_ky_cong_thuc_chi_tiet += [(0,0,{
					'PHEP_TINH': chitiet_baocaotcchitiet.PHEP_TINH,
					'KY_HIEU' : chitiet_baocaotcchitiet.KY_HIEU,
					'DIEN_GIAI' : chitiet_baocaotcchitiet.DIEN_GIAI,
					'TAI_KHOAN_ID' : chitiet_baocaotcchitiet.TAI_KHOAN_ID,
					'TK_DOI_UNG_ID' : chitiet_baocaotcchitiet.TK_DOI_UNG_ID,
				})]
				
				new_line += [(0,0,{
					'MA_CHI_TIEU': chitietmacdinh.MA_CHI_TIEU,
					'TEN_CHI_TIEU' : chitietmacdinh.TEN_CHI_TIEU,
					'TEN_TIENG_ANH' : chitietmacdinh.TEN_TIENG_ANH,
					'LOAI_CHI_TIEU' : chitietmacdinh.LOAI_CHI_TIEU,
					'SO_CON_PHAI_NOP_KY_TRUOC_CHUYEN_SANG' : chitietmacdinh.SO_CON_PHAI_NOP_KY_TRUOC_CHUYEN_SANG,
					'SO_PHAI_NOP_TRONG_KY' : chitietmacdinh.SO_PHAI_NOP_TRONG_KY,
					'SO_DA_NOP_TRONG_KY' : chitietmacdinh.SO_DA_NOP_TRONG_KY,
					'KHONG_IN' : chitietmacdinh.KHONG_IN,
					'IN_DAM' : chitietmacdinh.IN_DAM,
					'IN_NGHIENG' : chitietmacdinh.IN_NGHIENG,
					'THONG_TU' : chitietmacdinh.THONG_TU,
					'XAY_DUNG_CONG_THUC' : chitietmacdinh.XAY_DUNG_CONG_THUC,
					'SO_THU_TU' : chitietmacdinh.SO_THU_TU,
					'TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_CHI_TIET_IDS' : phai_nop_trong_ky_cong_thuc_chi_tiet,
					'TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_TONG_HOP_IDS' : phai_nop_trong_ky_cong_thuc_tong_hop,
					'TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_CHI_TIET_IDS' : da_nop_trong_ky_cong_thuc_chi_tiet,
					'TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_TONG_HOP_IDS' : phai_nop_ky_truoc_cong_thuc_tong_hop,
					'TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_CHI_TIET_IDS' : phai_nop_ky_truoc_cong_thuc_chi_tiet,
					'TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_TONG_HOP_IDS' : da_nop_trong_ky_cong_thuc_tong_hop,
				})]
			return {'TIEN_ICH_TINH_HINH_THUC_HIEN_NGHIA_VU_DOI_VOI_NHA_NUOC_CHI_TIET_IDS': new_line}

	def thuc_hien_lay_bao_cao_theo_ma_bao_cao(self, args):
		ma_bao_cao = args['ma_bao_cao']
		id_bao_cao = self.env['tien.ich.thiet.lap.bao.cao.tai.chinh'].search([('MA_BAO_CAO', '=', ma_bao_cao)],limit=1).id
		return id_bao_cao

	
	
		
			




