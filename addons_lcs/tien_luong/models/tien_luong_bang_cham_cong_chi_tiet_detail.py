# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.addons import decimal_precision
import re
import datetime

# TO_FLOAT = re.compile(r"(?<![a-zA-Z:])[-+]?\d*\.?\d+")
TO_FLOAT = re.compile(r"[-+]?\d*\.?\d+")
re_VALID_H = {
    'LTL(Đ)': 'L.*T.*L.*(Đ|D).*',
    'LTL(N)': 'L.*T.*L.*(N|).*',
    'LTN(Đ)': 'L.*T.*N.*(Đ|D).*',
    'LTN(N)': 'L.*T.*N.*N.*',
    'LT(Đ)': 'L.*T.*(Đ|D).*',
    'LT(N)': 'L.*T.*(N|).*',
}
re_VALID = {
    '-': '-',
    '+': '\+',
    'Cô1/2': 'C.*(1|2).*',
    'Cô': 'C.*',
    'H1/2': 'H.*(1|2).*',
    'H': 'H.*',
    'KL1/2': 'K.*(1|2).*',
    'KL': 'K.*',
    'LĐ1/2': 'L.*(Đ|D).*(1|2).*',
    'LĐ': 'L.*(Đ|D).*',
    'NB1/2': 'N.*B.*1',
    'NB': 'N.*B.*',
    'N1/2': 'N.*(1|2).*',
    'N': 'N.*',
    'Ô1/2': '(Ô|O).*(1|2).*',
    'Ô': '(Ô|O).*',
    'SP': 'S.*P.*',
    'P1/2': 'P.*(1|2).*',
    'P': 'P.*',
    'TS1/2': 'T.*S.*(1|2).*',
    'TS': 'T.*S.*',
    'T1/2': 'T.*(1|2).*',
    'T': 'T.*',
}

