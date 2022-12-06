# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class SUPPLY_PHAN_BO_CHI_PHI_MUC_CHI_PHI(models.Model):
    _name = 'supply.phan.bo.chi.phi.muc.chi.phi'
    _description = ''
    _inherit = ['mail.thread']
    MA_CCDC = fields.Many2one('supply.ghi.tang',string='Mã ccdc', help='Mã ccdc')
    TEN_CCDC = fields.Char(string='Tên ccdc', help='Tên ccdc',related='MA_CCDC.TEN_CCDC')
    LOAI_CCDC_ID = fields.Many2one('danh.muc.loai.cong.cu.dung.cu', string='Loại ccdc', help='Loại ccdc')
    TONG_SO_TIEN_PHAN_BO = fields.Float(string='Tổng số tiền phân bổ', help='Tổng số tiền phân bổ', digits=decimal_precision.get_precision('VND'))
    SO_TIEN_PB_CCDC_DAG_DUNG = fields.Float(string='Số tiền pb ccdc đang dùng', help='Số tiền pb ccdc đang dùng', digits=decimal_precision.get_precision('VND'))
    GIA_TRI_CON_LAI_CUA_CCDC_GIAM = fields.Float(string='Giá trị còn lại của ccdc giảm', help='Giá trị còn lại của ccdc giảm',digits=decimal_precision.get_precision('VND'))
    PHAN_BO_CHI_PHI_ID = fields.Many2one('supply.phan.bo.chi.phi', string='Phân bổ chi phí', help='Phân bổ chi phí', ondelete='cascade')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    @api.onchange('SO_TIEN_PB_CCDC_DAG_DUNG')
    def _onchange_SO_TIEN_PB_CCDC_DAG_DUNG(self):
        if self.SO_TIEN_PB_CCDC_DAG_DUNG:
            self.TONG_SO_TIEN_PHAN_BO = self.SO_TIEN_PB_CCDC_DAG_DUNG + self.GIA_TRI_CON_LAI_CUA_CCDC_GIAM