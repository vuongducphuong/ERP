# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_round

class SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HD_FORM(models.Model):
    _name = 'sale.ex.phan.bo.chiet.khau.theo.tong.gia.tri.hd.form'
    _auto = False
    _description = ''
    
    SO_TIEN = fields.Monetary(string='Số tiền', help='Số tiền', currency_field='currency_id')
    PHUONG_PHAP_PHAN_BO = fields.Selection([('THEO_SO_LUONG', 'Theo số lượng'), ('THEO_GIA_TRI', 'Theo giá trị'), ('TU_NHAP', 'Tự nhập'), ], string='Phương pháp phân bổ', help='Phương pháp phân bổ',required=True,default='THEO_SO_LUONG')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    IS_PHUONG_PHAP_PHAN_BO = fields.Boolean(default=True)

    SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS = fields.One2many('sale.ex.phan.bo.chiet.khau.theo.tong.gia.tri.hd.chi.tiet', 'PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_ID', string='phân bổ chiết khấu theo tổng giá trị hóa đơn chi tiết')
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền',store=False)
    HINH_THUC_CHIET_KHAU = fields.Selection([
        ('GHI_DE','Ghi đè số tiền chiết khấu'),
        ('CONG_THEM','Cộng thêm vào số tiền chiết khấu'),
        ], default='GHI_DE')

    @api.onchange('PHUONG_PHAP_PHAN_BO')
    def update_IS_PHUONG_PHAP_PHAN_BO(self):
        if self.PHUONG_PHAP_PHAN_BO =='TU_NHAP':
            self.IS_PHUONG_PHAP_PHAN_BO = False
        else:
            self.IS_PHUONG_PHAP_PHAN_BO = True

    @api.onchange('SO_TIEN','PHUONG_PHAP_PHAN_BO')
    def update_SO_TIEN(self):
        # env_phai_tra = self.env['sale.ex.phan.bo.chiet.khau.theo.tong.gia.tri.hd.chi.tiet']
        # self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS = []
        # ct_thanh_toans = [
        #     {
        #     "Mahang": 'AO_SM_NAM',
        #     "Tenhang" : 'Áo sơ mi nam',
        #     "Soluong" : 1,
        #     "Thanhtien": 200000,
        #     "Tylephanbo": 0,
        #     "Tienchietkhau":0
        # },
        # {
        #     "Mahang": 'AO_SM_NU',
        #     "Tenhang" : 'Áo sơ mi nữ',
        #     "Soluong" : 1,
        #     "Thanhtien": 100000,
        #     "Tylephanbo": 0,
        #     "Tienchietkhau":0
        # }]

        # for ct in ct_thanh_toans:
        #     new_line_phai_tra = env_phai_tra.new({
        #         'MA_HANG': ct.get('Mahang'),
        #         'TEN_HANG' : ct.get('Tenhang'),
        #         'SO_LUONG' : ct.get('Soluong'),
        #         'THANH_TIEN' : ct.get('Thanhtien'),
        #         'TY_LE_PHAN_BO' : ct.get('Tylephanbo'),
        #         'TIEN_CHIET_KHAU' : ct.get('Tienchietkhau'),
        #     })
        #     self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS += new_line_phai_tra


        if self.PHUONG_PHAP_PHAN_BO=='THEO_SO_LUONG':
            tong_so_luong=0
            for record  in self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS:
                tong_so_luong += record.SO_LUONG
            if tong_so_luong==0:
                raise ValidationError('Tổng số lượng sản phẩm đang bằng 0. Xin vui lòng kiểm tra lại.')
            i = 0
            tong_so_tien_chiet_khau_o_dong_khac = 0
            ty_le_phan_bo_o_dong_khac = 0
            for record in self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS:
                # i = i+1
                i += 1
                if(i != len(self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS)):                        
                    
                    # tien_chiet_khau = float_round((self.SO_TIEN / tong_so_luong) * record. SO_LUONG,2)
                    tien_chiet_khau = self.currency_id.round((self.SO_TIEN / tong_so_luong) * record. SO_LUONG)
                    record.TIEN_CHIET_KHAU = tien_chiet_khau
                    tong_so_tien_chiet_khau_o_dong_khac += tien_chiet_khau
                    ty_le_phan_bo = (record.SO_LUONG / tong_so_luong)*100
                    record.TY_LE_PHAN_BO = ty_le_phan_bo
                    ty_le_phan_bo_o_dong_khac += ty_le_phan_bo
            
            if (len(self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS) > 0):
                tien_chiet_khau_dong_cuoi_cung = self.SO_TIEN - tong_so_tien_chiet_khau_o_dong_khac
                self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS[len(self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS) - 1].TIEN_CHIET_KHAU = tien_chiet_khau_dong_cuoi_cung
                # if record.THANH_TIEN==0:
                #     raise ValidationError('Thành tiền sản phẩm đang bằng 0. Xin vui lòng kiểm tra lại.')
                # self.CHI_TIET_IDS[len(self.CHI_TIET_IDS) - 1].TY_LE_CK = (tien_chiet_khau_dong_cuoi_cung / record.THANH_TIEN ) * 100
                ty_le_phan_bo_dong_cuoi_cung = 100 - ty_le_phan_bo_o_dong_khac
                self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS[len(self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS) - 1].TY_LE_PHAN_BO = ty_le_phan_bo_dong_cuoi_cung

        elif self.PHUONG_PHAP_PHAN_BO=='THEO_GIA_TRI':
            tong_thanh_tien=0
            for record  in self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS:
                tong_thanh_tien += record.THANH_TIEN
            if tong_thanh_tien==0:
                raise ValidationError('Tổng thành tiền sản phẩm đang bằng 0. Xin vui lòng kiểm tra lại.')
            i = 0
            tong_so_tien_chiet_khau_o_dong_khac = 0
            ty_le_phan_bo_o_dong_khac = 0
            for record in self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS:
                # i = i+1
                i += 1
                if(i != len(self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS)):                        
                    
                    # tien_chiet_khau = float_round((self.SO_TIEN / tong_thanh_tien) * record.THANH_TIEN,2) 
                    tien_chiet_khau = self.currency_id.round((self.SO_TIEN / tong_thanh_tien) * record.THANH_TIEN)
                    record.TIEN_CHIET_KHAU = tien_chiet_khau
                    tong_so_tien_chiet_khau_o_dong_khac += tien_chiet_khau
                    ty_le_phan_bo = (record.THANH_TIEN / tong_thanh_tien)*100
                    record.TY_LE_PHAN_BO = ty_le_phan_bo
                    ty_le_phan_bo_o_dong_khac += ty_le_phan_bo
            
            if (len(self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS) > 0):
                tien_chiet_khau_dong_cuoi_cung = self.SO_TIEN - tong_so_tien_chiet_khau_o_dong_khac
                self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS[len(self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS) - 1].TIEN_CHIET_KHAU = tien_chiet_khau_dong_cuoi_cung
                # if record.THANH_TIEN==0:
                #     raise ValidationError('Thành tiền sản phẩm đang bằng 0. Xin vui lòng kiểm tra lại.')
                # self.CHI_TIET_IDS[len(self.CHI_TIET_IDS) - 1].TY_LE_CK = (tien_chiet_khau_dong_cuoi_cung / record.THANH_TIEN ) * 100
                ty_le_phan_bo_dong_cuoi_cung = 100 - ty_le_phan_bo_o_dong_khac
                self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS[len(self.SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS) - 1].TY_LE_PHAN_BO = ty_le_phan_bo_dong_cuoi_cung    
            


            
            



    

    