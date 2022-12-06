# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from datetime import timedelta, datetime

class THUE_CHON_KY_TINH_THUE(models.Model):
    _name = 'thue.chon.ky.tinh.thue'
    _description = ''
    _auto = False

    LOAI_TO_KHAI = fields.Selection([('TO_KHAI_THANG', 'Tờ khai tháng'), ('TO_KHAI_QUY', 'Tờ khai quý'), ('TO_KHAI_LAN_PHAT_SINH', 'Tờ khai lần phát sinh'), ], string='Loại tờ khai', help='Loại tờ khai',default='TO_KHAI_THANG')
    DOANH_NGHIEP_THUOC_THUE_SUAT = fields.Selection([('20', '20%'), ('22', '22%'),], string='Doanh nghiệp thuộc đối tượng áp dụng thuế suất', help='Doanh nghiệp thuộc đối tượng áp dụng thuế suất',default='20')
    THANG = fields.Selection([('1', '1'), ('2', '2'),('3', '3'),('4', '4'),('5', '5'),('6', '6'),('7', '7'),('8', '8'),('9', '9'),('10', '10'),('11', '11'),('12', '12')],string='Tháng', help='Tháng',default='1')
    QUY = fields.Selection([('1', '1'), ('2', '2'),('3', '3'),('4', '4')],string='Quý', help='Quý',default='1')
    NAM = fields.Integer(string='Năm', help='Năm')
    HANG_MUC_KHAI = fields.Selection([('TO_KHAI_LAN_DAU', 'Tờ khai lần đầu'), ('TO_KHAI_BO_SUNG', ' Tờ khai bổ sung'), ], string='Hạng mục khai', help='Hạng mục khai',default='TO_KHAI_BO_SUNG')
    LAN_KHAI = fields.Integer(string='Lần', help='Lần khai')
    NGAY_LAP_KHBS = fields.Date(string='Ngày lập KHBS', help='Ngày lập bản giải trình khai bổ sung',default=fields.Datetime.now)
    NGAY = fields.Integer(string='Ngày', help='Ngày')
    TU_NGAY = fields.Date(string='Từ ngày', help='Từ ngày')
    DEN_NGAY = fields.Date(string='Đến ngày', help='Đến ngày')
    DANH_MUC_NGHANH_NGHE = fields.Selection([('SAN_XUAT_KINH_DOANH', 'Nghành hàng sản xuất, kinh doanh thông thường'), ('THAM_DO_PHAT_TRIEN', 'Từ hoạt động thăm dò, phát triển mỏ và khai thác dầu, khí thiên nhiên'), ('XO_SO_KIEN_THIET', 'Từ hoạt động xổ số kiến thiết của các công ty xổ số kiến thiết'), ], string='Danh mục nghành nghề', help='Danh mục nghành nghề',default='SAN_XUAT_KINH_DOANH')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    KHOAN_MUC_THUE = fields.Selection([('TT26', 'Tờ khai thuế GTGT khấu trừ (01/GTGT)'), ('TT119', 'Tờ khai thuế GTGT khấu trừ (01/GTGT)'),('THUE_GTGT_DU_AN_DAU_TU', 'Tờ khai thuế GTGT cho dự án đầu tư (02/GTGT)'),('THUE_GTGT_TRUC_TIEP_TREN_GTGT', 'Tờ khai thuế GTGT trực tiếp trên GTGT (03/GTGT)'),('QUYET_TOAN_THUE_TNDN', 'Quyết toán thuế TNDN năm (03/TNDN)'),('TIEU_THU_DAC_BIET', 'Tờ khai thuế tiêu thụ đặc biệt (01/TTĐB)'),('THUE_TAI_NGUYEN', 'Tờ khai thuế tài nguyên (01/TAIN)')  ], string='Khoản mục thuế', help='Khoản mục thuế')
    THUE_PHU_LUC_KE_KHAI_IDS = fields.One2many('thue.phu.luc.ke.khai', 'CHI_TIET_ID', string='Phụ lục kê khai')

    FIELD_IDS = fields.One2many('model.name')
    @api.model
    def default_get(self, default_fields):
        result = super(THUE_CHON_KY_TINH_THUE, self).default_get(default_fields)
        result['LAN_KHAI'] = 1
        result['THANG'] = str(datetime.now().month)
        result['NAM'] = datetime.now().year
        result['NGAY'] = datetime.now().day
        
        return result
    @api.onchange('LOAI_TO_KHAI')
    def update_HANG_MUC_KHAI(self):
        self.HANG_MUC_KHAI = 'TO_KHAI_LAN_DAU'
    
    def lay_danh_sach_phu_luc_ke_khai(self, args):
        phu_luc_thue_ke_khai = [[5]]
        khoan_muc_thue = args.get('khoan_muc_thue')
        if khoan_muc_thue =='TT26':
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-1/GTGT','TEN_PHU_LUC':'Bảng kê bán ra thuế GTGT',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-2/GTGT','TEN_PHU_LUC':'Bảng kê mua vào thuế GTGT',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-5/GTGT','TEN_PHU_LUC':'Bảng kê số thuế GTGT đã nộp của doanh thu kinh doanh XD, lắp đặt, bán hàng bất động sản ngoại tỉnh',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-6/GTGT','TEN_PHU_LUC':'Bảng phân bổ số thuế GTGT cho địa phương nơi đóng trụ sở chính và CSSX trực thuộc không hạch toán kế toán',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-7/GTGT','TEN_PHU_LUC':'Bảng phân bổ số thuế giá trị gia tăng cho các địa phương nơi có công trình xây dựng, lắp đặt liên tỉnh',})]
        elif khoan_muc_thue =='TT119':
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-1/GTGT','TEN_PHU_LUC':'Bảng kê bán ra thuế GTGT',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-2/GTGT','TEN_PHU_LUC':'Bảng kê mua vào thuế GTGT',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-5/GTGT','TEN_PHU_LUC':'Bảng kê số thuế GTGT đã nộp của doanh thu kinh doanh XD, lắp đặt, bán hàng bất động sản ngoại tỉnh',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-6/GTGT','TEN_PHU_LUC':'Bảng phân bổ số thuế GTGT cho địa phương nơi đóng trụ sở chính và CSSX trực thuộc không hạch toán kế toán',})]
        elif khoan_muc_thue =='THUE_GTGT_DU_AN_DAU_TU':
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-2/GTGT','TEN_PHU_LUC':'Phụ lục PL 01-2/GTGT: Bảng kê mua vào thuế GTGT',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-2-1/GTGT','TEN_PHU_LUC':'Phụ lục PL 01-2-1/GTGT: Bảng kê mua vào thuế GTGT',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-2-2/GTGT','TEN_PHU_LUC':'Phụ lục PL 01-2-2/GTGT: Bảng kê mua vào thuế GTGT',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-2-3/GTGT','TEN_PHU_LUC':'Phụ lục PL 01-2-3/GTGT: Bảng kê mua vào thuế GTGT',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-2-4/GTGT','TEN_PHU_LUC':'Phụ lục PL 01-2-4/GTGT: Bảng kê mua vào thuế GTGT',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-2-5/GTGT','TEN_PHU_LUC':'Phụ lục PL 01-2-5/GTGT: Bảng kê mua vào thuế GTGT',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-2-6/GTGT','TEN_PHU_LUC':'Phụ lục PL 01-2-6/GTGT: Bảng kê mua vào thuế GTGT',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-2-7/GTGT','TEN_PHU_LUC':'Phụ lục PL 01-2-7/GTGT: Bảng kê mua vào thuế GTGT',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-2-8/GTGT','TEN_PHU_LUC':'Phụ lục PL 01-2-8/GTGT: Bảng kê mua vào thuế GTGT',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-2-9/GTGT','TEN_PHU_LUC':'Phụ lục PL 01-2-9/GTGT: Bảng kê mua vào thuế GTGT',})]
        elif khoan_muc_thue =='QUYET_TOAN_THUE_TNDN':
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'03-1A/TNDN','TEN_PHU_LUC':'Kết quả hoạt động sản xuất kinh doanh',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'03-2A/TNDN','TEN_PHU_LUC':'Chuyển lỗ từ hoạt động sản xuất kinh doanh',})]
        elif khoan_muc_thue =='TIEU_THU_DAC_BIET':
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL 01-1/TTĐB','TEN_PHU_LUC':'Bảng xác định số thuế tiêu thụ đặc biệt được khấu trừ (nếu có)',})]
            phu_luc_thue_ke_khai +=[(0,0,{'MA_PHU_LUC':'PL-BKBR/TTĐB','TEN_PHU_LUC':'Bảng kê hóa đơn, hàng hóa, dịch vụ bán ra chịu thuế tiêu thụ đặc biệt',})]

        return {'THUE_PHU_LUC_KE_KHAI_IDS':phu_luc_thue_ke_khai,
                'KHOAN_MUC_THUE':khoan_muc_thue,}
