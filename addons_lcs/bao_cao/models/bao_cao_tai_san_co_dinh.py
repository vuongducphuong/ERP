# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class BAO_CAO_TAI_SAN_CO_DINH(models.Model):
    _name = 'bao.cao.tai.san.co.dinh'
    
    
    _auto = False

    CHI_NHANH_ID = fields.Many2one('res.company', string='Chi nhánh', help='Chi nhánh')
    BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm số liệu chi nhánh phụ thuộc', help='Bao gồm số liệu chi nhánh phụ thuộc',default='True')
    DON_VI_SU_DUNG_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị sử dụng', help='Đơn vị sử dụng')
    LOAI_TAI_SAN_CO_DINH_ID = fields.Many2one('danh.muc.loai.cong.cu.dung.cu', string='Loại tài sản cố định', help='Loại tài sản cố định')
    KY_BAO_CAO = fields.Selection([('HOM_NAY', 'Hôm nay'), ('TUAN_NAY', 'Tuần này'), ('DAU_TUAN_DEN_HIEN_TAI', 'Đầu tuần đến hiện tại'), ('THANG_NAY', 'Tháng này'), ('DAU_THANG_DEN_HIEN_TAI', 'Đầu tháng đến hiện tại'), ('QUY_NAY', 'Quý này'), ('DAU_QUY_DEN_HIEN_TAI', 'Đầu quý đến hiện tại'), ('NAM_NAY', 'Năm nay'), ('DAU_NAM_DEN_HIEN_TAI', 'Đầu năm đến hiện tại'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', '6 tháng cuối năm'), ('THANG_1', 'Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('QUY_1', 'Quý 1'), ('QUY_2', 'Quý 2'), ('QUY_3', 'Quý 3'), ('QUY_4', 'Quý 4'), ('HOM_QUA', 'Hôm qua'), ('TUAN_TRUOC', 'Tuần trước'), ('THANG_TRUOC', 'Tháng trước'), ('QUY_TRUOC', 'Quý trước'), ('NAM_TRUOC', 'Năm trước'), ('TUAN_SAU', 'Tuần sau'), ('THANG_SAU', 'Tháng sau'), ('QUY_SAU', 'Quý sau'), ('NAM_SAU', 'Năm sau'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ báo cáo', help='Kỳ báo cáo',default='DAU_THANG_DEN_HIEN_TAI')
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày',default=fields.Datetime.now)
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày',default=fields.Datetime.now)
    MA_TSCD = fields.Char(string='Mã tscđ', help='Mã tscđ')#, auto_num='bao_cao_tai_san_co_dinh_MA_TSCD')
    SO_HIEU_CT = fields.Float(string='Số hiệu ct', help='Số hiệu ct')
    NGAY_THANG_CT = fields.Datetime(string='Ngày tháng ct', help='Ngày tháng ct')
    NUOC_SAN_XUAT = fields.Char(string='Nước sản xuất', help='Nước sản xuất')
    THANG_NAM_DUA_VAO_SU_DUNG = fields.Datetime(string='Tháng năm đưa vào sử dụng', help='Tháng năm đưa vào sử dụng')
    SO_HIEU_TSCD = fields.Char(string='Số hiệu tscđ', help='Số hiệu tscđ')
    NGUYEN_GIA = fields.Float(string='Nguyên giá', help='Nguyên giá')
    GIA_TRI_TINH_KH = fields.Float(string='Giá trị tính kh', help='Giá trị tính kh')
    TY_LE_KHAU_HAO = fields.Float(string='Tỷ lệ khấu hao', help='Tỷ lệ khấu hao')
    KHAU_HAO = fields.Float(string='Khấu hao', help='Khấu hao')
    KHAU_HAO_LUY_KE = fields.Float(string='Khấu hao lũy kế', help='Khấu hao lũy kế')
    SO_HIEU_CT2 = fields.Char(string='Số hiệu ct2', help='Số hiệu ct2')
    NGAY_THANG_NAM_CT2 = fields.Datetime(string='Ngày tháng năm ct2', help='Ngày tháng năm ct2')
    LY_DO_GIAM_TSCD = fields.Char(string='Lý do giảm tscđ', help='Lý do giảm tscđ')
    STT = fields.Integer(string='STT',help='STT')
    name = fields.Char(string='Name', help='Name', oldname='NAME')


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
        DON_VI_SU_DUNG_ID = params['DON_VI_SU_DUNG_ID'] if 'DON_VI_SU_DUNG_ID' in params.keys() else 'False'
        LOAI_TAI_SAN_CO_DINH_ID = params['LOAI_TAI_SAN_CO_DINH_ID'] if 'LOAI_TAI_SAN_CO_DINH_ID' in params.keys() else 'False'
        KY_BAO_CAO = params['KY_BAO_CAO'] if 'KY_BAO_CAO' in params.keys() else 'False'
        TU_NGAY = params['TU_NGAY'] if 'TU_NGAY' in params.keys() else 'False'
        DEN_NGAY = params['DEN_NGAY'] if 'DEN_NGAY' in params.keys() else 'False'
        # Execute SQL query here
        cr = self.env.cr
        query = """SELECT * FROM danh_muc_vat_tu_hang_hoa"""
        cr.execute(query)
        # Get and show result
        for line in cr.dictfetchall():
            record.append({
                'CHI_NHANH_ID': '',
                'BAO_GOM_SO_LIEU_CHI_NHANH_PHU_THUOC': '',
                'DON_VI_SU_DUNG_ID': '',
                'LOAI_TAI_SAN_CO_DINH_ID': '',
                'KY_BAO_CAO': '',
                'TU_NGAY': '',
                'DEN_NGAY': '',
                'STT': '',
                'MA_TSCD': '',
                'SO_HIEU_CT': '',
                'NGAY_THANG_CT': '',
                'NUOC_SAN_XUAT': '',
                'THANG_NAM_DUA_VAO_SU_DUNG': '',
                'SO_HIEU_TSCD': '',
                'NGUYEN_GIA': '',
                'GIA_TRI_TINH_KH': '',
                'TY_LE_KHAU_HAO': '',
                'KHAU_HAO': '',
                'KHAU_HAO_LUY_KE': '',
                'SO_HIEU_CT2': '',
                'NGAY_THANG_NAM_CT2': '',
                'LY_DO_GIAM_TSCD': '',
                'name': '',
                })
        return record

    #@api.onchange('field_name')
    #def _cap_nhat(self):
    #    for item in self:
    #        item.FIELDS_IDS = self.env['model_name'].search([])

    #@api.model
    #def default_get(self, fields_list):
    #    result = super(BAO_CAO_TAI_SAN_CO_DINH, self).default_get(fields_list)
    #    result['FIELDS_IDS'] = self.env['model_name'].search([]).ids
    #    return result
    ### END IMPLEMENTING CODE ###

    def _action_view_report(self):
        action = self.env.ref('bao_cao.open_report__tai_san_co_dinh').read()[0]
        # action['options'] = {'clear_breadcrumbs': True}
        return action