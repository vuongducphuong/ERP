# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class STOCK_EX_TINH_GIA_VON_GHI_LOG(models.Model):
    _name = 'stock.ex.tinh.gia.von.ghi.log'
    _description = ''
    _inherit = ['mail.thread']
    
    VAT_TU_HANG_HOA_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Vật tư hàng hóa', help='Vật tư hàng hóa')
    KHO_ID = fields.Many2one('danh.muc.kho', string='Kho', help='Kho')
    HANH_DONG = fields.Integer(string='Hành động', help='ActionRowOnMaterial')
    LOI = fields.Text(string='Lỗi', help='Lỗi')
    THOI_GIAN = fields.Datetime(string='Thời gian', help='Thời gian')
    PHUONG_PHAP_TINH_GIA = fields.Char(string='Phương pháp tính giá', help='Phương pháp tính giá')