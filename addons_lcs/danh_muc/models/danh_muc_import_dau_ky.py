# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ImportDauKy(models.TransientModel):
    _name = "import.dau.ky"
    _description = "Import số dư đầu kỳ"

    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh')
    state = fields.Selection([
        ('bat_dau', 'Bắt đầu'),
        ('chon_tep', 'Chọn tệp dữ liệu'),
        ('kiem_tra', 'Kiểm tra dữ liệu'),
        ('nhap_khau', 'Nhập khẩu dữ liệu'),
        ], string='Status', readonly=True, copy=False, index=True, default='bat_dau')
        
    def action_next(self):
        # self.ensure_one()
        state = self.state
        if (self.state == 'bat_dau'):
            state = 'chon_tep'
        elif (self.state == 'chon_tep'):
            state = 'kiem_tra'
        elif (self.state == 'kiem_tra'):
            state = 'nhap_khau'
        self.state = state
        self.write({
            'state': state
        })
        # return {
        #     "type": "ir.actions.do_nothing",
        # }
        
        # return {
        #     'name': 'Halo',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'view_id': False,
        #     'res_model': 'import.dau.ky',
        #     'domain': [],
        #     'context': dict(self._context, active_ids=self.ids),
        #     'type': 'ir.actions.act_window',
        #     'target': 'new',
        #     'res_id': self.id,
        # }

    def action_back(self):
        state = self.state
        if (self.state == 'chon_tep'):
            state = 'bat_dau'
        elif (self.state == 'kiem_tra'):
            state = 'chon_tep'
        elif (self.state == 'nhap_khau'):
            state = 'kiem_tra'
        self.write({
            'state': state
        })
        # return True