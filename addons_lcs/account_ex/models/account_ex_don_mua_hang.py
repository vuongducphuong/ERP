# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.exceptions import ValidationError
class PURCHASE_EX_DON_MUA_HANG(models.Model):
    _name = 'purchase.ex.don.mua.hang'
    _description = 'Đơn mua hàng'
    _inherit = ['mail.thread']
    _order = "NGAY_GIAO_HANG desc, NGAY_DON_HANG desc, SO_DON_HANG desc"


    NHA_CUNG_CAP_ID = fields.Many2one('res.partner', string='Nhà cung cấp', help='Nhà cung cấp', track_visibility='onchange')
    TEN_NHA_CUNG_CAP = fields.Char(string='Tên NCC', help='Tên nhà cung cấp')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    NV_MUA_HANG_ID = fields.Many2one('res.partner', string='NV mua hàng', help='Nhân viên mua hàng')
    DIEU_KHOAN_TT_ID = fields.Many2one('danh.muc.dieu.khoan.thanh.toan', string='Điều khoản TT', help='Điều khoản thanh toán')
    SO_NGAY_DUOC_NO = fields.Integer(string='Số ngày được nợ', help='Số ngày được nợ')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu')
    NGAY_DON_HANG = fields.Date(string='Ngày đơn hàng', help='Ngày đơn hàng',default=fields.Datetime.now)
    SO_DON_HANG = fields.Char(string='Số đơn hàng', help='Số đơn hàng', auto_num='purchase_ex_don_mua_hang_SO_DON_HANG')
    TINH_TRANG = fields.Selection([('0', 'Chưa thực hiện'), ('1', 'Đang thực hiện'), ('2', 'Hoàn thành'), ('3', 'Đã hủy bỏ'), ], string='Tình trạng', help='Tình trạng',default='0',required="True", track_visibility='onchange')
    NGAY_GIAO_HANG = fields.Date(string='Ngày giao hàng', help='Ngày giao hàng')

    # currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá')
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    LA_TIEN_CO_SO = fields.Boolean(string='Loại tiền', help='Loại tiền')
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, )


    DIA_DIEM_GIAO_HANG = fields.Char(string='Địa điểm giao hàng', help='Địa điểm giao hàng') 
    DIEU_KHOAN_KHAC = fields.Char(string='Điều khoản khác', help='Điều khoản khác')
    TONG_TIEN_THANH_TOAN = fields.Monetary(string='Tổng tiền thanh toán', help='Tổng tiền thanh toán',compute='tinhtongtien',store=True, currency_field='currency_id', track_visibility='onchange')
    TIEN_CHIET_KHAU = fields.Monetary(string='Tiền chiết khấu', help='Tiền chiết khấu',compute='tinhtongtien',store=True, currency_field='currency_id')
    TIEN_THUE = fields.Monetary(string='Tiền thuế', help='Tiền thuế',compute='tinhtongtien',store=True, currency_field='currency_id')
    TONG_TIEN_HANG = fields.Monetary(string='Tổng tiền hàng', help='Tổng tiền hàng',compute='tinhtongtien',store=True, currency_field='currency_id')
    name = fields.Char(string='Name' ,related="SO_DON_HANG")
    
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())


    # IS_TY_GIA = fields.Boolean(string='Loại tiền', help='Loại tiền',default=True)
    PURCHASE_EX_DON_MUA_HANG_CHI_TIET_IDS = fields.One2many('purchase.ex.don.mua.hang.chi.tiet', 'DON_MUA_HANG_CHI_TIET_ID', string='Đơn mua hàng chi tiết', copy=True)

    TONG_TIEN_HANG_QUY_DOI = fields.Monetary(string='',help='Tiền hàng quy đổi',compute='tinhtongtien',store=True, currency_field='base_currency_id')
    TIEN_THUE_GTGT_QUY_DOI = fields.Monetary(string='', help='Tiền thuế gtgt',compute='tinhtongtien',store=True, currency_field='base_currency_id')
    TIEN_CHIET_KHAU_QUY_DOI = fields.Monetary(string='',help='Tiền chiết khấu',compute='tinhtongtien',store=True, currency_field='base_currency_id')
    TONG_TIEN_QUY_DOI = fields.Monetary(string='',help='Tổng tiền thanh toán quy đổi',compute='tinhtongtien',store=True, currency_field='base_currency_id')
    PHAN_TRAM_THUE = fields.Char(string='phần trăm thuế GTGT', help='phần trăm thuế GTGT',compute='tinhtongtien',strore=True)
    SO_THU_TU_NHAP_CHUNG_TU = fields.Integer(string='Số chứng tự nhập chứng từ', help='Số chứng tự nhập chứng từ')
    LOAI_CHUNG_TU = fields.Integer(string='Loại chứng từ', help='Loại chứng từ') 

    _sql_constraints = [
	('SO_DON_HANG_DMH_uniq', 'unique ("SO_DON_HANG")', 'Số đơn hàng <<>> đã tồn tại, vui lòng nhập số đơn hàng khác!'),
	]


    @api.onchange('currency_id')
    def update_tygia(self):
        self.TY_GIA = self.currency_id.TY_GIA_QUY_DOI
        if self.TY_GIA == 1.0 :
            self.LA_TIEN_CO_SO = True
        else:
            self.LA_TIEN_CO_SO = False   

    

    @api.onchange('NHA_CUNG_CAP_ID')
    def update_ncc(self):
        self.TEN_NHA_CUNG_CAP = self.NHA_CUNG_CAP_ID.HO_VA_TEN
        self.DIA_CHI = self.NHA_CUNG_CAP_ID.DIA_CHI
        self.MA_SO_THUE = self.NHA_CUNG_CAP_ID.MA_SO_THUE
        
    
    @api.model
    def default_get(self, fields):
        rec = super(PURCHASE_EX_DON_MUA_HANG, self).default_get(fields)
        rec['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')]).id
        rec['LOAI_CHUNG_TU'] = 301
        return rec

    @api.onchange('DIEU_KHOAN_TT_ID')
    def _onchange_DIEU_KHOAN_TT_ID(self):
        self.SO_NGAY_DUOC_NO = self.DIEU_KHOAN_TT_ID.SO_NGAY_DUOC_NO


    @api.depends('PURCHASE_EX_DON_MUA_HANG_CHI_TIET_IDS')
    def tinhtongtien(self):
        for order in self:
            tongtienhang = tienthuegtgt = tongtienthanhtoan =tongtienhangquydoi = tienthuegtgtquydoi  = tongtienquydoi = tongtienchietkhau = tongtienchietkhauquydoi  =0.0
            phan_tram_thue=0

            for line in order.PURCHASE_EX_DON_MUA_HANG_CHI_TIET_IDS:
                #neu thueGTGT>phantramthue
                    #phantramthue=thueGTGT
                if line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT > phan_tram_thue:
                    phan_tram_thue= line.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT

                
                tongtienhang += line.THANH_TIEN
                tienthuegtgt += line.TIEN_THUE_GTGT
                tongtienchietkhau += line.TIEN_CHIET_KHAU
                tongtienthanhtoan = tongtienhang + tienthuegtgt

                tongtienhangquydoi += line.THANH_TIEN_QUY_DOI
                tienthuegtgtquydoi += line.TIEN_THUE_GTGT_QUY_DOI
                tongtienchietkhauquydoi += line.TIEN_CHIET_KHAU_QUY_DOI
                tongtienquydoi = tongtienhangquydoi + tienthuegtgtquydoi 

            order.update({
                'TONG_TIEN_HANG': tongtienhang,
                'TIEN_THUE': tienthuegtgt,
                'TONG_TIEN_THANH_TOAN': tongtienthanhtoan,
                'TIEN_CHIET_KHAU' : tongtienchietkhau,

                'TONG_TIEN_HANG_QUY_DOI': tongtienhangquydoi,
                'TIEN_THUE_GTGT_QUY_DOI': tienthuegtgtquydoi,
                'TONG_TIEN_QUY_DOI': tongtienquydoi,
                'PHAN_TRAM_THUE': phan_tram_thue,
                'TIEN_CHIET_KHAU_QUY_DOI' : tongtienchietkhauquydoi,

            })


    # @api.multi
    # def validate(self, vals, option=None):
    #     if vals.get('NGAY_DON_HANG') == None:
	# 		raise ValidationError('Ngày đơn hàng không được bỏ trống')
    #     elif vals.get('SO_DON_HANG') == None:
    #         raise ValidationError('Số đơn hàng không được bỏ trống')
    #     elif vals.get('TINH_TRANG') == None:
    #         raise ValidationError("Tình trạng không được bỏ trống")

           