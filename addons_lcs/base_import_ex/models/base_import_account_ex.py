# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, helper

MODULE = 'base_import_ex'


class Import(models.TransientModel):
    _inherit = 'base_import_ex.import'

    # Quỹ Phiếu chi

    def _import_CAPayment(self, tag):
        rec_model = 'account.ex.phieu.thu.chi'
        res = {
            'LOAI_PHIEU':'PHIEU_CHI',
            'TYPE_NH_Q' : 'QUY'
        }
        rec_id = False

        # ref_type =''
        # for child in tag.getchildren():
        #     if child.tag =='RefType':
        #         ref_type=child.text
        #         break
        # if ref_type=='1020':
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            
            # elif child.tag == 'RefType':
            #     if child.text=='1020':
            #         res['LOAI_PHIEU'] = 'PHIEU_CHI'
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
                res['TEN_DOI_TUONG'] = child.text
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
            elif child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountObjectName':
                res['TEN_DOI_TUONG'] = child.text
            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text
            elif child.tag == 'AccountObjectContactName':
                res['NGUOI_NOP'] = child.text

            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI_PC'] = child.text
                res['LY_DO_CHI_PC_NOP_TIEN'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'EmployeeID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHAN_VIEN_ID'] = rid.id
            elif child.tag == 'DocumentIncluded':
                res['KEM_THEO_CHUNG_TU_GOC'] = child.text
            elif child.tag == 'CurrencyID':
                res['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1).id
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            
            elif child.tag == 'ReasonTypeID':
                if child.text=='21':
                    res['LY_DO_CHI'] ='TAM_UNG_CHO_NHAN_VIEN'
                elif child.text=='22':
                    res['LY_DO_CHI'] ='GUI_TIEN_VAO_NGAN_HANG'
                elif child.text=='23':
                    res['LY_DO_CHI'] ='CHI_KHAC'
            elif child.tag == 'GLVoucherRefID':
                rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHUNG_TU_NGHIEP_VU_KHAC_ID'] =rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Quỹ Phiếu chi chi tiết
    def _import_CAPaymentDetail(self, tag):
        rec_model = 'account.ex.phieu.thu.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['PHIEU_THU_CHI_ID'] = rid.id
            elif child.tag == 'Description':
                res['DIEN_GIAI_DETAIL'] = child.text
            elif child.tag == 'DebitAccount':
                res['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id 
            elif child.tag == 'CreditAccount':
                res['TK_CO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id 
            

            elif child.tag == 'AmountOC':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'Amount':
                res['SO_TIEN_QUY_DOI'] = float(child.text)
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id

            
            elif child.tag == 'BankAccountID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['TK_NGAN_HANG_ID'] = rid.id
                
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_ID'] = rid.id
            elif child.tag == 'ProjectWorkID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CONG_TRINH_ID'] = rid.id
            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id
                
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id

            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_THCP_ID'] = rid.id
                
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
            elif child.tag == 'PUContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_MUA_ID'] = rid.id
                
            elif child.tag == 'PUOrderRefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_MUA_HANG_ID'] = rid.id

            elif child.tag == 'CashOutDiffAmountFinance':
                res['CHENH_LECH'] = float(child.text)
            elif child.tag == 'CashOutDiffAccountNumberFinance':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_XU_LY_CHENH_LECH'] = rid.id  
        return self.env['ir.model.data']._update(
            rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Quỹ phiếu chi tiết (thuế)

    def _import_CAPaymentDetailTax(self, tag):
        rec_model = 'account.ex.phieu.thu.chi.thue'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['PHIEU_THU_THUE_ID'] = rid.id
            elif child.tag == 'VATAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_THUE_GTGT_ID'] = rid.id
            elif child.tag == 'VATRate':
                rid = self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:
                    res['PHAN_TRAM_THUE_GTGT_ID'] = rid.id
            elif child.tag == 'VATAmount':
                res['TIEN_THUE_GTGT'] = float(child.text)
            elif child.tag == 'TurnoverAmount':
                res['GIA_TRI_HHDV_CHUA_THUE'] = float(child.text)
           
            elif child.tag == 'Description':
                res['DIEN_GIAI_THUE'] = child.text
            elif child.tag == 'InvDate':
                res['NGAY_HOA_DON'] = child.text
            elif child.tag == 'InvNo':
                res['SO_HOA_DON'] = child.text
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_NCC'] = child.text
            elif child.tag == 'AccountObjectTaxCode':
                res['MA_SO_THUE_NCC'] = child.text
            elif child.tag == 'PurchasePurposeID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['NHOM_HHDV_MUA_VAO'] = rid.id
            elif child.tag == 'InvTemplateNo':
                rid = self.env['danh.muc.mau.so.hd'].search( [('MAU_SO_HD', '=', child.text)], limit=1)
                if rid:
                    res['MAU_SO_HD_ID'] = rid.id
            elif child.tag == 'InvSeries':
                res['KY_HIEU_HOA_DON'] = child.text
        return self.env['ir.model.data']._update(
            rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Quỹ phiếu chi thông tin trả lương

    def _import_CAPaymentDetailSalary(self, tag):
        rec_model = 'tien.luong.uy.nhiem.chi.thong.tin.tra.luong.nhan.vien'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['THONG_TIN_TRA_LUONG_CHI_TIET_ID'] = rid.id
            elif child.tag == 'EmployeeID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['MA_NHAN_VIEN'] = rid.id
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI'] = rid.id
            elif child.tag == 'Amount':
                res['SO_TRA'] = float(child.text)
            elif child.tag == 'PayableAmount':
                res['SO_CON_PHAI_TRA'] = float(child.text)
        return self.env['ir.model.data']._update(
            rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # quỹ-phiếu thu
    def _import_CAReceipt(self, tag):
        rec_model = 'account.ex.phieu.thu.chi'
        res = {
            'LOAI_PHIEU': 'PHIEU_THU',
            'TYPE_NH_Q': 'QUY'
        }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(
                    MODULE, child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_DOI_TUONG'] = child.text
            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text
            elif child.tag == 'AccountObjectContactName':
                res['NGUOI_NOP'] = child.text
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(
                    MODULE, child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'EmployeeID':
                rid = self.env.ref('{}.{}'.format(
                    MODULE, child.text), False)
                if rid:
                    res['NHAN_VIEN_ID'] = rid.id
            elif child.tag == 'DocumentIncluded':
                res['KEM_THEO_CHUNG_TU_GOC'] = child.text
            elif child.tag == 'CurrencyID':
                res['currency_id'] = self.env['res.currency'].search(
                    [('MA_LOAI_TIEN', '=', child.text)], limit=1).id
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            elif child.tag == 'ReasonTypeID':
                res['LY_DO_NOP'] =child.text

            elif child.tag == 'CustomField1':
                res['MO_RONG1'] = child.text
            elif child.tag == 'CustomField2':
                res['MO_RONG2'] = child.text
            elif child.tag == 'CustomField3':
                res['MO_RONG3'] = child.text
            elif child.tag == 'GLVoucherRefID':
                rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHUNG_TU_NGHIEP_VU_KHAC_ID'] =rid.id
        return self.env['ir.model.data']._update(
            rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # Quỹ Phiếu thu chi tiết
    def _import_CAReceiptDetail(self, tag):
        rec_model = 'account.ex.phieu.thu.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['PHIEU_THU_CHI_ID'] = rid.id
            elif child.tag == 'Description':
                res['DIEN_GIAI_DETAIL'] = child.text
            elif child.tag == 'DebitAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id
            elif child.tag == 'CreditAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id
            
            elif child.tag == 'AmountOC':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'Amount':
                res['SO_TIEN_QUY_DOI'] = float(child.text)
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'BankAccountID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['TK_NGAN_HANG_ID'] = rid.id
                
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_ID'] = rid.id
            elif child.tag == 'ProjectWorkID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CONG_TRINH_ID'] = rid.id
            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id
                
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id
            elif child.tag == 'SortOrder':
                res['THU_TU_SAP_XEP_CHI_TIET'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)



# Ngân hàng thu tiền gửi

    def _import_BADeposit(self, tag):
        rec_model = 'account.ex.phieu.thu.chi'
        res = {
            'LOAI_PHIEU': 'PHIEU_THU',
            'TYPE_NH_Q': 'NGAN_HANG'
        }
        rec_id = False
        # ref_type =''
        # for child in tag.getchildren():
        #     if child.tag =='RefType':
        #         ref_type=child.text
        #         break
        # if ref_type=='1500':
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_DOI_TUONG'] = child.text
            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text

            elif child.tag == 'BankAccountID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['TAI_KHOAN_NOP_ID'] = rid.id

            elif child.tag == 'BankName':
                res['TEN_TK_THU'] = child.text
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text


            elif child.tag == 'JournalMemo':
                res['TEN_LY_DO_THU'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'ReasonTypeID':
                res['ly_do_thu'] =child.text

            elif child.tag == 'CurrencyID':
                res['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1).id
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            elif child.tag == 'EmployeeID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHAN_VIEN_ID'] = rid.id
        return self.env['ir.model.data']._update(
            rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

        # Ngân hàng thu tiền gửi chi tiết
    def _import_BADepositDetail(self, tag):
        rec_model = 'account.ex.phieu.thu.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['PHIEU_THU_CHI_ID'] = rid.id

            elif child.tag == 'Description':
                res['DIEN_GIAI_DETAIL'] = child.text
            elif child.tag == 'DebitAccount':
                res['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search(
                    [('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag == 'CreditAccount':
                res['TK_CO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search(
                    [('SO_TAI_KHOAN', '=', child.text)], limit=1).id
           
            elif child.tag == 'AmountOC':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'Amount':
                res['SO_TIEN_QUY_DOI'] = float(child.text)
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id

            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_ID'] = rid.id
            elif child.tag == 'ProjectWorkID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CONG_TRINH_ID'] = rid.id
            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id
                
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id

            # elif child.tag == 'JobID':
            #     rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
            #     if rid:
            #         res['DOI_TUONG_THCP_ID'] = rid.id
                
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
           

        return self.env['ir.model.data']._update(
            rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Ngân hàng chi tiền( ủy nhiệm chi)

    def _import_BAWithDraw(self, tag):
        rec_model = 'account.ex.phieu.thu.chi'
        res = {
            'LOAI_PHIEU': 'PHIEU_CHI',
            'TYPE_NH_Q': 'NGAN_HANG'
        }
        rec_id = False
        # ref_type =''
        # for child in tag.getchildren():
        #     if child.tag=='RefType':
        #         ref_type= child.text
        #         break
        # if ref_type=='1510':
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_DOI_TUONG'] = child.text
                res['CO_QUAN_BH_UNC_NOP_TIEN'] = child.text
            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text

            elif child.tag == 'BankAccountID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['TAI_KHOAN_CHI_GUI_ID'] = rid.id

            elif child.tag == 'EmployeeID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['NHAN_VIEN_ID'] = rid.id

            elif child.tag == 'BankName':
                res['TEN_TK_CHI'] = child.text
            elif child.tag == 'RefType':
                if child.text =='1510':
                    res['PHUONG_THUC_TT'] = 'UY_NHIEM_CHI'
                elif child.text =='1520':
                    res['PHUONG_THUC_TT'] = 'SEC_TIEN_MAT'
                elif child.text =='1530':
                    res['PHUONG_THUC_TT'] = 'SEC_CHUYEN_KHOAN'
                res['LOAI_CHUNG_TU'] = int(child.text)
            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['TEN_NOI_DUNG_TT'] = child.text
                res['NOI_DUNG_THANH_TOAN_UNC_NOP_TIEN'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'ReasonTypeID':
                res['NOI_DUNG_TT'] =child.text
            elif child.tag == 'AccountObjectBankAccount':
                res['TAI_KHOAN_NHAN_UNC_NOP_TIEN'] = child.text
                res['TAI_KHOAN_THU_NHAN_ID'] = self.env['danh.muc.doi.tuong.chi.tiet'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id 
            elif child.tag == 'AccountObjectBankName':
                res['TEN_TK_NHAN'] =child.text
                res['TEN_TAI_KHOAN_NHAN_UNC_NOP_TIEN'] =child.text
            elif child.tag == 'CurrencyID':
                res['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1).id
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            elif child.tag == 'AccountObjectContactName':
                res['NGUOI_LINH_TIEN'] = child.text

            elif child.tag == 'AccountObjectContactIDNumber':
                res['SO_CMND'] = child.text
            elif child.tag == 'AccountObjectContactIssueDate':
                res['NGAY_CAP'] = child.text

            elif child.tag == 'AccountObjectContactIssueBy':
                res['NOI_CAP'] = child.text
        return self.env['ir.model.data']._update(
            rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Ngân hàng chi tiền gửi chi tiết(hạch toán)

    def _import_BAWithDrawDetail(self, tag):
        rec_model = 'account.ex.phieu.thu.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['PHIEU_THU_CHI_ID'] = rid.id

            elif child.tag == 'Description':
                res['DIEN_GIAI_DETAIL'] = child.text
            elif child.tag == 'DebitAccount':
                res['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search(
                    [('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag == 'CreditAccount':
                res['TK_CO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search(
                    [('SO_TAI_KHOAN', '=', child.text)], limit=1).id

            elif child.tag == 'AmountOC':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'Amount':
                res['SO_TIEN_QUY_DOI'] = float(child.text)
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id
                
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_ID'] = rid.id
            elif child.tag == 'ProjectWorkID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CONG_TRINH_ID'] = rid.id
            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id
                
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id

            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_THCP_ID'] = rid.id
                
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
            elif child.tag == 'PUContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_MUA_ID'] = rid.id
                
            elif child.tag == 'PUOrderRefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_MUA_HANG_ID'] = rid.id
            elif child.tag == 'SortOrder':
                res['THU_TU_SAP_XEP_CHI_TIET'] = int(child.text)
            
        return self.env['ir.model.data']._update(
            rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


 # Ngân hàng phiếu chi tiết (hạch toán)

    def _import_BAWithdrawDetailTax(self, tag):
        rec_model = 'account.ex.phieu.thu.chi.thue'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['PHIEU_THU_THUE_ID'] = rid.id
            elif child.tag == 'VATAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_THUE_GTGT_ID'] = rid.id
            elif child.tag == 'VATRate':
                rid = self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:
                    res['PHAN_TRAM_THUE_GTGT_ID'] = rid.id
            elif child.tag == 'VATAmount':
                res['TIEN_THUE_GTGT'] = float(child.text)
            elif child.tag == 'TurnoverAmount':
                res['GIA_TRI_HHDV_CHUA_THUE'] = float(child.text)
           
            elif child.tag == 'Description':
                res['DIEN_GIAI_THUE'] = child.text
            elif child.tag == 'InvDate':
                res['NGAY_HOA_DON'] = child.text
            elif child.tag == 'InvNo':
                res['SO_HOA_DON'] = child.text
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_NCC'] = child.text
            elif child.tag == 'AccountObjectTaxCode':
                res['MA_SO_THUE_NCC'] = child.text
            elif child.tag == 'PurchasePurposeID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['NHOM_HHDV_MUA_VAO'] = rid.id
            elif child.tag == 'InvTemplateNo':
                rid = self.env['danh.muc.mau.so.hd'].search( [('MAU_SO_HD', '=', child.text)], limit=1)
                if rid:
                    res['MAU_SO_HD_ID'] = rid.id
            elif child.tag == 'InvSeries':
                res['KY_HIEU_HOA_DON'] = child.text
        return self.env['ir.model.data']._update(
            rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Ngân hàng phiếu chi thông tin trả lương

    def _import_BAWithDrawDetailSalary(self, tag):
        rec_model = 'tien.luong.uy.nhiem.chi.thong.tin.tra.luong.nhan.vien'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['THONG_TIN_TRA_LUONG_CHI_TIET_ID'] = rid.id
            elif child.tag == 'EmployeeID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['MA_NHAN_VIEN'] = rid.id
            elif child.tag == 'BankAccountNumber':
                res['SO_TAI_KHOAN'] = self.env['danh.muc.doi.tuong.chi.tiet'].search(
                    [('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI'] = rid.id
            elif child.tag == 'Amount':
                res['SO_TRA'] = float(child.text)
            elif child.tag == 'PayableAmount':
                res['SO_CON_PHAI_TRA'] = float(child.text)
        return self.env['ir.model.data']._update(
            rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
        # Ngân hàng chuyển tiền nội bộ

    def _import_BAInternalTransfer(self, tag):
        rec_model = 'account.ex.phieu.thu.chi'
        res = {
            'LOAI_PHIEU': 'PHIEU_CHUYEN_TIEN',
            'TYPE_NH_Q': 'NGAN_HANG'
        }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'FromBankAccountID':
                rid =self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['TAI_KHOAN_CHI_GUI_ID'] =rid.id
                
            elif child.tag == 'FromBankAccountName':
                res['TEN_TK_CHI'] = child.text
            elif child.tag == 'ToBankAccountID':
                rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['TAI_KHOAN_DEN_ID'] =rid.id
                
            elif child.tag == 'ToBankAccountName':
                res['TEN_TK_NHAN_CTNB'] = child.text
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)

            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'CurrencyID':
                res['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1).id
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            # elif child.tag == 'BranchID':
            #     res['chi_nhanh_id'] = self.env.ref('{}.{}'.format(MODULE,child.text)).id

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #Ngân hàng chuyển tiền nội bộ chi tiết
    def _import_BAInternalTransferDetail(self, tag):
        rec_model = 'account.ex.phieu.thu.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['PHIEU_THU_CHI_ID'] =rid.id
                
            elif child.tag == 'Description':
                res['DIEN_GIAI_DETAIL'] = child.text
            elif child.tag == 'DebitAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id
            elif child.tag == 'CreditAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id
            
            elif child.tag == 'AmountOC':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'Amount':
                res['SO_TIEN_QUY_DOI'] = float(child.text)
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id
            elif child.tag == 'SortOrder':
                res['THU_TU_SAP_XEP_CHI_TIET'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # chứng từ nghiệp vụ khác

    def _import_GLVoucherOther(self, tag):
        rec_model = 'account.ex.chung.tu.nghiep.vu.khac'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so' 
            elif child.tag == 'RefType':
                if child.text == '4017':
                    res['LOAI_CHUNG_TU_QTTU_NVK'] = 'XU_LY_CHENH_LECH_TY_GIA_XUAT_QUY'
                    res['LOAI_CHUNG_TU'] = '4017'
                elif child.text =='4010':
                    res['LOAI_CHUNG_TU_QTTU_NVK'] = 'NGHIEP_VU'  
                    res['LOAI_CHUNG_TU'] = '4010'
                elif child.text =='4015':
                    res['LOAI_CHUNG_TU_QTTU_NVK'] = 'QUYET_TOAN'
                    res['LOAI_CHUNG_TU'] = '4015'
                elif child.text =='4016':
                    res['LOAI_CHUNG_TU_QTTU_NVK'] = 'XU_LY_CHENH_LECH_TY_GIA_TK_NGOAI_TE'
                    res['LOAI_CHUNG_TU'] = '4016'
                elif child.text =='4014':
                    res['LOAI_CHUNG_TU_QTTU_NVK'] = 'BU_TRU_CN'
                    res['LOAI_CHUNG_TU'] = '4014'
                elif child.text =='4011':
                    res['LOAI_CHUNG_TU_QTTU_NVK'] = 'KHAU_TRU_THUE_GTGT'
                    res['LOAI_CHUNG_TU'] = '4011'

            elif child.tag == 'DueDate':
                res['HAN_THANH_TOAN'] = child.text
            elif child.tag == 'DeductionAmountLastPeriod':
                res['THUE_GTGT_DAU_VAO_DUOC_KHAU_TRU'] = float(child.text)
            elif child.tag == 'DeductionAmountThisPeriod':
                res['THUE_GTGT_DAU_RA'] = float(child.text)

            elif child.tag == 'PeriodTypeVATDeduction':
                if child.text =='1':
                    res['LOAI_TO_KHAI'] = 'TO_KHAI_QUY'
                elif child.text =='0':
                    res['LOAI_TO_KHAI'] = 'TO_KHAI_THANG'


            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'CurrencyID':
                rid= self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            
            elif child.tag == 'AccountObjectName':
                res['TEN_DOI_TUONG'] = child.text
            elif child.tag == 'CreditAccount':
                rid= self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_XU_LY_LAI_ID'] = rid.id
            elif child.tag == 'DebitAccount':
                rid= self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_XU_LY_LO_ID'] = rid.id
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id

            elif child.tag == 'Month':
                res['THANG'] = child.text
            elif child.tag == 'Year':
                res['NAM'] = int(child.text)
            elif child.tag == 'CrossEntryDate':
                res['NGAY_BU_TRU'] = child.text
        
        for child in tag.getchildren():
            if child.tag == 'Month':
                if 'LOAI_TO_KHAI' in res:
                    if res['LOAI_TO_KHAI'] == 'TO_KHAI_QUY':
                        res['KY_TINH_THUE_QUY'] = child.text
                    elif res['LOAI_TO_KHAI'] == 'TO_KHAI_THANG':
                        res['KY_TINH_THUE_THANG'] = child.text
                    break
            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)



        #chứng từ quyết toán tạm ứng

    def _import_GLVoucherAdvance(self, tag):
        rec_model = 'account.ex.chung.tu.nghiep.vu.khac'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = child.text
                if child.text == '4015':
                    res['LOAI_CHUNG_TU_QTTU_NVK'] = 'QUYET_TOAN'
            elif child.tag == 'AdvancedAmountOC':
                res['SO_TIEN_TAM_UNG'] = float(child.text)
            elif child.tag == 'DiffAmountOC':
                res['SO_TIEN_THUA_THIEU'] = float(child.text)
            elif child.tag == 'AdvancedAmount':
                res['SO_TIEN_TAM_UNG_QD'] = float(child.text)
            elif child.tag == 'DiffAmount':
                res['SO_TIEN_THUA_THIEU_QD'] = float(child.text)
            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'EmployeeID':
                rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['NHAN_VIEN_ID'] =rid.id
            elif child.tag =='IsOnceSettlementAdvance':
                res['QUYET_TOAN_CHO_TUNG_LAN_TAM_UNG'] = True if child.text == 'true' else False  
            elif child.tag == 'CurrencyID':
                rid= self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            # elif child.tag == 'CurrencyID':
            #     res['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1).id
            # elif child.tag == 'ExchangeRate':
            #     res['TY_GIA'] = float(child.text)
            # elif child.tag == 'BranchID':
            #     res['chi_nhanh_id'] = self.env.ref('{}.{}'.format(MODULE,child.text)).id

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)





# Kết chuyển lãi, lỗ
    def _import_GLVoucherProfitAndLoss(self, tag):
        rec_model = 'account.ex.chung.tu.nghiep.vu.khac'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so' 
            elif child.tag == 'RefType':
                if child.text == '4012':
                    res['LOAI_CHUNG_TU'] = '4012'
           

            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id

            res['LOAI_CHUNG_TU_QTTU_NVK'] = 'KET_CHUYEN_LAI_LO'

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

# chứng từ nghiệp vụ khác  chi tiết(hạch toán)
    def _import_GLVoucherDetail(self, tag):
        rec_model = 'account.ex.chung.tu.nghiep.vu.khac.hach.toan'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHUNG_TU_NGHIEP_VU_KHAC_ID'] = rid.id
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'DebitAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id  
            elif child.tag == 'CreditAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id   
            elif child.tag == 'AmountOC':
                res['SO_TIEN'] = float(child.text)
            
            elif child.tag == 'BusinessType':
                if child.text =='3':
                    res['NGHIEP_VU'] = 'KHAU_TRU_THUE_HOAT_DONG_KINH_DOANH'
                elif child.text =='4':
                    res['NGHIEP_VU'] = 'KHAU_TRU_THUE_HOAT_DONG_DAU_TU'

            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_NO_ID'] = rid.id
            elif child.tag == 'CreditAccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_CO_ID'] = rid.id
            elif child.tag == 'BankAccountID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['TK_NGAN_HANG_ID'] = rid.id
            elif child.tag == 'EmployeeID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHAN_VIEN_ID'] = rid.id
            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_ID'] = rid.id
            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_THCP_ID'] = rid.id
            elif child.tag == 'ProjectWorkID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CONG_TRINH_ID'] = rid.id
            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
            elif child.tag == 'PUOrderRefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_MUA_HANG_ID'] = rid.id
            elif child.tag == 'PUContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_MUA_ID'] = rid.id
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id
            elif child.tag =='UnResonableCost':
                res['CP_KHONG_HOP_LY'] = True if child.text == 'true' else False
            elif child.tag == 'CashOutAmountOC':
                res['SO_TIEN_DA_XUAT'] = float(child.text)
            elif child.tag == 'CashOutAmountOrg':
                res['QUY_DOI_THEO_CT_GOC'] = float(child.text)
            elif child.tag == 'CashOutExchangeRate':
                res['TY_GIA_XUAT_QUY_BINH_QUAN'] = float(child.text)
            elif child.tag == 'CashOutAmount':
                res['QUY_DOI_THEO_TY_GIA_XUAT_QUY'] = float(child.text)
            elif child.tag == 'Amount':
                res['SO_TIEN_QUY_DOI'] = float(child.text)
            elif child.tag == 'CashOutCurrencyID':
                rid= self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
            elif child.tag == 'VATAmountOC':
                res['TIEN_THUE_GTGT'] = float(child.text)
            elif child.tag == 'VATAmount':
                res['TIEN_THUE_GTGT_QD'] = float(child.text)
            elif child.tag == 'VATAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_THUE_GTGT_ID'] = rid.id  
            elif child.tag == 'VATRate':
                rid = self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search( [('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:
                    res['PHAN_TRAM_THUE_GTGT_ID'] = rid.id
               
            elif child.tag == 'InvTemplateNo':
                rid = self.env['danh.muc.mau.so.hd'].search( [('MAU_SO_HD', '=', child.text)], limit=1)
                if rid:
                    res['MAU_SO_HD_ID'] = rid.id
            elif child.tag == 'PurchasePurposeID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHOM_HHDV_MUA_VAO_ID'] = rid.id
                
            elif child.tag == 'InvSeries':
                res['KY_HIEU_HD'] = child.text
            elif child.tag == 'InvNo':
                res['SO_HOA_DON'] = child.text
            elif child.tag == 'InvDate':
                res['NGAY_HOA_DON'] = child.text 


            elif child.tag == 'CashOutExchangeRateFinance':
                res['TY_GIA_XUAT_QUY'] = float(child.text)
            elif child.tag == 'CashOutAmountFinance':
                res['THANH_TIEN_THEO_TY_GIA_XUAT_QUY'] = float(child.text)
            elif child.tag == 'CashOutDiffAmountFinance':
                res['CHENH_LECH'] = float(child.text) 

            elif child.tag == 'CashOutDiffAccountNumberFinance':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_XU_LY_CHENH_LECH'] = rid.id  

            elif child.tag == 'TaxAccountObjectTaxCode':
                res['MA_SO_THUE'] = child.text
            elif child.tag == 'TaxAccountObjectAddress':
                res['DIA_CHI'] = child.text 
            elif child.tag =='NotIncludeInvoice':
                res['KHONG_CO_HOA_DON'] = True if child.text == 'true' else False 
            elif child.tag == 'LastExchangeRate':
                res['TY_GIA_DANH_GIA_LAI_GAN_NHAT'] = child.text 
            elif child.tag == 'SortOrder':
                res['THU_TU_SAP_XEP_CHI_TIET'] = int(child.text)
            elif child.tag == 'DebitBankAccount':
                res['SO_TAI_KHOAN_NGAN_HANG_DT_NO'] = child.text
            elif child.tag == 'DebitBankName':
                res['TEN_TAI_KHOAN_NGAN_HANG_DT_NO'] = child.text  
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

 #CHỨNG từ nghiệp vụ khác chi tiết(số dư ngoại tệ)
    def _import_GLVoucherDetailForeignExchange(self, tag):
        rec_model = 'tong.hop.chung.tu.nghiep.vu.khac.so.du.ngoai.te'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHUNG_TU_NGHIEP_VU_KHAC_ID'] =rid.id
            elif child.tag == 'AccountNumber':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TAI_KHOAN_ID'] = rid.id  
              
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            elif child.tag == 'DebitAmountOC':
                res['SO_TIEN_DU_NO'] = float(child.text)
            elif child.tag == 'DebitAmount':
                res['QUY_DOI_DU_NO'] = float(child.text)
            elif child.tag == 'DebitRevaluate':
                res['DANH_GIA_LAI_DU_NO'] =float(child.text)
            elif child.tag == 'DebitDifference':
                res['CHENH_LECH_DU_NO'] = float(child.text)

            elif child.tag == 'CreditAmountOC':
                res['SO_TIEN_DU_CO'] = float(child.text)
            elif child.tag == 'CreditAmount':
                res['QUY_DOI_DU_CO'] = float(child.text)
            elif child.tag == 'CreditRevaluate':
                res['DANH_GIA_LAI_DU_CO'] =float(child.text)
            elif child.tag == 'CreditDifference':
                res['CHENH_LECH_DU_CO'] = float(child.text)
  
            elif child.tag == 'BankAccountID':
                rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['TK_NGAN_HANG_ID'] =rid.id
            
            
            
            
            elif child.tag == 'AccountObjectID':
                rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] =rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_DOI_TUONG'] = child.text
            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #CHỨNG từ nghiệp vụ khác chi tiết(công nợ và thanh toán)
    def _import_GLVoucherDetailDebtPayment(self, tag):
        rec_model = 'tong.hop.chung.tu.nghiep.vu.khac.cong.no.thanh.toan'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHUNG_TU_NGHIEP_VU_KHAC_ID'] =rid.id
            elif child.tag == 'VoucherAccountNumber':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CONG_NO_ID'] = rid.id  
            
            elif child.tag == 'VoucherRefType':
                rid = self.env['danh.muc.reftype'].search( [('REFTYPE', '=', child.text)], limit=1)
                if rid:
                    res['LOAI_CHUNG_TU_ID'] = rid.id  
                res['LOAI_CHUNG_TU'] =child.text
            elif child.tag == 'VoucherRefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'VoucherPostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'VoucherInvNo':
                res['SO_HOA_DON'] = child.text
            elif child.tag == 'VoucherRefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'VoucherJounalMemo':
                res['DIEN_GIAI'] = child.text
            
            elif child.tag == 'VoucherExchangeRate':
                res['TY_GIA_TREN_CT'] = float(child.text)
            elif child.tag == 'LastExchangeRate':
                res['TY_GIA_DANH_GIA_LAI_GAN_NHAT'] = float(child.text)
            elif child.tag == 'ReamainingAmountOC':
                res['SO_CHUA_DOI_TRU'] = float(child.text)
            elif child.tag == 'ReamainingAmount':
                res['SO_CHUA_DOI_TRU_QUY_DOI'] =float(child.text)
            # elif child.tag == 'ReValueAmount':
            #     res['CHENH_LECH_DU_NO'] = float(child.text)
            elif child.tag == 'DiffAmount':
                res['CHENH_LECH'] = float(child.text)
            elif child.tag == 'ReValueAmount':
                res['DANH_GIA_LAI'] = float(child.text)
            elif child.tag == 'RevalueExchangeRate':
                res['TY_GIA_DANH_GIA_LAI'] = float(child.text)
            
            elif child.tag == 'VoucherAccountObjectID':
                rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] =rid.id    
            elif child.tag == 'VoucherRefID':
                rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['ID_CHUNG_TU_GOC'] =rid.id
                    res['MODEL_CHUNG_TU_GOC'] =rid._name
            elif child.tag == 'VoucherInvDate':
                res['NGAY_HOA_DON'] = child.text
           
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #CHỨNG từ nghiệp vụ khác chi tiết(Chứng từ công nợ)
    def _import_GLVoucherCrossEntryDetail(self, tag):
        rec_model = 'sale.ex.doi.tru.chi.tiet'
        res = {}
        rec_id = False

        Cross_Type = ''
        for child in tag.getchildren():
            if child.tag=='CrossType':
                Cross_Type = child.text
                break
        #Cross_Type = 2 : Bù trừ công nợ  GLVoucherRefID
        #Cross_Type = 1 : đối trừ chứng từ  RefDetailID
        #Cross_Type = 0 : đối trừ chứng từ khách hàng RefDetailID
        if Cross_Type == '2':
            rec_model = 'tong.hop.chung.tu.nvk.bu.tru.chi.tiet'
            res = {}
            rec_id = False
            receipt_type = ''
            for child in tag.getchildren():
                if child.tag=='ReceiptType':
                    receipt_type = child.text
                    break

            if receipt_type=='true':
                for child in tag.getchildren():
                    if child.tag == 'MappingCrossID':
                        rec_id = child.text
                    elif child.tag == 'GLVoucherRefID':
                        rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                        if rid:
                            res['CHUNG_TU_NGHIEP_VU_KHAC_ID'] =rid.id
                    elif child.tag == 'DebtRefType':
                        res['LOAI_CHUNG_TU_CONG_NO'] = child.text
                        rid= self.env['danh.muc.reftype'].search([('REFTYPE', '=', child.text)], limit=1)
                        if rid:
                            res['TEN_LOAI_CHUNG_TU_CONG_NO'] = rid.REFTYPENAME
                    elif child.tag == 'DebtRefDate':
                        res['NGAY_CHUNG_TU_CONG_NO'] = child.text
                    elif child.tag == 'DebtRefNo':
                        res['SO_CHUNG_TU_CONG_NO'] = child.text
                    elif child.tag == 'DebtInvNo':
                        res['SO_HOA_DON_CONG_NO'] = child.text

                    elif child.tag == 'TotalDebtableAmountOC':
                        res['SO_TIEN_CON_NO'] = float(child.text)
                    elif child.tag == 'TotalDebtableAmount':
                        res['SO_TIEN_CON_NO_QUY_DOI'] = float(child.text)
                    elif child.tag == 'DebtableAmountOC':
                        res['SO_TIEN_CONG_NO'] = float(child.text)
                    elif child.tag == 'DebtableAmount':
                        res['SO_TIEN_CONG_NO_QUY_DOI'] = child.text
                    elif child.tag == 'DebtAmountOC':
                        res['SO_CONG_NO_THANH_TOAN_LAN_NAY'] = float(child.text)
                    elif child.tag == 'DebtAmount':
                        res['SO_CONG_NO_THANH_TOAN_LAN_NAY_QUY_DOI'] = float(child.text)


                    elif child.tag =='CrossType':
                        if child.text == '1':
                            res['LOAI_DOI_TRU'] = '1'
                        elif child.text == '0':
                            res['LOAI_DOI_TRU'] = '0'
                        elif child.text == '2':
                            res['LOAI_DOI_TRU'] = '2'
                    elif child.tag == 'CurrencyID':
                        rid= self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                        if rid:
                            res['currency_id'] = rid.id
                    elif child.tag == 'AccountNumber':
                        rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
                        if rid:
                            res['TAI_KHOAN_ID'] = rid.id 
                    elif child.tag == 'DebtRefID':
                        rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                        if rid:
                            res['ID_CHUNG_TU_CONG_NO'] = rid.id
                            res['MODEL_CHUNG_TU_CONG_NO'] = rid._name 
                    elif child.tag =='IsPayVoucherPosted':
                        res['CTTT_DA_GHI_SO'] = True if child.text == 'true' else False 
            else:
                for child in tag.getchildren():
                    if child.tag == 'MappingCrossID':
                        rec_id = child.text
                    if child.tag == 'IsPostedFinance':
                        res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
                    elif child.tag == 'GLVoucherRefID':
                        rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                        if rid:
                            res['CHUNG_TU_NGHIEP_VU_KHAC_ID'] =rid.id
                    elif child.tag == 'DebtRefType':
                        res['LOAI_CHUNG_TU_THANH_TOAN'] = child.text
                        rid= self.env['danh.muc.reftype'].search([('REFTYPE', '=', child.text)], limit=1)
                        if rid:
                            res['TEN_LOAI_CHUNG_TU_THANH_TOAN'] = rid.REFTYPENAME
                    elif child.tag == 'PayRefID':
                        rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                        if rid:
                            res['ID_CHUNG_TU_THANH_TOAN'] = rid.id
                            res['MODEL_CHUNG_TU_THANH_TOAN'] = rid._name
                    elif child.tag == 'DebtRefDate':
                        res['NGAY_CHUNG_TU_THANH_TOAN'] =child.text
                    elif child.tag == 'DebtInvNo':
                        res['SO_HOA_DON_THANH_TOAN'] = child.text
                    elif child.tag == 'DebtRefNo':
                        res['SO_CHUNG_TU_THANH_TOAN'] = child.text
                    elif child.tag == 'DebtDueDate':
                        res['HAN_THANH_TOAN'] = child.text

                    elif child.tag == 'TotalDebtableAmountOC':
                        res['SO_CHUA_THANH_TOAN'] = float(child.text)
                    elif child.tag == 'TotalDebtableAmount':
                        res['SO_CHUA_THANH_TOAN_QUY_DOI'] = float(child.text)
                    elif child.tag == 'DebtableAmountOC':
                        res['SO_TIEN_THANH_TOAN'] = float(child.text)
                    elif child.tag == 'DebtableAmount':
                        res['SO_TIEN_THANH_TOAN_QUY_DOI'] = child.text
                    elif child.tag == 'DebtAmountOC':
                        res['SO_THANH_TOAN_LAN_NAY'] = float(child.text)
                    elif child.tag == 'DebtAmount':
                        res['SO_THANH_TOAN_LAN_NAY_QUY_DOI'] = float(child.text)

                    elif child.tag =='CrossType':
                        if child.text == '1':
                            res['LOAI_DOI_TRU'] = '1'
                        elif child.text == '0':
                            res['LOAI_DOI_TRU'] = '0'
                        elif child.text == '2':
                            res['LOAI_DOI_TRU'] = '2'
                    elif child.tag == 'CurrencyID':
                        rid= self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                        if rid:
                            res['currency_id'] = rid.id
                    elif child.tag == 'AccountNumber':
                        rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
                        if rid:
                            res['TAI_KHOAN_ID'] = rid.id
                    elif child.tag =='IsDebtVoucherPosted':
                        res['CTCN_DA_GHI_SO'] = True if child.text == 'true' else False
                    elif child.tag == 'DebtEmployeeID':
                        rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                        if rid:
                            res['NHAN_VIEN_ID'] = rid.id  
            self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
        
        #cập nhật toàn bộ cho đối trừ
        rec_model = 'sale.ex.doi.tru.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            # import đối trừ chứng từ
            if child.tag == 'RefDetailID':
                    rec_id = child.text
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'PayRefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['ID_CHUNG_TU_THANH_TOAN'] = rid.id
                    res['MODEL_CHUNG_TU_THANH_TOAN'] = rid._name
            elif child.tag == 'DebtRefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['ID_CHUNG_TU_CONG_NO'] = rid.id
                    res['MODEL_CHUNG_TU_CONG_NO'] = rid._name
            elif child.tag == 'AccountNumber':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TAI_KHOAN_ID'] = rid.id  
            elif child.tag == 'DiscountAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TAI_KHOAN_GIAM_GIA_ID'] = rid.id   
            elif child.tag =='CrossType':
                if child.text == '1':
                    res['LOAI_DOI_TRU'] = '1'
                elif child.text == '0':
                    res['LOAI_DOI_TRU'] = '0'
                elif child.text == '2':
                    res['LOAI_DOI_TRU'] = '2'
            elif child.tag == 'CurrencyID':
                    res['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1).id
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'PayRefType':
                res['LOAI_CHUNG_TU_THANH_TOAN'] = child.text
                rid= self.env['danh.muc.reftype'].search([('REFTYPE', '=', child.text)], limit=1)
                if rid:
                    res['TEN_LOAI_CHUNG_TU_THANH_TOAN'] = rid.REFTYPENAME
            elif child.tag == 'DebtRefType':
                res['LOAI_CHUNG_TU_CONG_NO'] = child.text
                rid= self.env['danh.muc.reftype'].search([('REFTYPE', '=', child.text)], limit=1)
                if rid:
                    res['TEN_LOAI_CHUNG_TU_CONG_NO'] = rid.REFTYPENAME
            elif child.tag == 'PayPostedDate':
                res['NGAY_HACH_TOAN_THANH_TOAN'] = child.text
            elif child.tag == 'PayRefNo':
                res['SO_CHUNG_TU_THANH_TOAN'] = child.text
            elif child.tag == 'PayAmountOC':
                res['SO_TIEN_THANH_TOAN'] = float(child.text)
            elif child.tag == 'PayAmount':
                res['SO_TIEN_THANH_TOAN_QUY_DOI'] = float(child.text)
            elif child.tag == 'DebtExchangeRate':
                res['TY_GIA_CONG_NO'] = float(child.text)

            elif child.tag == 'PayRefDate':
                res['NGAY_CHUNG_TU_THANH_TOAN'] = child.text
            elif child.tag == 'DebtRefDate':
                res['NGAY_CHUNG_TU_CONG_NO'] = child.text
            elif child.tag == 'DebtPostedDate':
                res['NGAY_HACH_TOAN_CONG_NO'] = child.text
            elif child.tag == 'DebtRefNo':
                res['SO_CHUNG_TU_CONG_NO'] = child.text
            elif child.tag == 'DebtInvNo':
                res['SO_HOA_DON_CONG_NO'] = child.text
            elif child.tag == 'DebtDueDate':
                res['HAN_THANH_TOAN_CONG_NO'] = child.text
            elif child.tag == 'DebtAmountOC':
                res['SO_TIEN_CONG_NO'] = float(child.text)
            elif child.tag == 'DebtAmount':
                res['SO_TIEN_CONG_NO_QUY_DOI'] = float(child.text)
            elif child.tag == 'ExchangeDiffAmount':
                res['CHENH_LECH_TY_GIA_SO_TIEN_QUY_DOI'] = float(child.text)
            elif child.tag =='IsPayVoucherPosted':
                res['CTTT_DA_GHI_SO'] = True if child.text == 'true' else False 
            elif child.tag =='IsDebtVoucherPosted':
                res['CTCN_DA_GHI_SO'] = True if child.text == 'true' else False
            elif child.tag == 'DebtEmployeeID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHAN_VIEN_ID'] = rid.id 
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)







    #CHỨNG từ nghiệp vụ khác chi tiết(thuế)
    def _import_GLVoucherDetailTax(self, tag):
        rec_model = 'account.ex.thue'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHUNG_TU_KHAC_THUE_ID'] =rid.id
            elif child.tag == 'VATAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_THUE_GTGT_ID'] = rid.id  
            elif child.tag == 'InvTemplateNo':
                rid = self.env['danh.muc.mau.so.hd'].search( [('MAU_SO_HD', '=', child.text)], limit=1)
                if rid:
                    res['MAU_SO_HD_ID'] = rid.id
            elif child.tag == 'PurchasePurposeID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHOM_HHDV_MUA_VAO_ID'] = rid.id  
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            
            elif child.tag == 'VATAmount':
                res['TIEN_THUE_GT'] = float(child.text)
            elif child.tag == 'TurnoverAmount':
                res['GIA_TRI_HHDV_CHUA_THUE'] = float(child.text)
            elif child.tag == 'InvSeries':
                res['KY_HIEU_HD'] = child.text
            elif child.tag == 'InvNo':
                res['SO_HOA_DON'] = child.text
            elif child.tag == 'InvDate':
                res['NGAY_HOA_DON'] = child.text
            
            elif child.tag == 'AccountObjectID':
                rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] =rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_DOI_TUONG'] = child.text
            elif child.tag == 'AccountObjectTaxCode':
                res['MA_SO_THUE'] = child.text
            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text
            elif child.tag == 'VATRate':
                rid = self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search( [('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:
                    res['PHAN_TRAM_THUE_GTGT_ID'] = rid.id   
                
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    

 # Phân bổ chi phí bảo hiểm,QLDN, chi phí khác cho đơn vị

    def _import_JCAllocationExpense(self, tag):
        rec_model = 'tong.hop.phan.bo.chi.phi.bh.qldn.chi.phi.khac.cho.don.vi'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
                if child.text=='4100':
                    res['PHAN_BO_SELECTION_LAY_DU_LIEU'] = 'PHAN_BO_CHO_DON_VI'
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'RefNo':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'PeriodDescription':
                res['KY_PHAN_BO'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'AllocationMethod':
                res['TIEU_THUC_PHAN_BO_ALL'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #Phân bổ chi phí bảo hiểm,QLDN, chi phí khác cho đơn vị chi tiết(chi phí)
    def _import_JCAllocationExpenseDetail(self, tag):
        rec_model = 'tong.hop.phan.bo.chi.phi.bh.qldn.chi.tiet.chi.phi'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID'] =rid.id
            elif child.tag == 'AccountNumber':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TAI_KHOAN_ID'] = rid.id  
              
            elif child.tag == 'AccountName':
                res['TEN_TAI_KHOAN'] = child.text

            elif child.tag == 'TotalCostAmount':
                res['TONG_CHI_PHI'] = float(child.text)
            elif child.tag == 'AllocationRate':
                res['TY_LE_PHAN_BO'] = float(child.text)
            elif child.tag == 'AllocationAmount':
                res['SO_TIEN_PHAN_BO'] =float(child.text)
             
            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id
            elif child.tag == 'ExpenseItemName':
                res['TEN_KHOAN_MUC_CHI_PHI'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #Phân bổ chi phí bảo hiểm,QLDN, chi phí khác cho đơn vị chi tiết(Phân bổ)
    def _import_JCAllocationExpenseDetailTable(self, tag):
        rec_model = 'tong.hop.phan.bo.chi.phi.bh.qldn.chi.tiet.phan.bo'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID'] =rid.id
            elif child.tag == 'AllocationObjectID':
                rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['MA_DON_VI_ID'] =rid.id
            elif child.tag == 'AccountNumber':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TAI_KHOAN_ID'] = rid.id  
              
            elif child.tag == 'AllocationRate':
                res['TY_LE'] = float(child.text)
            elif child.tag == 'AllocationAmount':
                res['SO_TIEN'] = float(child.text)

            elif child.tag == 'AllocationObjectType':
                res['CAP_TO_CHUC'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # # chứng từ quyết toán tạm ứng  chi tiết(hạch toán)
    # def _import_GLVoucherDetail(self, tag):
    #     rec_model = 'account.ex.tam.ung.hach.toan'
    #     res = {}
    #     rec_id = False
    #     for child in tag.getchildren():
    #         if child.tag == 'RefDetailID':
    #             rec_id = child.text
    #         elif child.tag == 'RefID':
    #             rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
    #             if rid:
    #                 res['TAM_UNG_HACH_TOAN_ID'] = rid.id
    #         elif child.tag == 'Description':
    #             res['DIEN_GIAI'] = child.text
    #         elif child.tag == 'DebitAccount':
    #             rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
    #             if rid:
    #                 res['TK_NO_ID'] = rid.id  
    #         elif child.tag == 'CreditAccount':
    #             rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
    #             if rid:
    #                 res['TK_CO_ID'] = rid.id   
    #         elif child.tag == 'AmountOC':
    #             res['SO_TIEN'] = float(child.text)
    #         elif child.tag == 'Amount':
    #             res['SO_TIEN_QUY_DOI'] = float(child.text)
    #         elif child.tag == 'VATAmountOC':
    #             res['TIEN_THUE_GTGT'] = float(child.text)
    #         # elif child.tag == 'DueDate':
    #         #     res['NGHIEP_VU'] = child.text
    #         elif child.tag == 'VATDescription':
    #             res['DIEN_GIAI_THUE'] = child.text
    #         elif child.tag == 'AccountObjectID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
    #             if rid:
    #                 res['DOI_TUONG_NO_ID'] = rid.id
    #         elif child.tag == 'CreditAccountObjectID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
    #             if rid:
    #                 res['DOI_TUONG_CO_ID'] = rid.id

    #         elif child.tag == 'ExpenseItemID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
    #             if rid:
    #                 res['KHOAN_MUC_CP_ID'] = rid.id
    #         elif child.tag == 'OrganizationUnitID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
    #             if rid:
    #                 res['DON_VI_ID'] = rid.id
    #         elif child.tag == 'JobID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
    #             if rid:
    #                 res['DOI_TUONG_THCP_ID'] = rid.id
    #         elif child.tag == 'ProjectWorkID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
    #             if rid:
    #                 res['CONG_TRINH_ID'] = rid.id
    #         elif child.tag == 'ContractID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
    #             if rid:
    #                 res['HOP_DONG_BAN_ID'] = rid.id
    #         elif child.tag == 'OrderID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
    #             if rid:
    #                 res['DON_DAT_HANG_ID'] = rid.id
    #         elif child.tag == 'PUOrderRefID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
    #             if rid:
    #                 res['DON_MUA_HANG_ID'] = rid.id
    #         elif child.tag == 'PUContractID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
    #             if rid:
    #                 res['HOP_DONG_MUA_ID'] = rid.id
    #         elif child.tag == 'ListItemID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
    #             if rid:
    #                 res['MA_THONG_KE_ID'] = rid.id
    #         elif child.tag == 'VATRate':
    #             rid = self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search( [('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
    #             if rid:
    #                 res['PHAN_TRAM_THUE_GTGT_ID'] = rid.id
    #         elif child.tag == 'VATAccount':
    #             rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
    #             if rid:
    #                 res['TK_THUE_GTGT_ID'] = rid.id     
    #         elif child.tag =='UnResonableCost':
    #             res['CP_KHONG_HOP_LY'] = True if child.text == 'true' else False  
    #         elif child.tag =='NotIncludeInvoice':
    #             res['KHONG_CO_HOA_DON'] = True if child.text == 'true' else False 
    #         elif child.tag == 'InvTemplateNo':
    #             rid = self.env['danh.muc.mau.so.hd'].search( [('MAU_SO_HD', '=', child.text)], limit=1)
    #             if rid:
    #                 res['MAU_SO_HD_ID'] = rid.id
    #         elif child.tag == 'PurchasePurposeID':
    #             rid = self.env['danh.muc.nhom.hhdv'].search( [('MA_NHOM_HHDV', '=', child.text)], limit=1)
    #             if rid:
    #                 res['NHOM_HHDV_MUA_VAO_ID'] = rid.id        
    #         elif child.tag == 'Description':
    #             res['DIEN_GIAI'] = child.text
    #         elif child.tag == 'InvSeries':
    #             res['KY_HIEU_HD'] = child.text
    #         elif child.tag == 'InvNo':
    #             res['SO_HOA_DON'] = child.text
    #         elif child.tag == 'InvDate':
    #             res['NGAY_HOA_DON'] = child.text
    #         elif child.tag == 'AccountObjectTaxCode':
    #             res['MA_SO_THUE'] = child.text
    #         elif child.tag == 'AccountObjectAddress':
    #             res['DIA_CHI'] = child.text  
    #     return self.env['ir.model.data']._update(
    #         rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    #CHỨNG từ quyết toán tạm ứng chi  chi tiết(hoa đơn)
    # def _import_GLVoucherDetail(self, tag):
    #     rec_model = 'account.ex.tam.ung.hoa.don'
    #     res = {}
    #     rec_id = False
    #     for child in tag.getchildren():
    #         if child.tag == 'RefDetailID':
    #             rec_id = child.text
    #         elif child.tag == 'RefID':
    #             rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
    #             if rid:
    #                 res['TAM_UNG_HOA_DON_ID'] =rid.id
    #         elif child.tag =='NotIncludeInvoice':
    #             res['KHONG_CO_HOA_DON'] = True if child.text == 'true' else False 
    #         elif child.tag == 'InvTemplateNo':
    #             rid = self.env['danh.muc.mau.so.hd'].search( [('MAU_SO_HD', '=', child.text)], limit=1)
    #             if rid:
    #                 res['MAU_SO_HD_ID'] = rid.id
    #         elif child.tag == 'PurchasePurposeID':
    #             rid = self.env['danh.muc.nhom.hhdv'].search( [('MA_NHOM_HHDV', '=', child.text)], limit=1)
    #             if rid:
    #                 res['NHOM_HHDV_MUA_VAO_ID'] = rid.id        
    #         elif child.tag == 'Description':
    #             res['DIEN_GIAI'] = child.text
    #         elif child.tag == 'InvSeries':
    #             res['KY_HIEU_HD'] = child.text
    #         elif child.tag == 'InvNo':
    #             res['SO_HOA_DON'] = child.text
    #         elif child.tag == 'InvDate':
    #             res['NGAY_HOA_DON'] = child.text
            
    #         elif child.tag == 'AccountObjectID':
    #             rid=self.env.ref('{}.{}'.format(MODULE, child.text), False)
    #             if rid:
    #                 res['DOI_TUONG_ID'] =rid.id
    #         elif child.tag == 'AccountObjectName':
    #             res['TEN_DOI_TUONG'] = child.text
    #         elif child.tag == 'AccountObjectTaxCode':
    #             res['MA_SO_THUE'] = child.text
    #         elif child.tag == 'AccountObjectAddress':
    #             res['DIA_CHI'] = child.text  
    #     return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    

    

    # # Chi phí trả trước chi tiết(thiết lập phân bổ)
    # def _import_PrepaidExpensesDetail(self, tag):
    #     rec_model = 'tong.hop.chi.phi.tra.truoc.thiet.lap.phan.bo'
    #     res = {}
    #     rec_id = False
    #     for child in tag.getchildren():
    #         if child.tag == 'PrepaidExpensesDetailID':
    #             rec_id = child.text
    #         elif child.tag == 'PrepaidExpensesID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
    #             if rid:
    #                 res['CHI_PHI_TRA_TRUOC_ID'] = rid.id
            
    #         elif child.tag == 'AllocationObjectID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
    #             if rid:
    #                 res['DOI_TUONG_PHAN_BO_ID'] = rid.id
    #         elif child.tag == 'AllocationObjectName':
    #             res['TEN_DOI_TUONG_PHAN_BO'] = child.text
    #         elif child.tag == 'CostAccount':
    #             rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
    #             if rid:
    #                 res['TK_NO_ID'] = rid.id
    #         elif child.tag == 'AllocationRate':
    #             res['TY_LE_PB'] = float(child.text)
    #         elif child.tag == 'ExpenseItemID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
    #             if rid:
    #                 res['KHOAN_MUC_CP_ID'] = rid.id
    #     return self.env['ir.model.data']._update(
    #         rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # phân bổ chi phí trả trước

    def _import_GLVoucherExpense(self, tag):
        rec_model = 'account.ex.chung.tu.nghiep.vu.khac'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so' 
            
            elif child.tag == 'RefType':                
                res['LOAI_CHUNG_TU'] = int(child.text)
            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'Month':
                res['THANG'] = child.text
            elif child.tag == 'Year':
                res['NAM'] = int(child.text)
           
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # phân bổ chi phí chi tiết(xác định chi phí)
    def _import_GLVoucherDetailExpenses(self, tag):
        rec_model = 'tong.hop.phan.bo.chi.phi.tra.truoc.xd.chi.phi'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['PHAN_BO_CHI_PHI_TRA_TRUOC_ID'] = rid.id
            
            
            elif child.tag == 'PrepaidExpensesID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_CP_TRA_TRUOC_ID'] = rid.id
            elif child.tag == 'Amount':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'RemainingAmount':
                res['SO_TIEN_CHUA_PHAN_BO'] = float(child.text)
            elif child.tag == 'AllocationAmount':
                res['SO_TIEN_PHAN_BO_TRONG_KY'] = float(child.text)
            
        return self.env['ir.model.data']._update(
            rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # phân bổ chi phí trả trước  chi tiết(phân bổ)
    def _import_GLVoucherDetailExpensesAllocation(self, tag):
        rec_model = 'tong.hop.phan.bo.chi.phi.tra.truoc.phan.bo'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['PHAN_BO_CHI_PHI_TRA_TRUOC_ID'] = rid.id
            
            
            elif child.tag == 'PrepaidExpensesID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_CP_TRA_TRUOC_ID'] = rid.id
            elif child.tag == 'AllocationObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_PHAN_BO_ID'] = rid.id
            
            elif child.tag == 'OrganizationUnitName':
                res['TEN_DOI_TUONG_PHAN_BO'] = child.text
            elif child.tag == 'AllocationRate':
                res['TY_LE'] = float(child.text)
            elif child.tag == 'AllocationAmount':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'TotalAllocationAmount':
                res['CHI_PHI_PHAN_BO'] = float(child.text)
            elif child.tag == 'CostAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id
            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id
            
        return self.env['ir.model.data']._update(
            rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)



    #Danh sách chi phí trả trước

    def _import_PrepaidExpenses(self, tag):
        rec_model = 'tong.hop.chi.phi.tra.truoc'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'PrepaidExpensesID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefDate':
                res['NGAY_GHI_NHAN'] = child.text
            elif child.tag == 'RefNo':
                res['SO_CHUNG_TU'] = child.text

            elif child.tag == 'PrepaidExpensesCode':
                res['MA_CHI_PHI_TRA_TRUOC'] = child.text
            elif child.tag == 'PrepaidExpensesName':
                res['TEN_CHI_PHI_TRA_TRUOC'] = child.text
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)

            elif child.tag == 'Amount':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'AllocationTime':
                res['SO_KY_PHAN_BO'] = int(child.text)
            elif child.tag == 'AllocationAmount':
                res['SO_TIEN_PB_HANG_KY'] = float(child.text)
            elif child.tag == 'AllocationAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CHO_PHAN_BO_ID'] = rid.id 
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id   
            elif child.tag == 'Inactive':
                res['NGUNG_PHAN_BO'] = False if child.text == 'false' else True     
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # Chi phí trả trước  chi tiết(Thiết lập phân bổ)
    def _import_PrepaidExpensesDetail(self, tag):
        rec_model = 'tong.hop.chi.phi.tra.truoc.thiet.lap.phan.bo'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'PrepaidExpensesDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'PrepaidExpensesID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_PHI_TRA_TRUOC_ID'] = rid.id
            
            elif child.tag == 'AllocationObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_PHAN_BO_ID'] = rid.id
            
            elif child.tag == 'AllocationObjectName':
                res['TEN_DOI_TUONG_PHAN_BO'] = child.text
            elif child.tag == 'AllocationRate':
                res['TY_LE_PB'] = float(child.text)
            
            elif child.tag == 'CostAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id
            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id
            
        return self.env['ir.model.data']._update(
            rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    