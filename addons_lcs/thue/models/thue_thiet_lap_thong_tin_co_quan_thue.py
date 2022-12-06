# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class THUE_THIET_LAP_THONG_TIN_CO_QUAN_THUE(models.Model):
    _name = 'thue.thiet.lap.thong.tin.co.quan.thue'
    _description = 'Thiết lập thông tin cơ quan thuế, đại lý thuế, đơn vị cung cấp DV kế toán'
    _inherit = ['mail.thread']
    CO_QUAN_THUE_CAP_CUC = fields.Char(string='Cơ quan thuế cấp cục', help='Cơ quan thuế cấp cục')
    CO_QUAN_THUE_QUAN_LY = fields.Char(string='Cơ quan thuế quản lý', help='Cơ quan thuế quản lý')
    TEN_DAI_LY_THUE = fields.Char(string='Tên đại lý thuế', help='Tên đại lý thuế')
    MA_SO_THUE = fields.Char(string='Mã số thuế', help='Mã số thuế')
    DIA_CHI = fields.Text(string='Địa chỉ', help='Địa chỉ')
    QUAN_HUYEN = fields.Char(string='Quận huyện', help='Quận huyện')
    TINH_THANH_PHO = fields.Char(string='Tỉnh thành phố', help='Tỉnh thành phố')
    DIEN_THOAI = fields.Char(string='Điện thoại', help='Điện thoại')
    FAX = fields.Char(string='Fax', help='Fax')
    EMAIL = fields.Char(string='Email', help='Email')
    HOP_DONG_SO = fields.Char(string='Hợp đồng số', help='Hợp đồng số')
    NGAY_HOP_DONG = fields.Date(string='Ngày hợp đồng', help='Ngày hợp đồng')
    NV_DAI_LY_THUE = fields.Char(string='NV đại lý thuế', help='Nhân viên đại lý thuế')
    CHUNG_CHI_HANH_NGHE_SO = fields.Char(string='Chứng chỉ hành nghề số', help='Chứng chỉ hành nghề số')
    HIEN_THI_THONG_TIN_DAI_LY_THUE_TREN_TO_KHAI = fields.Boolean(string='Hiển thị thông tin đại lý thuế trên tờ khai', help='Hiển thị thông tin đại lý thuế trên tờ khai')
    SO_CHUNG_CHI_HANH_NGHE = fields.Char(string='Số chứng chỉ hành nghề', help='Số chứng chỉ hành nghề')
    DON_VI_CUNG_CAP_DICH_VU_KE_TOAN = fields.Char(string='Đơn vị cung cấp dịch vụ kế toán', help='Đơn vị cung cấp dịch vụ kế toán')

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    
    name = fields.Char(string='Name', help='Name',related='TEN_DAI_LY_THUE')

    @api.model
    def default_get(self, fields_list):
        # Kiểm tra trong db có dữ liệu chưa
        result = super(THUE_THIET_LAP_THONG_TIN_CO_QUAN_THUE, self).default_get(fields_list)
        data= self.env['thue.thiet.lap.thong.tin.co.quan.thue'].search([],limit=1)
        # load dữ liệu lên view
        if data:
            result['CO_QUAN_THUE_CAP_CUC'] = data.CO_QUAN_THUE_CAP_CUC
            result['CO_QUAN_THUE_QUAN_LY'] = data.CO_QUAN_THUE_QUAN_LY
            result['TEN_DAI_LY_THUE'] = data.TEN_DAI_LY_THUE
            result['MA_SO_THUE'] = data.MA_SO_THUE
            result['DIA_CHI'] = data.DIA_CHI
            result['QUAN_HUYEN'] = data.QUAN_HUYEN
            result['TINH_THANH_PHO'] = data.TINH_THANH_PHO
            result['DIEN_THOAI'] = data.DIEN_THOAI
            result['FAX'] = data.FAX
            result['EMAIL'] = data.EMAIL
            result['HOP_DONG_SO'] = data.HOP_DONG_SO
            result['NGAY_HOP_DONG'] = data.NGAY_HOP_DONG
            result['NV_DAI_LY_THUE'] = data.NV_DAI_LY_THUE
            result['CHUNG_CHI_HANH_NGHE_SO'] = data.CHUNG_CHI_HANH_NGHE_SO
            result['HIEN_THI_THONG_TIN_DAI_LY_THUE_TREN_TO_KHAI'] = data.HIEN_THI_THONG_TIN_DAI_LY_THUE_TREN_TO_KHAI
            result['SO_CHUNG_CHI_HANH_NGHE'] = data.SO_CHUNG_CHI_HANH_NGHE
            result['DON_VI_CUNG_CAP_DICH_VU_KE_TOAN'] = data.DON_VI_CUNG_CAP_DICH_VU_KE_TOAN
        return result

    @api.model
    def create(self, values):
        data= self.env['thue.thiet.lap.thong.tin.co.quan.thue'].search([],limit=1)
        if data:
            data.write(values)
            return data
        else:
            return super(THUE_THIET_LAP_THONG_TIN_CO_QUAN_THUE, self).create(values)