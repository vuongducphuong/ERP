# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_BCTC_CHON_NGHIEP_VU_VA_HOAT_DONG_LCTT_FORM(models.Model):
    _name = 'tong.hop.bctc.chon.nghiep.vu.va.hoat.dong.lctt.form'
    _description = ''
    _auto = False

    CHON_NGHIEP_VU_AP_CHO_TAT_CA_CHUNG_TU = fields.Selection([('NGHIEP_VU_THANH_LY_NHUONG_BAN_TSCD_BDSDT', 'Nghiệp vụ thanh lý nhượng bán TSCĐ BĐSĐT'), ('DANH_GIA_LAI_TAI_SAN_GOP_VON_DAU_TU', ' Đánh giá lại tài sản góp vốn đầu tư'), ('BAN_THU_HOI_CAC_KHOAN_DAU_TU_TAI_CHINH', ' Bán thu hồi các khoản đầu tư tài chính'), ('LAI_CHO_VAY_LAI_TIEN_GUI_CO_TUC_VA_LOI_NHUAN_DUOC_CHIA_LAI_DAU_TU_DINH_KY', ' Lãi cho vay lãi tiền gửi cổ tức và lợi nhuận được chia lãi đầu tư định kỳ'), ('CHI_PHI_LAI_VAY_CHI_TRA_LAI_VAY', ' Chi phí lãi vay chi trả lãi vay '), ], string='Chọn nghiệp vụ áp cho tất cả chứng từ', help='Chọn nghiệp vụ áp cho tất cả chứng từ',default='NGHIEP_VU_THANH_LY_NHUONG_BAN_TSCD_BDSDT',required=True)
    CHON_HOAT_DONG_LCTT_AP_CHO_TAT_CA_CAC_CHUNG_TU = fields.Selection([('HOAT_DONG_KINH_DOANH', 'Hoạt động kinh doanh'), ('HOAT_DONG_DAU_TU', ' Hoạt động đầu tư'), ('HOAT_DONG_TAI_CHINH', ' Hoạt động tài chính'), ], string='Chọn hoạt động LCTT áp cho tất cả các chứng từ', help='Chọn hoạt động LCTT áp cho tất cả các chứng từ',default='HOAT_DONG_KINH_DOANH',required=True)
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(TONG_HOP_BCTC_CHON_NGHIEP_VU_VA_HOAT_DONG_LCTT_FORM, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result
    TONG_HOP_BCTC_CHON_NV_VA_HD_LCTT_CHI_TIET_PHAT_SINH_FORM_IDS = fields.One2many('tong.hop.bctc.chon.nv.va.hd.lctt.chi.tiet.phat.sinh.form', 'BCTC_CHON_NGHIEP_VU_VA_HOAT_DONG_LCTT_ID', string='BCTC chọn NV và HD LCTT chi tiết phát sinh form')
    TONG_HOP_BCTC_CHON_NV_VA_HD_LCTT_CHI_TIET_THEO_DT_FORM_IDS = fields.One2many('tong.hop.bctc.chon.nv.va.hd.lctt.chi.tiet.theo.dt.form', 'BCTC_CHON_NGHIEP_VU_VA_HOAT_DONG_LCTT_ID', string='BCTC chọn NV và HD LCTT chi tiết theo đt form')
    TONG_HOP_BCTC_CHON_NV_VA_HD_LCTT_CHI_TIET_KO_THEO_DT_FORM_IDS = fields.One2many('tong.hop.bctc.chon.nv.va.hd.lctt.chi.tiet.ko.theo.dt.form', 'BCTC_CHON_NGHIEP_VU_VA_HOAT_DONG_LCTT_ID', string='BCTC chọn NV và HD LCTT chi tiết ko theo đt form')
    TONG_HOP_BCTC_CHON_NV_VA_HD_LCTT_CHI_TIET_DIEU_CHINH_FORM_IDS = fields.One2many('tong.hop.bctc.chon.nv.va.hd.lctt.chi.tiet.dieu.chinh.form', 'BCTC_CHON_NGHIEP_VU_VA_HOAT_DONG_LCTT_ID', string='BCTC chọn NV và HD LCTT chi tiết điều chỉnh form')
    STEP = fields.Integer(string='bước', help='bước',store=False)
    @api.model
    def default_get(self, fields):
        rec = super(TONG_HOP_BCTC_CHON_NGHIEP_VU_VA_HOAT_DONG_LCTT_FORM, self).default_get(fields)
        rec['STEP'] =1
        return rec