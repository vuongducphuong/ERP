# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, helper

MODULE = 'base_import_ex'


class Import(models.TransientModel):
	_inherit = 'base_import_ex.import'

	# Thiết lập báo cáo tài chính chi tiết mặc định

	def _import_FRTemplateDefault(self, tag):
		rec_model = 'tien.ich.bao.cao.tai.chinh.chi.tiet.mac.dinh'
		res = { }
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'ItemID':
				rec_id = child.text 
				res['ID_CHI_TIEU'] = child.text.lower()
			elif child.tag == 'ReportID':
				res['ReportID'] = int(child.text)
			elif child.tag == 'ItemIndex':
				res['SO_THU_TU'] = int(child.text)
			elif child.tag == 'ItemCode':
				res['MA_CHI_TIEU'] = child.text
			elif child.tag == 'ItemName':
				res['TEN_CHI_TIEU'] = child.text
			elif child.tag == 'ItemNameEnglish':
				res['TEN_TIENG_ANH'] = child.text
			elif child.tag == 'Description':
				res['THUYET_MINH'] = child.text
			elif child.tag == 'FormulaType':
				res['LOAI_CHI_TIEU'] = child.text
			elif child.tag == 'FormulaFrontEnd':
				res['CONG_THUC'] = child.text
			elif child.tag == 'Formula':
				res['TIEN_ICH_XAY_DUNG_CONG_THUC_IDS'] = [[5]]
				res['TIEN_ICH_XAY_DUNG_CONG_THUC_LCT_CHI_TIET_IDS'] = [[5]]
				for child_root in child.getchildren():
					if child_root.tag == 'root':
						for child_master_formular in child_root.getchildren():
							if child_master_formular.tag == 'MasterFormula':
								guid = child_master_formular.attrib.get('ItemID').lower() if child_master_formular.attrib.get('ItemID') != None else ''
								res['TIEN_ICH_XAY_DUNG_CONG_THUC_IDS'] += [(0,0,{
									'MA_CHI_TIEU': child_master_formular.attrib.get('ItemCode'),
									'TEN_CHI_TIEU':  guid + '_,_' + child_master_formular.attrib.get('ItemName'),
									'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
									'ID_CHI_TIEU': guid,
								})]
							elif child_master_formular.tag == 'DetailFormula':
								text_tk = '' 
								text_tk_du = ''
								tk_fomuala_details =False
								tk_ud_fomuala_details =False
								if child_master_formular.attrib.get('AccountNumber'):
									text_tk = child_master_formular.attrib.get('AccountNumber')
									tk_fomuala_details =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', text_tk)], limit=1).id
								if child_master_formular.attrib.get('CorrespondingAccountNumber'):
									text_tk_du = child_master_formular.attrib.get('CorrespondingAccountNumber')
									tk_ud_fomuala_details = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', text_tk_du)], limit=1).id
								res['TIEN_ICH_XAY_DUNG_CONG_THUC_LCT_CHI_TIET_IDS'] += [(0,0,{
									'KY_HIEU': child_master_formular.attrib.get('OperandString'),
									'DIEN_GIAI': child_master_formular.attrib.get('Description'),
									'TAI_KHOAN_ID':tk_fomuala_details,
									'TK_DOI_UNG_ID': tk_ud_fomuala_details,
									'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
								})]
			
			elif child.tag == 'AccountingSystem':
				res['THONG_TU'] = child.text
			elif child.tag == 'Hidden':
				res['KHONG_IN'] = True if child.text == '1' else False
			elif child.tag == 'IsBold':
				res['IN_DAM'] = True if child.text == '1' else False
			elif child.tag == 'IsItalic':
				res['IN_NGHIENG'] = True if child.text == '1' else False
			elif child.tag == 'IsEdited':
				res['DA_SUA_CT_MAC_DINH'] = True if child.text == '1' else False
			
		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

	# Thiết lập báo cáo tài chính thuyết minh báo cáo tài chính chi tiết mặc định

	def _import_FRB09DNTemplateDefault(self, tag):
		rec_model = 'tien.ich.thuyet.minh.bao.cao.tai.chinh.chi.tiet.mac.dinh'
		res = { }
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'ItemID':
				rec_id = child.text 
			elif child.tag == 'ItemCode':
				res['MA_CHI_TIEU'] = child.text
			elif child.tag == 'ItemIndex':
				res['SO_THU_TU'] = int(child.text)
			elif child.tag == 'ItemName':
				res['TEN_CHI_TIEU'] = child.text
			elif child.tag == 'Description':
				res['NOI_DUNG'] = child.text
			elif child.tag == 'ItemNameEnglish':
				res['TEN_TIENG_ANH'] = child.text
			elif child.tag == 'FormulaType':
				res['LOAI_CHI_TIEU'] = child.text
			elif child.tag == 'Part':
				res['THUOC_PHAN'] = child.text
			elif child.tag == 'Hidden':
				res['KHONG_IN'] = True if child.text == '1' else False
			elif child.tag == 'IsBold':
				res['IN_DAM'] = True if child.text == '1' else False
			elif child.tag == 'IsItalic':
				res['IN_NGHIENG'] = True if child.text == '1' else False
			elif child.tag == 'PartInTab':
				res['PART_IN_TAB'] = int(child.text)
			elif child.tag == 'ClosingBalance':
				res['CUOI_NAM'] = child.text
			elif child.tag == 'OpeningBalance':
				res['DAU_NAM'] = child.text
			elif child.tag == 'Equipment_IssueRight_TotalPayAndCapital':
				res['DU_PHONG_CUOI_NAM'] = child.text
			elif child.tag == 'Equipment_Trademark_PayDebitThisYearAndOtherCapital':
				res['PHUONG_TIEN_VAN_TAI_TRUYEN_DAN'] = child.text
			elif child.tag == 'Transport_CopyRight_PayInterestAndDecrease':
				res['DU_PHONG_DAU_NAM'] = child.text
			elif child.tag == 'License_PayInterestLastYearAndRevalueFA':
				res['CAY_LAU_NAM_SUC_VAT_LAM_VIEC_CHO_SAN_PHAM'] = child.text
			elif child.tag == 'IntFA_OrtherIntFA_PayDebitLastYearAndDiffExchangeRate':
				res['KET_CAU_HA_TANG_DNNDTXD'] = child.text
			elif child.tag == 'OtherFA_Software_TotalPayLastYearAndTreasuryShare':
				res['TAI_SAN_CO_DINH_HUU_HINH_KHAC'] = child.text
			elif child.tag == 'Total':
				res['TONG_CONG'] = child.text
			elif child.tag == 'BuildingAndRealty':
				res['NHA_CUA_VAT_CHAT_KIEN_TRUC'] = child.text
			elif child.tag == 'Formula':
				res['TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_IDS'] = [[5]]
				res['TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LCT_CHI_TIET_IDS'] = [[5]]
				for child_root in child.getchildren():
					if child_root.tag == 'root':
						for child_master_formular in child_root.getchildren():
							if child_master_formular.tag == 'MasterFormula':
								res['TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_IDS'] += [(0,0,{
									'MA_CHI_TIEU': child_master_formular.attrib.get('ItemCode'),
									'TEN_CHI_TIEU': child_master_formular.attrib.get('ItemName'),
									'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
								})]
							elif child_master_formular.tag == 'DetailFormula':
								text_tk = '' 
								text_tk_du = ''
								tk_fomuala_details =False
								tk_ud_fomuala_details =False
								if child_master_formular.attrib.get('AccountNumber'):
									text_tk = child_master_formular.attrib.get('AccountNumber')
									tk_fomuala_details =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', text_tk)], limit=1).id
								if child_master_formular.attrib.get('CorrespondingAccountNumber'):
									text_tk_du = child_master_formular.attrib.get('CorrespondingAccountNumber')
									tk_ud_fomuala_details = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', text_tk_du)], limit=1).id
								if child_master_formular.attrib.get('FormulaColumnName') =='ClosingBalance' or child_master_formular.attrib.get('FormulaColumnName') =='OpeningBalance' or child_master_formular.attrib.get('FormulaColumnName') =='Equipment_IssueRight_TotalPayAndCapital' or child_master_formular.attrib.get('FormulaColumnName') =='Equipment_Trademark_PayDebitThisYearAndOtherCapital' or child_master_formular.attrib.get('FormulaColumnName') =='Transport_CopyRight_PayInterestAndDecrease' or child_master_formular.attrib.get('FormulaColumnName') =='License_PayInterestLastYearAndRevalueFA' or child_master_formular.attrib.get('FormulaColumnName') =='IntFA_OrtherIntFA_PayDebitLastYearAndDiffExchangeRate' or child_master_formular.attrib.get('FormulaColumnName') =='OtherFA_Software_TotalPayLastYearAndTreasuryShare' or child_master_formular.attrib.get('FormulaColumnName') =='Total' or child_master_formular.attrib.get('FormulaColumnName') =='BuildingAndRealty' :
								
									res['TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LCT_CHI_TIET_IDS'] += [(0,0,{
										'KY_HIEU': child_master_formular.attrib.get('OperandString'),
										'DIEN_GIAI': child_master_formular.attrib.get('Description'),
										'TAI_KHOAN_ID':tk_fomuala_details,
										'TK_DOI_UNG_ID': tk_ud_fomuala_details,
										'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
									})]
		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

	# Thiết lập báo cáo tài chính thực hiện nghĩa vụ đối với nhà nước chi tiết mặc định

	def _import_FRObligationToGovTemplateDefault(self, tag):
		rec_model = 'tien.ich.thuc.hien.nghia.vu.doi.voi.nha.nuoc.mac.dinh'
		res = { }
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'ItemID':
				rec_id = child.text 
			elif child.tag == 'ItemIndex':
				res['SO_THU_TU'] = int(child.text)
			elif child.tag == 'ItemCode':
				res['MA_CHI_TIEU'] = child.text
			elif child.tag == 'ItemName':
				res['TEN_CHI_TIEU'] = child.text
			elif child.tag == 'ItemNameEnglish':
				res['TEN_TIENG_ANH'] = child.text
			elif child.tag == 'FormulaType':
				res['LOAI_CHI_TIEU'] = child.text
			elif child.tag == 'UnPaidOfPrevPeriodAmount':
				res['SO_CON_PHAI_NOP_KY_TRUOC_CHUYEN_SANG'] = child.text
			elif child.tag == 'PayableAmount':
				res['SO_PHAI_NOP_TRONG_KY'] = child.text
			elif child.tag == 'PaidAmount':
				res['SO_DA_NOP_TRONG_KY'] = child.text
			elif child.tag == 'Formula':
				res['TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_CHI_TIET_MD_IDS'] = [[5]]
				res['TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_TONG_HOP_MD_IDS'] = [[5]]
				res['TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_CHI_TIET_MD_IDS'] = [[5]]
				res['TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_TONG_HOP_MD_IDS'] = [[5]]
				res['TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_CHI_TIET_MD_IDS'] = [[5]]
				res['TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_TONG_HOP_MD_IDS'] = [[5]]
				for child_root in child.getchildren():
					if child_root.tag == 'root':
						for child_master_formular in child_root.getchildren():
							if child_master_formular.tag == 'MasterFormula':
								res['TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_TONG_HOP_MD_IDS'] += [(0,0,{
									'MA_CHI_TIEU': child_master_formular.attrib.get('ItemCode'),
									'TEN_CHI_TIEU': child_master_formular.attrib.get('ItemName'),
									'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
								})]
								res['TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_TONG_HOP_MD_IDS'] += [(0,0,{
									'MA_CHI_TIEU': child_master_formular.attrib.get('ItemCode'),
									'TEN_CHI_TIEU': child_master_formular.attrib.get('ItemName'),
									'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
								})]
								res['TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_TONG_HOP_MD_IDS'] += [(0,0,{
									'MA_CHI_TIEU': child_master_formular.attrib.get('ItemCode'),
									'TEN_CHI_TIEU': child_master_formular.attrib.get('ItemName'),
									'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
								})]
							elif child_master_formular.tag == 'DetailFormula':
								text_tk = '' 
								text_tk_du = ''
								tk_fomuala_details =False
								tk_ud_fomuala_details =False
								if child_master_formular.attrib.get('AccountNumber'):
									text_tk = child_master_formular.attrib.get('AccountNumber')
									tk_fomuala_details =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', text_tk)], limit=1).id
								if child_master_formular.attrib.get('CorrespondingAccountNumber'):
									text_tk_du = child_master_formular.attrib.get('CorrespondingAccountNumber')
									tk_ud_fomuala_details = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', text_tk_du)], limit=1).id
								if child_master_formular.attrib.get('FormulaColumnName') =='UnPaidOfPrevPeriodAmount':
									res['TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_CHI_TIET_MD_IDS'] += [(0,0,{
										'KY_HIEU': child_master_formular.attrib.get('OperandString'),
										'DIEN_GIAI': child_master_formular.attrib.get('Description'),
										'TAI_KHOAN_ID':tk_fomuala_details,
										'TK_DOI_UNG_ID': tk_ud_fomuala_details,
										'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
									})]
								elif child_master_formular.attrib.get('FormulaColumnName') =='PayableAmount':
									res['TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_CHI_TIET_MD_IDS'] += [(0,0,{
										'KY_HIEU': child_master_formular.attrib.get('OperandString'),
										'DIEN_GIAI': child_master_formular.attrib.get('Description'),
										'TAI_KHOAN_ID':tk_fomuala_details,
										'TK_DOI_UNG_ID': tk_ud_fomuala_details,
										'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
									})]
								elif child_master_formular.attrib.get('FormulaColumnName') =='PaidAmount':
									res['TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_CHI_TIET_MD_IDS'] += [(0,0,{
										'KY_HIEU': child_master_formular.attrib.get('OperandString'),
										'DIEN_GIAI': child_master_formular.attrib.get('Description'),
										'TAI_KHOAN_ID':tk_fomuala_details,
										'TK_DOI_UNG_ID': tk_ud_fomuala_details,
										'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
									})]
			elif child.tag == 'Hidden':
				res['KHONG_IN'] = True if child.text == '1' else False
			elif child.tag == 'IsBold':
				res['IN_DAM'] = True if child.text == '1' else False
			elif child.tag == 'IsItalic':
				res['IN_NGHIENG'] = True if child.text == '1' else False
			elif child.tag == 'Formula':
				res['XAY_DUNG_CONG_THUC'] = child.text
			elif child.tag == 'AccountingSystem':
				res['THONG_TU'] = child.text
			
		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

	# import Tiện ích thiết lập báo cáo tài chính chi tiết
	def _import_FRTemplate(self, tag):
		rec_model = 'tien.ich.bao.cao.tai.chinh.chi.tiet'
		res = { }
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'ItemID':
				rec_id = child.text 
				res['ID_CHI_TIEU'] = child.text.lower()
			elif child.tag == 'ReportID':
				res['ReportID'] = int(child.text)
			elif child.tag == 'ItemIndex':
				res['SO_THU_TU'] = int(child.text)
			elif child.tag == 'ItemCode':
				res['MA_CHI_TIEU'] = child.text
			elif child.tag == 'ItemName':
				res['TEN_CHI_TIEU'] = child.text
			elif child.tag == 'ItemNameEnglish':
				res['TEN_TIENG_ANH'] = child.text
			elif child.tag == 'Description':
				res['THUYET_MINH'] = child.text
			elif child.tag == 'FormulaType':
				res['LOAI_CHI_TIEU'] = child.text
			elif child.tag == 'FormulaFrontEnd':
				res['CONG_THUC'] = child.text
			elif child.tag == 'Formula':
				res['TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_TONG_HOP_IDS'] = [[5]]
				res['TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_CHI_TIET_IDS'] = [[5]]
				for child_root in child.getchildren():
					if child_root.tag == 'root':
						for child_master_formular in child_root.getchildren():
							if child_master_formular.tag == 'MasterFormula':
								guid = child_master_formular.attrib.get('ItemID').lower() if child_master_formular.attrib.get('ItemID') != None else ''
								res['TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_TONG_HOP_IDS'] += [(0,0,{
									'MA_CHI_TIEU': child_master_formular.attrib.get('ItemCode'),
									'TEN_CHI_TIEU': guid + '_,_' +child_master_formular.attrib.get('ItemName'),
									'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
									'ID_CHI_TIEU': guid,
								})]
							elif child_master_formular.tag == 'DetailFormula':
								text_tk = '' 
								text_tk_du = ''
								tk_fomuala_details =False
								tk_ud_fomuala_details =False
								if child_master_formular.attrib.get('AccountNumber'):
									text_tk = child_master_formular.attrib.get('AccountNumber')
									tk_fomuala_details =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', text_tk)], limit=1).id
								if child_master_formular.attrib.get('CorrespondingAccountNumber'):
									text_tk_du = child_master_formular.attrib.get('CorrespondingAccountNumber')
									tk_ud_fomuala_details = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', text_tk_du)], limit=1).id
								res['TIEN_ICH_XAY_DUNG_CONG_THUC_LOAI_CHI_TIEU_CHI_TIET_IDS'] += [(0,0,{
									'KY_HIEU': child_master_formular.attrib.get('OperandString'),
									'DIEN_GIAI': child_master_formular.attrib.get('Description'),
									'TAI_KHOAN_ID':tk_fomuala_details,
									'TAI_KHOAN' : text_tk,
									'TK_DOI_UNG_ID': tk_ud_fomuala_details,
									'TK_DOI_UNG' : text_tk_du,
									'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
									'ID_CHI_TIEU': child_master_formular.attrib.get('ItemID').lower() if child_master_formular.attrib.get('ItemID') != None else '',
								})]
			
			elif child.tag == 'AccountingSystem':
				res['THONG_TU'] = child.text
			elif child.tag == 'Hidden':
				res['KHONG_IN'] = True if child.text == '1' else False
			elif child.tag == 'IsBold':
				res['IN_DAM'] = True if child.text == '1' else False
			elif child.tag == 'IsItalic':
				res['IN_NGHIENG'] = True if child.text == '1' else False
			elif child.tag == 'IsEdited':
				res['DA_SUA_CT_MAC_DINH'] = True if child.text == '1' else False
		ten_bao_cao = ''
		ma_bao_cao = ''
		if res['ReportID']==1:
			ten_bao_cao='BANG_CAN_DOI_KE_TOAN'
			ma_bao_cao = 'B01-DN'
		elif res['ReportID']==2:
			ten_bao_cao ='BAO_CAO_KET_QUA_HOAT_DONG_KINH_DOANH'
			ma_bao_cao = 'B02-DN'
		elif res['ReportID']==3:
			ten_bao_cao ='BAO_CAO_LUU_CHUYEN_TIEN_TE_TRUC_TIEP'
			ma_bao_cao = 'B03-DN'
		else:
			ten_bao_cao ='BAO_CAO_LUU_CHUYEN_TIEN_TE_GIAN_TIEP'
			ma_bao_cao = 'B03-DN-GT'

		bao_cao = self.env['tien.ich.thiet.lap.bao.cao.tai.chinh'].search([('TEN_BAO_CAO', '=', ten_bao_cao ),('CHE_DO_KE_TOAN','=',res['THONG_TU'])], limit=1)
		if not bao_cao:
			bao_cao = self.env['tien.ich.thiet.lap.bao.cao.tai.chinh'].create({
				'CHE_DO_KE_TOAN':  res.get('THONG_TU'),
				'name': ma_bao_cao,
				'MA_BAO_CAO': ma_bao_cao,
				'TEN_BAO_CAO': ten_bao_cao,
			})
		res['CHI_TIET_ID'] = bao_cao.id
			
		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
	# import Tiện ích thiết lập báo cáo tài chính - tiện ích thuyết minh báo cáo tài chính chi tiết

	def _import_FRB03GTBussiness(self, tag):
		rec_model = 'tong.hop.bctc.nghiep.vu.cho.ct.chi.tiet.form'
		res = { }
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'RefDetailID':
				rec_id = 'FRB03GTBussiness' + str(child.text)
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['CHI_TIET_ID'] = rid.id
					res['CHI_TIET_MODEL'] = rid._name
			elif child.tag == 'BussinessID':
				res['NGHIEP_VU'] = child.text

		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

	def _import_FRB03ReportDetailActivity(self, tag):
		rec_model = 'tong.hop.bctc.chon.lai.hoat.dong.lctt.chi.tiet.form'
		res = { }
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'RefDetailID':
				rec_id = 'FRB03ReportDetailActivity' + str(child.text)
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['CHI_TIET_ID'] = rid.id
					res['CHI_TIET_MODEL'] = rid._name
			elif child.tag == 'ActivityID':
				res['HOAT_DONG'] = child.text

		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

	def _import_FRB03OPNDetailByActivity(self, tag):
		rec_model = 'tong.hop.bctc.chon.nv.va.hd.lctt.chi.tiet.theo.dt.form'
		res = { }
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'AccountNumber':
				rec_id = 'FRB03OPNDetailByActivity' + str(child.text)
				rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
				if rid:
					res['TAI_KHOAN_ID'] =rid.id
			elif child.tag == 'IsDebitBalance':
				res['LA_SO_DU_NO'] = True if child.text == '1' else False
			elif child.tag == 'BussinessAmount':
				res['SO_TIEN_KINH_DOANH'] = float(child.text)
			elif child.tag == 'InvestmentAmount':
				res['SO_TIEN_DAU_TU'] = float(child.text)
			elif child.tag == 'FinancialAmount':
				res['SO_TIEN_TAI_CHINH'] = float(child.text)
			elif child.tag == 'BranchID':
				rid= self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['CHI_NHANH_ID']=rid.id
					

		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

	def _import_FRB09DNTemplate(self, tag):
		rec_model = 'tien.ich.thuyet.minh.bao.cao.tai.chinh.chi.tiet'
		res = { }
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'ItemID':
				rec_id = child.text 
			elif child.tag == 'ItemCode':
				res['MA_CHI_TIEU'] = child.text
			elif child.tag == 'ItemIndex':
				res['SO_THU_TU'] = int(child.text)
			elif child.tag == 'ItemName':
				res['TEN_CHI_TIEU'] = child.text
			elif child.tag == 'Description':
				res['NOI_DUNG'] = child.text
			elif child.tag == 'ItemNameEnglish':
				res['TEN_TIENG_ANH'] = child.text
			elif child.tag == 'Part':
				res['THUOC_PHAN'] = child.text
			elif child.tag == 'FormulaType':
				res['LOAI_CHI_TIEU'] = child.text
			elif child.tag == 'PartInTab':
				res['PART_IN_TAB'] = int(child.text)
			elif child.tag == 'Hidden':
				res['KHONG_IN'] = True if child.text == '1' else False
			elif child.tag == 'IsBold':
				res['IN_DAM'] = True if child.text == '1' else False
			elif child.tag == 'IsItalic':
				res['IN_NGHIENG'] = True if child.text == '1' else False
			elif child.tag == 'ClosingBalance':
				res['CUOI_NAM'] = child.text
			elif child.tag == 'OpeningBalance':
				res['DAU_NAM'] = child.text
			elif child.tag == 'Equipment_IssueRight_TotalPayAndCapital':
				res['DU_PHONG_CUOI_NAM'] = child.text
			elif child.tag == 'Equipment_Trademark_PayDebitThisYearAndOtherCapital':
				res['PHUONG_TIEN_VAN_TAI_TRUYEN_DAN'] = child.text
			elif child.tag == 'Transport_CopyRight_PayInterestAndDecrease':
				res['DU_PHONG_DAU_NAM'] = child.text
			elif child.tag == 'License_PayInterestLastYearAndRevalueFA':
				res['CAY_LAU_NAM_SUC_VAT_LAM_VIEC_CHO_SAN_PHAM'] = child.text
			elif child.tag == 'IntFA_OrtherIntFA_PayDebitLastYearAndDiffExchangeRate':
				res['KET_CAU_HA_TANG_DNNDTXD'] = child.text
			elif child.tag == 'OtherFA_Software_TotalPayLastYearAndTreasuryShare':
				res['TAI_SAN_CO_DINH_HUU_HINH_KHAC'] = child.text
			elif child.tag == 'Total':
				res['TONG_CONG'] = child.text
			elif child.tag == 'BuildingAndRealty':
				res['NHA_CUA_VAT_CHAT_KIEN_TRUC'] = child.text

			elif child.tag == 'Formula':
				res['TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_TONG_HOP_IDS'] = [[5]]
				res['TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_CHI_TIET_IDS'] = [[5]]
				for child_root in child.getchildren():
					if child_root.tag == 'root':
						for child_master_formular in child_root.getchildren():
							if child_master_formular.tag == 'MasterFormula':
								res['TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_TONG_HOP_IDS'] += [(0,0,{
									'MA_CHI_TIEU': child_master_formular.attrib.get('ItemCode'),
									'TEN_CHI_TIEU': child_master_formular.attrib.get('ItemName'),
									'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
								})]
							elif child_master_formular.tag == 'DetailFormula':
								text_tk = '' 
								text_tk_du = ''
								tk_fomuala_details =False
								tk_ud_fomuala_details =False
								if child_master_formular.attrib.get('AccountNumber'):
									text_tk = child_master_formular.attrib.get('AccountNumber')
									tk_fomuala_details =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', text_tk)], limit=1).id
								if child_master_formular.attrib.get('CorrespondingAccountNumber'):
									text_tk_du = child_master_formular.attrib.get('CorrespondingAccountNumber')
									tk_ud_fomuala_details = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', text_tk_du)], limit=1).id
								if child_master_formular.attrib.get('FormulaColumnName') =='ClosingBalance' or child_master_formular.attrib.get('FormulaColumnName') =='OpeningBalance' or child_master_formular.attrib.get('FormulaColumnName') =='Equipment_IssueRight_TotalPayAndCapital' or child_master_formular.attrib.get('FormulaColumnName') =='Equipment_Trademark_PayDebitThisYearAndOtherCapital' or child_master_formular.attrib.get('FormulaColumnName') =='Transport_CopyRight_PayInterestAndDecrease' or child_master_formular.attrib.get('FormulaColumnName') =='License_PayInterestLastYearAndRevalueFA' or child_master_formular.attrib.get('FormulaColumnName') =='IntFA_OrtherIntFA_PayDebitLastYearAndDiffExchangeRate' or child_master_formular.attrib.get('FormulaColumnName') =='OtherFA_Software_TotalPayLastYearAndTreasuryShare' or child_master_formular.attrib.get('FormulaColumnName') =='Total' or child_master_formular.attrib.get('FormulaColumnName') =='BuildingAndRealty' :
								
									res['TIEN_ICH_XAY_DUNG_CONG_THUC_TMBCTC_LOAI_CHI_TIEU_CHI_TIET_IDS'] += [(0,0,{
										'KY_HIEU': child_master_formular.attrib.get('OperandString'),
										'DIEN_GIAI': child_master_formular.attrib.get('Description'),
										'TAI_KHOAN_ID':tk_fomuala_details,
										'TK_DOI_UNG_ID': tk_ud_fomuala_details,
										'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
									})]
		ten_bao_cao ='THUYET_MINH_BAO_CAO_TAI_CHINH'
		ma_bao_cao = 'B09-DN'
		bao_cao = self.env['tien.ich.thiet.lap.bao.cao.tai.chinh'].search([('TEN_BAO_CAO', '=', ten_bao_cao )], limit=1)
		if not bao_cao:
			bao_cao = self.env['tien.ich.thiet.lap.bao.cao.tai.chinh'].create({
				'name': ma_bao_cao,
				'MA_BAO_CAO': ma_bao_cao,
				'TEN_BAO_CAO': ten_bao_cao,
			})
		res['CHI_TIET_ID_1'] = bao_cao.id

		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
	# import Tiện ích thiết lập báo cáo tài chính - Thực hiện nghĩa vụ đối với nhà nước chi tiết
	def _import_FRObligationToGovTemplate(self, tag):
		rec_model = 'tien.ich.thuc.hien.nghia.vu.doi.voi.nha.nuoc.chi.tiet'
		res = { }
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'ItemID':
				rec_id = child.text 
			elif child.tag == 'ItemIndex':
				res['SO_THU_TU'] = int(child.text)
			elif child.tag == 'ItemCode':
				res['MA_CHI_TIEU'] = child.text
			elif child.tag == 'ItemName':
				res['TEN_CHI_TIEU'] = child.text
			elif child.tag == 'ItemNameEnglish':
				res['TEN_TIENG_ANH'] = child.text
			elif child.tag == 'FormulaType':
				res['LOAI_CHI_TIEU'] = child.text
			elif child.tag == 'UnPaidOfPrevPeriodAmount':
				res['SO_CON_PHAI_NOP_KY_TRUOC_CHUYEN_SANG'] = child.text
			elif child.tag == 'PayableAmount':
				res['SO_PHAI_NOP_TRONG_KY'] = child.text
			elif child.tag == 'PaidAmount':
				res['SO_DA_NOP_TRONG_KY'] = child.text
			elif child.tag == 'Formula':
				res['TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_CHI_TIET_IDS'] = [[5]]
				res['TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_TONG_HOP_IDS'] = [[5]]
				res['TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_CHI_TIET_IDS'] = [[5]]
				res['TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_TONG_HOP_IDS'] = [[5]]
				res['TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_CHI_TIET_IDS'] = [[5]]
				res['TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_TONG_HOP_IDS'] = [[5]]
				for child_root in child.getchildren():
					if child_root.tag == 'root':
						for child_master_formular in child_root.getchildren():
							if child_master_formular.tag == 'MasterFormula':
								res['TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_TONG_HOP_IDS'] += [(0,0,{
									'MA_CHI_TIEU': child_master_formular.attrib.get('ItemCode'),
									'TEN_CHI_TIEU': child_master_formular.attrib.get('ItemName'),
									'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
								})]
								res['TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_TONG_HOP_IDS'] += [(0,0,{
									'MA_CHI_TIEU': child_master_formular.attrib.get('ItemCode'),
									'TEN_CHI_TIEU': child_master_formular.attrib.get('ItemName'),
									'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
								})]
								res['TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_TONG_HOP_IDS'] += [(0,0,{
									'MA_CHI_TIEU': child_master_formular.attrib.get('ItemCode'),
									'TEN_CHI_TIEU': child_master_formular.attrib.get('ItemName'),
									'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
								})]
							elif child_master_formular.tag == 'DetailFormula':
								text_tk = '' 
								text_tk_du = ''
								tk_fomuala_details =False
								tk_ud_fomuala_details =False
								if child_master_formular.attrib.get('AccountNumber'):
									text_tk = child_master_formular.attrib.get('AccountNumber')
									tk_fomuala_details =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', text_tk)], limit=1).id
								if child_master_formular.attrib.get('CorrespondingAccountNumber'):
									text_tk_du = child_master_formular.attrib.get('CorrespondingAccountNumber')
									tk_ud_fomuala_details = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', text_tk_du)], limit=1).id
								if child_master_formular.attrib.get('FormulaColumnName') =='UnPaidOfPrevPeriodAmount':
									res['TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_CHI_TIET_IDS'] += [(0,0,{
										'KY_HIEU': child_master_formular.attrib.get('OperandString'),
										'DIEN_GIAI': child_master_formular.attrib.get('Description'),
										'TAI_KHOAN_ID':tk_fomuala_details,
										'TK_DOI_UNG_ID': tk_ud_fomuala_details,
										'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
									})]
								elif child_master_formular.attrib.get('FormulaColumnName') =='PayableAmount':
									res['TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_CHI_TIET_IDS'] += [(0,0,{
										'KY_HIEU': child_master_formular.attrib.get('OperandString'),
										'DIEN_GIAI': child_master_formular.attrib.get('Description'),
										'TAI_KHOAN_ID':tk_fomuala_details,
										'TK_DOI_UNG_ID': tk_ud_fomuala_details,
										'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
									})]
								elif child_master_formular.attrib.get('FormulaColumnName') =='PaidAmount':
									res['TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_CHI_TIET_IDS'] += [(0,0,{
										'KY_HIEU': child_master_formular.attrib.get('OperandString'),
										'DIEN_GIAI': child_master_formular.attrib.get('Description'),
										'TAI_KHOAN_ID':tk_fomuala_details,
										'TK_DOI_UNG_ID': tk_ud_fomuala_details,
										'PHEP_TINH': 'CONG' if child_master_formular.attrib.get('OperationSign') == '1' else 'TRU',
									})]
			elif child.tag == 'Hidden':
				res['KHONG_IN'] = True if child.text == '1' else False
			elif child.tag == 'IsBold':
				res['IN_DAM'] = True if child.text == '1' else False
			elif child.tag == 'IsItalic':
				res['IN_NGHIENG'] = True if child.text == '1' else False
			elif child.tag == 'Formula':
				res['XAY_DUNG_CONG_THUC'] = child.text
			elif child.tag == 'AccountingSystem':
				res['THONG_TU'] = child.text
		ten_bao_cao ='TINH_HINH_THUC_HIEN_NGHIA_VU_DOI_VOI_NHA_NUOC'
		ma_bao_cao = 'THTHNV'
		bao_cao = self.env['tien.ich.thiet.lap.bao.cao.tai.chinh'].search([('TEN_BAO_CAO', '=', ten_bao_cao ),('CHE_DO_KE_TOAN','=',res['THONG_TU'])], limit=1)
		if not bao_cao:
			bao_cao = self.env['tien.ich.thiet.lap.bao.cao.tai.chinh'].create({
				'CHE_DO_KE_TOAN':  res.get('THONG_TU'),
				'name': ma_bao_cao,
				'MA_BAO_CAO': ma_bao_cao,
				'TEN_BAO_CAO': ten_bao_cao,
			})
		res['CHI_TIET_ID_2'] = bao_cao.id

			
		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
	
	# Tiện ích / báo cáo
	# sql 
