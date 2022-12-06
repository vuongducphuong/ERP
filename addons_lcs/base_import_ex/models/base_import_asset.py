from odoo import api, fields, models, helper

MODULE = 'base_import_ex'
class Import(models.TransientModel):
    _inherit = 'base_import_ex.import'
    
    # Ghi tăng tài sản cố định
    def _import_FixedAsset(self, tag):
        rec_model = 'asset.ghi.tang'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'FixedAssetID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefNo':
                res['SO_CT_GHI_TANG'] = child.text
                if child.text == 'OPN':
                    res['KHAI_BAO_DAU_KY'] = True
            elif child.tag == 'RefDate':
                res['NGAY_GHI_TANG'] = child.text
            elif child.tag == 'FixedAssetCode':
                res['MA_TAI_SAN'] = child.text
            elif child.tag == 'FixedAssetName':
                res['TEN_TAI_SAN'] = child.text

            elif child.tag == 'FixedAssetCategoryID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['LOAI_TAI_SAN_ID'] = rid.id
            elif child.tag == 'GuaranteeDuration':
                res['THOI_GIAN_BAO_HANH'] = child.text
            elif child.tag == 'GuaranteeCondition':
                res['DIEU_KIEN_BAO_HANH'] = child.text
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'VendorName':
                res['TEN_NCC'] = child.text
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_SU_DUNG_ID'] = rid.id
            elif child.tag == 'Manufacturer':
                res['NHA_SAN_XUAT'] = child.text
            elif child.tag == 'ProductionYear':
                res['NAM_SAN_XUAT'] = float(child.text)
            elif child.tag == 'SerialNumber':
                res['SO_HIEU'] = child.text
            elif child.tag == 'MadeIn':
                res['NUOC_SAN_XUAT'] = child.text
            elif child.tag == 'CapacityMachine':
                res['CONG_SUAT'] = child.text
            elif child.tag == 'OrgPriceAccount':
                sid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if sid:
                    res['TK_NGUYEN_GIA_ID'] = sid.id
            elif child.tag == 'DepreciationAccount':
                sid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if sid:
                    res['TK_KHAU_HAO_ID'] = sid.id
            elif child.tag == 'OrgPrice':
                res['NGUYEN_GIA'] = float(child.text)
            elif child.tag == 'DepreciationAmount':
                res['GIA_TRI_TINH_KHAU_HAO'] = float(child.text)
            elif child.tag == 'DepreciationDate':
                res['NGAY_BAT_DAU_TINH_KH'] = child.text
            elif child.tag == 'DepreciationRateMonth':
                res['TY_LE_TINH_KHAU_HAO_THANG'] = child.text
            elif child.tag == 'DepreciationRateYear':
                res['TY_LE_TINH_KHAU_HAO_NAM'] = child.text
            elif child.tag == 'MonthlyDepreciationAmount':
                res['GIA_TRI_TINH_KHAU_HAO_THANG'] = child.text
            elif child.tag == 'YearlyDepreciationAmount':
                res['GIA_TRI_KHAU_HAO_NAM'] = child.text
            elif child.tag == 'RemainingAmount':
                res['GIA_TRI_CON_LAI'] = child.text
            elif child.tag == 'DeliveryRecordDate':
                res['NGAY'] = child.text
            elif child.tag == 'DeliveryRecordNo':
                res['BB_GIAO_NHAN_SO'] = child.text


            elif child.tag == 'LifeTimeUnit':
                res['THOI_GIAN_SU_DUNG'] = child.text
            elif child.tag == 'LifeTimeRemainingUnit':
                res['DVT_THOI_GIAN_SU_DUNG_CON_LAI'] = child.text

            elif child.tag == 'LifeTime':
                res['SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC'] = float(child.text)
            elif child.tag == 'LifeTimeInMonth':
                res['SO_THOI_GIAN_SU_DUNG'] = float(child.text)
            elif child.tag == 'AccumDepreciationAmount':
                res['HAO_MON_LUY_KE'] = float(child.text)
            elif child.tag == 'DepreciationAmountByIncomeTax':
                res['GIA_TRI_TINH_KH_THEO_LUAT'] = float(child.text)
            elif child.tag == 'MonthlyDepreciationAmountByIncomeTax':
                res['GIA_TRI_KH_THANG_THEO_LUAT'] = float(child.text)
            elif child.tag =='IsLimitDepreciationAmount':
                res['GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN'] = True if child.text == 'true' else False
            elif child.tag =='IsNotDepreciation':
                res['KHONG_TINH_KHAU_HAO'] = True if child.text == 'true' else False
            
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'LifeTimeRemainingInMonth':
                res['THOI_GIAN_SU_DUNG_CON_LAI'] = float(child.text)
            elif child.tag == 'LifeTimeRemaining':
                res['THOI_GIAN_SU_DUNG_CON_LAI_NGUYEN_GOC'] = float(child.text)
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] =int(child.text)
            
            elif child.tag == 'State':
                res['TINH_TRANG_GHI_TANG'] = child.text
            elif child.tag == 'Quality':
                res['CHAT_LUONG_HIEN_THOI'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # Ghi tăng tài sản cố định
    def _import_FixedAssetOpening(self, tag):
        rec_model = 'asset.ghi.tang'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'FixedAssetID':
                rec_id = child.text
            elif child.tag == 'RefNo':
                res['SO_CT_GHI_TANG'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_GHI_TANG'] = child.text
            elif child.tag == 'FixedAssetCode':
                res['MA_TAI_SAN'] = child.text
            elif child.tag == 'FixedAssetName':
                res['TEN_TAI_SAN'] = child.text

            elif child.tag == 'FixedAssetCategoryID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['LOAI_TAI_SAN_ID'] = rid.id
            elif child.tag == 'GuaranteeDuration':
                res['THOI_GIAN_BAO_HANH'] = child.text
            elif child.tag == 'GuaranteeCondition':
                res['DIEU_KIEN_BAO_HANH'] = child.text
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'VendorName':
                res['TEN_NCC'] = child.text
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_SU_DUNG_ID'] = rid.id
            elif child.tag == 'Manufacturer':
                res['NHA_SAN_XUAT'] = child.text
            elif child.tag == 'ProductionYear':
                res['NAM_SAN_XUAT'] = float(child.text)
            elif child.tag == 'SerialNumber':
                res['SO_HIEU'] = child.text
            elif child.tag == 'MadeIn':
                res['NUOC_SAN_XUAT'] = child.text
            elif child.tag == 'CapacityMachine':
                res['CONG_SUAT'] = child.text
            elif child.tag == 'OrgPriceAccount':
                sid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if sid:
                    res['TK_NGUYEN_GIA_ID'] = sid.id
            elif child.tag == 'DepreciationAccount':
                sid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if sid:
                    res['TK_KHAU_HAO_ID'] = sid.id
            elif child.tag == 'OrgPrice':
                res['NGUYEN_GIA'] = float(child.text)
            elif child.tag == 'DepreciationAmount':
                res['GIA_TRI_TINH_KHAU_HAO'] = float(child.text)
            elif child.tag == 'DepreciationDate':
                res['NGAY_BAT_DAU_TINH_KH'] = child.text
            elif child.tag == 'DepreciationRateMonth':
                res['TY_LE_TINH_KHAU_HAO_THANG'] = child.text
            elif child.tag == 'DepreciationRateYear':
                res['TY_LE_TINH_KHAU_HAO_NAM'] = child.text
            elif child.tag == 'MonthlyDepreciationAmount':
                res['GIA_TRI_TINH_KHAU_HAO_THANG'] = child.text
            elif child.tag == 'YearlyDepreciationAmount':
                res['GIA_TRI_KHAU_HAO_NAM'] = child.text
            elif child.tag == 'RemainingAmount':
                res['GIA_TRI_CON_LAI'] = child.text
            elif child.tag == 'DeliveryRecordDate':
                res['NGAY'] = child.text
            elif child.tag == 'DeliveryRecordNo':
                res['BB_GIAO_NHAN_SO'] = child.text


            elif child.tag == 'LifeTimeUnit':
                res['THOI_GIAN_SU_DUNG'] = child.text
            elif child.tag == 'LifeTimeRemainingUnit':
                res['DVT_THOI_GIAN_SU_DUNG_CON_LAI'] = child.text

            elif child.tag == 'LifeTime':
                res['SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC'] = float(child.text)
            elif child.tag == 'LifeTimeInMonth':
                res['SO_THOI_GIAN_SU_DUNG'] = float(child.text)
            elif child.tag == 'LifeTimeRemainingInMonth':
                res['THOI_GIAN_SU_DUNG_CON_LAI'] = float(child.text)
            elif child.tag == 'LifeTimeRemaining':
                res['THOI_GIAN_SU_DUNG_CON_LAI_NGUYEN_GOC'] = float(child.text)
            elif child.tag == 'AccumDepreciationAmount':
                res['HAO_MON_LUY_KE'] = float(child.text)
            elif child.tag == 'DepreciationAmountByIncomeTax':
                res['GIA_TRI_TINH_KH_THEO_LUAT'] = float(child.text)
            elif child.tag == 'MonthlyDepreciationAmountByIncomeTax':
                res['GIA_TRI_KH_THANG_THEO_LUAT'] = float(child.text)
            elif child.tag =='IsLimitDepreciationAmount':
                res['GH_GIA_TRI_TINH_KH_THEO_LUAT_THUE_TNDN'] = True if child.text == 'true' else False
            elif child.tag =='IsNotDepreciation':
                res['KHONG_TINH_KHAU_HAO'] = True if child.text == 'true' else False
            
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] =int(child.text)
            
            elif child.tag == 'State':
                res['TINH_TRANG_GHI_TANG'] = child.text
            elif child.tag == 'Quality':
                res['CHAT_LUONG_HIEN_THOI'] = child.text
            res['KHAI_BAO_DAU_KY'] = True
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # thiết lập phân bổ
    def _import_FixedAssetDetailAllocation(self, tag):
        rec_model = 'asset.ghi.tang.thiet.lap.phan.bo'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'FixedAssetDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'FixedAssetID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['TAI_SAN_CO_DINH_GHI_TANG_ID'] = rid.id


            elif child.tag == 'ObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:                    
                    if rid._name == 'danh.muc.doi.tuong.tap.hop.chi.phi':
                        res['DOI_TUONG_PHAN_BO_ID'] = rid._name +  ',Đối tượng THCP,' + str(rid.id)
                    elif rid._name == 'danh.muc.cong.trinh':
                        res['DOI_TUONG_PHAN_BO_ID'] = rid._name +   ',Công trình,' + str(rid.id)
                    elif rid._name == 'account.ex.don.dat.hang':
                        res['DOI_TUONG_PHAN_BO_ID'] = rid._name +   ',Đơn hàng,' + str(rid.id)
                    elif rid._name == 'sale.ex.hop.dong.ban':
                        res['DOI_TUONG_PHAN_BO_ID'] = rid._name +   ',Hợp đồng,' + str(rid.id)
                    elif rid._name == 'danh.muc.to.chuc':
                        res['DOI_TUONG_PHAN_BO_ID'] = rid._name +   ',Đơn vị,' + str(rid.id)

            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id
            elif child.tag == 'AllocationRate':
                res['TY_LE_PB'] = float(child.text)
            elif child.tag == 'CostAccount':
                sid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if sid:
                    res['TK_NO_ID'] = sid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


# nguồn gốc hình thành 
    def _import_FixedAssetDetailSource(self, tag):
        rec_model = 'asset.ghi.tang.nguon.goc.hinh.thanh'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'FixedAssetDetailID':
                rec_id = child.text
            elif child.tag == 'FixedAssetID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['TAI_SAN_CO_DINH_GHI_TANG_ID'] = rid.id
            elif child.tag == 'Amount':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'DebitAccount':
                rid=self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id
            elif child.tag == 'CreditAccount':
                rid=self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] =int(child.text)
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'SortOrder':
                res['THU_TU_SAP_XEP_CHI_TIET'] =int(child.text)
            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
