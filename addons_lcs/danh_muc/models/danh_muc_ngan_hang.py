# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class DANH_MUC_NGAN_HANG(models.Model):
    _name = 'danh.muc.ngan.hang'
    _description = 'Ngân hàng'
    _inherit = ['mail.thread']
    _order="TEN_VIET_TAT, TEN_DAY_DU, DIA_CHI_HOI_SO_CHINH, DIEN_GIAI"
    
    TEN_VIET_TAT = fields.Char(string='Tên viết tắt', help='Tên viết tắt')
    TEN_DAY_DU = fields.Char(string='Tên đầy đủ', help='Tên đầy đủ')
    TEN_TIENG_ANH = fields.Char(string='Tên tiếng anh', help='Tên tiếng anh')
    DIA_CHI_HOI_SO_CHINH = fields.Char(string='Địa chỉ hội sở chính', help='Địa chỉ hội sở chính')
    DIEN_GIAI = fields.Char(string='Diễn giải', help='Diễn giải')
    # image  = fields.Char(string='Chọn logo', help='Chọn logo')
    name = fields.Char(string='Name', help='Name',related='TEN_DAY_DU',store=True)
    active = fields.Boolean(string='Theo dõi', help='Theo dõi', default=True)

    image = fields.Binary("Image", attachment=True,
       help="Chọn logo",)

    _sql_constraints = [
        ('TEN_VIET_TAT_uniq', 'unique ("TEN_VIET_TAT")', 'Tên viết tắt <<>> đã tồn tại. Xin vui lòng kiểm tra lại!'),
    ]


    @api.model
    def create(self, vals): 
        if (vals.get('TEN_VIET_TAT')):
            vals['name'] = vals.get('TEN_VIET_TAT')
        return super(DANH_MUC_NGAN_HANG, self).create(vals)