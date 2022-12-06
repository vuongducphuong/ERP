# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, helper

MODULE = 'base_import_ex'


class Import(models.TransientModel):
    _inherit = 'base_import_ex.import'

    # Nhập kho

    def _import_INInward(self, tag):
        rec_model = 'stock.ex.nhap.xuat.kho'
        res = {'type':'NHAP_KHO'}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text.lower()
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_NGUOI_GIAO_HANG'] = child.text
            elif child.tag == 'ContactName':
                res['NGUOI_GIAO_HANG_TEXT'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text

            elif child.tag == 'RefType':
                if child.text == '2010':
                    res['LOAI_NHAP_KHO'] = 'THANH_PHAM'
                elif child.text =='2013':
                    res['LOAI_NHAP_KHO'] = 'TRA_LAI'
                elif child.text == '2014':
                    res['LOAI_NHAP_KHO'] = 'KHAC'
                elif child.text == '2011':
                    res['LOAI_CHUNG_TU_2'] = '2011'
                elif child.text == '2012':
                    res['LOAI_CHUNG_TU_2'] = '2012'
                elif child.text == '2015':
                    res['LOAI_CHUNG_TU_2'] = '2015'
                elif child.text == '2024':
                    res['LOAI_CHUNG_TU_2'] = '2024'
                elif child.text == '2026':
                    res['LOAI_CHUNG_TU_2'] = '2026'
                elif child.text == '2025':
                    res['LOAI_CHUNG_TU_2'] = '2025'
                elif child.text == '2020':
                    res['LOAI_XUAT_KHO'] = 'BAN_HANG'
                elif child.text == '2023':
                    res['LOAI_XUAT_KHO'] = 'SAN_XUAT'
                elif child.text == '2021':
                    res['LOAI_XUAT_KHO'] = 'XUAT_HANG'
                elif child.text == '2022':
                    res['LOAI_XUAT_KHO'] = 'KHAC'
                elif child.text == '2030':
                    res['loai_chuyen_kho'] = 'van_chuyen'
                elif child.text == '2031':
                    res['loai_chuyen_kho'] = 'gui_ban'
                elif child.text == '2032':
                    res['loai_chuyen_kho'] = 'chuyen_kho'


            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'EmployeeID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['NHAN_VIEN_ID'] = rid.id
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'DocumentIncluded':
                res['KEM_THEO_CHUNG_TU_GOC'] = child.text
            elif child.tag == 'AssemblyRefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['LAP_RAP_THAO_DO_ID'] = rid.id
            elif child.tag == 'UnitPriceMethod':
                res['PHUONG_THUC_TINH_DON_GIA_NHAP'] = child.text
            elif child.tag == 'SAReturnRefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['LAP_TU_HANG_BAN_TRA_LAI'] = rid.id
            elif child.tag == 'IsReturnWithInward':
                res['KIEM_TRA_PHIEU_NHAP_KHO'] = False if child.text == 'false' else True
            elif child.tag == 'RefOrder':
                res['STT_NHAP_CHUNG_TU'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # xuất chi tiết
    def _import_INInwardDetail(self, tag):
        rec_model = 'stock.ex.nhap.xuat.kho.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text.lower()
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['NHAP_XUAT_ID'] = rid.id
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id
            elif child.tag == 'Description':
                res['TEN_HANG'] = child.text
            elif child.tag == 'StockID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['KHO_ID'] = rid.id
            elif child.tag == 'DebitAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text.lower())], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id

            elif child.tag == 'CreditAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text.lower())], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id

            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'UnitPriceFinance':
                res['DON_GIA_VON'] = float(child.text)
            elif child.tag == 'AmountFinance':
                res['TIEN_VON_QUY_DOI'] = float(child.text) 
            elif child.tag == 'AmountFinanceOC':
                res['TIEN_VON'] = float(child.text)
            elif child.tag == 'SalePrice':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'SaleAmount':
                res['THANH_TIEN'] = float(child.text)
            elif child.tag == 'ExpiryDate':
                res['HAN_SU_DUNG'] = child.text
            elif child.tag == 'LotNo':
                res['SO_LO'] = child.text

            elif child.tag == 'UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['DVT_ID'] = rid.id
            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['DON_VI_ID'] = rid.id

            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['DOI_TUONG_THCP_ID'] = rid.id

            elif child.tag == 'ProjectWorkID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['CONG_TRINH_ID'] = rid.id
            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id

            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id
            
            elif child.tag == 'ProductionOrderRefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['LENH_SAN_XUAT_ID'] = rid.id 
            
            elif child.tag == 'ProductionID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['THANH_PHAM_ID'] = rid.id     
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
            elif child.tag == 'SAOrderRefDetailID':
                rid =self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['DON_DAT_HANG_CHI_TIET_ID'] = rid.id
            elif child.tag == 'MainQuantity':
                res['SO_LUONG_THEO_DVT_CHINH'] = float(child.text)
            elif child.tag == 'ExchangeRateOperator':
                if child.text =='*':
                    res['TOAN_TU_QUY_DOI'] = '0'
                elif child.text =='/':
                    res['TOAN_TU_QUY_DOI'] = '1'
            elif child.tag == 'MainConvertRate':
                res['TY_LE_CHUYEN_DOI_RA_DVT_CHINH'] = float(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # phiếu xuất
    def _import_INOutward(self, tag):
        rec_model = 'stock.ex.nhap.xuat.kho'
        res = {'type': 'XUAT_KHO'}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text.lower()
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_KHACH_HANG'] = child.text
            elif child.tag == 'ContactName':
                res['NGUOI_NHAN_TEXT'] = child.text
            elif child.tag == 'AccountObjectAddress':
                res['DIA_CHI'] = child.text


            elif child.tag == 'OrderNo':
                res['LENH_DIEU_DONG_SO'] = child.text
            elif child.tag == 'OrderDate':
                res['NGAY'] = child.text
            elif child.tag == 'ContractCode':
                res['HOP_DONG_SO'] = child.text
            elif child.tag == 'Transport':
                res['PHUONG_TIEN'] = helper.Obj.convert_to_key(child.text)
            elif child.tag == 'TransporterID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['NGUOI_VAN_CHUYEN_ID'] = rid.id
            elif child.tag == 'TransporterName':
                res['TEN_NGUOI_VAN_CHUYEN'] = child.text
            elif child.tag == 'JournalMemo':
                res['LY_DO_XUAT'] = child.text
            elif child.tag == 'FromStockID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['XUAT_TAI_KHO_ID'] = rid.id
            elif child.tag == 'ToStockID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['NHAP_TAI_KHO_ID'] = rid.id

            elif child.tag == 'RefType':
                if child.text == '2020':
                    res['LOAI_XUAT_KHO'] = 'BAN_HANG'
                elif child.text == '2023':
                    res['LOAI_XUAT_KHO'] = 'SAN_XUAT'
                elif child.text == '2021':
                    res['LOAI_XUAT_KHO'] = 'XUAT_HANG'
                elif child.text == '2022':
                    res['LOAI_XUAT_KHO'] = 'KHAC'
                
                elif child.text == '2011':
                    res['LOAI_CHUNG_TU_2'] = '2011'
                elif child.text == '2012':
                    res['LOAI_CHUNG_TU_2'] = '2012'
                elif child.text == '2015':
                    res['LOAI_CHUNG_TU_2'] = '2015'
                elif child.text == '2024':
                    res['LOAI_CHUNG_TU_2'] = '2024'
                elif child.text == '2026':
                    res['LOAI_CHUNG_TU_2'] = '2026'

                elif child.text == '2025':
                    res['LOAI_CHUNG_TU_2'] = '2025'

                elif child.text == '2010':
                    res['LOAI_NHAP_KHO'] = 'THANH_PHAM'
                elif child.text == '2013':
                    res['LOAI_NHAP_KHO'] = 'TRA_LAI'
                elif child.text == '2014':
                    res['LOAI_NHAP_KHO'] = 'KHAC'
                
                elif child.text == '2030':
                    res['loai_chuyen_kho'] = 'van_chuyen'
                elif child.text == '2031':
                    res['loai_chuyen_kho'] = 'gui_ban'
                elif child.text == '2032':
                    res['loai_chuyen_kho'] = 'chuyen_kho'
                
                
                
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'EmployeeID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['NHAN_VIEN_ID'] = rid.id
            elif child.tag == 'DocumentIncluded':
                res['KEM_THEO_CHUNG_TU_GOC'] = child.text
            elif child.tag == 'ShippingAddress':
                res['DIA_DIEM_GIAO_HANG_ID'] = child.text
            
            elif child.tag == 'InvTemplateNo':
                res['MAU_SO'] = child.text
            elif child.tag == 'InvSeries':
                res['KY_HIEU'] = child.text
            elif child.tag == 'InvNo':
                res['SO_CHUNG_TU_CK_READONLY'] = child.text
            elif child.tag == 'CurrencyID':
                rid =self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
            elif child.tag == 'RevenueStatus':
                res['TRANG_THAI_DOANH_THU'] = int(child.text)
            elif child.tag == 'IsSaleWithOutward':
                res['KIEM_PHIEU_NHAP_XUAT_KHO'] = True if child.text == 'true' else False
        
        # Tìm chứng từ tạo ra phiếu xuất này. Hiện tại chỉ có chứng từ bán hàng
        for model in ('sale.document',):
            domains = [('XUAT_KHO_REF_ID', '=', rec_id)]
            doc = self.env[model].search(domains, limit=1)
            if doc:
                # Chỉ lấy một số giá trị trong hóa đơn gắn kèm, các giá trị còn lại không đúng
                doc.write({
                    'SO_CHUNG_TU_PHIEU_XUAT': res.get('SO_CHUNG_TU'),
                    'NGUOI_GIAO_NHAN_HANG': res.get('NGUOI_NHAN_TEXT'),
                    'LY_DO_NHAP_XUAT': res.get('LY_DO_XUAT'),
                    # 'PHIEU_XUAT_IDS': [(4, rid.id)]
                })
                res['SOURCE_ID'] = doc._name + ',' + str(doc.id)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    #phiếu xuất chi tiết

    def _import_INOutwardDetail(self, tag):
        rec_model = 'stock.ex.nhap.xuat.kho.chi.tiet'
        res = {}
        rec_id = False

        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text.lower()
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['NHAP_XUAT_ID'] = rid.id
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id
            elif child.tag == 'Description':
                res['TEN_HANG'] = child.text
            elif child.tag == 'StockID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['KHO_ID'] = rid.id
            elif child.tag == 'DebitAccount':
                res['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search(
                    [('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag == 'CreditAccount':
                res['TK_CO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search(
                    [('SO_TAI_KHOAN', '=', child.text)], limit=1).id
            elif child.tag == 'UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['DVT_ID'] = rid.id
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'MainQuantity':
                res['SO_LUONG_THEO_DVT_CHINH'] = float(child.text)
            elif child.tag == 'UnitPriceFinance':
                res['DON_GIA_VON'] = float(child.text)
            # vì bảng này không có nguyên tệ
            elif child.tag == 'AmountFinance':
                res['TIEN_VON'] = float(child.text)
            elif child.tag == 'SalePrice':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'SaleAmount':
                res['THANH_TIEN'] = float(child.text)
            elif child.tag == 'LotNo':
                res['SO_LO'] = child.text
            elif child.tag == 'ExpiryDate':
                res['HAN_SU_DUNG'] = child.text

            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['DON_VI_ID'] = rid.id
            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['DOI_TUONG_THCP_ID'] = rid.id
            elif child.tag == 'ProjectWorkID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['CONG_TRINH_ID'] = rid.id
            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id 
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_DOI_TUONG'] = child.text
            elif child.tag == 'PUContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['HOP_DONG_MUA_ID'] = rid.id
            
            elif child.tag == 'ProductionOrderRefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['LENH_SAN_XUAT_ID'] = rid.id 
            
            elif child.tag == 'ProductionID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['THANH_PHAM_ID'] = rid.id 
            
            elif child.tag == 'SAOrderRefDetailID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['DON_DAT_HANG_CHI_TIET_ID'] = rid.id 

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


# phiếu chuyển kho


    def _import_INTransfer(self, tag):
        rec_model = 'stock.ex.nhap.xuat.kho'
        res = {'type': 'CHUYEN_KHO'}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'

            elif child.tag == 'RefType':
                if child.text == '2030':
                    res['loai_chuyen_kho'] = 'van_chuyen'
                elif child.text =='2031':
                    res['loai_chuyen_kho'] = 'gui_ban'
                elif child.text =='2032':
                    res['loai_chuyen_kho'] = 'chuyen_kho'

            elif child.tag == 'TransporterID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['NGUOI_VAN_CHUYEN_ID'] = rid.id
            elif child.tag == 'TransporterName':
                res['TEN_NGUOI_VAN_CHUYEN'] = child.text
            elif child.tag == 'ContractCode':
                res['LENH_DIEU_DONG_SO'] = child.text
            elif child.tag == 'ContractDate':
                res['NGAY'] = child.text
            elif child.tag == 'ContractOwner':
                res['CUA'] = child.text
            elif child.tag == 'JournalMemo':
                res['VE_VIEC'] = child.text
            elif child.tag == 'TransportContractCode':
                res['HOP_DONG_SO'] = child.text
            # elif child.tag == 'ContractCode':
            #     res['HOP_DONG_KT_SO'] = child.text
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'AccountObjectName':
                res['TEN_KHACH_HANG'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            # elif child.tag == 'RefType':
            #     res['LOAI_CHUNG_TU'] = int(child.text)
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text



            elif child.tag == 'InvTemplateNo':
                res['MAU_SO'] = child.text
            elif child.tag == 'InvSeries':
                res['KY_HIEU'] = child.text
            elif child.tag == 'InvNo':
                res['SO_CHUNG_TU_CK_READONLY'] = child.text

            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id

            elif child.tag == 'Transport':
                res['PHUONG_TIEN'] = helper.Obj.convert_to_key(child.text)
            elif child.tag == 'CompanyTaxCode':
                
                res['MA_SO_THUE'] = child.text
            elif child.tag == 'ListNo':
                res['SO_KHAC'] = child.text
            elif child.tag == 'ListDate':
                res['NGAY_CK'] = child.text
            elif child.tag == 'CommonInventoryName':
                res['TEN_MAT_HANG_CHUNG'] = child.text
            elif child.tag == 'IsAttachList':
                res['IN_KEM_BANG_KE'] = True if child.text == 'true' else False
            
            elif child.tag == 'InventoryPostedDate':
                res['NGAY_GHI_SO_CK'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

# phiếu chuyển kho chi tiết
    def _import_INTransferDetail(self, tag):
        rec_model = 'stock.ex.nhap.xuat.kho.chi.tiet'
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
                    res['NHAP_XUAT_ID'] = rid.id
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id
            elif child.tag == 'Description':
                res['TEN_HANG'] = child.text
            elif child.tag == 'FromStockID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['XUAT_TAI_KHO_ID'] = rid.id
            elif child.tag == 'ToStockID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['NHAP_TAI_KHO_ID'] = rid.id
            elif child.tag == 'DebitAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id
            elif child.tag == 'CreditAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id

            elif child.tag == 'UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'UnitPriceFinance':
                res['DON_GIA_VON'] = float(child.text)
            elif child.tag == 'AmountFinance':
                res['TIEN_VON'] = float(child.text)
            elif child.tag == 'SalePrice':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'SaleAmount':
                res['THANH_TIEN'] = float(child.text)
            elif child.tag == 'LotNo':
                res['SO_LO'] = child.text
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id
            elif child.tag == 'ExpiryDate':
                res['HAN_SU_DUNG'] = child.text
            elif child.tag == 'MainQuantity':
                res['SO_LUONG_THEO_DVT_CHINH'] = float(child.text)
            elif child.tag == 'MainUnitPriceFinance':
                res['DON_GIA_DVT_CHINH'] = float(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Lệnh sản xuất
    def _import_INProductionOrder(self, tag):
        rec_model = 'stock.ex.lenh.san.xuat'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefNo':
                res['SO_LENH'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY'] = child.text
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'Status':
                res['TINH_TRANG'] = child.text
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'IsInwardDone':
                res['DA_LAP_DU_PN'] = True if child.text == 'true' else False
            elif child.tag == 'IsOutwardDone':
                res['DA_LAP_DU_PX'] = True if child.text == 'true' else False
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # lắp sản xuất chi tiết(thành phẩm)
    def _import_INProductionOrderProduct(self, tag):
        rec_model = 'stock.ex.lenh.san.xuat.chi.tiet.thanh.pham'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ProductionID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID'] = rid.id
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id
            elif child.tag == 'Description':
                res['TEN_THANH_PHAM'] = child.text
            elif child.tag == 'UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id
            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_THCP_ID'] = rid.id
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'SortOrder':
                res['sequence'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # lắp sản xuất chi tiết(định mức nvl)
    def _import_INProductionOrderDetail(self, tag):
        rec_model = 'stock.ex.thanh.pham.chi.tiet.dinh.muc.xuat.nvl'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'ProductionID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['THANH_PHAM_CHI_TIET_DINH_MUC_XUAT_NVL_ID'] = rid.id
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id
            elif child.tag == 'Description':
                res['TEN_NGUYEN_VAT_LIEU'] = child.text
            elif child.tag == 'UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id
            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id
            
            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_THCP_ID'] = rid.id
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id
            elif child.tag == 'QuantityOnUnit':
                res['SO_LUONG_NVL_TREN_SP'] = float(child.text)
            elif child.tag == 'Quantity':
                res['SO_LUONG_NVL'] = float(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    


    # Lắp ráp, tháo dỡ
    def _import_INAssemblyDisassembly(self, tag):
        rec_model = 'stock.ex.lap.rap.thao.do'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HANG_HOA_ID'] = rid.id
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'RefDate':
                res['NGAY'] = child.text
            elif child.tag == 'RefNo':
                res['SO'] = child.text
            elif child.tag == 'UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id
            elif child.tag =='RefType':
                if child.text=='2050':
                    res['LAP_RAP_THAO_DO']='LAP_RAP'
                else:
                    res['LAP_RAP_THAO_DO']='THAO_DO'
                res['LOAI_CHUNG_TU'] = int(child.text)
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # lắp ráp tháo dỡ chi tiết
    def _import_INAssemblyDisassemblyDetail(self, tag):
        rec_model = 'stock.ex.lap.rap.thao.do.chi.tiet'
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
                    res['LAP_RAP_THAO_DO_CHI_TIET_ID'] = rid.id
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id
            elif child.tag == 'Description':
                res['TEN_HANG'] = child.text
            elif child.tag == 'StockID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHO_ID'] = rid.id
            elif child.tag == 'UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'UnitPriceFinance':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'AmountFinance':
                res['THANH_TIEN'] = float(child.text)
            elif child.tag == 'SortOrder':
                res['sequence'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


#  # kiểm kê vật tư hàng hóa
    def _import_INAudit(self, tag):
        rec_model = 'stock.ex.kiem.ke.bang.kiem.ke.vat.tu.hang.hoa.form'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefDate':
                res['NGAY'] = child.text
            elif child.tag == 'AuditDate':
                res['DEN_NGAY'] = child.text
            elif child.tag == 'RefNo':
                res['SO'] = child.text
            elif child.tag == 'JournalMemo':
                res['MUC_DICH'] = child.text
            elif child.tag == 'Summary':
                res['KET_LUAN'] = child.text

            elif child.tag == 'AuditType':
                if child.text=='1':
                    res['CHI_TIET_THEO_SELECTION'] = '1'
                elif child.text=='2':
                    res['CHI_TIET_THEO_SELECTION'] = '2'
            # elif child.tag == 'RefTime':
            #     res['GIO'] = float(child.text)
            elif child.tag == 'StockID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KIEM_KE_KHO_ID'] = rid.id
            elif child.tag == 'IsValueAudit':
                res['KIEM_KE_GIA_TRI'] = True if child.text == 'true' else False
            elif child.tag == 'IsExecuted':
                res['DA_XU_LY_CHENH_LECH'] = True if child.text == 'true' else False
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # #kiểm kê vật tư hàng hóa chi tiết
    def _import_INAuditDetail(self, tag):
        rec_model = 'stock.ex.bang.kiem.ke.vthh.can.dieu.chinh.chi.tiet.form'
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
                    res['KIEM_KE_BANG_KIEM_KE_VTHH_ID'] = rid.id
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id
            elif child.tag == 'UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DVT_ID'] = rid.id
            elif child.tag == 'GoodQuantity':
                res['PHAM_CHAT_CON_TOT'] = float(child.text)
            elif child.tag == 'LowQuantity':
                res['KEM_PHAM_CHAT'] = float(child.text)
            elif child.tag == 'LostQuantity':
                res['MAT_PHAM_CHAT'] = float(child.text)

            elif child.tag == 'AmountAudit':
                res['GIA_TRI_KIEM_KE'] = float(child.text)
            elif child.tag == 'AmountOnBook':
                res['GIA_TRI_SO_KE_TOAN'] = float(child.text)
            elif child.tag == 'DiffAmount':
                res['GIA_TRI_CHENH_LECH'] = float(child.text) 

            elif child.tag == 'QuantityOnBook':
                res['SO_LUONG_SO_KE_TOAN'] = float(child.text)
            elif child.tag == 'QuantityAudit':
                res['SO_LUONG_KIEM_KE'] = float(child.text)
            elif child.tag == 'DiffQuantity':
                res['SO_LUONG_CHENH_LECH'] = float(child.text) 

            elif child.tag == 'LotNo':
                res['SO_LO'] =child.text
            elif child.tag == 'ExpiryDate':
                res['HAN_SU_DUNG'] =child.text 

            elif child.tag == 'SerialNumber1':
                res['MA_QUY_CACH_1'] = child.text
            elif child.tag == 'SerialNumber2':
                res['MA_QUY_CACH_2'] = child.text
            elif child.tag == 'SerialNumber3':
                res['MA_QUY_CACH_3'] =child.text
            elif child.tag == 'SerialNumber4':
                res['MA_QUY_CACH_4'] =child.text
            elif child.tag == 'SerialNumber5':
                res['MA_QUY_CACH_5'] =child.text
            elif child.tag == 'StockID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_KHO_ID'] = rid.id       
            
            elif child.tag == 'ExecuteAction':
                res['XU_LY'] =child.text
            elif child.tag == 'SortOrder':
                res['sequence'] = int(child.text) 
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # kiểm kê vật tư hàng hóa chi tiet(thanh vien tham gia)
    def _import_INAuditMemberDetail(self, tag):
        rec_model = 'stock.ex.bang.kiem.ke.vthh.tv.tham.gia.chi.tiet.form'
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
                    res['BANG_KIEM_KE_VTHH_ID'] = rid.id
            
            elif child.tag == 'AccountObjectName':
                res['HO_VA_TEN'] = child.text
            elif child.tag == 'Position':
                res['CHUC_DANH'] =child.text
            elif child.tag == 'Representative':
                res['DAI_DIEN'] = child.text
            elif child.tag == 'SortOrder':
                res['sequence'] = int(child.text) 
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


#  # Tính giá xuất kho tức thời theo kho
    def _import_InventoryItemPriceOutwardImmediate(self, tag):
        rec_model = 'stock.ex.tinh.gia.xuat.kho.tuc.thoi.theo.kho'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ID_Action':
                rec_id = child.text.lower()
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id
            elif child.tag == 'UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['MA_DON_VI_TINH_ID'] = rid.id
            elif child.tag == 'MainUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['MA_DON_VI_TINH_CHINH_ID'] = rid.id
            elif child.tag == 'ExchangeRateOperator':
                if child.text=='*':
                    res['TOAN_TU_QUY_DOI'] = 'NHAN'
                elif child.text=='/':
                    res['TOAN_TU_QUY_DOI'] = 'CHIA'

            elif child.tag == 'ConvertRate':
                res['TY_LE_CHUYEN_DOI'] = float(child.text)
            elif child.tag == 'StockID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['MA_KHO_ID'] = rid.id

            elif child.tag == 'DateTimeAction':
                res['THOI_GIAN_HOAT_DONG'] = child.text
            elif child.tag == 'Quantity':
                res['SO_LUONG_VAT_TU'] = float(child.text)
            elif child.tag == 'PriceRow':
                res['DON_GIA_DONG'] = float(child.text)
            elif child.tag == 'AmountRow':
                res['THANH_TIEN_DONG'] = child.text
            elif child.tag == 'QuantityMainUnit':
                res['SO_LUONG_THEO_DVT_CHINH'] = float(child.text)
            elif child.tag == 'PriceMainUnit':
                res['DON_GIA_THEO_DVT_CHINH'] = float(child.text)
            elif child.tag == 'AmountRowMainUnit':
                res['THANH_TIEN_DONG_DVT_CHINH'] = float(child.text)
            elif child.tag == 'RemainQuantityMainUnit':
                res['SO_LUONG_TON_THEO_DVT_CHINH'] = float(child.text)

            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'SortOrder':
                res['STT'] = int(child.text)
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
            
            elif child.tag == 'IsUnUpdateOutwardPrice':
                res['KHONG_CAP_NHAT_GIA_XUAT'] = True if child.text == '1' else False
            elif child.tag == 'AssemblyRefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['LAP_RAP_THAO_DO_ID'] = rid.id
            elif child.tag == 'IsNeedUpdatePrice':
                res['KHONG_CAN_CAP_NHAT_GIA_XUAT'] = True if child.text == '1' else False
            elif child.tag == 'LastTimeUpdatePrice':
                res['THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT'] = child.text
            elif child.tag == 'UnitPriceMethod':
                res['PHAN_BIET_GIA'] = int(child.text)
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
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'AccumQuantityMainUnit':
                res['SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH'] = float(child.text)
            elif child.tag == 'AccumAmountStock':
                res['TONG_GIA_TRI_LUY_KE_KHO'] = float(child.text)
            
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['ID_CHUNG_TU'] = rid.id
                    res['MODEL_CHUNG_TU'] = rid._name
            elif child.tag == 'RefDetailID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['ID_CHUNG_TU_CHI_TIET'] = rid.id
                    res['MODEL_CHUNG_TU_TIET'] = rid._name
            elif child.tag == 'TypeActionInOut':
                res['LOAI_HOAT_DONG_NHAP_XUAT'] = int(child.text)
            elif child.tag == 'ActionDetail':
                res['HOAT_DONG_CHI_TIET'] = int(child.text)
            elif child.tag == 'AmountStockAfterActionMainUnit':
                res['GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH'] = float(child.text)
            elif child.tag == 'PriceOutwardStockMainUnit':
                res['DON_GIA_XUAT_KHO_THEO_DVT_CHINH'] = float(child.text)
            elif child.tag == 'ActionRowOnMaterial':
                res['HANH_DONG_TREN_VAT_TU'] = int(child.text)
            elif child.tag == 'IsCaculateByStock':
                res['IsCaculateByStock'] = True if child.text == '1' else False

            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


        #  # Tính giá xuất kho tức thời không  theo kho
    def _import_InventoryItemPriceOutwardImmeNoStock(self, tag):
        rec_model = 'stock.ex.tinh.gia.xuat.kho.tuc.thoi.khong.theo.kho'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ID_Action':
                rec_id = child.text.lower()
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['MA_HANG_ID'] = rid.id
            elif child.tag == 'UnitID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['MA_DON_VI_TINH_ID'] = rid.id
            elif child.tag == 'MainUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['MA_DON_VI_TINH_CHINH_ID'] = rid.id
            elif child.tag == 'ExchangeRateOperator':
                if child.text=='*':
                    res['TOAN_TU_QUY_DOI'] = 'NHAN'
                elif child.text=='/':
                    res['TOAN_TU_QUY_DOI'] = 'CHIA'

            elif child.tag == 'ConvertRate':
                res['TY_LE_CHUYEN_DOI'] = float(child.text)

            elif child.tag == 'DateTimeAction':
                res['THOI_GIAN_HOAT_DONG'] = child.text
            elif child.tag == 'Quantity':
                res['SO_LUONG_VAT_TU'] = float(child.text)
            elif child.tag == 'PriceRow':
                res['DON_GIA_DONG'] = float(child.text)
            elif child.tag == 'AmountRow':
                res['THANH_TIEN_DONG'] = child.text
            elif child.tag == 'QuantityMainUnit':
                res['SO_LUONG_THEO_DVT_CHINH'] = float(child.text)
            elif child.tag == 'PriceMainUnit':
                res['DON_GIA_THEO_DVT_CHINH'] = float(child.text)
            elif child.tag == 'AmountRowMainUnit':
                res['THANH_TIEN_DONG_DVT_CHINH'] = float(child.text)
            elif child.tag == 'RemainQuantityMainUnit':
                res['SO_LUONG_TON_THEO_DVT_CHINH'] = float(child.text)

            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'SortOrder':
                res['STT'] = int(child.text)
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
            
            elif child.tag == 'IsUnUpdateOutwardPrice':
                res['KHONG_CAP_NHAT_GIA_XUAT'] = True if child.text == '1' else False
            elif child.tag == 'AssemblyRefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['LAP_RAP_THAO_DO_ID'] = rid.id
            elif child.tag == 'IsNeedUpdatePrice':
                res['KHONG_CAN_CAP_NHAT_GIA_XUAT'] = True if child.text == '1' else False
            elif child.tag == 'LastTimeUpdatePrice':
                res['THOI_GIAN_CAP_NHAT_GIA_XUAT_GAN_NHAT'] = child.text
            elif child.tag == 'UnitPriceMethod':
                res['PHAN_BIET_GIA'] = int(child.text)
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
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'AccumQuantityMainUnit':
                res['SO_LUONG_TON_THUC_TE_THEO_DVT_CHINH'] = float(child.text)
            elif child.tag == 'AccumAmountStock':
                res['TONG_GIA_TRI_LUY_KE_KHO'] = float(child.text)
            
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['ID_CHUNG_TU'] = rid.id
                    res['MODEL_CHUNG_TU'] = rid._name
            elif child.tag == 'RefDetailID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['ID_CHUNG_TU_CHI_TIET'] = rid.id
                    res['MODEL_CHUNG_TU_TIET'] = rid._name
            elif child.tag == 'TypeActionInOut':
                res['LOAI_HOAT_DONG_NHAP_XUAT'] = int(child.text)
            elif child.tag == 'ActionDetail':
                res['HOAT_DONG_CHI_TIET'] = int(child.text)
            elif child.tag == 'AmountStockAfterActionMainUnit':
                res['GIA_TRI_KHO_SAU_HOAT_DONG_THEO_DVT_CHINH'] = float(child.text)
            elif child.tag == 'PriceOutwardStockMainUnit':
                res['DON_GIA_XUAT_KHO_THEO_DVT_CHINH'] = float(child.text)
            elif child.tag == 'ActionRowOnMaterial':
                res['HANH_DONG_TREN_VAT_TU'] = int(child.text)
            elif child.tag == 'IsCaculateByStock':
                res['IsCaculateByStock'] = True if child.text == '1' else False


            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    #Tính giá xuất kho ghi log

    def _import_InventoryItemCalculatePriceErrors(self, tag):
        rec_model = 'stock.ex.tinh.gia.von.ghi.log'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ErrorID':
                rec_id = child.text
            elif child.tag == 'InventoryItemID':
                if child.text:
                    rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)               
                    if rid:
                        res['VAT_TU_HANG_HOA_ID'] = rid.id
            elif child.tag == 'StockID':
                if child.text:
                    rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                    if rid:
                        res['KHO_ID'] = rid.id
            elif child.tag == 'ActionRowOnMaterial':
                res['HANH_DONG'] = int(child.text)
            elif child.tag == 'ErrorMessage':
                res['LOI'] = child.text
            elif child.tag == 'Datetime_act':
                res['THOI_GIAN'] = child.text  
            elif child.tag == 'CalculatePriceMethod':
                res['PHUONG_PHAP_TINH_GIA'] = child.text       
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


 #log unpost vật tư hàng hóa

    def _import_InventoryItemLogUnPost(self, tag):
        rec_model = 'stock.ex.log.unpost.vat.tu.hang.hoa'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'LogID':
                rec_id = child.text
            elif child.tag == 'InventoryItemID':
                if child.text:
                    rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)               
                    if rid:
                        res['VAT_TU_HANG_HOA_ID'] = rid.id
            elif child.tag == 'BranchID':
                if child.text:
                    rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                    if rid:
                        res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'DatetimeAction':
                res['THOI_GIAN_THUC_HIEN'] = child.text  
            elif child.tag == 'ActionTypeID':
                res['LOAI_HANH_DONG'] = child.text 
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['ID_CHUNG_TU'] = rid.id
                    res['MODEL_CHUNG_TU'] = rid._name
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = child.text  
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text 
            elif child.tag == 'INRefOrder':
                res['SO_THU_TU_CHUNG_TU'] = int(child.text) 
            elif child.tag == 'RefDetailID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['ID_CHUNG_TU_CHI_TIET'] = rid.id
                    res['MODEL_CHUNG_TU_CHI_TIET'] = rid._name 
            elif child.tag == 'RefNo':
                res['SO_CHUNG_TU'] = child.text       
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)







    # # Bảng lưu mã quy cách để v02
    # def _import_INAuditMemberDetail(self, tag):
    #     rec_model = 'stock.ex.chung.tu.luu.ma.quy.cach'
    #     res = {}
    #     rec_id = False
    #     for child in tag.getchildren():
    #         if child.tag == 'RefID':
    #             rec_id = child.text
    #         elif child.tag == 'RefDetailID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
    #             if rid:
    #                 res['CHI_TIET_ID'] = rid.id
    #         elif child.tag == 'RefType':
    #             res['LOAI_CHUNG_TU'] = int(child.text)
            
    #         elif child.tag == 'PostedDate':
    #             res['NGAY_HACH_TOAN'] = child.text
    #         elif child.tag == 'RefNoFinance':
    #             res['SO_CHUNG_TU'] =child.text
    #         elif child.tag == 'InwardStockID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
    #             if rid:
    #                 res['KHO_NHAP'] = rid.id
    #         elif child.tag == 'InventoryItemID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
    #             if rid:
    #                 res['VAT_TU_HANG_HOA_ID'] = rid.id
    #     return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    
