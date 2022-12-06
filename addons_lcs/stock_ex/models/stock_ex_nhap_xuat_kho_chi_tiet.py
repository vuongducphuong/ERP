# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class STOCK_EX_NHAP_XUAT_KHO_CHI_TIET(models.Model):
    _name = 'stock.ex.nhap.xuat.kho.chi.tiet'
    
    NHAP_XUAT_ID = fields.Many2one('stock.ex.nhap.xuat.kho', ondelete='cascade')
    name = fields.Char(string='Số phiếu' )
    MA_HANG_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã hàng', required=True)
    TEN_HANG = fields.Text(string='Tên hàng', help='Tên hàng')  
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK nợ', help='Tài khoản nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK có', help='Tài khoản có')
    DVT_ID = fields.Many2one('danh.muc.don.vi.tinh', string='ĐVT', help='Đơn vị tính')
    DVT = fields.Char(string='ĐVT', help='Đơn vị tính')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    # Nếu có SO_LUONG_YEU_CAU thì trường SO_LUONG là số lượng thực xuất/nhập
    SO_LUONG_YEU_CAU = fields.Float(string='SL yêu cầu', help='Số lượng yêu cầu',digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits=decimal_precision.get_precision('DON_GIA'))
    DON_GIA2 = fields.Float(string='Đơn giá', help='Đơn giá',digits=decimal_precision.get_precision('DON_GIA'),related='DON_GIA')
    DON_GIA1 = fields.Float(string='Đơn giá', help='Đơn giá',digits=decimal_precision.get_precision('DON_GIA') )
    THANH_TIEN = fields.Float(string='Thành tiền', help='Thành tiền',digits=decimal_precision.get_precision('VND'))
    LENH_SAN_XUAT_ID = fields.Many2one('stock.ex.lenh.san.xuat', string='Lệnh sản xuất', help='Lệnh sản xuất')
    SO_LO = fields.Char(string='Số lô', help='Số lô')
    HAN_SU_DUNG = fields.Date(string='Hạn sử dụng', help='Hạn sử dụng')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng tập hợp chi phí')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục CP', help='Khoản mục cp')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    THANH_PHAM = fields.Char(string='Thành phẩm', help='Thành phẩm',readonly='true')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    # DON_DAT_HANG_ID2 = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    # HOP_DONG_BAN_ID2 = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    HOP_DONG_MUA_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang', string='Hợp đồng mua', help='Hợp đồng mua')
    XUAT_TAI_KHO_ID = fields.Many2one('danh.muc.kho', string='Xuất tại kho', help='Xuất tại kho')
    NHAP_TAI_KHO_ID = fields.Many2one('danh.muc.kho', string='Nhập tại kho', help='Nhập tại kho')
    DON_GIA_BAN = fields.Float(string='Đơn giá bán', help='Đơn giá bán', digits=decimal_precision.get_precision('DON_GIA'))
    DON_GIA_VON = fields.Float(string='Đơn giá', help='Đơn giá', digits=decimal_precision.get_precision('DON_GIA'))
    TIEN_VON = fields.Float(string='Thành tiền', help='Thành tiền',digits=decimal_precision.get_precision('VND'))
    KHO_ID = fields.Many2one('danh.muc.kho', string='Kho', help='Kho')
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng')
    THANH_TIEN_2 = fields.Float(string='Thành tiền', help='Thành tiền',digits=decimal_precision.get_precision('VND'),related='THANH_TIEN' )
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng')
    THANH_TIEN_QUY_DOI = fields.Float(string='Thành tiền quy đổi', help='Thành tiền quy đổi')
    TIEN_VON_QUY_DOI = fields.Float(string='Tiền vốn quy đổi', help='Tiền vốn quy đổi', compute='_compute_tien_von', store=True)
    TOAN_TU_QUY_DOI = fields.Selection([('0', 'nhân'), ('1', 'chia')], string='ExchangeRateOperator')
    TY_LE_CHUYEN_DOI_RA_DVT_CHINH = fields.Float(string='Tỷ lệ chuyển đổi ra đơn vị tính chính', help='Tỷ lệ chuyển đổi ra đơn vị tính chính')
    # LOAI_CHUNG_TU = fields.Char(string='Loại chuyển kho', related='NHAP_XUAT_ID.type')
    LENH_LR_TD_ID = fields.Many2one('stock.ex.lap.rap.thao.do', string='Lệnh LR/TD', help='Lệnh lắp ráp tháo dỡ', ondelete='cascade')
    # NHAP_MA_QUY_CACH = fields.Char(string='Nhập mã quy cách', help='Nhập mã quy cách',readonly=1)
    # STOCK_EX_CHUNG_TU_LUU_MA_QUY_CACH_MASTER_IDS = fields.One2many('stock.ex.chung.tu.luu.ma.quy.cach.master', 'NHAP_XUAT_KHO_CHI_TIET_ID', string='Chứng từ lưu mã quy cách master')
    STOCK_EX_CHUNG_TU_LUU_MA_QUY_CACH_IDS = fields.One2many('stock.ex.chung.tu.luu.ma.quy.cach', 'NHAP_XUAT_KHO_CHI_TIET_ID', string='Chứng từ lưu mã quy cách')
    THANH_PHAM_ID = fields.Many2one('stock.ex.lenh.san.xuat.chi.tiet.thanh.pham',string='Lệnh sản xuất')

    # Mạnh sửa bug1603 & bug2101
    # Updated 2019-08-03 by anhtuan: Đổi trường này thành Char, do chỉ để hiển thị
    LENH_SAN_XUAT_VIEW_ID = fields.Char(string='Thành phẩm', help='Thành phẩm', related='THANH_PHAM_ID.name', store=True) #Thêm một trường lệnh sản xuất để hiển thị lên view 

    #VŨ
    SO_LUONG_THEO_DVT_CHINH = fields.Float(string='Số lượng theo đvt chính', help='Số lượng theo đvt chính', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_DAT_HANG_CHI_TIET_ID = fields.Many2one('account.ex.don.dat.hang.chi.tiet', string='Đơn đặt hàng chi tiết', help='SAOrderRefDetailID')
    DA_TINH_GIA_XUAT_KHO = fields.Boolean(string='Đã tính giá xuất kho', help='Đã tính giá xuất kho',default=False)
    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết',help='Thứ tự sắp xếp các dòng chi tiết')

    DON_GIA_DVT_CHINH = fields.Float(string='Đơn giá ĐVT chính', help='Đơn giá theo đơn vị tính chính')
    
    @api.onchange('THANH_PHAM_ID')
    def update_thanh_pham_id(self):
        self.LENH_SAN_XUAT_ID = self.THANH_PHAM_ID.LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID

    @api.onchange('MA_HANG_ID')
    def thaydoihang(self):
        if self.MA_HANG_ID:
            self.TEN_HANG = self.MA_HANG_ID.TEN
            self.DVT_ID = self.MA_HANG_ID.DVT_CHINH_ID
            self.SO_LUONG = 1
            self.KHO_ID = self.MA_HANG_ID.KHO_NGAM_DINH_ID.id
            # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/2238
            tk = 'TK_NO_ID' if self.NHAP_XUAT_ID.type == 'NHAP_KHO' else 'TK_CO_ID'
            if self.MA_HANG_ID.TAI_KHOAN_KHO_ID:
                setattr(self, tk, self.MA_HANG_ID.TAI_KHOAN_KHO_ID.id)
            elif self.MA_HANG_ID.KHO_NGAM_DINH_ID:
                setattr(self, tk, self.MA_HANG_ID.KHO_NGAM_DINH_ID.TK_KHO_ID.id)

    @api.onchange('NHAP_TAI_KHO_ID')
    def thaydoikhonhap(self):
        if self.NHAP_XUAT_ID.loai_chuyen_kho!= 'gui_ban' and self.NHAP_TAI_KHO_ID.TK_KHO_ID:
            self.TK_NO_ID = self.NHAP_TAI_KHO_ID.TK_KHO_ID.id

    @api.onchange('MA_HANG_ID','DVT_ID')
    def onchange_dvt_id(self):
        # Nếu là nhập kho thì DON_GIA_VON lấy theo đơn giá mua gần nhất
        # https://quanhm.visualstudio.com/lecosy-addons/_workitems/edit/3162
        if self.MA_HANG_ID:
            if self.NHAP_XUAT_ID.type == 'NHAP_KHO':
                self.DON_GIA_VON = self.MA_HANG_ID.compute_DON_GIA_MUA_GAN_NHAT(self.DVT_ID.id)
                if self.NHAP_XUAT_ID.LOAI_NHAP_KHO == 'THANH_PHAM':
                    self.DOI_TUONG_THCP_ID = self.MA_HANG_ID.lay_doi_tuong_thcp()
            else:
                self.DON_GIA_VON = self.MA_HANG_ID.compute_DON_GIA_BAN(self.DVT_ID.id)
            self.DON_GIA = self.MA_HANG_ID.compute_DON_GIA_BAN(self.DVT_ID.id)
            self.TY_LE_CHUYEN_DOI_RA_DVT_CHINH = self.MA_HANG_ID.compute_ty_le_chuyen_doi(self.DVT_ID.id)
            self.TOAN_TU_QUY_DOI = self.MA_HANG_ID.compute_toan_tu_quy_doi(self.DVT_ID.id)
        
    @api.onchange('SO_LUONG','DON_GIA','DON_GIA_VON')
    def thaydoisoluong(self):
        self.THANH_TIEN = self.SO_LUONG*self.DON_GIA
        # self.THANH_TIEN = self.SO_LUONG*self.DON_GIA_BAN
        self.TIEN_VON = self.SO_LUONG*self.DON_GIA_VON

    @api.onchange('THANH_TIEN','TIEN_VON')
    def _onchange_THANH_TIEN(self):
        if self.SO_LUONG:
            self.DON_GIA = self.THANH_TIEN/self.SO_LUONG
            self.DON_GIA_VON = self.TIEN_VON/self.SO_LUONG

    # @api.onchange('LENH_SAN_XUAT_ID')
    # def thaydoilenhsanxuat(self):
    #     self.THANH_PHAM_ID = self.LENH_SAN_XUAT_ID.STOCK_EX_LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_IDS.id

    # @api.onchange('THANH_TIEN')
    # def thaydoithanhtien(self):
    #     self.DON_GIA = self.THANH_TIEN/self.SO_LUONG

    @api.onchange('DOI_TUONG_ID')
    def thaydoidt(self):
        self.TEN_DOI_TUONG = self.DOI_TUONG_ID.HO_VA_TEN

    @api.depends('TIEN_VON')
    def _compute_tien_von(self):
        for record in self:
            record.TIEN_VON_QUY_DOI = record.TIEN_VON

