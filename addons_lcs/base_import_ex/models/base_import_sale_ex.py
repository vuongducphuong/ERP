from odoo import api, fields, models, helper

MODULE = 'base_import_ex'
class Import(models.TransientModel):
    _inherit = 'base_import_ex.import'

    # Chứng từ bán hàng 
    def _import_SAVoucher(self, tag):
        rec_model = 'sale.document'
        res = { }
        rec_id = False
        res['HAN_THANH_TOAN'] = False
        res['DIEN_GIAI'] = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_KHACH_HANG'] = child.text
            elif child.tag == 'InvNo':
                res['SO_HOA_DON'] = child.text
            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text
            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'Payer':
                res['NGUOI_LIEN_HE'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'AccountObjectTaxCode':
                res['MA_SO_THUE'] = child.text
            elif child.tag == 'SupplierID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_GIAO_DAI_LY_ID'] = rid.id
            elif child.tag == 'SupplierName':
                res['TEN_DON_VI'] = child.text
            elif child.tag == 'PaymentTermID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DIEU_KHOAN_TT_ID'] = rid.id
            elif child.tag == 'DueDay':
                res['SO_NGAY_DUOC_NO'] = int(child.text)
            elif child.tag == 'DueDate':
                res['HAN_THANH_TOAN'] = child.text
            elif child.tag == 'SupplierName':
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
                rid = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            elif child.tag == 'DocumentIncluded':
                res['KEM_THEO_CHUNG_TU_GOC'] = child.text
            
            elif child.tag == 'BankAccountID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NOP_VAO_TK_ID'] = rid.id
            elif child.tag == 'BankName':
                res['TEN_TK'] = child.text

            elif child.tag == 'RefType':
                if child.text == '3530':
                    res['LOAI_NGHIEP_VU'] = 'TRONG_NUOC'
                    res['THU_TIEN_NGAY'] = False
                    
                elif child.text == '3534':
                    res['LOAI_NGHIEP_VU'] = 'DAI_LY'
                    res['THU_TIEN_NGAY'] = False
                
                elif child.text == '3532':
                    res['LOAI_NGHIEP_VU'] = 'XUAT_KHAU'
                    res['THU_TIEN_NGAY'] = False
                    
                elif child.text == '3536':
                    res['LOAI_NGHIEP_VU'] = 'UY_THAC'
                    res['THU_TIEN_NGAY'] = False
                
                elif child.text == '3531':
                    res['LOAI_NGHIEP_VU'] = 'TRONG_NUOC'
                    res['THU_TIEN_NGAY'] = True
                    res['LOAI_THANH_TOAN'] = 'TIEN_MAT'
                elif child.text == '3537':
                    res['LOAI_NGHIEP_VU'] = 'TRONG_NUOC'
                    res['THU_TIEN_NGAY'] = True
                    res['LOAI_THANH_TOAN'] = 'CHUYEN_KHOAN'
                elif child.text == '3535':
                    res['LOAI_NGHIEP_VU'] = 'DAI_LY'
                    res['THU_TIEN_NGAY'] = True
                    res['LOAI_THANH_TOAN'] = 'TIEN_MAT'
                elif child.text == '3538':
                    res['LOAI_NGHIEP_VU'] = 'DAI_LY'
                    res['THU_TIEN_NGAY'] = True
                    res['LOAI_THANH_TOAN'] = 'CHUYEN_KHOAN'

            elif child.tag == 'IncludeInvoice':
                res['LAP_KEM_HOA_DON'] = True if child.text == 'true' else False
           
            elif child.tag == 'IsInvoiceExported':
                res['DA_LAP_HOA_DON'] = True if child.text == 'true' else False
            elif child.tag == 'IsSaleWithOutward':
                res['KIEM_PHIEU_NHAP_XUAT_KHO'] = True if child.text == 'true' else False
            
            # Updated 2019-07-19 by anhtuan: Bổ sung thông tin ngày hóa đơn
            elif child.tag == 'InvDate':
                res['NGAY_HOA_DON'] = child.text
        #quanhm: trùng code với hàm _compute_SO_CHUNG_TU ở chứng từ bán hàng
        if(res["THU_TIEN_NGAY"]):
            #xu li phieu thu
            if (res["LOAI_THANH_TOAN"]=='TIEN_MAT'):
                res["SO_CHUNG_TU_PHIEU_THU_TIEN_MAT"] = res["SO_CHUNG_TU"]
            else:
                res["SO_CHUNG_TU_PHIEU_THU_CHUYEN_KHOAN"] = res["SO_CHUNG_TU"]
        else:
            res["SO_CHUNG_TU_GHI_NO"] = res["SO_CHUNG_TU"]
        # res['TAO_TU_IMPORT'] = True
        
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Chứng từ bán hàng chi tiết (hàng tiền,thuế,thống kê)
    def _import_SAVoucherDetail(self, tag):
        rec_model = 'sale.document.line'
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
                    res['SALE_DOCUMENT_ID'] = rid.id 

            elif child.tag == 'SAInvoiceRefID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOA_DON_ID'] = rid.id 


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
            elif child.tag == 'AmountOC':
                res['THANH_TIEN'] = float(child.text)   
            elif child.tag == 'Amount':
                res['THANH_TIEN_QUY_DOI'] = float(child.text)
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'UnitPrice':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'DiscountRate':
                res['TY_LE_CK'] = float(child.text)
            elif child.tag == 'DiscountAmountOC':
                res['TIEN_CHIET_KHAU'] = float(child.text)

            elif child.tag == 'VATRate':
                rid =self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:
                    res['THUE_GTGT_ID'] = rid.id 
            elif child.tag == 'VATAmountOC':
                res['TIEN_THUE_GTGT'] = float(child.text)
            elif child.tag == 'VATAmount':
                res['TIEN_THUE_GTGT_QUY_DOI'] = float(child.text)
            
            elif child.tag == 'ExportTaxAccount':
                rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_THUE_XK_ID'] = rid.id 
            elif child.tag == 'ExportTaxRate':
                 res['THUE_XUAT_KHAU'] = float(child.text)
            elif child.tag == 'FOBAmount':
                res['GIA_TINH_THUE_XK'] = float(child.text)
            elif child.tag == 'ExportTaxAmount':
                res['TIEN_THUE_XUAT_KHAU'] = float(child.text)
            elif child.tag == 'DiscountAmount':
                res['TIEN_CK_QUY_DOI'] = float(child.text)
            elif child.tag == 'VATDescription':
                res['DIEN_GIAI_THUE'] = child.text
            elif child.tag == 'VATAccount':
                rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_THUE_GTGT_ID'] = rid.id 
            
            elif child.tag == 'ListItemID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id 
            elif child.tag == 'ContractID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id 
            elif child.tag == 'ProjectWorkID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CONG_TRINH_ID'] = rid.id 
            elif child.tag == 'OrganizationUnitID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_ID'] = rid.id 
            elif child.tag == 'JobID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_THCP_ID'] = rid.id   
            elif child.tag == 'OrderID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
            elif child.tag == 'SAOrderRefDetailID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_CHI_TIET_ID'] = rid.id
            elif child.tag == 'DiscountAccount':
                res['TK_CHIET_KHAU_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id 
            elif child.tag == 'IsPromotion':
                res['LA_HANG_KHUYEN_MAI'] = True if child.text == 'true' else False
            elif child.tag == 'SAOrderRefDetailID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_CHI_TIET_ID'] = rid.id
            elif child.tag == 'InvTemplateNo':
                rid =self.env['danh.muc.mau.so.hd'].search([('MAU_SO_HD', '=', child.text)], limit=1)
                if rid:
                    res['MAU_SO_HD_ID'] = rid.id
            elif child.tag == 'SortOrder':
                res['THU_TU_SAP_XEP_CHI_TIET'] = int(child.text)
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Chứng từ trả lại hàng bán
    def _import_SAReturn(self, tag):
        rec_model = 'sale.ex.tra.lai.hang.ban'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            
            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'RefType':
                if child.text == '3540':
                    res['selection_chung_tu_ban_hang'] = 'giam_tru_cong_no'
                    res['CHUNG_TU_HANG_BAN_BI_TRA_LAI'] = 'BAN_HANG_HOA_DICH_VU'
                elif child.text == '3542':
                    res['selection_chung_tu_ban_hang'] = 'giam_tru_cong_no'
                    res['CHUNG_TU_HANG_BAN_BI_TRA_LAI'] = 'BAN_HANG_DAI_LY_BAN_DUNG_GIA'
                elif child.text == '3544':
                    res['selection_chung_tu_ban_hang'] = 'giam_tru_cong_no'
                    res['CHUNG_TU_HANG_BAN_BI_TRA_LAI'] = 'BAN_HANG_UY_THAC_XUAT_KHAU'
                elif child.text == '3541':
                    res['selection_chung_tu_ban_hang'] = 'tra_lai_tien_mat'
                    res['CHUNG_TU_HANG_BAN_BI_TRA_LAI'] = 'BAN_HANG_HOA_DICH_VU'
                elif child.text == '3543':
                    res['selection_chung_tu_ban_hang'] = 'tra_lai_tien_mat'
                    res['CHUNG_TU_HANG_BAN_BI_TRA_LAI'] = 'BAN_HANG_DAI_LY_BAN_DUNG_GIA'
                else:
                    res['selection_chung_tu_ban_hang'] = 'tra_lai_tien_mat'
                    res['CHUNG_TU_HANG_BAN_BI_TRA_LAI'] = 'BAN_HANG_UY_THAC_XUAT_KHAU'


            elif child.tag == 'IsReturnWithInward':
                res['KIEM_TRA_PHIEU_NHAP_KHO'] = False if child.text == 'false' else True
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_KHACH_HANG'] = child.text

            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text
            elif child.tag == 'Receiver':
                res['NGUOI_NHAN'] = child.text

            elif child.tag == 'ContactName':
                res['NGUOI_GIAO_HANG'] = child.text
            elif child.tag == 'DocumentIncluded':
                res['KEM_THEO'] = child.text
            
            # elif child.tag == 'DocumentIncluded':
            #     res['KEM_THEO_PN'] = child.text


                
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
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
                rid = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            elif child.tag == 'SupplierID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_GIAO_DAI_LY_ID'] = rid.id 
            elif child.tag == 'SupplierName':
                res['TEN_DON_VI_GIAO_DAI_LY'] = child.text
            elif child.tag == 'PUInvoiceRefID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOA_DON_MUA_HANG_ID'] = rid.id 
                res['HOA_DON_REF_ID'] = child.text
        
        #trùng với hàm compute_so_chung_tu
        if(res['selection_chung_tu_ban_hang']=='tra_lai_tien_mat'):
            res['SO_CHUNG_TU_PHIEU_CHI']=res['SO_CHUNG_TU']
        else:
            res['SO_CHUNG_TU_GIAM_TRU_CONG_NO']=res['SO_CHUNG_TU']

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Chứng từ trả lại bán hàng chi tiết (hàng tiền,thuế,thống kê)
    def _import_SAReturnDetail(self, tag):
        rec_model = 'sale.ex.tra.lai.hang.ban.chi.tiet'
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
                    res['TRA_LAI_HANG_BAN_ID'] =rid.id
            elif child.tag == 'InventoryItemID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id 
            elif child.tag == 'Description':
                res['TEN_HANG'] = child.text
            elif child.tag == 'DebitAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_TRA_LAI_ID'] =rid.id
                
            elif child.tag == 'CreditAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] =rid.id
                
            elif child.tag == 'UnitID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id 
            elif child.tag == 'Amount':
                res['THANH_TIEN_QUY_DOI'] = float(child.text)
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'UnitPrice':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'DiscountRate':
                res['TY_LE_CK_PHAN_TRAM'] = float(child.text)
            elif child.tag == 'DiscountAmountOC':
                res['TIEN_CHIET_KHAU'] = float(child.text)
            elif child.tag == 'AmountOC':
                res['THANH_TIEN'] = float(child.text)
            elif child.tag == 'DiscountAmount':
                res['TIEN_CHIET_KHAU_QUY_DOI'] = float(child.text)
            elif child.tag == 'DiscountAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CHIET_KHAU'] =rid.id
                
            elif child.tag == 'VATDescription':
                res['DIEN_GIAI_THUE'] = child.text
            elif child.tag == 'VATAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_THUE_GTGT_ID'] =rid.id
                
            elif child.tag == 'VATAmountOC':
                res['TIEN_THUE_GTGT'] = float(child.text)
            elif child.tag == 'VATAmount':
                res['TIEN_THUE_GTGT_QUY_DOI'] = float(child.text)

            elif child.tag == 'ListItemID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE'] = rid.id 
            elif child.tag == 'ContractID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id 
            elif child.tag == 'ProjectWorkID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CONG_TRINH_ID'] = rid.id 
            elif child.tag == 'OrganizationUnitID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_ID'] = rid.id 
            elif child.tag == 'JobID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_THCP_ID'] = rid.id  

            elif child.tag == 'VATRate':
                rid =self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:
                    res['PHAN_TRAM_THUE_GTGT_ID'] = rid.id  
            
            elif child.tag == 'PurchasePurposeID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHOM_HHDV_MUA_VAO_ID'] = rid.id  
            elif child.tag == 'OrderID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id

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
            
            elif child.tag == 'SAVoucherRefID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['SO_CHUNG_TU_ID'] = rid.id 
            elif child.tag == 'IsPromotion':
                res['LA_HANG_KHUYEN_MAI'] = True if child.text == 'true' else False
            elif child.tag == 'SAOrderRefDetailID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_CHI_TIET_ID'] = rid.id
            elif child.tag == 'SortOrder':
                res['THU_TU_SAP_XEP_CHI_TIET'] = int(child.text)
            elif child.tag == 'CashOutDiffVATAmountFinance':
                res['CHENH_LECH_TIEN_THUE_GTGT'] = float(child.text)
            elif child.tag == 'CashOutVATAmountFinance':
                res['TIEN_THUE_GTGT_QUY_DOI_THEO_TGXQ'] = float(child.text) 
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Hóa đơn bán hàng
    def _import_SAInvoice(self, tag):
        rec_model = 'sale.ex.hoa.don.ban.hang'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'

            elif child.tag == 'RefType':
                if child.text == '3560':
                    res['HOA_DON'] = 'BAN_HANG_HOA_DICH_VU_TRONG_NUOC'
                elif child.text == '3561':
                    res['HOA_DON'] = 'BAN_HANG_XUAT_KHAU'
                elif child.text == '3562':
                    res['HOA_DON'] = 'BAN_HANG_DAI_LY_BAN_DUNG_GIA'
                else:
                    res['HOA_DON'] = 'BAN_HANG_UY_THAC_XUAT_KHAU'


            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_KHACH_HANG'] = child.text
            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text
            elif child.tag == 'AccountObjectTaxCode':
                res['MA_SO_THUE'] = child.text


            elif child.tag == 'AccountObjectBankAccount':
                rid =self.env['danh.muc.doi.tuong.chi.tiet'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['partner_bank_id'] = rid.id

            elif child.tag == 'PaymentMethod':
                res['HINH_THUC_TT'] = helper.Obj.convert_to_key(child.text)
            elif child.tag == 'Buyer':
                res['NGUOI_MUA_HANG'] = child.text

            # elif child.tag == 'InvTemplateNo':
            #     res['MAU_SO_HD_ID'] = child.text

            elif child.tag == 'InvTemplateNo':
                rid =self.env['danh.muc.mau.so.hd'].search([('MAU_SO_HD', '=', child.text)], limit=1)
                if rid:
                    res['MAU_SO_HD_ID'] = rid.id

            elif child.tag == 'InvSeries':
                res['KY_HIEU_HD'] = child.text
            elif child.tag == 'InvNo':
                res['SO_HOA_DON'] = child.text
            elif child.tag == 'InvDate':
                res['NGAY_HOA_DON'] = child.text

            elif child.tag == 'IsAttachList':
                res['IN_KEM_BANG_KE'] = True if child.text == 'true' else False
            elif child.tag == 'IsPosted':
                res['DA_HACH_TOAN'] = True if child.text == 'true' else False
            elif child.tag == 'ListNo':
                res['SO'] = child.text
            elif child.tag == 'ListDate':
                res['NGAY'] = child.text
            elif child.tag == 'CommonInventoryName':
                res['TEN_MAT_HANG_CHUNG'] = child.text
            elif child.tag == 'ContractCode':
                res['SO_HOP_DONG'] = child.text
            elif child.tag == 'PlaceOfDelivery':
                res['DIA_DIEM_GIAO_HANG'] = child.text
            elif child.tag == 'PlaceOfReceipt':
                res['DIA_DIEM_NHAN_HANG'] = child.text
            elif child.tag == 'ContainerNo':
                res['SO_CONTAINER'] = child.text
            elif child.tag == 'TransportName':
                res['DV_VAN_CHUYEN'] = child.text
            elif child.tag == 'ContractDate':
                res['NGAY_HOP_DONG'] = child.text
            elif child.tag == 'BillOfLadingNo':
                res['SO_VAN_DON'] = child.text
            elif child.tag == 'IncludeInvoice':
                res['LAP_KEM_HOA_DON'] = True if child.text == 'true' else False

            elif child.tag == 'BranchID':
                rid= self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID']=rid.id
            elif child.tag == 'EmployeeID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHAN_VIEN_ID'] = rid.id
                
            elif child.tag == 'CurrencyID':
                rid=self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            elif child.tag == 'AdjustRefType':
                res['LOAI_CHUNG_TU_DIEU_CHINH'] = int(child.text)
            
        
        # Chứng từ bán hàng sẽ không có thông tin của hóa đơn gắn kèm
        for model in ('purchase.ex.tra.lai.hang.mua','sale.ex.giam.gia.hang.ban',):#, 'sale.document'):
            doc = self.env[model].search([('HOA_DON_REF_ID', '=', rec_id)], limit=1)
            if doc:
                data = {
                    'MAU_SO_HD_ID': res.get('MAU_SO_HD_ID'),
                    'KY_HIEU_HD': res.get('KY_HIEU_HD'),
                    'SO_HOA_DON': res.get('SO_HOA_DON'),
                    'NGAY_HOA_DON': res.get('NGAY_HOA_DON'),
                    'MA_SO_THUE': res.get('MA_SO_THUE'),
                    'DIA_CHI': res.get('DIA_CHI'),
                }
                if model == 'purchase.ex.tra.lai.hang.mua' and res.get('HINH_THUC_TT'):
                    data['HINH_THUC_TT'] = 'TM_CK' if res.get('HINH_THUC_TT') == 'TM/CK' else res.get('HINH_THUC_TT')
                
                doc.write(data)
                return doc
        # if res.get('HINH_THUC_TT') == 'TM_CK':
        #     res['HINH_THUC_TT'] = 'TM/CK'
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Hóa đơn bán hàng chi tiết 
    def _import_SAInvoiceDetail(self, tag):
        rec_model = 'sale.ex.chi.tiet.hoa.don.ban.hang'
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
                    res['HOA_DON_ID_ID'] = rid.id 
                
            elif child.tag == 'InventoryItemID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id 
            elif child.tag == 'Description':
                res['TEN_HANG'] = child.text
            
            elif child.tag == 'UnitID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
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
            elif child.tag == 'DiscountAmountOC':
                res['TIEN_CHIET_KHAU'] = float(child.text)
            elif child.tag == 'DiscountRate':
                res['TY_LE_CK'] = float(child.text)
            elif child.tag == 'DiscountAmount':
                res['TIEN_CHIET_KHAU_QUY_DOI'] = float(child.text)
            elif child.tag == 'VATRate':
                rid =self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:
                    res['THUE_GTGT'] = rid.id 
            elif child.tag == 'VATAmountOC':
                res['TIEN_THUE_GTGT'] = float(child.text)
            elif child.tag == 'VATAmount':
                res['TIEN_THUE_GTGT_QUY_DOI'] = float(child.text)
            elif child.tag == 'IsPromotion':
                res['LA_HANG_KHUYEN_MAI'] = True if child.text == 'true' else False
            elif child.tag == 'VATAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_THUE_GTGT_ID'] =rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Giảm giá hàng bán 
    def _import_SADiscount(self, tag):
        rec_model = 'sale.ex.giam.gia.hang.ban'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'


            elif child.tag == 'RefType':
                if child.text == '3550':
                    res['selection_chung_tu_giam_gia_hang_ban'] = 'giam_tru_cong_no'
                    res['CHUNG_TU_GIAM_GIA_HANG_BAN'] = 'BAN_HANG_HOA_DICH_VU'
                elif child.text == '3552':
                    res['selection_chung_tu_giam_gia_hang_ban'] = 'giam_tru_cong_no'
                    res['CHUNG_TU_GIAM_GIA_HANG_BAN'] = 'BAN_HANG_DAI_LY_BAN_DUNG_GIA'
                elif child.text == '3554':
                    res['selection_chung_tu_giam_gia_hang_ban'] = 'giam_tru_cong_no'
                    res['CHUNG_TU_GIAM_GIA_HANG_BAN'] = 'BAN_HANG_UY_THAC_XUAT_KHAU'
                elif child.text == '3551':
                    res['selection_chung_tu_giam_gia_hang_ban'] = 'tra_lai_tien_mat'
                    res['CHUNG_TU_GIAM_GIA_HANG_BAN'] = 'BAN_HANG_HOA_DICH_VU'
                elif child.text == '3553':
                    res['selection_chung_tu_giam_gia_hang_ban'] = 'tra_lai_tien_mat'
                    res['CHUNG_TU_GIAM_GIA_HANG_BAN'] = 'BAN_HANG_DAI_LY_BAN_DUNG_GIA'
                else:
                    res['selection_chung_tu_giam_gia_hang_ban'] = 'tra_lai_tien_mat'
                    res['CHUNG_TU_GIAM_GIA_HANG_BAN'] = 'BAN_HANG_UY_THAC_XUAT_KHAU'


            elif child.tag == 'AccountObjectID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id 
            elif child.tag == 'AccountObjectName':
                res['TEN_KHACH_HANG'] = child.text
            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text
            
            elif child.tag == 'Receiver':
                res['NGUOI_NHAN'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text  
            elif child.tag == 'DocumentIncluded':
                res['KEM_THEO_CT_GOC'] = child.text


            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            # elif child.tag == 'RefNoFinance':
            #     res['SO_PHIEU_CHI'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text  
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'BranchID':
                rid= self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID']=rid.id
            elif child.tag == 'EmployeeID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHAN_VIEN_ID'] = rid.id 
                
            elif child.tag == 'CurrencyID':
                rid=self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
                
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)

            elif child.tag == 'SupplierID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_UY_THAC_ID'] = rid.id 
                
            elif child.tag == 'SupplierName':
                res['TEN_DON_VI_UY_THAC'] = child.text
            elif child.tag == 'SAInvoiceRefID':
                res['HOA_DON_REF_ID'] = child.text
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOA_DON_BAN_HANG_ID'] =rid.id
         #trùng với hàm compute_so_chung_tu
        if(res['selection_chung_tu_giam_gia_hang_ban']=='tra_lai_tien_mat'):
            res['SO_PHIEU_CHI']=res['SO_CHUNG_TU']
        else:
            res['SO_CHUNG_TU_GIAM_TRU_CONG_NO']=res['SO_CHUNG_TU']
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # bán hàng giảm giá hàng bán chi tiết ()
    def _import_SADiscountDetail(self, tag):
        rec_model = 'sale.ex.chi.tiet.giam.gia.hang.ban'
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
                    res['GIAM_GIA_HANG_BAN_ID'] = rid.id 
                
            elif child.tag == 'InventoryItemID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id 
            elif child.tag == 'Description':
                res['TEN_HANG'] = child.text
            
            elif child.tag == 'DebitAccount':
                rid= self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id
            elif child.tag == 'CreditAccount':
                rid= self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id
            

            elif child.tag == 'UnitID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id 
            elif child.tag == 'AmountOC':
                res['THANH_TIEN'] = float(child.text)
            elif child.tag == 'Amount':
                res['THANH_TIEN_QUY_DOI'] = float(child.text)
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'UnitPrice':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'DiscountRate':
                res['TY_LE_CHIET_KHAU_PHAN_TRAM'] = float(child.text)
            elif child.tag == 'DiscountAmountOC':
                res['TIEN_CHIET_KHAU'] = float(child.text)
            elif child.tag == 'VATDescription':
                res['DIEN_GIAI_THUE'] = child.text
            elif child.tag == 'DiscountAccount':
                rid= self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CHIET_KHAU_ID'] = rid.id
            elif child.tag == 'DiscountRate':
                res['TY_LE_CHIET_KHAU_PHAN_TRAM'] = float(child.text)
            elif child.tag == 'VATRate':
                rid =self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:
                    res['PHAN_TRAM_THUE_GTGT_ID'] = rid.id 
                
            elif child.tag == 'VATAmountOC':
                res['TIEN_THUE_GTGT'] = float(child.text)
            elif child.tag == 'VATAccount':
                rid= self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_THUE_GTGT_ID'] = rid.id

            elif child.tag == 'DiscountAmount':
                res['TIEN_CHIET_KHAU_QUY_DOI'] = float(child.text)
            
            elif child.tag == 'VATAmountOC':
                res['TIEN_THUE_GTGT'] = float(child.text)
            elif child.tag == 'VATAmount':
                res['TIEN_THUE_GTGT_QUY_DOI'] = float(child.text)

            elif child.tag == 'ListItemID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id 
            elif child.tag == 'ContractID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id 
            elif child.tag == 'ProjectWorkID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CONG_TRINH_ID'] = rid.id 
            elif child.tag == 'OrganizationUnitID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_ID'] = rid.id 
            elif child.tag == 'JobID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_THCP_ID'] = rid.id 

            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id 


            elif child.tag == 'CashOutExchangeRateFinance':
                res['TY_GIA_XUAT_QUY'] = float(child.text)
            elif child.tag == 'CashOutAmountFinance':
                res['THANH_TIEN_THEO_TY_GIA_XUAT_QUY'] = float(child.text)
            elif child.tag == 'CashOutDiffAmountFinance':
                res['CHENH_LECH'] = float(child.text) 

            elif child.tag == 'CashOutVATAmountFinance':
                res['TIEN_THUE_GTGT_THEO_TGXQ'] = float(child.text)
            elif child.tag == 'CashOutDiffVATAmountFinance':
                res['CHENH_LECH_TIEN_THUE_GTGT'] = float(child.text) 
            elif child.tag == 'SAVoucherRefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHUNG_TU_BAN_HANG_ID'] =rid.id
            elif child.tag == 'SAInvoiceRefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOA_DON_BAN_HANG_ID'] =rid.id
            elif child.tag == 'SAOrderRefDetailID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_CHI_TIET_ID'] = rid.id
            elif child.tag == 'SortOrder':
                res['THU_TU_SAP_XEP_CHI_TIET'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Báo giá
    def _import_SAQuote(self, tag):
        rec_model = 'sale.ex.bao.gia'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = child.text
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHACH_HANG_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_KHACH_HANG'] = child.text
            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text
            elif child.tag == 'JournalMemo':
                res['GHI_CHU'] = child.text
            elif child.tag == 'AccountObjectContactName':
                res['NGUOI_LIEN_HE'] = child.text  
            
            
            elif child.tag == 'AccountObjectTaxCode':
                res['MA_SO_THUE'] = child.text
            elif child.tag == 'RefNo':
                res['SO_BAO_GIA'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_BAO_GIA'] = child.text  
            elif child.tag == 'EffectiveDate':
                res['HIEU_LUC_DEN'] = child.text
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
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Báo giá chi tiết
    def _import_SAQuoteDetail(self, tag):
        rec_model = 'sale.ex.bao.gia.chi.tiet'
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
                    res['BAO_GIA_CHI_TIET_ID'] = rid.id    
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

            
            elif child.tag == 'VATRate':
                rid = self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:
                    res['PHAN_TRAM_THUE_GTGT_ID'] = rid.id  
            elif child.tag == 'DiscountRate':
                res['TY_LE_CK'] = float(child.text) 
            elif child.tag == 'SortOrder':
                res['THU_TU_SAP_XEP_CHI_TIET'] = int(child.text) 
            elif child.tag == 'IsPromotion':
                res['LA_HANG_KHUYEN_MAI'] = True if child.text == 'true' else False            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)  

    # Đơn đặt  hàng
    def _import_SAOrder(self, tag):
        rec_model = 'account.ex.don.dat.hang'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'

            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = child.text
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHACH_HANG_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_KHACH_HANG'] = child.text
            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'ShippingAddress':
                res['DIA_DIEM_GIAO_HANG'] = child.text  
            elif child.tag == 'OtherTerm':
                res['DIEU_KHOAN_KHAC'] = child.text
            elif child.tag == 'Status':
                res['TINH_TRANG'] = child.text
            elif child.tag == 'AccountObjectTaxCode':
                res['MA_SO_THUE'] = child.text
            elif child.tag == 'Receiver':
                res['NGUOI_NHAN_HANG'] = child.text
            elif child.tag == 'RefNo':
                res['SO_DON_HANG'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_DON_HANG'] = child.text  
            elif child.tag == 'DeliveryDate':
                res['NGAY_GIAO_HANG'] = child.text
            elif child.tag == 'BranchID':
                rid= self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID']=rid.id
            elif child.tag == 'EmployeeID':
                rid= self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NV_BAN_HANG_ID']=rid.id
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
            elif child.tag == 'IsCalculatedCost':
                res['TINH_GIA_THANH'] = True if child.text == 'true' else False
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Đơn đặt hàng chi tiết 
    def _import_SAOrderDetail(self, tag):
        rec_model = 'account.ex.don.dat.hang.chi.tiet'
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
                    res['DON_DAT_HANG_CHI_TIET_ID'] = rid.id    
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
            # elif child.tag == 'QuantityDelivered':
            #     res['SO_LUONG_DA_GIAO'] = float(child.text)
            

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

            elif child.tag == 'QuantityDeliveredSALastYear':
                res['SO_LUONG_DA_GIAO_NAM_TRUOC_BAN_HANG'] = float(child.text)
            elif child.tag == 'QuantityDeliveredINLastYear':
                res['SO_LUONG_DA_GIAO_NAM_TRUOC_PX'] = float(child.text)
            elif child.tag == 'QuantityDeliveredSA':
                res['SO_LUONG_DA_GIAO_BAN_HANG'] = float(child.text)
            elif child.tag == 'QuantityDeliveredIN':
                res['SO_LUONG_DA_GIAO_PX'] = float(child.text) 
            elif child.tag == 'DiscountAmount':
                res['TIEN_CHIET_KHAU_QUY_DOI'] = float(child.text)
            elif child.tag == 'LastYearDeliveredAmount':
                res['SO_TIEN_QUY_DOI_DA_GIAO_NAM_TRUOC'] = float(child.text)  
            elif child.tag == 'IsPromotion':
                res['LA_HANG_KHUYEN_MAI'] = True if child.text == 'true' else False   
            elif child.tag == 'SortOrder':
                res['THU_TU_SAP_XEP_CHI_TIET'] = int(child.text) 
            elif child.tag == 'DiscountRate':
                res['PHAN_TRAM_CHIET_KHAU'] = float(child.text) 
            elif child.tag == 'DiscountAmountOC':
                res['TIEN_CHIET_KHAU'] = float(child.text)        
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Hợp đồng bán
    def _import_Contract(self, tag):
        rec_model = 'sale.ex.hop.dong.ban'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ContractID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag=='IsProject':
                if child.text=='true':
                    res['HOP_DONG_DU_AN_SELECTION']='DU_AN'
                    res['LA_DU_AN']= True
                else:
                     res['HOP_DONG_DU_AN_SELECTION']='HOP_DONG'
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHACH_HANG_ID'] = rid.id
            elif child.tag == 'ProjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['THUOC_DU_AN_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_KHACH_HANG'] = child.text
            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text
            elif child.tag == 'OtherTerm':
                res['DIEU_KHOAN_KHAC'] = child.text
            elif child.tag == 'AccountObjectContactName':
                res['NGUOI_LIEN_HE'] = child.text
            elif child.tag == 'PaymentDate':
                res['HAN_THANH_TOAN'] = child.text  
            elif child.tag == 'DeliveryDate':
                res['HAN_GIAO_HANG'] = child.text
            elif child.tag == 'ContractCode':
                res['SO_HOP_DONG'] = child.text
            elif child.tag == 'SignDate':
                res['NGAY_KY'] = child.text
            elif child.tag == 'ContractSubject':
                res['TRICH_YEU'] = child.text  
            elif child.tag == 'OtherTerms':
                res['DIEU_KHOAN_KHAC'] = child.text

            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)

            elif child.tag == 'CloseDate':
                res['NGAY_THANH_LY_HUY_BO'] = child.text  
            elif child.tag == 'CloseReason':
                res['LY_DO'] = child.text
            elif child.tag == 'BranchID':
                rid= self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID']=rid.id
            elif child.tag == 'EmployeeID':
                rid= self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NGUOI_THUC_HIEN_ID']=rid.id
            elif child.tag == 'OrganizationUnitID':
                rid= self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_THUC_HIEN_ID']=rid.id
            elif child.tag == 'CurrencyID':
                rid = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
            elif child.tag == 'ExchangeRate':
                res['TY_GIA'] = float(child.text)
            elif child.tag == 'IsArisedBeforeUseSoftware':
                res['LA_HOP_DONG_DU_AN_PHAT_SINH_TRUOC_KHI_SU_DUNG_PHAN_MEM'] = True if child.text == 'true' else False
            elif child.tag == 'IsCalculatedCost':
                res['TINH_GIA_THANH'] = True if child.text == 'true' else False
            elif child.tag == 'IsInvoiced':
                res['DA_XUAT_HOA_DON'] = True if child.text == 'true' else False
           
            
            elif child.tag == 'RevenueDate':
                res['NGAY_GHI_DOANH_SO'] = child.text

            elif child.tag == 'ContractAmountOC':
                res['GIA_TRI_HOP_DONG'] = float(child.text)
            elif child.tag == 'ContractAmount':
                res['GTHD_QUY_DOI'] = float(child.text)
            elif child.tag == 'CloseAmountOC':
                res['GIA_TRI_THANH_LY'] = float(child.text)
            elif child.tag == 'CloseAmount':
                res['GTTL_QUY_DOI'] = float(child.text)

            elif child.tag == 'ExpenseAmountFinance':
                res['SO_DA_CHI'] = float(child.text)
            elif child.tag == 'ReceiptAmountOCFinance':
                res['SO_DA_THU'] = float(child.text)
            elif child.tag == 'ReceiptAmountFinance':
                res['SO_DA_THU_QUY_DOI'] = float(child.text)
            elif child.tag == 'InvoiceAmountOCFinance':
                res['GIA_TRI_DA_XUAT_HD'] = float(child.text)
            elif child.tag == 'InvoiceAmountFinance':
                res['GT_DA_XUAT_HD_QUY_DOI'] = float(child.text)
            elif child.tag == 'AccumSaleAmountFinance':
                res['DOANH_THU'] = float(child.text)
            elif child.tag == 'AccumCostAmountFinance':
                res['GIA_VON_HANG_BAN'] = float(child.text)
            elif child.tag == 'AccumOtherAmountFinance':
                res['CHI_PHI_KHAC'] = float(child.text)
            elif child.tag == 'ContractStatusID':
                res['TINH_TRANG_HOP_DONG'] = child.text
            elif child.tag == 'IsParent':           
                res['isparent'] = True if child.text == 'true' else False
            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False) 

    # Hợp đồng bán  chi tiết(dự kiến chi)
    def _import_ContractDetailExpense(self, tag):
        rec_model = 'sale.ex.hop.dong.ban.chi.tiet.du.kien.chi'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ContractDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'ContractID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id    
            elif child.tag == 'ExpenseItemID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id    
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'OrganizationUnitID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_ID'] = rid.id    
            elif child.tag == 'Rate':
                res['TY_LE_PHAN_TRAM'] = float(child.text)
            elif child.tag == 'Amount':
                res['SO_TIEN'] = float(child.text)
            # elif child.tag == 'QuantityDelivered':
            #     res['SO_LUONG_DA_GIAO'] = float(child.text)
            elif child.tag == 'ExpenseDate':
                res['NGAY_DU_KIEN_CHI'] = child.text 
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # Hợp đồng bán chi tiết(hàng hóa dịch vụ) 
    def _import_ContractDetailInventoryItem(self, tag):
        rec_model = 'sale.ex.hop.dong.ban.chi.tiet.hang.hoa.dich.vu'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ContractDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'ContractID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id    
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
                res['SO_LUONG_YEU_CAU'] = float(child.text)
            elif child.tag == 'UnitPrice':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'QuantityDeliveredSA':
                res['SO_LUONG_DA_GIAO'] = float(child.text)
            elif child.tag == 'AmountOC':
                res['THANH_TIEN'] = float(child.text)
            elif child.tag == 'Amount':
                res['THANH_TIEN_QUY_DOI'] = float(child.text)

            elif child.tag == 'DiscountRate':
                res['TY_LE_CK'] = float(child.text)
            elif child.tag == 'DiscountAmountOC':
                res['TIEN_CHIET_KHAU'] = float(child.text)
            elif child.tag == 'DiscountAmount':
                res['TIEN_CHIET_KHAU_QUY_DOI'] = float(child.text)


            elif child.tag == 'VATAmountOC':
                res['TIEN_THUE_GTGT'] = float(child.text)
            elif child.tag == 'VATAmount':
                res['TIEN_THUE_GTGT_QUY_DOI'] = float(child.text)
            
            elif child.tag == 'VATRate':
                rid = self.env['danh.muc.thue.suat.gia.tri.gia.tang'].search([('PHAN_TRAM_THUE_GTGT', '=', child.text)], limit=1)
                if rid:
                    res['PHAN_TRAM_THUE_GTGT_ID'] = rid.id   
            elif child.tag == 'SAOrderID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id  
            elif child.tag == 'TotalAmountOC':
                res['TONG_TIEN'] = float(child.text)
            elif child.tag == 'TotalAmount':
                res['TONG_TIEN_QUY_DOI'] = float(child.text) 
            elif child.tag == 'SortOrder':
                res['STT'] = int(child.text)        
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Hợp đồng bán  chi tiết(liên hệ)
    def _import_ContractDetailContact(self, tag):
        rec_model = 'sale.ex.hop.dong.ban.chi.tiet.lien.he'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ContractDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'ContractID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id    
            elif child.tag == 'ContactName':
                res['HO_VA_TEN'] = child.text
            elif child.tag == 'ContactTitle':
                res['CHUC_VU'] = child.text
            elif child.tag == 'ContactMobile':
                res['DT_DI_DONG'] = child.text
            elif child.tag == 'OtherContactMobile':
                res['DT_DI_DONG_KHAC'] = child.text
            elif child.tag == 'ContactOfficeTel':
                res['DT_CO_DINH'] = child.text
            # elif child.tag == 'QuantityDelivered':
            #     res['SO_LUONG_DA_GIAO'] = float(child.text)
            elif child.tag == 'ContactEmail':
                res['EMAIL'] = child.text 
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Hợp đồng bán  chi tiết(ghi nhận doanh số)
    def _import_ContractDetailRevenue(self, tag):
        rec_model = 'sale.ex.hop.dong.ban.chi.tiet.ghi.nhan.doanh.so'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ContractDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'ContractID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id    
            elif child.tag == 'EmployeeID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['NHAN_VIEN_ID'] = rid.id    
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'OrganizationUnitID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_ID'] = rid.id   
            elif child.tag == 'InventoryItemID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HANG_HOA_ID'] = rid.id     
            elif child.tag == 'Rate':
                res['TY_LE_PHAN_TRAM'] = float(child.text)
            elif child.tag == 'RevenueAmount':
                res['DOANH_SO_GHI_NHAN_HUY_BO'] = float(child.text)
            # elif child.tag == 'QuantityDelivered':
            #     res['SO_LUONG_DA_GIAO'] = float(child.text)
            elif child.tag == 'CancelRevenueDate':
                res['NGAY'] = child.text 
            elif child.tag == 'RevenueType':
                res['LOAI'] = child.text 
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Reference giữa chứng từ bán hàng và hóa đơn
    def _import_SAInvoiceReference(self, tag):
        ref = False
        rid = False
        for child in tag.getchildren():
            if child.tag == 'VoucherRefID':
                ref = self.env.ref('{}.{}'.format(MODULE,child.text), False)
            elif child.tag == 'SAInvoiceRefID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)

        if rid and ref and ((hasattr(ref, 'LAP_KEM_HOA_DON') and ref.LAP_KEM_HOA_DON) or not hasattr(ref, 'LAP_KEM_HOA_DON')):
            # Update hóa đơn
            rid.write({'SOURCE_ID': ref._name + ',' + str(ref.id)})
            # Update chứng từ
            ref.write({
                'SO_HOA_DON': rid.SO_HOA_DON,
                'NGAY_HOA_DON': rid.NGAY_HOA_DON,
                'KY_HIEU_HD': rid.KY_HIEU_HD,
                'MAU_SO_HD_ID': rid.MAU_SO_HD_ID.id,
                'HOA_DON_IDS': [(4, rid.id)]
                })
        elif rid and ref:
            # Update chứng từ
            ref.write({
                'HOA_DON_IDS': [(4, rid.id)]
                })
        # Đã update trực tiếp ở bên trên, không cần update lại nữa
        # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/1537

    # Reference giữa chứng từ bán hàng và phiếu xuất
    def _import_SaleOutwardReference(self, tag):
        ref = False
        rid = False
        XUAT_KHO_REF_ID = False
        for child in tag.getchildren():
            if child.tag == 'SAVoucherRefID':
                ref = self.env.ref('{}.{}'.format(MODULE,child.text), False)
            elif child.tag == 'INOutwardRefID':
                XUAT_KHO_REF_ID = child.text
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
        
        if ref and ((hasattr(ref, 'KIEM_PHIEU_NHAP_XUAT_KHO') and ref.KIEM_PHIEU_NHAP_XUAT_KHO) or not hasattr(ref, 'KIEM_PHIEU_NHAP_XUAT_KHO')):
            if rid:
                # Update phiếu xuất
                rid.write({'SOURCE_ID': ref._name + ',' + str(ref.id)})
                # Update chứng từ
                ref.write({
                    'SO_CHUNG_TU_PHIEU_XUAT': rid.SO_CHUNG_TU,
                    'NGUOI_GIAO_NHAN_HANG': rid.NGUOI_NHAN_TEXT,
                    'LY_DO_NHAP_XUAT': rid.LY_DO_XUAT,
                    'PHIEU_XUAT_IDS': [(4, rid.id)]
                    })
            elif XUAT_KHO_REF_ID:
                ref.write({
                    'XUAT_KHO_REF_ID': XUAT_KHO_REF_ID,
                })
        # Đã update trực tiếp ở bên trên, không cần update lại nữa
        # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/1537

    def _import_SaleOutwardReferenceDetail(self, tag):
        ref = False
        rid = False
        for child in tag.getchildren():
            if child.tag == 'SAVoucherRefDetailID':
                ref = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
            elif child.tag == 'INOutwardRefDetailID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
        
        if ref and rid:
            # Update chứng từ
            if ref.id not in [sale['id'] for sale in rid.SALE_DOCUMENT_LINE_IDS]:
                rid.write({
                    'SALE_DOCUMENT_LINE_IDS': [(4, ref.id)]
                    })

    def _import_SAReturnInwardReferenceDetail(self, tag):
        ref = False
        rid = False
        for child in tag.getchildren():
            if child.tag == 'SAReturnRefDetailID':
                ref = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
            elif child.tag == 'InwardRefDetailID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
        
        if ref and rid:
            # Update chứng từ
            if ref.id not in [sale['id'] for sale in rid.TRA_LAI_HANG_BAN_CHI_TIET_IDS]:
                rid.write({
                    'TRA_LAI_HANG_BAN_CHI_TIET_IDS': [(4, ref.id)]
                    })
            
        