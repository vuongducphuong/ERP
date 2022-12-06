# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.tools.float_utils import float_round

class ACCOUNT_EX_PHIEU_THU_CHI_TIET(models.Model):
    _name = 'account.ex.phieu.thu.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    # DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK Nợ', help='Tài khoản nợ')
    TK_CO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK Có', help='Tài khoản có')
    TK_CO_PC_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK Có', help='Tk có', related='TK_CO_ID')
    TK_NGAN_HANG_ID = fields.Many2one('danh.muc.tai.khoan.ngan.hang', string='TK ngân hàng', help='Tài khoản ngân hàng')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    
    TY_GIA_XUAT_QUY = fields.Float(string='Tỷ giá xuất quỹ', help='Tỷ giá xuất quỹ')
    QUY_DOI_THEO_TGXQ = fields.Float(string='Quy đổi theo TGXQ', help='Quy đổi theo tỷ giá xuất quỹ' ,digits= decimal_precision.get_precision('Product Price'))
    CHENH_LECH = fields.Float(string='Chênh lệch', help='Chênh lệch' ,digits= decimal_precision.get_precision('Product Price'))
    TK_XU_LY_CHENH_LECH = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK xử lý chênh lệch', help='Tài khoản xử lý chênh lệch')
    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng')
    TEN_DOI_TUONG = fields.Char(string='Tên đối tượng', help='Tên đối tượng', related='DOI_TUONG_ID.HO_VA_TEN',store=True)
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', help='Đơn vị')
    CONG_TRINH_ID = fields.Many2one('danh.muc.cong.trinh', string='Công trình', help='Công trình')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán')
    PHIEU_THU_CHI_ID = fields.Many2one('account.ex.phieu.thu.chi', string='Phiếu thu chi', help='Phiếu thu chi', ondelete='cascade')
    SO_TIEN_QUY_DOI = fields.Monetary(string='Quy đổi', help='Số tiền quy đổi', store=True,currency_field='base_currency_id') 
    
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',related='PHIEU_THU_CHI_ID.currency_id', store=True)
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)
    SO_TIEN = fields.Monetary(string='Số tiền', help='Số tiền', currency_field='currency_id')
    # QUY_DOI = fields.Monetary(string='Quy đổi', help='Quy đổi', currency_field='base_currency_id')
    

    DIEN_GIAI_DETAIL = fields.Text(string='Diễn giải', help='Diễn giải')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục CP', help='Khoản mục cp')
    DON_VI_PHIEU_CHI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị phiếu chi', help='Đơn vị phiếu chi')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng THCP', help='Đối tượng thcp')
    DON_DAT_HANG_ID = fields.Many2one('account.ex.don.dat.hang', string='Đơn đặt hàng', help='Đơn đặt hàng')
    DON_MUA_HANG_ID = fields.Many2one('purchase.ex.don.mua.hang', string='Đơn mua hàng', help='Đơn mua hàng')
    HOP_DONG_MUA_ID = fields.Many2one('purchase.ex.hop.dong.mua.hang', string='Hợp đồng mua', help='Hợp đồng mua')


    TY_GIA = fields.Float(string='Tỷ giá', help='Tỷ giá',related='PHIEU_THU_CHI_ID.TY_GIA', store=True)
    THU_TU_SAP_XEP_CHI_TIET = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết',help='Thứ tự sắp xếp các dòng chi tiết')
    # @api.depends('SO_TIEN')
    # def tinh_so_tien_quy_doi(self):
    #     for record in self:
    #         record.SO_TIEN_QUY_DOI = record.SO_TIEN * record.currency_id.TY_GIA_QUY_DOI

    @api.onchange('SO_TIEN','TY_GIA')
    def on_change_tinh_tien_quy_doi(self):
        for record in self:
            record.tinh_tien_quy_doi()

    def tinh_tien_quy_doi(self):        
        self.SO_TIEN_QUY_DOI = float_round(self.SO_TIEN * self.TY_GIA, 0)
