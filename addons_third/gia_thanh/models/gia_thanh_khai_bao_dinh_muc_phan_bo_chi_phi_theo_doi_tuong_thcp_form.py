# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class GIA_THANH_KHAI_BAO_DINH_MUC_PHAN_BO_CHI_PHI_THEO_DOI_TUONG_THCP_FORM(models.Model):
    _name = 'gia.thanh.kbdm.pbcp.theo.doi.tuong.thcp.form'
    _description = ''
    _inherit = ['mail.thread']
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    GIA_THANH_KHAI_BAO_DINH_MUC_PHAN_BO_CHI_PHI_THEO_DOI_TUONG_THCP_CHI_TIET_IDS = fields.One2many('gia.thanh.kbdm.pbcp.theo.dt.thcp.chi.tiet', 'CHI_TIET_ID', string='Khai báo định mức phân bổ chi phí theo đối tượng THCP chi tiết')

    def lay_du_lieu_gia_thanh_khai_bao_dinh_muc(self, args):
        new_line_khai_bao_dinh_muc_gia_thanh_thanh_pham = [[5]]
        chi_tiet_ids = self.env['gia.thanh.kbdm.pbcp.theo.dt.thcp.chi.tiet'].search([])
        arr_dtthcp = []
        if chi_tiet_ids:
            for line in chi_tiet_ids:
                new_line_khai_bao_dinh_muc_gia_thanh_thanh_pham += [(0,0,{
                    'DOI_TUONG_THCP_ID' : [line.DOI_TUONG_THCP_ID.id,line.DOI_TUONG_THCP_ID.MA_DOI_TUONG_THCP],
                    'TEN_DOI_TUONG_THCP' : line.DOI_TUONG_THCP_ID.TEN_DOI_TUONG_THCP,
                    'LOAI_DOI_TUONG_THCP' : line.LOAI_DOI_TUONG_THCP,
                    'TK_621' : line.TK_621,
                    'TK_622' : line.TK_622,
                    'TK_6271' : line.TK_6271,
                    'TK_6272' : line.TK_6272,
                    'TK_6273' : line.TK_6273,
                    'TK_6274' : line.TK_6274,
                    'TK_6277' : line.TK_6277,
                    'TK_6278' : line.TK_6278,
                    'TONG_CONG' : line.TONG_CONG,
                    })]
                if line.DOI_TUONG_THCP_ID.id not in arr_dtthcp:
                    arr_dtthcp.append(line.DOI_TUONG_THCP_ID.id)
        dtthcp_ids = self.env['danh.muc.doi.tuong.tap.hop.chi.phi'].search([])
        if dtthcp_ids:
            for dtthcp in dtthcp_ids:
                if dtthcp.id not in arr_dtthcp:
                    new_line_khai_bao_dinh_muc_gia_thanh_thanh_pham += [(0,0,{
                    'DOI_TUONG_THCP_ID' : [dtthcp.id,dtthcp.MA_DOI_TUONG_THCP],
                    'TEN_DOI_TUONG_THCP' : dtthcp.TEN_DOI_TUONG_THCP,
                    'LOAI_DOI_TUONG_THCP' : dtthcp.LOAI,
                    'TK_621' : 0,
                    'TK_622' : 0,
                    'TK_6271' : 0,
                    'TK_6272' : 0,
                    'TK_6273' : 0,
                    'TK_6274' : 0,
                    'TK_6277' : 0,
                    'TK_6278' : 0,
                    'TONG_CONG' : 0,
                    })]

        return {'GIA_THANH_KHAI_BAO_DINH_MUC_PHAN_BO_CHI_PHI_THEO_DOI_TUONG_THCP_CHI_TIET_IDS': new_line_khai_bao_dinh_muc_gia_thanh_thanh_pham,} 
    
    
    @api.model
    def create(self, values):
        chi_tiet_ids = self.env['gia.thanh.kbdm.pbcp.theo.dt.thcp.chi.tiet'].search([])
        if chi_tiet_ids:
            for chi_tiet in chi_tiet_ids:
                chi_tiet.unlink()
        master = self.env['gia.thanh.kbdm.pbcp.theo.doi.tuong.thcp.form'].search([])
        if master:
            for mt in master:
                mt.unlink()
        
        if values.get('GIA_THANH_KHAI_BAO_DINH_MUC_PHAN_BO_CHI_PHI_THEO_DOI_TUONG_THCP_CHI_TIET_IDS'):
            for line in values.get('GIA_THANH_KHAI_BAO_DINH_MUC_PHAN_BO_CHI_PHI_THEO_DOI_TUONG_THCP_CHI_TIET_IDS'):
                if line[2].get('TK_621') > 0 or line[2].get('TK_622') > 0 or line[2].get('TK_6271') > 0 or line[2].get('TK_6272') > 0 or line[2].get('TK_6273') > 0 or line[2].get('TK_6274') > 0 or line[2].get('TK_6277') > 0 or line[2].get('TK_6278') > 0:
                    self.env['gia.thanh.kbdm.pbcp.theo.dt.thcp.chi.tiet'].create(line[2])

        # tạo dữ liệu cho bảng gia.thanh.dinh.muc.phan.bo.cp.theo.thcp.va.tk
        # dict_luu_theo_tai_khoan = {}
        gia_thanh_theo_tk_va_dtthcp_ids = self.env['gia.thanh.dinh.muc.phan.bo.cp.theo.thcp.va.tk'].search([])
        if gia_thanh_theo_tk_va_dtthcp_ids:
            for chi_tiet in gia_thanh_theo_tk_va_dtthcp_ids:
                chi_tiet.unlink()

        arr_create_luu_theo_tk = []
        if values.get('GIA_THANH_KHAI_BAO_DINH_MUC_PHAN_BO_CHI_PHI_THEO_DOI_TUONG_THCP_CHI_TIET_IDS'):
            for line in values.get('GIA_THANH_KHAI_BAO_DINH_MUC_PHAN_BO_CHI_PHI_THEO_DOI_TUONG_THCP_CHI_TIET_IDS'):
                # if line[2].get('TK_621') > 0 or line[2].get('TK_622') > 0 or line[2].get('TK_6271') > 0 or line[2].get('TK_6272') > 0 or line[2].get('TK_6273') > 0 or line[2].get('TK_6274') > 0 or line[2].get('TK_6277') > 0 or line[2].get('TK_6278') > 0:
                if line[2].get('TK_621') > 0:
                    dict_luu_theo_tai_khoan = {
                        'DOI_TUONG_THCP_ID' : line[2].get('DOI_TUONG_THCP_ID'),
                        'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('621'),
                        'SO_TIEN' : line[2].get('TK_621'),
                    }
                    arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

                if line[2].get('TK_622') > 0:
                    dict_luu_theo_tai_khoan = {
                        'DOI_TUONG_THCP_ID' : line[2].get('DOI_TUONG_THCP_ID'),
                        'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('622'),
                        'SO_TIEN' : line[2].get('TK_622'),
                    }
                    arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

                if line[2].get('TK_6271') > 0:
                    dict_luu_theo_tai_khoan = {
                        'DOI_TUONG_THCP_ID' : line[2].get('DOI_TUONG_THCP_ID'),
                        'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6271'),
                        'SO_TIEN' : line[2].get('TK_6271'),
                    }
                    arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

                if line[2].get('TK_6272') > 0:
                    dict_luu_theo_tai_khoan = {
                        'DOI_TUONG_THCP_ID' : line[2].get('DOI_TUONG_THCP_ID'),
                        'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6272'),
                        'SO_TIEN' : line[2].get('TK_6272'),
                    }
                    arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

                if line[2].get('TK_6273') > 0:
                    dict_luu_theo_tai_khoan = {
                        'DOI_TUONG_THCP_ID' : line[2].get('DOI_TUONG_THCP_ID'),
                        'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6273'),
                        'SO_TIEN' : line[2].get('TK_6273'),
                    }
                    arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

                if line[2].get('TK_6274') > 0:
                    dict_luu_theo_tai_khoan = {
                        'DOI_TUONG_THCP_ID' : line[2].get('DOI_TUONG_THCP_ID'),
                        'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6274'),
                        'SO_TIEN' : line[2].get('TK_6274'),
                    }
                    arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

                if line[2].get('TK_6277') > 0:
                    dict_luu_theo_tai_khoan = {
                        'DOI_TUONG_THCP_ID' : line[2].get('DOI_TUONG_THCP_ID'),
                        'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6277'),
                        'SO_TIEN' : line[2].get('TK_6277'),
                    }
                    arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)

                if line[2].get('TK_6278') > 0:
                    dict_luu_theo_tai_khoan = {
                        'DOI_TUONG_THCP_ID' : line[2].get('DOI_TUONG_THCP_ID'),
                        'TAI_KHOAN_ID' : self.get_id_by_so_tai_khoan('6278'),
                        'SO_TIEN' : line[2].get('TK_6278'),
                    }
                    arr_create_luu_theo_tk.append(dict_luu_theo_tai_khoan)
            if arr_create_luu_theo_tk:
                for line in arr_create_luu_theo_tk:
                    self.env['gia.thanh.dinh.muc.phan.bo.cp.theo.thcp.va.tk'].create(line)


        values['GIA_THANH_KHAI_BAO_DINH_MUC_PHAN_BO_CHI_PHI_THEO_DOI_TUONG_THCP_CHI_TIET_IDS'] = {}
        result = super(GIA_THANH_KHAI_BAO_DINH_MUC_PHAN_BO_CHI_PHI_THEO_DOI_TUONG_THCP_FORM, self).create(values)

        return result
    
    def get_id_by_so_tai_khoan(self,so_tai_khoan):
        id = False
        tai_khoan = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', so_tai_khoan)],limit=1)
        if tai_khoan:
            id = tai_khoan.id
        return id


    # @api.model
    # def default_get(self, fields):
    #     rec = super(GIA_THANH_KHAI_BAO_DINH_MUC_PHAN_BO_CHI_PHI_THEO_DOI_TUONG_THCP_FORM, self).default_get(fields)
    #     # rec['Trường'] = Giá trị
    #     chi_tiet_ids = self.env['gia.thanh.kbdm.pbcp.theo.dt.thcp.chi.tiet'].search([])
        
    #     return rec
