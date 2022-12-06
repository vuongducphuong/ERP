# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision
from datetime import datetime

class BAO_CAO_THE_KHO(models.Model):
    _name = 'bao.cao.the.kho'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default='DAU_THANG_DEN_HIEN_TAI',required='True')
    TU = fields.Date(string='Từ', help='Từ',default=fields.Datetime.now,required='True')
    DEN = fields.Date(string='Đến', help='Đến',default=fields.Datetime.now)
    NHOM_VTHH_ID = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm VTHH', help='Nhóm vthh')
    DON_VI_TINH = fields.Selection([('DON_VI_TINH_CHINH', 'Đơn vị tính chính'), ('DON_VI_CHUYEN_DOI_1', 'Đơn vị chuyển đổi 1'), ('DON_VI_CHUYEN_DOI_2', 'Đơn vị chuyển đổi 2'), ], string='Đơn vị tính', help='Đơn vị tính',default='DON_VI_TINH_CHINH',required='True')
    KHO_ID = fields.Many2one('danh.muc.kho', string='Kho', help='Kho')
   
    CHUNG_TU_SO_HIEU_NHAP = fields.Float(string='Nhập', help='Chứng từ số hiệu nhập')
    CHUNG_TU_SO_HIEU_XUAT = fields.Float(string='Xuất', help='Chứng từ số hiệu xuất')
    NGAY_NHAP_XUAT = fields.Date(string='Ngày nhập xuất', help='Ngày nhập xuất')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    NHAP_SO_LUONG = fields.Float(string='Nhập', help='Nhập số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    XUAT_SO_LUONG = fields.Float(string='Xuất', help='Xuất sô lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    TON_SO_LUONG = fields.Float(string='Tồn', help='Tồn số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    KY_XAC_NHAN_CUA_KE_TOAN = fields.Char(string='Ký xác nhận của kế toán', help='Ký xác nhận của kế toán')
    SO_LO = fields.Char(string='Số lô', help='Số lô')


    HANG_ID = fields.One2many('danh.muc.vat.tu.hang.hoa')

    ### START IMPLEMENTING CODE ###
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_THE_KHO, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        hang_hoas = self.env['danh.muc.vat.tu.hang.hoa'].search([],order ="TEN")
        result['KHO_ID'] = -1
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        if hang_hoas:
            result['HANG_ID'] = hang_hoas.ids
        return result

    # @api.onchange('field_name')
    # def _cap_nhat(self):
    #     for item in self:
    #         item.FIELDS_IDS = self.env['model_name'].search([])

    def _validate(self):
        params = self._context
        HANG_ID = params['HANG_ID'] if 'HANG_ID' in params.keys() else 'False'
        KHO_ID = params['KHO_ID'] if 'KHO_ID' in params.keys() else 'False'
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        TU = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

        if(TU=='False'):
            raise ValidationError('<Từ> không được bỏ trống.')
        elif(DEN=='False'):
            raise ValidationError('<Đến> không được bỏ trống.')
        elif(TU > DEN):
            raise ValidationError('<Đến> phải lớn hơn hoặc bằng <Từ>.')
        # kiểm tra danh sách hàng bị trống 
        elif KHO_ID =='False':
            raise ValidationError('Bạn chưa chọn <Kho>. Xin vui lòng chọn lại.')
        elif HANG_ID =='False':
            raise ValidationError('Bạn chưa chọn <Hàng>. Xin vui lòng chọn lại.')


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
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        DON_VI_TINH = params['DON_VI_TINH'] if 'DON_VI_TINH' in params.keys() else 'False'
        KHO_ID = params['KHO_ID'] if 'KHO_ID' in params.keys() else 'False'
        NHOM_VTHH_ID = params['NHOM_VTHH_ID'] if 'NHOM_VTHH_ID' in params.keys() else 'False'
        # Execute SQL query here
        cr = self.env.cr
        query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
        cr.execute(query)
        # Get and show result
        for line in cr.dictfetchall():
            record.append({
                'CHUNG_TU_SO_HIEU_NHAP': '',
                'CHUNG_TU_SO_HIEU_XUAT': '',
                'NGAY_NHAP_XUAT': '',
                'DIEN_GIAI': '',
                'NHAP_SO_LUONG': '',
                'XUAT_SO_LUONG': '',
                'TON_SO_LUONG': '',
                'KY_XAC_NHAN_CUA_KE_TOAN': '',
                })
        return record

    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        action = self.env.ref('bao_cao.open_report_the_kho').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        return action

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')