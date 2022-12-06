# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.exceptions import ValidationError

class ASSET_KHAI_BAO_TAI_SAN_CO_DINH_DAU_KY(models.Model):
    _name = 'asset.khai.bao.dau.ky'
    _description = 'Khai báo tài sản cố định đầu kỳ'
    # _auto = False


    TEN = fields.Char(string='Tên', help='Tên')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    ASSET_KHAI_BAO_TAI_SAN_CO_DINH_DAU_KY_CHI_TIET_IDS = fields.One2many('asset.khai.bao.dau.ky.chi.tiet', 'KHAI_BAO_TAI_SAN_CO_DINH_DAU_KY_ID', string='Khai báo tài sản cố định đầu kỳ chi tiết')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    
    @api.model
    def create(self, values):


        ngay_vld = str(self.lay_ngay_dau_ky())
        if not  values.get('ASSET_KHAI_BAO_TAI_SAN_CO_DINH_DAU_KY_CHI_TIET_IDS'):
            raise ValidationError('Bạn phải khai báo tài sản cố định chi tiết')
        for line in values.get('ASSET_KHAI_BAO_TAI_SAN_CO_DINH_DAU_KY_CHI_TIET_IDS'):
            if not line[2].get('NGAY_GHI_TANG'):
                raise ValidationError('Ngày ghi tăng không được để trống')
            if line[2].get('NGAY_GHI_TANG') > ngay_vld:
                raise ValidationError('Ngày khai báo số dư đầu kỳ phải nhỏ hơn ngày sử dụng')
        result = super(ASSET_KHAI_BAO_TAI_SAN_CO_DINH_DAU_KY, self).create(values)
        self._create_ghi_tang(result)
        return result
    

    def _create_ghi_tang(self, doc):
        for doc in doc.ASSET_KHAI_BAO_TAI_SAN_CO_DINH_DAU_KY_CHI_TIET_IDS:
            line_ids = []
            ten_doi_tuong_phan_bo = ''
            id_doi_tuong_phan_bo = ''
            doi_tuong_phan_bo_reference = False

            if doc.DOI_TUONG_PHAN_BO_ID:
                ten_doi_tuong_phan_bo = doc.DOI_TUONG_PHAN_BO_ID._name
                id_doi_tuong_phan_bo = doc.DOI_TUONG_PHAN_BO_ID.id
                doi_tuong_phan_bo_reference = ten_doi_tuong_phan_bo +','+ str(id_doi_tuong_phan_bo)

            line_ids = [(0,0,{
                # 'TAI_SAN_CO_DINH_GHI_TANG_ID' : ghi_tang.id,
                'DOI_TUONG_PHAN_BO_ID': doi_tuong_phan_bo_reference,
                'TEN_DOI_TUONG_PHAN_BO': ten_doi_tuong_phan_bo,
                'TY_LE_PB': doc.TY_LE_PB,
                'TK_NO_ID': doc.TK_NO_ID.id if doc.TK_NO_ID.id else False,
                'KHOAN_MUC_CP_ID': doc.KHOAN_MUC_CP_ID.id if doc.KHOAN_MUC_CP_ID.id else False,
                'MA_THONG_KE_ID': doc.MA_THONG_KE_ID.id if doc.MA_THONG_KE_ID.id else False,
                
                })]

            if doc.MA_TAI_SAN == False:
                raise ValidationError('Mã tài sản không được bỏ trống')              
            elif doc.TEN_TAI_SAN == False:
                raise ValidationError('Tên tài sản không được bỏ trống')
            elif doc.LOAI_TAI_SAN_ID == False:
                raise ValidationError('Loại tài sản không được bỏ trống')
            elif doc.DON_VI_SU_DUNG_ID == False:
                raise ValidationError('Đơn vị sử dụng không được bỏ trống')
            elif doc.NGAY_GHI_TANG == False:
                raise ValidationError('Ngày ghi tăng không được bỏ trống')
            elif doc.NGAY_BAT_DAU_TINH_KH == False:
                raise ValidationError('Ngày bắt đầu tính khấu hao không được bỏ trống')
            elif doc.TK_KHAU_HAO_ID == False:
                raise ValidationError('Tài khoản tính khấu hao không được bỏ trống')
            elif doc.TK_NGUYEN_GIA_ID == False:
                raise ValidationError('Tài khoản nguyên giá không được bỏ trống')
            elif doc.DOI_TUONG_PHAN_BO_ID == False:
                raise ValidationError('Đối tượng phân bổ không được bỏ trống')

            self.env['asset.ghi.tang'].create({
                'MA_TAI_SAN': doc.MA_TAI_SAN,
                'TEN_TAI_SAN': doc.TEN_TAI_SAN,
                'LOAI_TAI_SAN_ID': doc.LOAI_TAI_SAN_ID.id,
                'DON_VI_SU_DUNG_ID': doc.DON_VI_SU_DUNG_ID.id,
                'NGAY_GHI_TANG': doc.NGAY_GHI_TANG,
                'NGAY_BAT_DAU_TINH_KH': doc.NGAY_BAT_DAU_TINH_KH,
                'THOI_GIAN_SU_DUNG': doc.DVT_THOI_GIAN_SD,
                'DVT_THOI_GIAN_SU_DUNG_CON_LAI' : doc.DVT_THOI_GIAN_SD,
                'SO_THOI_GIAN_SU_DUNG_NGUYEN_GOC': doc.THOI_GIAN_SU_DUNG,
                'LOAI_CHUNG_TU' : 615,
                'THOI_GIAN_SU_DUNG_CON_LAI_NGUYEN_GOC' : doc.THOI_GIAN_SD_CON_LAI,
                'SO_CT_GHI_TANG': 'OPN',
                'NGUYEN_GIA': doc.NGUYEN_GIA,
                'GIA_TRI_TINH_KHAU_HAO': doc.GIA_TRI_TINH_KHAU_HAO,
                'HAO_MON_LUY_KE': doc.HAO_MON_LUY_KE,
                'GIA_TRI_CON_LAI': doc.GIA_TRI_CON_LAI,
                'GIA_TRI_TINH_KHAU_HAO_THANG': doc.GIA_TRI_KH_THANG,
                'TK_KHAU_HAO_ID': doc.TK_KHAU_HAO_ID.id,
                'TK_NGUYEN_GIA_ID': doc.TK_NGUYEN_GIA_ID.id,
                'KHAI_BAO_DAU_KY' : True,
                'TY_LE_TINH_KHAU_HAO_THANG' : (100/doc.THOI_GIAN_SU_DUNG)/12 if doc.THOI_GIAN_SU_DUNG else False,
                'TY_LE_TINH_KHAU_HAO_NAM' : 100/doc.THOI_GIAN_SU_DUNG if doc.THOI_GIAN_SU_DUNG > 0 else False,
                'GIA_TRI_KHAU_HAO_NAM' : doc.GIA_TRI_KH_THANG*12,
                'ASSET_TAI_SAN_CO_DINH_THIET_LAP_PHAN_BO_IDS' : line_ids
                })

            