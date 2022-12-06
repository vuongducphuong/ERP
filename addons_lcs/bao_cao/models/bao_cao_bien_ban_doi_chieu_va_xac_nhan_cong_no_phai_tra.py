# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_BIEN_BAN_DOI_CHIEU_VA_XAC_NHAN_CONG_NO_PHAI_TRA(models.Model):
    _name = 'bao.cao.bien.ban.doi.chieu.va.xac.nhan.cong.no.phai.tra'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc ', help='Bao gồm số liệu chi nhánh phụ thuộc ',default='true')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default='DAU_THANG_DEN_HIEN_TAI',required=True)
    NHOM_NCC_ID = fields.Many2one('danh.muc.nhom.khach.hang.nha.cung.cap', string='Nhóm NCC', help='Nhóm nhà cung cấp')
    TU = fields.Date(string='Từ', help='Từ',default=fields.Datetime.now,required=True)
    DEN = fields.Date(string='Đến', help='Đến',default=fields.Datetime.now,required=True)
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID',required=True)
    

    TAIKHOAN_IDS = fields.One2many('danh.muc.he.thong.tai.khoan')
    NHACUNGCAP_IDS = fields.One2many('res.partner')

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
        NHOM_NCC_ID = params['NHOM_NCC_ID'] if 'NHOM_NCC_ID' in params.keys() else 'False'
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        currency_id = params['currency_id'] if 'currency_id' in params.keys() else 'False'
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
                'NHOM_NCC_ID': '',
                'TU': '',
                'DEN': '',
                'currency_id': '',
                })
        return record

    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')

    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_BIEN_BAN_DOI_CHIEU_VA_XAC_NHAN_CONG_NO_PHAI_TRA, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        loai_tien = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')],limit=1)
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        if loai_tien:
            result['currency_id'] = loai_tien.id
        tai_khoans =  self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','331'),('SO_TAI_KHOAN','=','1123')])
        if tai_khoans:
            result['TAIKHOAN_IDS'] = tai_khoans.ids
        nha_cung_caps =self.env['res.partner'].search([('LA_NHA_CUNG_CAP','=','True')])
        if nha_cung_caps:
            result['NHACUNGCAP_IDS'] = nha_cung_caps.ids
        return result
    ### END IMPLEMENTING CODE ###
    def _validate(self):
        params = self._context
        NHACUNGCAP_IDS = params['NHACUNGCAP_IDS'] if 'NHACUNGCAP_IDS' in params.keys() else 'False'
        TAIKHOAN_IDS = params['TAIKHOAN_IDS'] if 'TAIKHOAN_IDS' in params.keys() else 'False'
        TU = params['TU'] if 'TU' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN = params['DEN'] if 'DEN' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        if(TU=='False'):
            raise ValidationError('<Từ ngày> không được bỏ trống.')
        elif(DEN=='False'):
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        elif(TU_NGAY_F > DEN_NGAY_F):
            raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')
         # validate của các trường hợp thống kê không chọn
        elif TAIKHOAN_IDS=='False':
            # kiểm tra danh sách khách hàng bị trống
            raise ValidationError('Bạn chưa chọn <Tài khoản>. Xin vui lòng chọn lại.')
        elif NHACUNGCAP_IDS =='False':
            # kiểm tra danh sách khách hàng bị trống
            raise ValidationError('Bạn chưa chọn <Nhà cung cấp>. Xin vui lòng chọn lại.')

    def _action_view_report(self):
        self._validate()
        action = self.env.ref('bao_cao.open_report__bien_ban_doi_chieu_va_xac_nhan_cong_no_phai_tra').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        return action