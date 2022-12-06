# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, helper

MODULE = 'base_import_ex'
class Import(models.TransientModel):
    _inherit = 'base_import_ex.import'

    # import số dư tài khoản
    def _import_OpeningAccountEntryOther(self, tag):
        rec_model = 'account.ex.so.du.tai.khoan.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountNumber':
                tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                res['TK_ID'] = tai_khoan.id 
                res['TEN_TAI_KHOAN'] = tai_khoan.TEN_TAI_KHOAN 
                res['SO_TAI_KHOAN'] = tai_khoan.SO_TAI_KHOAN 
            elif child.tag == 'DebitAmountOC':
                res['DU_NO_NGUYEN_TE'] = float(child.text)
            elif child.tag == 'DebitAmount':
                res['DU_NO'] = float(child.text)
            elif child.tag == 'CreditAmountOC':
                res['DU_CO_NGUYEN_TE'] = float(child.text)
            elif child.tag == 'CreditAmount':
                res['DU_CO'] = float(child.text)
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'CurrencyID':
                rid = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'CashBookPostedDate':
                res['NGAY_GHI_SO'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # import số dư tài khoản ngân hàng
    def _import_OpeningAccountEntryBank(self, tag):
        rec_model = 'account.ex.so.du.tai.khoan.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountNumber':
                tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                res['TK_ID'] = tai_khoan.id 
                res['TEN_TAI_KHOAN'] = tai_khoan.TEN_TAI_KHOAN 
                res['SO_TAI_KHOAN'] = tai_khoan.SO_TAI_KHOAN 
            elif child.tag == 'DebitAmountOC':
                res['DU_NO_NGUYEN_TE'] = float(child.text)
            elif child.tag == 'DebitAmount':
                res['DU_NO'] = float(child.text)
            elif child.tag == 'CreditAmountOC':
                res['DU_CO_NGUYEN_TE'] = float(child.text)
            elif child.tag == 'CreditAmount':
                res['DU_CO'] = float(child.text)
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'BankAccountID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['TK_NGAN_HANG_ID'] = rid.id
                    res['TEN_NGAN_HANG'] = self.env['danh.muc.tai.khoan.ngan.hang'].search([('id', '=', rid.id)], limit=1).CHI_NHANH
            elif child.tag == 'CurrencyID':
                rid = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'CashBookPostedDate':
                res['NGAY_GHI_SO'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # import số dư công nợ khách hàng 
    def _import_OpeningAccountEntryCustomer(self, tag):
        rec_model = 'account.ex.so.du.tai.khoan.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountNumber':
                tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                res['TK_ID'] = tai_khoan.id 
                res['TEN_TAI_KHOAN'] = tai_khoan.TEN_TAI_KHOAN 
                res['SO_TAI_KHOAN'] = tai_khoan.SO_TAI_KHOAN 
            elif child.tag == 'DebitAmountOC':
                res['DU_NO_NGUYEN_TE'] = float(child.text)
            elif child.tag == 'DebitAmount':
                res['DU_NO'] = float(child.text)
            elif child.tag == 'CreditAmountOC':
                res['DU_CO_NGUYEN_TE'] = float(child.text)
            elif child.tag == 'CreditAmount':
                res['DU_CO'] = float(child.text)
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
                    res['TEN_DOI_TUONG'] = self.env['res.partner'].search([('id', '=', rid.id)], limit=1).HO_VA_TEN
            elif child.tag == 'CurrencyID':
                rid = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'CashBookPostedDate':
                res['NGAY_GHI_SO'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # import công nợ nhà cung cấp 
    def _import_OpeningAccountEntryVendor(self, tag):
        rec_model = 'account.ex.so.du.tai.khoan.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountNumber':
                tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                res['TK_ID'] = tai_khoan.id 
                res['TEN_TAI_KHOAN'] = tai_khoan.TEN_TAI_KHOAN 
                res['SO_TAI_KHOAN'] = tai_khoan.SO_TAI_KHOAN 
            elif child.tag == 'DebitAmountOC':
                res['DU_NO_NGUYEN_TE'] = float(child.text)
            elif child.tag == 'DebitAmount':
                res['DU_NO'] = float(child.text)
            elif child.tag == 'CreditAmountOC':
                res['DU_CO_NGUYEN_TE'] = float(child.text)
            elif child.tag == 'CreditAmount':
                res['DU_CO'] = float(child.text)
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
                    res['TEN_DOI_TUONG'] = self.env['res.partner'].search([('id', '=', rid.id)], limit=1).HO_VA_TEN
            elif child.tag == 'CurrencyID':
                rid = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'CashBookPostedDate':
                res['NGAY_GHI_SO'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # import số dư công nợ nhân viên
    def _import_OpeningAccountEntryEmployee(self, tag):
        rec_model = 'account.ex.so.du.tai.khoan.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountNumber':
                tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                res['TK_ID'] = tai_khoan.id 
                res['TEN_TAI_KHOAN'] = tai_khoan.TEN_TAI_KHOAN 
                res['SO_TAI_KHOAN'] = tai_khoan.SO_TAI_KHOAN 
            elif child.tag == 'DebitAmountOC':
                res['DU_NO_NGUYEN_TE'] = float(child.text)
            elif child.tag == 'DebitAmount':
                res['DU_NO'] = float(child.text)
            elif child.tag == 'CreditAmountOC':
                res['DU_CO_NGUYEN_TE'] = float(child.text)
            elif child.tag == 'CreditAmount':
                res['DU_CO'] = float(child.text)
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
                    res['TEN_DOI_TUONG'] = self.env['res.partner'].search([('id', '=', rid.id)], limit=1).HO_VA_TEN
            elif child.tag == 'CurrencyID':
                rid = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'CashBookPostedDate':
                res['NGAY_GHI_SO'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # import số dư tồn kho vật tư, hàng hóa
    def _import_OpeningInventoryEntry(self, tag):
        rec_model = 'account.ex.ton.kho.vat.tu.hang.hoa'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountNumber':
                tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                res['TK_ID'] = tai_khoan.id 
                res['TEN_TAI_KHOAN'] = tai_khoan.TEN_TAI_KHOAN 
                res['SO_TAI_KHOAN'] = tai_khoan.SO_TAI_KHOAN 
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id
                    res['TEN_HANG'] = self.env['danh.muc.vat.tu.hang.hoa'].search([('id', '=', rid.id)], limit=1).TEN
            elif child.tag == 'StockID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHO_ID'] = rid.id
            elif child.tag == 'UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id
            elif child.tag == 'MainUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_CHINH_ID'] = rid.id
            elif child.tag == 'SetInventoryItemSerial':
                res['NHAP_MA_QUY_CACH'] = child.text
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'Amount':
                res['GIA_TRI_TON'] = float(child.text)
            elif child.tag == 'LotNo':
                res['SO_LO'] = child.text
            elif child.tag == 'MainQuantity':
                res['SO_LUONG_THEO_DVT_CHINH'] = float(child.text)
            elif child.tag == 'MainConvertRate':
                res['TY_LE_CHUYEN_DOI_THEO_DVT_CHINH'] = float(child.text)
            elif child.tag == 'ExchangeRateOperator':
                if child.text =='*':
                    res['TOAN_TU_QUY_DOI'] = 'NHAN'
                elif child.text =='/':
                    res['TOAN_TU_QUY_DOI'] = 'CHIA'
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = child.text
            elif child.tag == 'InventoryPostedDate':
                res['NGAY_HACH_TOAN'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # import số dư chi phí dở dang
    def _import_JCOPN(self, tag):
        rec_model = 'account.ex.chi.phi.do.dang'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_DOI_TUONG_THCP_ID'] = rid.id
                    res['TEN_DOI_TUONG_THCP'] = self.env['danh.muc.doi.tuong.tap.hop.chi.phi'].search([('id', '=', rid.id)], limit=1).TEN_DOI_TUONG_THCP
                    res['LOAI_DOI_TUONG_THCP'] = self.env['danh.muc.doi.tuong.tap.hop.chi.phi'].search([('id', '=', rid.id)], limit=1).LOAI

            elif child.tag == 'ProjectWorkID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_CONG_TRINH_ID'] = rid.id
                    res['TEN_CONG_TRINH'] = self.env['danh.muc.cong.trinh'].search([('id', '=', rid.id)], limit=1).TEN_CONG_TRINH
                    # res['LOAI_CONG_TRINH'] = self.env['danh.muc.cong.trinh'].search([('id', '=', rid.id)], limit=1).LOAI

            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_HANG_ID'] = rid.id
                    res['NGAY_DON_HANG'] = self.env['account.ex.don.dat.hang'].search([('id', '=', rid.id)], limit=1).NGAY_DON_HANG
                    res['DIEN_GIAI'] = self.env['account.ex.don.dat.hang'].search([('id', '=', rid.id)], limit=1).DIEN_GIAI
                    # res['KHACH_HANG_ID'] = self.env['account.ex.don.dat.hang'].search([('id', '=', rid.id)], limit=1).KHACH_HANG_ID.HO_VA_TEN

            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_ID'] = rid.id
                    hop_dong = self.env['sale.ex.hop.dong.ban'].search([('id', '=', rid.id)], limit=1)
                    res['SO_HOP_DONG'] = hop_dong.SO_HOP_DONG
                    res['NGAY_KY'] = hop_dong.NGAY_KY
                    res['TRICH_YEU'] = hop_dong.TRICH_YEU
                    # res['KHACH_HANG_ID'] = self.env['sale.ex.hop.dong.ban'].search([('id', '=', rid.id)], limit=1).KHACH_HANG_ID.HO_VA_TEN
            elif child.tag == 'MachineIndirectMatetialAmount':
                res['MTC_CHI_PHI_NVL_GIAN_TIEP'] = float(child.text)
            elif child.tag == 'MachineIndirectLaborAmount':
                res['MTC_CHI_PHI_NHAN_CONG'] = float(child.text)
            elif child.tag == 'MachineDepreciationAmount':
                res['MTC_CHI_PHI_KHAU_HAO_DAU_KY'] = float(child.text)
            elif child.tag == 'MachinePurchaseAmount':
                res['MTC_CHI_PHI_MUA_NGOAI_DAU_KY'] = float(child.text)
            elif child.tag == 'MachineOtherAmount':
                res['MTC_CHI_PHI_KHAC_CHUNG'] = float(child.text)
                res['MTC_TONG'] = float(child.text)
            elif child.tag == 'UncompletedAccount':
                res['TAI_KHOAN_CPSXKD_DO_DANG_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id 
            elif child.tag == 'DirectMatetialAmount':
                res['CHI_PHI_NVL_TRUC_TIEP'] = float(child.text)
            elif child.tag == 'IndirectMatetialAmount':
                res['CHI_PHI_NVL_GIAN_TIEP'] = float(child.text)
                # res['CHI_PHI_CHUNG_CHI_PHI_NVL_GIAN_TIEP'] = float(child.text)
            elif child.tag == 'DirectLaborAmount':
                res['CHI_PHI_NHAN_CONG_TRUC_TIEP'] = float(child.text)
            elif child.tag == 'IndirectLaborAmount':
                res['CHI_PHI_NHAN_CONG_GIAN_TIEP'] = float(child.text)
                # res['CHI_PHI_CHUNG_CHI_PHI_NHAN_CONG_GIAN_TIEP'] = float(child.text)
            elif child.tag == 'DepreciationAmount':
                # res['KHAU_HAO'] = float(child.text)
                res['CHI_PHI_KHAU_HAO'] = float(child.text)
            elif child.tag == 'PurchaseAmount':
                res['CHI_PHI_MUA_NGOAI'] = float(child.text)
                # res['CHI_PHI_CHUNG_CHI_PHI_MUA_NGOAI_DAU_KY'] = float(child.text)
            elif child.tag == 'OtherAmount':
                res['CHI_PHI_KHAC_CHUNG'] = float(child.text)
                # res['CHI_PHI_CHUNG'] = float(child.text)
                # res['CHI_PHI_CHUNG_CHI_PHI_KHAC_CHUNG'] = float(child.text)
                # res['CHI_PHI_CHUNG_TONG'] = float(child.text)
            elif child.tag == 'TotalAmount':
                res['TONG_CHI_PHI'] = float(child.text)
            elif child.tag == 'AcceptedAmount':
                res['SO_DA_NGHIEM_THU'] = float(child.text)
            elif child.tag == 'NotAcceptedAmount':
                res['SO_CHUA_NGHIEM_THU'] = float(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # import số dư tài khoản
    def _import_OpeningAccountEntryDetailInvoice(self, tag):
        rec_model = 'account.ex.sdtkct.theo.hoa.don'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            elif child.tag == 'DueDate':
                res['HAN_THANH_TOAN'] = child.text
            elif child.tag == 'InvoiceAmountOC':
                res['GIA_TRI_HOA_DON_NGUYEN_TE'] = child.text
            elif child.tag == 'InvoiceAmount':
                res['GIA_TRI_HOA_DON'] = child.text
            elif child.tag == 'AmountOC':
                res['SO_CON_PHAI_THU_NGUYEN_TE'] = child.text
            elif child.tag == 'Amount':
                res['SO_CON_PHAI_THU'] = child.text
            elif child.tag == 'PayAmountOC':
                res['SO_THU_TRUOC_NGUYEN_TE'] = child.text
            elif child.tag == 'PayAmount':
                res['SO_THU_TRUOC'] = child.text
            elif child.tag == 'InvNo':
                res['SO_HOA_DON'] = child.text
            elif child.tag == 'InvDate':
                res['NGAY_HOA_DON'] = child.text
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['SO_DU_TAI_KHOAN_CHI_TIET_ID'] = rid.id
            elif child.tag == 'EmployeeID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHAN_VIEN_ID'] = rid.id
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
        if 'TY_GIA' not in res:
            res['TY_GIA'] =0
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    

    def _import_OpeningAccountEntryDetail(self, tag):
        rec_model = 'account.ex.sdtkct.theo.doi.tuong'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            elif child.tag == 'DebitAmountOC':
                res['DU_NO_NGUYEN_TE'] = child.text
            elif child.tag == 'DebitAmount':
                res['DU_NO'] = child.text
            elif child.tag == 'CreditAmountOC':
                res['DU_CO_NGUYEN_TE'] = child.text
            elif child.tag == 'CreditAmount':
                res['DU_CO'] = child.text
            elif child.tag == 'EmployeeID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHAN_VIEN_ID'] = rid.id
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_ID'] = rid.id
            elif child.tag == 'ProjectWorkID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CONG_TRINH_ID'] = rid.id
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['SO_DU_TAI_KHOAN_CHI_TIET_ID'] = rid.id
            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id
            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_THCP_ID'] = rid.id
            elif child.tag == 'PUContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_MUA_ID'] = rid.id
            elif child.tag == 'PUOrderRefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_MUA_HANG_ID'] = rid.id
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id
            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

