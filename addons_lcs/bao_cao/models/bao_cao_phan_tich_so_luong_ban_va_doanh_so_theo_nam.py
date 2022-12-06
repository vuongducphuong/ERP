# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_PHAN_TICH_SO_LUONG_BAN_VA_DOANH_SO_THEO_NAM(models.Model):
    _name = 'bao.cao.phan.tich.so.luong.ban.va.doanh.so.theo.nam'
    
    
    _auto = False

    THONG_KE_THEO = fields.Selection([('KHACH_HANG_VA_MAT_HANG_THEO_THANG', 'Khách hàng và mặt hàng theo tháng'), ('KHACH_HANG_VA_MAT_HANG_THEO_QUY', 'Khách hàng và mặt hàng theo quý'), ('MAT_HANG_THEO_THANG', 'Mặt hàng theo tháng'), ('MAT_HANG_THEO_QUY', 'Mặt hàng theo quý'), ], string='Thông kê theo', help='Thông kê theo',default='KHACH_HANG_VA_MAT_HANG_THEO_THANG',required=True)
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default='True')
    NAM = fields.Integer(string='Năm', help='Năm',required=True)
    NHOM_VTHH_ID = fields.Many2one('danh.muc.nhom.vat.tu.hang.hoa.dich.vu', string='Nhóm VTHH', help='Nhóm vật tư hàng hóa')
    NHOM_KH_ID = fields.Many2one('danh.muc.nhom.khach.hang.nha.cung.cap', string='Nhóm KH', help='Nhóm khách hàng')
    DON_VI_TINH = fields.Selection([('DON_VI_TINH_CHINH', 'Đơn vị tính chính'), ('DON_VI_CHUYEN_DOI_1', 'Đơn vị chuyển đổi 1'), ('DON_VI_CHUYEN_DOI_2', 'Đơn vị chuyển đổi 2'), ], string='Đơn vị tính', help='Đơn vị tính',default='DON_VI_TINH_CHINH',required=True)
    MA_HANG = fields.Char(string='Mã hàng', help='Mã hàng')#, auto_num='bao_cao_phan_tich_so_luong_ban_va_doanh_so_theo_nam_MA_HANG')
    TEN_HANG = fields.Char(string='Tên hàng', help='Tên hàng')
    DVT = fields.Char(string='ĐVT', help='Đơn vị tính')
    THANG_1_SL = fields.Float(string='Tháng 1', help='Tháng 1_sl',digits= decimal_precision.get_precision('VND'))
    THANG_2_SL = fields.Float(string='Tháng 2', help='Tháng 2_sl',digits= decimal_precision.get_precision('VND'))
    THANG_3_SL = fields.Float(string='Tháng 3', help='Tháng 3_sl',digits= decimal_precision.get_precision('VND'))
    THANG_4_SL = fields.Float(string='Tháng 4', help='Tháng 4_sl',digits= decimal_precision.get_precision('VND'))
    THANG_5_SL = fields.Float(string='Tháng 5', help='Tháng 5_sl',digits= decimal_precision.get_precision('VND'))
    THANG_6_SL = fields.Float(string='Tháng 6', help='Tháng 6_sl',digits= decimal_precision.get_precision('VND'))
    THANG_7_SL = fields.Float(string='Tháng 7', help='Tháng 7_sl',digits= decimal_precision.get_precision('VND'))
    THANG_8_SL = fields.Float(string='Tháng 8', help='Tháng 8_sl',digits= decimal_precision.get_precision('VND'))
    THANG_9_SL = fields.Float(string='Tháng 9', help='Tháng 9_sl',digits= decimal_precision.get_precision('VND'))
    THANG_10_SL = fields.Float(string='Tháng 10', help='Tháng 10_sl',digits= decimal_precision.get_precision('VND'))
    THANG_11_SL = fields.Float(string='Tháng 11', help='Tháng 11_sl',digits= decimal_precision.get_precision('VND'))
    THANG_12_SL = fields.Float(string='Tháng 12', help='Tháng 12_sl',digits= decimal_precision.get_precision('VND'))
    TONG_CONG_SL = fields.Float(string='Tổng cộng', help='Tổng cộng sl',digits= decimal_precision.get_precision('VND'))
    THANG_1_DS = fields.Float(string='Tháng 1', help='Tháng 1_ds',digits= decimal_precision.get_precision('VND'))
    THANG_2_DS = fields.Float(string='Tháng 2', help='Tháng 2_ds',digits= decimal_precision.get_precision('VND'))
    THANG_3_DS = fields.Float(string='Tháng 3 ', help='Tháng 3_ds ',digits= decimal_precision.get_precision('VND'))
    THANG_4_DS = fields.Float(string='Tháng 4', help='Tháng 4_ds',digits= decimal_precision.get_precision('VND'))
    THANG_5_DS = fields.Float(string='Tháng 5', help='Tháng 5_ds',digits= decimal_precision.get_precision('VND'))
    THANG_6_DS = fields.Float(string='Tháng 6', help='Tháng 6_ds',digits= decimal_precision.get_precision('VND'))
    THANG_7_DS = fields.Float(string='Tháng 7', help='Tháng 7_ds',digits= decimal_precision.get_precision('VND'))
    THANG_8_DS = fields.Float(string='Tháng 8', help='Tháng 8_ds',digits= decimal_precision.get_precision('VND'))
    THANG_9_DS = fields.Float(string='Tháng 9', help='Tháng 9_ds',digits= decimal_precision.get_precision('VND'))
    THANG_10_DS = fields.Float(string='Tháng 10', help='Tháng 10_ds',digits= decimal_precision.get_precision('VND'))
    THANG_11_DS = fields.Float(string='Tháng 11', help='Tháng 11_ds',digits= decimal_precision.get_precision('VND'))
    THANG_12_DS = fields.Float(string='Tháng 12', help='Tháng 12_ds',digits= decimal_precision.get_precision('VND'))
    TONG_CONG_DS = fields.Float(string='Tổng cộng', help='Tổng cộng ds',digits= decimal_precision.get_precision('VND'))
    THANG_1_DTT = fields.Float(string='Tháng 1', help='Tháng 1_dtt',digits= decimal_precision.get_precision('VND'))
    THANG_2_DTT = fields.Float(string='Tháng 2', help='Tháng 2_dtt',digits= decimal_precision.get_precision('VND'))
    THANG_3_DTT = fields.Float(string='Tháng 3', help='Tháng 3_dtt',digits= decimal_precision.get_precision('VND'))
    THANG_4_DTT = fields.Float(string='Tháng 4', help='Tháng 4_dtt',digits= decimal_precision.get_precision('VND'))
    THANG_5_DTT = fields.Float(string='Tháng 5', help='Tháng 5_dtt',digits= decimal_precision.get_precision('VND'))
    THANG_6_DTT = fields.Float(string='Tháng 6', help='Tháng 6_dtt',digits= decimal_precision.get_precision('VND'))
    THANG_7_DTT = fields.Float(string='Tháng 7', help='Tháng 7_dtt',digits= decimal_precision.get_precision('VND'))
    THANG_8_DTT = fields.Float(string='Tháng 8', help='Tháng 8_dtt',digits= decimal_precision.get_precision('VND'))
    THANG_9_DTT = fields.Float(string='Tháng 9', help='Tháng 9_dtt',digits= decimal_precision.get_precision('VND'))
    THANG_10_DTT = fields.Float(string='Tháng 10', help='Tháng 10_dtt',digits= decimal_precision.get_precision('VND'))
    THANG_11_DTT = fields.Float(string='Tháng 11', help='Tháng 11_dtt',digits= decimal_precision.get_precision('VND'))
    THANG_12_DTT = fields.Float(string='Tháng 12', help='Tháng 12_dtt',digits= decimal_precision.get_precision('VND'))
    TONG_CONG_DTT = fields.Float(string='Tổng cộng', help='Tổng cộng dtt',digits= decimal_precision.get_precision('VND'))
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    TEN_KHACH_HANG = fields.Char( string='Tên khách hàng', help='Tên khách hàng')

    QUI_1_SL = fields.Float(string='Quý I', help='Quý I',digits= decimal_precision.get_precision('VND'))
    QUI_2_SL = fields.Float(string='Quý II', help='Quý II',digits= decimal_precision.get_precision('VND'))
    QUI_3_SL = fields.Float(string='Quý III', help='Quý III',digits= decimal_precision.get_precision('VND'))
    QUI_4_SL = fields.Float(string='Quý IV', help='Quý IV',digits= decimal_precision.get_precision('VND'))
    QUI_1_DS = fields.Float(string='Quý I', help='Quý I',digits= decimal_precision.get_precision('VND'))
    QUI_2_DS = fields.Float(string='Quý II', help='Quý II',digits= decimal_precision.get_precision('VND'))
    QUI_3_DS = fields.Float(string='Quý III', help='Quý III',digits= decimal_precision.get_precision('VND'))
    QUI_4_DS = fields.Float(string='Quý IV', help='Quý IV',digits= decimal_precision.get_precision('VND'))
    QUI_1_DTT = fields.Float(string='Quý I', help='Quý I',digits= decimal_precision.get_precision('VND'))
    QUI_2_DTT = fields.Float(string='Quý II', help='Quý II',digits= decimal_precision.get_precision('VND'))
    QUI_3_DTT = fields.Float(string='Quý III', help='Quý III',digits= decimal_precision.get_precision('VND'))
    QUI_4_DTT = fields.Float(string='Quý IV', help='Quý IV',digits= decimal_precision.get_precision('VND'))

    SAN_PHAM_IDS_KHvaMHtheothang = fields.One2many('danh.muc.vat.tu.hang.hoa')
    SAN_PHAM_IDS_KHvaMHtheoquy = fields.One2many('danh.muc.vat.tu.hang.hoa')
    SAN_PHAM_IDS_MHtheothang = fields.One2many('danh.muc.vat.tu.hang.hoa')
    SAN_PHAM_IDS_MHtheoquy = fields.One2many('danh.muc.vat.tu.hang.hoa')
    KHACH_HANG_IDS_KHvaMHtheothang = fields.One2many('res.partner')
    KHACH_HANG_IDS_KHvaMHtheoquy = fields.One2many('res.partner')

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
        NAM = params['NAM'] if 'NAM' in params.keys() else 'False'
        NHOM_VTHH_ID = params['NHOM_VTHH_ID'] if 'NHOM_VTHH_ID' in params.keys() else 'False'
        NHOM_KH_ID = params['NHOM_KH_ID'] if 'NHOM_KH_ID' in params.keys() else 'False'
        DON_VI_TINH = params['DON_VI_TINH'] if 'DON_VI_TINH' in params.keys() else 'False'
        SAN_PHAM_IDS_KHvaMHtheothang= params['SAN_PHAM_IDS_KHvaMHtheothang'] if 'SAN_PHAM_IDS_KHvaMHtheothang' in params.keys() else 'False'
        KHACH_HANG_IDS_KHvaMHtheothang= params['KHACH_HANG_IDS_KHvaMHtheothang'] if 'KHACH_HANG_IDS_KHvaMHtheothang' in params.keys() else 'False'
        SAN_PHAM_IDS_KHvaMHtheoquy = params['SAN_PHAM_IDS_KHvaMHtheoquy'] if 'SAN_PHAM_IDS_KHvaMHtheoquy' in params.keys() else 'False'
        KHACH_HANG_IDS_KHvaMHtheoquy = params['KHACH_HANG_IDS_KHvaMHtheoquy'] if 'KHACH_HANG_IDS_KHvaMHtheoquy' in params.keys() else 'False'
        SAN_PHAM_IDS_MHtheothang = params['SAN_PHAM_IDS_MHtheothang'] if 'SAN_PHAM_IDS_MHtheothang' in params.keys() else 'False'
        SAN_PHAM_IDS_MHtheoquy = params['SAN_PHAM_IDS_MHtheoquy'] if 'SAN_PHAM_IDS_MHtheoquy' in params.keys() else 'False'
        # Execute SQL query here
        if THONG_KE_THEO=='KHACH_HANG_VA_MAT_HANG_THEO_THANG': 
            cr = self.env.cr
            query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
            cr.execute(query)
            # Get and show result
            for line in cr.dictfetchall():
                record.append({
                    'MA_HANG': '',
                    'TEN_HANG': '',
                    'DVT': '',
                    'THANG_1_SL': '',
                    'THANG_2_SL': '',
                    'THANG_3_SL': '',
                    'THANG_4_SL': '',
                    'THANG_5_SL': '',
                    'THANG_6_SL': '',
                    'THANG_7_SL': '',
                    'THANG_8_SL': '',
                    'THANG_9_SL': '',
                    'THANG_10_SL': '',
                    'THANG_11_SL': '',
                    'THANG_12_SL': '',
                    'TONG_CONG_SL': '',
                    'THANG_1_DS': '',
                    'THANG_2_DS': '',
                    'THANG_3_DS': '',
                    'THANG_4_DS': '',
                    'THANG_5_DS': '',
                    'THANG_6_DS': '',
                    'THANG_7_DS': '',
                    'THANG_8_DS': '',
                    'THANG_9_DS': '',
                    'THANG_10_DS': '',
                    'THANG_11_DS': '',
                    'THANG_12_DS': '',
                    'TONG_CONG_DS': '',
                    'THANG_1_DTT': '',
                    'THANG_2_DTT': '',
                    'THANG_3_DTT': '',
                    'THANG_4_DTT': '',
                    'THANG_5_DTT': '',
                    'THANG_6_DTT': '',
                    'THANG_7_DTT': '',
                    'THANG_8_DTT': '',
                    'THANG_9_DTT': '',
                    'THANG_10_DTT': '',
                    'THANG_11_DTT': '',
                    'THANG_12_DTT': '',
                    'TONG_CONG_DTT': '',
                    'name': '',
                    'TEN_KHACH_HANG':'',
                    })
            return record
        elif THONG_KE_THEO=='KHACH_HANG_VA_MAT_HANG_THEO_QUY':
            cr = self.env.cr
            query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
            cr.execute(query)
            # Get and show result
            for line in cr.dictfetchall():
                record.append({
                    'MA_HANG': '',
                    'TEN_HANG': '',
                    'DVT': '',
                    'QUI_1_SL': '',
                    'QUI_2_SL': '',
                    'QUI_3_SL': '',
                    'QUI_4_SL': '',
                    'TONG_CONG_SL': '',
                    'QUI_1_DS': '',
                    'QUI_2_DS': '',
                    'QUI_3_DS': '',
                    'QUI_4_DS': '',
                    'TONG_CONG_DS': '',
                    'QUI_1_DTT': '',
                    'QUI_2_DS': '',
                    'QUI_3_DS': '',
                    'QUI_4_DS': '',
                    'TONG_CONG_DTT': '',
                    'name': '',
                    'TEN_KHACH_HANG':'',
                    })
            return record
        elif THONG_KE_THEO=='MAT_HANG_THEO_THANG': 
            cr = self.env.cr
            query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
            cr.execute(query)
            # Get and show result
            for line in cr.dictfetchall():
                record.append({
                    'MA_HANG': '',
                    'TEN_HANG': '',
                    'DVT': '',
                    'THANG_1_SL': '',
                    'THANG_2_SL': '',
                    'THANG_3_SL': '',
                    'THANG_4_SL': '',
                    'THANG_5_SL': '',
                    'THANG_6_SL': '',
                    'THANG_7_SL': '',
                    'THANG_8_SL': '',
                    'THANG_9_SL': '',
                    'THANG_10_SL': '',
                    'THANG_11_SL': '',
                    'THANG_12_SL': '',
                    'TONG_CONG_SL': '',
                    'THANG_1_DS': '',
                    'THANG_2_DS': '',
                    'THANG_3_DS': '',
                    'THANG_4_DS': '',
                    'THANG_5_DS': '',
                    'THANG_6_DS': '',
                    'THANG_7_DS': '',
                    'THANG_8_DS': '',
                    'THANG_9_DS': '',
                    'THANG_10_DS': '',
                    'THANG_11_DS': '',
                    'THANG_12_DS': '',
                    'TONG_CONG_DS': '',
                    'THANG_1_DTT': '',
                    'THANG_2_DTT': '',
                    'THANG_3_DTT': '',
                    'THANG_4_DTT': '',
                    'THANG_5_DTT': '',
                    'THANG_6_DTT': '',
                    'THANG_7_DTT': '',
                    'THANG_8_DTT': '',
                    'THANG_9_DTT': '',
                    'THANG_10_DTT': '',
                    'THANG_11_DTT': '',
                    'THANG_12_DTT': '',
                    'TONG_CONG_DTT': '',
                    'name': '',
                    })
            return record
        elif THONG_KE_THEO=='MAT_HANG_THEO_QUY':
            cr = self.env.cr
            query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
            cr.execute(query)
            # Get and show result
            for line in cr.dictfetchall():
                record.append({
                    'MA_HANG': '',
                    'TEN_HANG': '',
                    'DVT': '',
                    'QUI_1_SL': '',
                    'QUI_2_SL': '',
                    'QUI_3_SL': '',
                    'QUI_4_SL': '',
                    'TONG_CONG_SL': '',
                    'QUI_1_DS': '',
                    'QUI_2_DS': '',
                    'QUI_3_DS': '',
                    'QUI_4_DS': '',
                    'TONG_CONG_DS': '',
                    'QUI_1_DTT': '',
                    'QUI_2_DS': '',
                    'QUI_3_DS': '',
                    'QUI_4_DS': '',
                    'TONG_CONG_DTT': '',
                    'name': '',
                    })
            return record


    #@api.onchange('field_name')
    #def _cap_nhat(self):
    #    for item in self:
    #        item.FIELDS_IDS = self.env['model_name'].search([])

    def _validate(self):
        params = self._context
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        SAN_PHAM_IDS_KHvaMHtheothang= params['SAN_PHAM_IDS_KHvaMHtheothang'] if 'SAN_PHAM_IDS_KHvaMHtheothang' in params.keys() else 'False'
        KHACH_HANG_IDS_KHvaMHtheothang= params['KHACH_HANG_IDS_KHvaMHtheothang'] if 'KHACH_HANG_IDS_KHvaMHtheothang' in params.keys() else 'False'
        SAN_PHAM_IDS_KHvaMHtheoquy = params['SAN_PHAM_IDS_KHvaMHtheoquy'] if 'SAN_PHAM_IDS_KHvaMHtheoquy' in params.keys() else 'False'
        KHACH_HANG_IDS_KHvaMHtheoquy = params['KHACH_HANG_IDS_KHvaMHtheoquy'] if 'KHACH_HANG_IDS_KHvaMHtheoquy' in params.keys() else 'False'
        SAN_PHAM_IDS_MHtheothang = params['SAN_PHAM_IDS_MHtheothang'] if 'SAN_PHAM_IDS_MHtheothang' in params.keys() else 'False'
        SAN_PHAM_IDS_MHtheoquy = params['SAN_PHAM_IDS_MHtheoquy'] if 'SAN_PHAM_IDS_MHtheoquy' in params.keys() else 'False'

        if THONG_KE_THEO=='KHACH_HANG_VA_MAT_HANG_THEO_THANG':
            if(SAN_PHAM_IDS_KHvaMHtheothang=='False'):
                raise ValidationError('Bạn chưa chọn <Hàng hóa>. Xin vui lòng chọn lại.')
            elif(KHACH_HANG_IDS_KHvaMHtheothang=='False'):
                raise ValidationError('Bạn chưa chọn <Khách hàng>. Xin vui lòng chọn lại.')
        # validate của các trường hợp thống kê theo Công trình 
        elif THONG_KE_THEO=='KHACH_HANG_VA_MAT_HANG_THEO_QUY':
            if(SAN_PHAM_IDS_KHvaMHtheoquy=='False'):
                raise ValidationError('Bạn chưa chọn <Hàng hóa>. Xin vui lòng chọn lại.')
            elif(KHACH_HANG_IDS_KHvaMHtheoquy=='False'):
                raise ValidationError('Bạn chưa chọn <Khách hàng>. Xin vui lòng chọn lại.')
        # validate của các trường hợp thống kê theo Hợp đồng
        elif THONG_KE_THEO=='MAT_HANG_THEO_THANG':
            if(SAN_PHAM_IDS_MHtheothang=='False'):
                raise ValidationError('Bạn chưa chọn <Hàng hóa>. Xin vui lòng chọn lại.')
        # validate của các trường hợp thống kê theo Đơn đặt hàng
        elif THONG_KE_THEO=='MAT_HANG_THEO_QUY':
            if(SAN_PHAM_IDS_MHtheoquy=='False'):
                raise ValidationError('Bạn chưa chọn <Hàng hóa>. Xin vui lòng chọn lại.')

    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_PHAN_TICH_SO_LUONG_BAN_VA_DOANH_SO_THEO_NAM, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        san_phams = self.env['danh.muc.vat.tu.hang.hoa'].search([])
        khach_hangs = self.env['res.partner'].search([('LA_KHACH_HANG','=','true')])
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        if san_phams:
            result['SAN_PHAM_IDS_KHvaMHtheothang'] = san_phams.ids
            result['SAN_PHAM_IDS_KHvaMHtheoquy'] = san_phams.ids
            result['SAN_PHAM_IDS_MHtheothang'] = san_phams.ids
            result['SAN_PHAM_IDS_MHtheoquy'] = san_phams.ids
        if khach_hangs:
            result['KHACH_HANG_IDS_KHvaMHtheothang'] = khach_hangs.ids
            result['KHACH_HANG_IDS_KHvaMHtheoquy'] = khach_hangs.ids
        return result
    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        Nam = self.get_context('NAM')
        THONG_KE_THEO = self.get_context('THONG_KE_THEO')
        param = ''
        SAN_PHAM_IDS_KHvaMHtheothang = self._context.get('SAN_PHAM_IDS_KHvaMHtheothang')
        SAN_PHAM_IDS_KHvaMHtheoquy = self._context.get('SAN_PHAM_IDS_KHvaMHtheoquy')
        SAN_PHAM_IDS_MHtheothang = self._context.get('SAN_PHAM_IDS_MHtheothang')
        SAN_PHAM_IDS_MHtheoquy = self._context.get('SAN_PHAM_IDS_MHtheoquy')
        KHACH_HANG_IDS_KHvaMHtheothang = self._context.get('KHACH_HANG_IDS_KHvaMHtheothang')
        KHACH_HANG_IDS_KHvaMHtheoquy = self._context.get('KHACH_HANG_IDS_KHvaMHtheoquy')
        if THONG_KE_THEO=='KHACH_HANG_VA_MAT_HANG_THEO_THANG':
            if len(SAN_PHAM_IDS_KHvaMHtheothang)==1 and len(KHACH_HANG_IDS_KHvaMHtheothang)==1 :
                san_pham = SAN_PHAM_IDS_KHvaMHtheothang[0].get('TEN')
                khach_hang =  KHACH_HANG_IDS_KHvaMHtheothang[0].get('name')
                param = 'Năm: %s;Hàng hóa: %s;Khách hàng: %s' % (Nam,san_pham,khach_hang)
            elif len(SAN_PHAM_IDS_KHvaMHtheothang)==1 and len(KHACH_HANG_IDS_KHvaMHtheothang)!=1:
                san_pham = SAN_PHAM_IDS_KHvaMHtheothang[0].get('TEN')
                param = 'Năm: %s;Hàng hóa: %s' % (Nam,san_pham)
            elif len(SAN_PHAM_IDS_KHvaMHtheothang)!=1 and len(KHACH_HANG_IDS_KHvaMHtheothang)==1:
                khach_hang =  KHACH_HANG_IDS_KHvaMHtheothang[0].get('name')
                param = 'Năm: %s;Khách hàng: %s' % (Nam,khach_hang)
            else:
                param = 'Năm: %s' % (Nam,)
            action = self.env.ref('bao_cao.open_report__phan_tich_so_luong_ban_va_doanh_so_theo_nam_khmhtheothang').read()[0]
        elif THONG_KE_THEO=='KHACH_HANG_VA_MAT_HANG_THEO_QUY':
            if len(SAN_PHAM_IDS_KHvaMHtheoquy)==1 and len(KHACH_HANG_IDS_KHvaMHtheoquy)==1 :
                san_pham = SAN_PHAM_IDS_KHvaMHtheoquy[0].get('TEN')
                khach_hang =  KHACH_HANG_IDS_KHvaMHtheoquy[0].get('name')
                param = 'Năm: %s;Hàng hóa: %s;Khách hàng: %s' % (Nam,san_pham,khach_hang)
            elif len(SAN_PHAM_IDS_KHvaMHtheoquy)==1 and len(KHACH_HANG_IDS_KHvaMHtheoquy)!=1:
                san_pham = SAN_PHAM_IDS_KHvaMHtheoquy[0].get('TEN')
                param = 'Năm: %s;Hàng hóa: %s' % (Nam,san_pham)
            elif len(SAN_PHAM_IDS_KHvaMHtheoquy)!=1 and len(KHACH_HANG_IDS_KHvaMHtheoquy)==1:
                khach_hang =  KHACH_HANG_IDS_KHvaMHtheoquy[0].get('name')
                param = 'Năm: %s;Khách hàng: %s' % (Nam,khach_hang)
            else:
                param = 'Năm: %s' % (Nam,)
            action = self.env.ref('bao_cao.open_report__phan_tich_so_luong_ban_va_doanh_so_theo_nam_khmhtheoquy').read()[0]
        elif THONG_KE_THEO=='MAT_HANG_THEO_THANG':
            if len(SAN_PHAM_IDS_MHtheothang)==1:
                san_pham = SAN_PHAM_IDS_MHtheothang[0].get('TEN')
                param = 'Năm: %s;Hàng hóa: %s' % (Nam,san_pham)
            else:
                param = 'Năm: %s' % (Nam,)
            action = self.env.ref('bao_cao.open_report__phan_tich_so_luong_ban_va_doanh_so_theo_nam_mhtheothang').read()[0]
        elif THONG_KE_THEO=='MAT_HANG_THEO_QUY':
            if len(SAN_PHAM_IDS_MHtheoquy)==1:
                san_pham = SAN_PHAM_IDS_MHtheoquy[0].get('TEN')
                param = 'Năm: %s;Hàng hóa: %s' % (Nam,san_pham)
            else:
                param = 'Năm: %s' % (Nam,)
            action = self.env.ref('bao_cao.open_report__phan_tich_so_luong_ban_va_doanh_so_theo_nam_mhtheoquy').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action