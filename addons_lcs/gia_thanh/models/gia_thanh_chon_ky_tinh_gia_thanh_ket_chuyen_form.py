# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_CHON_KY_TINH_GIA_THANH_KET_CHUYEN_FORM(models.Model):
    _name = 'gia.thanh.chon.ky.tinh.gia.thanh.ket.chuyen.form'
    _description = ''
    _auto = False

    KY_TINH_GIA_THANH_ID = fields.Many2one('gia.thanh.ky.tinh.gia.thanh', string='Kỳ tính giá thành', help='Kỳ tính giá thành', required=True)
    DEN_NGAY = fields.Date(string='Đến ngày' , help = 'Đến ngày' ,related='KY_TINH_GIA_THANH_ID.DEN_NGAY')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    @api.model
    def default_get(self, fields_list):
      result = super(GIA_THANH_CHON_KY_TINH_GIA_THANH_KET_CHUYEN_FORM, self).default_get(fields_list)
      ky_tinh_gia_thanh = self.env['gia.thanh.ky.tinh.gia.thanh'].search([],limit=1)
      if ky_tinh_gia_thanh:
        result['KY_TINH_GIA_THANH_ID'] = ky_tinh_gia_thanh.id
      return result

    def kiem_tra_ket_chuyen_chi_phi (self, args):
        ky_tinh_gia_thanh_id = args.get('ky_tinh_gia_thanh_id')
        id_ket_chuyen_chi_phi = 0
        if ky_tinh_gia_thanh_id:
            ket_chuyen_chi_phi = self.env['gia.thanh.ket.chuyen.chi.phi'].search([('KY_TINH_GIA_THANH_ID', '=', ky_tinh_gia_thanh_id)],limit=1)
            if ket_chuyen_chi_phi:
                id_ket_chuyen_chi_phi = ket_chuyen_chi_phi.id
        return id_ket_chuyen_chi_phi
            