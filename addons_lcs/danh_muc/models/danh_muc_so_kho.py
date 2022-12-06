# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.exceptions import ValidationError

class SO_KHO(models.Model):
    _name = 'so.kho'
    _description = 'Sổ kho'

    name = fields.Char()
    line_ids = fields.One2many('so.kho.chi.tiet', 'SO_KHO_ID')
    
class SO_KHO_CHI_TIET(models.Model):
    _name = 'so.kho.chi.tiet'
    _description = 'Sổ kho chi tiết'

    SO_KHO_ID = fields.Many2one('so.kho', string='Sổ kho', ondelete="cascade")
    ID_CHUNG_TU = fields.Integer(string='Id chứng từ', help='Id chứng từ', required=True)
    SO_CHUNG_TU = fields.Char(string='Số chứng từ', help='RefNo')
    LOAI_CHUNG_TU = fields.Char(string='Loại chứng từ', help='RefType')
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='RefDate')
    THU_TU_TRONG_CHUNG_TU = fields.Integer(string='Thứ tự trong chứng từ', help='SortOrder')
    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='PostedDate', required=True)
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True)
    TEN_LOAI_TIEN = fields.Char(string='Tên loại tiền', help='CurrencyID', compute='_compute_loai_tien', store=True, )
    TY_GIA = fields.Float(string='Tỉ giá', help='ExchangeRate')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='?')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='?')
    DIEN_GIAI_CHUNG = fields.Char(string='Diễn giải chứng từ', help='JournalMemo')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Description,')
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Sản phẩm', help='InventoryItemID')
    MA_HANG = fields.Char(string='Mã sản phẩm', help='InventoryItemCode', compute='_compute_ma_hang', store=True)
    TEN_HANG = fields.Text(string='Tên sản phẩm', help='InventoryItemName', compute='_compute_ma_hang', store=True)
    KHO_ID = fields.Many2one('danh.muc.kho', string='Kho', help='StockID')
    MA_KHO = fields.Char(string='Mã kho', help='StockCode', compute='_compute_kho', store=True, )
    TEN_KHO = fields.Char(string='Tên kho', help='StockName', compute='_compute_kho', store=True, )
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='AccountNumber')
    MA_TK_NO = fields.Char(string='Mã tài khoản', help='AccountNumber', compute='_compute_tk_no', store=True, )
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản đối ứng', help='CorrespondingAccountNumber')
    MA_TK_CO = fields.Char(string='Mã tài khoản đối ứng', help='CorrespondingAccountNumber', compute='_compute_tk_co', store=True, )
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Đơn vị tính', help='UnitID')
    TEN_DVT = fields.Char(string='Tên đơn vị tính', help='UnitID', compute='_compute_dvt', store=True, )
    SO_LUONG_NHAP = fields.Float(string='Số lượng nhập', help='InwardQuantity', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_XUAT = fields.Float(string='Số lượng xuất', help='OutwardQuantity', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='UnitPrice', digits=decimal_precision.get_precision('DON_GIA'))
    SO_TIEN_NHAP = fields.Float(string='Số tiền nhập', help='InwardAmount')
    SO_TIEN_XUAT = fields.Float(string='Số tiền xuất', help='OutwardAmount')
    PHAN_TRAM_THUE_VAT = fields.Float(string='Thuế vat', help='?')
    SO_TIEN_VAT = fields.Float(string='Tiền vat', help='?')
    TAI_KHOAN_VAT_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản vat', help='?')
    PHAN_TRAM_THUE_NHAP_KHAU = fields.Float(string='Thuế nhập khẩu', help='?')
    SO_TIEN_NHAP_KHAU = fields.Float(string='Tiền nhập khẩu', help='?')
    TAI_KHOAN_NHAP_KHAU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản nhập khẩu', help='?')
    PHAN_TRAM_CHIET_KHAU = fields.Float(string='Chiết khấu', help='?')
    SO_TIEN_CHIET_KHAU = fields.Float(string='Tiền chiết khấu', help='?')
    TK_CHIET_KHAU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản chiết khấu', help='?')
    SO_LO = fields.Char(string='Số lô', help='LotNo')
    NGAY_HET_HAN = fields.Date(string='Ngày hết hạn', help='ExpiryDate')
    THOI_GIAN_BAO_HANH = fields.Float(string='Thời gian bảo hành', help='?')
    LA_HANG_KHUYEN_MAI = fields.Boolean(string='Là hàng khuyến mại', help='IsPromotion')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='AccountObjectID')
    MA_DOI_TUONG = fields.Char(string='Mã đối tượng', help='AccountObjectCode', compute='_compute_doi_tuong', store=True, )
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='AccountObjectName', compute='_compute_doi_tuong', store=True, )
    DIA_CHI_DOI_TUONG = fields.Char(string='Địa chỉ đối tượng', help='AccountObjectAddress', compute='_compute_doi_tuong', store=True, )
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên bán hàng', help='EmployeeID')
    MA_NHAN_VIEN = fields.Char(string='Mã nhân viên bán hàng', help='EmployeeCode', compute='_compute_nhan_vien', store=True, )
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên bán hàng', help='EmployeeName', compute='_compute_nhan_vien', store=True, )
    # DON_BAN_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn bán hàng', help='Đơn bán hàng')
    # HOP_DONG_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng', help='Hợp đồng')
    MA_HOP_DONG = fields.Char(string='Mã hợp đồng', help='ContractCode')
    TEN_HOP_DONG = fields.Char(string='Tên hợp đồng', help='Tên hợp đồng')
    DIEU_KHOAN_THANH_TOAN_ID = fields.Many2one('danh.muc.dieu.khoan.thanh.toan', string='Điều khoản thanh toán', help='?')
    MA_DIEU_KHOAN_THANH_TOAN = fields.Char(string='Mã điều khoản thanh toán', help='?')
    TEN_DIEU_KHOAN_THANH_TOAN = fields.Char(string='Tên điều khoản thanh toán', help='?')
    NGUOI_LIEN_HE = fields.Char(string='Người liên hệ',)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', readonly=True)
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='OrganizationUnitID')
    CHI_TIET_ID = fields.Integer(string='Chi tiết', help='Chi tiết')
    CHI_TIET_MODEL = fields.Char(string='model chi tiết', help='model chi tiết')
    MODEL_CHUNG_TU = fields.Char(string='Model chứng từ', help='Model chứng từ', required=True)
    LOAI_KHU_VUC_NHAP_XUAT = fields.Selection([('1', 'Nhập kho'), ('2', 'chuyển kho'), ('3', 'Xuất kho')], string='InOutWardType')
    PHUONG_THUC_THANH_TOAN = fields.Selection([('0', 'Loại 0'), ('1', 'Loại 2')], string='UnitPriceMethod')
    LOAI_KHONG_CAP_NHAT_GIA_XUAT = fields.Selection([('0', 'Loại 0'), ('1', 'Loại 1'), ('2', 'Loại 2'), ('3', '')], string='UnUpdateOutwardPriceType')
    KHONG_CAP_NHAT_GIA_XUAT = fields.Boolean(string='Không cập nhật giá xuất', help='IsUnUpdateOutwardPrice')
    GIA_VON = fields.Float(string='Giá vốn', help='UnitPrice')

    # Theo đơn vị tính chính
    DVT_CHINH_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Đơn vị tính chính', help='MainUnitID', compute='_compute_tinh_theo_dvt_chinh', store=True)
    TY_LE_CHUYEN_DOI = fields.Float(string='Tỉ lệ chuyển đổi dvt chính', help='MainConvertRate')
    PHEP_TINH_CHUYEN_DOI = fields.Char(string='Phép tính chuyển đổi dvt chính', help='?')
    SO_LUONG_NHAP_THEO_DVT_CHINH = fields.Float(string='Số lượng nhập theo dvt chính', help='MainInwardQuantity', compute='_compute_tinh_theo_dvt_chinh', store=True, digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_XUAT_THEO_DVT_CHINH = fields.Float(string='Số lượng xuất theo dvt chính', help='MainOutwardQuantity', compute='_compute_tinh_theo_dvt_chinh', store=True, digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA_THEO_DVT_CHINH = fields.Float(string='Đơn giá chính', help='MainUnitPrice', compute='_compute_tinh_theo_dvt_chinh', store=True)
    NGAY_NHAP_HANG = fields.Date(string='Ngày đặt hàng', help='?')
    LAP_RAP_THAO_DO_ID = fields.Integer(string='ID lắp ráp tháo dỡ', help='?')
    SO_CHUNG_TU_NHAP_DOI_TRU = fields.Integer(string='Số chứng từ nhập đối trừ', help='ConfrontingRefDetailID')
    TOAN_TU_QUY_DOI = fields.Selection([('NHAN', '*'),('CHIA', '/'),],string="Toán tử quy đổi",help = 'ExchangeRateOperator')
    LA_NHAP_KHO = fields.Boolean(string='Là nhập kho', help='IsInward') 

   #vu them 
 
    STT_LOAI_CHUNG_TU = fields.Datetime(string='Số thứ tự loại  chứng từ', help='INRefOrder', compute='_compute_STT_LOAI_CHUNG_TU', store=True )
    MA_DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='JobID')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='ProjectWorkID')
    ID_CHUNG_TU_XUAT_KHO = fields.Integer(string='Id chứng từ xuất kho ', help='OutwardRefID')
    MODEL_CHUNG_TU_XUAT_KHO = fields.Char(string='Model chứng từ xuất kho', help='Model chứng từ xuất kho')
    ID_CHUNG_TU_XUAT_KHO_CHI_TIET = fields.Integer(string='Id chứng từ xuất kho chi tiết', help='OutwardRefDetailID')
    MODEL_CHUNG_TU_XUAT_KHO_CHI_TIET = fields.Char(string='Model chứng từ xuất kho chi tiết', help='Model chứng từ xuất kho chi tiết')
    @api.model
    def create(self, vals):
        result = super(SO_KHO_CHI_TIET, self).create(vals)
        result._validate()
        return result

    def _validate(self):
        # Validate số lượng xuất
        allow_exceed = self.env['ir.config_parameter'].sudo().get_param('he_thong.CHO_PHEP_XUAT_QUA_SO_LUONG_TON')
        if not allow_exceed and self.SO_LUONG_XUAT_THEO_DVT_CHINH > 0:
            if not self.KHO_ID:
                raise ValidationError("Ghi sổ không thành công. Thiếu thông tin kho!")
            so_luong_ton = self.MA_HANG_ID.lay_so_luong_ton(self.KHO_ID.id, self.NGAY_HACH_TOAN + ' 00:00:00', self.NGAY_HACH_TOAN + ' 23:59:59',self.CHI_NHANH_ID.id)
            if so_luong_ton < self.SO_LUONG_XUAT_THEO_DVT_CHINH:
                raise ValidationError("""Ghi sổ không thành công.\nKhông thể xuất vật tư, hàng hóa <%s - %s> quá số lượng tồn trong kho <%s - %s>. Số lượng tồn trong kho này hiện tại là: %s""" 
                    % (self.MA_HANG, self.TEN_HANG, self.MA_KHO, self.TEN_KHO, so_luong_ton))

    # Compute
    @api.depends('NGAY_HACH_TOAN')
    def _compute_STT_LOAI_CHUNG_TU(self):
        for record in self:
            record.STT_LOAI_CHUNG_TU = record.NGAY_HACH_TOAN


    @api.depends('KHO_ID')
    def _compute_kho(self):
        for record in self:
            record.MA_KHO = record.KHO_ID.MA_KHO
            record.TEN_KHO = record.KHO_ID.TEN_KHO
    
    @api.depends('TK_NO_ID')
    def _compute_tk_no(self):
        for record in self:
            record.MA_TK_NO = record.TK_NO_ID.SO_TAI_KHOAN
            record.TEN_TK_NO = record.TK_NO_ID.TEN_TAI_KHOAN
    
    @api.depends('TK_CO_ID')
    def _compute_tk_co(self):
        for record in self:
            record.MA_TK_CO = record.TK_CO_ID.SO_TAI_KHOAN
            record.TEN_TK_CO = record.TK_CO_ID.TEN_TAI_KHOAN

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
            record.TEN_DOI_TUONG = record.DOI_TUONG_ID.HO_VA_TEN
            record.MA_DOI_TUONG = record.DOI_TUONG_ID.MA
            record.DIA_CHI_DOI_TUONG = record.DOI_TUONG_ID.DIA_CHI
            record.MA_SO_THUE_DOI_TUONG = record.DOI_TUONG_ID.MA_SO_THUE

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
            record.SO_TAI_KHOAN_NGAN_HANG = record.TAI_KHOAN_NGAN_HANG_ID.SO_TAI_KHOAN
            record.TEN_NGAN_HANG = record.TAI_KHOAN_NGAN_HANG_ID.CHI_NHANH

    @api.depends('MA_HANG_ID')
    def _compute_tinh_theo_dvt_chinh(self):
        for record in self:
            record.DVT_CHINH_ID = record.MA_HANG_ID.DVT_CHINH_ID.id
            record.DON_GIA_THEO_DVT_CHINH = 0
            record.SO_LUONG_NHAP_THEO_DVT_CHINH = 0
            record.SO_LUONG_XUAT_THEO_DVT_CHINH = 0
            if record.DVT_CHINH_ID.id == record.DVT_ID.id:
                    record.DON_GIA_THEO_DVT_CHINH = record.DON_GIA
                    record.SO_LUONG_NHAP_THEO_DVT_CHINH = record.SO_LUONG_NHAP
                    record.SO_LUONG_XUAT_THEO_DVT_CHINH = record.SO_LUONG_XUAT
            else:
                if record.MA_HANG_ID.DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI_IDS:
                    for dv_chuyen_doi in record.MA_HANG_ID.DANH_MUC_VAT_TU_HANG_HOA_DON_VI_CHUYEN_DOI_IDS:
                        if record.DVT_ID.id == dv_chuyen_doi.DVT_ID.id:
                            if dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_NHAN':
                                record.DON_GIA_THEO_DVT_CHINH = record.DON_GIA*dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                record.SO_LUONG_NHAP_THEO_DVT_CHINH = record.SO_LUONG_NHAP*dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                record.SO_LUONG_XUAT_THEO_DVT_CHINH = record.SO_LUONG_XUAT*dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                            elif dv_chuyen_doi.PHEP_TINH_CHUYEN_DOI == 'PHEP_CHIA':
                                if dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH != 0:
                                    record.DON_GIA_THEO_DVT_CHINH = record.DON_GIA/dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                    record.SO_LUONG_NHAP_THEO_DVT_CHINH = record.SO_LUONG_NHAP/dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                                    record.SO_LUONG_XUAT_THEO_DVT_CHINH = record.SO_LUONG_XUAT/dv_chuyen_doi.TY_LE_CHUYEN_DOI_VA_DON_VI_CHINH
                    