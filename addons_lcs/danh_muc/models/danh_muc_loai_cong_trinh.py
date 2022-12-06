# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_LOAI_CONG_TRINH(models.Model):
    _name = 'danh.muc.loai.cong.trinh'
    _description = 'Loại công trình'
    _inherit = ['mail.thread']
    _order = "MA_LOAI_CONG_TRINH"

    MA_LOAI_CONG_TRINH = fields.Char(string='Mã loại công trình', help='Mã loại công trình', required=True)# auto_num='danh_muc_loai_cong_trinh_MA_LOAI_CONG_TRINH')
    name = fields.Char(string='Tên loại công trình', help='Tên loại công trình')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)

    _sql_constraints = [
        ('MA_LOAI_CONG_TRINH_uniq', 'unique ("MA_LOAI_CONG_TRINH")', 'Mã loại công trình <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]