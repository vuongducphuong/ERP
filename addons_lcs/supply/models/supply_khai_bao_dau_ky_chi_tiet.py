# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.exceptions import ValidationError

class SUPPLY_KHAI_BAO_CCDC_DAU_KY_CHI_TIET(models.Model):
    _name = 'supply.khai.bao.dau.ky.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MA_CCDC = fields.Char(string='Mã CCDC', help='Mã CCDC')
    TEN_CCDC = fields.Char(string='Tên CCDC', help='Tên CCDC')
    LOAI_CCDC_ID = fields.Many2one('danh.muc.loai.cong.cu.dung.cu', string='Loại CCDC', help='Loại CCDC')
    NHOM_CCDC = fields.Char(string='Nhóm CCDC', help='Nhóm CCDC')
    LY_DO_GHI_TANG = fields.Char(string='Lý do ghi tăng', help='Lý do ghi tăng')
    DON_VI_TINH = fields.Char(string='Đơn vị tính', help='Đơn vị tính')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    NGAY_GHI_TANG = fields.Date(string='Ngày ghi tăng', help='Ngày ghi tăng')
    TONG_SO_KY_PB = fields.Integer(string='Tổng số kỳ pb', help='Tổng số kỳ pb')
    SO_KY_PB_CON_LAI = fields.Integer(string='Số kỳ pb còn lại', help='Số kỳ pb còn lại')
    GIA_TRI_CCDC = fields.Float(string='Giá trị CCDC', help='Giá trị CCDC', digits=decimal_precision.get_precision('VND'))
    GIA_TRI_DA_PHAN_BO = fields.Float(string='Giá trị đã phân bổ', help='Giá trị đã phân bổ', digits=decimal_precision.get_precision('VND'))
    GIA_TRI_CON_LAI = fields.Float(string='Giá trị còn lại', help='Giá trị còn lại', digits=decimal_precision.get_precision('VND'))
    SO_TIEN_PHAN_BO_HANG_KY = fields.Float(string='Số tiền phân bổ hàng kỳ', help='Số tiền phân bổ hàng kỳ', digits=decimal_precision.get_precision('VND'))
    TK_CHO_PHAN_BO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk chờ phân bổ', help='Tk chờ phân bổ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CCDC_DAU_KY_ID = fields.Many2one('supply.khai.bao.dau.ky', string='Ccdc đầu kỳ', help='Ccdc đầu kỳ', ondelete='cascade')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu',compute='thaydoidvsd')

    SUPPLY_KHAI_BAO_CCDC_DAU_KY_THIET_LAP_PB_IDS = fields.One2many('supply.khai.bao.dau.ky.thiet.lap.pb', 'CCDC_DAU_KY_CHI_TIET_ID', string='Thiết lập phân bổ')
    SUPPLY_KHAI_BAO_CCDC_DAU_KY_DON_VI_SD_IDS = fields.One2many('supply.khai.bao.dau.ky.don.vi.sd', 'CCDC_DAU_KY_CHI_TIET_ID', string='Đơn vị sử dụng')

    @api.onchange('GIA_TRI_CCDC','GIA_TRI_DA_PHAN_BO','TONG_SO_KY_PB')
    def _onchange_GIA_TRI_CCDC(self):
        self.GIA_TRI_CON_LAI = self.GIA_TRI_CCDC - self.GIA_TRI_DA_PHAN_BO
        if self.TONG_SO_KY_PB:
            self.SO_TIEN_PHAN_BO_HANG_KY = self.GIA_TRI_CCDC/self.TONG_SO_KY_PB
        else:
            if self.TONG_SO_KY_PB == 0:
                self.TONG_SO_KY_PB = 1
                self.SO_TIEN_PHAN_BO_HANG_KY = self.GIA_TRI_CCDC/self.TONG_SO_KY_PB

    @api.depends('SUPPLY_KHAI_BAO_CCDC_DAU_KY_DON_VI_SD_IDS')
    def thaydoidvsd(self):
        env = self.env['supply.khai.bao.dau.ky.thiet.lap.pb']
        self.SUPPLY_KHAI_BAO_CCDC_DAU_KY_THIET_LAP_PB_IDS = []
        # sl = self.SO_LUONG
        tl_pb = 0
        tong_ty_le = 0
        i = 0
        count = len(self.SUPPLY_KHAI_BAO_CCDC_DAU_KY_DON_VI_SD_IDS)
        tai_chi_phi = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '6423')], limit=1)
        for dvsd in self.SUPPLY_KHAI_BAO_CCDC_DAU_KY_DON_VI_SD_IDS:
            if dvsd.MA_DON_VI_ID:
                doi_tuong_reference = 'danh.muc.to.chuc,' + str(dvsd.MA_DON_VI_ID.id) 
                tong_ty_le += tl_pb

                tl_pb = (dvsd.SO_LUONG / self.SO_LUONG)*100
                i += 1
                if count == 1:
                    tl_pb = 100
                elif i == count:
                    tl_pb = 100 - tong_ty_le

                new_line = env.new({
                    'DOI_TUONG_PHAN_BO_ID': doi_tuong_reference,
                    'TEN_DOI_TUONG_PHAN_BO': dvsd.MA_DON_VI_ID.TEN_DON_VI,  
                    'TY_LE_PB' : tl_pb, 
                    'TK_NO_ID' : tai_chi_phi.id if tai_chi_phi else False,
                })
                self.SUPPLY_KHAI_BAO_CCDC_DAU_KY_THIET_LAP_PB_IDS += new_line
                

                
    @api.model
    def default_get(self, fields):
        rec = super(SUPPLY_KHAI_BAO_CCDC_DAU_KY_CHI_TIET, self).default_get(fields)
        rec['SO_LUONG'] = 1
        tai_khoan_cho_pb = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '242')], limit=1)
        if tai_khoan_cho_pb:
            rec['TK_CHO_PHAN_BO_ID'] = tai_khoan_cho_pb.id
        return rec
        return rec

    # @api.multi
    # def validate(self, vals, option=None):
    #     if vals.get('MA_CCDC') == None:
    #         raise ValidationError('Mã công cụ dụng cụ không được bỏ trống')
    #     elif vals.get('TEN_CCDC') == None:
    #         raise ValidationError('Tên công cụ dụng cụ không được bỏ trống')
    #     elif vals.get('NGAY_GHI_TANG') == None:
    #         raise ValidationError('Ngày ghi tăng không được bỏ trống')
        
