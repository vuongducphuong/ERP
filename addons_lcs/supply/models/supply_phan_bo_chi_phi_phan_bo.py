# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class SUPPLY_PHAN_BO_CHI_PHI_PHAN_BO(models.Model):
    _name = 'supply.phan.bo.chi.phi.phan.bo'
    _description = ''
    _inherit = ['mail.thread']
    MA_CCDC = fields.Many2one('supply.ghi.tang',string='Mã ccdc', help='Mã ccdc')
    TEN_CCDC = fields.Char(string='Tên ccdc', help='Tên ccdc',related='MA_CCDC.TEN_CCDC')
    CHI_PHI_PHAN_BO = fields.Float(string='Chi phí phân bổ', help='Chi phí phân bổ',digits=decimal_precision.get_precision('VND'))
    DOI_TUONG_PHAN_BO_ID = fields.Reference(selection=[('danh.muc.doi.tuong.tap.hop.chi.phi', 'Đối tượng THCP'),
                                                        ('danh.muc.cong.trinh', 'Công trình'),
                                                        ('purchase.ex.hop.dong.mua.hang', 'Hợp đồng'),
                                                        ('sale.ex.hop.dong.ban', 'Hợp đồng'),
                                                        ('danh.muc.to.chuc', 'Đơn vị')], string='Đối tượng phân bổ')
    TEN_DOI_TUONG_PHAN_BO = fields.Char(string='Tên đối tượng phân bổ', help='Tên đối tượng phân bổ',compute='set_ten_doi_tuong_pb',store=True)
    TY_LE = fields.Float(string='Tỷ lệ', help='Tỷ lệ',digits=decimal_precision.get_precision('VND'))
    SO_TIEN = fields.Float(string='Số tiền', help='Số tiền',digits=decimal_precision.get_precision('VND'))
    TK_NO_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='Tk chi phí', help='Tk chi phí')
    KHOAN_MUC_CP_ID = fields.Many2one('danh.muc.khoan.muc.cp', string='Khoản mục cp', help='Khoản mục cp')
    PHAN_BO_CHI_PHI_ID = fields.Many2one('supply.phan.bo.chi.phi', string='Phân bổ chi phí', help='Phân bổ chi phí', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    THU_TU_SAP_XEP = fields.Integer(string='Thứ tự sắp xếp các dòng chi tiết', help='SortOrder' )
    sequence = fields.Integer()
    
    @api.onchange('TY_LE')
    def _onchange_TY_LE(self):
        self.SO_TIEN = self.TY_LE*self.CHI_PHI_PHAN_BO/100


    @api.depends('DOI_TUONG_PHAN_BO_ID')
    def set_ten_doi_tuong_pb(self):
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