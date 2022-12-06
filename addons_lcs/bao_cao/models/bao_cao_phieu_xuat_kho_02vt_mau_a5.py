# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_PHIEU_XUAT_KHO_02VT_MAU_A5(models.Model):
    _name = 'bao.cao.phieu.xuat.kho.02vt.mau.a5'
    _auto = False

    ref = fields.Char(string='Reffence ID')
    
    ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
    LOAI_CHUNG_TU =  fields.Integer(string='Loại chứng từ') #RefType
    LOAI_KHACH_HANG =  fields.Integer(string='Loại đối tượng') #AccountObjectType
    MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')
    ID_CHUNG_TU_CHI_TIET =  fields.Integer(string='ID chứng từ chi tiết')
    NGAY_CHUNG_TU =  fields.Date(string='Ngày chứng từ')
    SO_CHUNG_TU =  fields.Char(string='Số chứng từ')
    TEN_KHACH_HANG =  fields.Char(string='Tên khách hàng')
    TEN_NGUOI_NHAN_NOP =  fields.Char(string='Tên người nhận nộp')
    DIA_CHI =  fields.Char(string='Địa chỉ')
    DIEN_GIAI =  fields.Char(string='Diễn giải')
    LIST_TK_KHO =  fields.Char(string='Danh sách tài khoản kho')
    LIST_TK_NO =  fields.Char(string='Danh sách tài khoản nợ')
    LIST_TK_CO =  fields.Char(string='Danh sách tài khoản có')
    DIA_DIEM_KHO =  fields.Char(string='Địa điểm kho')
    SO_CT_GOC_KEM_THEO =  fields.Integer(string='Số chứng từ kèm theo')
    STT =  fields.Integer(string='Số thứ tự')
    TONG_TIEN =  fields.Monetary(string='Tổng tiền', currency_field='currency_id')
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())
    NGUOI_NHAN_HANG =  fields.Char(string='Người nhận hàng')
    
    PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS = fields.One2many('bao.cao.phieu.xuat.kho.02vt.mau.a5.chi.tiet', 'CHUNG_TU_TRA_LAI_HANG_MUA_ID')
    

class BAO_CAO_PHIEU_XUAT_KHO_02VT_MAU_A5_REPORT(models.AbstractModel):
    _name = 'report.bao_cao.template_v02_vt_a5'

    @api.model
    def get_report_values(self, docids, data=None):
        ############### START SQL lấy dữ liệu ###############
        refTypeList, records = self.get_reftype_list(data,'stock.ex.nhap.xuat.kho')
        
        env = self.env['report.bao_cao.template_02_vt']
        sql_result = env.ham_lay_du_lieu_sql(refTypeList)
        ####################### END SQL #######################

        # Tạo object để in
        for line in sql_result:
            key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))
            master_data = self.env['bao.cao.phieu.xuat.kho.02vt.mau.a5'].convert_for_update(line)
            detail_data = self.env['bao.cao.phieu.xuat.kho.02vt.mau.a5.chi.tiet'].convert_for_update(line)
            if records.get(key):
                records[key].update(master_data)
                records[key].PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS += self.env['bao.cao.phieu.xuat.kho.02vt.mau.a5.chi.tiet'].new(detail_data)
        
        docs = [records.get(k) for k in records]
        for record in docs:
            if record.LIST_TK_CO:
                if len(record.LIST_TK_CO) > 2 :
                    record.LIST_TK_CO = record.LIST_TK_CO[0 : len(record.LIST_TK_CO) - 2]

            if record.LIST_TK_NO:
                if len(record.LIST_TK_NO) > 2 :
                    record.LIST_TK_NO = record.LIST_TK_NO[0 : len(record.LIST_TK_NO) - 2]

            if record.LIST_TK_KHO:
                if len(record.LIST_TK_KHO) > 2 :
                    record.LIST_TK_KHO = record.LIST_TK_KHO[0 : len(record.LIST_TK_KHO) - 2]

            if record.DIA_DIEM_KHO == '\n':
                record.DIA_DIEM_KHO = False

            if record.LOAI_CHUNG_TU == 2023 or record.LOAI_CHUNG_TU == 2024 or  record.LOAI_CHUNG_TU == 2025: 
                record.NGUOI_NHAN_HANG = record.TEN_KHACH_HANG
            else:
                record.NGUOI_NHAN_HANG = record.TEN_NGUOI_NHAN_NOP

            strTenKhachHang = ''

            if record.TEN_KHACH_HANG == False:
                record.TEN_KHACH_HANG = ''
            if record.TEN_NGUOI_NHAN_NOP == False:
                record.TEN_NGUOI_NHAN_NOP = ''
            if record.TEN_KHACH_HANG != '' and record.TEN_NGUOI_NHAN_NOP != '':
                if record.LOAI_KHACH_HANG == 0:
                    strTenKhachHang = record.TEN_NGUOI_NHAN_NOP + ' - ' + record.TEN_KHACH_HANG
                else:
                    strTenKhachHang = record.TEN_NGUOI_NHAN_NOP
            else:
                if record.TEN_KHACH_HANG != '':
                    strTenKhachHang = record.TEN_KHACH_HANG
                elif record.TEN_NGUOI_NHAN_NOP != '':
                    strTenKhachHang = record.TEN_NGUOI_NHAN_NOP
                else:
                    strTenKhachHang = False
            record.TEN_KHACH_HANG  = strTenKhachHang


            tong_tien = 0
            if record.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS:
                for line in record.PURCHASE_EX_CHI_TIET_CHUNG_TU_TRA_LAI_HANG_MUA_IDS:
                    tong_tien +=  line.SO_TIEN
            record.TONG_TIEN = tong_tien
            record.currency_id = self.lay_loai_tien_mac_dinh()
        return {
            'docs': docs,
        }
