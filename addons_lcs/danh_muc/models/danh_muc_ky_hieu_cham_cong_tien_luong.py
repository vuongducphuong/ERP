# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_KY_HIEU_CHAM_CONG_TIEN_LUONG(models.Model):
    _name = 'danh.muc.ky.hieu.cham.cong.tien.luong'
    _description = 'Danh mục ký hiệu chấm công lương nhân viên'
    _inherit = ['mail.thread']
    KY_HIEU = fields.Char(string='Ký hiệu (*)', help='Ký hiệu',required=True)
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    TY_LE_HUONG_LUONG = fields.Float(string='Tỷ lệ hưởng lương (%)', help='Tỷ lệ hưởng lương')
    LA_KY_HIEU_MAC_DINH = fields.Boolean(string='Là ký hiệu mặc định khi lập bảng chấm công', help='Là ký hiệu mặc định khi lập bảng chấm công')
    LA_KY_HIEU_NUA_NGAY = fields.Boolean(string='Là ký hiệu nửa ngày', help='Là ký hiệu nửa ngày')
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)
    name = fields.Char(string='Name', help='Name', related='KY_HIEU', store=True)

    _sql_constraints = [
        ('KY_HIEU_uniq', 'unique ("KY_HIEU")', 'Ký hiệu chấm công <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]