class TIEN_LUONG_BANG_CHAM_CONG_CHI_TIET_DETAIL(models.Model):
    _name = 'tien.luong.bang.cham.cong.chi.tiet.detail'
    _description = ''
    _inherit = ['mail.thread']
    _order = "SO_THU_TU,id"

    TEN_BANG_CHAM_CONG = fields.Char(string='Tên bảng chấm công', help='Tên bảng chấm công')
    PHONG_BAN = fields.Char(string='Phòng ban', help='Phòng ban')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    SO_THU_TU = fields.Integer(string='STT', help='Số thứ tự')
    MA_NHAN_VIEN = fields.Many2one('res.partner', string='Mã nhân viên', help='Mã nhân viên')
    TEN_NHAN_VIEN = fields.Char(string='Tên nhân viên', help='Tên nhân viên', related='MA_NHAN_VIEN.HO_VA_TEN',store=True )
    NGAY_1 = fields.Char(string='1', help='Ngày 1')
    NGAY_2 = fields.Char(string='2', help='Ngày 2')
    NGAY_3 = fields.Char(string='3', help='Ngày 3')
    NGAY_4 = fields.Char(string='4', help='Ngày 4')
    NGAY_5 = fields.Char(string='5', help='Ngày 5')
    NGAY_6 = fields.Char(string='6', help='Ngày 6')
    NGAY_7 = fields.Char(string='7', help='Ngày 7')
    NGAY_8 = fields.Char(string='8', help='Ngày 8')
    NGAY_9 = fields.Char(string='9', help='Ngày 9')
    NGAY_10 = fields.Char(string='10', help='Ngày 10')
    NGAY_11 = fields.Char(string='11', help='Ngày 11')
    NGAY_12 = fields.Char(string='12', help='Ngày 12')
    NGAY_13 = fields.Char(string='13', help='Ngày 13')
    NGAY_14 = fields.Char(string='14', help='Ngày 14')
    NGAY_15 = fields.Char(string='15', help='Ngày 15')
    NGAY_16 = fields.Char(string='16', help='Ngày 16')
    NGAY_17 = fields.Char(string='17', help='Ngày 17')
    NGAY_18 = fields.Char(string='18', help='Ngày 18')
    NGAY_19 = fields.Char(string='19', help='Ngày 19')
    NGAY_20 = fields.Char(string='20', help='Ngày 20')
    NGAY_21 = fields.Char(string='21', help='Ngày 21')
    NGAY_22 = fields.Char(string='22', help='Ngày 22')
    NGAY_23 = fields.Char(string='23', help='Ngày 23')
    NGAY_24 = fields.Char(string='24', help='Ngày 24')
    NGAY_25 = fields.Char(string='25', help='Ngày 25')
    NGAY_26 = fields.Char(string='26', help='Ngày 26')
    NGAY_27 = fields.Char(string='27', help='Ngày 27')
    NGAY_28 = fields.Char(string='28', help='Ngày 28')
    NGAY_29 = fields.Char(string='29', help='Ngày 29')
    NGAY_30 = fields.Char(string='30', help='Ngày 30')
    NGAY_31 = fields.Char(string='31', help='Ngày 31')
    THANG = fields.Integer(string='Tháng',related='CHI_TIET_ID.thang',store=True)
    NAM = fields.Char(string='Năm',related='CHI_TIET_ID.nam',store=True)
    SO_CONG_HUONG = fields.Float(string='Số công hưởng 100% lương', help='Số công hưởng 100% lương' , digits=decimal_precision.get_precision('SO_CONG'))
    SO_CONG_KHONG_HUONG = fields.Float(string='Số công không hưởng 100% lương', help='Số công không hưởng 100% lương',digits=decimal_precision.get_precision('SO_CONG'))
    NGAY_THUONG_BAN_NGAY = fields.Float(string='Ngày thưởng ban ngày', help='Ngày thưởng ban ngày',digits=decimal_precision.get_precision('SO_CONG'))
    THU_BAY_CHU_NHAT_BAN_NGAY = fields.Float(string='Thứ bảy chủ nhật ban ngày', help='Thứ bảy chủ nhật ban ngày',digits=decimal_precision.get_precision('SO_CONG'))
    LE_TET_BAN_NGAY = fields.Float(string='Lễ tết ban ngày', help='Lễ tết ban ngày',digits=decimal_precision.get_precision('SO_CONG'))
    NGAY_THUONG_BAN_DEM = fields.Float(string='Ngày thường ban đêm', help='Ngày thường ban đêm',digits=decimal_precision.get_precision('SO_CONG'))
    THU_7_CHU_NHAT_BAN_DEM = fields.Float(string='Thứ 7 chủ nhật ban đêm', help='Thứ 7 chủ nhật ban đêm',digits=decimal_precision.get_precision('SO_CONG'))
    LE_TET_BAN_DEM = fields.Float(string='Lễ tết ban đêm', help='Lễ tết ban đêm',digits=decimal_precision.get_precision('SO_CONG'))
    TONG_LAM_THEM = fields.Float(string='Tổng làm thêm', help='Tổng làm thêm',digits=decimal_precision.get_precision('SO_CONG'))
    CHI_TIET_ID = fields.Many2one('tien.luong.bang.cham.cong.chi.tiet.master', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị', related='MA_NHAN_VIEN.DON_VI_ID', store=True, )
    LOAI_CHAM_CONG = fields.Selection([('CHAM_CONG_THEO_BUOI', 'Chấm công theo buổi'), ('CHAM_CONG_THEO_GIO', 'Chấm công theo giờ'), ], related='CHI_TIET_ID.LOAI_CHAM_CONG', store=True)

    so_ngay_cua_thang = fields.Integer(string="Số ngày của tháng", related='CHI_TIET_ID.so_ngay_cua_thang', store=True)
    sequence = fields.Integer()

    
    @api.model
    def default_get(self, fields):
        rec = super(TIEN_LUONG_BANG_CHAM_CONG_CHI_TIET_DETAIL, self).default_get(fields)
        return rec

    @api.onchange('NGAY_1')
    def _onchange_NGAY_1(self):
        self.NGAY_1,_ = self.format_du_lieu(self.NGAY_1)
        self.tinh_cong()

    @api.onchange('NGAY_2')
    def _onchange_NGAY_2(self):
        self.NGAY_2,_ = self.format_du_lieu(self.NGAY_2)
        self.tinh_cong()
    
    @api.onchange('NGAY_3')
    def _onchange_NGAY_3(self):
        self.NGAY_3,_ = self.format_du_lieu(self.NGAY_3)
        self.tinh_cong()
    
    @api.onchange('NGAY_4')
    def _onchange_NGAY_4(self):
        self.NGAY_4,_ = self.format_du_lieu(self.NGAY_4)
        self.tinh_cong()

    @api.onchange('NGAY_5')
    def _onchange_NGAY_5(self):
        self.NGAY_5,_ = self.format_du_lieu(self.NGAY_5)
        self.tinh_cong()
    
    @api.onchange('NGAY_6')
    def _onchange_NGAY_6(self):
        self.NGAY_6,_ = self.format_du_lieu(self.NGAY_6)
        self.tinh_cong()
    
    @api.onchange('NGAY_7')
    def _onchange_NGAY_7(self):
        self.NGAY_7,_ = self.format_du_lieu(self.NGAY_7)
        self.tinh_cong()
    
    @api.onchange('NGAY_8')
    def _onchange_NGAY_8(self):
        self.NGAY_8,_ = self.format_du_lieu(self.NGAY_8)
        self.tinh_cong()

    @api.onchange('NGAY_9')
    def _onchange_NGAY_9(self):
        self.NGAY_9,_ = self.format_du_lieu(self.NGAY_9)
        self.tinh_cong()
    
    @api.onchange('NGAY_10')
    def _onchange_NGAY_10(self):
        self.NGAY_10,_ = self.format_du_lieu(self.NGAY_10)
        self.tinh_cong()
    
    @api.onchange('NGAY_11')
    def _onchange_NGAY_11(self):
        self.NGAY_11,_ = self.format_du_lieu(self.NGAY_11)
        self.tinh_cong()

    @api.onchange('NGAY_12')
    def _onchange_NGAY_12(self):
        self.NGAY_12,_ = self.format_du_lieu(self.NGAY_12)
        self.tinh_cong()
    
    @api.onchange('NGAY_13')
    def _onchange_NGAY_13(self):
        self.NGAY_13,_ = self.format_du_lieu(self.NGAY_13)
        self.tinh_cong()

    @api.onchange('NGAY_14')
    def _onchange_NGAY_14(self):
        self.NGAY_14,_ = self.format_du_lieu(self.NGAY_14)
        self.tinh_cong()

    @api.onchange('NGAY_15')
    def _onchange_NGAY_15(self):
        self.NGAY_15,_ = self.format_du_lieu(self.NGAY_15)
        self.tinh_cong()

    @api.onchange('NGAY_16')
    def _onchange_NGAY_16(self):
        self.NGAY_16,_ = self.format_du_lieu(self.NGAY_16)
        self.tinh_cong()

    @api.onchange('NGAY_17')
    def _onchange_NGAY_17(self):
        self.NGAY_17,_ = self.format_du_lieu(self.NGAY_17)
        self.tinh_cong()
    
    @api.onchange('NGAY_18')
    def _onchange_NGAY_18(self):
        self.NGAY_18,_ = self.format_du_lieu(self.NGAY_18)
        self.tinh_cong()

    @api.onchange('NGAY_19')
    def _onchange_NGAY_19(self):
        self.NGAY_19,_ = self.format_du_lieu(self.NGAY_19)
        self.tinh_cong()

    @api.onchange('NGAY_20')
    def _onchange_NGAY_20(self):
        self.NGAY_20,_ = self.format_du_lieu(self.NGAY_20)
        self.tinh_cong()

    @api.onchange('NGAY_21')
    def _onchange_NGAY_21(self):
        self.NGAY_21,_ = self.format_du_lieu(self.NGAY_21)
        self.tinh_cong()

    @api.onchange('NGAY_22')
    def _onchange_NGAY_22(self):
        self.NGAY_22,_ = self.format_du_lieu(self.NGAY_22)
        self.tinh_cong()

    @api.onchange('NGAY_23')
    def _onchange_NGAY_23(self):
        self.NGAY_23,_ = self.format_du_lieu(self.NGAY_23)
        self.tinh_cong()

    @api.onchange('NGAY_24')
    def _onchange_NGAY_24(self):
        self.NGAY_24,_ = self.format_du_lieu(self.NGAY_24)
        self.tinh_cong()
    
    @api.onchange('NGAY_25')
    def _onchange_NGAY_25(self):
        self.NGAY_25,_ = self.format_du_lieu(self.NGAY_25)
        self.tinh_cong()

    @api.onchange('NGAY_26')
    def _onchange_NGAY_26(self):
        self.NGAY_26,_ = self.format_du_lieu(self.NGAY_26)
        self.tinh_cong()

    @api.onchange('NGAY_27')
    def _onchange_NGAY_27(self):
        self.NGAY_27,_ = self.format_du_lieu(self.NGAY_27)
        self.tinh_cong()

    @api.onchange('NGAY_28')
    def _onchange_NGAY_28(self):
        self.NGAY_28,_ = self.format_du_lieu(self.NGAY_28)
        self.tinh_cong()

    @api.onchange('NGAY_29')
    def _onchange_NGAY_29(self):
        self.NGAY_29,_ = self.format_du_lieu(self.NGAY_29)
        self.tinh_cong()
    
    @api.onchange('NGAY_30')
    def _onchange_NGAY_30(self):
        self.NGAY_30,_ = self.format_du_lieu(self.NGAY_30)
        self.tinh_cong()

    @api.onchange('NGAY_31')
    def _onchange_NGAY_31(self):
        self.NGAY_31,_ = self.format_du_lieu(self.NGAY_31)
        self.tinh_cong()


    NGAY_THUONG_BAN_NGAY = fields.Float(string='Ngày thưởng ban ngày', help='Ngày thưởng ban ngày',digits=decimal_precision.get_precision('SO_CONG'))
    THU_BAY_CHU_NHAT_BAN_NGAY = fields.Float(string='Thứ bảy chủ nhật ban ngày', help='Thứ bảy chủ nhật ban ngày',digits=decimal_precision.get_precision('SO_CONG'))
    LE_TET_BAN_NGAY = fields.Float(string='Lễ tết ban ngày', help='Lễ tết ban ngày',digits=decimal_precision.get_precision('SO_CONG'))
    NGAY_THUONG_BAN_DEM = fields.Float(string='Ngày thường ban đêm', help='Ngày thường ban đêm',digits=decimal_precision.get_precision('SO_CONG'))
    THU_7_CHU_NHAT_BAN_DEM = fields.Float(string='Thứ 7 chủ nhật ban đêm', help='Thứ 7 chủ nhật ban đêm',digits=decimal_precision.get_precision('SO_CONG'))
    LE_TET_BAN_DEM = fields.Float(string='Lễ tết ban đêm', help='Lễ tết ban đêm',digits=decimal_precision.get_precision('SO_CONG'))
    TONG_LAM_THEM = fields.Float(string='Tổng làm thêm', help='Tổng làm thêm',digits=decimal_precision.get_precision('SO_CONG'))

    @api.onchange('NGAY_THUONG_BAN_NGAY','THU_BAY_CHU_NHAT_BAN_NGAY','LE_TET_BAN_NGAY','NGAY_THUONG_BAN_DEM','THU_7_CHU_NHAT_BAN_DEM','LE_TET_BAN_DEM')
    def tinh_tong_lam_them_theo_tung_nhan_vien(self):
        tong_lam_them = 0
        tong_lam_them = self.NGAY_THUONG_BAN_NGAY + self.THU_BAY_CHU_NHAT_BAN_NGAY + self.LE_TET_BAN_NGAY + self.NGAY_THUONG_BAN_DEM + self.THU_7_CHU_NHAT_BAN_DEM + self.LE_TET_BAN_DEM
        self.TONG_LAM_THEM = tong_lam_them

    def tinh_cong(self):
        self.SO_CONG_HUONG = 0
        self.SO_CONG_KHONG_HUONG = 0
        self.LE_TET_BAN_DEM = 0
        self.LE_TET_BAN_NGAY = 0
        self.THU_7_CHU_NHAT_BAN_DEM = 0
        self.THU_BAY_CHU_NHAT_BAN_NGAY = 0
        self.NGAY_THUONG_BAN_DEM = 0
        self.NGAY_THUONG_BAN_NGAY = 0
        
        cong_huong_100 = 0
        for i in range(1,32):
            du_lieu_ngay = self.lay_du_lieu_chuan(getattr(self, 'NGAY_'+str(i)))
            # For lần lượt trong du_lieu_ngay ={}
            # Chấm công theo buổi
            ky_hieu_cong_huong_100 = ['+','H','LĐ','NB','P','TS']
            ky_hieu_cong_huong_100_nua_ngay = ['-','H1/2','LĐ1/2','NB1/2','P1/2','TS1/2']
            ky_hieu_cong_khong_huong_100 = ['Cô','KL','N','Ô','SP','T']
            ky_hieu_cong_khong_huong_100_nua_ngay = ['Cô1/2','KL1/2','N1/2','Ô1/2','T1/2']

            # Ký hiệu chấm công theo giờ
            ky_hieu_cong_huong_100_theo_gio = ['+','H','LĐ','NB','P','TS','-','H1/2','LĐ1/2','NB1/2','P1/2','TS1/2']
            ky_hieu_cong_khong_huong_100_theo_gio = ['Cô','KL','N','Ô','SP','T','Cô1/2','KL1/2','N1/2','Ô1/2','T1/2']

            if self.CHI_TIET_ID.LOAI_CHAM_CONG == 'CHAM_CONG_THEO_BUOI':
                for ky_hieu in du_lieu_ngay:

                    if ky_hieu in ky_hieu_cong_huong_100:
                        self.SO_CONG_HUONG += 1
                    if ky_hieu in ky_hieu_cong_huong_100_nua_ngay:
                        self.SO_CONG_HUONG += 0.5

                    if ky_hieu in ky_hieu_cong_khong_huong_100:
                        self.SO_CONG_KHONG_HUONG += 1
                    if ky_hieu in ky_hieu_cong_khong_huong_100_nua_ngay:
                        self.SO_CONG_KHONG_HUONG += 0.5
                        
                    if ky_hieu == 'LTL(Đ)':
                        self.LE_TET_BAN_DEM += du_lieu_ngay[ky_hieu]
                    if ky_hieu == 'LTL(N)':
                        self.LE_TET_BAN_NGAY += du_lieu_ngay[ky_hieu]
                    if ky_hieu == 'LTN(Đ)':
                        self.THU_7_CHU_NHAT_BAN_DEM += du_lieu_ngay[ky_hieu]
                    if ky_hieu == 'LTN(N)':
                        self.THU_BAY_CHU_NHAT_BAN_NGAY += du_lieu_ngay[ky_hieu]
                    if ky_hieu == 'LT(Đ)':
                        self.NGAY_THUONG_BAN_DEM += du_lieu_ngay[ky_hieu]
                    if ky_hieu == 'LT(N)':
                        self.NGAY_THUONG_BAN_NGAY += du_lieu_ngay[ky_hieu]

            elif self.CHI_TIET_ID.LOAI_CHAM_CONG == 'CHAM_CONG_THEO_GIO':
                for ky_hieu in du_lieu_ngay:

                    if ky_hieu in ky_hieu_cong_huong_100_theo_gio:
                        self.SO_CONG_HUONG += du_lieu_ngay[ky_hieu]
                        
                    if ky_hieu in ky_hieu_cong_khong_huong_100_theo_gio:
                        self.SO_CONG_KHONG_HUONG += du_lieu_ngay[ky_hieu]

                    if ky_hieu == 'LTL(Đ)':
                        self.LE_TET_BAN_DEM += du_lieu_ngay[ky_hieu]
                    if ky_hieu == 'LTL(N)':
                        self.LE_TET_BAN_NGAY += du_lieu_ngay[ky_hieu]
                    if ky_hieu == 'LTN(Đ)':
                        self.THU_7_CHU_NHAT_BAN_DEM += du_lieu_ngay[ky_hieu]
                    if ky_hieu == 'LTN(N)':
                        self.THU_BAY_CHU_NHAT_BAN_NGAY += du_lieu_ngay[ky_hieu]
                    if ky_hieu == 'LT(Đ)':
                        self.NGAY_THUONG_BAN_DEM += du_lieu_ngay[ky_hieu]
                    if ky_hieu == 'LT(N)':
                        self.NGAY_THUONG_BAN_NGAY += du_lieu_ngay[ky_hieu]
                
    def lay_du_lieu_chuan(self, raw, isChamCongTheoBuoi=None):
        struct = {}
        if isChamCongTheoBuoi is None:
            isChamCongTheoBuoi = self.LOAI_CHAM_CONG=='CHAM_CONG_THEO_BUOI'
        if raw:
            for element in raw.split(';'):
                element = element.strip()
                isValid = False
                for v in re_VALID_H:
                    if v in element:
                        h = float(element.split(':')[1])
                        struct.update({v: h})
                        isValid = True
                        break
                
                if not isValid:
                    if isChamCongTheoBuoi:
                        for v in re_VALID:
                            if v in element:
                                struct.update({v: 0})
                                break
                    else:
                        for v in re_VALID:
                            if v in element:
                                default = 8
                                if '2' in element.split(':')[0]:
                                    default = 4
                                h = float(element.split(':')[1]) or default
                                struct.update({v: h})
                                break
                
        return struct

    def format_du_lieu(self, raw):
        if not raw:
            return ('',{})
        result = ''
        struct = {}
        isChamCongTheoBuoi = self.LOAI_CHAM_CONG=='CHAM_CONG_THEO_BUOI'
        for element in raw.split(';'):
            element = element.strip().upper().replace(',','.')
            isValid = False
            for v in re_VALID_H:
                if re.search(re_VALID_H.get(v),element):
                    spl = element.split(':')
                    if len(spl) < 1:
                        spl = element.split(' ')
                    # h = 0
                    se = spl[1] if len(spl) > 1 else element
                    try_float = re.findall(TO_FLOAT, se)
                    h = try_float[0] if len(try_float)>0 else 0
                    result += v + ':' + str(h) +'; '
                    struct.update({v: h})
                    isValid = True
                    break
            
            if not isValid:
                if isChamCongTheoBuoi:
                    for v in re_VALID:
                        if re.search(re_VALID.get(v),element):
                            result += v + '; '
                            struct.update({v: 0})
                            break
                else:
                    for v in re_VALID:
                        spl = element.split(':')
                        if re.search(re_VALID.get(v),spl[0]):
                            h = 8
                            # Có thể chấp nhận dấu space thay :
                            if len(spl) <= 1:
                                spl = element.split(' ')
                            if '1' in spl[0] or '2' in spl[0]:
                                h = 4
                            if len(spl) > 1:
                                se = spl[1]
                                try_float = re.findall(TO_FLOAT, se)
                                if len(try_float) > 0:
                                    h = try_float[0]
                            result += v + ':' + str(h) +'; '
                            struct.update({v: h})
                            break
                
        return result.replace('.',','), struct
    