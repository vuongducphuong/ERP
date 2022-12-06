# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime

class ACCOUNT_EX_CONG_NO_KHACH_HANG_EXCEL(models.Model):
    _name = 'chi.phi.do.dang.cong.trinh'
    _description = ''
    _auto = False

    MA_CONG_TRINH = fields.Char(string='Mã công trình (*)')
    
    NVL_TRUC_TIEP = fields.Float(string='NVL trực tiếp')
    NHAN_CONG_TRUOC_TIEP = fields.Float(string='Nhân công trực tiếp')
    MTC_NVL_GIAN_TIEP = fields.Float(string='NVL gián tiếp (Máy thi công)')
    MTC_NHAN_CONG = fields.Float(string='Nhân công (Máy thi công)')
    MTC_KHAU_HAO = fields.Float(string='Khấu hao (Máy thi công)')
    MTC_CHI_PHI_MUA_NGOAI = fields.Float(string='Chi phí mua ngoài (Máy thi công)')
    MTC_CHI_PHI_KHAC = fields.Float(string='Chi phí khác (Máy thi công)/Chi phí Máy thi công')
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

            du_lieu_trong_dtb = self.env['account.ex.chi.phi.do.dang'].search([('LOAI_CHI_PHI_DO_DANG','=','2')])
            i = 0
            for data in data_field:
                i += 1
                cong_trinh = False
                cong_trinh_id = False
                if data.get('MA_CONG_TRINH') != '':
                    cong_trinh = self.env['danh.muc.cong.trinh'].search([('MA_CONG_TRINH', '=', data.get('MA_CONG_TRINH').strip())])
                    if cong_trinh:
                        cong_trinh_id = cong_trinh.id
                    else:
                        thong_bao = u'Cột Mã công trình (*) dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong Danh mục/Công trình'
                        error.append({'type':'error', 'message' : thong_bao})
                else:
                    thong_bao = u'Cột Mã công trình (*) dòng thứ ' + str(i) + u' là trường bắt buộc nhập vui long nhập để import'
                    error.append({'type':'error', 'message' : thong_bao})

                tai_khoan_do_dang = False
                if data.get('TK_CPSXKD_DO_DANG') != '':
                    tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', data.get('TK_CPSXKD_DO_DANG').strip())])
                    if tai_khoan:
                        tai_khoan_do_dang = tai_khoan.id
                    else:
                        thong_bao = u'Cột TK CPSXKD dở dang dòng thứ ' + str(i) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/hệ thống tài khoản'
                        error.append({'type':'error', 'message' : thong_bao})
                
                key_data_excel = str(cong_trinh_id)
                arr_excel.append(key_data_excel)
                
                if cong_trinh_id not in dict_create:
                    dict_create[cong_trinh_id] = []

                line_ids = dict_create[cong_trinh_id]

                # tính tổng chi phí của máy thi công
                MTC_CHI_PHI_NVL_GIAN_TIEP = float(data.get('MTC_NVL_GIAN_TIEP')) if data.get('MTC_NVL_GIAN_TIEP') != '' else False
                MTC_CHI_PHI_NHAN_CONG = float(data.get('MTC_NHAN_CONG')) if data.get('MTC_NHAN_CONG') !='' else False
                MTC_CHI_PHI_KHAU_HAO_DAU_KY = float(data.get('MTC_KHAU_HAO')) if data.get('MTC_KHAU_HAO') !='' else False
                MTC_CHI_PHI_MUA_NGOAI_DAU_KY = float(data.get('MTC_CHI_PHI_MUA_NGOAI')) if data.get('MTC_CHI_PHI_MUA_NGOAI') !='' else False
                MTC_CHI_PHI_KHAC_CHUNG = float(data.get('MTC_CHI_PHI_KHAC')) if data.get('MTC_CHI_PHI_KHAC') !='' else False
                MTC_TONG = MTC_CHI_PHI_NVL_GIAN_TIEP + MTC_CHI_PHI_NHAN_CONG + MTC_CHI_PHI_KHAU_HAO_DAU_KY + MTC_CHI_PHI_MUA_NGOAI_DAU_KY + MTC_CHI_PHI_KHAC_CHUNG

                # tính tổng chi phí chung
                CHI_PHI_CHUNG_CHI_PHI_NVL_GIAN_TIEP = float(data.get('NVL_GIAN_TIEP')) if data.get('NVL_GIAN_TIEP') !='' else False
                CHI_PHI_CHUNG_CHI_PHI_NHAN_CONG_GIAN_TIEP = float(data.get('NHAN_CONG_GIAN_TIEP')) if data.get('NHAN_CONG_GIAN_TIEP') !='' else False
                CHI_PHI_CHUNG_CHI_PHI_KHAU_HAO_DAU_KY = float(data.get('KHAU_HAO')) if data.get('KHAU_HAO') !='' else False
                CHI_PHI_CHUNG_CHI_PHI_MUA_NGOAI_DAU_KY = float(data.get('CHI_PHI_MUA_NGOAI')) if data.get('CHI_PHI_MUA_NGOAI') !='' else False
                CHI_PHI_CHUNG_CHI_PHI_KHAC_CHUNG = float(data.get('CHI_PHI_KHAC_CHUNG')) if data.get('CHI_PHI_KHAC_CHUNG') !='' else False
                TONG_CHI_PHI = CHI_PHI_CHUNG_CHI_PHI_NVL_GIAN_TIEP + CHI_PHI_CHUNG_CHI_PHI_NHAN_CONG_GIAN_TIEP + CHI_PHI_CHUNG_CHI_PHI_KHAU_HAO_DAU_KY + CHI_PHI_CHUNG_CHI_PHI_MUA_NGOAI_DAU_KY + CHI_PHI_CHUNG_CHI_PHI_KHAC_CHUNG

                CHI_PHI_NVL_TRUC_TIEP = float(data.get('NVL_TRUC_TIEP')) if data.get('NVL_TRUC_TIEP') != '' else False
                CHI_PHI_NHAN_CONG_TRUC_TIEP = float(data.get('NHAN_CONG_TRUOC_TIEP')) if data.get('NHAN_CONG_TRUOC_TIEP') != '' else False

                du_lieu_1_dong = {
                    'MA_CONG_TRINH_ID' : cong_trinh_id,
                    'TEN_CONG_TRINH' : cong_trinh.TEN_CONG_TRINH,
                    'LOAI_CONG_TRINH' : cong_trinh.LOAI_CONG_TRINH.id,

                    'CHI_PHI_NVL_TRUC_TIEP' : CHI_PHI_NVL_TRUC_TIEP,  
                    'CHI_PHI_NHAN_CONG_TRUC_TIEP' : CHI_PHI_NHAN_CONG_TRUC_TIEP,  

                    'MTC_CHI_PHI_NVL_GIAN_TIEP' : MTC_CHI_PHI_NVL_GIAN_TIEP,  
                    'MTC_CHI_PHI_NHAN_CONG' : MTC_CHI_PHI_NHAN_CONG,
                    'MTC_CHI_PHI_KHAU_HAO_DAU_KY' : MTC_CHI_PHI_KHAU_HAO_DAU_KY,
                    'MTC_CHI_PHI_MUA_NGOAI_DAU_KY' : MTC_CHI_PHI_MUA_NGOAI_DAU_KY,
                    'MTC_CHI_PHI_KHAC_CHUNG' : MTC_CHI_PHI_KHAC_CHUNG,

                    'CHI_PHI_NVL_GIAN_TIEP' : CHI_PHI_CHUNG_CHI_PHI_NVL_GIAN_TIEP,
                    'CHI_PHI_NHAN_CONG_GIAN_TIEP' : CHI_PHI_CHUNG_CHI_PHI_NHAN_CONG_GIAN_TIEP,
                    'CHI_PHI_KHAU_HAO' : CHI_PHI_CHUNG_CHI_PHI_KHAU_HAO_DAU_KY,
                    'CHI_PHI_MUA_NGOAI' : CHI_PHI_CHUNG_CHI_PHI_MUA_NGOAI_DAU_KY,
                    'CHI_PHI_KHAC_CHUNG' : CHI_PHI_CHUNG_CHI_PHI_KHAC_CHUNG,
                    'SO_DA_NGHIEM_THU' : float(data.get('SO_DA_NGHIEM_THU')) if data.get('SO_DA_NGHIEM_THU') !='' else False,
                    'TAI_KHOAN_CPSXKD_DO_DANG_ID' : tai_khoan_do_dang,
                    'LOAI_CHI_PHI_DO_DANG' : '2',
                    'MTC_TONG' : MTC_TONG,
                    'TONG_CHI_PHI' : TONG_CHI_PHI,
                    'TONG' : MTC_TONG + TONG_CHI_PHI + CHI_PHI_NVL_TRUC_TIEP + CHI_PHI_NHAN_CONG_TRUC_TIEP,
                    # 'DON_GIA' : float(data.get('GIA_TRI_TON'))/float(data.get('SO_LUONG')) if data.get('GIA_TRI_TON') != '' and data.get('SO_LUONG') != '' and float(data.get('SO_LUONG')) != 0 else 0,
                    # 'DON_GIA_THEO_DVT_CHINH' : float(data.get('GIA_TRI_TON'))/float(data.get('SO_LUONG')) if data.get('GIA_TRI_TON') != '' and data.get('SO_LUONG') != '' and float(data.get('SO_LUONG')) != 0 else 0,

                }                    
                line_ids += [(0,0,du_lieu_1_dong)]

            if du_lieu_trong_dtb:
                for du_lieu in du_lieu_trong_dtb:
                    key_data_base = str(du_lieu.MA_CONG_TRINH_ID.id)
                    
                    # dict_database[key_data_base] = du_lieu
                    if key_data_base not in arr_excel:
                        cong_trinh_id = du_lieu.MA_CONG_TRINH_ID.id

                        if cong_trinh_id not in dict_create:
                            dict_create[cong_trinh_id] = []

                        line_ids = dict_create[cong_trinh_id]
                        du_lieu_1_dong = {
                            'MA_CONG_TRINH_ID' : du_lieu.MA_CONG_TRINH_ID.id, 
                            'TEN_CONG_TRINH' : du_lieu.TEN_CONG_TRINH, 
                            'LOAI_CONG_TRINH' : du_lieu.LOAI_CONG_TRINH.id, 
                            'CHI_PHI_NVL_TRUC_TIEP' : du_lieu.CHI_PHI_NVL_TRUC_TIEP, 
                            'CHI_PHI_NHAN_CONG_TRUC_TIEP' : du_lieu.CHI_PHI_NHAN_CONG_TRUC_TIEP, 
                            'MTC_CHI_PHI_NVL_GIAN_TIEP' : du_lieu.MTC_CHI_PHI_NVL_GIAN_TIEP,  
                            'MTC_CHI_PHI_NHAN_CONG' : du_lieu.MTC_CHI_PHI_NHAN_CONG,  
                            'MTC_CHI_PHI_KHAU_HAO_DAU_KY' : du_lieu.MTC_CHI_PHI_KHAU_HAO_DAU_KY,  
                            'MTC_CHI_PHI_MUA_NGOAI_DAU_KY' : du_lieu.MTC_CHI_PHI_MUA_NGOAI_DAU_KY, 
                            'MTC_CHI_PHI_KHAC_CHUNG' : du_lieu.MTC_CHI_PHI_KHAC_CHUNG, 
                            'CHI_PHI_NVL_GIAN_TIEP' : du_lieu.CHI_PHI_NVL_GIAN_TIEP, 
                            'CHI_PHI_NHAN_CONG_GIAN_TIEP' : du_lieu.CHI_PHI_NHAN_CONG_GIAN_TIEP, 
                            'CHI_PHI_KHAU_HAO' : du_lieu.CHI_PHI_KHAU_HAO, 
                            'CHI_PHI_MUA_NGOAI' : du_lieu.CHI_PHI_MUA_NGOAI, 
                            'CHI_PHI_KHAC_CHUNG' : du_lieu.CHI_PHI_KHAC_CHUNG, 
                            'SO_DA_NGHIEM_THU' : du_lieu.SO_DA_NGHIEM_THU, 
                            'MTC_TONG' : du_lieu.MTC_TONG,
                            'TONG_CHI_PHI' : du_lieu.TONG_CHI_PHI,
                            'TONG' : du_lieu.TONG,
                            
                            'TAI_KHOAN_CPSXKD_DO_DANG_ID' : du_lieu.TAI_KHOAN_CPSXKD_DO_DANG_ID.id,
                            'LOAI_CHI_PHI_DO_DANG' : '2',
                        }                    
                        line_ids += [(0,0,du_lieu_1_dong)]
            
            # tạo mới dữ liệu
            for cong_trinh in dict_create:
                self.env['account.ex.chi.phi.do.dang.master'].create({
                    # 'KHO_ID': kho_create,
                    'ACCOUNT_EX_CHI_PHI_DO_DANG_IDS': dict_create[cong_trinh],
                })
            # if dict_loi:
            #     for key in dict_loi:
            #         thong_bao = u'cột ' +dict_loi[key]+ ' dòng thứ ' + str(key) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/kho'
            #         error.append({'type':'error', 'message' : thong_bao})
        if error == []:
            return {}
        else:
            return {'messages' : error}