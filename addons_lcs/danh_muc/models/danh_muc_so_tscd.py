# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SO_TSCD(models.Model):
    _name = 'so.tscd'
    _description = 'Sổ tài sản cố định'

    name = fields.Char()
    line_ids = fields.One2many('so.tscd.chi.tiet', 'SO_TSCD_ID')

class SO_TSCD_CHI_TIET(models.Model):
    _name = 'so.tscd.chi.tiet'
    _description = 'Sổ tài sản cố định chi tiết'

    name = fields.Char(string="name")
    SO_TSCD_ID = fields.Many2one('so.tscd', ondelete="cascade")
    ID_CHUNG_TU = fields.Integer(string='Id chứng từ', help='Id chứng từ', required=True)
    MODEL_CHUNG_TU = fields.Char(string='Model chứng từ', help='Model chứng từ', required=True)
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='RefType')
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='RefNo')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='RefDate')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='PostedDate', required=True)
    DON_VI_SU_DUNG_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị sử dụng', help='OrganizationUnitID')
    THOI_GIAN_SU_DUNG = fields.Float(string='Thời gian sử dụng', help='LifeTimeInMonth')
    THOI_GIAN_SU_DUNG_CON_LAI = fields.Float(string='Thời gian sử dụng còn lại', help='LifeTimeRemainingInMonth')
    TY_LE_KHAU_HAO_THANG = fields.Float(string='Tỉ lệ khấu hao tháng', help='DepreciationRateMonth')
    GIA_TRI_KHAU_HAO_THANG = fields.Float(string='Giá trị khấu hao tháng', help='MonthlyDepreciationAmount')
    GIA_TRI_TINH_KHAU_HAO = fields.Float(string='Giá trị tính khấu hao', help='DepreciationAmount')
    GIA_TRI_HAO_MON_LUY_KE = fields.Float(string='Giá trị hao mòn lũy kế', help='AccumDepreciationAmount')
    GIA_TRI_CON_LAI = fields.Float(string='Giá trị còn lại', help='RemainingAmount')
    DIEN_GIAI_CHUNG = fields.Char(string='Diễn giải chung', help='JournalMemo')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='BranchID')
    LOAI_TSCD_ID = fields.Many2one('danh.muc.loai.tai.san.co.dinh', string='Loại tscd', help='FixedAssetCategoryID')
    LOAI_TSCD = fields.Char(string='Loại tscd', help='Loại tscd', compute='_compute_LOAI_TSCD_ID', store=True)
    MA_LOAI_TSCD = fields.Char(string='Mã loại tscd', help='FixedAssetCode', compute='_compute_LOAI_TSCD_ID', store=True)
    NGUYEN_GIA = fields.Float(string='Nguyên giá', help='OrgPrice')
    TK_NGUYEN_GIA_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk nguyên giá', help='OrgPriceAccount')
    TK_HAO_MON_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk hao mòn', help='DepreciationAccount')
    CHENH_LECH_GIA_TRI_HAO_MON_LUY_KE = fields.Float(string='Chênh lệch giá trị hao mòn lũy kế', help='DiffAccumDepreciationAmount')
    CHENH_LECH_THOI_GIAN_SU_DUNG = fields.Float(string='Chênh lệch thời gian sử dụng', help='SumDiffLifeTime')
    CHENH_LECH_GIA_TRI_TINH_KHAU_HAO = fields.Float(string='Chênh lệch giá trị tính khấu hao', help='DiffDepreciationAmount')
    CHENH_LECH_GIA_TRI_CON_LAI = fields.Float(string='Chênh lệch giá trị còn lại', help='SumDiffRemainingAmount')
    # CHENH_LENH_GIA_TRI_TINH_KHAU_HAO = fields.Float(string='Chênh lệnh giá trị tính khấu hao', help='Chênh lệnh giá trị tính khấu hao')
    GTKH_THANG_THEO_LUAT_SAU_DIEU_CHINH = fields.Float(string='Gtkh tháng theo luật sau điều chỉnh', help='?')

    GIA_TRI_TINH_KH_THEO_LUAT = fields.Float(string='Giá trị tính kh theo luật', help='DepreciationAmountByIncomeTax')
    GIA_TRI_KH_THANG_THEO_LUAT = fields.Float(string='Giá trị kh tháng theo luật', help='MonthlyDepreciationAmountByIncomeTax')
    THU_TU_NGHIEP_VU = fields.Integer(string='Thứ tự nghiệp vụ', help='RefOrderInSubSystem', compute='_compute_THU_TU_NGHIEP_VU', store=True)

    CHENH_LECH_NGUYEN_GIA = fields.Float(string='Chênh lệch nguyên giá', help='DiffOrgPriceAmount ')
    GIA_TRI_KHAU_HAO_THANG_KHI_KH = fields.Float(string='Gía trị khấu hao tháng khi khấu hao', help='MonthlyDepreciationAmountOnDepreciation ')
    TONG_CHENH_LECH_GIA_TRI_HAO_MON_LUY_KE = fields.Float(string='Tổng chênh lệch giá trị hao mòn lũy kế', help='Tổng chênh lệch giá trị hao mòn lũy kế')

    THU_TU_CHUNG_TU_NHAP_TRUOC_NHAP_SAU = fields.Integer(string='Thứ tự chứng từ nhập trước nhập sau', help='RefOrder')
    STT_CHUNG_TU = fields.Char(string='Số thứ tự chứng từ', help='Số thứ tự chứng từ') 

    @api.depends('LOAI_TSCD_ID')
    def _compute_LOAI_TSCD_ID(self):
        for record in self:
            record.MA_LOAI_TSCD = record.LOAI_TSCD_ID.MA
            record.LOAI_TSCD = record.LOAI_TSCD_ID.TEN

    @api.depends('LOAI_CHUNG_TU')
    def _compute_THU_TU_NGHIEP_VU(self):
        for record in self:
            if record.LOAI_CHUNG_TU == 615:
                record.THU_TU_NGHIEP_VU = 0
            elif record.LOAI_CHUNG_TU == 250:
                record.THU_TU_NGHIEP_VU = 1
            elif record.LOAI_CHUNG_TU == 256:
                record.THU_TU_NGHIEP_VU = 2
            elif record.LOAI_CHUNG_TU == 252:
                record.THU_TU_NGHIEP_VU = 3
            elif record.LOAI_CHUNG_TU == 253:
                record.THU_TU_NGHIEP_VU = 4
            elif record.LOAI_CHUNG_TU == 254:
                record.THU_TU_NGHIEP_VU = 5
            elif record.LOAI_CHUNG_TU == 251:
                record.THU_TU_NGHIEP_VU = 6
    