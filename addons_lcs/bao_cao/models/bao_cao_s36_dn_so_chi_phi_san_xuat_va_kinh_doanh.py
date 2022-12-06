# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_S36_DN_SO_CHI_PHI_SAN_XUAT_VA_KINH_DOANH(models.Model):
    _name = 'bao.cao.s36.dn.so.chi.phi.san.xuat.va.kinh.doanh'
    
    
    _auto = False

    THONG_KE_THEO = fields.Selection([('DOI_TUONG_TAP_HOP_CHI_PHI', 'Đối tượng tập hợp chi phí'), ('HOP_DONG', 'Hợp đồng'), ('DON_HANG', 'Đơn hàng'), ('CONG_TRINH', 'Công trình'), ], string='Thống kê theo', help='Thống kê theo', default='DOI_TUONG_TAP_HOP_CHI_PHI', required='True')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc', default ='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', 'Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo', default='DAU_THANG_DEN_HIEN_TAI', requied='True')
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày', default=fields.Datetime.now, required='True')
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày',default=fields.Datetime.now, required='True')
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản')
    HIEN_THI_SO_HOA_DON = fields.Boolean(string='Hiển thị số hóa đơn', help='Hiển thị số hóa đơn', default='True')
    HIEN_THI_THEO_DANG_MO_RONG = fields.Boolean(string='Hiển thị theo dạng mở rộng', help='Hiển thị theo dạng mở rộng',default='True')
    HIEN_THI_SO_LUONG_VA_DON_VI_TINH_CHINH_CUA_VAT_TU = fields.Boolean(string='Hiển thị số lượng và ĐVT chính của vật tư', help='Hiển thị số lượng và đơn vị tính chính của vật tư')
    NGAY_THANG_GHI_SO = fields.Date(string='Ngày tháng ghi sổ', help='Ngày tháng ghi sổ')
    SO_HIEU = fields.Float(string='Số hiệu', help='Số hiệu')
    NGAY_THANG = fields.Date(string='Ngày tháng', help='Ngày tháng')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TK_DOI_UNG = fields.Char(string='TK đối ứng', help='Tài khoản đối ứng')
    TONG_SO_TIEN = fields.Float(string='Tổng số tiền', help='Tổng số tiền')
    name = fields.Char(string='Name', help='Name', oldname='NAME')


    DOI_TUONG_THCP_IDS = fields.One2many('danh.muc.doi.tuong.tap.hop.chi.phi')
    CONG_TRINH_IDS = fields.One2many('danh.muc.cong.trinh')
    HOP_DONG_IDS = fields.One2many('sale.ex.hop.dong.ban')
    DON_HANG_IDS = fields.One2many('account.ex.don.dat.hang')
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_S36_DN_SO_CHI_PHI_SAN_XUAT_VA_KINH_DOANH, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        doi_tuong_thcps = self.env['danh.muc.doi.tuong.tap.hop.chi.phi'].search([])
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        if doi_tuong_thcps:
            result['DOI_TUONG_THCP_IDS'] = doi_tuong_thcps.ids
        return result

    @api.onchange('THONG_KE_THEO')
    def _onchange_thong_ke_theo(self):
        if self.THONG_KE_THEO == 'DOI_TUONG_TAP_HOP_CHI_PHI':
            doi_tuong_thcps = self.env['danh.muc.doi.tuong.tap.hop.chi.phi'].search([])
            if doi_tuong_thcps:
                self.DOI_TUONG_THCP_IDS = doi_tuong_thcps.ids
        elif self.THONG_KE_THEO == 'HOP_DONG':
            hop_dongs = self.env['sale.ex.hop.dong.ban'].search([])
            if hop_dongs:
                self.HOP_DONG_IDS = hop_dongs.ids
        elif self.THONG_KE_THEO == 'DON_HANG':
            don_hangs = self.env['account.ex.don.dat.hang'].search([])
            if don_hangs:
                self.DON_HANG_IDS = don_hangs.ids
        elif self.THONG_KE_THEO == 'CONG_TRINH':
            cong_trinhs = self.env['danh.muc.cong.trinh'].search([])
            if cong_trinhs:
                self.CONG_TRINH_IDS = cong_trinhs.ids
    


    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU_NGAY', 'DEN_NGAY')

    def _validate(self):
        params = self._context
        THONG_KE_THEO = params['THONG_KE_THEO'] if 'THONG_KE_THEO' in params.keys() else 'False'
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        TU_NGAY = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DEN_NGAY = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DOI_TUONG_THCP_IDS = params['DOI_TUONG_THCP_IDS'] if 'DOI_TUONG_THCP_IDS' in params.keys() else 'False'
        HOP_DONG_IDS = params['HOP_DONG_IDS'] if 'HOP_DONG_IDS' in params.keys() else 'False'
        DON_HANG_IDS = params['DON_HANG_IDS'] if 'DON_HANG_IDS' in params.keys() else 'False'
        CONG_TRINH_IDS = params['CONG_TRINH_IDS'] if 'CONG_TRINH_IDS' in params.keys() else 'False'
        TAI_KHOAN_ID = params['TAI_KHOAN_ID'] if 'TAI_KHOAN_ID' in params.keys() else 'False'

        if(TU_NGAY=='False'):
            raise ValidationError('<Từ ngày> không được bỏ trống.')
        elif(DEN_NGAY=='False'):
            raise ValidationError('<Đến ngày> không được bỏ trống.')
        elif(TU_NGAY > DEN_NGAY):
            raise ValidationError('<Đến ngày> phải lớn hơn hoặc bằng <Từ ngày>.')
        elif TAI_KHOAN_ID =='False':
            raise ValidationError('<Tài khoản> không được bỏ trống.')
        elif THONG_KE_THEO == 'DOI_TUONG_TAP_HOP_CHI_PHI':
            if DOI_TUONG_THCP_IDS=='False':
                raise ValidationError('Bạn chưa chọn <Đối tượng tập hợp chi phí>. Xin vui lòng chọn lại.')
        elif THONG_KE_THEO == 'HOP_DONG':
            if HOP_DONG_IDS=='False':
               raise ValidationError('Bạn chưa chọn <Hợp đồng/ dự án>. Xin vui lòng chọn lại.')
        elif THONG_KE_THEO == 'DON_HANG':
            if DON_HANG_IDS=='False':
                raise ValidationError('Bạn chưa chọn <Đơn hàng>. Xin vui lòng chọn lại.')
        elif THONG_KE_THEO == 'CONG_TRINH':
            if CONG_TRINH_IDS=='False':
                raise ValidationError('Bạn chưa chọn <Công trình>. Xin vui lòng chọn lại.')


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
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        TAI_KHOAN_ID = params['TAI_KHOAN_ID'] if 'TAI_KHOAN_ID' in params.keys() else 'False'
        HIEN_THI_SO_HOA_DON = params['HIEN_THI_SO_HOA_DON'] if 'HIEN_THI_SO_HOA_DON' in params.keys() else 'False'
        HIEN_THI_THEO_DANG_MO_RONG = params['HIEN_THI_THEO_DANG_MO_RONG'] if 'HIEN_THI_THEO_DANG_MO_RONG' in params.keys() else 'False'
        HIEN_THI_SO_LUONG_VA_DON_VI_TINH_CHINH_CUA_VAT_TU = params['HIEN_THI_SO_LUONG_VA_DON_VI_TINH_CHINH_CUA_VAT_TU'] if 'HIEN_THI_SO_LUONG_VA_DON_VI_TINH_CHINH_CUA_VAT_TU' in params.keys() else 'False'

        DOI_TUONG_THCP_IDS = params['DOI_TUONG_THCP_IDS'] if 'DOI_TUONG_THCP_IDS' in params.keys() else 'False'
        CONG_TRINH_IDS = params['CONG_TRINH_IDS'] if 'CONG_TRINH_IDS' in params.keys() else 'False'
        HOP_DONG_IDS = params['HOP_DONG_IDS'] if 'HOP_DONG_IDS' in params.keys() else 'False'
        DON_HANG_IDS = params['DON_HANG_IDS'] if 'DON_HANG_IDS' in params.keys() else 'False'
        # Execute SQL query here
        cr = self.env.cr
        query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
        cr.execute(query)
        # Get and show result
        for line in cr.dictfetchall():
            record.append({
                'NGAY_THANG_GHI_SO': '',
                'SO_HIEU': '',
                'NGAY_THANG': '',
                'DIEN_GIAI': '',
                'TK_DOI_UNG': '',
                'TONG_SO_TIEN': '',
                'name': '',
                })
        return record


    def _action_view_report(self):
        self._validate()
        TU_NGAY = self.get_vntime('TU_NGAY')
        DEN_NGAY = self.get_vntime('DEN_NGAY')
        TAI_KHOAN_ID = self.get_context('TAI_KHOAN_ID')
        TU_NGAY = self.get_vntime('TU_NGAY')
        param = 'Từ ngày: %s đến ngày %s' % (TU_NGAY, DEN_NGAY)
        action = self.env.ref('bao_cao.open_report__s36_dn_so_chi_phi_san_xuat_va_kinh_doanh').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action