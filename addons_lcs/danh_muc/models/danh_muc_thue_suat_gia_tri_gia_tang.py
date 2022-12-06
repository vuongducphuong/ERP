# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_THUE_SUAT_GIA_TRI_GIA_TANG(models.Model):
    _name = 'danh.muc.thue.suat.gia.tri.gia.tang'
    _description = 'Danh mục vật tư hàng hóa'
    _inherit = ['mail.thread']
    name = fields.Char(string='name', help='name' , related='TEN_THUE', store=True)
    TEN_THUE = fields.Char(string='Tên thuế', help='Tên thuế')
    DIEN_GIAI_THUE = fields.Char (string='Diễn giải thuế',help='Diễn giải thuế')
    PHAN_TRAM_THUE_GTGT = fields.Float(string='Phần trăm thuế GTGT',digits=(16, 4),help='Phần trăm thuế GTGT')

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if name and name.isdigit() and '%' not in name:
            name += '%'
        return super(DANH_MUC_THUE_SUAT_GIA_TRI_GIA_TANG, self).name_search(name, args, operator, limit)

    # @api.model_cr
    # def init(self):
    #     # Remove các thuế suất được tạo thừa
    #     cr = self._cr
    #     cr.execute('DELETE FROM danh_muc_thue_suat_gia_tri_gia_tang WHERE id > 3')
    