# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class STOCK_EX_TINH_GIA_XUAT_KHO_CHON_VAT_TU_HANG_HOA_FORM(models.Model):
    _name = 'stock.ex.tinh.gia.xuat.kho.chon.vat.tu.hang.hoa.form'
    _description = ''
    _auto = False

    TINH = fields.Char(string='Tính', help='Tính')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    MA_VAT_TU_HANG_HOA_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa')
    #FIELD_IDS = fields.One2many('model.name')
    
    STOCK_EX_TINH_GIA_XUAT_KHO_CHON_VAT_TU_HANG_HOA_CHI_TIET_FORM_IDS = fields.One2many('stock.ex.tinh.gia.xuat.kho.chon.vat.tu.hang.hoa.chi.tiet.form', 'TINH_GIA_XUAT_KHO_CHON_VAT_TU_HANG_HOA_ID', string='Tính giá xuất kho chọn vật tư hàng hóa tính giá xuất chi tiết form')


    # @api.model
    # def default_get(self,default_fields):
    #     res = super(STOCK_EX_TINH_GIA_XUAT_KHO_CHON_VAT_TU_HANG_HOA_FORM, self).default_get(default_fields)
    #     arr_chon_tinh_gia_xuat_kho= []
    #     chon_vt_hang_hoa = self.env['danh.muc.vat.tu.hang.hoa'].search([])
    #     res['STOCK_EX_TINH_GIA_XUAT_KHO_CHON_VAT_TU_HANG_HOA_CHI_TIET_FORM_IDS'] =[]
    #     for vt_hang_hoa_dt in chon_vt_hang_hoa:
    #             id_nhom_vthh = False
    #             if len(vt_hang_hoa_dt.NHOM_VTHH.ids)>0:
    #                 id_nhom_vthh = vt_hang_hoa_dt.NHOM_VTHH.ids[0]
    #             arr_chon_tinh_gia_xuat_kho +=[(0,0,{
    #                 'MA_VAT_TU_HANG_HOA_ID':vt_hang_hoa_dt.id,
    #                 'TEN_VAT_TU_HANG_HOA':vt_hang_hoa_dt.TEN,
    #                 'NHOM_VAT_TU_HANG_HOA_ID':id_nhom_vthh,
                       
    #             })]
    #     res['STOCK_EX_TINH_GIA_XUAT_KHO_CHON_VAT_TU_HANG_HOA_CHI_TIET_FORM_IDS'] +=arr_chon_tinh_gia_xuat_kho

    #     return res

    # Tạo hàm để load dữ liệu lên form bật ra sau  thay hàm default_get:
    
    @api.model
    def load_du_lieu(self,args):
        arr_chon_tinh_gia_xuat_kho= [[5]]
        chon_vt_hang_hoa = self.env['danh.muc.vat.tu.hang.hoa'].search([])
        for vt_hang_hoa_dt in chon_vt_hang_hoa:
                id_nhom_vthh = False
                if len(vt_hang_hoa_dt.NHOM_VTHH.ids)>0:
                    id_nhom_vthh = vt_hang_hoa_dt.NHOM_VTHH.ids[0]
                arr_chon_tinh_gia_xuat_kho +=[(0,0,{
                    'MA_VAT_TU_HANG_HOA_ID':vt_hang_hoa_dt.id,
                    'TEN_VAT_TU_HANG_HOA':vt_hang_hoa_dt.TEN,
                    'NHOM_VAT_TU_HANG_HOA_ID':id_nhom_vthh,
                       
                })]
        return arr_chon_tinh_gia_xuat_kho
     