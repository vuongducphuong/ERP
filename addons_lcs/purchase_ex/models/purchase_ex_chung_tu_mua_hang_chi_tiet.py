# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime
from odoo import api, fields, models, _, helper
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round

class PurchaseDocumentLine(models.Model):
    _name = 'purchase.document.line'
    _description = 'Chứng từ mua hàng chi tiết'
    _order = 'NGAY_HACH_TOAN desc,order_id,sequence,id'

    DIEN_GIAI_THUE = fields.Char(string='Diễn giải')
    name = fields.Text(string='Tên hàng')
    SO_LUONG = fields.Float(string='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    # Nếu có SO_LUONG_YEU_CAU thì trường SO_LUONG là số lượng thực nhập
    SO_LUONG_YEU_CAU = fields.Float(string='SL yêu cầu', help='Số lượng yêu cầu',digits=decimal_precision.get_precision('SO_LUONG'))
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đơn vị tính')
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', required=True)
    DON_GIA = fields.Float(string='Đơn giá', digits=decimal_precision.get_precision('DON_GIA'))#,  currency_field='currency_id') #Mạnh sửa bug2022: Đơn giá không cho phép nhập dấu phẩy
    THANH_TIEN_QUY_DOI = fields.Monetary(string='Thành tiền quy đổi', help='Thành tiền quy đổi', currency_field='base_currency_id')
    TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='Tiền thuế GTGT quy đổi', help='Tiền thuế GTGT quy đổi', currency_field='base_currency_id')
    TIEN_THUE_GTGT_QUY_DOI_NHAP_KHAU = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế GTGT', currency_field='base_currency_id')
    TIEN_THUE_GTGT_THEO_TGXQ = fields.Monetary(string='Tiền thuế GTGT theo TGXQ', help='Tiền thuế giá trị gia tăng theo tỷ giá xuất quỹ', currency_field='base_currency_id')
    CHENH_LECH_TIEN_THUE_GTGT = fields.Monetary(string='Chênh lệch tiền thuế GTGT', help='Chênh lệch tiền thuế giá trị gia tăng', currency_field='base_currency_id')
    TIEN_THUE_TTDB_QUY_DOI = fields.Monetary(string='Tiền thuế TTĐB', help='Tiền thuế TTĐB', currency_field='base_currency_id')
    TIEN_THUE_NK_QUY_DOI = fields.Monetary(string='Tiền thuế NK quy đổi', help='Tiền thuế NK quy đổi', currency_field='base_currency_id')
    TK_THUE_BVMT = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản thuế bảo vệ môi trường', help='Tài khoản thuế bảo vệ môi trường')
    TIEN_THUE_BVMT = fields.Monetary(string='Tiền thuế bảo vệ môi trường', help='Tiền thuế bảo vệ môi trường', currency_field='currency_id')
    TIEN_THUE_BVMT_QUY_DOI = fields.Monetary(string='Tiền thuế bảo vệ môi trường quy đổi', help='Tiền thuế bảo vệ môi trường quy đổi', currency_field='base_currency_id')
    THANH_TIEN = fields.Monetary(string='Thành tiền', store=True, currency_field='currency_id')
    TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu',currency_field='currency_id')
    TIEN_CHIET_KHAU_QUY_DOI = fields.Monetary(string='Tiền chiết khấu quy đổi', help='Tiền chiết khấu quy đổi', currency_field='base_currency_id')
    HOP_DONG_MUA_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang', string='Hợp đồng mua', help='Hợp đồng mua')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục CP', help='Khoản mục CP')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn vị')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Hợp đồng bán')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    THANH_PHAM_ID = fields.Many2one('stock.ex.lenh.san.xuat.chi.tiet.thanh.pham',string='Thành phẩm')
    LENH_SAN_XUAT_ID = fields.Many2one('stock.ex.lenh.san.xuat',string='Lệnh sản xuất')
    NHOM_HHDV_ID = fields.Many2one('danh.muc.nhom.hhdv', string='Nhóm HHDV mua vào', help='Nhóm HHDV mua vào', default=lambda self: self.lay_nhom_hhdv_mac_dinh())
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng THCP')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế GTGT', currency_field='currency_id')
    PHI_TRUOC_HAI_QUAN = fields.Monetary(string='Phí trước hải quan', help='Phí trước hải quan', currency_field='base_currency_id')
    GIA_TRI_NHAP = fields.Monetary(string='Giá trị nhập', help='Giá trị nhập', currency_field='base_currency_id')
    TY_GIA_XUAT_QUY = fields.Float(string='Tỷ giá xuất quỹ', help='Tỷ giá xuất quỹ')
    THANH_TIEN_SAU_TY_GIA_XUAT_QUY = fields.Monetary(string='Thành tiền sau CK theo TGXQ', help='Thành tiền sau chiết khấu theo tỷ giá xuất quỹ', currency_field='base_currency_id')
    CHENH_LECH = fields.Monetary(string='Tỷ giá xuất quỹ', help='Tỷ giá xuất quỹ', currency_field='base_currency_id')
    TK_XU_LY_CHENH_LECH = fields.Many2one('danh.muc.he.thong.tai.khoan',string='TK xử lý chênh lệch', help='Tài khoản xử lý chênh lệch')
    CHI_TIET_DON_MUA_HANG_ID = fields.Many2one('purchase.ex.don.mua.hang.chi.tiet',string='Đơn mua hàng chi tiết', help='Đơn mua hàng chi tiết')
    SO_LO1 = fields.Char(string='Số lô',related='SO_LO')
    HAN_SU_DUNG1 = fields.Date('Hạn sử dụng',related='HAN_SU_DUNG')
    GIA_TINH_THUE_NK = fields.Monetary(string='Giá tính thuế NK', help='Giá tính thuế nhập khẩu', currency_field='base_currency_id')
    THUE_NK = fields.Float(string='% thuế NK', help='% thuế nhập khẩu')
    TIEN_THUE_NK = fields.Monetary(string='Tiền thuế NK', help='Tiền thuế nhập khẩu', currency_field='base_currency_id')
    TK_THUE_NK_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK thuế NK', help='TK thuế nhập khẩu')
    THUE_TTDB = fields.Float(string='% thuế TTĐB', help='% thuế tiêu thụ đặc biệt')
    TIEN_THUE_TTDB = fields.Monetary(string='Tiền thuế TTĐB', help='Tiền thuế tiêu thụ đặc biệt', currency_field='base_currency_id')
    TK_THUE_TTDB_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK thuế TTĐB', help='TK thuế tiêu thụ đặc biệt')
    TK_DU_THUE_GTGT_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TKĐƯ thuế GTGT', help='Tài khoản đối ứng thuế Giá trị gia tăng', oldname='TK_THUE_DOI_UNG')
    TK_THUE_GTGT_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK thuế GTGT', help='TK thuế GTGT')
    # Updated 2019-07-30 by anhtuan: Do không thể thay đổi DOI_TUONG_ID ở detail, nên để related tới master
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng', related='order_id.DOI_TUONG_ID', store=True)
    TEN_TRUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng')
    TY_LE_CK = fields.Float(string='Chiết khấu (%)', digits=decimal_precision.get_precision('Discount'))
    KHO_ID = fields.Many2one('danh.muc.kho', string='Kho')
    # TK_KHO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK kho', help='Tài khoản kho',related='TK_NO_ID')
    # TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chi phí', help='Tài khoản chi phí')
    # TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK công nợ', help='Tài khoản công nợ')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK kho', help='Tài khoản nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK công nợ/TK tiền', help='Tài khoản có')
    CHI_PHI_MUA_HANG = fields.Monetary(string='Chi phí mua hàng', currency_field='base_currency_id')
    GIA_TRI_NHAP_KHO = fields.Monetary(string='Giá trị nhập kho', currency_field='base_currency_id')
    SO_LO = fields.Char(string='Số lô')
    HAN_SU_DUNG = fields.Date('Hạn sử dụng')
    DON_MUA_HANG_ID = fields.Many2one('purchase.ex.don.mua.hang', string='Đơn mua hàng')
    THUE_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang', string='% thuế GTGT', ondelete='restrict')
    amount = fields.Float()
    TONG_TIEN_THANH_TOAN = fields.Monetary(string="Amount",store=True, currency_field='currency_id')
    sequence = fields.Integer()
    # currency_id = fields.Many2one('res.currency', related='order_id.currency_id', store=True, readonly=True)
    NHOM_HHDV = fields.Char(string='Nhóm HHDV mua vào')
    SO_HOA_DON_DETAIL = fields.Char(string='Số hóa đơn')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn')
    MA_SO_THUE_NCC = fields.Char(string='Mã số thuế NCC')
    MA_NCC_ID = fields.Many2one('res.partner', string='Mã NCC', help='Mã NCC')
    TEN_NCC = fields.Char(string='Tên NCC', help='Tên NCC')
    DIA_CHI_NCC = fields.Char(string='Địa chỉ NCC')
    TIEN_THUE = fields.Monetary(string='Tiền thuế', help='Tiền thuế', currency_field='base_currency_id', store=True)
    DVT_CHINH_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT chính', help='ĐVT chính')
    DON_GIA_THEO_DVT_CHINH = fields.Float(string='Đơn giá theo đvt chính', help='Đơn giá theo đvt chính', compute='_compute_theo_DON_GIA', store=True, )
    SO_LUONG_THEO_DVT_CHINH = fields.Float(string='Số lượng theo đvt chính', help='Số lượng theo đvt chính', digits=decimal_precision.get_precision('SO_LUONG'), compute='_compute_so_luong_theo_dvt_chinh', store=True)
    SO_PHAN_BO_LAN_NAY = fields.Float(string='Số phân bổ lần này' ) 

    DON_GIA_QUY_DOI = fields.Float(string='Đơn giá quy đổi')#,  currency_field='currency_id') #Mạnh sửa bug2529: Thêm 1 đơn giá quy đổi để lấy cột đơn giá cho mẫu in khi trên chứng từ loại tiền là ngoại tệ
    # Masters
    order_id = fields.Many2one('purchase.document', string='Order Reference', index=True, ondelete='cascade')
    HOA_DON_ID = fields.Many2one('purchase.ex.hoa.don.mua.hang', string='Hóa đơn', ondelete='set null')
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng', compute='_compute_doi_tuong')
    # currency_id = fields.Many2one(related='order_id.currency_id', store=True, string='Currency', readonly=True)
    NGAY_DAT_HANG = fields.Datetime(related='order_id.NGAY_DAT_HANG', string='Order Date', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='order_id.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá',related='order_id.TY_GIA', store=True)
    MAU_SO_HD_ID = fields.Many2one('danh.muc.mau.so.hd', string='Mẫu số HĐ', help='Mẫu số hđ')
    KY_HIEU_HOA_DON = fields.Char(string='Ký hiệu hóa đơn', help='InvSeries')
    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết',help='Thứ tự sắp xếp các dòng chi tiết')
    CHI_PHI_KHONG_HOP_LY = fields.Boolean(string='CP không hợp lý', help='CP không hợp lý')

    NGAY_HACH_TOAN = fields.Date(string='Ngày hạch toán', help='Ngày hạch toán' , related='order_id.NGAY_HACH_TOAN', store=True)
    NGAY_CHUNG_TU = fields.Date(string='Ngày chứng từ', help='Ngày chứng từ', related='order_id.NGAY_CHUNG_TU')
    # DOI_TUONG_ID = fields.Many2one(string='Khách hàng', help='Khách hàng', related='order_id.DOI_TUONG_ID', store=True)


    # Xem xét việc tính DON_GIA_THEO_DVT_CHINH theo cả currency_id
    # Tuy nhiên, do giới hạn về resource nên sẽ làm khi có issue

    CHIEU_DAI = fields.Float(string='Chiều dài', digits=decimal_precision.get_precision('KICH_THUOC'))
    CHIEU_RONG = fields.Float(string='Chiều rộng', digits=decimal_precision.get_precision('KICH_THUOC'))
    CHIEU_CAO = fields.Float(string='Chiều cao', digits=decimal_precision.get_precision('KICH_THUOC'))
    BAN_KINH = fields.Float(string='Bán kính', digits=decimal_precision.get_precision('KICH_THUOC'))
    LUONG = fields.Float(string='Lượng', default=1)

    @api.onuichange('MA_HANG_ID')
    def thay_doi_ma_hang_cap_nhat_lai_toan_bo_cac_cot_dai_rong_cao_ban_kinh_luong(self):
        if self.MA_HANG_ID and self.order_id.CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH:
            self.CHIEU_DAI = 0
            self.CHIEU_RONG = 0
            self.CHIEU_CAO = 0
            self.BAN_KINH = 0
            self.LUONG = 1

    @api.onchange('CHIEU_DAI','CHIEU_RONG','CHIEU_CAO','BAN_KINH','LUONG')
    def thay_doi_chieu_dai_rong_cao_ban_kinh_de_tinh_so_luong(self):
        if self.MA_HANG_ID and self.order_id.CO_VAT_TU_SO_LUONG_THEO_CHU_VI_THE_TICH:
            sl = self.MA_HANG_ID.tinh_so_luong_theo_cong_thuc(self.CHIEU_DAI, self.CHIEU_RONG, self.CHIEU_CAO, self.BAN_KINH, self.LUONG)
            if sl is not None:
                self.set_so_luong(sl)

    @api.multi
    @api.depends('DON_GIA','DVT_ID')
    def _compute_theo_DON_GIA(self):
        for record in self:
            if record.MA_HANG_ID:
                record.DON_GIA_THEO_DVT_CHINH = record.MA_HANG_ID.compute_DON_GIA_THEO_DVT_CHINH(record.DON_GIA, record.DVT_ID.id)

    @api.onchange('TIEN_THUE_GTGT_QUY_DOI_NHAP_KHAU')
    def _onchange_TIEN_THUE_GTGT_QUY_DOI_NHAP_KHAU(self):
        if self.TIEN_THUE_GTGT_QUY_DOI_NHAP_KHAU:
            # self.TIEN_THUE_GTGT = self.TIEN_THUE_GTGT = self.TIEN_THUE_GTGT_QUY_DOI_NHAP_KHAU
            self.TIEN_THUE_GTGT_QUY_DOI = self.TIEN_THUE_GTGT_QUY_DOI_NHAP_KHAU
    
    @api.onchange('MA_NCC_ID')
    def update_ncc(self):
        self.TEN_NCC = self.MA_NCC_ID.HO_VA_TEN
        self.DIA_CHI_NCC = self.MA_NCC_ID.DIA_CHI
        self.MA_SO_THUE_NCC = self.MA_NCC_ID.MA_SO_THUE

    LOAI_CHUNG_TU_MH = fields.Selection([
        ('trong_nuoc_nhap_kho', '1. Mua hàng trong nước nhập kho'),
        ('trong_nuoc_khong_qua_kho', '2. Mua hàng trong nước không qua kho'),
        ('nhap_khau_nhap_kho', '3. Mua hàng nhập khẩu nhập kho'),
        ('nhap_khau_khong_qua_kho', '4. Mua hàng nhập khẩu không qua kho'),
        ], string='Loại chứng từ', help='Loại chứng từ mua hàng' ,related='order_id.LOAI_CHUNG_TU_MH',store=True)

    LOAI_HOA_DON = fields.Selection([
        ('1', 'Nhận kèm hóa đơn'),
        ('0', 'Không kèm hóa đơn'),
        ('2', 'Không có hóa đơn'),
        ], string='Hóa đơn', default='1',related='order_id.LOAI_HOA_DON')

    type = fields.Selection([
        ('hang_hoa', 'Chứng từ mua hàng hóa'),
        ('dich_vu', 'Chứng từ mua dịch vụ')
        ], string='Status', related='order_id.type')

    @api.onchange('LOAI_CHUNG_TU_MH','THANH_TIEN','TIEN_THUE_GTGT','TIEN_CHIET_KHAU','TY_GIA','THUE_GTGT_ID')
    def on_change_tinh_tien_quy_doi(self):
        for record in self:
            record.tinh_tien_quy_doi()

    @api.onchange('DON_GIA','TY_GIA')
    def update_DON_GIA_QUY_DOI(self):
        for record in self:
            record.tinh_don_gia_quy_doi()

    def tinh_don_gia_quy_doi(self):
        self.DON_GIA_QUY_DOI = float_round(self.DON_GIA * self.TY_GIA, 0)

    def tinh_tien_quy_doi(self):        
        self.THANH_TIEN_QUY_DOI = float_round(self.THANH_TIEN * self.TY_GIA, 0)
        # self.GIA_TINH_THUE_NK = self.THANH_TIEN * self.TY_GIA
        self.TIEN_CHIET_KHAU_QUY_DOI = float_round(self.TIEN_CHIET_KHAU * self.TY_GIA, 0)

        if self.type == 'hang_hoa':
            if self.LOAI_CHUNG_TU_MH in ('trong_nuoc_nhap_kho','trong_nuoc_khong_qua_kho'):
                self.TIEN_THUE_GTGT_QUY_DOI = float_round(self.TIEN_THUE_GTGT * self.TY_GIA, 0)
                self.TIEN_THUE_GTGT_QUY_DOI_NHAP_KHAU = float_round(self.TIEN_THUE_GTGT * self.TY_GIA, 0)
            else:
                self.TIEN_THUE_GTGT_QUY_DOI = float_round(self.TIEN_THUE_GTGT, 0)
                self.TIEN_THUE_GTGT_QUY_DOI_NHAP_KHAU = float_round(self.TIEN_THUE_GTGT, 0)
                self.TIEN_THUE_TTDB_QUY_DOI = float_round(self.TIEN_THUE_TTDB * self.TY_GIA, 0)
                self.TIEN_THUE_BVMT_QUY_DOI = float_round(self.TIEN_THUE_BVMT * self.TY_GIA, 0)
        else:
            self.TIEN_THUE_GTGT_QUY_DOI = float_round(self.TIEN_THUE_GTGT * self.TY_GIA, 0)
            self.TIEN_THUE_GTGT_QUY_DOI_NHAP_KHAU = float_round(self.TIEN_THUE_GTGT * self.TY_GIA, 0)

    @api.onchange('GIA_TINH_THUE_NK','THUE_NK')
    def on_change_tien_thue_nk(self):
        for record in self:
            record.tinh_tien_thue_nk()
    
    @api.onchange('GIA_TINH_THUE_NK','THUE_TTDB','TIEN_THUE_NK','TIEN_THUE_TTDB')
    def on_change_tien_thue_ttdb(self):
        for record in self:
            record.tinh_tien_thue_ttdb()
            record.ham_tinh_thue_gtgt()

    def tinh_tien_thue_nk(self):        
        self.TIEN_THUE_NK = (self.GIA_TINH_THUE_NK )* (self.THUE_NK /100)

    def tinh_tien_thue_ttdb(self):        
        self.TIEN_THUE_TTDB = (self.GIA_TINH_THUE_NK + self.TIEN_THUE_NK)* (self.THUE_TTDB /100)

    @api.depends('DOI_TUONG_ID')
    def _compute_doi_tuong(self):
        for record in self:
            record.TEN_DOI_TUONG = record.DOI_TUONG_ID.HO_VA_TEN

    @api.onchange('SO_LUONG', 'SO_LUONG_YEU_CAU', 'DON_GIA', 'TY_LE_CK', 'CHI_PHI_MUA_HANG', 'PHI_TRUOC_HAI_QUAN','currency_id')
    def _compute_amount(self):
        self.THANH_TIEN = self.get_so_luong()*self.DON_GIA
        self.THANH_TIEN_QUY_DOI = float_round(self.THANH_TIEN*self.TY_GIA, 0)
        self.TIEN_CHIET_KHAU = (self.DON_GIA*self.get_so_luong()*self.TY_LE_CK)/100
        self.lay_gia_tri_nhap_kho()
        self.lay_gia_tri_tinh_thue_nk()
        # tungdd - 2019-07-08 - vì thành tiền dùng onuichange nên phải tự gọi ở đây để cập nhật
        # record._onchange_THANH_TIEN()

    @api.onchange('THANH_TIEN_QUY_DOI')
    def _update_gia_tri_nhap_kho(self):
        for record in self:
            record.lay_gia_tri_nhap_kho()
           
    @api.model
    def create(self, values):
        line = super(PurchaseDocumentLine, self).create(values)
        # Cập nhật lại DON_GIA_MUA_GAN_NHAT cho MA_HANG_ID
        line.MA_HANG_ID.DON_GIA_MUA_GAN_NHAT = line.DON_GIA_THEO_DVT_CHINH
        return line
    
    @api.onchange('THUE_GTGT_ID')
    def _update_tien_thue(self):
        for record in self:
            if record.THUE_GTGT_ID:
                record.ham_tinh_thue_gtgt()
                record.TONG_TIEN_THANH_TOAN = record.THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT*(record.THANH_TIEN - record.TY_LE_CK)/100

    @api.onuichange('THANH_TIEN')
    def _onuichange_THANH_TIEN(self):
        sl = self.get_so_luong()
        if sl > 0:
            self.DON_GIA = self.THANH_TIEN/sl
            self.tinh_don_gia_quy_doi()

    @api.onchange('THANH_TIEN','LOAI_CHUNG_TU_MH')
    def _onchange_THANH_TIEN(self):
        # if self.SO_LUONG > 0:
        #     self.DON_GIA = self.THANH_TIEN/self.SO_LUONG
        self.TIEN_CHIET_KHAU = (self.DON_GIA*self.get_so_luong()*self.TY_LE_CK)/100
        self.THANH_TIEN_QUY_DOI = float_round(self.THANH_TIEN*self.TY_GIA, 0)
        self.lay_gia_tri_nhap_kho()
        self.lay_gia_tri_tinh_thue_nk()
        self.ham_tinh_thue_gtgt()

    # Hàm thay đổi giá trị Giá tính thuế NK
    def lay_gia_tri_tinh_thue_nk(self):
        if self.LOAI_CHUNG_TU_MH in ('nhap_khau_nhap_kho', 'nhap_khau_khong_qua_kho') and self.type == 'hang_hoa':
            self.GIA_TINH_THUE_NK = self.THANH_TIEN_QUY_DOI - self.TIEN_CHIET_KHAU_QUY_DOI + self.PHI_TRUOC_HAI_QUAN
    
    # Hàm tính thuế GTGT 
    def ham_tinh_thue_gtgt(self):
        if self.type == 'hang_hoa':
            if self.LOAI_CHUNG_TU_MH == 'trong_nuoc_nhap_kho' or self.LOAI_CHUNG_TU_MH == 'trong_nuoc_khong_qua_kho':
                self.TIEN_THUE_GTGT =  self.THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT * (self.THANH_TIEN - self.TIEN_CHIET_KHAU) /100
            else:
                self.TIEN_THUE_GTGT = self.THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT * (self.GIA_TINH_THUE_NK  + self.TIEN_THUE_NK + self.TIEN_THUE_TTDB) /100
        else:
            self.TIEN_THUE_GTGT =  self.THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT * (self.THANH_TIEN - self.TIEN_CHIET_KHAU) /100
    #Hàm thay đổi giá trị nhập kho
    def lay_gia_tri_nhap_kho(self):
        if self.type == 'hang_hoa':
            if self.order_id.currency_id.MA_LOAI_TIEN =='VND':
                #nếu Chứng từ mua hàng = MH trong nước nhập kho và không qua kho : Giá trị nhập kho = self.THANH_TIEN - self.TIEN_CHIET_KHAU + self.CHI_PHI_MUA_HANG
                if self.LOAI_CHUNG_TU_MH == 'trong_nuoc_nhap_kho' or self.LOAI_CHUNG_TU_MH == 'trong_nuoc_khong_qua_kho':
                    self.GIA_TRI_NHAP_KHO = self.THANH_TIEN - self.TIEN_CHIET_KHAU + self.CHI_PHI_MUA_HANG 
                #nếu Chứng từ mua hàng = MH nhập khẩu nhập kho : Giá trị nhập kho = self.THANH_TIEN - self.TIEN_CHIET_KHAU +  self.CHI_PHI_MUA_HANG + self.PHI_TRUOC_HAI_QUAN
                elif  self.LOAI_CHUNG_TU_MH == 'nhap_khau_nhap_kho':
                    self.GIA_TRI_NHAP_KHO = self.THANH_TIEN - self.TIEN_CHIET_KHAU + self.CHI_PHI_MUA_HANG + self.PHI_TRUOC_HAI_QUAN
                #nếu Chứng từ mua hàng = MH nhập khẩu không qua kho : Giá trị nhập kho = self.THANH_TIEN - self.TIEN_CHIET_KHAU +  self.PHI_TRUOC_HAI_QUAN + self.PHI_TRUOC_HAI_QUAN
                elif self.LOAI_CHUNG_TU_MH == 'nhap_khau_khong_qua_kho':
                    self.GIA_TRI_NHAP_KHO = self.THANH_TIEN - self.TIEN_CHIET_KHAU + self.PHI_TRUOC_HAI_QUAN + self.CHI_PHI_MUA_HANG
            else:
                #nếu Chứng từ mua hàng = MH trong nước nhập kho và không qua kho : Giá trị nhập kho = self.THANH_TIEN_QUY_DOI - self.TIEN_CHIET_KHAU_QUY_DOI + self.CHI_PHI_MUA_HANG
                if self.LOAI_CHUNG_TU_MH == 'trong_nuoc_nhap_kho' or self.LOAI_CHUNG_TU_MH == 'trong_nuoc_khong_qua_kho':
                    self.GIA_TRI_NHAP_KHO = self.THANH_TIEN_QUY_DOI - self.TIEN_CHIET_KHAU_QUY_DOI + self.CHI_PHI_MUA_HANG 
                #nếu Chứng từ mua hàng = MH nhập khẩu nhập kho : Giá trị nhập kho = self.THANH_TIEN_QUY_DOI - self.TIEN_CHIET_KHAU_QUY_DOI +  self.CHI_PHI_MUA_HANG + self.PHI_TRUOC_HAI_QUAN
                elif  self.LOAI_CHUNG_TU_MH == 'nhap_khau_nhap_kho':
                    self.GIA_TRI_NHAP_KHO = self.THANH_TIEN_QUY_DOI - self.TIEN_CHIET_KHAU_QUY_DOI  + self.CHI_PHI_MUA_HANG + self.PHI_TRUOC_HAI_QUAN
                #nếu Chứng từ mua hàng = MH nhập khẩu không qua kho : Giá trị nhập kho = self.THANH_TIEN_QUY_DOI - self.TIEN_CHIET_KHAU_QUY_DOI +  self.PHI_TRUOC_HAI_QUAN + self.PHI_TRUOC_HAI_QUAN
                elif self.LOAI_CHUNG_TU_MH == 'nhap_khau_khong_qua_kho':
                    self.GIA_TRI_NHAP_KHO = self.THANH_TIEN_QUY_DOI - self.TIEN_CHIET_KHAU_QUY_DOI + self.PHI_TRUOC_HAI_QUAN + self.CHI_PHI_MUA_HANG
            

    # Hàm để tính lại tiền thuế GTGT khi số tiền Giá trị nhập kho thay đổi và sản phẩm khi chọn có sẵn thuế GTGT
    # @api.onchange('GIA_TRI_NHAP_KHO')
    # def update_thue_gia_tri_gia_tang(self):
    #     if self.THUE_GTGT_ID:
    #         self.TIEN_THUE_GTGT = self.THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT * self.GIA_TRI_NHAP_KHO / 100

    @api.onchange('TIEN_CHIET_KHAU','TIEN_THUE_GTGT')
    def _update_tien_quy_doi(self):
        self.TIEN_THUE_GTGT_QUY_DOI = float_round(self.TIEN_THUE_GTGT*self.TY_GIA, 0)
        self.TIEN_CHIET_KHAU_QUY_DOI = float_round(self.TIEN_CHIET_KHAU*self.TY_GIA, 0)

        

    @api.onchange('TIEN_CHIET_KHAU','TIEN_CHIET_KHAU_QUY_DOI')
    def update_TY_LE_CK(self):
        if self.THANH_TIEN==0:
            self.TY_LE_CK = 0
        else:
            self.TY_LE_CK = (self.TIEN_CHIET_KHAU / self.THANH_TIEN)*100
    
    
    _sql_constraints = [
        ('discount_limit', 'CHECK ("TY_LE_CK" <= 100.0)',
         'Discount must be lower than 100%.'),
    ]
   
    @api.onchange('MA_HANG_ID')
    def onchange_product_id(self):
        for record in self:
            record.DON_GIA = record.MA_HANG_ID.DON_GIA_MUA_GAN_NHAT
            record.name = record.MA_HANG_ID.TEN
            record.DIEN_GIAI_THUE = 'Thuế GTGT - '+ str(record.MA_HANG_ID.TEN) if record.MA_HANG_ID.TEN else "" 
            record.KHO_ID = record.MA_HANG_ID.KHO_NGAM_DINH_ID.id
            record.TK_NO_ID = record.MA_HANG_ID.TAI_KHOAN_KHO_ID.id
            record.DVT_ID = record.MA_HANG_ID.DVT_CHINH_ID
            record.set_so_luong(1)
            # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/2023
            # tungdd - 2019-07-15 sửa lỗi không nhận kèm hóa đơn mà tổng tiền vẫn có tiền thuế
            if record.LOAI_HOA_DON == '1':
                record.TIEN_THUE_GTGT = record.THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT*(record.THANH_TIEN - record.TIEN_CHIET_KHAU)/100
                record.THUE_GTGT_ID = record.MA_HANG_ID.THUE_SUAT_GTGT_ID
        
    #Mạnh thêm hàm onchange để khi thay đổi Kho thì TK kho thay đổi
    @api.onchange('KHO_ID')
    def onchange_tk_kho(self):
        for record in self:
            record.TK_NO_ID = record.KHO_ID.TK_KHO_ID

    @api.onchange('DVT_ID')
    def onchange_dvt_id(self):
        if self.MA_HANG_ID:
            self.DON_GIA = self.MA_HANG_ID.compute_DON_GIA_MUA_GAN_NHAT(self.DVT_ID.id)

    @api.depends('SO_LUONG','SO_LUONG_YEU_CAU')
    def _compute_so_luong_theo_dvt_chinh(self):
        for record in self:
            record.SO_LUONG_THEO_DVT_CHINH = record.MA_HANG_ID.compute_SO_LUONG_THEO_DVT_CHINH(record.get_so_luong(),record.DVT_ID.id)