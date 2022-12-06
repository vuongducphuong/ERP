# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class ACCOUNT_EX_THUE(models.Model):
    _name = 'account.ex.thue'
    _description = ''
    _inherit = ['mail.thread']
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải',default='Thuế giá trị gia tăng')
    TK_THUE_GTGT_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK thuế GTGTGT', help='Tk thuế gtgt')
    TIEN_THUE_GT = fields.Monetary(string='Tiền thuế  GT', help='Tiền thuế  gt', currency_field='base_currency_id')
    PHAN_TRAM_THUE_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang' , string='% thuế GTGT', help='Phần trăm thuế gtgt')
    GIA_TRI_HHDV_CHUA_THUE = fields.Monetary(string='Gía trị HHDV chưa thuế', help='Gía trị hhdv chưa thuế', currency_field='base_currency_id')
    MAU_SO_HD_ID = fields.Many2one('danh.muc.mau.so.hd', string='Mẫu số HĐ', help='Mẫu số hđ')
    KY_HIEU_HD = fields.Char(string='Ký hiệu HĐ', help='Ký hiệu HĐ')
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn')
    NHOM_HHDV_MUA_VAO_ID = fields.Many2one('danh.muc.nhom.hhdv', string='Nhóm HHDV mua vào', help='Nhóm hhdv mua vào', default=lambda self: self.lay_nhom_hhdv_mac_dinh())
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Mã đối tượng', help='Mã đối tượng')
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    CHUNG_TU_KHAC_THUE_ID = fields.Many2one('account.ex.chung.tu.nghiep.vu.khac', tring='Chứng từ khác thuế', help='Chứng từ khác thuế', ondelete='cascade')


    
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)

    @api.onchange('DOI_TUONG_ID')
    def doituong(self):
       self.TEN_DOI_TUONG = self.DOI_TUONG_ID.HO_VA_TEN
       self.MA_SO_THUE = self.DOI_TUONG_ID.MA_SO_THUE
       self.DIA_CHI=self.DOI_TUONG_ID.DIA_CHI


    @api.onchange('TIEN_THUE_GT')
    def tienthuegtthaydoi(self):
        if(self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT !=0):
            self.GIA_TRI_HHDV_CHUA_THUE=(self.TIEN_THUE_GT/(self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT))*100

    
    @api.onchange('PHAN_TRAM_THUE_GTGT_ID')
    def phantramthuegtthaydoi(self):
        if(self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT !=0):
            self.GIA_TRI_HHDV_CHUA_THUE=(self.TIEN_THUE_GT/(self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT))*100 
        else:
            self.GIA_TRI_HHDV_CHUA_THUE=0
    
    # @api.model
    # def default_get(self,default_fields):
    #     res = super(ACCOUNT_EX_THUE, self).default_get(default_fields)
    #     res['DIEN_GIAI'] = 'Thuế giá trị gia tăng'
    #     return res
