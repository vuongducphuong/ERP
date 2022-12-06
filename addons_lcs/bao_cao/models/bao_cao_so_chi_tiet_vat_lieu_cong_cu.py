# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_SO_CHI_TIET_VAT_LIEU_CONG_CU(models.Model):
    _name = 'bao.cao.so.chi.tiet.vat.lieu.cong.cu'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('res.company', string='Chi nhánh', help='Chi nhánh')
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default='DAU_THANG_DEN_HIEN_TAI')
    KHO_ID = fields.Many2one('danh.muc.kho', string='Kho', help='Kho')
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày',default=fields.Datetime.now)
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày',default=fields.Datetime.now)
    DON_VI_TINH = fields.Selection([('DON_VI_TINH_CHINH', 'Đơn vị tính chính'), ('DON_VI_CHUYEN_DOI_1', 'Đơn vị chuyển đổi 1'), ('DON_VI_CHUYEN_DOI_2', 'Đơn vị chuyển đổi 2'), ], string='Đơn vị tính', help='Đơn vị tính',default='DON_VI_TINH_CHINH')
    NHOM_VTHH_ID = fields.Many2one('bao.cao.nhom.vthh', string='Nhóm vthh', help='Nhóm vthh')
    SAN_PHAM_ID = fields.One2many('danh.muc.vat.tu.hang.hoa')
    SO_HIEU = fields.Char(string='Số hiệu', help='Số hiệu')
    NGAY_THANG = fields.Datetime(string='Ngày tháng', help='Ngày tháng')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TAI_KHOAN_DOI_TUONG = fields.Char(string='Tài khoản đổi tượng', help='Tài khoản đổi tượng')
    DVT = fields.Char(string='Đvt', help='Đvt')
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá', digits=decimal_precision.get_precision('DON_GIA'))
    SO_LUONG_1 = fields.Float(string='Số lượng 1', help='Số lượng 1', digits=decimal_precision.get_precision('SO_LUONG'))
    THANH_TIEN_1 = fields.Float(string='Thành tiền 1', help='Thành tiền 1')
    SO_LUONG_2 = fields.Float(string='Số lượng 2', help='Số lượng 2', digits=decimal_precision.get_precision('SO_LUONG'))
    THANH_TIEN_2 = fields.Float(string='Thành tiền 2', help='Thành tiền 2')
    SO_LUONG_3 = fields.Float(string='Số lượng 3', help='Số lượng 3', digits=decimal_precision.get_precision('SO_LUONG'))
    THANH_TIEN_3 = fields.Float(string='Thành tiền 3', help='Thành tiền 3')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    GHI_CHU = fields.Char(string='Ghi chú', help='Ghi chú')
    MA_HANG = fields.Char(string='Mã hàng', help='Mã hàng')


    #FIELD_IDS = fields.One2many('model.name')

    ### START IMPLEMENTING CODE ###
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() else 'False'
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() else 'False'
        KY_BAO_CAO = params['KY_BAO_CAO'] if 'KY_BAO_CAO' in params.keys() else 'False'
        KHO_ID = params['KHO_ID'] if 'KHO_ID' in params.keys() else 'False'
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DON_VI_TINH = params['DON_VI_TINH'] if 'DON_VI_TINH' in params.keys() else 'False'
        NHOM_VTHH_ID = params['NHOM_VTHH_ID'] if 'NHOM_VTHH_ID' in params.keys() else 'False'
        # Execute SQL query here
        cr = self.env.cr
        query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
        cr.execute(query)
        # Get and show result
        for line in cr.dictfetchall():
            record.append({
                'CHI_NHANH_ID': '',
                'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC': '',
                'KY_BAO_CAO': '',
                'KHO_ID': '',
                'TU_NGAY': '',
                'DEN_NGAY': '',
                'DON_VI_TINH': '',
                'NHOM_VTHH_ID': '',
                'SO_HIEU': '',
                'NGAY_THANG': '',
                'DIEN_GIAI': '',
                'TAI_KHOAN_DOI_TUONG': '',
                'DVT': '',
                'DON_GIA': '',
                'SO_LUONG_1': '',
                'THANH_TIEN_1': '',
                'SO_LUONG_2': '',
                'THANH_TIEN_2': '',
                'SO_LUONG_3': '',
                'THANH_TIEN_3': '',
                'name': '',
                'MA_HANG': '',
                })
        return record

    #@api.onchange('field_name')
    #def _cap_nhat(self):
    #    for item in self:
    #        item.FIELDS_IDS = self.env['model_name'].search([])

    #@api.model
    #def default_get(self, fields_list):
    #    result = super(BAO_CAO_SO_CHI_TIET_VAT_LIEU_CONG_CU, self).default_get(fields_list)
    #    result['FIELDS_IDS'] = self.env['model_name'].search([]).ids
    #    return result
    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        action = self.env.ref('bao_cao.open_report__so_chi_tiet_vat_lieu_cong_cu').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        return action