# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class ASSET_TINH_KHAU_HAO_PHAN_BO(models.Model):
    _name = 'asset.tinh.khau.hao.phan.bo'
    _description = ''
    _inherit = ['mail.thread']
    MA_TAI_SAN_ID = fields.Many2one('asset.ghi.tang', string='Mã tài sản', help='Mã tài sản')
    TEN_TAI_SAN = fields.Char(string='Tên tài sản', help='Tên tài sản',related='MA_TAI_SAN_ID.TEN_TAI_SAN',store=True)
    DON_VI_SU_DUNG_ID = fields.Many2one('danh.muc.to.chuc', string='Đơn vị sử dụng', help='Đơn vị sử dụng')
    GIA_TRI_KH_THANG = fields.Float(string='Giá trị kh tháng', help='Giá trị kh tháng',digits=decimal_precision.get_precision('VND'))
    DOI_TUONG_PHAN_BO_ID = fields.Reference(selection=[('danh.muc.doi.tuong.tap.hop.chi.phi', 'Đối tượng THCP'),
                                                        ('danh.muc.cong.trinh', 'Công trình'),
                                                        ('account.ex.don.dat.hang', 'Đơn hàng'),
                                                        ('sale.ex.hop.dong.ban', 'Hợp đồng'),
                                                        ('danh.muc.to.chuc', 'Đơn vị')], string='Đối tượng phân bổ')
    TEN_DOI_TUONG_PHAN_BO = fields.Char(string='Tên đối tượng phân bổ', help='Tên đối tượng phân bổ',compute='update_DOI_TUONG_PHAN_BO_ID',store=True)
    TY_LE = fields.Float(string='Tỷ lệ', help='Tỷ lệ')
    CHI_PHI_PHAN_BO = fields.Float(string='Chi phí phân bổ', help='Chi phí phân bổ',digits=decimal_precision.get_precision('VND'))
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk chi phí', help='Tk chi phí')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục cp', help='Khoản mục cp')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    TINH_KHAU_HAO_ID = fields.Many2one('asset.tinh.khau.hao', string='Tính khấu hao', help='Tính khấu hao', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    @api.model
    def default_get(self, fields):
        rec = super(ASSET_TINH_KHAU_HAO_PHAN_BO, self).default_get(fields)
        rec['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like', '6424%')], limit=1).id
        return rec

    
    @api.depends('DOI_TUONG_PHAN_BO_ID')
    def update_DOI_TUONG_PHAN_BO_ID(self):
        for record in self:
            ten_doi_tuong = ''
            if record.DOI_TUONG_PHAN_BO_ID != False:
                if record.DOI_TUONG_PHAN_BO_ID._name =='danh.muc.doi.tuong.tap.hop.chi.phi':
                    ten_doi_tuong =record.DOI_TUONG_PHAN_BO_ID.TEN_DOI_TUONG_THCP
                elif record.DOI_TUONG_PHAN_BO_ID._name =='danh.muc.cong.trinh':
                    ten_doi_tuong = record.DOI_TUONG_PHAN_BO_ID.TEN_CONG_TRINH
                elif record.DOI_TUONG_PHAN_BO_ID._name =='account.ex.don.dat.hang':
                    ten_doi_tuong = record.DOI_TUONG_PHAN_BO_ID.DIEN_GIAI
                elif record.DOI_TUONG_PHAN_BO_ID._name =='sale.ex.hop.dong.ban':
                    ten_doi_tuong =record.DOI_TUONG_PHAN_BO_ID.TRICH_YEU
                elif record.DOI_TUONG_PHAN_BO_ID._name =='danh.muc.to.chuc':
                    ten_doi_tuong = record.DOI_TUONG_PHAN_BO_ID.TEN_DON_VI
            record.TEN_DOI_TUONG_PHAN_BO = ten_doi_tuong