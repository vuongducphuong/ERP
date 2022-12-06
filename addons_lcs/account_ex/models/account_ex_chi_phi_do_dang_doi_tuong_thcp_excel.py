# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime

class ACCOUNT_EX_CONG_NO_KHACH_HANG_EXCEL(models.Model):
    _name = 'chi.phi.do.dang.doi.tuong.thcp'
    _description = ''
    _auto = False

    MA_DOI_TUONG_THCP = fields.Char(string='Mã đối tượng THCP')
    
    NVL_TRUC_TIEP = fields.Float(string='NVL trực tiếp')
    NHAN_CONG_TRUOC_TIEP = fields.Float(string='Nhân công trực tiếp')
    NVL_GIAN_TIEP = fields.Float(string='NVL gián tiếp')
    NHAN_CONG_GIAN_TIEP = fields.Float(string='Nhân công gián tiếp')
    KHAU_HAO = fields.Float(string='Khấu hao')
    CHI_PHI_MUA_NGOAI = fields.Float(string='Chi phí mua ngoài')
    CHI_PHI_KHAC_CHUNG = fields.Float(string='Chi phí khác/Chi phí chung')
    # SO_DA_NGHIEM_THU = fields.Float(string='Số đã nghiệm thu')
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

            du_lieu_trong_dtb = self.env['account.ex.chi.phi.do.dang'].search([('LOAI_CHI_PHI_DO_DANG','=','1')])
            i = 0
            for data in data_field:
                i += 1
                doi_tuong_thcp = False
                doi_tuong_thcp_id = False
                if data.get('MA_DOI_TUONG_THCP') != '':
                    doi_tuong_thcp = self.env['danh.muc.doi.tuong.tap.hop.chi.phi'].search([('MA_DOI_TUONG_THCP', '=', data.get('MA_DOI_TUONG_THCP').strip())])
                    if doi_tuong_thcp:
                        doi_tuong_thcp_id = doi_tuong_thcp.id
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
                
                key_data_excel = str(doi_tuong_thcp_id)
                arr_excel.append(key_data_excel)
                
                if doi_tuong_thcp_id not in dict_create:
                    dict_create[doi_tuong_thcp_id] = []

                line_ids = dict_create[doi_tuong_thcp_id]

                
                # tính tổng chi phí chung
                CHI_PHI_NVL_GIAN_TIEP = float(data.get('NVL_GIAN_TIEP')) if data.get('NVL_GIAN_TIEP') !='' else False
                CHI_PHI_NHAN_CONG_GIAN_TIEP = float(data.get('NHAN_CONG_GIAN_TIEP')) if data.get('NHAN_CONG_GIAN_TIEP') !='' else False
                CHI_PHI_KHAU_HAO = float(data.get('KHAU_HAO')) if data.get('KHAU_HAO') !='' else False
                CHI_PHI_MUA_NGOAI = float(data.get('CHI_PHI_MUA_NGOAI')) if data.get('CHI_PHI_MUA_NGOAI') !='' else False
                CHI_PHI_KHAC_CHUNG = float(data.get('CHI_PHI_KHAC_CHUNG')) if data.get('CHI_PHI_KHAC_CHUNG') !='' else False
                TONG_CHI_PHI = CHI_PHI_NVL_GIAN_TIEP + CHI_PHI_NHAN_CONG_GIAN_TIEP + CHI_PHI_KHAU_HAO + CHI_PHI_MUA_NGOAI + CHI_PHI_KHAC_CHUNG

                CHI_PHI_NVL_TRUC_TIEP = float(data.get('NVL_TRUC_TIEP')) if data.get('NVL_TRUC_TIEP') != '' else False
                CHI_PHI_NHAN_CONG_TRUC_TIEP = float(data.get('NHAN_CONG_TRUOC_TIEP')) if data.get('NHAN_CONG_TRUOC_TIEP') != '' else False

                du_lieu_1_dong = {
                    'MA_DOI_TUONG_THCP_ID' : doi_tuong_thcp_id,
                    'TEN_DOI_TUONG_THCP' : doi_tuong_thcp.TEN_DOI_TUONG_THCP,
                    'LOAI_DOI_TUONG_THCP' : doi_tuong_thcp.LOAI,

                    'CHI_PHI_NVL_TRUC_TIEP' : CHI_PHI_NVL_TRUC_TIEP,  
                    'CHI_PHI_NHAN_CONG_TRUC_TIEP' : CHI_PHI_NHAN_CONG_TRUC_TIEP,  
                
                    'CHI_PHI_NVL_GIAN_TIEP' : CHI_PHI_NVL_GIAN_TIEP,
                    'CHI_PHI_NHAN_CONG_GIAN_TIEP' : CHI_PHI_NHAN_CONG_GIAN_TIEP,
                    'CHI_PHI_KHAU_HAO' : CHI_PHI_KHAU_HAO,
                    'CHI_PHI_MUA_NGOAI' : CHI_PHI_MUA_NGOAI,
                    'CHI_PHI_KHAC_CHUNG' : CHI_PHI_KHAC_CHUNG,
                    'TAI_KHOAN_CPSXKD_DO_DANG_ID' : tai_khoan_do_dang,
                    'LOAI_CHI_PHI_DO_DANG' : '1',
                    'TONG' : TONG_CHI_PHI + CHI_PHI_NVL_TRUC_TIEP + CHI_PHI_NHAN_CONG_TRUC_TIEP,
                    'TONG_CHI_PHI' : TONG_CHI_PHI,

                }                    
                line_ids += [(0,0,du_lieu_1_dong)]

            if du_lieu_trong_dtb:
                for du_lieu in du_lieu_trong_dtb:
                    key_data_base = str(du_lieu.MA_DOI_TUONG_THCP_ID.id)
                    
                    # dict_database[key_data_base] = du_lieu
                    if key_data_base not in arr_excel:
                        doi_tuong_thcp_id = du_lieu.MA_DOI_TUONG_THCP_ID.id

                        if doi_tuong_thcp_id not in dict_create:
                            dict_create[doi_tuong_thcp_id] = []

                        line_ids = dict_create[doi_tuong_thcp_id]
                        du_lieu_1_dong = {
                            'MA_DOI_TUONG_THCP_ID' : du_lieu.MA_DOI_TUONG_THCP_ID.id, 
                            'TEN_DOI_TUONG_THCP' : du_lieu.TEN_DOI_TUONG_THCP, 
                            'LOAI_DOI_TUONG_THCP' : du_lieu.LOAI_DOI_TUONG_THCP, 
                            'CHI_PHI_NVL_TRUC_TIEP' : du_lieu.CHI_PHI_NVL_TRUC_TIEP, 
                            'CHI_PHI_NHAN_CONG_TRUC_TIEP' : du_lieu.CHI_PHI_NHAN_CONG_TRUC_TIEP, 
                            
                            'CHI_PHI_NVL_GIAN_TIEP' : du_lieu.CHI_PHI_NVL_GIAN_TIEP, 
                            'CHI_PHI_NHAN_CONG_GIAN_TIEP' : du_lieu.CHI_PHI_NHAN_CONG_GIAN_TIEP, 
                            'CHI_PHI_KHAU_HAO' : du_lieu.CHI_PHI_KHAU_HAO, 
                            'CHI_PHI_MUA_NGOAI' : du_lieu.CHI_PHI_MUA_NGOAI, 
                            'CHI_PHI_KHAC_CHUNG' : du_lieu.CHI_PHI_KHAC_CHUNG, 
                            'TONG_CHI_PHI' : du_lieu.TONG_CHI_PHI, 
                            'TONG' : du_lieu.TONG,
                            
                            'TAI_KHOAN_CPSXKD_DO_DANG_ID' : du_lieu.TAI_KHOAN_CPSXKD_DO_DANG_ID.id,
                            'LOAI_CHI_PHI_DO_DANG' : '1',
                        }                    
                        line_ids += [(0,0,du_lieu_1_dong)]
            
            # tạo mới dữ liệu
            for doi_tuong_thcp in dict_create:
                self.env['account.ex.chi.phi.do.dang.master'].create({
                    'ACCOUNT_EX_CHI_PHI_DO_DANG_IDS': dict_create[doi_tuong_thcp],
                })
            # if dict_loi:
            #     for key in dict_loi:
            #         thong_bao = u'cột ' +dict_loi[key]+ ' dòng thứ ' + str(key) + u' sai kiểu dữ liệu hoặc chưa tồn tại trong danh mục/kho'
            #         error.append({'type':'error', 'message' : thong_bao})
        if error == []:
            return {}
        else:
            return {'messages' : error}