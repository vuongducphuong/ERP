# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class bao_cao_dieu_chinh_cong_cu_dung_cu_chi_tiet(models.Model):
    _name = 'bao.cao.dieu.chinh.cong.cu.dung.cu.chi.tiet'
    _auto = False
    
    NHAP_XUAT_ID = fields.Many2one('bao.cao.dieu.chinh.cong.cu.dung.cu')

    MA_CCDC_ID = fields.Integer(string='MA_CCDC_ID')
    SO_LUONG = fields.Float(string='SO_LUONG', help='Quantity',digits= decimal_precision.get_precision('SO_LUONG'))
    TK_CHO_PB = fields.Char(string='TK_CHO_PB', help='AllocationAccount')
    GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH = fields.Float(string='GIA_TRI_CON_LAI_TRUOC_DIEU_CHINH', help='CurrentRemainingAmount',digits= decimal_precision.get_precision('VND'))
    GIA_TRI_CON_LAI_SAU_DIEU_CHINH = fields.Float(string='GIA_TRI_CON_LAI_SAU_DIEU_CHINH', help='NewRemainingAmount',digits= decimal_precision.get_precision('VND'))
    SO_KY_PHAN_BO_CON_LAI_TRUOC_DIEU_CHINH = fields.Float(string='SO_KY_PHAN_BO_CON_LAI_TRUOC_DIEU_CHINH', help='CurrentRemainingAllocationTime',digits= decimal_precision.get_precision('VND'))
    SO_KY_CON_LAI_SAU_DIEU_CHINH = fields.Float(string='SO_KY_CON_LAI_SAU_DIEU_CHINH', help='NewRemainingAllocationTime',digits= decimal_precision.get_precision('VND'))
    SO_TIEN_PHAN_BO_HANG_KY = fields.Float(string='SO_TIEN_PHAN_BO_HANG_KY', help='TermlyAllocationAmount',digits= decimal_precision.get_precision('VND'))
    CHENH_LECH_GIA_TRI_CON_LAI = fields.Float(string='CHENH_LECH_GIA_TRI_CON_LAI', help='DiffRemainingAmount',digits= decimal_precision.get_precision('VND'))
    CHENH_LENH_KY = fields.Float(string='CHENH_LENH_KY', help='DiffAllocationTime',digits= decimal_precision.get_precision('VND'))
    SortOrderDetail = fields.Integer(string='SortOrderDetail', help='SortOrderDetail')
    MA_CCDC = fields.Char(string='MA_CCDC', help='SupplyCode')
    TEN_CCDC = fields.Char(string='TEN_CCDC', help='SupplyName')

    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh())

