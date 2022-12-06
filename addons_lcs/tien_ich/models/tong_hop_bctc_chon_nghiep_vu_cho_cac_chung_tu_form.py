# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_BCTC_CHON_NGHIEP_VU_CHO_CAC_CHUNG_TU_FORM(models.Model):
    _name = 'tong.hop.bctc.chon.nghiep.vu.cho.cac.chung.tu.form'
    _description = ''
    _auto = False

    CHON_NGHIEP_VU_CHO_CAC_CHUNG_TU = fields.Selection([('NGHIEP_VU_THANH_LY_NHUONG_BAN_TSCD_BDSDT', 'Nghiệp vụ thanh lý nhượng bán TSCĐ BĐSĐT'), ('DANH_GIA_LAI_TAI_SAN_GOP_VON_DAU_TU', ' Đánh giá lại tài sản góp vốn đầu tư'), ('BAN_THU_HOI_CAC_KHOAN_DAU_TU_TAI_CHINH', ' Bán thu hồi các khoản đầu tư tài chính'), ('LAI_CHO_VAY_LAI_TIEN_GUI_CO_TUC_VA_LOI_NHUAN_DUOC_CHIA_LAI_DAU_TU_DINH_KY', ' Lãi cho vay lãi tiền gửi cổ tức và lợi nhuận được chia lãi đầu tư định kỳ'), ('CHI_PHI_LAI_VAY_CHI_TRA_LAI_VAY', ' Chi phí lãi vay chi trả lãi vay '), ], string='Chọn nghiệp vụ cho các chứng từ', help='Chọn nghiệp vụ cho các chứng từ',default='NGHIEP_VU_THANH_LY_NHUONG_BAN_TSCD_BDSDT',required=True)
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(TONG_HOP_BCTC_CHON_NGHIEP_VU_CHO_CAC_CHUNG_TU_FORM, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result
    TONG_HOP_BCTC_CHON_NGHIEP_VU_CHO_CAC_CHUNG_TU_CHI_TIET_FORM_IDS = fields.One2many('tong.hop.bctc.nghiep.vu.cho.ct.chi.tiet.form', 'BCTC_CHON_NGHIEP_VU_CHO_CAC_CHUNG_TU_ID', string='BCTC Chọn nghiệp vụ cho các chứng từ chi tiết form')