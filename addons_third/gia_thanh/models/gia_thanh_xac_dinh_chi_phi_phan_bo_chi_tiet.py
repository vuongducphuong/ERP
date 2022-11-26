# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET(models.Model):
    _name = 'gia.thanh.xac.dinh.chi.phi.phan.bo.chi.tiet'
    _description = ''
    
    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tài khoản', help='Tài khoản')
    TEN_TAI_KHOAN = fields.Char(string='Tên tài khoản', help='Tên tài khoản')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Mã khoản mục CP', help='Mã khoản mục CP')
    TEN_KHOAN_MUC_CP = fields.Char(string='Tên khoản mục CP', help='Tên khoản mục CP')
    TONG_SO_TIEN = fields.Float(string='Tổng số tiền', help='Tổng số tiền')
    SO_CHUA_PHAN_BO = fields.Float(string='Số chưa phân bổ', help='Số chưa phân bổ')
    PHAN_TRAM_PB_LAN_NAY = fields.Float(string='(%) PB lần này', help='Phần trăm phân bổ lần này')
    SO_PHAN_BO_LAN_NAY = fields.Float(string='Số phân bổ lần này', help='Số phân bổ lần này')
    TIEU_THUC_PHAN_BO = fields.Selection([('NGUYEN_VAT_LIEU', 'Nguyên vật liệu trực tiếp'), ('NHAN_CONG', 'Nhân công trực tiếp'), ('CHI_PHI', 'Chi phí trực tiếp (NVLTT, NCTT)'), ('DINH_MUC', 'Định mức'), ('DOANH_THU', 'Doanh thu'), ],string='Tiêu thức phân bổ', help='Tiêu thức phân bổ')
    DOI_TUONG_THCP_ID = fields.Many2many('danh.muc.doi.tuong.tap.hop.chi.phi','dtthcp_gia_thanh_xdcp_phan_bo_chi_tiet_rel', string='Đối tượng THCP', help='Đối tượng tập hợp chi phí')
    SO_DON_HANG_ID = fields.Many2many('account.ex.don.dat.hang','don_hang_thanh_xdcp_phan_bo_chi_tiet_rel', string='Số đơn hàng', help='Số đơn hàng')
    CONG_TRINH_ID = fields.Many2many('danh.muc.cong.trinh','cong_trinh_gia_thanh_xdcp_phan_bo_chi_tiet_rel', string='Công trình', help='Công trình')
    HOP_DONG_BAN_ID = fields.Many2many('sale.ex.hop.dong.ban','hop_dong_ban_gia_thanh_xdcp_phan_bo_chi_tiet_rel', string='Hợp đồng', help='Hợp đồng bán')    
    CHI_TIET_CHUNG_TU = fields.Char(string='Chi tiết chứng từ', help='Chi tiết chứng từ')
    CHI_TIET_ID = fields.Many2one('gia.thanh.tinh.gia.thanh', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    PHAN_BO_CHI_PHI_CHUNG_CHI_TIET_ID = fields.Many2one('gia.thanh.phan.bo.chi.phi.chung', string='Phân bổ chi phí chung chi tiết', help='Phân bổ chi phí chung chi tiết')
    KY_TINH_GIA_THANH_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh', string='Chi tiết', help='Chi tiết', ondelete='cascade')
    GIA_THANH_CHI_TIET_CHUNG_TU_PHAN_BO_CHI_PHI_CHUNG_IDS = fields.One2many('gia.thanh.chi.tiet.chung.tu.phan.bo.chi.phi.chung', 'XAC_DINH_CHI_PHI_PHAN_BO_CHI_TIET_ID', string='Kết quả phân bổ chi tiết')
    
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    @api.onuichange('PHAN_TRAM_PB_LAN_NAY')
    def update_so_phan_bo_lan_nay(self):
        for record in self:
            record.SO_PHAN_BO_LAN_NAY = (record.PHAN_TRAM_PB_LAN_NAY * record.SO_CHUA_PHAN_BO) / 100
    
    @api.onuichange('SO_PHAN_BO_LAN_NAY')
    def update_phan_tram_phan_bo_lan_nay(self):
        for record in self:
            record.PHAN_TRAM_PB_LAN_NAY = (record.SO_PHAN_BO_LAN_NAY / record.SO_CHUA_PHAN_BO) * 100