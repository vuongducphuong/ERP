# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class SUPPLY_KHAI_BAO_CCDC_DAU_KY_THIET_LAP_PB(models.Model):
    _name = 'supply.khai.bao.dau.ky.thiet.lap.pb'
    _description = ''
    _inherit = ['mail.thread']
    DOI_TUONG_PHAN_BO_ID = fields.Reference(selection=[('danh.muc.doi.tuong.tap.hop.chi.phi', 'Đối tượng THCP'),
                                                        ('danh.muc.cong.trinh', 'Công trình'),
                                                        ('account.ex.don.dat.hang', 'Đơn hàng'),
                                                        ('sale.ex.hop.dong.ban', 'Hợp đồng'),
                                                        ('danh.muc.to.chuc', 'Đơn vị')], string='Đối tượng phân bổ')
    TEN_DOI_TUONG_PHAN_BO = fields.Char(string='Tên đối tượng phân bổ', help='Tên đối tượng phân bổ')

    
    TY_LE_PB = fields.Float(string='Tỷ lệ pb', help='Tỷ lệ pb')
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk chi phí', help='Tk chi phí')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục chi phí', help='Khoản mục chi phí', oldname='KHOAN_MUC_CHI_PHI_ID')
    CCDC_DAU_KY_CHI_TIET_ID = fields.Many2one('supply.khai.bao.dau.ky.chi.tiet', string='Ccdc đầu kỳ chi tiết', help='Ccdc đầu kỳ chi tiết', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    @api.onchange('DOI_TUONG_PHAN_BO_ID')
    def update_DOI_TUONG_PHAN_BO_ID(self):
        ten_doi_tuong = ''
        if self.DOI_TUONG_PHAN_BO_ID != False:
            if self.DOI_TUONG_PHAN_BO_ID._name =='danh.muc.doi.tuong.tap.hop.chi.phi':
                ten_doi_tuong =self.DOI_TUONG_PHAN_BO_ID.TEN_DOI_TUONG_THCP
            elif self.DOI_TUONG_PHAN_BO_ID._name =='danh.muc.cong.trinh':
                ten_doi_tuong = self.DOI_TUONG_PHAN_BO_ID.TEN_CONG_TRINH
            elif self.DOI_TUONG_PHAN_BO_ID._name =='account.ex.don.dat.hang':
                ten_doi_tuong = self.DOI_TUONG_PHAN_BO_ID.DIEN_GIAI
            elif self.DOI_TUONG_PHAN_BO_ID._name =='sale.ex.hop.dong.ban':
                ten_doi_tuong =self.DOI_TUONG_PHAN_BO_ID.TRICH_YEU
            elif self.DOI_TUONG_PHAN_BO_ID._name =='danh.muc.to.chuc':
                ten_doi_tuong = self.DOI_TUONG_PHAN_BO_ID.TEN_DON_VI
        self.TEN_DOI_TUONG_PHAN_BO = ten_doi_tuong


    @api.model
    def default_get(self, fields):
        rec = super(SUPPLY_KHAI_BAO_CCDC_DAU_KY_THIET_LAP_PB, self).default_get(fields)
       
        rec['TK_NO_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', 'in',('6422','6423'))],limit=1).id
        return rec