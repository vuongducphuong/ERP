# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, helper

MODULE = 'base_import_ex'


class Import(models.TransientModel):
	_inherit = 'base_import_ex.import'

	# Sổ cái chi tiết
	def _import_GeneralLedger(self,tag):
		rec_model = 'so.cai.chi.tiet'
		res = {}
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'GeneralLedgerID':
				rec_id = child.text
			elif child.tag == 'RefDetailID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CHI_TIET_ID'] = rid.id
					res['CHI_TIET_MODEL'] = rid._name
				else:
					rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
					if rid:
						res['CHI_TIET_ID'] = rid.id
						res['CHI_TIET_MODEL'] = rid._name
			elif child.tag == 'RefID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['ID_CHUNG_TU'] = rid.id
					res['MODEL_CHUNG_TU'] = rid._name
				else:
					rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
					if rid:
						res['ID_CHUNG_TU'] = rid.id
						res['MODEL_CHUNG_TU'] = rid._name
			elif child.tag == 'RefType':
			   	res['LOAI_CHUNG_TU'] = child.text
			elif child.tag == 'RefNo':
			   	res['SO_CHUNG_TU'] = child.text
			elif child.tag == 'RefDate':
			   	res['NGAY_CHUNG_TU'] = child.text
			elif child.tag == 'PostedDate':
				res['NGAY_HACH_TOAN'] = child.text
			elif child.tag == 'AccountNumber':
				rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
				if rid:
					res['TAI_KHOAN_ID'] = rid.id 
			elif child.tag == 'CorrespondingAccountNumber':
				rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
				if rid:
					res['TAI_KHOAN_DOI_UNG_ID'] = rid.id
			elif child.tag == 'CurrencyID':
				rid = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
				if rid:
					res['currency_id'] = rid.id
			elif child.tag == 'BankAccountID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['TAI_KHOAN_NGAN_HANG_ID'] = rid.id 
			elif child.tag == 'ExchangeRate':
				res['TY_GIA'] = float(child.text)
			elif child.tag == 'DebitAmountOC':
			   	res['GHI_NO_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'DebitAmount':
				res['GHI_NO'] = float(child.text)
			elif child.tag == 'CreditAmountOC':
				res['GHI_CO_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'CreditAmount':
				res['GHI_CO'] = float(child.text)
			elif child.tag == 'Quantity':
				res['SO_LUONG'] = float(child.text)
			elif child.tag == 'UnitPrice':
				res['DON_GIA'] = float(child.text)
				res['GIA_VON'] = float(child.text)
			elif child.tag == 'EntryType':
			   	res['LOAI_HACH_TOAN'] = child.text
			elif child.tag == 'InvNo':
			   	res['SO_HOA_DON'] = child.text
			elif child.tag == 'InvDate':
			   	res['NGAY_HOA_DON'] = child.text
			elif child.tag == 'JournalMemo':
			   	res['DIEN_GIAI_CHUNG'] = child.text
			elif child.tag == 'Description':
			   	res['DIEN_GIAI'] = child.text
			elif child.tag == 'ContactName':
			   	res['NGUOI_LIEN_HE'] = child.text
			elif child.tag == 'InventoryItemID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['MA_HANG_ID'] = rid.id
			elif child.tag == 'UnitID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['DVT_ID'] = rid.id
			elif child.tag == 'AccountObjectID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['DOI_TUONG_ID'] = rid.id
			elif child.tag == 'EmployeeID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['NHAN_VIEN_ID'] = rid.id
			elif child.tag == 'SortOrder':
				res['THU_TU_TRONG_CHUNG_TU'] = int(child.text)
			elif child.tag == 'BusinessType':
				res['LOAI_NGHIEP_VU'] = child.text
			elif child.tag == 'ProjectWorkID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CONG_TRINH_ID'] = rid.id

			elif child.tag == 'ListItemID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['MA_THONG_KE_ID'] = rid.id
			elif child.tag == 'JobID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['DOI_TUONG_THCP_ID'] = rid.id
			elif child.tag == 'OrderID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['DON_DAT_HANG_ID'] = rid.id
			elif child.tag == 'DetailPostOrder':
				res['THU_TU_CHI_TIET_GHI_SO'] = int(child.text)
			elif child.tag == 'BranchID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CHI_NHANH_ID'] = rid.id
			elif child.tag == 'ContractID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['HOP_DONG_BAN_ID'] = rid.id
			elif child.tag == 'DueDate':
				res['HAN_THANH_TOAN'] = child.text
			elif child.tag == 'UnitPriceOC':
				res['DON_GIA_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'MainUnitPrice':
			   	res['DON_GIA_THEO_DVT_CHINH'] = float(child.text)
			elif child.tag == 'RefTypeName':
				res['TEN_LOAI_CHUNG_TU'] = child.text
		if res['SO_CHUNG_TU'].startswith('CTTC'):
			res['ID_CHUNG_TU'] = 1
			res['MODEL_CHUNG_TU'] = 'cho.thue.tscd'
		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

	
	# Sổ mua hàng chi tiết
	def _import_PurchaseLedger(self,tag):
		rec_model = 'so.mua.hang.chi.tiet'
		res = {}
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'PurchaseLedgerID':
				rec_id = child.text
			elif child.tag == 'RefDetailID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CHI_TIET_ID'] = rid.id
					res['CHI_TIET_MODEL'] = rid._name
			elif child.tag == 'RefID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['ID_CHUNG_TU'] = rid.id
					res['MODEL_CHUNG_TU'] = rid._name
			elif child.tag == 'RefType':
			   	res['LOAI_CHUNG_TU'] = child.text
			elif child.tag == 'RefNo':
			   	res['SO_CHUNG_TU'] = child.text
			elif child.tag == 'RefDate':
			   	res['NGAY_CHUNG_TU'] = child.text
			elif child.tag == 'PostedDate':
				res['NGAY_HACH_TOAN'] = child.text
			elif child.tag == 'CurrencyID':
				rid = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
				if rid:
					res['currency_id'] = rid.id
			elif child.tag == 'ExchangeRate':
				res['TY_GIA'] = float(child.text)
			elif child.tag == 'UnitPrice':
				res['DON_GIA'] = float(child.text)
			elif child.tag == 'InvNo':
			   	res['SO_HOA_DON'] = child.text
			elif child.tag == 'InvDate':
			   	res['NGAY_HOA_DON'] = child.text
			elif child.tag == 'JournalMemo':
			   	res['DIEN_GIAI_CHUNG'] = child.text
			elif child.tag == 'Description':
			   	res['DIEN_GIAI'] = child.text
			elif child.tag == 'InventoryItemID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['MA_HANG_ID'] = rid.id
			elif child.tag == 'UnitID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['DVT_ID'] = rid.id
			elif child.tag == 'AccountObjectID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['DOI_TUONG_ID'] = rid.id
			elif child.tag == 'EmployeeID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['NHAN_VIEN_ID'] = rid.id
			elif child.tag == 'SortOrder':
				res['THU_TU_TRONG_CHUNG_TU'] = int(child.text)
			elif child.tag == 'ProjectWorkID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CONG_TRINH_ID'] = rid.id
			elif child.tag == 'StockID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['KHO_ID'] = rid.id
			elif child.tag == 'DebitAccount':
				rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
				if rid:
					res['TK_NO_ID'] = rid.id 
			elif child.tag == 'CreditAccount':
				rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
				if rid:
					res['TK_CO_ID'] = rid.id
			elif child.tag == 'PurchaseQuantity':
				res['SO_LUONG'] = float(child.text)
			elif child.tag == 'PurchaseAmount':
				res['SO_TIEN'] = float(child.text)
			elif child.tag == 'VATRate':
				res['PHAN_TRAM_THUE_VAT'] = float(child.text)
			elif child.tag == 'VATAmount':
				res['SO_TIEN_VAT'] = float(child.text)
			elif child.tag == 'VATAmountOC':
				res['SO_TIEN_VAT_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'DiscountRate':
				res['PHAN_TRAM_CHIET_KHAU'] = float(child.text)
			elif child.tag == 'DiscountAmount':
				res['SO_TIEN_CHIET_KHAU'] = float(child.text)
			elif child.tag == 'DiscountAmountOC':
				res['SO_TIEN_CHIET_KHAU_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'ReturnQuantity':
				res['SO_LUONG_TRA_LAI'] = float(child.text)
			elif child.tag == 'ReturnMainQuantity':
				res['SO_LUONG_TRA_LAI_THEO_DVT_CHINH'] = float(child.text)
			elif child.tag == 'ReturnAmount':
				res['SO_TIEN_TRA_LAI'] = float(child.text)
			elif child.tag == 'ReturnAmountOC':
				res['SO_TIEN_TRA_LAI_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'ReduceAmount':
				res['SO_TIEN_GIAM_TRU'] = float(child.text)
			elif child.tag == 'ReduceAmountOC':
				res['SO_TIEN_GIAM_TRU_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'LotNo':
				res['SO_LO'] = child.text
			elif child.tag == 'DueDate':
				res['NGAY_HET_HAN'] = child.text
			elif child.tag == 'ContractCode':
				res['MA_HOP_DONG'] = child.text
			elif child.tag == 'ContractName':
				res['TEN_HOP_DONG'] = child.text
			elif child.tag == 'PaymentTermCode':
				res['MA_DIEU_KHOAN_THANH_TOAN'] = child.text
			elif child.tag == 'PaymentTermName':
				res['TEN_DIEU_KHOAN_THANH_TOAN'] = child.text
			elif child.tag == 'UnitPriceOC':
				res['DON_GIA_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'MainUnitID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['DVT_CHINH_ID'] = rid.id
			elif child.tag == 'MainUnitPrice':
				res['DON_GIA_THEO_DVT_CHINH'] = float(child.text)
			elif child.tag == 'MainQuantity':
				res['SO_LUONG_THEO_DVT_CHINH'] = float(child.text)
			elif child.tag == 'MainUnitPriceOC':
				res['DON_GIA_NGUYEN_TE_THEO_DVT_CHINH'] = float(child.text)
			elif child.tag == 'BranchID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CHI_NHANH_ID'] = rid.id
			
			
		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
	
	# Sổ công nợ chi tiết
	def _import_AccountObjectLedger(self,tag):
		rec_model = 'so.cong.no.chi.tiet'
		res = {}
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'AccountObjectLedgerID':
				rec_id = child.text
			elif child.tag == 'RefDetailID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CHI_TIET_ID'] = rid.id
					res['CHI_TIET_MODEL'] = rid._name
			elif child.tag == 'RefID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['ID_CHUNG_TU'] = rid.id
					res['MODEL_CHUNG_TU'] = rid._name
			elif child.tag == 'RefType':
			   	res['LOAI_CHUNG_TU'] = child.text
			elif child.tag == 'RefNo':
			   	res['SO_CHUNG_TU'] = child.text
			elif child.tag == 'RefDate':
			   	res['NGAY_CHUNG_TU'] = child.text
			elif child.tag == 'PostedDate':
				res['NGAY_HACH_TOAN'] = child.text
			elif child.tag == 'CurrencyID':
				rid= self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
				if rid:
					res['currency_id'] = rid.id
			elif child.tag == 'ExchangeRate':
				res['TY_GIA'] = float(child.text)
			elif child.tag == 'UnitPrice':
				res['DON_GIA'] = float(child.text)
				res['GIA_VON'] = float(child.text)
			elif child.tag == 'InvNo':
			   	res['SO_HOA_DON'] = child.text
			elif child.tag == 'InvDate':
			   	res['NGAY_HOA_DON'] = child.text
			elif child.tag == 'JournalMemo':
			   	res['DIEN_GIAI_CHUNG'] = child.text
			elif child.tag == 'Description':
			   	res['DIEN_GIAI'] = child.text
			elif child.tag == 'InventoryItemID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['MA_HANG_ID'] = rid.id
			elif child.tag == 'UnitID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['DVT_ID'] = rid.id
			elif child.tag == 'AccountObjectID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['DOI_TUONG_ID'] = rid.id
			elif child.tag == 'EmployeeID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['NHAN_VIEN_ID'] = rid.id
			elif child.tag == 'SortOrder':
				res['THU_TU_TRONG_CHUNG_TU'] = int(child.text)
			elif child.tag == 'ProjectWorkID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CONG_TRINH_ID'] = rid.id
			elif child.tag == 'DueDate':
				res['NGAY_HET_HAN'] = child.text
			elif child.tag == 'UnitPriceOC':
				res['DON_GIA_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'MainUnitID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['DVT_CHINH_ID'] = rid.id
			elif child.tag == 'MainUnitPrice':
				res['DON_GIA_THEO_DVT_CHINH'] = float(child.text)
			elif child.tag == 'MainQuantity':
				res['SO_LUONG_THEO_DVT_CHINH'] = float(child.text)
			elif child.tag == 'MainUnitPriceOC':
				res['DON_GIA_NGUYEN_TE_THEO_DVT_CHINH'] = float(child.text)
			elif child.tag == 'RefTypeName':
				res['TEN_LOAI_CHUNG_TU'] = child.text
			elif child.tag == 'AccountNumber':
				rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
				if rid:
					res['TK_ID'] = rid.id
			elif child.tag == 'CorrespondingAccountNumber':
				rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
				if rid:
					res['TK_DOI_UNG_ID'] = rid.id
			elif child.tag == 'Quantity':
				res['SO_LUONG'] = float(child.text)
			elif child.tag == 'DebitAmountOC':
			   	res['GHI_NO_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'DebitAmount':
				res['GHI_NO'] = float(child.text)
			elif child.tag == 'CreditAmountOC':
				res['GHI_CO_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'CreditAmount':
				res['GHI_CO'] = float(child.text)
			elif child.tag == 'EntryType':
			   	res['LOAI_HACH_TOAN'] = child.text
			elif child.tag == 'PaymentTermID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['DIEU_KHOAN_TT_ID'] = rid.id
			elif child.tag == 'ContractCode':
				res['SO_HOP_DONG'] = child.text
			elif child.tag == 'BranchID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CHI_NHANH_ID'] = rid.id
			elif child.tag == 'ContractID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['HOP_DONG_BAN_ID'] = rid.id
			elif child.tag == 'OrderID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['DON_DAT_HANG_ID'] = rid.id
			elif child.tag == 'OrganizationUnitID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['DON_VI_ID'] = rid.id
			elif child.tag == 'PUContractID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['HOP_DONG_MUA_ID'] = rid.id
			elif child.tag == 'PUOrderRefID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['DON_MUA_HANG_ID'] = rid.id
			elif child.tag == 'ListItemID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['MA_THONG_KE_ID'] = rid.id
			elif child.tag == 'DetailPostOrder':
				res['THU_TU_CHI_TIET_GHI_SO'] = int(child.text)
		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
	
	# Sổ kho chi tiết
	def _import_InventoryLedger(self,tag):
		rec_model = 'so.kho.chi.tiet'
		res = {}
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'InventoryLedgerID':
				rec_id = child.text
			elif child.tag == 'RefDetailID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CHI_TIET_ID'] = rid.id
					res['CHI_TIET_MODEL'] = rid._name
				else:
					rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
					if rid:
						res['CHI_TIET_ID'] = rid.id
						res['CHI_TIET_MODEL'] = rid._name
			elif child.tag == 'RefID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['ID_CHUNG_TU'] = rid.id
					res['MODEL_CHUNG_TU'] = rid._name
				else:
					rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
					if rid:
						res['ID_CHUNG_TU'] = rid.id
						res['MODEL_CHUNG_TU'] = rid._name
			elif child.tag == 'RefType':
			   	res['LOAI_CHUNG_TU'] = child.text
			elif child.tag == 'RefNo':
			   	res['SO_CHUNG_TU'] = child.text
			elif child.tag == 'RefDate':
			   	res['NGAY_CHUNG_TU'] = child.text
			elif child.tag == 'PostedDate':
				res['NGAY_HACH_TOAN'] = child.text
			elif child.tag == 'CurrencyID':
				rid= self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
				if rid:
					res['currency_id'] = rid.id
			elif child.tag == 'ExchangeRate':
				res['TY_GIA'] = float(child.text)
			elif child.tag == 'UnitPrice':
				res['DON_GIA'] = float(child.text)
				res['GIA_VON'] = float(child.text)
			elif child.tag == 'InvNo':
			   	res['SO_HOA_DON'] = child.text
			elif child.tag == 'InvDate':
			   	res['NGAY_HOA_DON'] = child.text
			elif child.tag == 'JournalMemo':
			   	res['DIEN_GIAI_CHUNG'] = child.text
			elif child.tag == 'Description':
			   	res['DIEN_GIAI'] = child.text
			elif child.tag == 'InventoryItemID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['MA_HANG_ID'] = rid.id
			elif child.tag == 'UnitID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['DVT_ID'] = rid.id
			elif child.tag == 'AccountObjectID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['DOI_TUONG_ID'] = rid.id
			elif child.tag == 'EmployeeID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['NHAN_VIEN_ID'] = rid.id
			elif child.tag == 'SortOrder':
				res['THU_TU_TRONG_CHUNG_TU'] = int(child.text)
			elif child.tag == 'DueDate':
				res['NGAY_HET_HAN'] = child.text
			elif child.tag == 'ContractCode':
				res['MA_HOP_DONG'] = child.text
			elif child.tag == 'MainUnitID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['DVT_CHINH_ID'] = rid.id
			elif child.tag == 'AccountNumber':
				rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
				if rid:
					res['TK_NO_ID'] = rid.id
			elif child.tag == 'CorrespondingAccountNumber':
				rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
				if rid:
					res['TK_CO_ID'] = rid.id
			elif child.tag == 'StockID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['KHO_ID'] = rid.id
			elif child.tag == 'InwardQuantity':
				res['SO_LUONG_NHAP'] = float(child.text)
			elif child.tag == 'OutwardQuantity':
				res['SO_LUONG_XUAT'] = float(child.text)
			elif child.tag == 'InwardAmount':
				res['SO_TIEN_NHAP'] = float(child.text)
			elif child.tag == 'OutwardAmount':
				res['SO_TIEN_XUAT'] = float(child.text)
			elif child.tag == 'LotNo':
				res['SO_LO'] = child.text
			elif child.tag == 'IsPromotion':
				res['LA_HANG_KHUYEN_MAI'] = True if child.text == '1' else False
			elif child.tag == 'OrganizationUnitID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['DON_VI_ID'] = rid.id
			elif child.tag == 'InOutWardType':
				res['LOAI_KHU_VUC_NHAP_XUAT'] = child.text
			elif child.tag == 'UnitPriceMethod':
				res['PHUONG_THUC_THANH_TOAN'] = child.text
			elif child.tag == 'UnUpdateOutwardPriceType':
				res['LOAI_KHONG_CAP_NHAT_GIA_XUAT'] = child.text
			elif child.tag == 'IsUnUpdateOutwardPrice':
				res['KHONG_CAP_NHAT_GIA_XUAT'] = True if child.text == '1' else False
			elif child.tag == 'ContactName':
				res['NGUOI_LIEN_HE'] = child.text
			elif child.tag == 'BranchID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CHI_NHANH_ID'] = rid.id
			elif child.tag == 'ExpiryDate':
			   	res['NGAY_HET_HAN'] = child.text
			elif child.tag == 'MainConvertRate':
				res['TY_LE_CHUYEN_DOI'] = float(child.text)
			elif child.tag == 'ExchangeRateOperator':
				if child.text =='*':
					res['TOAN_TU_QUY_DOI'] = 'NHAN'
				elif child.text =='/':
					res['TOAN_TU_QUY_DOI'] = 'CHIA'
			elif child.tag == 'INRefOrder':
				res['STT_LOAI_CHUNG_TU'] = child.text
			elif child.tag == 'AssemblyRefID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CHUNG_TU_LAP_RAP_THAO_DO_ID'] = rid.id
			elif child.tag == 'MainInwardQuantity':
				res['SO_LUONG_NHAP_THEO_DVT_CHINH'] = float(child.text)
			elif child.tag == 'MainOutwardQuantity':
				res['SO_LUONG_XUAT_THEO_DVT_CHINH'] = float(child.text)
			elif child.tag == 'MainUnitPrice':
				res['DON_GIA_THEO_DVT_CHINH'] = float(child.text)
			elif child.tag == 'IsInward':
				res['LA_NHAP_KHO'] = True if child.text == '1' else False
			elif child.tag == 'ProductionOrderRefID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CHUNG_TU_LENH_SAN_XUAT_ID'] = rid.id
			elif child.tag == 'JobID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['MA_DOI_TUONG_THCP_ID'] = rid.id
			elif child.tag == 'ProjectWorkID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CONG_TRINH_ID'] = rid.id
			elif child.tag == 'OrderID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['DON_DAT_HANG_ID'] = rid.id
			elif child.tag == 'ContractID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['HOP_DONG_BAN_ID'] = rid.id
			elif child.tag == 'OutwardRefID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['ID_CHUNG_TU_XUAT_KHO'] = rid.id
					res['MODEL_CHUNG_TU_XUAT_KHO'] = rid._name
			elif child.tag == 'OutwardRefDetailID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['ID_CHUNG_TU_XUAT_KHO_CHI_TIET'] = rid.id
					res['MODEL_CHUNG_TU_XUAT_KHO_CHI_TIET'] = rid._name
		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
	
	# Sổ bán hàng chi tiết
	def _import_SaleLedger(self,tag):
		rec_model = 'so.ban.hang.chi.tiet'
		res = {}
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'SaleLedgerID':
				rec_id = child.text
			elif child.tag == 'RefDetailID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CHI_TIET_ID'] = rid.id
					res['CHI_TIET_MODEL'] = rid._name
			elif child.tag == 'RefID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['ID_CHUNG_TU'] = rid.id
					res['MODEL_CHUNG_TU'] = rid._name
			elif child.tag == 'RefType':
			   	res['LOAI_CHUNG_TU'] = child.text
			elif child.tag == 'RefNo':
			   	res['SO_CHUNG_TU'] = child.text
			elif child.tag == 'RefDate':
			   	res['NGAY_CHUNG_TU'] = child.text
			elif child.tag == 'PostedDate':
				res['NGAY_HACH_TOAN'] = child.text
			elif child.tag == 'CurrencyID':
				rid= self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
				if rid:
					res['currency_id'] = rid.id
			elif child.tag == 'ExchangeRate':
				res['TY_GIA'] = float(child.text)
			elif child.tag == 'UnitPrice':
				res['DON_GIA'] = float(child.text)
			elif child.tag == 'InvNo':
			   	res['SO_HOA_DON'] = child.text
			elif child.tag == 'InvDate':
			   	res['NGAY_HOA_DON'] = child.text
			elif child.tag == 'JournalMemo':
			   	res['DIEN_GIAI_CHUNG'] = child.text
			elif child.tag == 'Description':
			   	res['DIEN_GIAI'] = child.text
			elif child.tag == 'InventoryItemID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['MA_HANG_ID'] = rid.id
			elif child.tag == 'UnitID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['DVT_ID'] = rid.id
			elif child.tag == 'AccountObjectID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['DOI_TUONG_ID'] = rid.id
			elif child.tag == 'EmployeeID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['NHAN_VIEN_ID'] = rid.id
			elif child.tag == 'SortOrder':
				res['THU_TU_TRONG_CHUNG_TU'] = int(child.text)
			elif child.tag == 'DueDate':
				res['NGAY_HET_HAN'] = child.text
			elif child.tag == 'ContractCode':
				res['MA_HOP_DONG'] = child.text
			elif child.tag == 'MainUnitID':
				rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
				if rid:
					res['DVT_CHINH_ID'] = rid.id
			elif child.tag == 'MainUnitPrice':
				res['DON_GIA_THEO_DVT_CHINH'] = float(child.text)
			elif child.tag == 'SaleQuantity':
				res['SO_LUONG'] = float(child.text)

			elif child.tag == 'SaleAmount':
				res['SO_TIEN'] = float(child.text)

			elif child.tag == 'SaleAmountOC':
				res['SO_TIEN_NGUYEN_TE'] = float(child.text)
			
			elif child.tag == 'StockID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['KHO_ID'] = rid.id
			
			elif child.tag == 'LotNo':
				res['SO_LO'] = child.text
			elif child.tag == 'IsPromotion':
				res['LA_HANG_KHUYEN_MAI'] = True if child.text == '1' else False
				res['LA_KHUYEN_MAI'] = True if child.text == '1' else False
			elif child.tag == 'OrganizationUnitID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['DON_VI_ID'] = rid.id
			elif child.tag == 'DebitAccount':
				rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
				if rid:
					res['TK_NO_ID'] = rid.id
			elif child.tag == 'CreditAccount':
				rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
				if rid:
					res['TK_CO_ID'] = rid.id
			elif child.tag == 'VATRate':
				res['PHAN_TRAM_THUE_VAT'] = float(child.text)
			elif child.tag == 'VATAmount':
				res['SO_TIEN_VAT'] = float(child.text)
			elif child.tag == 'VATAmountOC':
				res['SO_TIEN_VAT_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'VATAccount':
				rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
				if rid:
					res['TAI_KHOAN_VAT_ID'] = rid.id
			elif child.tag == 'ExportTaxRate':
				res['PHAN_TRAM_THUE_NHAP_KHAU'] = float(child.text)
			elif child.tag == 'ExportTaxAmount':
				res['SO_TIEN_NHAP_KHAU'] = float(child.text)
			elif child.tag == 'ExportTaxAmountOC':
				res['SO_TIEN_NHAP_KHAU_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'ExportTaxAccount':
				rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
				if rid:
					res['TAI_KHOAN_NHAP_KHAU_ID'] = rid.id
			elif child.tag == 'DiscountRate':
				res['PHAN_TRAM_CHIET_KHAU'] = float(child.text)
			elif child.tag == 'DiscountAmount':
				res['SO_TIEN_CHIET_KHAU'] = float(child.text)
			elif child.tag == 'DiscountAmountOC':
				res['SO_TIEN_CHIET_KHAU_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'DiscountAccount':
				rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
				if rid:
					res['TK_CHIET_KHAU_ID'] = rid.id
			elif child.tag == 'ReturnQuantity':
				res['SO_LUONG_TRA_LAI'] = float(child.text)
			elif child.tag == 'ReturnMainQuantity':
				res['SL_TRA_LAI_THEO_DVT_CHINH'] = float(child.text)
			elif child.tag == 'ReturnAmount':
				res['SO_TIEN_TRA_LAI'] = float(child.text)
			elif child.tag == 'ReturnAmountOC':
				res['SO_TIEN_TRA_LAI_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'ReduceAmount':
				res['SO_TIEN_GIAM_TRU'] = float(child.text)
			elif child.tag == 'ReduceAmountOC':
				res['SO_TIEN_GIAM_TRU_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'Warranty':
				res['THOI_GIAN_BAO_HANH'] = float(child.text)
			elif child.tag == 'BranchID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CHI_NHANH_ID'] = rid.id
			elif child.tag == 'ProjectWorkID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CONG_TRINH_ID'] = rid.id
			elif child.tag == 'UnitPriceOC':
				res['DON_GIA_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'MainQuantity':
				res['SO_LUONG_THEO_DVT_CHINH'] = float(child.text)
			elif child.tag == 'MainUnitPriceOC':
				res['DON_GIA_NGUYEN_TE_THEO_DVT_CHINH'] = float(child.text)
			elif child.tag == 'PaymentTermCode':
				res['MA_DIEU_KHOAN_THANH_TOAN'] = child.text
			elif child.tag == 'PaymentTermName':
				res['TEN_DIEU_KHOAN_THANH_TOAN'] = child.text
			elif child.tag == 'ContractName':
				res['TEN_HOP_DONG'] = child.text
		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
	
	# Sổ thuế chi tiết
	def _import_TaxLedger(self,tag):
		rec_model = 'so.thue.chi.tiet'
		res = {}
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'TaxLedgerID':
				rec_id = child.text
			elif child.tag == 'RefDetailID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CHI_TIET_ID'] = rid.id
					res['CHI_TIET_MODEL'] = rid._name
			elif child.tag == 'RefID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['ID_CHUNG_TU'] = rid.id
					res['MODEL_CHUNG_TU'] = rid._name
			elif child.tag == 'RefType':
			   	res['LOAI_CHUNG_TU'] = child.text
			elif child.tag == 'RefNo':
			   	res['SO_CHUNG_TU'] = child.text
			elif child.tag == 'RefDate':
			   	res['NGAY_CHUNG_TU'] = child.text
			elif child.tag == 'PostedDate':
				res['NGAY_HACH_TOAN'] = child.text
			elif child.tag == 'InvNo':
			   	res['SO_HOA_DON'] = child.text
			elif child.tag == 'InvDate':
			   	res['NGAY_HOA_DON'] = child.text
			elif child.tag == 'JournalMemo':
			   	res['DIEN_GIAI_CHUNG'] = child.text
			elif child.tag == 'Description':
			   	res['DIEN_GIAI'] = child.text
			elif child.tag == 'AccountObjectID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['DOI_TUONG_ID'] = rid.id
			elif child.tag == 'SortOrder':
				res['THU_TU_TRONG_CHUNG_TU'] = int(child.text)
			elif child.tag == 'BranchID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CHI_NHANH_ID'] = rid.id
			elif child.tag == 'VATAmountOC':
				res['SO_TIEN_VAT_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'TurnOverAmountOC':
				res['SO_TIEN_CHIU_VAT_NGUYEN_TE'] = float(child.text)
			elif child.tag == 'InvTemplateNo':
				res['MAU_SO_HOA_DON'] = child.text
			elif child.tag == 'InvSeries':
				res['KY_HIEU_HOA_DON'] = child.text

			elif child.tag == 'VATAmount':
				res['SO_TIEN_VAT'] = float(child.text)
			elif child.tag == 'VATRate':
				res['PHAN_TRAM_VAT'] = float(child.text)
			elif child.tag == 'TurnOverAmount':
				res['SO_TIEN_CHIU_VAT'] = float(child.text)
			elif child.tag == 'VoucherRefType':
				res['LOAI_CHUNG_TU_GOC'] = child.text
			elif child.tag == 'VoucherRefNo':
				res['SO_CHUNG_TU_GOC'] = child.text
			elif child.tag == 'VoucherRefDate':
				res['NGAY_CHUNG_TU_GOC'] = child.text
			elif child.tag == 'VoucherPostedDate':
				res['NGAY_HACH_TOAN_CHUNG_TU_GOC'] = child.text
			elif child.tag == 'TableListType':
				res['DS_LOAI_BANG'] = int(child.text)
			elif child.tag == 'PurchasePurposeID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['MUC_DICH_MUA_HANG_ID'] = rid.id
			elif child.tag == 'VoucherRefDetailID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CHI_TIET_ID_CHUNG_TU_GOC'] = rid.id
					res['CHI_TIET_MODEL_CHUNG_TU_GOC'] = rid._name
			elif child.tag == 'NotInVATDeclaration':
				res['HHDV_KO_TONG_HOP_TREN_TO_KHAI_GTGT'] = True if child.text == '1' else False
			elif child.tag == 'VoucherRefID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['ID_CHUNG_TU_GOC'] = rid.id
					res['MODEL_CHUNG_TU_GOC'] = rid._name
			elif child.tag == 'VATAccount':
				rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
				if rid:
					res['TK_VAT_ID'] = rid.id
			elif child.tag == 'AccountObjectCode':
			   	res['MA_DOI_TUONG'] = child.text
			elif child.tag == 'AccountObjectName':
			   	res['TEN_DOI_TUONG'] = child.text
			elif child.tag == 'CompanyTaxCode':
			   	res['MA_SO_THUE_DOI_TUONG'] = child.text
		if res.get('PHAN_TRAM_VAT')== None:
			res['PHAN_TRAM_VAT'] = -2	   
		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
	
	# Sổ tài sản cố định chi tiết
	def _import_FixedAssetLedger(self,tag):
		rec_model = 'so.tscd.chi.tiet'
		res = {}
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'FixedAssetLedgerID':
				rec_id = child.text
			elif child.tag == 'RefID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['ID_CHUNG_TU'] = rid.id
					res['MODEL_CHUNG_TU'] = rid._name
			elif child.tag == 'RefType':
			   	res['LOAI_CHUNG_TU'] = child.text
			elif child.tag == 'RefNo':
			   	res['SO_CHUNG_TU'] = child.text
			elif child.tag == 'RefDate':
			   	res['NGAY_CHUNG_TU'] = child.text
			elif child.tag == 'PostedDate':
				res['NGAY_HACH_TOAN'] = child.text
			elif child.tag == 'JournalMemo':
			   	res['DIEN_GIAI_CHUNG'] = child.text
			elif child.tag == 'BranchID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CHI_NHANH_ID'] = rid.id
			elif child.tag == 'OrganizationUnitID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['DON_VI_SU_DUNG_ID'] = rid.id
			elif child.tag == 'LifeTimeInMonth':
			   	res['THOI_GIAN_SU_DUNG'] = float(child.text)
			elif child.tag == 'LifeTimeRemainingInMonth':
			   	res['THOI_GIAN_SU_DUNG_CON_LAI'] = float(child.text)
			elif child.tag == 'DepreciationRateMonth':
			   	res['TY_LE_KHAU_HAO_THANG'] = float(child.text)
			elif child.tag == 'MonthlyDepreciationAmount':
			   	res['GIA_TRI_KHAU_HAO_THANG'] = float(child.text)
			elif child.tag == 'DepreciationAmount':
			   	res['GIA_TRI_TINH_KHAU_HAO'] = float(child.text)
			elif child.tag == 'AccumDepreciationAmount':
			   	res['GIA_TRI_HAO_MON_LUY_KE'] = float(child.text)
			elif child.tag == 'RemainingAmount':
			   	res['GIA_TRI_CON_LAI'] = float(child.text)
			elif child.tag == 'FixedAssetCategoryID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['LOAI_TSCD_ID'] = rid.id
			elif child.tag == 'OrgPrice':
			   	res['NGUYEN_GIA'] = float(child.text)
			elif child.tag == 'OrgPriceAccount':
				rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
				if rid:
					res['TK_NGUYEN_GIA_ID'] = rid.id
			elif child.tag == 'DepreciationAccount':
				rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
				if rid:
					res['TK_HAO_MON_ID'] = rid.id
			elif child.tag == 'DiffAccumDepreciationAmount':
			   	res['CHENH_LECH_GIA_TRI_HAO_MON_LUY_KE'] = float(child.text)
			elif child.tag == 'SumDiffLifeTime':
			   	res['CHENH_LECH_THOI_GIAN_SU_DUNG'] = float(child.text)
			elif child.tag == 'DiffDepreciationAmount':
			   	res['CHENH_LECH_GIA_TRI_TINH_KHAU_HAO'] = float(child.text)
			elif child.tag == 'SumDiffRemainingAmount':
			   	res['CHENH_LECH_GIA_TRI_CON_LAI'] = float(child.text)
			elif child.tag == 'DepreciationAmountByIncomeTax':
			   	res['GIA_TRI_TINH_KH_THEO_LUAT'] = float(child.text)
			elif child.tag == 'MonthlyDepreciationAmountByIncomeTax':
			   	res['GIA_TRI_KH_THANG_THEO_LUAT'] = float(child.text)
			elif child.tag == 'DiffOrgPriceAmount':
			   	res['CHENH_LECH_NGUYEN_GIA'] = float(child.text)
			elif child.tag == 'MonthlyDepreciationAmountOnDepreciation':
			   	res['GIA_TRI_KHAU_HAO_THANG_KHI_KH'] = float(child.text)
			elif child.tag == 'RefOrder':
			   	res['THU_TU_CHUNG_TU_NHAP_TRUOC_NHAP_SAU'] = int(child.text)
			elif child.tag == 'FixedAssetID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['TSCD_ID'] = rid.id
		if res['SO_CHUNG_TU'].startswith('CTTC'):
			res['ID_CHUNG_TU'] = 1
			res['MODEL_CHUNG_TU'] = 'cho.thue.tscd'
		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
	

	# Sổ công cụ dụng cụ chi tiết
	def _import_SupplyLedger(self,tag):
		rec_model = 'so.ccdc.chi.tiet'
		res = {}
		rec_id = False
		for child in tag.getchildren():
			if child.tag == 'SupplyLedgerID':
				rec_id = child.text
			elif child.tag == 'RefID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['ID_CHUNG_TU'] = rid.id
					res['MODEL_CHUNG_TU'] = rid._name
			elif child.tag == 'RefType':
			   	res['LOAI_CHUNG_TU'] = child.text
			elif child.tag == 'RefNo':
			   	res['SO_CHUNG_TU'] = child.text
			elif child.tag == 'RefDate':
			   	res['NGAY_CHUNG_TU'] = child.text
			elif child.tag == 'PostedDate':
				res['NGAY_HACH_TOAN'] = child.text
			elif child.tag == 'JournalMemo':
			   	res['DIEN_GIAI_CHUNG'] = child.text
			elif child.tag == 'Description':
			   	res['DIEN_GIAI'] = child.text
			
			elif child.tag == 'SortOrder':
				res['THU_TU_TRONG_CHUNG_TU'] = int(child.text)
			elif child.tag == 'BranchID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CHI_NHANH_ID'] = rid.id
			elif child.tag == 'IncrementAllocationTime':
				res['SO_KY_PHAN_BO_GHI_TANG'] = int(child.text)
			elif child.tag == 'DecrementAllocationTime':
				res['SO_KY_PHAN_BO_GHI_GIAM'] = int(child.text)
			elif child.tag == 'IncrementQuantity':
				res['SO_LUONG_GHI_TANG'] = float(child.text)
			elif child.tag == 'DecrementQuantity':
				res['SO_LUONG_GHI_GIAM'] = float(child.text)
			elif child.tag == 'IncrementAmount':
				res['SO_TIEN_GHI_TANG'] = float(child.text)
			elif child.tag == 'DecrementAmount':
				res['SO_TIEN_GHI_GIAM'] = float(child.text)
			elif child.tag == 'AllocationAmount':
				res['SO_TIEN_PHAN_BO'] = float(child.text)
			elif child.tag == 'TermlyAllocationAmount':
				res['SO_TIEN_PHAN_BO_HANG_KY'] = float(child.text)
			elif child.tag == 'OrganizationUnitID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['DOI_TUONG_PHAN_BO_ID'] = rid.id
			elif child.tag == 'SupplyCategoryID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['LOAI_CCDC_ID'] = rid.id
			elif child.tag == 'SupplyID':
				rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
				if rid:
					res['CCDC_ID'] = rid.id
		return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
	




 