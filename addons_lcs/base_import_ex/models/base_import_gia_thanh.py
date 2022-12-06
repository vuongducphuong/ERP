# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, helper

MODULE = 'base_import_ex'


class Import(models.TransientModel):
    _inherit = 'base_import_ex.import'

    # Kỳ tính giá thành sản xuất liên tục - Giản đơn

    def _import_JCPeriod(self, tag):
        rec_model = 'gia.thanh.ky.tinh.gia.thanh'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'JCPeriodID':
                rec_id = child.text
            elif child.tag == 'JCPeriodType':
                if child.text == '0':
                    res['LOAI_GIA_THANH'] = 'DON_GIAN'
                elif child.text == '1':
                    res['LOAI_GIA_THANH'] = 'HE_SO_TY_LE'
                elif child.text == '3':
                    res['LOAI_GIA_THANH'] = 'CONG_TRINH'
                elif child.text == '4':
                    res['LOAI_GIA_THANH'] = 'DON_HANG'
                elif child.text == '5':
                    res['LOAI_GIA_THANH'] = 'HOP_DONG'
                elif child.text == '2':
                    res['LOAI_GIA_THANH'] = 'PHAN_BUOC'
            elif child.tag == 'BranchID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'JCPeriodName':
                res['TEN'] = child.text
            elif child.tag == 'FromDate':
                res['TU_NGAY'] = child.text
            elif child.tag == 'ToDate':
                res['DEN_NGAY'] = child.text

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # kỳ tính giá thành chi tiết
    def _import_JCPeriodDetail(self,tag):
        rec_model = 'gia.thanh.ky.tinh.gia.thanh.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'JCPeriodDetailID':
                rec_id = child.text
            elif child.tag == 'JCPeriodID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['KY_TINH_GIA_THANH_ID'] = rid.id
            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['MA_DOI_TUONG_THCP_ID'] = rid.id
            elif child.tag == 'ProjectWorkID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['MA_CONG_TRINH_ID'] = rid.id
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['SO_DON_HANG_ID'] = rid.id
            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['SO_HOP_DONG_ID'] = rid.id
            elif child.tag == 'SortOrder':
                res['STT'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    # Kết chuyển chi phí
    def _import_JCExpenseTranfer(self,tag):
        rec_model = 'gia.thanh.ket.chuyen.chi.phi'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            elif child.tag == 'JCPeriodID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['KY_TINH_GIA_THANH_ID'] = rid.id
                    if rid.LOAI_GIA_THANH =='DON_GIAN':
                        res['LOAI_KET_CHUYEN_CHI_PHI'] = 'GIAN_DON'
                    elif rid.LOAI_GIA_THANH =='HE_SO_TY_LE':
                        res['LOAI_KET_CHUYEN_CHI_PHI'] = 'HE_SO_TY_LE'
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
            elif child.tag == 'TotalAmount':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'RefNo':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    # Kết chuyển chi phí chi tiết
    def _import_JCExpenseTranferDetail(self,tag):
        rec_model = 'gia.thanh.ket.chuyen.chi.phi.hach.toan'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHI_TIET_ID'] = rid.id
            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['MA_DOI_TUONG_THCP_ID'] = rid.id
            elif child.tag == 'ProjectWorkID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['MA_CONG_TRINH_ID'] = rid.id
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['SO_DON_HANG_ID'] = rid.id
            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'Amount':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'SortOrder':
                res['STT'] = int(child.text)
            elif child.tag == 'DebitAccount':
                rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id 
            elif child.tag == 'CreditAccount':
                rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id 
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Import nghiệm thu
    def _import_JCAccepted(self,tag):
        rec_model = 'gia.thanh.nghiem.thu'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            elif child.tag == 'JCPeriodID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['KY_TINH_GIA_THANH_ID'] = rid.id
                    res['KY_TINH_GIA_THANH'] = rid.TEN
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
            elif child.tag == 'TotalAmount':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'RefNo':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Import nghiệm thu chi tiết
    def _import_JCAcceptedDetail(self,tag):
        rec_model = 'gia.thanh.nghiem.thu.hach.toan'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHI_TIET_ID'] = rid.id
            elif child.tag == 'ProjectWorkID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['MA_CONG_TRINH_ID'] = rid.id
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['SO_DON_HANG_ID'] = rid.id
            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['HOP_DONG_BAN_ID'] = rid.id
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'RevenueAmount':
                res['DOANH_THU'] = float(child.text)
            elif child.tag == 'Amount':
                res['GIA_TRI_NGHIEM_THU'] = float(child.text)
            elif child.tag == 'TotalCostAmount':
                res['SO_CHUA_NGHIEM_THU'] = float(child.text)
            elif child.tag == 'AcceptedRate':
                res['PHAN_TRAM_NGHIEM_THU'] = float(child.text)
            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id
            elif child.tag == 'ListItemID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['MA_THONG_KE_ID'] = rid.id
            elif child.tag == 'SortOrder':
                res['STT'] = int(child.text)
            elif child.tag == 'DebitAccount':
                rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id 
            elif child.tag == 'CreditAccount':
                rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id 
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Import định mức nguyên vật liệu công trình
    def _import_ProjectWorkNorm(self,tag):
        rec_model = 'gia.thanh.dinh.muc.nguyen.vat.lieu.cong.trinh'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ProjectWorkNormID':
                rec_id = child.text
            elif child.tag == 'ProjectWorkID':
                text_lower = child.text.lower()
                rid = self.env.ref('{}.{}'.format(MODULE, text_lower), False)
                if rid:
                    res['CONG_TRINH_ID'] = rid.id
            elif child.tag == 'FromDate':
                res['TU_NGAY'] = child.text
            elif child.tag == 'ToDate':
                res['DEN_NGAY'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'Inactive':
                res['ACTIVE'] = False if child.text == '0' else True
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Import định mức nguyên vật liệu công trình chi tiết
    def _import_ProjectWorkNormDetail(self,tag):
        rec_model = 'gia.thanh.dinh.muc.nguyen.vat.lieu.cong.trinh.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ProjectWorkNormDetailID':
                rec_id = child.text
            elif child.tag == 'ProjectWorkNormID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHI_TIET_ID'] = rid.id
            elif child.tag == 'InventoryItemID':
                text_lower = child.text.lower()
                rid = self.env.ref('{}.{}'.format(MODULE, text_lower), False)
                if rid:
                    res['MA_NGUYEN_VAT_LIEU_ID'] = rid.id
            elif child.tag == 'Description':
                res['TEN_NGUYEN_VAT_LIEU'] = child.text
            elif child.tag == 'UnitID':
                text_lower = child.text.lower()
                rid = self.env.ref('{}.{}'.format(MODULE, text_lower), False)
                if rid:
                    res['DVT_ID'] = rid.id
            elif child.tag == 'Quantity':
                res['SO_LUONG_DINH_MUC'] = float(child.text)
            elif child.tag == 'UnitPrice':
                res['DON_GIA_DINH_MUC'] = float(child.text)
            elif child.tag == 'Amount':
                res['THANH_TIEN'] = float(child.text)
            elif child.tag == 'SortOrder':
                res['STT'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # Import cấu hình số dư đầu kỳ
    def _import_JCOPNConfig(self,tag):
        rec_model = 'gia.thanh.cau.hinh.so.du.dau.ky'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'JCOPNConfigID':
                rec_id = child.text
            elif child.tag == 'IsDetailJobByExpense':
                res['CHI_TIET_THEO_DTTHCP'] = True if child.text == 'true' else False
            elif child.tag == 'IsDetailProjectWorkByExpense':
                res['CHI_TIET_THEO_CONG_TRINH'] = True if child.text == 'true' else False
            elif child.tag == 'IsDetailOrderByExpense':
                res['CHI_TIET_THEO_DON_HANG'] = True if child.text == 'true' else False
            elif child.tag == 'IsDetailContractByExpense':
                res['CHI_TIET_THEO_HOP_DONG'] = True if child.text == 'true' else False
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


 # Import giá thành kết quả phân bổ chi phí chung
    def _import_JCCostAllocationDetail(self,tag):
        rec_model = 'gia.thanh.ket.qua.phan.bo.chi.phi.chung'
        res = {}
        rec_id = False

        
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            elif child.tag == 'JCPeriodDetailID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['KY_TINH_GIA_THANH_CHI_TIET_ID'] = rid.id 
            elif child.tag == 'JCPeriodID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['KY_TINH_GIA_THANH_ID'] = rid.id 
            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['MA_DOI_TUONG_THCP_ID'] = rid.id 


            elif child.tag == 'ProjectWorkID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['MA_CONG_TRINH_ID'] = rid.id 
            elif child.tag == 'OrderID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['SO_DON_HANG_ID'] = rid.id 
            elif child.tag == 'ContractID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['SO_HOP_DONG_ID'] = rid.id 
            elif child.tag == 'ExpenseItemID ':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id          
            elif child.tag == 'AccountNumber':
                rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TAI_KHOAN_ID'] = rid.id 
            elif child.tag == 'AllocationRate':
                res['TY_LE'] = float(child.text)
            elif child.tag == 'AllocationAmount':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'AllocationMethod':
                res['TIEU_THUC_PHAN_BO'] = child.text
            elif child.tag == 'IsAllocation':
                res['DA_PHAN_BO'] = True if child.text == 'true' else False
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # Import giá thành chi tiết chứng từ phân bổ chi phí chung
    def _import_JCCostVoucher(self,tag):
        rec_model = 'gia.thanh.chi.tiet.chung.tu.phan.bo.chi.phi.chung'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'JCCostVoucherID':
                rec_id = child.text
            elif child.tag == 'JCPeriodID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['KY_TINH_GIA_THANH_ID'] = rid.id
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text

            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] =int(child.text)
            elif child.tag == 'RefNo':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'AccountNumber':
                rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CHI_PHI_ID'] = rid.id 
            elif child.tag == 'TotalAmount':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'RemainingAmount':
                res['SO_CHUA_PHAN_BO'] = float(child.text)
            elif child.tag == 'AllocationAmount':
                res['SO_PHAN_BO_LAN_NAY'] = float(child.text)
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['ID_GOC'] = rid.id
                    res['MODEL_GOC'] = rid._name
            elif child.tag == 'ExpenseItemID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['KHOAN_MUC_CP_ID'] = rid.id
            elif child.tag == 'AllocationRate':
                res['TY_LE_PHAN_BO'] = float(child.text)
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'AccountNumberRemainingAmount':
                res['SO_TAI_KHOAN_CON_LAI'] = float(child.text)
            elif child.tag == 'AccountNumberTotalAmount':
                res['SO_TAI_KHOAN_TONG_TIEN'] = float(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

# Import giá thành khai báo định mức giá thành phẩm chi tiết
    def _import_JCProductQuantum(self,tag):
        rec_model = 'gia.thanh.khai.bao.dinh.muc.gttp.chi.tiet'
        res = {}
        rec_id = False
  
        inventory_id =''
        
        for child in tag.getchildren():
            if child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                inventory_id = child.text.lower()
                if rid:
                    res['MA_THANH_PHAM_ID'] = rid.id 

            elif child.tag == 'DirectMatetialAmount':
                res['NVL_TRUC_TIEP'] = float(child.text)
            elif child.tag == 'IndirectMatetialAmount':
                res['NVL_GIAN_TIEP'] = float(child.text)
            elif child.tag == 'DirectLaborAmount':
                res['NHAN_CONG_TRUC_TIEP'] = float(child.text)
            elif child.tag == 'IndirectLaborAmount':
                res['NHAN_CONG_GIAN_TIEP'] = float(child.text)
            elif child.tag == 'DepreciationAmount':
                res['KHAU_HAO'] = float(child.text)
            elif child.tag == 'PurchaseAmount':
                res['CHI_PHI_MUA_NGOAI'] = float(child.text)
            elif child.tag == 'OtherAmount':
                res['CHI_PHI_KHAC'] = float(child.text)
            elif child.tag == 'TotalAmount':
                res['TONG_CONG'] = float(child.text)                    
        rec_id = 'gia_thanh_khai_bao_dinh_muc_gttp_chi_tiet' + inventory_id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

# giá thành kết quả chi phí dở dang cuối kỳ chi tiết
    def _import_JCUncompleteDetail(self,tag):
        rec_model = 'gia.thanh.ket.qua.chi.phi.do.dang.cuoi.ky.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHI_TIET_ID'] = rid.id
            elif child.tag == 'JCPeriodID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['KY_TINH_GIA_THANH_ID'] = rid.id
            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['MA_DOI_TUONG_THCP_ID'] = rid.id
           
            elif child.tag == 'DirectMatetialAmount':
                res['NVL_TRUC_TIEP'] = float(child.text)
            elif child.tag == 'IndirectMatetialAmount':
                res['NVL_GIAN_TIEP'] = float(child.text)
            elif child.tag == 'DirectLaborAmount':
                res['NHAN_CONG_TRUC_TIEP'] = float(child.text)
            elif child.tag == 'IndirectLaborAmount':
                res['NHAN_CONG_GIAN_TIEP'] = float(child.text)
            elif child.tag == 'DepreciationAmount':
                res['KHAU_HAO'] = float(child.text)
            elif child.tag == 'PurchaseAmount':
                res['CHI_PHI_MUA_NGOAI'] = float(child.text)
            elif child.tag == 'OtherAmount':
                res['CHI_PHI_KHAC'] = float(child.text)
            elif child.tag == 'TotalUncompleteAmount':
                res['TONG_CHI_PHI'] = float(child.text)  
            elif child.tag == 'SortOrder':
                res['sequence'] = int(child.text)         
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    
    # giá thành bảng giá thành chi tiết
    def _import_JCProductCostDetail(self,tag):
        rec_model = 'gia.thanh.bang.gia.thanh.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text.lower()
            elif child.tag == 'JCPeriodID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['KY_TINH_GIA_THANH_ID'] = rid.id 
            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['MA_DOI_TUONG_THCP_ID'] = rid.id 
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['MA_THANH_PHAM_ID'] = rid.id 
           
            elif child.tag == 'DirectMatetialAmount':
                res['NVL_TRUC_TIEP'] = float(child.text)
            elif child.tag == 'IndirectMatetialAmount':
                res['NVL_GIAN_TIEP'] = float(child.text)
            elif child.tag == 'DirectLaborAmount':
                res['NHAN_CONG_TRUC_TIEP'] = float(child.text)
            elif child.tag == 'IndirectLaborAmount':
                res['NHAN_CONG_GIAN_TIEP'] = float(child.text)
            elif child.tag == 'DepreciationAmount':
                res['KHAU_HAO'] = float(child.text)
            elif child.tag == 'PurchaseAmount':
                res['CHI_PHI_MUA_NGOAI'] = float(child.text)
            elif child.tag == 'OtherAmount':
                res['CHI_PHI_KHAC'] = float(child.text)
            elif child.tag == 'TotalAmount':
                res['TONG'] = float(child.text) 
            elif child.tag == 'TotalQuantity':
                res['SO_LUONG_THANH_PHAM'] = float(child.text)  
            elif child.tag == 'CostPrice':
                res['GIA_THANH_DON_VI'] = float(child.text)   
            elif child.tag == 'SortOrder':
                res['sequence'] = int(child.text)         
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    
 # Import giá thành định mức phân bổ chi phí theo thcp và tk
    def _import_JCAllocationQuantumConfig (self,tag):
        rec_model = 'gia.thanh.dinh.muc.phan.bo.cp.theo.thcp.va.tk'
        res = {}
        rec_id = False
        iob_id =''  
        Period_ID ='' 
        ACCOUNT_NUMBER =''     
        for child in tag.getchildren():
            if child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                iob_id = child.text.lower()
                if rid:
                    res['DOI_TUONG_THCP_ID'] = rid.id 
            elif child.tag == 'JCPeriodID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                Period_ID = child.text.lower()
                if rid:
                    res['KY_TINH_GIA_THANH_ID'] = rid.id 
            elif child.tag == 'AccountNumber':
                rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                ACCOUNT_NUMBER = child.text
                if rid:
                    res['TAI_KHOAN_ID'] = rid.id 
            elif child.tag == 'Amount':
                res['SO_TIEN'] = float(child.text)                    
        rec_id = iob_id + Period_ID + ACCOUNT_NUMBER
           
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


    # Import giá thành khai báo định mức giá thành phẩm chi tiết
    def _import_JCAllocationQuantum(self,tag):
        rec_model = 'gia.thanh.khai.bao.dinh.muc.gttp.chi.tiet'
        res = {}
        rec_id = False  
        inventory_id =''        
        for child in tag.getchildren():
            if child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                inventory_id = child.text.lower()
                if rid:
                    res['MA_THANH_PHAM_ID'] = rid.id 
            elif child.tag == 'DirectMatetialAmount':
                res['NVL_TRUC_TIEP'] = float(child.text)
            elif child.tag == 'IndirectMatetialAmount':
                res['NVL_GIAN_TIEP'] = float(child.text)
            elif child.tag == 'DirectLaborAmount':
                res['NHAN_CONG_TRUC_TIEP'] = float(child.text)
            elif child.tag == 'IndirectLaborAmount':
                res['NHAN_CONG_GIAN_TIEP'] = float(child.text)
            elif child.tag == 'DepreciationAmount':
                res['KHAU_HAO'] = float(child.text)
            elif child.tag == 'PurchaseAmount':
                res['CHI_PHI_MUA_NGOAI'] = float(child.text)
            elif child.tag == 'OtherAmount':
                res['CHI_PHI_KHAC'] = float(child.text)
            elif child.tag == 'TotalAmount':
                res['TONG_CONG'] = float(child.text)
            elif child.tag == 'JobID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['DOI_TUONG_THCP_ID'] = rid.id                  
        rec_id = 'gia_thanh_khai_bao_dinh_muc_gttp_chi_tiet' + inventory_id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)


#  giá thành xác định dở dang chi tiết
    def _import_JCUncompleteDetailInventoryItem(self,tag):
        rec_model = 'gia.thanh.xac.dinh.do.dang.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'JCUncompleteDetailInventoryItemID':
                rec_id = child.text
            elif child.tag == 'RefDetailID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['GIA_THANH_KQ_CHI_PHI_DO_DANG_CHI_TIET_ID'] = rid.id
            elif child.tag == 'InventoryItemID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['MA_THANH_PHAM_ID'] = rid.id
            elif child.tag == 'Quantity':
                res['SL_DO_DANG_CUOI_KY'] = float(child.text)
            elif child.tag == 'PercenComplete':
                res['PHAN_TRAM_HOAN_THANH'] = float(child.text)
            elif child.tag == 'CostPrice':
                res['DON_GIA_DINH_MUC'] = float(child.text)
            elif child.tag == 'SortOrder':
                res['sequence'] = int(child.text)
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
   
   
    # Kỳ tính giá thành 

    def _import_JCUncomplete(self, tag):
        rec_model = 'gia.thanh.tinh.gia.thanh'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text          
            elif child.tag == 'JCPeriodDetailID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['KY_TINH_GIA_THANH_CHI_TIET_ID'] = rid.id
           

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
