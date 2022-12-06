# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, helper

MODULE = 'base_import_ex'


class Import(models.TransientModel):
    _inherit = 'base_import_ex.import'

    # Bảng chấm công

    def _import_PATimeSheet(self, tag):
        rec_model = 'tien.luong.bang.cham.cong.chi.tiet.master'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            elif child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so' 
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
                if child.text == '6000':
                    res['ten_loai_cham_cong'] = 'Bảng chấm công theo buổi'
                elif child.text == '6001':
                    res['ten_loai_cham_cong'] = 'Bảng chấm công theo giờ'
            elif child.tag == 'PATimeSheetMonth':
                res['thang'] = int(child.text)

            elif child.tag == 'PATimeSheetYear':
                res['nam'] = child.text
            elif child.tag == 'PATimeSheetName':
                res['TEN_BANG_CHAM_CONG'] = child.text
            
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Bảng chấm công chi tiết
    def _import_PATimeSheetDetail(self,tag):
        rec_model = 'tien.luong.bang.cham.cong.chi.tiet.detail'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            elif child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text.lower()), False)
                if rid:
                    res['CHI_TIET_ID'] = rid.id
            elif child.tag == 'EmployeeID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['MA_NHAN_VIEN'] = rid.id
            elif child.tag == 'OrganizationUnitID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text.lower()), False)
                if rid:
                    res['DON_VI_ID'] = rid.id
            elif child.tag == 'Day1':
                res['NGAY_1'] = child.text
            elif child.tag == 'Day2':
                res['NGAY_2'] = child.text
            elif child.tag == 'Day3':
                res['NGAY_3'] = child.text
            elif child.tag == 'Day4':
                res['NGAY_4'] = child.text
            elif child.tag == 'Day5':
                res['NGAY_5'] = child.text
            elif child.tag == 'Day6':
                res['NGAY_6'] = child.text
            elif child.tag == 'Day7':
                res['NGAY_7'] = child.text
            elif child.tag == 'Day8':
                res['NGAY_8'] = child.text
            elif child.tag == 'Day9':
                res['NGAY_9'] = child.text
            elif child.tag == 'Day10':
                res['NGAY_10'] = child.text
            elif child.tag == 'Day11':
                res['NGAY_11'] = child.text
            elif child.tag == 'Day12':
                res['NGAY_12'] = child.text
            elif child.tag == 'Day13':
                res['NGAY_13'] = child.text
            elif child.tag == 'Day14':
                res['NGAY_14'] = child.text
            elif child.tag == 'Day15':
                res['NGAY_15'] = child.text
            elif child.tag == 'Day16':
                res['NGAY_16'] = child.text
            elif child.tag == 'Day17':
                res['NGAY_17'] = child.text
            elif child.tag == 'Day18':
                res['NGAY_18'] = child.text
            elif child.tag == 'Day19':
                res['NGAY_19'] = child.text
            elif child.tag == 'Day20':
                res['NGAY_20'] = child.text
            elif child.tag == 'Day21':
                res['NGAY_21'] = child.text
            elif child.tag == 'Day22':
                res['NGAY_22'] = child.text
            elif child.tag == 'Day23':
                res['NGAY_23'] = child.text
            elif child.tag == 'Day24':
                res['NGAY_24'] = child.text
            elif child.tag == 'Day25':
                res['NGAY_25'] = child.text
            elif child.tag == 'Day26':
                res['NGAY_26'] = child.text
            elif child.tag == 'Day27':
                res['NGAY_27'] = child.text
            elif child.tag == 'Day28':
                res['NGAY_28'] = child.text
            elif child.tag == 'Day29':
                res['NGAY_29'] = child.text
            elif child.tag == 'Day30':
                res['NGAY_30'] = child.text
            elif child.tag == 'Day31':
                res['NGAY_31'] = child.text
            elif child.tag == 'PaidWorkingday':
                res['SO_CONG_HUONG'] = float(child.text)
            elif child.tag == 'NonPaidWorkingday':
                res['SO_CONG_KHONG_HUONG'] = float(child.text)
            elif child.tag == 'WorkingDay':
                res['NGAY_THUONG_BAN_NGAY'] = float(child.text)
            elif child.tag == 'WeekendDay':
                res['THU_BAY_CHU_NHAT_BAN_NGAY'] = float(child.text)
            elif child.tag == 'Holiday':
                res['LE_TET_BAN_NGAY'] = float(child.text)
            elif child.tag == 'WorkingDayNight':
                res['NGAY_THUONG_BAN_DEM'] = float(child.text)
            elif child.tag == 'WeekendDayNight':
                res['THU_7_CHU_NHAT_BAN_DEM'] = float(child.text)
            elif child.tag == 'HolidayNight':
                res['LE_TET_BAN_DEM'] = float(child.text)
            elif child.tag == 'TotalOverTime':
                res['TONG_LAM_THEM'] = float(child.text)
            elif child.tag == 'SortOrder':
                res['SO_THU_TU'] = int(child.text)
        return self.env['ir.model.data']._update(
            rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

#  Tổng hợp chấm công 
    def _import_PATimeSheetSummary(self, tag):
        rec_model = 'tien.luong.bang.tong.hop.cham.cong'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            elif child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so' 
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = float(child.text)
                if child.text == '6010':
                    res['LOAI_CHAM_CONG'] = 'Tổng hợp chấm công theo buổi'
                elif child.text == '6011':
                    res['LOAI_CHAM_CONG'] = 'Tổng hợp chấm công theo giờ'
            elif child.tag == 'PATimeSheetMonth':
                res['THANG'] = child.text
            elif child.tag == 'PATimeSheetYear':
                res['NAM'] = child.text
            elif child.tag == 'PATimeSheetName':
                res['TEN_BANG_CHAM_CONG'] = child.text
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

# Bảng tổng hợp chấm công chi tiết
    def _import_PATimeSheetSummaryDetail(self,tag):
        rec_model = 'tien.luong.bang.tong.hop.cham.cong.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            elif child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHI_TIET_ID'] = rid.id
            elif child.tag == 'EmployeeID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_NHAN_VIEN'] = rid.id
            elif child.tag == 'OrganizationUnitID':
                res['DON_VI_ID'] = self.env.ref('{}.{}'.format(MODULE,child.text)).id
            elif child.tag == 'PaidWorkingday':
                res['LUONG_THOI_GIAN_CA_NGAY'] = float(child.text)
            elif child.tag == 'NonPaidWorkingday':
                res['LUONG_THOI_GIAN_NUA_NGAY'] = float(child.text)
            elif child.tag == 'WorkingDay':
                res['NGAY_THUONG_BAN_NGAY'] = float(child.text)
            elif child.tag == 'WeekendDay':
                res['THU_BAY_CHU_NHAT_BAN_NGAY'] = float(child.text)
            elif child.tag == 'Holiday':
                res['LE_TET_BAN_NGAY'] = float(child.text)
            elif child.tag == 'WorkingDayNight':
                res['NGAY_THUONG_BAN_DEM'] = float(child.text)
            elif child.tag == 'WeekendDayNight':
                res['THU_BAY_CHU_NHAT_BAN_DEM'] = float(child.text)
            elif child.tag == 'HolidayNight':
                res['LE_TET_BAN_DEM'] = float(child.text)
            elif child.tag == 'SortOrder':
                res['STT'] = int(child.text)
            elif child.tag == 'TotalOverTime':
                res['TONG'] = float(child.text)
            
        return self.env['ir.model.data']._update(
            rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

#  Bảng lương
    def _import_PASalarySheet(self, tag):
        rec_model = 'tien.luong.bang.luong'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            elif child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so' 
            elif child.tag == 'RefType':
                if child.text =='6020':
                    res['LOAI_BANG_LUONG'] = 'Bảng lương cố định(không dựa trên bảng chấm công)'
                    res['TEN_LOAI_BANG_LUONG'] = 'LUONG_CO_DINH'
                elif child.text=='6021':
                    res['LOAI_BANG_LUONG'] = 'Bảng lương thời gian theo buổi'
                    res['TEN_LOAI_BANG_LUONG'] = 'LUONG_THOI_GIAN_THEO_BUOI'
                elif child.text=='6022':
                    res['LOAI_BANG_LUONG'] = 'Bảng lương thời gian theo giờ'
                    res['TEN_LOAI_BANG_LUONG'] = 'LUONG_THOI_GIAN_THEO_GIO'
                elif child.text=='6023':
                    res['LOAI_BANG_LUONG'] = 'Bảng lương tạm ứng'
                    res['TEN_LOAI_BANG_LUONG'] = 'LUONG_TAM_UNG'
                res['LOAI_CHUNG_TU'] = int(child.text)
            elif child.tag == 'PASalarySheetMonth':
                res['THANG'] = child.text
            elif child.tag == 'PASalarySheetYear':
                res['NAM'] = child.text
            elif child.tag == 'PASalarySheetName':
                res['TEN_BANG_LUONG'] = child.text
            elif child.tag == 'TotalNetIncomeAmount':
                res['TONG_SO_TIEN'] = float(child.text)
            elif child.tag == 'BranchID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

# Bảng tính lương chi tiết
    def _import_PASalarySheetDetail(self,tag):
        rec_model = 'tien.luong.bang.luong.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'PASalarySheetDetailID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so'
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHI_TIET_ID'] = rid.id
            elif child.tag == 'SortOrder':
                res['STT'] = int(child.text)
            elif child.tag == 'EmployeeID':
                rid = self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['MA_NHAN_VIEN'] = rid.id
            elif child.tag == 'ContactTitle':
                res['CHUC_DANH'] = child.text
            elif child.tag == 'BasicWage':
                res['LUONG_CO_BAN'] = float(child.text)
            elif child.tag == 'PayrollFundAllowance':
                res['PHU_CAP_THUOC_QUY_LUONG'] = float(child.text)
            elif child.tag == 'OtherAllowance':
                res['PHU_CAP_KHAC'] = float(child.text)
            elif child.tag == 'TotalAmount':
                res['TONG_SO'] = float(child.text)
            elif child.tag == 'AdvancePaymentAmount':
                res['SO_TIEN_TAM_UNG'] = float(child.text)
            elif child.tag == 'InsuranceSalaryAmount':
                res['LUONG_DONG_BH'] = float(child.text)
            elif child.tag == 'SocialInsuranceAmount':
                res['BHXH_KHAU_TRU'] = float(child.text)
            elif child.tag == 'HealthInsurranceAmount':
                res['BHYT_KHAU_TRU'] = float(child.text)
            elif child.tag == 'UnemploymentInsurranceAmount':
                res['BHTN_KHAU_TRU'] = float(child.text)
            elif child.tag == 'LaborUnionContributionAmount':
                res['KPCD_KHAU_TRU'] = float(child.text)
            elif child.tag == 'IncomeTaxAmount':
                res['THUE_TNCN_KHAU_TRU'] = float(child.text)
            elif child.tag == 'SumOfDeductionAmount':
                res['CONG_KHAU_TRU'] = float(child.text)
            elif child.tag == 'FamilyCoditionDeductionAmount':
                res['GIAM_TRU_GIA_CANH'] = float(child.text)
            elif child.tag == 'TotalPersonalTaxIncomeAmount':
                res['TONG_THU_NHAP_CHIU_THUE_TNCN'] = float(child.text)
            elif child.tag == 'IncomeForTaxCalculation':
                res['THU_NHAP_TINH_THUE_TNCN'] = float(child.text)
            elif child.tag == 'NetAmount':
                res['SO_TIEN_CON_DUOC_LINH'] = float(child.text)
            elif child.tag == 'CompanySocialInsuranceAmount':
                res['BHXH_CONG_TY_DONG'] = float(child.text)
            elif child.tag == 'CompanyHealthInsurranceAmount':
                res['BHYT_CONG_TY_DONG'] = float(child.text)
            elif child.tag == 'CompanyUnemploymentInsurranceAmount':
                res['BHTN_CONG_TY_DONG'] = float(child.text)
            elif child.tag == 'CompanyLaborUnionContributionAmount':
                res['KPCD_CONG_TY_DONG'] = float(child.text)
            elif child.tag == 'WorkingDayUnitPrice':
                res['DON_GIA_NGAY_CONG'] = float(child.text)
            elif child.tag == 'NumberOfPaidWorkingdayTimeSheet':
                res['SO_CONG_HUONG'] = float(child.text)
                # res['SO_NGAY_CONG_HUONG'] = float(child.text)
            elif child.tag == 'PaidWorkingdayAmount':
                res['SO_TIEN_HUONG'] = float(child.text)
            elif child.tag == 'NumberOfNonWorkingdayTimeSheet':
                res['SO_CONG_KHONG_HUONG'] = float(child.text)
                # res['SO_NGAY_CONG_KHONG_HUONG'] = float(child.text)
            elif child.tag == 'NonWorkingdayAmount':
                res['SO_TIEN_KHONG_HUONG'] = float(child.text)
            elif child.tag == 'TotalOverTime':
                res['SO_GIO_CONG_LAM_THEM'] = float(child.text)
            elif child.tag == 'OverTimeAmount':
                res['SO_TIEN_LAM_THEM'] = float(child.text)
            elif child.tag == 'WorkingHourUnitPrice':
                res['DON_GIA_GIO_CONG'] = float(child.text)
            elif child.tag == 'OrganizationUnitID':
                res['DON_VI_ID'] = self.env.ref('{}.{}'.format(MODULE,child.text)).id
            elif child.tag == 'SalaryCoefficient':
                res['HE_SO_LUONG'] = float(child.text)  
            elif child.tag == 'SignName':
                res['KY_NHAN'] = child.text
            elif child.tag == 'AdvancePaymentAmount141':
                res['TAM_UNG_141'] = float(child.text)      
        return self.env['ir.model.data']._update(
            rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
#  Hạch toán chi phí lương
    def _import_PASalaryExpense(self, tag):
        rec_model = 'tien.luong.hach.toan.chi.phi.luong'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            if child.tag == 'IsPostedFinance':
                res['state'] = 'da_ghi_so' if child.text == 'true' else 'chua_ghi_so' 
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] = int(child.text)
            elif child.tag == 'PostedDate':
                res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'RefNoFinance':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'PASalarySheetName':
                res['BANG_LUONG'] = child.text
            elif child.tag == 'TotalAmount':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'BranchID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'PASalarySheetRefID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['BANG_LUONG_ID'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

# Hạch toán chi phí lương chi tiết
    def _import_PASalaryExpenseDetail(self,tag):
        rec_model = 'tien.luong.hach.toan.chi.phi.luong.chi.tiet'
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
                    res['CHI_TIET_ID'] = rid.id
            elif child.tag == 'Description':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'DebitAccount':
                res['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id 
            elif child.tag == 'CreditAccount':
                res['TK_CO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1).id 
            elif child.tag == 'Amount':
                res['SO_TIEN'] = float(child.text)
            elif child.tag == 'DebitAccountObjectID':
                res['DOI_TUONG_NO_ID'] = self.env.ref('{}.{}'.format(MODULE,child.text)).id
            elif child.tag == 'CreditAccountObjectID':
                res['DOI_TUONG_CO_ID'] = self.env.ref('{}.{}'.format(MODULE,child.text)).id
            elif child.tag == 'OrganizationUnitID':
                res['DON_VI_ID'] = self.env.ref('{}.{}'.format(MODULE,child.text)).id
            elif child.tag == 'ExpenseItemID':
                res['KHOAN_MUC_CP_ID'] = self.env.ref('{}.{}'.format(MODULE,child.text)).id
            elif child.tag == 'JobID':
                res['DOI_TUONG_THCP_ID'] = self.env.ref('{}.{}'.format(MODULE,child.text)).id
            elif child.tag == 'ProjectWorkID':
                res['CONG_TRINH_ID'] = self.env.ref('{}.{}'.format(MODULE,child.text)).id
            elif child.tag == 'OrderID':
                res['DON_DAT_HANG_ID'] = self.env.ref('{}.{}'.format(MODULE,child.text)).id
            elif child.tag == 'ContractID':
                res['HOP_DONG_BAN_ID'] = self.env.ref('{}.{}'.format(MODULE,child.text)).id
            elif child.tag =='UnResonableCost':
                res['CP_KHONG_HOP_LY'] = True if child.text == 'true' else False
            elif child.tag == 'ListItemID':
                res['MA_THONG_KE_ID'] = self.env.ref('{}.{}'.format(MODULE,child.text)).id
            elif child.tag == 'SortOrder':
                res['STT'] = int(child.text)
        return self.env['ir.model.data']._update(
            rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)   