# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class BAO_CAO_BAO_CAO_TIEN_DO_SAN_XUAT(models.Model):
    _name = 'bao.cao.bao.cao.tien.do.san.xuat'
    _description = 'Báo cáo tiến độ sản xuất'
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh',required=True)
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default='DAU_THANG_DEN_HIEN_TAI',required='True')
    TU = fields.Date(string='Từ', help='Từ',default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến',default=fields.Datetime.now)
    MA_THANH_PHAM = fields.Char(string='Mã thành phẩm', help='Mã thành phẩm')
    TEN_THANH_PHAM = fields.Char(string='Tên thành phẩm', help='Tên thành phẩm')
    SO_LENH_SAN_XUAT = fields.Char(string='Số lệnh sản xuất', help='Số lệnh sản xuất')
    DVT = fields.Char(string='ĐVT', help='Đơn vị tính')
    SO_LUONG_YEU_CAU = fields.Float(string='Số lượng yêu cầu', help='Số lượng yêu cầu', digits=decimal_precision.get_precision('SO_LUONG'))
    SO_LUONG_SAN_XUAT = fields.Float(string='Số lượng sản xuất', help='Số lượng sản xuất' , digits=decimal_precision.get_precision('SO_LUONG'))
    CHENH_LECH = fields.Float(string='Chênh lệch', help='Chênh lệch')


    LENH_SAN_XUAT = fields.One2many('stock.ex.lenh.san.xuat')

    ### START IMPLEMENTING CODE ###
    @api.model
    def default_get(self, fields_list):
        result = super(BAO_CAO_BAO_CAO_TIEN_DO_SAN_XUAT, self).default_get(fields_list)
        chi_nhanh = self.env['danh.muc.to.chuc'].search([],limit=1)
        if chi_nhanh:
            result['CHI_NHANH_ID'] = chi_nhanh.id
        return result

   

    # def _validate(self):
    #     params = self._context
    #     FIELDS_IDS = params['FIELDS_IDS'] if 'FIELDS_IDS' in params.keys() else 'False'
    #     if(not len(FIELDS_IDS)):
    #         raise ValidationError('Vui lòng kiểm tra lại!')

    def _validate(self):
        params = self._context
        LENH_SAN_XUAT = params['LENH_SAN_XUAT'] if 'LENH_SAN_XUAT' in params.keys() else 'False'
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
        elif LENH_SAN_XUAT =='False':
            raise ValidationError('Bạn chưa chọn <Lệnh sản xuất>. Xin vui lòng chọn lại.')


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
        # Execute SQL query here
        cr = self.env.cr
        query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
        cr.execute(query)
        # Get and show result
        for line in cr.dictfetchall():
            record.append({
                'MA_THANH_PHAM': '',
                'TEN_THANH_PHAM': '',
                'DVT': '',
                'SO_LUONG_YEU_CAU': '',
                'SO_LUONG_SAN_XUAT': '',
                'CHENH_LECH': '',
                })
        return record

    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        self._validate()
        TU_NGAY_F = self.get_vntime('TU')
        DEN_NGAY_F = self.get_vntime('DEN')
        param =''
        lenh_san_xuats = self._context.get('LENH_SAN_XUAT')
        if len(lenh_san_xuats)==1:
            lenh_san_xuat = lenh_san_xuats[0].get('SO_LENH')
            param = 'Lệnh sản xuất: %s;Từ ngày: %s đến ngày %s' % (lenh_san_xuat, TU_NGAY_F, DEN_NGAY_F)
        else:
            param = 'Từ ngày %s đến ngày %s' % ( TU_NGAY_F, DEN_NGAY_F)
        action = self.env.ref('bao_cao.open_report__tien_do_san_xuat').read()[0]
        action['context'] = eval(action.get('context','{}').replace('\n',''))
        action['context'].update({'breadcrumb_ex': param})
        return action


    @api.onchange('KY_BAO_CAO')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY_BAO_CAO, 'TU', 'DEN')

    @api.onchange('TU','DEN')
    def thay_doi_kbc(self):
        if(self.TU < self.DEN):
           self.LENH_SAN_XUAT= self.env['stock.ex.lenh.san.xuat'].search([('NGAY', '>', self.TU),('NGAY', '<', self.DEN)]).ids
        
        
            