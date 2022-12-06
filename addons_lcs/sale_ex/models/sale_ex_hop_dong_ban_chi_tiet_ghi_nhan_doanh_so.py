# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SALE_EX_HOP_DONG_BAN_CHI_TIET_GHI_NHAN_DOANH_SO(models.Model):
    _name = 'sale.ex.hop.dong.ban.chi.tiet.ghi.nhan.doanh.so'
    _description = ''
    _inherit = ['mail.thread']
    LOAI = fields.Selection([('0', 'Đề nghị ghi doanh số'), ('1', 'Doanh số ghi nhận')], string='Loại', help='Loại')
    NGAY = fields.Date(string='Ngày', help='Ngày')
    NHAN_VIEN_ID = fields.Many2one('res.partner', string='Nhân viên', help='Nhân viên')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc',string='Đơn vị', help='Đơn vị')
    HANG_HOA_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Hàng hóa', help='Hàng hóa')
    TY_LE_PHAN_TRAM = fields.Float(string='Tỷ lệ phần trăm', help='Tỷ lệ phần trăm')
    DOANH_SO_GHI_NHAN_HUY_BO = fields.Float(string='Doanh số ghi nhận hủy bỏ', help='Doanh số ghi nhận hủy bỏ')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    HOP_DONG_BAN_ID = fields.Many2one('sale.ex.hop.dong.ban', string='Hợp đồng bán', help='Hợp đồng bán', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')