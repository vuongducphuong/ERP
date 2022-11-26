# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError

class HE_THONG_CHON_CHI_NHANH_LAM_VIEC(models.Model):
    _name = 'he.thong.chon.chi.nhanh.lam.viec'
    _auto = False

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', help='Chi nhánh', domain=[('CAP_TO_CHUC','in',['1','2'])], default=lambda self: self.get_chi_nhanh())
    BAO_GOM_CHUNG_TU_CHI_NHANH_PHU_THUOC = fields.Boolean(string='Bao gồm chứng từ chi nhánh phụ thuộc', help='Bao gồm chứng từ chi nhánh phụ thuộc', default=lambda self: self.env.user.BAO_GOM_CHUNG_TU_CHI_NHANH_PHU_THUOC)

    # Thiết lập ngày hạch toán
    def action_view_report(self):
        if (self.get_context('CHI_NHANH_ID')):
            new_cn = self.get_context('CHI_NHANH_ID')
            gom_cn_pt = self.get_context('BAO_GOM_CHUNG_TU_CHI_NHANH_PHU_THUOC') == 'True'
            if self.env.user.CHI_NHANH_ID != new_cn or self.env.user.BAO_GOM_CHUNG_TU_CHI_NHANH_PHU_THUOC != gom_cn_pt:
                self.env.user.write({
                    'CHI_NHANH_ID': new_cn,
                    'BAO_GOM_CHUNG_TU_CHI_NHANH_PHU_THUOC': gom_cn_pt
                })
                return {'reload': True}
        else:
            ValidationError('Vui lòng chọn một chi nhánh làm việc!')