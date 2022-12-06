# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class STOCK_EX_KIEM_KE_VAT_TU_HANG_HOA(models.Model):
    _name = 'stock.ex.kiem.ke.vat.tu.hang.hoa'
    _description = ''
    _auto = False

    KIEM_KE_KHO_ID = fields.Many2one('danh.muc.kho', string='Kiểm kê kho', help='Kiểm kê kho')
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày',default=fields.Datetime.now)
    CHI_TIET_THEO = fields.Boolean(string='Chi tiết theo', help='Chi tiết theo')
    CHI_TIET_THEO_SELECTION = fields.Selection([('1', 'Số lô, hạn sử dụng'), ('2', ' Mã quy cách')],required=True)
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CHON_CHI_PHI_JSON = fields.Text(store=False)
    DON_VI_TINH = fields.Selection([('0', 'Đơn vị tính chính'), ('1', 'Đơn vị chuyển đổi 1'), ('2', 'Đơn vị chuyển đổi 2')], string='Đơn vị tính',default='0')
    LAY_TAT_CA_VAT_TU = fields.Boolean(string='Lấy tất cả vật tư', help='Lấy tất cả vật tư')
    NGAY_BAT_DAU_HACH_TOAN = fields.Date(string='Ngày bắt đầu hạch toán', help='Ngày bắt đầu hạch toán')
    
    @api.model
    def default_get(self, fields):
        rec = super(STOCK_EX_KIEM_KE_VAT_TU_HANG_HOA, self).default_get(fields)
        rec['KIEM_KE_KHO_ID'] = -1
        rec['NGAY_BAT_DAU_HACH_TOAN'] = self.env['ir.config_parameter'].get_param('he_thong.TU_NGAY_BAT_DAU_TAI_CHINH')
        return rec