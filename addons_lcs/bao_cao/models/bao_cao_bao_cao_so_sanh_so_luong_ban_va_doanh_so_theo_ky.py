# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_BAO_CAO_SO_SANH_SO_LUONG_BAN_VA_DOANH_SO_THEO_KY(models.Model):
    _name = 'bao.cao.bao.cao.so.sanh.so.luong.ban.va.doanh.so.theo.ky'
    
    
    _auto = False

    THONG_KE_THEO = fields.Selection([('SO_SANH_CUNG_KY_BAO_CAO_GIUA_CAC_NAM', 'So sánh cùng kỳ báo cáo giữa các năm'), ('SO_SANH_GIUA_CAC_KY_BAO_CAO_KHAC_NHAU', 'So sánh giữa các kỳ báo cáo khác nhau'), ], string='Thống kê theo', help='Thống kê theo',default = 'SO_SANH_CUNG_KY_BAO_CAO_GIUA_CAC_NAM',required=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc')
    KY_BAO_CAO = fields.Selection([('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', 'Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default='DAU_THANG_DEN_HIEN_TAI',required=True)
    SO_SANH_KY = fields.Selection([('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', 'Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='So sánh kỳ', help='So sánh kỳ',default='DAU_THANG_DEN_HIEN_TAI',required=True)
    TU = fields.Date(string='Từ', help='Từ',default=fields.Datetime.now,required=True)
    DEN = fields.Date(string='Đến', help='Đến',default=fields.Datetime.now,required=True)
    TU_1 = fields.Date(string='Từ', help='Từ',default=fields.Datetime.now,required=True)
    DEN_1 = fields.Date(string='Đến', help='Đến',default=fields.Datetime.now,required=True)
    VOI_KY = fields.Selection([('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', 'Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Với kỳ', help='Với kỳ',default='DAU_THANG_DEN_HIEN_TAI',required=True)
    NHOM_VTHH_ID = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm VTHH', help='Nhóm vật tư hàng hóa')
    TU_NGAY = fields.Date(string='Từ ', help='Từ ngày',default=fields.Datetime.now,required=True)
    DEN_NGAY = fields.Date(string='Đến ', help='Đến ngày',default=fields.Datetime.now, required=True)
    NHOM_KH_ID = fields.Many2one('danh.muc.nhom.khach.hang.nha.cung.cap', string='Nhóm KH', help='Nhóm khách hàng')
    SO_SANH_VOI = fields.Integer(string='So sánh với', help='So sánh với')
    DON_VI_TINH = fields.Selection([('DON_VI_TINH_CHINH', 'Đơn vị tính chính'), ('DON_VI_CHUYEN_DOI_1', 'Đơn vị chuyển đổi 1'), ('DON_VI_CHUYEN_DOI_2', 'Đơn vị chuyển đổi 2'), ], string='Đơn vị tính', help='Đơn vị tính',default='DON_VI_TINH_CHINH',required=True)
    HIEN_THI_THEO_DANG_MO_RONG = fields.Boolean(string='Hiển thị theo dạng mở rộng', help='Hiển thị theo dạng mở rộng', default = 'True')
    MA_HANG = fields.Char(string='Mã hàng', help='Mã hàng')#, auto_num='bao_cao_bao_cao_so_sanh_so_luong_ban_va_doanh_so_theo_ky_MA_HANG')
    TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng')
    DVT = fields.Char(string='ĐVT', help='Đơn vị tính')
    NAM_MOT_SL = fields.Float(string='Năm 1', help='Năm 1',digits= decimal_precision.get_precision('VND'))
    NAM_HAI_SL = fields.Float(string='Năm 2', help='Năm 2',digits= decimal_precision.get_precision('VND'))
    NAM_MOT_DS = fields.Float(string='Năm 1', help='Năm 1',digits= decimal_precision.get_precision('VND'))
    NAM_HAI_DS = fields.Float(string='Năm 2', help='Năm 2',digits= decimal_precision.get_precision('VND'))
    NAM_MOT_DTT = fields.Float(string='Năm 1', help='Năm 1',digits= decimal_precision.get_precision('VND'))
    NAM_HAI_DTT = fields.Float(string='Năm 2', help='Năm 2',digits= decimal_precision.get_precision('VND'))

    TEN_KHACH_HANG = fields.Char(string='Tên khách hàng', help='Tên khách hàng')

    KHOANG_TG1_SL = fields.Float(string='Khoảng thời gian thứ 1', help='Khoảng thời gian thứ 1 ',digits= decimal_precision.get_precision('VND'))
    KHOANG_TG2_SL = fields.Float(string='Khoảng thời gian thứ 2', help='Khoảng thời gian thứ 2 ',digits= decimal_precision.get_precision('VND'))
    CHENH_LECH_SL = fields.Float(string='Chênh lệch', help='Chênh lệch ',digits= decimal_precision.get_precision('VND'))
    KHOANG_TG1_DS = fields.Float(string='Khoảng thời gian thứ 1', help='Khoảng thời gian thứ 2 ',digits= decimal_precision.get_precision('VND'))
    KHOANG_TG2_DS = fields.Float(string='Khoảng thời gian thứ 1', help='Khoảng thời gian thứ 2 ',digits= decimal_precision.get_precision('VND'))
    CHENH_LECH_DS = fields.Float(string='Chênh lệch', help='Chênh lệch ',digits= decimal_precision.get_precision('VND'))
    KHOANG_TG1_DTT = fields.Float(string='Khoảng thời gian thứ 1', help='Khoảng thời gian thứ 2 ',digits= decimal_precision.get_precision('VND'))
    KHOANG_TG2_DTT = fields.Float(string='Khoảng thời gian thứ 1', help='Khoảng thời gian thứ 2 ',digits= decimal_precision.get_precision('VND'))
    CHENH_LECH_DTT = fields.Float(string='Chênh lệch', help='Chênh lệch ',digits= decimal_precision.get_precision('VND'))


    SAN_PHAM_IDS_cacnam = fields.One2many('danh.muc.vat.tu.hang.hoa')
    SAN_PHAM_IDS_khacnhau = fields.One2many('danh.muc.vat.tu.hang.hoa')
    KHACH_HANG_IDS_cacnam = fields.One2many('res.partner')
    KHACH_HANG_IDS_khacnhau = fields.One2many('res.partner')

    ### START IMPLEMENTING CODE ###
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        if not params.get('active_model'):
            return
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() else 'False'
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() else 'False'
        KY_BAO_CAO = params['KY_BAO_CAO'] if 'KY_BAO_CAO' in params.keys() else 'False'
        SO_SANH_KY = params['SO_SANH_KY'] if 'SO_SANH_KY' in params.keys() else 'False'
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        TU_1 = params['TU_1'] if 'TU_1' in params.keys() else 'False'
        DEN_1 = params['DEN_1'] if 'DEN_1' in params.keys() else 'False'
        VOI_KY = params['VOI_KY'] if 'VOI_KY' in params.keys() else 'False'
        NHOM_VTHH_ID = params['NHOM_VTHH_ID'] if 'NHOM_VTHH_ID' in params.keys() else 'False'
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        NHOM_KH_ID = params['NHOM_KH_ID'] if 'NHOM_KH_ID' in params.keys() else 'False'
        SO_SANH_VOI = params['SO_SANH_VOI'] if 'SO_SANH_VOI' in params.keys() else 'False'
        DON_VI_TINH = params['DON_VI_TINH'] if 'DON_VI_TINH' in params.keys() else 'False'
        HIEN_THI_THEO_DANG_MO_RONG = params['HIEN_THI_THEO_DANG_MO_RONG'] if 'HIEN_THI_THEO_DANG_MO_RONG' in params.keys() else 'False'
        SAN_PHAM_IDS_cacnam= params['SAN_PHAM_IDS_cacnam'] if 'SAN_PHAM_IDS_cacnam' in params.keys() else 'False'
        SAN_PHAM_IDS_khacnhau= params['SAN_PHAM_IDS_khacnhau'] if 'SAN_PHAM_IDS_khacnhau' in params.keys() else 'False'
        KHACH_HANG_IDS_cacnam= params['KHACH_HANG_IDS_cacnam'] if 'KHACH_HANG_IDS_cacnam' in params.keys() else 'False'
        KHACH_HANG_IDS_khacnhau= params['KHACH_HANG_IDS_khacnhau'] if 'KHACH_HANG_IDS_khacnhau' in params.keys() else 'False'
        # Execute SQL query here
        if THONG_KE_THEO=='SO_SANH_CUNG_KY_BAO_CAO_GIUA_CAC_NAM':
            cr = self.env.cr
            query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
            cr.execute(query)
            # Get and show result
            for line in cr.dictfetchall():
                record.append({
                    'MA_HANG': '',
                    'TEN_HANG': '',
                    'DVT': '',
                    'NAM_MOT_SL': '',
                    'NAM_HAI_SL': '',
                    'NAM_MOT_DS': '',
                    'NAM_HAI_DS': '',
                    'NAM_MOT_DTT': '',
                    'NAM_HAI_DTT': '',
                    'TEN_KHACH_HANG': '',
                    })
            return record
        elif THONG_KE_THEO=='SO_SANH_GIUA_CAC_KY_BAO_CAO_KHAC_NHAU':
            cr = self.env.cr
            query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
            cr.execute(query)
            # Get and show result
            for line in cr.dictfetchall():
                record.append({
                    'MA_HANG': '',
                    'TEN_HANG': '',
                    'DVT': '',
                    'KHOANG_TG1_SL': '',
                    'KHOANG_TG2_SL': '',
                    'CHENH_LECH_SL': '',
                    'KHOANG_TG1_DS': '',
                    'KHOANG_TG2_DS': '',
                    'CHENH_LECH_DS': '',
                    'KHOANG_TG1_DTT': '',
                    'KHOANG_TG2_DTT': '',
                    'CHENH_LECH_DTT': '',
                    'TEN_KHACH_HANG': '',
                    })
            return record

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay1(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')
    
    @api.onchange('SO_SANH_KY')
    def _cap_nhat_ngay2(self):
        self.onchange_time(self.SO_SANH_KY, 'TU_1', 'DEN_1')
    
    @api.onchange('VOI_KY')
    def _cap_nhat_ngay3(self):
        self.onchange_time(self.VOI_KY, 'TU_NGAY', 'DEN_NGAY')
    
    

    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_BAO_CAO_SO_SANH_SO_LUONG_BAN_VA_DOANH_SO_THEO_KY, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        san_phams =  self.env['danh.muc.vat.tu.hang.hoa'].search([])
        khach_hangs = self.env['res.partner'].search([('LA_KHACH_HANG','=','true')])
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        if san_phams:
            result['SAN_PHAM_IDS_cacnam'] = san_phams.ids
            result['SAN_PHAM_IDS_khacnhau'] = san_phams.ids
        if khach_hangs:
            result['KHACH_HANG_IDS_cacnam'] = khach_hangs.ids
            result['KHACH_HANG_IDS_khacnhau'] = khach_hangs.ids
        return result
    ### END IMPLEMENTING CODE ###
    def _validate(self):
        params = self._context
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        SAN_PHAM_IDS_cacnam= params['SAN_PHAM_IDS_cacnam'] if 'SAN_PHAM_IDS_cacnam' in params.keys() else 'False'
        SAN_PHAM_IDS_khacnhau= params['SAN_PHAM_IDS_khacnhau'] if 'SAN_PHAM_IDS_khacnhau' in params.keys() else 'False'
        KHACH_HANG_IDS_cacnam= params['KHACH_HANG_IDS_cacnam'] if 'KHACH_HANG_IDS_cacnam' in params.keys() else 'False'
        KHACH_HANG_IDS_khacnhau= params['KHACH_HANG_IDS_khacnhau'] if 'KHACH_HANG_IDS_khacnhau' in params.keys() else 'False'
        if THONG_KE_THEO=='SO_SANH_CUNG_KY_BAO_CAO_GIUA_CAC_NAM':
            if(SAN_PHAM_IDS_cacnam=='False'):
                raise ValidationError('Bạn chưa chọn <Hàng hóa>. Xin vui lòng chọn lại.')
            elif(KHACH_HANG_IDS_cacnam=='False'):
                raise ValidationError('Bạn chưa chọn <Khách hàng>. Xin vui lòng chọn lại.')
        # validate của các trường hợp thống kê theo Công trình 
        elif THONG_KE_THEO=='SO_SANH_GIUA_CAC_KY_BAO_CAO_KHAC_NHAU':
            if(SAN_PHAM_IDS_khacnhau=='False'):
                raise ValidationError('Bạn chưa chọn <Hàng hóa>. Xin vui lòng chọn lại.')
            elif(KHACH_HANG_IDS_khacnhau=='False'):
                raise ValidationError('Bạn chưa chọn <Khách hàng>. Xin vui lòng chọn lại.')

    def _action_view_report(self):
        self._validate()
        THONG_KE_THEO = self.get_context('THONG_KE_THEO')
        if THONG_KE_THEO=='SO_SANH_CUNG_KY_BAO_CAO_GIUA_CAC_NAM':
            action = self.env.ref('bao_cao.open_report___so_sanh_so_luong_ban_va_doanh_so_theo_ky_cacnam').read()[0]
        elif THONG_KE_THEO=='SO_SANH_GIUA_CAC_KY_BAO_CAO_KHAC_NHAU':
            action = self.env.ref('bao_cao.open_report___so_sanh_so_luong_ban_va_doanh_so_theo_ky_khacnhau').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        return action