#     SELECT TOP 1000 [ReportID]
#       ,[ReportName]
#       ,[ReportName48]
#       ,[GroupID]     
#       ,[SortOrder]
#       ,[AccountingSystem]
#       ,[BranchID]
#       ,[Description]
#       ,[FormNo]
#       ,[FormNo48]      
#       ,[IsBeta]
#       ,[IsInvoice]
#       ,[IsSystem]
#       ,[IsShow]     
#       ,[ReportNameEnglish]
#       ,[ReportNameEnglish48]     
#       ,[ReportName133]
#       ,[ReportNameEnglish133]    
#   FROM [dbo].[SYSReportList]
#   where GroupID in (SELECT TOP 1000 [GroupID]
#   FROM [dbo].[SYSReportGroup]
#     where SortOrder > = 1
# 	order by SortOrder)
# FOR XML PATH
  


#   SELECT TOP 1000 [GroupID]
#       ,[GroupName]
#       ,[Description]
#       ,[Inactive]
#       ,[SortOrder]
#       ,[GroupNameEnglish]
#   FROM [dbo].[SYSReportGroup]
#     where SortOrder > = 1
# 	order by SortOrder
# FOR XML PATH

	def _import_SYSReportGroup(self, tag):
		rec_model = 'tien.ich.bao.cao'
		res = { }
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'GroupID':
				rec_id = child.text 
				res['THUOC'] = child.text
			elif child.tag == 'GroupName':
				res['TEN_BAO_CAO'] = child.text
			elif child.tag == 'SortOrder':
				res['STT'] = int(child.text)
			elif child.tag == 'GroupNameEnglish':
				res['TEN_BAO_CAO_TIENG_ANH'] = child.text
			elif child.tag == 'Inactive':
				res['active'] = False if child.text == '1' else True
			
		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


	def _import_SYSReportList(self, tag):
		rec_model = 'tien.ich.bao.cao'
		res = { }
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'ReportID':
				rec_id = child.text 
			elif child.tag == 'ReportName':
				res['TEN_BAO_CAO'] = child.text
			elif child.tag == 'SortOrder':
				res['STT'] = int(child.text)
			elif child.tag == 'ReportNameEnglish':
				res['TEN_BAO_CAO_TIENG_ANH'] = child.text
			elif child.tag == 'GroupID':
				res['parent_id'] = self.env['tien.ich.bao.cao'].search([('THUOC', '=', child.text)], limit=1).id
			res['active'] = True
		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)



	# Thiết lập cấu hình lãi lỗ cho công trình, hợp đồng, đơn hàng

	def _import_SYSReportTemplate(self, tag):
		rec_model = 'tien.ich.cau.hinh.lai.lo.cho.ct.hd.dh'
		res = { }
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'ReportItemID':
				rec_id = child.text 
			elif child.tag == 'ReportID':
				res['MA_BAO_CAO'] = child.text
			elif child.tag == 'ReportItemIndex':
				res['MA_THU_TU'] = float(child.text)
			elif child.tag == 'ReportItemAlias':
				res['MA_CHI_TIEU_DINH_DANH'] = child.text
			elif child.tag == 'ReportItemCode':
				res['MA_CHI_TIEU'] = child.text
			elif child.tag == 'ReportItemName':
				res['TEN_CHI_TIEU'] = child.text
			elif child.tag == 'ParentID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['CHI_TIEU_CHA_ID'] = rid.id 		
			elif child.tag == 'Grade':
				res['BAC'] = int(child.text)
			elif child.tag == 'IsParent':
				res['LA_CHI_TIEU_CHA'] = True if child.text == '1' else False
			elif child.tag == 'IsBold':
				res['IN_DAM'] = True if child.text == '1' else False
			elif child.tag == 'IsItalic':
				res['IN_NGHIENG'] = True if child.text == '1' else False
			elif child.tag == 'SortOrder':
				res['sequence'] =float(child.text)
			elif child.tag == 'Formula ':
				res['CONG_THUC'] = child.text			
		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


		# Thiết lập cấu hình lãi lỗ cho công trình, hợp đồng, đơn hàng công thức

	def _import_SYSReportFormula(self, tag):
		rec_model = 'tien.ich.cau.hinh.lai.lo.cho.ct.hd.dh.cong.thuc'
		res = { }
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'ItemDetailID':
				rec_id = child.text 
			elif child.tag == 'ReportID':
				res['MA_BAO_CAO'] = child.text
			elif child.tag == 'AccountSystem':
				res['HE_THONG_KE_TOAN'] = child.text
			elif child.tag == 'ReportItemID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
				if rid:
					res['CAU_HINH_LAI_LO_CHO_CT_HD_DH_ID'] = rid.id 
			elif child.tag == 'ColumnName':
				res['TEN_COT'] = child.text
			elif child.tag == 'FormulaSign':
				res['AM_DUONG'] = int(child.text)
			elif child.tag == 'FunctionCode':
				res['MA_HAM'] = child.text
					
			elif child.tag == 'AccountNumber':
				res['MA_TAI_KHOAN'] = child.text
			elif child.tag == 'CorrespondingAccountNumber':
				res['TAI_KHOAN_DOI_UNG'] = child.text
			elif child.tag == 'SortOrder':
				res['sequence'] = int(child.text)
			elif child.tag == 'Period':
				res['KY'] = int(child.text)	
		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)