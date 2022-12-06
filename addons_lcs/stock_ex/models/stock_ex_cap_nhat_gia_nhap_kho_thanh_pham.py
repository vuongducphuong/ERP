# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class STOCK_EX_CAP_NHAT_GIA_NHAP_KHO_THANH_PHAM(models.Model):
    _name = 'stock.ex.cap.nhat.gia.nhap.kho.thanh.pham'
    _description = ''
    _auto = False

    KHOANG_THOI_GIAN = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Khoảng thời gian', help='Khoảng thời gian',required=True,default='THANG_NAY')
    NHOM_VTHH_ID = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm VTHH', help='Nhóm vthh')
    TU = fields.Date(string='Từ', help='Từ',default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến',default=fields.Datetime.now)
    MA_KHO_ID = fields.Many2one('danh.muc.kho', string='Mã kho', help='Mã kho')
    LOAI_PHIEU_NHAP = fields.Selection([('TAT_CA', '<<Tất cả>>'), ('NHAP_KHO_THANH_PHAM', ' Nhập kho thành phẩm'), ('NHAP_KHO_KHAC', ' Nhập kho khác'), ('NHAP_KHO_TU_LAP_RAP_THAO_DO', ' Nhập kho từ lắp ráp tháo dỡ'), ('NHAP_KHO_TU_KIEM_KE', ' Nhập kho từ kiểm kê'), ], string='Loại phiếu nhập', help='Loại phiếu nhập',required=True,default='TAT_CA')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(STOCK_EX_CAP_NHAT_GIA_NHAP_KHO_THANH_PHAM, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result
    STOCK_EX_CAP_NHAT_GIA_NHAP_KHO_THANH_PHAM_CHI_TIET_IDS = fields.One2many('stock.ex.cap.nhat.gia.nhap.kho.thanh.pham.chi.tiet', 'CAP_NHAT_GIA_NHAP_KHO_THANH_PHAM_ID', string='Cập nhật giá nhập kho thành phẩm chi tiết')


    @api.onchange('KHOANG_THOI_GIAN')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KHOANG_THOI_GIAN, 'TU', 'DEN')

    @api.model
    def default_get(self, fields):
        rec = super(STOCK_EX_CAP_NHAT_GIA_NHAP_KHO_THANH_PHAM, self).default_get(fields)
        arr_cap_nhat_kho_tp_chi_tiet = []
        cap_nhat_kho_chi_tiet = self.env['danh.muc.vat.tu.hang.hoa'].search([])
        rec['STOCK_EX_CAP_NHAT_GIA_NHAP_KHO_THANH_PHAM_CHI_TIET_IDS'] =[]
        for cap_nhat_kho_dt in cap_nhat_kho_chi_tiet:
             arr_cap_nhat_kho_tp_chi_tiet +=[(0,0,{
                    'MA_HANG_ID':cap_nhat_kho_dt.id,
                    'TEN_HANG':cap_nhat_kho_dt.TEN,
                    'DON_GIA':0,
                       
                })]

        rec['STOCK_EX_CAP_NHAT_GIA_NHAP_KHO_THANH_PHAM_CHI_TIET_IDS'] +=arr_cap_nhat_kho_tp_chi_tiet
        return rec