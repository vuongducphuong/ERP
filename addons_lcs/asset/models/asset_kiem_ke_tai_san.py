# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ASSET_KIEM_KE_TAI_SAN_CO_DINH_TAI_SAN(models.Model):
    _name = 'asset.kiem.ke.tai.san'
    _description = ''
    _inherit = ['mail.thread']
    MA_TAI_SAN = fields.Many2one('asset.ghi.tang', string='Mã tài sản', help='Mã tài sản')
    TEN_TAI_SAN = fields.Char(string='Tên tài sản', help='Tên tài sản',related='MA_TAI_SAN.TEN_TAI_SAN',store=True)
    DON_VI_SU_DUNG_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị sử dụng', help='Đơn vị sử dụng')
    NGUYEN_GIA = fields.Float(string='Nguyên giá', help='Nguyên giá',digits=decimal_precision.get_precision('Product Price'))
    GIA_TRI_TINH_KHAU_HAO = fields.Float(string='Giá trị tính khấuhao', help='Giá trị tính khấuhao',digits=decimal_precision.get_precision('Product Price'))
    HAO_MON_LUY_KE = fields.Float(string='Hao mòn lũy kế', help='Hao mòn lũy kế',digits=decimal_precision.get_precision('Product Price'))
    GIA_TRI_CON_LAI = fields.Float(string='Giá trị còn lại', help='Giá trị còn lại',digits=decimal_precision.get_precision('Product Price'))
    TON_TAI = fields.Selection([('0', 'Còn'), ('1', 'Mất'), ], string='Tồn tại', help='Tồn tại',default='0',required=True)
    CHAT_LUONG_HIEN_THOI = fields.Selection([('0', 'Hoạt động tốt'), ('1', 'Bị hỏng'), ('3', 'Không xác định'), ], string='Chất lượng hiện thời', help='Chất lượng hiện thời',default='0',required=True)
    KIEN_NGHI_XU_LY = fields.Selection([('0', 'Không kiến nghị'), ('1', 'Ghi giảm'), ], string='Kiến nghị xử lý', help='Kiến nghị xử lý',default='0')
    KIEM_KE_TAI_SAN_CO_DINH_ID = fields.Many2one('asset.kiem.ke', string='Kiểm kê tài sản cố định', help='Kiểm kê tài sản cố định', ondelete='cascade')
    GHI_CHU = fields.Char(string='Ghi chú', help='Ghi chú')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    @api.onchange('TON_TAI','CHAT_LUONG_HIEN_THOI')
    def _onchange_TON_TAI(self):
        if self.TON_TAI and self.CHAT_LUONG_HIEN_THOI:
            if self.TON_TAI == '1' or self.CHAT_LUONG_HIEN_THOI == '1':
                self.KIEN_NGHI_XU_LY = '1'
            else :
                self.KIEN_NGHI_XU_LY = '0'

    
