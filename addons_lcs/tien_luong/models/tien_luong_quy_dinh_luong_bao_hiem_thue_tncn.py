# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision


class TIEN_LUONG_QUY_DINH_LUONG_BAO_HIEM_THUE_TNCN(models.Model):
    _name = 'tien.luong.quy.dinh.luong.bao.hiem.thue.tncn'
    _description = 'Quy định lương, bảo hiểm, thuế TNCN'

    MUC_LUONG_TOI_THIEU = fields.Float(string='Mức lương tối thiểu', help='Mức lương tối thiểu')
    MUC_LUONG_TOI_DA_DONG_BHXH = fields.Float(string='Mức lương tối đa đóng bhxh', help='Mức lương tối đa đóng bhxh')
    MUC_LUONG_TOI_DA_DONG_BHTN = fields.Float(string='Mức lương tối đa đóng bhtn', help='Mức lương tối đa đóng bhtn')
    SO_NGAY_TINH_CONG_TRONG_THANG = fields.Float(string='Số ngày tính công trong tháng', help='Số ngày tính công trong tháng')
    SO_GIO_TINH_CONG_TRONG_NGAY = fields.Float(string='Số giờ tính công trong ngày', help='Số giờ tính công trong ngày')
    LAM_THEM_NGAY_THUONG_BAN_NGAY = fields.Float(string='Làm thêm ngày thường ban ngày', help='Làm thêm ngày thường ban ngày')
    THU_7_CHU_NHAT_BAN_NGAY = fields.Float(string='Thứ 7 chủ nhật ban ngày', help='Thứ 7 chủ nhật ban ngày')
    NGAY_LE_TET_BAN_NGAY = fields.Float(string='Ngày lễ tết ban ngày', help='Ngày lễ tết ban ngày')
    LAM_THEM_NGAY_THUONG_BAN_DEM = fields.Float(string='Làm thêm ngày thường ban đêm', help='Làm thêm ngày thường ban đêm')
    THU_7_CHU_NHAT_BAN_DEM = fields.Float(string='Thứ 7 chủ nhật ban đêm', help='Thứ 7 chủ nhật ban đêm')
    NGAY_LE_TET_BAN_DEM = fields.Float(string='Ngày lễ tết ban đêm', help='Ngày lễ tết ban đêm')
    BAO_HIEM_XA_HOI_CONG_TY_DONG = fields.Float(string='Bảo hiểm xã hội công ty đóng', help='Bảo hiểm xã hội công ty đóng')
    BAO_HIEM_Y_TE_CONG_TY_DONG = fields.Float(string='Bảo hiểm y tế công ty đóng', help='Bảo hiểm y tế công ty đóng')
    BAO_HIEM_THAT_NGHIEP_CONG_TY_DONG = fields.Float(string='Bảo hiểm thất nghiệp công ty đóng', help='Bảo hiểm thất nghiệp công ty đóng')
    KINH_PHI_CONG_DOAN_CONG_TY_DONG = fields.Float(string='Kinh phí công đoàn công ty đóng', help='Kinh phí công đoàn công ty đóng')
    BAO_HIEM_XA_HOI_NV_DONG = fields.Float(string='Bảo hiểm xã hội nv đóng', help='Bảo hiểm xã hội nv đóng')
    BAO_HIEM_Y_TE_NV_DONG = fields.Float(string='Bảo hiểm y tế nv đóng', help='Bảo hiểm y tế nv đóng')
    BAO_HIEM_THAT_NGHIEP_NV_DONG = fields.Float(string='Bảo hiểm thất nghiệp nv đóng', help='Bảo hiểm thất nghiệp nv đóng')
    KINH_PHI_CONG_DOAN_NV_DONG = fields.Float(string='Kinh phí công đoàn nv đóng', help='Kinh phí công đoàn nv đóng')
    THUE_GIAM_TRU_BAN_THAN = fields.Float(string='Thuế giảm trừ bản thân', help='Thuế giảm trừ bản thân')
    THUE_GIAM_TRU_NGUOI_PHU_THUOC = fields.Float(string='Thuế giảm trừ người phụ thuộc', help='Thuế giảm trừ người phụ thuộc')

    #FIELD_IDS = fields.One2many('model.name')
    # Kiểm tra trong databse có dữ liệu chưa
    # load dữ liệu đó lên view


    @api.model
    def default_get(self, fields_list):
        # Kiểm tra trong db có dữ liệu chưa
        result = super(TIEN_LUONG_QUY_DINH_LUONG_BAO_HIEM_THUE_TNCN, self).default_get(fields_list)
        data= self.env['tien.luong.quy.dinh.luong.bao.hiem.thue.tncn'].search([],limit=1)
        # load dữ liệu lên view
        if data:
            result['MUC_LUONG_TOI_THIEU'] = data.MUC_LUONG_TOI_THIEU
            result['MUC_LUONG_TOI_DA_DONG_BHXH'] = data.MUC_LUONG_TOI_DA_DONG_BHXH
            result['MUC_LUONG_TOI_DA_DONG_BHTN'] = data.MUC_LUONG_TOI_DA_DONG_BHTN
            result['SO_NGAY_TINH_CONG_TRONG_THANG'] = data.SO_NGAY_TINH_CONG_TRONG_THANG
            result['SO_GIO_TINH_CONG_TRONG_NGAY'] = data.SO_GIO_TINH_CONG_TRONG_NGAY
            result['LAM_THEM_NGAY_THUONG_BAN_NGAY'] = data.LAM_THEM_NGAY_THUONG_BAN_NGAY
            result['THU_7_CHU_NHAT_BAN_NGAY'] = data.THU_7_CHU_NHAT_BAN_NGAY
            result['NGAY_LE_TET_BAN_NGAY'] = data.NGAY_LE_TET_BAN_NGAY
            result['LAM_THEM_NGAY_THUONG_BAN_DEM'] = data.LAM_THEM_NGAY_THUONG_BAN_DEM
            result['THU_7_CHU_NHAT_BAN_DEM'] = data.THU_7_CHU_NHAT_BAN_DEM
            result['NGAY_LE_TET_BAN_DEM'] = data.NGAY_LE_TET_BAN_DEM
            result['BAO_HIEM_XA_HOI_CONG_TY_DONG'] = data.BAO_HIEM_XA_HOI_CONG_TY_DONG
            result['BAO_HIEM_Y_TE_CONG_TY_DONG'] = data.BAO_HIEM_Y_TE_CONG_TY_DONG
            result['BAO_HIEM_THAT_NGHIEP_CONG_TY_DONG'] = data.BAO_HIEM_THAT_NGHIEP_CONG_TY_DONG
            result['KINH_PHI_CONG_DOAN_CONG_TY_DONG'] = data.KINH_PHI_CONG_DOAN_CONG_TY_DONG
            result['BAO_HIEM_XA_HOI_NV_DONG'] = data.BAO_HIEM_XA_HOI_NV_DONG
            result['BAO_HIEM_Y_TE_NV_DONG'] = data.BAO_HIEM_Y_TE_NV_DONG
            result['BAO_HIEM_THAT_NGHIEP_NV_DONG'] = data.BAO_HIEM_THAT_NGHIEP_NV_DONG
            result['KINH_PHI_CONG_DOAN_NV_DONG'] = data.KINH_PHI_CONG_DOAN_NV_DONG
            result['THUE_GIAM_TRU_BAN_THAN'] = data.THUE_GIAM_TRU_BAN_THAN
            result['THUE_GIAM_TRU_NGUOI_PHU_THUOC'] = data.THUE_GIAM_TRU_NGUOI_PHU_THUOC
        return result

    @api.model
    def create(self, values):
        data= self.env['tien.luong.quy.dinh.luong.bao.hiem.thue.tncn'].search([],limit=1)
        if data:
            data.write(values)
            return data
        else:
            return super(TIEN_LUONG_QUY_DINH_LUONG_BAO_HIEM_THUE_TNCN, self).create(values)

    
