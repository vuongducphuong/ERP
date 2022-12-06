# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError

class TONG_HOP_KHOA_SO_KY_KE_TOAN(models.Model):
    _name = 'tong.hop.khoa.so.ky.ke.toan'
    _description = ''
    _auto = False

    NGAY_KHOA_SO_HIEN_THOI = fields.Date(string='Ngày khóa sổ hiện thời', help='Ngày khóa sổ hiện thời')
    KHOA_SO_THU_KHO = fields.Boolean(string='Khóa sổ thủ kho', help='Khóa sổ thủ kho')
    CHON_NGAY_KHOA_SO_MOI = fields.Date(string='Chọn ngày khóa sổ mới', help='Chọn ngày khóa sổ mới',default=fields.Datetime.now)
    KHOA_SO_THU_QUY = fields.Boolean(string='Khóa sổ thủ quỹ', help='Khóa sổ thủ quỹ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(TONG_HOP_KHOA_SO_KY_KE_TOAN, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result
    TONG_HOP_KHOA_SO_KY_KE_TOAN_CHI_TIET_IDS = fields.One2many('tong.hop.khoa.so.ky.ke.toan.chi.tiet', 'KHOA_SO_KY_KE_TOAN_ID', string='khóa sổ kỳ kế toán chi tiết')

    @api.model
    def default_get(self, fields):
        rec = super(TONG_HOP_KHOA_SO_KY_KE_TOAN, self).default_get(fields)
        arr_tong_hop_khoa_so_ky_ke_toan_chi_tiet = []
        khoa_so_ke_toan_chi_tiet = self.env['danh.muc.to.chuc'].search([('name','=','ten don vi chi nhanh')])
        rec['TONG_HOP_KHOA_SO_KY_KE_TOAN_CHI_TIET_IDS'] =[]
        for ke_toan_dt in khoa_so_ke_toan_chi_tiet:
             arr_tong_hop_khoa_so_ky_ke_toan_chi_tiet +=[(0,0,{
                    'CHI_NHANH_ID':ke_toan_dt.id,
                    
                })]

        rec['TONG_HOP_KHOA_SO_KY_KE_TOAN_CHI_TIET_IDS'] +=arr_tong_hop_khoa_so_ky_ke_toan_chi_tiet
       
        return rec

    @api.multi
    def btn_thuc_hien(self):
        raise ValidationError('Chức năng đang được phát triển. Vui lòng thử lại sau!')