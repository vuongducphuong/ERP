# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round
class ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN(models.Model):
    _name = 'account.ex.chung.tu.nghiep.vu.khac.hach.toan'
    _description = ''
    _inherit = ['mail.thread']
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK Nợ', help='Tk nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK Có', help='Tk có')
    SO_TIEN = fields.Monetary(string='Số tiền', help='Số tiền', currency_field='currency_id')
    NGHIEP_VU = fields.Selection([('KHAU_TRU_THUE_HOAT_DONG_DAU_TU', 'Khấu trừ thuế hoạt động đầu tư'), ('KHAU_TRU_THUE_HOAT_DONG_KINH_DOANH', 'Khấu trừ thuế hoạt động kinh doanh'), ], string='Nghiệp vụ', help='Nghiệp vụ')
    DOI_TUONG_NO_ID = fields.Many2one('res.partner', string='Đối tượng Nợ', help='Đối tượng nợ')
    TEN_DOI_TUONG_NO = fields.Char(string='Tên đối tượng Nợ', help='Tên đối tượng nợ',related='DOI_TUONG_NO_ID.HO_VA_TEN',store=True)
    DOI_TUONG_CO_ID = fields.Many2one('res.partner', string='Đối tượng Có', help='Đối tượng có')
    TEN_DOI_TUONG_CO = fields.Char(string='Tên đối tượng Có', help='Tên đối tượng có',related='DOI_TUONG_CO_ID.HO_VA_TEN',store=True)
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên', help='Nhân viên')
    TK_NGAN_HANG_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='TK ngân hàng', help='Tk ngân hàng')

    SO_TAI_KHOAN_NGAN_HANG_DT_NO = fields.Char(string='Số tài khoản ngân hàng đối tượng nợ', help='Số tài khoản ngân hàng đối tượng nợ')
    TEN_TAI_KHOAN_NGAN_HANG_DT_NO = fields.Char(string='Tên tài khoản ngân hàng đối tượng nợ', help='Tên tài khoản ngân hàng đối tượng nợ')

    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục CP', help='Khoản mục cp')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng thcp')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    DON_MUA_HANG_ID = fields.Many2one('purchase.ex.don.mua.hang', string='Đơn mua hàng', help='Đơn mua hàng')
    HOP_DONG_MUA_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang', string='Hợp đồng mua', help='Hợp đồng mua')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    CP_KHONG_HOP_LY = fields.Boolean(string='CP không hợp lý', help='CP không hợp lý')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    name = fields.Char(string='Name', oldname='NAME')
    SO_TIEN_QUY_DOI = fields.Monetary(string='Số tiền quy đổi', help='Số tiền quy đổi', currency_field='base_currency_id')
    CHUNG_TU_NGHIEP_VU_KHAC_ID = fields.Many2one('account.ex.chung.tu.nghiep.vu.khac', string='Chứng từ nghiệp vụ khác', help='Chứng từ nghiệp vụ khác', ondelete='cascade')
    ID_CHUNG_TU_GOC = fields.Integer(string='ID chứng từ gốc', help='ID chứng từ gốc')
    MODEL_CHUNG_TU_GOC = fields.Char(string='Model chứng từ gốc', help='Model chứng từ gốc')
    CHENH_LECH_DANH_GIA_LAI = fields.Float(string='Chênh lệch đánh giá lại', help='Chênh lệch đánh giá lại')

    DIEN_GIAI_THUE = fields.Char(string='Diễn giải thuế', help='Diễn giải thuế',default="Thuế giá trị gia tăng")
    PHAN_TRAM_THUE_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang', string='% thuế GTGT', help='Phần trăm thuế gtgt')
    TK_THUE_GTGT_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK thuế GTGT', help='Tk thuế gtgt')
    TIEN_THUE_GTGT = fields.Monetary(string='Tiền thuế GTGT', help='Tiền thuế gtgt', currency_field='currency_id')
    TIEN_THUE_GTGT_QD = fields.Monetary(string='Tiền thuế GTGT QĐ', help='Tiền thuế gtgt QĐ', currency_field='base_currency_id')

    SO_TIEN_DA_XUAT = fields.Monetary(string='Số tiền đã xuất', help='Số tiền đã xuất', currency_field='currency_id')
    QUY_DOI_THEO_CT_GOC = fields.Monetary(string='Quy đổi theo CT gốc', help='Quy đổi theo ct gốc', currency_field='base_currency_id')
    TY_GIA_XUAT_QUY_BINH_QUAN = fields.Monetary(string='Tỷ giá xuất quỹ bình quân', help='Tỷ giá xuất quỹ bình quân', currency_field='currency_id')
    QUY_DOI_THEO_TY_GIA_XUAT_QUY = fields.Monetary(string='Quy đổi theo tỷ giá xuất quỹ', help='Quy đổi theo tỷ giá xuất quỹ', currency_field='base_currency_id')
    SO_CHENH_LECH = fields.Monetary(string='Số chênh lệch', help='Số chênh lệch', currency_field='base_currency_id')
   #  currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền' ,related='CHUNG_TU_NGHIEP_VU_KHAC_ID.currency_id')

    KHONG_CO_HOA_DON = fields.Boolean(string='Không có hóa đơn', help='Không có hóa đơn')
    MAU_SO_HD_ID = fields.Many2one('danh.muc.mau.so.hd', string='Mẫu số HĐ', help='Mẫu số hđ')
    KY_HIEU_HD = fields.Char(string='Ký hiệu HĐ', help='Ký hiệu hđ')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    NHOM_HHDV_MUA_VAO_ID = fields.Many2one('danh.muc.nhom.hhdv', string='Nhóm HHDV mua vào', help='Nhóm hhdv mua vào', default=lambda self: self.lay_nhom_hhdv_mac_dinh())
    
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    
    
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='CHUNG_TU_NGHIEP_VU_KHAC_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)

    TY_GIA_XUAT_QUY = fields.Monetary(string='Tỷ giá xuất quỹ', help='Tỷ giá xuất quỹ', currency_field='currency_id')
    THANH_TIEN_THEO_TY_GIA_XUAT_QUY = fields.Monetary(string='Quy đổi theo TGXQ', help='Quy đổi theo TGXQ', currency_field='base_currency_id')
    CHENH_LECH = fields.Monetary(string='Chênh lệch', help='Chênh lệch', currency_field='base_currency_id')
    TK_XU_LY_CHENH_LECH = fields.Many2one('danh.muc.he.thong.tai.khoan',string='TK xử lý chênh lệch', help='Tài khoản xử lý chênh lệch')
    TY_GIA_DANH_GIA_LAI_GAN_NHAT = fields.Float(string='Tỷ giá đánh giá lại gần nhất', help='Tỷ giá đánh giá lại gần nhất')

    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá',related='CHUNG_TU_NGHIEP_VU_KHAC_ID.TY_GIA', store=True)
    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết',help='Thứ tự sắp xếp các dòng chi tiết')
    @api.onchange('DOI_TUONG_NO_ID')
    def thaydoildt(self):
       self.TEN_DOI_TUONG_NO = self.DOI_TUONG_NO_ID.HO_VA_TEN
       self.MA_SO_THUE=self.DOI_TUONG_NO_ID.MA_SO_THUE
       self.DIA_CHI=self.DOI_TUONG_NO_ID.DIA_CHI
    @api.onchange('DOI_TUONG_CO_ID')
    def thaydoildtco(self):
       self.TEN_DOI_TUONG_CO = self.DOI_TUONG_CO_ID.HO_VA_TEN


    @api.onchange('SO_TIEN','TY_GIA')
    def on_change_tinh_tien_quy_doi(self):
        for record in self:
            record.tinh_tien_quy_doi()

    def tinh_tien_quy_doi(self):        
        self.SO_TIEN_QUY_DOI = float_round(self.SO_TIEN * self.TY_GIA, 0)

    @api.onchange('SO_TIEN','PHAN_TRAM_THUE_GTGT_ID') #Mạnh xử lý bug1976
    def update_TIEN_THUE_GTGT(self):
        self.TIEN_THUE_GTGT = self.SO_TIEN * self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT / 100

    @api.onchange('TIEN_THUE_GTGT') #Mạnh xử lý bug1976
    def _onchange_TIEN_THUE_GTGT_QD(self):
        for record in self:
            record.TIEN_THUE_GTGT_QD = float_round(record.TIEN_THUE_GTGT * record.TY_GIA , 0)

   
    


