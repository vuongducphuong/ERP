# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_PHAN_TICH_CONG_NO_PHAI_TRA_THEO_TUOI_NO(models.Model):
    _name = 'bao.cao.phan.tich.cong.no.phai.tra.theo.tuoi.no'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='true')
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày',default=fields.Datetime.now,required=True)
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản',required=True)
    NHOM_NCC_ID = fields.Many2one('danh.muc.nhom.khach.hang.nha.cung.cap', string='Nhóm NCC', help='Nhóm nhà cung cấp')
    MA_NHOM_NCC = fields.Char(string='Mã nhóm NCC', help='Mã nhóm nhà cung cấp')#, auto_num='bao_cao_phan_tich_cong_no_phai_tra_theo_tuoi_no_MA_NHOM_NCC')
    MA_NHA_CUNG_CAP = fields.Char(string='Mã nhà cung cấp', help='Mã nhà cung cấp')#, auto_num='bao_cao_phan_tich_cong_no_phai_tra_theo_tuoi_no_MA_NHA_CUNG_CAP')
    TEN_NHA_CUNG_CAP = fields.Char(string='Tên nhà cung cấp', help='Tên nhà cung cấp')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    TONG_NO = fields.Float(string='Tổng nợ', help='Tổng nợ',digits= decimal_precision.get_precision('VND'))
    KHONG_CO_HAN_NO = fields.Float(string='Không có hạn nợ', help='Không có hạn nợ',digits= decimal_precision.get_precision('VND'))
    NO_TRUOC_HAN_0_30_NGAY = fields.Float(string='0-30 ngày', help='Nợ trước hạn 0-30 ngày',digits= decimal_precision.get_precision('VND'))
    NO_TRUOC_HAN_31_60_NGAY = fields.Float(string='31-60 ngày', help='Nợ trước hạn 31-60 ngày',digits= decimal_precision.get_precision('VND'))
    NO_TRUOC_HAN_61_90_NGAY = fields.Float(string='61-90 ngày', help='Nợ trước hạn 61-90 ngày',digits= decimal_precision.get_precision('VND'))
    NO_TRUOC_HAN_91_120_NGAY = fields.Float(string='91-120 ngày', help='Nợ trước hạn 91-120 ngày',digits= decimal_precision.get_precision('VND'))
    NO_TRUOC_HAN_TREN_120_NGAY = fields.Float(string='trên 120 ngày', help='Nợ trước hạn trên 120 ngày',digits= decimal_precision.get_precision('VND'))
    NO_TRUOC_HAN_TONG = fields.Float(string='Tổng', help='Nợ trước hạn tổng',digits= decimal_precision.get_precision('VND'))
    NO_QUA_HAN_1_30_NGAY = fields.Float(string='1-30 ngày', help='Nợ quá hạn 1-30 ngày',digits= decimal_precision.get_precision('VND'))
    NO_QUA_HAN_31_60_NGAY = fields.Float(string='31-60 ngày', help='Nợ quá hạn 31-60 ngày',digits= decimal_precision.get_precision('VND'))
    NO_QUA_HAN_61_90_NGAY = fields.Float(string='61-90 ngày', help='Nợ quá hạn 61-90 ngày',digits= decimal_precision.get_precision('VND'))
    NO_QUA_HAN_91_120_NGAY = fields.Float(string='91-120 ngày', help='Nợ quá hạn 91-120 ngày',digits= decimal_precision.get_precision('VND'))
    NO_QUA_HAN_TREN_120_NGAY = fields.Float(string='trên 120 ngày', help='Nợ quá hạn trên 120 ngày',digits= decimal_precision.get_precision('VND'))
    NO_QUA_HAN_TONG = fields.Float(string='Tổng', help='Nợ quá hạn tổng',digits= decimal_precision.get_precision('VND'))


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
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        TAI_KHOAN_ID = params['TAI_KHOAN_ID'] if 'TAI_KHOAN_ID' in params.keys() else 'False'
        NHOM_NCC_ID = params['NHOM_NCC_ID'] if 'NHOM_NCC_ID' in params.keys() else 'False'
        # Execute SQL query here
        cr = self.env.cr
        query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
        cr.execute(query)
        # Get and show result
        for line in cr.dictfetchall():
            record.append({
                'CHI_NHANH_ID': '',
                'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC': '',
                'DEN_NGAY': '',
                'TAI_KHOAN_ID': '',
                'NHOM_NCC_ID': '',
                'MA_NHOM_NCC': '',
                'MA_NHA_CUNG_CAP': '',
                'TEN_NHA_CUNG_CAP': '',
                'DIA_CHI': '',
                'TONG_NO': '',
                'KHONG_CO_HAN_NO': '',
                'NO_TRUOC_HAN_0_30_NGAY': '',
                'NO_TRUOC_HAN_31_60_NGAY': '',
                'NO_TRUOC_HAN_61_90_NGAY': '',
                'NO_TRUOC_HAN_91_120_NGAY': '',
                'NO_TRUOC_HAN_TREN_120_NGAY': '',
                'NO_TRUOC_HAN_TONG': '',
                'NO_QUA_HAN_1_30_NGAY': '',
                'NO_QUA_HAN_31_60_NGAY': '',
                'NO_QUA_HAN_61_90_NGAY': '',
                'NO_QUA_HAN_91_120_NGAY': '',
                'NO_QUA_HAN_TREN_120_NGAY': '',
                'NO_QUA_HAN_TONG': '',
                })
        return record

    #@api.onchange('field_name')
    #def _cap_nhat(self):
    #    for item in self:
    #        item.FIELDS_IDS = self.env['model_name'].search([])

    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_PHAN_TICH_CONG_NO_PHAI_TRA_THEO_TUOI_NO, self).default_get(fields_list)
        tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '331')],limit=1)
        nha_cung_caps = self.env['res.partner'].search([('LA_NHA_CUNG_CAP', '=', 'True')])
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        if tai_khoan:
            result['TAI_KHOAN_ID'] = tai_khoan.id
        if nha_cung_caps:
            result['NHACUNGCAP_IDS'] = nha_cung_caps.ids
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        return result
    ### END IMPLEMENTING CODE ###
    def _validate(self):
        params = self._context
        NHACUNGCAP_IDS = params['NHACUNGCAP_IDS'] if 'NHACUNGCAP_IDS' in params.keys() else 'False'
        if NHACUNGCAP_IDS =='False':
            # kiểm tra danh sách khách hàng bị trống
                raise ValidationError('Bạn chưa chọn <Nhà cung cấp>. Xin vui lòng chọn lại.')

    def _action_view_report(self):
        self._validate()
        DEN_NGAY_F = self.get_vntime('DEN_NGAY')
        TAI_KHOAN_ID = self.get_context('TAI_KHOAN_ID')
        tai_khoan =''
        tai_khoan_id = self.env['danh.muc.he.thong.tai.khoan'].browse(TAI_KHOAN_ID)
        if tai_khoan_id:
            tai_khoan = tai_khoan_id.SO_TAI_KHOAN
        param = ''
        nha_cung_caps = self._context.get('NHACUNGCAP_IDS')
        if len(nha_cung_caps) == 1:
            nha_cung_cap = nha_cung_caps[0].get('name')
            param = 'Tài khoản: %s;nhà cung cấp: %s;Đến ngày %s' % (tai_khoan, nha_cung_cap , DEN_NGAY_F)
        else:
            param = 'Tài khoản: %s;Đến ngày %s' % (tai_khoan, DEN_NGAY_F)
        action = self.env.ref('bao_cao.open_report__phan_tich_cong_no_phai_tra_theo_tuoi_no').read()[0]
        action['context'] = eval(action.get('context','{}').replace('\n',''))
        action['context'].update({'breadcrumb_ex': param})
        return action