# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
class ACCOUNT_EX_PHIEU_THU_CHI_THUE(models.Model):
    _name = 'account.ex.phieu.thu.chi.thue'
    _description = ''
    _inherit = ['mail.thread']
    DIEN_GIAI_THUE = fields.Char(string='Diễn giải', help='Diễn giải',default='Thuế giá trị gia tăng')
    TK_THUE_GTGT_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK thuế GTGT', help='Tk thuế GTGT')
    TIEN_THUE_GTGT = fields.Float(string='Tiền thuế GTGT', help='Tiền thuế GTGT', digits= decimal_precision.get_precision('VND') )
    PHAN_TRAM_THUE_GTGT_ID = fields.Many2one('danh.muc.thue.suat.gia.tri.gia.tang', string='% thuế GTGT', help='Phần trăm thuế GTGT')
    GIA_TRI_HHDV_CHUA_THUE = fields.Float(string='Giá trị HHDV chưa thuế', help='Giá trị hhdv chưa thuế',digits= decimal_precision.get_precision('VND'))
    NGAY_HOA_DON = fields.Date(string='Ngày hóa đơn', help='Ngày hóa đơn',default=fields.Datetime.now)
    SO_HOA_DON = fields.Char(string='Số hóa đơn', help='Số hóa đơn')
    NHOM_HHDV_MUA_VAO = fields.Many2one('danh.muc.nhom.hhdv',string='Nhóm HHDV mua vào', help='Nhóm hhdv mua vào', default=lambda self: self.lay_nhom_hhdv_mac_dinh())
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Mã NCC', help='Mã ncc')
    TEN_NCC = fields.Char(string='Tên NCC', help='Tên ncc',related='DOI_TUONG_ID.HO_VA_TEN',store=True)
    MA_SO_THUE_NCC = fields.Char(string='Mã số thuế NCC', help='Mã số thuế ncc',related='DOI_TUONG_ID.MA_SO_THUE',store=True)
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    PHIEU_THU_THUE_ID = fields.Many2one('account.ex.phieu.thu.chi', string='Phiếu thu thuế', help='Phiếu thu thuế', ondelete='cascade')
    MAU_SO_HD_ID = fields.Many2one('danh.muc.mau.so.hd', string='Mẫu số HĐ', help='Mẫu số hđ')
    KY_HIEU_HOA_DON = fields.Char(string='Ký hiệu hóa đơn', help='InvSeries')

    @api.onchange('TIEN_THUE_GTGT','PHAN_TRAM_THUE_GTGT_ID')
    def thaydoitienthue(self):
        if not self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT:
            self.GIA_TRI_HHDV_CHUA_THUE=0
        else:
            self.GIA_TRI_HHDV_CHUA_THUE=(self.TIEN_THUE_GTGT*100)/self.PHAN_TRAM_THUE_GTGT_ID.PHAN_TRAM_THUE_GTGT
