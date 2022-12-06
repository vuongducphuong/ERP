# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError

class ASSET_CHON_KY_TINH_KHAU_HAO(models.Model):
    _name = 'asset.chon.ky.tinh.khau.hao'
    _description = ''
    _auto = False

    THANG = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ], string='Tháng', help='Tháng')
    NAM = fields.Integer(string='Năm', help='Năm')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    @api.model
    def default_get(self, fields_list):
        result = super(ASSET_CHON_KY_TINH_KHAU_HAO, self).default_get(fields_list)
        thang = datetime.now().month
        result['NAM'] = datetime.now().year
        result['THANG'] = str(thang)
        return result

    def action_view_result(self):
        nam_tai_chinh = int(self.env['ir.config_parameter'].get_param('he_thong.NAM_TAI_CHINH_BAT_DAU'))
        nam_thuc_hien_tinh_khau_hao = self.get_context('NAM')
        if nam_thuc_hien_tinh_khau_hao < nam_tai_chinh: #Mạnh sửa bug2355 : Thêm đoạn code này để check xem nếu năm thực hiện tính khấu hao nhỏ hơn năm tài chính thì thông báo lỗi cho người dùng.
            raise ValidationError('Chương trình không cho phép nhập Năm nhỏ hơn năm bắt đầu hạch toán của chương trình. Bạn vui lòng kiểm tra lại.')
        else:
            thang_da_phan_bo = self.env['asset.tinh.khau.hao'].search([])
            for pb in thang_da_phan_bo:
                if self.get_context('NAM') == pb.NAM:
                    if self.get_context('THANG') == str(pb.THANG):
                        raise ValidationError('Bảng tính khấu hao tài sản cố định tháng ' +str(self.get_context('THANG')) +' năm ' +str(self.get_context('NAM')) + ' đã tồn tại')
        action = self.env.ref('asset.action_open_asset_chon_ky_tinh_khau_hao_form').read()[0]
       


        context = {

            'default_THANG': self.get_context('THANG'),
            'default_NAM': self.get_context('NAM'),
            
            }

        action['context'] = helper.Obj.merge(context, action.get('context'))
        # action['options'] = {'clear_breadcrumbs': True}
        return action