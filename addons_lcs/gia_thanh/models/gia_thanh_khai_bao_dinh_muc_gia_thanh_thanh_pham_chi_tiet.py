# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_KHAI_BAO_DINH_MUC_GIA_THANH_THANH_PHAM_CHI_TIET(models.Model):
    _name = 'gia.thanh.khai.bao.dinh.muc.gttp.chi.tiet'
    _description = ''

    MA_THANH_PHAM_ID = fields.Many2one('danh.muc.vat.tu.hang.hoa', string='Mã thành phẩm', help='Mã thành phẩm')
    TEN_THANH_PHAM = fields.Char(string='Tên thành phẩm', help='Tên thành phẩm')
    DON_VI_TINH_ID = fields.Many2one('danh.muc.don.vi.tinh', string='Đơn vị tính', help='Đơn vị tính')
    NVL_TRUC_TIEP = fields.Float(string='NVL trực tiếp', help='Nguyên vật liệu trực tiếp')
    NVL_GIAN_TIEP = fields.Float(string='NVL gián tiếp', help='Nguyên vật liệu gián tiếp')
    NHAN_CONG_TRUC_TIEP = fields.Float(string='Nhân công trực tiếp', help='Nhân công trực tiếp')
    NHAN_CONG_GIAN_TIEP = fields.Float(string='Nhân công gián tiếp', help='Nhân công gián tiếp')
    KHAU_HAO = fields.Float(string='Khấu hao', help='Khấu hao')
    CHI_PHI_MUA_NGOAI = fields.Float(string='Chi phí mua ngoài', help='Chi phí mua ngoài')
    CHI_PHI_KHAC = fields.Float(string='Chi phí khác', help='Chi phí khác')
    TONG_CONG = fields.Float(string='Tổng cộng', help='Tổng cộng', compute='_compute_tong_tien', store=True)
    name = fields.Char(string='Name', oldname='NAME')
    DOI_TUONG_THCP_ID = fields.Many2one('danh.muc.doi.tuong.tap.hop.chi.phi', string='Đối tượng tập hợp chi phí', help='Đối tượng tập hợp chi phí')
    CHI_TIET_ID = fields.Many2one('gia.thanh.khai.bao.dinh.muc.gttp.form', string='Chi tiết', help='Chi tiết', ondelete='cascade')

    # @api.onchange('NVL_TRUC_TIEP','NVL_GIAN_TIEP','NHAN_CONG_TRUC_TIEP','NHAN_CONG_GIAN_TIEP','KHAU_HAO','CHI_PHI_MUA_NGOAI','CHI_PHI_KHAC')
    # def _onchange_field(self):
    #     self.TONG_CONG = self.NVL_TRUC_TIEP + self.NVL_GIAN_TIEP + self.NHAN_CONG_TRUC_TIEP + self.NHAN_CONG_GIAN_TIEP + self.KHAU_HAO + self.CHI_PHI_MUA_NGOAI + self.CHI_PHI_KHAC

    @api.depends('NVL_TRUC_TIEP','NVL_GIAN_TIEP','NHAN_CONG_TRUC_TIEP','NHAN_CONG_GIAN_TIEP','KHAU_HAO','CHI_PHI_MUA_NGOAI','CHI_PHI_KHAC')
    def _compute_tong_tien(self):
        for record in self:
            record.TONG_CONG = record.NVL_TRUC_TIEP + record.NVL_GIAN_TIEP + record.NHAN_CONG_TRUC_TIEP + record.NHAN_CONG_GIAN_TIEP + record.KHAU_HAO + record.CHI_PHI_MUA_NGOAI + record.CHI_PHI_KHAC
        a = 1