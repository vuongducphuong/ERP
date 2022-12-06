# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper

class THUE_NOP_THUE_FORM(models.Model):
    _name = 'thue.nop.thue.form'
    _description = ''
    _auto = False

    LOAI_THUE = fields.Selection([('THUE_HANG_NHAP_KHAU', 'Thuế hàng nhập khẩu'), ('THUE_KHAC', ' Thuế khác'), ], string='Loại thuế', help='Loại thuế', default='THUE_KHAC',required=True)
    NGAY_NOP_THUE = fields.Date(string='Ngày nộp thuế', help='Ngày nộp thuế',default=fields.Datetime.now)
    PHUONG_THUC_THANH_TOAN = fields.Selection([('TIEN_GUI', 'Tiền gửi'), ('TIEN_MAT', ' Tiền mặt'), ], string='Phương thức thanh toán', help='Phương thức thanh toán' , default='TIEN_MAT')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    
    THUE_NOP_THUE_CHI_TIET_IDS = fields.One2many('thue.nop.thue.chi.tiet', 'CHI_TIET_ID', string='Nộp thuế chi tiết')

    def action_view_result(self):
        if self.get_context('PHUONG_THUC_THANH_TOAN') == 'TIEN_GUI':
            context = {
            'default_LOAI_CHUNG_TU': 1512,
            'default_TYPE_NH_Q': 'NGAN_HANG',
            'default_LOAI_PHIEU': 'PHIEU_CHI',
            }
            action = self.env.ref('account_ex.action_account_ex_ngan_hang_phieu_chi_tien').read()[0]
            action['context'] = helper.Obj.merge(context, action.get('context'))
            # action['options'] = {'clear_breadcrumbs': True}
        elif self.get_context('PHUONG_THUC_THANH_TOAN') == 'TIEN_MAT':
            context = {
            'default_LOAI_CHUNG_TU': 1022,
            'default_TYPE_NH_Q': 'QUY',
            'default_LOAI_PHIEU': 'PHIEU_CHI',
            }
            action = self.env.ref('account_ex.action_account_ex_quy_phieu_chi_tien').read()[0]
            action['context'] = helper.Obj.merge(context, action.get('context'))
            # action['options'] = {'clear_breadcrumbs': True}
        return action