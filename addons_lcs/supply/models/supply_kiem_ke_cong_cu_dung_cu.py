# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision

class SUPPLY_KIEM_KE_CCDC_CCDC(models.Model):
    _name = 'supply.kiem.ke.cong.cu.dung.cu'
    _description = ''
    _inherit = ['mail.thread']
    # MA_CCDC = fields.Char(string='Mã ccdc', help='Mã ccdc', auto_num='supply_kiem_ke_ccdc_MA_CCDC')
    TEN_CCDC = fields.Char(string='Tên ccdc', help='Tên ccdc',related='MA_CCDC_ID.TEN_CCDC')
    DON_VI_SU_DUNG_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị sử dụng', help='Đơn vị sử dụng')
    DVT = fields.Char(string='Dvt', help='Dvt',compute='set_dvt',store=True)
    TREN_SO_KE_TOAN = fields.Float(string='Trên sổ kế toán', help='Trên sổ kế toán')
    KIEM_KE = fields.Float(string='Kiểm kê', help='Kiểm kê')
    CHENH_LECH = fields.Float(string='Chênh lệch', help='Chênh lệch')
    SO_LUONG_TOT = fields.Float(string='Số lượng tốt', help='Số lượng tốt', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_HONG = fields.Float(string='Số lượng hỏng', help='Số lượng hỏng', digits=decimal_precision.get_precision('SO_LUONG'))
    KIEN_NGHI_XU_LY = fields.Selection([('0', 'Ghi tăng'), ('1', 'Ghi giảm'), ('2', 'Không xử lý'), ], string='Kiến nghị xử lý', help='Kiến nghị xử lý')
    SO_LUONG_XU_LY = fields.Float(string='Số lượng xử lý', help='Số lượng xử lý', digits=decimal_precision.get_precision('SO_LUONG'))
    KIEM_KE_CCDC_ID = fields.Many2one('supply.kiem.ke', string='Kiểm kê công cụ dụng cụ', help='Kiểm kê công cụ dụng cụ', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    GHI_CHU = fields.Char(string='Ghi chú', help='Ghi chú')

    MA_CCDC_ID = fields.Many2one('supply.ghi.tang', string='Mã CCDC', help='Mã công cụ dụng cụ')

    @api.onchange('KIEM_KE')
    def update_KIEM_KE(self):
        self.CHENH_LECH = self.KIEM_KE - self.TREN_SO_KE_TOAN
        self.SO_LUONG_TOT = self.KIEM_KE
        
        if self.CHENH_LECH > 0:
            self.KIEN_NGHI_XU_LY = '0'
            self.SO_LUONG_XU_LY = self.CHENH_LECH
        elif self.CHENH_LECH < 0:
            self.KIEN_NGHI_XU_LY = '1'
            self.SO_LUONG_XU_LY = self.CHENH_LECH*(-1)
        else:
            self.KIEN_NGHI_XU_LY = '2'

    @api.onchange('SO_LUONG_TOT')
    def update_SO_LUONG_TOT(self):
        for record in self:
            if record.SO_LUONG_TOT > record.KIEM_KE :
                raise ValidationError('Số lượng tốt phải nhỏ hơn hoặc bằng số lượng kiểm kê.')
            else:
                record.SO_LUONG_HONG = record.KIEM_KE - record.SO_LUONG_TOT
       

    @api.onchange('SO_LUONG_HONG')
    def update_SO_LUONG_HONG(self):
        for record in self:
            if record.SO_LUONG_HONG > record.KIEM_KE :
                raise ValidationError('Số lượng hỏng phải nhỏ hơn hoặc bằng số lượng kiểm kê.')
            else:
                record.SO_LUONG_TOT = record.KIEM_KE - record.SO_LUONG_HONG

    
    @api.depends('MA_CCDC_ID')
    def set_dvt(self):
        for record in self:
            record.DVT = record.MA_CCDC_ID.DON_VI_TINH