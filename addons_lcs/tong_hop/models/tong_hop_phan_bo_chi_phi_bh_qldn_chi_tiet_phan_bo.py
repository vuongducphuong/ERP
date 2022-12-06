# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_PHAN_BO_CHI_PHI_BH_QLDN_CHI_TIET_PHAN_BO(models.Model):
    _name = 'tong.hop.phan.bo.chi.phi.bh.qldn.chi.tiet.phan.bo'
    _description = ''
    _inherit = ['mail.thread']
    MA_DON_VI_ID = fields.Many2one('danh.muc.to.chuc', string='Mã đơn vị', help='Mã đơn vị')
    TEN_DON_VI = fields.Char(string='Tên đơn vị', help='Tên đơn vị',related='MA_DON_VI_ID.TEN_DON_VI',store=True)
    CAP_TO_CHUC = fields.Selection([('1', 'Tổng công ty/Công ty'), ('2', 'Chi nhánh'), ('3', 'Văn phòng/Trung tâm'), ('4', 'Phòng ban'), ('5', 'Phân xưởng'), ('6', 'Nhóm/Tổ/Đội') ], string='Cấp tổ chức', require=True)
    TONG_TIEN = fields.Monetary(string='Tổng tiền', help='Tổng tiền', currency_field='base_currency_id')

    DOI_TUONG_PB_ID = fields.Many2one('danh.muc.to.chuc', string='Đối tượng phân bổ', help='Đối tượng phân bổ')
    TEN_DOI_TUONG_PB = fields.Char(string='Tên đối tượng phân bổ', help='Tên đối tượng phân bổ')
    LOAI = fields.Char(string='Loại', help='Loại')
    TONG_TIEN_PB = fields.Float(string='Tổng tiền', help='Tổng tiền')
    PHAN_BO_CHI_PHI_BH_QLDN_CHI_PHI_KHAC_CHO_DON_VI_ID = fields.Many2one('tong.hop.phan.bo.chi.phi.bh.qldn.chi.phi.khac.cho.don.vi', string='Phân bổ chi phí bh qldn chi phí khác cho đơn vị', help='Phân bổ chi phí bh qldn chi phí khác cho đơn vị', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    TAI_KHOAN_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK', help='Tài khoản ')
    TY_LE = fields.Float(string='Tỷ lệ(%)', help='Tỷ lệ ')
    SO_TIEN= fields.Monetary(string='Số tiền', help='Số tiền', currency_field='base_currency_id')

    
    base_currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',default=lambda self: self.lay_loai_tien_mac_dinh(), store=True, readonly=True)

    @api.onchange('MA_DON_VI_ID')
    def update_cap_to_chuc(self):
        self.CAP_TO_CHUC = self.MA_DON_VI_ID.CAP_TO_CHUC
    