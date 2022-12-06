# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError

class ASSET_KIEM_KE_TAI_SAN_CO_DINH_THAM_SO(models.Model):
    _name = 'asset.kiem.ke.tham.so'
    _description = ''
    _auto = False

    KIEM_KE_DEN_NGAY = fields.Date(string='Kiểm kê đến ngày', help='Kiểm kê đến ngày', default=fields.Datetime.now)
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(ASSET_KIEM_KE_TAI_SAN_CO_DINH_THAM_SO, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result

    def action_view_result(self):
        context = {}
        ngay_bat_dau_tai_chinh = self.env['ir.config_parameter'].get_param('he_thong.TU_NGAY_BAT_DAU_TAI_CHINH')
        ngay_tren_form = self.get_context('KIEM_KE_DEN_NGAY')
        ngay_thuc_hien_kiem_ke = datetime.strptime(ngay_tren_form, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y-%m-%d')
        if ngay_thuc_hien_kiem_ke < ngay_bat_dau_tai_chinh: #Mạnh sửa bug2355 : Thêm đoạn code này để check xem nếu ngày thực hiện kiểm kê nhỏ hơn ngày tài chính thì thông báo lỗi cho người dùng.
            raise ValidationError('Ngày kiểm kê phải lớn hơn hoặc bằng ngày bắt đầu hạch toán.')
        else:
            context = {
            'default_KIEM_KE_DEN_NGAY': self.get_context('KIEM_KE_DEN_NGAY'),
            }
        action = self.env.ref('asset.action_open_asset_kiem_ke_tham_so_form').read()[0]
        action['context'] = helper.Obj.merge(context, action.get('context'))
        # action['options'] = {'clear_breadcrumbs': True}
        return action
