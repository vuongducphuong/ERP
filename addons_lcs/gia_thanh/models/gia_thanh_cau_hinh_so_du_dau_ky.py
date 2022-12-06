# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_CAU_HINH_SO_DU_DAU_KY(models.Model):
    _name = 'gia.thanh.cau.hinh.so.du.dau.ky'
    _description = ''
    _inherit = ['mail.thread']
    CHI_TIET_THEO_DTTHCP = fields.Boolean(string='Chi tiết theo đối tượng tập hợp chi phí', help='Chi tiết theo đối tượng tập hợp chi phí', default=False)
    CHI_TIET_THEO_CONG_TRINH = fields.Boolean(string='Chi tiết theo công trình', help='Chi tiết theo công trình', default=False)
    CHI_TIET_THEO_DON_HANG = fields.Boolean(string='Chi tiết theo đơn hàng', help='Chi tiết theo đơn hàng', default=False)
    CHI_TIET_THEO_HOP_DONG = fields.Boolean(string='Chi tiết theo hợp đồng', help='Chi tiết theo hợp đồng', default=False)