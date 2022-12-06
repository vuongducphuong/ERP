# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, fields, models, helper
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.addons import decimal_precision

class PURCHASE_EX_BU_TRU_CONG_NO(models.Model):
    _name = 'purchase.ex.bu.tru.cong.no'
    _description = 'Bù trừ công nợ'
    _auto = False

    DOI_TUONG_ID = fields.Many2one('res.partner', string='Đối tượng', help='Đối tượng')
    TK_PHAI_THU_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK phải thu', help='Tài khoản phải thu')
    TK_PHAI_TRA_ID = fields.Many2one('danh.muc.he.thong.tai.khoan', string='TK phải trả', help='Tài khoản phải trả')
    NGAY_BU_TRU = fields.Date(string='Ngày bù trừ', help='Ngày bù trừ',default=fields.Datetime.now)
    currency_id = fields.Many2one('res.currency', string='Loại tiền',oldname='LOAI_TIEN_ID')
    name = fields.Char(string='Name', help='Name', oldname='NAME')
    #FIELD_IDS = fields.One2many('model.name')
    @api.model
    def default_get(self, fields_list):
      result = super(PURCHASE_EX_BU_TRU_CONG_NO, self).default_get(fields_list)
      result['TK_PHAI_THU_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','131')]).id
      result['TK_PHAI_TRA_ID'] = self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN','=','331')]).id
      result['currency_id'] = self.env['res.currency'].search([('MA_LOAI_TIEN','=','VND')],limit=1).id
      return result
    PURCHASE_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS = fields.One2many('purchase.bu.tru.cong.no.chung.tu.phai.tra', 'BU_TRU_CONG_NO_ID', string='Bù trừ công nợ chứng từ phải trả')
    PURCHASE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS = fields.One2many('purchase.ex.bu.tru.cong.no.chung.tu.phai.thu', 'BU_TRU_CONG_NO_ID', string='Bù trừ công nợ chứng từ phải thu')

    def _validate(self):
        params = self._context
        DOI_TUONG_ID= params['DOI_TUONG_ID'] if 'DOI_TUONG_ID' in params.keys() else 'False'
        PURCHASE_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS= params['PURCHASE_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS'] if 'PURCHASE_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS' in params.keys() else 'False'
        PURCHASE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS= params['PURCHASE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS'] if 'PURCHASE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS' in params.keys() else 'False'
        if(DOI_TUONG_ID=='False'):
            raise ValidationError('<Đối tượng> không được bỏ trống.')
        elif PURCHASE_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS =='False' :
            raise ValidationError('Bạn phải chọn các chứng từ để thực hiện bù trừ.')
        elif PURCHASE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS == 'False':
            raise ValidationError('Bạn phải chọn các chứng từ để thực hiện bù trừ.')

    def action_view_result(self):
        self._validate()
        action = self.env.ref('purchase_ex.action_open_purchase_ex_bu_tru_cong_no_form').read()[0]
        id_doituong = self.get_context('DOI_TUONG_ID')
        id_tkthu = self.get_context('TK_PHAI_THU_ID')
        id_tktra = self.get_context('TK_PHAI_TRA_ID')
        id_loaitien = self.get_context('currency_id')
        ma_doi_tuong = self.env['res.partner'].search([('id', '=', id_doituong)], limit=1).MA
        ma_tai_khoan_thu = self.env['danh.muc.he.thong.tai.khoan'].search([('id', '=', id_tkthu)], limit=1).SO_TAI_KHOAN
        ma_tai_khoan_tra = self.env['danh.muc.he.thong.tai.khoan'].search([('id', '=', id_tktra)], limit=1).SO_TAI_KHOAN
        ten_loai_tien = self.env['res.currency'].search([('id', '=', id_loaitien)], limit=1).name
        name = self.env['res.partner'].search([('id', '=', id_doituong)], limit=1).HO_VA_TEN
        str1 = 'Bù trừ công nợ phải thu, phải trả với ' + str(name)
        chung_tu_phai_tra_ids = self.get_context('PURCHASE_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS')
        chung_tu_phai_thu_ids = self.get_context('PURCHASE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS')
        sotien = 0
        for line in chung_tu_phai_thu_ids:
            sotien += line.get('SO_TIEN_BU_TRU')
        arr1 = []
        arr2 = []

        arr1 += [(0, 0, {
            'DIEN_GIAI' : 'Bù trừ công nợ phải thu, phải trả',
            'TK_NO_ID' : ma_tai_khoan_tra,
            'TK_CO_ID' : ma_tai_khoan_thu,
            'SO_TIEN': sotien,
            # 'NHAN_VIEN_ID' :  ,
            # 'KHOAN_MUC_CP' : ,
            # 'DON_VI_ID' : ,
            # 'MA_THONG_KE_ID' : ,
            })]
        # for 
        #     for line in chung_tu_phai_thu_ids:
        #         if line['CHON'] == 'True':
        #             arr2 += [(0, 0, {
                        # 'MA_HANG_ID' : dl.MA_HANG_ID.SO_TAI_KHOAN,
                        # 'TEN_HANG' : dl.MA_HANG_ID.TEN,
                        # 'TK_THUE_ID' : dl.TK_THUE_NK_ID.SO_TAI_KHOAN,
                        # 'TK_CO_ID' : dl.tk_cong_no_id.SO_TAI_KHOAN,
                        # 'GIA_TRI_HHDV_CHUA_THUE' : giatrihhchuathue ,
                        # 'DIEN_GIAI_THUE' : dl.dien_giai_thue,
                        # 'PHAN_TRAM_THUE_GTGT_ID' : dl.tax_name,
                        # 'TIEN_THUE_GTGT' : dl.TONG_TIEN_THUE_GTGT,
                        # 'NHOM_HHDV_MUA_VAO_ID' : dl.NHOM_HHDV_ID.name,
                        # 'DON_MUA_HANG_ID' : dl.don_mua_hang_id.name,
                        # 'SO_CHUNG_TU' : dl.chung_tu_id,
                        # 'CONG_TRINH_ID' : dl.cong_trinh_id.MA_CONG_TRINH,
                        # 'HOP_DONG_MUA_ID' : dl.HOP_DONG_MUA_ID,
                        # 'MA_THONG_KE_ID' : dl.ma_thong_ke_id,
                        # })]
                    

        context = {
            'default_DOI_TUONG': ma_doi_tuong,
            'default_TEN_DOI_TUONG': name ,
            'default_TK_PHAI_THU': ma_tai_khoan_thu,
            'default_TK_PHAI_TRA': ma_tai_khoan_tra,
            'default_LY_DO': str1,
            'default_NGAY_BU_TRU':self.get_vntime('NGAY_BU_TRU'),
            'default_LOAI_TIEN':  ten_loai_tien,
            'default_PURCHASE_EX_CHUNG_TRU_BU_TRU_CONG_NO_KET_QUA_HACH_TOAN_IDS' : arr1,
        }
        action['context'] = helper.Obj.merge(context, action.get('context'))
        # action['options'] = {'clear_breadcrumbs': True}
        return action

    @api.onchange('DOI_TUONG_ID')
    def update_DOI_TUONG_ID(self):
       if self.DOI_TUONG_ID:
            env_phai_tra = self.env['purchase.bu.tru.cong.no.chung.tu.phai.tra']
            env_phai_thu = self.env['purchase.ex.bu.tru.cong.no.chung.tu.phai.thu']
            self.PURCHASE_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS = []
            self.PURCHASE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS = []
            # ct_thanh_toans = self.env['account.move.line'].get_move_lines_for_manual_reconciliation(self.TK_PHAI_THU_ID.id,self.DOI_TUONG_ID.id)

            ct_thanh_toans = [
                {
                    "debit": 50000000,
                    "date" : '2018-12-20',
                    "name" : 'Mua hàng của công ty Minh Anh'
                } ,
                {
                    "credit": 20000000,
                    "date" : '2018-12-30',
                    "name" : 'Mua hàng của công ty Bảo Anh'
                } 
            ]

            for ct in ct_thanh_toans:
                if ct.get('debit'):
                    new_line_phai_tra = env_phai_tra.new({
                        'SO_TIEN': ct.get('debit'),
                        'NGAY_CHUNG_TU' : ct.get('date'),
                        'SO_CON_NO' : ct.get('debit'),
                        'DIEN_GIAI' : ct.get('name'),
                    })
                    self.PURCHASE_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS += new_line_phai_tra
                if ct.get('credit') :
                    new_line_phai_thu = env_phai_thu.new({
                        'SO_TIEN': ct.get('credit'),
                        'NGAY_CHUNG_TU' : ct.get('date'),
                        'SO_CHUA_THU' : ct.get('credit'),
                        'DIEN_GIAI' : ct.get('name'),
                    })
                    self.PURCHASE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS += new_line_phai_thu
    
    @api.depends('PURCHASE_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS.CHON')
    def bu_tru_phai_thu(self):
        tong_tien_phai_tra = 0
        tong_tien_phai_thu = 0
        for line in self.PURCHASE_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS:
            if line.CHON == True:
                tong_tien_phai_tra += line.SO_CON_NO
        for line in self.PURCHASE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS:
            if line.CHON == True:
                tong_tien_phai_thu += line.SO_CHUA_THU
        if tong_tien_phai_thu > 0 and tong_tien_phai_tra > 0:
            if tong_tien_phai_tra > tong_tien_phai_thu:
                for line in self.PURCHASE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS:
                    if line.CHON == True:
                        line.SO_TIEN_BU_TRU = line.SO_CHUA_THU
                for line1 in self.PURCHASE_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS:
                    if line1.CHON == True:
                        if tong_tien_phai_thu == 0:
                        #     line1.SO_TIEN_BU_TRU = line1.SO_CHUA_DOI_TRU
                        # if tong_tien_phai_thu == 1:
                            line1.SO_TIEN_BU_TRU = 0
                        elif line1.SO_CON_NO < tong_tien_phai_thu:
                            line1.SO_TIEN_BU_TRU = line1.SO_CON_NO
                            tong_tien_phai_thu = tong_tien_phai_thu - line1.SO_TIEN_BU_TRU
                        elif line1.SO_CON_NO > tong_tien_phai_thu:
                            line1.SO_TIEN_BU_TRU = tong_tien_phai_thu
                            tong_tien_phai_thu = 0
            elif tong_tien_phai_tra < tong_tien_phai_thu:
                for line1 in self.PURCHASE_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS:
                    if line1.CHON == True:
                        # if line1.SO_CHUA_DOI_TRU > tong_tien_phai_thu:
                        #     line1.SO_TIEN_BU_TRU = tong_tien_phai_thu
                        #     tong_tien_phai_thu = 0
                        line1.SO_TIEN_BU_TRU = line1.SO_TIEN

                for line in self.PURCHASE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS:
                    if line.CHON == True:
                        if tong_tien_phai_tra == 0:
                            #line.SO_TIEN_BU_TRU = line.SO_CON_NO
                        # if tong_tien_phai_tra == 1:
                            line.SO_TIEN_BU_TRU = 0
                        elif tong_tien_phai_tra > line.SO_CHUA_THU:
                            line.SO_TIEN_BU_TRU = line.SO_CHUA_THU
                            tong_tien_phai_tra = tong_tien_phai_tra - line.SO_TIEN_BU_TRU
                        elif tong_tien_phai_tra  < line.SO_CHUA_THU:
                            line.SO_TIEN_BU_TRU = tong_tien_phai_tra
                            tong_tien_phai_tra = 0

    @api.depends('PURCHASE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS.CHON')
    def bu_tru_phai_tra(self):
        tong_tien_phai_tra = 0
        tong_tien_phai_thu = 0
        for line in self.PURCHASE_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS:
            if line.CHON == True:
                tong_tien_phai_tra += line.SO_CON_NO
        for line in self.PURCHASE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS:
            if line.CHON == True:
                tong_tien_phai_thu += line.SO_CHUA_THU
        if tong_tien_phai_thu > 0 and tong_tien_phai_tra > 0:
            if tong_tien_phai_tra > tong_tien_phai_thu:
                for line in self.PURCHASE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS:
                    if line.CHON == True:
                        line.SO_TIEN_BU_TRU = line.SO_CHUA_THU
                for line1 in self.PURCHASE_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS:
                    if line1.CHON == True:
                        if tong_tien_phai_thu == 0:
                        #     line1.SO_TIEN_BU_TRU = line1.SO_CHUA_DOI_TRU
                        # if tong_tien_phai_thu == 1:
                            line1.SO_TIEN_BU_TRU = 0
                        elif line1.SO_CON_NO < tong_tien_phai_thu:
                            line1.SO_TIEN_BU_TRU = line1.SO_CON_NO
                            tong_tien_phai_thu = tong_tien_phai_thu - line1.SO_TIEN_BU_TRU
                        elif line1.SO_CON_NO > tong_tien_phai_thu:
                            line1.SO_TIEN_BU_TRU = tong_tien_phai_thu
                            tong_tien_phai_thu = 0
            elif tong_tien_phai_tra < tong_tien_phai_thu:
                for line1 in self.PURCHASE_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS:
                    if line1.CHON == True:
                        # if line1.SO_CHUA_DOI_TRU > tong_tien_phai_thu:
                        #     line1.SO_TIEN_BU_TRU = tong_tien_phai_thu
                        #     tong_tien_phai_thu = 0
                        line1.SO_TIEN_BU_TRU = line1.SO_TIEN

                for line in self.PURCHASE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS:
                    if line.CHON == True:
                        if tong_tien_phai_tra == 0:
                            #line.SO_TIEN_BU_TRU = line.SO_CON_NO
                        # if tong_tien_phai_tra == 1:
                            line.SO_TIEN_BU_TRU = 0
                        elif tong_tien_phai_tra > line.SO_CON_NO:
                            line.SO_TIEN_BU_TRU = line.SO_CON_NO
                            tong_tien_phai_tra = tong_tien_phai_tra - line.SO_TIEN_BU_TRU
                        elif tong_tien_phai_tra  < line.SO_CON_NO:
                            line.SO_TIEN_BU_TRU = tong_tien_phai_tra
                            tong_tien_phai_tra = 0
