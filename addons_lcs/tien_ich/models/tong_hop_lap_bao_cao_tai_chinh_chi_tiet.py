# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_LAP_BAO_CAO_TAI_CHINH_CHI_TIET(models.Model):
    _name = 'tong.hop.lap.bao.cao.tai.chinh.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    AUTO_SELECT = fields.Boolean()
    MA_BAO_CAO_ID = fields.Many2one('tien.ich.thiet.lap.bao.cao.tai.chinh', string='Mã báo cáo', help='Mã báo cáo')
    TEN_BAO_CAO = fields.Selection([('BANG_CAN_DOI_KE_TOAN', 'Bảng cân đối kế toán'), ('BAO_CAO_KET_QUA_HOAT_DONG_KINH_DOANH', 'Báo cáo kết quả hoạt động kinh doanh'), ('BAO_CAO_LUU_CHUYEN_TIEN_TE_TRUC_TIEP', 'Báo cáo lưu chuyển tiền tệ (theo phương pháp trực tiếp)'), ('BAO_CAO_LUU_CHUYEN_TIEN_TE_GIAN_TIEP', 'Báo cáo lưu chuyển tiền tệ (theo phương pháp gián tiếp)'), ('THUYET_MINH_BAO_CAO_TAI_CHINH', 'Thuyết minh báo cáo tài chính'), ('TINH_HINH_THUC_HIEN_NGHIA_VU_DOI_VOI_NHA_NUOC', 'Tình hình thực hiện nghĩa vụ đối với nhà nước'), ], string='Tên báo cáo', help='Tên báo cáo',default='BANG_CAN_DOI_KE_TOAN',required=True)
    LAP_BAO_CAO_TAI_CHINH_ID = fields.Many2one('tong.hop.lap.bao.cao.tai.chinh', string='Lập báo cáo tài chính', help='Lập báo cáo tài chính')
    name = fields.Char(string='Name', help='Name', oldname='NAME')