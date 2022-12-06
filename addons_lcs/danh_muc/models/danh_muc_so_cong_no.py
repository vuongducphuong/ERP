# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class SO_CONG_NO(models.Model):
    _name = 'so.cong.no'
    _description = 'Sổ công nợ'

    name = fields.Char()
    line_ids = fields.One2many('so.cong.no.chi.tiet', 'SO_CONG_NO_ID')

class SO_CONG_NO_CHI_TIET(models.Model):
    _name = 'so.cong.no.chi.tiet'
    _description = 'Sổ công nợ chi tiết'

    name = fields.Char(string="name")
    SO_CONG_NO_ID = fields.Many2one('so.cong.no', ondelete="cascade")
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh', readonly=True)
    ID_CHUNG_TU = fields.Integer(string='Id chứng từ', help='Id chứng từ', required=True)
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='RefType')
    TEN_LOAI_CHUNG_TU = fields.Char(string='Tên loại chứng từ', help='RefTypeName', compute='_compute_ten_loai_chung_tu', store=True)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='RefNo')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='RefDate')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='PostedDate', required=True)
    ID_HOA_DON = fields.Char(string='Hóa đơn', help='InvRefID')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='InvNo')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='InvDate')
    TK_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk', help='AccountNumber')
    MA_TK = fields.Char(string='Mã tk', help='AccountNumber', compute='_compute_tai_khoan', store=True,)
    TEN_TK = fields.Char(string='Tên tk', help='AccountName', compute='_compute_tai_khoan', store=True,)
    TINH_CHAT_TK = fields.Char(string='Tính chất tk', help='?', compute='_compute_tai_khoan', store=True,)
    TK_DOI_UNG_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk đối ứng', help='CorrespondingAccountNumber')
    MA_TK_DOI_UNG = fields.Char(string='Mã tk đối ứng', help='CorrespondingAccountNumber', compute='_compute_tai_khoan_doi_ung', store=True,)
    TINH_CHAT_TK_DOI_UNG = fields.Char(string='Tính chất tk đối ứng', help='?', compute='_compute_tai_khoan_doi_ung', store=True,)
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Đvt', help='UnitID')
    DON_GIA = fields.Float(string='Đơn giá', help='UnitPrice', digits=decimal_precision.get_precision('DON_GIA'))
    SO_LUONG = fields.Float(string='Số lượng', help='Quantity', digits=decimal_precision.get_precision('SO_LUONG'))
    GHI_NO = fields.Float(string='Ghi nợ', help='DebitAmount')
    GHI_CO = fields.Float(string='Ghi có', help='CreditAmount')
    DIEN_GIAI_CHUNG = fields.Char(string='Diễn giải chung', help='JournalMemo')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Description')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='AccountObjectID')
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='AccountObjectName')
    MA_DOI_TUONG = fields.Char(string='Mã đối tượng', help='AccountObjectCode', compute='_compute_doi_tuong', store=True,)
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', help='InventoryItemID')
    MA_HANG = fields.Char(string='Mã hàng', help='InventoryItemCode', compute='_compute_ma_hang', store=True)
    TEN_HANG = fields.Text(string='Tên hàng', help='InventoryItemName', compute='_compute_ma_hang', store=True)
    THU_TU_TRONG_CHUNG_TU = fields.Integer(string='Thứ tự trong chứng từ', help='SortOrder')
    NGAY_HET_HAN = fields.Date(string='Ngày hết hạn', help='DueDate')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên', help='EmployeeID')
    MA_NHAN_VIEN = fields.Char(string='Mã nhân viên', help='EmployeeCode', compute='_compute_nhan_vien', store=True)
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='EmployeeName', compute='_compute_nhan_vien', store=True)
    HOP_DONG_MUA_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang', string='Hợp đồng mua', help='PUcontractID')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng ban', help='ContractID')
    NGAY_KY_HOP_DONG_MUA = fields.Date(string='Ngày ký hợp đồng bán', help='PUSignDate', compute='_compute_hop_dong_mua', store=True)
    SO_HOP_DONG_MUA = fields.Char(string='Mã hợp đồng mua', help='PUContractCode', compute='_compute_hop_dong_mua', store=True)
    TEN_HOP_DONG_MUA = fields.Char(string='Tên hợp đồng mua', help='PUContractName', compute='_compute_hop_dong_mua', store=True)
    SO_HOP_DONG = fields.Char(string='Số hợp đồng', help='ContractCode')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='ProjectWorkID')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='OrganizationUnitID')    
    CHI_TIET_ID = fields.Integer(string='Chi tiết', help='Chi tiết')
    CHI_TIET_MODEL = fields.Char(string='model chi tiết', help='model chi tiết')
    MODEL_CHUNG_TU = fields.Char(string='Model chứng từ', help='Model chứng từ', required=True)
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    
    DON_MUA_HANG_ID = fields.Many2one('purchase.ex.don.mua.hang', string='Đơn mua hàng', help='PUOrderRefID')
    # Theo loại tiền
    currency_id = fields.Many2one('res.currency', string='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True)
    TY_GIA = fields.Float(string='Tỷ giá', help='ExchangeRate')
    DON_GIA_NGUYEN_TE = fields.Float(string='Đơn giá nguyên tệ', help='UnitPriceOC')
    GHI_NO_NGUYEN_TE = fields.Float(string='Ghi nợ nguyên tệ', help='DebitAmountOC')
    GHI_CO_NGUYEN_TE = fields.Float(string='Ghi có nguyên tệ', help='CreditAmountOC')
    GIA_VON = fields.Float(string='Giá vốn', help='UnitPrice')
    TY_LE_CHIET_KHAU = fields.Float(string='Tỷ lệ chiết khấu', help='?')
    TIEN_CHIET_KHAU = fields.Float(string='Tiền chiết khấu', help='?')
    DIEU_KHOAN_TT_ID = fields.Many2one('danh.muc.dieu.khoan.thanh.toan', string='Điều khoản tt', help='PaymentTermID')
    LOAI_HACH_TOAN = fields.Selection([('1', 'Chứng từ ghi nợ'), ('2', 'Chứng từ ghi có')], string='Loại hạch toán' , help='EntryType')
    
    # Theo ĐVT chính
    DVT_CHINH_ID = fields.Many2one('danh.muc.don.vi.tinh', string='MainUnitID')
    TY_LE_CHUYEN_DOI = fields.Float(string='Tỷ lệ chuyển đổi',help='?')
    SO_LUONG_THEO_DVT_CHINH = fields.Float(string='Số lượng theo đvt chính',help='MainQuantity', compute='_compute_tinh_theo_dvt_chinh', store=True, digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA_THEO_DVT_CHINH = fields.Float(string='Đơn giá theo đvt chính',help='MainUnitPrice', compute='_compute_tinh_theo_dvt_chinh', store=True)

    # Theo loại tiền và ĐVT chính
    DON_GIA_NGUYEN_TE_THEO_DVT_CHINH = fields.Float(string='Đơn giá nguyên tệ theo đvt chính',help='MainUnitPriceOC')

    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê',help='ListItemID')
    THU_TU_CHI_TIET_GHI_SO = fields.Integer(string='Thứ tự chi tiết ghi sổ', help='DetailPostOrder')
    @api.depends('TK_ID')
    def _compute_tai_khoan(self):
        for record in self:
            record.MA_TK = record.TK_ID.SO_TAI_KHOAN
            record.TEN_TK = record.TK_ID.TEN_TAI_KHOAN
            record.TINH_CHAT_TK = record.TK_ID.TINH_CHAT

    @api.depends('NHAN_VIEN_ID')
    def _compute_nhan_vien(self):
        for record in self:
            record.MA_NHAN_VIEN = record.NHAN_VIEN_ID.MA
            record.TEN_NHAN_VIEN = record.NHAN_VIEN_ID.HO_VA_TEN

    @api.depends('TK_DOI_UNG_ID')
    def _compute_tai_khoan_doi_ung(self):
        for record in self:
            record.MA_TK_DOI_UNG = record.TK_DOI_UNG_ID.SO_TAI_KHOAN
            record.TEN_NHAN_VIEN = record.TK_DOI_UNG_ID.TINH_CHAT

    @api.depends('DOI_TUONG_ID')
    def _compute_doi_tuong(self):
        for record in self:
            record.MA_DOI_TUONG = record.DOI_TUONG_ID.MA

    @api.depends('MA_HANG_ID')
    def _compute_ma_hang(self):
        for record in self:
            record.MA_HANG = record.MA_HANG_ID.MA
            record.TEN_HANG = record.MA_HANG_ID.TEN

    @api.depends('HOP_DONG_MUA_ID')
    def _compute_hop_dong_mua(self):
        for record in self:
            if record.HOP_DONG_MUA_ID:
                record.NGAY_KY_HOP_DONG_MUA = record.HOP_DONG_MUA_ID.NGAY_KY
                record.SO_HOP_DONG_MUA = record.HOP_DONG_MUA_ID.SO_HOP_DONG
                record.TEN_HOP_DONG_MUA = record.HOP_DONG_MUA_ID.TRICH_YEU

    @api.depends('LOAI_CHUNG_TU')
    def _compute_ten_loai_chung_tu(self):
        for record in self:
            loai_chung_tu = self.env['danh.muc.reftype'].search([('REFTYPE', '=', record.LOAI_CHUNG_TU)],limit=1)
            if loai_chung_tu:
                ten_loai_chung_tu = loai_chung_tu.REFTYPENAME
            else:
                ten_loai_chung_tu = ''
            record.TEN_LOAI_CHUNG_TU = ten_loai_chung_tu

    # @api.depends('GHI_NO','GHI_NO_NGUYEN_TE','GHI_CO','GHI_CO_NGUYEN_TE')
    # def _compute_loai_hach_toan(self):
    #     for record in self:
    #         if record.GHI_NO > 0 or record.GHI_NO_NGUYEN_TE > 0:
    #             record.LOAI_HACH_TOAN = '1'
    #         else:
    #             record.LOAI_HACH_TOAN = '2'
    @api.depends('DVT_CHINH_ID')
    def _compute_tinh_theo_dvt_chinh(self):
        for record in self:
            record.DVT_CHINH_ID = record.MA_HANG_ID.DVT_CHINH_ID.id
            record.DON_GIA_THEO_DVT_CHINH = 0
            record.SO_LUONG_THEO_DVT_CHINH = 0
            if record.DVT_CHINH_ID.id == record.DVT_ID.id:
                    record.DON_GIA_THEO_DVT_CHINH = record.DON_GIA
                    record.SO_LUONG_THEO_DVT_CHINH = record.SO_LUONG
            else:
                if record.MA_HANG_ID.DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI_IDS:
                    for dv_chuyen_doi in record.MA_HANG_ID.DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI_IDS:
                        if record.DVT_ID.id == dv_chuyen_doi.DVT_ID.id:
                            if dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_NHAN':
                                record.DON_GIA_THEO_DVT_CHINH = record.DON_GIA*dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                record.SO_LUONG_THEO_DVT_CHINH = record.SO_LUONG*dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                            elif dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_CHIA':
                                if dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH != 0:
                                    record.DON_GIA_THEO_DVT_CHINH = record.DON_GIA/dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                    record.SO_LUONG_THEO_DVT_CHINH = record.SO_LUONG/dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH

    @api.model
    def create(self, values):
        result = super(SO_CONG_NO_CHI_TIET, self).create(values)
    
        return result
    