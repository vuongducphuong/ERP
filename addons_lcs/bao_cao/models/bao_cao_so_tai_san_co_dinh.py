# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_SO_TAI_SAN_CO_DINH(models.Model):
    _name = 'bao.cao.so.tai.san.co.dinh'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default='DAU_THANG_DEN_HIEN_TAI',required='True')
    TU = fields.Date(string='Từ', help='Từ',default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến',default=fields.Datetime.now)
    LOAI_TSCD_ID = fields.Many2one('danh.muc.loai.tai.san.co.dinh', string='Loại TSCĐ', help='Loại tài sản cố định')
    DON_VI_SU_DUNG_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị sử dụng', help='Đơn vị sử dụng')
    MA_TSCD = fields.Char(string='Mã TSCĐ', help='Mã tài sản cố định')#, auto_num='bao_cao_so_tai_san_co_dinh_MA_TSCD')
    TEN_TSCD = fields.Char(string='Tên TSCĐ', help='Tên tài sản cố định')
    NGAY_GHI_TANG = fields.Date(string='Ngày ghi tăng', help='Ngày ghi tăng')
    SO_CT_GHI_TANG = fields.Char(string='Số CT ghi tăng', help='Số chứng từ ghi tăng')
    NGAY_BAT_DAU_TINH_KH = fields.Date(string='Ngày bắt đầu tính KH', help='Ngày bắt đầu tính khấu hao')
    THOI_GIAN_SD = fields.Integer(string='Thời gian SD(Tháng)', help='Thời gian sử dụng (Tháng)')
    THOI_GIAN_SD_CON_LAI = fields.Integer(string='Thời gian SD còn lại(Tháng)', help='Thời gian sử dụng còn lại (Tháng)')
    NGUYEN_GIA = fields.Float(string='Nguyên giá', help='Nguyên giá')
    GIA_TRI_TINH_KH = fields.Float(string='Giá trị tính KH', help='Giá trị tính khấu hao',digits=decimal_precision.get_precision('VND'))
    HAO_MON_TRONG_KY = fields.Float(string='Hao mòn trong kỳ', help='Hao mòn trong kỳ',digits=decimal_precision.get_precision('VND'))
    HAO_MON_LUY_KE = fields.Float(string='Hao mòn lũy kế', help='Hao mòn lũy kế',digits=decimal_precision.get_precision('VND'))
    GIA_TRI_CON_LAI = fields.Float(string='Giá trị còn lại', help='Giá trị còn lại',digits=decimal_precision.get_precision('VND'))
    GIA_TRI_KH_THANG = fields.Float(string='Giá trị KH tháng', help='Giá trị khấu hao tháng',digits=decimal_precision.get_precision('VND'))
    TK_NGUYEN_GIA = fields.Char(string='TK nguyên giá', help='Tài khoản nguyên giá')
    TK_KHAU_HAO = fields.Char(string='TK khấu hao', help='Tài khoản khấu hao')
    name = fields.Char(string='Name', help='Name', oldname='NAME')


    #FIELD_IDS = fields.One2many('model.name')

    ### START IMPLEMENTING CODE ###
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_SO_TAI_SAN_CO_DINH, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        return result
    
    def _validate(self):
        params = self._context
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        if(TU=='False'):
            raise ValidationError('<Từ> không được bỏ trống.')
        elif(DEN=='False'):
            raise ValidationError('<Đến> không được bỏ trống.')
        elif(TU > DEN):
            raise ValidationError('<Đến> phải lớn hơn hoặc bằng <Từ>.')
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
        LOAI_TSCD_ID = params['LOAI_TSCD_ID'] if 'LOAI_TSCD_ID' in params.keys() else 'False'
        DON_VI_SU_DUNG_ID = params['DON_VI_SU_DUNG_ID'] if 'DON_VI_SU_DUNG_ID' in params.keys() else 'False'
        # Execute SQL query here
        cr = self.env.cr
        query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
        cr.execute(query)
        # Get and show result
        for line in cr.dictfetchall():
            record.append({
                'MA_TSCD': '',
                'TEN_TSCD': '',
                'NGAY_GHI_TANG': '',
                'NGAY_BAT_DAU_TINH_KH': '',
                'THOI_GIAN_SD': '',
                'THOI_GIAN_SD_CON_LAI': '',
                'NGUYEN_GIA': '',
                'GIA_TRI_TINH_KH': '',
                'HAO_MON_TRONG_KY': '',
                'HAO_MON_LUY_KE': '',
                'GIA_TRI_CON_LAI': '',
                'GIA_TRI_KH_THANG': '',
                'TK_NGUYEN_GIA': '',
                'TK_KHAU_HAO': '',
                'name': '',
                })
        return record

    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU')
        DEN_NGAY_F = self.get_vntime('DEN')
        param = 'Từ ngày %s đến ngày %s' % (TU_NGAY_F, DEN_NGAY_F)
        action = self.env.ref('bao_cao.open_report_so_tai_san_co_dinh').read()[0]
        action['context'] = eval(action.get('context','{}').replace('\n',''))
        action['context'].update({'breadcrumb_ex': param})
        return action
    
    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')