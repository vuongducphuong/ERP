# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_CAU_HINH_LAI_LO_CHO_CT_HD_DH(models.Model):
    _name = 'tien.ich.cau.hinh.lai.lo.cho.ct.hd.dh'
    _description = ''
    _inherit = ['mail.thread']
    MA_BAO_CAO = fields.Char(string='Mã báo cáo ', help='Mã báo cáo ')
    MA_THU_TU = fields.Float(string='Mã thứ tự', help='Mã thứ tự')
    MA_CHI_TIEU_DINH_DANH = fields.Char(string='Mã chi tiêu định danh', help='Mã chi tiêu định danh')
    MA_CHI_TIEU = fields.Char(string='Mã chỉ tiêu', help='Mã chỉ tiêu')
    TEN_CHI_TIEU = fields.Char(string='Tên chỉ tiêu', help='Tên chỉ tiêu')
    CHI_TIEU_CHA_ID = fields.Many2one('tien.ich.cau.hinh.lai.lo.cho.ct.hd.dh', string='Chỉ tiêu cha', help='Chỉ tiêu cha')
    LA_CHI_TIEU_CHA = fields.Boolean(string='Là chỉ tiêu cha', help='Là chỉ tiêu cha')
    BAC = fields.Integer(string='Bậc', help='Bậc')
    IN_DAM = fields.Boolean(string='In đậm', help='In đậm')
    IN_NGHIENG = fields.Boolean(string='In nghiêng', help='In nghiêng')
    CONG_THUC = fields.Char(string='Công thức', help='Công thức')
    sequence = fields.Float()