# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class SUPPLY_GHI_TANG_HANG_LOAT_CHI_TIET(models.Model):
    _name = 'supply.ghi.tang.hang.loat.chi.tiet'
    _description = ''
    _inherit = ['mail.thread']
    MA_CCDC = fields.Char(string='Mã ccdc', help='Mã ccdc')
    TEN_CCDC = fields.Char(string='Tên ccdc', help='Tên ccdc')
    LOAI_CCDC_ID = fields.Many2one('danh.muc.loai.cong.cu.dung.cu', string='Loại ccdc', help='Loại ccdc')
    NHOM_CCDC = fields.Char(string='Nhóm ccdc', help='Nhóm ccdc')
    LY_DO_GHI_TANG = fields.Char(string='Lý do ghi tăng', help='Lý do ghi tăng')
    DVT = fields.Char(string='Đvt', help='Đvt')
    SO_LUONG = fields.Float(string='Số lượng', help='Số lượng', digits=decimal_precision.get_precision('SO_LUONG'))
    DON_GIA = fields.Float(string='Đơn giá', help='Đơn giá',digits=decimal_precision.get_precision('DON_GIA'))
    THANH_TIEN = fields.Float(string='Thành tiền', help='Thành tiền', digits=decimal_precision.get_precision('VND'))
    NGAY_GHI_TANG = fields.Date(string='Ngày ghi tăng', help='Ngày ghi tăng',default=fields.Datetime.now)
    SO_CHUNG_TU_GHI_TANG = fields.Char(string='Số chứng từ ghi tăng', help='Số chứng từ ghi tăng', auto_num='supply_ghi_tang_hang_loat_chi_tiet_SO_CHUNG_TU_GHI_TANG')
    SO_KY_PHAN_BO = fields.Integer(string='Số kỳ phân bổ', help='Số kỳ phân bổ')
    SO_TIEN_PHAN_BO_HANG_KY = fields.Float(string='Số tiền phân bổ hàng kỳ', help='Số tiền phân bổ hàng kỳ', digits=decimal_precision.get_precision('VND'))
    TK_CHO_PHAN_BO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk chờ phân bổ', help='Tk chờ phân bổ')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    GHI_TANG_HANG_LOAT_ID = fields.Many2one('supply.ghi.tang.cong.cu.dung.cu.hang.loat', string='Ghi tăng hàng loạt', help='Ghi tăng hàng loạt', ondelete='cascade')
    THAM_CHIEU = fields.Char(string='Tham chiếu', help='Tham chiếu',compute='thaydoidvsd')
    ID_GOC = fields.Integer(string='ID gốc', help='ID gốc')
    MODEL_GOC = fields.Char(string='Model gốc', help='Model gốc')

    SUPPLY_GHI_TANG_THIET_LAP_PHAN_BO_IDS = fields.One2many('supply.ghi.tang.thiet.lap.phan.bo', 'GHI_TANG_HANG_LOAT_CHI_TIET_ID', string='Ghi tăng thiết lập phân bổ')
    SUPPLY_GHI_TANG_DON_VI_SU_DUNG_IDS = fields.One2many('supply.ghi.tang.don.vi.su.dung', 'GHI_TANG_HANG_LOAT_CHI_TIET_ID', string='Ghi tăng đơn vị sử dụng')

    @api.onchange('SO_LUONG','DON_GIA')
    def _onchange_SO_LUONG(self):
        self.THANH_TIEN = self.SO_LUONG*self.DON_GIA
        if self.SO_LUONG == 0:
            self.SO_LUONG = 1


    @api.onchange('THANH_TIEN','SO_KY_PHAN_BO')
    def _onchange_SO_KY_PHAN_BO(self):
        self.SO_TIEN_PHAN_BO_HANG_KY = self.THANH_TIEN/self.SO_KY_PHAN_BO
        if self.SO_KY_PHAN_BO == 0:
            self.SO_KY_PHAN_BO = 1

    @api.model
    def default_get(self, fields):
        rec = super(SUPPLY_GHI_TANG_HANG_LOAT_CHI_TIET, self).default_get(fields)
        rec['SO_LUONG'] = 1
        rec['SO_KY_PHAN_BO'] = 1
        rec['TK_CHO_PHAN_BO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '242')], limit = 1).id
        return rec


    @api.depends('SUPPLY_GHI_TANG_DON_VI_SU_DUNG_IDS')
    def thaydoidvsd(self):
        env = self.env['supply.ghi.tang.thiet.lap.phan.bo']
        self.SUPPLY_GHI_TANG_THIET_LAP_PHAN_BO_IDS = []
        # sl = self.SO_LUONG
        tl_pb = 0
        tong_ty_le = 0
        i = 0
        count = len(self.SUPPLY_GHI_TANG_DON_VI_SU_DUNG_IDS)
        for dvsd in self.SUPPLY_GHI_TANG_DON_VI_SU_DUNG_IDS:
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
                    'TEN_DOI_TUONG_PHAN_BO': dvsd.MA_DON_VI_ID.name,  
                    'TY_LE_PB' : tl_pb, 
                    'TK_NO_ID' : 8230,
                })
                self.SUPPLY_GHI_TANG_THIET_LAP_PHAN_BO_IDS += new_line
