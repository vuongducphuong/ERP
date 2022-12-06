# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper

class STOCK_EX_LENH_SAN_XUAT_LAP_PN_FORM(models.Model):
    _name = 'stock.ex.lenh.san.xuat.lap.pn.form'
    _description = ''
    _auto = False

    LAP_PN = fields.Char(string='Lập pn', help='Lập pn')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    #@api.model
    #def default_get(self, fields_list):
    #   result = super(STOCK_EX_LENH_SAN_XUAT_LAP_PN_FORM, self).default_get(fields_list)
    #   result['FIELD_IDS'] = self.env['model.name'].search([]).ids
    #   return result
    STOCK_EX_LENH_SAN_XUAT_LAP_PN_CHI_TIET_FORM_IDS = fields.One2many('stock.ex.lenh.san.xuat.lap.pn.chi.tiet.form', 'LAP_PN_CHI_TIET_ID', string='Lệnh sản xuất lập PN chi tiết form')
    LENH_SX_PN_PX = fields.Selection([
        ('PHIEU_NHAP', 'Phiếu nhập'), 
        ('PHIEU_XUAT', 'Phiếu xuất'), 
        ], string='Lệnh sản xuất phiếu nhập, phiếu xuất')

    LSX_ID = fields.Many2one('stock.ex.lenh.san.xuat',string='Lệnh sản xuất', help='LSX')
    

    @api.model
    def default_get(self,default_fields):
        res = super(STOCK_EX_LENH_SAN_XUAT_LAP_PN_FORM, self).default_get(default_fields)
        id_lenh_san_xuat = self.get_context('default_ID_LENH_SAN_XUAT')

        #nếu id_lenh_san_xuất tồn tại
            #giá trị chọn thành phẩm = giá trị detail form lsx
        if id_lenh_san_xuat:
            arr_lenh_san_xuat_nhap_xuat= []
            # lsx_mt_pn = self.env['stock.ex.lenh.san.xuat'].search([('id','=',id_lenh_san_xuat)])
            lenh_san_xuat_detail = self.env['stock.ex.lenh.san.xuat.chi.tiet.thanh.pham'].search([('LENH_SAN_XUAT_CHI_TIET_THANH_PHAM_ID','=',id_lenh_san_xuat)])
            res['STOCK_EX_LENH_SAN_XUAT_LAP_PN_CHI_TIET_FORM_IDS'] =[]
            for lsx_detail in lenh_san_xuat_detail:
                arr_lenh_san_xuat_nhap_xuat +=[(0,0,{
                        'MA_THANH_PHAM_ID':lsx_detail.MA_HANG_ID.id,
                        'TEN_THANH_PHAM':lsx_detail.TEN_THANH_PHAM,
                        'SO_LUONG':lsx_detail.SO_LUONG,
                        'SO_LUONG_SAN_XUAT':lsx_detail.SO_LUONG,

                        # 'LENH_SAN_XUAT_ID'  :lsx_mt_pn.id,
                        'DVT_ID':lsx_detail.DVT_ID.id,
                        'LENH_SAN_XUAT_THANH_PHAM_ID' : lsx_detail.id,
                        # 'KHO_ID'  :lsx_detail.MA_HANG_ID.KHO_NGAM_DINH_ID.id,
                        # 'TK_NO_ID'  :lsx_detail.MA_HANG_ID.TAI_KHOAN_KHO_ID.id,
                        # 'DOI_TUONG_THCP_ID'  :lsx_detail.DOI_TUONG_THCP_ID.id,
                        # 'MA_THONG_KE_ID'  :lsx_detail.MA_THONG_KE_ID.id,
                        })]
            res['STOCK_EX_LENH_SAN_XUAT_LAP_PN_CHI_TIET_FORM_IDS'] += arr_lenh_san_xuat_nhap_xuat



        loai_nut = self.get_context('default_LENH_SX_PN_PX')
        #b1: lấy giá trị từ contex sang
        #b2: chuyển đổi giá trị vào model
        res['LENH_SX_PN_PX']=loai_nut
        res['LSX_ID']=id_lenh_san_xuat
        return res

    # def action_view_result(self):
    #     action = self.env.ref('stock_ex.action_open_stock_ex_lenh_san_xuat_lap_pn_form_form').read()[0]
    #     # action['options'] = {'clear_breadcrumbs': True}
    #     return action
    # @api.multi
    # def btn_phieu_nhap_xuat_kho(self):
    #     id_lsx_phieu_nhap_xuat_kho = self.id
    #     #neu loai nut== phieu nhap
    #         #bật form phiếu nhập
    #     #nguoc lai
    #         #bật form phiếu xuất
    #     if self.get_context('LENH_SX_PN_PX') == 'PHIEU_NHAP':
    #         action = self.env.ref('stock_ex.action_open_stock_ex_nk_form').read()[0]
    #     else:
    #         action = self.env.ref('stock_ex.action_open_stock_ex_xk_form').read()[0]
    #     context ={
    #         'default_ID_LSX_LAP_PHIEU_NX': id_lsx_phieu_nhap_xuat_kho,
    #      }
    #     action['context'] = helper.Obj.merge(context, action.get('context'))
    #     return action


   
