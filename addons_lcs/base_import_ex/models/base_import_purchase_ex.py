from odoo import api, fields, models, helper
import logging

_logger = logging.getLogger(__name__)


MODULE = 'base_import_ex'
class Import(models.TransientModel):
    _inherit = 'base_import_ex.import'

    # Chứng từ mua hàng hóa
    def _import_PUVoucher(self, tag):
        rec_model = 'purchase.document'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountObjectID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_DOI_TUONG'] = child.text
            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text
            
            elif child.tag == 'AccountObjectContactName':
                res['NGUOI_GIAO_HANG'] = child.text
            elif child.tag == 'IssueDate':
                res['NGAY_CAP_CMND'] = child.text
            elif child.tag == 'IssueBy':
                res['NOI_CAP_CMND'] = child.text
            elif child.tag == 'DocumentIncluded':
                res['KEM_THEO'] = child.text
            elif child.tag == 'CABAJournalMemo':
                res['LY_DO_CHI'] = child.text
            elif child.tag == 'IdentificationNumber':
                res['SO_CMND'] = child.text
            elif child.tag == 'Receiver':
                res['NGUOI_NHAN'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
           
            elif child.tag == 'CABARefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            
           


            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'PaymentTermID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DIEU_KHOAN_THANH_TOAN_ID'] = rid.id
            elif child.tag == 'CABADocumentIncluded':
                res['KEM_THEO_PC'] = child.text 
            elif child.tag == 'DueTime':
                res['SO_NGAY_DUOC_NO'] = child.text
            elif child.tag == 'DueDate':
                res['HAN_THANH_TOAN'] = child.text
               
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text

            elif child.tag == 'BankAccountID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['TK_CHI_ID'] = rid.id
                
            elif child.tag == 'BankName':
                res['CHI_NHANH_TK_CHI'] = child.text

            elif child.tag == 'AccountObjectBankAccount':
                rid=self.env['danh.muc.doi.tuong.chi.tiet'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NHAN_ID'] = rid.id   
                
            elif child.tag == 'AccountObjectBankName':
                res['CHI_NHANH_TK_NHAN'] = child.text
            elif child.tag == 'BranchID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
                
            elif child.tag == 'EmployeeID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHAN_VIEN_ID'] = rid.id
            elif child.tag == 'CurrencyID':
                rid=self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id   
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)


            elif child.tag == 'RefNoFinance':
                res['SO_PHIEU_NHAP'] = child.text
            
            elif child.tag == 'InvTemplateNo':
                rid =self.env['danh.muc.mau.so.hd'].search([('MAU_SO_HD', '=', child.text)], limit=1)
                if rid:
                    res['MAU_SO_HD_ID'] = rid.id

            elif child.tag == 'RefType':
                if child.text == '302':
                    res['LOAI_CHUNG_TU_MH'] = 'trong_nuoc_nhap_kho'
                    res['DA_THANH_TOAN'] = False
                   
                elif child.text == '312':
                    res['LOAI_CHUNG_TU_MH'] = 'trong_nuoc_khong_qua_kho'
                    res['DA_THANH_TOAN'] = False
                   
                elif child.text == '318':
                    res['LOAI_CHUNG_TU_MH'] = 'nhap_khau_nhap_kho'
                    res['DA_THANH_TOAN'] = False
                elif child.text == '324':
                    res['LOAI_CHUNG_TU_MH'] = 'nhap_khau_khong_qua_kho'
                    res['DA_THANH_TOAN'] = False

                elif child.text == '307':
                    res['LOAI_CHUNG_TU_MH'] = 'trong_nuoc_nhap_kho'
                    res['DA_THANH_TOAN'] = True
                    res['LOAI_THANH_TOAN'] = 'tien_mat'
                   
                elif child.text == '313':
                    res['LOAI_CHUNG_TU_MH'] = 'trong_nuoc_khong_qua_kho'
                    res['DA_THANH_TOAN'] = True
                    res['LOAI_THANH_TOAN'] = 'tien_mat'
                elif child.text == '319':
                    res['LOAI_CHUNG_TU_MH'] = 'nhap_khau_nhap_kho'
                    res['DA_THANH_TOAN'] = True
                    res['LOAI_THANH_TOAN'] = 'tien_mat'
                elif child.text == '325':
                    res['LOAI_CHUNG_TU_MH'] = 'nhap_khau_khong_qua_kho'
                    res['DA_THANH_TOAN'] = True
                    res['LOAI_THANH_TOAN'] = 'tien_mat'
                

                elif child.text == '308':
                    res['LOAI_CHUNG_TU_MH'] = 'trong_nuoc_nhap_kho'
                    res['DA_THANH_TOAN'] = True
                    res['LOAI_THANH_TOAN'] = 'uy_nhiem_chi'
                elif child.text == '314':
                    res['LOAI_CHUNG_TU_MH'] = 'trong_nuoc_khong_qua_kho'
                    res['DA_THANH_TOAN'] = True
                    res['LOAI_THANH_TOAN'] = 'uy_nhiem_chi'
                elif child.text == '320':
                    res['LOAI_CHUNG_TU_MH'] = 'nhap_khau_nhap_kho'
                    res['DA_THANH_TOAN'] = True
                    res['LOAI_THANH_TOAN'] = 'uy_nhiem_chi'
                elif child.text == '326':
                    res['LOAI_CHUNG_TU_MH'] = 'nhap_khau_khong_qua_kho'
                    res['DA_THANH_TOAN'] = True
                    res['LOAI_THANH_TOAN'] = 'uy_nhiem_chi'


                elif child.text == '309':
                    res['LOAI_CHUNG_TU_MH'] = 'trong_nuoc_nhap_kho'
                    res['DA_THANH_TOAN'] = True
                    res['LOAI_THANH_TOAN'] = 'sec_chuyen_khoan'
                elif child.text == '315':
                    res['LOAI_CHUNG_TU_MH'] = 'trong_nuoc_khong_qua_kho'
                    res['DA_THANH_TOAN'] = True
                    res['LOAI_THANH_TOAN'] = 'sec_chuyen_khoan'
                elif child.text == '321':
                    res['LOAI_CHUNG_TU_MH'] = 'nhap_khau_nhap_kho'
                    res['DA_THANH_TOAN'] = True
                    res['LOAI_THANH_TOAN'] = 'sec_chuyen_khoan'
                elif child.text == '327':
                    res['LOAI_CHUNG_TU_MH'] = 'nhap_khau_khong_qua_kho'
                    res['DA_THANH_TOAN'] = True
                    res['LOAI_THANH_TOAN'] = 'sec_chuyen_khoan'

                elif child.text == '310':
                    res['LOAI_CHUNG_TU_MH'] = 'trong_nuoc_nhap_kho'
                    res['DA_THANH_TOAN'] = True
                    res['LOAI_THANH_TOAN'] = 'sec_tien_mat'
                elif child.text == '316':
                    res['LOAI_CHUNG_TU_MH'] = 'trong_nuoc_khong_qua_kho'
                    res['DA_THANH_TOAN'] = True
                    res['LOAI_THANH_TOAN'] = 'sec_tien_mat'
                elif child.text == '322':
                    res['LOAI_CHUNG_TU_MH'] = 'nhap_khau_nhap_kho'
                    res['DA_THANH_TOAN'] = True
                    res['LOAI_THANH_TOAN'] = 'sec_tien_mat'
                elif child.text == '328':
                    res['LOAI_CHUNG_TU_MH'] = 'nhap_khau_khong_qua_kho'
                    res['DA_THANH_TOAN'] = True
                    res['LOAI_THANH_TOAN'] = 'sec_tien_mat'


                   
            elif child.tag == 'IncludeInvoice':
                res['LOAI_HOA_DON'] = child.text

            elif child.tag == 'AccountObjectIdentificationNumberOther':
                res['SO_CMND_KHAC'] = child.text
            
            elif child.tag == 'PUInvoiceRefID':
                res['HOA_DON_REF_ID'] = child.text

                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOA_DON_MUA_HANG_ID'] = rid.id
            elif child.tag == 'IsPULotVoucher':
                res['LA_PHIEU_MUA_HANG'] = True if child.text == 'true' else False
        if (res['DA_THANH_TOAN']):
            #xu lý thanh toán ngay
            if(res['LOAI_THANH_TOAN']=='uy_nhiem_chi'):
                res['SO_UY_NHIEM_CHI'] = res['SO_CHUNG_TU']
            elif (res['LOAI_THANH_TOAN'] == 'sec_chuyen_khoan'):
                res['SO_SEC_CHUYEN_KHOAN']= res['SO_CHUNG_TU']
            elif (res['LOAI_THANH_TOAN'] == 'sec_tien_mat'):
                res['SO_SEC_TIEN_MAT']= res['SO_CHUNG_TU']
            else:
                res['SO_PHIEU_CHI']= res['SO_CHUNG_TU']
        else:
            res['SO_CHUNG_TU_MUA_HANG']= res['SO_PHIEU_NHAP']
        # Khi import thì không tạo mới hóa đơn
        # res['TAO_TU_IMPORT'] = True
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Chứng từ mua hàng chi tiết (hàng tiền,thuế, thống kê)
    def _import_PUVoucherDetail(self, tag):
        rec_model = 'purchase.document.line'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['order_id'] = rid.id
                
            elif child.tag == 'InventoryItemID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id
                
            elif child.tag == 'Description':
                res['name'] = child.text
            elif child.tag == 'StockID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHO_ID'] = rid.id
            elif child.tag == 'DebitAccount':
                rid=self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id
            elif child.tag == 'CreditAccount':
                rid=self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id
            elif child.tag == 'UnitID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id
            elif child.tag == 'Amount':
                res['THANH_TIEN_QUY_DOI'] = float(child.text)
            elif child.tag == 'AmountOC':
                res['THANH_TIEN'] = float(child.text)
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'UnitPrice':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'DiscountRate':
                res['TY_LE_CK'] = float(child.text)
            elif child.tag == 'DiscountAmountOC':
                res['TIEN_CHIET_KHAU'] = float(child.text)

            elif child.tag == 'DiscountAmount':
                res['TIEN_CHIET_KHAU_QUY_DOI'] = float(child.text)


            elif child.tag == 'FreightAmount':
                res['CHI_PHI_MUA_HANG'] = float(child.text)

            elif child.tag == 'InwardAmount':
                res['GIA_TRI_NHAP_KHO'] = float(child.text)
            elif child.tag == 'VATDescription':
                res['DIEN_GIAI_THUE'] = child.text
            elif child.tag == 'VATAccount':
                rid=self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_THUE_GTGT_ID'] = rid.id
            elif child.tag == 'VATAmount':
                res['TIEN_THUE_GTGT_QUY_DOI'] = float(child.text)
            
            elif child.tag == 'VATAmountOC':
                res['TIEN_THUE_GTGT'] = float(child.text)
            elif child.tag == 'OrganizationUnitID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_ID'] = rid.id 



            elif child.tag == 'ImportChargeAmount':
                res['PHI_TRUOC_HAI_QUAN'] = float(child.text)
            elif child.tag == 'ImportTaxRatePrice':
                res['GIA_TINH_THUE_NK'] = float(child.text)
            elif child.tag == 'ImportTaxRate':
                res['THUE_NK'] = float(child.text)
            elif child.tag == 'ImportTaxAmountOC':
                res['TIEN_THUE_NK'] = float(child.text)


            elif child.tag == 'SpecialConsumeTaxRate':
                res['THUE_TTDB'] = float(child.text)
            elif child.tag == 'SpecialConsumeTaxAmountOC':
                res['TIEN_THUE_TTDB'] = float(child.text)
            elif child.tag == 'SpecialConsumeTaxAmount':
                res['TIEN_THUE_TTDB_QUY_DOI'] = float(child.text)
            elif child.tag == 'ImportTaxRate':
                res['THUE_NK'] = float(child.text)
            elif child.tag == 'ImportTaxAmount':
                res['TIEN_THUE_NK_QUY_DOI'] = float(child.text)


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
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id  

            elif child.tag == 'LotNo':
                res['SO_LO'] = child.text
            elif child.tag == 'ExpiryDate':
                res['HAN_SU_DUNG'] = child.text


            elif child.tag == 'DeductionDebitAccount':
                rid=self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_DU_THUE_GTGT_ID'] = rid.id
            elif child.tag == 'ImportTaxAccount':
                rid=self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_THUE_NK_ID'] = rid.id
            elif child.tag == 'SpecialConsumeTaxAccount':
                rid=self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_THUE_TTDB_ID'] = rid.id

            elif child.tag == 'VATRate':
                rid=self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:
                    res['THUE_GTGT_ID'] = rid.id   

           
            elif child.tag == 'PUContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_MUA_ID'] = rid.id
            elif child.tag == 'PUOrderRefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_MUA_HANG_ID'] = rid.id   
            elif child.tag == 'PurchasePurposeID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['NHOM_HHDV_ID'] = rid.id       
            elif child.tag == 'INProductionOrderRefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['LENH_SAN_XUAT_ID'] = rid.id 

            elif child.tag == 'ProductionID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['THANH_PHAM_ID'] = rid.id     
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id      
            
            elif child.tag == 'CashOutExchangeRateFinance':
                res['TY_GIA_XUAT_QUY'] = float(child.text)
            elif child.tag == 'CashOutAmountFinance':
                res['THANH_TIEN_SAU_TY_GIA_XUAT_QUY'] = float(child.text)
            elif child.tag == 'CashOutDiffAmountFinance':
                res['CHENH_LECH'] = float(child.text) 

            elif child.tag == 'CashOutDiffAccountNumberFinance':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search( [('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_XU_LY_CHENH_LECH'] = rid.id  
            
            elif child.tag == 'CashOutVATAmountFinance':
                res['TIEN_THUE_GTGT_THEO_TGXQ'] = float(child.text)
            elif child.tag == 'CashOutDiffVATAmountFinance':
                res['CHENH_LECH_TIEN_THUE_GTGT'] = float(child.text) 
            elif child.tag == 'TaxAccountObjectName':
                res['TEN_NCC'] = child.text
            elif child.tag == 'SortOrder':
                res['THU_TU_SAP_XEP_CHI_TIET'] = int(child.text)
            if child.tag == 'UnResonableCost':
                res['CHI_PHI_KHONG_HOP_LY'] = True if child.text == 'true' else False
            elif child.tag == 'PUOrderRefDetailID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_TIET_DON_MUA_HANG_ID'] = rid.id

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    
    # Chứng từ mua hàng chi tiết (CHI PHÍ )
    def _import_PUVoucherDetailCost(self, tag):
        rec_model = 'purchase.chi.phi'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['purchase_document_id'] = rid.id    
            
			# Todof: Trường CHUNG_TU_ID không còn tồn tại
            # elif child.tag == 'CostRefID':
                # rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                # if rid:
                    # res['CHUNG_TU_ID'] = rid.id    
            
            elif child.tag == 'RefDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_CHUNG_TU'] = child.text
            
            elif child.tag == 'AccountObjectID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id    
                
            elif child.tag == 'TotalFreightAmount':
                res['TONG_CHI_PHI'] = float(child.text)
            elif child.tag == 'Amount':
                res['SO_PHAN_BO_LAN_NAY'] = float(child.text)
            elif child.tag == 'AccumulatedAllocateAmount':
                res['LUY_KE_DA_PHAN_BO'] = float(child.text)
            
                        
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Mua hàng-chứng từ mua dịch vụ
    def _import_PUService(self, tag):
        rec_model = 'purchase.document'
        res = {'type':'dich_vu' }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            #nếu childtag==reftype
                #nếu childtex=='331'
                    #res['DA_THANH_TOAN']= True
                    #res['LOAI_THANH_TOAN']= 'tien_mat'
                #nếu childtex=='332'
                    #res['DA_THANH_TOAN']= True
                    #res['LOAI_THANH_TOAN']= 'uy_nhiem_chi'
                #nguoc lai
                    #res['DA_THANH_TOAN']= False
            
            elif child.tag == 'RefType':
                if child.text == '330':
                    res['DA_THANH_TOAN'] = False
                   
                elif child.text == '331':
                    res['LOAI_THANH_TOAN'] = 'tien_mat'
                    res['DA_THANH_TOAN'] = True
                elif child.text == '332':
                    res['LOAI_THANH_TOAN'] = 'uy_nhiem_chi'
                    res['DA_THANH_TOAN'] = True
                elif child.text == '333':
                    res['LOAI_THANH_TOAN'] = 'sec_chuyen_khoan'
                    res['DA_THANH_TOAN'] = True
                elif child.text == '334':
                    res['LOAI_THANH_TOAN'] = 'sec_tien_mat'
                    res['DA_THANH_TOAN'] = True

            elif child.tag == 'IncludeInvoice':
                res['LOAI_HOA_DON'] = child.text 
            
            elif child.tag == 'IsFreightService':
                res['LA_CHI_PHI_MUA_HANG'] = False if child.text == 'false' else True
            elif child.tag == 'AccountObjectID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id  
                
            elif child.tag == 'AccountObjectName':
                res['TEN_DOI_TUONG'] = child.text
            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text
            
            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
                # res['SO_PHIEU_CHI'] = child.text
                # res['SO_UY_NHIEM_CHI'] = child.text 
                # res['SO_SEC_TIEN_MAT'] = child.text
                # res['SO_SEC_CHUYEN_KHOAN'] = child.text
            
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI_CHUNG'] = child.text

            # elif child.tag == 'JournalMemo':
            #     res['NOI_DUNG_THANH_TOAN'] = child.text


            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text

            
            # elif child.tag == 'AccountObjectContactname':
            #     res['NGUOI_LINH_TIEN'] = child.text
            elif child.tag == 'AccountObjectContactname':
                res['NGUOI_NHAN'] = child.text
            elif child.tag == 'DocumentIncluded':
                res['KEM_THEO'] = child.text
            elif child.tag == 'AccountObjectBankAccount':
                rid=self.env['danh.muc.doi.tuong.chi.tiet'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NHAN_ID'] = rid.id 
            elif child.tag == 'AccountObjectBankName':
                res['CHI_NHANH_TK_NHAN'] = child.text  
            
            elif child.tag == 'InvTemplateNo':
                rid =self.env['danh.muc.mau.so.hd'].search([('MAU_SO_HD', '=', child.text)], limit=1)
                if rid:
                    res['MAU_SO_HD_ID'] = rid.id


            elif child.tag == 'IdentificationNumber':
                res['SO_CMND'] = child.text
            elif child.tag == 'IssueDate':
                res['NGAY_CAP_CMND'] = child.text  
            elif child.tag == 'IssueBy':
                res['NOI_CAP_CMND'] = child.text
            elif child.tag == 'BankAccountID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['TK_CHI_ID'] = rid.id 
            elif child.tag == 'BankName':
                res['CHI_NHANH_TK_CHI'] = child.text
            elif child.tag == 'BranchID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id 
            elif child.tag == 'EmployeeID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHAN_VIEN_ID'] = rid.id 
            elif child.tag == 'CurrencyID':
                rid=self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id 
                
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            


            elif child.tag == 'PaymentTermID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DIEU_KHOAN_THANH_TOAN_ID'] = rid.id
            elif child.tag == 'DueTime':
                res['SO_NGAY_DUOC_NO'] = child.text
            elif child.tag == 'DueDate':
                res['HAN_THANH_TOAN'] = child.text 

            elif child.tag == 'AccountObjectIdentificationNumberOther':
                res['SO_CMND_KHAC'] = child.text
            elif child.tag == 'AccountObjectAddressOther':
                res['DIA_CHI'] = child.text 

        if (res['DA_THANH_TOAN']):
            #xu lý thanh toán ngay
            if(res['LOAI_THANH_TOAN']=='uy_nhiem_chi'):
                res['SO_UY_NHIEM_CHI'] = res['SO_CHUNG_TU']
            elif (res['LOAI_THANH_TOAN'] == 'sec_chuyen_khoan'):
                res['SO_SEC_CHUYEN_KHOAN']= res['SO_CHUNG_TU']
            elif (res['LOAI_THANH_TOAN'] == 'sec_tien_mat'):
                res['SO_SEC_TIEN_MAT']= res['SO_CHUNG_TU']
            else:
                res['SO_PHIEU_CHI']= res['SO_CHUNG_TU']
        else:
            res['SO_CHUNG_TU_MUA_HANG']= res['SO_CHUNG_TU']
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #chứng từ mua dịch vụ chi tiết (hạch toán)
    def _import_PUServiceDetail(self, tag):
        rec_model = 'purchase.document.line'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['order_id'] = rid.id 
                
            elif child.tag == 'InventoryItemID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id 
                
            elif child.tag == 'Description':
                res['name'] = child.text
            elif child.tag == 'DebitAccount':
                rid=self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id 
                
            elif child.tag == 'CreditAccount':
                rid=self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id 
                
            elif child.tag == 'UnitID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id 
            elif child.tag == 'Amount':
                res['THANH_TIEN_QUY_DOI'] = float(child.text)
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'UnitPrice':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'AmountOC':
                res['THANH_TIEN'] = float(child.text)
            elif child.tag == 'VATDescription':
                res['DIEN_GIAI_THUE'] = child.text
            elif child.tag == 'VATRate':
                rid =self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:
                    res['THUE_GTGT_ID'] = rid.id
            elif child.tag == 'VATAmount':
                res['TIEN_THUE_GTGT_QUY_DOI'] = child.text
            elif child.tag == 'InvNo':
                res['SO_HOA_DON_DETAIL'] = child.text

            elif child.tag == 'VATAmountOC':
                res['TIEN_THUE_GTGT'] = child.text
            # elif child.tag == 'CashOutAmountFinance':
            #     res['DIEN_GIAI_THUE'] = child.text
            # elif child.tag == 'CashOutDiffAmountFinance':
            #     res['DIEN_GIAI_THUE'] = child.text
            # elif child.tag == 'CashOutDiffAccountNumberFinance':
            #     rid=self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
            #     if rid:
            #         res['TK_THUE_GTGT_ID'] = rid.id 

            elif child.tag == 'VATAccount':
                rid=self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_THUE_GTGT_ID'] = rid.id 
            elif child.tag == 'VATAmountOC':
                res['TIEN_THUE_GTGT'] = float(child.text)
            elif child.tag == 'OrganizationUnitID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_ID'] = rid.id 
            elif child.tag == 'TaxAccountObjectID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_NCC_ID'] = rid.id 
            elif child.tag == 'TaxAccountObjectName':
                res['TEN_NCC'] = child.text
            elif child.tag == 'TaxAccountObjectAddress':
                res['DIA_CHI_NCC'] = child.text
            elif child.tag == 'TaxAccountObjectTaxCode':
                res['MA_SO_THUE_NCC'] = child.text
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
            elif child.tag == 'PUContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_MUA_ID'] = rid.id
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
            # elif child.tag == 'OrderID':
            #     rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
            #     if rid:
            #         res['HOP_DONG_MUA_ID'] = rid.id
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id  
            
            elif child.tag == 'PurchasePurposeID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['NHOM_HHDV_ID'] = rid.id
            elif child.tag == 'InvDate':
                res['NGAY_HOA_DON'] = child.text
            elif child.tag == 'CashOutAmountFinance':
                res['THANH_TIEN_SAU_TY_GIA_XUAT_QUY'] = float(child.text) 
            elif child.tag == 'CashOutVATAmountFinance':
                res['TIEN_THUE_GTGT_THEO_TGXQ'] = float(child.text) 
            elif child.tag == 'SortOrder':
                res['THU_TU_SAP_XEP_CHI_TIET'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Mua hàng- trả lại hàng mua
    def _import_PUReturn(self, tag):
        rec_model = 'purchase.ex.tra.lai.hang.mua'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'


            elif child.tag == 'RefType':
                if child.text=='3030':
                    res['selection_chung_tu_mua_hang'] = 'giam_tru_cong_no'
                    res['TRA_LAI_HANG_TRONG_KHO'] = True
                elif child.text=='3031':
                    res['selection_chung_tu_mua_hang'] = 'thu_tien_mat'
                    res['TRA_LAI_HANG_TRONG_KHO'] = True
                elif child.text=='3033':
                    res['selection_chung_tu_mua_hang'] = 'thu_tien_mat'
                    res['TRA_LAI_HANG_TRONG_KHO'] = False
                elif child.text=='3032':
                    res['selection_chung_tu_mua_hang'] = 'giam_tru_cong_no'
                    res['TRA_LAI_HANG_TRONG_KHO'] = False

            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
                
            elif child.tag == 'AccountObjectName':
                res['TEN_NHA_CUNG_CAP'] = child.text
            elif child.tag == 'ReceiverAddress':
                res['DIA_CHI'] = child.text
            elif child.tag == 'Receiver':
                res['NGUOI_NHAN_HANG'] = child.text
            
            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'CARefNoFinance':
                res['SO_PHIEU_THU'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['LY_DO_XUAT'] = child.text
               
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
            elif child.tag == 'CurrencyID':
                res['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1).id
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            elif child.tag == 'Payer':
                res['NGUOI_NOP'] = child.text
            elif child.tag == 'CAJournalMemo':
                res['LY_DO_NOP'] = child.text
            elif child.tag == 'CADocumentIncluded':
                res['KEM_THEO_PT'] = child.text
            elif child.tag == 'OutDocumentIncluded':
                res['KEM_THEO'] = child.text
            elif child.tag == 'SAInvoiceRefID':
                res['HOA_DON_REF_ID'] = child.text
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOA_DON_ID'] = rid.id
            elif child.tag == 'PaymentMethod':
                if child.text == 'TM/CK':
                    res['HINH_THUC_TT'] = 'TM_CK'
                else:
                    res['HINH_THUC_TT'] = child.text
            elif child.tag == 'PayerAddress':
                res['DIA_CHI_NGUOI_NOP'] = child.text
            #trung ham compute_so_chung_tu
        if (res['TRA_LAI_HANG_TRONG_KHO']):
            res['SO_PHIEU_XUAT']=res['SO_CHUNG_TU']
        else:
            if(res['selection_chung_tu_mua_hang']=='thu_tien_mat'):
                res['SO_PHIEU_THU']=res['SO_PHIEU_THU']
            else:
                res['SO_CHUNG_TU_GIAM_TRU_CONG_NO']=res['SO_CHUNG_TU']

            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Chứng từ trả lại mua hàng chi tiết ()
    def _import_PUReturnDetail(self, tag):
        rec_model = 'purchase.ex.tra.lai.hang.mua.chi.tiet'
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
                    res['CHUNG_TU_TRA_LAI_HANG_MUA_ID'] = rid.id
                
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id
                
            elif child.tag == 'Description':
                res['TEN_HANG'] = child.text
            elif child.tag == 'CreditAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id
                
            elif child.tag == 'DebitAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id
                
            elif child.tag == 'UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id
                
            elif child.tag == 'Amount':
                res['THANH_TIEN_QUY_DOI'] = float(child.text) 
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'UnitPrice':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'AmountOC':
                res['THANH_TIEN'] = float(child.text)
            
            elif child.tag == 'StockID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHO_ID'] = rid.id
                
            elif child.tag == 'VATDescription':
                res['DIEN_GIAI_THUE'] = child.text
            elif child.tag == 'VATAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_THUE_GTGT_ID'] = rid.id
            elif child.tag == 'VATAmount':
                res['TIEN_THUE_GTGT_QUY_DOI'] = float(child.text)
            elif child.tag == 'VATAmountOC':
                res['TIEN_THUE_GTGT'] = float(child.text)



            elif child.tag == 'UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id
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
            # elif child.tag == 'OrderID':
            #     rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
            #     if rid:
            #         res['HOP_DONG_MUA'] = rid.id
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id 
            elif child.tag == 'LotNo':
                res['SO_LO'] = child.text
            elif child.tag == 'ExpiryDate':
                res['HAN_SU_DUNG'] = child.text 
            elif child.tag == 'VATRate':
                rid =self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:
                    res['PHAN_TRAM_THUE_GTGT_ID'] = rid.id
            elif child.tag == 'PurchasePurposeID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['NHOM_HHDV_MUA_VAO_ID'] = rid.id
            elif child.tag == 'PUContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_MUA_ID'] = rid.id
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
            elif child.tag == 'INProductionOrderRefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['LENH_SAN_XUAT_ID'] = rid.id
            
            elif child.tag == 'MainQuantity':
                res['SO_LUONG_DVT_CHINH'] = float(child.text)
            elif child.tag == 'MainUnitPrice':
                res['DON_GIA_DVT_CHINH'] = float(child.text)
            # elif child.tag == 'ProductionID':
            #     rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
            #     if rid:
            #         res['THANH_PHAM_ID'] = rid.id
            elif child.tag == 'SortOrder':
                res['THU_TU_SAP_XEP_CHI_TIET'] = int(child.text)
            elif child.tag == 'PUOrderRefDetailID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_TIET_DON_MUA_HANG_ID'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Mua hàng- giảm giá hàng mua
    def _import_PUDiscount(self, tag):
        rec_model = 'purchase.ex.giam.gia.hang.mua'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefType':
                if child.text=='3040':
                    res['selection_chung_tu_giam_gia_hang_mua'] = 'giam_tru_cong_no'
                    res['GIAM_GIA_TRI_HANG_NHAP_KHO'] = True
                elif child.text=='3041':
                    res['selection_chung_tu_giam_gia_hang_mua'] = 'tra_lai_tien_mat'
                    res['GIAM_GIA_TRI_HANG_NHAP_KHO'] = True
                elif child.text=='3042':
                    res['selection_chung_tu_giam_gia_hang_mua'] = 'giam_tru_cong_no'
                    res['GIAM_GIA_TRI_HANG_NHAP_KHO'] = False
                elif child.text=='3043':
                    res['selection_chung_tu_giam_gia_hang_mua'] = 'tra_lai_tien_mat'
                    res['GIAM_GIA_TRI_HANG_NHAP_KHO'] = False
            elif child.tag == 'AccountObjectID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_NHA_CUNG_CAP'] = child.text
            elif child.tag == 'PayerAddress':
                res['DIA_CHI'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            
            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text  
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'BranchID':
                res['CHI_NHANH_ID'] = self.env.ref('{}.{}'.format(MODULE,child.text), False).id
            elif child.tag == 'EmployeeID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHAN_VIEN_ID'] = rid.id
            elif child.tag == 'CurrencyID':
                rid =self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            elif child.tag == 'DocumentIncluded':
                res['KEM_THEO_CT_GOC'] = child.text
            # elif child.tag == 'IsValueDecrementFromStock':
            #     res['GIAM_GIA_TRI_HANG_NHAP_KHO'] = True if child.text == 'true' else False
            elif child.tag == 'Payer':
                res['NGUOI_NOP'] = child.text
            elif child.tag == 'PUInvoiceRefID':
                res['HOA_DON_REF_ID'] = child.text
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOA_DON_MUA_HANG_ID'] = rid.id
        
        if(res['selection_chung_tu_giam_gia_hang_mua']=='tra_lai_tien_mat'):
            res['SO_PHIEU_THU']=res['SO_CHUNG_TU']
        else:
            res['SO_CHUNG_TU_GIAM_TRU_CONG_NO']=res['SO_CHUNG_TU']
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #chứng từ giảm giá hàng mua chi tiết ()
    def _import_PUDiscountDetail(self, tag):
        rec_model = 'purchase.ex.giam.gia.hang.mua.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['GIAM_GIA_HANG_MUA_CHI_TIET_ID_ID'] = rid.id
                
            elif child.tag == 'InventoryItemID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id
            elif child.tag == 'Description':
                res['TEN_HANG'] = child.text
            elif child.tag == 'DebitAccount':
                rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id
            elif child.tag == 'CreditAccount':
                rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id
            elif child.tag == 'UnitID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id

            elif child.tag == 'TIEN_THUE_GTGT_QUY_DOI':
                res['TIEN_THUE_GTGT'] = float(child.text)
            elif child.tag == 'VATAmountOC':
                res['TIEN_THUE_GTGT'] = float(child.text)
            elif child.tag == 'AmountOC':
                res['THANH_TIEN'] = float(child.text)

            elif child.tag == 'Amount':
                res['THANH_TIEN_QUY_DOI'] = float(child.text)
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'UnitPrice':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'StockID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHO_ID'] = rid.id
            elif child.tag == 'VATDescription':
                res['DIEN_GIAI_THUE'] = child.text
            elif child.tag == 'VATAccount':
                rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_THUE_GTGT_ID'] = rid.id
            elif child.tag == 'VATRate':
                rid =self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:
                    res['PHAN_TRAM_THUE_GTGT_ID'] = rid.id
            elif child.tag == 'VATAmount':
                res['TIEN_THUE_GTGT_QUY_DOI'] = float(child.text)
            elif child.tag == 'LotNo':
                res['SO_LO'] = child.text
            elif child.tag == 'ExpiryDate':
                res['HAN_SU_DUNG'] = child.text
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
            elif child.tag == 'PUContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_MUA_ID'] = rid.id
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id   
            elif child.tag == 'PurchasePurposeID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['NHOM_HHDV_MUA_VAO_ID'] = rid.id
            elif child.tag == 'SortOrder':
                res['THU_TU_SAP_XEP_CHI_TIET'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Hóa đơn mua hàng hóa
    def _import_PUInvoice(self, tag):
        rec_model = 'purchase.ex.hoa.don.mua.hang'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id

            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
            elif child.tag == 'AccountObjectName':
                res['TEN_NHA_CUNG_CAP'] = child.text
            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text
            
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'InvTemplateNo':
                res['MAU_SO_HD_ID'] = self.env['danh.muc.mau.so.hd'].search([('MAU_SO_HD', '=', child.text)], limit=1).id 
            elif child.tag == 'InvDate':
                res['NGAY_HOA_DON'] = child.text  
            elif child.tag == 'InvSeries':
                res['KY_HIEU_HD'] = child.text
            elif child.tag == 'InvNo':
                res['SO_HOA_DON'] = child.text

            elif child.tag == 'AccountObjectTaxCode':
                res['MA_SO_THUE'] = child.text
            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text  
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'EmployeeID':
                rid= self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHAN_VIEN_ID']=rid.id
            
            elif child.tag == 'CurrencyID':
                res['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1).id
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            elif child.tag == 'DueDate':
                res['HAN_THANH_TOAN'] = child.text 
            elif child.tag == 'IncludeInvoice':
                res['NHAN_HOA_DON'] = True if child.text == 'true' else False
        
        # Tìm chứng từ gắn kèm hóa đơn. Nếu có, cập nhật trực tiếp vào chứng từ này
        for model in ('purchase.document', 'purchase.ex.giam.gia.hang.mua', 'sale.ex.tra.lai.hang.ban'):
            domains = [('HOA_DON_REF_ID', '=', rec_id)]
            if model == 'purchase.document':
                domains += [('LOAI_HOA_DON', '=', '1')]
            doc = self.env[model].search(domains, limit=1)
            if doc:
                # Chỉ lấy một số giá trị trong hóa đơn gắn kèm, các giá trị còn lại không đúng
                doc.write({
                    'MAU_SO_HD_ID': res.get('MAU_SO_HD_ID'),
                    'KY_HIEU_HD': res.get('KY_HIEU_HD'),
                    'SO_HOA_DON': res.get('SO_HOA_DON'),
                    'NGAY_HOA_DON': res.get('NGAY_HOA_DON'),
                    'MA_SO_THUE': res.get('MA_SO_THUE'),
                    'DIA_CHI': res.get('DIA_CHI'),
                })
                return doc
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # mua hàng-nhận hóa đơn mua hàng chi tiết ()
    def _import_PUInvoiceDetail(self, tag):
        rec_model = 'purchase.ex.hoa.don.mua.hang.chi.tiet'
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
                    res['HOA_DON_MUA_HANG_ID'] = rid.id
                
            elif child.tag == 'InventoryItemID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_HANG_ID']=rid.id
            elif child.tag == 'Description':
                res['TEN_HANG'] = child.text
            elif child.tag == 'DebitAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_THUE_ID'] = rid.id
                
            elif child.tag == 'CreditAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id
                
            
            elif child.tag == 'TurnoverAmountOC':
                res['GIA_TRI_HHDV_CHUA_THUE'] = float(child.text)
            elif child.tag == 'TurnoverAmount':
                res['GIA_TRI_HHDV_CHUA_THUE_QUY_DOI'] = float(child.text)
            elif child.tag == 'VATDescription':
                res['DIEN_GIAI_THUE'] = child.text
            elif child.tag == 'VATRate':
                rid = self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:
                    res['PHAN_TRAM_THUE_GTGT_ID'] = rid.id
                
            elif child.tag == 'PUVoucherRefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'VATAmountOC':
                res['TIEN_THUE_GTGT'] = float(child.text)
            elif child.tag == 'VATAmount':
                res['TIEN_THUE_GTGT_QUY_DOI'] = float(child.text)
            elif child.tag == 'PurchasePurposeID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['NHOM_HHDV_MUA_VAO_ID'] = rid.id
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id  
            
            elif child.tag == 'PUContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_MUA_ID'] = rid.id  
            elif child.tag == 'ProjectWorkID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CONG_TRINH_ID'] = rid.id  

            elif child.tag == 'PUVoucherRefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['SO_CHUNG_TU_ID'] = rid.id  
            elif child.tag == 'PUOrderRefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_MUA_HANG_ID'] = rid.id
            elif child.tag == 'PUVoucherRefDetailID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHUNG_TU_MUA_HANG_CHI_TIET_ID'] = rid.id      
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #Mua hàng-đơn mua hàng
    def _import_PUOrder(self, tag):
        rec_model = 'purchase.ex.don.mua.hang'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHA_CUNG_CAP_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_NHA_CUNG_CAP'] = child.text
            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'ReceiveAddress':
                res['DIA_DIEM_GIAO_HANG'] = child.text  
            elif child.tag == 'OtherTerm':
                res['DIEU_KHOAN_KHAC'] = child.text
            elif child.tag == 'Status':
                res['TINH_TRANG'] = child.text
            elif child.tag == 'AccountObjectTaxCode':
                res['MA_SO_THUE'] = child.text
            elif child.tag == 'RefNo':
                res['SO_DON_HANG'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_DON_HANG'] = child.text  
            elif child.tag == 'ReceiveDate':
                res['NGAY_GIAO_HANG'] = child.text
            elif child.tag == 'BranchID':
                rid= self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID']=rid.id
            elif child.tag == 'EmployeeID':
                rid= self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NV_MUA_HANG_ID']=rid.id
            elif child.tag == 'PaymentTermID':
                rid= self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DIEU_KHOAN_TT_ID']=rid.id
            elif child.tag == 'DueDay':
                res['SO_NGAY_DUOC_NO'] = int(child.text)
            elif child.tag == 'CurrencyID':
                rid = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # mua hàng đơn mua hàng chi tiết 
    def _import_PUOrderDetail(self, tag):
        rec_model = 'purchase.ex.don.mua.hang.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_MUA_HANG_CHI_TIET_ID'] = rid.id    
            elif child.tag == 'InventoryItemID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id    
            elif child.tag == 'Description':
                res['TEN_HANG'] = child.text
            elif child.tag == 'UnitID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id    
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'UnitPrice':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'QuantityReceipt':
                res['SO_LUONG_NHAN'] = float(child.text)
            

            elif child.tag == 'AmountOC':
                res['THANH_TIEN'] = float(child.text)
            elif child.tag == 'Amount':
                res['THANH_TIEN_QUY_DOI'] = float(child.text)
            elif child.tag == 'VATAmountOC':
                res['TIEN_THUE_GTGT'] = float(child.text)
            elif child.tag == 'VATAmount':
                res['TIEN_THUE_GTGT_QUY_DOI'] = float(child.text)
            
            elif child.tag == 'VATRate':
                rid = self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:
                    res['PHAN_TRAM_THUE_GTGT_ID'] = rid.id    
            elif child.tag == 'SortOrder':
                res['THU_TU_CAC_DONG_CHI_TIET'] = int(child.text) 
            elif child.tag == 'QuantityReceiptLastYear':
                res['SO_LUONG_NHAN_NAM_TRUOC'] = float(child.text)
            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #Mua hàng-hợp đồng mua
    def _import_PUContract(self, tag):
        rec_model = 'purchase.ex.hop.dong.mua.hang'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'PUContractID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHA_CUNG_CAP_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_NCC'] = child.text
            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text
            
            elif child.tag == 'DeliverAddress':
                res['DIA_CHI_GIAO'] = child.text  
            elif child.tag == 'OtherTerm':
                res['DIEU_KHOAN_KHAC'] = child.text
            elif child.tag == 'Status':
                res['TINH_TRANG'] = child.text
            elif child.tag == 'AccountObjectTaxCode':
                res['MA_SO_THUE'] = child.text
            elif child.tag == 'AccountObjectContactName':
                res['NGUOI_LIEN_HE'] = child.text
            elif child.tag == 'DueDate':
                res['HAN_THANH_TOAN'] = child.text  
            elif child.tag == 'DeliverDueDate':
                res['HAN_GIAO_HANG'] = child.text



            elif child.tag == 'ContractCode':
                res['SO_HOP_DONG'] = child.text
            elif child.tag == 'SignDate':
                res['NGAY_KY'] = child.text
            elif child.tag == 'Subject':
                res['TRICH_YEU'] = child.text  
            elif child.tag == 'PaymentTerm':
                res['DIEU_KHOAN_KHAC'] = child.text
            elif child.tag == 'BranchID':
                rid= self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID']=rid.id
            elif child.tag == 'EmployeeID':
                rid= self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NV_MUA_HANG_ID']=rid.id
            
            
            elif child.tag == 'CurrencyID':
                rid = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            elif child.tag == 'IsArisedBeforeUseSoftware':
                res['LA_HOP_DONG_PHAT_SINH_TRUOC_KHI_SU_DUNG_PHAN_MEM'] = True if child.text == 'true' else False
            elif child.tag == 'ExecutedAmountFinance':
                res['GIA_TRI_DA_THUC_HIEN'] = float(child.text)
            elif child.tag == 'PaidAmountFinance':
                res['SO_DA_TRA'] = float(child.text)
            

            elif child.tag == 'AmountOC':
                res['GIA_TRI_HOP_DONG'] = float(child.text)
            elif child.tag == 'Amount':
                res['GT_HOP_DONG_QUY_DOI'] = float(child.text)
            elif child.tag == 'CloseAmountOC':
                res['GT_THANH_LY_QUY_DOI'] = float(child.text)
            elif child.tag == 'CloseAmount':
                res['SO_DA_TRA'] = float(child.text)
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False) 

    # mua hàng hợp đồng mua chi tiết 
    def _import_PUContractDetailInventoryItem(self, tag):
        rec_model = 'purchase.ex.hop.dong.mua.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'PUContractID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_MUA_CHI_TIET_ID'] = rid.id    
            elif child.tag == 'InventoryItemID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id    
            elif child.tag == 'Description':
                res['TEN_HANG'] = child.text
            elif child.tag == 'UnitID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id    
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'UnitPrice':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'AmountOC':
                res['THANH_TIEN'] = float(child.text)
            elif child.tag == 'Amount':
                res['THANH_TIEN_QUY_DOI'] = float(child.text)
            elif child.tag == 'VATAmountOC':
                res['TIEN_THUE_GTGT'] = float(child.text)
            elif child.tag == 'VATAmount':
                res['TIEN_THUE_GTGT_QUY_DOI'] = float(child.text)
            elif child.tag == 'DiscountAmountOC':
                res['TIEN_CHIET_KHAU'] = float(child.text)
            elif child.tag == 'DiscountAmount':
                res['TIEN_CHIET_KHAU_QUY_DOI'] = float(child.text)

            elif child.tag == 'TotalAmountOC':
                res['TONG_TIEN_THANH_TOAN'] = float(child.text)
            elif child.tag == 'TotalAmount':
                res['TONG_TIEN_THANH_TOAN_QUY_DOI'] = float(child.text)
            elif child.tag == 'VATRate':
                rid = self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:
                    res['PHAN_TRAM_THUE_GTGT_ID'] = rid.id  
            elif child.tag == 'DiscountRate':
                res['TY_LE_CK'] = float(child.text)          
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)  

    # Nhóm HHDV mua vào
    def _import_PurchasePurpose(self, tag):
        rec_model = 'danh.muc.nhom.hhdv'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'PurchasePurposeID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
           
            elif child.tag == 'PurchasePurposeCode':
                res['MA_NHOM_HHDV'] = child.text
            elif child.tag == 'PurchasePurposeName':
                res['TEN_NHOM_HHDV'] = child.text
           
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # Khoảng thời gian nợ
    def _import_PUDebtPeriod(self, tag):
        rec_model = 'purchase.ex.khoang.thoi.gian.theo.doi.no'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'DebtPeriodID':
                rec_id = child.text
                      
            elif child.tag == 'DebtPeriodName':
                res['TEN_KHOANG_THOI_GIAN_NO'] = child.text
            elif child.tag == 'DebtPeriodType':
                res['LOAI_KHOANG_THOI_GIAN_NO'] = int(child.text)
            elif child.tag == 'FromDay':
                res['TU_NGAY'] = int(child.text)
            elif child.tag == 'ToDay':
                res['DEN_NGAY'] = int(child.text)
            elif child.tag == 'SortOrder':
                res['SAP_XEP'] = int(child.text)
            elif child.tag == 'ReportID':
                res['MA_BAO_CAO'] = child.text
           
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
