# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_BANG_KE_THU_MUA_HANG(models.Model):
    _name = 'bao.cao.bang.ke.thu.mua.hang'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh', required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    KY_BAO_CAO = fields.Boolean(string='Kỳ báo cáo', help='Kỳ báo cáo')
    KHOANG_THOI_GIAN = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Khoảng thời gian', help='Khoảng thời gian',default='HOM_NAY', required='True')
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày',default=fields.Datetime.now)
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày',default=fields.Datetime.now)
    NGUOI_PHU_TRACH_THU_MUA_ID = fields.Many2one('res.partner', string='Người phụ trách thu mua', help='Người phụ trách thu mua')
    DIA_CHI_NOI_TO_CHUC_THU_MUA = fields.Char(string='Địa chỉ nơi tổ chức thu mua', help='Địa chỉ nơi tổ chức thu mua')
    HIEN_THI_SO_CHUNG_TU_TRONG_PHAN_GHI_CHU = fields.Boolean(string='Hiển thị số chứng từ trong phần ghi chú', help='Hiển thị số chứng từ trong phần ghi chú')
    THANG = fields.Selection([('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', 'Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ], string='Tháng', help='Tháng',default='THANG_1')
    NAM = fields.Char(string='Năm', help='Năm',default='2018')
    NGAY_THANG_NAM_MUA_HANG = fields.Datetime(string='Ngày tháng năm mua hàng', help='Ngày tháng năm mua hàng')
    TEN_NGUOI_BAN = fields.Char(string='Tên người bán', help='Tên người bán')
    DIA_CHI = fields.Char(string='Địa chỉ', help='Địa chỉ')
    SO_CMT_NHAN_DAN = fields.Char(string='Số CMT nhân dân', help='Số chứng minh thư nhân dân')
    TEN_DAT_HANG = fields.Char(string='Tên đặt hàng', help='Tên đặt hàng')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits=decimal_precision.get_precision('DON_GIA'))
    TONG_GIA_THANH_TOAN = fields.Float(string='Tổng giá thanh toán', help='Tổng giá thanh toán',digits=decimal_precision.get_precision('VND'))
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    GHI_CHU = fields.Char(string='Ghi chú', help='Ghi chú')
    KY_BAO_CAO_SLT = fields.Selection([
        ('THEO_NGAY', 'Theo ngày'),
        ('THEO_THANG', 'Theo tháng'),   
        ], default='THEO_NGAY')


    #FIELD_IDS = fields.One2many('model.name')

    ### START IMPLEMENTING CODE ###
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        record = []
        # Get paramerters here
        params = self._context
        CHI_NHANH_ID = params['CHI_NHANH_ID'] if 'CHI_NHANH_ID' in params.keys() else 'False'
        BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = params['BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC'] if 'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC' in params.keys() else 'False'
        KY_BAO_CAO = params['KY_BAO_CAO'] if 'KY_BAO_CAO' in params.keys() else 'False'
        KHOANG_THOI_GIAN = params['KHOANG_THOI_GIAN'] if 'KHOANG_THOI_GIAN' in params.keys() else 'False'
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        NGUOI_PHU_TRACH_THU_MUA_ID = params['NGUOI_PHU_TRACH_THU_MUA_ID'] if 'NGUOI_PHU_TRACH_THU_MUA_ID' in params.keys() else 'False'
        DIA_CHI_NOI_TO_CHUC_THU_MUA = params['DIA_CHI_NOI_TO_CHUC_THU_MUA'] if 'DIA_CHI_NOI_TO_CHUC_THU_MUA' in params.keys() else 'False'
        HIEN_THI_SO_CHUNG_TU_TRONG_PHAN_GHI_CHU = params['HIEN_THI_SO_CHUNG_TU_TRONG_PHAN_GHI_CHU'] if 'HIEN_THI_SO_CHUNG_TU_TRONG_PHAN_GHI_CHU' in params.keys() else 'False'
        THANG = params['THANG'] if 'THANG' in params.keys() else 'False'
        NAM = params['NAM'] if 'NAM' in params.keys() else 'False'
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
                'KHOANG_THOI_GIAN': '',
                'TU_NGAY': '',
                'DEN_NGAY': '',
                'NGUOI_PHU_TRACH_THU_MUA_ID': '',
                'DIA_CHI_NOI_TO_CHUC_THU_MUA': '',
                'HIEN_THI_SO_CHUNG_TU_TRONG_PHAN_GHI_CHU': '',
                'THANG': '',
                'NAM': '',
                'NGAY_THANG_NAM_MUA_HANG': '',
                'TEN_NGUOI_BAN': '',
                'DIA_CHI': '',
                'SO_CMT_NHAN_DAN': '',
                'TEN_DAT_HANG': '',
                'SO_LUONG': '',
                'DON_GIA': '',
                'TONG_GIA_THANH_TOAN': '',
                'name': '',
                })
        return record

    @api.onchange('KHOANG_THOI_GIAN')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KHOANG_THOI_GIAN, 'TU_NGAY', 'DEN_NGAY')
    
    def _validate(self):
        params = self._context
        if not params.get('active_model'):
            return
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        TU_NGAY_F = datetime.strptime(TU_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        DEN_NGAY_F = datetime.strptime(DEN_NGAY, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')

        if(TU_NGAY=='False'):
            raise ValidationError('<Từ> không được bỏ trống.')
        elif(DEN_NGAY=='False'):
            raise ValidationError('<Đến> không được bỏ trống.')
        elif(TU_NGAY_F > DEN_NGAY_F):
            raise ValidationError('<Đến> phải lớn hơn hoặc bằng <Từ>.')



    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_BANG_KE_THU_MUA_HANG, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        # nhan_viens = self.env['res.partner'].search([('LA_NHAN_VIEN', '=', 'True')])
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        # if nhan_viens : 
        #     result['NGUOI_PHU_TRACH_THU_MUA_ID'] = nhan_viens.id
        return result
    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        TU_NGAY = self.get_vntime('TU_NGAY')
        DEN_NGAY = self.get_vntime('DEN_NGAY')
        param = 'Từ ngày: %s đến ngày %s' % (TU_NGAY, DEN_NGAY)
        action = self.env.ref('bao_cao.open_report__bang_ke_thu_mua_hang').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        action['context'] = eval(action.get('context','{}'))
        action['context'].update({'breadcrumb_ex': param})
        return action