#bộ phận cấu thành 

    def _import_FixedAssetDetail(self, tag):
        rec_model = 'asset.ghi.tang.bo.phan.cau.thanh'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'FixedAssetDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'FixedAssetID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['TAI_SAN_CO_DINH_GHI_TANG_ID'] = rid.id
            elif child.tag == 'Description':
                    res['BO_PHAN'] = child.text
            elif child.tag == 'Unit':
                    res['DON_VI_TINH'] = child.text
            elif child.tag == 'Quantity':
                    res['SO_LUONG'] = float(child.text)
            elif child.tag == 'WarrantyTime':
                    res['THOI_HAN_BAO_HANH'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    
    # dụng cụ, phụ tùng kèm theo
    def _import_FixedAssetDetailAccessory(self, tag):
        rec_model = 'asset.ghi.tang.dung.cu.phu.tung'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'FixedAssetDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'FixedAssetID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['TAI_SAN_CO_DINH_GHI_TANG_ID'] = rid.id
            elif child.tag == 'Description':
                    res['TEN_QUY_CACH_DUNG_CU_PHU_TUNG'] = child.text
            elif child.tag == 'Unit':
                    res['DON_VI_TINH'] = child.text
            elif child.tag == 'Quantity':
                    res['SO_LUONG'] = float(child.text)
            elif child.tag == 'Amount':
                    res['GIA_TRI'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


     # #  # kiểm kê tài sản cố định
    def _import_FAAudit(self, tag):
        rec_model = 'asset.kiem.ke'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefDate':
                res['NGAY'] = child.text
            elif child.tag == 'InventoryDate':
                res['KIEM_KE_DEN_NGAY_TSCD'] = child.text
            elif child.tag == 'RefNo':
                res['SO'] = child.text
            elif child.tag == 'JournalMemo':
                res['MUC_DICH'] = child.text
            elif child.tag == 'Summary':
                res['KET_LUAN'] = child.text
            
            elif child.tag == 'IsExecuted':
                res['DA_XU_LY_KIEN_DINH'] = True if child.text == 'true' else False
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # #kiểm kê tài sản cố định chi tiết
    def _import_FAAuditDetail(self, tag):
        rec_model = 'asset.kiem.ke.tai.san'
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
                    res['KIEM_KE_TAI_SAN_CO_DINH_ID'] = rid.id
            elif child.tag == 'FixedAssetID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_TAI_SAN'] = rid.id
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_SU_DUNG_ID'] = rid.id
            elif child.tag == 'OrgPrice':
                res['NGUYEN_GIA'] = float(child.text)
            elif child.tag == 'DepreciationAmount':
                res['GIA_TRI_TINH_KHAU_HAO'] = float(child.text)
            elif child.tag == 'AccumDepreciationAmount':
                res['HAO_MON_LUY_KE'] = float(child.text)  
            elif child.tag == 'RemainingAmount':
                res['GIA_TRI_CON_LAI'] = float(child.text)
            elif child.tag == 'ExistInStock':
                res['TON_TAI'] = child.text   
            elif child.tag == 'Quality':
                res['CHAT_LUONG_HIEN_THOI'] = child.text   
            elif child.tag == 'Note':
                res['GHI_CHU'] =child.text
            elif child.tag == 'Recommendation':
                res['KIEN_NGHI_XU_LY'] =child.text       
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # kiểm kê tài sản chi tiet(thanh vien tham gia)
    def _import_FAAuditMemberDetail(self, tag):
        rec_model = 'asset.kiem.ke.thanh.vien.tham.gia'
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
                    res['KIEM_KE_TAI_SAN_CO_DINH_ID'] = rid.id
            
            elif child.tag == 'AccountObjectName':
                res['HO_TEN'] = child.text
            elif child.tag == 'Position':
                res['CHUC_DANH'] =child.text
            elif child.tag == 'Representative':
                res['DAI_DIEN'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)



    # # khấu hao tài sản cố định
    def _import_FADepreciation(self, tag):
        rec_model = 'asset.tinh.khau.hao'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'RefNo':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'Month':
                res['THANG'] = int(child.text)
            elif child.tag == 'Year':
                res['NAM'] = int(child.text)
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] =int(child.text)
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'IsPostedFinance':
                if child.text == 'true':
                    res['state'] = 'da_ghi_so'
                else:
                    res['state'] = 'chua_ghi_so'
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # khấu hao tài sản chi tiet(tính khấu hao)
    def _import_FADepreciationDetail(self, tag):
        rec_model = 'asset.tinh.khau.hao.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['TINH_KHAU_HAO_ID'] = rid.id
            elif child.tag == 'FixedAssetID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_TAI_SAN_ID'] = rid.id
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_SU_DUNG_ID'] = rid.id
            elif child.tag == 'MonthlyDepreciationAmount':
                res['GIA_TRI_KH_THANG'] = float(child.text)
            elif child.tag == 'AmountResonableCost':
                res['GIA_TRI_TINH_VAO_CP_HOP_LY'] = float(child.text)
            elif child.tag == 'AmountUnResonableCost':
                res['GIA_TRI_TINH_VAO_CP_KHONG_HOP_LY'] = float(child.text)  
            elif child.tag == 'SortOrder':
                res['sequence'] = int(child.text)  
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # khấu hao tài sản chi tiet(phân bổ)
    def _import_FADepreciationDetailAllocation(self, tag):
        rec_model = 'asset.tinh.khau.hao.phan.bo'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['TINH_KHAU_HAO_ID'] = rid.id
            elif child.tag == 'FixedAssetID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_TAI_SAN_ID'] = rid.id
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_SU_DUNG_ID'] = rid.id
            elif child.tag == 'MonthlyDepreciationAmount':
                res['GIA_TRI_KH_THANG'] = float(child.text)


            elif child.tag == 'AllocationObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:                    
                    if rid._name == 'danh.muc.doi.tuong.tap.hop.chi.phi':
                        res['DOI_TUONG_PHAN_BO_ID'] = rid._name +  ',Đối tượng THCP,' + str(rid.id)
                    elif rid._name == 'danh.muc.cong.trinh':
                        res['DOI_TUONG_PHAN_BO_ID'] = rid._name +   ',Công trình,' + str(rid.id)
                    elif rid._name == 'account.ex.don.dat.hang':
                        res['DOI_TUONG_PHAN_BO_ID'] = rid._name +   ',Đơn hàng,' + str(rid.id)
                    elif rid._name == 'sale.ex.hop.dong.ban':
                        res['DOI_TUONG_PHAN_BO_ID'] = rid._name +   ',Hợp đồng,' + str(rid.id)
                    elif rid._name == 'danh.muc.to.chuc':
                        res['DOI_TUONG_PHAN_BO_ID'] = rid._name +   ',Đơn vị,' + str(rid.id)

            elif child.tag == 'AllocationRate':
                res['TY_LE'] = float(child.text)
            elif child.tag == 'AllocationAmount':
                res['CHI_PHI_PHAN_BO'] = float(child.text)
            elif child.tag == 'CostAccount':
                res['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id 
            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id  
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id  
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # khấu hao tài sản cố định chi tiet(hạch toán)
    def _import_FADepreciationDetailPost(self, tag):
        rec_model = 'asset.tinh.khau.hao.hach.toan'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['TINH_KHAU_HAO_ID'] = rid.id
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text

            elif child.tag == 'DebitAccount':
                rid=self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id
            elif child.tag == 'CreditAccount':
                rid=self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id
            elif child.tag == 'Amount':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'DebitAccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_NO_ID'] = rid.id
            elif child.tag == 'CreditAccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_CO_ID'] = rid.id

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
            elif child.tag == 'UnResonableCost':
                res['CP_KHONG_HOP_LY'] = True if child.text == 'true' else False
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # # Điều chuyển tài sản cố định
    def _import_FATransfer(self, tag):
        rec_model = 'asset.dieu.chuyen'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefDate':
                res['NGAY'] = child.text
            elif child.tag == 'RefNo':
                res['BIEN_BAN_GIAO_NHAN_SO'] = child.text
            elif child.tag == 'HandOverName':
                res['NGUOI_BAN_GIAO'] = child.text
            elif child.tag == 'RecipientName':
                res['NGUOI_TIEP_NHAN'] = child.text
            elif child.tag == 'JournalMemo':
                res['LY_DO_DIEU_CHUYEN'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH'] = rid.id
            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # Điều chuyển tài sản cố định chi tiet
    def _import_FATransferDetail(self, tag):
        rec_model = 'asset.dieu.chuyen.chi.tiet'
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
                    res['DIEU_CHUYEN_TAI_KHOAN_CO_DINH_ID'] = rid.id
            elif child.tag == 'FixedAssetID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_TAI_SAN_ID'] = rid.id
            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id
            elif child.tag == 'ProjectWorkID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CONG_TRINH_ID'] = rid.id
            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_THCP_ID'] = rid.id

            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id

            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id
            elif child.tag == 'CostAccount':
                res['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id 
            elif child.tag == 'FromOrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['TU_DON_VI'] = rid.id
            elif child.tag == 'ToOrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DEN_DON_VI_ID'] = rid.id
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)



     # Ghi giảm tài sản cố định
    def _import_FADecrement(self, tag):
        rec_model = 'asset.ghi.giam'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] =int(child.text)
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'RefNo':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['LY_DO_GIAM'] = helper.Obj.convert_to_key(child.text)
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Ghi giảm tài sản cố định chi tiết(tài sản)
    def _import_FADecrementDetail(self, tag):
        rec_model = 'asset.ghi.giam.tai.san'
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
                    res['TAI_SAN_CO_DINH_GHI_GIAM_ID'] = rid.id
            elif child.tag == 'FixedAssetID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_TAI_SAN'] = rid.id
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_SU_DUNG_ID'] = rid.id
            elif child.tag == 'OrgPrice':
                res['NGUYEN_GIA'] = float(child.text)
            elif child.tag == 'DepreciationAmount':
                res['GIA_TRI_TINH_KHAU_HAO'] = float(child.text)

            elif child.tag == 'AccumDepreciationAmount':
                res['HAO_MON_LUY_KE'] = float(child.text) 
            elif child.tag == 'RemainingAmount':
                res['GIA_TRI_CON_LAI'] = float(child.text)  
            
            elif child.tag == 'OrgPriceAccount':
                rid= self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NGUYEN_GIA_ID'] = rid.id
            elif child.tag == 'DepreciationAccount':
                rid= self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_HAO_MON_ID'] = rid.id
            elif child.tag == 'RemainingAccount':
                rid= self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_XU_LY_GIA_TRI_CON_LAI_ID'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Ghi giảm tài sản cố định chi tiết(hạch toán)
    def _import_FADecrementDetailPost(self, tag):
        rec_model = 'asset.ghi.giam.hach.toan'
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
                    res['TAI_SAN_CO_DINH_GHI_GIAM_ID'] = rid.id
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'ProjectWorkID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CONG_TRINH_ID'] = rid.id
            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_THCP_ID'] = rid.id

            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id

            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_ID'] = rid.id
            
            
            elif child.tag == 'DebitAccount':
                rid= self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id
            elif child.tag == 'CreditAccount':
                rid= self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id
            elif child.tag =='UnResonableCost':
                res['CP_KHONG_HOP_LY'] = True if child.text == 'true' else False
            elif child.tag == 'Amount':
                res['SO_TIEN'] = float(child.text) 
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # # đánh giá lại tài sản cố định
    def _import_FAAdjustment(self, tag):
        rec_model = 'asset.danh.gia.lai'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'DecisionDate':
                res['NGAY'] = child.text
            elif child.tag == 'DecisionNo':
                res['BIEN_BAN_SO'] = child.text
            elif child.tag == 'JournalMemo':
                res['KET_LUAN'] = child.text
            
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'RefNo':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'Reason':
                res['LY_DO'] = helper.Obj.convert_to_key(child.text)
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] =int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # đánh giá lại tài sản cố đimh chi tiet(chi tiet dieu chinh)
    def _import_FAAdjustmentDetail(self, tag):
        rec_model = 'asset.danh.gia.lai.chi.tiet.dieu.chinh'
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
                    res['DANH_GIA_LAI_TAI_SAN_CO_DINH_CHI_TIET_ID'] = rid.id
            elif child.tag == 'FixedAssetID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_TAI_SAN_ID'] = rid.id
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_SU_DUNG'] = rid.id
            elif child.tag == 'CurrentRemainingAmount':
                res['GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH'] = float(child.text)
            elif child.tag == 'NewRemainingAmount':
                res['GIA_TRI_CON_LAI_SAU_DIEU_CHINH'] = float(child.text)

            elif child.tag == 'DiffRemainingAmount':
                res['CHENH_LECH_GIA_TRI'] = float(child.text)

            elif child.tag == 'CurrentLifeTime':
                res['THOI_GIAN_CON_LAI_TRUOC_DIEU_CHINH'] = float(child.text)
            elif child.tag == 'NewLifeTime':
                res['THOI_GIAN_CON_LAI_SAU_DIEU_CHINH'] = float(child.text)

            elif child.tag == 'DiffLifeTime':
                res['CHENH_LECH_THOI_GIAN'] = float(child.text)

            elif child.tag == 'CurrentAccumDepreciationAmount':
                res['HAO_MON_LUY_KE_TRUOC_DIEU_CHINH'] = float(child.text)
            elif child.tag == 'NewAccumDepreciationAmount':
                res['HAO_MON_LUY_KE_SAU_DIEU_CHINH'] = float(child.text)
            elif child.tag == 'DiffAccumDepreciationAmount':
                res['CHENH_LECH_HAO_MON_LUY_KE'] = float(child.text)
            elif child.tag == 'CurrentDepreciationAmount':
                res['GIA_TRI_KHAU_HAO_TRUOC_DIEU_CHINH'] = float(child.text)
            elif child.tag == 'NewDepreciationAmount':
                res['GIA_TRI_KHAU_HAO_SAU_DIEU_CHINH'] = float(child.text)
            elif child.tag == 'DiffDepreciationAmount':
                res['CHENH_LECH_GTKH'] = float(child.text)

            elif child.tag == 'NewMonthlyDepreciationAmount':
                res['GTKH_THANG_SAU_DIEU_CHINH'] = float(child.text)
            elif child.tag == 'NewMonthlyDepreciationAmountByIncomeTax':
                res['GTKH_THANG_THEO_LUAT_SAU_DIEU_CHINH'] = float(child.text)

            

            elif child.tag == 'AdjustmentAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_DANH_GIA_LAI_GTKH'] = rid.id 
            elif child.tag == 'CostAccount':
                sid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if sid:
                    res['TK_CHI_PHI_HAO_MON_LUY_KE'] = sid.id
            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # đánh giá lại tài sản cố định chi tiết(hạch toán)
    def _import_FAAdjustmentDetailPost(self, tag):
        rec_model = 'asset.danh.gia.lai.hach.toan'
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
                    res['DANH_GIA_LAI_TAI_SAN_CO_DINH_ID'] = rid.id
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'Amount':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id
            elif child.tag == 'AccountObjectID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_ID'] = rid.id
            elif child.tag == 'ProjectWorkID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CONG_TRINH_ID'] = rid.id
            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DOI_TUONG_THCP_ID'] = rid.id

            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id

            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_ID'] = rid.id
            
            
            elif child.tag == 'DebitAccount':
                rid= self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id
            elif child.tag == 'CreditAccount':
                rid= self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id
            elif child.tag =='UnResonableCost':
                res['CP_KHONG_HOP_LY'] = True if child.text == 'true' else False
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # def _import_FixedAssetLedger(self, tag):
    #     rec_model = 'so.tscd.chi.tiet'
    #     res = {}
    #     rec_id = False
    #     for child in tag.getchildren():
    #         if child.tag == 'FixedAssetLedgerID':
    #             rec_id = child.text

    #         elif child.tag == 'LifeTimeInMonth':
    #             res['THOI_GIAN_SU_DUNG'] = float(child.text)
    #         elif child.tag == 'LifeTimeRemainingInMonth':
    #             res['THOI_GIAN_SU_DUNG_CON_LAI'] = float(child.text)
    #         elif child.tag == 'DepreciationRateMonth':
    #             res['TY_LE_KHAU_HAO_THANG'] = float(child.text)
    #         elif child.tag == 'MonthlyDepreciationAmount':
    #             res['GIA_TRI_KHAU_HAO_THANG'] = float(child.text)
    #         elif child.tag == 'DepreciationAmount':
    #             res['GIA_TRI_TINH_KHAU_HAO'] = float(child.text)
    #         elif child.tag == 'AccumDepreciationAmount':
    #             res['GIA_TRI_HAO_MON_LUY_KE'] = float(child.text)
    #         elif child.tag == 'RemainingAmount':
    #             res['GIA_TRI_CON_LAI'] = float(child.text)
    #         elif child.tag == 'OrgPrice':
    #             res['NGUYEN_GIA'] = float(child.text)
    #         elif child.tag == 'SumDiffLifeTime':
    #             res['CHENH_LECH_THOI_GIAN_SU_DUNG'] = float(child.text)
    #         elif child.tag == 'SumDiffRemainingAmount':
    #             res['CHENH_LECH_GIA_TRI_CON_LAI'] = float(child.text)
    #         elif child.tag == 'DiffDepreciationAmount':
    #             res['CHENH_LECH_GIA_TRI_TINH_KHAU_HAO'] = float(child.text)
    #         elif child.tag == 'DiffAccumDepreciationAmount':
    #             res['CHENH_LECH_GIA_TRI_HAO_MON_LUY_KE'] = float(child.text)
    #         elif child.tag == 'DiffOrgPriceAmount':
    #             res['CHENH_LECH_NGUYEN_GIA'] = float(child.text)
    #         elif child.tag == 'RefOrderInSubSystem':
    #             res['THU_TU_NGHIEP_VU'] = float(child.text)
    #         elif child.tag == 'MonthlyDepreciationAmountByIncomeTax':
    #             res['GIA_TRI_KH_THANG_THEO_LUAT'] = float(child.text)
    #         elif child.tag == 'MonthlyDepreciationAmountOnDepreciation':
    #             res['GIA_TRI_KHAU_HAO_THANG_KHI_KH'] = float(child.text)
    #         elif child.tag == 'RefType':
    #             res['LOAI_CHUNG_TU'] =int(child.text)

    #         elif child.tag == 'RefNo':
    #             res['SO_CHUNG_TU'] = child.text
    #         elif child.tag == 'FixedAssetCode':
    #             res['MA_TSCD'] = child.text
    #         elif child.tag == 'FixedAssetName':
    #             res['TEN_TSCD'] = child.text
    #         elif child.tag == 'RefDate':
    #             res['NGAY_CHUNG_TU'] =child.text
    #         elif child.tag == 'PostedDate':
    #             res['NGAY_HACH_TOAN'] = child.text
    #         elif child.tag == 'FixedAssetID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
    #             if rid:
    #                 res['TSCD_ID'] = rid.id
    #         elif child.tag == 'OrganizationUnitID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
    #             if rid:
    #                 res['DON_VI_SU_DUNG_ID'] = rid.id
    #         elif child.tag == 'BranchID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
    #             if rid:
    #                 res['CHI_NHANH_ID'] = rid.id
    #         elif child.tag == 'FixedAssetCategoryID':
    #             rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
    #             if rid:
    #                 res['LOAI_TSCD_ID'] = rid.id
    #         elif child.tag == 'DepreciationAccount':
    #             sid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
    #             if sid:
    #                 res['TK_HAO_MON_ID'] = sid.id
    #         elif child.tag == 'OrgPriceAccount':
    #             sid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
    #             if sid:
    #                 res['TK_NGUYEN_GIA_ID'] = sid.id

    #         elif child.tag == 'JournalMemo':
    #             res['DIEN_GIAI_CHUNG'] = child.text
    #         res['ID_CHUNG_TU'] = 1
    #         res['MODEL_CHUNG_TU'] = 'cho.thue.tscd'
            
    #     return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

