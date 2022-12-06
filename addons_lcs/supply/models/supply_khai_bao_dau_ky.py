# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError

class SUPPLY_KHAI_BAO_CCDC_DAU_KY(models.Model):
    _name = 'supply.khai.bao.dau.ky'
    _description = ''
    # _auto = False
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    SUPPLY_KHAI_BAO_CCDC_DAU_KY_CHI_TIET_IDS = fields.One2many('supply.khai.bao.dau.ky.chi.tiet', 'CCDC_DAU_KY_ID', string='Khai báo CCDC đầu kỳ')

    
    @api.model
    def create(self, values):
        ngay_vld = str(self.lay_ngay_dau_ky())
        if not  values.get('SUPPLY_KHAI_BAO_CCDC_DAU_KY_CHI_TIET_IDS'):
            raise ValidationError('Bạn phải khai báo Công cụ dụng chi tiết')
        for line in values.get('SUPPLY_KHAI_BAO_CCDC_DAU_KY_CHI_TIET_IDS'):
            if not line[2].get('MA_CCDC'):
                raise ValidationError('Mã công cụ dụng cụ không được bỏ trống')
            if not line[2].get('TEN_CCDC'):
                raise ValidationError('Tên công cụ dụng cụ không được bỏ trống')
            if not line[2].get('NGAY_GHI_TANG'):
                raise ValidationError('Ngày ghi tăng không được để trống')
            if line[2].get('NGAY_GHI_TANG') > ngay_vld:
                raise ValidationError('Ngày khai báo số dư đầu kỳ phải nhỏ hơn ngày sử dụng')
        result = super(SUPPLY_KHAI_BAO_CCDC_DAU_KY, self).create(values)
        self._create_ghi_tang(result)
        return result

    


    def _create_ghi_tang(self, doc):
        for line in doc.SUPPLY_KHAI_BAO_CCDC_DAU_KY_CHI_TIET_IDS:
            ten_doi_tuong_phan_bo = ''
            id_doi_tuong_phan_bo = ''
            doi_tuong_phan_bo_reference = False
            
            line_dtpb_ids = []            
            for dvsd in line.SUPPLY_KHAI_BAO_CCDC_DAU_KY_THIET_LAP_PB_IDS:
                if dvsd.DOI_TUONG_PHAN_BO_ID:
                    ten_doi_tuong_phan_bo = dvsd.DOI_TUONG_PHAN_BO_ID._name
                    id_doi_tuong_phan_bo = dvsd.DOI_TUONG_PHAN_BO_ID.id
                    doi_tuong_phan_bo_reference = ten_doi_tuong_phan_bo +','+ str(id_doi_tuong_phan_bo)

                line_dtpb_ids = [(0,0,{
                    'DOI_TUONG_PHAN_BO_ID': doi_tuong_phan_bo_reference,
                    'TEN_DOI_TUONG_PHAN_BO': dvsd.DOI_TUONG_PHAN_BO_ID.name,
                    'TY_LE_PB': dvsd.TY_LE_PB,
                    'TK_NO_ID': dvsd.TK_NO_ID.id,
                    'KHOAN_MUC_CP_ID': dvsd.KHOAN_MUC_CP_ID.id if dvsd.KHOAN_MUC_CP_ID.id else False,
                    })]

            line_dvsd_ids = []
            for dtpb in line.SUPPLY_KHAI_BAO_CCDC_DAU_KY_DON_VI_SD_IDS:
                line_dvsd_ids = [(0,0,{
                    'MA_DON_VI_ID': dtpb.MA_DON_VI_ID.id if dtpb.MA_DON_VI_ID.id else False,
                    'TEN_DON_VI': dtpb.TEN_DON_VI,
                    'SO_LUONG': dtpb.SO_LUONG,
                    
                    })]

            self.env['supply.ghi.tang'].create({
                'SO_CT_GHI_TANG' : 'OPN',
                'MA_CCDC': line.MA_CCDC,
                'TEN_CCDC': line.TEN_CCDC,
                'LOAI_CCDC_ID': line.LOAI_CCDC_ID.id if line.LOAI_CCDC_ID.id else False,
                'NHOM_CCDC': line.NHOM_CCDC,
                'LY_DO_GHI_TANG': line.LY_DO_GHI_TANG,
                'DON_VI_TINH': line.DON_VI_TINH,
                'SO_LUONG': line.SO_LUONG,
                'NGAY_GHI_TANG' : line.NGAY_GHI_TANG,
                'SO_KY_PHAN_BO' : line.TONG_SO_KY_PB,
                'SO_KY_PB_CON_LAI': line.SO_KY_PB_CON_LAI,
                'THANH_TIEN': line.GIA_TRI_CCDC,
                'DON_GIA' : line.GIA_TRI_CCDC/line.SO_LUONG,
                'GIA_TRI_DA_PHAN_BO': line.GIA_TRI_DA_PHAN_BO,
                'GIA_TRI_CON_LAI': line.GIA_TRI_CON_LAI,
                'SO_TIEN_PHAN_BO_HANG_KY': line.SO_TIEN_PHAN_BO_HANG_KY,
                'TK_CHO_PHAN_BO_ID': line.TK_CHO_PHAN_BO_ID.id if line.TK_CHO_PHAN_BO_ID.id else False,
                'KHAI_BAO_DAU_KY' : True,
                'LOAI_CHUNG_TU' : 457,
                'SUPPLY_GHI_TANG_DON_VI_SU_DUNG_IDS' : line_dvsd_ids,
                'SUPPLY_GHI_TANG_THIET_LAP_PHAN_BO_IDS' : line_dtpb_ids,
                })
            
           
    