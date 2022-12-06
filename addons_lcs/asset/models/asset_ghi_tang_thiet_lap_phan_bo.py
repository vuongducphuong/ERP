# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class ASSET_TAI_SAN_CO_DINH_THIET_LAP_PHAN_BO(models.Model):
    _name = 'asset.ghi.tang.thiet.lap.phan.bo'
    _description = ''
    _inherit = ['mail.thread']
    DOI_TUONG_PHAN_BO_ID = fields.Reference(selection=[('danh.muc.doi.tuong.tap.hop.chi.phi', 'Đối tượng THCP'),
                                                        ('danh.muc.cong.trinh', 'Công trình'),
                                                        ('account.ex.don.dat.hang', 'Đơn hàng'),
                                                        ('sale.ex.hop.dong.ban', 'Hợp đồng'),
                                                        ('danh.muc.to.chuc', 'Đơn vị')], string='Đối tượng phân bổ')


    TEN_DOI_TUONG_PHAN_BO = fields.Char(string='Tên đối tượng phân bổ', help='Tên đối tượng phân bổ',compute='update_DOI_TUONG_PHAN_BO_ID',store=True)
    TY_LE_PB = fields.Float(string='Tỷ lệ pb', help='Tỷ lệ pb')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk chi phí', help='Tk chi phí')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục chi phí', help='Khoản mục chi phí', oldname='KHOAN_MUC_CHI_PHI_ID')
    MA_THONG_KE_ID = fields.Many2one('danh.muc.ma.thong.ke', string='Mã thống kê', help='Mã thống kê')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    TAI_SAN_CO_DINH_GHI_TANG_ID = fields.Many2one('asset.ghi.tang', string='Tài sản cố định ghi tăng', help='Tài sản cố định ghi tăng', ondelete='cascade')
    LOAI_DOI_TUONG = fields.Selection([('0', 'ĐT tập hợp CP'), ('1', 'Công trình'), ('2', 'đơn hàng'), ('3', 'hợp đồng'), ('4', 'đơn vị') ], string='Loại đối tượng',compute='update_DOI_TUONG_PHAN_BO_ID',store=True)
    sequence = fields.Integer()

    @api.depends('DOI_TUONG_PHAN_BO_ID')
    def update_DOI_TUONG_PHAN_BO_ID(self):
        ten_doi_tuong = ''
        for record in self:
            if record.DOI_TUONG_PHAN_BO_ID:
                if record.DOI_TUONG_PHAN_BO_ID._name =='danh.muc.doi.tuong.tap.hop.chi.phi':
                    ten_doi_tuong =record.DOI_TUONG_PHAN_BO_ID.TEN_DOI_TUONG_THCP
                    record.LOAI_DOI_TUONG = '0'
                elif record.DOI_TUONG_PHAN_BO_ID._name =='danh.muc.cong.trinh':
                    ten_doi_tuong = record.DOI_TUONG_PHAN_BO_ID.TEN_CONG_TRINH
                    record.LOAI_DOI_TUONG = '1'
                elif record.DOI_TUONG_PHAN_BO_ID._name =='account.ex.don.dat.hang':
                    ten_doi_tuong = record.DOI_TUONG_PHAN_BO_ID.DIEN_GIAI
                    record.LOAI_DOI_TUONG = '2'
                elif record.DOI_TUONG_PHAN_BO_ID._name =='sale.ex.hop.dong.ban':
                    ten_doi_tuong =record.DOI_TUONG_PHAN_BO_ID.TRICH_YEU
                    record.LOAI_DOI_TUONG = '3'
                elif record.DOI_TUONG_PHAN_BO_ID._name =='danh.muc.to.chuc':
                    ten_doi_tuong = record.DOI_TUONG_PHAN_BO_ID.TEN_DON_VI
                    record.LOAI_DOI_TUONG = '4'
            record.TEN_DOI_TUONG_PHAN_BO = ten_doi_tuong
        # self.TEN_DOI_TUONG_PHAN_BO = self.DOI_TUONG_PHAN_BO_ID.name
        # self.TK_NO_ID = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=like', '6424%')], limit=1).id