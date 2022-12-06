# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round
class PURCHASE_EX_HOP_DONG_MUA_HANG(models.Model):
    _inherit = 'purchase.ex.hop.dong.mua.hang'
    _order = "NGAY_KY desc, SO_HOP_DONG desc"

    SO_HOP_DONG = fields.Char(string='Số hợp đồng', help='Số hợp đồng', auto_num='purchase_ex_hop_dong_mua_hang_SO_HOP_DONG')
    NGAY_KY = fields.Date(string='Ngày ký', help='Ngày ký',default=fields.Datetime.now)
    NHA_CUNG_CAP_ID = fields.Many2one('res.partner', string='Nhà cung cấp', help='Nhà cung cấp')
    TRICH_YEU = fields.Text(string='Trích yếu', help='Trích yếu')
    TEN_NCC = fields.Char(string='Tên ncc', help='Tên ncc', related='NHA_CUNG_CAP_ID.HO_VA_TEN')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    # currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    GIA_TRI_HOP_DONG = fields.Monetary(string='Giá trị hợp đồng', help='Giá trị hợp đồng',currency_field='currency_id')
    NGUOI_LIEN_HE = fields.Char(string='Người liên hệ', help='Người liên hệ')
    GT_HOP_DONG_QUY_DOI = fields.Monetary(string='GT hợp đồng QĐ', help='Giá trị hợp đồng quy đổi',currency_field='base_currency_id')
    HAN_GIAO_HANG = fields.Date(string='Hạn giao hàng', help='Hạn giao hàng')
    TINH_TRANG = fields.Selection([('0', 'Chưa thực hiện'), ('1', 'Đang thực hiện'), ('2', 'Đã thanh lý'), ('3', 'Đã Hủy bỏ'), ], string='Tình trạng', help='Tình trạng',default='1',required="True")
    DIA_CHI_GIAO = fields.Char(string='Địa chỉ giao', help='Địa chỉ giao')
    GIA_TRI_THANH_LY = fields.Monetary(string='Giá trị thanh lý', help='Giá trị thanh lý', related='GIA_TRI_HOP_DONG', store=True, currency_field='currency_id')
    GT_THANH_LY_QUY_DOI = fields.Monetary(string='GT thanh lý QĐ', help='Giá trị thanh lý quy đổi',store=True, currency_field='base_currency_id')
    NGAY_THANH_LY_HUY_BO = fields.Date(string='Ngày thanh lý/hủy bỏ', help='Ngày thanh lý hủy bỏ')
    NV_MUA_HANG_ID = fields.Many2one('res.partner', string='NV mua hàng', help='Nhân viên mua hàng')
    LY_DO = fields.Char(string='Lý do', help='Lý do')
    DIEU_KHOAN_KHAC = fields.Text(string='Điều khoản khác', help='Điều khoản khác')
    LA_HOP_DONG_PHAT_SINH_TRUOC_KHI_SU_DUNG_PHAN_MEM = fields.Boolean(string='Là hợp đồng phát sinh trước khi sử dụng phần mểm', help='Là hợp đồng phát sinh trước khi sử dụng phần mểm')
    GIA_TRI_DA_THUC_HIEN = fields.Float(string='Giá trị đã thực hiện', help='Giá trị đã thực hiện',digits= decimal_precision.get_precision('Product Price'))
    SO_DA_TRA = fields.Float(string='Số đã trả', help='Số đã trả',digits= decimal_precision.get_precision('Product Price'))
    HAN_THANH_TOAN = fields.Date(string='Hạn thanh toán', help='Hạn thanh toán')
    name = fields.Char(string='name', help='name',related='SO_HOP_DONG')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())

    # IS_TY_GIA = fields.Boolean(string='Loại tiền', help='Loại tiền',default=True)
    SO_CON_PHAI_TRA_DU_KIEN = fields.Float(string='Số còn phải trả dự kiến', help='Số còn phải trả dự kiến')
    SO_CON_PHAI_TRA = fields.Float(string='Số còn phải trả ', help='Số còn phải trả')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ')

    PURCHASE_EX_HOP_DONG_MUA_CHI_TIET_IDS = fields.One2many('purchase.ex.hop.dong.mua.chi.tiet', 'HOP_DONG_MUA_CHI_TIET_ID', string='Hợp đồng mua chi tiết', copy=True)


    
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, )
    DON_MUA_HANG_ID = fields.Many2one('purchase.ex.don.mua.hang', string='Hợp đồng mua', help='Đơn mua hàng')

    _sql_constraints = [
	('SO_HOP_DONG_HDMH_uniq', 'unique ("SO_HOP_DONG")', 'Số hợp đồng <<>> đã tồn tại, vui lòng nhập số hợp đồng khác!'),
	]

    @api.onchange('currency_id')
    def update_tygia(self):
        self.TY_GIA = self.currency_id.TY_GIA_QUY_DOI

    @api.onchange('TY_GIA')
    def update_thaydoiIsTy_gia(self):
        self.GT_HOP_DONG_QUY_DOI = float_round(self.GIA_TRI_HOP_DONG * self.TY_GIA,0)
        self.GT_THANH_LY_QUY_DOI = float_round(self.GIA_TRI_THANH_LY * self.TY_GIA,0)
        if self.TY_GIA == 1.0 :
            self.LA_TIEN_CO_SO = True
        else:
            self.LA_TIEN_CO_SO =False
        
    
    @api.onchange('NHA_CUNG_CAP_ID')
    def update_ncc(self):
        self.TEN_NHA_CUNG_CAP = self.NHA_CUNG_CAP_ID.HO_VA_TEN
        self.DIA_CHI = self.NHA_CUNG_CAP_ID.DIA_CHI
        self.MA_SO_THUE = self.NHA_CUNG_CAP_ID.MA_SO_THUE
    
    @api.model
    def default_get(self, fields):
        rec = super(PURCHASE_EX_HOP_DONG_MUA_HANG, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')],limit=1)
        if currency_id:
            rec['currency_id'] = currency_id.id
        rec['LOAI_CHUNG_TU'] = 9040
        return rec

    # @api.depends('PURCHASE_EX_HOP_DONG_MUA_CHI_TIET_IDS')
    # def tinhtongtien(self):
    #     for order in self:
    #         giatrihopdong = giatrihopdongquydoi = giatrithanhly = giatrithanhlyquydoi  = 0.0
    #         for line in order.PURCHASE_EX_HOP_DONG_MUA_CHI_TIET_IDS:
    #             giatrihopdong += line.TONG_TIEN_THANH_TOAN
    #             giatrihopdongquydoi += line.TONG_TIEN_THANH_TOAN_QUY_DOI
    #             giatrithanhly += line.TONG_TIEN_THANH_TOAN
    #             giatrithanhlyquydoi += line.TONG_TIEN_THANH_TOAN_QUY_DOI
    #         order.update({
    #             'GIA_TRI_HOP_DONG': giatrihopdong,
    #             'GT_HOP_DONG_QUY_DOI': giatrihopdongquydoi,
    #             'GIA_TRI_THANH_LY': giatrithanhly,
    #             'GT_THANH_LY_QUY_DOI': giatrithanhlyquydoi,
    #         })

    @api.onchange('PURCHASE_EX_HOP_DONG_MUA_CHI_TIET_IDS')
    def onchange_chi_tiet_hop_dong_mua(self):
        for order in self:
            giatrihopdong = 0.0
            for line in order.PURCHASE_EX_HOP_DONG_MUA_CHI_TIET_IDS:
                giatrihopdong += line.TONG_TIEN_THANH_TOAN
                # giatrihopdongquydoi += line.TONG_TIEN_THANH_TOAN_QUY_DOI
                # giatrithanhly += line.TONG_TIEN_THANH_TOAN
                # giatrithanhlyquydoi += line.TONG_TIEN_THANH_TOAN_QUY_DOI

            order.GIA_TRI_HOP_DONG = giatrihopdong
            # order.GT_HOP_DONG_QUY_DOI = giatrihopdongquydoi
            # order.GIA_TRI_THANH_LY = giatrithanhly
            # order.GT_THANH_LY_QUY_DOI = giatrithanhlyquydoi

    @api.onchange('GIA_TRI_HOP_DONG','GIA_TRI_THANH_LY')
    def update_gia_tri_hop_dong(self):
        self.GT_HOP_DONG_QUY_DOI = float_round(self.GIA_TRI_HOP_DONG * self.TY_GIA,0)
        self.GT_THANH_LY_QUY_DOI = float_round(self.GIA_TRI_THANH_LY * self.TY_GIA,0)




    @api.onchange('DON_MUA_HANG_ID')
    def onchange_hop_dong_mua(self):
        if self.DON_MUA_HANG_ID:
            for record in self:
                record.NHA_CUNG_CAP_ID = record.DON_MUA_HANG_ID.NHA_CUNG_CAP_ID
                record.TEN_NCC = record.DON_MUA_HANG_ID.TEN_NHA_CUNG_CAP
                record.DIA_CHI = record.DON_MUA_HANG_ID.DIA_CHI
                record.MA_SO_THUE = record.DON_MUA_HANG_ID.MA_SO_THUE
        
                record.NV_MUA_HANG_ID = record.DON_MUA_HANG_ID.NV_MUA_HANG_ID
                record.currency_id = record.DON_MUA_HANG_ID.currency_id

    @api.onchange('DON_MUA_HANG_ID')
    def update_hop_dong_mua_chi_tiet(self):
        if self.DON_MUA_HANG_ID:
            self.PURCHASE_EX_HOP_DONG_MUA_CHI_TIET_IDS = []
            for don_mua_hang_chi_tiet in self.DON_MUA_HANG_ID.PURCHASE_EX_DON_MUA_HANG_CHI_TIET_IDS:
                new_line = self.env['purchase.ex.hop.dong.mua.chi.tiet'].new({
                    'MA_HANG_ID' : don_mua_hang_chi_tiet.MA_HANG_ID,
                    'TEN_HANG' : don_mua_hang_chi_tiet.TEN_HANG,
                    'DVT_ID' : don_mua_hang_chi_tiet.DVT_ID,
                    'SO_LUONG' : don_mua_hang_chi_tiet.SO_LUONG,
                    'DON_GIA' : don_mua_hang_chi_tiet.DON_GIA,
                    
                    'THANH_TIEN' : don_mua_hang_chi_tiet.THANH_TIEN,
                    'THANH_TIEN_QUY_DOI' : don_mua_hang_chi_tiet.THANH_TIEN_QUY_DOI,
                    'PHAN_TRAM_THUE_GTGT_ID' : don_mua_hang_chi_tiet.PHAN_TRAM_THUE_GTGT_ID,
                    'TIEN_THUE_GTGT' : don_mua_hang_chi_tiet.TIEN_THUE_GTGT,
                    'TIEN_THUE_GTGT_QUY_DOI' : don_mua_hang_chi_tiet.TIEN_THUE_GTGT_QUY_DOI,
                
                    'TY_LE_CK' : don_mua_hang_chi_tiet.TY_LE_CHIET_KHAU,
                    'TIEN_CHIET_KHAU' : don_mua_hang_chi_tiet.TIEN_CHIET_KHAU,
                    'TIEN_CHIET_KHAU_QUY_DOI' : don_mua_hang_chi_tiet.TIEN_CHIET_KHAU_QUY_DOI,
                    # 'TONG_TIEN_THANH_TOAN' : don_mua_hang_chi_tiet.TIEN_THUE_GTGT,
                    # 'TONG_TIEN_THANH_TOAN_QUY_DOI' : don_mua_hang_chi_tiet.TIEN_THUE_GTGT_QUY_DOI,
                })
                self.PURCHASE_EX_HOP_DONG_MUA_CHI_TIET_IDS += new_line
   