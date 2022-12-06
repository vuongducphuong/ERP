# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from datetime import timedelta, datetime
from odoo.addons import decimal_precision
class TONG_HOP_LAP_BAO_CAO_TAI_CHINH(models.Model):
    _name = 'tong.hop.lap.bao.cao.tai.chinh'
    _description = ''
    _auto = False

    KY = fields.Selection([('NAM_NAY', 'Năm'), ('QUY_1', ' Qúy 1'), ('QUY_2', 'Qúy 2'), ('QUY_3', 'Qúy 3'), ('QUY_4', ' Qúy 4'), ('6_THANG_DAU_NAM', '6 tháng đầu năm'), ('6_THANG_CUOI_NAM', ' 6 tháng cuối năm'), ('THANG_1', ' Tháng 1'), ('THANG_2', 'Tháng 2'), ('THANG_3', 'Tháng 3'), ('THANG_4', 'Tháng 4'), ('THANG_5', ' Tháng 5'), ('THANG_6', 'Tháng 6'), ('THANG_7', 'Tháng 7'), ('THANG_8', 'Tháng 8'), ('THANG_9', 'Tháng 9'), ('THANG_10', 'Tháng 10'), ('THANG_11', 'Tháng 11'), ('THANG_12', 'Tháng 12'), ('TUY_CHON', 'Tùy chọn'), ], string='Kỳ ', help='Kỳ ',default='NAM_NAY',required=True)
    NAM = fields.Integer(string='Năm', help='Năm')
    TU = fields.Date(string='Từ', help='Từ',default=fields.Datetime.now)
    DEN = fields.Date(string='Đến', help='Đến',default=fields.Datetime.now)
    DOANH_NGHIEP_SELECTION = fields.Selection([('DOANH_NGHIEP_DAP_UNG_GIA_DINH_HOAT_DONG_LIEN_TUC', 'Doanh nghiệp đáp ứng giả định hoạt động liên tục'), ('DOANH_NGHIEP_KHONG_DAP_UNG_GIA_DINH_HOAT_DONG_LIEN_TUC', 'Doanh nghiệp không đáp ứng giả định hoạt động liên tục'), ], string='NO_SAVE',default='DOANH_NGHIEP_DAP_UNG_GIA_DINH_HOAT_DONG_LIEN_TUC')
    BU_TRU_CONG_NO_CUA_CUNG_DOI_TUONG_GIUA_CAC_CHI_NHANH = fields.Boolean(string='Bù trừ công nợ của cùng đối tượng giữa các chi nhánh', help='Bù trừ công nợ của cùng đối tượng giữa các chi nhánh',default=True)
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    TONG_HOP_LAP_BAO_CAO_TAI_CHINH_CHI_TIET_IDS = fields.One2many('tong.hop.lap.bao.cao.tai.chinh.chi.tiet', 'LAP_BAO_CAO_TAI_CHINH_ID', string='Lập báo cáo tài chính chi tiết')


    @api.model
    def default_get(self, fields):
        rec = super(TONG_HOP_LAP_BAO_CAO_TAI_CHINH, self).default_get(fields)
        arr_lap_bao_cao_tai_chinh_chi_tiet = []
        lap_bao_cao_tai_chinh_chi_tiet = self.env['tien.ich.thiet.lap.bao.cao.tai.chinh'].search(['|','|','|',('TEN_BAO_CAO','=','BANG_CAN_DOI_KE_TOAN'),('TEN_BAO_CAO','=','BAO_CAO_KET_QUA_HOAT_DONG_KINH_DOANH'),('TEN_BAO_CAO','=','BAO_CAO_LUU_CHUYEN_TIEN_TE_TRUC_TIEP'),('TEN_BAO_CAO','=','BAO_CAO_LUU_CHUYEN_TIEN_TE_GIAN_TIEP')])
        rec['TONG_HOP_LAP_BAO_CAO_TAI_CHINH_CHI_TIET_IDS'] =[]
        for chi_tiet in lap_bao_cao_tai_chinh_chi_tiet:
             arr_lap_bao_cao_tai_chinh_chi_tiet +=[(0,0,{
                    'MA_BAO_CAO_ID':chi_tiet.id,
                    'TEN_BAO_CAO':chi_tiet.TEN_BAO_CAO,   
                })]
        rec['TONG_HOP_LAP_BAO_CAO_TAI_CHINH_CHI_TIET_IDS'] +=arr_lap_bao_cao_tai_chinh_chi_tiet
        rec['NAM'] = datetime.now().year
        return rec

    @api.onchange('KY')
    def _cap_nhat_ngay(self):
        self.onchange_time(self.KY, 'TU', 'DEN')


    # @api.multi
    # def btn_dong_y(self):
        
    #     action = self.env.ref('tong_hop.open_tong_hop_bao_cao_tai_chinh_tham_so_form').read()[0]
    #     return action
