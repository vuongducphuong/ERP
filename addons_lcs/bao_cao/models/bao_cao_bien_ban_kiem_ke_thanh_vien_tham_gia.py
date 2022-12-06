# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError

class bao_cao_bien_ban_kiem_ke_thanh_vien_tham_gia(models.Model):
    _name = 'bao.cao.bien.ban.kiem.ke.thanh.vien.tham.gia'
    _auto = False

    ID_CHUNG_TU = fields.Integer(string='ID_CHUNG_TU')
    HO_VA_TEN = fields.Char(string='HO_VA_TEN', help='AccountObjectName')
    CHUC_DANH = fields.Char(string='CHUC_DANH', help='Position')
    DAI_DIEN = fields.Char(string='DAI_DIEN', help='Representative')
    SortOrderMaster = fields.Integer(string='SortOrderMaster', help='SortOrderMaster')
    STT = fields.Integer(string='STT', help='SortOrder')

    BIEN_BAN_KIEM_KE_ID = fields.Many2one('bao.cao.bien.ban.kiem.ke')
