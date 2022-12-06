# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_LUONG_HACH_TOAN_CHI_PHI_LUONG_FORM_THAM_SO(models.Model):
    _name = 'tien.luong.hach.toan.chi.phi.luong.form.tham.so'
    _description = ''
    _auto = False

    BANG_LUONG = fields.Many2one('tien.luong.bang.luong',string='Bảng lương', help='Bảng lương')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    
    def kiem_tra_bang_luong_ton_tai (self, args):
        bang_luong_id = args.get('bang_luong_id')
        if bang_luong_id:
            bang_luong = self.env['tien.luong.hach.toan.chi.phi.luong'].search([('BANG_LUONG_ID', '=', bang_luong_id)],limit=1)
            if bang_luong:
                return True
        return False

