# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TONG_HOP_BCTC_THEM_PHU_LUC_FORM(models.Model):
    _name = 'tong.hop.bctc.them.phu.luc.form'
    _description = ''
    _inherit = ['mail.thread']

    AUTO_SELECT = fields.Boolean()
    MA_PHU_LUC_ID = fields.Many2one('tien.ich.thiet.lap.bao.cao.tai.chinh', string='Mã phụ lục', help='Mã phụ lục')
    TEN_PHU_LUC = fields.Char(string='Tên phụ lục', help='Tên phụ lục')
    BAO_CAO_TAI_CHINH_ID = fields.Many2one('tong.hop.bao.cao.tai.chinh', string='Báo cáo tài chính', help='Báo cáo tài chính', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
