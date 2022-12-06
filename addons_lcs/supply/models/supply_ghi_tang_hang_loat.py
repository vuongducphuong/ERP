# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
import json
from odoo.exceptions import ValidationError

class SUPPLY_GHI_TANG_CONG_CU_DUNG_CU_HANG_LOAT(models.Model):
    _name = 'supply.ghi.tang.cong.cu.dung.cu.hang.loat'
    _description = ''
    _inherit = ['mail.thread']
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    CHUNG_TU_JSON = fields.Text()
    CHUNG_TU_GHI_GIAM_JSON = fields.Text()

    SUPPLY_GHI_TANG_HANG_LOAT_CHI_TIET_IDS = fields.One2many('supply.ghi.tang.hang.loat.chi.tiet', 'GHI_TANG_HANG_LOAT_ID', string='Ghi tăng hàng loạt chi tiết')

    
    @api.model
    def create(self, values):
        result = super(SUPPLY_GHI_TANG_CONG_CU_DUNG_CU_HANG_LOAT, self).create(values)
        self._create_ghi_tang(result)
        return result


    @api.onchange('CHUNG_TU_JSON')
    def _onchange_CHUNG_TU_JSON(self):
        if self.CHUNG_TU_JSON:
            chon_chung_tu = json.loads(self.CHUNG_TU_JSON).get('ACCOUNT_EX_CHON_CHUNG_TU_XUAT_KHO_MUA_HANG_CHI_TIET_IDS', [])
            tk_cho_pb = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '242')], limit = 1).id
            self.SUPPLY_GHI_TANG_HANG_LOAT_CHI_TIET_IDS = []
            env = self.env['supply.ghi.tang.hang.loat.chi.tiet']
            for line in chon_chung_tu:
                hang = self.env['danh.muc.vat.tu.hang.hoa'].search([('id', '=', line.get('MA_HANG_ID'))],limit=1)
                new_line = env.new({
                        'MA_CCDC': hang.MA,
                        'TEN_CCDC': line.get('TEN_HANG'),
                        'NHOM_CCDC': line.get('TEN_HANG'),
                        'DVT': line.get('DVT_ID'),
                        'SO_LUONG': line.get('SO_LUONG'),
                        'DON_GIA': line.get('DON_GIA'),
                        'THANH_TIEN': line.get('THANH_TIEN'),
                        'NGAY_GHI_TANG': line.get('NGAY_HACH_TOAN'),
                        'SO_KY_PHAN_BO': 1,
                        'SO_TIEN_PHAN_BO_HANG_KY': line.get('THANH_TIEN'),
                        'TK_CHO_PHAN_BO_ID': tk_cho_pb,
                        'ID_GOC': line.get('ID_GOC'),
                        'MODEL_GOC': line.get('MODEL_GOC'),
                        'SO_CHUNG_TU_GHI_TANG' : self.env['ir.sequence'].next_by_code('supply_ghi_tang_SO_CT_GHI_TANG')
                })
                self.SUPPLY_GHI_TANG_HANG_LOAT_CHI_TIET_IDS += new_line
    
    @api.onchange('CHUNG_TU_GHI_GIAM_JSON')
    def _onchange_CHUNG_TU_GHI_GIAM_JSON(self):
        if self.CHUNG_TU_GHI_GIAM_JSON:
            chon_chung_tu = json.loads(self.CHUNG_TU_GHI_GIAM_JSON).get('SUPPLY_CHON_CHUNG_TU_GHI_GIAM_TSCD_CHI_TIET_IDS', [])
            tk_cho_pb = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '242')], limit = 1).id
            self.SUPPLY_GHI_TANG_HANG_LOAT_CHI_TIET_IDS = []
            env = self.env['supply.ghi.tang.hang.loat.chi.tiet']
            for line in chon_chung_tu:
                ma_ts = self.env['asset.ghi.tang'].search([('id', '=', line.get('MA_TAI_SAN_ID'))])
                new_line = env.new({
                        'MA_CCDC': ma_ts.MA_TAI_SAN,
                        'TEN_CCDC': line.get('TEN_TAI_SAN'),
                        # 'NHOM_CCDC': line.get('TEN_TAI_SAN'),
                        'SO_LUONG': 1,
                        'DON_GIA': line.get('GIA_TRI_CON_LAI'),
                        'THANH_TIEN': line.get('GIA_TRI_CON_LAI'),
                        'NGAY_GHI_TANG': line.get('NGAY_HACH_TOAN'),
                        'SO_KY_PHAN_BO': 1,
                        'SO_TIEN_PHAN_BO_HANG_KY': line.get('GIA_TRI_CON_LAI'),
                        'TK_CHO_PHAN_BO_ID': tk_cho_pb,
                        'ID_GOC': line.get('ID_GOC'),
                        'MODEL_GOC': line.get('MODEL_GOC'),
                        'SO_CHUNG_TU_GHI_TANG' : self.env['ir.sequence'].next_by_code('supply_ghi_tang_SO_CT_GHI_TANG')
                })
                self.SUPPLY_GHI_TANG_HANG_LOAT_CHI_TIET_IDS += new_line

    def _create_ghi_tang(self, doc):
        for line in doc.SUPPLY_GHI_TANG_HANG_LOAT_CHI_TIET_IDS:

            if line.MA_CCDC == False:
                raise ValidationError('Mã công cụ dụng cụ không được bỏ trống')
            elif line.TEN_CCDC == False:
                raise ValidationError('Tên công cụ dụng cụ không được bỏ trống')

            line_dtpb_ids = []            
            for dvsd in line.SUPPLY_GHI_TANG_THIET_LAP_PHAN_BO_IDS:
                line_dtpb_ids = [(0,0,{
                    'DOI_TUONG_PHAN_BO_ID': str(dvsd.DOI_TUONG_PHAN_BO_ID._name)+ ',' + str(dvsd.DOI_TUONG_PHAN_BO_ID.id),
                    'TEN_DOI_TUONG_PHAN_BO': dvsd.DOI_TUONG_PHAN_BO_ID.name,
                    'TY_LE_PB': dvsd.TY_LE_PB,
                    'TK_NO_ID': dvsd.TK_NO_ID.id,
                    'KHOAN_MUC_CP_ID': dvsd.KHOAN_MUC_CP_ID.id,
                    })]

            line_dvsd_ids = []
            for dtpb in line.SUPPLY_GHI_TANG_DON_VI_SU_DUNG_IDS:
                line_dvsd_ids = [(0,0,{
                    'MA_DON_VI_ID': dtpb.MA_DON_VI_ID.id,
                    'TEN_DON_VI': dtpb.TEN_DON_VI,
                    'SO_LUONG': dtpb.SO_LUONG,
                    
                    })]

            self.env['supply.ghi.tang'].create({
                'SO_CT_GHI_TANG' : line.SO_CHUNG_TU_GHI_TANG,
                'MA_CCDC': line.MA_CCDC,
                'name': line.TEN_CCDC,
                'LOAI_CCDC_ID': line.LOAI_CCDC_ID.id,
                'NHOM_CCDC': line.NHOM_CCDC,
                'LY_DO_GHI_TANG': line.LY_DO_GHI_TANG,
                'DON_VI_TINH': line.DVT,
                'SO_LUONG': line.SO_LUONG,
                'DON_GIA': line.DON_GIA,
                'THANH_TIEN': line.THANH_TIEN,
                'NGAY_GHI_TANG' : line.NGAY_GHI_TANG,
                'SO_KY_PHAN_BO' : line.SO_KY_PHAN_BO,
                'SO_TIEN_PHAN_BO_HANG_KY': line.SO_TIEN_PHAN_BO_HANG_KY,
                'TK_CHO_PHAN_BO_ID': line.TK_CHO_PHAN_BO_ID.id,
                'LOAI_CHUNG_TU' : 450,
                'SUPPLY_GHI_TANG_DON_VI_SU_DUNG_IDS' : line_dvsd_ids,
                'SUPPLY_GHI_TANG_THIET_LAP_PHAN_BO_IDS' : line_dtpb_ids,
                })

            
    
    @api.model
    def default_get(self, fields):
        rec = super(SUPPLY_GHI_TANG_CONG_CU_DUNG_CU_HANG_LOAT, self).default_get(fields)
        id_kiem_ke = self.get_context('default_ID_KIEM_KE')
        if id_kiem_ke:
            arr_tai_san = []
            kiem_ke = self.env['supply.kiem.ke.cong.cu.dung.cu'].search([('KIEM_KE_CCDC_ID', '=', id_kiem_ke)])
            rec['SUPPLY_GHI_TANG_HANG_LOAT_CHI_TIET_IDS'] = []
            for line in kiem_ke:
                if line.KIEN_NGHI_XU_LY == '0':
                    arr_dvst = []
                    
                    ghi_tang = self.env['supply.ghi.tang'].search([('id', '=', line.MA_CCDC_ID.id)])
                    kiem_ke_mt = self.env['supply.kiem.ke'].search([('id', '=', id_kiem_ke)])
                    tk_cho_pb = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', '242')], limit = 1).id
                    if ghi_tang.SO_KY_PHAN_BO:
                        so_tien_pb_hang_ky = (line.SO_LUONG_XU_LY*ghi_tang.DON_GIA)/ghi_tang.SO_KY_PHAN_BO
                    arr_dvst = [(0,0,{
                        'MA_DON_VI_ID' : line.MA_CCDC_ID.id,
                        'SO_LUONG' : line.SO_LUONG_XU_LY
                    })]
                    arr_tai_san += [(0,0,{
                        'MA_CCDC': line.MA_CCDC_ID.MA_CCDC,
                        'TEN_CCDC': line.TEN_CCDC,
                        'DVT' : line.DVT,
                        'SO_LUONG' : line.SO_LUONG_XU_LY,
                        'DON_GIA' : ghi_tang.DON_GIA,
                        'THANH_TIEN' : line.SO_LUONG_XU_LY*ghi_tang.DON_GIA,
                        # 'NGAY_GHI_TANG' : kiem_ke_mt.NGAY,
                        'SO_KY_PHAN_BO' : ghi_tang.SO_KY_PHAN_BO,
                        'SO_TIEN_PHAN_BO_HANG_KY' : so_tien_pb_hang_ky,
                        'TK_CHO_PHAN_BO_ID' : tk_cho_pb,
                        'SUPPLY_GHI_TANG_DON_VI_SU_DUNG_IDS' : arr_dvst
                    })]
            rec['SUPPLY_GHI_TANG_HANG_LOAT_CHI_TIET_IDS'] = arr_tai_san
        return rec
    