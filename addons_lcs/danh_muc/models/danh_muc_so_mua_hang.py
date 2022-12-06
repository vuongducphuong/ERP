# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class SO_MUA_HANG(models.Model):
    _name = 'so.mua.hang'
    _description = 'Sổ mua hàng'

    name = fields.Char()
    line_ids = fields.One2many('so.mua.hang.chi.tiet', 'SO_MUA_HANG_ID')

class SO_MUA_HANG_CHI_TIET(models.Model):
    _name = 'so.mua.hang.chi.tiet'
    _description = 'Sổ mua hàng chi tiết'
    
    SO_MUA_HANG_ID = fields.Many2one('so.mua.hang', ondelete="cascade")
    ID_CHUNG_TU = fields.Integer(string='Id chứng từ', help='Id chứng từ', required=True)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='RefNo')
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='RefType')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='RefDate')
    THU_TU_TRONG_CHUNG_TU = fields.Integer(string='Thứ tự trong chứng từ', help='SortOrder')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='PostedDate', required=True)
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='InvDate')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='InvNo')
    DIEN_GIAI_CHUNG = fields.Char(string='Diễn giải chứng từ', help='JournalMemo')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Description')
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Sản phẩm', help='InventoryItemID')
    MA_HANG = fields.Char(string='Mã sản phẩm', help='InventoryItemCode', compute='_compute_ma_hang', store=True)
    TEN_HANG = fields.Text(string='Tên sản phẩm', help='InventoryItemName', compute='_compute_ma_hang', store=True)
    KHO_ID = fields.Many2one('danh.muc.kho', string='Kho', help='StockID')
    MA_KHO = fields.Char(string='Mã kho', help='StockCode', compute='_compute_kho', store=True, )
    TEN_KHO = fields.Char(string='Tên kho', help='StockName', compute='_compute_kho', store=True, )
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản nợ', help='DebitAccount')
    MA_TK_NO = fields.Char(string='Mã tài khoản nợ', help='DebitAccount', compute='_compute_tk_no', store=True, )
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản có', help='CreditAccount')
    MA_TK_CO = fields.Char(string='Mã tài khoản có', help='CreditAccount', compute='_compute_tk_co', store=True, )
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Đơn vị tính', help='UnitID')
    TEN_DVT = fields.Char(string='Tên đơn vị tính', help='Tên đơn vị tính', compute='_compute_dvt', store=True, )
    
    SO_LUONG = fields.Float(string='Số lượng', help='PurchaseQuantity', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='UnitPrice', digits=decimal_precision.get_precision('DON_GIA'))
    SO_TIEN = fields.Float(string='Số tiền', help='PurchaseAmount')
    PHAN_TRAM_THUE_VAT = fields.Float(string='Thuế vat', help='VATRate')
    SO_TIEN_VAT = fields.Float(string='Tiền vat', help='VATAmount')
    SO_TIEN_VAT_NGUYEN_TE = fields.Float(string='Tiền vat nguyên tệ', help='VATAmountOC')
    TAI_KHOAN_VAT_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản vat', help='VATAccount')
    PHAN_TRAM_THUE_NHAP_KHAU = fields.Float(string='Thuế nhập khẩu', help='?')
    SO_TIEN_NHAP_KHAU = fields.Float(string='Tiền nhập khẩu', help='?')
    TAI_KHOAN_NHAP_KHAU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản nhập khẩu', help='?')
    PHAN_TRAM_CHIET_KHAU = fields.Float(string='Chiết khấu', help='DiscountRate')
    SO_TIEN_CHIET_KHAU = fields.Float(string='Tiền chiết khấu', help='DiscountAmount')
    SO_TIEN_CHIET_KHAU_NGUYEN_TE = fields.Float(string='Tiền chiết khấu nguyên tệ', help='DiscountAmountOC')
    TK_CHIET_KHAU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản chiết khấu', help='?')
    SO_LUONG_TRA_LAI = fields.Float(string='Số lượng trả lại', help='ReturnQuantity', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_TRA_LAI_THEO_DVT_CHINH = fields.Float(string='Số lượng trả lại', help='ReturnMainQuantity', compute='_compute_tinh_theo_dvt_chinh', store=True, digits=decimal_precision.get_precision('SO_LUONG'))
    SO_TIEN_TRA_LAI = fields.Float(string='Số tiền trả lại', help='ReturnAmount')
    SO_TIEN_TRA_LAI_NGUYEN_TE = fields.Float(string='Số tiền trả lại nguyên tệ', help='ReturnAmountOC')
    SO_TIEN_GIAM_TRU = fields.Float(string='Số tiền giảm trừ', help='ReduceAmount')
    SO_TIEN_GIAM_TRU_NGUYEN_TE = fields.Float(string='Số tiền giảm trừ nguyên tệ', help='ReduceAmountOC')
    SO_LO = fields.Char(string='Số lô', help='LotNo')
    NGAY_HET_HAN = fields.Date(string='Ngày hết hạn', help='DueDate')
    THOI_GIAN_BAO_HANH = fields.Float(string='Thời gian bảo hành', help='?')
    LA_HANG_KHUYEN_MAI = fields.Boolean(string='Là hàng khuyến mại', help='?')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='AccountObjectID')
    MA_DOI_TUONG = fields.Char(string='Mã đối tượng', help='AccountObjectCode', compute='_compute_doi_tuong', store=True, )
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='AccountObjectName' )
    DIA_CHI_DOI_TUONG = fields.Char(string='Tên đối tượng', help='AccountObjectAddress' )
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên mua hàng', help='EmployeeID')
    MA_NHAN_VIEN = fields.Char(string='Mã nhân viên mua hàng', help='EmployeeCode', compute='_compute_nhan_vien', store=True, )
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên mua hàng', help='EmployeeName', compute='_compute_nhan_vien', store=True, )
    # DON_MUA_HANG_ID = fields.Many2one('purchase.ex.don.mua.hang', string='Đơn mua hàng', help='Đơn mua hàng')
    # HOP_DONG_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang', string='Hợp đồng', help='Hợp đồng')
    MA_HOP_DONG = fields.Char(string='Mã hợp đồng', help='ContractCode')
    TEN_HOP_DONG = fields.Char(string='Tên hợp đồng', help='ContractName')
    DIEU_KHOAN_THANH_TOAN_ID = fields.Many2one('danh.muc.dieu.khoan.thanh.toan', string='Điều khoản thanh toán', help='Điều khoản thanh toán')
    MA_DIEU_KHOAN_THANH_TOAN = fields.Char(string='Mã điều khoản thanh toán', help='PaymentTermCode', compute='_compute_dieu_khoan_tt', store=True)
    TEN_DIEU_KHOAN_THANH_TOAN = fields.Char(string='Tên điều khoản thanh toán', help='PaymentTermName', compute='_compute_dieu_khoan_tt', store=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', readonly=True)
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='ProjectWorkID')
    CHI_TIET_ID = fields.Integer(string='Chi tiết id', help='Chi tiết id')
    CHI_TIET_MODEL = fields.Char(string='model chi tiết', help='model chi tiết')
    MODEL_CHUNG_TU = fields.Char(string='Model chứng từ', help='Model chứng từ', required=True)

    # Theo nguyên tệ
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True)
    TEN_LOAI_TIEN = fields.Char(string='Tên loại tiền', help='CurrencyID', compute='_compute_loai_tien', store=True, )
    TY_GIA = fields.Float(string='Tỉ giá', help='ExchangeRate')
    DON_GIA_NGUYEN_TE = fields.Float(string='Đơn giá', help='UnitPriceOC')
    
    # Theo đơn vị tính chính
    DVT_CHINH_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Đơn vị tính chính', help='MainUnitID')
    TY_LE_CHUYEN_DOI = fields.Float(string='Tỉ lệ chuyển đối', help='?')
    DON_GIA_THEO_DVT_CHINH = fields.Float(string='Đơn giá', help='MainUnitPrice', compute='_compute_tinh_theo_dvt_chinh', store=True)
    SO_LUONG_THEO_DVT_CHINH = fields.Float(string='Số lượng', help='MainQuantity', compute='_compute_tinh_theo_dvt_chinh', store=True, digits=decimal_precision.get_precision('SO_LUONG'))

    # Theo cả nguyên tệ và đơn vị tính chính
    DON_GIA_NGUYEN_TE_THEO_DVT_CHINH = fields.Float(string='Đơn giá', help='MainUnitPriceOC')

    # Compute
    @api.depends('KHO_ID')
    def _compute_kho(self):
        for record in self:
            record.MA_KHO = record.KHO_ID.MA_KHO
            record.TEN_KHO = record.KHO_ID.TEN_KHO

    @api.depends('DIEU_KHOAN_THANH_TOAN_ID')
    def _compute_dieu_khoan_tt(self):
        for record in self:
            record.MA_DIEU_KHOAN_THANH_TOAN = record.DIEU_KHOAN_THANH_TOAN_ID.MA_DIEU_KHOAN
            record.TEN_DIEU_KHOAN_THANH_TOAN = record.DIEU_KHOAN_THANH_TOAN_ID.TEN_DIEU_KHOAN
    
    @api.depends('TK_NO_ID')
    def _compute_tk_no(self):
        for record in self:
            record.MA_TK_NO = record.TK_NO_ID.SO_TAI_KHOAN
            record.TEN_TK_NO = record.TK_NO_ID.name
    
    @api.depends('TK_CO_ID')
    def _compute_tk_co(self):
        for record in self:
            record.MA_TK_CO = record.TK_CO_ID.SO_TAI_KHOAN
            record.TEN_TK_CO = record.TK_CO_ID.name

    @api.depends('DVT_ID')
    def _compute_dvt(self):
        for record in self:
            record.TEN_DVT = record.DVT_ID.DON_VI_TINH

    @api.depends('currency_id')
    def _compute_loai_tien(self):
        for record in self:
            record.TEN_LOAI_TIEN = record.currency_id.MA_LOAI_TIEN

    @api.depends('DOI_TUONG_ID')
    def _compute_doi_tuong(self):
        for record in self:
            # record.TEN_DOI_TUONG = record.DOI_TUONG_ID.HO_VA_TEN
            record.MA_DOI_TUONG = record.DOI_TUONG_ID.MA
            # record.DIA_CHI_DOI_TUONG = record.DOI_TUONG_ID.DIA_CHI

    @api.depends('MA_HANG_ID')
    def _compute_ma_hang(self):
        for record in self:
            record.MA_HANG = record.MA_HANG_ID.MA
            record.TEN_HANG = record.MA_HANG_ID.TEN

    @api.depends('NHAN_VIEN_ID')
    def _compute_nhan_vien(self):
        for record in self:
            record.MA_NHAN_VIEN = record.NHAN_VIEN_ID.MA
            record.TEN_NHAN_VIEN = record.NHAN_VIEN_ID.HO_VA_TEN

    @api.depends('TAI_KHOAN_NGAN_HANG_ID')
    def _compute_tai_khoan_ngan_hang(self):
        for record in self:
            record.SO_TAI_KHOAN_NGAN_HANG = record.TAI_KHOAN_NGAN_HANG_ID.acc_number
            record.TEN_NGAN_HANG = record.TAI_KHOAN_NGAN_HANG_ID.CHI_NHANH


    @api.depends('DVT_CHINH_ID')
    def _compute_tinh_theo_dvt_chinh(self):
        for record in self:
            record.DVT_CHINH_ID = record.MA_HANG_ID.DVT_CHINH_ID.id
            record.DON_GIA_THEO_DVT_CHINH = 0
            record.SO_LUONG_THEO_DVT_CHINH = 0
            record.SO_LUONG_TRA_LAI_THEO_DVT_CHINH = 0
            if record.DVT_CHINH_ID.id == record.DVT_ID.id:
                    record.DON_GIA_THEO_DVT_CHINH = record.DON_GIA
                    record.SO_LUONG_THEO_DVT_CHINH = record.SO_LUONG
                    record.SO_LUONG_TRA_LAI_THEO_DVT_CHINH = record.SO_LUONG_TRA_LAI
            else:
                if record.MA_HANG_ID.DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI_IDS:
                    for dv_chuyen_doi in record.MA_HANG_ID.DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI_IDS:
                        if record.DVT_ID.id == dv_chuyen_doi.DVT_ID.id:
                            if dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_NHAN':
                                record.DON_GIA_THEO_DVT_CHINH = record.DON_GIA*dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                record.SO_LUONG_THEO_DVT_CHINH = record.SO_LUONG*dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                record.SO_LUONG_TRA_LAI_THEO_DVT_CHINH = record.SO_LUONG_TRA_LAI*dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                            elif dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_CHIA':
                                if dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH != 0:
                                    record.DON_GIA_THEO_DVT_CHINH = record.DON_GIA/dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                    record.SO_LUONG_THEO_DVT_CHINH = record.SO_LUONGSO_LUONG_XUAT/dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                    record.SO_LUONG_TRA_LAI_THEO_DVT_CHINH = record.SO_LUONG_TRA_LAI/dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH