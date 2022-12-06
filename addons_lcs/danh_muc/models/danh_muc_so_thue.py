# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SO_THUE(models.Model):
    _name = 'so.thue'
    _description = 'Sổ thuế'

    name = fields.Char()
    line_ids = fields.One2many('so.thue.chi.tiet', 'SO_THUE_ID')

class SO_THUE_CHI_TIET(models.Model):
    _name = 'so.thue.chi.tiet'
    _description = 'Sổ thuế chi tiết'
    
    SO_THUE_ID = fields.Many2one('so.thue', ondelete="cascade")
    ID_CHUNG_TU = fields.Integer(string='Id chứng từ', help='Id chứng từ', required=True)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='RefNo')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='RefDate')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='PostedDate', required=True)
    TK_VAT_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk thuế VAT', help='VATAccount')
    MA_TK_VAT = fields.Char(string='Mã tk thuế VAT', help='VATAccount', compute='_compute_tai_khoan', store=True)
    TK_DOI_UNG_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk đối ứng', help='CorespondingAccountNumber')
    DIEN_GIAI_CHUNG = fields.Char(string='Diễn giải chung', help='JournalMemo')
    SO_TIEN_VAT = fields.Float(string='Số tiền vat', help='VATAmount')
    PHAN_TRAM_VAT = fields.Float(string='Phần trăm vat', help='VATRate')
    SO_TIEN_CHIU_VAT = fields.Float(string='Số tiền chịu thuế VAT', help='TurnOverAmount')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='InvNo')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='InvDate')

    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='AccountObjectID')
    MA_DOI_TUONG = fields.Char(string='Mã đối tượng', help='AccountObjectCode', compute='_compute_doi_tuong', store=True)
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='AccountObjectName')
    MA_SO_THUE_DOI_TUONG = fields.Char(string='MST đối tượng', help='CompanyTaxCode')
    
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='BranchID')
    THU_TU_TRONG_CHUNG_TU = fields.Integer(string='Thứ tự trong chứng từ', help='SortOrder')
    MUC_DICH_MUA_HANG = fields.Char(string='Mục đích mua hàng', help='?')
    TEN_MUC_DICH_MUA_HANG = fields.Char(string='Tên mục đích mua hàng', help='Tên mục đích mua hàng',compute='_compute_muc_dich', store=True)
    SO_TIEN_VAT_NGUYEN_TE = fields.Float(string='Số tiền vat nguyên tệ', help='VATAmountOC')
    SO_TIEN_CHIU_VAT_NGUYEN_TE = fields.Float(string='Số tiền chịu thuế nguyên tệ', help='TurnOverAmountOC')

    MAU_SO_HD_ID = fields.Many2one('danh.muc.mau.so.hd', string='Mẫu số HĐ', help='Mẫu số hđ')
    MAU_SO_HOA_DON = fields.Char(string='Mẫu số hóa đơn', help='InvTemplateNo',compute='_compute_so_hoa_don', store=True)
    CHI_TIET_ID = fields.Integer(string='Chi tiết chứng từ', help='Chi tiết chứng từ')
    CHI_TIET_MODEL = fields.Char(string='model chi tiết', help='model chi tiết')
    MODEL_CHUNG_TU = fields.Char(string='Model chứng từ', help='Model chứng từ', required=True)
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='RefType')
    KY_HIEU_HOA_DON = fields.Char(string='Ký hiệu hóa đơn', help='InvSeries')
    GIA_TRI_HHDV_CHUA_THUE = fields.Float(string='Giá trị HHDV chưa thuế', help='?')
    THUE_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang', string='% thuế gtgt', help='VATRate')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Description')
    MUC_DICH_MUA_HANG_ID = fields.Many2one('danh.muc.nhom.hhdv', string='Mục đính mua hàng', help='PurchasePurposeID')

    ID_CHUNG_TU_GOC = fields.Integer(string='ID chứng từ gốc', help='VoucherRefID')
    MODEL_CHUNG_TU_GOC = fields.Char(string='Model chứng từ gốc', help='VoucherRefID')
    
    LOAI_CHUNG_TU_GOC = fields.Char(string='Loại chứng từ gốc', help='VoucherRefType')
    SO_CHUNG_TU_GOC = fields.Char(string='Số chứng từ gốc', help='VoucherRefNo')
    NGAY_CHUNG_TU_GOC = fields.Date(string='Ngày chứng từ gốc', help='VoucherRefDate')
    NGAY_HACH_TOAN_CHUNG_TU_GOC = fields.Date(string='Ngày hạch toán chứng từ gốc', help='VoucherPostedDate')

    DS_LOAI_BANG = fields.Integer(string='Danh sách loại bảng', help='TableListType',compute='_compute_ds_loai_bang', store=True)
    CHI_TIET_ID_CHUNG_TU_GOC = fields.Integer(string='Chi tiết chứng từ gốc', help='VoucherRefDetailID')
    CHI_TIET_MODEL_CHUNG_TU_GOC = fields.Char(string='model chi tiết chứng từ gốc', help='VoucherRefDetailID')

    HHDV_KO_TONG_HOP_TREN_TO_KHAI_GTGT = fields.Boolean(string='Hàng hóa dịch vụ ko tổng hợp trên tờ khai GTGT', help='NotInVATDeclaration')
   
    
    
    @api.depends('CHI_TIET_MODEL','LOAI_CHUNG_TU')
    def _compute_ds_loai_bang(self):
        for record in self:
            if record.CHI_TIET_MODEL in ('sale.ex.tra.lai.hang.ban.chi.tiet','sale.ex.chi.tiet.hoa.don.ban.hang','sale.document.line','sale.ex.chi.tiet.giam.gia.hang.ban'):
                record.DS_LOAI_BANG = 0
            else:
                record.DS_LOAI_BANG = 1

    @api.depends('TK_VAT_ID')
    def _compute_so_hoa_don(self):
        for record in self:
            record.MAU_SO_HOA_DON = record.MAU_SO_HD_ID.MAU_SO_HD

    @api.depends('TK_VAT_ID')
    def _compute_tai_khoan(self):
        for record in self:
            record.MA_TK_VAT = record.TK_VAT_ID.SO_TAI_KHOAN

    @api.depends('MUC_DICH_MUA_HANG_ID')
    def _compute_muc_dich(self):
        for record in self:
            record.TEN_MUC_DICH_MUA_HANG = record.MUC_DICH_MUA_HANG_ID.TEN_NHOM_HHDV

    @api.depends('DOI_TUONG_ID')
    def _compute_doi_tuong(self):
        for record in self:
            if record.DOI_TUONG_ID:
                record.MA_DOI_TUONG = record.DOI_TUONG_ID.MA
    
    # @api.depends('DOI_TUONG_ID')
    # def _compute_doi_tuong(self):
    #     for record in self:
    #         record.TEN_DOI_TUONG = record.DOI_TUONG_ID.HO_VA_TEN
    #         record.MA_DOI_TUONG = record.DOI_TUONG_ID.MA
    #         record.MA_SO_THUE_DOI_TUONG = record.DOI_TUONG_ID.MA_SO_THUE