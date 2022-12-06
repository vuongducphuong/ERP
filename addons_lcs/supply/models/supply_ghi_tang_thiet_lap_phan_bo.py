# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SUPPLY_GHI_TANG_THIET_LAP_PHAN_BO(models.Model):
    _name = 'supply.ghi.tang.thiet.lap.phan.bo'
    _description = ''
    _inherit = ['mail.thread']
    DOI_TUONG_PHAN_BO_ID = fields.Reference(selection=[('danh.muc.doi.tuong.tap.hop.chi.phi', 'Đối tượng THCP'),
                                                        ('danh.muc.cong.trinh', 'Công trình'),
                                                        ('account.ex.don.dat.hang', 'Đơn hàng'),
                                                        ('sale.ex.hop.dong.ban', 'Hợp đồng'),
                                                        ('danh.muc.to.chuc', 'Đơn vị')], string='Đối tượng phân bổ', required=True)

    TEN_DOI_TUONG_PHAN_BO = fields.Char(string='Tên đối tượng phân bổ', help='Tên đối tượng phân bổ',compute='set_ten_doi_tuong_pb',store=True)
    TY_LE_PB = fields.Float(string='Tỷ lệ PB(%)', help='Tỷ lệ pb')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK chi phí', help='Tk chi phí')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục chi phí', help='Khoản mục chi phí', oldname='KHOAN_MUC_CHI_PHI_ID')
    GHI_TANG_THIET_LAP_PHAN_BO_ID = fields.Many2one('supply.ghi.tang', string='Ghi tăng thiết lập phân bổ', help='Ghi tăng đối tượng phân bổ', ondelete='cascade')
    # GHI_TANG_CCDC_HANG_LOAT_ID = fields.Many2one('supply.ghi.tang.hang.loat', string='Ghi tăng ccdc hàng loạt', help='Ghi tăng ccdc hàng loạt')
    GHI_TANG_HANG_LOAT_CHI_TIET_ID = fields.Many2one('supply.ghi.tang.hang.loat.chi.tiet', string='Ghi tăng hàng loạt chi tiết', help='Ghi tăng hàng loạt chi tiết', ondelete='set null')

    LOAI_DOI_TUONG = fields.Selection([('0', 'Đối tượng tập hợp chi phí'), ('1', 'Công trình'),('2', 'Đơn hàng'), ('3', 'Hợp đồng'), ('4', 'Đơn vị')], string='Loại đối tượng')
    THU_TU_SAP_XEP = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết', help='SortOrder' )
    sequence = fields.Integer() 
    @api.model
    def default_get(self, fields):
        rec = super(SUPPLY_GHI_TANG_THIET_LAP_PHAN_BO, self).default_get(fields)
        # rec['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '6423')],limit=1).id
        # rec['TK_NO_ID'] = 100
        return rec

    @api.depends('DOI_TUONG_PHAN_BO_ID')
    def set_ten_doi_tuong_pb(self):
        ten_doi_tuong = ''
        for record in self:
            if record.DOI_TUONG_PHAN_BO_ID:
                if record.DOI_TUONG_PHAN_BO_ID._name =='danh.muc.doi.tuong.tap.hop.chi.phi':
                    ten_doi_tuong = record.DOI_TUONG_PHAN_BO_ID.TEN_DOI_TUONG_THCP
                elif record.DOI_TUONG_PHAN_BO_ID._name =='danh.muc.cong.trinh':
                    ten_doi_tuong = record.DOI_TUONG_PHAN_BO_ID.TEN_CONG_TRINH
                elif record.DOI_TUONG_PHAN_BO_ID._name =='account.ex.don.dat.hang':
                    ten_doi_tuong = record.DOI_TUONG_PHAN_BO_ID.DIEN_GIAI
                elif record.DOI_TUONG_PHAN_BO_ID._name =='sale.ex.hop.dong.ban':
                    ten_doi_tuong =record.DOI_TUONG_PHAN_BO_ID.TRICH_YEU
                elif record.DOI_TUONG_PHAN_BO_ID._name =='danh.muc.to.chuc':
                    ten_doi_tuong = record.DOI_TUONG_PHAN_BO_ID.TEN_DON_VI
            record.TEN_DOI_TUONG_PHAN_BO = ten_doi_tuong

   