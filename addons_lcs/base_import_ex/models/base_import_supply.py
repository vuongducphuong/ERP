from odoo import api, fields, models, helper

MODULE = 'base_import_ex'
class Import(models.TransientModel):
    _inherit = 'base_import_ex.import'
    
    # Ghi tăng công cụ dụng cụ
    def _import_SUIncrement(self, tag):
        rec_model = 'supply.ghi.tang'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'SupplyID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefDate':
                res['NGAY_GHI_TANG'] = child.text
            elif child.tag == 'SupplyCode':
                res['MA_CCDC'] = child.text
            elif child.tag == 'SupplyName':
                res['TEN_CCDC'] = child.text
            elif child.tag == 'SupplyCategoryID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['LOAI_CCDC_ID'] = rid.id
            elif child.tag == 'RefNo':
                res['SO_CT_GHI_TANG'] = child.text
                if child.text == 'OPN':
                    res['KHAI_BAO_DAU_KY'] = True
            elif child.tag == 'Unit':
                res['DON_VI_TINH'] = child.text
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'UnitPrice':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'Amount':
                res['THANH_TIEN'] = float(child.text)
            elif child.tag == 'AllocationTime':
                res['SO_KY_PHAN_BO'] = float(child.text)
            elif child.tag == 'TermlyAllocationAmount':
                res['SO_TIEN_PHAN_BO_HANG_KY'] = float(child.text)
            elif child.tag == 'SupplyGroup':
                res['NHOM_CCDC'] = child.text
            elif child.tag == 'AllocationAccount':
                sid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if sid:
                    res['TK_CHO_PHAN_BO_ID'] = sid.id
            elif child.tag == 'ReasonIncrement':
                res['LY_DO_GHI_TANG'] = child.text
            
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag =='SuspendAllocate':
                res['NGUNG_PHAN_BO'] = True if child.text == 'true' else False
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
            elif child.tag == 'RemainingAllocationTime':
                res['SO_KY_PB_CON_LAI'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # Ghi tăng công cụ dụng cụ -OPN
    def _import_SUIncrementOpening(self, tag):
        rec_model = 'supply.ghi.tang'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'SupplyID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefDate':
                res['NGAY_GHI_TANG'] = child.text
            elif child.tag == 'SupplyCode':
                res['MA_CCDC'] = child.text
            elif child.tag == 'SupplyName':
                res['TEN_CCDC'] = child.text
            elif child.tag == 'SupplyCategoryID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['LOAI_CCDC_ID'] = rid.id
            elif child.tag == 'RefNo':
                res['SO_CT_GHI_TANG'] = child.text
            elif child.tag == 'Unit':
                res['DON_VI_TINH'] = child.text
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'UnitPrice':
                res['DON_GIA'] = float(child.text)
            elif child.tag == 'Amount':
                res['THANH_TIEN'] = float(child.text)
            elif child.tag == 'AllocationTime':
                res['SO_KY_PHAN_BO'] = float(child.text)
            elif child.tag == 'TermlyAllocationAmount':
                res['SO_TIEN_PHAN_BO_HANG_KY'] = float(child.text)

            elif child.tag == 'AllocatedAmount':
                res['GIA_TRI_DA_PHAN_BO'] = float(child.text)
            elif child.tag == 'RemainingAllocationTime':
                res['SO_KY_PB_CON_LAI'] = float(child.text)

            elif child.tag == 'SupplyGroup':
                res['NHOM_CCDC'] = child.text
            elif child.tag == 'AllocationAccount':
                sid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if sid:
                    res['TK_CHO_PHAN_BO_ID'] = sid.id
            elif child.tag == 'ReasonIncrement':
                res['LY_DO_GHI_TANG'] = child.text
            
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag =='SuspendAllocate':
                res['NGUNG_PHAN_BO'] = True if child.text == 'true' else False
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
            res['KHAI_BAO_DAU_KY'] = True
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Ghi tăng ccdc-detail đơn vị sử dụng
    def _import_SUIncrementDetailDepartment(self, tag):
        rec_model = 'supply.ghi.tang.don.vi.su.dung'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'SupplyDetailID':
                rec_id = child.text
            elif child.tag == 'SupplyID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['GHI_TANG_DON_VI_SU_DUNG_ID'] = rid.id
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_DON_VI_ID'] = rid.id
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'SortOrder':
                res['sequence'] = int(child.text)
            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


        # Ghi tăng ccdc-detail thiết lập phân bổ
    def _import_SUIncrementDetailAllocation(self, tag):
        rec_model = 'supply.ghi.tang.thiet.lap.phan.bo'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'SupplyDetailID':
                rec_id = child.text
           
            elif child.tag == 'SupplyID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['GHI_TANG_THIET_LAP_PHAN_BO_ID'] = rid.id
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
            elif child.tag == 'ObjectType':
                res['LOAI_DOI_TUONG'] = child.text
            elif child.tag == 'SortOrder':
                res['THU_TU_SAP_XEP'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


     # Ghi tăng ccdc-detail mô tả chi tiết
    def _import_SUIncrementDetail(self, tag):
        rec_model = 'supply.ghi.tang.mo.ta.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'SupplyDetailID':
                rec_id = child.text
            elif child.tag == 'SupplyID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['GHI_TANG_MO_TA_CHI_TIET_ID'] = rid.id
            elif child.tag == 'Description':
                res['MO_TA'] = child.text
            elif child.tag == 'NumberNo':
                res['SO_HIEU'] = child.text
            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Điều chuyển công cụ dụng cụ
    def _import_SUTransfer(self, tag):
        rec_model = 'supply.dieu.chuyen.cong.cu.dung.cu'
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
            elif child.tag == 'DeliveryName':
                res['NGUOI_BAN_GIAO'] = child.text
            elif child.tag == 'ReceiptName':
                res['NGUOI_TIEP_NHAN'] = child.text
            elif child.tag == 'JournalMemo':
                res['LY_DO_DIEU_CHUYEN'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
            elif child.tag == 'RefOrder':
                res['STT_NHAP_CT'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # Điều chuyển công cụ dụng cụ chi tiet
    def _import_SUTransferDetail(self, tag):
        rec_model = 'supply.dieu.chuyen.chi.tiet'
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
                    res['DIEU_CHUYEN_CCDC_CHI_TIET_ID_ID'] = rid.id
            elif child.tag == 'SupplyID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_CCDC_ID'] = rid.id
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
                    res['DOI_TUONG_TONG_HOP_CHI_PHI_ID'] = rid.id

            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id

            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id
            
            elif child.tag == 'UseQuantity':
                res['SO_LUONG_DANG_DUNG'] = float(child.text)
            elif child.tag == 'TransferQuantity':
                res['SO_LUONG_DIEU_CHUYEN'] = float(child.text)
            elif child.tag == 'CostAccount':
                res['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id 
            elif child.tag == 'FromOrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['TU_DON_VI_ID'] = rid.id
            elif child.tag == 'ToOrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DEN_DON_VI_ID'] = rid.id
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
            elif child.tag == 'SortOrder':
                res['THU_TU_SAP_XEP'] = int(child.text)
            
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # Điều chỉnh công cụ dụng cụ
    def _import_SUAdjustment(self, tag):
        rec_model = 'supply.dieu.chinh'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'RefNo':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['LY_DO_DIEU_CHINH'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # Điều chỉnh công cụ dụng cụ chi tiet
    def _import_SUAdjustmentDetail(self, tag):
        rec_model = 'supply.dieu.chinh.chi.tiet'
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
                    res['CHI_TIET_DIEU_CHINH_CCDC_ID_ID'] = rid.id
            elif child.tag == 'SupplyID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_CCDC'] = rid.id
            elif child.tag == 'Quantity':
                res['SO_LUONG'] = float(child.text)
            elif child.tag == 'CurrentRemainingAmount':
                res['GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH'] = float(child.text)

            elif child.tag == 'NewRemainingAmount':
                res['GIA_TRI_CON_LAI_SAU_DIEU_CHINH'] = float(child.text)
            elif child.tag == 'DiffRemainingAmount':
                res['CHENH_LECH_GIA_TRI'] = float(child.text)
            elif child.tag == 'CurrentRemainingAllocationTime':
                res['SO_KY_PHAN_BO_CON_LAI_TRUOC_DIEU_CHINH'] = int(child.text)
            elif child.tag == 'NewRemainingAllocationTime':
                res['SO_KY_CON_LAI_SAU_DIEU_CHINH'] = int(child.text)
            elif child.tag == 'DiffAllocationTime':
                res['CHENH_LENH_KY'] = int(child.text)
            elif child.tag == 'TermlyAllocationAmount':
                res['SO_TIEN_PHAN_BO_HANG_KY'] = float(child.text)

            elif child.tag == 'Note':
                res['GHI_CHU'] = child.text

            elif child.tag == 'AllocationAccount':
                rid = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TAI_KHOAN_CHO_PHAN_BO'] = rid.id 
            elif child.tag == 'SortOrder':
                res['sequence'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    #  # Ghi giảm công cụ dụng cụ
    def _import_SUDecrement(self, tag):
        rec_model = 'supply.ghi.giam'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'RefNo':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                if helper.Obj.convert_to_key(child.text) == 'NHUONG_BAN,_THANH_LY':
                    res['LY_DO_GHI_GIAM'] = 'NHUONG_BAN_THANH_LY'
                else:
                    res['LY_DO_GHI_GIAM'] = helper.Obj.convert_to_key(child.text)
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Ghi giảm công cụ dụng cụ chi tiet
    def _import_SUDecrementDetail(self, tag):
        rec_model = 'supply.ghi.giam.chi.tiet'
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
                    res['CCDC_GHI_GIAM_ID'] = rid.id
            elif child.tag == 'SupplyID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_CCDC_ID'] = rid.id
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_SU_DUNG_ID'] = rid.id
            elif child.tag == 'UseQuantity':
                res['SO_LUONG_DANG_DUNG'] = float(child.text)
            elif child.tag == 'DecrementQuantity':
                res['SO_LUONG_GHI_GIAM'] = float(child.text)

            elif child.tag == 'RemainingDecrementAmount':
                res['GIA_TRI_CON_LAI_CUA_CCDC_GHI_GIAM'] = float(child.text)
            elif child.tag == 'SUAllocationID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['PHAN_BO_CHI_PHI_ID'] = rid.id 
            elif child.tag == 'SortOrder':
                res['sequence'] = int(child.text) 
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    #  # Phân bổ chi phí công cụ dụng cụ
    def _import_SUAllocation(self, tag):
        rec_model = 'supply.phan.bo.chi.phi'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'RefNo':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'Month':
                res['THANG'] = child.text
            elif child.tag == 'Year':
                res['NAM'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'RefOrder':
                res['STT_NHAP_CT'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # phân bổ chi phí công cụ dụng cụ chi tiet(xác định mức chi phí)
    def _import_SUAllocationDetailExpense(self, tag):
        rec_model = 'supply.phan.bo.chi.phi.muc.chi.phi'
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
                    res['PHAN_BO_CHI_PHI_ID'] = rid.id
            elif child.tag == 'SupplyID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_CCDC'] = rid.id
            elif child.tag == 'SupplyCategoryID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['LOAI_CCDC_ID'] = rid.id
            elif child.tag == 'TotalAllocationAmount':
                res['TONG_SO_TIEN_PHAN_BO'] = float(child.text)
            elif child.tag == 'AllocationAmount':
                res['SO_TIEN_PB_CCDC_DAG_DUNG'] = float(child.text)
            elif child.tag == 'RemainingAmount':
                res['GIA_TRI_CON_LAI_CUA_CCDC_GIAM'] = float(child.text)  
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # phân bổ chi phí chi tiet(phân bổ)
    def _import_SUAllocationDetailTable(self, tag):
        rec_model = 'supply.phan.bo.chi.phi.phan.bo'
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
                    res['PHAN_BO_CHI_PHI_ID'] = rid.id
            elif child.tag == 'SupplyID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_CCDC'] = rid.id
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
            elif child.tag == 'TotalAllocationAmount':
                res['CHI_PHI_PHAN_BO'] = float(child.text)
            elif child.tag == 'AllocationRate':
                res['TY_LE'] = float(child.text)
            elif child.tag == 'AllocationAmount':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'CostAccount':
                res['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id 
            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id  
            elif child.tag == 'SortOrder':
                res['THU_TU_SAP_XEP'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # phân bổ chi phí chi tiet(hạch toán)
    def _import_SUAllocationDetailPost(self, tag):
        rec_model = 'supply.phan.bo.chi.phi.hach.toan'
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
                    res['PHAN_BO_CHI_PHI_ID'] = rid.id
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
                res['CB_KHONG_HOP_LY'] = True if child.text == 'true' else False
            
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_DAT_HANG_ID'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    #  # kiểm kê công cụ dụng cụ
    def _import_SUAudit(self, tag):
        rec_model = 'supply.kiem.ke'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefDate':
                res['NGAY'] = child.text
            elif child.tag == 'BalanceDate':
                res['KIEM_KE_DEN_NGAY_CCDC'] = child.text
            elif child.tag == 'RefNo':
                res['SO'] = child.text
            elif child.tag == 'JournalMemo':
                res['MUC_DICH'] = child.text
            elif child.tag == 'Summary':
                res['KET_LUAN'] = child.text
            # elif child.tag == 'CreatedDate':
            #     res['GIO'] = child.text
            elif child.tag == 'IsExecuted':
                res['DA_XU_LY_KIEN_NGHI'] = True if child.text == 'true' else False
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # #kiểm kê công cụ dụng cụ chi tiết
    def _import_SUAuditDetail(self, tag):
        rec_model = 'supply.kiem.ke.cong.cu.dung.cu'
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
                    res['KIEM_KE_CCDC_ID'] = rid.id
            elif child.tag == 'SupplyID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_CCDC_ID'] = rid.id
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['DON_VI_SU_DUNG_ID'] = rid.id
            elif child.tag == 'QuantityOnBook':
                res['TREN_SO_KE_TOAN'] = float(child.text)
            elif child.tag == 'QuantityInventory':
                res['KIEM_KE'] = float(child.text)
            elif child.tag == 'DiffQuantity':
                res['CHENH_LECH'] = float(child.text)  
            elif child.tag == 'GoodQuantity':
                res['SO_LUONG_TOT'] = float(child.text)
            elif child.tag == 'DamageQuantity':
                res['SO_LUONG_HONG'] = float(child.text)
            elif child.tag == 'ExecuteQuantity':
                res['SO_LUONG_XU_LY'] = float(child.text)  
            elif child.tag == 'Note':
                res['GHI_CHU'] =child.text
            elif child.tag == 'Action':
                res['KIEN_NGHI_XU_LY'] =child.text       
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # kiểm kê công cụ dụng cụ chi tiet(thanh vien tham gia)
    def _import_SUAuditMemberDetail(self, tag):
        rec_model = 'supply.kiem.ke.thanh.vien.tham.gia'
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
                    res['KIEM_KE_CCDC_ID'] = rid.id
            
            elif child.tag == 'AccountObjectName':
                res['HO_TEN'] = child.text
            elif child.tag == 'Position':
                res['CHUC_DANH'] =child.text
            elif child.tag == 'Representative':
                res['DAI_DIEN'] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)



    

    