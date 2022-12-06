# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields
from odoo.addons import decimal_precision

class BAO_CAO_01TT_PHIEU_THU_MAU_A5(models.Model):
    _name = 'bao.cao.01tt.phieu.thu.a5'
    _auto = False

    
    ref = fields.Char(string='Reffence ID')
    ID_CHUNG_TU =  fields.Integer(string='ID chứng từ')
    MODEL_CHUNG_TU =  fields.Char(string='Model chứng từ')
    NGUOI_NHAN_NGUOI_NOP =  fields.Char(string='Người nhận người nộp')#ContactName
    NGAY_CHUNG_TU =  fields.Date(string='Ngày chứng từ') #RefDate
    NGAY_HACH_TOAN =  fields.Date(string='Ngày hạch toán') #PostedDate
    SO_CHUNG_TU =  fields.Char(string='Số chứng từ') #RefNo
    MA_KHACH_HANG =  fields.Char(string='Mã khách hàng') #AccountObjectName
    TEN_KHACH_HANG =  fields.Char(string='Tên khách hàng') #AccountObjectName
    DIA_CHI =  fields.Char(string='Địa chỉ') #AccountObjectAddress
    DIEN_GIAI =  fields.Char(string='Diễn giải') #JournalMemo
    LOAI_TIEN =  fields.Char(string='Loại tiền') #CurrencyID
    TY_GIA =  fields.Monetary(string='Tỷ giá', currency_field='currency_id') #ExchangeRate
    SO_CT_GOC_KEM_THEO =  fields.Integer(string='Số chứng từ kèm theo') #DocumentIncluded

    TK_NO = fields.Char(string='TK Nợ', help='Tài khoản nợ')#DebitAccount
    TK_CO = fields.Char(string='TK Có', help='Tài khoản có')#CreditAccount
    

    
    LOAI_KHACH_HANG =  fields.Integer(string='Loại đối tượng') #AccountObjectType

    TONG_TIEN =  fields.Monetary(string='Tổng tiền', currency_field='currency_id')
    TONG_TIEN_QUY_DOI =  fields.Monetary(string='Tổng tiền quy đổi', currency_field='currency_id')
    
    CHI_NHANH_ID = fields.Many2one('danh.muc.to.chuc', string='Chi nhánh', default=lambda self: self.get_chi_nhanh())
    currency_id = fields.Many2one('res.currency', string='Loại tiền', help='Loại tiền', default=lambda self: self.lay_loai_tien_mac_dinh())

    ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS = fields.One2many('bao.cao.01tt.phieu.thu.a5.chi.tiet', 'PHIEU_THU_CHI_ID', string='Phiếu thu chi tiết')

    

class BAO_CAO_01TT_PHIEU_THU_MAU_A5_REPORT(models.AbstractModel):
    _name = 'report.bao_cao.template_v01_tt_a5'

    @api.model
    def get_report_values(self, docids, data=None):
        refTypeList, records = self.get_reftype_list(data)
        ############### START SQL lấy dữ liệu ###############
        env = self.env['report.bao_cao.template_v01_tt']
        ####################### END SQL #######################
        sql_result = env.ham_lay_du_lieu_sql_tra_ve(refTypeList)

        dic_tk_no  = {}
        dic_tk_co  = {}

        for line in sql_result:
            key = str(line.get('MODEL_CHUNG_TU')) + ',' + str(line.get('ID_CHUNG_TU'))

            
            if key not in dic_tk_no:
                dic_tk_no[key] = []
            if key not in dic_tk_co:
                dic_tk_co[key] = []

            if line.get('TK_NO') and line.get('TK_NO') not in dic_tk_no[key]:
                dic_tk_no[key] += [line.get('TK_NO')]

            if line.get('TK_CO') and line.get('TK_CO') not in dic_tk_co[key]:
                dic_tk_co[key] += [line.get('TK_CO')]

            master_data = self.env['bao.cao.01tt.phieu.thu.a5'].convert_for_update(line)
            detail_data = self.env['bao.cao.01tt.phieu.thu.a5.chi.tiet'].convert_for_update(line)
            if records.get(key):
                records[key].update(master_data)
                records[key].ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS += self.env['bao.cao.01tt.phieu.thu.a5.chi.tiet'].new(detail_data)
        
        for key in records:
            if key in dic_tk_no:
                records[key].TK_NO = ', '.join(dic_tk_no[key])
            if key in dic_tk_co:
                records[key].TK_CO = ', '.join(dic_tk_co[key])

        docs = [records.get(k) for k in records]

        for record in docs:
            
            if not record.LOAI_TIEN:
                record.currency_id = self.lay_loai_tien_mac_dinh()
            else:
                loai_tien_id = self.env['res.currency'].search([('MA_LOAI_TIEN', '=', record.LOAI_TIEN)],limit=1)
                if loai_tien_id:
                    record.currency_id = loai_tien_id.id

            tong_tien = 0
            tong_tien_quy_doi = 0
            for line in record.ACCOUNT_EX_PHIEU_THU_CHI_TIET_IDS:
                line.currency_id = record.currency_id
                tong_tien += line.THANH_TIEN
                tong_tien_quy_doi += line.SO_TIEN
            record.TONG_TIEN = tong_tien
            record.TONG_TIEN_QUY_DOI = tong_tien_quy_doi
           
        
        return {
            'docs': docs,
        }