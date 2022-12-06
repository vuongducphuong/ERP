# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from datetime import timedelta, datetime

class ASSET_KHAI_BAO_TAI_SAN_CO_DINH_DAU_KY_CHI_TIET(models.Model):
    _name = 'asset.khai.bao.dau.ky.chi.tiet'
    _description = ''
    # _inherit = ['mail.thread']
    MA_TAI_SAN = fields.Char(string='Mã tài sản', help='Mã tài sản')
    TEN_TAI_SAN = fields.Char(string='Tên tài sản', help='Tên tài sản')
    LOAI_TAI_SAN_ID = fields.Many2one('danh.muc.loai.tai.san.co.dinh', string='Loại tài sản', help='Loại tài sản')
    DON_VI_SU_DUNG_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị sử dụng', help='Đơn vị sử dụng')
    NGAY_GHI_TANG = fields.Date(string='Ngày ghi tăng', help='Ngày ghi tăng')
    NGAY_BAT_DAU_TINH_KH = fields.Date(string='Ngày bắt đầu tính KH', help='Ngày bắt đầu tính khấu hao')
    DVT_THOI_GIAN_SD = fields.Selection([('0', 'Tháng'), ('1', 'Năm'), ], string='ĐVT thời gian SD', help='Đơn vị tính thời gian sử dụng',required=True,default='0')
    THOI_GIAN_SD_CON_LAI = fields.Float(string='Thời gian SD còn lại', help='Thời gian sử dụng còn lại')
    THOI_GIAN_SU_DUNG = fields.Float(string='Thời gian SD', help='Thời gian sử dụng')
    NGUYEN_GIA = fields.Float(string='Nguyên giá', help='Nguyên giá',digits=decimal_precision.get_precision('VND'))
    GIA_TRI_TINH_KHAU_HAO = fields.Float(string='Giá trị tính khấu hao', help='Giá trị tính khấu hao',digits=decimal_precision.get_precision('VND'))
    HAO_MON_LUY_KE = fields.Float(string='Hao mòn lũy kế', help='Hao mòn lũy kế',digits=decimal_precision.get_precision('VND'))
    GIA_TRI_CON_LAI = fields.Float(string='Giá trị còn lại', help='Giá trị còn lại',digits=decimal_precision.get_precision('VND'))
    GIA_TRI_KH_THANG = fields.Float(string='Giá trị KH tháng', help='Giá trị khấu hao tháng',digits=decimal_precision.get_precision('VND'))
    TK_KHAU_HAO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK khấu hao', help='Tài khoản khấu hao')
    TK_NGUYEN_GIA_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK nguyên giá', help='Tài khoản nguyên giá')
    DOI_TUONG_PHAN_BO_ID = fields.Reference(selection=[('danh.muc.doi.tuong.tap.hop.chi.phi', 'Đối tượng THCP'),
                                                        ('danh.muc.cong.trinh', 'Công trình'),
                                                        ('account.ex.don.dat.hang', 'Đơn hàng'),
                                                        ('sale.ex.hop.dong.ban', 'Hợp đồng'),
                                                        ('danh.muc.to.chuc', 'Đơn vị')], string='Đối tượng phân bổ')
    TY_LE_PB = fields.Float(string='Tỷ lệ PB (%)', help='Tỷ lệ phân bổ')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chi phí', help='Tài khoản chi phí')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục chi phí', help='Khoản mục chi phí', oldname='KHOAN_MUC_CHI_PHI_ID')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    name = fields.Char(string='Name', help='Name', oldname='NAME')    
    KHAI_BAO_TAI_SAN_CO_DINH_DAU_KY_ID = fields.Many2one('asset.khai.bao.dau.ky', string='Khai báo tài sản cố định đầu kỳ', help='Khai báo tài sản cố định đầu kỳ', ondelete='cascade')

    @api.onchange('NGAY_GHI_TANG')
    def _onchange_NGAY_GHI_TANG(self):
        if self.NGAY_GHI_TANG:
            self.NGAY_BAT_DAU_TINH_KH = self.NGAY_GHI_TANG
    
    # @api.onchange('THOI_GIAN_SU_DUNG')
    # def _onchange_THOI_GIAN_SU_DUNG(self):
    #     if self.THOI_GIAN_SU_DUNG:
    #         self.THOI_GIAN_SD_CON_LAI = self.THOI_GIAN_SU_DUNG

    @api.onchange('NGUYEN_GIA')
    def _onchange_NGUYEN_GIA(self):
        if self.NGUYEN_GIA:
            self.GIA_TRI_TINH_KHAU_HAO = self.NGUYEN_GIA

    @api.onchange('HAO_MON_LUY_KE')
    def _onchange_HAO_MON_LUY_KE(self):
        self.GIA_TRI_CON_LAI = self.NGUYEN_GIA - self.HAO_MON_LUY_KE

    @api.onchange('LOAI_TAI_SAN_ID')
    def _onchange_LOAI_TAI_SAN_ID(self):
        self.TK_KHAU_HAO_ID = self.LOAI_TAI_SAN_ID.TK_KHAU_HAO_ID
        self.TK_NGUYEN_GIA_ID = self.LOAI_TAI_SAN_ID.TK_NGUYEN_GIA_ID
        self.TY_LE_PB = 100
    
    @api.onchange('DON_VI_SU_DUNG_ID')
    def _onchange_DON_VI_SU_DUNG_ID(self):
        if self.DON_VI_SU_DUNG_ID:
            self.DOI_TUONG_PHAN_BO_ID = str(self.DON_VI_SU_DUNG_ID._name) + ',Đơn vị,' + str(self.DON_VI_SU_DUNG_ID.id)


    @api.model
    def default_get(self, fields):
        rec = super(ASSET_KHAI_BAO_TAI_SAN_CO_DINH_DAU_KY_CHI_TIET, self).default_get(fields)
       
        return rec



    # @api.depends('DVT_THOI_GIAN_SD','NGAY_BAT_DAU_TINH_KH')
    # def _compute_tinh_thoi_gian_su_dung_con_lai(self):
    #     for record in self:
    #         if record.DVT_THOI_GIAN_SU_DUNG_CON_LAI == '0':
    #             record.THOI_GIAN_SD_CON_LAI = record.THOI_GIAN_SU_DUNG_CON_LAI_NGUYEN_GOC
    #         elif record.DVT_THOI_GIAN_SU_DUNG_CON_LAI == '1':
    #             record.THOI_GIAN_SD_CON_LAI = record.THOI_GIAN_SU_DUNG_CON_LAI_NGUYEN_GOC*12

    @api.onchange('NGAY_BAT_DAU_TINH_KH','THOI_GIAN_SU_DUNG','DVT_THOI_GIAN_SD')
    def _onchange_tinh_thoi_gian_su_dung_con_lai(self):
        nam = self.env['ir.config_parameter'].get_param('he_thong.NAM_TAI_CHINH_BAT_DAU')
        ngay_bat_dau_nam_tai_chinh = datetime(year=int(nam), month=1, day=1)
        thoi_gian_da_su_dung = 0
        if self.NGAY_BAT_DAU_TINH_KH and self.THOI_GIAN_SU_DUNG > 0:
            ngay_bat_dau_tinh_kh = datetime.strptime(self.NGAY_BAT_DAU_TINH_KH, '%Y-%m-%d').date()
            if self.diff_month(ngay_bat_dau_nam_tai_chinh,ngay_bat_dau_tinh_kh) > 0:
                thoi_gian_da_su_dung = self.diff_month(ngay_bat_dau_nam_tai_chinh,ngay_bat_dau_tinh_kh)
            if self.DVT_THOI_GIAN_SD == '1':
                thoi_gian_da_su_dung = thoi_gian_da_su_dung/12
            if  thoi_gian_da_su_dung > 0:
                self.THOI_GIAN_SD_CON_LAI = self.THOI_GIAN_SU_DUNG - thoi_gian_da_su_dung if (self.THOI_GIAN_SU_DUNG - thoi_gian_da_su_dung) > 0 else 0
            else:
                self.THOI_GIAN_SD_CON_LAI = self.THOI_GIAN_SU_DUNG if self.THOI_GIAN_SU_DUNG > 0 else 0

            if self.GIA_TRI_TINH_KHAU_HAO > 0:
                self.GIA_TRI_KH_THANG = self.GIA_TRI_TINH_KHAU_HAO/self.THOI_GIAN_SU_DUNG


    def diff_month(self,d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month


    @api.onchange('GIA_TRI_TINH_KHAU_HAO','THOI_GIAN_SD_CON_LAI')
    def _onchange_GIA_TRI_TINH_KHAU_HAO(self):
        if self.THOI_GIAN_SD_CON_LAI > 0 and self.THOI_GIAN_SU_DUNG > 0:
            thoi_gian_da_su_dung = self.THOI_GIAN_SU_DUNG - self.THOI_GIAN_SD_CON_LAI
            if thoi_gian_da_su_dung > 0:
                self.HAO_MON_LUY_KE = self.GIA_TRI_TINH_KHAU_HAO*(thoi_gian_da_su_dung/self.THOI_GIAN_SU_DUNG)
                self.GIA_TRI_CON_LAI = self.GIA_TRI_TINH_KHAU_HAO - self.HAO_MON_LUY_KE
                self.GIA_TRI_KH_THANG = self.GIA_TRI_TINH_KHAU_HAO/self.THOI_GIAN_SU_DUNG
                

    
    