# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime

class ACCOUNT_EX_CONG_NO_KHACH_HANG_EXCEL(models.Model):
    _name = 'chi.phi.do.dang.don.hang'
    _description = ''
    _auto = False

    SO_DON_HANG = fields.Char(string='Số đơn hàng (*)')
    
    NVL_TRUC_TIEP = fields.Float(string='NVL trực tiếp')
    NHAN_CONG_TRUOC_TIEP = fields.Float(string='Nhân công trực tiếp')
    NVL_GIAN_TIEP = fields.Float(string='NVL gián tiếp')
    NHAN_CONG_GIAN_TIEP = fields.Float(string='Nhân công gián tiếp')
    KHAU_HAO = fields.Float(string='Khấu hao')
    CHI_PHI_MUA_NGOAI = fields.Float(string='Chi phí mua ngoài')
    CHI_PHI_KHAC_CHUNG = fields.Float(string='Chi phí khác/Chi phí chung')
    SO_DA_NGHIEM_THU = fields.Float(string='Số đã nghiệm thu')
    TK_CPSXKD_DO_DANG = fields.Float(string='TK CPSXKD dở dang')
    


    def import_from_excel(self, import_fields, data):
        # 1. trường hợp import thông thuwongf, gọi vào hàm load()
        if data and import_fields:
            dict_create = {}
            arr_excel = []
            dict_loi = {}
            error = []

            data_field = []
            for row in data:
                j = 0
                row_field = {}
                for field in import_fields:
                    row_field[field] = row[j]
                    j += 1
                data_field.append(row_field)

            du_lieu_trong_dtb = self.env['account.ex.chi.phi.do.dang'].search([('LOAI_CHI_PHI_DO_DANG','=','3')])
            i = 0
            for data in data_field:
                i += 1
                don_hang = False
                don_hang_id = False
                if data.get('SO_DON_HANG') != '':
                    don_hang = self.env['account.ex.don.dat.hang'].search([('SO_DON_HANG', '=', data.get('SO_DON_HANG').strip())])
                    if don_hang:
                        don_hang_id = don_hang.id
                    else:
                        thong_bao = u'Cột Số đơn hàng (*) dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong Danh mục/Đơn đặt hàng'
                        error.append({'type':'error', 'message' : thong_bao})
                else:
                    thong_bao = u'Cột Số đơn hàng (*) dòng thứ ' + str(i) + u' là trường bắt buộc nhập vui long nhập để import'
                    error.append({'type':'error', 'message' : thong_bao})

                tai_khoan_do_dang = False
                if data.get('TK_CPSXKD_DO_DANG') != '':
                    tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', data.get('TK_CPSXKD_DO_DANG').strip())])
                    if tai_khoan:
                        tai_khoan_do_dang = tai_khoan.id
                    else:
                        thong_bao = u'Cột TK CPSXKD dở dang dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/hệ thống tài khoản'
                        error.append({'type':'error', 'message' : thong_bao})
                
                key_data_excel = str(don_hang_id)
                arr_excel.append(key_data_excel)
                
                if don_hang_id not in dict_create:
                    dict_create[don_hang_id] = []

                line_ids = dict_create[don_hang_id]

                # tính tổng chi phí chung
                # tính tổng chi phí chung
                CHI_PHI_NVL_GIAN_TIEP = float(data.get('NVL_GIAN_TIEP')) if data.get('NVL_GIAN_TIEP') !='' else False
                CHI_PHI_NHAN_CONG_GIAN_TIEP = float(data.get('NHAN_CONG_GIAN_TIEP')) if data.get('NHAN_CONG_GIAN_TIEP') !='' else False
                CHI_PHI_KHAU_HAO = float(data.get('KHAU_HAO')) if data.get('KHAU_HAO') !='' else False
                CHI_PHI_MUA_NGOAI = float(data.get('CHI_PHI_MUA_NGOAI')) if data.get('CHI_PHI_MUA_NGOAI') !='' else False
                CHI_PHI_KHAC_CHUNG = float(data.get('CHI_PHI_KHAC_CHUNG')) if data.get('CHI_PHI_KHAC_CHUNG') !='' else False
                TONG_CHI_PHI = CHI_PHI_NVL_GIAN_TIEP + CHI_PHI_NHAN_CONG_GIAN_TIEP + CHI_PHI_KHAU_HAO + CHI_PHI_MUA_NGOAI + CHI_PHI_KHAC_CHUNG

                CHI_PHI_NVL_TRUC_TIEP = float(data.get('NVL_TRUC_TIEP')) if data.get('NVL_TRUC_TIEP') != '' else False
                CHI_PHI_NHAN_CONG_TRUC_TIEP = float(data.get('NHAN_CONG_TRUOC_TIEP')) if data.get('NHAN_CONG_TRUOC_TIEP') != '' else False
                SO_DA_NGHIEM_THU = float(data.get('SO_DA_NGHIEM_THU')) if data.get('SO_DA_NGHIEM_THU') != '' else False

                du_lieu_1_dong = {
                    'DON_HANG_ID' : don_hang_id,
                    'SO_DON_HANG' : don_hang.SO_DON_HANG,
                    'NGAY_DON_HANG' : don_hang.NGAY_DON_HANG,
                    'DIEN_GIAI' : don_hang.DIEN_GIAI,
                    'KHACH_HANG_ID' : don_hang.KHACH_HANG_ID.id,

                    'CHI_PHI_NVL_TRUC_TIEP' : CHI_PHI_NVL_TRUC_TIEP,  
                    'CHI_PHI_NHAN_CONG_TRUC_TIEP' : CHI_PHI_NHAN_CONG_TRUC_TIEP,  
                
                    'CHI_PHI_NVL_GIAN_TIEP' : CHI_PHI_NVL_GIAN_TIEP,
                    'CHI_PHI_NHAN_CONG_GIAN_TIEP' : CHI_PHI_NHAN_CONG_GIAN_TIEP,
                    'CHI_PHI_KHAU_HAO' : CHI_PHI_KHAU_HAO,
                    'CHI_PHI_MUA_NGOAI' : CHI_PHI_MUA_NGOAI,
                    'CHI_PHI_KHAC_CHUNG' : CHI_PHI_KHAC_CHUNG,
                    'TAI_KHOAN_CPSXKD_DO_DANG_ID' : tai_khoan_do_dang,
                    'LOAI_CHI_PHI_DO_DANG' : '3',
                    'TONG' : TONG_CHI_PHI + CHI_PHI_NVL_TRUC_TIEP + CHI_PHI_NHAN_CONG_TRUC_TIEP,
                    'TONG_CHI_PHI' : TONG_CHI_PHI,
                    'SO_DA_NGHIEM_THU' : SO_DA_NGHIEM_THU,

                }                    
                line_ids += [(0,0,du_lieu_1_dong)]

            if du_lieu_trong_dtb:
                for du_lieu in du_lieu_trong_dtb:
                    key_data_base = str(du_lieu.DON_HANG_ID.id)
                    
                    # dict_database[key_data_base] = du_lieu
                    if key_data_base not in arr_excel:
                        don_hang_id = du_lieu.DON_HANG_ID.id

                        if don_hang_id not in dict_create:
                            dict_create[don_hang_id] = []

                        line_ids = dict_create[don_hang_id]
                        du_lieu_1_dong = {
                            'DON_HANG_ID' : du_lieu.DON_HANG_ID.id, 
                            'SO_DON_HANG' : du_lieu.SO_DON_HANG, 
                            'NGAY_DON_HANG' : du_lieu.NGAY_DON_HANG,
                            'DIEN_GIAI' : du_lieu.DIEN_GIAI,
                            'KHACH_HANG_ID' : du_lieu.KHACH_HANG_ID.id, 
                            'CHI_PHI_NVL_TRUC_TIEP' : du_lieu.CHI_PHI_NVL_TRUC_TIEP, 
                            'CHI_PHI_NHAN_CONG_TRUC_TIEP' : du_lieu.CHI_PHI_NHAN_CONG_TRUC_TIEP, 
                            
                            'CHI_PHI_NVL_GIAN_TIEP' : du_lieu.CHI_PHI_NVL_GIAN_TIEP, 
                            'CHI_PHI_NHAN_CONG_GIAN_TIEP' : du_lieu.CHI_PHI_NHAN_CONG_GIAN_TIEP, 
                            'CHI_PHI_KHAU_HAO' : du_lieu.CHI_PHI_KHAU_HAO, 
                            'CHI_PHI_MUA_NGOAI' : du_lieu.CHI_PHI_MUA_NGOAI, 
                            'CHI_PHI_KHAC_CHUNG' : du_lieu.CHI_PHI_KHAC_CHUNG, 
                            'TONG_CHI_PHI' : du_lieu.TONG_CHI_PHI, 
                            'TONG' : du_lieu.TONG,
                            'SO_DA_NGHIEM_THU' : du_lieu.SO_DA_NGHIEM_THU,
                            
                            'TAI_KHOAN_CPSXKD_DO_DANG_ID' : du_lieu.TAI_KHOAN_CPSXKD_DO_DANG_ID.id,
                            'LOAI_CHI_PHI_DO_DANG' : '3',
                        }                    
                        line_ids += [(0,0,du_lieu_1_dong)]
            
            # tạo mới dữ liệu
            for don_hang in dict_create:
                self.env['account.ex.chi.phi.do.dang.master'].create({
                    # 'KHO_ID': kho_create,
                    'ACCOUNT_EX_CHI_PHI_DO_DANG_IDS': dict_create[don_hang],
                })
            # if dict_loi:
            #     for key in dict_loi:
            #         thong_bao = u'cột ' +dict_loi[key]+ ' dòng thứ ' + str(key) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/kho'
            #         error.append({'type':'error', 'message' : thong_bao})
        if error == []:
            return {}
        else:
            return {'messages' : error}